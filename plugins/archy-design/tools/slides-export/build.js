// Paper artboard specs -> .pptx
//
// Canvas 1920x1080 px maps onto an 18 x 10 in slide, the slide size of the v2 source
// deck, so generated slides mix into it without rescaling.
//
// The map is by WIDTH, not by height, because the two are not the same shape: the canvas
// is 16:9 (1.7778) and an 18x10 slide is 1.8. Scaling 1920 px to 18 in puts the content
// column's margins at a symmetric 0.9 in and sends y=1080 to 10.125 in - 0.125 in past
// the bottom edge. Nothing is lost there: the foot-cap Ruler sits at y=1056 (9.9 in) and
// everything below it is margin. Mapping by height instead would fit 1080 px into 10 in
// but leave 0.22 in of dead width on the right, so the design would stop filling the frame.
//
// Conversion constants, both exact:
//   1 canvas px = 0.675 pt  (1920 px = 1296 pt = 18 in)
//   1 canvas px = 3/320 in
// Font sizes and line heights are canvas px in the spec and converted here, so the
// specs stay readable against Paper's own values and CLAUDE.md's type scale.
//
//   node build.js specs.js archy-deck-templates.pptx   # every spec, one slide each
//   node build.js spec-03.json 03-metrics.pptx         # a single JSON spec
//
// Paths: see archywork.js. A relative output lands in the work directory ($ARCHY_WORK or
// --work=DIR), never beside this script. Image `src` values ("assets/...") resolve
// against the work directory first and fall back to the generic set in assets-base/.
// pptxgenjs is loaded from the work/base directory's node_modules, not from here.

const fs = require("fs");
const path = require("path");
const W = require("./archywork");
const PptxGenJS = W.requireDep("pptxgenjs");

const SLIDE_IN = { w: 18, h: 10 };      // v2 source deck slide size
const PX_TO_IN = SLIDE_IN.w / 1920;     // 3/320 - map by width, see header
const PX_TO_PT = PX_TO_IN * 72;         // 0.675

const inch = (px) => px * PX_TO_IN;
const pt = (px) => px * PX_TO_PT;

function addSpec(pres, spec, pageNumber) {
  const slide = pres.addSlide();
  slide.background = { color: spec.background };

  for (const it of spec.items) {
    // The meta page number is derived from position, never authored. Fourteen hand-typed
    // numbers is the same staleness trap as numbering the artboards: reorder anything and
    // they all lie. The Paper templates carry "NN" and this fills in the truth.
    if (it.layer === "Meta Page") {
      slide.addText(String(pageNumber).padStart(2, "0"), {
        x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h),
        isTextBox: true, margin: 0, fontFace: it.font, fontSize: pt(it.size),
        color: it.color, lineSpacing: pt(it.line), valign: "top", fit: "none",
        charSpacing: (it.track || 0) * it.size * PX_TO_PT,
      });
      continue;
    }

    // Opacity travels as `transparency` (0-100), never as an 8-digit hex: an alpha
    // channel in the colour string corrupts the file. A white-at-0.3 Ruler on a dark
    // ground is the common case.
    const fillOf = (item) => it.transparency
      ? { color: item.fill, transparency: item.transparency }
      : { color: item.fill };

    // A tilted scrapbook card. pptxgenjs spins a shape about its own centre in degrees,
    // clockwise - the same sense and sign as CSS `rotate` with transform-origin 50% 50%,
    // so the angle carries straight across and paper2spec has already swung each leaf's
    // centre into place.
    const spun = (o) => (it.rot ? { ...o, rotate: it.rot } : o);

    if (it.type === "rect") {
      slide.addShape(pres.ShapeType.rect, spun({
        x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h),
        fill: fillOf(it),
        line: { type: "none" },
      }));
      continue;
    }

    if (it.type === "ellipse") {
      slide.addShape(pres.ShapeType.ellipse, spun({
        x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h),
        fill: fillOf(it),
        line: { type: "none" },
      }));
      continue;
    }

    if (it.type === "pill") {
      // rectRadius only works on ROUNDED_RECTANGLE, never on RECTANGLE.
      slide.addShape(pres.ShapeType.roundRect, spun({
        x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h),
        fill: fillOf(it),
        line: { type: "none" },
        rectRadius: inch(it.h / 2),
      }));
      continue;
    }

    if (it.type === "line") {
      // A straight segment between two points. pptxgenjs draws a line from (x,y) to
      // (x+w, y+h); flipV makes it climb instead of fall, which is how an upward slope
      // is expressed. Used for the polyline in `Line / Area` and the waterfall connectors.
      const up = it.y2 < it.y1;
      slide.addShape(pres.ShapeType.line, {
        x: inch(Math.min(it.x1, it.x2)),
        y: inch(Math.min(it.y1, it.y2)),
        w: inch(Math.abs(it.x2 - it.x1)),
        h: inch(Math.abs(it.y2 - it.y1)),
        line: { color: it.color, width: pt(it.width || 4) },
        flipV: up,
      });
      continue;
    }

    if (it.type === "polygon") {
      // The area wash under a line. pptxgenjs has no polygon primitive; custGeom with a
      // points array is the only route, and validate.py is what confirms PowerPoint
      // accepts the geometry it writes.
      slide.addShape(pres.ShapeType.custGeom, {
        x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h),
        points: it.points.map(([px, py]) => ({ x: inch(px), y: inch(py) })),
        fill: { color: it.fill },
        line: { type: "none" },
      });
      continue;
    }

    if (it.type === "image") {
      // Slides cannot take SVG, so the wordmark and the Hugeicons come in as PNG
      // exported from Paper at 4x.
      const img = {
        path: W.asset(it.src),
        // pptxgenjs writes the path into the picture's alt text when none is given. Keep
        // the spec's own relative src there, so no machine's absolute path ships in a deck.
        altText: it.src,
        x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h),
      };
      // Paper crops a photo with background-size; pptx stretches to the box unless told
      // otherwise, so the crop has to be carried across or the picture distorts.
      // A circular portrait. pptxgenjs crops the picture to an ellipse rather than
      // drawing a shape over it, so the mask survives as a real picture in Slides.
      if (it.round) img.rounding = true;
      if (it.rot) img.rotate = it.rot;
      if (it.crop) {
        // The visible window, expressed against the image's own displayed box: `w`/`h`
        // above stay the full picture so the scale is right, and sizing carries the part
        // of it that shows.
        img.sizing = {
          type: "crop",
          x: inch(it.crop.x), y: inch(it.crop.y),
          w: inch(it.crop.w), h: inch(it.crop.h),
        };
      } else if (it.fit) {
        img.sizing = { type: it.fit, w: inch(it.w), h: inch(it.h) };
      }
      slide.addImage(img);
      continue;
    }

    if (it.type === "text") {
      // Two shapes of text item:
      //   it.text  -> a single run
      //   it.runs  -> several runs in ONE paragraph, each with its own colour.
      // The two-tone headline is the second kind. CLAUDE.md describes that device as a
      // mid-sentence colour split and notes the two stacked nodes are a Paper
      // limitation, not the design - OOXML runs express the real intent. An explicit
      // breakLine between runs keeps the colour split and the line break at the same
      // place, so re-writing the copy cannot slide the colour boundary mid-line.
      const body = it.runs
        ? it.runs.map((r, i) => ({
            text: it.upper ? r.text.toUpperCase() : r.text,
            // `stack: false` is the one-line headline: the halves belong in the same
            // paragraph separated by a space, not on two lines.
            options: {
              color: r.color,
              // A run may carry its own face: a one-line headline can change weight
              // mid-sentence ("Bold lead. Grey continuation") and still be one field.
              ...(r.font && r.font !== it.font ? { fontFace: r.font } : {}),
              breakLine: it.stack !== false && i < it.runs.length - 1,
            },
          }))
        : it.upper
        ? it.text.toUpperCase()
        : it.text;

      // Fresh options object every call: pptxgenjs mutates these in place.
      const opts = {
        x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h),
        isTextBox: true,
        margin: 0, // kill the built-in inset or nothing lines up with the Rulers
        fontFace: it.font,
        fontSize: pt(it.size),
        valign: "top",
        align: it.align || "left",
        fit: "none",
        wrap: it.wrap !== false,
      };
      if (it.rot) opts.rotate = it.rot;

      // "line" is either canvas px (exact point spacing, mirroring Paper's line-height)
      // or the string "single" (100%, letting the font's own metrics govern). Headlines
      // use "single"; wrapping body copy keeps its exact spacing, because 22/32 is a
      // deliberately open measure in the type scale and single would tighten it to ~1.2x.
      // The 128/128 Cover-title tier also stays exact - it is set solid by design.
      if (it.line === "single") opts.lineSpacingMultiple = 1;
      else opts.lineSpacing = pt(it.line);

      // letterSpacing is silently ignored; charSpacing is the real option, in points.
      if (it.track) opts.charSpacing = it.track * it.size * PX_TO_PT;
      // A per-run colour would be overridden by a paragraph-level one.
      if (!it.runs) opts.color = it.color;

      slide.addText(body, opts);
      continue;
    }

    throw new Error(`unknown item type: ${it.type}`);
  }

  return spec.items.length;
}

// The library's seven categories, in the order they read as a deck. This is a template
// library, so slides come out grouped by category rather than in presentation order -
// the same grouping as the Paper pages.
const CATEGORY_ORDER = [
  "Frames", "Numbers", "Charts", "Lists", "Comparisons", "Proof", "Showcase",
];

function main() {
  const [specArg, outArg] = process.argv.slice(2);
  if (!specArg) {
    console.error("usage: node build.js <specs.js | spec.json> [out.pptx]");
    process.exit(1);
  }

  const pres = new PptxGenJS();
  // A custom layout, not LAYOUT_16x9: the v2 deck is 18 x 10 in (ratio 1.8), which is not
  // one of pptxgenjs's presets. Must be defined and set before the first addSlide.
  pres.defineLayout({ name: "ARCHY_18x10", width: SLIDE_IN.w, height: SLIDE_IN.h });
  pres.layout = "ARCHY_18x10";

  let specs;
  if (specArg.endsWith(".json")) {
    // One spec, or an array of them - paper2spec.js emits an array so a whole Paper page
    // converts in one pass and stays in canvas order.
    const parsed = JSON.parse(fs.readFileSync(W.input(specArg), "utf8"));
    const list = Array.isArray(parsed) ? parsed : [parsed];
    specs = list.map((spec) => ({ category: null, spec }));
  } else {
    const mod = require(W.input(specArg));
    // --only key,key builds just those exports, in the order given. Used for side-by-side
    // comparisons rather than for producing the library.
    const only = process.argv.slice(2).find((a) => a.startsWith("--only="));
    if (only) {
      specs = only.slice(7).split(",").map((k) => {
        if (!mod[k]) throw new Error(`no spec exported as "${k}"`);
        return { category: "Selection", spec: mod[k] };
      });
    } else {
      specs = CATEGORY_ORDER.flatMap((cat) =>
        Object.values(mod.categories[cat] || {}).map((spec) => ({ category: cat, spec })));
      const empty = CATEGORY_ORDER.filter((c) => !Object.keys(mod.categories[c] || {}).length);
      if (empty.length) console.log(`empty categories: ${empty.join(", ")}`);
    }
  }

  let shapes = 0;
  let lastCat = null;
  for (const { category, spec } of specs) {
    if (category !== lastCat) {
      console.log(`${category}`);
      lastCat = category;
    }
    shapes += addSpec(pres, spec, pres.slides.length + 1);
    console.log(`  ${String(pres.slides.length).padStart(2, "0")}  ${spec.name}`);
  }

  const out = W.output(outArg || path.basename(specArg).replace(/\.(json|js)$/, "") + ".pptx");
  fs.mkdirSync(path.dirname(out), { recursive: true });
  return pres.writeFile({ fileName: out }).then(() => {
    console.log(`wrote ${out}  (${specs.length} slides, ${shapes} shapes)`);
  });
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
