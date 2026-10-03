(() => {
  'use strict';
  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('.menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav');
  const mobileQuery = window.matchMedia('(max-width: 760px)');
  const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  const assetManifest = document.getElementById('site-assets');
  const assetUrls = assetManifest ? JSON.parse(assetManifest.textContent) : {};
  const campaignAsset = path => assetUrls[path] || path;

  function setMenu(open, returnFocus = false) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    mobileNav.hidden = !open;
    header.classList.toggle('menu-open', open);
    if (returnFocus) toggle.focus();
  }
  toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !mobileNav.hidden) setMenu(false, true);
  });
  document.addEventListener('click', event => {
    if (!mobileNav.hidden && !header.contains(event.target)) setMenu(false);
  });
  header.addEventListener('focusout', event => {
    if (event.relatedTarget && !header.contains(event.relatedTarget) && !mobileNav.hidden) setMenu(false);
  });
  mobileQuery.addEventListener('change', () => setMenu(false));

  let scrollPending = false;
  function updateScroll() {
    header.classList.toggle('scrolled', window.scrollY > 30);
    scrollPending = false;
  }
  window.addEventListener('scroll', () => {
    if (!scrollPending) {
      scrollPending = true;
      requestAnimationFrame(() => {
        // Read geometry before the header class changes to avoid forced layout.
        if (!mobileQuery.matches) updateParallax();
        updateScroll();
      });
    }
  }, { passive: true });
  updateScroll();

  const revealElements = document.querySelectorAll('.reveal');
  let observer;
  if ('IntersectionObserver' in window && !motionQuery.matches) {
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px 35px 0px' });
    revealElements.forEach(element => {
      // Only hide elements once their observer is ready; content works without JS.
      observer.observe(element);
      element.classList.add('will-reveal');
    });
  }
  motionQuery.addEventListener('change', event => {
    if (event.matches) {
      observer?.disconnect();
      revealElements.forEach(element => element.classList.add('is-visible'));
    }
  });

  // Keep the FAQ compact while retaining native keyboard and no-JS behavior.
  const questions = document.querySelectorAll('.faq-list details');
  questions.forEach(question => question.addEventListener('toggle', () => {
    if (question.open) questions.forEach(other => { if (other !== question) other.open = false; });
  }));

  const ambientVideos = [...document.querySelectorAll('[data-ambient]')];
  const dialog = document.querySelector('.media-dialog');
  const dialogMedia = dialog.querySelector('.dialog-media');
  const parallaxItems = [...document.querySelectorAll('[data-parallax]')];
  let lastMediaTrigger;
  let syncDiaryPlayback = () => {};
  const motionIsPaused = () => motionQuery.matches;

  const heroReel = document.querySelector('[data-hero-reel]');
  const heroWatch = document.querySelector('[data-hero-watch]');
  const heroImage = document.querySelector('.hero-portrait img');
  let heroImageReady = !heroImage || heroImage.complete;
  let ambientReady = false;
  function scheduleAmbient() {
    const start = () => { ambientReady = true; syncAmbientVideos(); };
    if ('requestIdleCallback' in window) window.requestIdleCallback(start, { timeout: 2000 });
    else window.setTimeout(start, 200);
  }
  if (document.readyState === 'complete') scheduleAmbient();
  else window.addEventListener('load', scheduleAmbient, { once: true });
  if (!heroImageReady) {
    const finishHeroImage = () => { heroImageReady = true; syncAmbientVideos(); };
    heroImage.addEventListener('load', finishHeroImage, { once: true });
    heroImage.addEventListener('error', finishHeroImage, { once: true });
  }
  const heroClips = [
    ['botox_rosa.mp4', 'fernanda-poster.jpg', 'Um convite da Dra. Fernanda', 'convite'],
    ['fernanda1.mp4', 'fernanda1-poster.jpg', 'A campanha, pela Dra. Fernanda', 'proposito'],
    ['editado1.mp4', 'historia-poster.jpg', 'A causa na voz de quem participou', 'historia'],
    ['tiago1.mp4', 'camiseta-poster.jpg', 'O momento de vestir a causa', 'gesto'],
    ['vere2.mp4', 'acolhimento-poster.jpg', 'Um olhar atento para cada pessoa', 'cuidado'],
    ['vide_vere.mp4', 'gesto-poster.jpg', 'Técnica e cuidado, de perto', 'bastidores'],
    ['video_vere3.mp4', 'conexoes-poster.jpg', 'Mais uma voz pela causa', 'conexoes']
  ];
  let heroClipIndex = -1;
  if (heroReel && heroWatch) {
    function updateHeroWatch() {
      const clipIndex = Math.min(heroClips.length - 1, Math.floor(heroReel.currentTime / 5));
      if (clipIndex === heroClipIndex) return;
      heroClipIndex = clipIndex;
      const [file, poster, title, videoId] = heroClips[clipIndex];
      const source = `assets/optimized/videos/${file}`;
      heroWatch.dataset.media = campaignAsset(source);
      heroWatch.dataset.trackVideo = videoId;
      heroWatch.dataset.poster = campaignAsset(`assets/media/${poster}`);
      heroWatch.dataset.title = title;
      heroWatch.dataset.description = 'Um registro da campanha Botox Rosa na FB Harmonização & Odontologia.';
      heroWatch.setAttribute('aria-label', `Assistir com áudio: ${title}`);
    }
    heroReel.addEventListener('timeupdate', updateHeroWatch);
    heroReel.addEventListener('seeked', updateHeroWatch);
    updateHeroWatch();
  }

  function syncAmbientVideos() {
    const canPlay = ambientReady && heroImageReady && !navigator.connection?.saveData && !motionIsPaused() && !document.hidden && !dialog.open;
    syncDiaryPlayback();
    ambientVideos.forEach(video => {
      if (canPlay && video.dataset.inView === 'true') {
        if (!video.hasAttribute('src')) video.src = video.dataset.src;
        video.play().catch(() => { /* Keep the poster if autoplay is unavailable. */ });
      } else {
        video.pause();
      }
    });
  }
  function updateMotionPreference() {
    const paused = motionIsPaused();
    document.body.classList.toggle('motion-paused', paused);
    if (paused) parallaxItems.forEach(item => item.style.removeProperty('--parallax'));
    syncAmbientVideos();
  }
  motionQuery.addEventListener('change', updateMotionPreference);
  document.addEventListener('visibilitychange', syncAmbientVideos);
  if ('IntersectionObserver' in window) {
    const videoObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => { entry.target.dataset.inView = String(entry.isIntersecting); });
      syncAmbientVideos();
    }, { threshold: 0.15 });
    ambientVideos.forEach(video => videoObserver.observe(video));
  }
  updateMotionPreference();

  const hero = document.querySelector('.hero-cinema');
  function updateParallax() {
    if (!motionIsPaused() && !mobileQuery.matches) {
      const distance = Math.min(1, Math.max(0, -hero.getBoundingClientRect().top / hero.offsetHeight));
      parallaxItems.forEach(item => item.style.setProperty('--parallax', `${distance * Number(item.dataset.parallax)}px`));
    }
  }
  mobileQuery.addEventListener('change', () => {
    parallaxItems.forEach(item => item.style.removeProperty('--parallax'));
  });

  function closeMedia() {
    dialog.close();
  }
  document.querySelectorAll('[data-media]').forEach(trigger => {
    trigger.addEventListener('click', () => {
      lastMediaTrigger = trigger;
      dialog.querySelector('#media-title').textContent = trigger.dataset.title;
      dialog.querySelector('#media-description').textContent = trigger.dataset.description;
      dialogMedia.replaceChildren();
      if (trigger.dataset.type === 'image') {
        const photo = document.createElement('img');
        photo.src = trigger.dataset.media;
        photo.alt = trigger.dataset.title;
        dialogMedia.append(photo);
      } else {
        const video = document.createElement('video');
        video.dataset.trackVideo = trigger.dataset.trackVideo || '';
        video.dataset.trackPlacement = trigger.dataset.trackPlacement || (trigger.hasAttribute('data-hero-watch') ? 'hero' : 'galeria');
        video.controls = true;
        video.playsInline = true;
        video.preload = 'metadata';
        video.src = trigger.dataset.media;
        if (trigger.dataset.poster) video.poster = trigger.dataset.poster;
        video.setAttribute('aria-label', trigger.dataset.title);
        dialogMedia.append(video);
      }
      dialog.showModal();
      document.body.classList.add('dialog-open');
      syncAmbientVideos();
      const activeVideo = dialogMedia.querySelector('video');
      if (activeVideo) activeVideo.play().catch(() => { /* Native controls remain available. */ });
    });
  });
  dialog.querySelector('.dialog-close').addEventListener('click', closeMedia);
  dialog.addEventListener('click', event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) closeMedia();
  });
  dialog.addEventListener('close', () => {
    const video = dialogMedia.querySelector('video');
    if (video) {
      video.pause();
      video.removeAttribute('src');
      video.load();
    }
    dialogMedia.replaceChildren();
    document.body.classList.remove('dialog-open');
    syncAmbientVideos();
    lastMediaTrigger?.focus({ preventScroll: true });
  });

  const diary = document.querySelector('.diary-album');
  if (diary) {
    const cards = [...diary.querySelectorAll('.diary-card')];
    const steps = [...diary.querySelectorAll('[data-diary-step]')];
    const thumbNav = diary.querySelector('.diary-thumbs');
    const thumbs = [];
    diary.classList.toggle('is-single', cards.length < 2);
    const pauseButton = diary.querySelector('[data-diary-pause]');
    const previews = cards.map(card => card.querySelector('video'));
    previews.forEach(video => {
      if (video?.poster) video.parentElement.style.backgroundImage = `url("${video.poster}")`;
    });
    let current = 0;
    let timer;
    let inView = !('IntersectionObserver' in window);
    let userPaused = false;
    let focusPaused = false;
    const canPreview = () => inView && !userPaused && !motionQuery.matches &&
      !navigator.connection?.saveData && !document.hidden && !dialog.open;
    const canMix = () => canPreview() && !focusPaused;

    function stopTimer() {
      clearTimeout(timer);
      timer = undefined;
    }
    syncDiaryPlayback = () => {
      const playing = canMix();
      diary.classList.toggle('mix-playing', canPreview());
      previews.forEach((video, position) => {
        if (!video) return;
        if (canPreview() && position === current) {
          if (!video.hasAttribute('src')) video.src = video.dataset.previewSrc;
          video.play().catch(() => { /* The cover and manual navigation remain available. */ });
        } else video.pause();
      });
      if (!playing) stopTimer();
      else if (!timer && cards.length > 1) {
        timer = setTimeout(() => {
          timer = undefined;
          showDiaryRecord(current + 1);
        }, cards[current].dataset.type === 'video' ? 6000 : 4500);
      }
      if (pauseButton) {
        pauseButton.textContent = userPaused ? 'Retomar mix' : 'Pausar mix';
        pauseButton.setAttribute('aria-pressed', String(userPaused));
      }
    };
    function showDiaryRecord(index) {
      if (!cards.length) return;
      stopTimer();
      current = (index + cards.length) % cards.length;
      cards.forEach((card, position) => {
        card.hidden = position !== current;
        card.classList.toggle('is-current', position === current);
        const preview = previews[position];
        if (preview && position !== current) {
          preview.pause();
          if (preview.readyState) preview.currentTime = 0;
        }
      });
      thumbs.forEach((thumb, position) => thumb.setAttribute('aria-pressed', String(position === current)));
      const status = diary.querySelector('[data-diary-status]');
      // Automatic changes stay quiet for screen readers; user navigation is announced.
      status.setAttribute('aria-live', canMix() ? 'off' : 'polite');
      status.textContent = `${String(current + 1).padStart(2, '0')} / ${String(cards.length).padStart(2, '0')}`;
      syncDiaryPlayback();
    }
    if (pauseButton) {
      pauseButton.hidden = cards.length < 2;
      pauseButton.addEventListener('click', () => {
        userPaused = !userPaused;
        syncDiaryPlayback();
      });
    }
    diary.addEventListener('focusin', event => { focusPaused = event.target !== pauseButton; syncDiaryPlayback(); });
    diary.addEventListener('focusout', event => {
      if (!diary.contains(event.relatedTarget)) { focusPaused = false; syncDiaryPlayback(); }
    });
    motionQuery.addEventListener('change', syncDiaryPlayback);
    navigator.connection?.addEventListener('change', syncDiaryPlayback);
    if ('IntersectionObserver' in window) {
      const mixObserver = new IntersectionObserver(entries => {
        inView = entries[0].isIntersecting;
        syncDiaryPlayback();
      }, { threshold: .25 });
      mixObserver.observe(diary);
    }
    if (thumbNav && cards.length > 1) {
      cards.forEach((card, index) => {
        const thumb = document.createElement('button');
        thumb.type = 'button';
        thumb.className = 'diary-thumb';
        const isVideo = card.dataset.type === 'video';
        thumb.setAttribute('aria-label', `Ver ${isVideo ? 'vídeo' : 'foto'} ${index + 1} da campanha de 2026`);
        thumb.setAttribute('aria-controls', 'diary-stage');
        const previewSrc = card.dataset.poster || card.querySelector('.diary-visual img')?.getAttribute('src');
        if (previewSrc) {
          const image = document.createElement('img');
          image.src = previewSrc;
          image.alt = '';
          image.loading = 'lazy';
          image.decoding = 'async';
          thumb.append(image);
        }
        const label = document.createElement('span');
        label.textContent = `${String(index + 1).padStart(2, '0')} / ${isVideo ? 'Vídeo' : 'Foto'}`;
        thumb.append(label);
        thumb.addEventListener('click', () => showDiaryRecord(index));
        thumbs.push(thumb);
        thumbNav.append(thumb);
      });
      thumbNav.hidden = false;
    }
    steps.forEach(button => {
      button.hidden = cards.length < 2;
      button.addEventListener('click', () => showDiaryRecord(current + Number(button.dataset.diaryStep)));
    });
    diary.addEventListener('keydown', event => {
      if (!['ArrowLeft', 'ArrowRight'].includes(event.key) || cards.length < 2) return;
      const focusedCard = event.target.closest('.diary-card');
      event.preventDefault();
      showDiaryRecord(current + (event.key === 'ArrowRight' ? 1 : -1));
      if (focusedCard) cards[current].focus({ preventScroll: true });
    });
    mobileQuery.addEventListener('change', () => showDiaryRecord(current));
    showDiaryRecord(0);
  }

  const pastAlbum = document.querySelector('.past-album');
  function syncPastAlbumLayout() {
    if (pastAlbum) pastAlbum.open = window.location.hash === '#momentos';
  }
  syncPastAlbumLayout();
  function openPastAlbum() {
    if (pastAlbum && window.location.hash === '#momentos') pastAlbum.open = true;
  }
  document.querySelectorAll('a[href="#momentos"]').forEach(link => {
    link.addEventListener('click', () => { if (pastAlbum) pastAlbum.open = true; });
  });
  window.addEventListener('hashchange', openPastAlbum);
  openPastAlbum();

  const albumCards = [...document.querySelectorAll('.moments-track>.moment-card')];
  // Reuse the image selected by srcset; below-fold backgrounds must not prefetch the album.
  document.querySelectorAll('.moment-visual img, .diary-visual img').forEach(image => {
    function syncBackground() {
      if (image.naturalWidth) image.parentElement.style.backgroundImage = `url("${image.currentSrc || image.src}")`;
    }
    image.addEventListener('load', syncBackground);
    if (image.complete) syncBackground();
  });
  const albumNavigation = document.querySelector('.album-pagination');
  if (albumCards.length && albumNavigation) {
    const pageSize = 6;
    const pageCount = Math.ceil(albumCards.length / pageSize);
    const pageButtons = [];
    let albumPage = 0;
    function showAlbumPage(page) {
      albumPage = Math.max(0, Math.min(page, pageCount - 1));
      const first = albumPage * pageSize;
      albumCards.forEach((card, index) => { card.hidden = index < first || index >= first + pageSize; });
      pageButtons.forEach((button, index) => {
        if (index === albumPage) button.setAttribute('aria-current', 'page');
        else button.removeAttribute('aria-current');
      });
      albumNavigation.querySelector('[data-album-step="-1"]').disabled = albumPage === 0;
      albumNavigation.querySelector('[data-album-step="1"]').disabled = albumPage === pageCount - 1;
      albumNavigation.querySelector('.album-status').textContent = `Registros ${first + 1}–${Math.min(first + pageSize, albumCards.length)} de ${albumCards.length}`;
    }
    for (let page = 0; page < pageCount; page++) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'album-page-button';
      button.textContent = String(page + 1);
      button.setAttribute('aria-label', `Página ${page + 1} do álbum`);
      button.setAttribute('aria-controls', 'album-grid');
      button.addEventListener('click', () => showAlbumPage(page));
      albumNavigation.querySelector('.album-pages').append(button);
      pageButtons.push(button);
    }
    albumNavigation.querySelectorAll('[data-album-step]').forEach(button => {
      button.addEventListener('click', () => showAlbumPage(albumPage + Number(button.dataset.albumStep)));
    });
    showAlbumPage(0);
    albumNavigation.hidden = pageCount <= 1;
  }

  // Optional conversion hook for hosts that already use Google Analytics.
  document.querySelectorAll('[data-whatsapp]').forEach(link => {
    link.addEventListener('click', () => {
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'whatsapp_click', { campaign: 'botox_rosa_2026', link_text: link.textContent.trim() });
      }
    });
  });
})();
