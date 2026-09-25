#!/usr/bin/env bash
# Build the deck, or just part of it.
#
#   export.sh                 every dump          -> <project>.pptx
#   export.sh 94              one slide           -> <project>-94.pptx
#   export.sh 66-70           a range             -> <project>-66-70.pptx
#   export.sh 66-70,94 out.pptx
#   export.sh --work DIR 94   same, with the work directory given explicitly
#
# <project> is the work directory's own name. The selection is by the dump's numeric
# prefix, which is also the deck order. A partial build is safe only when the deck's meta
# line carries no page number: in the template library, where the meta is "NN", build.js
# fills it from position and a partial build would number from 1.
#
# Paths. The script's own directory is the plugin folder and is never written to. Dumps,
# assets and the output live in the work directory:
#   --work DIR  >  $ARCHY_WORK  >  $BASE
# where BASE is $ARCHY_WORK_BASE, else ${CLAUDE_PLUGIN_DATA}/slides-export, else
# ./archy-work/slides-export. node_modules and .venv are installed once in BASE.
set -euo pipefail
TOOLS="$(cd "$(dirname "$0")" && pwd)"

if [ "${1:-}" = "--work" ]; then ARCHY_WORK="$2"; shift 2
elif [[ "${1:-}" == --work=* ]]; then ARCHY_WORK="${1#--work=}"; shift
fi

if [ -n "${ARCHY_WORK_BASE:-}" ]; then BASE="$ARCHY_WORK_BASE"
elif [ -n "${CLAUDE_PLUGIN_DATA:-}" ]; then BASE="$CLAUDE_PLUGIN_DATA/slides-export"
else BASE="$PWD/archy-work/slides-export"
fi
WORK="${ARCHY_WORK:-$BASE}"
mkdir -p "$WORK" "$BASE"
WORK="$(cd "$WORK" && pwd)"
BASE="$(cd "$BASE" && pwd)"
export ARCHY_WORK="$WORK" ARCHY_WORK_BASE="$BASE"
cd "$WORK"

# The Python that has Pillow, lxml and cairosvg: $ARCHY_PYTHON, else a .venv in the work
# directory, in BASE, or in the work directory's parent, else python3 on the PATH.
PY="${ARCHY_PYTHON:-}"
if [ -z "$PY" ]; then
  for v in "$WORK/.venv" "$BASE/.venv" "$(dirname "$WORK")/.venv"; do
    if [ -x "$v/bin/python" ]; then PY="$v/bin/python"; break; fi
  done
fi
PY="${PY:-python3}"

[ -d dump ] || { echo "no dump/ in $WORK" >&2; exit 1; }
PROJECT="$(basename "$WORK")"

RANGE="${1:-}"
if [ -z "$RANGE" ]; then
  FILES=(dump/)
  OUT="${2:-$PROJECT.pptx}"
else
  FILES=()
  IFS=',' read -ra PARTS <<< "$RANGE"
  for part in "${PARTS[@]}"; do
    if [[ "$part" == *-* ]]; then lo="${part%-*}"; hi="${part#*-}"; else lo="$part"; hi="$part"; fi
    for n in $(seq "$lo" "$hi"); do
      for f in dump/"$n"-*.json; do [ -e "$f" ] && FILES+=("$f"); done
    done
  done
  [ ${#FILES[@]} -eq 0 ] && { echo "no dumps match $RANGE" >&2; exit 1; }
  OUT="${2:-$PROJECT-$RANGE.pptx}"
fi

mkdir -p scratchpad
SPECS="scratchpad/specs-partial.json"
node "$TOOLS/paper2spec.js" "${FILES[@]}" > "$SPECS"
node "$TOOLS/build.js" "$SPECS" "$OUT"
"$PY" "$TOOLS/postprocess.py" "$OUT"
"$PY" "$TOOLS/shrink-media.py" "$OUT"
