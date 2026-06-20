---
title: "Module 3 — Le modèle Article"
description: "Définir le modèle Article, puis prouver que sa logique marche avec de vrais tests"
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
    message: "Ajoute une méthode `__str__` à ton modèle (pratique pour le debug et l'admin)."
  - type: file_exists
    path: "workspace/articles/validators.py"
    message: "Crée workspace/articles/validators.py avec les fonctions is_valid_title et is_valid_content (voir l'exercice interactif ci-dessous)."
  - type: test_passes
    cwd: "workspace"
    test_path: "articles"
    timeout: 30
    message: "Les tests de articles/tests.py ne passent pas (ou n'existent pas encore). Lis le détail ci-dessous pour voir quelle fonction corriger."
---

## Explications

### Qu'est-ce qu'un modèle ?

Un modèle Django est une classe Python qui décrit une table de base de
données. Chaque **attribut de classe** devient une **colonne**, chaque
**instance** de la classe devient une **ligne**.

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
```

Cette seule ligne dit à Django : « crée une colonne `title`, de type texte
court, qui ne dépasse pas 200 caractères ». Au Module 4, tu traduiras ça en
vraie table SQL avec une migration — pas avant : Django sépare toujours
*décrire* la structure (le modèle) et *l'appliquer* en base (la migration).

### `CharField` vs `TextField` — le piège classique

- `CharField` : texte **court**, longueur **obligatoirement** limitée par
  `max_length`. Pour un titre, un nom, un slug.
- `TextField` : texte **long**, sans limite imposée. Pour un corps
  d'article, une description.

Confondre les deux ne fait planter ni Django ni ton check — c'est le genre
de bug qu'on ne voit qu'en production, quand un vrai utilisateur colle un
roman dans un champ censé rester court.

> Les checks `contains_text` ci-dessus vérifient la présence du texte, pas
> le type exact du champ — c'est un filet de sécurité, pas un correcteur
> automatique. L'exercice interactif plus bas, lui, vérifie un vrai
> comportement.

## Consignes — le modèle

1. Ouvre `articles/models.py`.
2. Crée une classe `Article` qui hérite de `models.Model`, avec :
   - `title` (un `CharField`, `max_length=200`)
   - `content` (un `TextField`)
3. Ajoute une méthode `__str__` qui retourne le titre.

## Exercice interactif — prouve que ta logique marche

Un check qui cherche juste le mot `title` dans ton fichier ne sait pas si
une fonction *fait* ce qu'elle doit faire. Pour vérifier un vrai
comportement, il faut un vrai test — celui que tu vas écrire ici sert pour
le reste du projet (Module 5 pourra réutiliser `is_valid_title`).

**1.** Crée `articles/validators.py` avec ces deux fonctions :

```python
def is_valid_title(title):
    """True si le titre n'est ni vide ni trop long (max 200 caractères)."""
    return 0 < len(title) <= 200


def is_valid_content(content):
    """True si le contenu n'est pas vide."""
    return len(content) > 0
```

**2.** Colle ce test (fourni, ne l'invente pas) dans `articles/tests.py` :

```python
from django.test import TestCase

from .validators import is_valid_content, is_valid_title


class ValidatorsTests(TestCase):
    def test_normal_title_is_valid(self):
        self.assertTrue(is_valid_title("Mon premier article"))

    def test_empty_title_is_invalid(self):
        self.assertFalse(is_valid_title(""))

    def test_too_long_title_is_invalid(self):
        self.assertFalse(is_valid_title("x" * 201))

    def test_normal_content_is_valid(self):
        self.assertTrue(is_valid_content("Un peu de texte."))

    def test_empty_content_is_invalid(self):
        self.assertFalse(is_valid_content(""))
```

**3.** Lance `python manage.py test articles` toi-même dans ton terminal —
c'est plus rapide que de cliquer sur « Vérifier » à chaque essai pendant
que tu corriges.

**4.** Quand `OK` s'affiche dans ton terminal, reviens ici et clique sur
« Vérifier ».
