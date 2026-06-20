---
title: "Module 7 — L'admin Django"
description: "Découvrir l'interface d'administration générée automatiquement par Django"
checks:
  - type: contains_text
    path: "workspace/articles/admin.py"
    text: "from .models import Article"
    message: "admin.py doit importer Article : `from .models import Article`."
  - type: contains_text
    path: "workspace/articles/admin.py"
    text: "admin.site.register(Article)"
    message: "Article n'est pas enregistré dans l'admin : `admin.site.register(Article)`."
  - type: command_passes
    cwd: "workspace"
    command: "python manage.py check"
    timeout: 30
    message: "`manage.py check` échoue — Django charge admin.py au démarrage, une erreur dedans (import oublié, faute de frappe) casse tout le projet."
  - type: http_ok
    url: "http://localhost:8001/admin/"
    expect_text: "Django administration"
    message: "http://localhost:8001/admin/ ne répond pas. As-tu `python manage.py runserver 8001` actif dans son terminal ?"
---

## Explications

### Ce que l'admin fait pour toi

Django regarde tes modèles et te génère une interface web complète pour les
gérer — créer, lire, modifier, supprimer — sans que tu écrives la moindre
vue ni le moindre template. Aux Modules 5 et 6, tu as construit à la main
une page qui *affiche* les articles ; l'admin fait ça automatiquement, et
bien plus (créer, modifier, supprimer), pour n'importe quel modèle que tu
lui désignes.

### Pourquoi il faut « enregistrer » un modèle

Par défaut, l'admin ne connaît aucun de tes modèles. Tu dois dire
explicitement à Django lesquels administrer — c'est volontaire : tu ne veux
pas qu'un modèle interne devienne modifiable depuis une URL web sans que tu
l'aies décidé toi-même.

## Consignes

**1.** Ouvre `articles/admin.py`.

**2.** Importe ton modèle et enregistre-le :

```python
from django.contrib import admin

from .models import Article

admin.site.register(Article)
```

**3.** Crée un compte administrateur (une seule fois pour tout le projet) :

```
python manage.py createsuperuser
```

Réponds aux questions (nom d'utilisateur, email optionnel, mot de
passe). Retiens ces identifiants — l'outil ne les voit jamais et ne
peut pas te les rappeler.

**4.** Avec `runserver 8001` toujours actif (Module 5), ouvre
`http://localhost:8001/admin/` dans ton navigateur, connecte-toi, et
vérifie que **Articles** apparaît — tu peux en créer un directement
depuis cette interface.

**5.** Reviens ici et clique sur « Vérifier ».

> Le check ne peut pas vérifier que tu t'es connecté avec succès (ton mot
> de passe n'est jamais transmis à l'outil, par sécurité) — il vérifie que
> la route `/admin/` répond et que `Article` est bien enregistré. La
> vraie preuve, c'est de voir « Articles » dans l'interface toi-même.
