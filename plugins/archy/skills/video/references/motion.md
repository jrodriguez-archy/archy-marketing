# Archy video motion

Read this before animating any Archy video graphic. The `Guidelines` page of `Master - Videos` shows the same rules on boards 04 (Pixel Transitions), 05 (Text Motion), 11 (Motion) and 12 (Highlights and Subtitles). After Effects is the reference tool; the numbers below are at 24 fps.

## Rhythm: stop-motion in steps

- Every animated graphic (text, boxes, pixels, moons, cards) moves in held poses, **10 a second**: each pose holds 2 to 3 frames. In After Effects, keep normal eased keyframes and add `posterizeTime()` on every animated property, driven by one shared slider ("Steps per second") so the whole video can be retimed in one place.
- Footage and the pixel-gradient grounds stay smooth.
- Eases are spread over the move: outgoing speed about 1.4 times the average with 25% influence, incoming 55% influence. With steps, front-loaded eases read as a jump.

## Text arrival

- Words arrive one by one, 84 ms apart: each rises 40px in 280 ms, out of a 12px blur that clears in 300 ms, while its opacity goes from 0 to 100 in 180 ms.
- About 0.35 s after it lands, a word flashes `sky-blue-400` and settles to its colour in 170 ms. On Ice the colour it settles to is navy.
- Text inside a box (lower thirds, highlight bars) skips the flash.
- The wordmark rises 48px with the same timing.
- Moons unfold from the spiral's off-frame corner: each slides out from 80% of the way to the centre and grows from 55% to 100%, nearest the corner first, then breathes 3% with an offset per moon.

## Text life

Big titles do not sit dead still, but nothing runs constantly:

- At most **two words per title** carry an effect, never neighbours: one breaks into pixels (a mosaic of 16px blocks at 128px type, smaller on smaller type) for 2 steps with a 2px sideways shift; the other trembles 1.5px for 3 steps. The rest of the title only steps.
- Each chosen word gets exactly one event per about 2.5 s of its settled hold, at a random moment between settling and the exit or cut. A title of two words gets one effect; a URL or a single line of a few words gets none.
- No text life on product UI, small labels, highlights or subtitles.

## Text in boxes

- Lower thirds and highlight bars mask their text: the box (a hidden copy of it as an alpha track matte) clips the words, so they rise in from inside it and drop out inside it, never showing outside the box.
- Boxes grow from their left edge; their pixel accents pop in on the steps after the box opens.

## Holds and exits

- **No scene zooms or pushes into its transition**, and opener moons never fold back: every scene holds still until the wipe covers it.
- Openers, titles and end cards have no exit; the wipe takes them.
- Lower-third and highlight boxes retract while their words drop 40px inside them. Product headlines blur out word by word and the UI card breaks into growing pixels before the wipe.
- Each scene holds at least 2.5 s once its last word has settled.

## Transitions: pixel wipes

- Every scene change is a **pixel wipe** on the 40px cell, **1.2 s in 12 steps**. The next scene shows through the cells (a matte), led by a `sky-blue-400` edge and a dithered `blue-tint-300` fringe; once covered, a few stray pixels blink off over the new scene for three steps.
- The next scene's first words land about 0.15 s before the wipe ends, so there is never an empty frame between scenes.
- Three wipe shapes: **Corner** (a dithered diagonal from the bottom left or bottom right, to open a section), **Pixel disk** (a disk of cells from the centre with a sky ring, into the speaker; the footage inside settles from 109% to 100%), **Rows** (staggered rows rising from the bottom, to close a section or bring in the end card). No cross-dissolves, slides or zooms.
- In After Effects, keep each wipe as two image sequences (matte and edge) at 10 fps plus a solid that holds the cover; hundreds of single frames make the project heavy and unstable.

## Highlights and subtitles

- **Highlights:** the bar opens to its line's width in 0.23 s, then all the words of the point rise in together, fast, masked by the bar. The point holds about 2.5 to 3 s, then the words drop out together. Points less than 0.6 s apart keep the bars, which step to the next width; a longer pause closes them. They start after the lower third has gone.
- **Subtitles:** the whole line appears when the speaker starts it and leaves when the phrase ends, with a one-step fade; no rise, blur, flash or text life. A line never starts before the previous one could be read.

## After Effects notes

- Build the scenes as separate comps, strung in one reel comp that holds the control sliders (Steps per second, moon breathe, text life sizes).
- Reference effect controls by index (`effect("Steps per second")(1)`), not by the control's name: the name changes with the After Effects language.
- Render each reel over its full length, not the work area.
- Export only when the requester asks, as H.264 for review or a mezzanine format for the edit.
