# Audio and grade

## Dialogue

- Both cameras record the same take; use CAM A's audio as the dialogue, extracted to WAV and placed as its own Audio layers (one per contiguous segment). Camera video layers stay muted, so any camera can be on screen without changing the sound.
- Level: highpass 70 Hz + two-pass linear loudnorm to -16 LUFS, true peak -1.5 dBFS (`scripts/level_audio.sh`). The mix then measures about -16 LUFS integrated.
- Keep the original extraction and write the recipe to `audio/PROCESSING.md`.

## Music and stings

- Intro music: its own -18 LUFS derivative, gain 1.0, with the envelope from `doclib.Edit.music_envelope` (one slow, progressive descent: starts easing down 1 s before the first word, -10 dB 0.5 s into the words, then a steady fall in dB to -50 dB 0.1 s before the file ends; ~3.9 s from full to silent with a 13 s file. `timing.music_duck_lead`, `music_duck_db`, `music_floor_db`). Never let the music, or anything else, stop without a fade.
- Last dialogue segment: cos² fade over the room-tone tail after `timing.voice_end_src` (up to 0.8 s, `Edit.dialogue_envelope`), so the room tone does not cut to digital silence before the end card and the last word is untouched.
- End card sting: gain 5.6 on the end card clip (it is supplied quiet, about -35 LUFS).
- Wipe whoosh: gain 4.
- Measure the export: `ffmpeg -i out.mp4 -af ebur128=peak=true -f null -`.

## Grade

The course footage arrives log or flat (grey, low contrast); the two cameras differ.

1. `setup_project.py` measures each camera's luminance at 0.5 / 50 / 99.5 % over five frames and suggests: levels black = p0.5 - 10, white = p99.5 + 12; CAM B gamma matched so its midtone lands on CAM A's; hue/saturation +30; temperature +15.
2. Check a frame of each camera and adjust by eye (skin natural and slightly warm, blacks not crushed, the wall not teal). The suggestion is a start, not the answer.
3. **Match CAM B to CAM A: every camera must look the same** (house rule, F9.3 v5 and F9.5 v4). The cameras film the same person saying the same thing, so a cut from A to B must not change the colour of the person or the room.
   - Compare what both cameras see, on graded frames (`tsrct preview`): the skin (same face: match its hue, r/g and b/g; its level only roughly, because the side camera sees the shadow side), the wall right beside the head (level and colour; the angles may see different parts of the wall) and anything neutral such as the shirt (white balance). When they disagree, skin wins.
   - Targets: ratios within ~0.01, wall and skin highlights (p95) within a few levels. Then check an A/B cut by eye.
   - `scripts/grade_match.py <Video>` automates it: it renders graded frames of both cameras from a throwaway copy of the project, measures skin (weighted double) and wall, and searches B's gamma, temperature, tint and saturation until they land on A's (`--write` saves it to video.json; rebuild, then check the cut).
   - Behaviour of the controls: temperature moves blue; saturation warms skin but also greens a green wall; a positive `tint` is green, a negative one magenta; levels gamma shifts chroma too, so re-check after it. When skin is too cool but the wall is already right, raise saturation instead of a magenta tint (which fixes skin but turns the wall red).
   - Landed values: F9.1 B gamma 1.12 -> 1.04, temp 15 -> 20, tint -2, sat 26. F9.3 B tint +5. F9.5 (flat 4K Post) A 70/177 sat 30 temp 15; B 43/178 gamma 1.08 sat 40 temp 28 tint -5. F9.6 A 63/177 sat 30 temp 15; B 45/185 gamma 1.34 sat 64 temp 19.
4. Already graded finals (wide luminance range) get an identity grade; check them by eye too, and still match B to A.

Units: `levels` works in 0-255 (0-1 values render black); `hueSaturation.saturation` and `temperatureTint.temperature` are small-number scales (30 and 15 are moderate).

## Colour of the ground

The graphics ground is `--color-video-ground` (#EFEDD8). Exports carry it as about (240, 236, 217), the same as the published references. A player's colour management can make it look whiter; compare against a reference video in the same player before changing anything.
