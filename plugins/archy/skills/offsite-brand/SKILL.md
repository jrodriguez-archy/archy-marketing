---
name: offsite-brand
description: Visual identity for the Archy Offsite 2026 internal event (Las Vegas, Sep 8–10). Load it before designing, editing or reviewing any Offsite 2026 piece, including the key art, the Offsite lockup, attendee badges (front or back), venue display posters (Welcome and daily agendas), or anything else in the `Archy Offsite - 2026` Paper file. The Offsite identity is separate from the Archy brand system.
---

# Archy Offsite 2026 brand

The Offsite 2026 identity is **its own system**. It borrows Archy's blues and the arch icon, but nothing else carries over.

## Separation, both ways

- **Never apply the Archy system here:** no Brand tokens (`--color-royal-blue-500` and the rest), no Onest or Inter, no Rulers, no mascot, no Archy type scale. Do not "correct" an Offsite piece toward Archy tokens.
- **Never apply Offsite tokens to Archy or DOC work.** `--color-navy`, `--color-royal`, `--color-cyan`, `--color-sky`, `--color-ice`, `--color-gold` and Overpass belong to this event only.

Paper file: `Archy Offsite - 2026` (`app.paper.design/file/01M1J43XB229DWACG11Z51P1AV`). New pieces clone the `Asset · Lockup` artboard.

## Which reference to read

| Task | Read |
|---|---|
| Palette, key art, lockup, file structure, nested-SVG technique | `references/identity.md` |
| Attendee badge, front or back | `references/identity.md` (*Rebuilding the badge*) |
| Venue display posters: Welcome, Tuesday, Wednesday, Thursday | `references/posters.md` (and `identity.md` for palette) |

Read the reference before touching the canvas; both carry exact geometry that must not be re-derived.

## Hard rules

1. **Colour comes from the Paper file's tokens** (or the RGB master artwork). The CMYK badge artwork's hexes are conversion artefacts, never the palette.
2. **Gold (`--color-gold`, `#FFC302`) is on one element only: the sparkle.** Do not spread it.
3. **Separator is the bullet `•`, never the middle dot `·`.** Overpass's middle dot glues itself to the following word.
4. **FutureProof never appears on any Offsite piece**, even though the agenda source mentions it.
5. **Type is Overpass** (Regular 400, Bold 700) as the substitute for Interstate, which is not installed.
6. **Navy (`--color-navy`) is the only ground.** Never set `--color-royal` as text on navy; it vanishes.
7. **Prefer cutting copy to shrinking type** when a row or note does not fit, and report what changed.
8. **The dot frame's colour sequence is deliberately irregular.** Do not normalise it into a pattern.
9. **Fixed-width time slots, never a gap**, so every title starts on the same lane.
10. **Dashed rules are `border` dashes**, never `repeating-linear-gradient` (Paper paints nothing).

## Open decisions

- The badge department band's blue: currently `--color-royal`, while the CMYK original uses a different blue from the icon disc. Confirm before print.
- The badge source defines no bleed. Resolve before sending to a printer.
- Poster delivery format, rotation schedule and screen safe area are assumptions (see `posters.md`).
