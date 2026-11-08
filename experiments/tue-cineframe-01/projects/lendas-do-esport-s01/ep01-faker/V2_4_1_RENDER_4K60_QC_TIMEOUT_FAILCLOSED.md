# Faker V2.4.1 — Controle de exportação 4K60, falha real e correção

**Data:** 08/11/2026
**Status:** EXPERIMENTO DE COMPOSIÇÃO DO SET DE TREINO; **REPROVADO COMO VÍDEO**. **Rasalgethi ausente**. Sem publicação ou agendamento.

## Trabalho preservado

- Cena S02 combina cenário vetorial original 2.5D com rig candidato do Faker (cabeça, torso, antebraços, mãos e objetos em camadas).
- Integração física por coordenadas: mãos se projetam em teclado/mouse na mesma cena, com arquitetura, cadeira e mesa em profundidade e oclusão.
- Render interno de **90 quadros distintos**, 3 s, 540×960/30 FPS, **não destinado a entrega**.
- Fonte SVG declarada 2160×3840; existe um *fotograma vetorial estático* nesse tamanho, que não comprova um vídeo 4K/60 final nem fidelidade ao conceito.

## Falha observada em render de alta resolução

Foi solicitada uma prova técnica de 1 segundo, 2160×3840, 60 FPS (60 quadros), H.264. O processo foi encerrado por limite de execução local. O arquivo parcial continha **41 quadros / 0,683333 segundos**, embora os metadados informassem 2160×3840/60 FPS. Por não atingir a duração e a contagem esperadas, foi **reprovado e removido**, nunca enviado como piloto.

Este ambiente de execução **não possui GPU NVIDIA acessível** (o comando `nvidia-smi` não existe). A simples listagem de um encoder `h264_nvenc` no FFmpeg não garante hardware disponível. Produção 4K60 em processamento contínuo não foi validada aqui.

## Correção do fluxo

O código `render_native_qc.py` agora usa saída provisória `.part.mp4`, verifica codec, dimensões, FPS exato, número de quadros, duração e ausência de quadros repetidos no fluxo de entrada. **Só renomeia para MP4 verificado se TODAS as verificações passarem**. Em falha comum, apaga o parcial e registra erro; se o processo for morto pelo host, qualquer arquivo remanescente conserva a extensão `.part.mp4` e não poderá ser confundido com entrega.

## Arquivos da V2.4.1

ZIP confirmado no Drive: https://drive.google.com/file/d/167V8hB6Zz_n9FKzA61gO5v-wGG_uZ7xe/view

Contém scripts reproduzíveis, fontes SVG locais, composição editável, imagem de QC estática e animação interna 540p30, além do relatório da falha 4K60. **Não contém render final ou clipe aprovado.**

Tamanho de arquivo local: **1.783.458 bytes**. SHA256: `503ddd73170f2c097ab5e3bc081a1e918e0fc1c46d071e280b9650df662111bc`.

A V2.4 anterior foi movida para `REPROVADOS`, deixando esta V2.4.1 como pacote de trabalho ativo. Ficha do personagem aprovada continua imutável:
https://drive.google.com/file/d/163C38f5RBR1mtf7r8z9FBYuQfrJubQnF/view

## Pendências de aprovação

- Personagem V2.3 ainda **não** alcança a fidelidade da ficha original, incluindo rosto, franja e detalhes do desenho.
- Pose sentada e atuação das mãos ainda precisam de correção anatômica e acabamento.
- Cenografia não passou em qualidade artística; não há os 14 takes aprovados.
- Voz Rasalgethi, trilhas sincronizadas, legendas finais e longa completo inexistentes.
- Estratégia de desempenho deve ser **testada e validada** em runner com GPU realmente acessível; não presumir que executar no GitHub basta.
- **NÃO liberar vídeo só porque tem metadados 4K/60 FPS.**

**Gate:** `NO_PREVIEW_UNTIL_QUALITY_PASS`. Nenhum arquivo experimental deve ser postado ou apresentado como filme final.
