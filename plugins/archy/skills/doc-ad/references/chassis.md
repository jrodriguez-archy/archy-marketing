# The DOC ad chassis

Read this before filling or adapting any DOC ad. Colour, type and lockup rules are in the `doc-brand` references; this file covers structure, sizing and the formats.

**The structure, the tokens and the scale are the system; the gaps, the leading and the tracking token are decisions taken per artboard.** Start from the sibling in the master, derive each number from the piece in front of you, and expect a designer to retune it.

---

## Structure

```
Artboard        display: block · overflow: clip · ground = theme token
├── [bleeds]    absolute: footer band, photo, scrim, a slot that bleeds off the trim, a corner block
└── Content     absolute, inset on all four sides · flex column
    ├── Lockup  flex-shrink: 0
    ├── Body    flex: 1 · flex column · justify-content: center · gap
    └── CTA     flex-shrink: 0
```

- **`inset` on all four sides** gives a `Content` box that re-derives when the artboard height changes. With `space-between` on it, one design serves 1:1, 4:5 and 9:16 by changing the artboard height and the type.
- Containers that grow with content: `height: fit-content`, never a fixed height with large padding.
- A child that keeps its size: `flex-shrink: 0` plus an explicit size. Only the block meant to absorb slack gets `flex: 1`, one per axis.
- Full width: `align-self: stretch`, not a typed width. Spacing between blocks: `gap` with a `--spacing-*` token, never a computed `top`.
- A row that must survive long copy: `min-height` + `height: fit-content`, `flex: 1` on the label, `flex-shrink: 0` on the value, `align-items: flex-start` with `padding-block` (an ordinal centred with `align-items: center` drops between lines when the item wraps).
- A data block (table, list) keeps one density across formats: rows `fit-content` with a `min-height`; the surrounding `Body` absorbs the extra height.
- When the void belongs in the middle, `Content` is `space-between` over exactly two groups. Three or more `space-between` children divide the slack evenly and land on sub-pixel positions.
- An art slot that is the subject takes `align-self: stretch` + `flex-grow: 1`, so the art absorbs the format change.
- A slot pinned by hand as a bleed layer must be re-read (`get_node_info` on its spacer) and moved whenever the content above it changes height.
- Headline nodes keep `white-space: pre` with explicit `\n`: the block reflows, the lines do not re-break by themselves.

Paper traps that apply here (full list in `archy:brand` › `paper-quirks.md`): `create_artboard` makes a flex artboard (set `display: block`); `move_nodes` into a flex parent adds `flex: 1` to the moved children, and `flex` cannot be removed with `update_styles` (cap it with `max-width`, or rebuild the subtree); `write_html` names every node `Frame` / `Text` (rename after each write).

---

## Margins and the format ladder

| | 1080×1080 | 1080×1350 | 1080×1920 (Story) |
|---|---|---|---|
| `Content` inset | 72 | 72 | top **206**, bottom **180**, sides 72 |
| Lockup (`11k × 4k`) | 220 × 80 (k 20) | 275 × 100 (k 25) | 330 × 120 (k 30) |
| Compositional gaps (between blocks) | base step | one `--spacing-*` step up | one or two steps up |
| CTA button | 336 × 79 | 336 × 79 | 336 × 79 |
| CTA text link | 32 | 36 | 40 |

- **The lockup grows with the format, always**, one `11k × 4k` step per format, without being asked. (`Track Colorway` runs a larger band lockup, 275 × 100 on 1:1 and 4:5; some layouts with a lockup that must balance a heavy element run a step larger.)
- **The CTA button never scales**: it is a tap target. The words inside a CTA bar do grow a notch per format (eyebrow 20 / 20 / 22, line 34 / 35 / 36).
- The Story's top and bottom margins keep information clear of Instagram's interface. A full-bleed footer band on a Story grows upward (it becomes the lower third) rather than sitting under the interface.
- **A Story is not a stretched Feed.** Take the extra height one of two ways: re-set the type larger and re-break the copy (4 lines where the 4:5 had 3), or give it to the element that is the picture (art slot, portraits, chart bars). On a tall Story keep the message together as one centred group or split it deliberately to the edges, judged per layout; a headline pinned to the top and a footer pinned to the bottom with nothing between reads as two posters.
- **A hero already capped by the column cannot grow with the format**; the extra height becomes air. That is correct, not a defect.
- Build a missing format from the nearest sibling that already carries the right line breaks (a Story from the 4:5, not the 1:1).

---

## Sizing type

- **Fill the measure.** After every copy change, resize the hero type until its longest line reaches about 890 to 920 of the 936 column (measure at the node's own tracking; body copy has none). A themed variant may carry a different size from its siblings because its copy is different. Only copy that already fills the column keeps its size.
- **Measure widths in one call**: a `flex-direction: row; gap: 0` frame of `width: max-content` candidates, then `get_children` (each `x` is the running sum). Delete the frame afterwards.
- **The lead under a headline is a second voice**: start around 0.45 × the headline (about 48 to 50 on a 120 headline), leading about 1.2 to 1.3. Supporting lines under a stat run around 0.22 × the stat.
- **One headline break for all three formats** of a campaign, so they read as one; body copy may break differently per format, always at a sense unit.
- Rough starting sizes (then fill the measure): two-weight headline 96 / 120 / 124 (1:1 / 4:5 / 9:16); single-word or numeral heroes 200 to 420; body 45 / 50 / 52.
- The two-weight headline's gap, leading and tracking follow `doc-brand` › `identity.md`.

---

## The CTA

Three forms, all on tokens:

| Form | Where | Spec |
|---|---|---|
| **Button** | Bar, Keep Scrolling, Object Photo | 336 × 79, `--radius-button`, label 30 / 36 Bold `--tracking-heading`, arrow 28 × 18, gap 14. Colours per ground in `doc-brand` › `identity.md` |
| **CTA bar** | Bar | Full content width, `--radius-card`, padding 40: eyebrow + line on the left, the button on the right, vertically centred |
| **Text link** | Most other layouts | Label + arrow in one row, Bold, the accent colour of the theme (cream on Dark, never red text on Dark). Track Colorway puts the arrow inside the string (`Enroll now →`) |

The CTA copy comes from the theme (`voice.md`).

---

## Ad review checks

Run these on top of `doc-brand` › `review-checklist.md`:

- [ ] `Content` insets match the format (72 / 72 / 206-180).
- [ ] The lockup is the right `11k × 4k` step for the format; wrapper and `SVG` both resized.
- [ ] The button is 336 × 79 in every format.
- [ ] The hero fills the measure, or is capped by the column on purpose.
- [ ] The headline breaks the same way in all three formats.
- [ ] On the Story, nothing that must be read sits in the top 206 or the bottom 180.
- [ ] Hand-pinned bleed slots were re-read after any change above them.
- [ ] No sub-pixel positions from `space-between` over three or more children.
