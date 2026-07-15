# -*- coding: utf-8 -*-
from reportlab.lib.colors import Color, HexColor

from ..components import *   # noqa
from . import page


@page("gazmatek", priority="required")
def render(c, ctx):
    cfg, m = ctx.cfg, ctx.module
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    hero_h = 268
    hb = H - hero_h
    img_cover(c, P(cfg["images"]["gazmatek_hero"]), 0, hb, W, hero_h)
    c.saveState()
    c.setFillColor(Color(0, 0, 0, alpha=0.38))
    c.rect(0, hb, W, hero_h, stroke=0, fill=1)
    c.restoreState()
    veil(c, 0, hb, W, hero_h * 0.72, BLACK, top=0.0, bottom=0.9)

    c.drawImage(P("gaz_white.png"), M, H - 108, 40, 45.1, mask='auto')
    ls_text(c, W - M, H - 84, "LE PROJET CULTUREL", "Inter-M", 8, HexColor("#C9CDD4"), 1.8,
            align="r")
    ls_text(c, M, hb + 92, "Gazmatek :", "Inter-B", 27, WHITE, -0.6)
    ls_text(c, M, hb + 60, "créer des expériences", "Inter-L", 27, WHITE, -0.6)
    ls_text(c, M, hb + 28, "culturelles uniques.", "Inter-L", 27, WHITE, -0.6)

    y = hb - 40
    y = para(c, M, y, m["gazmatek"]["intro"], "Inter-L", 10.8, 16.6, CW - 40, BODY) - 22

    eyebrow(c, M, y, "NOS AFFICHES")
    y -= 16
    pw = (CW - 3 * 10) / 4
    for i, po in enumerate(cfg["images"]["posters"]):
        img_fit(c, po, M + i * (pw + 10), y - pw, pw, pw)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.rect(M + i * (pw + 10), y - pw, pw, pw, stroke=1, fill=0)
    y -= pw + 22

    eyebrow(c, M, y, "NOS ÉVÉNEMENTS")
    y -= 16
    gh, gw = 96, (CW - 2 * 10) / 3
    for i, g in enumerate(cfg["images"]["events"]):
        img_box(c, g, M + i * (gw + 10), y - gh, gw, gh)
    y -= gh + 22

    band(c, M, y, CW, "megaphone", m["gazmatek"]["band"]["title"], m["gazmatek"]["band"]["text"])
