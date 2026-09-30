/**
 * Headless smoke test for the Spice Route site.
 * Loads every page in jsdom, runs the real js/site-data.js + js/script.js and
 * fails on any console error, unhandled exception or failed resource.
 *
 *   node tools/smoke.mjs
 */
import { JSDOM, VirtualConsole } from 'jsdom';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PAGES = ['index.html', 'menu.html', 'about.html', 'gallery.html', 'contact.html'];
const BASE = 'http://localhost:8080/';

let failures = 0;
const fail = (page, msg) => { console.log(`  ✗ [${page}] ${msg}`); failures++; };
const pass = (page, msg) => console.log(`  ✓ [${page}] ${msg}`);

async function load(page) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', (e) => {
    const msg = String(e.message || e);
    // The sandbox has no outbound network, so the Google Fonts CDN fails.
    // The site is designed to degrade gracefully, so this is not a defect.
    if (/fonts\.googleapis|fonts\.gstatic/.test(msg)) return;
    errors.push('jsdomError: ' + (e.stack || e.message));
  });
  vc.on('error', (...a) => errors.push('console.error: ' + a.join(' ')));

  const dom = await JSDOM.fromURL(BASE + page, {
    runScripts: 'dangerously',
    resources: 'usable',
    pretendToBeVisual: true,
    virtualConsole: vc,
  });
  await new Promise((r) => setTimeout(r, 700));
  return { dom, errors, win: dom.window };
}

function click(win, el) {
  el.dispatchEvent(new win.MouseEvent('click', { bubbles: true, cancelable: true }));
}
function key(win, el, k) {
  el.dispatchEvent(new win.KeyboardEvent('keydown', { key: k, bubbles: true, cancelable: true }));
}

for (const page of PAGES) {
  console.log(`\n▸ ${page}`);
  const { dom, errors, win } = await load(page);
  const doc = win.document;
  const $ = (s) => doc.querySelector(s);
  const $$ = (s) => Array.from(doc.querySelectorAll(s));

  // 1. no runtime errors on load
  if (errors.length) errors.forEach((e) => fail(page, e));
  else pass(page, 'no console errors on load');

  // 2. data hydration from site-data.js
  const wa = $('[data-site-field="whatsappHref"]');
  if (!wa) fail(page, 'no whatsapp element found');
  else if (!wa.getAttribute('href').startsWith('https://wa.me/919876543210'))
    fail(page, 'WhatsApp link not hydrated: ' + wa.getAttribute('href'));
  else pass(page, 'WhatsApp link hydrated from site-data.js');

  const phone = $('[data-site-field="phoneHref"]');
  if (phone && phone.getAttribute('href') !== 'tel:+919876543210')
    fail(page, 'phone link not hydrated: ' + phone.getAttribute('href'));

  const copy = $('[data-site-field="copyright"]');
  if (copy && !/©/.test(copy.textContent)) fail(page, 'copyright not hydrated');

  // 3. active nav state
  const active = $$('.site-nav__link[aria-current="page"]');
  if (active.length !== 1) fail(page, `expected 1 aria-current nav link, found ${active.length}`);
  else pass(page, 'active navigation state correct');

  // 4. mobile nav opens, locks scroll, and closes on Escape
  const toggle = $('.nav-toggle');
  const nav = $('#site-nav');
  if (toggle && nav) {
    click(win, toggle);
    if (!nav.classList.contains('is-open')) fail(page, 'mobile nav did not open');
    else if (toggle.getAttribute('aria-expanded') !== 'true') fail(page, 'aria-expanded not set to true');
    else if (!doc.body.classList.contains('is-locked')) fail(page, 'body scroll not locked');
    else pass(page, 'mobile nav opens, aria-expanded + scroll lock set');

    key(win, doc, 'Escape');
    if (nav.classList.contains('is-open')) fail(page, 'Escape did not close mobile nav');
    else if (toggle.getAttribute('aria-expanded') !== 'false') fail(page, 'aria-expanded not reset');
    else if (doc.body.classList.contains('is-locked')) fail(page, 'body scroll still locked');
    else pass(page, 'Escape closes nav and releases scroll');
  }

  // ---- page-specific behaviour -------------------------------------
  if (page === 'menu.html') {
    const items = $$('.menu-item');
    const shown = () => items.filter((i) => !i.hidden).length;
    const total = shown();
    pass(page, `${total} menu items rendered`);

    // filter to a category
    const chip = $$('.filter-chip').find((c) => c.getAttribute('data-filter') === 'breads');
    click(win, chip);
    const after = shown();
    if (after === 0 || after === total) fail(page, `category filter did not narrow results (${after}/${total})`);
    else pass(page, `category filter works (${after} of ${total})`);
    if (chip.getAttribute('aria-pressed') !== 'true') fail(page, 'aria-pressed not set on active chip');
    else if ($$('.filter-chip[aria-pressed="true"]').length !== 1) fail(page, 'multiple chips pressed');
    else pass(page, 'filter chips expose correct aria-pressed');

    // search (reset the category filter first, otherwise this is
    // testing "biryani within breads", which correctly returns nothing)
    click(win, $$('.filter-chip').find((c) => c.getAttribute('data-filter') === 'all'));
    const search = $('#menu-search');
    search.value = 'biryani';
    search.dispatchEvent(new win.Event('input', { bubbles: true }));
    const found = shown();
    if (found === 0) fail(page, 'search for "biryani" returned nothing');
    else pass(page, `search works (${found} result(s) for "biryani")`);

    search.value = 'zzzznope';
    search.dispatchEvent(new win.Event('input', { bubbles: true }));
    if (!$('.empty-state').classList.contains('is-visible')) fail(page, 'empty state not shown for no matches');
    else pass(page, 'empty state appears when nothing matches');

    // back to all
    click(win, $$('.filter-chip').find((c) => c.getAttribute('data-filter') === 'all'));
    search.value = '';
    search.dispatchEvent(new win.Event('input', { bubbles: true }));
    if (shown() !== total) fail(page, 'reset did not restore all items');
    else pass(page, 'reset restores the full menu');

    // vegetarian toggle
    const veg = $('#veg-only');
    veg.checked = true;
    veg.dispatchEvent(new win.Event('change', { bubbles: true }));
    const vegOnly = items.filter((i) => !i.hidden).every((i) => i.getAttribute('data-veg') === 'true');
    if (!vegOnly) fail(page, 'vegetarian-only toggle let non-veg through');
    else pass(page, 'vegetarian-only toggle filters correctly');
    veg.checked = false;
    veg.dispatchEvent(new win.Event('change', { bubbles: true }));
  }

  if (page === 'gallery.html') {
    const tiles = $$('.gallery-item');
    const visible = () => tiles.filter((t) => !t.hidden).length;
    pass(page, `${visible()} gallery tiles rendered`);

    const chip = $$('.gallery-filter').find((c) => c.getAttribute('data-filter') === 'kitchen');
    click(win, chip);
    if (visible() === 0 || visible() === tiles.length) fail(page, 'gallery filter did not narrow results');
    else pass(page, `gallery filter works (${visible()} of ${tiles.length})`);
    click(win, $$('.gallery-filter').find((c) => c.getAttribute('data-filter') === 'all'));

    // lightbox
    const lb = $('.lightbox');
    click(win, tiles[1]);
    if (!lb.classList.contains('is-open')) fail(page, 'lightbox did not open');
    else if (!$('[data-lightbox-image]').getAttribute('src')) fail(page, 'lightbox image not set');
    else pass(page, `lightbox opens ("${$('[data-lightbox-title]').textContent}")`);
    if (!$('[data-lightbox-image]').alt) fail(page, 'lightbox image has no alt text');

    const before = $('[data-lightbox-counter]').textContent;
    key(win, doc, 'ArrowRight');
    const after = $('[data-lightbox-counter]').textContent;
    if (before === after) fail(page, 'arrow-key navigation did not move: ' + after);
    else pass(page, `arrow keys navigate the lightbox (${before.trim()} -> ${after.trim()})`);

    key(win, doc, 'ArrowLeft');
    if ($('[data-lightbox-counter]').textContent !== before)
      fail(page, 'ArrowLeft did not return to the previous photo');
    else pass(page, 'ArrowLeft steps back');

    key(win, doc, 'Escape');
    if (lb.classList.contains('is-open')) fail(page, 'Escape did not close lightbox');
    else if (doc.body.classList.contains('is-locked')) fail(page, 'scroll lock left on after lightbox close');
    else pass(page, 'Escape closes lightbox and releases scroll');
  }

  if (page === 'contact.html') {
    // tabs
    const tabs = $$('[role="tab"]');
    click(win, tabs[1]);
    if (tabs[1].getAttribute('aria-selected') !== 'true') fail(page, 'tab did not activate on click');
    else if (!$('#panel-enquiry').hidden === false) fail(page, 'enquiry panel not shown');
    else pass(page, 'tabs switch panels');
    key(win, tabs[1], 'ArrowLeft');
    if (tabs[0].getAttribute('aria-selected') !== 'true') fail(page, 'arrow-key tab navigation failed');
    else pass(page, 'arrow keys navigate tabs');
    click(win, tabs[0]);

    // --- validation: submit empty booking form ---
    const form = $('#panel-book form');
    form.dispatchEvent(new win.Event('submit', { bubbles: true, cancelable: true }));
    const errs = $$('#panel-book .field.has-error');
    if (errs.length === 0) fail(page, 'empty booking form submitted with no errors shown');
    else pass(page, `empty booking form blocked with ${errs.length} field error(s)`);
    const msg = $('#panel-book .field.has-error .field__error span');
    if (msg && !msg.textContent.trim()) fail(page, 'error message element is empty');
    const invalid = $('#book-name').getAttribute('aria-invalid');
    if (invalid !== 'true') fail(page, 'aria-invalid not set on invalid field');
    else pass(page, 'aria-invalid + inline error messages set');

    // --- invalid email ---
    $('#book-name').value = 'A';
    $('#book-phone').value = '+91 98765 43210';
    $('#book-email').value = 'not-an-email';
    $('#booking-date').value = '2099-01-01';
    $('#booking-time').value = '7:00 pm';
    $('#booking-guests').value = '2 guests';
    $('#book-consent').checked = true;
    form.dispatchEvent(new win.Event('submit', { bubbles: true, cancelable: true }));
    if (!$('#book-email').closest('.field').classList.contains('has-error')) fail(page, 'invalid email was accepted');
    else if (!$('#book-name').closest('.field').classList.contains('has-error')) fail(page, '1-character name was accepted');
    else pass(page, 'invalid email and too-short name rejected');

    // --- fully valid form ---
    $('#book-name').value = 'Ananya Rao';
    $('#book-email').value = 'ananya@example.com';
    form.dispatchEvent(new win.Event('submit', { bubbles: true, cancelable: true }));
    const success = $('#panel-book .form-success');
    if (!success.classList.contains('is-visible')) fail(page, 'valid form did not show the success panel');
    else pass(page, 'valid form shows the confirmation panel');
    if (!form.hidden) fail(page, 'form not hidden after successful submit');
    const waLink = $('[data-whatsapp-send]').getAttribute('href');
    if (!waLink.startsWith('https://wa.me/') || !decodeURIComponent(waLink).includes('Ananya Rao'))
      fail(page, 'WhatsApp handoff link malformed: ' + waLink.slice(0, 80));
    else pass(page, 'WhatsApp handoff link built correctly');
    const mailLink = $('[data-mail-send]').getAttribute('href');
    if (!mailLink.startsWith('mailto:')) fail(page, 'email fallback link malformed');
    else pass(page, 'email fallback link built correctly');
    if (!$('.toast').classList.contains('is-visible')) fail(page, 'toast confirmation not shown');
    else pass(page, 'toast confirmation shown');
  }

  // 4b. live open/closed status resolved from site-data.js
  const st = $('[data-open-status] span:last-child');
  if (st) {
    if (/loading/i.test(st.textContent)) fail(page, 'open/closed status still says "Loading…"');
    else if (!/open now|closed now/i.test(st.textContent)) fail(page, 'bad status text: ' + st.textContent);
    else pass(page, `live status resolved to "${st.textContent.trim()}"`);
  }
  const badge = $('[data-open-badge]');
  if (badge) {
    const bt = $('[data-open-badge-text]');
    const hrs = $('[data-today-hours]');
    // The sandbox clock is often outside opening hours, so accept either state.
    if (!bt || !/open today|closed now/i.test(bt.textContent)) fail(page, 'hero badge text not resolved: ' + (bt && bt.textContent));
    else if (!hrs || !/\d/.test(hrs.textContent)) fail(page, 'hero badge hours not resolved: ' + (hrs && hrs.textContent));
    else pass(page, `hero badge shows "${bt.textContent.trim()} · ${hrs.textContent.trim()}"`);
  }

  // 5. scroll-to-top appears after scrolling
  Object.defineProperty(win, 'scrollY', { value: 1200, writable: true, configurable: true });
  win.dispatchEvent(new win.Event('scroll'));
  await new Promise((r) => setTimeout(r, 50));
  const fab = $('.fab--top');
  if (fab && !fab.classList.contains('is-visible')) fail(page, 'scroll-to-top button did not appear');
  else pass(page, 'scroll-to-top button appears on scroll');

  dom.window.close();
}

console.log(failures ? `\n✗ ${failures} problem(s) found\n` : '\n✓ All pages load and behave correctly with no console errors.\n');
process.exit(failures ? 1 : 0);
