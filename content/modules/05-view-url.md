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
  - type: file_exists
    path: "workspace/articles/sorting.py"
    message: "Crée workspace/articles/sorting.py avec la fonction sort_titles (voir l'exercice interactif ci-dessous)."
  - type: test_passes
    cwd: "workspace"
    test_path: "articles"
    timeout: 30
    message: "Les tests de articles/tests.py ne passent pas. Lis le détail ci-dessous."
---

## Explications

Une vue Django reçoit une requête et retourne une réponse. Une URL relie un
chemin (`/articles/`) à une vue. On regroupe les URLs d'une app dans son
propre `urls.py`, puis on les inclut depuis `blog/urls.py`.

> On commence par une réponse simple, sans template — un template HTML
> arrive au Module 6. Inutile de mélanger « le routage marche » et
> « le rendu HTML marche » dans la même étape.

### `objects.all()` ne renvoie pas une liste

`Article.objects.all()` renvoie un `QuerySet` — pas une liste Python, même
si on peut le parcourir comme une liste (`for`, `len()`, indexation). La
différence compte : un `QuerySet` est **paresseux** (il ne touche la base
qu'au moment où tu l'utilises réellement, pas à sa création) et il a ses
propres méthodes (`.filter()`, `.order_by()`, `.count()`...). L'exercice
plus bas convertit volontairement un `QuerySet` en vraie liste Python
(`sorted(...)` renvoie une `list`), pour que tu voies la différence.

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

## Exercice interactif — trier de vraies données

**5.** Crée `articles/sorting.py` avec cette fonction :

```python
def sort_titles(articles):
    """Retourne les titres des articles, triés par ordre alphabétique."""
    return sorted(article.title for article in articles)
```

**6.** Ajoute cette classe de test dans `articles/tests.py`, **sous** la
classe `ValidatorsTests` du Module 3 (ne la supprime pas — les deux
classes de test coexistent dans le même fichier) :

```python
from .sorting import sort_titles


class SortingTests(TestCase):
    def test_sorts_titles_alphabetically(self):
        Article.objects.create(title="Zebre", content="...")
        Article.objects.create(title="Abeille", content="...")
        self.assertEqual(sort_titles(Article.objects.all()), ["Abeille", "Zebre"])

    def test_empty_queryset_returns_empty_list(self):
        self.assertEqual(sort_titles(Article.objects.none()), [])
```

Il te faut aussi `from .models import Article` en haut du fichier si ce
n'est pas déjà là depuis le Module 3.

**7.** Reviens ici et clique sur « Vérifier ».
