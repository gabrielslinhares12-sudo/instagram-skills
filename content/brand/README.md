# PADRÃO MESTRE ATIVO: [TUE-MESTRE-01](TUE-MESTRE-01.md)

**Sempre aplicar em qualquer conteúdo Instagram TUE.** Comando: `ATIVAR TUE-MESTRE-01`. Prevalece sobre regras contraditórias abaixo. **Sem numeração visível; “Arraste →” legível, obrigatório em todas as lâminas com continuação e ausente na última. Modelo 1 editorial exclusivo.** Nenhuma aprovação por QC exclusivamente técnico.

# Instagram TUE — PADRÃO VISUAL CANÔNICO (obrigatório)

**Fonte única para geração e validação:** [padrao-visual.json](padrao-visual.json).

## Arquivos reais no repositório

- [Lúmino original PNG — imutável](lumino-original.png) — SHA-256 `f905d801f013c2e253b8a17ae3bc1279b57022d1b805baa632f291a3b73e0c1b`.
- [Contrato editorial e visual TUE-MESTRE-01](TUE-MESTRE-01.md) — padrão aprovado em 01/11; **não existe imagem-modelo de oito painéis ativa**.

As cópias existentes em `content/visual-standard/assets/` são espelhos, não uma segunda identidade visual. O verificador exige que o **PNG canônico do Lúmino** e seu espelho sejam byte a byte idênticos, além da presença do contrato TUE-MESTRE-01. Nenhuma grade de oito painéis pode ser carregada como referência vigente.

## Características que não podem mudar

Cada carrossel tem **2 a 20 imagens JPEG distintas, 1080×1350 px**, em quantidade definida pelo roteiro, jamais uma única imagem 2×4. Fundo **papel claro texturizado**, com fotografia/ilustração contextual ocupando espaço substancial. Manchete preta, grande e condensada, sobre pincelada **amarela irregular**, com destaques vermelhos; cartões claros e legíveis, dados/ícones informativos, indicadores discretos da página. Variar enquadramento de cenas em **todas as páginas necessárias ao conteúdo**, sem número fixo de lâminas. O nível gráfico das internas precisa acompanhar a capa.

O Lúmino é **uma camada proveniente do PNG original**, nunca regenerado: cabeça de lanterna de vidro e metal dourado, lâmpada acesa, óculos redondos, olhos ciano, lupa, luvas e sobretudo cáqui; **sem boca nem pernas**. O teste confere amostras dos pixels do PNG original sobrepostos no resultado e rejeita alterações relevantes.

**Atenção:** os dados eleitorais da imagem-modelo são exemplos de composição, **não fatos a reutilizar**. O roteiro deve ser conferido separadamente.

## Execução obrigatória: direção artística primeiro, empacotamento depois

**PROIBIDO usar o script `render_instagram_carrossel.py` na entrega final.** Seu template fixo `hero/split/diagram` produz apenas **rascunhos técnicos**, mesmo que passe em testes de cor, tamanho e mascote. O GitHub rejeita qualquer tentativa de promover esses rascunhos para uma publicação nova. O único padrão em vigor é **TUE-MESTRE-01 (01/11)**. O arquivo antigo de oito painéis é obsoleto e não participa da geração, validação nem aprovação.

1. **Criar de 2 a 20 artes prontas, uma de cada vez, no mesmo processo criativo.** Para cada página, usar **TUE-MESTRE-01**, o PNG canônico do Lúmino, o briefing específico do tema e a identidade editorial. Gerar uma **imagem individual completa**, revisar conteúdo, tipografia, cenário e qualidade da página no tamanho de um celular. Não produzir nem recortar colagens de referência: cada peça deve ser uma arte individual final, 1080×1350, com apresentação própria e conteúdo novo.
2. **Sem intervenção criativa do empacotador.** As artes devem ser JPGs finais `1080×1350`, com o Lúmino canônico visivelmente integrado. Caso uma arte não tenha esses atributos, refazer **aquela página**, não substituí-la por um template genérico.
3. **Empacotar sem re-renderização.** Criar um `brief.json` na pasta das imagens:
   ```json
   {
     "post_id": "identificador-seguro",
     "slides": [
       {
         "file": "arte-01.jpg",
         "headline": "Título revisado",
         "layout": "hero",
         "mascot_box": [18, 973, 274, 284],
         "credit": "Ilustração editorial produzida para o canal"
       }
     ]
   }
   ```
   A lista **deve conter tantas entradas quantas forem necessárias (2 a 20)**, e `mascot_box` contém a posição REAL do PNG canônico em cada uma (o exemplo acima não é uma posição obrigatória para todas as páginas). Campos `layout` (`hero/split/diagram`) servem somente para identificação e verificação, não autorizam um script a desenhar a página.
4. **Executar o novo empacotador** com as artes finais:
   ```bash
   python3 scripts/package_individual_carousel.py --spec artes/brief.json --out entrega/carrossel
   python3 scripts/instagram_visual_standard.py verify-package --manifest entrega/carrossel/visual-manifest.json
   ```
   O comando **copia todos os JPEGs byte a byte**, preserva seus SHA-256, rejeita dimensões erradas e duplicações quase idênticas e verifica o PNG canônico. A identidade TUE-MESTRE-01 é aplicada sem um modelo de oito quadros. A prévia `PREVIA-NN-ARTES.png` (NN = total de páginas) é construída **somente a partir dos JPGs finais**. O validador recompõe essa prévia para impedir o truque de uma colagem bonita e oito JPEGs diferentes.
5. **Inspeção editorial individual é obrigatória.** É necessário avaliar todas as páginas visualmente, inclusive a consistência com o modelo, a leitura no celular, fatos, direitos das imagens, texto sem cortes e sobreposições. Nenhum comparador automático atesta criatividade, identidade estética completa ou verdade factual com certeza. Quando qualquer página falhar, reprovar o carrossel e corrigir o painel; jamais promover o pacote parcialmente.
6. **Bloqueio antes da Meta.** Para carrosséis novos, `audit-queue` exige `production_mode=individually_art_directed_v1`, prévia recomputável, hashes válidos, `approved=true`, `visual_reviewed=true`, `owner_authorized=true`, anotação de aprovação não vazia e hashes idênticos aos da fila. `approved`, `visual_reviewed` e `owner_authorized` vêm **false** no pacote recém-gerado: não se tornam verdadeiros por completar os testes. Publicar exige autorização expressa do proprietário. O processo não altera `content/schedule.json` nem `content/publication-state.json` durante a produção.
7. **Verificação automática:** `.github/workflows/instagram-editorial-quality.yml` testa a identidade canônica, a integridade da fila e as prévias derivadas dos JPEGs. `.github/workflows/instagram-scheduler.yml` chama `audit-queue` antes de publicação, sem alterar o workflow legado do Halloween.

## Arquitetura de execução 100% na nuvem — sem PC

- **Executor:** GitHub Actions `ubuntu-latest` (runner hospedado pelo GitHub), sem dependência do GUTHY, Android, ADB, Appium ou TinyFish.
- **Publicação automática oficial:** usar Instagram Graph API para carrossel sem música, somente quando a estratégia editorial autorizar expressamente esse formato; respeitar o limite de itens da API e não alterar a aprovação de conteúdo.
- **Carrossel com música nativa:** a API oficial não oferece um campo de música para carrosséis. O pipeline não deve simular que adicionou música nem publicar sem música quando o post foi marcado para música obrigatória.
- **Reel com música:** é uma modalidade alternativa e distinta; exige arquivo MP4, direitos de uso de áudio e conexão elegível com a API de áudio ou trilha incorporada licenciada. Não converter carrossel em Reel sem aprovação editorial.
- **Credenciais:** armazenar em GitHub Secrets e renovar quando expirarem. Um erro de permissões (como Meta code 200) deve bloquear o envio, gerar diagnóstico e alerta, sem tentar repetidamente publicar ou alterar conta.
- **Entrega:** registrar ID/permalink verdadeiro e status `published` apenas após confirmação da Meta; quando não houver confirmação, manter pendente para revisão de duplicidade.
- **Recuperação do Halloween 31/10 18h:** preservar as oito artes e a legenda. Corrigir a conexão Meta, conferir se já foi publicado e então decidir uma publicação atrasada. Não marcar sucesso sem recibo.
- **Limitação estrutural:** não existe garantia de carrossel de fotos com música nativa 100% automatizado por GitHub Actions usando apenas a API oficial da Meta. A arquitetura deve registrar esse bloqueio, não mascará-lo com outro formato.

## Distribuição preferencial: carrossel com música nativa (elegibilidade Reels)

**Regra por padrão:** gerar fotos individuais em carrossel, na quantidade editorialmente necessária (2–20), sem converter em MP4. **Ao publicar no aplicativo Instagram no celular:** criar uma **Publicação** (não Reel), selecionar os JPGs na ordem, tocar em **Adicionar música**, escolher faixa disponibilizada para a conta e trecho, revisar texto e publicar apenas após autorização. O resultado continua sendo um carrossel deslizável de fotos, mas fica **elegível** a aparecer na experiência/aba Reels, conforme recomendação pública de Adam Mosseri; distribuição a não seguidores **não é garantida**. A aba Reels do perfil e o feed de descoberta não são conceitos intercambiáveis.

**Limite técnico inegociável:** o Instagram permite até 20 páginas no aplicativo, porém nosso publicador via API Meta recebe somente 2–10 JPGs por carrossel e **não consegue anexar uma faixa da biblioteca nativa a carrosséis**. Portanto:
- Os pacotes novos recebem `distribution_mode=native_music_carousel`, `music_status=pending_selection_in_instagram_app` e uma lista de verificação `PUBLICACAO-NATIVA-COM-MUSICA.txt`.
- Se o carrossel tiver música nativa obrigatória, a chamada ao publicador automático é **bloqueada** por `verify_publication_route`. Um cron de GitHub não deve publicar carrossel silencioso e chamá-lo de Reel.
- Publicar sem música por API só é permitido com mudança explícita do manifesto para `distribution_mode=api_carousel_without_native_music`, com `owner_authorized_without_music=true`, revisão editorial e autorização expressa. Nunca aplicar esse desvio automaticamente.
- **A decisão do formato permanece editorial.** Um Reel real exige vídeo MP4; criar Reel estático ou animado não é requisito para alcançar a aba Reels com carrossel musical. Se o Instagram não disponibilizar música na conta, a publicação musical permanece pendente: não inventar faixa, não forçar áudio sem licença e não declarar sucesso.
- Medir alcance de não seguidores, compartilhamentos, salvamentos e visualizações quando o Instagram estiver conectado a uma ferramenta de análise. A elegibilidade Reels não garante melhora mensurável.

Fontes: [Meta — música em carrosséis](https://about.fb.com/br/news/2023/08/mais-formas-de-criar-e-colaborar-com-amigos-no-instagram/amp/), [fala de Mosseri sobre elegibilidade para Reels](https://www.socialmediatoday.com/news/ig-chief-recommends-posting-carousels-improve-reach/730232/), [limitações da API](https://help.metricool.com/api-limitations-per-social-network-n7zlr).

## Comandos de manutenção

```bash
python3 -m pip install 'Pillow>=11,<13'
python3 scripts/instagram_visual_standard.py verify-assets
python3 scripts/instagram_visual_standard.py audit-queue
python3 -m unittest discover -s scripts -p test_instagram_visual_standard.py -v
```

**Situação editorial em 31/10/2026:** a semana de 1 a 6 de novembro permanece em revisão e sem autorização de publicação. A tirinha de Halloween das 12h de 31/10 tem recibo Meta; o carrossel das 18h enfrentou erro HTTP 400/código 200. O histórico aprovado de 31/10 é preservado; nada é reenviado por este processo.

O objetivo da barreira é impedir novamente que a produção faça somente uma capa bonita e publique páginas internas em outro estilo. O gerador oferece consistência estrutural; a revisão editorial continua indispensável.
