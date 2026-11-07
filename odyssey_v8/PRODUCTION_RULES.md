# Odisseia V8 — reconstrução do zero (contrato editorial e técnico)

**Situação:** em produção, NÃO APROVADA, NÃO PUBLICÁVEL.

## Fonte única da narrativa
- Narração original, duração 560,1 s, idioma português brasileiro, voz Rasalgethi. O master privado original é fonte de áudio e de conferência de texto; NÃO reutilizar seus desenhos, bonecos, camadas ou cenas.
- Divisão prevista: EP01 0–88,6 s, EP02 88,6–317,4 s, EP03 317,4–560,1 s.
- Cada fala deve ser verificada contra cenas do roteiro e legenda original. Um timecode aproximado NÃO aprova nenhum frame.

## Motor novo
- Cenas tridimensionais independentes, com geometria, escala, profundidade/oclusão e câmera em um único espaço 3D.
- Personagens articulados com mãos, ombros, joelhos, tornozelos e marcha vinculados ao deslocamento do corpo. Não é permitido deslizar uma figura estática.
- O plano deve mostrar **preparação → ação concreta → consequência**: abrir o portão, atravessar, fechá-lo; embarcar, remar, deixar o cais; chegar à entrada, empurrar a PEDRA MAIOR QUE A PORTA, ver saída completamente bloqueada.
- Objetos têm dono e física: palmas tocam o objeto durante todo empurrão; pés apoiam no solo; ninguém atravessa a parede sem passagem explícita; uma pedra que deveria vedar a abertura deve ser maior do que ela.
- **Sem sobreposição como método de montagem:** proibido colocar protagonista, cenários, barco, objetos ou personagens por cima de uma animação genérica. Todos existem em coordenadas compartilhadas e dependem da câmera com z-buffer.
- Cada tomada tem casting próprio. Odisseu não aparece automaticamente em todos os planos. Cenário não reaproveitado como enchimento.
- Transições respeitam direções de deslocamento e posições do plano anterior; lentes/cortes só mudam com motivação narrativa.

## Modelo de produção, sem APIs pagas, sem PC
- Open-source: VTK para verificação espacial rápida; Blender com personagens 3D CC0 rigados para aprimoramento visual e render cloud no GitHub Actions.
- A primeira sequência experimental é a **caverna de Polifemo (38–55 s)**, porque exige personagens entrando, gigante retornando e rocha vedando a passagem — um teste exigente da integração 3D. Uma versão de bloqueio técnico 720 × 1280/30 FPS NÃO é o produto 4K final.
- Novo storyboard por plano, casting e objetos antes de render. Se um teste falha visualmente, corrigir o sistema e refazer o plano, não empilhar elementos por cima.
- Audio Rasalgethi e legendas do master originais: preservação; o vídeo do Github pode ser silencioso por não expor o master privado no repositório.

## QC *fail closed*
1. Assistir a sequência sem áudio: o observador consegue contar o acontecimento corretamente?
2. Assistir com áudio: cada fato falado aparece na ordem e com causa/consequência?
3. Verificar quadro a quadro entradas/saídas de objetos, contatos, profundidade, continuidade de membros, postura e movimento da câmera.
4. Inspecionar pontos de corte de cada cena e limites de quadro: nenhuma cabeça cortada ou ator oculto acidentalmente.
5. Verificar a ligação do passo ao deslocamento e ausência de teletransporte/animais desaparecendo.
6. Confirmar autoria/licenças das malhas/rigs externos. Sem marca d’água. Divulgação de conteúdo sintético conforme regras da plataforma quando aplicáveis.
7. **Só após QC visual e narrativo real:** render final nativo 2160 × 3840, 60 FPS, sincronismo, revisão completa, e então preparar o arquivo 1080 × 1920 permitido pela Meta API.
8. Sem publicação automática nem agendamento de amostras; V5/V7.1 marcadas REPROVADAS permanecem explicitamente bloqueadas.

## Estado real
Protótipo V8 da caverna produzido em 3D independente. A marcha e o empurrão estão sendo refinados. Isso NÃO prova qualidade cinematográfica de uma série completa. Próximo marco é aprovação visual de uma sequência com elenco/atuação e linguagem inteligível, não número de cenas.


## Direção de arte e identidade visual — obrigatório para novas cenas (06/11/2026)

**Documento normativo:** [DIRECAO_VISUAL_E_BIBLIA_DE_PERSONAGENS.md](DIRECAO_VISUAL_E_BIBLIA_DE_PERSONAGENS.md).

- Antes de qualquer render, definir **CHAR_ID, modelo de rosto/silhueta, figurino por fase, paleta, pose e adereços** de cada ator. Nenhum clone entre papéis; o mesmo ator mantém sua identidade ao longo do filme.
- **Roteiro por plano é obrigatório**, com fala original/timecode, elenco, cenário completo e objetos, direção artística, câmera, blocking temporal (preparação → ação → consequência), continuidade e critérios de QC. Prompt genérico ou narração isolada não autoriza gerar cena.
- **Elmo e figurinos:** construir partes e fixações com proporções coerentes; crista, laterais e encaixe devem funcionar em close e perfil. Elmo heroico só na fase narrativa apropriada: Odisseu deve ser reconhecível mesmo sem ele.
- **Cenografia física e legível:** embarcação, cordames, pisos, terra, rocha, portas, interiores, vegetação e elementos secundários precisam de escala, materiais e função; não são enfeites sobrepostos.
- O visual pode ser estilizado como ilustração épica, **mas o filme final permanece 3D real**, com oclusão, profundidade e interação física, como determina a seção "Motor novo". Animatics 2D são intermediários, não entrega cinematográfica aprovada.
- **Fidelidade narrativa:** no canto XIII de Homero, os feácios deixam Odisseu **adormecido** na costa de Ítaca e partem; a sequência de passarela e desembarque consciente usada em testes 2D é adaptação, não o relato original. A voz original e a documentação de qualquer adaptação prevalecem sobre cenas demonstrativas.
- Acrescentar verificação visual da identidade e de detalhes de elmo, roupas, estruturas, props e atmosfera ao QC *fail closed*. Nenhuma alteração aqui autoriza publicação ou reclassifica renders existentes como aprovados.
