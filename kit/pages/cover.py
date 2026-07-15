# -*- coding: utf-8 -*-
from reportlab.lib.colors import Color, HexColor

from ..components import *   # noqa
from . import page


@page("cover", priority="required")
def render(c, ctx):
    cfg, m = ctx.cfg, ctx.module
    img_cover(c, P(cfg["images"]["cover"]), 0, 0, W, H)
    c.saveState()
    c.setFillColor(Color(0, 0, 0, alpha=0.30))
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.restoreState()
    veil(c, 0, 0, W, H * 0.60, BLACK, top=0.0, bottom=0.95)
    veil(c, 0, H * 0.80, W, H * 0.20, BLACK, top=0.78, bottom=0.0)

    c.drawImage(P("eagle_white.png"), M, H - 106, 48, 42.1, mask='auto')
    c.drawImage(P("gaz_white.png"), M + 64, H - 108, 42, 47.4, mask='auto')
    ls_text(c, W - M, H - 82, "DOSSIER DE PARTENARIAT · %s" % cfg["year"], "Inter-M", 8,
            WHITE, 1.8, align="r")

    by = 214
    c.setStrokeColor(BLUE)
    c.setLineWidth(2.2)
    c.line(M, by + 196, M + 46, by + 196)
    ls_text(c, M, by + 168, m["cover"]["kicker"].upper(), "Inter-B", 9.4, WHITE, 2.4)
    ls_text(c, M, by + 108, "Partenariat", "Inter-B", 44, WHITE, -1.2)
    ls_text(c, M, by + 58, "Falc'ohm System", "Inter-L", 44, WHITE, -1.2)
    ls_text(c, M + tw(c, "Falc'ohm System", "Inter-L", 44, -1.2) + 14, by + 58, "ASBL",
            "Inter-L", 44, HexColor("#7FA0F0"), -1.2)
    ls_text(c, M, by + 26, m["cover"]["subtitle"], "Inter-L", 12.6, HexColor("#C9CDD4"))

    c.setStrokeColor(Color(1, 1, 1, alpha=0.22))
    c.setLineWidth(0.7)
    c.line(M, 116, W - M, 116)
    org = cfg["org"]
    s1, s2 = org["sites"][0], org["sites"][1]
    ls_text(c, M, 92, s1["label"], "Inter-M", 9.2, WHITE, 0.6)
    link(c, M, 92, tw(c, s1["label"], "Inter-M", 9.2, 0.6), 11, s1["url"])
    x2 = M + tw(c, s1["label"], "Inter-M", 9.2, 0.6) + 10
    ls_text(c, x2, 92, "·", "Inter-M", 9.2, HexColor("#8A9099"), 0.6)
    ls_text(c, x2 + 12, 92, s2["label"], "Inter-M", 9.2, WHITE, 0.6)
    link(c, x2 + 12, 92, tw(c, s2["label"], "Inter-M", 9.2, 0.6), 11, s2["url"])
    ls_text(c, W - M, 98, org["contact"]["name"], "Inter-M", 9.2, WHITE, 0.4, align="r")
    ls_text(c, W - M, 84, "%s, %s" % (org["contact"]["role"], org["name"]), "Inter-L", 8.4,
            HexColor("#A9AEB6"), 0.4, align="r")
    ctx.no_footer = True
