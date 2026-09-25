# Slides Export

Turns a deck layout designed in the Paper **Master - Decks** file into an editable `.pptx`, so the
team can open it in Google Slides and change copy without touching the design.

Paper exports only `png / jpg / webp / avif / pdf / svg` - there is no editable-text path
out of it. So the `.pptx` is *generated* from Paper's own values instead.

## Why this is cheap rather than a rewrite

`get_children` in the Paper MCP returns `worldX` / `worldY` for every node, which means
**Paper has already resolved the flex layout**. The generator flattens an artboard to
absolutely-positioned leaves and emits them one-for-one. It never reimplements flexbox.

## Paths

This folder ships inside the `archy-design` plugin and is replaced on every update, so
**nothing is ever written here**. Every script works in a work directory:

| | |
|---|---|
| `--work DIR` (or `--work=DIR`) | highest priority, on any script |
| `$ARCHY_WORK` | the project directory, e.g. `$BASE/<project>` |
| `$BASE` | used when neither is set |

`BASE` is `$ARCHY_WORK_BASE`, else `${CLAUDE_PLUGIN_DATA}/slides-export`, else
`./archy-work/slides-export`. Dumps (`dump/`), reads (`trees/ styles/ text/ assets/`, or the
same under `scratchpad/`), project assets (`assets/`) and every output `.pptx` live in the
work directory; a relative output path always lands there. The shared resolution is in
`archywork.js` / `archywork.py`.

Code lookups stay beside the code: `tokens.json`, and `assets-base/`, the generic images the
55-layout template library needs (the wordmark, the fourteen Hugeicons, `bk-fade-dark.png`).
An image a spec names as `assets/<file>` is taken from the work directory first and from
`assets-base/<file>` otherwise, so the library builds in an empty work directory.

## Setup (once per machine)

```bash
BASE="${CLAUDE_PLUGIN_DATA}/slides-export"
npm install --prefix "$BASE" pptxgenjs@3.12.0
python3 -m venv "$BASE/.venv"
"$BASE/.venv/bin/pip" install defusedxml lxml Pillow cairosvg "markitdown[pptx]"
```

`build.js` loads `pptxgenjs` from `node_modules` in the work directory, in `BASE`, or in the
work directory's parent (then `NODE_PATH`). `export.sh` picks the Python from `$ARCHY_PYTHON`,
else a `.venv` in the same three places, else `python3`.

## Build

```bash
TOOLS="${CLAUDE_PLUGIN_ROOT}/tools/slides-export"
export ARCHY_WORK="$BASE/templates"
node "$TOOLS/build.js" "$TOOLS/specs.js" archy-deck-templates.pptx
"$BASE/.venv/bin/python" "$TOOLS/postprocess.py" archy-deck-templates.pptx
```

`build-assets.py` regenerates the template assets into `<work>/assets/`; it only needs
running to change or add an icon, since `assets-base/` already holds its output.

Then drop the `.pptx` in Drive and open it with Google Slides.

**Both steps are required.** `postprocess.py` is not optional - see *Autofit* below.
`build.js` also accepts a single `.json` spec if you ever want one layout on its own.

## Assets

Google Slides cannot take SVG, so the wordmark on `Cover` / `Closing` and the Hugeicons in
`Product grid`, `Matrix` and `Icon List` go in as PNG. `build-assets.py` generates all
fifteen, plus the one scrim the deck needs, into `<work>/assets/` (a copy ships in
`assets-base/`):

- **Icons** come straight from the `@hugeicons/core-free-icons` npm package - the same
  source the `hugeicons` skill uses to put them on a canvas - so they are reproducible
  rather than hand-exported. It refuses to write an icon whose path data came back empty,
  which is the silent failure mode of that extraction. Two icons exist twice, once
  neutral and once royal (`icon-verify` / `icon-verify-royal`): `Product grid` draws them
  in `--color-neutral-light` because every cell there carries a state, and `Icon List`
  needs royal because none of them do.
- **`bk-fade-dark.png`** is the scrim for `Capture + Scrim` - a 1920 × 680 vertical
  gradient, transparent to `#00004E`, generated with Pillow. It is the only raster in the
  library that is not a logo or an icon, and it exists because pptxgenjs cannot fill a
  shape with a gradient.
- **The wordmark** is the 5-path mark off the Paper canvas, `viewBox "0 5 252 98"` in a
  `translate(0 21.752)` group. Its 252 × 98 ink matches its 360 × 140 placement exactly.
  Never take this mark from the Webflow `index.html`: that inline SVG is missing the
  counter of the "A" and renders as "∩rchy".

Paper's own `export` writes to `~/Downloads`, which macOS TCC blocks scripts from
reading - hence generating from source rather than exporting by hand.

## The two conversions, both exact

The slide is 18 × 10 in (16459200 × 9144000 EMU), mapped by width: 1920 px to 18 in. `build.js` defines this layout before the first slide. (An older investor deck used 10 × 5.625 in; that mapping is superseded.)

| Canvas px → | |
|---|---|
| Position and size | **× 8572.5 EMU**, or `px × 3/320` inches (18 × 10 in slide) |
| Font size and line height | **× 0.675 pt** - 128 → 86.4pt, 60 → 40.5pt, 22 → 14.85pt |
| Tracking (`em`) | `em × px × 0.675` pt, emitted as `charSpacing` |

## Fonts

Use the per-weight family names - `Onest`, `Onest SemiBold`, `Inter`, `Inter Medium`,
`Inter SemiBold` - and **never a bold flag**. Those are the exact names Google Slides
uses, which is how we know they resolve: the source deck came *out of* Google Slides, and
its embedded `ppt/fonts/Onest-regular.fntdata` files carry that exporter's signature.

## Writing a spec

All fifty-five live in `specs.js`, as a module rather than fifty-five JSON files, so the
parts that are identical by construction - the Rulers frame, the Meta line, the
three-part header - are written and verified **once**. That mirrors the design system (the `archy:brand` skill),
which says to derive a new light layout by duplicating `Metrics 2×2`, not by
rebuilding it. `meta()`, `eyebrow()`, `headline()`, `lightFrame()`, `footerFrame()`,
`captureSlot()` and `logoSlot()` are the shared pieces; each layout then supplies only its
own body data.

**Image slots** are `rect` items filled `EEEEEE` with a centred `CAPTURE` label -
`captureSlot()` builds the pair. A full-bleed slot fills `666666` instead so white type
and the white-at-0.3 Rulers read on it, and it must be the **first** item in the array or
it covers the Rulers, Meta and eyebrow.

Item types:

```jsonc
{ "type": "rect",    "x": 0, "y": 20, "w": 1920, "h": 2, "fill": "EEEEEE" }
{ "type": "ellipse", "x": 136, "y": 936, "w": 72, "h": 72, "fill": "CCEAFF" }  // portraits, dots
{ "type": "pill",    "x": 136, "y": 440, "w": 81, "h": 34, "fill": "E6F4FF" }  // Status pill
{ "type": "image",   "x": 1464, "y": 856, "w": 360, "h": 140, "src": "assets/archy-wordmark.png" }

{ "type": "text", "x": 148, "y": 544, "w": 700, "h": 96,
  "text": "…", "font": "Inter", "size": 22, "line": 32, "color": "666666" }
```

Everything is in **canvas px** and hex **without `#`** (a `#` or an 8-digit hex with alpha
corrupts the file). `"upper": true` uppercases the string, because OOXML has no
`text-transform` and Paper stores the untransformed text.

`"line"` takes either a number in canvas px - emitted as exact point spacing, mirroring
Paper's `line-height` - or the string `"single"`, which emits 100% and lets the font's own
metrics govern. **Headlines use `"single"`. Everything else uses the number.** Reviewed in
Slides, the headline reads better on Single, and it survives someone changing the size;
wrapping body copy must keep its exact spacing, because 22/32 is a deliberately open
measure in the type scale and Single tightens it to about 1.2×.

### The two-tone headline

Use `runs` instead of `text`. **One text box, several coloured runs** - not one box per
line:

```jsonc
{ "type": "text", "layer": "Headline", "x": 96, "y": 144, "w": 1728, "h": 140,
  "runs": [
    { "text": "Dental practices run on decades-old server-based software", "color": "00004E" },
    { "text": "and drown in administrative work.", "color": "666666" }
  ],
  "font": "Onest SemiBold", "size": 60, "line": "single", "track": -0.02 }
```

**This applies to every layout, not just this one.** Wherever a `Headline` frame in Paper
holds stacked text nodes at `gap: 0`, they collapse into one item with one run each. It is
a required step in converting an artboard, not a per-slide judgement call.

The design system (the `archy:brand` skill) describes this device as a colour split *mid-sentence*, and says the two
stacked text nodes in Paper are a workaround for Paper not being able to colour part of a
text node. OOXML runs are native, so the export expresses the real intent and the team
gets one editable field instead of two.

**That is also the answer to "why does Paper still show two lines?"** - it has to, and it
always will. Paper cannot colour part of a text node, so the merge lives only here.

Keep the explicit break between runs. Without it the colour boundary is anchored to a
character position, so re-written copy can slide it into the middle of a line.

## Charts

**Drawn from `rect` items. Never `addChart`.** The pptx skill says to keep charts native,
which is right for PowerPoint and **wrong for Google Slides: a native pptx chart imports
as a flat image.** That loses the editable data the native route existed for, and loses
what rectangles keep - real shapes a person can still select and recolour. Tested by
building the same slide twice into one file, identical by construction outside the plot.
`build.js` therefore has no chart item type on purpose.

**Every chart shares the baseline `CHART_BASE = 976`**, and each scales its own peak to
whatever leaves room for its labels - 490 for the full-width plots, 400 for the plot in
`Chart + Hero Number`'s narrower column, **440** for `Waterfall`, whose tallest point is
the *middle* step with a label above it (at 490 that label lands at y −20).

**Stacked segments come from cumulative boundaries, not from scaling each segment.**
Rounding each segment independently lets the parts drift off the total.

**`Line / Area` needs two item types nothing else uses:** `line` (a segment; pptxgenjs
draws from `(x,y)` to `(x+w,y+h)`, so an upward slope is `flipV: true`) and `polygon` (the
area wash, via `custGeom` - pptxgenjs has no polygon primitive, and `validate.py` is what
confirms PowerPoint accepts the geometry it writes).

**`Cohort Curves` needs no new item type either.** Its three polylines are emitted as
`line` segments by a `polyline()` helper in `specs.js` - 18 segments across three series.
`build.js` deliberately gains nothing: the segments are what a drawn chart is made of, and
they stay selectable shapes in Slides.

**On a dark ground the series colours invert.** `--color-royal-blue-500` is the forecast
colour on white and it disappears against navy, so the dark charts step
`--color-sky-blue-400` → `-blue-tint-300` → `-blue-tint-200` instead. Same problem as
`--color-blue-tint-200` vanishing on white, mirrored.

**Bar heights are derived from the data, never authored.** `BARS` in `specs.js` holds
`[value, label, year, isForecast]`; `barHeight()` scales each value against the tallest so
the peak always lands on `BAR_MAX` (490px) and the plot stays full whatever the magnitudes
are. Heights are rounded to integers - a fractional bar height is exactly the sub-pixel
defect the design system's Figma paste checklist (the `archy:brand` skill) flags. **Real numbers are a one-line change:** replace
the values and the labels beside them; the geometry follows in proportion.

## pptxgenjs footguns, all hit and verified here

- **`letterSpacing` is silently ignored.** The real option is `charSpacing`, in points.
- **Autofit.** `fit: "none"` emits *no* autofit element, which in OOXML means "inherit" -
  Google Slides is then free to shrink text on overflow, and the type scale is silently
  lost the moment someone types a longer headline. `postprocess.py` injects an explicit
  `<a:noAutofit/>` into every text body. Overflowing is the *correct* failure: it is
  visible and gets fixed; shrinking is invisible and breaks the scale.
- **`margin: 0` on every text box.** The built-in inset otherwise pushes text off the
  Ruler it is supposed to align with.
- **`breakLine: true` produces two `<a:p>` paragraphs**, not an `<a:br/>`. Fine, but check
  `lnSpc` landed on *both* - on only the first, the second line drifts.
- **Hex colours: no `#`, no alpha.** Both corrupt the file. Use `transparency: 0-100`.
- **Gradient fills are not supported at all.** This is why the thirteen dark layouts sit
  on flat `--color-dark-background` rather than the dark gradient ground: a gradient would
  become a background image on every one of them and stop being an editable shape. The one
  gradient the library genuinely needs is `Capture + Scrim`'s `BK Fade`, and that goes in
  as a PNG `build-assets.py` generates - transparent to `#00004E` by 65% of its height,
  which is the design-system rule (the `archy:brand` skill) that a fade reach full opacity before the art ends.

## Checking the output

```bash
"$BASE/.venv/bin/python" <pptx-skill>/scripts/office/validate.py out.pptx   # must print PASSED
"$BASE/.venv/bin/markitdown" out.pptx                                        # every string present?
```

There is no local visual render - and it would
only be a proxy anyway. **Google Slides is the real renderer; check it there.** What to
look at: tracking on the uppercase labels, Ruler weight (2 canvas px = 0.75pt), and where
the body lines break. Then type a longer headline and confirm nothing shrinks.

## Status

All **fifty-five** layouts have specs and build into one deck - 1,527 shapes, schema
validation passing, every string present, 21 images embedded. Slides come out **grouped by
the seven library categories** (`CATEGORY_ORDER` in `build.js`), the same grouping as the
Paper pages - this is a template library, not a deck.

Thirteen of the fifty-five are dark. They are not recolours: the header inversion on a dark
ground is a fixed mapping in the design system (the `archy:brand` skill), so a dark twin of an existing layout would cost
nothing and add nothing. Each dark layout is a distribution that does not exist on light -
see *The dark set* in the design system (the `archy:brand` skill).

Every coordinate was read out of Paper rather than derived by eye, and that mattered
repeatedly - `Big Number`'s third point turned out to have a two-line body where arithmetic
predicted three, which would have put its title 16px off the lane, and `Case Study`'s left
column is a real flex column whose four resolved y values could not have been guessed.

**Verified in Google Slides.** The deck was imported and reviewed there - fonts resolve,
the type scale holds, nothing shrank, and `Market Sizing` reads correctly. The two things
that were flagged as most likely to shift both came through: the tight quote-mark line
boxes (`Quotes` at 80/28, `Quote Statement` and `Hero Testimonial` at 120/40) and
`Number Full-bleed` at 180pt.

Re-check after any change to those, and after adding a layout that sets type in a line box
smaller than its font size - that is the pattern CSS and PowerPoint disagree about.
