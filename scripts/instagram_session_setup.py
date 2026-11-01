#!/usr/bin/env python3
"""Create INSTAGRAM_PRIVATE_SESSION_B64 securely from an interactive one-time login.

Run ONLY in a trusted private terminal (e.g. your own GitHub Codespace).
This script NEVER prints or writes your password, 2FA code or session settings.
Session settings are encrypted by the GitHub CLI locally before upload.
The Instagram interface is UNOFFICIAL, may trigger challenges or restrictions.
"""
from __future__ import annotations

import base64
from getpass import getpass
import json
import os
import shutil
import subprocess
import sys

REPOSITORY = "gabrielslinhares12-sudo/instagram-skills"
ACCOUNT = "temumaexplicacao"
SESSION_SECRET_NAME = "INSTAGRAM_PRIVATE_SESSION_B64"

def fail(message: str) -> int:
    print(f"\nNão foi possível concluir: {message}", flush=True)
    return 1

def gh(*args: str, input_value: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["gh", *args],
        input=input_value,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=80,
    )

def main() -> int:
    print("Instagram TUE — autenticação ÚNICA; nenhuma postagem será enviada.")
    print("ATENÇÃO: usa instagrapi, uma API NÃO OFICIAL; pode exigir verificação ou restringir a conta.")
    print("Não compartilhe senha, código 2FA, sessão JSON ou valor do secret com terceiros/ChatGPT.\n")

    if shutil.which("gh") is None:
        return fail("GitHub CLI ausente neste ambiente. Use GitHub Codespaces ou instale gh.")
    try:
        # Check permissions BEFORE signing in, so a missing GitHub grant does not
        # unnecessarily create a new Instagram session.
        permission = gh("api", f"repos/{REPOSITORY}/actions/secrets/public-key", "--jq", ".key_id")
        if permission.returncode != 0 or not permission.stdout.strip():
            return fail(
                "GitHub CLI não pode gerenciar os Secrets de Actions deste repositório. "
                "Execute 'gh auth status' e autorize acesso ao GitHub antes de tentar novamente."
            )
    except (OSError, subprocess.TimeoutExpired):
        return fail("Não foi possível validar acesso aos Secrets do GitHub.")

    try:
        from instagrapi import Client
    except ImportError:
        return fail("instagrapi ausente. Execute primeiro o script de preparação do ambiente.")

    answer = input("Você aceita o risco de autenticar pela API móvel NÃO OFICIAL? Digite ACEITO: ").strip()
    if answer != "ACEITO":
        print("Autenticação cancelada; nenhum secret modificado.")
        return 0

    password = getpass(f"Senha do Instagram @{ACCOUNT} (entrada oculta): ")
    if not password:
        return fail("Senha vazia.")
    code = getpass("Código atual de autenticação 2FA (se houver; entrada oculta, Enter para ignorar): ").strip()
    print("\nAutenticando no Instagram. Confira avisos de login no aplicativo oficial se houver.")
    try:
        client = Client()
        # No file logging of the credentials or raw session. The library may
        # keep the session in memory during this short-lived setup process.
        client.login(ACCOUNT, password, verification_code=code)
        account = client.account_info()
        if str(getattr(account, "username", "")).casefold() != ACCOUNT:
            return fail("A conta autenticada não corresponde a @temumaexplicacao.")
        settings = client.get_settings()
        if not isinstance(settings, dict) or not settings:
            return fail("O Instagram não retornou uma sessão reutilizável.")
        payload = base64.b64encode(
            json.dumps(settings, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        )
        if not payload or len(payload) > 48_000:
            return fail("A sessão não cabe em um Secret de Actions.")
    except Exception as err:
        # Do NOT print the exception; some clients echo sensitive response data.
        if type(err).__name__ == "PleaseWaitFewMinutes":
            return fail(
                "O Instagram aplicou um limite temporário (PleaseWaitFewMinutes). "
                "NENHUM código foi necessariamente enviado. Interrompa as tentativas "
                "com esta API não oficial e confira a segurança da conta no aplicativo "
                "oficial. Não tente novamente agora: várias tentativas podem agravar "
                "o bloqueio."
            )
        return fail(
            "Instagram recusou o login ou solicitou validação adicional "
            f"({type(err).__name__}). Verifique a conta pelo aplicativo oficial; "
            "não tente repetidamente se houver bloqueio."
        )
    finally:
        password = ""
        code = ""

    try:
        # CLI reads secret on stdin and encrypts it for the repository before upload.
        # Never place secrets in command-line flags, files, logs, Git, or terminal output.
        result = gh("secret", "set", SESSION_SECRET_NAME, "--repo", REPOSITORY, input_value=payload)
        if result.returncode != 0:
            return fail(
                "GitHub recusou a criação do Secret. Confira se você tem permissão de "
                "admin no repositório e reexecute o procedimento com a sessão válida."
            )
    except (OSError, subprocess.TimeoutExpired):
        return fail("Houve falha de conexão ao guardar o Secret.")
    finally:
        payload = b""
        settings = None

    print("\nSUCESSO: sessão armazenada no GitHub Actions Secret:", SESSION_SECRET_NAME)
    print("Nenhum post foi publicado. A automação com API não oficial continua desativada.")
    print("Agora é possível executar o teste 'validar biblioteca de carrossel com musica na nuvem'.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
