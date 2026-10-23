#!/bin/bash
# The design tools used to ship in the separate archy-design plugin, whose data folder
# (work directories, venvs, the Figma plugin copy) has another name. Link each of its
# tool folders into this plugin's data folder, in place, so nothing moves and absolute
# paths keep working. Silent, idempotent, and a no-op on new installs.
new="${CLAUDE_PLUGIN_DATA:-}"
[ -n "$new" ] || exit 0
old="$(dirname "$new")/archy-design-${new##*/archy-}"
[ -d "$old" ] || exit 0
mkdir -p "$new" || exit 0
for dir in "$old"/*/; do
  [ -d "$dir" ] || continue
  tool="$(basename "$dir")"
  [ -e "$new/$tool" ] || [ -L "$new/$tool" ] || ln -s "$old/$tool" "$new/$tool"
done
exit 0
