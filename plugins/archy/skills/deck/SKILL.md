---
name: deck
description: Build Archy presentation slides in Paper from the Master - Decks template library (55 layouts, 1920×1080). Use when someone needs a slide, a deck, or an existing deck re-set in the Archy system. For taking slides out to PowerPoint or Google Slides, use the slides-export skill.
---

# Archy decks

Load the `brand` skill first; its hard rules and workflow apply here unchanged.

## Source

Paper file `Master - Decks` (`app.paper.design/file/01M1HZF1EW0RX9H3YSMJ3GAMK7`): 55 layouts on one page per content category (Frames · Numbers · Charts · Lists · Comparisons · Proof · Showcase). Pick a layout by the **content in hand** ("three stats and a claim"), using `references/layout-catalog.md`.

## Starting point: two paths

1. **Redesigning an existing deck** (the usual case). The requester creates a folder inside their Claude working folder, for example `Decks/<deck name>/`, and puts the source `.pptx` and its `.pdf` in it. Read both before anything else:
   - The `.pdf` is the visual truth. Render pages with `pdftoppm -png -r 96 <file>.pdf <folder>/page` to look at them.
   - The `.pptx` holds the exact copy. Extract every `<a:t>` run per slide; that text is what gets transcribed.
   - For each source slide, pick the Master - Decks layout that holds its content shape, and list the mapping (source slide → layout) for the requester to confirm before building.
2. **A new deck from the templates** (less common). Ask for the content slide by slide, pick layouts by content shape, and build from the masters the same way.

Either way, every slide starts as a duplicate of a Master - Decks layout. If no layout fits a source slide exactly, take the closest one and adapt it (more rows, a column less, a different split), keeping the header, Rulers and type scale, and note it in the mapping.

## Deck-specific rules

1. **Content is transcribed, never authored.** When re-setting an existing deck, copy is the source's character for character. Verify against the `.pptx` text before finishing.
2. **Every slide carries the three-part header**: eyebrow, meta line, two-tone headline (two stacked text nodes).
3. **Canvas 1920 × 1080, margins 96**, type from the slide scale. When copy does not fit, stack it or rewrap it first; step type down only as a last resort, and report it.
4. **Rulers frame** at y 20 / 344 / 1056 plus column verticals, solid colour for the ground.
5. **Charts are drawn from frames**, with bar heights derived from the data. Never eyeball a data mark.
6. **A dark slide is a beat, not a recolour.** Use a dark layout only where the deck needs punctuation.
7. **Rename a duplicated slide first.** Its name carries its position in the deck.

## References: read on demand

| File | Read it when |
|---|---|
| `references/slide-system.md` | Always, before touching a slide: canvas, type scale, header, Rulers, lanes, bands, icons, status pill |
| `references/layout-catalog.md` | Choosing a layout; image and logo slots |
| `references/dark-set.md` | Working on a dark layout |
| `references/charts.md` | Any chart, plot, waterfall or sizing diagram |
| `../brand/references/review-checklist.md` | Reviewing every slide |
| `../brand/references/paper-quirks.md` | Paper tool behaviour |

When the slides are done and the requester wants them in Google Slides or PowerPoint, hand over to the `slides-export` skill.
