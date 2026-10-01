# SEO local e GEO — Botox Rosa

Revisão de 01/10/2026. URL canônica: https://fernandabeltrao.com.br/botox-rosa/.

## Análise e alterações

| Aspecto | Antes | Implementação |
| --- | --- | --- |
| Título e descrição de busca | Identificação geral da campanha | Serviços e localização explícitos: Menino Deus, Porto Alegre |
| Conteúdo local | Endereço concentrado no FAQ e no rodapé | Localização na hero, apresentação da clínica e respostas do FAQ |
| Identificação da clínica | Texto visível | Texto visível e dados estruturados de clínica, profissional e serviços |
| Rastreamento | Sem sitemap ou robots na raiz | `robots.txt` e sitemap com uma URL canônica |
| Respostas sobre a campanha | Mecânica de participação | Explicação direta de quem organiza, onde atende e quando ocorre |

A implementação distribui os termos em conteúdo útil e legível. Não acrescenta listas ocultas de palavras-chave nem repetições artificiais. Essa abordagem segue as orientações do Google para [títulos](https://developers.google.com/search/docs/appearance/title-link?hl=pt-br), [descrições](https://developers.google.com/search/docs/appearance/snippet?hl=pt-br) e [políticas contra spam](https://developers.google.com/search/docs/essentials/spam-policies?hl=pt-br).

## Termos e intenção de busca

| Termos | Onde aparecem |
| --- | --- |
| Botox Rosa, Botox Rosa 2026 | Metadados, campanha, oferta e FAQ |
| Botox em Porto Alegre, botox no Menino Deus | Título de busca, descrição, apresentação da clínica e FAQ |
| Harmonização facial em Porto Alegre e no Menino Deus | Descrição, apresentação da clínica, oferta e dados dos serviços |
| Dra. Fernanda Beltrão, FB Harmonização & Odontologia | Metadados, apresentação, contato e dados estruturados |

A grafia usada é **harmonização facial**. Os termos entram em frases naturais, como “Botox e harmonização facial no Menino Deus”.

Título de busca:

> Botox Rosa em Porto Alegre | Botox no Menino Deus

Descrição de busca:

> Botox Rosa 2026: botox e harmonização facial no Menino Deus, Porto Alegre, com a Dra. Fernanda Beltrão. Camiseta IMAMA e condições especiais em outubro.

O título visível da hero, o título da origem da campanha e a oferta foram mantidos. Open Graph e Twitter Cards preservam a descrição de compartilhamento aprovada pelo usuário.

## Informações para buscas e respostas com IA

O conteúdo responde diretamente o que é o Botox Rosa, quem realiza o atendimento, em qual bairro e cidade fica a clínica e como participar. As informações principais estão no HTML inicial, disponíveis sem JavaScript. Endereço, telefone, CRO-RS e identidade da profissional são consistentes entre conteúdo e dados estruturados.

O Google informa que os fundamentos de SEO também se aplicam aos seus recursos de IA, sem arquivo ou marcação especial adicional. Por isso, o trabalho de GEO prioriza conteúdo claro, rastreável e factual, seguindo a [documentação sobre recursos de IA](https://developers.google.com/search/docs/appearance/ai-features?hl=pt-br).

Os links de IMAMA e INCA já presentes na página permanecem como referências institucionais. A campanha é descrita como apoio simbólico à causa; não foram acrescentadas alegações de parceria formal, repasse financeiro, resultados clínicos ou avaliações de pacientes.

## Configuração técnica

- URL canônica única nos dois HTMLs; a raiz continua redirecionando para a LP.
- JSON-LD com `WebSite`, `WebPage`, campanha, `Dentist`, `Person` e dois `Service`, com identificadores conectados.
- Nome, endereço, telefone, imagem e perfil social da clínica nos dados estruturados, seguindo a [documentação de empresas locais](https://developers.google.com/search/docs/appearance/structured-data/local-business?hl=pt-br).
- `robots.txt` permite rastreamento e aponta para `https://fernandabeltrao.com.br/sitemap.xml`.
- Sitemap com a URL canônica e data de alteração real, conforme a [documentação de sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=pt-br).
- Diretivas de prévia autorizam snippets e imagens grandes; não determinam como o buscador exibirá o resultado.
- Microsoft Clarity assíncrono, projeto `yqwnjvqus9`, incluído apenas na LP.

## Validação

O domínio retornou HTTP 200 por HTTPS em 01/10/2026 e o GitHub Pages informou HTTPS obrigatório. Localmente, foram conferidos JSON-LD válido e referências internas, título, descrição, canonical, sitemap, robots e preservação dos metadados sociais. O conteúdo local e o FAQ funcionam sem JavaScript.

Layout conferido em 320, 390, 768, 1024 e 1440 px, sem rolagem horizontal. As cinco perguntas do FAQ funcionam e o navegador não apresentou erros de JavaScript na verificação do conteúdo. Não foi realizado teste de resultados avançados do Google nem confirmada indexação nos buscadores.

O teste local do Clarity confirmou uma única solicitação ao projeto correto, script assíncrono e função inicial disponível, simulando a resposta externa. O recebimento de eventos no painel do Clarity não foi verificado.

## Próximos passos no Google

1. Verificar a propriedade do domínio no Google Search Console, usando o registro TXT fornecido pela própria conta.
2. Enviar `https://fernandabeltrao.com.br/sitemap.xml` e inspecionar a URL da LP para solicitar indexação.
3. Conferir no Perfil da Empresa no Google o nome, endereço, telefone e link do site, mantendo os mesmos dados da página.

Essas etapas dependem das contas da clínica. A otimização implementada não garante posição de busca ou presença em respostas com IA.
