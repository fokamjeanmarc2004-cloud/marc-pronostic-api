# -*- coding: utf-8 -*-
"""
Bot Telegram -> coupons du site Cousin Marc.

Tu envoies une PHOTO a ton bot avec une legende :
    cote2        -> cote2.jpg         (page Cote de 2 + coupon du jour de l'accueil)
    tpi 1xbet    -> tpi-1xbet.jpg     (page Total Pair/Impair, coupon 1xBet)
    tpi melbet   -> tpi-melbet.jpg    (page Total Pair/Impair, coupon Melbet)
    resultat     -> result-photo.jpg  (page Resultats)

Ce script est lance automatiquement par GitHub Actions (toutes les ~5 minutes).
Il lit les nouveaux messages, enregistre les photos sous le bon nom dans le depot,
puis GitHub Actions les publie (commit). Le bot te repond pour confirmer.

Secrets GitHub necessaires (Settings > Secrets and variables > Actions) :
    TELEGRAM_BOT_TOKEN  : le jeton donne par @BotFather
    TELEGRAM_ALLOWED_ID : ton identifiant Telegram (seul toi peux publier)
"""
import json, os, re, sys, unicodedata, urllib.parse, urllib.request

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
ALLOWED = {x.strip() for x in os.environ.get("TELEGRAM_ALLOWED_ID", "").split(",") if x.strip()}
API = f"https://api.telegram.org/bot{TOKEN}"
FILE_API = f"https://api.telegram.org/file/bot{TOKEN}"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFFSET_FILE = os.path.join(ROOT, ".telegram_offset")

# mot-cle de la legende -> nom du fichier sur le site
TARGETS = [
    (r"^(cote|côte)\s*(de\s*)?2$|^c2$", "cote2.jpg", "Côte de 2 + coupon du jour de l'accueil"),
    (r"^tpi\s*1\s*x\s*bet$|^tpi\s*1xbet$|^pair\s*impair\s*1xbet$", "tpi-1xbet.jpg", "Total Pair/Impair · 1xBet"),
    (r"^tpi\s*melbet$|^pair\s*impair\s*melbet$", "tpi-melbet.jpg", "Total Pair/Impair · Melbet"),
    (r"^(resultat|résultat|resultats|résultats)$", "result-photo.jpg", "Résultats"),
]
HELP = ("📸 Envoie la photo du coupon avec une légende :\n"
        "• cote2 → Côte de 2 (+ accueil)\n"
        "• tpi 1xbet → Pair/Impair 1xBet\n"
        "• tpi melbet → Pair/Impair Melbet\n"
        "• resultat → page Résultats\n\n"
        "Le site est mis à jour en 5 à 15 minutes.")


def call(method, **params):
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(f"{API}/{method}", data=data, timeout=30) as r:
        out = json.load(r)
    if not out.get("ok"):
        raise RuntimeError(f"{method}: {out}")
    return out["result"]


def reply(chat_id, text):
    try:
        call("sendMessage", chat_id=chat_id, text=text)
    except Exception as e:  # une reponse ratee ne doit pas bloquer la publication
        print("reponse impossible :", e)


def norm(caption):
    t = unicodedata.normalize("NFKC", caption or "").strip().lower()
    return re.sub(r"\s+", " ", t)


def target_for(caption):
    c = norm(caption)
    for pattern, filename, label in TARGETS:
        if re.match(pattern, c):
            return filename, label
    return None, None


def download(file_id, dest):
    info = call("getFile", file_id=file_id)
    with urllib.request.urlopen(f"{FILE_API}/{info['file_path']}", timeout=60) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)


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
        file_id = None
        if photo:
            file_id = photo[-1]["file_id"]           # la plus grande taille
        elif doc and str(doc.get("mime_type", "")).startswith("image/"):
            file_id = doc["file_id"]
        if not file_id:
            reply(chat_id, HELP)
            continue
        filename, label = target_for(msg.get("caption"))
        if not filename:
            reply(chat_id, "❓ Légende non reconnue.\n\n" + HELP)
            continue
        size = download(file_id, os.path.join(ROOT, filename))
        changed.append(filename)
        reply(chat_id, f"✅ Reçu ! {label} ({filename}, {size // 1024} Ko).\n"
                       f"Visible sur cousinmarc-pronostic.com dans quelques minutes.")
    with open(OFFSET_FILE, "w") as f:
        f.write(str(offset))
    print("fichiers mis a jour :", ", ".join(changed) or "aucun")


if __name__ == "__main__":
    main()
