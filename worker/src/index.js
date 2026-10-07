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
import { RESP, FOOTER, HELP as HELP_TXT, COUPON_DU_JOUR, TARGETS, PROMOS } from "./messages.js";

const REPO = "fokamjeanmarc2004-cloud/marc-pronostic-api";
const HELP = HELP_TXT.replace("mis à jour en 5 à 15 minutes", "mis à jour en quelques secondes");

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

export function channelText(text, comment) {
  const body = [comment, text].filter(Boolean).join("\n\n");
  return (body || "⚽ Cousin Marc") + FOOTER;
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

  let fileId = null, asPhoto = true;
  if (msg.photo && msg.photo.length) fileId = msg.photo[msg.photo.length - 1].file_id;
  else if (msg.document && String(msg.document.mime_type || "").startsWith("image/")) { fileId = msg.document.file_id; asPhoto = false; }
  if (!fileId) { await reply(env, chatId, HELP); return; }

  const c = parseCaption(msg.caption);
  if (!c.label) { await reply(env, chatId, "❓ Légende non reconnue.\n\n" + HELP); return; }
  const post = channelText(c.text, c.comment);
  let status;

  if (c.toSite && c.file) {
    try {
      const info = await tg(env, "getFile", { file_id: fileId });
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

async function sendPromo(env, index) {
  const p = PROMOS[index];
  const hour = new Date().toISOString().slice(0, 13).replace(/\D/g, "");
  const image = p.image === "COUPON_DU_JOUR" ? `${COUPON_DU_JOUR}?t=${hour}` : p.image;
  const text = p.text + RESP;
  if (image) {
    try {
      await tg(env, "sendPhoto", { chat_id: channelOf(env), photo: image, caption: text });
      return `message ${index + 1} publié (avec image)`;
    } catch (e) {
      console.log("image", e.message);
    }
  }
  await tg(env, "sendMessage", { chat_id: channelOf(env), text });
  return `message ${index + 1} publié (texte)`;
}

// ---------------------------------------------------------------- Entrees du Worker
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const keyOk = env.WEBHOOK_SECRET && url.searchParams.get("key") === env.WEBHOOK_SECRET;

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
      if (!keyOk) return new Response("cle incorrecte", { status: 403 });
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
      if (!keyOk) return new Response("cle incorrecte", { status: 403 });
      const n = parseInt(url.searchParams.get("n") || "", 10);
      const i = n >= 1 && n <= PROMOS.length ? n - 1 : pickIndex(new Date());
      const out = await sendPromo(env, i);
      return new Response(`✅ ${out} dans ${channelOf(env)}`, { headers: { "content-type": "text/plain; charset=utf-8" } });
    }

    return new Response("Bot Cousin Marc : en ligne ✅", { headers: { "content-type": "text/plain; charset=utf-8" } });
  },

  // 5h00 et 20h00 UTC = 6h00 et 21h00 au Cameroun
  async scheduled(event, env, ctx) {
    ctx.waitUntil(sendPromo(env, pickIndex(new Date(event.scheduledTime))).then(console.log));
  },
};
