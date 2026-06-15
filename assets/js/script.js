document.addEventListener('DOMContentLoaded', function () {
  // Nav scroll
  const nav = document.querySelector('.nav');
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });

  // Mobile menu
  const toggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('open');
      toggle.classList.toggle('active');
      toggle.setAttribute('aria-expanded', isOpen);
    });
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        toggle.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Scroll reveal
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  // Testimonials infinite scroll
  const track = document.getElementById('testimonialsTrack');
  if (track) {
    const cards = track.querySelectorAll('.testimonial-card');
    if (cards.length > 1) {
      const cardStyle = cards[0].currentStyle || window.getComputedStyle(cards[0]);
      const cardWidth = cards[0].offsetWidth + parseInt(cardStyle.marginRight || 0);
      const gap = 24;
      const step = cardWidth + gap;
      const total = cards.length;

      // Clone cards for seamless loop
      for (let i = 0; i < total; i++) {
        const clone = cards[i].cloneNode(true);
        track.appendChild(clone);
      }

      let pos = 0;
      let running = true;

      function scroll() {
        if (!running) return;
        pos -= 0.6;
        if (pos <= -(total * step)) pos = 0;
        track.style.transform = `translateX(${pos}px)`;
        requestAnimationFrame(scroll);
      }

      const slider = track.parentElement;
      slider.addEventListener('mouseenter', () => { running = false; });
      slider.addEventListener('mouseleave', () => { running = true; requestAnimationFrame(scroll); });

      // Pause while tab is hidden
      document.addEventListener('visibilitychange', () => {
        running = !document.hidden;
        if (running) requestAnimationFrame(scroll);
      });

      scroll();
    }
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // Parallax effect on hero image
  const heroImage = document.querySelector('.hero-image-wrapper');
  if (heroImage && window.innerWidth > 768) {
    window.addEventListener('mousemove', (e) => {
      const rect = heroImage.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      heroImage.style.transform = `perspective(800px) rotateY(${x * 4}deg) rotateX(${y * -4}deg)`;
    });
    heroImage.addEventListener('mouseleave', () => {
      heroImage.style.transform = 'perspective(800px) rotateY(0deg) rotateX(0deg)';
    });
  }
});
