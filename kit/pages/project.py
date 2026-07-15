# -*- coding: utf-8 -*-
from reportlab.lib.colors import HexColor

from ..components import *   # noqa
from . import page


@page("project", priority="required")
def render(c, ctx):
    m = ctx.module
    pr = m["project"]
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("03", pr.get("kicker", "Le projet"), pr["title"]) - 32
    y = para(c, M, y, pr["intro"], "Inter-L", 11.4, 17.6, CW - 30, INK) - 8
    y = para(c, M, y, pr["intro2"], width=CW - 30) - 26

    ph, gap = 226, 12
    py = y - ph
    ims = pr["images"]
    lw = CW * 0.44
    rw = CW - lw - gap
    h_top = (ph - gap) * 0.56
    h_bot = ph - gap - h_top
    img_box(c, ims[0]["file"], M, py, lw, ph)
    if ims[1].get("fit"):
        img_fit(c, ims[1]["file"], M + lw + gap, py + h_bot + gap, rw, h_top,
                HexColor("#3C424C"))
        c.setStrokeColor(LINE)
        c.rect(M + lw + gap, py + h_bot + gap, rw, h_top, stroke=1, fill=0)
    else:
        img_box(c, ims[1]["file"], M + lw + gap, py + h_bot + gap, rw, h_top)
    img_box(c, ims[2]["file"], M + lw + gap, py, rw, h_bot)
    photo_caption(c, M, py, ims[0]["caption"].upper())
    photo_caption(c, M + lw + gap, py + h_bot + gap, ims[1]["caption"].upper())
    photo_caption(c, M + lw + gap, py, ims[2]["caption"].upper())
    ls_text(c, M, py - 16, pr["caption"], "Inter-L", 7.8, GREY, 0.4)

    y = py - 42
    eyebrow(c, M, y, m["needs"]["title"])
    cards(c, y - 20, m["needs"]["items"])
