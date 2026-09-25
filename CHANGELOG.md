# Changelog

All notable changes to the `archy` plugin. Versions follow semver:

- **Patch**: a copy fix or a rule clarified.
- **Minor**: a new template, skill or tool.
- **Major**: a change to the slot naming convention.

## archy 0.4.3 (2026-09-25)

- archy: the shell edge (`#C3DDF3`, print `#A9C8E6`) applies on any tinted pale ground, not only Tint 100; pure white keeps no edge.
- archy: review checklist checks the shell edge on pale grounds.

## archy 0.4.2 (2026-09-25)

- archy: every Archy file now carries the Brand mascot master; removed the notes that described the superseded Events head as current.

## archy 0.4.1 (2026-09-25)

- archy: the mascot's eyes are sized by the master; never transplant or hand-scale them.
- archy: a piece that still carries the superseded head gets the whole Brand head, at the old shell size.
- archy: the brand workflow now applies the mascot rules (antenna, edge, orientation, raised eyes, crop) every time he is used.
- archy: review checklist checks that the mascot is the Brand master at its proportions.

## archy 0.4.0 and archy-design 0.1.1 (2026-09-24)

- archy: the mascot is named Archy and is "he"; canvas names say `Mascot`, never "Mascota" (layers and the `Countdown Mascot` template renamed in Master - Events).
- archy: crop rule changed: the ears may be trimmed, the eyes never.
- archy: tone-matched edge per ground (screen and print colours, 5 units, `overflow: visible`), antenna colour per ground, raised eyes in a bleed.
- archy: Brand Mascot page, canonical construction, expressions, the five agents, Mono, and poses.
- archy: review checklist and Paper quirks updated (SVG child replace, SVG via img imports as raster, CSS `d: path`).
- archy-design: print-pdf swaps the mascot edges to print colours; removed the deck-specific scripts from slides-export.

## archy 0.3.0 and archy-design 0.1.0 (2026-09-24)

- New plugin `archy-design` for designers (depends on `archy`): `prepare-template`, `explore`, `publish`, and the tools `slides-export`, `figma-export`, `print-pdf`, `hugeicons`, which moved here from `archy`.
- Tools ported into `archy-design/tools/`: every script reads and writes a work directory (`ARCHY_WORK`, default `${CLAUDE_PLUGIN_DATA}/<tool>/`), never the plugin folder; generic assets in `assets-base/`; new `hugeicons.py`.
- La mascota: the antenna always points into the canvas (top 180°, right −90°, left +90°, bottom upright), "raise/lower" read in her own axis, about two thirds visible, one canonical full-body construction with four expressions, antenna colour follows the ground, eyes raised in a bleed.
- New deck reference: playful decks (warm, non-corporate decks such as onboarding).
- README: the two plugins and setup for designers.

## 0.2.0 (2026-09-24)

- Master - Events: nine event templates, each with Post, Stories and OG: Booth Icon List, Booth Invite Photo, Booth Invite Offer, Booth Light Rulers, Booth Photo Band, Speaker Invite, Countdown Mascota, Countdown Offer, Countdown Masthead. Slots named, partner logo separated into its own slot, solid Rulers, pills and offer bars that grow with their text.
- Templates run on the flat Archy grounds; photos only for speaker portraits and untreated city photos. No background art.
- When no template is chosen, the agent builds 2 or 3 options (the Post of each) for the requester to pick.
- Missing facts: ask; if a fact does not exist, remove it together with its label; placeholders only for facts that are pending.
- Partner logos: requester's file, the official logo made one-colour when needed, or a placeholder; sized optically.
- Masters are never edited: work happens in the user's file or a clone of the master.
- Paper quirks: moving or duplicating vector elements into another SVG, recolouring SVG paths, fixed-width SVG pills.

## 0.1.0 (2026-09-24)

- First release.
- `brand`: Archy brand rules (tokens, composition, voice, review checklist, Paper quirks) and the template catalog. Flexible defaults: masters stay untouched, work happens in a copy, 2 or 3 template options when none is chosen, placeholders for missing facts and logos.
- `social-post`: event social pieces (Post, Stories, OG) from Master - Events. First template: `Booth Icon List`.
- `deck`: slides from the Master - Decks library, including redesigning an existing deck from its PPTX and PDF.
- `offsite-brand`: the Archy Offsite 2026 identity.
- `slides-export`, `figma-export`, `print-pdf`, `hugeicons`: tool skills (documentation; the tools themselves ship in a later version).
- Archy Workspace folder with the marketplaces pre-registered and auto-update on.
