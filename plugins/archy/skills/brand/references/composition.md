# Archy composition rules

Read this when you are laying out a marketing piece (social post, Stories, OG card, event poster, ad): placing the mascot, drawing Rulers, building a logo lockup, sizing type and gaps, or adapting a layout across formats.

Token values (colours, grounds, radii, Ruler colours per ground) live in `tokens.md`. Slide layouts live in the `deck` skill (`layout-catalog.md`); marketing templates and their slots in `templates.md`. Pre-ship checks live in `review-checklist.md`. Paper MCP behaviour (rotation pivots, badge offsets, masks) lives in `paper-quirks.md`.

---

## Non-negotiables

These are not preferences to weigh. They are always true.

- **Rulers are always a SOLID colour. Never `opacity`, never an alpha colour, on any ground.** Translucent lines darken wherever they cross, and on a grid device the intersections are what the eye lands on. The colour per ground is in `tokens.md`. This supersedes every older "white at 0.3" instruction; convert old Rulers to solid when a piece is touched, and never copy the translucent version into new work.
- **The Archy wordmark on any white or light ground is `--color-royal-blue-500`.** Never navy, never black. On dark grounds it stays white.
- **A contour around the whole mascot is white, never tinted.** He only needs one when he would otherwise dissolve into the ground. A part that matches the ground gets its own tone-matched edge instead (see *The mascot*).
- **The mascot's antenna always points into the canvas.** When he peeks in from an edge, the top of his head leads in and the crop falls on his chin (orientation table under *The mascot*). An upright figure with a side crop, or an antenna hidden off the trim, reads as a sticker pasted on.
- **A crop never touches the eyes.** Both eyes stay whole and clear of the trim. The ears may be trimmed a little by a bleed.
- **No mint in event pieces.** It has an in-house precedent on the campaign pages (see *Devices from the website*), but it is not part of this system.

---

## Rulers

The hairline rules borrowed from the website (1px `#EEE` verticals inset from the trim plus full-bleed horizontals capping each band) are called **Rulers**. Use that name.

They are the preferred structuring device across every ground, not just light ones. **Reach for Rulers before reaching for a container**: information sitting directly on the surface, separated by a Ruler, beats the same information boxed in a card. Only box something when the box itself carries meaning.

At poster scale use **2px**; 1px vanishes on a phone. On every ground a Ruler is a solid colour (see `tokens.md`).

- **Content must never touch the column verticals, and there are two ways out.** The verticals sit at 96 and 1822, so anything that runs the full content width (96 → 1824) lands on them. Either **inset the content to the cell lane** (136 → 1784), which is the normal fix, or **drop the verticals** when the layout is too dense to give up that width (six cards across the column need every pixel; there the two verticals come off and the full-bleed horizontals stay). Inset first; removing them is the answer only when the content genuinely cannot afford the 80px.
- **Side verticals run the full height, trim to trim.** A vertical that stops short of the top or bottom edge reads as unfinished. In a grid, a photo may fill its cell flush to the Rulers (the photo is the cell); that is the one case where content meets a Ruler.
- **Rulers separate; they do not bracket.** In a stack of rows, put a Ruler *between* rows only, never above the first or below the last. A closing Ruler under the last row reads as a box drawn in hairlines, which defeats the point.
- **A row's title-to-body gap scales with the mass of the body; it is not one constant down the column.** An eight-line paragraph sits 22px under its title while a one-line placeholder beside it sits at 12. Setting both to the same value makes the heavy block look cramped under its title and the light one look detached. The gap *between* rows stays constant (48 in that case); only the internal one moves.
- **One Ruler per boundary.** If full-bleed Rulers already divide the artboard into bands, an inset Ruler inside one of those bands is noise. Pick the level the Ruler belongs to and use it there only.
- **Removing something from a band must not move the band.** Give the block a fixed height and `justify-content: center` so the full-bleed Rulers stay where they are. Otherwise every edit re-flows the whole grid.
- **A Ruler can carry the kicker.** Flanking the label with two Ruler segments turns a floating kicker into a masthead, and it is the fix when the top of a layout feels unanchored. Build it as a flex row, `[Ruler flex-grow:1] [label] [Ruler flex-grow:1]`, **not** as one full-width Ruler with the label knocked out on top of it: a Text node's `backgroundColor` does not paint in Paper, so the line runs straight through the words. If you want the knock-out version, the label has to sit in a Frame that carries the background.
- **The mascot may cross a Ruler; he is not a sticker.** His antenna running across a band Ruler where he peeks up from the bottom reads well. The sticker rule below does not apply to him.
- **A sticker may terminate a Ruler, but never sit across one.** Covering the *end* of a rule at the trim is fine: a badge landing in the top-right corner turns a symmetric header into `rule → label → sticker`, which reads as deliberate. What is wrong is a sticker dropped mid-span, hiding the middle of a line that then reappears on both sides.

---

## The mascot

**The mascot is named Archy**, the same as the brand: a robot with a rounded shell, sleepy eyes and a dark navy face plate, as a head or full body (head plus a blue capsule body with the Archy "A"). Refer to him as **he** (him, his). On the canvas he is always **Mascot** (layer and artboard names, labels).

### Where he lives

The masters are in the Brand file, page **Mascot**, left to right: `Mascot · Expressions` (full body, four faces), `Mascot · Heads` (head only), `Mascot · Poses` (exploration), `Mascot · Agents` (the five agents), `Mascot · Mono` (one-colour head, four faces), `Mascot · Mono Colour` (positive and reversed colourways), `Mascot · Construction` (seven parts and their colours), `Mascot · Grounds` (blue, dark and white, antenna rule and body edge applied), `Mascot · Light Blue Grounds` (Tint 100 and Tint 300 with their edges, plus the screen and print edge table), `Mascot · Placement` (the three bleeds, raised eyes) and `Mascot · Misuse` (antenna off the edge, upright side crop, crop through the eyes). **Copy him from there** rather than redrawing or re-deriving a rotation.

- **One canonical construction:** short antenna (24 units wide) and the wider shell. Full body `viewBox 0 0 670.54 644`, head only `0 0 670.54 444`, flattened (no `<g>`). Every Archy file now carries the master. The older long-antenna head is the superseded drawing; if it turns up (an old paste, an external file), replace the whole head with the master, match the old shell size so the layout does not move, then apply the antenna colour and the raised eyes.
- **Expressions:** `Neutral` (round eyes) is the default; `Joyful` (filled arcs) is a favourite and used a lot; `Happy` (outline arcs) and `Love` (hearts) by context. To change the expression, swap the whole SVG: rewriting only the eye nodes with `write_html` turns a `<circle>` into an empty rectangle.
- **The eyes are sized by the master.** Never transplant eyes from one drawing into another, and never scale or redraw them by hand: the eye-to-plate ratio is fixed by the asset, and a hand-fitted eye always comes out the wrong size.

### Placing him

- **Bleed direction follows the canvas orientation, not the source layout.** He bleeds off the *top* on vertical formats (Post, Stories) and off the *side* on landscape (OG, slides). What stays constant is that he peeks in and how much shows, not which edge.
- **Orientation: the antenna points into the canvas.** The antenna is the top of his head; the crop falls on his chin.

  | Bleeds off | Rotation of the upright master (antenna up) | Antenna points |
  |---|---|---|
  | Top (Post, Stories) | **180°**, upside down | down, into the frame |
  | Right edge (OG, slides) | **−90°** | left, into the frame |
  | Left edge | **+90°** | right, into the frame |
  | Bottom (thumbnail-scale pieces) | **0°**, upright | up, into the frame |

  In the templates the head is already rotated for its bleed, so a copy from a template works as is (the top bleed is `691×461 @ 195, -152`). From the Brand master, rotate per the table. Either way, check where the antenna lands; if it is off the canvas, he is backwards.
- **"Raise" and "lower" him in his own axis, not the canvas's** (antenna = up, chin = down). Raise = rise out of the edge, show more; lower = sink into the edge, show less. On the upside-down top bleed, lowering him moves him *up* the canvas. When an instruction is ambiguous, restate it as "show more / show less of him" before moving anything.
- **Show about two thirds of him on every edge** (measured: 65% on a top bleed, 64% off the right edge, 62% from the bottom). A peek reads as curiosity; three quarters of him reads as a second headline.
- **The crop never touches the eyes.** Both eyes stay whole and clear of the trim; the ears may be trimmed a little.
- **In a bleed his eyes move up, toward the antenna** (`translate: 0 -50px` in viewBox units on both eye nodes, about 17% of the face plate height). With centred eyes and two thirds visible, the crop would land on the eyes; raised, they clear it on every edge. It is the one place the eyes leave centre.
- **The empty column beside a left-aligned headline is where he goes.** A 3-line headline set left leaves a tall gap on the right; he fills it, bleeding off the right edge rotated −90° (antenna pointing left), at the headline's own height. Beside the headline he balances it; on a photo he competes with it.
- **He may cross a Ruler.** He is not a sticker.
- **When rotated he does not render where `left`/`top` say.** Position by screenshot and nudge (see `paper-quirks.md`).

### Colour against the ground

- **Antenna colour follows the ground.** Light ground: `--color-blue-tint-800`. Blue or dark ground: `--color-blue-tint-300`, because a dark antenna sinks into both. It is a solid token fill on a node named `Antenna`, so switching it is one `update_styles` on that node.
- **Tone-matched edge: when one part matches the ground, only that part gets a barely-there darker edge** in its own hue. A contour around the whole mascot is still white only; this is a per-part edge. Values are asset hexes (no token sits that close to the part):

  | Ground | Part that sinks | Edge, screen | Edge, print (CMYK) |
  |---|---|---|---|
  | Royal blue gradient | body capsule | `#0A30D6` | `#0726B0` |
  | Any tinted pale ground: `--color-light-foreground`, `--color-blue-tint-25`, `-50`, `-100` (close to the shell) | shell | `#C3DDF3` | `#A9C8E6` |
  | `--color-blue-tint-300` (close to the ears) | both ears | `#4DA8F0` | `#3690DB` |

  **5 units** wide on the 670-wide viewBox (about 1.5px at 200px display): it must be felt, not seen; 10 units in stronger blues was far too heavy. **For print, use the darker column** before running `archy-design:print-pdf`, because an edge this subtle disappears on press, where blues already print duller; the width stays 5 units. The ears touch the viewBox edge, so the SVG and its wrapper need `overflow: visible` or half the ear stroke is clipped.
- **Pure white ground: no edge**, the navy face plate carries him. **Any tinted pale ground** (off-white, `--color-light-foreground`, the pale blue tints, or a gradient between them): the shell gets its `#C3DDF3` edge by default, because his near-white shell sinks into it and the head reads as a floating plate. Check it on the screenshot either way.

### Agents

Archy has **five agents**: the full-body mascot plus the objects of each job, in the brand greens (the `#00E08F` family). This is the one sanctioned use of mint outside the campaign pages; do not spread it to layouts.

| Agent | Face | Objects |
|---|---|---|
| Insight | Neutral | chart report (left), document (right) |
| Scribe | Neutral | pencil (left), clipboard (right) |
| Connect | Happy | phone (left), chat bubble (right) |
| Verify | Joyful | magnifier (left), check seal (right) |
| Revenue | Happy | card terminal (left), card and coin (right) |

Each is built as a `Props · <Agent>` SVG layered over a duplicate of the base, same viewBox, `overflow: visible`. The one-line job descriptions on the sheet were inferred from the objects and are not yet confirmed.

### Mono

**Mono** is Archy in one colour, for icons, favicons, app tiles, stamps, embroidery and any surface where gradients cannot go. All four expressions exist. It is its own drawing (antenna 26 wide); do not force it to the full-colour construction.

- **Positive, on light grounds:** two paths, `Contour` (shell ring, ears, antenna) and `Face` (the plate, with the eyes as `fill-rule: evenodd` holes), both `--color-blue-tint-800` by default; `--color-royal-blue-500` when the piece should carry the brand colour; pure black only for one-colour print.
- **Reverse, on royal or navy:** never the positive recoloured white (that paints the face plate white and leaves dark eyes, a photographic negative). The reverse is its own shape: one white path, `evenodd`, built as outer silhouette + face plate as a hole + eyes, so the shell is solid white, the face plate is the ground, and the eyes are white.
- **Open:** minimum size and clear space.

### Poses (exploration)

Motion without redrawing: the parts stay identical, only their angle and offset change. `Mascot · Poses` has Tilt (head +7°, body −3°), Listen (Neutral, head +10°, dropped 8), Look (Neutral, eyes slid 38 toward the content, head −4°, body +2°), Laugh (Joyful, head −9° and up 14, body +4°), Jump (Joyful, head up 40, body up 16), Crush (Love, head +12°, antenna flicked −18°, body −4°).

Built with CSS `rotate` + `translate` on each SVG child, no path rewritten. Paper rotates SVG children about the viewBox origin, so a rotation θ about a pivot c is `rotate: θ` plus `translate: c − R(θ)·c (+ offset)`. Pivots on the 670 × 644 viewBox: head (335.27, 244), body (335.27, 553.6), antenna base (335.27, 53.41). Keep head angles within about ±12° and body within ±4°: past that the neck gap closes on one side and he reads as broken rather than lively.

---

## Logo lockups

**Match the partner marks optically, not numerically.** The Archy wordmark ships at 210 × 81 and the Hinman mark at 304 × 100; dropped in as-is, Archy reads noticeably smaller. Scale Archy to roughly **250 × 97** so the two share a cap height. Check every lockup this way; the imported sizes are never the right relationship.

**Do not take the wordmark from `index.html`.** The inline SVG there (viewBox `0 0 500 195.5`) is missing the counter of the "A", so it renders as "∩rchy". The correct mark is the one already on the canvas in the Master - Events file: 5 paths in a `<g transform="translate(0 21.752)">`, viewBox `0 5 252 98`, ink 252 × 98. Copy it from there, or from the Decks cover.

**The wordmark's native ink is 252 × 98, which is exactly 18:7, so its integer scales are `18k × 7k`.** This matters whenever the mark sits inside auto-layout: in a 420 × 220 flex column, a 260 × 101 mark centred its content at y 41.5 and put both children on sub-pixel positions, while 252 × 98 (k = 14) lands on 43. Pick an `18k × 7k` pair before reaching for a hand-tuned height.

**Inside a component the wordmark follows the ground it sits on, not the artboard's.** A royal-blue block on a dark-ground layout carries a white mark. The rule that turns it royal blue is about *white and light* grounds only.

**The lockup always spans the full content width.** Archy sits at the left edge of the column and the partner mark at the right; they anchor the two ends. It is not a compact "logo lockup" that scales down for smaller formats: shrinking it to a narrow block huddles the two marks in the middle and reads as an afterthought. On the OG it still runs the whole column, just shorter.

---

## Scale and restraint

- **Type runs bigger than feels safe.** Every draft has come back with "make it bigger"; one headline was corrected upward four times, 72 → 88 → 96 → 100. If a layout is clean, that is exactly the licence to push the typography; a clean layout with timid type reads as empty, not minimal. **Start a 1080 Post headline at 100px minimum**, 180px+ when it is the hero, and only come down if it breaks.
- **Leading tightens as the format tightens.** Post headlines run **1.03–1.10×** (100/103, 109/118, 115/126). OG headlines run **~0.99×**, set solid (77/76, 80/86, 184/183), because the format has no room to spend on leading and the lines still read as one block. A **single-line label or value never wraps, so it has no neighbour to collide with**: set those solid or slightly under (24/24, 36/34). The "line-height is never smaller than font-size" rule (see `tokens.md`) exists to protect *wrapping body copy*; it is not a floor for headlines or for one-line values.
- **Gaps run tighter than feels safe.** This has been corrected repeatedly downward (87 → 61 → 53 on one light layout). Outer gaps above ~120px read as a hole. If a piece looks empty, the fix is bigger type, not more air.
- **Radii run smaller than feels safe.** The tokens cap at 12px (see `tokens.md`). Scaling them "for poster size" produces the over-rounded look that keeps getting flagged. Use the token value directly. The one exception is the event posters' viewing-distance correction, below.
- **Banned, because they read as generic AI output:** an outlined pill with a word inside it, an element floating with no relationship to anything around it, and a decorative accent colour applied because it was available. If an element cannot justify its position against something else on the page, remove it.

---

## Devices from the website

The Webflow home is **entirely light**: white, `#F7F7F7` and `#EEE` hairlines, royal blue as the only chroma, no dark sections anywhere. The event posters are its inverse, not a subset of it, so a light poster is the *more* brand-faithful option, not the risky one. Four devices from the site, all proven on a poster:

| Device | Construction |
|---|---|
| **Hairline frame** | 1px `#EEE` verticals inset from the gutter running full height, plus full-bleed horizontals capping each band. Reads as an engineering drawing. At poster scale use **2px**; 1px vanishes on a phone. |
| **Two-tone headline** | Onest 600, `-0.02em`, split mid-sentence: first half `--color-light-text`, second half `--color-neutral`. Paper cannot colour part of a text node, so it is **two stacked text nodes in a flex column with gap 0**. |
| **Composite tag** | A bordered white square plate sitting *flush* inside a `--color-blue-tint-50` bar; the bar has **no left padding**. Give the plate `border-radius: 24px 0 0 24px` so it nests instead of leaving a notch, and keep the plate white on every variant; recolouring it to match an inverted bar makes it read as a hole. |
| **Status pill** | `--radius-pill`, a `--color-royal-blue-500` dot + uppercase tracked label on `--color-blue-tint-100`. |
| **Primary button** | The site's `.button_v2`: `--color-royal-blue-500` fill, white Inter Medium, `--radius-button` (8px) with a trailing arrow. On a 1080 poster or ad: 30/36 type, radius 16, padding 22 / 32, gap 16, Hugeicons arrow at 28px, stroke 2. Not a pill. Inverted (white fill, royal label) on a royal blue ground. |

**What the site does not have:** no blobs, meshes, glows, drop shadows, rotations or blend modes. Decoration is hairlines, `1px #EEE` rounded rectangles, and *inset* shadows used as a letterpress cue. Do not introduce those effects; they read as off-brand.

**The rotation half of that ban is scoped to decoration.** Rotation is legal where the angle is the content rather than an effect: the event family already rotates (the booth badge at 6°, the mascot at 90° off a side edge), and a scrapbook slide may tilt polaroid cards between −5° and +5° because it *is* a scrapbook. **A tilt on a chart, a Ruler, a grid cell or a photo that is not pretending to be a print is still wrong.**

**That list is the whole ban, and gradients are not on it.** Both artboard grounds are `linear-gradient`s, and the `BK Fade` is a gradient the composition rules call mandatory. Paper's own house guide warns against "excessive gradients"; that is Paper's advice, not Archy's. The Decks artboards are flat-filled because the source deck is flat-filled, which is an observation about the source, not a constraint on new work. A gradient ground on a slide is open to explore; what stays out is the effects list above.

**Radii for posters.** Site radii are only `.5 / .75 / 1rem`. A 1080px poster is viewed small, so scale them to roughly **20 / 30 / 40px**. This is a correction for viewing distance, and the *only* place the 12px cap is exceeded.

**Mint** appears nowhere on the home page, but it does live on Archy's own campaign/event pages (`airpods`, `tesla`, `ignite`, FutureProof), including 2px mint rules. That is precedent, not permission: the non-negotiable stands, no mint in event pieces.

---

## Social layouts and the label/value pattern

There is no single Post layout. Campaigns arrive as different designs: the mascot-hero families (1–4) put logos at the bottom; the speaker-invite layout (5) puts them at the top, adds a photographic ground, a circular speaker portrait and a footer note. **Expect a new layout with each paste and read it on its own terms; only the token system, the safe areas and the label/value pattern below carry across.**

### The label/value pattern

Any "LABEL over VALUE" stack (location, date, speaker) uses it:

| | Size / leading | Weight | Colour |
|---|---|---|---|
| Label (uppercase, `0.02em`) | 32 / 40 | Bold | `--color-blue-tint-300` |
| Primary value | 48 / 56 | SemiBold | `--color-white` |
| Secondary value | 36 / 44 | Regular | `--color-blue-tint-100` |

### Spacing scale: 12 / 20 / 40 / 56

Inside a text block 12; label to a photo or any non-text block 20; between detail blocks 40; between the outer content blocks 56.

- **A gap is only as big as it looks.** 4px between two text lines reads as ~12px, because the label's line-height (40 over 32) and the value's (56 over 48) each donate ~4px of leading. A portrait, a circle or a rule donates nothing, so the same 4px reads as glued-on. Match the *optical* gap, never the number: that is why label→text is 12 and label→portrait is 20.
- **The scale is a budget, not a preference.** The safe area is 1140px tall and the ink (type, portrait, logos, footer) takes ~830 of it, so every gap in the artboard is competing for ~310px. Widening an inner gap silently narrows the outer ones; push the inner too far and the levels collapse into each other. Change one gap and re-derive the rest, keeping each level clearly larger than the one inside it.

### Photos

- **A photo can leave the column.** Full-bleed is the strongest thing it can do on a light layout: run it 0 → 1080 with square corners, outside the content column entirely, so it breaks the grid the Rulers establish. Sitting it **below all the content** as a base band that bleeds off the bottom reads better than parking it in the middle, where it cuts the piece in half. A framed photo inside the column (mat, border, rounded corners) was tried and rejected: the frame reads as fussy at poster scale.
- **Rings over a photo derive from `--color-white` at low opacity**, not from a blue tint: a 4px portrait ring is white at 0.45, because it has to let the photo read through. Pasted equivalents (`#7194FE`, `#5391F9`) decode to exactly that. **This does not extend to lines on a flat or gradient ground**: a footer divider or any Ruler is a solid colour, since translucent lines darken wherever they cross.

---

## Event three-format family (Post / Stories / OG)

Every campaign ships as **`N.1` / `N.2` / `N.3`**, all derived from the Post. Duplicate and adapt, never rebuild, so the SVG assets (logos, badge ribbon, Bulls mark, mascot) carry over intact.

| | Size | Safe area |
|---|---|---|
| `N.1 … Post` | 1080 × 1350 | x 105–975, y 105–1245 |
| `N.2 … Stories` | 1080 × 1920 | x 105–975, **y 250–1670**; Instagram's UI covers the top and bottom 250px |
| `N.3 … OG / Link preview` | 1200 × 630 | ~60–72px margins |

**Rulers rotate with the format.** Horizontal Rulers separating stacked rows on a Post become **vertical dividers** between columns on the OG, where the same rows sit side by side. The device survives the re-layout; its orientation does not.

**Check how the `Content` frame is positioned before adapting it.** Several artboards ended up with `Content` at `position: relative` inside an artboard that is itself `display: flex`. Setting `top` on it then does nothing: the artboard's own alignment decides where it lands, and the block silently ends up hundreds of pixels off. Set `position: absolute` with explicit `left`/`top` first, then place it.

**Adapting across the three formats.**
- **Stories only ever needs repositioning.** Keep every block size and gap identical to the Post and let the extra height become margin, then move the bleed art down by the same delta the content moved so its relationship to the content is preserved.
- **The OG needs re-layout.** The Post's column will not fit in 630px, so blocks that stack vertically pair up into rows (location beside date), and anything that survives being cut gets cut. A label above a portrait is the first to go: at ~500px wide the portrait and the name explain themselves.

**The OG headline is not small.** It runs **72–104px** on the 1200 × 630 canvas, around 80 as a starting point, higher when the column is wide and the line count is low. Sizing it at 48–56 "because the format is small" is the mistake that keeps getting corrected: the card is read at a glance, so the headline has to survive being the only thing anyone registers.

**Count the labels when you budget an OG.** Every label adds its line-height *plus* its gap, ~42px at OG scale, which is most of a margin. Sizing from the values alone and forgetting the labels overshoots the artboard.

**1200 × 630 is the Open Graph standard**: the preview card when a link is shared on Facebook, LinkedIn, X, Slack, Discord, WhatsApp, plus feed link ads. It renders around 500px wide, so legibility beats completeness. Drop the secondary hook (the Bulls tickets bar) and the venue line; keep title, city, dates, booth badge and the logos.

**Structure every artboard the same way:** one `Content` frame with real auto-layout (flex column + gap) holding the stacked blocks. Only bleed and overlay layers stay absolute: background art, photo band, scrim, `BK Fade`, the mascot, the badge. Layer order should read top-to-bottom like the design does.

**Spacing:** the gap *between* blocks must exceed the gap *within* a block. Getting this backwards is the most common reason a layout feels cramped.

**Two anchors fix the vertical rhythm on the Post; the block gap absorbs the rest.** The mascot bleed and the logos lockup are constants: the mascot's visible edge lands at y309 and the content's bottom at y≈1241, just inside the safe area. So place the `Content` frame ~40px below the mascot, end it at 1241, and *derive* the gap: `(1241 − top − Σ block heights) / (blocks − 1)`. A campaign with fewer blocks gets a bigger gap, not a hole at one end. Family 2 has five blocks and lands on 40; family 4 has four and lands on 96. Never solve the difference by parking the content at one end and leaving a gap at the other.

---

## Composition rules

1. **Bleed direction follows the canvas orientation, not the source layout.** The mascot bleeds off the *top* on vertical formats (Post, Stories: `691×461 @ 195, -152`, a 33% crop) and rotates 90° to bleed off the *side* on landscape (OG). What stays constant is that he peeks in and how much shows, not which edge.

2. **Make room for a sticker; do not squeeze it in.** A badge dropped into whatever gap is left will end up crossing a Ruler or sitting on the headline, and covering a letter of the hero line ("day" reading as "dau") is a legibility failure, not a depth cue. The fix is upstream: re-anchor the block above it (align the headline to the top of its band instead of centring it) so a real hole opens, then place the sticker in it. It may overlap the mascot or run off the trim; it may not overlap type or a Ruler.

3. **The booth badge is a decorative sticker; it may break the safe area.** The safe area protects information; the badge repeats a fact that survives a clipped edge. Letting it push out means it overlaps the mascot, which reads better than floating in a gap. Do not police the safe area on decorative elements.

   **It should attach to something, not float in open field.** Every time it has been placed fully inside an empty area it has been moved: to a corner bleeding off the trim, or onto the seam where two fields meet. A sticker that clears everything by a comfortable margin reads as *placed*; one that breaks an edge reads as *stuck on*. Give it something to overlap. (The badge's rendered position is offset from `left`/`top` by its rotation; see `paper-quirks.md`.)

4. **Centre against the dominant visual mass**, not against a floating accent.

5. **Reframing a photo: scale the subject up before trying to move it.** If a subject sits at the edge of its source frame you cannot reposition it into the middle; enlarge the image rect instead (`backgroundSize: cover`, so no distortion) until the subject dominates. Social art is viewed on a phone: a distant subject disappears, a large one survives.

6. **Fading background art:** a `BK Fade` rectangle above the art and below everything else, `linear-gradient(180deg, transparent 0%, var(--color-<artboard background>) N%)`. The gradient must reach full opacity **before** the art ends, or a faint ghost survives. `transparent → token` interpolates cleanly in Chromium (no grey midpoint, colour still from a token). Match the end colour to that artboard's own background token (`--color-royal-blue-500` on the blue families, `--color-dark-background` on the navy ones; see the ground table in `tokens.md`).

   **Vector background art always gets one; it is not optional.** Wherever the art's own bottom edge falls inside the canvas, it renders as a hard horizontal line with flat ground beneath it, and it reads as a mistake. The check is mechanical: if `art top + art height < artboard height`, that artboard needs a `BK Fade`. Only art that is clipped by the trim can go without. Add it at the same time as the art, not as a later fix; it has been forgotten and caught in review more than once.

   **This is not a Stories-only device.** Any format where the vector skyline competes with the content wants one. On the Post it starts at the photo edge and runs to the bottom, so the logos land on clean background while a hint of skyline survives behind the title. Reach for the fade before reaching for lower opacity: dimming the art flattens it everywhere, the fade keeps it strong where it reads as texture and removes it where it fights type.

7. **The gap between the photo band and the content is the same as the content's own block gap**: 64px on Stories. It is a family constant, so check a new Stories artboard against the existing ones rather than eyeballing it; a bigger gap reads as a mistake even when the block below is short.
