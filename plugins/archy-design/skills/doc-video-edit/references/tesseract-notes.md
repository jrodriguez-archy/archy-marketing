# Tesseract notes for DOC video work

Behaviour of the Tesseract CLI learned on real DOC edits. The installed schema (`tsrct project schema --document`) and the render are authoritative.

## Document

- `tsrct project create` makes a 1080x1920, 3 s document; `build_video.py` sets 1920x1080 and the duration.
- Asset IDs cannot be replaced: import new versions of a file (proxy -> final) as new IDs (`camA2`, `camA3`) and point the config at them.
- Animation is stored in `composition.dynamics`. A checkout -> edit -> commit keeps old keyframes on reused layer IDs, so `doclib` clears `dynamics` on every build and re-applies all keyframe actions. Never skip that step.
- Layer order: index 0 is frontmost. Group children are listed front to back in the document (`doclib.G` keeps them back to front while building).

## Layers

- `rect.position` is the rect's top-left inside the layer; place and anchor with the transform.
- Point text origin is the baseline start. `doclib.Metrics.baseline` converts a CSS line box top to the baseline with the Satoshi file's own metrics, so text lands where Paper puts it.
- Right-justified point text anchors at the baseline end (used by the count-up).
- Track mattes (`trackMatte: {mode: alpha, layer: id}`) work across siblings, and the matte layer itself is not rendered. Use them to clip text to a box that is wiping in.
- `import-font` returns the family/style to use: Satoshi Regular = `Satoshi`/`Regular`, Bold = `Satoshi`/`Bold`, Medium = `Satoshi Medium`/`Regular`, Black = `Satoshi Black`/`Regular`.
- Images: PNG, JPG and WebP only (no SVG). Draw simple shapes as native layers.

## Animation

- Keyframe easing belongs to the destination key. `hold` makes a hard switch; use it to turn a covered layer off.
- Audio envelopes: `setFxPropertyAnimator` on property `volume` with a `jsScript` that returns the full linear gain.
- `textContent` can be driven by a `jsScript` (count-ups).

## Effects

- `levels` is 0-255. `lumaKey` threshold 0.08 / softness 0.05 removes studio-range black from the red wipe clip.

## Rendering and review

- Black frame on a camera cut (export only; `tsrct preview` of the same time is fine): it happens when the first rendered frame of a clip that needs a seek in its file (a change of camera) falls ~1-2 frames after a keyframe of that file (seen at +13 and +43 ms of source; +58 ms and later rendered fine). Keep every camera-change clip start out of the first ~0.12 s after a keyframe (`ffprobe -select_streams v -skip_frame nokey -show_entries frame=pts_time`), moving the cut to just before the keyframe while it stays in the pause. Overlapping the outgoing shot under the new one does not help: the whole frame renders black.

- `tsrct preview --time` renders one frame; `scripts/psheet.py` tiles many (use 24 fps steps for motion).
- Export: `tsrct export --fps 24` (the footage is 23.976; 24 is the closest offered). About 2.5 min for a 3 min video.
- On hosts whose ffmpeg lacks `drawtext`, the Tesseract waveform helper fails; use `scripts/wave.py`.
