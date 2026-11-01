# Instagram TUE — retomada operacional em 01/11/2026

> Auditoria somente leitura do estado publicado no repositório. Horário aproximado da conferência: 13h08–13h15 America/Fortaleza (16h08–16h15 UTC). Este documento NÃO autoriza publicação, remarcação nem aceite de custos.

## Resultado comprovado

- Conta de destino canônica: `@temumaexplicacao`.
- `content/publication-state.json` contém um único recibo confirmado: `halloween-2026-10-31-tirinha-aprovada`, mídia Instagram `18114706189871027`, publicada em `2026-10-31T15:06:47Z` (12h06 Brasília).
- `halloween-2026-10-31-historia-8-laminas`: aprovado, mas a janela original (31/10 18h Brasília) expirou. Não existe recibo desse item no ledger oficial consultado. **Não remarca automaticamente e não duplica.**
- `votos-validos-2026-11-01-v2-revisao` (01/11 12h): `approved=false`; janela já vencida e revisão visual pendente.
- `meme-voto-branco-nulo-2026-11-01-v2-revisao` (01/11 18h): `approved=false`; não agendar/publicar sem QC e autorização.
- O planejamento de 02/11 a 06/11 continua em revisão editorial, conforme `content/editorial/STATUS-PRODUCAO-2-POSTS-DIA-2026-11-01-a-06.md`.
- A fila GeeLark `content/geelark-music-plan.json` está vazia e `content/geelark-task-state.json` não tem tarefas enviadas.

## Evidência de testes e lacunas

- GitHub Actions [41324387897](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41324387897) passou **13 testes offline** do orquestrador GeeLark e auditoria de imagens. Modo efetivo foi `check`, sem solicitação ao fornecedor nem publicação.
- Nesse check: `api_token_present=false`, `phone_id_present=false`, `publisher_enabled=false`, `account_confirmed=false`, `vendor_cost_approved=false`, `ready_to_attempt=false`, `publication_attempted=false`.
- A validação [41324299387](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41324299387) constatou `session_secret_configured=false` para `INSTAGRAM_PRIVATE_SESSION_B64`, apesar da instalação e testes offline de biblioteca.
- O diagnóstico Android [41324290120](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41324290120) não substitui teste de autenticação no app Instagram. Testes anteriores de seleção múltipla na UI falharam.
- O último reparo dos testes GeeLark passou; uma execução anterior falhou no teste de data editorial diferente e foi corrigida por commits posteriores.

## Próxima etapa — somente após autenticação legítima

1. **Não repetir tentativas com instagrapi** após erro `PleaseWaitFewMinutes`; conservar o acesso oficial Meta que já foi validado.
2. Se o proprietário optar por GeeLark, verificar primeiro a necessidade de plano/app desktop e custos. **Não contratar, ativar ou aceitar custos automaticamente.**
3. Autenticar uma conta GeeLark e o Instagram **no aplicativo oficial dentro de celular Android persistente**, conferir o perfil `@temumaexplicacao`; não enviar senhas, cookies, códigos ou tokens em chats/commits/logs.
4. Somente depois da identificação correta, disponibilizar `GEELARK_TOKEN` como Actions Secret e `GEELARK_PHONE_ID` como variável. As travas `GEELARK_PUBLISH_ENABLED`, `GEELARK_ACCOUNT_CONFIRMED` e `GEELARK_COST_APPROVED` permanecem `false` até aprovação real.
5. Rever visualmente cada post contra o modelo Lúmino aprovado, selecionar uma fonte musical pública compatível, criar aprovação editorial individual, executar um teste sem publicar, e somente então tentar agendar **um item por vez**, com claim durável e validação posterior por ID/permalink, número de fotos e música.
6. Não transformar carrossel com música em Reel, não remover a música sem autorização, não alterar horários vencidos por conta própria.

## Protocolo de encerramento

Publicação = recibo oficial `media_id` e URL legível + conta certa + arte/legenda aprovadas + música verificada quando exigida. Sucesso de CI, tarefa de fornecedor, oito hashes ou sessão de rede social **não** equivalem a publicação.
