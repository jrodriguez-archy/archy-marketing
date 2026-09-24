# Figma export: how it works and what crosses over

Read this when a Figma import looks wrong, when someone asks what the export can and cannot carry, or before changing `build.js` or the plugin.

## Why it works

Paper has already resolved the layout. `get_jsx` returns the whole subtree in one call: structure, text, raw SVG, and every style as a Tailwind class on the 4px scale (`w-160` = 640, `px-8` = 32, `leading-8.5` = 34). Colours come through as token names when the file uses tokens (`bg-navy-panel`) and as plain values when it does not (`bg-[#001797]`); both are handled.

So the export never re-implements flexbox. It reads the authored intent (direction, gap, padding, alignment, grow/shrink) and hands Figma the equivalent auto-layout.

**Nothing in the tool is project-specific.** The payload declares which colours and fonts the artboard uses; the plugin reads whatever Figma file it is running in and proposes a mapping, which the person importing can change before anything is created. It works on any design, palette and fonts. `plugin/` is self-contained: it reads a payload and the file it is running in, and knows nothing else.

## What crosses over

| Paper | Figma |
|---|---|
| Frame with `display: flex` | Frame with auto-layout: direction, `itemSpacing`, padding, both alignments |
| `flex-grow: 1` | `layoutSizingHorizontal/Vertical = 'FILL'` |
| `flex-shrink: 0` + fixed width | `FIXED` |
| No `align-items` (CSS stretch) | Child fills the counter axis |
| Absolute child inside a flex parent | `layoutPositioning = 'ABSOLUTE'` at Paper's coordinates |
| Text | **Editable** TextNode: family, weight, size, line-height, tracking, alignment |
| SVG node | Vector, via `createNodeFromSvg` |
| One-sided dashed rule | Stroke with per-side weight + `dashPattern` |
| `--color-*` tokens | Existing Variables, new ones, or plain colours, chosen per colour |
| Raw colours (a file with no tokens) | Plain paints; `bg-[#001797]` works as well as `bg-navy-panel` |

## What does not

- **Components.** Paper clones could map to instances; deliberately out of scope.
- **Gradients.** Detected and reported, not painted. `build.js` warns at build time and the plugin warns again at import, so a gradient never disappears quietly. Anything whose ground is a `linear-gradient` needs attention first. Note that both Archy artboard grounds are gradients.
- **Images.** Would have to travel as bytes in the payload.

## The mapping step in Figma

- **Colours:** each is matched to an existing Variable by name, then by value, and pre-selected if found. Otherwise the importer chooses: bind it to any variable in the file, create it (in an existing collection or a new named one), or paint it as a plain colour with no variable.
- **Fonts:** each family maps to any font installed in that file. Weights find their closest available style, and the plugin reports every substitution rather than doing it silently.

## Two things that will bite

**Silent bad geometry.** When Paper's canvas is not rendering, reads come back unresolved and every child reports `0,0`, with no error. A payload built on that looks plausible and is garbage. `build.js` refuses to write when it sees the tell (a padded frame whose first child sits at the origin). If it aborts, bring the Paper file to the front and re-read; do not work around it. See `brand/references/paper-quirks.md` for the full renderer diagnostic.

**Font metrics.** Text is the one thing that can drift, because Figma wraps with its own metrics. Anything with a fixed width comes across as `HEIGHT` auto-resize so the box holds; anything hugging may take a different line. Check text-dense artboards after import. A font the target file does not have is never silently swapped: the importer picks the replacement, and any weight with no exact match is reported. Anything on Google Fonts resolves in Figma; a licensed desktop font not installed in the Figma file will not.

## Tool layout

```
build.js     JSX + tree -> payload. No dependencies, plain Node.
plugin/      manifest.json · code.js · ui.html
example/     sample.jsx · sample.tree · tokens.json · payload.json
```

`example/` is a small self-contained run: the two raw reads, a token file and the payload they produce. It mixes tokens with raw hex on purpose, so both paths get exercised. Paste `example/payload.json` into the plugin to see it work before wiring up a real file.

## Status

Validated end to end on the Paper side on a 49-node poster: no unmapped classes, and a manifest of exactly the colours and fonts that artboard uses.

**The Figma side has not been run in a real file yet.** Expect the first pass to turn up small sizing fixes; that is what the warning list is for. It never fails silently: every substitution, every unmappable colour and every unsupported fill is reported in the UI.
