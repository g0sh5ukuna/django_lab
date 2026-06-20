---
title: "Module 1 — Créer le projet Django"
description: "Initialiser un projet Django fonctionnel dans workspace/"
checks:
  - type: file_exists
    path: "workspace/manage.py"
    message: "manage.py introuvable. As-tu lancé `django-admin startproject blog .` dans workspace/ ?"
  - type: file_exists
    path: "workspace/blog/settings.py"
    message: "workspace/blog/settings.py introuvable. Le nom du projet doit être `blog`."
  - type: command_passes
    cwd: "workspace"
    command: "python manage.py check"
    timeout: 30
    message: "`manage.py check` échoue. Lis l'erreur ci-dessous."
---

## Explications

Un projet Django est le conteneur de ton application : configuration,
URLs racine, point d'entrée `manage.py`. Une app (qu'on créera au Module 2)
vit à l'intérieur d'un projet.

## Consignes

**1.** Si ce n'est pas déjà fait (Module 0), active le venv et place-toi dans
`workspace/`.

**2.** Lance :

```
django-admin startproject blog .
```

Le `.` final compte : il dit à Django de créer le projet **ici**, sans
sous-dossier supplémentaire.

**3.** Vérifie que `manage.py` et `blog/settings.py` existent.

**4.** Reviens ici et clique sur « Vérifier ».
