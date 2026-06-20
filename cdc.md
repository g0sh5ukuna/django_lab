# Django Lab — Cahier des charges MVP

**Version** : 0.3.0 (révision de la v0.2.0)
**Statut** : Brouillon cadré, prêt pour décision Go/No-Go
**Auteur** : Omi
**Date** : 2026-06-20

---

## ⚠️ Révisions v0.2 → v0.3 (à lire en premier)

Un trou du même type que les bugs corrigés en v0.1→v0.2 : non-bloquant sur le papier,
bloquant en pratique dès le Module 1.

| # | Changement | Pourquoi |
|---|---|---|
| 1 | **Module 0 détaillé (activation du venv)** | La v0.2 disait « les deux processus partagent le même venv » mais ne précisait jamais comment l'apprenant active ce venv dans **son propre terminal** (celui où il tape `django-admin startproject`, `manage.py startapp`, etc.). Sans ça, dès le Module 1 : `ModuleNotFoundError: No module named 'django'`. Module 0 ajouté en §8 avec la commande exacte par OS. |
| 2 | **Rappels d'activation dans les consignes Module 1 et Module 5** | Module 1 = première commande tapée par l'apprenant dans un terminal séparé de `start.sh`. Module 5 = ouverture d'un **second** terminal pour `runserver 8001`. Ce sont les deux points où l'activation peut être oubliée. |
| 3 | **Note sur la résolution de l'interpréteur Python** | `command_passes` invoque le littéral `"python"` — ajouté en §12 comme dépendance implicite sur l'environnement du process appelant. |

---

## ⚠️ Révisions v0.1 → v0.2

Cette version corrige trois problèmes techniques de la v0.1 qui auraient cassé l'outil
en pratique, plus quelques ajustements de cadrage. Rien n'est cosmétique.

| # | Changement | Pourquoi |
|---|---|---|
| 1 | **Les `checks` passent du corps Markdown au frontmatter YAML** | La v0.1 inventait un format `[checks]` custom dans le corps, avec un parser maison fragile (c'était son propre risque listé). Le frontmatter YAML est déjà parsé par PyYAML : zéro parser à écrire, zéro étape « retirer le bloc avant rendu ». **Le composant le plus risqué de la v0.1 disparaît.** |
| 2 | **Conflit de ports résolu** | La v0.1 lançait l'UI de l'outil ET demandait `GET /articles/` sur le **même** `localhost:8000`. Impossible : deux projets Django ne partagent pas un port. → Outil sur `:8000`, projet de l'apprenant sur `:8001`. |
| 3 | **Modèle venv / install clarifié** | La v0.1 ne disait pas où Django était installé. → Le workspace **partage le venv de l'outil**. Django est installé une fois via `requirements.txt`. L'apprenant ne fait aucun `pip install`. |
| 4 | **Frontière de sécurité documentée** | `command_passes` exécute des commandes shell déclarées dans les fichiers `.md`. C'est un **vecteur d'exécution de code arbitraire** si des modules viennent de contributeurs externes. Trust model explicité + `timeout` ajouté. |
| 5 | **Checks du Module 3 allégés** | Vérifier « hérite de `models.Model` » ou « champ de type `CharField` » par simple recherche de texte est trop fragile. Ces checks fins partent en post-MVP (`model_has_field` par introspection). Le MVP garde ce que `contains_text` vérifie honnêtement. |
| 6 | **Décisions ouvertes ajoutées** | Licence (MIT vs GPL) et disponibilité du nom « Django Lab » ne sont **pas tranchées** — listées en §11, pas inventées. |

---

## Table des matières

1. [Vision & objectifs](#1-vision--objectifs)
2. [Public cible & contexte](#2-public-cible--contexte)
3. [Périmètre MVP — ce qui est dedans / dehors](#3-périmètre-mvp)
4. [Architecture générale](#4-architecture-générale)
5. [Composants détaillés](#5-composants-détaillés)
6. [Format des modules `.md`](#6-format-des-modules-md)
7. [Types de checks disponibles](#7-types-de-checks-disponibles)
8. [Modules MVP (6 modules)](#8-modules-mvp-6-modules)
9. [Scénarios d'usage](#9-scénarios-dusage)
10. [Roadmap post-MVP](#10-roadmap-post-mvp)
11. [Décisions ouvertes (à trancher avant de coder)](#11-décisions-ouvertes)
12. [Contraintes & risques](#12-contraintes--risques)

---

## 1. Vision & objectifs

**Django Lab** est un outil local d'auto-apprentissage de Django.
Il ne *dispense* pas le cours — il **vérifie** que l'apprenant a correctement réalisé
chaque étape sur son propre projet.

### Différence clé avec un tutoriel

| Tutoriel classique | Django Lab |
|---|---|
| Te dit quoi taper | Te dit *si tu l'as bien fait* |
| Pas de feedback automatique | ✅ / ❌ immédiat |
| Ligne par ligne | Par étape validée |
| L'instructeur doit tout relire | L'instructeur n'intervient qu'en cas de ❌ bloquant |

### Objectifs du MVP

- **Valider le concept** via un critère unique et mesurable (l'OMTM, voir §3) :
  *un apprenant traverse-t-il les 6 modules avec moins d'intervention du formateur
  qu'en formation classique ?*
- **Limiter le scope** : un seul projet fil rouge (un blog), 6 étapes, aucun compte
  utilisateur, l'outil lui-même n'a aucun modèle de données.
- **Zéro configuration serveur** : tout tourne en local, hors-ligne une fois installé.

---

## 2. Public cible & contexte

| Élément | Description |
|---|---|
| **Public** | Aspirants développeurs juniors : **base Python acquise, zéro Django** |
| **Hors public** | Vrais débutants n'ayant jamais codé, et non-développeurs (entrepreneurs) — le parcours suppose qu'on sait ouvrir un terminal et lire une erreur Python |
| **Contexte géographique** | Bénin, connexion bas débit ou intermittente → tout doit fonctionner hors-ligne |
| **Prérequis apprenant** | Python 3.10+ installé, terminal, éditeur de code, notions Python |
| **Prérequis machine** | Python 3.10+, pip, ~500 Mo disque |
| **Mode d'installation** | Le formateur guide l'installation en séance 1 (Module 0, non chronométré) |

> 🔧 **Cadrage honnête** : le public a été resserré à « base Python, zéro Django ».
> La v0.1 disait « divers débutants » + « de A à Z », ce qui aurait imposé d'enseigner
> *aussi* Python, le terminal et Git — un scope de plusieurs mois de contenu. Hors MVP.

---

## 3. Périmètre MVP

### ✅ Inclus (le « Fer » — vital)

- 6 modules fil rouge (projet → app → modèle → migration → vue/URL → template)
- Moteur de validation avec 5 types de checks
- UI locale (liste des modules + page module + bouton « Vérifier » + résultats)
- Contenu en Markdown éditable par le formateur, sans toucher au code

### ❌ Hors scope v1 (le « Paille » — sacrifiable sans rien casser)

- Comptes utilisateurs / persistance de la progression
- Dashboard formateur multi-apprenants
- Exécutable packagé (PyInstaller)
- Modules avancés (auth, DRF, déploiement)
- Éditeur de code intégré, gamification, dark mode

### OMTM — la seule métrique qui prouve la valeur

> **Nombre d'interventions formateur nécessaires pour qu'un apprenant atteigne le Module 6.**
> Référence à battre : le nombre d'interventions en formation classique sur le même parcours.

### Gate Go/No-Go (à passer avec **1** apprenant réel avant d'écrire plus de modules)

- [ ] L'apprenant atteint le Module 6 avec **moins** d'interventions qu'en formation classique → **GO** (on ajoute des modules)
- [ ] Même charge d'intervention, mais l'apprenant dit gagner en autonomie → **ADJUST** (revoir les messages d'erreur)
- [ ] Pas de gain, ou l'install bloque tout le monde → **NO-GO** (l'outil n'aide pas, on arrête avant d'y mettre un mois)

---

## 4. Architecture générale

```
django-lab/                  ← Racine du dépôt (cloné par l'apprenant)
│
├── lab/                      ← Application Django de l'OUTIL (ne pas toucher)
│   ├── manage.py
│   ├── lab/
│   │   ├── settings.py       ← Config Django minimale, AUCUN modèle custom
│   │   ├── urls.py           ← Route racine → checker
│   │   └── wsgi.py
│   ├── checker/              ← App Django : l'interface de vérification
│   │   ├── views.py          ← index() et module_detail()
│   │   ├── urls.py
│   │   └── templates/checker/
│   │       ├── base.html     ← Layout, CSS embarqué (zéro build step)
│   │       ├── index.html    ← Liste des modules
│   │       └── module.html   ← Consigne + bouton "Vérifier" + résultats
│   ├── loader.py             ← Parse content/modules/*.md → objets Module
│   └── validators.py         ← Exécute les checks déclarés dans les .md
│
├── content/
│   └── modules/              ← LE contenu éditable (Markdown)
│       ├── 01-project-setup.md
│       ├── 02-start-app.md
│       ├── 03-model-article.md
│       ├── 04-migrations.md
│       ├── 05-view-url.md
│       └── 06-template-list.md
│
├── workspace/                ← L'apprenant code SON projet Django ICI (port 8001)
│   └── .gitkeep
│
├── start.sh                  ← Lancement Linux/Mac
├── start.bat                 ← Lancement Windows
├── requirements.txt
└── README.md
```

### Deux processus, deux ports (corrige le bug v0.1)

| Processus | Lancé par | Port | Rôle |
|---|---|---|---|
| UI de l'outil (`lab/`) | `start.sh` | `:8000` | Affiche les modules, exécute les checks |
| Projet de l'apprenant (`workspace/`) | l'apprenant, `manage.py runserver 8001` | `:8001` | Le blog en construction — ciblé par les checks `http_ok` |

> Les deux partagent **le même environnement virtuel**. Django est installé une seule
> fois via `requirements.txt`. L'apprenant ne fait jamais de `pip install`.

### Séparation des responsabilités

| Dossier | Responsabilité | Modifiable par l'apprenant ? |
|---|---|---|
| `lab/` | Code de l'outil (UI + validateur) | ❌ Non |
| `content/modules/` | Leçons en Markdown | ✅ Oui (le formateur) |
| `workspace/` | Projet Django de l'apprenant | ✅ Oui |

---

## 5. Composants détaillés

### 5.1. Loader (`lab/loader.py`)

**Rôle** : lire les `.md` de `content/modules/`, parser le frontmatter YAML
(métadonnées **et** checks), garder le corps Markdown pour l'affichage.

**Entrée** : répertoire `content/modules/`
**Sortie** : liste d'objets `Module`, triés par nom de fichier.

```python
@dataclass
class Check:
    type: str          # "file_exists" | "command_passes" | "http_ok" | "contains_text" | "test_passes"
    message: str       # Message d'erreur si échec
    params: dict       # Arguments selon le type (path, cwd, command, url, text, timeout…)

@dataclass
class Module:
    slug: str          # Nom du fichier sans extension
    title: str         # Titre affiché
    description: str    # Sous-titre
    content_md: str    # Corps Markdown (tout ce qui suit le frontmatter)
    checks: list[Check]
```

> 🔧 **Simplification majeure** : plus de parser custom. `load_modules()` sépare le
> frontmatter (entre les deux `---`), fait `yaml.safe_load()` dessus, lit `title`,
> `description`, `checks`. Le reste du fichier = `content_md`, rendu tel quel.

### 5.2. Validateurs (`lab/validators.py`)

**Rôle** : exécuter chaque check, retourner un résultat.

```python
@dataclass
class CheckResult:
    passed: bool
    message: str       # "✅ Fichier trouvé" / "❌ Fichier introuvable : ..."
    detail: str = ""   # stdout/stderr, affiché en <pre> si présent
```

`run_check(check) -> CheckResult` dispatche vers le validateur du bon type.
**Tous les chemins sont relatifs à la racine `django-lab/`.**

> 🔒 **Sécurité — frontière de confiance** : `command_passes` et `test_passes`
> exécutent des commandes arbitraires définies dans les fichiers `.md`. Un fichier
> module est donc **du code de confiance**, à traiter comme un script qu'on lance.
> Conséquences :
> - Les modules officiels sont écrits/relus par le formateur.
> - Une contribution externe (PR de module) doit être **relue ligne par ligne**
>   avant merge — au même titre que du code.
> - Tout check qui exécute un process a un `timeout` obligatoire (défaut 30 s) pour
>   éviter un blocage ou une boucle infinie.

### 5.3. UI Checker (`lab/checker/`)

**Technologie** : templates Django, CSS embarqué (pas de Tailwind, pas de build),
zéro JavaScript (form POST classique).

| Route | Template | Rôle |
|---|---|---|
| `/` | `index.html` | Liste les modules (cliquables) |
| `/module/<slug>/` | `module.html` | Consigne + bouton « Vérifier » + résultats |

- `index.html` : titre « 📚 Django Lab », cartes (titre + description), message vide
  « Ajoute des fichiers `.md` dans `content/modules/` » si aucun module.
- `module.html` : fil d'Ariane, contenu Markdown rendu, bouton « 🔍 Vérifier » (POST),
  résultats conditionnels — vert si tout passe, orange avec détail par check sinon,
  `detail` technique en `<pre>`.

### 5.4. Modules de contenu (`content/modules/`)

Un fichier = un module. Nommage `NN-titre-slug.md` (tri alphabétique = ordre pédagogique).
Format : frontmatter YAML (métadonnées + checks) suivi du corps Markdown.
Ajouter un module = créer un fichier + redémarrer le serveur. L'apprenant ne voit
jamais les checks (ils sont dans le frontmatter, jamais rendus).

### 5.5. Workspace (`workspace/`)

Répertoire où l'apprenant crée son projet Django. **L'outil le lit, ne le modifie jamais.**
L'apprenant organise son code librement tant que les checks passent.

### 5.6. Scripts de lancement (`start.sh` / `start.bat`)

Une seule commande qui :

1. crée le venv s'il n'existe pas, l'active ;
2. installe `requirements.txt` ;
3. crée `workspace/` s'il manque ;
4. applique les migrations Django internes (le checker n'a pas de modèle custom →
   seules les apps Django par défaut migrent, sur un fichier SQLite jetable `lab/db.sqlite3`) ;
5. démarre l'UI sur `localhost:8000` ;
6. affiche « ✅ C'est prêt — ouvre http://localhost:8000 ».

> 🔧 La v0.1 parlait de « SQLite en mémoire ». En pratique, une base en mémoire ne
> survit pas entre connexions avec `runserver`. Un fichier SQLite jetable est plus
> simple et suffisant — l'outil ne persiste rien d'important de toute façon.
> **Pas de Docker au MVP** : c'est un prérequis lourd pour le public visé.

---

## 6. Format des modules `.md`

### Spécification exacte (checks dans le frontmatter)

```markdown
---
title: "Créer le projet Django"
description: "Initialiser un projet Django fonctionnel dans workspace/"
checks:
  - type: file_exists
    path: "workspace/manage.py"
    message: "manage.py introuvable. As-tu lancé `django-admin startproject blog .` dans workspace/ ?"
  - type: command_passes
    cwd: "workspace"
    command: "python manage.py check"
    timeout: 30
    message: "`manage.py check` échoue. Lis l'erreur ci-dessous."
---

## Explications

Du Markdown libre : concepts, contexte, snippets de code.

## Consignes

1. Place-toi dans le dossier `workspace/`.
2. Lance `django-admin startproject blog .` (le `.` compte).
3. Reviens ici et clique sur « Vérifier ».
```

### Règles du frontmatter

- Délimité par deux lignes `---`.
- `title` et `description` : chaînes obligatoires.
- `checks` : liste YAML. Chaque check a **au minimum** `type` et `message` ; les autres
  clés dépendent du type (§7).
- Tout ce qui suit le second `---` est du Markdown affiché tel quel.
- Validation au chargement reportée en V0.2 du produit (cf. roadmap) ; au MVP, un YAML
  mal formé lève une erreur explicite au démarrage plutôt que silencieusement.

---

## 7. Types de checks disponibles

### MVP (v0.1.0 de l'outil)

| # | Type | Params | Exemple | Réussite si |
|---|---|---|---|---|
| 1 | `file_exists` | `path` | `path: "workspace/manage.py"` | le fichier/dossier existe |
| 2 | `command_passes` | `cwd`, `command`, `timeout?` | `command: "python manage.py check"` | code retour 0 |
| 3 | `http_ok` | `url`, `expect_text?` | `url: "http://localhost:8001/articles/"` | status 200 (+ texte présent si `expect_text`) |
| 4 | `contains_text` | `path`, `text` | `text: "class Article"` | texte/regex trouvé dans le fichier |
| 5 | `test_passes` | `cwd`, `test_path`, `timeout?` | `test_path: "articles"` | `manage.py test` passe |

> ⚠️ **`http_ok` exige que le serveur de l'apprenant tourne** (`runserver 8001` dans un
> second terminal). Les consignes des Modules 5 et 6 le rappellent explicitement.
> Limite connue : deux terminaux = friction pour un débutant. Alternative plus robuste
> (test client Django in-process, sans serveur à lancer) prévue en post-MVP.

### Post-MVP envisagés

| Type | Description |
|---|---|
| `model_has_field` | Champ d'un modèle (nom + type) **par introspection**, pas par regex |
| `migration_applied` | Une migration précise est appliquée |
| `admin_registered` | Un modèle est enregistré dans `admin.py` |
| `url_reverses` | Une URL nommée existe |
| `template_extends` | Un template étend un layout |

---

## 8. Modules MVP (6 modules)

Projet fil rouge : un **blog** (`blog`) avec une app **articles**.

### Module 0 — Installation & activation (non chronométré, encadré par le formateur)

**Objectif** : machine prête, et surtout — l'apprenant sait **comment activer le venv
partagé dans un terminal**, geste qu'il va répéter à chaque fois qu'il ouvre un nouveau
terminal pour travailler dans `workspace/`.

**Étapes** :
1. Cloner le dépôt, lancer `./start.sh` (Linux/Mac) ou `start.bat` (Windows) — crée le
   venv, installe `requirements.txt`, démarre l'UI sur `:8000`.
2. **Ouvrir un second terminal** (celui où l'apprenant codera dans `workspace/`) et
   activer le même venv :
   - Linux/Mac : `source venv/bin/activate`
   - Windows (PowerShell) : `venv\Scripts\Activate.ps1`
   - Windows (cmd) : `venv\Scripts\activate.bat`
3. Vérifier que ça a marché : `python -m django --version` doit afficher un numéro de
   version, pas `ModuleNotFoundError`.
4. `cd workspace`.

**Pas de check automatique pour ce module** (rien à valider côté outil — c'est un
prérequis d'environnement, pas une étape du projet fil rouge). Le formateur confirme
visuellement en séance 1 que l'étape 3 a réussi pour chaque apprenant avant de passer
au Module 1.

> 🔧 **Pourquoi ce module existe** : sans lui, l'apprenant tape les commandes du
> Module 1 dans un terminal où le venv n'est pas activé → `django-admin` ou
> `python manage.py` ne trouvent pas Django → échec immédiat, qui ressemble à une
> erreur de l'outil alors que c'est un oubli d'activation. Voir §12.

### Module 1 — Création du projet
**Objectif** : projet Django fonctionnel dans `workspace/`.
**Checks** : `workspace/manage.py` existe · `workspace/blog/settings.py` existe ·
`python manage.py check` passe (cwd `workspace`).

### Module 2 — Création de l'app
**Objectif** : app `articles` créée et enregistrée.
**Checks** : `workspace/articles/apps.py` existe · `articles` présent dans `INSTALLED_APPS`
(`contains_text` sur `settings.py`).

### Module 3 — Modèle Article
**Objectif** : un modèle `Article` avec `title` et `content`.
**Checks (MVP, allégés)** : `workspace/articles/models.py` existe ·
contient `class Article` · contient `title` · contient `content` · contient `def __str__`.

> 🔧 Les vérifications fines « hérite de `models.Model` », « `title` est un `CharField` »
> sont **retirées du MVP** : impossibles à vérifier fiablement par recherche de texte.
> Elles reviendront via `model_has_field` (introspection) en post-MVP. Assumé : au MVP,
> un check peut passer sur un code imparfait — c'est un filet, pas un correcteur.

### Module 4 — Migrations
**Objectif** : migrations créées et appliquées.
**Checks** : `workspace/articles/migrations/0001_initial.py` existe ·
`python manage.py migrate --check` passe (cwd `workspace`) · `manage.py check` passe.

### Module 5 — Vue + URL
**Objectif** : une vue qui liste les articles, accessible par URL.
**Checks** : `workspace/articles/views.py` existe · `workspace/articles/urls.py` existe ·
`blog/urls.py` inclut `articles.urls` (`contains_text`) ·
`http_ok` sur `http://localhost:8001/articles/`.
**Consigne** : rappeler que si c'est un **nouveau terminal**, il faut réactiver le venv
(Module 0, étape 2) avant de lancer `python manage.py runserver 8001`.

### Module 6 — Template liste
**Objectif** : un template HTML affichant la liste des articles.
**Checks** : `workspace/articles/templates/articles/article_list.html` existe ·
contient une boucle `{% for %}` (`contains_text`) ·
`http_ok` sur `http://localhost:8001/articles/` avec `expect_text: "Articles"`.

---

## 9. Scénarios d'usage

### Nominal — apprenant seul
Clone → `./start.sh` → ouvre `localhost:8000` → Module 1 → lit, code dans `workspace/`
→ « Vérifier » → ❌ un fichier manque → corrige → ✅ → Module 2 → … → Module 6.

### Intervention formateur
L'apprenant bloque (❌ persistant) → il envoie le message d'erreur exact → le formateur
voit *quel* check échoue, guide sur ce point précis → ✅ → suite.
**Économie** : le formateur ne relit pas les modules réussis ni tout le code.

### Ajout de module
Le formateur écrit `content/modules/07-forms.md` (frontmatter + checks) → commit/push →
l'apprenant pull, redémarre → le module 7 apparaît.

---

## 10. Roadmap post-MVP

- **V0.2 — Robustesse** : validation du frontmatter au chargement · timeouts gérés ·
  tests unitaires `loader`/`validators` · gestion workspace inexistant / Python absent.
- **V0.3 — Expérience apprenant** : barre de progression · sauvegarde locale · mode
  « indice avant solution » · dark mode.
  *Note : la « sauvegarde locale » via `localStorage` réintroduit du JavaScript, que le
  MVP exclut. À décider : fichier JSON local côté serveur (cohérent avec le zéro-JS) vs
  localStorage (impose du JS).*
- **V0.4 — Expérience formateur** : dashboard progression (réseau local) · export ·
  parcours personnalisés.
- **V1.0 — Distribution** : exécutable PyInstaller (Windows), pour supprimer le prérequis Python.
- **Au-delà** : autres frameworks (FastAPI, Flask) · modules avancés (auth, DRF,
  déploiement, tests) · éditeur intégré · gamification.

---

## 11. Décisions ouvertes

À trancher **avant** de communiquer publiquement / coder plus loin. Non inventées ici.

| Décision | Options | Note |
|---|---|---|
| **Licence open-source** | MIT (adoption max, forks peuvent fermer le code) · GPL/AGPL (force les forks à rester ouverts) | Choix structurant pour un outil pédagogique communautaire. |
| **Nom « Django Lab »** | à conserver / à changer | ⚠️ Non vérifié : je ne peux pas confirmer sans recherche que le nom est libre sur PyPI/GitHub/marques. À vérifier avant toute communication. |
| **Champ Auteur** | « Omi » (valeur du document source) | Conservé tel quel, non modifié. |
| **`http_ok` à deux terminaux** | garder au MVP · passer au test client in-process | Friction réelle pour débutant ; voir §7. |

---

## 12. Contraintes & risques

| Contrainte / Risque | Impact | Mitigation |
|---|---|---|
| Hors-ligne obligatoire | Pas de CDN ni d'appel externe dans l'UI | CSS embarqué, dépendances installées localement |
| Multi-OS | Windows/Mac/Linux | `start.sh` + `start.bat`, chemins via `pathlib.Path` |
| Public débutant | Cloner/installer reste un prérequis | Module 0 encadré par le formateur en séance 1 |
| **Exécution de code arbitraire via les modules** | Un module malveillant peut lancer n'importe quelle commande sur la machine de l'apprenant | Modules = code de confiance ; relecture obligatoire des PR ; `timeout` sur tout process (§5.2) |
| **`http_ok` requiert le serveur apprenant actif** | Check échoue si `runserver 8001` n'est pas lancé → faux négatif déroutant | Consignes explicites Modules 5-6 ; test client in-process en post-MVP |
| L'apprenant modifie `lab/` par erreur | Outil cassé | `.gitignore`, conventions claires, séparation physique |
| Checks non exhaustifs | Un check passe sur du code imparfait | Assumé : filet de sécurité, pas correcteur automatique |
| Pas de persistance | Progression perdue au redémarrage | Acceptable au MVP ; sauvegarde locale en V0.3 |
| **Venv non activé dans le terminal de l'apprenant** | `django-admin`/`manage.py` introuvables → échec dès le Module 1, lu comme un bug de l'outil | Module 0 explicite (§8) + rappel à chaque ouverture de nouveau terminal (Module 5) |
| `command_passes` invoque le littéral `"python"` | Résout vers le mauvais interpréteur si le process appelant n'a pas hérité du venv activé | Le checker tourne dans le process déjà activé par `start.sh` ; pas de check qui lance des commandes depuis un contexte externe au MVP |

---

## Annexe A — Dépendances

```text
django>=4.2     # Framework de l'UI de l'outil
pyyaml>=6.0     # Parser le frontmatter YAML (métadonnées + checks)
requests>=2.28  # Checks http_ok
markdown>=3.4   # Rendu Markdown → HTML
```

Taille estimée : < 50 Mo avec le venv.

## Annexe B — Glossaire

| Terme | Définition |
|---|---|
| Module | Une leçon = un fichier `.md` (frontmatter + corps) |
| Check | Une vérification automatisée déclarée dans le frontmatter |
| Workspace | Dossier où l'apprenant code son projet Django |
| Loader | Composant qui parse les `.md` en objets `Module` |
| Validateur | Composant qui exécute un check et retourne un `CheckResult` |
| Frontmatter | Bloc YAML en tête de fichier `.md`, entre `---` |
| OMTM | *One Metric That Matters* — ici : interventions formateur jusqu'au Module 6 |