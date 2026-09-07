**Objet :** Une question, une ligne de réponse

Bonjour {{CONTACT_NAME}},

Plutôt qu'un long dossier, une question directe.

Nous fabriquons nos enceintes et nous cherchons un partenaire {{MODULE}} sur plusieurs années,
pas une commande ponctuelle. La demande tient en une phrase : {{DEMANDE_EN_UNE_PHRASE}}.

Est-ce le genre de démarche que {{COMPANY}} peut examiner, ou faut-il que je m'adresse à
quelqu'un d'autre chez vous ? Un oui, un non ou un nom suffisent, et je m'adapte.

Bien à vous,
{{SENDER}}, {{ORG}}

---

## Règles

Ce gabarit s'appelait autrefois « demande de rendez-vous » et proposait un échange de vingt
minutes. **On ne propose plus jamais d'appel, de visio ni de rendez-vous** (`CLAUDE.md`).

Demander du temps à un inconnu est la demande la plus coûteuse d'un premier message, et celle qui
fait le moins avancer. Une question fermée obtient une réponse. Une proposition d'appel obtient un
silence poli, et on ne saura jamais si c'était un refus ou un agenda plein.

Si l'entreprise propose elle-même un appel, c'est différent : on accepte, évidemment. Ce qui est
banni, c'est de le proposer en premier.

- `{{DEMANDE_EN_UNE_PHRASE}}` : la demande telle qu'on la dirait à voix haute, tirée de
  `ask.detail` de la fiche CRM. Vérifier d'abord dans `data/existing-suppliers.yaml` que le poste
  n'est pas déjà couvert.
- Toujours une personne nommée. Jamais `info@`.
- Relance à J+10, puis J+30. Trois contacts maximum.
