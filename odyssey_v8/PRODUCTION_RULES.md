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
