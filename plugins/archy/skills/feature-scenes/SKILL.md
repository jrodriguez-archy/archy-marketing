---
name: feature-scenes
description: Build product feature scenes in Paper: short "before / after" frames that show one moment of the Archy app (a confirmation, a claim sent, a payment, a chart finding, a report, an AI agent), styled like the Video - Hero 1 frames and ready to animate in Rive. Use when a brief asks for product UI visuals per feature, hero or video frames, or app screens for marketing.
---

# Feature scenes

For designers. Load `archy:brand` first: tokens only, English on the canvas, never touch a `Master - …` file, never invent facts. Paper behaviour lives in `brand/references/paper-quirks.md`.

A feature scene sells one capability in one glance. Viewers do not stay long, so show the idea, not the steps.

## The scene

- **One moment per feature.** Pick the single state change that proves the feature (unconfirmed to confirmed, no claim to claim sent, balance due to paid, tooth unmarked to finding charted, morning to end-of-day numbers, recording to note ready). Do not build a step-by-step sequence; when the brief has several steps, choose the one that carries the value.
- **Two frames per scene by default: `A Before` and `B After`, with the same layers.** Only the moment's layers differ, by text, colour or `display: none`, so the pair can be animated (Rive) by interpolating between them. Name them `NN · Feature · Moment · A Before / B After`.
- **A short sequence (3 or 4 frames) when the action itself is the feature.** When the value is a gesture in the UI (start a recording, it runs, the result is ready, the result opens), build one frame per state, still with the same layers in every frame, named `NN · Feature · Moment · 1 Start / 2 … / 3 … / 4 …`. Keep it to the states that change on screen; do not add steps the viewer would not notice.
- **Image only.** No progress bars, no titles, no copy outside the UI: the pixel-gradient ground (`Video - Hero 1` assets) plus the app.
- **Frame:** 718 × 840 by default, `overflow: clip`, ground = a brand blue token plus a pixel PNG at `background-size: cover`.

## How the app sits in the frame

Use one of these, in this order of preference:

1. **Full screen, cropped from its top-left corner.** The whole 2056 × 1160 screen at 1:1 at `left: 40; top: 40`, radius 16, clipped, bleeding off the right and bottom edges (logo and side nav visible). Never crop from the middle of a screen. The visible area is roughly the screen's first 678 × 800 px, so put the moment there: reorder sections or columns of the hybrid screen when needed, and say that the order is adjusted.
2. **A module extract.** A real module or block of the app (a table, a ledger, an odontogram, a report board) without the side nav, anchored at its own top-left corner at 40/40 and bleeding right. Never cut through the middle of a module. When the module ends before the frame's bottom, fit its height to the content and round all four corners; centre it vertically when it is alone in the frame, and keep it at the top when a floating window shares the frame. A module may be enlarged with CSS `zoom` (1.15 to 1.3) and may hide columns or sections that do not serve the moment (say which).
3. **Show the feature where it lives in the app first.** When the feature has a home in the UI (Archy Scribe sits in the patient sidebar, a claim in the Claims table), show its state change there and open its result as a popup from that spot; move the section up inside its panel when it falls outside the crop, and say so. A detached floating card styled like the video is the alternative when the real spot cannot carry the moment; when in doubt, build both and let the designer choose.
4. **A zoomed crop for a UI-led sequence.** When the action happens in a small part of the screen (a sidebar card), zoom the full screen (CSS `zoom` 1.2 to 1.3 on the screen inside the 40/40 container) so that part reads large. Keep its top at 0: the logo and breadcrumb need their normal air above them, never cut against the container's top edge. Shift a module that would otherwise show empty space (an odontogram's quadrant labels, say) with `translate` inside a clipped parent so the meaningful content enters the crop. Add the pointer from the `Video - Hero 1` frames on the control being used.
5. **A floating window** over 1, 2 or 4: a card (claim, X-ray, Scribe note) or the patient's phone. Keep windows at least 56 px from the frame's right and bottom edges and off the layers that change. The phone is the exception: it may bleed off the bottom on purpose. Offset a floating window from the module's edge rather than aligning it exactly. A window may be enlarged with `zoom` to make it the hero.
6. **A full drawer for a large result.** When the result is the hero (a generated note, a report), open it as a drawer that covers the app inside the same container, not as a floating modal: anchored to the container's top, bleeding right and bottom, leaving a strip of the app on the left (the side nav works well) under a scrim, so it reads as sitting on top. Give its content the same padding on both sides against the frame edge, and let long text run past the bottom of its box under a white fade so it reads as a real document that continues.

## Hybrid UI

Real structure and data, marketing finish:

- **Structure and labels come from the product**: the UI kit screens and, read-only, the live preprod app (navigate, open a tab, expand a row; never create, save, send or type into forms). Status pills, column names and empty states are copied as they are.
- **Visible components take the polished look** of the `Video - Hero 1` frames and `Master - Product` (softer cards, coloured status stacks, larger type in cards).
- **Keep one cast and one story across the scenes** (one patient, one practice, one tooth or claim threading through features), so the set reads as one day in one practice.
- **Simulated data is allowed and must be flagged**: numbers when preprod has none, message wording, times. List every simulated item in the delivery. A generated image (an X-ray, say) needs the user's OK and is reported as generated.

## Workflow

1. For each feature, look at the kit screen and preprod, then offer two or three candidate moments in one question; build only the chosen one.
2. Build or update the hybrid full screen on a `Full Screens` page (it is the source), then the frames on a `Frames` page: one row per feature, ordered by feature number, the first state at x 0 and the next ones beside it.
3. Screenshot every frame; check the moment reads in one second, windows keep their margins, only the moment's layers differ, tokens only.
   Check the spacing inside every card at `scale: 2`: a title needs at least 16 px from the content under it, and no two blocks may touch. A card rebuilt from the video at a different size keeps the video's proportions, not its pixel gaps.
4. Record the scene (layout, states, real vs simulated) in the project notes, and delete frames that are no longer used.
