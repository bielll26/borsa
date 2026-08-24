/* =====================================================================
   Clínica Dental RAIS — interacciones y animaciones
   ===================================================================== */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- año del pie ---------- */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- menú ---------- */
  var menuBtn = document.getElementById('menuBtn');
  var overlay = document.getElementById('navOverlay');
  var menuClose = document.getElementById('menuClose');

  function openMenu() {
    overlay.hidden = false;
    document.body.style.overflow = 'hidden';
    requestAnimationFrame(function () { overlay.classList.add('is-open'); });
    menuBtn.setAttribute('aria-expanded', 'true');
  }
  function closeMenu() {
    overlay.classList.remove('is-open');
    document.body.style.overflow = '';
    menuBtn.setAttribute('aria-expanded', 'false');
    window.setTimeout(function () { overlay.hidden = true; }, 450);
  }
  if (menuBtn && overlay) {
    Array.prototype.forEach.call(overlay.querySelectorAll('[data-i]'), function (el) {
      el.style.setProperty('--d', el.getAttribute('data-i'));
    });
    menuBtn.addEventListener('click', openMenu);
    menuClose.addEventListener('click', closeMenu);
    overlay.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') closeMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('is-open')) closeMenu();
    });
  }

  /* ---------- aparición al hacer scroll ---------- */
  var revealables = document.querySelectorAll('.reveal');
  Array.prototype.forEach.call(document.querySelectorAll('.cards, .team, .stats'), function (group) {
    Array.prototype.forEach.call(group.children, function (child, i) {
      child.style.setProperty('--i', i % 4);
    });
  });

  if ('IntersectionObserver' in window && !reduced) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    Array.prototype.forEach.call(revealables, function (el) { revealObserver.observe(el); });
  } else {
    Array.prototype.forEach.call(revealables, function (el) { el.classList.add('is-in'); });
  }

  /* ---------- hero: pase de imágenes ---------- */
  var slidesWrap = document.getElementById('heroSlides');
  if (slidesWrap) {
    var slides = slidesWrap.querySelectorAll('.hero__slide');
    var caption = document.getElementById('heroCaption');
    var current = 0;
    var timer = null;

    function go(index) {
      if (index === current) return;
      var next = slides[index];
      var text = next.getAttribute('data-caption');

      caption.classList.add('is-swapping');
      window.setTimeout(function () {
        caption.querySelector('h1').textContent = text;
        caption.classList.remove('is-swapping');
      }, 380);

      slides[current].classList.remove('is-active');
      next.classList.add('is-active');
      current = index;
    }
    function tick() { go((current + 1) % slides.length); }
    function restart() {
      window.clearInterval(timer);
      if (!reduced) timer = window.setInterval(tick, 5200);
    }
    restart();
  }

  /* ---------- contadores ---------- */
  var statsSection = document.getElementById('stats');
  if (statsSection) {
    var counters = statsSection.querySelectorAll('.stat__num');
    var started = false;

    function runCounters() {
      if (started) return;
      started = true;
      Array.prototype.forEach.call(counters, function (el) {
        var target = parseInt(el.getAttribute('data-count'), 10) || 0;
        var suffix = el.getAttribute('data-suffix') || '';
        var duration = 2200;
        var startedAt = null;

        if (reduced) { el.textContent = format(target) + suffix; return; }

        function step(now) {
          if (!startedAt) startedAt = now;
          var p = Math.min((now - startedAt) / duration, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = format(Math.round(target * eased)) + suffix;
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }
    function format(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }

    if ('IntersectionObserver' in window) {
      var statObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) { if (entry.isIntersecting) runCounters(); });
      }, { threshold: 0.35 });
      statObserver.observe(statsSection);
    } else {
      runCounters();
    }
  }

  /* ---------- antes / después ---------- */
  var ba = document.getElementById('ba');
  if (ba) {
    var before = document.getElementById('baBefore');
    var handle = document.getElementById('baHandle');
    var range = document.getElementById('baRange');
    var dragging = false;

    function setPos(pct) {
      pct = Math.max(0, Math.min(100, pct));
      before.style.clipPath = 'inset(0 ' + (100 - pct) + '% 0 0)';
      handle.style.left = pct + '%';
      ba.style.setProperty('--pos', pct + '%');
      ba.querySelector('.ba__tag--before').style.opacity = pct < 14 ? 0 : 1;
      ba.querySelector('.ba__tag--after').style.opacity = pct > 86 ? 0 : 1;
      range.value = pct;
      lineEl.style.left = pct + '%';
    }

    // línea divisoria del comparador
    var lineEl = document.createElement('span');
    lineEl.style.cssText = 'position:absolute;top:0;bottom:0;width:3px;background:#fff;z-index:3;transform:translateX(-50%);left:50%';
    ba.appendChild(lineEl);
    ba.style.setProperty('--pos', '50%');

    function fromEvent(e) {
      var rect = ba.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
      setPos((x / rect.width) * 100);
    }
    ba.addEventListener('mousedown', function (e) { e.preventDefault(); dragging = true; document.body.classList.add('is-dragging'); fromEvent(e); });
    window.addEventListener('mousemove', function (e) { if (dragging) fromEvent(e); });
    window.addEventListener('mouseup', function () { dragging = false; document.body.classList.remove('is-dragging'); });
    ba.addEventListener('touchstart', function (e) { dragging = true; fromEvent(e); }, { passive: true });
    ba.addEventListener('touchmove', function (e) { if (dragging) fromEvent(e); }, { passive: true });
    ba.addEventListener('touchend', function () { dragging = false; });
    range.addEventListener('input', function () { setPos(parseFloat(range.value)); });
    handle.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') setPos(parseFloat(range.value) - 4);
      if (e.key === 'ArrowRight') setPos(parseFloat(range.value) + 4);
    });
    setPos(50);
  }

  /* ---------- carrusel de opiniones ---------- */
  var track = document.getElementById('reviewsTrack');
  if (track) {
    var dots = document.getElementById('reviewsDots');
    var cards = track.querySelectorAll('.review');
    var index = 0;
    var auto = null;

    Array.prototype.forEach.call(cards, function (card, i) {
      var dot = document.createElement('button');
      dot.type = 'button';
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-label', 'Opinión ' + (i + 1));
      if (i === 0) dot.classList.add('is-active');
      dot.addEventListener('click', function () { scrollTo(i); resetAuto(); });
      dots.appendChild(dot);
    });

    function scrollTo(i) {
      index = i;
      var card = cards[i];
      track.scrollTo({ left: card.offsetLeft - track.offsetLeft, behavior: reduced ? 'auto' : 'smooth' });
      syncDots();
    }
    function syncDots() {
      Array.prototype.forEach.call(dots.children, function (dot, i) {
        dot.classList.toggle('is-active', i === index);
      });
    }
    track.addEventListener('scroll', function () {
      var closest = 0;
      var min = Infinity;
      Array.prototype.forEach.call(cards, function (card, i) {
        var d = Math.abs(card.offsetLeft - track.offsetLeft - track.scrollLeft);
        if (d < min) { min = d; closest = i; }
      });
      if (closest !== index) { index = closest; syncDots(); }
    }, { passive: true });

    function resetAuto() {
      window.clearInterval(auto);
      if (!reduced) auto = window.setInterval(function () { scrollTo((index + 1) % cards.length); }, 6000);
    }
    resetAuto();
    track.addEventListener('pointerdown', function () { window.clearInterval(auto); });
  }

  /* ---------- acordeón de preguntas frecuentes ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('.faq__item'), function (item) {
    var btn = item.querySelector('.faq__q');
    var panel = item.querySelector('.faq__a');
    btn.addEventListener('click', function () {
      var open = item.classList.contains('is-open');
      Array.prototype.forEach.call(document.querySelectorAll('.faq__item.is-open'), function (other) {
        if (other !== item) {
          other.classList.remove('is-open');
          other.querySelector('.faq__a').style.height = '0px';
          other.querySelector('.faq__q').setAttribute('aria-expanded', 'false');
        }
      });
      if (open) {
        panel.style.height = panel.scrollHeight + 'px';
        requestAnimationFrame(function () { panel.style.height = '0px'; });
        item.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      } else {
        item.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
        panel.style.height = panel.scrollHeight + 'px';
        window.setTimeout(function () {
          if (item.classList.contains('is-open')) panel.style.height = 'auto';
        }, 460);
      }
    });
  });

  /* ---------- botón de cookies (demostrativo) ---------- */
  var cookieBtn = document.getElementById('cookieBtn');
  if (cookieBtn) {
    cookieBtn.addEventListener('click', function () {
      window.alert('Preferencias de cookies');
    });
  }
})();
