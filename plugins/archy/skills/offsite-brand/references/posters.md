# Offsite XL poster family (768 × 1296)

Read this when building or editing the Offsite 2026 venue display posters (the Welcome poster or any of the daily agendas).

Four screen pieces for the venue displays, rotating in pairs: `04 · Poster`, `Welcome` (fixed, repeats every day) plus one of `05/06/07 · Poster`, `Tuesday / Wednesday / Thursday`. In Paper the artboard names join the two parts with an em dash; search by the day name. Ratio 1:1.69, so hierarchy resolves in stacked blocks. This is a display, not print, so nothing runs below 26px.

**Shared grid.** Margins 64 all round, content column 640. The footer band is the one full-bleed element, 768 × 116 @ 1180.

## Welcome

The badge front re-proportioned: `Lockup` 480 × 567 @ 144, 164 (the asset at 1.191×) → `Dot Divider` @ 802 → `WELCOME` 128/128 → dates 48/56 `--color-sky` → venue 32/40 `--color-ice`. **It has no footer band.** The ink is centred in the canvas instead, 164 top and bottom.

**FutureProof does not appear on any piece.** The agenda source carries `Ahead of FutureProof 2026` as a third, subordinate line. It is context, not a message, and at band scale it reads as though the offsite were part of FutureProof. Do not add it.

## The agendas

The badge back re-proportioned: masthead + `Archy Wordmark` 200 × 77 → `Dot Divider` → weekday 96/96 white + date 52/58 in the day's accent → `Agenda` panel 640 × 720 @ 64, 440 → footer band in the day's accent.

| Module | Geometry |
|---|---|
| Session row | padding 0 32. Time slot **140px fixed** 34/40 Regular white, then title 34/40 Bold white + location 28/34 `--color-sky` |
| Meal row | Same grid, same height. Time and title in `--color-ice`, title uppercase Bold `0.04em` reading `BREAKFAST • UNTIL 9:00a`, plus a **dashed bottom border** |

**Rows carry a location, never a description.** The agenda source's Details column is dropped on the posters: at this size the useful second line is where to go, and the room names are short enough to always fit. The badge keeps the detail; the poster keeps the room.

### Row heights

**Rows fill the panel, and meals get a shorter tier than sessions**, roughly 0.7 : 1, so the panel reads as blocks of work separated by strips. Heights are whatever divides that day's panel (720) exactly:

| | Meal row | Session row | Feature row |
|---|---|---|---|
| Tuesday (2 + 2 + 1) | 104 | 116 | 280 |
| Wednesday, Thursday (2 + 2) | 148 | 212 | (none) |

Do **not** centre a short stack in a fixed panel and leave air top and bottom. Dividing the panel is what makes each day feel sized to its own content.

**A meal row with only one line is centred, not lane-aligned.** Wednesday's `BREAK` has no location. Pinning its content column to the two-line height so the title kept the shared lane left a visible void underneath, which read as content that failed to load. On the shorter meal tier the row is a strip, so `height: fit-content` + `justify-content: center` is right, and the ~19px the title moves off the other meal's lane is invisible. This is the exception to the lane rule, and it exists because the row is a different tier, not because the lane stopped mattering.

**A session row missing its second line needs a fixed-height content column**, not a deleted one. With the location node simply removed, a title centres in the row and drops off the lane every other title sits on. Setting the content column to `height: 72` (34 + 4 + 34) with `justify-content: flex-start` puts it back.

**Alternate the row fill by position, not by type**: odd rows `--color-navy-panel`, even rows `--color-navy-panel-alt`. Strict alternation only survives if it ignores whether a row is a meal or a session; tying the tone to the type produces two same-toned rows in a row as soon as a day's counts are uneven.

**The meal's dashed rule is a bottom border, never a top one.** On top, the first row's rule lands on the panel's own edge and brackets the container. As a bottom border it always falls between two rows.

### Day accent and footer band

**The day accent is two elements and no more: the date line and the footer band.** Tuesday `--color-ice`, Wednesday `--color-sky`, Thursday `--color-cyan`: three clearly separated steps, so the day reads across the room.

The band's line must be **specific to that day and absent from the rows above it**: `REGISTRATION CLOSES AT 12:00P` / `TOPGOLF SHUTTLE FROM 9:30A` / `SALES B/C • P&D D • CX E`. A line that is true of all three days (a dietary note, for example) reads as filler once the posters start rotating. Roughly 30 characters fit at 34px.

Footer text is always `--color-navy` on those three. `--color-royal` is not used as a band anywhere in this family: the Welcome has no band at all, and that absence is what separates it from an agenda at a glance. **Never use `--color-royal` as a text colour on navy**: two dark blues, and it vanishes.

### Panel geometry

**The panel is a fixed size on every agenda.** Tuesday has five items, Wednesday and Thursday four. Holding the panel constant keeps the frame from jumping between rotations, which matters more than the first row landing on the same lane: the pieces are seen in sequence in the same physical frame, never side by side.

**A row can carry a sub-list, and then it becomes the day's feature block.** Tuesday's Team Meeting carries five untimed sections under its location line: bullets at 26/32 **white** in one Text node with `\n` breaks and `white-space: pre`. White, not `--color-sky`: these are content, not metadata, and sky would file them with the room name. That list set the family's geometry: panel 720 @ 440, day block at 250 on all three agendas, so nothing shifts when the posters rotate. Tuesday's rows are 104 / 116 with the feature row at **280**; Wednesday and Thursday go 148 / 212. Both divide 720 exactly.

**A time in a tall row must be pinned to the title, not centred against the row.** With the row's own `align-items: center`, `12:15p` floats down beside the third bullet. `align-self: flex-start` plus a `padding-top` equal to the content column's own offset (15px, half of 280 − 250) puts it back on the title's line box. Centre against the first element, never against the whole stack.

**Row copy has a ceiling.** With the 140px time slot the note column holds about 30 characters at 28px and the title about 20; measure on the canvas when in doubt. Rows are a fixed height, so a note that wraps overflows the module instead of growing it (`Individual team breakouts • Offsite` had to become `Team breakouts • Offsite`). Cut the copy, never the type size.

## Open assumptions to confirm with the requester

- The brief says the Welcome rotates "both days" but asks for three agendas. Treated as three days of rotation, which changes nothing since the Welcome is designed once.
- Delivery is assumed static PNG at 768 × 1296 (export at 2× if the screens are retina).
- No safe-area spec was given. 64px margins are respected everywhere, but the footer band is deliberately full-bleed and would be the first thing a physical bezel clips.
