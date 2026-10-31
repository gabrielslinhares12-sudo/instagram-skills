# Entrega local consolidada — Instagram Tem Uma Explicação (31/10–06/11/2026)

> **ATUALIZAÇÃO — TRANSFERÊNCIA CONCLUÍDA EM 31/10/2026:** os 27 arquivos finais já estão no GitHub, extraídos e com URLs fixadas em SHA imutável. O texto abaixo registra o estado histórico anterior à transferência. Veja `content/editorial/TRANSFERENCIA-CONCLUIDA-2026-10-31.md`. Publicação no Instagram continua desativada e sem recibos.

**Status em 31/10/2026:** foi criado um pacote local de 7 conteúdos com mídias, roteiros, legendas e checksums SHA-256. **Não foi transferido ao GitHub** (o repositório não recebeu as mídias binárias novas); **não está agendado no Instagram**; a fila existente permanece bloqueada e o controle de publicação não tem recibos.

## Conteúdos locais terminados
| Dia planejado | Pauta | Entrega |
|---|---|---|
| 31/10 | Halloween / Lúmino no sofá com gato | 1 JPEG 1080×1350 |
| 01/11 | Votos válidos e denominadores | 8 JPEGs 1080×1350 |
| 02/11 | Por que o dólar varia | 8 JPEGs 1080×1350 |
| 03/11 | Onça-parda vs. onça-pintada | 7 JPEGs 1080×1350 |
| 04/11 | ENEM / distração com formigas | 1 JPEG 1080×1350 |
| 05/11 | Como foguetes aceleram no vácuo | 1 MP4 H.264 + AAC 1080×1920, ~41s, narração PT-BR local sintetizada |
| 06/11 | Por que a Lua parece seguir o carro | 1 MP4 H.264 + AAC 1080×1920, ~42,5s, narração PT-BR local sintetizada |

Total: 25 imagens + 2 vídeos. A fonte de cada imagem pode ser ilustrativa/gerada; não apresentá-la como foto documental. Os Reels usam voz sintética local (não Google AI Studio) e composição musical original. A identidade do Lúmino deve passar por revisão visual e os Reels por revisão de voz antes de qualquer upload público.

**Artefato entregue nesta conversa:** `Instagram_TUE_semana_31out_06nov_2026.zip`, com `manifesto-arquivos.json` (SHA-256 individual), subpastas por dia, `legenda.txt` e `LEIA-ME.md`. Esse nome corresponde ao arquivo da conversa ChatGPT, **não é URL HTTP pública** acessível ao GitHub Actions.

## Segurança de publicação / preferências atuais
- O usuário pediu produção de todos os conteúdos em sequência **sem tarefas horárias** e pediu **retirar verificações periódicas do GitHub**.
- O workflow `.github/workflows/instagram-scheduler.yml` foi alterado para **somente `workflow_dispatch`**, sem `schedule`; não reativá-lo sem nova instrução.
- A automação ChatGPT de produção foi desativada; não prometer notificação posterior sem nova automação.
- **Não definir `approved=true` enquanto os arquivos de imagem/vídeo corretos não tiverem sido enviados e verificados com URLs HTTPS públicas e estáveis.**
- Não usar imagens antigas rejeitadas; não publicar placeholder `PENDENTE.jpg`.
- O recibo de publicação do Instagram só existe se `content/publication-state.json` registrar `published` com `media_id`. Não inferir de saída local ou de GitHub Action de teste.

## Próxima etapa indispensável para publicação
Transferir os 27 arquivos finais do pacote ao repositório; confirmar dimensões, assinaturas e a integridade; substituir URLs de mídia por endereços permanentes fixados em commit e revisar legendas; executar preflight Meta; liberar um a um e acionar manualmente o workflow respeitando as datas/relevância. Se datas passarem, não publicar eventos antigos automaticamente.

## Fontes factuais de referência
- ICMBio: https://www.gov.br/icmbio/pt-br/assuntos/biodiversidade/pan/pan-grandes-felinos
- USFWS: https://www.fws.gov/rivers/carp/species/jaguar-panthera-onca
- NASA Glenn: https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/rocket-thrust-equation/
- TSE: https://www.tse.jus.br/comunicacao/noticias/2022/Outubro/entenda-como-e-eleito-o-presidente-da-republica

## Instalador de upload em lote (adicionado em 31/10)
O pacote ZIP final `Instagram_TUE_semana_31out_06nov_2026.zip`, entregue na conversa ChatGPT, contém `instalar_semana_github.py` e `INSTALAR_NO_GITHUB.cmd`. O instalador foi exercitado em um repositório Git de teste, com cópia de 27 mídias e atualização de sete entradas do manifesto, mas **não foi executado contra o repositório de produção**. Requer conexão do computador do proprietário com GitHub, Python e Git autenticado; extrair o ZIP inteiro e executar o CMD uma vez. A rotina verifica hashes, publica os 27 binários no GitHub em um único lote, confirma os URLs públicos com os hashes, atualiza as legendas e fixa URLs em SHA de commit; o item cuja data já tiver passado fica `approved=false`. O workflow não é habilitado para execução recorrente e nenhuma postagem é publicada automaticamente com este instalador.

**Atenção:** O estado do GitHub ainda não tem os 27 arquivos finais até que a execução de upload no computador conectado seja comprovada por commit. Não informar conclusão do agendamento/publicação do Instagram antes de recibo `published` e `media_id`.
