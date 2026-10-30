# Publicação diária de @temumaexplicacao

As imagens e os vídeos desta pasta são arquivos finais destinados à publicação
no perfil. As URLs de mídia do manifesto devem apontar para um commit específico,
preservando os bytes revisados. Os arquivos podem ser vistos publicamente porque
o Instagram precisa buscá-los por HTTPS; credenciais nunca ficam nesta pasta.

O proprietário solicitou produzir e programar o lote de sete pautas discutidas,
com o mascote Lúmino. A referência é uma lanterna de vidro vintage com lâmpada
quente interna, óculos redondos, olhos ciano e sobretudo cáqui flutuante, sem
boca, pernas ou pés. A autorização vale para esse lote, não para uma produção
indefinida de novos assuntos.

`schedule.json` define as mídias, legendas, destino e horários em UTC.
`publication-state.json` é o registro da automação. Não apagar entradas desse
registro para tentar novamente: uma publicação incerta exige conferência manual
da conta e do container antes de qualquer recuperação.

O workflow `instagram-scheduler.yml` confere a fila a cada 15 minutos, com
concorrência única e a variável `INSTAGRAM_SCHEDULER_ENABLED=true`. Os horários
são alvos; o GitHub Actions pode atrasar. Uma publicação com atraso superior a
12 horas não é enviada automaticamente. Uma claim é salva no Git remoto antes
de qualquer chamada de publicação, evitando duplicação após resposta incerta.

Conferência local, sem chamadas à Meta:

```bash
python3 scripts/instagram_queue.py --dry-run
```

A verificação `instagram_preflight.py` consulta as permissões e a identidade
usando apenas GET. Ela não publica conteúdo nem garante que um futuro upload
será aceito. O token permanece em GitHub Secrets; sua expiração informada pelo
proprietário é 29/12/2026 e ainda não há renovação automática.
