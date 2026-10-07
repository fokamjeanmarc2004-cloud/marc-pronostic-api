# -*- coding: utf-8 -*-
"""
Message promo automatique dans le canal Telegram (2 fois par jour : 6h et 21h, heure du Cameroun).

Les messages tournent : un different a chaque publication (cycle de 13 messages, environ 6 jours et demi).
Pour modifier un texte : change-le dans la liste MESSAGES ci-dessous (garde les guillemets).
Chaque message = (image affichee au-dessus, texte). Image "" = message sans image.

Secrets GitHub utilises : TELEGRAM_BOT_TOKEN (deja en place).
Le bot doit etre administrateur du canal.
"""
import datetime, json, os, sys, urllib.parse, urllib.request

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHANNEL = os.environ.get("TELEGRAM_CHANNEL_ID", "").strip() or "@marc_prono"
SITE = "https://cousinmarc-pronostic.com"
RESP = "\n\n🔞 18+ · Joue de façon responsable."
# Coupon du jour envoye au bot (cote2) : le ?t= force Telegram a prendre la derniere version
COUPON_DU_JOUR = ("https://raw.githubusercontent.com/fokamjeanmarc2004-cloud/marc-pronostic-api/main/cote2.jpg"
                  f"?t={datetime.datetime.utcnow():%Y%m%d%H}")

# Visuels promo (dossier "promo" du depot marc-pronostic-api)
IMG = "https://raw.githubusercontent.com/fokamjeanmarc2004-cloud/marc-pronostic-api/main/promo"

SEP = "━━━━━━━━━━━━━━━━━━━━━━━━━━"
TUTO = "https://youtu.be/Z-vnaLR3jYM"


def entete(titre):
    return f"{SEP}\n{titre}\n{SEP}\n\n"


def bloc(nom, code, site, appli="", bonus=""):
    """Un bookmaker, au format Cousin Marc : 🌐 = site, 📲 = application."""
    t = f"🎯 {nom} — Code promo : {code}\n"
    if bonus:
        t += f"🎁 {bonus}\n"
    t += f"\n🌐 {site}\n"
    if appli:
        t += f"📲 {appli}\n"
    return t


def pied(code="FFN"):
    return (f"\n{SEP}\n"
            f"🎁 CODE PROMO OBLIGATOIRE À L'INSCRIPTION :\n"
            f"🔥 {code} 🔥\n"
            f"{SEP}\n"
            f"📺 Tuto création de compte :\n\n{TUTO}\n\n"
            f"{SEP}\n"
            f"🌐 = site · 📲 = application")


B_1XBET = bloc("1XBET", "FFN", "https://tinyurl.com/3vptk7a4", "https://tinyurl.com/7vucc2fu")
B_PARIPESA = bloc("PARIPESA", "FFN", "https://paripesa.bet/flex4", "https://paripesa.bet/cousinmarc")
B_MELBET = bloc("MELBET", "FFN", "https://tinyurl.com/48f3ukrb", "https://tinyurl.com/4nsmfukc")
B_WINWIN = bloc("WINWIN", "FFN", "https://slim.link/FFN", "https://slim.link/FFN_APK")

MESSAGES = [
 # 1 - ton message habituel (les 4 bookmakers)
 (f"{IMG}/promo-inscris-toi.jpg",
  entete("🔔 INSCRIS-TOI MAINTENANT")
  + B_1XBET + "\n\n" + B_PARIPESA + "\n\n" + B_MELBET + "\n" + B_WINWIN + pied()),

 # 2 - preuve VIP
 (f"{IMG}/promo-vip.jpg",
  entete("⭐ REJOINS LE VIP COUSIN MARC")
  + "🎯 Côte de 2 VIP tous les jours\n"
  "🚀 Grosses cotes plusieurs fois par semaine\n"
  "⚡ Pronostics en live pendant les matchs\n"
  "💬 Canal privé + questions directes\n\n"
  "💳 1 mois 30 $ · 3 mois 75 $ · 1 an 250 $\n"
  "📲 Paiement Orange Money, MTN ou crypto\n\n"
  f"👉 {SITE}/vip.html\n"
  f"{SEP}\n"
  "Aucun gain n'est garanti."),

 # 3 - 1xBet
 (f"{SITE}/affiche-1xbet.jpg",
  entete("🔥 PAS ENCORE DE COMPTE 1XBET ?")
  + bloc("1XBET", "FFN", "https://tinyurl.com/3vptk7a4", "https://tinyurl.com/7vucc2fu",
         "100% sur ton 1er dépôt (jusqu'à 100 000 FCFA au Cameroun)")
  + "📲 Dépôt et retrait par Mobile Money\n" + pied()),

 # 4 - comparateur
 (f"{IMG}/promo-quel-bookmaker.jpg",
  entete("🤔 QUEL BOOKMAKER CHOISIR ?")
  + "Donne ton pays et ton moyen de paiement\n"
  "(Orange Money, MTN, Wave, crypto…)\n"
  "et je te donne ton TOP 3 avec le bon code promo 👇\n\n"
  f"🧭 {SITE}/quel-bookmaker-choisir.html\n"
  f"{SEP}"),

 # 5 - Melbet
 (f"{SITE}/affiche-melbet.jpg",
  entete("🟡 MELBET : TON BONUS T'ATTEND")
  + bloc("MELBET", "FFN", "https://tinyurl.com/48f3ukrb", "https://tinyurl.com/4nsmfukc",
         "100% sur ton 1er dépôt") + pied()),

 # 6 - coupon cote de 2
 (COUPON_DU_JOUR,
  entete("⚽ COUPON CÔTE DE 2 DU JOUR")
  + "Un coupon court pour viser une cote autour de 2.\n"
  "Gratuit, sur le site et ici sur le canal 👇\n\n"
  f"👉 {SITE}/cote-de-2.html\n\n"
  "Pas encore de compte ?\n\n" + B_1XBET + pied()),

 # 7 - 1win (code ESS22)
 (f"{SITE}/affiche-1win.jpg",
  entete("🚀 1WIN : JUSQU'À 500% DE BONUS")
  + bloc("1WIN", "ESS22", "https://1win.com/", "",
         "jusqu'à 500% sur tes 4 premiers dépôts")
  + "\n⚠️ Pour 1win, le code est ESS22 (pas FFN)\n" + pied("ESS22")),

 # 8 - aide code
 (f"{IMG}/promo-code-aide.jpg",
  entete("❓ TON CODE PROMO NE MARCHE PAS ?")
  + "Code refusé, oublié à l'inscription,\n"
  "bonus pas reçu, retrait bloqué…\n"
  "Toutes les solutions sont ici 👇\n\n"
  f"🛠️ {SITE}/code-promo-ne-marche-pas.html\n\n"
  "Toujours bloqué ? Écris-moi en privé avec une capture.\n"
  f"{SEP}"),

 # 9 - Paripesa
 (f"{SITE}/affiche-paripesa.jpg",
  entete("🟠 PARIPESA : MÊME CODE, MÊME BONUS")
  + bloc("PARIPESA", "FFN", "https://paripesa.bet/flex4", "https://paripesa.bet/cousinmarc",
         "100% sur ton 1er dépôt") + pied()),

 # 10 - preuve VIP 2
 (f"{IMG}/promo-vip.jpg",
  entete("🚀 LES GROSSES COTES, C'EST DANS LE VIP")
  + "Les cotes à 5, 8, 10 et plus que vous aimez 🔥\n"
  "sont partagées en priorité dans le canal VIP,\n"
  "avec la côte de 2 du jour et le live.\n\n"
  f"🏆 Mes derniers tickets gagnants : {SITE}/vip.html#preuves\n\n"
  "💳 Dès 30 $/mois · Orange Money, MTN ou crypto\n"
  f"👉 {SITE}/vip.html\n"
  f"{SEP}\n"
  "Aucun gain n'est garanti."),

 # 11 - WinWin
 (f"{SITE}/affiche-winwin.jpg",
  entete("🟢 WINWIN : INSCRIS-TOI AVEC FFN")
  + "🎯 WINWIN — Code promo : FFN\n"
  "🎁 100% sur ton 1er dépôt\n\n"
  "🌐 https://slim.link/FFN\n"
  "📲 Android : https://slim.link/FFN_APK\n"
  "🍏 iPhone : https://apps.apple.com/sc/app/win-win-sports-betting/id6747608407\n"
  + pied()),

 # 12 - Megapari + GoldPari
 (f"{SITE}/affiche-goldpari.jpg",
  entete("💎 2 AUTRES BOOKMAKERS AVEC FFN")
  + bloc("MEGAPARI", "FFN", "https://4646532.megapari-359310.net", "", "100% sur ton 1er dépôt")
  + "\n\n"
  + bloc("GOLDPARI", "FFN", "https://slim.link/yHtzWdS", "https://slim.link/5gRZnVB", "300% jusqu'à 200 $")
  + pied()),

 # 13 - tous les codes
 (f"{IMG}/promo-tous-les-codes.jpg",
  entete("🎟️ TOUS MES CODES PROMO")
  + "🔥 FFN → 1xBet · Melbet · Paripesa · WinWin · Megapari · GoldPari\n"
  "🔥 ESS22 → 1win · Linebet\n"
  "🔥 FJM → BetAndYou · Fastparie\n"
  "🔥 CMF → Betwiner\n\n"
  f"👉 Tous les liens (site + application) :\n{SITE}\n\n"
  "⚠️ Le code s'entre UNE seule fois, à l'inscription.\n"
  f"{SEP}\n"
  f"📺 Tuto création de compte :\n\n{TUTO}\n"
  f"{SEP}"),
]


def call(method, **params):
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/{method}", data=data, timeout=30) as r:
        out = json.load(r)
    if not out.get("ok"):
        raise RuntimeError(f"{method}: {out}")
    return out["result"]


def pick(now_utc):
    """Un message different a chaque publication : 2 par jour (matin / soir)."""
    days = (now_utc.date() - datetime.date(2026, 1, 1)).days
    slot = 0 if now_utc.hour < 12 else 1
    return (days * 2 + slot) % len(MESSAGES)


def main():
    if not TOKEN:
        sys.exit("Secret TELEGRAM_BOT_TOKEN manquant.")
    forced = os.environ.get("PROMO_INDEX", "").strip()
    i = int(forced) - 1 if forced.isdigit() and 1 <= int(forced) <= len(MESSAGES) else pick(datetime.datetime.utcnow())
    image, text = MESSAGES[i]
    text += RESP
    if image:
        try:
            call("sendPhoto", chat_id=CHANNEL, photo=image, caption=text)
        except Exception as e:  # image indisponible : on envoie quand meme le texte
            print("image impossible :", e)
            call("sendMessage", chat_id=CHANNEL, text=text, disable_web_page_preview="true")
    else:
        call("sendMessage", chat_id=CHANNEL, text=text)
    print(f"message {i + 1}/{len(MESSAGES)} publie dans {CHANNEL}")


if __name__ == "__main__":
    main()
