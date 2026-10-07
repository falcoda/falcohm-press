<!-- Écrit à la main le 2026-10-02, jour de la sortie du clip « Tout est facile » (chaîne
     BASEBelgium, https://www.youtube.com/watch?v=mEW-r2EkRVM, publié le 2026-10-02).
     Fiche : crm/companies/base.yaml, knowledge/Base.md.
     Relation actuelle : FOURNISSEUR payé (tournage du 2026-09-06, sound system en décor).
     Ce texte ouvre une demande NOUVELLE : un partenariat durable avec l'ASBL, soutien de
     BASE contre visibilité sur nos événements et nos canaux. Pas de demande de crédit sur le clip
     (décision de Corentin, 2026-10-02). -->

> ### Consignes d'envoi
> - **À :** TODO. La responsable BASE rencontrée sur le tournage du 06/09, à condition d'avoir son
>   adresse dans un échange réel (devis, facture, brief). La description du clip nomme l'équipe
>   projet BASE : Sandrine Decleer, Laetitia Descamps, Catherine Van Dingenen, Stéphanie Lengelé.
>   Aucune adresse prouvée pour elles dans le dépôt : ne pas en deviner une.
> - **Destinataire côté BASE, pas côté production.** Si la commande du 06/09 est passée par
>   Incendie Films, la productrice n'a pas la main sur un budget de marque : ce mail va chez BASE.
> - **Le sound system était un élément de DÉCOR**, il n'a pas sonorisé le clip. Ne jamais écrire
>   le contraire.
> - **Pièce jointe : aucune.** Le dossier `output/Base/` date de juillet et repose sur la piste
>   cabine, abandonnée. S'ils demandent un dossier, le regénérer d'abord
>   (`python -m kit --target base`) et le relire.
> - Tracer après envoi :
>   `python -m kit --log base mail "Demande de partenariat ASBL Génération Débrouille, après la sortie du clip" --status sent`

---

**Objet :** Après « Tout est facile » : Génération Débrouille sur nos événements

Bonjour Madame TODO,

Le clip est sorti ce matin, et c'est un plaisir de retrouver en arrière-plan, sur une bonne partie
des images, le sound system que nous avions installé pour le tournage du 6 septembre. Merci encore
pour votre confiance.

Je vous écris pour vous proposer d'aller plus loin ensemble. Falc'ohm System est une ASBL du Brabant
wallon, fondée en 2020, qui porte deux marques : Gazmatek, sous laquelle nous organisons des
événements de musiques électroniques, et Falc'ohm System, sous laquelle nous construisons et
exploitons le sound system qui les sonorise. L'association repose sur 80 bénévoles : ils construisent
le système d'après les plans d'un concepteur, puis l'installent et le font tourner eux-mêmes le
soir de l'événement. C'est, assez littéralement, une histoire de Génération Débrouille.

Nous organisons 6 à 10 dates par an, qui réunissent plus de 10 000 festivaliers, et nous sommes
suivis par 27 000 personnes sur Instagram et Facebook.

Nous aimerions que BASE devienne partenaire de notre ASBL, dans la durée : un soutien de BASE à
l'association, et en retour une présence Génération Débrouille sur nos événements et nos canaux :

- votre logo sur les affiches de nos événements ;
- une mention dans nos aftermovies, et des posts dédiés sur nos réseaux ;
- le droit d'utiliser nos événements et notre projet dans votre propre communication ;
- un communiqué de presse commun à l'annonce du partenariat ;
- des entrées et un accès backstage sur nos dates, pour votre équipe ou vos clients.

Notre prochaine date, Halloween Shadow, a lieu le 31 octobre au Studio City Gate ; l'édition 2025 a
réuni 2 500 personnes. Elle pourrait être une première occasion, sous réserve de ce que les délais
permettent encore de mettre en place de part et d'autre.

Est-ce le genre de démarche que vous pouvez examiner, ou faut-il que je m'adresse à quelqu'un
d'autre chez BASE ?

Bien à vous,

Corentin Dallenogare
Président, Falc'ohm System ASBL
contact@falcohmsystem.com · gazmatek.com · falcohmsystem.com

---

## Ce que ce texte fait, et pourquoi

1. **Il s'ouvre sur leur sortie, le jour même.** Le clip est le prétexte naturel prévu dans la
   fiche CRM ; on écrit pendant qu'il est encore une bonne nouvelle chez eux. Le sound system y
   est décrit comme ce qu'il était : à l'image, en arrière-plan.
2. **Il passe explicitement de fournisseur à partenaire.** « Aller plus loin ensemble » : elle
   sait que c'est une demande nouvelle, et on ne la cache pas derrière la prestation.
3. **Il reprend leurs propres mots.** « Génération Débrouille » décrit ce que fait l'ASBL : des
   bénévoles qui fabriquent leur système eux-mêmes. On ne plaque pas leur slogan, on montre qu'on
   en est un exemple.
4. **Les contreparties sont toutes livrables.** Elles reprennent le contenu du palier
   « Partenaire de saison » de `data/benefits-catalog.yaml` (`realistic: true`). Pas de naming ni de stand d'activation :
   ces paliers sont marqués non livrables aujourd'hui. Pas de marquage sur les caissons non plus :
   une marque grand public n'en a pas besoin (règle du catalogue).
5. **Aucun montant.** On ne s'engage sur rien ; le chiffrage vient avec leur réponse.
6. **Les chiffres viennent de `data/`** : 2020, 80 bénévoles, 6 à 10 dates organisées, +10 000
   festivaliers, 27 000 abonnés (`data/stats.yaml`), 2 500 personnes
   (`events/shadow-3-stages.yaml`). On écrit 6 à 10 et non 10 à 15 : un partenaire de visibilité
   compte les dates organisées, pas les locations de matériel.
7. **Un partenaire de l'ASBL, pas d'une saison** (consigne de Corentin, 2026-10-02). La relation
   n'a pas de date de fin écrite ; elle porte sur l'association, ses événements et ses canaux.
8. **Shadow proposé avec réserve.** Quatre semaines, c'est court pour un budget de marque
   télécom : « première occasion, sous réserve des délais » laisse BASE dire non à Shadow sans
   dire non au partenariat.
9. **Le bois n'est pas revendiqué.** La découpe n'est pas toujours faite par l'ASBL : le texte dit
   que les bénévoles construisent, installent et exploitent, rien de plus.
10. **Une seule question finale, qui se répond en une ligne.** Pas d'appel, pas de rendez-vous,
   aucun « sponsor ».
