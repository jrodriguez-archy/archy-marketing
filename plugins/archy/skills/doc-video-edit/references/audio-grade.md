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
3. **Match CAM B to CAM A: every camera must look the same.** The cameras film the same person saying the same thing, so a cut from A to B must not change the colour of the person or the room. Run `scripts/measure_color.py <Video>`: it measures skin and wall on three speaker shots per camera and prints B - A; adjust B one control at a time until B - A is within a few levels on both, then check an A/B cut by eye. Keep the grade moderate (saturation about +35 at most, B gamma about 0.95 to 1.15): past that it amplifies the noise and banding of flat 8-bit sources.
4. Already graded finals (wide luminance range) may need only a light match: start from an identity grade, measure, and match B to A.

**When the video folder has a `COLOR_GUIDE.md`, follow it instead:** it sets the targets, starting values, limits and any extra effect (such as grain) for that video or module. `measure_color.py` reads its skin and wall targets from that file and checks both cameras against them. Without that file there are no fixed targets: only steps 1 to 4 apply.

Units: `levels` works in 0-255 (0-1 values render black); `hueSaturation.saturation` and `temperatureTint.temperature` are small-number scales (30 and 15 are moderate). Temperature moves blue; saturation moves skin and wall away from neutral together; a positive `tint` is green, a negative one magenta; levels gamma shifts chroma too, so re-measure after it.

## Colour of the ground

The graphics ground is `--color-video-ground` (#EFEDD8). Exports carry it as about (240, 236, 217), the same as the published references. A player's colour management can make it look whiter; compare against a reference video in the same player before changing anything.
