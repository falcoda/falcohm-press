# Media Kit Gazmatek — spécification

Le media kit **ne demande jamais d'argent**. Il explique pourquoi Gazmatek est une marque avec
laquelle il est intéressant de s'associer. C'est le document que l'on envoie *avant* toute demande,
et celui qu'un journaliste, un booker ou un directeur marketing peut lire seul.

Durée de vie : plusieurs années. Seules les données changent (`data/`), jamais la structure.

| # | Page (`id`) | But | Données | Photos | KPI affichés | CTA |
|---|---|---|---|---|---|---|
| 1 | `mk_cover` | Poser la marque en 3 secondes | `org`, `year` | Foule, lumière, plein cadre | — | — |
| 2 | `mk_manifesto` | Dire ce qu'est Gazmatek, en une phrase forte | `content.manifesto` | Aucune (typo pleine page) | — | — |
| 3 | `about` | Qui porte le projet (ASBL + pôle technique) | `about`, `stats` | Bande live | 5 chiffres clés | — |
| 4 | `mk_audience` | Montrer **qui** est le public | `audience` | 3 photos public | Âge, provenance, genre | — |
| 5 | `mk_reach` | Prouver la portée | `stats`, `reach` | — | Abonnés, portée, croissance, graphique | — |
| 6 | `gazmatek` | Les événements : affiches + photos | `images.posters`, `images.events` | 4 affiches + 3 photos | — | — |
| 7 | `mk_events` | Le palmarès : dates, lieux, jauges | `events/*.yaml` | — | Jauge, artistes, année | — |
| 8 | `ecosystem` | Gazmatek + Falc'ohm : la machine | `org_blocks` | — | — | — |
| 9 | `mk_partners` | Ils nous font confiance (+ emplacements libres) | `partners actifs` | Logos | — | — |
| 10 | `mk_opportunities` | Ce qu'un partenaire peut faire avec nous | `benefits_catalog` | Mockups | Niveaux d'engagement | Discret : « parlons-en » |
| 11 | `contact` | Coordonnées, QR | `org` | Bande live | — | Prendre contact |

## Règles de rédaction
- **Aucun prix** dans le media kit. Les tarifs vivent dans les *proposals*.
- Aucun « nous recherchons » : le media kit **présente**, il ne **demande** pas.
- Chaque chiffre affiché doit exister dans `data/` et être vérifiable.
- Les pages 3, 6, 8 et 11 sont **partagées** avec les dossiers de partenariat : elles ne sont
  écrites qu'une fois.

## Ce qu'il manque aujourd'hui pour l'atteindre (à collecter)
- [ ] Statistiques d'audience Meta (âge, genre, villes) → `data/audience.yaml`
- [ ] Portée mensuelle Instagram + Facebook → `data/reach.yaml`
- [ ] Jauges réelles et fréquentation par événement → `events/*.yaml`
- [ ] Logos des partenaires actuels → `assets/partners/current/`
- [ ] 3 photos « public » nettes, droits clairs → `assets/photos/audience/`
