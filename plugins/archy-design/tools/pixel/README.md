# pixel

Archy's pixel textures, documented on the Textures page of the Brand file: **Pixel Gradients** (static PNG, seamless video loops, web snippets) and **Pixel Effects** (the grain applied to a photo). Python 3 + Pillow; `video` also needs `ffmpeg`.

```bash
TOOL="${CLAUDE_PLUGIN_ROOT}/tools/pixel/pixel.py"

# Pixel Gradients
python3 "$TOOL" gradient list                          # the nine gradients, tokens and resolved hex
python3 "$TOOL" gradient png all --out ./pixel         # 3456x1944 statics (2x of 1728x972)
python3 "$TOOL" gradient png sky --cell 24 --steps 3   # any grain
python3 "$TOOL" gradient video royal-blue              # 8 s, 30 fps, 1920x1080 mp4
python3 "$TOOL" gradient frames royal-blue --count 4   # poster frames of the loop
python3 "$TOOL" gradient web royal-blue                # <Dithering> snippet for @paper-design/shaders-react
python3 "$TOOL" gradient webflow                       # the Webflow custom-code script

# Pixel Effects
python3 "$TOOL" effect dissolve --gradient royal-blue --size 470x1080 --start 864 --photo cutout.png --photo-rect -124,120,718,960
python3 "$TOOL" effect behind --gradient sky --size 378x378 --photo cutout.png --photo-rect -116,-17,605,808
python3 "$TOOL" effect tone city.jpg --gradient ice --invert --size 1080x1080
```

- `presets.json` is the single definition of the gradients: each one is a base token plus a front colour that moves `amount` of the way toward a second token. The six blobs are shared, so the family stays consistent.
- Every value (cell size, steps, colours, density, where an effect starts) is a starting point exposed as a flag.
- In the effects, the ground and the cells share one grid that divides the frame and is anchored to the bleed edge.
- Loops are seamless by construction: each blob centre travels a closed ellipse whose period is the loop length.
- The web snippet uses the official Paper Shaders `Dithering` component, which is two-colour: base and front. It animates live, so it needs no loop.
