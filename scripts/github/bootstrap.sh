#!/usr/bin/env bash
# Crée / met à jour labels, milestones, issues, GitHub Project et protection de main
# à partir de scripts/github/issues.yml. Idempotent.
#
#   scripts/github/bootstrap.sh              # DRY RUN : affiche le résumé, ne touche à rien
#   scripts/github/bootstrap.sh --list       # + liste de toutes les issues
#   scripts/github/bootstrap.sh --apply      # applique sur GitHub
#
# Prérequis : gh authentifié avec les scopes repo + project
#   gh auth login && gh auth refresh -s project
# et uv (https://docs.astral.sh/uv/) pour exécuter le script Python.
set -euo pipefail

cd "$(dirname "$0")"

command -v gh >/dev/null || { echo "gh (GitHub CLI) est requis" >&2; exit 1; }
if command -v uv >/dev/null; then
  UV=(uv)
elif python -m uv --version >/dev/null 2>&1; then
  UV=(python -m uv)
else
  echo "uv est requis (pip install uv)" >&2; exit 1
fi

if [[ " $* " == *" --apply "* ]]; then
  gh auth status >/dev/null 2>&1 || { echo "gh n'est pas authentifié : gh auth login" >&2; exit 1; }
fi

PYTHONIOENCODING=utf-8 exec "${UV[@]}" run --quiet --no-project --python 3.12 --with pyyaml \
  python bootstrap.py "$@"
