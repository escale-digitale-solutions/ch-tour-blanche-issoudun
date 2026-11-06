# Publication GitHub Pages

Le dépôt public contient le projet complet du Centre Hospitalier de la Tour Blanche à Issoudun, dans sa version graphique lumineuse avec assistant documentaire local.

- `main` : sources Python, styles, scripts, images, polices, tests et site généré dans `dist/`.
- `gh-pages` : contenu de `dist/` publié à la racine, avec un fichier `.nojekyll`.
- GitHub Pages : publication depuis la branche `gh-pages`, dossier `/ (root)`.

## Mettre à jour

1. Modifier les sources sous `src/`.
2. Exécuter `python3 src/build.py`.
3. Exécuter `python3 -m unittest discover -s tests -p test_assistant_index.py` et `node tests/test_assistant_engine.js`.
4. Enregistrer les sources sur `main`, puis synchroniser le contenu de `dist/` vers la racine de `gh-pages`, en conservant `.nojekyll`.

Le site utilise des liens relatifs : les pages, les photos, la recherche et l’assistant restent utilisables sous le chemin du dépôt GitHub Pages. L’assistant n’utilise aucune clé API et sa base est régénérée lors du build.

Cette publication reste une proposition de refonte. Le site institutionnel actuel demeure distinct. Les sources visuelles et les limites de validation sont documentées dans `README.md` et `VALIDATION.md`.
