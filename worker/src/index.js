/**
 * Bot Telegram Cousin Marc — version Cloudflare Workers (instantanee).
 *
 * 1) Tu envoies une photo a ton bot avec une legende (cote2, tpi 1xbet, tpi melbet, resultat,
 *    + "site" / "canal", ou "canal" seul). Telegram previent le Worker immediatement :
 *      - la photo est enregistree dans le depot GitHub (le site l'affiche),
 *      - elle est publiee dans le canal,
 *      - le bot te repond + t'envoie le texte pour WhatsApp.
 * 2) Messages promo automatiques a 6h00 et 21h00 (heure du Cameroun) via les Cron Triggers.
 *
 * Secrets a definir dans Cloudflare (Settings > Variables and Secrets) :
 *   TELEGRAM_BOT_TOKEN   jeton du bot (@BotFather)
 *   TELEGRAM_ALLOWED_ID  ton identifiant Telegram (834076281)
 *   GITHUB_TOKEN         cle GitHub "fine-grained" : depot marc-pronostic-api, Contents = Read and write
 *   WEBHOOK_SECRET       un mot de passe que tu inventes (lettres et chiffres, sans espace)
 * Variable facultative :
 *   TELEGRAM_CHANNEL_ID  ton canal (par defaut @marc_prono)
 */
import { RESP, FOOTER, HELP as HELP_TXT, COUPON_DU_JOUR, TARGETS, PROMOS, VIP_RAPPELS, VIP_IMAGE, MIDI, MIDI_BK, EN, withEn } from "./messages.js";

const REPO = "fokamjeanmarc2004-cloud/marc-pronostic-api";
const SITE = "https://cousinmarc-pronostic.com";
const EMOJI_PACK = "https://t.me/addemoji/FFN_emojis";
const COMMANDS = "\n\n🎨 Commandes :\n/emojis → ton pack d'emojis FFN\n/stickers → ton pack de stickers (le crée la 1re fois)\n/affiche → l'outil pour fabriquer une affiche avec ton code";
const HELP = HELP_TXT.replace("mis à jour en 5 à 15 minutes", "mis à jour en quelques secondes") + COMMANDS;

// ---------------------------------------------------------------- Stickers
// Un emoji associe a chaque image du dossier stickers/ du depot (meme ordre alphabetique).
const STICKER_EMOJIS = ["🔥", "🔥", "⚠️", "✅", "🎯", "⭐", "👇", "🎁", "🔥", "🔥", "🔥", "🔥", "💰", "🎯", "🙏"];

async function stickerSetName(env) {
  const me = await tg(env, "getMe", {});
  return { name: `cousinmarc_ffn_by_${me.username}`, bot: me.username };
}

async function stickerSetLink(env) {
  const { name } = await stickerSetName(env);
  try { await tg(env, "getStickerSet", { name }); return `https://t.me/addstickers/${name}`; } catch (e) { return null; }
}

// Cree le pack la premiere fois (images lues dans le depot GitHub) et renvoie le lien.
async function ensureStickers(env, userId) {
  const existing = await stickerSetLink(env);
  if (existing) return { link: existing, created: false };
  const { name } = await stickerSetName(env);
  const list = await (await gh(env, "contents/stickers?ref=main")).json();
  if (!Array.isArray(list)) throw new Error("dossier stickers/ introuvable dans le depot GitHub");
  const files = list.filter((f) => /\.png$/i.test(f.name)).sort((a, b) => a.name.localeCompare(b.name)).slice(0, 50);
  if (!files.length) throw new Error("aucune image dans stickers/");
  const form = new FormData();
  form.append("user_id", String(userId));
  form.append("name", name);
  form.append("title", "Cousin Marc · Code promo FFN");
  const stickers = [];
  for (let i = 0; i < files.length; i++) {
    const img = await fetch(files[i].download_url);
    form.append(`s${i}`, new Blob([await img.arrayBuffer()], { type: "image/png" }), files[i].name);
    stickers.push({ sticker: `attach://s${i}`, format: "static", emoji_list: [STICKER_EMOJIS[i] || "🔥"] });
  }
  form.append("stickers", JSON.stringify(stickers));
  const r = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/createNewStickerSet`, { method: "POST", body: form });
  const out = await r.json();
  if (!out.ok) throw new Error(`createNewStickerSet: ${out.description || r.status}`);
  return { link: `https://t.me/addstickers/${name}`, created: true, count: files.length };
}

async function handleCommand(env, chatId, userId, text) {
  const cmd = text.trim().split(/[\s@]/)[0].toLowerCase();
  if (cmd === "/emojis") {
    await reply(env, chatId, `😎 Ton pack d'emojis animés FFN :\n${EMOJI_PACK}\n\n(Les emojis personnalisés s'écrivent à la main dans Telegram : le bot ne peut pas les envoyer à ta place.)`);
  } else if (cmd === "/stickers") {
    try {
      const s = await ensureStickers(env, userId);
      await reply(env, chatId, `${s.created ? `✅ Pack créé (${s.count} stickers) !` : "✅ Ton pack de stickers :"}\n${s.link}\n\nPartage ce lien dans ton canal et tes groupes.`);
    } catch (e) {
      console.log("stickers", e.message);
      await reply(env, chatId, `⚠️ Impossible de créer le pack : ${e.message}`);
    }
  } else if (cmd === "/affiche" || cmd === "/moncode") {
    await reply(env, chatId, `🖼️ Fabrique une affiche avec ton prénom et ton code promo :\n${SITE}/affiche.html\n\nChoisis le bookmaker, télécharge l'image, partage-la.`);
  } else {
    await reply(env, chatId, HELP);
  }
}

// ---------------------------------------------------------------- Telegram
async function tg(env, method, params) {
  const r = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/${method}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(params),
  });
  const out = await r.json();
  if (!out.ok) throw new Error(`${method}: ${out.description || r.status}`);
  return out.result;
}

async function reply(env, chatId, text) {
  try {
    await tg(env, "sendMessage", { chat_id: chatId, text, disable_web_page_preview: true });
  } catch (e) {
    console.log("reponse impossible", e.message);
  }
}

const channelOf = (env) => (env.TELEGRAM_CHANNEL_ID || "").trim() || "@marc_prono";

// ---------------------------------------------------------------- Legendes
function norm(t) {
  return (t || "").normalize("NFKC").trim().toLowerCase().replace(/\s+/g, " ");
}

export function parseCaption(caption) {
  const lines = (caption || "").trim().split(/\r?\n/);
  let first = norm(lines[0] || "");
  const comment = lines.slice(1).join("\n").trim();
  let toChannel = true, toSite = true;
  if (first === "canal") return { label: "Canal", file: null, text: "", comment, toChannel: true, toSite: false };
  if (first.endsWith(" site")) { first = first.slice(0, -5).trim(); toChannel = false; }
  else if (first.endsWith(" canal")) { first = first.slice(0, -6).trim(); toSite = false; }
  for (const t of TARGETS) {
    if (new RegExp(t.pattern).test(first)) return { label: t.label, file: t.file, text: t.text, comment, toChannel, toSite };
  }
  return { label: null, file: null, text: null, comment, toChannel, toSite };
}

export function channelText(text, comment, en) {
  const body = [comment, text].filter(Boolean).join("\n\n");
  return withEn(body || "⚽ Cousin Marc", en);
}

// ---------------------------------------------------------------- GitHub
function toBase64(bytes) {
  const u8 = new Uint8Array(bytes);
  let bin = "";
  for (let i = 0; i < u8.length; i += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return btoa(bin);
}

async function gh(env, path, init = {}) {
  return fetch(`https://api.github.com/repos/${REPO}/${path}`, {
    ...init,
    headers: {
      "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
      "Accept": "application/vnd.github+json",
      "User-Agent": "cousinmarc-bot",
      "X-GitHub-Api-Version": "2022-11-28",
      ...(init.headers || {}),
    },
  });
}

async function saveToGithub(env, file, bytes, label) {
  const current = await gh(env, `contents/${file}?ref=main`);
  const sha = current.ok ? (await current.json()).sha : undefined;
  const r = await gh(env, `contents/${file}`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      message: `Coupon mis a jour depuis Telegram (${label})`,
      content: toBase64(bytes),
      branch: "main",
      ...(sha ? { sha } : {}),
      committer: { name: "cousinmarc-bot", email: "cousinmarc-bot@users.noreply.github.com" },
    }),
  });
  if (!r.ok) throw new Error(`GitHub ${r.status}: ${(await r.text()).slice(0, 200)}`);
}


// ---------------------------------------------------------------- Preuves VIP (legende « vip »)
// Ligne 1 : vip (ou « vip canal » pour publier aussi dans le canal)
// Ligne 2 (facultatif) : le match, la cote et le gain, ex : Rennes – OFI Crète · cote 11 · 3 850 000 F
export function parseVip(caption) {
  const lines = (caption || "").trim().split(/\r?\n/);
  const first = norm(lines[0] || "");
  if (!/^vip( canal)?$/.test(first)) return null;
  const rest = lines.slice(1).join(" ").trim();
  let cote = "", gain = "";
  // le gain : un grand nombre suivi de F / FCFA (ex : 3 850 000 F, 2.675.000 FCFA, 2515000F)
  const mg = rest.match(/(?:gains?\s*:?\s*)?(\d{1,3}(?:[\s.]\d{3})+|\d{5,})\s*(?:f|fcfa|xaf|xof)\b/i);
  if (mg) gain = mg[1].replace(/[\s.]/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " F";
  const restA = mg ? rest.replace(mg[0], " · ") : rest;
  // la cote : « cote 11 », « @12.9 » ou un nombre a virgule seul (ex : 5.03)
  const mc = restA.match(/cote\s*:?\s*@?\s*(\d+(?:[.,]\d+)?)/i) || restA.match(/@\s*(\d+(?:[.,]\d+)?)/) || restA.match(/(?:^|\s)(\d{1,3}[.,]\d{1,2})(?=\s|$|·)/);
  if (mc) cote = mc[1].replace(",", ".");
  let titre = restA.replace(mc ? mc[0] : "", " ").replace(/[·|,;-]\s*$/g, "").replace(/\s*[·|]\s*[·|]\s*/g, " · ").replace(/^[\s·|,;-]+|[\s·|,;-]+$/g, "").trim();
  if (!titre) titre = "Ticket gagnant VIP";
  return { toChannel: first.endsWith("canal"), titre: "⚽ " + titre, cote, gain };
}

async function addVipProof(env, bytes, info) {
  const d = new Date().toISOString().replace(/\D/g, "").slice(0, 14);
  const file = `tg-${d}.jpg`;
  await saveToGithub(env, `promo/preuves/${file}`, bytes, "preuve VIP");
  // liste des preuves (lue par la page VIP du site et par les images du rappel de 13h)
  const path = "promo/preuves/preuves.json";
  for (let essai = 0; essai < 3; essai++) {
    const cur = await gh(env, `contents/${path}?ref=main`);
    if (!cur.ok) throw new Error(`GitHub ${cur.status}`);
    const meta = await cur.json();
    const bin = atob(meta.content.replace(/\n/g, ""));
    const list = JSON.parse(new TextDecoder().decode(Uint8Array.from(bin, (ch) => ch.charCodeAt(0))));
    list.unshift({ file, titre: info.titre, cote: info.cote, gain: info.gain, date: new Date().toISOString().slice(0, 10) });
    const body = new TextEncoder().encode(JSON.stringify(list, null, 1));
    const r = await gh(env, `contents/${path}`, {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ message: "Nouvelle preuve VIP depuis Telegram", content: toBase64(body), branch: "main", sha: meta.sha,
        committer: { name: "cousinmarc-bot", email: "cousinmarc-bot@users.noreply.github.com" } }),
    });
    if (r.ok) return file;
    if (r.status !== 409) throw new Error(`GitHub ${r.status}: ${(await r.text()).slice(0, 200)}`);
  }
  throw new Error("GitHub : conflit, réessaie");
}

const VIP_POST = "━━━━━━━━━━━━━━━━━━━━━━━━━━\n⭐ ENCORE UN TICKET GAGNANT DANS LE VIP\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🏆 Mes tickets gagnants : https://cousinmarc-pronostic.com/vip.html#preuves\n💳 Dès 25 000 FCFA par mois · Orange Money, MTN, Wave ou crypto\n👉 https://cousinmarc-pronostic.com/vip.html\n━━━━━━━━━━━━━━━━━━━━━━━━━━\nAucun gain n'est garanti.";


// ---------------------------------------------------------------- Resultats des matchs (message « score »)
// Une ligne par match :  score Roma Real 2-1 gagné   (ou perdu / remboursé ; le score est facultatif)
function plain(t) {
  return (t || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}
const RES_WORDS = { gagne: "gagne", gagner: "gagne", win: "gagne", perdu: "perdu", perd: "perdu", rembourse: "rembourse", annule: "rembourse" };

export function parseScoreLine(line) {
  let t = plain(line).replace(/^(score|scores|resultat|resultats)\s+/, "");
  const words = t.split(" ");
  const res = RES_WORDS[words[words.length - 1]];
  if (!res) return null;
  t = words.slice(0, -1).join(" ");
  let score = "";
  const ms = line.match(/(\d+)\s*[-:–]\s*(\d+)/);
  if (ms) { score = `${ms[1]}-${ms[2]}`; t = t.replace(new RegExp(`\\b${ms[1]}\\s+${ms[2]}\\b`), " "); }
  const teams = t.split(" ").filter((w) => w.length >= 3 && !/^\d+$/.test(w));
  return teams.length ? { teams, res, score } : null;
}

export function applyScores(text, lines, now = new Date()) {
  const blocks = text.split("\n---\n");
  const done = [], missing = [];
  for (const L of lines) {
    let best = -1, bestDate = "";
    blocks.forEach((b, i) => {
      const d = (b.match(/^date:\s*(.+)$/m) || [])[1];
      const e1 = (b.match(/^equipe1:\s*(.+)$/m) || [])[1], e2 = (b.match(/^equipe2:\s*(.+)$/m) || [])[1];
      if (!d || !e1 || !e2) return;
      if (new Date(d.trim().replace(" ", "T") + ":00+01:00") > now) return;
      const names = plain(e1 + " " + e2);
      if (!L.teams.every((w) => names.includes(w))) return;
      if (d > bestDate) { bestDate = d; best = i; }
    });
    if (best < 0) { missing.push(L.teams.join(" ")); continue; }
    let b = blocks[best].replace(/^resultat:.*\n?/m, "");
    b = b.replace(/^(bookmaker:.*)$/m, `$1\nresultat: ${L.res}`);
    if (!/^resultat:/m.test(b)) b = b.replace(/^(cote:.*)$/m, `$1\nresultat: ${L.res}`);
    const e1 = b.match(/^equipe1:\s*(.+)$/m)[1].trim(), e2 = b.match(/^equipe2:\s*(.+)$/m)[1].trim();
    if (L.score) {
      b = b.replace(/\nScore final : .*$/m, "");
      const [a, c] = L.score.split("-");
      b = b.replace(/\s*$/, "") + `\nScore final : ${e1} ${a}-${c} ${e2}.`;
    }
    blocks[best] = b;
    done.push(`${e1} – ${e2}${L.score ? " " + L.score : ""} : ${L.res === "gagne" ? "✅ gagné" : L.res === "perdu" ? "❌ perdu" : "↩️ remboursé"}`);
  }
  return { text: blocks.join("\n---\n"), done, missing };
}

async function handleScores(env, chatId, msgText) {
  const lines = msgText.split(/\r?\n/).map(parseScoreLine).filter(Boolean);
  if (!lines.length) {
    await reply(env, chatId, "✍️ Pour mettre un résultat, écris une ligne par match :\nscore Roma Real 2-1 gagné\nscore Betis Barcelone 1-3 perdu\n\n(gagné, perdu ou remboursé à la fin ; le score est facultatif)");
    return;
  }
  const path = "site-src/matchs.txt";
  try {
    const cur = await gh(env, `contents/${path}?ref=main`);
    if (!cur.ok) throw new Error(`GitHub ${cur.status}`);
    const meta = await cur.json();
    const bin = atob(meta.content.replace(/\n/g, ""));
    const text = new TextDecoder().decode(Uint8Array.from(bin, (ch) => ch.charCodeAt(0)));
    const r = applyScores(text, lines);
    if (r.done.length) {
      const body = new TextEncoder().encode(r.text);
      const put = await gh(env, `contents/${path}`, {
        method: "PUT",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ message: "Resultats depuis Telegram", content: toBase64(body), branch: "main", sha: meta.sha,
          committer: { name: "cousinmarc-bot", email: "cousinmarc-bot@users.noreply.github.com" } }),
      });
      if (!put.ok) throw new Error(`GitHub ${put.status}: ${(await put.text()).slice(0, 150)}`);
    }
    let msg = r.done.length ? "✅ Résultats mis sur le site (visibles dans 2 à 3 minutes) :\n" + r.done.join("\n") : "";
    if (r.missing.length) msg += (msg ? "\n\n" : "") + "❓ Match introuvable (déjà joué ?) : " + r.missing.join(", ") + "\nÉcris les noms comme sur le site, ex : score Real Madrid Seville 2-0 gagné";
    await reply(env, chatId, msg);
  } catch (e) {
    console.log("score", e.message);
    await reply(env, chatId, "⚠️ Impossible de mettre le résultat sur le site (vérifie la clé GITHUB_TOKEN dans Cloudflare).");
  }
}

// ---------------------------------------------------------------- Resultats NBA automatiques (scores ESPN, sans intervention)
// Chaque matin a 6h et chaque soir a 21h (Douala) : pour chaque match NBA du site deja termine et sans resultat,
// le bot lit le score officiel sur ESPN, decide gagne / perdu d'apres le pronostic « X to win », et ecrit le resultat dans matchs.txt.
const AR_RES = { gagne: "التوقع ناجح ✅", perdu: "التوقع خاسر ❌" };

function etDateOf(douala) { // "2026-11-11 01:30" (heure de Douala, UTC+1) -> "20261110" (date du match aux Etats-Unis, heure de New York)
  const utc = Date.parse(douala.trim().replace(" ", "T") + ":00+01:00");
  return new Date(utc - 5 * 3600000).toISOString().slice(0, 10).replace(/-/g, "");
}

export function nbaPending(text, now = new Date()) {
  const out = [];
  text.split("\n---\n").forEach((b, i) => {
    if (!/^competition:\s*NBA\s*$/m.test(b) || /^resultat:/m.test(b)) return;
    const d = (b.match(/^date:\s*(.+)$/m) || [])[1];
    if (!d) return;
    const start = Date.parse(d.trim().replace(" ", "T") + ":00+01:00");
    // termine (au moins 3h apres le debut) et pas plus vieux que 5 jours
    if (start + 3 * 3600000 > now.getTime() || start < now.getTime() - 5 * 86400000) return;
    out.push({ i, et: etDateOf(d) });
  });
  return out;
}

export function nbaApply(block, game) {
  // game = { home, away, hs, as } (noms ESPN « displayName » et points)
  const get = (k) => ((block.match(new RegExp(`^${k}:\\s*(.+)$`, "m")) || [])[1] || "").trim();
  const e1 = get("equipe1"), e2 = get("equipe2"), p = get("pronostic"), pen = get("pronostic_en");
  const s1 = plain(e1) === plain(game.home) ? game.hs : game.as, s2 = plain(e1) === plain(game.home) ? game.as : game.hs;
  const winner = s1 > s2 ? e1 : e2;
  const pick = (pen.match(/^(.+?)\s+to win$/i) || [])[1];
  if (!pick || s1 === s2) return null; // pronostic non « vainqueur » : on laisse le resultat a la main
  const res = plain(winner).includes(plain(pick)) ? "gagne" : "perdu";
  const sc = `${s1}-${s2}`;
  const fr = `Score final : ${e1} ${sc} ${e2}. ` + (res === "gagne" ? `Pronostic gagné ✅ : ${p.charAt(0).toLowerCase() + p.slice(1)}.` : `Pronostic perdu ❌ : ${winner} a gagné.`);
  const en = `Final score: ${e1} ${sc} ${e2}. ` + (res === "gagne" ? `Prediction won ✅: ${pen}.` : `Prediction lost ❌: ${winner} won.`);
  const ar = `النتيجة النهائية: ${sc}. ${AR_RES[res]}`;
  const lines = block.split("\n");
  const k = lines.findIndex((l) => l.startsWith("bookmaker:"));
  lines.splice(k + 1, 0, `resultat: ${res}`);
  const starts = lines.map((l, j) => (/^(analyse_en|analyse_ar|analyse)\s*:/.test(l) ? j : -1)).filter((j) => j >= 0);
  let last = lines.length - 1;
  while (last > 0 && !lines[last].trim()) last--;
  const ins = starts.map((s, n) => {
    const end = n + 1 < starts.length ? starts[n + 1] - 1 : last;
    const key = lines[s].split(":")[0].trim();
    return [end, key === "analyse" ? fr : key === "analyse_en" ? en : ar];
  }).sort((a, b) => b[0] - a[0]);
  for (const [end, txt] of ins) lines.splice(end + 1, 0, txt);
  return { block: lines.join("\n"), line: `🏀 ${e1} ${sc} ${e2} : ${res === "gagne" ? "✅ gagné" : "❌ perdu"}` };
}

export async function nbaResults(env, now = new Date(), dryText = null) {
  const path = "site-src/matchs.txt";
  let text = dryText, sha = null;
  if (text === null) {
    const cur = await gh(env, `contents/${path}?ref=main`);
    if (!cur.ok) throw new Error(`GitHub ${cur.status}`);
    const meta = await cur.json();
    sha = meta.sha;
    const bin = atob(meta.content.replace(/\n/g, ""));
    text = new TextDecoder().decode(Uint8Array.from(bin, (ch) => ch.charCodeAt(0)));
  }
  const pending = nbaPending(text, now);
  if (!pending.length) return "NBA : aucun résultat à mettre";
  const games = {};
  for (const et of [...new Set(pending.map((x) => x.et))]) {
    const r = await fetch(`https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=${et}`);
    if (!r.ok) continue;
    for (const ev of (await r.json()).events || []) {
      if (!ev.status?.type?.completed) continue;
      const c = ev.competitions[0].competitors;
      const h = c.find((t) => t.homeAway === "home"), a = c.find((t) => t.homeAway === "away");
      games[`${et}|${plain(h.team.displayName)}|${plain(a.team.displayName)}`] = { home: h.team.displayName, away: a.team.displayName, hs: +h.score, as: +a.score };
    }
  }
  const blocks = text.split("\n---\n");
  const done = [];
  for (const { i, et } of pending) {
    const e1 = plain((blocks[i].match(/^equipe1:\s*(.+)$/m) || [])[1] || ""), e2 = plain((blocks[i].match(/^equipe2:\s*(.+)$/m) || [])[1] || "");
    const g = games[`${et}|${e1}|${e2}`] || games[`${et}|${e2}|${e1}`];
    if (!g) continue;
    const r = nbaApply(blocks[i], g);
    if (!r) continue;
    blocks[i] = r.block;
    done.push(r.line);
  }
  if (!done.length) return "NBA : scores pas encore disponibles";
  const out = blocks.join("\n---\n");
  if (dryText !== null) return { text: out, done };
  const put = await gh(env, `contents/${path}`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ message: "Resultats NBA automatiques (ESPN)", content: toBase64(new TextEncoder().encode(out)), branch: "main", sha,
      committer: { name: "cousinmarc-bot", email: "cousinmarc-bot@users.noreply.github.com" } }),
  });
  if (!put.ok) throw new Error(`GitHub ${put.status}: ${(await put.text()).slice(0, 150)}`);
  return "NBA : résultats mis sur le site\n" + done.join("\n");
}

// ---------------------------------------------------------------- Message recu
async function handleUpdate(update, env) {
  const msg = update.message;
  if (!msg || !msg.chat) return;
  const chatId = msg.chat.id;
  const userId = String((msg.from || {}).id || "");
  const allowed = (env.TELEGRAM_ALLOWED_ID || "").split(",").map((s) => s.trim()).filter(Boolean);
  if (!allowed.includes(userId)) {
    await reply(env, chatId, `⛔ Bot privé. Ton identifiant Telegram est : ${userId}`);
    return;
  }

  if (msg.text && msg.text.trim().startsWith("/")) { await handleCommand(env, chatId, userId, msg.text); return; }
  if (msg.text && /^\s*(score|scores)\b/i.test(msg.text)) { await handleScores(env, chatId, msg.text); return; }

  let fileId = null, asPhoto = true;
  if (msg.photo && msg.photo.length) fileId = msg.photo[msg.photo.length - 1].file_id;
  else if (msg.document && String(msg.document.mime_type || "").startsWith("image/")) { fileId = msg.document.file_id; asPhoto = false; }
  if (!fileId) { await reply(env, chatId, HELP); return; }

  const v = parseVip(msg.caption);
  if (v) {
    let st;
    try {
      const info = await tg(env, "getFile", { file_id: fileId });
      const img = await fetch(`https://api.telegram.org/file/bot${env.TELEGRAM_BOT_TOKEN}/${info.file_path}`);
      const bytes = await img.arrayBuffer();
      await addVipProof(env, bytes, v);
      st = `✅ Ticket ajouté à la galerie VIP du site (visible dans 5 minutes environ).\n${v.titre}${v.cote ? " · cote " + v.cote : ""}${v.gain ? " · " + v.gain : ""}\nIl sera aussi utilisé dans les rappels VIP de 13h.`;
      if (!v.cote) st += "\nℹ️ Astuce : ajoute la cote et le gain sur la 2e ligne, ex : Rennes – OFI · cote 11 · 3 850 000 F";
    } catch (e) {
      console.log("vip", e.message);
      st = "⚠️ Impossible d'ajouter le ticket au site (vérifie la clé GITHUB_TOKEN dans Cloudflare).";
    }
    if (v.toChannel) {
      try {
        await tg(env, asPhoto ? "sendPhoto" : "sendDocument", { chat_id: channelOf(env), caption: withEn(VIP_POST, EN.vip_post), [asPhoto ? "photo" : "document"]: fileId });
        st += `\n📢 Publié dans le canal ${channelOf(env)}.`;
      } catch (e) { st += "\n⚠️ Impossible de publier dans le canal."; }
    }
    await reply(env, chatId, st);
    return;
  }

  const c = parseCaption(msg.caption);
  if (!c.label) { await reply(env, chatId, "❓ Légende non reconnue.\n\n" + HELP); return; }
  const post = channelText(c.text, c.comment, c.file ? EN.targets[c.file] : null);
  let status;

  if (c.toSite && c.file) {
    try {
      // pour le site : version 1280 px de Telegram (3 fois plus legere, toujours lisible sur telephone)
      let siteId = fileId;
      if (msg.photo && msg.photo.length) {
        const okSizes = msg.photo.filter((s) => Math.max(s.width || 0, s.height || 0) <= 1280);
        if (okSizes.length) siteId = okSizes[okSizes.length - 1].file_id;
      }
      const info = await tg(env, "getFile", { file_id: siteId });
      const img = await fetch(`https://api.telegram.org/file/bot${env.TELEGRAM_BOT_TOKEN}/${info.file_path}`);
      const bytes = await img.arrayBuffer();
      await saveToGithub(env, c.file, bytes, c.label);
      status = `✅ Reçu ! ${c.label} (${c.file}, ${Math.round(bytes.byteLength / 1024)} Ko).\nSur le site dans quelques minutes.`;
    } catch (e) {
      console.log("site", e.message);
      status = "⚠️ Impossible de mettre le coupon sur le site (vérifie la clé GITHUB_TOKEN dans Cloudflare).";
    }
  } else {
    status = "✅ Reçu ! Publication dans le canal seulement (le site ne change pas).";
  }

  if (c.toChannel) {
    try {
      const key = asPhoto ? "photo" : "document";
      await tg(env, asPhoto ? "sendPhoto" : "sendDocument", { chat_id: channelOf(env), caption: post, [key]: fileId });
      status += `\n📢 Publié dans le canal ${channelOf(env)}.`;
    } catch (e) {
      console.log("canal", e.message);
      status += "\n⚠️ Impossible de publier dans le canal : vérifie que le bot est administrateur du canal.";
    }
  }
  await reply(env, chatId, status);
  await reply(env, chatId, "📋 Texte pour ta chaîne WhatsApp (appui long → Copier) :\n\n" + post);
}

// ---------------------------------------------------------------- Promo 6h / 21h
export function pickIndex(date) {
  const days = Math.floor((Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()) - Date.UTC(2026, 0, 1)) / 86400000);
  const slot = date.getUTCHours() < 12 ? 0 : 1;
  return (days * 2 + slot) % PROMOS.length;
}

// Image neuve du jour (fabriquee chaque mois par scripts/visuels.py) : promo/visuels/AAAA-MM/JJ-matin.jpg ou JJ-soir.jpg
const VISUELS = "https://raw.githubusercontent.com/fokamjeanmarc2004-cloud/marc-pronostic-api/main/promo/visuels";
function visuelDuJour(date) {
  const d = date.toISOString();
  return `${VISUELS}/${d.slice(0, 7)}/${d.slice(8, 10)}-${date.getUTCHours() < 12 ? "matin" : "soir"}.jpg`;
}

async function sendPromo(env, index, date = new Date()) {
  const p = PROMOS[index];
  const hour = new Date().toISOString().slice(0, 13).replace(/\D/g, "");
  const image = p.image === "COUPON_DU_JOUR" ? `${COUPON_DU_JOUR}?t=${hour}` : p.image;
  // le coupon du jour garde la vraie photo ; les autres messages prennent l'image neuve du jour si elle existe
  let fresh = null;
  if (p.image !== "COUPON_DU_JOUR" && index === pickIndex(date)) {
    const url = visuelDuJour(date);
    try { if ((await fetch(url, { method: "HEAD" })).ok) fresh = url; } catch (e) { console.log("visuel", e.message); }
  }
  let body = p.text;
  if (body.includes("__STICKERS__")) {
    let link = null;
    try { link = await stickerSetLink(env); } catch (e) { console.log("stickers", e.message); }
    body = link ? body.replace("__STICKERS__", link) : body.replace(/🔥 Stickers[^\n]*\n__STICKERS__\n\n/, "");
  }
  const text = withEn(body, EN.promos[index]);
  for (const img of [fresh, image]) {
    if (!img) continue;
    try {
      await tg(env, "sendPhoto", { chat_id: channelOf(env), photo: img, caption: text });
      return `message ${index + 1} publié (${img === fresh ? "image neuve du jour" : "image"})`;
    } catch (e) {
      console.log("image", e.message);
    }
  }
  await tg(env, "sendMessage", { chat_id: channelOf(env), text });
  return `message ${index + 1} publié (texte)`;
}

// ---------------------------------------------------------------- 13h (Cameroun) : VIP le dimanche seulement, un sujet par jour sinon
function weekOf(date) {
  return Math.floor((Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()) - Date.UTC(2026, 0, 1)) / 86400000 / 7);
}

async function sendMidi(env, date = new Date()) {
  const wd = date.getUTCDay();
  if (wd === 0) return sendVip(env, date);
  const m = wd === 4 ? MIDI_BK[weekOf(date) % MIDI_BK.length] : MIDI[wd];
  const text = withEn(m.text, wd === 4 ? EN.midibk[weekOf(date) % MIDI_BK.length] : EN.midi[wd]);
  const d = date.toISOString();
  const fresh = `${VISUELS}/${d.slice(0, 7)}/${d.slice(8, 10)}-midi.jpg`;
  let ok = false;
  try { ok = (await fetch(fresh, { method: "HEAD" })).ok; } catch (e) { console.log("visuel midi", e.message); }
  for (const img of [ok ? fresh : null, m.image]) {
    if (!img) continue;
    try {
      await tg(env, "sendPhoto", { chat_id: channelOf(env), photo: img, caption: text });
      return `message de 13h publié (${img === fresh ? "image neuve du jour" : "image"})`;
    } catch (e) { console.log("image midi", e.message); }
  }
  await tg(env, "sendMessage", { chat_id: channelOf(env), text });
  return "message de 13h publié (texte)";
}

async function sendVip(env, date = new Date()) {
  const vi = weekOf(date) % VIP_RAPPELS.length;
  const text = withEn(VIP_RAPPELS[vi], EN.vip[vi]);
  const d = date.toISOString();
  const fresh = `${VISUELS}/${d.slice(0, 7)}/${d.slice(8, 10)}-vip.jpg`;
  let ok = false;
  try { ok = (await fetch(fresh, { method: "HEAD" })).ok; } catch (e) { console.log("visuel vip", e.message); }
  for (const img of [ok ? fresh : null, VIP_IMAGE]) {
    if (!img) continue;
    try {
      await tg(env, "sendPhoto", { chat_id: channelOf(env), photo: img, caption: text });
      return `rappel VIP publié (${img === fresh ? "image neuve du jour" : "image VIP"})`;
    } catch (e) { console.log("image vip", e.message); }
  }
  await tg(env, "sendMessage", { chat_id: channelOf(env), text });
  return "rappel VIP publié (texte)";
}

// ---------------------------------------------------------------- 6h : mes pronostics du jour (liens vers les analyses du site)
// Treve internationale : jusqu'a cette date (heure de Douala), le canal ne recoit QUE les pronostics (minuit et 6h), pas de promo
const PAUSE_PROMO_JUSQUA = "2026-11-20";
function enPause(date) { return new Date(date.getTime() + 3600000).toISOString().slice(0, 10) < PAUSE_PROMO_JUSQUA; }

// moment = "nuit" (envoi de minuit : matchs avant 6h, NBA) ou "jour" (envoi de 6h : matchs a partir de 6h)
async function sendAnalyses(env, date = new Date(), moment = "jour") {
  const day = new Date(date.getTime() + 3600000).toISOString().slice(0, 10); // date du jour a Douala (UTC+1)
  let list = [];
  try { list = await (await fetch(`${SITE}/matchs.json?t=${Date.now()}`)).json(); } catch (e) { return "analyses : matchs.json illisible (" + e.message + ")"; }
  const nuit = moment === "nuit";
  const today = list.filter((m) => m.d === day && (nuit ? m.h < "06:00" : m.h >= "06:00")).slice(0, 10);
  if (!today.length) return `analyses (${moment}) : aucun match`;
  const pause = enPause(date);
  // bilingue : chaque match en francais puis en anglais
  const build = (withLinksEn) => {
    let s = nuit ? "🌙 MES PRONOSTICS DE LA NUIT\n🇬🇧 TONIGHT'S PREDICTIONS\n" : "⚽ MES PRONOSTICS DU JOUR\n🇬🇧 TODAY'S PREDICTIONS\n";
    for (const m of today) {
      s += `\n🕘 ${m.h} · ${m.e1} – ${m.e2}\n✅ ${m.p}\n`;
      if (m.p_en && m.p_en !== m.p) s += `🇬🇧 ${m.p_en}\n`;
      s += `👉 ${SITE}/${m.slug}.html\n`;
      if (withLinksEn && m.slug_en) s += `🇬🇧 ${SITE}/${m.slug_en}.html\n`;
    }
    if (pause) return s + "\n" + EN.resp;
    return s + "\n🎁 Pas encore de compte ? Inscris-toi avec le code promo FFN pour ton bonus.\n🇬🇧 No account yet? Register with promo code FFN for your bonus.\n\n" + EN.resp;
  };
  let text = build(true);
  if (text.length > 1000) { const short = build(false); if (short.length <= 1000) text = short; }
  const photo = `${SITE}/og/${today[0].slug}.jpg`;
  if (text.length <= 1000) {
    try {
      await tg(env, "sendPhoto", { chat_id: channelOf(env), photo, caption: text });
      return `analyses du jour publiées (${today.length} match(s), image)`;
    } catch (e) { console.log("image analyses", e.message); }
  }
  await tg(env, "sendMessage", { chat_id: channelOf(env), text, disable_web_page_preview: false });
  return `analyses du jour publiées (${today.length} match(s), texte)`;
}

// ---------------------------------------------------------------- Entrees du Worker
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const given = (url.searchParams.get("key") || "").trim();
    const keyOk = env.WEBHOOK_SECRET && given === env.WEBHOOK_SECRET.trim();
    const keyHelp = () => !env.WEBHOOK_SECRET
      ? "❌ Le secret WEBHOOK_SECRET est absent dans Cloudflare (Settings > Variables and Secrets)."
      : `❌ Clé incorrecte : tu as tapé ${given.length} caractères, le mot de passe enregistré en a ${env.WEBHOOK_SECRET.trim().length}. Attention aux majuscules/minuscules.`;

    // Messages envoyes par Telegram
    if (url.pathname === "/telegram" && request.method === "POST") {
      if (request.headers.get("X-Telegram-Bot-Api-Secret-Token") !== env.WEBHOOK_SECRET) {
        return new Response("interdit", { status: 403 });
      }
      const update = await request.json();
      ctx.waitUntil(handleUpdate(update, env).catch((e) => console.log("erreur", e.message)));
      return new Response("ok");
    }

    // A ouvrir UNE fois : branche Telegram sur ce Worker
    if (url.pathname === "/setup") {
      if (!keyOk) return new Response(keyHelp(), { status: 403, headers: { "content-type": "text/plain; charset=utf-8" } });
      const res = await tg(env, "setWebhook", {
        url: `${url.origin}/telegram`,
        secret_token: env.WEBHOOK_SECRET,
        allowed_updates: ["message"],
      });
      const me = await tg(env, "getMe", {});
      return new Response(`✅ Bot @${me.username} branché sur Cloudflare (${res}).`, { headers: { "content-type": "text/plain; charset=utf-8" } });
    }

    // Test d'un message promo : /promo?key=...&n=1
    if (url.pathname === "/promo") {
      if (!keyOk) return new Response(keyHelp(), { status: 403, headers: { "content-type": "text/plain; charset=utf-8" } });
      const n = parseInt(url.searchParams.get("n") || "", 10);
      const i = n >= 1 && n <= PROMOS.length ? n - 1 : pickIndex(new Date());
      const out = await sendPromo(env, i);
      return new Response(`✅ ${out} dans ${channelOf(env)}`, { headers: { "content-type": "text/plain; charset=utf-8" } });
    }

    if (url.pathname === "/midi") {
      if (!keyOk) return new Response(keyHelp(), { status: 403, headers: { "content-type": "text/plain; charset=utf-8" } });
      const out = await sendMidi(env);
      return new Response(`✅ ${out} dans ${channelOf(env)}`, { headers: { "content-type": "text/plain; charset=utf-8" } });
    }

    if (url.pathname === "/analyses") {
      if (!keyOk) return new Response(keyHelp(), { status: 403, headers: { "content-type": "text/plain; charset=utf-8" } });
      const out = await sendAnalyses(env);
      return new Response(`✅ ${out} dans ${channelOf(env)}`, { headers: { "content-type": "text/plain; charset=utf-8" } });
    }

    if (url.pathname === "/vip") {
      if (!keyOk) return new Response(keyHelp(), { status: 403, headers: { "content-type": "text/plain; charset=utf-8" } });
      const out = await sendVip(env);
      return new Response(`✅ ${out} dans ${channelOf(env)}`, { headers: { "content-type": "text/plain; charset=utf-8" } });
    }

    return new Response("Bot Cousin Marc : en ligne ✅", { headers: { "content-type": "text/plain; charset=utf-8" } });
  },

  // 5h00 et 20h00 UTC = 6h00 et 21h00 au Cameroun
  async scheduled(event, env, ctx) {
    const when = new Date(event.scheduledTime);
    // 23h00 UTC = minuit au Cameroun : pronostics de la nuit (NBA...)
    if (when.getUTCHours() === 23) { ctx.waitUntil(sendAnalyses(env, when, "nuit").then(console.log).catch((e) => console.log("nuit", e.message))); return; }
    const pause = enPause(when);
    // 6h et 21h : resultats NBA automatiques (scores ESPN)
    if (when.getUTCHours() === 5 || when.getUTCHours() === 20) ctx.waitUntil(nbaResults(env, when).then(console.log).catch((e) => console.log("nba", e.message)));
    // 12h00 UTC = 13h00 au Cameroun : VIP le dimanche, sujet du jour sinon ; sinon promo de 6h ou 21h
    if (pause) console.log("treve : pas de promo");
    else if (when.getUTCHours() === 12) ctx.waitUntil(sendMidi(env, when).then(console.log));
    else ctx.waitUntil(sendPromo(env, pickIndex(when), when).then(console.log));
    // 6h : reconstruit le site (pages « pronostic foot aujourd'hui / demain » a la bonne date)
    if (when.getUTCHours() === 5) ctx.waitUntil(saveToGithub(env, "site-src/jour.txt", new TextEncoder().encode(when.toISOString().slice(0, 10) + "\n"), "reconstruction du jour").catch((e) => console.log("jour", e.message)));
    // 6h : apres la promo, la liste des analyses du jour (seulement les jours de match)
    if (when.getUTCHours() === 5) ctx.waitUntil(new Promise((r) => setTimeout(r, pause ? 0 : 20000)).then(() => sendAnalyses(env, when, "jour")).then(console.log).catch((e) => console.log("analyses", e.message)));
  },
};
