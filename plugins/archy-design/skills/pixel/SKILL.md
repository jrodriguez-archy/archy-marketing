---
name: pixel
description: Makes Archy's pixel textures. Pixel Gradients are the nine dithered backgrounds (Navy, Deep Blue, Primary, Royal Blue, Sky, Ice, Pure White, White, Mist) as PNG, seamless MP4 or WebM loops, and live Webflow or React backgrounds. Pixel Effects bring the same grain into a photo (Pixel Dissolve, Pixels Behind, Pixel Tone). Use when someone needs a gradient or textured background for a slide, post, video or the website, wants one animated, wants a pixel effect on a portrait or a place photo, or wants to change or add a gradient.
---

# Archy pixel textures

Archy's textures are one idea: a pixel grain made from ordered 8×8 Bayer dithering, drawn only in brand tokens. It comes in two families, both documented on the **Textures** page of the Brand file:

| Artboard | Family | What it is |
|---|---|---|
| `00 · Textures` | | Overview, which one to use, fixed and flexible |
| `01 · Pixel Gradients`, `02 · Pixel Gradients · Usage` | Pixel Gradients | Backgrounds made from scratch |
| `03 · Pixel Effects` | Pixel Effects | The grain applied to a photo |

Every output comes from code, so never draw or generate the pixels by hand. Work in `${CLAUDE_PLUGIN_DATA}/pixel/` (call it `$WORK`).

```bash
TOOL="${CLAUDE_PLUGIN_ROOT}/tools/pixel/pixel.py"
```

Needs Python 3 with Pillow (`python3 -m pip install --user pillow`); video also needs `ffmpeg` (`brew install ffmpeg`). If either is missing, say exactly what to install.

## Fixed and flexible

The values in this skill are a **starting point**, not a rule. Tune them to the piece; every one is a flag, so any variation stays reproducible.

- **Fixed:** brand tokens only; the person is always a real photo (faces are never pixelated); one grain per piece (the gradient behind a photo and its effect share one cell size); whole cells only (the grid divides the frame and is anchored to the bleed edge); made with this tool.
- **Flexible:** cell size (`--cell`), tone steps (`--steps`), how many colours and which ones (`--colours`, any tokens that contrast with the ground), how many cells and how random (`--density`, `--curve`, `--seed`), and where an effect starts (`--start`). When the requester or the piece asks for something else, do it and say what changed.

## Which one

| The piece needs | Use |
|---|---|
| A ground for a slide, post, video or web section | a Pixel Gradient |
| A person bleeding off the bottom of the frame | Pixel Dissolve |
| A headshot in a small or square frame | Pixels Behind |
| A city, office or practice behind text | Pixel Tone (never on people) |

## Pixel Gradients

One definition per gradient in `tools/pixel/presets.json`: a base token and a front colour that moves part of the way toward a neighbouring token. PNG, video and web all read it, so they match.

| Name | Base | Front | Text on it |
|---|---|---|---|
| `navy` | blue-tint-800 | blue-tint-700 | white, body blue-tint-200 |
| `deep-blue` | blue-tint-700 | 50% toward sky-blue-400 | white |
| `primary` | primary-blue-600 | royal-blue-500 | white |
| `royal-blue` | royal-blue-500 | 50% toward sky-blue-400 | white |
| `sky` | sky-blue-400 | 60% toward blue-tint-300 | white |
| `ice` | blue-tint-100 | blue-tint-200 | blue-tint-800 |
| `pure-white` | white | neutral-lightest (base dominates) | blue-tint-800 |
| `white` | neutral-super-light | white | blue-tint-800 |
| `mist` | neutral-lightest | neutral-super-light | blue-tint-800 |

Default recipe: six soft blobs (the same six for all, so the set reads as one family), 8.8 px cells at 2×, 6 steps between base and front, scale 1.08. The tones stay close on purpose: the grain is the character, not a colour shift.

### Static background (slides, posts, Paper)

```bash
python3 "$TOOL" gradient list                                       # the nine, tokens and hex
python3 "$TOOL" gradient png royal-blue --out "$WORK"                # 3456×1944, 2× of 1728×972
python3 "$TOOL" gradient png all --size 2160x2700 --out "$WORK"      # any size; cells scale with the width
python3 "$TOOL" gradient png sky --cell 24 --steps 3 --out "$WORK"   # a bigger, bolder grain
```

In Paper, set the PNG as the artboard or frame background with a percent-encoded `file://` URL and `background-size: cover` in the same call (see the brand skill's `paper-quirks.md`, *Images*).

### Video loop

```bash
python3 "$TOOL" gradient video royal-blue --out "$WORK"                    # 8 s, 30 fps, 1920×1080 mp4
python3 "$TOOL" gradient video all --format webm --seconds 12 --size 3840x2160 --out "$WORK"
python3 "$TOOL" gradient frames royal-blue --count 4 --out "$WORK"         # poster frames at 0, 1/4, 1/2, 3/4
```

Loops are seamless by construction (each blob travels a closed orbit that lasts one loop). The dither grid stays fixed on screen; only the tones move under it.

### Website

The site runs the official Paper Shaders `Dithering` shader live on the GPU: no video file, no loop needed. It is two-colour (base and front), so it reads slightly flatter than the PNG and video, and Pure White comes out close to White.

**Webflow** (where the Archy site is built): `python3 "$TOOL" gradient webflow` prints the custom-code script with all nine gradients.

1. In the section, add a Div Block as the first child, class `archy-gradient`: position absolute, all sides 0, z-index 0. The section is position relative; its content sits above at z-index 1.
2. Custom attribute on that Div: name `data-archy-gradient`, value one of the names above.
3. Paste the script in Page settings › Custom code › Before `</body>` tag, or once in Site settings › Custom code › Footer code for the whole site.
4. Custom code runs only on the published site. Give the Div the base colour as its background so the Designer shows the right ground. Reduced motion is honoured automatically.

**React** (`npm i @paper-design/shaders-react`): `python3 "$TOOL" gradient web royal-blue` prints a ready `<Dithering>` component.

### Changing or adding a gradient

Edit `presets.json` (a base token, a `toward` token, an `amount` between 0 and 1; `gamma` above 1 makes the base dominate), then regenerate the PNG, the loop and the Webflow script, and update `01` and `02` on the Textures page. Keep base and front neighbours: a big jump turns the grain into a visible pattern.

## Pixel Effects

The same grain applied to a photo. The person always stays a real, untouched photo; only the edge, the ground and place photos are treated. `--size` is the frame's size on the canvas; files are written at 2× (`--scale`). The ground and the cells share one grid (8px by default) that divides the frame and is anchored to the bleed edge.

### Pixel Dissolve, a portrait bleeding off the bottom

```bash
python3 "$TOOL" effect dissolve --gradient royal-blue --size 470x1080 --start 864 \
  --photo cutout.png --photo-rect -124,120,718,960 --out "$WORK/ae"
```

- Writes `dissolve-ground.png` (the gradient on the effect's grid), `dissolve-overlay.png` (transparent PNG with the cells) and `dissolve-preview.png`.
- In Paper: the ground is the frame's background (`background-size: 100% 100%`), the untouched cut-out sits on it and still bleeds to the trim, and the overlay is a full-frame layer named `Pixel Dissolve` above the photo. Swapping the portrait never touches the effect.
- `--start` is the y where the cells begin, below the face, the chest and any logo on the clothes (default 80% of the edge). `--edge` is the y of the trim when the frame runs past the artboard (an arch that bleeds off the bottom).
- Cells are scattered across the whole frame, sparse at first and up to `--density` (0.55) in the last row; `--curve` sets how fast they build up and `--seed` gives a different scatter.
- Colours default to light cells on blue grounds (Tint 300, White, Sky, Tint 200) and dark cells on light grounds (Navy, Royal Blue, Sky, Tint 300). Pass `--colours` with any number of token names. When a white plate sits on light cells, keep the plate white and give it a 2px `--color-blue-tint-300` border rather than recolouring.

### Pixels Behind, a headshot in a tight crop

```bash
python3 "$TOOL" effect behind --gradient sky --size 378x378 --photo cutout.png --photo-rect -116,-17,605,808 --out "$WORK/ae"
```

Writes `behind-ground.png`: the gradient with a band of cells (Navy, Royal Blue, Tint 200 by default) rising from `--start` (a third of the way down) to the trim. Use it as the frame's background and put the untouched cut-out on top.

### Pixel Tone, a place photo as a quiet background

```bash
python3 "$TOOL" effect tone city.jpg --gradient royal-blue --size 1080x1080 --out "$WORK"
python3 "$TOOL" effect tone city.jpg --gradient ice --invert --size 1080x1080 --out "$WORK"
```

The photo is dithered into the gradient's own two tones on a 1px cell, so the difference stays very subtle; raise `--cell` or `--steps` for a bolder read. On light grounds pass `--invert` so dark subjects take the darker tone. Never on a person.

## Paper notes

- **If an uploaded PNG renders as a broken image** although the upload worked, set the node's `backgroundImage` again with the `https://app.paper.design/file-assets/…` URL that `get_computed_styles` reports.
- Local files must be percent-encoded `file://` URLs; a file under the plugin's data folder uploads more reliably than one in a temporary folder.
