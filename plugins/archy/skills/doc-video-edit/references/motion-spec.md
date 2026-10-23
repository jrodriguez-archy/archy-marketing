# DOC video motion spec

Exact motion for the DOC video graphics. `scripts/doclib.py` implements all of it; change a value there, not per video. Times are milliseconds from the graphic's start; the geometry of each graphic is the Paper template's (`archy:doc-video`).

## Lower thirds (speaker S3 and captions L1)

Measured frame by frame from the editor's lower-third asset (`02_Lower-third.mp4`, 24 fps) and fitted per track (error ~1 px):

| Track | What moves | Start | End | Curve (cubic-bezier) |
|---|---|---|---|---|
| Red lead | red-500 rect, box size, BEHIND the box, scaleX 0 -> 97 % from the left | 20 | 1000 | 0.2, 0.3, 0.2, 1 |
| Box | video-ground box, scaleX 0 -> 100 % from the left, in front of the red | 100 | 1025 | 0.2, 0.2, 0.2, 1 |
| Name / caption text | clipped by a box-shaped track matte, slides 80 px right to left | 240 | 1000 | 0.2, 0.6, 0.5, 1 |
| Role tag | red-500, grows up from its bottom edge (scaleY, anchor bottom), IN FRONT of the box | 140 | 975 | 0.3, 0.2, 0, 1 |
| Role text | clipped by a tag-shaped matte, rises 46 px | 300 | 1000 | 0, 0, 0, 1 |

- The red only shows as the band in front of the opening box; the box catches it and covers it. It never shrinks, pops or returns.
- Exit: the exact time mirror of every track over the last second (`dur - end` to `dur - start`, mirrored curve). The red is switched off while covered, so the exit has no red.
- Nothing in a lower third fades in or out; everything is revealed or hidden by a wipe, a matte or a scale from an edge.

## Splits (T1 list, T2 numbered, T4 blocks)

- The panel and the speaker framing change on the hard cut.
- Title: opacity 0 -> 100 and 20 px rise, 650 ms, from 60 ms (second title line 90 ms later).
- Rule: scaleX 0 -> 100 from the left, 850 ms, from 220 ms.
- Items, on their words: bullet opacity 350 ms + 22 px rise 600 ms; text opacity + 22 px rise 650 ms. Numbered squares: scaleX 450 ms, digit opacity 200-500 ms.
- Curve for all of these: 0.33, 0, 0.2, 1 (gentle ease-out).

- Section marker (T2 with `highlight`): every item builds with the panel, 120 ms apart from 300 ms; the items not in focus settle at 30 % opacity.

## Number chains (N3, N6, N7, N8)

- Label box (cream-100): 22 px rise + fade, 650 ms; its text 60 ms later.
- Connector (1.69 px ink): draws down 400 ms, starting 350 ms before the result; its red-400 dot fades in 250-500 ms.
- Result box (red-500): scaleX from the left, 450 ms; its text fades in 200-500 ms, and every number in it counts up (same rule as the number card). "=" fades in over the 300 ms before the result.
- Caption: rises like a list item. Each piece enters on the word that says it.

## Number card (T11)

- Hard cut in. Figure rises 30 px, label 20 px 350 ms later (650 ms each).
- Count-up: every number of the figure counts from 0 over 1.3 s from 200 ms, cubic ease-out, then holds (both sides of "1,200 - 1,500" or "20% + 5%"; thousands keep their comma). Step ~1/60 of the value rounded to 1, 2, 5, 10 ...; numbers below 2 stay still. Decimals count in their last place ("3.1 miles": 0.0 -> 3.1 in tenths). Each counter is right-aligned at its final right edge so the text between numbers never moves.

## Closing card (T10)

- Lines rise 24 px (650 ms), the second block 520 ms after the first; lines inside a block 120 ms apart.
- Inside the video (`full_card`, `statement_card`): hard cut in and out, no fade.
- Both fade out over 0.6 s ending 0.4 s before the card ends; the whole card then crossfades 0.4 s into the end card underneath.

## Wipe

- `03_Transitions` is red bars on black: luma key (threshold 0.08, softness 0.05), first 2.4 s of the clip, frontmost layer, gain x4 on its whoosh.
