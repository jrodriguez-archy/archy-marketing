#!/usr/bin/env python3
"""Archy pixel textures: Pixel Gradients (PNG, seamless video loop, web) and Pixel Effects (photos).

    pixel.py gradient list                               the nine gradients and their tokens
    pixel.py gradient png   <name|all> [--size 3456x1944]    static background (2x of 1728x972)
    pixel.py gradient video <name|all> [--seconds 8] [--fps 30] [--size 1920x1080]
                                  [--format mp4|webm]   seamless loop, needs ffmpeg
    pixel.py gradient frames <name> [--count 4]              poster frames of the loop (t = 0, 1/n, ...)
    pixel.py gradient web   <name|all>                       <Dithering> snippet for a React site
    pixel.py gradient webflow                                the Webflow custom-code script (all nine)
    pixel.py effect dissolve --size WxH [--start Y] [--photo cutout.png --photo-rect x,y,w,h]
    pixel.py effect behind   --size WxH [--gradient sky] [--photo ...]
    pixel.py effect tone     <photo> --size WxH [--gradient ice --invert]

Every value (cell size, steps, colours, density, where an effect starts) is a starting
point and a flag, so each piece can be tuned and still reproduced.

One definition per gradient (presets.json): a base token and a front colour that moves
`amount` of the way toward a second token. PNG, video and web all read that same table, so
the three outputs match.

How a frame is made:
1. A soft field from six Gaussian blobs (the same six for every gradient, so they read as
   one family), normalised to 0..1. `gamma` > 1 pushes the field down so the base colour
   dominates (Pure White).
2. Ordered 8x8 Bayer dithering over `steps` + 1 colour levels between base and front, on a
   grid of `size` px cells (8.8 CSS px at 2x, as the Paper Shaders `size` prop).
3. For video, each blob centre travels a closed ellipse whose period is the loop length, so
   the last frame leads straight back into the first: seamless by construction. The dither
   grid stays fixed on screen, which is what gives the gentle pixel shimmer.

Output goes to --out DIR, else $ARCHY_WORK, else ${CLAUDE_PLUGIN_DATA}/pixel, else
./archy-work/pixel. Needs Python 3 and Pillow; `video` also needs ffmpeg on the PATH.
"""
import argparse
import json
import math
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True   # never write __pycache__ into the plugin folder

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is missing: python3 -m pip install --user pillow")

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "presets.json")) as fh:
    PRESETS = json.load(fh)
RECIPE = PRESETS["recipe"]
TOKENS = PRESETS["tokens"]
BY_NAME = {g["name"]: g for g in PRESETS["gradients"]}

ORBIT = 0.10          # how far a blob centre travels in a loop (fraction of the frame)


def bayer(n=8):
    m = [[0, 2], [3, 1]]
    while len(m) < n:
        k = len(m)
        m = [[4 * m[y % k][x % k] + [0, 2, 3, 1][(y // k) * 2 + (x // k)]
              for x in range(2 * k)] for y in range(2 * k)]
    return [[(v + 0.5) / (n * n) for v in row] for row in m]


B8 = bayer(8)


def rgb(hexcode):
    h = hexcode.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexcode(c):
    return "#%02X%02X%02X" % tuple(int(round(v)) for v in c)


def colours(g):
    """Base and front colour of a gradient, as RGB tuples."""
    b = rgb(TOKENS[g["base"]])
    t = rgb(TOKENS[g["toward"]])
    a = g["amount"]
    return b, tuple(b[i] + (t[i] - b[i]) * a for i in range(3))


def palette(g):
    b, f = colours(g)
    n = RECIPE["steps"]
    return [tuple(int(round(b[c] + (f[c] - b[c]) * i / n)) for c in range(3)) for i in range(n + 1)]


def percentile(sorted_vals, p):
    pos = p / 100 * (len(sorted_vals) - 1)
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


class Field:
    """The blob field on a grid of gw x gh cells, at loop phase t (0..1)."""

    def __init__(self, gw, gh):
        self.gw, self.gh = gw, gh
        s = RECIPE["scale"]
        self.bw, self.bh = round(gw * s), round(gh * s)
        self.m = max(self.bw, self.bh)
        self.ox, self.oy = (self.bw - gw) // 2, (self.bh - gh) // 2
        self.norm = None

    def raw(self, t):
        bw, bh, m = self.bw, self.bh, self.m
        blobs = []
        for k, (x, y, r, a) in enumerate(RECIPE["blobs"]):
            ph = k * 1.7
            d = 1 if k % 2 == 0 else -1
            ang = 2 * math.pi * t * d + ph
            dx = ORBIT * (math.cos(ang) - math.cos(ph))
            dy = ORBIT * 0.8 * (math.sin(ang) - math.sin(ph))
            blobs.append(((x + dx) * bw / m, (y + dy) * bh / m, 2 * r * r, a))
        out = []
        for j in range(self.oy, self.oy + self.gh):
            yy = j / m
            row = []
            for i in range(self.ox, self.ox + self.gw):
                xx = i / m
                v = 0.0
                for cx, cy, s2, a in blobs:
                    v += a * math.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / s2)
                row.append(v)
            out.append(row)
        return out

    def at(self, t):
        f = self.raw(t)
        if self.norm is None:
            # Normalise once, on the first frame, so a loop never breathes in brightness.
            # (Computed on the full uncropped field, as the original static renders were.)
            full = Field.__new__(Field)
            full.__dict__.update(self.__dict__)
            full.gw, full.gh, full.ox, full.oy = self.bw, self.bh, 0, 0
            vals = sorted(v for row in full.raw(0.0) for v in row)
            self.norm = (percentile(vals, 2), percentile(vals, 98))
        lo, hi = self.norm
        return [[min(1.0, max(0.0, (v - lo) / (hi - lo))) for v in row] for row in f]


def grid_size(w, h, cell):
    return round(w / cell), round(h / cell)


def render(g, field_vals, w, h):
    pal = palette(g)
    n = RECIPE["steps"]
    gamma = g.get("gamma", 1.0)
    gh, gw = len(field_vals), len(field_vals[0])
    img = Image.new("RGB", (gw, gh))
    px = img.load()
    for j in range(gh):
        brow = B8[j % 8]
        for i in range(gw):
            v = field_vals[j][i] ** gamma
            idx = min(n, max(0, int(math.floor(v * n + brow[i % 8]))))
            px[i, j] = pal[idx]
    return img.resize((w, h), Image.NEAREST)


def targets(name):
    if name == "all":
        return PRESETS["gradients"]
    if name not in BY_NAME:
        sys.exit("unknown gradient %r. Try: %s, all" % (name, ", ".join(BY_NAME)))
    return [BY_NAME[name]]


def parse_size(s):
    w, h = s.lower().split("x")
    return int(w), int(h)


def out_dir(args):
    d = args.out or os.environ.get("ARCHY_WORK") or (
        os.path.join(os.environ["CLAUDE_PLUGIN_DATA"], "pixel") if os.environ.get("CLAUDE_PLUGIN_DATA")
        else os.path.join(os.getcwd(), "archy-work", "pixel"))
    os.makedirs(d, exist_ok=True)
    return d


def cell_for(w, size_arg):
    # `size` is CSS px at a 2x render, like the shader: 8.8 -> 17.6 px cells on a 3456 px PNG.
    # For a 1x frame (video at 1920 wide) the cell is 8.8 px. Scale by width vs the 2x baseline.
    return RECIPE["size"] * 2 * (w / 3456) if size_arg is None else size_arg


def cmd_list(args):
    for g in PRESETS["gradients"]:
        b, f = colours(g)
        mix = g["toward"] if g["amount"] == 1 else "%d%% toward %s" % (g["amount"] * 100, g["toward"])
        print("%-11s %-6s %-20s -> %-30s %s %s" % (g["name"], g["group"], g["base"], mix, hexcode(b), hexcode(f)))


def cmd_png(args):
    w, h = parse_size(args.size)
    gw, gh = grid_size(w, h, cell_for(w, args.cell))
    vals = Field(gw, gh).at(0.0)
    d = out_dir(args)
    for g in targets(args.name):
        p = os.path.join(d, "%s-pixel-subtle.png" % g["name"])
        render(g, vals, w, h).save(p, optimize=True)
        print(p)


def cmd_frames(args):
    w, h = parse_size(args.size)
    gw, gh = grid_size(w, h, cell_for(w, args.cell))
    field = Field(gw, gh)
    d = out_dir(args)
    for g in targets(args.name):
        for k in range(args.count):
            p = os.path.join(d, "%s-frame-%d.png" % (g["name"], k))
            render(g, field.at(k / args.count), w, h).save(p, optimize=True)
            print(p)


def cmd_video(args):
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is missing: brew install ffmpeg (or ffmpeg.org), then run again")
    w, h = parse_size(args.size)
    gw, gh = grid_size(w, h, cell_for(w, args.cell))
    field = Field(gw, gh)
    total = int(round(args.seconds * args.fps))
    gs = targets(args.name)
    d = out_dir(args)
    codec = (["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "12", "-preset", "slow", "-movflags", "+faststart"]
             if args.format == "mp4" else
             ["-c:v", "libvpx-vp9", "-pix_fmt", "yuv420p", "-crf", "18", "-b:v", "0"])
    procs = {}
    for g in gs:
        p = os.path.join(d, "%s-loop.%s" % (g["name"], args.format))
        procs[g["name"]] = (p, subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
             "-s", "%dx%d" % (w, h), "-r", str(args.fps), "-i", "-"] + codec + [p],
            stdin=subprocess.PIPE))
    for k in range(total):
        vals = field.at(k / total)          # frame `total` would equal frame 0: never rendered
        for g in gs:
            procs[g["name"]][1].stdin.write(render(g, vals, w, h).tobytes())
        if k % args.fps == 0:
            print("frame %d/%d" % (k, total), file=sys.stderr)
    for p, proc in procs.values():
        proc.stdin.close()
        proc.wait()
        print(p)


def cmd_web(args):
    for g in targets(args.name):
        b, f = colours(g)
        print("// %s: %s -> %s" % (g["label"], g["base"],
              g["toward"] if g["amount"] == 1 else "%d%% toward %s" % (g["amount"] * 100, g["toward"])))
        print("<Dithering colorBack=\"%s\" colorFront=\"%s\" shape=\"warp\" type=\"8x8\" size={%s}\n"
              "  speed={0.2} scale={%s} style={{ position: 'fixed', inset: 0, zIndex: -1 }} />\n"
              % (hexcode(b), hexcode(f), RECIPE["size"], RECIPE["scale"]))


WEBFLOW_JS = """<script type="module">
  // Archy pixel gradients: animates every element with data-archy-gradient="<name>"
  import { ShaderMount, ditheringFragmentShader as fs, getShaderColorFromString as c }
    from 'https://cdn.jsdelivr.net/npm/@paper-design/shaders@0.0.81/dist/index.js';
  const G = {
%s
  };
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-archy-gradient]').forEach((el, i) => {
    const [back, front] = G[el.dataset.archyGradient] || G['royal-blue'];
    new ShaderMount(el, fs, {
      u_colorBack: c(back), u_colorFront: c(front),
      u_shape: 2, u_type: 4, u_pxSize: %s, u_scale: %s,
      u_fit: 0, u_rotation: 0, u_offsetX: 0, u_offsetY: 0,
      u_originX: 0.5, u_originY: 0.5, u_worldWidth: 0, u_worldHeight: 0,
    }, undefined, still ? 0 : 0.2, i * 7000);
  });
</script>"""


def cmd_webflow(args):
    rows = []
    for g in PRESETS["gradients"]:
        b, f = colours(g)
        rows.append("    '%s': ['%s', '%s']," % (g["name"], hexcode(b), hexcode(f)))
    print(WEBFLOW_JS % ("\n".join(rows), RECIPE["size"], RECIPE["scale"]))


# ---------------------------------------------------------------------------
# Pixel Effects (the 03 · Pixel Effects artboard on the Textures page)
#
# Every treatment shares one rule with the gradients: one grain per piece. The
# gradient behind the photo and the treatment cells sit on the same grid, the
# grid divides the frame exactly, and it is anchored to the bleed edge so no
# row is cut at the trim. Sizes are the frame's size on the canvas (CSS px);
# files are written at --scale (2x by default).

import random

LIGHT_CELLS = ["blue-tint-300", "white", "sky-blue-400", "blue-tint-200"]
DARK_CELLS = ["blue-tint-800", "royal-blue-500", "sky-blue-400", "blue-tint-300"]
LIGHT_GROUNDS = {"ice", "pure-white", "white", "mist"}


def token_list(csv, gradient):
    if csv:
        names = [t.strip() for t in csv.split(",") if t.strip()]
    else:
        names = DARK_CELLS if gradient in LIGHT_GROUNDS else LIGHT_CELLS
    bad = [n for n in names if n not in TOKENS]
    if bad:
        sys.exit("unknown token(s) %s. Known: %s" % (", ".join(bad), ", ".join(TOKENS)))
    return [rgb(TOKENS[n]) for n in names]


def grid_for(w, h, cell):
    gw, gh = grid_size(w, h, cell)
    return gw, gh, w / gw, h / gh


def ground(gradient, w, h, cell):
    """The gradient rendered on the treatment's grid (w, h and cell already scaled)."""
    g = targets(gradient)[0]
    gw, gh = grid_size(w, h, cell)
    return render(g, Field(gw, gh).at(0.0), w, h).convert("RGBA")


def paste_cell(img, gx, gy, cw, ch, colour):
    box = (round(gx * cw), round(gy * ch), round((gx + 1) * cw), round((gy + 1) * ch))
    img.paste(Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), colour + (255,)), box[:2])


def load_cutout(path):
    im = Image.open(path).convert("RGBA")
    if im.getchannel("A").getextrema()[0] == 255:
        print("warning: %s has no transparency; the treatments expect a cut-out" % path, file=sys.stderr)
    return im


def place_photo(canvas, photo, rect, k):
    """rect = x,y,w,h of the photo box on the canvas (CSS px), contain + bottom aligned like Paper."""
    x, y, w, h = [float(v) for v in rect.split(",")]
    s = min(w * k / photo.width, h * k / photo.height)
    f = photo.resize((round(photo.width * s), round(photo.height * s)), Image.LANCZOS)
    ox = round(x * k + (w * k - f.width) / 2)
    oy = round(y * k + h * k - f.height)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(f, (ox, oy), f)       # handles boxes that bleed past the frame
    canvas.alpha_composite(layer)


def cmd_photo_dissolve(args):
    w, h = parse_size(args.size); k = args.scale
    W2, H2, C = round(w * k), round(h * k), args.cell * k
    gw, gh, cw, ch = grid_for(W2, H2, C)
    edge = args.edge if args.edge is not None else h
    last = round(edge * k / ch)
    first = int((args.start if args.start is not None else edge * 0.8) * k / ch) + 1
    if not 0 < first < last <= gh:
        sys.exit("the effect needs --start above --edge, inside the frame")
    cols = token_list(args.colours, args.gradient)
    over = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); rnd = random.Random(args.seed); span = last - first
    for gy in range(first, last):
        p = args.density * ((gy - first + 1) / span) ** args.curve
        for gx in range(gw):
            if rnd.random() < p:
                paste_cell(over, gx, gy, cw, ch, rnd.choice(cols))
    d = out_dir(args)
    bg = ground(args.gradient, W2, H2, C)
    bg.convert("RGB").save(os.path.join(d, "dissolve-ground.png"), optimize=True)
    over.save(os.path.join(d, "dissolve-overlay.png"), optimize=True)
    preview = bg.copy()
    if args.photo:
        place_photo(preview, load_cutout(args.photo), args.photo_rect or "0,0,%d,%d" % (w, h), k)
    preview.alpha_composite(over)
    preview.convert("RGB").save(os.path.join(d, "dissolve-preview.png"), optimize=True)
    print("\n".join(os.path.join(d, n) for n in ("dissolve-ground.png", "dissolve-overlay.png", "dissolve-preview.png")))
    print("grid %d x %d cells, effect rows %d to %d" % (gw, gh, first, last), file=sys.stderr)


def cmd_photo_behind(args):
    w, h = parse_size(args.size); k = args.scale
    W2, H2, C = round(w * k), round(h * k), args.cell * k
    gw, gh, cw, ch = grid_for(W2, H2, C)
    cols = token_list(args.colours or "blue-tint-800,royal-blue-500,blue-tint-200", args.gradient)
    band = ground(args.gradient, W2, H2, C); n = len(cols)
    for gy in range(gh):
        f = max(0.0, (gy / gh - args.start) / (1 - args.start))
        for gx in range(gw):
            t = B8[gy % 8][gx % 8]
            if f > t:
                paste_cell(band, gx, gy, cw, ch, cols[min(n - 1, int(t / f * n))])
    d = out_dir(args)
    band.convert("RGB").save(os.path.join(d, "behind-ground.png"), optimize=True)
    out = [os.path.join(d, "behind-ground.png")]
    if args.photo:
        prev = band.copy(); place_photo(prev, load_cutout(args.photo), args.photo_rect or "0,0,%d,%d" % (w, h), k)
        prev.convert("RGB").save(os.path.join(d, "behind-preview.png"), optimize=True); out.append(os.path.join(d, "behind-preview.png"))
    print("\n".join(out))


def cmd_photo_tone(args):
    g = targets(args.gradient)[0]
    base, front = colours(g)
    if args.invert:
        base, front = front, base
    w, h = parse_size(args.size); k = args.scale
    W2, H2 = round(w * k), round(h * k)
    src = ImageOps.fit(Image.open(args.photo).convert("RGB"), (W2, H2), Image.LANCZOS)
    cell = max(1, round(args.cell * k)); gw, gh = W2 // cell, H2 // cell
    L = ImageOps.autocontrast(src.resize((gw, gh), Image.LANCZOS).convert("L"), cutoff=1).load()
    n = args.steps; pal = [tuple(round(base[c] + (front[c] - base[c]) * i / n) for c in range(3)) for i in range(n + 1)]
    out = Image.new("RGB", (gw, gh)); px = out.load()
    for y in range(gh):
        for x in range(gw):
            px[x, y] = pal[min(n, max(0, int(math.floor(L[x, y] / 255 * n + B8[y % 8][x % 8]))))]
    p = os.path.join(out_dir(args), "tone-%s.png" % args.gradient)
    out.resize((W2, H2), Image.NEAREST).save(p, optimize=True); print(p)


def main():
    ap = argparse.ArgumentParser(description="Archy pixel textures: Pixel Gradients and Pixel Effects")
    fam = ap.add_subparsers(dest="family", required=True)

    # Pixel Gradients
    gp = fam.add_parser("gradient", help="Pixel Gradients: backgrounds made from scratch")
    sub = gp.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("webflow")
    for c, size in (("png", "3456x1944"), ("video", "1920x1080"), ("frames", "1728x972"), ("web", None)):
        p = sub.add_parser(c)
        p.add_argument("name")
        if size:
            p.add_argument("--size", default=size)
            p.add_argument("--cell", type=float, default=None, help="cell size in px (default 8.8 at 2x, scaled with the width)")
            p.add_argument("--steps", type=int, default=None, help="tone steps between base and front (default %d)" % RECIPE["steps"])
            p.add_argument("--out", default=None)
        if c == "video":
            p.add_argument("--seconds", type=float, default=8)
            p.add_argument("--fps", type=int, default=30)
            p.add_argument("--format", choices=["mp4", "webm"], default="mp4")
        if c == "frames":
            p.add_argument("--count", type=int, default=4)

    # Pixel Effects
    ep = fam.add_parser("effect", help="Pixel Effects: the grain applied to a photo")
    sub = ep.add_subparsers(dest="cmd", required=True)
    for c in ("dissolve", "behind", "tone"):
        p = sub.add_parser(c)
        p.add_argument("--gradient", default="royal-blue", help="ground gradient (tone: whose two tones to use)")
        p.add_argument("--size", required=True, help="frame size on the canvas, e.g. 470x1080")
        p.add_argument("--scale", type=float, default=2, help="export scale (2 = 2x)")
        p.add_argument("--out", default=None)
        if c == "tone":
            p.add_argument("photo", help="any place photo (never a person)")
            p.add_argument("--cell", type=float, default=1, help="cell in CSS px (default 1)")
            p.add_argument("--steps", type=int, default=4)
            p.add_argument("--invert", action="store_true", help="dark subjects on the darker tone (light grounds)")
            continue
        p.add_argument("--photo", default=None, help="cut-out PNG, only for the preview")
        p.add_argument("--photo-rect", default=None, help="x,y,w,h of the photo box on the frame, as in Paper")
        p.add_argument("--colours", default=None, help="comma-separated token names for the cells, as many as you like")
        p.add_argument("--cell", type=float, default=8, help="cell in CSS px, shared with the ground (default 8)")
        if c == "dissolve":
            p.add_argument("--start", type=float, default=None, help="y where the cells begin (below the face, chest and any logo); default 80%% of the edge")
            p.add_argument("--edge", type=float, default=None, help="y of the bleed edge inside the frame; default the frame height")
            p.add_argument("--density", type=float, default=0.55, help="share of cells filled in the last row (0 to 1)")
            p.add_argument("--curve", type=float, default=1.4, help="how fast the density rises (1 = even, higher = more at the bottom)")
            p.add_argument("--seed", type=int, default=7, help="change it for a different random scatter")
        else:
            p.add_argument("--start", type=float, default=0.35, help="fraction of the height where the band begins")

    args = ap.parse_args()
    if getattr(args, "steps", None) and args.family == "gradient":
        RECIPE["steps"] = args.steps
    run = {("gradient", "list"): cmd_list, ("gradient", "webflow"): cmd_webflow, ("gradient", "png"): cmd_png,
           ("gradient", "video"): cmd_video, ("gradient", "frames"): cmd_frames, ("gradient", "web"): cmd_web,
           ("effect", "dissolve"): cmd_photo_dissolve, ("effect", "behind"): cmd_photo_behind, ("effect", "tone"): cmd_photo_tone}
    run[(args.family, args.cmd)](args)


if __name__ == "__main__":
    main()
