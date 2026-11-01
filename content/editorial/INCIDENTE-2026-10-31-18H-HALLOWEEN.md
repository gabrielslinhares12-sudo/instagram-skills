# Incidente: carrossel Halloween das 18h — 31/10/2026

**Status: FALHOU / NÃO HÁ RECIBO DE PUBLICAÇÃO. Recuperação pendente de autorização Meta.**

Post: `halloween-2026-10-31-historia-8-laminas`, "A história do Halloween — da celebração celta à cultura pop"; oito JPGs. Agendado para 18:00 America/Sao_Paulo (`2026-10-31T21:00:00Z`).

## Evidência

- [18h23 — GitHub Actions #41243393274](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41243393274): prévia marcou `due`, mas etapa `instagram_preflight.py` retornou `{"ok":false,"error":"Meta rejected the request.","http_status":400,"code":200}`.
- [18h40 — GitHub Actions #41244633510](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41244633510): mesma resposta HTTP 400 / Meta code 200.
- Em ambos, `instagram_queue.py --execute` **não foi chamado**: o erro ocorreu antes, no preflight de permissões/identidade.
- [Verificação posterior](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41253213250) identificou `missed_window`; `MAX_LATENESS` de 2h impede publicação tardia sem nova decisão.
- `content/publication-state.json` só confirma o post das 12h, `halloween-2026-10-31-tirinha-aprovada`. Não contém mídia publicada para o das 18h.
- Código 200 na Graph API é indicativo de erro de permissões, **mas o escopo ou endpoint exato não consta dos logs públicos**.

## Recuperação segura: o mesmo post, não criar outro

1. Conferir conta Instagram profissional, Página Facebook vinculada, papel do usuário na Página, status do app e permissões `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`.
2. Reautorizar a conexão e atualizar o secret `FACEBOOK_USER_ACCESS_TOKEN` no GitHub (nunca em arquivos públicos). Verificar se o app possui o acesso necessário para a conta.
3. Rodar o preflight GET de identidade/permissões de forma segura antes de publicar: `python3 scripts/instagram_preflight.py` no contexto com Secrets.
4. Confirmar pela conta Instagram correta que esse carrossel **não** foi publicado fora do ledger. Não confiar apenas na ausência de recibo.
5. Recuperar **os mesmos oito arquivos e legenda**, preservando os hashes originais. Só então preparar publicação fora do horário, mediante autorização específica ou confirmação editorial do atraso.
6. Registrar o `media_id` real e data/hora após resposta confirmada da Meta. Não trocar status por suposição.
7. Melhorar o preflight para identificar **fase** (leitura de permissões ou validação da identidade) sem expor token.

Não forçar `rerun` da execução de 18h antes de corrigir a causa: apenas repetiria erro 200, e a janela de duas horas foi encerrada. Não alterar a publicação de 12h nem tornar posts de 01/11 aprovados.

Nenhum reenvio ou novo agendamento foi efetuado por este documento.
