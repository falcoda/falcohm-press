# Stratégie de prospection

Trois phases. On ne mélange pas : un fournisseur technique et une marque grand public ne se
convainquent pas avec le même dossier ni avec le même vocabulaire.

## Phase 1 — Équiper Falc'ohm  *(persona : fournisseur technique / fabricant audio)*
Objectif : obtenir du **matériel** ou des **conditions préférentielles**. Pas d'argent.

| Cible | Module | Fichier |
|---|---|---|
| Triplaco, Biemar, Cras, Wopaco | bois | `targets/triplaco.yaml`… |
| Würth | visserie | `targets/wurth.yaml` |
| Penn Elcom, Adam Hall | flightcases | `targets/pennelcom.yaml` |
| B&C, Faital, Powersoft | audio | `targets/bc.yaml` |

Argument central : *le matériel est utilisé chaque week-end, il est visible, et le besoin est
récurrent sur 5 à 10 ans.*

## Phase 2 — Faire grandir Gazmatek  *(personas : marque grand public / institution)*
Objectif : **soutien financier**, activation de marque, subsides.

| Cible | Module |
|---|---|
| Base, Proximus | telecom |
| Red Bull, AB InBev | boissons |
| Loterie Nationale, Province, FWB | institutionnel |

Argument central : *+10 000 festivaliers par an, 27 000 abonnés, un public jeune, un projet
non lucratif porté par 40 bénévoles.*

## Phase 3 — Devenir un événement reconnu
Media kit annuel : chiffres à jour, nouvelles photos, partenaires acquis, projets à venir.
Techniquement, c'est un `dossiers/mediakit.yaml` avec sa propre liste de pages.

## Règles de séquencement
1. **Une phase à la fois.** Un « non » de Red Bull ne coûte rien ; un « non » de Triplaco bloque
   la construction.
2. **Toujours viser une personne nommée.** L'adresse `info@` ne répond jamais.
3. **Trois contacts maximum** : envoi, relance J+10, relance J+30. Ensuite on passe à autre chose.
4. **Chaque envoi est tracé** dans `data/partners.yaml` (`make crm` affiche le pipeline).
