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

Une migration traduit ton modèle Python en instructions de base de données.
Il y a deux étapes distinctes, et la différence compte :

- **créer** la migration (`makemigrations`) : Django compare tes modèles à
  l'état précédent (déduit des migrations existantes) et génère un
  **fichier Python** qui décrit le changement — pas du SQL brut, des
  instructions (`CreateModel`, `AddField`...) que Django traduira selon
  ta base de données.
- **l'appliquer** (`migrate`) : Django exécute ces instructions sur la
  base réelle.

### Le check `migrate --check` ne fait qu'une seule chose

Il vérifie qu'il n'existe pas de migration **déjà créée mais pas encore
appliquée** — autrement dit, qu'il ne te manque pas un `migrate`. Il ne
vérifie **pas** que tes modèles correspondent à tes migrations : si tu
modifies `models.py` sans relancer `makemigrations`, ni ce check ni
`manage.py check` ne le verront — `migrate --check` continuera de dire
« tout est appliqué », simplement parce qu'il ne connaît pas le changement
que tu n'as pas encore traduit en migration.

> **Retiens-le comme deux questions différentes** : *« ai-je traduit mon
> modèle en migration ? »* (`makemigrations`) et *« ai-je appliqué cette
> traduction à la base ? »* (`migrate`). Une seule des deux est vérifiée
> automatiquement ici — l'autre, c'est à toi d'y penser à chaque fois que
> tu touches `models.py`.

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
