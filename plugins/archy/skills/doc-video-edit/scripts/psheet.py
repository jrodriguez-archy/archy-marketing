#!/usr/bin/env python3
"""Labeled sheet of Tesseract preview frames.
  psheet.py PROJECT.tsrct OUT.png COLS t1 t2 ...        (edit seconds)
  psheet.py PROJECT.tsrct OUT.png COLS --crop x0,y0,x1,y1 t1 t2 ...
Use it after every build to review motion, cuts and graphics (24 fps steps: 0.0417 s)."""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

TSRCT = os.environ.get("TSRCT") or os.path.expanduser("~/Library/Application Support/Tesseract/bin/tsrct")
args = sys.argv[1:]
project, out, cols = args[0], args[1], int(args[2])
crop = None
rest = args[3:]
if rest and rest[0] == "--crop":
    crop = tuple(int(v) for v in rest[1].split(","))
    rest = rest[2:]
times = [float(t) for t in rest]
tiles = []
with tempfile.TemporaryDirectory() as tmp:
    for i, t in enumerate(times):
        p = os.path.join(tmp, f"{i}.png")
        subprocess.run([TSRCT, "preview", "--project", project, "--time", str(t), "--output", p],
                       check=True, capture_output=True)
        im = Image.open(p).convert("RGB")
        if crop:
            im = im.crop(crop)
        w = 480 if cols >= 4 else 640
        im = im.resize((w, int(im.height * w / im.width)))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 120, 24], fill=(0, 0, 0))
        d.text((4, 3), f"{int(t // 60)}:{t % 60:05.2f}", fill=(255, 255, 0), font=ImageFont.load_default(size=17))
        tiles.append(im)
w, h = tiles[0].size
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), (40, 40, 40))
for i, im in enumerate(tiles):
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(out)
print(out, len(tiles))
