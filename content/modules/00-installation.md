---
title: "Module 0 — Installation & activation"
description: "Préparer la machine et apprendre à activer le venv partagé"
checks: []
---

## Pourquoi ce module

Django Lab tourne dans un environnement virtuel Python (« venv ») partagé entre
l'outil et ton projet. Le formateur l'a déjà créé en lançant `./start.sh`
(ou `start.bat` sous Windows). Mais **chaque fois que tu ouvres un nouveau
terminal**, ce terminal ne connaît pas ce venv par défaut — il faut l'activer
toi-même. Sans cette étape, dès le Module 1, tes commandes `django-admin` ou
`python manage.py` ne trouveront pas Django.

## Étapes

1. Ouvre un **second terminal** (le premier fait déjà tourner l'outil sur
   `localhost:8000`, ne le ferme pas). C'est dans ce second terminal que tu
   coderas ton projet.
2. Active le venv partagé, depuis la racine du dépôt :
   - Linux/Mac : `source venv/bin/activate`
   - Windows (PowerShell) : `venv\Scripts\Activate.ps1`
   - Windows (cmd) : `venv\Scripts\activate.bat`
3. Vérifie que ça a marché :

   ```
   python -m django --version
   ```

   Si tu vois un numéro de version (ex: `5.2.15`), c'est bon. Si tu vois
   `ModuleNotFoundError: No module named 'django'`, le venv n'est pas activé
   — recommence l'étape 2.
4. Place-toi dans le dossier de travail :

   ```
   cd workspace
   ```

   C'est ici que tu coderas tout le reste — ne touche jamais au dossier `lab/`.

## Important

Tu devras refaire l'étape 2 (l'activation) **à chaque fois que tu ouvres un
nouveau terminal**, par exemple au Module 5 quand on te demandera d'en ouvrir
un troisième pour lancer ton propre serveur.

Pas de bouton « Vérifier » pour ce module : il n'y a rien à vérifier côté
code, seulement ton environnement. Quand l'étape 3 affiche un numéro de
version, dis-le à ton formateur et passe au Module 1.
