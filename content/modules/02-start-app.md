---
title: "Module 2 — Créer l'app articles"
description: "Créer une app Django et l'enregistrer dans le projet"
checks:
  - type: file_exists
    path: "workspace/articles/apps.py"
    message: "workspace/articles/apps.py introuvable. As-tu lancé `python manage.py startapp articles` ?"
  - type: contains_text
    path: "workspace/blog/settings.py"
    text: "articles"
    message: "`articles` n'apparaît pas dans INSTALLED_APPS de blog/settings.py."
---

## Explications

Un projet Django est composé d'« apps » : chacune gère une fonctionnalité
(ici, la gestion des articles du blog). Une app doit être déclarée dans
`INSTALLED_APPS` pour que Django la prenne en compte.

## Consignes

1. Dans `workspace/`, lance :

   ```
   python manage.py startapp articles
   ```

2. Ouvre `blog/settings.py` et ajoute `"articles"` à la liste `INSTALLED_APPS`.
3. Reviens ici et clique sur « Vérifier ».
