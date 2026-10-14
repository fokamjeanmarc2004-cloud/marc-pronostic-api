# -*- coding: utf-8 -*-
"""Visuels du canal Telegram Cousin Marc : une image neuve pour chaque message de 6h et de 21h.

    python scripts/visuels.py 2026-11        -> fabrique tout le mois de novembre
    python scripts/visuels.py 2026-11 --demo -> quelques exemples seulement (dossier promo/visuels/demo)

Chaque mois a son propre style (themes qui tournent d'un mois a l'autre) et, dans le mois,
chaque image a sa mise en page, ses couleurs et sa phrase : aucune image n'est publiee deux fois.
Les images sont rangees dans promo/visuels/AAAA-MM/JJ-matin.jpg et JJ-soir.jpg.
Le bot (worker/src/index.js) prend l'image du jour ; si elle n'existe pas, il garde l'ancienne image.
"""
import calendar, datetime, glob, html, json, os, random, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGOS = os.path.join(ROOT, "promo", "logos")
OUT = os.path.join(ROOT, "promo", "visuels")
W, H = 1080, 1350

# ------------------------------------------------------------------ Sujets (meme ordre que PROMOS dans worker/src/messages.js)
BK = {"1xbet": "1xBet", "melbet": "Melbet", "paripesa": "Paripesa", "winwin": "WinWin", "megapari": "Megapari",
      "goldpari": "GoldPari", "1win": "1win", "afroparie": "Afroparie", "linebet": "Linebet", "betandyou": "BetAndYou",
      "fastparie": "Fastparie", "betwiner": "Betwiner"}
B300 = "300% sur ton 1er dépôt"
B300b = "jusqu'à 300 000 FCFA"

TOPICS = [
 {"k": "Inscription", "h": ["Inscris-toi avec le code FFN", "Ton compte en 2 minutes", "Un seul code pour 4 bookmakers", "Commence aujourd'hui avec FFN"],
  "sub": "1xBet · Paripesa · Melbet · WinWin", "code": "FFN", "big": "300%", "line": B300, "line2": B300b,
  "logos": ["1xbet", "paripesa", "melbet", "winwin"], "cta": "Liens et tuto dans le message"},
 {"k": "VIP", "h": ["Rejoins le VIP Cousin Marc", "Le VIP, c'est ici", "Passe au niveau supérieur", "Mes meilleurs coupons en premier"],
  "sub": "Côte de 2 VIP chaque jour · Grosses cotes · Live", "big": "VIP", "line": "Dès 30 $ par mois", "line2": "Orange Money · MTN · crypto",
  "rows": [("Côte de 2 VIP", "tous les jours"), ("Grosses cotes", "plusieurs fois par semaine"), ("Pronostics en live", "pendant les matchs"), ("Canal privé", "questions directes")],
  "cta": "Infos et paiement dans le message", "vip": True},
 {"k": "1xBet", "h": ["Pas encore de compte 1xBet ?", "1xBet : ton bonus t'attend", "Ouvre ton compte 1xBet", "1xBet avec le code FFN"],
  "sub": "Dépôt et retrait par Mobile Money", "code": "FFN", "big": "300%", "line": B300, "line2": B300b, "logos": ["1xbet"], "cta": "Lien d'inscription dans le message"},
 {"k": "Comparateur", "h": ["Quel bookmaker choisir ?", "Ton top 3 en 10 secondes", "Le bon bookmaker pour ton pays", "Ne choisis plus au hasard"],
  "sub": "Ton pays + ton moyen de paiement = ton top 3", "big": "TOP 3", "line": "Orange Money · MTN · Wave · crypto", "line2": "Gratuit sur le site",
  "logos": ["1xbet", "melbet", "paripesa", "winwin", "megapari", "goldpari"], "cta": "Lien du comparateur dans le message",
  "rows": [("Choisis ton pays", "Cameroun, Côte d'Ivoire, Sénégal, RDC…"), ("Choisis ton paiement", "Orange Money, MTN, Wave ou crypto"), ("Reçois ton top 3", "avec le bon code promo")]},
 {"k": "Melbet", "h": ["Melbet : ton bonus t'attend", "Inscris-toi sur Melbet", "Melbet avec le code FFN", "Ton compte Melbet en 2 minutes"],
  "sub": "Même code, même bonus", "code": "FFN", "big": "300%", "line": B300, "line2": B300b, "logos": ["melbet"], "cta": "Lien d'inscription dans le message"},
 None,  # coupon du jour : c'est la vraie photo du coupon qui est publiee
 {"k": "1win", "h": ["1win : jusqu'à 500% de bonus", "Le plus gros bonus du moment", "1win avec le code ESS22", "Ouvre ton compte 1win"],
  "sub": "Sur tes 4 premiers dépôts", "code": "ESS22", "big": "500%", "line": "jusqu'à 500% de bonus", "line2": "Code ESS22 (pas FFN)", "logos": ["1win"], "cta": "Lien d'inscription dans le message"},
 {"k": "Aide", "h": ["Ton code promo ne marche pas ?", "Bonus pas reçu ?", "Bloqué à l'inscription ?", "On règle ton problème"],
  "sub": "Code refusé · bonus absent · retrait bloqué", "big": "?", "line": "Toutes les solutions sur le site", "line2": "Sinon écris-moi en privé",
  "rows": [("Code refusé", "la solution pas à pas"), ("Code oublié", "ce qu'on peut encore faire"), ("Bonus pas reçu", "les vérifications"), ("Retrait bloqué", "les bons réflexes")],
  "cta": "Lien de l'aide dans le message"},
 {"k": "Paripesa", "h": ["Paripesa : même code, même bonus", "Inscris-toi sur Paripesa", "Paripesa avec le code FFN", "Ton compte Paripesa en 2 minutes"],
  "sub": "Site et application", "code": "FFN", "big": "300%", "line": B300, "line2": B300b, "logos": ["paripesa"], "cta": "Lien d'inscription dans le message"},
 {"k": "VIP", "h": ["Les grosses cotes, c'est dans le VIP", "Cotes à 5, 8, 10 et plus", "Les gros tickets en priorité", "Vise plus haut avec le VIP"],
  "sub": "Côte de 2 du jour + live + grosses cotes", "big": "x10", "line": "Dès 30 $ par mois", "line2": "Mes tickets gagnants sur le site",
  "rows": [("Grosses cotes", "partagées en priorité"), ("Côte de 2", "chaque jour"), ("Live", "pendant les matchs")], "cta": "Infos VIP dans le message", "vip": True},
 {"k": "WinWin", "h": ["WinWin : inscris-toi avec FFN", "Ton bonus WinWin t'attend", "WinWin avec le code FFN", "Ouvre ton compte WinWin"],
  "sub": "Android et iPhone", "code": "FFN", "big": "300%", "line": B300, "line2": B300b, "logos": ["winwin"], "cta": "Liens Android et iPhone dans le message"},
 {"k": "Megapari · GoldPari", "h": ["2 autres bookmakers avec FFN", "Megapari et GoldPari", "Encore plus de choix avec FFN", "Même code, 2 bookmakers"],
  "sub": "Le même bonus chez les deux", "code": "FFN", "big": "300%", "line": B300, "line2": B300b, "logos": ["megapari", "goldpari"], "cta": "Liens dans le message"},
 {"k": "Tous mes codes", "h": ["Tous mes codes promo", "Le bon code pour chaque site", "Garde cette image", "Mes codes, au même endroit"],
  "sub": "Le code s'entre une seule fois, à l'inscription", "big": "4 codes", "line": "Tous les liens sur le site", "line2": "cousinmarc-pronostic.com",
  "codes": [("FFN", ["1xbet", "melbet", "paripesa", "winwin", "megapari", "goldpari"]), ("ESS22", ["1win", "linebet"]), ("FJM", ["betandyou", "fastparie"]), ("CMF", ["betwiner"])],
  "cta": "Tous les liens dans le message"},
 {"k": "Stickers · Affiche", "h": ["Stickers, emojis et affiche FFN", "Fais ton affiche avec ton code", "Les emojis FFN sont là", "Partage le code FFN avec style"],
  "sub": "Emojis animés · stickers · affiche personnalisée", "code": "FFN", "big": "FFN", "line": "Affiche gratuite avec ton prénom", "line2": "Partage-la à tes amis",
  "cta": "Liens dans le message",
  "rows": [("Emojis animés FFN", "à ajouter en un clic sur Telegram"), ("Stickers Cousin Marc", "pour tes discussions"), ("Ton affiche perso", "avec ton prénom et ton code")]},
]

# ------------------------------------------------------------------ Styles du mois (un theme par mois, ils tournent)
THEMES = [
 {"name": "verre-clair", "dark": False, "bg": "#eaf2ff",
  "pal": [("#3b82f6", "#a855f7", "#22d3ee", "#facc15"), ("#2563eb", "#06b6d4", "#f472b6", "#fde047"), ("#4f46e5", "#0ea5e9", "#34d399", "#fbbf24"),
          ("#1d4ed8", "#ec4899", "#38bdf8", "#facc15"), ("#7c3aed", "#3b82f6", "#2dd4bf", "#fb923c"), ("#0284c7", "#8b5cf6", "#4ade80", "#fde047")]},
 {"name": "nuit-neon", "dark": True, "bg": "#060a24",
  "pal": [("#2563eb", "#7c3aed", "#06b6d4", "#facc15"), ("#1d4ed8", "#db2777", "#22d3ee", "#fde047"), ("#4338ca", "#0ea5e9", "#10b981", "#fbbf24"),
          ("#6d28d9", "#2563eb", "#f43f5e", "#facc15"), ("#0369a1", "#9333ea", "#14b8a6", "#fb923c"), ("#1e40af", "#c026d3", "#38bdf8", "#fde047")]},
 {"name": "noir-or", "dark": True, "bg": "#0b0904",
  "pal": [("#b45309", "#facc15", "#78350f", "#fde68a"), ("#a16207", "#f59e0b", "#422006", "#fef3c7"), ("#92400e", "#eab308", "#1c1917", "#fde047"),
          ("#ca8a04", "#d97706", "#292524", "#fef9c3"), ("#854d0e", "#fbbf24", "#44403c", "#fde68a"), ("#b45309", "#fcd34d", "#1f2937", "#fffbeb")]},
 {"name": "coucher-soleil", "dark": False, "bg": "#fff1e6",
  "pal": [("#f97316", "#ec4899", "#facc15", "#8b5cf6"), ("#ef4444", "#f59e0b", "#f472b6", "#6366f1"), ("#fb7185", "#fb923c", "#fde047", "#a855f7"),
          ("#f43f5e", "#f97316", "#facc15", "#3b82f6"), ("#e11d48", "#fbbf24", "#fb923c", "#7c3aed"), ("#ea580c", "#db2777", "#fde047", "#2563eb")]},
 {"name": "stade-neon", "dark": True, "bg": "#03140c",
  "pal": [("#16a34a", "#22d3ee", "#a3e635", "#facc15"), ("#059669", "#3b82f6", "#84cc16", "#fde047"), ("#15803d", "#06b6d4", "#4ade80", "#fbbf24"),
          ("#047857", "#0ea5e9", "#bef264", "#facc15"), ("#166534", "#2dd4bf", "#a3e635", "#fde68a"), ("#065f46", "#38bdf8", "#86efac", "#fde047")]},
 {"name": "ocean-glace", "dark": False, "bg": "#e6fbff",
  "pal": [("#06b6d4", "#3b82f6", "#a78bfa", "#facc15"), ("#0ea5e9", "#14b8a6", "#818cf8", "#fde047"), ("#0891b2", "#6366f1", "#2dd4bf", "#fbbf24"),
          ("#0284c7", "#22d3ee", "#c084fc", "#facc15"), ("#0e7490", "#60a5fa", "#5eead4", "#fde68a"), ("#0369a1", "#38bdf8", "#a5b4fc", "#fde047")]},
]
LAYOUTS = ["hero", "ticket", "bulle", "liste"]

def theme_for(year, month):
    return THEMES[(year * 12 + month - (2026 * 12 + 10)) % len(THEMES)]

def topic_index(day, slot, n=14):
    days = (day - datetime.date(2026, 1, 1)).days
    return (days * 2 + slot) % n

# ------------------------------------------------------------------ Dessin
def logo_uri(slug):
    return "file:///" + os.path.join(LOGOS, slug + ".png").replace("\\", "/")

def ball_svg(size, op=1):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" style="opacity:{op}"><defs><radialGradient id="bg{size}" cx="35%" cy="30%">'
            f'<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#cbd5e1"/></radialGradient></defs>'
            f'<circle cx="50" cy="50" r="48" fill="url(#bg{size})" stroke="#0f172a" stroke-width="2"/>'
            '<polygon points="50,30 69,44 62,66 38,66 31,44" fill="#0f172a"/>'
            '<path d="M50 30 L50 4 M69 44 L94 36 M62 66 L78 88 M38 66 L22 88 M31 44 L6 36" stroke="#0f172a" stroke-width="3"/>'
            '<path d="M50 4 L36 2 M50 4 L64 2 M94 36 L98 50 M94 36 L86 20 M78 88 L88 76 M78 88 L64 97 M22 88 L36 97 M22 88 L12 76 M6 36 L14 20 M6 36 L2 50" stroke="#0f172a" stroke-width="3"/></svg>')

def css(th, pal, rnd):
    dark = th["dark"]
    c1, c2, c3, c4 = pal
    ink = "#ffffff" if dark else "#0b1d5c"
    mute = "rgba(255,255,255,.78)" if dark else "#334155"
    glass_bg = ("linear-gradient(160deg,rgba(255,255,255,.20),rgba(255,255,255,.05) 50%,rgba(255,255,255,.10))" if dark
                else "linear-gradient(160deg,rgba(255,255,255,.78),rgba(255,255,255,.42) 55%,rgba(255,255,255,.62))")
    glass_bd = "rgba(255,255,255,.38)" if dark else "rgba(255,255,255,.95)"
    orbs = ""
    spots = [(rnd.randint(-15, 40), rnd.randint(-10, 25)), (rnd.randint(55, 100), rnd.randint(15, 45)), (rnd.randint(-10, 45), rnd.randint(55, 90)), (rnd.randint(50, 100), rnd.randint(65, 105))]
    for (x, y), c in zip(spots, (c1, c2, c3, c4)):
        orbs += f"radial-gradient({rnd.randint(420, 640)}px {rnd.randint(380, 600)}px at {x}% {y}%,{c}{'cc' if dark else 'b3'},transparent 70%),"
    extra = ""
    if th["name"] == "stade-neon":
        extra = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1080' height='1350'%3E%3Cg fill='none' stroke='%23a3e635' stroke-opacity='.22' stroke-width='4'%3E"
                 "%3Crect x='60' y='60' width='960' height='1230' rx='8'/%3E%3Cpath d='M60 675h960'/%3E%3Ccircle cx='540' cy='675' r='150'/%3E%3Crect x='300' y='60' width='480' height='200'/%3E%3Crect x='300' y='1090' width='480' height='200'/%3E%3C/g%3E%3C/svg%3E\"),")
    if th["name"] == "noir-or":
        extra = "repeating-linear-gradient(115deg,rgba(250,204,21,.05) 0 2px,transparent 2px 26px),"
    return f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:Inter,'Segoe UI',Arial,sans-serif;color:{ink};background:{extra}{orbs}{th['bg']};position:relative}}
.grain{{position:absolute;inset:0;background-image:radial-gradient(rgba({'255,255,255' if dark else '11,29,92'},.06) 1px,transparent 1px);background-size:6px 6px;pointer-events:none}}
.disp{{font-family:'Bricolage Grotesque','Segoe UI Black',Arial,sans-serif;font-weight:800;letter-spacing:-.035em}}
.glass{{position:relative;background:{glass_bg};border:2px solid {glass_bd};border-radius:48px;
  box-shadow:inset 4px 6px 2px -2px rgba(255,255,255,{'.75' if dark else '1'}),inset -4px -6px 6px -2px {c2}55,inset 0 0 50px rgba(255,255,255,{'.08' if dark else '.35'}),0 40px 80px {'rgba(0,0,20,.55)' if dark else c1 + '33'};
  backdrop-filter:blur(26px) saturate(1.8);-webkit-backdrop-filter:blur(26px) saturate(1.8)}}
.glass::after{{content:"";position:absolute;left:6%;top:3%;width:46%;height:16%;border-radius:50%;background:linear-gradient(180deg,rgba(255,255,255,{'.45' if dark else '.85'}),rgba(255,255,255,0));filter:blur(3px);pointer-events:none}}
.top{{position:absolute;left:64px;right:64px;top:56px;display:flex;align-items:center;justify-content:space-between}}
.brand{{display:flex;align-items:center;gap:16px;font-size:40px}}
.dot{{width:30px;height:30px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff7c2,#facc15 55%,#d97706);box-shadow:0 0 26px #facc15}}
.brand b{{color:{c1 if not dark else '#93c5fd'}}}
.pill{{padding:16px 28px;border-radius:999px;font-weight:800;font-size:28px;letter-spacing:.04em}}
.kick{{display:inline-block;padding:14px 30px;border-radius:999px;font-weight:800;font-size:30px;letter-spacing:.14em;text-transform:uppercase;color:{ink}}}
.h1{{font-size:104px;line-height:.98}}
.h1 em{{font-style:normal;background:linear-gradient(90deg,{(c4 + ',' + c2) if th['name'] == 'noir-or' else ((c3 + ',' + c4) if dark else (c1 + ',' + c2))});-webkit-background-clip:text;background-clip:text;color:transparent}}
.sub{{font-size:38px;font-weight:600;color:{mute};line-height:1.3}}
.big{{font-size:300px;line-height:.85;background:linear-gradient(180deg,{'#fff' if dark else c1} 10%,{c2} 95%);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 18px 30px {c2}55)}}
.drop .big{{background:linear-gradient(180deg,#0b1d5c 10%,{c1} 95%);-webkit-background-clip:text;background-clip:text;filter:drop-shadow(0 8px 14px rgba(255,255,255,.5))}}
.code{{font-size:170px;letter-spacing:.08em;line-height:1}}
.gold{{background:linear-gradient(180deg,{'#fff7c2,#facc15 45%,#d97706' if dark else '#f59e0b,#d97706 45%,#92400e'});-webkit-background-clip:text;background-clip:text;color:transparent}}
.code.gold{{background:linear-gradient(180deg,#fff7c2,#facc15 45%,#d97706);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 10px 18px rgba(217,119,6,.45))}}
.logo{{border-radius:28%;background:#fff;box-shadow:0 14px 30px rgba(0,0,0,.25),0 0 0 6px rgba(255,255,255,.65)}}
.drop{{border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle at 30% 25%,rgba(255,255,255,.95),rgba(255,255,255,.35) 55%,{c3}55);
  border:3px solid rgba(255,255,255,.9);box-shadow:inset 0 6px 4px rgba(255,255,255,.9),inset 0 -14px 24px {c1}44,0 30px 60px {c1}44}}
.cta{{position:absolute;left:64px;right:64px;bottom:120px;display:flex;align-items:center;justify-content:center;gap:18px;padding:30px;border-radius:999px;font-weight:800;font-size:36px;color:#fff;
  background:linear-gradient(135deg,{c1},{c2});box-shadow:inset 0 4px 2px rgba(255,255,255,.55),inset 0 -8px 16px rgba(0,0,40,.25),0 24px 50px {c1}66}}
.foot{{position:absolute;left:0;right:0;bottom:48px;text-align:center;font-size:26px;font-weight:700;color:{mute};letter-spacing:.06em}}
.bub{{position:absolute;border-radius:50%;background:radial-gradient(circle at 30% 28%,rgba(255,255,255,.95) 0 10%,rgba(255,255,255,.35) 30%,{c3}33 65%,transparent 72%);border:2px solid rgba(255,255,255,.7)}}
.row{{display:flex;align-items:center;gap:26px;padding:22px 32px;border-radius:34px}}
.row .n{{width:64px;height:64px;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:32px;color:#fff;background:linear-gradient(135deg,{c1},{c2});flex:0 0 auto;box-shadow:inset 0 3px 2px rgba(255,255,255,.5)}}
.row b{{font-size:40px;display:block}}.row small{{font-size:29px;color:{mute};font-weight:600}}
"""

def bubbles(rnd, n=7):
    out = ""
    for _ in range(n):
        s = rnd.randint(30, 150)
        out += f'<i class="bub" style="width:{s}px;height:{s}px;left:{rnd.choice([rnd.randint(-50, 60), rnd.randint(W - 140, W - 20)])}px;top:{rnd.randint(140, H - 260)}px;opacity:{rnd.uniform(.35, .9):.2f}"></i>'
    return out

def head_html(t, headline):
    words = headline.split()
    # met en couleur les 1 a 2 derniers mots forts
    k = 2 if len(words) > 3 else 1
    return html.escape(" ".join(words[:-k])) + " <em>" + html.escape(" ".join(words[-k:])) + "</em>"

def top_html(t, th):
    pill = ('<span class="pill glass" style="border-radius:999px">VIP · dès <b>30 $</b></span>' if t.get("vip_day")
            else f'<span class="pill glass" style="border-radius:999px">CODE <b>{html.escape(t.get("code", "FFN"))}</b></span>')
    return f'<div class="top"><div class="brand disp"><span class="dot"></span>cousin <b>marc</b></div>{pill}</div>'

def logos_row(slugs, size):
    return "".join(f'<span class="drop" style="width:{size + 50}px;height:{size + 50}px"><img class="logo" src="{logo_uri(s)}" width="{size}" height="{size}"></span>' for s in slugs)

def lines(txt, per):
    return max(1, -(-len(txt) // per))

def layout_hero(t, th, rnd, headline):
    logos = t.get("logos", [])
    top = 190 + 84 + 34 + lines(headline, 17) * 102 + 24 + 50 + 44
    body = f"""
<div style="position:absolute;left:64px;right:64px;top:190px">
  <span class="kick glass">{html.escape(t['k'])}</span>
  <div class="h1 disp" style="margin-top:34px">{head_html(t, headline)}</div>
  <div class="sub" style="margin-top:24px">{html.escape(t['sub'])}</div>
</div>
<div class="glass" style="position:absolute;left:64px;right:64px;top:{top}px;padding:40px 46px;display:flex;align-items:center;gap:40px">
  <div style="flex:1">
    <div class="big disp" style="font-size:{200 if len(t['big']) <= 4 else 140}px">{html.escape(t['big'])}</div>
    <div style="font-size:40px;font-weight:800;margin-top:14px">{html.escape(t['line'])}</div>
    <div class="sub" style="font-size:32px">{html.escape(t['line2'])}</div>
  </div>
  <div style="display:grid;grid-template-columns:repeat({2 if len(logos) > 2 else 1},auto);gap:18px">{logos_row(logos[:4], 110 if len(logos) > 1 else 170)}</div>
</div>"""
    return body

def layout_ticket(t, th, rnd, headline):
    code = t.get("code") or t["big"]
    logos = t.get("logos", [])
    return f"""
<div style="position:absolute;left:64px;right:64px;top:180px;text-align:center">
  <span class="kick glass">{html.escape(t['k'])}</span>
  <div class="h1 disp" style="margin-top:34px;font-size:92px">{head_html(t, headline)}</div>
</div>
<div class="glass" style="position:absolute;left:90px;right:90px;top:{250 + 84 + 34 + lines(headline, 19) * 92 + 40}px;padding:36px 40px 34px;text-align:center;border-radius:56px">
  <div style="font-size:30px;font-weight:800;letter-spacing:.3em;opacity:.8">{'CODE PROMO' if t.get('code') else 'COUSIN MARC'}</div>
  <div class="code disp gold" style="margin:10px 0 4px;font-size:{150 if len(code) <= 3 else 124}px">{html.escape(code)}</div>
  <div style="border-top:5px dashed rgba(127,127,127,.35);margin:14px -40px 22px;position:relative">
    <i style="position:absolute;left:-28px;top:-30px;width:56px;height:56px;border-radius:50%;background:{th['bg']}"></i>
    <i style="position:absolute;right:-28px;top:-30px;width:56px;height:56px;border-radius:50%;background:{th['bg']}"></i></div>
  <div style="font-size:44px;font-weight:900">{html.escape(t['line'])}</div>
  <div class="sub" style="font-size:32px;margin-top:6px">{html.escape(t['line2'])}</div>
  <div style="display:flex;justify-content:center;gap:12px;margin-top:20px">{logos_row(logos[:6], 60 if len(logos) > 3 else 80)}</div>
</div>"""

def layout_bulle(t, th, rnd, headline):
    logos = t.get("logos") or []
    main = logos[0] if logos else None
    inner = (f'<img class="logo" src="{logo_uri(main)}" width="200" height="200">' if main and len(logos) == 1
             else f'<div class="big disp" style="font-size:{150 if len(t["big"]) <= 4 else 100}px;text-align:center">{html.escape(t["big"])}</div>')
    side = "right:70px" if rnd.random() < .5 else "left:70px"
    align = "left" if "right" in side else "right"
    return f"""
<div class="drop" style="position:absolute;{side};top:165px;width:470px;height:470px">{inner}</div>
<div style="position:absolute;left:64px;right:64px;top:680px;text-align:{align}">
  <span class="kick glass">{html.escape(t['k'])}</span>
  <div class="h1 disp" style="margin-top:24px;font-size:{88 if len(headline) < 30 else 76}px">{head_html(t, headline)}</div>
  <div class="glass" style="display:inline-flex;align-items:center;gap:22px;margin-top:30px;padding:22px 34px;border-radius:999px">
    <span style="font-size:38px;font-weight:900">{html.escape(t['line'])}</span>
    {f'<span class="disp" style="font-size:44px;color:#d97706">· {html.escape(t["code"])}</span>' if t.get('code') else ''}
  </div>
</div>"""

def layout_liste(t, th, rnd, headline):
    if t.get("codes"):
        rows = "".join(f'<div class="row glass"><span class="disp" style="font-size:58px;min-width:230px;color:#d97706">{c}</span>'
                       f'<span style="display:flex;gap:10px;flex-wrap:wrap">{"".join(f"<img class=logo src={logo_uri(s)} width=62 height=62>" for s in sl)}</span></div>'
                       for c, sl in t["codes"])
    elif t.get("rows"):
        rows = "".join(f'<div class="row glass"><span class="n">{i + 1}</span><span><b>{html.escape(a)}</b><small>{html.escape(b)}</small></span></div>' for i, (a, b) in enumerate(t["rows"]))
    else:
        logos = t.get("logos", [])
        items = [(t["line"], "bonus de bienvenue"), (t["line2"], t["sub"]), ("Code " + t.get("code", "FFN"), "à entrer une seule fois, à l'inscription")]
        rows = "".join(f'<div class="row glass"><span class="n">{i + 1}</span><span><b>{html.escape(a)}</b><small>{html.escape(b)}</small></span></div>' for i, (a, b) in enumerate(items))
        if logos:
            rows = f'<div style="display:flex;gap:18px;margin-bottom:6px">{logos_row(logos[:4], 96)}</div>' + rows
    return f"""
<div style="position:absolute;left:64px;right:64px;top:190px">
  <span class="kick glass">{html.escape(t['k'])}</span>
  <div class="h1 disp" style="margin-top:26px;font-size:{86 if len(headline) < 28 else 74}px">{head_html(t, headline)}</div>
  <div style="display:flex;flex-direction:column;gap:16px;margin-top:32px">{rows}</div>
</div>"""


# ------------------------------------------------------------------ Rappel VIP du jour (13h) : un vrai ticket gagnant chaque jour
PREUVES = json.load(open(os.path.join(ROOT, "promo", "preuves", "preuves.json"), encoding="utf-8")) if os.path.exists(os.path.join(ROOT, "promo", "preuves", "preuves.json")) else []
VIP_H = ["Rejoins le VIP aujourd'hui", "Ce ticket est passé dans le VIP", "Mes meilleurs coupons sont dans le VIP",
         "Les grosses cotes, c'est dans le VIP", "Joue avec mes coupons VIP", "Encore un ticket gagnant VIP",
         "Tu veux mes coupons avant tout le monde ?", "Le VIP, c'est maintenant", "Passe au niveau supérieur",
         "Mes tickets VIP de la semaine"]
VIP_T = {"k": "Canal VIP", "cta": "Rejoins le VIP : infos dans le message", "vip_day": True,
         "rows": [("Côte de 2 VIP", "tous les jours"), ("Grosses cotes", "plusieurs fois par semaine"), ("Pronostics en live", "pendant les matchs"), ("Canal privé", "questions directes")]}
VIP_LAYOUTS = ["vip-preuve", "vip-preuve-g", "vip-liste"]

def _clean(t):
    return re.sub(r"^[^\w(]+", "", t).strip()

def preuve_uri(f):
    return "file:///" + os.path.join(ROOT, "promo", "preuves", f).replace("\\", "/")

def _proof_card(pr, w, rot):
    gain = f'<div style="font-size:28px;font-weight:800;margin-top:6px;white-space:nowrap">Gain : <span class="gold disp" style="font-size:36px;white-space:nowrap">{html.escape(pr["gain"])}</span></div>' if pr.get("gain") else ""
    return f"""<div class="glass" style="width:{w}px;padding:18px;border-radius:40px;transform:rotate({rot}deg)">
<div style="border-radius:26px;overflow:hidden;height:{int(w * 1.12)}px;background:#fff"><img src="{preuve_uri(pr['file'])}" style="width:100%;display:block"></div>
<div style="margin-top:14px;font-size:26px;font-weight:700;opacity:.85;line-height:1.25">{html.escape(_clean(pr['titre']))[:70]}</div>
<div style="font-size:30px;font-weight:800;margin-top:6px">Cote : <span class="gold disp" style="font-size:44px">{html.escape(pr['cote'])}</span></div>{gain}
</div>"""

def layout_vip_preuve(t, th, rnd, headline, left=False):
    pr = t["proof"]
    side = "left:60px" if left else "right:60px"
    tx = "right:60px;text-align:right" if left else "left:64px"
    return f"""
<div style="position:absolute;{side};top:170px">{_proof_card(pr, 470, rnd.choice([-3, -2, 2, 3]))}</div>
<div style="position:absolute;{tx};top:190px;width:430px">
  <span class="kick glass">VIP</span>
  <div class="h1 disp" style="margin-top:26px;font-size:{74 if len(headline) < 28 else 64}px">{head_html(t, headline)}</div>
  <div class="sub" style="margin-top:20px;font-size:32px">Côte de 2 VIP chaque jour, grosses cotes et live.</div>
  <div class="glass" style="display:inline-block;margin-top:26px;padding:20px 30px;border-radius:30px">
    <div style="font-size:26px;font-weight:800;opacity:.85">À partir de</div>
    <div class="disp gold" style="font-size:86px;line-height:1">30 $</div>
    <div style="font-size:26px;font-weight:800;opacity:.85">par mois</div></div>
</div>
<div style="position:absolute;left:64px;right:64px;top:1010px;text-align:center;font-size:28px;font-weight:700;opacity:.8">Orange Money · MTN · crypto · Aucun gain n'est garanti</div>"""

def layout_vip_liste(t, th, rnd, headline):
    pr = t["proof"]
    rows = "".join(f'<div class="row glass"><span class="n">{i + 1}</span><span><b>{html.escape(a)}</b><small>{html.escape(b)}</small></span></div>' for i, (a, b) in enumerate(t["rows"][:3]))
    return f"""
<div style="position:absolute;left:64px;top:190px;width:560px">
  <span class="kick glass">Canal VIP</span>
  <div class="h1 disp" style="margin-top:26px;font-size:{78 if len(headline) < 28 else 66}px">{head_html(t, headline)}</div>
  <div style="display:flex;flex-direction:column;gap:14px;margin-top:30px">{rows}</div>
</div>
<div style="position:absolute;right:40px;top:330px">{_proof_card(pr, 360, 4)}</div>"""

def page(t, th, pal, layout, headline, seed):
    rnd = random.Random(seed)
    body = {"hero": layout_hero, "ticket": layout_ticket, "bulle": layout_bulle, "liste": layout_liste,
            "vip-preuve": layout_vip_preuve, "vip-preuve-g": lambda *a: layout_vip_preuve(*a, left=True),
            "vip-liste": layout_vip_liste}[layout](t, th, rnd, headline)
    deco = bubbles(rnd, rnd.randint(5, 9))
    ball = f'<div style="position:absolute;{rnd.choice(["right:-70px", "left:-70px"])};top:{rnd.randint(980, 1080)}px;transform:rotate({rnd.randint(0, 90)}deg)">{ball_svg(rnd.randint(150, 210), .9)}</div>' if layout not in ("bulle", "vip-preuve", "vip-preuve-g", "vip-liste") else ""
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Inter:wght@600;700;800;900&display=block" rel="stylesheet">
<style>{css(th, pal, rnd)}</style></head><body><div class="grain"></div>{deco}{ball}{top_html(t, th)}{body}
<div class="cta">{html.escape(t['cta'])} &#8595;</div>
<div class="foot">cousinmarc-pronostic.com · 18+ · Joue de façon responsable</div></body></html>"""

def chrome():
    for c in (os.environ.get("CHROME"), shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chromium-browser"),
              r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
        if c and os.path.exists(c): return c
    sys.exit("Chrome introuvable")

def render(html_text, out_jpg):
    from PIL import Image
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "v.html"); png = os.path.join(d, "v.png")
        open(src, "w", encoding="utf-8").write(html_text)
        subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        f"--window-size={W},{H}", "--virtual-time-budget=6000", "--force-device-scale-factor=1",
                        f"--screenshot={png}", "file:///" + src.replace("\\", "/")], check=True, capture_output=True, timeout=120)
        im = Image.open(png).convert("RGB")
        if im.size != (W, H): im = im.crop((0, 0, W, H))
        im.save(out_jpg, quality=82, optimize=True, progressive=True)

def plan_month(year, month):
    th = theme_for(year, month)
    count = {}
    jobs = []
    for d in range(1, calendar.monthrange(year, month)[1] + 1):
        day = datetime.date(year, month, d)
        for slot, name in ((0, "matin"), (1, "soir")):
            ti = topic_index(day, slot)
            t = TOPICS[ti]
            if t is None: continue
            k = count.get(ti, 0); count[ti] = k + 1
            # chaque repetition du meme sujet dans le mois change de mise en page, de couleurs et de phrase
            layout = LAYOUTS[(k + ti + month) % len(LAYOUTS)]
            if layout == "liste" and not (t.get("rows") or t.get("codes")) and k % 2: layout = "hero"
            pal = th["pal"][(k * 2 + ti) % len(th["pal"])]
            headline = t["h"][(k + k // len(LAYOUTS) + year + month) % len(t["h"])]
            jobs.append((day, name, t, th, pal, layout, headline, f"{day}-{name}"))
        if PREUVES:
            n = (day - datetime.date(2026, 1, 1)).days
            tv = dict(VIP_T, proof=PREUVES[(n * 5) % len(PREUVES)])
            jobs.append((day, "vip", tv, th, th["pal"][(n + 3) % len(th["pal"])], VIP_LAYOUTS[n % len(VIP_LAYOUTS)],
                         VIP_H[(n + n // len(VIP_H)) % len(VIP_H)], f"{day}-vip"))
    return th, jobs

def main():
    ym = sys.argv[1] if len(sys.argv) > 1 else (datetime.date.today().replace(day=28) + datetime.timedelta(days=7)).strftime("%Y-%m")
    year, month = map(int, ym.split("-"))
    demo = "--demo" in sys.argv
    th, jobs = plan_month(year, month)
    folder = os.path.join(OUT, "demo" if demo else f"{year:04d}-{month:02d}")
    os.makedirs(folder, exist_ok=True)
    if demo:
        seen, pick = set(), []
        for j in jobs:
            if j[5] not in seen or len(pick) < 4:
                if j[5] in seen and len(pick) >= 4: continue
                seen.add(j[5]); pick.append(j)
            if len(pick) >= 6: break
        jobs = pick
    start = datetime.date.fromisoformat(sys.argv[sys.argv.index("--from") + 1]) if "--from" in sys.argv else None
    for day, name, t, th_, pal, layout, headline, seed in jobs:
        if start and day < start: continue
        out = os.path.join(folder, f"{day.day:02d}-{name}.jpg" if not demo else f"{th['name']}-{day.day:02d}-{name}-{layout}.jpg")
        render(page(t, th_, pal, layout, headline, seed), out)
        print(os.path.relpath(out, ROOT), "|", t["k"], "|", layout, "|", headline)
    # on garde seulement le mois en cours et le mois fabrique (les anciens sont effaces)
    if not demo:
        keep = {f"{year:04d}-{month:02d}", datetime.date.today().strftime("%Y-%m")}
        for d in glob.glob(os.path.join(OUT, "20??-??")):
            if os.path.basename(d) not in keep:
                shutil.rmtree(d); print("efface", os.path.basename(d))

if __name__ == "__main__":
    main()
