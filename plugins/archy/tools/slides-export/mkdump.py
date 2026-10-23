#!/usr/bin/env python3
"""Assemble a dump/<n>-<slug>.json from two files saved verbatim off the MCP.

    trees/<n>.txt      get_tree_summary(depth 10)  -> the `summary` string, as-is
    styles/<n>.json    get_computed_styles([ids])  -> the `styles` object, as-is
    text/<n>.json      optional {id: full string}  for anything truncated at 60 chars
    assets/<n>.json    optional {svg node id: "assets/....png"}

The reads live in the work directory ($ARCHY_WORK or --work=DIR; see archywork.py), either
directly (trees/, styles/, ...) or under scratchpad/. The dump is written to <work>/dump/.

Nothing here interprets a value: the point is to stop hand-retyping 100 style objects per
slide, because a mistyped `left` shifts a slide by twelve pixels and nothing complains.

    mkdump.py 66 direct-mail "66 · Direct Mail"
"""
import json, os, sys, re

import sys; sys.dont_write_bytecode = True   # never write __pycache__ into the plugin folder

import archywork

# Where the verbatim reads were saved: <work>/trees/... or <work>/scratchpad/trees/...
SCR = next((d for d in (archywork.work(), archywork.work("scratchpad"))
            if os.path.isdir(os.path.join(d, "trees"))), archywork.work())


def main():
    n, slug, name = sys.argv[1], sys.argv[2], sys.argv[3]
    tree = open(f"{SCR}/trees/{n}.txt", encoding="utf-8").read().rstrip("\n")
    styles = json.load(open(f"{SCR}/styles/{n}.json", encoding="utf-8"))
    styles = styles.get("styles", styles)

    tp = f"{SCR}/text/{n}.json"
    text = json.load(open(tp, encoding="utf-8")) if os.path.exists(tp) else {}

    ids = re.findall(r"\(([0-9A-Z]+-0)\)", tree)
    # A path inside an SVG never becomes a shape - paper2spec skips it and the whole icon
    # goes in as one PNG - so its styles are dead weight and are not worth a read.
    paths = set(re.findall(r"SVGVisualElement \"[^\"]*\" \(([0-9A-Z]+-0)\)", tree))
    for i in paths:
        styles.setdefault(i, {})
    missing = [i for i in ids if i not in styles]
    if missing:
        raise SystemExit(f"{n}: {len(missing)} nodes in the tree have no styles: {missing[:8]}")

    ap = f"{SCR}/assets/{n}.json"
    assets = json.load(open(ap, encoding="utf-8")) if os.path.exists(ap) else {}

    out = {"name": name, "tree": tree, "styles": styles}
    if text:
        out["text"] = text
    if assets:
        out["svgAssets"] = assets
    os.makedirs(archywork.work("dump"), exist_ok=True)
    path = archywork.work("dump", f"{n}-{slug}.json")
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"  {os.path.basename(path):<40} {len(ids)} nodes"
          + (f", {len(text)} text overrides" if text else "")
          + (f", {len(assets)} svg assets" if assets else ""))


if __name__ == "__main__":
    main()
