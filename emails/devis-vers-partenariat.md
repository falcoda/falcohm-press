# Transformer un devis en partenariat

Situation : on a écrit à `info@`, et un commercial a répondu **avec un prix**. Pas de collaboration,
juste un devis. C'est ce qui est arrivé sur le module bois après la campagne du 23/08/2026.

## Pourquoi ce n'est pas un échec

Un devis vaut mieux qu'une réponse polie, pour trois raisons :

1. **Il est signé.** Un devis porte un nom, une fonction, une adresse directe et souvent un numéro
   de ligne. C'est exactement l'interlocuteur nommé que la règle du dépôt exige, obtenu sans
   téléphoner. Neuf envois sur `info@` n'en avaient pas produit un seul.
2. **Il prouve un mandat.** Cette personne a le droit d'engager un prix. Elle n'a peut-être pas le
   droit d'accorder un partenariat, mais elle sait qui l'a, et maintenant elle nous connaît.
3. **Il donne des chiffres réels.** Un prix au m² de multiplex bouleau, écrit par un fournisseur,
   c'est une donnée qui entre dans `data/` et qui rend tous les dossiers suivants crédibles.

**Ce qu'il faut faire immédiatement :** recopier le nom, la fonction et l'adresse du signataire dans
`contacts:` de la fiche CRM, avec `source_url` = le devis reçu, `retrieved_on` = la date, `evidence` =
la ligne de signature recopiée. Une adresse lue sur un devis reçu est **prouvée**, elle nous a écrit.

## Le texte

Répondre **au devis lui-même**, dans le fil, à la personne qui l'a signé. Sous 48 h : le dossier est
encore ouvert sur son bureau.

> **Objet :** Re: {{OBJET_DU_DEVIS}}
>
> Bonjour {{NOM_DU_SIGNATAIRE}},
>
> Merci pour ce devis, et merci d'avoir pris le temps de le chiffrer.
>
> Je dois vous dire que mon premier message était mal formulé, et le devis en est la conséquence :
> j'avais mis « demande de prix » dans l'objet. Ce n'est pas un devis ponctuel que nous cherchons.
>
> Nous sommes une ASBL culturelle de Genappe qui fabrique ses propres enceintes pour ses événements.
> {{VOLUME_REEL}}, et ce besoin revient chaque année, sur cinq à dix ans de construction et de
> maintenance. Ce que nous cherchons, c'est un fournisseur unique sur cette durée, à conditions
> préférentielles, plutôt qu'un devis à chaque série.
>
> En échange, nous offrons une visibilité réelle : votre marquage sur des caissons utilisés sur
> 10 à 15 dates par an, une mention auprès de nos 27 000 abonnés, et le making-of de la
> construction, photos professionnelles cédées.
>
> Votre devis reste la meilleure base de discussion que j'aie. Deux questions simples :
>
> 1. Est-ce vous qui pouvez examiner un accord de ce type, ou quelqu'un d'autre chez vous ?
> 2. Si c'est vous : sur quelle base travaillez-vous un tarif annuel plutôt qu'un devis à l'unité ?
>
> Bien à vous,
> Corentin Dallenogare
> Président, Falc'ohm System ASBL
> contact@falcohmsystem.com · gazmatek.com · falcohmsystem.com

## Les deux variables à remplir

`{{VOLUME_REEL}}`, **le cœur du message, et le seul endroit où on peut se tirer une balle dans le
pied.** Un fournisseur ne consent une remise permanente que contre un volume. Écrire le vrai, pris
dans `data/` : nombre de panneaux par série, nombre de caissons prévus. Si le chiffre n'est pas
connu, écrire ce qui est connu (« une première série de N caissons, puis N par an »), jamais un
volume gonflé. Un volume inventé se retourne à la première commande, et il se retourne devant
quelqu'un qui a nos prix par écrit.

`{{OBJET_DU_DEVIS}}`, garder leur objet à eux. Un nouveau fil serait un nouveau mail à ignorer ;
une réponse dans le fil arrive avec l'historique et le devis attachés.

## Ce qu'on ne fait pas

- **Ne pas négocier le prix du devis.** On ne discute pas un tarif ponctuel, on demande à changer de
  cadre. Marchander décrédibilise la démarche : on redevient un client parmi d'autres.
- **Ne pas renvoyer le dossier PDF.** Il est déjà parti le 23/08. Le renvoyer dit qu'on n'a pas
  remarqué qu'ils avaient répondu.
- **Ne pas promettre de contrepartie hors `data/benefits-catalog.yaml`** (champ `realistic`).
- **Ne pas laisser passer plus de 48 h.** Passé une semaine, un devis non suivi est un devis mort,
  et relancer dessus fait mendiant.

## Après

Statut CRM : `replied` (pas `sent`, ils ont répondu). Puis `meeting` si l'échange téléphonique est
obtenu. `python -m kit --log <slug> réponse "devis reçu, signé par X" --status replied --date <ISO>`.
