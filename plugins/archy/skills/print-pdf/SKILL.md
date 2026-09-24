---
name: print-pdf
description: Turns a Paper PDF export into a print-ready file at the exact physical trim size, optionally converted to CMYK with a pure-black QR code, and verifies the plates. Use when an artboard is going to a printer, needs a specific page size in inches, needs CMYK, or when a Paper PDF export has the wrong size or a blank extra page.
---

# Print-ready PDF from Paper

Paper's PDF export is not print-ready. This skill fixes page size, drops the extra page, converts to CMYK and makes a QR pure K. Work in `${CLAUDE_PLUGIN_DATA}/print-pdf/<project>/` (call it `$WORK`).

## 1. Preflight

Check each tool answers; if any is missing, tell the user exactly what to install (Homebrew):

| Check | Install |
|---|---|
| `gs --version` | `brew install ghostscript` |
| `qpdf --version` (also provides `fix-qdf`) | `brew install qpdf` |
| `pdfinfo -v` | `brew install poppler` |

For CMYK you also need Adobe's `CoatedGRACoL2006.icc`. On a Mac with Acrobat it ships in `/Library/Application Support/Adobe/Color/Profiles/Recommended/`. **Copy it into `$WORK` first**: Ghostscript is denied read access to that folder.

## 2. Export from Paper

1. `open_file` on the artboard's page. `export_combined_pdf` only assembles artboards on the **active** page; otherwise every node fails with `Error assembling PDF page for "<name>"`, repeating one name for all of them.
2. Export the PDF. `export` and `export_combined_pdf` **ignore `outputPath` / `outputDirectory` and always write to `~/Downloads`**, auto-incrementing (`Combined.pdf`, `Combined (1).pdf`). `export`'s `scale` is a string (`"1x"`).
3. macOS TCC blocks the shell from listing `~/Downloads`, with or without the sandbox. Move the file with Finder, which is the only scripted route:
   ```bash
   osascript -e 'tell application "Finder" to move file "Combined.pdf" of (path to downloads folder) to POSIX file "'"$WORK"'" as alias'
   ```
4. If the piece has a QR code, export a **second copy with the QR set to `--color-black`** for step 5.

## 3. What is wrong with Paper's PDF

Verified on a 1600 × 975 canvas meant for 8 × 4.875 in:

1. The page is **0.75 pt per canvas px** (1600 px → 1200 pt = 16.67 in), and the height comes out 731.04, not 731.25, so the aspect is a hair off.
2. Every PDF carries a **blank grey second page**.
3. A CSS gradient ground is **rasterised at 1× (800 × 487 px)**, while text, icons and SVG stay vector with fonts embedded.

## 4. Fix size and pages (Ghostscript)

Keep page 1 only, force the physical size, and scale by **height**, centring the tiny horizontal overshoot so no white hairline appears on a coloured ground:

```bash
gs -o "$WORK/trim.pdf" -sDEVICE=pdfwrite \
   -dFirstPage=1 -dLastPage=1 -dFIXEDMEDIA \
   -dDEVICEWIDTHPOINTS=576 -dDEVICEHEIGHTPOINTS=351 \
   -c "<</Install {Tx 0 translate S S scale}>> setpagedevice" -f "$WORK/in.pdf"
```

`S` = target height ÷ source height, `Tx` = (target width − source width × `S`) ÷ 2. Example for 8 × 4.875 in from 1200 × 731.04 pt: `S` = 351 / 731.04, `Tx` ≈ −0.08. Target points are inches × 72.

Check: `pdfinfo "$WORK/trim.pdf"` must report the target, e.g. `Page size: 576 x 351 pts` (= 8 × 4.875 in), and `Pages: 1`.

## 5. CMYK and a pure-K QR

1. Convert with the profile: `-sColorConversionStrategy=CMYK -dRenderIntent=1`, with `CoatedGRACoL2006.icc` from `$WORK` as the output profile.
2. RGB black converts to a 4-colour rich black (C86 M77 Y70 K96). **A QR must be pure K.** Using the copy exported with the QR at `--color-black`:
   ```bash
   qpdf --qdf --object-streams=disable "$WORK/cmyk.pdf" "$WORK/cmyk.qdf.pdf"
   # rewrite the QR's exact `k` operator (its rich-black values) to: 0 0 0 1 k
   fix-qdf "$WORK/cmyk.qdf.pdf" > "$WORK/final.pdf"
   ```
3. `--color-royal-blue-500` lands at ~C88 M70 and prints visibly duller than on screen. Warn the requester.

## 6. Verify the plates

```bash
gs -o "$WORK/sep.tif" -sDEVICE=tiffsep -r300 "$WORK/final.pdf"
```

Do **not** pass `OutputICCProfile` here, or the plates get re-mapped. Then confirm:

- [ ] C, M and Y are 0 under every 100% K pixel.
- [ ] The QR decodes from the Black plate alone.
- [ ] `pdfinfo` shows the physical size and one page.
- [ ] Text is still vector with fonts embedded; only a gradient ground is raster.
- [ ] Bleed: nothing in this pipeline adds bleed. Confirm the printer's bleed requirement before sending.
