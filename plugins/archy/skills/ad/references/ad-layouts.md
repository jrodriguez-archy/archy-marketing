# Ad layouts: person-led social ads

Read this when building or adjusting a social ad that puts a person (an Account Executive, a speaker, a team member) next to a headline, a short benefit list and a CTA, such as the AE Spotlight Post 1080 × 1080 in the `Archy - Ads` file, page `AE Spotlights`. Every rule here came out of a design review of those options; together they describe how a reviewed ad column is built.

Base rules (tokens, Rulers, scale, the mascot) live in `../../brand/references/composition.md`. This file only adds what is specific to ads.

---

## Starting from an AI mockup

- **An AI mockup is a concept, not a layout to recreate.** When a request arrives with a ChatGPT (or similar) image, take the idea and the required elements from it, then propose 2 or 3 directions that differ in ground, composition and what leads. A faithful rebuild of the mockup is the weakest option.
- **Break the brief down first.** List what is required (real photo, name, title, headline, benefits, CTA, logo) and what is optional (the mascot, the device, the region). The product is always a real screenshot; it does not have to sit inside a laptop. A crop, a tile or a screen bleeding off the edge all work.
- **Never set a name in a handwritten font with a curved arrow pointing at the person.** It reads as AI output. Show the name in brand type and let its position (a grid cell next to the portrait, a plate on the photo, a tile under it) make the connection.

## The column

- **Three anchors: logo at the top, CTA at the bottom, one `Main` block in between.** Group the headline and the benefit list in a single `Main` frame (gap 64) and let the column's `justify-content: space-between` share the remaining space above and below it. Spreading the headline, the list and the CTA as three separate blocks leaves the headline floating away from the list it introduces.
- **The logo may sit tight to the headline** (about 28px) when the two form a masthead. The gap between groups stays larger than the gaps inside them.
- **Children fill their container.** Give the headline, the list and the list's Rulers `width: 100%` instead of a fixed width, so a designer can resize the column by hand and everything reflows.
- **Leave hand edits alone.** Designers adjust these artboards between rounds. Read the current state before editing and change only what was asked; when a change does not fit, propose the trade-off instead of shrinking something else.

## The headline

- **Size it for the column it has.** A headline sharing the canvas with a photo lives in roughly half the width: 76 to 84px in Onest Medium is the working range there, and four large lines (`Meet your / local Archy / platform / expert.`) beat three small ones. Push toward the 100px Post minimum in `composition.md` whenever the column allows it.
- **Use the width you have.** When the headline sits in a full-width cell, let it run (`Meet your local Archy / platform expert.`) instead of breaking lines early.
- **Centre it optically in its cell,** and open the leading slightly when it runs four lines (about 81 on 76) so the block breathes.
- **Accent one phrase, not the whole line.** Paper cannot colour part of a text node, so the accent phrase is its own node in a flex row.

## Benefit lists with icons

- **Icon loose, no circle:** Hugeicons at 36px in the accent colour for the ground.
- **Copy:** Inter Medium 28/36, one line per item.
- **Rows:** 18 to 24px of padding per row, with a solid Ruler between rows (never above the first or below the last), running the full width of the column.
- **Inside grid cells,** pad each cell symmetrically (the same left and right) and centre its content vertically; text pressed against one Ruler with a wide gap on the other side reads as a mistake.
- **When an item does not fit on one line,** shorten the copy (with the requester's approval) before shrinking anything else.

## The CTA button

Build it as the website's primary button (`.button_v2`): `--color-royal-blue-500` fill, white Inter Medium 30/36, `border-radius: 16px` (the poster correction of the 8px button radius), padding 22 / 32, gap 16, Hugeicons `ArrowRight02` at 28px with stroke 2. Not a pill. On a royal blue ground invert it: white fill, royal blue label and arrow.

## Photo and name

- **The photo dominates.** In a stacked photo + name tile, give the photo about 880 of the 1080px and the name tile only the height it needs.
- **Share the CTA's baseline.** Name, title and name plates rest on the same bottom line as the CTA (y 1008 on a 1080 Post), so the bottom of the piece reads as one row across the seam.
- **A photo may fill its grid cell flush to the Rulers**: the photo is the cell. This is the one place content meets a Ruler.

## Pixel Effects on portraits

A portrait on a gradient ground can take the pixel grain: **Pixel Dissolve** when the person bleeds off the bottom, **Pixels Behind** when the crop is a tight square. Generate them with the `archy-design:pixel` skill (`effect dissolve`, `effect behind`), never by hand. The cells start below the face, the chest and any logo on the clothes; the gradient behind shares their grid, so the piece has one grain; and a white plate over light cells keeps its colour and takes a 2px `--color-blue-tint-300` border. Cell size, colours and density are a starting point: tune them to the piece.

## The arch frame

- **The arch is a true semicircle,** like the curve of the Archy "A": `border-radius` of half the width on both top corners. Unequal radii read as a distorted logo.
- **It may bleed off the right and bottom trims.** Centre whatever sits on it (the name plate, the placeholder) on the visible part of the arch, not on the full shape.

## Grid layouts

- **Side verticals run the full height, trim to trim.** A vertical that stops short of the top or bottom edge reads as unfinished; horizontals stay full bleed.
- **Reorder rows by weight:** headline row, then the benefit row, then the portrait row with name, title and CTA together, so the photo can bleed off the bottom trim.
