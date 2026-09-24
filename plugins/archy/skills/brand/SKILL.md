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

**The templates and brand rules are the base, not a lock.** Start from the templates, respect the brand, and deliver. The agent adapts where the brief needs it, and may also propose new pieces inspired by the templates when asked. Marketing and Design keep the final say and can adjust anything afterwards.

## Always true

1. **Never touch a master.** `Master - …` files are the templates. Work in a copy (see *Where the work goes*).
2. **The brand rules hold**: the non-negotiables in `references/composition.md` (solid Rulers, wordmark colour, la mascota), tokens instead of hex, Onest + Inter for marketing type, Open Sans for any product UI.
3. **Everything on the canvas is in US English**: copy, layer names, artboard names. Talk to the user in whatever language they write in.
4. **Never invent facts.** Dates, booth numbers, names and prices come from the requester or an official source. When one does not exist, the piece goes without it (see *Missing information*).

## Defaults, and how far they bend

| Default | When the brief asks for more |
|---|---|
| The requester picked a template (named it, or has it selected in Paper: check `get_selection`) | Use it |
| The requester did not pick one | Choose **2 or 3 different templates** that suit the case and build one option from each, so they can compare and choose (see *Options* below) |
| Nothing in the catalog fits, or the requester wants something new | Build a proposal **inspired by** the templates: same grid, type scale, Rulers and colour logic. Say it is an exploration |
| Change the slots first | Adjust anything else the piece needs: rewrap, resize, reduce display type, move or remove a block |
| Copy fits as given | Rewrap first, then reduce the type a little, then shorten, keeping the requester's wording |
| Every fact is provided | See *Missing information* below |
| Every image is provided | See *Photos* below |

**Report what you did**: what the piece started from, anything changed beyond the slots, what was removed or generated, and anything still to fill.

## Missing information

1. **Ask once** for everything the template shows (event, city, venue, dates, booth, speaker, partner...).
2. **If a fact does not exist** (no booth number, no venue yet, no time), remove that block from the piece: the value **and its label** (`Booth` and `#1234` go together), or the whole `optional-*` block. Let the layout close up so the piece does not look like something is missing.
3. **If it exists but the requester does not have it yet**, use a visible placeholder (`[Booth #]`) and list it as pending.
4. The partner logo follows its own recipe (`references/templates.md`, *Partner logo*).

## Photos

Only two kinds of photo live in the templates: **speaker portraits** and **city photos** (the city bands of `Booth Invite Photo`, `Booth Invite Offer`, `Booth Photo Band`). Every other template runs on its flat Archy ground; do not add photos or background art to it.

- **Speaker portrait:** always from the requester or the speaker. Never generate a photo of a real person. If there is none yet, keep the portrait frame with a placeholder and list it as pending.
- **City photo:** the requester's photo first. Otherwise a natural, well-lit photo of the host city (a recognisable skyline or landmark), with no filter or colour treatment: generate it with Paper's image generation (`paper-gen://google-nano-banana-2`, tell the requester it uses their Paper generation credits), check it on the screenshot, and say it was generated. Generate once on the Post and reuse the resulting image URL (read it with `get_computed_styles`) on Stories and OG.
- **If there is no usable photo**, remove the photo band and let the ground close the gap.

## Options

When the requester has not chosen a template, give them a choice instead of a single answer:

- Pick 2 or 3 templates that genuinely suit the content: what the piece announces (booth, talk, reminder), how much copy there is, whether there is a photo or a speaker. Prefer options that differ from each other (ground, composition, where the image sits) over near-duplicates, and do not default to the same template every time.
- Build **one format per option** (the Post, unless the brief names another), with the real copy, side by side, named `<Campaign> · Option A · <Template>`.
- Show them with one line each on why it suits the case. When the requester chooses, build the remaining formats from that option only, and delete the others unless they want to keep them.

## Where the work goes

Never in the master file. Either:
- **a file the user names** (their own working file), or
- **a new copy of the master file**: `create_file` with `cloneFileId` = the master's id and a name like `<Campaign> · Events`, then delete the templates that are not used in that copy.

If a copy cannot be made, ask the user to duplicate the master file in Paper (right-click the file, Duplicate) and open it.

## Workflow

1. **Read the brief** and pick the starting template from `references/templates.md`, or 2 or 3 of them as options.
2. **Make or open the working copy** (above). Ask once for missing facts; continue with placeholders if they are not available yet.
3. **Fill and adapt.** Slots first, then whatever else the piece needs.
4. **Review.** Screenshot every artboard and run `references/review-checklist.md`. Fix what fails.
5. **Deliver.** Call `finish_working_on_nodes` and report as above.

## References: read on demand

| File | Read it when |
|---|---|
| `references/templates.md` | Choosing a template, and the slots of each one |
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
| Screenshots come back empty | Paper sometimes only renders the page on screen, or the file's renderer is stuck | Carry on and review with `get_node_info` / `get_computed_styles`; mention that the user can open that page (or close and reopen the file) for a visual check |
| Tools stop responding | Connection dropped | Restart Paper Desktop, then start a new session |
| An export does not appear where expected | Paper always exports to `~/Downloads` | Look in Downloads |
