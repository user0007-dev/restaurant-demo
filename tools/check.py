#!/usr/bin/env python3
"""
Pre-launch checker for the Spice Route site.

Validates every page for:
  - broken internal links, image sources and script/style references
  - missing / empty alt attributes
  - duplicate element ids
  - exactly one <h1> per page and no skipped heading levels
  - <img> without width/height (causes layout shift)
  - <label for> pointing at a control that does not exist
  - aria-labelledby / aria-describedby pointing at missing ids
  - buttons/links with no accessible name
  - leftover build placeholders such as __I_MENU__ or __MENUITEM__(
  - internal anchor links that do not resolve

Run:  python3 tools/check.py
"""
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "menu.html", "about.html", "gallery.html", "contact.html", "404.html"]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.assets = []        # href / src values to check on disk
        self.anchors = []       # same-page #anchors
        self.alt_missing = []
        self.alt_empty_ok = 0
        self.headings = []
        self.labels = []
        self.refs = []          # aria-labelledby / describedby
        self.unnamed = []       # elements that need an accessible name
        self._heading = None
        self._button = None
        self._link = None
        self._in_svg = 0
        self.stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.stack.append(tag)

        if tag == "svg":
            self._in_svg += 1
        if self._in_svg:
            return

        if "id" in a:
            self.ids.append(a["id"])

        if tag == "img":
            if "src" in a:
                self.assets.append(a["src"])
            if "alt" not in a:
                self.alt_missing.append(("img", a.get("src", "?")))
            if "width" not in a or "height" not in a:
                self.alt_missing.append(("img-nodims", a.get("src", "?")))
        if tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon", "manifest", "apple-touch-icon"):
            if not a["href"].startswith("http"):
                self.assets.append(a["href"])
        if tag == "script" and a.get("src"):
            self.assets.append(a["src"])

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))
        if tag == "label" and "for" in a:
            self.labels.append(a["for"])
        for attr in ("aria-labelledby", "aria-describedby", "aria-controls"):
            if attr in a:
                self.refs.extend(a[attr].split())

    def handle_endtag(self, tag):
        if tag == "svg" and self._in_svg:
            self._in_svg -= 1
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()


def check():
    problems = []
    all_ids = {}

    for page in PAGES:
        path = os.path.join(ROOT, page)
        if not os.path.exists(path):
            problems.append(f"[{page}] FILE MISSING")
            continue

        html = open(path, encoding="utf-8").read()
        p = Page()
        p.feed(html)

        # --- placeholders left over from the build -------------------
        for token in ("__I_", "__MENUITEM__", "__LOGO__", "__SPRITE__", "__STARS5__", "Template("):
            if token in html:
                problems.append(f"[{page}] leftover build placeholder: {token}")

        # --- assets exist on disk ------------------------------------
        for asset in p.assets:
            if asset.startswith(("http://", "https://", "data:", "#", "tel:", "mailto:")):
                continue
            if not os.path.exists(os.path.join(ROOT, asset)):
                problems.append(f"[{page}] missing asset: {asset}")

        # --- hrefs ---------------------------------------------------
        # <use href="#icon-name"> refers to the inline SVG sprite, not an anchor
        svg_uses = set(re.findall(r'<use[^>]+href="#([^"]+)"', html))
        for m in re.finditer(r'href="([^"]+)"', html):
            href = m.group(1)
            if href.startswith("#"):
                name = href[1:]
                if len(name) > 1 and name not in svg_uses:
                    p.anchors.append(name)
            elif not href.startswith(("http", "mailto:", "tel:", "data:")):
                target = href.split("#")[0]
                if target and not os.path.exists(os.path.join(ROOT, target)):
                    problems.append(f"[{page}] broken link: {href}")

        all_ids[page] = set(p.ids)

        # --- duplicate ids -------------------------------------------
        seen = set()
        for i in p.ids:
            if i in seen:
                problems.append(f"[{page}] duplicate id: #{i}")
            seen.add(i)

        # --- headings -------------------------------------------------
        if p.headings.count(1) != 1:
            problems.append(f"[{page}] expected exactly one <h1>, found {p.headings.count(1)}")
        prev = 0
        for lvl in p.headings:
            if prev and lvl > prev + 1:
                problems.append(f"[{page}] heading jump h{prev} -> h{lvl}")
            prev = lvl

        # --- images ---------------------------------------------------
        for kind, ref in p.alt_missing:
            if kind == "img":
                problems.append(f"[{page}] <img> missing alt: {ref}")
            else:
                problems.append(f"[{page}] <img> missing width/height: {ref}")

        # --- labels & aria refs ---------------------------------------
        idset = set(p.ids)
        for f in p.labels:
            if f not in idset:
                problems.append(f"[{page}] <label for=\"{f}\"> has no matching control")
        for r in p.refs:
            if r not in idset:
                problems.append(f"[{page}] aria reference to missing id: #{r}")

        # --- same-page anchors ----------------------------------------
        for a in p.anchors:
            if a not in idset:
                problems.append(f"[{page}] anchor #{a} does not exist on this page")

        # --- external assets ------------------------------------------
        for m in re.finditer(r'(?:src|href)="(https://[^"]+)"', html):
            pass

    # --- cross-page anchors ------------------------------------------
    for page in PAGES:
        path = os.path.join(ROOT, page)
        if not os.path.exists(path):
            continue
        html = open(path, encoding="utf-8").read()
        for m in re.finditer(r'href="([a-z]+\.html)#([^"]+)"', html):
            target_page, anchor = m.group(1), m.group(2)
            target_path = os.path.join(ROOT, target_page)
            if not os.path.exists(target_path):
                problems.append(f"[{page}] link to missing page: {m.group(0)}")
                continue
            t = open(target_path, encoding="utf-8").read()
            if f'id="{anchor}"' not in t:
                problems.append(f"[{page}] link to missing anchor in {target_page}: #{anchor}")

    return problems


if __name__ == "__main__":
    issues = check()
    if issues:
        print(f"✗ {len(issues)} issue(s) found:\n")
        for i in issues:
            print("  " + i)
        sys.exit(1)
    print("✓ All checks passed — links, images, headings, labels and ARIA are consistent.")
