const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('botox-rosa/assets/analytics.js', 'utf8');
function visit({hostname = 'fernandabeltrao.com.br', search = '', referrer = '', api} = {}) {
  const handlers = new Map(), scripts = [];
  const window = {location: {hostname, search}, ...(api ? {gtag: api} : {})};
  const document = {referrer, addEventListener: (name, fn) => handlers.set(name, fn), createElement: () => ({}), head: {appendChild: el => scripts.push(el)}};
  const context = {window, document, URL, URLSearchParams};
  vm.runInNewContext(source, context);
  return {window, scripts, handlers, rerun: () => vm.runInNewContext(source, context), calls: () => [...(window.dataLayer || [])].map(a => [...a]), click: dataset => handlers.get('click')({target: {closest: () => ({dataset})}})};
}
test('production initializes one tag and one page config; repeated initialization stays idempotent', () => {
  const v = visit(); v.rerun();
  assert.equal(v.scripts.length, 1);
  assert.equal(v.scripts[0].src, 'https://www.googletagmanager.com/gtag/js?id=G-FGM9MBKS4D');
  assert.equal(v.calls().filter(c => c[0] === 'config').length, 1);
  const config = v.calls().find(c => c[0] === 'config');
  assert.equal(config[1], 'G-FGM9MBKS4D');
  assert.equal(config[2].allow_google_signals, false);
  assert.equal(config[2].allow_ad_personalization_signals, false);
});
test('only campaign labels enter page_location and referrer query data is excluded', () => {
  const v = visit({search:'?utm_source=instagram&utm_medium=organic_social&utm_campaign=botox_rosa_2026&utm_content=stories&utm_id=outubro&email=patient@example.com&text=private&gclid=private&utm_term=medical',referrer:'https://example.com/private?email=patient@example.com#private'});
  const config = v.calls().find(c => c[0] === 'config')[2];
  assert.equal(config.page_referrer, 'https://example.com/');
  const page = new URL(config.page_location);
  assert.equal(page.searchParams.get('utm_source'), 'instagram');
  assert.equal(page.searchParams.get('utm_campaign'), 'botox_rosa_2026');
  assert.equal(page.searchParams.size, 5);
  assert.ok(!JSON.stringify(v.calls()).includes('private'));
  assert.ok(!JSON.stringify(v.calls()).includes('patient@example.com'));
});
test('one click emits one GA event with placement, with no phone, link or message', () => {
  const v = visit(); v.click({trackCta:'hero',trackIntent:'duvidas',text:'private'});
  const events = v.calls().filter(c => c[0] === 'event');
  assert.equal(events.length, 1);assert.equal(events[0][1], 'whatsapp_click');
  assert.deepEqual(JSON.parse(JSON.stringify(events[0][2])), {send_to:'G-FGM9MBKS4D',campaign:'botox_rosa_2026',cta_position:'hero',contact_intent:'duvidas'});
  v.click({trackCta:'patient@example.com'}); assert.equal(v.calls().filter(c => c[0] === 'event').length, 1);
});
test('previews and other hosts never initialize or send analytics', () => {
  for (const hostname of ['localhost','127.0.0.1','example.com']) {const v=visit({hostname});assert.equal(v.scripts.length,0);assert.equal(v.calls().length,0);assert.equal(v.handlers.size,0);}
});
test('blocked and rejecting analytics do not throw on contact', async () => {
  for (const api of [()=>{throw Error('blocked')},()=>Promise.reject(Error('blocked'))]) {const v=visit({api});assert.doesNotThrow(()=>v.click({trackCta:'hero',trackIntent:'horarios'}));}
  await new Promise(r=>setImmediate(r));
});
test('the LP loads analytics once and the old GA click hook is absent', () => {
  const html = fs.readFileSync('botox-rosa/index.html','utf8');
  assert.equal(html.split('src="assets/analytics.js"').length-1,1);
  assert.ok(!fs.readFileSync('botox-rosa/assets/campaign.js','utf8').includes("window.gtag('event'"));
  assert.ok(!fs.readFileSync('index.html','utf8').includes('analytics.js'));
});
