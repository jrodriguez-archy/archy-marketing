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

File: `Master - Events`, `app.paper.design/file/01M1F9VXX1S3JJETTVWG2H2PCD`. Every template ships as three formats: Post 1080×1350, Stories 1080×1920, OG 1200×630 (see `composition.md`, *Event three-format family*). The `Night Out` templates add a fourth, **Square 1080×1080** (content column x 105–975, y 90–990), in the fourth column of their row. `Event Cover` is a single 1200×900 format. Masters are named `TPL · <Template> · <Format> <W×H>`.

At a glance, to pick 2 or 3 options that differ from each other:

| Template | Purpose | Ground | Signature |
|---|---|---|---|
| `Booth Icon List` | Booth invite | Royal blue | Kicker pill, three icon rows with Rulers, the mascot off the top |
| `Booth Invite Photo` | Booth invite | Dark navy | City photo band on top, booth badge |
| `Booth Light Rulers` | Booth invite | White | Rulers grid, two-tone headline, booth button |
| `Booth Photo Band` | Booth invite | Light blue gradient | City photo as a base band at the bottom, the mascot off the side |
| `Speaker Invite` | Talk, dinner, local event | Royal blue | Speaker portrait and name, date & time, optional share note |
| `Countdown Mascot` | Day-before reminder | Dark navy | Centred "Tomorrow is the day", the mascot and badge on top |
| `Countdown Masthead` | Day-before reminder | Dark navy | Ruler-flanked masthead, huge headline, badge on the masthead |
| `Booth Invite Offer` | Booth invite with a giveaway | Royal blue | Like `Booth Invite Photo`, plus an offer strip with a team or sponsor logo ("Win prizes + Bulls tickets") |
| `Countdown Offer` | Day-before reminder with a giveaway | Royal blue | Like `Countdown Mascot`, plus the offer strip |
| `Night Out Illustration` | Hosted social evening (dinner, drinks, golf) with a sign-up | Dark navy | Cocktail illustration and sparkles off the top right, label/value details, primary button |
| `Night Out Venue` | Hosted social evening at a named venue | Dark navy | Venue photo band on top, drinks pattern texture, white perks pill, centred |
| `Event Cover` | Cover image for the event page or invite (1200×900) | Royal blue photo | Venue photo under a royal blue scrim, white card with `Archy \| Event` lockup, guest photo circle |

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

Fixed by design (adjust only when the piece needs it): the kicker pill, labels (`Location`, `Date`, `Booth`), icons, Rulers, the mascot, the OG badge, the Archy wordmark.


#### Booth Invite Photo

Booth invite with a photo of the host city. **Use when** there is a booth and a good city photo. **Not when** there is no photo of the city (use `Booth Icon List` or `Booth Light Rulers`).

| Slot | Notes |
|---|---|
| `slot-image-photo` | City photo, `background-size: cover`. Post band 1080×379, Stories 1080×600, OG right half behind a scrim |
| `slot-text-headline` | About 16 characters per line, 3 lines (Post, Stories); 2 lines on the OG. `Meet Archy at <event>` |
| `slot-text-city`, `slot-text-venue`, `slot-text-date` | Venue not on the OG |
| `slot-text-booth` | Inside the badge: 5 characters (`#1039`) |

#### Countdown Mascot

Day-before reminder. **Use when** the event is tomorrow. **Not when** it is an invitation weeks ahead.

| Slot | Notes |
|---|---|
| `slot-text-kicker` | Event name + year in a white pill that grows with the text; keep it to one line (about 30 characters) |
| `slot-text-headline` | `Tomorrow is the day` or an equivalent short line; two lines, break with `\n` |
| `slot-text-city`, `slot-text-venue` | Venue not on the OG |
| `slot-text-booth` | Inside the badge: 5 characters |

#### Speaker Invite

A talk, dinner or local event with a named speaker. **Use when** there is a speaker and a date and time. **Not when** it is a booth at a trade show.

| Slot | Notes |
|---|---|
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
| `slot-image-photo` | City photo band (Chicago in the sample) |
| `slot-text-headline` | `Join Archy at <event>`, 3 lines |
| `slot-text-city`, `slot-text-venue`, `slot-text-date` | Venue not on the OG |
| `slot-text-booth` | Inside the badge: 5 characters |
| `optional-offer` | The giveaway strip (Post, Stories). Remove it if there is no offer |
| `slot-text-offer` | Uppercase line in the navy bar, which grows with the text; about 30 characters |
| `slot-logo-offer` | The team or sponsor mark at the left of the bar (the Bulls in the sample) |
| `slot-logo-partner` | The organiser (Chicago Dental Society in the sample) |

#### Countdown Offer

`Countdown Mascot` with the giveaway strip, from the Chicago Midwinter campaign. **Use when** the event is tomorrow and there is an offer to promote.

| Slot | Notes |
|---|---|
| `slot-text-kicker` | Event name in the white pill |
| `slot-text-headline` | `Tomorrow is the day` |
| `slot-text-city`, `slot-text-venue` | Venue not on the OG |
| `slot-text-booth` | Inside the badge |
| `optional-offer`, `slot-text-offer`, `slot-logo-offer` | As in `Booth Invite Offer` (Post, Stories) |

#### Countdown Masthead

Day-before reminder with the event name as a Ruler-flanked masthead, on the dark navy ground. **Use when** the event is tomorrow and the name should lead. **Not when** it is an early invitation.

| Slot | Notes |
|---|---|
| `slot-text-kicker` | Event name + year between two Rulers; the Rulers shrink as it grows, keep it to about 30 characters |
| `slot-text-headline` | `Tomorrow is the day`: two lines on Post and Stories, one on the OG |
| `slot-text-booth` | Inside the badge: 5 characters |
| `slot-text-city`, `slot-text-venue`, `slot-text-date` | Venue not on the OG |

#### Night Out Illustration

A free evening Archy hosts for local dentists (drinks, food, golf, a dinner), with a call to sign up. From the Dallas Topgolf campaign. Four formats: Post, Stories, OG, Square. **Use when** Archy is the host, there is a date, time and place, and no venue photo (or a lighter, illustrated feel is wanted). **Not when** it is a booth at a trade show, or a talk with a named speaker (use `Speaker Invite`).

`Content` spans the safe area (Post y 150–1240, Stories y 380–1560, Square y 90–990) with four blocks spread by `justify-content: space-between`: `Header` (wordmark + headline), `slot-text-subhead`, `Details`, `Button`. The cocktail sits beside the headline; `Stars` layers add sparkles in the open areas. Stories runs a larger wordmark (324×125) and the cocktail at 1.35× (resize `Cocktail`, which scales the lime by percentage, then the glass and sparkle SVGs by the same factor), bleeding off the top right. When a longer copy changes a block's height the gaps absorb it; keep every star clear of the text. The OG has no button.

| Slot | Post / Stories / Square | OG | Example | Notes |
|---|---|---|---|---|
| `slot-text-headline` | ≤ 20 characters per line, 2 lines, break with `\n` | ≤ 20 per line, 2 lines | `A Free Night Out\nFor Dallas Dentists` | 100/106 bold (84/84 on the OG). A third line pushes into the cocktail: shorten first, then reduce the size |
| `slot-text-subhead` | ≤ 34 characters per line, 3 lines (Stories ≤ 30; Square 42px, 2 lines of ≤ 45) | ≤ 52 per line, 2 lines | `Just free drinks, great food, a few rounds of golf, and Dallas dentists who get it.` | One sentence, the offer in plain words. Post 54/75 with `text-wrap: pretty`, Stories 62/83 with `balance` |
| `slot-text-city` | ≤ 14 characters | ≤ 15 | `Dallas, TX` | `City, ST` |
| `slot-text-venue` | ≤ 21 characters | ≤ 18 | `Topgolf Dallas` | |
| `slot-text-date` | ≤ 18 characters | ≤ 19 | `Friday, October 9` | Weekday + date, format from `voice.md` |
| `slot-text-time` | ≤ 24 characters | ≤ 24 | `6:00 – 8:00 PM` | |
| `slot-text-cta` | ≤ 26 characters | (no button) | `Claim your spot` | Inter Medium 36, padding 28 / 44, arrow 36. Sentence case, the button grows with it |
| `optional-illustration` | Swoosh, cocktail, sparkles, `Stars` | Cocktail, sparkles, `Stars` | | Delete the whole layer for a plain ground; the layout needs no other change |

Fixed by design: the labels (`Location`, `Date & Time`), the arrow icon, the wordmark. The illustration keeps its own asset colours (lime, glass blues); do not recolour it.

#### Night Out Venue

The same hosted evening, led by a photo of the venue. From the Dallas Topgolf campaign. Four formats: Post, Stories, OG, Square. **Use when** Archy hosts at a named venue and there is a good photo of it. **Not when** there is no venue photo (use `Night Out Illustration`).

Everything is centred on Post, Stories and Square; the OG sets the content left-aligned beside a photo column. `Content` holds three groups with an 80px gap (56 on the Square), centred in the ground below the photo: `Header` (headline + perks pill, 40px apart), `Details`, and the wordmark (288×112; 180×70 on the OG). A `BK Fade` over the drinks pattern (a dark oval behind the text plus a fade to the bottom) keeps the texture at the edges only.

| Slot | Post / Stories | Square | OG | Example | Notes |
|---|---|---|---|---|---|
| `slot-image-venue` | Top band 1080×420 (Stories 1080×700) | Top band 1080×320 | Left column 420×630 | Topgolf building | `background-size: cover`. A photo from the requester or the venue, never generated (see *Photos* in the brand skill) |
| `slot-text-headline` | ≤ 20 characters per line, 2 lines | ≤ 22 per line, 2 lines | ≤ 25 per line, 2 lines | `30 Dallas dentists.\nOne night out.` | 100/104 bold (88 Square, 64 OG). Break with `\n` |
| `slot-text-perks` | ≤ 49 characters, 1 line | ≤ 49 | ≤ 55 | `Free golf, appetizers, drinks & socializing` | Typed in sentence case, set uppercase by the style. The white pill grows with the text |
| `slot-text-city`, `slot-text-venue` | ≤ 14 / ≤ 20 characters | same | ≤ 12 / ≤ 18 | `Dallas, TX`, `Topgolf Dallas` | |
| `slot-text-date`, `slot-text-time` | ≤ 19 / ≤ 24 characters | same | ≤ 20 / ≤ 24 | `Friday, October 9`, `6:00 – 8:00 PM` | |
| `optional-illustration` | Drinks pattern at 0.16 opacity | | | | Delete for a plain ground; the `BK Fade` can go with it |

The drinks pattern is texture, not content: it stays at low opacity (it arrived with a `multiply` blend, which is banned). Fixed by design: labels, pill style, the wordmark at the bottom (top of the column on the OG).

#### Event Cover

The cover image for the event's registration page or invite (1200×900), from the Dallas Topgolf campaign. One format. **Use when** an event page, Luma or email invite needs a header image. **Not when** the piece is a social post (use the `Night Out` templates).

A white card (`Content`, 844×804 at 48, 48, padding 56) on a venue photo tinted by a royal blue `Scrim` at 0.8 (a solid scrim replaces the `overlay` blend it arrived with). Inside: `Logo Lockup` (royal blue wordmark, 2px `Divider`, kicker), headline, and a `Footer` row with the guest photo circle and the subhead.

| Slot | Limit | Example | Notes |
|---|---|---|---|
| `slot-image-venue` | Full bleed 1200×900 | Topgolf bays | Under the `Scrim`; any photo reads as a blue duotone. From the requester or the venue, never generated |
| `slot-text-kicker` | ≤ 12 characters | `Event` | Set uppercase by the style (`Event`, `Dinner`, `Webinar`) |
| `slot-text-headline` | ≤ 17 characters per line, 3 lines | `A Free Night Out\nFor Dallas Dentists` | 88/96 medium, navy (`--color-light-text`) |
| `slot-image-photo` | 216 circle, 4px royal blue ring | Guests toasting | People enjoying the venue. Real photos only |
| `slot-text-subhead` | ≤ 25 characters per line, 3 lines | `A few rounds of Topgolf, free drinks, apps and great company on us` | |


### Master - Ads (ads)

File: `Master - Ads`, `app.paper.design/file/01M4697421B4576AVJ6RKSRGE3`, page `Templates`. Rows: Post at x 0, Stories at x 1160. The page `AE Spotlights` keeps the five original explorations as references.

| Template | Purpose | Ground | Signature |
|---|---|---|---|
| `AE Spotlight` | Introduce one Account Executive (or any person) to local practices, with a demo CTA | White, with a royal blue photo panel | Two-tone hero `Meet <Name>.`, three benefit rows, cut-out portrait over Pixel Dissolve, white name plate |

#### AE Spotlight

Masters: `TPL · AE Spotlight · Post 1080×1080`, `TPL · AE Spotlight · Stories 1080×1920`. **Use when** a person is the message: an AE, a speaker or a team member introduced by first name, with a demo or meeting CTA. **Not when** the ad sells a product claim (use `Platform · One-pager` / `Platform · Post` in `Archy - Ads`) or announces an event booth (`Master - Events`).

| Slot | Post | Stories | Example | Notes |
|---|---|---|---|---|
| `slot-text-ae-first-name` | ≤ 7 characters at full size, 1 line; down to 70% (≤ 10) | ≤ 5 beside `Meet`; longer names drop to a second line (≤ 9 at full size) | `Sarah.` | Keep the period. `Meet` scales with the name so the hero always reads as one size. On Stories, reduce first to stay on one line, then let the row wrap |
| `slot-text-ae-name` | ≤ 18 characters per line, 2 lines | ≤ 35 per line, 2 lines | `Sarah Thompson` | Name plate, Onest semibold. The plate is anchored to the bottom (Post: the CTA baseline), so a second line grows it upward |
| `slot-text-ae-title` | ≤ 29 characters per line, 2 lines | ≤ 57 per line, 2 lines | `Sr. Account Executive` | Shares the plate with the name: when the name takes two lines, keep the title to one (`Sr. Enterprise AE`) |
| `optional-ae-location` / `slot-text-ae-location` | ≤ 20 characters (≤ 24 at 85%) | ≤ 46 characters | `Austin, TX` | Pill, set uppercase by the style. Remove the whole pill when there is no city; nothing else moves |
| `slot-image-ae` | Cut-out portrait (transparent PNG), bottom aligned | Same image twice: in the panel and in the head pop-out above it | | Always the person's real photo, background removed. Framing like the sample: head and shoulders, face in the upper half |

Fixed by design: `Meet`, the subline, the three benefit rows, the CTA, the wordmark, the gradient panel and the Pixel Dissolve. Change them only when the brief needs it (the rules in `../ad/references/ad-layouts.md` still apply). On Stories the hero fits on two lines only while the content column stays above the photo panel (y 1160): check the CTA on the screenshot.

### Archy - Ads

File: `Archy - Ads`, `app.paper.design/file/01M33E66BD6FJNP4BPE88V90X0`. **Not a master yet**: its pieces are being designed as future templates and have no slots. Use them as references (duplicate or clone parts into your own file); never edit them in place. The `ad` skill covers how to work from them.

| Page | Pieces | Formats |
|---|---|---|
| `MDIB Social Summit Ad` | `Platform · One-pager`, `Platform · Post`, `Logo · Post` | 1500×1942, 1080×1080 |
| `SDCDS Marketing Material` | `SDCDS Facets Ad A` / `B` (print, plus CMYK export copies) | 1600×975 |
| `AE Spotlights` | Person-led ad, Options A to E (`Meet John`, `The Arch`, `Grid Card`, `Mosaic`, `Forum White`). Option A is now the `AE Spotlight` master in `Master - Ads` | Post 1080×1080, Stories 1080×1920 |

Third-party ad references for inspiration live in the `Refs - Ads` file (not brand material).

### Archy - Various Collateral

File: `Archy - Various Collateral`, `app.paper.design/file/01M37ZJ6ECM7XJ5TG5W2Z2YR4N`.

| Template | Formats |
|---|---|
| `Chrome Store · Feature Explainer` | 1280×800 |
| `Chrome Store · Sneak Peek Promo` | 440×280 |

### Master - Decks

File: `Master - Decks`, `app.paper.design/file/01M1HZF1EW0RX9H3YSMJ3GAMK7`. 57 slide layouts at 1920×1080, one page per category. The roster is in the `deck` skill (`layout-catalog.md`).
