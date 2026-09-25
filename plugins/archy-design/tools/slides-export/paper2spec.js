// Paper artboard -> build.js spec, mechanically.
//
// The 55-layout library in specs.js is hand-written, because those layouts are the design
// system and writing them out by hand is how they got verified. The Offsite deck is the
// opposite case: ~56 one-off artboards that already exist on the canvas and only need to
// come back out. Hand-writing those specs would be transcription, not design, so this
// reads Paper's own resolved values instead.
//
// Three inputs per artboard, all straight from the MCP with no interpretation:
//
//   tree     get_tree_summary(depth 10)  -> id, component, name, w x h, text content
//   styles   get_computed_styles([ids])   -> fontSize, colour, fill, display, gap, ...
//   coords   get_children(frame)          -> worldX / worldY, for spot-checks only
//
// Every SIZE is Paper's own resolved value, never computed here - which is what makes the
// position pass safe. Laying out a flex line is trivial once the children's widths and
// heights are known; the hard half of flexbox is measuring wrapped text, and Paper has
// already done it. So this places boxes it does not measure.
//
// `coords` overrides a computed position for any id it names. Use it to pin anything this
// does not model (a rotation, a hand-dragged translate) and as the regression check: the
// Cover ships with all fifteen of its real world positions, so a change here that breaks
// placement fails loudly instead of shifting a slide by twelve pixels unseen.
//
//   node paper2spec.js dump/<slide>.json  > spec.json
//   node paper2spec.js dump/              > specs-offsite.json   (a whole page)

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
// Paths: tokens.json is the tool's own (beside this file); every image an asset path
// names ("assets/...") is looked up in the work directory, then in assets-base/.
const W = require("./archywork");

// --------------------------------------------------------------------------- tokens

const TOKENS = JSON.parse(
  fs.readFileSync(path.join(__dirname, "tokens.json"), "utf8")
);

// "var(--color-white)" / "#FFF" / "rgb(1, 61, 245)" -> "FFFFFF", no leading #.
// build.js rejects a "#" and an 8-digit hex outright: both corrupt the file.
// The alpha of an 8-digit hex or an rgba(), as a pptx `transparency` (0-100). Paper
// writes a translucent fill as "#FFFFFF2E" - white at 18% - and hex() drops the alpha, so
// without this the disc on the blue stage comes out solid white.
function alphaOf(value) {
  const v = String(value || "").trim();
  const rgba = v.match(/rgba\(([^)]+)\)/i);
  if (rgba) {
    const parts = rgba[1].split(",");
    if (parts.length === 4) return Math.round((1 - parseFloat(parts[3])) * 100);
    return 0;
  }
  const m = v.replace(/^#/, "");
  if (/^[0-9a-f]{8}$/i.test(m)) {
    return Math.round((1 - parseInt(m.slice(6), 16) / 255) * 100);
  }
  return 0;
}

function hex(value) {
  if (!value) return null;
  let v = String(value).trim();

  const varMatch = v.match(/var\((--[a-z0-9-]+)\)/i);
  if (varMatch) {
    const tok = TOKENS[varMatch[1]];
    if (!tok) throw new Error(`unknown token ${varMatch[1]}`);
    v = tok;
  }

  const rgb = v.match(/rgba?\(([^)]+)\)/i);
  if (rgb) {
    const [r, g, b] = rgb[1].split(",").map((n) => parseFloat(n));
    return [r, g, b].map((n) => Math.round(n).toString(16).padStart(2, "0")).join("").toUpperCase();
  }

  v = v.replace(/^#/, "");
  if (v.length === 3) v = v.split("").map((c) => c + c).join("");
  if (v.length === 8) v = v.slice(0, 6);            // drop alpha, carried as transparency
  if (!/^[0-9a-f]{6}$/i.test(v)) return null;
  return v.toUpperCase();
}

const px = (v, fallback = null) => {
  if (v === undefined || v === null) return fallback;
  let str = String(v);
  // Lengths come through as tokens as readily as colours do - border-radius is usually
  // var(--radius-pill), and parseFloat on that is NaN, which silently squares a pill.
  const tok = str.match(/var\((--[a-z0-9-]+)\)/i);
  if (tok && TOKENS[tok[1]]) str = TOKENS[tok[1]];
  const n = parseFloat(str);
  return Number.isFinite(n) ? n : fallback;
};

// A length that may be a percentage of the box it sits in. `top: 50%` paired with
// `translate: 0 -50%` is how the deck centres a Content frame vertically, so both halves
// have to resolve or the block lands 500px high.
const lenOf = (v, basis, fallback = 0) => {
  if (v === undefined || v === null) return fallback;
  const str = String(v).trim();
  if (str.endsWith("%")) return (parseFloat(str) / 100) * basis;
  return px(str, fallback);
};

// "0 -50%" / "12px 0" / "-50%" -> [x, y] against the node's own box.
const translateOf = (v, w, h) => {
  if (!v || v === "none") return [0, 0];
  const parts = String(v).trim().split(/\s+/);
  return [lenOf(parts[0], w, 0), lenOf(parts[1] !== undefined ? parts[1] : parts[0], h, 0)];
};

// The exporter wants the per-weight family names Google Slides itself uses - "Onest
// SemiBold", not Onest with a bold flag. Paper stores them hyphenated in the stack.
function fontFace(fontFamily, weight) {
  const first = String(fontFamily || "").split(",")[0].replace(/["']/g, "").trim();
  // Paper stores the per-weight face hyphenated ("Onest-SemiBold"). Google Slides wants it
  // spaced - and the 400 weight is just the family name there, never "Onest Regular",
  // which does not resolve and silently falls back.
  if (first && first.includes("-")) return first.replace(/-Regular$/, "").replace(/-/g, " ");
  // A node built by `write_html` comes back with the BARE family and the weight beside it:
  // Paper normalises `font-family: Inter-Medium` to `"Inter", system-ui` + fontWeight 500,
  // and setting the hyphenated face back on it is a silent no-op. Reading the weight is
  // therefore the only way to recover the face - without it a 96px SemiBold title exports
  // as regular Inter and nobody notices until it is on the projector.
  const FACE = { 500: " Medium", 600: " SemiBold", 700: " Bold" };
  if (first) return first + (FACE[Number(weight)] || "");
  return Number(weight) >= 600 ? "Inter SemiBold" : "Inter";
}

// --------------------------------------------------------------------- tree parsing

// One node per line, indented two spaces per level:
//   `    Text "Meta Copyright" (8-0) 146×22 "ARCHY © 2026"`
// A text node's content can itself contain newlines, so a line that does not match the
// node pattern is a continuation of the string opened on the line before it.
// get_tree_summary cuts a text node's content at this many characters.
const TRUNCATION_LIMIT = 60;

const NODE_RE = /^(\s*)(\w+)\s+"((?:[^"\\]|\\.)*)"\s+\(([\w-]+)\)\s+([\d.]+)×([\d.]+)(?:\s+"([\s\S]*))?$/;

function parseTree(summary) {
  const nodes = [];
  let open = null; // node whose text string is still unterminated

  for (const line of summary.split("\n")) {
    if (open) {
      open.text += "\n" + line;
      if (line.endsWith('"')) {
        open.text = open.text.slice(0, -1);
        open = null;
      }
      continue;
    }

    const m = line.match(NODE_RE);
    if (!m) continue;

    const node = {
      depth: m[1].length / 2,
      component: m[2],
      name: m[3],
      id: m[4],
      w: parseFloat(m[5]),
      h: parseFloat(m[6]),
      text: null,
    };

    if (m[7] !== undefined) {
      if (m[7].endsWith('"')) node.text = m[7].slice(0, -1);
      else {
        node.text = m[7];
        open = node;
      }
    }

    nodes.push(node);
  }

  // depth -> parent, so a container can be told from a leaf
  const stack = [];
  for (const n of nodes) {
    stack[n.depth] = n;
    n.parent = n.depth > 0 ? stack[n.depth - 1] : null;
    n.children = [];
    if (n.parent) n.parent.children.push(n);
  }

  return nodes;
}

// ------------------------------------------------------------------ item conversion

// A local image arrives as backgroundImage: url("file:///…/Deck%20Assets/x.png").
// pptx needs a real path, so undo the percent-encoding and drop the scheme.
// pptxgenjs supports no gradient fill at all, so a gradient ground is embedded as a
// bitmap that make-gradients.py renders - keyed by a hash of the CSS, so the dump keeps
// the declaration Paper reported and the two cannot drift apart.
function gradientPath(backgroundImage) {
  const m = String(backgroundImage || "").match(/linear-gradient\([^()]*(?:\([^()]*\)[^()]*)*\)/);
  if (!m) return null;
  const key = crypto.createHash("sha1").update(m[0]).digest("hex").slice(0, 12);
  return `assets/gradients/${key}.png`;
}

function imagePath(backgroundImage) {
  const raw = String(backgroundImage || "");

  // A picture dropped onto the canvas is uploaded, so Paper reports its own CDN URL and
  // not the path it came from. fetch-photos.py caches those under assets/photos by asset
  // id; pptx needs real bytes on disk either way.
  const hosted = raw.match(/url\(\s*["']?https:\/\/app\.paper\.design\/file-assets\/[\w-]+\/([\w-]+)\.(\w+)["']?\s*\)/);
  if (hosted) return `assets/photos/${hosted[1]}.${hosted[2]}`;

  const local = raw.match(/url\(\s*["']?(file:\/\/[^"')]+)["']?\s*\)/);
  if (local) return decodeURIComponent(local[1].replace(/^file:\/\//, ""));
  return null;
}


// ------------------------------------------------------------------- intrinsic sizes

// `background-size: cover` is only resolvable against the picture's own dimensions, and
// the deck depends on it: slide 12 puts ONE screenshot into two boxes at two different
// `background-position` values - a nav strip and a hero - so getting this wrong shows the
// same band of the image twice. Reading a JPEG/PNG header is cheaper than a dependency.
const sizeCache = new Map();

function imageSize(file) {
  if (sizeCache.has(file)) return sizeCache.get(file);
  let out = null;
  try {
    const buf = fs.readFileSync(W.asset(file));
    if (buf.length > 24 && buf.readUInt32BE(0) === 0x89504e47) {
      out = { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };       // PNG IHDR
    } else if (buf[0] === 0xff && buf[1] === 0xd8) {                     // JPEG
      let i = 2;
      while (i < buf.length - 9) {
        if (buf[i] !== 0xff) { i++; continue; }
        const marker = buf[i + 1];
        // SOF0..SOF15, excluding the DHT/JPG/DAC markers that share the range
        if (marker >= 0xc0 && marker <= 0xcf &&
            marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc) {
          out = { h: buf.readUInt16BE(i + 5), w: buf.readUInt16BE(i + 7) };
          break;
        }
        i += 2 + buf.readUInt16BE(i + 2);
      }
    }
  } catch (e) { out = null; }
  sizeCache.set(file, out);
  return out;
}

// "50% 48%" / "50%" / "left top" -> fractions of the overflow, the way CSS resolves a
// percentage background-position: 0% pins the top edge, 100% the bottom.
function positionOf(v) {
  const parts = String(v || "50% 50%").trim().split(/\s+/);
  const one = (t, fallback) => {
    if (t === undefined) return fallback;
    if (t === "left" || t === "top") return 0;
    if (t === "right" || t === "bottom") return 1;
    if (t === "center") return 0.5;
    if (String(t).endsWith("%")) return parseFloat(t) / 100;
    return fallback;
  };
  return [one(parts[0], 0.5), one(parts[1], 0.5)];
}

function isHidden(s) {
  return s.display === "none" || px(s.opacity, 1) === 0;
}

// A frame paints if it has a fill or an image; otherwise it is pure layout and only its
// children reach the slide.
function paints(s) {
  return Boolean(
    (s.backgroundColor && s.backgroundColor !== "transparent" && hex(s.backgroundColor)) ||
    imagePath(s.backgroundImage) || gradientPath(s.backgroundImage) ||
    px(s.borderWidth, 0) || px(s.borderTopWidth, 0) || px(s.borderRightWidth, 0) ||
    px(s.borderBottomWidth, 0) || px(s.borderLeftWidth, 0)
  );
}


// ------------------------------------------------------------------ layout resolution

// CLAUDE.md: "A frame's children stay absolute until the frame is `display: flex`."
// So a frame is one of exactly two things, and both are cheap:
//
//   not flex -> every child is absolutely positioned; read its own left/top
//   flex     -> one line of children along the main axis, gap between them
//
// Nothing wraps (no flex-wrap anywhere in the deck) and no child is flex-sized in a way
// that changes its measured box, because the measured box is what the tree already
// reports. That leaves only where each box goes.
function resolveLayout(nodes, styles, coords) {
  const pos = {};
  const clip = {};   // id -> the [x, y, w, h] its nearest `overflow: clip` ancestor allows
  const spin = {};   // id -> {cx, cy, deg} of the nearest rotated ancestor, in world coords

  const walk = (frame, originX, originY, clipRect, spinning) => {
    pos[frame.id] = [originX, originY];
    if (clipRect) clip[frame.id] = clipRect;
    if (spinning) spin[frame.id] = spinning;
    // A rotated frame becomes the pivot for everything under it. The layout position Paper
    // reports is the box BEFORE the transform, so the resolver does the turn itself - the
    // same deal as `translate` and `top: 50%`. pptx rotates a shape about its own centre,
    // so what has to be carried is the pivot, and each leaf's own centre gets swung around
    // it. Only one level is modelled: nested rotation never appears in the deck, and
    // composing it silently would be worse than refusing.
    const deg = parseFloat(String((styles[frame.id] || {}).rotate || ""));
    if (deg) {
      if (spinning) throw new Error(`nested rotation on ${frame.id} "${frame.name}" \u2014 not modelled`);
      // Paper NORMALISES transform-origin to `0% 0%` - author it as `50% 50%` and read it
      // back and it says `0% 0%`, silently. So the pivot is the frame's TOP-LEFT corner,
      // never its centre. (This is the same thing the badge note records: the rendered box
      // is offset from left/top, and by how much depends on the size and the angle.)
      const origin = String((styles[frame.id] || {}).transformOrigin || "0% 0%");
      if (!/^\s*0%\s+0%\s*$/.test(origin)) {
        throw new Error(`${frame.name}: rotate assumes transform-origin 0% 0%, got "${origin}"`);
      }
      spinning = { cx: originX, cy: originY, deg };
      spin[frame.id] = spinning;
    }
    // A frame that clips becomes the window for everything under it. This is how the deck
    // reframes a photo: an oversized image rect at a negative offset inside a smaller
    // frame. pptx has no clipping container, so the window has to become a crop.
    const own = (styles[frame.id] || {}).overflow;
    if (own === "clip" || own === "hidden") {
      const box = [originX, originY, frame.w, frame.h];
      clipRect = clipRect ? intersect(clipRect, box) : box;
    }
    const kids = frame.children;
    if (!kids.length) return;

    const fs = styles[frame.id] || {};
    // Paper reports the shorthand it was authored with, so paddingInline / paddingBlock
    // turn up as often as the long-hand ones. Missing one silently shifts a whole cell.
    const pad = px(fs.padding, 0);
    const padX = px(fs.paddingInline, pad);
    const padY = px(fs.paddingBlock, pad);
    const padT = px(fs.paddingTop, padY);
    const padR = px(fs.paddingRight, padX);
    const padB = px(fs.paddingBottom, padY);
    const padL = px(fs.paddingLeft, padX);

    if (fs.display !== "flex") {
      // Two kinds of child, and the difference is the padding. An absolutely positioned
      // one resolves against the PADDING box, so padding does not move it - that is every
      // Ruler and every pinned Content frame. A static one is ordinary block flow inside
      // the CONTENT box, so padding does move it: that is the 12px white mat behind a
      // photo, and reading it the other way puts the picture over its own border.
      let flowY = originY + padT;
      for (const k of kids) {
        const ks = styles[k.id] || {};
        const [tx, ty] = translateOf(ks.translate, k.w, k.h);
        if (ks.position === "absolute" || ks.position === "fixed") {
          walk(k, originX + lenOf(ks.left, frame.w) + tx,
                  originY + lenOf(ks.top, frame.h) + ty, clipRect, spinning);
        } else {
          walk(k, originX + padL + lenOf(ks.left, frame.w) + tx, flowY + ty, clipRect, spinning);
          flowY += k.h;
        }
      }
      return;
    }

    // An absolutely positioned child of a FLEX container is out of flow too - CSS resolves
    // it against the padding box exactly as in a block container, and flexbox never sees
    // it. Laying it out as a flex item instead stacks it along the main axis: slide 34's
    // six pinned bar frames came out in a vertical pile at one x, every one of them
    // "correct" in isolation. Partition first, then run the flex maths on what is left.
    const flowKids = [];
    for (const k of kids) {
      const ks = styles[k.id] || {};
      if (ks.position === "absolute" || ks.position === "fixed") {
        const [tx, ty] = translateOf(ks.translate, k.w, k.h);
        walk(k, originX + lenOf(ks.left, frame.w) + tx,
                originY + lenOf(ks.top, frame.h) + ty, clipRect, spinning);
      } else {
        flowKids.push(k);
      }
    }
    if (!flowKids.length) return;

    const col = String(fs.flexDirection || "row").startsWith("column");
    const gap = px(fs.gap, px(fs.rowGap, 0));
    const justify = fs.justifyContent || "flex-start";
    const align = fs.alignItems || "stretch";

    const innerX = originX + padL;
    const innerY = originY + padT;
    const innerW = frame.w - padL - padR;
    const innerH = frame.h - padT - padB;

    const mainSize = (k) => (col ? k.h : k.w);
    const crossSize = (k) => (col ? k.w : k.h);
    const innerMain = col ? innerH : innerW;
    const innerCross = col ? innerW : innerH;

    // A child can carry its own margin - an icon with `margin-bottom: 8px` is how the
    // deck opens a gap under one item without changing the column's gap for all of them.
    // Ignoring it walks everything below that child up by exactly that much.
    const marginBefore = (k) => {
      const ks = styles[k.id] || {};
      const v = col ? ks.marginTop : ks.marginLeft;
      return v === "auto" ? 0 : px(v, 0);
    };
    const marginAfter = (k) => {
      const ks = styles[k.id] || {};
      const v = col ? ks.marginBottom : ks.marginRight;
      return v === "auto" ? 0 : px(v, 0);
    };

    const total = flowKids.reduce((a, k) => a + mainSize(k) + marginBefore(k) + marginAfter(k), 0)
                  + gap * (flowKids.length - 1);
    const slack = innerMain - total;

    // `margin-<start>: auto` on a child eats all the slack before it - the bottom-anchor
    // trick the deck uses to hold a quote attribution on one lane whatever the quote does.
    const autoIndex = flowKids.findIndex((k) => {
      const ks = styles[k.id] || {};
      return (col ? ks.marginTop : ks.marginLeft) === "auto";
    });

    let cursor = 0;
    let between = gap;
    if (autoIndex === -1) {
      if (justify === "center") cursor = slack / 2;
      else if (justify === "flex-end" || justify === "end") cursor = slack;
      else if (justify === "space-between" && flowKids.length > 1) between = gap + slack / (flowKids.length - 1);
      else if (justify === "space-around" && flowKids.length) {
        between = gap + slack / flowKids.length;
        cursor = (slack / flowKids.length) / 2;
      }
      else if (justify === "space-evenly" && flowKids.length) {
        between = gap + slack / (flowKids.length + 1);
        cursor = slack / (flowKids.length + 1);
      }
    }

    flowKids.forEach((k, i) => {
      if (i === autoIndex) cursor += slack;

      const ks = styles[k.id] || {};
      const selfAlign = ks.alignSelf && ks.alignSelf !== "auto" ? ks.alignSelf : align;
      let cross = 0;
      if (selfAlign === "center") cross = (innerCross - crossSize(k)) / 2;
      else if (selfAlign === "flex-end" || selfAlign === "end") cross = innerCross - crossSize(k);

      cursor += marginBefore(k);

      const [tx, ty] = translateOf(ks.translate, k.w, k.h);
      const crossMargin = col ? px(ks.marginLeft === "auto" ? 0 : ks.marginLeft, 0)
                              : px(ks.marginTop === "auto" ? 0 : ks.marginTop, 0);
      const x = (col ? innerX + cross + crossMargin : innerX + cursor) + tx;
      const y = (col ? innerY + cursor : innerY + cross + crossMargin) + ty;
      walk(k, x, y, clipRect, spinning);

      cursor += mainSize(k) + marginAfter(k) + between;
    });
  };

  const root = nodes.find((n) => n.depth === 0);
  walk(root, 0, 0, null);

  // An explicit coord always wins: it is measured, and this is inferred. A disagreement
  // is reported before it is applied - silently correcting one would hide the case this
  // resolver cannot model, which is exactly what the pinned coords exist to catch.
  for (const [id, xy] of Object.entries(coords)) {
    const got = pos[id];
    if (got && (Math.abs(got[0] - xy[0]) > 1 || Math.abs(got[1] - xy[1]) > 1)) {
      console.error(`  ~ ${id}: resolved ${got.map(Math.round)} but measured ${xy} \u2014 pinned`);
    }
    pos[id] = xy;
  }
  return { pos, clip, spin };
}

function intersect(a, b) {
  const x = Math.max(a[0], b[0]);
  const y = Math.max(a[1], b[1]);
  const r = Math.min(a[0] + a[2], b[0] + b[2]);
  const bt = Math.min(a[1] + a[3], b[1] + b[3]);
  return [x, y, Math.max(0, r - x), Math.max(0, bt - y)];
}

// The two-tone headline: stacked Text nodes in a flex column at gap 0, all set in the
// same face at the same size, differing only in colour. That is Paper's workaround for
// not being able to colour part of a text node - CLAUDE.md calls it a colour split
// mid-sentence - so the export puts it back together as ONE text box with one run per
// line, which is what OOXML does natively. The team then edits one field, not two.
//
// The test is structural rather than by layer name, so a headline called something else
// still collapses, and a stack that only looks similar does not: `Session Stack` sits at
// gap 6 in two different faces and stays two items, which is correct.
function headlineRuns(frame, styles) {
  const kids = frame.children;
  if (kids.length < 2) return null;
  if (!kids.every((k) => k.component === "Text")) return null;

  const fs = styles[frame.id] || {};
  if (fs.display !== "flex") return null;

  // Two shapes, one device. A headline that wraps is a COLUMN at gap 0 - the two lines
  // are two nodes only because Paper cannot colour half a text node. A headline that fits
  // on one line is a ROW on the baseline, where the gap stands in for the word space
  // between the halves. Both are a colour split mid-sentence and both must come out as a
  // single editable field.
  const column = String(fs.flexDirection || "row").startsWith("column");
  if (column) {
    if (px(fs.gap, px(fs.rowGap, 0)) !== 0) return null;
  } else {
    // A sentence laid out as a row is aligned on the baseline, or centred when the two
    // halves share a size. Anything else is a layout of separate things, not a sentence.
    if (fs.alignItems !== "baseline" && fs.alignItems !== "center") return null;
  }

  const first = styles[kids[0].id] || {};
  const same = (k) => {
    const ks = styles[k.id] || {};
    return ks.fontSize === first.fontSize
        && ks.lineHeight === first.lineHeight
        && ks.textTransform === first.textTransform
        // A column is one headline in one face; only a one-line row is allowed to change
        // weight mid-sentence, which is how "Bold lead. Grey continuation" is built.
        && (!column || ks.fontFamily === first.fontFamily);
  };
  if (!kids.every(same)) return null;

  // Something has to actually differ, or there was never a split to express and these are
  // two deliberate paragraphs that must not be welded together.
  const colours = new Set(kids.map((k) => (styles[k.id] || {}).color));
  const faces = new Set(kids.map((k) => (styles[k.id] || {}).fontFamily));
  if (colours.size < 2 && faces.size < 2) return null;

  // An ordinal beside a label - "1" + "What we do" - passes every test above and is NOT
  // this device: it is two things laid out, not one sentence split by colour. Merging it
  // would also replace a 14px gap with a word space and pull the label left.
  //
  // The tell is position, not digits: an ordinal LEADS. A numeral anywhere else is part
  // of the sentence - "A day in the practice," / "2031." is a headline and must merge.
  if (/^\s*\d{1,3}\s*[.)·:-]?\s*$/.test(kids[0].text || "")) return null;

  return { face: first, column };
}

// A hairline border round a screenshot is the same device as a Ruler, and it arrives as
// CSS border properties rather than as child frames. pptx can outline a shape, but not
// with a different border per side - slide 12 frames a nav strip on three sides so the
// seam with the hero below it stays open - so each side is emitted as its own thin rect.
// That is also exactly how the deck draws every other hairline.
function borderItems(n, s, x, y) {
  const out = [];
  const all = px(s.borderWidth, 0);
  const allColor = s.borderColor;
  const sides = [
    ["Top",    x, y, n.w, null],
    ["Right",  x + n.w, y, null, n.h],
    ["Bottom", x, y + n.h, n.w, null],
    ["Left",   x, y, null, n.h],
  ];
  for (const [side, sx, sy, sw, sh] of sides) {
    const w = px(s["border" + side + "Width"], s.borderStyle || allColor ? all : 0);
    if (!w) continue;
    const style = s["border" + side + "Style"] || s.borderStyle;
    if (style === "none") continue;
    const fill = hex(s["border" + side + "Color"] || allColor);
    if (!fill) continue;
    out.push({
      type: "rect",
      layer: `${n.name} Border ${side}`,
      x: side === "Right" ? sx - w : sx,
      y: side === "Bottom" ? sy - w : sy,
      w: sw === null ? w : sw,
      h: sh === null ? w : sh,
      fill,
    });
  }
  return out;
}

function convert(dump) {
  const fsOf = (n) => (dump.styles || {})[n.id] || {};
  const nodes = parseTree(dump.tree);
  const styles = dump.styles || {};
  const { pos, clip, spin } = resolveLayout(nodes, styles, dump.coords || {});
  const items = [];

  const at = (n) => {
    const c = pos[n.id];
    if (!c) throw new Error(`${dump.name}: no world position for ${n.id} "${n.name}"`);
    const sp = spin[n.id];
    if (!sp) return { x: Math.round(c[0]), y: Math.round(c[1]) };
    const t = (sp.deg * Math.PI) / 180;
    const dx = c[0] + n.w / 2 - sp.cx;
    const dy = c[1] + n.h / 2 - sp.cy;
    const rx = sp.cx + dx * Math.cos(t) - dy * Math.sin(t);
    const ry = sp.cy + dx * Math.sin(t) + dy * Math.cos(t);
    return { x: Math.round(rx - n.w / 2), y: Math.round(ry - n.h / 2), rot: sp.deg };
  };

  const consumed = new Set();

  // The artboard's own fill normally becomes `spec.background`, which cannot hold a
  // gradient - so a gradient ground goes in as a full-bleed image, and it has to be the
  // FIRST item or it covers the Rulers and the type.
  const rootNode = nodes.find((n) => n.depth === 0);
  const rootGrad = gradientPath((styles[rootNode.id] || {}).backgroundImage);
  if (rootGrad) {
    items.push({ type: "image", layer: "Ground", x: 0, y: 0,
                 w: rootNode.w, h: rootNode.h, src: rootGrad });
  }
  // Borders are collected as they are met and flushed at the very end. A frame's border
  // belongs ON TOP of what the frame holds, and in Paper the frame is met before its
  // children - so emitted in place, every hairline round a screenshot ends up underneath
  // the screenshot and invisible.
  const outlines = [];

  for (const n of nodes) {
    if (n.depth === 0) continue;                       // the artboard itself
    if (consumed.has(n.id)) continue;                  // folded into a headline above
    const s = styles[n.id] || {};
    if (isHidden(s)) continue;

    if (n.component === "Frame" && !paints(s)) {
      const merged = headlineRuns(n, styles);
      if (merged) {
        const { face, column } = merged;
        const kids = n.children;
        const rowGap = px(fsOf(n).gap, px(fsOf(n).columnGap, 0));
        const { x, y, rot } = at(kids[0]);
        const size = px(face.fontSize, 16);
        const item = {
          type: "text",
          layer: n.name,
          x, y,
          w: column
            ? Math.ceil(Math.max(...kids.map((k) => k.w))) + 2
            : Math.ceil(kids.reduce((a, k) => a + k.w, 0) + rowGap * (kids.length - 1)) + 8,
          h: column
            ? Math.ceil(kids.reduce((a, k) => a + k.h, 0))
            : Math.ceil(Math.max(...kids.map((k) => k.h))),
          runs: kids.map((k, i) => ({
            // On one line the gap between the nodes IS the word space, so it has to come
            // back as a real space - without it the two halves collide into one word.
            // Unless the row is at gap 0, which means the copy already carries its own
            // spaces: a bold word mid-sentence is written as "… book a " + "qualified" +
            // " demo …", and adding a space there would double it on both sides.
            text: ((dump.text && dump.text[k.id] !== undefined) ? dump.text[k.id] : (k.text || ""))
                  + (!column && rowGap > 0 && i < kids.length - 1 ? " " : ""),
            color: hex((styles[k.id] || {}).color) || "000000",
            font: fontFace((styles[k.id] || {}).fontFamily, (styles[k.id] || {}).fontWeight),
          })),
          stack: column,
          font: fontFace(face.fontFamily, face.fontWeight),
          size,
          // Paper's own leading, not "single": this deck is reviewed slide by slide
          // against the canvas, so leading that drifts from the design reads as a bug.
          line: px(face.lineHeight, Math.round(size * 1.3)),
        };
        const track = parseFloat(String(face.letterSpacing || "0"));
        if (track) item.track = track;
        if (face.textTransform === "uppercase") item.upper = true;
        if (face.textAlign === "center" || face.textAlign === "right") item.align = face.textAlign;
        if (rot) item.rot = rot;

        for (const k of kids) {
          consumed.add(k.id);
          if (k.text !== null && k.text !== undefined && k.text.length === TRUNCATION_LIMIT
              && !(dump.text && dump.text[k.id] !== undefined)) {
            throw new Error(`${dump.name}: ${k.id} "${k.name}" is truncated at ${TRUNCATION_LIMIT} chars \u2014 supply it in "text".`);
          }
        }
        console.error(`  = ${dump.name}: merged ${kids.length} lines into "${n.name}"`);
        items.push(item);
        continue;
      }
    }

    // An SVG on a slide is the wordmark or a Hugeicon. Slides cannot take SVG, so it goes
    // in as one of the PNGs build-assets.py generates; the node's own children are its
    // paths and never become shapes.
    if (n.component === "SVG") {
      const asset = dump.svgAssets && dump.svgAssets[n.id];
      if (!asset) {
        console.error(`  ! ${dump.name}: SVG ${n.id} "${n.name}" has no asset mapping \u2014 skipped`);
        continue;
      }
      const { x, y, rot } = at(n);
      const item = { type: "image", layer: n.name, x, y, w: n.w, h: n.h, src: asset };
      if (rot) item.rot = rot;
      // Vector art bleeds off an edge as readily as a photo does - the mascota runs off
      // the top - and the artboard's own `overflow: clip` is what cuts it.
      const win = clip[n.id];
      if (win) {
        const vis = intersect(win, [x, y, n.w, n.h]);
        if (Math.abs(vis[2] - n.w) > 0.5 || Math.abs(vis[3] - n.h) > 0.5) {
          if (vis[2] <= 0 || vis[3] <= 0) continue;
          item.crop = { x: vis[0] - x, y: vis[1] - y, w: vis[2], h: vis[3] };
          item.x = vis[0];
          item.y = vis[1];
        }
      }
      items.push(item);
      continue;
    }
    if (n.component === "SVGVisualElement") continue;  // a path inside an SVG

    if (n.component === "Text") {
      const { x, y, rot } = at(n);
      // get_tree_summary truncates a string at 60 characters with no ellipsis and no
      // flag, so a long line comes back looking like valid copy that just stops. Shipping
      // that is the `#1211` rendered as `#121` defect: wrong content, invisible on
      // review. Anything at the cutoff must be supplied in full via `text`, read with
      // get_node_info - this refuses rather than guessing.
      let copy = (dump.text && dump.text[n.id] !== undefined) ? dump.text[n.id] : n.text;
      if (copy === null || copy === undefined) copy = "";
      if (copy.length === TRUNCATION_LIMIT && !(dump.text && dump.text[n.id] !== undefined)) {
        throw new Error(
          `${dump.name}: ${n.id} "${n.name}" is exactly ${TRUNCATION_LIMIT} chars \u2014 ` +
          `get_tree_summary truncates there. Read it with get_node_info and put the ` +
          `full string in the dump's "text" map.`
        );
      }
      const size = px(s.fontSize, 16);
      const item = {
        type: "text",
        layer: n.name,
        x, y,
        // A max-content text node reports its ink width; give the box a little slack so a
        // re-typed string does not wrap at the exact character it fits today.
        w: Math.ceil(n.w) + 2,
        h: Math.ceil(n.h),
        text: copy,
        font: fontFace(s.fontFamily, s.fontWeight),
        size,
        line: px(s.lineHeight, Math.round(size * 1.3)),
        color: hex(s.color) || "000000",
      };
      const track = parseFloat(String(s.letterSpacing || "0"));
      if (track) item.track = track;
      if (s.textTransform === "uppercase") item.upper = true;
      if (s.textAlign === "center" || s.textAlign === "right") item.align = s.textAlign;
      // A single-line label must not reflow; only wrapping copy needs wrap on.
      if (s.whiteSpace === "pre" || s.width === "max-content") item.wrap = false;
      const op = px(s.opacity, 1);
      if (op < 1) item.transparency = Math.round((1 - op) * 100);
      if (rot) item.rot = rot;
      items.push(item);
      continue;
    }

    if (n.component === "Frame" || n.component === "Rectangle") {
      if (!paints(s)) continue;                        // layout-only container
      const { x, y, rot } = at(n);
      // A border sits on top of whatever the frame holds, so it is emitted last - but it
      // is collected first, because each branch below ends in a `continue`.
      const borders = borderItems(n, s, x, y);
      if (rot) for (const b of borders) b.rot = rot;
      // A fully rounded frame holding a photo is a circular portrait, and pptx can do that
      // - but only on the picture itself, so the radius has to travel with the image
      // rather than becoming a shape. Read it before the image branch consumes the node.
      const rounded = /infinity/i.test(String(s.borderRadius || "")) ||
                      px(s.borderRadius, 0) >= Math.min(n.w, n.h) / 2;

      const grad = gradientPath(s.backgroundImage);
      if (grad) {
        items.push({ type: "image", layer: n.name, x, y, w: n.w, h: n.h, src: grad });
        outlines.push(...borders);
        continue;
      }
      const src = imagePath(s.backgroundImage);
      if (src) {
        // Resolve `cover` / `contain` into the rectangle the picture actually occupies,
        // then let the clip pass below crop it - so ONE mechanism handles both reasons a
        // photo is cropped: the fit, and the frame that shows only part of it.
        //
        // This has to be exact, not approximate. Slide 12 puts a single screenshot into
        // two boxes at two different `background-position` values - a 66px nav strip at
        // 0% and a 386px hero at 48% - so a fit resolved by eye shows the same band twice.
        let box = [x, y, n.w, n.h];
        const size = String(s.backgroundSize || "");
        if (size === "cover" || size === "contain") {
          const nat = imageSize(src);
          if (!nat) {
            console.error(`  ! ${dump.name}: cannot read the size of ${src} \u2014 ` +
                          `"${n.name}" will be stretched instead of ${size}-fitted.`);
          } else {
            const pick = size === "cover" ? Math.max : Math.min;
            const scale = pick(n.w / nat.w, n.h / nat.h);
            const dw = nat.w * scale;
            const dh = nat.h * scale;
            const [fx, fy] = positionOf(s.backgroundPosition);
            box = [x - (dw - n.w) * fx, y - (dh - n.h) * fy, dw, dh];
          }
        }

        const win = clip[n.id];
        const window = win ? intersect(win, [x, y, n.w, n.h]) : [x, y, n.w, n.h];
        const vis = intersect(window, box);
        if (vis[2] <= 0 || vis[3] <= 0) continue;          // clipped away entirely

        const item = { type: "image", layer: n.name,
                       x: vis[0], y: vis[1], w: box[2], h: box[3], src };
        if (rounded && Math.abs(n.w - n.h) < 1) item.round = true;
        if (rot) item.rot = rot;
        if (Math.abs(vis[2] - box[2]) > 0.5 || Math.abs(vis[3] - box[3]) > 0.5) {
          item.crop = { x: vis[0] - box[0], y: vis[1] - box[1], w: vis[2], h: vis[3] };
        }
        items.push(item);
        outlines.push(...borders);
        continue;
      }
      if (!s.backgroundColor || !hex(s.backgroundColor)) {
        outlines.push(...borders);                       // a frame that is only an outline
        continue;
      }
      // Paper writes a fully rounded corner as `calc(infinity * 1px)`, which parseFloat
      // reads as NaN - and a NaN radius silently squares a circular portrait.
      const radiusRaw = String(s.borderRadius || "");
      const radius = /infinity/i.test(radiusRaw) ? Infinity : px(radiusRaw, 0);
      const item = {
        type: radius >= Math.min(n.w, n.h) / 2 ? (n.w === n.h ? "ellipse" : "pill") : "rect",
        layer: n.name,
        x, y, w: n.w, h: n.h,
        fill: hex(s.backgroundColor),
      };
      // Opacity and a fill alpha compound: a 50%-opaque layer holding a 50%-alpha fill
      // reads at 25%. pptx has one transparency per shape, so they are combined here.
      const op = px(s.opacity, 1);
      const alpha = alphaOf(s.backgroundColor) / 100;
      const clear = 1 - (1 - alpha) * op;
      if (clear > 0.005) item.transparency = Math.round(clear * 100);
      if (rot) item.rot = rot;
      items.push(item);
      outlines.push(...borders);
      continue;
    }
  }

  items.push(...outlines);

  // The artboard's own fill is the slide background, so it never becomes an item; read it
  // off the root unless the dump names one explicitly.
  const root = nodes.find((n) => n.depth === 0);
  const bg = dump.background || (styles[root.id] || {}).backgroundColor;
  return { name: dump.name, background: hex(bg) || "FFFFFF", items };
}

// ---------------------------------------------------------------------------- main

function main() {
  const targets = process.argv.slice(2);
  if (!targets.length) {
    console.error("usage: node paper2spec.js <dump.json | dump-dir/> [more.json ...]");
    process.exit(1);
  }

  // Several targets are accepted so a partial build - one slide, or a range - needs no
  // temporary directory: `export.sh` just hands over the dumps it selected.
  const files = targets.map(W.input).flatMap((t) => (fs.statSync(t).isDirectory()
    ? fs.readdirSync(t).filter((f) => f.endsWith(".json")).sort().map((f) => path.join(t, f))
    : [t]));

  const specs = files.map((f) => {
    const spec = convert(JSON.parse(fs.readFileSync(f, "utf8")));
    console.error(`  ${path.basename(f).padEnd(28)} ${String(spec.items.length).padStart(3)} items`);
    return spec;
  });

  process.stdout.write(JSON.stringify(specs, null, 2));
}

main();
