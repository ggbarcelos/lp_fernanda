(() => {
  'use strict';

  const measurementId = 'G-FGM9MBKS4D';
  // Local previews must never pollute the clinic's production reports.
  if (!['fernandabeltrao.com.br', 'www.fernandabeltrao.com.br'].includes(window.location.hostname)) return;
  if (window.fernandaAnalyticsInitialized) return;
  window.fernandaAnalyticsInitialized = true;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  function track(...args) {
    try {
      const result = window.gtag(...args);
      if (result && typeof result.catch === 'function') result.catch(() => {});
    } catch { /* Analytics failures must not interrupt contact or media. */ }
  }

  // Send only campaign labels from the URL, never arbitrary query data or fragments.
  const page = new URL('https://fernandabeltrao.com.br/botox-rosa/');
  const parameters = new URLSearchParams(window.location.search);
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_id'].forEach(key => {
    const value = parameters.get(key)?.trim();
    if (value && value.length <= 80 && /^[a-z0-9][a-z0-9_. -]*$/i.test(value)) page.searchParams.set(key, value);
  });
  let referrer = '';
  try {
    const source = new URL(document.referrer);
    if (['https:', 'http:'].includes(source.protocol)) referrer = source.origin + '/';
  } catch { /* A direct visit has no referrer. */ }

  track('js', new Date());
  track('config', measurementId, {
    page_location: page.href,
    page_referrer: referrer,
    page_title: 'Botox Rosa 2026 | Dra. Fernanda Beltrão',
    allow_google_signals: false,
    allow_ad_personalization_signals: false
  });

  document.addEventListener('click', event => {
    const link = event.target.closest?.('[data-whatsapp][data-track-cta]');
    const placement = link?.dataset.trackCta;
    if (!placement || !/^[a-z][a-z0-9_]{0,63}$/.test(placement)) return;
    const details = { send_to: measurementId, campaign: 'botox_rosa_2026', cta_position: placement };
    const intent = link.dataset.trackIntent;
    if (intent === 'duvidas' || intent === 'horarios') details.contact_intent = intent;
    track('event', 'whatsapp_click', details);
  }, true);

  const tag = document.createElement('script');
  tag.async = true;
  tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + measurementId;
  document.head.appendChild(tag);
})();
