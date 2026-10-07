<!-- Écrit à la main le 2026-10-02. Fiche : crm/companies/base.yaml.
     EXCEPTION À LA RÈGLE « jamais d'adresse générique », décidée par Corentin le 2026-10-02 :
     ce message ne porte PAS la demande de partenariat, il demande seulement à qui l'adresser.
     Aucune adresse prouvée n'existe pour Sandrine Decleer (Lead BASE Brand and Communication)
     ni pour le sponsoring Telenet. La demande elle-même : emails/base-tout-est-facile.md. -->

> ### Consignes d'envoi
> - **À :** press@telenetgroup.be. Adresse publiée dans le communiqué BASE du 12/05/2026,
>   https://press.telenet.be/base-evolves-its-internet-and-tv-offering-to-better-match-todays-usage-needs
>   (bloc contact : « Vanessa Zwaelens, Spokesperson, press@telenetgroup.be »).
> - **Pièce jointe : aucune.** Pas de dossier, pas de photos.
> - **Si on reçoit une adresse en réponse :** l'inscrire dans `contacts` avec ce mail comme
>   `source_url` et la ligne de réponse comme `evidence`, puis envoyer
>   `emails/base-tout-est-facile.md` à cette personne.
> - Tracer après envoi :
>   `python -m kit --log base mail "Demande de routage au service presse : contact partenariats de marque BASE" --status sent`

---

**Objet :** Demande de contact : partenariats de marque BASE

Bonjour Madame Zwaelens,

Je préside Falc'ohm System, une ASBL du Brabant wallon qui organise des événements sous le nom de
Gazmatek et construit le sound system qui les sonorise. Nous avons travaillé avec BASE sur le
tournage du clip « Tout est facile », sorti ce matin.

Nous souhaitons proposer à BASE un partenariat autour de Génération Débrouille, et je cherche la
bonne personne à qui l'adresser. Est-ce Sandrine Decleer ? Si oui, pourriez-vous me communiquer son
adresse, ou lui transmettre ce message ?

Merci d'avance,

Corentin Dallenogare
Président, Falc'ohm System ASBL
contact@falcohmsystem.com · gazmatek.com · falcohmsystem.com

---

## Ce que ce texte fait, et pourquoi

1. **Il ne vend rien.** Le service presse n'est pas le décideur ; lui envoyer la proposition,
   c'est la perdre. On lui demande seulement un aiguillage.
2. **Il nomme Vanessa Zwaelens**, la porte-parole citée sous l'adresse : le message n'arrive pas
   à « Madame, Monsieur ».
3. **Il nomme Sandrine Decleer.** La question devient fermée (« est-ce elle ? »), ce qui se répond
   en une ligne, et montre qu'on sait déjà qui porte Génération Débrouille.
4. **Deux sorties possibles** : l'adresse, ou la transmission. L'une ou l'autre nous suffit.
5. **La prestation est mentionnée en une ligne**, sans détail : elle justifie le contact, elle
   n'est pas l'argument.
