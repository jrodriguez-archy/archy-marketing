#!/usr/bin/env python3
"""Rasterise an SVG lifted out of Paper with get_jsx.

Google Slides takes no SVG, so anything vector on a slide - the mascota, a logo, an icon -
has to be embedded as a bitmap. The markup is copied verbatim rather than redrawn:
CLAUDE.md's rule is never to hand-type path data, because a wrong `d` renders a plausible
broken shape. get_jsx returns React attribute spellings, so the only edit is turning those
back into SVG ones.

    python jsx2png.py <in.jsx> <out.png> [scale] [size]

A relative <in.jsx> is looked up in the current directory, then in the work directory; a
relative <out.png> always lands in the work directory ($ARCHY_WORK or --work=DIR; see
archywork.py), never beside this script.
"""
import io, os, re, sys
import sys; sys.dont_write_bytecode = True   # never write __pycache__ into the plugin folder
import archywork
import cairosvg
from PIL import Image

# React spelling -> SVG spelling. Anything left camelCase is silently ignored by the
# renderer, which is how a gradient or a fill-rule goes missing without an error.
ATTRS = [
    ("fillRule", "fill-rule"), ("clipRule", "clip-rule"), ("clipPath", "clip-path"),
    ("strokeWidth", "stroke-width"), ("strokeLinecap", "stroke-linecap"),
    ("strokeLinejoin", "stroke-linejoin"), ("strokeDasharray", "stroke-dasharray"),
    ("strokeOpacity", "stroke-opacity"), ("fillOpacity", "fill-opacity"),
    ("stopColor", "stop-color"), ("stopOpacity", "stop-opacity"),
    ("gradientTransform", "gradientTransform"), ("gradientUnits", "gradientUnits"),
    ("xmlnsXlink", "xmlns:xlink"), ("xlinkHref", "xlink:href"),
]


def to_svg(jsx):
    m = re.search(r"<svg[\s\S]*</svg>", jsx)
    if not m:
        raise SystemExit("no <svg> element found")
    svg = m.group(0)
    svg = re.sub(r'\sclassName="[^"]*"', "", svg)
    svg = re.sub(r"\sstyle=\{\{[^}]*\}\}", "", svg)
    for a, b in ATTRS:
        svg = svg.replace(a + "=", b + "=")
    # A token cannot resolve outside Paper; a var() fill renders as black. Substitute
    # from the same tokens.json the exporter uses, so a colour cannot drift between the
    # canvas and the deck.
    import json
    tokens = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "tokens.json"), encoding="utf-8"))
    for name, value in tokens.items():
        svg = svg.replace("var(%s)" % name, value)
    if "var(--" in svg:
        raise SystemExit("unresolved token in the markup: %s" %
                         re.search(r"var\(--[a-z0-9-]+\)", svg).group(0))
    return svg


def main():
    src, out = archywork.input_path(sys.argv[1]), archywork.output_path(sys.argv[2])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    scale = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
    svg = to_svg(io.open(src, encoding="utf-8").read())
    # An icon's width/height ATTRIBUTES are often stale: Paper overrides them in an inline
    # style the JSX carries and this strips. Pass the size the tree reports instead.
    if len(sys.argv) > 4:
        w = h = float(sys.argv[4])
    else:
        w = float(re.search(r'width="([\d.]+)"', svg).group(1))
        h = float(re.search(r'height="([\d.]+)"', svg).group(1))
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out,
                     output_width=int(w * scale), output_height=int(h * scale))
    im = Image.open(out).convert("RGBA")
    ink = sum(1 for p in im.get_flattened_data() if p[3] > 10)
    if ink == 0:
        raise SystemExit("rendered blank - the paths did not survive the conversion")
    print("%s  %dx%d  ink px %d" % (out, im.width, im.height, ink))


if __name__ == "__main__":
    main()
