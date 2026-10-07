# -*- coding: utf-8 -*-
"""
Bot Telegram -> coupons du site Cousin Marc (+ publication dans le canal Telegram).

Tu envoies une PHOTO a ton bot avec une legende. 1re ligne = le mot-cle :
    cote2        -> cote2.jpg         (page Cote de 2 + coupon du jour de l'accueil)
    tpi 1xbet    -> tpi-1xbet.jpg     (page Total Pair/Impair, coupon 1xBet)
    tpi melbet   -> tpi-melbet.jpg    (page Total Pair/Impair, coupon Melbet)
    resultat     -> result-photo.jpg  (page Resultats)
Les lignes suivantes de la legende (facultatives) sont ajoutees au message du canal.
Ajoute le mot  site  a la fin du mot-cle (ex : "cote2 site") pour NE PAS publier dans le canal.

Ce script est lance automatiquement par GitHub Actions (toutes les ~5 minutes).

Secrets GitHub (Settings > Secrets and variables > Actions) :
    TELEGRAM_BOT_TOKEN  : le jeton donne par @BotFather
    TELEGRAM_ALLOWED_ID : ton identifiant Telegram (seul toi peux publier)
    TELEGRAM_CHANNEL_ID : (facultatif) ton canal, ex : @marc_prono
                          -> le bot doit etre ADMINISTRATEUR du canal (droit "Publier")
"""
import json, os, re, sys, unicodedata, urllib.parse, urllib.request

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
ALLOWED = {x.strip() for x in os.environ.get("TELEGRAM_ALLOWED_ID", "").split(",") if x.strip()}
# Ton canal Telegram (public, pas un secret). Mets "" pour ne jamais publier dans un canal.
CHANNEL = os.environ.get("TELEGRAM_CHANNEL_ID", "").strip() or "@marc_prono"
API = f"https://api.telegram.org/bot{TOKEN}"
FILE_API = f"https://api.telegram.org/file/bot{TOKEN}"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFFSET_FILE = os.path.join(ROOT, ".telegram_offset")
SITE = "https://cousinmarc-pronostic.com"

# (mot-cle, fichier sur le site, nom affiche, texte pour le canal / WhatsApp)
TARGETS = [
    (r"^(cote|côte)\s*(de\s*)?2$|^c2$", "cote2.jpg", "Côte de 2 + coupon du jour de l'accueil",
     "🎯 COUPON CÔTE DE 2 DU JOUR\n\n"
     "✅ Pas encore de compte ? Inscris-toi avec le code promo FFN\n"
     f"🌐 {SITE}/cote-de-2.html"),
    (r"^tpi\s*1\s*x\s*bet$|^tpi\s*1xbet$|^pair\s*impair\s*1xbet$", "tpi-1xbet.jpg", "Total Pair/Impair · 1xBet",
     "🎲 TOTAL PAIR / IMPAIR · 1xBet\n\n"
     "✅ Code promo 1xBet : FFN\n"
     f"🌐 {SITE}/total-pair-impair.html"),
    (r"^tpi\s*melbet$|^pair\s*impair\s*melbet$", "tpi-melbet.jpg", "Total Pair/Impair · Melbet",
     "🎲 TOTAL PAIR / IMPAIR · Melbet\n\n"
     "✅ Code promo Melbet : FFN\n"
     f"🌐 {SITE}/total-pair-impair.html"),
    (r"^(resultat|résultat|resultats|résultats)$", "result-photo.jpg", "Résultats",
     "🏆 RÉSULTAT COUSIN MARC\n\n"
     "📊 Tous les résultats publiés :\n"
     f"🌐 {SITE}/resultats.html"),
]
FOOTER = "\n\n18+ · Joue de façon responsable"
HELP = ("📸 Envoie la photo du coupon avec une légende :\n"
        "• cote2 → Côte de 2 (+ accueil)\n"
        "• tpi 1xbet → Pair/Impair 1xBet\n"
        "• tpi melbet → Pair/Impair Melbet\n"
        "• resultat → page Résultats\n\n"
        "Tu peux écrire ton commentaire sur les lignes suivantes : il sera ajouté au message du canal.\n"
        "Ajoute « site » après le mot-clé (ex : cote2 site) pour publier seulement sur le site.\n\n"
        "Le site et le canal sont mis à jour en 5 à 15 minutes.")


def call(method, **params):
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(f"{API}/{method}", data=data, timeout=30) as r:
        out = json.load(r)
    if not out.get("ok"):
        raise RuntimeError(f"{method}: {out}")
    return out["result"]


def reply(chat_id, text):
    try:
        call("sendMessage", chat_id=chat_id, text=text, disable_web_page_preview="true")
    except Exception as e:  # une reponse ratee ne doit pas bloquer la publication
        print("reponse impossible :", e)


def norm(text):
    t = unicodedata.normalize("NFKC", text or "").strip().lower()
    return re.sub(r"\s+", " ", t)


def parse_caption(caption):
    """Renvoie (fichier, nom, texte canal, commentaire, publier_dans_canal)."""
    lines = (caption or "").strip().splitlines()
    first = norm(lines[0]) if lines else ""
    comment = "\n".join(lines[1:]).strip()
    to_channel = True
    if first.endswith(" site"):
        first, to_channel = first[:-5].strip(), False
    for pattern, filename, label, text in TARGETS:
        if re.match(pattern, first):
            return filename, label, text, comment, to_channel
    return None, None, None, comment, to_channel


def target_for(caption):  # garde pour compatibilite
    f, label, *_ = parse_caption(caption)
    return f, label


def download(file_id, dest):
    info = call("getFile", file_id=file_id)
    with urllib.request.urlopen(f"{FILE_API}/{info['file_path']}", timeout=60) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)


def channel_text(text, comment):
    return (f"{comment}\n\n{text}" if comment else text) + FOOTER


def main():
    if not TOKEN or not ALLOWED:
        sys.exit("Secrets TELEGRAM_BOT_TOKEN et TELEGRAM_ALLOWED_ID manquants.")
    offset = 0
    if os.path.exists(OFFSET_FILE):
        offset = int(open(OFFSET_FILE).read().strip() or 0)
    updates = call("getUpdates", offset=offset, timeout=0, allowed_updates=json.dumps(["message"]))
    changed = []
    for u in updates:
        offset = max(offset, u["update_id"] + 1)
        msg = u.get("message") or {}
        chat_id = msg.get("chat", {}).get("id")
        user_id = str(msg.get("from", {}).get("id", ""))
        if not chat_id:
            continue
        if user_id not in ALLOWED:
            reply(chat_id, f"⛔ Bot privé. Ton identifiant Telegram est : {user_id}")
            continue
        photo = msg.get("photo")
        doc = msg.get("document")
        file_id, as_photo = None, True
        if photo:
            file_id = photo[-1]["file_id"]           # la plus grande taille
        elif doc and str(doc.get("mime_type", "")).startswith("image/"):
            file_id, as_photo = doc["file_id"], False
        if not file_id:
            reply(chat_id, HELP)
            continue
        filename, label, text, comment, to_channel = parse_caption(msg.get("caption"))
        if not filename:
            reply(chat_id, "❓ Légende non reconnue.\n\n" + HELP)
            continue
        size = download(file_id, os.path.join(ROOT, filename))
        changed.append(filename)
        post = channel_text(text, comment)
        status = f"✅ Reçu ! {label} ({filename}, {size // 1024} Ko).\nSur le site dans quelques minutes."
        if CHANNEL and to_channel:
            try:
                method = "sendPhoto" if as_photo else "sendDocument"
                key = "photo" if as_photo else "document"
                call(method, chat_id=CHANNEL, caption=post, **{key: file_id})
                status += f"\n📢 Publié dans le canal {CHANNEL}."
            except Exception as e:
                print("canal :", e)
                status += ("\n⚠️ Impossible de publier dans le canal : vérifie que le bot est "
                           "administrateur du canal avec le droit de publier.")
        reply(chat_id, status)
        reply(chat_id, "📋 Texte pour ta chaîne WhatsApp (appui long → Copier) :\n\n" + post)
    with open(OFFSET_FILE, "w") as f:
        f.write(str(offset))
    print("fichiers mis a jour :", ", ".join(changed) or "aucun")


if __name__ == "__main__":
    main()
