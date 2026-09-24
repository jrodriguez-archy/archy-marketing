# Template catalog and slot convention

Read this when choosing a template for any Archy piece, and before touching any layer inside one.

**Status: ready** means the master has named slots and measured limits, so filling it is fast and safe. **Not prepared** means the layout exists (usually as a campaign on `Archive`) but has no slots yet: it can still be used, by duplicating that campaign to `Output` and replacing its copy directly. Say which one you started from.

---

## Slot convention

Slots are where a piece is meant to change. Start there. Anything else can still be adjusted when the piece needs it (see the `brand` skill, *Defaults, and how far they bend*), and every such adjustment is reported.

| Prefix | What the agent may do | Tool | Example |
|---|---|---|---|
| `slot-text-<role>` | Replace the text | `set_text_content` | `slot-text-headline-1`, `slot-text-city`, `slot-text-booth` |
| `slot-image-<role>` | Replace the picture with an approved image file | `update_styles` on `backgroundImage` only (plus `backgroundSize` in the same call) | `slot-image-photo`, `slot-image-speaker` |
| `slot-logo-partner` | Swap the partner mark for one from the file's `Assets` page, and size it to the format's logo height | `delete_nodes` on the mark inside the slot, `duplicate_nodes` from `Assets` with `parentId` = the slot frame, then `update_styles` `width`/`height` on that SVG only (keep its aspect ratio) | |
| `optional-<role>` | Delete the whole block when there is no content for it | `delete_nodes` | `optional-tickets-offer`, `optional-footer-note` |
| `variant-<name>` | Keep one of several pre-designed versions, delete the others | `delete_nodes` | `variant-ground-blue`, `variant-ground-dark` |

A slot's role names what it holds, not what it currently says: `slot-text-city`, never `slot-text-atlanta`.

### Two-tone headlines

A two-tone headline is two text nodes (Paper cannot colour part of one). They are two slots: `slot-text-headline-1` (first colour) and `slot-text-headline-2` (second colour). Split the copy where the design splits it, usually mid-sentence.

### Adapting beyond the slots

- Keep the template's structure: the same blocks, in the same order, on the same grid.
- Prefer, in this order: rewrapping text, resizing a text box, reducing display type (not below about 75% of the template size), adjusting a gap, hiding a block.
- Never touch the master on `Templates`; adapt the copy on `Output`.
- List every adjustment in the delivery message.

### Missing partner logo

The piece is always delivered; the logo is completed when it is available.

1. **Check `Assets`** (`Partner Logos · White on blue`). If it is there, use it.
2. **If the user has the file**, they can drop it straight into the `slot-logo-partner` frame in Paper; offer that.
3. **Otherwise look for the official logo** on the organiser's website or press kit (their homepage header usually links it). Then:
   - A vector you can recolour: set its fills to `var(--color-white)`.
   - A colour raster or an SVG that only wraps a PNG (common): make a one-colour white version from its alpha channel (Python: `Image.open(f).convert('RGBA')`, keep the alpha, paint every pixel white) and save it to `${CLAUDE_PLUGIN_DATA}/logos/<name>-white.png`.
   - Place it with `write_html` into `slot-logo-partner`: `<img src="paper-asset://<absolute path>" style="width:…;height:…;flex-shrink:0;object-fit:contain">`. Paper uploads it to its own storage, so the piece keeps working after the local file is gone.
   - Size it **optically**, not to the number: a thin serif mark needs to be larger than a heavy one to match the Archy wordmark (Yankee Dental Congress needed 124px tall where Hinman sits at 100). Check the lockup in the screenshot.
   - Copy it onto `Assets` → `Partner Logos · White on blue`, named `Logo <Partner> (to verify)`, and tell the user where it came from so a designer can swap in the official reversed version.
4. **If there is no usable logo**, put a placeholder in `slot-logo-partner`: a frame at the format's logo height and about 300px wide, `2px dashed var(--color-blue-tint-300)` border, `--radius-tag` corners, with `PARTNER LOGO` centred in the kicker style (uppercase, `0.05em`, `--color-blue-tint-300`). Name it `placeholder-logo-partner` and list it as pending.

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

### Master - Events (event social)

File: `Master - Events`, `app.paper.design/file/01M1F9VXX1S3JJETTVWG2H2PCD`. Every template ships as three formats: Post 1080×1350, Stories 1080×1920, OG 1200×630 (see `composition.md`, *Event three-format family*).

Past campaigns (numbered 1 to 9) are on the `Archive` page. Seven distinct layouts come out of them; each becomes a master on `Templates` once prepared:

| Template | Built from | Layout in one line | Status |
|---|---|---|---|
| `Booth Invite · Photo` | 1.x (Chicago), 3.x (Atlanta) | "Join/Meet Archy at <event>" over a photo band and city skyline, booth badge, location + date, optional tickets offer, logo lockup | not prepared |
| `Countdown · Mascota` | 2.x (Chicago), 4.x (Atlanta) | Label pill, "Tomorrow is the day", la mascota bleeding off the top, skyline, badge, location, logo lockup | not prepared |
| `Speaker Invite` | 5.x (Denver, AADOM) | Photographic ground, headline, speaker portrait + name, location, date & time, footer share note, logos at the top | not prepared |
| `Booth · Light Rulers` | 6.x (Hinman) | Light ground, Rulers, two-tone headline, location + date, booth line, logo lockup | not prepared |
| `Booth Icon List` | 7.x (Hinman) | Royal blue ground, kicker pill, headline, three icon rows (location, date, booth) separated by Rulers, la mascota off the top, logo lockup | **ready** |
| `Booth · Photo Band` | 8.x (Hinman) | Photo band at the top, logos, headline, one Ruler, location and date side by side | not prepared |
| `Countdown · Skyline Masthead` | 9.x (Hinman) | Ruler-flanked masthead, "Tomorrow is the day" with the badge in the headline band, skyline + BK Fade, details row, logo lockup | not prepared |

Full slot tables are added here as each template is prepared.

#### Booth Icon List · **ready**

Booth invitation for a dental meeting or trade show where Archy has a booth. Masters on page `Templates`:

| Format | Master |
|---|---|
| Post | `TPL · Booth Icon List · Post 1080×1350` |
| Stories | `TPL · Booth Icon List · Stories 1080×1920` |
| OG | `TPL · Booth Icon List · OG 1200×630` |

**Use when** the brief is "come see us at booth #N": event name, city, venue, dates, booth number and the organiser's logo.
**Not when** there is no booth (a talk, a dinner, a local meetup: see `Speaker Invite`), or the day-before reminder (see the `Countdown` templates).

Slots (limits measured on the canvas at each slot's own size; the rendered screenshot is the final check):

| Slot | Post / Stories | OG | Example | Notes |
|---|---|---|---|---|
| `slot-text-kicker` | ≤ 48 characters, 1 line | ≤ 48, 1 line | `Hinman Dental Meeting 2026` | Official event name + year. Set uppercase by the style; type it in title case |
| `slot-text-headline` | ≤ 15 characters per line, ≤ 3 lines (~40 total) | ≤ 20 per line, **2 lines**, break with `\n` | `Meet Archy at Hinman Dental Meeting` | Keep the `Meet Archy at <event>` pattern. OG: put the line break yourself (`Meet Archy at\nHinman Dental Meeting`); its second line must end before the badge. If the event name does not fit two lines, first reduce the headline size in small steps (down to about 64px); if it still does not fit, use the organiser's own short name (`Yankee Dental`, `Hinman`) on the OG only and mention it. The full name stays in the kicker |
| `slot-text-city` | ≤ 34 characters | city + date together ≤ 44 | `Atlanta, GA` | `City, ST` |
| `slot-text-venue` | ≤ 50 characters | (not in the OG) | `Georgia World Congress Center` | |
| `slot-text-date` | ≤ 34 characters | see city | `March 12 – 14, 2026` | Format from `voice.md` |
| `slot-text-booth` | ≤ 12 characters | **≤ 5 characters** (badge) | `#1039` | Always `#` + number. The OG badge holds 5 characters; check it at `scale: 2` |
| `slot-logo-partner` | height 100 | height 86 | Hinman | Partner logos live on `Assets` → `Partner Logos · White on blue`. Match the Archy wordmark optically (see `composition.md`, *Logo lockups*) |

Locked: the kicker pill, labels (`Location`, `Date`, `Booth`), icons, Rulers, la mascota, the OG badge ribbon, the Archy wordmark, every position and size.
No optional blocks.

If the partner's logo is not on `Assets`, follow *Missing partner logo* above.

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
