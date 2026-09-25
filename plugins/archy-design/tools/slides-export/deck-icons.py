#!/usr/bin/env python3
"""Rasterise the deck's Hugeicons into PNGs the .pptx can embed.

Google Slides cannot take SVG, so every icon on a slide has to arrive as a bitmap. The
path data is copied verbatim out of Paper with `get_jsx` on the icon's SVG node - never
retyped: CLAUDE.md's rule is that a hand-typed `d` renders a plausible-looking broken icon,
and it has produced one before.

Icons are 56px on the canvas (CLAUDE.md: 56 across this deck, not the arithmetic 32) and
render at 4x so they stay crisp when Slides scales them.
"""
import io, os, json, hashlib
import cairosvg

import sys; sys.dont_write_bytecode = True   # never write __pycache__ into the plugin folder

import archywork   # writes <work>/assets/deck, never beside this file

DIR = archywork.WORK
OUT = os.path.join(DIR, "assets", "deck")
SCALE = 4
SIZE = 56

ROYAL = "#013DF5"
TINT3 = "#66BFFF"
GREY_L = "#AAAAAA"
WHITE = "#FFFFFF"

# name -> (stroke colour, [path d, ...])
ICONS = {
    "look-back": (ROYAL, [
        "M5.438 19.55C6.549 20.516 7.891 21.251 9.41 21.658C10.275 21.889 11.145 22 12 22M16.537 20.906C17.697 20.314 18.739 19.499 19.595 18.5M21.656 14.585C21.935 13.544 22.04 12.498 21.987 11.477M20.91 7.461C20.699 7.046 20.459 6.646 20.192 6.265M16.47 3.053C15.88 2.759 15.252 2.519 14.59 2.342C9.257 0.915 3.775 4.082 2.344 9.415C1.783 11.505 1.928 13.618 2.632 15.5",
        "M12 6V12L16 14",
    ]),
    "why-now": (ROYAL, [
        "M5.226 11.329L12.224 2.347C12.771 1.644 13.797 2.081 13.797 3.017V9.97C13.797 10.53 14.2 10.985 14.696 10.985H18.1C18.873 10.985 19.285 12.015 18.774 12.671L11.776 21.654C11.229 22.356 10.203 21.919 10.203 20.983V14.03C10.203 13.47 9.8 13.015 9.304 13.015H5.9C5.127 13.015 4.715 11.985 5.226 11.329Z",
    ]),
    "look-ahead": (ROYAL, [
        "M15.879 3L10.283 3C7.321 3 5.84 3 4.92 3.879C4 4.757 4 6.172 4 9L4.106 15L15.879 15C18.102 15 19.213 15 19.685 14.425C19.815 14.267 19.911 14.084 19.966 13.889C20.164 13.184 19.497 12.335 18.163 10.636L18.163 10.636C17.608 9.93 17.331 9.577 17.281 9.175C17.267 9.059 17.267 8.941 17.281 8.825C17.331 8.423 17.608 8.07 18.163 7.364L18.163 7.364C19.497 5.665 20.164 4.816 19.966 4.111C19.911 3.916 19.815 3.733 19.685 3.574C19.213 3 18.102 3 15.879 3L15.879 3Z",
        "M4 21L4 8",
    ]),
}

TMPL = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{px}" '
        'height="{px}" fill="none" stroke="{c}" stroke-width="1.5" '
        'stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (colour, ds) in ICONS.items():
        for d in ds:
            # The silent failure of the extraction route is an empty `d`, which renders a
            # blank square that looks like a spacing bug rather than a missing icon.
            if not d.strip():
                raise SystemExit("icon %s has an empty path" % name)
        paths = "".join('<path d="%s"/>' % d for d in ds)
        svg = TMPL.format(px=SIZE, c=colour, paths=paths)
        path = os.path.join(OUT, name + ".png")
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=path,
                         output_width=SIZE * SCALE, output_height=SIZE * SCALE)
        print("  %-16s %s" % (name, os.path.relpath(path, DIR)))


if __name__ == "__main__":
    main()
