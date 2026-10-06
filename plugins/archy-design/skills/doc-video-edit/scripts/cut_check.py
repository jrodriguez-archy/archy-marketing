#!/usr/bin/env python3
"""Report the camera cuts of a DOC video and flag the measurable errors. Writes nothing.

  cut_check.py PROJECT_DIR           report every shot change in .tesseract-work/video.json

House rule (edit-system > Cameras, "Where to cut"): a camera change goes where a thought ends, in a real
pause, and the frame inside the pause is chosen by watching it. This script only catches what can be
measured (a cut in speech, mid-sentence, in a short pause, a short shot); it never chooses or moves a cut.

Columns: out = silence the outgoing shot holds before the cut, in = silence the incoming shot shows before
he speaks (both from the waveform). Flags: MID-SENTENCE (no . ? ! on the word before), IN-SPEECH (cut while
he is talking), SHORT-PAUSE (pause < 350 ms), SHORT (camera shot < 5 s), SANDWICH (short shot between two
graphics), LOOK (either shot holds more than ~1 s of silence at the cut: watch the frames and decide; a
shorter silence is the editor's call, not a fault). For every LOOK the report prints a psheet.py line with those frames.
Word times come from words.json (whisper), which can drift 0.3-1 s: the waveform decides, the words only label.
"""
import array, json, math, os, subprocess, sys

GAP_DB, GAP_MS, SEARCH = -40.0, 120, 0.4
FRAME = 1001 / 24000
LOOK_IN, LOOK_OUT = 1.0, 1.0    # only "worth a look" thresholds, not placement rules
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
                # the pause nearest to the cut
                cand = (a + b) / 2
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

    tpath = os.path.join(work, "timing.json")
    tshots = json.load(open(tpath))["shots"] if os.path.exists(tpath) else []
    def edit_of(t):
        """edit time of a source cut, from the last build (timing.json)"""
        for a, b, c, f, ea, eb, *z in tshots:
            if abs(a - t) < 0.02:
                return ea
        return None

    flags_total, look = 0, []
    print(f"{'#':>2} {'cut':>7} {'shot':>5}  change                 out   in   flags / suggestion        words")
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
            if not g:
                sug = "no pause within 0.4 s"
        # silence each side shows (speech edges at about -45 dBFS)
        i_ = int(p[1] * 100)
        while i_ > 0 and db[i_] < -45: i_ -= 1
        sil_out = max(0.0, p[1] - (i_ + 1) / 100)
        j_ = int(s[0] * 100)
        while j_ < len(db) - 1 and db[j_] < -45: j_ += 1
        sil_in = max(0.0, j_ / 100 - s[0])
        under_wipe = any(abs(t - w) < 0.05 for w in cfg.get("wipes", []))
        if (kind != "graphic" or join) and not under_wipe and (sil_in > LOOK_IN or sil_out > LOOK_OUT):
            flags.append("LOOK")
            if edit_of(t) is not None:
                e = edit_of(t)
                look.append(" ".join(f"{e + k * FRAME:.3f}" for k in range(-4, 5)))
        flags_total += len(flags)
        change = f"{p[2]}{p[3]}->{s[2]}{s[3]}" + (" JOIN" if join else "")
        print(f"{i:2d} {t:7.2f} {dur:5.2f}  {change:22s} {sil_out:4.2f} {sil_in:4.2f}  {' '.join(flags + [sug]):25s} {ctx(t)[:60]}")
    print(f"\n{flags_total} flags")
    if look:
        print("\nWatch these cuts (9 frames around each, edit times of the last build):")
        for l in look:
            print(f"  psheet.py <Video>/<Video>.tsrct look.png 9 {l}")

if __name__ == "__main__":
    main()
