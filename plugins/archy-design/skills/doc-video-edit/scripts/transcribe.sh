#!/bin/bash
# Local transcription with whisper.cpp (nothing leaves the machine).
#   transcribe.sh MEDIA OUT_DIR            -> transcript.srt, transcript.txt, words.json ([start, end, word], s)
#   transcribe.sh MEDIA OUT_DIR START DUR "prompt"   -> a prompted pass on one range (keeps disfluencies
#                                            such as "with a, with a" that the normal pass cleans up)
# Finds whisper-cli via $WHISPER_CLI, ~/.local/whisper.cpp/build/bin, or PATH; the model via
# $WHISPER_MODEL or ~/.cache/whisper/ggml-medium.en.bin. See SKILL.md > Setup to install them.
set -euo pipefail
MEDIA="$1"; OUT="$2"; mkdir -p "$OUT"
CLI="${WHISPER_CLI:-}"
[ -z "$CLI" ] && [ -x "$HOME/.local/whisper.cpp/build/bin/whisper-cli" ] && CLI="$HOME/.local/whisper.cpp/build/bin/whisper-cli"
[ -z "$CLI" ] && CLI="$(command -v whisper-cli || true)"
[ -z "$CLI" ] && { echo "whisper-cli not found (see SKILL.md > Setup)"; exit 1; }
MODEL="${WHISPER_MODEL:-$HOME/.cache/whisper/ggml-medium.en.bin}"
[ -f "$MODEL" ] || { echo "model not found: $MODEL"; exit 1; }

if [ $# -ge 5 ]; then
  START="$3"; DUR="$4"; PROMPT="$5"
  ffmpeg -v error -y -ss "$START" -t "$DUR" -i "$MEDIA" -ac 1 -ar 16000 "$OUT/range_16k.wav"
  "$CLI" -m "$MODEL" -f "$OUT/range_16k.wav" -l en -ml 1 --prompt "$PROMPT" -otxt -of "$OUT/range" -np >/dev/null 2>&1
  echo "words from ${START}s (offsets relative to the range):"; tr '\n' ' ' < "$OUT/range.txt"; echo
  exit 0
fi

ffmpeg -v error -y -i "$MEDIA" -ac 1 -ar 16000 -c:a pcm_s16le "$OUT/audio_16k.wav"
"$CLI" -m "$MODEL" -f "$OUT/audio_16k.wav" -l en -osrt -otxt -of "$OUT/transcript" -np >/dev/null 2>&1
"$CLI" -m "$MODEL" -f "$OUT/audio_16k.wav" -l en -ml 1 -sow -ojf -of "$OUT/transcript_words" -np >/dev/null 2>&1
python3 - "$OUT" <<'EOF'
import json, sys, os
out = sys.argv[1]
d = json.load(open(os.path.join(out, "transcript_words.json")))
words = [(s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000, s["text"].strip())
         for s in d["transcription"] if s["text"].strip()]
json.dump(words, open(os.path.join(out, "words.json"), "w"))
print(f"{len(words)} words -> {out}/words.json, transcript.srt")
EOF
