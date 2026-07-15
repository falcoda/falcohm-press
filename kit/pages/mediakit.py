# -*- coding: utf-8 -*-
"""Pages propres au Media Kit. Elles ne demandent jamais d'argent."""
from reportlab.lib.colors import Color, HexColor

from ..components import *   # noqa
from . import page


@page("mk_cover", priority="required")
def cover(c, ctx):
    cfg = ctx.cfg
    img_cover(c, P(cfg["images"]["mk_cover"]), 0, 0, W, H)
    c.saveState()
    c.setFillColor(Color(0, 0, 0, alpha=0.34))
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.restoreState()
    veil(c, 0, 0, W, H * 0.58, BLACK, top=0.0, bottom=0.95)
    veil(c, 0, H * 0.82, W, H * 0.18, BLACK, top=0.7, bottom=0.0)

    c.drawImage(P("gaz_white.png"), M, H - 118, 52, 58.7, mask='auto')
    ls_text(c, W - M, H - 86, "MEDIA KIT · %s" % cfg["year"], "Inter-B", 8.4, WHITE, 2.4,
            align="r")

    by = 200
    c.setStrokeColor(BLUE)
    c.setLineWidth(2.2)
    c.line(M, by + 150, M + 46, by + 150)
    ls_text(c, M, by + 118, "COLLECTIF · SOUND SYSTEM · ÉVÉNEMENTS", "Inter-M", 9,
            HexColor("#9FB4E8"), 2.2)
    ls_text(c, M, by + 58, "Gazmatek", "Inter-B", 58, WHITE, -2.0)
    ls_text(c, M, by + 22, cfg["content"]["baseline"], "Inter-L", 13.4, HexColor("#C9CDD4"))

    c.setStrokeColor(Color(1, 1, 1, alpha=0.22))
    c.setLineWidth(0.7)
    c.line(M, 116, W - M, 116)
    ls_text(c, M, 92, cfg["org"]["sites"][0]["label"], "Inter-M", 9.2, WHITE, 0.6)
    link(c, M, 92, tw(c, cfg["org"]["sites"][0]["label"], "Inter-M", 9.2, 0.6), 11,
         cfg["org"]["sites"][0]["url"])
    ls_text(c, W - M, 92, "Un projet de %s" % cfg["org"]["name"], "Inter-L", 8.6,
            HexColor("#A9AEB6"), 0.4, align="r")
    ctx.no_footer = True


@page("mk_manifesto")
def manifesto(c, ctx):
    cfg = ctx.cfg
    c.setFillColor(BLACK)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.drawImage(P("gaz_white.png"), M, H - 108, 40, 45.1, mask='auto')
    ls_text(c, W - M, H - 84, "MANIFESTE", "Inter-M", 8, HexColor("#B9BEC6"), 1.8, align="r")

    y = H / 2 + 90
    c.setStrokeColor(BLUE)
    c.setLineWidth(2.2)
    c.line(M, y + 46, M + 46, y + 46)
    for i, ln in enumerate(cfg["content"]["manifesto"]):
        f = "Inter-B" if i == 0 else "Inter-L"
        ls_text(c, M, y - i * 40, ln, f, 30, WHITE, -0.8)
    y = y - len(cfg["content"]["manifesto"]) * 40 - 30
    para(c, M, y, cfg["content"]["manifesto_text"], "Inter-L", 11.4, 18, CW - 120,
         HexColor("#9AA1AC"))
    ls_text(c, M, 92, "gazmatek.com", "Inter-M", 8.6, HexColor("#5C6470"), 1.2)
    ctx.no_footer = True


@page("mk_audience", requires=None)
def audience(c, ctx):
    cfg = ctx.cfg
    a = cfg["audience"]
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("01", "Notre public", "À qui parlez-vous\nquand vous parlez avec nous ?") - 30
    y = para(c, M, y, a["intro"], "Inter-L", 11.2, 17.4, CW - 40, BODY) - 26

    gw, gh = (CW - 2 * 10) / 3, 132
    for i, im in enumerate(cfg["images"]["audience"]):
        img_box(c, im, M + i * (gw + 10), y - gh, gw, gh)
    y -= gh + 26

    y = stats_strip(c, y, a["profile"]) - 26
    eyebrow(c, M, y, "OÙ SONT-ILS")
    y -= 20
    y = cards(c, y, a["geo"], tint=True) - 24
    band(c, M, y, CW, "social", a["band"]["title"], a["band"]["text"], bg=INK,
         sub=HexColor("#9AA1AC"), accent=BLUE)


@page("mk_reach")
def reach(c, ctx):
    cfg = ctx.cfg
    r = cfg["reach"]
    c.setFillColor(LIGHT)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("02", "Portée", "Ce que votre marque\ntouche avec nous.") - 30
    y = para(c, M, y, r["intro"], "Inter-L", 11.2, 17.4, CW - 40, BODY) - 26
    y = stats_strip(c, y, r["items"]) - 30

    # histogramme de croissance (vectoriel, pas d'image)
    eyebrow(c, M, y, r["chart"]["title"])
    y -= 22
    ch = 122
    base = y - ch
    rrect(c, M, base, CW, ch + 30, 8, fill=WHITE, stroke=LINE)
    series = r["chart"]["series"]
    vmax = max(s["value"] for s in series) * 1.15
    bw = (CW - 60) / len(series) * 0.52
    step = (CW - 60) / len(series)
    for i, s in enumerate(series):
        bx = M + 30 + i * step + (step - bw) / 2
        bh = (s["value"] / vmax) * (ch - 26)
        last = i == len(series) - 1
        rrect(c, bx, base + 22, bw, bh, 3, fill=BLUE if last else HexColor("#C9D6F7"))
        ls_text(c, bx + bw / 2, base + 8, s["label"], "Inter-M", 7.4, GREY, 0.6, align="c")
        ls_text(c, bx + bw / 2, base + 26 + bh, s["display"], "Inter-B", 8.4,
                BLUE if last else INK, 0.4, align="c")
    y = base - 26

    eyebrow(c, M, y, "CE QUE ÇA VEUT DIRE")
    y -= 20
    y = cards(c, y, r["meaning"]) - 24
    band(c, M, y, CW, "megaphone", r["band"]["title"], r["band"]["text"])


@page("mk_events")
def events(c, ctx):
    cfg = ctx.cfg
    evs = cfg["events"]
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("03", "Nos événements", "Ce que nous avons\ndéjà construit.") - 30
    y = para(c, M, y, cfg["content"]["events_intro"], "Inter-L", 11.2, 17.4, CW - 40, BODY) - 26

    # tableau : année | événement | lieu | jauge
    rh = 26
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    ls_text(c, M, y, "ANNÉE", "Inter-B", 7.4, GREY, 1.2)
    ls_text(c, M + 60, y, "ÉVÉNEMENT", "Inter-B", 7.4, GREY, 1.2)
    ls_text(c, M + 250, y, "LIEU", "Inter-B", 7.4, GREY, 1.2)
    ls_text(c, W - M, y, "FRÉQUENTATION", "Inter-B", 7.4, GREY, 1.2, align="r")
    y -= 8
    c.line(M, y, W - M, y)
    y -= 18
    for i, e in enumerate(evs):
        if i % 2 == 0:
            c.setFillColor(LIGHT)
            c.rect(M - 6, y - 8, CW + 12, rh - 6, stroke=0, fill=1)
        # « TODO » / vide sont des marqueurs internes : à l'écran, un tiret propre.
        cap = str(e.get("capacity") or "").strip()
        cap = "—" if cap in ("", "TODO", "-") else cap
        venue = str(e.get("venue") or "").strip()
        venue = "à venir" if venue in ("", "TODO") else venue
        ls_text(c, M, y, str(e["year"]), "Inter-SB", 9, BLUE)
        ls_text(c, M + 60, y, e["name"], "Inter-SB", 9.4, INK)
        ls_text(c, M + 250, y, venue, "Inter-L", 8.8, GREY)
        ls_text(c, W - M, y, cap, "Inter-M", 9, INK, 0, align="r")
        y -= rh
    y -= 10

    y = band(c, M, y, CW, "star", cfg["content"]["events_band"]["title"],
             cfg["content"]["events_band"]["text"], bg=INK, sub=HexColor("#9AA1AC"),
             accent=BLUE) - 24
    photo_band(c, cfg["images"]["gazmatek_hero"], y, 84,
               "Nos événements, sonorisés par notre propre matériel")


@page("mk_partners")
def partners(c, ctx):
    cfg = ctx.cfg
    c.setFillColor(LIGHT)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("04", "Partenaires", "Ils nous accompagnent.") - 30
    y = para(c, M, y, cfg["content"]["partners_intro"], "Inter-L", 11.2, 17.4, CW - 40,
             BODY) - 30

    cols, rows = 4, 3
    bw = (CW - (cols - 1) * 12) / cols
    bh = 62
    logos = cfg.get("partner_logos", [])
    for r in range(rows):
        for k in range(cols):
            i = r * cols + k
            x = M + k * (bw + 12)
            yy = y - (r + 1) * (bh + 12) + 12
            rrect(c, x, yy, bw, bh, 6, fill=WHITE, stroke=LINE)
            if i < len(logos):
                try:
                    img_fit(c, logos[i], x + 10, yy + 10, bw - 20, bh - 20, WHITE)
                except Exception:
                    pass
            else:
                ls_text(c, x + bw / 2, yy + bh / 2 - 3, "VOTRE LOGO", "Inter-B", 6.4,
                        HexColor("#C6CBD3"), 1.2, align="c")
    y = y - rows * (bh + 12) - 14

    band(c, M, y, CW, "handshake" if False else "link",
         cfg["content"]["partners_band"]["title"], cfg["content"]["partners_band"]["text"])


@page("mk_opportunities")
def opportunities(c, ctx):
    cfg = ctx.cfg
    o = cfg["opportunities"]
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("05", "Collaborer", "Ce que l'on peut\nconstruire ensemble.") - 30
    y = para(c, M, y, o["intro"], "Inter-L", 11.2, 17.4, CW - 40, BODY) - 26
    y = cards(c, y, o["families"], tint=True) - 26

    eyebrow(c, M, y, "NIVEAUX D'ENGAGEMENT")
    y -= 20
    rh = 46
    for i, lv in enumerate(o["levels"]):
        ry = y - (i + 1) * (rh + 8) + 8
        rrect(c, M, ry, CW, rh, 7, fill=WHITE, stroke=LINE)
        c.setFillColor(BLUE if lv.get("highlight") else LIGHT)
        c.roundRect(M + 1, ry + 1, 84, rh - 2, 6, stroke=0, fill=1)
        ls_text(c, M + 43, ry + rh / 2 - 3.4, lv["tier"], "Inter-B", 9,
                WHITE if lv.get("highlight") else INK, 0.8, align="c")
        ls_text(c, M + 100, ry + rh - 18, lv["title"], "Inter-SB", 10, INK)
        ls_text(c, M + 100, ry + 12, lv["text"], "Inter-L", 8.4, GREY)
    y = y - len(o["levels"]) * (rh + 8) - 14
    band(c, M, y, CW, "megaphone", o["band"]["title"], o["band"]["text"], bg=INK,
         sub=HexColor("#9AA1AC"), accent=BLUE)
