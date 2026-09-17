<!-- Écrit à la main le 2026-09-09, après la recherche approfondie (knowledge/TLHP.md). Réécrit le
     2026-09-11 : l'ASBL est DÉJÀ CLIENTE PROFESSIONNELLE de TLHP (compte falcohm6tm@outlook.com), et
     Corentin cherche un PARTENARIAT, pas un compte pro. Le dossier généré du module audio n'est pas
     joint : il n'a pas été relu pour ce cas, et il ne doit citer ni ampli ni DSP.
     Brouillon Gmail : r7787036453420236984, destinataire info@tlhp.fr depuis le 2026-09-12. -->

> **À :** `info@tlhp.fr`
> **EXCEPTION À LA RÈGLE DES ADRESSES GÉNÉRIQUES**, décidée par Corentin le 2026-09-12. TLHP ne
> publie aucune adresse nominative. `info@tlhp.fr` est l'adresse que les fabricants (Fostex)
> donnent comme contact de TLHP, et celle des échanges du compte pro existant ; dans une
> entreprise familiale de cinq personnes, elle est lue par un Denoual. Le mail s'ouvre sur
> « Monsieur Denoual » pour être routé. Si une adresse nominative apparaît dans la réponse, la
> reporter dans la fiche CRM.
>
> Envoyer depuis `contact@falcohmsystem.com` : l'adresse outlook est citée pour qu'ils retrouvent
> le compte.
>
> **Pièce jointe : le dossier de partenariat**, à joindre à la main dans Gmail (le connecteur ne
> porte pas un fichier de 2 Mo) : `output/TLHP-SAS-Tout-Le-Haut-Parleur/TLHP-SAS-Tout-Le-Haut-Parleur-Partnership-2026.pdf`,
> régénéré le 2026-09-13 après correction du module audio (plus d'amplification ni de DSP demandés).
> Alternative plus légère : le one-pager du même dossier, 700 Ko.
>
> Tracer après envoi : `python -m kit --log tlhp mail "Premier contact partenariat a <Prenom Nom>" --status sent --date <ISO>`

---

**Objet :** Devenir partenaires : un client pro qui agrandit son sound system (Falc'ohm System / Gazmatek)

Bonjour Monsieur Denoual,

Nous sommes déjà clients professionnels chez vous, sous l'adresse falcohm6tm@outlook.com. Notre
sound system tourne déjà, et nous l'agrandissons avec une nouvelle série de caissons qui s'étale
sur plusieurs années : nous voudrions aller plus loin avec vous, et vous proposer un partenariat.

Falc'ohm System est une association sans but lucratif de Genappe, en Belgique, fondée en 2020.
Elle porte deux marques : Gazmatek, sous laquelle elle organise ses événements de musiques
électroniques, et Falc'ohm System, sous laquelle elle construit et exploite le matériel qui les
sonorise. Nous fabriquons nos caissons nous-mêmes, d'après les plans de deux concepteurs, dans un
atelier tenu par des bénévoles : 80 inscrits, 45 actifs sur les événements, formés au son, à la
lumière, à la réparation et au reconing. Le système tourne devant plus de 10 000 spectateurs par an.

Nos références de haut-parleurs sont arrêtées, et elles figurent à votre stock, avec leurs kits
de reconing. Nous cherchons un soutien matériel sur ce que nous achetons de façon récurrente :

- des haut-parleurs de grave et des moteurs de compression, le poste le plus lourd, et un
  consommable puisqu'ils se remplacent et se recônent ;
- de la connectique et du câblage ;
- de la quincaillerie de caisson ;
- des kits de reconing pour la maintenance.

Conditions préférentielles au-delà de notre tarif pro, ou dotation partielle sur la nouvelle
série : nous sommes ouverts sur la forme.

Pour situer le volume : quatre caissons fermes cette année, une quinzaine sur deux ans selon les
prix obtenus, et une vingtaine de haut-parleurs et de moteurs pour cette série.

En retour, nous documentons entièrement la construction, photos d'atelier et d'exploitation,
fiche par modèle de caisson, pour votre galerie de réalisations et votre forum. Le marquage
partenaire est apposé sur les caissons eux-mêmes, donc il voyage sur chaque date que nous jouons,
et nous citons les composants que vous fournissez sur nos supports. Vous trouverez notre dossier de
partenariat en pièce jointe.

Est-ce le genre de partenariat que TLHP peut examiner, ou faut-il que je m'adresse à quelqu'un
d'autre chez vous ?

Bien à vous,

Corentin Dallenogare
Président, Falc'ohm System ASBL
contact@falcohmsystem.com

---

## Ce que ce texte fait, et pourquoi

1. **Il ouvre sur la relation qui existe déjà** : clients professionnels, compte
   falcohm6tm@outlook.com (Corentin, 2026-09-11). Le lecteur retrouve l'historique en une
   recherche, et la demande devient « aller plus loin » plutôt qu'une sollicitation d'inconnu.
   Rien n'est dit de ce qu'on a acheté : le dépôt ne le sait pas.
2. **Il demande un partenariat, en positif et en liste** : quatre postes en catégories, références
   non nommées. Pas de composants de filtre passif (aucun modèle n'en utilise hors le FB464, qui se
   commande avec le moteur), ni ampli ni DSP (ADmark).
3. **Il nomme les deux formes possibles sans en imposer une** : conditions préférentielles
   au-delà du tarif pro qu'ils nous font déjà, ou dotation partielle. Jamais « remise », jamais
   « sponsor ». La recherche du 2026-09-09 dit qu'ils vendent avec conseil plutôt qu'ils ne
   donnent : la première forme est la plus probable, la seconde reste ouverte.
4. **Un seul repère de volume, arrondi là où il dépend du prix.** Chez SoundImports, la première
   réponse a été six questions sur les volumes. Les 4 Solana, déjà équipés, ne sont pas comptés.
5. **Nous fabriquons, nous ne concevons pas** : « d'après les plans de deux concepteurs » (JW
   Sound et Marc.o, data/bom.yaml). Une erreur ici décrédibiliserait tout auprès de gens qui
   vendent des kits de sound system.
6. **Les contreparties sont dans leurs mots et dans le catalogue** : galerie de réalisations,
   forum (leurs mots), marquage permanent sur les caissons et making-of
   (data/benefits-catalog.yaml, contreparties réalistes). Pas de « 27 000 abonnés » : ce n'est pas
   ce qu'un distributeur de composants achète.
7. **La question finale se répond en une ligne**, et donne une sortie honorable vers le bon
   interlocuteur si ce n'est pas lui. Pas d'appel, pas de rendez-vous.
