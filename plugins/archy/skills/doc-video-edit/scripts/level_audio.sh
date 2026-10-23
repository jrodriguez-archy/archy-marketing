#!/bin/bash
# Two-pass loudness normalisation (linear) to a 48 kHz 24-bit WAV derivative. The original is untouched.
#   level_audio.sh IN OUT.wav LUFS [prefilter]
#   dialogue: level_audio.sh camA.wav dialogue_lev-16.wav -16 "highpass=f=70,"
#   music:    level_audio.sh music.mp3 music_lev-18.wav -18
# True peak is limited to -1.5 dBFS. Prints the measured result.
set -euo pipefail
IN="$1"; OUT="$2"; I="$3"; PRE="${4:-}"
J=$(ffmpeg -nostats -i "$IN" -af "${PRE}loudnorm=I=${I}:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
MI=$(echo "$J" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y -i "$IN" -af "${PRE}loudnorm=I=${I}:TP=-1.5:LRA=11:${MI}:linear=true" -ar 48000 -c:a pcm_s24le "$OUT"
ffmpeg -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
