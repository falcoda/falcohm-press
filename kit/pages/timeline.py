# -*- coding: utf-8 -*-
from reportlab.lib.colors import HexColor

from ..components import *   # noqa
from . import page


@page("timeline")
def render(c, ctx):
    cfg, m = ctx.cfg, ctx.module
    c.setFillColor(LIGHT)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("05", "Trajectoire", "Un partenariat qui\ns'inscrit dans la durée.") - 32
    y = para(c, M, y, m["timeline"]["intro"], "Inter-L", 11.2, 17.4, CW - 40, BODY) - 34

    steps = []
    for s in cfg["timeline"]:
        s = dict(s)
        ov = m["timeline"].get("overrides", {}).get(s["year"])
        if ov:
            s.update(ov)
        steps.append(s)

    lx = M + 54
    c.setStrokeColor(HexColor("#D7DAE0"))
    c.setLineWidth(1)
    c.line(lx, y - len(steps) * 40 + 12, lx, y + 4)
    for i, s in enumerate(steps):
        sy = y - i * 40
        last = i >= len(steps) - 2
        c.setFillColor(BLUE if last else WHITE)
        c.setStrokeColor(BLUE if last else HexColor("#C6CBD3"))
        c.setLineWidth(1.2)
        c.circle(lx, sy - 3, 5, stroke=1, fill=1)
        ls_text(c, lx - 16, sy, s["year"], "Inter-B", 10.4, BLUE if last else GREY, 0.4,
                align="r")
        ls_text(c, lx + 18, sy, s["title"], "Inter-SB", 10.8, INK)
        ls_text(c, lx + 18, sy - 13, s["text"], "Inter-L", 8.6, GREY)
    y = y - len(steps) * 40 - 10

    eyebrow(c, M, y, "CE QUI VIENT ENSUITE")
    y = cards(c, y - 20, m["timeline"]["next"]) - 24
    band(c, M, y, CW, "clock", m["timeline"]["band"]["title"], m["timeline"]["band"]["text"],
         bg=INK, sub=HexColor("#9AA1AC"), accent=BLUE)
