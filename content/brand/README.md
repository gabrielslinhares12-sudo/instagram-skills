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

## Processo implantado

1. **Produção de oito lâminas individuais:** preparar JSON de entrada com `post_id` e lista `slides`, cada uma com `headline`, `body`, `photo`, `credit`, `layout` (`hero`, `split` ou `diagram`), `callout` e `photo_secondary` diferente quando `split`.
2. **Renderização determinística:** `python3 scripts/render_instagram_carrossel.py --spec caminho/brief.json --out caminho/saida`. O programa usa o PNG original do repositório, verifica as fotos e cria `01.jpg` a `08.jpg` com `visual-manifest.json`; o campo `approved` começa **false**.
3. **Verificação técnica:** `python3 scripts/instagram_visual_standard.py verify-assets` e `python3 scripts/instagram_visual_standard.py verify-package --manifest caminho/saida/visual-manifest.json`. Ela confere hashes dos arquivos-base, proporção, ordem, paleta, painel claro, mascote original e hashes das oito páginas.
4. **Revisão humana obrigatória:** conferir cada imagem em tamanho de celular, fidelidade ao modelo real, português, qualidade da cena, licenças/créditos e fatos. A validação automática **não consegue atestar qualidade artística ou verdade factual por si só**.
5. **Autorização antes de publicar:** nenhum `approved=true` da semana 01–06/11 basta sozinho. Para carrossel, o pacote aprovado deve estar em `content/approved/<id>/visual-manifest.json` com `approved=true`, `visual_reviewed=true`, `owner_authorized=true`, `approval_note` não vazia e hashes iguais aos de `content/schedule.json`. O manifest gerado não marca esses campos automaticamente. Para meme/post avulso, é necessário `content/approved/<id>/approval.json` com revisão e autorização explícita e mesmos hashes. Para Reels, somente capa não basta: exigem MP4 e voz Rasalgethi revisados; atualmente a publicação é bloqueada até existir verificação própria.
6. **Gate no GitHub Actions:** `.github/workflows/instagram-editorial-quality.yml` roda em push/PR relevantes, `.github/workflows/instagram-scheduler.yml` verifica antes de publicar e o workflow legado de Halloween também passa pela barreira. A fila/ledger não são modificados por esta etapa.

## Comandos de manutenção

```bash
python3 -m pip install 'Pillow>=11,<13'
python3 scripts/instagram_visual_standard.py verify-assets
python3 scripts/instagram_visual_standard.py audit-queue
python3 -m unittest discover -s scripts -p test_instagram_visual_standard.py -v
```

**Situação editorial em 31/10/2026:** a semana de 1 a 6 de novembro permanece em revisão e sem autorização de publicação. A tirinha de Halloween das 12h de 31/10 tem recibo Meta; o carrossel das 18h enfrentou erro HTTP 400/código 200. O histórico aprovado de 31/10 é preservado; nada é reenviado por este processo.

O objetivo da barreira é impedir novamente que a produção faça somente uma capa bonita e publique sete páginas em outro estilo. O gerador oferece consistência estrutural; a revisão editorial continua indispensável.
