const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const {test} = require('node:test');
const script = fs.readFileSync('assets/js/site-update.js', 'utf8');
const oldVersion = 'a'.repeat(40), newVersion = 'b'.repeat(40);

async function visit({version = oldVersion, latest = version, href = 'https://fernandabeltrao.com.br/botox-rosa/?utm_source=instagram#momentos', openDialog = false, hidden = false, fail = false} = {}) {
  const requests = [], navigations = [], windowEvents = {}, documentEvents = {};
  const document = {
    hidden, baseURI: href,
    querySelector: selector => selector.startsWith('meta') ? {content:version, dataset:{manifest:'../site-version.json'}} : openDialog ? {} : null,
    addEventListener: (event, listener) => { documentEvents[event] = listener; }
  };
  const context = {
    document, location:{href, protocol:'https:', replace: target => navigations.push(target)},
    window:{addEventListener: (event, listener) => { windowEvents[event] = listener; }},
    URL, Date, AbortController, setTimeout, clearTimeout,
    fetch: async (url, options) => {
      requests.push({url, options});
      if (fail) throw new Error('Offline');
      return {ok:true, json: async () => ({revision:latest})};
    }
  };
  vm.runInNewContext(script, context);
  await new Promise(resolve => setImmediate(resolve));
  return {requests, navigations, context, windowEvents, documentEvents, closeDialog: () => { openDialog = false; }};
}

test('checks current release without storing or reusing cached manifest', async () => {
  const result = await visit();
  assert.equal(result.requests.length, 1);
  assert.equal(result.requests[0].options.cache, 'no-store');
  const manifest = new URL(result.requests[0].url);
  assert.equal(manifest.pathname, '/site-version.json');
  assert.ok(manifest.searchParams.has('_check'));
  assert.equal(result.navigations.length, 0);
});

test('cached HTML navigates to new release and retains tracking and anchor', async () => {
  const result = await visit({latest:newVersion});
  assert.equal(result.navigations.length, 1);
  const target = new URL(result.navigations[0]);
  assert.equal(target.searchParams.get('_site_v'), newVersion);
  assert.equal(target.searchParams.get('utm_source'), 'instagram');
  assert.equal(target.hash, '#momentos');
});

test('stale CDN response cannot trigger an endless reload', async () => {
  const result = await visit({latest:newVersion, href:`https://fernandabeltrao.com.br/botox-rosa/?_site_v=${newVersion}`});
  assert.equal(result.navigations.length, 0);
});

test('offline or invalid manifest leaves the page usable', async () => {
  for (const options of [{fail:true}, {latest:'invalid'}]) {
    const result = await visit(options);
    assert.equal(result.navigations.length, 0);
  }
});

test('local development does not fetch a production release', async () => {
  const result = await visit({version:'development'});
  assert.equal(result.requests.length, 0);
});

test('open media finishes before automatic navigation', async () => {
  const result = await visit({latest:newVersion, openDialog:true});
  assert.equal(result.navigations.length, 0);
  result.closeDialog();
  result.documentEvents.close();
  assert.equal(result.navigations.length, 1);
});

test('returning to a hidden tab and restoring a page check the release', async () => {
  const result = await visit({hidden:true,latest:newVersion});
  assert.equal(result.requests.length, 0);
  result.context.document.hidden = false;
  await result.documentEvents.visibilitychange();
  assert.equal(result.navigations.length, 1);
  const restored = await visit();
  await restored.windowEvents.pageshow({persisted:true});
  assert.equal(restored.requests.length, 2);
});
