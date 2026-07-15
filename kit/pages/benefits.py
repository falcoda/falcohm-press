# -*- coding: utf-8 -*-
from reportlab.lib.colors import HexColor

from ..components import *   # noqa
from . import page


def _mockups(c, ctx, y):
    cfg, m = ctx.cfg, ctx.module
    mh, mw = 122, (CW - 2 * 12) / 3
    myy = y - mh
    mx = M
    # 1 — sites internet
    rrect(c, mx, myy, mw, mh, 6, fill=LIGHT, stroke=LINE)
    c.setFillColor(HexColor("#E4E6EA"))
    c.roundRect(mx + 1, myy + mh - 16, mw - 2, 15, 4, stroke=0, fill=1)
    c.setFillColor(HexColor("#CBD0D7"))
    for k in range(3):
        c.circle(mx + 12 + k * 7, myy + mh - 8.5, 1.9, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.rect(mx + 38, myy + mh - 13, mw - 52, 8, stroke=0, fill=1)
    ls_text(c, mx + 42, myy + mh - 11.2, "gazmatek.com/partenaires", "Inter-L", 4.4, GREY)
    ls_text(c, mx + 14, myy + mh - 32, "NOS PARTENAIRES", "Inter-B", 6, INK, 1.2)
    for r in range(2):
        for k in range(3):
            bxx = mx + 14 + k * ((mw - 28) / 3)
            byy = myy + mh - 52 - r * 21
            bwid = (mw - 28) / 3 - 6
            if r == 0 and k == 0:
                rrect(c, bxx, byy, bwid, 16, 2, fill=BLUE)
                ls_text(c, bxx + bwid / 2, byy + 5.8, "VOTRE LOGO", "Inter-B", 4.2, WHITE, 0.6,
                        align="c")
            else:
                rrect(c, bxx, byy, bwid, 16, 2, fill=WHITE, stroke=LINE)
    ls_text(c, mx + 14, myy + 12, "Sites Gazmatek & Falc'ohm", "Inter-M", 6.8, GREY, 0.4)

    # 2 — post réseaux
    mx2 = mx + mw + 12
    rrect(c, mx2, myy, mw, mh, 6, fill=LIGHT, stroke=LINE)
    img_cover(c, P(cfg["images"]["mockup_post"]), mx2 + 1, myy + mh - 52, mw - 2, 51)
    c.setFillColor(WHITE)
    c.circle(mx2 + 17, myy + mh - 66, 7, stroke=0, fill=1)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.circle(mx2 + 17, myy + mh - 66, 7, stroke=1, fill=0)
    c.drawImage(P("gaz_dark.png"), mx2 + 12, myy + mh - 72.5, 10, 11.3, mask='auto')
    ls_text(c, mx2 + 29, myy + mh - 64, "gazmatek", "Inter-SB", 6.2, INK)
    ls_text(c, mx2 + 29, myy + mh - 72, "Brabant wallon, Belgique", "Inter-L", 5, GREY)
    tyy = myy + mh - 84
    for ln in wrap(c, m["benefits"]["post_text"], "Inter-L", 5.4, mw - 28)[:2]:
        ls_text(c, mx2 + 14, tyy, ln, "Inter-L", 5.4, BODY)
        tyy -= 7.6
    ls_text(c, mx2 + 14, myy + 12, "Réseaux, %s abonnés" % cfg["followers"], "Inter-M", 6.8,
            GREY, 0.4)

    # 3 — marquage matériel
    mx3 = mx2 + mw + 12
    rrect(c, mx3, myy, mw, mh, 6, fill=LIGHT, stroke=LINE)
    ex = mx3 + (mw - 58) / 2
    ey = myy + 30
    c.setFillColor(HexColor("#1A1C21"))
    c.roundRect(ex, ey, 58, 80, 4, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#33373E"))
    c.setLineWidth(0.8)
    c.roundRect(ex + 9, ey + 10, 40, 24, 2, stroke=1, fill=0)
    c.circle(ex + 20, ey + 22, 4, stroke=1, fill=0)
    c.circle(ex + 38, ey + 22, 4, stroke=1, fill=0)
    rrect(c, ex + 10, ey + 52, 38, 14, 2, fill=BLUE)
    ls_text(c, ex + 29, ey + 57.6, "VOTRE LOGO", "Inter-B", 4, WHITE, 0.5, align="c")
    ls_text(c, ex + 29, ey + 43, m["benefits"]["marking_text"], "Inter-M", 3.3,
            HexColor("#8A9099"), 0.4, align="c")
    ls_text(c, mx3 + 14, myy + 20, m["benefits"]["marking_label"], "Inter-M", 6.8, GREY, 0.4)
    ls_text(c, mx3 + 14, myy + 11, "Support fourni par le partenaire", "Inter-L", 6.2, GREY)


@page("benefits", priority="required")
def render(c, ctx):
    cfg, m = ctx.cfg, ctx.module
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("06", "Contreparties", "Pourquoi devenir partenaire ?") - 30
    y = para(c, M, y, m["benefits"]["intro"], "Inter-L", 11, 17, CW - 60, BODY) - 22
    y = cards(c, y, cfg["benefits"], tint=True) - 14
    y = band(c, M, y, CW, "link", cfg["benefits_band"]["title"], m["benefits"]["band_text"],
             bg=INK, sub=HexColor("#9AA1AC")) - 24
    eyebrow(c, M, y, "VOTRE MARQUE, PARTOUT OÙ NOUS SOMMES")
    _mockups(c, ctx, y - 16)
