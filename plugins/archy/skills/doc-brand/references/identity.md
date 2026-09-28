# DOC identity

Read this for the lockup, colourways, grounds and themes, track coding, type and the two-weight headline. Token values are in `tokens.md`. Ad layouts, sizes per format and the CTA copy per theme live in the `doc-ad` skill.

The guideline artboards in `DOC - Brand` (pages Brand, Logo, Color, Typography, Elements, numbered `01` to `18`) describe the **web** system and note where ads extend it (grounds, lockup colourways, track grounds, card radius, the weight floor). Those extensions are marked **On ads** below: the ad rule applies to ads, the web rule everywhere else. If a guideline artboard and this file ever disagree, flag it.

---

## The lockup

- **Outlined artwork, 26 paths, viewBox `0 0 132 48`.** A square symbol with a knocked-out bar on the left, the three-line wordmark `Dental / Ownership / Collective` on the right. Copy it from `DOC - Brand` › Logo (`Asset · Lockup`, `Asset · Lockup Red`, `Asset · Symbol`) or from any ad artboard. Never set the wordmark live in Satoshi: it is close, and wrong.
- **The bar is a hole, not a shape.** The ground shows through it, so the lockup only works on a flat ground.
- **Scale on its own 11 : 4 grid.** The ink is exactly 11 : 4, so sizes are `11k × 4k`: 132 × 48 (k 12), 220 × 80 (k 20), 275 × 100 (k 25), 330 × 120 (k 30). Pick the integer step before reaching for a hand size. When a lockup is resized, set width and height on **both** the wrapper Frame and the `SVG` node (a clipped wrapper hides an unresized SVG), and verify with `get_node_info`.
- **Clear space:** the wordmark's cap height, a quarter of the lockup's height, on all four sides.
- **Minimum size:** the full lockup at 48px tall. Below that, use the symbol alone (down to 24px: favicons, avatars, app icons). Never squash the lockup into a square.

### Colourways

| Guideline (web) | On ads |
|---|---|
| Two only, the same lockup inverted: **cream on red, red on cream** | Also **cream (`--color-cream-500`) on the track grounds and on the Dark ground**, and **ink with a red square** on the Light ground (the square is the first path; the wordmark paths are `--color-ink`) |
| Never on purple, green, yellow, a mid-tone grey or a photograph | Never on yellow, a mid-tone grey or a photograph without a scrim; purple and green only as a full flat ground, never recolouring the lockup itself |

Recolouring the lockup is `update_styles` with `fill` on its path nodes. There is no outlined version and no other single-colour version.

---

## Grounds and themes

**Guideline (web):** every surface is one of six grounds, three creams (100 / 200 / 300) and three reds (500 / 600 / 900), alternating so no two adjacent bands share a value. On light grounds: heading ink, body neutral-500, eyebrow red-700, hairline neutral-200. On red grounds: all text cream-500, hairlines cream at low opacity.

**On ads, five themes.** Each ad layout exists in all five; the artboard name carries the theme (`<Layout> · <Theme> · <W×H>`).

| Theme | Ground | Type | Where the red goes |
|---|---|---|---|
| **Foundations** | `--color-red-500` (= track-foundations) | cream | It is the ground |
| **Startup** | `--color-track-startup` | cream | Nowhere; the accent is the track colour |
| **Acquisition** | `--color-track-acquisition` | cream | Nowhere; the accent is the track colour |
| **Dark** | `--color-ink` | cream | **Fills only**: a button, a key bar. Never red text or red hairline icons on Dark: they lose contrast. Containers on Dark are `--color-ink-soft` |
| **Light** | `--color-cream-200` | ink | As the **container**: the CTA bar, a card, the footer band is red with cream content |

The general rule behind it: **on a track colour the containers are cream and the accent is the track; on a neutral ground (ink or cream) the red comes in as the container itself.** A piece recolours from its ground token, so keep every accent tied to that token.

---

## Track coding

Three tracks, three colours: Foundations red, Startup purple, Acquisition green. The code is the same everywhere it appears: card border, tag fill, module count, track name, curriculum kicker.

- **Guideline (web):** the code is carried by those small elements and is never a section ground. Purple and green never fill a whole band.
- **On ads:** the track colour may be the whole ground (the Startup and Acquisition themes, the Track Colorway layout). It is still never mixed with another track in one piece.

---

## Type

**Satoshi, one family.** No serif, no second face, no display cut: the voice comes out of weight and size.

- **Regular 400 is the lightest weight on DOC pieces.** Light 300 is in the font and the token set but is not used. Regular is wider than Light, so re-check every line break after a weight change.
- Web scale: display sets in Regular, everything else in Medium, Bold for emphasis and labels.
- Uppercase labels and eyebrows: Bold, `--tracking-label` (0.063em).
- Italic exists and renders (for example, a part of speech in a dictionary entry).

### The two-weight headline

DOC's one typographic device: a headline that changes weight mid-sentence, **Regular setup, Bold claim**, so the claim is louder than the setup.

- **Paper cannot hold two weights in one text node** (a `<b>`, `<strong>` or weighted `<span>` is silently flattened). The device is **two stacked text nodes**, `Regular` then `Bold`.
- **So the weight change must land on a line end.** Re-break the copy so the Bold half starts a line; use `\n` with `set_text_content` and `white-space: pre`. Never split a sentence twice.
- The one exception: when the change falls mid-line and that line does not wrap, a flex row of two `width: max-content` nodes on the baseline works.
- **Colour:** on the web and on ads the split is **weight only**, both halves the same colour. A colour step (setup `--color-neutral-500`, claim `--color-ink`) belongs to organic social posts only.
- **The gap between the two halves is grammatical and follows the type size:**
  - two separate statements (setup, then payoff): about **0.25 to 0.3 ×** the font size, so the change reads as a beat;
  - one sentence broken across the weights: about **0.12 to 0.16 ×**, so the gap gets out of the way;
  - a list of parallel lines where the weight marks the last item: close to **0**, with the air moved into the leading.
  Snap the result to the nearest `--spacing-*` step and check it on the screenshot.
- **Leading is a judgement.** Two short display lines alone in open space want air (about 1.05 to 1.13 ×); a wall of four or more lines can go solid. Sub-solid is earned by mass, not by size.
- **Tracking is a token picked by eye:** `--tracking-display` or `--tracking-heading`. There is no rule for which; both are in the system. Do not normalise them across a file.

---

## Elements

| Element | Spec |
|---|---|
| **Eyebrow** | Bold uppercase, `--tracking-label`. `--color-red-700` on cream, `--color-cream-500` on red |
| **Tag** | Bold uppercase, `--radius-tag`, padding 4 / 8, fill the track colour, text `--color-cream-100` |
| **Hairline** | `--color-neutral-200` on cream (1px on web, 2px on artboards). Separates rows; never above the first or below the last |
| **Track card** | The only container on the web: cream-100, a border in the track colour, square corners, padding 40, gap 40. **On ads** cards take `--radius-card` |
| **Footer** | Lockup at one end, meta at the other, a hairline above when there is a meta block. The same pattern closes a web page, a slide and a post |
| **CTA button** | 336 × 79, `--radius-button`, gap 14. Label 30 / 36 Bold, `--tracking-heading`, arrow 28 × 18 (stroke 2.4). On red: fill red-500, label and arrow cream-200. On cream: inverted. On Dark: fill red-500, label and arrow cream-100. **The button never scales with the format**: it is a tap target, identical on 1:1, 4:5 and 9:16 |

Icons: DOC has no defined icon library yet. When an icon is unavoidable, use Hugeicons Stroke Rounded (the `archy-design:hugeicons` skill) with a DOC token colour, and say it is provisional.
