# gradients

Archy pixel gradients (the Gradients page of the Brand file) as static PNG, seamless video loops and web snippets. Python 3 + Pillow; `video` also needs `ffmpeg`.

```bash
TOOL="${CLAUDE_PLUGIN_ROOT}/tools/gradients/gradients.py"
python3 "$TOOL" list                          # the nine gradients, tokens and resolved hex
python3 "$TOOL" png all --out ./gradients     # 3456x1944 statics (2x of 1728x972)
python3 "$TOOL" video royal-blue --out ./gradients                   # 8 s, 30 fps, 1920x1080 mp4
python3 "$TOOL" video all --format webm --seconds 12 --out ./gradients
python3 "$TOOL" frames royal-blue --count 4 --out ./gradients        # poster frames of the loop
python3 "$TOOL" web royal-blue                # <Dithering> snippet for @paper-design/shaders-react
```

- `presets.json` is the single definition: each gradient is a base token plus a front colour that moves `amount` of the way toward a second token. The recipe (8x8 Bayer, size 8.8, 6 steps, scale 1.08) and the six blobs are shared, so the family stays consistent.
- Loops are seamless by construction: each blob centre travels a closed ellipse whose period is the loop length.
- The web snippet uses the official Paper Shaders `Dithering` component, which is two-colour: base and front. It animates live, so it needs no loop.
