# Archy video system

Read this before filling, adapting or designing any Archy video graphic. The `Guidelines` page of `Master - Videos` shows the same rules visually.

## Themes

Every template exists in three themes. The ground always carries its pixel grain (the theme's Pixel Gradient image), never a flat fill.

| Theme | Ground | Text | Accents | Moons |
|---|---|---|---|---|
| Royal | `royal-blue-500` + Royal Pixel Gradient | white, secondary `blue-tint-200` | `sky-blue-400` | `primary-blue-600` |
| Navy | `blue-tint-800` + Navy Pixel Gradient | white, secondary `blue-tint-200` | `royal-blue-500` | `primary-blue-600` |
| Ice | `white` + Ice White Pixel Gradient | `blue-tint-800`, secondary `royal-blue-500` | `royal-blue-500` | `blue-tint-200` |

Recolouring a Royal piece:

- **Navy:** navy boxes and chips become royal so they do not disappear into the ground; the chips sitting on them become navy. Lower third, highlight and quote boxes become navy; a `blue-tint-300` pixel accent becomes royal.
- **Ice:** white text on the ground becomes navy, `blue-tint-200` / `blue-tint-300` text and rules become royal, and the wordmark becomes royal (brand rule for light grounds). White active boxes become royal with white text. Navy boxes stay navy. Lower third and highlight boxes become white with navy text.
- Text on a `sky-blue-400` fill is always white, in every theme.
- A QR code stays navy on its white plate in every theme.

## Grid, margins and type

- 1920 × 1080, content inside a 120px margin. Statements and subtitles centre; highlights, chapters and lower thirds align left on the margin.
- Headings in Onest 500 with tight tracking (-0.03em at display sizes); labels and secondary lines in Inter. Product UI keeps Open Sans and the product tokens.
- A long line gets a new break before it gets a smaller size. Avoid a single word left alone on the last line.
- Centre logos and titles optically, not by their box: the wordmark's descender pulls its box down, so its body sits a little above the box centre.
- The wordmark's native ink is 18:7; size it as `18k × 7k` (252 × 98, 432 × 168, 540 × 210, 594 × 231).

## Pixels

- Accents, stepped tags and breaking container edges are built from **16px** cells (32px in the vertical format, so they stay in proportion with the bigger boxes).
- A pixel always touches what it belongs to: an edge, a tag, the end of a bar. No loose pixels floating in the frame.
- Boxes and tags have square corners; product UI keeps its own radius.

## The moon spiral

- The moons are a pixelated spiral of crescents (`primary-blue-600` on Royal and Navy, `blue-tint-200` on Ice). Use them on some openers, titles and end cards only, never on every frame.
- The centre of the spiral always stays off frame: only the outer, larger crescents show, as whole moons with no flat cuts.
- Reuse the ready crops on `Components` › Backgrounds (`1D · Moon Spiral · Right`, `1E · Moon Spiral · Top Right`) and in the templates (vertical crops in V1 and V2). Each crop is its own SVG at the artboard size; scaling or shifting one shows cut edges, so a new placement needs a new crop rendered from the source vector.
- The spiral never sits behind the wordmark or the text.

## Over footage and Overlays

- Over-footage templates show a placeholder footage frame (`slot-image-footage`) so the graphic can be judged in context.
- Their `· Overlay` twin has the footage removed and a transparent ground; any change to the template goes into the twin too.

## Product UI

- Rebuild the UI from the Product UI Kit large enough to read on a phone (body text 22px or more); never shrink a screenshot.
- White card, radius 12, soft navy shadow. One highlight per frame; everything else stays quiet.
- No pixel details on the UI itself; pixels belong to the Archy frame around it.

## QR codes

- Generate a real QR for the exact URL and verify it decodes (the `business-card` skill's `make_qr.py`; a short URL fits version 2, 25 modules). Draw it as an SVG path in navy on a white plate, with `shape-rendering="crispEdges"` and whole-number module sizes.
- Keep at least two modules of white around the code. Name the layer `slot-qr · <url>`.
- Ask the requester to scan it from the screen before delivery.

## Vertical (1080 × 1920)

- For Reels, Shorts and TikTok. Content stays inside 120px at the sides, 220px at the top and 400px at the bottom, clear of the platform's captions and buttons. Background pattern may run into those zones; text, logos and QR codes never do.
- Scale type up for the phone: lower third name about 76px, highlights about 88px, subtitles 60px, titles 120 to 180px.
- Reframe the footage so the speaker sits in the vertical frame.

## Feed (1080 × 1350)

- The 4:5 post for Instagram, LinkedIn and Facebook feeds. Content inside 120px; the same type sizes as the vertical set (titles 120 to 180px, lower third name 76px, highlights 88px, subtitles 48px).
- The product template stacks a large headline above the UI card, centred as a group; there is no side-by-side layout at this width.

## Highlights and subtitles

- **Highlights** carry a short point that reinforces the speaker, never a transcript. One or two lines, filled from the bottom (a one-line point sits on the lower bar). Break lines where they are most even, never ending a line on a short word (a, the, to, of) and never leaving one word alone. A point that will not fit in two lines is rewritten shorter or split into two points.
- **Subtitles** carry the literal speech: centred, no box, Onest Medium with a soft dark shadow (about 60% black, 3px down, soft) so they read on bright footage. White by default; `subtitle-yellow` when the requester prefers it. One line when it fits, two at most, broken evenly. Sizes: 44/56 in 16:9 (84px from the bottom), 60/76 in 9:16 (400px from the bottom, clear of the app buttons), 48/62 in 4:5 (96px from the bottom).
- They never share the frame with a lower third, and a highlight and a subtitle never overlap.

## Video review checks

On top of `brand` › `review-checklist.md`:

- The template's theme recolour is complete (no white text on Ice, no navy box lost on Navy).
- Every `slot-*` is filled or removed; no sample copy left.
- The Overlay twin matches its template.
- Pixels touch their element; none float. Moons show no centre and no flat cuts, and stay clear of text.
- Titles and logos are centred optically.
- In vertical, nothing important sits in the top 220px or bottom 400px.
- Highlights back up a point (no transcript); subtitles are the exact words, with no glitch, boil or box.
