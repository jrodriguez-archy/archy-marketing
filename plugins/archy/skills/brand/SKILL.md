---
name: brand
description: Archy brand rules for any work in Paper. Load before creating, filling, reviewing or exporting any Archy piece (social post, ad, event asset, slide, Chrome Store image). Not for DOC (Dental Ownership Collective) or the Archy Offsite 2026 identity, which have their own brand skills.
---

# Archy brand

The base rules every Archy skill follows. Production skills (`social-post`, `ad`, `deck`, `chrome-store`) load this first.

## Which brand is this?

Three identities live in this plugin and they never mix:

| Identity | Skill | Paper files |
|---|---|---|
| **Archy** | this one | `Brand`, `Small Events - 2026`, `Archy - Ads`, `Master - Decks`, `Archy - Various Collateral` |
| **DOC** (Dental Ownership Collective) | `doc-brand` | `DOC - Brand`, `DOC - Ads` |
| **Archy Offsite 2026** | `offsite-brand` | `Archy Offsite - 2026` |

If the request does not say which one, ask. Never apply one identity's tokens, type, logo or mascot to another.

## Hard rules

1. **Never create from scratch.** Every piece starts as a duplicate of a master artboard from the template catalog (`references/templates.md`). If no template fits, stop and say so. Do not improvise a layout.
2. **Only slots change.** Edit only layers named `slot-*`, `optional-*` or `variant-*`, and only in the ways the catalog allows. Everything else is locked.
3. **Only `ready` templates.** A template marked `not prepared` cannot be used yet. Stop and name it.
4. **Everything on the canvas is in US English**: copy, layer names, artboard names. Talk to the user in whatever language they write in.
5. **Tokens, never hex.** Colours go through `var(--color-…)`.
6. **Never shrink type to fit copy.** Shorten the copy and get the requester's approval.
7. **Never invent facts.** Dates, booth numbers, names and prices come from the requester.
8. **Product UI is Open Sans.** Any mockup of the Archy app inside a marketing piece stays Open Sans; marketing type is Onest + Inter.

## Base values, not a straitjacket

The numbers and layouts in these references are the documented base. A particular piece can need an adjustment the base does not cover, and that is normal: it does not have to become a new rule, and it does not change the base for the next piece. The exception is anything listed under *Non-negotiables* in `references/composition.md`, which always holds.

As the agent, stay inside the slots. When a piece seems to need something beyond them, describe the adjustment and why, and apply it only if the requester approves, to that piece only.

## Workflow

1. **Preflight.** Call `get_basic_info` without a `fileId`. Confirm the open file is the one the catalog names for this template and that it has `Templates` and `Output` pages. If not, tell the user exactly which file to open in Paper Desktop and stop. See *Troubleshooting* below.
2. **Pick the template** from `references/templates.md`. Check its status.
3. **Collect the brief.** Ask for every fact the template's slots need. Check each string against the slot's limit.
4. **Duplicate** the master into the `Output` page, rename it, set `translate: none` and an integer `left`/`top`.
5. **Fill the slots.** Delete empty `optional-*` blocks. Pick `variant-*`s.
6. **Review.** Screenshot every artboard and run `references/review-checklist.md`. Fix what fails, within the slot rules.
7. **Finish.** Call `finish_working_on_nodes`. Report what was created, where, and anything the checklist could not verify.

## References: read on demand

| File | Read it when |
|---|---|
| `references/templates.md` | Choosing a template, or before editing any layer |
| `references/tokens.md` | Checking a colour, ground, font or icon, or finding which Paper file holds what |
| `references/composition.md` | Anything about Rulers, la mascota, logo lockups, the booth badge, BK Fade, scale or the three-format family |
| `references/voice.md` | Writing or shortening copy |
| `references/review-checklist.md` | Step 6, every time |
| `references/paper-quirks.md` | Before your first Paper write in a session, and whenever a Paper tool result looks wrong |

## Troubleshooting

| Symptom | Cause | What to tell the user |
|---|---|---|
| No Paper tools available | Paper Desktop closed, no file open, or a cloud session | Open Paper Desktop with a file, and use a **local** session in the Claude app |
| Preflight shows the wrong file | Paper works on whichever file is active | Switch to the right file in Paper, then ask again |
| Screenshots come back empty, sizes read 0 | The file's renderer is stuck | Close the file in Paper and reopen it |
| Tools stop responding | Connection dropped | Restart Paper Desktop, then start a new session |
| An export does not appear where expected | Paper always exports to `~/Downloads` | Look in Downloads |
