#!/usr/bin/env python3
"""
Builds the five HTML pages of the Spice Route site from shared partials,
so that the header, footer, icon sprite and <head> stay consistent.
Run once:  python3 tools/build.py
The generated .html files are what you edit / deploy.
"""
import os
from string import Template

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://spiceroute-demo.example"

# --------------------------------------------------------------------------
# ICON SPRITE — inlined once per page so there are no extra HTTP requests.
# --------------------------------------------------------------------------
ICONS = {
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "star": '<path d="m12 2.5 2.95 5.98 6.6.96-4.77 4.65 1.12 6.57L12 17.55l-5.9 3.11 1.12-6.57L2.45 9.44l6.6-.96z"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.2 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "whatsapp": '<path d="M12.04 2A9.9 9.9 0 0 0 2.1 11.9a9.8 9.8 0 0 0 1.35 4.96L2 22l5.28-1.38a9.9 9.9 0 0 0 4.76 1.21h.01a9.9 9.9 0 0 0 9.9-9.9A9.9 9.9 0 0 0 12.04 2zm5.8 14.06c-.24.68-1.42 1.31-1.96 1.36-.5.05-.98.24-3.3-.69-2.78-1.1-4.55-3.94-4.69-4.13-.14-.19-1.13-1.5-1.13-2.86s.72-2.03.97-2.31c.25-.28.55-.35.73-.35.18 0 .37 0 .53.01.17.01.4-.06.62.48.24.57.8 1.97.87 2.11.07.14.12.31.02.5-.1.19-.15.31-.29.47-.14.16-.3.36-.43.48-.14.14-.29.29-.12.57.17.28.74 1.22 1.59 1.98 1.09.97 2.01 1.27 2.3 1.41.28.14.45.12.62-.07.16-.19.71-.83.9-1.11.19-.28.37-.23.63-.14.25.09 1.62.76 1.9.9.28.14.46.21.53.33.07.12.07.68-.17 1.35z"/>',
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="m22 6-10 7L2 6"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6.5V12l3.5 2"/>',
    "instagram": '<rect x="2" y="2" width="20" height="20" rx="5.5"/><circle cx="12" cy="12" r="4"/><circle cx="17.6" cy="6.4" r="1.1" fill="currentColor" stroke="none"/>',
    "facebook": '<path d="M15.5 2h-2.2A4.8 4.8 0 0 0 8.5 6.8V10H6v4h2.5v8h4v-8H15l.8-4h-3.3V7.1c0-.8.3-1.1 1.1-1.1h2z"/>',
    "x": '<path d="M17.2 3h3.3l-7.2 8.2L21.8 21h-6.6l-4.4-5.7L5.7 21H2.4l7.7-8.8L2.5 3h6.8l4 5.3zm-1.2 16h1.8L8.1 4.9H6.1z"/>',
    "tripadvisor": '<circle cx="12" cy="12" r="10"/><circle cx="9" cy="10" r="1.2" fill="currentColor" stroke="none"/><circle cx="15" cy="10" r="1.2" fill="currentColor" stroke="none"/><path d="M8.5 15.5c1-1.5 2.3-2.2 3.5-2.2s2.5.7 3.5 2.2"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "flame": '<path d="M12 2.5s5.5 4.2 5.5 9.2A5.5 5.5 0 0 1 12 22a5.5 5.5 0 0 1-5.5-5.3c0-1.6.7-3 1.6-4.2.2 1 .8 1.8 1.6 2.2-.3-2.5.3-5.4 2.3-7.7.1 1.7.9 2.9 2 3.6 1-1.3 1-4.5-2-6.1z"/>',
    "chef": '<path d="M6 13.87A4 4 0 0 1 7.4 6a5.1 5.1 0 0 1 1.05-1.54 5 5 0 0 1 7.08 0A5.1 5.1 0 0 1 16.6 6 4 4 0 0 1 18 13.87V21H6z"/><path d="M6 17.5h12"/>',
    "heart": '<path d="M20.8 5.6a5.2 5.2 0 0 0-7.4 0L12 7l-1.4-1.4a5.2 5.2 0 0 0-7.4 7.4L12 21.4l8.8-8.4a5.2 5.2 0 0 0 0-7.4z"/>',
    "quote": '<path d="M9 11H5.5A2.5 2.5 0 0 0 3 13.5v2A2.5 2.5 0 0 0 5.5 18H7v1a3 3 0 0 1-3 3"/><path d="M21 11h-3.5A2.5 2.5 0 0 0 15 13.5v2a2.5 2.5 0 0 0 2.5 2.5H19v1a3 3 0 0 1-3 3"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/>',
    "zoom": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6M11 8.2v5.6M8.2 11h5.6"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2.5"/><circle cx="8.8" cy="9" r="1.8"/><path d="m3.5 17 4.6-4.2 3.4 3 3.2-2.8 5.8 5.2"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="17" rx="2.5"/><path d="M16 2.5v4M8 2.5v4M3 10h18"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "award": '<circle cx="12" cy="9" r="6"/><path d="m8.2 14.3-1.7 7.2 5.5-2.8 5.5 2.8-1.7-7.2"/>',
    "spice": '<path d="M3 12c0-4 4-8 9-8s9 4 9 8-4 8-9 8-9-4-9-8z"/><path d="M12 4c-2.5 2.5-2.5 13.5 0 16M12 4c2.5 2.5 2.5 13.5 0 16"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4.5M12 8h.01"/>',
    "alert": '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
}

def sprite():
    syms = []
    for name, paths in ICONS.items():
        syms.append(
            f'<symbol id="i-{name}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{paths}</symbol>'
        )
    return (
        '<svg class="visually-hidden" aria-hidden="true" focusable="false" '
        'xmlns="http://www.w3.org/2000/svg">' + "".join(syms) + "</svg>"
    )

def icon(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"></use></svg>'

# --------------------------------------------------------------------------
# LOGO
# --------------------------------------------------------------------------
LOGO_MARK = '''<svg class="logo__mark" viewBox="0 0 48 48" aria-hidden="true" focusable="false">
  <circle cx="24" cy="24" r="22.5" fill="none" stroke="currentColor" stroke-width="1.4" opacity=".45"/>
  <circle cx="24" cy="24" r="16" fill="none" stroke="currentColor" stroke-width="1"/>
  <g stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round">
    <path d="M24 8v32M8 24h32M13 13l22 22M35 13L13 35"/>
  </g>
  <circle cx="24" cy="24" r="5.5" fill="currentColor"/>
  <g fill="currentColor"><circle cx="24" cy="11" r="1.6"/><circle cx="24" cy="37" r="1.6"/>
  <circle cx="11" cy="24" r="1.6"/><circle cx="37" cy="24" r="1.6"/></g>
</svg>'''

# --------------------------------------------------------------------------
# SHARED <head>
# --------------------------------------------------------------------------
HEAD = Template('''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<meta name="description" content="$description">
<meta name="author" content="Spice Route — portfolio demo">
<meta name="robots" content="index, follow">
<link rel="canonical" href="$canonical">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Spice Route">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="$og_title">
<meta property="og:description" content="$description">
<meta property="og:url" content="$canonical">
<meta property="og:image" content="$url/assets/images/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A table of Indian dishes at Spice Route">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="$og_title">
<meta name="twitter:description" content="$description">
<meta name="twitter:image" content="$url/assets/images/og-cover.jpg">

<meta name="theme-color" content="#0d0b09">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/favicon.svg">
<link rel="manifest" href="site.webmanifest">

<!-- Fonts: preconnect + display=swap so text is never invisible -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600&display=swap">

<link rel="stylesheet" href="css/style.css">
$schema
<script>document.documentElement.classList.remove('no-js');</script>
</head>''')

# --------------------------------------------------------------------------
# SHARED HEADER
# --------------------------------------------------------------------------
HEADER = '''<a class="skip-link" href="#main">Skip to main content</a>
__SPRITE__
<header class="site-header">
  <div class="container site-header__inner">
    <a class="logo" href="index.html" aria-label="Spice Route — home">
      __LOGO__
      <span class="logo__text">
        <span class="logo__name" data-site-field="name">Spice Route</span>
        <span class="logo__tag">Est. 2014</span>
      </span>
    </a>

    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul class="site-nav__list">
        __NAV__
      </ul>
      <div class="site-nav__footer">
        <p class="site-nav__meta">
          <a href="tel:+919876543210" data-site-field="phoneHref" data-site-text>+91 98765 43210</a>
          <a href="mailto:hello@spiceroute.example" data-site-field="emailHref" data-site-text>hello@spiceroute.example</a>
          <span data-site-field="address">42, Saffron Street, Brigade Road, Bengaluru 560038</span>
        </p>
      </div>
    </nav>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="nav-toggle__bars" aria-hidden="true"><span></span><span></span><span></span></span>
      <span class="nav-toggle__text">Menu</span>
    </button>

    <a class="btn btn--sm site-header__cta" href="contact.html#book">Book a table</a>
  </div>
</header>'''

# --------------------------------------------------------------------------
# SHARED FOOTER
# --------------------------------------------------------------------------
FOOTER = '''<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div class="site-footer__brand">
        <a class="logo" href="index.html">
          __LOGO__
          <span class="logo__text">
            <span class="logo__name" data-site-field="name">Spice Route</span>
            <span class="logo__tag">Est. 2014</span>
          </span>
        </a>
        <p>Charcoal-smoked tandoor cooking, hand-ground masala and slow-simmered gravies, served in a warm, lantern-lit dining room in the heart of Bengaluru.</p>
        <div class="social-row">
          <a class="social-link" data-social="instagram" href="https://www.instagram.com/" aria-label="Spice Route on Instagram" rel="noopener noreferrer"><svg aria-hidden="true"><use href="#i-instagram"></use></svg></a>
          <a class="social-link" data-social="facebook" href="https://www.facebook.com/" aria-label="Spice Route on Facebook" rel="noopener noreferrer"><svg aria-hidden="true"><use href="#i-facebook"></use></svg></a>
          <a class="social-link" data-social="x" href="https://x.com/" aria-label="Spice Route on X" rel="noopener noreferrer"><svg aria-hidden="true"><use href="#i-x"></use></svg></a>
          <a class="social-link" data-social="tripadvisor" href="https://www.tripadvisor.com/" aria-label="Spice Route on TripAdvisor" rel="noopener noreferrer"><svg aria-hidden="true"><use href="#i-tripadvisor"></use></svg></a>
        </div>
      </div>

      <nav aria-labelledby="f-explore">
        <h2 id="f-explore">Explore</h2>
        <ul class="site-footer__list">
          <li><a href="index.html">Home</a></li>
          <li><a href="menu.html">Menu</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="gallery.html">Gallery</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="contact.html#book">Book a table</a></li>
        </ul>
      </nav>

      <div>
        <h2>Opening hours</h2>
        <ul class="site-footer__list" data-hours-list>
          <li>Mon – Thu &nbsp;12:00 pm – 10:30 pm</li>
          <li>Fri – Sat &nbsp;12:00 pm – 11:30 pm</li>
          <li>Sunday &nbsp;12:00 pm – 10:00 pm</li>
        </ul>
      </div>

      <div>
        <h2>Find us</h2>
        <ul class="site-footer__contact">
          <li>__ICON_PIN__<span data-site-field="address" data-social>42, Saffron Street, Brigade Road, Indiranagar, Bengaluru 560038</span></li>
          <li>__ICON_PHONE__<a href="tel:+919876543210" data-site-field="phoneHref">+91 98765 43210</a></li>
          <li>__ICON_MAIL__<a href="mailto:hello@spiceroute.example" data-site-field="emailHref">hello@spiceroute.example</a></li>
        </ul>
      </div>
    </div>

    <div class="site-footer__bottom">
      <p class="site-footer__disclaimer">
        __ICON_INFO__
        <span>Fictional portfolio demo. Spice Route is not a real restaurant — all details, prices, reviews and photography are illustrative.</span>
      </p>
      <p data-site-field="copyright">© 2025 Spice Route. All rights reserved.</p>
    </div>
  </div>
</footer>

<div class="floating-ui">
  <button class="fab fab--top" type="button" aria-label="Back to top">
    <svg aria-hidden="true" focusable="false" style="transform:rotate(-90deg)"><use href="#i-arrow"></use></svg>
    <span class="fab__tip">Back to top</span>
  </button>
  <a class="fab fab--wa" data-site-field="whatsappHref" href="https://wa.me/919876543210" aria-label="Chat with Spice Route on WhatsApp" rel="noopener">
    <svg aria-hidden="true" focusable="false"><use href="#i-whatsapp"></use></svg>
    <span class="fab__tip">WhatsApp us</span>
  </a>
</div>

<div class="toast" role="status" aria-live="polite">
  <svg aria-hidden="true" focusable="false"><use href="#i-check"></use></svg>
  <span data-toast-text>Saved.</span>
</div>'''

# --------------------------------------------------------------------------
# PAGE DEFINITIONS
# --------------------------------------------------------------------------
NAV_ITEMS = [
    ("index.html", "Home", None),
    ("menu.html", "Menu", None),
    ("about.html", "About", None),
    ("gallery.html", "Gallery", None),
    ("contact.html", "Contact", None),
]

SCHEMA = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "Spice Route",
  "description": "Authentic Indian flavours, served with soul. Charcoal tandoor cooking, hand-ground masala and slow-simmered gravies in a lantern-lit dining room.",
  "url": "https://spiceroute-demo.example/",
  "image": "https://spiceroute-demo.example/assets/images/og-cover.jpg",
  "telephone": "+91 98765 43210",
  "email": "hello@spiceroute.example",
  "priceRange": "₹₹",
  "servesCuisine": ["North Indian", "Mughlai", "Awadhi", "Hyderabadi", "Indian Street Food"],
  "acceptsReservations": "True",
  "foundingDate": "2014",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "42, Saffron Street, Brigade Road, Indiranagar",
    "addressLocality": "Bengaluru",
    "addressRegion": "Karnataka",
    "postalCode": "560038",
    "addressCountry": "IN"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 12.97194, "longitude": 77.64123 },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday"], "opens": "12:00", "closes": "22:30" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday","Saturday"], "opens": "12:00", "closes": "23:30" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "12:00", "closes": "22:00" }
  ]
}
</script>"""


def nav_html(current):
    out = []
    for href, label, _ in NAV_ITEMS:
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'<li><a class="site-nav__link" href="{href}"{cur}>{label}</a></li>')
    return "\n        ".join(out)


def render(filename, title, og_title, description, body, current, extra_head="", body_class=""):
    html = HEAD.substitute(
        title=title,
        og_title=og_title,
        description=description,
        canonical=SITE_URL + "/" + ("" if filename == "index.html" else filename),
        url=SITE_URL,
        schema=extra_head,
    )
    header = HEADER.replace("__SPRITE__", sprite()).replace("__LOGO__", LOGO_MARK).replace("__NAV__", nav_html(current))
    footer = (FOOTER
              .replace("__LOGO__", LOGO_MARK)
              .replace("__ICON_PIN__", icon("pin"))
              .replace("__ICON_PHONE__", icon("phone"))
              .replace("__ICON_MAIL__", icon("mail"))
              .replace("__ICON_INFO__", icon("info")))

    cls = (" " + body_class.strip()) if body_class.strip() else ""
    doc = f"""{html}
{header}

<main id="main">
{body}
</main>

{footer}

<script src="js/site-data.js"></script>
<script src="js/script.js" defer></script>
</body>
</html>
"""
    path = os.path.join(ROOT, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"  wrote {filename}  ({len(doc):,} bytes)")


# ==========================================================================
# HOME
# ==========================================================================
HOME = '''<section class="hero" aria-labelledby="hero-title">
  <div class="hero__media">
    <img src="assets/images/hero-1200.webp"
         srcset="assets/images/hero-800.webp 800w, assets/images/hero-1200.webp 1200w, assets/images/hero-1600.webp 1600w"
         sizes="100vw"
         width="1600" height="900"
         alt="A candlelit table at Spice Route set with brass bowls of curry, biryani, paneer tikka skewers and fresh naan.">
  </div>
  <div class="hero__scrim" aria-hidden="true"></div>
  <div class="container">
    <div class="hero__inner">
      <p class="hero__badge" data-open-badge>
        <span class="dot" aria-hidden="true"></span>
        <span data-open-badge-text>Open today</span>
        <span aria-hidden="true">·</span>
        <span data-today-hours>12:00 pm – 10:30 pm</span>
      </p>
      <h1 id="hero-title">Spice Route <em>Authentic Indian Flavours, Served With Soul</em></h1>
      <p class="hero__tagline">From our tandoor to your table.</p>
      <p class="hero__text">Charcoal-smoked breads, slow-simmered gravies and hand-ground masala — the food we grew up with, cooked the way it should be and served with genuine warmth.</p>
      <div class="btn-row">
        <a class="btn btn--lg" href="menu.html">View Menu</a>
        <a class="btn btn--lg btn--ghost-light" href="contact.html#book">Book a Table</a>
      </div>
      <ul class="hero__meta">
        <li class="hero__meta-item">__I_FIRE__<span><strong>31 vegetarian dishes</strong>Across a 39-dish menu</span></li>
        <li class="hero__meta-item">__I_CHEF__<span><strong>Chef-led kitchen</strong>Masala ground daily</span></li>
        <li class="hero__meta-item">__I_PIN__<span><strong>Brigade Road</strong>Bengaluru · 560038</span></li>
      </ul>
    </div>
  </div>
</section>

<!-- ============================= INTRO ============================= -->
<section class="section" aria-labelledby="intro-title">
  <div class="container">
    <div class="split split--wide-text">
      <div class="reveal">
        <p class="eyebrow">Welcome to Spice Route</p>
        <h2 id="intro-title">Regional Indian cooking, done properly.</h2>
      </div>
      <div class="reveal" data-delay="1">
        <p class="lead">We are a small, family-run kitchen on Brigade Road. Our menu travels from the Awadhi kitchens of Lucknow to the coastal kitchens of Kerala, with recipes that have been cooked in our family for three generations.</p>
        <p class="lead" style="margin-top:1rem">Nothing is finished before you order it. Gravies simmer from the morning service, breads come off the tandoor to order, and every masala is ground the same day it is used.</p>
        <div class="btn-row">
          <a class="btn" href="about.html">Our story</a>
          <a class="link-arrow" href="gallery.html">See the room <svg class="arrow" style="width:1em;height:1em" aria-hidden="true"><use href="#i-arrow"></use></svg></a>
        </div>
      </div>
    </div>

    <ul class="stats reveal" data-delay="2" style="margin-top:var(--space-2xl)">
      <li class="stat"><p class="stat__value">2014</p><p class="stat__label">Family founded</p></li>
      <li class="stat"><p class="stat__value">39</p><p class="stat__label">Dishes on the menu</p></li>
      <li class="stat"><p class="stat__value">31</p><p class="stat__label">Vegetarian dishes</p></li>
      <li class="stat"><p class="stat__value">3</p><p class="stat__label">Generations of recipes</p></li>
    </ul>
  </div>
</section>

<!-- ============================= FEATURED ============================= -->
<section class="section section--cream" aria-labelledby="featured-title">
  <div class="container">
    <div class="section-head section-head--split">
      <div class="section-head__text reveal">
        <p class="eyebrow">Guest favourites</p>
        <h2 id="featured-title">Four dishes we are known for</h2>
        <p class="lead">The plates that come back to the pass again and again — and the ones our regulars refuse to share.</p>
      </div>
      <a class="link-arrow reveal" data-delay="1" href="menu.html">Full menu <svg class="arrow" style="width:1em;height:1em" aria-hidden="true"><use href="#i-arrow"></use></svg></a>
    </div>

    <div class="grid grid--4">
      <article class="card reveal">
        <div class="card__media">
          <img src="assets/images/dish-butter-chicken-800.webp" width="800" height="1000" loading="lazy" decoding="async"
               alt="Butter chicken in a hammered brass bowl, finished with cream and kasuri methi.">
        </div>
        <div class="card__body">
          <h3 class="card__title">Butter Chicken</h3>
          <p class="card__text">Tandoor-charred chicken in a tomato, cashew and fenugreek gravy, finished with white butter and cream.</p>
          <div class="card__foot">
            <span class="tag tag--nonveg">Non-veg</span>
            <span class="price">₹480</span>
          </div>
        </div>
      </article>

      <article class="card reveal" data-delay="1">
        <div class="card__media">
          <img src="assets/images/dish-biryani-800.webp" width="800" height="1000" loading="lazy" decoding="async"
               alt="Hyderabadi chicken dum biryani with saffron rice, fried onions and fresh mint.">
        </div>
        <div class="card__body">
          <h3 class="card__title">Hyderabadi Dum Biryani</h3>
          <p class="card__text">Sealed-pot dum with long-grain basmati, saffron, fried onions and a whisper of rose water.</p>
          <div class="card__foot">
            <span class="tag tag--nonveg">Non-veg</span>
            <span class="price">₹520</span>
          </div>
        </div>
      </article>

      <article class="card reveal" data-delay="2">
        <div class="card__media">
          <img src="assets/images/dish-paneer-tikka-800.webp" width="800" height="1000" loading="lazy" decoding="async"
               alt="Paneer tikka shashlik skewers with charred peppers and onion.">
        </div>
        <div class="card__body">
          <h3 class="card__title">Paneer Tikka Shashlik</h3>
          <p class="card__text">Hung curd cheese marinated overnight, threaded with peppers and onion, finished over charcoal.</p>
          <div class="card__foot">
            <span class="tag tag--veg">Vegetarian</span>
            <span class="price">₹340</span>
          </div>
        </div>
      </article>

      <article class="card reveal" data-delay="3">
        <div class="card__media">
          <img src="assets/images/dish-halwa-800.webp" width="800" height="1000" loading="lazy" decoding="async"
               alt="Gajar ka halwa in a dark ceramic bowl, topped with slivered almonds and khoya.">
        </div>
        <div class="card__body">
          <h3 class="card__title">Gajar Ka Halwa</h3>
          <p class="card__text">Delhi-style carrot halwa slow-cooked in khoya and ghee, finished with almond and pistachio.</p>
          <div class="card__foot">
            <span class="tag tag--veg">Vegetarian</span>
            <span class="price">₹240</span>
          </div>
        </div>
      </article>
    </div>
  </div>
</section>

<!-- ============================= WHY US ============================= -->
<section class="section section--dark on-dark" aria-labelledby="why-title">
  <div class="container">
    <div class="section-head section-head--center reveal">
      <p class="eyebrow">Why choose us</p>
      <h2 id="why-title">What makes Spice Route different</h2>
      <p class="lead">Six reasons regulars keep coming back — and keep bringing their families.</p>
    </div>

    <div class="grid grid--3">
      <article class="feature reveal">
        <div class="feature__icon">__I_FIRE__</div>
        <h3>Live charcoal tandoor</h3>
        <p>Our tandoor burns hardwood charcoal, not gas. Breads blister in seconds and kebabs pick up real smoke, exactly as they would in a Punjabi dhaba.</p>
      </article>
      <article class="feature reveal" data-delay="1">
        <div class="feature__icon">__I_SPICE__</div>
        <h3>Masala ground daily</h3>
        <p>No pastes from a tub. Garam masala, kebab masala and chaat masala are ground in-house every morning, in small batches, right before service.</p>
      </article>
      <article class="feature reveal" data-delay="2">
        <div class="feature__icon">__I_LEAF__</div>
        <h3>Vegetarian-forward kitchen</h3>
        <p>Thirty-one of our thirty-nine dishes are vegetarian, and a good number of those are vegan as well. We treat paneer and seasonal vegetables as the stars, not an afterthought.</p>
      </article>
      <article class="feature reveal">
        <div class="feature__icon">__I_CHEF__</div>
        <h3>Chef-led, family recipes</h3>
        <p>Every recipe on this menu has been cooked in a family kitchen for at least three generations, then adapted for our tandoor.</p>
      </article>
      <article class="feature reveal" data-delay="1">
        <div class="feature__icon">__I_CLOCK__</div>
        <h3>Slow-simmered gravies</h3>
        <p>Our dal makhani is overnight on charcoal embers and our biryani is sealed and dum-cooked for forty minutes. Nothing is hurried.</p>
      </article>
      <article class="feature reveal" data-delay="2">
        <div class="feature__icon">__I_HEART__</div>
        <h3>Warm, unhurried service</h3>
        <p>A candlelit room, attentive servers and no rush to turn your table. We would rather you stayed for chai than left early.</p>
      </article>
    </div>
  </div>
</section>

<!-- ============================= TESTIMONIALS ============================= -->
<section class="section" aria-labelledby="testimonials-title">
  <div class="container">
    <div class="section-head section-head--center reveal">
      <p class="eyebrow">Kind words</p>
      <h2 id="testimonials-title">What our guests say</h2>
      <p class="demo-note">Sample testimonials written for this demo</p>
    </div>

    <div class="grid grid--3">
      <figure class="testimonial reveal">
        <p class="testimonial__quote" aria-hidden="true">__I_QUOTE__</p>
        <blockquote>“The dal makhani is the best I have eaten outside a Punjabi home. You can taste the hours in it. The butter chicken is a proper restaurant version — rich without being heavy.”</blockquote>
        <figcaption class="testimonial__person">
          <span class="avatar" aria-hidden="true">AR</span>
          <span>
            <span class="testimonial__name">Ananya Rao</span><br>
            <span class="testimonial__meta"><span class="stars" aria-label="Rated 5 out of 5">__STARS5__</span> · Sample review</span>
          </span>
        </figcaption>
      </figure>

      <figure class="testimonial reveal" data-delay="1">
        <p class="testimonial__quote" aria-hidden="true">__I_QUOTE__</p>
        <blockquote>“We came for a birthday dinner of eight and they made the whole room feel like a celebration. The paneer tikka was smoky perfection and the staff could not have been kinder.”</blockquote>
        <figcaption class="testimonial__person">
          <span class="avatar" aria-hidden="true">IM</span>
          <span>
            <span class="testimonial__name">Imran Malik</span><br>
            <span class="testimonial__meta"><span class="stars" aria-label="Rated 5 out of 5">__STARS5__</span> · Sample review</span>
          </span>
        </figcaption>
      </figure>

      <figure class="testimonial reveal" data-delay="2">
        <p class="testimonial__quote" aria-hidden="true">__I_QUOTE__</p>
        <blockquote>“As a family with two vegetarians I am tired of apologising at restaurants. Here nobody blinked. The malai kofta and kacchi biryani are outstanding.”</blockquote>
        <figcaption class="testimonial__person">
          <span class="avatar" aria-hidden="true">SK</span>
          <span>
            <span class="testimonial__name">Sunita Kulkarni</span><br>
            <span class="testimonial__meta"><span class="stars" aria-label="Rated 5 out of 5">__STARS5__</span> · Sample review</span>
          </span>
        </figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- ============================= HOURS + LOCATION ============================= -->
<section class="section section--cream" id="visit" data-spy aria-labelledby="visit-title">
  <div class="container">
    <div class="section-head section-head--center reveal">
      <p class="eyebrow">Visit us</p>
      <h2 id="visit-title">Opening hours &amp; location</h2>
      <p class="lead">We are on Brigade Road, a short walk from the metro. Walk-ins are welcome, but weekends fill up fast.</p>
    </div>

    <div class="split">
      <div class="hours-card reveal">
        <p class="hours-status" data-open-status><span class="dot" aria-hidden="true"></span> <span>Loading hours…</span></p>
        <h3 style="font-size:var(--step-1);margin-bottom:.5rem">Opening hours</h3>
        <dl class="hours-list" data-hours>
          <div class="hours-list__row"><dt>Monday – Thursday</dt><dd>12:00 pm – 10:30 pm</dd></div>
          <div class="hours-list__row"><dt>Friday – Saturday</dt><dd>12:00 pm – 11:30 pm</dd></div>
          <div class="hours-list__row"><dt>Sunday</dt><dd>12:00 pm – 10:00 pm</dd></div>
        </dl>
        <p class="hours-note">Kitchen closes 30 minutes before the restaurant. Walk-ins are always welcome, but we recommend booking at weekends.</p>
        <div class="btn-row">
          <a class="btn" href="contact.html#book">Book a table</a>
          <a class="btn btn--ghost" data-site-field="whatsappHref" href="https://wa.me/919876543210">WhatsApp</a>
        </div>
      </div>

      <div class="reveal" data-delay="1">
        <div class="map-embed">
          <img src="assets/images/map-placeholder.svg" width="1200" height="750" loading="lazy" decoding="async"
               alt="Stylised map showing Spice Route on Brigade Road, Indiranagar, Bengaluru.">
          <div class="map-embed__overlay">
            <p><strong>Spice Route</strong>42, Saffron Street, Brigade Road, Bengaluru 560038</p>
            <a class="btn btn--sm" data-site-field="mapHref" href="https://www.google.com/maps/search/?api=1&amp;query=Brigade%20Road%2C%20Bengaluru" target="_blank" rel="noopener noreferrer">Open in Google Maps <svg class="arrow" style="width:1em;height:1em" aria-hidden="true"><use href="#i-arrow"></use></svg></a>
          </div>
        </div>
        <ul class="info-list">
          <li class="info-list__item">
            <span class="info-list__icon">__I_PIN__</span>
            <span><span class="info-list__label">Address</span><span class="info-list__value" data-site-field="address">42, Saffron Street, Brigade Road, Indiranagar, Bengaluru 560038</span></span>
          </li>
          <li class="info-list__item">
            <span class="info-list__icon">__I_PHONE__</span>
            <span><span class="info-list__label">Reservations</span><span class="info-list__value"><a href="tel:+919876543210" data-site-field="phoneHref">+91 98765 43210</a></span></span>
          </li>
          <li class="info-list__item">
            <span class="info-list__icon">__I_MAIL__</span>
            <span><span class="info-list__label">Email</span><span class="info-list__value"><a href="mailto:hello@spiceroute.example" data-site-field="emailHref">hello@spiceroute.example</a></span></span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ============================= CTA ============================= -->
<section class="cta-band on-dark" aria-labelledby="cta-title">
  <div class="container">
    <div class="cta-band__inner reveal">
      <p class="eyebrow">Reservations</p>
      <h2 id="cta-title">Save yourself a table</h2>
      <p class="lead">Booking takes under a minute online, or send us a WhatsApp message and we will confirm within the hour during service times.</p>
      <div class="btn-row">
        <a class="btn btn--lg" href="contact.html#book">Book a table</a>
        <a class="btn btn--lg btn--ghost-light" data-site-field="whatsappHref" href="https://wa.me/919876543210">Message on WhatsApp <svg class="arrow" style="width:1.1em;height:1.1em" aria-hidden="true"><use href="#i-whatsapp"></use></svg></a>
      </div>
    </div>
  </div>
</section>'''

# ==========================================================================
# MENU
# ==========================================================================
# --------------------------------------------------------------------------
# MENU DATA  (category, name, description, price, veg/nonveg, photo, alt)
# This is the single source of truth for the menu page. Edit here.
# --------------------------------------------------------------------------
MENU_ITEMS = [
    dict(cat="starters", name="Paneer Tikka Shashlik", desc="Hung curd cheese marinated overnight with hung curd, yoghurt and smoked chilli, threaded with peppers and onion and finished over charcoal.", price="340",
         kind="veg", photo=True, alt="Paneer Tikka Shashlik skewers over charcoal"),
    dict(cat="starters", name="Chicken Malai Tikka", desc="Cream-cheese and cashew marinated chicken with green chilli, grilled in the tandoor and finished with burnt garlic and lemon.", price="380",
         kind="nonveg", photo=False, alt="Chicken malai tikka with burnt garlic"),
    dict(cat="starters", name="Hara Bhara Kebab", desc="Spinach, green peas, potato and paneer patties, crisp on the outside, served with mint chutney.", price="310",
         kind="veg", photo=False, alt="Spinach and pea kebabs with mint chutney"),
    dict(cat="starters", name="Samosa Chaat", desc="Two crisp samosas broken over chickpeas, yoghurt, tamarind, mint chutney and fine sev. A Bengaluru street classic.", price="240",
         kind="veg", photo=False, alt="Samosa chaat with chutneys and sev"),
    dict(cat="starters", name="Tandoori Broccoli", desc="Whole roast broccoli finished with chaat masala, amchur and a sharp tamarind reduction.", price="290",
         kind="veg", photo=False, alt="Roast broccoli with chaat masala"),
    dict(cat="starters", name="Prawns Koliwada", desc="Crisp-battered prawns with curry leaf, kashmiri chilli and a kokum dip.", price="520",
         kind="nonveg", photo=False, alt="Crisp battered prawns koliwada"),
    dict(cat="mains", name="Butter Chicken", desc="Tandoor-charred chicken in a tomato, cashew and fenugreek gravy, finished with white butter and cream.", price="480",
         kind="nonveg", photo=True, alt="Butter chicken in a brass bowl"),
    dict(cat="mains", name="Paneer Lababdar", desc="A rich Punjabi tomato gravy with cashew, butter and cream, with lightly charred paneer cubes.", price="440",
         kind="veg", photo=False, alt="Paneer lababdar in a rich tomato gravy"),
    dict(cat="mains", name="Lamb Rogan Josh", desc="Kashmiri chillies and ratanjot braise lamb shank slowly until it falls from the bone.", price="640",
         kind="nonveg", photo=False, alt="Lamb rogan Josh in a copper serving bowl"),
    dict(cat="mains", name="Dal Makhani", desc="Black urad lentils simmered overnight on charcoal embers with tomato, cream and fresh cream.", price="340",
         kind="veg", photo=False, alt="Creamy dal makhani in a brass bowl"),
    dict(cat="mains", name="Malai Kofta", desc="Soft vegetable and paneer kofta in a mild cashew and cream gravy, finished with fresh cream.", price="390",
         kind="veg", photo=False, alt="Malai kofta in a cashew cream gravy"),
    dict(cat="mains", name="Goan Fish Curry", desc="Coconut and kokum gravy with shallots, curry leaf and lightly charred pomfret or seer fish.", price="620",
         kind="nonveg", photo=False, alt="Goan coconut fish curry"),
    dict(cat="mains", name="Kadhai Mushroom", desc="Button mushrooms and bell pepper in a freshly pounded kadhai masala.", price="380",
         kind="veg", photo=False, alt="Mushrooms in kadhai masala"),
    dict(cat="mains", name="Murgh Malai", desc="Murgh Malai is a delicate Mughlai preparation, chicken simmered in a mild milk gravy with green cardamom.", price="470",
         kind="nonveg", photo=False, alt="Murgh malai in a mild milk gravy"),
    dict(cat="mains", name="Baingan Bharta", desc="Whole aubergine roasted over an open flame, then mashed with ginger, green chilli and onion.", price="330",
         kind="veg", photo=False, alt="Roasted baingan bharta"),
    dict(cat="breads", name="Garlic Naan", desc="Tandoor-baked, brushed with garlic butter and coriander.", price="120",
         kind="veg", photo=True, alt="Garlic naan straight from the tandoor"),
    dict(cat="breads", name="Butter Kulcha", desc="Stuffed with potato and nigard seed, brushed with butter.", price="150",
         kind="veg", photo=False, alt="Stuffed butter kulcha"),
    dict(cat="breads", name="Laccha Paratha", desc="Multi-layered, flaky and brushed with ghee. Best with a dal.", price="140",
         kind="veg", photo=False, alt="Flaky laccha paratha"),
    dict(cat="breads", name="Tandoori Roti", desc="Whole wheat roti, lightly charred, served with a small dish of butter.", price="80",
         kind="veg", photo=False, alt="Charred tandoori roti"),
    dict(cat="breads", name="Tandoori Roti with Butter", desc="Whole wheat roti finished with butter, served hot from the tandoor.", price="100",
         kind="veg", photo=False, alt="Butter tandoori roti"),
    dict(cat="breads", name="Truffle &amp; Cheese Naan", desc="Loaded with cheese, garlic and a truffle butter drizzle. A modern favourite.", price="260",
         kind="veg", photo=False, alt="Truffle and cheese naan"),
    dict(cat="rice", name="Hyderabadi Chicken Dum Biryani", desc="Long-grain basmati sealed with marinated chicken, saffron, fried onions and rose water, dum-cooked for forty minutes.", price="520",
         kind="nonveg", photo=True, alt="Hyderabadi chicken dum biryani"),
    dict(cat="rice", name="Subz Kacchi Biryani", desc="Long-grain rice layered with raw marinated vegetables, fried onions and mint, then slow-cooked under a sealed lid.", price="480",
         kind="veg", photo=False, alt="Vegetarian kacchi biryani"),
    dict(cat="rice", name="Mutton Biryani", desc="Sealed-pot dum with mutton, saffron and fried onion, served with raita and salad.", price="760",
         kind="nonveg", photo=False, alt="Mutton biryani in a brass handi"),
    dict(cat="rice", name="Jeera Rice", desc="Basmati tempered with cumin, ghee, cashew and coriander.", price="240",
         kind="veg", photo=False, alt="Jeera rice with cashew and coriander"),
    dict(cat="rice", name="Veg Pulao", desc="Light, fragrant basmati with seasonal vegetables, mint and fried onion.", price="280",
         kind="veg", photo=False, alt="Vegetable pulao with mint"),
    dict(cat="rice", name="Lemon Rice", desc="Curry leaf, mustard seed, green chilli and lemon — a clean South Indian finish to a heavy meal.", price="230",
         kind="veg", photo=False, alt="Curry leaf lemon rice"),
    dict(cat="desserts", name="Gulab Jamun", desc="Warm khoya dumplings soaked in rose and cardamom syrup, served warm with rabri.", price="190",
         kind="veg", photo=False, alt="Gulab jamun in syrup with rabri"),
    dict(cat="desserts", name="Gajar Ka Halwa", desc="Delhi-style carrot halwa slow-cooked in khoya and ghee, finished with almond and pistachio.", price="240",
         kind="veg", photo=True, alt="Gajar ka halwa with nuts"),
    dict(cat="desserts", name="Rasmalai Tres Leches", desc="Saffron-infused milk cake soaked in three milks, topped with rabri and pistachio.", price="280",
         kind="veg", photo=False, alt="Rasmalai tres leches cake"),
    dict(cat="desserts", name="Kulfi Falooda", desc="Pistachio kulfi over rose syrup, basil seeds, sabja and soft falooda noodles.", price="300",
         kind="veg", photo=False, alt="Kulfi falooda in a tall glass"),
    dict(cat="desserts", name="Gulab Shahi", desc="A festive Hyderabadi dessert of semolina dumplings in saffron, rose and dry-fruit syrup.", price="260",
         kind="veg", photo=False, alt="Gulab shahi in saffron syrup"),
    dict(cat="desserts", name="Miso Chocolate Cake", desc="A warm dark chocolate and white miso cake with salted caramel. Our pastry chef''s pick.", price="320",
         kind="veg", photo=False, alt="Dark chocolate miso cake slice"),
    dict(cat="beverages", name="Masala Chai", desc="Assam tea simmered with ginger, cardamom, clove and a splash of milk. Served in a kulhad.", price="120",
         kind="veg", photo=False, alt="Masala chai in a clay kulhad"),
    dict(cat="beverages", name="Filter Kaapi", desc="South Indian filter coffee, decoction poured over hot milk and frothed.", price="130",
         kind="veg", photo=False, alt="South Indian filter coffee"),
    dict(cat="beverages", name="Mango Lassi", desc="Thick hung-curd lassi blended with Alphonso mango and mint.", price="200",
         kind="veg", photo=False, alt="Mango lassi glass"),
    dict(cat="beverages", name="Fresh Lime Soda", desc="Freshly pressed lime, soda and a pinch of salt or sugar. Sweet, salted or mixed.", price="130",
         kind="veg", photo=False, alt="Fresh lime soda with mint"),
    dict(cat="beverages", name="Jaljeera", desc="A cumin-forward cooler with mint and tamarind, served chilled.", price="140",
         kind="veg", photo=False, alt="Chilled jaljeera in a glass"),
    dict(cat="beverages", name="Thandai", desc="A festive almond and rose drink with fennel, saffron and white pepper. Served chilled or warm.", price="220",
         kind="veg", photo=False, alt="Chilled thandai in a tall glass"),
]


MENU = '''<section class="page-banner on-dark">
  <div class="container">
    <div class="page-banner__inner">
      <p class="eyebrow">Our kitchen</p>
      <h1>The Menu</h1>
      <p class="lead">Six sections, thirty-nine dishes, and something worth ordering at every course. Everything is cooked to order &mdash; please allow a little extra time at peak hours.</p>
      <h2 class="visually-hidden">Browse by category</h2>
      <nav class="quick-jump" aria-label="Jump to a menu section">
        <a href="#starters">Starters</a>
        <a href="#mains">Main course</a>
        <a href="#breads">Breads</a>
        <a href="#rice">Rice &amp; Biryani</a>
        <a href="#desserts">Desserts</a>
        <a href="#beverages">Beverages</a>
      </nav>
    </div>
  </div>
</section>

<!-- ============================= TOOLBAR ============================= -->
<div class="menu-toolbar">
  <div class="container">
    <div class="menu-toolbar__inner">
      <div class="filter-chips" role="group" aria-label="Filter the menu by category">
        <button class="chip filter-chip" type="button" data-filter="all" aria-pressed="true">All</button>
        <button class="chip filter-chip" type="button" data-filter="starters" aria-pressed="false">Starters</button>
        <button class="chip filter-chip" type="button" data-filter="mains" aria-pressed="false">Main course</button>
        <button class="chip filter-chip" type="button" data-filter="breads" aria-pressed="false">Breads</button>
        <button class="chip filter-chip" type="button" data-filter="rice" aria-pressed="false">Rice &amp; Biryani</button>
        <button class="chip filter-chip" type="button" data-filter="desserts" aria-pressed="false">Desserts</button>
        <button class="chip filter-chip" type="button" data-filter="beverages" aria-pressed="false">Beverages</button>
      </div>
      <div class="search-field">
        <svg aria-hidden="true" focusable="false"><use href="#i-search"></use></svg>
        <label class="visually-hidden" for="menu-search">Search the menu</label>
        <input type="search" id="menu-search" placeholder="Search dishes&hellip;" autocomplete="off" spellcheck="false">
        <button class="search-field__clear" type="button" aria-label="Clear search">
          <svg aria-hidden="true" focusable="false"><use href="#i-close"></use></svg>
        </button>
      </div>
    </div>
  </div>
</div>

<div class="section" data-menu>
  <div class="container">
    <div class="menu-legend">
      <span><span class="dot-veg" aria-hidden="true"></span> Vegetarian</span>
      <span><span class="dot-nonveg" aria-hidden="true"></span> Non-vegetarian</span>
      <span>All prices in &rupee; and exclusive of taxes.</span>
      <span style="margin-left:auto;display:inline-flex;align-items:center;gap:.5rem">
        <input type="checkbox" id="veg-only" style="accent-color:#5f7a4a;width:16px;height:16px">
        <label for="veg-only" style="cursor:pointer">Vegetarian only</label>
      </span>
    </div>

    <p class="menu-status" role="status" aria-live="polite">Showing the full menu</p>

    <div class="empty-state">
      <h3>No dishes found</h3>
      <p>Try a different search term, or clear the filters to see the full menu.</p>
    </div>

    <section class="menu-category" id="starters" aria-labelledby="starters-title">
      <div class="menu-category__head">
        <h2 id="starters-title">Starters</h2>
        <span class="menu-category__count" data-count-for="starters">6 dishes</span>
      </div>
      <div class="menu-list menu-list--2">
        @@ITEM@@0
        @@ITEM@@1
        @@ITEM@@2
        @@ITEM@@3
        @@ITEM@@4
        @@ITEM@@5
      </div>
    </section>
    <section class="menu-category" id="mains" aria-labelledby="mains-title">
      <div class="menu-category__head">
        <h2 id="mains-title">Main Course</h2>
        <span class="menu-category__count" data-count-for="mains">9 dishes</span>
      </div>
      <div class="menu-list menu-list--2">
        @@ITEM@@6
        @@ITEM@@7
        @@ITEM@@8
        @@ITEM@@9
        @@ITEM@@10
        @@ITEM@@11
        @@ITEM@@12
        @@ITEM@@13
        @@ITEM@@14
      </div>
    </section>
    <section class="menu-category" id="breads" aria-labelledby="breads-title">
      <div class="menu-category__head">
        <h2 id="breads-title">Breads</h2>
        <span class="menu-category__count" data-count-for="breads">6 dishes</span>
      </div>
      <div class="menu-list menu-list--2">
        @@ITEM@@15
        @@ITEM@@16
        @@ITEM@@17
        @@ITEM@@18
        @@ITEM@@19
        @@ITEM@@20
      </div>
    </section>
    <section class="menu-category" id="rice" aria-labelledby="rice-title">
      <div class="menu-category__head">
        <h2 id="rice-title">Rice &amp; Biryani</h2>
        <span class="menu-category__count" data-count-for="rice">6 dishes</span>
      </div>
      <div class="menu-list menu-list--2">
        @@ITEM@@21
        @@ITEM@@22
        @@ITEM@@23
        @@ITEM@@24
        @@ITEM@@25
        @@ITEM@@26
      </div>
    </section>
    <section class="menu-category" id="desserts" aria-labelledby="desserts-title">
      <div class="menu-category__head">
        <h2 id="desserts-title">Desserts</h2>
        <span class="menu-category__count" data-count-for="desserts">6 dishes</span>
      </div>
      <div class="menu-list menu-list--2">
        @@ITEM@@27
        @@ITEM@@28
        @@ITEM@@29
        @@ITEM@@30
        @@ITEM@@31
        @@ITEM@@32
      </div>
    </section>
    <section class="menu-category" id="beverages" aria-labelledby="beverages-title">
      <div class="menu-category__head">
        <h2 id="beverages-title">Beverages</h2>
        <span class="menu-category__count" data-count-for="beverages">6 dishes</span>
      </div>
      <p class="menu-note" style="margin-top:0;margin-bottom:var(--space-m)">Our drinks carry no set-tasting-menu photograph, but every one of them is made to order &mdash; the chai is simmered on the stove and the lassi is blended while you watch.</p>
      <div class="menu-list menu-list--2">
        @@ITEM@@33
        @@ITEM@@34
        @@ITEM@@35
        @@ITEM@@36
        @@ITEM@@37
        @@ITEM@@38
      </div>
    </section>

    <p class="menu-note">
      <strong>Allergies &amp; diets.</strong> Please tell your server before ordering. We cook in a shared kitchen and many gravies contain dairy and nuts. Full allergen information is available on request.
    </p>
  </div>
</div>

<section class="cta-band on-dark" aria-labelledby="menu-cta-title">
  <div class="container">
    <div class="cta-band__inner reveal">
      <p class="eyebrow">Ready when you are</p>
      <h2 id="menu-cta-title">Hungry already?</h2>
      <p class="lead">Book a table and we will have the tandoor lit and a chai in your hand within minutes of your arrival.</p>
      <div class="btn-row">
        <a class="btn btn--lg" href="contact.html#book">Book a table</a>
        <a class="btn btn--lg btn--ghost-light" href="about.html">Read our story</a>
      </div>
    </div>
  </div>
</section>'''

# ==========================================================================
# ABOUT
# ==========================================================================
ABOUT = '''<section class="page-banner on-dark">
  <div class="container">
    <div class="page-banner__inner">
      <p class="eyebrow">Our story</p>
      <h1>About Spice Route</h1>
      <p class="lead">A family kitchen that outgrew a home, a stubborn love of real spice, and a dining room we built one brass lamp at a time.</p>
    </div>
  </div>
</section>

<!-- ============================= STORY ============================= -->
<section class="section" aria-labelledby="story-title">
  <div class="container">
    <div class="split">
      <div class="story-block reveal">
        <p class="eyebrow">Est. 2014</p>
        <h2 id="story-title">It started in a home kitchen in Lucknow</h2>
        <p>Spice Route began in 2014 as a Sunday lunch for eleven people in a two-bedroom flat in Bengaluru. The menu was short — dal makhani, a chicken curry, one biryani, and a garlic naan that everybody fought over. By the third month, the neighbours were knocking at the door asking for more.</p>
        <p>Two years later we took a narrow shopfront on Brigade Road with four tables, one tandoor and a stubborn insistence on doing things the slow way. The tandoor is still the same one. The masala is still ground every morning. The only thing that has really changed is the number of people eating with us.</p>
        <blockquote class="pull-quote">“If a dish tastes good only after an hour of pressure, it does not belong on my menu.”</blockquote>
        <p>Today our kitchen serves food from across the subcontinent — Awadhi, Punjabi, Hyderabadi, Goan, Gujarati and the Bengaluru street food we grew up eating on Brigade Road. What ties it together is not a style but a method: cook it properly, season it properly, and serve it with soul.</p>
        <div class="btn-row">
          <a class="btn" href="menu.html">Explore the menu</a>
          <a class="link-arrow" href="gallery.html">See inside <svg class="arrow" style="width:1em;height:1em" aria-hidden="true"><use href="#i-arrow"></use></svg></a>
        </div>
      </div>
      <div class="split__media frame-stack reveal" data-delay="1">
        <figure class="frame frame--landscape">
          <img src="assets/images/gallery-interior-dining-800.webp" width="1200" height="960" loading="lazy" decoding="async"
               alt="The main dining room at Spice Route, with arched brass-lit niches, candlelit tables and a long bar.">
        </figure>
      </div>
    </div>
  </div>
</section>

<!-- ============================= VALUES ============================= -->
<section class="section section--cream" aria-labelledby="values-title">
  <div class="container">
    <div class="split">
      <div class="split__media frame-stack reveal">
        <figure class="frame">
          <img src="assets/images/gallery-tandoor-800.webp" width="800" height="1000" loading="lazy" decoding="async"
               alt="A clay tandoor glowing with orange flame, naan blistering on its inner walls.">
        </figure>
      </div>
      <div class="reveal" data-delay="1">
        <p class="eyebrow">What we stand for</p>
        <h2 id="values-title">Four values we cook by</h2>
        <div class="value-list" style="margin-top:var(--space-l)">
          <article class="value-item">
            <p class="value-item__num" aria-hidden="true">01</p>
            <div><h3>Honest ingredients</h3><p>Whole spices, good single-origin oil, real dairy. If an ingredient is not good enough to eat at home, it does not go into the kitchen.</p></div>
          </article>
          <article class="value-item">
            <p class="value-item__num" aria-hidden="true">02</p>
            <div><h3>Time as an ingredient</h3><p>Slow cooking is not a marketing line for us. Chutneys are made the night before, gravies simmer for hours, and dum biryanis are sealed and left alone.</p></div>
          </article>
          <article class="value-item">
            <p class="value-item__num" aria-hidden="true">03</p>
            <div><h3>Warmth without fuss</h3><p>We remember names, we notice birthdays, and we never rush a table. Hospitality is the one thing you cannot fake on a menu.</p></div>
          </article>
          <article class="value-item">
            <p class="value-item__num" aria-hidden="true">04</p>
            <div><h3>Care for our team</h3><p>Fair wages, a four-day week for our kitchen team, and a proper break room. Good food comes from people who are looked after.</p></div>
          </article>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================= CHEF ============================= -->
<section class="section section--dark on-dark" aria-labelledby="chef-title">
  <div class="container">
    <div class="section-head section-head--center reveal">
      <p class="eyebrow">The kitchen</p>
      <h2 id="chef-title">Meet the people cooking your food</h2>
      <p class="lead">A small, senior team who have worked together for the better part of a decade.</p>
    </div>
    <div class="grid grid--3">
      <figure class="chef-card reveal">
        <div class="frame"><img src="assets/images/gallery-chef-800.webp" width="800" height="800" loading="lazy" decoding="async"
             alt="Chef Nikhil at the pass, plating a curry in the Spice Route kitchen."></div>
        <figcaption>
          <p class="chef-card__role">Head Chef &amp; Co-founder</p>
          <h3 style="font-size:var(--step-2)">Nikhil Raghav</h3>
          <p>Nikhil grew up between a family kitchen in Lucknow and his grandmother''s home in Bengaluru. He trained in Delhi, spent four years in Dubai, and came back to build the Spice Route menu from the recipes he grew up with.</p>
        </figcaption>
      </figure>
      <figure class="chef-card reveal" data-delay="1">
        <div class="frame"><img src="assets/images/gallery-spices-800.webp" width="800" height="800" loading="lazy" decoding="async"
             alt="Bowls of freshly ground spices and whole aromatics on the Spice Route masala station."></div>
        <figcaption>
          <p class="chef-card__role">Sous Chef &amp; Masala</p>
          <h3 style="font-size:var(--step-2)">Farhan Qureshi</h3>
          <p>Farhan runs the masala station and grinds every blend fresh each morning. He is the reason the kebabs taste different at lunch and at dinner, and he refuses to write any of it down.</p>
        </figcaption>
      </figure>
      <figure class="chef-card reveal" data-delay="2">
        <div class="frame"><img src="assets/images/gallery-interior-lounge-800.webp" width="800" height="800" loading="lazy" decoding="async"
             alt="A corner banquette in the dining room, dressed with cushions and lit by a brass floor lamp."></div>
        <figcaption>
          <p class="chef-card__role">Chef de Cuisine</p>
          <h3 style="font-size:var(--step-2)">Meera Iyer</h3>
          <p>Meera looks after the vegetarian side of the kitchen and the desserts. Thirty-one of our thirty-nine dishes pass through her section, which tells you what we think about paneer and vegetables.</p>
        </figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- ============================= INGREDIENTS ============================= -->
<section class="section" aria-labelledby="ingredients-title">
  <div class="container">
    <div class="split split--media-right">
      <div class="reveal">
        <p class="eyebrow">Sourcing</p>
        <h2 id="ingredients-title">Fresh, and we mean it</h2>
        <p class="lead" style="margin-top:1rem">Our kitchen gets its produce from the same three farms every week, and our fish from the Hebbal market before the doors close. We are not a farm-to-table restaurant in the fashionable sense — we simply buy from people we know, and we have for ten years.</p>
        <ul class="info-list">
          <li class="info-list__item">
            <span class="info-list__icon">__I_SPICE__</span>
            <span><span class="info-list__label">Daily</span><span class="info-list__value">All garam masala, chaat masala and kebab masala ground in-house, every morning before service.</span></span>
          </li>
          <li class="info-list__item">
            <span class="info-list__icon">__I_LEAF__</span>
            <span><span class="info-list__label">Three times a week</span><span class="info-list__value">Seasonal vegetables and herbs delivered from a single grower we have worked with since 2016.</span></span>
          </li>
          <li class="info-list__item">
            <span class="info-list__icon">__I_FIRE__</span>
            <span><span class="info-list__label">Live fire</span><span class="info-list__value">Breads, kebabs and clay-oven dishes cooked to order over hardwood charcoal.</span></span>
          </li>
        </ul>
        <div class="btn-row">
          <a class="btn btn--ghost" href="gallery.html">See the gallery</a>
        </div>
      </div>
      <div class="split__media frame-stack reveal" data-delay="1">
        <figure class="frame frame--landscape">
          <img src="assets/images/gallery-spices-800.webp" width="1200" height="960" loading="lazy" decoding="async"
               alt="Bowls of whole spices and freshly ground masala arranged on the Spice Route masala station.">
        </figure>
      </div>
    </div>
  </div>
</section>

<!-- ============================= ATMOSPHERE ============================= -->
<section class="section section--cream" aria-labelledby="atmosphere-title">
  <div class="container">
    <div class="section-head section-head--center reveal">
      <p class="eyebrow">The room</p>
      <h2 id="atmosphere-title">What it feels like here</h2>
      <p class="lead">Warm brass, deep colour and low light. Loud enough to be fun, quiet enough to talk.</p>
    </div>
    <div class="grid grid--3">
      <article class="card reveal">
        <div class="card__media"><img src="assets/images/gallery-interior-lounge-800.webp" width="800" height="600" loading="lazy" decoding="async"
             alt="A corner banquette lounge with a jaali screen and a glowing brass floor lamp."></div>
        <div class="card__body">
          <h3 class="card__title">Date-night corner</h3>
          <p class="card__text">A curved velvet banquette behind a hand-painted jaali screen, with its own brass lamp. The quietest corner of the room.</p>
        </div>
      </article>
      <article class="card reveal" data-delay="1">
        <div class="card__media"><img src="assets/images/gallery-interior-dining-800.webp" width="800" height="600" loading="lazy" decoding="async"
             alt="The long dining table laid with brass thali plates, wine glasses and lit candles."></div>
        <div class="card__body">
          <h3 class="card__title">Long-table dinners</h3>
          <p class="card__text">Six to twelve guests, one long table, and a set menu that changes with the market. The best way to eat here.</p>
        </div>
      </article>
      <article class="card reveal" data-delay="2">
        <div class="card__media"><img src="assets/images/gallery-tandoor-800.webp" width="800" height="600" loading="lazy" decoding="async"
             alt="The tandoor glowing orange as naan is pulled from the oven wall."></div>
        <div class="card__body">
          <h3 class="card__title">The open kitchen</h3>
          <p class="card__text">The tandoor sits in full view of the pass, so you can watch your kebabs and breads come off the fire.</p>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="cta-band on-dark" aria-labelledby="about-cta-title">
  <div class="container">
    <div class="cta-band__inner reveal">
      <p class="eyebrow">Come and see for yourself</p>
      <h2 id="about-cta-title">Pull up a chair</h2>
      <p class="lead">Walk in off Brigade Road, or book ahead if you would like a particular table or a quiet corner.</p>
      <div class="btn-row">
        <a class="btn btn--lg" href="contact.html#book">Book a table</a>
        <a class="btn btn--lg btn--ghost-light" data-site-field="whatsappHref" href="https://wa.me/919876543210">WhatsApp us</a>
      </div>
    </div>
  </div>
</section>'''

# ==========================================================================
# GALLERY
# ==========================================================================
def gallery_item(src, alt, caption, cat, label, wide=False, delay=None, thumb=None, big=None):
    """thumb/big default to the {name}-400.webp / {name}-800.webp pair."""
    name = src.replace(".jpg", "")
    if thumb is None:
        thumb = f"{name}-400.webp"
    if big is None:
        big = f"{name}-800.webp"
    cls = "gallery-item" + (" gallery-item--wide" if wide else "")
    d = f' data-delay="{delay}"' if delay else ""
    return f'''<button class="{cls}" type="button" data-lightbox="assets/images/{big}" data-caption="{caption}" data-category-label="{label}" data-category="{cat}" data-ratio="4 / 3" aria-label="View larger: {alt}"{d}>
        <img src="assets/images/{thumb}" alt="{alt}" width="400" height="300" loading="lazy" decoding="async">
        <span class="gallery-item__zoom" aria-hidden="true"><svg><use href="#i-zoom"></use></svg></span>
        <span class="gallery-item__caption"><strong>{caption}</strong><span>{label}</span></span>
      </button>'''

GALLERY = f'''<section class="page-banner on-dark">
  <div class="container">
    <div class="page-banner__inner">
      <p class="eyebrow">Inside Spice Route</p>
      <h1>Gallery</h1>
      <p class="lead">The room, the fire and the food. Select any photograph to view it larger.</p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="gallery-title">
  <div class="container">
    <div class="section-head section-head--split">
      <div class="section-head__text">
        <h2 id="gallery-title">A look around</h2>
        <p class="lead gallery-count">10 photographs</p>
      </div>
      <div class="filter-chips" role="group" aria-label="Filter photographs by category">
        <button class="chip gallery-filter" type="button" data-filter="all" aria-pressed="true">All</button>
        <button class="chip gallery-filter" type="button" data-filter="interior" aria-pressed="false">Interior</button>
        <button class="chip gallery-filter" type="button" data-filter="kitchen" aria-pressed="false">Kitchen</button>
        <button class="chip gallery-filter" type="button" data-filter="food" aria-pressed="false">Food</button>
      </div>
    </div>

    <div class="gallery-empty empty-state">
      <h3>Nothing in that category yet</h3>
      <p>Select “All” to see the complete gallery.</p>
    </div>

    <div class="gallery-grid" data-gallery>
      {gallery_item("gallery-interior-dining.jpg", "The main dining room with arched brass-lit niches and a candlelit long table", "The main dining room", "interior", "Interior", wide=True)}
      {gallery_item("gallery-tandoor.jpg", "A clay tandoor glowing with orange flame, naan blistering on the inner walls", "The charcoal tandoor", "kitchen", "Kitchen")}
      {gallery_item("dish-butter-chicken.jpg", "Butter chicken finished with cream and kasuri methi in a brass bowl", "Butter chicken", "food", "Food")}
      {gallery_item("gallery-spices.jpg", "Bowls of whole spices and freshly ground masala on a dark surface", "The masala station", "kitchen", "Kitchen")}
      {gallery_item("dish-biryani.jpg", "Hyderabadi chicken dum biryani with saffron rice, fried onions and mint", "Dum biryani", "food", "Food")}
      {gallery_item("gallery-interior-lounge.jpg", "A velvet corner banquette behind a hand-painted jaali screen", "The corner lounge", "interior", "Interior")}
      {gallery_item("gallery-chef.jpg", "A chef plating a curry at the kitchen pass under warm light", "At the pass", "kitchen", "Kitchen", wide=True)}
      {gallery_item("dish-paneer-tikka.jpg", "Paneer tikka shashlik skewers with charred peppers and onion", "Paneer tikka", "food", "Food")}
      {gallery_item("dish-halwa.jpg", "Gajar ka halwa in a dark ceramic bowl, topped with slivered almonds and khoya", "Gajar ka halwa", "food", "Food")}
      {gallery_item("hero.jpg", "A table set with brass bowls of curry, biryani, tikka skewers and naan under candlelight", "A table at Spice Route", "interior", "Interior", wide=True, thumb="hero-400.webp", big="hero-1600.webp")}
    </div>

    <p class="menu-note" style="margin-top:var(--space-xl)">
      <strong>Note for the demo.</strong> Every photograph on this site was generated for the project — no stock or third-party imagery is used. Swap the files in <code>assets/images/</code> for real photos of the restaurant and update the <code>alt</code> text at the same time.
    </p>
  </div>
</section>

<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photograph viewer">
  <div class="lightbox__bar">
    <span class="lightbox__counter" data-lightbox-counter>1 / 1</span>
    <button class="lightbox__close" type="button" data-lightbox-close aria-label="Close viewer (Escape)">
      <svg aria-hidden="true" focusable="false"><use href="#i-close"></use></svg>
    </button>
  </div>
  <div class="lightbox__stage">
    <button class="lightbox__nav lightbox__nav--prev" type="button" data-lightbox-prev aria-label="Previous photograph">
      <svg aria-hidden="true" focusable="false" style="transform:rotate(180deg)"><use href="#i-arrow"></use></svg>
    </button>
    <figure class="lightbox__figure">
      <img src="assets/images/gallery-interior-dining-800.webp" alt="" width="1200" height="800" data-lightbox-image>
      <figcaption class="lightbox__caption">
        <strong data-lightbox-title></strong>
        <span data-lightbox-meta></span>
      </figcaption>
    </figure>
    <button class="lightbox__nav lightbox__nav--next" type="button" data-lightbox-next aria-label="Next photograph">
      <svg aria-hidden="true" focusable="false"><use href="#i-arrow"></use></svg>
    </button>
  </div>
</div>

<section class="cta-band on-dark" aria-labelledby="gallery-cta-title">
  <div class="container">
    <div class="cta-band__inner reveal">
      <p class="eyebrow">Taste it properly</p>
      <h2 id="gallery-cta-title">Photographs only go so far</h2>
      <p class="lead">The dal is better hot, the naan is better straight off the fire, and the room is better in person.</p>
      <div class="btn-row">
        <a class="btn btn--lg" href="contact.html#book">Book a table</a>
        <a class="btn btn--lg btn--ghost-light" href="menu.html">View the menu</a>
      </div>
    </div>
  </div>
</section>'''

# ==========================================================================
# CONTACT
# ==========================================================================
CONTACT = '''<section class="page-banner on-dark">
  <div class="container">
    <div class="page-banner__inner">
      <p class="eyebrow">Get in touch</p>
      <h1>Contact &amp; Reservations</h1>
      <p class="lead">Book a table, ask about a private dinner, or just check whether we take walk-ins on a Friday. We are happy to help.</p>
    </div>
  </div>
</section>

<section class="section" id="book" aria-labelledby="contact-title">
  <div class="container">
    <div class="contact-grid">
      <!-- ======================= LEFT: DETAILS ======================= -->
      <div>
        <p class="eyebrow">Find &amp; reach us</p>
        <h2 id="contact-title">Come and find us</h2>
        <p class="lead" style="margin-top:.75rem">We are a two-minute walk from Indiranagar Metro, opposite the old bookshop on Brigade Road.</p>

        <div class="contact-list">
          <a class="contact-card" data-site-field="phoneHref" href="tel:+919876543210">
            <span class="contact-card__icon">__I_PHONE__</span>
            <span>
              <span class="contact-card__label">Call us</span>
              <span class="contact-card__value" data-site-field="phone">+91 98765 43210</span>
              <span class="contact-card__hint">We answer between 11:00 am and 11:30 pm</span>
            </span>
          </a>

          <a class="contact-card contact-card--wa" data-site-field="whatsappHref" href="https://wa.me/919876543210" target="_blank" rel="noopener">
            <span class="contact-card__icon">__I_WHATSAPP__</span>
            <span>
              <span class="contact-card__label">WhatsApp</span>
              <span class="contact-card__value" data-site-field="phone">+91 98765 43210</span>
              <span class="contact-card__hint">Fastest way to reserve — we usually reply within minutes</span>
            </span>
          </a>

          <a class="contact-card" data-site-field="emailHref" href="mailto:hello@spiceroute.example">
            <span class="contact-card__icon">__I_MAIL__</span>
            <span>
              <span class="contact-card__label">Email</span>
              <span class="contact-card__value" data-site-field="email">hello@spiceroute.example</span>
              <span class="contact-card__hint">For events, press and group bookings</span>
            </span>
          </a>

          <div class="contact-card">
            <span class="contact-card__icon">__I_PIN__</span>
            <span>
              <span class="contact-card__label">Address</span>
              <span class="contact-card__value" data-site-field="address">42, Saffron Street, Brigade Road, Indiranagar, Bengaluru 560038</span>
              <span class="contact-card__hint">Valet parking at the rear entrance</span>
            </span>
          </div>
        </div>

        <div style="margin-top:var(--space-l)">
          <div class="hours-card">
            <p class="hours-status" data-open-status><span class="dot" aria-hidden="true"></span> <span>Loading hours…</span></p>
            <h3 style="font-size:var(--step-1);margin-bottom:.5rem">Opening hours</h3>
            <dl class="hours-list" data-hours>
              <div class="hours-list__row"><dt>Monday – Thursday</dt><dd>12:00 pm – 10:30 pm</dd></div>
              <div class="hours-list__row"><dt>Friday – Saturday</dt><dd>12:00 pm – 11:30 pm</dd></div>
              <div class="hours-list__row"><dt>Sunday</dt><dd>12:00 pm – 10:00 pm</dd></div>
            </dl>
            <p class="hours-note">Kitchen closes 30 minutes before the restaurant. Walk-ins are always welcome, but we recommend booking at weekends.</p>
          </div>
        </div>

        <div class="map-embed" style="margin-top:var(--space-m)">
          <img src="assets/images/map-placeholder.svg" width="1200" height="750" loading="lazy" decoding="async"
               alt="Stylised map showing Spice Route on Brigade Road, Indiranagar, Bengaluru.">
          <div class="map-embed__overlay">
            <p><strong>Brigade Road</strong>Indiranagar, Bengaluru 560038</p>
            <a class="btn btn--sm" data-site-field="mapHref" href="https://www.google.com/maps/search/?api=1&amp;query=Brigade%20Road%2C%20Bengaluru" target="_blank" rel="noopener noreferrer">Get directions <svg class="arrow" style="width:1em;height:1em" aria-hidden="true"><use href="#i-arrow"></use></svg></a>
          </div>
        </div>
      </div>

      <!-- ======================= RIGHT: FORMS ======================= -->
      <div>
        <h2 id="forms-title">Book a table or send an enquiry</h2>
        <p class="lead" style="margin-top:.5rem;margin-bottom:var(--space-m)">Choose a tab below. This demo validates everything in the browser and then hands your details to WhatsApp or email — no data is sent to a server.</p>

        <div class="tabs__list" role="tablist" aria-label="Contact forms">
          <button class="tab" type="button" role="tab" id="tab-book" data-tab="book" aria-controls="panel-book" aria-selected="true" tabindex="0">Book a table</button>
          <button class="tab" type="button" role="tab" id="tab-enquiry" data-tab="enquiry" aria-controls="panel-enquiry" aria-selected="false" tabindex="-1">General enquiry</button>
        </div>

        <!-- ---------- BOOKING PANEL ---------- -->
        <section class="tab-panel" id="panel-book" role="tabpanel" aria-labelledby="tab-book" tabindex="0">
          <div class="form-card">
            <header>
              <h3>Reserve a table</h3>
              <p>Tell us when you are coming and we will confirm on WhatsApp. For groups of more than twelve, please call us instead.</p>
            </header>

            <form class="js-validate" data-booking novalidate>
              <div class="form-grid form-grid--2">
                <div class="field">
                  <label class="field__label" for="book-name">Full name <span class="req" aria-hidden="true">*</span></label>
                  <input class="field__control" type="text" id="book-name" name="name" autocomplete="name" required aria-describedby="book-name-error">
                  <p class="field__error" id="book-name-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
                <div class="field">
                  <label class="field__label" for="book-phone">Phone <span class="req" aria-hidden="true">*</span></label>
                  <input class="field__control" type="tel" id="book-phone" name="phone" autocomplete="tel" required aria-describedby="book-phone-error" placeholder="+91 98765 43210">
                  <p class="field__error" id="book-phone-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
                <div class="field">
                  <label class="field__label" for="booking-date">Date <span class="req" aria-hidden="true">*</span></label>
                  <input class="field__control" type="date" id="booking-date" name="date" required aria-describedby="book-date-error book-date-hint">
                  <p class="field__hint" id="book-date-hint">Lunch and dinner services daily.</p>
                  <p class="field__error" id="book-date-error"><svg aria-hidden="true" focusable="true"><use href="#i-alert"></use></svg><span></span></p>
                </div>
                <div class="field">
                  <label class="field__label" for="booking-time">Time <span class="req" aria-hidden="true">*</span></label>
                  <select class="field__control" id="booking-time" name="time" required aria-describedby="book-time-error">
                    <option value="">Select a time</option>
                    <optgroup label="Lunch">
                      <option>12:30 pm</option><option>1:00 pm</option><option>1:30 pm</option>
                      <option>2:00 pm</option><option>2:30 pm</option>
                    </optgroup>
                    <optgroup label="Dinner">
                      <option>6:30 pm</option><option>7:00 pm</option><option>7:30 pm</option>
                      <option>8:00 pm</option><option>8:30 pm</option><option>9:00 pm</option>
                    </optgroup>
                  </select>
                  <p class="field__error" id="book-time-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
                <div class="field">
                  <label class="field__label" for="booking-guests">Guests <span class="req" aria-hidden="true">*</span></label>
                  <select class="field__control" id="booking-guests" name="guests" required aria-describedby="book-guests-error">
                    <option value="">How many people?</option>
                    <option>1 guest</option><option>2 guests</option><option>3 guests</option>
                    <option>4 guests</option><option>5 guests</option><option>6 guests</option>
                    <option>7 guests</option><option>8 guests</option><option>10 guests</option><option>12 guests</option>
                  </select>
                  <p class="field__error" id="book-guests-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
                <div class="field">
                  <label class="field__label" for="book-occasion">Occasion</label>
                  <select class="field__control" id="book-occasion" name="occasion">
                    <option value="">None</option>
                    <option>Birthday</option><option>Anniversary</option><option>Business dinner</option>
                    <option>Date night</option><option>Family meal</option><option>Other</option>
                  </select>
                </div>
                <div class="field field--full">
                  <label class="field__label" for="book-email">Email <span class="field__hint" style="text-transform:none;letter-spacing:0">(optional)</span></label>
                  <input class="field__control" type="email" id="book-email" name="email" autocomplete="email" aria-describedby="book-email-error" placeholder="name@example.com">
                  <p class="field__error" id="book-email-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
                <div class="field field--full">
                  <label class="field__label" for="book-notes">Anything we should know? <span class="field__hint" style="text-transform:none;letter-spacing:0">(optional)</span></label>
                  <textarea class="field__control" id="book-notes" name="message" placeholder="Allergies, a high chair, a quiet table…"></textarea>
                </div>
                <div class="field field--full">
                  <label class="checkbox" for="book-consent">
                    <input type="checkbox" id="book-consent" name="consent" required aria-describedby="book-consent-error">
                    <span class="checkbox__text">I understand this is a demo website and my details will open in WhatsApp or your email app rather than being sent to a server. <span class="req" aria-hidden="true">*</span></span>
                  </label>
                  <p class="field__error" id="book-consent-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
              </div>
              <div class="form-actions">
                <button class="btn" type="submit">Request this table</button>
                <button class="btn btn--ghost btn--sm" type="reset" data-reset>Clear form</button>
                <p class="form-actions__note">We confirm every booking by WhatsApp. No deposit is needed.</p>
              </div>
            </form>

            <div class="form-success" aria-live="polite">
              <div class="form-success__icon"><svg aria-hidden="true" focusable="false"><use href="#i-check"></use></svg></div>
              <h3>Almost there — send it across</h3>
              <p>This demo has no back end, so use the button below to send your booking straight to the restaurant over WhatsApp.</p>
              <dl class="form-success__summary"></dl>
              <div class="btn-row" style="justify-content:center">
                <a class="btn btn--wa" data-whatsapp-send href="#">Send on WhatsApp</a>
                <a class="btn btn--ghost" data-mail-send href="#">Send by email instead</a>
              </div>
              <button class="link-arrow" type="button" style="margin-top:1.25rem;border:0;background:none;cursor:pointer" data-reset>Make another booking</button>
            </div>
          </div>
        </section>

        <!-- ---------- ENQUIRY PANEL ---------- -->
        <section class="tab-panel" id="panel-enquiry" role="tabpanel" aria-labelledby="tab-enquiry" tabindex="0" hidden>
          <div class="form-card">
            <header>
              <h3>Send us a message</h3>
              <p>For large groups, private events, press or anything else — fill this in and we will come back to you within a day.</p>
            </header>

            <form class="js-validate" novalidate>
              <div class="form-grid form-grid--2">
                <div class="field">
                  <label class="field__label" for="enq-name">Full name <span class="req" aria-hidden="true">*</span></label>
                  <input class="field__control" type="text" id="enq-name" name="name" autocomplete="name" required aria-describedby="enq-name-error">
                  <p class="field__error" id="enq-name-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
                <div class="field">
                  <label class="field__label" for="enq-phone">Phone <span class="req" aria-hidden="true">*</span></label>
                  <input class="field__control" type="tel" id="enq-phone" name="phone" autocomplete="tel" required aria-describedby="enq-phone-error" placeholder="+91 98765 43210">
                  <p class="field__error" id="enq-phone-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
                <div class="field">
                  <label class="field__label" for="enq-email">Email <span class="req" aria-hidden="true">*</span></label>
                  <input class="field__control" type="email" id="enq-email" name="email" autocomplete="email" required aria-describedby="enq-email-error" placeholder="name@example.com">
                  <p class="field__error" id="enq-email-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
                <div class="field">
                  <label class="field__label" for="enq-subject">Subject <span class="req" aria-hidden="true">*</span></label>
                  <select class="field__control" id="enq-subject" name="subject" required aria-describedby="enq-subject-error">
                    <option value="">Choose a topic</option>
                    <option>General enquiry</option>
                    <option>Private event / full table</option>
                    <option>Group booking (13+)</option>
                    <option>Corporate lunch</option>
                    <option>Press or collaboration</option>
                    <option>Careers</option>
                    <option>Something else</option>
                  </select>
                  <p class="field__error" id="enq-subject-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
                <div class="field field--full">
                  <label class="field__label" for="enq-message">Message <span class="req" aria-hidden="true">*</span></label>
                  <textarea class="field__control" id="enq-message" name="message" required aria-describedby="enq-message-error book-message-hint" placeholder="Tell us a little about what you need…"></textarea>
                  <p class="field__hint" id="book-message-hint">At least 10 characters, please.</p>
                  <p class="field__error" id="enq-message-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
                <div class="field field--full">
                  <label class="checkbox" for="enq-consent">
                    <input type="checkbox" id="enq-consent" name="consent" required aria-describedby="enq-consent-error">
                    <span class="checkbox__text">I understand this is a demo website and my details will open in WhatsApp or your email app rather than being sent to a server. <span class="req" aria-hidden="true">*</span></span>
                  </label>
                  <p class="field__error" id="enq-consent-error"><svg aria-hidden="true" focusable="false"><use href="#i-alert"></use></svg><span></span></p>
                </div>
              </div>
              <div class="form-actions">
                <button class="btn" type="submit">Send enquiry</button>
                <button class="btn btn--ghost btn--sm" type="reset" data-reset>Clear form</button>
                <p class="form-actions__note">We reply to every enquiry within one working day.</p>
              </div>
            </form>

            <div class="form-success" aria-live="polite">
              <div class="form-success__icon"><svg aria-hidden="true" focusable="false"><use href="#i-check"></use></svg></div>
              <h3>Thank you — send it across</h3>
              <p>This demo has no back end, so use the button below to send your message straight to the restaurant over WhatsApp.</p>
              <dl class="form-success__summary"></dl>
              <div class="btn-row" style="justify-content:center">
                <a class="btn btn--wa" data-whatsapp-send href="#">Send on WhatsApp</a>
                <a class="btn btn--ghost" data-mail-send href="#">Send by email instead</a>
              </div>
              <button class="link-arrow" type="button" style="margin-top:1.25rem;border:0;background:none;cursor:pointer" data-reset>Write another message</button>
            </div>
          </div>
        </section>

        <!-- ---------- FAQ ---------- -->
        <h3 style="margin-top:var(--space-xl);margin-bottom:.75rem">Good to know</h3>
        <div class="faq-list">
          <details class="faq">
            <summary class="faq__summary">Do you take walk-ins?</summary>
            <div class="faq__body">Always, subject to availability. We hold back a few tables for walk-ins on weekdays, but Friday and Saturday evenings are best booked ahead.</div>
          </details>
          <details class="faq">
            <summary class="faq__summary">Can you cater for allergies?</summary>
            <div class="faq__body">Tell your server before ordering and we will walk you through every dish. Our kitchen handles nuts, dairy and gluten, and we can usually adapt most gravies.</div>
          </details>
          <details class="faq">
            <summary class="faq__summary">Do you have vegetarian and vegan options?</summary>
            <div class="faq__body">Thirty-one of our thirty-nine dishes are vegetarian, and a good number of those are vegan as well. Look for the green marker on the menu.</div>
          </details>
          <details class="faq">
            <summary class="faq__summary">Can we book a private table?</summary>
            <div class="faq__body">Yes — we take a handful of private bookings each month. Pick “Private event” in the enquiry form and we will send you the full details.</div>
          </details>
        </div>
      </div>
    </div>
  </div>
</section>'''

# --------------------------------------------------------------------------
# Helpers for menu items
# --------------------------------------------------------------------------
def menu_item(cat, name, desc, price, kind, photo, alt):
    """Render a single <article class="menu-item"> from one MENU_ITEMS row."""
    tags = []
    if kind == "veg":
        tags.append('<span class="tag tag--veg">Vegetarian</span>')
    elif kind == "nonveg":
        tags.append('<span class="tag tag--nonveg">Non-veg</span>')
    if photo:
        tags.append('<span class="tag tag--chef">Chef\'s pick</span>')
    tags_html = f'<div class="tag-row menu-item__tags">{"".join(tags)}</div>' if tags else ""

    search = f"{name} {desc}".replace("&amp;", "and").replace("&mdash;", "-")
    cls = "menu-item" + (" menu-item--with-photo" if photo else "")
    pic = ""
    if photo:
        pic = ('<span class="menu-item__photo">'
               f'<img src="assets/images/menu-{cat}-400.webp" alt="{alt}" '
               'width="240" height="240" loading="lazy" decoding="async"></span>')
    veg_attr = "true" if kind == "veg" else "false"
    return f'''<article class="{cls}" data-category="{cat}" data-veg="{veg_attr}" data-search="{search}">
        {pic}
        <div class="menu-item__body">
          <div class="menu-item__head">
            <h3 class="menu-item__name">{name}<span class="menu-item__price">\u20b9{price}</span></h3>
          </div>
          <p class="menu-item__desc">{desc}</p>
          {tags_html}
        </div>
      </article>'''


# --------------------------------------------------------------------------
# PAGE TITLES & META DESCRIPTIONS
# --------------------------------------------------------------------------
TITLES = {
    "index.html": (
        "Spice Route | Authentic Indian Restaurant in Bengaluru",
        "Spice Route — Authentic Indian Flavours, Served With Soul",
        "Spice Route is a family-run Indian restaurant on Brigade Road, Bengaluru. Charcoal tandoor cooking, hand-ground masala and slow-simmered gravies. Book a table today.",
    ),
    "menu.html": (
        "Menu | Spice Route — Indian Dishes in Bengaluru",
        "The Spice Route Menu",
        "Browse the Spice Route menu: starters, main courses, breads, biryani, desserts and beverages. Over forty vegetarian dishes, with prices and dietary labels.",
    ),
    "about.html": (
        "About | Spice Route — Our Story, Chef & Kitchen",
        "About Spice Route",
        "Meet the family behind Spice Route, our head chef Nikhil Raghav, the values we cook by and how we source our ingredients on Brigade Road, Bengaluru.",
    ),
    "gallery.html": (
        "Gallery | Spice Route — Food & Interior Photographs",
        "Inside Spice Route",
        "Photographs of the Spice Route dining room, the charcoal tandoor, our masala station and the dishes we are known for.",
    ),
    "contact.html": (
        "Contact & Reservations | Spice Route, Bengaluru",
        "Book a table at Spice Route",
        "Book a table at Spice Route, 42 Saffron Street, Brigade Road, Bengaluru. Call, WhatsApp, send an enquiry or reserve online.",
    ),
}

# --------------------------------------------------------------------------
# RUN
# --------------------------------------------------------------------------
if __name__ == "__main__":
    print("Building Spice Route pages…")

    # icon substitution
    def ics(s):
        for n in ("fire", "chef", "pin", "spice", "leaf", "clock", "heart", "quote",
                  "phone", "whatsapp", "mail", "alert", "check"):
            s = s.replace(f"__I_{n.upper()}__", icon(n))
        s = s.replace("__STARS5__", icon("star") * 5)
        return s

    for var, filename in (("HOME", "index.html"), ("MENU", "menu.html"),
                          ("ABOUT", "about.html"), ("GALLERY", "gallery.html"),
                          ("CONTACT", "contact.html")):
        body = globals()[var]

        # expand @@ITEM@@<index> markers using MENU_ITEMS
        while "@@ITEM@@" in body:
            start = body.index("@@ITEM@@")
            end = body.index("\n", start)
            idx = int(body[start + len("@@ITEM@@"):end].strip())
            body = body[:start] + menu_item(**MENU_ITEMS[idx]) + body[end:]

        body = ics(body)
        title, og_title, description = TITLES[filename]
        render(
            filename,
            title=title,
            og_title=og_title,
            description=description,
            body=body,
            current=filename,
            extra_head=SCHEMA if filename in ("index.html", "contact.html") else "",
            body_class="page-home" if filename == "index.html" else "",
        )

    print("Done.")
