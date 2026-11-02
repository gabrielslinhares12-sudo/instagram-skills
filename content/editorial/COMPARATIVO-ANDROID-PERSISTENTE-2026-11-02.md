# Android persistente — comparação e etapa de autenticação — 02/11/2026

Objetivo: manter Instagram autenticado em Android na nuvem, controlado pelo GitHub, sem PC, sem contratação sem aprovação e sem republicação.

## Histórico
- A plataforma Github Actions já executou Android 11 e recuperou 8 imagens; o diagnóstico 41388475229 comprovou que a Google Play exige login. É emulador efêmero.
- A alternativa GeeLark está ARQUIVADA E PROIBIDA pelo proprietário desde 01/11/2026. Não reativar.

## Alternativas públicas
- DuoPlus: 1 telefone por 30 dias com apenas 30 minutos de uso no teste grátis; painel web mobile; OpenAPI e gateway HTTP para UI. A disponibilidade de API no teste gratuito NÃO foi comprovada. https://www.duoplus.net/pricing/ e https://help.duoplus.net/docs/AIControlled-Cloud-Phone-API
- Clousd: 30 minutos no plano grátis; painel web e API documentados, mas a tabela Free não oferece API/MCP/ADB. Uso pago. https://clousd.com/pricing/
- MoreLogin: 100 minutos de cloud phone gratuitos, mas onboarding prevê cliente desktop. https://www.morelogin.com/cloud-phone
- Genymotion SaaS: US$ 0,06/minuto, cobrança por uso. https://www.genymotion.com/pricing/

## Implementado no GitHub
- scripts/instagram_duoplus_readiness.py consulta EXCLUSIVAMENTE a lista documentada de aparelhos, por POST sem efeito de escrita (endpoint de consulta).
- scripts/test_instagram_duoplus_readiness.py verifica falha segura, token ausente, id ausente, estado offline, HTTP desligado e nenhum dado sensível em saída.
- .github/workflows/instagram-duoplus-readiness.yml executa testes offline a cada alteração; a consulta remota SÓ ocorre via disparo manual workflow_dispatch.
- Nunca utiliza endpoints de instalação, início, edição, pagamento ou publicação; não opera a UI do Instagram nem cria sessões.
- Os dados sensíveis da resposta do fornecedor (IP, adb_password, nome, cookies) NÃO são impressos.

## Ponto de ajuda estritamente necessário
1. Proprietário escolhe testar DuoPlus; cadastro diretamente no navegador do próprio celular em https://my.duoplus.net (não usar cartão).
2. Verificar dentro da conta se o teste gratuito permite abrir um telefone e gerar chave em Automation > API.
3. Caso API liberada, chave SOMENTE em GitHub Actions Secret DUOPLUS_API_KEY, nunca no chat; ID do telefone em Actions Variable DUOPLUS_PHONE_ID.
4. Depois, executar workflow manual read-only, validar acesso, então pedir autorização separada antes de instalar Instagram/logar no Android do terceiro.
5. Nunca guardar senha Google/Instagram ou sessão em Actions artifacts, logs ou Git commits.

## Estado editorial
- Halloween publicado: https://www.instagram.com/p/DfNVlLDmC8P/ ; não repostar.
- Thriller continua pendente; teste de conexão NÃO significa música aplicada.
- Nenhuma compra, nenhum cadastro e nenhuma publicação foram efetuados.
