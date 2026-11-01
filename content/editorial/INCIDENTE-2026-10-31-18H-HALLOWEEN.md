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

## Recuperação solicitada em 01/11/2026 — estado final **ambíguo**

O proprietário **autorizou em 01/11** publicar o carrossel Halloween que havia falhado em 31/10, mantendo as **8 imagens aprovadas** e a legenda, com música inserida **depois** pelo Instagram móvel.

- Drive com as oito imagens APROVADAS (arquivos `01-historia-HALLOWEEN-APROVADA.jpg` ... `08-historia-HALLOWEEN-APROVADA.jpg`): https://drive.google.com/drive/folders/1n_gVeAILscdLvjf0xO9ETlOMsv5nOTol . Não usar a prévia anterior nem arquivos sem o sufixo `APROVADA`.
- Recuperação exclusiva e bloqueios de duplicatas na main, `distribution_mode=api_carousel_then_native_music`, `owner_authorized_two_step_music=true`. O checkout e os SHA-256 do lote passaram QC em https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41333115028 . **Não foi autorizada a liberação dos rascunhos de 01/11**.
- A primeira execução de recuperação https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41332969496 parou em QC porque o horário novo acionou a regra de novos carrosséis; corrigido com verificação excepcional ESTRITA dos oito JPGs legados (mesmos URLs imutáveis, hashes, dimensões), preservando a regra das novas pautas.
- A segunda execução de recuperação https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41333115028 passou QC, preflight Meta e checagem de carrossel duplicado nos 100 posts recentes. A Meta criou o contêiner `18102064946100158`, porém retornou HTTP 400 / subcódigo **2207003**, apontando demora no download/processamento de mídia. O ledger gravou `needs_review`.
- Diagnóstico somente GET https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41333320892 mostrou `status_code=FINISHED` e nenhum carrossel idêntico na lista.
- Houve **UMA** tentativa de finalizar esse mesmo contêiner já processado, com reserva durável antes da chamada https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41333454184 . A API não retornou ID de mídia confirmado e o ledger registrou `resume_outcome_uncertain` e `resume_attempted_at`. Nunca repetir esse POST sem reconciliação explícita.
- Diagnóstico adicional https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41333515974 e https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41333623094: Meta reporta contêiner como **PUBLISHED**, entretanto a listagem de mídia da própria conta ainda mostra apenas a tirinha de 31/10 (ID `18114706189871027`). **Nenhum `media_id` nem permalink do novo carrossel foi confirmado.**
- **Conclusão de auditoria:** publicação final **NÃO CONFIRMADA**. Status correto de ledger: `needs_review`. Não transformar em `published` nem `awaiting_native_music`, não dar como postado, não reenviar nem finalizar música antes de localizar a publicação no app/Graph. `PUBLISHED` no contêiner não substitui recibo de mídia final.
- A música nativa não foi adicionada nem testada no carrossel. O usuário confirmou a opção **Adicionar música** ao editar uma publicação de FOTO no app oficial, mas isso não prova disponibilidade para carrossel.
- Próxima ação: checar no app oficial `@temumaexplicacao` se o novo carrossel apareceu (imagens e legenda). Se existir, localizar permalink/ID e reconciliar o registro. Se não existir, só avaliar nova tentativa com origem de mídia alternativa depois de garantir ausência da publicação/duplicata; não repetir contêiner `PUBLISHED`.


- Verificação final de propagação às **17h54 UTC de 01/11**: https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41333820574 — contêiner permanece `PUBLISHED`, mas a consulta `/{ig_user_id}/media?fields=id,caption,media_type,permalink,timestamp` ainda retorna exclusivamente a tirinha de 31/10, **sem** carrossel correspondente. Resultado da publicação permanece **não verificável**; nenhuma nova tentativa de upload efetuada.

## RESOLVIDO: carrossel publicado em 01/11/2026, aguardando música nativa

- Após a confirmação do proprietário de que não havia carrossel visível, o procedimento de recuperação testou a **mesma sequência de oito JPGs** (SHA256 idênticos) pela CDN versionada jsDelivr, em modo somente GET. [Pré-validação 8/8 aprovada](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41334604459).
- Uma **única** execução com essa origem alternativa passou pela autenticação da conta correta e verificou ausência de post duplicado antes de criar novas mídias: [reparo aprovado](https://github.com/gabrielslinhares12-sudo/instagram-skills/actions/runs/41334769693).
- **CONFIRMADO via Meta Graph API:** `media_id=18107496023215107`; `media_type=CAROUSEL_ALBUM`; legenda integral corresponde ao carrossel aprovado. Link real: **https://www.instagram.com/p/DfNVlLDmC8P/** .
- Publicação registrada em `2026-11-01T18:06:47Z` (15h06min47s America/Sao_Paulo). Novo contêiner de carrossel `18102067970100158`; oito contêineres-filhos preparados; nenhum conteúdo adicional da fila semanal foi liberado.
- O ledger mantém **`status=awaiting_native_music`**, não `published`, porque o requisito de **música adicionada no aplicativo oficial ainda está pendente**. O usuário já confirmou que a conta permite **Adicionar música** na edição de uma foto; a função num carrossel continua a verificar no app.
- Erro histórico de upload pelo raw.githubusercontent e tentativa de retomada foi preservado em `previous_attempt_error`; a recuperação confirmou a publicação. **Jamais reexecutar workflows antigos ou fazer novo upload desse mesmo carrossel.**
- Próxima etapa: abrir o link acima no app Instagram, tocar em ⋯ > Editar > Adicionar música, escolher e salvar a faixa. Confirmar música audível no **mesmo permalink**; só então registrar a conclusão da etapa musical.
