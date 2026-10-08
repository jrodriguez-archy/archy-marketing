---
name: prepare-template
description: Turn a finished Archy campaign or design in Paper into a slot-ready template for the marketing team, and document it in the template catalog. Use when a designer wants to add, prepare, convert or fix a template in a Master file (Master - Events, Master - Ads, Master - Decks and others).
---

# Prepare a template

For designers. Load `archy:brand` first: every template must already follow the brand rules, and this is the moment to fix what does not. The result is a master the `archy` production skills can fill quickly and safely.

## 1. Pick the source and the master file

- The source is a finished campaign or a new design. The destination is the matching `Master - …` file, page `Templates`. Exception: `Master - Ads` has one page per template, named after it (`AE Spotlight`); a new ad template gets a new page with `create_page`, a new variant or theme goes on its template's page. Masters keep the three formats together (Post, Stories, OG) when the family has them.
- Before building, check the catalog (`archy:brand` → `references/templates.md`, *At a glance*) and decide what the design is:
  - **A new template** when it serves a purpose no template has.
  - **A new variant** of an existing template when it serves the same purpose with a different design, even with exactly the same content. Give it the template's slot names.
  - **A new theme** of a variant when only the colours change: recolour a copy with tokens on another brand ground (`templates.md`, *Templates, variants, formats and themes*).
  - **An improvement** of the existing master when it is the same design with different copy.
- Duplicate the source artboards onto `Templates` (or the template's page in `Master - Ads`; never edit the original in place), one row per template or variant (Post at `left: 0`, Stories at 1160, OG at 2320, rows about 2080 apart), `translate: none`. With themes, the themes of a row sit side by side as Post + Stories pairs.
- Name them `TPL · <Template> · <Format> <W×H>`, or `TPL · <Template> · <Variant> · <Theme> · <Format> <W×H>` when the template has variants, with no numbers.
- Paper only screenshots the active page: build and review the copies on the page that is open, then move them to `Templates` (or the template's page) with `move_nodes`.

## 2. Fix it against the brand

Screenshot each artboard and run `archy:brand` → `references/review-checklist.md`. The defects that come up every time:

- **Rulers and dividers at `opacity` or white-alpha** → solid colour for the ground (table in `tokens.md`). A divider drawn as an SVG path cannot be recoloured with `update_styles`: replace it with a 2px frame with a `backgroundColor`.
- **Hex fills** → tokens.
- **Labels typed wrong** and hidden by `text-transform` (`location`, `Date & TIME`) → type them properly.
- **Fixed-width SVG shapes behind text** (a pill, a label bar) → a frame with `backgroundColor`, `padding`, `borderRadius` and `width: fit-content`, so a longer text stays inside.
- **Fixed-width text columns** that make a longer string wrap (a spaced date) → widen the column, rebalance the gaps.
- **Background art or fades with no job** → remove them. Templates run on the Archy grounds: a Pixel Gradient on event templates (`archy-design:pixel`, recipe in `templates.md`), with the ground token kept as `backgroundColor`; photos only for speaker portraits and untreated city photos. A photo band gets its 6px photo bar (`tokens.md`).
- **Sample copy** in the house style (`voice.md`), e.g. `March 12 – 14, 2026`.

## 3. Separate the partner logo

The lockup must be `Logo Lockup` (flex row, `space-between`) = `Logo Archy` + a `slot-logo-partner` frame holding the partner mark, so it can be swapped. Imports usually arrive as one SVG holding both marks. In order of preference:

1. **Clone a lockup that is already clean** (from another template in the file) with `<x-paper-clone>`, then set the Archy and partner sizes to the original's.
2. **Write the partner SVG fresh** with `write_html` from its `get_jsx` path data, with `fill="var(--color-…)"` on every path.
3. **Heavy marks** (dozens of paths inheriting colour from the root): move the whole root SVG into the slot frame, delete the Archy element from it, and offset it with `position: absolute; left: -<x>px` so only the partner shows.

Never move or duplicate a vector *element* into another SVG: it lands hundreds of pixels off and loses its colour (see `archy:brand` → `paper-quirks.md`).

## 4. Name the slots

Rename every layer that changes per piece (convention in `templates.md`, *Slots*):

- `slot-text-<role>`: `kicker`, `headline` (or `headline-1` / `-2` for two-tone), `city`, `venue`, `date`, `datetime`, `booth`, `speaker-name`, `speaker-role`, `speaker-company`, `perks`, `footer-note`…
- `slot-image-<role>`: `photo`, `speaker`.
- `slot-logo-partner`.
- `optional-<role>` for a block that can go when empty (`optional-footer-note`, `optional-illustration`).

Read the tree (`get_tree_summary`) and confirm each name against the node's actual text: children are not always in the same order between formats. Name the mascot `Mascot`.

## 5. Measure and document

- Measure the room each text slot has (character widths from the sample text, or a `max-content` row of test strings) and note the practical limit and line count per format.
- Add the template to `templates.md`: a row in *At a glance* (purpose, ground, signature), and a section with **Use when / Not when** and the slot table with limits and notes.
- Screenshot the three formats one last time, then `finish_working_on_nodes`.

## 6. Publish

The template is live in Paper for everyone as soon as it is saved, but the catalog is not. Run the `publish` skill (minor version: a new template).
