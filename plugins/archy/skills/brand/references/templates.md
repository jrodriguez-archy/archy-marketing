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
| `slot-art-<role>` | Vector background art tied to the content (a city skyline); swap it for the right city's art or remove it | `slot-art-city` |
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

File: `Master - Events`, `app.paper.design/file/01M1F9VXX1S3JJETTVWG2H2PCD`. Every template ships as three formats: Post 1080×1350, Stories 1080×1920, OG 1200×630 (see `composition.md`, *Event three-format family*). Masters are named `TPL · <Template> · <Format> <W×H>`.

At a glance, to pick 2 or 3 options that differ from each other:

| Template | Purpose | Ground | Signature |
|---|---|---|---|
| `Booth Icon List` | Booth invite | Royal blue | Kicker pill, three icon rows with Rulers, la mascota off the top |
| `Booth Invite Photo` | Booth invite | Dark navy | City photo band on top, booth badge, skyline art behind |
| `Booth Light Rulers` | Booth invite | White | Rulers grid, two-tone headline, booth button |
| `Booth Photo Band` | Booth invite | Light blue gradient | City photo as a base band at the bottom, la mascota off the side |
| `Speaker Invite` | Talk, dinner, local event | Royal blue over a photo | Speaker portrait and name, date & time, optional share note |
| `Countdown Mascota` | Day-before reminder | Dark navy | Centred "Tomorrow is the day", la mascota and badge on top |
| `Countdown Skyline Masthead` | Day-before reminder | Dark navy | Ruler-flanked masthead, huge headline, badge on the masthead |
| `Booth Invite Offer` | Booth invite with a giveaway | Blue under a dark skyline | Like `Booth Invite Photo`, plus an offer strip with a team or sponsor logo ("Win prizes + Bulls tickets") |
| `Countdown Offer` | Day-before reminder with a giveaway | Blue under a dark skyline | Like `Countdown Mascota`, plus the offer strip |

Common to all: `slot-logo-partner` sits at the right of the lockup (about 100 tall on Post and Stories, smaller on the OG); balance it optically with the Archy wordmark. Kickers and event names are typed in title case; the style sets them uppercase. Dates follow `voice.md` (`March 12 – 14, 2026`).

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


#### Booth Invite Photo

Booth invite with a photo of the host city. **Use when** there is a booth and a good city photo. **Not when** there is no photo of the city (use `Booth Icon List` or `Booth Light Rulers`).

| Slot | Notes |
|---|---|
| `slot-image-photo` | City photo, `background-size: cover`. Post band 1080×379, Stories 1080×600, OG right half behind a scrim |
| `slot-art-city` | Vector skyline behind the content (Post, Stories), faded by the BK Fade. Swap for the right city or remove it |
| `slot-text-headline` | About 16 characters per line, 3 lines (Post, Stories); 2 lines on the OG. `Meet Archy at <event>` |
| `slot-text-city`, `slot-text-venue`, `slot-text-date` | Venue not on the OG |
| `slot-text-booth` | Inside the badge: 5 characters (`#1039`) |

#### Countdown Mascota

Day-before reminder. **Use when** the event is tomorrow. **Not when** it is an invitation weeks ahead.

| Slot | Notes |
|---|---|
| `slot-text-kicker` | Event name + year in a white pill that grows with the text; keep it to one line (about 30 characters) |
| `slot-text-headline` | `Tomorrow is the day` or an equivalent short line; two lines, break with `\n` |
| `slot-text-city`, `slot-text-venue` | Venue not on the OG |
| `slot-text-booth` | Inside the badge: 5 characters |
| `slot-art-city` | Skyline silhouette behind the content (Post, Stories) |

#### Speaker Invite

A talk, dinner or local event with a named speaker. **Use when** there is a speaker and a date and time. **Not when** it is a booth at a trade show.

| Slot | Notes |
|---|---|
| `slot-image-background` | Full-bleed photo behind a royal blue wash |
| `slot-text-headline` | The talk title; two lines, about 22 characters each |
| `slot-image-speaker` | Circular portrait (the frame clips it) |
| `slot-text-speaker-name`, `slot-text-speaker-role`, `slot-text-speaker-company` | One line each |
| `slot-text-city`, `slot-text-venue` | Venue not on the OG |
| `slot-text-datetime` | `February 24, 2026 · 6:00 pm` |
| `optional-footer-note` / `slot-text-footer-note` | Share prompt under a Ruler (Post, Stories); remove the block if there is none |
| `slot-logo-partner` | The hosting association (AADOM in the sample) |

#### Booth Light Rulers

Booth invite on white with the Rulers grid. **Use when** the piece should feel light and editorial, or sits next to other light pieces. **Not when** the feed needs a strong colour moment.

| Slot | Notes |
|---|---|
| `slot-text-headline-1` / `slot-text-headline-2` | Two-tone headline: `Meet Archy at` (navy) / `<event>` (grey) |
| `slot-text-city`, `slot-text-venue`, `slot-text-date` | Venue not on the OG |
| `slot-text-booth` | The whole button label: `Booth #1039` |
| Logos | Archy in royal blue, partner in navy (`--color-light-text`) on this ground |

#### Booth Photo Band

Booth invite on a light ground with the city photo as a base band. **Use when** there is a strong city photo and a lighter look is wanted. **Not when** there is no photo.

| Slot | Notes |
|---|---|
| `slot-text-headline` | About 16 characters per line, 3 lines (Post, Stories), 3 on the OG |
| `slot-text-city`, `slot-text-venue` | Venue not on the OG |
| `slot-text-date`, `slot-text-booth` | Booth sits under the date as `Booth #1039` (Post, Stories); on the OG it is the badge (5 characters) |
| `slot-image-photo` | Bottom band on Post and Stories, right third on the OG |
| Logos | Archy in royal blue, partner in navy on this ground |

#### Booth Invite Offer

`Booth Invite Photo` with a giveaway strip, from the Chicago Midwinter campaign. **Use when** there is a booth and a prize or tickets to promote. **Not when** there is no offer (use `Booth Invite Photo`).

| Slot | Notes |
|---|---|
| `slot-image-photo`, `slot-art-city` | City photo band and city skyline (Chicago in the sample) |
| `slot-text-headline` | `Join Archy at <event>`, 3 lines |
| `slot-text-city`, `slot-text-venue`, `slot-text-date` | Venue not on the OG |
| `slot-text-booth` | Inside the badge: 5 characters |
| `optional-offer` | The giveaway strip (Post, Stories). Remove it if there is no offer |
| `slot-text-offer` | Uppercase line in the navy bar, which grows with the text; about 30 characters |
| `slot-logo-offer` | The team or sponsor mark at the left of the bar (the Bulls in the sample) |
| `slot-logo-partner` | The organiser (Chicago Dental Society in the sample) |

#### Countdown Offer

`Countdown Mascota` with the giveaway strip, from the Chicago Midwinter campaign. **Use when** the event is tomorrow and there is an offer to promote.

| Slot | Notes |
|---|---|
| `slot-text-kicker` | Event name in the white pill |
| `slot-text-headline` | `Tomorrow is the day` |
| `slot-text-city`, `slot-text-venue` | Venue not on the OG |
| `slot-text-booth` | Inside the badge |
| `optional-offer`, `slot-text-offer`, `slot-logo-offer` | As in `Booth Invite Offer` (Post, Stories) |
| `slot-art-city` | City skyline behind the content |

#### Countdown Skyline Masthead

Day-before reminder with the event name as a Ruler-flanked masthead. **Use when** the event is tomorrow and the name should lead. **Not when** it is an early invitation.

| Slot | Notes |
|---|---|
| `slot-text-kicker` | Event name + year between two Rulers; the Rulers shrink as it grows, keep it to about 30 characters |
| `slot-text-headline` | `Tomorrow is the day`: two lines on Post and Stories, one on the OG |
| `slot-text-booth` | Inside the badge: 5 characters |
| `slot-text-city`, `slot-text-venue`, `slot-text-date` | Venue not on the OG |
| `slot-art-city` | Skyline silhouette behind the content |


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
