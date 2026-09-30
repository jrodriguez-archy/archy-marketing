#!/usr/bin/env python3
"""Prepare a DOC video project for build_video.py, or swap its camera files.

  setup_project.py PROJECT_DIR              first setup: create the .tsrct, import footage, bookends,
                                            music, fonts, level dialogue + music, suggest the grade,
                                            write .tesseract-work/video.json (from the template)
  setup_project.py PROJECT_DIR --swap       new camera files (proxy -> final) are in footage/: measure
                                            their offset against the current dialogue, import them as
                                            new asset IDs, re-level the dialogue, re-suggest the grade
  add --dry-run to only report, --regrade to overwrite an existing grade

File naming inside PROJECT_DIR (as delivered by the editor):
  footage/*CAM_A*.mp4, footage/*CAM_B*.mp4, footage/Intro*.mp4, footage/*Transition*.mp4,
  footage/*End Card*.mp4, audio/music/*.mp3|wav (the intro music). Fonts: the brand kit's
  Satoshi files (fonts_dir in video.json, default ../../brand/fonts).
"""
import array, glob, json, math, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.environ.get("TSRCT") or os.path.expanduser("~/Library/Application Support/Tesseract/bin/tsrct")
DRY, SWAP, REGRADE = "--dry-run" in sys.argv, "--swap" in sys.argv, "--regrade" in sys.argv

def run(*a, capture=True):
    r = subprocess.run(list(a), capture_output=capture, text=True)
    if r.returncode:
        sys.exit(f"failed: {' '.join(a)}\n{r.stdout}{r.stderr}")
    return r.stdout

def duration_ms(f):
    return int(round(float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f)) * 1000))

def one(pattern, root):
    hits = sorted(glob.glob(os.path.join(root, pattern)))
    return hits[0] if hits else None

def pcm(f, ss, t, sr=8000):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(t), "-i", f, "-vn", "-ac", "1",
                        "-ar", str(sr), "-f", "s16le", "-"], capture_output=True).stdout
    return array.array("h", b)

def env(a, h=80):
    return [math.sqrt(sum(x * x for x in a[i:i + h]) / h) for i in range(0, len(a) - h, h)]

def offset(new, old, at=100.0, win=20.0, search=3.0):
    """Seconds to add to old source times to land on the same audio in `new` (10 ms steps)."""
    ref, big = env(pcm(old, at, win)), env(pcm(new, at - search, win + 2 * search))
    best = None
    for lag in range(0, len(big) - len(ref)):
        seg = big[lag:lag + len(ref)]
        n = math.sqrt(sum(x * x for x in ref) * sum(y * y for y in seg)) or 1
        c = sum(x * y for x, y in zip(ref, seg)) / n
        if best is None or c > best[0]:
            best = (c, lag)
    return round(best[1] / 100 - search, 2), best[0]

def luma_percentiles(f, times):
    from PIL import Image
    import io
    hist = [0] * 256
    for t in times:
        b = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", f, "-frames:v", "1", "-f", "image2pipe",
                            "-vcodec", "png", "-"], capture_output=True).stdout
        for i, v in enumerate(Image.open(io.BytesIO(b)).convert("L").histogram()):
            hist[i] += v
    n, out, c = sum(hist), {}, 0
    for i, v in enumerate(hist):
        c += v
        for p in (0.005, 0.5, 0.995):
            if p not in out and c >= n * p:
                out[p] = i
    return out[0.005], out[0.5], out[0.995]

def suggest_grade(cams, dur_s):
    """Log/flat footage -> levels around the 0.5-99.5 % luminance range, B matched to A's midtone,
    +30 saturation, +15 temperature. Already-graded footage (wide range) -> identity."""
    times = [dur_s * k for k in (0.1, 0.3, 0.5, 0.7, 0.9)]
    stats = {c: luma_percentiles(f, times) for c, f in cams.items()}
    grade, target = {}, None
    for c in ("A", "B"):
        lo, mid, hi = stats[c]
        if hi - lo > 200:
            grade[c] = [{"type": "levels", "inputBlack": 0, "inputWhite": 255, "gamma": 1.0, "outputBlack": 0, "outputWhite": 255},
                        {"type": "hueSaturation", "hue": 0, "saturation": 0, "lightness": 0},
                        {"type": "temperatureTint", "temperature": 0.0, "tint": 0.0}]
            continue
        black, white = max(0, lo - 10), min(255, hi + 12)
        m = (mid - black) / (white - black)
        gamma = 1.0 if target is None else round(math.log(m) / math.log(target), 2)
        target = target or m
        grade[c] = [{"type": "levels", "inputBlack": black, "inputWhite": white, "gamma": gamma, "outputBlack": 0, "outputWhite": 255},
                    {"type": "hueSaturation", "hue": 0, "saturation": 30, "lightness": 0},
                    {"type": "temperatureTint", "temperature": 15.0, "tint": 0.0}]
    return grade, stats

def next_id(base, cfg_assets):
    used = set(str(v) for v in cfg_assets.values())
    n = 1
    while (f"{base}{n if n > 1 else ''}") in used:
        n += 1
    return f"{base}{n if n > 1 else ''}"

def main():
    root = os.path.abspath(sys.argv[1])
    work = os.path.join(root, ".tesseract-work")
    os.makedirs(work, exist_ok=True)
    vpath = os.path.join(work, "video.json")
    cfg = json.load(open(vpath)) if os.path.exists(vpath) else json.load(open(os.path.join(HERE, "..", "templates", "video.json")))
    name = os.path.basename(root)
    cfg["project"] = cfg.get("project") or f"{name}.tsrct"
    if cfg["project"].startswith("<"):
        cfg["project"] = f"{name}.tsrct"
    project = os.path.join(root, cfg["project"])
    A = cfg.setdefault("assets", {})
    cams = {"A": one("footage/*CAM_A*.mp4", root), "B": one("footage/*CAM_B*.mp4", root)}
    if not all(cams.values()):
        sys.exit("need footage/*CAM_A*.mp4 and footage/*CAM_B*.mp4")
    cam_ms = duration_ms(cams["A"])
    print(f"cameras: {cam_ms / 1000:.2f} s (A), {duration_ms(cams['B']) / 1000:.2f} s (B)")

    if SWAP:
        old = os.path.join(root, cfg.get("dialogue_source", ""))
        if not os.path.exists(old):
            sys.exit("video.json has no dialogue_source to compare against")
        for c in ("A", "B"):
            off, corr = offset(cams[c], old)
            print(f"CAM {c}: offset {off:+.2f} s vs current dialogue (corr {corr:.3f})")
            if abs(off) > 0.005:
                print("  -> not aligned: shift every source time in segments/shots/wipes/graphics by this offset "
                      "(or re-sync the files) before building")
    if DRY:
        print(json.dumps({"cameras": cams, "cam_ms": cam_ms}, indent=1))
        return

    if not os.path.exists(project):
        run(T, "project", "create", "--project", project)
    ids = {}
    if SWAP or "camA" not in A:
        for c in ("A", "B"):
            ids[c] = next_id(f"cam{c}", A) if SWAP else f"cam{c}"
            run(T, "project", "import-video", "--project", project, "--file", cams[c], "--asset-id", ids[c])
            A[f"cam{c}"] = ids[c]
        A["cam_ms"] = cam_ms
        # frame width of the camera files: doclib scales UHD layers to the 1920 frame
        A["cam_width"] = int(run("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width",
                                 "-of", "csv=p=0", cams["A"]).strip())
    if not SWAP:
        for key, pat in (("intro", "footage/Intro*.mp4"), ("wipe", "footage/*Transition*.mp4"), ("endcard", "footage/*End*Card*.mp4")):
            f = one(pat, root)
            if f and key not in A:
                run(T, "project", "import-video", "--project", project, "--file", f, "--asset-id", key)
                A[key], A[f"{key}_ms"] = key, duration_ms(f)
        music = one("audio/music/*.mp3", root) or one("audio/music/*.wav", root)
        if music and "music" not in A:
            lev = os.path.join(root, "audio/music", os.path.splitext(os.path.basename(music))[0] + "_lev-18.wav")
            print(run(os.path.join(HERE, "level_audio.sh"), music, lev, "-18"))
            run(T, "project", "import-asset", "--project", project, "--file", lev, "--asset-id", "intro-music-lev", "--kind", "audio")
            A["music"], A["music_ms"] = "intro-music-lev", duration_ms(lev)
        fonts = os.path.normpath(os.path.join(root, cfg.get("fonts_dir", "../../brand/fonts")))
        for w in ("Regular", "Medium", "Bold", "Black"):
            run(T, "project", "import-font", "--project", project, "--file", os.path.join(fonts, f"Satoshi-{w}.otf"))

    # Dialogue = CAM A audio as its own layers, leveled to -16 LUFS.
    os.makedirs(os.path.join(root, "audio/dialogue"), exist_ok=True)
    tag = ids.get("A", "camA")
    raw = os.path.join(root, f"audio/dialogue/dialogue_{tag}.wav")
    lev = os.path.join(root, f"audio/dialogue/dialogue_{tag}_lev-16.wav")
    run("ffmpeg", "-v", "error", "-y", "-i", cams["A"], "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s24le", raw)
    print(run(os.path.join(HERE, "level_audio.sh"), raw, lev, "-16", "highpass=f=70,"))
    did = next_id("dialogue-lev", A) if SWAP or "dialogue" in A else "dialogue-lev"
    run(T, "project", "import-asset", "--project", project, "--file", lev, "--asset-id", did, "--kind", "audio")
    A["dialogue"], A["dialogue_ms"] = did, duration_ms(lev)
    cfg["dialogue_source"] = os.path.relpath(raw, root)

    if REGRADE or SWAP or not cfg.get("grade"):
        grade, stats = suggest_grade(cams, cam_ms / 1000)
        cfg["grade"] = grade
        print("grade suggestion (luma p0.5 / p50 / p99.5):", stats, "-> review on a frame and adjust by eye")
    json.dump(cfg, open(vpath, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {vpath}")

if __name__ == "__main__":
    main()
