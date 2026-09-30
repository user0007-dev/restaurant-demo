/* ==========================================================================
   SPICE ROUTE — SITE SCRIPT
   --------------------------------------------------------------------------
   Vanilla JavaScript, no dependencies, no build step.
   Every feature below is opt-in: it only runs if the matching markup exists
   on the page, so this single file can be used on every page of the site.

     01. Helpers
     02. Business data hydration      (js/site-data.js)
     03. Header: stuck state
     04. Mobile navigation
     05. Smooth scrolling + scroll spy
     06. Scroll-to-top button
     07. Reveal on scroll
     08. Menu page: filter, search, counters
     09. Gallery page: filter + lightbox
     10. Contact page: tabs
     11. Form validation + demo submit
     12. Live open/closed status
     13. Toast
     14. Boot
   ========================================================================== */
(function () {
  'use strict';

  /* ======================================================================
     01. HELPERS
     ====================================================================== */
  const $  = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.prototype.slice.call((ctx || document).querySelectorAll(sel));

  const prefersReducedMotion = window.matchMedia
    ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
    : false;

  /** Adds a listener and returns an unsubscribe function (if supported). */
  function on(el, evt, handler, opts) {
    el.addEventListener(evt, handler, opts);
    return function () { el.removeEventListener(evt, handler, opts); };
  }

  /** Traps Tab focus inside a container. Returns a release function. */
  function trapFocus(container) {
    const selector =
      'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), ' +
      'select:not([disabled]), textarea:not([disabled]), details > summary, [tabindex]:not([tabindex="-1"])';

    function focusables() {
      return $$(selector, container).filter(function (el) {
        return el.offsetWidth > 0 || el.offsetHeight > 0 || el === document.activeElement;
      });
    }

    function onKeydown(e) {
      if (e.key !== 'Tab') return;
      const items = focusables();
      if (!items.length) return;
      const first = items[0];
      const last = items[items.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }

    document.addEventListener('keydown', onKeydown);
    return function () { document.removeEventListener('keydown', onKeydown); };
  }

  /** Scrolls an element into view, but never lets a missing/unsupported
      implementation break the feature that called it. */
  function safeScrollIntoView(el, block) {
    try {
      if (el && typeof el.scrollIntoView === 'function') {
        el.scrollIntoView({ behavior: prefersReducedMotion ? 'auto' : 'smooth', block: block || 'center' });
      }
    } catch (e) { /* older engines reject the options object - ignore */ }
  }

  const FOCUSABLE =
    'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled])';

  function lockScroll(locked) {
    document.body.classList.toggle('is-locked', !!locked);
  }

  /* ======================================================================
     02. BUSINESS DATA HYDRATION
     ----------------------------------------------------------------------
     Reads window.SITE (js/site-data.js) and writes the values into any
     element carrying  data-site-field="<key>".  Static HTML acts as the
     fallback, so the site is fully readable with JavaScript disabled.
     ====================================================================== */
  function hydrateSiteData() {
    const SITE = window.SITE;
    if (!SITE) return;

    const hoursOneLine = SITE.hours
      .filter(function (h) { return !h.closed; })
      .map(function (h) { return h.days + ': ' + h.open + ' – ' + h.close; })
      .join(' · ');

    const map = {
      name: SITE.name,
      tagline: SITE.tagline,
      shortDescription: SITE.shortDescription,
      phone: SITE.phoneDisplay,
      phoneHref: 'tel:' + SITE.phoneDial,
      whatsapp: SITE.phoneDisplay,
      whatsappHref:
        'https://wa.me/' + SITE.whatsappNumber + '?text=' + encodeURIComponent(SITE.whatsappMessage),
      email: SITE.email,
      emailHref: 'mailto:' + SITE.email,
      address: SITE.address.oneLine,
      addressHref:
        'https://www.google.com/maps/search/?api=1&query=' +
        encodeURIComponent(SITE.address.oneLine),
      mapHref: SITE.mapUrl,
      hours: hoursOneLine,
      copyright: SITE.copyright
    };

    $$('[data-site-field]').forEach(function (el) {
      const value = map[el.getAttribute('data-site-field')];
      if (value === undefined || value === null || value === '') return;

      if (el.tagName === 'A') {
        el.setAttribute('href', value);
        // keep the visible label from stale markup
        if (el.hasAttribute('data-site-text')) el.textContent = value;
      } else if (el.tagName === 'TIME') {
        el.setAttribute('datetime', value);
        el.textContent = value;
      } else {
        el.textContent = value;
      }
    });

    // Social links
    $$('[data-social]').forEach(function (el) {
      const url = SITE.social && SITE.social[el.getAttribute('data-social')];
      if (!url) { el.hidden = true; return; }
      el.setAttribute('href', url);
      el.setAttribute('rel', 'noopener noreferrer');
    });
  }

  /* ======================================================================
     03. HEADER — STUCK STATE
     ====================================================================== */
  function initHeader() {
    const header = $('.site-header');
    if (!header) return;

    const update = function () {
      header.classList.toggle('is-stuck', window.scrollY > 24);
    };

    update();
    on(window, 'scroll', update, { passive: true });
  }

  /* ======================================================================
     04. MOBILE NAVIGATION
     ====================================================================== */
  function initMobileNav() {
    const toggle = $('.nav-toggle');
    const nav = $('#site-nav');
    if (!toggle || !nav) return;

    const openers = $$('[data-nav-open]', document.body);
    const closers = $$('[data-nav-close]', nav);

    let releaseFocus = null;

    function openNav() {
      nav.classList.add('is-open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.querySelector('.nav-toggle__text').textContent = 'Close';
      lockScroll(true);
      releaseFocus = trapFocus(nav);
      const first = nav.querySelector(FOCUSABLE);
      if (first) first.focus();
      document.addEventListener('keydown', onEsc);
    }

    function closeNav(returnFocus) {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.querySelector('.nav-toggle__text').textContent = 'Menu';
      lockScroll(false);
      document.removeEventListener('keydown', onEsc);
      if (releaseFocus) { releaseFocus(); releaseFocus = null; }
      if (returnFocus) toggle.focus();
    }

    function onEsc(e) {
      if (e.key === 'Escape') closeNav(true);
    }

    on(toggle, 'click', function () {
      if (toggle.getAttribute('aria-expanded') === 'true') closeNav(true);
      else openNav();
    });

    openers.forEach(function (btn) {
      on(btn, 'click', function () { openNav(); });
    });

    closers.forEach(function (btn) {
      on(btn, 'click', function () { closeNav(false); });
    });

    // Close when a menu link is used, and when resizing back to desktop
    $$('.site-nav__link', nav).forEach(function (link) {
      on(link, 'click', function () { closeNav(false); });
    });

    let resizeTimer;
    on(window, 'resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        if (window.innerWidth >= 1000 && nav.classList.contains('is-open')) {
          closeNav(false);
        }
      }, 150);
    });
  }

  /* ======================================================================
     05. SMOOTH SCROLLING + SCROLL SPY
     ====================================================================== */
  function initSmoothScroll() {
    on(document, 'click', function (e) {
      const link = e.target.closest('a[href^="#"]');
      if (!link) return;

      const id = link.getAttribute('href');
      if (!id || id === '#' || link.hasAttribute('data-no-scroll')) return;

      const target = document.getElementById(id.slice(1));
      if (!target) return;

      e.preventDefault();
      const header = $('.site-header');
      const offset = (header ? header.offsetHeight : 0) + 12;

      window.scrollTo({
        top: target.getBoundingClientRect().top + window.scrollY - offset,
        behavior: prefersReducedMotion ? 'auto' : 'smooth'
      });

      // Move keyboard focus for screen-reader users
      target.setAttribute('tabindex', '-1');
      target.focus({ preventScroll: true });
      if (history.replaceState) history.replaceState(null, '', id);
    });
  }

  function initScrollSpy() {
    const sections = $$('[data-spy]');
    const links = $$('.site-nav__link[href^="#"]');
    if (!sections.length || !links.length) return;

    const byId = {};
    links.forEach(function (l) { byId[l.getAttribute('href').slice(1)] = l; });

    function update() {
      const line = window.scrollY + (window.innerHeight * 0.3);
      let currentId = null;

      sections.forEach(function (section) {
        if (section.offsetTop <= line) currentId = section.id;
      });

      links.forEach(function (l) { l.classList.remove('is-current'); });
      if (currentId && byId[currentId]) byId[currentId].classList.add('is-current');
    }

    update();
    on(window, 'scroll', update, { passive: true });
  }

  /* ======================================================================
     06. SCROLL-TO-TOP BUTTON
     ====================================================================== */
  function initScrollTop() {
    const btn = $('.fab--top');
    if (!btn) return;

    const update = function () {
      btn.classList.toggle('is-visible', window.scrollY > 520);
    };

    update();
    on(window, 'scroll', update, { passive: true });

    on(btn, 'click', function () {
      window.scrollTo({ top: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
      // send focus somewhere sensible
      const first = $('.skip-link') || $('body');
      if (first && first.focus) first.focus({ preventScroll: true });
    });
  }

  /* ======================================================================
     07. REVEAL ON SCROLL
     ====================================================================== */
  function initReveal() {
    const items = $$('.reveal');
    if (!items.length) return;

    if (prefersReducedMotion || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }

    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    items.forEach(function (el) { io.observe(el); });
  }

  /* ======================================================================
     08. MENU PAGE — FILTER, SEARCH, COUNTERS
     ====================================================================== */
  function initMenu() {
    const root = $('[data-menu]');
    if (!root) return;

    const items = $$('.menu-item', root);
    const categories = $$('.menu-category', root);
    const chips = $$('.filter-chip');
    const searchInput = $('#menu-search');
    const searchField = searchInput ? searchInput.closest('.search-field') : null;
    const clearBtn = $('.search-field__clear', searchField || document);
    const status = $('.menu-status');
    const empty = $('.empty-state');
    const vegToggle = $('#veg-only');

    let activeCategory = 'all';

    function matches(item, query) {
      if (activeCategory !== 'all' && item.getAttribute('data-category') !== activeCategory) {
        return false;
      }
      if (vegToggle && vegToggle.checked && item.getAttribute('data-veg') !== 'true') {
        return false;
      }
      if (!query) return true;

      const haystack = (item.getAttribute('data-search') || item.textContent || '')
        .toLowerCase()
        .replace(/\s+/g, ' ');
      return query.split(/\s+/).every(function (word) {
        return haystack.indexOf(word) !== -1;
      });
    }

    function apply() {
      const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
      let shown = 0;

      items.forEach(function (item) {
        const ok = matches(item, query);
        item.hidden = !ok;
        if (ok) shown += 1;
      });

      // Hide a whole category when nothing inside it is visible
      categories.forEach(function (cat) {
        const any = $$('.menu-item', cat).some(function (i) { return !i.hidden; });
        cat.hidden = !any;
      });

      // Update the per-category counters
      $$('[data-count-for]', root).forEach(function (el) {
        const id = el.getAttribute('data-count-for');
        const cat = document.getElementById(id);
        if (!cat) return;
        const n = $$('.menu-item', cat).filter(function (i) { return !i.hidden; }).length;
        el.textContent = n + (n === 1 ? ' dish' : ' dishes');
      });

      if (searchField) searchField.classList.toggle('has-value', !!searchInput.value);
      if (empty) empty.classList.toggle('is-visible', shown === 0);

      if (status) {
        const parts = [];
        const catLabel = activeCategory === 'all'
          ? 'the full menu'
          : (chips.filter(function (c) { return c.getAttribute('data-filter') === activeCategory; })[0] || {}).textContent;
        parts.push(shown + (shown === 1 ? ' dish' : ' dishes') + ' in ' + (catLabel || 'the full menu'));
        if (query) parts.push('matching “' + searchInput.value.trim() + '”');
        if (vegToggle && vegToggle.checked) parts.push('· vegetarian only');
        status.textContent = parts.join(' ');
      }
    }

    chips.forEach(function (chip) {
      on(chip, 'click', function () {
        activeCategory = chip.getAttribute('data-filter');
        chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
        apply();
      });
    });

    if (searchInput) {
      on(searchInput, 'input', apply);
      on(searchInput, 'keydown', function (e) {
        if (e.key === 'Escape' && searchInput.value) {
          searchInput.value = '';
          apply();
        }
      });
    }

    if (clearBtn) {
      on(clearBtn, 'click', function () {
        if (!searchInput) return;
        searchInput.value = '';
        searchInput.focus();
        apply();
      });
    }

    if (vegToggle) on(vegToggle, 'change', apply);

    // Allow ?filter=biryani in the URL for sharing a filtered view
    const params = new URLSearchParams(window.location.search);
    const preset = params.get('filter');
    if (preset) {
      const match = chips.filter(function (c) { return c.getAttribute('data-filter') === preset; })[0];
      if (match) match.click();
    }

    apply();
  }

  /* ======================================================================
     09. GALLERY PAGE — FILTER + LIGHTBOX
     ====================================================================== */
  function initGalleryFilter() {
    const grid = $('[data-gallery]');
    if (!grid) return;

    const tiles = $$('.gallery-item', grid);
    const chips = $$('.gallery-filter');
    const empty = $('.gallery-empty');
    const count = $('.gallery-count');

    function apply(filter) {
      let shown = 0;
      tiles.forEach(function (tile) {
        const ok = filter === 'all' || tile.getAttribute('data-category') === filter;
        tile.hidden = !ok;
        if (ok) shown += 1;
      });
      if (empty) empty.classList.toggle('is-visible', shown === 0);
      if (count) count.textContent = shown + (shown === 1 ? ' photograph' : ' photographs');
    }

    chips.forEach(function (chip) {
      on(chip, 'click', function () {
        chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
        apply(chip.getAttribute('data-filter'));
      });
    });

    apply('all');
  }

  function initLightbox() {
    const lightbox = $('.lightbox');
    if (!lightbox) return;

    const triggers = $$('[data-lightbox]');
    const img = $('[data-lightbox-image]', lightbox);
    const titleEl = $('[data-lightbox-title]', lightbox);
    const metaEl = $('[data-lightbox-meta]', lightbox);
    const counterEl = $('[data-lightbox-counter]', lightbox);
    const closeBtn = $('[data-lightbox-close]', lightbox);
    const prevBtn = $('[data-lightbox-prev]', lightbox);
    const nextBtn = $('[data-lightbox-next]', lightbox);

    let list = [];
    let index = 0;
    let lastFocus = null;
    let releaseFocus = null;

    function visibleItems() {
      // `hidden` is what the category filter toggles. Avoid offsetParent here:
      // it is null for anything inside a positioned/fixed ancestor.
      return triggers.filter(function (t) { return !t.hidden; });
    }

    function render() {
      const trigger = list[index];
      if (!trigger || !img) return;

      const full = trigger.getAttribute('data-lightbox');
      const thumb = trigger.querySelector('img');

      img.setAttribute('src', full);
      img.setAttribute('alt', trigger.getAttribute('data-caption') || (thumb ? thumb.alt : ''));
      // size the box before the image paints, to avoid layout jump
      img.style.aspectRatio = trigger.getAttribute('data-ratio') || '';

      if (titleEl) titleEl.textContent = trigger.getAttribute('data-caption') || '';
      if (metaEl) metaEl.textContent = trigger.getAttribute('data-category-label') || '';
      if (counterEl) counterEl.textContent = index + 1 + ' / ' + list.length;
    }

    function open(trigger) {
      list = visibleItems();
      index = Math.max(0, list.indexOf(trigger));
      lastFocus = document.activeElement;

      render();
      lightbox.classList.add('is-open');
      lockScroll(true);
      document.addEventListener('keydown', onKey);
      releaseFocus = trapFocus(lightbox);
      if (closeBtn) closeBtn.focus();
    }

    function close() {
      lightbox.classList.remove('is-open');
      lockScroll(false);
      document.removeEventListener('keydown', onKey);
      if (releaseFocus) { releaseFocus(); releaseFocus = null; }
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    function step(delta) {
      if (!list.length) return;
      index = (index + delta + list.length) % list.length;
      render();
    }

    function onKey(e) {
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') step(1);
      else if (e.key === 'ArrowLeft') step(-1);
      else if (e.key === 'Tab' && e.shiftKey) {
        // let focus stay inside the dialog
        e.preventDefault();
        if (nextBtn) nextBtn.focus();
      }
    }

    triggers.forEach(function (trigger) {
      on(trigger, 'click', function (e) { e.preventDefault(); open(trigger); });
      on(trigger, 'keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(trigger); }
      });
    });

    if (closeBtn) on(closeBtn, 'click', close);
    if (prevBtn) on(prevBtn, 'click', function () { step(-1); });
    if (nextBtn) on(nextBtn, 'click', function () { step(1); });

    on(lightbox, 'click', function (e) {
      // close when clicking the dimmed backdrop (but not the image itself)
      if (e.target === lightbox || e.target.classList.contains('lightbox__stage')) close();
    });

    // swipe on touch devices
    let touchX = null;
    on(lightbox, 'touchstart', function (e) { touchX = e.changedTouches[0].clientX; }, { passive: true });
    on(lightbox, 'touchend', function (e) {
      if (touchX === null) return;
      const delta = e.changedTouches[0].clientX - touchX;
      if (Math.abs(delta) > 55) step(delta < 0 ? 1 : -1);
      touchX = null;
    }, { passive: true });
  }

  /* ======================================================================
     10. CONTACT PAGE — TABS
     ====================================================================== */
  function initTabs() {
    const tablist = $('[role="tablist"]');
    if (!tablist) return;

    const tabs = $$('[role="tab"]', tablist);
    const panels = $$('[role="tabpanel"]');
    if (tabs.length < 2) return;

    function select(tab, setFocus) {
      tabs.forEach(function (t) {
        const active = t === tab;
        t.setAttribute('aria-selected', String(active));
        t.setAttribute('tabindex', active ? '0' : '-1');
      });
      panels.forEach(function (p) {
        p.hidden = p.id !== tab.getAttribute('aria-controls');
      });
      if (setFocus) tab.focus();
    }

    tabs.forEach(function (tab, i) {
      on(tab, 'click', function () { select(tab, false); });

      on(tab, 'keydown', function (e) {
        let next = null;
        if (e.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
        else if (e.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
        else if (e.key === 'Home') next = tabs[0];
        else if (e.key === 'End') next = tabs[tabs.length - 1];
        if (next) { e.preventDefault(); select(next, true); }
      });
    });

    // open a tab from a link like ?tab=book
    const preset = new URLSearchParams(window.location.search).get('tab');
    if (preset) {
      const match = tabs.filter(function (t) { return t.getAttribute('data-tab') === preset; })[0];
      if (match) select(match, false);
    }
  }

  /* ======================================================================
     11. FORM VALIDATION + DEMO SUBMIT
     ----------------------------------------------------------------------
     There is no back end on this demo, so a valid form composes a message
     and hands the visitor to WhatsApp / mail — which is also what a real
     restaurant would do. Swap `handleSubmit` for a fetch() call when a
     back end is added.
     ====================================================================== */
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;
  const PHONE_RE = /^[+\d][\d\s()-]{6,19}$/;

  const MESSAGES = {
    required: 'Please fill in this field.',
    email: 'Please enter a valid email address, e.g. name@example.com',
    phone: 'Please enter a valid phone number, e.g. +91 98765 43210',
    name: 'Please enter your name (at least 2 characters).',
    guests: 'Please choose a number of guests.',
    date: 'Please choose a date.',
    datePast: 'Please choose a date that is not in the past.',
    time: 'Please choose a time.',
    message: 'Please add a short message (at least 10 characters).',
    consent: 'Please confirm before submitting.',
    emailOptional: 'Please enter a valid email address, or leave this field empty.'
  };

  function fieldWrap(control) {
    return control.closest('.field') || control.closest('.checkbox') || control.parentElement;
  }

  function errorNode(control) {
    const wrap = fieldWrap(control);
    return wrap ? wrap.querySelector('.field__error') : null;
  }

  function setError(control, message) {
    const wrap = fieldWrap(control);
    const error = errorNode(control);
    if (wrap) wrap.classList.toggle('has-error', !!message);
    if (error) error.textContent = message || '';

    if (message) {
      control.setAttribute('aria-invalid', 'true');
      const id = control.id;
      if (id) {
        let describedBy = control.getAttribute('aria-describedby') || '';
        if (describedBy.split(/\s+/).indexOf(error.id) === -1) {
          describedBy = (describedBy + ' ' + error.id).trim();
          control.setAttribute('aria-describedby', describedBy);
        }
      }
    } else {
      control.removeAttribute('aria-invalid');
    }
  }

  function validateControl(control) {
    const value = (control.value || '').trim();
    const name = control.getAttribute('name');
    let message = '';

    if (control.type === 'checkbox') {
      if (control.hasAttribute('required') && !control.checked) message = MESSAGES.consent;
    } else if (control.hasAttribute('required') && !value) {
      message = MESSAGES.required;
    } else if (!value) {
      message = ''; // optional and empty is fine
    } else if (control.type === 'email' || control.dataset.validate === 'email') {
      if (!EMAIL_RE.test(value)) message = control.hasAttribute('required') ? MESSAGES.email : MESSAGES.emailOptional;
    } else if (control.type === 'tel' || control.dataset.validate === 'phone') {
      if (!PHONE_RE.test(value)) message = MESSAGES.phone;
    } else if (name === 'name' && value.length < 2) {
      message = MESSAGES.name;
    } else if (name === 'message' && value.length < 10) {
      message = MESSAGES.message;
    } else if (control.type === 'date') {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const picked = new Date(value + 'T00:00:00');
      if (isNaN(picked.getTime())) message = MESSAGES.date;
      else if (picked < today) message = MESSAGES.datePast;
    } else if (name === 'guests' && (!value || Number(value) < 1)) {
      message = MESSAGES.guests;
    }

    setError(control, message);
    return !message;
  }

  function validateForm(form) {
    const controls = $$('[data-validate] input, [data-validate] select, [data-validate] textarea, input[data-validate], select[data-validate], textarea[data-validate]', form)
      .concat($$('input, select, textarea', form))
      .filter(function (c, i, arr) {
        return c.type !== 'hidden' && c.name && arr.indexOf(c) === i;
      });

    let firstInvalid = null;

    controls.forEach(function (control) {
      // never validate fields inside a hidden tab panel
      const panel = control.closest('[role="tabpanel"]');
      if (panel && panel.hidden) return;

      if (!validateControl(control) && !firstInvalid) firstInvalid = control;
    });

    if (firstInvalid) {
      firstInvalid.focus();
      safeScrollIntoView(firstInvalid, 'center');
    }

    return !firstInvalid;
  }

  function fieldLabel(form, name) {
    const control = form.querySelector('[name="' + name + '"]');
    if (!control) return '';
    const wrapper = control.closest('.field');
    const label = wrapper && wrapper.querySelector('.field__label');
    if (!label) return '';
    return label.textContent.replace('*', '').trim();
  }

  function handleSubmit(form) {
    const data = new FormData(form);
    const dataSite = window.SITE || {};
    const isBooking = form.hasAttribute('data-booking');

    const name = (data.get('name') || '').toString().trim();
    const email = (data.get('email') || '').toString().trim();
    const phone = (data.get('phone') || '').toString().trim();
    const message = (data.get('message') || '').toString().trim();

    let text;
    if (isBooking) {
      const d = (data.get('date') || '');
      const formatted = d
        ? new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
        : '';
      text =
        'Hello ' + (dataSite.name || 'Spice Route') + '! I would like to book a table.\n\n' +
        'Name: ' + name + '\n' +
        'Phone: ' + phone + '\n' +
        (email ? 'Email: ' + email + '\n' : '') +
        'Date: ' + formatted + '\n' +
        'Time: ' + (data.get('time') || '') + '\n' +
        'Guests: ' + (data.get('guests') || '') + '\n' +
        (data.get('occasion') ? 'Occasion: ' + data.get('occasion') + '\n' : '') +
        (message ? 'Notes: ' + message + '\n' : '');
    } else {
      text =
        'Hello ' + (dataSite.name || 'Spice Route') + '! I have an enquiry.\n\n' +
        'Name: ' + name + '\n' +
        'Phone: ' + phone + '\n' +
        (email ? 'Email: ' + email + '\n' : '') +
        'Subject: ' + (data.get('subject') || 'General enquiry') + '\n\n' +
        message;
    }

    // Show the on-page confirmation
    const success = form.parentElement.querySelector('.form-success');
    if (success) {
      const summary = success.querySelector('.form-success__summary');
      if (summary) {
        const rows = [];
        ['name', 'phone', 'email'].forEach(function (k) {
          const v = (data.get(k) || '').toString().trim();
          if (v) rows.push('<div><dt>' + fieldLabel(form, k) + '</dt><dd>' + escapeHtml(v) + '</dd></div>');
        });
        if (isBooking) {
          ['date', 'time', 'guests'].forEach(function (k) {
            const v = (data.get(k) || '').toString().trim();
            if (v) rows.push('<div><dt>' + fieldLabel(form, k) + '</dt><dd>' + escapeHtml(v) + '</dd></div>');
          });
        }
        summary.innerHTML = rows.join('');
      }
      form.hidden = true;
      success.classList.add('is-visible');
      success.setAttribute('tabindex', '-1');
      try { success.focus({ preventScroll: true }); } catch (e) { success.focus(); }
      safeScrollIntoView(success, 'center');
    }

    // Hand off to WhatsApp (the real booking channel on this demo)
    const waBtn = success && success.querySelector('[data-whatsapp-send]');
    if (waBtn) {
      const number = dataSite.whatsappNumber || '';
      waBtn.setAttribute(
        'href',
        'https://wa.me/' + number + '?text=' + encodeURIComponent(text)
      );
    }

    // Offer a mailto fallback
    const mailBtn = success && success.querySelector('[data-mail-send]');
    if (mailBtn) {
      const subject = isBooking ? 'Table booking request' : 'Website enquiry';
      mailBtn.setAttribute(
        'href',
        'mailto:' + (dataSite.email || '') + '?subject=' + encodeURIComponent(subject + ' — ' + name) +
        '&body=' + encodeURIComponent(text)
      );
    }

    if (form.hasAttribute('data-auto-submit') && waBtn) {
      window.open(waBtn.getAttribute('href'), '_blank', 'noopener');
    }

    showToast('Thanks ' + (name.split(' ')[0] || '') + ' — your details are ready to send.');
    form.reset();
    $$('.field', form).forEach(function (f) { f.classList.remove('has-error'); });
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function initForms() {
    const forms = $$('.js-validate');
    if (!forms.length) return;

    // Booking form: block past dates and cap the party size
    const SITE = window.SITE || {};
    const dateInput = $('#booking-date');
    if (dateInput) {
      const today = new Date();
      const pad = function (n) { return String(n).padStart(2, '0'); };
      const iso = function (d) {
        return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
      };
      const min = new Date(today.getTime() + (SITE.bookingLeadTimeDays || 0) * 86400000);
      dateInput.setAttribute('min', iso(min));

      // Sensible default: tonight, then keep it in step with the date field
      if (!dateInput.value) dateInput.value = iso(min);
    }

    const guestsSelect = $('#booking-guests');
    if (guestsSelect && SITE.maxGuestsPerBooking) {
      guestsSelect.setAttribute('max', String(SITE.maxGuestsPerBooking));
    }

    forms.forEach(function (form) {
      // Validate on blur once the field has been touched
      $$('input, select, textarea', form).forEach(function (control) {
        if (control.type === 'hidden') return;
        let touched = false;

        on(control, 'blur', function () {
          touched = true;
          validateControl(control);
        });

        on(control, 'input', function () {
          if (touched) validateControl(control);
        });

        on(control, 'change', function () {
          if (touched) validateControl(control);
        });
      });

      on(form, 'submit', function (e) {
        e.preventDefault();
        if (validateForm(form)) handleSubmit(form);
      });

      const resetBtn = form.querySelector('[data-reset]');
      if (resetBtn) {
        on(resetBtn, 'click', function (e) {
          e.preventDefault();
          form.reset();
          $$('.field', form).forEach(function (f) { f.classList.remove('has-error'); });
          const first = form.querySelector('input, select, textarea');
          if (first) first.focus();
        });
      }
    });
  }

  /* ======================================================================
     12. LIVE OPEN / CLOSED STATUS
     ----------------------------------------------------------------------
     Turns the static "Loading hours…" placeholders into a real-time
     open/closed pill, using the hours in js/site-data.js. The markup is a
     sensible fallback, so the site is still usable without JavaScript.
     ====================================================================== */
  function parseTime(str) {
    // "12:00 pm" / "10:30 pm" -> minutes since midnight
    const m = /(\d{1,2}):(\d{2})\s*(am|pm)/i.exec(String(str).trim());
    if (!m) return null;
    let h = parseInt(m[1], 10) % 12;
    if (/pm/i.test(m[3])) h += 12;
    return h * 60 + parseInt(m[2], 10);
  }

  /** Maps JS getDay() (0=Sun) onto the ranges listed in SITE.hours. */
  function dayRangeIndex(day) {
    if (day === 0) return 2;  // Sunday
    if (day === 5 || day === 6) return 1; // Friday, Saturday
    return 0;                 // Monday – Thursday
  }

  function initOpenStatus() {
    const SITE = window.SITE;
    if (!SITE || !SITE.hours || !SITE.hours.length) return;

    function update() {
      const now = new Date();
      const minutes = now.getHours() * 60 + now.getMinutes();
      const row = SITE.hours[dayRangeIndex(now.getDay())];

      let open = false;
      let todayLabel = '';
      if (row && !row.closed) {
        const o = parseTime(row.open);
        const c = parseTime(row.close);
        if (o !== null && c !== null) {
          open = minutes >= o && minutes < c;
          // closed overnight? handle close < open
          if (c <= o) open = minutes >= o || minutes < c;
        }
        todayLabel = row.days + ': ' + row.open + ' – ' + row.close;
      }

      $$('[data-open-status]').forEach(function (el) {
        el.classList.toggle('is-closed', !open);
        const label = el.querySelector('span:last-child');
        if (label) label.textContent = open ? 'Open now' : 'Closed now';
        el.setAttribute('title', todayLabel);
      });

      // Any element that mirrors today's hours (e.g. the hero badge)
      $$('[data-today-hours]').forEach(function (el) {
        el.textContent = todayLabel || '';
      });
      $$('[data-open-badge]').forEach(function (el) {
        el.classList.toggle('is-closed', !open);
        const txt = el.querySelector('[data-open-badge-text]');
        if (txt) txt.textContent = open ? 'Open today' : 'Closed now';
        el.hidden = !todayLabel;
      });
    }

    update();
    // refresh every minute, and when the tab comes back into focus
    on(window, 'focus', update);
    setInterval(update, 60000);
  }

  /* ======================================================================
     13. TOAST
     ====================================================================== */
  let toastTimer;
  function showToast(message) {
    const toast = $('.toast');
    if (!toast) return;
    const text = $('[data-toast-text]', toast);
    if (text) text.textContent = message;
    toast.classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toast.classList.remove('is-visible');
    }, 5000);
  }

  /* ======================================================================
     BOOT
     ====================================================================== */
  function init() {
    document.documentElement.classList.remove('no-js');
    hydrateSiteData();
    initHeader();
    initMobileNav();
    initSmoothScroll();
    initScrollSpy();
    initScrollTop();
    initReveal();
    initMenu();
    initGalleryFilter();
    initLightbox();
    initTabs();
    initForms();
    initOpenStatus();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
