# DOC review checklist

Run this after filling or adapting a DOC piece, and before reporting it as done.

## How to run it

1. **Compare with the sibling.** A new piece is usually an existing layout with new copy; the same layout in the same format is the spec. Everything that is not copy should match it.
2. `open_file` with the artboard's `pageId` so the page is active; on an inactive page screenshots come back empty and geometry is unresolved.
3. `get_screenshot` on every artboard, and at `scale: 2` on small or dense parts (CTA, footer, labels, lockup).
4. Read every text node back with `get_node_info`; `get_tree_summary` truncates at 60 characters.
5. Use `get_computed_styles` for colours, sizes and leading; never read a value off a screenshot.
6. Fix, then re-screenshot.

## Copy

- [ ] Every fact, number, date and name is correct against the brief. Specimens are marked and listed as pending.
- [ ] The CTA matches the theme (`voice.md`), with no full stop.
- [ ] All canvas copy, layer names and artboard names are US English.
- [ ] No text is clipped or overflowing its box.
- [ ] No orphan and no one-word line; breaks fall on sense units.
- [ ] No hyphenated word broken by `text-wrap: balance` / `pretty`.

## Type

- [ ] Satoshi only; nothing lighter than Regular 400.
- [ ] Two-weight headline: two nodes, the Bold half starts a line, both halves the same colour (ads), the gap suits the grammar (`identity.md`).
- [ ] The hero type fills the measure (longest line close to the column width) unless the layout caps it.
- [ ] The lead under a headline is a second voice, not a caption (roughly 0.4 to 0.5 × the headline).
- [ ] Wrapping body copy has line-height at or above its size.

## Tokens

- [ ] Every colour, weight, tracking, spacing and radius is a token. `find_nodes` with `{styleValue: "#*"}` on the artboard returns nothing, and nothing uses `color-mix()`.
- [ ] No sub-pixel sizes or positions from a hand drag; `translate: none` on moved nodes.

## Colour and theme

- [ ] The ground is one of the five themes and every accent follows it (`identity.md`, *Grounds and themes*).
- [ ] Dark: no red text or red hairline icons; containers are `--color-ink-soft`; red only as a fill.
- [ ] Light: red appears as the container (CTA bar, card, band), lockup is ink with the red square.
- [ ] Track colours are never mixed in one piece.

## Lockup

- [ ] It is the outlined artwork from the file, not re-typed.
- [ ] Its colourway suits the ground (`identity.md`, *Colourways*).
- [ ] Its size is an `11k × 4k` step, both wrapper and `SVG` resized (`get_node_info`).
- [ ] Clear space of one cap height holds on all sides.

## Structure

- [ ] The artboard is `display: block`; one `Content` frame with auto-layout holds the stacked blocks; only bleeds (bands, photos, scrims, slots that bleed) are absolute.
- [ ] Layer names match their content.
- [ ] A gap inside a block is smaller than the gap between blocks.

## Before reporting

- [ ] A final full-artboard screenshot after the last fix.
- [ ] `finish_working_on_nodes` called.
