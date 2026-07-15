# Architecture

```
data/          les faits          (chiffres, contacts, textes, images)   ← source unique de vérité
modules/       le discours        (un secteur = un YAML)
personas/      la stratégie       (objectif, ton, pages, template d'e-mail)
targets/       les entreprises    (persona + module + interlocuteur)
kit/pages/     la mise en page    (une page = un fichier = un id)
kit/build.py   la composition
                       ↓
output/<Entreprise>/   PDF + one-pager + e-mail
```

## L'ordre de priorité des surcharges

```
data/  <  module  <  persona  <  target
```

Concrètement : un target peut tout écraser (une photo de couverture, une stat, une liste de pages)
sans dupliquer quoi que ce soit.

## Les pages disponibles

| id | rôle | dépend de |
|---|---|---|
| `cover` | couverture | `module.cover` |
| `about` | qui sommes-nous + chiffres | `data` |
| `gazmatek` | le projet culturel, affiches, photos | `module.gazmatek` |
| `ecosystem` | Gazmatek → Falc'ohm → partenaire | `module.ecosystem` |
| `project` | le projet + les besoins | `module.project`, `module.needs` |
| `material` | la matière / le composant | `module.material` *(page ignorée si absente)* |
| `timeline` | trajectoire + ce qui vient | `module.timeline` |
| `benefits` | contreparties + mockups | `data.benefits`, `module.benefits` |
| `packages` | formes de collaboration | `module.packages` |
| `contact` | merci + coordonnées + QR | `data.org` |
| `onepager` | tout le dossier en 1 page | `module.onepager` |

Une page déclarée dans un persona mais dont le module ne fournit pas la donnée est **ignorée
silencieusement** (`requires=` dans le décorateur `@page`). C'est ce qui permet à un persona
« fournisseur technique » de demander `material` alors que le module `visserie` n'en a pas.

## Ajouter une cible

```yaml
# targets/neutrik.yaml
company: "Neutrik"
persona: fournisseur-technique
module: audio            # ou un nouveau module connectique
phase: 1
contact: { name: "M. X", role: "Responsable commercial", email: "" }
website: "https://www.neutrik.com"
overrides:               # facultatif : tout ce qui est dans data/ peut être écrasé
  images: { cover: autre_photo.jpg }
```

```bash
python -m kit --target neutrik
# → output/Neutrik/Neutrik-Partnership-2026.pdf
#   output/Neutrik/Neutrik-OnePager-2026.pdf
#   output/Neutrik/email.md
```

## Ce que le dépôt pourra générer ensuite

Le moteur est agnostique du type de document : une page = un id, un document = une liste d'ids.
Ajouter un dossier de presse, un communiqué ou une page « Partenaires » pour le site revient à
écrire une page et une liste — les données ne bougent pas.
