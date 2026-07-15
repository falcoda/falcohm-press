# -*- coding: utf-8 -*-
"""Base événements : lecture et croisement avec le CRM."""
import glob
import os
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS = os.path.join(ROOT, "events")


def load():
    out = []
    for f in sorted(glob.glob(os.path.join(EVENTS, "*.yaml"))):
        if os.path.basename(f).startswith("_"):
            continue
        d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        d["_file"] = f
        out.append(d)
    return out


def partners_of(event_slug):
    for e in load():
        if e["slug"] == event_slug:
            return (e.get("sponsors") or []) + (e.get("partners") or [])
    return []


def events_of(company_slug):
    """Tous les événements où une entreprise était présente."""
    return [e["name"] for e in load()
            if company_slug in (e.get("sponsors") or []) + (e.get("partners") or [])]


def report():
    evs = load()
    print("%-28s %-8s %-18s %-9s %s" % ("ÉVÉNEMENT", "DATE", "LIEU", "JAUGE", "PARTENAIRES"))
    print("-" * 88)
    for e in evs:
        pr = (e.get("sponsors") or []) + (e.get("partners") or [])
        print("%-28s %-8s %-18s %-9s %s" % (
            e["name"][:28], str(e.get("date", ""))[:7], str(e.get("venue", ""))[:18],
            str(e.get("capacity", "-")), ", ".join(pr) or "-"))
    total = sum(1 for e in evs)
    todo = sum(1 for e in evs if not e.get("attendance"))
    print("\n%d événements · %d fiches à compléter (fréquentation réelle manquante)" % (total, todo))
