# -*- coding: utf-8 -*-
"""CRM : lecture, scoring, validation, pipeline, relances. Un fichier YAML par entreprise.

    python -m kit --crm               le pipeline, relances dues en tête
    python -m kit --crm-rank          le classement : à qui donner son mois
    python -m kit --crm-validate      refuse toute adresse non sourcée     (tourne en CI)
    python -m kit --crm-brief <slug>  le mémo d'attaque d'une entreprise
    python -m kit --log <slug> ...    trace une interaction

Le score ne se saisit pas, il se calcule :

    score = business_fit × partnership_probability × impact_if_successful / 10     (0-100)

On multiplie, on n'additionne pas. Un produit parfait qu'ils refuseront ne vaut rien ;
un oui certain sans effet non plus. Une somme pondérée masquerait exactement ce qu'on
cherche à voir : le zéro sur un axe doit tuer la ligne, et il la tue.

Tant qu'une fiche n'a pas ses trois notes, on retombe sur le score structurel d'origine.
La migration se fait fiche par fiche, rien ne casse en attendant.
"""
import datetime
import glob
import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRM = os.path.join(ROOT, "crm")
COMPANIES = os.path.join(CRM, "companies")
MODULES = os.path.join(ROOT, "modules")
PERSONAS = os.path.join(ROOT, "personas")

PIPELINE = ["lead", "qualified", "researched", "sent", "followup_1", "followup_2",
            "replied", "meeting", "proposal", "negotiation", "won", "active", "renewal",
            "lost", "discarded"]

# jours avant relance, par état
DUE = {"sent": 10, "followup_1": 20, "followup_2": 30, "replied": 3, "meeting": 5,
       "proposal": 7, "negotiation": 7}

EMAIL_STATUSES = ["verified_public", "generic", "none"]
ASK_TYPES = ["financial", "material", "discount", "loan", "consumables", "visibility", "services"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
# La PEC italienne : une boîte de recommandé légal. Toute société italienne la publie, et tout
# agent de recherche la ramasse. Y prospecter, c'est envoyer un courrier d'huissier.
PEC_RE = re.compile(r"@(?:.+\.)?pec\.|@pec\.|@.*\.pec$", re.I)
STALE_DAYS = 365


# ─────────────────────────────────────────────────────────────────────  lecture

def load():
    out = []
    for f in sorted(glob.glob(os.path.join(COMPANIES, "*.yaml"))):
        if os.path.basename(f).startswith("_"):
            continue
        d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        d["_file"] = f
        d["_name"] = os.path.basename(f)[:-5]
        out.append(d)
    return out


def save(d):
    f, n = d.pop("_file"), d.pop("_name", None)
    yaml.safe_dump(d, open(f, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
    d["_file"] = f
    if n:
        d["_name"] = n


def _yaml(path):
    if not os.path.exists(path):
        return {}
    return yaml.safe_load(open(path, encoding="utf-8")) or {}


def categories():
    return {c["id"]: c for c in _yaml(os.path.join(CRM, "categories.yaml")).get("categories", [])}


def suppression():
    """Les adresses et les entreprises à qui on ne parle plus. RGPD, art. 21."""
    rows = _yaml(os.path.join(CRM, "suppression.yaml")).get("suppressed") or []
    return ({r["email"].strip().lower() for r in rows if r.get("email")},
            {r["company"].strip().lower() for r in rows if r.get("company")})


def _known(folder):
    return {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(folder, "*.yaml"))}


# ─────────────────────────────────────────────────────────────────────  score

def _structural(d):
    """L'ancien score : ce qu'on SAIT d'une entreprise. Repli tant qu'elle n'est pas notée."""
    s = 0
    if d.get("sector"):
        s += 30
    tags = d.get("tags") or []
    if "deja-sponsor" in tags:
        s += 20
    contacts = [c for c in (d.get("contacts") or []) if c.get("name") and c.get("email")]
    if contacts:
        s += 20
    elif any(c.get("name") for c in (d.get("contacts") or [])):
        s += 8
    if "belge" in tags:
        s += 15
    if "pme" in tags:
        s += 10
    elif "gros-compte" in tags:
        s += 4
    if "contact-chaud" in tags:
        s += 5
    return min(s, 100)


def notes(d):
    """Les trois notes, ou None si la fiche n'est pas encore évaluée."""
    s = d.get("scoring") or {}
    v = [s.get("business_fit"), s.get("partnership_probability"), s.get("impact_if_successful")]
    if all(isinstance(x, int) and 0 <= x <= 10 for x in v):
        return v
    return None


def score(d):
    """0-100. Ce qu'on peut ATTENDRE d'une entreprise — pas ce qu'on sait d'elle."""
    v = notes(d)
    if v is None:
        return _structural(d)
    fit, prob, imp = v
    return int(round(fit * prob * imp / 10.0))


def stars(s):
    for threshold, n in ((60, 5), (40, 4), (25, 3), (12, 2)):
        if s >= threshold:
            return n
    return 1


def temperature(s):
    return "chaud" if s >= 70 else ("tiède" if s >= 40 else "froid")


def reachability(d):
    """Comment on les joint, en un mot. `info@` ne répond jamais (CLAUDE.md).

    Entre la personne nommée et le fourre-tout, il y a l'adresse de SERVICE : un
    `sales@` explicitement dédié aux partenariats de long terme n'est pas un `info@`.
    """
    cs = d.get("contacts") or []
    if any(c.get("email") and str(c.get("name") or "").strip() for c in cs):
        return "nominatif"
    if any(c.get("email") and c.get("email_status") == "verified_public" for c in cs):
        return "service"
    if any(c.get("email") for c in cs):
        return "générique"
    if d.get("inbound_channels"):
        return "formulaire"
    return "AUCUN"


# ─────────────────────────────────────────────────────────────────────  historique

def last_interaction(d):
    ints = d.get("interactions") or []
    if not ints:
        return None
    return max(str(i.get("date", "")) for i in ints)


def due_date(d):
    days = DUE.get(d.get("status"))
    last = last_interaction(d)
    if not days or not last:
        return None
    try:
        return (datetime.date.fromisoformat(str(last))
                + datetime.timedelta(days=days)).isoformat()
    except ValueError:
        return None


def log(slug, kind, summary, status=None, document=None):
    """Ajoute une interaction datée et fait avancer le pipeline."""
    for d in load():
        if d.get("slug") == slug:
            d.setdefault("interactions", []).append({
                "date": datetime.date.today().isoformat(),
                "type": kind, "resume": summary})
            if document:
                d.setdefault("documents", []).append(document)
            if status:
                if status not in PIPELINE:
                    raise SystemExit("État inconnu : %s — attendu : %s"
                                     % (status, " | ".join(PIPELINE)))
                d["status"] = status
            d["score"] = score(d)
            save(d)
            return d
    raise SystemExit("Entreprise inconnue dans le CRM : %s" % slug)


# ─────────────────────────────────────────────────────────────────────  validation

def _as_date(v):
    if isinstance(v, datetime.date):
        return v
    if isinstance(v, str) and v.strip():
        try:
            return datetime.date.fromisoformat(v.strip()[:10])
        except ValueError:
            return None
    return None


def _domain(url):
    m = re.search(r"https?://([^/]+)", str(url or ""), re.I)
    return re.sub(r"^www\.", "", (m.group(1) if m else "").lower())


def check(d, cats, modules, personas, sup_mail, sup_name):
    """(erreurs, avertissements). Une erreur fait échouer la CI. Un avertissement, non."""
    errs, warns = [], []
    name = d["_name"]
    e = lambda m: errs.append("%s: %s" % (name, m))          # noqa: E731
    w = lambda m: warns.append("%s: %s" % (name, m))         # noqa: E731

    if d.get("slug") != name:
        e("`slug: %s` ne correspond pas au nom du fichier (%s.yaml)" % (d.get("slug"), name))
    for k in ("company", "persona", "status", "website"):
        if not d.get(k):
            e("champ obligatoire manquant : `%s`" % k)

    if d.get("status") not in PIPELINE:
        e("`status: %s` inconnu — attendu : %s" % (d.get("status"), " | ".join(PIPELINE)))
    if (d.get("company") or "").strip().lower() in sup_name:
        e("entreprise en liste d'opposition (crm/suppression.yaml) — ne plus la contacter")

    sector = d.get("sector")
    if not sector:
        w("pas de `sector` : cette fiche ne peut pas encore produire de PDF")
    elif sector not in modules:
        e("`sector: %s` introuvable dans modules/ — %s" % (sector, ", ".join(sorted(modules))))
    if d.get("persona") and d["persona"] not in personas:
        e("`persona: %s` introuvable dans personas/" % d["persona"])
    for c in d.get("categories") or []:
        if c not in cats:
            e("catégorie inconnue : `%s` (voir crm/categories.yaml)" % c)

    # Les trois notes. Facultatives — mais si elles sont là, elles sont complètes et justifiées.
    s = d.get("scoring") or {}
    if s:
        for k in ("business_fit", "partnership_probability", "impact_if_successful"):
            v = s.get(k)
            if not isinstance(v, int) or not 0 <= v <= 10:
                e("`scoring.%s` doit être un entier de 0 à 10 (reçu : %r)" % (k, v))
        if not str(s.get("rationale") or "").strip():
            e("`scoring.rationale` est obligatoire — trois chiffres sans justification ne valent rien")
        if isinstance(s.get("business_fit"), int) and s["business_fit"] < 4:
            w("business_fit %d/10 : à écarter (`status: discarded`) plutôt qu'à travailler"
              % s["business_fit"])
    elif d.get("status") not in ("lead", "discarded"):
        w("pas de `scoring` : la fiche avance dans le pipeline sans avoir été évaluée")

    ask = d.get("ask") or {}
    for t in ask.get("type") or []:
        if t not in ASK_TYPES:
            e("`ask.type: %s` inconnu — attendu : %s" % (t, " | ".join(ASK_TYPES)))

    if d.get("knowledge") and not os.path.exists(os.path.join(ROOT, str(d["knowledge"]))):
        w("`knowledge: %s` n'existe pas" % d["knowledge"])
    if not d.get("sponsorship_history") and d.get("scoring"):
        w("`sponsorship_history` vide : ce qu'ils sponsorisent déjà est le meilleur prédicteur "
          "d'un oui. Cherche avant de conclure qu'il n'y a rien.")

    # ── Le cœur. Une adresse se prouve, ou elle ne s'écrit pas.
    site = _domain(d.get("website"))
    cs = d.get("contacts") or []
    for i, c in enumerate(cs):
        tag = "contacts[%d] (%s)" % (i, c.get("name") or c.get("email") or "?")
        mail = str(c.get("email") or "").strip()
        st = c.get("email_status")

        if st is not None and st not in EMAIL_STATUSES:
            e("%s : `email_status: %r` — attendu : %s. Une adresse devinée ne rentre pas "
              "dans cette base." % (tag, st, " | ".join(EMAIL_STATUSES)))
        if mail:
            if not EMAIL_RE.match(mail):
                e("%s : `%s` n'est pas une adresse valide" % (tag, mail))
            if mail.lower() in sup_mail:
                e("%s : adresse en liste d'opposition (crm/suppression.yaml)" % tag)
            if PEC_RE.search(mail):
                e("%s : `%s` est une adresse PEC (recommandé légal italien). Elle est réelle et "
                  "elle est inutilisable : y prospecter, c'est envoyer un courrier d'huissier. "
                  "Sors-la de `contacts` et passe par `inbound_channels`." % (tag, mail))
            if st == "none":
                e("%s : un e-mail est renseigné mais `email_status: none`" % tag)
            for k in ("source_url", "retrieved_on", "evidence"):
                if not c.get(k):
                    e("%s : e-mail sans `%s`. Une adresse se prouve ou ne s'écrit pas." % (tag, k))
            if c.get("source_url") and not str(c["source_url"]).startswith("http"):
                e("%s : `source_url` doit être une URL" % tag)
            host = mail.split("@")[-1].lower()
            if site and host != site and not host.endswith("." + site) \
                    and not site.endswith("." + host):
                w("%s : adresse en @%s alors que le site est %s. Vérifie — c'est la signature "
                  "d'une adresse extrapolée." % (tag, host, site))
        elif st in ("verified_public", "generic"):
            e("%s : `email_status: %s` sans e-mail" % (tag, st))

        got = _as_date(c.get("retrieved_on"))
        if c.get("retrieved_on") and not got:
            e("%s : `retrieved_on` doit être une date ISO (2026-07-14)" % tag)
        elif got and (datetime.date.today() - got).days > STALE_DAYS:
            w("%s : information vieille de plus d'un an — revérifier avant d'écrire" % tag)

    if not cs and not d.get("inbound_channels"):
        e("ni contact, ni `inbound_channels` : on ne sait pas comment les joindre")
    if cs and not any(str(c.get("name") or "").strip() for c in cs):
        w("aucun contact nommé. « L'adresse info@ ne répond jamais » (STRATEGIE.md)")

    for i, src in enumerate(d.get("sources") or []):
        if not str(src.get("url", "")).startswith("http"):
            e("sources[%d] : URL manquante ou invalide" % i)
    if d.get("scoring") and not d.get("sources"):
        w("aucune `sources` : la fiche est notée mais rien ne l'étaye")

    return errs, warns


def validate():
    cats, mods, pers = categories(), _known(MODULES), _known(PERSONAS)
    sup_mail, sup_name = suppression()
    rows = load()
    errs, warns = [], []
    for d in rows:
        a, b = check(d, cats, mods, pers, sup_mail, sup_name)
        errs += a
        warns += b

    # Les doublons. Deux fiches pour une même entreprise, c'est deux e-mails au même
    # interlocuteur — et le partenariat est mort avant d'avoir commencé.
    seen = {}
    for d in rows:
        for n in [d.get("company")] + (d.get("aka") or []):
            k = re.sub(r"[^a-z0-9]", "", str(n).lower())
            if k and seen.get(k, d["_name"]) != d["_name"]:
                errs.append("%s : doublon probable avec %s (« %s »)" % (d["_name"], seen[k], n))
            elif k:
                seen[k] = d["_name"]

    # Le nom peut varier (« FWB » vs « FWB — Service de la Musique ») ; le domaine, non.
    by_host = {}
    for d in rows:
        host = _domain(d.get("website"))
        if not host:
            continue
        by_host.setdefault(host, []).append(d["_name"])
    for host, names in by_host.items():
        if len(names) > 1:
            warns.append("%s : même site (%s) — une seule entreprise, %d fiches. Fusionne, "
                         "ou distingue-les par `aka`." % (", ".join(names), host, len(names)))

    for m in warns:
        print("  ! %s" % m)
    for m in errs:
        print("  X %s" % m)
    if errs:
        print("\n%d fiche(s) · %d erreur(s) · %d avertissement(s). Rien n'est envoyable en l'état."
              % (len(rows), len(errs), len(warns)))
        return 1
    print("\n%d fiche(s) · 0 erreur · %d avertissement(s). Toute adresse est sourcée."
          % (len(rows), len(warns)))
    return 0


# ─────────────────────────────────────────────────────────────────────  classement

def rank(top=25, tier=None):
    cats = categories()
    rows = []
    for d in load():
        if d.get("status") in ("discarded", "lost"):
            continue
        cs = d.get("categories") or ([d["sector"]] if d.get("sector") else [])
        if tier and not any(cats.get(c, {}).get("tier") == tier for c in cs):
            continue
        v = notes(d) or [0, 0, 0]
        rows.append((score(d), d, cs, v))
    rows.sort(key=lambda r: (-r[0], -((r[1].get("ask") or {}).get("realistic_value_eur") or 0),
                             r[1].get("company", "")))

    print("%-5s %-6s %-27s %-3s %-16s %-9s %-11s %-11s %s"
          % ("SCORE", "", "ENTREPRISE", "", "CATÉGORIE", "VALEUR", "JOIGNABLE", "ÉTAT", "F/P/I"))
    print("-" * 110)
    for i, (s, d, cs, v) in enumerate(rows):
        if top and i == top:
            print("-" * 110)
            print("  ↑ les %d cibles qui méritent ton temps.   ↓ le reste : plus tard, ou jamais."
                  % top)
            print("-" * 110)
        eur = (d.get("ask") or {}).get("realistic_value_eur")
        print("%-5d %-6s %-27.27s %-3s %-16.16s %8s %-11s %-11s %s"
              % (s, "*" * stars(s), d.get("company", ""), d.get("country", ""),
                 (cs[0] if cs else "-"), ("%s€" % eur) if eur else "-", reachability(d),
                 d.get("status", ""), ("%d/%d/%d" % tuple(v)) if notes(d) else "non évaluée"))
    if not rows:
        print("(aucune fiche)")
        return 0

    unrated = [d for _, d, _, _ in rows if notes(d) is None]
    if unrated:
        print("\n%d fiche(s) sans les trois notes — score structurel de repli, à évaluer : %s"
              % (len(unrated), ", ".join(d["_name"] for d in unrated[:8])))
    return 0


def report():
    """Le pipeline. Inchangé, mais trié par le nouveau score."""
    rows = load()
    for d in rows:
        d["score"] = score(d)
    rows.sort(key=lambda d: (-d["score"],
                             PIPELINE.index(d.get("status", "lead"))
                             if d.get("status") in PIPELINE else 99))
    today = datetime.date.today().isoformat()
    print("%-28s %-14s %-12s %-6s %-7s %s" % ("ENTREPRISE", "SECTEUR", "ÉTAT", "SCORE",
                                              "TEMP.", "RELANCE"))
    print("-" * 88)
    for d in rows:
        due = due_date(d) or "-"
        flag = " ⚠" if due != "-" and due <= today else ""
        print("%-28s %-14s %-12s %-6d %-7s %s%s" % (
            d.get("company", "")[:28], d.get("sector", ""), d.get("status", ""),
            d["score"], temperature(d["score"]), due, flag))
    print()
    by = {}
    for d in rows:
        by[d.get("status", "?")] = by.get(d.get("status", "?"), 0) + 1
    print("Pipeline : " + " · ".join("%s %d" % (k, v) for k, v in by.items()))
    late = [d for d in rows if (due_date(d) or "9") <= today]
    if late:
        print("À relancer aujourd'hui : " + ", ".join(d["company"] for d in late))


# ─────────────────────────────────────────────────────────────────────  mémo

def export_partners():
    """Régénère data/partners.yaml comme une VUE du CRM, pas une source concurrente.

    Le repo avait deux vérités pour une même chose : data/partners.yaml (18 lignes, l'ancien
    format plat) et crm/companies/ (les fiches). Un contact mis à jour dans l'un ne l'était pas
    dans l'autre. On garde le fichier — d'autres outils peuvent le lire — mais il DÉCOULE des
    fiches, il ne les contredit plus.
    """
    rows = []
    for d in sorted(load(), key=lambda x: -score(x)):
        if d.get("status") == "discarded":
            continue
        cs = [c for c in (d.get("contacts") or []) if c.get("email")]
        named = next((c for c in cs if str(c.get("name") or "").strip()), None)
        best = named or (cs[0] if cs else {})
        pipe = d.get("pipeline") or {}
        rows.append({
            "company": d.get("company", ""),
            "module": d.get("sector", ""),
            "status": d.get("status", "lead"),
            "score": score(d),
            "contact": best.get("name") or "",
            "email": best.get("email") or "",
            "sent": pipe.get("sent") or (d.get("interactions") or [{}])[0].get("date", "")
            if d.get("status") in ("sent", "followup_1", "followup_2") else "",
            "followup": pipe.get("followup") or "",
        })
    out = os.path.join(ROOT, "data", "partners.yaml")
    with open(out, "w", encoding="utf-8") as f:
        f.write("# VUE générée depuis crm/companies/ par `python -m kit --crm-sync`.\n"
                "# Ne pas éditer à la main : la vérité est dans les fiches. Triée par score.\n"
                "# Statuts : lead | contacted | replied | negotiating | won | lost.\n")
        yaml.safe_dump({"partners": rows}, f, allow_unicode=True, sort_keys=False, width=200)
    return len(rows)


def deadlines(days=None):
    """Les dates de dépôt, triées. Rater une date de subside coûte un an : c'est la seule
    donnée du CRM qu'on ne peut pas rattraper le lendemain."""
    rows = deadlines_data(days)

    if not rows:
        print("Aucune échéance à venir.")
        return 0
    print("%-12s %-6s %-30s %s" % ("DATE", "J-", "ORGANISME", "DÉPÔT"))
    print("-" * 108)
    for when, left, d, x in rows:
        flag = "⚠ " if left <= 60 else "  "
        print("%s%-10s %-6s %-30.30s %.55s"
              % (flag, when.isoformat(), "J-%d" % left, d.get("company", ""),
                 str(x.get("what") or "").replace("\n", " ")))
    urgent = [r for r in rows if r[1] <= 60]
    print("\n%d échéance(s). %d dans les 60 jours." % (len(rows), len(urgent)))
    if urgent:
        print("Prochaine : %s — %s (J-%d)"
              % (urgent[0][0].isoformat(), urgent[0][2].get("company"), urgent[0][1]))
    return 0


def sync(force=False):
    """La fiche devient une cible. Le CRM alimente la chaîne de production, il ne la double pas.

    On n'écrase jamais un `targets/*.yaml` existant : il peut avoir été réglé à la main
    (une photo de couverture, une page en plus). On crée ce qui manque, c'est tout.
    """
    seen = {}
    for path in glob.glob(os.path.join(ROOT, "targets", "*.yaml")):
        t = _yaml(path)
        seen[str(t.get("company") or "").strip().lower()] = os.path.basename(path)[:-5]

    created, skipped = [], []
    for d in load():
        name, slug = str(d.get("company") or "").strip(), d["_name"]
        if d.get("status") in ("discarded", "lost") or not d.get("sector") or not d.get("persona"):
            skipped.append(slug)
            continue
        if name.lower() in seen:
            continue                                   # déjà une cible, sous un autre nom de fichier
        path = os.path.join(ROOT, "targets", "%s.yaml" % slug)
        if os.path.exists(path) and not force:
            continue

        cs = d.get("contacts") or []
        best = (next((c for c in cs if c.get("email") and str(c.get("name") or "").strip()), None)
                or next((c for c in cs if c.get("email_status") == "verified_public"), None)
                or next((c for c in cs if c.get("email")), None) or {})
        tgt = {
            "company": name,
            "persona": d["persona"],
            "module": d["sector"],
            "phase": d.get("phase", 1),
            "contact": {"name": best.get("name") or "",
                        "role": best.get("role") or "",
                        "email": best.get("email") or ""},
            "website": d.get("website") or "",
            "notes": "%s\nFiche CRM : crm/companies/%s.yaml\n"
                     % (str(d.get("why_us") or "").strip(), slug),
        }
        # Un nom d'organisme public (> 34 car.) déborde le bandeau du one-pager. On lui donne
        # un nom d'affichage court : `display_name` explicite, sinon le premier alias, sinon
        # le nom coupé au tiret. Le nom légal complet reste dans `company`.
        short = d.get("display_name") or (d.get("aka") or [None])[0]
        if len(name) > 34:
            tgt["display_name"] = short or name.split("—")[0].split("(")[0].strip()
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(tgt, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        created.append(slug)

    for x in created:
        print("  + targets/%s.yaml" % x)
    n = export_partners()
    print("\n%d cible(s) créée(s), %d ignorée(s) (écartées, ou sans module/persona)."
          % (len(created), len(skipped)))
    print("data/partners.yaml régénéré depuis le CRM : %d ligne(s)." % n)
    if skipped:
        print("Sans module : %s" % ", ".join(skipped[:10]))
    return 0


def plan():
    """Le plan de contact : qui, dans quel ordre, à quelle adresse, avec quel argument.
    Généré depuis les fiches — se régénère à chaque évolution du CRM."""
    cats = categories()
    rows = [d for d in load() if d.get("status") not in ("discarded", "lost")]
    for d in rows:
        d["_score"] = score(d)
    rows.sort(key=lambda d: (-d["_score"], -((d.get("ask") or {}).get("realistic_value_eur") or 0)))

    def contact_line(d):
        cs = [c for c in (d.get("contacts") or []) if c.get("email")]
        named = next((c for c in cs if str(c.get("name") or "").strip()), None)
        service = next((c for c in cs if c.get("email_status") == "verified_public"), None)
        c = named or service or (cs[0] if cs else None)
        if c:
            who = c.get("name") or "*(pas de nom)*"
            tag = "" if str(c.get("name") or "").strip() else " ⚠ générique — trouver un nom"
            return "`%s`%s<br><sub>%s</sub>" % (c["email"], tag, who)
        ch = (d.get("inbound_channels") or [{}])[0]
        return "*%s* : %s" % (ch.get("type", "aucun canal"), ch.get("url", "—")) if ch.get("url") \
            else "**aucun contact — à chercher**"

    L = ["# Plan de contact — qui, quand, comment\n\n",
         "> Généré par `python -m kit --crm-plan` depuis les fiches CRM. Ne pas éditer à la main.\n",
         "> Le score = adéquation × probabilité × impact ⁄ 10. La barre est à 25.\n\n"]

    urgent = deadlines_data(60)
    if urgent:
        L.append("## ⏰ À ne pas rater — échéances sous 60 jours\n\n")
        L.append("| Date | J- | Organisme | Dépôt |\n|---|---|---|---|\n")
        for when, left, d, x in urgent:
            L.append("| **%s** | J-%d | %s | %.60s |\n"
                     % (when.isoformat(), left, d.get("display_name") or d.get("company"),
                        str(x.get("what") or "").replace("\n", " ")))
        L.append("\n")

    prior = [d for d in rows if d.get("prior_relationship")]
    if prior:
        L.append("## 🤝 On les connaît déjà — ouvrir là-dessus\n\n")
        for d in prior:
            pr = d["prior_relationship"]
            L.append("- **%s** — %s\n" % (d.get("display_name") or d.get("company"),
                                          str(pr.get("what") or "").strip()))
        L.append("\n")

    for tier, label in (("A", "Tier A — le levier réel, on commence ici"),
                        ("B", "Tier B — du potentiel, ensuite"),
                        ("C", "Tier C — plus tard, ou jamais")):
        sub = [d for d in rows if cats.get((d.get("categories") or [""])[0], {}).get("tier") == tier]
        if not sub:
            continue
        L.append("## %s\n\n" % label)
        L.append("| # | Score | Entreprise | Demande | À qui écrire | L'angle |\n")
        L.append("|---|---|---|---|---|---|\n")
        for i, d in enumerate(sub, 1):
            ask = d.get("ask") or {}
            angle = ""
            if d.get("sponsorship_history"):
                angle = "Sponsorise déjà — partir de là"
            elif d.get("prior_relationship"):
                angle = "Relation antérieure"
            elif ask.get("detail"):
                angle = str(ask["detail"]).strip()[:70]
            L.append("| %d | **%d** | %s<br><sub>%s · %s</sub> | %s<br><sub>~%s €</sub> | %s | %.75s |\n"
                     % (i, d["_score"], d.get("display_name") or d.get("company"),
                        d.get("country") or "", (d.get("categories") or ["?"])[0],
                        " + ".join(ask.get("type") or []) or "—",
                        ask.get("realistic_value_eur") or "?", contact_line(d), angle))
        L.append("\n")

    L.append("---\n<sub>%d entreprises actives · généré depuis crm/companies/</sub>\n" % len(rows))
    out = os.path.join(ROOT, "docs", "PLAN-DE-CONTACT.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("".join(L))
    print("✓ %s" % out)
    return 0


def deadlines_data(days=None):
    today = datetime.date.today()
    out = []
    for d in load():
        for x in d.get("deadlines") or []:
            when = _as_date(x.get("date"))
            if when and 0 <= (when - today).days <= (days or 99999):
                out.append((when, (when - today).days, d, x))
    return sorted(out, key=lambda r: r[0])


def brief(slug, outdir=None):
    """Qui, quoi, avec quel document, quel argument. Une page, et on décroche le téléphone."""
    d = next((x for x in load() if x.get("slug") == slug or x["_name"] == slug), None)
    if not d:
        raise SystemExit("Entreprise inconnue dans le CRM : %s" % slug)
    per = _yaml(os.path.join(PERSONAS, "%s.yaml" % d["persona"])) if d.get("persona") else {}
    mod = _yaml(os.path.join(MODULES, "%s.yaml" % d["sector"])) if d.get("sector") else {}
    s, sc, ask = score(d), d.get("scoring") or {}, d.get("ask") or {}
    L = []

    L.append("# %s — %s  (%d/100)\n\n" % (d.get("company"), "★" * stars(s), s))
    L.append("%s · %s · %s\n" % (d.get("country") or "", ", ".join(d.get("categories") or []),
                                 d.get("website") or ""))

    L.append("\n## La demande\n\n")
    L.append("**%s** — %s\n\n" % (" + ".join(ask.get("type") or []) or "à définir",
                                  str(ask.get("detail") or "").strip()))
    if ask.get("realistic_value_eur"):
        L.append("Ordre de grandeur : **%s €/an**\n" % ask["realistic_value_eur"])
    if d.get("why_us"):
        L.append("\n## Pourquoi eux\n\n%s\n" % str(d["why_us"]).strip())

    L.append("\n## L'angle\n\n")
    hist = d.get("sponsorship_history") or []
    if hist:
        L.append("Ils sponsorisent **déjà**. C'est l'accroche : on part de là.\n\n")
        for h in hist:
            L.append("- %s — %s\n" % (h.get("what"), h.get("url") or ""))
    else:
        L.append("Aucun sponsoring connu. L'angle se construit sur leurs valeurs : %s\n"
                 % (", ".join(d.get("values") or []) or "— à chercher —"))
    if d.get("values"):
        L.append("\nLeurs mots, à réemployer tels quels : *%s*\n" % ", ".join(d["values"]))

    L.append("\n## À qui écrire\n\n")
    for c in d.get("contacts") or []:
        L.append("- **%s** — %s  \n  %s  \n  <sub>source : %s (%s)</sub>\n"
                 % (c.get("name") or "?", c.get("role") or c.get("position") or "?",
                    c.get("email") or c.get("linkedin") or "pas d'adresse publique",
                    c.get("source_url") or c.get("source") or "—", c.get("retrieved_on") or "—"))
    for ch in d.get("inbound_channels") or []:
        L.append("- %s : %s\n" % (ch.get("type"), ch.get("url")))
    if reachability(d) in ("générique", "AUCUN"):
        L.append("\n> Pas de contact nommé. Cherches-en un avant d'envoyer : `info@` ne répond jamais.\n")

    L.append("\n## Quoi envoyer\n\n| | |\n|---|---|\n")
    L.append("| Persona | `%s` — %s |\n" % (d.get("persona"), per.get("objective", "")))
    L.append("| Ton | %s |\n" % per.get("tone", ""))
    L.append("| Module | `%s` — %s |\n" % (d.get("sector"), mod.get("label", "")))
    L.append("| Pages | %s |\n" % ", ".join(per.get("pages") or []))
    L.append("| E-mail | `emails/%s.md` |\n" % per.get("email", "technique"))
    L.append("\n```bash\npython -m kit --target %s\n```\n" % slug)

    if d.get("deadlines"):
        L.append("\n## Échéances\n\n")
        for x in sorted(d["deadlines"], key=lambda y: str(y.get("date"))):
            L.append("- **%s** — %s — %s\n" % (x.get("date"), x.get("what"), x.get("url") or ""))

    if notes(d):
        fit, prob, imp = notes(d)
        L.append("\n## Le score, et pourquoi\n\n| Critère | Note |\n|---|---|\n")
        L.append("| Adéquation produit | %d/10 |\n| Probabilité d'un oui | %d/10 |\n"
                 "| Impact si ça aboutit | %d/10 |\n| **Score** | **%d/100** |\n"
                 % (fit, prob, imp, s))
        L.append("\n%s\n" % str(sc.get("rationale") or "").strip())

    if d.get("interactions"):
        L.append("\n## Historique\n\n")
        for i in d["interactions"]:
            L.append("- %s — %s — %s\n" % (i.get("date"), i.get("type"), i.get("resume")))
    if d.get("notes"):
        L.append("\n## Notes\n\n%s\n" % str(d["notes"]).strip())
    L.append("\n---\n<sub>Sources : %s</sub>\n"
             % (" · ".join(str(x.get("url", "")) for x in (d.get("sources") or [])) or "—"))

    folder = outdir or os.path.join(ROOT, "output", slug)
    os.makedirs(folder, exist_ok=True)
    out = os.path.join(folder, "brief.md")
    open(out, "w", encoding="utf-8").write("".join(L))
    print("✓ %s" % out)
    return 0
