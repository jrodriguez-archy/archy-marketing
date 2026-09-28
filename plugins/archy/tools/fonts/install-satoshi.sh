#!/bin/bash
# Installs Satoshi (DOC's typeface) for the current macOS user, straight from Fontshare.
# The font is licensed per user under the ITF Free Font License, so it is downloaded
# from its official source and never shipped in this repository.
#
# Usage: install-satoshi.sh            install if missing
#        install-satoshi.sh --check    only report whether it is installed (exit 0 yes, 1 no)
# FONT_DIR overrides the target folder (default ~/Library/Fonts), for testing.

set -u
URL="https://api.fontshare.com/v2/fonts/download/satoshi"
PAGE="https://www.fontshare.com/fonts/satoshi"
FONT_DIR="${FONT_DIR:-$HOME/Library/Fonts}"

installed() {
  [ -f "$FONT_DIR/Satoshi-Regular.otf" ] || [ -f "/Library/Fonts/Satoshi-Regular.otf" ]
}

# macOS does not always pick up files dropped into ~/Library/Fonts (for example when the folder
# did not exist before), and then no app can see the font. Register each file with CoreText for
# the current user, which is what Font Book does, and report whether the system now lists it.
register_fonts() {
  [ "$FONT_DIR" = "$HOME/Library/Fonts" ] || return 0
  osascript -l JavaScript >/dev/null 2>&1 <<EOF
ObjC.import('CoreText'); ObjC.import('Foundation');
var dir = "$FONT_DIR";
var names = \$.NSFileManager.defaultManager.contentsOfDirectoryAtPathError(dir, null).js.map(function (x) { return x.js; });
names.filter(function (n) { return /^Satoshi.*\.otf$/.test(n); }).forEach(function (n) {
  \$.CTFontManagerRegisterFontsForURL(\$.NSURL.fileURLWithPath(dir + '/' + n), 2, null);
});
EOF
}

system_lists_satoshi() {
  osascript -l JavaScript -e 'ObjC.import("AppKit"); $.NSFontManager.sharedFontManager.availableFontFamilies.js.map(function(x){return x.js;}).indexOf("Satoshi") >= 0' 2>/dev/null | grep -q true
}

manual() {
  cat <<EOF
Could not install Satoshi automatically ($1).
Install it by hand:
  1. Open $PAGE and click "Download family".
  2. Unzip it, open the Fonts/OTF folder, select every .otf file, double-click and choose Install.
  3. Quit Paper completely (Cmd+Q) and open it again.
EOF
  exit 1
}

if [ "${1:-}" = "--check" ]; then
  if installed; then echo "Satoshi is installed."; exit 0; else echo "Satoshi is not installed."; exit 1; fi
fi

if installed; then
  register_fonts
  if [ "$FONT_DIR" = "$HOME/Library/Fonts" ] && ! system_lists_satoshi; then
    manual "the files are in place but macOS does not list the font"
  fi
  echo "Satoshi is installed. If Paper still shows another typeface, quit Paper (Cmd+Q) and open it again."
  exit 0
fi

TMP="$(mktemp -d)" || manual "no temporary folder"
trap 'rm -rf "$TMP"' EXIT

curl -fsSL -o "$TMP/satoshi.zip" "$URL" || manual "the download from Fontshare failed"
unzip -q "$TMP/satoshi.zip" -d "$TMP" || manual "the download is not a valid zip"

OTF_DIR="$(find "$TMP" -type d -path '*Fonts/OTF' | head -1)"
[ -n "$OTF_DIR" ] && ls "$OTF_DIR"/Satoshi-*.otf >/dev/null 2>&1 || manual "the package has no OTF files"

mkdir -p "$FONT_DIR" || manual "cannot write to $FONT_DIR"
cp "$OTF_DIR"/Satoshi-*.otf "$FONT_DIR"/ || manual "cannot copy into $FONT_DIR"
# Files that arrive from a download carry a quarantine flag that can keep apps from loading them.
xattr -d com.apple.quarantine "$FONT_DIR"/Satoshi-*.otf 2>/dev/null || true
register_fonts

if [ "$FONT_DIR" = "$HOME/Library/Fonts" ] && ! system_lists_satoshi; then
  manual "the files were copied but macOS does not list the font"
fi
echo "Installed $(ls "$FONT_DIR"/Satoshi-*.otf | wc -l | tr -d ' ') Satoshi files into $FONT_DIR."
echo "Now quit Paper completely (Cmd+Q) and open it again so it picks the font up."
