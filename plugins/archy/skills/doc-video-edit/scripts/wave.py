#!/usr/bin/env python3
"""Speech waveform view that does not need ffmpeg drawtext.
  wave.py AUDIO START_S DUR_S OUT.png [marker_s ...] [--words words.json]
Draws 10 ms RMS (square-root scale), transcript words (from transcribe.sh), gaps below -40 dBFS
and white review markers. Prints the quiet gaps (>= 80 ms) on the SOURCE clock: cut inside them."""
import array, json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

args = sys.argv[1:]
words_path = None
if "--words" in args:
    i = args.index("--words")
    words_path = args[i + 1]
    del args[i:i + 2]
src, start, dur, out = args[0], float(args[1]), float(args[2]), args[3]
marks = [float(m) for m in args[4:]]
sr = 16000
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(start), "-t", str(dur), "-i", src,
                      "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True).stdout
pcm = array.array("h", raw)
hop = sr // 100
rms = [math.sqrt(sum(s * s for s in pcm[i:i + hop]) / hop) / 32768 for i in range(0, len(pcm) - hop, hop)]
db = [20 * math.log10(max(r, 1e-6)) for r in rms]
gaps, run = [], None
for i, d in enumerate(db + [0]):
    if d < -40:
        run = i if run is None else run
    elif run is not None:
        if i - run >= 8:
            gaps.append((start + run / 100, start + i / 100))
        run = None
for a, b in gaps:
    print(f"gap {a:.2f}-{b:.2f} ({(b - a) * 1000:.0f} ms)")

W, H = 1800, 420
im = Image.new("RGB", (W, H), (18, 18, 20))
d = ImageDraw.Draw(im)
font = ImageFont.load_default(size=15)
x = lambda t: int((t - start) / dur * W)
for a, b in gaps:
    d.rectangle([x(a), 300, x(b), 312], fill=(40, 160, 70))
for i, r in enumerate(rms):
    h = math.sqrt(r) * 300
    px = int(i / max(1, len(rms)) * W)
    d.line([px, 160 - h / 2, px, 160 + h / 2], fill=(90, 170, 255))
for s in range(int(start), int(start + dur) + 1):
    for k in range(10):
        t = s + k / 10
        if start <= t <= start + dur:
            d.line([x(t), 0, x(t), 8 if k else 18], fill=(120, 120, 120))
    if start <= s <= start + dur:
        d.text((x(s) + 2, 20), f"{s}s", fill=(160, 160, 160), font=font)
if words_path:
    row = 0
    for f, e, w in json.load(open(words_path)):
        if f < start + dur and e > start:
            d.line([x(f), 330, x(f), 340], fill=(255, 200, 60))
            d.text((x(f) + 1, 345 + (row % 3) * 22), w, fill=(255, 220, 120), font=font)
            row += 1
for m in marks:
    d.line([x(m), 0, x(m), H], fill=(255, 255, 255), width=2)
    d.text((x(m) + 3, 280), f"{m:.2f}", fill=(255, 255, 255), font=font)
im.save(out)
print(out)
