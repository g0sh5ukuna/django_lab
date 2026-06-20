---
title: "Module 6 — Template liste"
description: "Afficher les articles dans un vrai template HTML"
checks:
  - type: file_exists
    path: "workspace/articles/templates/articles/article_list.html"
    message: "Template introuvable. Django cherche dans <app>/templates/<app>/."
  - type: contains_text
    path: "workspace/articles/templates/articles/article_list.html"
    text: "{% for"
    message: "Le template doit boucler sur les articles avec {% for article in articles %}."
  - type: http_ok
    url: "http://localhost:8001/articles/"
    expect_text: "Articles"
    message: "La page ne contient pas le texte 'Articles'. As-tu mis à jour la vue pour utiliser render() ?"
---

## Explications

Django cherche les templates dans `<app>/templates/<app>/<nom>.html` — le
dossier d'app répété deux fois évite les collisions de noms entre apps.

## Consignes

**1.** Crée `articles/templates/articles/article_list.html` :

```html
<h1>Articles</h1>
<ul>
{% for article in articles %}
  <li>{{ article.title }}</li>
{% endfor %}
</ul>
```

**2.** Reviens dans `articles/views.py` et repasse à `render()` (tu avais utilisé
`HttpResponse` au Module 5, c'était volontaire — l'étape suivante) :

```python
from django.shortcuts import render
from .models import Article

def article_list(request):
    articles = Article.objects.all()
    return render(request, "articles/article_list.html", {"articles": articles})
```

**3.** Le serveur du Module 5 (`runserver 8001`) recharge automatiquement quand
tu sauvegardes — pas besoin de le relancer (sauf si tu avais déjà visité
`/articles/` avec `render()` *avant* de créer le template : redémarre-le
dans ce cas, Django garde en cache la liste des templates au premier essai).

**4.** Reviens ici et clique sur « Vérifier ».

## Et après ?

Tu as maintenant le cycle complet : projet → app → modèle → migration →
vue/URL → template. Le Module 7 te montre ce que Django offre gratuitement
une fois ce cycle fait une première fois : une interface d'administration
pour gérer tes données sans écrire de vue.
