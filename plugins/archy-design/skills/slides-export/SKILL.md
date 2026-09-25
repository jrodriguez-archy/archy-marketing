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

All dumps, assets and output go in `$WORK` (`trees/ styles/ text/ assets/ dump/`). Never write inside `${CLAUDE_PLUGIN_ROOT}`: it is replaced on every update.

Every script takes its work directory from `--work DIR`, else `$ARCHY_WORK`, else `$BASE`. So `export ARCHY_WORK="$WORK"` once per session and every relative path below resolves there. Relative output paths always land in the work directory, never beside the code. Images a spec names as `assets/<file>` come from `$WORK/assets/` first and fall back to `$TOOLS/assets-base/` (the wordmark, the template-library Hugeicons and `bk-fade-dark.png`).

## 1. Preflight

1. `node --version` and `python3 --version`. If either is missing, stop and tell the user: install Node.js (nodejs.org, or `brew install node`) and Python 3 (python.org, or `brew install python`).
2. Once per machine, install the Node dependency and a Python venv:
   ```bash
   npm install --prefix "$BASE" pptxgenjs@3.12.0
   python3 -m venv "$BASE/.venv"
   "$BASE/.venv/bin/pip" install defusedxml lxml Pillow cairosvg "markitdown[pptx]"
   ```
   `build.js` finds `pptxgenjs` in `$BASE/node_modules` on its own (it also looks in `$WORK` and `$WORK/..`). Run Python with `"$BASE/.venv/bin/python"`; `export.sh` picks that venv up by itself.
3. Confirm the Paper MCP is connected and the Paper app has the file open.

## 2. Template library (Master - Decks)

The 55 layouts already have hand-written specs:

```bash
export ARCHY_WORK="$BASE/templates"
node "$TOOLS/build.js" "$TOOLS/specs.js" archy-deck-templates.pptx
"$BASE/.venv/bin/python" "$TOOLS/postprocess.py" archy-deck-templates.pptx
```

This needs no dump and no assets of its own: the images come from `$TOOLS/assets-base/`. Only run `build-assets.py` (it writes `$ARCHY_WORK/assets/`) to change or add a template icon.

## 3. A real deck

`export ARCHY_WORK="$WORK"` first. For each artboard, in deck order (`NN` = its number):

1. `open_file` with the artboard's `pageId`. Reads on an inactive page return unresolved geometry.
2. `get_screenshot` on the artboard. **If it is empty, stop**: the renderer is not running. Ask the user to close and reopen the file in Paper. Do not read coordinates until it renders.
3. `get_tree_summary` (depth 10) → save the `summary` verbatim to `$WORK/trees/NN.txt`.
4. `get_computed_styles` for every non-path id (batched) → save the `styles` object verbatim to `$WORK/styles/NN.json`.
5. For any text that may exceed 60 characters, `get_node_info` → `{id: textContent}` in `$WORK/text/NN.json`.
6. For each icon, logo or vector: `get_jsx` on the node, save it to `$WORK/jsx/<name>.jsx`, then `"$BASE/.venv/bin/python" "$TOOLS/jsx2png.py" jsx/<name>.jsx assets/deck/<name>.png [scale]` (relative paths resolve in `$WORK`). Map the SVG node id to that `assets/deck/<name>.png` in `$WORK/assets/NN.json`. Read the ink colour from the JSX; never reuse a PNG by name.
7. `"$BASE/.venv/bin/python" "$TOOLS/mkdump.py" NN <slug> "<artboard name>"` → `$WORK/dump/NN-<slug>.json`. It reads `trees/ styles/ text/ assets/` from `$WORK` (or `$WORK/scratchpad/`). It refuses if a node has no styles; fix the read, never the dump.

Then, with `ARCHY_WORK="$WORK"`:

```bash
"$BASE/.venv/bin/python" "$TOOLS/fetch-photos.py"       # Paper-hosted photos → $WORK/assets/photos
"$BASE/.venv/bin/python" "$TOOLS/make-gradients.py"     # CSS gradients → $WORK/assets/gradients (Oklab)
"$TOOLS/export.sh"            # whole deck         → $WORK/<project>.pptx
"$TOOLS/export.sh" 94         # one slide          → $WORK/<project>-94.pptx
"$TOOLS/export.sh" 66-70,94   # a subset (by dump prefix)
```

`export.sh` runs `paper2spec.js` → `build.js` → `postprocess.py` → `shrink-media.py`. All four are required. `<project>` is the name of the work directory; pass a second argument to name the file yourself. The intermediate spec is kept at `$WORK/scratchpad/specs-partial.json`.

## 4. Verify

1. `validate.py out.pptx` from the pptx skill must print `PASSED`.
2. `"$BASE/.venv/bin/markitdown" out.pptx`: every string present, character for character against Paper.
3. Unzip and confirm `lnSpc` is on **both** `<a:p>` of every merged headline, and `<a:noAutofit/>` is on every text body.
4. Tell the user to open it in Google Slides (the real renderer) and check label tracking, Ruler weight, body line breaks, and that typing a longer headline shrinks nothing.

## Rules

- Never hand-edit a saved read. They are evidence of what Paper said.
- Never derive a coordinate while the renderer is stuck.
- Two-tone headlines merge into one text box with runs; Paper keeps two nodes. That is correct.
- Charts stay drawn rectangles. Never `addChart`: Google Slides imports native charts as a flat image.
- Do not rebuild or re-send the deck unless asked. Editing a slide is not a request to export it.
- A partial build is safe only when the deck's meta carries no page number.
