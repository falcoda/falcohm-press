# -*- coding: utf-8 -*-
"""Primitives graphiques — dossier de partenariat Falc'ohm System ASBL"""
import os
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
FONTS = os.path.join(ASSETS, "fonts")

_INDEX = None


def asset(name):
    """Résout un asset par nom de fichier, où qu'il soit dans assets/.

    Permet d'écrire `cover.jpg` dans le YAML sans se soucier du sous-dossier.
    """
    global _INDEX
    if os.path.sep in name or "/" in name:
        p = os.path.join(ASSETS, name)
        if os.path.exists(p):
            return p
    if _INDEX is None:
        _INDEX = {}
        for root, _, files in os.walk(ASSETS):
            for f in files:
                _INDEX.setdefault(f, os.path.join(root, f))
    if name not in _INDEX:
        raise FileNotFoundError("asset introuvable : %s (cherché dans %s)" % (name, ASSETS))
    return _INDEX[name]

for name, f in [("Inter", "Inter-Regular.ttf"), ("Inter-L", "Inter-Light.ttf"),
                ("Inter-M", "Inter-Medium.ttf"), ("Inter-SB", "Inter-SemiBold.ttf"),
                ("Inter-B", "Inter-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONTS, f)))

W, H = 595.276, 841.890
M = 52
CW = W - 2 * M

BLACK = HexColor("#0E0F12")
INK = HexColor("#191B20")
BODY = HexColor("#4B5058")
# #8A9099 tombait à 3.2:1 sur blanc et 2.9:1 sur les cartes — sous le seuil WCAG AA (4.5:1).
# Les légendes et les libellés étaient à la limite du lisible, et illisibles une fois imprimés
# en noir et blanc. #646B75 tient 5.4:1 sur blanc et 4.9:1 sur LIGHT, sans alourdir le gris.
GREY = HexColor("#646B75")
LIGHT = HexColor("#F3F4F6")
LINE = HexColor("#E3E5E9")
BLUE = HexColor("#1F5FEB")
WHITE = HexColor("#FFFFFF")


# ───────────────────────── optimisation des images ─────────────────────────
# Les sources font jusqu'à 4000 px : inutile pour un A4 envoyé par e-mail. On les
# ré-échantillonne à la résolution réellement utile et on met le résultat en cache.
# PRESS_DPI=300 pour une sortie destinée à l'impression.
DPI = int(os.environ.get("PRESS_DPI", "150"))
JPEG_QUALITY = int(os.environ.get("PRESS_JPEG_QUALITY", "80"))
CACHE = os.path.join(ROOT, ".cache")


def optimized(path, w_pt, h_pt):
    """Version de l'image dimensionnee pour une boite de w_pt x h_pt."""
    from PIL import Image
    im = Image.open(path)
    iw, ih = im.size
    max_w = int(w_pt / 72.0 * DPI)
    max_h = int(h_pt / 72.0 * DPI)
    scale = max(max_w / float(iw), max_h / float(ih))
    if scale >= 1.0:
        return path
    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
    has_alpha = im.mode in ("RGBA", "LA", "P")
    ext = ".png" if has_alpha else ".jpg"
    key = "%s_%dx%d_q%d%s" % (os.path.splitext(os.path.basename(path))[0], nw, nh,
                              JPEG_QUALITY, ext)
    out = os.path.join(CACHE, key)
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(path):
        return out
    os.makedirs(CACHE, exist_ok=True)
    im = im.resize((nw, nh), Image.LANCZOS)
    if has_alpha:
        im.save(out, "PNG", optimize=True)
    else:
        im.convert("RGB").save(out, "JPEG", quality=JPEG_QUALITY, optimize=True,
                               progressive=True)
    return out


def tw(c, txt, font, size, space=0.0):
    return c.stringWidth(txt, font, size) + space * max(len(txt) - 1, 0)


def ls_text(c, x, y, txt, font, size, color, space=0.0, align="l"):
    w = tw(c, txt, font, size, space)
    if align == "c":
        x -= w / 2
    elif align == "r":
        x -= w
    t = c.beginText()
    t.setTextOrigin(x, y)
    t.setFont(font, size)
    t.setFillColor(color)
    t.setCharSpace(space)
    t.textOut(txt)
    c.drawText(t)


def ellipsize(c, txt, font, size, width, space=0):
    """Tronque avec « … » pour tenir dans `width`. Un nom d'organisme public tient sur
    trois lignes de raison sociale ; un bandeau n'en a qu'une."""
    if tw(c, txt, font, size, space) <= width:
        return txt
    ell = "…"
    while txt and tw(c, txt + ell, font, size, space) > width:
        txt = txt[:-1].rstrip()
    return (txt + ell) if txt else ell


def wrap(c, txt, font, size, width):
    lines, cur = [], ""
    for word in txt.split():
        t = (cur + " " + word).strip()
        if c.stringWidth(t, font, size) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(c, x, y, txt, font="Inter-L", size=9.6, lead=15.4, width=CW, color=BODY):
    for block in txt.split("\n"):
        if not block.strip():
            y -= lead * 0.6
            continue
        for ln in wrap(c, block, font, size, width):
            ls_text(c, x, y, ln, font, size, color)
            y -= lead
    return y


def rrect(c, x, y, w, h, r=6, fill=None, stroke=None, lw=0.7):
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, stroke=1 if stroke is not None else 0,
                fill=1 if fill is not None else 0)


def img_cover(c, path, x, y, w, h):
    from PIL import Image
    path = optimized(path, w, h)
    iw, ih = Image.open(path).size
    ar_box, ar_img = w / h, iw / ih
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    if ar_img > ar_box:
        dh, dw = h, h * ar_img
        c.drawImage(path, x - (dw - w) / 2, y, dw, dh, mask='auto')
    else:
        dw, dh = w, w / ar_img
        c.drawImage(path, x, y - (dh - h) / 2, dw, dh, mask='auto')
    c.restoreState()


def veil(c, x, y, w, h, color=BLACK, top=0.0, bottom=0.85, steps=90):
    c.saveState()
    seg = h / steps
    for i in range(steps):
        t = i / (steps - 1)
        a = bottom + (top - bottom) * t
        if a <= 0.003:
            continue
        c.setFillColor(Color(color.red, color.green, color.blue, alpha=a))
        c.rect(x, y + h * t, w, seg + 0.6, stroke=0, fill=1)
    c.restoreState()


def kicker(c, x, y, num, label, color=BLUE):
    ls_text(c, x, y, num, "Inter-B", 8.4, color, 1.5)
    wnum = tw(c, num, "Inter-B", 8.4, 1.5)
    c.setStrokeColor(color)
    c.setLineWidth(0.9)
    c.line(x + wnum + 7, y + 2.6, x + wnum + 21, y + 2.6)
    ls_text(c, x + wnum + 28, y, label.upper(), "Inter-M", 8.4, GREY, 1.5)


def title(c, x, y, txt, size=28, color=INK, width=CW, lead=None):
    lead = lead or size * 1.16
    for block in txt.split("\n"):
        for ln in wrap(c, block, "Inter-B", size, width):
            ls_text(c, x, y, ln, "Inter-B", size, color, -0.4)
            y -= lead
    return y + lead


def eyebrow(c, x, y, txt, color=INK):
    ls_text(c, x, y, txt.upper(), "Inter-B", 8.6, color, 1.4)


def footer(c, page, dark=False):
    # L'interlettrage était à 1.2 : un copier-coller rendait « F A L C ' O H M   S Y S T E M »
    # et collait les deux blocs. Le pied de page porte le nom légal de l'ASBL et le titre du
    # document — c'est de l'information, pas de la décoration : elle doit rester extractible.
    # 0.4 garde l'air du dessin sans faire éclater le mot à l'extraction.
    col = GREY if not dark else HexColor("#8B929C")
    c.setStrokeColor(LINE if not dark else HexColor("#23262C"))
    c.setLineWidth(0.6)
    c.line(M, 56, W - M, 56)
    ls_text(c, M, 42, "FALC'OHM SYSTEM ASBL", "Inter-M", 7, col, 0.4)
    ls_text(c, W / 2, 42, "DOSSIER DE PARTENARIAT", "Inter-L", 7, col, 0.4, align="c")
    ls_text(c, W - M, 42, "%02d" % page, "Inter-B", 7, BLUE, 0.4, align="r")


# ───────────────────────── icônes ─────────────────────────
def icon(c, name, x, y, s=15, color=BLUE, lw=1.15):
    import math
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(lw)
    c.setLineCap(1)
    c.setLineJoin(1)
    u = s / 20.0
    X = lambda v: x + v * u
    Y = lambda v: y + v * u

    if name == "pin":
        p = c.beginPath()
        p.moveTo(X(10), Y(1.5))
        p.curveTo(X(3.5), Y(9), X(3), Y(11), X(3), Y(13))
        p.curveTo(X(3), Y(17), X(6.2), Y(19), X(10), Y(19))
        p.curveTo(X(13.8), Y(19), X(17), Y(17), X(17), Y(13))
        p.curveTo(X(17), Y(11), X(16.5), Y(9), X(10), Y(1.5))
        c.drawPath(p, stroke=1, fill=0)
        c.circle(X(10), Y(13.2), 2.5 * u, stroke=1, fill=0)
    elif name == "calendar":
        c.roundRect(X(2.5), Y(2.5), 15 * u, 14 * u, 1.6 * u, stroke=1, fill=0)
        c.line(X(2.5), Y(12.6), X(17.5), Y(12.6))
        c.line(X(6.5), Y(19), X(6.5), Y(15.2))
        c.line(X(13.5), Y(19), X(13.5), Y(15.2))
        c.circle(X(7), Y(8.4), 0.9 * u, stroke=0, fill=1)
        c.circle(X(11), Y(8.4), 0.9 * u, stroke=0, fill=1)
    elif name == "target":
        c.circle(X(10), Y(10), 8 * u, stroke=1, fill=0)
        c.circle(X(10), Y(10), 4.4 * u, stroke=1, fill=0)
        c.circle(X(10), Y(10), 1.1 * u, stroke=0, fill=1)
    elif name == "heart":
        p = c.beginPath()
        p.moveTo(X(10), Y(3.5))
        p.curveTo(X(2), Y(10), X(2.5), Y(16.5), X(6.5), Y(17.2))
        p.curveTo(X(8.6), Y(17.6), X(10), Y(15.6), X(10), Y(14.4))
        p.curveTo(X(10), Y(15.6), X(11.4), Y(17.6), X(13.5), Y(17.2))
        p.curveTo(X(17.5), Y(16.5), X(18), Y(10), X(10), Y(3.5))
        c.drawPath(p, stroke=1, fill=0)
    elif name == "check":
        c.circle(X(10), Y(10), 8.2 * u, stroke=1, fill=0)
        p = c.beginPath()
        p.moveTo(X(6), Y(10.3))
        p.lineTo(X(9), Y(7.2))
        p.lineTo(X(14.2), Y(13.4))
        c.drawPath(p, stroke=1, fill=0)
    elif name == "globe":
        c.circle(X(10), Y(10), 8.2 * u, stroke=1, fill=0)
        c.line(X(1.8), Y(10), X(18.2), Y(10))
        p = c.beginPath()
        p.moveTo(X(10), Y(1.8))
        p.curveTo(X(5.4), Y(6), X(5.4), Y(14), X(10), Y(18.2))
        p.curveTo(X(14.6), Y(14), X(14.6), Y(6), X(10), Y(1.8))
        c.drawPath(p, stroke=1, fill=0)
    elif name == "megaphone":
        p = c.beginPath()
        p.moveTo(X(4), Y(8))
        p.lineTo(X(4), Y(13))
        p.lineTo(X(9), Y(13))
        p.lineTo(X(16), Y(17.5))
        p.lineTo(X(16), Y(3.5))
        p.lineTo(X(9), Y(8))
        p.close()
        c.drawPath(p, stroke=1, fill=0)
        c.line(X(6.5), Y(8), X(7.5), Y(3.5))
    elif name == "social":
        c.circle(X(5), Y(10), 2.6 * u, stroke=1, fill=0)
        c.circle(X(15), Y(15.5), 2.6 * u, stroke=1, fill=0)
        c.circle(X(15), Y(4.5), 2.6 * u, stroke=1, fill=0)
        c.line(X(7.3), Y(11.3), X(12.8), Y(14.3))
        c.line(X(7.3), Y(8.7), X(12.8), Y(5.7))
    elif name == "video":
        c.roundRect(X(2.5), Y(5.5), 10 * u, 9 * u, 1.6 * u, stroke=1, fill=0)
        p = c.beginPath()
        p.moveTo(X(13.6), Y(11.5))
        p.lineTo(X(17.6), Y(14.5))
        p.lineTo(X(17.6), Y(5.5))
        p.lineTo(X(13.6), Y(8.5))
        p.close()
        c.drawPath(p, stroke=1, fill=0)
    elif name == "link":
        c.roundRect(X(2.4), Y(7.4), 9 * u, 5.2 * u, 2.6 * u, stroke=1, fill=0)
        c.roundRect(X(8.6), Y(7.4), 9 * u, 5.2 * u, 2.6 * u, stroke=1, fill=0)
        c.line(X(9.4), Y(10), X(10.6), Y(10))
    elif name == "layers":
        for dy in (0, 3.6, 7.2):
            p = c.beginPath()
            p.moveTo(X(10), Y(4.4 + dy))
            p.lineTo(X(17), Y(7.6 + dy))
            p.lineTo(X(10), Y(10.8 + dy))
            p.lineTo(X(3), Y(7.6 + dy))
            p.close()
            c.drawPath(p, stroke=1, fill=0)
    elif name == "cnc":
        c.line(X(2.6), Y(3.2), X(17.4), Y(3.2))
        c.roundRect(X(7.4), Y(12), 5.2 * u, 5.6 * u, 1 * u, stroke=1, fill=0)
        p = c.beginPath()
        p.moveTo(X(8.2), Y(12))
        p.lineTo(X(10), Y(7))
        p.lineTo(X(11.8), Y(12))
        c.drawPath(p, stroke=1, fill=0)
        c.line(X(10), Y(7), X(10), Y(3.2))
        c.line(X(4.4), Y(3.2), X(4.4), Y(6))
        c.line(X(15.6), Y(3.2), X(15.6), Y(6))
    elif name == "speaker":
        c.roundRect(X(4.5), Y(2.5), 11 * u, 15 * u, 1.4 * u, stroke=1, fill=0)
        c.circle(X(10), Y(7.6), 3.4 * u, stroke=1, fill=0)
        c.circle(X(10), Y(7.6), 1.1 * u, stroke=0, fill=1)
        c.circle(X(10), Y(14.6), 1.7 * u, stroke=1, fill=0)
    elif name == "tag":
        p = c.beginPath()
        p.moveTo(X(3.2), Y(10.6))
        p.lineTo(X(10.4), Y(3.4))
        p.lineTo(X(17), Y(10))
        p.lineTo(X(9.8), Y(17.2))
        p.close()
        c.drawPath(p, stroke=1, fill=0)
        c.circle(X(13), Y(13), 1.5 * u, stroke=1, fill=0)
    elif name == "euro":
        c.circle(X(10), Y(10), 8.2 * u, stroke=1, fill=0)
        c.line(X(5.6), Y(9), X(12.6), Y(9))
        c.line(X(5.6), Y(11.6), X(12.6), Y(11.6))
        p = c.beginPath()
        p.moveTo(X(13.6), Y(6.4))
        p.curveTo(X(7), Y(4.4), X(6.4), Y(15.6), X(13.6), Y(14))
        c.drawPath(p, stroke=1, fill=0)
    elif name == "boxes":
        c.rect(X(2.6), Y(3), 6.6 * u, 6.6 * u, stroke=1, fill=0)
        c.rect(X(10.8), Y(3), 6.6 * u, 6.6 * u, stroke=1, fill=0)
        c.rect(X(6.7), Y(11), 6.6 * u, 6.6 * u, stroke=1, fill=0)
    elif name == "star":
        p = c.beginPath()
        for i in range(10):
            r = (8.4 if i % 2 == 0 else 3.6) * u
            a = math.pi / 2 + i * math.pi / 5
            px, py = x + 10 * u + r * math.cos(a), y + 10 * u + r * math.sin(a)
            p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
        p.close()
        c.drawPath(p, stroke=1, fill=0)
    elif name == "wood":
        c.roundRect(X(2.6), Y(5), 14.8 * u, 10 * u, 1.2 * u, stroke=1, fill=0)
        for dy in (7.6, 10, 12.4):
            c.line(X(5), Y(dy), X(15), Y(dy))
    elif name == "tools":                       # atelier / fabrication
        c.line(X(3.4), Y(3.4), X(11), Y(11))
        c.circle(X(13.6), Y(13.6), 3.6 * u, stroke=1, fill=0)
        c.line(X(11.4), Y(16.2), X(16.2), Y(11.4))
    elif name == "shield":
        p = c.beginPath()
        p.moveTo(X(10), Y(18.4))
        p.lineTo(X(17), Y(15))
        p.lineTo(X(17), Y(8.6))
        p.curveTo(X(17), Y(4.6), X(13.6), Y(2.6), X(10), Y(1.6))
        p.curveTo(X(6.4), Y(2.6), X(3), Y(4.6), X(3), Y(8.6))
        p.lineTo(X(3), Y(15))
        p.close()
        c.drawPath(p, stroke=1, fill=0)
    elif name == "recycle":
        for k in range(3):
            a = math.pi / 2 + k * 2 * math.pi / 3
            px, py = x + 10 * u + 6 * u * math.cos(a), y + 10 * u + 6 * u * math.sin(a)
            c.circle(px, py, 1.6 * u, stroke=0, fill=1)
        c.circle(X(10), Y(10), 6 * u, stroke=1, fill=0)
    elif name == "camera":
        c.roundRect(X(2.4), Y(4.6), 15.2 * u, 10.8 * u, 1.8 * u, stroke=1, fill=0)
        c.circle(X(10), Y(10), 3.4 * u, stroke=1, fill=0)
        c.rect(X(7.4), Y(15.4), 5.2 * u, 1.8 * u, stroke=1, fill=0)
    elif name == "door":                       # visite d'atelier
        c.rect(X(4.4), Y(2.6), 11.2 * u, 15 * u, stroke=1, fill=0)
        c.circle(X(12.6), Y(10), 1 * u, stroke=0, fill=1)
    elif name == "clock":
        c.circle(X(10), Y(10), 8.2 * u, stroke=1, fill=0)
        c.line(X(10), Y(10), X(10), Y(15))
        c.line(X(10), Y(10), X(13.6), Y(8.4))
    c.restoreState()


# ───────────────────────── cartes (icône alignée au titre) ─────────────────────────
PAD = 18
TS, TL = 10.2, 13.4
BS, BL = 8.6, 12.8
IC = 15


def card_lines(c, w, ttl, txt):
    iw = w - 2 * PAD - IC - 9
    return (len(wrap(c, ttl, "Inter-SB", TS, iw)),
            sum(len(wrap(c, b, "Inter-L", BS, w - 2 * PAD)) for b in txt.split("\n") if b.strip()))


def card_metrics(c, w, items):
    """(hauteur, nb lignes de titre) communs à une rangée de cartes"""
    nt = max(card_lines(c, w, t, tx)[0] for _, t, tx in items)
    nb = max(card_lines(c, w, t, tx)[1] for _, t, tx in items)
    return PAD + nt * TL + 10 + nb * BL + PAD - 2, nt


def card_h(c, w, ttl, txt):
    nt, nb = card_lines(c, w, ttl, txt)
    return PAD + nt * TL + 10 + nb * BL + PAD - 2


def card(c, x, y, w, h, ic, ttl, txt, tint=False, stroke=LINE, nt=None):
    rrect(c, x, y, w, h, 8, fill=LIGHT if tint else WHITE, stroke=stroke)
    iw = w - 2 * PAD - IC - 9
    ty = y + h - PAD - 10
    if ic:
        icon(c, ic, x + PAD, ty - 4.2, IC, BLUE, 1.15)
    tx = x + PAD + (IC + 9 if ic else 0)
    lines = wrap(c, ttl, "Inter-SB", TS, iw)
    for ln in lines:
        ls_text(c, tx, ty, ln, "Inter-SB", TS, INK)
        ty -= TL
    nt = nt or len(lines)
    by = y + h - PAD - 10 - nt * TL - 10
    para(c, x + PAD, by, txt, "Inter-L", BS, BL, w - 2 * PAD, GREY)


def band(c, x, y_top, w, ic, ttl, txt, bg=BLUE, sub=HexColor("#D3E0FF"), accent=None):
    iw = w - 92
    lines = wrap(c, txt, "Inter-L", 8.9, iw)
    h = 30 + 16 + len(lines) * 13 + 12
    y = y_top - h
    rrect(c, x, y, w, h, 8, fill=bg)
    if accent:
        c.setFillColor(accent)
        c.rect(x, y, 3.4, h, stroke=0, fill=1)
    if ic:
        icon(c, ic, x + 24, y + h - 46, 20, WHITE if bg != INK else BLUE, 1.2)
    ls_text(c, x + 60, y + h - 30, ttl, "Inter-SB", 11.4, WHITE)
    ty = y + h - 48
    for ln in lines:
        ls_text(c, x + 60, ty, ln, "Inter-L", 8.9, sub)
        ty -= 13
    return y


def stat(c, x, y, w, big, small):
    size = 21
    while tw(c, big, "Inter-B", size, -0.6) > w and size > 12:
        size -= 0.5
    ls_text(c, x, y, big, "Inter-B", size, INK, -0.6)
    ty = y - 15
    for ln in wrap(c, small, "Inter-L", 7.8, w):
        ls_text(c, x, ty, ln, "Inter-L", 7.8, GREY)
        ty -= 10.8
    return ty
