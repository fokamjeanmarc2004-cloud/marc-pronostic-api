# -*- coding: utf-8 -*-
import os, re, html, json, shutil, datetime, unicodedata
_MOIS_FR = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
_MOIS_EN = ["January","February","March","April","May","June","July","August","September","October","November","December"]
_MOIS_ES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
_MOIS_AR = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
_NOW = datetime.date.today()
MAJ_FR = f"{_MOIS_FR[_NOW.month-1]} {_NOW.year}"
MAJ_EN = f"{_MOIS_EN[_NOW.month-1]} {_NOW.year}"
MAJ_ES = f"{_MOIS_ES[_NOW.month-1]} de {_NOW.year}"
MAJ_AR = f"{_MOIS_AR[_NOW.month-1]} {_NOW.year}"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")  # dossier "site" a cote du script (Windows/Mac/Linux)
os.makedirs(OUT, exist_ok=True)
BASE = "https://cousinmarc-pronostic.com"

# --- Données bookmakers : site + app + codes ---
BOOKMAKERS = [
    {
        "slug": "code-promo-1xbet", "name": "1xBet", "code": "FFN", "reg_code": None,
        "site": "https://tinyurl.com/3vptk7a4",
        "apps": [("Application", "https://tinyurl.com/7vucc2fu")],
        "bonus_max": "100% jusqu'à 130€",
        "countries": [
            ("Sénégal", "jusqu'à 260 000 XOF"), ("Burkina Faso", "jusqu'à 78 000 XOF"),
            ("Cameroun", "jusqu'à 100 000 XAF"), ("Congo (RDC)", "jusqu'à 221 000 CDF"),
            ("Maroc", "jusqu'à 970 MAD"), ("Zone euro", "jusqu'à 130 €"),
        ],
    },
    {
        "slug": "code-promo-melbet", "name": "Melbet", "code": "FFN", "reg_code": None,
        "site": "https://tinyurl.com/48f3ukrb",
        "apps": [("Application", "https://tinyurl.com/4nsmfukc")],
        "bonus_max": "100% sur 1er dépôt",
        "countries": [
            ("Sénégal", "jusqu'à 130 000 XOF"), ("Cameroun", "jusqu'à 100 000 XAF"),
            ("Côte d'Ivoire", "jusqu'à 130 000 XOF"), ("Maroc", "jusqu'à 1 000 MAD"),
            ("Zone euro", "jusqu'à 100 €"),
        ],
    },
    {
        "slug": "code-promo-paripesa", "name": "Paripesa", "code": "FFN", "reg_code": None,
        "site": "https://paripesa.bet/flex4",
        "apps": [("Application", "https://paripesa.bet/cousinmarc")],
        "bonus_max": "100% sur 1er dépôt",
        "countries": [
            ("Sénégal", "jusqu'à 100 000 XOF"), ("Cameroun", "jusqu'à 100 000 XAF"),
            ("Congo (RDC)", "jusqu'à 150 000 CDF"), ("Zone euro", "jusqu'à 100 €"),
        ],
    },
    {
        "slug": "code-promo-megapari", "name": "Megapari", "code": "FFN", "reg_code": None,
        "site": "https://4646532.megapari-359310.net",
        "apps": [],
        "bonus_max": "100% jusqu'à 130€",
        "countries": [
            ("Cameroun", "jusqu'à 100 000 XAF"), ("Sénégal", "jusqu'à 130 000 XOF"),
            ("Zone euro", "jusqu'à 130 €"),
        ],
    },
    {
        "slug": "code-promo-winwin", "name": "WinWin", "code": "FFN", "reg_code": None,
        "site": "https://slim.link/FFN",
        "apps": [("Android", "https://slim.link/FFN_APK"), ("iPhone", "https://apps.apple.com/sc/app/win-win-sports-betting/id6747608407")],
        "bonus_max": "100% sur 1er dépôt",
        "countries": [("Cameroun", "jusqu'à 100 000 XAF"), ("Afrique", "selon devise locale")],
    },
    {
        "slug": "code-promo-betandyou", "name": "BetAndYou", "code": "FJM", "reg_code": None,
        "site": "https://betandyouafrica.com",
        "apps": [],
        "bonus_max": "100% sur 1er dépôt",
        "countries": [("Afrique", "selon devise locale"), ("Zone euro", "jusqu'à 100 €")],
    },
    {
        "slug": "code-promo-betwiner", "name": "Betwiner", "code": "CMF", "reg_code": None,
        "site": "https://betwinner2.com/fr",
        "apps": [],
        "bonus_max": "100% sur 1er dépôt",
        "countries": [("Afrique", "selon devise locale"), ("Zone euro", "jusqu'à 100 €")],
    },
    {
        "slug": "code-promo-linebet", "name": "Linebet", "code": "ESS22", "reg_code": None,
        "site": "https://linebet.press/ess22",
        "apps": [],
        "bonus_max": "100% sur 1er dépôt",
        "countries": [
            ("Cameroun", "jusqu'à 100 000 XAF"), ("Sénégal", "jusqu'à 130 000 XOF"),
            ("Nigeria", "selon devise locale"), ("Zone euro", "jusqu'à 100 €"),
        ],
    },
    {
        "slug": "code-promo-1xbit", "name": "1xBit", "code": "FFN", "reg_code": None,
        "site": "https://refpa04636.pro/L?tag=b_5738120m_3429c_&site=5738120&ad=3429",
        "apps": [],
        "bonus_max": "Bonus de bienvenue en crypto (jusqu'à 7 BTC)",
        "countries": [
            ("Bitcoin (BTC)", "dépôts & retraits"), ("USDT / Ethereum", "acceptés"),
            ("Inscription", "rapide, sans KYC"), ("International", "paris en crypto"),
        ],
    },
    {
        "slug": "code-promo-fastparie", "name": "Fastparie", "code": "FJM", "reg_code": None,
        "site": "https://refpa15124.com/L?tag=d_4221683m_77525c_&site=4221683&ad=77525",
        "apps": [],
        "bonus_max": "100% sur 1er dépôt",
        "countries": [
            ("Sénégal", "bonus de bienvenue"), ("Cameroun", "bonus de bienvenue"),
            ("Côte d'Ivoire", "bonus de bienvenue"), ("Zone euro", "bonus de bienvenue"),
        ],
    },
    {
        "slug": "code-promo-afroparie", "name": "Afroparie", "code": "FFN", "reg_code": None,
        "site": "https://refpa84423.com/L?tag=d_3630898m_73229c_&site=3630898&ad=73229",
        "apps": [],
        "bonus_max": "100% sur 1er dépôt",
        "countries": [
            ("Sénégal", "bonus de bienvenue"), ("Cameroun", "bonus de bienvenue"),
            ("Côte d'Ivoire", "bonus de bienvenue"), ("Zone euro", "bonus de bienvenue"),
        ],
    },
    {
        "slug": "code-promo-1win", "name": "1win", "code": "ESS22", "reg_code": None,
        "site": "https://1win.com/",
        "apps": [],
        "bonus_max": "500% sur les 4 premiers dépôts",
        "countries": [
            ("Afrique francophone", "jusqu'à 500%"), ("Maghreb", "jusqu'à 500%"),
            ("Zone euro", "jusqu'à 500%"), ("International", "jusqu'à 500%"),
        ],
    },
    {
        "slug": "code-promo-goldpari", "name": "GoldPari", "code": "FFN", "reg_code": None,
        "site": "https://slim.link/yHtzWdS",
        "apps": [("Application", "https://slim.link/5gRZnVB")],
        "bonus_max": "300% jusqu'à 200$",
        "countries": [],
    },
]

SOCIAL = [
    ("Telegram", "https://t.me/marc_prono"),
    ("WhatsApp", "https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h"),
    ("YouTube", "https://youtube.com/@prossport"),
    ("Facebook", "https://www.facebook.com/1041369209050714"),
    ("Instagram", "https://instagram.com/mr.f.fn"),
    ("Snapchat", "https://www.snapchat.com/add/cousinmarc"),
]

BRAND = {
    "code-promo-1xbet": "#3b8ef0",
    "code-promo-melbet": "#ffd23f",
    "code-promo-paripesa": "#ff7a2f",
    "code-promo-megapari": "#e23b4e",
    "code-promo-winwin": "#1fc7a0",
    "code-promo-betandyou": "#6c7bff",
    "code-promo-betwiner": "#2fc46b",
    "code-promo-linebet": "#ff4757",
    "code-promo-1xbit": "#0fb9c4",
    "code-promo-fastparie": "#c026d3",
    "code-promo-afroparie": "#16a34a",
    "code-promo-1win": "#2563eb",
    "code-promo-goldpari": "#b8860b",
}

# Contenu unique par bookmaker (SEO anti-duplication) : bonus réel + intro par langue
BK_CONTENT = {
 "code-promo-1xbet": {
  "bonus": {"fr":"100% sur le 1er dépôt","en":"100% on 1st deposit","es":"100% en el 1er depósito","ar":"100% على أول إيداع"},
  "intro": {
   "fr":"1xBet est l'un des plus grands bookmakers au monde : des milliers d'événements chaque jour, des cotes parmi les plus élevées et des dépôts Mobile Money très pratiques en Afrique.",
   "en":"1xBet is one of the biggest bookmakers in the world, with thousands of daily events, some of the highest odds and convenient Mobile Money deposits across Africa.",
   "es":"1xBet es una de las casas de apuestas más grandes del mundo, con miles de eventos diarios, cuotas de las más altas y depósitos Mobile Money muy prácticos en África.",
   "ar":"1xBet من أكبر شركات المراهنات في العالم، مع آلاف الأحداث يوميًا ونسب من الأعلى وإيداعات Mobile Money عملية في إفريقيا."}},
 "code-promo-melbet": {
  "bonus": {"fr":"100% sur le 1er dépôt","en":"100% on 1st deposit","es":"100% en el 1er depósito","ar":"100% على أول إيداع"},
  "intro": {
   "fr":"Melbet se distingue par la richesse de ses marchés football et ses cotes compétitives, avec une application mobile fluide et des retraits rapides en devise locale.",
   "en":"Melbet stands out for its rich football markets and competitive odds, with a smooth mobile app and fast withdrawals in local currency.",
   "es":"Melbet destaca por su amplia oferta de mercados de fútbol y cuotas competitivas, con una app móvil fluida y retiros rápidos en moneda local.",
   "ar":"يتميّز Melbet بأسواق كرة قدم غنية ونسب تنافسية، مع تطبيق سلس وسحوبات سريعة بالعملة المحلية."}},
 "code-promo-paripesa": {
  "bonus": {"fr":"100% sur le 1er dépôt","en":"100% on 1st deposit","es":"100% en el 1er depósito","ar":"100% على أول إيداع"},
  "intro": {
   "fr":"Paripesa est apprécié pour sa simplicité et sa rapidité, avec une offre solide sur le football africain et international et des paiements adaptés aux pays francophones.",
   "en":"Paripesa is loved for its simplicity and speed, with strong coverage of African and international football and payments suited to French-speaking countries.",
   "es":"Paripesa es apreciada por su sencillez y rapidez, con una sólida oferta de fútbol africano e internacional y pagos adaptados a los países francófonos.",
   "ar":"يُقدَّر Paripesa لبساطته وسرعته، مع تغطية قوية لكرة القدم الإفريقية والدولية ووسائل دفع مناسبة للدول الناطقة بالفرنسية."}},
 "code-promo-megapari": {
  "bonus": {"fr":"100% sur le 1er dépôt","en":"100% on 1st deposit","es":"100% en el 1er depósito","ar":"100% على أول إيداع"},
  "intro": {
   "fr":"Megapari propose une plateforme moderne : large choix de sports, casino intégré et promotions régulières, en plus d'un bonus de bienvenue généreux.",
   "en":"Megapari offers a modern platform with a wide range of sports, an integrated casino, regular promotions and a generous welcome bonus.",
   "es":"Megapari ofrece una plataforma moderna con una amplia variedad de deportes, casino integrado, promociones frecuentes y un generoso bono de bienvenida.",
   "ar":"يوفّر Megapari منصّة عصرية بتشكيلة واسعة من الرياضات وكازينو مدمج وعروض منتظمة إضافةً إلى مكافأة ترحيب سخية."}},
 "code-promo-winwin": {
  "bonus": {"fr":"100% sur le 1er dépôt","en":"100% on 1st deposit","es":"100% en el 1er depósito","ar":"100% على أول إيداع"},
  "intro": {
   "fr":"WinWin est un bookmaker en pleine croissance en Afrique, avec une application légère, des cotes attractives et des paiements Mobile Money pratiques.",
   "en":"WinWin is a fast-growing bookmaker in Africa, with a lightweight app, attractive odds and convenient Mobile Money payments.",
   "es":"WinWin es una casa de apuestas en pleno crecimiento en África, con una app ligera, cuotas atractivas y pagos Mobile Money prácticos.",
   "ar":"WinWin شركة مراهنات سريعة النمو في إفريقيا، بتطبيق خفيف ونسب جذّابة ومدفوعات Mobile Money عملية."}},
 "code-promo-betandyou": {
  "bonus": {"fr":"100% sur le 1er dépôt","en":"100% on 1st deposit","es":"100% en el 1er depósito","ar":"100% على أول إيداع"},
  "intro": {
   "fr":"BetAndYou réunit paris sportifs et casino sur une seule plateforme, avec des promotions fréquentes et une prise en main simple, idéale pour débuter.",
   "en":"BetAndYou combines sports betting and casino on a single platform, with frequent promotions and a simple, beginner-friendly experience.",
   "es":"BetAndYou reúne apuestas deportivas y casino en una sola plataforma, con promociones frecuentes y un manejo sencillo, ideal para principiantes.",
   "ar":"يجمع BetAndYou بين المراهنات الرياضية والكازينو في منصّة واحدة، مع عروض متكرّرة وتجربة بسيطة مناسبة للمبتدئين."}},
 "code-promo-betwiner": {
  "bonus": {"fr":"100% sur le 1er dépôt","en":"100% on 1st deposit","es":"100% en el 1er depósito","ar":"100% على أول إيداع"},
  "intro": {
   "fr":"Betwinner offre une couverture sportive très large, des cotes élevées et de nombreuses options de paiement, dont le Mobile Money et les cryptomonnaies.",
   "en":"Betwinner offers very broad sports coverage, high odds and many payment options, including Mobile Money and cryptocurrencies.",
   "es":"Betwinner ofrece una cobertura deportiva muy amplia, cuotas altas y numerosas opciones de pago, incluyendo Mobile Money y criptomonedas.",
   "ar":"يوفّر Betwinner تغطية رياضية واسعة جدًا ونسبًا مرتفعة وخيارات دفع متعدّدة، منها Mobile Money والعملات الرقمية."}},
 "code-promo-linebet": {
  "bonus": {"fr":"100% sur le 1er dépôt","en":"100% on 1st deposit","es":"100% en el 1er depósito","ar":"100% على أول إيداع"},
  "intro": {
   "fr":"Linebet mise sur la rapidité : inscription express, paris en direct fluides et retraits rapides, avec une bonne offre sur le football et l'eSport.",
   "en":"Linebet focuses on speed: express registration, smooth live betting and fast withdrawals, with strong football and eSports coverage.",
   "es":"Linebet apuesta por la rapidez: registro exprés, apuestas en vivo fluidas y retiros rápidos, con buena oferta de fútbol y eSports.",
   "ar":"يركّز Linebet على السرعة: تسجيل فوري ومراهنات مباشرة سلسة وسحوبات سريعة، مع تغطية جيّدة لكرة القدم والرياضات الإلكترونية."}},
 "code-promo-1xbit": {
  "bonus": {"fr":"Bonus crypto jusqu'à 7 BTC","en":"Crypto bonus up to 7 BTC","es":"Bono cripto hasta 7 BTC","ar":"مكافأة كريبتو حتى 7 BTC"},
  "intro": {
   "fr":"1xBit est un bookmaker 100% crypto : tu paries en Bitcoin, USDT ou Ethereum, sans vérification d'identité, avec des transactions rapides et anonymes.",
   "en":"1xBit is a 100% crypto bookmaker: bet in Bitcoin, USDT or Ethereum, with no identity verification and fast, anonymous transactions.",
   "es":"1xBit es una casa de apuestas 100% cripto: apuesta en Bitcoin, USDT o Ethereum, sin verificación de identidad y con transacciones rápidas y anónimas.",
   "ar":"1xBit شركة مراهنات بالعملات الرقمية بالكامل: راهن بعملة Bitcoin أو USDT أو Ethereum دون التحقّق من الهوية، مع معاملات سريعة ومجهولة."}},
 "code-promo-fastparie": {
  "bonus": {"fr":"100% sur le 1er dépôt","en":"100% on 1st deposit","es":"100% en el 1er depósito","ar":"100% على أول إيداع"},
  "intro": {
   "fr":"Fastparie est pensé pour la rapidité : inscription simple, paris football en quelques clics et paiements adaptés à l'Afrique francophone.",
   "en":"Fastparie is built for speed: simple registration, football betting in a few clicks and payments suited to French-speaking Africa.",
   "es":"Fastparie está pensada para la rapidez: registro sencillo, apuestas de fútbol en pocos clics y pagos adaptados al África francófona.",
   "ar":"صُمّم Fastparie من أجل السرعة: تسجيل بسيط ومراهنات كرة قدم بنقرات قليلة ووسائل دفع مناسبة لإفريقيا الناطقة بالفرنسية."}},
 "code-promo-afroparie": {
  "bonus": {"fr":"100% sur le 1er dépôt","en":"100% on 1st deposit","es":"100% en el 1er depósito","ar":"100% على أول إيداع"},
  "intro": {
   "fr":"Afroparie est un bookmaker orienté public africain, avec une interface en français, des cotes locales et des dépôts Mobile Money faciles à utiliser.",
   "en":"Afroparie is a bookmaker focused on the African audience, with a French interface, local odds and easy Mobile Money deposits.",
   "es":"Afroparie es una casa de apuestas orientada al público africano, con interfaz en francés, cuotas locales y depósitos Mobile Money fáciles de usar.",
   "ar":"Afroparie شركة مراهنات موجّهة للجمهور الإفريقي، بواجهة بالفرنسية ونسب محلية وإيداعات Mobile Money سهلة الاستخدام."}},
 "code-promo-1win": {
  "bonus": {"fr":"Jusqu'à 500% sur les 1ers dépôts","en":"Up to 500% on first deposits","es":"Hasta 500% en los primeros depósitos","ar":"حتى 500% على أول الإيداعات"},
  "intro": {
   "fr":"1win est réputé pour son bonus de bienvenue très élevé (jusqu'à 500% sur les premiers dépôts), son casino intégré et son application rapide.",
   "en":"1win is known for its very high welcome bonus (up to 500% on your first deposits), its integrated casino and its fast app.",
   "es":"1win es conocido por su bono de bienvenida muy alto (hasta 500% en los primeros depósitos), su casino integrado y su app rápida.",
   "ar":"يشتهر 1win بمكافأة ترحيب مرتفعة جدًا (حتى 500% على أول إيداعاتك) وكازينو مدمج وتطبيق سريع."}},
}

# ---------------------------------------------------------------- Bonus code FFN (300 %)
# Bookmakers du code FFN : 300 % jusqu'a 300 000 FCFA dans les pays FCFA (1xBit exclu : 100 % crypto, pas de FCFA)
FFN300 = {"code-promo-1xbet", "code-promo-melbet", "code-promo-paripesa", "code-promo-megapari",
          "code-promo-winwin", "code-promo-afroparie", "code-promo-goldpari"}
B300 = {"fr": "300% jusqu'à 300 000 FCFA", "en": "300% up to 300,000 FCFA", "es": "300% hasta 300 000 FCFA", "ar": "300% حتى 300 000 فرنك CFA"}
FCFA_PAYS = ["Cameroun", "Côte d'Ivoire", "Sénégal", "Burkina Faso", "Bénin", "Mali", "Togo"]
for _b in BOOKMAKERS:
    if _b["slug"] in FFN300:
        _b["bonus_max"] = B300["fr"]
        _keep = [(c, v) for c, v in _b["countries"] if c not in FCFA_PAYS and c not in ("Afrique", "Afrique francophone")]
        _b["countries"] = [(c, B300["fr"]) for c in FCFA_PAYS] + _keep
        BK_CONTENT.setdefault(_b["slug"], {})["bonus"] = dict(B300)
FFN300_NAMES = {_b["name"] for _b in BOOKMAKERS if _b["slug"] in FFN300}

def pct(x, lang="fr", long=False):
    """'300%' pour les bookmakers du code FFN, sinon '100%'. x = bookmaker (dict) ou son nom."""
    hit = (x.get("slug") in FFN300) if isinstance(x, dict) else (x in FFN300_NAMES)
    if not hit: return "100%"
    return ("300% (" + B300[lang].split(" ", 1)[1] + ")") if long else "300%"

def bk_bonus(b, lang):
    return BK_CONTENT.get(b["slug"], {}).get("bonus", {}).get(lang, b.get("bonus_max", ""))
def bk_intro(b, lang):
    return BK_CONTENT.get(b["slug"], {}).get("intro", {}).get(lang, "")

# Dimensions des affiches 2026 (JPG compresses, max 1200 px de large ; WebP en priorite)
AFFICHE_DIMS = {
 "1xbet":1122,"1xbit":1122,"afroparie":1200,"betandyou":1122,"betwiner":1200,
 "fastparie":1200,"goldpari":1122,"linebet":1122,"megapari":1122,"melbet":1122,
 "paripesa":1122,"winwin":1122,"1win":1200,
}
AFFICHE_DIMS_H = {
 "1xbet":1402,"1xbit":1402,"afroparie":400,"betandyou":1402,"betwiner":900,
 "fastparie":400,"goldpari":1402,"linebet":1402,"megapari":1402,"melbet":1402,
 "paripesa":1402,"winwin":1402,"1win":400,
}
def affiche_img(b, lang):
    fn = b["slug"].replace("code-promo-", "")
    alts = {
     "fr": f"Affiche code promo {b['name']} 2026 : {b['code']} — Cousin Marc",
     "en": f"{b['name']} promo code 2026 poster: {b['code']} — Cousin Marc",
     "es": f"Póster código promocional {b['name']} 2026: {b['code']} — Cousin Marc",
     "ar": f"ملصق الرمز الترويجي {b['name']} 2026: {b['code']} — Cousin Marc",
    }
    alt = alts.get(lang, alts["fr"])
    w = AFFICHE_DIMS.get(fn, 520); h = AFFICHE_DIMS_H.get(fn, 520)
    return (f'<div class="wrap" style="padding:6px 20px 0">'
            f'<a href="{b["site"]}" rel="sponsored nofollow" style="display:block;max-width:460px;margin:0 auto">'
            f'<picture><source srcset="affiche-{fn}.webp" type="image/webp">'
            f'<img src="affiche-{fn}.jpg" alt="{alt}" loading="lazy" decoding="async" width="{w}" height="{h}" '
            f'style="width:100%;height:auto;display:block;border-radius:22px;box-shadow:0 14px 40px rgba(0,0,0,.4)"></picture></a></div>')


# ===== MUR DES GAGNANTS (vrais coupons payes) =====
WINNERS = [
 ("win-01.jpg","4 426 500 F"),("win-02.jpg","2 059 771 F"),("win-03.jpg","2 750 000 F"),
 ("win-04.jpg","3 582 211 F"),("win-05.jpg","2 162 500 F"),("win-06.jpg","2 660 000 F"),
 ("win-07.jpg","2 530 858 F"),("win-08.jpg","2 400 000 F"),("win-09.jpg","4 268 352 F"),
 ("win-10.jpg","5 117 482 F"),
]
WALL_L = {
 "fr": ("\U0001F3C6 Ils ont gagne\u0301 avec Cousin Marc",
        "S\u00e9lection de coupons pay\u00e9s r\u00e9cemment partag\u00e9s par la communaut\u00e9. Les r\u00e9sultats pass\u00e9s ne garantissent pas les r\u00e9sultats futurs.","Pay\u00e9"),
 "en": ("\U0001F3C6 They won with Cousin Marc",
        "A selection of recently paid coupons shared by the community. Past results do not guarantee future results.","Paid"),
 "es": ("\U0001F3C6 Ganaron con Cousin Marc",
        "Una selecci\u00f3n de cupones pagados recientemente compartidos por la comunidad. Los resultados pasados no garantizan resultados futuros.","Pagado"),
 "ar": ("\U0001F3C6 \u0644\u0642\u062f \u0631\u0628\u062d\u0648\u0627 \u0645\u0639 Cousin Marc",
        "\u0645\u062c\u0645\u0648\u0639\u0629 \u0645\u062e\u062a\u0627\u0631\u0629 \u0645\u0646 \u0627\u0644\u0642\u0633\u0627\u0626\u0645 \u0627\u0644\u0645\u062f\u0641\u0648\u0639\u0629 \u0645\u0624\u062e\u0631\u064b\u0627 \u0648\u0627\u0644\u062a\u064a \u0634\u0627\u0631\u0643\u0647\u0627 \u0623\u0641\u0631\u0627\u062f \u0627\u0644\u0645\u062c\u062a\u0645\u0639. \u0627\u0644\u0646\u062a\u0627\u0626\u062c \u0627\u0644\u0633\u0627\u0628\u0642\u0629 \u0644\u0627 \u062a\u0636\u0645\u0646 \u0646\u062a\u0627\u0626\u062c \u0645\u0633\u062a\u0642\u0628\u0644\u064a\u0629.","\u0645\u062f\u0641\u0648\u0639"),
}
def winners_wall(lang):
    title, sub, paid = WALL_L.get(lang, WALL_L["fr"])
    cards = "".join(
      f'<div class="wcard"><img src="{img}" alt="Coupon gagnant {gain} Cousin Marc" loading="lazy" width="360" height="760"><div class="wbadge">\u2705 {paid} \u00b7 {gain}</div></div>'
      for img, gain in WINNERS)
    track = cards + cards
    css = ""
    return (f'<section class="winsec">{css}'
      f'<div class="wrap" style="text-align:center"><h2 style="justify-content:center">{title}</h2>'
      f'<p style="max-width:600px;margin:8px auto 0">{sub}</p></div>'
      f'<div class="winmarq"><div class="wtrack">{track}</div></div>'
      f'</section>')



ARTICLES = [
{
"slug":"comment-sinscrire-1xbet-2026",
"title":"Comment s'inscrire sur 1xBet en 2026 (guide étape par étape)",
"date_iso":"2026-06-17","date_fr":"17 juin 2026",
"desc":"Guide complet pour s'inscrire sur 1xBet en 2026 : étapes, code promo FFN et vérification du compte. Expliqué simplement par Cousin Marc.",
"excerpt":"Ouvrir un compte 1xBet en moins de 5 minutes : la procédure complète, étape par étape, avec le code promo pour le bonus maximum.",
"body":"""<p class="meta">Par Cousin Marc</p>
<p>Tu veux ouvrir un compte 1xBet mais tu ne sais pas par où commencer ? Je te montre la procédure complète. Ça prend moins de 5 minutes.</p>
<h2>Ce qu'il te faut avant de commencer</h2>
<ul>
<li>Un numéro de téléphone valide</li>
<li>Une adresse email</li>
<li>Un moyen de paiement (Orange Money, MTN MoMo, Moov Money, carte...)</li>
<li>Avoir 18 ans ou plus</li>
</ul>
<h2>Les étapes d'inscription</h2>
<ol class="steps">
<li><b>Ouvre la page d'inscription</b> de 1xBet via le bouton sur ma page dédiée.</li>
<li><b>Choisis ton pays et ta devise.</b> Le bonus s'adapte automatiquement à ta zone.</li>
<li><b>Remplis tes informations</b> : téléphone, email et un mot de passe solide.</li>
<li><b>Saisis le code promo <span style="color:var(--gold)">FFN</span></b> dans le champ prévu, avant de valider. C'est lui qui débloque le bonus maximum.</li>
<li><b>Valide ton compte</b> puis fais ton premier dépôt pour activer le bonus.</li>
</ol>
<h2>🎥 Le tuto en vidéo</h2>
<p>Je montre l'inscription complète et comment créer un compte authentique, étape par étape :</p>
<div class="video yt-facade" data-yt="EnBk9p_Akvc" data-yt-title="Comment s'inscrire - tuto Cousin Marc"><img src="https://img.youtube.com/vi/EnBk9p_Akvc/hqdefault.jpg" alt="Comment s'inscrire - tuto Cousin Marc" loading="lazy"><span class="ytf-play">▶</span></div>
<p style="margin-top:12px"><a href="https://youtu.be/EnBk9p_Akvc" rel="nofollow" style="color:var(--gold);font-weight:700">▶️ Regarder sur YouTube</a> &nbsp;·&nbsp; <a href="https://youtube.com/@prossport" rel="nofollow" style="color:var(--gold);font-weight:700">S'abonner à la chaîne</a></p>
<h2>N'oublie pas le code promo</h2>
<p>Le champ « code promo » apparaît pendant l'inscription. Si tu l'oublies à ce moment-là, tu ne pourras pas l'ajouter après coup. Colle donc bien <b>FFN</b> avant de finaliser. Tous les détails sont sur ma page <a href="code-promo-1xbet.html">code promo 1xBet</a>.</p>
<h2>Vérifie ton compte dès le début</h2>
<p>Pour retirer tes gains sans blocage plus tard, pense à vérifier ton identité dans les paramètres de ton compte dès l'inscription. Ça t'évite les mauvaises surprises au moment du retrait.</p>
<div class="note">⚠️ Réservé aux 18 ans et +. Le pari comporte des risques, ne mise que ce que tu peux te permettre de perdre.</div>""",
"cta_slug":"code-promo-1xbet","cta_label":"Voir le code promo 1xBet",
},
{
"slug":"deposer-retirer-paris-afrique",
"title":"Comment retirer ses gains sur 1xBet, Melbet, Paripesa (Mobile Money + Crypto)",
"date_iso":"2026-06-16","date_fr":"16 juin 2026",
"desc":"Comment retirer ses gains sur 1xBet, Melbet, Paripesa en Afrique : Mobile Money (Orange Money, MTN, Moov) et cryptomonnaie, expliqué en vidéo par Cousin Marc.",
"excerpt":"Comment retirer ton argent sur les sites de paris en Afrique : Mobile Money et crypto, expliqué simplement et en vidéo.",
"body":"""<p class="meta">Par Cousin Marc</p>
<p>En Afrique, la plupart des parieurs utilisent le mobile money. Voici comment alimenter ton compte et récupérer tes gains, simplement.</p>
<h2>🎥 Le tuto en vidéo</h2>
<p>Je te montre tout en vidéo : le retrait par Mobile Money (Orange Money, MTN, Moov) et par cryptomonnaie, étape par étape.</p>
<div class="video yt-facade" data-yt="ogsHWfjycBE" data-yt-title="Comment retirer ses gains - tuto Cousin Marc"><img src="https://img.youtube.com/vi/ogsHWfjycBE/hqdefault.jpg" alt="Comment retirer ses gains - tuto Cousin Marc" loading="lazy"><span class="ytf-play">▶</span></div>
<p style="margin-top:12px"><a href="https://youtu.be/ogsHWfjycBE" rel="nofollow" style="color:var(--gold);font-weight:700">▶️ Regarder sur YouTube</a> &nbsp;·&nbsp; <a href="https://youtube.com/@prossport" rel="nofollow" style="color:var(--gold);font-weight:700">S'abonner à la chaîne</a></p>
<h2>Les moyens de paiement les plus utilisés</h2>
<ul>
<li>Orange Money</li>
<li>MTN Mobile Money (MoMo)</li>
<li>Moov Money</li>
<li>Wave (selon les pays)</li>
<li>Cartes bancaires, et crypto sur certains sites</li>
</ul>
<h2>Comment déposer</h2>
<ol class="steps">
<li><b>Connecte-toi</b> à ton compte sur le site ou l'application.</li>
<li><b>Va dans la section « Dépôt ».</b></li>
<li><b>Choisis ton mobile money</b> (Orange Money, MTN...).</li>
<li><b>Entre le montant</b> puis valide avec le code reçu par SMS.</li>
</ol>
<h2>Comment retirer tes gains</h2>
<ol class="steps">
<li><b>Va dans « Retrait ».</b></li>
<li><b>Choisis le même moyen</b> que pour ton dépôt.</li>
<li><b>Entre le montant</b> et confirme.</li>
</ol>
<h2>Retrait par cryptomonnaie</h2>
<p>Certains sites permettent aussi de retirer en crypto (USDT, Bitcoin, TON...). Pour ça, il te faut un portefeuille crypto (wallet). Dans la section « Retrait », choisis la crypto, colle l'adresse de ton wallet, entre le montant et confirme. C'est souvent rapide, mais vérifie bien l'adresse avant de valider : une erreur d'adresse est irréversible.</p>
<h2>Délais et conseils</h2>
<ul>
<li>Les dépôts sont en général <b>instantanés</b>.</li>
<li>Les retraits prennent de quelques minutes à quelques heures.</li>
<li>Garde le <b>même moyen</b> pour le dépôt et le retrait.</li>
<li>Vérifie ton compte (identité) avant de demander un gros retrait.</li>
</ul>
<h2>Sécurité</h2>
<p>Ne partage jamais ton code de confirmation mobile money ni ton mot de passe. Aucun « agent » sérieux ne te demandera ça en message privé. Méfie-toi des faux comptes qui usurpent mon nom.</p>
<div class="note">⚠️ Réservé aux 18 ans et +. Joue de manière responsable.</div>""",
"cta_slug":"","cta_label":"",
},
{
"slug":"5-conseils-parier-football",
"title":"5 conseils pour mieux parier sur le football",
"date_iso":"2026-06-15","date_fr":"15 juin 2026",
"desc":"5 conseils simples pour parier plus malin sur le foot : budget, cotes, combinés, analyse et jeu responsable. Les bases par Cousin Marc.",
"excerpt":"Parier, c'est d'abord du plaisir. Voici 5 principes simples pour éviter les erreurs classiques et parier plus malin.",
"body":"""<p class="meta">Par Cousin Marc</p>
<p>Parier sur le foot, c'est avant tout du plaisir. Mais quelques principes simples peuvent t'éviter les erreurs les plus courantes. Voici mes 5 conseils.</p>
<h2>1. Fixe-toi un budget</h2>
<p>Décide à l'avance combien tu peux miser sur le mois, et ne dépasse jamais cette somme. Ne parie jamais avec de l'argent dont tu as besoin pour autre chose.</p>
<h2>2. Comprends les cotes</h2>
<p>Une cote, c'est une probabilité. Plus la cote est haute, moins l'événement est probable. Une cote de 1.50 est « plus sûre » qu'une cote de 4.00, mais rapporte moins. Apprends à lire ça avant de miser.</p>
<h2>3. Évite les combinés à rallonge</h2>
<p>Mettre 10 matchs dans un seul coupon, c'est tentant pour la grosse cote, mais il suffit d'un seul match raté pour tout perdre. Les combinés courts (2 à 4 matchs) sont plus réalistes.</p>
<h2>4. Analyse avant de parier</h2>
<p>Regarde la forme des équipes, les blessures, les confrontations passées, le contexte du match. Un pari réfléchi vaut mieux que dix paris au feeling.</p>
<h2>5. Joue de manière responsable</h2>
<p>Le pari n'est pas un moyen de gagner sa vie. Si ça devient une source de stress ou que tu paries pour « te refaire », fais une pause. Lis ma page <a href="jeu-responsable.html">jeu responsable</a>.</p>
<div class="note">⚠️ Réservé aux 18 ans et +. Aucun pronostic n'est garanti.</div>""",
"cta_slug":"","cta_label":"",
},
]

# Correspondance slug FR -> slug EN pour les articles
ARTICLE_FR2EN = {
"comment-sinscrire-1xbet-2026":"how-to-register-1xbet-2026",
"deposer-retirer-paris-afrique":"how-to-withdraw-1xbet-melbet-paripesa",
"5-conseils-parier-football":"5-tips-football-betting",
}

ARTICLE_FR2ES = {
"comment-sinscrire-1xbet-2026":"como-registrarse-1xbet-2026",
"deposer-retirer-paris-afrique":"como-retirar-1xbet-melbet-paripesa",
"5-conseils-parier-football":"5-consejos-apuestas-futbol",
}

ARTICLES_ES = [
{
"slug":"como-registrarse-1xbet-2026","fr_slug":"comment-sinscrire-1xbet-2026",
"title":"Cómo registrarse en 1xBet en 2026 (guía paso a paso)",
"date_iso":"2026-06-17","date_es":"17 de junio de 2026",
"desc":"Guía completa para registrarse en 1xBet en 2026: pasos, código promocional FFN y verificación de la cuenta. Explicado de forma sencilla por Cousin Marc.",
"excerpt":"Abre una cuenta de 1xBet en menos de 5 minutos: el proceso completo paso a paso, con el código promocional para el bono máximo.",
"body":"""<p class="meta">Por Cousin Marc</p>
<p>¿Quieres abrir una cuenta de 1xBet pero no sabes por dónde empezar? Te muestro todo el proceso. Tardarás menos de 5 minutos.</p>
<h2>Lo que necesitas antes de empezar</h2>
<ul>
<li>Un número de teléfono válido</li>
<li>Una dirección de correo electrónico</li>
<li>Un método de pago (Orange Money, MTN MoMo, tarjeta...)</li>
<li>Ser mayor de 18 años</li>
</ul>
<h2>Los pasos del registro</h2>
<ol class="steps">
<li><b>Abre la página de registro</b> de 1xBet con el botón de mi página dedicada.</li>
<li><b>Elige tu país y tu moneda.</b> El bono se adapta automáticamente a tu zona.</li>
<li><b>Rellena tus datos</b>: teléfono, correo y una contraseña segura.</li>
<li><b>Introduce el código promocional <span style="color:var(--gold)">FFN</span></b> en el campo correspondiente, antes de confirmar. Es lo que desbloquea el bono máximo.</li>
<li><b>Confirma tu cuenta</b> y haz tu primer depósito para activar el bono.</li>
</ol>
<h2>🎥 El tutorial en vídeo</h2>
<p>Muestro el registro completo y cómo crear una cuenta auténtica, paso a paso:</p>
<div class="video yt-facade" data-yt="EnBk9p_Akvc" data-yt-title="Cómo registrarse - tutorial Cousin Marc"><img src="https://img.youtube.com/vi/EnBk9p_Akvc/hqdefault.jpg" alt="Cómo registrarse - tutorial Cousin Marc" loading="lazy"><span class="ytf-play">▶</span></div>
<p style="margin-top:12px"><a href="https://youtu.be/EnBk9p_Akvc" rel="nofollow" style="color:var(--gold);font-weight:700">▶️ Ver en YouTube</a> &nbsp;·&nbsp; <a href="https://youtube.com/@prossport" rel="nofollow" style="color:var(--gold);font-weight:700">Suscribirse al canal</a></p>
<h2>No olvides el código promocional</h2>
<p>El campo «código promocional» aparece durante el registro. Si lo olvidas en ese momento, no podrás añadirlo después. Así que pega bien <b>FFN</b> antes de finalizar. Todos los detalles están en mi página <a href="1xbet-codigo-promocional.html">código promocional 1xBet</a>.</p>
<h2>Verifica tu cuenta desde el principio</h2>
<p>Para retirar tus ganancias más tarde sin bloqueos, recuerda verificar tu identidad en los ajustes de tu cuenta nada más registrarte. Te evita sorpresas desagradables al retirar.</p>
<div class="note">⚠️ Solo mayores de 18 años. Apostar implica riesgos, apuesta solo lo que puedas permitirte perder.</div>""",
"cta_slug":"1xbet-codigo-promocional","cta_label":"Ver el código promocional 1xBet",
},
{
"slug":"como-retirar-1xbet-melbet-paripesa","fr_slug":"deposer-retirer-paris-afrique",
"title":"Cómo retirar tus ganancias en 1xBet, Melbet, Paripesa (Mobile Money + Cripto)",
"date_iso":"2026-06-16","date_es":"16 de junio de 2026",
"desc":"Cómo retirar tus ganancias en 1xBet, Melbet, Paripesa: Mobile Money (Orange Money, MTN, Moov) y criptomonedas, explicado en vídeo por Cousin Marc.",
"excerpt":"Cómo retirar tu dinero en los sitios de apuestas: Mobile Money y cripto, explicado de forma sencilla y en vídeo.",
"body":"""<p class="meta">Por Cousin Marc</p>
<p>Muchos apostadores usan el mobile money o las criptomonedas. Aquí te explico cómo recargar tu cuenta y recuperar tus ganancias, de forma sencilla.</p>
<h2>🎥 El tutorial en vídeo</h2>
<p>Te muestro todo en vídeo: el retiro por Mobile Money (Orange Money, MTN, Moov) y por criptomoneda, paso a paso.</p>
<div class="video yt-facade" data-yt="ogsHWfjycBE" data-yt-title="Cómo retirar ganancias - tutorial Cousin Marc"><img src="https://img.youtube.com/vi/ogsHWfjycBE/hqdefault.jpg" alt="Cómo retirar ganancias - tutorial Cousin Marc" loading="lazy"><span class="ytf-play">▶</span></div>
<p style="margin-top:12px"><a href="https://youtu.be/ogsHWfjycBE" rel="nofollow" style="color:var(--gold);font-weight:700">▶️ Ver en YouTube</a> &nbsp;·&nbsp; <a href="https://youtube.com/@prossport" rel="nofollow" style="color:var(--gold);font-weight:700">Suscribirse al canal</a></p>
<h2>Los métodos de pago más usados</h2>
<ul>
<li>Orange Money</li>
<li>MTN Mobile Money (MoMo)</li>
<li>Moov Money</li>
<li>Tarjetas bancarias</li>
<li>Criptomonedas en algunos sitios</li>
</ul>
<h2>Cómo depositar</h2>
<ol class="steps">
<li><b>Inicia sesión</b> en tu cuenta en el sitio o la app.</li>
<li><b>Ve a la sección «Depósito».</b></li>
<li><b>Elige tu método</b> (Mobile Money, tarjeta...).</li>
<li><b>Introduce el importe</b> y confirma con el código recibido por SMS.</li>
</ol>
<h2>Cómo retirar tus ganancias</h2>
<ol class="steps">
<li><b>Ve a «Retiro».</b></li>
<li><b>Elige el mismo método</b> que usaste para depositar.</li>
<li><b>Introduce el importe</b> y confirma.</li>
</ol>
<h2>Retiro por criptomoneda</h2>
<p>Algunos sitios permiten retirar en cripto (USDT, Bitcoin, TON...). Para eso necesitas una cartera (wallet). En la sección «Retiro», elige la cripto, pega la dirección de tu wallet, introduce el importe y confirma. Suele ser rápido, pero verifica bien la dirección antes de confirmar: un error de dirección es irreversible.</p>
<h2>Plazos y consejos</h2>
<ul>
<li>Los depósitos suelen ser <b>instantáneos</b>.</li>
<li>Los retiros tardan de unos minutos a unas horas.</li>
<li>Usa el <b>mismo método</b> para depositar y retirar.</li>
<li>Verifica tu cuenta (identidad) antes de pedir un retiro grande.</li>
</ul>
<h2>Seguridad</h2>
<p>Nunca compartas tu código de confirmación ni tu contraseña. Ningún «agente» serio te pedirá eso por mensaje privado. Desconfía de las cuentas falsas que usurpan mi nombre.</p>
<div class="note">⚠️ Solo mayores de 18 años. Juega de forma responsable.</div>""",
"cta_slug":"","cta_label":"",
},
{
"slug":"5-consejos-apuestas-futbol","fr_slug":"5-conseils-parier-football",
"title":"5 consejos para apostar mejor en el fútbol",
"date_iso":"2026-06-15","date_es":"15 de junio de 2026",
"desc":"5 consejos sencillos para apostar de forma más inteligente en el fútbol: presupuesto, cuotas, combinadas, análisis y juego responsable. Lo básico por Cousin Marc.",
"excerpt":"Apostar es ante todo diversión. Aquí tienes 5 principios sencillos para evitar los errores clásicos y apostar mejor.",
"body":"""<p class="meta">Por Cousin Marc</p>
<p>Apostar en el fútbol es ante todo diversión. Pero unos pocos principios sencillos pueden ahorrarte los errores más comunes. Aquí van mis 5 consejos.</p>
<h2>1. Fíjate un presupuesto</h2>
<p>Decide de antemano cuánto puedes apostar al mes, y nunca lo superes. Nunca apuestes con dinero que necesitas para otra cosa.</p>
<h2>2. Entiende las cuotas</h2>
<p>Una cuota es una probabilidad. Cuanto más alta es la cuota, menos probable es el evento. Una cuota de 1.50 es «más segura» que una de 4.00, pero paga menos. Aprende a leer eso antes de apostar.</p>
<h2>3. Evita las combinadas interminables</h2>
<p>Poner 10 partidos en un solo boleto es tentador por la cuota alta, pero basta un partido fallado para perderlo todo. Las combinadas cortas (2 a 4 partidos) son más realistas.</p>
<h2>4. Analiza antes de apostar</h2>
<p>Mira el estado de forma de los equipos, las lesiones, los enfrentamientos pasados, el contexto del partido. Una apuesta pensada vale más que diez apuestas por intuición.</p>
<h2>5. Juega de forma responsable</h2>
<p>Apostar no es una forma de ganarse la vida. Si se convierte en fuente de estrés o apuestas para «recuperar», haz una pausa. Lee mi página <a href="juego-responsable.html">juego responsable</a>.</p>
<div class="note">⚠️ Solo mayores de 18 años. Ningún pronóstico está garantizado.</div>""",
"cta_slug":"","cta_label":"",
},
]

ARTICLE_FR2AR = {
"comment-sinscrire-1xbet-2026":"comment-sinscrire-1xbet-2026-ar",
"deposer-retirer-paris-afrique":"deposer-retirer-paris-afrique-ar",
"5-conseils-parier-football":"5-conseils-parier-football-ar",
}

ARTICLES_AR = [
{
"slug":"comment-sinscrire-1xbet-2026-ar","fr_slug":"comment-sinscrire-1xbet-2026",
"title":"كيفية التسجيل في 1xBet في 2026 (دليل خطوة بخطوة)",
"date_iso":"2026-06-17","date_ar":"17 يونيو 2026",
"desc":"دليل كامل للتسجيل في 1xBet في 2026: الخطوات، الرمز الترويجي FFN والتحقق من الحساب. شرح مبسّط من Cousin Marc.",
"excerpt":"افتح حساب 1xBet في أقل من 5 دقائق: العملية كاملة خطوة بخطوة، مع الرمز الترويجي للحصول على أقصى مكافأة.",
"body":"""<p class="meta">بقلم Cousin Marc</p>
<p>تريد فتح حساب 1xBet لكنك لا تعرف من أين تبدأ؟ سأشرح لك العملية كاملة. تستغرق أقل من 5 دقائق.</p>
<h2>ما تحتاجه قبل البدء</h2>
<ul>
<li>رقم هاتف صالح</li>
<li>عنوان بريد إلكتروني</li>
<li>وسيلة دفع (Orange Money، MTN MoMo، بطاقة بنكية...)</li>
<li>أن يكون عمرك 18 عامًا أو أكثر</li>
</ul>
<h2>خطوات التسجيل</h2>
<ol class="steps">
<li><b>افتح صفحة التسجيل</b> في 1xBet عبر الزر الموجود في صفحتي المخصصة.</li>
<li><b>اختر بلدك وعملتك.</b> تتكيّف المكافأة تلقائيًا مع منطقتك.</li>
<li><b>أدخل بياناتك</b>: الهاتف، البريد الإلكتروني وكلمة مرور قوية.</li>
<li><b>أدخل الرمز الترويجي <span style="color:var(--gold)">FFN</span></b> في الحقل المخصص قبل التأكيد. هو الذي يفعّل أقصى مكافأة.</li>
<li><b>أكّد حسابك</b> ثم قم بإيداعك الأول لتفعيل المكافأة.</li>
</ol>
<h2>🎥 الشرح بالفيديو</h2>
<p>أعرض التسجيل الكامل وكيفية إنشاء حساب صحيح، خطوة بخطوة:</p>
<div class="video yt-facade" data-yt="EnBk9p_Akvc" data-yt-title="كيفية التسجيل - شرح Cousin Marc"><img src="https://img.youtube.com/vi/EnBk9p_Akvc/hqdefault.jpg" alt="كيفية التسجيل - شرح Cousin Marc" loading="lazy"><span class="ytf-play">▶</span></div>
<p style="margin-top:12px"><a href="https://youtu.be/EnBk9p_Akvc" rel="nofollow" style="color:var(--gold);font-weight:700">▶️ المشاهدة على YouTube</a> &nbsp;·&nbsp; <a href="https://youtube.com/@prossport" rel="nofollow" style="color:var(--gold);font-weight:700">اشترك في القناة</a></p>
<h2>لا تنسَ الرمز الترويجي</h2>
<p>يظهر حقل «الرمز الترويجي» أثناء التسجيل. إذا نسيته في تلك اللحظة، لن تتمكن من إضافته لاحقًا. لذا أدخل <b>FFN</b> قبل إنهاء التسجيل. كل التفاصيل في صفحتي <a href="1xbet-promo-ar.html">الرمز الترويجي 1xBet</a>.</p>
<h2>تحقق من حسابك من البداية</h2>
<p>لسحب أرباحك لاحقًا دون عوائق، تذكّر التحقق من هويتك في إعدادات حسابك فور التسجيل. هذا يجنّبك المفاجآت غير السارة عند السحب.</p>
<div class="note">⚠️ للبالغين فقط (18 عامًا فأكثر). المراهنة تنطوي على مخاطر، راهن فقط بما يمكنك تحمّل خسارته.</div>""",
"cta_slug":"1xbet-promo-ar","cta_label":"عرض الرمز الترويجي 1xBet",
},
{
"slug":"deposer-retirer-paris-afrique-ar","fr_slug":"deposer-retirer-paris-afrique",
"title":"كيفية سحب أرباحك على 1xBet، Melbet، Paripesa (Mobile Money + العملات الرقمية)",
"date_iso":"2026-06-16","date_ar":"16 يونيو 2026",
"desc":"كيفية سحب أرباحك على 1xBet، Melbet، Paripesa: Mobile Money والعملات الرقمية، مشروح بالفيديو من Cousin Marc.",
"excerpt":"كيفية سحب أموالك من مواقع المراهنات: Mobile Money والعملات الرقمية، بشرح مبسّط وبالفيديو.",
"body":"""<p class="meta">بقلم Cousin Marc</p>
<p>يستخدم الكثير من المراهنين المحافظ الإلكترونية أو العملات الرقمية. إليك كيفية شحن حسابك واسترداد أرباحك ببساطة.</p>
<h2>🎥 الشرح بالفيديو</h2>
<p>أعرض لك كل شيء بالفيديو: السحب عبر Mobile Money وعبر العملات الرقمية، خطوة بخطوة.</p>
<div class="video yt-facade" data-yt="ogsHWfjycBE" data-yt-title="كيفية سحب الأرباح - شرح Cousin Marc"><img src="https://img.youtube.com/vi/ogsHWfjycBE/hqdefault.jpg" alt="كيفية سحب الأرباح - شرح Cousin Marc" loading="lazy"><span class="ytf-play">▶</span></div>
<p style="margin-top:12px"><a href="https://youtu.be/ogsHWfjycBE" rel="nofollow" style="color:var(--gold);font-weight:700">▶️ المشاهدة على YouTube</a> &nbsp;·&nbsp; <a href="https://youtube.com/@prossport" rel="nofollow" style="color:var(--gold);font-weight:700">اشترك في القناة</a></p>
<h2>وسائل الدفع الأكثر استخدامًا</h2>
<ul>
<li>Orange Money</li>
<li>MTN Mobile Money (MoMo)</li>
<li>Moov Money</li>
<li>البطاقات البنكية</li>
<li>العملات الرقمية على بعض المواقع</li>
</ul>
<h2>كيفية الإيداع</h2>
<ol class="steps">
<li><b>سجّل الدخول</b> إلى حسابك على الموقع أو التطبيق.</li>
<li><b>اذهب إلى قسم «الإيداع».</b></li>
<li><b>اختر وسيلتك</b> (Mobile Money، بطاقة...).</li>
<li><b>أدخل المبلغ</b> ثم أكّد بالرمز المستلَم عبر الرسائل القصيرة.</li>
</ol>
<h2>كيفية سحب أرباحك</h2>
<ol class="steps">
<li><b>اذهب إلى «السحب».</b></li>
<li><b>اختر نفس الوسيلة</b> التي استخدمتها للإيداع.</li>
<li><b>أدخل المبلغ</b> وأكّد.</li>
</ol>
<h2>السحب بالعملات الرقمية</h2>
<p>تتيح بعض المواقع السحب بالعملات الرقمية (USDT، Bitcoin، TON...). لذلك تحتاج إلى محفظة. في قسم «السحب»، اختر العملة، الصق عنوان محفظتك، أدخل المبلغ وأكّد. غالبًا ما يكون سريعًا، لكن تحقق جيدًا من العنوان قبل التأكيد: خطأ في العنوان لا يمكن التراجع عنه.</p>
<h2>المدد والنصائح</h2>
<ul>
<li>الإيداعات عادةً <b>فورية</b>.</li>
<li>عمليات السحب تستغرق من دقائق إلى ساعات.</li>
<li>استخدم <b>نفس الوسيلة</b> للإيداع والسحب.</li>
<li>تحقق من حسابك (الهوية) قبل طلب سحب كبير.</li>
</ul>
<h2>الأمان</h2>
<p>لا تشارك أبدًا رمز التأكيد أو كلمة المرور. لا يطلب منك أي «وكيل» جاد ذلك عبر رسالة خاصة. احذر من الحسابات المزيفة التي تنتحل اسمي.</p>
<div class="note">⚠️ للبالغين فقط (18 عامًا فأكثر). العب بمسؤولية.</div>""",
"cta_slug":"","cta_label":"",
},
{
"slug":"5-conseils-parier-football-ar","fr_slug":"5-conseils-parier-football",
"title":"5 نصائح للمراهنة بذكاء على كرة القدم",
"date_iso":"2026-06-15","date_ar":"15 يونيو 2026",
"desc":"5 نصائح بسيطة للمراهنة بذكاء على كرة القدم: الميزانية، الاحتمالات، المركّبات، التحليل والمراهنة المسؤولة. الأساسيات من Cousin Marc.",
"excerpt":"المراهنة متعة قبل كل شيء. إليك 5 مبادئ بسيطة لتجنّب الأخطاء الشائعة والمراهنة بذكاء.",
"body":"""<p class="meta">بقلم Cousin Marc</p>
<p>المراهنة على كرة القدم متعة قبل كل شيء. لكن بعض المبادئ البسيطة قد تجنّبك أكثر الأخطاء شيوعًا. إليك نصائحي الخمس.</p>
<h2>1. حدّد ميزانية</h2>
<p>قرّر مسبقًا كم يمكنك أن تراهن شهريًا، ولا تتجاوز هذا المبلغ أبدًا. لا تراهن أبدًا بمال تحتاجه لشيء آخر.</p>
<h2>2. افهم الاحتمالات</h2>
<p>الاحتمال هو احتمالية. كلما ارتفع الاحتمال، قلّ ترجيح وقوع الحدث. احتمال 1.50 «أكثر أمانًا» من احتمال 4.00، لكنه يربح أقل. تعلّم قراءة ذلك قبل المراهنة.</p>
<h2>3. تجنّب المركّبات الطويلة</h2>
<p>وضع 10 مباريات في قسيمة واحدة مغرٍ بسبب الاحتمال الكبير، لكن خسارة مباراة واحدة تكفي لخسارة كل شيء. المركّبات القصيرة (من 2 إلى 4 مباريات) أكثر واقعية.</p>
<h2>4. حلّل قبل المراهنة</h2>
<p>انظر إلى حالة الفرق، الإصابات، المواجهات السابقة، سياق المباراة. رهان مدروس خير من عشرة رهانات بالحدس.</p>
<h2>5. العب بمسؤولية</h2>
<p>المراهنة ليست وسيلة لكسب العيش. إذا أصبحت مصدر توتر أو راهنت كي «تعوّض» خسارتك، توقّف قليلًا. اقرأ صفحتي <a href="jeu-responsable-ar.html">المراهنة المسؤولة</a>.</p>
<div class="note">⚠️ للبالغين فقط (18 عامًا فأكثر). لا يوجد توقّع مضمون.</div>""",
"cta_slug":"","cta_label":"",
},
]

ARTICLES_EN = [
{
"slug":"how-to-register-1xbet-2026","fr_slug":"comment-sinscrire-1xbet-2026",
"title":"How to Register on 1xBet in 2026 (Step-by-Step Guide)",
"date_iso":"2026-06-17","date_en":"June 17, 2026",
"desc":"Complete guide to register on 1xBet in 2026: steps, promo code FFN and account verification. Explained simply by Cousin Marc.",
"excerpt":"Open a 1xBet account in under 5 minutes: the full step-by-step process, with the promo code for the maximum bonus.",
"body":"""<p class="meta">By Cousin Marc</p>
<p>Want to open a 1xBet account but don't know where to start? Let me walk you through the whole process. It takes less than 5 minutes.</p>
<h2>What you need before you start</h2>
<ul>
<li>A valid phone number</li>
<li>An email address</li>
<li>A payment method (Orange Money, MTN MoMo, Moov Money, card...)</li>
<li>To be 18 or older</li>
</ul>
<h2>The registration steps</h2>
<ol class="steps">
<li><b>Open the 1xBet registration page</b> using the button on my dedicated page.</li>
<li><b>Choose your country and currency.</b> The bonus adapts automatically to your region.</li>
<li><b>Fill in your details</b>: phone, email and a strong password.</li>
<li><b>Enter the promo code <span style="color:var(--gold)">FFN</span></b> in the dedicated field before confirming. This is what unlocks the maximum bonus.</li>
<li><b>Confirm your account</b> then make your first deposit to activate the bonus.</li>
</ol>
<h2>🎥 Video tutorial</h2>
<p>I show the full registration and how to create a genuine account, step by step:</p>
<div class="video yt-facade" data-yt="EnBk9p_Akvc" data-yt-title="How to register - Cousin Marc tutorial"><img src="https://img.youtube.com/vi/EnBk9p_Akvc/hqdefault.jpg" alt="How to register - Cousin Marc tutorial" loading="lazy"><span class="ytf-play">▶</span></div>
<p style="margin-top:12px"><a href="https://youtu.be/EnBk9p_Akvc" rel="nofollow" style="color:var(--gold);font-weight:700">▶️ Watch on YouTube</a> &nbsp;·&nbsp; <a href="https://youtube.com/@prossport" rel="nofollow" style="color:var(--gold);font-weight:700">Subscribe to the channel</a></p>
<h2>Don't forget the promo code</h2>
<p>The "promo code" field appears during registration. If you forget it at that moment, you cannot add it afterwards. So make sure to paste <b>FFN</b> before finalizing. All the details are on my <a href="1xbet-promo-code.html">1xBet promo code</a> page.</p>
<h2>Verify your account from the start</h2>
<p>To withdraw your winnings later without any blocks, remember to verify your identity in your account settings right after signing up. It saves you nasty surprises at withdrawal time.</p>
<div class="note">⚠️ 18+ only. Betting involves risk, only stake what you can afford to lose.</div>""",
"cta_slug":"1xbet-promo-code","cta_label":"See the 1xBet promo code",
},
{
"slug":"how-to-withdraw-1xbet-melbet-paripesa","fr_slug":"deposer-retirer-paris-afrique",
"title":"How to Withdraw Your Winnings on 1xBet, Melbet, Paripesa (Mobile Money + Crypto)",
"date_iso":"2026-06-16","date_en":"June 16, 2026",
"desc":"How to withdraw your winnings on 1xBet, Melbet, Paripesa in Africa: Mobile Money (Orange Money, MTN, Moov) and cryptocurrency, explained on video by Cousin Marc.",
"excerpt":"How to withdraw your money on betting sites in Africa: Mobile Money and crypto, explained simply and on video.",
"body":"""<p class="meta">By Cousin Marc</p>
<p>In Africa, most bettors use mobile money. Here's how to fund your account and get your winnings out, simply.</p>
<h2>🎥 Video tutorial</h2>
<p>I show you everything on video: withdrawal by Mobile Money (Orange Money, MTN, Moov) and by cryptocurrency, step by step.</p>
<div class="video yt-facade" data-yt="ogsHWfjycBE" data-yt-title="How to withdraw winnings - Cousin Marc tutorial"><img src="https://img.youtube.com/vi/ogsHWfjycBE/hqdefault.jpg" alt="How to withdraw winnings - Cousin Marc tutorial" loading="lazy"><span class="ytf-play">▶</span></div>
<p style="margin-top:12px"><a href="https://youtu.be/ogsHWfjycBE" rel="nofollow" style="color:var(--gold);font-weight:700">▶️ Watch on YouTube</a> &nbsp;·&nbsp; <a href="https://youtube.com/@prossport" rel="nofollow" style="color:var(--gold);font-weight:700">Subscribe to the channel</a></p>
<h2>The most used payment methods</h2>
<ul>
<li>Orange Money</li>
<li>MTN Mobile Money (MoMo)</li>
<li>Moov Money</li>
<li>Wave (depending on country)</li>
<li>Bank cards, and crypto on some sites</li>
</ul>
<h2>How to deposit</h2>
<ol class="steps">
<li><b>Log in</b> to your account on the site or the app.</li>
<li><b>Go to the "Deposit" section.</b></li>
<li><b>Choose your mobile money</b> (Orange Money, MTN...).</li>
<li><b>Enter the amount</b> then confirm with the code received by SMS.</li>
</ol>
<h2>How to withdraw your winnings</h2>
<ol class="steps">
<li><b>Go to "Withdrawal".</b></li>
<li><b>Choose the same method</b> you used for your deposit.</li>
<li><b>Enter the amount</b> and confirm.</li>
</ol>
<h2>Withdrawal by cryptocurrency</h2>
<p>Some sites also let you withdraw in crypto (USDT, Bitcoin, TON...). For that, you need a crypto wallet. In the "Withdrawal" section, choose the crypto, paste your wallet address, enter the amount and confirm. It's often fast, but double-check the address before confirming: an address mistake is irreversible.</p>
<h2>Timing and tips</h2>
<ul>
<li>Deposits are generally <b>instant</b>.</li>
<li>Withdrawals take from a few minutes to a few hours.</li>
<li>Keep the <b>same method</b> for deposit and withdrawal.</li>
<li>Verify your account (identity) before requesting a large withdrawal.</li>
</ul>
<h2>Security</h2>
<p>Never share your mobile money confirmation code or your password. No serious "agent" will ever ask you for that in a private message. Beware of fake accounts impersonating my name.</p>
<div class="note">⚠️ 18+ only. Play responsibly.</div>""",
"cta_slug":"","cta_label":"",
},
{
"slug":"5-tips-football-betting","fr_slug":"5-conseils-parier-football",
"title":"5 Tips to Bet Smarter on Football",
"date_iso":"2026-06-15","date_en":"June 15, 2026",
"desc":"5 simple tips to bet smarter on football: budget, odds, accumulators, analysis and responsible gambling. The basics by Cousin Marc.",
"excerpt":"Betting is first about fun. Here are 5 simple principles to avoid the classic mistakes and bet smarter.",
"body":"""<p class="meta">By Cousin Marc</p>
<p>Betting on football is first and foremost about fun. But a few simple principles can save you from the most common mistakes. Here are my 5 tips.</p>
<h2>1. Set yourself a budget</h2>
<p>Decide in advance how much you can stake for the month, and never go over it. Never bet with money you need for something else.</p>
<h2>2. Understand the odds</h2>
<p>Odds represent a probability. The higher the odds, the less likely the event. Odds of 1.50 are "safer" than odds of 4.00, but pay less. Learn to read that before staking.</p>
<h2>3. Avoid endless accumulators</h2>
<p>Putting 10 matches in a single slip is tempting for the big odds, but a single missed match loses everything. Short accumulators (2 to 4 matches) are more realistic.</p>
<h2>4. Analyze before betting</h2>
<p>Look at team form, injuries, past head-to-heads, the match context. One thoughtful bet beats ten gut-feeling bets.</p>
<h2>5. Play responsibly</h2>
<p>Betting is not a way to make a living. If it becomes a source of stress or you bet to "win it back", take a break. Read my <a href="responsible-gambling.html">responsible gambling</a> page.</p>
<div class="note">⚠️ 18+ only. No prediction is guaranteed.</div>""",
"cta_slug":"","cta_label":"",
},
]

ICONS = {
"Telegram":'<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3 18.6 19.1c-.2 1-.9 1.3-1.8.8l-4.9-3.6-2.4 2.3c-.3.3-.5.5-1 .5l.3-4.9 9-8.1c.4-.3-.1-.5-.6-.2L6.8 13.5l-4.8-1.5c-1-.3-1-1 .2-1.5l18.8-7.2c.9-.3 1.6.2 1.3 1z"/></svg>',
"WhatsApp":'<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.8-1.5A10 10 0 1 0 12 2zm5.5 14.1c-.2.7-1.4 1.3-2 1.4-.5.1-1.1.1-1.8-.1-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5-4.5-.2-.2-1.2-1.6-1.2-3s.7-2.1 1-2.4c.2-.3.5-.4.7-.4h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.3 0 .5l-.4.6c-.2.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.2.1.4.1.6-.1l.8-1c.2-.2.3-.2.6-.1l1.9.9c.3.1.5.2.6.4.1.2.1.7-.1 1.4z"/></svg>',
"YouTube":'<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M23 7.5c-.3-1-1-1.8-2-2C19 5 12 5 12 5s-7 0-9 .5c-1 .2-1.7 1-2 2C.5 9.5.5 12 .5 12s0 2.5.5 4.5c.3 1 1 1.8 2 2C5 19 12 19 12 19s7 0 9-.5c1-.2 1.7-1 2-2 .5-2 .5-4.5.5-4.5s0-2.5-.5-4.5zM9.8 15.3V8.7l5.7 3.3-5.7 3.3z"/></svg>',
"Facebook":'<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.2c-1.2 0-1.6.8-1.6 1.5V12h2.7l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z"/></svg>',
"Instagram":'<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M12 4.5c2.5 0 2.8 0 3.8.1.9 0 1.4.2 1.7.3.4.2.7.4 1 .7.3.3.5.6.7 1 .1.3.3.8.3 1.7.1 1 .1 1.3.1 3.7s0 2.7-.1 3.7c0 .9-.2 1.4-.3 1.7-.2.4-.4.7-.7 1-.3.3-.6.5-1 .7-.3.1-.8.3-1.7.3-1 .1-1.3.1-3.8.1s-2.8 0-3.8-.1c-.9 0-1.4-.2-1.7-.3-.4-.2-.7-.4-1-.7-.3-.3-.5-.6-.7-1-.1-.3-.3-.8-.3-1.7-.1-1-.1-1.3-.1-3.7s0-2.7.1-3.7c0-.9.2-1.4.3-1.7.2-.4.4-.7.7-1 .3-.3.6-.5 1-.7.3-.1.8-.3 1.7-.3 1-.1 1.3-.1 3.8-.1zM12 8.1a3.9 3.9 0 1 0 0 7.8 3.9 3.9 0 0 0 0-7.8zm0 6.4a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5zm4-6.6a.9.9 0 1 1-1.8 0 .9.9 0 0 1 1.8 0z"/></svg>',
"Snapchat":'<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M12 2.5c2.5 0 4.2 1.8 4.3 4.3 0 .6 0 1.1-.1 1.7.3.2.7.2 1 0 .2-.1.4-.1.6-.1.5 0 .8.4.8.8 0 .5-.4.7-.9 1-.5.2-1 .4-1.1.7-.1.3.1.6.3.9.6 1 1.7 1.8 2.8 2.1.3.1.6.3.6.6 0 .6-1.1 1-1.9 1.1-.2 0-.3.2-.4.4-.1.3-.1.6-.4.7-.2.1-.5.1-.8.1-.5 0-1 0-1.5.2-.5.2-1 .7-1.9.7s-1.4-.5-1.9-.7c-.5-.2-1-.2-1.5-.2-.4 0-.6 0-.8-.1-.3-.1-.3-.4-.4-.7-.1-.2-.2-.4-.4-.4-.8-.1-1.9-.5-1.9-1.1 0-.3.2-.5.6-.6 1.1-.3 2.2-1.1 2.8-2.1.2-.3.4-.6.3-.9-.1-.3-.6-.5-1.1-.7-.5-.3-.9-.5-.9-1 0-.4.4-.8.9-.8.2 0 .4 0 .6.1.3.2.7.2 1 0-.1-.6-.1-1.1-.1-1.7C7.8 4.3 9.5 2.5 12 2.5z"/></svg>',
}

CSS = """
/* ==========================================================
   COUSIN MARC — design 2026 « clair & pro »
   Blanc · noir · vert. Mobile d'abord.
   ========================================================== */
:root{
  --bg:#ffffff;--soft:#f4f6f3;--soft2:#eef1ed;
  --ink:#0a0d0b;--ink2:#2a302c;--muted:#5d6862;--line:#e3e7e4;
  --green:#2563eb;--green-d:#1d4ed8;--green-ink:#1d4ed8;--green-soft:#eef4ff;
  --red:#e5322d;--radius:18px;
  --shadow:0 1px 2px rgba(10,13,11,.04),0 8px 24px rgba(10,13,11,.06);
  --shadow-lg:0 2px 4px rgba(10,13,11,.04),0 24px 60px rgba(10,13,11,.10);
  --display:"Bricolage Grotesque","Inter",-apple-system,"Segoe UI",sans-serif;
  --sans:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  /* anciens noms (styles en ligne du generateur) remappes sur le theme clair */
  --pitch:#ffffff;--pitch-deep:var(--soft);--gold:var(--green-ink);--gold-deep:var(--green-d);
  --orange:#ff6b2c;--mist:var(--muted);--floodlight:var(--ink);--turf:var(--green-soft);
  --text2:var(--ink2);--home-green:var(--green-ink);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;background:var(--bg);-webkit-text-size-adjust:100%}
body{font-family:var(--sans);background:var(--bg);color:var(--ink);font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
img{max-width:100%}
a{color:inherit}
p{color:var(--ink2)}
b,strong{color:var(--ink);font-weight:700}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
main.wrap{max-width:880px}
h1,h2,h3,h4{font-family:var(--display);color:var(--ink);letter-spacing:-.025em;line-height:1.1}
h1{font-size:clamp(36px,6.4vw,64px);font-weight:800}
h2{font-size:clamp(24px,3.6vw,32px);font-weight:800;margin-bottom:14px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
h3{font-size:20px;font-weight:700}
.hl{color:var(--green-ink);background:linear-gradient(180deg,transparent 62%,rgba(37,99,235,.22) 62%);padding:0 .06em}
.muted{color:var(--muted)}
::selection{background:rgba(37,99,235,.25)}
:focus-visible{outline:3px solid var(--green);outline-offset:2px;border-radius:6px}

/* ---------- BARRE DE NAVIGATION ---------- */
nav.top{position:sticky;top:0;z-index:60;background:rgba(255,255,255,.88);backdrop-filter:saturate(1.6) blur(14px);-webkit-backdrop-filter:saturate(1.6) blur(14px);border-bottom:1px solid var(--line)}
nav.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:64px}
nav.top .logo{display:flex;align-items:center;gap:9px;text-decoration:none;font-family:var(--display);font-weight:800;font-size:20px;letter-spacing:-.03em;color:var(--ink);white-space:nowrap}
nav.top .logo .dot{width:12px;height:12px;border-radius:50%;background:var(--green);box-shadow:0 0 0 4px var(--green-soft)}
nav.top .logo b{color:var(--green-ink)}
[dir="rtl"] nav.top .logo{direction:ltr}
/* ---------- BANDEAU DEFILANT + BANDE AFRIQUE ---------- */
.ticker{position:relative;background:linear-gradient(90deg,#1d4ed8,#2563eb 50%,#1d4ed8);color:#fff;overflow:hidden;white-space:nowrap;font-size:13px;font-weight:700;line-height:1;direction:ltr}
.ticker::after{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;background:linear-gradient(90deg,#16a34a 0 33.34%,#dc2626 33.34% 66.67%,#facc15 66.67%)}
.ticker-track{display:inline-flex;padding:10px 0 12px;animation:tickmove 42s linear infinite;will-change:transform}
.ticker:hover .ticker-track{animation-play-state:paused}
.ticker a{color:#fff;text-decoration:none;padding:0 22px;unicode-bidi:plaintext}
.ticker a:hover{text-decoration:underline}
.ticker a+a::before{content:"";display:inline-block;width:5px;height:5px;border-radius:50%;background:#facc15;margin:0 22px 1px -22px;vertical-align:middle}
@keyframes tickmove{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@media(prefers-reduced-motion:reduce){.ticker-track{animation:none}.ticker{overflow-x:auto}}
/* code FFN qui brille doucement + cartes qui se soulevent */
.tcode,.codebox .code{background-image:linear-gradient(100deg,transparent 30%,rgba(255,255,255,.75) 50%,transparent 70%);background-size:220% 100%;background-repeat:no-repeat;background-position:-120% 0;animation:ffnshine 4.5s ease-in-out infinite}
@keyframes ffnshine{0%,55%{background-position:-120% 0}100%{background-position:220% 0}}
@media(prefers-reduced-motion:reduce){.tcode,.codebox .code{animation:none}}
.tcard,.bkrow,.mcard{transition:transform .18s,box-shadow .18s}
@media(hover:hover){.tcard:hover,.mcard:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg)}}
.related a.flagc{border-left:5px solid var(--fc,#2563eb)}
.related a.flagc .bk::before{content:attr(data-flag) " ";font-size:20px}
.toplinks{display:none;align-items:center;gap:4px;list-style:none}
.toplinks a{display:block;text-decoration:none;font-weight:600;font-size:14.5px;color:var(--ink2);padding:8px 12px;border-radius:999px;transition:background .15s,color .15s}
.toplinks a:hover{background:var(--soft);color:var(--ink)}
.toplinks a.vip{background:var(--ink);color:#fff;padding:8px 16px}
.toplinks a.vip:hover{background:#000}
.toplang{display:none;gap:2px;list-style:none;margin-left:6px;padding-left:10px;border-left:1px solid var(--line)}
.toplang a{display:block;font-size:12px;font-weight:700;letter-spacing:.04em;text-decoration:none;color:var(--muted);padding:6px 7px;border-radius:8px}
.toplang a:hover{color:var(--ink);background:var(--soft)}
.navright{display:flex;align-items:center;gap:4px}
.burger{width:44px;height:44px;border:1px solid var(--line);background:#fff;border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;cursor:pointer}
.burger span{display:block;width:18px;height:2px;background:var(--ink);border-radius:2px}
@media(min-width:960px){.toplinks,.toplang{display:flex}.burger{display:none}}

/* panneau mobile */
.navmask{position:fixed;inset:0;background:rgba(10,13,11,.35);opacity:0;pointer-events:none;transition:opacity .2s;z-index:90}
.navmask.open{opacity:1;pointer-events:auto}
.navpanel{position:fixed;top:0;right:0;bottom:0;width:min(340px,88vw);background:#fff;z-index:100;transform:translateX(105%);transition:transform .25s ease;display:flex;flex-direction:column;padding:20px;box-shadow:var(--shadow-lg);overflow-y:auto}
[dir="rtl"] .navpanel{right:auto;left:0;transform:translateX(-105%)}
.navpanel.open{transform:none}
.navpanel-head{font-family:var(--display);font-weight:800;font-size:22px;padding:6px 6px 16px;border-bottom:1px solid var(--line);margin-bottom:10px}
.navpanel-links{display:flex;flex-direction:column;gap:2px}
.navpanel-links a{display:flex;align-items:center;gap:12px;padding:13px 10px;border-radius:12px;text-decoration:none;font-weight:600;font-size:16px;color:var(--ink)}
.navpanel-links a:hover,.navpanel-links a.active{background:var(--green-soft);color:var(--green-ink)}
.navpanel-links .ic{width:24px;text-align:center}
.navpanel-lang{margin-top:auto;padding-top:16px;border-top:1px solid var(--line)}
.langrow{display:flex;gap:8px;list-style:none;flex-wrap:wrap}
.langlink{display:inline-block;text-decoration:none;font-weight:700;font-size:13px;padding:8px 14px;border:1px solid var(--line);border-radius:999px;color:var(--ink2)}
.langlink:hover{border-color:var(--ink);color:var(--ink)}

/* ---------- BANDEAU VIDEO ---------- */
.ytbar{display:flex;align-items:center;gap:14px;margin:18px auto 0;max-width:880px;padding:10px;border:1px solid var(--line);border-radius:16px;background:#fff}
.ytthumb{position:relative;flex:0 0 auto;width:112px;border-radius:10px;overflow:hidden;display:block;line-height:0}
.ytthumb img{width:112px;height:64px;object-fit:cover;display:block}
.ytplay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:18px;color:#fff;background:rgba(0,0,0,.28)}
.ytinfo{flex:1;min-width:0;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.yttitle{font-weight:700;font-size:14.5px;color:var(--ink)}
.ytsub{display:inline-block;background:var(--red);color:#fff;font-weight:700;font-size:13px;padding:8px 14px;border-radius:999px;text-decoration:none;white-space:nowrap}

/* ---------- HERO DES PAGES ---------- */
.hero{position:relative;padding:56px 0 48px;background:
  radial-gradient(900px 420px at 92% -10%,rgba(37,99,235,.13),transparent 60%),
  linear-gradient(180deg,var(--soft),#fff);border-bottom:1px solid var(--line)}
.hero .wrap{max-width:1120px}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:var(--muted);margin-bottom:16px}
.eyebrow::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--green)}
.hero h1{margin-bottom:16px}
.hero .sub{font-size:18px;max-width:560px;color:var(--ink2)}
.hero .btnrow{justify-content:flex-start}
@media(min-width:900px){
  .hero .wrap:has(.codebox){display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);column-gap:56px;align-items:center}
  .hero .wrap:has(.codebox)>*{grid-column:1}
  .hero .wrap:has(.codebox)>.codebox{grid-column:2;grid-row:1 / span 5;margin:0}
}
.hero-points{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px;list-style:none}
.hero-point{font-size:13px;font-weight:600;padding:7px 12px;border-radius:999px;background:#fff;border:1px solid var(--line)}
.combadge{display:inline-block;margin-top:16px;font-size:14px;padding:8px 14px;border-radius:999px;background:#fff;border:1px solid var(--line)}

/* ---------- CARTE CODE PROMO ---------- */
.codebox{position:relative;margin:28px 0 0;background:#fff;border:1px solid var(--line);border-radius:24px;padding:26px 24px 22px;box-shadow:var(--shadow-lg);text-align:center;max-width:460px}
.codebox .lab{display:block;font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.codebox .code{margin:14px 0 10px;font-family:var(--display);font-weight:800;font-size:clamp(44px,9vw,64px);letter-spacing:.08em;line-height:1;color:var(--ink);background:var(--green-soft);border:2px dashed var(--green);border-radius:16px;padding:18px 10px}
.codebox small{display:block;font-size:13px;color:var(--muted)}
.stamp{display:inline-block;margin-bottom:12px;font-size:12px;font-weight:700;color:var(--green-ink);background:var(--green-soft);border-radius:999px;padding:5px 12px}
.stamp br{display:none}
.stamp .st-txt::before{content:"✓ "}
.copybtn{margin-top:16px;width:100%;cursor:pointer;font:inherit;font-weight:700;font-size:16px;color:#fff;background:var(--ink);border:none;border-radius:14px;padding:15px 18px;transition:transform .1s,background .15s}
.copybtn:hover{background:#000}
.copybtn:active{transform:scale(.98)}
.reg{margin-top:12px;font-size:14px;color:var(--ink2)}

/* ---------- BOUTONS ---------- */
.btnrow{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:24px}
.cta{display:inline-flex;align-items:center;justify-content:center;gap:8px;text-decoration:none;font-weight:700;font-size:15.5px;color:#fff;background:var(--green);border:1px solid var(--green);border-radius:14px;padding:14px 22px;transition:background .15s,transform .1s,box-shadow .15s;box-shadow:0 6px 18px rgba(37,99,235,.25)}
.cta:hover{background:#1d4ed8;box-shadow:0 8px 24px rgba(37,99,235,.35)}
.cta:active{transform:scale(.98)}
.cta.alt{background:#fff;color:var(--ink);border-color:var(--line);box-shadow:none}
.cta.alt:hover{border-color:var(--ink)}

/* ---------- AFFICHE ---------- */
.wrap>a>picture img,picture img{border-radius:20px!important;box-shadow:var(--shadow-lg)!important;border:1px solid var(--line)!important}

/* ---------- SECTIONS DE CONTENU ---------- */
main.wrap>section,main>section{padding:44px 0;border-bottom:1px solid var(--line)}
main.wrap>section:last-child{border-bottom:none}
section p+p{margin-top:12px}
section ul,section ol{padding-left:22px;margin:12px 0}
[dir="rtl"] section ul,[dir="rtl"] section ol{padding-left:0;padding-right:22px}
section li{margin:6px 0;color:var(--ink2)}
.num{display:inline-flex;align-items:center;justify-content:center;font-family:var(--sans);font-size:12px;font-weight:800;letter-spacing:.04em;color:var(--green-ink);background:var(--green-soft);border-radius:999px;padding:4px 10px}
ol.steps{list-style:none;padding:0;margin:18px 0;counter-reset:st;display:grid;gap:10px}
ol.steps li{counter-increment:st;position:relative;padding:16px 16px 16px 60px;background:var(--soft);border-radius:14px;margin:0}
[dir="rtl"] ol.steps li{padding:16px 60px 16px 16px}
ol.steps li::before{content:counter(st);position:absolute;left:16px;top:14px;width:30px;height:30px;border-radius:50%;background:var(--ink);color:#fff;font-weight:800;font-size:14px;display:flex;align-items:center;justify-content:center}
[dir="rtl"] ol.steps li::before{left:auto;right:16px}
.note{margin-top:18px;padding:16px 18px;border-radius:14px;background:var(--green-soft);border:1px solid rgba(37,99,235,.25);color:var(--ink2);font-size:15px}
.note .cta{box-shadow:none}
.tablecard{margin-top:14px;border:1px solid var(--line);border-radius:16px;overflow:hidden;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:15px}
th{background:var(--soft);text-align:left;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:700;padding:12px 16px}
[dir="rtl"] th{text-align:right}
td{padding:13px 16px;border-top:1px solid var(--line);color:var(--ink2)}
td:last-child{font-weight:800;color:var(--ink)}
details{border:1px solid var(--line);border-radius:14px;margin-top:10px;background:#fff;overflow:hidden}
summary{cursor:pointer;list-style:none;padding:16px 48px 16px 18px;font-weight:700;position:relative}
[dir="rtl"] summary{padding:16px 18px 16px 48px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";position:absolute;right:18px;top:50%;transform:translateY(-50%);font-size:22px;font-weight:400;color:var(--muted)}
[dir="rtl"] summary::after{right:auto;left:18px}
details[open] summary::after{content:"–"}
details>p,details>div{padding:0 18px 16px}

/* ---------- AUTEUR / RESEAUX ---------- */
.author{display:flex;align-items:center;gap:14px;margin-top:8px}
.av{width:52px;height:52px;flex:0 0 auto;border-radius:50%;background:var(--ink);color:#fff;font-family:var(--display);font-weight:800;display:flex;align-items:center;justify-content:center}
.nm{font-weight:800}
.ro{font-size:14px;color:var(--muted)}
.social{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.social a{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-size:14px;font-weight:600;padding:9px 14px;border:1px solid var(--line);border-radius:999px;background:#fff}
.social a:hover{border-color:var(--ink)}
.social svg{width:18px;height:18px}
/* reseaux sociaux aux couleurs de chaque marque */
.social a{color:#fff;border:none;font-weight:700;transition:transform .15s,filter .15s}
.social a:hover{transform:translateY(-1px);filter:brightness(1.08)}
.social a[href*="t.me"]{background:#229ed9}
.social a[href*="whatsapp"]{background:#25d366}
.social a[href*="youtube"]{background:#ff0000}
.social a[href*="facebook"]{background:#1877f2}
.social a[href*="instagram"]{background:linear-gradient(45deg,#f9a825,#e1306c 45%,#833ab4)}
.social a[href*="snapchat"]{background:#fffc00;color:#111}
.truststats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:18px}
.truststat{background:var(--soft);border-radius:14px;padding:14px;text-align:center}
.truststat b{display:block;font-family:var(--display);font-size:26px}
.truststat span{font-size:13px;color:var(--muted)}

/* ---------- GRILLES DE BOOKMAKERS ---------- */
.related,.hubgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-top:16px}
.related a,.hubcard{display:block;text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px;transition:border-color .15s,transform .15s,box-shadow .15s}
.related a:hover,.hubcard:hover{border-color:var(--ink);transform:translateY(-2px);box-shadow:var(--shadow)}
.related .bk,.hubcard .bk{font-weight:800;font-size:16px;color:var(--ink)!important}
.related .cd,.hubcard .cd{font-size:13px;color:var(--muted);margin-top:2px}
.hubcard .bn{font-size:14px;color:var(--ink2);margin:4px 0 8px}
.hubcard .cd{display:inline-block;font-weight:800;color:var(--ink);background:var(--green-soft);border:1px dashed var(--green);border-radius:8px;padding:2px 9px}

/* ---------- MUR DES GAGNANTS ---------- */
.winsec{padding:56px 0;overflow:hidden;background:var(--soft);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.winmarq{overflow:hidden;margin-top:26px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 5%,#000 95%,transparent);mask-image:linear-gradient(90deg,transparent,#000 5%,#000 95%,transparent)}
.wtrack{display:flex;gap:14px;width:max-content;animation:wmarq 60s linear infinite}
.winsec:hover .wtrack{animation-play-state:paused}
.wcard{width:180px;flex:0 0 auto;background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:var(--shadow)}
.wcard img{width:100%;height:320px;object-fit:cover;object-position:top;display:block}
.wbadge{padding:10px 6px;text-align:center;color:var(--green-ink);font-weight:800;font-size:13px}
@keyframes wmarq{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@media(prefers-reduced-motion:reduce){.wtrack{animation:none}.winmarq{overflow-x:auto}}

/* ---------- VIDEO / COUPONS / ARTICLES ---------- */
.video,.yt-facade{position:relative;aspect-ratio:16/9;border-radius:18px;overflow:hidden;background:#000;margin-top:16px;cursor:pointer}
.yt-facade img{width:100%;height:100%;object-fit:cover;display:block}
.ytf-play{position:absolute;inset:0;margin:auto;width:68px;height:48px;border-radius:14px;background:var(--red);color:#fff;display:flex;align-items:center;justify-content:center;font-size:22px}
.couponimg{display:block;width:100%;max-width:560px;margin:16px auto 0;border-radius:18px;border:1px solid var(--line);box-shadow:var(--shadow)}
.postlist{display:grid;gap:12px;margin-top:16px}
.postcard{display:block;text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px;transition:border-color .15s,box-shadow .15s}
.postcard:hover{border-color:var(--ink);box-shadow:var(--shadow)}
.postcard .date,.meta{font-size:13px;color:var(--muted)}
.postcard .pt{font-family:var(--display);font-weight:700;font-size:20px;margin:4px 0 6px;color:var(--ink)}
.postcard .ex{font-size:15px;color:var(--ink2)}
.postcard .more{display:inline-block;margin-top:8px;font-weight:700;color:var(--green-ink)}
.article h2{margin-top:30px}
.legalbody h2{margin-top:26px;font-size:22px}

/* ---------- PIED DE PAGE ---------- */
footer{background:var(--ink);color:#c9d1cc;margin-top:64px;padding:56px 0 110px}
footer .cols{display:grid;grid-template-columns:repeat(2,1fr);gap:28px}
@media(min-width:820px){footer .cols{grid-template-columns:repeat(5,1fr)}}
footer h4{font-family:var(--sans);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#fff;margin-bottom:12px}
footer a{display:block;color:#c9d1cc;text-decoration:none;font-size:14.5px;padding:4px 0}
footer a:hover{color:#fff}
footer p{color:#8f9a94;font-size:13px}
footer .warn{margin-top:36px;padding:16px 18px;border-radius:14px;border:1px solid rgba(255,255,255,.12);font-size:13.5px;color:#c9d1cc;line-height:1.6}
footer .warn a{display:inline;color:#93c5fd!important}
@media(min-width:641px){footer{padding-bottom:48px}}

/* ---------- BARRE COLLANTE MOBILE ---------- */
.stickybar{position:fixed;left:10px;right:10px;bottom:10px;z-index:70;display:flex;align-items:center;gap:8px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:8px;box-shadow:var(--shadow-lg)}
.sb-code{font-family:var(--display);font-weight:800;font-size:18px;letter-spacing:.06em;padding:8px 12px;background:var(--green-soft);border:1px dashed var(--green);border-radius:12px}
.sb-copy{font:inherit;font-weight:700;font-size:14px;cursor:pointer;border:1px solid var(--line);background:#fff;border-radius:12px;padding:10px 12px;color:var(--ink)}
.sb-go{flex:1;text-align:center;text-decoration:none;font-weight:800;font-size:14px;color:#fff;background:var(--green);border-radius:12px;padding:11px 10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media(min-width:900px){.stickybar{display:none}}
body.has-sticky{padding-bottom:0}

/* ---------- ACCUEIL ---------- */
.home-hero{padding:56px 0 40px;background:
  radial-gradient(800px 380px at 100% 0%,rgba(37,99,235,.14),transparent 60%),
  linear-gradient(180deg,var(--soft),#fff 85%)}
.home-hero h1{font-size:clamp(44px,8.4vw,88px);line-height:.98;letter-spacing:-.04em;max-width:820px}
.home-hero h1 em{font-style:normal;color:var(--green-ink)}
.home-hero .lead{font-size:clamp(17px,2.2vw,20px);max-width:600px;margin-top:20px;color:var(--ink2)}
.home-hero .btnrow{justify-content:flex-start;margin-top:28px}
.home-trust{display:grid;grid-template-columns:repeat(4,auto);justify-content:start;gap:12px 28px;margin-top:30px;font-size:14px;color:var(--muted)}
.home-trust b{display:block;font-family:var(--display);font-size:26px;color:var(--ink);letter-spacing:-.02em}
.topcodes{display:grid;grid-template-columns:1fr;gap:12px;margin-top:40px}
@media(min-width:760px){.topcodes{grid-template-columns:repeat(3,1fr)}}
.tcard{position:relative;background:#fff;border:1px solid var(--line);border-radius:22px;padding:20px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:12px}
.tcard .trank{position:absolute;top:18px;right:18px;font-size:12px;font-weight:800;color:var(--muted)}
[dir="rtl"] .tcard .trank{right:auto;left:18px}
.tcard .tname{display:flex;align-items:center;gap:10px;font-family:var(--display);font-weight:800;font-size:22px}
.blogo{width:40px;height:40px;flex:0 0 auto;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#fff;font-family:var(--sans);font-weight:800;font-size:14px}
.tcard .tbonus{font-size:14.5px;color:var(--ink2);min-height:24px}
.tcode{display:flex;align-items:center;justify-content:space-between;gap:8px;background:var(--green-soft);border:2px dashed var(--green);border-radius:14px;padding:8px 8px 8px 16px}
[dir="rtl"] .tcode{padding:8px 16px 8px 8px}
.tcode span{font-family:var(--display);font-weight:800;font-size:26px;letter-spacing:.08em}
.tcode button{font:inherit;font-weight:700;font-size:13.5px;cursor:pointer;border:none;border-radius:10px;padding:9px 12px;background:var(--ink);color:#fff}
.tcard .tactions{display:flex;gap:8px}
.tcard .tactions a{flex:1;text-align:center;text-decoration:none;font-weight:700;font-size:14px;border-radius:12px;padding:11px 8px}
.tcard .tgo{background:var(--green);color:#fff}
.tcard .tmore{border:1px solid var(--line);color:var(--ink)}
.tcard .tmore:hover{border-color:var(--ink)}
.hsec{padding:64px 0;border-top:1px solid var(--line)}
.hsec-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:24px}
.hsec-head h2{margin:0;font-size:clamp(28px,4.4vw,44px)}
.hsec-head p{max-width:520px;margin-top:8px}
.kicker{font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--green-ink);margin-bottom:8px}
.bklist{border:1px solid var(--line);border-radius:22px;overflow:hidden;background:#fff}
.bkrow .bkname{font-weight:800;font-size:16.5px;color:var(--ink)}
.bkrow .bkbonus{font-size:13.5px;color:var(--muted)}
.bkrow .bkcode{font-family:var(--display);font-weight:800;letter-spacing:.06em;background:var(--green-soft);border:1px dashed var(--green);border-radius:10px;padding:6px 12px;color:var(--ink)}
.coupon-grid{display:grid;gap:22px;align-items:start}
@media(min-width:860px){.coupon-grid{grid-template-columns:1.1fr .9fr}}
.coupon-card{background:#fff;border:1px solid var(--line);border-radius:22px;padding:14px;box-shadow:var(--shadow)}
.coupon-card img,.coupon-card .couponimg{display:block;width:100%;max-width:none;margin:0;border:none;box-shadow:none;border-radius:14px}
.facts{display:grid;gap:10px}
.fact{display:flex;gap:14px;align-items:flex-start;background:var(--soft);border-radius:16px;padding:16px 18px}
.fact .fi{width:36px;height:36px;flex:0 0 auto;border-radius:10px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:18px;border:1px solid var(--line)}
.fact b{display:block}
.fact span{font-size:14.5px;color:var(--muted)}
.countrygrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.countrygrid a{display:flex;align-items:center;gap:10px;text-decoration:none;font-weight:700;background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.countrygrid a:hover{border-color:var(--ink)}
.tgband{display:grid;gap:20px;align-items:center;background:var(--ink);color:#fff;border-radius:28px;padding:36px 28px;margin:64px auto 0}
.tgband h2{color:#fff;font-size:clamp(26px,4vw,40px)}
.tgband p{color:#c9d1cc;max-width:520px}
.tgband .cta{justify-self:start}
@media(min-width:820px){.tgband{grid-template-columns:1fr auto;padding:44px 48px}}
.about-grid{display:grid;gap:24px}
@media(min-width:820px){.about-grid{grid-template-columns:1fr 1fr;align-items:center}}

/* ---------- VIP / DIVERS ---------- */
.label{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.ico{display:inline-flex}

/* ---------- LOGOS ---------- */
img.blogo{width:40px;height:40px;flex:0 0 auto;border-radius:12px;object-fit:cover;border:1px solid var(--line);background:#fff;display:block}
img.cblogo{display:block;width:64px;height:64px;margin:0 auto 12px;border-radius:18px;object-fit:cover;border:1px solid var(--line);box-shadow:var(--shadow)}
span.cblogo{display:flex;width:64px;height:64px;margin:0 auto 12px;border-radius:18px;align-items:center;justify-content:center;font-weight:800}
.rlogo{width:28px;height:28px;border-radius:8px;object-fit:cover;border:1px solid var(--line);vertical-align:middle;margin-right:10px;display:inline-block}
[dir="rtl"] .rlogo{margin-right:0;margin-left:10px}
span.rlogo{display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:800}

/* ---------- VIDEO EN TETE ---------- */
.vidhero{padding:28px 0 32px;background:var(--ink);color:#fff}
.vidgrid{display:grid;gap:20px;align-items:center}
@media(min-width:860px){.vidgrid{grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:40px}.vidhero{padding:40px 0 44px}}
.vidhero .yt-facade{margin:0;aspect-ratio:16/9;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.45);border:1px solid rgba(255,255,255,.08)}
.vidhero .yt-facade:hover .ytf-play{transform:scale(1.08)}
.vidhero .ytf-play{width:76px;height:54px;font-size:24px;border-radius:16px;transition:transform .15s;box-shadow:0 8px 24px rgba(0,0,0,.35)}
.vidtext .kicker{color:#93c5fd}
.vidtext h2{color:#fff;font-size:clamp(24px,3.4vw,36px);margin-bottom:10px}
.vidtext p{color:#c9d1cc}
.vidtext .ytsub{display:inline-block;margin-top:16px;background:var(--red);color:#fff;font-weight:700;font-size:14px;padding:11px 18px;border-radius:12px;text-decoration:none}

/* ---------- LISTE DES BOOKMAKERS (avec boutons) ---------- */
.verified{display:inline-flex;align-items:center;gap:6px;font-size:13.5px;font-weight:700;color:var(--green-ink);background:var(--green-soft);border-radius:999px;padding:7px 14px;margin:0 0 14px}
.bkrow{display:grid;grid-template-columns:auto 1fr auto;grid-template-areas:"logo info info" "code code join";gap:10px 14px;align-items:center;padding:14px 16px;border-top:1px solid var(--line)}
.bkrow:first-child{border-top:none}
.bkrow:hover{background:var(--soft)}
.bkrow .blogo{grid-area:logo}
.bkinfo{grid-area:info;text-decoration:none;display:flex;flex-direction:column;min-width:0}
.bkinfo:hover .bkname{text-decoration:underline}
.bkcodebox{grid-area:code;display:flex;align-items:center;justify-content:space-between;gap:8px;background:var(--green-soft);border:1px dashed var(--green);border-radius:12px;padding:5px 5px 5px 14px}
[dir="rtl"] .bkcodebox{padding:5px 14px 5px 5px}
.bkcodebox .bkcode{background:none;border:none;padding:0;font-size:17px}
.bkcodebox button,.tcode button{font:inherit;font-weight:700;font-size:13px;cursor:pointer;border:none;border-radius:9px;padding:8px 12px;background:var(--ink);color:#fff}
.bkjoin{grid-area:join;text-align:center;text-decoration:none;font-weight:700;font-size:14.5px;color:#fff;background:var(--green);border-radius:12px;padding:11px 16px;white-space:nowrap}
.bkjoin:hover{background:var(--green-d)}
@media(min-width:720px){
  .bkrow{grid-template-columns:auto 1fr 210px 130px;grid-template-areas:"logo info code join";padding:12px 18px}
}

/* ---------- BARRE MOBILE ACCUEIL ---------- */
.homebar .sb-go{background:var(--red)}
.sb-tg{flex:0 0 44px;width:44px;height:44px;border-radius:12px;background:#229ed9;display:flex;align-items:center;justify-content:center}
.stickybar{bottom:calc(10px + env(safe-area-inset-bottom,0px))}

/* ---------- COMPARATEUR ---------- */
.cmp{background:#fff;border:1px solid var(--line);border-radius:22px;padding:22px;box-shadow:var(--shadow)}
.cmp-step+.cmp-step{margin-top:18px}
.cmp-q{display:flex;align-items:center;gap:10px;font-weight:800;color:var(--ink);margin-bottom:10px}
.cmp-q span{width:26px;height:26px;border-radius:50%;background:var(--ink);color:#fff;font-size:13px;display:flex;align-items:center;justify-content:center}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font:inherit;font-weight:600;font-size:14.5px;cursor:pointer;border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:999px;padding:9px 15px;transition:border-color .15s,background .15s}
.chip:hover{border-color:var(--ink)}
.chip.on{background:var(--ink);border-color:var(--ink);color:#fff}
/* pays du comparateur aux couleurs du drapeau */
.cmp-c .chip[data-v]{color:#fff;font-weight:800;border:none;padding:10px 17px;text-shadow:0 1px 3px rgba(0,0,0,.75);box-shadow:inset 0 0 0 999px rgba(0,0,0,.28);transition:transform .15s,box-shadow .15s}
.cmp-c .chip[data-v]:hover{transform:translateY(-1px);box-shadow:inset 0 0 0 999px rgba(0,0,0,.18)}
.cmp-c .chip[data-v].on{outline:3px solid var(--ink);outline-offset:2px;box-shadow:inset 0 0 0 999px rgba(0,0,0,.12)}
.cmp-c .chip[data-v="cameroun"]{background:linear-gradient(90deg,#007a5e 0 33.3%,#ce1126 33.3% 66.6%,#fcd116 66.6%)}
.cmp-c .chip[data-v="cote-divoire"]{background:linear-gradient(90deg,#f77f00 0 33.3%,#e8e8e8 33.3% 66.6%,#009e60 66.6%)}
.cmp-c .chip[data-v="senegal"]{background:linear-gradient(90deg,#00853f 0 33.3%,#fdef42 33.3% 66.6%,#e31b23 66.6%)}
.cmp-c .chip[data-v="rdc"]{background:linear-gradient(150deg,#007fff 0 38%,#f7d618 38% 43%,#ce1021 43% 57%,#f7d618 57% 62%,#007fff 62%)}
.cmp-c .chip[data-v="benin"]{background:linear-gradient(90deg,#008751 0 40%,transparent 40%),linear-gradient(180deg,#fcd116 0 50%,#e8112d 50%)}
.cmp-c .chip[data-v="mali"]{background:linear-gradient(90deg,#14b53a 0 33.3%,#fcd116 33.3% 66.6%,#ce1126 66.6%)}
.cmp-c .chip[data-v="togo"]{background:linear-gradient(#d21034,#d21034) 0 0/34% 60% no-repeat,repeating-linear-gradient(180deg,#006a4e 0 20%,#ffce00 20% 40%)}
.cmp-c .chip[data-v="burkina-faso"]{background:linear-gradient(180deg,#ef2b2d 0 50%,#009e49 50%)}
.cmp-c .chip[data-v="autre"]{background:linear-gradient(135deg,#3b82f6,#1d4ed8)}
/* vrai logo Telegram dans les boutons */
.tgi{display:inline-block;width:20px;height:20px;vertical-align:-4px;margin-right:7px;flex:none}
.cmp-out:empty{display:none}
.cmp-out{margin-top:22px;padding-top:20px;border-top:1px solid var(--line)}
.cmp-title{font-family:var(--display);font-weight:800;font-size:20px;color:var(--ink);margin-bottom:12px}
.cmp-list{display:grid;gap:12px}
@media(min-width:760px){.cmp-list{grid-template-columns:repeat(3,1fr)}}
.cmp-card{position:relative;border:1px solid var(--line);border-radius:18px;padding:16px;display:flex;flex-direction:column;gap:12px}
.cmp-card.best{border:2px solid var(--green);box-shadow:var(--shadow)}
.cmp-badge{position:absolute;top:-11px;left:14px;font-size:12px;font-weight:800;background:var(--green);color:#fff;border-radius:999px;padding:3px 10px}
[dir="rtl"] .cmp-badge{left:auto;right:14px}
.cmp-head{display:flex;gap:12px;align-items:center}
.cmp-head b{display:block;font-size:17px}
.cmp-head span{font-size:13.5px;color:var(--muted)}
.cmp-card .tactions{display:flex;gap:8px}
.cmp-card .tactions a{flex:1;text-align:center;text-decoration:none;font-weight:700;font-size:14px;border-radius:12px;padding:11px 8px}
.cmp-card .tgo{background:var(--green);color:#fff}
.cmp-card .tmore{border:1px solid var(--line);color:var(--ink)}
.cmp-note{font-size:13px;color:var(--muted);margin-top:14px}
.cmp-note a{color:var(--green-ink);font-weight:700}

/* ---------- MATCHS ---------- */
.mgrid{display:grid;gap:12px;margin-top:8px}
@media(min-width:760px){.mgrid{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1000px){.hsec .mgrid{grid-template-columns:repeat(3,1fr)}}
.mcard{position:relative;display:block;text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;transition:border-color .15s,box-shadow .15s}
a.mcard:hover{border-color:var(--ink);box-shadow:var(--shadow)}
.mcard.big{margin-top:18px;max-width:560px;box-shadow:var(--shadow-lg);padding:22px}
.mmeta{font-size:13px;color:var(--muted);font-weight:600}
.mteams{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:8px 0 12px;font-family:var(--display);font-size:22px;color:var(--ink)}
.mcard.big .mteams{font-size:28px}
.mteams span{font-family:var(--sans);font-size:13px;font-weight:700;color:var(--muted)}
.mpick{display:flex;align-items:center;justify-content:space-between;gap:10px;background:var(--green-soft);border:1px dashed var(--green);border-radius:12px;padding:10px 14px;font-weight:700;color:var(--ink)}
.mpick b{font-family:var(--display);font-size:20px;color:var(--green-ink)}
.mstatus{position:absolute;top:16px;right:16px;font-size:12px;font-weight:800;border-radius:999px;padding:3px 10px}
[dir="rtl"] .mstatus{right:auto;left:16px}
.mstatus.soon{background:var(--soft);color:var(--muted)}
.mstatus.win{background:#e7f8ee;color:#0f7a3d}
.mstatus.lose{background:#fdecec;color:#b42318}
.mstatus.void{background:#fff4e5;color:#9a5b00}
button.cta{font:inherit;font-weight:700;cursor:pointer}

/* ---------- PAGE VIP ---------- */
.vhero{padding:56px 0 44px;background:radial-gradient(900px 420px at 90% -10%,rgba(37,99,235,.35),transparent 60%),var(--ink);color:#fff}
.vhero .eyebrow{color:#93c5fd}
.vhero .eyebrow::before{background:#93c5fd}
.vhero h1{color:#fff;font-size:clamp(38px,7vw,72px);line-height:1.02;letter-spacing:-.035em;max-width:860px}
.vhero h1 em{font-style:normal;color:#93c5fd}
.vhero .lead{color:#c9d1cc;font-size:clamp(17px,2.2vw,20px);max-width:640px;margin-top:18px}
.vhero .btnrow{justify-content:flex-start;margin-top:26px}
.vhero .cta.alt{background:transparent;color:#fff;border-color:rgba(255,255,255,.25)}
.vhero .cta.alt:hover{border-color:#fff}
.vperday{margin-top:14px;color:#c9d1cc;font-size:15px}
.vperday b{color:#fff}
.vhero .home-trust{color:#9aa5a0}
.vhero .home-trust b{color:#fff}
.vcmp th:nth-child(2),.vcmp th:nth-child(3),.vcmp td:nth-child(2),.vcmp td:nth-child(3){text-align:center;width:22%}
.vcmp td:last-child{color:var(--green-ink);font-weight:800;background:var(--green-soft)}
.vcmp th:last-child{color:var(--green-ink);background:var(--green-soft)}
.vcmp td.no{color:#a3aba7}
.vsteps{display:grid;gap:12px;margin-top:6px}
.vstep{display:flex;gap:14px;align-items:flex-start;background:var(--soft);border-radius:16px;padding:18px}
.vstep .fi{width:42px;height:42px;flex:0 0 auto;border-radius:12px;background:#fff;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-size:20px}
.vstep b{display:block;font-size:17px;margin-bottom:2px}
.vstep p{font-size:15px}
.vprice{max-width:460px;margin:8px auto 0;text-align:center;background:#fff;border:2px solid var(--green);border-radius:24px;padding:28px 24px;box-shadow:var(--shadow-lg)}
.vamount{font-family:var(--display);font-weight:800;font-size:64px;line-height:1;margin:8px 0 4px;letter-spacing:-.03em}
.vsmall{color:var(--muted);font-size:14px}
.vprice ul{list-style:none;padding:0;margin:20px 0;text-align:left;display:grid;gap:8px}
[dir="rtl"] .vprice ul{text-align:right}
.vprice li{position:relative;padding-left:30px;margin:0;color:var(--ink2)}
.vprice li::before{content:"✓";position:absolute;left:0;top:2px;width:20px;height:20px;border-radius:50%;background:var(--green-soft);color:var(--green-ink);font-weight:800;font-size:12px;display:flex;align-items:center;justify-content:center}
[dir="rtl"] .vprice li{padding-left:0;padding-right:30px}
[dir="rtl"] .vprice li::before{left:auto;right:0}
.vprice .cta{width:100%}
.vcryptos{display:grid;gap:12px}
@media(min-width:760px){.vcryptos{grid-template-columns:repeat(2,1fr)}}
.vcrypto{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;text-align:center}
.vcrypto.reco{border:2px solid var(--green);box-shadow:var(--shadow)}
.vc-head{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:6px 8px}
.vc-head b{font-size:19px}
.vc-head span{font-size:13px;color:var(--muted)}
.vc-head .vbadge{font-size:11.5px;font-weight:800;background:var(--green);color:#fff;border-radius:999px;padding:3px 10px}
.vvol{font-size:12.5px;color:#9a5b00;margin-top:6px}
.vcrypto img{display:block;width:164px;height:164px;margin:12px auto;border:1px solid var(--line);border-radius:12px;padding:6px;background:#fff}
.vaddr{word-break:break-all;font-weight:700;font-size:12.5px;background:var(--soft);border-radius:10px;padding:10px;color:var(--ink)}
.vcopy{font:inherit;font-weight:700;font-size:14px;cursor:pointer;border:none;border-radius:12px;padding:11px 18px;margin-top:10px;background:var(--ink);color:#fff;width:100%}
.vwarn{margin-top:10px;font-size:12.5px;color:#9b1c1c;background:rgba(229,50,45,.07);border-radius:10px;padding:9px}
.vproof{text-align:center;margin-top:24px}
.vproof .cta{background:#229ed9;border-color:#229ed9;font-size:17px;padding:16px 26px}
.vproof p{max-width:460px;margin:12px auto 0;color:var(--muted);font-size:14px}

.vpay-h{font-size:22px;margin-top:22px}
.vmomos{display:grid;gap:12px}
@media(min-width:760px){.vmomos{grid-template-columns:repeat(2,1fr)}}
.vmomo{background:#fff;border:2px solid var(--green);border-radius:18px;padding:18px;box-shadow:var(--shadow)}
.vm-head{display:flex;align-items:center;gap:10px}
.vm-head b{font-size:18px}
.vm-logo{width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;color:#0a0d0b}
.vm-num{font-family:var(--display);font-weight:800;font-size:28px;letter-spacing:.02em;margin:14px 0 10px;direction:ltr;unicode-bidi:embed}
[dir="rtl"] .vm-num{text-align:right}
.vm-row{display:flex;justify-content:space-between;gap:10px;font-size:14.5px;padding:8px 0;border-top:1px solid var(--line)}
.vm-row span{color:var(--muted)}
.vmomo .vcopy{margin-top:12px}
.vwarn{color:#9b1c1c}
p.vwarn[style]{background:var(--green-soft);color:var(--green-ink);font-weight:600}
/* ---------- BARRE D'ONGLETS MOBILE ---------- */
.topffn{display:flex;align-items:center;height:44px;padding:0 12px;border-radius:12px;border:1.5px dashed var(--green);background:var(--green-soft);color:var(--ink);font:inherit;font-family:var(--display);font-weight:800;font-size:15px;letter-spacing:.04em;cursor:pointer;white-space:nowrap}
.topffn:active{transform:scale(.96)}
@media(min-width:960px){.topffn{display:none}}
.toptg{display:flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:12px;background:#229ed9}
.tabbar{position:fixed;left:0;right:0;bottom:0;z-index:70;display:grid;grid-template-columns:repeat(5,1fr);align-items:end;background:rgba(255,255,255,.96);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-top:1px solid var(--line);padding:6px 4px calc(6px + env(safe-area-inset-bottom,0px))}
.tabbar a{display:flex;flex-direction:column;align-items:center;gap:2px;text-decoration:none;font-size:11.5px;font-weight:600;color:var(--muted);padding:4px 0}
.tabbar a .ti{font-size:20px;line-height:1;filter:grayscale(1);opacity:.75}
.tabbar a.on{color:var(--green-ink)}
.tabbar a.on .ti{filter:none;opacity:1}
.tabbar .tb-vip{color:var(--ink)}
.tb-ffn{justify-self:center;margin-top:-26px;width:64px;height:64px;border-radius:50%;border:4px solid #fff;background:var(--green);color:#fff;font:inherit;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(37,99,235,.35);transition:background .15s,transform .1s}
.tb-ffn b{font-family:var(--display);font-size:16px;letter-spacing:.06em;line-height:1}
.tb-ffn small{font-size:10px;font-weight:600;opacity:.9}
.tb-ffn:active{transform:scale(.95)}
.tb-ffn.ok{background:#0f7a3d}
body.has-sticky .tabbar{display:none}
@media(min-width:960px){.tabbar,.toptg{display:none}}

/* ---------- LISTE REPLIABLE ---------- */
.bklist.folded .bkrow:nth-child(n+6){display:none}
.bkmore{display:block;width:100%;margin-top:10px;font:inherit;font-weight:700;font-size:15px;cursor:pointer;background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px;color:var(--ink)}
.bkmore:hover{border-color:var(--ink)}
.vmodes{display:grid;gap:12px;margin-top:6px}
@media(min-width:760px){.vmodes{grid-template-columns:repeat(2,1fr)}}
.vmode{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;display:flex;flex-direction:column;gap:10px}
.vmode-h{display:flex;gap:12px;align-items:center}
.vmode-h .fi{width:44px;height:44px;flex:0 0 auto;border-radius:12px;background:var(--soft);display:flex;align-items:center;justify-content:center;font-size:22px}
.vmode-h b{display:block;font-size:18px;color:var(--ink)}
.vmode-h small{font-size:13px;color:var(--green-ink);font-weight:700}
.vmode p{font-size:15px}
.vrisk{align-self:flex-start;font-size:12px;font-weight:700;color:var(--muted);background:var(--soft);border-radius:999px;padding:4px 10px}
.vproof-period{font-weight:700;color:var(--green-ink);background:var(--green-soft);border-radius:12px;padding:10px 14px;margin:4px 0 16px;font-size:15px}
.vproofs{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;align-items:start}
.vproof-card{margin:0;background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:var(--shadow)}
.vproof-card img{display:block;width:100%;height:auto}
.vproof-card figcaption{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;padding:10px 14px;border-top:1px solid var(--line);font-size:14px}
.vproof-card figcaption span{flex:1 1 auto;font-weight:600;color:var(--ink)}
.vproof-card figcaption b{font-family:var(--display);font-size:18px;color:var(--green-ink)}
.vproof-card figcaption em{font-style:normal;font-size:11px;font-weight:800;color:#fff;background:var(--red);border-radius:6px;padding:2px 7px}
.vproof-card figcaption strong{flex-basis:100%;color:#0f7a3d;font-size:15px}
.vplans{display:grid;gap:12px;margin-top:8px}
@media(min-width:760px){.vplans{grid-template-columns:repeat(3,1fr);align-items:stretch}}
.vplan{position:relative;background:#fff;border:1px solid var(--line);border-radius:20px;padding:22px 18px 18px;text-align:center;display:flex;flex-direction:column}
.vplan.best{border:2px solid var(--green);box-shadow:var(--shadow-lg)}
@media(max-width:759px){.vplan.best{order:-1;margin-top:10px}}
.vbest{position:absolute;top:-12px;left:50%;transform:translateX(-50%);white-space:nowrap;font-size:12px;font-weight:800;background:var(--green);color:#fff;border-radius:999px;padding:4px 12px}
.vp-name{font-weight:800;color:var(--ink);font-size:16px}
.vp-price{font-family:var(--display);font-weight:800;font-size:34px;line-height:1.05;letter-spacing:-.03em;margin:6px 0 2px;color:var(--ink)}
.vp-xaf{font-weight:700;color:var(--ink2);font-size:15px}
.vp-pm{color:var(--muted);font-size:13.5px;margin-top:2px}
.vp-save{color:#0f7a3d;font-weight:800;font-size:13.5px;margin:8px 0 14px}
.vplan .cta{margin-top:auto;width:100%}
.vincluded{max-width:560px;margin:22px auto 0;background:var(--soft);border-radius:18px;padding:18px 20px}
.vincluded ul{list-style:none;padding:0;margin:10px 0 0;display:grid;gap:8px}
.vincluded li{position:relative;padding-left:28px;margin:0;color:var(--ink2)}
.vincluded li::before{content:"✓";position:absolute;left:0;top:1px;width:20px;height:20px;border-radius:50%;background:#fff;color:var(--green-ink);font-weight:800;font-size:12px;display:flex;align-items:center;justify-content:center}
[dir="rtl"] .vincluded li{padding-left:0;padding-right:28px}
[dir="rtl"] .vincluded li::before{left:auto;right:0}
/* ---------- RTL ---------- */
[dir="rtl"] body{font-family:"IBM Plex Sans Arabic","Inter",sans-serif}
[dir="rtl"] h1,[dir="rtl"] h2,[dir="rtl"] h3{font-family:"IBM Plex Sans Arabic",var(--display);letter-spacing:0}
[dir="rtl"] th{text-align:right}
[dir="rtl"] .code,[dir="rtl"] .bk,[dir="rtl"] .hero h1 .hl,[dir="rtl"] .tcode span,[dir="rtl"] .bkcode,[dir="rtl"] .sb-code{direction:ltr;unicode-bidi:embed}

/* ---------- PETITS ECRANS ---------- */
@media(max-width:640px){
  .hero{padding:36px 0 32px}
  .hero .sub{font-size:16.5px}
  .codebox{padding:22px 16px 18px}
  .btnrow .cta{flex:1 1 100%}
  .ytbar{margin:12px 12px 0}
  .ytthumb,.ytthumb img{width:88px}
  .ytthumb img{height:52px}
  .hsec{padding:48px 0}
  .home-trust{gap:10px 18px;font-size:12.5px}
  .home-trust b{font-size:22px}
  .tgband{border-radius:22px;margin:48px 16px 0}
}
"""

def _lang_items(current, fr=None, en=None, es=None, ar=None):
    out = ""
    if current != "fr" and fr: out += f'<li><a href="{fr}" class="langlink">FR</a></li>'
    if current != "en" and en: out += f'<li><a href="{en}" class="langlink">EN</a></li>'
    if current != "es" and es: out += f'<li><a href="{es}" class="langlink">ES</a></li>'
    if current != "ar" and ar: out += f'<li><a href="{ar}" class="langlink">AR</a></li>'
    return out

BURGER_SCRIPT = """<script>(function(){
  var b=document.querySelector('.burger'), p=document.querySelector('.navpanel'), ov=document.querySelector('.navmask');
  if(!b||!p)return;
  var focusables=function(){return p.querySelectorAll('a,button');};
  function open(){
    p.classList.add('open');ov.classList.add('open');b.setAttribute('aria-expanded','true');document.body.style.overflow='hidden';
    var f=focusables();if(f.length)f[0].focus();
    document.addEventListener('keydown',onKey);
  }
  function close(){
    p.classList.remove('open');ov.classList.remove('open');b.setAttribute('aria-expanded','false');document.body.style.overflow='';
    document.removeEventListener('keydown',onKey);
    b.focus();
  }
  function onKey(e){
    if(e.key==='Escape'){close();return;}
    if(e.key==='Tab'){
      var f=focusables();if(!f.length)return;
      var first=f[0],last=f[f.length-1];
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
    }
  }
  b.addEventListener('click',function(){p.classList.contains('open')?close():open();});
  ov.addEventListener('click',close);
  p.querySelectorAll('a').forEach(function(a){a.addEventListener('click',close);});
  var p2=location.pathname, h=location.hash, key='';
  if(h==='#bookmakers'){key='codes';}
  else if(/vip/i.test(p2)){key='vip';}
  else if(p2.indexOf('cote-de-2.html')>-1||p2.indexOf('odds-of-2.html')>-1||p2.indexOf('cuota-de-2.html')>-1||p2.indexOf('cote-2-ar.html')>-1){key='cote2';}
  else if(p2.indexOf('total-pair-impair.html')>-1||p2.indexOf('total-odd-even.html')>-1||p2.indexOf('total-par-impar.html')>-1||p2.indexOf('total-pair-impair-ar.html')>-1){key='tpi';}
  else if(p2.indexOf('resultats.html')>-1||p2.indexOf('results.html')>-1||p2.indexOf('resultados.html')>-1||p2.indexOf('resultats-ar.html')>-1){key='resultats';}
  else if(p2.indexOf('index.html')>-1||p2.indexOf('promo-codes.html')>-1||p2.indexOf('codigos-promocionales.html')>-1||p2.indexOf('promo-codes-ar.html')>-1||p2==='/'||p2===''){key='accueil';}
  if(key){var el=p.querySelector('a[data-key="'+key+'"]');if(el)el.classList.add('active');}
})();</script>"""

NAV_L = {
  "fr": {"title":"Menu","items":[("accueil","\U0001F3E0","Accueil","index.html"),("codes","\U0001F39F\uFE0F","Codes promo","index.html#bookmakers"),
         ("analyses","\U0001F4CA","Analyses des matchs","pronostics.html"),("cote2","\u26BD","Côte de 2","cote-de-2.html"),("tpi","\U0001F3B2","Total Pair/Impair","total-pair-impair.html"),
         ("compare","\U0001F9ED","Quel bookmaker choisir ?","quel-bookmaker-choisir.html"),("aide","❓","Code qui ne marche pas","code-promo-ne-marche-pas.html"),
         ("resultats","\U0001F3C6","Résultats","resultats.html"),
         ("vip","\u2B50","VIP","vip.html")]},
  "en": {"title":"Menu","items":[("accueil","\U0001F3E0","Home","promo-codes.html"),("codes","\U0001F39F\uFE0F","Promo codes","promo-codes.html#bookmakers"),
         ("analyses","\U0001F4CA","Match predictions","predictions.html"),("cote2","\u26BD","Odds of 2","odds-of-2.html"),("tpi","\U0001F3B2","Total Odd/Even","total-odd-even.html"),
         ("resultats","\U0001F3C6","Results","results.html"),("vip","\u2B50","VIP","vip-en.html")]},
  "es": {"title":"Menú","items":[("accueil","\U0001F3E0","Inicio","codigos-promocionales.html"),("codes","\U0001F39F\uFE0F","Códigos promo","codigos-promocionales.html#bookmakers"),
         ("analyses","\U0001F4CA","Pronósticos de partidos","pronosticos.html"),("cote2","\u26BD","Cuota de 2","cuota-de-2.html"),("tpi","\U0001F3B2","Total Par/Impar","total-par-impar.html"),
         ("resultats","\U0001F3C6","Resultados","resultados.html"),("vip","\u2B50","VIP","vip-es.html")]},
  "ar": {"title":"القائمة","items":[("accueil","\U0001F3E0","الرئيسية","promo-codes-ar.html"),("codes","\U0001F39F\uFE0F","الرموز الترويجية","promo-codes-ar.html#bookmakers"),
         ("analyses","\U0001F4CA","توقعات المباريات","pronostics-ar.html"),("cote2","\u26BD","رهان بضعف 2","cote-2-ar.html"),("tpi","\U0001F3B2","زوجي/فردي","total-pair-impair-ar.html"),
         ("resultats","\U0001F3C6","النتائج","resultats-ar.html"),("vip","\u2B50","VIP","vip-ar.html")]},
}

def burger_html():
    return '<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>'

def navpanel_html(lang="fr", lang_links=""):
    d = NAV_L.get(lang, NAV_L["fr"])
    items = "".join(f'<a href="{href}" data-key="{key}"><span class="ic">{ic}</span>{label}</a>' for key,ic,label,href in d["items"])
    return (f'<div class="navmask"></div>\n<nav class="navpanel">\n'
            f'<div class="navpanel-head"><span>{d["title"]}</span></div>\n'
            f'<div class="navpanel-links">{items}</div>\n'
            f'<div class="navpanel-lang">{lang_links}</div>\n'
            f'</nav>{BURGER_SCRIPT}')

VIP_SLUG = {"fr":"vip.html","en":"vip-en.html","es":"vip-es.html","ar":"vip-ar.html"}
TOPLINKS_L = {
  "fr": [("Codes promo","index.html#bookmakers"),("Analyses","pronostics.html"),("Côte de 2","cote-de-2.html"),("Pair/Impair","total-pair-impair.html"),("Résultats","resultats.html")],
  "en": [("Promo codes","promo-codes.html#bookmakers"),("Predictions","predictions.html"),("Odds of 2","odds-of-2.html"),("Odd/Even","total-odd-even.html"),("Results","results.html")],
  "es": [("Códigos","codigos-promocionales.html#bookmakers"),("Pronósticos","pronosticos.html"),("Cuota de 2","cuota-de-2.html"),("Par/Impar","total-par-impar.html"),("Resultados","resultados.html")],
  "ar": [("الرموز","promo-codes-ar.html#bookmakers"),("التوقعات","pronostics-ar.html"),("رهان بضعف 2","cote-2-ar.html"),("زوجي/فردي","total-pair-impair-ar.html"),("النتائج","resultats-ar.html")],
}
HOME_L = {"fr":"index.html","en":"promo-codes.html","es":"codigos-promocionales.html","ar":"promo-codes-ar.html"}

TABBAR_L = {
  "fr": ("Accueil", "Codes", "Copier", "Coupon", "VIP", "Copié !", "cote-de-2.html"),
  "en": ("Home", "Codes", "Copy", "Coupon", "VIP", "Copied!", "odds-of-2.html"),
  "es": ("Inicio", "Códigos", "Copiar", "Cupón", "VIP", "¡Copiado!", "cuota-de-2.html"),
  "ar": ("الرئيسية", "الرموز", "نسخ", "القسيمة", "VIP", "تم النسخ", "cote-2-ar.html"),
}
TABBAR_SCRIPT = """<script>(function(){var t=document.querySelector('.tabbar');if(!t)return;var p=location.pathname.split('/').pop()||'index.html';
t.querySelectorAll('a[data-p]').forEach(function(a){if(a.getAttribute('data-p')===p&&!location.hash)a.classList.add('on');});
var b=t.querySelector('.tb-ffn');b.addEventListener('click',function(){var l=b.querySelector('small'),o=l.textContent;
try{navigator.clipboard.writeText('FFN');}catch(e){}l.textContent=b.getAttribute('data-ok');b.classList.add('ok');
if(typeof gtag==='function')gtag('event','copy_promo_code',{page_path:location.pathname,source:'tabbar'});
setTimeout(function(){l.textContent=o;b.classList.remove('ok');},1600);});})();</script>"""

def tabbar_html(lang):
    home, codes, copy, coupon, vip, ok, cslug = TABBAR_L[lang]
    h = HOME_L[lang]
    return (f'<nav class="tabbar" aria-label="Navigation rapide">'
            f'<a href="{h}" data-p="{h}"><span class="ti">🏠</span>{home}</a>'
            f'<a href="{h}#bookmakers"><span class="ti">🎟️</span>{codes}</a>'
            f'<button type="button" class="tb-ffn" data-ok="{ok}" aria-label="{copy} FFN"><b translate="no">FFN</b><small>{copy}</small></button>'
            f'<a href="{cslug}" data-p="{cslug}"><span class="ti">⚽</span>{coupon}</a>'
            f'<a href="{VIP_SLUG[lang]}" data-p="{VIP_SLUG[lang]}" class="tb-vip"><span class="ti">⭐</span>{vip}</a>'
            f'</nav>' + TABBAR_SCRIPT)

TICKER_L = {
 "fr": [("🔥 Coupon côte de 2 du jour", "cote-de-2.html"), ("⚽ Pronostics des grands matchs", "pronostics.html"),
        ("🎁 Code promo FFN : bonus jusqu'à 100 %", "#bookmakers"), ("⭐ VIP 25 000 FCFA / mois", VIP_SLUG["fr"]),
        ("✅ Mes tickets gagnants", VIP_SLUG["fr"] + "#preuves"), ("📲 Rejoins le canal Telegram", "https://t.me/marc_prono")],
 "en": [("🔥 Daily 2-odds coupon", HOME_L["en"]), ("🎁 Promo code FFN: bonus up to 100%", HOME_L["en"]),
        ("⭐ VIP from $30 / month", VIP_SLUG["en"]), ("✅ My winning tickets", VIP_SLUG["en"] + "#preuves"),
        ("📲 Join the Telegram channel", "https://t.me/marc_prono")],
 "es": [("🔥 Cupón de cuota 2 del día", HOME_L["es"]), ("🎁 Código promocional FFN: bono hasta 100 %", HOME_L["es"]),
        ("⭐ VIP 25 000 FCFA / mes", VIP_SLUG["es"]), ("✅ Mis boletos ganadores", VIP_SLUG["es"] + "#preuves"),
        ("📲 Únete al canal de Telegram", "https://t.me/marc_prono")],
 "ar": [("🔥 كوبون الأودز 2 اليومي", HOME_L["ar"]), ("🎁 كود البروموشن FFN: بونص حتى 100%", HOME_L["ar"]),
        ("⭐ VIP بـ 25 000 فرنك شهرياً", VIP_SLUG["ar"]), ("✅ تذاكري الرابحة", VIP_SLUG["ar"] + "#preuves"),
        ("📲 انضم إلى قناة تيليجرام", "https://t.me/marc_prono")],
}

TICKER_ON = False   # bandeau defilant en haut (desactive a la demande de Marc)

# Mes coupons joues (photos dans site/), affiches sur l'accueil et la page Pronostics
# (fichier, titre, cote, code coupon WinWin ou "", matchs)
COUPONS_LDC = [
 ("coupon-ldc-20oct-10-39.jpg", "Combiné Ligue des champions · mardi 20 oct.", "10.39", "", "Fenerbahçe – Slavia · Liverpool – Villarreal · Naples – Bodø · Porto – PSV · Stuttgart – Atlético"),
 ("coupon-ldc-21oct-17-01.jpg", "Combiné Ligue des champions · mercredi 21 oct.", "17.01", "", "Como – Man United · Lille – Galatasaray · Aston Villa – Viking · Bayern – Arsenal"),
]

def coupons_ldc_html():
    if not COUPONS_LDC: return ""
    cards = ""
    for f, t, c, code, m in COUPONS_LDC:
        if not os.path.exists(os.path.join(OUT, f)): continue
        cp = (f'<div class="tcode" style="margin-top:8px"><span translate="no">{code}</span>'
              f'<button class="copybtn-mini" onclick="copyCode(this,\'{code}\')">📋 Copier le code coupon</button></div>') if code else ""
        cards += (f'<figure class="vproof-card"><img src="{f}" alt="{html.escape(t)} cote {c} — Cousin Marc" loading="lazy">'
                  f'<figcaption><span>{html.escape(t)}</span><b>@{c}</b><strong style="color:var(--ink2);font-weight:600;font-size:13px">{html.escape(m)}</strong>{cp}</figcaption></figure>')
    return f'<div class="vproofs">{cards}</div>' if cards else ""

def ticker_html(lang):
    if not TICKER_ON: return ""
    ext = lambda h: ' target="_blank" rel="nofollow"' if h.startswith("http") else ""
    one = "".join(f'<a href="{h}"{ext(h)}>{t}</a>' for t, h in TICKER_L[lang])
    return f'<div class="ticker" aria-label="Infos"><div class="ticker-track">{one}{one}</div></div>'

def topnav(lang, langs_html, top_langs):
    links = "".join(f'<li><a href="{h}">{t}</a></li>' for t,h in TOPLINKS_L[lang])
    links += f'<li><a class="vip" href="{VIP_SLUG[lang]}">VIP</a></li>'
    return (ticker_html(lang) + f'<nav class="top"><div class="wrap">'
            f'<a class="logo" href="{HOME_L[lang]}" translate="no"><span class="dot"></span>cousin<b>marc</b></a>'
            f'<div class="navright"><ul class="toplinks">{links}</ul><ul class="toplang">{top_langs}</ul>'
            f'<button type="button" class="topffn" onclick="copyCode(this,\'FFN\')" aria-label="Copier le code promo FFN">FFN 📋</button>'
            f'<a class="toptg" href="https://t.me/marc_prono" target="_blank" rel="nofollow" aria-label="Telegram Cousin Marc"><svg width="22" height="22" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71l-4.14-3.05-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg></a>{burger_html()}</div>'
            f'</div></nav>\n{navpanel_html(lang, langs_html)}')

def _top_langs(current, **kw):
    return "".join(f'<li><a href="{kw[k]}" hreflang="{k}">{k.upper()}</a></li>' for k in ("fr","en","es","ar") if k != current and kw.get(k))

def nav_fr(en="promo-codes.html", es=None, ar="promo-codes-ar.html"):
    return topnav("fr", f'<ul class="langrow">{_lang_items("fr", en=en, es=es, ar=ar)}</ul>', _top_langs("fr", en=en, es=es, ar=ar))

def nav_en(fr="index.html", es=None, ar="promo-codes-ar.html"):
    return topnav("en", f'<ul class="langrow">{_lang_items("en", fr=fr, es=es, ar=ar)}</ul>', _top_langs("en", fr=fr, es=es, ar=ar))

def nav_es(fr="index.html", en="promo-codes.html", ar="promo-codes-ar.html"):
    return topnav("es", f'<ul class="langrow">{_lang_items("es", fr=fr, en=en, ar=ar)}</ul>', _top_langs("es", fr=fr, en=en, ar=ar))

def nav_ar(fr="index.html", en="promo-codes.html", es="codigos-promocionales.html"):
    return topnav("ar", f'<ul class="langrow">{_lang_items("ar", fr=fr, en=en, es=es)}</ul>', _top_langs("ar", fr=fr, en=en, es=es))

NAV = nav_fr(es="codigos-promocionales.html")

def social_html():
    return "\n".join(f'<a href="{u}" rel="nofollow">{ICONS.get(n,"")}<span>{n}</span></a>' for n,u in SOCIAL)

def footer_html():
    return f"""<footer><div class="wrap">
<div class="cols">
<div>
<h4>Navigation</h4>
<a href="index.html">Codes promo</a>
<a href="cote-de-2.html">Côte de 2</a>
<a href="pronostics.html">Pronostics</a>
<a href="resultats.html">Résultats</a>
<a href="actualites.html">Actualités</a>
<a href="a-propos.html">À propos</a>
</div>
<div>
<h4>Bookmakers</h4>
{''.join(f'<a href="{b["slug"]}.html">{b["name"]}</a>' for b in BOOKMAKERS[:4])}
</div>
<div>
<h4>Infos</h4>
<a href="comment-sinscrire-1xbet-2026.html">Comment s'inscrire</a>
<a href="deposer-retirer-paris-afrique.html">Comment retirer</a>
<a href="jeu-responsable.html">Jeu responsable</a>
<a href="quel-bookmaker-choisir.html">Quel bookmaker choisir ?</a>
<a href="code-promo-ne-marche-pas.html">Code promo qui ne marche pas</a>
</div>
<div>
<h4>Pays</h4>
{country_links_footer()}
</div>
<div>
<h4>Réseaux</h4>
<a href="https://t.me/marc_prono" rel="nofollow">Telegram</a>
<a href="https://youtube.com/@prossport" rel="nofollow">YouTube</a>
<a href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">WhatsApp</a>
</div>
</div>
<div class="warn">⚠️ Réservé aux 18 ans et +. Le jeu comporte des risques : endettement, dépendance, isolement. Jouez de manière responsable et ne misez que ce que vous pouvez vous permettre de perdre. <a href="jeu-responsable.html" style="color:var(--gold)">En savoir plus</a></div>
<p style="margin-top:18px">© 2026 Cousin Marc Pronostic · Code promo FFN · Pronostics foot Afrique</p>
</div></footer>
<script>function copyCode(btn,code){{navigator.clipboard.writeText(code).then(function(){{var t=btn.textContent;btn.textContent="✅ Copié !";setTimeout(function(){{btn.textContent=t;}},1500);}});}}</script>"""


def faq_jsonld(name, code, extra=()):
    qs = list(extra) + [
        (f"Quel est le code promo {name} en 2026 ?",
         f"Le code promo {name} valable en 2026 est {code}. Il s'utilise à l'inscription et débloque le bonus de bienvenue de {pct(name, 'fr', True)} sur le premier dépôt."),
        (f"Comment utiliser le code promo {name} {code} ?",
         f"Pendant l'inscription sur {name}, colle le code {code} dans le champ « Code promo ». Le bonus est crédité automatiquement après le premier dépôt."),
        (f"Le code promo {name} est-il gratuit ?",
         f"Oui, le code {code} est 100% gratuit. Il sert uniquement à activer le bonus de bienvenue."),
    ]
    data = {"@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qs]}
    return json.dumps(data, ensure_ascii=False, indent=2)

STICKY_L = {"fr":("📋 Copier","S'inscrire"),"en":("📋 Copy","Register"),"es":("📋 Copiar","Registrarse"),"ar":("📋 نسخ","التسجيل")}
STICKY_BAR_ON = False   # barre collante en bas d'ecran (desactivee : bas de l'ecran laisse libre)

def sticky_bar(b, lang="fr"):
    if not STICKY_BAR_ON:
        return ""
    cp, go = STICKY_L.get(lang, STICKY_L["fr"])
    return (f'<div class="stickybar"><span class="sb-code">{b["code"]}</span>'
            f'<button class="sb-copy" aria-label="Copier le code promo {b["code"]}" onclick="copyCode(this,\'{b["code"]}\')">{cp}</button>'
            f'<a class="sb-go" href="{b["site"]}" rel="sponsored nofollow">{go} {b["name"]}</a></div>'
            f'<script>document.body.classList.add("has-sticky")</script>')

FEAT_L = {"fr":("Recommande du moment","Voir le code"),"en":("Featured pick","See code"),
          "es":("Recomendado","Ver código"),"ar":("الأنسب لك الآن","عرض الرمز")}
def featured_html(lang):
    b = BOOKMAKERS[0]
    tag, cta = FEAT_L.get(lang, FEAT_L["fr"])
    bonus = BK_CONTENT.get(b["slug"],{}).get("bonus",{}).get(lang, b["bonus_max"])
    if lang == "en": slug = en_slug(b)
    elif lang == "es": slug = es_slug(b)
    elif lang == "ar": slug = ar_slug(b)
    else: slug = b["slug"]
    return (f'<a class="featured" href="{slug}.html">'
            f'<div class="flogo" style="background:{BRAND[b["slug"]]}">{b["name"][:2].upper()}</div>'
            f'<div class="finfo"><div class="ftag">⭐ {tag}</div>'
            f'<div class="fname" translate="no">{b["name"]}</div>'
            f'<div class="fbonus">{bonus} · {b["code"]}</div></div>'
            f'<span class="fgo">{cta}</span></a>')

def buttons(b):
    out = f'<a class="cta" href="{b["site"]}" rel="sponsored nofollow">🌐 S\'inscrire sur le site</a>'
    for label, url in b["apps"]:
        icon = "🤖" if label in ("Android","Application") else "🍏"
        out += f'<a class="cta alt" href="{url}" rel="sponsored nofollow">{icon} {label}</a>'
    return out

def reg_block(b):
    if b["reg_code"]:
        return f'<div class="reg">Code d\'inscription : <b>{b["reg_code"]}</b></div>'
    return ""

def country_rows(b):
    return "\n".join(f'<tr><td>{html.escape(c)}</td><td>{html.escape(v)}</td><td>{b["code"]}</td></tr>' for c,v in b["countries"])

def related_block(current):
    cards=""
    for b in BOOKMAKERS:
        if b["slug"]==current: continue
        cards += f'<a href="{b["slug"]}.html" style="border-left:3px solid {BRAND[b["slug"]]}"><div class="bk" translate="no">{bk_logo(b, "rlogo", 28)}{b["name"]}</div><div class="cd">Code : {b["code"]}</div></a>\n'
    return cards


# ===== BANDEAU VIDEO YOUTUBE (haut de toutes les pages) =====
YT_VID = "Z-vnaLR3jYM"
YT_CHAN = "https://youtube.com/@prossport"
YT_L = {
 "fr": ("Regarde le tuto en vidéo", "S'abonner à la chaîne"),
 "en": ("Watch the video tutorial", "Subscribe to the channel"),
 "es": ("Mira el tutorial en vídeo", "Suscríbete al canal"),
 "ar": ("شاهد الشرح بالفيديو", "اشترك في القناة"),
}
VIDEO_L = {
 "fr": ("Commence ici", "Regarde la vidéo avant de t'inscrire", "Je t'explique pas à pas comment créer ton compte, entrer le code promo et faire ton premier dépôt.", "S'abonner à la chaîne", "Lire la vidéo"),
 "en": ("Start here", "Watch the video before you sign up", "Step by step: how to create your account, enter the promo code and make your first deposit.", "Subscribe to the channel", "Play video"),
 "es": ("Empieza aquí", "Mira el vídeo antes de registrarte", "Paso a paso: cómo crear tu cuenta, poner el código promocional y hacer tu primer depósito.", "Suscríbete al canal", "Reproducir vídeo"),
 "ar": ("ابدأ من هنا", "شاهد الفيديو قبل التسجيل", "خطوة بخطوة: كيف تنشئ حسابك وتدخل الرمز الترويجي وتقوم بأول إيداع.", "اشترك في القناة", "تشغيل الفيديو"),
}
def video_block(lang):
    kick, title, sub, subscribe, play = VIDEO_L.get(lang, VIDEO_L["fr"])
    return (f'<section class="vidhero" id="video"><div class="wrap vidgrid">'
      f'<div class="yt-facade" data-yt="{YT_VID}" data-yt-title="{title}" role="button" tabindex="0" aria-label="{play} : {title}">'
      f'<img src="https://i.ytimg.com/vi/{YT_VID}/hqdefault.jpg" alt="{title} — Cousin Marc" width="480" height="360" fetchpriority="high">'
      f'<span class="ytf-play" aria-hidden="true">▶</span></div>'
      f'<div class="vidtext"><p class="kicker">🎥 {kick}</p><h2>{title}</h2><p>{sub}</p>'
      f'<a class="ytsub" href="{YT_CHAN}" target="_blank" rel="nofollow">▶ {subscribe}</a></div>'
      f'</div></section>')

def youtube_banner(lang):
    title, sub = YT_L.get(lang, YT_L["fr"])
    css = ""
    return (f'{css}<div class="ytbar wrap">'
      f'<a class="ytthumb" href="https://youtu.be/{YT_VID}" target="_blank" rel="nofollow">'
      f'<img src="https://img.youtube.com/vi/{YT_VID}/hqdefault.jpg" alt="{title} - Cousin Marc" loading="lazy" width="132" height="78">'
      f'<span class="ytplay">▶</span></a>'
      f'<div class="ytinfo"><div class="yttitle">🎥 {title}</div>'
      f'<a class="ytsub" href="{YT_CHAN}" target="_blank" rel="nofollow">▶ {sub}</a></div>'
      f'</div>')


# ---------------------------------------------------------------- Animations entre les pages (decoratif)
# Le petit script choisit une animation au hasard au clic, et la page suivante la joue a l'ouverture.
# Navigateurs sans « View Transitions » : seules les bulles s'affichent, la page s'ouvre normalement.
VT_HEAD = """<script>(function(){try{var R=matchMedia('(prefers-reduced-motion: reduce)').matches;if(R)return;var d=document.documentElement,k='cmvt',v=JSON.parse(sessionStorage.getItem(k)||'null');if(v&&Date.now()-v.t<4000){d.setAttribute('data-vt',v.a);d.style.setProperty('--vx',v.x+'%');d.style.setProperty('--vy',v.y+'%');if(v.a==='bulles')addEventListener('DOMContentLoaded',function(){cmBubbles(16,null)});}sessionStorage.removeItem(k);
function mk(c,st){var e=document.createElement('i');e.className=c;e.setAttribute('aria-hidden','true');for(var p in st)e.style[p]=st[p];return e;}
window.cmBubbles=function(n,pt){var w=document.createElement('div');w.className='cm-bubbles';w.setAttribute('aria-hidden','true');for(var i=0;i<n;i++){var z=10+Math.random()*(pt?22:46);var b=mk('cm-b',{width:z+'px',height:z+'px'});if(pt){b.style.left=pt.x+'px';b.style.top=pt.y+'px';var a=Math.random()*6.283,r=40+Math.random()*90;b.style.setProperty('--dx',Math.cos(a)*r+'px');b.style.setProperty('--dy',Math.sin(a)*r+'px');b.classList.add('burst');}else{b.style.left=(Math.random()*100)+'vw';b.style.animationDelay=(Math.random()*.35)+'s';b.style.animationDuration=(.9+Math.random()*.7)+'s';b.style.setProperty('--sw',(Math.random()*40-20)+'px');}w.appendChild(b);}document.body.appendChild(w);setTimeout(function(){w.remove()},1900);};
addEventListener('click',function(e){var t=e.target.closest('a,button,.chip,.cta');if(!t||e.button||e.ctrlKey||e.metaKey||e.shiftKey)return;cmBubbles(10,{x:e.clientX,y:e.clientY});var h=t.getAttribute&&t.getAttribute('href');if(!h||h.charAt(0)==='#'||t.target==='_blank'||/^(mailto|tel|javascript):/.test(h))return;var u=new URL(h,location.href);if(u.origin!==location.origin)return;var A=['cercle','glisse','zoom','bulles'];sessionStorage.setItem(k,JSON.stringify({a:A[Math.floor(Math.random()*A.length)],x:Math.round(e.clientX/innerWidth*100),y:Math.round(e.clientY/innerHeight*100),t:Date.now()}));},true);var SQ='a.cta,.tgo,.tmore,.bkjoin,.copybtn-mini,.toptg,.topffn,.chip,.social a,.langlink,.navpanel-links a,button';addEventListener('pointerdown',function(e){var t=e.target.closest&&e.target.closest(SQ);if(!t)return;var r=document.createElement('i');r.className='cm-rip';r.setAttribute('aria-hidden','true');r.style.left=e.clientX+'px';r.style.top=e.clientY+'px';document.body.appendChild(r);setTimeout(function(){r.remove()},750);t.classList.remove('cm-sq');void t.offsetWidth;t.classList.add('cm-sq');setTimeout(function(){t.classList.remove('cm-sq')},520);if(navigator.vibrate&&e.pointerType==='touch')try{navigator.vibrate(8)}catch(_){}},{passive:true});addEventListener('DOMContentLoaded',function(){if(!('IntersectionObserver' in window))return;var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('cm-wet');io.unobserve(x.target);}})},{threshold:.12});document.querySelectorAll('.tcard,.mcard,.coupon-card,.vproof-card,.hubcard,.fact,.tgband,.bkrow').forEach(function(el){var b=el.getBoundingClientRect();if(b.top>innerHeight)io.observe(el);});});}catch(_){}})();</script>"""

CSS += r"""
/* ---------- Animations entre les pages (decoratif, desactive si « reduire les animations ») ---------- */
@view-transition{navigation:auto}
::view-transition-old(root),::view-transition-new(root){animation-duration:.5s;animation-timing-function:cubic-bezier(.2,.7,.2,1)}
html[data-vt="cercle"]::view-transition-old(root){animation:none}
html[data-vt="cercle"]::view-transition-new(root){animation:vt-cercle .6s cubic-bezier(.2,.7,.2,1) both}
@keyframes vt-cercle{from{clip-path:circle(0 at var(--vx,50%) var(--vy,50%))}to{clip-path:circle(150% at var(--vx,50%) var(--vy,50%))}}
html[data-vt="glisse"]::view-transition-old(root){animation:vt-out .35s ease both}
html[data-vt="glisse"]::view-transition-new(root){animation:vt-up .5s cubic-bezier(.2,.7,.2,1) both}
@keyframes vt-out{to{opacity:0;transform:translateY(-24px)}}
@keyframes vt-up{from{opacity:0;transform:translateY(40px)}}
html[data-vt="zoom"]::view-transition-old(root){animation:vt-zout .35s ease both}
html[data-vt="zoom"]::view-transition-new(root){animation:vt-zin .5s cubic-bezier(.2,.7,.2,1) both}
@keyframes vt-zout{to{opacity:0;transform:scale(1.04)}}
@keyframes vt-zin{from{opacity:0;transform:scale(.94)}}
html[data-vt="bulles"]::view-transition-old(root){animation:vt-fade .4s ease both}
html[data-vt="bulles"]::view-transition-new(root){animation:vt-fadein .5s ease both}
@keyframes vt-fade{to{opacity:0}}
@keyframes vt-fadein{from{opacity:0}}
/* bulles d'eau */
.cm-bubbles{position:fixed;inset:0;pointer-events:none;z-index:9999;overflow:hidden}
.cm-b{position:absolute;bottom:-70px;border-radius:50%;
  background:radial-gradient(circle at 30% 28%,rgba(255,255,255,.95) 0 10%,rgba(191,219,254,.55) 22%,rgba(59,130,246,.18) 58%,rgba(59,130,246,.05) 70%);
  border:1.5px solid rgba(147,197,253,.75);box-shadow:inset -3px -4px 8px rgba(29,78,216,.18),0 0 10px rgba(147,197,253,.35);
  animation:cm-rise 1.2s cubic-bezier(.3,.6,.4,1) forwards}
@keyframes cm-rise{0%{transform:translate(0,0) scale(.6);opacity:0}15%{opacity:1}50%{transform:translate(var(--sw,0),-55vh) scale(1)}100%{transform:translate(calc(var(--sw,0) * -1),-115vh) scale(1.1);opacity:0}}
.cm-b.burst{bottom:auto;margin:-8px 0 0 -8px;animation:cm-burst .65s cubic-bezier(.2,.8,.3,1) forwards}
@keyframes cm-burst{0%{transform:translate(0,0) scale(.3);opacity:.95}80%{opacity:.8}100%{transform:translate(var(--dx),var(--dy)) scale(1);opacity:0}}
@media(prefers-reduced-motion:reduce){@view-transition{navigation:none}.cm-bubbles{display:none}}
"""

def head(title, desc, canonical, extra="", nav=None, lang="fr", alternates=None, image=None, show_youtube=True):
    if nav is None: nav = NAV
    hreflang = ""
    if alternates:
        fr_url, en_url = alternates[0], alternates[1]
        es_url = alternates[2] if len(alternates) > 2 else None
        ar_url = alternates[3] if len(alternates) > 3 else None
        hreflang = f'<link rel="alternate" hreflang="fr" href="{fr_url}"><link rel="alternate" hreflang="en" href="{en_url}">'
        if es_url:
            hreflang += f'<link rel="alternate" hreflang="es" href="{es_url}">'
        if ar_url:
            hreflang += f'<link rel="alternate" hreflang="ar" href="{ar_url}">'
        hreflang += f'<link rel="alternate" hreflang="x-default" href="{fr_url}">'
    oglocale = {"fr":"fr_FR","en":"en_US","es":"es_ES","ar":"ar_AR"}.get(lang,"fr_FR")
    diratt = ' dir="rtl"' if lang=="ar" else ''
    ogimg = image if image else f"{BASE}/og-cousinmarc-v3.jpg"
    return f"""<!DOCTYPE html>
<html lang="{lang}"{diratt}><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><!-- Preload critical fonts for faster LCP --><link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap" /><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap" media="print" onload="this.media='all'" /><noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap" /></noscript>
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{hreflang}
<meta name="robots" content="index, follow">
<link rel="icon" href="favicon.ico?v=2" sizes="any"><link rel="icon" type="image/svg+xml" href="favicon.svg?v=2">
<link rel="icon" type="image/png" sizes="48x48" href="favicon-48.png?v=2"><link rel="icon" type="image/png" sizes="192x192" href="favicon-192.png?v=2">
<link rel="apple-touch-icon" href="apple-touch-icon.png?v=2"><meta name="theme-color" content="#ffffff"><link rel="manifest" href="manifest.json"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="Cousin Marc"><meta name="mobile-web-app-capable" content="yes">
<meta property="og:type" content="website"><meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}"><meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{oglocale}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ogimg}">
{extra}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-4LDDTEQ1GB"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-4LDDTEQ1GB');</script>
<script>document.addEventListener("click",function(e){{try{{
  var t=e.target.closest('a[rel*="sponsored"]');
  if(t&&typeof gtag==="function"){{gtag("event","affiliate_click",{{"link_url":t.href,"link_text":t.textContent.trim(),"page_path":location.pathname}});}}
  var c=e.target.closest(".copybtn,.copybtn-mini,.sb-copy");
  if(c&&typeof gtag==="function"){{gtag("event","copy_promo_code",{{"page_path":location.pathname}});}}
  var tg=e.target.closest("#cm-tg,a[href*='t.me/']");
  if(tg&&typeof gtag==="function"){{gtag("event","telegram_click",{{"page_path":location.pathname}});}}
  var wa=e.target.closest("a[href*='whatsapp.com']");
  if(wa&&typeof gtag==="function"){{gtag("event","whatsapp_click",{{"page_path":location.pathname}});}}
  var yt=e.target.closest(".yt-facade");
  if(yt){{
    var id=yt.getAttribute("data-yt"), ttl=yt.getAttribute("data-yt-title")||"";
    var ifr=document.createElement("iframe");
    ifr.src="https://www.youtube.com/embed/"+id+"?autoplay=1";
    ifr.title=ttl;ifr.loading="lazy";ifr.allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";ifr.allowFullscreen=true;
    ifr.style.position="absolute";ifr.style.inset="0";ifr.style.width="100%";ifr.style.height="100%";ifr.style.border="0";
    yt.innerHTML="";yt.appendChild(ifr);
    if(typeof gtag==="function")gtag("event","video_play",{{"video_id":id,"page_path":location.pathname}});
  }}
}}catch(err){{}}}});
document.addEventListener("keydown",function(e){{var f=e.target.closest&&e.target.closest(".yt-facade");if(f&&(e.key==="Enter"||e.key===" ")){{e.preventDefault();f.click();}}}});</script>
<link rel="stylesheet" href="style.css?v=2026-10t"><script>
document.addEventListener("DOMContentLoaded",function(){{
  try{{
    var b=Math.floor(Date.now()/600000); /* recharge les coupons toutes les 10 min */
    document.querySelectorAll("[data-gh]").forEach(function(e){{
      var u=e.getAttribute("data-gh")+"?t="+b;
      if(e.tagName==="IMG"){{ e.src=u; }}
      else if(e.tagName==="SOURCE"){{ e.src=u; var v=e.closest("video"); if(v){{ v.load(); }} }}
    }});
  }}catch(e){{}}
  try{{
    if(!document.getElementById("cm-tg")){{
      var t=document.createElement("a");
      t.id="cm-tg"; t.href="https://t.me/marc_prono"; t.target="_blank"; t.rel="nofollow";
      t.setAttribute("aria-label","Telegram Cousin Marc");
      t.innerHTML='<svg width="30" height="30" viewBox="0 0 24 24" fill="#fff"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71l-4.14-3.05-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg>';
      var sb=document.querySelector(".stickybar");
      if(window.innerWidth<960){{ /* mobile : Telegram est dans l'en-tete */ }}
      else if(sb&&window.innerWidth<900){{
        /* mobile avec barre du bas : le bouton Telegram s'integre a la barre (ne cache plus le contenu) */
        t.className="sb-tg"; t.querySelector("svg").setAttribute("width","24"); t.querySelector("svg").setAttribute("height","24");
        sb.appendChild(t);
      }} else {{
        var s=t.style;
        s.position="fixed"; s.bottom="18px"; s.width="56px"; s.height="56px";
        s.background="#229ED9"; s.borderRadius="50%"; s.display="flex";
        s.alignItems="center"; s.justifyContent="center";
        s.boxShadow="0 6px 18px rgba(0,0,0,.3)"; s.zIndex="80";
        if(document.documentElement.dir==="rtl"){{ s.left="18px"; }} else {{ s.right="18px"; }}
        document.body.appendChild(t);
      }}
    }}
  }}catch(e){{}}
}});
</script>{VT_HEAD}</head><body>{nav}{video_block(lang) if show_youtube else ""}"""


# ===== CONTENU ENRICHI (SEO) pour WinWin & Megapari =====
EXTRA_LABELS = {
 "fr":{"avis":"Avis sur","atouts":"Les atouts","faq":"Questions fréquentes"},
 "en":{"avis":"Review of","atouts":"Highlights","faq":"FAQ"},
 "es":{"avis":"Reseña de","atouts":"Ventajas","faq":"Preguntas frecuentes"},
 "ar":{"avis":"مراجعة","atouts":"المزايا","faq":"أسئلة شائعة"},
}
BK_EXTRA = {
 "code-promo-winwin": {
  "fr":{"rev":["WinWin est un bookmaker en forte croissance en Afrique francophone, très populaire au Cameroun, au Sénégal, en Côte d'Ivoire et au Bénin. En 2026, il se distingue par une application mobile légère qui fonctionne même avec une connexion lente, des cotes compétitives sur le football africain et international, et des dépôts et retraits en Mobile Money rapides et sans frais cachés.","Avec le code promo WinWin FFN, tu actives le bonus de bienvenue maximum dès ton premier dépôt. Le code se saisit une seule fois, à la création de ton compte. WinWin propose aussi les paris en direct, le cash-out et des promotions régulières, ce qui en fait une vraie alternative aux grands noms du marché."],
   "pros":["Application légère, idéale même en connexion faible","Dépôts et retraits Mobile Money rapides","Cotes attractives sur le football africain","Code promo FFN pour le bonus maximum"],
   "faq":[("Le code promo WinWin FFN est-il gratuit ?","Oui, le code FFN est 100% gratuit. Tu le saisis à l'inscription pour débloquer ton bonus de bienvenue, sans aucun frais."),("Comment déposer sur WinWin en Afrique ?","WinWin accepte le Mobile Money (Orange Money, MTN MoMo, Moov Money…) selon ton pays. Le dépôt est instantané et le retrait rapide.")]},
  "en":{"rev":["WinWin is a fast-growing bookmaker in French-speaking Africa, very popular in Cameroon, Senegal, Ivory Coast and Benin. In 2026 it stands out with a lightweight mobile app that works even on a slow connection, competitive odds on African and international football, and fast Mobile Money deposits and withdrawals with no hidden fees.","With the WinWin promo code FFN, you unlock the maximum welcome bonus on your first deposit. You enter the code once, when creating your account. WinWin also offers live betting, cash-out and regular promotions, making it a real alternative to the big names."],
   "pros":["Lightweight app, great even on a weak connection","Fast Mobile Money deposits and withdrawals","Attractive odds on African football","FFN promo code for the maximum bonus"],
   "faq":[("Is the WinWin promo code FFN free?","Yes, the FFN code is 100% free. Enter it at registration to unlock your welcome bonus, with no fees."),("How do I deposit on WinWin in Africa?","WinWin accepts Mobile Money (Orange Money, MTN MoMo, Moov Money…) depending on your country. Deposits are instant and withdrawals are fast.")]},
  "es":{"rev":["WinWin es una casa de apuestas en pleno crecimiento en el África francófona, muy popular en Camerún, Senegal, Costa de Marfil y Benín. En 2026 destaca por una aplicación móvil ligera que funciona incluso con conexión lenta, cuotas competitivas en el fútbol africano e internacional, y depósitos y retiros Mobile Money rápidos y sin comisiones ocultas.","Con el código promocional WinWin FFN, activas el bono de bienvenida máximo en tu primer depósito. El código se introduce una sola vez, al crear tu cuenta. WinWin también ofrece apuestas en vivo, cash-out y promociones regulares."],
   "pros":["App ligera, ideal incluso con conexión débil","Depósitos y retiros Mobile Money rápidos","Cuotas atractivas en el fútbol africano","Código FFN para el bono máximo"],
   "faq":[("¿El código promocional WinWin FFN es gratis?","Sí, el código FFN es 100% gratuito. Introdúcelo al registrarte para desbloquear tu bono de bienvenida, sin comisiones."),("¿Cómo depositar en WinWin?","WinWin acepta Mobile Money (Orange Money, MTN MoMo, Moov Money…) según tu país. El depósito es instantáneo y el retiro rápido.")]},
  "ar":{"rev":["WinWin شركة مراهنات سريعة النمو في إفريقيا الناطقة بالفرنسية، وتحظى بشعبية كبيرة في الكاميرون والسنغال وساحل العاج وبنين. في 2026 تتميّز بتطبيق خفيف يعمل حتى مع اتصال ضعيف، ونسب تنافسية على كرة القدم الإفريقية والدولية، وإيداعات وسحوبات Mobile Money سريعة دون رسوم خفية.","باستخدام رمز WinWin الترويجي FFN، تفعّل أقصى مكافأة ترحيب عند إيداعك الأول. يُدخل الرمز مرة واحدة عند إنشاء الحساب. كما يوفّر WinWin المراهنة المباشرة وسحب الأرباح المبكر وعروضًا منتظمة."],
   "pros":["تطبيق خفيف مناسب حتى مع اتصال ضعيف","إيداعات وسحوبات Mobile Money سريعة","نسب جذّابة على كرة القدم الإفريقية","رمز FFN للحصول على المكافأة القصوى"],
   "faq":[("هل رمز WinWin الترويجي FFN مجاني؟","نعم، الرمز FFN مجاني 100%. أدخله عند التسجيل لتفعيل مكافأة الترحيب دون أي رسوم."),("كيف أودع في WinWin؟","يقبل WinWin خدمة Mobile Money (Orange Money، MTN MoMo، Moov Money…) حسب بلدك. الإيداع فوري والسحب سريع.")]},
 },
 "code-promo-megapari": {
  "fr":{"rev":["Megapari est une plateforme moderne qui réunit paris sportifs et casino, avec une couverture impressionnante : des milliers d'événements chaque jour, un très large choix de marchés et des cotes parmi les plus élevées. En 2026, Megapari séduit de plus en plus de parieurs grâce à son interface fluide, ses promotions fréquentes et son bonus de bienvenue généreux.","En saisissant le code promo Megapari FFN à l'inscription, tu débloques le bonus maximum sur ton premier dépôt. Megapari accepte de nombreux moyens de paiement, dont le Mobile Money et les cryptomonnaies, et propose un service client réactif."],
   "pros":["Paris sportifs + casino sur une seule plateforme","Cotes élevées et marchés très variés","Paiements Mobile Money et cryptomonnaies","Code promo FFN pour le bonus maximum"],
   "faq":[("Quel est le code promo Megapari en 2026 ?","Le code promo Megapari est FFN. Saisis-le à l'inscription pour activer ton bonus de bienvenue maximum."),("Megapari propose-t-il un casino ?","Oui, Megapari combine paris sportifs et casino en ligne (machines à sous, jeux en direct) sur la même plateforme.")]},
  "en":{"rev":["Megapari is a modern platform that combines sports betting and casino, with impressive coverage: thousands of events every day, a very wide choice of markets and some of the highest odds. In 2026, Megapari is winning over more and more bettors thanks to its smooth interface, frequent promotions and generous welcome bonus.","By entering the Megapari promo code FFN at registration, you unlock the maximum bonus on your first deposit. Megapari accepts many payment methods, including Mobile Money and cryptocurrencies, and offers responsive customer support."],
   "pros":["Sports betting + casino on one platform","High odds and a very wide range of markets","Mobile Money and crypto payments","FFN promo code for the maximum bonus"],
   "faq":[("What is the Megapari promo code in 2026?","The Megapari promo code is FFN. Enter it at registration to activate your maximum welcome bonus."),("Does Megapari have a casino?","Yes, Megapari combines sports betting and an online casino (slots, live games) on the same platform.")]},
  "es":{"rev":["Megapari es una plataforma moderna que combina apuestas deportivas y casino, con una cobertura impresionante: miles de eventos cada día, una amplísima variedad de mercados y algunas de las cuotas más altas. En 2026, Megapari conquista a cada vez más apostadores gracias a su interfaz fluida, sus promociones frecuentes y su generoso bono de bienvenida.","Al introducir el código promocional Megapari FFN al registrarte, desbloqueas el bono máximo en tu primer depósito. Megapari acepta muchos métodos de pago, incluyendo Mobile Money y criptomonedas, y ofrece un servicio al cliente ágil."],
   "pros":["Apuestas deportivas + casino en una plataforma","Cuotas altas y mercados muy variados","Pagos Mobile Money y criptomonedas","Código FFN para el bono máximo"],
   "faq":[("¿Cuál es el código promocional de Megapari en 2026?","El código promocional de Megapari es FFN. Introdúcelo al registrarte para activar tu bono de bienvenida máximo."),("¿Megapari tiene casino?","Sí, Megapari combina apuestas deportivas y casino en línea (tragamonedas, juegos en vivo) en la misma plataforma.")]},
  "ar":{"rev":["Megapari منصّة عصرية تجمع بين المراهنات الرياضية والكازينو، بتغطية مذهلة: آلاف الأحداث يوميًا وتشكيلة واسعة جدًا من الأسواق ونِسب من الأعلى. في 2026 يكسب Megapari المزيد من المراهنين بفضل واجهته السلسة وعروضه المتكرّرة ومكافأة الترحيب السخية.","بإدخال رمز Megapari الترويجي FFN عند التسجيل، تفتح أقصى مكافأة على إيداعك الأول. يقبل Megapari وسائل دفع عديدة منها Mobile Money والعملات الرقمية، ويوفّر دعم عملاء سريع الاستجابة."],
   "pros":["مراهنات رياضية + كازينو في منصّة واحدة","نسب مرتفعة وأسواق متنوّعة جدًا","مدفوعات Mobile Money وعملات رقمية","رمز FFN للحصول على المكافأة القصوى"],
   "faq":[("ما هو رمز Megapari الترويجي في 2026؟","رمز Megapari الترويجي هو FFN. أدخله عند التسجيل لتفعيل أقصى مكافأة ترحيب."),("هل يوفّر Megapari كازينو؟","نعم، يجمع Megapari بين المراهنات الرياضية والكازينو (سلوتس وألعاب مباشرة) على المنصّة نفسها.")]},
 },
}
def bk_extra(b, lang):
    d = BK_EXTRA.get(b["slug"], {}).get(lang)
    if not d:
        return ""
    lab = EXTRA_LABELS.get(lang, EXTRA_LABELS["fr"])
    revs = "".join(f"<p>{p}</p>" for p in d["rev"])
    pros = "".join(f"<li>{x}</li>" for x in d["pros"])
    faqs = "".join(f'<div style="margin-top:12px"><b>{q}</b><br><span style="color:var(--mist)">{a}</span></div>' for q, a in d["faq"])
    vid_html = ""
    if b["slug"] == "code-promo-winwin":
        vlab = {"fr":"Tuto vidéo : télécharger WinWin et créer ton compte","en":"Video tutorial: download WinWin and create your account","es":"Tutorial en vídeo: descargar WinWin y crear tu cuenta","ar":"شرح بالفيديو: تحميل WinWin وإنشاء حسابك"}.get(lang, "Tuto WinWin")
        vid_html = (f'<p style="font-weight:800;margin-top:18px">\U0001F3A5 {vlab}</p>'
                    f'<div class="video yt-facade" data-yt="_ZuV0yzf95g" data-yt-title="{vlab}"><img src="https://img.youtube.com/vi/_ZuV0yzf95g/hqdefault.jpg" alt="{vlab}" loading="lazy"><span class="ytf-play">▶</span></div>')
    return (f'<section style="border-bottom:none">'
            f'<h2><span class="num">★</span> {lab["avis"]} {b["name"]}</h2>'
            f'{revs}'
            f'<p style="font-weight:800;margin-top:14px">{lab["atouts"]} :</p><ul style="margin-top:6px">{pros}</ul>'
            f'<p style="font-weight:800;margin-top:16px">{lab["faq"]}</p>{faqs}'
            f'{vid_html}'
            f'</section>')


TITLE_OVERRIDE = {
 "code-promo-winwin": {
   "fr": ("Code Promo WinWin 2026 : FFN → Bonus 300% jusqu'à 300 000 FCFA (MTN MoMo, Orange Money)",
          "Code promo WinWin FFN : bonus de bienvenue 300% jusqu'à 300 000 FCFA au Cameroun. Dépôt MTN Mobile Money et Orange Money, retrait rapide, appli Android et iPhone. Tuto vidéo par Cousin Marc."),
   "en": ("WinWin Promo Code 2026: FFN → 300% Bonus up to 300,000 FCFA (MTN MoMo, Orange Money)",
          "WinWin promo code FFN: 300% welcome bonus up to 300,000 FCFA in Cameroon. Deposit with MTN Mobile Money or Orange Money, fast withdrawals, Android and iPhone app. Video tutorial by Cousin Marc."),
 },
 "code-promo-1xbet": {
   "fr": ("Code Promo 1xBet 2026 : FFN → Bonus 300% jusqu'à 300 000 FCFA | Cousin Marc",
          "Code promo 1xBet 100% gratuit et vérifié : utilise FFN à l'inscription pour activer ton bonus de bienvenue de 300% jusqu'à 300 000 FCFA. Dépôt Mobile Money, guide complet par Cousin Marc."),
   "en": ("1xBet Promo Code 2026: FFN → 300% Bonus up to 300,000 FCFA | Cousin Marc",
          "Free, verified 1xBet promo code: use FFN at signup to activate your 300% welcome bonus up to 300,000 FCFA. Mobile Money deposits, full guide by Cousin Marc."),
 },
 "code-promo-1xbit": {
   "fr": ("Code Promo 1xBit Gratuit 2026 : FFN → Bonus Crypto jusqu'à 7 BTC (Sans KYC) | Cousin Marc",
          "Code promo 1xBit gratuit et vérifié : utilise FFN à l'inscription pour activer ton bonus crypto jusqu'à 7 BTC. Dépôts Bitcoin, USDT, Ethereum, sans vérification d'identité. Guide complet par Cousin Marc."),
   "en": ("1xBit Promo Code 2026 Free: FFN → Crypto Bonus up to 7 BTC (No KYC) | Cousin Marc",
          "Free, verified 1xBit promo code: use FFN at signup to activate your crypto bonus up to 7 BTC. Bitcoin, USDT and Ethereum deposits, no ID verification. Full guide by Cousin Marc."),
 },
 "code-promo-afroparie": {
   "fr": ("Code Promo Afropari (Afroparie) 2026 : FFN → 300% jusqu'à 300 000 FCFA | Cousin Marc",
          "Code promo Afroparie 100% gratuit et vérifié : utilise FFN à l'inscription pour activer ton bonus de bienvenue de 300% jusqu'à 300 000 FCFA. Dépôt Mobile Money rapide, interface en français. Guide complet par Cousin Marc."),
   "en": ("Afropari Promo Code 2026 (Afroparie): FFN → 300% Bonus up to 300,000 FCFA | Cousin Marc",
          "Free, verified Afroparie promo code: use FFN at signup to activate your 300% welcome bonus up to 300,000 FCFA. Fast Mobile Money deposits, French interface. Full guide by Cousin Marc."),
 },
}
COUNTRY_TITLE_OVERRIDE = {
 ("code-promo-melbet", "cameroun"): (
   "Code Promo Melbet Cameroun 2026 : FFN → 300% jusqu'à 300 000 FCFA (MTN MoMo, Orange Money)",
   "Code promo Melbet gratuit et vérifié pour le Cameroun : FFN à l'inscription = bonus de 300% sur ton 1er dépôt, jusqu'à 300 000 FCFA. Dépôt MTN Mobile Money ou Orange Money, à Douala, Yaoundé et partout au Cameroun."),
}
def _cty_title_desc(b, c, default_title, default_desc):
    o = COUNTRY_TITLE_OVERRIDE.get((b["slug"], c["slug"]))
    return o if o else (default_title, default_desc)
def _title_desc(b, lang, default_title, default_desc):
    o = TITLE_OVERRIDE.get(b["slug"], {}).get(lang)
    return o if o else (default_title, default_desc)


# ---------------------------------------------------------------- Guides detailles par bookmaker (pages code promo FR)
_VERIF = datetime.date.today()
VERIF_FR = f"{_VERIF.day} {_MOIS_FR[_VERIF.month - 1]} {_VERIF.year}"

def _calc_rows(rate=3, cap=300000):
    out = ""
    for dep in (1000, 5000, 10000, 25000, 50000, 100000):
        bonus = min(dep * rate, cap)
        out += f'<tr><td>{dep:,} FCFA</td><td><b>+ {bonus:,} FCFA</b></td><td>{dep + bonus:,} FCFA</td></tr>'.replace(",", " ")
    return out

BK_GUIDE_FR = {
 "code-promo-melbet": lambda b: f"""
<section id="fiche">
<h2>Code promo Melbet FFN : la fiche en bref</h2>
<div class="tablecard"><table>
<tbody>
<tr><td>Code promo</td><td><b>FFN</b> (à saisir une seule fois, à l'inscription)</td></tr>
<tr><td>Bonus de bienvenue</td><td><b>300% sur ton 1er dépôt</b>, jusqu'à 300 000 FCFA</td></tr>
<tr><td>Pays</td><td>Cameroun, Côte d'Ivoire, Sénégal, Burkina Faso, Bénin, Mali, Togo, RDC et la plupart des pays d'Afrique</td></tr>
<tr><td>Paiement</td><td>MTN Mobile Money, Orange Money, Moov Money, Wave, M-Pesa, Airtel Money, crypto (selon le pays)</td></tr>
<tr><td>Application</td><td>Android et iPhone (le code FFN marche aussi dans l'application)</td></tr>
<tr><td>Dernière vérification</td><td>{VERIF_FR}, par Cousin Marc</td></tr>
</tbody></table></div>
</section>
<section id="meilleur-code">
<h2>Quel est le meilleur code promo Melbet ?</h2>
<p>Sur internet, tu trouves des dizaines de « codes promo Melbet ». Ils ne se valent pas : beaucoup activent seulement le bonus standard de 100%, d'autres ne marchent pas dans ton pays.</p>
<p>Le bon réflexe, c'est de comparer <b>le pourcentage</b> et <b>le plafond dans ta devise</b>. Avec <b>FFN</b>, le bonus monte à <b>300% de ton premier dépôt, jusqu'à 300 000 FCFA</b> : c'est trois fois plus que le bonus de base.</p>
<p>Attention : tu ne peux utiliser <b>qu'un seul code</b>, et seulement au moment de l'inscription. Si tu as déjà un compte Melbet, un nouveau code ne s'applique pas à ce compte.</p>
</section>
<section id="calcul-bonus">
<h2>Combien tu reçois : calcul du bonus Melbet</h2>
<p>Le bonus est de 3 fois ton premier dépôt (300%), plafonné à 300 000 FCFA. Quelques exemples :</p>
<div class="tablecard"><table>
<thead><tr><th>Ton 1er dépôt</th><th>Bonus avec FFN</th><th>Total pour parier</th></tr></thead>
<tbody>{_calc_rows()}</tbody></table></div>
<div class="note" style="margin-top:14px"><label for="calc-dep" style="font-weight:700">Calcule ton bonus :</label>
<input id="calc-dep" type="number" min="0" step="500" placeholder="Ton dépôt en FCFA" style="margin:8px 8px 0 0;padding:10px 12px;border-radius:12px;border:1px solid var(--line);font:inherit;width:190px">
<b id="calc-out"></b>
<script>(function(){{var i=document.getElementById('calc-dep'),o=document.getElementById('calc-out');i.addEventListener('input',function(){{var d=Math.max(0,parseInt(i.value||0,10)),bo=Math.min(d*3,300000);o.textContent=d?('Bonus : + '+bo.toLocaleString('fr-FR')+' FCFA · Total : '+(d+bo).toLocaleString('fr-FR')+' FCFA'):'';}});}})();</script></div>
<p style="font-size:13px;color:var(--mist);margin-top:10px">Montants indicatifs. Le montant exact s'affiche dans ton compte après le dépôt.</p>
</section>
<section id="conditions">
<h2>Conditions du bonus Melbet : à lire avant de déposer</h2>
<ul class="steps">
<li><b>Le bonus n'est pas retirable tout de suite.</b> Il doit d'abord être rejoué un certain nombre de fois, en général en paris combinés d'au moins 3 matchs, avec une cote minimale par match.</li>
<li><b>Les règles exactes dépendent de ton pays.</b> Tu les trouves dans ton compte, rubrique « Promotions » ou « Bonus », juste après ton dépôt. Lis-les avant de parier.</li>
<li><b>Un seul bonus par personne</b> (même téléphone, même numéro Mobile Money, même adresse). Un deuxième compte peut être bloqué.</li>
<li><b>Ton compte doit être complet</b> (nom, date de naissance, numéro de téléphone vérifié) pour pouvoir retirer tes gains.</li>
</ul>
</section>
<section id="depot-retrait">
<h2>Dépôt et retrait sur Melbet en Afrique</h2>
<div class="tablecard"><table>
<thead><tr><th>Pays</th><th>Moyens de paiement les plus utilisés</th></tr></thead>
<tbody>
<tr><td><a href="code-promo-melbet-cameroun.html">Cameroun</a></td><td>MTN Mobile Money, Orange Money</td></tr>
<tr><td>Côte d'Ivoire</td><td>Orange Money, MTN, Moov Money, Wave</td></tr>
<tr><td>Sénégal</td><td>Wave, Orange Money, Free Money</td></tr>
<tr><td><a href="code-promo-melbet-burkina-faso.html">Burkina Faso</a></td><td>Orange Money, Moov Money</td></tr>
<tr><td>Bénin</td><td>MTN Mobile Money, Moov Money</td></tr>
<tr><td>Mali</td><td>Orange Money, Moov Money</td></tr>
<tr><td>Togo</td><td>T-Money, Flooz</td></tr>
<tr><td><a href="code-promo-melbet-rdc.html">RDC</a></td><td>M-Pesa, Orange Money, Airtel Money</td></tr>
</tbody></table></div>
<p style="margin-top:12px">Pour retirer : menu « Retirer », même moyen de paiement que pour le dépôt, puis confirmation sur ton téléphone. Si un retrait bloque, <a href="code-promo-ne-marche-pas.html">voici les solutions</a>. Pour le pas à pas complet : <a href="deposer-retirer-paris-afrique.html">déposer et retirer sur Melbet, étape par étape</a>.</p>
</section>
<section id="coupon">
<h2>Code promo ou code coupon Melbet : quelle différence ?</h2>
<p>On confond souvent les deux :</p>
<ul class="steps">
<li><b>Le code promo (FFN)</b> sert une seule fois, à l'inscription, pour activer ton bonus de bienvenue.</li>
<li><b>Le code coupon</b> sert à charger un ticket déjà préparé par quelqu'un : tu l'entres dans le coupon de paris de Melbet et les mêmes matchs s'ajoutent à ton ticket.</li>
</ul>
<p>Je partage mes coupons du jour sur ma chaîne Telegram et dans la <a href="cote-de-2.html">côte de 2 du jour</a>. Mes analyses de match sont dans l'onglet <a href="pronostics.html">Analyses</a>.</p>
</section>
<section id="application">
<h2>Application Melbet : Android et iPhone</h2>
<p>L'application Melbet est plus rapide que le site sur un petit réseau. Sur Android, elle s'installe depuis le lien officiel (fichier APK : autorise l'installation depuis cette source si ton téléphone le demande). Sur iPhone, elle se trouve sur l'App Store.</p>
<p>Le champ « Code promo » est aussi dans l'application : <b>FFN</b> fonctionne exactement comme sur le site. Que tu sois à Abidjan, Dakar, Ouagadougou, Douala ou Yaoundé, tout se fait en ligne, depuis ton téléphone.</p>
</section>
""",
}

BK_FAQ_FR = {
 "code-promo-melbet": [
  ("Quel est le meilleur code promo Melbet en 2026 ?", "Le code FFN : il donne 300% sur le premier dépôt, jusqu'à 300 000 FCFA, contre 100% pour le bonus de base. Il s'utilise une seule fois, à l'inscription."),
  ("J'ai oublié de mettre le code promo Melbet, que faire ?", "Le code ne peut pas être ajouté après l'inscription. Contacte le support Melbet depuis ton compte, sans faire de dépôt, et explique que tu voulais utiliser le code FFN. Ne crée pas de deuxième compte : il risque d'être bloqué."),
  ("Le code promo Melbet marche-t-il au Cameroun et en Côte d'Ivoire ?", "Oui. FFN fonctionne au Cameroun, en Côte d'Ivoire, au Sénégal, au Burkina Faso, au Bénin, au Mali, au Togo, en RDC et dans la plupart des pays où Melbet est disponible."),
  ("Quelle différence entre code promo et code coupon Melbet ?", "Le code promo (FFN) active le bonus à l'inscription. Le code coupon sert à charger un ticket de paris déjà préparé dans ton coupon Melbet."),
  ("Quel dépôt faire pour avoir le bonus maximum ?", "Avec 300%, un dépôt de 100 000 FCFA donne le bonus maximum de 300 000 FCFA. Un dépôt de 10 000 FCFA donne 30 000 FCFA de bonus."),
 ],
}


# Sections communes aux bookmakers du code FFN (fiche, calcul, conditions, paiements, coupon, application)
_PAY_ROWS = [("Cameroun", "MTN Mobile Money, Orange Money"), ("Côte d'Ivoire", "Orange Money, MTN, Moov Money, Wave"),
             ("Sénégal", "Wave, Orange Money, Free Money"), ("Burkina Faso", "Orange Money, Moov Money"),
             ("Bénin", "MTN Mobile Money, Moov Money"), ("Mali", "Orange Money, Moov Money"), ("Togo", "T-Money, Flooz"),
             ("RDC", "M-Pesa, Orange Money, Airtel Money")]

def _ffn_common(b, links=None):
    name, code = b["name"], b["code"]
    links = links or {}
    pays = ""
    for c, m in _PAY_ROWS:
        cell = f'<a href="{links[c]}">{c}</a>' if c in links else c
        pays += f"<tr><td>{cell}</td><td>{m}</td></tr>"
    return f"""
<section id="fiche">
<h2>Code promo {name} {code} : la fiche en bref</h2>
<div class="tablecard"><table><tbody>
<tr><td>Code promo</td><td><b>{code}</b> (à saisir une seule fois, à l'inscription)</td></tr>
<tr><td>Bonus de bienvenue</td><td><b>300% sur ton 1er dépôt</b>, jusqu'à 300 000 FCFA</td></tr>
<tr><td>Pays</td><td>Cameroun, Côte d'Ivoire, Sénégal, Burkina Faso, Bénin, Mali, Togo, RDC et la plupart des pays d'Afrique</td></tr>
<tr><td>Paiement</td><td>MTN Mobile Money, Orange Money, Moov Money, Wave, M-Pesa, Airtel Money, crypto (selon le pays)</td></tr>
{('<tr><td>Application</td><td>Android et iPhone (' + code + " marche aussi dans l'application)</td></tr>") if b.get("apps") else ""}
<tr><td>Dernière vérification</td><td>{VERIF_FR}, par Cousin Marc</td></tr>
</tbody></table></div>
</section>
<section id="calcul-bonus">
<h2>Combien tu reçois : calcul du bonus {name}</h2>
<p>Le bonus est de 3 fois ton premier dépôt (300%), plafonné à 300 000 FCFA. Quelques exemples :</p>
<div class="tablecard"><table>
<thead><tr><th>Ton 1er dépôt</th><th>Bonus avec {code}</th><th>Total pour parier</th></tr></thead>
<tbody>{_calc_rows()}</tbody></table></div>
<p style="font-size:13px;color:var(--mist);margin-top:10px">Montants indicatifs. Le montant exact s'affiche dans ton compte après le dépôt.</p>
</section>
<section id="conditions">
<h2>Conditions du bonus {name} : à lire avant de déposer</h2>
<ul class="steps">
<li><b>Le bonus n'est pas retirable tout de suite.</b> Il doit d'abord être rejoué un certain nombre de fois, en général en paris combinés d'au moins 3 matchs, avec une cote minimale par match.</li>
<li><b>Les règles exactes dépendent de ton pays.</b> Tu les trouves dans ton compte, rubrique « Promotions » ou « Bonus », juste après ton dépôt.</li>
<li><b>Un seul bonus par personne</b> (même téléphone, même numéro Mobile Money, même adresse). Un deuxième compte peut être bloqué.</li>
<li><b>Ton compte doit être complet</b> (nom, date de naissance, téléphone vérifié) pour pouvoir retirer tes gains.</li>
</ul>
</section>
<section id="depot-retrait">
<h2>Dépôt et retrait sur {name} en Afrique</h2>
<div class="tablecard"><table>
<thead><tr><th>Pays</th><th>Moyens de paiement les plus utilisés</th></tr></thead>
<tbody>{pays}</tbody></table></div>
<p style="margin-top:12px">Pour retirer : menu « Retirer », même moyen de paiement que pour le dépôt, puis confirmation sur ton téléphone. Le pas à pas complet : <a href="deposer-retirer-paris-afrique.html">déposer et retirer sur {name}</a>. Un blocage ? <a href="code-promo-ne-marche-pas.html">Voici les solutions</a>.</p>
</section>
<section id="coupon">
<h2>Code promo ou code coupon {name} : quelle différence ?</h2>
<ul class="steps">
<li><b>Le code promo ({code})</b> sert une seule fois, à l'inscription, pour activer ton bonus de bienvenue.</li>
<li><b>Le code coupon</b> sert à charger un ticket déjà préparé par quelqu'un : tu l'entres dans le coupon de paris de {name} et les mêmes matchs s'ajoutent à ton ticket.</li>
</ul>
<p>Je partage mes coupons du jour sur Telegram et dans la <a href="cote-de-2.html">côte de 2 du jour</a>. Mes analyses de match sont dans l'onglet <a href="pronostics.html">Analyses</a>.</p>
</section>
"""

BK_GUIDE_FR["code-promo-1xbet"] = lambda b: f"""
{_ffn_common(b, {"Sénégal": "code-promo-1xbet-senegal.html"})}
<section id="meilleur-code">
<h2>Quel est le meilleur code promo 1xBet ?</h2>
<p>Il existe des centaines de codes promo 1xBet sur internet. Pour choisir, regarde deux choses : <b>le pourcentage du bonus</b> et <b>le plafond dans ta devise</b>. Avec <b>FFN</b>, tu reçois <b>300% de ton premier dépôt, jusqu'à 300 000 FCFA</b>, soit trois fois le bonus de base de 100%.</p>
<p>Tu ne peux utiliser qu'<b>un seul code</b>, une seule fois, au moment de créer ton compte. Il ne s'ajoute pas à un compte qui existe déjà.</p>
</section>
<section id="generateur">
<h2>« Générateur de code promo 1xBet » : attention aux arnaques</h2>
<p>Beaucoup de gens cherchent un « générateur de code promo 1xBet ». <b>Ça n'existe pas.</b> Un code promo n'est pas fabriqué au hasard par une application : c'est un code partenaire fixe, attribué par 1xBet à une personne (comme FFN pour Cousin Marc).</p>
<ul class="steps">
<li>Un site ou une appli qui « génère » des codes, des bonus gratuits ou des coupons gagnants à coup sûr cherche ton argent ou tes identifiants.</li>
<li>Ne donne jamais ton mot de passe 1xBet, ton code Mobile Money ou un code reçu par SMS.</li>
<li>Le bonus officiel se débloque seulement avec un code partenaire à l'inscription, puis un vrai dépôt.</li>
</ul>
</section>
<section id="facultatif">
<h2>Le champ « Code promo (facultatif) » sur 1xBet</h2>
<p>Dans le formulaire d'inscription 1xBet, le champ code promo est marqué « facultatif » : tu peux créer ton compte sans le remplir. <b>Mais si tu le laisses vide, tu n'auras pas le bonus de 300%.</b> Et après l'inscription, il est trop tard pour l'ajouter.</p>
<p>Avant de valider, vérifie donc que <b>FFN</b> est bien écrit dans ce champ, en majuscules, sans espace. Le guide en images : <a href="comment-sinscrire-1xbet-2026.html">comment s'inscrire sur 1xBet en 2026</a>.</p>
</section>
<section id="codes-celebrites">
<h2>Codes promo 1xBet de célébrités : ça change quoi ?</h2>
<p>Tu as peut-être vu des codes promo 1xBet associés à des artistes ou des influenceurs. Ce sont aussi des codes partenaires : ils activent le bonus de bienvenue de la même façon. Ce qui compte, ce n'est pas le nom derrière le code, c'est <b>le bonus réellement obtenu dans ta devise</b>.</p>
<p>Pour l'Afrique francophone, FFN te donne 300% jusqu'à 300 000 FCFA, avec en plus mes coupons, mes analyses et l'aide de la communauté si tu bloques.</p>
</section>
<section id="inscription-methodes">
<h2>Les façons de s'inscrire sur 1xBet</h2>
<p>1xBet propose plusieurs formulaires : en un clic, par numéro de téléphone, par e-mail ou via un réseau social. <b>Dans tous les cas, le champ code promo est présent</b> : colle FFN avant de valider.</p>
<p>Je te conseille l'inscription <b>par numéro de téléphone</b> : ton compte est lié à ton numéro, ce qui facilite les dépôts et retraits Mobile Money et la récupération du compte.</p>
</section>
<section id="application">
<h2>Application 1xBet : Android et iPhone</h2>
<p>L'application 1xBet est plus rapide que le site sur un petit réseau. Sur Android, elle s'installe depuis le lien officiel (fichier APK : autorise l'installation depuis cette source si ton téléphone le demande). Sur iPhone, elle se trouve sur l'App Store. Le code FFN fonctionne de la même manière dans l'application.</p>
</section>
"""

BK_FAQ_FR["code-promo-1xbet"] = [
  ("Quel est le meilleur code promo 1xBet en 2026 ?", "Le code FFN : il donne 300% sur le premier dépôt, jusqu'à 300 000 FCFA, contre 100% pour le bonus de base. Il s'utilise une seule fois, à l'inscription."),
  ("Un générateur de code promo 1xBet, ça marche ?", "Non. Les codes promo 1xBet sont des codes partenaires fixes : aucun site ni application ne peut en générer. Ces « générateurs » sont des arnaques ; ne donne jamais ton mot de passe ni ton code Mobile Money."),
  ("Pourquoi le code promo est « facultatif » sur 1xBet ?", "Parce que tu peux t'inscrire sans code. Mais sans code, tu n'as pas le bonus de 300%, et tu ne peux plus l'ajouter après l'inscription. Mets FFN avant de valider."),
  ("J'ai oublié le code promo 1xBet à l'inscription, que faire ?", "Contacte le support 1xBet depuis ton compte avant de faire ton premier dépôt et explique que tu voulais utiliser le code FFN. Ne crée pas de deuxième compte : il risque d'être bloqué."),
  ("Combien de bonus pour 10 000 FCFA déposés sur 1xBet ?", "Avec 300%, un dépôt de 10 000 FCFA donne 30 000 FCFA de bonus, soit 40 000 FCFA pour parier. Le bonus maximum de 300 000 FCFA est atteint avec un dépôt de 100 000 FCFA."),
]


def _ffn_best(name, code="FFN"):
    return f"""
<section id="meilleur-code">
<h2>Quel est le meilleur code promo {name} ?</h2>
<p>Pour comparer deux codes promo {name}, regarde <b>le pourcentage du bonus</b> et <b>le plafond dans ta devise</b>. Avec <b>{code}</b>, tu reçois <b>300% de ton premier dépôt, jusqu'à 300 000 FCFA</b>, soit trois fois le bonus de base.</p>
<p>Un seul code par personne, une seule fois, au moment de l'inscription : il ne s'ajoute pas à un compte déjà créé.</p>
</section>"""

def _ffn_app(name, has_app):
    if not has_app:
        return ""
    return f"""
<section id="application">
<h2>Application {name} : Android et iPhone</h2>
<p>L'application {name} est plus légère que le site sur un petit réseau. Sur Android, elle s'installe depuis le lien officiel (fichier APK : autorise l'installation depuis cette source si ton téléphone le demande). Le champ « Code promo » est aussi dans l'application : <b>FFN</b> marche exactement comme sur le site.</p>
</section>"""

def _ffn_faq(name, extra=()):
    return list(extra) + [
        (f"Quel est le meilleur code promo {name} en 2026 ?", f"Le code FFN : il donne 300% sur le premier dépôt, jusqu'à 300 000 FCFA, contre 100% pour le bonus de base. Il s'utilise une seule fois, à l'inscription."),
        (f"J'ai oublié le code promo {name} à l'inscription, que faire ?", f"Le code ne peut pas être ajouté après coup. Contacte le support {name} depuis ton compte, avant ton premier dépôt, et explique que tu voulais utiliser FFN. Ne crée pas de deuxième compte : il risque d'être bloqué."),
        (f"Combien de bonus pour 10 000 FCFA déposés sur {name} ?", "Avec 300%, un dépôt de 10 000 FCFA donne 30 000 FCFA de bonus, soit 40 000 FCFA pour parier. Le maximum de 300 000 FCFA est atteint avec 100 000 FCFA déposés."),
    ]

BK_GUIDE_FR["code-promo-paripesa"] = lambda b: _ffn_common(b) + _ffn_best("Paripesa") + """
<section id="paripesa-senegal">
<h2>Paripesa au Sénégal, en Côte d'Ivoire et au Cameroun</h2>
<p>Paripesa est surtout utilisé en Afrique de l'Ouest et du Centre. Au Sénégal, les dépôts se font en général avec Wave ou Orange Money ; en Côte d'Ivoire avec Orange Money, MTN, Moov ou Wave ; au Cameroun avec MTN Mobile Money ou Orange Money. Le code <b>FFN</b> est le même dans tous ces pays, seul le plafond du bonus dépend de ta devise.</p>
<p>Astuce : choisis bien ton pays et ta devise dans le formulaire. Ils ne se changent pas facilement après l'inscription, et ce sont eux qui déterminent tes moyens de paiement.</p>
</section>""" + _ffn_app("Paripesa", True)

BK_GUIDE_FR["code-promo-winwin"] = lambda b: _ffn_common(b) + _ffn_best("WinWin") + """
<section id="winwin-2026">
<h2>Le code promo WinWin 2026 en un mot : FFN</h2>
<p>Tu as peut-être cherché « codepromowinwin2026 » ou « code promo WinWin 2026 » : la réponse tient en trois lettres, <b>FFN</b>. Le code ne change pas d'une année à l'autre, il reste valable en 2026.</p>
<p>WinWin est un bookmaker récent, pensé pour le mobile, avec dépôts et retraits par Mobile Money.</p>
</section>
<section id="application">
<h2>Application WinWin : Android et iPhone</h2>
<p>WinWin a une application <b>Android</b> (fichier APK, depuis le lien officiel) et une application <b>iPhone</b> sur l'App Store. Les deux liens sont dans les boutons en haut de cette page. Le champ « Code promo » est présent dans les deux : mets <b>FFN</b> avant de valider ton inscription.</p>
</section>"""

BK_GUIDE_FR["code-promo-megapari"] = lambda b: _ffn_common(b) + _ffn_best("Megapari") + """
<section id="verifier-coupon">
<h2>Vérifier un coupon Megapari</h2>
<p>Pour savoir où en est ton ticket, ouvre ton compte Megapari puis <b>l'historique des paris</b> : chaque coupon y apparaît avec son statut (en cours, gagné, perdu) et le détail des matchs.</p>
<p>Si quelqu'un te donne un <b>code coupon</b>, tu peux le charger dans le coupon de paris pour voir les matchs avant de jouer. Méfie-toi des « coupons sûrs à 100% » vendus sur les réseaux : aucun pronostic n'est garanti.</p>
</section>"""

BK_GUIDE_FR["code-promo-goldpari"] = lambda b: _ffn_common(b) + _ffn_best("GoldPari") + """
<section id="goldpari">
<h2>GoldPari avec le code FFN</h2>
<p>GoldPari fait partie des bookmakers partenaires du code <b>FFN</b> : même code que sur 1xBet, Melbet, Paripesa, WinWin et Megapari, et même bonus de 300% sur le premier dépôt, jusqu'à 300 000 FCFA.</p>
<p>Tu peux avoir un compte sur plusieurs bookmakers différents avec le même code FFN : c'est un seul compte par bookmaker qui est interdit, pas l'utilisation du même code chez plusieurs.</p>
</section>""" + _ffn_app("GoldPari", True)

BK_GUIDE_FR["code-promo-afroparie"] = lambda b: """
<section id="afropari">
<h2>Afropari ou Afroparie : c'est le même bookmaker</h2>
<p>Tu verras les deux orthographes, <b>Afropari</b> et <b>Afroparie</b> : il s'agit du même site de paris. Le code promo est le même dans les deux cas : <b>FFN</b>, pour un bonus de <b>300% sur ton premier dépôt, jusqu'à 300 000 FCFA</b>.</p>
<p>Le code promo Afropari et le « bonus code » Afropari, c'est aussi la même chose : un code à coller une seule fois dans le formulaire d'inscription.</p>
</section>""" + _ffn_common(b) + _ffn_best("Afropari (Afroparie)")

BK_FAQ_FR["code-promo-paripesa"] = _ffn_faq("Paripesa", [("Le code promo Paripesa marche-t-il au Sénégal ?", "Oui. FFN fonctionne au Sénégal, en Côte d'Ivoire, au Cameroun et dans la plupart des pays où Paripesa est disponible. Seul le plafond du bonus dépend de ta devise.")])
BK_FAQ_FR["code-promo-winwin"] = _ffn_faq("WinWin", [("Quel est le code promo WinWin 2026 ?", "Le code promo WinWin 2026 est FFN. Il donne 300% sur le premier dépôt, jusqu'à 300 000 FCFA, sur Android comme sur iPhone.")])
BK_FAQ_FR["code-promo-megapari"] = _ffn_faq("Megapari", [("Comment vérifier un coupon Megapari ?", "Ouvre ton compte Megapari puis l'historique des paris : chaque coupon y apparaît avec son statut et le détail des matchs.")])
BK_FAQ_FR["code-promo-goldpari"] = _ffn_faq("GoldPari", [("Puis-je utiliser FFN sur GoldPari et sur 1xBet ?", "Oui. Tu peux t'inscrire avec FFN chez plusieurs bookmakers différents. Ce qui est interdit, c'est d'avoir deux comptes chez le même bookmaker.")])
BK_FAQ_FR["code-promo-afroparie"] = _ffn_faq("Afropari", [("Afropari et Afroparie, c'est pareil ?", "Oui, ce sont deux orthographes du même bookmaker. Le code promo est FFN dans les deux cas : 300% sur le premier dépôt, jusqu'à 300 000 FCFA.")])

def bookmaker_page(b):
    name, code, slug = b["name"], b["code"], b["slug"]
    extra = f'<script type="application/ld+json">\n{faq_jsonld(name, code, BK_FAQ_FR.get(slug, ()))}\n</script>'
    _t, _d = _title_desc(b, "fr",
        f"Code Promo {name} 2026 : {code} → {bk_bonus(b,'fr')} | Cousin Marc",
        f"Code promo {name} 2026 : utilise {code} à l'inscription et active ton bonus ({bk_bonus(b,'fr')}). Guide d'inscription pas à pas par Cousin Marc.")
    return head(_t, _d,
        f"{BASE}/{slug}.html", extra, nav=nav_fr(en=f"{en_slug(b)}.html", es=f"{es_slug(b)}.html", ar=f"{ar_slug(b)}.html"), alternates=(f"{BASE}/{slug}.html", f"{BASE}/{en_slug(b)}.html", f"{BASE}/{es_slug(b)}.html", f"{BASE}/{ar_slug(b)}.html"), image=f"{BASE}/affiche-" + slug.replace("code-promo-","") + ".jpg") + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Cousin Marc Pronostic · Mis à jour {MAJ_FR}</p>
<h1>Code Promo <span class="hl" translate="no">{name}</span> 2026</h1>
<p class="sub">Active ton bonus de bienvenue <b>({bk_bonus(b,'fr')})</b> avec le code officiel ci-dessous. Vérifié et testé par Cousin Marc.</p>
<div class="codebox">{bk_logo(b, "cblogo", 64)}<div class="stamp"><span class="st-txt">Vérifié par CM</span></div>
<div class="lab">Code promo officiel</div>
<div class="code">{code}</div>
<small>À coller dans le champ « Code promo » à l'inscription</small>
<div><button class="copybtn" aria-label="Copier le code promo {code}" onclick="copyCode(this,'{code}')">📋 Copier le code</button></div>
{reg_block(b)}
</div>
<div class="btnrow">{buttons(b)}</div>
</div></header>
{affiche_img(b,'fr')}
<main class="wrap">
<section>
<h2><span class="num">01</span> C'est quoi le code promo {name} ?</h2>
<p>{bk_intro(b,'fr')}</p>
<p>Le code promo <b>{code}</b> est un code partenaire officiel : tu le saisis une seule fois à l'inscription pour activer le bonus de bienvenue de {name}.</p>
</section>
<section>
<h2><span class="num">02</span> Comment s'inscrire sur {name}</h2>
<ol class="steps">
<li><b>Ouvre {name}</b> via le bouton « S'inscrire sur le site » {"ou l'application" if b["apps"] else ""}.</li>
<li><b>Choisis ton pays et ta devise</b> — le bonus s'adapte automatiquement.</li>
<li><b>Colle le code <span style="color:var(--gold)">{code}</span></b> dans le champ « Code promo » avant de valider.</li>
<li><b>Effectue ton premier dépôt</b> : le bonus de {pct(b)} est crédité immédiatement.</li>
<li><b>Place tes paris</b> en suivant les pronostics de la communauté.</li>
</ol>
<div class="note" style="display:flex;flex-wrap:wrap;align-items:center;gap:14px;justify-content:space-between">
<span>🎥 Besoin d'aide en vidéo ? Je montre l'inscription complète et comment créer un compte authentique sur ma chaîne YouTube.</span>
<a class="cta" href="https://youtu.be/EnBk9p_Akvc" rel="nofollow" style="background:#ff0000;color:#fff">▶️ Voir le tuto YouTube</a>
</div>
</section>
<section>
<h2><span class="num">03</span> Bonus {name} par pays</h2>
<p>Avec le code <b>{b['code']}</b>, le bonus est de <b>{pct(b)} sur ton premier dépôt</b>{', jusqu’à 300 000 FCFA dans les pays FCFA' if b['slug'] in FFN300 else ''}, plafonné selon ta devise :</p>
<div class="tablecard"><table>
<thead><tr><th>Pays</th><th>Bonus maximum</th><th>Code</th></tr></thead>
<tbody>
{country_rows(b)}
</tbody></table></div>
<p style="font-size:13px;color:var(--mist);margin-top:12px">Montants indicatifs, susceptibles d'évoluer selon les promotions en cours.</p>
</section>
{BK_GUIDE_FR[slug](b) if slug in BK_GUIDE_FR else ""}
<section>
<h2><span class="num">04</span> Pourquoi me faire confiance ?</h2>
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">Pronostiqueur foot · communauté de 95 000+ abonnés</div></div></div>
<p style="margin-top:16px">Je publie des analyses foot pour l'Afrique depuis plusieurs années. J'utilise {name} moi-même : j'ai testé l'inscription, les dépôts et les retraits avec le code {code} avant de le partager.</p>
<div class="social">{social_html()}</div>
</section>
<section>
<h2><span class="num">05</span> Questions fréquentes</h2>
<details open><summary>Le code promo {name} {code} est-il gratuit ?</summary><p>Oui, totalement. Le code {code} ne coûte rien. Il sert uniquement à activer le bonus de bienvenue maximum à l'inscription.</p></details>
<details><summary>Où saisir le code promo sur {name} ?</summary><p>Pendant la création de ton compte, un champ « Code promo » apparaît dans le formulaire. Colles-y {code} avant de valider. Si tu l'oublies, tu ne pourras pas l'ajouter après coup.</p></details>
<details><summary>Le code marche-t-il dans mon pays ?</summary><p>Oui. {code} fonctionne dans tous les pays où {name} est disponible. Seul le montant maximum du bonus change selon ta devise.</p></details>
<details><summary>Puis-je utiliser {code} sur l'application mobile ?</summary><p>Absolument. Que tu t'inscrives depuis le site ou l'application, le champ code promo est présent et {code} fonctionne pareil.</p></details>
{"".join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in BK_FAQ_FR.get(slug, ()))}
<p style="margin-top:14px">Un souci avec le code ou le bonus ? <a href="code-promo-ne-marche-pas.html">Voir toutes les solutions →</a></p>
</section>
{country_block_for_bk(b)}
<section>
<h2><span class="num">06</span> Autres bookmakers & codes promo</h2>
<p>Compare les bonus des autres plateformes partenaires :</p>
<div class="related">
{bk_extra(b,'fr')}
{related_block(slug)}
</div>
</section>
<section style="text-align:center;border-bottom:none">
<h2 style="justify-content:center">Prêt à activer ton bonus ?</h2>
<p style="max-width:480px;margin:10px auto 0">Inscris-toi maintenant avec le code <b style="color:var(--gold)">{code}</b>.</p>
<div class="btnrow">{buttons(b)}</div>
</section>
</main>
{footer_html()}
{sticky_bar(b,'fr')}
</body></html>"""

HOME_T = {
 "fr": dict(eyebrow="Cousin Marc · Mis à jour {maj}", h1="Pronostics foot &amp; codes promo <em>vérifiés.</em>",
   lead="Le coupon du jour, les codes officiels des bookmakers et les guides pour s'inscrire, déposer et retirer en Afrique. Simple, clair, gratuit.",
   verified="Codes vérifiés le {d}", bar_copy="📋 Copier", bar_video="▶ Vidéo", more="Voir les {n} autres bookmakers", cta1="Voir les codes promo", cta2="Coupon du jour",
   trust=[("95K+","abonnés"),("{n}","bookmakers"),("4","langues"),("18+","jeu responsable")],
   copy="Copier", copy_aria="Copier le code promo", join="S'inscrire", guide="Guide",
   c_kick="Aujourd'hui", c_h2="Le coupon du jour", c_p="Publié sur le site et sur Telegram. Vérifie toujours le ticket avant de miser.",
   c_alt="Coupon Côte de 2 du jour — Cousin Marc",
   facts=[("🎯","Objectif côte 2","Une sélection courte, pensée pour doubler la mise."),("🆓","Gratuit","Le coupon est publié gratuitement chaque jour de match."),("📊","Résultats publiés","Les tickets passés sont visibles, gagnés comme perdus.")],
   c_full="Voir le coupon complet", c_res="Résultats",
   b_kick="Codes promo 2026", b_h2="Tous les bookmakers", b_p="Un code à saisir une seule fois à l'inscription pour activer le bonus de bienvenue. Clique pour le guide complet.",
   b_note="Bonus et conditions variables selon le pays. Liens partenaires : une commission peut être perçue, sans coût pour toi.",
   p_kick="Afrique", p_h2="Codes promo par pays", p_p="Devises, moyens de paiement et bookmakers disponibles dans ton pays.",
   a_kick="Qui est derrière ?", a_p="Le site rassemble mes analyses football, les coupons publiés et les guides des plateformes partenaires. Les liens d'affiliation sont signalés.",
   a_l1="Pronostics", a_l2="À propos", a_ro="Pronostics football · guides · communauté",
   tg_h2="Le coupon arrive d'abord sur Telegram.", tg_p="Rejoins la chaîne pour recevoir les nouveaux coupons et codes dès leur publication.", tg_cta="Rejoindre Telegram",
   urls=dict(cote2="cote-de-2.html", res="resultats.html", prono="pronostics.html", about="a-propos.html")),
 "en": dict(eyebrow="Cousin Marc · Updated {maj}", h1="Football tips &amp; <em>verified</em> promo codes.",
   lead="Today's coupon, official bookmaker promo codes and simple guides to sign up, deposit and withdraw in Africa. Clear and free.",
   verified="Codes checked on {d}", bar_copy="📋 Copy", bar_video="▶ Video", more="See the other {n} bookmakers", cta1="See the promo codes", cta2="Today's coupon",
   trust=[("95K+","followers"),("{n}","bookmakers"),("4","languages"),("18+","play responsibly")],
   copy="Copy", copy_aria="Copy promo code", join="Sign up", guide="Guide",
   c_kick="Today", c_h2="Today's coupon", c_p="Posted on the site and on Telegram. Always check the ticket before you bet.",
   c_alt="Today's odds of 2 coupon — Cousin Marc",
   facts=[("🎯","Target odds: 2","A short selection built to double your stake."),("🆓","Free","The coupon is published for free on every match day."),("📊","Published results","Past tickets stay visible, won or lost.")],
   c_full="See the full coupon", c_res="Results",
   b_kick="Promo codes 2026", b_h2="All bookmakers", b_p="Enter the code once when you sign up to unlock the welcome bonus. Tap for the full guide.",
   b_note="Bonuses and terms vary by country. Partner links: we may earn a commission at no cost to you.",
   a_kick="Who's behind it?", a_p="This site gathers my football analysis, published coupons and partner bookmaker guides. Affiliate links are clearly marked.",
   a_l1="Predictions", a_l2="About", a_ro="Football tips · guides · community",
   tg_h2="Coupons land on Telegram first.", tg_p="Join the channel to get new coupons and codes as soon as they're posted.", tg_cta="Join Telegram",
   urls=dict(cote2="odds-of-2.html", res="results.html", prono="predictions.html", about="about.html")),
 "es": dict(eyebrow="Cousin Marc · Actualizado {maj}", h1="Pronósticos de fútbol y códigos promo <em>verificados.</em>",
   lead="El cupón del día, los códigos oficiales de las casas de apuestas y guías para registrarte, depositar y retirar. Claro y gratis.",
   verified="Códigos verificados el {d}", bar_copy="📋 Copiar", bar_video="▶ Vídeo", more="Ver las otras {n} casas", cta1="Ver los códigos", cta2="Cupón del día",
   trust=[("95K+","seguidores"),("{n}","casas de apuestas"),("4","idiomas"),("18+","juego responsable")],
   copy="Copiar", copy_aria="Copiar el código promocional", join="Registrarse", guide="Guía",
   c_kick="Hoy", c_h2="El cupón del día", c_p="Publicado en el sitio y en Telegram. Revisa siempre el ticket antes de apostar.",
   c_alt="Cupón cuota de 2 del día — Cousin Marc",
   facts=[("🎯","Objetivo cuota 2","Una selección corta para duplicar la apuesta."),("🆓","Gratis","El cupón se publica gratis cada día de partido."),("📊","Resultados publicados","Los tickets pasados siguen visibles, ganados o perdidos.")],
   c_full="Ver el cupón completo", c_res="Resultados",
   b_kick="Códigos promocionales 2026", b_h2="Todas las casas de apuestas", b_p="Introduce el código una sola vez al registrarte para activar el bono de bienvenida. Toca para ver la guía.",
   b_note="Bonos y condiciones variables según el país. Enlaces de socios: podemos recibir una comisión sin coste para ti.",
   a_kick="¿Quién está detrás?", a_p="El sitio reúne mis análisis de fútbol, los cupones publicados y las guías de las casas asociadas. Los enlaces de afiliado están señalados.",
   a_l1="Pronósticos", a_l2="Acerca de", a_ro="Pronósticos de fútbol · guías · comunidad",
   tg_h2="El cupón llega primero a Telegram.", tg_p="Únete al canal para recibir los nuevos cupones y códigos en cuanto se publican.", tg_cta="Unirse a Telegram",
   urls=dict(cote2="cuota-de-2.html", res="resultados.html", prono="pronosticos.html", about="acerca-de.html")),
 "ar": dict(eyebrow="Cousin Marc · تحديث {maj}", h1="توقعات كرة القدم ورموز ترويجية <em>موثوقة.</em>",
   lead="قسيمة اليوم، الرموز الترويجية الرسمية لمواقع المراهنات، وأدلة بسيطة للتسجيل والإيداع والسحب. واضح ومجاني.",
   verified="تم التحقق من الرموز في {d}", bar_copy="📋 نسخ", bar_video="▶ شاهد الفيديو", more="عرض {n} مواقع أخرى", cta1="عرض الرموز الترويجية", cta2="قسيمة اليوم",
   trust=[("95K+","متابع"),("{n}","موقع مراهنات"),("4","لغات"),("18+","لعب مسؤول")],
   copy="نسخ", copy_aria="نسخ الرمز الترويجي", join="التسجيل", guide="الدليل",
   c_kick="اليوم", c_h2="قسيمة اليوم", c_p="تُنشر على الموقع وعلى تيليغرام. تحقق دائمًا من التذكرة قبل المراهنة.",
   c_alt="قسيمة رهان بضعف 2 لليوم — Cousin Marc",
   facts=[("🎯","الهدف: احتمال 2","اختيار قصير لمضاعفة الرهان."),("🆓","مجاني","تُنشر القسيمة مجانًا في كل يوم مباريات."),("📊","نتائج منشورة","التذاكر السابقة تبقى ظاهرة، رابحة أو خاسرة.")],
   c_full="عرض القسيمة كاملة", c_res="النتائج",
   b_kick="الرموز الترويجية 2026", b_h2="كل مواقع المراهنات", b_p="أدخل الرمز مرة واحدة عند التسجيل لتفعيل مكافأة الترحيب. اضغط لعرض الدليل الكامل.",
   b_note="المكافآت والشروط تختلف حسب البلد. روابط شركاء: قد نحصل على عمولة دون أي تكلفة عليك.",
   a_kick="من وراء الموقع؟", a_p="يجمع الموقع تحليلاتي لكرة القدم والقسائم المنشورة وأدلة المواقع الشريكة. روابط الإحالة مُشار إليها بوضوح.",
   a_l1="التوقعات", a_l2="من نحن", a_ro="توقعات كرة القدم · أدلة · مجتمع",
   tg_h2="القسيمة تصل أولًا على تيليغرام.", tg_p="انضم إلى القناة لتصلك القسائم والرموز الجديدة فور نشرها.", tg_cta="الانضمام إلى تيليغرام",
   urls=dict(cote2="cote-2-ar.html", res="resultats-ar.html", prono="pronostics-ar.html", about="a-propos-ar.html")),
}
_BONUS_TR = {
 "en": [("100% sur 1er dépôt","100% first deposit"),("100% sur le 1er dépôt","100% first deposit"),("jusqu'à","up to"),("sur les 4 premiers dépôts","on first 4 deposits"),("Bonus de bienvenue en crypto","Crypto welcome bonus")],
 "es": [("100% sur 1er dépôt","100% primer depósito"),("100% sur le 1er dépôt","100% primer depósito"),("jusqu'à","hasta"),("sur les 4 premiers dépôts","en los 4 primeros depósitos"),("Bonus de bienvenue en crypto","Bono de bienvenida en cripto")],
 "ar": [("100% sur 1er dépôt","100% على الإيداع الأول"),("100% sur le 1er dépôt","100% على الإيداع الأول"),("jusqu'à","حتى"),("sur les 4 premiers dépôts","على أول 4 إيداعات"),("Bonus de bienvenue en crypto","مكافأة ترحيب بالعملات الرقمية")],
}
def home_bonus(b, lang):
    v = BK_CONTENT.get(b["slug"], {}).get("bonus", {}).get(lang)
    if v: return v
    v = b["bonus_max"]
    for a, c in _BONUS_TR.get(lang, []): v = v.replace(a, c)
    return v

def _home_slug(b, lang):
    return {"en": en_slug, "es": es_slug, "ar": ar_slug}.get(lang, lambda x: x["slug"])(b)

def _logo_txt(hexcol):
    h = hexcol.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return "#0a0d0b" if (0.299*r + 0.587*g + 0.114*b) > 165 else "#ffffff"

def bk_logo(b, cls="blogo", size=40):
    fn = b["slug"].replace("code-promo-", "")
    if os.path.exists(os.path.join(OUT, "logos", fn + ".png")):
        return f'<img class="{cls}" src="logos/{fn}.png" alt="Logo {b["name"]}" width="{size}" height="{size}" loading="lazy" decoding="async">'
    col = BRAND.get(b["slug"], "#0a0d0b")
    return f'<span class="{cls}" style="background:{col};color:{_logo_txt(col)}" aria-hidden="true">{b["name"][:2].upper()}</span>'

def home_page(lang, title, desc, canonical, nav, alternates, footer):
    T = HOME_T[lang]
    maj = {"fr": MAJ_FR, "en": MAJ_EN, "es": MAJ_ES, "ar": MAJ_AR}[lang]
    U = T["urls"]
    top = ""
    for i, sl in enumerate(["code-promo-1xbet", "code-promo-melbet", "code-promo-paripesa"], 1):
        b = _bk(sl)
        top += (f'<article class="tcard"><span class="trank">#{i}</span>'
                f'<div class="tname" translate="no">{bk_logo(b)}{b["name"]}</div>'
                f'<div class="tbonus">{home_bonus(b, lang)}</div>'
                f'<div class="tcode"><span translate="no">{b["code"]}</span>'
                f'<button class="copybtn-mini" aria-label="{T["copy_aria"]} {b["code"]}" onclick="copyCode(this,\'{b["code"]}\')">{T["copy"]}</button></div>'
                f'<div class="tactions"><a class="tgo" href="{b["site"]}" rel="sponsored nofollow">{T["join"]}</a>'
                f'<a class="tmore" href="{_home_slug(b, lang)}.html">{T["guide"]} <span translate="no">{b["name"]}</span></a></div></article>')
    rows = "".join(
        f'<div class="bkrow">{bk_logo(b)}'
        f'<a class="bkinfo" href="{_home_slug(b, lang)}.html"><span class="bkname" translate="no">{b["name"]}</span><span class="bkbonus">{home_bonus(b, lang)}</span></a>'
        f'<div class="bkcodebox"><span class="bkcode" translate="no">{b["code"]}</span>'
        f'<button class="copybtn-mini" aria-label="{T["copy_aria"]} {b["code"]}" onclick="copyCode(this,\'{b["code"]}\')">{T["copy"]}</button></div>'
        f'<a class="bkjoin" href="{b["site"]}" rel="sponsored nofollow">{T["join"]}</a></div>'
        for b in BOOKMAKERS)
    day = {"fr": f"{_NOW.day} {_MOIS_FR[_NOW.month-1]} {_NOW.year}", "en": f"{_MOIS_EN[_NOW.month-1]} {_NOW.day}, {_NOW.year}",
           "es": f"{_NOW.day} de {_MOIS_ES[_NOW.month-1]} de {_NOW.year}", "ar": f"{_NOW.day} {_MOIS_AR[_NOW.month-1]} {_NOW.year}"}[lang]
    verified = T["verified"].replace("{d}", day)
    trust = "".join(f'<div><b>{v.replace("{n}", str(len(BOOKMAKERS)))}</b>{t}</div>' for v, t in T["trust"])
    facts = "".join(f'<div class="fact"><span class="fi">{i}</span><div><b>{t}</b><span>{d}</span></div></div>' for i, t, d in T["facts"])
    countries = ""
    matchs_home = ""
    compare_home = ""
    coupons_home = ""
    if lang == "fr" and coupons_ldc_html():
        coupons_home = (f'<section class="hsec" id="mes-coupons"><div class="wrap">'
                        f'<div class="hsec-head"><div><p class="kicker">Mes tickets joués</p><h2>🎫 Mes coupons Ligue des champions</h2>'
                        f'<p>Les combinés que j\'ai joués avec mon argent. Tu peux reprendre les mêmes matchs sur WinWin (inscription avec le code FFN).</p></div></div>'
                        f'{coupons_ldc_html()}<p class="muted" style="font-size:13px;margin-top:12px">18+ · Un pronostic n\'est jamais sûr. Ne mise que ce que tu peux perdre.</p></div></section>')
    if lang == "fr" and MATCHS:
        matchs_home += (f'<section class="hsec" id="pronostics"><div class="wrap">'
                       f'<div class="hsec-head"><div><p class="kicker">Pronostics</p><h2>Les derniers matchs analysés</h2>'
                       f'<p>Mon pronostic, la cote et l\'analyse pour chaque grand match.</p></div><a class="cta alt" href="pronostics.html">Tous les pronostics</a></div>'
                       f'{matchs_list_html(6)}</div></section>')
    if lang == "fr":
        compare_home = (f'<section class="hsec" id="comparateur"><div class="wrap">'
                        f'<div class="hsec-head"><div><p class="kicker">En 10 secondes</p><h2>Quel bookmaker pour toi ?</h2>'
                        f'<p>Choisis ton pays et ton moyen de paiement, je te donne ton top 3 avec le bon code.</p></div></div>'
                        f'{comparator_html()}</div></section>')
    if lang == "fr":
        countries = (f'<section class="hsec" id="pays"><div class="wrap">'
                     f'<div class="hsec-head"><div><p class="kicker">{T["p_kick"]}</p><h2>{T["p_h2"]}</h2><p>{T["p_p"]}</p></div></div>'
                     f'<div class="related">{country_index_cards()}</div></div></section>')
    return head(title, desc, canonical, nav=nav, lang=lang, alternates=alternates, show_youtube=True) + f"""
<header class="home-hero"><div class="wrap">
<p class="eyebrow">{T["eyebrow"].replace("{maj}", maj)}</p>
<h1>{T["h1"]}</h1>
<p class="lead">{T["lead"]}</p>
<div class="btnrow"><a class="cta" href="#bookmakers">{T["cta1"]}</a><a class="cta alt" href="#coupon-du-jour">{T["cta2"]}</a></div>
<div class="home-trust">{trust}</div>
<div class="topcodes">{top}</div>
</div></header>

{coupons_home}

{compare_home}

<section class="hsec" id="coupon-du-jour"><div class="wrap">
<div class="hsec-head"><div><p class="kicker">{T["c_kick"]}</p><h2>{T["c_h2"]}</h2><p>{T["c_p"]}</p></div></div>
<div class="coupon-grid">
<div class="coupon-card">{cote2_history_html(lang, T["c_alt"])}</div>
<div class="facts">{facts}
<div class="btnrow" style="justify-content:flex-start;margin-top:6px"><a class="cta" href="{U["cote2"]}">{T["c_full"]}</a><a class="cta alt" href="{U["res"]}">{T["c_res"]}</a></div>
</div>
</div>
</div></section>

<section class="hsec" id="bookmakers"><div class="wrap">
<div class="hsec-head"><div><p class="kicker">{T["b_kick"]}</p><h2>{T["b_h2"]}</h2><p>{T["b_p"]}</p></div></div>
<p class="verified">✅ {verified}</p>
<div class="bklist">{rows}</div>
<p style="font-size:13px;color:var(--muted);margin-top:12px">{T["b_note"]}</p>
</div></section>

{winners_wall(lang)}

{matchs_home}

{countries}

<section class="hsec"><div class="wrap about-grid">
<div><p class="kicker">{T["a_kick"]}</p><h2>Cousin Marc</h2>
<p>{T["a_p"]}</p>
<div class="btnrow" style="justify-content:flex-start"><a class="cta alt" href="{U["prono"]}">{T["a_l1"]}</a><a class="cta alt" href="{U["about"]}">{T["a_l2"]}</a></div></div>
<div><div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">{T["a_ro"]}</div></div></div>
<div class="social">{social_html()}</div></div>
</div></section>

<div class="wrap"><div class="tgband"><div><h2>{T["tg_h2"]}</h2><p>{T["tg_p"]}</p></div>
<a class="cta" href="https://t.me/marc_prono" rel="nofollow">{T["tg_cta"]}</a></div></div>
{footer()}
</body></html>"""

def index_page():
    return home_page("fr",
        "Cousin Marc Pronostic : Pronostics Foot & Codes Promo 2026 (FFN)",
        "Pronostics foot, coupon du jour et codes promo bookmakers 2026. Retrouve les analyses de Cousin Marc et les codes officiels dont FFN.",
        f"{BASE}/", NAV, (f"{BASE}/", f"{BASE}/promo-codes.html", f"{BASE}/codigos-promocionales.html", f"{BASE}/promo-codes-ar.html"),
        footer_html)

def pronostics_page():
    now = datetime.datetime.now()
    upcoming = sorted([m for m in MATCHS if not m.get("resultat") and m["dt"] >= now - datetime.timedelta(hours=3)], key=lambda m: m["dt"])
    done = sorted([m for m in MATCHS if m not in upcoming], key=lambda m: m["dt"], reverse=True)
    res = [_RES_FR.get(m.get("resultat", "").lower(), (None, None))[1] for m in MATCHS]
    w, l = res.count("win"), res.count("lose")
    stats = f'<div><b>{len(MATCHS)}</b>analyses publiées</div><div><b>{len(upcoming)}</b>matchs à venir</div>'
    if w + l:
        stats += f'<div><b>{w}</b>gagnés</div><div><b>{l}</b>perdus</div><div><b>{round(100 * w / (w + l))} %</b>de réussite</div>'
    comps = sorted({m.get("competition", "Football") for m in MATCHS})
    chips = '<button type="button" class="chip on" data-f="*">Tout</button>' + "".join(
        f'<button type="button" class="chip" data-f="{html.escape(c)}">{html.escape(c)}</button>' for c in comps)

    def by_day(lst):
        out, day = "", None
        for m in lst:
            d = m["dt"].date()
            if d != day:
                if day is not None: out += "</div></div>"
                day = d
                out += (f'<div class="daygroup"><h3>{_JOURS_FR[m["dt"].weekday()].capitalize()} {m["dt"].day} {_MOIS_FR[m["dt"].month-1]}</h3><div class="mgrid">')
            out += match_card(m).replace('<a class="mcard"', f'<a class="mcard" data-c="{html.escape(m.get("competition", "Football"))}"', 1)
        return out + ("</div></div>" if day is not None else "")

    itemlist = json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": "Pronostics et analyses foot de Cousin Marc",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f'{BASE}/{m["slug"]}.html', "name": f'Pronostic {m["equipe1"]} vs {m["equipe2"]}'}
                            for i, m in enumerate(upcoming + done)]}, ensure_ascii=False)
    up_html = by_day(upcoming) or '<p class="muted">Les prochaines analyses arrivent bientôt. Rejoins le Telegram pour être prévenu.</p>'
    done_html = (f'<section id="termines"><h2><span class="num">✓</span> Matchs terminés</h2>'
                 f'<p>Je garde tous mes pronostics en ligne, gagnés comme perdus : c\'est plus honnête.</p>{by_day(done)}</section>') if done else ""
    coupons = (f'<section id="mes-coupons"><h2><span class="num">🎫</span> Mes coupons joués</h2>'
               f'<p>Les combinés que j\'ai joués. Tu peux reprendre les mêmes matchs sur WinWin (inscription avec le code FFN).</p>{coupons_ldc_html()}</section>') if coupons_ldc_html() else ""
    return head(
        "Pronostics foot du jour : analyses des grands matchs | Cousin Marc",
        "Mes analyses et pronostics gratuits des grands matchs : Ligue des champions, Premier League, Liga, Ligue 1… Mon avis, la cote et le résultat, mis à jour chaque semaine.",
        f"{BASE}/pronostics.html", nav=nav_fr(en="predictions.html", es="pronosticos.html", ar="pronostics-ar.html"),
        alternates=(f"{BASE}/pronostics.html", f"{BASE}/predictions.html", f"{BASE}/pronosticos.html", f"{BASE}/pronostics-ar.html"),
        extra=f'<script type="application/ld+json">{itemlist}</script>') + f"""
<style>
.astats{{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}}
.astats div{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px 16px;font-size:13px;color:var(--muted);font-weight:600}}
.astats b{{display:block;font-family:var(--display);font-size:24px;color:var(--ink)}}
.afilter{{position:sticky;top:64px;z-index:5;background:var(--bg,#fff);padding:10px 0;margin-bottom:6px}}
.daygroup{{margin-top:22px}}
.daygroup h3{{font-size:15px;text-transform:uppercase;letter-spacing:.06em;color:var(--green-ink);margin-bottom:8px}}
</style>
<header class="hero"><div class="wrap">
<p class="eyebrow">📊 Analyses · mis à jour {MAJ_FR}</p>
<h1>Pronostics foot <span class="hl">du jour</span></h1>
<p class="sub">Mes analyses des grands matchs : Ligue des champions, Premier League, Liga, Ligue 1, CAN… Pour chaque match : mon pronostic, la cote, mon avis, puis le résultat.</p>
<div class="astats">{stats}</div>
</div></header>
<main class="wrap">
<section id="a-venir">
<h2><span class="num">⚽</span> Prochains matchs analysés</h2>
<div class="afilter chips" role="group" aria-label="Filtrer par compétition">{chips}</div>
{up_html}
</section>
{coupons}
{done_html}
<section>
<h2><span class="num">●</span> Les analyses en avant-première sur Telegram</h2>
<p>Je confirme chaque pronostic le jour du match, après les compositions, sur mon canal Telegram et ma chaîne WhatsApp. C'est gratuit.</p>
<div class="btnrow" style="justify-content:flex-start">
<a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Rejoindre le Telegram</a>
<a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 Rejoindre le WhatsApp</a>
</div>
<div class="note" style="margin-top:16px">Un pronostic n'est jamais une certitude. Ne mise que ce que tu peux te permettre de perdre. 18+</div>
</section>
<section>
<h2><span class="num">●</span> Parie avec les bons codes promo</h2>
<p>Avant de suivre mes pronos, ouvre ton compte sur un de nos bookmakers partenaires et profite du bonus de bienvenue :</p>
<div class="related">
{related_block("")}
</div>
</section>
</main>
<script>
(function(){{var bs=document.querySelectorAll('.afilter .chip');bs.forEach(function(b){{b.addEventListener('click',function(){{
bs.forEach(function(x){{x.classList.toggle('on',x===b);}});var f=b.getAttribute('data-f');
document.querySelectorAll('#a-venir .mcard,#termines .mcard').forEach(function(c){{c.style.display=(f==='*'||c.getAttribute('data-c')===f)?'':'none';}});
document.querySelectorAll('.daygroup').forEach(function(g){{var v=[].some.call(g.querySelectorAll('.mcard'),function(c){{return c.style.display!=='none';}});g.style.display=v?'':'none';}});
}});}});}})();
</script>
{footer_html()}
</body></html>"""

def apropos_page():
    return head(
        "Cousin Marc Pronostic : qui suis-je, code promo FFN, Telegram & WhatsApp",
        "Cousin Marc, pronostiqueur foot Afrique (95 000+ abonnés). Mon code promo FFN testé sur 1xBet, Melbet, Paripesa, WinWin. Rejoins mes pronostics gratuits sur Telegram et WhatsApp.",
        f"{BASE}/a-propos.html", nav=nav_fr(en="about.html", es="acerca-de.html", ar="a-propos-ar.html"), alternates=(f"{BASE}/a-propos.html", f"{BASE}/about.html", f"{BASE}/acerca-de.html", f"{BASE}/a-propos-ar.html")) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Qui suis-je ?</p>
<h1>Cousin Marc <span class="hl">Pronostic</span></h1>
<p class="sub">Pronostiqueur foot pour l'Afrique francophone. 95 000+ abonnés sur Telegram, WhatsApp, Facebook, YouTube et Snapchat.</p>
<div class="codebox"><div class="stamp"><span class="st-txt">Vérifié par CM</span></div>
<div class="lab">Mon code promo (tous bookmakers)</div>
<div class="code">FFN</div>
<small>1xBet · Melbet · Paripesa · WinWin · Megapari</small>
<div><button class="copybtn" aria-label="Copier le code promo FFN" onclick="copyCode(this,'FFN')">📋 Copier le code</button></div>
</div>
<div class="btnrow"><a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Pronostics Telegram</a><a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 WhatsApp</a></div>
</div></header>
<main class="wrap legalbody">
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">Pronostiqueur foot · communauté de 95 000+ abonnés</div></div></div>
<p>Je suis Cousin Marc, pronostiqueur passionné de football. Depuis plusieurs années, j'accompagne une large communauté de parieurs à travers l'Afrique francophone avec des analyses de matchs, des conseils, et une sélection de bons plans bookmakers.</p>
<h2>Ma mission</h2>
<p>T'aider à parier de façon plus informée : comprendre les cotes, choisir les bonnes plateformes, profiter des meilleurs bonus de bienvenue, et le faire de manière responsable.</p>
<h2>Pourquoi mes codes promo ?</h2>
<p>Chaque code promo partagé sur ce site (FFN, et les codes spécifiques par bookmaker) est testé personnellement avant d'être publié. Je vérifie l'inscription, le dépôt et le retrait pour m'assurer que tout fonctionne.</p>
<h2>Ce que tu trouves sur ce site</h2>
<ul>
<li><a href="index.html" style="color:var(--gold);font-weight:700">Les codes promo</a> de 12 bookmakers, avec le bonus par pays.</li>
<li><a href="cote-de-2.html" style="color:var(--gold);font-weight:700">Le coupon Côte de 2</a> du jour et le <a href="total-pair-impair.html" style="color:var(--gold);font-weight:700">Total Pair/Impair</a>.</li>
<li><a href="resultats.html" style="color:var(--gold);font-weight:700">Les résultats</a> : preuves de coupons gagnants payés.</li>
<li><a href="paris-sportifs-cameroun.html" style="color:var(--gold);font-weight:700">Les guides par pays</a> : Cameroun, Côte d'Ivoire, Sénégal, RDC, Bénin, Mali, Togo, Burkina.</li>
<li><a href="vip.html" style="color:var(--gold);font-weight:700">L'abonnement VIP</a> pour les pronostics premium.</li>
</ul>
<h2>Rejoins la communauté</h2>
<p>Pour mes pronostics en avant-première et mes analyses détaillées :</p>
<div class="social">{social_html()}</div>
<div class="note">⚠️ Le pari sportif comporte des risques. Je partage des analyses et des bons plans, mais aucun pronostic n'est garanti. Joue de manière responsable.</div>
</main>
{footer_html()}
</body></html>"""

def jeu_responsable_page():
    return head(
        "Jeu Responsable | Cousin Marc Pronostic",
        "Conseils pour parier de manière responsable. Le jeu doit rester un plaisir : limites, signes d'alerte et ressources d'aide.",
        f"{BASE}/jeu-responsable.html", nav=nav_fr(en="responsible-gambling.html", es="juego-responsable.html", ar="jeu-responsable-ar.html"), alternates=(f"{BASE}/jeu-responsable.html", f"{BASE}/responsible-gambling.html", f"{BASE}/juego-responsable.html", f"{BASE}/jeu-responsable-ar.html")) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Important</p>
<h1>Jeu <span class="hl">responsable</span></h1>
</div></header>
<main class="wrap legalbody">
<p>Les paris sportifs doivent rester un divertissement, jamais une source de revenus ni une solution à des difficultés financières. Voici quelques règles essentielles.</p>
<h2>Les règles de base</h2>
<ul>
<li>Réservé aux personnes majeures (18 ans et +).</li>
<li>Ne mise que ce que tu peux te permettre de perdre.</li>
<li>Fixe-toi un budget et des limites de temps, et respecte-les.</li>
<li>Ne parie jamais pour « te refaire » après une perte.</li>
<li>Le pari n'est pas un moyen de gagner de l'argent de façon régulière.</li>
</ul>
<h2>Signes d'alerte</h2>
<ul>
<li>Tu paries plus que prévu, ou avec de l'argent dont tu as besoin.</li>
<li>Tu penses au pari en permanence.</li>
<li>Tu caches tes paris à tes proches.</li>
<li>Tu paries pour échapper à des problèmes ou au stress.</li>
</ul>
<h2>Besoin d'aide ?</h2>
<p>Si le jeu devient un problème pour toi ou un proche, parles-en à une personne de confiance et rapproche-toi d'une structure d'aide locale spécialisée dans la dépendance au jeu. La plupart des bookmakers proposent aussi des outils d'auto-limitation et d'auto-exclusion dans les paramètres de ton compte.</p>
<div class="note">Le jeu doit rester un plaisir. Si ce n'est plus le cas, fais une pause.</div>
</main>
{footer_html()}
</body></html>"""

def mentions_page():
    return head(
        "Mentions légales | Cousin Marc Pronostic",
        "Mentions légales du site Cousin Marc Pronostic : éditeur, hébergement, liens d'affiliation et avertissement sur les paris sportifs.",
        f"{BASE}/mentions-legales.html") + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Informations</p>
<h1>Mentions <span class="hl">légales</span></h1>
</div></header>
<main class="wrap legalbody">
<h2>Éditeur du site</h2>
<p>Ce site est édité par Cousin Marc Pronostic, dans le cadre d'une activité de création de contenu et d'affiliation autour des paris sportifs.</p>
<h2>Hébergement</h2>
<p>Le site est hébergé par Netlify. Le nom de domaine est enregistré via Cloudflare.</p>
<h2>Liens d'affiliation</h2>
<p>Ce site contient des liens d'affiliation vers des bookmakers partenaires. Lorsqu'un utilisateur s'inscrit via ces liens et le code promo, le site peut percevoir une commission, sans coût supplémentaire pour l'utilisateur. Cela n'influence pas l'honnêteté des informations partagées.</p>
<h2>Avertissement</h2>
<p>Les paris sportifs sont réservés aux personnes majeures (18 ans et +) et comportent des risques financiers. Les informations de ce site sont fournies à titre indicatif. Aucun pronostic n'est garanti. Consulte notre page <a href="jeu-responsable.html" style="color:var(--gold)">Jeu responsable</a>.</p>
<h2>Contenu</h2>
<p>Les montants de bonus, codes et offres sont indicatifs et susceptibles d'évoluer selon les conditions des bookmakers et ton pays de résidence. Vérifie toujours les conditions officielles sur le site du bookmaker.</p>
</main>
{footer_html()}
</body></html>"""


# ===== PAGE VIP (abonnement premium crypto) =====
VIP_TG   = "https://t.me/Barcilone"
VIP_PRICE = "400 $"  # prix annuel (voir VIP_PLANS pour toutes les formules)
VIP_PRICE_XAF = "25 000 / 65 000 / 240 000 FCFA"   # montants Mobile Money des 3 formules
# Formules VIP : (cle, prix $, prix FCFA, prix mensuel equivalent, meilleure offre ?)
VIP_PLANS = [
 ("m1", "42 $", "25 000 FCFA", "25 000 FCFA", False),
 ("m3", "108 $", "65 000 FCFA", "≈ 21 700 FCFA", False),
 ("y1", "400 $", "240 000 FCFA", "20 000 FCFA", True),
]
# Photos de grosses cotes gagnantes (fichiers a placer dans le dossier site/), ex. "vip-proof-01.jpg"
# (fichier, match, cote, en direct ?, gain paye ou "")
VIP_PROOFS = [
 ("vip-proof-41.jpg", "⚽ Barcelone – Real Madrid (Clásico, victoire du Real)", "4.06", False, "8 120 000 F"),
 ("vip-proof-42.jpg", "⚽ Torino – Como (Serie A, victoire de Como)", "18", False, "8 100 000 F"),
 ("vip-proof-43.jpg", "⚽ Barcelone – Real Madrid (Clásico, victoire du Real)", "7.1", False, "3 550 000 F"),
 ("vip-proof-35.jpg", "⚽ Fribourg – Wolfsbourg (Coupe d'Allemagne, Wolfsbourg 1re mi-temps)", "8.56", False, "4 280 000 F"),
 ("vip-proof-36.jpg", "⚽ St. Louis City – Portland Timbers (MLS, Portland marque en 1re mi-temps)", "8.4", True, "4 200 000 F"),
 ("vip-proof-37.jpg", "⚽ St. Louis City – Portland Timbers (MLS, Portland 1re mi-temps)", "8", True, "4 000 000 F"),
 ("vip-proof-38.jpg", "⚽ Fribourg – Wolfsbourg (Coupe d'Allemagne, Wolfsbourg 1re mi-temps)", "6.55", False, "3 275 000 F"),
 ("vip-proof-39.jpg", "⚽ Toronto – D.C. United (MLS, D.C. United 1re mi-temps)", "4.51", True, "2 255 000 F"),
 ("vip-proof-40.jpg", "⚽ St. Louis City – Portland Timbers (MLS, Portland 1re mi-temps)", "4.03", True, "2 015 000 F"),
 ("vip-proof-32.jpg", "⚽ Daejeon Hana Citizen – Gwangju (K League 1)", "6.6", False, "4 917 000 F"),
 ("vip-proof-33.jpg", "⚽ Austin – Whitecaps de Vancouver (MLS, Austin 1re mi-temps)", "5.83", False, "3 253 350 F"),
 ("vip-proof-34.jpg", "⚽ Combiné (3 matchs) Machida Zelvia – Avispa Fukuoka…", "8.47", False, "1 313 600 F"),
 ("vip-proof-26.jpg", "⚽ Stade Rennais – OFI Crète (Ligue Europa, OFI 1re mi-temps)", "11", False, "3 850 000 F"),
 ("vip-proof-27.jpg", "⚽ Torreense – Sunderland (Ligue Europa, Torreense 1re mi-temps)", "12.9", False, "3 225 000 F"),
 ("vip-proof-28.jpg", "⚽ Tampines Rovers – Machida Zelvia (Ligue des champions AFC 2)", "10.7", False, "2 675 000 F"),
 ("vip-proof-29.jpg", "⚽ Rubin Kazan – Orenbourg (Coupe de Russie, Orenbourg 1re mi-temps)", "5.03", False, "2 515 000 F"),
 ("vip-proof-30.jpg", "⚽ BG Pathum – Adelaide United (Ligue des champions AFC 2)", "4.53", False, "2 265 000 F"),
 ("vip-proof-31.jpg", "⚽ Torreense – Sunderland (Torreense +0,5 but 1re mi-temps)", "7.7", False, "1 925 000 F"),
 ("vip-proof-23.jpg", "🎾 Sabalenka – Ann Li (WTA Wuhan, en direct)", "6.02", True, "3 010 000 F"),
 ("vip-proof-24.jpg", "🎾 Sabalenka – Ann Li (2e set Ann Li, en direct)", "4.67", True, "2 335 000 F"),
 ("vip-proof-25.jpg", "🎾 Sabalenka – Ann Li (jeu du 3e set, en direct)", "3.62", True, "1 267 000 F"),
 ("vip-proof-21.jpg", "⚽ Combiné Championship : Wolves – Bolton · Burnley – Charlton", "5.63", False, "2 816 700 F"),
 ("vip-proof-20.jpg", "⚽ Wolves – Bolton (Bolton +1.5 buts)", "5.25", False, "2 625 000 F"),
 ("vip-proof-22.jpg", "⚽ Viking – Bayern Munich (Viking +2.5 buts)", "4.72", False, "2 360 000 F"),
 ("vip-proof-19.jpg", "⚽ Combiné Ligue des champions : Lens – Sporting · Atlético – Man Utd · Galatasaray – Barça", "8.92", False, "2 230 449 F"),
 ("vip-proof-18.jpg", "⚽ Combiné Ligue des champions (4 matchs) : Lens – Sporting · Villarreal – Naples · Leipzig – PSV · Viking – Bayern", "7.76", False, "1 940 694 F"),
 ("vip-proof-11.jpg", "⚽ Charlotte – Dallas", "24", False, "6 000 000 F"),
 ("vip-proof-12.jpg", "⚽ Combiné (4 matchs) Feyenoord – AZ…", "11.69", False, "2 924 228 F"),
 ("vip-proof-13.jpg", "🏒 Colorado Avalanche – Toronto Maple Leafs", "8.1", False, "2 835 000 F"),
 ("vip-proof-14.jpg", "⚽ Charlotte – Dallas (Total Charlotte +2.5)", "7.9", False, "2 765 000 F"),
 ("vip-proof-15.jpg", "🏒 Buffalo Sabres – Utah Mammoth", "4.36", True, "2 180 000 F"),
 ("vip-proof-16.jpg", "⚽ Combiné MLS (2 matchs)", "4.16", False, "2 080 000 F"),
 ("vip-proof-17.jpg", "🏒 Colorado – Toronto (1ère période)", "8.1", True, "1 215 000 F"),
 ("vip-proof-07.jpg", "🏒 Dynamo Moscou – Shanghai Dragons", "6.5", False, "6 500 000 F"),
 ("vip-proof-08.jpg", "🏀 U-BT Cluj-Napoca – Reyer Venise", "4.58", False, "4 580 000 F"),
 ("vip-proof-09.jpg", "🏒 Dynamo Moscou – Shanghai Dragons", "8", False, "2 800 000 F"),
 ("vip-proof-10.jpg", "🏒 Combiné KHL (4 matchs)", "10.25", False, "2 564 461 F"),
 ("vip-proof-01.jpg", "⚽ Kazakhstan – Moldavie", "11", True, "2 750 000 F"),
 ("vip-proof-03.jpg", "🏀 Virtus – Maxima Roma", "10.5", False, ""),
 ("vip-proof-04.jpg", "⚽ Almería – Burgos", "8.2", True, ""),
 ("vip-proof-05.jpg", "⚽ Cap-Vert – Rwanda", "7.8", False, ""),
 ("vip-proof-06.jpg", "🏒 Sotchi – Salavat Oufa", "5", False, ""),
]   # prix VIP pour le paiement Mobile Money (a modifier si besoin)
# (operateur, numero affiche, numero a copier, beneficiaire, couleur, logo texte)
MOMO = [
 ("Orange Money", "+237 6 93 56 64 90", "693566490", "FOKAM JEAN MARC", "#ff7900", "OM"),
 ("MTN Mobile Money", "+237 6 79 06 79 38", "679067938", "FOKAM JEAN MARC", "#ffcc00", "MTN"),
 ("Wave", "01 50 18 29 51", "0150182951", "ADADE JEANNE", "#1dc8f2", "W"),
]
# (nom, reseau, adresse, qr, stable, recommande)
CRYPTOS = [
 ("USDT","TRC20 (Tron)","TKqo7hSJK6FfMPfVoeLjXDW7R4FhwsVVcM","vip-usdt-qr.png",True,True),
 ("USDC","Ethereum (ERC20)","0x264cd543f33fc17c9b70a5b8cd64f692b3a002c1","vip-evm-qr.png",True,False),
 ("BTC","Bitcoin","1NThXyzY1ZYCFAoEwwL9Z2PXSojVzMQiio","vip-btc-qr.png",False,False),
 ("ETH","Ethereum (ERC20)","0x264cd543f33fc17c9b70a5b8cd64f692b3a002c1","vip-evm-qr.png",False,False),
 ("BNB","BNB Smart Chain (BEP20)","0x264cd543f33fc17c9b70a5b8cd64f692b3a002c1","vip-evm-qr.png",False,False),
]
VIP_L = {
 "fr": {"proofs_period":'Du 25 au 28 octobre 2026 : 9 tickets gagnants (cotes de 4.03 à 18, dont le Clásico), près de 40 millions F encaissés. Et depuis le 29 septembre : 42 grosses cotes gagnées, dont 11 en live.',"modes_title":'4 façons de jouer avec le VIP',"modes":[('🎯', 'Côte de 2 VIP', 'Tous les jours', 'Un coupon court pour doubler ta mise, avec mon analyse.', 'Risque modéré'), ('🚀', 'Grosses cotes', 'Plusieurs fois par semaine', "Mes combinés à grosse cote : c'est ce que ma communauté adore. On vise gros avec une petite mise.", 'Risque élevé'), ('⚡', 'Live', 'Pendant les matchs', "Je repère les bons moments en direct et je t'envoie le pari au bon moment.", 'Selon le match'), ('🛡️', 'Haute confiance', "Quand l'occasion se présente", 'Mes sélections les plus solides, pour les jours où tu veux jouer plus prudent.', 'Risque plus faible')],"proofs":'Mes grosses cotes passées',"proofs_sub":'Quelques tickets gagnants partagés avec la communauté. Les gains passés ne garantissent pas les gains futurs.',"momo_title":'Payer par Mobile Money (Orange Money, MTN, Wave)',"momo_sub":"Envoie le montant de ta formule ({xaf}) sur l'un de ces numéros :","momo_name":'Bénéficiaire',"momo_amount":'Montant',"momo_copy":'Copier le numéro',"momo_tip":'Avant de valider, vérifie que le nom affiché correspond au bénéficiaire indiqué : FOKAM JEAN MARC pour Orange Money et MTN, ADADE JEANNE pour Wave.',"crypto_title":'Ou payer en crypto (tous pays)',"title":"VIP Cousin Marc : mes meilleurs coupons en avant-première (25 000 FCFA/mois)",
  "desc":"Le VIP Cousin Marc : coupons exclusifs chaque jour, analyses complètes et canal privé. 25 000 FCFA par mois, 65 000 FCFA les 3 mois ou 240 000 FCFA l'année. Paiement Mobile Money (Orange, MTN, Wave) ou crypto.",
  "eyebrow":"Accès VIP · 25 000 FCFA / mois",
  "h1":"Mes meilleurs coupons, <em>avant tout le monde.</em>",
  "sub":"Sur les canaux gratuits, tu vois une partie de mon travail. Dans le VIP, tu reçois tout : les coupons exclusifs, mes analyses complètes et un accès direct à moi.",
  "cta":"Rejoindre le VIP · 25 000 FCFA", "cta2":"Ce que tu reçois",
  "perday":"<b>25 000 FCFA le mois</b>, ou <b>240 000 FCFA l'année</b> : moins de <b>700 FCFA par jour</b>",
  "trust":[("95K+","personnes suivent Cousin Marc"),("3","formules au choix"),("0","renouvellement automatique")],
  "cmp_title":"Gratuit ou VIP : la différence", "cmp_free":"Gratuit", "cmp_vip":"VIP",
  "cmp_rows":[('Coupon du jour gratuit (côte de 2)', '✓', '✓'), ('Côte de 2 VIP tous les jours', '—', '✓'), ('Grosses cotes (combinés)', '—', '✓'), ('Pronostics en live', '—', '✓'), ('Sélections haute confiance', '—', '✓'), ('Analyse complète de chaque sélection', 'Résumé', '✓'), ('Canal privé + questions directes', '—', '✓')],
  "how_title":"Comment ça se passe dans le VIP",
  "how":[("📲","Les coupons arrivent dans le canal privé","Chaque jour de match, je publie mes sélections VIP dans le canal Telegram réservé aux membres, avant les matchs."),
         ("🧠","Chaque choix est expliqué","Tu sais pourquoi je joue ce match, quelle cote viser et combien de risque il y a. Tu apprends à parier mieux, pas juste à copier."),
         ("💬","Tu peux me poser tes questions","Un doute sur un ticket, une cote qui a bougé ? Tu m'écris directement dans le canal privé.")],
  "price_title":"Choisis ta formule", "price_label":"Inclus dans toutes les formules", "per_month":"/ mois", "plan_cta":"Choisir", "plans":{"m1":("1 mois",""),"m3":("3 mois","Économise 10 000 FCFA"),"y1":("1 an","Économise 60 000 FCFA")}, "best":"Meilleure offre",
  "price_list":['Côte de 2 VIP tous les jours', 'Grosses cotes pour viser gros (petite mise)', 'Pronostics en live pendant les matchs', 'Sélections haute confiance', 'Analyses complètes + canal privé', "Paiement unique : pas d'abonnement caché"],
  "price_cta":"Payer maintenant ↓",
  "pay_title":"Payer en 2 minutes", "choose":"Choisis ta crypto et envoie le montant de ta formule (42 $, 108 $ ou 400 $) :",
  "steps":["Choisis ta formule et envoie le montant par Orange Money, MTN ou Wave (en FCFA), ou en crypto (en $).","Fais une capture d'écran de ton paiement.","Envoie-moi la capture sur Telegram en précisant ta formule : je vérifie et je t'ajoute au canal VIP."],
  "copy":"Copier l'adresse","copied":"✓ Copiée","reco":"Recommandé · stable",
  "vol_note":"Cours variable : envoie l'équivalent en $ de ta formule.",
  "warn_net":"Envoie UNIQUEMENT via le réseau","warn_lost":"Un autre réseau = fonds perdus.",
  "tg_btn":"✈ J'ai payé : j'envoie ma preuve",
  "after":"Je vérifie chaque paiement moi-même avant de t'ajouter au canal VIP.",
  "faq_title":"Questions fréquentes",
  "faq":[("Comment je reçois mon accès ?","Après ton paiement, envoie la capture d'écran sur Telegram avec le bouton ci-dessus. Dès que j'ai vérifié le paiement, je t'ajoute au canal VIP privé."),
         ("Je n'ai jamais acheté de crypto, je fais comment ?","Le plus simple est l'USDT sur le réseau TRC20. Tu peux en acheter avec Mobile Money sur une plateforme d'échange (par exemple en P2P), puis l'envoyer à l'adresse USDT indiquée. Si tu bloques, écris-moi sur Telegram avant de payer."),
         ("L'abonnement se renouvelle tout seul ?","Non. Tu paies une seule fois pour la durée choisie (1, 3 ou 12 mois). Rien n'est prélevé ensuite : à la fin, tu choisis de continuer ou non."),
         ("Les gains sont-ils garantis ?","Non, et personne d'honnête ne peut te le promettre. Je partage mes meilleures analyses et je t'explique chaque choix, mais le pari reste un risque. Mise toujours raisonnablement.")],
  "final_title":"Prêt à passer au niveau supérieur ?", "final_sub":"Rejoins le canal privé et reçois mes coupons VIP dès demain.",
  "disc":"18+ · Les paris comportent des risques : aucun gain n'est garanti. Ne mise que ce que tu peux te permettre de perdre."},
 "en": {"proofs_period":'From 25 to 28 October 2026: 9 winning tickets (odds from 4.03 to 18, including El Clásico), almost 40 million F cashed out. And since 29 September: 42 big odds won, 11 of them live.',"modes_title":'4 ways to play with the VIP',"modes":[('🎯', 'VIP odds of 2', 'Every day', 'A short coupon to double your stake, with my analysis.', 'Moderate risk'), ('🚀', 'Big odds', 'Several times a week', 'My big-odds accumulators: what my community loves most. Aim high with a small stake.', 'High risk'), ('⚡', 'Live', 'During matches', 'I spot the right moments live and send you the bet at the right time.', 'Depends on the match'), ('🛡️', 'High confidence', 'When the chance comes', 'My most solid picks, for the days you want to play it safer.', 'Lower risk')],"proofs":'My past big odds',"proofs_sub":"A few winning tickets shared with the community. Past wins don't guarantee future wins.","momo_title":'Pay with Mobile Money (Orange Money, MTN, Wave)',"momo_sub":'Send your plan amount ({xaf}) to one of these numbers:',"momo_name":'Recipient',"momo_amount":'Amount',"momo_copy":'Copy number',"momo_tip":'Before confirming, check that the name shown matches the recipient: FOKAM JEAN MARC for Orange Money and MTN, ADADE JEANNE for Wave.',"crypto_title":'Or pay with crypto (all countries)',"title":"Cousin Marc VIP: my best coupons, before everyone else (25,000 FCFA/month)",
  "desc":"Cousin Marc VIP: exclusive coupons every day, full analysis and a private channel. 25,000 FCFA a month, 65,000 FCFA for 3 months or 240,000 FCFA a year. Mobile Money (Orange, MTN, Wave) or crypto payment.",
  "eyebrow":"VIP access · 25,000 FCFA / month",
  "h1":"My best coupons, <em>before everyone else.</em>",
  "sub":"On the free channels you see part of my work. In the VIP you get everything: exclusive coupons, my full analysis and direct access to me.",
  "cta":"Join the VIP · 25,000 FCFA", "cta2":"What you get",
  "perday":"<b>25,000 FCFA a month</b>, or <b>240,000 FCFA a year</b>: less than <b>700 FCFA a day</b>",
  "trust":[("95K+","people follow Cousin Marc"),("3","plans to choose from"),("0","automatic renewal")],
  "cmp_title":"Free vs VIP: the difference", "cmp_free":"Free", "cmp_vip":"VIP",
  "cmp_rows":[('Free daily coupon (odds of 2)', '✓', '✓'), ('VIP odds of 2 every day', '—', '✓'), ('Big odds (accumulators)', '—', '✓'), ('Live tips', '—', '✓'), ('High-confidence picks', '—', '✓'), ('Full analysis of each pick', 'Summary', '✓'), ('Private channel + direct questions', '—', '✓')],
  "how_title":"How the VIP works",
  "how":[("📲","Coupons land in the private channel","On every match day I post my VIP picks in the members-only Telegram channel, before kick-off."),
         ("🧠","Every pick is explained","You know why I play a match, which odds to target and how much risk there is. You learn to bet better, not just copy."),
         ("💬","You can ask me questions","Unsure about a ticket or the odds moved? Message me directly in the private channel.")],
  "price_title":"Choose your plan", "price_label":"Included in every plan", "per_month":"/ month", "plan_cta":"Choose", "plans":{"m1":("1 month",""),"m3":("3 months","Save 10,000 FCFA"),"y1":("1 year","Save 60,000 FCFA")}, "best":"Best value",
  "price_list":['VIP odds of 2 every day', 'Big odds to aim high (small stake)', 'Live tips during matches', 'High-confidence picks', 'Full analysis + private channel', 'One-time payment: no hidden subscription'],
  "price_cta":"Pay now ↓",
  "pay_title":"Pay in 2 minutes", "choose":"Choose your crypto and send your plan amount (42 $, 108 $ or 400 $):",
  "steps":["Choose your plan and send the amount via Orange Money, MTN or Wave (in FCFA), or in crypto (in $).","Take a screenshot of your payment.","Send me the screenshot on Telegram with your plan: I check it and add you to the VIP channel."],
  "copy":"Copy address","copied":"✓ Copied","reco":"Recommended · stable",
  "vol_note":"Variable rate: send the $ equivalent of your plan.",
  "warn_net":"Send ONLY via the network","warn_lost":"Any other network = lost funds.",
  "tg_btn":"✈ I've paid: send my proof",
  "after":"I check every payment myself before adding you to the VIP channel.",
  "faq_title":"FAQ",
  "faq":[("How do I get access?","After paying, send the screenshot on Telegram using the button above. As soon as I've checked the payment, I add you to the private VIP channel."),
         ("I've never bought crypto, what do I do?","The easiest is USDT on the TRC20 network. You can buy it with Mobile Money on an exchange (for example via P2P), then send it to the USDT address shown. If you get stuck, message me on Telegram before paying."),
         ("Does it renew automatically?","No. You pay once for the period you choose (1, 3 or 12 months). Nothing is charged afterwards: at the end, you decide whether to continue."),
         ("Are wins guaranteed?","No, and nobody honest can promise that. I share my best analysis and explain every pick, but betting is always a risk. Always stake responsibly.")],
  "final_title":"Ready to level up?", "final_sub":"Join the private channel and get my VIP coupons from tomorrow.",
  "disc":"18+ · Betting involves risk: no win is guaranteed. Only stake what you can afford to lose."},
 "es": {"proofs_period":'Del 25 al 28 de octubre de 2026: 9 tickets ganadores (cuotas de 4.03 a 18, incluido el Clásico), casi 40 millones F cobrados. Y desde el 29 de septiembre: 42 cuotas altas ganadas, 11 de ellas en vivo.',"modes_title":'4 formas de jugar con el VIP',"modes":[('🎯', 'Cuota de 2 VIP', 'Todos los días', 'Un cupón corto para duplicar tu apuesta, con mi análisis.', 'Riesgo moderado'), ('🚀', 'Cuotas altas', 'Varias veces por semana', 'Mis combinadas de cuota alta: lo que más gusta a mi comunidad. Apunta alto con poca apuesta.', 'Riesgo alto'), ('⚡', 'En vivo', 'Durante los partidos', 'Detecto los buenos momentos en directo y te envío la apuesta a tiempo.', 'Según el partido'), ('🛡️', 'Alta confianza', 'Cuando surge la ocasión', 'Mis selecciones más sólidas, para los días en que quieres jugar más prudente.', 'Riesgo menor')],"proofs":'Mis cuotas altas pasadas',"proofs_sub":'Algunos tickets ganadores compartidos con la comunidad. Las ganancias pasadas no garantizan las futuras.',"momo_title":'Pagar con Mobile Money (Orange Money, MTN, Wave)',"momo_sub":'Envía el importe de tu plan ({xaf}) a uno de estos números:',"momo_name":'Beneficiario',"momo_amount":'Importe',"momo_copy":'Copiar número',"momo_tip":'Antes de confirmar, comprueba que el nombre coincide con el beneficiario: FOKAM JEAN MARC para Orange Money y MTN, ADADE JEANNE para Wave.',"crypto_title":'O pagar en cripto (todos los países)',"title":"VIP Cousin Marc: mis mejores cupones, antes que nadie (25 000 FCFA/mes)",
  "desc":"VIP Cousin Marc: cupones exclusivos cada día, análisis completos y canal privado. 25 000 FCFA al mes, 65 000 FCFA por 3 meses o 240 000 FCFA al año. Pago por Mobile Money (Orange, MTN, Wave) o cripto.",
  "eyebrow":"Acceso VIP · 25 000 FCFA / mes",
  "h1":"Mis mejores cupones, <em>antes que nadie.</em>",
  "sub":"En los canales gratuitos ves una parte de mi trabajo. En el VIP lo recibes todo: cupones exclusivos, mis análisis completos y acceso directo a mí.",
  "cta":"Unirme al VIP · 25 000 FCFA", "cta2":"Qué recibes",
  "perday":"<b>25 000 FCFA al mes</b>, o <b>240 000 FCFA al año</b>: menos de <b>700 FCFA al día</b>",
  "trust":[("95K+","personas siguen a Cousin Marc"),("3","planes a elegir"),("0","renovación automática")],
  "cmp_title":"Gratis o VIP: la diferencia", "cmp_free":"Gratis", "cmp_vip":"VIP",
  "cmp_rows":[('Cupón diario gratis (cuota de 2)', '✓', '✓'), ('Cuota de 2 VIP todos los días', '—', '✓'), ('Cuotas altas (combinadas)', '—', '✓'), ('Pronósticos en vivo', '—', '✓'), ('Selecciones de alta confianza', '—', '✓'), ('Análisis completo de cada selección', 'Resumen', '✓'), ('Canal privado + preguntas directas', '—', '✓')],
  "how_title":"Cómo funciona el VIP",
  "how":[("📲","Los cupones llegan al canal privado","Cada día de partido publico mis selecciones VIP en el canal de Telegram exclusivo para miembros, antes de los partidos."),
         ("🧠","Cada elección está explicada","Sabes por qué juego ese partido, qué cuota buscar y cuánto riesgo hay. Aprendes a apostar mejor, no solo a copiar."),
         ("💬","Puedes hacerme preguntas","¿Dudas con un ticket o la cuota cambió? Escríbeme directamente en el canal privado.")],
  "price_title":"Elige tu plan", "price_label":"Incluido en todos los planes", "per_month":"/ mes", "plan_cta":"Elegir", "plans":{"m1":("1 mes",""),"m3":("3 meses","Ahorra 10 000 FCFA"),"y1":("1 año","Ahorra 60 000 FCFA")}, "best":"Mejor oferta",
  "price_list":['Cuota de 2 VIP todos los días', 'Cuotas altas para apuntar alto (apuesta pequeña)', 'Pronósticos en vivo durante los partidos', 'Selecciones de alta confianza', 'Análisis completos + canal privado', 'Pago único: sin suscripción oculta'],
  "price_cta":"Pagar ahora ↓",
  "pay_title":"Paga en 2 minutos", "choose":"Elige tu cripto y envía el importe de tu plan (42 $, 108 $ o 400 $):",
  "steps":["Elige tu plan y envía el importe por Orange Money, MTN o Wave (en FCFA), o en cripto (en $).","Haz una captura de pantalla de tu pago.","Envíame la captura por Telegram indicando tu plan: la verifico y te añado al canal VIP."],
  "copy":"Copiar dirección","copied":"✓ Copiada","reco":"Recomendado · estable",
  "vol_note":"Cotización variable: envía el equivalente en $ de tu plan.",
  "warn_net":"Envía SOLO por la red","warn_lost":"Otra red = fondos perdidos.",
  "tg_btn":"✈ Ya pagué: envío mi comprobante",
  "after":"Verifico cada pago personalmente antes de añadirte al canal VIP.",
  "faq_title":"Preguntas frecuentes",
  "faq":[("¿Cómo recibo mi acceso?","Después de pagar, envía la captura por Telegram con el botón de arriba. En cuanto verifico el pago, te añado al canal VIP privado."),
         ("Nunca he comprado cripto, ¿qué hago?","Lo más sencillo es USDT en la red TRC20. Puedes comprarlo con Mobile Money en una plataforma de intercambio (por ejemplo en P2P) y enviarlo a la dirección USDT indicada. Si te bloqueas, escríbeme por Telegram antes de pagar."),
         ("¿Se renueva automáticamente?","No. Pagas una sola vez por el periodo elegido (1, 3 o 12 meses). No se cobra nada después: al final decides si continúas."),
         ("¿Las ganancias están garantizadas?","No, y nadie honesto puede prometerlo. Comparto mis mejores análisis y explico cada elección, pero apostar siempre es un riesgo. Apuesta con responsabilidad.")],
  "final_title":"¿Listo para subir de nivel?", "final_sub":"Únete al canal privado y recibe mis cupones VIP desde mañana.",
  "disc":"18+ · Las apuestas conllevan riesgo: ninguna ganancia está garantizada. Apuesta solo lo que puedas permitirte perder."},
 "ar": {"proofs_period":'من 25 إلى 28 أكتوبر 2026: 9 تذاكر رابحة (نسب من 4.03 إلى 18، منها الكلاسيكو)، وما يقارب 40 مليون F من الأرباح. ومنذ 29 سبتمبر: 42 نسبة كبيرة رابحة، منها 11 مباشرة.',"modes_title":'4 طرق للعب مع VIP',"modes":[('🎯', 'رهان بضعف 2 VIP', 'يوميًا', 'قسيمة قصيرة لمضاعفة رهانك مع تحليلي.', 'مخاطرة متوسطة'), ('🚀', 'نسب كبيرة', 'عدة مرات أسبوعيًا', 'رهاناتي المركبة ذات النسب الكبيرة: ما يحبه مجتمعي أكثر. استهدف ربحًا كبيرًا برهان صغير.', 'مخاطرة عالية'), ('⚡', 'مباشر (لايف)', 'أثناء المباريات', 'ألتقط اللحظات المناسبة مباشرة وأرسل لك الرهان في الوقت المناسب.', 'حسب المباراة'), ('🛡️', 'ثقة عالية', 'عند توفر الفرصة', 'أكثر اختياراتي ثباتًا، للأيام التي تريد فيها اللعب بحذر أكبر.', 'مخاطرة أقل')],"proofs":'نسبي الكبيرة السابقة',"proofs_sub":'بعض التذاكر الرابحة التي شاركتها مع المجتمع. الأرباح السابقة لا تضمن الأرباح المستقبلية.',"momo_title":'الدفع عبر Mobile Money (Orange Money وMTN وWave)',"momo_sub":'أرسل مبلغ خطتك ({xaf}) إلى أحد هذه الأرقام:',"momo_name":'المستفيد',"momo_amount":'المبلغ',"momo_copy":'نسخ الرقم',"momo_tip":'قبل التأكيد، تحقق من أن الاسم يطابق المستفيد: FOKAM JEAN MARC لـ Orange Money وMTN، وADADE JEANNE لـ Wave.',"crypto_title":'أو الدفع بالعملات الرقمية (كل الدول)',"title":"VIP Cousin Marc: أفضل قسائمي قبل الجميع (25 000 فرنك شهريًا)",
  "desc":"VIP Cousin Marc: قسائم حصرية يوميًا وتحليلات كاملة وقناة خاصة. 25 000 فرنك شهريًا، 65 000 فرنك لـ 3 أشهر أو 240 000 فرنك للسنة. الدفع عبر Mobile Money (Orange وMTN وWave) أو بالعملات الرقمية.",
  "eyebrow":"اشتراك VIP · 25 000 فرنك شهريًا",
  "h1":"أفضل قسائمي، <em>قبل الجميع.</em>",
  "sub":"في القنوات المجانية ترى جزءًا من عملي. في VIP تحصل على كل شيء: القسائم الحصرية وتحليلاتي الكاملة وتواصل مباشر معي.",
  "cta":"انضم إلى VIP · 25 000 فرنك", "cta2":"ماذا تحصل عليه",
  "perday":"<b>25 000 فرنك شهريًا</b>، أو <b>240 000 فرنك للسنة</b>: أقل من <b>700 فرنك في اليوم</b>",
  "trust":[("95K+","شخص يتابعون Cousin Marc"),("3","خطط للاختيار"),("0","تجديد تلقائي")],
  "cmp_title":"مجاني أم VIP: الفرق", "cmp_free":"مجاني", "cmp_vip":"VIP",
  "cmp_rows":[('قسيمة يومية مجانية (رهان بضعف 2)', '✓', '✓'), ('رهان بضعف 2 VIP يوميًا', '—', '✓'), ('نسب كبيرة (رهانات مركبة)', '—', '✓'), ('توقعات مباشرة (لايف)', '—', '✓'), ('اختيارات عالية الثقة', '—', '✓'), ('تحليل كامل لكل اختيار', 'ملخص', '✓'), ('قناة خاصة + أسئلة مباشرة', '—', '✓')],
  "how_title":"كيف يعمل VIP",
  "how":[("📲","القسائم تصل إلى القناة الخاصة","في كل يوم مباريات أنشر اختياراتي VIP في قناة تيليغرام المخصصة للأعضاء قبل المباريات."),
         ("🧠","كل اختيار مشروح","تعرف لماذا أختار المباراة وما الاحتمال المستهدف وحجم المخاطرة. تتعلم المراهنة بشكل أفضل، لا مجرد النسخ."),
         ("💬","يمكنك طرح أسئلتك","لديك شك في تذكرة أو تغيرت النسبة؟ راسلني مباشرة في القناة الخاصة.")],
  "price_title":"اختر خطتك", "price_label":"مشمول في كل الخطط", "per_month":"/ شهر", "plan_cta":"اختيار", "plans":{"m1":("شهر واحد",""),"m3":("3 أشهر","وفّر 10 000 فرنك"),"y1":("سنة","وفّر 60 000 فرنك")}, "best":"أفضل عرض",
  "price_list":['رهان بضعف 2 VIP يوميًا', 'نسب كبيرة لأرباح أكبر (رهان صغير)', 'توقعات مباشرة أثناء المباريات', 'اختيارات عالية الثقة', 'تحليلات كاملة + قناة خاصة', 'دفعة واحدة: بدون اشتراك مخفي'],
  "price_cta":"ادفع الآن ↓",
  "pay_title":"ادفع في دقيقتين", "choose":"اختر عملتك وأرسل مبلغ خطتك (42 $ أو 108 $ أو 400 $):",
  "steps":["اختر خطتك وأرسل المبلغ عبر Orange Money أو MTN أو Wave (بالفرنك) أو بالعملات الرقمية (بالدولار).","التقط لقطة شاشة لعملية الدفع.","أرسل لي اللقطة عبر تيليغرام مع ذكر خطتك: أتحقق منها وأضيفك إلى قناة VIP."],
  "copy":"نسخ العنوان","copied":"✓ تم النسخ","reco":"موصى به · مستقر",
  "vol_note":"السعر متغير: أرسل ما يعادل خطتك بالدولار.",
  "warn_net":"أرسل فقط عبر شبكة","warn_lost":"أي شبكة أخرى = ضياع الأموال.",
  "tg_btn":"✈ دفعت: أرسل الإثبات",
  "after":"أتحقق من كل دفعة بنفسي قبل إضافتك إلى قناة VIP.",
  "faq_title":"أسئلة شائعة",
  "faq":[("كيف أحصل على الوصول؟","بعد الدفع، أرسل لقطة الشاشة عبر تيليغرام بالزر أعلاه. بمجرد التحقق من الدفع، أضيفك إلى قناة VIP الخاصة."),
         ("لم أشترِ عملات رقمية من قبل، ماذا أفعل؟","الأسهل هو USDT على شبكة TRC20. يمكنك شراؤه عبر Mobile Money على منصة تداول (مثلًا عبر P2P) ثم إرساله إلى عنوان USDT المعروض. إذا واجهت مشكلة، راسلني على تيليغرام قبل الدفع."),
         ("هل يتجدد الاشتراك تلقائيًا؟","لا. تدفع مرة واحدة للمدة التي تختارها (1 أو 3 أو 12 شهرًا). لا يُقتطع أي شيء بعد ذلك: في النهاية تقرر المتابعة أو لا."),
         ("هل الأرباح مضمونة؟","لا، ولا يمكن لأي شخص صادق أن يعدك بذلك. أشارك أفضل تحليلاتي وأشرح كل اختيار، لكن المراهنة تبقى مخاطرة. راهن دائمًا بمسؤولية.")],
  "final_title":"جاهز للمستوى التالي؟", "final_sub":"انضم إلى القناة الخاصة واحصل على قسائم VIP بدءًا من الغد.",
  "disc":"+18 · المراهنات تنطوي على مخاطر: لا يوجد ربح مضمون. راهن فقط بما يمكنك تحمّل خسارته."},
}
def vip_page(lang):
    L=VIP_L[lang]; slug=VIP_SLUG[lang]; canonical=f"{BASE}/{slug}"
    navmap={"fr":nav_fr(en=VIP_SLUG["en"],es=VIP_SLUG["es"],ar=VIP_SLUG["ar"]),
            "en":nav_en(fr=VIP_SLUG["fr"],es=VIP_SLUG["es"],ar=VIP_SLUG["ar"]),
            "es":nav_es(fr=VIP_SLUG["fr"],en=VIP_SLUG["en"],ar=VIP_SLUG["ar"]),
            "ar":nav_ar(fr=VIP_SLUG["fr"],en=VIP_SLUG["en"],es=VIP_SLUG["es"])}
    footmap={"fr":footer_html,"en":footer_html_en,"es":footer_html_es,"ar":footer_html_ar}
    alternates=(f"{BASE}/{VIP_SLUG['fr']}",f"{BASE}/{VIP_SLUG['en']}",f"{BASE}/{VIP_SLUG['es']}",f"{BASE}/{VIP_SLUG['ar']}")
    trust="".join(f'<div><b>{v}</b>{t}</div>' for v,t in L["trust"])
    rows="".join(f'<tr><td>{a}</td><td class="{"no" if f=="—" else ""}">{f}</td><td class="yes">{v}</td></tr>' for a,f,v in L["cmp_rows"])
    modes="".join(f'<div class="vmode"><div class="vmode-h"><span class="fi">{i}</span><div><b>{t}</b><small>{f}</small></div></div><p>{d}</p><span class="vrisk">{r}</span></div>' for i,t,f,d,r in L["modes"])
    proofs=""
    if VIP_PROOFS:
        imgs="".join(
            f'<figure class="vproof-card"><img src="{f}" alt="{m} — @{c} — Cousin Marc" loading="lazy">'
            f'<figcaption><span>{m}</span><b>@{c}</b>{"<em>LIVE</em>" if live else ""}{f"<strong>✅ {paid}</strong>" if paid else ""}</figcaption></figure>'
            for f,m,c,live,paid in VIP_PROOFS)
        proofs=(f'<section id="preuves"><h2>{L["proofs"]}</h2><p class="vproof-period">{L["proofs_period"]}</p>'
                f'<div class="vproofs">{imgs}</div><p class="muted" style="font-size:13px;margin-top:12px">{L["proofs_sub"]}</p></section>' + '<script>(function(){var R="https://raw.githubusercontent.com/fokamjeanmarc2004-cloud/marc-pronostic-api/main/promo/preuves/";var g=document.querySelector(".vproofs");if(!g||!window.fetch)return;fetch(R+"preuves.json",{cache:"no-store"}).then(function(r){return r.json()}).then(function(l){l.filter(function(p){return /^tg-/.test(p.file)}).slice(0,30).reverse().forEach(function(p){var f=document.createElement("figure");f.className="vproof-card";var i=document.createElement("img");i.src=R+p.file;i.loading="lazy";i.alt=(p.titre||"")+" - Cousin Marc";var c=document.createElement("figcaption");var s=document.createElement("span");s.textContent=(p.titre||"").replace(/^[^\w(]+/,"");c.appendChild(s);if(p.cote){var b=document.createElement("b");b.textContent="@"+p.cote;c.appendChild(b)}if(p.gain){var t=document.createElement("strong");t.textContent="✅ "+p.gain;c.appendChild(t)}f.appendChild(i);f.appendChild(c);g.insertBefore(f,g.firstChild)})}).catch(function(){})})();</script>')
    how="".join(f'<div class="vstep"><span class="fi">{i}</span><div><b>{t}</b><p>{d}</p></div></div>' for i,t,d in L["how"])
    plist="".join(f'<li>{x}</li>' for x in L["price_list"])
    plans=""
    for key,usd,xaf,pm,best in VIP_PLANS:
        name,save=L["plans"][key]
        badge='<span class="vbest">⭐ '+L["best"]+'</span>' if best else ''
        save_html='<p class="vp-save">'+(save or '&nbsp;')+'</p>'
        cls=' best' if best else ''
        btn='' if best else ' alt'
        plans+=(f'<div class="vplan{cls}">{badge}'
                f'<p class="vp-name">{name}</p><div class="vp-price">{xaf}</div><p class="vp-xaf">{usd} (crypto)</p>'
                f'<p class="vp-pm">{pm} {L["per_month"]}</p>{save_html}'
                f'<a class="cta{btn}" href="#paiement">{L["plan_cta"]}</a></div>')
    steps="".join(f'<li>{x}</li>' for x in L["steps"])
    faq="".join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i,(q,a) in enumerate(L["faq"]))
    faq_ld=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in L["faq"]]},ensure_ascii=False)
    momo=""
    for op,disp,raw,holder,col,short in MOMO:
        momo+=(f'<div class="vmomo"><div class="vm-head"><span class="vm-logo" style="background:{col}">{short}</span><b>{op}</b></div>'
               f'<div class="vm-num" translate="no">{disp}</div>'
               f'<div class="vm-row"><span>{L["momo_name"]}</span><b translate="no">{holder}</b></div>'
               f'<div class="vm-row"><span>{L["momo_amount"]}</span><b>{VIP_PRICE_XAF}</b></div>'
               f'<button type="button" class="vcopy" onclick="try{{navigator.clipboard.writeText(\'{raw}\');this.textContent=\'{L["copied"]}\';}}catch(e){{}}">{L["momo_copy"]}</button></div>')
    cards=""
    for name,net,addr,qr,stable,reco in CRYPTOS:
        badge=f'<span class="vbadge">⭐ {L["reco"]}</span>' if reco else ''
        note=f'<p class="vvol">{L["vol_note"]}</p>' if not stable else ''
        cards+=(f'<div class="vcrypto{" reco" if reco else ""}"><div class="vc-head"><b>{name}</b><span>{net}</span>{badge}</div>{note}'
                f'<img src="{qr}" alt="QR {name} Cousin Marc VIP" width="164" height="164" loading="lazy">'
                f'<div class="vaddr" translate="no">{addr}</div>'
                f'<button type="button" class="vcopy" onclick="try{{navigator.clipboard.writeText(\'{addr}\');this.textContent=\'{L["copied"]}\';}}catch(e){{}}">{L["copy"]}</button>'
                f'<p class="vwarn">⚠️ {L["warn_net"]} <b>{net}</b>. {L["warn_lost"]}</p></div>')
    body=f'''
<header class="vhero"><div class="wrap">
<p class="eyebrow">⭐ {L["eyebrow"]}</p>
<h1>{L["h1"]}</h1>
<p class="lead">{L["sub"]}</p>
<div class="btnrow"><a class="cta" href="#paiement">{L["cta"]}</a><a class="cta alt" href="#preuves">{L["proofs"]}</a></div>
<p class="vperday">{L["perday"]}</p>
<div class="home-trust">{trust}</div>
</div></header>
<main class="wrap">
<section id="contenu">
<h2>{L["cmp_title"]}</h2>
<div class="tablecard vcmp"><table><thead><tr><th></th><th>{L["cmp_free"]}</th><th>⭐ {L["cmp_vip"]}</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
{proofs}
<section>
<h2>{L["modes_title"]}</h2>
<div class="vmodes">{modes}</div>
</section>
<section>
<h2>{L["how_title"]}</h2>
<div class="vsteps">{how}</div>
</section>
<section>
<h2>{L["price_title"]}</h2>
<div class="vplans">{plans}</div>
<div class="vincluded"><p class="label">{L["price_label"]}</p><ul>{plist}</ul></div>
</section>
<section id="paiement">
<h2>{L["pay_title"]}</h2>
<ol class="steps">{steps}</ol>
<h3 class="vpay-h">📱 {L["momo_title"]}</h3>
<p class="muted" style="margin:6px 0 12px">{L["momo_sub"].replace("{xaf}", "<b>" + VIP_PRICE_XAF + "</b>")}</p>
<div class="vmomos">{momo}</div>
<p class="vwarn" style="margin-top:12px">✅ {L["momo_tip"]}</p>
<h3 class="vpay-h" style="margin-top:30px">💰 {L["crypto_title"]}</h3>
<p class="muted" style="margin:6px 0 12px">{L["choose"]}</p>
<div class="vcryptos">{cards}</div>
<div class="vproof"><a class="cta" href="{VIP_TG}" target="_blank" rel="nofollow">{L["tg_btn"]}</a><p>{L["after"]}</p></div>
</section>
<section>
<h2>{L["faq_title"]}</h2>
{faq}
</section>
</main>
<div class="wrap"><div class="tgband"><div><h2>{L["final_title"]}</h2><p>{L["final_sub"]}</p></div>
<a class="cta" href="#paiement">{L["cta"]}</a></div></div>
<div class="wrap"><p class="note" style="margin-top:28px">{L["disc"]}</p></div>
{footmap[lang]()}
</body></html>'''
    return head(L["title"], L["desc"], canonical, extra=f'<script type="application/ld+json">{faq_ld}</script>', nav=navmap[lang], lang=lang, alternates=alternates) + body

def sitemap():
    pages = ["", "promo-codes.html", "codigos-promocionales.html", "promo-codes-ar.html",
             "cote-de-2.html", "odds-of-2.html", "cuota-de-2.html", "cote-2-ar.html",
             "pronostics.html", "predictions.html", "pronosticos.html", "pronostics-ar.html",
             "actualites.html", "news.html", "noticias.html", "actualites-ar.html",
             "a-propos.html", "about.html", "acerca-de.html", "a-propos-ar.html",
             "jeu-responsable.html", "responsible-gambling.html", "juego-responsable.html", "jeu-responsable-ar.html",
             TPI_SLUG["fr"], TPI_SLUG["en"], TPI_SLUG["es"], TPI_SLUG["ar"],
             RESULTS_SLUG["fr"], RESULTS_SLUG["en"], RESULTS_SLUG["es"], RESULTS_SLUG["ar"], VIP_SLUG["fr"], VIP_SLUG["en"], VIP_SLUG["es"], VIP_SLUG["ar"]] \
            + [f"{b['slug']}.html" for b in BOOKMAKERS] + [f"{en_slug(b)}.html" for b in BOOKMAKERS] + [f"{es_slug(b)}.html" for b in BOOKMAKERS] + [f"{ar_slug(b)}.html" for b in BOOKMAKERS] \
            + [f"{a['slug']}.html" for a in ARTICLES] + [f"{a['slug']}.html" for a in ARTICLES_EN] + [f"{a['slug']}.html" for a in ARTICLES_ES] + [f"{a['slug']}.html" for a in ARTICLES_AR] \
            + [f"{cty_hub_slug(c)}.html" for c in COUNTRIES] \
            + [f"{cty_bk_slug(_bk(s), c)}.html" for c in COUNTRIES for s in c["books"] if (s, c["slug"]) in KEEP_COUNTRY_BK] \
            + [COMPARE_SLUG, HELP_SLUG, "affiche.html"] + [m["slug"] + ".html" for m in MATCHS]
    items = "\n".join(f"  <url><loc>{BASE}/{p}</loc><changefreq>weekly</changefreq></url>" for p in pages)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>'

def article_jsonld(a):
    canonical=f"{BASE}/{a['slug']}.html"
    data={"@context":"https://schema.org","@type":"Article","headline":a["title"],
          "datePublished":a["date_iso"],"dateModified":a["date_iso"],
          "author":{"@type":"Person","name":"Cousin Marc"},
          "publisher":{"@type":"Organization","name":"Cousin Marc Pronostic"},
          "mainEntityOfPage":canonical}
    return json.dumps(data,ensure_ascii=False,indent=2)

def article_cta(a):
    if a.get("cta_slug"):
        return f'<section style="text-align:center;border-bottom:none"><h2 style="justify-content:center">Passe à l\'action</h2><div class="btnrow" style="margin-top:18px"><a class="cta" href="{a["cta_slug"]}.html">{a["cta_label"]}</a></div></section>'
    return '<section style="text-align:center;border-bottom:none"><h2 style="justify-content:center">Mes pronos du jour</h2><p style="max-width:480px;margin:10px auto 0">Retrouve mes pronostics en direct sur Telegram et WhatsApp.</p><div class="btnrow" style="margin-top:18px"><a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a><a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 WhatsApp</a></div></section>'

def article_page(a):
    canonical=f"{BASE}/{a['slug']}.html"
    extra=f'<script type="application/ld+json">\n{article_jsonld(a)}\n</script>'
    return head(f"{a['title']} | Cousin Marc Pronostic", a["desc"], canonical, extra, nav=nav_fr(en=f"{ARTICLE_FR2EN[a['slug']]}.html", es=f"{ARTICLE_FR2ES[a['slug']]}.html", ar=f"{ARTICLE_FR2AR[a['slug']]}.html"), alternates=(canonical, f"{BASE}/{ARTICLE_FR2EN[a['slug']]}.html", f"{BASE}/{ARTICLE_FR2ES[a['slug']]}.html", f"{BASE}/{ARTICLE_FR2AR[a['slug']]}.html"))+f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Actualités · {a['date_fr']}</p>
<h1>{a['title']}</h1>
</div></header>
<main class="wrap article">
{a['body']}
<section style="border-bottom:none">
<h3>À propos de l'auteur</h3>
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">Pronostiqueur foot · communauté de 95 000+ abonnés</div></div></div>
<div class="social" style="margin-top:16px">{social_html()}</div>
</section>
{article_cta(a)}
</main>
{footer_html()}
</body></html>"""

def actualites_page():
    cards=""
    for a in sorted(ARTICLES,key=lambda x:x["date_iso"],reverse=True):
        cards+=f'<a class="postcard" href="{a["slug"]}.html"><div class="date">{a["date_fr"]}</div><div class="pt">{a["title"]}</div><div class="ex">{a["excerpt"]}</div><span class="more">Lire l\'article →</span></a>\n'
    return head("Actualités & Guides Paris Sportifs | Cousin Marc Pronostic",
        "Guides et actualités paris sportifs : inscription, dépôts et retraits mobile money, conseils pour parier sur le foot. Par Cousin Marc.",
        f"{BASE}/actualites.html", nav=nav_fr(en="news.html", es="noticias.html", ar="actualites-ar.html"), alternates=(f"{BASE}/actualites.html", f"{BASE}/news.html", f"{BASE}/noticias.html", f"{BASE}/actualites-ar.html"))+f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">⚽ Guides & Actualités</p>
<h1>Actualités <span class="hl">& guides</span></h1>
<p class="sub">Mes guides pour parier malin : inscription, dépôts, retraits et conseils foot.</p>
</div></header>
<main class="wrap">
<section style="border-bottom:none">
<div class="postlist">
{cards}
</div>
</section>
</main>
{footer_html()}
</body></html>"""

def cote_de_2_page():
    onex = next(b["site"] for b in BOOKMAKERS if b["slug"]=="code-promo-1xbet")
    return head(
        "Côte de 2 du jour : le coupon de Cousin Marc",
        "Le coupon Côte de 2 du jour de Cousin Marc : un pari combiné avec une cote autour de 2, publié chaque matin. Code promo FFN.",
        f"{BASE}/cote-de-2.html", nav=nav_fr(en="odds-of-2.html", es="cuota-de-2.html", ar="cote-2-ar.html"), alternates=(f"{BASE}/cote-de-2.html", f"{BASE}/odds-of-2.html", f"{BASE}/cuota-de-2.html", f"{BASE}/cote-2-ar.html")) + f"""
<header class="hero" style="padding:30px 0 20px"><div class="wrap">
<p class="eyebrow">⚽ Coupon du jour</p>
<h1>Côte de <span class="hl">2</span></h1>
</div></header>
<main class="wrap">
<section style="border-bottom:none;padding-top:20px">
{cote2_history_html("fr","Coupon Cote de 2 de Cousin Marc")}
<p style="text-align:center;color:var(--mist);font-size:14px;margin-top:12px">📅 Coupon mis à jour chaque matin</p>
<div class="btnrow" style="margin-top:20px">
<a class="cta" href="{onex}" rel="sponsored nofollow">🌐 Jouer ce coupon</a>
<a class="cta alt" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a>
</div>
</section>
<section>
<h2><span class="num">●</span> C'est quoi la « Côte de 2 » ?</h2>
<p>La « Côte de 2 », c'est un coupon combiné dont la cote totale tourne autour de 2. L'idée est simple : viser un gain régulier en doublant ta mise, avec un risque maîtrisé. Chaque matin, je publie ici mon coupon du jour.</p>
</section>
<section>
<h2><span class="num">●</span> Joue avec le code promo</h2>
<p>Avant de jouer le coupon, ouvre ton compte avec le code <b style="color:var(--gold)">FFN</b> pour profiter du bonus de bienvenue.</p>
<div class="related">{related_block("")}</div>
</section>
<section style="border-bottom:none">
<div class="note">⚠️ Réservé aux 18 ans et +. Aucun coupon n'est garanti à 100%. Joue de manière responsable et ne mise que ce que tu peux te permettre de perdre.</div>
</section>
</main>
{footer_html()}
</body></html>"""

def en_slug(b): return b["name"].lower().replace(" ","")+"-promo-code"

def buttons_en(b):
    out = f'<a class="cta" href="{b["site"]}" rel="sponsored nofollow">🌐 Register on the site</a>'
    for label, url in b["apps"]:
        icon = "🤖" if label in ("Android","Application") else "🍏"
        lab = "App" if label=="Application" else label
        out += f'<a class="cta alt" href="{url}" rel="sponsored nofollow">{icon} {lab}</a>'
    return out

def country_rows_en(b):
    rows=""
    for c,v in b["countries"]:
        ve = v.replace("jusqu'à","up to").replace("selon devise locale","depending on local currency")
        rows += f'<tr><td>{html.escape(c)}</td><td>{html.escape(ve)}</td><td>{b["code"]}</td></tr>'
    return rows

def faq_jsonld_en(name, code):
    qs = [
        (f"What is the {name} promo code in 2026?",
         f"The {name} promo code valid in 2026 is {code}. Enter it during registration to unlock the {pct(name, 'en', True)} welcome bonus on your first deposit."),
        (f"How do I use the {name} promo code {code}?",
         f"During registration on {name}, paste the code {code} in the 'Promo code' field. The bonus is credited automatically after your first deposit."),
        (f"Is the {name} promo code free?",
         f"Yes, the code {code} is 100% free. It only serves to activate the welcome bonus."),
    ]
    data = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qs]}
    return json.dumps(data, ensure_ascii=False, indent=2)

def related_block_en(current):
    cards=""
    for b in BOOKMAKERS:
        if b["slug"]==current: continue
        cards += f'<a href="{en_slug(b)}.html" style="border-left:3px solid {BRAND[b["slug"]]}"><div class="bk" translate="no">{bk_logo(b, "rlogo", 28)}{b["name"]}</div><div class="cd">Code: {b["code"]}</div></a>\n'
    return cards

def footer_html_en():
    return f"""<footer><div class="wrap">
<div class="cols">
<div><h4>Navigation</h4>
<a href="promo-codes.html">Promo codes</a>
<a href="odds-of-2.html">Odds of 2</a>
<a href="predictions.html">Predictions</a>
<a href="results.html">Results</a>
<a href="news.html">News</a>
<a href="about.html">About</a>
<a href="index.html">Français</a>
</div>
<div><h4>Bookmakers</h4>
{''.join(f'<a href="{en_slug(b)}.html">{b["name"]}</a>' for b in BOOKMAKERS[:4])}
</div>
<div><h4>Networks</h4>
<a href="https://t.me/marc_prono" rel="nofollow">Telegram</a>
<a href="https://youtube.com/@prossport" rel="nofollow">YouTube</a>
<a href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">WhatsApp</a>
</div>
</div>
<div class="warn">⚠️ 18+ only. Gambling involves risks: debt, addiction, isolation. Play responsibly and only bet what you can afford to lose.</div>
<p style="margin-top:18px">© 2026 Cousin Marc Pronostic · Promo code FFN · Football tips Africa</p>
</div></footer>
<script>function copyCode(btn,code){{navigator.clipboard.writeText(code).then(function(){{var t=btn.textContent;btn.textContent="✅ Copied!";setTimeout(function(){{btn.textContent=t;}},1500);}});}}</script>"""

def bookmaker_page_en(b):
    name, code, slug = b["name"], b["code"], b["slug"]
    es = en_slug(b); canonical = f"{BASE}/{es}.html"
    extra = f'<script type="application/ld+json">\n{faq_jsonld_en(name, code)}\n</script>'
    alternates = (f"{BASE}/{slug}.html", canonical, f"{BASE}/{es_slug(b)}.html", f"{BASE}/{ar_slug(b)}.html")
    appnote = " or the app" if b["apps"] else ""
    _t, _d = _title_desc(b, "en",
        f"{name} Promo Code 2026: {code} \u2192 {bk_bonus(b,'en')} | Cousin Marc",
        f"{name} promo code 2026: use {code} at registration and activate your bonus ({bk_bonus(b,'en')}). Step-by-step guide by Cousin Marc.")
    return head(_t, _d,
        canonical, extra, nav=nav_en(fr=f"{slug}.html", es=f"{es_slug(b)}.html", ar=f"{ar_slug(b)}.html"), lang="en", alternates=alternates) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Cousin Marc Pronostic · Updated {MAJ_EN}</p>
<h1><span class="hl" translate="no">{name}</span> Promo Code 2026</h1>
<p class="sub">Activate your <b>welcome bonus ({bk_bonus(b,'en')})</b> with the official code below. Checked and tested by Cousin Marc.</p>
<div class="codebox">{bk_logo(b, "cblogo", 64)}<div class="stamp"><span class="st-txt">Verified by CM</span></div>
<div class="lab">Official promo code</div>
<div class="code">{code}</div>
<small>Paste it in the "Promo code" field at registration</small>
<div><button class="copybtn" aria-label="Copy promo code {code}" onclick="copyCode(this,'{code}')">📋 Copy code</button></div>
</div>
<div class="btnrow">{buttons_en(b)}</div>
</div></header>
{affiche_img(b,'en')}
<main class="wrap">
<section>
<h2><span class="num">01</span> What is the {name} promo code?</h2>
<p>{bk_intro(b,'en')}</p>
<p>The promo code <b>{code}</b> is an official partner code: you enter it once at registration to activate {name}'s welcome bonus.</p>
</section>
<section>
<h2><span class="num">02</span> How to register on {name}</h2>
<ol class="steps">
<li><b>Open {name}</b> using the "Register on the site" button{appnote}.</li>
<li><b>Choose your country and currency</b> — the bonus adapts automatically.</li>
<li><b>Paste the code <span style="color:var(--gold)">{code}</span></b> in the "Promo code" field before confirming.</li>
<li><b>Make your first deposit</b>: the {pct(b)} bonus is credited instantly.</li>
<li><b>Place your bets</b> following the community's tips.</li>
</ol>
</section>
<section>
<h2><span class="num">03</span> {name} bonus by country</h2>
<p>With the code <b>{b['code']}</b>, the bonus is <b>{pct(b)} of your first deposit</b>{', up to 300,000 FCFA in FCFA countries' if b['slug'] in FFN300 else ''}, capped by your currency:</p>
<div class="tablecard"><table>
<thead><tr><th>Country</th><th>Maximum bonus</th><th>Code</th></tr></thead>
<tbody>{country_rows_en(b)}</tbody></table></div>
</section>
<section>
<h2><span class="num">04</span> Why trust me?</h2>
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">Football tipster · 95,000+ community</div></div></div>
<p style="margin-top:16px">I have been sharing football analysis for Africa for several years. I use {name} myself: I tested registration, deposits and withdrawals with the code {code} before sharing it.</p>
</section>
<section>
<h2><span class="num">05</span> Frequently asked questions</h2>
<details open><summary>Is the {name} promo code {code} free?</summary><p>Yes, completely. The code {code} costs nothing. It only activates the maximum welcome bonus at registration.</p></details>
<details><summary>Where do I enter the promo code on {name}?</summary><p>During account creation, a "Promo code" field appears in the form. Paste {code} there before confirming. If you forget it, you cannot add it afterwards.</p></details>
<details><summary>Does the code work in my country?</summary><p>Yes. {code} works in every country where {name} is available. Only the maximum bonus amount changes with your currency.</p></details>
</section>
<section>
<h2><span class="num">06</span> Other bookmakers & promo codes</h2>
{bk_extra(b,'en')}
<div class="related">{related_block_en(slug)}</div>
</section>
<section style="text-align:center;border-bottom:none">
<h2 style="justify-content:center">Ready to claim your bonus?</h2>
<p style="max-width:480px;margin:10px auto 0">Sign up now with the code <b style="color:var(--gold)">{code}</b>.</p>
<div class="btnrow">{buttons_en(b)}</div>
</section>
</main>
{footer_html_en()}
{sticky_bar(b,'en')}
</body></html>"""

def index_page_en():
    return home_page("en",
        "Sports Betting Promo Codes 2026 (FFN) | Cousin Marc",
        "All sports betting promo codes 2026: 1xBet, Melbet, Paripesa, Megapari and more. 100% welcome bonus with Cousin Marc's official codes.",
        f"{BASE}/promo-codes.html", nav_en(es="codigos-promocionales.html"), (f"{BASE}/", f"{BASE}/promo-codes.html", f"{BASE}/codigos-promocionales.html", f"{BASE}/promo-codes-ar.html"), footer_html_en)

def es_slug(b): return b["name"].lower().replace(" ","")+"-codigo-promocional"

def buttons_es(b):
    out = f'<a class="cta" href="{b["site"]}" rel="sponsored nofollow">🌐 Registrarse en el sitio</a>'
    for label, url in b["apps"]:
        icon = "🤖" if label in ("Android","Application") else "🍏"
        lab = "App" if label=="Application" else label
        out += f'<a class="cta alt" href="{url}" rel="sponsored nofollow">{icon} {lab}</a>'
    return out

def country_rows_es(b):
    rows=""
    for c,v in b["countries"]:
        ve = v.replace("jusqu'à","hasta").replace("selon devise locale","según la moneda local")
        rows += f'<tr><td>{html.escape(c)}</td><td>{html.escape(ve)}</td><td>{b["code"]}</td></tr>'
    return rows

def faq_jsonld_es(name, code):
    qs = [
        (f"¿Cuál es el código promocional de {name} en 2026?",
         f"El código promocional de {name} válido en 2026 es {code}. Introdúcelo al registrarte para desbloquear el bono de bienvenida del {pct(name, 'es', True)} en tu primer depósito."),
        (f"¿Cómo usar el código promocional {name} {code}?",
         f"Durante el registro en {name}, pega el código {code} en el campo «Código promocional». El bono se acredita automáticamente tras tu primer depósito."),
        (f"¿El código promocional de {name} es gratis?",
         f"Sí, el código {code} es 100% gratis. Solo sirve para activar el bono de bienvenida."),
    ]
    data = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qs]}
    return json.dumps(data, ensure_ascii=False, indent=2)

def related_block_es(current):
    cards=""
    for b in BOOKMAKERS:
        if b["slug"]==current: continue
        cards += f'<a href="{es_slug(b)}.html" style="border-left:3px solid {BRAND[b["slug"]]}"><div class="bk" translate="no">{bk_logo(b, "rlogo", 28)}{b["name"]}</div><div class="cd">Código: {b["code"]}</div></a>\n'
    return cards

def footer_html_es():
    return f"""<footer><div class="wrap">
<div class="cols">
<div><h4>Navegación</h4>
<a href="codigos-promocionales.html">Códigos promo</a>
<a href="cuota-de-2.html">Cuota de 2</a>
<a href="total-par-impar.html">Total Par/Impar</a>
<a href="pronosticos.html">Pronósticos</a>
<a href="resultados.html">Resultados</a>
<a href="noticias.html">Noticias</a>
<a href="acerca-de.html">Acerca de</a>
<a href="juego-responsable.html">Juego responsable</a>
<a href="index.html">Français</a>
<a href="promo-codes.html">English</a>
</div>
<div><h4>Casas de apuestas</h4>
{''.join(f'<a href="{es_slug(b)}.html">{b["name"]}</a>' for b in BOOKMAKERS[:4])}
</div>
<div><h4>Redes</h4>
<a href="https://t.me/marc_prono" rel="nofollow">Telegram</a>
<a href="https://youtube.com/@prossport" rel="nofollow">YouTube</a>
<a href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">WhatsApp</a>
</div>
</div>
<div class="warn">⚠️ Solo mayores de 18 años. El juego implica riesgos: deudas, adicción, aislamiento. Juega de forma responsable y apuesta solo lo que puedas permitirte perder.</div>
<p style="margin-top:18px">© 2026 Cousin Marc Pronostic · Código promocional FFN · Pronósticos de fútbol</p>
</div></footer>
<script>function copyCode(btn,code){{navigator.clipboard.writeText(code).then(function(){{var t=btn.textContent;btn.textContent="✅ ¡Copiado!";setTimeout(function(){{btn.textContent=t;}},1500);}});}}</script>"""

def bookmaker_page_es(b):
    name, code, slug = b["name"], b["code"], b["slug"]
    ess = es_slug(b); canonical = f"{BASE}/{ess}.html"
    extra = f'<script type="application/ld+json">\n{faq_jsonld_es(name, code)}\n</script>'
    alternates = (f"{BASE}/{slug}.html", f"{BASE}/{en_slug(b)}.html", canonical, f"{BASE}/{ar_slug(b)}.html")
    appnote = " o la app" if b["apps"] else ""
    return head(
        f"Código Promocional {name} 2026: {code} \u2192 {bk_bonus(b,'es')} | Cousin Marc",
        f"Código promocional {name} 2026: usa {code} al registrarte y activa tu bono ({bk_bonus(b,'es')}). Guía paso a paso por Cousin Marc.",
        canonical, extra, nav=nav_es(fr=f"{slug}.html", en=f"{en_slug(b)}.html", ar=f"{ar_slug(b)}.html"), lang="es", alternates=alternates) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Cousin Marc Pronostic · Actualizado en {MAJ_ES}</p>
<h1>Código Promocional <span class="hl" translate="no">{name}</span> 2026</h1>
<p class="sub">Activa tu <b>bono de bienvenida ({bk_bonus(b,'es')})</b> con el código oficial de abajo. Verificado y probado por Cousin Marc.</p>
<div class="codebox">{bk_logo(b, "cblogo", 64)}<div class="stamp"><span class="st-txt">Verificado por CM</span></div>
<div class="lab">Código promocional oficial</div>
<div class="code">{code}</div>
<small>Pégalo en el campo «Código promocional» al registrarte</small>
<div><button class="copybtn" aria-label="Copiar código promocional {code}" onclick="copyCode(this,'{code}')">📋 Copiar código</button></div>
</div>
<div class="btnrow">{buttons_es(b)}</div>
</div></header>
{affiche_img(b,'es')}
<main class="wrap">
<section>
<h2><span class="num">01</span> ¿Qué es el código promocional de {name}?</h2>
<p>{bk_intro(b,'es')}</p>
<p>El código promocional <b>{code}</b> es un código oficial de socio: lo introduces una sola vez al registrarte para activar el bono de bienvenida de {name}.</p>
</section>
<section>
<h2><span class="num">02</span> Cómo registrarse en {name}</h2>
<ol class="steps">
<li><b>Abre {name}</b> con el botón «Registrarse en el sitio»{appnote}.</li>
<li><b>Elige tu país y tu moneda</b>: el bono se adapta automáticamente.</li>
<li><b>Pega el código <span style="color:var(--gold)">{code}</span></b> en el campo «Código promocional» antes de confirmar.</li>
<li><b>Haz tu primer depósito</b>: el bono del {pct(b)} se acredita al instante.</li>
<li><b>Haz tus apuestas</b> siguiendo los pronósticos de la comunidad.</li>
</ol>
</section>
<section>
<h2><span class="num">03</span> Bono de {name} por país</h2>
<p>Con el código <b>{b['code']}</b>, el bono es del <b>{pct(b)} de tu primer depósito</b>{', hasta 300 000 FCFA en los países FCFA' if b['slug'] in FFN300 else ''}, con un tope según tu moneda:</p>
<div class="tablecard"><table>
<thead><tr><th>País</th><th>Bono máximo</th><th>Código</th></tr></thead>
<tbody>{country_rows_es(b)}</tbody></table></div>
</section>
<section>
<h2><span class="num">04</span> ¿Por qué confiar en mí?</h2>
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">Pronosticador de fútbol · comunidad de más de 95.000</div></div></div>
<p style="margin-top:16px">Llevo varios años compartiendo análisis de fútbol. Yo mismo uso {name}: probé el registro, los depósitos y los retiros con el código {code} antes de compartirlo.</p>
</section>
<section>
<h2><span class="num">05</span> Preguntas frecuentes</h2>
<details open><summary>¿El código promocional {name} {code} es gratis?</summary><p>Sí, completamente. El código {code} no cuesta nada. Solo activa el bono de bienvenida máximo al registrarte.</p></details>
<details><summary>¿Dónde introduzco el código promocional en {name}?</summary><p>Durante la creación de la cuenta aparece un campo «Código promocional» en el formulario. Pega {code} ahí antes de confirmar. Si lo olvidas, no podrás añadirlo después.</p></details>
<details><summary>¿Funciona el código en mi país?</summary><p>Sí. {code} funciona en todos los países donde {name} está disponible. Solo cambia el importe máximo del bono según tu moneda.</p></details>
</section>
<section>
<h2><span class="num">06</span> Otras casas de apuestas y códigos</h2>
{bk_extra(b,'es')}
<div class="related">{related_block_es(slug)}</div>
</section>
<section style="text-align:center;border-bottom:none">
<h2 style="justify-content:center">¿Listo para tu bono?</h2>
<p style="max-width:480px;margin:10px auto 0">Regístrate ahora con el código <b style="color:var(--gold)">{code}</b>.</p>
<div class="btnrow">{buttons_es(b)}</div>
</section>
</main>
{footer_html_es()}
{sticky_bar(b,'es')}
</body></html>"""

def index_page_es():
    return home_page("es",
        "Códigos Promocionales de Apuestas 2026 (FFN) | Cousin Marc",
        "Todos los códigos promocionales de apuestas 2026: 1xBet, Melbet, Paripesa, Megapari y más. Bono de bienvenida del 100% con los códigos oficiales de Cousin Marc.",
        f"{BASE}/codigos-promocionales.html", nav_es(), (f"{BASE}/", f"{BASE}/promo-codes.html", f"{BASE}/codigos-promocionales.html", f"{BASE}/promo-codes-ar.html"), footer_html_es)

def predictions_page_en():
    return head(
        "Football Predictions Today: Big Match Analysis | Cousin Marc",
        "Free football predictions from Cousin Marc: match analysis, odds and betting tips. Join the community for early predictions.",
        f"{BASE}/predictions.html", nav=nav_en(fr="pronostics.html", es="pronosticos.html", ar="pronostics-ar.html"), lang="en",
        alternates=(f"{BASE}/pronostics.html", f"{BASE}/predictions.html", f"{BASE}/pronosticos.html", f"{BASE}/pronostics-ar.html")) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">⚽ Analysis & Predictions</p>
<h1>Daily <span class="hl">Predictions</span></h1>
<p class="sub">My free football analysis. For early predictions and VIP accumulators, join my Telegram and WhatsApp community.</p>
<div class="btnrow"><a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a><a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 WhatsApp</a></div>
</div></header>
<main class="wrap">
{analyses_block("en")}
<section>
<h2><span class="num">●</span> My predictions are on Telegram &amp; WhatsApp</h2>
<p>I post my daily predictions live, every day, on my Telegram and WhatsApp channels. That's where you'll find my analysis, my accumulators and my tips first. Join the community, it's free.</p>
<div class="btnrow" style="justify-content:flex-start">
<a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Join the Telegram</a>
<a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 Join the WhatsApp</a>
</div>
<div class="social" style="margin-top:22px">{social_html()}</div>
</section>
<section>
<h2><span class="num">●</span> Bet with the right promo codes</h2>
<p>Before following my predictions, open your account with one of our partner bookmakers and enjoy the welcome bonus:</p>
<div class="related">{related_block_en("")}</div>
</section>
</main>
{footer_html_en()}
</body></html>"""

def about_page_en():
    return head(
        "About Cousin Marc Pronostic",
        "Who is Cousin Marc? Football tipster for Africa, community of 95,000+ followers. Analysis, verified promo codes and bettor support.",
        f"{BASE}/about.html", nav=nav_en(fr="a-propos.html", es="acerca-de.html", ar="a-propos-ar.html"), lang="en",
        alternates=(f"{BASE}/a-propos.html", f"{BASE}/about.html", f"{BASE}/acerca-de.html", f"{BASE}/a-propos-ar.html")) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Who am I?</p>
<h1>About <span class="hl">Cousin Marc</span></h1>
</div></header>
<main class="wrap legalbody">
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">Football tipster · 95,000+ community</div></div></div>
<p>I'm Cousin Marc, a football tipster who's passionate about the game. For several years, I have been guiding a large community of bettors across Africa with match analysis, tips, and a selection of bookmaker deals.</p>
<h2>My mission</h2>
<p>To help you bet in a more informed way: understand the odds, choose the right platforms, take advantage of the best welcome bonuses, and do it responsibly.</p>
<h2>Why my promo codes?</h2>
<p>Every promo code shared on this site (FFN, and the bookmaker-specific codes) is personally tested before being published. I check registration, deposit and withdrawal to make sure everything works.</p>
<h2>Join the community</h2>
<p>For my early predictions and detailed analysis:</p>
<div class="social">{social_html()}</div>
<div class="note">⚠️ Sports betting involves risk. I share analysis and deals, but no prediction is guaranteed. Play responsibly.</div>
</main>
{footer_html_en()}
</body></html>"""

def responsible_gambling_page_en():
    return head(
        "Responsible Gambling | Cousin Marc Pronostic",
        "Tips to bet responsibly. Gambling should stay fun: limits, warning signs and help resources.",
        f"{BASE}/responsible-gambling.html", nav=nav_en(fr="jeu-responsable.html", es="juego-responsable.html", ar="jeu-responsable-ar.html"), lang="en",
        alternates=(f"{BASE}/jeu-responsable.html", f"{BASE}/responsible-gambling.html", f"{BASE}/juego-responsable.html", f"{BASE}/jeu-responsable-ar.html")) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Important</p>
<h1>Responsible <span class="hl">Gambling</span></h1>
</div></header>
<main class="wrap legalbody">
<p>Sports betting should remain entertainment, never a source of income nor a solution to financial difficulties. Here are a few essential rules.</p>
<h2>The basic rules</h2>
<ul>
<li>For adults only (18 and over).</li>
<li>Only stake what you can afford to lose.</li>
<li>Set yourself a budget and time limits, and stick to them.</li>
<li>Never bet to "win back" a loss.</li>
<li>Betting is not a way to make money regularly.</li>
</ul>
<h2>Warning signs</h2>
<ul>
<li>You bet more than planned, or with money you need.</li>
<li>You think about betting constantly.</li>
<li>You hide your bets from those close to you.</li>
<li>You bet to escape problems or stress.</li>
</ul>
<h2>Need help?</h2>
<p>If gambling becomes a problem for you or someone close to you, talk to a trusted person and reach out to a local support organization specialized in gambling addiction. Most bookmakers also offer self-limitation and self-exclusion tools in your account settings.</p>
<div class="note">Gambling should stay fun. If it no longer is, take a break.</div>
</main>
{footer_html_en()}
</body></html>"""

def odds_of_2_page_en():
    onex = next(b["site"] for b in BOOKMAKERS if b["slug"]=="code-promo-1xbet")
    return head(
        "Odds of 2 of the Day: Cousin Marc's Coupon",
        "Cousin Marc's daily Odds of 2 coupon: an accumulator bet with total odds around 2, posted every morning. Promo code FFN.",
        f"{BASE}/odds-of-2.html", nav=nav_en(fr="cote-de-2.html", es="cuota-de-2.html", ar="cote-2-ar.html"), lang="en",
        alternates=(f"{BASE}/cote-de-2.html", f"{BASE}/odds-of-2.html", f"{BASE}/cuota-de-2.html", f"{BASE}/cote-2-ar.html")) + f"""
<header class="hero" style="padding:30px 0 20px"><div class="wrap">
<p class="eyebrow">⚽ Coupon of the day</p>
<h1>Odds of <span class="hl">2</span></h1>
</div></header>
<main class="wrap">
<section style="border-bottom:none;padding-top:20px">
{cote2_history_html("en","Cousin Marc Odds of 2 coupon")}
<p style="text-align:center;color:var(--mist);font-size:14px;margin-top:12px">📅 Coupon updated every morning</p>
<div class="btnrow" style="margin-top:20px">
<a class="cta" href="{onex}" rel="sponsored nofollow">🌐 Play this coupon</a>
<a class="cta alt" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a>
</div>
</section>
<section>
<h2><span class="num">●</span> What is the "Odds of 2"?</h2>
<p>The "Odds of 2" is an accumulator coupon whose total odds are around 2. The idea is simple: aim for a steady win by doubling your stake, with controlled risk. Every morning, I post my coupon of the day here.</p>
</section>
<section>
<h2><span class="num">●</span> Play with the promo code</h2>
<p>Before playing the coupon, open your account with the code <b style="color:var(--gold)">FFN</b> to enjoy the welcome bonus.</p>
<div class="related">{related_block_en("")}</div>
</section>
<section style="border-bottom:none">
<div class="note">⚠️ 18+ only. No coupon is guaranteed 100%. Play responsibly and only stake what you can afford to lose.</div>
</section>
</main>
{footer_html_en()}
</body></html>"""

def article_jsonld_en(a):
    canonical=f"{BASE}/{a['slug']}.html"
    data={"@context":"https://schema.org","@type":"Article","headline":a["title"],
          "datePublished":a["date_iso"],"dateModified":a["date_iso"],
          "author":{"@type":"Person","name":"Cousin Marc"},
          "publisher":{"@type":"Organization","name":"Cousin Marc Pronostic"},
          "mainEntityOfPage":canonical}
    return json.dumps(data,ensure_ascii=False,indent=2)

def article_cta_en(a):
    if a.get("cta_slug"):
        return f'<section style="text-align:center;border-bottom:none"><h2 style="justify-content:center">Take action</h2><div class="btnrow" style="margin-top:18px"><a class="cta" href="{a["cta_slug"]}.html">{a["cta_label"]}</a></div></section>'
    return '<section style="text-align:center;border-bottom:none"><h2 style="justify-content:center">My predictions of the day</h2><p style="max-width:480px;margin:10px auto 0">Find my live predictions on Telegram and WhatsApp.</p><div class="btnrow" style="margin-top:18px"><a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a><a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 WhatsApp</a></div></section>'

def article_page_en(a):
    canonical=f"{BASE}/{a['slug']}.html"
    extra=f'<script type="application/ld+json">\n{article_jsonld_en(a)}\n</script>'
    return head(f"{a['title']} | Cousin Marc Pronostic", a["desc"], canonical, extra,
        nav=nav_en(fr=f"{a['fr_slug']}.html", es=f"{ARTICLE_FR2ES[a['fr_slug']]}.html", ar=f"{ARTICLE_FR2AR[a['fr_slug']]}.html"), lang="en",
        alternates=(f"{BASE}/{a['fr_slug']}.html", canonical, f"{BASE}/{ARTICLE_FR2ES[a['fr_slug']]}.html", f"{BASE}/{ARTICLE_FR2AR[a['fr_slug']]}.html"))+f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">News · {a['date_en']}</p>
<h1>{a['title']}</h1>
</div></header>
<main class="wrap article">
{a['body']}
<section style="border-bottom:none">
<h3>About the author</h3>
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">Football tipster · 95,000+ community</div></div></div>
<div class="social" style="margin-top:16px">{social_html()}</div>
</section>
{article_cta_en(a)}
</main>
{footer_html_en()}
</body></html>"""

def news_page_en():
    cards=""
    for a in sorted(ARTICLES_EN,key=lambda x:x["date_iso"],reverse=True):
        cards+=f'<a class="postcard" href="{a["slug"]}.html"><div class="date">{a["date_en"]}</div><div class="pt">{a["title"]}</div><div class="ex">{a["excerpt"]}</div><span class="more">Read the article →</span></a>\n'
    return head("Sports Betting News & Guides | Cousin Marc Pronostic",
        "Sports betting guides and news: registration, mobile money deposits and withdrawals, tips to bet on football. By Cousin Marc.",
        f"{BASE}/news.html", nav=nav_en(fr="actualites.html", es="noticias.html", ar="actualites-ar.html"), lang="en",
        alternates=(f"{BASE}/actualites.html", f"{BASE}/news.html", f"{BASE}/noticias.html", f"{BASE}/actualites-ar.html"))+f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">⚽ Guides &amp; News</p>
<h1>News <span class="hl">&amp; guides</span></h1>
<p class="sub">My guides to bet smart: registration, deposits, withdrawals and football tips.</p>
</div></header>
<main class="wrap">
<section style="border-bottom:none">
<div class="postlist">
{cards}
</div>
</section>
</main>
{footer_html_en()}
</body></html>"""

def predictions_page_es():
    return head(
        "Pronósticos de Fútbol de Hoy: Análisis de los Grandes Partidos | Cousin Marc",
        "Pronósticos de fútbol gratis de Cousin Marc: análisis de partidos, cuotas y consejos de apuestas. Únete a la comunidad para los pronósticos en primicia.",
        f"{BASE}/pronosticos.html", nav=nav_es(fr="pronostics.html", en="predictions.html", ar="pronostics-ar.html"), lang="es",
        alternates=(f"{BASE}/pronostics.html", f"{BASE}/predictions.html", f"{BASE}/pronosticos.html", f"{BASE}/pronostics-ar.html")) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">⚽ Análisis y Pronósticos</p>
<h1>Pronósticos <span class="hl">del día</span></h1>
<p class="sub">Mis análisis de fútbol gratis. Para los pronósticos en primicia y las combinadas VIP, únete a mi comunidad de Telegram y WhatsApp.</p>
<div class="btnrow"><a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a><a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 WhatsApp</a></div>
</div></header>
<main class="wrap">
{analyses_block("es")}
<section>
<h2><span class="num">●</span> Mis pronósticos están en Telegram y WhatsApp</h2>
<p>Publico mis pronósticos del día en directo, cada día, en mis canales de Telegram y WhatsApp. Ahí encontrarás mis análisis, mis combinadas y mis consejos en primicia. Únete a la comunidad, es gratis.</p>
<div class="btnrow" style="justify-content:flex-start">
<a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Unirse al Telegram</a>
<a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 Unirse al WhatsApp</a>
</div>
<div class="social" style="margin-top:22px">{social_html()}</div>
</section>
<section>
<h2><span class="num">●</span> Apuesta con los códigos correctos</h2>
<p>Antes de seguir mis pronósticos, abre tu cuenta en una de nuestras casas de apuestas asociadas y aprovecha el bono de bienvenida:</p>
<div class="related">{related_block_es("")}</div>
</section>
</main>
{footer_html_es()}
</body></html>"""

def about_page_es():
    return head(
        "Acerca de Cousin Marc Pronostic",
        "¿Quién es Cousin Marc? Pronosticador de fútbol, comunidad de más de 95.000 seguidores. Análisis, códigos promocionales verificados y apoyo a los apostadores.",
        f"{BASE}/acerca-de.html", nav=nav_es(fr="a-propos.html", en="about.html", ar="a-propos-ar.html"), lang="es",
        alternates=(f"{BASE}/a-propos.html", f"{BASE}/about.html", f"{BASE}/acerca-de.html", f"{BASE}/a-propos-ar.html")) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">¿Quién soy?</p>
<h1>Acerca de <span class="hl">Cousin Marc</span></h1>
</div></header>
<main class="wrap legalbody">
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">Pronosticador de fútbol · comunidad de más de 95.000</div></div></div>
<p>Soy Cousin Marc, pronosticador apasionado del fútbol. Desde hace varios años, acompaño a una amplia comunidad de apostadores con análisis de partidos, consejos y una selección de ofertas de casas de apuestas.</p>
<h2>Mi misión</h2>
<p>Ayudarte a apostar de forma más informada: entender las cuotas, elegir las plataformas adecuadas, aprovechar los mejores bonos de bienvenida y hacerlo de manera responsable.</p>
<h2>¿Por qué mis códigos promocionales?</h2>
<p>Cada código promocional compartido en este sitio (FFN y los códigos específicos por casa) se prueba personalmente antes de publicarse. Verifico el registro, el depósito y el retiro para asegurarme de que todo funciona.</p>
<h2>Únete a la comunidad</h2>
<p>Para mis pronósticos en primicia y mis análisis detallados:</p>
<div class="social">{social_html()}</div>
<div class="note">⚠️ Las apuestas deportivas implican riesgos. Comparto análisis y ofertas, pero ningún pronóstico está garantizado. Juega de forma responsable.</div>
</main>
{footer_html_es()}
</body></html>"""

def responsible_gambling_page_es():
    return head(
        "Juego Responsable | Cousin Marc Pronostic",
        "Consejos para apostar de forma responsable. El juego debe seguir siendo un placer: límites, señales de alerta y recursos de ayuda.",
        f"{BASE}/juego-responsable.html", nav=nav_es(fr="jeu-responsable.html", en="responsible-gambling.html", ar="jeu-responsable-ar.html"), lang="es",
        alternates=(f"{BASE}/jeu-responsable.html", f"{BASE}/responsible-gambling.html", f"{BASE}/juego-responsable.html", f"{BASE}/jeu-responsable-ar.html")) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Importante</p>
<h1>Juego <span class="hl">responsable</span></h1>
</div></header>
<main class="wrap legalbody">
<p>Las apuestas deportivas deben seguir siendo un entretenimiento, nunca una fuente de ingresos ni una solución a dificultades económicas. Aquí tienes algunas reglas esenciales.</p>
<h2>Las reglas básicas</h2>
<ul>
<li>Solo para mayores de edad (18 años o más).</li>
<li>Apuesta solo lo que puedas permitirte perder.</li>
<li>Fíjate un presupuesto y límites de tiempo, y respétalos.</li>
<li>Nunca apuestes para «recuperar» una pérdida.</li>
<li>Apostar no es una forma de ganar dinero de manera regular.</li>
</ul>
<h2>Señales de alerta</h2>
<ul>
<li>Apuestas más de lo previsto, o con dinero que necesitas.</li>
<li>Piensas en apostar constantemente.</li>
<li>Ocultas tus apuestas a tus seres queridos.</li>
<li>Apuestas para escapar de problemas o del estrés.</li>
</ul>
<h2>¿Necesitas ayuda?</h2>
<p>Si el juego se convierte en un problema para ti o para alguien cercano, háblalo con una persona de confianza y acude a una organización local de ayuda especializada en la adicción al juego. La mayoría de las casas de apuestas también ofrecen herramientas de autolimitación y autoexclusión en los ajustes de tu cuenta.</p>
<div class="note">El juego debe seguir siendo un placer. Si ya no lo es, haz una pausa.</div>
</main>
{footer_html_es()}
</body></html>"""

def cuota_de_2_page_es():
    onex = next(b["site"] for b in BOOKMAKERS if b["slug"]=="code-promo-1xbet")
    return head(
        "Cuota de 2 del día: el boleto de Cousin Marc",
        "El boleto Cuota de 2 del día de Cousin Marc: una apuesta combinada con una cuota cercana a 2, publicada cada mañana. Código promocional FFN.",
        f"{BASE}/cuota-de-2.html", nav=nav_es(fr="cote-de-2.html", en="odds-of-2.html", ar="cote-2-ar.html"), lang="es",
        alternates=(f"{BASE}/cote-de-2.html", f"{BASE}/odds-of-2.html", f"{BASE}/cuota-de-2.html", f"{BASE}/cote-2-ar.html")) + f"""
<header class="hero" style="padding:30px 0 20px"><div class="wrap">
<p class="eyebrow">⚽ Boleto del día</p>
<h1>Cuota de <span class="hl">2</span></h1>
</div></header>
<main class="wrap">
<section style="border-bottom:none;padding-top:20px">
{cote2_history_html("es","Boleto Cuota de 2 de Cousin Marc")}
<p style="text-align:center;color:var(--mist);font-size:14px;margin-top:12px">📅 Boleto actualizado cada mañana</p>
<div class="btnrow" style="margin-top:20px">
<a class="cta" href="{onex}" rel="sponsored nofollow">🌐 Jugar este boleto</a>
<a class="cta alt" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a>
</div>
</section>
<section>
<h2><span class="num">●</span> ¿Qué es la «Cuota de 2»?</h2>
<p>La «Cuota de 2» es un boleto combinado cuya cuota total ronda el 2. La idea es sencilla: buscar una ganancia regular duplicando tu apuesta, con un riesgo controlado. Cada mañana publico aquí mi boleto del día.</p>
</section>
<section>
<h2><span class="num">●</span> Juega con el código promocional</h2>
<p>Antes de jugar el boleto, abre tu cuenta con el código <b style="color:var(--gold)">FFN</b> para aprovechar el bono de bienvenida.</p>
<div class="related">{related_block_es("")}</div>
</section>
<section style="border-bottom:none">
<div class="note">⚠️ Solo mayores de 18 años. Ningún boleto está garantizado al 100%. Juega de forma responsable y apuesta solo lo que puedas permitirte perder.</div>
</section>
</main>
{footer_html_es()}
</body></html>"""

def article_jsonld_es(a):
    canonical=f"{BASE}/{a['slug']}.html"
    data={"@context":"https://schema.org","@type":"Article","headline":a["title"],
          "datePublished":a["date_iso"],"dateModified":a["date_iso"],
          "author":{"@type":"Person","name":"Cousin Marc"},
          "publisher":{"@type":"Organization","name":"Cousin Marc Pronostic"},
          "mainEntityOfPage":canonical}
    return json.dumps(data,ensure_ascii=False,indent=2)

def article_cta_es(a):
    if a.get("cta_slug"):
        return f'<section style="text-align:center;border-bottom:none"><h2 style="justify-content:center">Pasa a la acción</h2><div class="btnrow" style="margin-top:18px"><a class="cta" href="{a["cta_slug"]}.html">{a["cta_label"]}</a></div></section>'
    return '<section style="text-align:center;border-bottom:none"><h2 style="justify-content:center">Mis pronósticos del día</h2><p style="max-width:480px;margin:10px auto 0">Encuentra mis pronósticos en directo en Telegram y WhatsApp.</p><div class="btnrow" style="margin-top:18px"><a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a><a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 WhatsApp</a></div></section>'

def article_page_es(a):
    canonical=f"{BASE}/{a['slug']}.html"
    extra=f'<script type="application/ld+json">\n{article_jsonld_es(a)}\n</script>'
    en_eq = ARTICLE_FR2EN[a['fr_slug']]
    return head(f"{a['title']} | Cousin Marc Pronostic", a["desc"], canonical, extra,
        nav=nav_es(fr=f"{a['fr_slug']}.html", en=f"{en_eq}.html", ar=f"{ARTICLE_FR2AR[a['fr_slug']]}.html"), lang="es",
        alternates=(f"{BASE}/{a['fr_slug']}.html", f"{BASE}/{en_eq}.html", canonical, f"{BASE}/{ARTICLE_FR2AR[a['fr_slug']]}.html"))+f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Noticias · {a['date_es']}</p>
<h1>{a['title']}</h1>
</div></header>
<main class="wrap article">
{a['body']}
<section style="border-bottom:none">
<h3>Sobre el autor</h3>
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">Pronosticador de fútbol · comunidad de más de 95.000</div></div></div>
<div class="social" style="margin-top:16px">{social_html()}</div>
</section>
{article_cta_es(a)}
</main>
{footer_html_es()}
</body></html>"""

def news_page_es():
    cards=""
    for a in sorted(ARTICLES_ES,key=lambda x:x["date_iso"],reverse=True):
        cards+=f'<a class="postcard" href="{a["slug"]}.html"><div class="date">{a["date_es"]}</div><div class="pt">{a["title"]}</div><div class="ex">{a["excerpt"]}</div><span class="more">Leer el artículo →</span></a>\n'
    return head("Noticias y Guías de Apuestas | Cousin Marc Pronostic",
        "Guías y noticias de apuestas deportivas: registro, depósitos y retiros, consejos para apostar al fútbol. Por Cousin Marc.",
        f"{BASE}/noticias.html", nav=nav_es(fr="actualites.html", en="news.html", ar="actualites-ar.html"), lang="es",
        alternates=(f"{BASE}/actualites.html", f"{BASE}/news.html", f"{BASE}/noticias.html", f"{BASE}/actualites-ar.html"))+f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">⚽ Guías y Noticias</p>
<h1>Noticias <span class="hl">y guías</span></h1>
<p class="sub">Mis guías para apostar con cabeza: registro, depósitos, retiros y consejos de fútbol.</p>
</div></header>
<main class="wrap">
<section style="border-bottom:none">
<div class="postlist">
{cards}
</div>
</section>
</main>
{footer_html_es()}
</body></html>"""

def ar_slug(b): return b["name"].lower().replace(" ","")+"-promo-ar"

def buttons_ar(b):
    out = f'<a class="cta" href="{b["site"]}" rel="sponsored nofollow">🌐 التسجيل في الموقع</a>'
    for label, url in b["apps"]:
        icon = "🤖" if label in ("Android","Application") else "🍏"
        lab = "تطبيق" if label=="Application" else label
        out += f'<a class="cta alt" href="{url}" rel="sponsored nofollow">{icon} {lab}</a>'
    return out

def country_rows_ar(b):
    rows=""
    for c,v in b["countries"]:
        ve = v.replace("jusqu'à","حتى").replace("selon devise locale","حسب العملة المحلية")
        rows += f'<tr><td>{html.escape(c)}</td><td>{html.escape(ve)}</td><td>{b["code"]}</td></tr>'
    return rows

def faq_jsonld_ar(name, code):
    qs = [
        (f"ما هو الرمز الترويجي لـ {name} في 2026؟",
         f"الرمز الترويجي لـ {name} الصالح في 2026 هو {code}. أدخله عند التسجيل لتفعيل مكافأة الترحيب بنسبة {pct(name, 'ar', True)} على إيداعك الأول."),
        (f"كيف أستخدم الرمز الترويجي {name} {code}؟",
         f"أثناء التسجيل في {name}، الصق الرمز {code} في حقل «الرمز الترويجي». تُضاف المكافأة تلقائيًا بعد إيداعك الأول."),
        (f"هل الرمز الترويجي لـ {name} مجاني؟",
         f"نعم، الرمز {code} مجاني 100%. يُستخدم فقط لتفعيل مكافأة الترحيب."),
    ]
    data = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qs]}
    return json.dumps(data, ensure_ascii=False, indent=2)

def related_block_ar(current):
    cards=""
    for b in BOOKMAKERS:
        if b["slug"]==current: continue
        cards += f'<a href="{ar_slug(b)}.html" style="border-right:3px solid {BRAND[b["slug"]]}"><div class="bk" translate="no">{bk_logo(b, "rlogo", 28)}{b["name"]}</div><div class="cd">الرمز: {b["code"]}</div></a>\n'
    return cards

def footer_html_ar():
    return f"""<footer><div class="wrap">
<div class="cols">
<div><h4>التنقّل</h4>
<a href="promo-codes-ar.html">رموز ترويجية</a>
<a href="cote-2-ar.html">رهان بضعف 2</a>
<a href="total-pair-impair-ar.html">إجمالي زوجي/فردي</a>
<a href="pronostics-ar.html">توقعات</a>
<a href="resultats-ar.html">النتائج</a>
<a href="actualites-ar.html">أخبار</a>
<a href="a-propos-ar.html">من نحن</a>
<a href="jeu-responsable-ar.html">المراهنة المسؤولة</a>
<a href="index.html">Français</a>
<a href="promo-codes.html">English</a>
</div>
<div><h4>المراهنات</h4>
{''.join(f'<a href="{ar_slug(b)}.html">{b["name"]}</a>' for b in BOOKMAKERS[:4])}
</div>
<div><h4>الشبكات</h4>
<a href="https://t.me/marc_prono" rel="nofollow">Telegram</a>
<a href="https://youtube.com/@prossport" rel="nofollow">YouTube</a>
<a href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">WhatsApp</a>
</div>
</div>
<div class="warn">⚠️ للبالغين فقط (18 عامًا فأكثر). المراهنة تنطوي على مخاطر: ديون، إدمان، عزلة. العب بمسؤولية وراهن فقط بما يمكنك تحمّل خسارته.</div>
<p style="margin-top:18px">© 2026 Cousin Marc Pronostic · الرمز الترويجي FFN · توقعات كرة القدم</p>
</div></footer>
<script>function copyCode(btn,code){{navigator.clipboard.writeText(code).then(function(){{var t=btn.textContent;btn.textContent="✅ تم النسخ!";setTimeout(function(){{btn.textContent=t;}},1500);}});}}</script>"""

def bookmaker_page_ar(b):
    name, code, slug = b["name"], b["code"], b["slug"]
    ars = ar_slug(b); canonical = f"{BASE}/{ars}.html"
    extra = f'<script type="application/ld+json">\n{faq_jsonld_ar(name, code)}\n</script>'
    alternates = (f"{BASE}/{slug}.html", f"{BASE}/{en_slug(b)}.html", f"{BASE}/{es_slug(b)}.html", canonical)
    appnote = " أو التطبيق" if b["apps"] else ""
    return head(
        f"الرمز الترويجي {name} 2026: {code} \u2190 {bk_bonus(b,'ar')} | Cousin Marc",
        f"الرمز الترويجي {name} 2026: استخدم {code} عند التسجيل وفعّل مكافأتك ({bk_bonus(b,'ar')}). دليل خطوة بخطوة من Cousin Marc.",
        canonical, extra, nav=nav_ar(fr=f"{slug}.html", en=f"{en_slug(b)}.html", es=f"{es_slug(b)}.html"), lang="ar", alternates=alternates) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Cousin Marc Pronostic · تحديث {MAJ_AR}</p>
<h1>الرمز الترويجي <span class="hl" translate="no">{name}</span> 2026</h1>
<p class="sub">فعّل <b>مكافأة الترحيب ({bk_bonus(b,'ar')})</b> بالرمز الرسمي أدناه. مُتحقَّق منه ومُجرَّب من Cousin Marc.</p>
<div class="codebox">{bk_logo(b, "cblogo", 64)}<div class="stamp"><span class="st-txt">موثّق من CM</span></div>
<div class="lab">الرمز الترويجي الرسمي</div>
<div class="code">{code}</div>
<small>الصقه في حقل «الرمز الترويجي» عند التسجيل</small>
<div><button class="copybtn" aria-label="نسخ الرمز الترويجي {code}" onclick="copyCode(this,'{code}')">📋 نسخ الرمز</button></div>
</div>
<div class="btnrow">{buttons_ar(b)}</div>
</div></header>
{affiche_img(b,'ar')}
<main class="wrap">
<section>
<h2><span class="num">01</span> ما هو الرمز الترويجي لـ {name}؟</h2>
<p>{bk_intro(b,'ar')}</p>
<p>الرمز الترويجي <b>{code}</b> هو رمز شريك رسمي: تُدخله مرة واحدة عند التسجيل لتفعيل مكافأة الترحيب من {name}.</p>
</section>
<section>
<h2><span class="num">02</span> كيفية التسجيل في {name}</h2>
<ol class="steps">
<li><b>افتح {name}</b> عبر زر «التسجيل في الموقع»{appnote}.</li>
<li><b>اختر بلدك وعملتك</b> — تتكيّف المكافأة تلقائيًا.</li>
<li><b>الصق الرمز <span style="color:var(--gold)">{code}</span></b> في حقل «الرمز الترويجي» قبل التأكيد.</li>
<li><b>قم بإيداعك الأول</b>: تُضاف مكافأة {pct(b)} فورًا.</li>
<li><b>ضع رهاناتك</b> باتباع توقعات المجتمع.</li>
</ol>
</section>
<section>
<h2><span class="num">03</span> مكافأة {name} حسب البلد</h2>
<p>المكافأة تساوي <b>{pct(b)} من إيداعك الأول</b>، بحد أقصى حسب عملتك:</p>
<div class="tablecard"><table>
<thead><tr><th>البلد</th><th>الحد الأقصى للمكافأة</th><th>الرمز</th></tr></thead>
<tbody>{country_rows_ar(b)}</tbody></table></div>
</section>
<section>
<h2><span class="num">04</span> لماذا تثق بي؟</h2>
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">خبير توقعات كرة القدم · مجتمع من أكثر من 95,000</div></div></div>
<p style="margin-top:16px">أشارك تحليلات كرة القدم منذ سنوات. أستخدم {name} بنفسي: جرّبت التسجيل والإيداع والسحب بالرمز {code} قبل مشاركته.</p>
</section>
<section>
<h2><span class="num">05</span> الأسئلة الشائعة</h2>
<details open><summary>هل الرمز الترويجي {name} {code} مجاني؟</summary><p>نعم، تمامًا. الرمز {code} لا يكلّف شيئًا. يفعّل فقط أقصى مكافأة ترحيب عند التسجيل.</p></details>
<details><summary>أين أُدخل الرمز الترويجي في {name}؟</summary><p>أثناء إنشاء الحساب يظهر حقل «الرمز الترويجي» في النموذج. الصق {code} هناك قبل التأكيد. إذا نسيته، لا يمكنك إضافته لاحقًا.</p></details>
<details><summary>هل يعمل الرمز في بلدي؟</summary><p>نعم. يعمل {code} في كل البلدان التي يتوفر فيها {name}. يتغيّر فقط الحد الأقصى للمكافأة حسب عملتك.</p></details>
</section>
<section>
<h2><span class="num">06</span> مراهنات ورموز أخرى</h2>
{bk_extra(b,'ar')}
<div class="related">{related_block_ar(slug)}</div>
</section>
<section style="text-align:center;border-bottom:none">
<h2 style="justify-content:center">جاهز للحصول على مكافأتك؟</h2>
<p style="max-width:480px;margin:10px auto 0">سجّل الآن بالرمز <b style="color:var(--gold)">{code}</b>.</p>
<div class="btnrow">{buttons_ar(b)}</div>
</section>
</main>
{footer_html_ar()}
{sticky_bar(b,'ar')}
</body></html>"""

def index_page_ar():
    return home_page("ar",
        "رموز ترويجية للمراهنات 2026 (FFN) | Cousin Marc",
        "كل الرموز الترويجية للمراهنات الرياضية 2026: 1xBet، Melbet، Paripesa، Megapari والمزيد. مكافأة ترحيب 100% مع رموز Cousin Marc الرسمية.",
        f"{BASE}/promo-codes-ar.html", nav_ar(), (f"{BASE}/", f"{BASE}/promo-codes.html", f"{BASE}/codigos-promocionales.html", f"{BASE}/promo-codes-ar.html"), footer_html_ar)

def predictions_page_ar():
    return head(
        "توقعات كرة القدم اليوم: تحليل المباريات الكبرى | Cousin Marc",
        "توقعات كرة القدم المجانية من Cousin Marc: تحليل المباريات، الاحتمالات ونصائح المراهنة. انضم إلى المجتمع للحصول على التوقعات حصريًا.",
        f"{BASE}/pronostics-ar.html", nav=nav_ar(fr="pronostics.html", en="predictions.html", es="pronosticos.html"), lang="ar",
        alternates=(f"{BASE}/pronostics.html", f"{BASE}/predictions.html", f"{BASE}/pronosticos.html", f"{BASE}/pronostics-ar.html")) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">⚽ تحليلات وتوقعات</p>
<h1>توقعات <span class="hl">اليوم</span></h1>
<p class="sub">تحليلاتي المجانية لكرة القدم. للحصول على التوقعات حصريًا والمركّبات VIP، انضم إلى مجتمعي على Telegram وWhatsApp.</p>
<div class="btnrow"><a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a><a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 WhatsApp</a></div>
</div></header>
<main class="wrap">
{analyses_block("ar")}
<section>
<h2><span class="num">●</span> توقعاتي على Telegram وWhatsApp</h2>
<p>أنشر توقعاتي اليومية مباشرةً، كل يوم، على قنواتي في Telegram وWhatsApp. هناك تجد تحليلاتي ومركّباتي ونصائحي حصريًا. انضم إلى المجتمع، إنه مجاني.</p>
<div class="btnrow" style="justify-content:flex-end">
<a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ الانضمام إلى Telegram</a>
<a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 الانضمام إلى WhatsApp</a>
</div>
<div class="social" style="margin-top:22px">{social_html()}</div>
</section>
<section>
<h2><span class="num">●</span> راهن بالرموز الصحيحة</h2>
<p>قبل متابعة توقعاتي، افتح حسابك في إحدى مواقع المراهنة الشريكة واستفد من مكافأة الترحيب:</p>
<div class="related">{related_block_ar("")}</div>
</section>
</main>
{footer_html_ar()}
</body></html>"""

def about_page_ar():
    return head(
        "من نحن - Cousin Marc Pronostic",
        "من هو Cousin Marc؟ خبير توقعات كرة القدم، مجتمع من أكثر من 95,000 متابع. تحليلات، رموز ترويجية مُتحقَّق منها ومرافقة المراهنين.",
        f"{BASE}/a-propos-ar.html", nav=nav_ar(fr="a-propos.html", en="about.html", es="acerca-de.html"), lang="ar",
        alternates=(f"{BASE}/a-propos.html", f"{BASE}/about.html", f"{BASE}/acerca-de.html", f"{BASE}/a-propos-ar.html")) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">من أنا؟</p>
<h1>من نحن · <span class="hl">Cousin Marc</span></h1>
</div></header>
<main class="wrap legalbody">
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">خبير توقعات كرة القدم · مجتمع من أكثر من 95,000</div></div></div>
<p>أنا Cousin Marc، خبير توقعات شغوف بكرة القدم. منذ سنوات، أرافق مجتمعًا واسعًا من المراهنين بتحليلات المباريات والنصائح ومجموعة مختارة من عروض المراهنات.</p>
<h2>مهمتي</h2>
<p>مساعدتك على المراهنة بطريقة أكثر وعيًا: فهم الاحتمالات، اختيار المنصات المناسبة، الاستفادة من أفضل مكافآت الترحيب، والقيام بذلك بمسؤولية.</p>
<h2>لماذا رموزي الترويجية؟</h2>
<p>كل رمز ترويجي يُشارَك على هذا الموقع (FFN والرموز الخاصة بكل موقع) يُجرَّب شخصيًا قبل نشره. أتحقق من التسجيل والإيداع والسحب للتأكد من أن كل شيء يعمل.</p>
<h2>انضم إلى المجتمع</h2>
<p>للحصول على توقعاتي حصريًا وتحليلاتي المفصّلة:</p>
<div class="social">{social_html()}</div>
<div class="note">⚠️ المراهنات الرياضية تنطوي على مخاطر. أشارك تحليلات وعروضًا، لكن لا يوجد توقّع مضمون. العب بمسؤولية.</div>
</main>
{footer_html_ar()}
</body></html>"""

def responsible_gambling_page_ar():
    return head(
        "المراهنة المسؤولة | Cousin Marc Pronostic",
        "نصائح للمراهنة بمسؤولية. يجب أن يبقى اللعب متعة: الحدود، علامات التحذير وموارد المساعدة.",
        f"{BASE}/jeu-responsable-ar.html", nav=nav_ar(fr="jeu-responsable.html", en="responsible-gambling.html", es="juego-responsable.html"), lang="ar",
        alternates=(f"{BASE}/jeu-responsable.html", f"{BASE}/responsible-gambling.html", f"{BASE}/juego-responsable.html", f"{BASE}/jeu-responsable-ar.html")) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">مهم</p>
<h1>المراهنة <span class="hl">المسؤولة</span></h1>
</div></header>
<main class="wrap legalbody">
<p>يجب أن تبقى المراهنات الرياضية ترفيهًا، لا مصدر دخل ولا حلًّا للصعوبات المالية. إليك بعض القواعد الأساسية.</p>
<h2>القواعد الأساسية</h2>
<ul>
<li>للبالغين فقط (18 عامًا فأكثر).</li>
<li>راهن فقط بما يمكنك تحمّل خسارته.</li>
<li>حدّد ميزانية وحدودًا زمنية، والتزم بها.</li>
<li>لا تراهن أبدًا لـ«تعويض» خسارة.</li>
<li>المراهنة ليست وسيلة لكسب المال بانتظام.</li>
</ul>
<h2>علامات التحذير</h2>
<ul>
<li>تراهن أكثر مما خطّطت، أو بمال تحتاجه.</li>
<li>تفكّر في المراهنة باستمرار.</li>
<li>تخفي رهاناتك عن المقرّبين منك.</li>
<li>تراهن للهروب من المشاكل أو التوتر.</li>
</ul>
<h2>تحتاج مساعدة؟</h2>
<p>إذا أصبحت المراهنة مشكلة لك أو لشخص قريب، تحدّث مع شخص تثق به وتواصل مع جهة محلية متخصصة في إدمان المقامرة. توفّر معظم مواقع المراهنة أيضًا أدوات للحد الذاتي والاستبعاد الذاتي في إعدادات حسابك.</p>
<div class="note">يجب أن يبقى اللعب متعة. إذا لم يعد كذلك، خذ استراحة.</div>
</main>
{footer_html_ar()}
</body></html>"""

def cote_de_2_page_ar():
    onex = next(b["site"] for b in BOOKMAKERS if b["slug"]=="code-promo-1xbet")
    return head(
        "رهان بضعف 2 لليوم: قسيمة Cousin Marc",
        "قسيمة «رهان بضعف 2» اليومية من Cousin Marc: رهان مركّب باحتمال قريب من 2، يُنشَر كل صباح. الرمز الترويجي FFN.",
        f"{BASE}/cote-2-ar.html", nav=nav_ar(fr="cote-de-2.html", en="odds-of-2.html", es="cuota-de-2.html"), lang="ar",
        alternates=(f"{BASE}/cote-de-2.html", f"{BASE}/odds-of-2.html", f"{BASE}/cuota-de-2.html", f"{BASE}/cote-2-ar.html")) + f"""
<header class="hero" style="padding:30px 0 20px"><div class="wrap">
<p class="eyebrow">⚽ قسيمة اليوم</p>
<h1>رهان بضعف <span class="hl">2</span></h1>
</div></header>
<main class="wrap">
<section style="border-bottom:none;padding-top:20px">
{cote2_history_html("ar","قسيمة رهان بضعف 2 من Cousin Marc")}
<p style="text-align:center;color:var(--mist);font-size:14px;margin-top:12px">📅 القسيمة تُحدَّث كل صباح</p>
<div class="btnrow" style="margin-top:20px">
<a class="cta" href="{onex}" rel="sponsored nofollow">🌐 العب هذه القسيمة</a>
<a class="cta alt" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a>
</div>
</section>
<section>
<h2><span class="num">●</span> ما هو «رهان بضعف 2»؟</h2>
<p>«رهان بضعف 2» هو قسيمة مركّبة احتمالها الإجمالي قريب من 2. الفكرة بسيطة: استهداف ربح منتظم بمضاعفة رهانك، مع مخاطرة محسوبة. كل صباح، أنشر هنا قسيمة اليوم.</p>
</section>
<section>
<h2><span class="num">●</span> العب بالرمز الترويجي</h2>
<p>قبل لعب القسيمة، افتح حسابك بالرمز <b style="color:var(--gold)">FFN</b> للاستفادة من مكافأة الترحيب.</p>
<div class="related">{related_block_ar("")}</div>
</section>
<section style="border-bottom:none">
<div class="note">⚠️ للبالغين فقط (18 عامًا فأكثر). لا قسيمة مضمونة 100%. العب بمسؤولية وراهن فقط بما يمكنك تحمّل خسارته.</div>
</section>
</main>
{footer_html_ar()}
</body></html>"""

def article_jsonld_ar(a):
    canonical=f"{BASE}/{a['slug']}.html"
    data={"@context":"https://schema.org","@type":"Article","headline":a["title"],
          "datePublished":a["date_iso"],"dateModified":a["date_iso"],
          "author":{"@type":"Person","name":"Cousin Marc"},
          "publisher":{"@type":"Organization","name":"Cousin Marc Pronostic"},
          "mainEntityOfPage":canonical}
    return json.dumps(data,ensure_ascii=False,indent=2)

def article_cta_ar(a):
    if a.get("cta_slug"):
        return f'<section style="text-align:center;border-bottom:none"><h2 style="justify-content:center">انتقل إلى الفعل</h2><div class="btnrow" style="margin-top:18px"><a class="cta" href="{a["cta_slug"]}.html">{a["cta_label"]}</a></div></section>'
    return '<section style="text-align:center;border-bottom:none"><h2 style="justify-content:center">توقعاتي لليوم</h2><p style="max-width:480px;margin:10px auto 0">تابع توقعاتي مباشرةً على Telegram وWhatsApp.</p><div class="btnrow" style="margin-top:18px"><a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a><a class="cta alt" href="https://whatsapp.com/channel/0029VbBBh2u9xVJnAVMu833h" rel="nofollow">💬 WhatsApp</a></div></section>'

def article_page_ar(a):
    canonical=f"{BASE}/{a['slug']}.html"
    extra=f'<script type="application/ld+json">\n{article_jsonld_ar(a)}\n</script>'
    en_eq=ARTICLE_FR2EN[a['fr_slug']]; es_eq=ARTICLE_FR2ES[a['fr_slug']]
    return head(f"{a['title']} | Cousin Marc Pronostic", a["desc"], canonical, extra,
        nav=nav_ar(fr=f"{a['fr_slug']}.html", en=f"{en_eq}.html", es=f"{es_eq}.html"), lang="ar",
        alternates=(f"{BASE}/{a['fr_slug']}.html", f"{BASE}/{en_eq}.html", f"{BASE}/{es_eq}.html", canonical))+f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">أخبار · {a['date_ar']}</p>
<h1>{a['title']}</h1>
</div></header>
<main class="wrap article">
{a['body']}
<section style="border-bottom:none">
<h3>عن الكاتب</h3>
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">خبير توقعات كرة القدم · مجتمع من أكثر من 95,000</div></div></div>
<div class="social" style="margin-top:16px">{social_html()}</div>
</section>
{article_cta_ar(a)}
</main>
{footer_html_ar()}
</body></html>"""

def news_page_ar():
    cards=""
    for a in sorted(ARTICLES_AR,key=lambda x:x["date_iso"],reverse=True):
        cards+=f'<a class="postcard" href="{a["slug"]}.html"><div class="date">{a["date_ar"]}</div><div class="pt">{a["title"]}</div><div class="ex">{a["excerpt"]}</div><span class="more">اقرأ المقال →</span></a>\n'
    return head("أخبار وأدلة المراهنات الرياضية | Cousin Marc Pronostic",
        "أدلة وأخبار المراهنات الرياضية: التسجيل، الإيداع والسحب، نصائح للمراهنة على كرة القدم. بقلم Cousin Marc.",
        f"{BASE}/actualites-ar.html", nav=nav_ar(fr="actualites.html", en="news.html", es="noticias.html"), lang="ar",
        alternates=(f"{BASE}/actualites.html", f"{BASE}/news.html", f"{BASE}/noticias.html", f"{BASE}/actualites-ar.html"))+f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">⚽ أدلة وأخبار</p>
<h1>أخبار <span class="hl">وأدلة</span></h1>
<p class="sub">أدلتي للمراهنة بذكاء: التسجيل، الإيداع، السحب ونصائح كرة القدم.</p>
</div></header>
<main class="wrap">
<section style="border-bottom:none">
<div class="postlist">
{cards}
</div>
</section>
</main>
{footer_html_ar()}
</body></html>"""

# === TOTAL PAIR/IMPAIR : coupons du jour (à modifier chaque jour) ===
TPI_SLUG = {"fr":"total-pair-impair.html","en":"total-odd-even.html","es":"total-par-impar.html","ar":"total-pair-impair-ar.html"}

TPI_COUPONS = [
 {"book":"1xBet","brand":"1xbet","img":"coupon-tpi-1xbet.jpg","site":"https://tinyurl.com/3vptk7a4","apk":"","tuto":"https://youtu.be/EnBk9p_Akvc"},
 {"book":"Melbet","brand":"melbet","img":"coupon-tpi-melbet.jpg","site":"https://tinyurl.com/48f3ukrb","apk":"https://tinyurl.com/4nsmfukc","tuto":""},
]

TPI_L = {
 "fr":{"eyebrow":"⚽ Coupons du jour","h1a":"Total ","h1b":"Pair / Impair",
   "sub":"Le coupon Total Pair/Impair du jour. Gratuit pour tous les comptes créés avec le code FFN.",
   "meta_desc":"Coupon Total Pair/Impair gratuit, mis à jour chaque matin par Cousin Marc. Crée ton compte 1xBet ou Melbet avec le code FFN pour le débloquer.",
   "cond_title":"Conditions pour télécharger ce coupon","cond_intro":"Ce coupon est 100% gratuit, mais réservé aux membres de la communauté. Pour pouvoir le jouer :",
   "steps":["Crée un compte avec le code promo <b>FFN</b> sur Melbet ou 1xBet. <a href='https://youtu.be/EnBk9p_Akvc' rel='nofollow' style='color:var(--gold);font-weight:700;white-space:nowrap'>▶️ Voir comment créer un compte</a>","Recharge ton compte d'au moins <b>3000 FCFA (10$)</b> pour l'activation.","Copie le code du coupon ci-dessous et joue-le sur ton appli."],
   "coupons_title":"Coupons du jour","copy":"📋 Copier le code","register":"🌐 S'inscrire","apk":"📲 APK","tuto":"▶️ Voir le tuto",
   "cote_label":"Cote","code_word":"Code","min_note":"Dépôt minimum d'activation : 3000 FCFA / 10$.",
   "disc":"⚠️ 18+. Aucun coupon n'est garanti à 100%. Joue de façon responsable et mise seulement ce que tu peux te permettre de perdre.",
   "promo_title":"Inscris-toi avec le bon code","promo_p":"Pour télécharger les coupons, ton compte doit être créé avec le code <b>FFN</b> :"},
 "en":{"eyebrow":"⚽ Coupons of the day","h1a":"Total ","h1b":"Odd / Even",
   "sub":"The Total Odd/Even coupon of the day. Free for all accounts created with code FFN.",
   "meta_desc":"Free Total Odd/Even coupon, updated every morning by Cousin Marc. Create your 1xBet or Melbet account with code FFN to unlock it.",
   "cond_title":"Conditions to download this coupon","cond_intro":"This coupon is 100% free, but reserved for community members. To play it:",
   "steps":["Create an account with promo code <b>FFN</b> on Melbet or 1xBet. <a href='https://youtu.be/EnBk9p_Akvc' rel='nofollow' style='color:var(--gold);font-weight:700;white-space:nowrap'>▶️ See how to create an account</a>","Top up your account with at least <b>3000 FCFA (10$)</b> for activation.","Copy the coupon code below and play it in your app."],
   "coupons_title":"Today's coupons","copy":"📋 Copy code","register":"🌐 Register","apk":"📲 APK","tuto":"▶️ Watch tutorial",
   "cote_label":"Odds","code_word":"Code","min_note":"Minimum activation deposit: 3000 FCFA / 10$.",
   "disc":"⚠️ 18+. No coupon is 100% guaranteed. Play responsibly and only stake what you can afford to lose.",
   "promo_title":"Register with the right code","promo_p":"To download the coupons, your account must be created with code <b>FFN</b>:"},
 "es":{"eyebrow":"⚽ Cupones del día","h1a":"Total ","h1b":"Par / Impar",
   "sub":"El cupón Total Par/Impar del día. Gratis para todas las cuentas creadas con el código FFN.",
   "meta_desc":"Cupón Total Par/Impar gratis, actualizado cada mañana por Cousin Marc. Crea tu cuenta 1xBet o Melbet con el código FFN para desbloquearlo.",
   "cond_title":"Condiciones para descargar este cupón","cond_intro":"Este cupón es 100% gratis, pero reservado a los miembros de la comunidad. Para jugarlo:",
   "steps":["Crea una cuenta con el código promocional <b>FFN</b> en Melbet o 1xBet. <a href='https://youtu.be/EnBk9p_Akvc' rel='nofollow' style='color:var(--gold);font-weight:700;white-space:nowrap'>▶️ Ver cómo crear una cuenta</a>","Recarga tu cuenta con al menos <b>3000 FCFA (10$)</b> para la activación.","Copia el código del cupón abajo y juégalo en tu app."],
   "coupons_title":"Cupones del día","copy":"📋 Copiar código","register":"🌐 Registrarse","apk":"📲 APK","tuto":"▶️ Ver tutorial",
   "cote_label":"Cuota","code_word":"Código","min_note":"Depósito mínimo de activación: 3000 FCFA / 10$.",
   "disc":"⚠️ Solo +18. Ningún cupón está garantizado al 100%. Juega con responsabilidad y apuesta solo lo que puedas permitirte perder.",
   "promo_title":"Regístrate con el código correcto","promo_p":"Para descargar los cupones, tu cuenta debe crearse con el código <b>FFN</b>:"},
 "ar":{"eyebrow":"⚽ قسائم اليوم","h1a":"إجمالي ","h1b":"زوجي / فردي",
   "sub":"قسيمة إجمالي زوجي/فردي لهذا اليوم. مجانية لكل الحسابات المُنشأة بالرمز FFN.",
   "meta_desc":"قسيمة إجمالي زوجي/فردي مجانية، تُحدَّث كل صباح من طرف Cousin Marc. أنشئ حسابك على 1xBet أو Melbet بالرمز FFN لفتحها.",
   "cond_title":"شروط تحميل هذه القسيمة","cond_intro":"هذه القسيمة مجانية 100%، لكنها مخصّصة لأعضاء المجتمع. لتتمكّن من لعبها:",
   "steps":["أنشئ حسابًا بالرمز الترويجي <b>FFN</b> على Melbet أو 1xBet. <a href='https://youtu.be/EnBk9p_Akvc' rel='nofollow' style='color:var(--gold);font-weight:700;white-space:nowrap'>▶️ شاهد كيفية إنشاء حساب</a>","اشحن حسابك بما لا يقل عن <b>3000 فرنك (10$)</b> للتفعيل.","انسخ رمز القسيمة أدناه والعبها في تطبيقك."],
   "coupons_title":"قسائم اليوم","copy":"📋 نسخ الرمز","register":"🌐 التسجيل","apk":"📲 APK","tuto":"▶️ شاهد الشرح",
   "cote_label":"الاحتمال","code_word":"الرمز","min_note":"الحد الأدنى للإيداع للتفعيل: 3000 فرنك / 10$.",
   "disc":"⚠️ للبالغين فقط. لا قسيمة مضمونة 100%. العب بمسؤولية وراهن فقط بما يمكنك تحمّل خسارته.",
   "promo_title":"سجّل بالرمز الصحيح","promo_p":"لتحميل القسائم، يجب إنشاء حسابك بالرمز <b>FFN</b>:"},
}

GH_BASE = "https://raw.githubusercontent.com/fokamjeanmarc2004-cloud/marc-pronostic-api/main"

def _tpi_coupon_cards(L, lang):
    imgmap={"1xbet":f"{GH_BASE}/tpi-1xbet.jpg","melbet":f"{GH_BASE}/tpi-melbet.jpg"}
    out=""
    for c in TPI_COUPONS:
        color=BRAND.get("code-promo-"+c["brand"],"#f2851f")
        img=imgmap.get(c["brand"]) or c["img"]
        btns=f'<a class="cta" href="{c["site"]}" rel="sponsored nofollow">{L["register"]}</a>'
        if c["apk"]: btns+=f'<a class="cta alt" href="{c["apk"]}" rel="sponsored nofollow">{L["apk"]}</a>'
        if c["tuto"]: btns+=f'<a class="cta alt" href="{c["tuto"]}" rel="nofollow">{L["tuto"]}</a>'
        out+=f'''<div style="margin-top:22px;border:1.5px solid {color};border-radius:16px;padding:16px;background:var(--pitch)">
<div translate="no" style="color:{color};font-size:18px;font-weight:800;text-align:center;margin-bottom:12px">{c["book"]}</div>
<img src="{img}" data-gh="{img}" alt="{c["book"]} {L["coupons_title"]}" class="couponimg" style="border-radius:10px">
<div class="btnrow" style="margin-top:14px">{btns}</div>
</div>'''
    return out

def tpi_page(lang):
    L=TPI_L[lang]
    slug=TPI_SLUG[lang]; canonical=f"{BASE}/{slug}"
    navmap={"fr":nav_fr(en=TPI_SLUG["en"],es=TPI_SLUG["es"],ar=TPI_SLUG["ar"]),
            "en":nav_en(fr=TPI_SLUG["fr"],es=TPI_SLUG["es"],ar=TPI_SLUG["ar"]),
            "es":nav_es(fr=TPI_SLUG["fr"],en=TPI_SLUG["en"],ar=TPI_SLUG["ar"]),
            "ar":nav_ar(fr=TPI_SLUG["fr"],en=TPI_SLUG["en"],es=TPI_SLUG["es"])}
    footmap={"fr":footer_html(),"en":footer_html_en(),"es":footer_html_es(),"ar":footer_html_ar()}
    relmap={"fr":related_block(""),"en":related_block_en(""),"es":related_block_es(""),"ar":related_block_ar("")}
    alternates=(f"{BASE}/{TPI_SLUG['fr']}",f"{BASE}/{TPI_SLUG['en']}",f"{BASE}/{TPI_SLUG['es']}",f"{BASE}/{TPI_SLUG['ar']}")
    steps="".join(f"<li>{x}</li>" for x in L["steps"])
    return head(
        f'Coupon {L["h1a"]}{L["h1b"]} Gratuit 2026 (Code FFN) | Cousin Marc' if lang=="fr" else f'{L["h1a"]}{L["h1b"]} Free Coupon 2026 (Code FFN) | Cousin Marc' if lang=="en" else f'Cupón {L["h1a"]}{L["h1b"]} Gratis 2026 (Código FFN) | Cousin Marc' if lang=="es" else f'قسيمة {L["h1a"]}{L["h1b"]} مجانية 2026 (كود FFN) | Cousin Marc',
        L["meta_desc"], canonical, nav=navmap[lang], lang=lang, alternates=alternates) + f"""
<header class="hero" style="padding:30px 0 20px"><div class="wrap">
<p class="eyebrow">{L["eyebrow"]}</p>
<h1>{L["h1a"]}<span class="hl">{L["h1b"]}</span></h1>
<p class="sub">{L["sub"]}</p>
</div></header>
<main class="wrap">
<section style="border-bottom:none;padding-top:24px">
<div style="background:rgba(242,133,31,.10);border:1.5px solid var(--orange);border-radius:16px;padding:22px">
<h2 style="margin-bottom:4px"><span class="num">✅</span> {L["cond_title"]}</h2>
<p style="margin-top:8px">{L["cond_intro"]}</p>
<ol class="steps">{steps}</ol>
<p style="margin-top:10px;color:var(--gold);font-weight:700">{L["min_note"]}</p>
</div>
</section>
<section style="padding-top:10px">
<h2><span class="num">🎟️</span> {L["coupons_title"]}</h2>
{_tpi_coupon_cards(L, lang)}
</section>
<section>
<h2><span class="num">●</span> {L["promo_title"]}</h2>
<p>{L["promo_p"]}</p>
<div class="related">{relmap[lang]}</div>
</section>
<section style="border-bottom:none">
<div class="note">{L["disc"]}</div>
</section>
</main>
{footmap[lang]}
</body></html>"""

# === PAGE RÉSULTATS (preuves de gains) ===
RESULTS_SLUG = {"fr":"resultats.html","en":"results.html","es":"resultados.html","ar":"resultats-ar.html"}

# Liste des preuves (ajouter en HAUT pour que le plus récent soit affiché en premier).
# "type": "img" (jpg/png) ou "video" (mp4). "media": nom du fichier dans le dossier.
RESULTS = [
 {"media":"result-video.mp4","type":"video"},
 {"media":"result-photo.jpg","type":"img"},
]

RESULTS_L = {
 "fr":{"menu":"Résultats","eyebrow":"🏆 Preuves de gains","h1a":"Nos ","h1b":"Résultats",
   "sub":"Les coupons gagnants partagés sur le site. Des preuves réelles, payées.",
   "date":"Date","cote":"Cote","gain":"Gain","status":"Payé","lost":"Perdu","empty":"Les preuves des prochains coupons gagnants apparaîtront ici.","proofalt":"Coupon gagnant Cousin Marc","proofcap":"Preuve filmée depuis l'application",
   "cta":"Pour jouer les coupons du jour, inscris-toi avec le code FFN :",
   "disc":"⚠️ Les gains passés ne garantissent pas les gains futurs. 18+. Joue de façon responsable et mise seulement ce que tu peux perdre."},
 "en":{"menu":"Results","eyebrow":"🏆 Winning proof","h1a":"Our ","h1b":"Results",
   "sub":"The winning coupons shared on the site. Real, paid proof.",
   "date":"Date","cote":"Odds","gain":"Win","status":"Paid","lost":"Lost","empty":"Proof of the next winning coupons will appear here.","proofalt":"Cousin Marc winning coupon","proofcap":"Proof filmed from the app",
   "cta":"To play today's coupons, register with code FFN:",
   "disc":"⚠️ Past wins do not guarantee future wins. 18+. Play responsibly and only stake what you can afford to lose."},
 "es":{"menu":"Resultados","eyebrow":"🏆 Pruebas de ganancias","h1a":"Nuestros ","h1b":"Resultados",
   "sub":"Los cupones ganadores compartidos en el sitio. Pruebas reales, pagadas.",
   "date":"Fecha","cote":"Cuota","gain":"Ganancia","status":"Pagado","lost":"Perdido","empty":"Las pruebas de los próximos cupones ganadores aparecerán aquí.","proofalt":"Cupón ganador Cousin Marc","proofcap":"Prueba grabada desde la app",
   "cta":"Para jugar los cupones del día, regístrate con el código FFN:",
   "disc":"⚠️ Las ganancias pasadas no garantizan ganancias futuras. +18. Juega con responsabilidad y apuesta solo lo que puedas permitirte perder."},
 "ar":{"menu":"النتائج","eyebrow":"🏆 إثباتات الأرباح","h1a":"","h1b":"النتائج",
   "sub":"القسائم الرابحة المنشورة على الموقع. إثباتات حقيقية ومدفوعة.",
   "date":"التاريخ","cote":"الاحتمال","gain":"الربح","status":"مدفوع","lost":"خسارة","empty":"ستظهر هنا إثباتات القسائم الرابحة القادمة.","proofalt":"قسيمة رابحة Cousin Marc","proofcap":"إثبات مصوّر من التطبيق",
   "cta":"للعب قسائم اليوم، سجّل بالرمز FFN:",
   "disc":"⚠️ الأرباح السابقة لا تضمن أرباحًا مستقبلية. للبالغين فقط. العب بمسؤولية وراهن فقط بما يمكنك تحمّل خسارته."},
}

def _result_cards(L, lang):
    if not RESULTS:
        return f'<p style="text-align:center;color:var(--mist)">{L["empty"]}</p>'
    out=""
    for r in RESULTS:
        u=f"{GH_BASE}/{r['media']}"
        if r.get("type")=="video":
            media=f'<video controls preload="metadata" playsinline style="width:100%;border-radius:10px;display:block;background:#000"><source data-gh="{u}" src="{u}" type="video/mp4"></video>'
        else:
            media=f'<img src="{u}" data-gh="{u}" alt="{L["proofalt"]}" class="couponimg" style="border-radius:10px">'
        out+=f'''<div style="margin-top:22px;border:1.5px solid var(--line);border-radius:16px;padding:16px;background:var(--pitch)">
{media}
<div style="display:flex;flex-wrap:wrap;gap:8px 14px;justify-content:center;margin-top:14px;font-size:15px">
<span class="cd" style="color:var(--green-ink);font-weight:800">✅ {L["status"]}</span>
<span class="cd">{L["proofcap"]}</span>
</div>
</div>'''
    return out

def results_page(lang):
    L=RESULTS_L[lang]; slug=RESULTS_SLUG[lang]; canonical=f"{BASE}/{slug}"
    navmap={"fr":nav_fr(en=RESULTS_SLUG["en"],es=RESULTS_SLUG["es"],ar=RESULTS_SLUG["ar"]),
            "en":nav_en(fr=RESULTS_SLUG["fr"],es=RESULTS_SLUG["es"],ar=RESULTS_SLUG["ar"]),
            "es":nav_es(fr=RESULTS_SLUG["fr"],en=RESULTS_SLUG["en"],ar=RESULTS_SLUG["ar"]),
            "ar":nav_ar(fr=RESULTS_SLUG["fr"],en=RESULTS_SLUG["en"],es=RESULTS_SLUG["es"])}
    footmap={"fr":footer_html(),"en":footer_html_en(),"es":footer_html_es(),"ar":footer_html_ar()}
    relmap={"fr":related_block(""),"en":related_block_en(""),"es":related_block_es(""),"ar":related_block_ar("")}
    alternates=(f"{BASE}/{RESULTS_SLUG['fr']}",f"{BASE}/{RESULTS_SLUG['en']}",f"{BASE}/{RESULTS_SLUG['es']}",f"{BASE}/{RESULTS_SLUG['ar']}")
    return head(
        f'{L["h1a"]}{L["h1b"]} | Cousin Marc Pronostic', L["sub"], canonical,
        nav=navmap[lang], lang=lang, alternates=alternates) + f"""
<header class="hero" style="padding:30px 0 20px"><div class="wrap">
<p class="eyebrow">{L["eyebrow"]}</p>
<h1>{L["h1a"]}<span class="hl">{L["h1b"]}</span></h1>
<p class="sub">{L["sub"]}</p>
</div></header>
<main class="wrap">
<section style="border-bottom:none;padding-top:18px">
{_result_cards(L, lang)}
</section>
{winners_wall(lang)}
<section>
<h2><span class="num">●</span> {L["cta"]}</h2>
<div class="related">{relmap[lang]}</div>
</section>
<section style="border-bottom:none">
<div class="note">{L["disc"]}</div>
</section>
</main>
{footmap[lang]}
</body></html>"""

# ===== HISTORIQUE DES COUPONS (rolling 30 jours) =====
# Le plus RECENT en PREMIER. En fin de mois : vider les listes et supprimer les vieilles images.
HIST_L = {
 "fr":{"hist":"Historique (30 derniers jours)"},
 "en":{"hist":"History (last 30 days)"},
 "es":{"hist":"Historial (ultimos 30 dias)"},
 "ar":{"hist":"السجل (آخر 30 يومًا)"},
}

COTE2_HISTORY = [
 {"date":"27/06/2026","img":"coupon-cote2-2026-06-27.jpg"},
]

TPI_HISTORY = [
 {"date":"27/06/2026","x1bet":"coupon-tpi-1xbet-2026-06-27.jpg","melbet":"coupon-tpi-melbet-2026-06-27.jpg"},
]

def cote2_history_html(lang, alt):
    u=f"{GH_BASE}/cote2.jpg"
    return f'<img src="{u}" data-gh="{u}" alt="{alt}" class="couponimg">'

# ===== PAGES PAYS (SEO local) =====
# Chaque pays genere :
#   - 1 page hub  : paris-sportifs-<slug>.html
#   - N pages     : code-promo-<bookmaker>-<slug>.html  (mot-cle exact)
COUNTRIES = [
 {"slug":"cameroun","name":"Cameroun","adj":"camerounais","the":"au Cameroun","in":"au Cameroun",
  "cur":"franc CFA (XAF)","cur_short":"FCFA",
  "momo":["MTN Mobile Money","Orange Money"],
  "extra_pay":"cartes bancaires Visa/Mastercard et cryptomonnaies (USDT, BTC)",
  "cities":"Douala, Yaoundé, Bafoussam, Garoua et Bamenda",
  "foot":"les Lions Indomptables, le championnat Elite One, Coton Sport de Garoua et l'Union Sportive de Douala",
  "books":["code-promo-1xbet","code-promo-melbet","code-promo-paripesa","code-promo-winwin","code-promo-megapari"]},

 {"slug":"cote-divoire","name":"Côte d'Ivoire","adj":"ivoirien","the":"en Côte d'Ivoire","in":"en Côte d'Ivoire",
  "cur":"franc CFA (XOF)","cur_short":"FCFA",
  "momo":["Orange Money","MTN Mobile Money","Moov Money","Wave"],
  "extra_pay":"cartes bancaires et cryptomonnaies (USDT, BTC)",
  "cities":"Abidjan, Bouaké, Yamoussoukro, Daloa et San-Pédro",
  "foot":"les Éléphants, la Ligue 1 ivoirienne, l'ASEC Mimosas et l'Africa Sports",
  "books":["code-promo-1xbet","code-promo-melbet","code-promo-paripesa","code-promo-winwin","code-promo-megapari"]},

 {"slug":"senegal","name":"Sénégal","adj":"sénégalais","the":"au Sénégal","in":"au Sénégal",
  "cur":"franc CFA (XOF)","cur_short":"FCFA",
  "momo":["Orange Money","Wave","Free Money"],
  "extra_pay":"cartes bancaires et cryptomonnaies (USDT, BTC)",
  "cities":"Dakar, Thiès, Touba, Saint-Louis et Ziguinchor",
  "foot":"les Lions de la Teranga, la Ligue 1 sénégalaise, Génération Foot et le Casa Sports",
  "books":["code-promo-1xbet","code-promo-melbet","code-promo-paripesa","code-promo-winwin","code-promo-megapari"]},

 {"slug":"rdc","name":"RDC (Congo-Kinshasa)","adj":"congolais","the":"en RDC","in":"en RDC",
  "cur":"franc congolais (CDF)","cur_short":"CDF",
  "momo":["M-Pesa (Vodacom)","Orange Money","Airtel Money","Africell Money"],
  "extra_pay":"cartes bancaires et cryptomonnaies (USDT, BTC)",
  "cities":"Kinshasa, Lubumbashi, Goma, Bukavu et Kisangani",
  "foot":"les Léopards, la Linafoot, le TP Mazembe et l'AS Vita Club",
  "books":["code-promo-1xbet","code-promo-melbet","code-promo-paripesa","code-promo-winwin"]},

 {"slug":"benin","name":"Bénin","adj":"béninois","the":"au Bénin","in":"au Bénin",
  "cur":"franc CFA (XOF)","cur_short":"FCFA",
  "momo":["MTN Mobile Money","Moov Money","Celtiis Cash"],
  "extra_pay":"cartes bancaires et cryptomonnaies (USDT, BTC)",
  "cities":"Cotonou, Porto-Novo, Parakou et Abomey-Calavi",
  "foot":"les Écureuils, le championnat béninois et les clubs de Cotonou",
  "books":["code-promo-1xbet","code-promo-melbet","code-promo-paripesa","code-promo-winwin"]},

 {"slug":"mali","name":"Mali","adj":"malien","the":"au Mali","in":"au Mali",
  "cur":"franc CFA (XOF)","cur_short":"FCFA",
  "momo":["Orange Money","Moov Money (Malitel)"],
  "extra_pay":"cartes bancaires et cryptomonnaies (USDT, BTC)",
  "cities":"Bamako, Sikasso, Ségou, Mopti et Kayes",
  "foot":"les Aigles du Mali, le Stade Malien de Bamako et le Djoliba AC",
  "books":["code-promo-1xbet","code-promo-melbet","code-promo-paripesa","code-promo-winwin"]},

 {"slug":"togo","name":"Togo","adj":"togolais","the":"au Togo","in":"au Togo",
  "cur":"franc CFA (XOF)","cur_short":"FCFA",
  "momo":["T-Money (Togocom)","Flooz (Moov Africa)"],
  "extra_pay":"cartes bancaires et cryptomonnaies (USDT, BTC)",
  "cities":"Lomé, Sokodé, Kara et Atakpamé",
  "foot":"les Éperviers du Togo, le championnat national et l'ASKO de Kara",
  "books":["code-promo-1xbet","code-promo-melbet","code-promo-paripesa","code-promo-winwin"]},

 {"slug":"burkina-faso","name":"Burkina Faso","adj":"burkinabè","the":"au Burkina Faso","in":"au Burkina Faso",
  "cur":"franc CFA (XOF)","cur_short":"FCFA",
  "momo":["Orange Money","Moov Money"],
  "extra_pay":"cartes bancaires et cryptomonnaies (USDT, BTC)",
  "cities":"Ouagadougou, Bobo-Dioulasso, Koudougou et Banfora",
  "foot":"les Étalons du Burkina, l'ASFA Yennenga et le Rahimo FC",
  "books":["code-promo-1xbet","code-promo-melbet","code-promo-paripesa","code-promo-winwin"]},
]

COUNTRY_ALIASES = {"rdc":["Congo (RDC)","RDC","Congo"],"cote-divoire":["Côte d'Ivoire"],
                   "cameroun":["Cameroun"],"senegal":["Sénégal"],"benin":["Bénin"],"mali":["Mali"],
                   "togo":["Togo"],"burkina-faso":["Burkina Faso"]}

# Pages pays x bookmaker a conserver en URL dediee (verifie sur 3 mois de Search Console,
# 2026-10-06 : 262 / 67 / 18 / 13 impressions respectivement, les 31 autres combos a 0-7
# impressions sur 3 mois sont >=97% identiques textuellement entre elles -> contenu fin/duplique
# qui dilue le positionnement de tout le site. Elles sont desormais redirigees (301) vers la
# page bookmaker generique au lieu d'avoir leur propre URL quasi-copiee-collee.
KEEP_COUNTRY_BK = {
    ("code-promo-melbet", "cameroun"),
    ("code-promo-1xbet", "senegal"),
    ("code-promo-melbet", "rdc"),
    ("code-promo-melbet", "burkina-faso"),
}

def _bk(slug):
    return next(b for b in BOOKMAKERS if b["slug"] == slug)

def _short(b):
    return b["slug"].replace("code-promo-", "")

def _cap(t):
    return t[0].upper() + t[1:]

def cty_bonus(b, c):
    """Montant du bonus pour ce bookmaker dans ce pays (exact si connu, sinon generique)."""
    names = COUNTRY_ALIASES.get(c["slug"], [c["name"]])
    for cname, val in b["countries"]:
        if cname in names:
            return val
    return b["bonus_max"]

def cty_bk_slug(b, c):
    if (b["slug"], c["slug"]) not in KEEP_COUNTRY_BK:
        return b["slug"]
    return f'{b["slug"]}-{c["slug"]}'

def cty_hub_slug(c):
    return f'paris-sportifs-{c["slug"]}'

def cty_momo_list(c):
    return ", ".join(c["momo"][:-1]) + " et " + c["momo"][-1] if len(c["momo"]) > 1 else c["momo"][0]

def cty_momo_rows(c):
    return "\n".join(f'<tr><td>{html.escape(m)}</td><td>Dépôt &amp; retrait</td><td>Quelques minutes</td></tr>' for m in c["momo"])

def cty_table_rows(c):
    rows = ""
    for s in c["books"]:
        b = _bk(s)
        rows += (f'<tr><td><a href="{cty_bk_slug(b,c)}.html" style="color:{BRAND[s]};font-weight:800" translate="no">{b["name"]}</a></td>'
                 f'<td>{html.escape(cty_bonus(b,c))}</td><td style="color:var(--gold);font-weight:800">{b["code"]}</td></tr>\n')
    return rows

def cty_cards(c, current=""):
    out = ""
    for s in c["books"]:
        if s == current:
            continue
        b = _bk(s)
        out += (f'<a class="hubcard" href="{cty_bk_slug(b,c)}.html" style="border-top:3px solid {BRAND[s]}">'
                f'<div class="bk" translate="no">{bk_logo(b, "rlogo", 28)}{b["name"]}</div>'
                f'<div class="bn">{html.escape(cty_bonus(b,c))}</div>'
                f'<span class="cd">Code : {b["code"]}</span></a>\n')
    return out

def cty_other_countries(c):
    out = ""
    for o in COUNTRIES:
        if o["slug"] == c["slug"]:
            continue
        out += f'<a href="{cty_hub_slug(o)}.html"><div class="bk">{html.escape(o["name"])}</div><div class="cd">Codes promo</div></a>\n'
    return out

def cty_faq_jsonld(qs):
    data = {"@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in qs]}
    return json.dumps(data, ensure_ascii=False, indent=2)

# ---------- Page bookmaker x pays ----------
def country_bk_page(b, c):
    name, code = b["name"], b["code"]
    slug = cty_bk_slug(b, c)
    bonus = cty_bonus(b, c)
    momo = cty_momo_list(c)
    qs = [
        (f"Quel est le code promo {name} {c['name']} en 2026 ?",
         f"Le code promo {name} valable {c['the']} en 2026 est {code}. Il se saisit une seule fois à l'inscription et débloque le bonus de bienvenue de {pct(b)} sur le premier dépôt ({bonus})."),
        (f"Comment déposer sur {name} {c['in']} ?",
         f"{c['name']} : les dépôts se font par Mobile Money ({momo}), ainsi que par {c['extra_pay']}. Le dépôt est crédité en quelques minutes."),
        (f"Le code {code} fonctionne-t-il {c['in']} ?",
         f"Oui. Le code {code} est valable {c['the']} tant que tu choisis ce pays et la devise {c['cur']} au moment de l'inscription sur {name}."),
        (f"Comment retirer ses gains {name} {c['in']} ?",
         f"Le retrait se fait vers le même moyen de paiement que le dépôt, généralement Mobile Money ({momo}). Le compte doit être vérifié et le bonus entièrement joué avant le retrait."),
    ]
    extra = f'<script type="application/ld+json">\n{cty_faq_jsonld(qs)}\n</script>'
    _t, _d = _cty_title_desc(b, c,
        f"Code Promo {name} {c['name']} 2026 : {code} → {bonus} | Cousin Marc",
        f"Code promo {name} {c['name']} 2026 : saisis {code} à l'inscription et récupère ton bonus de bienvenue ({bonus}). Dépôt Mobile Money {momo}. Guide par Cousin Marc.")
    return head(
        _t, _d,
        f"{BASE}/{slug}.html", extra, nav=nav_fr(), lang="fr",
        image=f"{BASE}/affiche-" + _short(b) + ".jpg") + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Cousin Marc Pronostic · {c['name']} · Mis à jour {MAJ_FR}</p>
<h1>Code Promo <span class="hl" translate="no">{name}</span> {c['name']} 2026</h1>
<p class="sub">Le code officiel pour les parieurs {c['adj']}s. Bonus de bienvenue <b>{bonus}</b>, dépôt par {momo}.</p>
<div class="codebox">{bk_logo(b, "cblogo", 64)}<div class="stamp"><span class="st-txt">Vérifié par CM</span></div>
<div class="lab">Code promo officiel {c['name']}</div>
<div class="code">{code}</div>
<small>À coller dans le champ « Code promo » à l'inscription</small>
<div><button class="copybtn" aria-label="Copier le code promo {code}" onclick="copyCode(this,'{code}')">📋 Copier le code</button></div>
{reg_block(b)}
</div>
<div class="btnrow">{buttons(b)}</div>
</div></header>
<main class="wrap">
<section>
<h2><span class="num">01</span> Code promo {name} {c['name']} : ce que tu obtiens</h2>
<p>Si tu paries {c['the']}, le code <b style="color:var(--gold)">{code}</b> est le code partenaire à utiliser sur {name}. Il ne coûte rien : il sert uniquement à activer le bonus de bienvenue maximum au moment de l'inscription.</p>
<p>Pour un compte ouvert {c['the']} avec la devise <b>{c['cur']}</b>, le bonus est de <b>{bonus}</b> sur ton premier dépôt.</p>
<div class="note">⚠️ Le code se saisit <b>pendant</b> la création du compte. Une fois le compte créé sans code, il n'est plus possible de l'ajouter.</div>
</section>
<section>
<h2><span class="num">02</span> Inscription {name} {c['in']} : les étapes</h2>
<ol class="steps">
<li><b>Ouvre {name}</b> avec le bouton ci-dessus{" ou télécharge l'application" if b["apps"] else ""}.</li>
<li><b>Choisis « {c['name']} »</b> comme pays et <b>{c['cur_short']}</b> comme devise.</li>
<li><b>Renseigne ton numéro de téléphone {c['adj']}</b> (celui lié à ton compte Mobile Money).</li>
<li><b>Colle le code <span style="color:var(--gold)">{code}</span></b> dans le champ « Code promo ».</li>
<li><b>Dépose via {c['momo'][0]}</b> : le bonus de {pct(b)} est crédité immédiatement.</li>
</ol>
<div class="note" style="display:flex;flex-wrap:wrap;align-items:center;gap:14px;justify-content:space-between">
<span>🎥 Je montre l'inscription complète en vidéo, étape par étape.</span>
<a class="cta" href="https://youtu.be/EnBk9p_Akvc" rel="nofollow" style="background:#ff0000;color:#fff">▶️ Voir le tuto YouTube</a>
</div>
</section>
<section>
<h2><span class="num">03</span> Dépôt et retrait {c['in']}</h2>
<p>{c['name']} fonctionne principalement au Mobile Money. Sur {name}, les moyens disponibles sont :</p>
<div class="tablecard"><table>
<thead><tr><th>Moyen de paiement</th><th>Usage</th><th>Délai</th></tr></thead>
<tbody>
{cty_momo_rows(c)}
</tbody></table></div>
<p style="margin-top:14px">En complément, {name} accepte aussi les {c['extra_pay']}. Pour le retrait, utilise le <b>même moyen que le dépôt</b> : c'est la règle appliquée par presque tous les bookmakers, et elle évite les blocages de vérification.</p>
</section>
<section>
<h2><span class="num">04</span> Parier sur le foot {c['in']}</h2>
<p>{c['name']} est un pays de foot : {c['foot']} font partie des paris les plus suivis par la communauté, à {c['cities']}. Sur {name}, tu retrouves ces compétitions en plus des grands championnats européens (Premier League, Liga, Ligue 1), de la CAN et de la Ligue des Champions CAF.</p>
<p>Mes pronostics du jour sont publiés gratuitement sur Telegram et WhatsApp — beaucoup de membres de la communauté parient depuis {c['name']}.</p>
<div class="btnrow" style="justify-content:flex-start">
<a class="cta" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a>
<a class="cta alt" href="cote-de-2.html">⚽ Coupon Côte de 2</a>
</div>
</section>
{('<section id="calcul-bonus-pays"><h2>Combien tu reçois ' + c['in'] + ' avec le code ' + code + '</h2>'
   '<p>Le bonus ' + name + ' est de 3 fois ton premier dépôt (300%), plafonné à 300 000 FCFA. Exemples :</p>'
   '<div class="tablecard"><table><thead><tr><th>Ton 1er dépôt</th><th>Bonus</th><th>Total pour parier</th></tr></thead><tbody>' + _calc_rows() + '</tbody></table></div>'
   '<p style="margin-top:12px">Avec 100 000 FCFA déposés, tu atteins déjà le bonus maximum. Que tu sois à ' + c['cities'] + ', tout se fait en ligne depuis ton téléphone.</p></section>') if b['slug'] in FFN300 and c['cur_short'] == 'FCFA' else ''}
<section>
<h2>Code promo ou code coupon {name} ?</h2>
<p>Le <b>code promo {code}</b> s'utilise une seule fois, à l'inscription, pour activer ton bonus. Le <b>code coupon</b>, lui, sert à charger un ticket de paris déjà préparé : tu l'entres dans le coupon de {name} et les matchs s'ajoutent à ton ticket. Je partage mes coupons sur Telegram et dans la <a href="cote-de-2.html">côte de 2 du jour</a>.</p>
</section>
<section>
<h2><span class="num">05</span> Questions fréquentes — {name} {c['name']}</h2>
<details open><summary>Le code promo {name} {code} est-il gratuit {c['in']} ?</summary><p>Oui, 100% gratuit. Il ne fait qu'activer le bonus de bienvenue maximum pour un compte {c['adj']}.</p></details>
<details><summary>Quel est le montant du bonus {c['in']} ?</summary><p>Le bonus correspond à {bonus + ' sur ton premier dépôt' if b['slug'] in FFN300 else pct(b) + ' de ton premier dépôt (' + bonus + ')'}. Montant indicatif, il peut évoluer selon les promotions en cours.</p></details>
<details><summary>Puis-je déposer avec {c['momo'][0]} ?</summary><p>Oui. {c['momo'][0]} est l'un des moyens de dépôt les plus utilisés {c['the']} sur {name}. Le compte est crédité en quelques minutes.</p></details>
<details><summary>Faut-il vérifier son compte pour retirer ?</summary><p>Oui. Une pièce d'identité est demandée avant le premier retrait important. Utilise tes vraies informations à l'inscription : un nom qui ne correspond pas à ta pièce bloque le retrait.</p></details>
<details><summary>Je suis {c['adj']} mais je vis à l'étranger, que choisir ?</summary><p>Choisis le pays où tu résides réellement et où se trouve ton moyen de paiement. Le code {code} reste valable dans tous les cas.</p></details>
</section>
<section>
<h2><span class="num">06</span> Autres codes promo {c['in']}</h2>
<p>Compare les bonus des autres bookmakers disponibles {c['the']} :</p>
<div class="hubgrid">
{cty_cards(c, b["slug"])}
</div>
<p style="margin-top:16px"><a href="{cty_hub_slug(c)}.html" style="color:var(--gold);font-weight:700">→ Voir tous les codes promo {c['name']} 2026</a></p>
</section>
<section style="text-align:center;border-bottom:none">
<h2 style="justify-content:center">Prêt à activer ton bonus {c['in']} ?</h2>
<p style="max-width:480px;margin:10px auto 0">Inscris-toi avec le code <b style="color:var(--gold)">{code}</b> et dépose via {c['momo'][0]}.</p>
<div class="btnrow">{buttons(b)}</div>
</section>
</main>
{footer_html()}
{sticky_bar(b,'fr')}
</body></html>"""

# ---------- Page hub pays ----------

# ---------------------------------------------------------------- Contenu propre a chaque pays (pages pays)
# utc = decalage horaire du pays ; op = operateur national historique des jeux ; intro = texte propre au pays
CTY_EXTRA = {
 "cameroun": {"utc": 1, "op": "le PMUC (Pari Mutuel Urbain Camerounais)",
   "intro": "Au Cameroun, la grande majorité des parieurs de la communauté déposent avec MTN Mobile Money ou Orange Money, en francs CFA (XAF). Douala et Yaoundé concentrent l'essentiel des joueurs, qui suivent les Lions Indomptables autant que la Premier League et la Ligue des champions."},
 "cote-divoire": {"utc": 0, "op": "la LONACI (Loterie Nationale de Côte d'Ivoire)",
   "intro": "La Côte d'Ivoire est aujourd'hui le premier pays de la communauté Cousin Marc sur le site, avec Abidjan loin devant les autres villes. On y dépose surtout par Orange Money, MTN Mobile Money, Moov Money et Wave, en francs CFA (XOF)."},
 "senegal": {"utc": 0, "op": "la LONASE (Loterie Nationale Sénégalaise)",
   "intro": "Au Sénégal, Wave et Orange Money dominent les dépôts, en francs CFA (XOF). Les matchs des Lions de la Teranga et les grands championnats européens sont les plus joués par les parieurs de Dakar et de Thiès."},
 "rdc": {"utc": 1, "op": "la SONAL (Société Nationale de Loterie)",
   "intro": "En RDC, on parie en francs congolais (CDF) ou en dollars, avec M-Pesa, Orange Money et Airtel Money. Le TP Mazembe, l'AS Vita Club et les Léopards font partie des matchs les plus suivis, de Kinshasa à Lubumbashi.",
   "tz_note": "Heures de Kinshasa. À Lubumbashi, Goma et Bukavu (une heure de plus), ajoute 1 h."},
 "benin": {"utc": 1, "op": "la LNB (Loterie Nationale du Bénin)",
   "intro": "Au Bénin, MTN Mobile Money et Moov Money sont les moyens de dépôt les plus utilisés, en francs CFA (XOF). Cotonou est la première ville béninoise de la communauté, qui suit de près les Écureuils et la Ligue des champions."},
 "mali": {"utc": 0, "op": "le PMU-Mali",
   "intro": "Au Mali, Orange Money et Moov Money permettent de déposer en quelques minutes, en francs CFA (XOF). Les Aigles, le Stade Malien et le Djoliba AC sont les équipes les plus suivies à Bamako."},
 "togo": {"utc": 0, "op": "la LONATO (Loterie Nationale Togolaise)",
   "intro": "Au Togo, on dépose surtout avec T-Money et Flooz, en francs CFA (XOF). Lomé rassemble la majorité des parieurs togolais de la communauté, qui suivent les Éperviers et les grands championnats européens."},
 "burkina-faso": {"utc": 0, "op": "la LONAB (Loterie Nationale Burkinabè)",
   "intro": "Le Burkina Faso est le deuxième pays de la communauté Cousin Marc sur le site, porté par Ouagadougou et Bobo-Dioulasso. Les dépôts se font surtout par Orange Money et Moov Money, en francs CFA (XOF)."},
}

# Grands matchs (heure de Paris) -> heure locale, en heure d'ete (jusqu'au dernier samedi d'octobre) et en heure d'hiver
KICKOFFS = [("Ligue des champions (match du soir)", 21, 0), ("Ligue des champions (début de soirée)", 18, 45),
            ("Ligue 1 (affiche du dimanche soir)", 20, 45), ("Premier League (samedi après-midi)", 16, 0)]

def cty_kickoff_rows(c):
    utc = CTY_EXTRA.get(c["slug"], {}).get("utc", 0)
    out = ""
    for lab, h, mi in KICKOFFS:
        # Premier League : heure de Londres (UTC+1 l'ete, UTC+0 l'hiver) ; autres : heure de Paris (UTC+2 / UTC+1)
        off_ete, off_hiver = (1, 0) if "Premier" in lab else (2, 1)
        ref = "Londres" if "Premier" in lab else "Paris"
        ete = (h - off_ete + utc) % 24; hiver = (h - off_hiver + utc) % 24
        out += f'<tr><td>{lab}<br><small style="color:var(--muted)">{h}h{mi:02d} à {ref}</small></td><td><b>{ete}h{mi:02d}</b></td><td><b>{hiver}h{mi:02d}</b></td></tr>'
    return out

def country_hub_page(c):
    slug = cty_hub_slug(c)
    momo = cty_momo_list(c)
    first = _bk(c["books"][0])
    qs = [
        (f"Quel est le meilleur code promo paris sportifs {c['name']} en 2026 ?",
         f"Le code {first['code']} est le code partenaire de Cousin Marc, valable {c['the']} sur {first['name']} et sur la plupart des bookmakers partenaires. Il active le bonus de bienvenue (jusqu'à 300% avec le code FFN, soit jusqu'à 300 000 FCFA dans les pays FCFA) sur le premier dépôt."),
        (f"Comment parier {c['in']} avec Mobile Money ?",
         f"{c['name']} : après l'inscription, choisis la devise {c['cur']} puis dépose via {momo}. Le compte est crédité en quelques minutes et le bonus s'active automatiquement."),
        (f"À quelle heure sont les matchs de Ligue des champions {c['in']} ?",
         f"Un match de Ligue des champions à 21h à Paris se joue à {(19 + CTY_EXTRA.get(c['slug'], {}).get('utc', 0))}h {c['in']} jusqu'à fin octobre, puis à {(20 + CTY_EXTRA.get(c['slug'], {}).get('utc', 0))}h après le passage à l'heure d'hiver en Europe."),
        (f"Quel bookmaker choisir {c['in']} ?",
         f"Cela dépend de ton moyen de paiement et des cotes recherchées. {', '.join(_bk(s)['name'] for s in c['books'])} sont tous disponibles {c['the']} et acceptent le Mobile Money local."),
    ]
    extra = f'<script type="application/ld+json">\n{cty_faq_jsonld(qs)}\n</script>'
    return head(
        f"Codes Promo Paris Sportifs {c['name']} 2026 : bonus &amp; Mobile Money | Cousin Marc",
        f"Tous les codes promo paris sportifs {c['name']} 2026 : {', '.join(_bk(s)['name'] for s in c['books'])}. Bonus de bienvenue jusqu'à 300% avec le code FFN, dépôt {momo}. Guide de Cousin Marc.",
        f"{BASE}/{slug}.html", extra, nav=nav_fr(), lang="fr") + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">⚽ Paris sportifs {c['name']} · Mis à jour {MAJ_FR}</p>
<h1>Codes Promo <span class="hl">{c['name']}</span> 2026</h1>
<p class="sub">Les meilleurs bookmakers disponibles {c['the']}, leur bonus en {c['cur_short']} et le code promo à utiliser. Dépôt par {momo}.</p>
<div class="btnrow"><a class="cta" href="#bookmakers">Voir les codes</a><a class="cta alt" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a></div>
</div></header>
<main class="wrap">
<section id="bookmakers" style="padding-top:16px">
<h2><span class="num">01</span> Codes promo {c['in']} : le tableau</h2>
<div class="tablecard"><table>
<thead><tr><th>Bookmaker</th><th>Bonus {c['in']}</th><th>Code</th></tr></thead>
<tbody>
{cty_table_rows(c)}
</tbody></table></div>
<p style="font-size:13px;color:var(--mist);margin-top:12px">Montants indicatifs en {c['cur']}, susceptibles d'évoluer selon les promotions en cours.</p>
<div class="hubgrid" style="margin-top:20px">
{cty_cards(c)}
</div>
</section>
<section>
<h2><span class="num">●</span> Les paris sportifs {c['in']} en bref</h2>
<p>{CTY_EXTRA.get(c['slug'], {}).get('intro', '')}</p>
<p>{_cap(CTY_EXTRA.get(c['slug'], {}).get('op', "l'opérateur national"))} est l'opérateur national historique des jeux et paris {c['the']}. Les bookmakers en ligne de ce site sont internationaux : vérifie toujours la réglementation locale avant de jouer. 18+.</p>
</section>
<section id="heure-des-matchs">
<h2><span class="num">●</span> À quelle heure sont les grands matchs {c['in']} ?</h2>
<p>Les horaires annoncés en Europe ne sont pas ceux {c['the']}. Voici la correspondance pour ne plus rater un coup d'envoi (et placer ton pari à temps) :</p>
<div class="tablecard"><table>
<thead><tr><th>Match</th><th>Heure {c['in']}<br><small>jusqu'à fin octobre</small></th><th>Heure {c['in']}<br><small>de novembre à mars</small></th></tr></thead>
<tbody>
{cty_kickoff_rows(c)}
</tbody></table></div>
<p style="font-size:13px;color:var(--mist);margin-top:10px">{CTY_EXTRA.get(c['slug'], {}).get('tz_note', '')} L'Europe passe à l'heure d'hiver le dernier dimanche d'octobre et revient à l'heure d'été le dernier dimanche de mars.</p>
</section>
{('<section><h2><span class="num">●</span> Mes dernières analyses de match</h2><p>Les grands matchs que j&#x27;analyse cette semaine, avec mon pronostic et la cote :</p>' + matchs_list_html(4) + '<p style="margin-top:12px"><a href="pronostics.html" style="color:var(--gold);font-weight:700">→ Toutes mes analyses</a></p></section>') if MATCHS else ''}
<section>
<h2><span class="num">02</span> Comment ouvrir un compte {c['in']}</h2>
<ol class="steps">
<li><b>Choisis un bookmaker</b> dans le tableau ci-dessus.</li>
<li><b>Sélectionne « {c['name']} »</b> comme pays et <b>{c['cur_short']}</b> comme devise.</li>
<li><b>Entre le code promo</b> dans le champ prévu — sans lui, pas de bonus.</li>
<li><b>Dépose via {c['momo'][0]}</b> : le bonus (jusqu'à 300% avec le code FFN) est crédité immédiatement.</li>
</ol>
<div class="note">⚠️ Utilise tes vraies informations (nom, date de naissance, numéro). Un compte non conforme à ta pièce d'identité est bloqué au moment du retrait.</div>
</section>
<section>
<h2><span class="num">03</span> Dépôt et retrait {c['in']}</h2>
<p>Le Mobile Money reste le moyen le plus rapide {c['the']}. Les opérateurs acceptés par les bookmakers partenaires :</p>
<div class="tablecard"><table>
<thead><tr><th>Moyen de paiement</th><th>Usage</th><th>Délai</th></tr></thead>
<tbody>
{cty_momo_rows(c)}
</tbody></table></div>
<p style="margin-top:14px">Les {c['extra_pay']} sont également acceptés sur la plupart des plateformes. Retire toujours vers le <b>même moyen que ton dépôt</b>.</p>
<p><a href="deposer-retirer-paris-afrique.html" style="color:var(--gold);font-weight:700">→ Mon guide complet dépôt &amp; retrait en Afrique</a></p>
</section>
<section>
<h2><span class="num">04</span> Sur quoi parier {c['in']} ?</h2>
<p>{_cap(c['foot'])} : ce sont les paris les plus suivis par la communauté {c['the']}, de {c['cities']}. À cela s'ajoutent les grands championnats européens, la CAN et la Ligue des Champions CAF.</p>
<p>Je publie chaque jour un coupon gratuit et mes analyses sur Telegram et WhatsApp.</p>
<div class="btnrow" style="justify-content:flex-start">
<a class="cta" href="cote-de-2.html">⚽ Coupon Côte de 2</a>
<a class="cta alt" href="total-pair-impair.html">🎟️ Total Pair/Impair</a>
</div>
</section>
<section>
<h2><span class="num">05</span> Pourquoi me faire confiance ?</h2>
<div class="author"><div class="av">CM</div><div><div class="nm">Cousin Marc</div><div class="ro">Pronostiqueur foot · communauté de 95 000+ abonnés</div></div></div>
<p style="margin-top:16px">Je teste personnellement chaque plateforme (inscription, dépôt Mobile Money, retrait) avant de la recommander. Une grande partie de ma communauté parie depuis {c['name']}.</p>
<div class="social">{social_html()}</div>
</section>
<section>
<h2><span class="num">06</span> Questions fréquentes — paris sportifs {c['name']}</h2>
<details open><summary>Les codes promo sont-ils gratuits {c['in']} ?</summary><p>Oui. Un code promo ne coûte rien : il active simplement le bonus de bienvenue maximum à l'inscription.</p></details>
<details><summary>À quelle heure sont les matchs de Ligue des champions {c['in']} ?</summary><p>Un match à 21h à Paris se joue à <b>{19 + CTY_EXTRA.get(c['slug'], {}).get('utc', 0)}h</b> {c['in']} jusqu'à fin octobre, puis à <b>{20 + CTY_EXTRA.get(c['slug'], {}).get('utc', 0)}h</b> de novembre à mars. Voir <a href="#heure-des-matchs">le tableau des horaires</a>.</p></details>
<details><summary>Quel bonus avec le code FFN {c['in']} ?</summary><p>Avec le code FFN, le bonus de bienvenue va jusqu'à 300% sur le premier dépôt chez les bookmakers partenaires{' (jusqu’à 300 000 FCFA)' if c['cur_short'] == 'FCFA' else ''}. Le montant exact dépend du bookmaker : voir le tableau en haut de page.</p></details>
<details><summary>Puis-je parier depuis mon téléphone {c['in']} ?</summary><p>Oui. Toutes les plateformes du tableau ont une application mobile ou un site optimisé, et acceptent le dépôt par {momo}.</p></details>
<details><summary>Quel est le montant minimum pour parier ?</summary><p>Le dépôt minimum est bas sur la plupart des plateformes. Pour activer certains coupons de la communauté, un dépôt d'environ 3000 {c['cur_short']} (10$) est demandé.</p></details>
<details><summary>Les paris sportifs sont-ils autorisés {c['in']} ?</summary><p>Les paris sportifs en ligne sont pratiqués {c['the']} et réservés aux personnes majeures (18 ans et +). Renseigne-toi sur la réglementation locale en vigueur avant de jouer.</p></details>
</section>
<section>
<h2><span class="num">07</span> Codes promo dans les autres pays</h2>
<div class="related">
{cty_other_countries(c)}
</div>
</section>
<section style="border-bottom:none">
<div class="note">⚠️ Réservé aux 18 ans et +. Le jeu comporte des risques : endettement, dépendance, isolement. Ne mise que ce que tu peux te permettre de perdre. <a href="jeu-responsable.html" style="color:var(--gold)">En savoir plus</a></div>
</section>
</main>
{footer_html()}
</body></html>"""

def country_links_footer():
    return "".join(f'<a href="{cty_hub_slug(c)}.html">{html.escape(c["name"])}</a>' for c in COUNTRIES)

def country_block_for_bk(b):
    """Bloc 'par pays' insere sur la page FR d'un bookmaker.
    Pour un pays sans page dediee (hors KEEP_COUNTRY_BK), on renvoie vers le hub du pays
    plutot que vers cty_bk_slug (qui renverrait vers cette page-ci elle-meme)."""
    cs = [c for c in COUNTRIES if b["slug"] in c["books"]]
    if not cs:
        return ""
    cards = "".join(
        f'<a href="{(cty_bk_slug(b,c)+".html") if (b["slug"],c["slug"]) in KEEP_COUNTRY_BK else (cty_hub_slug(c)+".html")}"><div class="bk">{html.escape(c["name"])}</div>'
        f'<div class="cd">{html.escape(cty_bonus(b,c))}</div></a>' for c in cs)
    return (f'<section><h2><span class="num">●</span> Code promo {b["name"]} par pays</h2>'
            f'<p>Guide détaillé, bonus local et moyens de paiement Mobile Money pour ton pays :</p>'
            f'<div class="related">{cards}</div></section>')

def country_index_cards():
    out = ""
    FLAG = {"cameroun": ("🇨🇲", "#16a34a"), "cote-divoire": ("🇨🇮", "#f97316"), "senegal": ("🇸🇳", "#16a34a"), "rdc": ("🇨🇩", "#0ea5e9"),
            "benin": ("🇧🇯", "#facc15"), "mali": ("🇲🇱", "#facc15"), "togo": ("🇹🇬", "#16a34a"), "burkina-faso": ("🇧🇫", "#dc2626")}
    for c in COUNTRIES:
        n = len(c["books"])
        fl, fc = FLAG.get(c["slug"], ("🌍", "#2563eb"))
        out += (f'<a class="flagc" style="--fc:{fc}" href="{cty_hub_slug(c)}.html"><div class="bk" data-flag="{fl}">{html.escape(c["name"])}</div>'
                f'<div class="cd">{n} bookmakers · {c["cur_short"]}</div></a>\n')
    return out


# =====================================================================
#  1) COMPARATEUR « QUEL BOOKMAKER POUR MOI ? »  (FR)
# =====================================================================
COMPARE_SLUG = "quel-bookmaker-choisir.html"

def _compare_data():
    def card(b, bonus):
        return {"name": b["name"], "code": b["code"], "bonus": bonus, "site": b["site"],
                "guide": b["slug"] + ".html", "logo": "logos/" + _short(b) + ".png",
                "app": bool(b["apps"])}
    data = {"countries": [], "other": [], "crypto": card(_bk("code-promo-1xbit"), _bk("code-promo-1xbit")["bonus_max"])}
    for c in COUNTRIES:
        data["countries"].append({"slug": c["slug"], "name": c["name"], "in": c["in"],
            "pay": c["momo"] + ["Carte bancaire", "Crypto (USDT, BTC)"],
            "hub": cty_hub_slug(c) + ".html",
            "books": [card(_bk(sl), cty_bonus(_bk(sl), c)) for sl in c["books"]]})
    data["other"] = [card(_bk(sl), _bk(sl)["bonus_max"]) for sl in ["code-promo-1xbet", "code-promo-melbet", "code-promo-paripesa"]]
    return json.dumps(data, ensure_ascii=False)

COMPARE_JS = """<script>(function(){
var D=JSON.parse(document.getElementById('cmp-data').textContent),root=document.getElementById('cmp');if(!root)return;
var st={c:null,p:null};
function esc(t){return String(t).replace(/[&<>"]/g,function(m){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m];});}
function chips(el,items,sel,cb){el.innerHTML='';items.forEach(function(it){var b=document.createElement('button');b.type='button';b.className='chip'+(sel===it.v?' on':'');b.setAttribute('data-v',it.v);b.textContent=it.t;b.setAttribute('aria-pressed',sel===it.v?'true':'false');b.onclick=function(){cb(it.v);};el.appendChild(b);});}
function render(){
  var cs=D.countries.map(function(c){return{v:c.slug,t:c.name};}).concat([{v:'autre',t:'Autre pays'}]);
  chips(root.querySelector('.cmp-c'),cs,st.c,function(v){st.c=v;st.p=null;render();});
  var stepP=root.querySelector('.cmp-step-p'),out=root.querySelector('.cmp-out');
  if(!st.c){stepP.hidden=true;out.innerHTML='';return;}
  var C=D.countries.filter(function(x){return x.slug===st.c;})[0];
  var pays=C?C.pay:['Carte bancaire','Crypto (USDT, BTC)'];
  stepP.hidden=false;
  chips(root.querySelector('.cmp-p'),pays.map(function(p){return{v:p,t:p};}),st.p,function(v){st.p=v;render();});
  if(!st.p){out.innerHTML='';return;}
  var books=(C?C.books:D.other).slice(0,3);
  if(/Crypto/.test(st.p)&&!books.some(function(b){return b.name===D.crypto.name;})){books=books.slice(0,2).concat([D.crypto]);}
  var where=C?C['in']:'dans ton pays';
  var h='<p class="cmp-title">Ton top 3 '+esc(where)+' · dépôt '+esc(st.p)+'</p><div class="cmp-list">';
  books.forEach(function(b,i){
    h+='<article class="cmp-card'+(i===0?' best':'')+'">'+(i===0?'<span class="cmp-badge">⭐ Recommandé</span>':'')
     +'<div class="cmp-head"><img class="blogo" src="'+esc(b.logo)+'" alt="Logo '+esc(b.name)+'" width="40" height="40" loading="lazy"><div><b translate="no">'+esc(b.name)+'</b><span>Bonus : '+esc(b.bonus)+(b.app?' · appli mobile':'')+'</span></div></div>'
     +'<div class="tcode"><span translate="no">'+esc(b.code)+'</span><button class="copybtn-mini" onclick="copyCode(this,\\''+esc(b.code)+'\\')">Copier</button></div>'
     +'<div class="tactions"><a class="tgo" href="'+esc(b.site)+'" rel="sponsored nofollow">S\\'inscrire</a><a class="tmore" href="'+esc(b.guide)+'">Guide</a></div></article>';
  });
  h+='</div><p class="cmp-note">Les moyens de paiement proposés peuvent varier : vérifie la caisse du bookmaker avant ton dépôt.'+(C?' <a href="'+esc(C.hub)+'">Tout savoir sur les paris '+esc(C['in'])+' →</a>':'')+'</p>';
  out.innerHTML=h;
  if(window.gtag)gtag('event','comparator_result',{country:st.c,payment:st.p});
}
render();
})();</script>"""

def comparator_html():
    return (f'<div class="cmp" id="cmp">'
            f'<div class="cmp-step"><p class="cmp-q"><span>1</span> Tu es dans quel pays ?</p><div class="chips cmp-c"></div></div>'
            f'<div class="cmp-step cmp-step-p" hidden><p class="cmp-q"><span>2</span> Tu veux déposer comment ?</p><div class="chips cmp-p"></div></div>'
            f'<div class="cmp-out" aria-live="polite"></div>'
            f'<script type="application/json" id="cmp-data">{_compare_data()}</script>'
            f'</div>' + COMPARE_JS)

def compare_page():
    return head("Quel bookmaker choisir ? Comparateur par pays 2026 | Cousin Marc",
        "Trouve en 10 secondes le meilleur bookmaker pour ton pays et ton moyen de paiement (MTN, Orange Money, Wave, crypto), avec le bonus et le code promo.",
        f"{BASE}/{COMPARE_SLUG}") + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Comparateur · Mis à jour {MAJ_FR}</p>
<h1>Quel bookmaker <span class="hl">pour moi ?</span></h1>
<p class="sub">Choisis ton pays et ton moyen de paiement : je te montre les 3 bookmakers les plus adaptés, avec le bonus et le code promo à utiliser.</p>
</div></header>
<main class="wrap">
<section>{comparator_html()}</section>
<section>
<h2><span class="num">?</span> Comment je choisis</h2>
<p>Pour chaque pays, je ne garde que les bookmakers disponibles localement, qui acceptent la devise locale et que j'utilise moi-même. Le premier de la liste est celui que je recommande en priorité.</p>
<p>Un souci avec ton code ? Lis le guide <a href="code-promo-ne-marche-pas.html">« Mon code promo ne marche pas »</a>.</p>
</section>
</main>
{footer_html()}
</body></html>"""

# =====================================================================
#  2) « MON CODE PROMO NE MARCHE PAS ? »  (FR)
# =====================================================================
HELP_SLUG = "code-promo-ne-marche-pas.html"
HELP_QA = [
 ("J'ai oublié de mettre le code promo à l'inscription",
  "Chez la plupart des bookmakers, le code ne peut plus être ajouté une fois le compte créé. Contacte tout de suite le support du bookmaker (chat en direct) en expliquant que tu as oublié le code : certains acceptent de l'ajouter si tu n'as pas encore fait de dépôt. <b>Ne crée surtout pas un deuxième compte</b> : c'est interdit et ça peut bloquer tes gains."),
 ("Le site dit que le code est invalide",
  "Vérifie trois choses : le code est tapé <b>en majuscules et sans espace</b> ; tu l'écris dans le champ « Code promo » (pas « Code parrain » ni « Code ami ») ; et c'est le bon code pour ce bookmaker (voir le tableau plus bas). Si le message persiste, copie-colle le code depuis cette page."),
 ("Mon bonus n'apparaît pas après le dépôt",
  "Le bonus est souvent crédité seulement si : ton premier dépôt atteint le <b>minimum demandé</b> ; ton <b>profil est complet</b> (nom, date de naissance, téléphone confirmé) ; et le bonus de bienvenue sport est <b>activé dans ton profil</b> (rubrique « Bonus » ou « Paramètres du compte » selon le bookmaker). Attends quelques minutes puis contacte le support avec la preuve de dépôt."),
 ("Je n'arrive pas à retirer mon bonus",
  "Un bonus de bienvenue ne se retire pas directement : il faut d'abord le <b>miser un certain nombre de fois</b> sur des paris combinés avec une cote minimale (les « conditions de mise »). Elles sont indiquées dans la page Promotions du bookmaker. Ton argent réel, lui, reste retirable."),
 ("On me demande une vérification d'identité",
  "C'est normal et obligatoire avant un retrait : envoie une pièce d'identité lisible et, si demandé, un selfie. Utilise les mêmes nom et prénom que sur ton compte. Sans vérification, le retrait reste bloqué."),
 ("Mon retrait est bloqué ou refusé",
  "Les causes les plus fréquentes : conditions de mise du bonus non terminées, compte non vérifié, ou retrait demandé vers un moyen de paiement différent de celui du dépôt. Retire de préférence sur le même numéro Mobile Money que celui utilisé pour déposer."),
]

def help_page():
    jsonld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in HELP_QA]},
        ensure_ascii=False)
    rows = "".join(f'<tr><td><span translate="no">{bk_logo(b, "rlogo", 28)}{b["name"]}</span></td><td>{b["code"]}</td>'
                   f'<td><a href="{b["slug"]}.html">Guide</a></td></tr>' for b in BOOKMAKERS)
    qa = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(HELP_QA))
    return head("Code promo qui ne marche pas ? Les solutions (1xBet, Melbet…) | Cousin Marc",
        "Code promo refusé, oublié à l'inscription, bonus non reçu ou retrait bloqué : toutes les solutions pas à pas pour 1xBet, Melbet, Paripesa et les autres.",
        f"{BASE}/{HELP_SLUG}", extra=f'<script type="application/ld+json">{jsonld}</script>') + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Aide · Mis à jour {MAJ_FR}</p>
<h1>Mon code promo <span class="hl">ne marche pas ?</span></h1>
<p class="sub">Code refusé, oublié, bonus absent ou retrait bloqué : voici les solutions qui marchent dans 9 cas sur 10.</p>
<div class="btnrow"><a class="cta" href="#solutions">Voir les solutions</a><a class="cta alt" href="https://t.me/marc_prono" rel="nofollow">Me poser la question</a></div>
</div></header>
<main class="wrap">
<section id="solutions">
<h2><span class="num">01</span> Les problèmes les plus fréquents</h2>
{qa}
</section>
<section>
<h2><span class="num">02</span> Le bon code pour chaque bookmaker</h2>
<p>Attention : tous les bookmakers n'utilisent pas le même code.</p>
<div class="tablecard"><table><thead><tr><th>Bookmaker</th><th>Code</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
<section>
<h2><span class="num">03</span> Toujours bloqué ?</h2>
<p>Envoie-moi une capture d'écran sur Telegram en précisant le bookmaker et ton pays : je t'aide à débloquer la situation.</p>
<div class="btnrow" style="justify-content:flex-start"><a class="cta" href="https://t.me/marc_prono" rel="nofollow">Écrire sur Telegram</a><a class="cta alt" href="{COMPARE_SLUG}">Choisir un autre bookmaker</a></div>
</section>
</main>
{footer_html()}
</body></html>"""

# =====================================================================
#  3) PAGES « MATCH DU JOUR »  (FR) — remplies depuis matchs.txt
# =====================================================================
MATCHS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "matchs.txt")
MATCHS_TEMPLATE = """# =============================================================
#  PRONOSTICS « MATCH DU JOUR » — Cousin Marc
#  Ajoute un bloc par match, separe par une ligne ---
#  Les lignes qui commencent par # sont ignorees.
#  Puis relance :  python build2.py
#
#  Champs :
#    date        : AAAA-MM-JJ HH:MM   (heure du coup d'envoi)
#    competition : ex. Ligue des Champions
#    equipe1     : equipe a domicile
#    equipe2     : equipe a l'exterieur
#    pronostic   : ex. Les deux equipes marquent
#    cote        : ex. 1.75
#    bookmaker   : 1xbet, melbet, paripesa, megapari, winwin, betandyou,
#                  betwiner, linebet, 1xbit, fastparie, afroparie, 1win, goldpari
#    resultat    : (facultatif, apres le match) gagne / perdu / rembourse
#    analyse     : texte libre, sur une ou plusieurs lignes (toujours en dernier)
#
#  Exemple (enleve les # pour l'activer) :
# ---
# date: 2026-10-21 21:00
# competition: Ligue des Champions
# equipe1: PSG
# equipe2: Real Madrid
# pronostic: Les deux equipes marquent
# cote: 1.72
# bookmaker: 1xbet
# analyse: Le PSG marque a domicile depuis 12 matchs.
# Le Real a encaisse au moins un but lors de 4 de ses 5 derniers deplacements.
# =============================================================
"""
_JOURS_FR = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]

def _slugify(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

def load_matchs():
    if not os.path.exists(MATCHS_FILE):
        open(MATCHS_FILE, "w", encoding="utf-8").write(MATCHS_TEMPLATE)
        return []
    out = []
    for block in re.split(r"^\s*---\s*$", open(MATCHS_FILE, encoding="utf-8").read(), flags=re.M):
        lines = [l for l in block.splitlines() if l.strip() and not l.lstrip().startswith("#")]
        if not lines: continue
        m, key = {}, None
        for l in lines:
            mm = re.match(r"^\s*(date|competition|equipe1|equipe2|pronostic_en|pronostic_es|pronostic_ar|pronostic|cote|bookmaker|resultat|images?|analyse)\s*:\s*(.*)$", l, re.I)
            if mm and key != "analyse":
                key = mm.group(1).lower(); m[key] = mm.group(2).strip()
            elif key == "analyse":
                m["analyse"] += "\n" + l.strip()
        need = ["date", "equipe1", "equipe2", "pronostic"]
        if any(not m.get(k) for k in need):
            print("  ! match ignore (champ manquant) :", m.get("equipe1", "?"), "-", m.get("equipe2", "?")); continue
        try:
            m["dt"] = datetime.datetime.strptime(m["date"], "%Y-%m-%d %H:%M")
        except ValueError:
            print("  ! date invalide (format AAAA-MM-JJ HH:MM) :", m["date"]); continue
        bk = "code-promo-" + m.get("bookmaker", "1xbet").lower().replace(" ", "")
        m["bk"] = _bk(bk) if any(b["slug"] == bk for b in BOOKMAKERS) else BOOKMAKERS[0]
        m["slug"] = f'pronostic-{_slugify(m["equipe1"])}-{_slugify(m["equipe2"])}-{m["dt"]:%Y-%m-%d}'
        out.append(m)
    out.sort(key=lambda x: x["dt"], reverse=True)
    return out

MATCHS = load_matchs()

def _date_fr(dt):
    return f'{_JOURS_FR[dt.weekday()]} {dt.day} {_MOIS_FR[dt.month-1]} {dt.year} à {dt:%H:%M}'

_RES_FR = {"gagne": ("✅ Gagné", "win"), "gagné": ("✅ Gagné", "win"), "perdu": ("❌ Perdu", "lose"), "rembourse": ("↩️ Remboursé", "void"), "remboursé": ("↩️ Remboursé", "void")}

def match_card(m, link=True):
    res = _RES_FR.get(m.get("resultat", "").lower())
    status = f'<span class="mstatus {res[1]}">{res[0]}</span>' if res else '<span class="mstatus soon">À venir</span>'
    cote = f'<b>@{html.escape(m["cote"])}</b>' if m.get("cote") else ""
    inner = (f'<div class="mmeta">{html.escape(m.get("competition", "Football"))} · {m["dt"].day} {_MOIS_FR[m["dt"].month-1]} · {m["dt"]:%H:%M}</div>'
             f'<div class="mteams"><b>{html.escape(m["equipe1"])}</b><span>vs</span><b>{html.escape(m["equipe2"])}</b></div>'
             f'<div class="mpick"><span>{html.escape(m["pronostic"])}</span>{cote}</div>{status}')
    return f'<a class="mcard" href="{m["slug"]}.html">{inner}</a>' if link else f'<div class="mcard big">{inner}</div>'

def matchs_list_html(limit=6, exclude=None):
    items = [m for m in MATCHS if m["slug"] != exclude][:limit]
    return f'<div class="mgrid">{"".join(match_card(m) for m in items)}</div>' if items else ""


# ---------------------------------------------------------------- Fiche Google des matchs (SportsEvent)
# Stade de l'equipe qui recoit : (stade, ville, code pays). Ajoute une ligne pour chaque nouvelle equipe a domicile.
HOME_VENUE = {
    "Galatasaray": ("RAMS Park", "Istanbul", "TR"), "Atlético Madrid": ("Riyadh Air Metropolitano", "Madrid", "ES"),
    "Villarreal": ("Estadio de la Cerámica", "Villarreal", "ES"), "RC Lens": ("Stade Bollaert-Delelis", "Lens", "FR"),
    "RB Leipzig": ("Red Bull Arena", "Leipzig", "DE"), "Roma": ("Stadio Olimpico", "Rome", "IT"),
    "Manchester City": ("Etihad Stadium", "Manchester", "GB"), "Bodo Glimt": ("Aspmyra Stadion", "Bodø", "NO"),
    "Feyenoord": ("De Kuip", "Rotterdam", "NL"), "PSG": ("Parc des Princes", "Paris", "FR"),
    "Real Madrid": ("Santiago Bernabéu", "Madrid", "ES"), "Barcelone": ("Spotify Camp Nou", "Barcelone", "ES"),
    "Fenerbahçe": ("Stade Şükrü Saracoğlu", "Istanbul", "TR"), "Liverpool": ("Anfield", "Liverpool", "GB"),
    "Naples": ("Stadio Diego Armando Maradona", "Naples", "IT"), "Porto": ("Estádio do Dragão", "Porto", "PT"),
    "VfB Stuttgart": ("MHPArena", "Stuttgart", "DE"), "Como": ("Stadio Giuseppe Sinigaglia", "Côme", "IT"),
    "Lille": ("Stade Pierre-Mauroy", "Villeneuve-d'Ascq", "FR"), "Aston Villa": ("Villa Park", "Birmingham", "GB"),
    "Bayern Munich": ("Allianz Arena", "Munich", "DE"),
    "Everton": ("Hill Dickinson Stadium", "Liverpool", "GB"), "Strasbourg": ("Stade de la Meinau", "Strasbourg", "FR"),
    "Real Betis": ("Stade du Real Betis", "Séville", "ES"), "Leeds United": ("Elland Road", "Leeds", "GB"),
    "Nottingham Forest": ("City Ground", "Nottingham", "GB"),
    "Le Havre": ("Stade Océane", "Le Havre", "FR"), "Chelsea": ("Stamford Bridge", "Londres", "GB"),
    "Marseille": ("Orange Vélodrome", "Marseille", "FR"), "Manchester United": ("Old Trafford", "Manchester", "GB"),
    "AEK Athènes": ("OPAP Arena", "Athènes", "GR"), "Borussia Dortmund": ("Signal Iduna Park", "Dortmund", "DE"),
    "Milan": ("San Siro", "Milan", "IT"), "Juventus": ("Allianz Stadium", "Turin", "IT"),
    "Udinese": ("Bluenergy Stadium", "Udine", "IT"), "Levante": ("Ciutat de València", "Valence", "ES"),
    "Racing Santander": ("El Sardinero", "Santander", "ES"), "Cameroun": ("Cameroun", "", "CM"),
    "Slavia Prague": ("Fortuna Arena", "Prague", "CZ"),
}
ORGANIZER = {"Ligue des Champions": ("UEFA", "https://www.uefa.com"), "Ligue Europa": ("UEFA", "https://www.uefa.com"),
             "Ligue 1": ("Ligue de Football Professionnel", "https://www.lfp.fr"), "Premier League": ("Premier League", "https://www.premierleague.com"),
             "Liga": ("LaLiga", "https://www.laliga.com"), "CAN": ("CAF", "https://www.cafonline.com")}

def sports_event_ld(m, desc):
    e1, e2 = m["equipe1"], m["equipe2"]
    t1, t2 = {"@type": "SportsTeam", "name": e1}, {"@type": "SportsTeam", "name": e2}
    start = m["dt"]; end = start + datetime.timedelta(hours=2)
    stade, ville, pays = HOME_VENUE.get(e1, (f"Stade de {e1}", "", ""))
    addr = {"@type": "PostalAddress", "addressLocality": ville or e1}
    if pays: addr["addressCountry"] = pays
    org = ORGANIZER.get(m.get("competition", ""), (m.get("competition", "Football"), BASE))
    return {"@context": "https://schema.org", "@type": "SportsEvent", "name": f"{e1} vs {e2}",
            "description": desc, "sport": "Football",
            "startDate": start.strftime("%Y-%m-%dT%H:%M") + "+01:00",   # heures saisies en heure du Cameroun
            "endDate": end.strftime("%Y-%m-%dT%H:%M") + "+01:00",
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "image": [f"{BASE}/og-cousinmarc-v3.jpg"],
            "homeTeam": t1, "awayTeam": t2, "competitor": [t1, t2], "performer": [t1, t2],
            "location": {"@type": "Place", "name": stade, "address": addr},
            "organizer": {"@type": "Organization", "name": org[0], "url": org[1]}}

def match_page(m):
    b = m["bk"]; e1, e2 = m["equipe1"], m["equipe2"]
    title = f'Pronostic {e1} vs {e2} ({m["dt"]:%d/%m}) | Cousin Marc'   # court : Google coupe vers 60 caracteres
    desc = f'Pronostic {e1} - {e2} du {m["dt"].day} {_MOIS_FR[m["dt"].month-1]} {m["dt"].year} ({m.get("competition","football")}) : {m["pronostic"]}' + (f' à la cote {m["cote"]}' if m.get("cote") else "") + ". Analyse de Cousin Marc."
    paras = "".join(f"<p>{html.escape(p.strip())}</p>" for p in m.get("analyse", "").split("\n") if p.strip())
    imgs = [i.strip() for i in (m.get("images") or m.get("image") or "").split(",") if i.strip()]
    tickets = ("".join(f'<figure class="vproof-card"><img src="{html.escape(i)}" alt="Coupon Cousin Marc : {html.escape(e1)} vs {html.escape(e2)}" loading="lazy"></figure>' for i in imgs))
    tickets = f'<div class="vproofs" style="margin-top:16px">{tickets}</div>' if imgs else ""
    jsonld = json.dumps(sports_event_ld(m, desc), ensure_ascii=False)
    others = matchs_list_html(4, exclude=m["slug"])
    return head(html.escape(title), html.escape(desc), f'{BASE}/{m["slug"]}.html', extra=f'<script type="application/ld+json">{jsonld}</script>') + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow"><a href="pronostics.html" style="color:inherit">📊 Toutes les analyses</a> · {html.escape(m.get("competition", "Football"))} · {_date_fr(m["dt"])}</p>
<h1>Pronostic {html.escape(e1)} <span class="hl">vs</span> {html.escape(e2)}</h1>
{match_card(m, link=False)}
<div class="btnrow"><a class="cta" href="{b["site"]}" rel="sponsored nofollow">Jouer ce pronostic sur {b["name"]}</a><button class="cta alt" onclick="copyCode(this,'{b["code"]}')">📋 Code {b["code"]}</button></div>
</div></header>
<main class="wrap">
<section>
<h2><span class="num">01</span> Mon analyse</h2>
{paras or "<p>Analyse détaillée publiée sur Telegram.</p>"}
{f'<h3 style="margin-top:22px">🎫 Mes tickets avec ce match</h3>{tickets}' if tickets else ""}
<div class="note">Un pronostic n'est jamais une certitude. Ne mise que ce que tu peux te permettre de perdre. 18+</div>
</section>
<section>
<h2><span class="num">02</span> Où jouer ce match</h2>
<p>Pas encore de compte ? Inscris-toi sur <b>{b["name"]}</b> avec le code <b>{b["code"]}</b> pour activer le bonus de bienvenue ({bk_bonus(b, "fr")}).</p>
<div class="btnrow" style="justify-content:flex-start"><a class="cta" href="{b["site"]}" rel="sponsored nofollow">S'inscrire sur {b["name"]}</a><a class="cta alt" href="{COMPARE_SLUG}">Quel bookmaker pour moi ?</a></div>
</section>
{f'<section><h2><span class="num">03</span> Autres pronostics</h2>{others}</section>' if others else ""}
</main>
{footer_html()}
{sticky_bar(b, "fr")}
</body></html>"""


# ============================================================
#  OUTIL « AFFICHE PERSONNALISEE » (affiche.html) : fabrique une image avec TON prenom et TON code
#  Le HTML de l'outil est dans promo-images/affiche_tool.html.txt
# ============================================================
AFFICHE_SLUG = "affiche.html"
AFFICHE_TPL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "promo-images", "affiche_tool.html.txt")

def affiche_page():
    ok = [b for b in BOOKMAKERS if os.path.exists(os.path.join(OUT, "logos", b["slug"].replace("code-promo-", "") + ".png"))]
    bks = json.dumps([{"n": b["name"], "c": b["code"], "s": b["slug"].replace("code-promo-", "")} for b in ok], ensure_ascii=False)
    tpl = open(AFFICHE_TPL_FILE, encoding="utf-8").read().replace("__BKS__", bks)
    return head("Fais ton affiche avec ton code promo (gratuit) | Cousin Marc",
                "Outil gratuit : crée une affiche avec ton prénom et ton code promo (FFN) pour la partager sur WhatsApp, Telegram ou Facebook.",
                f"{BASE}/{AFFICHE_SLUG}", show_youtube=False) + tpl + f"\n{footer_html()}\n</body></html>"


# ============================================================
#  ONGLET ANALYSES EN ANGLAIS / ESPAGNOL / ARABE (liste des matchs, analyse complete en francais)
# ============================================================
_JOURS_L = {"en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "es": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
            "ar": ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]}
_MOIS_L = {"en": _MOIS_EN, "es": _MOIS_ES, "ar": _MOIS_AR}
COMP_L = {"Ligue des Champions": {"en": "Champions League", "es": "Liga de Campeones", "ar": "دوري أبطال أوروبا"},
          "Ligue Europa": {"en": "Europa League", "es": "Europa League", "ar": "الدوري الأوروبي"},
          "Ligue 1": {"en": "Ligue 1", "es": "Ligue 1", "ar": "الدوري الفرنسي"},
          "Premier League": {"en": "Premier League", "es": "Premier League", "ar": "الدوري الإنجليزي"},
          "Liga": {"en": "La Liga", "es": "LaLiga", "ar": "الدوري الإسباني"},
          "Serie A": {"en": "Serie A", "es": "Serie A", "ar": "الدوري الإيطالي"},
          "Bundesliga": {"en": "Bundesliga", "es": "Bundesliga", "ar": "الدوري الألماني"},
          "CAN": {"en": "AFCON", "es": "Copa Africana", "ar": "كأس أمم أفريقيا"}}
TEAM_L = {"Cameroun": {"en": "Cameroon", "es": "Camerún"}, "Namibie": {"en": "Namibia", "es": "Namibia"}, "Milan": {"en": "AC Milan", "es": "AC Milan"}, "Inter": {"en": "Inter Milan", "es": "Inter de Milán"}, "Barcelone": {"en": "Barcelona", "es": "Barcelona"}, "Naples": {"en": "Napoli", "es": "Nápoles"},
          "Sporting Portugal": {"en": "Sporting CP", "es": "Sporting de Portugal"},
          "Séville": {"en": "Sevilla", "es": "Sevilla"},
          "Slavia Prague": {"en": "Slavia Prague", "es": "Slavia de Praga"}, "Bayern Munich": {"en": "Bayern Munich", "es": "Bayern de Múnich"},
          "Bodø/Glimt": {"en": "Bodø/Glimt", "es": "Bodø/Glimt"},
          "Lyon": {"en": "Lyon", "es": "Olympique de Lyon"}, "Marseille": {"en": "Marseille", "es": "Olympique de Marsella"},
          "AEK Athènes": {"en": "AEK Athens", "es": "AEK Atenas"}, "Alavés": {"en": "Alavés", "es": "Alavés"}}
AN_L = {
 "en": {"h2": "Upcoming analysed matches", "done": "Finished matches", "all": "All", "soon": "Upcoming", "win": "✅ Won", "lose": "❌ Lost", "void": "↩️ Void",
        "stats": ("predictions published", "upcoming matches", "won", "lost", "success rate"),
        "note": "For each match: my pick and the odds. Tap a match to read my full analysis (in French).", "at": "at", "empty": "New predictions are coming soon. Join the Telegram to be notified."},
 "es": {"h2": "Próximos partidos analizados", "done": "Partidos terminados", "all": "Todo", "soon": "Próximo", "win": "✅ Ganado", "lose": "❌ Perdido", "void": "↩️ Anulado",
        "stats": ("pronósticos publicados", "próximos partidos", "ganados", "perdidos", "de acierto"),
        "note": "Para cada partido: mi pronóstico y la cuota. Toca un partido para leer mi análisis completo (en francés).", "at": "a las", "empty": "Pronto llegan nuevos pronósticos. Únete al Telegram para enterarte."},
 "ar": {"h2": "المباريات القادمة التي حللتها", "done": "المباريات المنتهية", "all": "الكل", "soon": "قادمة", "win": "✅ رابح", "lose": "❌ خاسر", "void": "↩️ ملغى",
        "stats": ("توقعات منشورة", "مباريات قادمة", "رابحة", "خاسرة", "نسبة النجاح"),
        "note": "لكل مباراة: توقعي والاحتمال. اضغط على المباراة لقراءة تحليلي الكامل (بالفرنسية).", "at": "الساعة", "empty": "توقعات جديدة قريبًا. انضم إلى تيليجرام ليصلك التنبيه."},
}

def _team_l(t, lang): return TEAM_L.get(t, {}).get(lang) or TEAM_L.get(t, {}).get("en", t)

def match_card_l(m, lang):
    L = AN_L[lang]
    res = {"gagne": "win", "gagné": "win", "perdu": "lose", "rembourse": "void", "remboursé": "void"}.get(m.get("resultat", "").lower())
    status = f'<span class="mstatus {res}">{L[res]}</span>' if res else f'<span class="mstatus soon">{L["soon"]}</span>'
    comp = COMP_L.get(m.get("competition", ""), {}).get(lang, m.get("competition", "Football"))
    pick = m.get("pronostic_" + lang) or m["pronostic"]
    cote = f'<b>@{html.escape(m["cote"])}</b>' if m.get("cote") else ""
    d = m["dt"]
    when = f'{d.day} {_MOIS_L[lang][d.month-1]} · {d:%H:%M}' if lang != "en" else f'{_MOIS_EN[d.month-1]} {d.day} · {d:%H:%M}'
    return (f'<a class="mcard" href="{m["slug"]}.html" hreflang="fr" data-c="{html.escape(comp)}">'
            f'<div class="mmeta">{html.escape(comp)} · {when}</div>'
            f'<div class="mteams" dir="ltr"><b>{html.escape(_team_l(m["equipe1"], lang))}</b><span>vs</span><b>{html.escape(_team_l(m["equipe2"], lang))}</b></div>'
            f'<div class="mpick"><span>{html.escape(pick)}</span>{cote}</div>{status}</a>')

def analyses_block(lang):
    L = AN_L[lang]
    now = datetime.datetime.now()
    upcoming = sorted([m for m in MATCHS if not m.get("resultat") and m["dt"] >= now - datetime.timedelta(hours=3)], key=lambda m: m["dt"])
    done = sorted([m for m in MATCHS if m not in upcoming], key=lambda m: m["dt"], reverse=True)
    res = [str(m.get("resultat", "")).lower() for m in MATCHS]
    w = sum(r in ("gagne", "gagné") for r in res); l = sum(r == "perdu" for r in res)
    st = L["stats"]
    stats = f'<div><b>{len(MATCHS)}</b>{st[0]}</div><div><b>{len(upcoming)}</b>{st[1]}</div>'
    if w + l:
        stats += f'<div><b>{w}</b>{st[2]}</div><div><b>{l}</b>{st[3]}</div><div><b>{round(100 * w / (w + l))} %</b>{st[4]}</div>'
    comps = sorted({COMP_L.get(m.get("competition", ""), {}).get(lang, m.get("competition", "Football")) for m in MATCHS})
    chips = f'<button type="button" class="chip on" data-f="*">{L["all"]}</button>' + "".join(
        f'<button type="button" class="chip" data-f="{html.escape(c)}">{html.escape(c)}</button>' for c in comps)

    def by_day(lst):
        out, day = "", None
        for m in lst:
            if m["dt"].date() != day:
                if day is not None: out += "</div></div>"
                day = m["dt"].date(); d = m["dt"]
                lab = f'{_JOURS_L[lang][d.weekday()]}, {_MOIS_EN[d.month-1]} {d.day}' if lang == "en" else f'{_JOURS_L[lang][d.weekday()]} {d.day} {_MOIS_L[lang][d.month-1]}'
                out += f'<div class="daygroup"><h3>{lab}</h3><div class="mgrid">'
            out += match_card_l(m, lang)
        return out + ("</div></div>" if day is not None else "")

    up = by_day(upcoming) or f'<p class="muted">{L["empty"]}</p>'
    fin = f'<section id="termines"><h2><span class="num">✓</span> {L["done"]}</h2>{by_day(done)}</section>' if done else ""
    return f"""<style>
.astats{{display:flex;flex-wrap:wrap;gap:10px;margin:6px 0 14px}}
.astats div{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px 16px;font-size:13px;color:var(--muted);font-weight:600}}
.astats b{{display:block;font-family:var(--display);font-size:24px;color:var(--ink)}}
.afilter{{position:sticky;top:64px;z-index:5;background:var(--bg,#fff);padding:10px 0;margin-bottom:6px}}
.daygroup{{margin-top:22px}}
.daygroup h3{{font-size:15px;text-transform:uppercase;letter-spacing:.06em;color:var(--green-ink);margin-bottom:8px}}
</style>
<section id="a-venir">
<h2><span class="num">⚽</span> {L["h2"]}</h2>
<p>{L["note"]}</p>
<div class="astats">{stats}</div>
<div class="afilter chips" role="group">{chips}</div>
{up}
</section>
{fin}
<script>
(function(){{var bs=document.querySelectorAll('.afilter .chip');bs.forEach(function(b){{b.addEventListener('click',function(){{
bs.forEach(function(x){{x.classList.toggle('on',x===b);}});var f=b.getAttribute('data-f');
document.querySelectorAll('#a-venir .mcard,#termines .mcard').forEach(function(c){{c.style.display=(f==='*'||c.getAttribute('data-c')===f)?'':'none';}});
document.querySelectorAll('.daygroup').forEach(function(g){{var v=[].some.call(g.querySelectorAll('.mcard'),function(c){{return c.style.display!=='none';}});g.style.display=v?'':'none';}});
}});}});}})();
</script>"""

# --- Écriture ---
written=[]
open(os.path.join(OUT,"index.html"),"w",encoding="utf-8").write(index_page()); written.append("index.html")
open(os.path.join(OUT,"promo-codes.html"),"w",encoding="utf-8").write(index_page_en()); written.append("promo-codes.html")
for b in BOOKMAKERS:
    open(os.path.join(OUT,f"{en_slug(b)}.html"),"w",encoding="utf-8").write(bookmaker_page_en(b)); written.append(f"{en_slug(b)}.html")
for b in BOOKMAKERS:
    open(os.path.join(OUT,f"{b['slug']}.html"),"w",encoding="utf-8").write(bookmaker_page(b)); written.append(f"{b['slug']}.html")
open(os.path.join(OUT,"pronostics.html"),"w",encoding="utf-8").write(pronostics_page()); written.append("pronostics.html")
open(os.path.join(OUT,COMPARE_SLUG),"w",encoding="utf-8").write(compare_page()); written.append(COMPARE_SLUG)
open(os.path.join(OUT,HELP_SLUG),"w",encoding="utf-8").write(help_page()); written.append(HELP_SLUG)
open(os.path.join(OUT,AFFICHE_SLUG),"w",encoding="utf-8").write(affiche_page()); written.append(AFFICHE_SLUG)
for _m in MATCHS:
    open(os.path.join(OUT,_m["slug"]+".html"),"w",encoding="utf-8").write(match_page(_m)); written.append(_m["slug"]+".html")
print(f"  {len(MATCHS)} page(s) match du jour")
open(os.path.join(OUT,"a-propos.html"),"w",encoding="utf-8").write(apropos_page()); written.append("a-propos.html")
open(os.path.join(OUT,"jeu-responsable.html"),"w",encoding="utf-8").write(jeu_responsable_page()); written.append("jeu-responsable.html")
open(os.path.join(OUT,"actualites.html"),"w",encoding="utf-8").write(actualites_page()); written.append("actualites.html")
open(os.path.join(OUT,"cote-de-2.html"),"w",encoding="utf-8").write(cote_de_2_page()); written.append("cote-de-2.html")
# Pages anglaises (versions complètes)
open(os.path.join(OUT,"predictions.html"),"w",encoding="utf-8").write(predictions_page_en()); written.append("predictions.html")
open(os.path.join(OUT,"about.html"),"w",encoding="utf-8").write(about_page_en()); written.append("about.html")
open(os.path.join(OUT,"responsible-gambling.html"),"w",encoding="utf-8").write(responsible_gambling_page_en()); written.append("responsible-gambling.html")
open(os.path.join(OUT,"news.html"),"w",encoding="utf-8").write(news_page_en()); written.append("news.html")
open(os.path.join(OUT,"odds-of-2.html"),"w",encoding="utf-8").write(odds_of_2_page_en()); written.append("odds-of-2.html")
for a in ARTICLES_EN:
    open(os.path.join(OUT,f"{a['slug']}.html"),"w",encoding="utf-8").write(article_page_en(a)); written.append(f"{a['slug']}.html")
# Pages espagnoles (site complet)
open(os.path.join(OUT,"codigos-promocionales.html"),"w",encoding="utf-8").write(index_page_es()); written.append("codigos-promocionales.html")
for b in BOOKMAKERS:
    open(os.path.join(OUT,f"{es_slug(b)}.html"),"w",encoding="utf-8").write(bookmaker_page_es(b)); written.append(f"{es_slug(b)}.html")
open(os.path.join(OUT,"pronosticos.html"),"w",encoding="utf-8").write(predictions_page_es()); written.append("pronosticos.html")
open(os.path.join(OUT,"acerca-de.html"),"w",encoding="utf-8").write(about_page_es()); written.append("acerca-de.html")
open(os.path.join(OUT,"juego-responsable.html"),"w",encoding="utf-8").write(responsible_gambling_page_es()); written.append("juego-responsable.html")
open(os.path.join(OUT,"noticias.html"),"w",encoding="utf-8").write(news_page_es()); written.append("noticias.html")
open(os.path.join(OUT,"cuota-de-2.html"),"w",encoding="utf-8").write(cuota_de_2_page_es()); written.append("cuota-de-2.html")
for a in ARTICLES_ES:
    open(os.path.join(OUT,f"{a['slug']}.html"),"w",encoding="utf-8").write(article_page_es(a)); written.append(f"{a['slug']}.html")
# Pages arabes (site complet, RTL)
open(os.path.join(OUT,"promo-codes-ar.html"),"w",encoding="utf-8").write(index_page_ar()); written.append("promo-codes-ar.html")
for b in BOOKMAKERS:
    open(os.path.join(OUT,f"{ar_slug(b)}.html"),"w",encoding="utf-8").write(bookmaker_page_ar(b)); written.append(f"{ar_slug(b)}.html")
open(os.path.join(OUT,"pronostics-ar.html"),"w",encoding="utf-8").write(predictions_page_ar()); written.append("pronostics-ar.html")
open(os.path.join(OUT,"a-propos-ar.html"),"w",encoding="utf-8").write(about_page_ar()); written.append("a-propos-ar.html")
open(os.path.join(OUT,"jeu-responsable-ar.html"),"w",encoding="utf-8").write(responsible_gambling_page_ar()); written.append("jeu-responsable-ar.html")
open(os.path.join(OUT,"actualites-ar.html"),"w",encoding="utf-8").write(news_page_ar()); written.append("actualites-ar.html")
open(os.path.join(OUT,"cote-2-ar.html"),"w",encoding="utf-8").write(cote_de_2_page_ar()); written.append("cote-2-ar.html")
for a in ARTICLES_AR:
    open(os.path.join(OUT,f"{a['slug']}.html"),"w",encoding="utf-8").write(article_page_ar(a)); written.append(f"{a['slug']}.html")
# Pages Total Pair/Impair (4 langues)
for _lang, _sl in TPI_SLUG.items():
    open(os.path.join(OUT,_sl),"w",encoding="utf-8").write(tpi_page(_lang)); written.append(_sl)
# (medias copies en bloc plus bas)
# Pages Résultats (4 langues) + médias des preuves
for _lang, _sl in RESULTS_SLUG.items():
    open(os.path.join(OUT,_sl),"w",encoding="utf-8").write(results_page(_lang)); written.append(_sl)
# Copie des medias si le dossier source existe (portable hors environnement Claude)
_MEDIA_SRC = "/home/claude/site"
if os.path.isdir(_MEDIA_SRC):
    for _f in sorted(os.listdir(_MEDIA_SRC)):
        if _f.lower().endswith((".jpg",".jpeg",".png",".webp",".mp4",".gif",".svg",".ico")):
            shutil.copy(os.path.join(_MEDIA_SRC,_f), os.path.join(OUT,_f)); written.append(_f)
for a in ARTICLES:
    open(os.path.join(OUT,f"{a['slug']}.html"),"w",encoding="utf-8").write(article_page(a)); written.append(f"{a['slug']}.html")
for _vlang in ("fr","en","es","ar"):
    _vs=VIP_SLUG[_vlang]
    open(os.path.join(OUT,_vs),"w",encoding="utf-8").write(vip_page(_vlang)); written.append(_vs)
# Pages PAYS (FR) : hub + bookmaker x pays (seuls les combos de KEEP_COUNTRY_BK ont une URL dediee)
for _c in COUNTRIES:
    _hs = f"{cty_hub_slug(_c)}.html"
    open(os.path.join(OUT,_hs),"w",encoding="utf-8").write(country_hub_page(_c)); written.append(_hs)
    for _s in _c["books"]:
        if (_s, _c["slug"]) not in KEEP_COUNTRY_BK:
            continue
        _b = _bk(_s); _bs = f"{cty_bk_slug(_b,_c)}.html"
        open(os.path.join(OUT,_bs),"w",encoding="utf-8").write(country_bk_page(_b,_c)); written.append(_bs)
open(os.path.join(OUT,"sitemap.xml"),"w",encoding="utf-8").write(sitemap()); written.append("sitemap.xml")
_redirects = ""
for _w in sorted(set(x for x in written if x.endswith(".html"))):
    if _w in ("index.html", "google5d6ef3eb30a3bfc3.html"):
        continue
    _redirects += f'\n[[redirects]]\n  from = "/{_w[:-5]}"\n  to = "/{_w}"\n  status = 301\n  force = true\n'
# Redirections des 31 pages pays x bookmaker retirees (contenu >=97% duplique) vers la page
# bookmaker generique correspondante, avec et sans .html (voir KEEP_COUNTRY_BK plus haut).
_retired_redirects = ""
for _c in COUNTRIES:
    for _s in _c["books"]:
        if (_s, _c["slug"]) in KEEP_COUNTRY_BK:
            continue
        _old = f'{_s}-{_c["slug"]}'
        _target = f'{_s}.html'
        _retired_redirects += f'\n[[redirects]]\n  from = "/{_old}"\n  to = "/{_target}"\n  status = 301\n  force = true\n'
        _retired_redirects += f'\n[[redirects]]\n  from = "/{_old}.html"\n  to = "/{_target}"\n  status = 301\n  force = true\n'
# Anciennes affiches PNG (2 Mo) -> JPG legers : garde valides les liens deja partages
_affiche_redirects = "\n# Affiches : anciens PNG remplaces par des JPG legers (< 300 Ko)\n"
for _fn in sorted(AFFICHE_DIMS):
    _affiche_redirects += f'\n[[redirects]]\n  from = "/affiche-{_fn}.png"\n  to = "/affiche-{_fn}.jpg"\n  status = 301\n  force = true\n'
open(os.path.join(OUT,"netlify.toml"),"w",encoding="utf-8").write(
"# Desactive la reecriture d'URL de Netlify (Pretty URLs)\n"
"# Sans ca, /page.html est redirige vers /page => conflit avec les balises canonical\n"
"[build.processing]\n  skip_processing = false\n\n"
"[build.processing.html]\n  pretty_urls = false\n\n"
"# Redirections 301 des anciennes URL sans .html (heritage Pretty URLs)\n"
"# Elles consolident le jus SEO vers l'URL canonique et vident les doublons.\n"
+ _redirects +
"\n# Redirections 301 des pages pays x bookmaker a faible volume, consolidees vers la page\n"
"# bookmaker generique (voir KEEP_COUNTRY_BK) pour reduire le contenu quasi-duplique.\n"
+ _retired_redirects + _affiche_redirects); written.append("netlify.toml")
# Construction automatique par Netlify (depot GitHub) : meme fichier + section [build], a cote du script
_toml_site = open(os.path.join(OUT, "netlify.toml"), encoding="utf-8").read()
_toml_build = ('[build]\n  command = "python build2.py"\n  publish = "site"\n'
               '  ignore = "git diff --quiet $CACHED_COMMIT_REF $COMMIT_REF -- ."\n\n'
               '[build.environment]\n  PYTHON_VERSION = "3.12"\n\n')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "netlify.toml"), "w", encoding="utf-8").write(_toml_build + _toml_site)

def page_404():
    return head("Page introuvable | Cousin Marc Pronostic", "Cette page n'existe plus. Retrouve les codes promo, le coupon du jour et les pronostics de Cousin Marc.",
        f"{BASE}/404.html", nav=nav_fr()) + f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Erreur 404</p>
<h1>Page <span class="hl">introuvable</span></h1>
<p class="sub">Le lien est peut-être ancien. Voici où aller :</p>
<div class="btnrow"><a class="cta" href="index.html">Codes promo</a><a class="cta alt" href="cote-de-2.html">⚽ Coupon du jour</a><a class="cta alt" href="https://t.me/marc_prono" rel="nofollow">✈️ Telegram</a></div>
</div></header>
<main class="wrap"><section style="border-bottom:none"><div class="related">{related_block("")}</div></section></main>
{footer_html()}
</body></html>"""
open(os.path.join(OUT,"404.html"),"w",encoding="utf-8").write(page_404().replace('<meta name="robots" content="index, follow">','<meta name="robots" content="noindex, follow">')); written.append("404.html")
MANIFEST = {
  "name": "Cousin Marc Pronostic",
  "short_name": "Cousin Marc",
  "description": "Codes promo paris sportifs, pronostics et coupons du jour.",
  "start_url": "/index.html",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#070b12",
  "theme_color": "#070b12",
  "lang": "fr",
  "icons": [
    {"src": "favicon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
    {"src": "favicon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
    {"src": "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}
  ]
}
open(os.path.join(OUT,"manifest.json"),"w",encoding="utf-8").write(json.dumps(MANIFEST, ensure_ascii=False, indent=2)); written.append("manifest.json")

CSS += r"""
/* ==========================================================
   HABILLAGE 2026 V2 — plus de couleur, meme contenu
   (CSS seulement : textes, titres et liens inchanges pour Google)
   ========================================================== */
:root{--blue1:#3b82f6;--blue2:#1d4ed8;--navy:#0b1d5c;--gold:#facc15;--tint:#f5f8ff;
  --shadow:0 1px 2px rgba(11,29,92,.05),0 10px 28px rgba(11,29,92,.08);
  --shadow-lg:0 2px 6px rgba(11,29,92,.06),0 28px 64px rgba(11,29,92,.14)}
::selection{background:rgba(250,204,21,.45)}

/* Barre du haut : logo plus vivant */
nav.top .logo .dot{background:linear-gradient(135deg,var(--gold),#f59e0b);box-shadow:0 0 0 4px rgba(250,204,21,.22)}
.topffn{background:linear-gradient(135deg,#fff7d1,#fde68a)!important;border-color:#f59e0b!important;color:var(--navy)!important}

/* Accueil : fond du haut avec halo bleu et lignes de terrain tres legeres */
.home-hero{background:
  radial-gradient(900px 420px at 92% -10%,rgba(59,130,246,.22),transparent 60%),
  radial-gradient(700px 360px at -10% 110%,rgba(250,204,21,.16),transparent 60%),
  url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='300' viewBox='0 0 600 300'%3E%3Cg fill='none' stroke='%231d4ed8' stroke-opacity='.06' stroke-width='2'%3E%3Cpath d='M300 0v300'/%3E%3Ccircle cx='300' cy='150' r='70'/%3E%3Crect x='0' y='75' width='90' height='150'/%3E%3Crect x='510' y='75' width='90' height='150'/%3E%3C/g%3E%3C/svg%3E") center top/900px auto no-repeat,
  linear-gradient(180deg,#f3f7ff,#fff 70%)!important}
.hero{background:radial-gradient(800px 360px at 95% -20%,rgba(59,130,246,.16),transparent 60%),linear-gradient(180deg,#f5f8ff,#fff)}
h1 .hl,.hl{background:linear-gradient(90deg,var(--blue2),var(--blue1));-webkit-background-clip:text;background-clip:text;color:transparent}

/* Sections : alternance de fonds et petit badge au-dessus des titres */
.hsec:nth-of-type(even){background:var(--tint)}
.kicker{display:inline-block;background:linear-gradient(90deg,#e0ebff,#eef4ff);color:var(--blue2);padding:6px 12px;border-radius:999px;font-size:12px}
.hsec-head h2::after,main section>h2::after{content:"";display:block;width:56px;height:4px;border-radius:4px;margin-top:10px;background:linear-gradient(90deg,var(--blue2),var(--blue1) 60%,var(--gold))}
main section>h2{flex-wrap:wrap}
main section>h2::after{flex-basis:100%;max-width:56px}
h2 .num{background:linear-gradient(135deg,var(--blue2),var(--blue1));color:#fff}
.vidtext .kicker,.vhero .kicker,.tgband .kicker{background:rgba(147,197,253,.16);color:#93c5fd}

/* Boutons */
.cta:not(.alt){background:linear-gradient(135deg,var(--blue1),var(--blue2));border-color:transparent;box-shadow:0 8px 22px rgba(29,78,216,.28)}
.cta{transition:transform .15s,box-shadow .15s,filter .15s}
@media(hover:hover){.cta:hover{transform:translateY(-1px)}.cta:not(.alt):hover{box-shadow:0 12px 28px rgba(29,78,216,.36)}}
.tgo{background:linear-gradient(135deg,var(--blue1),var(--blue2))!important;color:#fff!important}

/* Cartes */
.tcard,.mcard,.vproof-card,.hubcard,.related a,.tablecard,.coupon-card,.fact,.vplan,.vmode,.author{border-color:#e4eaf6!important;box-shadow:var(--shadow)}
.tcard{border-top:4px solid var(--blue1)!important}
.tcard:nth-child(2){border-top-color:var(--gold)!important}
.tcard:nth-child(3){border-top-color:#f97316!important}
@media(hover:hover){.related a:hover,.hubcard:hover,.vproof-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg)}}
.vproof-card,.related a,.hubcard{transition:transform .18s,box-shadow .18s}
.mpick{background:linear-gradient(90deg,#eef4ff,#f8fbff)!important;border-color:#bcd2ff!important}
.mstatus.soon{background:#fff7d1;color:#92400e}
.mstatus.win{background:#dcfce7;color:#166534}
.mstatus.lose{background:#fee2e2;color:#991b1b}

/* Codes promo */
.tcode,.bkcodebox{background-color:#f3f7ff!important;border-color:var(--blue1)!important}
.copybtn-mini{background:linear-gradient(135deg,#111827,#0b1d5c)!important}

/* Liste des bookmakers : lignes plus aerees */
.bklist{border-radius:20px;overflow:hidden;box-shadow:var(--shadow);background:#fff}
@media(hover:hover){.bkrow:hover{background:#f8fbff}}

/* Tableaux */
table thead th{background:#eef4ff!important;color:var(--navy)!important}
table tbody tr:nth-child(even){background:#fafcff}

/* Pied de page bleu nuit */
footer{background:linear-gradient(180deg,#0b1d5c,#070f33)!important;border-top:4px solid var(--blue1)}
footer a:hover{color:var(--gold)!important}
footer .warn{border-color:rgba(147,197,253,.25)!important;background:rgba(255,255,255,.03)}

@media(prefers-reduced-motion:reduce){.cta,.vproof-card,.related a,.hubcard{transition:none}}
"""


CSS += r"""
/* ==========================================================
   VERRE LIQUIDE — boutons et cartes comme du plastique transparent rempli d'eau
   (decoratif seulement : textes, titres et liens inchanges)
   ========================================================== */
:root{--lq-rim:inset 0 2px 1px rgba(255,255,255,.7),inset 0 -3px 7px rgba(0,10,60,.22),inset 0 0 0 1px rgba(255,255,255,.16)}

/* 1. Boutons de couleur : goutte brillante (reflet en haut, profondeur en bas) */
.cta,.tgo,.bkjoin,.copybtn-mini,.toptg,.topffn,.chip,.social a,.tmore,.langlink{position:relative;overflow:hidden;isolation:isolate}
.cta::after,.tgo::after,.bkjoin::after,.copybtn-mini::after,.toptg::after,.topffn::after,.chip::after,.social a::after,.tmore::after{
  content:"";position:absolute;left:8%;right:8%;top:2px;height:42%;border-radius:999px;pointer-events:none;z-index:1;
  background:linear-gradient(180deg,rgba(255,255,255,.5),rgba(255,255,255,0));opacity:.6}
.cta:not(.alt),.tgo,.bkjoin,.copybtn-mini,.toptg,.social a{box-shadow:var(--lq-rim),0 8px 20px rgba(29,78,216,.26)!important}
.bkjoin,.tgo{background:linear-gradient(135deg,#3b82f6,#1d4ed8)!important}
.chip[data-v]{box-shadow:inset 0 0 0 999px rgba(0,0,0,.26),var(--lq-rim),0 6px 14px rgba(11,29,92,.18)}
.chip[data-v].on{box-shadow:inset 0 0 0 999px rgba(0,0,0,.1),var(--lq-rim),0 6px 14px rgba(11,29,92,.18)}

/* 2. Boutons clairs : plastique transparent teinte d'eau bleue */
.cta.alt,.tmore,.chip:not([data-v]):not(.on),.langlink,.topffn{
  background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(226,236,255,.78))!important;
  border:1px solid rgba(147,197,253,.75)!important;
  box-shadow:inset 0 2px 1px #fff,inset 0 -7px 14px rgba(59,130,246,.14),0 6px 16px rgba(29,78,216,.10)!important}
.topffn{background:linear-gradient(180deg,#fffbe6,#fde68a)!important;border-color:#f5c542!important;box-shadow:inset 0 2px 1px #fff,inset 0 -6px 12px rgba(217,119,6,.22),0 6px 14px rgba(217,119,6,.18)!important}

/* 3. Logos des bookmakers dans une goutte d'eau */
img.blogo{border-radius:50%;padding:3px;background:radial-gradient(circle at 30% 25%,#fff,rgba(219,234,254,.9) 60%,rgba(147,197,253,.7));
  box-shadow:inset 0 2px 1px #fff,inset 0 -3px 6px rgba(29,78,216,.25),0 0 0 1px rgba(147,197,253,.7),0 6px 14px rgba(29,78,216,.18);object-fit:contain}

/* 4. Cartes : bloc de verre clair (reflet en haut, eau bleutee au fond) */
.tcard,.mcard,.coupon-card,.vproof-card,.hubcard,.fact,.wcard{
  background:linear-gradient(170deg,#fff 0%,#fff 55%,rgba(232,241,255,.95) 100%)!important;
  box-shadow:inset 0 1px 0 #fff,inset 0 -14px 28px rgba(59,130,246,.07),0 1px 2px rgba(11,29,92,.05),0 14px 34px rgba(11,29,92,.10)!important}
.bklist{background:linear-gradient(180deg,#fff,#f6f9ff)!important;box-shadow:inset 0 1px 0 #fff,0 14px 34px rgba(11,29,92,.10)!important}
.tcode,.bkcodebox{background:linear-gradient(180deg,rgba(255,255,255,.95),rgba(224,235,255,.85))!important;box-shadow:inset 0 2px 1px #fff,inset 0 -5px 10px rgba(59,130,246,.12)}

/* 5. Barre du haut et menu : verre depoli */
nav.top{background:linear-gradient(180deg,rgba(255,255,255,.78),rgba(255,255,255,.6))!important;
  -webkit-backdrop-filter:blur(18px) saturate(1.9);backdrop-filter:blur(18px) saturate(1.9);
  box-shadow:inset 0 -1px 0 rgba(255,255,255,.7),0 8px 24px rgba(11,29,92,.06)}
.navpanel{background:linear-gradient(170deg,rgba(255,255,255,.86),rgba(235,243,255,.80))!important;
  -webkit-backdrop-filter:blur(22px) saturate(1.8);backdrop-filter:blur(22px) saturate(1.8);
  border-left:1px solid rgba(255,255,255,.9);box-shadow:inset 2px 0 1px rgba(255,255,255,.9),-20px 0 60px rgba(11,29,92,.18)!important}
.navpanel-links a{border:1px solid transparent;transition:background .2s,border-color .2s}
.navpanel-links a.active,.navpanel-links a:hover{background:linear-gradient(180deg,rgba(255,255,255,.95),rgba(219,234,254,.8))!important;border-color:rgba(147,197,253,.7);box-shadow:inset 0 2px 1px #fff,inset 0 -5px 10px rgba(59,130,246,.12)}
.navpanel.open .navpanel-links a{animation:cm-wet .7s cubic-bezier(.2,.9,.25,1) both}
.navpanel.open .navpanel-links a:nth-child(2){animation-delay:.04s}.navpanel.open .navpanel-links a:nth-child(3){animation-delay:.08s}
.navpanel.open .navpanel-links a:nth-child(4){animation-delay:.12s}.navpanel.open .navpanel-links a:nth-child(5){animation-delay:.16s}
.navpanel.open .navpanel-links a:nth-child(6){animation-delay:.2s}.navpanel.open .navpanel-links a:nth-child(n+7){animation-delay:.24s}

/* 6. Zones bleu nuit (video, bandeau Telegram) : lumieres colorees + vrai verre liquide */
.vidhero,.tgband{background:radial-gradient(420px 260px at 12% 15%,rgba(37,99,235,.55),transparent 70%),radial-gradient(380px 260px at 92% 30%,rgba(124,58,237,.42),transparent 70%),radial-gradient(360px 240px at 60% 110%,rgba(6,182,212,.35),transparent 70%),#0b1033!important}
.vidhero .cta,.tgband .cta,.vhero .cta.alt,footer .cta.alt{background:linear-gradient(160deg,rgba(255,255,255,.22),rgba(255,255,255,.06) 50%,rgba(120,160,255,.12))!important;
  -webkit-backdrop-filter:blur(6px) saturate(1.8);backdrop-filter:blur(6px) saturate(1.8);color:#fff!important;
  border:1.5px solid rgba(255,255,255,.32)!important;
  box-shadow:inset 2px 3px 1px -1px rgba(255,255,255,.85),inset -2px -3px 2px -1px rgba(160,190,255,.35),inset 0 0 22px rgba(255,255,255,.1),0 16px 34px rgba(0,0,20,.45)!important}
.vidtext .kicker,.tgband .kicker{background:linear-gradient(160deg,rgba(255,255,255,.2),rgba(255,255,255,.05))!important;border:1px solid rgba(255,255,255,.28);box-shadow:inset 0 1px 1px rgba(255,255,255,.6)}
.vidhero .yt-facade{box-shadow:inset 0 0 0 1px rgba(255,255,255,.25),0 24px 60px rgba(0,0,20,.55)!important}

/* Choix du moyen de paiement (comparateur) : verre clair, et bleu nuit une fois choisi */
.cmp-c .chip[data-v*=" "]:not(.on),.chip[data-v*=" "]:not(.on){color:var(--ink)!important;text-shadow:none!important;
  background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(226,236,255,.78))!important;border:1px solid rgba(147,197,253,.75)!important;
  box-shadow:inset 0 2px 1px #fff,inset 0 -7px 14px rgba(59,130,246,.14),0 6px 16px rgba(29,78,216,.10)!important}
.cmp-c .chip[data-v*=" "].on,.chip[data-v*=" "].on{color:#fff!important;background:linear-gradient(135deg,#1e3a8a,#0b1d5c)!important;outline:none!important;
  box-shadow:var(--lq-rim),0 8px 18px rgba(11,29,92,.28)!important}

/* 7. Animations : la goutte s'ecrase au toucher, onde d'eau, apparition « mouillee » */
.cm-sq{animation:cm-squish .5s cubic-bezier(.3,1.6,.4,1)!important}
@keyframes cm-squish{0%{transform:scale(1)}25%{transform:scale(1.08,.88)}50%{transform:scale(.95,1.06)}75%{transform:scale(1.02,.98)}100%{transform:scale(1)}}
.cm-rip{position:fixed;z-index:9998;pointer-events:none;border-radius:50%;width:150px;height:150px;margin:-75px 0 0 -75px;
  border:2px solid rgba(96,165,250,.8);box-shadow:0 0 14px rgba(147,197,253,.6),inset 0 0 12px rgba(147,197,253,.5);animation:cm-rip .7s ease-out forwards}
@keyframes cm-rip{from{transform:scale(0);opacity:1}to{transform:scale(1);opacity:0}}
.cm-wet{animation:cm-wet .9s cubic-bezier(.2,.9,.25,1) both}
@keyframes cm-wet{0%{transform:scale(.94,.94)}40%{transform:scale(1.025,.975)}65%{transform:scale(.99,1.012)}85%{transform:scale(1.004,.996)}100%{transform:none}}
@media(prefers-reduced-motion:reduce){.cm-sq,.cm-wet,.navpanel.open .navpanel-links a{animation:none!important}.cm-rip{display:none}}
"""

open(os.path.join(OUT,"style.css"),"w",encoding="utf-8").write(CSS); written.append("style.css")
open(os.path.join(OUT,"robots.txt"),"w",encoding="utf-8").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n"); written.append("robots.txt")
open(os.path.join(OUT,"google5d6ef3eb30a3bfc3.html"),"w",encoding="utf-8").write("google-site-verification: google5d6ef3eb30a3bfc3.html\n"); written.append("google5d6ef3eb30a3bfc3.html")

print("Pages générées :")
for w in written: print(" -", w)

# ---------------------------------------------------------------- Logo Telegram
TG_ICON = ('<svg class="tgi" viewBox="0 0 240 240" aria-hidden="true"><circle cx="120" cy="120" r="114" fill="#229ED9" stroke="#fff" stroke-width="12"/>'
           '<path fill="#fff" d="M53 117.5l109.4-42.2c5.1-1.8 9.5 1.2 7.9 9l-18.6 87.7c-1.4 6.2-5.1 7.7-10.3 4.8l-28.4-20.9-13.7 13.2c-1.5 1.5-2.8 2.8-5.7 2.8l2-28.9 52.6-47.5c2.3-2-.5-3.1-3.5-1.1l-65 40.9-28-8.7c-6.1-1.9-6.2-6.1 1.3-9.1z"/></svg>')
WA_ICON = ('<svg class="tgi" viewBox="0 0 240 240" aria-hidden="true"><circle cx="120" cy="120" r="114" fill="#25D366" stroke="#fff" stroke-width="12"/>'
           '<path fill="#fff" d="M120 58a61 61 0 0 0-52.6 92.2L59 182l32.8-8.4A61 61 0 1 0 120 58zm0 111.5a50.4 50.4 0 0 1-25.7-7l-1.8-1.1-19.5 5 5.2-19-1.2-1.9A50.5 50.5 0 1 1 120 169.5zm27.7-37.8c-1.5-.8-9-4.4-10.4-4.9s-2.4-.8-3.4.8-3.9 4.9-4.8 5.9-1.8 1.1-3.3.4a41.4 41.4 0 0 1-20.6-18c-1.6-2.7 1.6-2.5 4.5-8.4.5-1 .3-1.9-.1-2.7l-4.6-11.2c-1.2-2.9-2.4-2.5-3.4-2.6h-2.9a5.6 5.6 0 0 0-4 1.9 17 17 0 0 0-5.3 12.6c0 7.4 5.4 14.6 6.2 15.6s10.6 16.2 25.7 22.7c9.5 4.1 13.3 4.5 18 3.8 2.9-.4 9-3.7 10.3-7.2s1.3-6.6.9-7.2-1.3-1-2.8-1.7z"/></svg>')
_n = 0
for _f in os.listdir(OUT):
    if _f.endswith(".html"):
        _p = os.path.join(OUT, _f)
        _t = _t0 = open(_p, encoding="utf-8").read()
        _t = _t.replace("✈️ ", TG_ICON).replace("✈️", TG_ICON)
        _t = re.sub(r'(<a[^>]*whatsapp[^>]*>)💬 ?', lambda m: m.group(1) + WA_ICON, _t)
        if _t != _t0:
            open(_p, "w", encoding="utf-8").write(_t); _n += 1
print(f"  logos Telegram/WhatsApp mis dans {_n} page(s)")
