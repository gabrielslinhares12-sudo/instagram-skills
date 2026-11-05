# TUE Motion

Base de animação de cenas para Instagram TUE, usando Remotion. Exportação 9:16,
60 fps, composição 2160×3840. Prévia a 1080×1920. Não publica nem altera a fila.

## Sem computador local

O workflow **TUE Motion - render sem PC** usa `ubuntu-latest` hospedado pelo
GitHub. Na aba Actions, execute `Run workflow` e escolha `preview` ou `4k`.
O MP4 fica no artifact do run durante três dias. Após integrar na branch padrão,
o disparo manual estará disponível. PRs que alteram esta base renderizam a demo.
Não usa runner local, API paga de vídeo nem serviço AWS Lambda.

O uso de runners padrão em repositórios públicos é gratuito segundo o GitHub;
armazenamento e outras modalidades têm limites próprios. Remotion permite uso
comercial gratuito por indivíduos e empresas de até três pessoas, sujeito aos
termos. Não é uma garantia de gratuidade para qualquer tamanho de operação.

## O que está implementado

- Cenas sequenciais com duração configurável em JSON.
- Três ambientes vetoriais originais de demonstração: laboratório, cidade e
  observatório. São ilustrações editoriais; não representam registros reais.
- Entrada, flutuação discreta e inclinação de descoberta do PNG original.
- Câmera com aproximação, deslocamento lateral ou enquadramento estático.
- Fundo opcional de fotografia/vídeo, cobrindo 9:16 sem esticar.
- Narração global importada e efeitos sonoros por cena, com volume e duração.
- Uma legenda por vez, sem caixa preta; título limitado a três segundos.
- Validação de intervalos, assets locais, IDs e integridade do Lúmino.
- Fonte Barlow Condensed empacotada localmente, sem dependência de Google Fonts
  durante o render. Licença OFL no pacote `@fontsource/barlow-condensed`.

## Primeiro teste

```bash
cd motion
npm ci
npm run check
npm run preview
npm run render
npm run studio
```

A demo `examples/demo.json` dura 12 segundos e não tem áudio. Serve para testar
cenários e composição, não é um Reel editorial final aprovado. A direção de arte
precisa ser revisada contra `../content/brand/TUE-MESTRE-01.md` antes de cada post.
O personagem canônico tem resolução própria: exportar 4K não inventa detalhe.
Não existe rig de braços, novas poses nem sincronização labial nesta versão;
o desenho original não é recortado, redesenhado ou deformado.

## Novo episódio

Duplique `examples/demo.json`. Mantenha `title`, `narration` e `scenes`.
Cada cena possui `id`, `duration` em segundos, `environment`, `actor`, `side`,
`camera`, `captions` e opcionalmente `background` / `sounds`.
As legendas e sons usam segundos relativos ao início da própria cena.
Os arquivos adicionais devem estar em `public/` e os caminhos são relativos a
essa pasta. `prepare-assets` não apaga arquivos extras. Para renderizar na nuvem,
os assets devem estar no checkout (por exemplo, `git add -f motion/public/audio.wav`)
ou ser baixados por etapa explícita de preparação com origem/licença verificadas.
Nunca adicionar credenciais.

```json
{
  "background": {"kind":"video", "src":"footage/cena.mp4", "credit":"Autor, URL e licença"},
  "sounds": [{"src":"audio/efeito.wav", "start":1, "duration":1.5, "volume":0.25}]
}
```

```bash
npm run preview -- --props=examples/meu-episodio.json
```

Para narração, informar `narration: "audio/voz.wav"` após gerar/baixar Rasalgethi
pelo site Google AI Studio. Esta base importa áudio; não gera voz nem automatiza
login. Ajustar duração e legendas ao áudio real. Conferir som e sincronismo no
MP4, principalmente em cortes. Fotografias/vídeos exigem inspeção do recorte;
`cover` não garante enquadramento correto por si só.

## Escolha tecnológica

Motion (`motiondivision/motion`) é uma biblioteca MIT de animação web.
Remotion fornece composição e renderização de vídeos com tempo determinado por
quadro. A documentação não oferece integração pronta com Framer Motion;
combinar ambos adicionaria trabalho de sincronização sem necessidade nesta base.

Referências consultadas em 04/11/2026:
- https://github.com/motiondivision/motion
- https://www.remotion.dev/docs/render
- https://www.remotion.dev/docs/third-party
- https://www.remotion.dev/docs/license/pricing
- https://docs.github.com/en/billing/concepts/product-billing/github-actions
## Piloto: O Último Sinal
Roteiro, com oito cenas e 78 segundos, em stories/o-ultimo-sinal-parte-1.md.
Manifesto em examples/ultimo-sinal-parte-1.json. Cinco cenários vetoriais
originais com oclusão de primeiro plano, luz ambiental e o Lúmino canônico.
O PR renderiza uma prévia silenciosa de 12 segundos do piloto, não um Reel final.
Gerar com npm run pilot-preview. A produção integral depende da voz Rasalgethi
obtida no site Google AI Studio, ajustes de sincronismo e revisão visual.

### QC de oito cenas
O comando npm run pilot-qc gera montagem técnica de 24 segundos, com 3 segundos por cena.
A ação pull_request renderiza esse QC; o vídeo é silencioso e não está liberado para postagem.

### Render mestre 4K
A opção 4k do workflow executa pilot-master e renderiza o episódio do
manifesto (78s) em 2160x3840 a 60fps, **não** a demo de 12s.
Esse render é manual, pode consumir muitos minutos do runner hospedado e
permanece sem voz enquanto narration estiver null. Não é publicação.
