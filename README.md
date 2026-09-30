# Spice Route — Restaurant Website

> **This is a portfolio / demo project.**
> *Spice Route* is a **fictional** restaurant created to demonstrate front-end
> development skills. The name, address, phone numbers, prices, reviews and
> photography are all invented. Do not present this as a real business.

A five-page, production-quality marketing website for a premium Indian
restaurant, built with **plain HTML5, CSS3 and vanilla JavaScript**. No
frameworks, no build step, no dependencies, no back end, no paid services.

---

## Table of contents

1. [What is this?](#what-is-this)
2. [Live demo](#live-demo)
3. [Technologies used](#technologies-used)
4. [Project structure](#project-structure)
5. [Running it locally](#running-it-locally)
6. [Deploying it](#deploying-it)
7. [Making client edits](#making-client-edits) ← *read this one*
8. [Features & how they work](#features--how-they-work)
9. [Accessibility](#accessibility)
10. [SEO](#seo)
11. [Performance](#performance)
12. [Adding a back end later](#adding-a-back-end-later)
13. [Browser support](#browser-support)
14. [Licence](#licence)

---

## What is this?

A complete restaurant website designed to show a potential client what a
small-business site can look and feel like:

- **Five pages** — Home, Menu, About, Gallery, Contact
- **Fully responsive**, mobile-first, from 320 px phones to wide desktops
- **Accessible** — keyboard navigable, screen-reader friendly, WCAG AA colours
- **SEO-ready** — semantic HTML, per-page metadata, Open Graph, JSON-LD
- **Fast** — no framework, ~1 MB of images for the whole site, all lazy-loaded

Everything is plain text you can open in any code editor. There is no
`npm install`, no `npm run build`, and nothing that can break because a
dependency changed.

---

## Live demo

Open `index.html` in a browser — that is it.

To serve it locally instead (recommended, so the fonts and scripts behave
exactly as they will on a real server):

```bash
# Python 3 — works out of the box, no install needed
python3 -m http.server 8000

# …then visit http://localhost:8000
```

Or with Node, if you prefer:

```bash
npx serve .
```

> Tip: open the site with your browser's device toolbar (Ctrl/Cmd + Shift + M)
> and step through the breakpoints to check the responsive layouts.

---

## Technologies used

| Layer | Choice | Why |
|---|---|---|
| Markup | HTML5 | Semantic elements (`header`, `nav`, `main`, `article`, `footer`), native accessibility |
| Styling | CSS3 | Custom properties, `clamp()`, Grid, Flexbox, no framework |
| Behaviour | Vanilla JavaScript (ES5-compatible syntax) | ~950 lines, one IIFE, zero dependencies |
| Icons | Inline SVG sprite | 24 icons, no icon-font request, colourable via `currentColor` |
| Fonts | Google Fonts — Fraunces + Inter | Free, self-hostable, loaded with `display=swap` |
| Images | WebP with `srcset` | One 1600 px hero, everything else lazy-loaded |
| Maps | Stylised SVG placeholder | Swappable for a real Google Maps embed |
| Schema | JSON-LD `Restaurant` markup | Rich results in Google |

The only external request the site makes is the Google Fonts stylesheet.
Everything else — icons, textures, patterns, the map — is CSS or SVG, so the
site still looks correct if fonts or the network fail.

---

## Project structure

```
.
├── index.html              # Home
├── menu.html               # Menu (filter, search, dietary toggle)
├── about.html              # Our story, chefs, values, sourcing, atmosphere
├── gallery.html            # Filterable grid + accessible lightbox
├── contact.html            # Details, hours, map + booking & enquiry forms
├── 404.html                # Not-found page
│
├── css/
│   └── style.css           # The entire stylesheet, in 18 numbered sections
│
├── js/
│   ├── site-data.js        # ★ ALL BUSINESS DETAILS LIVE HERE
│   └── script.js           # All behaviour, 14 numbered modules
│
├── assets/
│   ├── favicon.svg         # Favicon (also used as a PWA icon)
│   ├── icon-192.svg
│   ├── icon-512.svg
│   └── images/
│       ├── map-placeholder.svg   # Stylised map — swap for a Maps embed
│       ├── og-cover.jpg          # Social share image (1200 × 630)
│       ├── hero-*.webp           # Hero, 4 widths (400/800/1200/1600)
│       ├── dish-*.webp           # Featured dishes
│       ├── gallery-*.webp        # Gallery photographs
│       └── menu-*.webp           # Menu category thumbnails
│
├── tools/                  # Optional helpers (not needed to run the site)
│   ├── build.py            # Regenerates the 6 pages from shared partials
│   ├── images.py           # Resizes / converts raw images to WebP
│   ├── check.py            # Pre-launch link / a11y / SEO checker
│   ├── contrast.py         # WCAG AA contrast audit of the palette
│   └── smoke.mjs           # Headless functional test (needs jsdom)
│
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── .gitignore
└── README.md
```

### About the `tools/` folder

The HTML pages are **complete, standalone files** — edit them directly and
they will keep working forever. Everything in `tools/` is optional.

| Tool | What it does | Needs |
|---|---|---|
| `build.py` | Regenerates the 6 pages from shared partials (header, footer, `<head>`, menu data) | Python 3 |
| `images.py` | Resizes and converts source images in `assets/images/raw/` to WebP | ImageMagick |
| `check.py` | Checks every page for broken links, missing `alt`, duplicate ids, heading jumps, unlabelled inputs and dead ARIA references | Python 3 |
| `contrast.py` | Audits the colour palette against WCAG AA | Python 3 |
| `smoke.mjs` | Loads every page headlessly and exercises the nav, filters, lightbox, tabs and forms | Node + `jsdom` |

```bash
python3 tools/check.py       # → "All checks passed"
python3 tools/contrast.py    # → "All colour pairs meet WCAG AA"
python3 tools/build.py       # only if you changed shared partials
```

> ⚠️ If you have hand-edited the `.html` files, `build.py` will overwrite
> those edits the next time it runs. For normal client edits (menu prices,
> phone number, opening hours) edit `js/site-data.js` or the `MENU_ITEMS`
> list at the top of `build.py` — no build step needed at all.

---

## Running it locally

1. Download or clone the project.
2. Open the folder in your code editor (VS Code, Sublime, etc.).
3. Double-click `index.html`, **or** run a local server (see
   [Live demo](#live-demo)).
4. Edit and save — the browser reloads.

There is nothing to install and nothing to configure.

---

## Deploying it

Because this is a static site, deployment is a file upload. Pick whichever is
easiest for you and your client.

### Netlify (free, drag and drop)

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop).
2. Drag the project folder in.
3. Done — you get a live HTTPS URL immediately.
4. Site settings → Change site name to `spice-route`.

### Vercel

```bash
npx vercel --prod
```

No framework preset is needed; it detects the static HTML automatically.

### GitHub Pages

```bash
git init
git add .
git commit -m "Spice Route website"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

Then **Settings → Pages → Source: Deploy from a branch → `main` / root**.
The site is served from `https://<you>.github.io/<repo>/`.

> If you use a sub-folder URL, remember the site is already written with
> **relative** links (`menu.html`, `css/style.css`), so it works from any
> folder without changing a thing.

### Traditional shared hosting

Upload the contents of the folder to `public_html/` over FTP. Done.

### Before you go live for a real client

Search and replace these demo values:

- [ ] `https://spiceroute-demo.example` in all five `.html` files
      (canonical + Open Graph URLs) and in `sitemap.xml` / `robots.txt`
- [ ] The business details in `js/site-data.js`
- [ ] The demo disclaimer in the footer (`js/site-data.js` → `disclaimer`)

---

## Making client edits

This is the part that matters most when a real client phones up.

### ⭐ Change 1 — business details (90% of all requests)

Open **`js/site-data.js`**. It is heavily commented and is the *only* file you
need for phone numbers, email, address, hours, social links and the footer
disclaimer. **Change it once and all five pages update.**

```js
phoneDisplay: '+91 98765 43210',   // shown to visitors
phoneDial:    '+919876543210',     // digits only, used by tel: links
whatsappNumber: '919876543210',    // country code + number, digits only
email:  'hello@spiceroute.example',
address: { …, oneLine: '…' },
hours:  [ { days: 'Monday – Thursday', open: '12:00 pm', close: '10:30 pm' } ],
social: { instagram: '…', facebook: '…', x: '…', tripadvisor: '…' },
```

**How it works:** the HTML contains sensible fallback text, then
`js/script.js` looks for any element tagged `data-site-field="phone"` (or
`email`, `whatsappHref`, `address`, `mapHref`, `copyright`…) and replaces its
content and `href`. So you can also hand a client a single line to change,
and it propagates everywhere.

### Change 2 — menu items, dishes and prices

The menu has **39 dishes** across six categories, generated from a single
`MENU_ITEMS` list near the top of **`tools/build.py`**. Edit a row, re-run
`python3 tools/build.py`, and `menu.html` is rebuilt:

```python
dict(cat="mains", name="Butter Chicken",
     desc="Tandoor-charred chicken in a tomato, cashew and fenugreek gravy, "
          "finished with white butter and cream.",
     price="480", kind="nonveg", photo=True,
     alt="Butter chicken in a brass bowl"),
```

| Field | Values |
|---|---|
| `cat` | `starters` · `mains` · `breads` · `rice` · `desserts` · `beverages` |
| `name`, `desc` | Text shown to guests — `desc` is also what the live search reads |
| `price` | Number only — no currency symbol, no commas (`"480"`) |
| `kind` | `veg` or `nonveg` — drives the green/red badge **and** the "Vegetarian only" filter |
| `photo` | `True` shows the category thumbnail. Each thumbnail is a square crop of one photograph per category, so this is kept to a single signature dish in each section |
| `alt` | Required whenever `photo=True` — this is what screen readers announce |

To **add** a dish, copy a `dict(...)` line into `MENU_ITEMS` and re-run the
build. To **remove** one, delete its line. The "6 dishes" counters under each
heading update automatically.

> 💡 Prefer to edit the HTML? That is completely fine — `menu.html` is ordinary
> readable markup. Just avoid running `tools/build.py` afterwards, or your
> edits will be replaced.

**Badges.** To tag a dish "New", add this inside its `.tag-row`:

```html
<span class="tag tag--new">New</span>
```

Available: `tag--veg`, `tag--nonveg`, `tag--gf` (gluten free), `tag--chef`, `tag--new`.


### Change 3 — featured dishes on the home page

`index.html` → search for `featured-title`. Each card is a `<article class="card">`.
Swap the `<img src>` and the text. To add one, copy a card and change its
`data-delay="3"` to the next number (0–5) for the staggered reveal.

### Change 4 — gallery photographs

`gallery.html` → search for `data-gallery`. Each tile is:

```html
<button class="gallery-item" type="button"
        data-lightbox="assets/images/gallery-naan-800.webp"
        data-caption="Straight from the tandoor"
        data-category-label="Food"
        data-category="food"
        data-ratio="4 / 3"
        aria-label="View larger: Fresh naan with charred bubbles">
  <img src="assets/images/gallery-naan-400.webp" alt="…" width="400" height="300" loading="lazy">
</button>
```

- `data-category` must be `food`, `interior` or `kitchen` to match a filter chip.
- `data-lightbox` is the large image shown in the lightbox.
- **Always update the `alt` text** when you swap a photo — it is what makes the
  page accessible and what Google Images reads.

### Change 5 — photos, colours and typography

**Photos.** Drop a new file in `assets/images/` and update the `src`. Aim for
WebP and always set `width` and `height` attributes to prevent the page
jumping while images load. Keep files under ~100 KB.

**Colours.** The whole palette lives in one block at the very top of
`css/style.css` (section `01. DESIGN TOKENS`):

```css
:root {
  --gold:   #c9962f;   /* primary accent  */
  --chilli: #a8321c;   /* non-veg / alerts */
  --leaf:   #5f7a4a;   /* veg marker      */
  --cream:  #fbf7f0;   /* page background */
  --ink:    #0d0b09;   /* dark sections   */
}
```

Change those five and the entire site re-themes.

**Fonts.** Two custom properties, `--font-display` and `--font-body`, plus the
Google Fonts `<link>` in each page's `<head>`.

### Change 6 — forms that actually submit

Right now the forms validate in the browser and then hand the details to
WhatsApp or the visitor's email client — a genuinely working pattern that
needs no server. To post to a real back end, open `js/script.js`, find the
`handleSubmit(form)` function, and replace the `/* … */` block at the top of
it with your `fetch()` call. Everything else (validation, error messages,
accessibility, the success panel) already works.

### Quick reference: "where do I change…?"

| Client says | You open |
|---|---|
| "Our phone number changed" | `js/site-data.js` |
| "Move us to Instagram" | `js/site-data.js` → `social` |
| "We close at 9 on weekdays" | `js/site-data.js` → `hours` |
| "Change the price of the biryani" | `menu.html` → search the dish |
| "Add a new starter" | `menu.html` → copy a block in `#starters` |
| "Take the paneer tikka photo off" | `menu.html` → delete the `menu-item__photo` span |
| "Swap the logo" | `assets/favicon.svg` + the logo `<svg>` in each page |
| "Make it pink and blue" | `css/style.css` → section 01 |
| "Add a new page" | Copy a `.html` file, add it to the nav in `tools/build.py`, re-run the build |
| "The map is wrong" | `assets/images/map-placeholder.svg` and `mapUrl` in `js/site-data.js` |

---

## Features & how they work

Every feature is **progressive-enhancement friendly** — if JavaScript fails,
the page still reads and every link still works.

| Feature | Where | Notes |
|---|---|---|
| Mobile navigation drawer | `initMobileNav` | Focus is trapped, `Esc` closes, body scroll locks, `aria-expanded` updates |
| Sticky header that shrinks | `initHeader` | Adds `.is-stuck` after 24 px of scroll |
| Smooth scrolling | `initSmoothScroll` | Offsets for the fixed header, moves focus for screen readers |
| Scroll spy | `initScrollSpy` | Highlights the nav item for the section you are reading |
| Menu filtering | `initMenu` | Six categories, updates per-category counts and an `aria-live` status line |
| Menu live search | `initMenu` | Multi-word AND search, `Esc` clears, result count announced |
| Vegetarian-only toggle | `initMenu` | Combines with the active category filter |
| Deep-linked filters | `initMenu` | `menu.html?filter=biryani` opens filtered — handy for sharing |
| Gallery filter | `initGalleryFilter` | Food / Interior / Kitchen, with an empty state |
| Lightbox | `initLightbox` | Focus trapped, `Esc` closes, arrow keys navigate, swipe on touch, focus returns to the tile you opened |
| Tabs | `initTabs` | Full ARIA tab pattern: arrows, `Home`, `End` |
| Form validation | `initForms` | Per-field rules, inline errors, `aria-invalid`, first invalid field focused and scrolled to |
| Booking date guard | `initForms` | Disables past dates, driven by `bookingLeadTimeDays` in `site-data.js` |
| Scroll-to-top | `initScrollTop` | Appears after 520 px, respects reduced motion |
| Reveal on scroll | `initReveal` | `IntersectionObserver`, staggered with `data-delay`, disabled under `prefers-reduced-motion` |
| Floating WhatsApp button | markup | Always visible on every page, populated from `site-data.js` |

### Animations are deliberately restrained

One slow fade-up on scroll, a gentle zoom on the hero, a lift on hover. They
all run behind `@media (prefers-reduced-motion: reduce)`, so the site is calm
for motion-sensitive users.

---

## Accessibility

Built in, not bolted on:

- **Semantic landmarks** — `header`, `nav`, `main`, `section`, `article`, `footer`, plus a "Skip to main content" link
- **Heading hierarchy** — exactly one `<h1>` per page, no skipped levels
- **Keyboard** — visible `:focus-visible` outlines everywhere, focus trapped in the nav drawer and the lightbox, full arrow-key support in the tabs
- **Forms** — every input has a real `<label>`, errors are linked with `aria-describedby`, and results are announced via `aria-live`
- **Images** — descriptive `alt` text (or `alt=""` where decorative); every image has explicit `width`/`height` to prevent layout shift
- **Colour contrast** — body text `#241e1a` on `#fbf7f0` and gold on near-black both exceed WCAG AA
- **Motion** — all animation respects `prefers-reduced-motion`
- **Icons** — decorative SVGs are `aria-hidden`; icon-only buttons carry `aria-label`

Test it yourself: put the mouse aside and `Tab` through the whole site.

---

## SEO

- Unique `<title>` and meta description on every page
- `<link rel="canonical">` on every page
- **Open Graph + Twitter card** metadata (so links look right when shared)
- **JSON-LD `Restaurant` schema** on the home and contact pages: address, geo
  coordinates, opening hours, price range, cuisines, phone, email
- `robots.txt` and `sitemap.xml` included
- Semantic HTML with a clean heading hierarchy
- Descriptive `alt` text on every image
- Favicon and web app manifest for mobile home-screen icons

> When you deploy for a real client, replace `https://spiceroute-demo.example`
> with their domain in the canonical tags, `sitemap.xml` and `robots.txt`.

---

## Performance

- No framework, no build step, no libraries — roughly **1 MB of images** for the
  entire site, and only what is on screen is loaded
- The hero uses `srcset` to serve 800/1200/1600 px variants
- Every image below the fold has `loading="lazy" decoding="async"`
- The 24-icon sprite is inlined in each page, so there is no icon request
- Background textures are inline SVG data URIs
- Fonts load with `display=swap` and `preconnect`, so text is readable immediately
- The page is fully readable with JavaScript disabled

Optional next steps for a real client: add a critical-CSS inline block, self-host
the fonts, and set long-lived cache headers for `/assets/`.

---

## Adding a back end later

The site needs none, but it is ready for one:

1. **Forms** — `handleSubmit()` in `js/script.js` is the single place to swap in
   a `fetch()` POST. Keep the `FormData` you already have.
2. **Reservations** — point `SITE.whatsappNumber` at a booking service, or post
   the payload to a Google Sheet via a free form relay.
3. **The map** — replace the `<img class="map-embed">` with a Google Maps
   `<iframe>` embed, or a Mapbox/Leaflet map.
4. **Headless CMS** — the menu is plain HTML today, so a CMS like Sanity,
   Contentful or Netlify CMS can slot in without changing the styling.

---

## Browser support

Chrome, Edge, Firefox and Safari (current and previous versions), plus
iOS Safari and Android Chrome. The site uses CSS Grid, custom properties and
`IntersectionObserver` — all supported since 2016/2019.

Older browsers degrade gracefully: no JavaScript means no filters or lightbox,
but all five pages remain fully readable with every link working.

---

## Licence

The code in this project is released for **portfolio and demonstration use**.
You are welcome to use, adapt and rebrand it for client work — just remove
the demo disclaimer once the business is real.

The photographs in `assets/images/` were generated for this project and carry
no third-party rights. Replace them with the client's own photography before
launching a real site.
