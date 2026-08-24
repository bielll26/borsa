/* =========================================================
   Clínica Dental RAIS · comportamiento de la página principal
   ========================================================= */
(function () {
  'use strict';

  const $  = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------
     Año en curso en el pie
     --------------------------------------------------- */
  const year = $('#year');
  if (year) year.textContent = new Date().getFullYear();

  /* ---------------------------------------------------
     Cabecera fija + barra de progreso de lectura
     --------------------------------------------------- */
  const header   = $('#header');
  const progress = $('#progress');
  const toTop    = $('#toTop');

  function onScroll() {
    const y = window.scrollY || document.documentElement.scrollTop;

    if (header) header.classList.toggle('is-stuck', y > 12);
    if (toTop)  toTop.classList.toggle('is-visible', y > 600);

    if (progress) {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';
    }
  }

  let ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { onScroll(); ticking = false; });
  }, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  }

  /* ---------------------------------------------------
     Menú móvil
     --------------------------------------------------- */
  const burger = $('#burger');
  const drawer = $('#drawer');
  const scrim  = $('#scrim');
  const dClose = $('#drawerClose');

  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle('is-open', open);
    scrim.classList.toggle('is-open', open);
    burger.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    document.body.classList.toggle('no-scroll', open);
  }

  if (burger) burger.addEventListener('click', () => setDrawer(!drawer.classList.contains('is-open')));
  if (scrim)  scrim.addEventListener('click', () => setDrawer(false));
  if (dClose) dClose.addEventListener('click', () => setDrawer(false));
  $$('#drawer nav a').forEach(a => a.addEventListener('click', () => setDrawer(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') setDrawer(false); });

  /* ---------------------------------------------------
     Apariciones al hacer scroll
     --------------------------------------------------- */
  const revealables = $$('[data-reveal]');

  if (!('IntersectionObserver' in window) || reduceMotion) {
    revealables.forEach(el => el.classList.add('is-in'));
  } else {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    revealables.forEach(el => io.observe(el));
  }

  /* ---------------------------------------------------
     Contadores animados
     --------------------------------------------------- */
  function animateCount(el) {
    const to       = parseFloat(el.dataset.to || '0');
    const decimals = parseInt(el.dataset.decimals || '0', 10);
    const suffix   = el.dataset.suffix || '';
    const group    = el.dataset.group === '1';
    const duration = 1800;
    const start    = performance.now();

    function format(n) {
      let s = n.toFixed(decimals);
      if (group) s = Number(s).toLocaleString('es-ES');
      return s + suffix;
    }

    if (reduceMotion) { el.textContent = format(to); return; }

    function step(now) {
      const t = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3);          // easeOutCubic
      el.textContent = format(to * eased);
      if (t < 1) requestAnimationFrame(step);
      else el.textContent = format(to);
    }
    requestAnimationFrame(step);
  }

  const counters = $$('.count');
  if (counters.length) {
    if (!('IntersectionObserver' in window)) {
      counters.forEach(animateCount);
    } else {
      const cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          animateCount(entry.target);
          cio.unobserve(entry.target);
        });
      }, { threshold: 0.5 });
      counters.forEach(el => cio.observe(el));
    }
  }

  /* ---------------------------------------------------
     Paralaje suave del hero
     --------------------------------------------------- */
  const parallax = $$('[data-parallax]');
  if (parallax.length && !reduceMotion) {
    let raf = null;
    window.addEventListener('scroll', function () {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        const y = window.scrollY;
        parallax.forEach(function (el) {
          const k = parseFloat(el.dataset.parallax) || 0;
          el.style.translate = '0 ' + (y * k).toFixed(1) + 'px';
        });
        raf = null;
      });
    }, { passive: true });
  }

  /* ---------------------------------------------------
     Marquesina: duplicamos el contenido para el bucle
     --------------------------------------------------- */
  const marquee = $('#marquee');
  if (marquee) marquee.innerHTML += marquee.innerHTML;

  /* ---------------------------------------------------
     Comparador antes / después
     --------------------------------------------------- */
  const compare = $('#compare');
  if (compare) {
    let dragging = false;

    function setPos(clientX) {
      const r = compare.getBoundingClientRect();
      const pct = Math.min(100, Math.max(0, ((clientX - r.left) / r.width) * 100));
      compare.style.setProperty('--pos', pct + '%');
      compare.setAttribute('aria-valuenow', Math.round(pct));
    }

    compare.addEventListener('pointerdown', function (e) {
      dragging = true;
      compare.setPointerCapture(e.pointerId);
      setPos(e.clientX);
    });
    compare.addEventListener('pointermove', function (e) { if (dragging) setPos(e.clientX); });
    ['pointerup', 'pointercancel'].forEach(function (ev) {
      compare.addEventListener(ev, function () { dragging = false; });
    });

    compare.addEventListener('keydown', function (e) {
      const cur = parseFloat(compare.getAttribute('aria-valuenow')) || 50;
      let next = cur;
      if (e.key === 'ArrowLeft')  next = Math.max(0, cur - 4);
      if (e.key === 'ArrowRight') next = Math.min(100, cur + 4);
      if (next === cur) return;
      e.preventDefault();
      compare.style.setProperty('--pos', next + '%');
      compare.setAttribute('aria-valuenow', next);
    });

    // Pequeño gesto de bienvenida la primera vez que entra en pantalla
    if (!reduceMotion && 'IntersectionObserver' in window) {
      const hint = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          hint.disconnect();
          const seq = [66, 34, 50];
          compare.classList.add('is-hinting');
          seq.forEach(function (v, i) {
            setTimeout(function () {
              compare.style.setProperty('--pos', v + '%');
              compare.setAttribute('aria-valuenow', v);
            }, 620 * i + 320);
          });
          setTimeout(function () { compare.classList.remove('is-hinting'); }, 620 * seq.length + 900);
        });
      }, { threshold: 0.4 });
      hint.observe(compare);
    }
  }

  /* ---------------------------------------------------
     Carrusel de opiniones
     --------------------------------------------------- */
  const slider = $('#slider');
  const track  = $('#track');
  if (slider && track) {
    const slides = $$('.slide', track);
    const dotsEl = $('#dots');
    let index = 0;
    let timer = null;

    const perView = () => (window.innerWidth >= 900 ? 2 : 1);
    const pages   = () => Math.max(1, slides.length - perView() + 1);

    function renderDots() {
      dotsEl.innerHTML = '';
      for (let i = 0; i < pages(); i++) {
        const b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('aria-label', 'Ir a la opinión ' + (i + 1));
        b.addEventListener('click', function () { go(i, true); });
        dotsEl.appendChild(b);
      }
    }

    function go(i, stop) {
      const n = pages();
      index = ((i % n) + n) % n;
      track.style.transform = 'translateX(-' + (index * (100 / perView())) + '%)';
      $$('button', dotsEl).forEach((d, k) => d.classList.toggle('is-active', k === index));
      if (stop) restart();
    }

    function restart() {
      if (timer) clearInterval(timer);
      if (reduceMotion) return;
      timer = setInterval(function () { go(index + 1); }, 6000);
    }

    $('#next').addEventListener('click', function () { go(index + 1, true); });
    $('#prev').addEventListener('click', function () { go(index - 1, true); });

    slider.addEventListener('mouseenter', function () { if (timer) clearInterval(timer); });
    slider.addEventListener('mouseleave', restart);

    // Arrastre táctil
    let x0 = null;
    track.addEventListener('pointerdown', function (e) { x0 = e.clientX; });
    track.addEventListener('pointerup', function (e) {
      if (x0 === null) return;
      const dx = e.clientX - x0;
      if (Math.abs(dx) > 45) go(index + (dx < 0 ? 1 : -1), true);
      x0 = null;
    });

    let rt = null;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () { renderDots(); go(0); }, 180);
    });

    renderDots();
    go(0);
    restart();
  }

  /* ---------------------------------------------------
     Acordeón de preguntas frecuentes
     --------------------------------------------------- */
  $$('.acc').forEach(function (acc) {
    const q = $('.acc__q', acc);
    q.addEventListener('click', function () {
      const open = acc.classList.contains('is-open');
      // Cerramos el resto para que solo quede uno abierto
      $$('.acc').forEach(function (other) {
        other.classList.remove('is-open');
        $('.acc__q', other).setAttribute('aria-expanded', 'false');
      });
      if (!open) {
        acc.classList.add('is-open');
        q.setAttribute('aria-expanded', 'true');
      }
    });
  });

  /* ---------------------------------------------------
     Navegación activa según la sección visible
     --------------------------------------------------- */
  const navLinks = $$('.nav__link[href^="#"]');
  const sections = navLinks
    .map(a => document.getElementById(a.getAttribute('href').slice(1)))
    .filter(Boolean);

  if (sections.length && 'IntersectionObserver' in window) {
    const sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (a) {
          a.classList.toggle('is-active', a.getAttribute('href') === '#' + entry.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(s => sio.observe(s));
  }

  /* ---------------------------------------------------
     Formulario de cita
     --------------------------------------------------- */
  const form = $('#form');
  if (form) {
    // Mantiene la etiqueta flotante del desplegable en su sitio
    const motivo = $('#motivo', form);
    motivo.addEventListener('change', function () {
      motivo.classList.toggle('has-value', !!motivo.value);
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      let ok = true;

      const checks = [
        ['#nombre',   v => v.trim().length > 1],
        ['#telefono', v => /^[+\d][\d\s.\-()]{7,}$/.test(v.trim())],
        ['#email',    v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim())]
      ];

      checks.forEach(function (pair) {
        const el    = $(pair[0], form);
        const field = el.closest('.field');
        const valid = pair[1](el.value);
        field.classList.toggle('is-error', !valid);
        if (!valid && ok) { el.focus(); ok = false; }
      });

      const rgpd = $('#rgpd', form);
      if (!rgpd.checked) {
        rgpd.closest('.check').style.color = '#d9534f';
        ok = false;
      } else {
        rgpd.closest('.check').style.color = '';
      }

      if (!ok) return;

      const ack = $('#formOk');
      ack.classList.add('is-visible');
      form.reset();
      motivo.classList.remove('has-value');
      setTimeout(function () { ack.classList.remove('is-visible'); }, 7000);
    });
  }

  /* ---------------------------------------------------
     Aviso de cookies
     --------------------------------------------------- */
  const cookies = $('#cookies');
  if (cookies) {
    let decided = false;
    try { decided = localStorage.getItem('rais-cookies') !== null; } catch (err) { decided = false; }

    if (!decided) setTimeout(function () { cookies.classList.add('is-visible'); }, 1400);

    function decide(value) {
      try { localStorage.setItem('rais-cookies', value); } catch (err) { /* modo privado */ }
      cookies.classList.remove('is-visible');
    }
    $('#cookiesOk').addEventListener('click', function () { decide('all'); });
    $('#cookiesNo').addEventListener('click', function () { decide('necessary'); });
  }
})();
