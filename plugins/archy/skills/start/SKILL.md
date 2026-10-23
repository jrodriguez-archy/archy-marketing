---
name: start
description: Welcome and first steps for a designer new to the Archy plugin. Checks that Paper (and Satoshi, for DOC) is ready, lists what the plugin can do by area (brand and templates, decks, DOC, Offsite, product scenes, pixel textures, video, exports, business cards, publishing), shares the working rules that matter, and offers a first task. Use when someone says it is their first time, asks what they can do, how to start, how this works, what the plugin includes, or asks for help getting started.
---

# Getting started with Archy

The person is a designer on the Archy team. Answer in the language they write in, short and concrete. Do the checks yourself.

## 1. Check the setup

1. **Paper.** Call `get_basic_info`. If it answers, say which file is open. If Paper tools are missing or fail, ask them to open Paper Desktop, sign in to the Archy team, open any file, and start a new session; if it still fails, read the error and fix what you can.
2. **Satoshi, only if they mention DOC.** Follow step 0 of the `doc-brand` skill (check with `get_font_family_info`, offer to install). Skip it otherwise; do not install anything unprompted.

Keep this to one or two lines when everything works.

## 2. Say what the plugin does

A short menu by area, one line each, naming only what exists:

| Area | Skills |
|---|---|
| Brand rules (load before any piece) | `brand`, `doc-brand`, `offsite-brand` |
| Pieces from the templates | `social-post`, `ad`, `doc-ad`, `chrome-store` |
| Decks | `deck`, then `slides-export` for an editable `.pptx` |
| New designs and templates | `explore`, `prepare-template` |
| Product UI moments for marketing and video | `feature-scenes` |
| Textures and icons | `pixel` (Pixel Gradients and Pixel Effects), `hugeicons` |
| DOC video | `doc-video` (graphics in Paper), `doc-video-edit` (the full edit in Tesseract) |
| Out of Paper | `figma-export`, `print-pdf`, `business-card` |
| Sharing what was learned | `publish` (rules, templates and skills to the team's repository) |

Add one example request only if they ask for examples, and say it is an illustration, not a real event.

## 3. The rules that matter

Four at most:

- **Brand first.** Load the brand skill for the identity being worked on; Archy, DOC and Offsite never mix.
- **The masters stay untouched.** Work in a copy named after the campaign, or in a file they choose.
- **Never invent facts.** Anything missing becomes a visible placeholder to fill later.
- **Exports and publishing are their call.** Nothing is exported, pushed or released until they say so.

## 4. Offer a first task

End with one question: what do they want to work on first? When they answer, continue with the matching skill from the table.
