#!/usr/bin/env python3
"""
Asset pipeline for the Spice Route demo.

Converts the raw source images in assets/images/raw/ into web-ready WebP
files at several widths, plus the Open Graph cover and the raster fallback
for the map. Everything is stripped of metadata and written at a quality
that keeps the whole gallery under ~15 KB per image.

Run:  python3 tools/images.py
"""
import os
import subprocess
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "assets", "images", "raw")
OUT = os.path.join(ROOT, "assets", "images")

# name -> (widths to emit, crop aspect for the "square-ish" menu thumbs)
IMAGES = {
    "hero":                    [400, 800, 1200, 1600],
    "dish-butter-chicken":     [400, 800],
    "dish-biryani":            [400, 800],
    "dish-paneer-tikka":       [400, 800],
    "dish-halwa":              [400, 800],
    "gallery-interior-dining": [400, 800, 1200],
    "gallery-interior-lounge": [400, 800],
    "gallery-spices":          [400, 800],
    "gallery-chef":            [400, 800],
    "gallery-tandoor":         [400, 800],
}

# Menu-section thumbnails are square crops of the matching photograph.
MENU_THUMBS = {
    "menu-starters":  ("dish-paneer-tikka",    "Paneer tikka skewers over charcoal"),
    "menu-mains":     ("dish-butter-chicken", "Butter chicken in a brass bowl"),
    "menu-breads":    ("gallery-tandoor",      "Naan blistering on the tandoor wall"),
    "menu-rice":      ("dish-biryani",         "Hyderabadi dum biryani with saffron"),
    "menu-desserts":  ("dish-halwa",           "Gajar ka halwa topped with almonds"),
}
# NOTE: there is deliberately no thumbnail for menu-beverages. The Beverages
# category is presented without photographs — see the note in menu.html.
# To turn thumbnails back on, drop a photo in raw/gallery-drinks.jpg and
# add "menu-beverages": ("gallery-drinks", "…") here.

WEBP_Q = 78
JPG_Q = 82


def run(args):
    subprocess.run(args, check=True)


def build(name, widths, source=None):
    src = os.path.join(RAW, f"{source or name}.jpg")
    if not os.path.exists(src):
        print(f"  ! missing source: {os.path.basename(src)}  (skipped {name})")
        return False
    for w in widths:
        dst = os.path.join(OUT, f"{name}-{w}.webp")
        run([
            "convert", src,
            "-auto-orient",
            "-resize", f"{w}x{w}>",
            "-strip",
            "-quality", str(WEBP_Q),
            "-define", "webp:method=6",
            dst,
        ])
    return True


def main():
    print("Building images…")

    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    built = set()
    for name, widths in IMAGES.items():
        if build(name, widths):
            built.add(name)

    # Square 240px crops for the menu page
    for name, (src, _alt) in MENU_THUMBS.items():
        source = os.path.join(RAW, f"{src}.jpg")
        if not os.path.exists(source):
            print(f"  ! missing source for {name}: {src}")
            continue
        run([
            "convert", source,
            "-auto-orient",
            "-resize", "400x400^",
            "-gravity", "center",
            "-extent", "400x400",
            "-strip",
            "-quality", str(WEBP_Q),
            "-define", "webp:method=6",
            os.path.join(OUT, f"{name}-400.webp"),
        ])

    # Open Graph / social share card: 1200x630 crop of the hero
    hero = os.path.join(RAW, "hero.jpg")
    if os.path.exists(hero):
        run([
            "convert", hero,
            "-auto-orient",
            "-resize", "1200x630^",
            "-gravity", "center",
            "-extent", "1200x630",
            "-strip",
            "-quality", "84",
            os.path.join(OUT, "og-cover.jpg"),
        ])

    total = 0
    count = 0
    for f in sorted(glob.glob(os.path.join(OUT, "*.webp")) + glob.glob(os.path.join(OUT, "*.jpg"))):
        total += os.path.getsize(f)
        count += 1
    print(f"  {count} files, {total/1024:.0f} KB total")
    print("Done.")


if __name__ == "__main__":
    main()
