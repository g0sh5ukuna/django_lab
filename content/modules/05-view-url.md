---
title: "Module 5 — Vue et URL"
description: "Afficher la liste des articles via une vue accessible par URL"
checks:
  - type: file_exists
    path: "workspace/articles/views.py"
    message: "workspace/articles/views.py introuvable."
  - type: file_exists
    path: "workspace/articles/urls.py"
    message: "Crée workspace/articles/urls.py (il n'est pas généré automatiquement par startapp)."
  - type: contains_text
    path: "workspace/blog/urls.py"
    text: "articles.urls"
    message: "blog/urls.py n'inclut pas articles.urls. Utilise `include('articles.urls')`."
  - type: http_ok
    url: "http://localhost:8001/articles/"
    message: "http://localhost:8001/articles/ ne répond pas. As-tu lancé `python manage.py runserver 8001` dans un terminal séparé ?"
---

## Explications

Une vue Django reçoit une requête et retourne une réponse. Une URL relie un
chemin (`/articles/`) à une vue. On regroupe les URLs d'une app dans son
propre `urls.py`, puis on les inclut depuis `blog/urls.py`.

> On commence par une réponse simple, sans template — un template HTML
> arrive au Module 6. Inutile de mélanger « le routage marche » et
> « le rendu HTML marche » dans la même étape.

## Consignes

**1.** Dans `articles/views.py`, écris une vue qui retourne le nombre d'articles
(pas encore de template — ça vient au Module 6) :

```python
from django.http import HttpResponse
from .models import Article

def article_list(request):
    articles = Article.objects.all()
    return HttpResponse(f"{articles.count()} article(s)")
```

**2.** Crée `articles/urls.py` :

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.article_list, name="article_list"),
]
```

**3.** Dans `blog/urls.py`, ajoute `include` à l'import existant et la ligne
`articles/` à `urlpatterns` (ne supprime pas la ligne `admin/`) :

```python
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("articles/", include("articles.urls")),
]
```

**4.** **Important — nouveau terminal** : ouvre un troisième terminal,
réactive le venv (Module 0, étape 2), `cd workspace`, puis lance :

```
python manage.py runserver 8001
```

Laisse-le tourner. C'est ce serveur que le check `http_ok` va appeler.

**5.** Reviens ici et clique sur « Vérifier ».
