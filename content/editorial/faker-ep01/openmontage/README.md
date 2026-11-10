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


## V5.2 — montagem documental variada (10/11/2026, revisão privada)

- **MP4 disponível no Drive:** https://drive.google.com/file/d/1gpM57_LemHfcOypZ9OR8cLyPyuT1zCSV/view
- **Relatório de QC, decupagem, fontes e direitos:** https://drive.google.com/file/d/1mM4N7aUaH5gRGdmoK2rgYxuWXadngQvI/view
- **Fatos técnicos verificados:** 298,513s, 1080x1920, 30fps, H.264/AAC, 89.361.897 bytes, narração Rasalgethi original.
- **Mudança visual:** 43 tomadas, sendo 35 de arquivos em vídeo e 8 estáticas, 243,2s associados a arquivos audiovisuais; a entrevista de Faker de 2020 foi utilizada apenas uma vez, ~10s; vídeo 9:16 em tela cheia, sem miniaturas centrais nem molduras.
- **Fontes de apoio genéricas explicitamente separadas:** os jogadores e arenas de stock não representam Faker, T1 ou finais reais. Noticiários podem conter fotos e não equivalem a 243,2s de gameplay.
- **Materiais de arquivo reais por período:** 2013, 2015, 2016, 2017, 2023, 2024. Restam lacunas do campeonato 2022, final 2025 e premiações/eventos 2026; algumas cenas do corte são apenas apoio documental, jamais identificadas como captação da partida.
- **Rights gate:** clipes de partidas/noticiários/trailer não têm direito de republicação garantido; autores CC BY necessitam crédito. É apenas V5.2 de revisão, NÃO master 4K60 e NÃO aprovado para postagem.
- **Montagem técnica efetiva:** FFmpeg local, reaproveitando diretrizes OpenMontage hybrid; não representa execução integral do motor OpenMontage.
- **Publicação e agendamento:** nenhum, até autorização expressa após QC editorial.


## V5.3 — QUADRO A QUADRO, BANCO HD E REGRAS OBRIGATÓRIAS (10/11/2026)

**Atenção:** V5.3 é uma etapa de curadoria verificável, NÃO um novo MP4 e NÃO um master pronto.

- [Planilha de 87 falas, 31 blocos, 35 fontes e QC técnico](https://docs.google.com/spreadsheets/d/1E12C9epxjJd-kj-lzra0UsQjmHH7UbnD/edit)
- [ZIP com originais CC BY 3.0 Full HD e mapa de edição/checagens](https://drive.google.com/file/d/19j8FGohsFUmAruHycJVOxb4cUa4ws8Y0/view)
- Os 87 blocos SRT passam a ser a referência primária de cada cena, não uma lista solta de vídeos. Cada palavra que nomeia jogadores exige rosto real correto e compatível com o período; quando é citado o elenco, apresentar vídeo do grupo junto.
- **ZOFGK** = Zeus/Oner/Faker/Gumayusi/Keria (2022–24); **T1 2025** = Doran/Oner/Faker/Gumayusi/Keria; **seleção 2023** = Zeus/Kanavi/Faker/Chovy/Ruler/Keria. Nenhum desses elencos pode ser representado por entrevistas dos anos errados ou modelos genéricos.
- **Auditoria da biblioteca prévia:** 43 arquivos foram inventariados: 36 vídeos reduzidos/reconvertidos em 720×1280 ou 960×540, 4 arquivos Full HD com somente duas entrevistas duplicadas, 3 arquivos inválidos. Muitos dos vídeos de partida do Dailymotion exibiam resolução original **288p** ou **384p**, mesmo antes de serem ampliados em um vídeo 960x540: REJEITAR. Render 4K não devolve detalhes.
- **Novos ativos HD adquiridos:** 4 trechos distintos de 9s, fonte 1920×1080 original CC BY 3.0, entrevista de 2020 de Clid/Bdd/Ruler. Acervo compilado no ZIP também contém os originais licenciados de Faker, Keria e Bdd de 2020. São arquivos históricos com ano explícito; não usar para representar escalações atuais.
- **Qualidade:** procurar master original 4K (3840×2160) para gameplay; fonte 1920×1080 no mínimo para entrevistas, ainda sujeito a revisão de legibilidade do crop vertical. Reprovar arquivos 720p e abaixo (e upscales derivados). Não alegar 4K nativo apenas por configurar encoder.
- **Sem conteúdo enganoso:** não colocar personagens errados, times genéricos, estádio qualquer, imagem da final errada, entrevista antiga como celebração recente, vídeo que contém uma foto interna fingindo footage real, letras em caixas, miniaturas, 3D inventado, fotos com zoom.
- **Licenças:** YouTube/T1/Riot/Weverse não são liberados para download/repost apenas por serem públicos. O inventário da planilha distingue 'referência encontrada' de 'arquivo aprovado com direitos'. CC BY 3.0 exige atribuição e indicação de adaptação.
- **Bloqueio:** não renderizar um novo master e não publicar enquanto faltar confirmação *por tomada* de pessoa, evento/ano, arquivo original legível, enquadramento, origem e permissão de publicação.
