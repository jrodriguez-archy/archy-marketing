---
name: social-post
description: Create Archy event social posts in Paper (Instagram/LinkedIn Post 1080×1350, Stories 1080×1920, OG link preview 1200×630) from the Events templates. Use when someone needs social art for a trade show, dental meeting, booth invite, speaker event or day-before reminder.
---

# Archy event social posts

Load the `brand` skill first. Its *Always true* list holds without exception; everything else is a default that bends to the brief. The job is to **always deliver the pieces**, adapted to the content, with anything unresolved marked for the requester.

**Paper file:** `Master - Events` (the Events template file, `01M1F9VXX1S3JJETTVWG2H2PCD`). Masters on `Templates`, work on `Output`, partner logos on `Assets`, past campaigns on `Archive`.

## 1. Open the file

`get_basic_info`. Identify the file by its id (`01M1F9VXX1S3JJETTVWG2H2PCD`), not its name, which may change. If it is not the open file, `open_file` it. Read `../brand/references/templates.md` (section *Master - Events*) and `../brand/references/paper-quirks.md` once per session.

## 2. Pick the starting point

Match the brief to the catalog's **Use when**.

- A **ready** template fits: use it.
- The best fit is **not prepared**: duplicate its campaign from `Archive` (the catalog's *Built from* column says which) and work on that copy. Tell the user it is not a prepared template yet, so a designer may want to check it.
- Nothing fits well: take the closest one and adapt it, and say what you adapted.

## 3. Collect the brief

Ask once, in one message, for what is missing: event name and year, city and state, venue, dates, booth number, partner logo, formats (default: all three). If the user does not have something yet, continue with a placeholder (`[Booth #]`, `[Venue]`) and list it as pending.

Apply the mechanics in `../brand/references/voice.md` (date format, `City, ST`, `#` before the booth). Keep the requester's wording.

## 4. Build each format

For each format, Post, then Stories, then OG:

1. `duplicate_nodes` the master (or the `Archive` campaign) with `parentId: "root_node_<Output pageId>"`.
2. Rename it `<Event short name> <year> · <Format> <W×H>`, e.g. `Yankee Dental 2027 · Post 1080×1350`.
3. Place it: integer `left`/`top`, `translate: none`. One row per campaign: Post at `left: 0`, Stories at 1160, OG at 2320, `top` 80px below the tallest artboard already on `Output`.
4. Fill the slots with `set_text_content` in one batch, using the `descendantIdMap` to find them. On the OG headline set the line break with `\n`.
5. **Make it fit.** If a text overflows its limit or collides with something: rewrap it, then reduce its size in small steps (not below about 75% of the template's size), then use a shorter form the organiser uses themselves. Report what you did.
6. **Partner logo.** Follow *Missing partner logo* in `templates.md`: from `Assets` if it is there, otherwise the official logo from the organiser's site, otherwise a `placeholder-logo-partner`. Size it to the format's logo height and match the Archy wordmark optically.

## 5. Review

For every artboard:
1. `get_screenshot` of the whole artboard, then `scale: 2` on the kicker, the detail rows, the logo lockup and, on the OG, the booth badge. If screenshots come back empty (Paper sometimes only renders the page on screen), continue with the checks below and mention that a visual check is pending.
2. Read every slot back with `get_node_info` and compare it with the approved copy.
3. Run `../brand/references/review-checklist.md`. Typical problems here: a headline wrapping to one line too many, the OG headline running into the badge, a booth number clipped in the badge, a partner logo optically bigger or smaller than the Archy wordmark.
4. Fix what fails and re-check.

## 6. Deliver

Call `finish_working_on_nodes`. Tell the user:
- the artboards created on `Output`, by name, and what they started from;
- the copy used in each;
- every adjustment beyond the slots (sizes reduced, names shortened, blocks moved);
- every placeholder still to fill, and how (for a logo: drop the file into the `slot-logo-partner` frame).

Exports are the user's call. If asked, `export` each artboard as PNG at 1x (Paper saves to `~/Downloads`).
