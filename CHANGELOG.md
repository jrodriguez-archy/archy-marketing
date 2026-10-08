# Changelog

All notable changes to the `archy` plugin. Versions follow semver:

- **Patch**: a copy fix or a rule clarified.
- **Minor**: a new template, skill or tool.
- **Major**: a change to the slot naming convention.

## archy 0.13.2 (2026-10-08)

- Event Cover: the `Event` label next to the Archy wordmark is fixed on every cover (layer `Event Label`, formerly `slot-text-kicker`); it is not a slot and is never replaced by the event name.

## archy-design 0.7.3 (2026-10-06)

- doc-video-edit: the frame of a camera change inside its pause is chosen by eye again. `cut_pick.py` and `cut_check.py --pick` / `--snap` are removed: on approved videos the script moved up to 17 cuts per video by 0.3 to 1.1 s, biased late, onto the mouth opening and sometimes into another pause.
- doc-video-edit: `cut_check.py` is a report only: it flags measurable errors (in speech, mid-sentence, short pause, short shot, sandwich) and LOOK only for a silence over ~1 s; it never moves a cut.

## archy 0.13.1 (2026-10-06)

- doc-video: numbered squares (T2, T7, any figure in a square) centre the digit with a flex frame instead of hand offsets, plus a small optical correction (Satoshi figures sit low; a `1` looks left-heavy), checked with a screenshot at scale 4.

## archy-design 0.7.2 (2026-10-05)

- business-card, print-pdf: print files are named `<Piece> - Print - Bleed.pdf` and `<Piece> - Print - Bleed - Crop Marks.pdf` (`Print` implies CMYK; `Bleed` on both, since both carry it).

## archy-design 0.7.1 (2026-10-05)

- business-card: a card ships as exactly two PDFs (crop marks, bleed only), each with both sides; no single-page files.
- print-pdf: single-page files only on request; the combined PDF is the delivery, and Illustrator users open one page at a time to get editable curves.

## archy-design 0.7.0 (2026-10-05)

- New skill `business-card`: Archy business cards from the `Archy - Business Cards` templates: what to ask for, a page per print batch, slot rules (two-line name, one- or two-line role with the bottom-anchored Details block), a HubSpot booking QR generated and verified by `scripts/make_qr.py`, and delivery in two versions (crop marks, bleed only) plus single-page files.
- print-pdf: text converted to curves (`-dNoOutputFonts`), checked with `pdffonts`.
- print-pdf: crop marks with `scripts/marks.ps`: sheet 0.5 in larger than trim, 0.25 pt registration marks outside the bleed, TrimBox and BleedBox written; documents the `initgraphics` trap that draws marks inside the artwork.
- print-pdf: deliver one file per page as well, since Illustrator opens multi-page PDFs as embedded objects; hide guide layers with `opacity: 0` before export; design QRs in `--color-black`; multi-artboard exports, the canvas-colour base fill and plate checks at 600 dpi.

## archy 0.13.0 (2026-10-05)

- New template family in the catalog: `Archy - Business Cards` (Front, Back, Back QR at 3.5 × 2 in + bleed), with guides, slot limits and the long-role rule (`templates.md`).
- tokens.md: print-equivalent tokens (`--color-print-*`) for print pieces that must match material already printed, with their CMYK builds, and the guide tokens; the Business Cards file in *Where things live*.
- paper-quirks.md: `display: none` then `block` strips `position: absolute` from a frame's children; hide with `opacity: 0`.

## archy 0.12.0 (2026-10-05)

- New master file `Master - Ads` with its first template, `AE Spotlight` (Post 1080×1080, Stories 1080×1920): slot table with measured limits in `templates.md`.
- AE Spotlight: the name plate is anchored to the bottom so a two-line name grows upward; on Stories the `Meet <Name>.` row wraps for long names; `Meet` scales with the name.
- `ad` skill starts person-led ads from `TPL · AE Spotlight`; the `AE Spotlights` explorations stay as references.

## archy-design 0.6.2 (2026-10-01)

- doc-video-edit: no dead air at section starts: the speaker is already talking on the first frame after the intro (start the take ~0.1 s before the first word) and as each wipe opens (a long pause there shortened to ~0.4 s, the join hidden at the wipe cover); on `_Post_` footage only with the user's OK.
- doc-video-edit: closing without a T10 goes out ~0.45 s after the last word, then the crossfade; a longer `_Post_` tail (over ~1 s) is proposed for a trim, and ending the take there is enough when the speaker stays still.
- doc-video-edit: a black frame on a cut is fixed by moving the cut 1-2 frames; aligning it to a source frame does not help.

## archy-design 0.6.1 (2026-10-01)

- doc-video-edit: a colour guide is no longer a plugin rule: when the video folder has a `COLOR_GUIDE.md`, grade to it (`measure_color.py` reads its skin and wall targets); without one, grade from the setup suggestion and match CAM B to CAM A (`measure_color.py` checks B - A only). `references/color-guide.md` removed.
- doc-video-edit: `scripts/export_final.sh` (ProRes -> x264 export) removed; export with `tsrct export --fps 24`.

## archy-design 0.6.0 (2026-10-01)

- doc-video-edit: where to cut inside a pause is now decided per cut, not by a fixed offset: the outgoing shot ends on the finished thought, the incoming shot starts with life (speech, a breath, a movement), never on a silent, frozen face (edit-system > Cameras, "Where to cut", and checklist point 3).
- doc-video-edit: new `scripts/cut_pick.py` chooses that frame for every camera change by measuring each camera's face movement through the pause against its own talking movement (still, life, blink); `cut_check.py --pick` shows the choice and the reason, `--snap` applies it, and every moved cut is then checked by eye.
- doc-video-edit: `cut_check.py` reports the silence each shot holds at every cut and a LOOK flag with the psheet frames to watch; the contradictory fixed-offset rules and flags (DEAD-HOLD, LATE-CUT, DEAD-AIR) are removed.
- doc-video-edit: house colour guide `references/color-guide.md` (measured skin and wall targets for both cameras, starting values, limits, grain, export) with `scripts/measure_color.py`, and `scripts/export_final.sh` for 10-bit finals; `grade_match.py` and its out-of-limit per-video values are removed.
- doc-video-edit: the export step uses Tesseract's direct export (with the house grain) and measures the export's colour.

## archy-design 0.5.1 (2026-09-30)

- archy-design: the plugin description now mentions DOC course video editing.

## archy-design 0.5.0 (2026-09-30)

- archy-design: new skill `doc-video-edit`: edits a DOC Foundations course video end to end in Tesseract from the two camera files, the brief and the video's page in `DOC - Videos Foundations` (cut list, camera plan, native animated graphics, red section wipes, intro and end card, sound, grade), with a builder (`scripts/`) that turns a per-video `video.json` into the project.
- doc-video-edit: builders for S3, L1, T1, T2 (with a highlighted section-marker state), T4 (with re-entry), T7, T11 (every number counts up), N3, N6, N7, N8, and T10 at the end or inside the video.
- doc-video-edit: house rules: `_Post_` footage is not re-cut, every sound ends on a fade, the intro music leaves in one slow progressive descent, number cards get reading time, an ending on camera crossfades into the end card, and every export is scanned for black frames.
- doc-video-edit: camera rhythm: A/B changes follow ideas and land at sentence ends, shots hold ~8 to 20 s, and `build_video.py` prints `pacing:` warnings (short shots, same-camera zoom cuts, a split or card not covered by its graphic).
- doc-video-edit: a five-point checklist for every cut (ends a thought, real pause checked by transcribing each side, face still, cameras in sync, holds in the export).
- doc-video-edit: multicam as one picture: `scripts/cam_sync.py` measures the picture offset between cameras (`cam_offset`), `reframe` composes each camera without enlarging the face, and `scripts/grade_match.py` matches CAM B's grade to CAM A by measurement.
- doc-video-edit: a lower third never covers the face: every lower third is checked on its actual shot after a reframe.

## archy 0.11.2 (2026-09-29)

- archy: `templates.md` › `Night Out Illustration` re-laid out: four blocks spread over the safe area, larger subhead, details and button, extra `Stars` layers, and on Stories a larger wordmark and a 1.35× cocktail. Limits updated.
- archy: `templates.md` › `Night Out Venue`: two-line headline at 100px, headline and perks pill grouped, content centred below a larger venue photo, larger wordmark, and a `BK Fade` that keeps the drinks pattern at the edges.

## archy 0.11.1 (2026-09-29)

- archy: `doc-video` › S3 Speaker Lower Third: the role tag hangs off the right end of the name box, not centred under it.
- archy: `doc-video` › T2 Numbered List: how to centre the digit in its red square.
- archy: `brand` › `paper-quirks.md`: a layer hidden in Paper cannot be shown through the MCP; rebuild it visible or toggle it by hand.

## archy 0.11.0 (2026-09-29)

- archy: three new `Master - Events` templates from the Dallas Topgolf campaign: `Night Out Illustration` and `Night Out Venue` (hosted social evening, Post, Stories, OG and a new Square 1080×1080 format) and `Event Cover` (1200×900 event page or invite cover). Catalog rows, slots and measured limits in `templates.md`.
- archy: `brand` › *Photos* adds venue photos (`slot-image-venue`) as a third allowed kind: from the requester or the venue, never generated.
- archy: `social-post` covers hosted evenings, the Square format and the event cover, and asks for the time and the call to action.

## archy 0.10.0 (2026-09-29)

- archy: new `start` skill for first-time users: checks that Paper is connected (and Satoshi for DOC work), lists what they can ask for with one example per skill, gives the key tips (real facts, untouched masters, options, exports) and offers a first piece.

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
