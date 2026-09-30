#!/usr/bin/env python3
"""
Contrast audit for the Spice Route palette (WCAG 2.1).
Checks every foreground/background pair actually used in style.css
against the AA thresholds: 4.5:1 for body text, 3:1 for large text/UI.

Run:  python3 tools/contrast.py
"""


def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)


def ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# (label, foreground, background, minimum, note)
PAIRS = [
    ("Body text on page",        "#241e1a", "#fbf7f0", 4.5, "main copy"),
    ("Muted text on page",       "#6a5d52", "#fbf7f0", 4.5, "descriptions"),
    ("Muted text on cream-soft", "#6a5d52", "#f4ece0", 4.5, "notes"),
    ("Body text on white card",  "#241e1a", "#ffffff", 4.5, "card copy"),
    ("Gold-deep link on page",   "#876013", "#fbf7f0", 4.5, "arrow links"),
    ("Gold-deep on cream-soft", "#876013", "#f4ece0", 4.5, "menu note link"),
    ("Price gold-deep on white", "#876013", "#ffffff", 4.5, "dish prices"),
    ("Veg tag green on page",    "#5f7a4a", "#fbf7f0", 4.5, "vegetarian tag"),
    ("Chilli red on page",       "#a8321c", "#fbf7f0", 4.5, "non-veg tag"),
    ("Error red on white",       "#a8321c", "#ffffff", 4.5, "form errors"),
    ("Field label muted",        "#6a5d52", "#ffffff", 4.5, "form labels"),
    ("Placeholder on cream",     "#8a7b6c", "#f4ece0", 3.0, "placeholder"),
    ("Body on dark",             "#f6efe4", "#0d0b09", 4.5, "hero copy"),
    ("Muted on dark",            "#c3b6a4", "#0d0b09", 4.5, "footer body"),
    ("Gold-light on dark",       "#e9c67e", "#0d0b09", 4.5, "gold on dark"),
    ("Gold on dark soft",        "#c9962f", "#17130f", 4.5, "button on dark band"),
    ("Muted on dark soft band",  "#c3b6a4", "#17130f", 4.5, "cta band body"),
    ("Gold-light on footer",     "#e9c67e", "#0d0b09", 4.5, "footer headings"),
    ("Button ink on gold",       "#0d0b09", "#c9962f", 4.5, "primary button"),
    ("Button ink on gold-light", "#0d0b09", "#e9c67e", 4.5, "dark section button"),
    ("WhatsApp white on green",  "#ffffff", "#1aa74b", 3.0, "WhatsApp FAB (UI)"),
    ("WhatsApp white on deep gr","#ffffff", "#1a7a44", 4.5, "WhatsApp button"),
    ("Social icon on dark",      "#c3b6a4", "#0d0b09", 4.5, "social icons"),
    ("Focus ring on page",       "#8f6415", "#fbf7f0", 3.0, "focus outline (UI)"),
    ("Focus ring on dark",       "#e9c67e", "#0d0b09", 3.0, "focus outline dark"),
    ("Saffron tag on page",      "#b05715", "#fbf7f0", 4.5, "chef's pick tag"),
]

if __name__ == "__main__":
    print("WCAG 2.1 contrast audit\n")
    print(f"  {'pair':30s} {'ratio':>7s}  {'min':>5s}  result")
    print("  " + "-" * 66)
    failures = 0
    for label, fg, bg, minimum, note in PAIRS:
        r = ratio(fg, bg)
        ok = r >= minimum
        if not ok:
            failures += 1
        flag = "PASS" if ok else "FAIL"
        print(f"  {label:30s} {r:6.2f}:1  {minimum:4.1f}  {flag}  ({note})")

    print()
    if failures:
        print(f"✗ {failures} pair(s) below the required contrast")
        raise SystemExit(1)
    print("✓ All colour pairs meet WCAG AA")
