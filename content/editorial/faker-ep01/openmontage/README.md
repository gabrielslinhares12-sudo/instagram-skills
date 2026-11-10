# FAKER EP01 — Lendas do E-sport | OpenMontage (V4.9)

> Estado editorial: **PREPARAÇÃO / QC BLOQUEADO**. Nenhum vídeo está aprovado ou autorizado para publicação.

## Base técnica correta

- **Código-base externo:** [OpenMontageInc/OpenMontage](https://github.com/OpenMontageInc/OpenMontage)
- **Revisão verificada:** `fecb9a1e3cc23ef84de30b272059457a427f16f8` (main em 09/11/2026)
- **Pipeline principal:** `pipeline_defs/hybrid.yaml`, OpenMontage. Não usar `ui-ux-pro-max-skill` como motor de vídeo.
- **Recuperação de mídia:** aplicar a abordagem `documentary-montage` / retrieval-first apenas dentro do estágio de assets do `hybrid`; priorizar fontes documentais reais de eventos de esports.
- **Composição pretendida:** Remotion atelier para uma montagem original source-led com vídeo de campeonato real e gráficos discretos; avaliar Remotion/HyperFrames por disponibilidade antes de travar a execução no runtime.
- **Dependências gratuitas:** GitHub Actions, FFmpeg e recursos gratuitos do OpenMontage, sem API paga, sem Runway, sem Guthy.
- **Licença da ferramenta:** OpenMontage é AGPL-3.0. A referência externa não é uma declaração de que os VODs da Riot ou imagens de terceiros sejam livres para redistribuição.

## Material recuperado da produção anterior (Google Drive)

1. [Pacote de produção V4.7](https://drive.google.com/file/d/1aIZLTAQCHgrt4ytHka6HJtPcjjqoznr5/view) — contém `FAKER_SCENE_PLAN.json` com 24 tomadas, plano editorial, `qc_assets.py`, CSV de mídias, SRT e a narração original.
2. [Rasalgethi: corte editorial 298,513s](https://drive.google.com/file/d/1NJSjzN_PTej6AchYoVV7decismgrNBoB/view) — conservar arquivo WAV original.
3. [Legendas SRT alinhadas](https://drive.google.com/file/d/1yn6qZaasYb34QFpUoLQlVGi8qLXMcQDk/view) — manter sincronismo; reduzir densidade por unidade de leitura no QC sem alterar a voz.
4. [Decupagem e fontes documentais](https://drive.google.com/file/d/1RQb7DFjJgkEG3kBDaYYpMuijUDR-BpxF/view).
5. [Workflow V4.8 de avaliação privada de fontes](https://drive.google.com/file/d/1ljIM3854unam4fFw063bOPVXR5txHUCO/view). Trata-se de teste de disponibilidade de arquivos, não de licença de publicação.

## Contrato editorial

- Instagram Reels 9:16 / 2160x3840 / 60fps / duração-alvo 298,513s.
- Explicar primeiro o quadro **Lendas do E-sport**; apresentar Faker só depois; narrar trajetória e relevância nacional.
- Títulos mundiais: 2013, 2015, 2016, 2023, 2024, 2025. Outros trechos: derrota de 2017, DRX 2022, ZOFGK, seleção olímpica/asiática, dispensa do serviço militar convencional (não isenção completa), Doran em 2025, vida pessoal, Hall of Legends, Cheongnyong, Jogos Asiáticos de 2026 e Mundial 2026.
- Verificação externa em 10/11/2026: 2026 Jogos Asiáticos — ouro da Coreia do Sul e segunda medalha de ouro de Faker (Yonhap 02/10/2026); Mundial 2026 — T1 perdeu a semifinal por 1x3 contra BLG em 08/11/2026. Fonte de cada evento deve ser associada ao take correto.
- **Fonte primária:** gravações de jogos, transmissões, jogadores e cerimônias da ocasião correta. Cada clipe deve guardar origem, ano, enquadramento e licença/termos de uso. Referência em YouTube não equivale a download autorizado.
- **Proibido:** gráficos de HUD genérico, mapas inventados, Faker gerado por IA, deepfakes, fotos horizontais esticadas ou com zoom simulando filme, cartelas permanentes, azul neon, grids repetitivos.
- Identidade: TUE-MESTRE-01, fundo claro/marfim, preto, amarelo, vermelho em gráficos. A transmissão oficial mantém sua colorimetria original.
- Legendas **somente no rodapé**, até duas linhas, tipografia limpa com margem de segurança.
- Antes de renderizar exigir todas as 24 tomadas verificadas e pelo menos 80% da duração sustentada em vídeo real **em movimento**. Caso não haja autorização de alguma mídia, substituir por outra mídia com direitos verificáveis, jamais falsificar.

## Estado real

`QC_PRE_INSTALL.json` no pacote V4.7 registra **0/24 tomadas verificadas** e **0 segundos de footage real validado**. A narração e o roteiro existem, mas o MP4 final 4K/60fps ainda **não**. Esta branch contém contrato e preflight sem publicação, não afirma que o master foi renderizado.

### Próximo passo operacional

Importar os arquivos do Drive para um checkout autenticado do OpenMontage (fora desta branch), copiar o pacote V4.7 para `projects/tue-faker-ep01/`, rodar o preflight de ferramentas e o QC de fontes, selecionar as mídias reais e só então montar o corte fonte-principal, os gráficos, a mixagem e o master.

NÃO publicar ou agendar antes da revisão visual e autorização do proprietário.
