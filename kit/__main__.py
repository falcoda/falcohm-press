# -*- coding: utf-8 -*-
"""CLI.

  python -m kit --list                 dossiers, modules, personas, cibles
  python -m kit bois                   un dossier générique
  python -m kit --all                  tous les dossiers génériques
  python -m kit --target triplaco      PDF + one-pager + e-mail pour une entreprise
  python -m kit --targets              idem pour toutes les cibles
  python -m kit --crm                  état du pipeline, relances dues en tête
  python -m kit --crm-rank             le classement : à qui donner son mois
  python -m kit --crm-validate         refuse toute adresse non sourcée   (tourne en CI)
  python -m kit --crm-brief triplaco   le mémo d'attaque d'une entreprise
"""
import argparse
import sys

# La console Windows est en cp1252 : sans ça, un « é » ou une étoile fait planter l'affichage.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from . import crm as crm_mod  # noqa: E402
from . import events as events_mod
from .build import (build, build_target, list_dossiers, list_modules, list_personas,
                    list_targets, load_data, OUTPUT)


def crm():
    crm_mod.report()


def main():
    ap = argparse.ArgumentParser(prog="kit")
    ap.add_argument("dossier", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--target", metavar="NOM")
    ap.add_argument("--targets", action="store_true")
    ap.add_argument("--crm", action="store_true")
    ap.add_argument("--crm-rank", action="store_true", help="le classement, par score décroissant")
    ap.add_argument("--crm-validate", action="store_true",
                    help="refuse toute adresse e-mail non sourcée")
    ap.add_argument("--crm-brief", metavar="SLUG", help="le mémo d'attaque d'une entreprise")
    ap.add_argument("--crm-sync", action="store_true",
                    help="crée les targets/ manquants depuis les fiches CRM")
    ap.add_argument("--crm-deadlines", action="store_true",
                    help="les dates de dépôt des subsides, triées — rater une date coûte un an")
    ap.add_argument("--crm-plan", action="store_true",
                    help="génère docs/PLAN-DE-CONTACT.md : qui contacter, dans quel ordre")
    ap.add_argument("--tier", metavar="A|B|C", help="restreint --crm-rank à un tier")
    ap.add_argument("--top", type=int, default=25, help="la barre du --crm-rank (défaut : 25)")
    ap.add_argument("--events", action="store_true")
    ap.add_argument("--log", nargs=3, metavar=("SLUG", "TYPE", "RESUME"),
                    help="trace une interaction : --log triplaco mail \"dossier envoyé\"")
    ap.add_argument("--status", metavar="ETAT", help="nouvel état du pipeline (avec --log)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("-o", "--outdir", default=OUTPUT)
    a = ap.parse_args()

    if a.list:
        print("dossiers : %s" % ", ".join(list_dossiers()))
        print("modules  : %s" % ", ".join(list_modules()))
        print("personas : %s" % ", ".join(list_personas()))
        print("cibles   : %s" % ", ".join(list_targets()))
        return 0
    if a.crm_validate:
        return crm_mod.validate()
    if a.crm_sync:
        return crm_mod.sync()
    if a.crm_deadlines:
        return crm_mod.deadlines()
    if a.crm_plan:
        return crm_mod.plan()
    if a.crm_rank:
        return crm_mod.rank(top=a.top, tier=a.tier)
    if a.crm_brief:
        return crm_mod.brief(a.crm_brief)
    if a.log:
        d = crm_mod.log(a.log[0], a.log[1], a.log[2], status=a.status)
        print("✓ %s : %s (score %d)" % (d["company"], d["status"], d["score"]))
        return 0
    if a.events:
        events_mod.report()
        return 0
    if a.crm:
        crm()
        return 0
    if a.targets or a.target:
        for t in (list_targets() if a.targets else [a.target]):
            for f in build_target(t, a.outdir):
                print("✓ %s" % f)
        return 0
    targets = list_dossiers() if a.all else ([a.dossier] if a.dossier else [])
    if not targets:
        ap.error("précise un dossier, --all, --target, --targets, --crm ou --list")
    for t in targets:
        print("✓ %-14s → %s" % (t, build(t, a.outdir)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
