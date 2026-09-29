---
name: start
description: Welcome and first steps for someone new to the Archy plugin. Checks that Paper is connected, explains in plain words what they can ask for (Archy event social, ads, slides, DOC ads and video graphics, Offsite pieces, Chrome Store images), shares the few tips that matter, and offers to make a first piece together. Use when someone says it is their first time, asks what they can do, how to start, how this works, what to ask for, or asks for help getting started.
---

# Getting started with Archy

The person is usually not technical and may be using Claude and Paper for the first time. Answer in the language they write in, in plain words, short. Do the checks yourself; never ask them to run commands.

## 1. Check the setup

1. **Paper.** Call `get_basic_info`. If it answers, say which file is open. If Paper tools are missing or fail, ask them to open Paper Desktop, sign in to the Archy team, open any file, and start a new session; if it still fails, tell them to send the error to Marketing & Design.
2. **Satoshi, only if they mention DOC.** Follow step 0 of the `doc-brand` skill (check with `get_font_family_info`, offer to install). Skip it otherwise; do not install anything unprompted.

Keep this to one or two lines when everything works.

## 2. Say what they can ask for

Give a short menu with one real example each. Name only what exists:

| They need | Example request | Skill |
|---|---|---|
| Event social (Post, Stories, link preview) | "We have booth #1234 at the Chicago Midwinter Meeting, Feb 19 to 21. Make the social posts." | `social-post` |
| Archy ads, spotlights, one-pagers | "Make a spotlight ad for our AE at the Denver event." | `ad` |
| Slides in the Archy deck system | "Turn these notes into three slides." | `deck` |
| DOC ads | "A DOC ad for the next Foundations course, square and story." | `doc-ad` |
| DOC course video graphics | "A lower third and a title card for the F3 video." | `doc-video` |
| Archy Offsite pieces | "A daily agenda poster for day 2 of the Offsite." | `offsite-brand` |
| Chrome Web Store images | "Update the store images for the Portal Manager extension." | `chrome-store` |

The examples above are illustrations of the kind of request, not real events: say so if they ask, and never reuse their facts in a piece.

If `archy-design` is installed, add one line: designers can also explore new designs, prepare templates, and export to Google Slides, Figma or print.

## 3. The tips that matter

Four at most:

- **Give the real facts** (event, city, venue, dates, booth, partner). Claude never invents them; anything missing becomes a visible placeholder to fill later.
- **The masters stay untouched.** Claude works in a copy named after the campaign, or in a file they choose.
- **No template picked? They get 2 or 3 options** to compare, then the other formats of the one they choose.
- **Exports are their call.** "Export these as PNG" saves them to their Downloads folder.

## 4. Offer a first piece

End with one question: what do they want to make first? If they have nothing real yet, offer to walk through a practice piece with placeholders in a new file, never in a master. When they answer, continue with the matching skill from the table.
