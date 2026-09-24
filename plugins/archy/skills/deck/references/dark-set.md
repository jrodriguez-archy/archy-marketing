# The Dark Set

Read this when deciding whether a slide should sit on a dark ground, building one of the thirteen dark layouts, or colouring a chart or image slot on navy.

The dark layouts are marked **◆** in `layout-catalog.md`. The dark-ground header mapping (eyebrow, headline, meta, Rulers, body) is in `slide-system.md`; the solid-Rulers rule in `../../brand/references/composition.md`.

---

## What earns a dark slide

Thirteen of the fifty-five layouts sit on `--color-dark-background`, and they exist for one reason: **a dark slide is a beat in the deck, not a page of information.** It is punctuation between light sections. `Big Number` and `Matrix` were dark long before the set was filled out, and both are stop-and-look slides; that is the pattern, not a coincidence.

**That test is strict, because a dark version of an existing layout is a free recolour.** The header inversion on a dark ground is a fixed mapping, so re-grounding `Metrics 2×2` costs nothing and produces nothing. Every dark layout in the library is therefore a *distribution* that does not exist on light:

| Layout | Distribution |
|---|---|
| `Manifesto` | Ink in the lower two thirds |
| `The Ask` | Anchored top and bottom with a void between |
| `Number Full-bleed` | Type as the whole image |
| `Platform Stack` | Bands of unequal height |
| `Key-value rows` | Right-aligned value lanes |
| `The Wedge` | Radial |
| `Cost Stack` | Horizontal stacked bars |
| `Capture + Scrim` | Copy on a scrim |
| `Screen Trio` | Portrait slots |

---

## The ground

**The ground is flat navy, not the dark gradient.** The brand defines a dark gradient ground for posters and it is open to explore on a slide, but `pptxgenjs` supports no gradient fills at all: a gradient ground would go into the `.pptx` as a background image on every dark slide and stop being an editable shape. Flat `--color-dark-background` exports as a real solid fill. The one place a raster is unavoidable is `Capture + Scrim`'s `BK Fade`, and that is one image rather than thirteen.

---

## Colour on navy

**Chart series steps are `--color-sky-blue-400` / `--color-blue-tint-300` / `--color-blue-tint-200`.** This is the exact inverse of the light rule and it has the same cause: `--color-royal-blue-500` is the forecast colour on white and it *disappears* against navy, the way a `--color-blue-tint-200` stroke nearly vanishes on white. Brightest step is the newest or most important series. (Light-ground chart colours are in `charts.md`.)

**An image slot fills `--color-neutral` (#666666), not `--color-neutral-lightest`.** #EEEEEE is the light-ground slot fill; on navy three of them read as three white slabs that become the subject of the slide instead of placeholders. Same reasoning that already sends a full-bleed slot to #666666 (see `layout-catalog.md`).

**A five-step blue ramp exists and only `Cost Stack` uses it:**

| Step | Token |
|---|---|
| 1 | `--color-primary-blue-600` |
| 2 | `--color-royal-blue-500` |
| 3 | `--color-sky-blue-400` |
| 4 | `--color-blue-tint-300` |
| 5 | `--color-blue-tint-200` |

Reach for it only when a chart genuinely has five parts to separate; the ordinary stacked bar uses three. The two lightest steps need their labels inverted to `--color-blue-tint-800`.
