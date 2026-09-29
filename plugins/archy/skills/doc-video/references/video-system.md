# DOC video system

Read this when filling or adapting a DOC video graphic. Every number here was measured on frames of the Foundations videos and checked against exports of the master. It describes the videos as they are; the numbers are the reference, and a new piece that needs a different value says so in the report.

## Frame

- **1920×1080**, ground `--color-cream-500`. Margin 88 from the frame edge; `--spacing-video-safe` (96) is the title-safe line.
- **Split:** footage 0 to 960, a cream-500 `Panel` 960 to 1920. Panel content starts at about x 1060 (lists at 1104), or is centred in the panel when it is a column of tiles.
- **Overlay twin:** the same artboard with the footage placeholder deleted and the artboard background transparent; the Panel stays. Any edit to a template goes to its twin too. Check with an export: the PNG must be RGBA, alpha 0 on the left half.
- The footage placeholder in split templates is an image rectangle standing in for the speaker. It is never exported as part of the graphic.

## Colour

| Use | Token |
|---|---|
| Ground and split panel | `--color-cream-500` |
| Boxes, tags, icon tiles | `--color-cream-100` |
| Figure boxes, bullets, dots, intro ground, icon fills | `--color-red-400` (the videos measure 255, 5, 0; not red-500) |
| Hero illustrations (map pin, gift ribbon, scoreboard) | `--color-red-500` (measured 236, 5, 6) |
| Titles and items | `--color-neutral-900` |
| Box labels | `--color-neutral-700` |
| Hero outlines | `--color-ink`; strokes of the monitor and the dashed route are `--color-neutral-900` |
| Hero light fills (pin centre, scoreboard face) | `--color-cream-300` |
| Rule under list titles, acronym divider | `--color-cream-rule` (3px) |
| Muted chart labels ("Mo.") | `--color-ink-muted` |
| Donut second share | `--color-red-300` |
| Venn intersection | `--color-red-lens` |
| Segmented bar dark segment | `--color-red-wipe` |
| Monitor toggle knob | `--color-red-toggle` |

The last six are video-only tokens that exist in this file. If a new piece needs another colour, flag it and ask for a token.

## Type

Satoshi throughout; Regular 400 is the lightest weight used (no Light, so `doc-brand` holds unchanged).

| Element | Setting |
|---|---|
| List title (split) | Black 75 / 88, neutral-900; 3px rule under it, at least 542 wide |
| List title (full) | Black 70, block centred with `left: 50%` + `translate: -50% 0` |
| List items | Medium 60, 80 pitch; 16px red-400 bullet, 28 gap; text at x 1104 |
| Quote, two lines | Regular 84 + Bold 84, 98 pitch, centred |
| Quote, one line | 99px |
| Acronym | red-400 block 94×406, cream letters Bold 126; words Regular 84, 130 pitch |
| Title card | Eyebrow Medium 22, no tracking; title Bold 76 / 88; lockup 198×72; tag cream-100 |
| Red figure boxes | Black 54 to 56, cream-100 |
| Label boxes | Bold 44, or Medium 45 to 52, neutral-700 |
| Chart titles | Black 68 to 88 |
| Captions under tiles | Medium 30, neutral-900, centred; about 27px from the tile to the cap top (lh 40), tighter under the 234 tiles of F2c |
| Hero caption (scoreboard) | Regular 40 / 46, centred |

Centring a multi-line text node in Paper: `text-align` is ignored on a fixed-width `pre` text, so use `left: 50%` + `translate: -50% 0` with `width: fit-content`.

## Boxes and connectors

- Chains read left to right or top to bottom: a connector is a 2px ink line ending in a red-400 dot tucked under the next box.
- Only figure boxes are red; everything else is a cream-100 box. Tag boxes (E2, E3) have square corners.

## Icon tiles

- Tiles are cream-100 with `--radius-tile` (10px). Sizes seen: 248 (rows and columns), 234 (F2c), 250 (F2b), 294 (F1), 360 (F3b), 198 (D5).
- The icon sits centred with about 20px of air: a 208 SVG in a 248 tile, 196 in 234, about 300 in 360. Match the drawing's visible size to the video, not the SVG box; some icons need a step larger.
- Rows keep a fixed gap (28 in F1b, 102 in F1); columns 40 (F2a). Use fixed-width slots so captions of different lengths do not shift the tiles.

## The icon library

`F · Assets` holds 26 icons as `Icon · <name>` frames (180px) with a 100×100 viewBox, plus the lockups (Ink, Cream, Symbol Red). Strokes are **3.5px with `vector-effect: non-scaling-stroke`**, because in the videos the stroke stays about 3.5px at any icon size; fills are red-400 with cream-100 inside shapes.

To use an icon, `x-paper-clone` its frame into the tile, then resize both the clone and its inner SVG (the clone keeps the SVG at 180 otherwise). A new icon is drawn in the same style and added to `F · Assets`, never to a working copy only.

## Hero illustrations (F4)

The four heroes are **drawn at full size** as one 1920×1080 SVG traced from the frame, not scaled icons: their strokes are 6 to 8px, thicker than the icon library. Text inside them stays editable as text nodes (ON, HOME, SET, the scores, the caption). The scoreboard clock is SVG seven-segment polygons, so changing the time means redrawing segments.

The videos set the scoreboard labels and scores in a squarer display face; the master uses Satoshi Black with an ink outline. Paper ignores `-webkit-text-stroke`, so the outline is eight `text-shadow`s (3px for labels, 4px for scores) in `--color-neutral-900`.

## Paper notes for video work

- `create_artboard` ignores the position: set `display: block`, `left`, `top` and `overflow: clip` right after.
- Empty divs are dropped on write: write a placeholder text and delete it.
- Write at most five icon clones per `write_html`; a nine-icon write froze the renderer once (fixed by restarting Paper).
- Exports right after a write can be stale: export again.
- Paper PNG exports carry a Display P3 profile, so mid reds read shifted when sampled (red-500 reads about 217, 48, 34). Compare shapes and positions against the video frame, not raw colour values.

## Video review checks

On top of `doc-brand` › `review-checklist.md`:

- The template is in the layout the videos show; no derived full or split version.
- Type sizes are the template's; a longer line was re-broken before it was resized.
- Chart geometry matches the figures.
- Every split template has an updated `· Overlay` twin, and its PNG is transparent on the left half.
- Icons come from `F · Assets` and keep 3.5px non-scaling strokes.
- No hex anywhere: `find_nodes` with `styleValue: "#*"` on the page returns nothing.
