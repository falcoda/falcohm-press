# -*- coding: utf-8 -*-
from reportlab.lib.colors import HexColor

from ..components import *   # noqa
from . import page


@page("ecosystem", priority="required")
def render(c, ctx):
    cfg, m = ctx.cfg, ctx.module
    c.setFillColor(LIGHT)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("02", "Notre organisation", "Deux projets,\nune même ambition.")
    y = para(c, M, y - 32, m["ecosystem"]["intro"], "Inter-L", 11.2, 17.4, CW - 30, BODY) - 30

    bw, bh = (CW - 2 * 34) / 3, 186
    byy = y - bh
    blocks = [
        ("Gazmatek", "Le projet culturel", cfg["org_blocks"]["gazmatek"], "dark"),
        ("Falc'ohm System", "Le pôle technique", cfg["org_blocks"]["falcohm"], "white"),
        ("Votre entreprise", m["partner"]["role"], m["partner"]["items"], "blue"),
    ]
    for i, (nm, sub, items, style) in enumerate(blocks):
        bx = M + i * (bw + 34)
        dark = style == "dark"
        if style == "blue":
            rrect(c, bx, byy, bw, bh, 8, fill=WHITE, stroke=BLUE, lw=1.4)
        else:
            rrect(c, bx, byy, bw, bh, 8, fill=INK if dark else WHITE,
                  stroke=None if dark else LINE)
        if i == 0:
            c.drawImage(P("gaz_white.png"), bx + 18, byy + bh - 50, 26, 29.3, mask='auto')
        elif i == 1:
            c.drawImage(P("typo_black.png"), bx + 18, byy + bh - 42, 74, 19.4, mask='auto')
        else:
            icon(c, m["partner"]["icon"], bx + 18, byy + bh - 46, 22, BLUE, 1.2)
        tcol = WHITE if dark else (BLUE if style == "blue" else INK)
        scol = HexColor("#8A9099") if dark else (BLUE if style == "blue" else GREY)
        ls_text(c, bx + 18, byy + bh - 68, nm, "Inter-B", 12, tcol)
        ls_text(c, bx + 18, byy + bh - 81, sub, "Inter-M", 7.4, scol, 1.1)
        c.setStrokeColor(HexColor("#2A2E35") if dark else LINE)
        c.setLineWidth(0.7)
        c.line(bx + 18, byy + bh - 93, bx + bw - 18, byy + bh - 93)
        iy = byy + bh - 111
        for it in items:
            c.setFillColor(BLUE)
            c.circle(bx + 21, iy + 3, 1.7, stroke=0, fill=1)
            ls_text(c, bx + 29, iy, it, "Inter-L", 8.6, HexColor("#C9CDD4") if dark else BODY)
            iy -= 15
        if i < 2:
            ax = bx + bw + 9
            c.setStrokeColor(BLUE)
            c.setLineWidth(1.2)
            c.line(ax, byy + bh / 2, ax + 12, byy + bh / 2)
            p = c.beginPath()
            p.moveTo(ax + 9, byy + bh / 2 + 3.4)
            p.lineTo(ax + 14, byy + bh / 2)
            p.lineTo(ax + 9, byy + bh / 2 - 3.4)
            c.drawPath(p, stroke=1, fill=0)

    y = band(c, M, byy - 26, CW, "speaker", m["ecosystem"]["band"]["title"],
             m["ecosystem"]["band"]["text"]) - 26
    photo_band(c, cfg["images"]["org_band"], y, 84, cfg["images"]["org_band_caption"])
