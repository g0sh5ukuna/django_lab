# Django Lab — Suivi de développement

Référence : [`cdc.md`](cdc.md) v0.3.0
Méthode : arbre de problèmes — 1 étape = 1 action < 30 min, validée avant la suivante.
Pas de macroplanning par jours/sprints. Si une étape révèle une erreur de cadrage,
on recompose les étapes suivantes plutôt que de forcer le plan initial.

Légende : `[ ]` à faire · `[~]` en cours · `[x]` fait · `[!]` bloqué (raison notée)

---

## Phase 0 — Squelette technique

- [x] **0.1** Initialiser le dépôt `django-lab/` avec la structure de [§4 du CDC](cdc.md#4-architecture-générale) (dossiers vides : `lab/`, `content/modules/`, `workspace/`) — projet Django existant restructuré (`django_lab/` → `lab/lab/`), `manage.py check` OK
- [x] **0.2** Créer `requirements.txt` (Annexe A du CDC : django, pyyaml, requests, markdown) — Django 5.2 LTS (`<6.0`, pas la feature release 6.0), installé dans `venv/`, `pip freeze` vérifié
- [x] **0.3** Créer le projet Django `lab/` minimal (`django-admin startproject lab .` dans `lab/`), `settings.py` sans modèle custom — déjà fait en 0.1 (restructuration), `manage.py check` OK via `venv/`
- [x] **0.4** App `checker` créée et enregistrée dans `INSTALLED_APPS` — `manage.py check` OK
- [x] **0.5** `start.sh` : crée le venv, installe `requirements.txt`, crée `workspace/` si absent, migre, démarre `:8000` — testé à froid (venv supprimé puis recréé) : création venv + install + migrate + ✅ + runserver, tous OK.
- [x] **0.6** `start.bat` (équivalent Windows) écrit, miroir de `start.sh` — **non testé** (pas de machine Windows ici), à valider par un apprenant Windows en Phase 4

**Critère de passage Phase 0 → 1** : `./start.sh` lancé sur une machine vierge affiche « ✅ C'est prêt » sans erreur.

---

## Phase 1 — Moteur (loader + validateurs)

- [x] **1.1** `lab/loader.py` : dataclasses `Check` et `Module` (§5.1 du CDC)
- [x] **1.2** `load_modules()` : split frontmatter YAML / corps Markdown, `yaml.safe_load()`, erreur explicite si YAML mal formé — testé sur module factice (5 checks) + cas d'erreur (frontmatter absent → `ValueError` explicite)
- [x] **1.3** `lab/validators.py` : dataclass `CheckResult` + `run_check()` dispatch
- [x] **1.4** Implémenter les 5 types de check un par un, avec un test manuel par type :
  - [x] `file_exists` — succès + échec testés
  - [x] `command_passes` (timeout obligatoire, défaut 30s — §5.2) — succès, échec, timeout (1s sur `sleep 5`) testés
  - [x] `contains_text` — succès, texte absent, fichier absent testés
  - [x] `http_ok` (dépend de `requests`) — succès (200 + texte), texte absent, connexion refusée testés
  - [x] `test_passes` — succès et échec testés contre un `manage.py` factice (workspace/ réel pas encore créé, Phase 3)

**Critère de passage Phase 1 → 2** : un module `.md` factice avec un check de chaque type, exécuté en Python shell (sans UI), retourne les bons `CheckResult`.

---

## Phase 2 — UI Checker

- [x] **2.1** `checker/views.py` : `index()` → liste des modules
- [x] **2.2** `checker/views.py` : `module_detail()` → consigne (Markdown rendu) + bouton « Vérifier » (POST) + résultats
- [x] **2.3** Templates `base.html` / `index.html` / `module.html`, CSS embarqué, zéro JS (§5.3)
- [x] **2.4** Message vide si `content/modules/` ne contient aucun `.md` — testé via `Client()`, `GET /` → 200 + message affiché

**Critère de passage Phase 2 → 3** : navigation complète dans le navigateur, d'`index.html` à un module et retour, sans erreur 500.
✅ Validé via `Client()` Django (module factice temporaire, supprimé après test) : index liste le module → détail affiche les consignes Markdown rendues → POST « Vérifier » retourne des résultats mixtes (✅/❌) corrects → 404 propre sur slug inconnu.

---

## Phase 3 — Contenu (les 7 modules)

Rédaction des fichiers `.md` dans `content/modules/`, frontmatter + corps, un par un.
Chaque module est testé en conditions réelles (je code le projet fil rouge moi-même
en suivant la consigne, je vérifie que le check passe/échoue comme attendu).

- [ ] **3.0** `00-installation.md` — pas de check auto, juste les instructions (Module 0, §8)
- [ ] **3.1** `01-project-setup.md`
- [ ] **3.2** `02-start-app.md`
- [ ] **3.3** `03-model-article.md`
- [ ] **3.4** `04-migrations.md`
- [ ] **3.5** `05-view-url.md` (tester avec et sans `runserver 8001` actif pour valider le message d'erreur `http_ok`)
- [ ] **3.6** `06-template-list.md`

**Critère de passage Phase 3 → 4** : moi-même (ou une personne technique), en partant d'un dépôt vierge, je traverse les Modules 0 à 6 jusqu'à ✅ sur tous, sans lire le code de l'outil.

---

## Phase 4 — Validation Go/No-Go (le vrai test)

- [ ] **4.1** Trouver 1 apprenant réel correspondant au public cible (§2 du CDC : base Python, zéro Django)
- [ ] **4.2** Séance avec l'apprenant : Module 0 encadré, puis autonomie sur 1 à 6, noter chaque intervention formateur (quoi, à quel module, pourquoi)
- [ ] **4.3** Comparer au nombre d'interventions en formation classique sur le même parcours (référence à définir avant la séance, pas après)
- [ ] **4.4** Trancher : GO / ADJUST / NO-GO (grille exacte en §3 du CDC)

**Ceci est la porte de sortie du MVP.** Pas d'étape au-delà tant que 4.4 n'est pas GO ou ADJUST.

---

## Décisions ouvertes à trancher avant Phase 3 (pas avant, pas après)

Reprises du §11 du CDC — ne pas les laisser traîner jusqu'à la communication publique :

- [ ] Licence (MIT vs GPL/AGPL)
- [ ] Disponibilité du nom « Django Lab » (PyPI/GitHub/marques — à vérifier, pas supposer)

---

## Hors scope tant que la Phase 4 n'est pas GO

Tout le §10 du CDC (comptes utilisateurs, dashboard formateur, exécutable PyInstaller,
modules avancés, etc.) — ne pas anticiper.
