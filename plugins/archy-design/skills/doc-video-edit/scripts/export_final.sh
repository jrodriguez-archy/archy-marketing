#!/bin/bash
# OPTIONAL export, for 10-bit final camera files only (the standard is the direct `tsrct export`, see
# references/color-guide.md section 5). Tesseract's direct MP4 is ~10 Mbps H.264 and turns the flat, graded background into
# visible steps and blocks. Export a ProRes master instead and encode the delivery MP4 with x264 at CRF 16
# (tune grain keeps the fine grain that breaks the gradient steps). The ProRes master is temporary (~4 GB/min).
#   export_final.sh PROJECT_DIR OUT.mp4 [TMP_DIR]
set -euo pipefail
ROOT="$1"; OUT="$2"; TMP="${3:-${TMPDIR:-/tmp}}"
T="${TSRCT:-$HOME/Library/Application Support/Tesseract/bin/tsrct}"
PROJECT="$ROOT/$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['project'])" "$ROOT/.tesseract-work/video.json")"
MASTER="$TMP/$(basename "${OUT%.*}")_master.mov"
cleanup() { rm -f -- "$MASTER"; }
trap cleanup EXIT
"$T" export --project "$PROJECT" --fps 24 --format prores --output "$MASTER" >/dev/null
ffmpeg -v error -y -i "$MASTER" -c:v libx264 -preset slow -crf 16 -tune grain -pix_fmt yuv420p \
  -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 256k -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration,bit_rate -of compact "$OUT"
