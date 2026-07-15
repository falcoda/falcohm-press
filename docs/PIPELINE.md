# Pipeline commercial

| # | Étape | Ce qu'on fait | Document produit | Sortie / critère | KPI | Automatisable |
|---|---|---|---|---|---|---|
| 1 | **Lead** | Repérer une entreprise (salon, concurrent d'un partenaire, fournisseur qu'on utilise déjà) | `crm/companies/<slug>.yaml` | Fiche créée | Nb de leads / mois | Oui — script d'import |
| 2 | **Qualification** | Le module existe-t-il ? Le moment est-il bon ? La taille est-elle adaptée ? | Score CRM | Score ≥ 40 | % de leads qualifiés | Oui — `crm.score()` |
| 3 | **Recherche** | Qui décide ? Que sponsorisent-ils déjà ? Quelles valeurs ? | `knowledge/<Entreprise>.md` | Interlocuteur **nommé** | % de fiches avec nom + e-mail | Partiellement — recherche web |
| 4 | **Documents** | Générer le dossier ciblé | `python -m kit --target <slug>` | PDF + one-pager + e-mail | Temps de production (< 1 min) | **Oui, entièrement** |
| 5 | **Premier contact** | Envoyer, à une personne, jamais à `info@` | `output/<E>/email.md` | E-mail envoyé | Taux d'ouverture / réponse | Semi — l'envoi reste manuel |
| 6 | **Relance J+10** | Court, une seule question | `emails/relance-j10.md` | — | Taux de réponse après relance | Oui — alerte CRM |
| 7 | **Relance J+30** | Dernière tentative, on laisse la porte ouverte | `emails/relance-j30.md` | — | — | Oui — alerte CRM |
| 8 | **Visio** | 20 min, comprendre leur intérêt, pas vendre | Compte-rendu dans `interactions` | Besoin identifié | Nb de visios / mois | Non |
| 9 | **Proposition** | Contreparties chiffrées, adaptées à ce qu'ils ont dit | `proposals/<slug>.md` | Proposition envoyée | Taux de passage visio → proposition | Semi |
| 10 | **Négociation** | Ajuster le périmètre, pas brader la marque | — | Accord de principe | Durée moyenne | Non |
| 11 | **Signature** | Convention écrite, même courte | `proposals/<slug>-convention.md` | Contrat signé | Taux de closing | Non |
| 12 | **Activation** | Livrer ce qu'on a promis : logo, post, marquage, photos | Checklist d'activation | Contreparties livrées | % de contreparties livrées | Oui — checklist |
| 13 | **Suivi** | Envoyer les preuves : photos, stats du post, matériel en usage | Rapport d'activation | Partenaire content | Nb de preuves envoyées | Semi |
| 14 | **Renouvellement** | Bilan chiffré + proposition de reconduction | `proposals/<slug>-bilan.md` | Reconduction | Taux de renouvellement | Semi |

## Les KPI qui comptent vraiment
- **Taux de réponse au premier contact** (cible : > 25 % si l'interlocuteur est nommé, < 5 % sur `info@`).
- **Taux visio → partenariat** (cible : > 40 %).
- **Délai lead → signature** (attendu : 2 à 4 mois pour un fournisseur, 6 à 12 pour une institution).
- **Taux de renouvellement** (le seul qui compte à long terme).

## Automatisations en place
- Génération des documents : `python -m kit --target <slug>` (PDF + one-pager + e-mail, < 1 min).
- Traçabilité : les documents générés sont écrits dans la fiche CRM automatiquement.
- Relances : `python -m kit --crm` affiche ⚠ sur toute entreprise dont la relance est due.
- Scoring : recalculé à chaque `--log`.

## Ce qui ne doit jamais être automatisé
L'e-mail de premier contact est **relu et personnalisé à la main** quand le score est ≥ 70.
Un dossier parfait envoyé à une adresse générique ne sert à rien.
