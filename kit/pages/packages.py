# -*- coding: utf-8 -*-
from reportlab.lib.colors import HexColor

from ..components import *   # noqa
from . import page


@page("packages", priority="required")
def render(c, ctx):
    cfg, m = ctx.cfg, ctx.module
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("07", "Formes de collaboration", "Ce que nous recherchons") - 30
    y = para(c, M, y, m["packages"]["intro"], "Inter-L", 11, 17, CW - 40, BODY) - 24
    y = rows_list(c, y, m["packages"]["items"]) - 14
    band(c, M, y, CW, "link", cfg["collab_band"]["title"], cfg["collab_band"]["text"],
         bg=INK, sub=HexColor("#9AA1AC"), accent=BLUE)
