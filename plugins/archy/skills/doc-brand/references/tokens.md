# DOC tokens

Read this when you need a colour, weight, tracking, spacing or radius value for a DOC piece. How they are used (grounds, themes, the lockup, the headline) is in `identity.md`.

`DOC - Brand` and `DOC - Ads` carry the same token set; `get_basic_info` lists it. **Everything on the canvas goes through a token.** When a piece needs a value no token covers, flag it and propose a token; do not type a hex or a hand number.

Hand values that stay px on purpose: font size, line-height and absolute `left` / `top`. DOC's `--text-*` / `--leading-*` tokens are the web scale (64 / 48 / 24…) and no ad headline sits on them.

---

## Colour

### Neutrals

| Token | Hex | Role |
|---|---|---|
| `--color-ink` | `#222222` | Text on light grounds; the Dark ground. There is no pure black on DOC; if pure black is ever needed it gets its own token |
| `--color-ink-soft` | `#3A3A3A` | One step lighter than ink: containers on the Dark ground (elevation by tone) |
| `--color-neutral-900 / 800 / 700 / 500 / 400 / 300 / 200` | `#111 / #222 / #444 / #666 / #AAA / #CCC / #EEE` | Muted text (500), hairlines on cream (200), rules (300) |
| `--color-white` | `#FFFFFF` | Rarely used; cream is the light |

### Cream (the light ground)

| Token | Hex |
|---|---|
| `--color-cream-100` | `#FDFCF5` |
| `--color-cream-200` | `#FAF9EE` |
| `--color-cream-300` | `#F8F6E8` |
| `--color-cream-400` | `#F6F4E1` |
| `--color-cream-500` | `#F3F1D9` |

The ramp is a warmth dial as much as a lightness one: the red minus blue difference roughly triples from 100 to 500. **`--color-cream-200` is the ad ground.** When a cream surface reads too yellow, the culprit is almost never the ground; look for the largest `cream-500` element and step it down.

### Red (the brand colour)

| Token | Hex |
|---|---|
| `--color-red-400` | `#FF0600` |
| `--color-red-500` | `#ED0606`, **the brand red** |
| `--color-red-600 / 700 / 800 / 900` | `#CC0000 / #990000 / #660000 / #330000` |

The brand red is `red-500`, not `#FF0000` and not `red-400`.

### Tracks

| Token | Hex | Track |
|---|---|---|
| `--color-track-foundations` | `#ED0606` (= red-500) | Foundations: free, 12 modules, the shared core |
| `--color-track-startup` | `#69228F` (= `--color-purple`) | Startup: paid, 11 modules, build it from scratch |
| `--color-track-acquisition` | `#00593E` (= `--color-green`) | Acquisition: paid, 13 modules, buy one that works |

Also in the set: `--color-purple-dark #5B1D7C`, `--color-purple-light #E8CDFF`, `--color-yellow #FBF900`.

### Overlays and tints

Paper has no reliable way to derive these on the canvas, so each one is its own token. Use them instead of writing an alpha hex or `color-mix()`.

| Token | Value | Use |
|---|---|---|
| `--color-cream-200-a10` | cream-200 at 10% | Card fill on a colour or Dark ground |
| `--color-cream-200-a15` | 15% | Incoming chat bubbles, portrait slots, thread hairline |
| `--color-cream-200-a20` | 20% | Rules and quote highlights on colour or Dark grounds |
| `--color-cream-200-a25` | 25% | Card borders, ticket dashes |
| `--color-cream-200-a30` | 30% | Portrait slot border |
| `--color-cream-200-a35` | 35% | Ghost card outline |
| `--color-cream-200-a45` | 45% | Illustration slot outline |
| `--color-cream-200-a55` | 55% | Illustration slot label |
| `--color-cream-500-a35` | cream-500 at 35% | Rule on a stat layout |
| `--color-red-500-a06 / a10 / a14 / a22` | red-500 at 6 / 10 / 14 / 22% | The same roles on the Light ground: card fill, bubbles and slots, highlight and hairline, card border |
| `--color-red-tint` | red-500 mixed ~35% with white, opaque | A pale block on a red or Light ground |
| `--color-purple-tint` | the Startup purple, same mix | Same, on Startup |
| `--color-green-tint` | the Acquisition green, same mix | Same, on Acquisition |

---

## Type

| Token | Value |
|---|---|
| `--font-sans` | Satoshi |
| `--font-weight-regular / medium / bold / black` | 400 / 500 / 700 / 900 |
| `--font-weight-light` | 300. Present in the set but **not used on DOC pieces** |
| `--tracking-display` | -0.016em. Headlines |
| `--tracking-heading` | -0.01em. Headlines and CTA labels |
| `--tracking-normal` | 0 |
| `--tracking-label` | 0.063em. Uppercase labels and eyebrows |

Web scale (`--text-*` / `--leading-*`): display 64/70, heading 48/58, lead 24/34, body-lg 20/31, body 18/27, label 16/24. Guideline artboards use it; ad type is sized to the piece (see the `doc-ad` skill).

Body copy carries no letter-spacing; only headlines and CTA labels take a tracking token.

---

## Spacing

`--spacing-1` 4 · `-2` 8 · `-3` 12 · `-4` 16 · `-5` 20 · `-6` 24 · `-8` 32 · `-10` 40 · `-12` 48 · `-16` 64 · `-24` 96 · `-32` 128.

Every gap goes through the scale. Above 32 the steps are coarse, so snapping can move things visibly: screenshot after. When two steps are equally close, break the tie by hierarchy (a gap inside a block stays smaller than the gap between blocks), not by rounding.

The CTA button's internal gap of 14 is part of the button spec and stays 14.

---

## Radius

| Token | Value | Use |
|---|---|---|
| `--radius-none` | 0 | Default. The web system is square-cornered |
| `--radius-tag` | 4px | Tags |
| `--radius-tail` | 8px | The tail corner of a chat bubble |
| `--radius-button` | 10px | The CTA button |
| `--radius-card` | 12px | Cards, the CTA bar, chat threads, portrait slots on ads |
| `--radius-bubble` | 28px | Chat bubble corners |
| `--radius-full` | 9999px | Pills, round notches, one-line bubbles |
