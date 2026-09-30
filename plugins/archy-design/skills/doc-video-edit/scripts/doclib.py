#!/usr/bin/env python3
"""DOC course video builder library.

Turns a per-video config (video.json) into a Tesseract editable document plus keyframe
actions: footage cut list (two cameras), dialogue layers, intro + music, red section wipes,
end card, per-camera grade and the DOC graphics (lower thirds, splits, cards) rebuilt natively
with the motion measured from the DOC reference edits (see references/motion-spec.md).

Clocks: every time in video.json is a SOURCE time in seconds on the camera clock (CAM A and B
share it). Edit time = source time + the offset of the dialogue segment that contains it.
Layer ranges are milliseconds; keyframe times are layer-local milliseconds.
"""
import json, os
from PIL import ImageFont

ms = lambda s: int(round(s * 1000))

# --- DOC video tokens (DOC - Videos Foundations) ---------------------------------------------
GROUND = "EFEDD8"   # --color-video-ground
INK = "181816"      # --color-video-ink
RED500 = "ED0606"   # --color-red-500
RED400 = "FF0600"   # --color-red-400
WHITE = "FFFFFF"    # --color-white
RULE = "DCDAC4"     # --color-cream-rule
CREAM200 = "FAF9EE" # --color-cream-200
CREAM100 = "FDFCF5" # --color-cream-100

def hexc(h, a=1.0):
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)] + [a]

# Weight -> (file, tsrct fontFamily, fontStyle) as returned by `tsrct project import-font`.
FACE = {"Regular": ("Satoshi-Regular.otf", "Satoshi", "Regular"),
        "Medium": ("Satoshi-Medium.otf", "Satoshi Medium", "Regular"),
        "Bold": ("Satoshi-Bold.otf", "Satoshi", "Bold"),
        "Black": ("Satoshi-Black.otf", "Satoshi Black", "Regular")}

class Metrics:
    """Text metrics from the same Satoshi files that are packaged in the project."""
    def __init__(self, fonts_dir):
        self.dir = fonts_dir

    def font(self, w, size):
        return ImageFont.truetype(os.path.join(self.dir, FACE[w][0]), size=int(round(size)))

    def width(self, text, w, size):
        return self.font(w, size).getlength(text) * size / int(round(size))

    def baseline(self, top, lh, w, size):
        """CSS line box top -> baseline y (half-leading model), matching Paper's layout."""
        asc, desc = self.font(w, size).getmetrics()
        k = size / int(round(size))
        return top + (lh - (asc * k + desc * k)) / 2 + asc * k

def XF(x=0, y=0, ax=0, ay=0, op=100):
    return {"anchorPoint": [ax, ay], "position": [x, y], "scale": [100, 100], "rotation": 0, "opacity": op}

def xf(pos=(0, 0), scale=100, anchor=(0, 0)):
    return {"anchorPoint": list(anchor), "position": list(pos), "scale": [scale, scale],
            "rotation": 0, "opacity": 100}

# --- Easing -----------------------------------------------------------------------------------
def _bz(x1, y1, x2, y2): return {"type": "cubicBezier", "x1": x1, "y1": y1, "x2": x2, "y2": y2}
def _mirror(x1, y1, x2, y2): return _bz(1 - x2, 1 - y2, 1 - x1, 1 - y1)

EASE = {"lin": {"type": "linear"},
        "out": _bz(0.16, 1.0, 0.3, 1.0),
        "soft": _bz(0.33, 0.0, 0.2, 1.0),       # splits, cards: gentle ease-out
        "inout": _bz(0.65, 0.0, 0.35, 1.0),
        "in": _bz(0.55, 0.0, 0.75, 0.4),
        "hold": {"type": "hold"}}

# Lower-third tracks, fitted per frame to the DOC lower-third asset (rms ~1 px):
# (bezier, start ms, end ms). Exit = time mirror over the last second.
LT = {"cream": ((0.2, 0.2, 0.2, 1.0), 100, 1025), "red": ((0.2, 0.3, 0.2, 1.0), 20, 1000),
      "tag": ((0.3, 0.2, 0.0, 1.0), 140, 975), "name": ((0.2, 0.6, 0.5, 1.0), 240, 1000),
      "role": ((0.0, 0.0, 0.0, 1.0), 300, 1000)}
for _k, (_c, _, _) in LT.items():
    EASE[_k + "_in"] = _bz(*_c)
    EASE[_k + "_out"] = _mirror(*_c)

# --- Graphic group ----------------------------------------------------------------------------
class G:
    """One graphic = one Group at the composition origin; children use frame pixels."""
    def __init__(self, gid, name, start, end, m):
        self.gid, self.name, self.start, self.end, self.m = gid, name, start, end, m
        self.children, self.anims, self.n = [], [], 0

    @property
    def dur(self):
        return ms(self.end - self.start)

    def nid(self):
        self.n += 1
        return self.gid + self.n

    def _layer(self, lid, name, t0, t1):
        a = ms(t0 - self.start) if t0 is not None else 0
        b = ms((t1 if t1 is not None else self.end) - self.start)
        return {"id": lid, "name": name, "blendMode": "normal", "activeRange": {"start": a, "duration": b - a}}

    def child(self, lid):
        return next(c for c in self.children if c["id"] == lid)

    def rect(self, name, x, y, w, h, color, anchor="left", t0=None, t1=None, op=100, sy=100, radius=0):
        """x, y = top-left in frame pixels. anchor: left | right | center (x), top (y)."""
        lid = self.nid()
        L = self._layer(lid, name, t0, t1)
        ax = {"left": 0, "right": w, "center": w / 2}[anchor]
        t = XF(x + ax, y, ax, 0, op)
        t["scale"] = [100, sy]
        L.update({"type": "Rect", "transform": t,
                  "rect": {"size": [w, h], "position": [0, 0], "fillColor": hexc(color)}})
        if radius:
            L["rect"]["roundness"] = radius
        self.children.append(L)
        return lid

    def text(self, name, s, x, top, lh, w, size, color, t0=None, t1=None, op=100):
        """Point text; (x, top) is the CSS line box top-left, converted to the baseline origin."""
        lid = self.nid()
        L = self._layer(lid, name, t0, t1)
        L.update({"type": "Text", "transform": XF(x, self.m.baseline(top, lh, w, size), op=op),
                  "sourceText": {"text": s, "fontFamily": FACE[w][1], "fontStyle": FACE[w][2], "fontSize": size,
                                 "fillColor": hexc(color), "strokeWidth": 0, "justification": "left"}})
        self.children.append(L)
        return lid

    def ctext(self, name, s, cx, top, lh, w, size, color, **kw):
        """Point text centred on cx (Paper text-align: center)."""
        return self.text(name, s, cx - self.m.width(s, w, size) / 2, top, lh, w, size, color, **kw)

    def key(self, lid, prop, frames):
        """frames: [(layer-local ms, value, easing name)]; easing belongs to the destination key."""
        ks = [{"id": f"k{lid}-{prop}-{i}", "layerTime": int(t), "value": {"type": "float", "value": v},
               "easing": EASE[ez]} for i, (t, v, ez) in enumerate(frames)]
        self.anims.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
                           "property": {"layerId": lid, "propertyType": prop}, "keyframes": ks})

    def put_behind(self, lid, ref_id):
        item = self.child(lid)
        self.children.remove(item)
        self.children.insert(self.children.index(self.child(ref_id)), item)

    def matte_to(self, lid, matte_id):
        """Track matte: the matte layer is not rendered; lid shows only inside it."""
        self.child(lid)["trackMatte"] = {"mode": "alpha", "layer": matte_id}

    def layer(self):
        return {"type": "Group", "id": self.gid, "name": self.name, "blendMode": "normal",
                "activeRange": {"start": ms(self.start), "duration": self.dur},
                "transform": XF(), "layers": self.children[::-1]}  # first added = backmost

# --- Motion helpers ---------------------------------------------------------------------------
def rise(g, lid, base_y, at_ms, dy=24, dur=650, peak=100, out_at=None, out_dur=600):
    fr = [(at_ms, 0, "lin"), (at_ms + dur * 0.75, peak, "soft")]
    if out_at is not None:
        fr += [(out_at, peak, "hold"), (out_at + out_dur, 0, "in")]
    g.key(lid, "opacity", fr)
    g.key(lid, "positionY", [(at_ms, base_y + dy, "lin"), (at_ms + dur, base_y, "soft")])

def draw_x(g, lid, at_ms, dur=850):
    g.key(lid, "scaleX", [(at_ms, 0, "lin"), (at_ms + dur, 100, "soft")])

def lt_keys(g, lid, prop, track, v_hidden, v_shown):
    _, t0, t1 = LT[track]
    d = g.dur
    g.key(lid, prop, [(t0, v_hidden, "lin"), (t1, v_shown, track + "_in"),
                      (d - t1, v_shown, "hold"), (d - t0, v_hidden, track + "_out")])

def box_reveal(g, x, top, bw, bh, text_ids, text_x, color=GROUND):
    """Red lead wipes to 97 % behind the box; the box wipes in front of it; text clipped by a
    box matte slides 80 px into place. Exit mirrors it; the red is off by then (never on exit)."""
    box = g.rect("Box", x, top, bw, bh, color)
    g.put_behind(box, text_ids[0])
    red = g.rect("Red lead", x, top, bw, bh, RED500)
    g.put_behind(red, box)
    matte = g.rect("Box matte", x, top, bw, bh, WHITE)
    _, r0, r1 = LT["red"]
    g.key(red, "scaleX", [(r0, 0, "lin"), (r1, 97, "red_in"), (r1 + 100, 0, "hold")])
    for lid in (box, matte):
        lt_keys(g, lid, "scaleX", "cream", 0, 100)
    for t, tx in zip(text_ids, text_x):
        g.matte_to(t, matte)
        lt_keys(g, t, "positionX", "name", tx + 80, tx)
    return box

# --- Graphic builders (geometry from the DOC - Videos Foundations templates) ------------------
def speaker_lt(g, name, role, x=88, y=779, tag_x=404, tag_y=919):
    """S3 speaker lower third: name box Black 65 (padding 50/75) + red role tag Medium 40
    (padding 15/25) that grows up from its bottom edge in front of the box."""
    m = g.m
    bw, bh = m.width(name, "Black", 65) + 150, 65 * 1.11 + 100
    n = g.text("Name", name, x + 75, y + 50, 65 * 1.11, "Black", 65, INK)
    box_reveal(g, x, y, bw, bh, [n], [x + 75])
    rw, th = m.width(role, "Medium", 40) + 50, 40 * 1.11 + 30
    tag = g.rect("Role tag", tag_x, tag_y, rw, th, RED500)
    tmatte = g.rect("Tag matte", tag_x, tag_y, rw, th, WHITE)
    for lid in (tag, tmatte):
        L = g.child(lid)
        L["transform"]["anchorPoint"] = [0, th]
        L["transform"]["position"] = [tag_x, tag_y + th]
        lt_keys(g, lid, "scaleY", "tag", 0, 100)
    r = g.text("Role", role, tag_x + 25, tag_y + 15, 40 * 1.11, "Medium", 40, WHITE)
    g.matte_to(r, tmatte)
    rb = m.baseline(tag_y + 15, 40 * 1.11, "Medium", 40)
    lt_keys(g, r, "positionY", "role", rb + 46, rb)

def caption_lt(g, lines, x=88, top=740, w="Bold", size=60, lh=72, pad=50):
    """L1 caption: video-ground box, Bold 60/72, padding 50, bottom-left over footage."""
    tw = max(g.m.width(s, w, size) for s in lines)
    bw, bh = tw + 2 * pad, lh * len(lines) + 2 * pad
    tids = [g.text(f"Line {i + 1}", s, x + pad, top + pad + i * lh, lh, w, size, INK) for i, s in enumerate(lines)]
    box_reveal(g, x, top, bw, bh, tids, [x + pad] * len(tids))

def split_list(g, title_lines, items, reveals, gap_bullet=25):
    """T1: panel 960-1920; column at x 1060, vertically centred: title Black 70/84 (op .9),
    24 gap, 3px cream-rule 700 wide, 24 gap, items Medium 60/72 with 17px red-400 bullets.
    reveals: edit times (s) of each item; an item at the group start shows with the panel."""
    m = g.m
    g.rect("Panel", 960, 0, 960, 1080, GROUND)
    th = 84 * len(title_lines) if len(title_lines) > 1 else 79
    total = th + 24 + 1 + 24 + 72 * len(items)
    top = 540 - total / 2
    nudge = 2.5 if len(title_lines) == 1 else 0
    tids = [g.text(f"Title {i + 1}", s, 1060, top + i * 84 - nudge, 84, "Black", 70, INK, op=90)
            for i, s in enumerate(title_lines)]
    rule_y = top + th + 24
    rule = g.rect("Rule", 1060, rule_y - 1, 700, 3, RULE)
    for i, t in enumerate(tids):
        rise(g, t, m.baseline(top + i * 84 - nudge, 84, "Black", 70), 60 + i * 90, dy=20)
    draw_x(g, rule, 220)
    y0 = rule_y + 1 + 24
    for i, (s, at) in enumerate(zip(items, reveals)):
        ry = y0 + i * 72
        t0 = at if i or at > g.start + 0.3 else g.start
        b = g.rect(f"Bullet {i + 1}", 1060, ry + 27.5, 17, 17, RED400, t0=t0)
        t = g.text(f"Item {i + 1}", s, 1060 + 17 + gap_bullet, ry, 72, "Medium", 60, INK, t0=t0)
        g.key(b, "opacity", [(0, 0, "lin"), (350, 100, "soft")])
        g.key(b, "positionY", [(0, ry + 27.5 + 22, "lin"), (600, ry + 27.5, "soft")])
        rise(g, t, m.baseline(ry, 72, "Medium", 60), 0, dy=22)

def split_numbered(g, title, items, reveals, highlight=None):
    """T2: numbered list: title Black 70/84 at x 1061 (one line: top 337; two lines, a list: top 342),
    3px rule 769 wide 21 below the title box, items Medium 60 at x 1131 every 88 px from 47 below
    the rule, red-500 52px squares with cream-200 Bold 39.39 digits. An item whose reveal is at the
    group start shows with the panel (a card brought back with rows already on).
    highlight (1-based): section-marker state (the Big Three): every item builds with the panel,
    120 ms apart, and the others settle at 30 % opacity, as in the Paper templates."""
    m = g.m
    lines = title if isinstance(title, list) else [title]
    if highlight:
        reveals = [g.start] * len(items)
    g.rect("Panel", 960, 0, 960, 1080, GROUND)
    top, th = (337 - 2.5, 79) if len(lines) == 1 else (342, 84 * len(lines))
    for i, s in enumerate(lines):
        t = g.text(f"Title {i + 1}", s, 1061, top + i * 84, 84, "Black", 70, INK, op=90)
        rise(g, t, m.baseline(top + i * 84, 84, "Black", 70), 60 + i * 90, dy=20)
    rule_y = (437 if len(lines) == 1 else top + th + 21)
    r = g.rect("Rule", 1061, rule_y, 769, 3, RULE)
    draw_x(g, r, 220)
    for i, (s, at) in enumerate(zip(items, reveals)):
        ty = rule_y + 47 + 88 * i
        by = ty + 14.5
        t0 = g.start if at <= g.start + 0.3 else at
        d = 120 if t0 == g.start else 0
        if highlight:
            d = 300 + 120 * i
        k = 0.3 if highlight and i + 1 != highlight else 1.0
        box = g.rect(f"Number box {i + 1}", 1059, by, 52, 52, RED500, t0=t0, op=round(100 * k))
        nw = m.width(str(i + 1), "Bold", 39.39)
        num = g.text(f"Number {i + 1}", str(i + 1), 1059 + 26 - nw / 2, by, 52, "Bold", 39.39, CREAM200, t0=t0, op=round(90 * k))
        it = g.text(f"Item {i + 1}", s, 1131, ty, 72, "Medium", 60, INK, t0=t0)
        g.key(box, "scaleX", [(d, 0, "lin"), (d + 450, 100, "soft")])
        g.key(num, "opacity", [(d + 200, 0, "lin"), (d + 500, round(90 * k), "soft")])
        rise(g, it, m.baseline(ty, 72, "Medium", 60), d + 60, dy=22, peak=round(100 * k))

def split_blocks(g, blocks, top=212, gap=70, preset=False):
    """T4: stacked blocks (e.g. Associate / Owner): label Black 75/88, 14 gap, 3px rule
    (min 542 wide), items Medium 60/80 with 16px red-400 bullets. blocks: [{label, items,
    title_at, at}] with edit times. top: the block column's top in the Paper artboard.
    preset: the card is brought back (a re-entry after a cut to camera); whatever is timed at the
    group start is already on, like the panel, and only the later items animate."""
    m = g.m
    g.rect("Panel", 960, 0, 960, 1080, GROUND)
    on = lambda t: preset and t <= g.start + 0.05
    y_top = top
    for b in blocks:
        label, items, t_title, t_items = b["label"], b["items"], b["title_at"], b["at"]
        rows_w = max(16 + 28 + m.width(s, "Medium", 60) for s in items)
        bw = max(542, m.width(label, "Black", 75), rows_w)
        tt = g.text(f"{label} title", label, 1060, y_top, 88, "Black", 75, INK, t0=t_title)
        rl = g.rect(f"{label} rule", 1060, y_top + 88 + 14, bw, 3, RULE, t0=t_title)
        if not on(t_title):
            rise(g, tt, m.baseline(y_top, 88, "Black", 75), 0 if t_title > g.start + 0.1 else 60, dy=20)
            draw_x(g, rl, 160 if t_title > g.start + 0.1 else 220)
        y = y_top + 88 + 14 + 3 + 14 + 14
        for i, (s, at) in enumerate(zip(items, t_items)):
            ry = y + 80 * i
            bl = g.rect(f"{label} bullet {i + 1}", 1060, ry + 32, 16, 16, RED400, t0=at)
            tx = g.text(f"{label} item {i + 1}", s, 1060 + 16 + 28, ry, 80, "Medium", 60, INK, t0=at)
            if on(at):
                continue
            g.key(bl, "opacity", [(0, 0, "lin"), (350, 100, "soft")])
            g.key(bl, "positionY", [(0, ry + 32 + 22, "lin"), (600, ry + 32, "soft")])
            rise(g, tx, m.baseline(ry, 80, "Medium", 60), 0, dy=22)
        y_top += 88 + 14 + 3 + 14 + 14 + 80 * len(items) + gap

def framework_card(g, title_lines, items, reveals, top=169, x=219):
    """T7: full-screen numbered framework (e.g. The three concepts). Title Black 102.96, leading 98 %
    (op .9), two lines centred on a 174 px box at the column top; rows at 269 / 416 / 655 below it
    (a row is 87 px, +92 per extra text line), 3px cream-rule 1478 wide 30 px above each later row;
    red-500 52px squares with cream-200 Bold 39 digits, items Medium 76.16/92 (op .9) at +85.5 px.
    items: [[line, ...], ...]; reveals: edit times, one per row (rules draw with the row below)."""
    m = g.m
    g.rect("Ground", 0, 0, 1920, 1080, GROUND)
    tlh = 102.96 * 0.98
    ttop = top + (174 - tlh * len(title_lines)) / 2
    for i, s in enumerate(title_lines):
        t = g.text(f"Title {i + 1}", s, x, ttop + i * tlh, tlh, "Black", 102.96, INK, op=90)
        rise(g, t, m.baseline(ttop + i * tlh, tlh, "Black", 102.96), 60 + i * 90, dy=20, peak=90)
    rx, row_top = x + 3.49, top + 269
    for i, (lines, at) in enumerate(zip(items, reveals)):
        rh = 87 + 92 * (len(lines) - 1)
        t0 = g.start if at <= g.start + 0.3 else at
        d = 120 if t0 == g.start else 0
        if i:
            r = g.rect(f"Rule {i}", rx, row_top - 30 - 1.5, 1478, 3, RULE, t0=t0)
            draw_x(g, r, d)
        by = row_top + 17.5
        box = g.rect(f"Number box {i + 1}", rx, by, 52, 52, RED500, t0=t0)
        nw = m.width(str(i + 1), "Bold", 39)
        num = g.text(f"Number {i + 1}", str(i + 1), rx + 26 - nw / 2, by, 52, "Bold", 39, CREAM200, t0=t0, op=90)
        g.key(box, "scaleX", [(d, 0, "lin"), (d + 450, 100, "soft")])
        g.key(num, "opacity", [(d + 200, 0, "lin"), (d + 500, 90, "soft")])
        ltop = row_top + rh / 2 - 46 * len(lines)
        for k, s in enumerate(lines):
            it = g.text(f"Item {i + 1}.{k + 1}", s, rx + 82, ltop + 92 * k, 92, "Medium", 76.16, INK, t0=t0, op=90)
            rise(g, it, m.baseline(ltop + 92 * k, 92, "Medium", 76.16), d + 60 + 90 * k, dy=22, peak=90)
        row_top += rh + 60

INKSOFT = "2E2E2A"   # --color-video-ink-soft

def _fmt_js(v, comma):
    return f"String({v}).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ',')" if comma else f"String({v})"

def number_card(g, figure, label, count=None, label2=None, eyebrow=None, color=None, y=None, size=None, fig_op=90, label2_ms=650):
    """T11: full-screen figure Black 170.85/206, label Bold 76.16/92, optional label2 Regular
    76.16/92 below it and an eyebrow Medium 40/48 uppercase above (tracking 0.063em, ink-soft).
    y: centre lines {"eyebrow", "figure", "label", "label2"} from the Paper artboard (default: one
    label, figure 503, label 634). color: figure colour (default ink; red-500 where Paper uses it).
    size: [font size, line height] of the figure when Paper sets it larger (e.g. [220, 250]); fig_op:
    figure opacity (90 as in the template, 100 where Paper has none).
    count: {"all": true, "delay": 200, "dur": 1300, "stagger": 0} counts EVERY number of the figure up
    (house rule); the legacy {"text": "$500K", "prefix": "$", "to": 500, "step": 10, "suffix": "K"}
    counts only the leading part. Counters are right-aligned at their final right edge so the static
    text never moves."""
    m = g.m
    y = dict({"figure": 503, "label": 634}, **(y or {}))
    fc = color or INK
    g.rect("Ground", 0, 0, 1920, 1080, GROUND)
    size, lh = size or (170.85, 206)
    fw = m.width(figure, "Black", size)
    left = 960 - fw / 2
    ftop = y["figure"] - lh / 2
    fy = m.baseline(ftop, lh, "Black", size)
    if count and count.get("all"):
        figs, counters = _figure_counters(g, figure, left, ftop, lh, size, fc)
    elif count:
        head = count["text"]
        cw = m.width(head, "Black", size)
        cnt = g.text("Figure count", head, left + cw, ftop, lh, "Black", size, fc, op=90)
        g.child(cnt)["sourceText"]["justification"] = "right"
        rest = figure[len(head):]
        figs = (cnt, g.text("Figure rest", rest, left + cw, ftop, lh, "Black", size, fc, op=90)) if rest else (cnt,)
        counters = [(cnt, count["prefix"], count["to"], count["step"], count["suffix"], count.get("comma"))]
    else:
        figs, counters = (g.text("Figure", figure, left, ftop, lh, "Black", size, fc, op=90),), []
    lw = m.width(label, "Bold", 76.16)
    l_id = g.text("Label", label, 960 - lw / 2, y["label"] - 46, 92, "Bold", 76.16, INK, op=90)
    for lid in figs:
        rise(g, lid, fy, 40, dy=30, peak=fig_op)
    rise(g, l_id, m.baseline(y["label"] - 46, 92, "Bold", 76.16), 350, dy=20, peak=90)
    if label2:
        w2 = m.width(label2, "Regular", 76.16)
        l2 = g.text("Label 2", label2, 960 - w2 / 2, y["label2"] - 46, 92, "Regular", 76.16, INK, op=90)
        rise(g, l2, m.baseline(y["label2"] - 46, 92, "Regular", 76.16), label2_ms, dy=20, peak=90)
    if eyebrow:
        s = eyebrow.upper()
        tr = 0.063 * 40
        ew = m.width(s, "Medium", 40) + tr * (len(s) - 1)
        e = g.text("Eyebrow", s, 960 - ew / 2, y["eyebrow"] - 24, 48, "Medium", 40, INKSOFT, op=90)
        g.child(e)["sourceText"]["tracking"] = 63
        rise(g, e, m.baseline(y["eyebrow"] - 24, 48, "Medium", 40), 0, dy=16, peak=90)
    for i, (lid, pre, to, step, suf, comma, *rest) in enumerate(counters):
        steps = to // step
        dec = rest[0] if rest else 0
        v = f"Math.round(p*{steps})*{step}" if not dec else f"(Math.round(p*{steps})*{step}/{10 ** dec}).toFixed({dec})"
        delay = count.get("delay", 200) + i * count.get("stagger", 0)
        js = (f"var p=Math.max(0,Math.min(1,(input.time.milliseconds-{delay})/{count.get('dur', 1300)}));"
              f"p=1-Math.pow(1-p,3);return '{pre}'+{_fmt_js(v, comma)}+'{suf}';")
        g.anims.append({"type": "setFxPropertyAnimator", "compositionId": "main",
                        "property": {"layerId": lid, "propertyType": "textContent"},
                        "animator": {"type": "jsScript", "layerTimeJsCode": js}, "dependencies": []})

def _nice_step(v):
    """About 60 steps for the count, rounded to 1, 2, 5, 10, 20, 50 ..."""
    raw = max(1, v / 60)
    k = 1
    while True:
        for b in (1, 2, 5):
            if b * k >= raw:
                return b * k if v % (b * k) == 0 else 1
        k *= 10

def _figure_counters(g, figure, left, ftop, lh, size, color, w="Black", op=90):
    """Every number of the figure counts up (house rule: '20% + 5%', '1,200 - 1,500' animate on
    both sides). Each number is right-aligned at its final right edge; the text between numbers
    is static. Numbers below 2 stay static (nothing to count)."""
    import re
    m, figs, counters, pos = g.m, [], [], 0
    for k, mt in enumerate(re.finditer(r"\d[\d,]*(?:\.\d+)?", figure)):
        a, b = mt.span()
        num = mt.group().replace(",", "")
        dec = len(num.split(".")[1]) if "." in num else 0   # "3.1 miles" counts 0.0 -> 3.1 in tenths
        val = float(num)
        if a > pos:
            figs.append(g.text(f"Figure text {k + 1}", figure[pos:a], left + m.width(figure[:pos], w, size),
                               ftop, lh, w, size, color, op=op))
        if val < 2:
            figs.append(g.text(f"Figure number {k + 1}", mt.group(), left + m.width(figure[:a], w, size),
                               ftop, lh, w, size, color, op=op))
        else:
            lid = g.text(f"Figure count {k + 1}", mt.group(), left + m.width(figure[:b], w, size),
                         ftop, lh, w, size, color, op=op)
            g.child(lid)["sourceText"]["justification"] = "right"
            figs.append(lid)
            units = int(round(val * 10 ** dec))
            counters.append((lid, "", units, _nice_step(units), "", "," in mt.group(), dec))
        pos = b
    if pos < len(figure):
        figs.append(g.text("Figure text end", figure[pos:], left + m.width(figure[:pos], w, size),
                           ftop, lh, w, size, color, op=op))
    return tuple(figs), counters

def closing_card(g, line1, line2, fade_ms, xfade_ms, mid=False):
    """T10: a Bold block over a Regular block, 83.79/102 (op .9), centred as a stack on y 540
    (one line each: 489 / 591). A block may hold several lines ("\n"). Lines rise in (the Regular
    block 520 ms after the Bold one, lines 120 ms apart); at the end the text fades and the card
    crossfades into the end card. mid=True: a full card inside the video, hard cut in and out."""
    m = g.m
    g.rect("Ground", 0, 0, 1920, 1080, GROUND)
    b1, b2 = line1.split("\n"), line2.split("\n")
    top = 540 - 51 * (len(b1) + len(b2))
    t_end = g.dur - xfade_ms
    out = {} if mid else {"out_at": t_end - fade_ms, "out_dur": fade_ms}
    rows = [(s, "Bold", 80 + 120 * i) for i, s in enumerate(b1)] + [(s, "Regular", 600 + 120 * i) for i, s in enumerate(b2)]
    for i, (s, w, at) in enumerate(rows):
        a = g.ctext(f"Line {i + 1}", s, 960, top + 102 * i, 102, w, 83.79, INK, op=90)
        rise(g, a, m.baseline(top + 102 * i, 102, w, 83.79), at, dy=24, peak=90, **out)
    if not mid:
        g.key(g.gid, "opacity", [(t_end, 100, "lin"), (t_end + xfade_ms, 0, "soft")])

# --- Number chains on a split (N6 / N7 / N8, DOC - Videos Foundations F9.4) ---------------------
# Pieces: cream-100 label box (Bold ink-soft, op .9, leading 97 %), a 1.69 px ink connector with a
# red-400 dot where it meets the red-500 result box (white Black/Bold text, op .9).
# Motion (same language as the splits): a box rises 22 px and fades in (650 ms); the connector
# draws down (400 ms) and its dot fades in; the red box opens from the left (450 ms) and its text
# fades in 200-500 ms after; captions rise like list items.
def _box_in(g, box, tids, y_box, y_texts, at):
    rise(g, box, y_box, at, dy=22)
    for t, y in zip(tids, y_texts):
        rise(g, t, y, at + 60, dy=22, peak=90)

def _connector(g, x, top, h, dot_y, at):
    ln = g.rect("Connector", x, top, 1.69, h, INK)
    L = g.child(ln)
    g.key(ln, "scaleY", [(at, 0, "lin"), (at + 400, 100, "soft")])
    dot = g.rect("Connector dot", x + 0.845 - 5.512, dot_y, 11.024, 11.024, RED400, radius=5.512)
    g.key(dot, "opacity", [(at + 250, 0, "lin"), (at + 500, 100, "soft")])
    return ln, dot

def _red_box(g, x, top, w, h, text, w_font, size, at, lh=None, count=True):
    """count: every number in the result counts up (house rule), 1.3 s cubic ease-out from +200 ms."""
    lh = lh or size * 0.97
    box = g.rect("Result box", x, top, w, h, RED500)
    g.key(box, "scaleX", [(at, 0, "lin"), (at + 450, 100, "soft")])
    ttop = top + (h - lh) / 2
    if count:
        figs, counters = _figure_counters(g, text, x + w / 2 - g.m.width(text, w_font, size) / 2, ttop, lh, size,
                                          WHITE, w=w_font)
    else:
        figs, counters = (g.ctext("Result", text, x + w / 2, ttop, lh, w_font, size, WHITE, op=90),), []
    for t in figs:
        g.key(t, "opacity", [(at + 200, 0, "lin"), (at + 500, 90, "soft")])
    for lid, pre, to, step, suf, comma, dec in counters:
        v = f"Math.round(p*{to // step})*{step}" if not dec else f"(Math.round(p*{to // step})*{step}/{10 ** dec}).toFixed({dec})"
        js = (f"var p=Math.max(0,Math.min(1,(input.time.milliseconds-{at + 200})/1300));"
              f"p=1-Math.pow(1-p,3);return '{pre}'+{_fmt_js(v, comma)}+'{suf}';")
        g.anims.append({"type": "setFxPropertyAnimator", "compositionId": "main",
                        "property": {"layerId": lid, "propertyType": "textContent"},
                        "animator": {"type": "jsScript", "layerTimeJsCode": js}, "dependencies": []})
    return box, figs[0]

def split_result(g, label, figure, caption, at_label, at_figure, at_caption):
    """N7: label box 618 wide (padding 45.11, Bold 50.82) at (1131, 325.9), connector to a red-500
    box 618x143 at y 527.6 (figure Black 56.39), caption Medium 40/48 at (1131, 701). at_*: ms."""
    m = g.m
    g.rect("Panel", 960, 0, 960, 1080, GROUND)
    lh = 50.82 * 0.97
    btop, bh = 395.615 - (90.22 + lh) / 2, 90.22 + lh
    box = g.rect("Label box", 1131, btop, 618, bh, CREAM100)
    lt = g.ctext("Label", label, 1440, btop + 45.11, lh, "Bold", 50.82, INKSOFT, op=90)
    _box_in(g, box, [lt], btop, [m.baseline(btop + 45.11, lh, "Bold", 50.82)], at_label)
    ln, dot = _connector(g, 1438.155, 465.609, 64.072, 523.765, at_figure - 350)
    rb, _ = _red_box(g, 1131, 527.61, 618, 143, figure, "Black", 56.39, at_figure)
    g.put_behind(dot, rb)
    for i, s in enumerate(caption):
        c = g.text(f"Caption {i + 1}", s, 1131, 701 + 48 * i, 48, "Medium", 40, INK, op=90)
        rise(g, c, m.baseline(701 + 48 * i, 48, "Medium", 40), at_caption + 90 * i, dy=22, peak=90)

def split_equals(g, label_lines, result, at_label, at_result):
    """N6: label box 618 wide (padding 45.11, Bold 50.82, centred lines) centred on y 412, "=" Bold
    50.82 ink-soft at (1423, 511), red-500 result box 618x143 at (1131, 570), Black 56.39."""
    m = g.m
    g.rect("Panel", 960, 0, 960, 1080, GROUND)
    lh = 50.82 * 0.97
    bh = 90.22 + lh * len(label_lines)
    btop = 412 - bh / 2
    box = g.rect("Label box", 1131, btop, 618, bh, CREAM100)
    tids = [g.ctext(f"Label {i + 1}", s, 1440, btop + 45.11 + lh * i, lh, "Bold", 50.82, INKSOFT, op=90)
            for i, s in enumerate(label_lines)]
    _box_in(g, box, tids, btop, [m.baseline(btop + 45.11 + lh * i, lh, "Bold", 50.82) for i in range(len(tids))], at_label)
    eq = g.text("Equals", "=", 1423, 511, lh, "Bold", 50.82, INKSOFT, op=90)
    g.key(eq, "opacity", [(at_result - 300, 0, "lin"), (at_result, 90, "soft")])
    _red_box(g, 1131, 570, 618, 143, result, "Black", 56.39, at_result)

def split_pairs(g, pairs):
    """N8: two label -> result pairs, boxes 600 wide at x 1140 (padding 40, Bold 45.07), label box
    top 174.1, connector 55 px at x 1437.7, red box top 353.1; the second pair 430 px lower.
    pairs: [{label, figure, at_label, at_figure}] (ms)."""
    m = g.m
    g.rect("Panel", 960, 0, 960, 1080, GROUND)
    lh = 45.07 * 0.97
    bh = 80 + lh
    for k, p in enumerate(pairs):
        dy, dx = 430 * k, 0.5 * k
        btop = 236 + dy - bh / 2
        box = g.rect(f"Label box {k + 1}", 1140, btop, 600, bh, CREAM100)
        lt = g.ctext(f"Label {k + 1}", p["label"], 1440, btop + 40, lh, "Bold", 45.07, INKSOFT, op=90)
        _box_in(g, box, [lt], btop, [m.baseline(btop + 40, lh, "Bold", 45.07)], p["at_label"])
        ln, dot = _connector(g, 1437.655 + dx, 298 + dy, 55, 347 + dy, p["at_figure"] - 350)
        rb, _ = _red_box(g, 1140, 415 + dy - bh / 2, 600, bh, p["figure"], "Bold", 45.07, p["at_figure"])
        g.put_behind(dot, rb)

# --- F9.5 builders: N3 equation split, T10 as a statement mid-video ----------------------------
INK222 = "222222"    # --color-ink

def _t0(g, at):
    return at if at > g.start + 0.3 else g.start

def _count_line(g, name, s, cx, top, lh, w, size, color, t0, delay, dur=1300):
    """Centred text whose numbers (>= 2) count up from 0 (house rule: every number counts). Each
    counter is right-aligned at its final right edge so the words between never move."""
    import re
    m = g.m
    left = cx - m.width(s, w, size) / 2
    ids, pos = [], 0
    for k, mt in enumerate(re.finditer(r"\d+", s)):
        a, b = mt.span()
        if a > pos:
            ids.append(g.text(f"{name} text {k + 1}", s[pos:a], left + m.width(s[:pos], w, size), top, lh, w, size, color, t0=t0))
        val = int(mt.group())
        if val < 2:
            ids.append(g.text(f"{name} number {k + 1}", mt.group(), left + m.width(s[:a], w, size), top, lh, w, size, color, t0=t0))
        else:
            lid = g.text(f"{name} count {k + 1}", mt.group(), left + m.width(s[:b], w, size), top, lh, w, size, color, t0=t0)
            g.child(lid)["sourceText"]["justification"] = "right"
            ids.append(lid)
            step = _nice_step(val)
            js = (f"var p=Math.max(0,Math.min(1,(input.time.milliseconds-{delay})/{dur}));"
                  f"p=1-Math.pow(1-p,3);return String(Math.round(p*{val // step})*{step});")
            g.anims.append({"type": "setFxPropertyAnimator", "compositionId": "main",
                            "property": {"layerId": lid, "propertyType": "textContent"},
                            "animator": {"type": "jsScript", "layerTimeJsCode": js}, "dependencies": []})
        pos = b
    if pos < len(s):
        ids.append(g.text(f"{name} text end", s[pos:], left + m.width(s[:pos], w, size), top, lh, w, size, color, t0=t0))
    return ids

def equation_split(g, top_box, result, caption, reveals, count=False):
    """N3: panel 960-1920; a 516-wide column centred at x 1440 from y 320: cream-100 box 140 high
    (Medium 52/64 ink-soft), '=' Medium 54/64, red-500 box 140 high (Black 56/64 cream-100), caption
    Medium 39/48 ink after 44 px. reveals: [top box, '=' + result, caption] edit times.
    count: the numbers in both boxes count up ('40', and '20' of '1 hr 20 min'; 1 stays)."""
    m = g.m
    g.rect("Panel", 960, 0, 960, 1080, GROUND)
    cx, bx, bw = 1440, 1182, 516
    t_a, t_b, t_c = (_t0(g, reveals[0]), reveals[1], reveals[2])

    def centred(name, s, top, lh, w, size, color, t0, delay):
        if count:
            return _count_line(g, name, s, cx, top, lh, w, size, color, t0, delay)
        return [g.text(name, s, cx - m.width(s, w, size) / 2, top, lh, w, size, color, t0=t0)]

    b1 = g.rect("Box 1", bx, 320, bw, 140, CREAM100, t0=t_a)
    g.key(b1, "opacity", [(0, 0, "lin"), (450, 100, "soft")])
    g.key(b1, "positionY", [(0, 320 + 22, "lin"), (650, 320, "soft")])
    for x1 in centred("Box 1 text", top_box, 358, 64, "Medium", 52, INKSOFT, t_a, 200):
        rise(g, x1, m.baseline(358, 64, "Medium", 52), 60, dy=22)
    eq = g.text("Equals", "=", cx - m.width("=", "Medium", 54) / 2, 460, 64, "Medium", 54, INKSOFT, t0=t_b)
    rise(g, eq, m.baseline(460, 64, "Medium", 54), 0, dy=16)
    b2 = g.rect("Box 2", bx, 524, bw, 140, RED500, t0=t_b)
    g.key(b2, "scaleX", [(120, 0, "lin"), (620, 100, "soft")])
    for x2 in centred("Box 2 text", result, 562, 64, "Black", 56, CREAM100, t_b, 350):
        rise(g, x2, m.baseline(562, 64, "Black", 56), 300, dy=22)
    cap = g.text("Caption", caption, cx - m.width(caption, "Medium", 39) / 2, 708, 48, "Medium", 39, INK222, t0=t_c)
    rise(g, cap, m.baseline(708, 48, "Medium", 39), 0, dy=20)

def statement_card(g, line1, line2, at2):
    """T10 geometry (Bold / Regular 83.79/102 centred at y 489 / 591, op .9) as a mid-video full
    screen: hard cut in, line 1 rises at 80 ms, line 2 on its own word, hard cut out."""
    m = g.m
    g.rect("Ground", 0, 0, 1920, 1080, GROUND)
    w1, w2 = m.width(line1, "Bold", 83.79), m.width(line2, "Regular", 83.79)
    a1 = g.text("Line 1", line1, 960 - w1 / 2, 489 - 51, 102, "Bold", 83.79, INK, op=90)
    rise(g, a1, m.baseline(489 - 51, 102, "Bold", 83.79), 80, dy=24, peak=90)
    a2 = g.text("Line 2", line2, 960 - w2 / 2, 591 - 51, 102, "Regular", 83.79, INK, t0=_t0(g, at2), op=90)
    rise(g, a2, m.baseline(591 - 51, 102, "Regular", 83.79), 0, dy=24, peak=90)


def _shift_y(g, prefix, dy):
    """Move the children whose name starts with prefix by dy px, keyframed positionY included.
    Used for the T7 title: at 98 % leading Paper sets the glyphs 14 px lower than the half-leading
    model (measured on the F9.5 render against the artboard; rows match within 1 px)."""
    if not dy:
        return
    ids = {c["id"] for c in g.children if c["name"].startswith(prefix)}
    for c in g.children:
        if c["id"] in ids:
            c["transform"]["position"][1] += dy
    for a in g.anims:
        if a["property"]["layerId"] in ids and a["property"]["propertyType"] == "positionY":
            for k in a["keyframes"]:
                k["value"]["value"] += dy


# --- Edit ------------------------------------------------------------------------------------
# k = camera pixels per frame pixel (1 for 1080p files, 2 for UHD): the layer draws at the file's own
# size, so anchors are in camera pixels and scales are divided by k.
FRAMING = {
    "full": lambda k: xf((0, 0), 100 / k),
    "card": lambda k: xf((0, 0), 100 / k),
    "punch": lambda k: xf((960, 400), 115 / k, (960 * k, 400 * k)),   # 115 % about the frontal camera's eyeline
    "split": lambda k: xf((-480, 0), 100 / k),                          # speaker centred in the left half
    "split2": lambda k: xf((480, 400), 106 / k, (960 * k, 400 * k)),   # split + 6 % to hide a cut inside a split
    # 106 % anchored at x 480: crops ~86 px right / 65 px bottom (hides a set object in a corner of
    # CAM A full) and moves the speaker ~29 px right.
    "full_clean": lambda k: xf((480, 0), 106 / k, (480 * k, 0)),
}

def reframed(fr, k, rf):
    """House rule (F9.2 v5): every camera gets a composed base frame, cfg["reframe"][cam] =
    {"scale": s, "center": [cx, cy], "punch": 1.10}: the source point (cx, cy) in 1920x1080 frame
    pixels sits at the frame centre, zoomed s. It crops set edges, stands, lights and dead headroom
    without making the face big (s ~1.08-1.20). Every framing builds on it: punch zooms a further
    `punch` about the eyeline, split puts the same frame in the left half, split2 adds 6 %. The
    visible window must stay inside the picture (checked)."""
    s, (cx, cy), p = rf["scale"], rf["center"], rf.get("punch", 1.10)
    if fr == "punch":
        t, win = xf((960, 400), 100 * s * p / k, (cx * k, (cy - 140 / s) * k)), (s * p, cx, cy - 140 / s + 140 / (s * p), 960)
    elif fr == "split":
        t, win = xf((480, 540), 100 * s / k, (cx * k, cy * k)), (s, cx, cy, 480)
    elif fr == "split2":
        t, win = xf((480, 400), 106 * s / k, (cx * k, (cy - 140 / s) * k)), (s * 1.06, cx, cy - 140 / s + 140 / (s * 1.06), 480)
    else:
        t, win = xf((960, 540), 100 * s / k, (cx * k, cy * k)), (s, cx, cy, 960)
    z, wx, wy, half = win
    if wx - half / z < -0.5 or wx + half / z > 1920.5 or wy - 540 / z < -0.5 or wy + 540 / z > 1080.5:
        raise ValueError(f"reframe {rf} shows past the picture edge in framing {fr}")
    return t

class Edit:
    def __init__(self, cfg, fonts_dir):
        self.cfg = cfg
        self.m = Metrics(fonts_dir)
        t = cfg["timing"]
        self.intro = t["intro"]
        self.segs = [tuple(s) for s in cfg["segments"]]
        self.speech_end = self.intro + sum(b - a for a, b in self.segs)
        c = cfg["closing"]
        # closing.mode "camera": no closing card; the speaker holds cam_tail after the last word and
        # the last shot crossfades (xfade) into the end card. Otherwise the T10 closing card.
        self.camera_end = c.get("mode") == "camera"
        if self.camera_end:
            self.ff_start = None
            self.ff_end = self.e(t["voice_end_src"]) + t["cam_tail"] + t["xfade"]
        else:
            self.ff_start = self.e(c["start_src"])
            self.ff_end = self.e(t["voice_end_src"]) + t["ff_tail"] + t["ff_fade"] + t["xfade"]
        self.duration = self.ff_end - t["xfade"] + t["endcard"]

    def seg_offset(self, src):
        edit = self.intro
        for a, b in self.segs:
            if a - 1e-6 <= src <= b + 1e-6:
                return edit - a
            edit += b - a
        raise ValueError(f"source time {src} is not inside any dialogue segment")

    def e(self, src):
        return src + self.seg_offset(src)

    # footage, audio, wipes ------------------------------------------------------------------
    def footage(self):
        A, grade, out, nid = self.cfg["assets"], self.cfg["grade"], [], 100
        for a, b, cam, fr, *freeze in self.cfg["shots"]:
            # optional 5th value: a freeze frame (source s) held for the whole shot, e.g. the speaker's
            # closed-mouth frame after the last word while the room tone plays out (see freeze_anims)
            if self.seg_offset(a) != self.seg_offset(b):
                raise ValueError(f"shot {a}-{b} crosses a dialogue join")
            # cfg["cam_offset"][cam]: seconds added to that camera's source time so its picture lines up
            # with CAM A (measured by motion cross-correlation; F9.3 CAM B ran 0.85 frame early). The
            # dialogue stays on CAM A's clock.
            src = freeze[0] if freeze else a + self.cfg.get("cam_offset", {}).get(cam, 0.0)
            if not freeze and self.cfg.get("cam_offset", {}).get(cam):
                # land the offset start on a source frame (a between-frames start rendered one black
                # frame on F9.3 v5)
                fps = self.cfg["assets"].get("cam_fps", 24000 / 1001)
                src = round(src * fps) / fps
            out.append({"type": "Video", "id": nid, "name": f"CAM {cam} {a:.2f}-{b:.2f} {fr}" + (f" freeze {src:.3f}" if freeze else ""),
                        "blendMode": "normal",
                        "activeRange": {"start": ms(self.e(a)), "duration": ms(b - a)},
                        "sourceRange": {"start": ms(src), "duration": ms(b - a)},
                        "sourceIntrinsicDuration": A["cam_ms"], "volume": None, "transform": (reframed(fr, A.get("cam_width", 1920) / 1920, self.cfg["reframe"][cam]) if cam in self.cfg.get("reframe", {}) and fr in ("full", "card", "punch", "split", "split2") else FRAMING[fr](A.get("cam_width", 1920) / 1920)),
                        "source": {"assetId": A["cam" + cam], "fit": "contain"},
                        "effects": [{"id": nid * 10 + k, "enabled": True, "effect": fx} for k, fx in enumerate(grade[cam])]})
            nid += 1
        return out

    def freeze_anims(self):
        """Shots with a freeze frame: a constant TimeRemap (parent clock -> that source frame)."""
        out = []
        for i, (a, b, cam, fr, *freeze) in enumerate(self.cfg["shots"]):
            if not freeze:
                continue
            v = ms(freeze[0])
            keys = [{"id": f"tr{100 + i}-{k}", "time": ms(self.e(t)), "value": v, "easing": EASE["lin"]}
                    for k, t in enumerate((a, b))]
            out.append({"type": "setFxLayerTimeRemap", "compositionId": "main", "layerId": 100 + i,
                        "timeRemap": {"keyframes": keys, "before": "hold", "after": "hold"}})
        return out

    def dialogue(self):
        A = self.cfg["assets"]
        # 5000+: clear of footage (100+), graphics (1000 + 100 per graphic) and bookends (10-12, 60+ wipes)
        return [{"type": "Audio", "id": 5000 + i, "name": f"Dialogue {a:.2f}-{b:.2f}",
                 "activeRange": {"start": ms(self.e(a)), "duration": ms(b - a)},
                 "sourceRange": {"start": ms(a), "duration": ms(b - a)},
                 "sourceIntrinsicDuration": A["dialogue_ms"], "source": {"assetId": A["dialogue"]},
                 "volume": 1.0, "captionsEnabled": False} for i, (a, b) in enumerate(self.segs)]

    def dialogue_envelope(self):
        """House rule: no audio ends abruptly. The last dialogue segment fades out over its
        room-tone tail after timing.voice_end_src (up to timing.dialogue_fade, default 0.8 s), so the
        room tone never cuts to digital silence and the last word is never touched. Leave a tail:
        end the last segment ~0.3-0.8 s after the last word, before any next word."""
        a, b = self.segs[-1]
        d = ms(b - a)
        voice_end = self.cfg["timing"].get("voice_end_src") or b
        # the fade lives in the room-tone tail after the last word, never on the word itself
        f = max(40, min(ms(self.cfg["timing"].get("dialogue_fade", 0.8)), ms(b - voice_end - 0.05)))
        js = (f"var t=input.time.milliseconds;if(t<{d - f})return 1.0;"
              f"var p=Math.min(1,(t-{d - f})/{f});return Math.pow(Math.cos(p*Math.PI/2),2);")
        return [{"type": "setFxPropertyAnimator", "compositionId": "main",
                 "property": {"layerId": 5000 + len(self.segs) - 1, "propertyType": "volume"},
                 "animator": {"type": "jsScript", "layerTimeJsCode": js}, "dependencies": []}]

    def bookends(self):
        A, t, mix = self.cfg["assets"], self.cfg["timing"], self.cfg["mix"]
        intro = {"type": "Video", "id": 10, "name": self.cfg.get("intro_name", "Intro"), "blendMode": "normal",
                 "activeRange": {"start": 0, "duration": ms(self.intro)}, "sourceRange": {"start": 0, "duration": ms(self.intro)},
                 "sourceIntrinsicDuration": A["intro_ms"], "volume": None, "transform": xf(),
                 "source": {"assetId": A["intro"], "fit": "contain"}}
        music = {"type": "Audio", "id": 11, "name": "Intro music", "activeRange": {"start": 0, "duration": A["music_ms"]},
                 "sourceRange": {"start": 0, "duration": A["music_ms"]}, "sourceIntrinsicDuration": A["music_ms"],
                 "source": {"assetId": A["music"]}, "volume": 1.0, "captionsEnabled": False}
        endcard = {"type": "Video", "id": 12, "name": "End card", "blendMode": "normal",
                   "activeRange": {"start": ms(self.ff_end - t["xfade"]), "duration": ms(t["endcard"])},
                   "sourceRange": {"start": 0, "duration": ms(t["endcard"])}, "sourceIntrinsicDuration": A["endcard_ms"],
                   "volume": mix["endcard_gain"], "transform": xf(), "source": {"assetId": A["endcard"], "fit": "contain"}}
        return intro, endcard, music

    def wipes(self):
        A, t, mix = self.cfg["assets"], self.cfg["timing"], self.cfg["mix"]
        return [{"type": "Video", "id": 60 + i, "name": f"Red wipe {s:.2f}", "blendMode": "normal",
                 "activeRange": {"start": ms(self.e(s) - t["wipe_cover"]), "duration": 2400},
                 "sourceRange": {"start": 0, "duration": 2400}, "sourceIntrinsicDuration": A["wipe_ms"],
                 "volume": mix["wipe_gain"], "transform": xf(), "source": {"assetId": A["wipe"], "fit": "contain"},
                 "effects": [{"id": 600 + i, "enabled": True,
                              "effect": {"type": "lumaKey", "threshold": 0.08, "softness": 0.05}}]}
                for i, s in enumerate(self.cfg["wipes"])]

    def music_envelope(self):
        """House rule: the intro music never cuts, and it leaves slowly. One continuous, progressive
        descent, no plateau and no step: it starts easing down timing.music_duck_lead (1.0 s) before
        the speaker's first word, reaches timing.music_duck_db (-10 dB) 0.5 s into the words, then
        keeps falling at a steady rate in dB (a straight line in dB sounds even) down to
        timing.music_floor_db (-50 dB, inaudible under the voice) 0.1 s before the music file ends,
        where it goes to 0. With a 13 s music file and a 10 s intro: ~3.9 s from full to silent."""
        k, A, t = self.intro, self.cfg["assets"], self.cfg["timing"]
        lead, duck, floor = t.get("music_duck_lead", 1.0), t.get("music_duck_db", -10.0), t.get("music_floor_db", -50.0)
        t0, t1 = k - lead, k + 0.5
        end = A["music_ms"] / 1000 - 0.1
        js = ("var t=input.time.seconds;function e(p){p=Math.max(0,Math.min(1,p));return (1-Math.cos(p*Math.PI))/2;}\n"
              "function g(db){return Math.pow(10,db/20);}\n"
              f"if(t<{t0:g}) return 1.0;\n"
              f"if(t<{t1:g}) return g({duck:g}*e((t-{t0:g})/{t1 - t0:g}));\n"
              f"if(t<{end:g}) return g({duck:g}+({floor - duck:g})*(t-{t1:g})/{end - t1:g});\n"
              "return 0.0;")
        return [{"type": "setFxPropertyAnimator", "compositionId": "main", "property": {"layerId": 11, "propertyType": "volume"},
                 "animator": {"type": "jsScript", "layerTimeJsCode": js}, "dependencies": []}]

    # graphics ------------------------------------------------------------------------------
    def graphics(self):
        groups = []
        t = self.cfg["timing"]
        for i, spec in enumerate(self.cfg["graphics"]):
            gid = 1000 + 100 * i
            kind = spec["type"]
            if kind == "closing_card":
                g = G(gid, spec["name"], self.ff_start, self.ff_end, self.m)
                closing_card(g, spec["lines"][0], spec["lines"][1], ms(t["ff_fade"]), ms(t["xfade"]))
            else:
                g = G(gid, spec["name"], self.e(spec["in"]), self.e(spec["out"]), self.m)
                at = [self.e(s) for s in spec.get("at", [])]
                if kind == "speaker_lt":
                    speaker_lt(g, spec["name_text"], spec["role"])
                elif kind == "caption_lt":
                    caption_lt(g, spec["lines"], top=spec.get("top", 740))
                elif kind == "split_list":
                    split_list(g, spec["title"], spec["items"], at)
                elif kind == "split_numbered":
                    split_numbered(g, spec["title"], spec["items"], at or [g.start] * len(spec["items"]),
                                   spec.get("highlight"))
                elif kind == "split_blocks":
                    split_blocks(g, [dict(b, title_at=self.e(b["title_at"]), at=[self.e(s) for s in b["at"]])
                                     for b in spec["blocks"]], top=spec.get("top", 212), gap=spec.get("gap", 70),
                                 preset=spec.get("preset", False))
                elif kind == "framework_card":
                    framework_card(g, spec["title"], spec["items"], at, top=spec.get("top", 169), x=spec.get("x", 219))
                    _shift_y(g, "Title", spec.get("title_dy", 0))   # Paper sets the 98 % title ~14 px lower
                elif kind == "equation_split":
                    equation_split(g, spec["top"], spec["result"], spec["caption"], at, spec.get("count", False))
                elif kind == "statement_card":
                    statement_card(g, spec["lines"][0], spec["lines"][1], at[0])
                elif kind == "number_card":
                    number_card(g, spec["figure"], spec["label"], spec.get("count"), spec.get("label2"),
                                spec.get("eyebrow"), spec.get("color") and globals()[spec["color"]], spec.get("y"),
                                spec.get("size"), spec.get("fig_op", 90),
                                ms(self.e(spec["label2_at"]) - g.start) if "label2_at" in spec else 650)
                elif kind == "full_card":
                    closing_card(g, spec["lines"][0], spec["lines"][1], 0, 0, mid=True)
                elif kind in ("split_result", "split_equals", "split_pairs"):
                    rel = lambda s: ms(self.e(s)) - ms(g.start)
                    if kind == "split_result":
                        split_result(g, spec["label"], spec["figure"], spec["caption"],
                                     rel(spec["at_label"]), rel(spec["at_figure"]), rel(spec["at_caption"]))
                    elif kind == "split_equals":
                        split_equals(g, spec["label"], spec["result"], rel(spec["at_label"]), rel(spec["at_result"]))
                    else:
                        split_pairs(g, [dict(p, at_label=rel(p["at_label"]), at_figure=rel(p["at_figure"]))
                                        for p in spec["pairs"]])
                else:
                    raise ValueError(f"unknown graphic type {kind}")
            groups.append(g)
        return groups

    # document ------------------------------------------------------------------------------
    def document(self, checked_out):
        doc = checked_out
        doc["dimensions"] = {"width": 1920, "height": 1080}
        doc["duration"] = round(self.duration, 3)
        groups = self.graphics()
        intro, endcard, music = self.bookends()
        # Animation lives in composition.dynamics: clear it so every rebuild re-applies the keys from
        # scratch (stale keys on reused layer IDs otherwise survive).
        doc["composition"]["dynamics"] = {"entries": []}
        # Order is front to back: wipes above everything, then graphics, footage, bookends, audio.
        no_t10 = not any(sp["type"] == "closing_card" for sp in self.cfg["graphics"])
        # A frozen last shot (TimeRemap) evaluates its own keyframes on the frozen source clock, so it
        # cannot fade out: the end card goes above the footage and fades in over it instead.
        frozen_end = no_t10 and len(self.cfg["shots"][-1]) > 4
        doc["composition"]["layers"] = (self.wipes() + [g.layer() for g in groups][::-1]
                                        + ([endcard] if frozen_end else []) + self.footage()[::-1]
                                        + ([intro, music] if frozen_end else [intro, endcard, music]) + self.dialogue())
        anims = [a for g in groups for a in g.anims] + self.freeze_anims()
        if no_t10:
            # No T10: the last camera shot runs to the end and crossfades into the end card below it.
            last = self.footage()[-1]
            d, xd = last["activeRange"]["duration"], ms(self.cfg["timing"]["xfade"])
            if last["activeRange"]["start"] + d != ms(self.ff_end):
                raise ValueError(f"last shot must end at the end-card crossfade (edit {self.ff_end:.2f} s)")
        if frozen_end:
            anims.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
                          "property": {"layerId": endcard["id"], "propertyType": "opacity"},
                          "keyframes": [{"id": "k12-xfade-0", "layerTime": 0, "value": {"type": "float", "value": 0},
                                         "easing": EASE["lin"]},
                                        {"id": "k12-xfade-1", "layerTime": xd, "value": {"type": "float", "value": 100},
                                         "easing": EASE["soft"]}]})
        elif no_t10:
            anims.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
                          "property": {"layerId": last["id"], "propertyType": "opacity"},
                          "keyframes": [{"id": f"k{last['id']}-xfade-0", "layerTime": d - xd, "value": {"type": "float", "value": 100},
                                         "easing": EASE["lin"]},
                                        {"id": f"k{last['id']}-xfade-1", "layerTime": d, "value": {"type": "float", "value": 0},
                                         "easing": EASE["soft"]}]})
        return doc, anims, self.music_envelope() + self.dialogue_envelope(), groups

    def pacing_warnings(self, min_s=8.0):
        """House rule (F9.3 v3): camera changes follow ideas, not a timer. Warn (never block) on a
        speaker shot under min_s (except the first) and on a same-camera full <-> punch zoom cut."""
        out, sh = [], self.cfg["shots"]
        for i, (a, b, cam, fr, *_) in enumerate(sh):
            if i and fr in ("full", "punch") and b - a < min_s:
                out.append(f"short shot {a:.2f}-{b:.2f} CAM {cam} {fr} ({b - a:.1f} s < {min_s:g} s)")
            if i and sh[i - 1][2] == cam and {sh[i - 1][3], fr} == {"full", "punch"} and \
                    not any(abs(a - w) < 0.05 for w in self.cfg["wipes"]):  # a wipe hides the change
                out.append(f"same-camera zoom cut at {a:.2f} (CAM {cam} {sh[i - 1][3]} -> {fr})")
        # a split/card framing with no graphic over the same range shows the bare shifted camera
        # (black half) for the frames that are not covered
        spans = [(sp.get("in"), sp.get("out")) for sp in self.cfg["graphics"] if sp.get("in") is not None]
        spans.append((self.cfg["closing"]["start_src"], None))
        for a, b, cam, fr, *_ in sh:
            if fr in ("split", "card") and not any(abs(i - a) < 1e-3 and (o is None or abs(o - b) < 1e-3) for i, o in spans):
                out.append(f"{fr} shot {a:.2f}-{b:.2f} has no graphic with the same in/out")
        return out

    def timing_report(self):
        return {"intro": self.intro, "speech_end": self.speech_end, "ff_start": self.ff_start, "ff_end": self.ff_end,
                "duration": self.duration, "segs": [[a, b, self.seg_offset(a)] for a, b in self.segs],
                "shots": [[a, b, c, f, self.e(a), self.e(b)] + z for a, b, c, f, *z in self.cfg["shots"]],
                "wipes": [[s, self.e(s)] for s in self.cfg["wipes"]]}
