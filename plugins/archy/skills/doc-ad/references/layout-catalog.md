# DOC ad layout catalog

Read this when choosing a layout for a DOC ad. Every layout lives on the `Ads` page of `DOC - Ads` in five themes × three formats (`<Layout> · <Theme> · 1080×1080 | 1080×1350 | 1080×1920`). Rows on the canvas are layouts; columns are themes (Foundations, Startup, Acquisition, Dark, Light). Read positions from `get_basic_info`, not from this file: the canvas gets rearranged by hand.

Each layout exists because it holds a **content shape** the others cannot. Choose by what the ad says.

## At a glance

| Layout | What you have in hand | Signature |
|---|---|---|
| `Bar` | A claim and a CTA | Two-weight headline, body line, CTA bar with button at the foot |
| `Illustration Split` | A claim and a drawing | Text column on the left, line-art slot bleeding off the bottom right |
| `Line-art Hero` | A drawing that is the idea | The art slot fills the piece; the headline is its caption |
| `Index` | A list of five | Numbered hairline rows under a two-weight headline |
| `Stat Hero` | One number | The number at poster size, an eyebrow above, a line below |
| `Track Colorway` | A track name and one strong line | Track label, huge two-line headline, full-bleed footer band with lockup and CTA; recolours from the track token |
| `Comparison` | Two options, DOC and the alternative | Two cards side by side; the DOC card is the only filled shape |
| `Highlight Quote` | A member quote | The quote is the whole ad, key phrases marked with a flat tint |
| `Familiar Thread` | A pain the reader has lived | A chat thread from a broker, landlord or seller; the reply is the punchline |
| `Faculty Card` | A faculty member and their session | A ticket with perforation and notches; portrait, name, role, what they teach |
| `Live Session` | An event with speakers | Question headline, event line, three portrait slots |
| `Apology` | An interruption with a wry reason | A Bold apology, a tagline, the lockup in a solid block bleeding off a corner |
| `Keep Scrolling` | Reverse psychology | "Keep scrolling." on a tilted tint block hanging into the margin, then the real line |
| `Climb Chart` | A cost that builds up | Six bars climbing to the headline's number, bleeding off the bottom |
| `Object Photo` | An absurd staged photo | Full-bleed photo slot carrying its own art direction, scrims top and bottom |
| `Definition` | A term the reader should know | A dictionary entry, part of a numbered glossary series |
| `Checklist` | Steps before a decision | Some items ticked and struck through, the rest open |
| `Myth / Fact` | A belief to correct | The myth faded, the fact in Bold below it |
| `Save the Date` | A date | The date as a numeral at poster size, one line under it |

## Notes per layout

**Bar.** The default when there is one claim. Two-weight headline (setup / payoff), a two-line body broken after the comma, then the CTA bar. On track grounds the bar is cream and the accent is the track colour; on Dark the bar is `--color-ink-soft` with a red button; on Light the bar is red with a cream button. The eyebrow and line in the bar set up the CTA verb (`voice.md`).

**Illustration Split.** Use when a drawing supports the claim. The headline often sits at one size for every format (it is measure-capped), so the extra height of the taller formats goes to the art. The slot is an **outline, never a filled block** (the art is line drawing on the ground): cream at 45% on colour and Dark grounds, `--color-neutral-300` on Light. A spacer in the text row holds the slot's place; the visible slot is a bleed layer pinned to it, so re-pin it after any change above.

**Line-art Hero.** Use when the drawing carries the message. The slot takes `flex-grow`, so every format's extra height goes to the art. The caption is a two-weight line sized to fill the measure.

**Index.** Five numbered items. Ordinals in a fixed-width slot, rules between rows only (never above the first or below the last), rows `min-height` + `fit-content`. The headline is one sentence broken across the weights, so its gap is small (`--spacing-4`).

**Stat Hero.** One figure at poster size (capped by the column, so it stays the same size across formats). Only real figures; a non-numeric "stat" (`Day one`, `3 tracks`) is fine when there is no sourced number. Never invent a statistic.

**Track Colorway.** The ground is the track token and the CTA label takes the same token, so the piece recolours from one value. Margin 64, not 72. The footer band is full-bleed, 200 tall on 1:1 and 4:5; on the Story it grows to the lower third.

**Comparison.** Two cards of equal width. On colour grounds the alternative is a ghost (transparent, cream outline) and the DOC card is solid cream; on Light the DOC card is red; on Dark the alternative is `--color-ink-soft` and the DOC card red. The CTA closes the comparison at the foot.

**Highlight Quote.** The quote, line by line, with two or three key phrases marked by a **straight, square-cornered tint** (not a pill): cream at 20% on colour grounds, `--color-ink-soft` on Dark, red at 14% on Light, text unchanged. The highlight frame uses negative margin equal to its padding so the words keep their lane. Lines are hand-broken per format. Quotes and names come from the requester; placeholders are marked.

**Familiar Thread.** A chat card that fills the band between headline and foot, messages centred in it. Incoming bubbles are a tint of the ground; the reply inverts to the one solid shape, and is set slightly larger. Bubbles use `--radius-bubble` with a `--radius-tail` corner, grouped like a real chat. The contact per theme: Broker, Contractor, Seller, Office Manager, Landlord.

**Faculty Card.** A ticket on the theme ground: perforation with round notches filled with the ground colour, a stub carrying the session. Portrait slot, name, role, "teaches". Faculty names and photos only from the requester.

**Live Session.** Question headline, event line, three portrait slots (4:5 portraits). On the taller formats the speakers go full width above the lockup. CTA is **Save your seat** on every theme.

**Apology.** Four-line Bold apology, a Medium tagline, the lockup in a solid block bleeding off the bottom-right corner. The final full stop is its own node so it can take the accent (red on Light only). On the Story the headline and footer form one centred group.

**Keep Scrolling.** A block tilted −2° hanging into the margin so its text sits on the headline's lane, filled with the tint of the ground (`--color-red-tint`, `--color-purple-tint`, `--color-green-tint`; `--color-ink-soft` on Dark). The lockup runs a step larger here. Rotation is part of the device; do not spread it to other layouts.

**Climb Chart.** Six bars, heights **derived from the data**, never eyeballed: on a bleed, `h = 40 + (Hmax − 40) · v / max` (the 40 is the part off the trim). The last bar equals the headline's number and is the only solid one. Figures come from the requester; otherwise mark them as specimens.

**Object Photo.** A full-bleed photo slot whose label is the art direction (the absurd staging is the idea). Scrims top and bottom in the theme colour keep the headline and the lockup readable. The photo has to be shot or sourced; never generate a real person.

**Definition.** "DOC Glossary · No. NN": the headword at poster size sized to the measure, pronunciation, an italic part of speech, two numbered senses (the plain meaning, then the owner's reality). A series: keep the numbering consistent.

**Checklist.** Two items ticked and struck through, the rest open and Bold, a caption offering help with the rest. Strike-through belongs to this layout; do not reuse it on Myth / Fact.

**Myth / Fact.** The myth at reduced emphasis over the fact in Bold, no strike-through.

**Save the Date.** The date as a numeral (`M.DD`) at poster size, one line under it, an offer line. CTA **Save your spot** on every theme.
