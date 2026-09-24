---
name: social-post
description: Create Archy event social posts in Paper (Instagram/LinkedIn Post 1080×1350, Stories 1080×1920, OG link preview 1200×630) from the approved Small Events templates. Use when someone needs social art for a trade show, dental meeting, booth invite, speaker event or day-before reminder.
---

# Archy event social posts

Load the `brand` skill first. Its hard rules apply here without exception: duplicate a master, change only slots, only `ready` templates, US English, never shrink type, never invent facts.

**Paper file:** `Small Events - 2026`. Masters on `Templates`, work on `Output`, partner logos on `Assets`, past campaigns on `Archive`.

## 1. Preflight

1. `get_basic_info` with no `fileId`. The file name must be `Small Events - 2026` and its pages must include `Templates`, `Output` and `Assets`. If not, tell the user: "Open **Small Events - 2026** in Paper Desktop, then ask me again." Stop.
2. Read `../brand/references/templates.md`, section *Small Events - 2026*, and `../brand/references/paper-quirks.md` once per session.

## 2. Choose the template

Match the brief to a template's **Use when / Not when**. Only templates marked **ready** can be used.

- One ready template fits: name it to the user and continue.
- It fits but is `not prepared`: name every template that fits, say none is prepared yet and that Marketing & Design has to prepare one. Stop.
- Nothing fits: say so, name the closest template and why it does not fit. Stop. Never build a layout.

## 3. Collect the brief

Ask, in one message, for every fact the template's slots need and that the user has not given. For `Booth Icon List`: event name and year, city and state, venue, dates, booth number, partner logo, and which formats (default: all three).

Then check every string against the slot limits in the catalog:
- Fits: use it exactly as given, apart from the mechanics in `voice.md` (date format, `City, ST`, `#` before the booth).
- Too long: propose a shorter version and wait for approval. Never cut words silently, never reduce type.
- Partner logo missing from `Assets`: do not build anything. Ask for it to be added, in the same message as any copy that needs approval.

Show the final copy per format and get a yes before writing to the canvas.

## 4. Build each format

For each format, in this order: Post, Stories, OG.

1. `duplicate_nodes` the master with `parentId: "root_node_<Output pageId>"`.
2. Rename the copy `<Event short name> <year> · <Format> <W×H>`, e.g. `Hinman 2027 · Post 1080×1350`.
3. `update_styles` on the new artboard only: integer `left`/`top`, `translate: none`. Each campaign gets its own row on `Output`: Post at `left: 0`, Stories at 1160, OG at 2320, and `top` 80px below the tallest artboard already there.
4. Use the `descendantIdMap` to find each `slot-*` node in the copy, then `set_text_content` in one batch. On the OG headline, put the line break yourself with `\n`.
5. Partner logo, if it changes: `delete_nodes` the SVG inside `slot-logo-partner`, `duplicate_nodes` the approved logo from `Assets` with `parentId` = the copy's `slot-logo-partner` frame, then set that SVG's `width`/`height` to the format's logo height, keeping its aspect ratio.
6. Nothing else. No `write_html`, no other `update_styles`, no moves, no renames beyond the artboard.

## 5. Review

If a screenshot comes back empty, ask the user to switch to the `Output` page in Paper and try again (`open_file` cannot switch pages on a file that is already open).

For every artboard:
1. `get_screenshot` of the whole artboard, then `scale: 2` on the kicker, the detail rows, the logo lockup and, on the OG, the booth badge.
2. Read every slot back with `get_node_info` and compare it character by character with the approved copy.
3. Run `../brand/references/review-checklist.md`. The checks that fail most often here: text wrapping past its line limit, the OG headline's second line running into the badge, a booth number clipped in the badge, a partner logo optically bigger or smaller than the Archy wordmark.
4. A failure you can fix within the slot rules (shorter copy, with approval): fix it and re-screenshot. A failure you cannot: report it, do not work around it.

## 6. Finish

Call `finish_working_on_nodes`. Tell the user:
- which artboards were created on `Output`, by name;
- the copy used in each;
- anything the review could not confirm.

Exports are the user's call. If asked, `export` each artboard as PNG at 1x (Paper saves to `~/Downloads`).
