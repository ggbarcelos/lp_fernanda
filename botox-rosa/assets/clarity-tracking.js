(() => {
  'use strict';

  const campaign = 'botox_rosa_2026';
  const visitorKey = 'botox_rosa_clarity_visitor';
  const uuidPattern = /^[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}$/i;
  const labelPattern = /^[a-z][a-z0-9_]{0,63}$/;

  // Analytics failures must never interrupt navigation or media controls.
  function clarity(...args) {
    try {
      if (typeof window.clarity !== 'function') return;
      const result = window.clarity(...args);
      if (result && typeof result.catch === 'function') result.catch(() => {});
    } catch { /* The site remains usable if tracking is blocked. */ }
  }

  function visitorId() {
    try {
      const stored = window.localStorage.getItem(visitorKey);
      if (stored && uuidPattern.test(stored)) return stored;
    } catch { /* Restricted storage falls back to an ID for this page only. */ }

    let id;
    try {
      if (typeof window.crypto?.randomUUID === 'function') {
        id = window.crypto.randomUUID();
      } else if (typeof window.crypto?.getRandomValues === 'function') {
        const bytes = window.crypto.getRandomValues(new Uint8Array(16));
        bytes[6] = (bytes[6] & 15) | 64;
        bytes[8] = (bytes[8] & 63) | 128;
        const hex = Array.from(bytes, byte => byte.toString(16).padStart(2, '0')).join('');
        id = `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
      }
    } catch { return null; }
    if (!id) return null;
    try { window.localStorage.setItem(visitorKey, id); } catch { /* Keep the in-memory ID. */ }
    return id;
  }

  if (typeof window.clarity === 'function') {
    const id = visitorId();
    // Keep Clarity's own session ID; provide a stable campaign page identifier.
    if (id) clarity('identify', id, undefined, campaign);
  }
  clarity('set', 'campanha', campaign);
  clarity('set', 'pagina', 'botox_rosa');

  // Only campaign labels are copied, never the full URL, query or WhatsApp text.
  const parameters = new URLSearchParams(window.location.search);
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'].forEach(key => {
    const value = parameters.get(key)?.trim();
    if (value && value.length <= 80 && /^[a-z0-9][a-z0-9_. -]*$/i.test(value)) {
      clarity('set', key, value.toLowerCase().replace(/ +/g, '_'));
    }
  });

  document.addEventListener('click', event => {
    const link = event.target.closest?.('[data-whatsapp][data-track-cta]');
    const placement = link?.dataset.trackCta;
    if (!placement || !labelPattern.test(placement)) return;
    clarity('set', 'whatsapp_cta', placement);
    clarity('event', 'whatsapp_click');
    clarity('event', `whatsapp_click_${placement}`);
  }, true);

  const playedVideos = new WeakSet();
  const completedVideos = new WeakSet();
  function trackVideo(event, action, seen) {
    const video = event.target;
    const id = video.dataset?.trackVideo;
    const placement = video.dataset?.trackPlacement;
    if (video.tagName !== 'VIDEO' || !video.closest('.media-dialog') ||
        !id || !labelPattern.test(id) || seen.has(video)) return;
    seen.add(video);
    clarity('set', 'video', id);
    if (placement && labelPattern.test(placement)) clarity('set', 'video_local', placement);
    clarity('event', action);
    clarity('event', `${action}_${id}`);
  }
  // Capture native media events: they do not bubble. Background loops are excluded.
  document.addEventListener('playing', event => trackVideo(event, 'video_play', playedVideos), true);
  document.addEventListener('ended', event => trackVideo(event, 'video_complete', completedVideos), true);

  if (!('IntersectionObserver' in window)) return;
  const sections = new Map();
  function cancelView(state) {
    window.clearTimeout(state.timer);
    state.timer = null;
  }
  function scheduleView(element, state) {
    if (!state.visible || state.recorded || state.timer !== null || document.hidden) return;
    state.timer = window.setTimeout(() => {
      state.timer = null;
      if (!state.visible || document.hidden) return;
      state.recorded = true;
      clarity('event', `section_view_${state.id}`);
      observer.unobserve(element);
    }, 1000);
  }
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const state = sections.get(entry.target);
      if (!state) return;
      state.visible = entry.isIntersecting && entry.intersectionRatio >= 0.5;
      if (state.visible) scheduleView(entry.target, state);
      else cancelView(state);
    });
  }, { threshold: [0, 0.5] });
  document.querySelectorAll('[data-track-section]').forEach(element => {
    const id = element.dataset.trackSection;
    if (!labelPattern.test(id)) return;
    sections.set(element, { id, visible: false, recorded: false, timer: null });
    observer.observe(element);
  });
  document.addEventListener('visibilitychange', () => {
    sections.forEach((state, element) => {
      if (document.hidden) cancelView(state);
      else scheduleView(element, state);
    });
  });
})();
