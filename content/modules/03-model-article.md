---
title: "Module 3 — Le modèle Article"
description: "Définir le modèle Article avec un titre et un contenu"
checks:
  - type: file_exists
    path: "workspace/articles/models.py"
    message: "workspace/articles/models.py introuvable."
  - type: contains_text
    path: "workspace/articles/models.py"
    text: "class Article"
    message: "Aucune classe `Article` trouvée dans models.py."
  - type: contains_text
    path: "workspace/articles/models.py"
    text: "title"
    message: "Le modèle Article n'a pas de champ `title`."
  - type: contains_text
    path: "workspace/articles/models.py"
    text: "content"
    message: "Le modèle Article n'a pas de champ `content`."
  - type: contains_text
    path: "workspace/articles/models.py"
    text: "def __str__"
    message: "Ajoute une méthode `__str__` à ton modèle (pratique pour le debug)."
---

## Explications

Un modèle Django décrit la structure d'une table en base de données. Chaque
attribut de classe devient une colonne.

> Ce check vérifie la présence du texte, pas la validité exacte du type de
> champ — c'est un filet de sécurité, pas un correcteur automatique. Une
> vérification plus fine (type de champ par introspection) arrivera en
> post-MVP.

## Consignes

1. Ouvre `articles/models.py`.
2. Crée une classe `Article` qui hérite de `models.Model`, avec au minimum :
   - `title` (un `CharField`)
   - `content` (un `TextField`)
3. Ajoute une méthode `__str__` qui retourne le titre (pratique pour
   l'admin et le debug).
4. Reviens ici et clique sur « Vérifier ».
