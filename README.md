# Centre Hospitalier de la Tour Blanche — seconde version

Refonte multipage fondée sur le ZIP fourni `ch-tour-blanche-maquette.zip`. Cette version possède son propre projet et son propre dépôt. Le premier site est conservé.

## Construire

```sh
python3 src/build.py
```

Le résultat est généré dans `dist/` (69 pages). Aucune dépendance Python externe ni bibliothèque JavaScript n’est nécessaire. Le répertoire généré peut être hébergé sur un serveur statique ; les liens fonctionnent aussi en ouvrant les fichiers localement.

## Modifier

- `src/core.py` : navigation, en-tête, pied de page et gabarits.
- `src/home_v2.py` : nouvel accueil.
- `src/pages.py` et `src/services.py` : contenu du site fourni.
- `src/assets/site.css` : système graphique et responsive.
- `src/assets/warm.css` : palette lumineuse, compositions photographiques et déclinaisons sur les pages intérieures.
- `src/assets/site.js` : recherche, filtres, liste de préparation, confort de lecture et orientation contact.
- `src/assets/images` : logo authentique et photographies de l’établissement.

La version de présentation est partageable par lien et non indexable. Le contact oriente vers des coordonnées réelles ; aucun formulaire ne prétend envoyer un message. Les rendez-vous passent par les secrétariats. Aucun dossier patient ni paiement n’est collecté.

## Sources des visuels

Visuels d’origine de l’établissement, conservés sans génération artificielle :

- Logo : https://www.ch-issoudun.fr/wp-content/uploads/2021/12/logo_issoudun.jpg
- Façade : https://www.ch-issoudun.fr/wp-content/uploads/2021/12/DSC5276-copie-1024x684.jpg
- Jardins : https://www.ch-issoudun.fr/wp-content/uploads/2021/12/DSC4824-1024x684.jpg
- Bâtiments : https://www.ch-issoudun.fr/wp-content/uploads/2022/04/DSC3930-1024x681.jpg
- Équipes à la semaine de l’éducation thérapeutique, événement du 5 février 2026 : https://www.ch-issoudun.fr/wp-content/uploads/2026/02/01f69d30-2366-4748-8966-885900f4705c-scaled.jpg — article https://www.ch-issoudun.fr/semaine-etp/ (11 février 2026).
- Sorties en vélo adapté : https://www.ch-issoudun.fr/wp-content/uploads/2026/04/6e3f6f4c-4f25-495e-b2f8-406aaa5bd421-scaled.jpg — article https://www.ch-issoudun.fr/sorties-velo-ehpad/ (20 avril 2026).

Ces fichiers correspondent aux originaux récupérés sur le site institutionnel lors de l’audit et de la révision graphique. Le contexte de la photo d’accueil est indiqué dans sa légende.

## Passage au domaine officiel

Faire valider les contenus, les coordonnées, les droits des visuels, les mentions légales et l’accessibilité par l’établissement ; définir le circuit éditorial. Retirer ensuite la mention de proposition et le blocage d’indexation. La présente publication n’effectue aucun changement sur le domaine de l’hôpital.

## Assistant documentaire sans API

Le bouton « Une question ? » est présent sur les69 pages. Le moteur utilise exclusivement le contenu des68 pages utiles (page404 exclue), sans API, modèle externe ou envoi des questions. L’index `dist/assets/assistant-index.json` est régénéré automatiquement par `src/build.py` et téléchargé à chaque ouverture de l’assistant.

- `src/assistant_index.py` extrait les paragraphes, listes, définitions et tableaux et ajoute les ancres de source.
- `src/assets/assistant-engine.js` classe les extraits, reconnaît des synonymes, des variantes et quelques fautes, et applique des règles de sélection pour les démarches fréquentes.
- `src/assets/assistant-ui.js` et `assistant.css` constituent l’interface sur toutes les pages.
- Aucune conversation n’est persistée. Les réponses citent des passages ; une question incertaine déclenche une demande de précision ou une réponse d’absence d’information.
- Les contenus de PDF et de sites externes liés ne sont pas analysés. Leurs liens restent disponibles dans les pages documentaires. Les informations du site officiel ne sont pas surveillées à distance : la base reflète les sources du présent site au dernier build.

Vérification : `python -m unittest discover -s tests -p 'test_assistant_index.py'` puis `node tests/test_assistant_engine.js` après le build.
