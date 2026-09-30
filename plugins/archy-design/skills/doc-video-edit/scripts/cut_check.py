#!/usr/bin/env python3
"""Check (and optionally snap) the camera cuts of a DOC video.

  cut_check.py PROJECT_DIR           report every shot change in .tesseract-work/video.json
  cut_check.py PROJECT_DIR --snap    move camera changes (A<->B, punch in/out) onto the nearest
                                     breath gap and write video.json (video_prev.json keeps the old)

House rule: a camera change lands at a sentence end with a pause of ~350 ms or more (dialogue
below -40 dBFS), cut ~4 frames (0.17 s) before the next sentence's first word, so the new angle
arrives with the new thought. Shots hold ~8-20 s, never under ~5 s. Changes into or out of a split / card enter on
their anchor word and are only reported, never moved; dialogue joins are never moved.

Flags: SHORT (camera shot < 5 s), SHORT-PAUSE (pause at the cut < 350 ms), IN-SPEECH (cut while he is talking), SANDWICH (short shot
between two graphics), MID-SENTENCE (camera change or punch-in not after a sentence end: . ? ! on the word before).
Word times come from words.json (whisper), which can lag the audio by 0.3-0.5 s: the waveform
decides, the words only label.
"""
import array, json, math, os, shutil, subprocess, sys

GAP_DB, GAP_MS, SEARCH, LEAD = -40.0, 120, 0.4, 0.17
PAUSE_MS, MIN_SHOT = 350, 5.0   # house rule (edit-system > Cameras): pause >= ~350 ms under -40 dBFS; shots >= ~5 s
GRAPHIC = {"split", "split2", "card"}

def levels(wav):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    a = array.array("h", raw)
    return [20 * math.log10(max(1e-6, math.sqrt(sum(x * x for x in a[i:i + 160]) / 160) / 32768))
            for i in range(0, len(a) - 160, 160)]

def gaps(db):
    out, run = [], None
    for i, d in enumerate(db + [0]):
        if d < GAP_DB:
            run = i if run is None else run
        elif run is not None:
            if (i - run) * 10 >= GAP_MS:
                out.append((run / 100, i / 100))
            run = None
    return out

def main():
    root = os.path.abspath(sys.argv[1])
    snap = "--snap" in sys.argv
    work = os.path.join(root, ".tesseract-work")
    cfg = json.load(open(os.path.join(work, "video.json")))
    db = levels(os.path.join(root, cfg["dialogue_source"]))
    G = gaps(db)
    wpath = os.path.join(work, "words.json")
    words = json.load(open(wpath)) if os.path.exists(wpath) else []
    shots = cfg["shots"]

    def level_at(t):
        i = int(t * 100)
        return max(db[max(0, i - 3):i + 3] or [-120])

    def near_gap(t):
        best = None
        for a, b in G:
            if a - SEARCH <= t <= b + SEARCH:
                cand = max(a, b - LEAD)
                d = abs(cand - t)
                if best is None or d < best[0]:
                    best = (d, cand, a, b)
        return best

    def before(t):
        # whisper can lag, never lead: a word that starts before the cut was said before it
        return [w for w in words if w[0] < t - 0.02]

    def clause_end(t):
        """True when the word before the cut closes a sentence (. ? !)."""
        prev = before(t)
        return bool(prev) and prev[-1][2].rstrip()[-1:] in ".?!"

    def ctx(t):
        b = [w[2] for w in before(t)][-3:]
        a = [w[2] for w in words if w[0] >= t - 0.02][:3]
        return f"{' '.join(b)} | {' '.join(a)}"

    flags_total, moved = 0, 0
    print(f"{'#':>2} {'cut':>7} {'shot':>5}  change                 level  flags / suggestion        words")
    for i in range(1, len(shots)):
        p, s = shots[i - 1], shots[i]
        t, dur = s[0], s[1] - s[0]
        join = abs(p[1] - s[0]) > 0.01
        kind = "join" if join else ("graphic" if (s[3] in GRAPHIC or p[3] in GRAPHIC) else "camera")
        lv = level_at(t)
        flags = []
        if s[3] not in GRAPHIC and dur < MIN_SHOT:
            flags.append("SHORT")
        if (i + 1 < len(shots) and s[3] not in GRAPHIC and p[3] in GRAPHIC and shots[i + 1][3] in GRAPHIC and dur < 5.0):
            flags.append("SANDWICH")
        sug = ""
        if kind == "camera":
            if lv > GAP_DB:
                flags.append("IN-SPEECH")
            if not clause_end(t):
                flags.append("MID-SENTENCE")
            g = near_gap(t)
            if g and (g[3] - g[2]) * 1000 < PAUSE_MS:
                flags.append("SHORT-PAUSE")
            if g and abs(g[1] - t) > 0.02:
                sug = f"-> {g[1]:.2f} (gap {g[2]:.2f}-{g[3]:.2f})"
                if snap:
                    p[1] = s[0] = round(g[1], 2)
                    moved += 1
            elif not g:
                sug = "no gap within 0.4 s"
        flags_total += len(flags)
        change = f"{p[2]}{p[3]}->{s[2]}{s[3]}" + (" JOIN" if join else "")
        print(f"{i:2d} {t:7.2f} {dur:5.2f}  {change:22s} {lv:5.0f}  {' '.join(flags + [sug]):25s} {ctx(t)[:60]}")
    print(f"\n{flags_total} flags")
    if snap and moved:
        shutil.copy(os.path.join(work, "video.json"), os.path.join(work, "video_prev.json"))
        json.dump(cfg, open(os.path.join(work, "video.json"), "w"), indent=1, ensure_ascii=False)
        print(f"snapped {moved} camera changes (previous config in video_prev.json)")

if __name__ == "__main__":
    main()
