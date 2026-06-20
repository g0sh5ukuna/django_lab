# Django Lab

Outil local d'auto-apprentissage de Django : pas un tutoriel, un **vérificateur**.
L'apprenant code son projet dans `workspace/`, clique sur « Vérifier », et
voit immédiatement quelles étapes sont validées.

Spécification complète : [`cdc.md`](cdc.md). Avancement du développement :
[`suivi2dev.md`](suivi2dev.md).

## Démarrage rapide (formateur)

```
git clone <ce dépôt>
cd django_lab
./start.sh          # Linux/Mac
start.bat           # Windows
```

`start.sh`/`start.bat` créent le venv, installent les dépendances, appliquent
les migrations internes et démarrent l'UI sur **http://localhost:8000**.

## Pour l'apprenant : un second terminal

L'UI tourne sur `:8000`, mais l'apprenant code dans un **second terminal**,
dans `workspace/`. Ce terminal doit activer le même venv pour que `django-admin`
et `python manage.py` fonctionnent — c'est l'objet du Module 0
(`content/modules/00-installation.md`). Sans cette activation, rien ne marche
dès le Module 1 — voir `cdc.md` §12 si un apprenant bloque dessus.

## Structure

```
lab/                  ← code de l'outil (UI + moteur de validation), ne pas toucher
content/modules/       ← les 7 modules pédagogiques (.md), éditables sans toucher au code
workspace/              ← projet Django de l'apprenant — vidé entre deux sessions
start.sh / start.bat
requirements.txt
```

## Ajouter ou modifier un module

Un module = un fichier `.md` dans `content/modules/`, nommé `NN-slug.md`
(le tri alphabétique fixe l'ordre pédagogique). Frontmatter YAML + corps
Markdown :

```markdown
---
title: "Titre affiché"
description: "Sous-titre"
checks:
  - type: file_exists
    path: "workspace/manage.py"
    message: "Message affiché si ce check échoue"
---

## Explications
Du Markdown libre.

## Consignes
1. ...
```

Types de check disponibles : `file_exists`, `command_passes` (timeout 30s par
défaut), `contains_text`, `http_ok`, `test_passes`. Détail des paramètres :
`cdc.md` §7.

**Frontière de confiance** : `command_passes`/`test_passes` exécutent des
commandes shell définies dans le `.md`. Un module est donc du code de
confiance — toute contribution externe doit être relue ligne par ligne avant
merge (`cdc.md` §5.2).

Après modification d'un `.md`, redémarrer le serveur de l'outil (`Ctrl+C` puis
relancer `start.sh`) pour recharger.

## Avant une session avec un apprenant

- `workspace/` doit être vierge (seul `.gitkeep` dedans) — sinon les checks du
  Module 1 passeront à tort.
- Vérifier que `./start.sh` tourne et affiche bien `http://localhost:8000`.

## Le test qui compte

Ce dépôt a passé les Phases 0 à 3 du `suivi2dev.md` : le moteur, l'UI et les
7 modules fonctionnent, testés en conditions réelles par le développeur.
**Il n'a pas encore été testé par un apprenant réel** — c'est la Phase 4, le
seul test qui détermine si l'outil sert à quelque chose (grille GO/ADJUST/NO-GO
dans `cdc.md` §3).
