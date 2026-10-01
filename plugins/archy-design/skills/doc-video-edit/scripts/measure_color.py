#!/usr/bin/env python3
"""Measure the colour of both cameras of a DOC video: CAM B against CAM A, and against the targets of the
video folder's COLOR_GUIDE.md when there is one.

  measure_color.py PROJECT_DIR                    render preview frames of the built project
  measure_color.py PROJECT_DIR --export FILE.mp4  measure an exported video instead

For each camera it picks up to 3 speaker shots (not split, card or punch) from .tesseract-work/timing.json,
takes the middle frame and measures:
  skin  mean RGB of skin-coloured pixels in the upper half (r > g > b, r - b > 18 and > 18 % of r, r > 90;
        the cream lower-third box is excluded)
  wall  mean RGB of the background in the two top corners (x < 18 % or x > 83 %, y < 22 %)
Without a COLOR_GUIDE.md it checks only B - A (same person, same words: the cameras must look the same).
With one, it reads the skin and wall targets and tolerances from its table rows, e.g.
  | Skin | **191 154 133** | +-5 per channel | ...
  | Wall | **94 106 94** | +-6 per channel | ...
and checks both cameras against them as well.
"""
import glob, io, json, os, re, subprocess, sys
from PIL import Image

TOL = {"skin": 5, "wall": 6}          # max per-channel difference that still reads as the same picture

def guide_targets(root):
    """Skin and wall targets (and tolerances) from the folder's COLOR_GUIDE.md, or None."""
    hits = [f for f in glob.glob(os.path.join(root, "*")) if os.path.basename(f).lower() == "color_guide.md"]
    if not hits:
        return None, None
    text = open(hits[0], encoding="utf-8").read()
    target, tol = {}, dict(TOL)
    for k in ("skin", "wall"):
        m = re.search(r"\|\s*" + k + r"\s*\|\s*\**\s*(\d+)\s+(\d+)\s+(\d+)\s*\**\s*\|\s*(?:\D{0,3}?(\d+))?", text, re.I)
        if m:
            target[k] = tuple(int(m.group(i)) for i in (1, 2, 3))
            if m.group(4):
                tol[k] = int(m.group(4))
    return (target if len(target) == 2 else None), tol

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
    sign = lambda d: "%+5.0f %+5.0f %+5.0f" % d
    target, tol = guide_targets(root)
    ok = True
    if target:
        print(f"{'':12s}{'R     G     B':>18s}   diff vs COLOR_GUIDE.md target")
    else:
        print("no COLOR_GUIDE.md in the video folder: checking CAM B against CAM A only")
        print(f"{'':12s}{'R     G     B':>18s}")
    for cam, m in res.items():
        for k in ("skin", "wall"):
            if target:
                d = tuple(m[k][i] - target[k][i] for i in range(3))
                bad = max(abs(v) for v in d) > tol[k]
                ok &= not bad
                print(f"CAM {cam} {k:5s} {fmt(m[k])}   {sign(d)}{'   <- adjust' if bad else ''}")
            else:
                print(f"CAM {cam} {k:5s} {fmt(m[k])}")
    if "A" in res and "B" in res:
        ds = {k: tuple(res["B"][k][i] - res["A"][k][i] for i in range(3)) for k in ("skin", "wall")}
        ba_bad = any(max(abs(v) for v in ds[k]) > (tol or TOL)[k] for k in ds)
        ok &= not ba_bad
        print(f"B - A  skin {sign(ds['skin'])}   wall {sign(ds['wall'])}{'   <- match B to A' if ba_bad else ''}")
    if target:
        print(f"target skin {fmt(target['skin'])}   wall {fmt(target['wall'])}   {'OK' if ok else 'OUT OF RANGE'}")
    else:
        print("OK" if ok else "B DOES NOT MATCH A")

if __name__ == "__main__":
    main()
