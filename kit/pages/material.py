# -*- coding: utf-8 -*-
from reportlab.lib.colors import HexColor

from ..components import *   # noqa
from . import page


@page("material", audience=("wood", "audio", "hardware"), requires="material")
def render(c, ctx):
    cfg, m = ctx.cfg, ctx.module
    mat = m["material"]
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("04", mat.get("kicker", "La matière"), mat["title"]) - 32
    y = para(c, M, y, mat["intro"], "Inter-L", 11.2, 17.4, CW - 30, INK) - 26
    y = checklist(c, y, mat["props"]) - 22

    eyebrow(c, M, y, "NOTRE APPROCHE")
    y = cards(c, y - 20, cfg["approach"], tint=True) - 24
    band(c, M, y, CW, "clock", cfg["partner_band"]["title"], cfg["partner_band"]["text"],
         bg=INK, sub=HexColor("#9AA1AC"), accent=BLUE)
