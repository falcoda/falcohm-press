# -*- coding: utf-8 -*-
from reportlab.lib.colors import Color, HexColor
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

from ..components import *   # noqa
from . import page


@page("contact", priority="required")
def render(c, ctx):
    cfg = ctx.cfg
    org = cfg["org"]
    c.setFillColor(BLACK)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    img_cover(c, P(cfg["images"]["thanks"]), 0, H - 320, W, 320)
    c.saveState()
    c.setFillColor(Color(0, 0, 0, alpha=0.42))
    c.rect(0, H - 320, W, 320, stroke=0, fill=1)
    c.restoreState()
    veil(c, 0, H - 320, W, 250, BLACK, top=0.0, bottom=1.0)
    veil(c, 0, H - 320, W, 320, BLACK, top=0.55, bottom=0.0)

    c.drawImage(P("eagle_white.png"), M, H - 106, 42, 36.8, mask='auto')
    c.drawImage(P("gaz_white.png"), M + 56, H - 108, 38, 42.9, mask='auto')
    ls_text(c, W - M, H - 82, "MERCI DE VOTRE LECTURE", "Inter-M", 8, HexColor("#B9BEC6"), 1.8,
            align="r")

    y = H - 358
    c.setStrokeColor(BLUE)
    c.setLineWidth(2.2)
    c.line(M, y + 78, M + 46, y + 78)
    ls_text(c, M, y, "Merci.", "Inter-B", 46, WHITE, -1.4)
    y = para(c, M, y - 36, cfg["thanks_text"], "Inter-L", 12.4, 19, CW - 150,
             HexColor("#B9BEC6")) - 26

    c.setStrokeColor(HexColor("#23262C"))
    c.setLineWidth(0.8)
    c.line(M, y + 8, W - M, y + 8)
    y -= 14
    ls_text(c, M, y, "CONTACT", "Inter-B", 8, BLUE, 1.6)
    y -= 24
    ls_text(c, M, y, org["contact"]["name"], "Inter-SB", 15, WHITE)
    y -= 17
    ls_text(c, M, y, "%s, %s" % (org["contact"]["role"], org["name"]), "Inter-L", 10, GREY)
    y -= 30
    for row in org["contact_rows"]:
        ls_text(c, M, y, row["label"].upper(), "Inter-M", 7.4, HexColor("#6A7280"), 1.2)
        px = M + 100
        for j, part in enumerate(row["parts"]):
            if j:
                ls_text(c, px, y, "·", "Inter-L", 9.6, HexColor("#5C6470"))
                px += 10
            ls_text(c, px, y, part["text"], "Inter-L", 9.6, HexColor("#DDE0E5"))
            wpx = tw(c, part["text"], "Inter-L", 9.6)
            if part.get("url"):
                link(c, px, y, wpx, 12, part["url"])
            px += wpx + 8
        y -= 18

    qx, qy, qs = W - M - 104, 150, 104
    rrect(c, qx, qy, qs, qs, 8, fill=WHITE)
    qr = QrCodeWidget(org["qr_url"], barLevel="M")
    b = qr.getBounds()
    sz = 78
    d = Drawing(sz, sz, transform=[sz / (b[2] - b[0]), 0, 0, sz / (b[3] - b[1]), 0, 0])
    d.add(qr)
    renderPDF.draw(d, c, qx + (qs - sz) / 2, qy + (qs - sz) / 2)
    ls_text(c, qx + qs / 2, qy - 16, org["qr_label"], "Inter-M", 7.4, GREY, 0.8, align="c")
    link(c, qx, qy, qs, qs, org["qr_url"])

    ls_text(c, M, 118, "Falc'ohm System ASBL  ·  Gazmatek", "Inter-M", 9.6,
            HexColor("#DDE0E5"), 0.4)
    ls_text(c, M, 102, "Événements · Sonorisation · Culture · Festivals", "Inter-L", 8.4,
            HexColor("#6A7280"), 0.6)
    c.setStrokeColor(HexColor("#23262C"))
    c.setLineWidth(0.6)
    c.line(M, 76, W - M, 76)
    ls_text(c, M, 58, "FALC'OHM SYSTEM ASBL — DOSSIER DE PARTENARIAT", "Inter-M", 7,
            HexColor("#5C6470"), 1.2)
    ls_text(c, W - M, 58, "%02d" % ctx.page, "Inter-B", 7, BLUE, 1.2, align="r")
    ctx.no_footer = True
