# Figma Export

Publishes a Paper artboard into Figma as **real Figma nodes** - Frames with
auto-layout, editable Text, vectors, and colour Variables. Not an image, not a
flattened SVG.

**Nothing here is specific to a project.** The payload declares which colours
and fonts the artboard uses; the plugin reads whatever Figma file it is running
in and proposes a mapping, which the person importing can change before anything
is created. Hand the `plugin/` folder to anyone - it works on their design, their
palette, their fonts.

It is a **one-way publish**, not a sync. Paper stays the source of truth; edits
made in Figma do not come back.

## Running it through the plugin

This folder ships inside the `archy-design` plugin. The `figma-export` skill holds
the agent-facing workflow: with the **Paper MCP** connected (the only requirement;
the Figma MCP is not a substitute for it), ask Claude to export an artboard from
Paper to Figma and the skill takes it from there.

## Paths

The plugin folder is replaced on every update, so **nothing is written here**.
`build.js` works in a work directory: `--work DIR` (or `--work=DIR`), else
`$ARCHY_WORK`, else `$ARCHY_WORK_BASE`, else `${CLAUDE_PLUGIN_DATA}/figma-export`,
else `./archy-work/figma-export`. A relative input path is tried in the current
directory first, then in the work directory. The default token file is
`<work>/tokens.json`, and the payload is always written to `<work>/payloads/`.

Figma remembers the manifest's path, and the plugin folder moves on every update,
so copy `plugin/` into the data directory once and import it from there:

```bash
mkdir -p "${CLAUDE_PLUGIN_DATA}/figma-export"
cp -R "${CLAUDE_PLUGIN_ROOT}/tools/figma-export/plugin" "${CLAUDE_PLUGIN_DATA}/figma-export/figma-plugin"
```

Re-copy after a plugin update if `plugin/` changed.

---

## Why it works

Paper has already resolved the layout. `get_jsx` returns the whole subtree in
one call - structure, text, raw SVG, and every style as a Tailwind class on the
4px scale (`w-160` = 640, `px-8` = 32, `leading-8.5` = 34). Colours come through
as token names when the file uses tokens (`bg-navy-panel`) and as plain values
when it does not (`bg-[#001797]`) - both are handled.

So this never re-implements flexbox. It reads the authored intent -
direction, gap, padding, alignment, grow/shrink - and hands Figma the
equivalent auto-layout.

---

## Running it

**1 · Pull the two reads for one artboard** (Claude does this through the Paper MCP):

```
get_jsx(nodeId)                     -> raw/<name>.jsx
get_tree_summary(nodeId, depth 10)  -> raw/<name>.tree
```

Both come from the same traversal, so they zip positionally: the JSX carries the
styles, the tree carries layer names and node ids.

**2 · Build the payload**, pointing at the token list for that Paper file
(`get_tokens` -> `tokens/<file>.json`; omit it and colours travel as plain values):

```bash
export ARCHY_WORK="${CLAUDE_PLUGIN_DATA}/figma-export/<project>"
node "${CLAUDE_PLUGIN_ROOT}/tools/figma-export/build.js" raw/<slug>.jsx raw/<slug>.tree --tokens=tokens/<slug>.json
```

Writes `<work>/payloads/<slug>.json` - the tree, plus a manifest of **only the
colours and fonts this artboard actually uses**, so nobody is asked to map a
whole design system to import one poster.

**3 · Import in Figma:** `Plugins → Development → Import plugin from manifest…`
and pick `figma-plugin/manifest.json` from the data directory (once; see *Paths*). Run **Paper Import**, paste the payload,
press Continue.

**4 · Map, then build.** The plugin lists every colour and font in the payload
against what the target file already has:

- **Colours** - each one is matched to an existing Variable by name, then by
  value, and pre-selected if found. Otherwise you choose: bind it to any
  variable in the file, create it (in an existing collection or a new one you
  name), or paint it as a plain colour with no variable at all.
- **Fonts** - each family maps to any font installed in that file. Weights find
  their closest available style, and the plugin reports every substitution
  rather than doing it silently.

Then press Build.

---

## What crosses over

| Paper | Figma |
|---|---|
| Frame with `display: flex` | Frame with auto-layout - direction, `itemSpacing`, padding, both alignments |
| `flex-grow: 1` | `layoutSizingHorizontal/Vertical = 'FILL'` |
| `flex-shrink: 0` + fixed width | `FIXED` |
| No `align-items` (CSS stretch) | Child fills the counter axis |
| Absolute child inside a flex parent | `layoutPositioning = 'ABSOLUTE'` at Paper's coordinates |
| Text | **Editable** TextNode - family, weight, size, line-height, tracking, alignment |
| SVG node | Vector, via `createNodeFromSvg` |
| One-sided dashed rule | Stroke with per-side weight + `dashPattern` |
| `--color-*` tokens | Existing Variables, new ones, or plain colours - your choice per colour |
| Raw colours (a file with no tokens) | Plain paints; `bg-[#001797]` works as well as `bg-navy-panel` |

## What does not

- **Components.** Paper clones could map to instances; deliberately out of scope.
- **Gradients.** Detected and reported, not painted. `build.js` warns at build
  time and the plugin warns again at import, so a gradient never disappears
  quietly. Anything whose ground is a `linear-gradient` needs this first.
- **Images.** Would have to travel as bytes in the payload.

---

## Two things that will bite

**The silent-bad-geometry failure.** When Paper's canvas is not rendering, reads
come back unresolved and every child reports `0,0` - with no error. A payload
built on that looks plausible and is garbage. `build.js` refuses to write when it
sees the tell (a padded frame whose first child sits at the origin). If it aborts,
bring the Paper file to the front and re-read; do not work around it.

**Font metrics.** Text is the one thing that can drift, because Figma wraps with
its own metrics. Anything with a fixed width comes across as `HEIGHT` auto-resize
so the box holds; anything hugging may take a different line. Check text-dense
artboards after import. A font the target file does not have is never silently
swapped: you pick the replacement in the mapping step, and any weight that has
no exact match is reported.

Anything on Google Fonts resolves in Figma. A licensed desktop font that is not
installed in the Figma file will not, and you will be asked to choose a
replacement rather than getting one silently.

---

## Files

```
build.js            JSX + tree -> payload. No dependencies, plain Node.
plugin/             manifest.json · code.js · ui.html
example/            A complete worked run, to try the plugin against.
```

In the work directory:

```
raw/                Where the MCP reads get saved. Starts empty.
tokens/             One file per Paper file, straight from get_tokens.
payloads/           What you paste into the plugin.
```

`plugin/` is self-contained. It reads a payload and the file it is running in,
and knows nothing else.

## Status

Validated end to end on a 49-node poster: no unmapped classes, and a manifest of
exactly the colours and fonts that artboard uses.

`example/` holds a small self-contained run - the two raw reads, a token file
and the payload they produce. Paste `example/payload.json` into the plugin to
see it work before wiring up your own file. It mixes tokens with raw hex on
purpose, so both paths get exercised.

**The Figma side has not been run yet** - the plugin is written but needs its
first import in a real file. Expect the first pass to turn up small sizing
fixes; that is what the warning list is for. It never fails silently: every
substitution, every unmappable colour and every unsupported fill is reported
back in the UI.
