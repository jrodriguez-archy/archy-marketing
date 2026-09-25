# Offsite 2026 identity

Read this when building or editing any Archy Offsite 2026 piece (key art, lockup, badge front or back), or when you need the Offsite palette, file structure or badge geometry.

The Paper file **`Archy Offsite - 2026`** (`app.paper.design/file/01M1J43XB229DWACG11Z51P1AV`) holds the Archy Offsite 2026 event identity.

**It does not use the Archy design system.** No tokens from Brand, no Onest/Inter scale, no Rulers, no mascot. It borrows Archy's blues and the arch icon, but it is its own thing with its own token set. Do not "correct" it toward the Archy tokens.

## Palette

Seven values, all in the file as tokens. Read from the RGB master. **The badge artwork is CMYK and its hexes are conversion artefacts, not the palette.** Always take colour from the Paper file or from the RGB master artwork.

| Token | Hex | Carries |
|---|---|---|
| `--color-navy` | `#00005B` | The ground. The only background in the identity |
| `--color-white` | `#FFFFFF` | ARCHY wordmark, location line, the arch inside the icon |
| `--color-royal` | `#003EF9` | Archy icon disc |
| `--color-cyan` | `#009DFF` | Offsite script, the signature colour of the event |
| `--color-sky` | `#62C5FF` | 2026 |
| `--color-ice` | `#CDEBFF` | Lightest blue. Dot frame only |
| `--color-gold` | `#FFC302` | Sparkle. One warm accent on one element; do not spread it |

The dot frame runs all five blues plus white in a deliberately irregular sequence (cyan 29, royal 21, sky 20, ice 16, white 10 across 96 dots). It is not a repeating pattern; do not "fix" it into one.

## File structure

Both artboards paint `--color-navy` as their own background; there is no background rectangle.

- **`01 · Key Art`, `1920 × 1080`** (the artboard)
  - `Dot Frame`: 96 × 22px dots, ~59px pitch, inset 30px from the trim
  - `Lockup` (Frame, 403 × 476) → `Year 2026` · `Sparkle` · `Offsite` · `ARCHY` · `Location` · `Archy Icon`
- **`Asset · Lockup`** (600 × 700): the `Lockup` frame alone, centred. **This is what new pieces clone**, via `<x-paper-clone node-id="…">`

Artboard names in this file join their parts with an em dash (for example, key art, then size). Search by the distinctive part (`Key Art`, `Badge`, `Poster`) rather than retyping the full name.

**Paper has no `<g>`.** `write_html` silently drops one, so a group inside an SVG is built as a **nested `<svg>` with a tight viewBox**: create it with a throwaway `<rect fill="none">` child, `move_nodes` the real elements in, then delete the placeholder. The children keep their original absolute coordinates and the viewBox does the offset, so nothing has to be re-drawn, and z-order survives as long as the groups are contiguous runs of the original order.

Everything is outlined vector. There is no live text, so copy cannot be edited; new wording means new artwork.

## The badge is the reference for new pieces

The source badge (`Archy_Offsite_Badges_v3`) is 294.48 × 408.24pt, both sides:

- **Front**: lockup, a single row of dots as a divider, then attendee name, role, and a full-bleed department band at the foot (`MARKETING`)
- **Back**: `TEAM OFFSITE` / `SEP 8 - 10 // LAS VEGAS` masthead with the Archy wordmark opposite, then the agenda: a blue day header per day (`TUE · SEP 8`), rows of time + bold title + light detail, meal rows set as dashed rules with the meal name inline, and a footnote on rooms

Type is **Interstate** (Bold / Regular). The dashed meal rule and the day header band are the two devices worth carrying into other pieces.

## Rebuilding the badge

**Canvas 589 × 816**, twice the source's 294.48 × 408.24 pt. Every source value doubles cleanly, and type lands on sane numbers. Print output needs its physical size set on export; the source PDF declares MediaBox = TrimBox = BleedBox, so **there is no bleed defined**. Resolve that before it goes to a printer.

**Interstate is not installed. The substitute is Overpass**, which descends from the same Highway Gothic lineage and is the closest thing available. Weights: Regular 400 for name and detail, Bold 700 for the department band and headers.

### Front

All measurements at 589 × 816:

| Block | Geometry |
|---|---|
| `Lockup` | 273 × 322 @ 159, 79: the `Asset · Lockup` frame at 0.677×. Resize each group SVG *and* the frame; Paper has no `scale` |
| `Dot Divider` | 18 dots, 11px, flex row `space-between` across 497 @ 46, 428 |
| `Attendee` | Centred column, gap 22. Name 44/48 white, role 36/40 `--color-sky` |
| `Department Band` | Full bleed 589 × 146 @ 0, 670. 60/60 Bold, `0.02em`, white on `--color-royal` |

**Open decision: the department band's blue.** In the CMYK file the band (`#004899`) and the icon disc (`#2b4f9e`) are *different* blues, so the original has a colour the RGB key art does not. It is currently set to `--color-royal`, which makes band and disc read as one blue. That is a tighter system, but it is a decision to confirm, not a fact.

### Back

Artboard `03 · Badge`, `Back`:

| Block | Geometry |
|---|---|
| `Masthead` | @ 47, 78. `TEAM OFFSITE` 28/30 Bold `0.02em`, dateline 16/20 Bold `0.04em` `--color-sky` |
| `Archy Wordmark` | 156 × 60 @ 392, 76: the 5-path mark lifted from the badge back, not from `index.html` |
| `Schedule` | Column @ 47, 142, width 495. Days butt against each other: **no gap between a day's body and the next day's header** |
| Day header | Full-width band, h 39, padding 0 13, 18/18 Bold `0.04em` on `--color-royal` |
| Day body | `--color-navy-panel`, rows and meal rules stacked with gap 0 |
| Session row | h 46, padding 0 13. Time slot **78px fixed**, then title 14/17 Bold white + note 14/17 `--color-sky` |
| Meal rule | h 28: `[dash 70px] [label] [dash flex:1]`, label 14/16 Bold `0.03em` `--color-ice` |
| `Footnote` | Centred, 13/17 `--color-ice` @ 47, 762 |

**The time column is a fixed 78px slot, not a gap.** Every row's title has to start on the same lane; `gap` alone drifts as soon as one time string is wider than another.

**The dashed rule is a `border-top: 2px dashed`, not a gradient.** `repeating-linear-gradient` is accepted by `update_styles` and reported back, and paints nothing (same failure mode as a Text node's `backgroundColor`). The border renders.

**Overpass's middle dot `·` has almost all its sidebearing on the left**, so ` · ` renders as ` ·Word`, glued to whatever follows. Extra spaces do not fix it. Use the bullet `•` as the separator throughout this project.

**The agenda source carries a Location column the badge has no room for.** Fold the location into the note line after a bullet (`Until 5:00p • Lotus Room`), which is what the source badge does. Rows that would run to a second note line get their detail cut, not their type shrunk.

**`duplicate_nodes` inserts the copy next to its source, not at the end of the parent.** Duplicating a meal rule to build the next one lands it directly under the original, so a day comes out `rule · rule · row · row`. Fix the order with `move_nodes` (`{nodeId, before: siblingId}`) and verify.
