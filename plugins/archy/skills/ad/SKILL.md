---
name: ad
description: Create Archy ads in Paper (paid social, person-led spotlights, one-pagers and the Posts derived from them, print ads), starting from the Master - Ads templates and the pieces in the Archy - Ads file. Use when someone needs an Archy ad, an ad for a sponsor or partner event, an AE or speaker spotlight, a one-pager, or a square Post adapted from a larger ad. Not for event booth posts (social-post) or DOC ads (doc-ad).
---

# Archy ads

Load the `brand` skill first and follow it: never touch the source pieces, keep the brand rules, deliver, report.

## Source

**Templates:** `Master - Ads` (`app.paper.design/file/01M4697421B4576AVJ6RKSRGE3`), holds the slot-ready ads, one page per template named after it (today page `AE Spotlight`, Post and Stories). Fill them like any master: work in a copy (see *Where the work goes* in the `brand` skill) and follow the slot table in `../brand/references/templates.md` (*Master - Ads*).

**References:** Paper file `Archy - Ads` (`app.paper.design/file/01M33E66BD6FJNP4BPE88V90X0`). **It is not a master yet**: its pieces are being designed as future templates and carry no slots. Treat them as references:

- never edit them in place; work in the requester's file or a new one;
- borrow freely: duplicate artboards into your file, or clone parts (lockups, buttons, the mascot, benefit rows) with `<x-paper-clone>` when working in the same file, or `get_jsx` → `write_html` across files;
- since there are no slots, read the tree (`get_tree_summary`, `get_node_info`) to find the copy and images to replace, and rename layers to their content as you go.

What is there today is in `../brand/references/templates.md` (*Archy - Ads*). Third-party ad references for inspiration are in the `Refs - Ads` file; they are ideas, never brand material.

## Pick the starting point by what the ad has

| The ad has | Start from | Rules |
|---|---|---|
| A person (an AE, a speaker, a team member) with a headline, benefits and a CTA | `TPL · AE Spotlight` in `Master - Ads`: pick the variant (Meet Name by default) and the theme (White, Royal Blue, Navy) | `references/ad-layouts.md` |
| A product claim with the mascot, as a tall one-pager | `Platform · One-pager` | `references/one-pager-to-post.md` |
| A square Post derived from a taller ad | `Platform · Post` | `references/one-pager-to-post.md` |
| A print ad at a physical size | `SDCDS Facets Ad A` / `B` | then `archy-design:print-pdf` for the printer file |
| Nothing that fits, or an AI mockup | An exploration inspired by the pieces above | `references/ad-layouts.md`, *Starting from an AI mockup* |

When the requester has not chosen, offer 2 or 3 directions that differ in ground, composition and what leads (see *Options* in the `brand` skill), then build the other formats of the one they pick. Say which piece each started from, and say when it is an exploration.

## Steps

1. **Read the brief**: the one message, the person or product, the CTA and destination, the formats (Post 1080×1080, Stories 1080×1920, OG 1200×630, a one-pager, print). Ask once for missing facts; a person's name, title and photo always come from the requester.
2. **Make the working file** (the requester's, or a new one named after the campaign) and bring the starting piece into it.
3. **Fill and adapt**: copy first, then everything the piece needs. Type runs bigger than feels safe on the hero only; one hero per format; the lockup, Rulers, button and mascot follow `composition.md`.
4. **Other formats**: Stories keeps the Post's sizes and repositions; the OG is re-laid out (`composition.md`, *Event three-format family*).
5. **Review** every artboard with `../brand/references/review-checklist.md`, plus the ad rules in the references.
6. **Deliver**: the artboards, what each started from, the copy used, what was adapted, what is pending. If a piece should become a reusable template, say so; preparing it is `archy-design:prepare-template`, into `Master - Ads`.

Exports are the requester's call; if asked, export PNG at 1x (Paper saves to `~/Downloads`). Print goes through `archy-design:print-pdf`.

## References

| File | Read it when |
|---|---|
| `references/ad-layouts.md` | Any person-led ad, a headline next to a photo, a benefit list, the CTA button, or a brief that arrives as an AI mockup |
| `references/one-pager-to-post.md` | Deriving a square Post from a taller ad, or editing the Platform pieces |
| `../brand/references/composition.md` | Rulers, the mascot, logo lockups, scale and the three-format family |
| `../brand/references/review-checklist.md` | Reviewing every artboard |
| `../brand/references/paper-quirks.md` | Paper tool behaviour |
