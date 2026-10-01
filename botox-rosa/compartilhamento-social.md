# Prévia de compartilhamento — Botox Rosa 2026

## Arquivos finais

| Uso | Arquivo | Dimensões |
| --- | --- | --- |
| Open Graph, para leitores como Facebook, WhatsApp e LinkedIn | `assets/media/botox-rosa-social-2026-v2.jpg` | 1200 × 630 px |
| Twitter Cards / X, com `summary_large_image` | `assets/media/botox-rosa-social-x-2026-v2.jpg` | 1200 × 600 px |

Ambos são JPEG opaco, comprimidos para compartilhamento, abaixo de 300 KB. A margem da composição preserva o rosto e os textos no corte mais horizontal da versão para X. A foto original não foi modificada. A versão v2 remove a fita rosa e seu contorno dourado entre o fundo verde e a fotografia, mantendo a linha dourada horizontal sob a data. Os HTMLs usam novas URLs de imagem; as exportações v1 foram preservadas.

As tags `og:title`, `og:description`, `og:type`, `og:locale`, `og:site_name`, `og:url`, `og:image`, `og:image:secure_url`, `og:image:type`, `og:image:width`, `og:image:height` e `og:image:alt` estão nos dois HTMLs. Twitter Cards tem título, descrição, imagem e texto alternativo próprios. Os endereços de imagens e canonical são absolutos, em HTTPS, no domínio `fernandabeltrao.com.br`.

As tags ficam no HTML inicial para os leitores obterem a prévia sem executar JavaScript. Isso também cobre o compartilhamento da raiz, que redireciona navegadores para `/botox-rosa/`. Não há dependência de JavaScript para selecionar o banner.

As descrições Open Graph e Twitter Cards usam exatamente o texto informado: “Ao fazer seu botox ou um procedimento de harmonização facial, você ganha a camiseta oficial do IMAMA 2026 e aproveita condições especiais”. A descrição padrão para mecanismos de busca foi otimizada em 01/10/2026 para identificar os serviços, Menino Deus e Porto Alegre; isso não altera a descrição de compartilhamento aprovada.

## Publicação e cache

Desde 01/10/2026, o workflow de publicação versiona os banners automaticamente pelo conteúdo e atualiza as URLs nos dois HTMLs. A tabela acima identifica os arquivos de origem; os arquivos publicados recebem um hash antes da extensão. Alterar o banner e enviar ao `main` já gera uma nova URL na publicação, sem atualizar manualmente a versão do nome. O cache de uma prévia que já foi armazenada pelo aplicativo social continua sob controle desse aplicativo.

1. Enviar os HTMLs e os JPEGs alterados ao branch `main`; o workflow prepara e publica os arquivos no GitHub Pages.
2. Aguardar a conclusão do workflow. DNS e HTTPS do domínio já estão funcionando.
3. Conferir se a página e os JPEGs retornam HTTP 200 no domínio público.
4. Para atualizar uma prévia antiga, usar o [Sharing Debugger do Facebook](https://developers.facebook.com/tools/debug/) e o [Post Inspector do LinkedIn](https://www.linkedin.com/post-inspector/). A prévia no WhatsApp pode depender do cache do aplicativo; mensagens já enviadas não são uma validação da versão nova.
5. Em alterações futuras do banner, editar os arquivos de origem e publicar. O build atualiza automaticamente os endereços dos banners alterados.

O banner é uma prévia de **link**. Publicações de imagem em feed, Stories ou Status são outros formatos e não são configuradas pelos metadados da página. Cada aplicativo decide como apresentar o link; o arquivo fornecido não garante que todas as telas mostrem uma imagem grande.

## Referências consultadas em 30/09/2026

- [LinkedIn: Make your website shareable](https://www.linkedin.com/help/linkedin/answer/a521928): Open Graph, imagem com pelo menos 1200 × 627 px, proporção recomendada de 1,91:1 e até 5 MB. O arquivo de 1200 × 630 atende às dimensões mínimas e aproxima essa proporção.
- [Meta: Images in Link Shares](https://developers.facebook.com/docs/sharing/webmasters/images/): a página retornou limite de requisições durante esta verificação. A exportação Open Graph usa o formato horizontal de 1200 × 630 px.
- A antiga documentação do X para `summary_large_image` redireciona para [o portal atual](https://docs.x.com/overview), sem especificação de Cards no conteúdo retornado. A exportação dedicada usa 2:1; não é apresentada aqui como uma especificação recém-publicada do X.

## Edição atual (v2, sem fita rosa)

Modo: ferramenta integrada `image_gen`, usando o banner v1 como alvo de edição. Exportação técnica com `sips` para as mesmas dimensões finais. A fita separadora foi removida nas versões Open Graph e X; textos e enquadramento foram conferidos visualmente.

Prompt final da edição:

```text
Use case: precise-object-edit.
Input image 1 is the edit target: the existing Botox Rosa social banner.
Make one targeted change: completely remove the decorative curved pink ribbon that separates the teal green text panel from Fernanda's photograph, including the thin gold contour following that ribbon. Fill its former area by naturally extending the existing teal panel and the original photographic background, producing a clean border between the green area and photograph with no ribbon or decorative separator. Keep the existing overall curved silhouette if helpful, but no pink strip, gold border, shadow or replacement ornament.
Preserve everything else exactly: Fernanda's face, identity, age, expression, hairstyle, earrings, pose, pink outfit, shirt lettering, background, crop, position and proportions; green color and texture; every text's wording, position, font, size and color. Retain the small horizontal gold line below OUTUBRO 2026.
Text unchanged, verbatim:
BOTOX ROSA
OUTUBRO 2026
Cuidado com
propósito
Dra. Fernanda Beltrão
CRO-RS: 12341
fernandabeltrao.com.br
Do not redesign, retype, add, or remove anything else. Preserve the entire head with the existing margin above it. Same landscape aspect ratio as input; target 1200 x 630 pixels. Opaque background.
```

## Criação da arte original

Modo: ferramenta integrada `image_gen`, skill imagegen; referência local inspecionada antes da geração. Exportação técnica para JPEG e dimensões finais com `sips`. A composição foi conferida visualmente nas duas versões, com texto correto, enquadramento do rosto e identificação CRO-RS.

Fonte: `assets/material/fotos/principal.png`.

Prompt de criação original (v1):

```text
Use case: identity-preserve / ads-marketing.
Asset type: social link preview banner for the Botox Rosa 2026 landing page.
Input image 1 is the EDIT TARGET: the actual principal.png portrait of Dra. Fernanda Beltrão. Use that photograph, keeping her face, identity, age, expression, earrings, skin texture, pose, pink outfit and the readable IMAMA shirt print unchanged. Do not invent a different woman or retouch her face.
Create ONE finished landscape banner at exactly 1200 x 630 pixels (1.905:1).
Composition: refined editorial campaign layout, left 56% clean deep teal #4A6F70, right 44% the real portrait gently cropped from above the head to the waist. Keep her entire head comfortably inside the frame with breathing room above, her pink IMAMA dress and some natural original environment visible. Soft curved pink ribbon connecting the teal background and photo, tiny tasteful gold hairline detail #D7B36A. Cream lettering, pink campaign accents. Match a sophisticated warm clinic website, inspiring and human.
Text, verbatim, large and legible in this hierarchy, left aligned, with at least 60px outer margins:
"BOTOX ROSA" — very prominent large pink campaign title
"OUTUBRO 2026" — small uppercase tracked line
"Cuidado com" on one line and "propósito" on next line — elegant large cream editorial serif
"Dra. Fernanda Beltrão" — small neat sans serif
"CRO-RS: 12341" — tiny neat sans serif immediately below the name
"fernandabeltrao.com.br" — discreet cream footer at lower left
Do not add any other copy, invented logos, extra people, medical objects, or CTA buttons. Keep the essential headline and face clear in a small shared-link preview. All decorative effects must stay away from the face. The existing photograph is essential, preserve its person's likeness exactly. Opaque background.
```
