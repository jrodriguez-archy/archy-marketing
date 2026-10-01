#!/usr/bin/env python3
"""Measure the DOC house colour on a video and compare it with the targets (references/color-guide.md).

  measure_color.py PROJECT_DIR                    render preview frames of the built project
  measure_color.py PROJECT_DIR --export FILE.mp4  measure an exported video instead

For each camera it picks up to 3 speaker shots (not split, card or punch) from .tesseract-work/timing.json,
takes the middle frame and measures:
  skin  mean RGB of skin-coloured pixels in the upper half (r > g > b, r - b > 18 and > 18 % of r, r > 90;
        the cream lower-third box is excluded)
  wall  mean RGB of the background in the two top corners (x < 18 % or x > 83 %, y < 22 %)
and prints them next to the targets with the difference. Match CAM B to CAM A first (same person, same
words: the two cameras must look the same), then both to the targets.
"""
import io, json, os, subprocess, sys
from PIL import Image

# House targets: the median CAM A of the six approved Module 9 videos (F9.1-F9.6, 2026-09-30),
# 8-bit RGB of the 1080p export. CAM A was already consistent across them; CAM B drifted.
TARGET = {"skin": (191, 154, 133), "wall": (94, 106, 94)}
TOL = {"skin": 5, "wall": 6}          # max per-channel difference that still reads as the same picture

T = os.environ.get("TSRCT") or os.path.expanduser("~/Library/Application Support/Tesseract/bin/tsrct")

def frame(project, export, t):
    if export:
        cmd = ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", export, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"]
        return Image.open(io.BytesIO(subprocess.run(cmd, capture_output=True, check=True).stdout)).convert("RGB")
    out = os.path.join(os.path.dirname(project), ".tesseract-work", "measure_frame.png")
    subprocess.run([T, "preview", "--project", project, "--time", f"{t:.3f}", "--output", out], check=True, capture_output=True)
    return Image.open(out).convert("RGB")

def measure(im):
    px = im.resize((480, 270)).load()
    skin, wall = [], []
    for y in range(270):
        for x in range(480):
            r, g, b = px[x, y]
            if y < 140 and r > g > b and r - b > 18 and r - b > 0.18 * r and r > 90:  # not the cream LT box
                skin.append((r, g, b))
            if y < 60 and (x < 88 or x > 400):
                wall.append((r, g, b))
    avg = lambda a: tuple(sum(c[k] for c in a) / len(a) for k in range(3)) if a else (0, 0, 0)
    return {"skin": avg(skin), "wall": avg(wall)}

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = os.path.abspath(sys.argv[1])
    export = sys.argv[sys.argv.index("--export") + 1] if "--export" in sys.argv else None
    cfg = json.load(open(os.path.join(root, ".tesseract-work", "video.json")))
    project = os.path.join(root, cfg["project"])
    shots = json.load(open(os.path.join(root, ".tesseract-work", "timing.json")))["shots"]
    res = {}
    for cam in ("A", "B"):
        speaker = [s for s in shots if s[2] == cam and not s[3].startswith(("split", "card", "punch")) and s[5] - s[4] > 4]
        picks = speaker[::max(1, len(speaker) // 3)][:3]
        ms = [measure(frame(project, export, (s[4] + s[5]) / 2)) for s in picks]
        if not ms:
            continue
        res[cam] = {k: tuple(sum(m[k][i] for m in ms) / len(ms) for i in range(3)) for k in ("skin", "wall")}
    fmt = lambda c: "%5.0f %5.0f %5.0f" % c
    ok = True
    print(f"{'':6s}{'':6s}{'R     G     B':>18s}   diff vs target")
    for cam, m in res.items():
        for k in ("skin", "wall"):
            d = tuple(m[k][i] - TARGET[k][i] for i in range(3))
            bad = max(abs(v) for v in d) > TOL[k]
            ok &= not bad
            print(f"CAM {cam} {k:5s} {fmt(m[k])}   {'%+5.0f %+5.0f %+5.0f' % d}{'   <- adjust' if bad else ''}")
    if "A" in res and "B" in res:
        d = tuple(res["B"]["wall"][i] - res["A"]["wall"][i] for i in range(3))
        s = tuple(res["B"]["skin"][i] - res["A"]["skin"][i] for i in range(3))
        print(f"B - A  skin {'%+5.0f %+5.0f %+5.0f' % s}   wall {'%+5.0f %+5.0f %+5.0f' % d}")
    print(f"target skin {fmt(TARGET['skin'])}   wall {fmt(TARGET['wall'])}   {'OK' if ok else 'OUT OF RANGE'}")

if __name__ == "__main__":
    main()
