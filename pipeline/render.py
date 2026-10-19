#!/usr/bin/env python3
"""CarteGrise4x — générateur de vidéos verticales 1080x1920 (TikTok, Reels, Shorts).

Chaîne 100 % libre : Piper (voix FR), Pillow (images), NumPy (musique générée), FFmpeg (encodage).

  python3 render.py concepts.json            # rend toutes les vidéos manquantes dans out/
  python3 render.py concepts.json --only C012 --force
"""
import json, math, os, re, subprocess, sys, wave, hashlib, argparse, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
A = lambda p: os.path.join(ROOT, "assets", p)
FD = A("bricolage-grotesque-latin-700-800.ttf")   # titres (police du site)
FB = A("figtree-latin-700-normal.ttf")            # texte
FR = A("figtree-latin-600-normal.ttf")
PIPER = os.path.join(ROOT, "bin", "piper", "piper")
VOICE = os.path.join(ROOT, "voices", "fr-siwis-medium.onnx")

# Charte cartegrise4x.fr
NAVY = (11, 18, 32); INK = (15, 26, 46); EU = (11, 58, 143); EU2 = (21, 80, 196)
SUN = (255, 197, 49); WHITE = (255, 255, 255); SOFT = (185, 195, 214); OK = (76, 203, 133); BAD = (255, 123, 123)

THEMES = {  # fond par catégorie : variété visuelle entre les 3 vidéos du jour
    "acquisition": ((11, 18, 32), (14, 46, 110)),
    "pedagogie":   ((10, 22, 40), (16, 70, 92)),
    "conversion":  ((16, 14, 34), (60, 40, 120)),
}

_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

# ---------------------------------------------------------------- texte
def nbsp(text):
    return re.sub(r" ([?!:;»€%])", "\u00a0\\1", text).replace("« ", "«\u00a0")

def wrap(d, text, f, maxw):
    lines = []
    for para in nbsp(text).split("\n"):
        cur = ""
        for w in [x for x in para.split(" ") if x]:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= maxw: cur = t
            else:
                if cur: lines.append(cur)
                cur = w
        lines.append(cur)
    return lines

def fit(d, text, path, maxw, maxh, start, minsize=34, spacing=1.12):
    s = start
    while s > minsize:
        f = font(path, s); ls = wrap(d, text, f, maxw)
        if len(ls) * s * spacing <= maxh and all(d.textlength(l, font=f) <= maxw for l in ls): return f, ls
        s -= 4
    f = font(path, minsize); return f, wrap(d, text, f, maxw)

def draw_rich(d, x, y, lines, f, fill=WHITE, hl=SUN, center=True, spacing=1.12, maxw=W):
    """*mot* = surligné jaune. Retourne y de fin."""
    lh = int(f.size * spacing)
    for ln in lines:
        parts = re.split(r"(\*[^*]+\*)", ln)
        plain = ln.replace("*", "")
        tw = d.textlength(plain, font=f)
        cx = x + (maxw - tw) / 2 if center else x
        for p in parts:
            if not p: continue
            col = hl if p.startswith("*") else fill
            t = p.strip("*")
            d.text((cx, y), t, font=f, fill=col)
            cx += d.textlength(t, font=f)
        y += lh
    return y

def rich_wrap(d, text, f, maxw):
    # garder les marqueurs * sur des mots entiers
    return wrap(d, text, f, maxw)

def fix_stars(lines):
    out, open_ = [], False
    for l in lines:
        n = l.count("*")
        if open_: l = "*" + l
        if (n % 2 == 1): open_ = not open_
        if open_: l = l + "*"
        out.append(l)
    return out

# ---------------------------------------------------------------- icônes (dessinées, aucun droit tiers)
def icon(name, size=360, color=SUN):
    S = 4; s = size * S
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = color + (255,); w = (255, 255, 255, 255); n = (11, 18, 32, 255); lw = int(s * 0.045)
    def rr(b, r, **k): d.rounded_rectangle([int(v) for v in b], radius=int(r), **k)
    if name == "car":
        rr((s*.06, s*.45, s*.94, s*.72), s*.08, fill=c)
        d.polygon([(s*.24, s*.46), (s*.34, s*.25), (s*.66, s*.25), (s*.78, s*.46)], fill=c)
        d.polygon([(s*.31, s*.45), (s*.38, s*.31), (s*.49, s*.31), (s*.49, s*.45)], fill=n)
        d.polygon([(s*.53, s*.45), (s*.53, s*.31), (s*.63, s*.31), (s*.72, s*.45)], fill=n)
        for cx in (s*.27, s*.73):
            d.ellipse([cx-s*.11, s*.62, cx+s*.11, s*.84], fill=n); d.ellipse([cx-s*.06, s*.67, cx+s*.06, s*.79], fill=w)
        rr((s*.08, s*.52, s*.16, s*.58), s*.02, fill=w); rr((s*.84, s*.52, s*.92, s*.58), s*.02, fill=(255, 90, 90, 255))
    elif name == "doc":   # certificat d'immatriculation stylisé
        rr((s*.12, s*.2, s*.88, s*.8), s*.05, fill=w)
        rr((s*.12, s*.2, s*.88, s*.32), s*.05, fill=(11, 58, 143, 255)); d.rectangle([s*.12, s*.27, s*.88, s*.32], fill=(11, 58, 143, 255))
        d.rectangle([s*.16, s*.23, s*.2, s*.29], fill=(0, 85, 164, 255)); d.rectangle([s*.2, s*.23, s*.24, s*.29], fill=w); d.rectangle([s*.24, s*.23, s*.28, s*.29], fill=(239, 65, 53, 255))
        for i, ww in enumerate((.55, .42, .6, .35, .5)):
            rr((s*.18, s*(.39+i*.08), s*(.18+ww*.9), s*(.43+i*.08)), s*.015, fill=(200, 210, 228, 255))
        d.ellipse([s*.62, s*.58, s*.84, s*.8], fill=c); d.line([(s*.67, s*.69), (s*.72, s*.74), (s*.8, s*.64)], fill=n, width=lw)
    elif name == "plate":
        rr((s*.04, s*.36, s*.96, s*.64), s*.04, fill=w, outline=n, width=lw//2)
        rr((s*.04, s*.36, s*.16, s*.64), s*.04, fill=(0, 51, 153, 255)); d.rectangle([s*.1, s*.36, s*.16, s*.64], fill=(0, 51, 153, 255))
        rr((s*.84, s*.36, s*.96, s*.64), s*.04, fill=(0, 51, 153, 255)); d.rectangle([s*.84, s*.36, s*.9, s*.64], fill=(0, 51, 153, 255))
        f = font(FD, int(s*.15)); d.text((s*.5, s*.5), "AB-123-CD", font=f, fill=n, anchor="mm")
        f2 = font(FB, int(s*.06)); d.text((s*.1, s*.57), "F", font=f2, fill=w, anchor="mm")
    elif name == "calendar":
        rr((s*.14, s*.2, s*.86, s*.84), s*.06, fill=w); rr((s*.14, s*.2, s*.86, s*.38), s*.06, fill=c); d.rectangle([s*.14, s*.3, s*.86, s*.38], fill=c)
        for x in (.3, .7): rr((s*(x-.03), s*.13, s*(x+.03), s*.28), s*.02, fill=n)
        f = font(FD, int(s*.3)); d.text((s*.5, s*.62), "30", font=f, fill=n, anchor="mm")
    elif name == "euro":
        d.ellipse([s*.12, s*.12, s*.88, s*.88], fill=c); d.ellipse([s*.18, s*.18, s*.82, s*.82], outline=n, width=lw//2)
        f = font(FD, int(s*.46)); d.text((s*.5, s*.52), "€", font=f, fill=n, anchor="mm")
    elif name == "clock":
        d.ellipse([s*.12, s*.12, s*.88, s*.88], fill=w); d.ellipse([s*.12, s*.12, s*.88, s*.88], outline=c, width=lw)
        d.line([(s*.5, s*.5), (s*.5, s*.26)], fill=n, width=lw); d.line([(s*.5, s*.5), (s*.68, s*.6)], fill=n, width=lw); d.ellipse([s*.46, s*.46, s*.54, s*.54], fill=c)
    elif name == "check":
        d.ellipse([s*.1, s*.1, s*.9, s*.9], fill=OK + (255,)); d.line([(s*.3, s*.52), (s*.45, s*.66), (s*.72, s*.36)], fill=w, width=int(lw*1.6), joint="curve")
    elif name == "warn":
        d.polygon([(s*.5, s*.1), (s*.92, s*.86), (s*.08, s*.86)], fill=c); f = font(FD, int(s*.5)); d.text((s*.5, s*.6), "!", font=f, fill=n, anchor="mm")
    elif name == "house":
        d.polygon([(s*.5, s*.12), (s*.9, s*.46), (s*.1, s*.46)], fill=c); rr((s*.2, s*.44, s*.8, s*.86), s*.03, fill=w); rr((s*.42, s*.6, s*.58, s*.86), s*.02, fill=n)
    elif name == "key":
        d.ellipse([s*.1, s*.3, s*.46, s*.66], fill=c); d.ellipse([s*.2, s*.4, s*.36, s*.56], fill=(0, 0, 0, 0)); rr((s*.42, s*.44, s*.9, s*.52), s*.02, fill=c)
        rr((s*.72, s*.5, s*.78, s*.64), s*.01, fill=c); rr((s*.82, s*.5, s*.88, s*.6), s*.01, fill=c)
    elif name == "phone":
        rr((s*.3, s*.08, s*.7, s*.92), s*.07, fill=w); rr((s*.34, s*.15, s*.66, s*.8), s*.03, fill=(11, 58, 143, 255)); d.ellipse([s*.46, s*.83, s*.54, s*.89], fill=n)
        for i in range(3): rr((s*.38, s*(.22+i*.12), s*.62, s*(.3+i*.12)), s*.02, fill=c if i == 2 else (120, 160, 230, 255))
    elif name == "shield":
        d.polygon([(s*.5, s*.08), (s*.86, s*.22), (s*.8, s*.62), (s*.5, s*.92), (s*.2, s*.62), (s*.14, s*.22)], fill=c)
        d.line([(s*.33, s*.5), (s*.46, s*.63), (s*.68, s*.38)], fill=n, width=int(lw*1.4), joint="curve")
    elif name == "swap":   # cession : échange de clés / propriétaire
        d.ellipse([s*.08, s*.08, s*.92, s*.92], fill=w)
        d.line([(s*.25, s*.38), (s*.72, s*.38)], fill=EU + (255,), width=lw); d.polygon([(s*.78, s*.38), (s*.66, s*.3), (s*.66, s*.46)], fill=EU + (255,))
        d.line([(s*.75, s*.62), (s*.28, s*.62)], fill=c, width=lw); d.polygon([(s*.22, s*.62), (s*.34, s*.54), (s*.34, s*.7)], fill=c)
    elif name == "cards":  # 4 échéances
        for i in range(4):
            x = s*(.08+i*.215); rr((x, s*.3, x+s*.19, s*.7), s*.03, fill=c if i == 0 else w)
            f = font(FD, int(s*.12)); d.text((x+s*.095, s*.5), str(i+1), font=f, fill=n, anchor="mm")
    elif name == "map":
        d.ellipse([s*.1, s*.62, s*.9, s*.9], fill=(255, 255, 255, 60))
        d.ellipse([s*.24, s*.06, s*.76, s*.58], fill=c); d.polygon([(s*.28, s*.42), (s*.72, s*.42), (s*.5, s*.8)], fill=c)
        d.ellipse([s*.38, s*.2, s*.62, s*.44], fill=n)
    elif name == "question":
        d.ellipse([s*.1, s*.1, s*.9, s*.9], fill=c); f = font(FD, int(s*.55)); d.text((s*.5, s*.53), "?", font=f, fill=n, anchor="mm")
    elif name == "cross":
        d.ellipse([s*.1, s*.1, s*.9, s*.9], fill=BAD + (255,)); d.line([(s*.33, s*.33), (s*.67, s*.67)], fill=w, width=int(lw*1.5)); d.line([(s*.67, s*.33), (s*.33, s*.67)], fill=w, width=int(lw*1.5))
    elif name == "moto":
        for cx in (s*.24, s*.76):
            d.ellipse([cx-s*.15, s*.5, cx+s*.15, s*.8], outline=c, width=lw)
        d.polygon([(s*.24, s*.65), (s*.45, s*.4), (s*.66, s*.4), (s*.76, s*.65)], outline=w, width=lw)
        rr((s*.4, s*.32, s*.66, s*.44), s*.04, fill=c); d.line([(s*.66, s*.4), (s*.72, s*.26)], fill=w, width=lw)
    else:
        d.ellipse([s*.1, s*.1, s*.9, s*.9], fill=c)
    return im.resize((size, size), Image.LANCZOS)

# ---------------------------------------------------------------- fond animé
def make_bg(theme, seed):
    c1, c2 = THEMES.get(theme, THEMES["acquisition"])
    y = np.linspace(0, 1, H)[:, None]; x = np.linspace(0, 1, W)[None, :]
    t = np.clip(0.65 * y + 0.35 * x, 0, 1)[..., None]
    arr = (np.array(c1) * (1 - t) + np.array(c2) * t).astype(np.uint8)
    base = Image.fromarray(np.broadcast_to(arr, (H, W, 3)).copy(), "RGB").convert("RGBA")
    # trame de route subtile
    d = ImageDraw.Draw(base)
    rng = np.random.default_rng(seed)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); do = ImageDraw.Draw(ov)
    for i in range(9):   # marquage routier discret en perspective
        yy = 1500 + i * 60; ww = 6 + i * 3
        do.rectangle([W // 2 - ww, yy, W // 2 + ww, yy + 30], fill=(255, 255, 255, 10 + i * 2))
    base.alpha_composite(ov)
    return base

def blobs_layer(seed):
    rng = np.random.default_rng(seed)
    im = Image.new("RGBA", (W // 4, H // 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cols = [(255, 197, 49, 60), (21, 80, 196, 90), (122, 162, 255, 50)]
    for i in range(3):
        r = rng.integers(70, 130); cx = rng.integers(0, W // 4); cy = rng.integers(0, H // 4)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cols[i])
    return im.filter(ImageFilter.GaussianBlur(40)).resize((W + 160, H + 200), Image.BILINEAR)

_logo = None
def logo_pill(h=64):
    global _logo
    if _logo is None:
        lg = Image.open(A("logo.png")).convert("RGBA")
        lw = int(lg.width * h / lg.height); lg = lg.resize((lw, h), Image.LANCZOS)
        pill = Image.new("RGBA", (lw + 44, h + 28), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle([0, 0, pill.width - 1, pill.height - 1], radius=(h + 28) // 2, fill=(255, 255, 255, 245))
        pill.alpha_composite(lg, (22, 14)); _logo = pill
    return _logo

# ---------------------------------------------------------------- scènes
SAFE_X, SAFE_W = 90, W - 180   # zone sûre (boutons TikTok/Reels à droite, légende en bas)

def card(d, b, fill=(255, 255, 255, 22), outline=(255, 255, 255, 40), r=36):
    d.rounded_rectangle(b, radius=r, fill=fill, outline=outline, width=2)

def scene_layer(sc, idx, total, meta):
    """Couche RGBA statique d'une scène (sans animation)."""
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    t = sc["type"]
    top = 300
    if t == "hook":
        if sc.get("kicker"):
            f = font(FB, 44); tw = d.textlength(sc["kicker"].upper(), font=f)
            d.rounded_rectangle([(W - tw) / 2 - 28, top, (W + tw) / 2 + 28, top + 78], radius=39, fill=SUN + (255,))
            d.text((W / 2, top + 39), sc["kicker"].upper(), font=f, fill=NAVY, anchor="mm"); top += 120
        f, ls = fit(d, sc["big"], FD, SAFE_W, 560, 132); ls = fix_stars(ls)
        y = draw_rich(d, SAFE_X, top, ls, f, maxw=SAFE_W)
        if sc.get("icon"): L.alpha_composite(icon(sc["icon"], 340), ((W - 340) // 2, int(y + 40)))
    elif t == "stat":
        f = font(FD, 200 if len(sc["value"]) <= 6 else 150)
        d.text((W / 2, top + 200), sc["value"], font=f, fill=SUN, anchor="mm")
        f2, ls = fit(d, sc["label"], FB, SAFE_W, 300, 64); ls = fix_stars(ls)
        y = draw_rich(d, SAFE_X, top + 360, ls, f2, maxw=SAFE_W)
        if sc.get("icon"): L.alpha_composite(icon(sc["icon"], 280), ((W - 280) // 2, int(y + 40)))
    elif t == "point":
        if sc.get("n"):
            d.ellipse([W / 2 - 70, top, W / 2 + 70, top + 140], fill=SUN + (255,))
            d.text((W / 2, top + 72), str(sc["n"]), font=font(FD, 92), fill=NAVY, anchor="mm"); top += 180
        f, ls = fit(d, sc["title"], FD, SAFE_W, 330, 92); ls = fix_stars(ls)
        y = draw_rich(d, SAFE_X, top, ls, f, maxw=SAFE_W) + 24
        if sc.get("text"):
            f2, ls2 = fit(d, sc["text"], FR, SAFE_W - 80, 300, 54, spacing=1.25); ls2 = fix_stars(ls2)
            hh = len(ls2) * int(f2.size * 1.25) + 60
            card(d, [SAFE_X, y, W - SAFE_X, y + hh])
            y = draw_rich(d, SAFE_X + 40, y + 30, ls2, f2, fill=(232, 237, 247), maxw=SAFE_W - 80, spacing=1.25) + 50
        if sc.get("icon"): L.alpha_composite(icon(sc["icon"], 300), ((W - 300) // 2, int(min(y + 30, 960))))
    elif t == "list":
        f, ls = fit(d, sc["title"], FD, SAFE_W, 260, 84); ls = fix_stars(ls)
        y = draw_rich(d, SAFE_X, top, ls, f, maxw=SAFE_W) + 30
        items = sc["items"]; fi = font(FB, 56 if len(items) <= 4 else 48)
        for it in items:
            ok = not it.startswith("✗"); txt = it.lstrip("✓✗ ").strip()
            lines = wrap(d, txt, fi, SAFE_W - 170); hh = max(130, len(lines) * int(fi.size * 1.2) + 56)
            card(d, [SAFE_X, y, W - SAFE_X, y + hh], r=28)
            L.alpha_composite(icon("check" if ok else "cross", 74), (SAFE_X + 28, int(y + (hh - 74) / 2)))
            yy = y + (hh - len(lines) * int(fi.size * 1.2)) / 2
            for ln in lines: d.text((SAFE_X + 128, yy), ln, font=fi, fill=WHITE); yy += int(fi.size * 1.2)
            y += hh + 22
    elif t == "versus":
        f, ls = fit(d, sc.get("title") or "", FD, SAFE_W, 220, 80); ls = fix_stars(ls)
        y = draw_rich(d, SAFE_X, top, ls, f, maxw=SAFE_W) + 30 if sc.get("title") else top
        for lab, txt, col, ic in ((sc["left"][0], sc["left"][1], BAD, "cross"), (sc["right"][0], sc["right"][1], OK, "check")):
            f2, ls2 = fit(d, txt, FB, SAFE_W - 80, 260, 54, spacing=1.2)
            hh = len(ls2) * int(f2.size * 1.2) + 130
            card(d, [SAFE_X, y, W - SAFE_X, y + hh], outline=col + (160,))
            L.alpha_composite(icon(ic, 60), (SAFE_X + 36, int(y + 26)))
            d.text((SAFE_X + 112, y + 56), lab.upper(), font=font(FB, 42), fill=col, anchor="lm")
            draw_rich(d, SAFE_X + 40, y + 104, ls2, f2, center=False, maxw=SAFE_W - 80, spacing=1.2)
            y += hh + 28
    elif t == "steps":
        f, ls = fit(d, sc["title"], FD, SAFE_W, 220, 84); ls = fix_stars(ls)
        y = draw_rich(d, SAFE_X, top, ls, f, maxw=SAFE_W) + 30
        fi = font(FB, 48)
        for i, it in enumerate(sc["items"]):
            lines = wrap(d, it, fi, SAFE_W - 170); hh = max(110, len(lines) * 58 + 46)
            card(d, [SAFE_X, y, W - SAFE_X, y + hh], r=28)
            d.ellipse([SAFE_X + 26, y + hh / 2 - 38, SAFE_X + 102, y + hh / 2 + 38], fill=SUN + (255,))
            d.text((SAFE_X + 64, y + hh / 2), str(i + 1), font=font(FD, 50), fill=NAVY, anchor="mm")
            yy = y + (hh - len(lines) * 58) / 2
            for ln in lines: d.text((SAFE_X + 128, yy), ln, font=fi, fill=WHITE); yy += 58
            y += hh + 20
    elif t == "cta":
        lg = Image.open(A("logo.png")).convert("RGBA"); lw = 760; lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
        cardi = Image.new("RGBA", (lw + 80, lg.height + 80), (0, 0, 0, 0)); ImageDraw.Draw(cardi).rounded_rectangle([0, 0, cardi.width - 1, cardi.height - 1], radius=40, fill=WHITE + (255,))
        cardi.alpha_composite(lg, (40, 40)); L.alpha_composite(cardi, ((W - cardi.width) // 2, 330))
        f, ls = fit(d, sc.get("big", "Calculez le prix de votre carte grise"), FD, SAFE_W, 280, 88); ls = fix_stars(ls)
        y = draw_rich(d, SAFE_X, 620, ls, f, maxw=SAFE_W) + 40
        fb = font(FD, 70); url = "cartegrise4x.fr"; tw = d.textlength(url, font=fb)
        d.rounded_rectangle([(W - tw) / 2 - 60, y, (W + tw) / 2 + 60, y + 140], radius=70, fill=SUN + (255,))
        d.text((W / 2, y + 70), url, font=fb, fill=NAVY, anchor="mm"); y += 190
        if sc.get("sub"):
            fs = font(FB, 46)
            for ln in wrap(d, sc["sub"], fs, SAFE_W): d.text((W / 2, y), ln, font=fs, fill=WHITE, anchor="mt"); y += 58
            y += 22
        mentions = ["Service privé, non affilié à l'ANTS."]
        if meta.get("credit"):
            mentions.append("Paiement en 4 fois avec PayPal ou Klarna, selon éligibilité et sous réserve d'acceptation.")
            mentions.append("Un crédit vous engage et doit être remboursé. Vérifiez vos capacités de remboursement avant de vous engager.")
        fm = font(FR, 34); yy = max(y + 20, 1180)
        for m in mentions:
            for ln in wrap(d, m, fm, SAFE_W): d.text((W / 2, yy), ln, font=fm, fill=(214, 222, 236), anchor="mt"); yy += 44
            yy += 8
    return L

# ---------------------------------------------------------------- voix
SAY = [(r"cartegrise4x\.fr", "carte grise quatre x point f r"), (r"CarteGrise4x", "carte grise quatre x"), (r"\b4x\b", "quatre fois"),
       (r"(\d+),(\d+) ?€", r"\1 euros \2"), (r"(\d+) ?€", r"\1 euros"), (r"\bCV\b", "chevaux"), (r"\bANTS\b", "A N T S"), (r"\bSIV\b", "S I V"),
       (r"\bWW\b", "W garage"), (r"\bZFE\b", "Z F E"), (r"\bCT\b", "contrôle technique"), (r"cerfa", "serfa"), (r"\bVO\b", "voiture d'occasion"),
       (r"Crit'Air", "crit air"), (r"\bkm\b", "kilomètres"), (r"\bn°", "numéro "), (r"%", " pour cent"), (r"\bTTC\b", "T T C")]
def speakable(t):
    t = t.replace("*", "")
    for a, b in SAY: t = re.sub(a, b, t)
    return t

def synth_all(jobs, cache):
    """jobs: list of (text, path). Un seul processus Piper pour tout le lot."""
    todo = [(t, p) for t, p in jobs if not os.path.exists(p)]
    if not todo: return
    env = dict(os.environ, LD_LIBRARY_PATH=os.path.dirname(PIPER))
    inp = "\n".join(json.dumps({"text": speakable(t), "output_file": p}, ensure_ascii=False) for t, p in todo) + "\n"
    subprocess.run([PIPER, "-m", VOICE, "--json-input", "--length_scale", "0.9", "--sentence_silence", "0.12"],
                   input=inp.encode(), env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def wav_read(p):
    with wave.open(p) as w:
        sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return a, sr

# ---------------------------------------------------------------- musique générée (libre de droits par construction)
def music(dur, seed, sr=44100):
    rng = np.random.default_rng(seed); bpm = [92, 100, 108, 116][seed % 4]; beat = 60 / bpm
    n = int(dur * sr); t = np.arange(n) / sr; out = np.zeros(n, np.float32)
    keys = [[0, 3, 7, 10], [5, 8, 12, 15], [3, 7, 10, 14], [-2, 2, 5, 9]]
    root = 220 * 2 ** (rng.integers(-3, 3) / 12)
    bar = 4 * beat
    for bi in range(int(dur / bar) + 1):
        ch = keys[bi % 4]; s0 = int(bi * bar * sr); s1 = min(n, int((bi + 1) * bar * sr))
        if s0 >= n: break
        tt = t[s0:s1] - bi * bar; env = np.minimum(1, tt * 4) * np.exp(-tt * 0.35)
        for k in ch: out[s0:s1] += 0.05 * env * np.sin(2 * np.pi * root * 2 ** (k / 12) * tt) * (1 + 0.3 * np.sin(2 * np.pi * 0.5 * tt))
        out[s0:s1] += 0.07 * env * np.sin(2 * np.pi * root / 2 * 2 ** (ch[0] / 12) * tt)
    for k in range(int(dur / beat) + 1):
        s0 = int(k * beat * sr)
        if s0 >= n: break
        L_ = min(int(0.25 * sr), n - s0); tt = np.arange(L_) / sr
        out[s0:s0 + L_] += 0.32 * np.sin(2 * np.pi * (50 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14)   # kick
        h0 = int((k + 0.5) * beat * sr)
        if h0 < n:
            L2 = min(int(0.05 * sr), n - h0); out[h0:h0 + L2] += 0.04 * rng.standard_normal(L2) * np.exp(-np.arange(L2) / sr * 90)
    fade = np.minimum(1, np.minimum(t / 0.5, (dur - t) / 1.2)); return (out * fade).astype(np.float32)

# ---------------------------------------------------------------- rendu
def ease(x): return 1 - (1 - min(max(x, 0), 1)) ** 3

def caption_chunks(text, start, dur):
    words = speakable(text).split() if False else text.replace("*", "").split()
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 4 or w[-1] in ".?!,:": chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    total = sum(len(" ".join(c)) for c in chunks) or 1; t = start; res = []
    for c in chunks:
        dd = dur * len(" ".join(c)) / total; res.append((t, t + dd, c)); t += dd
    return res

_capc = {}
def caption_img(words, k):
    key = (tuple(words), k)
    if key in _capc: return _capc[key]
    f = font(FD, 66); im = Image.new("RGBA", (W, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    txt = " ".join(words); lines = wrap(d, txt, f, SAFE_W - 40)
    y = 110 - len(lines) * 40; wi = 0
    for ln in lines:
        ws = ln.split(); tw = d.textlength(ln, font=f); x = (W - tw) / 2
        for w_ in ws:
            col = SUN if wi == k else WHITE
            d.text((x, y), w_, font=f, fill=col, stroke_width=7, stroke_fill=(0, 0, 0)); x += d.textlength(w_ + " ", font=f); wi += 1
        y += 80
    _capc[key] = im; return im

def render(concept, outdir, tmp):
    cid = concept["id"]; out = os.path.join(outdir, cid + ".mp4")
    scenes = concept["scenes"]; seed = int(hashlib.md5(cid.encode()).hexdigest()[:6], 16)
    # durées depuis la voix
    timeline = []; t = 0.0; voice = []
    for i, sc in enumerate(scenes):
        p = os.path.join(tmp, f"{cid}_{i}.wav"); a, sr = wav_read(p)
        pad = 0.45 if sc["type"] != "cta" else 1.6
        dur = max(len(a) / sr + pad, sc.get("min", 1.8 if sc["type"] != "cta" else 4.5))
        timeline.append((t, dur, sc)); voice.append((t + 0.15, a, sr)); t += dur
    total = t; nfr = int(math.ceil(total * FPS))
    # audio
    sr = 44100; mix = np.zeros(int(total * sr) + sr, np.float32)
    for st, a, vsr in voice:
        if vsr != sr: a = np.interp(np.arange(0, len(a), vsr / sr), np.arange(len(a)), a)
        s0 = int(st * sr); mix[s0:s0 + len(a)] += 1.0 * a
    m = music(len(mix) / sr + 0.1, seed); m = np.pad(m, (0, max(0, len(mix) - len(m))))[:len(mix)]; vo = np.convolve(np.abs(mix), np.ones(4410) / 4410, "same")
    duck = 1 - 0.55 * np.clip(vo * 12, 0, 1); mix = mix + 0.55 * m[:len(mix)] * duck
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.89
    apath = os.path.join(tmp, cid + "_mix.wav")
    with wave.open(apath, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    # visuels
    bg = make_bg(concept.get("category", "acquisition"), seed); bl = blobs_layer(seed); pill = logo_pill()
    layers = [scene_layer(sc, i, len(scenes), concept) for i, (_, _, sc) in enumerate(timeline)]
    caps = []
    for (st, dur, sc) in timeline:
        if sc["type"] != "cta" and sc.get("voice"): caps += caption_chunks(sc["voice"], st + 0.15, dur - 0.45)
    cover = None
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", apath, "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2", "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    for fi in range(nfr):
        tt = fi / FPS
        si = max(i for i, (st, _, _) in enumerate(timeline) if st <= tt + 1e-6); st, dur, sc = timeline[si]; lt = tt - st
        fr = bg.copy()
        ox = int(70 * math.sin(tt * 0.35 + seed)); oy = int(90 * math.cos(tt * 0.27 + seed))
        fr.alpha_composite(bl.crop((80 + ox, 100 + oy, 80 + ox + W, 100 + oy + H)))
        lay = layers[si]
        k = ease(lt / 0.32) if not (si == 0 and fi < 2) else 1.0
        if si == 0: k = max(k, 0.85)                          # accroche lisible dès la 1re image
        if k < 1:
            sc_ = 0.92 + 0.08 * k; nw, nh = int(W * sc_), int(H * sc_)
            l2 = lay.resize((nw, nh), Image.BILINEAR)
            if k < 0.999:
                alpha = l2.getchannel("A").point(lambda v: int(v * k)); l2.putalpha(alpha)
            fr.alpha_composite(l2, ((W - nw) // 2, (H - nh) // 2 + int(40 * (1 - k))))
        else:
            fr.alpha_composite(lay, (0, int(4 * math.sin(tt * 2.2))) if sc["type"] != "cta" else (0, 0))
        if sc["type"] != "cta": fr.alpha_composite(pill, (SAFE_X, 120))
        for (c0, c1, words) in caps:
            if c0 <= tt < c1:
                kk = min(len(words) - 1, int((tt - c0) / max(1e-3, (c1 - c0)) * len(words)))
                fr.alpha_composite(caption_img(words, kk), (0, 1300)); break
        d = ImageDraw.Draw(fr); d.rectangle([0, 0, int(W * tt / total), 10], fill=SUN + (255,))
        rgb = fr.convert("RGB")
        if fi == int(min(total - 0.1, 1.2) * FPS): cover = rgb.copy()
        ff.stdin.write(rgb.tobytes())
    ff.stdin.close(); ff.wait()
    if ff.returncode != 0: raise RuntimeError("ffmpeg " + cid)
    # couverture : accroche lisible, pour Reels/TikTok/Shorts
    cv = Image.new("RGB", (W, H)); cv.paste(bg.convert("RGB")); cl = bg.copy(); cl.alpha_composite(bl.crop((80, 100, 80 + W, 100 + H))); cl.alpha_composite(layers[0]); cl.alpha_composite(pill, (SAFE_X, 120))
    cl.convert("RGB").save(os.path.join(outdir, cid + "_cover.jpg"), quality=90)
    return out, total

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("concepts"); ap.add_argument("--only"); ap.add_argument("--force", action="store_true"); ap.add_argument("--out", default=os.path.join(ROOT, "out"))
    ap.add_argument("--shard", default="0/1")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); tmp = os.path.join(ROOT, "tmp"); os.makedirs(tmp, exist_ok=True)
    cs = json.load(open(a.concepts, encoding="utf-8"))
    if a.only: cs = [c for c in cs if c["id"] in a.only.split(",")]
    k, n = map(int, a.shard.split("/")); cs = [c for i, c in enumerate(cs) if i % n == k]
    if not a.force: cs = [c for c in cs if not os.path.exists(os.path.join(a.out, c["id"] + ".mp4"))]
    if a.force:
        for c in cs:
            for i in range(len(c["scenes"])):
                p = os.path.join(tmp, f"{c['id']}_{i}.wav")
                if os.path.exists(p): os.remove(p)
    jobs = []
    for c in cs:
        for i, sc in enumerate(c["scenes"]):
            v = sc.get("voice") or ("Calculez le prix de votre carte grise sur cartegrise4x.fr." if sc["type"] == "cta" else "")
            sc["voice"] = v; jobs.append((v, os.path.join(tmp, f"{c['id']}_{i}.wav")))
    synth_all(jobs, tmp)
    log = open(os.path.join(ROOT, "render.log"), "a")
    for c in cs:
        try:
            p, d = render(c, a.out, tmp); print(f"OK {c['id']} {d:.1f}s", flush=True); log.write(f"OK {c['id']} {d:.1f}s\n")
        except Exception as e:
            print(f"ERREUR {c['id']} {e}", flush=True); log.write(f"ERREUR {c['id']} {e}\n")

if __name__ == "__main__":
    main()
