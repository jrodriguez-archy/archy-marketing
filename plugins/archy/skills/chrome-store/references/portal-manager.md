# Chrome Web Store assets: Portal Manager

Read this when building or editing Chrome Web Store listing images for the Portal Manager extension, or any browser-extension store asset that shows Archy product UI.

**File:** `Archy - Various Collateral` (`app.paper.design/file/01M37ZJ6ECM7XJ5TG5W2Z2YR4N`), page `Chrome - Portal Manager`. It holds the two required listing images for an **unlisted** extension (Portal Manager: Archy logs the practice into payer sites and supply houses), plus the product frames they are built from. Reference: Workona's listing; the `Inspiration` frame holds it and ten more.

| Artboard | Size | Construction |
|---|---|---|
| `Chrome Store · Feature Explainer 1280×800` | 1280 × 800 | Blue ground · wordmark **158 × 61 @ top 52** · two-tone headline Onest 600 56/60, **gap 6** between the two nodes · browser window 1040 wide @ 120, 298, bleeding off the bottom · extension popup 380 wide hanging from the toolbar icon, right edge 16px inside the window |
| `Chrome Store · Sneak Peek Promo 440×280` | 440 × 280 | Blue ground · wordmark **246 × 95** (56% of the width) as the hero · mascota 304 × 203 rotated 180°, bleeding off the bottom, ~55% visible |

Source frames: `Portal Manager - Archy - Chrome` (the popup), `Top level navigation - Grid view` (the app), `Portal Manager - Popup Compact (no 2FA)`.

Export: PNG, full bleed, no transparency, no rounded outer corners (Google's rule).

## Lessons

- **Build the mockup natively, never as an exported PNG.** Exporting the app and the popup and placing them as images (because Paper cannot scale a 1920 screen down to 0.54×) is rejected. The fix is not to scale the app but to **re-lay it out at 1:1** inside the browser: copies of the real Side Nav, Header and Container, grid cut to 3 columns and 6 cards. It stays editable, stays Open Sans, and it reads bigger.
- **Product UI stays Open Sans**, even inside a marketing piece. Never switch it to Inter or Onest.
- **The product does not have to be faithful, it has to fill the frame.** A 1:1 app shown at 0.54× reads as a white page with small islands of UI. Enlarge sidebar and grid so they occupy the window, in preference to accuracy.
- **Height budget decides what the popup keeps.** At 1:1 the full popup (637) cannot fit under a 40px toolbar at y≈300 with its button visible, so the card's email / status / avatars strip is dropped because the fields below repeat it. Cut repeated information before shrinking anything.
- **Browser chrome:** the address bar carries a **lock + grey skeleton bar**, not a URL; a real-looking address commits to one that may change. The extension icon is a **plain `#2057FE` circle with a white A**, no square tile inside a grey hover circle.
- **The wordmark runs bigger than feels safe too.** It went 108 → 144 → 158 on the 1280, and to 56% of the width on the 440. At thumbnail scale the logo is the message and the mascota is the accent.
- **A two-tone headline at 56/60 wants a few pixels between its two nodes** (6 here). At gap 0 the two lines read as crowded at this size.
- **The 440 sneak peek is the one sanctioned mascota crop through the ears**: a thumbnail-scale piece where she only peeks in from the bottom, rotated 180°, under a wordmark that is the real hero. It does not extend to posters, slides or any format where she is the image.
- **Round what a hand-drag leaves behind** (`top 52.276`, `height 61.4375`): set integer `left` / `top` / `width` / `height` and `translate: none`, then confirm with `get_node_info`.
