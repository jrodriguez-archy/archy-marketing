# Archy tokens and design system

Read this when you need a colour, type, icon, radius or Ruler value, when you need to know which artboard ground to use, or when you need to find the Paper file a piece of work lives in.

For how those tokens are composed on a canvas (Rulers, the mascot, lockups, layout families), see `composition.md`. For Paper MCP behaviour that affects how tokens land, see `paper-quirks.md`.

---

## Where things live

| | Where | Contents |
|---|---|---|
| **Brand** (Paper) | `app.paper.design/file/01M1EY5TFVT7MBV4DRBZXZRR9V` | 95 design tokens. Pages: **Styleguide** (color, themes, type, spacing, layout, components), **Brand Guidelines** (logo, iconography), **Icons** (164 Hugeicons), **Textures** (the pixel grain: Pixel Gradients, the nine dithered backgrounds, and Pixel Effects on photos; generated with the `archy-design:pixel` skill) |
| **Master - Events** (Paper) | `app.paper.design/file/01M1F9VXX1S3JJETTVWG2H2PCD` | Page **Templates**: event campaign artboards |
| **Ads** (Paper) | `app.paper.design/file/01M33E66BD6FJNP4BPE88V90X0` | Page 1: `Claim Stack` Post/Stories/OG. Page 2: `Platform · One-pager 1500×1942` (Letter proportion), rebuilt from a raster reference that sits beside it, and `Platform · Post 1080×1080` derived from it |
| **Master - Decks** (Paper) | `app.paper.design/file/01M1HZF1EW0RX9H3YSMJ3GAMK7` | Slide template library, 1920 × 1080. **One page per content category**: Frames · Numbers · Charts · Lists · Comparisons · Proof · Showcase. 55 layouts, all with export specs (see `templates.md`) |
| **Various Collateral** (Paper) | `app.paper.design/file/01M37ZJ6ECM7XJ5TG5W2Z2YR4N` | Page `Chrome - Portal Manager`: Chrome Web Store listing images for the Portal Manager extension, plus the product frames they are built from |

The export tooling (Slides export to `.pptx`, Figma export) and the source material it depends on ship with this plugin under the relevant skills; they are not listed here.

Archived Paper files disappear from `list_files` and cannot be reached. Unarchive a file before asking for work on it.

The source of truth for tokens is the live website's stylesheet, mirrored as Paper tokens in every Archy file (`get_basic_info` lists them). If a token here and a Paper file disagree, flag it to Marketing & Design rather than picking one.

---

## The token-only rule

Everything on a canvas goes through a token: `var(--color-…)`, never a hex.

The only sanctioned hexes are computed tints that Paper cannot express as a token (Paper drops `color-mix()`, see `paper-quirks.md`). When you use one, note which tokens it derives from. The one in current use is `#2A5DF6` (see *Ruler colours* below).

---

## Type

- **Marketing system:** Onest (headings) + Inter (body).
- The site uses the **`_v2`** class set (h1 = 60px/600). The older `_v1` classes belong to other pages.
- Freigeist XCon ships with the website's font files but the site never uses it. Do not use it.

### Product UI is Open Sans, always

**The Archy product UI is set in Open Sans, always.** Onest + Inter is the *marketing* system. Whenever an artboard reproduces the app itself (a screen, a popup, the Chrome extension, a mockup inside a browser frame), every text node stays Open Sans (`OpenSans` / `OpenSans-SemiBold`), even when it sits inside a marketing piece. Never "correct" product UI toward Inter.

### Line-height

**Rule:** line-height is never smaller than font-size. Text below 12px only in dense UI, never in marketing art.

**The one exception is display type.** A headline at 150px+ is set solid: leading equal to the font size, or a hair under it (184/183 on the 1080 Post). That is normal typographic practice at that scale, and it is what keeps two huge lines reading as one block. The rule holds for everything else.

The rule exists to protect *wrapping body copy*. A single-line label or value never wraps, so it can also be set solid or slightly under (24/24, 36/34). See *Scale and restraint* in `composition.md` for headline leading per format.

---

## Core palette

| Token | Hex | Role |
|---|---|---|
| Royal Blue 500 (`--color-royal-blue-500`) | `#013DF5` | Accent |
| Primary Blue 600 (`--color-primary-blue-600`) | `#0000C9` | |
| Blue Tint 800 (`--color-blue-tint-800`) | `#00004E` | Dark ground |
| Blue Tint 100 / 200 / 300 | | Light text on blue |
| White (`--color-white`) | | |

---

## Artboard grounds

Two grounds:

| Ground | Gradient |
|---|---|
| **Blue** | `linear-gradient(180deg, var(--color-primary-blue-600) 0%, var(--color-royal-blue-500) 55%)` |
| **Dark** | `linear-gradient(180deg, var(--color-dark-foreground) 0%, var(--color-dark-background) 55%)` |

Which one a campaign uses is a **design decision carried in the paste, not a default.** Decode the pasted gradient before replacing it (a raw `oklab()` gradient is unreadable by eye; convert the stops to hex first) and map it to whichever pair it is closer to.

Switching grounds is not a free swap. Three things invert with it:

| | Blue ground | Dark ground |
|---|---|---|
| Booth badge | `--color-blue-tint-800`, white text | `--color-royal-blue-500`, white text |
| `BK Fade` end stop | `--color-royal-blue-500` | `--color-dark-background` |
| Label pill | `--color-white` + `--color-primary-blue-600` text | unchanged |

The badge is the trap: leave it navy on a dark ground and it disappears into the background entirely.

---

## Wordmark colour

- **On any white or light ground the Archy wordmark is `--color-royal-blue-500`.** Never navy, never black.
- On dark grounds it stays white.
- Inside a component, the wordmark follows the ground it sits on, not the artboard's (a royal-blue block on a dark artboard carries a white mark).

Wordmark geometry and lockup rules are in `composition.md`.

---

## Icons

**Hugeicons Stroke Rounded**:

| Property | Value |
|---|---|
| Grid | 24 × 24 |
| `stroke-width` | 1.5 |
| Caps and joins | round |
| Colour | `currentColor` in shipped code; on the Paper canvas set an explicit token (see `paper-quirks.md`) |

The live site still carries Phosphor, Font Awesome and loose 16/20px grids as drift. Replace them as surfaces are touched.

---

## Radius tokens

| Token | Value |
|---|---|
| `--radius-card` | 12px |
| `--radius-large` | 12px |
| `--radius-button` | 8px |
| `--radius-pill` | 999px (Status pill) |

The tokens cap at 12px. Use the token value directly; scaling radii "for poster size" produces the over-rounded look that keeps getting flagged.

**Settled: the set does not need a radius above 12.** 12px is correct wherever the piece is read at or near its actual pixel size, which is every slide, every web surface and the OG card. The event posters' ~20 / 30 / 40 is not a bigger token; it is a correction for being viewed at a fraction of their size on a phone. It is a property of the format and stays documented with the event templates (see `composition.md`). Do not add `--radius-xlarge`: it would force every future surface to choose between two right answers. If a surface feels under-rounded at 12, check how it will actually be viewed before reaching for a number.

The site's own radii are only `.5 / .75 / 1rem`.

---

## Ruler colours per ground

**Rulers are always a SOLID colour. Never `opacity`, never an alpha colour, on any ground.** A translucent line paints twice where two Rulers cross, so every intersection shows as a darker knot, and on a grid device the intersections are exactly what the eye lands on. Pick a solid colour one subtle step off the ground instead:

| Ground | Ruler colour (solid) |
|---|---|
| White / light gradient | `--color-light-border` (#EEE) on pure white; `--color-blue-tint-200` on a blue-tinted light gradient |
| Royal blue (blue gradient, `--color-primary-blue-600` → `--color-royal-blue-500`) | `#2A5DF6`: `--color-royal-blue-500` + 16 % white, hex because Paper drops `color-mix()` |
| Dark navy (`--color-dark-background`) | `--color-dark-border` (#0000C9, = Primary Blue 600), the Brand Styleguide's own "Divider on dark". Never white at 0.3 |

The same table is documented on the canvas: Brand → Styleguide → *Rulers* section (right after *Borders & dividers*), one swatch per ground with the two lines crossing so the intersection is visible. Keep the two in sync.

This supersedes every older "white at 0.3" instruction, including templates that were built with it (the deck library, event posters). Existing artboards carry the old construction; convert their Rulers to solid when a piece is touched, and never copy the translucent version into new work.

How Rulers are used is in `composition.md`.
