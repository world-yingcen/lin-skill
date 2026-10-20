/* 光研 Lumen Lab - shared effects only (no content is rendered from JS) */
(function () {
  'use strict';

  // mobile menu toggle
  var header = document.querySelector('[data-evo-shared="header"]');
  var toggle = document.querySelector('.nav-toggle');
  if (header && toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // product quantity +/-
  var qty = document.querySelector('[data-evo-field="qty"]');
  if (qty) {
    var box = qty.parentElement;
    var minus = box ? box.querySelector('.qty-minus') : null;
    var plus = box ? box.querySelector('.qty-plus') : null;
    var step = function (d) {
      var v = parseInt(qty.value, 10) || 1;
      qty.value = Math.max(parseInt(qty.min, 10) || 1, v + d);
    };
    if (minus) { minus.addEventListener('click', function () { step(-1); }); }
    if (plus) { plus.addEventListener('click', function () { step(1); }); }
  }

  // hero slider: slide count is read from the DOM, never hard-coded
  var track = document.querySelector('.hero-track');
  if (track) {
    var hero = track.parentElement;
    var prev = hero.querySelector('.hero-prev');
    var next = hero.querySelector('.hero-next');
    var go = function (dir) {
      var w = track.clientWidth;
      var atEnd = track.scrollLeft + w >= track.scrollWidth - 4;
      var atStart = track.scrollLeft <= 4;
      if (dir > 0 && atEnd) { track.scrollTo({ left: 0, behavior: 'smooth' }); }
      else if (dir < 0 && atStart) { track.scrollTo({ left: track.scrollWidth, behavior: 'smooth' }); }
      else { track.scrollBy({ left: dir * w, behavior: 'smooth' }); }
    };
    if (prev) { prev.addEventListener('click', function () { go(-1); }); }
    if (next) { next.addEventListener('click', function () { go(1); }); }

    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reduce && track.children.length > 1) {
      var timer = null;
      var start = function () { stop(); timer = setInterval(function () { go(1); }, 6000); };
      var stop = function () { if (timer) { clearInterval(timer); timer = null; } };
      hero.addEventListener('mouseenter', stop);
      hero.addEventListener('mouseleave', start);
      hero.addEventListener('focusin', stop);
      hero.addEventListener('focusout', start);
      start();
    }
  }

  // product image carousel. After import the system writes one .pd-slide per product image, so the slides are
  // counted from the DOM when the page is ready, never hard-coded. The buttons and dots are created here, outside
  // .pd-track (anything inside the gallery element would be taken as a slide). One image: no controls.
  var initGalleries = function () {
    var galleries = document.querySelectorAll('.pd-gallery');
    for (var g = 0; g < galleries.length; g++) {
      (function (gallery) {
        var track = gallery.querySelector('.pd-track');
        var slides = track ? track.children : [];
        if (slides.length < 2) { return; }
        var current = 0;
        var dots = [];
        var show = function (i) {
          current = (i + slides.length) % slides.length;
          track.style.transform = 'translateX(' + (-100 * current) + '%)';
          for (var d = 0; d < dots.length; d++) {
            dots[d].classList.toggle('is-current', d === current);
            dots[d].setAttribute('aria-current', d === current ? 'true' : 'false');
          }
        };
        var button = function (cls, label, text, onClick) {
          var b = document.createElement('button');
          b.type = 'button';
          b.className = cls;
          b.setAttribute('aria-label', label);
          b.textContent = text;
          b.addEventListener('click', onClick);
          return b;
        };
        gallery.appendChild(button('pd-nav pd-prev', '上一張', '‹', function () { show(current - 1); }));
        gallery.appendChild(button('pd-nav pd-next', '下一張', '›', function () { show(current + 1); }));
        var dotBox = document.createElement('div');
        dotBox.className = 'pd-dots';
        for (var n = 0; n < slides.length; n++) {
          (function (i) {
            var dot = button('pd-dot', '第 ' + (i + 1) + ' 張', '', function () { show(i); });
            dots.push(dot);
            dotBox.appendChild(dot);
          })(n);
        }
        gallery.appendChild(dotBox);
        show(0);
      })(galleries[g]);
    }
  };
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', initGalleries); }
  else { initGalleries(); }
})();
