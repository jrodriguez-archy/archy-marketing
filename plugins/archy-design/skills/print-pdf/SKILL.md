---
name: print-pdf
description: Turns a Paper PDF export into a print-ready file at the exact physical size (with bleed and optional crop marks), text converted to curves, optionally converted to CMYK with a pure-black QR code, and verifies the plates. Use when an artboard is going to a printer, needs a specific page size in inches, needs CMYK, bleed or crop marks, needs its text outlined, or when a Paper PDF export has the wrong size or a blank extra page.
---

# Print-ready PDF from Paper

Paper's PDF export is not print-ready. This skill fixes page size, drops the extra page, outlines the text, adds crop marks when asked, converts to CMYK and makes a QR pure K. Work in `${CLAUDE_PLUGIN_DATA}/print-pdf/<project>/` (call it `$WORK`). Everything below is Ghostscript and qpdf, plus one bundled PostScript prelude for crop marks (`scripts/marks.ps`). Create `$WORK` first (`mkdir -p "$WORK"`) and keep every intermediate file there, never inside `${CLAUDE_PLUGIN_ROOT}`.

## 1. Preflight

Check each tool answers; if any is missing, tell the user exactly what to install (Homebrew):

| Check | Install |
|---|---|
| `gs --version` | `brew install ghostscript` |
| `qpdf --version` (also provides `fix-qdf`) | `brew install qpdf` |
| `pdfinfo -v` | `brew install poppler` |

For CMYK you also need Adobe's `CoatedGRACoL2006.icc`. On a Mac with Acrobat it ships in `/Library/Application Support/Adobe/Color/Profiles/Recommended/`. **Copy it into `$WORK` first**: Ghostscript is denied read access to that folder.

## 2. Export from Paper

1. **Design the artboard at bleed size** when the printer needs bleed (most do; 0.125 in per side is the usual default): the artboard is trim + bleed, every ground and edge-touching shape runs to the artboard edge, and content stays inside a safe zone. Nothing later in this pipeline can invent bleed.
2. **Hide guide layers** (trim, safe zone) with `opacity: 0`, export, then set them back to `opacity: 1`. Do not hide them with `display: none`: switching back to `block` strips `position: absolute` from their children and the guides land stacked at the frame's corner (see `archy:brand` → `paper-quirks.md`).
3. `open_file` on the artboard's page. `export_combined_pdf` only assembles artboards on the **active** page; otherwise every node fails with `Error assembling PDF page for "<name>"`, repeating one name for all of them.
4. Export the PDF. Several artboards of one piece (front and back) go in one `export_combined_pdf`, one page each. `export` and `export_combined_pdf` **ignore `outputPath` / `outputDirectory` and always write to `~/Downloads`**, auto-incrementing (`Combined.pdf`, `Combined (1).pdf`). `export`'s `scale` is a string (`"1x"`).
5. macOS TCC blocks the shell from listing `~/Downloads`, with or without the sandbox. Move the file with Finder, which is the only scripted route:
   ```bash
   osascript -e 'tell application "Finder" to move file "Combined.pdf" of (path to downloads folder) to POSIX file "'"$WORK"'" as alias'
   ```
6. If the piece has a QR code, set it to `--color-black` in the design itself (preferred: what you see is what prints); otherwise export a **second copy with the QR at `--color-black`** for step 6.

## 3. What is wrong with Paper's PDF

Verified on a 1600 × 975 canvas meant for 8 × 4.875 in:

1. The page is **0.75 pt per canvas px** (1600 px → 1200 pt = 16.67 in), and the height comes out 731.04, not 731.25, so the aspect is a hair off. `pdfinfo` gives the exact source size (`SW` × `SH`) for the formulas below.
2. A single-artboard PDF carries a **blank grey second page**. A combined export of several artboards has exactly one page per artboard.
3. A CSS gradient ground is **rasterised at 1× (800 × 487 px)**, while text, icons and SVG stay vector with fonts embedded (Type 3).
4. Every page starts with a **full-page fill of the canvas colour** (light grey `#EEEEEE` or dark `#282828`, depending on the app) under the artboard's own ground. The ground covers it exactly, so it does not print, but check the bleed edges on the plates (step 7).

## 4. Fix size and pages, outline the text (Ghostscript)

Force the physical size (trim + bleed), scale by **height**, centre the tiny horizontal overshoot so no white hairline appears on a coloured ground, and convert all text to curves with `-dNoOutputFonts` (printers and Illustrator then never need the fonts):

```bash
gs -o "$WORK/trim.pdf" -sDEVICE=pdfwrite -dFIXEDMEDIA \
   -dDEVICEWIDTHPOINTS=576 -dDEVICEHEIGHTPOINTS=351 -dNoOutputFonts \
   -c "<</Install {Tx 0 translate S S scale}>> setpagedevice" -f "$WORK/in.pdf"
```

`S` = target height ÷ source height, `Tx` = (target width − source width × `S`) ÷ 2. Example for 8 × 4.875 in from 1200 × 731.04 pt: `S` = 351 / 731.04, `Tx` ≈ −0.08. Target points are inches × 72. Add `-dFirstPage=1 -dLastPage=1` for a single-artboard export, to drop the blank page.

Check: `pdfinfo "$WORK/trim.pdf"` reports the target, e.g. `Page size: 576 x 351 pts` (= 8 × 4.875 in), and the expected page count; `pdffonts` lists **no fonts** (the text is curves).

## 5. Crop marks (when the printer wants them)

Run `scripts/marks.ps` instead of step 4's `-c` Install. It places each page (artwork already at trim + bleed) on a sheet 0.5 in larger than trim on every side, draws 0.25 pt crop marks in registration colour starting 3 pt past the bleed, and writes `TrimBox` and `BleedBox`, so imposition software reads the cut directly:

```bash
gs -o "$WORK/trim.pdf" -sDEVICE=pdfwrite -dFIXEDMEDIA \
   -dDEVICEWIDTHPOINTS=<TW+72> -dDEVICEHEIGHTPOINTS=<TH+72> -dNoOutputFonts \
   -dTW=<trim w> -dTH=<trim h> -dBL=<bleed> -dSW=<source w> -dSH=<source h> \
   "${CLAUDE_PLUGIN_ROOT}/skills/print-pdf/scripts/marks.ps" -f "$WORK/in.pdf"
```

Business card example (3.5 × 2 in, 0.125 in bleed, 1125 × 675 px artboard): `-dDEVICEWIDTHPOINTS=324 -dDEVICEHEIGHTPOINTS=216 -dTW=252 -dTH=144 -dBL=9 -dSW=844.08 -dSH=505.92`. Check with `pdfinfo -box`: `TrimBox 36 36 288 180`, `BleedBox 27 27 297 189`.

Ghostscript's `initgraphics` re-applies the `Install` transform, so marks drawn after it land scaled inside the artwork; the prelude undoes the transform first. If you write your own marks, render the page and look before trusting it.

## 6. CMYK and a pure-K QR

**Before exporting, swap the mascot's tone-matched edges to their print colours** (the print column in `archy:brand` → `composition.md`, *Colour against the ground*). An edge that is barely there on screen disappears on press, where blues print duller; the width stays the same.

1. Convert with the profile: `-sColorConversionStrategy=CMYK -dRenderIntent=1`, with `CoatedGRACoL2006.icc` from `$WORK` as the output profile. Ghostscript may print `Permission denied` / `/undefined in --runpdf--` at the end of a run in a sandboxed shell; the output is still complete, which step 7 confirms.
2. RGB black converts to a 4-colour rich black (C86 M77 Y70 K96). **A QR must be pure K.** With the QR at `--color-black`:
   ```bash
   qpdf --qdf --object-streams=disable "$WORK/cmyk.pdf" "$WORK/cmyk.qdf.pdf"
   LC_ALL=C sed 's/^0\.859 0\.765 0\.702 0\.961 k$/0 0 0 1 k/; s/^0\.859 0\.765 0\.702 0\.961 K$/0 0 0 1 K/' \
     "$WORK/cmyk.qdf.pdf" > "$WORK/fixed.qdf.pdf"
   fix-qdf "$WORK/fixed.qdf.pdf" > "$WORK/final.pdf"
   ```
   List the colours first (`grep -a -o -E "[0-9.]+ [0-9.]+ [0-9.]+ [0-9.]+ [kK]$" … | sort | uniq -c`) and confirm the rich-black value is the QR's and nothing else uses black.
3. `--color-royal-blue-500` lands at ~C88 M70 and prints visibly duller than on screen. Warn the requester. A piece that must match material already printed can carry print-equivalent tokens (see `archy:brand` → `tokens.md`, *Print-equivalent tokens*).

## 7. Verify the plates

```bash
gs -o "$WORK/sep%d.tif" -sDEVICE=tiffsep -r600 "$WORK/final.pdf"
```

Do **not** pass `OutputICCProfile` here, or the plates get re-mapped. Then confirm:

- [ ] C, M and Y are 0 under every 100% K pixel inside the bleed box (crop marks are registration, all four plates, by design).
- [ ] The QR decodes from the Black plate alone (e.g. OpenCV `QRCodeDetector` on the `(Black)` plate) and opens the right link.
- [ ] `pdfinfo` shows the physical size and the expected page count; with crop marks, `pdfinfo -box` shows the trim and bleed boxes.
- [ ] `pdffonts` lists no fonts and `pdfimages -list` lists no images, unless the piece has a photo or a gradient ground.
- [ ] Nothing dark on the bleed edges beyond what the design puts there (step 3, point 4).
- [ ] Render the pages to PNG and look at them, crop marks included.

## 8. Deliver

- **The combined file is the delivery.** Illustrator opens a multi-page PDF with "All" as embedded PDF objects that behave like images; opening one page at a time (*Page preview*) brings it in as editable curves. Split pages into separate files (`qpdf final.pdf --pages . <n> -- "<name> - <Side>.pdf"`) only when the requester asks for them. Business cards never ship single pages (see `business-card`).
- Name the files `<Piece> - Print CMYK - Crop Marks.pdf` / `<Piece> - Print CMYK - Bleed.pdf` so the version is clear without opening them.
- Confirm the printer's bleed and crop-mark requirements before sending. When they are unknown, send both versions (with crop marks, and bleed only).
