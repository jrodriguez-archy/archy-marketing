# Template catalog and slot convention

Read this when choosing a template for any Archy piece, and before touching any layer inside one.

---

## Master files

Each `Master - …` file holds its templates on the `Templates` page. **Nothing is ever written in a master file.** Pieces are made in a copy (see the `brand` skill, *Where the work goes*).

A template is named `TPL · <Family> · <Format> <W×H>`, with no numbers. A piece is named `<Event or campaign> · <Format> <W×H>`, for example `Hinman 2027 · Post 1080×1350`.

---

## Slots

A slot is a layer named for what it holds, where a piece is meant to change. They make the common case fast; everything else can still be adjusted when the piece needs it.

| Prefix | Holds | Example |
|---|---|---|
| `slot-text-<role>` | A text to replace (`set_text_content`) | `slot-text-headline`, `slot-text-city`, `slot-text-booth` |
| `slot-image-<role>` | A picture to replace | `slot-image-photo`, `slot-image-speaker` |
| `slot-logo-partner` | The partner's mark, next to the Archy wordmark | |
| `optional-<role>` | A block to remove when there is no content for it | `optional-tickets-offer` |
| `variant-<name>` | One of several pre-designed versions; keep one | `variant-ground-dark` |

A two-tone headline is two text nodes (Paper cannot colour part of one), so it is two slots: `slot-text-headline-1` and `slot-text-headline-2`, split where the design splits it.

### Partner logo

Each piece brings its own partner logo:

1. **The user has the file**: they can drop it straight into the `slot-logo-partner` frame in Paper, or give you the path.
2. **Otherwise find the official logo** on the organiser's website or press kit. It has to read on the piece's ground:
   - A vector: set its fills to `var(--color-white)` on a blue or dark ground.
   - A colour raster, or an SVG that only wraps a PNG (common): make a one-colour white version from its alpha channel (Python: `Image.open(f).convert('RGBA')`, keep the alpha, paint every pixel white), saved under `${CLAUDE_PLUGIN_DATA}/logos/`.
   - Place it in `slot-logo-partner` with `write_html`: `<img src="paper-asset://<absolute path>" style="width:…;height:…;flex-shrink:0;object-fit:contain">`. Paper uploads it, so the piece keeps working without the local file.
3. **No usable logo**: put a placeholder in the slot (a frame at the logo height, about 300px wide, `2px dashed var(--color-blue-tint-300)`, `PARTNER LOGO` centred in the kicker style) and list it as pending.

Size the logo **optically**, not to a number: a thin serif mark needs to be larger than a heavy one to balance the Archy wordmark (Yankee Dental Congress needed 124px tall where Hinman sits at 100). A logo you made or found yourself is provisional: say where it came from so the official version can replace it.

---

## How to read a catalog row

| Field | Meaning |
|---|---|
| **File** | The master file that holds the template |
| **Masters** | The master artboard name for each format |
| **Slots** | Every editable layer, with its limit: characters per line × lines, measured at the slot's real type size |
| **Use when / not when** | The brief this template answers, and the one it does not |

Limits are measured on the canvas at each slot's own size. They are a guide for when copy starts to need adapting; the screenshot is the final check.

---

## Catalog

### Master - Events (event social)

File: `Master - Events`, `app.paper.design/file/01M1F9VXX1S3JJETTVWG2H2PCD`. Every template ships as three formats: Post 1080×1350, Stories 1080×1920, OG 1200×630 (see `composition.md`, *Event three-format family*).

#### Booth Icon List

Booth invitation for a dental meeting or trade show where Archy has a booth. Masters on page `Templates`:

| Format | Master |
|---|---|
| Post | `TPL · Booth Icon List · Post 1080×1350` |
| Stories | `TPL · Booth Icon List · Stories 1080×1920` |
| OG | `TPL · Booth Icon List · OG 1200×630` |

**Use when** the brief is "come see us at booth #N": event name, city, venue, dates, booth number and the organiser's logo.
**Not when** there is no booth (a talk, a dinner, a local meetup) or it is the day-before reminder.

Slots (limits measured on the canvas at each slot's own size; the rendered screenshot is the final check):

| Slot | Post / Stories | OG | Example | Notes |
|---|---|---|---|---|
| `slot-text-kicker` | ≤ 48 characters, 1 line | ≤ 48, 1 line | `Hinman Dental Meeting 2026` | Official event name + year. Set uppercase by the style; type it in title case |
| `slot-text-headline` | ≤ 15 characters per line, ≤ 3 lines (~40 total) | ≤ 20 per line, **2 lines**, break with `\n` | `Meet Archy at Hinman Dental Meeting` | Keep the `Meet Archy at <event>` pattern. OG: put the line break yourself (`Meet Archy at\nHinman Dental Meeting`); its second line must end before the badge. If the event name does not fit two lines, first reduce the headline size in small steps (down to about 64px); if it still does not fit, use the organiser's own short name (`Yankee Dental`, `Hinman`) on the OG only and mention it. The full name stays in the kicker |
| `slot-text-city` | ≤ 34 characters | city + date together ≤ 44 | `Atlanta, GA` | `City, ST` |
| `slot-text-venue` | ≤ 50 characters | (not in the OG) | `Georgia World Congress Center` | |
| `slot-text-date` | ≤ 34 characters | see city | `March 12 – 14, 2026` | Format from `voice.md` |
| `slot-text-booth` | ≤ 12 characters | **≤ 5 characters** (badge) | `#1039` | Always `#` + number. The OG badge holds 5 characters; check it at `scale: 2` |
| `slot-logo-partner` | height about 100 | height about 86 | Hinman | Balance it optically with the Archy wordmark (see *Partner logo* above) |

Fixed by design (adjust only when the piece needs it): the kicker pill, labels (`Location`, `Date`, `Booth`), icons, Rulers, la mascota, the OG badge, the Archy wordmark.


### Archy - Ads

File: `Archy - Ads`, `app.paper.design/file/01M33E66BD6FJNP4BPE88V90X0`.

| Template | Formats |
|---|---|
| `Claim Stack` | Post, Stories, OG |
| `Platform · One-pager` | 1500×1942 (Letter proportion) |
| `Platform · Post` | 1080×1080 |

### Archy - Various Collateral

File: `Archy - Various Collateral`, `app.paper.design/file/01M37ZJ6ECM7XJ5TG5W2Z2YR4N`.

| Template | Formats |
|---|---|
| `Chrome Store · Feature Explainer` | 1280×800 |
| `Chrome Store · Sneak Peek Promo` | 440×280 |

### Master - Decks

File: `Master - Decks`, `app.paper.design/file/01M1HZF1EW0RX9H3YSMJ3GAMK7`. 55 slide layouts at 1920×1080, one page per category. The roster is in the `deck` skill (`layout-catalog.md`).
