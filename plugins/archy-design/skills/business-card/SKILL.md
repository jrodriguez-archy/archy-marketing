---
name: business-card
description: Makes print-ready Archy business cards (3.5 × 2 in) for one or more people from the templates in the Archy - Business Cards Paper file: fills name, role, email and phone, generates and verifies a HubSpot booking QR for the QR back, and exports CMYK PDFs with bleed, with and without crop marks. Use when a designer needs a business card for someone, a batch of cards, a QR card, or the card templates changed.
---

# Business cards

For designers. Load `archy:brand` first (tokens, Paper quirks). Cards are print pieces: they use the file's **print-equivalent tokens** (`archy:brand` → `tokens.md`) so what is on screen is what comes off the press, and they always finish with the `print-pdf` skill.

## The file

`Archy - Business Cards`, `app.paper.design/file/01M46XGRN8YXH5EXG4QSX0N446`. Page `Business Cards` holds the templates; the slot table is in `archy:brand` → `templates.md`, *Archy - Business Cards*.

| Template | Use |
|---|---|
| `TPL · Business Card · Front 3.5×2 in` | Every card. Same for everyone, no slots |
| `TPL · Business Card · Back 3.5×2 in` | Back with the arc: no booking link |
| `TPL · Business Card · Back QR 3.5×2 in` | Back with the `SCAN TO BOOK` QR plate: the person has a HubSpot meetings link |

Artboards are **1125 × 675 px**: 3.5 × 2 in trim at 300 px/in plus 0.125 in bleed (37.5 px) per side. Each carries a `Guides` frame on top: `Guide · Trim` (red) and `Guide · Safe Zone` (green, the box all content touches). Never write into the `TPL` artboards.

## 1. Ask once for

Per person: full name as it should read (and where a compound name breaks), exact role, email, phone in the format to print, and the HubSpot meetings link if the card gets a QR. Never invent any of them; a missing phone or link means asking, not guessing. Also ask whether the printer has bleed or crop-mark requirements and a colour profile; without an answer, deliver both versions (step 5) with GRACoL.

## 2. Build the cards

1. Work on a page named for the print batch (e.g. `Oct 2026 - 1`); create it if it does not exist. Duplicate the Front and the right Back onto it with `duplicate_nodes` and `parentId: root_node_<pageId>`, then set `left` / `top` / `translate: none` (copies land anywhere). One row per person: Front at x 0, Back at x 1205.
2. Rename: `<Full Name> · Front 3.5×2 in`, `<Full Name> · Back 3.5×2 in` or `<Full Name> · Back QR 3.5×2 in`.
3. Fill the slots with `set_text_content`:
   - `slot-text-name`: first name, `\n`, last name.
   - `slot-text-role`: one line at 50 / 60 px when it fits; a role that does not fit the column wraps to two lines at **40 / 49 px** (`Sales Development\nRepresentative`). The Details block is anchored to the bottom, so a second line grows upward and the phone line stays aligned with `archy.com`.
   - `slot-text-email`, `slot-text-phone`.
4. QR back only: generate the QR (step 3) and replace the placeholder `slot-image-qr` with `write_html` in `replace` mode, keeping its size (254 × 254), `flex-shrink: 0` and `shape-rendering="crispEdges"`. Name it `slot-image-qr · <Full Name> HubSpot`. The modules are `--color-black` so they print pure K.
5. Screenshot each artboard with the guides on: everything inside the green safe zone, nothing touching the QR plate. A screenshot can come back before a large SVG renders; take it again before assuming it is missing.

## 3. The QR

Generate it, never redraw or trace it, from the exact link the person gave:

```bash
python3 -m venv "${CLAUDE_PLUGIN_DATA}/qr-venv"
"${CLAUDE_PLUGIN_DATA}/qr-venv/bin/pip" install -q segno numpy opencv-python-headless
"${CLAUDE_PLUGIN_DATA}/qr-venv/bin/python" "${CLAUDE_PLUGIN_ROOT}/skills/business-card/scripts/make_qr.py" "<link>" --out "$WORK/qr.d"
```

It defaults to version 7, error correction Q (45 modules, the density the plate is designed for), refuses to output a code that does not decode back to the exact link, and prints the path `d` for `viewBox="0 0 45 45"`. After export, `print-pdf` checks the QR again from the black plate alone. The template's placeholder pattern does not scan on purpose: a card that ships with it fails at proof, not in someone's hand.

## 4. Export

Follow `print-pdf` with these values:

- Hide every `Guides` frame with `opacity: 0`, export, then restore `opacity: 1` (never `display: none`).
- `export_combined_pdf` with the person's Front and Back: 2 pages. Source page size is `844.08 × 505.92` pt.
- Outline the text, convert to CMYK (GRACoL 2006, intent 1) and rewrite the QR's rich black to `0 0 0 1 k`.

## 5. Deliver both versions

Every card ships as exactly two PDFs, both keeping the 0.125 in bleed and each holding both sides (page 1 Front, page 2 Back):

| Version | Page | How |
|---|---|---|
| `<Full Name> - Business Card - Print - Bleed - Crop Marks.pdf` | 4.5 × 3 in (324 × 216 pt), card centred, crop marks, TrimBox / BleedBox | `print-pdf` step 5 with `-dTW=252 -dTH=144 -dBL=9 -dSW=844.08 -dSH=505.92` |
| `<Full Name> - Business Card - Print - Bleed.pdf` | 3.75 × 2.25 in (270 × 162 pt), no marks | `print-pdf` step 4 at 270 × 162 |

Both names say `Bleed` because both files carry it; only one adds `Crop Marks`. `Print` already means CMYK, so the colour space is not in the name. No single-page files for cards: the two PDFs are the delivery. Group them per batch and person: `<batch>/<Full Name>/`. If someone needs to edit a side in Illustrator, they open that page alone (Illustrator's PDF import, *Page preview* on one page), which comes in as editable curves.

Before handing over, run the `print-pdf` plate checks, render both versions and look at them, and ask the requester to scan the QR from the PDF with a phone.

## Template notes

- **Colours are print-equivalent tokens** (`--color-print-*`), measured from cards already printed, so a reprint matches the stock. Do not swap them for the screen tokens.
- **Front pattern:** the moon pattern is one vector layer in `--color-print-navy`, scaled to run through the bleed.
- **Safe zone:** inset from trim 78 px left and right, 64 px top, 54 px bottom (the text boxes' own line-height space evens it out visually). The wordmark, name, QR plate, arc, Details block and `archy.com` all touch it.
- When a new back variant is needed, duplicate a `TPL` back, keep the bottom-anchored Details block and the guides, and add it to the catalog with `prepare-template`.
