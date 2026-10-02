const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const crypto = require('node:crypto');
const {test} = require('node:test');

const script = fs.readFileSync('botox-rosa/assets/clarity-tracking.js', 'utf8');
const visitorKey = 'botox_rosa_clarity_visitor';

function visit({storage = new Map(), blockedStorage = false, api = 'ready', search = '', observer = true, secureRandom = true, fallbackRandom = false, hidden = false} = {}) {
  const calls = [], handlers = new Map(), timers = new Map();
  const sections = ['origem', 'imama', 'galeria', 'profissional', 'duvidas', 'convite_final']
    .map(id => ({dataset: {trackSection: id}}));
  let observerInstance, nextTimer = 0;
  const document = {
    hidden,
    querySelectorAll: () => sections,
    addEventListener: (name, callback, capture) => handlers.set(name, {callback, capture})
  };
  const window = {
    location: {search},
    crypto: secureRandom ? fallbackRandom ? {getRandomValues: crypto.webcrypto.getRandomValues.bind(crypto.webcrypto)} : {randomUUID: crypto.randomUUID} : {},
    get localStorage() {
      if (blockedStorage) throw new Error('Storage denied');
      return {getItem: key => storage.get(key), setItem: (key, value) => storage.set(key, value)};
    },
    setTimeout(callback, delay) {
      assert.equal(delay, 1000);
      const id = ++nextTimer;
      timers.set(id, callback);
      return id;
    },
    clearTimeout: id => timers.delete(id)
  };
  if (api !== 'missing') window.clarity = (...args) => {
    if (api === 'throw') throw new Error('Tracker unavailable');
    calls.push(args);
    if (api === 'reject') return Promise.reject(new Error('Rejected'));
  };
  class IntersectionObserver {
    constructor(callback) { this.callback = callback; this.observed = new Set(); observerInstance = this; }
    observe(element) { this.observed.add(element); }
    unobserve(element) { this.observed.delete(element); }
  }
  if (observer) window.IntersectionObserver = IntersectionObserver;
  vm.runInNewContext(script, {window, document, URLSearchParams, IntersectionObserver});
  return {
    calls, storage, window, document, handlers, timers, sections,
    events: () => calls.filter(call => call[0] === 'event').map(call => call[1]),
    dispatch: (name, target) => handlers.get(name).callback({target}),
    intersect: (id, ratio) => {
      const target = sections.find(section => section.dataset.trackSection === id);
      observerInstance.callback([{target, isIntersecting: ratio > 0, intersectionRatio: ratio}]);
    },
    tick: () => {
      const pending = [...timers.values()];
      timers.clear();
      pending.forEach(callback => callback());
    }
  };
}

function clickTarget(placement) {
  return {closest: () => ({dataset: {trackCta: placement}})};
}
function videoTarget(id, placement = 'galeria', inDialog = true) {
  return {tagName: 'VIDEO', dataset: {trackVideo: id, trackPlacement: placement}, closest: () => inDialog ? {} : null};
}

test('return visits reuse a random browser ID and retain Clarity session management', () => {
  const first = visit(), second = visit({storage: first.storage}), other = visit();
  const identify = first.calls.find(call => call[0] === 'identify');
  assert.match(identify[1], /^[a-f0-9-]{36}$/);
  assert.equal(identify[2], undefined);
  assert.equal(identify[3], 'botox_rosa_2026');
  assert.equal(second.calls.find(call => call[0] === 'identify')[1], identify[1]);
  assert.notEqual(other.calls.find(call => call[0] === 'identify')[1], identify[1]);
  assert.ok(first.calls.some(call => call.join(':') === 'set:campanha:botox_rosa_2026'));
});

test('invalid stored identifiers are replaced rather than forwarded', () => {
  const result = visit({storage: new Map([[visitorKey, 'patient@example.com']])});
  assert.match(result.storage.get(visitorKey), /^[a-f0-9-]{36}$/);
  assert.ok(!JSON.stringify(result.calls).includes('patient@example.com'));
});

test('restricted storage and unavailable secure randomness do not break tracking', () => {
  const restricted = visit({blockedStorage: true});
  assert.ok(restricted.calls.some(call => call[0] === 'identify'));
  const fallback = visit({fallbackRandom: true});
  assert.match(fallback.storage.get(visitorKey), /^[a-f0-9]{8}-(?:[a-f0-9]{4}-){3}[a-f0-9]{12}$/);
  const noRandom = visit({secureRandom: false});
  assert.ok(!noRandom.calls.some(call => call[0] === 'identify'));
  noRandom.dispatch('click', clickTarget('hero'));
  assert.deepEqual(noRandom.events(), ['whatsapp_click', 'whatsapp_click_hero']);
});

test('campaign tags use only validated UTM labels and ignore personal/query content', () => {
  const result = visit({search: '?utm_source=Instagram&utm_medium=organic_social&utm_campaign=Botox%20Rosa%202026&utm_content=reels_lancamento&email=patient@example.com&text=private&gclid=secret'});
  for (const [key, value] of Object.entries({utm_source: 'instagram', utm_medium: 'organic_social', utm_campaign: 'botox_rosa_2026', utm_content: 'reels_lancamento'})) {
    assert.ok(result.calls.some(call => call[0] === 'set' && call[1] === key && call[2] === value));
  }
  assert.ok(!/patient|private|secret/.test(JSON.stringify(result.calls)));
  const unsafe = visit({search: '?utm_source=patient%40example.com&utm_content=' + 'a'.repeat(81)});
  assert.ok(!unsafe.calls.some(call => call[1].startsWith('utm_')));
  const direct = visit();
  assert.ok(!direct.calls.some(call => call[1].startsWith('utm_')));
});

test('every WhatsApp placement has an independently filterable event, including clicks on children', () => {
  const result = visit();
  for (const placement of ['cabecalho', 'menu_mobile', 'hero', 'origem', 'galeria', 'duvidas', 'convite_final', 'flutuante']) {
    result.dispatch('click', clickTarget(placement));
    assert.equal(result.events().at(-1), `whatsapp_click_${placement}`);
  }
  assert.equal(result.events().filter(event => event === 'whatsapp_click').length, 8);
  result.dispatch('click', {closest: () => null});
  result.dispatch('click', clickTarget('invalid label'));
  assert.equal(result.events().length, 16);
});

test('background playback is excluded; actual dialog playback counts once per opening', () => {
  const result = visit();
  result.dispatch('playing', videoTarget('convite', 'hero', false));
  assert.deepEqual(result.events(), []);
  const video = videoTarget('convite', 'hero');
  result.dispatch('playing', video);
  result.dispatch('playing', video); // Resume after pause/buffering.
  assert.deepEqual(result.events(), ['video_play', 'video_play_convite']);
  result.dispatch('ended', video);
  result.dispatch('ended', video);
  assert.deepEqual(result.events().slice(-2), ['video_complete', 'video_complete_convite']);
  result.dispatch('playing', videoTarget('convite')); // New dialog opening.
  assert.equal(result.events().filter(event => event === 'video_play').length, 2);
  assert.equal(result.handlers.get('playing').capture, true);
  assert.equal(result.handlers.get('ended').capture, true);
});

test('passing a section quickly does not count, but a continuous visible interval does', () => {
  const result = visit();
  result.intersect('origem', 0.49);
  assert.equal(result.timers.size, 0);
  result.intersect('origem', 0.5);
  result.intersect('origem', 0);
  result.tick();
  assert.deepEqual(result.events(), []);
  result.intersect('origem', 1);
  result.tick();
  result.intersect('origem', 0);
  result.intersect('origem', 1);
  result.tick();
  assert.deepEqual(result.events(), ['section_view_origem']);
});

test('hidden-tab time is excluded and sections are independent', () => {
  const result = visit();
  result.intersect('origem', 1);
  result.document.hidden = true;
  result.dispatch('visibilitychange');
  result.tick();
  assert.deepEqual(result.events(), []);
  result.document.hidden = false;
  result.dispatch('visibilitychange');
  result.intersect('imama', 1);
  result.tick();
  assert.deepEqual(result.events(), ['section_view_origem', 'section_view_imama']);
});

test('unavailable observers and missing, throwing or rejecting APIs leave interactions usable', async () => {
  for (const options of [{observer: false}, {api: 'missing'}, {api: 'throw'}, {api: 'reject'}]) {
    const result = visit(options);
    assert.doesNotThrow(() => result.dispatch('click', clickTarget('hero')));
    assert.doesNotThrow(() => result.dispatch('playing', videoTarget('proposito')));
    assert.doesNotThrow(() => result.dispatch('ended', videoTarget('proposito')));
  }
  await new Promise(resolve => setImmediate(resolve)); // Verify promise rejections are handled.
});

test('the HTML wires every CTA, video and section to stable labels before campaign initialization', () => {
  const html = fs.readFileSync('botox-rosa/index.html', 'utf8');
  const ctas = [...html.matchAll(/<a\b[^>]*\bdata-whatsapp\b[^>]*>/g)].map(match => match[0]);
  assert.equal(ctas.length, 9);
  assert.equal(new Set(ctas.map(tag => tag.match(/data-track-cta="([^"]+)"/)?.[1])).size, 9);
  const videos = [...html.matchAll(/<button\b[^>]*\bdata-media="[^"]+\.mp4"[^>]*>/g)].map(match => match[0]);
  assert.equal(videos.length, 13);
  assert.ok(videos.every(tag => /data-track-video="[a-z][a-z0-9_]{0,63}"/.test(tag)));
  assert.equal([...html.matchAll(/data-track-section="[^"]+"/g)].length, 7);
  assert.ok(html.includes('data-track-cta="campanha_2026"'));
  assert.ok(html.includes('data-track-section="campanha_2026"'));
  assert.ok(html.indexOf('assets/clarity-tracking.js') < html.indexOf('assets/campaign.js'));
});
