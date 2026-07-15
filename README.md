# falcohm-press

Le système commercial de **Gazmatek** et **Falc'ohm System ASBL** : la source unique de vérité, et
la chaîne qui en tire les documents.

On ne duplique pas un PDF. On décrit une **entreprise**, et le système produit le dossier, le
one-pager et l'e-mail adaptés — puis il s'en souvient.

```bash
pip install -r requirements.txt

python -m kit --target triplaco    # dossier + one-pager + e-mail, tracés dans le CRM
python -m kit --crm                # pipeline, scores, relances dues (⚠)
python -m kit --log triplaco mail "Envoyé au dir. commercial" --status sent
python -m kit mediakit             # le media kit de marque (11 pages)
python -m kit --events             # base événements
make all && make targets           # tout régénérer
make print                         # 300 dpi pour l'impression
```

## La chaîne

```
data/       les faits            chiffres, contacts, contreparties  ← on ne les écrit qu'ici
modules/    le discours          20 secteurs
personas/   la stratégie         4 profils (ton, pages, e-mail)
targets/    les entreprises      persona + module + interlocuteur
kit/pages/  la mise en page      17 pages composables
                 ↓
output/<Entreprise>/   Partnership.pdf · OnePager.pdf · email.md
                 ↓
crm/companies/<slug>.yaml   ← les documents s'y inscrivent automatiquement
```

Surcharges : `data/` < `module` < `persona` < `target`. Un chiffre changé dans `data/stats.yaml`
se propage partout.

## Les documents produits

| Document | Commande | Pages |
|---|---|---|
| **Dossier de partenariat** ciblé | `--target <slug>` | 9-10 |
| **One-pager** nominatif | idem (auto) | 1 |
| **E-mail** personnalisé | idem (auto) | — |
| **Media kit** de marque | `mediakit` | 11 |
| **Proposition** chiffrée | `proposals/_TEMPLATE.md` | — |
| **Communiqué / posts** | `press/` | — |

## Le CRM

Un fichier YAML par entreprise, versionné dans Git — lisible dans un diff, sans migration, pendant
dix ans. États, relances automatiques, historique daté, documents liés, événements liés.

```bash
python -m kit --crm-rank         # le classement : à qui donner son mois
python -m kit --crm-plan         # docs/PLAN-DE-CONTACT.md : qui contacter, dans quel ordre
python -m kit --crm-deadlines    # les dates de dépôt des subsides — rater une date coûte un an
python -m kit --crm-brief cras   # le mémo d'attaque : qui, quoi, quel argument, quel document
python -m kit --crm-validate     # refuse toute adresse e-mail non sourcée   (tourne en CI)
python -m kit --crm-sync         # fiche CRM → targets/ + data/partners.yaml (vue générée)
```

**Le score est calculé, pas saisi** : `business_fit × partnership_probability × impact_if_successful / 10`.
On multiplie — un produit parfait qu'ils refuseront ne vaut rien, et un oui certain sans effet non
plus. `crm-rank` pose la barre à 25 : au-dessus, ton mois ; en dessous, plus tard ou jamais.

**Une adresse e-mail se prouve, ou elle ne s'écrit pas.** Tout `email` porte `source_url`,
`retrieved_on` et `evidence` — la ligne recopiée telle quelle depuis la page. Sinon la validation
échoue et la CI est rouge. Il n'existe pas de statut « adresse devinée ». Voir `docs/CRM.md`.

## La documentation

| Fichier | Contenu |
|---|---|
| `CLAUDE.md` | **Le rôle de Claude** : procédures, règles absolues, ce qu'il produit sans qu'on le demande |
| `docs/STRATEGIE.md` | Les 3 phases : équiper Falc'ohm → faire grandir Gazmatek → media kit |
| `docs/PIPELINE.md` | Les 14 étapes, les documents, les KPI, ce qui est automatisable |
| `docs/CRM.md` | États, scoring, tags, relations |
| `docs/PARTNER-MATRIX.md` | 20 secteurs × persona × argument × CTA, avec leur statut de rédaction |
| `docs/MEDIA-KIT.md` | Spécification page par page du media kit |
| `brand/` | Couleurs, typo, grille, logos, style rédactionnel |
| `checklists/` | Avant envoi · activation d'un partenariat |

## Règles absolues

- Un chiffre ne s'écrit **que** dans `data/`.
- Nous **fabriquons** les enceintes d'après les plans d'un concepteur. Nous ne les **concevons** pas.
- Jamais « sponsor », jamais « remise » : *partenaire*, *conditions préférentielles*.
- Jamais d'envoi à `info@`.
- Jamais de contrepartie promise sans être livrable (`data/benefits-catalog.yaml`, `realistic`).

## État de la rédaction

- ✅ **Validé** : module `bois`, moteur, media kit (structure)
- 🟠 **À relire** : `audio`, `visserie`, `flightcases`, `eclairage`, `telecom`, `boissons`,
  `institutionnel`
- 🔴 **Squelettes à réécrire** : `outils`, `video`, `photo`, `securite`, `logistique`, `energie`,
  `banque`, `cloud`, `ia`, `medias`, `collectivites`
- ⚠ **Données à confirmer** : statistiques d'audience Meta, jauges et budgets des événements,
  logos des partenaires actuels (voir les `TODO` dans `data/mediakit.yaml` et `events/`)
