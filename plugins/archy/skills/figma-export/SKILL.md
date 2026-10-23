---
name: figma-export
description: Publishes a Paper artboard into Figma as real, editable nodes (auto-layout Frames, editable Text, vectors, colour Variables) by building a JSON payload for the bundled Paper Import plugin. Use when someone wants a Paper design moved, copied, exported or handed off into Figma.
---

# Figma export

A **one-way publish**, not a sync: Paper stays the source of truth, and edits made in Figma do not come back. Mapping table, reasoning and limits: `references/mapping.md`.

## Paths

```bash
TOOLS="${CLAUDE_PLUGIN_ROOT}/tools/figma-export"      # build.js, plugin/
WORK="${CLAUDE_PLUGIN_DATA}/figma-export/<project>"   # raw/ tokens/ payloads/
```

Never write reads or payloads inside `${CLAUDE_PLUGIN_ROOT}`: it is replaced on every update. `build.js` takes its work directory from `--work DIR`, else `$ARCHY_WORK`, else `${CLAUDE_PLUGIN_DATA}/figma-export`, and always writes the payload to `<work>/payloads/<slug>.json`. Relative input paths are tried in the current directory, then in the work directory. `export ARCHY_WORK="$WORK"` once per session.

## 1. Preflight

1. `node --version` must answer. If not, tell the user to install Node.js (nodejs.org, or `brew install node`). `build.js` has no dependencies.
2. The **Paper MCP** (`paper-desktop`) must be connected, and the Paper app open with the file visible. If the MCP is missing, say so plainly: no payload can be generated without it. The Figma MCP is not a substitute; it is read-only and plays no part here.

## 2. Ask for two things only

1. **Which Paper file**: a name or a URL.
2. **Which artboard**: a name. If unknown, list artboards from `get_basic_info` and let the user pick.

Ask for anything missing; do not guess.

## 3. Read

1. `open_file`, then `get_basic_info`. If the artboard is on another page, open that page too: reads on an inactive page return unresolved geometry.
2. `get_screenshot` on the artboard. **If it is empty, stop.** Paper is not rendering and every coordinate read after that is wrong with no error. Ask the user to bring the Paper window to the front, or to close and reopen the file, then retry.
3. Pick a short lowercase slug (`cover`, `poster-tue`, `badge-front`) and use it throughout.
4. `get_jsx` on the artboard → save the `jsx` string verbatim to `$WORK/raw/<slug>.jsx`.
5. `get_tree_summary` on the same node, `depth: 10` → save the `summary` string verbatim to `$WORK/raw/<slug>.tree`. The two come from the same traversal and zip positionally; do not reformat, re-indent or tidy either.
6. `get_tokens` (or the `tokens` block of `get_basic_info`) → save verbatim to `$WORK/tokens/<slug>.json`. Every response shape is understood, including `{ "items": [ … ] }` with `--color-` prefixes. Skip if the file has no tokens; colours then travel as plain values.

## 4. Build

```bash
export ARCHY_WORK="$WORK"
node "$TOOLS/build.js" raw/<slug>.jsx raw/<slug>.tree --tokens=tokens/<slug>.json
```

The payload lands at `$WORK/payloads/<slug>.json`.

The payload holds the tree plus a manifest of **only the colours and fonts this artboard uses**.

## 5. Report

Show the full output, **every warning included** (colours with no value, gradients). Tell the user the payload path, then the Figma steps, which only they can do (the plugin runs inside Figma and the Figma MCP cannot create nodes):

1. Once: copy the Figma plugin out of the plugin folder, because Figma remembers the manifest's path and `${CLAUDE_PLUGIN_ROOT}` moves on every update:
   ```bash
   mkdir -p "${CLAUDE_PLUGIN_DATA}/figma-export"
   cp -R "$TOOLS/plugin" "${CLAUDE_PLUGIN_DATA}/figma-export/figma-plugin"
   ```
   Then in Figma: **Plugins → Development → Import plugin from manifest…**, pick `${CLAUDE_PLUGIN_DATA}/figma-export/figma-plugin/manifest.json` (give the user the expanded path). Re-copy after a plugin update if `plugin/` changed.
2. Run **Paper Import**, paste the payload, press Continue.
3. Map each colour and font. Colours are pre-matched to existing Variables by name, then by value; anything unmatched can be bound to any variable, created fresh, or painted plain. Fonts map to any installed font; weight substitutions are reported.
4. Press Build.

Say up front: gradients are reported, not painted; images do not travel; components arrive as plain frames; text can rewrap, so eyeball text-heavy artboards after import.

## Rules

- **Never hand-edit a file in `raw/`.** They are evidence of what Paper said; if the build fails, the fix is upstream.
- **If `build.js` refuses to write, stop and tell the user.** It aborts when geometry looks unresolved (a padded frame whose first child sits at `0,0`), the signature of a canvas that was not rendering. Do not edit the raw files to get past the check, and do not disable it.
- **Report warnings, do not swallow them.**
- To see the output shape first, `$TOOLS/example/payload.json` is a complete run that pastes straight into the plugin.
