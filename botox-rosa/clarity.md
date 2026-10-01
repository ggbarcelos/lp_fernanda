# Clarity — Botox Rosa

O projeto `yqwnjvqus9` continua usando o snippet oficial no cabeçalho. `assets/clarity-tracking.js` executa antes de `campaign.js` e usa a fila do snippet mesmo enquanto a biblioteca remota carrega. Não precisa de outra chave ou biblioteca. Não altera as preferências de consentimento do Clarity.

## Identificação

`identify` recebe um UUID aleatório em `custom-id` e `botox_rosa_2026` em `custom-page-id`; o identificador de sessão é administrado pelo próprio Clarity. O UUID é guardado na chave `botox_rosa_clarity_visitor` do `localStorage` e reaproveitado no mesmo navegador. Apagar o armazenamento gera outro ID. Se o armazenamento estiver bloqueado, o ID vale somente para a página atual; sem geração aleatória segura, `identify` é omitido. Nomes, telefones, informações de saúde e nomes amigáveis não são usados nos identificadores ou eventos.

## Tags

- `campanha`: `botox_rosa_2026`.
- `pagina`: `botox_rosa`.
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`: etiquetas da URL atual, até 80 caracteres, aceitando letras ASCII, números, espaços, ponto, hífen e sublinhado; espaços viram sublinhados e letras ficam minúsculas. Outros parâmetros, a URL completa e a mensagem do WhatsApp não são enviados pela integração.
- `whatsapp_cta`: posição do botão clicado.
- `video` e `video_local`: conteúdo reproduzido e posição (`hero`, `galeria` ou `profissional`).

Use etiquetas de campanha nas UTMs, sem dados pessoais. Exemplo para o Reels de lançamento:

`https://fernandabeltrao.com.br/botox-rosa/?utm_source=instagram&utm_medium=organic_social&utm_campaign=botox_rosa_2026&utm_content=reels_lancamento`

Para comparar outras peças, use `stories_lancamento`, `bio` etc. em `utm_content`. Sem UTMs, essa integração não atribui uma origem personalizada; os dados nativos do Clarity continuam disponíveis. O redirecionamento da raiz preserva esses parâmetros quando JavaScript está ativo.

## Eventos

| Evento | Disparo |
| --- | --- |
| `section_view_origem` | Título da segunda dobra pelo menos 50% visível por 1 segundo contínuo, com a aba ativa |
| `section_view_imama`, `section_view_galeria`, `section_view_profissional`, `section_view_duvidas`, `section_view_convite_final` | Mesmo critério para o título de cada seção |
| `whatsapp_click` | Clique em qualquer CTA do WhatsApp |
| `whatsapp_click_<posição>` | Clique no botão específico: `cabecalho`, `menu_mobile`, `hero`, `origem`, `galeria`, `duvidas`, `convite_final` ou `flutuante` |
| `video_play` e `video_play_<conteúdo>` | Reprodução efetiva de um vídeo aberto no diálogo, no evento nativo `playing` |
| `video_complete` e `video_complete_<conteúdo>` | Fim do vídeo, no evento nativo `ended` |

Conteúdos: `convite`, `proposito`, `historia`, `encontro`, `cuidado`, `camiseta`, `gesto`, `bastidores`, `conexoes` e `tecnica`. Os IDs da hero acompanham a cena selecionada e permanecem estáveis após o build que versiona os arquivos.

Cada seção dispara uma vez por carregamento. Passagens rápidas pela seção e tempo com a aba oculta não contam. A métrica mede chegada ao título, sem afirmar leitura de todo o texto. Cada vídeo dispara início e conclusão uma vez por abertura: pausar e retomar não duplica; reabrir permite registrar uma nova reprodução. Os loops automáticos de fundo não contam. Os eventos gerais e específicos representam a mesma ação e não devem ser somados. Um clique no WhatsApp indica intenção de contato, não mensagem enviada ou agendamento confirmado.

Falhas no Clarity ou no armazenamento não impedem navegação, reprodução ou cliques. O gancho existente do Google Analytics permanece independente. Sem `IntersectionObserver`, apenas os eventos de seção ficam indisponíveis.

## Validação

Execute `node --test tests/*.test.cjs` e `python3 -m unittest discover -s tests -p 'test_*.py'`. O workflow de publicação executa ambas as suítes.

Após publicar, abra o link com UTMs, mantenha a segunda dobra visível por pelo menos 1 segundo, reproduza um vídeo e clique em um CTA. No projeto do Clarity, confira as tags em filtros e os eventos em Smart events/gravações. O recebimento no painel depende da publicação, da biblioteca remota e das configurações de coleta do projeto.

Referências: [API do Clarity](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-api) e [Identify API](https://learn.microsoft.com/en-us/clarity/setup-and-installation/identify-api).
