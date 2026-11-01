# Instagram TUE — PADRÃO VISUAL CANÔNICO (obrigatório)

**Fonte única para geração e validação:** [padrao-visual.json](padrao-visual.json).

## Arquivos reais no repositório

- [Lúmino original PNG — imutável](lumino-original.png) — SHA-256 `f905d801f013c2e253b8a17ae3bc1279b57022d1b805baa632f291a3b73e0c1b`.
- [Modelo visual de 8 páginas aprovado pelo proprietário](modelo-oficial-carrossel-8-paineis.png) — SHA-256 `6d3dcdebcea7006b4f1934e74c19618951453b000aea9deb6968add55d5f0e63`.

As cópias existentes em `content/visual-standard/assets/` são espelhos, não uma segunda identidade visual. O verificador exige **ambos os pares com SHA idênticos**.

## Características que não podem mudar

Cada carrossel tem **8 imagens JPEG distintas, 1080×1350 px**, jamais uma única imagem 2×4. Fundo **papel claro texturizado**, com fotografia/ilustração contextual ocupando espaço substancial. Manchete preta, grande e condensada, sobre pincelada **amarela irregular**, com destaques vermelhos; cartões claros e legíveis, dados/ícones informativos, indicadores discretos da página. Variar enquadramento de cenas ao longo das 8 páginas. O nível gráfico das internas precisa acompanhar a capa.

O Lúmino é **uma camada proveniente do PNG original**, nunca regenerado: cabeça de lanterna de vidro e metal dourado, lâmpada acesa, óculos redondos, olhos ciano, lupa, luvas e sobretudo cáqui; **sem boca nem pernas**. O teste confere amostras dos pixels do PNG original sobrepostos no resultado e rejeita alterações relevantes.

**Atenção:** os dados eleitorais da imagem-modelo são exemplos de composição, **não fatos a reutilizar**. O roteiro deve ser conferido separadamente.

## Execução obrigatória: direção artística primeiro, empacotamento depois

**PROIBIDO usar o script `render_instagram_carrossel.py` na entrega final.** Seu template fixo `hero/split/diagram` produz apenas **rascunhos técnicos**, mesmo que passe em testes de cor, tamanho e mascote. O GitHub rejeita qualquer tentativa de promover esses rascunhos para uma publicação nova.

1. **Criar 8 artes prontas, uma de cada vez, no mesmo processo criativo.** Para cada página, entregar o modelo de 8 painéis aprovado, a PNG original do Lúmino, o briefing do tema e a identidade editorial. Gerar uma **imagem individual completa**, revisar conteúdo, tipografia, cenário e qualidade da página no tamanho de um celular. A composição 2×4 serve apenas como *direção artística*; recortar seus painéis de baixa resolução e aumentá-los para 1080×1350 não produz uma arte de alta qualidade.
2. **Sem intervenção criativa do empacotador.** As oito artes devem ser JPGs finais `1080×1350`, com o Lúmino canônico visivelmente integrado. Caso uma arte não tenha esses atributos, refazer **aquela página**, não substituí-la por um template genérico.
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
   A lista **deve conter 8 entradas**, e `mascot_box` contém a posição REAL do PNG canônico em cada uma (o exemplo acima não é uma posição obrigatória para todas as páginas). Campos `layout` (`hero/split/diagram`) servem somente para identificação e verificação, não autorizam um script a desenhar a página.
4. **Executar o novo empacotador** com as artes finais:
   ```bash
   python3 scripts/package_individual_carousel.py --spec artes/brief.json --out entrega/carrossel
   python3 scripts/instagram_visual_standard.py verify-package --manifest entrega/carrossel/visual-manifest.json
   ```
   O comando **copia os oito JPEGs byte a byte**, preserva seus SHA-256, rejeita dimensões erradas e duplicações quase idênticas, verifica as cores e a presença do PNG original. A prévia `PREVIA-8-ARTES.png` é construída **somente a partir dos oito arquivos finais**. O validador recompõe essa prévia para impedir o truque de uma colagem bonita e oito JPEGs diferentes.
5. **Inspeção editorial individual é obrigatória.** É necessário avaliar as oito páginas visualmente, inclusive a consistência com o modelo, a leitura no celular, fatos, direitos das imagens, texto sem cortes e sobreposições. Nenhum comparador automático atesta criatividade, identidade estética completa ou verdade factual com certeza. Quando um dos oito painéis falhar, reprovar o carrossel e corrigir o painel; jamais promover o pacote parcialmente.
6. **Bloqueio antes da Meta.** Para carrosséis novos, `audit-queue` exige `production_mode=individually_art_directed_v1`, prévia recomputável, hashes válidos, `approved=true`, `visual_reviewed=true`, `owner_authorized=true`, anotação de aprovação não vazia e hashes idênticos aos da fila. `approved`, `visual_reviewed` e `owner_authorized` vêm **false** no pacote recém-gerado: não se tornam verdadeiros por completar os testes. Publicar exige autorização expressa do proprietário. O processo não altera `content/schedule.json` nem `content/publication-state.json` durante a produção.
7. **Verificação automática:** `.github/workflows/instagram-editorial-quality.yml` testa a identidade canônica, a integridade da fila e as prévias derivadas dos JPEGs. `.github/workflows/instagram-scheduler.yml` chama `audit-queue` antes de publicação, sem alterar o workflow legado do Halloween.

## Comandos de manutenção

```bash
python3 -m pip install 'Pillow>=11,<13'
python3 scripts/instagram_visual_standard.py verify-assets
python3 scripts/instagram_visual_standard.py audit-queue
python3 -m unittest discover -s scripts -p test_instagram_visual_standard.py -v
```

**Situação editorial em 31/10/2026:** a semana de 1 a 6 de novembro permanece em revisão e sem autorização de publicação. A tirinha de Halloween das 12h de 31/10 tem recibo Meta; o carrossel das 18h enfrentou erro HTTP 400/código 200. O histórico aprovado de 31/10 é preservado; nada é reenviado por este processo.

O objetivo da barreira é impedir novamente que a produção faça somente uma capa bonita e publique sete páginas em outro estilo. O gerador oferece consistência estrutural; a revisão editorial continua indispensável.
