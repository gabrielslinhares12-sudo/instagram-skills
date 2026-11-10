# Faker EP01 — OpenMontage hybrid V4.7 (10/11/2026)

**Status:** pacote de PRODUÇÃO preparado e testado; NÃO É O MASTER FINAL. NÃO PUBLICAR.

## Pacote executável da integração
**[OpenMontage adapter + narração Rasalgethi 298.512875s + SRT + 24 cenas + ferramentas de preparação e QC](https://drive.google.com/file/d/1aIZLTAQCHgrt4ytHka6HJtPcjjqoznr5/view)**

SHA-256 do ZIP: `d1f357a089c9dda876dff1ca37122872d972054f949fa4db0d9cf36b78c69abd`.

Arquivos: `PRODUCAO_OPENMONTAGE.md`, `FAKER_SCENE_PLAN.json`, `ASSETS_POR_CENA.csv`, `LEGENDAS_CORRIGIDAS.srt`, `NARRACAO_RASALGETHI_ORIGINAL_CORTE_4m58.wav`, `prepare_openmontage.py`, `qc_assets.py`, `QC_PRE_INSTALL.json`, `README.txt`.

**Verificações realizadas:** FFprobe áudio PCM mono 24kHz 298.512875s; linha do tempo de 24 cenas contíguas, término 298.55s; SRT final em 4:58.101; preflight `qc_assets.py` retornou FAIL com 24 faltas de mídias e 1 falha de cobertura <80% de vídeo real, como deveria. O gate exige identificação do ano de cada cena e mídia real, não sintética. Não há clipes reais baixados neste pacote.

## Escolha técnica auditada
- OpenMontage principal: https://github.com/OpenMontageInc/OpenMontage
- Guia: https://github.com/OpenMontageInc/OpenMontage/blob/main/AGENT_GUIDE.md
- **Base correta: [`pipeline_defs/hybrid.yaml`](https://github.com/OpenMontageInc/OpenMontage/blob/main/pipeline_defs/hybrid.yaml)** — vídeo narrado com filmagem real dominante e suporte gráfico mínimo, produção estável.
- **Apenas reutilizar pesquisa de mídia** da [documentary-montage beta](https://github.com/OpenMontageInc/OpenMontage/blob/main/pipeline_defs/documentary-montage.yaml): `direct_clip_search` e recuperação corpus. **Não usar a pipeline documental inteira**, porque seu próprio diretor descreve peças sobretudo sem narração de 30–180s e a voz do Faker dura quase 5 minutos.
- Remotion/FFmpeg; sem API paga, sem nova TTS. A instalação local de OpenMontage exige Python 3.10+, FFmpeg, Node em versão suportada/corrigida (22.23.4+, 24.22.1+ ou 26.12.1+, conforme README), e dependências do repositório. Na sessão atual, o host não permitiu git clone externo por falha de DNS; portanto a engine OpenMontage **não foi executada**.

## Contrato visual irrevogável
1. Para **fotografias**: fonte original `width < height` e proporções conservadas; foto horizontal/quadrada, stretch, `fit=fill`, blur-fill e falso Ken Burns **REPROVADOS**. Vídeos horizontais de partidas podem ser incluídos em quadro vertical com layout editorial adequado para não destruir o HUD/Rift.
2. Ao menos 80% **de tempo de cenas em movimento reais**, não cartelas e imagens de stock irrelevantes. Uma transmissão de 2015 não pode ilustrar o título de 2023. Guardar ano e equipe comprovados para todas as fontes.
3. Mostrar os seis títulos 2013, 2015, 2016, 2023, 2024, 2025; derrotas de 2017 e 2022; ZOFGK; Dream Team Jogos Asiáticos 2023; formação com Doran em 2025; vida social e 2026.
4. Rasalgethi e SRT já prontos, não substituir voz; 2160×3840 / 60 FPS só para export, origem histórica pode ser inferior. Identidade TUE-MESTRE-01, textos apenas de identificação e legenda inferior; não criar painéis e UI genérica.
5. Bloquear qualquer renderização rotulada `FINAL` antes de preencher todas as 24 fontes, rever provenance/licença, aprovar composição, validar áudio/legendas e QC; não publicar sem aprovação explícita.

## Uso no PC/runner
1. `git clone https://github.com/OpenMontageInc/OpenMontage.git` no ambiente com acesso externo.
2. Seguir instruções de `make setup` no repositório upstream, sem adicionar API paga.
3. Extrair pacote e executar `python prepare_openmontage.py /caminho/para/OpenMontage`.
4. No projeto OpenMontage, pedir ao agente para seguir `projects/tue-faker-ep01/PRODUCAO_OPENMONTAGE.md` com pipeline `hybrid` e o `FAKER_SCENE_PLAN.json`.
5. Preencher `media/` com vídeos reais, registrar fontes no JSON; executar `python qc_assets.py FAKER_SCENE_PLAN.json --media-root media` antes do render. A ferramenta bloqueia se faltar origem, ano, vídeo ou aprovação.

O usuário já reprovou V4.2 e a versão baseada em fotos horizontais. Não reciclar nenhuma das duas como master.
