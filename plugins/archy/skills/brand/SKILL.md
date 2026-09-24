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
| **Archy** | this one | `Brand`, `Master - Events`, `Archy - Ads`, `Master - Decks`, `Archy - Various Collateral` |
| **DOC** (Dental Ownership Collective) | `doc-brand` | `DOC - Brand`, `DOC - Ads` |
| **Archy Offsite 2026** | `offsite-brand` | `Archy Offsite - 2026` |

If the request does not say which one, infer it from the event, file or context; ask only when it is genuinely unclear. Never apply one identity's tokens, type, logo or mascot to another.

## How this system works

**The templates and rules are the base, not a lock.** The agent always delivers a piece. It starts from the closest template, follows the brand rules, adapts where the brief needs it, and leaves anything it could not resolve clearly marked for the requester or a designer to finish. Marketing and Design keep the final say: they can adjust any piece afterwards.

## Always true

These hold on every piece. Everything else is a default that can bend.

1. **Brand non-negotiables** in `references/composition.md` (solid Rulers, wordmark colour, la mascota's rules).
2. **Tokens, never hex.** Colours go through `var(--color-…)`.
3. **Everything on the canvas is in US English**: copy, layer names, artboard names. Talk to the user in whatever language they write in.
4. **Masters stay untouched.** Work on a duplicate on the `Output` page, never on `Templates`.
5. **Never invent facts.** A missing date, booth number, name or logo becomes a visible placeholder (see below), never a made-up value.
6. **Product UI is Open Sans.** Any mockup of the Archy app inside a marketing piece stays Open Sans; marketing type is Onest + Inter.

## Defaults, and how far they bend

| Default | When the brief does not fit it |
|---|---|
| Start from the best-fitting **ready** template | If the best fit is not prepared yet, duplicate its campaign from `Archive` (or the closest ready template) and adapt it. Say which one you used |
| Change the **slots** first | Go beyond them when the piece needs it: resize or rewrap a text box, reduce display type, adjust a gap, hide or remove a block, reposition an element. Stay inside the safe area and the brand rules |
| Copy fits the slot as given | First rewrap (move the line break). Then reduce the type size in small steps, never below about 75% of the template's size and never below the scale's floors. Only then propose a shorter version. Keep the requester's wording wherever possible |
| Every fact is provided | Use a placeholder and keep going: `[Booth #]`, `[Venue]`, `[Date]` in the slot, or a logo placeholder (see `references/templates.md`, *Missing partner logo*) |

**Report every adjustment.** At the end, list what was changed beyond the slots and every placeholder left in the piece, so the requester knows exactly what to check or complete.

## Workflow

1. **Open the right file.** Call `get_basic_info`. If the open file is not the one the catalog names for this kind of piece, open it with `open_file` (the file ids are in `references/templates.md`). If that fails, ask the user to open it in Paper Desktop.
2. **Pick the starting point** from `references/templates.md`: a ready template, or the closest `Archive` campaign.
3. **Collect the brief.** Ask once for missing facts. If the user does not have them yet, go ahead with placeholders.
4. **Duplicate** onto the `Output` page, rename it, set `translate: none` and an integer `left`/`top`.
5. **Fill and adapt.** Slots first; adjust beyond them where needed (see *Defaults*).
6. **Review.** Screenshot every artboard and run `references/review-checklist.md`. Fix what fails.
7. **Deliver.** Call `finish_working_on_nodes`. Report what was created and where, the copy used, every adjustment beyond the slots, and every placeholder still to fill.

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
| The wrong file is open | Paper works on whichever file is active | Open the right one with `open_file`; if that fails, ask the user to switch to it |
| Screenshots come back empty | Paper sometimes only renders the page on screen, or the file's renderer is stuck | Carry on and review with `get_node_info` / `get_computed_styles`; mention that the user can open the `Output` page (or close and reopen the file) for a visual check |
| Tools stop responding | Connection dropped | Restart Paper Desktop, then start a new session |
| An export does not appear where expected | Paper always exports to `~/Downloads` | Look in Downloads |
