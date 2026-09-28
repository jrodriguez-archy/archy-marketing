---
name: doc-ad
description: Create DOC (Dental Ownership Collective) ads in Paper from the DOC - Ads master (19 layouts, five themes, 1:1 / 4:5 / 9:16). Use when someone needs a DOC ad, a DOC paid social piece, a new theme or format of an existing DOC ad, or wants to explore a new DOC ad layout.
---

# DOC ads

Load the `doc-brand` skill first and follow it: never touch the master, tokens only, Satoshi, the lockup from the file, never invent facts, deliver and report.

**Master:** `DOC - Ads` (`app.paper.design/file/01M2696JRRAGD3VPABQBT9XP5H`), page `Ads`. Every layout exists in five themes (Foundations, Startup, Acquisition, Dark, Light) and three formats (1080×1080, 1080×1350, 1080×1920). Artboards are named `<Layout> · <Theme> · <W×H>`. The page `Archive` holds retired pieces for reference only.

## Steps

1. **Pick the layout by what the ad says**, using `references/layout-catalog.md`: a claim, a list, a number, a comparison, a quote, an event. If the requester named a layout or has it selected in Paper (`get_selection`), use it. Otherwise pick 2 or 3 layouts that carry the message in genuinely different ways, build one format of each as options (`<Campaign> · Option A · <Layout>`), and build the rest once they choose.
2. **Pick the theme by the track.** Foundations, Startup or Acquisition when the ad is about one track; Dark or Light when it speaks for DOC as a whole. The theme sets the CTA (`doc-brand` › `voice.md`).
3. **Make the working copy** as `doc-brand` describes, keeping only the artboards used.
4. **Get the facts once**: the message, the track, the CTA destination, any date, speaker, quote, number or photo. A fact that does not exist comes out of the piece; one that is pending gets a visible placeholder.
5. **Fill and adapt** each format, following `references/chassis.md`:
   - set the copy (`set_text_content`, `\n` for breaks) and re-break the two-weight headline so the Bold half starts a line;
   - re-size the hero type to the new copy so its longest line fills the column;
   - keep the lockup ladder and the fixed CTA button;
   - build every format you need from its own sibling in the master, never by stretching another format.
6. **Review** every artboard with `doc-brand` › `review-checklist.md`, plus the ad checks in `chassis.md`.
7. **Deliver**: the file and artboards, the layout and theme each started from, the copy used, anything adjusted beyond the copy, and what is still pending.

Exports are the requester's call; if asked, export PNG at 1x (Paper saves to `~/Downloads`).

## Exploring a new layout

When nothing in the catalog carries the message, propose a new layout and say it is an exploration. Vary **what the piece says** (its content shape), not where the button sits: ten layout permutations of one message read as one idea. Build it on the chassis, one theme and one format first; roll it out to the other themes and formats once it is approved. A layout the team will reuse goes into the master with `archy-design:prepare-template`.

## References

| File | Read it when |
|---|---|
| `references/layout-catalog.md` | Choosing a layout, and what each one holds |
| `references/chassis.md` | Filling or adapting any artboard: structure, margins, the format ladder, type sizing, the CTA, the ad review checks |
| `../doc-brand/references/voice.md` | Writing copy and choosing the CTA |
