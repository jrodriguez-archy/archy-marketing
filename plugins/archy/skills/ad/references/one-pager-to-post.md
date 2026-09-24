# Adapting the one-pager to a 1080 × 1080 Post

Read this when deriving a square social Post from a taller ad (such as the Platform one-pager), or when editing `Platform · Post 1080×1080`.

## Where the ads live

Paper file **`Archy - Ads`** (`app.paper.design/file/01M33E66BD6FJNP4BPE88V90X0`):

- **Page 1**: `Claim Stack` Post / Stories / OG.
- **Page 2**: `Platform · One-pager 1500×1942` (Letter proportion), rebuilt from a raster reference that sits beside it, and `Platform · Post 1080×1080` derived from it.

## The derivation

`Platform · Post 1080×1080` was derived by duplicating `Platform · One-pager 1500×1942`, then corrected by hand in review. The review changed almost every proportion, and the changes are the lessons. Measured off the reviewed artboard:

| | As built | As reviewed |
|---|---|---|
| Mascota | 437 × 292 @ 55, −92, visible to y200 | **589 × 394 @ 53, −131**, visible to y263, **55% of the width** |
| Masthead band | 138 | **224**: the headline drops 86px to sit clear of her |
| Claim | Onest 60/66, two lines | **Onest 40, one line** |
| Body | Inter 32/44, two forced lines, `all-in-one platform` SemiBold as its own node | **Inter 34/44, one node, `text-wrap: pretty`, three lines, no inline bold** |
| Footer alignment | top: button edge on the cap line of "Meet" | **bottom: URL and tagline share one baseline**, `align-items: end` |
| Button | fixed height 84, its own width | **stretched to the URL's width**, height from `padding-block: 10` |
| URL | 32/40 | **45/40**: bigger than the body, set solid |
| AI lockup | 48/52, "Meet" SemiBold | **40/52, "Meet" Medium**, "Archy Intelligence™" SemiBold |
| Tagline | two lines, 26/36 | **one line**: `Experience the AI Advantage.` cut |

## Lessons

**The mascota is the image, so size her first and fit the content around her.** Scaling her *down* from the one-pager to make room for text is backwards: on a square post she is the only picture, and at 44% of the width she reads as a corner accent. At 55% she carries the top of the piece. Budget her band before the type, not after.

**One hero per format.** Setting the claim at 60px over two lines (because 40px seemed weak after an 82px headline) made it a second headline competing with the first. A square has room for one display element. The claim is a *lead*: one line, and its emphasis comes from the weight contrast inside it (Regular / SemiBold on the two figures), not from size. **"Type runs bigger than feels safe" is about the hero, not about every level.** The footer went the same way: lockup 48 → 40 and the tagline down to one line. When a format shrinks, cut levels and quiet the supporting ones; do not enlarge everything.

**Type size beats the source's line break.** Holding the body at 32 to preserve the one-pager's break and its inline bold (at 33 its second line wrapped) was wrong. Let it wrap to three lines at 34 in a single node and drop the bold. At feed size the reader needs the bigger type more than the emphasis, and one node is also what the team can edit. **If holding a line break costs type size, let the text wrap** and clean the rag with `text-wrap: pretty`.

**Anchor a two-column footer to the floor.** Two columns of unequal height at the bottom of a piece align at the bottom, on a shared baseline (URL and tagline both land at ~y987), because the bottom edge is the one that meets the margin and the eye checks it first. Top-aligning them (button on the cap line of "Meet") is locally correct and leaves a 34px rag against the margin, which is where it shows most.

**The button and the URL are one block.** The button stretches to the URL's width, so the pair shares a left *and* a right edge and reads as one CTA instead of two stacked objects. The URL is the destination, not metadata: it sits above the body at 45px, set solid (45/40) per the single-line rule in *Scale and restraint*.

**The rhythm between text blocks is ~54, measured ink to ink**: rule → claim cap line, claim baseline → body cap line, and the body's last baseline → the divider all land at 54–55. That is the scale's 56 read optically, not a box gap.
