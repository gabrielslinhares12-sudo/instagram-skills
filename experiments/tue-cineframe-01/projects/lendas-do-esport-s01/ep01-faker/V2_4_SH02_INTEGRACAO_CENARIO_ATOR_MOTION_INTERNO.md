# EP01 Faker V2.4 — Composição 2.5D integrada SH02 / controle de atuação (08/11/2026)

**Status: projeto em produção, mas NÃO APROVADO. Não fornecer vídeo ao usuário.**

## Trabalho executado

- Unimos a maquete SVG da sala de treino de 2013 e o candidato de personagem em camadas do V2.3 em **uma mesma cena espacial 2D/2.5D**.
- A cena possui grupos separados para arquitetura de fundo, chão, objetos da mesa e monitor, cadeira atrás do personagem, luz reativa, controles de jogo e primeiro plano da mesa (oclusão).
- Reposicionamos o boneco dentro da cena usando coordenadas de mundo. O centro de mão esquerda projetado coincide com o teclado redesenhado, e o da direita coincide com o mouse. Isso corrige o problema do ator que ficava sobreposto sem relação espacial ao cenário.
- Em um teste **interno** de três segundos, o movimento passa por cabeça, tronco, dois braços, antebraços e mãos independentes, sem zoom de uma única imagem estática. Foram conferidos **90 fotogramas visualmente diferentes**.
- Geramos uma versão SVG editável e um fotograma em **2160×3840 renderizado de vetores**, não reamostrado de baixa resolução. O clipe para teste de movimento foi codificado deliberadamente em **540×960, 30 FPS** e nunca deve ser entregue como piloto, em respeito à regra de 4K60 para o cliente.
- O script foi tornado **reproduzível sem caminhos locais externos**. As duas dependências SVG usadas no layout vão junto com o código no ZIP.
- A fonte é para *study / blocking*. A ação da cena melhora em relação aos modelos isolados, mas não cumpre a exigência de semelhança facial e acabamento de cenário.

## Arquivos verificados

- Pasta interna de desenvolvimento V2: `https://drive.google.com/drive/folders/1ZcO0TNjW8Cf18BKRXHfqY8qJc_6SoAgE`
- Pacote V2.4: `https://drive.google.com/file/d/1Mu-DYOh1m0A-t7GnDxbDbj693lNqBXlA/view`
- Google Drive upload confirmado por leitura de metadados: **1.780.545 bytes**
- SHA-256 do ZIP: `61037f79092d1c2cc0cf1ae935db472e5b3230fcdcc54960ff3212477a5454a6`
- Arquivos principais:
  - `build_integrated_shot.py`
  - `assets/SET_A_TREINO_2013.svg`
  - `assets/FAKER_V3_SIT_PLAY_UNRIGGED.svg`
  - `outputs/SOURCE/FAKER_SH02_TRAINING_INTEGRATED_2_5D_4K.svg`
  - `outputs/INTERNAL_STILL_4K.png`
  - `outputs/INTERNAL_ACTOR_SCENE_3s_540p30_MOTION_QC.mp4`
  - `outputs/QC_REPORT.json`

## Revisão de qualidade REAL

| Elemento | Situação |
|---|---|
| Código de composição reproduzível | **OK** |
| Profundidade de arquitetura/mesa/cadeira | **BLOQUEIO TÉCNICO PARCIAL — experimental** |
| Mãos localizadas sobre teclado e mouse | **PASSO GEOMÉTRICO, sem aprovação de atuação orgânica** |
| 90 quadros diferentes com articulações independentes | **PASSO TÉCNICO INTERNO** |
| Fidelidade rosto/cabelo/óculos à ficha aprovada | **REPROVADO** |
| Anatomia/posição realista da pose sentada | **REPROVADO** |
| Tratamento cinematográfico e qualidade autoral de cenário | **REPROVADO** |
| Perfil, vista 3/4 e outras 13 tomadas finalizadas | **PENDENTE** |
| Narração Rasalgethi e legendas sincronizadas | **PENDENTE** |
| Filme completo 2160×3840 60 FPS com QA | **NÃO EXISTE** |
| Upload de vídeo aprovado ao Drive | **BLOQUEADO** |

A geração aqui **não** representa liberação para exibição do episódio. É comprovante de integração técnica, sem atribuir aprovação visual. Evitar claims de 4K60 de vídeo: somente o frame vetorial completo é 2160x3840; os 90 quadros do QC são 540x960/30fps.

## Próxima intervenção que realmente importa

1. Refazer Faker com vistas artísticas separadas **frente, perfil e 3/4** a partir do conceito aprovado, em vez de distorcer frontal genérica; bloquear o rig facial V2.2 até semelhança suficientemente alta.
2. Corrigir anatomia da mão/pulso/cotovelo e interação real com teclas/mouse; o *blocking* atual não substitui um animador de personagens.
3. Melhorar os sets para qualidade autoral cinematográfica e consistência da escala, evitando áreas grandes vazias.
4. Gerar Rasalgethi no Google AI Studio através da sessão autorizada e montar a história completa de ~112s.
5. Revisar o MP4 final em 2160×3840/60fps, origem nativa e QC editorial. Apenas então entregar link real do Drive.

**Sem publicação, agendamento, troca de voz ou gastos com API.**
