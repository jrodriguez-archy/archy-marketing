#!/usr/bin/env python3
"""Labeled contact sheet: sheet.py VIDEO OUT.png COLS WIDTH t1 t2 ... (seconds)."""
import subprocess, sys, io
from PIL import Image, ImageDraw, ImageFont

video, out, cols, width = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
times = [float(t) for t in sys.argv[5:]]
frames = []
for t in times:
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", video, "-frames:v", "1",
                          "-vf", f"scale={width}:-2", "-f", "image2pipe", "-vcodec", "png", "-"],
                         capture_output=True).stdout
    im = Image.open(io.BytesIO(png)).convert("RGB")
    d = ImageDraw.Draw(im)
    label = f"{int(t // 60)}:{t % 60:05.2f}"
    font = ImageFont.load_default(size=max(14, width // 16))
    d.rectangle([0, 0, width // 3, width // 11], fill=(0, 0, 0))
    d.text((4, 2), label, fill=(255, 255, 0), font=font)
    frames.append(im)
w, h = frames[0].size
rows = (len(frames) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), (40, 40, 40))
for i, im in enumerate(frames):
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(out)
print(out, len(frames))
