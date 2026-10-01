(() => {
  'use strict';
  const release = document.querySelector('meta[name="site-version"]');
  if (!release || release.content === 'development' || !/^https?:$/.test(location.protocol)) return;

  let checking = false;
  let pendingVersion;
  let navigating = false;

  function applyUpdate() {
    if (!pendingVersion || navigating || document.hidden || document.querySelector('dialog[open]')) return;
    const target = new URL(location.href);
    // A single navigation per revision also avoids loops during CDN propagation.
    if (target.searchParams.get('_site_v') === pendingVersion) return;
    target.searchParams.set('_site_v', pendingVersion);
    navigating = true;
    location.replace(target.href);
  }

  async function checkVersion() {
    if (checking || navigating || document.hidden) return;
    checking = true;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    try {
      const manifest = new URL(release.dataset.manifest, document.baseURI);
      manifest.searchParams.set('_check', Date.now().toString());
      const response = await fetch(manifest.href, { cache: 'no-store', signal: controller.signal });
      if (!response.ok) return;
      const latest = await response.json();
      if (!/^[a-f0-9]{40}$/.test(latest.revision)) return;
      pendingVersion = latest.revision === release.content ? undefined : latest.revision;
      applyUpdate();
    } catch {
      // Offline visits and unavailable checks keep the current page usable.
    } finally {
      clearTimeout(timeout);
      checking = false;
    }
  }

  window.addEventListener('pageshow', checkVersion);
  window.addEventListener('online', checkVersion);
  document.addEventListener('visibilitychange', checkVersion);
  document.addEventListener('close', applyUpdate, true);
  checkVersion();
})();
