#!/usr/bin/env python3
"""Force <a:noAutofit/> into every text bodyPr.

pptxgenjs's fit:"none" emits no autofit element at all, which means "inherit" in
OOXML. Google Slides is free to apply its own shrink-to-fit on import, and then a
team member typing a longer headline silently loses the type scale. An explicit
noAutofit is the only way to pin it.

Rewrites the .pptx in place. A relative path is looked up in the current directory, then
in the work directory ($ARCHY_WORK or --work=DIR; see archywork.py).
"""
import sys; sys.dont_write_bytecode = True   # never write __pycache__ into the plugin folder
import archywork
import re
import shutil
import sys
import zipfile

BODY_OPEN = re.compile(rb'(<a:bodyPr\b[^>]*?)(/>|></a:bodyPr>)')


def patch(xml: bytes) -> tuple[bytes, int]:
    n = 0

    def repl(m):
        nonlocal n
        attrs, close = m.group(1), m.group(2)
        # only text bodies carry zeroed insets in our generator; leave others alone
        if b'lIns="0"' not in attrs:
            return m.group(0)
        n += 1
        return attrs + b'><a:noAutofit/></a:bodyPr>'

    return BODY_OPEN.sub(repl, xml), n


def main(path):
    tmp = path + ".tmp"
    total = 0
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if re.match(r"ppt/slides/slide\d+\.xml$", item.filename):
                data, n = patch(data)
                total += n
            zout.writestr(item, data)
    shutil.move(tmp, path)
    print(f"injected noAutofit into {total} text bodies in {path}")


if __name__ == "__main__":
    main(archywork.input_path(sys.argv[1]))
