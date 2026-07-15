# -*- coding: utf-8 -*-
"""Composants réutilisables (au-dessus des primitives de core.py)."""
import os
from reportlab.lib.colors import Color, HexColor
from PIL import Image as _Im

from .core import *   # noqa

P = asset  # alias : P("cover.jpg") -> chemin absolu


def img_fit(c, name, x, y, w, h, bg=HexColor("#15171C")):
    """Image « contain » : entière, sur un fond (affiches, rendus 3D)."""
    path = optimized(P(name), w, h)
    iw, ih = _Im.open(path).size
    c.setFillColor(bg)
    c.rect(x, y, w, h, stroke=0, fill=1)
    sc = min(w / iw, h / ih)
    c.drawImage(path, x + (w - iw * sc) / 2, y + (h - ih * sc) / 2, iw * sc, ih * sc, mask='auto')


def img_box(c, name, x, y, w, h):
    """Image « cover » (crop centré) + filet."""
    img_cover(c, P(name), x, y, w, h)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.rect(x, y, w, h, stroke=1, fill=0)


def link(c, x, y, w, h, url):
    c.linkURL(url, (x, y - 3, x + w, y + h), relative=0, thickness=0)


def photo_caption(c, x, y, txt):
    """Pastille de légende posée en bas à gauche d'une photo."""
    rrect(c, x + 8, y + 8, tw(c, txt, "Inter-M", 6.6, 0.6) + 16, 15, 3,
          fill=Color(0, 0, 0, alpha=0.62))
    ls_text(c, x + 16, y + 12.6, txt, "Inter-M", 6.6, WHITE, 0.6)


def photo_band(c, name, y_top, y_bottom, caption=None):
    """Bande photo pleine largeur, assombrie, avec légende."""
    h = max(y_top - y_bottom, 110)
    img_cover(c, P(name), 0, y_bottom, W, h)
    veil(c, 0, y_bottom, W, h * 0.65, BLACK, top=0.0, bottom=0.85)
    if caption:
        ls_text(c, M, y_bottom + 22, caption, "Inter-M", 8.6, WHITE, 0.8)
    return y_bottom


def cards(c, y, items, cols=3, tint=False):
    """Grille de cartes (icône alignée au titre, corps aligné entre cartes)."""
    cw = (CW - (cols - 1) * 12) / cols
    triplets = [(i["icon"], i["title"], i["text"]) for i in items]
    ch, nt = card_metrics(c, cw, triplets)
    rows = (len(items) + cols - 1) // cols
    for k, (ic, t, tx) in enumerate(triplets):
        x = M + (k % cols) * (cw + 12)
        yy = y - ch - (k // cols) * (ch + 12)
        card(c, x, yy, cw, ch, ic, t, tx, tint=tint, nt=nt)
    return y - rows * ch - (rows - 1) * 12


def rows_list(c, y, items, rh=54):
    """Liste de lignes « icône | titre + texte | check »."""
    for i, o in enumerate(items):
        ry = y - (i + 1) * (rh + 8) + 8
        rrect(c, M, ry, CW, rh, 7, fill=WHITE, stroke=LINE)
        c.setFillColor(LIGHT)
        c.roundRect(M + 1, ry + 1, 52, rh - 2, 6, stroke=0, fill=1)
        icon(c, o["icon"], M + 18, ry + rh / 2 - 8.5, 17, BLUE)
        ls_text(c, M + 70, ry + rh - 22, o["title"], "Inter-SB", 10.6, INK)
        ls_text(c, M + 70, ry + 14, o["text"], "Inter-L", 8.8, GREY)
        icon(c, "check", W - M - 34, ry + rh / 2 - 8, 16, HexColor("#C9D6F7"), 1.1)
    return y - len(items) * (rh + 8)


def checklist(c, y, items, cols=2, rh=60):
    """Arguments « ✓ titre + texte » sur deux colonnes."""
    cw = (CW - 14) / cols
    for i, pr in enumerate(items):
        rx = M + (i % cols) * (cw + 14)
        ry = y - (i // cols + 1) * (rh + 10) + 10
        rrect(c, rx, ry, cw, rh, 7, fill=WHITE, stroke=LINE)
        icon(c, "check", rx + 16, ry + rh - 28, 16, BLUE, 1.15)
        ls_text(c, rx + 42, ry + rh - 25, pr["title"], "Inter-SB", 9.8, INK)
        para(c, rx + 42, ry + rh - 42, pr["text"], "Inter-L", 8.2, 11.4, cw - 58, GREY)
    rows = (len(items) + cols - 1) // cols
    return y - rows * (rh + 10)


def stats_strip(c, y, stats, h=92):
    """Bandeau de chiffres clés."""
    rrect(c, M, y - h, CW, h, 8, fill=LIGHT)
    cwid = CW / len(stats)
    for i, s in enumerate(stats):
        sx = M + i * cwid
        if i:
            c.setStrokeColor(HexColor("#E1E3E7"))
            c.setLineWidth(0.7)
            c.line(sx, y - h + 18, sx, y - 18)
        stat(c, sx + 15, y - 32, cwid - 30, s["value"], s["label"])
    return y - h


def chips(c, y, labels):
    cx = M
    for ch_ in labels:
        chw = c.stringWidth(ch_, "Inter-M", 8.4) + 30
        rrect(c, cx, y - 16, chw, 22, 11, stroke=LINE)
        c.setFillColor(BLUE)
        c.circle(cx + 11, y - 5, 1.8, stroke=0, fill=1)
        ls_text(c, cx + 19, y - 8, ch_, "Inter-M", 8.4, INK, 0.3)
        cx += chw + 8
    return y - 16
