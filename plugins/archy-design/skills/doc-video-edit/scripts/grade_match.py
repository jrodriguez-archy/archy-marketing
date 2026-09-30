#!/usr/bin/env python3
"""Match CAM B's grade to CAM A by measurement (multicam: both cameras must look the same).

  grade_match.py PROJECT_DIR            search and report the best CAM B grade
  grade_match.py PROJECT_DIR --write    also write it into .tesseract-work/video.json (then rebuild)

Renders graded frames of each camera from a throwaway copy of the project (the real .tsrct is
never touched), measures the mean skin colour (pixels with R > G > B, R - B > 25) and the hue of the wall
(frame corners above the speaker, as r/g and b/g ratios), and searches CAM B's levels gamma,
temperature, tint and saturation so both land on CAM A's. Skin decides (the same face); the wall
only guards the hue, because each angle sees a different, differently lit part of the room.
Saturation stays within -12/+25 of CAM A's. Build the project with build_video.py first; run again after a
reframe changes what the frames show. Check the result by eye on a cut.
"""
import itertools, json, os, shutil, subprocess, sys, tempfile
from PIL import Image

T = os.environ.get("TSRCT") or os.path.expanduser("~/Library/Application Support/Tesseract/bin/tsrct")

def stats(p):
    im = Image.open(p).convert("RGB")
    W, H = im.size
    px = im.load()
    skin, wall = [], []
    for y in range(int(H * 0.14), int(H * 0.58), 4):
        for x in range(int(W * 0.16), int(W * 0.88), 4):
            r, g, b = px[x, y]
            if r > g > b and r - b > 25 and 110 < r < 235:
                skin.append((r, g, b))
    for y in range(int(H * 0.06), int(H * 0.28), 5):
        for x in list(range(int(W * 0.08), int(W * 0.23), 5)) + list(range(int(W * 0.78), int(W * 0.94), 5)):
            wall.append(px[x, y])
    avg = lambda L: [sum(c[i] for c in L) / len(L) for i in range(3)] if L else [0, 0, 0]
    return avg(skin), avg(wall)

def main():
    root = os.path.abspath(sys.argv[1])
    work = os.path.join(root, ".tesseract-work")
    cfg = json.load(open(os.path.join(work, "video.json")))
    timing = json.load(open(os.path.join(work, "timing.json")))
    project = os.path.join(root, cfg["project"])
    # two mid-shot frames per camera from full-frame shots
    pick = lambda cam: [(s[4] + s[5]) / 2 for s in timing["shots"] if s[2] == cam and s[3] == "full"][:2]
    ta, tb = pick("A"), pick("B")
    if not ta or not tb:
        sys.exit("need at least one full shot of each camera")
    tmp = tempfile.mkdtemp()
    test = os.path.join(tmp, "t.tsrct")
    shutil.copy(project, test)
    base = json.load(open(os.path.join(work, "editable.json")))

    def measure(times):
        out = []
        for t in times:
            f = os.path.join(tmp, f"{t:.2f}.png")
            subprocess.run([T, "preview", "--project", test, "--time", str(t), "--output", f], check=True, capture_output=True)
            out.append(stats(f))
        n = len(out)
        return [sum(o[0][i] for o in out) / n for i in range(3)], [sum(o[1][i] for o in out) / n for i in range(3)]

    def with_b(gamma, temp, tint, sat):
        d = json.loads(json.dumps(base))
        for l in d["composition"]["layers"]:
            if l.get("type") == "Video" and l["name"].startswith("CAM B"):
                for e in l.get("effects", []):
                    f = e["effect"]
                    if f["type"] == "levels": f["gamma"] = gamma
                    if f["type"] == "temperatureTint": f["temperature"] = temp; f["tint"] = tint
                    if f["type"] == "hueSaturation": f["saturation"] = sat
        p = os.path.join(tmp, "t.json")
        json.dump(d, open(p, "w"))
        subprocess.run([T, "project", "commit", "--project", test, "--file", p], check=True, capture_output=True)

    subprocess.run([T, "project", "commit", "--project", test, "--file", os.path.join(work, "editable.json")], check=True, capture_output=True)
    skin_a, wall_a = measure(ta)
    B = {f["type"]: f for f in cfg["grade"]["B"]}
    g0 = B.get("levels", {}).get("gamma", 1.0)
    t0 = B.get("temperatureTint", {}).get("temperature", 15.0)
    s0 = B.get("hueSaturation", {}).get("saturation", 30)

    def loss(gamma, temp, tint, sat):
        with_b(gamma, temp, tint, sat)
        s, w = measure(tb)
        # skin (the same face) decides; the wall only checks the hue (r/g, b/g), not its brightness,
        # because each angle sees a different, differently lit part of the room
        hue = lambda c: (c[0] / c[1], c[2] / c[1]) if c[1] else (0, 0)
        wa, wb = hue(wall_a), hue(w)
        return (3 * sum((a - b) ** 2 for a, b in zip(s, skin_a))
                + 20000 * ((wa[0] - wb[0]) ** 2 + (wa[1] - wb[1]) ** 2)), s, w

    start = loss(g0, t0, B.get("temperatureTint", {}).get("tint", 0.0), s0)
    print(f"CAM A  skin {[round(v, 1) for v in skin_a]}  wall {[round(v, 1) for v in wall_a]}")
    print(f"CAM B now: loss {start[0]:.1f}  skin {[round(v, 1) for v in start[1]]}  wall {[round(v, 1) for v in start[2]]}")
    # coordinate descent: try +-step on one parameter at a time, keep what helps, halve the steps
    x = [g0, t0, B.get("temperatureTint", {}).get("tint", 0.0), s0]
    step = [0.04, 5.0, 4.0, 6.0]
    sat_a = {f["type"]: f for f in cfg["grade"]["A"]}.get("hueSaturation", {}).get("saturation", 30)
    lo_hi = [(0.85, 1.35), (-10, 45), (-15, 15), (max(0, sat_a - 12), sat_a + 25)]
    best_l = start[0]
    for _ in range(3):
        improved = True
        while improved:
            improved = False
            for i in range(4):
                for d in (+1, -1):
                    y = list(x)
                    y[i] = min(lo_hi[i][1], max(lo_hi[i][0], round(x[i] + d * step[i], 3)))
                    L = loss(*y)[0]
                    if L < best_l - 0.05:
                        best_l, x, improved = L, y, True
                        break
        step = [v / 2 for v in step]
    best = (best_l, *x)
    _, g, tp, ti, sa = best
    _, s, w = loss(g, tp, ti, sa)
    print(f"CAM B best: loss {best[0]:.1f}  gamma {g}  temperature {tp}  tint {ti}  saturation {sa}")
    print(f"           skin {[round(v, 1) for v in s]}  wall {[round(v, 1) for v in w]}")
    shutil.rmtree(tmp, ignore_errors=True)
    if "--write" in sys.argv:
        for f in cfg["grade"]["B"]:
            if f["type"] == "levels": f["gamma"] = g
            if f["type"] == "temperatureTint": f["temperature"], f["tint"] = float(tp), float(ti)
            if f["type"] == "hueSaturation": f["saturation"] = sa
        json.dump(cfg, open(os.path.join(work, "video.json"), "w"), indent=1, ensure_ascii=False)
        print("written to video.json: rebuild with build_video.py and check a cut by eye")

if __name__ == "__main__":
    main()
