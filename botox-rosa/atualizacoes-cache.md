# Atualização automática e cache

O workflow `.github/workflows/pages.yml` publica cada atualização do branch `main` pelo GitHub Actions. O build usa apenas a biblioteca padrão do Python e mantém o domínio personalizado e HTTPS. O diretório gerado `_site` não entra no Git. Os arquivos editáveis e a prévia local continuam com os nomes originais.

## Como funciona

1. O workflow executa os testes de versionamento e atualização.
2. `scripts/build_site.py` gera nomes com hash de conteúdo para CSS, JavaScript, imagens, logos e vídeos, e atualiza as referências no site. O hash de CSS também considera as URLs das imagens usadas nele.
3. HTMLs, banners sociais, dados estruturados, fundos de galeria e vídeos escolhidos pela hero apontam para os arquivos correspondentes.
4. O build publica `site-version.json` e identifica a versão no HTML com o SHA do commit.
5. Ao abrir a LP, restaurá-la pelo histórico ou voltar à aba, um verificador pequeno e embutido no HTML consulta a versão publicada sem reutilizar o cache do navegador. Se houver diferença, faz uma única navegação para atualizar a página, mantendo parâmetros de campanha e âncoras.

Arquivos que não mudaram conservam seus hashes, aproveitando o cache. Os endereços originais também são publicados para compatibilidade com links antigos. O conteúdo principal, as imagens e o layout funcionam sem JavaScript; nesse caso, a atualização de HTML segue as regras de cache normais do navegador.

O verificador tem timeout de cinco segundos. Falhas de rede, modo offline e respostas inválidas mantêm a página atual funcionando. Um diálogo de mídia aberto adia a navegação até fechar. O parâmetro `_site_v` limita o recarregamento a uma vez por versão, evitando ciclos se a CDN ainda responder com o HTML antigo. A URL canônica permanece limpa, sem parâmetros.

## Publicação e limites

Basta alterar o site e enviar ao `main`. Não é necessário trocar números de versão manualmente. As mudanças ficam disponíveis após o workflow de publicação concluir, não enquanto ainda estão apenas na máquina local.

O GitHub Pages administra seus próprios cabeçalhos de cache e a distribuição do conteúdo. A solução não promete atualização instantânea em todas as regiões. A primeira instalação do verificador também depende de o navegador receber o novo HTML; cópias antigas anteriores a esta implantação seguem o cache normal até serem revalidadas. Prévias já armazenadas por WhatsApp, Facebook e outros aplicativos seguem o cache desses serviços; os novos banners recebem novas URLs ao mudar.

Não foram adicionados meta tags que fingem substituir cabeçalhos HTTP, service workers ou redownload de todos os vídeos em cada visita. A verificação baixa somente um JSON pequeno.

## Comandos

Build local, usando o SHA completo de um commit:

```sh
rtk proxy python3 scripts/build_site.py --revision <SHA-completo>
```

Testes:

```sh
rtk proxy python3 -m unittest discover -s tests -p 'test_*.py'
rtk proxy node --test tests/site-update.test.cjs
```

Publicação manual, se necessário, pelo botão “Run workflow” de “Publish website” no GitHub Actions. O Pages deve estar configurado para **GitHub Actions**, em vez de publicação direta de uma pasta do branch.

## Verificações e referências

Os testes verificam mudanças de imagens e dependências de CSS, estabilidade dos arquivos sem alteração, metadados e mídia, exclusão de arquivos privados, proteção da pasta de origem e build reproduzível. O verificador cobre HTML antigo, parâmetros e âncoras, prevenção de ciclos, falhas de rede, desenvolvimento local, diálogos e retorno à aba/histórico.

No navegador, a versão gerada foi conferida em 320, 390 e 1440 px, com arquivos locais carregados, foto ampliada e vídeo da hero versionados. Uma visita simulando HTML antigo navegou para a versão atual uma única vez, preservando o parâmetro de campanha e a âncora.

- [GitHub: publicação por workflows personalizados](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
- [MDN: URLs versionadas e cache HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching).
- [MDN: `fetch` com `cache: no-store`](https://developer.mozilla.org/en-US/docs/Web/API/Request/cache).
