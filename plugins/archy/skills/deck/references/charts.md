# Charts

Read this when building or reviewing any chart slide: bars, lines, waterfalls, stacked or nested blocks, chart pairs.

Chart layouts live on the **Charts** page of **Master - Decks** (`app.paper.design/file/01M1HZF1EW0RX9H3YSMJ3GAMK7`); the roster is in `layout-catalog.md`. Dark-ground series colours are in `dark-set.md`. Header and Rulers are in `slide-system.md`. The exporter is the `slides-export` skill.

---

## Drawn from Frames, never a native chart object

**Charts are drawn from Frames. Never a native chart object: tested and rejected.**

The pptx skill says *"Keep charts native… do not fall back to a rendered image"*, and that is right for PowerPoint. **It inverts for Google Slides, which is where this deck lives:** a native pptx chart imports into Slides as a **flat image**. So the native route loses the one thing that justified it (editable data) *and* loses what drawn shapes keep, because rectangles arrive as real shapes a person can still select, recolour and resize.

Verified by building the same slide twice into one file (drawn vs `addChart`, identical by construction outside the plot) and importing it. Do not re-litigate this without re-running that test; the generic advice will keep pointing the wrong way.

The consequence for the exporter: it has **no chart item type**, on purpose. Bars are `rect` items and their geometry is computed from the data.

---

## `Bars`: the reference

Built entirely from Frames: no image, no library.

| Part | Construction |
|---|---|
| **Chart frame** | `left 96, top 346, 1056 × 710`, flex column, `gap 32`, `padding 48px 40px` → content 976 × 614 |
| **Legend first** | 22px tall: two keys, each a 14 × 14 swatch + an 18/22 uppercase label. Not optional: the actual/plan split is meaningless without it |
| **Plot** | Flex row, `align-items: flex-end`, height 560. Bars are columns of `[value label] [Column] [year label]` with `justify-content: flex-end` and `gap 8`, so every bar shares a baseline no matter its height |
| **Bar geometry** | Five bars in 976: width **128**, gap **84** (5 × 128 + 4 × 84 = 976). Max bar height = 560 − 30 − 24 − 16 = **490** |
| **Actual vs plan** | The colour moment: past bars `--color-blue-tint-200` with `--color-neutral` labels, forecast bars `--color-royal-blue-500` with royal-blue labels. Year labels carry the A/E suffix as well, so the chart survives being read in greyscale |
| **Axis** | A Ruler, absolutely positioned in the Rulers layer at the bar baseline (y **976** for the geometry above), spanning the full column 96 → 1152 so it meets the column's verticals |
| **Bars are square** | No radius: the token set caps at 12 and the site's language is hairlines, not rounded chrome |

A value and its delta go in a flex row with **`align-items: baseline`** and a real gap, never `space-between`: pushed to opposite ends of a 592px row the delta reads as unrelated to the number it qualifies.

**Every chart shares one baseline: y 976.** That is what makes two chart slides read as the same system when you page between them. The axis Ruler sits there, the year labels start at 984, and the plot's tallest mark reaches 490 above it.

---

## Plot widths

**Two plot widths, and the choice is structural, not cosmetic:**

| | Plot | Right column | For |
|---|---|---|---|
| **Column plot** | 96 → 1152 (976 content) | 1152 → 1824, three figures | Few periods that each need a caption: `Bars` |
| **Full-width plot** | 96 → 1824 (1648 content) | none | Many periods that need horizontal room: `Line / Area` |

**Each mark centres in its own equal column**, exactly as the bars do. `Line / Area` divides its 1648 into 8 columns of 206 and puts each point at a column centre (239 + 206n), so the period labels centre under their points with no fractional arithmetic. Spreading points edge-to-edge instead gives a pitch of 1648/7 = 235.43 and sub-pixel positions.

---

## Line charts

**A line chart's legend swatch is a line segment, not a square**: 20 × 4, the same weight as the stroke. A square swatch beside a line chart describes the wrong mark.

**Actual is `--color-blue-tint-300`, forecast is `--color-royal-blue-500`, on a line.** The rule "forecast is royal" carries over from `Bars`, but the *quiet* half cannot: a 4px stroke in `--color-blue-tint-200` nearly vanishes on white, where a bar of that colour reads fine. The area wash under the whole series is `--color-blue-tint-50`, light enough not to compete with the stroke.

---

## Peak height

**490 is the maximum, not the constant. Each chart scales its peak to whatever leaves room for its own labels:**

| | Peak | Why |
|---|---|---|
| `Bars`, `Line / Area`, `Stacked Bars` | 490 | One label above the tallest mark |
| `Chart + Hero Number` | 400 | The plot sits in the 864-wide right column; labels need more air at that scale |
| `Waterfall` | **440** | The peak is the *middle* step, and its label sits above it inside the plot. At 490 that label lands at y −20, off the artboard |

---

## Waterfall

**A decrease labels below its bar, not above.** In `Waterfall` the churn step sits at the top of the bridge, so its label would collide with the step before it. Below the bar it is also semantically right: the value hangs down, the way the quantity does.

**Waterfall steps need connectors or it is not a bridge.** A 2px `--color-light-border` at each cumulative level, from one step's right edge to the next step's left edge. Without them the five bars read as an ordinary column chart with odd heights.

**`--color-red` appears in exactly one place in the whole deck: the churn step.** It is semantic (a waterfall's subject is direction), not the "decorative accent applied because it was available" that the ban targets. Do not spread it.

---

## Chart pairs

**A chart pair replaces the legend with a sub-title over each plot**, and the two share the one axis Ruler spanning the full content column. That shared baseline is what makes them read as a pair rather than as two charts that happen to sit together.

---

## Nested blocks (`Market Sizing`)

**A nested-blocks diagram encodes AREA, so derive it by scaling both dimensions by `√ratio`, never by eye.** `Market Sizing`'s first version was hand-drawn and put SOM at 11% of TAM's area when the data says 4.3%: 2.5× too big, a chart misrepresenting its own numbers. This is the same rule as data-derived bar heights, and it is easier to break because a rectangle has two dimensions and halving both quarters the area. For TAM 784 × 560 the tiers land on:

| Tier | Size | Share of TAM area |
|---|---|---|
| TAM | 784 × 560 | 100% |
| SAM | 484 × 346 | 38.1% |
| SOM | 162 × 116 | 4.3% |

All three share a bottom edge and a left edge so each block visibly *contains* the next.

**Containment is the only reason to draw a nest instead of three bars.** People compare lengths accurately and areas badly, so a nest has to earn itself: reach for it when the claim is `SOM ⊂ SAM ⊂ TAM`, and for `Horizontal Bars` when the claim is just relative size.

---

## Labelling marks

**Name the mark in place; reach for a swatch only when you cannot.** `Market Sizing` shipped with three unlabelled blocks and three rows of text, and nothing tied one to the other but the reader's guess at the colour order: no key at all. The first fix was a swatch per legend row, and that was the weaker answer: **a swatch is what you use when a mark is too small or too numerous to carry its own name** (a bar in a five-bar series, a line in a three-line chart). Three blocks that each have room for a word should just say the word, at their own top-left with a 24px inset: nothing to decode.

**And once the mark is named, the swatch has no job left.** Both together is two keys for one mapping, which is the same noise as two Rulers on one boundary. `Bars` and `Line / Area` keep their swatches because their marks genuinely cannot be labelled individually.

**State the ratio in words too, not just in geometry.** If the point of a chart is a proportion, the proportion belongs in the copy: `Market Sizing`'s notes now open with "38% of TAM" and "4% of TAM". The area shows it; the sentence makes it quotable.
