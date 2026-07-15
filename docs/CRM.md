# CRM — architecture

Pas de base de données : **un fichier YAML par entreprise**, versionné dans Git. C'est le seul
format qui tienne dix ans sans migration, qui se lise dans un diff et qui se relie aux documents.

```
crm/companies/<slug>.yaml     l'entreprise, ses contacts, son historique, ses liens
events/<slug>.yaml            un événement (sponsors présents, chiffres, médias)
knowledge/<Entreprise>.md     la connaissance qualitative (ce qu'on a appris)
output/<Entreprise>/          les documents envoyés
```

## Pipeline (états)

| État | Définition | Sortie attendue |
|---|---|---|
| `lead` | Identifié, pas encore qualifié | Fiche knowledge créée |
| `qualified` | Bon secteur, bon moment, interlocuteur identifié | Nom + e-mail d'une personne |
| `researched` | Fiche knowledge remplie, arguments choisis | Angle d'attaque écrit |
| `sent` | Dossier + e-mail envoyés | Date d'envoi |
| `followup_1` | Relance J+10 | — |
| `followup_2` | Relance J+30 | — |
| `replied` | Réponse reçue (positive ou non) | Qualifier la réponse |
| `meeting` | Visio ou rendez-vous fixé | Compte-rendu |
| `proposal` | Proposition chiffrée envoyée | `proposals/<slug>.md` |
| `negotiation` | Discussion des contreparties | — |
| `won` | Partenariat signé | Contrat + annonce publique |
| `lost` | Refus ou silence après 3 contacts | Raison notée, à recontacter dans 12 mois |
| `active` | Partenariat en cours | Activation, suivi |
| `renewal` | Fin de cycle, à renouveler | Bilan chiffré |

## Scoring (0-100)

Trois notes, saisies à la main dans `scoring:`. Le score global, lui, est **calculé** :

```
score = business_fit × partnership_probability × impact_if_successful / 10
```

| Note | Question | Le piège |
|---|---|---|
| `business_fit` | Leurs produits répondent-ils à un besoin **réel** ? | Un beau nom n'est pas un besoin. |
| `partnership_probability` | Diront-ils **oui** ? | C'est le champ qu'on gonfle par optimisme. Un géant mondial avec un portail sponsoring saturé, c'est 2. Un négociant wallon dont le patron décide seul et qui sponsorise déjà le club local, c'est 8. |
| `impact_if_successful` | Et si oui, **qu'est-ce que ça change** ? | Un accord sans effet reste un accord sans effet. |

**On multiplie, on n'additionne pas.** Un produit parfait qu'ils refuseront ne vaut rien
(`9 × 1 × 9 = 8`) ; un oui certain sans effet non plus (`9 × 9 × 1 = 8`). Une somme pondérée
masquerait exactement ce qu'on cherche à voir : le zéro sur un axe doit tuer la ligne, et il la tue.
La cible qui mérite un mois de travail, elle, sort à `9 × 7 × 9 = 57`.

`scoring.rationale` est **obligatoire**. Trois chiffres sans justification ne valent rien : dans six
mois, personne — pas même celui qui les a écrits — ne saura sur quoi ils reposaient.

Tant qu'une fiche n'a pas ses trois notes, on retombe sur l'ancien score structurel. La migration se
fait fiche par fiche ; rien ne casse en attendant.

- `make crm-rank` → le classement, barre à 25. Au-dessus : ton mois. En dessous : plus tard, ou jamais.
- `make crm` → le pipeline, relances dues en tête.
- `make crm-brief T=<slug>` → le mémo d'attaque d'une entreprise.

## La règle qui prime sur toutes les autres

**Une adresse e-mail se prouve, ou elle ne s'écrit pas.**

Tout `email` doit porter `source_url` (l'URL exacte où on l'a lu), `retrieved_on` et `evidence`
(la ligne recopiée telle quelle depuis la page). `make crm-validate` en fait une **erreur**, pas un
avertissement, et la CI est rouge. Il n'existe pas de statut `pattern_guess` : une adresse
extrapolée à partir d'un motif (`prenom.nom@societe.be`) n'entre pas dans cette base.

Le validateur signale aussi les adresses dont le domaine diffère de celui du site — la signature
d'une extrapolation. Ce sont des avertissements : ils demandent une vérification humaine, ils ne
tranchent pas à ta place.

Une adresse devinée qui rebondit grille l'entreprise pour de bon, et on ne le saura jamais.

`crm/suppression.yaml` (RGPD, art. 21) : toute personne qui demande à ne plus être contactée y
atterrit le jour même. On ne supprime pas sa fiche — on la marque. Supprimer, c'est risquer de la
recontacter dans six mois en toute bonne foi.

## Tags
`technique`, `marque`, `institution`, `belge`, `international`, `deja-sponsor`, `contact-chaud`,
`gros-compte`, `pme`, `urgent`, `saisonnier`.

## Ce qui relie tout
Chaque entreprise pointe vers : ses `contacts`, ses `interactions` (historique daté), les
`documents` envoyés, les `events` où elle était présente, sa fiche `knowledge`. C'est ce qui permet
de répondre, dans deux ans, à « qu'est-ce qu'on a déjà envoyé à Triplaco et qu'est-ce qu'ils ont
répondu ? ».
