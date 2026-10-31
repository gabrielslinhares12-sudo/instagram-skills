# Produção local concluída — Lúmino: Por que o dólar sobe e desce?

**Data de produção:** 30/10/2026 (America/Fortaleza).  
**Status:** oito JPEGs finais renderizados e tecnicamente validados **somente no ambiente ChatGPT**. **NÃO HOSPEDADOS no GitHub, NÃO APROVADOS na fila, NÃO AGENDADOS e NÃO PUBLICADOS.** A URL atual do manifesto aponta para as quatro imagens antigas e **não pode ser liberada**.

## Entregáveis produzidos
- Oito JPGs 1080 × 1350 px, RGB, com leitura visual em miniatura revisada, sem numeração das lâminas.
- ZIP local: `/mnt/data/lumino_dolar_final_8_jpg.zip`
- Prévia local: `/mnt/data/lumino_dolar_final_previa.jpg`
- Arquivos separados: `/mnt/data/lumino_dolar_final_2026/dolar-01.jpg` a `dolar-08.jpg`
- Manifesto local com hashes: `/mnt/data/lumino_dolar_final_2026/hashes.json`
- Ilustração nova do Lúmino para a capa: `/mnt/data/a_clean_high_resolution_stylized_3d_cgi_illustra.png` (render 3D com filamento âmbar, olhos ciano, óculos e sobretudo; não reutilizar a imagem antiga de quatro páginas).

## Roteiro final de oito lâminas
1. **POR QUE O DÓLAR SOBE E DESCE?** — gancho: fluxos, riscos e expectativas.
2. **A COTAÇÃO NÃO É UM BOTÃO** — câmbio flutuante; exemplo estritamente hipotético US$ 1 = R$ 5,00 → R$ 5,50, alta de 10% do preço do dólar em reais.
3. **QUEM TRAZ E QUEM COMPRA?** — exportações, investimentos, crédito, importações, remessas e saída de capital; resultado não determinístico.
4. **JUROS IMPORTAM. MAS NÃO SOZINHOS.** — juros relativos, câmbio esperado, impostos, custos e risco.
5. **O MEDO TAMBÉM MEXE NO PREÇO** — risco percebido, crises e busca por segurança, sem causalidade automática.
6. **O BANCO CENTRAL PODE INTERVIR?** — pode manter funcionamento regular e prover liquidez, sem defender cotação fixa.
7. **DÓLAR ALTO = TUDO MAIS CARO?** — repasse parcial e desigual a preços.
8. **ENTÃO, O QUE VOCÊ DEVE OLHAR?** — síntese de fluxos, juros, risco, liquidez, BC e inflação.

## Hashes SHA-256 finais
| Arquivo | Bytes | SHA-256 |
|---|---:|---|
| `dolar-01.jpg` | 424204 | `a4ff4c311cd468abcf77eaea373c4a6a5f2437efde772c565047fe3f9b370903` |
| `dolar-02.jpg` | 282169 | `2efd78f06848057e37d5f18ed40059df87e5966e2bbdf6dbab977df6d7be004c` |
| `dolar-03.jpg` | 277137 | `4f61b0265a720f69c032f82db582b65fcae92797ecc5b2b54933ec28b8302d50` |
| `dolar-04.jpg` | 284591 | `24d5dd68799d6279314e521efc8d89f791cff2cd45d4c48e2c0829dcd05d2f26` |
| `dolar-05.jpg` | 301677 | `8b2c3a4b7898f85fff3ad28d55d4243713f387d8c2d144fc365a3d76d0172e8b` |
| `dolar-06.jpg` | 262658 | `6df042bd4bd66525f5c734c116c6c73fcef239da94928a6859ffb9c5f67f9d45` |
| `dolar-07.jpg` | 268090 | `6fe13155968d34eb4310beb5883b7f051a45404a7b6793354a40fd84247e62c9` |
| `dolar-08.jpg` | 297423 | `9e5d9f5cc7f594d6b29115da4374e9a80fd78620c0d1cd1a55bd4904dba73d7f` |

## Legenda final sugerida
Por que o dólar sobe mesmo quando ninguém parece estar comprando dólares? 💵

A cotação não depende só de turistas e casas de câmbio. Ela reage a fluxos internacionais, decisões de investimento, juros, riscos e expectativas sobre o Brasil e o mundo.

Quando o dólar vai de R$ 5,00 para R$ 5,50, **num exemplo hipotético**, ele ficou 10% mais caro em reais. Mas juros mais altos não garantem dólar mais barato, nem uma alta de 10% do dólar significa que todos os produtos subirão 10%.

O Brasil adota câmbio flutuante. O Banco Central pode atuar para garantir o funcionamento do mercado, mas não define uma cotação fixa.

Deslize pelas oito lâminas e salve para interpretar a próxima notícia sobre câmbio.

#Dólar #EconomiaBrasileira #EducaçãoFinanceira #Câmbio

## Fontes oficiais verificadas
- Banco Central, FAQ sobre intervenções: https://www.bcb.gov.br/meubc/faqs/p/por-que-o-banco-central-intervem-no-mercado-de-cambio
- Banco Central, política cambial: https://www.bcb.gov.br/estabilidadefinanceira/politicacambial
- Banco Central, estudo sobre repasse cambial (março de 2026): https://www.bcb.gov.br/content/ri/relatorioinflacao/202603/rpm202603b8p.pdf

## Próximo passo de produção
1. **Não reusar os quatro JPGs antigos** nem trocar os links para imagens não verificadas.
2. Transferir os oito JPGs exatos a `content/media/2026-11-02-lumino/` via meio que realmente aceite binários. Tentativas de egressar o JPEG de Halloween por conectores Canva/Picsart retornaram `BLOCKED_FILE_REFERENCE`, e o container não resolve DNS público; portanto a limitação continua sem solução nesta execução.
3. Confirmar URL pública HTTPS em SHA de commit fixo, comparar MIME, dimensão e SHA256 dos oito bytes com a tabela.
4. Revalidar `content/publication-state.json`, workflow, preflight Meta e janela de 02/11/2026 12h America/Fortaleza; só então atualizar `content/schedule.json` com 8 URLs e `approved=true`.
5. Enquanto não houver hospedagem verificada, `approved=false`. **Não há confirmação de agendamento/publicação.** Continuar a produção sequencial da próxima pauta sem reenviar itens incertos.
