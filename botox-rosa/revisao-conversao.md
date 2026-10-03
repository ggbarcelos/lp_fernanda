# Revisão da campanha Botox Rosa 2026

Branch: `codex/melhorias-conversao-fernanda`. Preparada para revisão, sem publicação em produção.

## Conteúdo e composição

A abertura identifica Botox Rosa 2026, traz “Seu cuidado. Nossa causa.”, explica a camiseta para mulheres e homens que realizarem botox durante outubro, informa profissional, CRO e localização e apresenta “Quero saber mais pelo WhatsApp”. Fotos, vídeos, cores e tipografia foram preservados. A apresentação profissional continua logo após a abertura, antes dos álbuns; o FAQ foi reduzido a sete perguntas práticas. O espaçamento solicitado acima do convite final foi mantido.

O README histórico registra anteriormente camiseta para harmonização facial e condições especiais. Para esta revisão, o briefing mais recente foi adotado como escopo editorial: a comunicação do benefício, inclusive nos metadados e dados estruturados, menciona somente botox. Os serviços da profissional continuam identificados em sua apresentação. Qualquer ampliação da oferta deve receber confirmação atual da responsável antes de retornar ao texto.

## WhatsApp e medição

Todos os 11 pontos de contato usam `https://wa.me/5551986390931` com mensagem codificada. A abertura utiliza exatamente a mensagem solicitada no briefing. Seções informativas convidam a tirar dúvidas e os pontos de agendamento convidam a consultar horários.

No celular, o WhatsApp permanece acessível com texto no cabeçalho fixo, evitando uma barra inferior sobre o conteúdo. No desktop, o botão flutuante tem ícone e texto visíveis; fica oculto quando o rodapé, os controles das galerias ou o fecho da abertura aparecem, e durante o diálogo de mídia.

Os atributos `data-whatsapp` e `data-track-cta`, o evento `whatsapp_click` e os eventos por posição foram preservados. A integração do Clarity continua independente do gancho opcional do GA. O GA agora usa somente a posição validada do botão e tolera falhas síncronas e assíncronas. Eventos por intenção são filtros do mesmo clique e não devem ser somados ao total. Clique não comprova mensagem recebida nem avaliação agendada. Não são enviados textos de mensagens, telefones ou dados de saúde nas propriedades personalizadas.

## Pendências da responsável

- Confirmar valor e condições da avaliação, incluindo se há cobrança. Nenhuma gratuidade foi anunciada.
- Informar dias e horários reais de atendimento. A página direciona a consulta para a equipe.
- Confirmar detalhes operacionais da entrega da camiseta: disponibilidade, tamanhos e eventuais critérios. Nenhuma quantidade, tamanho ou estoque foi anunciado.
- Confirmar se deseja estender a camiseta a outros procedimentos e quais condições comerciais podem ser divulgadas. Nesta revisão, o benefício comunicado está limitado a botox.
- Detalhar eventual apoio financeiro ou vínculo institucional com o IMAMA, caso exista. A página comunica conscientização e apoio simbólico, sem afirmar parceria formal ou destinação de receita.
- Revisar as respostas do FAQ sobre o atendimento antes de publicar.
- Depois da publicação autorizada, conferir recebimento dos eventos no painel do Clarity; acompanhar separadamente mensagens recebidas e avaliações agendadas. Validar a abertura do WhatsApp nos aparelhos da equipe.

## Verificação

28 testes automatizados passaram (9 Python e 19 Node) e o build gerou 171 arquivos versionados. As cores de texto/CTA revisadas apresentaram contraste entre 5,67:1 e 9,52:1; a avaliação usa as combinações base de cores, sem afirmar auditoria integral de acessibilidade.

Capturas e conferência visual em Chromium com movimento reduzido, além de validação das interações e reprodução de vídeo. Nas larguras 320, 390, 768, 1024 e 1440 px, o CTA da abertura permaneceu visível, sem rolagem horizontal nem imagens quebradas. Foram verificados menu e Escape, FAQ, álbum e paginação, ampliação de foto, reprodução de vídeo com controles, ocultação do flutuante no rodapé e redirecionamento com UTMs e âncora. Os 11 CTAs geraram uma vez cada evento geral e específico; falha deliberada do GA não introduziu erros. Parâmetro pessoal de teste e mensagens do WhatsApp ficaram fora das propriedades personalizadas. Nenhuma mensagem real foi enviada.
