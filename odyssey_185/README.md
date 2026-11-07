# A ODISSEIA — O REGRESSO A ÍTACA / PRODUÇÃO V9

**Projeto:** Tem Uma Explicação • **Meta:** 185 s • 9:16 • mestre 2160×3840/60 fps • PT-BR • narrador **Rasalgethi / Google AI Studio**.

> **ALERTA EDITORIAL — 07/11/2026: prévia 3D integral de 220,56s REPROVADA.** Não publicar nem reutilizar as cenas; falha de narrativa, atuação e escala. Ver [REPROVACAO_VISUAL_V9_TESTE_220S_20261107.md](REPROVACAO_VISUAL_V9_TESTE_220S_20261107.md). O WAV Rasalgethi foi fornecido na conversa, com duração 220,56 s, mas o arquivo original ainda não está neste repositório; as marcações 185s do manifest são históricas, não sincronizadas ao áudio real. Próxima etapa é um teste de 10–15s com ação 3D inteligível, antes de recriar o filme.

## Estado verificável

- manifest_v9.json: 16 cenas contíguas cobrindo 0–185 s, roteiro integral do usuário.
- narracao_rasalgethi.txt: 446 palavras; **WAV Rasalgethi fornecido pelo usuário na conversa, ainda não transferido ao GitHub. Duração do áudio: 220,56 segundos.**
- shotplan_64_v9.json: 64 tomadas com ações e cortes independentes, preparação, execução e consequência.
- cast_props_v9.json: identidades persistentes e dimensões de objetos.
- render_hook_3d.py: **somente piloto novo da abertura (7 s)**, com geometria 3D no Blender; sem arte reprovada V5/V7.1.
- .github/workflows/odisseia-185-3d-hook-qc.yml: valida narrativa, instala Blender/FFmpeg no GitHub-hosted runner, renderiza seis imagens de controle e 210 quadros de prévia silenciosa; **nunca publica**.

O roteiro e os contratos não são um filme pronto. A produção só poderá ser declarada concluída após renderização das 16 cenas, áudio Rasalgethi genuíno, som, legendas e revisão visual. Até lá: **NÃO PUBLICAR**.

## Método escolhido

GitHub Actions (runner gratuito dentro da franquia) + Blender open source + assets 3D CC0 verificados + FFmpeg. Texturas PBR/HDRI podem ser obtidas de fontes CC0 como Poly Haven. Não utilizar Runway, Guthy, API paga, motion/slideshow, sobreposição de atores, nem personagens genéricos.

O usuário já forneceu o WAV integral da narração Rasalgethi no ChatGPT (220,56s). Transferir o áudio **já existente** para o ambiente de renderização; não tentar gerar uma nova voz. Ajustar as tomadas à duração real sem acelerar artificialmente a voz. A meta anterior de 185s deixou de ser aplicável à faixa original.

## Render reproduzível para teste NÃO publicável

Com Blender instalado, a partir da raiz do repositório:

    python3 odyssey_185/validate_manifest.py
    blender -b --threads 2 --python odyssey_185/render_hook_3d.py -- --stills
    blender -b --threads 2 --python odyssey_185/render_hook_3d.py -- --preview
    ffmpeg -y -framerate 30 -start_number 1 -i odyssey_185/out/frames/frame-%04d.png -c:v libx264 -pix_fmt yuv420p odyssey_185/out/ODISSEIA_V9_3D_ARCO_7S_QC.mp4

O teste tem 720×1280/30 fps antes do fator QC_PERCENT, inferior ao master para revisar geometria. Nunca reportar como 4K60 ou filme concluído.

## Gates de aprovação

1. Elenco e geografia próprios para cada tomada; Odisseu usa o mesmo rosto nas quatro versões.
2. Mãos, pés, objetos e cenário têm contato e oclusão coerentes.
3. Cavalo completo atravessa portão de Troia; Polifemo tem 5,5 m e pedra veda entrada.
4. Marcha sem patinação; Cila com seis cabeças e seis vítimas; doze machados; cama feita na oliveira viva.
5. Primeiro assistir sem som e compreender a ação. Depois sincronizar narração e legenda.
6. Falhou QC artístico/narrativo: corrigir e refazer a tomada. Nunca substituir por foto.
7. Nenhuma publicação, agendamento ou alteração dos conteúdos antigos.

## Versões antigas

V5/V7.1 rejeitadas. V8.6/V8.7 são apenas protótipos técnicos e não devem ser recicladas para produzir 185 s. A nova V9 mantém os artefatos e as publicações anteriores intactos.
