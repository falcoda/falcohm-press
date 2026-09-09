# -*- coding: utf-8 -*-
"""Pages propres au document de présentation.

Le dossier de partenariat dit ce dont nous avons besoin, le media kit dit à quel public
une marque s'associe. Aucun des deux ne dit ce que nous savons faire pour quelqu'un
d'autre. C'est pourtant la seule chose qui intéresse un lieu, une salle ou une autre
association : ils n'ont ni matériel à donner ni budget de sponsoring, ils ont un endroit
et un projet, et ils se demandent ce qu'on leur apporte.
"""
from reportlab.lib.colors import HexColor

from ..components import *   # noqa
from . import page


@page("pr_capabilities", requires=None)
def capabilities(c, ctx):
    cfg = ctx.cfg
    k = cfg["capabilities"]
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = ctx.head("06", k.get("kicker", "Nos métiers"), k["title"]) - 30
    y = para(c, M, y, k["intro"], "Inter-L", 11.2, 17.4, CW - 40, BODY) - 26
    y = cards(c, y, k["items"], tint=True) - 26

    if k.get("with_us"):
        eyebrow(c, M, y, k.get("with_us_label", "CE QUE ÇA DONNE SUR PLACE"))
        y -= 20
        y = checklist(c, y, k["with_us"]) - 20

    band(c, M, y, CW, k.get("band_icon", "tools"), k["band"]["title"], k["band"]["text"],
         bg=INK, sub=HexColor("#9AA1AC"), accent=BLUE)
