# Changelog

All notable changes to the `archy` plugin. Versions follow semver:

- **Patch**: a copy fix or a rule clarified.
- **Minor**: a new template, skill or tool.
- **Major**: a change to the slot naming convention.

## archy 0.9.0 (2026-09-29)

- archy: `doc-video` master rebuilt with the editor's source files for the F3 Foundations videos: 55 templates in eight sections (Structure, Lower Thirds, Text and Lists, Numbers, Charts, Diagrams, Icons, Heroes), 29 Overlay twins, new codes `<Code> · <Name>`, one section label per row. The `Video` page holds templates only; each video gets its own page.
- archy: `doc-video` › `template-catalog.md` rewritten for the new codes, including the new lower thirds, checklist, numbered lists, equation stacks, icon equations, donuts with stats and single-icon layouts.
- archy: `doc-video` › `video-system.md` updated to the exact source values (`--color-video-ground`, `--color-video-ink`, `--color-video-ink-soft`, `--color-video-tag`, red-500 result boxes and icons, red-400 bullets, cream-200 tiles with an 8px radius), a 46-icon library, and a new section on turning an editor's source file into templates.

## archy 0.8.0 (2026-09-29)

- archy: new `doc-video` skill for DOC course video graphics, built on the `DOC - Videos Foundations` master (36 templates at 1920×1080: structure, lists and quotes, figure chains, charts, concept diagrams, icon tiles, hero illustrations; every split template has a transparent `· Overlay` twin).
- archy: `doc-video` references: `template-catalog.md` (each template, its layout and its source moment in the Foundations videos) and `video-system.md` (frame, split and Overlay, colour and type measured on the videos, boxes, icon tiles, icon library, heroes, Paper notes, video review checks).
- archy: `doc-brand` now names `doc-video` and the `DOC - Videos Foundations` master.

## archy 0.7.0 (2026-09-28)

- archy: two new section-divider layouts in `Master - Decks` › Frames: **◆**`Section Preview` (navy, title bottom-left, the section's slides listed in the Cover's right column) and `Section Emoji` (white, one emoji, eyebrow `Part NN`). The library is now 57 layouts, 14 of them dark.
- archy: `layout-catalog.md`, `dark-set.md` and the layout counts in `deck`, `templates.md` and `tokens.md` updated to match.
- archy: `playful-decks.md` gains *Section dividers*: one divider family per deck, where a divider earns its place, and how a divider with the mascot counts toward his appearances.

## archy-design 0.4.0 (2026-09-28)

- archy-design: `slides-export` specs for `Section Preview` and `Section Emoji` (solid `--color-dark-border` Rulers on navy; the emoji ships as `assets-base/emoji-rocket.png`). Template deck builds to 57 slides.

## archy 0.6.1 (2026-09-28)

- archy: new `tools/fonts/install-satoshi.sh`: installs DOC's Satoshi from Fontshare (never from this repository, per its licence), registers it with macOS and clears the quarantine flag; prints the manual steps if it cannot.
- archy: `doc-brand` starts with a font check: without Satoshi installed, Paper silently renders DOC in the system sans. Claude offers to install it and waits for Paper to be reopened.
- archy: `paper-quirks.md`: editing a text node's style while its font is missing rewrites the family to `system-ui` for good; how to detect and restore it; installing a font file is not always enough.
- archy: `doc-ad`: on a 1:1 the height can cap the hero before the width; how to clean the working copy of the 285-artboard master.
- README: DOC setup note about Satoshi.

## archy 0.6.0 (2026-09-28)

- archy: `ad` and `chrome-store` are now real skills (they only had references before, so they never triggered). `ad` works from the Archy - Ads pieces as references until an ads master exists; `chrome-store` covers the store listing images built from native product UI.
- archy: the Archy - Ads catalog lists what the file holds today (MDIB Social Summit, SDCDS print ads, AE Spotlights); `Claim Stack` removed, since it no longer exists.
- README lists `ad` and `chrome-store`.

## archy 0.5.0 (2026-09-28)

- archy: new `doc-brand` skill, the DOC (Dental Ownership Collective) identity: sources of truth and traps, tokens (including new alpha, tint and radius tokens), the lockup and its colourways, the five ad themes, track coding, Satoshi and the two-weight headline, voice and CTA per theme, review checklist.
- archy: new `doc-ad` skill for DOC ads from the `DOC - Ads` master: the ad chassis (auto-layout structure, margins, lockup ladder, fixed CTA button, format rules), type sizing, and a catalog of the 19 layouts.
- archy: `paper-quirks.md`: `color-mix()` is unreliable rather than always dropped; give a tint its own token.
- archy: the brand skill points DOC ads to `doc-ad`. README lists the DOC skills; a stale duplicate skills table removed.

## archy-design 0.3.3 (2026-09-28)

- slides-export: a border that is the same on all four sides becomes the shape's own outline, so a pill badge keeps a round ring and a rotated sticker keeps its frame. Other borders are still per-side strips, now swung with a rotated frame and cut to the clip window.
- slides-export: `align-items: baseline` rows line text up on the baseline (Inter metrics), so a small figure next to a large one no longer sits high.
- slides-export: `background-size` lengths such as `100%` keep the picture's aspect instead of stretching it to the box.

## archy-design 0.3.2 (2026-09-28)

- slides-export: `flex-wrap: wrap` rows now break onto new lines where their children overflow, so a 2 x 2 or 3 x 2 grid of cells exports as a grid instead of one row running off the slide. Frames whose children fit on one line lay out exactly as before.

## archy-design 0.3.1 (2026-09-28)

- slides-export: a rotated image clipped by the artboard (the mascot turned -90deg bleeding off an edge) is now cropped in its own unrotated frame and re-centred on the visible part, instead of losing the wrong side.
- slides-export: `export.sh 7` finds the zero-padded dump `07-…`; a single-digit selection used to match nothing.

## archy 0.4.7 and archy-design 0.3.0 (2026-09-25)

- archy-design: the `gradients` skill and tool are now `pixel` (`/archy-design:pixel`, `tools/pixel/pixel.py`), covering both texture families: `pixel.py gradient …` for Pixel Gradients and `pixel.py effect dissolve | behind | tone` for Pixel Effects.
- archy-design: new Pixel Effects: Pixel Dissolve (scattered cells over a portrait that bleeds off the bottom, as a separate overlay layer), Pixels Behind (a band of cells behind a tight headshot) and Pixel Tone (a place photo in a gradient's own two tones). The ground and the cells share one grid that divides the frame and is anchored to the bleed edge.
- archy-design: every value is a starting point and a flag: `--cell` and `--steps` on gradients; `--colours`, `--density`, `--curve`, `--seed` and `--start` on effects. The skill spells out what is fixed and what is flexible.
- archy: tokens reference points to the Brand file's Textures page; the ad layout guide covers Pixel Effects on portraits.

## archy 0.4.6 and archy-design 0.2.1 (2026-09-25)

- Display names in the plugin manager: `archy` shows as "Archy - Marketing", `archy-design` as "Archy - Design". Plugin ids and skill commands are unchanged.

## archy 0.4.5 and archy-design 0.2.0 (2026-09-25)

- archy-design: new `gradients` skill and tool: the nine Archy pixel-dithered gradients (Navy, Deep Blue, Primary, Royal Blue, Sky, Ice, Pure White, White, Mist) as static PNG, seamless MP4/WebM loops, and live backgrounds for Webflow and React, all from one `presets.json`.
- archy: tokens reference lists the Brand file's new **Gradients** page.
- README lists the `gradients` skill.

## archy 0.4.4 (2026-09-25)

- archy: new `ad/references/ad-layouts.md`, the reviewed rules for person-led ads: starting from an AI mockup, the three-anchor column, headline sizing, benefit lists with icons, the CTA button, photo and name tile, the arch frame and grid layouts.
- archy: Rulers: side verticals run the full height; a photo may fill its grid cell flush to the Rulers.
- archy: the website's primary button (`.button_v2`) and its poster-scale values added to *Devices from the website*.
- archy: the brand skill lists `ad-layouts.md` among its references.

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
