# -*- coding: utf-8 -*-
from ..components import *   # noqa
from . import page


@page("about", priority="required")
def render(c, ctx):
    cfg = ctx.cfg
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("01", "L'association", "Qui sommes-nous ?", size=30)
    y -= 30
    for ln in wrap(c, cfg["about"]["lead"], "Inter-L", 13.2, CW - 40):
        ls_text(c, M, y, ln, "Inter-L", 13.2, INK)
        y -= 20.5
    y -= 16
    col = (CW - 26) / 2
    y = min(para(c, M, y, cfg["about"]["col1"], width=col),
            para(c, M + col + 26, y, cfg["about"]["col2"], width=col)) - 30

    eyebrow(c, M, y, cfg["stats"]["title"])
    y = stats_strip(c, y - 22, cfg["stats"]["items"]) - 26
    y = chips(c, y, cfg["chips"]) - 14
    photo_band(c, cfg["images"]["about_band"], y, 84, cfg["images"]["about_band_caption"])
