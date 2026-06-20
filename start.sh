#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/venv"

if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ python3 introuvable. Installe Python 3.10+ avant de continuer." >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "📦 Création du venv..."
  python3 -m venv "$VENV_DIR"
fi

echo "📦 Installation des dépendances..."
"$VENV_DIR/bin/pip" install -q -r "$ROOT_DIR/requirements.txt"

mkdir -p "$ROOT_DIR/workspace"
touch "$ROOT_DIR/workspace/.gitkeep"

echo "🔧 Migrations internes..."
"$VENV_DIR/bin/python" "$ROOT_DIR/lab/manage.py" migrate --noinput

echo ""
echo "✅ C'est prêt — ouvre http://localhost:8000"
echo ""
exec "$VENV_DIR/bin/python" "$ROOT_DIR/lab/manage.py" runserver 8000
