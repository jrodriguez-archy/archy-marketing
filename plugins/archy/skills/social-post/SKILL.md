---
name: social-post
description: Create Archy event social pieces in Paper (Post 1080×1350, Stories 1080×1920, OG link preview 1200×630, Square 1080×1080, event page cover 1200×900), based on the Master - Events templates. Use when someone needs social art for a trade show, dental meeting, booth invite, speaker event, a night out or dinner Archy hosts, a day-before reminder, or an event page cover, or wants to explore a new event piece in the Archy style.
---

# Archy event social

Load the `brand` skill first and follow it: never touch the master, keep the brand rules, start from the templates, deliver, report.

**Templates:** `Master - Events` (file id `01M1F9VXX1S3JJETTVWG2H2PCD`). The catalog and each template's slots are in `../brand/references/templates.md`; the three-format family (how Post, Stories and OG relate) is in `../brand/references/composition.md`.

## Steps

1. **Pick the template.** If the requester named one or has it selected in Paper, use it. Otherwise choose 2 or 3 different templates that suit the case and build a Post from each as options (see *Options* in the `brand` skill); build Stories, OG and Square once they choose. If they want something new, propose a piece inspired by the templates and say it is an exploration.
2. **Make the working copy** as the `brand` skill describes (the user's file, or a clone of `Master - Events` named after the event). Keep only the artboards you use.
3. **Get the facts and images**: event name and year, city and state, venue, dates (and time for a hosted evening), booth number, partner logo, the sign-up link or call to action, photos, formats (default: all the template has, plus the event page cover when there is an event page). Ask once. A fact that does not exist is removed with its label; one that is only pending gets a placeholder. Photos follow *Photos* in the `brand` skill. Apply the mechanics in `../brand/references/voice.md`.
4. **Fill and adapt** each format. Slots first; then make it fit (rewrap, reduce the type a little, shorten) and handle the partner logo as the catalog's *Partner logo* section describes. On the OG and Square headlines, set the line break yourself.
   **Event page cover** (`Event Cover`, 1200×900, the Webflow CMS thumbnail): start from the cover in the same row (and theme) as the chosen template. Make its ground from a photo of the host city or the venue with the `archy-design:pixel` tool (`effect tone <photo> --gradient <royal-blue | navy | ice --invert> --size 1200x900`, matching the template's ground), set it on `slot-image-venue`, then fill the headline and the one content block (booth, speaker, or photo + text). The Pixel Tone is the whole ground: add no gradient or scrim on top. The cover never repeats the city, venue, date or time: the page carries them.
5. **Review** every artboard with a screenshot, plus a close look at the booth badge and the logo lockup, and run `../brand/references/review-checklist.md`. Watch for: a headline running one line too long, anything leaving the cover's white card, the OG headline touching the badge, a clipped booth number, a partner logo that looks bigger or smaller than the Archy wordmark.
6. **Deliver**: the file and artboards created, what they started from, the copy used, anything adjusted beyond the slots, and placeholders still to fill.

Exports are the user's call; if asked, export PNG at 1x (Paper saves to `~/Downloads`).
