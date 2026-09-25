#!/usr/bin/env python3
"""Generate the raster assets the .pptx needs, from source.

Google Slides cannot take SVG, so the Hugeicons used by `09 · Product grid` and
`14 · Matrix` have to go in as PNG. Rather than exporting them out of Paper by hand
(Paper writes to ~/Downloads, which macOS TCC blocks from scripts), this pulls the
icon geometry straight from the npm package - the same source CLAUDE.md documents for
getting Hugeicons onto a canvas - so the assets are reproducible from the repo.

    python build-assets.py

Writes <work>/assets/*.svg and *.png at 256px ($ARCHY_WORK or --work=DIR; see
archywork.py). A pre-built copy of this output ships with the tool in assets-base/, which
build.js falls back to, so this only needs running to change or add an icon. The
Hugeicons tarball is cached once in the shared base directory.

The Archy wordmark for `01 · Cover` is NOT generated here: it is a brand asset that
lives on the Paper canvas, and hand-typing its path data is exactly the mistake
CLAUDE.md warns about. Export it from Paper and drop it in as assets/archy-wordmark.png
- see the README.
"""
import os
import re
import subprocess
import sys
import tarfile
import urllib.request

import cairosvg
from PIL import Image

import sys; sys.dont_write_bytecode = True   # never write __pycache__ into the plugin folder

import archywork

ASSETS = archywork.work("assets")
TARBALL = os.path.join(archywork.BASE, ".hugeicons.tgz")

ROYAL, NEUTRAL, TINT300 = "#013DF5", "#AAAAAA", "#66BFFF"

# 09's row 1 is shipped (royal blue) and row 2 is roadmap (neutral-light) - the icon
# colour reinforces the Status pill. 14 sits on the dark ground, so all blue-tint-300.
PLAN = [
    ("icon-scribe",    "Note02Icon",            ROYAL),
    ("icon-revenue",   "Invoice01Icon",         ROYAL),
    ("icon-imaging",   "DentalToothIcon",       ROYAL),
    ("icon-verify",    "ShieldCheckIcon",       NEUTRAL),
    ("icon-insight",   "Analytics01Icon",       NEUTRAL),
    ("icon-connect",   "BubbleChatIcon",        NEUTRAL),
    ("icon-pms",       "DashboardSquare01Icon", TINT300),
    ("icon-payments",  "CreditCardIcon",        TINT300),
    ("icon-insurance", "ShieldCheckIcon",       TINT300),
    ("icon-staffing",  "UserGroupIcon",         TINT300),
    ("icon-financing", "BankIcon",              TINT300),
    ("icon-hardware",  "Package01Icon",         TINT300),
    # Icon List needs royal-blue variants of two icons the Product grid draws in
    # neutral: there every cell carries a state, here none of them do.
    ("icon-verify-royal",  "ShieldCheckIcon",   ROYAL),
    ("icon-insight-royal", "Analytics01Icon",   ROYAL),
]

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" '
       'viewBox="0 0 24 24" fill="none" stroke="{colour}" stroke-width="1.5" '
       'stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')


def fetch():
    if os.path.exists(TARBALL):
        return
    url = subprocess.run(
        ["npm", "view", "@hugeicons/core-free-icons", "dist.tarball"],
        capture_output=True, text=True, check=True).stdout.strip()
    print(f"downloading {url}")
    urllib.request.urlretrieve(url, TARBALL)


def paths_for(tar, name):
    """Pull the `d` attributes out of one icon module.

    The module's attribute keys are UNQUOTED JS, not JSON - `{ d: "M20.99...", ... }` -
    so a regex looking for `"d":` matches nothing and silently yields empty paths.
    Every element ends with a `key` property, which makes a reliable terminator.
    """
    src = tar.extractfile(f"package/dist/esm/{name}.js").read().decode()
    out = []
    for tag, attrs in re.findall(r'\["(\w+)",\s*\{(.*?)\s*key:', src, re.S):
        if tag != "path":
            raise SystemExit(f"{name}: unexpected element <{tag}>, needs handling")
        d = re.search(r'd:\s*"([^"]*)"', attrs)
        if not d or not d.group(1):
            raise SystemExit(f"{name}: empty path data")
        out.append(f'<path d="{d.group(1)}"/>')
    if not out:
        raise SystemExit(f"{name}: no paths found")
    return "".join(out)


# The Archy wordmark, copied verbatim out of the Paper canvas via get_jsx - 5 paths in a
# translate(0 21.752) group, viewBox "0 5 252 98", ink 252 x 98. Do NOT take it from the
# Webflow index.html: that inline SVG is missing the counter of the "A" and renders as
# "∩rchy". The aspect ratio 252/98 matches its 360 x 140 placement on the Cover exactly.
WORDMARK_PATHS = [
    "M81.301 51.629C81.301 51.629 69.056 51.629 69.056 51.629 69.056 51.629 69.056 23.733 69.056 23.733 69.056 11.492 78.938 1.531 91.085 1.531 91.085 1.531 94.726 1.531 94.726 1.531 94.726 1.531 94.726 13.873 94.726 13.873 94.726 13.873 91.085 13.873 91.085 13.873 85.688 13.873 81.301 18.296 81.301 23.733 81.301 23.733 81.301 51.629 81.301 51.629Z",
    "M173.905 4.314C169.558 4.314 165.48 5.526 161.948 7.639 161.948 7.639 161.948-16.752 161.948-16.752 161.948-16.752 149.682-16.752 149.682-16.752 149.682-16.752 149.682 51.629 149.682 51.629 149.682 51.629 161.948 51.629 161.948 51.629 161.948 51.629 161.948 29.727 161.948 29.727 161.948 22.533 167.315 16.678 173.905 16.678 180.496 16.678 185.862 22.533 185.862 29.727 185.862 29.727 185.862 51.629 185.862 51.629 185.862 51.629 198.13 51.629 198.13 51.629 198.13 51.629 198.13 29.727 198.13 29.727 198.13 15.717 187.264 4.317 173.905 4.317 173.905 4.317 173.905 4.314 173.905 4.314Z",
    "M239.734 7.748C239.734 7.748 239.734 27.015 239.734 27.015 239.734 34.482 234.367 40.554 227.776 40.554 221.185 40.554 215.819 34.482 215.819 27.015 215.819 27.015 215.819 7.748 215.819 7.748 215.819 7.748 203.552 7.748 203.552 7.748 203.552 7.748 203.552 27.015 203.552 27.015 203.552 41.293 214.418 52.91 227.776 52.91 232.124 52.91 236.202 51.672 239.734 49.52 239.734 49.52 239.734 55.856 239.734 55.856 239.734 63.045 234.367 68.896 227.776 68.896 221.185 68.896 215.819 63.05 215.819 55.856 215.819 55.856 203.552 55.856 203.552 55.856 203.552 69.858 214.418 81.248 227.776 81.248 241.134 81.248 252 69.858 252 55.856 252 55.856 252 7.748 252 7.748 252 7.748 239.734 7.748 239.734 7.748Z",
    "M120.418 40.305C113.428 40.305 107.737 34.308 107.737 26.942 107.737 19.574 113.428 13.577 120.418 13.577 125.88 13.577 130.549 17.239 132.328 22.358 132.328 22.358 144.982 22.358 144.982 22.358 142.88 10.324 132.667 1.166 120.418 1.166 106.649 1.166 95.449 12.729 95.449 26.945 95.449 41.163 106.649 52.726 120.418 52.726 132.667 52.726 142.88 43.567 144.982 31.534 144.982 31.534 132.328 31.534 132.328 31.534 130.549 36.653 125.88 40.315 120.418 40.315 120.418 40.315 120.418 40.305 120.418 40.305Z",
    "M12.283 47.429C12.283 36.978 20.72 28.478 31.093 28.478 41.466 28.478 49.903 36.978 49.903 47.429 49.903 47.429 49.903 51.629 49.903 51.629 49.903 51.629 62.186 51.629 62.186 51.629 62.186 51.629 62.186 14.569 62.186 14.569 62.186 9.389 60.905 4.249 58.474-0.285 53.027-10.441 42.538-16.752 31.088-16.752 30.508-16.752 29.923-16.735 29.342-16.704 18.848-16.115 9.439-10.281 4.165-1.096 3.808-0.476 3.468 0.166 3.154 0.811 1.063 5.12 0 9.749 0 14.569 0 14.569 0 51.629 0 51.629 0 51.629 12.283 51.629 12.283 51.629 12.283 51.629 12.283 47.429 12.283 47.429ZM12.283 14.569C12.283 11.647 12.924 8.851 14.185 6.251 14.375 5.861 14.581 5.471 14.796 5.098 17.988-0.463 23.684-3.996 30.026-4.351 30.379-4.373 30.74-4.382 31.093-4.382 38.02-4.382 44.366-0.563 47.662 5.588 49.129 8.327 49.903 11.43 49.903 14.569 49.903 14.569 49.903 22.509 49.903 22.509 44.676 18.496 38.158 16.108 31.093 16.108 24.029 16.108 17.51 18.496 12.283 22.509 12.283 22.509 12.283 14.569 12.283 14.569Z",
]

WORDMARK_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="560" '
    'viewBox="0 5 252 98"><g transform="translate(0 21.752)">{paths}</g></svg>'
)


def wordmark():
    paths = "".join(f'<path d="{d}" fill="#FFFFFF"/>' for d in WORDMARK_PATHS)
    svg = WORDMARK_SVG.format(paths=paths)
    with open(os.path.join(ASSETS, "archy-wordmark.svg"), "w") as f:
        f.write(svg)
    cairosvg.svg2png(bytestring=svg.encode(),
                     write_to=os.path.join(ASSETS, "archy-wordmark.png"),
                     output_width=1440, output_height=560)
    print("  archy-wordmark.png")



# The scrim on `Capture + Scrim` - the one raster the deck genuinely needs. pptxgenjs
# supports no gradient fills at all, so a CSS `BK Fade` cannot survive as a shape; it goes
# in as a PNG. Transparent at the top, fully --color-dark-background by 65% of its height,
# which is CLAUDE.md's rule that the gradient must reach full opacity BEFORE the art ends.
FADE_W, FADE_H, FADE_STOP = 1920, 680, 0.65
DARK_BG = (0, 0, 78)  # #00004E


def bk_fade():
    img = Image.new("RGBA", (1, FADE_H), (0, 0, 0, 0))
    px = img.load()
    stop = int(FADE_H * FADE_STOP)
    for y in range(FADE_H):
        a = 255 if y >= stop else round(255 * y / stop)
        px[0, y] = (*DARK_BG, a)
    img = img.resize((FADE_W, FADE_H), Image.NEAREST)
    img.save(os.path.join(ASSETS, "bk-fade-dark.png"))
    print("  bk-fade-dark.png")


def main():
    os.makedirs(ASSETS, exist_ok=True)
    os.makedirs(os.path.dirname(TARBALL), exist_ok=True)
    fetch()
    wordmark()
    bk_fade()
    with tarfile.open(TARBALL) as tar:
        names = {n.rsplit("/", 1)[-1][:-3] for n in tar.getnames()
                 if re.match(r"package/dist/esm/\w+Icon\.js$", n)}
        for out, key, colour in PLAN:
            if key not in names:
                raise SystemExit(f"{key} is not a real icon name")
            svg = SVG.format(colour=colour, paths=paths_for(tar, key))
            with open(os.path.join(ASSETS, out + ".svg"), "w") as f:
                f.write(svg)
            cairosvg.svg2png(bytestring=svg.encode(),
                             write_to=os.path.join(ASSETS, out + ".png"),
                             output_width=256, output_height=256)
            print(f"  {out}.png")
    print(f"\n{len(PLAN)} icons + the wordmark + the scrim written to assets/")


if __name__ == "__main__":
    sys.exit(main())
