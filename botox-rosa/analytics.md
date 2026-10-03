# Google Analytics 4 — Fernanda Beltrão

Integração criada em 03/10/2026 na conta Google autorizada pelo responsável.

- Conta: Fernanda Beltrão (`410579340`).
- Propriedade: Site Fernanda Beltrão (`557225021`).
- Fluxo Web: Site Fernanda Beltrão (`16008784098`).
- ID de medição público: `G-FGM9MBKS4D`.
- Site: https://fernandabeltrao.com.br/botox-rosa/.
- Fuso: São Paulo; moeda: real brasileiro.
- Painel: https://analytics.google.com/analytics/web/#/a410579340p557225021/.

## Medição

`assets/analytics.js` carrega a tag uma única vez, somente no domínio de produção. A raiz redireciona sem repetir a tag. Prévia local não gera acessos no GA4.

O evento `whatsapp_click` identifica a intenção de contato. Foi marcado como evento principal, contado uma vez por sessão e sem valor monetário padrão. Os cliques individuais continuam disponíveis como eventos. Um clique não confirma mensagem enviada, avaliação ou agendamento.

Dimensões personalizadas de escopo Evento:

| Dimensão | Parâmetro | Uso |
| --- | --- | --- |
| Posição do botão WhatsApp | `cta_position` | Comparar os pontos de contato na LP |
| Intenção do contato | `contact_intent` | Distinguir `duvidas` e `horarios` |

O evento também inclui a etiqueta `campaign=botox_rosa_2026`. Não há evento duplicado por posição. O Clarity continua funcionando de forma independente.

## Campanhas e dados

Use UTMs com etiquetas de campanha, nunca nomes, telefones, e-mails ou informações de pacientes:

`https://fernandabeltrao.com.br/botox-rosa/?utm_source=instagram&utm_medium=organic_social&utm_campaign=botox_rosa_2026&utm_content=bio`

A integração envia uma URL canônica, permitindo apenas `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` e `utm_id`, com valores limitados a 80 caracteres e etiquetas simples. Outros parâmetros e fragmentos são omitidos. O referenciador enviado contém somente a origem. Eventos de contato não incluem telefone, mensagem preenchida ou URL de destino do WhatsApp. Google Signals e personalização de anúncios estão desativados no código.

Na medição otimizada, permanecem visualizações de página e rolagem. Cliques externos, pesquisa no site, formulários, vídeos e downloads foram desativados para evitar captura automática de URLs de contato ou eventos redundantes.

## Verificação

Os testes em `tests/analytics.test.cjs` verificam inicialização única, exclusão de domínios locais, UTMs, ausência de dados de contato, cliques e tolerância a falhas da biblioteca. O workflow executa os testes Node e Python antes de publicar.

No painel, use Tempo real para conferir visitas. Compare sessões com o evento principal por origem e campanha; use as dimensões personalizadas para entender quais botões geram intenção. Confirme mensagens recebidas e agendamentos com a equipe de atendimento. Relatórios e dimensões dependem do processamento do Google e podem aparecer depois da coleta em tempo real.
