# DOC video system

Read this when filling or adapting a DOC video graphic. The values come from the editor's source files for the F3 Foundations videos (exact) and from frames of the first nine Foundations videos (measured). Where both existed, the source-file value won. A new piece that needs a different value says so in the report.

## Frame

- **1920×1080**, ground `--color-video-ground`. Margin 88 from the frame edge; `--spacing-video-safe` (96) is the title-safe line.
- **Split:** footage in the left half, a video-ground `Panel` 960 to 1920. Panel content starts at about x 1060, or is centred in the panel.
- **Over footage:** the footage fills the frame and the graphic (lower third, caption, term) sits in a video-ground box at the bottom left, about 135px from the left edge.
- **Overlay twin:** the same artboard with the footage placeholder deleted and a transparent artboard; the Panel stays on split templates. Any edit to a template goes to its twin too. Check with an export: the PNG must be RGBA, alpha 0 where the footage was.
- `Footage (placeholder)` stands in for the speaker and is the same image in every template. It is never exported as part of the graphic.

## Colour

| Use | Token |
|---|---|
| Ground, split panel, lower-third boxes | `--color-video-ground` |
| Intro ground | `--color-cream-500` |
| Label boxes, bullet boxes | `--color-cream-100` |
| Icon tiles | `--color-cream-200` |
| Figure and result boxes, title-card panel, role tag, icon fills, donut main share, hero reds | `--color-red-500` |
| Bullets, connector dots, acronym block, title-card artboard | `--color-red-400` |
| Titles and body text | `--color-video-ink` |
| Box labels, operators (− = +), captions under icons | `--color-video-ink-soft` |
| Title-card text and speaker tag | `--color-video-tag` |
| Text on red boxes | `--color-white` |
| Rule under list titles, acronym divider | `--color-cream-rule` (3px) |
| Icon and hero outlines | `--color-neutral-900`, `--color-ink` on the map and send heroes |
| Muted chart labels ("Mo.") | `--color-ink-muted` |
| Donut second share | `--color-red-300` |
| Venn intersection | `--color-red-lens` |
| Segmented bar dark segment | `--color-red-wipe` |
| Monitor toggle knob | `--color-red-toggle` |

The `video-*` tokens and the last five are video-only tokens that exist in this file. If a new piece needs another colour, flag it and ask for a token.

## Type

Satoshi throughout; Regular 400 is the lightest weight used, so `doc-brand` holds unchanged. Many source texts carry `opacity: 0.9`; keep it where the template has it.

| Element | Setting |
|---|---|
| Split list title | Black 70 / 84 |
| Split list items | Medium 60 / 72 (`--text-video-quote`) |
| Full list title | Black 103, two lines |
| Full numbered items | Medium 76 / 92, rules between rows |
| Lower-third caption | Bold 60 (`--text-video-quote`), box padding 50 |
| Term + definition | Term Bold 60, definition Italic 40 (`--text-video-subhead`) in quotes |
| Speaker lower third | Name Black 65; role Medium 40 in a red tag |
| Closing quote | Regular, two lines, centred |
| Stat hero | Black figure, Bold label, Regular line |
| Red result boxes | Black 56 white; label boxes Bold 45 to 51 video-ink-soft |
| Acronym | Letters Bold 125 white on red-400; words Regular 84 |
| Captions under tiles | Medium 30 |

Centring a multi-line text node in Paper: `text-align` is ignored on a fixed-width `pre` text, so use `left: 50%` + `translate: -50% 0` with `width: fit-content`.

## Boxes and connectors

- Chains read left to right or top to bottom: a connector is a thin video-ink line ending in a red-400 dot tucked under the next box.
- Only figure and result boxes are red; everything else is a cream-100 box. Tag boxes (D2, D3) have square corners.
- **Speaker lower third (S3):** the role tag hangs off the right end of the name box, not centred under it: it overlaps the last ~170px of the box and runs past its right edge. The box width follows the name, so place the tag after setting the name (absolute `left`, `translate: none`) and make the same change in the Overlay.
- **Numbered squares (T2):** size each number's frame to its square (52×52, same `left` / `top`) and give the digit a `line-height` equal to the square's height (52px), so it sits centred. A digit box shorter than its line-height pushes the digit low.

## Icon tiles

- Tiles are `--color-cream-200` with `--radius-tile` (8px). Sizes seen: 363 (I1), 248 (rows and columns), 234 (I4), 250 (I3), 360 (I6), 198 (C7).
- The icon sits centred with about 20px of air. Match the drawing's visible size to the source, not the SVG box.
- Split templates I7 to I9 show one large icon with no tile.

## The icon library

`A · Assets` holds 46 icons as `Icon · <name>` frames (180px) with a 100×100 viewBox, plus the lockups (Ink, Cream, Symbol Red). Strokes are **3.5px with `vector-effect: non-scaling-stroke`** in `--color-neutral-900`; fills are `--color-red-500` with `--color-cream-100` inside shapes.

To use an icon, `x-paper-clone` its frame, then resize both the clone and its inner SVG (the clone keeps the SVG at 180 otherwise). A new icon is drawn in the same style and added to `A · Assets`, never to a working page only. Never paste a raster icon from an editor's file: redraw it.

## Hero illustrations (H1 to H4)

The four heroes are **drawn at full size** as one 1920×1080 SVG traced from the frame, not scaled icons: their strokes are 6 to 8px, thicker than the icon library. Text inside them stays editable as text nodes. The scoreboard clock is SVG seven-segment polygons, so changing the time means redrawing segments. Scoreboard labels and scores use Satoshi Black with an ink outline made of eight `text-shadow`s (Paper ignores `-webkit-text-stroke`).

## Working from an editor's source file

When an editor hands over their scenes (a Figma paste), they are vectors and carry exact values. Duplicate the scene to the page root with `duplicate_nodes` (`parentId` = the page root), then:
- delete hidden `GUIDE` layers;
- map every hex to a token (`find_nodes` with `styleValue: "#*"` for styles, `*gradient*` for panels painted with a gradient over an image, and `get_jsx` for SVG `fill` / `stroke`, which `find_nodes` does not see; `update_styles` sets SVG `fill` and `stroke`);
- replace raster icons and logos with clones from `A · Assets`;
- replace real names with placeholders and rename layers to what they are.

## Paper notes for video work

- `create_artboard` ignores the position: set `display: block`, `left`, `top` and `overflow: clip` right after. A transparent `backgroundColor` on `create_artboard` becomes white; set the token after.
- Empty divs are dropped on write: write a placeholder text and delete it.
- Write at most five icon clones per `write_html`; a nine-icon write froze the renderer once.
- Run exports one call at a time and at most five artboards per call: parallel or larger exports time out (the files may still land in `~/Downloads` with a `(1)` suffix).
- Paper PNG exports carry a Display P3 profile, so mid reds read shifted when sampled (red-500 reads about 217, 48, 34). Compare shapes and positions, not raw colour values.

## Video review checks

On top of `doc-brand` › `review-checklist.md`:

- The template is in the layout the videos show; no derived full or split version.
- Type sizes are the template's; a longer line was re-broken before it was resized.
- Chart geometry matches the figures.
- Every split and over-footage template has an updated `· Overlay` twin, and its PNG is transparent where the footage was.
- Icons come from `A · Assets`, no raster icons.
- No real person's name unless the requester supplied it.
- No hex anywhere: `find_nodes` with `styleValue: "#*"` on the page returns nothing.
