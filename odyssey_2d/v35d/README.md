# A Odisseia — Regresso a Ítaca — Produção V35D (8/11/2026)

## O que é esta versão
Reconstrução da animação 2D em 16 cenas e 68 acontecimentos narrados, **sem publicar nas redes**. O vídeo original de 60s **Cavalo de Troia** é o estilo canônico: preservar Odisseu e cavalo extraídos do arquivo do proprietário, traço escuro, volumes desenhados planos, arquitetura micênica em várias camadas, ocre/azul-petróleo, figurinos consistentes.

### Origens verificáveis
- **Fonte do desenho**: `odyssey_2d/v35d/assets_base64/*.b64` — quatro PNGs EXATOS do proprietário, codificados apenas para preservação textual no GitHub. Decodificar com `base64 -d`. Não substituir por um Odisseu gerado ou redesenhado.
- **Motor e cenografia**: `render_v35d.py` + `environments_v35.py` + `special_acting_v35.py` + `focused_motion_v36.py`; as três bibliotecas de base estão neste diretório; `render_v34.py`, `puppet_original_v30.py` e `scenery_v28.py` permanecem em diretórios anteriores para importação, **não para reaproveitar trechos de vídeo**.
- **Voz**: WAV original Rasalgethi do usuário, 220,56s, SHA256 `9be8b79920b318c76f23874d38d12f4f77b46f8a9871833612ac1efa82b5d667`, disponível exclusivamente no repositório privado `tem-uma-explicacao`.
- **Contrato**: `odyssey_2d/v31/68_shot_story_contract.json`; pausas e texto por acontecimento em `odyssey_2d/v35c/story_sync_v35.py`.
- **Ações melhoradas especificamente na V35D**: rebanho sagrado, revelação da cicatriz por Euricleia, arco e flecha atravessando 12 machados, cama enraizada na oliveira, reencontro Penélope/Odisseu e reunião com Laertes. As outras cenas vêm de cenas v35c e devem seguir QC.

## Qualidade editorial (não presumir aprovação)
- Propriedade do usuário e estilo visual original **não bastam**: a animação precisa demonstrar atuação, escala física e ação conforme a narração, sem loops/movimentos sem propósito.
- `qa_v35d.py` decodifica a película, mede movimento real em cada tomada e procura planos praticamente duplicados, além de salvar pranchas de contato.
- Esse verificador **NÃO comprova** correspondência perfeita com o áudio nem garante qualidade cinematográfica: a revisão editorial humana é separada.
- Produção: desenho nativo 540×960 e export de QC 720×1280/30 FPS. **Não afirmar 4K/60 nativo.**
- Legendas seguem cláusulas textuais da gravação com marcação editorial; **não existe alinhamento ASR palavra a palavra validado**.
- Aprovação pendente. Não publicar/agendar e não substituir a referência canônica pelo material V27/V34.

## Execução isolada do vídeo com voz privada
A rotina `.github/workflows/odisseia-v35d-integral-2d-exact-troia-qc.yml` do repositório privado monta as bibliotecas, valida SHA e renderiza o filme em `private_media/odisseia_v35d/qc/`. A rotina independente `odisseia-v35d-movement-no-repeat-qc.yml` produz `MOVEMENT_QC_V35D.json` e contatos, sem aprovar automaticamente.

**Estado atual:** produção em andamento, teste completo em 8/11/2026, exportação final de revisão ainda sujeita a salvamento e controle de qualidade. Não confundir com filme aprovado.
