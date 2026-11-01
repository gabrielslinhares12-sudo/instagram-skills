#!/usr/bin/env bash
# Configuração interativa no Codespaces; nenhuma senha do Instagram é solicitada.
# O segredo GeeLark só é enviado ao GitHub Actions; nunca para chat/commits/logs.
set -euo pipefail
REPO="gabrielslinhares12-sudo/instagram-skills"
if ! command -v gh >/dev/null; then echo "GitHub CLI (gh) indisponível."; exit 1; fi
gh_owner() { env -u GH_TOKEN -u GITHUB_TOKEN gh "$@"; }
echo "Configurando integração GeeLark → GitHub Actions (sem criar ou publicar tarefas)."
if ! gh_owner api "repos/$REPO/actions/secrets/public-key" --jq '.key_id' >/dev/null; then
  echo "Autentique o GitHub CLI com acesso de administrador. Não é login do Instagram."
  exit 1
fi
read -rsp "Token GeeLark da área GeeHub > API (entrada oculta): " token
echo
if [ -z "$token" ]; then echo "Token não fornecido. Nada foi alterado."; exit 1; fi
printf '%s' "$token" | gh_owner secret set GEELARK_TOKEN --repo "$REPO" --app actions
unset token
echo "Secret GEELARK_TOKEN salvo. Nenhuma postagem ou compra realizada."
read -rp "ID do celular Android GeeLark já conectado (somente dígitos; Enter para deixar pendente): " phone
if [ -n "$phone" ]; then
  if ! [[ "$phone" =~ ^[0-9]{3,35}$ ]]; then
    echo "ID inválido; a variável não foi configurada."
    exit 1
  fi
  gh_owner variable set GEELARK_PHONE_ID --repo "$REPO" --body "$phone"
fi
unset phone
gh_owner variable set GEELARK_PUBLISH_ENABLED --repo "$REPO" --body false
gh_owner variable set GEELARK_ACCOUNT_CONFIRMED --repo "$REPO" --body false
gh_owner variable set GEELARK_COST_APPROVED --repo "$REPO" --body false
echo "Travas de publicação DESLIGADAS por segurança."
if gh_owner secret list --repo "$REPO" --app actions --json name --jq '.[].name' | grep -Fxq GEELARK_TOKEN; then
  echo "Concluído: GEELARK_TOKEN detectado nos Repository secrets do GitHub Actions."
else
  echo "O Secret não consta na lista; confira GitHub Settings > Secrets and variables > Actions."
  exit 1
fi
