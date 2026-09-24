# Template catalog and slot convention

Read this when choosing a template for any Archy piece, and before touching any layer inside one.

A skill may only produce a piece from a template whose row below says **Status: ready**. A template marked **not prepared** has no slots yet: stop, tell the user which template it is and that it has to be prepared first. Never improvise a layout, and never fill a template that is not ready.

---

## Slot convention

Only layers whose name starts with one of these prefixes may be changed. Every other layer is locked: do not restyle, move, resize, rename or delete it.

| Prefix | What the agent may do | Tool | Example |
|---|---|---|---|
| `slot-text-<role>` | Replace the text | `set_text_content` | `slot-text-headline-1`, `slot-text-city`, `slot-text-booth` |
| `slot-image-<role>` | Replace the picture with an approved image file | `update_styles` on `backgroundImage` only (plus `backgroundSize` in the same call) | `slot-image-photo`, `slot-image-speaker` |
| `slot-logo-partner` | Swap the partner mark for one from the file's `Assets` page | `duplicate_nodes` from `Assets` + `delete_nodes` on the old mark | |
| `optional-<role>` | Delete the whole block when there is no content for it | `delete_nodes` | `optional-tickets-offer`, `optional-footer-note` |
| `variant-<name>` | Keep one of several pre-designed versions, delete the others | `delete_nodes` | `variant-ground-blue`, `variant-ground-dark` |

A slot's role names what it holds, not what it currently says: `slot-text-city`, never `slot-text-atlanta`.

### Two-tone headlines

A two-tone headline is two text nodes (Paper cannot colour part of one). They are two slots: `slot-text-headline-1` (first colour) and `slot-text-headline-2` (second colour). Split the copy where the design splits it, usually mid-sentence.

### What is never allowed

- `write_html` into a template or a copy of one.
- `update_styles` on anything except a `slot-image-*` background and the position of the new artboard itself.
- Changing a font size to make copy fit. If copy does not fit its slot, shorten the copy.

---

## File structure

Every Paper file that holds templates has four pages:

| Page | Purpose | Agent may write? |
|---|---|---|
| `Templates` | Master artboards, named `TPL · <Family> · <Format> <W×H>` | **No** |
| `Output` | Where the agent duplicates a master and fills it | Yes |
| `Assets` | Approved partner logos, city skylines, photos | No (read and duplicate from it) |
| `Archive` | Past campaigns kept for reference | No |

Master names carry no numbers: order comes from the page, and a number goes stale the moment a template is inserted.

A new piece in `Output` is named `<Event or campaign> · <Format> <W×H>`, for example `Hinman 2026 · Post 1080×1350`.

---

## How to read a catalog row

| Field | Meaning |
|---|---|
| **File / page** | Which Paper file must be open, and which page the master lives on |
| **Masters** | The master artboard name for each format |
| **Slots** | Every editable layer, with its limit: characters per line × lines, measured at the slot's real type size |
| **Optional** | Blocks that may be deleted when empty |
| **Use when / not when** | The brief this template answers, and the one it does not |

Limits are measured, not estimated: on the canvas, at the slot's own size and weight. A limit of `22 × 2` means two lines of about 22 characters. Treat it as a ceiling; the rendered screenshot is the final check.

---

## Catalog

### Small Events - 2026 (event social)

File: `Small Events - 2026`, `app.paper.design/file/01M1F9VXX1S3JJETTVWG2H2PCD`. Every template ships as three formats: Post 1080×1350, Stories 1080×1920, OG 1200×630 (see `composition.md`, *Event three-format family*).

The file currently holds finished campaigns on a single page, numbered 1 to 9. Seven distinct layouts come out of them:

| Template | Built from | Layout in one line | Status |
|---|---|---|---|
| `Booth Invite · Photo` | 1.x (Chicago), 3.x (Atlanta) | "Join/Meet Archy at <event>" over a photo band and city skyline, booth badge, location + date, optional tickets offer, logo lockup | not prepared |
| `Countdown · Mascota` | 2.x (Chicago), 4.x (Atlanta) | Label pill, "Tomorrow is the day", la mascota bleeding off the top, skyline, badge, location, logo lockup | not prepared |
| `Speaker Invite` | 5.x (Denver, AADOM) | Photographic ground, headline, speaker portrait + name, location, date & time, footer share note, logos at the top | not prepared |
| `Booth · Light Rulers` | 6.x (Hinman) | Light ground, Rulers, two-tone headline, location + date, booth line, logo lockup | not prepared |
| `Booth · Icon List` | 7.x (Hinman) | Light ground, kicker with dot, headline, three icon rows (location, date, booth) separated by Rulers | not prepared |
| `Booth · Photo Band` | 8.x (Hinman) | Photo band at the top, logos, headline, one Ruler, location and date side by side | not prepared |
| `Countdown · Skyline Masthead` | 9.x (Hinman) | Ruler-flanked masthead, "Tomorrow is the day" with the badge in the headline band, skyline + BK Fade, details row, logo lockup | not prepared |

Full slot tables are added here as each template is prepared.

### Archy - Ads

File: `Archy - Ads`, `app.paper.design/file/01M33E66BD6FJNP4BPE88V90X0`.

| Template | Formats | Status |
|---|---|---|
| `Claim Stack` | Post, Stories, OG | not prepared |
| `Platform · One-pager` | 1500×1942 (Letter proportion) | not prepared |
| `Platform · Post` | 1080×1080 | not prepared |

### Archy - Various Collateral

File: `Archy - Various Collateral`, `app.paper.design/file/01M37ZJ6ECM7XJ5TG5W2Z2YR4N`.

| Template | Formats | Status |
|---|---|---|
| `Chrome Store · Feature Explainer` | 1280×800 | not prepared |
| `Chrome Store · Sneak Peek Promo` | 440×280 | not prepared |

### Master - Decks

File: `Master - Decks`, `app.paper.design/file/01M1HZF1EW0RX9H3YSMJ3GAMK7`. 55 slide layouts at 1920×1080, one page per category. The roster is in the `deck` skill (`layout-catalog.md`). Status: **not prepared** (all 55).
