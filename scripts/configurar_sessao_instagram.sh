#!/usr/bin/env bash
# Uso interativo em GitHub Codespaces: não coloque credenciais no comando.
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v python3 >/dev/null || ! command -v gh >/dev/null; then
  echo "É necessário Python 3.11+ e GitHub CLI (gh). Use GitHub Codespaces."
  exit 1
fi
if ! python3 -c 'import sys; assert sys.version_info >= (3,11)'; then
  echo "O Python precisa ser versão 3.11 ou superior."
  exit 1
fi
VENV="$(mktemp -d "${TMPDIR:-/tmp}/tue-ig-auth.XXXXXXXX")"
trap 'rm -rf "$VENV"' EXIT
python3 -m venv "$VENV/venv"
echo "Preparando biblioteca em diretório temporário, sem salvar senhas."
"$VENV/venv/bin/python" -m pip install -q --disable-pip-version-check \
  "instagrapi==3.2.2" "Pillow>=13,<14"
"$VENV/venv/bin/python" scripts/instagram_session_setup.py
