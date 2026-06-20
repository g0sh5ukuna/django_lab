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

### Ce que `startapp` crée

`python manage.py startapp articles` génère un dossier `articles/` avec
des fichiers vides, prêts à remplir :

- `models.py` — tes classes de données (Module 3)
- `views.py` — la logique qui répond à une requête (Module 5)
- `admin.py` — l'enregistrement dans l'interface d'admin (Module 7)
- `migrations/` — l'historique des changements de structure (Module 4)
- `apps.py` — la config de l'app elle-même, rarement modifié à ce stade

Remarque : `manage.py startapp` (pas `django-admin startapp`). Une fois
le projet créé, tu utilises toujours `manage.py` — il sait déjà quel
projet est concerné (`django-admin` tout seul ne le sait pas).

### Pourquoi `INSTALLED_APPS` n'est pas optionnel

Créer le dossier `articles/` ne suffit pas : Django ne regarde que les apps
listées dans `INSTALLED_APPS`. C'est volontaire, pas une formalité — ça
permet d'activer/désactiver une app sans la supprimer, et ça évite que
Django charge du code que tu n'as pas explicitement validé.

> **Piège fréquent** : oublier cette ligne ne fait pas planter `startapp`
> (le dossier existe, le code est valide) — l'erreur arrive plus tard, au
> Module 4, quand `makemigrations articles` refuse net avec
> `No installed app with label 'articles'`. Le message ne dit pas
> explicitement « va vérifier `INSTALLED_APPS` », donc si tu le croises,
> c'est la première chose à vérifier.

## Consignes

**1.** Dans `workspace/`, lance :

```
python manage.py startapp articles
```

**2.** Ouvre `blog/settings.py` et ajoute `"articles"` à la liste `INSTALLED_APPS`.

**3.** Reviens ici et clique sur « Vérifier ».
