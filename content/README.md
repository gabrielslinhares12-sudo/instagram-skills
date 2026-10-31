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

O workflow `instagram-scheduler.yml` **não verifica a fila automaticamente** (o gatilho recorrente foi desativado a pedido do proprietário). Só executa quando acionado manualmente, com
concorrência única. Para executar o lote de sete já autorizado, o agendamento
fica habilitado quando a variable `INSTAGRAM_SCHEDULER_ENABLED` estiver ausente
ou igual a `true`. Para suspender publicações, definir explicitamente a
variable do repositório como `INSTAGRAM_SCHEDULER_ENABLED=false`.
A autorização publicada no manifesto é individual: os dois Reels ainda têm
`approved=false` até a revisão técnica e visual completa.

Os horários são alvos; o GitHub Actions pode atrasar. Uma publicação com atraso
superior a 12 horas não é enviada automaticamente. O workflow consulta
identidade e permissões oficiais por GET antes de reivindicar qualquer item
devido; sem concessões, não consome a tentativa. Uma claim é salva no Git remoto
antes de qualquer chamada de publicação, evitando duplicação após resposta incerta.

Conferência local, sem chamadas à Meta:

```bash
python3 scripts/instagram_queue.py --dry-run
```

A verificação `instagram_preflight.py` consulta as permissões e a identidade
usando apenas GET. Ela não publica conteúdo nem garante que um futuro upload
será aceito. O token permanece em GitHub Secrets; sua expiração informada pelo
proprietário é 29/12/2026 e ainda não há renovação automática.
