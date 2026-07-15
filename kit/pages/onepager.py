# -*- coding: utf-8 -*-
"""One-pager : le dossier en une seule page, pour une relance ou une pièce jointe légère."""
from reportlab.lib.colors import Color, HexColor

from ..components import *   # noqa
from . import page


@page("onepager")
def render(c, ctx):
    cfg, m = ctx.cfg, ctx.module
    t = ctx.target or {}

    # bandeau haut
    hh = 176
    img_cover(c, P(cfg["images"]["cover"]), 0, H - hh, W, hh)
    c.saveState()
    c.setFillColor(Color(0, 0, 0, alpha=0.45))
    c.rect(0, H - hh, W, hh, stroke=0, fill=1)
    c.restoreState()
    veil(c, 0, H - hh, W, hh * 0.8, BLACK, top=0.0, bottom=0.85)
    c.drawImage(P("eagle_white.png"), M, H - 62, 34, 29.8, mask='auto')
    c.drawImage(P("gaz_white.png"), M + 44, H - 64, 28, 31.6, mask='auto')
    ls_text(c, W - M, H - 46, "DOSSIER DE PARTENARIAT · %s" % cfg["year"], "Inter-M", 7.4,
            HexColor("#C9CDD4"), 1.6, align="r")
    ls_text(c, M, H - hh + 58, m["cover"]["kicker"].upper(), "Inter-B", 8.4, WHITE, 2.0)
    title_w = tw(c, "Falc'ohm System ASBL", "Inter-B", 22, -0.6)
    ls_text(c, M, H - hh + 28, "Falc'ohm System ASBL", "Inter-B", 22, WHITE, -0.6)
    if t.get("company"):
        # « Pour <nom> », calé à droite. Un nom d'organisme public déborderait sous le titre :
        # on prend le nom court s'il existe, et on tronque dans l'espace qui reste.
        who = t.get("display_name") or t["company"]
        avail = CW - title_w - 24
        ls_text(c, W - M, H - hh + 28, "Pour %s" % ellipsize(c, who, "Inter-L", 13, avail),
                "Inter-L", 13, HexColor("#9FB4E8"), 0, align="r")

    y = H - hh - 34
    y = para(c, M, y, m["onepager"]["pitch"] if m.get("onepager") else m["project"]["intro"],
             "Inter-L", 10.8, 16.4, CW, INK) - 22

    y = stats_strip(c, y, cfg["stats"]["items"]) - 26

    # deux colonnes : ce que nous cherchons / ce que nous offrons
    colw = (CW - 16) / 2
    eyebrow(c, M, y, "CE QUE NOUS RECHERCHONS")
    eyebrow(c, M + colw + 16, y, "CE QUE NOUS OFFRONS")
    ly = y - 20
    for it in m["needs"]["items"]:
        icon(c, it["icon"], M, ly - 4, 14, BLUE, 1.1)
        ls_text(c, M + 22, ly, it["title"], "Inter-SB", 9.6, INK)
        ly2 = para(c, M + 22, ly - 13, it["text"], "Inter-L", 8.4, 11.6, colw - 22, GREY)
        ly = ly2 - 8
    ry = y - 20
    for b in cfg["benefits"][:4]:
        icon(c, b["icon"], M + colw + 16, ry - 4, 14, BLUE, 1.1)
        ls_text(c, M + colw + 38, ry, b["title"], "Inter-SB", 9.6, INK)
        ry2 = para(c, M + colw + 38, ry - 13, b["text"], "Inter-L", 8.4, 11.6, colw - 22, GREY)
        ry = ry2 - 8
    y = min(ly, ry) - 10

    y = band(c, M, y, CW, "clock", m["timeline"]["band"]["title"],
             m["timeline"]["band"]["text"], bg=INK, sub=HexColor("#9AA1AC"), accent=BLUE) - 22

    # contact compact
    org = cfg["org"]
    rrect(c, M, y - 62, CW, 62, 8, fill=LIGHT)
    ls_text(c, M + 20, y - 26, org["contact"]["name"], "Inter-SB", 11.4, INK)
    ls_text(c, M + 20, y - 42, "%s, %s" % (org["contact"]["role"], org["name"]),
            "Inter-L", 8.8, GREY)
    ls_text(c, M + 20, y - 55, "%s  ·  %s" % (org["contact"]["email"],
                                              org["sites"][0]["label"]), "Inter-M", 8.4, BLUE)
    link(c, M + 20, y - 55, tw(c, org["contact"]["email"], "Inter-M", 8.4), 10,
         "mailto:%s" % org["contact"]["email"])
    ctx.no_footer = True
