---
name: gradients
description: Generates the Archy pixel-dithered gradients (Navy, Deep Blue, Primary, Royal Blue, Sky, Ice, Pure White, White, Mist) as static PNG backgrounds, seamless video loops (MP4 or WebM) and live animated backgrounds for Webflow or React. Use when someone needs a gradient background for a slide, a post, a video or the website, wants one animated, or wants to change or add a gradient.
---

# Archy pixel gradients

The set lives on the **Gradients** page of the Brand file: one artboard shows the nine, the `Usage` artboard beside it explains how they are made and used. Every output comes from code, so never redraw a gradient by hand. Work in `${CLAUDE_PLUGIN_DATA}/gradients/` (call it `$WORK`).

```bash
TOOL="${CLAUDE_PLUGIN_ROOT}/tools/gradients/gradients.py"
```

Needs Python 3 with Pillow (`python3 -m pip install --user pillow`); video also needs `ffmpeg` (`brew install ffmpeg`). If either is missing, say exactly what to install.

## The set

One definition per gradient in `tools/gradients/presets.json`: a base token and a front colour that moves part of the way toward a neighbouring token. PNG, video and web all read it, so they match.

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

Shared recipe: six soft blobs (the same six for all, so the set reads as one family), ordered 8×8 Bayer dithering, 8.8 px cells at 2×, 6 steps between base and front, scale 1.08. The tones stay close on purpose: the pixel grain is the character, not a colour shift.

## Static background (slides, posts, Paper)

```bash
python3 "$TOOL" png royal-blue --out "$WORK"            # 3456×1944, 2× of 1728×972
python3 "$TOOL" png all --size 2160x2700 --out "$WORK"  # any size; cells scale with the width
```

In Paper, set the PNG as the artboard or frame background with a percent-encoded `file://` URL and `background-size: cover` in the same call (see the brand skill's `paper-quirks.md`, *Images*).

## Video loop

```bash
python3 "$TOOL" video royal-blue --out "$WORK"                       # 8 s, 30 fps, 1920×1080 mp4
python3 "$TOOL" video all --format webm --seconds 12 --size 3840x2160 --out "$WORK"
python3 "$TOOL" frames royal-blue --count 4 --out "$WORK"            # poster frames at 0, 1/4, 1/2, 3/4
```

Loops are seamless by construction (each blob travels a closed orbit that lasts one loop), so they can repeat forever in a player or an editor. The dither grid stays fixed on screen; only the tones move under it.

## Website

The site runs the official Paper Shaders `Dithering` shader live on the GPU: no video file, no loop needed. It is two-colour (base and front), so it reads slightly flatter than the PNG and video, and Pure White comes out close to White.

**Webflow** (where the Archy site is built):

```bash
python3 "$TOOL" webflow          # prints the custom-code script with all nine gradients
```

1. In the section, add a Div Block as the first child, class `archy-gradient`: position absolute, all sides 0, z-index 0. The section is position relative; its content sits above at z-index 1.
2. Custom attribute on that Div: name `data-archy-gradient`, value one of the names above.
3. Paste the script in Page settings › Custom code › Before `</body>` tag, or once in Site settings › Custom code › Footer code for the whole site.
4. Custom code runs only on the published site. Give the Div the base colour as its background so the Designer shows the right ground. Reduced motion is honoured automatically (the gradient stays, the movement stops).

**React** (`npm i @paper-design/shaders-react`): `python3 "$TOOL" web royal-blue` prints a ready `<Dithering>` component with the resolved colours.

## Changing or adding a gradient

Edit `presets.json` (a base token, a `toward` token, an `amount` between 0 and 1; `gamma` above 1 makes the base dominate), then regenerate the PNG, the loop and the Webflow script, and update the two artboards on the Gradients page. Keep base and front neighbours: a big jump turns the grain into a visible pattern.
