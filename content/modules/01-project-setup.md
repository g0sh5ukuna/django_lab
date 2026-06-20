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

### Projet vs app — la distinction qui sert pour tout le reste

Un **projet** Django est le conteneur : configuration globale (`settings.py`),
routage racine (`urls.py`), point d'entrée (`manage.py`). Une **app** (Module 2)
est un module qui vit à l'intérieur d'un projet et gère une fonctionnalité
précise. Un projet peut contenir plusieurs apps ; une app peut, en théorie,
être réutilisée dans un autre projet. Retiens juste : *le projet sait où
sont les choses, l'app sait comment une chose marche.*

### Ce que `django-admin startproject blog .` crée réellement

- `manage.py` — point d'entrée de toutes tes commandes (`runserver`,
  `migrate`, `makemigrations`...). Il configure l'environnement Django puis
  délègue à la commande demandée.
- `blog/settings.py` — toute la configuration : base de données, apps
  installées, fuseau horaire, etc.
- `blog/urls.py` — la table de routage racine : quelle URL va vers quel
  bout de code.
- `blog/wsgi.py` / `blog/asgi.py` — le point d'entrée pour un vrai serveur
  de production (pas utilisé en développement, `runserver` s'en charge).

### Le `.` final n'est pas cosmétique

`django-admin startproject blog` (sans le point) crée un dossier `blog/`
**contenant** `manage.py` et un sous-dossier `blog/` — un niveau
d'imbrication en trop. `django-admin startproject blog .` dit à Django
« utilise le dossier courant comme racine » : `manage.py` atterrit
directement dans `workspace/`. C'est ce que les checks de ce module
attendent — si tu as oublié le point, `workspace/manage.py` n'existera pas,
il sera un niveau plus bas.

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
