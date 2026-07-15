# -*- coding: utf-8 -*-
"""Registre des pages.

Chaque page est une fonction `render(c, ctx)` déclarée via @page("id").
Un dossier (dossiers/*.yaml) n'est qu'une liste d'ids à composer.
"""
import importlib
import pkgutil

REGISTRY = {}
META = {}


def page(pid, priority="optional", audience=("all",), requires=None):
    """`requires` : clé que le module doit fournir. Si elle manque, la page est
    silencieusement ignorée (un persona peut donc demander une page que le module
    ne remplit pas)."""
    def deco(fn):
        REGISTRY[pid] = fn
        META[pid] = {"id": pid, "priority": priority, "audience": list(audience),
                     "requires": requires}
        return fn
    return deco


def requires(pid):
    load_all()
    return META.get(pid, {}).get("requires")


def load_all():
    for m in pkgutil.iter_modules(__path__):
        if not m.name.startswith("_"):
            importlib.import_module("%s.%s" % (__name__, m.name))
    return REGISTRY


def get(pid):
    load_all()
    if pid not in REGISTRY:
        raise SystemExit("Page inconnue : %s (disponibles : %s)"
                         % (pid, ", ".join(sorted(REGISTRY))))
    return REGISTRY[pid]
