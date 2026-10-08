# Template catalog and slot convention

Read this when choosing a template for any Archy piece, and before touching any layer inside one.

---

## Master files

Each `Master - …` file holds its templates on the `Templates` page. **Nothing is ever written in a master file.** Pieces are made in a copy (see the `brand` skill, *Where the work goes*).

A template is named `TPL · <Family> · <Format> <W×H>`, with no numbers. A piece is named `<Event or campaign> · <Format> <W×H>`, for example `Hinman 2027 · Post 1080×1350`.

### Templates, variants, formats and themes

A template can hold several designs of the same job. Four levels, from broad to narrow:

| Level | What it is | Example |
|---|---|---|
| **Template** | The purpose: what the piece is for | `AE Spotlight` |
| **Variant** | One design (layout and composition) for that purpose | `The Arch`, `Grid Card` |
| **Format** | A size | `Post 1080×1080`, `Stories 1080×1920` |
| **Theme** | The colour treatment, on one of the brand grounds | `White`, `Royal Blue`, `Navy` |

A template with variants is named `TPL · <Template> · <Variant> · <Theme> · <Format> <W×H>`, for example `TPL · AE Spotlight · The Arch · Navy · Post 1080×1080`. On the `Templates` page each variant is a row and the themes sit side by side as Post + Stories pairs.

- **Every variant uses the same slot names**, so the same facts fill any of them and switching variant costs nothing. A slot only one variant has is documented as that variant's own.
- **A theme changes colour only.** Slots, sizes and positions are identical across the themes of a variant.
- **Themes come from the brand grounds** (`tokens.md`), always with tokens, and only where the variant reads well on that ground. A variant does not need every theme.

---

## Slots

A slot is a layer named for what it holds, where a piece is meant to change. They make the common case fast; everything else can still be adjusted when the piece needs it.

| Prefix | Holds | Example |
|---|---|---|
| `slot-text-<role>` | A text to replace (`set_text_content`) | `slot-text-headline`, `slot-text-city`, `slot-text-booth` |
| `slot-image-<role>` | A picture to replace | `slot-image-photo`, `slot-image-speaker` |
| `slot-logo-partner` | The partner's mark, next to the Archy wordmark | |
| `optional-<role>` | A block to remove when there is no content for it | `optional-tickets-offer` |
| `variant-<name>` | One of several pre-designed versions of a block inside one artboard; keep one. Whole alternative designs are variants of the template instead (above) | `variant-ground-dark` |

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

File: `Master - Events`, `app.paper.design/file/01M1F9VXX1S3JJETTVWG2H2PCD`. Every template ships as Post 1080×1350, Stories 1080×1920, OG 1200×630 (see `composition.md`, *Event three-format family*) and **Square 1080×1080**, the fourth column of each row (x 3600). `Event Cover` (1200×900) is the thumbnail of the event page in the Webflow CMS; it sits in the fifth column of the row whose template it follows (x 4830).

One row per template (or per theme), rows 2080 apart, grouped by job: `Booth Icon List`, `Booth Invite Photo` (Navy, then Royal Blue), `Countdown Mascot` (Navy, then Royal Blue), `Countdown Masthead`, `Speaker Invite`, `Booth Light Rulers`, `Booth Photo Band`, `Night Out Illustration`, `Night Out Venue`. The themes of one template always sit in consecutive rows, Navy above Royal Blue, each with its own cover. A new template or theme joins its group; move the rows below it down rather than leaving it at the end.

**Square 1080×1080** is the Post compressed to the square: content column x 105–975, y 90–990, same blocks and order. What changes, so the copy fits:
- Headlines drop to 76–84px and usually run two lines. On the booth templates break them as `Meet Archy at <event start>\n<rest>` (`Meet Archy at Hinman\nDental Meeting`); `Booth Photo Band` keeps the Post's three lines so the mascot stays clear of the text. Countdowns keep `Tomorrow\nis the day` at 124–160px.
- Photo bands shrink (city band 240–350px tall) and the mascot runs at 70–80% of the Post size, still about two thirds visible.
- `Speaker Invite` drops the `Speaker` label and runs the portrait at 160.
- `Booth Invite Photo · Royal Blue` drops the venue line on the Square and gives the room to the city photo (1080×300). `Content` runs to the bottom margin with `justify-content: space-between`, so the lockup sits on y 990 and the freed space becomes air and larger type (headline 88 / 136, city 54).
- Badges keep their size. Place them by screenshot: a badge never touches a text, a pill or the trim; keep about 40px of ground between the badge and any of them.
- Portraits stay centred in their circle when the circle shrinks (see *Photos* in the brand skill).

Masters are named `TPL · <Template> · <Format> <W×H>`; a template with themes adds the theme (`TPL · Booth Invite Photo · Navy · Post 1080×1350`, see *Templates, variants, formats and themes*). Covers are `TPL · Event Cover · <Variant> · Cover 1200×900`, plus the theme when their row has one. The countdown templates (`Countdown Mascot`, `Countdown Masthead`) have no cover: a day-before reminder never becomes an event page.

**Grounds.** Every event template runs on a Pixel Gradient (see the `archy-design:pixel` skill): the artboard keeps its ground token as `backgroundColor` and the gradient PNG on top (`background-size: cover`). `royal-blue` on royal blue templates, `navy` on dark navy ones, `white` or `pure-white` on light ones, made at twice the artboard size with `--cell 16` (8px cells on the canvas) and `--steps 4` on dark grounds, `--steps 6` on light grounds so the grain stays faint. Rulers and photo bars on these grounds follow `tokens.md`, *Ruler colours per ground*.

At a glance, to pick 2 or 3 options that differ from each other:

| Template | Purpose | Ground | Signature |
|---|---|---|---|
| `Booth Icon List` | Booth invite | Royal blue | Kicker pill, three icon rows with Rulers, the mascot off the top |
| `Booth Invite Photo` | Booth invite | Themes: Navy, Royal Blue | City photo band on top with a photo bar, booth badge |
| `Booth Light Rulers` | Booth invite | White | Rulers grid, two-tone headline, booth button |
| `Booth Photo Band` | Booth invite | Light blue gradient | City photo as a base band at the bottom, the mascot off the side |
| `Speaker Invite` | Talk, dinner, local event | Royal blue | Speaker portrait and name, date & time, optional share note |
| `Countdown Mascot` | Day-before reminder | Themes: Navy, Royal Blue | Centred "Tomorrow is the day", the mascot and badge on top |
| `Countdown Masthead` | Day-before reminder | Dark navy | Ruler-flanked masthead, huge headline, badge on the masthead |
| `Night Out Illustration` | Hosted social evening (dinner, drinks, golf) with a sign-up | Dark navy | Cocktail illustration and loose sparkles, label/value details, primary button |
| `Night Out Venue` | Hosted social evening at a named venue | Dark navy | Venue photo band on top with a photo bar, white perks pill, centred |
| `Event Cover` | Thumbnail of the event page in the Webflow CMS (1200×900) | Pixel Tone of the city or venue | White card with `Archy \| Event` + partner lockup, big headline, one content block (booth button, speaker, or photo + text) |

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

Two themes, same slots and layout: `TPL · Booth Invite Photo · Navy · <Format>` (royal blue badge) and `TPL · Booth Invite Photo · Royal Blue · <Format>` (navy badge, `Join Archy at <event>` in the Chicago sample). The Royal Blue theme's photo band is taller (Post 1080×496, Stories 1080×800) and its Square drops the venue line. A 6px `Ruler` bar marks the photo edge (`tokens.md`). On the OG the photo fills the artboard and the `Scrim` carries the grain: the theme's gradient PNG with `mask-image: linear-gradient(90deg, black 0%, black 64%, transparent 92%)`, so it fades into the photo.

| Slot | Notes |
|---|---|
| `slot-image-photo` | City photo, `background-size: cover`. Post band 1080×379 (Royal Blue 1080×496), Stories 1080×600 (Royal Blue 1080×800), OG right side behind the `Scrim` |
| `slot-text-headline` | About 16 characters per line, 3 lines (Post, Stories); 2 lines on the OG. `Meet Archy at <event>` or `Join Archy at <event>` |
| `slot-text-city`, `slot-text-venue`, `slot-text-date` | Venue not on the OG |
| `slot-text-booth` | Inside the badge: 5 characters (`#1039`) |
| `slot-logo-partner` | The organiser (Hinman, Chicago Dental Society in the samples) |

#### Countdown Mascot

Day-before reminder. **Use when** the event is tomorrow. **Not when** it is an invitation weeks ahead.

Two themes, same slots: `TPL · Countdown Mascot · Navy · <Format>` (royal blue badge) and `TPL · Countdown Mascot · Royal Blue · <Format>` (navy badge). On the Royal Blue Post and Stories the mascot, badge and central block sit lower and the extra air goes above the logos.

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

`Content` spans the safe area (Post y 150–1240, Stories y 380–1560, Square y 90–990) with four blocks spread by `justify-content: space-between`: `Header` (wordmark + headline), `slot-text-subhead`, `Details`, `Button`. The cocktail sits beside the headline. `optional-illustration` holds the `Cocktail` (a frame fitted to the glass, so it moves and scales on its own) and one `Star` layer per sparkle, white at 0.45 opacity, scattered in the open areas: move, duplicate or delete them one by one. Keep them sparse (about 12 to 17 per format) and never on a text, a button or cut by the trim. Stories runs a larger wordmark (324×125) and the cocktail at 1.35×, bleeding off the top right. When a longer copy changes a block's height the gaps absorb it; check the stars again. The OG has no button.

| Slot | Post / Stories / Square | OG | Example | Notes |
|---|---|---|---|---|
| `slot-text-headline` | ≤ 20 characters per line, 2 lines, break with `\n` | ≤ 20 per line, 2 lines | `A Free Night Out\nFor Dallas Dentists` | 100/106 bold (84/84 on the OG). A third line pushes into the cocktail: shorten first, then reduce the size |
| `slot-text-subhead` | ≤ 34 characters per line, 3 lines (Stories ≤ 30; Square 42px, 2 lines of ≤ 45) | ≤ 52 per line, 2 lines | `Just free drinks, great food, a few rounds of golf, and Dallas dentists who get it.` | One sentence, the offer in plain words. Post 54/75 with `text-wrap: pretty`, Stories 62/83 with `balance` |
| `slot-text-city` | ≤ 14 characters | ≤ 15 | `Dallas, TX` | `City, ST` |
| `slot-text-venue` | ≤ 21 characters | ≤ 18 | `Topgolf Dallas` | |
| `slot-text-date` | ≤ 18 characters | ≤ 19 | `Friday, October 9` | Weekday + date, format from `voice.md` |
| `slot-text-time` | ≤ 24 characters | ≤ 24 | `6:00 – 8:00 PM` | |
| `slot-text-cta` | ≤ 26 characters | (no button) | `Claim your spot` | Inter Medium 36, padding 28 / 44, arrow 36. Sentence case, the button grows with it |
| `optional-illustration` | `Cocktail` and `Star` layers | same | | Delete the whole layer for a plain ground; the layout needs no other change |

Fixed by design: the labels (`Location`, `Date & Time`), the arrow icon, the wordmark. The illustration keeps its own asset colours (lime, glass blues); do not recolour it.

#### Night Out Venue

The same hosted evening, led by a photo of the venue. From the Dallas Topgolf campaign. Four formats: Post, Stories, OG, Square. **Use when** Archy hosts at a named venue and there is a good photo of it. **Not when** there is no venue photo (use `Night Out Illustration`).

Everything is centred on Post, Stories and Square; the OG sets the content left-aligned beside a photo column. `Content` holds three groups with an 80px gap (56 on the Square), centred in the ground below the photo: `Header` (headline + perks pill, 40px apart), `Details`, and the wordmark (288×112; 180×70 on the OG). The ground is the navy Pixel Gradient alone (no pattern, no `BK Fade`), and a 6px royal blue `Ruler` bar marks the photo edge (vertical on the OG, at x 420).

| Slot | Post / Stories | Square | OG | Example | Notes |
|---|---|---|---|---|---|
| `slot-image-venue` | Top band 1080×420 (Stories 1080×700) | Top band 1080×320 | Left column 420×630 | Topgolf building | `background-size: cover`. A photo from the requester or the venue, never generated (see *Photos* in the brand skill) |
| `slot-text-headline` | ≤ 20 characters per line, 2 lines | ≤ 22 per line, 2 lines | ≤ 25 per line, 2 lines | `30 Dallas dentists.\nOne night out.` | 100/104 bold (88 Square, 64 OG). Break with `\n` |
| `slot-text-perks` | ≤ 49 characters, 1 line | ≤ 49 | ≤ 55 | `Free golf, appetizers, drinks & socializing` | Typed in sentence case, set uppercase by the style. The white pill grows with the text |
| `slot-text-city`, `slot-text-venue` | ≤ 14 / ≤ 20 characters | same | ≤ 12 / ≤ 18 | `Dallas, TX`, `Topgolf Dallas` | |
| `slot-text-date`, `slot-text-time` | ≤ 19 / ≤ 24 characters | same | ≤ 20 / ≤ 24 | `Friday, October 9`, `6:00 – 8:00 PM` | |

Fixed by design: labels, pill style, the photo bar, the wordmark at the bottom (top of the column on the OG).

#### Event Cover

The thumbnail of the event's page in the Webflow CMS (1200×900). One format (no Square, Stories or OG), one cover per event, placed in the fifth column of the row whose template it follows (x 4830). **Use when** an event page, Luma or email invite needs a header image. **Not when** the piece is a social post or a day-before reminder. Pick the cover that matches the social template of the same campaign (the table below); when the event has no social template yet, choose by content: a booth, a speaker, or a hosted evening.

Every cover is built the same way:

- **Ground:** always a photo related to the event (the host city or the venue), turned into a Pixel Tone, even when the social template it follows is illustrated. A cover is its own piece, not a copy of the Post: no illustrations, no mascot, no call-to-action button. The tone is made with the `archy-design:pixel` tool (`effect tone <photo> --gradient <name> --size 1200x900`). Match the ground of the template the cover follows: `royal-blue` for royal blue templates, `navy` for dark navy ones, `ice --invert` for light ones. Place photos only, never a person. Use the requester's photo; a city photo may be generated (see *Photos* in the brand skill); a venue photo is never generated. The Pixel Tone already is the grain: never add a gradient or scrim layer on top of it.
- **Card:** white `Content` (844×804 at 48, 48, padding 56), flex column with a 48px gap. On top, `Logo Lockup`: royal blue wordmark, 2px `Divider`, `Event Label` (`Event`, fixed on every cover: not a slot, never replaced by the event name) and `slot-logo-partner` pushed to the right (navy on the white card; recolour a white partner mark to `--color-light-text` by setting `fill` on every path, not only the root SVG; about 230 wide, 300 for a wide mark).
- **Headline:** two nodes, `slot-text-headline-1` (medium) + `slot-text-headline-2` (bold, the event or talk name), navy, 80–104px. On a light ground follow `Booth Light Rulers`: both semibold, the second in `--color-neutral`.
- **One content block at the bottom**, nothing else. The page itself carries the city, venue, date and time, so the cover does not repeat them:
  - **Booth:** a 2px `Ruler` (`--color-light-border`), then the `Booth Button` (radius 8, padding 24 / 36, `slot-text-booth` 44px bold uppercase, `Booth #1039`). On a blue or navy ground: a `--color-blue-tint-100` label with royal blue text. On a light ground (ice), where a pale label would disappear: a royal blue label with white text.
  - **Speaker:** `slot-image-speaker` (210 circle, 4px royal blue ring, face centred), `Speaker` label, `slot-text-speaker-name` (56), `slot-text-speaker-role` and `slot-text-speaker-company` (32, one line each). The text column is `flex: 1; min-width: 0` so a longer role wraps instead of leaving the card.
  - **Photo + text:** `slot-image-photo` (240 circle) and `slot-text-subhead` (52 semibold navy, 2 or 3 lines, break with `\n`). The subhead adds something the headline does not say (what happens there, where), never a rephrase of it. Two covers of the same event use different photos.
- Nothing ever leaves the card except the ground; check every text on the screenshot.

| Cover | Row | Ground | Content block |
|---|---|---|---|
| `TPL · Event Cover · Booth` | Booth Icon List | Royal Blue tone (Atlanta) | Booth |
| `TPL · Event Cover · Booth Photo · Navy` | Booth Invite Photo · Navy | Navy tone (Atlanta) | Booth |
| `TPL · Event Cover · Booth Photo · Royal Blue` | Booth Invite Photo · Royal Blue | Royal Blue tone (Chicago) | Booth |
| `TPL · Event Cover · Speaker` | Speaker Invite | Royal Blue tone (Denver) | Speaker |
| `TPL · Event Cover · Booth Light` | Booth Light Rulers | Ice tone (Atlanta) | Booth |
| `TPL · Event Cover · Booth Photo Band` | Booth Photo Band | Ice tone (Atlanta), headline medium + bold in navy (no mascot on the covers) | Booth |
| `TPL · Event Cover · Night Out` | Night Out Illustration | Navy tone (Topgolf patio at night); circle: the bays | Photo + text |
| `TPL · Event Cover · Night Out Venue` | Night Out Venue | Navy tone (Topgolf building); circle: guests | Photo + text |


### Master - Ads (ads)

File: `Master - Ads`, `app.paper.design/file/01M4697421B4576AVJ6RKSRGE3`, page `Templates`. One row per variant, rows 2080 apart; in each row the themes sit side by side: White at x 0 (Post) and 1160 (Stories), Royal Blue at 2320 / 3480, Navy at 4640 / 5800. The page `AE Spotlights` keeps the five original explorations as references.

| Template | Purpose | Variants | Themes |
|---|---|---|---|
| `AE Spotlight` | Introduce one Account Executive (or any person) to local practices, with a demo CTA | Meet Name, The Arch, Grid Card, Mosaic, Forum | White, Royal Blue, Navy |

#### AE Spotlight

Masters: `TPL · AE Spotlight · <Variant> · <Theme> · Post 1080×1080` and `… · Stories 1080×1920`, 30 artboards. **Use when** a person is the message: an AE, a speaker or a team member, with a demo or meeting CTA. **Not when** the ad sells a product claim (use `Platform · One-pager` / `Platform · Post` in `Archy - Ads`) or announces an event booth (`Master - Events`).

**Variants.** Meet Name is the default; offer one or two others when the requester has not chosen. Archy Studio renders every variant and theme (`design` / `theme` ids: `meet-name`, `the-arch`, `grid-card`, `mosaic`, `forum`; `white`, `royal`, `navy`).

| Variant | Signature | Headline |
|---|---|---|
| Meet Name | Two-tone hero `Meet <Name>.` beside a full-height photo panel, white name plate on the photo | `Meet <first name>.` + subline (slot) |
| The Arch | Portrait inside an arch, white name plate at its foot | `Meet Your Local Archy Platform Expert`, Title Case by design |
| Grid Card | Rulers across the whole canvas, benefits in three columns, small square portrait beside the name and CTA (Stories: portrait at the bottom) | `Meet your local Archy platform expert.` |
| Mosaic | Content column beside a tall photo panel with a name tile under it (Stories: tile and photo at the bottom) | Same, four lines |
| Forum | Name and role under the headline, above the benefits; half photo panel on Ice | Same, four lines |

**Themes.**

| | White | Royal Blue | Navy |
|---|---|---|---|
| Ground | `white` | `royal-blue-500` | `dark-background` |
| Wordmark, icons | `royal-blue-500` | `white` | wordmark `white`, icons `blue-tint-300` |
| Headline accent | `royal-blue-500` | `blue-tint-200` | `blue-tint-300` |
| Text | `light-text` | `white` | `white` |
| Rulers | `light-border` | `#2A5DF6` | `dark-border` |
| CTA | `royal-blue-500`, white label | `white`, royal label | `royal-blue-500`, white label |
| Location pill on the ground | `blue-tint-100`, royal text and dot | `white`, `primary-blue-600` text, royal dot | `dark-foreground`, white text, `blue-tint-300` dot |

A photo panel that would disappear into the ground takes another gradient: The Arch uses Gradient Royal Blue on White and Navy, Mosaic uses it on Navy, Meet Name uses Gradient Navy on Royal Blue. A pill or plate sitting on the photo keeps its colours in every theme. A Ruler inside a blue block (the Mosaic tile seam) stays `#2A5DF6` on every ground.

**Slots.** The same in every variant and theme.

| Slot | Example | Notes |
|---|---|---|
| `slot-text-ae-first-name` | `Sarah.` | Meet Name only. Keep the period. Post: ≤ 7 characters at full size, down to 70% (≤ 10). Stories: ≤ 5 beside `Meet`, longer names drop to a second line (≤ 9). `Meet` scales with the name |
| `slot-text-ae-name` | `Sarah Thompson` | Limits per variant below |
| `slot-text-ae-title` | `Sr. Account Executive` | Limits per variant below |
| `optional-ae-location` / `slot-text-ae-location` | `Austin, TX` | Post ≤ 20 characters (≤ 24 at 85%; Grid Card ≤ 42, its top row is free), Stories ≤ 29, every variant. Typed in title case, set uppercase by the style. Remove the whole pill when there is no city; nothing else moves |
| `optional-ae-plate` | | Meet Name and The Arch: the white plate holding name and title. Anchored to the bottom, so a second line grows it upward. Remove it when neither is known |
| `slot-image-ae` | | Cut-out portrait (transparent PNG), head and shoulders, face in the upper half. Stories holds it twice in every variant (panel and `Photo Pop-out`); fill both. Always the person's real photo |

| Variant | `ae-name` Post / Stories | `ae-title` Post / Stories | Where they sit |
|---|---|---|---|
| Meet Name | ≤ 18 per line, 2 lines / ≤ 35 per line, 2 lines | ≤ 29 per line, 2 lines / ≤ 57 per line, 2 lines | Plate on the photo. When the name takes two lines, keep the title to one (`Sr. Enterprise AE`) |
| The Arch | ≤ 15 per line, 2 lines / ≤ 18 per line, 2 lines | ≤ 24 per line, 2 lines / ≤ 30 per line, 2 lines | Plate at the foot of the arch. A longer name breaks with `\n` and the plate grows upward; keep it off the face (Stories: left half) |
| Grid Card | ≤ 19 / ≤ 15 | ≤ 30 / ≤ 25 | Name cell, one line each; on Stories keep it left of the portrait |
| Mosaic | ≤ 18 / ≤ 25 | ≤ 29 / ≤ 41 | Name tile, one line each (fixed text width: 378 Post, 535 Stories) |
| Forum | ≤ 24 / ≤ 42 | ≤ 35 / ≤ 62 | Under the headline, one line each |

Limits are measured by Archy Studio on each design and theme; when copy runs over, rewrap where the table allows two lines, then reduce the type a little, then shorten.

Fixed by design: the headlines of The Arch, Grid Card, Mosaic and Forum, the Meet Name subline, the three benefit rows, the CTA, the wordmark, the photo gradients and the Pixel Dissolve. Change them only when the brief needs it (the rules in `../ad/references/ad-layouts.md` still apply). On Meet Name Stories the hero fits on two lines only while the content column stays above the photo panel (y 1160): check the CTA on the screenshot.

### Archy - Ads

File: `Archy - Ads`, `app.paper.design/file/01M33E66BD6FJNP4BPE88V90X0`. **Not a master yet**: its pieces are being designed as future templates and have no slots. Use them as references (duplicate or clone parts into your own file); never edit them in place. The `ad` skill covers how to work from them.

| Page | Pieces | Formats |
|---|---|---|
| `MDIB Social Summit Ad` | `Platform · One-pager`, `Platform · Post`, `Logo · Post` | 1500×1942, 1080×1080 |
| `SDCDS Marketing Material` | `SDCDS Facets Ad A` / `B` (print, plus CMYK export copies) | 1600×975 |
| `AE Spotlights` | Person-led ad, Options A to E (`Meet John`, `The Arch`, `Grid Card`, `Mosaic`, `Forum White`). All five are now variants of the `AE Spotlight` master in `Master - Ads` | Post 1080×1080, Stories 1080×1920 |

Third-party ad references for inspiration live in the `Refs - Ads` file (not brand material).

### Archy - Various Collateral

File: `Archy - Various Collateral`, `app.paper.design/file/01M37ZJ6ECM7XJ5TG5W2Z2YR4N`.

| Template | Formats |
|---|---|
| `Chrome Store · Feature Explainer` | 1280×800 |
| `Chrome Store · Sneak Peek Promo` | 440×280 |

### Archy - Business Cards

File: `Archy - Business Cards`, `app.paper.design/file/01M46XGRN8YXH5EXG4QSX0N446`, page `Business Cards`. Print templates, 3.5 × 2 in, made and exported with the `archy-design:business-card` skill. Artboards are 1125 × 675 (300 px/in, 0.125 in bleed included) on the print-equivalent tokens (`tokens.md`). Each has a `Guides` frame on top: trim (red) and safe zone (green, the box every element touches); hide it with `opacity: 0` before export. Real cards go on a page per print batch (`Oct 2026 - 1`), named `<Full Name> · Front 3.5×2 in` / `· Back QR 3.5×2 in`.

| Template | Purpose | Ground | Signature |
|---|---|---|---|
| `Business Card · Front` | Every card | Print royal blue | White wordmark, two-tone tagline, navy moon pattern on the right |
| `Business Card · Back` | Contact side, no booking link | Print tint 100 | Two-line name, role, email, phone, light blue arc, `archy.com` |
| `Business Card · Back QR` | Contact side with a demo booking link | Print tint 100 | Same column, `SCAN TO BOOK` QR plate in place of the arc |

| Slot | Back | Back QR | Example | Notes |
|---|---|---|---|---|
| `slot-text-name` | ≤ 12 characters per line, 2 lines | ≤ 11 per line, 2 lines | `First Name\nLast Name` | 100 / 102 Onest bold. First name, line break, last name |
| `slot-text-role` | ≤ 22 characters on 1 line at 50 / 60 | Same | `Account Executive` | Longer roles wrap to 2 lines at 40 / 49 (`Sales Development\nRepresentative`). The Details block is anchored to the bottom, so it grows upward |
| `slot-text-email` | ≤ 38 characters | Same | `name@archy.com` | 40 / 56 medium |
| `slot-text-phone` | ≤ 22 characters | Same | `000-000-0000` | Shares its baseline with `archy.com` |
| `slot-image-qr` | | 45 × 45 modules, 254 px | | Generated from the person's HubSpot meetings link, `--color-black`. The template holds a placeholder that does not scan on purpose |

Fixed by design: the front, the arc, the plate, `SCAN TO BOOK`, `archy.com`. Sample content in the templates is placeholder (`First Name`, `name@archy.com`, `000-000-0000`) so a forgotten field shows at proof.

### Master - Decks

File: `Master - Decks`, `app.paper.design/file/01M1HZF1EW0RX9H3YSMJ3GAMK7`. 57 slide layouts at 1920×1080, one page per category. The roster is in the `deck` skill (`layout-catalog.md`).
