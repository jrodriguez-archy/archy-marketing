---
name: video
description: Create Archy video graphics in Paper from the Master - Videos file (openers, titles, chapters, lower thirds, highlights, subtitles, quotes, product screens, diagrams and end cards in Royal, Navy and Ice, plus 1080×1920 vertical and 1080×1350 feed sets; every over-footage template has a transparent Overlay twin), and animate them in the Archy motion language (stepped stop-motion, pixel wipes). Use when someone needs an on-screen graphic or its animation for an Archy product, marketing or social video, a vertical or 4:5 cut, highlights or subtitles over a speaker, or wants to explore a video graphic the catalog does not have. Not for DOC videos (doc-video).
---

# Archy video graphics

Load the `brand` skill first and follow it: never touch the master, tokens only, Onest + Inter (Open Sans for product UI), English on the canvas, never invent facts, deliver and report.

**Master:** `Master - Videos` (`app.paper.design/file/01M61VK85Z6JC0BQQY1E8SBSZ3`). Three pages:

| Page | What it is |
|---|---|
| `Guidelines` | The system on slides: themes, type, grid, pixel transitions, text motion, product on screen, talking head, structure, pixels and moons, template map, motion, highlights and subtitles |
| `Templates` | The finished templates, one block per type (below). Fill copies of these |
| `Components` | Where new pieces are designed and approved before they become templates. Nothing goes into `Templates` that was not approved here first |

Read positions with `get_basic_info`, not from this file: the canvas gets rearranged by hand.

## How Templates is organised

One block per type, stacked top to bottom in the order they appear in a video. Each block opens with a `§` label artboard at x 0, templates run left to right every 2000px (1240px in the vertical block), and the rows are **Royal, Navy, Ice**. Templates that sit on footage have an `· Overlay` twin (transparent, no footage) directly under each theme row. Artboards are named `<Code> · <Name> · <Theme>` (`· Overlay` at the end of the twin).

| Block | Codes |
|---|---|
| O · Openers | O1 to O6 |
| T · Titles | T1 to T9 |
| CH · Chapters | CH1, CH2 |
| LT · Lower Thirds | LT1 |
| HL · Highlights | HL1, HL2 |
| Q · Quotes | Q1 |
| P · Product | P1 to P14 |
| D · Diagrams | D1 to D10 |
| E · End Cards | E1 to E4 |
| V · Vertical (1080 × 1920) | V1 to V8 |
| F · Feed (1080 × 1350) | F1 to F8 |
| SB · Subtitles | SB1 (16:9), SB2 (vertical), SB3 (feed), in White and Yellow instead of themes |

What each one holds: `references/template-catalog.md`.

## Highlights or subtitles

Two different kinds of text over a speaker; never call either one "captions".

- **Highlights** (HL, V5, F5): a short point that backs up what the speaker says, not their words, on royal bars on the left margin.
- **Subtitles** (SB): the literal speech, small and centred near the bottom, no box, Onest Medium in white or `subtitle-yellow` (a video-only token in Master - Videos; never for titles, highlights or other graphics). They never overlap a highlight or a lower third.

## Steps

1. **Pick the template by what the moment says** (`references/template-catalog.md`). If the requester named one or has it selected (`get_selection`), use it. If the video has no theme yet, Royal opens and closes it and Navy and Ice alternate in between (`Guidelines` › Structure).
2. **Make the working copy.** Duplicate the master file as `brand` describes, or work on a page named after the video in a file the requester chooses, and `duplicate_nodes` the templates in the order they appear in the video, each with its `· Overlay` twin when it has one. Never edit `Templates` or `Components` in the master.
3. **Get the facts once**: wording, figures, names, roles, URL. A fact that does not exist comes out with its label; one that is pending gets a visible placeholder.
4. **Fill and adapt** (`references/video-system.md`): set the `slot-*` layers, keep the template's type sizes (rebreak a long line before shrinking it), and make the same change in the Overlay twin.
5. **Review** every artboard with `brand` › `review-checklist.md` plus the video checks in `video-system.md`.
6. **Deliver**: the artboards, the template each came from, the copy used, anything adjusted beyond the slots, and what is pending.

## Motion

When the graphics are animated (After Effects is the reference tool), follow `references/motion.md`: stepped stop-motion at 10 steps a second, words that rise out of a blur, the text life rule, text masked by its box, scenes that hold still until a pixel wipe covers them, and the four wipes.

Exports are the requester's call. Video editors take PNG; Overlays keep their transparency only as PNG. Paper saves to `~/Downloads`.

## Exploring a new graphic

When nothing in the catalog carries the moment, design it on the `Components` page of a copy (Royal first, built from the approved pieces in `video-system.md`) and say it is an exploration. Once approved it moves to `Templates` in all three themes; a graphic the team will reuse goes into the master with `prepare-template`.

## References

| File | Read it when |
|---|---|
| `references/template-catalog.md` | Choosing a template, and what each one holds |
| `references/video-system.md` | Filling or adapting any artboard: themes and recolouring, grid and safe zones, type, pixels, the moon spiral, product UI, QR codes, highlights and subtitles, the vertical and feed formats, the review checks |
| `references/motion.md` | Animating any of it: rhythm, text arrival, text life, boxes, holds, transitions, highlight and subtitle timing, After Effects notes |
| `../brand/references/voice.md` | Shortening on-screen copy |
