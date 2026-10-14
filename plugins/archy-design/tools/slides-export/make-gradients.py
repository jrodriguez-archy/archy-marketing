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
import io, os, re, sys, glob, hashlib, math
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


STOP_RE = re.compile(r"(var\(--[a-z0-9-]+\)|#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|oklab\([^)]*\)|transparent)"
                     r"\s*(-?[\d.]+%)?")


def colour(c, tokens):
    """A stop colour as (r, g, b, alpha 0-1). Tokens, hex with alpha, rgb(a) and the
    oklab(L a b / A) Paper writes for a transparent stop."""
    c = c.strip()
    if c.startswith("var"):
        c = tokens[re.search(r"--[a-z0-9-]+", c).group(0)]
    if c == "transparent":
        return (0, 0, 0, 0.0)
    if c.startswith("#"):
        h = c[1:]
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return hexrgb(h[:6]) + (a,)
    nums = re.findall(r"-?[\d.]+%?", c)
    num = lambda s, scale=1: float(s[:-1]) / 100 * scale if s.endswith("%") else float(s)
    if c.startswith("rgb"):
        a = num(nums[3], 1) if len(nums) > 3 else 1.0
        return (round(num(nums[0], 255)), round(num(nums[1], 255)), round(num(nums[2], 255)), a)
    if c.startswith("oklab"):
        L = num(nums[0], 1)
        a = num(nums[3], 1) if len(nums) > 3 else 1.0
        return from_oklab((L, float(nums[1]), float(nums[2]))) + (a,)
    raise SystemExit("unreadable gradient colour: %s" % c)


def parse(css, tokens):
    angle = 180.0                              # CSS default: top -> bottom
    m = re.match(r"linear-gradient\(\s*(?:in \w+\s*)?(-?[\d.]+)deg", css)
    if m:
        angle = float(m.group(1))
    elif "to top" in css:
        angle = 0.0
    body = css[css.index("(") + 1:-1]
    stops = [(colour(c, tokens), float(p[:-1]) / 100 if p else None)
             for c, p in STOP_RE.findall(body)]
    if len(stops) < 2:
        raise SystemExit("could not parse two stops from: %s" % css)
    # A stop with no position sits evenly between its neighbours (first 0, last 1).
    if stops[0][1] is None:
        stops[0] = (stops[0][0], 0.0)
    if stops[-1][1] is None:
        stops[-1] = (stops[-1][0], 1.0)
    i = 0
    while i < len(stops):
        if stops[i][1] is None:
            j = i
            while stops[j][1] is None:
                j += 1
            p0, p1 = stops[i - 1][1], stops[j][1]
            for k in range(i, j):
                stops[k] = (stops[k][0], p0 + (p1 - p0) * (k - i + 1) / (j - i + 1))
            i = j
        i += 1
    return angle, " in oklab" in css or "(in oklab" in css, stops


def sample(stops, oklab, t):
    """Colour at t along the line, interpolated premultiplied (as CSS does), so a fade to
    transparent does not pass through grey."""
    if t <= stops[0][1]:
        return stops[0][0]
    if t >= stops[-1][1]:
        return stops[-1][0]
    for (c0, p0), (c1, p1) in zip(stops, stops[1:]):
        if p0 <= t <= p1:
            f = (t - p0) / (p1 - p0) if p1 > p0 else 0
            a0, a1 = c0[3], c1[3]
            a = a0 + (a1 - a0) * f
            if a <= 0:
                return (0, 0, 0, 0.0)
            v0 = to_oklab(c0[:3]) if oklab else c0[:3]
            v1 = to_oklab(c1[:3]) if oklab else c1[:3]
            v = tuple((v0[k] * a0 + (v1[k] * a1 - v0[k] * a0) * f) / a for k in range(3))
            rgb = from_oklab(v) if oklab else tuple(max(0, min(255, round(x))) for x in v)
            return rgb + (a,)
    return stops[-1][0]


def render_layer(css, tokens, w, h):
    angle, oklab, stops = parse(css, tokens)
    if angle % 180 == 0:
        # Vertical: one exact column, stretched sideways (the common ground and scrim).
        col = Image.new("RGBA", (1, h))
        px = col.load()
        for y in range(h):
            t = y / (h - 1) if angle == 180 else 1 - y / (h - 1)
            r, g, b, a = sample(stops, oklab, t)
            px[0, y] = (r, g, b, round(a * 255))
        return col.resize((w, h), Image.NEAREST)
    # Any other angle, per CSS: the gradient line runs through the centre at `angle`
    # (0deg points up, clockwise) and is long enough that the corners hit 0% and 100%.
    # Rendered at a quarter of the size and scaled up; the ramp is smooth, so nothing shows.
    sw, sh = max(2, w // 4), max(2, h // 4)
    rad = math.radians(angle)
    dx, dy = math.sin(rad), -math.cos(rad)
    length = abs(w * dx) + abs(h * dy)
    img = Image.new("RGBA", (sw, sh))
    px = img.load()
    for j in range(sh):
        y = (j + 0.5) * h / sh - h / 2
        for i in range(sw):
            x = (i + 0.5) * w / sw - w / 2
            r, g, b, a = sample(stops, oklab, (x * dx + y * dy) / length + 0.5)
            px[i, j] = (r, g, b, round(a * 255))
    return img.resize((w, h), Image.BILINEAR)


def render(layers, tokens, w, h, path):
    """CSS paints the FIRST layer on top, so composite from the last one up."""
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for css in reversed(layers):
        out = Image.alpha_composite(out, render_layer(css, tokens, w, h))
    if out.getextrema()[3][0] == 255:
        out = out.convert("RGB")             # opaque ground: no alpha channel needed
    out.save(path)


def main():
    import json
    os.makedirs(OUT, exist_ok=True)
    tokens = json.load(io.open(archywork.here("tokens.json"), encoding="utf-8"))
    seen, made = set(), 0
    for f in sorted(glob.glob(os.path.join(DIR, "dump", "*.json"))):
        dump = json.load(io.open(f, encoding="utf-8"))
        for s in (dump.get("styles") or {}).values():
            layers = GRAD_RE.findall(str(s.get("backgroundImage") or ""))
            if not layers:
                continue
            # Same key as paper2spec's gradientPath(): every layer joined with ", ".
            key = hashlib.sha1(", ".join(layers).encode()).hexdigest()[:12]
            if key in seen:
                continue
            seen.add(key)
            path = os.path.join(OUT, key + ".png")
            if os.path.exists(path):
                continue
            size = lambda v, d: int(float(v[:-2])) if isinstance(v, str) and v.endswith("px") else d
            render(layers, tokens, size(s.get("width"), 1920), size(s.get("height"), 1080), path)
            print("  %s  %d layer(s)  %s" % (key, len(layers), layers[0][:60]))
            made += 1
    print("gradients: %d rendered, %d already there" % (made, len(seen) - made))


if __name__ == "__main__":
    main()
