#!/usr/bin/env python3
"""Measure the picture offset of CAM B against CAM A (same take, same audio).

  cam_sync.py PROJECT_DIR [windows]      default 12 windows of 20 s across the take

Identical audio does not mean the pictures line up: an editor's export can carry a sub-frame
offset, which shows as a jump on every A/B cut (F9.3: CAM B 0.85 frame early). This compares the
frame-to-frame motion of both cameras (head and hand moves are seen from both angles), finds the
lag with sub-frame precision per window and prints the median. Put the result in video.json as
"cam_offset": {"B": seconds} (added to CAM B's source time); re-run to check it reads ~0.
"""
import glob, json, os, statistics, subprocess, sys

def motion(f, ss, dur, w=96, h=54):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", f, "-vf",
                        f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    sz = w * h
    fr = [b[i * sz:(i + 1) * sz] for i in range(len(b) // sz)]
    return [sum(abs(x - y) for x, y in zip(fr[i], fr[i - 1])) / sz for i in range(1, len(fr))]

def lag(a, b, maxlag=4):
    """Frames by which B's motion comes before A's (negative = B early), sub-frame."""
    n = min(len(a), len(b)) - 2 * maxlag
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    va = sum((x - ma) ** 2 for x in a[maxlag:maxlag + n]) ** .5
    c = {}
    for k in range(-maxlag, maxlag + 1):
        seg = b[maxlag + k:maxlag + k + n]
        vb = sum((x - mb) ** 2 for x in seg) ** .5
        c[k] = sum((a[maxlag + i] - ma) * (seg[i] - mb) for i in range(n)) / (va * vb or 1)
    k = max(c, key=c.get)
    d = 0.0
    if -maxlag < k < maxlag:
        y0, y1, y2 = c[k - 1], c[k], c[k + 1]
        d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2) if (y0 - 2 * y1 + y2) else 0.0
    return k + d, c[k]

def main():
    root = os.path.abspath(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    cfg = json.load(open(os.path.join(root, ".tesseract-work", "video.json")))
    a = sorted(glob.glob(os.path.join(root, "footage", "*CAM_A*.mp4")))[0]
    b = sorted(glob.glob(os.path.join(root, "footage", "*CAM_B*.mp4")))[0]
    fps = eval(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate",
                               "-of", "csv=p=0", a], capture_output=True, text=True).stdout.strip())
    dur = cfg["assets"]["cam_ms"] / 1000
    off_now = cfg.get("cam_offset", {}).get("B", 0.0)
    lags = []
    for i in range(n):
        ss = 5 + (dur - 30) * i / max(1, n - 1)
        k, c = lag(motion(a, ss, 20), motion(b, ss + off_now, 20))
        print(f"  {ss:7.1f} s  lag {k:+.2f} frames  corr {c:.2f}")
        if c > 0.7:
            lags.append(k)
    med = statistics.median(lags)
    print(f"median lag {med:+.2f} frames ({med / fps * 1000:+.0f} ms) with cam_offset.B = {off_now:+.4f}")
    print(f"-> set \"cam_offset\": {{\"B\": {off_now + med / fps:+.4f}}}" if abs(med) > 0.25 else "-> in sync")

if __name__ == "__main__":
    main()
