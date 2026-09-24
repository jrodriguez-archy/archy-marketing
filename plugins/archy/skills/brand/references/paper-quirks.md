# Paper MCP quirks

Read this before building or editing anything through the Paper MCP, and again whenever a write is accepted but nothing changes on the canvas. Every item here was verified the hard way; do not assume Paper's CSS behaves normally.

Print output (PDF trimming, CMYK conversion, pure-K QR codes) lives in the `print-pdf` skill, not here.

---

## When Paper has no equivalent for a Figma feature

**"Paper doesn't support that" is never the answer. Find what the feature *does* and rebuild it.** Paper renders CSS, so a Figma feature is only ever missing as a *control*; the underlying capability is almost always there under a different name. Ask which CSS property produces the same result, not whether the Figma concept exists.

The worked example is masks (recipe under *Styles that silently fail*): Paper has no mask tool, but a mask is just "clip the child to this shape", which is `border-radius` + `overflow: clip` on the parent. Same output, no mask needed.

When a paste arrives with something broken and there is no obvious control for it:

1. Name what the feature does in plain terms.
2. Translate that to CSS.
3. Apply it with `update_styles`.
4. Screenshot to confirm.
5. Add the recipe to this file. Verified recipes only, never assumed ones, since Paper's CSS does diverge in places.

---

## Pages and artboards

- **`create_artboard` ignores `pageId`.** It creates on the active page. Create, then `move_nodes` to `root_node_<pageId>`, then set x/y, then confirm `parentId` with `get_node_info` before building into it.
- **`create_artboard` takes all geometry inside `styles`, as strings**: `{width:"1920px", height:"1080px", …}`. There are no top-level `width` / `height` / `pageId` arguments. **`left` / `top` passed there are ignored**: the artboard lands at an arbitrary position (observed at `-489,-1397` and at the previous artboard's slot) and the result echoes that position back, so it looks placed when it is not. Always follow the create with an `update_styles` setting `left` / `top`, and check the returned `worldX` / `worldY` rather than trusting the values you sent.
- **`create_artboard` makes the artboard `display: flex; flex-direction: column` by default.** Nothing says so in the result, and an absolutely positioned `Content` hides it on the canvas, but the layer panel shows those artboards with the stack icon instead of the plain frame one, so a file ends up with two kinds of main layer. Removing flex with `update_styles` cleans the CSS (`get_jsx` shows no flex) but does not change the layer-panel icon. **The reliable fix is structural:** duplicate a block-type artboard, empty it, `move_nodes` the flex artboard's children into it, delete the original. Moving children into a *block* parent is safe; moving them into a *flex* parent silently gives them `flex: 1`.
- **Never leave `display: flex` on an artboard.** Artboards hold absolutely positioned bleed layers plus one auto-layout `Content`. Flex on the artboard does nothing for absolute children, but it silently takes over any child left at `position: relative` and drops it wherever `align-items` / `justify-content` decide. That is how a `Content` frame ended up 400px from where its `top` said it was. Keep artboards `display: block` and pin `Content` with explicit `left` / `top`.
- **Moving an artboard between pages is safe.** `move_nodes` with `parentId: root_node_<pageId>` preserves node ids and leaves absolutely positioned children (Rulers, `Content` frames, bleed art) untouched. Set `left` / `top` afterwards to place it on the new page's grid.
- **`duplicate_nodes` works across pages.** Pass `parentId: "root_node_<pageId>"` for a page other than the active one and the copy lands there, ids mapped as usual. The copy arrives at an arbitrary position, so set `left` / `top` / `translate: none` immediately.
- **A page cannot be renamed or deleted from the MCP, and the two fail differently.** `rename_nodes` on `root_node_<pageId>` is accepted and echoed back, and nothing changes (a silent no-op). `delete_nodes` on a page root at least says so: `Cannot delete a page root node`, even for a page holding nothing but its own root. There is no `delete_page`. Plan page names at `create_page` time; renaming or removing a page is a manual step in the Paper app (right-click the page in the sidebar). The MCP can only empty it first.
- **Archived Paper files disappear from `list_files` and cannot be reached.** Unarchive before working on one.

---

## Renderer and reading geometry

- **`get_screenshot` only works on the active page.** An artboard on another page returns an empty result rather than an error. `open_file` with its `pageId` first.
- **`get_children` on an inactive page returns UNRESOLVED layout: `x` / `y` come back as 0** with no error and a plausible-looking payload. A frame with `padding: 48px 40px` reports its child at `0, 0` instead of `40, 48`. This is the most dangerous quirk in the list, because the export pipelines trust those coordinates. **`open_file` with the artboard's `pageId` before reading any geometry**, and if a padded frame reports a child at `0, 0`, that is the tell.
- **Those two symptoms are one symptom, and "inactive page" is not the only cause: a file's renderer can get stuck.** Empty screenshots and unresolved layout both mean *the renderer is not running for this file*, and that happens on the **active** page too. It has happened after a session of several hundred writes; once it starts, every screenshot in that file returns empty (including artboards never touched) and flex children report their parent's coordinates. Another tell: a text node reporting `0×0` and its parent frame `1728×0` while fixed-height frames still report correctly.

  **Diagnose in this order, because each step rules out a layer:**
  1. `get_selection`. If it answers, the MCP connection is fine.
  2. `get_screenshot` on an artboard in a **different file**. If that renders, the app and the renderer are fine and the problem is the one file. (A page of 1,100 nodes renders fine, so this is not about node count.)
  3. `open_file` on the stuck file. **This does not fix it.** Reopening through the MCP does not reset that file's renderer.

  The fix is manual: **close the file in the Paper app and reopen it**, or restart Paper. Closing files you are not using helps: four open files are four renderers.

  **While it is stuck:** everything except reading geometry still works. Writes, duplicates, deletes and `get_computed_styles` (which returns the *authored* values, not resolved ones) are reliable. Author absolute values, verify against `get_computed_styles`, and verify composition another way (for a deck, build the `.pptx` and read it back with `markitdown`). What you cannot do is trust `worldX` / `worldY` or see the result, so **do not derive a coordinate from a read while the renderer is down**. That is how a sub-pixel or off-lane value gets baked in unseen.

  A *single* unresolved read right after the file regains focus is different and harmless: re-read and it settles.
- **`get_tree_summary` truncates a text node's content at 60 characters**, with no ellipsis, no flag and no error. A long line comes back looking like copy that simply stops, which is the `#1211`-rendered-as-`#121` defect class: wrong content that survives review because it reads as plausible. `get_node_info` returns the full string in `textContent`. Treat anything measuring exactly 60 characters as truncated until proven otherwise.
- **`transform-origin` is silently normalised to `0% 0%`.** Author `transform-origin: 50% 50%`, read it back, and `get_computed_styles` says `0% 0%`. So **every rotation in Paper pivots on the frame's top-left corner**, never its centre, and `left` / `top` stop describing where the thing lands. Paper reports each rotated child's transformed **top-left corner** in `worldX` / `worldY`, so comparing that against a centre-derived number looks like a bug when nothing is wrong.
- **The booth badge does not render where you put it.** It carries a 6° rotation and its ribbon child carries −6°, both with `transform-origin: 0 0`, so the rendered box is offset from `left` / `top` (roughly +100 / +180 at a 200px size, and the offset scales). Position it by screenshotting and nudging, never by arithmetic. The same applies to la mascota when she is rotated 90°.
- **Three equal flex rows in a fixed band produce sub-pixel positions.** `flex: 1 1 0` over 710px with two 2px rulers gives 235.33px rows and children at y 237.33 / 472.66. Give the rows explicit integer heights that sum exactly (236 / 235 / 235 + 2 + 2 = 710).
- **Measure many text widths in one call.** Put the candidates in a `flex-direction: row; gap: 0` frame, each at `width: max-content`, then `get_children`. Each child's `x` is the running sum of its predecessors' widths, so N strings cost one write plus one read instead of N `get_node_info` calls. Delete the frame afterwards. Example result: Inter Medium at 26px measures ~11.5px per character, not the ~13 that eyeballing suggests, a 12% error that is enough to wrap a line that was supposed to fit.

---

## Writing nodes (write_html, duplicate, rename, text)

- **`write_html` silently drops an empty `<div>`.** Give a new container a throwaway text child, move the real children in, delete the placeholder.
- **`write_html` ignores `data-name`.** Every node comes back as `Frame` / `Rectangle` / `Text`. Follow each write with `rename_nodes`; there is no way to name nodes at creation.
- **`write_html` can hand back ids that a later `write_html` re-allocates, destroying the first batch silently.** One body write returned `68V-0 … 697-0`; the next `write_html` into a *different* artboard on the same page returned `68V-0 … 68Z-0` again, and the first subtree was gone, with no error. **If a `write_html` result contains an id you have already seen this session, the earlier nodes are gone.** `get_children` on the parent is the check. Mitigations: do not interleave writes across two artboards, and screenshot after each body.
- **A frame's children stay absolute until the frame is `display: flex`.** Setting `position: relative` on the child alone is ignored.
- **A duplicated node carries the original's `translate`, and it is usually stale.** Paper bakes a hand-dragged position into `translate` as absolute pixels (`translate: 957px 3467px`) or as a centre anchor (`translate: -50% -50%`). Duplicate that node into another artboard and it lands hundreds of pixels off-canvas, or its inner text sits outside its own shape. **Set `translate: none` on the copy and on every child you reposition, before setting `left` / `top`.**
- **`duplicate_nodes` does not preserve the order of a mixed batch.** Asking for `[Point, Ruler, Point]` in one call groups the copies by source node and appends the odd one last, so the parent ends up `Point · Ruler · Point · Point · Ruler`. When the order of an interleaved sequence matters, duplicate one node per call, or fix it afterwards with `move_nodes` (`{nodeId, before: siblingId}`). Always `get_children` on the parent to verify.
- **`duplicate_nodes` inserts the copy next to its source, not at the end of the parent.** Fix the order with `move_nodes` (`{nodeId, before: siblingId}`) and verify.
- **Passing the same id several times to `duplicate_nodes` yields that many copies**, each with its own `descendantIdMap` keyed by the *source* ids, so one call can spawn five artboards and you can still tell them apart. The source-relative keys are stable, which makes it easy to find the same child (for example `Header`) in every copy.
- **Round what a hand-drag leaves behind** (`top 52.276`, `height 61.4375`). Set integer `left` / `top` / `width` / `height` and `translate: none`, then confirm with `get_node_info`.
- **`scale` is not supported.** Resize the frame, then scale every absolutely positioned child by hand (positions *and* font sizes). Percentage-sized children scale with the frame; px-sized ones do not.
- **Resizing the booth badge breaks its text.** The ribbon and the `INFO` box are percentage-sized so they scale with the frame, but the two text nodes are px and do not. Scaling 273 → 180 means also scaling `INFO` to 135 × 78 @ 22, 51, `BOOTH` to 29/33 and the number to 41/45. Always screenshot the badge at `scale: 2` afterwards; this defect class once shipped `#1211` rendered as `#121`.
- **`set_text_content` honours `\n`.** A literal newline in the string forces a line break in a Text node, which is how you control where a two-word title splits without narrowing the box.
- **`write_html` collapses a literal newline in text; `set_text_content` honours it.** Build the node first and set multi-line copy afterwards, or accept one line.
- **Inline formatting inside a text node is flattened.** A `<b>`, `<strong>` or nested `<span>` with its own colour inside a paragraph is accepted and silently dropped; the whole run comes out in the outer node's style. This is the limit that forces the two-tone headline into two nodes. Two ways out: a flex row with `align-items: baseline` and two `width: max-content` nodes when the line does not wrap, or two stacked nodes (lead above, explanation below) when it does. A wrapping paragraph cannot be split across a flex row.
- **`write_html` normalises a per-weight font family back to the bare one, silently.** Author `font-family: Inter-Medium` and Paper stores `"Inter", system-ui, sans-serif` with `fontWeight: 500`; setting the hyphenated face back on the node afterwards is a no-op. The canvas still renders the right weight, so nothing looks wrong, but anything that reads the family alone loses the weight. The Slides exporter recovers the face from `fontWeight` (500 → Medium, 600 → SemiBold, 700 → Bold) when the family carries no hyphen.
- **`text-wrap: balance` works in Paper and is the right fix for an orphaned last line, but it will break a word at its hyphen.** One `update_styles` evens out a ragged paragraph or a two-tone headline's first node, and keeps working when the copy changes. The catch: CSS allows a break *after* a hyphen and balance actively hunts for one. `--color-neutral-500` came out as `--color-` / `neutral-500`, `knocked-out` as `knocked-` / `out`. **Balance everything except nodes carrying a token name or a hyphenated compound**, and set those back to `text-wrap: wrap`. There is no CSS guard: `word-break: keep-all` does not stop hyphen breaks.
- **In a two-tone headline the orphan is a defect of the split, not of the copy. Check first whether the frame is narrower than the content column.** The device is meant to give one line per weight; it only wraps when the box makes it. A headline frame authored at 1500 against a 1728 column wrapped its grey half and stranded two words above a full-width bold line; widening the frame to the column fixed it, where balancing had kept the three-line silhouette. **Fix the measure first, balance second.** Check the *rendered* line count of the first node, never its character count.

---

## Styles that silently fail

Each of these is accepted, often reported back by `get_computed_styles`, and paints nothing.

- **No masks: use `border-radius` + `overflow: clip` on the wrapper.** A Figma mask arrives as a `Mask` frame holding an oversized image plus a leftover filled shape (the mask path, usually `#000000`) that no longer clips anything. Set `borderRadius: 9999px` and `overflow: clip` on that frame and the crop is back; then delete the leftover shape. Any radius works; this is not circle-only. Keep the image rect larger than the frame so it still covers after rounding, and re-check the subject's framing, since the corners a mask removed were carrying part of it.
- **`color-mix()` is silently dropped from `backgroundColor`**, both `color-mix(in oklab, …)` and the `color-mix(var(--x) 40%, transparent)` form. The property vanishes from `get_computed_styles` and the element paints nothing. When a tint between two tokens is needed, compute it, set the hex, and note which tokens it derives from. Example: Rulers on the blue ground are `#2A5DF6` = `--color-royal-blue-500` + 16% white, solid.
- **A Text node ignores `backgroundColor`.** The style is accepted and reported back, and nothing paints. Wrap the text in a Frame and put the fill there.
- **`currentColor` does not resolve through a parent frame.** Set an explicit token on the SVG or its paths. Keep `currentColor` in shipped code, not on the canvas.
- **No shader control through the MCP.** `get_guide` offers only `paper-mcp-instructions`, `mobile-status-bar`, `figma-import` and `image-generation`. Shaders exist in the Paper app but cannot be set from here. For a subtle dark ground the options are: an existing vector asset at low opacity (0.18 reads as texture behind 180px type), a CSS gradient, a generated image via `paper-gen://` (costs the user's quota, ask first), or the user adds the shader by hand.

---

## SVG and icons

- **Moving or duplicating a vector element into another SVG lands it in the wrong place.** Paper tries to keep the element's on-screen position, computes it from stale layout, and bakes the difference into a `translate` (seen at about −1,200px, outside the new SVG's box, so the logo simply disappears). The element also loses any `fill` it inherited from its old parent SVG. To split one SVG into two (a combined logo lockup, for example), write each new SVG fresh with `write_html`, using the path data from `get_jsx` and an explicit `fill="var(--color-…)"` on every path.
- **`update_styles` cannot recolour an SVG path.** A `fill` set on a path node is accepted and ignored. Rewrite the SVG with the colour on each path, or, for a simple line, replace the SVG with a 2px frame that has a `backgroundColor`.
- **A text pill drawn as a fixed-width SVG does not grow with its text.** Replace it with a frame (`display: flex`, `padding`, `backgroundColor`, `borderRadius: 999px`, `width: fit-content`) holding the text, so a longer event name stays inside it.


- **`update_styles` cannot resize an `SVGVisualElement`.** Setting `width` / `height` on one is accepted, appears in `get_computed_styles`, and changes nothing; `get_node_info` still reports the old size. To rescale part of an SVG (one logo inside a lockup, say), resize it by hand in Paper, resize the whole parent SVG, or duplicate a copy that is already the right size from another artboard and swap it in. Verify with `get_node_info`, never with `get_computed_styles`.
  - **The `SVG` node itself *does* resize.** Only its `SVGVisualElement` children resist. Setting `width` / `height` on the `SVG` (and on the wrapper Frame) rescales a whole icon cleanly; `get_node_info` reports the new size (for example 40 × 40). That is how icons go 32 → 40 without re-writing markup.
- **Setting `stroke` on an `SVG` node does not override a stroke already set on its `path` children.** It is accepted and reported back and nothing changes. Recolour the paths: `get_children` on the icon's wrapper Frame gives the SVG, and its children are the paths.
- **Swap an icon with `write_html` in `replace` mode on the `SVG` node**, targeting the node id, not the wrapper. Rewriting the whole cell to change one icon throws away the text you just set.
- **Paper has no `<g>`.** `write_html` silently drops one. Build a group inside an SVG as a **nested `<svg>` with a tight viewBox**: create it with a throwaway `<rect fill="none">` child, `move_nodes` the real elements in, then delete the placeholder. The children keep their original absolute coordinates and the viewBox does the offset, so nothing has to be re-drawn, and z-order survives as long as the groups are contiguous runs of the original order.
- **Moving a vector asset between files is `get_jsx` → `write_html`, and the `<g>` has to be baked out by hand.** `duplicate_nodes` and `<x-paper-clone>` are same-file only, so a brand asset that lives in another file comes across as markup. Because Paper drops the `<g>`, **its transform is lost and the children land somewhere else**: compose the group's matrix into each child's own `transform` before writing. Example: la mascota is `Robot` (691 × 461) inside `4.1 - 1080x1350 Post` in the Events file; her eyes are a `<g transform="matrix(-1 0 0 -1 440 247)">`, so the second eye's `matrix(1 0 0 1 175.439 0)` composes to `matrix(-1 0 0 -1 264.561 247)`. Her gradients are the asset's own hexes, not tokens; leave them.
- **Never hand-type SVG path data.** A `d` string typed from memory produced `"5.16couple 11"` inside a path and rendered a broken icon that looked plausible at a glance. Always paste the `d` from the extracted module (see the `hugeicons` skill), and screenshot the icon afterwards.

---

## Images

- **A local image file must be referenced as a percent-encoded `file://` URL.** A bare absolute path in `backgroundImage` is silently dropped by `write_html` (the property never lands, and `get_computed_styles` shows no `backgroundImage`), and the same path in an `<img src>` renders the broken-image placeholder. `url('file:///path/to/Deck%20Assets/name.png')` works: note the `%20` for a space in a folder name, and the quotes, without which the space breaks the CSS. Set `backgroundSize` in the same call: a later `update_styles` that only replaces `backgroundImage` leaves the size unset and the picture renders hugely zoomed.
- **Size an image box to the asset's own aspect and use `background-size: contain`.** `100% 100%` is what Paper writes when a picture is dropped in by hand, and it stretches the moment the box is off (the defect that turned a round "O" logo into an ellipse). `contain` letterboxes instead of distorting, so an arithmetic slip shows up as a thin margin rather than a squashed logo. Use `cover` only when the box is deliberately a different aspect and the crop is wanted.
- **Photos dropped on a canvas live on Paper's CDN, not on disk.** `get_computed_styles` reports `url(https://app.paper.design/file-assets/…)`. The CDN **403s a bare urllib request**; it wants a browser User-Agent.

---

## Typography identification

- **Onest and Inter cannot be told apart by measurement at body sizes. The tell is the `y`.** Their width/cap-height ratios agree to within ±0.02em of tracking, so fitting rendered widths against a rasterised paste returns a tie and then picks the wrong one (it once chose Inter for a whole one-pager set in Onest). **Onest's `y` drops and curls into a hook to the left; Inter's is a straight diagonal cut at an angle.** The `g` tail confirms it. Identify the face by rendering both candidates over the source crop and looking at the `y` *before* measuring anything.
- **Derive a size from a flat-topped capital: `E`, `H`, `M`, `P`.** `S`, `C`, `O` and `G` overshoot the cap line by about 1px at poster scale, which inflates the derived size by ~3% and sends a whole type scale one step too big. The same measurement read 29 off an `S` and 28 off an `E` in the same line.

---

## Export and PDF

- **`export` and `export_combined_pdf` ignore `outputPath` / `outputDirectory` and always write to `~/Downloads`**, auto-incrementing (`Combined.pdf`, `Combined (1).pdf`). macOS TCC then blocks the shell from even listing that folder, with or without the sandbox, so a script cannot pick the file up. **Finder can**: `osascript -e 'tell application "Finder" to move file "X" of (path to downloads folder) to …'` works, and is the only route to a scripted rename. This is also why the Slides exporter generates the `.pptx` from Paper's values rather than exporting anything by hand.
- **`export_combined_pdf` only assembles artboards on the ACTIVE page.** Hand it a whole multi-page deck and every node fails with `Error assembling PDF page for "<name>"`, echoing the *same* artboard name for all of them, which hides the cause. Export one page at a time, or generate instead.
- **`export`'s `scale` is a string** (`"1x"`), not a number; a number is rejected by the schema.
- **Paper exports only `png / jpg / webp / avif / pdf / svg`.** There is no editable-text path out. For an editable deck use the `slides-export` skill; for Figma use `figma-export`.
- **Paper's PDF export is not print-ready.** For page size, the blank second page, rasterised gradients and CMYK, use the `print-pdf` skill.

---

## Argument shapes

| Tool | Shape |
|---|---|
| `update_styles` | `updates:[{nodeIds:[…], styles:{}}]` |
| `rename_nodes` | `updates:[{nodeId, name}]` |
| `move_nodes` | `moves:[…]` (use `{nodeId, before: siblingId}` to reorder) |
| `duplicate_nodes` | `nodes:[{id}]`. Repeat the id for several copies; `count` yields only one |
| `set_text_content` | `textContent` |
| `create_artboard` | All geometry inside `styles`, as strings |
| `export` | `scale` as a string, `"1x"` |
