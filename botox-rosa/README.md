# Botox Rosa — Outubro 2026

Landing page da campanha da Dra. Fernanda Beltrão. HTML, CSS e JavaScript estáticos, compatíveis com a hospedagem atual do projeto. O `index.html` da raiz redireciona automaticamente para `botox-rosa/`, preservando parâmetros e âncoras quando o JavaScript está disponível. Há redirecionamento por HTML para navegadores sem JavaScript; o conteúdo original da clínica permanece no arquivo da raiz.

- Página: `botox-rosa/index.html`.
- Domínio de publicação: `https://fernandabeltrao.com.br/botox-rosa/`.
- WhatsApp: `5551986390931`, reutilizado da página principal. Todos os CTAs têm mensagem específica da campanha.
- Identidade da clínica: verde `#4A6F70`, dourado `#D7B36A`, logo e fotografias existentes. Rosa da campanha: `#A7496D`.
- Sem bibliotecas JavaScript adicionais. Google Fonts é o único recurso visual externo; há fontes de sistema como alternativa.
- Abertura com fundo verde, títulos grandes e foto e vídeo em proporções próximas: `assets/material/fotos/principal.png` em destaque à direita e os vídeos da campanha à esquerda. A oferta completa aparece em uma composição inspirada em convite, com cabeçalho rosa, ícone de camiseta, divisão pontilhada e faixa verde para destacar a camiseta de presente. As condições especiais recebem um marcador rosa. O texto é de 18 px no desktop e 17 px no celular, com introdução maior. No celular, a oferta e o convite para participar aparecem logo após o título e antes das fotos e dos vídeos. Transição direta para a campanha e profundidade suave ao rolar.
- O álbum reúne nove fotos e nove vídeos intercalados, em três páginas de seis registros. As capas preservam o quadro completo com fundo desfocado, e as legendas ficam abaixo das imagens. A foto principal permanece na abertura e compõe os banners de compartilhamento social.

## Compartilhamento de links

Os arquivos `index.html` da raiz e `botox-rosa/index.html` incluem metadados estáticos Open Graph e Twitter Cards, disponíveis também para leitores que não executam JavaScript. Ambos usam o domínio `fernandabeltrao.com.br` e o mesmo título da campanha. A raiz continua redirecionando para a LP.

- Open Graph: `assets/media/botox-rosa-social-2026-v2.jpg`, JPEG de 1200 × 630 px.
- X: `assets/media/botox-rosa-social-x-2026-v2.jpg`, JPEG de 1200 × 600 px.
- A versão v2 remove a fita rosa que separava o fundo verde da fotografia. Os metadados usam as novas URLs para evitar reaproveitar a imagem v1 em cache.
- Os banners usam a foto `assets/material/fotos/principal.png`, com o rosto inteiro e a identidade visual da campanha.
- Especificações, prompt de criação e orientações sobre publicação/cache em [compartilhamento-social.md](compartilhamento-social.md).

Em 01/10/2026, o domínio público retornou HTTP 200 por HTTPS. O GitHub Pages está configurado para `main` e `/`, com `fernandabeltrao.com.br` cadastrado e HTTPS obrigatório.
- As fotos abrem em um diálogo de ampliação; os vídeos abrem com áudio e controles nativos. O diálogo fecha pelo botão, por Escape ou pelo fundo e devolve o foco ao elemento de origem.
- A hero reproduz `assets/media/hero-mix.mp4`: um mix em loop de 35 segundos, com trechos de 5 segundos dos sete vídeos de `assets/material/videos`. Ordem: `botox_rosa`, `fernanda1`, `editado1`, `tiago1`, `vere2`, `vide_vere`, `video_vere3`. Cada trecho usa os segundos 2 a 7 do original; saída vertical 540 × 960, 30 fps, H.264 sem áudio. O botão “Assistir com áudio” acompanha a cena atual e abre seu vídeo original completo. A reprodução pausa fora da área visível, ao abrir o diálogo, ao esconder a aba ou quando o navegador indica preferência por movimento reduzido.
- Os vídeos completos carregam apenas quando escolhidos. Versões locais em H.264/AAC, com início rápido, em `assets/media`. Os vídeos originais estão em `assets/material/videos` e as fotos em `assets/material/fotos`; as versões dos vídeos para a LP ficam em `assets/media`.
- Menu móvel, FAQ nativo, animações de entrada e selo animado. O botão “Pausar movimento” foi removido. A preferência por movimento reduzido do navegador continua sendo respeitada, pausando os vídeos de fundo e as animações decorativas. O conteúdo permanece visível sem JavaScript.

## SEO local e GEO

Em 01/10/2026, títulos e descrição de busca foram atualizados para Botox Rosa, botox no Menino Deus e harmonização facial em Porto Alegre. A apresentação da profissional e o FAQ identificam a clínica, o bairro, a cidade, o endereço e o contato. O título da hero, a oferta e a descrição de compartilhamento aprovada foram preservados.

O HTML contém dados estruturados de site, página, campanha, clínica (`Dentist`), profissional e serviços. A raiz mantém o redirecionamento e a mesma URL canônica. `robots.txt` permite rastreamento e informa o `sitemap.xml`, que contém apenas a URL canônica da LP. Análise, validação e próximos passos externos em [seo-geo.md](seo-geo.md).

O script assíncrono do Microsoft Clarity, projeto `yqwnjvqus9`, está no cabeçalho da LP. A página de redirecionamento da raiz não repete a integração.

## Conteúdo da campanha

A oferta de camiseta para pacientes que realizarem botox durante outubro foi informada pela solicitante. O texto menciona apoio à causa do IMAMA sem afirmar uma parceria institucional formal ou repasse financeiro específico.

A clínica confirmou para outubro de 2026: botox ou procedimento de harmonização facial, camiseta oficial do IMAMA 2026 de presente e condições especiais durante todo o mês. Valores, procedimentos e condições detalhadas devem ser consultados com a equipe. As legendas de 2025 documentam a camiseta como símbolo de apoio; os registros de 2025 continuam identificados como edição anterior.

A forma de contribuição financeira ao instituto ainda não foi informada. Não foram inventados percentuais, valores por procedimento, números de pacientes ou percentuais de desconto de 2026. Se a clínica confirmar compra de camisetas ou doação, atualizar o FAQ com a mecânica real.

A linguagem foi alinhada aos textos de 2025: beleza com propósito, autocuidado, solidariedade e gratidão. Análise e referências em [analise-textos-instagram.md](analise-textos-instagram.md).

## Fontes consultadas em 30/09/2026

- IMAMA: https://imama.org.br/ — nome oficial, natureza sem fins lucrativos e atividades de apoio às pacientes.
- Logo oficial: https://imama.org.br/wp-content/uploads/2020/03/imama-1-1-600x216.png — arquivo local `assets/imama-logo.png`, com proporções e cores preservadas.
- Foto de abertura: material disponibilizado no projeto, `assets/material/fotos/principal.png`. O registro anterior `assets/material/fotos/WhatsApp Image 2026-09-30 at 14.52.45.jpeg` é utilizado na seção da profissional. A abertura mostra a Dra. Fernanda vestida de rosa com a mensagem do IMAMA. Os registros de 2025 mantêm a identificação de edição anterior. Os arquivos originais da pasta `material` foram preservados.
- INCA, versão para população: https://www.gov.br/inca/pt-br/assuntos/cancer/tipos/mama/versao-para-populacao — sinais de atenção, detecção precoce e hábitos que reduzem o risco. A página não prescreve calendário individual de exames.
- Referência visual: https://marcwilmes.com/portfolio/creos-octobre-rose/ — campanha de conscientização com rosa como destaque e mensagem de cuidado.
- Referência de comunicação: https://www.pinkstondigital.com/work/courage-to-live/ — participação e acolhimento em uma campanha de conscientização. Nenhuma fotografia, depoimento ou texto desses projetos foi reproduzido.

## Verificação local

Layout conferido em 320, 390, 768, 1024 e 1440 px, sem rolagem horizontal. CTAs, âncoras, carregamento das imagens, menu móvel (incluindo Escape), FAQ e movimento reduzido verificados no Chromium. Não há compilação ou instalação de dependências para publicar esta página.

A revisão com mídia também foi verificada nessas cinco larguras: reprodução da montagem sem áudio, vídeos sob demanda com controles, abertura e fechamento do diálogo, ampliação de fotos, pausa do movimento e ausência de erros de JavaScript.

## Refatoração das seções após a hero

`assets/sections.css` organiza os novos estilos sem alterar a abertura ou a navegação. Origem da campanha em uma composição editorial com duas fotos reais, apresentação do IMAMA, painel da profissional com foto real, FAQ em acordeão e chamada final com botão do WhatsApp. O rodapé utiliza a logo1 branca e termina com o crédito “Desenvolvido por”, a logo original do Glauber e o link para seu site.

A refatoração foi conferida em 320, 390, 768, 1024 e 1440 px, sem rolagem horizontal. ampliação de fotos, reprodução de vídeo com controles, fechamento do diálogo e retorno do foco e abertura/fechamento do FAQ funcionaram. Imagens carregadas e nenhuma mensagem de erro de JavaScript no navegador. A abertura foi posteriormente atualizada para dar destaque à foto principal disponibilizada em `assets/material/fotos/principal.png`.

## Galeria restaurada

A seção “Histórias que vestem a causa” fica entre o IMAMA e a apresentação da profissional, com navegação por três páginas de seis registros, sem arquivos repetidos. As fotos abrem ampliadas e os vídeos abrem com áudio e controles. Os links de acesso e a numeração das seções foram restaurados. O destaque rosa na abertura, o link “Conheça a clínica” para o Instagram e a remoção da pergunta sobre botox e prevenção no FAQ foram mantidos.

## Origem e propósito

A segunda dobra explica a motivação do Botox Rosa: apoiar simbolicamente o trabalho do IMAMA e unir autocuidado, solidariedade e conscientização no Outubro Rosa. A composição traz o texto à esquerda e as fotos locais `foto_vere.jpeg` e `foto_tiago.jpeg` em duas molduras à direita, com os três conceitos acima. As imagens aparecem inteiras, sem legendas nas molduras, com ampliação ao clicar. No celular, texto e composição seguem em uma coluna, mantendo as duas fotos lado a lado. A oferta permanece na hero, no FAQ e no convite final.

O título da origem é “O presente é seu. A causa é de todos.”, evitando repetir o título da hero “Seu cuidado. Nossa causa. Outubro rosa.”. A oferta preserva integralmente o texto informado, com contraste mínimo medido de 5,35:1 entre os diferentes fundos e textos da composição e sem rolagem horizontal nas larguras 320, 390, 430, 760, 768, 960, 1024 e 1440 px.

A dobra de origem inclui a logo local do IMAMA, seu site e os perfis de Instagram, Facebook, YouTube e LinkedIn, conferidos nos links do próprio site `https://imama.org.br/` em 30/09/2026. Os links abrem em nova aba e a logo branca aparece sobre fundo verde para preservar o contraste.

O bloco do instituto ganhou um painel verde com logo maior, botão próprio para o site e ícones SVG de Instagram, Facebook, YouTube e LinkedIn. Cada ícone mantém um nome visível e um rótulo acessível. O convite para participar fica junto ao texto de origem. A composição das fotos não tem legendas nem frase abaixo.

## Remoção da seção de cuidados

A dobra “Um lembrete de mulher para mulher” foi removida, junto com a entrada “Seu cuidado” no menu. A entrada correspondente no menu e a numeração das seções foram atualizadas.

## Ordem das seções

A seção do instituto foi renomeada para “IMAMA: acolhimento e apoio” e fica imediatamente após “A origem do Botox Rosa”. Depois vêm a galeria, a apresentação da profissional e o FAQ. O menu e a numeração acompanham essa ordem.

A dobra do IMAMA usa fundo verde sálvia suave, títulos em verde e rosa e detalhes florais discretos. O texto “Juntas, a vida ganha mais força” apresenta a rede de acolhimento que inspira a campanha. A arte local `assets/material/fotos/imama.jpeg` aparece inteira e pode ser ampliada; sua legenda destaca a abertura oficial do Outubro Rosa do IMAMA em 2 de outubro de 2026, às 19h, no GNC Cinemas do Shopping Praia de Belas. Data e local foram transcritos da arte fornecida. No celular, texto e convite seguem em uma coluna. O card “2025 → 2026 · Uma história que continua” permanece removido.
