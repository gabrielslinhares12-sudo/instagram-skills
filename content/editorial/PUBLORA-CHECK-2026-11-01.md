# Instagram TUE — teste seguro da integração Publora (01/11/2026)

**Propósito:** verificar se o Publora pode listar uma conta Instagram conectada, sem criar rascunhos, carregar mídias, publicar, agendar ou alterar o calendário.

## Resultado técnico

- O pacote de skills do projeto já existe no repositório: `SKILL.md`, `skills/ig-carousel-planner/`, `lib/publora_client.py`, `.env.example` e `requirements.txt`.
- O comando `npx skills add sergebulaev/instagram-skills` é para **instalar no terminal do agente**. Não substitui autenticação, não configura o serviço no GitHub e não adiciona música.
- O instalador `npx` não respondeu no ambiente da conversa antes do timeout. Não há confirmação de nova instalação.
- O Publora usa a API oficial da Meta, suporta carrosséis de 2 a 10 fotos e NÃO consegue aplicar música nativa. Fonte: https://docs.publora.com/platforms/instagram
- Nosso Instagram profissional `@temumaexplicacao` já dispõe de integração oficial Meta no projeto, ver `references/meta-api-setup.md`. Criar uma segunda integração é opcional, não requisito para resolver o áudio.
- A alternativa instagrapi permanece experimental e exige sessão autêntica e aceite informado de risco; não confundir com Publora.

## O que foi preparado para quem quiser usar o Publora

- `scripts/publora_readonly_preflight.py`: só consulta `GET /api/v1/platform-connections`; verifica conta exata, status do vínculo e token, sem exibir segredos.
- `scripts/test_publora_readonly_preflight.py`: testes sem rede para evitar conta errada e mudanças involuntárias.
- `.github/workflows/instagram-publora-readonly-check.yml`: execução automática de testes offline ao mudar o código; checagem real da conexão somente mediante clique manual em **Run workflow**.

**Etapas que dependem do proprietário** (ainda não realizadas):

1. Criar ou entrar na conta Publora gratuitamente em https://app.publora.com/signup.
2. Em Channels > Add Channel > Instagram, autorizar `@temumaexplicacao` pelo OAuth oficial. O serviço exige uma conta profissional elegível; a elegibilidade Creator depende do fluxo Meta.
3. Abrir Settings > API > Create Key. Guardar a chave diretamente em GitHub > Settings > Secrets and variables > Actions > **Repository secret** `PUBLORA_API_KEY`. **Não postar a chave no chat nem fazer commit de `.env`.**
4. Copiar o Platform ID `instagram-...` do Publora e definir a **Repository variable** `INSTAGRAM_PLATFORM_ID`.
5. Acionar manualmente Actions > **Instagram TUE — checar conexão Publora sem publicar** > Run workflow.

**Critério de aceitação:** `mode=verified`, `account_matches=true`, `token_ready=true`, `connection_active=true`; `music_via_publora_api=false` permanece por limitação da API.

**Decisão operacional:** este check **não ativa** agendamento. Publicar carrossel com música continua bloqueado até existir um método realmente capaz de aplicar áudio e verificar o resultado; não fazer um post sem música como substituto.

Referências: https://docs.publora.com/endpoints/platform-connections , https://publora.com/instagram
