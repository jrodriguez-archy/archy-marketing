---
name: doc-video-edit
description: Edit a DOC (Dental Ownership Collective) course video end to end in Tesseract from the raw two-camera footage, the brief and the video's graphics page in Paper: cut list, camera plan, native animated graphics (lower thirds, splits, number and closing cards), red section wipes, intro and end card, sound and grade, in the DOC house style. Use when someone wants a DOC Foundations / curriculum video edited, revised, or its proxy footage swapped for finals. Not for designing the graphics themselves (archy:doc-video) or for non-DOC videos.
---

# Edit a DOC course video

Load `archy:doc-brand`, `archy:doc-video` and the `tesseract-video` skill first and follow them. This skill adds the DOC edit system, a builder that turns a per-video config into the Tesseract project, and the review loop. Read before building:

| File | For |
|---|---|
| `references/edit-system.md` | Structure, cameras, graphics timing, cuts, sound: the house style |
| `references/motion-spec.md` | Exact motion of every graphic (lower thirds measured from the editor's asset) |
| `references/audio-grade.md` | Loudness targets, music envelope, grading log footage |
| `references/tesseract-notes.md` | Engine behaviour that matters here (units, mattes, dynamics) |

Scripts are in `scripts/` next to this file; run them with `python3` / `bash` using that absolute path.

## Setup (once per machine)

- Tesseract skills and the pinned CLI: `npx skills add mirage-hq/Tesseract` in the working folder, then install `tsrct` as `tesseract-video` > installation describes.
- Local transcription: whisper.cpp built in the user folder (no admin rights needed):
  `python3 -m venv ~/.local/whisper-venv && ~/.local/whisper-venv/bin/pip install cmake`, clone `github.com/ggml-org/whisper.cpp` into `~/.local/whisper.cpp`, build `whisper-cli` with that cmake, and download `ggml-medium.en.bin` to `~/.cache/whisper/`. `scripts/transcribe.sh` finds them there.
- Python Pillow and ffmpeg/ffprobe on PATH. The DOC brand kit's Satoshi files (Regular, Medium, Bold, Black).

## Project layout

```
<Video>/
  footage/        *_CAM_A.mp4, *_CAM_B.mp4, Intro_*.mp4, 03_Transitions.mp4, 04_End Card.mp4
  audio/music/    the intro music        audio/dialogue/  (generated)
  references/     reference edits, the lower-third asset
  exports/        <Video>_vN.mp4         Previews/  filmstrips
  <Video>.tsrct
  .tesseract-work/video.json   the whole edit as data (plus transcript, checks, NOTES.md)
```

## Workflow

1. **Material.** Probe every file. Check the cameras are one synced take (same duration, identical audio) and look at frames of each (framing, log or graded, anything burned in). Check whether the cameras are already cut (`*_Post_*`, or the editor says so): then the brief's cuts are done: use the whole file, no internal cuts and no trim of the open or close, unless the user explicitly asks (edit-system > Cuts). Ask only what changes the edit.
2. **Transcript.** `transcribe.sh footage/<CAM_A> .tesseract-work` -> `words.json` + `transcript.srt`.
3. **Graphics.** Read the video's page in `DOC - Videos Foundations` (one artboard per brief note, template code in the name). Map each to a builder type: S3 `speaker_lt`, L1 `caption_lt`, T1 `split_list`, T2 `split_numbered` (`highlight: n` for a section marker such as the Big Three), T4 `split_blocks`, T7 `framework_card`, T11 `number_card`, N3 `equation_split`, N6 `split_equals`, N7 `split_result`, N8 `split_pairs`, T10 `closing_card` (at the end) or, inside the video, `full_card` (multi-line blocks) / `statement_card` (line 2 on its own word). `templates/video.json` has an example of each. Copy the text exactly from the artboard. For a template with no builder yet (charts, diagrams, icons, heroes), build it natively in the same motion language and add the builder to `doclib.py`; say it is new.
4. **Edit plan for approval.** From the brief and the transcript: the cut list with exact source times (waveform-checked with `wave.py ... --words .tesseract-work/words.json`), the camera plan, each graphic's in/out and item reveal words, the 2-3 wipe points, intro/closing handling, the estimated runtime, open questions. Wait for the OK.
5. **Setup.** `setup_project.py <Video>`: creates the `.tsrct`, imports footage, bookends and fonts, levels dialogue and music, suggests the grade, writes `video.json` from `templates/video.json`. Check one frame per camera and adjust the grade by eye, then after the first build match CAM B to CAM A with `measure_color.py <Video>` (audio-grade > Grade). When the video folder has a `COLOR_GUIDE.md`, grade to it instead. Also on a swap to finals.
6. **Fill `video.json`**: `segments` (kept dialogue ranges), `shots` (source in, out, camera, framing: `full`, `punch`, `split`, `split2`, `card`), `wipes`, `closing.start_src`, `timing.voice_end_src`, `graphics`. All times are source seconds on the camera clock. Delete the template's example graphics you do not use.
7. **Build.** First `cut_check.py <Video> --pick`: every camera change with the words either side, the silence each shot holds and, for each one, the frame `cut_pick.py` chooses by looking at both cameras in the pause (edit-system > Cameras, "Where to cut"). Fix every flag (SHORT, SHORT-PAUSE, IN-SPEECH, MID-SENTENCE, SANDWICH), apply the choices with `--snap`, and watch every cut that moved (and every LOOK) with psheet. Then `build_video.py <Video>` (checkout, build, commit, apply keyframes). Rebuild after every config change; never hand-edit the `.tsrct`.
8. **Review.** `psheet.py <Video>/<Video>.tsrct out.png 6 t1 t2 ...`: every graphic at its hold frame against the Paper artboard, every lower third at 24 fps in and out and at its hold frame on its actual shot (it must not cover the face, above all after a reframe), every cut, both wipes, the closing handoff. Fix and rebuild.
9. **Export and verify.** `tsrct export --fps 24 --output exports/<Video>_vN.mp4`; `scripts/measure_color.py <Video> --export <file>` (B - A within a few levels, and OK against the targets when the folder has a `COLOR_GUIDE.md`); loudness (target -16 LUFS); re-transcribe the export and read each join and the last word; contact sheet of the export to `Previews/`. Scan the export for black or dropped frames: `ffmpeg -i <export> -vf "scale=192:108,signalstats,metadata=print:key=lavfi.signalstats.YAVG" -an -f null - 2>&1` and flag any frame with YAVG < 45 outside the bookends; scan the left and right halves too (`crop=96:108:0:0` and `crop=96:108:96:0` after the scale), because the glitch can blank only the camera half of a split (F9.2 v4 at a split entry: full-frame average 118, left half 17). Fix by moving that cut 2 frames inside its pause (F9.4 v2 had one black frame on a camera cut that the preview renders fine: a render glitch; re-export and re-scan).
10. **Deliver.** The file, runtime, what changed, the checks actually run, what still needs a human listen or a decision. Keep `.tesseract-work/NOTES.md` (from `templates/NOTES.md`) current.

## Revisions

Change `video.json` (or `doclib.py` for a house-style change that should apply to every video), rebuild, re-check the touched moments and their neighbours, export `_vN+1`. Keep earlier exports.

## Swapping proxy footage for finals

When final camera files replace the proxies in `footage/` (same names):
1. `setup_project.py <Video> --swap --dry-run`: reports each camera's offset against the current dialogue. 0.00 means every time in `video.json` still holds; otherwise shift all source times by the offset first.
2. `setup_project.py <Video> --swap`: imports the finals as new asset IDs, re-extracts and re-levels the dialogue, re-suggests the grade (finals may already be graded).
3. Check the grade by eye, rebuild, re-verify the joins and the ending (a new file can end at a different point: update `timing.voice_end_src` and the last segment), export the next version. Nothing else changes.
