#!/usr/bin/env python3
"""Choose the best frame for a camera change inside a pause, by looking at both cameras.

  cut_pick.py PROJECT_DIR SRC_TIME            choose the cut for the change nearest SRC_TIME and explain it
  (used by cut_check.py --pick / --snap for every camera change)

No fixed offset. For every frame of the pause it scores what the viewer would see:
  - incoming shot: every frame he is silent AND still before he speaks counts as dead (a breath, a nod,
    a look or speech is life);
  - outgoing shot: silence right after the last word is the idea landing and is free for a moment; after
    that, frames where his face is frozen count as dead (less than on the incoming shot);
  - the cut frame itself: an isolated jump on either side (a blink, a twitch) is avoided; the ramp of a breath
    or a nod before he speaks is life, and the best place for the incoming shot to start.
The frame with the lowest score wins; ties go late (the pause stays on the outgoing shot). Movement is the
frame-to-frame change inside the face box of each camera, compared with that camera's own movement while he
talks just before the pause, so it adapts to each shot, camera and speaker.
"""
import glob, io, json, os, subprocess, sys
from PIL import Image, ImageChops, ImageStat

FPS = 24000 / 1001
FRAME = 1 / FPS
LANDING = 0.35        # silence the outgoing shot may hold freely: the idea landing
W_IN, W_OUT, W_SPIKE = 1.0, 0.6, 4.0

def camera_file(root, cam):
    hits = sorted(glob.glob(os.path.join(root, "footage", f"*CAM_{cam}*")))
    return hits[0] if hits else None

def face_box(cfg, cam, w, h):
    """Upper-middle box around the speaker's face, from the camera's reframe centre when set."""
    rf = cfg.get("reframe", {}).get(cam)
    cx = (rf["center"][0] if rf else (960 if cam == "A" else 1100)) / 1920
    cy = (rf["center"][1] if rf else 520) / 1080
    x0, x1 = max(0, cx - 0.16), min(1, cx + 0.16)
    y0, y1 = max(0, cy - 0.42), min(1, cy + 0.05)
    return int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)

def frames(path, start, dur, box_fn):
    """Grey, small face crops for every frame in [start, start + dur)."""
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{max(0, start):.3f}", "-t", f"{dur:.3f}", "-i", path,
           "-vf", "scale=480:270,format=gray", "-f", "image2pipe", "-vcodec", "png", "-"]
    data = subprocess.run(cmd, capture_output=True).stdout
    out, i = [], 0
    sig = b"\x89PNG\r\n\x1a\n"
    parts = data.split(sig)[1:]
    for p in parts:
        im = Image.open(io.BytesIO(sig + p))
        out.append(im.crop(box_fn(*im.size)).resize((64, 64)))
    return out

def motion(seq):
    return [0.0] + [ImageStat.Stat(ImageChops.difference(a, b)).mean[0] for a, b in zip(seq, seq[1:])]

def pick(root, cfg, gap, out_cam, in_cam):
    """gap = (pause start, pause end) in source seconds. Returns (cut time, explanation)."""
    a, b = gap
    pre = 1.0
    t0 = a - pre
    res = {}
    for cam in {out_cam, in_cam}:
        path = camera_file(root, cam)
        seq = frames(path, t0, (b - t0) + 0.3, lambda w, h, c=cam: face_box(cfg, c, w, h))
        m = motion(seq)
        talk = sorted(m[1:int(pre * FPS)]) or [1.0]
        ref = max(0.3, talk[len(talk) // 2])          # this camera's movement while he talks
        res[cam] = (m, ref)
    def at(cam, t):
        m, ref = res[cam]
        i = int(round((t - t0) * FPS))
        return (m[i] / ref) if 0 <= i < len(m) else 1.0
    # a face at rest in a pause measures ~0.3 of its talking movement (noise); a breath or a nod before
    # speaking ramps up past 1. Alive = clearly above rest.
    alive = lambda cam, t: at(cam, t) > 0.6
    def blink(cam, t):
        # an isolated one-frame jump (blink, twitch); a ramp (breath, nod, speech starting) is life, not a spike
        v, p, n = at(cam, t), at(cam, t - FRAME), at(cam, t + FRAME)
        return v > 2.5 and p < 1.2 and n < 1.2
    best = None
    c = a + 2 * FRAME
    while c <= b - FRAME + 1e-6:
        # incoming: still, silent frames from the cut until he speaks
        dead_in, t = 0, c
        while t < b:
            if not alive(in_cam, t):
                dead_in += 1
            t += FRAME
        # outgoing: frozen frames after the landing moment
        dead_out, t = 0, a + LANDING
        while t < c:
            if not alive(out_cam, t):
                dead_out += 1
            t += FRAME
        sp = 1 if (blink(out_cam, c - FRAME) or blink(out_cam, c) or blink(in_cam, c) or blink(in_cam, c + FRAME)) else 0
        score = W_IN * dead_in + W_OUT * dead_out + W_SPIKE * sp
        if best is None or score <= best[0]:          # <= : ties go late
            best = (score, c, dead_in, dead_out, sp)
        c += FRAME
    score, c, di, do, sp = best
    why = f"in {di} still frames, out {do} frozen after landing" + (", movement spike near cut" if sp else "")
    return round(c, 3), why

def main():
    root, t = os.path.abspath(sys.argv[1]), float(sys.argv[2])
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from cut_check import levels, gaps
    cfg = json.load(open(os.path.join(root, ".tesseract-work", "video.json")))
    G = gaps(levels(os.path.join(root, cfg["dialogue_source"])))
    g = min(G, key=lambda x: 0 if x[0] - 0.4 <= t <= x[1] + 0.4 else abs((x[0] + x[1]) / 2 - t))
    shots = cfg["shots"]
    i = min(range(1, len(shots)), key=lambda k: abs(shots[k][0] - t))
    c, why = pick(root, cfg, g, shots[i - 1][2], shots[i][2])
    print(f"pause {g[0]:.2f}-{g[1]:.2f}  {shots[i-1][2]}->{shots[i][2]}  cut {c:.3f}  ({why})")

if __name__ == "__main__":
    main()
