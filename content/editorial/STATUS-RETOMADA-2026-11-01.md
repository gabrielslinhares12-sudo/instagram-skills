# Instagram TUE — retomada operacional em 01/11/2026

> Auditoria somente leitura do estado publicado no repositório. Horário aproximado da conferência: 13h08–13h15 America/Fortaleza (16h08–16h15 UTC). Este documento NÃO autoriza publicação, remarcação nem aceite de custos.

## Continuação no Work — 01/11/2026

### Acesso e publicação musical
- Repositório consultado e clonado em `3c457af1f1a5f8914d8f25744e05dcec512ab1c5`.
- Instagram oficial aberto em navegador cloud: tela de login, sem perfil autenticado. O formulário seguro encerrou com `declined`; nenhuma autenticação foi comprovada. Não repetir sem nova solicitação do proprietário. Login web não substitui login no app Android nem comprova música nativa.
- Nenhuma tentativa de instagrapi, contratação, ativação paga ou publicação nesta continuação.
- Documentação oficial do endpoint GeeLark consultada novamente: `sameStyleUrl`, `publishPost` e `needShareLink` estão documentados. A resposta contém `taskId`, não recibo de publicação.
- **13 testes offline GeeLark e 5 testes do padrão visual passaram.** Os testes visuais exigiram disponibilizar a fonte DejaVuSansCondensed-Bold já presente no ambiente; nenhum código de renderização foi alterado.
- `verify-assets` e `audit-queue` passaram. Não há novo carrossel aprovado nessa auditoria; isso NÃO significa que rascunhos tenham passado no QC artístico.
- `check` local: sem token/phone ID, publicação/conta/custos desabilitados, `ready_to_attempt=false`, `publication_attempted=false`. Esse resultado descreve o ambiente local, não relê Secrets do GitHub.
- Preservados os quatro registros de agenda, o recibo anterior e os dois ledgers vazios do fluxo musical. Nenhum horário vencido foi remarcado.

### Revisão visual efetivamente realizada

| Material | Evidência examinada | Resultado e correção necessária |
|---|---|---|
| Modelo oficial | PNG de referência do repositório | Usar papel claro, manchete condensada sobre pincelada amarela, vermelho pontual e cenas variadas. Números da referência não são fonte factual. |
| Votos V2 | As 8 imagens individuais em `content/staging/votos-validos-2026-11-01/` | **QC visual reprovado.** Fundo e mascote repetidos em todas as páginas; restos de texto do fundo visíveis acima da faixa inferior; ícones de confirmação ausentes (quadrados vazios) nas páginas 2 e 8; cabeçalhos residuais no alto de algumas páginas. Página 5: representar arredondamento com ≈, ou escrever a conta completa `(46 ÷ 90) × 100 ≈ 51,1%`. A conta 44+46+10=100 é coerente. Não foi feita nova validação jurídica nesta etapa. |
| Meme votos V2 | JPG individual 1080×1350 | Texto visualmente legível; personagem com chapéu e olhos em pixels difere do PNG canônico. Memes podem variar o estilo, mas a identidade do Lúmino exige correção antes de liberação. |
| Foguetes V9 | Prévia de 8 imagens e página 5 individual | **QC visual reprovado.** Rótulo superior da cena da página 5 está cortado; layout/escala/posição do mascote se repetem nas 8 peças. Preservar o PNG original, variar composição e remover textos herdados das cenas. |
| Lua V9 | Prévia de 8 imagens e capa individual | **QC visual reprovado.** Rótulos `POSIÇÃO 2`, `OBSERVADOR 2` e restos de `VISÃO...` aparecem sem contexto ou cortados. Capas/cenas recorrentes e mesma pose/posição em todas as peças. Remover rótulos herdados e reconstruir demonstração de paralaxe legível. |

### Pacote recuperado e reconciliação semanal
- Recuperado `INSTAGRAM-TUE-05-06NOV-V9-16ARTES-PADRAO-CANONICO.zip`, SHA-256 `3010a2008a2504e957579aaea64d615c0b079f5db88cd95624afca6253ee43b8`.
- CRC sem erro; 16 JPEGs individuais, todos 1080×1350, 16 hashes distintos. A integridade do ZIP não remove os defeitos visuais acima.
- O relatório geral de produção anterior está desatualizado em relação às versões: Onças possui entrega reconstruída posterior ao V3 original; ENEM possui 9 artes V2; Foguetes/Lua possuem V9. Consultar os relatórios específicos de entrega antes de recuperar V1/V2 antigas.
- Dólar: ainda precisa harmonização de todas as páginas; não promover capa V3 isolada com interiores rejeitados.
- Onças e ENEM: relatórios de entrega lidos; os pacotes externos mais recentes ainda não foram inspecionados nesta continuação. Não declarar QA concluído.
- Reels de 05/11 e 06/11: permanecem pendentes no planejamento; não substituídos automaticamente pelos carrosséis V9.

### Próximo trabalho concreto
1. Corrigir os defeitos de Votos e do meme mantendo os horários vencidos bloqueados.
2. Recuperar os pacotes mais recentes de Onças/ENEM, revisar individualmente, depois harmonizar Dólar e reconstruir as cenas problemáticas da V9.
3. Retomar autenticação apenas com participação do proprietário no fluxo seguro. Para música, confirmar primeiro acesso ao Android persistente e custos reais, depois login no aplicativo oficial.
4. Selecionar faixa disponível na própria conta, preparar um carrossel revisado e executar teste sem publicar. Só então liberar um item autorizado, verificar as fotos e a música e registrar recibo real.

**Situação ao final desta etapa: revisão avançou; fila semanal NÃO concluída, NÃO agendada e NÃO publicada.**

---

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
