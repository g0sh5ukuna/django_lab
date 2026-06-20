---
title: "Module 8 — À toi de jouer : l'app categories"
description: "Refais le cycle complet (app → modèle → migration → vue → template) sans aide pas-à-pas"
checks:
  - type: file_exists
    path: "workspace/categories/apps.py"
    message: "L'app categories n'existe pas. `python manage.py startapp categories`."
  - type: contains_text
    path: "workspace/blog/settings.py"
    text: "categories"
    message: "categories n'est pas dans INSTALLED_APPS."
  - type: file_exists
    path: "workspace/categories/models.py"
    message: "categories/models.py introuvable."
  - type: contains_text
    path: "workspace/categories/models.py"
    text: "class Category"
    message: "Aucune classe Category dans models.py."
  - type: contains_text
    path: "workspace/categories/models.py"
    text: "name"
    message: "Le modèle Category n'a pas de champ name."
  - type: contains_text
    path: "workspace/categories/models.py"
    text: "def __str__"
    message: "Ajoute une méthode __str__ à Category."
  - type: file_exists
    path: "workspace/categories/migrations/0001_initial.py"
    message: "Migration introuvable. `python manage.py makemigrations categories`."
  - type: command_passes
    cwd: "workspace"
    command: "python manage.py migrate --check"
    timeout: 30
    message: "Des migrations ne sont pas appliquées. `python manage.py migrate`."
  - type: file_exists
    path: "workspace/categories/views.py"
    message: "categories/views.py introuvable."
  - type: file_exists
    path: "workspace/categories/urls.py"
    message: "categories/urls.py introuvable (pas généré automatiquement par startapp)."
  - type: contains_text
    path: "workspace/blog/urls.py"
    text: "categories.urls"
    message: "blog/urls.py n'inclut pas categories.urls."
  - type: http_ok
    url: "http://localhost:8001/categories/"
    message: "http://localhost:8001/categories/ ne répond pas. Vérifie la vue, l'URL, et que runserver 8001 tourne."
  - type: file_exists
    path: "workspace/categories/templates/categories/category_list.html"
    message: "Template introuvable. Django cherche dans <app>/templates/<app>/."
  - type: contains_text
    path: "workspace/categories/templates/categories/category_list.html"
    text: "{% for"
    message: "Le template doit boucler sur les catégories avec {% for %}."
  - type: http_ok
    url: "http://localhost:8001/categories/"
    expect_text: "Categories"
    message: "La page ne contient pas le mot Categories — vérifie que la vue utilise render() avec le bon template."
---

## Pas de code fourni, cette fois

Tu as fait ce cycle six fois (Modules 1 à 6) sur l'app `articles`. Cette
fois, la checklist seulement — si tu bloques sur une étape précise, le
module correspondant (numéros 1 à 6 dans la sidebar) a le détail complet.

## Ta mission : l'app `categories`

Crée une deuxième app, `categories`, avec un modèle `Category` (un seul
champ texte : `name`), et reproduis tout le cycle, de zéro :

1. **App** — crée l'app `categories`, enregistre-la dans `INSTALLED_APPS`.
2. **Modèle** — une classe `Category` avec un champ `name` et une méthode
   `__str__` qui retourne le nom.
3. **Migration** — génère-la, applique-la.
4. **Vue + URL** — une vue qui liste les catégories, montée sur
   `/categories/` depuis `blog/urls.py`. `runserver 8001` doit tourner
   pour que les checks `http_ok` passent.
5. **Template** — boucle sur les catégories, affiche le mot « Categories »
   quelque part sur la page (un `<h1>`, par exemple).

### Carte mémoire (pas un copier-coller)

- Créer une app : `python manage.py startapp <nom>`
- Un champ texte court : `models.CharField(max_length=100)`
- Générer puis appliquer une migration : `makemigrations <app>` · `migrate`
- Inclure les URLs d'une app : `include("<app>.urls")` dans `blog/urls.py`
- Emplacement d'un template : `<app>/templates/<app>/<nom>.html`

## Vérifie

Clique sur « Vérifier » une fois les 5 étapes faites — tous les checks
tournent d'un coup, comme un vrai contrôle final.

> **Dépannage** — si la page `/categories/` affiche `TemplateDoesNotExist`
> alors que tu es sûr que ton fichier existe au bon endroit : Django met en
> cache la liste des dossiers de templates au premier essai. Si tu as
> testé l'URL *avant* de créer le template, le serveur garde ce cache même
> après. Solution : arrête `runserver 8001` (Ctrl+C) et relance-le.
