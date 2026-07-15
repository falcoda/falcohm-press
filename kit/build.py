# -*- coding: utf-8 -*-
"""Composition : data + module + persona + target -> PDF, one-pager, e-mail."""
import copy
import datetime
import glob
import os
import re
import yaml
from reportlab.pdfgen import canvas

from .core import W, H, M, footer, kicker, title
from . import pages

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
MODULES = os.path.join(ROOT, "modules")
PERSONAS = os.path.join(ROOT, "personas")
TARGETS = os.path.join(ROOT, "targets")
DOSSIERS = os.path.join(ROOT, "dossiers")
EMAILS = os.path.join(ROOT, "emails")
OUTPUT = os.path.join(ROOT, "output")


def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def _yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_data():
    cfg = {}
    for f in sorted(glob.glob(os.path.join(DATA, "*.yaml"))):
        cfg = deep_merge(cfg, _yaml(f))
    return cfg


def _names(folder):
    return sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(folder, "*.yaml")))


def list_modules():
    return _names(MODULES)


def list_dossiers():
    return _names(DOSSIERS)


def list_targets():
    return _names(TARGETS)


def list_personas():
    return _names(PERSONAS)


class Ctx(object):
    def __init__(self, c, cfg, module, target=None, persona=None):
        self.c = c
        self.cfg = cfg
        self.module = module
        self.target = target or {}
        self.persona = persona or {}
        self.page = 1
        self.no_footer = False

    def head(self, num, label, ttl, size=28):
        y = H - 86
        kicker(self.c, M, y, num, label)
        return title(self.c, M, y - 34, ttl, size)


def _render(page_ids, cfg, module, out, target=None, persona=None, subject=""):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle("Dossier de partenariat — %s" % module.get("label", ""))
    c.setAuthor("%s — %s" % (cfg["org"]["contact"]["name"], cfg["org"]["name"]))
    c.setSubject(subject or module.get("subject", ""))
    ctx = Ctx(c, cfg, module, target, persona)
    pages.load_all()
    page_ids = [p for p in page_ids
                if not pages.requires(p) or module.get(pages.requires(p))]
    for pid in page_ids:
        ctx.no_footer = False
        pages.get(pid)(c, ctx)
        if not ctx.no_footer:
            footer(c, ctx.page)
        c.showPage()
        ctx.page += 1
    c.save()
    return out


def build(dossier_name, outdir=OUTPUT):
    """Génère un dossier générique (dossiers/<nom>.yaml)."""
    spec = _yaml(os.path.join(DOSSIERS, "%s.yaml" % dossier_name))
    module = _yaml(os.path.join(MODULES, "%s.yaml" % spec["module"]))
    cfg = deep_merge(load_data(), spec.get("overrides", {}))
    cfg = deep_merge(cfg, module.pop("overrides", {}))
    page_ids = spec.get("pages") or module.get("pages")
    out = os.path.join(outdir, spec.get("filename", "Dossier-%s.pdf" % dossier_name))
    return _render(page_ids, cfg, module, out)


def _slug(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")


def build_target(target_name, outdir=OUTPUT, with_onepager=True, with_email=True):
    """Génère TOUT pour une entreprise : dossier, one-pager, e-mail personnalisé."""
    tgt = _yaml(os.path.join(TARGETS, "%s.yaml" % target_name))
    persona = _yaml(os.path.join(PERSONAS, "%s.yaml" % tgt["persona"]))
    module = _yaml(os.path.join(MODULES, "%s.yaml" % tgt["module"]))

    cfg = load_data()
    cfg = deep_merge(cfg, module.pop("overrides", {}))
    cfg = deep_merge(cfg, persona.get("overrides", {}))
    cfg = deep_merge(cfg, tgt.get("overrides", {}))

    # priorité : target > persona > module
    page_ids = tgt.get("pages") or persona.get("pages") or module.get("pages")

    company = tgt["company"]
    slug = _slug(company)
    folder = os.path.join(outdir, slug)
    year = cfg["year"]
    made = []

    out = os.path.join(folder, "%s-Partnership-%s.pdf" % (slug, year))
    made.append(_render(page_ids, cfg, module, out, tgt, persona,
                        subject="Partenariat %s — %s" % (module.get("label", ""), company)))

    if with_onepager and "onepager" in pages.load_all():
        one = os.path.join(folder, "%s-OnePager-%s.pdf" % (slug, year))
        made.append(_render(["onepager"], cfg, module, one, tgt, persona))

    if with_email:
        made.append(_write_email(tgt, persona, module, cfg, folder))

    _crm_documents(company, made)
    return made


def _crm_documents(company, made):
    """Enregistre les documents produits dans la fiche CRM de l'entreprise."""
    try:
        from . import crm
        for d in crm.load():
            if d.get("company") == company:
                docs = d.setdefault("documents", [])
                for f in made:
                    rel = os.path.relpath(f, ROOT)
                    if rel not in docs:
                        docs.append(rel)
                d["score"] = crm.score(d)
                crm.save(d)
                return
    except Exception:
        pass


def _recipient(company):
    """Le bandeau d'envoi : à QUI, à quelle adresse, et comment on le sait.

    Un e-mail sans destinataire est un e-mail qu'on n'enverra pas. Autant que le fichier
    le dise en haut, plutôt que de le découvrir au moment de cliquer sur « envoyer ».
    """
    try:
        from . import crm
        d = next((x for x in crm.load() if x.get("company") == company), None)
    except Exception:                                          # noqa: BLE001
        d = None
    if not d:
        return ""

    cs = [c for c in (d.get("contacts") or []) if c.get("email")]
    named = [c for c in cs if str(c.get("name") or "").strip()]
    service = [c for c in cs if c.get("email_status") == "verified_public"]
    best = (named or service or cs)

    L = ["<!-- ENVOI — généré depuis crm/companies/%s.yaml. Relire avant d'expédier. -->\n\n"
         % d["_name"]]

    pr = d.get("prior_relationship")
    if pr:
        L.append("> ### Nous nous connaissons déjà.\n> **%s**\n" % str(pr.get("what") or "").strip())
        if pr.get("source_url"):
            L.append("> Preuve : %s\n" % pr["source_url"])
        L.append("> \n> Ouvre l'e-mail là-dessus. Ne te présente pas comme un inconnu.\n\n")

    if not best:
        L.append("> ### ⚠ Aucune adresse publique — ne pas envoyer par e-mail\n")
        for ch in d.get("inbound_channels") or []:
            L.append("> **%s** : %s\n" % (ch.get("type", "canal"), ch.get("url")))
        if not d.get("inbound_channels"):
            L.append("> Aucun canal connu. Trouver un contact avant toute chose.\n")
    else:
        to = best[0]
        L.append("> **À :** `%s`\n" % to["email"])
        who = " — ".join(x for x in (to.get("name"), to.get("role")) if str(x or "").strip())
        L.append("> **Personne :** %s\n" % (who or "*aucun nom identifié*"))
        L.append("> **Source de l'adresse :** %s (lue le %s)\n"
                 % (to.get("source_url") or "?", to.get("retrieved_on") or "?"))
        cc = [c["email"] for c in cs if c["email"] != to["email"]]
        if cc:
            L.append("> **En copie :** %s\n" % ", ".join("`%s`" % x for x in cc))
        if not str(to.get("name") or "").strip():
            L.append("> \n> ⚠ **Adresse non nominative.** « Jamais d'envoi à une adresse "
                     "générique » (CLAUDE.md). Un coup de fil pour obtenir un nom vaut mieux "
                     "qu'un dossier parfait envoyé dans le vide.\n")

    for x in sorted(d.get("deadlines") or [], key=lambda y: str(y.get("date"))):
        L.append("> \n> **Échéance : %s** — %s\n"
                 % (x.get("date"), str(x.get("what") or "").split(".")[0]))
    L.append("\n---\n\n")
    return "".join(L)


def _write_email(tgt, persona, module, cfg, folder):
    tpl_name = persona.get("email", "technique")
    tpl_path = os.path.join(EMAILS, "%s.md" % tpl_name)
    tpl = open(tpl_path, encoding="utf-8").read() if os.path.exists(tpl_path) else ""
    contact = tgt.get("contact") or {}
    repl = {
        "{{COMPANY}}": tgt["company"],
        "{{CONTACT_NAME}}": contact.get("name") or "Madame, Monsieur",
        "{{CONTACT_EMAIL}}": contact.get("email") or "",
        "{{CONTACT_ROLE}}": contact.get("role") or "",
        "{{MODULE}}": module.get("label", ""),
        "{{OBJECTIVE}}": persona.get("objective", ""),
        "{{SENDER}}": cfg["org"]["contact"]["name"],
        "{{SENDER_ROLE}}": cfg["org"]["contact"]["role"],
        "{{ORG}}": cfg["org"]["name"],
        "{{EMAIL}}": cfg["org"]["contact"]["email"],
        "{{SITES}}": " · ".join(s["label"] for s in cfg["org"]["sites"]),
        "{{FOLLOWERS}}": cfg["followers"],
        "{{DATE}}": datetime.date.today().isoformat(),
    }
    for k, v in repl.items():
        tpl = tpl.replace(k, str(v))
    tpl = _recipient(tgt["company"]) + tpl
    os.makedirs(folder, exist_ok=True)
    out = os.path.join(folder, "email.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(tpl)
    return out
