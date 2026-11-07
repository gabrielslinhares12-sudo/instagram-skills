# TUE-CINEFRAME-01 — Laboratório de cinema por referências

ID: TUE-CINEFRAME-01
Versão: 0.1.0 (experimental)
Estado: INDEPENDENTE / NÃO APROVADO PARA PUBLICAÇÃO
Criado: 07/11/2026

## Objetivo
Modelo alternativo para vídeos de personagens consistentes, planos com câmera dirigida e montagem cinematográfica. Inspiração metodológica: roteiro por cena, bíblia de imagens, image-to-video dirigido e edição por cortes. NÃO copia a identidade visual, o enredo nem os personagens do Reel de terceiros.

## Isolamento (regra obrigatória)
- Esta pasta é independente de odyssey_v8/, odyssey_2d/, odyssey_185/, content/, do padrão TUE-ANIMACAO-MESTRE-01 e do padrão TUE-MESTRE-01.
- O experimento vive exclusivamente na branch experimental/tue-cineframe-01. Não é permitido mesclar automaticamente com main.
- Não altera automações, horários, publicações, assets aprovados, áudio master ou fluxos existentes.
- Não disparar upload, agendamento ou publicação. Aprovação editorial humana explícita é necessária.
- Assets experimentais são novos. Referências aprovadas antigas são read-only, somente para comparação, nunca sobrescritas.
- Os renders de teste e arquivos temporários ficam em área experimental própria, nunca no diretório de publicação.

## Pastas
- docs/ : direção e governança
- templates/ : registro de personagens e planos em JSON
- scripts/ : verificador local sem serviços externos
- references/ : imagens de referência autorais, cada identidade com ID imutável
- tests/ : planos e renderizações somente para revisão
- renders/ : arquivos intermediários (não versionar vídeos pesados)
- delivery/ : exportações experimentais, nunca aprovadas automaticamente

## Pipeline A (com gerador de vídeo, opcional/pago)
1. Roteiro factual fechado e aprovado; separar em tomadas de 3-8 segundos.
2. Criar bíblia consistente de cada personagem e locação (frente, perfil, 3/4, expressões, acessórios e escala).
3. Congelar a ficha de personagem com id, imagem mestre e hash de aprovação; usar os mesmos arquivos em todas as tomadas.
4. Para cada tomada: quadro inicial e final, ação física, câmera, foco, perspectiva, fala exata, iluminação e lista do que evitar.
5. Gerar 2 tomadas candidatas quando necessário. Seedance é apenas motor opcional; verificar disponibilidade, direitos, política de uso e créditos antes.
6. QC sem som (a ação deve ser legível), QC de continuidade, QC de voz/legenda, só então montar no FFmpeg/CapCut.
7. Piloto para avaliação deve sair em 2160×3840 (9:16), 60 FPS, com qualidade e materiais de origem suficientes para essa entrega. Não aceitar 540×960, 720×1280 ou 1080×1920 ampliados como 4K nativo. Render de baixa resolução é apenas diagnóstico interno e não pode ser apresentado como piloto final.

## Pipeline B (custo zero, sem Seedance)
Usar desenhos autorais e sprites/rigs 2D por cena, composição Python/Remotion, movimento corporal real, fundos em camadas e FFmpeg. Mantém os mesmos contratos de personagens, roteiro e QC; NÃO prometer movimento generativo 3D realista por zoom em estáticos.

## Voz e acabamento
Preferência: Rasalgethi do Google AI Studio, quando áudio fornecido/produzido licitamente no fluxo já autenticado; não ativar API paga, não guardar chaves nem vozes privadas neste repositório. Legendas inferiores limpas (até 2 linhas), sem HUD, sem marca d'água e sem selo de IA.

## Contrato obrigatório de qualidade e entrega (vigente desde 07/11/2026)

- Todo piloto **entregue para visualização** deve ser renderizado e verificado em **2160×3840, 60 FPS, 9:16**, com composição e recursos adequados à resolução original. A exigência vale para pilotos, não apenas para o master final.
- Não ampliar um arquivo de baixa resolução para fingir 4K nativo. Se não for viável produzir com essa qualidade, manter como diagnóstico interno e relatar a limitação; não divulgar como piloto de aprovação.
- Fluxo padrão obrigatório: **render -> QC técnico e editorial -> upload para a pasta exclusiva no Google Drive -> leitura de confirmação do arquivo no Drive -> envio do link de visualização diretamente na conversa**.
- Pasta do laboratório: https://drive.google.com/drive/folders/1pX6O2cugZ5-T1eb4gHGvb6wZ5MH7aTXU . Usar subpasta individual por projeto sempre que necessário, preservando separação do acervo oficial.
- Link deve apontar ao **MP4 confirmado no Drive**, não a um arquivo imaginado, anexo local ou pasta sem arquivo. Se o upload falhar, dizer explicitamente que não foi enviado e não afirmar conclusão.
- Envio ao Drive **não** significa permissão para publicar/agendar no Instagram ou outras redes. O bloqueio de publicação permanece.
- O piloto histórico de Cleópatra 30s em 540×960/30fps antecede esta política e **não atende à nova exigência**; permanece como material diagnóstico, não como piloto final aprovado.

## Teste piloto
Começar com 3 tomadas novas de 6 s (18 s) inspiradas em Odisseu despertando em Ítaca (Odisseia, canto XIII). Esses arquivos são apenas exemplos de direção, não mídia criada. Usar personagens com identidade experimental diferente da versão oficial; comparação com o Cavalo de Troia aprovado é apenas diagnóstico.

## Como verificar contratos
python3 experiments/tue-cineframe-01/scripts/validate_manifest.py experiments/tue-cineframe-01/templates/shot-manifest.example.json

## Critérios para decidir adoção no futuro
Comparar duração real de produção, custo por segundo utilizável, estabilidade dos rostos/roupas, física e contatos, coerência espacial, ritmo e aprovação editorial. Permanecer separado até decisão específica do usuário.
