# Django Lab

**Apprends Django en le faisant, pas en le lisant.**

Django Lab n'est pas un tutoriel de plus — c'est un **vérificateur**. Tu
codes un vrai projet Django, étape par étape, dans ton propre éditeur et ton
propre terminal. À chaque étape, tu cliques sur « Vérifier » et l'outil te
dit précisément ce qui marche et ce qui bloque, avec un message d'erreur
qui pointe vers la correction — pas juste "❌".

Pas de compte à créer, pas de cloud, pas d'abonnement. Tout tourne en local,
hors-ligne une fois installé.

## Pourquoi ça existe

| Tutoriel classique | Django Lab |
|---|---|
| Te dit quoi taper | Te dit *si tu l'as bien fait* |
| Pas de feedback automatique | ✅ / ❌ immédiat, avec le détail technique |
| Tu avances en espérant avoir bon | Un check qui passe = une preuve, pas une impression |

## Démarrage rapide

```
git clone https://github.com/g0sh5ukuna/django_lab.git
cd django_lab
./start.sh          # Linux / Mac
start.bat           # Windows
```

`start.sh` / `start.bat` créent un environnement virtuel Python, installent
les dépendances, appliquent les migrations internes et démarrent l'outil sur
**http://localhost:8000**. La toute première étape (Module 0, dans l'outil)
t'explique comment activer ce même environnement dans un second terminal,
celui où tu coderas ton projet — c'est la seule manipulation à comprendre
avant de commencer.

**Prérequis** : Python 3.10+, des notions de Python (variables, fonctions,
classes), savoir ouvrir un terminal. Zéro Django requis — c'est le sujet.

## Les 9 modules

Un projet Django classique (un blog), construit de zéro, une brique à la
fois : création du projet → app → modèle de données → migration → vue et
URL → template HTML → interface d'administration → un dernier module sans
aide, pour vérifier que ça reste acquis sans la béquille.

Plusieurs modules incluent un exercice de code vérifié par de vrais tests
(pas juste une recherche de texte dans ton fichier) — la preuve que ta
fonction fait ce qu'elle doit faire, pas juste qu'elle existe.

## Structure du dépôt

```
lab/                    code de l'outil (UI + moteur de validation)
content/modules/        les modules pédagogiques (.md), éditables sans toucher au code
workspace/               ton projet Django — c'est ici que tu codes
start.sh / start.bat
requirements.txt
cdc.md                   cahier des charges complet (architecture, choix, risques connus)
suivi2dev.md             journal de développement (ce qui a été fait, testé, et pourquoi)
```

## Contribuer / écrire un nouveau module

Un module = un fichier `.md` dans `content/modules/`, nommé `NN-slug.md`
(le tri alphabétique fixe l'ordre). Frontmatter YAML pour les métadonnées et
les checks, Markdown libre pour le contenu :

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
Le pourquoi, pas que le comment.

## Consignes
**1.** ...
```

Types de check disponibles : `file_exists`, `contains_text`, `command_passes`
(commande shell, timeout 30s par défaut), `http_ok`, `test_passes` (lance les
tests Django de l'app). Détail complet des paramètres dans `cdc.md` §7.

**Important — frontière de confiance** : `command_passes` et `test_passes`
exécutent des commandes shell définies dans le `.md`. Un module est donc du
code de confiance, à traiter comme un script qu'on lance — toute
contribution externe (pull request ajoutant ou modifiant un module) doit
être relue ligne par ligne avant merge, au même titre que du code applicatif.

Après modification d'un `.md`, redémarre l'outil (`Ctrl+C` puis relance
`start.sh`) pour recharger le contenu.

## État du projet

Honnêteté avant tout : ce dépôt a passé un développement complet (moteur,
interface, 9 modules) testé en conditions réelles par le développeur, et un
premier retour d'un apprenant réel a déjà fait évoluer le contenu une fois
(verdict **ADJUST** — voir `suivi2dev.md` Phase 4-5). Il n'a **pas encore**
été validé par une séance formelle et chronométrée avec un débutant
complet — c'est le seul test qui dira vraiment si l'outil aide plus qu'une
formation classique. Si tu l'essaies et que ça bloque quelque part, une
issue avec le module concerné et ce que tu as tapé est la contribution la
plus utile que tu puisses faire.

## Licence

[MIT](LICENSE) — utilise, modifie, redistribue, y compris commercialement.
Pas d'obligation de republier tes modifications, une mention de la licence
d'origine suffit.
