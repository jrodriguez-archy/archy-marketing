# DOC course videos: colour guide (Module 9 house grade)

Reference: **F9.2 The Big Three Market Concepts, v6** (2026-09-30). Use this guide to grade every DOC Foundations video
the same way. The grade is not a fixed set of numbers to paste: each file arrives slightly different, so we match
**measured targets**, and the F9.2 settings are the starting point.

## 1. Targets (what the export must measure)

Measured on the 1080p export, 8-bit RGB, with `scripts/measure_color.py` (see section 4).

| Zone | Target R G B | Tolerance | What it is |
|---|---|---|---|
| Skin | **191 154 133** | ±5 per channel | The speaker's face, upper half of the frame |
| Wall | **94 106 94** | ±6 per channel | Background in the two top corners of the frame |

- The targets are the median CAM A of the six Module 9 videos (F9.1-F9.6). CAM A was already consistent across them; CAM B was not.
- **Both cameras hit the same targets.** A cut from A to B must not change the colour of the person or the room. B - A should be within a few levels on skin and wall.
- Look: natural, slightly warm skin; a soft grey-green wall, not teal; blacks not crushed; no clipped highlights on the forehead.

## 2. Starting grade (F9.2 v6)

Effects on each camera layer, in this order (Tesseract units: levels 0-255; saturation and temperature small-number scales).

| Effect | CAM A (frontal) | CAM B (side) |
|---|---|---|
| Levels | black **65**, white **176**, gamma **1.07**, output 0-255 | black **61**, white **164**, gamma **1.00**, output 0-255 |
| Hue/Saturation | saturation **+30** | saturation **+15** |
| Temperature/Tint | temperature **+15**, tint 0 | temperature **+15**, tint 0 |
| Grain | amount **0.7**, size 1.0, softness 0.5, seed 1 | same |

Result on the F9.2 v6 export: A skin 187 151 129 / wall 95 106 93; B skin 193 156 132 / wall 92 106 93. B - A: skin +6 +5 +3, wall -3 0 0 (before: B wall +20 over A). All within tolerance.

Why B is different from A: the side camera sees a flatter picture (skin and wall closer in level), so it needs a little
more contrast (a narrower levels range) to bring its wall down to A's without darkening the skin. More contrast also
raises colour intensity, so B takes less saturation (+15). Without this, B's wall comes out 15-25 levels lighter than A's
in every Module 9 video, which reads as a jump on every cut.

## 3. How to grade a video

1. Start from the F9.2 values above for both cameras.
2. Build, then run `measure_color.py <Video>` (renders frames of the project) and read the differences.
3. Adjust CAM A first, then CAM B, one control at a time:
   - Skin and wall both too dark or too light: move **gamma** (up = lighter mids) or the **black** point.
   - Wall too light but skin right (typical on CAM B): **narrow the levels range** (raise black, lower white slightly) and re-check the skin.
   - Skin right but too light overall: raise the **white** point a little (it pulls the highlights down more than the wall).
   - Skin too red / wall too green or teal: **lower saturation** (it moves both toward neutral). Do not go above +35.
   - Whole picture too cool or warm: **temperature** (moves blue). Tint only for a clear green/magenta cast.
4. Rebuild and measure again until both cameras read OK, then check one A/B cut by eye.
5. Export with Tesseract's direct export (section 5) and measure the export once more: `measure_color.py <Video> --export <file.mp4>`.

Limits: saturation +35 at most, B gamma between 0.95 and 1.15, levels range (white - black) not under ~95. Each of these
past its limit amplifies the noise and the banding of the source (section 6).

## 4. Measuring

```
python3 <skill>/scripts/measure_color.py "<Video folder>"                      # built project, preview frames
python3 <skill>/scripts/measure_color.py "<Video folder>" --export <file.mp4>  # an export
```

It takes three speaker shots per camera (full frames, not splits, cards or punch-ins), measures skin and wall, prints
them against the targets and prints B - A. "OK" means every value is within tolerance.

## 5. Export

Standard (the current proxy-quality `_Post` sources):

```
tsrct export --project "<Video>.tsrct" --fps 24 --output exports/<Video>_vN.mp4
```

The fine grain (section 2) does most of the work against the background steps. Tested on F9.2 (2026-09-30): with grain,
the direct export and a ProRes master re-encoded with x264 CRF 16 look the same at normal viewing; only with exaggerated
contrast does the direct export show slightly more blocking (block index 1.18 vs 1.07). The ProRes route costs ~70 min and
~30 GB of temporary disk per video against ~15-25 min, so it is not worth it on 8-bit proxy sources.

Optional, only for 10-bit final camera files (then it keeps detail the direct export loses):

```
bash <skill>/scripts/export_final.sh "<Video folder>" exports/<Video>_vN.mp4
```

It exports a ProRes master, encodes the MP4 with x264 CRF 16 (`tune grain`) and deletes the master (needs ~4 GB free per
minute of video while it runs: run one at a time).

After every export: `measure_color.py <Video> --export <file.mp4>` must read OK, and scan for dark frames (left and right
halves too, see the skill's step 9).

## 6. Why the background looks noisy or banded, and what to ask for in the finals

Diagnosis on F9.2 (2026-09-30):

1. **Source (main cause).** The `_Post` camera files are 4K H.264, 8-bit 4:2:0, only ~21 Mbps (F9.1: 1080p at 6.8 Mbps),
   and shot flat/log. The raw file already has the background gradient in steps (a patch of wall uses only 10-16 grey levels)
   and compression blocks. We cannot recover what is not in the file.
2. **The grade amplifies it.** Stretching a flat 8-bit picture to full contrast (x2.3) makes each step and the noise about twice
   as visible. High saturation adds colour noise.
3. **Tesseract's direct export adds a little blocking** (~10 Mbps H.264). With the grain on, this is minor at normal viewing (section 5).

What we do: moderate grade (limits above) and fine grain (0.7) that dissolves the steps into an even texture. With 10-bit
finals, the ProRes -> x264 export (section 5) is worth adding.

What to ask the editor for the final camera files:
- **10-bit** files at a high bitrate: ProRes 422 HQ (preferred) or H.265/HEVC 10-bit 4:2:2, 100 Mbps or more for 4K.
- Ideally already colour-corrected (Rec.709) in the editor's grading tool from the camera originals. Then the grade here is only a light match.
- If they stay log, the same 10-bit files let us stretch the contrast without steps.
- No burned-in proxy icon.

When finals arrive: `setup_project.py <Video> --swap`, then **re-grade from section 3** (finals may already be graded) and measure again.

## 7. Applying this to the other Module 9 videos (F9.1, F9.3-F9.6)

For each video folder:
1. Copy this file into the folder.
2. In `.tesseract-work/video.json`, set `grade.A` and `grade.B` to the section 2 values (keep a copy of the old grade as `grade_previous`).
3. Rebuild (`build_video.py`), run `measure_color.py`, adjust per section 3 until both cameras read OK.
4. Export the next version with the direct export (section 5), measure it and scan it for dark frames.

Current state measured on their latest exports (2026-09-30): CAM A is close to the targets in all of them (F9.4 and F9.5 walls
~6-8 levels dark). CAM B's wall is too light in F9.1 (+13), F9.5 (+12) and F9.6 (+26); F9.4 B skin is too red; F9.5 and F9.6 B skin
is ~10 levels dark.
