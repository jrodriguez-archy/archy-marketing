# Layout Catalog

Read this when choosing a layout for content in hand, adding a layout to the library, deriving a new slide from an existing one, or placing an image or logo slot.

The library is the Paper file **Master - Decks** (`app.paper.design/file/01M1HZF1EW0RX9H3YSMJ3GAMK7`): 55 layouts at 1920 × 1080, all with export specs. Shared geometry (header, Rulers, type scale) is in `slide-system.md`; the dark layouts' rules in `dark-set.md`; chart construction in `charts.md`. Export to Google Slides is the `archy-design:slides-export` skill.

---

## Organisation

**Organised by what content you have in hand, one Paper page per category.** The question a person actually arrives with is "I have three stats and a claim, what fits?", and the category answers it. Within a page, artboards sit on the usual 2000 × 1200 grid, four per row.

**Layout names carry no numbers.** In a library that grows, a number goes stale the moment something is inserted: adding one metrics layout would renumber everything after it, in the artboard names, the export specs, their README and this roster. Order comes from the page and from the exporter's `CATEGORY_ORDER`, never from the name.

Numbers and Charts are separate categories because "I have a figure" and "I have to plot a relationship" are different decisions.

## Roster

Dark layouts are marked **◆**. See `dark-set.md` for what earns one.

| Page | Layouts |
|---|---|
| **Frames** (8) | `Cover` · `Statement` · **◆**`Manifesto` · `Agenda` · `Section Divider` · `Quote Statement` · **◆**`The Ask` · `Closing` |
| **Numbers** (6) | **◆**`Big Number` · **◆**`Number Full-bleed` · **◆**`Two Numbers` · `Metrics 2×2` · `Metrics 3-up` · `Split stats` |
| **Charts** (9) | `Bars` · `Line / Area` · **◆**`Cohort Curves` · `Horizontal Bars` · `Stacked Bars` · `Waterfall` · `Chart + Hero Number` · `Two Charts` · **◆**`Market Sizing` |
| **Lists** (10) | `Columns 2-up` · `Columns 3-up` · `Columns 4-up` · `Numbered rows` · `Icon List` · `Product grid` · **◆**`Platform Stack` · **◆**`Key-value rows` · `Timeline` · `Roadmap` |
| **Comparisons** (7) | `Comparison Table` · **◆**`Matrix` · **◆**`The Wedge` · `Before / After` · `Competitive Table` · **◆**`Cost Stack` · `Positioning 2×2` |
| **Proof** (8) | `Quotes` · `Hero Testimonial` · **◆**`Proof Stack` · `Case Study` · `Logo Wall` · `Team grid` · `Team 3-up` · `Press & Investors` |
| **Showcase** (7) | `Capture Bleed Bottom` · `Split Copy / Image` · `Bento Grid` · `Capture Centred` · **◆**`Capture + Scrim` · **◆**`Screen Trio` · `Capture Full-bleed` |

## A layout has to hold a content shape the others cannot

Two planned layouts were dropped on that test:

- A fourth Comparison (two prose columns, "Them / Us") is `Before / After` with longer paragraphs.
- A **KPI Row** in Numbers (three to five compact stats as a band) is the top row of `Split stats`, which already pairs it with two wide rows. Numbers stops at four because four distinct shapes is what the category has: one hero figure, a 2 × 2 grid, a 3 × 2 grid, and a band plus rows. A fifth grid of stats would have produced the "assembled from a component library" sameness rather than new capability.

The same test that removes an element from a composition removes a layout from the library. **Numbers being the smallest category is the correct outcome, not a gap to fill.**

## Per-layout reference

"Source slide" is the page in the original investor deck the layout was rebuilt from; "none" means the layout has no source slide.

| | Ground | Body structure | Source slide |
|---|---|---|---|
| `Cover` | Royal Blue 500 | Title 128/128, date, presenter row, wordmark bottom-right | 1 |
| `Statement` | Royal Blue 500 | Centred two-tone statement 128/128, short vertical Ruler, lead + body. **No header band** | 2 |
| `Metrics 2×2` | Light | 2 × 2 cells, stat 80/84 + label 30/38 + body 22/32 | 4 |
| `Columns 4-up` | Light | 4 columns, ordinal 96/96 + two-line title + body | 5 |
| `Comparison Table` | Light | Label row 50px + 5 rows × 132px, columns Stage / Today / With Archy AI | 7 |
| `Quotes` | Light | 2 quote cells + a stats column split in two | 8 |
| `Team grid` | Light | 4 × 4 cells (177px), circular portrait + name + role | 14 |
| `Big Number` | Dark Background | Hero number 320/300 left, 3 Ruler-separated points right | 18 |
| `Product grid` | Light | 3 × 2 cells, icon + Status pill + body, **footer band** | 6 |
| `Metrics 3-up` | Light | 3 × 2 stats (305px rows), **footer band** | 9 |
| `Numbered rows` | Light | 3 rows × 237px: ordinal 96/96 · title + subtitle · two paragraphs | 10 |
| `Split stats` | Light | Row of 3 stats (258px) + 2 wide rows (224px) pairing a 40/48 value with a claim | 11 |
| `Bars` | Light | Bar chart left (1056 wide) + 3 projection rows right (672) | 12 |
| `Matrix` | Dark Background | 2 hero anchors (480 wide) + 3 × 2 icon cells, **footnote band** | 13 |
| `Before / After` | Light | 2 panels, 4 one-line claims each at 30/38, muted vs `--color-light-text` | none |
| `Competitive Table` | Light | Head row 69px + 5 rows × 128px; criteria 576 + 4 vendor columns of 288 | none |
| `Positioning 2×2` | Light | Axes as Rulers at x 960 / y 700, 4 plotted dots, 2 corner axis labels | none |
| `Capture Bleed Bottom` | Light | Header + slot 1728 × 734 running off the bottom. **No 1056 cap** | 17 |
| `Split Copy / Image` | Light | Copy column 96→960 + slot 960 × 710 off the right trim | none |
| `Bento Grid` | Light | 4 × 3 tiles (414 × 286, 24px gutters), headline in 2 merged cells. **No header band** | 16 |
| `Capture Centred` | Light | Header + slot 1200 × 560 centred + caption | none |
| `Capture Full-bleed` | Slot (#666666) | Slot 1920 × 1080, white eyebrow / meta / caption. **No 344 cap** | none |
| `Line / Area` | Light | Full-width plot, 8 points on 206 columns, area wash + solid/forecast stroke | none |
| `Horizontal Bars` | Light | Label column 96→672, bars from the vertical at 672, 5 rows × 142 | none |
| `Stacked Bars` | Light | Full-width, 5 bars of 160 in three blue steps, totals above | none |
| `Waterfall` | Light | 5 steps of 200 with connectors; peak scaled to **440**, not 490 | none |
| `Chart + Hero Number` | Light | Hero 240/232 left, 5-bar plot in the right column (max 400) | none |
| `Two Charts` | Light | Two 784-wide plots of 4 bars, sub-titles instead of a legend | none |
| `Agenda` | Light | 8 items, 2 columns × 4 rows of 177, ordinal in a fixed 60px slot + title 30/38 | none |
| `Section Divider` | Royal Blue 500 | Section number 160/160 + title 128/128, both left-aligned. **No header band, no eyebrow** | none |
| `Quote Statement` | Royal Blue 500 | One quote at 72/96 Onest Regular, left-aligned, + attribution. **No header band** | none |
| `Closing` | Royal Blue 500 | `Thank you.` 128/128 + one contact block; the Cover's spine and wordmark | none |
| `Logo Wall` | Light | 4 × 4 ruled cells, one 240 × 80 logo slot centred in each | none |
| `Hero Testimonial` | Royal Blue 500 | One vertical at 640: 240 portrait + attribution left, quote 60/80 right | none |
| `Case Study` | Light | Logo slot + two labelled blocks left, 3 Ruler-separated stats right | none |
| `Team 3-up` | Light | 3 columns, 200 portrait + name 30/38 + role + bio 22/32 | none |
| `Press & Investors` | Light | 2 bands split at 700, each a label + note and 3 logo slots | none |
| `Columns 2-up` | Light | 2 columns of 784, ordinal 96/96 + title **40/48** + body | none |
| `Columns 3-up` | Light | 3 columns of 496, ordinal 96/96 + two-line title 30/38 + body | none |
| `Icon List` | Light | 5 rows of 142: 40px icon + title 30/38 left of the 671 vertical, body right | none |
| `Timeline` | Light | 4 marks on an axis at 664, period above / title + body below | none |
| `Roadmap` | Light | 3 phases, timeframe + title 40/48 + 4 Ruler-separated items of 100 | none |
| `Manifesto` | Dark Background | 3 claims at 128/128 in the **lower two thirds**; the 20→560 band stays empty. **No header band** | none |
| `The Ask` | Dark Background | Headline 96/96 + lead above the 800 Ruler, 3 use-of-funds figures below. **No header band** | none |
| `Number Full-bleed` | Dark Background | One figure at **480/440**, the deck's largest type, + a 30/40 caption. **No header band** | none |
| `Two Numbers` | Dark Background | Full-height vertical at 960, one 240/240 value per half. **No header band** | none |
| `Cohort Curves` | Dark Background | 3 series from one origin on the 206 columns; axis starts at 85%, noted in the legend | none |
| `Market Sizing` | Dark Background | 3 blocks nested from a shared bottom-left corner, **areas derived by √ratio** + 3 Ruler-separated legend rows with swatches | none |
| `Platform Stack` | Dark Background | 4 full-width bands of **unequal height** (160/160/160/230), label lane split at 608 | none |
| `Key-value rows` | Dark Background | 5 rows of 142, labels left, values **right-aligned** past the 1247 vertical | none |
| `The Wedge` | Dark Background | **Radial**: 6 satellites of 320 × 120 converging on a 420 × 220 royal-blue core carrying the wordmark, through two hairline buses | none |
| `Cost Stack` | Dark Background | Two **horizontal** stacked bars (1728 vs 642), 5 segments vs 1, **footer band** | none |
| `Proof Stack` | Dark Background | 3 full-width bands, each a stat 80/84 left of the 608 vertical + quote and attribution right | none |
| `Capture + Scrim` | Slot (#666666) | Full-bleed slot + `BK Fade` to 65%, copy on the scrim. **No 344 cap** | none |
| `Screen Trio` | Dark Background | 3 portrait slots 260 × 520 centred in their columns + captions | none |

Note: `charts.md` ("Name the mark in place") states that once `Market Sizing`'s blocks carry their own names, the legend swatches have no job left. Check the canvas before relying on the swatch description above.

The source deck has no closing slide.

**The meta page number is `NN` on every template, on purpose.** It is a placeholder: the exporter (see the `archy-design:slides-export` skill) substitutes the real number from the slide index. Hand-typing fifty-five numbers is the same staleness trap as numbering the artboards.

---

## Deriving a new layout

**Rename the duplicate before anything else.** A derived artboard keeps the source's name, and the name is the only thing that carries the slide number; the exporter orders the deck by it. Shipping `69` still called `42 · Hardware In The Practice` is silent until someone reads the layer tree.

**Derive a new light layout by duplicating `Metrics 2×2`,** not by building from scratch: the Rulers frame, the Meta line and the three-part header come out identical by construction, and all that is left is repositioning the verticals, swapping the eyebrow/headline/page number and replacing the body frame. Set the duplicate to `display: block` and `translate: none` on every ruler you move (see `../../brand/references/paper-quirks.md` for why a duplicate's `translate` is stale).

---

## Image slots

A template carries an image **slot**, never a real capture, the way `Quotes` and `Team grid` carry `--color-blue-tint-200` placeholder circles instead of photographs. That is what makes Showcase buildable without deciding anything about importing assets. `Bento Grid` and `Capture Bleed Bottom` are source slides 16 and 17.

| Slot | Fill | Why |
|---|---|---|
| Standard (light ground) | `--color-neutral-lightest` (#EEEEEE), centred `CAPTURE` label 20/24 uppercase `0.05em` in `--color-neutral-light` | #EEEEEE is the site's own hairline grey and reads unmistakably as "a block goes here"; `--color-neutral-super-light` at 3% off white is too faint to register as a slot |
| Full-bleed | `--color-neutral` (#666666) | The white eyebrow, meta, caption *and* the Rulers all read on it. On a pale slot they vanish and the template previews as broken |
| On a dark ground | `--color-neutral` (#666666) | See `dark-set.md` |

On the full-bleed slot, the Rulers were built at white 0.3; that is legacy, and a solid light grey is the current rule (see `../../brand/references/composition.md`). The pale-slot failure is a template legibility problem, not a design one, but it makes the layout impossible to review.

- **A full-bleed slot must be the first child.** Added last it sits on top of the Rulers, Meta and header and hides them. `move_nodes` to index 0. Paper's own guide also warns that an artboard-covering absolute element blocks cursor interaction underneath; for a full-bleed layout that is unavoidable, so expect to select those layers from the tree.
- **A bento is tiles with gutters, not a ruled grid.** `Bento Grid` separates its slots with 24px gaps and carries only the 20 / 1056 caps, no Rulers between tiles. That is what the source does, and a bento whose cells were ruled would read as a table of pictures.
- **A layout whose image bleeds off an edge drops the cap on that edge.** `Capture Bleed Bottom` has no 1056 rule and `Capture Full-bleed` no 344 rule: a Ruler cutting across an image reads as a scratch. The caps that still apply stay exactly where they are.

A logo slot uses the same construction (240 × 80, `LOGO` label); see `slide-system.md`.

---

## Page splitting and node weight

**The pages are split for findability first.** The category answers the question a person arrives with; that is the reason, and it stands on its own.

**Node weight is a secondary consideration, and the old "~1,000 nodes per page" ceiling is not well established.** It came from the first 14 artboards sitting on one page at 834 nodes and the file feeling heavy. But `Brand`'s Icons page renders fine at **1,100 nodes on a single page**, which is direct evidence against that figure, and when this file's renderer got stuck (see `../../brand/references/paper-quirks.md`) it was stuck for the whole *file*, with `Charts` failing at only 450. So node-count-per-page is probably not the real constraint.

Measured at 55 layouts, for reference rather than as a limit:

| Page | Layouts | Nodes | Note |
|---|---|---|---|
| Lists | 10 | ~480 | The heaviest: `Logo Wall`'s 16 slots and `Icon List`'s five icons are ~30 nodes each on their own |
| Charts | 9 | ~450 | |
| Comparisons | 7 | ~425 | |
| Proof | 8 | ~380 | |
| Frames | 8 | ~200 | |

**The trigger for splitting a category should be that the page feels slow in use, not a number.** When it happens the fix is cheap and proven: `move_nodes` to another page's root preserves node ids and leaves absolutely-positioned children untouched.
