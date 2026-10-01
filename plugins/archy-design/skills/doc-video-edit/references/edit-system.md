# DOC course video edit system

The edit language of the DOC Foundations course videos, taken from the published references (F1.2 Financial Readiness, Building a Pre-Open Patient List) and the first video edited in Tesseract with this skill. Defaults, not locks: when the material asks for something else, do it and say why in the edit plan.

## Structure

| Part | Default |
|---|---|
| Intro | The supplied intro clip (DOC logo on cream, then the red title card with the speaker photo), about 10 s, video only. Its audio is replaced by the supplied intro music. |
| Handoff | Hard cut from the intro's red card to the speaker, who is already speaking: start the take ~0.1 s before his first word (a still face looking at the camera before he starts reads as dead air). On `_Post_` footage that is a trim of the open: propose it and do it only with the user's OK (see Cuts). The speaker lower third starts ~0.5 s into the first shot. |
| Body | The speaker, two cameras, graphics on the moments the brief marks. |
| Section breaks | The red multi-bar wipe (`03_Transitions`) at the 2 or 3 real changes of topic. Nowhere else. The speaker is speaking again as the wipe opens: when the take holds a long pause there (over ~0.6 s), shorten it to ~0.4 s with the dialogue join at the frame where the wipe fully covers the picture, which hides it. On `_Post_` footage only with the user's OK. |
| Closing | The closing card enters on the last line (mid-sentence is fine), about 10 s on screen in total, never much more: holds ~1.5 s after the last word, its text fades (0.6 s), the card crossfades (0.4 s) into the end card. |
| Closing without a T10 | Stay on the camera that says the last line and go out on it; never cut to the other camera for a silent tail (reads as a stray shot). Go out ~0.45 s after the last word, then the 0.5 s crossfade into the end card; a longer silent tail reads as the video stalling. On `_Post_` footage the take runs to its end (see Cuts); when its tail after the last word is longer than ~1 s, propose trimming it to that hold and do it only with the user's OK. When the speaker stays still and in frame through the hold, ending the take there is enough: the last segment ends at last word + hold + crossfade (`timing.voice_end_src` at the end of the last word's decay, `timing.ff_tail` = the hold). Only when he moves or speaks again inside that hold, freeze that camera on its closed-mouth frame right after the word (shot with a 5th value = freeze frame, source s), play the take's clean room tone under it (a tail segment from any silence), and the end card fades in over the frozen frame (`doclib` does this when the last shot is frozen). Set `closing.mode: "camera"` and `timing.cam_tail` (hold after the last word, ~0.4 s): the last shot then ends at the crossfade on its own. |
| End card | The supplied end card (DOC logo animating on cream) with its own sting. |

Runtime comes from the content: tighten, never pad. A brief's estimated runtime is a guide; report the real one.

## Cameras

- **CAM A** (frontal, centred) is the base. **CAM B** (side angle, tighter) comes in on real changes of idea and asides. Never cut on a timer.
- **Rhythm:** change cameras only where a thought ends (a sentence end with a real pause), never mid-sentence and never on a timer. Hold each shot about 8 to 20 s; nothing under ~5 s. Do not squeeze a short shot in just before a split or card: stay on the current camera into the graphic.
- **Where to cut: decide each cut by watching it, not by a formula.** Every pause is different, so there is no fixed offset in frames. For each camera change, find where the idea ends, then watch the frames around that pause on both cameras and pick the moment where the cut feels invisible:
  - The outgoing shot ends on a finished thought: the last word, a breath, a small nod or a look that closes it. A short silence there reads as the idea landing.
  - The incoming shot starts with life: he starts the next sentence, breathes in to speak, or moves. It must not open on a silent, frozen face waiting for something to happen; that reads as dead frames.
  - In most pauses that puts the cut late, close to the start of the next sentence, with the pause on the outgoing shot. When the outgoing face goes blank during a long pause (freezes, looks away, mouth hanging), cut on the moment his expression or posture changes instead. When the whole pause looks dead on both angles, put the change where the least of it shows; on footage that may be trimmed (not `_Post_`), shorten that pause under the change (a dialogue join hidden by the cut; where the framing would not change, vary it, 106 % -> 100 %).
  - Fine-tune by a frame or two so the cut does not land on a blink, in the middle of a head turn, or on the frame a mouth snaps open for a plosive ("But").
  - The same judgement applies to a split or card that enters or leaves in a pause (when it is not anchored to a word inside the sentence): its in/out moves with the shot.
  - **How the frame is chosen (dynamic, per cut):** `scripts/cut_pick.py` (run for every camera change by `cut_check.py --pick`, written with `--snap`) looks at both cameras through the pause. It measures each camera's face movement against that camera's own movement while he talks, so it adapts to every shot and speaker: a face at rest reads as still, a breath, a nod or speech starting reads as life, an isolated one-frame jump reads as a blink. It then takes the frame that leaves the fewest still, silent frames on the incoming shot, then the fewest frozen frames on the outgoing shot after the idea has landed, and that is not on a blink; ties go late (the pause stays on the outgoing shot). So each pause gets its own answer: late when nothing happens before the next sentence, earlier when the incoming shot has a breath or a movement to open on, or when the outgoing face goes blank.
  - The script proposes, you confirm: watch every cut it moved (psheet at 24 fps steps) and overrule it when the picture says otherwise.
- The waveform confirms the pause, the transcript only labels it: whisper word times drift by up to ~1 s, and a breath inside a phrase ("a really good | job, but") can look like a sentence gap. When the moment you chose has no real pause (dialogue under about -40 dBFS for ~350 ms or more), move the change to the next sentence end. To read the words either side of a cut, transcribe a few seconds before and after it as two separate whisper runs.
- When a camera shot between two graphics would be shorter than ~8 s, remove it rather than squeeze it in: hold the first graphic a little longer, or bring the next one forward to that pause (a split can hand straight to the next split or follow a card directly), so the speaker never flashes on screen for a few seconds between graphics.
- Keep camera changes ~3 s or more away from a split, card or wipe entering or leaving, so cuts never stack (F9.3 v3: 5 cuts in 27 s around a card read as random). `build_video.py` prints `pacing:` warnings for a speaker shot under 8 s (except the first), a same-camera full <-> punch cut not hidden by a wipe, and a split/card shot whose graphic does not cover exactly the same range (that gap renders the bare shifted camera with a black half). Fix every warning before exporting.
- **Picture sync (F9.3 v5):** identical audio does not mean the pictures line up. Run `scripts/cam_sync.py <Video>` once per video (and after a proxy -> final swap); if it reports a lag, set `"cam_offset": {"B": s}` in video.json (F9.3: CAM B 0.85 frame early -> -0.0417, one frame; doclib snaps each B start to a source frame, a between-frames start rendered a black frame). A sub-frame offset shows as a small jump on every A/B cut.
- Every internal cut (a removed stumble, a removed phrase, a shortened pause) lands on a camera change or inside a split, so there is never a visible jump.
- Punch-in: CAM A at 115 % around its eyeline for the lower-third moments, entered from CAM B on a sentence end (a mid-sentence A -> A zoom reads as a random cut). A lower third may also sit on CAM B: its tighter frame keeps the lower left clear.
- **Framing (house rule, F9.2 feedback):** compose every camera before cutting. Look at a few frames of each camera across the take and set `reframe` per camera in video.json (`{"A": {"scale": 1.12, "center": [cx, cy], "punch": 1.10}, "B": {...}}`, centre in 1920x1080 frame pixels). Crop out set edges, stands, lights or reflectors, odd shadows and dead headroom; eyes near the upper third, a little air above the hair, the speaker's look-room kept (CAM B looks left). Do it moderately: scale about 1.08-1.20, never a big face. Every framing builds on it (punch = a further `punch` zoom about the eyeline, splits reuse the same frame in the left half) and `doclib` refuses a window past the picture edge. Ignore a burned-in icon on proxy files (it goes with the finals); set the reframe on the proxies so the finals arrive already framed. To crop a set edge completely, measure where it ends in the source frame (column brightness) and use the least zoom that clears it: with the window against the far edge, s >= 1920 / (1920 - edge_x) (F9.1 CAM B: band to x ~340 -> 1.23, a little over the usual range, accepted because B is the tighter shot). Check the rendered full, punch and split frames.
- Splits use CAM A shifted -480 px so the speaker is centred in the left half; CAM B looks off to the left and would face away from the panel. Not dimmed.
- A cut inside a split: keep CAM A, change the scale to 106 % (framing `split2`).
- A split may enter mid-sentence on its anchor word; camera changes stay on sentence ends.

### Checklist for every cut

Every camera change passes five checks; when one fails, move the cut.

1. **It ends a thought.** Decide where an idea ends first, then look for the pause. A breath inside a phrase ("a really good | job") looks like a sentence gap on the waveform.
2. **It sits in a real pause.** Transcribe ~2.5 s before and ~2.4 s after the cut as two separate whisper runs. Do not trust `words.json` times for this: they drift 0.3 to 1 s.
3. **It feels invisible.** Start from the frame `cut_check.py --pick` chooses, then watch the frames either side of the cut on both cameras (`psheet.py` at 24 fps steps): the outgoing shot ends on the finished thought, the incoming one starts with life, neither opens or holds on a frozen, silent face, and the cut does not land on a blink, a head turn or a mouth snapping open. When it does not feel right, move it within the pause, or to another sentence end.
4. **The cameras are in sync.** Identical audio does not mean identical picture. Run `scripts/cam_sync.py` once per video and after every proxy -> final swap, and set `cam_offset` when it reports a lag.
5. **It holds in the export.** Check the exported file frame by frame at every cut, plus the black-frame scan (full frame and each half). Previews and the config do not show every render fault.

Fewer, motivated cuts carry less risk: a camera change follows an idea, never a timer. When one bad cut turns up, audit all the others with the same method before fixing it.

## Graphics timing

- Anchor each graphic to the words in the brief, found in the transcript (brief timecodes are rough).
- Lower thirds: 4 to 7 s. The speaker lower third runs through the first shot (~6.8 s) so the role tag is readable.
- A lower third never covers the face. After any reframe, look at every lower third on the shot it sits on: a zoomed CAM B puts the chin low, where a two-line caption lands on it (F9.5 LT 13). Move that lower third onto CAM A (punch) in the camera plan rather than moving the box.
- Splits and full cards enter and exit on hard cuts. List items appear on the word that says them.
- Reading time: hold a list at least ~3 s after its last item appears. When the speaker says the last item late, bring the item forward to the phrase that introduces it and/or extend the split into the next phrase.
- Number cards: long enough to read everything on them: ~4 s for a figure and one label, ~6 s or more with an eyebrow and two label lines (hold ~3 s after the last line lands). Enter on the phrase that sets the figure up, not on the figure itself, when that buys the time.
- Count-ups: every number on a card counts up, on both sides of a range or a sum ("1,200 - 1,500", "20% + 5%"), with `"count": {"all": true}`. Only text between the numbers stays still. The single leading counter is legacy.
- The red wipe is always the frontmost layer (above any graphic); put the camera or graphic change at the frame where it fully covers the picture (0.95 s into the clip).

## Cuts from the brief

- **Check first whether the footage is already cut.** Camera files named `*_Post_*` (or delivered by the editor as the edit's cut) already carry the brief's cut list. Do not cut inside them again: an extra cut on continuous footage breaks the rhythm and shows as a jump. Use the file whole, from its first frame to the end of the take: no internal cuts, no trim of the open or the close (not even a sales pitch the brief removes), unless the user explicitly asks for that specific cut. If the file still contains something the brief removes, raise it as a question; do not cut it.
- Find every quoted cut in the word-level transcript, then confirm the exact boundary on the waveform (`scripts/wave.py`): cut inside a quiet gap, ~50 to 120 ms clear of the words.
- Stumbles ("with a, with a") are often cleaned out of a normal transcript: run the prompted pass of `scripts/transcribe.sh` on that range to see them.
- After the export, re-transcribe it and read each join; state that the joins still need a human listen.
- If a camera file ends inside the last word, the file must be re-exported with a tail; do not trim into the word.

## Sound

- **No audio ever ends abruptly.** Every sound that ends inside the edit ends on a fade: the intro music (one continuous descent that finishes before the music file does), the last dialogue segment (fades over its room-tone tail after the last word, up to 0.8 s, so the room tone never cuts to digital silence under the closing card; end the last segment 0.3-0.8 s after the last word), and anything added later. `doclib` applies both fades on every build (`timing.music_duck_lead` / `music_duck_db` / `music_floor_db`, `timing.dialogue_fade`). Internal dialogue joins are the only exception.
- Speaker only under the body: no music bed.
- Intro music at full level over the intro, then one slow, progressive exit: it starts easing down 1 s before the first word, sits at -10 dB as he starts, and keeps falling steadily until it cannot be heard, just before the file ends. No plateau, no step, never a cut.
- The wipe keeps its short whoosh; the end card keeps its sting.
- Levels: see `audio-grade.md`.

## Deliverable

1920x1080, 24 fps H.264 MP4, `exports/<video>_vN.mp4`, plus the editable `.tsrct`, a filmstrip in `Previews/` and the notes in `.tesseract-work/NOTES.md`.
