# Segurança editorial, isolamento e QC — TUE-CINEFRAME-01

## Limites técnicos
1. Não mudar main, arquivos oficiais, workflow de postagens, secrets ou cron.
2. Não atualizar padrão canônico da Odisseia, arquivo de aprovação do Cavalo de Troia ou arquivos de voz do usuário.
3. Qualquer integração externa usa configuração separada e opt-in por execução; nunca consumir créditos pagos automaticamente.
4. Se usar referência ao filme de Troia aprovado, somente leitura para comparação. Não derivar novo rosto sobre a identidade oficial sem autorização.
5. Não criar tarefas GitHub Actions com upload automático. Testes locais não têm token de publicação.
6. Saída experimental vai à pasta própria e nunca à fila editorial.

## Checklist bloqueante de cada tomada
[ ] Identidade da personagem coincide com a bíblia, incluindo acessórios
[ ] Personagem continua fisicamente o mesmo em começo/meio/fim
[ ] Preparação, ação, contato, reação e consequência legíveis
[ ] Objetos mantêm tamanho, peso, posse e trajetória sem teletransporte
[ ] Câmera respeita eixo, escala, portas e limites do cenário
[ ] Não há membros extras, morphing, artefatos ou atuações repetidas
[ ] Ritmo, som e fala estão sincronizados à narração validada
[ ] Legenda inferior correta (até 2 linhas), sem interface inicial nem marca d'água
[ ] Sequência funciona sem som, só pela ação
[ ] Piloto entregue é 2160×3840, 9:16, 60 FPS, testado no MP4 real (metadados de ffprobe)
[ ] Fontes/composição têm qualidade de origem apropriada; upscale artificial não se declara 4K nativo
[ ] Arquivo MP4 foi enviado à pasta experimental exclusiva do Google Drive
[ ] Arquivo, tamanho e pasta foram confirmados por metadados de leitura do Drive
[ ] Link direto para assistir ao MP4 foi compartilhado na conversa, sem inventar URL
[ ] Nenhum conteúdo é apresentado como 4K nativo quando apenas ampliado
[ ] Custos e licenças registrados, com zero despesas por padrão

## Gates de liberação
RASCUNHO -> REFERÊNCIAS APROVADAS -> CENAS APROVADAS -> MONTAGEM QC -> APROVAÇÃO EDITORIAL -> EXPORTAÇÃO.
Gates não são automáticos. **A entrega exige upload ao Drive e envio de link na conversa após leitura de confirmação.** A publicação nas redes não é parte deste modelo. A reprovação devolve somente a tomada/etapa com falha para correção.

## Métricas de comparação com o padrão atual
Tempo de produção por minuto aceito; proporção de tomadas aproveitadas; gasto estimado e efetivo; consistência dos personagens; clareza da história; legibilidade sem som; naturalidade de gesto; qualidade da fala/legenda. Somente com comparativo e autorização alterar qualquer pipeline vigente.
