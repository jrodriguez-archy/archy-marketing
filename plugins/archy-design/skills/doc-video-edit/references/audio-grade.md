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

**The house grade is `references/color-guide.md`.** It holds the measured targets for skin and wall that both cameras must hit, the starting values for each camera, the limits, the grain and the export. Every video is graded the same way:

1. Start both cameras from the guide's starting values (section 2), with the grain.
2. Build, then run `scripts/measure_color.py <Video>`: it measures skin and wall on three speaker shots per camera and prints them against the targets and B - A.
3. Adjust one control at a time as the guide's section 3 describes (CAM A first, then CAM B) until it reads OK, staying inside the limits (saturation +35 at most, B gamma 0.95 to 1.15, levels range not under ~95): past them the grade amplifies the noise and banding of the source.
4. Check one A/B cut by eye: same person, same words, so a cut must not change the colour of the person or the room.
5. Export (direct `tsrct export`) and measure the export with `measure_color.py <Video> --export <file>`.

Already graded finals (wide luminance range) may need only a light match: start from an identity grade, measure, and adjust to the same targets.

Units: `levels` works in 0-255 (0-1 values render black); `hueSaturation.saturation` and `temperatureTint.temperature` are small-number scales (30 and 15 are moderate). Temperature moves blue; saturation moves skin and wall away from neutral together; a positive `tint` is green, a negative one magenta; levels gamma shifts chroma too, so re-measure after it.

## Colour of the ground

The graphics ground is `--color-video-ground` (#EFEDD8). Exports carry it as about (240, 236, 217), the same as the published references. A player's colour management can make it look whiter; compare against a reference video in the same player before changing anything.
