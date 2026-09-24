# Review checklist

Run this after filling or adapting a template, and before reporting the work as done. It covers the defects that arrive every time, most of them from Figma pastes, plus the rules that can be checked by eye on a screenshot.

## How to run it

1. **Find the sibling first.** A new piece is usually an existing layout with new copy. The already-corrected sibling is the spec: read its computed styles and compare numbers rather than re-deriving them. Everything that is not campaign copy should come out identical, which also catches defects the eye would pass over.
2. `open_file` with the artboard's `pageId`, so the page is active. On an inactive page `get_screenshot` returns empty and geometry reads come back unresolved (see `paper-quirks.md`).
3. `get_screenshot` on the whole artboard. Then `get_screenshot` at `scale: 2` on every small or dense element: badges, pills, footers, meta lines, numbers.
4. Read every text node back with **`get_node_info`** (`textContent`). Never trust `get_tree_summary` for copy: it truncates at 60 characters with no marker.
5. Use `get_computed_styles` for colours, sizes and leading. Never read a value off a screenshot.
6. Fix, then re-screenshot. Tick an item only after the screenshot that proves it.

---

## Text and copy

- [ ] **No text is clipped or overflowing its box.** Check the booth badge at `scale: 2`. One import rendered `#1211` as **`#121`**: a wrong booth number, shipped. This is the dangerous one.
- [ ] **Every number, date, time, booth number, URL and name is correct**, character for character against the brief or source. A truncated or mistyped value reads as plausible; compare it, do not eyeball it.
- [ ] **Copy was read back with `get_node_info`**, not `get_tree_summary`. Anything that measures exactly 60 characters in the tree summary is truncated until proven otherwise.
- [ ] **All canvas copy is in English**, spelled correctly, including layer names, labels and artboard names.
- [ ] **No token name or hyphenated compound is broken across a line** by `text-wrap: balance` (`--color-` / `neutral-500`). Those nodes use `text-wrap: wrap`.
- [ ] **No orphaned last line in a two-tone headline.** If the first node wraps, check the frame width against the content column before anything else.
- [ ] **A call to action is present** where the format needs one (URL, button, date to register), and it reads at the piece's viewing size.

## Type

- [ ] **`line-height` is never below `font-size`** on wrapping copy (a paste once carried 65px text on 32px leading, and badge text at `line-height: 0`). Exception: display type at 150px+ and single-line labels or values may be set solid or a hair under.
- [ ] **No text below 12px** except in dense product UI, never in marketing art.
- [ ] **Hierarchy is not inverted.** The more important line is never dimmer or smaller than its subtitle.
- [ ] **Product UI is Open Sans.** Any artboard reproducing the Archy app, popup or extension keeps every text node in `OpenSans` / `OpenSans-SemiBold`. Marketing copy around it is Onest + Inter.

## Tokens and values

- [ ] **Every colour is a token** (`var(--color-…)`), never a hex. Recurring intruders: `#D3E8FD` and `#BFDBFE` (Tailwind blues), `#0129A2` on the label pill. None are Archy colours. The one allowed hex is a computed Ruler colour such as `#2A5DF6`, with the tokens it derives from noted.
- [ ] **No sub-pixel values** from freehand resizing (`599.36 × 135.44 @ 78.64, 987.77`, `30.12px`). Integer `left` / `top` / `width` / `height`, `translate: none`, confirmed with `get_node_info`.
- [ ] **Radii are the token values** (12 card/large, 8 button), not scaled up, except the documented poster correction.

## Structure and layers

- [ ] **Layer names match content.** A text reading "DATE & TIME" is not named `Location`. `write_html` names everything `Frame` / `Text`; rename after each write.
- [ ] **Not everything is absolute.** One `Content` frame with real auto-layout holds the stacked blocks; only bleed and overlay layers (background art, photo band, scrim, `BK Fade`, la mascota, the badge) stay absolute.
- [ ] **Layer order reads top to bottom like the design does.**
- [ ] **The artboard is `display: block`**, and `Content` is pinned with explicit `left` / `top`.
- [ ] **The gap between blocks is larger than the gap within a block.**

## Safe area and format

- [ ] **Information stays inside the safe area.** Post 1080 × 1350: x 105–975, y 105–1245. Stories 1080 × 1920: x 105–975, y 250–1670. OG 1200 × 630: ~60–72px margins. A hidden `SAFE` guide often exists but is not respected.
- [ ] **Only decorative stickers break the safe area** (the booth badge may; information may not).

## Grounds, pills and badges

- [ ] **No blue-on-blue label pill or badge.** Pastes ship the kicker pill and the booth badge filled with the background's own accent.
- [ ] **Booth badge colour matches the ground.** Blue ground: `--color-blue-tint-800` with white text. Dark ground: `--color-royal-blue-500` with white text. A navy badge on a dark ground disappears.
- [ ] **Label pill on royal blue** is `--color-white` with `--color-primary-blue-600` text.
- [ ] **The ground gradient was decoded, not guessed.** A pasted `oklab()` gradient was converted to hex and mapped to the nearer of the two grounds, and the three dependent items (badge, `BK Fade` end stop, label pill) follow that ground.
- [ ] **No sticker overlaps type** (a badge covering a letter of the headline is a legibility failure).

## Background art

- [ ] **`BK Fade` is present wherever vector art ends inside the canvas.** The check is mechanical: if `art top + art height < artboard height`, the artboard needs one. Only art clipped by the trim can go without.
- [ ] **The `BK Fade` reaches full opacity before the art ends**, and its end stop matches the artboard's own background token (`--color-royal-blue-500` on blue, `--color-dark-background` on navy).

## La mascota

- [ ] **Her edge reads against the ground.** On a light blue ground close to her own tones she has a white (or very light) outline. The outline is never blue or tinted. On other grounds she usually needs none.
- [ ] **Off a side edge she is rotated 90°.** Upright with a side crop is wrong. Off the top she stays upright.
- [ ] **The crop never runs through an ear.** It falls on the shell. The only sanctioned exception is a thumbnail-scale piece where she peeks in from the bottom rotated 180°.

## Wordmark and logos

- [ ] **The Archy wordmark on a white or light ground is `--color-royal-blue-500`**, never navy or black. On dark grounds, and inside a royal-blue component, it is white.
- [ ] **The wordmark shows the counter of the "A"** (not "∩rchy", which means it came from `index.html`).
- [ ] **Partner logos are matched optically**, sharing a cap height, and the lockup spans the full content width.
- [ ] **Logo boxes use `background-size: contain`** at the asset's own aspect; nothing is stretched.

## Rulers

- [ ] **Every Ruler is a solid colour.** No `opacity`, no alpha colour, on any ground. Check the intersections on the screenshot: a darker knot where two lines cross means a translucent Ruler.
- [ ] **Ruler colour matches the ground:** `--color-light-border` on white, `--color-blue-tint-200` on a blue-tinted light gradient, `#2A5DF6` on royal blue, `--color-dark-border` on dark navy.
- [ ] **Rulers are 2px at poster scale.**
- [ ] **No sticker sits across a Ruler mid-span.** A sticker may terminate a Ruler at the trim. La mascota may cross one.
- [ ] **Rulers separate, they do not bracket:** none above the first row or below the last.
- [ ] **Content does not touch a column vertical.** It is inset to the cell lane, or the verticals were removed on purpose.
- [ ] **One Ruler per boundary.**

## Banned effects

- [ ] **None of the banned generic-AI devices:** an outlined pill with a word inside it and no state to carry, an element floating with no relationship to anything around it, a decorative accent colour applied because it was available.
- [ ] **No blobs, meshes, glows, drop shadows, decorative rotations or blend modes.**
- [ ] **No mint in event pieces.**

## Before reporting

- [ ] A final full-artboard `get_screenshot` taken after the last fix.
- [ ] `finish_working_on_nodes` called.
