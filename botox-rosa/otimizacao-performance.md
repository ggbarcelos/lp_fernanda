# Otimização de imagens e vídeos

## Revisão de Core Web Vitals · 02/10/2026

O diagnóstico informado tinha LCP de 4,7 s e INP de 290 ms, com apenas cinco visualizações. Foram aplicadas estas melhorias:

- DM Sans e Playfair Display locais, em três arquivos WOFF2 variáveis, com preload e `font-display: swap`; o CSS externo do Google Fonts deixou de bloquear a renderização.
- Texto, oferta e fotografia da hero visíveis desde a primeira pintura, sem animação de entrada com opacidade zero.
- Clarity remoto e reprodução ambiente agendados depois de `load`, em um intervalo ocioso. A função de fila do Clarity continua disponível imediatamente para os eventos de campanha.
- Rolagem com um único `requestAnimationFrame`, lendo a geometria antes de alterar o cabeçalho; parallax não é calculado no celular.
- Gradientes sem grandes camadas de blur animadas e cabeçalho sem backdrop-filter no celular. O diálogo usa sobreposição escura sem blur de tela inteira.
- Foto `assets/2026/fotos/img01.png` com versões responsivas WebP. A versão de 640 px ocupa 94.454 bytes, contra 1.800.435 bytes do original (94,8% menos). O original permanece no diálogo de ampliação. O build verifica o checksum antes de usar derivados.

Medição local comparativa em Chromium, cache frio, densidade 1×, latência de 150 ms, download de 200.000 bytes/s e CPU reduzida 4×:

| Indicador | Antes | Depois |
| --- | --- | --- |
| LCP em 390 px | 3,37 s | 2,04 s |
| LCP em 1440 px | 3,59 s | 2,36 s |
| CLS em 390 px | 0,060 | 0 |
| Foto original de 2026 na abertura | 1,8 MB | Não solicitada |

Os valores são uma execução comparativa de laboratório, não a pontuação do Clarity nem o INP de usuários reais. A nota deve ser medida novamente após publicação e novas visitas. As interações de menu, ampliação e FAQ no celular ficaram entre 32 e 48 ms na execução final, contra 40 a 96 ms na execução inicial; isso não representa o INP de campo. No desktop, as interações ficaram entre 112 e 200 ms, contra 152 a 256 ms inicialmente.

Para novas fotos de 2026: `python3 scripts/optimize_images.py --campaign-only`, com Pillow/WebP. O build do GitHub Actions continua usando apenas a biblioteca padrão do Python. Sem derivados válidos, usa a fotografia original atual.

Referências: [otimização de LCP](https://web.dev/articles/optimize-lcp) e [otimização de INP](https://web.dev/articles/optimize-inp).

Revisão de 01/10/2026. O layout, os textos aprovados, o Clarity e a configuração de atualização automática foram preservados.

## Resultados

| Recurso | Antes | Depois | Redução |
| --- | --- | --- | --- |
| Foto principal exibida no mobile de teste | 1.642 MiB | 0.077 MiB, versão de 640 px | 95,3% |
| Foto principal exibida no desktop de teste | 1.642 MiB | 0.131 MiB, versão de 960 px | 92,0% |
| Montagem da hero | 5.95 MiB | 3.92 MiB | 34,1% |
| Conjunto de 11 vídeos utilizados na LP | 42.42 MiB | 34.03 MiB | 19,8% |
| HTML de redirecionamento da raiz | 34.936 bytes | 3.053 bytes | 91,3% |

Na medição local com cache frio, largura de 390 px e densidade 2×, o volume registrado dos recursos próprios na abertura caiu de 3.473.000 para 289.462 bytes (91,7%), com seis imagens solicitadas em vez de 23. Em 1440 px e densidade 2×, caiu de 6.965.654 para 2.976.438 bytes (57,3%), com oito imagens em vez de 24.

Esses registros cobrem o carregamento até quatro segundos depois do evento `load`, incluindo o trecho já transferido do vídeo da hero quando visível. Excluem fontes externas e Clarity. São medições comparáveis no servidor local, não uma promessa de tempo de carregamento em todas as conexões nem uma pontuação Lighthouse.

## Imagens

- Versões WebP proporcionais em 360, 640, 960 px e no tamanho original, sem ampliar a resolução da fonte. O navegador seleciona a versão por `srcset` e `sizes`.
- Qualidade WebP 94 para a exibição da foto principal e 90 para as demais versões. Quando uma versão completa fica maior que o JPEG original, o JPEG continua como candidato nessa resolução.
- Ampliação principal em WebP sem perdas, com os mesmos pixels do PNG original; as outras fotografias abrem seus originais. Nenhuma foto fornecida foi sobrescrita.
- Logos sem perdas, com transparência; perfis de cor disponíveis foram preservados. Decodificação assíncrona e carregamento adiado para imagens fora da abertura.
- Fundos desfocados da galeria reutilizam o `currentSrc` da imagem carregada. Os fundos inline que antecipavam downloads de todo o álbum foram removidos.
- Banners sociais continuam em JPEG nas dimensões já aprovadas, para manter a compatibilidade dos leitores de compartilhamento.

## Vídeos

As cópias em `assets/optimized/videos` usam MP4/H.264, mantêm a resolução exibida, a proporção, o número de quadros e a duração dos originais. O áudio AAC foi copiado, sem nova compressão. `faststart` coloca as informações necessárias à reprodução no começo do arquivo.

O script tenta CRF 25 e, quando necessário, CRF 24, com preset `veryslow`. Só aceita recompressão se o arquivo ficar menor e a média VMAF amostrada atingir pelo menos 95. A comparação considera um quadro a cada cinco. O menor resultado aceito foi 95,01; a montagem da hero ficou em 96,00. Quando a recompressão aumenta o arquivo ou não atende ao critério, os fluxos originais são mantidos. O remux pode acrescentar uma pequena diferença de tamanho no contêiner.

Essa compressão é perceptual, não matematicamente sem perdas. A conferência visual preservou rostos, textos e enquadramentos; os arquivos originais continuam disponíveis no projeto. A montagem mantém 35 segundos, com as mesmas sete cenas de cinco segundos e `botox_rosa` primeiro.

A montagem aguarda o carregamento da foto principal antes de reproduzir. Os outros vídeos continuam sob demanda. O modo de economia de dados do navegador evita reprodução automática; o visitante pode assistir com áudio pelo botão existente.

## Entrada e publicação

A raiz foi reduzida a redirecionamento, metadados sociais e link de acesso. Não carrega mais Bootstrap, fontes e arquivos da página antiga da clínica. A versão anterior continua no histórico Git. A LP deixou de solicitar a família Manrope, que não era utilizada.

O build também versiona os candidatos de `srcset`. Imagens e vídeos novos recebem seus hashes na publicação, preservando o mecanismo de atualização de cache.

## Regeneração

Os derivados foram gerados antes da publicação e estão no repositório. Não são recomprimidos a cada visita ou publicação. Ao substituir um original, regenerar suas versões e conferir as referências da LP.

```sh
rtk proxy python3 scripts/optimize_images.py
rtk proxy python3 scripts/optimize_videos.py
```

Esses comandos requerem Pillow com WebP e FFmpeg com `libx264` e `libvmaf`. Os catálogos `scripts/image-variants.json` e `scripts/video-optimization.json` registram fontes, tamanhos e resultados. O build habitual do GitHub Actions continua sem essas dependências de conversão.

## Validação

- Layout em 320, 390, 768, 1024 e 1440 px, sem rolagem horizontal.
- Todas as 18 imagens/capas da galeria e os nove vídeos da seção abrem corretamente, com controles e enquadramento preservados.
- As 11 cópias de vídeo preservam dimensões exibidas, número de quadros e duração. Os hashes dos dados de áudio coincidem com os originais.
- Comparação de pixels confirma que a ampliação principal sem perdas é idêntica ao PNG de origem.
- Autoplay após a foto, redução de movimento, economia de dados, seleção da cena da hero e redirecionamento com parâmetros/âncoras verificados no navegador.
- Teste do build confirma que `srcset` mantém os descritores e usa os endereços com hash corretos.

Referências: [imagens responsivas, MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images), [carregamento adiado de vídeos, web.dev](https://web.dev/articles/lazy-loading-video) e [qualidade e compressão de codecs, MDN](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Video_codecs).
