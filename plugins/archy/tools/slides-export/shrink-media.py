#!/usr/bin/env python3
"""Resample the .pptx's embedded rasters down to the size they are actually shown at.

Paper's CDN hands back the original upload - a scrapbook portrait is a 2000px photo
sitting in a 208px well - so the deck leaves the builder at ~68 MB, most of it pixels
nobody sees. Google Slides has to convert every one of those on import.

Each image is capped at 3x its largest placement on any slide, which is past retina and
past what a projector resolves. Vector-derived assets (icons, arrows, the wordmark) are
already generated at 4x their box, so they are left alone by the same rule.

    python shrink-media.py deck.pptx

A relative path is looked up in the current directory, then in the work directory
($ARCHY_WORK or --work=DIR; see archywork.py).
"""
import io, os, re, shutil, sys, zipfile
import sys; sys.dont_write_bytecode = True   # never write __pycache__ into the plugin folder
import archywork
from lxml import etree
from PIL import Image

NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
EMU_PER_PX = 9525.0     # the pptx's own 96-dpi pixel; only used to size the raster
FACTOR = 3


def main():
    path = archywork.input_path(sys.argv[1])
    z = zipfile.ZipFile(path)
    names = z.namelist()

    # slideN.xml -> {rId: target media part}
    want = {}   # media part -> largest (w, h) in px it is ever drawn at
    for slide in [n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)]:
        rels = etree.fromstring(z.read(slide.replace("slides/", "slides/_rels/") + ".rels"))
        target = {r.get("Id"): os.path.normpath(os.path.join("ppt/slides", r.get("Target")))
                  for r in rels}
        root = etree.fromstring(z.read(slide))
        for pic in root.iter("{%s}pic" % NS["p"]):
            blip = pic.find(".//a:blip", NS)
            ext = pic.find(".//a:ext", NS)
            if blip is None or ext is None:
                continue
            part = target.get(blip.get("{%s}embed" % NS["r"]))
            if not part:
                continue
            w = int(ext.get("cx")) / EMU_PER_PX
            h = int(ext.get("cy")) / EMU_PER_PX
            prev = want.get(part, (0, 0))
            want[part] = (max(prev[0], w), max(prev[1], h))

    out = path + ".tmp"
    saved = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as w_:
        for item in z.infolist():
            data = z.read(item.filename)
            box = want.get(item.filename)
            if box and item.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                cap = (max(1, int(box[0] * FACTOR)), max(1, int(box[1] * FACTOR)))
                im = Image.open(io.BytesIO(data))
                if im.width > cap[0] or im.height > cap[1]:
                    im2 = im.copy()
                    im2.thumbnail(cap, Image.LANCZOS)
                    buf = io.BytesIO()
                    im2.save(buf, format=im.format or "PNG", optimize=True)
                    if buf.tell() < len(data):
                        saved += len(data) - buf.tell()
                        data = buf.getvalue()
            w_.writestr(item, data)
    z.close()
    shutil.move(out, path)
    print("shrank embedded media by %.1f MB in %s" % (saved / 1e6, os.path.basename(path)))


if __name__ == "__main__":
    main()
