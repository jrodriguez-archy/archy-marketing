---
name: chrome-store
description: Create or update Chrome Web Store listing images for Archy browser extensions in Paper (the 1280×800 feature explainer and the 440×280 promo tile), built from native product UI. Use when someone needs store images for the Portal Manager extension or any other Archy extension, or wants the existing listing images changed.
---

# Chrome Web Store assets

Load the `brand` skill first and follow it. These pieces mix two systems: the marketing frame is Archy marketing (Onest + Inter, tokens, the wordmark, the mascot); the product inside it is Archy product UI and stays **Open Sans**.

## Source

Paper file `Archy - Various Collateral` (`app.paper.design/file/01M37ZJ6ECM7XJ5TG5W2Z2YR4N`), page `Chrome - Portal Manager`:

| Artboard | Size | What it is |
|---|---|---|
| `Chrome Store · Feature Explainer 1280×800` | 1280 × 800 | The main listing image: headline, browser window, extension popup |
| `Chrome Store · Sneak Peek Promo 440×280` | 440 × 280 | The small promo tile: wordmark as the hero, the mascot peeking in |
| `Portal Manager - Archy - Chrome`, `Portal Manager - Popup Compact (no 2FA)` | 380 wide | The extension popup, source frames |
| `Top level navigation - Grid view` | 1920 × 1080 | The app, source frame |
| `Inspiration` | | Reference listings from other products |

Construction, sizes and every lesson are in `references/portal-manager.md`. Read it before touching the canvas.

## Steps

1. **Confirm the extension and what changed**: a new extension, a new feature to explain, or a refresh of the existing images. Get the extension's name, its one-line purpose and the screens to show; product screens come from the real product frames, never invented.
2. **Work in a copy.** For Portal Manager, duplicate the two listing artboards next to the originals, or into the requester's file. For a new extension, start from duplicates of the same two artboards and swap the product frames.
3. **Build the product natively at 1:1**: copies of the real navigation, header and content frames, re-laid out to fill the browser window. Never place exported screenshots of the product. Cut repeated information before shrinking anything.
4. **Headline and wordmark**: a two-tone headline (Onest 600) on the explainer; the wordmark as the hero on the 440. Both run bigger than feels safe.
5. **Review** both artboards with `../brand/references/review-checklist.md`, and check that every product text node is Open Sans.
6. **Export when asked**: PNG, full bleed, no transparency, no rounded outer corners (the store's rule), at the exact pixel size. Paper saves to `~/Downloads`.
7. **Deliver**: what changed, which frames the product came from, anything pending (copy, screens).

## References

| File | Read it when |
|---|---|
| `references/portal-manager.md` | Always: geometry, browser chrome, popup, sizes and lessons |
| `../brand/references/composition.md` | The mascot bleed, the wordmark, scale |
| `../brand/references/review-checklist.md` | Reviewing |
| `../brand/references/paper-quirks.md` | Paper tool behaviour |
