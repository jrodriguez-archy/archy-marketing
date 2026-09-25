#!/usr/bin/env python3
"""Cache every Paper-hosted image the dumps reference.

A picture dropped onto a Paper canvas is uploaded, so `get_computed_styles` reports it as
`url(https://app.paper.design/file-assets/<file>/<asset>.jpg)` rather than as the local
path it came from. pptx has to embed real bytes, so the assets are pulled once and
addressed by their own id - which also means the deck rebuilds offline and a re-run costs
nothing.

Reads <work>/dump/*.json and caches into <work>/assets/photos ($ARCHY_WORK or --work=DIR;
see archywork.py).
"""
import io, os, re, sys, json, glob, urllib.request

import sys; sys.dont_write_bytecode = True   # never write __pycache__ into the plugin folder

import archywork

DIR = archywork.WORK
OUT = os.path.join(DIR, "assets", "photos")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
URL_RE = re.compile(r"https://app\.paper\.design/file-assets/[\w-]+/([\w-]+)\.(\w+)")


def main():
    os.makedirs(OUT, exist_ok=True)
    seen, got, cached = set(), 0, 0
    for f in sorted(glob.glob(os.path.join(DIR, "dump", "*.json"))):
        for m in URL_RE.finditer(io.open(f, encoding="utf-8").read()):
            url, asset, ext = m.group(0), m.group(1), m.group(2)
            if asset in seen:
                continue
            seen.add(asset)
            path = os.path.join(OUT, "%s.%s" % (asset, ext))
            if os.path.exists(path) and os.path.getsize(path) > 0:
                cached += 1
                continue
            # The CDN 403s a bare urllib request - it wants a browser User-Agent.
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req) as r, io.open(path, "wb") as fh:
                fh.write(r.read())
            size = os.path.getsize(path)
            if size == 0:
                os.remove(path)
                raise SystemExit("empty download: %s" % url)
            print("  %s.%s  %d KB" % (asset, ext, size // 1024))
            got += 1
    print("photos: %d fetched, %d already cached" % (got, cached))


if __name__ == "__main__":
    main()
