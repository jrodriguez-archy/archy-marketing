---
name: hugeicons
description: Extracts Hugeicons Stroke Rounded icons from the free npm package and places them in a Paper file as correctly styled SVG (24 grid, stroke 1.5, round caps, token colour). Use when a design, slide or template needs an icon, or when replacing Phosphor, Font Awesome or other off-system icons.
---

# Hugeicons into Paper

Archy's icon set is **Hugeicons Stroke Rounded**. No install and no MCP server are needed: `@hugeicons/mcp-server` is search-and-docs only and returns no geometry. Work in `${CLAUDE_PLUGIN_DATA}/hugeicons/` (call it `$WORK`).

## Spec

| | |
|---|---|
| Style | Stroke Rounded |
| Grid | 24 × 24, `viewBox="0 0 24 24"` |
| Stroke | `stroke-width: 1.5`, `stroke-linecap: round`, `stroke-linejoin: round`, `fill="none"` |
| Colour on canvas | A token set explicitly on the `<svg>` or its paths. `currentColor` does not resolve through a parent frame in Paper; keep `currentColor` for shipped code only |
| On a slide | **40px**, not 32 (32 reads timid next to a 30px title). Stroke stays 1.5 |
| Slide colour | `--color-royal-blue-500` on light, `--color-blue-tint-300` on dark, `--color-neutral-light` for a secondary or not-yet-shipped state |

The live site still carries Phosphor, Font Awesome and loose 16/20px grids as drift. Replace them as surfaces are touched.

## 1. Get the package (once)

```bash
mkdir -p "$WORK" && cd "$WORK"
URL=$(npm view @hugeicons/core-free-icons dist.tarball)      # v4.3.0, MIT, 6,025 icons
curl -sL "$URL" -o hugeicons.tgz
tar -tzf hugeicons.tgz | grep "^package/dist/esm/.*Icon\.js$" | sed 's|.*/||;s|\.js$||' > names.txt
```

If `npm` is missing, tell the user to install Node.js (nodejs.org, or `brew install node`).

## 2. Extract an icon

1. **Validate the name against `names.txt`.** Near-miss names are easy to invent.
2. Read the module:
   ```bash
   tar -xzOf hugeicons.tgz package/dist/esm/<Name>.js
   ```
   Each module is `[["path", {d, stroke, strokeLinecap, strokeLinejoin, strokeWidth}], …]`. Icons may use `circle` / `rect`, not just `path`.
3. **The attribute keys are unquoted JS, not JSON**: `{ d: "M20.99…", stroke: "currentColor", …, key: "0" }`. A regex looking for `"d":` matches nothing and silently yields empty paths. Match `d:\s*"([^"]*)"`, and split elements on `\["(\w+)",\s*\{(.*?)\s*key:`. Every element ends with a `key` property, which makes a reliable terminator.
4. Emit `<svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">` with the elements inside, and `stroke` set to a colour token, not `currentColor`.
5. **Write the markup to a file in `$WORK` and read it back before pasting.** Empty `d=""` attributes are the failure mode and they are invisible in a tool result.

**Never hand-type path data.** A `d` typed from memory once produced `"5.16couple 11"` inside a path and rendered a broken icon that looked plausible at a glance.

## 3. Place it in Paper

1. `write_html` the SVG into its wrapper Frame. `write_html` names it `Frame`; follow with `rename_nodes`.
2. **To swap an icon**, `write_html` in `replace` mode on the `SVG` node id, not the wrapper. Rewriting the whole cell throws away its text.
3. **To resize**, set `width` / `height` on the `SVG` node (and its wrapper Frame). That works; setting them on an `SVGVisualElement` child is accepted and does nothing. Verify with `get_node_info`.
4. **To recolour**, set `stroke` on the `path` children. Setting it on the `SVG` node does not override a stroke already on its paths.
5. `get_screenshot` the icon afterwards.

## Budget

Roughly **6 Paper nodes per icon**: ~150 icons ≈ 1,000 nodes. The full 6,025 would make a file unusable. The Brand file's **Icons** page already holds 164 Hugeicons; copy from there when the icon exists (same file: `duplicate_nodes`; another file: `get_jsx` → `write_html`).
