#!/usr/bin/env python3
"""Build a DOC course video from its config.

  build_video.py PROJECT_DIR            rebuild and save the project (checkout -> build -> commit -> apply)
  build_video.py PROJECT_DIR --dry-run  write the JSON to .tesseract-work/ only, do not touch the .tsrct

PROJECT_DIR holds the .tsrct named in .tesseract-work/video.json. Assets, fonts and footage must
already be imported (see SKILL.md). The .tsrct is only written through tsrct commit / apply.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from doclib import Edit  # noqa: E402

def tsrct():
    for p in (os.environ.get("TSRCT"), os.path.expanduser("~/Library/Application Support/Tesseract/bin/tsrct"),
              os.path.expanduser("~/.local/share/Tesseract/bin/tsrct")):
        if p and os.path.exists(p):
            return p
    return "tsrct"

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = os.path.abspath(sys.argv[1])
    dry = "--dry-run" in sys.argv
    work = os.path.join(root, ".tesseract-work")
    cfg = json.load(open(os.path.join(work, "video.json")))
    project = os.path.join(root, cfg["project"])
    fonts = os.path.normpath(os.path.join(root, cfg["fonts_dir"]))
    T = tsrct()
    editable = os.path.join(work, "editable.json")
    subprocess.run([T, "project", "checkout", "--project", project, "--output", editable], check=True, capture_output=True)
    ed = Edit(cfg, fonts)
    doc, anims, audio_anims, groups = ed.document(json.load(open(editable)))
    json.dump(doc, open(editable, "w"), indent=1)
    json.dump(anims, open(os.path.join(work, "anim.json"), "w"), indent=1)
    json.dump(audio_anims, open(os.path.join(work, "audio_anim.json"), "w"), indent=1)
    json.dump(ed.timing_report(), open(os.path.join(work, "timing.json"), "w"), indent=1)
    print(f"duration {ed.duration:.2f}s  speech {ed.intro:.2f}-{ed.speech_end:.2f}  "
          f"closing {ed.ff_start or 0:.2f}-{ed.ff_end:.2f}  shots {len(cfg['shots'])}  graphics {len(groups)}")
    for g in groups:
        print(f"  {g.name:34s} {g.start:7.2f}-{g.end:7.2f}")
    for w in ed.pacing_warnings():
        print(f"  pacing: {w}")
    if dry:
        return
    subprocess.run([T, "project", "commit", "--project", project, "--file", editable], check=True)
    subprocess.run([T, "project", "apply", "--project", project, "--actions", os.path.join(work, "anim.json")], check=True)
    subprocess.run([T, "project", "apply", "--project", project, "--actions", os.path.join(work, "audio_anim.json")], check=True)
    # Verify the saved project really holds every animation (a build once lost the audio envelopes
    # without an error, so the intro music played flat and cut when its file ended).
    check = os.path.join(work, "saved_check.json")
    subprocess.run([T, "project", "checkout", "--project", project, "--output", check], check=True, capture_output=True)
    saved = {(e["target"].get("layerId"), e["target"].get("propertyType"))
             for e in json.load(open(check))["composition"]["dynamics"]["entries"]}
    missing = [a["property"] for a in anims + audio_anims
               if (a["property"]["layerId"], a["property"]["propertyType"]) not in saved]
    if missing:
        sys.exit(f"saved project is missing {len(missing)} animations, e.g. {missing[:3]}: rebuild")
    print(f"verified {len(saved)} animations in the saved project (audio envelopes: {len(audio_anims)})")

if __name__ == "__main__":
    main()
