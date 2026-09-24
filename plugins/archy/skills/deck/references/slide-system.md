# Slide System

Read this when building, deriving or reviewing any 1920 × 1080 slide: canvas, type scale, header, meta line, Rulers, source transcription, dark-ground mapping, bands, lanes, rows and icons.

The template library lives in the Paper file **Master - Decks** (`app.paper.design/file/01M1HZF1EW0RX9H3YSMJ3GAMK7`). For the roster see `layout-catalog.md`; for dark layouts `dark-set.md`; for charts `charts.md`. Getting a slide or a deck out to Google Slides is covered by the `slides-export` skill. Brand-wide rules (tokens, solid Rulers, wordmark) live in `../../brand/references/tokens.md` and `../../brand/references/composition.md`; Paper tool behaviour in `../../brand/references/paper-quirks.md`.

---

## Canvas and type scale

**Canvas 1920 × 1080**, exactly 2× the Google Slides export (960 × 540), so every source value doubles cleanly. Margins **96** all round; content column 96 → 1824 (1728 wide).

**Type scale**, derived from the original investor deck (pt × 1.333 × 2):

| Role | 1920 |
|---|---|
| Cover title | 128 / 128 |
| Big number | 160 |
| Stat | 80 / 84 |
| Headline | 60 / 70 |
| Subhead / cell label | 30 / 38 |
| Body | 22 / 32 |
| Eyebrow, role | 20 / 24 uppercase `0.05em` |
| Meta | 18 / 22 |

### Five extra scale steps

All added because the 1080-derived scale left the band looking empty:

| Role | Size / leading | Where |
|---|---|---|
| Hero big number | 320 / 300 | `Big Number`: the deck's largest type, 2.5× the cover title |
| Anchor number | 96 / 96 | `Matrix`: same step as the column ordinal |
| Column ordinal | 96 / 96 | `Columns 4-up`, `Numbered rows`: sits between Stat (80) and Cover title (128) |
| Secondary value | 40 / 48 | `Split stats`'s wide-row values, `Matrix`'s pool values: the tier below Stat (80) |
| Pull-quote | 36 / 52 | `Quotes`: Onest **Regular**, between Headline (60) and Subhead (30) |

### Stat colour

**Stat values are royal blue on light and `--color-blue-tint-300` on dark, at every tier.** That is the one colour rule the numbers follow across `Metrics 2×2 / Quotes / Metrics 3-up / Split stats / Bars / Matrix`. The exception is a *secondary* value sitting beside a primary one in the same layout: `Split stats`'s wide-row values go `--color-light-text` at 40/48 so the 80px royal-blue row above stays the hero. Two blue tiers in one slide dilutes both.

---

## The three-part header

**Every slide carries the same three-part header:** eyebrow top-left (`--color-royal-blue-500` on light), meta top-right, two-tone headline below. The headline is **two stacked text nodes**, because Paper cannot colour part of one: first line `--color-light-text`, second `--color-neutral`.

**The meta line is `[optional slot] | ARCHY © 2026 | NN`.** The optional slot holds free text ("Confidential", a client name, nothing) and is grouped **with its own divider** so deleting one node leaves a clean `ARCHY © 2026 | 01`.

### Header on a dark ground

**On a dark ground the header inverts, and it is a fixed mapping**, not a per-slide decision:

| | Light ground | Dark ground |
|---|---|---|
| Eyebrow | `--color-royal-blue-500` | `--color-blue-tint-300` |
| Headline line 1 | `--color-light-text` | `--color-white` |
| Headline line 2 | `--color-neutral` | `--color-blue-tint-200` |
| Meta text / dividers | `--color-neutral-light` / `-lighter` | `--color-blue-tint-200` / `-300` |
| Rulers | `--color-light-border` | solid `--color-dark-border` (#0000C9); never `--color-white` at `opacity` (see the solid-Rulers rule in `../../brand/references/composition.md`) |
| Body copy | `--color-neutral` | `--color-blue-tint-200` |

On the **royal-blue** ground (Cover, Statement) the headline's second line is `--color-blue-tint-300`, not `-200`: on the bright blue the 200 is too close to white to register as a second tone. Only the dark navy ground uses 200.

---

## The Rulers frame

**Slides use the full Rulers frame**, not just cell separators: full-bleed horizontals at y **20 / 344 / 1056** capping the top, the header band and the foot, plus verticals at the column boundaries running between the header and foot rules. A 4-column grid puts them at 96 / 528 / 960 / 1392 / 1824; a 2-column grid at 96 / 960 / 1824. This is the same graph-paper device as the website and the event posters.

**A slide with no header band gets only the two caps.** `Statement` and `Cover` carry the 20 and 1056 horizontals and nothing at 344: there is no header band to cap. The Cover adds **one vertical at 1315** (layer `Ruler V Divider`) running the full 20 → 1058, the deck's only full-height rule: it opens a right column that the meta line sits at the top of and the wordmark fills at the bottom. Do not give the Cover verticals at 96 / 1824. Two horizontals plus one vertical is a spine, and adding the outer pair turns it into a box.

### The Cover vertical is positioned by its gutter

**That vertical is positioned by its gutter, not by a column boundary**, and it is the one rule in the system that is. The Cover has no columns of content for a line to align to, so what governs it is clearance to the meta block, whose left edge Paper resolves to **1413** (the meta is right-aligned to 1824 and its five nodes plus gaps measure 411). Snapped to the 4-column boundary at 1392 it left only a 24px gutter and read as crowding the "C" of CONFIDENTIAL. **Settled: the gutter decides it, and the gutter is 96, the page margin.** The line sits at **x 1315** (2px wide), so its right edge is 1317 and 1413 − 1317 = 96.

**That 1413 is a measured flex result, not a constant.** It was once documented as 1416 from arithmetic; the real value is three pixels left of that. It depends on the meta's own copy, so if the optional slot changes from `Confidential` to something longer, re-check the clearance. 1315 is derived, not sacred.

Snapping to the module was the tidier-looking answer and it was wrong: `96 × 14 = 1344` puts the right edge at 1346 and *narrows* the gutter to 70, moving the line toward the very content it needs to clear. When a rule's job is clearance, the clearance is the derivation; the module is not. This is the only rule in the system positioned that way, which is exactly why it needs a stated reason rather than a hand-placed number.

### Taking structure, not coordinates, from a source deck

A source deck's layout is a reference for *which* elements exist and what they separate, never for where they land. Example, the original investor deck: **its Rulers are close to ours but not ours, and the difference is deliberate.** Measured off the PDF at 2× (`pdftoppm -png -r 96` gives a 960 × 540 render that maps 1:2 onto the canvas):

| | Source deck | This system |
|---|---|---|
| Horizontals | 48 / 326 / 676 / 1032 | **20 / 344 / 1056** (+ per-layout separators) |
| Left / right verticals | 96 / **1806** | 96 / **1824** |
| Cover vertical | 1186 | **1315** |
| Rule colour on blue | white at ~0.22 | **solid `#2A5DF6`**, never translucent (see `../../brand/references/composition.md`); the deck artboards built at white 0.3 are legacy |

The source's right margin is 114 against a left margin of 96: an asymmetry from hand-building, not a design. Its cover vertical at 1186 sits on no column boundary at all. **Take the source's structure, not its coordinates:** which rules exist and what they separate is the thing to copy; where they land comes from this system, so that the artboards line up when you page through them.

### Colour intruders in a source deck

**Source decks are rarely tokenised** (the investor deck used 6 real tokens out of 22 values). Map every source colour to its nearest token. Recurring intruders seen so far, beyond the usual Tailwind ones:

| Source hex | Token |
|---|---|
| `#0F172A`, `#10123C` | `--color-blue-tint-800` |
| `#0740FF`, `#2057FE`, `#3B6EFF`, `#2240F0` | `--color-royal-blue-500` |
| `#1729A5` | `--color-primary-blue-600` |
| `#6B7089`, `#94A3B8`, `#A8ADC8` | `--color-neutral` / `-light` |
| `#53BFFF` | `--color-blue-tint-300` |

**Expect no template system in the source.** The investor deck's 18 slides all sit on the "DEFAULT" layout: hand-built slides, which is exactly what the Master - Decks library replaces.

---

## Content is transcribed, never authored

When an existing deck is being redesigned, the job is to re-set its content in this system, not to edit it.

**Copy on a redesigned slide is the source's, character for character.** That includes dashes (an em dash stays an em dash), arrows, symbols, capitalisation and the count of items in a row. Verify by extracting every `<a:t>` run from the source `.pptx` slide and diffing it against the Paper text read back with `get_node_info`: the eye does not catch a dropped photo or a swapped dash.

**The meta slot is the one place source content is dropped rather than transcribed.** Page numbers, `Confidential` or production notes that the source parked in the top-right corner are chrome, not the slide's argument; the deck's own meta constant owns that corner. Everything inside the content column still transcribes exactly.

**Work from the one source version the requester gave you.** If a folder holds several versions of a deck (`v1`, `v2`, `final`), ask which one is the reference before starting, and do not switch mid-deck even if another looks more current. Versions differ in ways that look like improvements and are not yours to apply. Never assume page numbers line up across versions.

**Type is the one thing that does scale up.** Source decks are often set small (24pt headlines, 9.5pt captions); this system runs 60/70 headlines and 22/32 body because decks are read on a big screen. Plan for the consequence: copy that fits on one line in the source often will not here. Stack it or rewrap it first; step below the scale only as a last resort, and report any cut or size change.

---

## Composition in the band

**A branching diagram's fan-out is a free parameter, so size it to the band.** Slide 82 sends one node to two destinations, and the vertical distance between those two is decided by nothing but the designer. It shipped at ±111px from the axis and was opened to ±191 in review. The compressed version was not wrong anywhere locally (the bus was symmetric, the block was centred, every lane held); it just left 200px of empty band under a diagram that had no reason to be small. **Where a dimension is not derived from data or from the grid, the band's own height is what should derive it**: the same instinct as "type runs bigger than feels safe", applied to a distance instead of a size. This does not license inflating gaps *inside* a block, which is still a defect; it applies only where the spacing is the diagram's own geometry.

**A band with air under it is the family's normal state, not a defect.** Cells are top-aligned in the 344 → 1056 band, so a short column leaves 200–250px empty at the bottom. `Metrics 2×2`, `Columns 4-up` and `Quotes` all do this, and so does the source deck. Do not fix it by centring the cells (that breaks the shared lanes) or by inflating the gaps. The only legitimate fixes are bigger type or more content.

---

## Bands below the content

Two devices hang a strip under the content band. Both keep the family's 20 / 344 / 1056 full-bleed Rulers exactly where they are and add one more Ruler; **the content band shrinks, the caps never move.**

| | Extra Ruler | Content band | Strip | Type |
|---|---|---|---|---|
| **Footer band** (`Product grid`, `Metrics 3-up`) | full-bleed at **958** | 346 → 958 = **612** (two rows of 305) | 960 → 1056 = 96 | One takeaway line, 22/32 Inter Medium `--color-light-text` |
| **Footnote band** (`Matrix`) | full-bleed at **936** | 346 → 936 = **590** (two rows of 294) | 938 → 1056 = 118 | Sources note, 18/26 `--color-blue-tint-200` at `opacity: 0.6` |

**Column verticals stop at the extra Ruler**, not at 1056: height 614 for a footer band, 594 for a footnote band. That is what makes the strip read as a separate band rather than the last row of the grid.

**A footer band holding a label *plus* a note starts at x 96**, aligned with the eyebrow and headline rather than at the cells' 40px inset: the strip belongs to the header's level, not the grid's. **A band holding one takeaway line on its own is centred**, and that is a correction, not a variant: the line was left-aligned on slide 78 and moved back to centre in review. Left-aligning a single sentence under a full-width grid leaves a long tail of empty band to its right, which reads as a line that failed to fill rather than as a closing statement. The x-96 rule needs a second element to hold the other end of the strip.

The footer line is a *conclusion*, not a caption. It earns the band only when it says something the cells above do not.

---

## Lane alignment: the rule that keeps biting

Three separate layouts broke the same way, so state it plainly: **in a vertically centred cell, every element after the first must have a fixed height, or the cell's content drifts off the shared lane.** A stack that is centred inside a fixed-height cell places its *middle* at the cell's middle, so one cell whose last element wraps to fewer lines pushes everything above it upward. Symptoms seen: `Split stats`'s three stat values off by 15px because one meta ran to two lines; `Matrix`'s first pool title and value off by 13px because one body ran to one line.

The fix is a fixed height on the **last** element (`Split stats`: Meta `height: 56` = 2 × 28; `Matrix`: Body `height: 52` = 2 × 26). It is invisible, because the slack extends downward into the cell's own air.

This is the opposite of `Columns 4-up`'s lesson, and the difference is *which* element gets pinned:

| Pin | Result | Verdict |
|---|---|---|
| **The last element** | The extra height falls into empty space: no visible change, lanes fixed | Correct |
| **A middle element** (`Columns 4-up`'s title box at 76px) | The extra height becomes a gap between two pieces of text that should be tight; one-line titles read as floating | Wrong: fix the copy instead, forcing the line break with `\n` in `set_text_content` |

Row-level rules:

- **An icon beside a two-line title centres against the whole title block; an ordinal does not.** They look like the same problem and they are opposites. An ordinal is a position in a sequence, so it has to sit on the first line's line box or it stops reading as "item 4". An icon is a glyph *for the whole name* (`Product`/`configuration` is one label), so centring it on the block's middle is what makes it look attached to both lines. On slide 78 the icons shipped aligned to the first line and were moved down to the block centre in review: at 40px against a 76px stack the difference is 19px and it is very visible.
- **An ordinal beside a two-line stack must align to the title, not centre against the stack.** Let the stack hug (`height: fit-content`, `align-items: flex-start`) and let the row's own `align-items: center` place it; then the ordinal's line box lands on the title's. Centring the ordinal against the whole stack drops it between the two lines.
- **Top-align a value against its neighbouring text with one shared `padding-top`, never with per-cell centring.** In `Split stats`'s wide rows, a single 40/48 value centred in its cell sat 20px below the 30/38 title centred in the cell beside it. Setting `justify-content: flex-start; padding-top: 56px` on both cells puts the two line boxes on one lane with one number instead of two guesses.

---

## Rows, marks and lanes

Rules from building the Lists and Proof families, all about where a piece of content lands relative to something else.

**A separator Ruler between equal rows must fall equidistant between the two rows it separates.** `Roadmap`'s items sat at the *top* of their 100px rows, so each Ruler was 64px below the item above it and 36px above the item below; it read as belonging to the row underneath. Centring the item in its own row is the fix, and it is the general case of the rule that a Ruler separates rather than brackets. Give the item `height: fit-content` and place it at `row + (rowHeight − lineHeight) / 2`; a longer item then grows downward into the row's own slack.

**An ordinal beside a title goes in a fixed-width slot, never after a gap.** `Agenda` puts the number in a 60px `flex-shrink: 0` slot with a 20px gap, so `01` and `08` put their titles on the same lane. `gap` alone drifts the moment one string is wider than another.

**An icon, a title and a body in one row need three different offsets, not one.** In `Icon List` a 40px icon, a 30/38 title and a 22/32 body sit at `row + 45 / 46 / 49`, which puts their three line boxes on one optical centre. A single shared offset lands the icon a few pixels off the title's baseline, and at 40px that is visible.

**A connector is centred between ink, not between boxes.** The four engine steps on slide 84 sit in equal 322px boxes, but the copy inside them is 212–276 wide and varies per step. Centring each arrow in the gap between the *boxes* put it hard against the step it points at and left a hole behind it; re-centring on the gap between the previous step's last glyph and the next step's left edge moved all three left by 24–48px and made the row read as a chain. **A box is a layout convenience; the reader only sees ink.** This is the same principle as the Cover's vertical being derived from its gutter rather than from a column boundary: where an element's job is to span a clearance, the clearance is what derives it. Measure the ink (the `width` a `max-content` node reports, or the batched-width trick in `../../brand/references/paper-quirks.md`) rather than assuming the box is full.

**A mark sits at the content edge of its column, not centred in it.** `Timeline`'s dots are at x 136 / 568 / 1000 / 1432, the cells' own 40px inset, so every period, title and body left-aligns to the same lane the eyebrow and headline use. Centring the mark in its 432px column forces the labels to centre with it, and centred body copy at 22/32 in a 360px measure reads badly.

**A logo is a slot, exactly like a capture.** A 240 × 80 `--color-neutral-lightest` rect with a centred `LOGO` label, the same construction as an image slot (see `layout-catalog.md`). `Logo Wall`, `Case Study` and `Press & Investors` all use it; a template never carries a real mark.

**A chart-style axis is the one Ruler allowed to be a step darker.** `Timeline`'s axis is `--color-neutral-lighter` (#CCC) rather than `--color-light-border` (#EEE). At Ruler weight it is indistinguishable from the four column verticals it crosses, so nothing tells the reader which line is the timeline. This is the only place in the system where a rule steps up, and it exists because the rule *is* the content there, not the structure.

**The Status pill has two states, so a three-state layout cannot use it.** `Roadmap` needs Now / Next / Later, and the pill only codes shipped vs not. The timeframe eyebrow carries the state in its colour instead: `--color-royal-blue-500` / `--color-neutral` / `--color-neutral-light`, three clear steps and no new component. Reach for the pill only when the states are genuinely binary, as in `Product grid`.

**Past and planned are coded the same way everywhere.** `Timeline`'s marks follow the charts: shipped is `--color-blue-tint-200` with a `--color-neutral` label, planned is `--color-royal-blue-500` throughout. The claim is identical to the chart's actual/forecast split (see `charts.md`), so the coding is too.

---

## Icons and the Status pill

**Hugeicons on a slide run at 40px, not 32.** 32 is the arithmetically "correct" 24-grid scaled 1.33×, and it reads timid next to a 30px title. Stroke stays 1.5. Colour is a token on the `<svg>`:

| State | Colour |
|---|---|
| On light | `--color-royal-blue-500` |
| On dark | `--color-blue-tint-300` |
| Secondary or not-yet-shipped | `--color-neutral-light` |

Icon and value sit in a `Head` row (`justify-content: space-between`) at the top of the cell: icon left, value right. That right-aligns every value into a lane and gives the icon a fixed left edge.

**The Status pill from the website earns its place when it carries state, and only then.** `Product grid` uses it to separate shipped from roadmap, which is the whole point of the slide:

| | Fill | Dot | Label |
|---|---|---|---|
| Shipped (GA) | `--color-blue-tint-100` | `--color-royal-blue-500` | `--color-royal-blue-500` |
| Roadmap (H2, 2027) | `--color-neutral-super-light` | `--color-neutral-light` | `--color-neutral` |

Keep the structure identical across every cell and let colour do the work; the product name stays royal blue in both states, and the roadmap cells' icons go `--color-neutral-light` to reinforce it. A pill on every cell with no state to signal is the banned "outlined pill with a word inside it".
