---
title: "Module 4 — Migrations"
description: "Générer et appliquer la migration du modèle Article"
checks:
  - type: file_exists
    path: "workspace/articles/migrations/0001_initial.py"
    message: "Migration introuvable. As-tu lancé `python manage.py makemigrations articles` ?"
  - type: command_passes
    cwd: "workspace"
    command: "python manage.py migrate --check"
    timeout: 30
    message: "Des migrations ne sont pas appliquées. Lance `python manage.py migrate`."
  - type: command_passes
    cwd: "workspace"
    command: "python manage.py check"
    timeout: 30
    message: "`manage.py check` échoue. Lis l'erreur ci-dessous."
---

## Explications

Une migration traduit ton modèle Python en instructions SQL. Il y a deux
étapes distinctes :
- **créer** la migration (`makemigrations`) : Django compare tes modèles à
  l'état précédent et génère le fichier de migration ;
- **l'appliquer** (`migrate`) : Django exécute le SQL correspondant sur la
  base de données.

## Consignes

**1.** Dans `workspace/`, génère la migration :

```
python manage.py makemigrations articles
```

**2.** Applique-la :

```
python manage.py migrate
```

**3.** Reviens ici et clique sur « Vérifier ».
