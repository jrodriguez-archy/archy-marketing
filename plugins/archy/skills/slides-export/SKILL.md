---
name: slides-export
description: Generates an editable .pptx from slide artboards designed in Paper, so the team can edit copy in Google Slides or PowerPoint. Use when someone wants a Paper deck, a set of slides or the Master - Decks template library exported as a .pptx, opened in Google Slides, or made editable outside Paper.
---

# Slides export

Paper exports only images and PDF, so the `.pptx` is generated from Paper's own resolved values. Technical detail, conversions and footguns: `references/pipeline.md`.

## Paths

```bash
TOOLS="${CLAUDE_PLUGIN_ROOT}/tools/slides-export"
BASE="${CLAUDE_PLUGIN_DATA}/slides-export"
WORK="$BASE/<project>"          # short lowercase slug per deck, e.g. board-2026
```

All dumps, assets and output go in `$WORK` (`trees/ styles/ text/ assets/ dump/`). Never write inside `${CLAUDE_PLUGIN_ROOT}`.

## 1. Preflight

1. `node --version` and `python3 --version`. If either is missing, stop and tell the user: install Node.js (nodejs.org, or `brew install node`) and Python 3 (python.org, or `brew install python`).
2. Once per machine, install the Node dependency and a Python venv:
   ```bash
   npm install --prefix "$BASE" pptxgenjs
   python3 -m venv "$BASE/.venv"
   "$BASE/.venv/bin/pip" install defusedxml lxml Pillow cairosvg "markitdown[pptx]"
   ```
   Run Node with `NODE_PATH="$BASE/node_modules"` and Python with `"$BASE/.venv/bin/python"`.
3. Confirm the Paper MCP is connected and the Paper app has the file open.

## 2. Template library (Master - Decks)

The 55 layouts already have hand-written specs:

```bash
node "$TOOLS/build.js" "$TOOLS/specs.js" "$WORK/archy-deck-templates.pptx"
"$BASE/.venv/bin/python" "$TOOLS/postprocess.py" "$WORK/archy-deck-templates.pptx"
```

## 3. A real deck

For each artboard, in deck order (`NN` = its number):

1. `open_file` with the artboard's `pageId`. Reads on an inactive page return unresolved geometry.
2. `get_screenshot` on the artboard. **If it is empty, stop**: the renderer is not running. Ask the user to close and reopen the file in Paper. Do not read coordinates until it renders.
3. `get_tree_summary` (depth 10) → save the `summary` verbatim to `$WORK/trees/NN.txt`.
4. `get_computed_styles` for every non-path id (batched) → save the `styles` object verbatim to `$WORK/styles/NN.json`.
5. For any text that may exceed 60 characters, `get_node_info` → `{id: textContent}` in `$WORK/text/NN.json`.
6. For each icon, logo or vector: `get_jsx` on the node, then `jsx2png.py <in.jsx> <out.png> [scale]` into `$WORK/assets/`. Read the ink colour from the JSX; never reuse a PNG by name.
7. `mkdump.py NN <slug> "<artboard name>"` → `$WORK/dump/NN-<slug>.json`. It refuses if a node has no styles; fix the read, never the dump.

Then, from `$WORK`:

```bash
"$BASE/.venv/bin/python" "$TOOLS/fetch-photos.py"       # Paper-hosted photos
"$BASE/.venv/bin/python" "$TOOLS/make-gradients.py"     # CSS gradients → PNG (Oklab)
"$TOOLS/export.sh"            # whole deck
"$TOOLS/export.sh" 66-70,94   # a subset (by dump prefix)
```

`export.sh` runs `paper2spec.js` → `build.js` → `postprocess.py` → `shrink-media.py`. All four are required.

## 4. Verify

1. `validate.py out.pptx` from the pptx skill must print `PASSED`.
2. `markitdown out.pptx`: every string present, character for character against Paper.
3. Unzip and confirm `lnSpc` is on **both** `<a:p>` of every merged headline, and `<a:noAutofit/>` is on every text body.
4. Tell the user to open it in Google Slides (the real renderer) and check label tracking, Ruler weight, body line breaks, and that typing a longer headline shrinks nothing.

## Rules

- Never hand-edit a saved read. They are evidence of what Paper said.
- Never derive a coordinate while the renderer is stuck.
- Two-tone headlines merge into one text box with runs; Paper keeps two nodes. That is correct.
- Charts stay drawn rectangles. Never `addChart`: Google Slides imports native charts as a flat image.
- Do not rebuild or re-send the deck unless asked. Editing a slide is not a request to export it.
- A partial build is safe only when the deck's meta carries no page number.
