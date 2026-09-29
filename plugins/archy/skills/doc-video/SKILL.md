---
name: doc-video
description: Create DOC (Dental Ownership Collective) video graphics in Paper from the DOC - Videos Foundations master (55 templates at 1920×1080 in eight sections, every split or over-footage template with a transparent Overlay twin). Use when someone needs an on-screen graphic for a DOC course video (title card, lower third, caption, list, quote, figure chain, equation, chart, diagram, icon tiles, hero illustration), a new variant of one, or wants to explore a graphic the catalog does not have.
---

# DOC video graphics

Load the `doc-brand` skill first and follow it: never touch the master, tokens only, Satoshi, the lockup from the file, never invent facts, deliver and report.

**Master:** `DOC - Videos Foundations` (`app.paper.design/file/01M3N7N1T2X0H9Z9Y4FFKAD364`), page `Video`. It was rebuilt from the Foundations course videos and the editor's own source files, so it is the reference for how DOC videos look. The `Video` page holds templates only: one row per section (S Structure, L Lower Thirds, T Text and Lists, N Numbers, C Charts, D Diagrams, I Icons, H Heroes), each opened by a `§` label artboard. Artboards are named `<Code> · <Name>`, with `· Overlay` on the transparent twin, which sits directly below its template. `A · Assets` holds the lockups and the icon library. Read positions from `get_basic_info`, not from this file: the canvas gets rearranged by hand.

## The rule that matters most

**Stay inside what the videos show.** The graphics are edited into footage that already exists, so a template must look like the moments already on screen. Only the layout seen in the videos exists: a split graphic is not redrawn as full screen or the other way round, and there are no invented transitions, wipes or outros. When a message needs something the catalog cannot hold, say so and propose it as an exploration (below).

## Steps

1. **Pick the template by what the moment says**, using `references/template-catalog.md`: a list, a quote, a figure that leads to others, a chart, a concept, a set of icons, one drawing. If the requester named a template or has it selected in Paper (`get_selection`), use it.
2. **Pick the layout that template has.** Split templates keep the speaker in the left half; they come with an `· Overlay` twin, which is the one the editor uses over footage. Full-screen templates cut away from the speaker.
3. **Make the working page.** The team works one page per video in the master file: `create_page` named after the video (for example `F3.4 · Owner Compensation`), then `duplicate_nodes` the templates the video needs onto it (`parentId` = that page's root), both the template and its Overlay twin, in the order they appear in the video. Never edit the `Video` page itself. When the requester prefers a separate file, make a copy as `doc-brand` describes instead.
4. **Get the facts once**: the exact wording, figures, labels and names from the script or the requester. A figure that does not exist comes out of the graphic; one that is pending gets a visible placeholder.
5. **Fill and adapt**, following `references/video-system.md`:
   - set the copy (`set_text_content`, `\n` for breaks) and keep the type sizes of the template; a longer line gets a new break before it gets a smaller size;
   - chains, lists and icon rows take the number of items the moment needs: duplicate or delete items and re-space them with the template's own gap;
   - chart geometry comes from the data (bar widths, donut arcs, line points), never eyeballed;
   - swap icons by cloning `Icon · <name>` from `A · Assets` and resizing its inner SVG too;
   - make the same change in the `· Overlay` twin.
6. **Review** every artboard with `doc-brand` › `review-checklist.md`, plus the video checks in `video-system.md`.
7. **Deliver**: the file and artboards, the template each started from, the copy used, anything adjusted beyond the copy, and what is still pending.

Exports are the requester's call. Video editors need PNG at 1x; Overlays keep their transparency only as PNG. Paper saves to `~/Downloads`.

## Exploring a new graphic

When nothing in the catalog carries the moment, propose a new graphic and say it is an exploration. Build it from the pieces the videos already use (video-ground ground, cream-100 boxes, cream-200 tiles, red-500 result boxes, red-400 bullets, the connector line with its red dot, 3.5px icon strokes) and in the layout the moment calls for. A graphic the team will reuse goes into the master with `archy-design:prepare-template`.

## References

| File | Read it when |
|---|---|
| `references/template-catalog.md` | Choosing a template, and what each one holds |
| `references/video-system.md` | Filling or adapting any artboard: frame, split, over footage and Overlay, colour, type, boxes, icons, heroes, turning an editor's source file into templates, Paper notes, the video review checks |
| `../doc-brand/references/voice.md` | Shortening on-screen copy |
