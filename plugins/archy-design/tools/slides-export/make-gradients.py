#!/usr/bin/env python3
"""Render every CSS gradient the dumps reference into a PNG.

pptxgenjs supports no gradient fills at all, so a gradient ground has to be embedded as a
bitmap - the same conclusion CLAUDE.md reaches for the dark layouts in the template
library. It stops being an editable shape, and that is unavoidable.

Interpolation is done in **Oklab**, because that is what the canvas says: Paper writes
`linear-gradient(in oklab ...)`. Lerping the same two blues in sRGB desaturates through
the middle and reads as a different ground - the exact reason the CSS asks for oklab.

Reads <work>/dump/*.json and writes <work>/assets/gradients ($ARCHY_WORK or --work=DIR;
see archywork.py). tokens.json is the tool's own.
"""
import io, os, re, sys, glob, hashlib
from PIL import Image

import sys; sys.dont_write_bytecode = True   # never write __pycache__ into the plugin folder

import archywork

DIR = archywork.WORK
OUT = os.path.join(DIR, "assets", "gradients")
GRAD_RE = re.compile(r"linear-gradient\([^()]*(?:\([^()]*\)[^()]*)*\)")


# ---- sRGB <-> Oklab (Björn Ottosson)
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _srgb(c):
    c = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return max(0, min(255, round(c * 255)))

def to_oklab(rgb):
    r, g, b = (_lin(v) for v in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)

def from_oklab(lab):
    L, a, b = lab
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (_srgb(+4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s),
            _srgb(-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s),
            _srgb(-0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s))


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def render(css, tokens, w, h, path):
    oklab = " in oklab" in css or "(in oklab" in css
    angle = 180
    m = re.search(r"(-?[\d.]+)deg", css)
    if m:
        angle = float(m.group(1))
    if angle % 180 != 0:
        raise SystemExit("only vertical gradients are handled: %s" % css)

    stops = []
    for colour, pos in re.findall(r"(var\(--[a-z0-9-]+\)|#[0-9a-fA-F]{3,8})\s*([\d.]+)%", css):
        c = tokens[re.search(r"--[a-z0-9-]+", colour).group(0)] if colour.startswith("var") else colour
        stops.append((float(pos) / 100.0, hexrgb(c)))
    if len(stops) < 2:
        raise SystemExit("could not parse two stops from: %s" % css)
    stops.sort()

    down = angle == 180                       # 180deg runs top -> bottom in CSS
    img = Image.new("RGB", (1, h))
    px = img.load()
    for y in range(h):
        t = (y / (h - 1)) if down else 1 - (y / (h - 1))
        # Before the first stop and after the last, the colour is flat - which is what
        # makes a 0%..55% gradient sit on solid colour for its bottom 45%.
        if t <= stops[0][0]:
            px[0, y] = stops[0][1]
            continue
        if t >= stops[-1][0]:
            px[0, y] = stops[-1][1]
            continue
        for i in range(len(stops) - 1):
            (p0, c0), (p1, c1) = stops[i], stops[i + 1]
            if p0 <= t <= p1:
                f = (t - p0) / (p1 - p0) if p1 > p0 else 0
                if oklab:
                    a, b = to_oklab(c0), to_oklab(c1)
                    px[0, y] = from_oklab(tuple(a[k] + (b[k] - a[k]) * f for k in range(3)))
                else:
                    px[0, y] = tuple(round(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))
                break
    img.resize((w, h), Image.NEAREST).save(path)


def main():
    os.makedirs(OUT, exist_ok=True)
    tokens = {}
    import json
    for k, v in json.load(io.open(archywork.here("tokens.json"), encoding="utf-8")).items():
        tokens[k] = v
    seen, made = set(), 0
    for f in sorted(glob.glob(os.path.join(DIR, "dump", "*.json"))):
        for css in GRAD_RE.findall(io.open(f, encoding="utf-8").read()):
            key = hashlib.sha1(css.encode()).hexdigest()[:12]
            if key in seen:
                continue
            seen.add(key)
            path = os.path.join(OUT, key + ".png")
            if os.path.exists(path):
                continue
            render(css, tokens, 1920, 1080, path)
            print("  %s  %s" % (key, css[:70]))
            made += 1
    print("gradients: %d rendered, %d already there" % (made, len(seen) - made))


if __name__ == "__main__":
    main()
