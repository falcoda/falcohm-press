# -*- coding: utf-8 -*-
"""Le relevé de consommation boissons, en tableur.

    python -m kit --consumption      écrit output/Consommation-Falcohm-System.csv

Un tableau collé dans un corps d'e-mail est illisible dès qu'il dépasse cinq lignes, et un
service commercial de brasserie veut trier, filtrer et projeter. On lui envoie donc un fichier
qu'il ouvre dans Excel, pas un bloc de texte aligné à la main.

Séparateur point-virgule et BOM UTF-8 : c'est ce qu'Excel attend en configuration francophone.
Avec une virgule, tout atterrit dans la colonne A ; sans BOM, les accents sont illisibles.
"""
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "consumption.yaml")
OUT = os.path.join(ROOT, "output", "Consommation-Falcohm-System.csv")

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def _fr(iso):
    try:
        a, m, j = str(iso).split("-")
        return "%d %s %s" % (int(j), MOIS[int(m) - 1], a)
    except (ValueError, IndexError):
        return str(iso)


def _num(v):
    """Nombre à la française : la virgule décimale, sinon Excel FR lit du texte."""
    if v is None:
        return ""
    if isinstance(v, float):
        return ("%.2f" % v).replace(".", ",")
    return str(v)


def build(out=OUT):
    d = yaml.safe_load(open(SRC, encoding="utf-8")) or {}
    rows = [["Date", "Session", "Personnes", "Fûts pils", "Fûts IPA", "Fûts triple",
             "Total fûts", "Litres", "Litres par personne"]]

    tf = tl = tp = 0
    for e in d.get("events") or []:
        k = e.get("kegs") or {}
        total, litres, pers = e.get("kegs_total"), e.get("litres"), e.get("attendance")
        ratio = round(litres / pers, 2) if (litres and pers) else None
        rows.append([
            _fr(e.get("date")), e.get("label", ""), _num(pers),
            _num(k.get("pils")), _num(k.get("ipa")), _num(k.get("triple")),
            _num(total) or "à retrouver", _num(litres) or "à retrouver", _num(ratio),
        ])
        if total:
            tf += total
            tl += litres or 0
            tp += pers or 0

    t = d.get("totals") or {}
    rows.append([])
    rows.append(["TOTAL RELEVÉ", "", _num(tp), "", "", "", _num(tf), _num(tl),
                 _num(round(tl / tp, 2)) if tp else ""])

    by = d.get("by_year") or {}
    rows.append([])
    rows.append(["Par année", "Dates", "", "", "", "", "Fûts", "Litres", ""])
    for an in sorted(by):
        y = by[an] or {}
        rows.append([an, _num(y.get("dates")), "", "", "", "",
                     _num(y.get("kegs")), _num(y.get("litres")), ""])

    p = d.get("products") or {}
    rows.append([])
    rows.append(["Par produit", "", "", "", "", "", "Fûts", "Litres", "Part du volume"])
    for nom, lab in (("pils", "Pils"), ("ipa", "IPA"), ("triple", "Triple")):
        v = p.get(nom) or {}
        rows.append([lab, "", "", "", "", "", _num(v.get("kegs")), _num(v.get("litres")),
                     "%s %%" % _num(v.get("share_pct"))])

    rows.append([])
    rows.append(["Unité : tous les fûts sont des 30 litres."])
    miss = [e for e in (d.get("events") or []) if not e.get("kegs_total")]
    for e in miss:
        rows.append(["Chiffre manquant : %s, %s personnes. Non estimé volontairement."
                     % (_fr(e.get("date")), _num(e.get("attendance")))])

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        for r in rows:
            f.write(";".join(str(c).replace(";", ",") for c in r) + "\r\n")
    return out


def report():
    p = build()
    print("✓ %s" % p)
    print("  Séparateur point-virgule, BOM UTF-8 : s'ouvre directement dans Excel.")
    return 0
