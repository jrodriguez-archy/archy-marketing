---
name: doc-brand
description: DOC (Dental Ownership Collective) brand rules for any work in Paper. Load before creating, filling, reviewing or exporting any DOC piece (ads, and any other DOC asset), or anything in the `DOC - Brand` or `DOC - Ads` Paper files. DOC is its own identity, separate from Archy and from the Archy Offsite.
---

# DOC brand

**DOC, the Dental Ownership Collective**, is the ownership education platform for dentists who want their own practice. It is a brand of its own: Archy appears on it only as a sponsor ("Sponsored by Archy", "Brought to you by Archy"). Production skills for DOC (`doc-ad`) load this first.

## Separation, both ways

- **Never apply the Archy system here:** no Archy tokens (`--color-royal-blue-500` and the rest), no Onest or Inter, no Rulers, no mascot, no Archy 12px radius cap, no Archy type scale. Do not "correct" a DOC piece toward Archy.
- **Never apply DOC to Archy or Offsite work.** Satoshi, the cream and red ramps, the track colours and the DOC lockup belong to DOC only.

## How this system works

The guidelines and templates are the base, not a lock. Start from the templates, respect the brand, deliver. Numbers such as gaps, leading and which tracking token a headline takes are judgements made per piece against the content in front of you; the tokens, the type family, the colour logic and the lockup are the system. Marketing and Design keep the final say.

## Always true

1. **Never touch a master.** `DOC - Ads` is the master for ads and `DOC - Brand` holds the guidelines. Work in a copy (see *Where the work goes*).
2. **Tokens, never hex.** Every colour, weight, tracking, spacing and radius on the canvas is a `var(--…)` from the file. If a value is missing, flag it and ask for a token rather than typing a hex or a hand number (tokens: `references/tokens.md`).
3. **Satoshi only**, Regular 400 as the lightest weight on DOC pieces (details in `references/identity.md`).
4. **The lockup is outlined artwork**, copied from the file, never re-typed, redrawn or recoloured beyond its documented colourways.
5. **Everything on the canvas is in US English**: copy, layer names, artboard names. Talk to the user in whatever language they write in.
6. **Never invent facts.** Prices, module counts, dates, stats, names and quotes come from the requester or an official DOC source. Where a specimen figure is used as a placeholder, say so and list it as pending. Never put a real person's name or photo on a piece unless the requester supplies it.

## Sources of truth, in order

1. **The live site, `dentalownership.com`**: the real CSS tokens and Satoshi in use. The authority for colour and type.
2. **The `DOC - Brand` Paper file** (`app.paper.design/file/01M265WH7R1CNVXVP5CB4BZKM7`): tokens mirrored from the site, and the guideline artboards.
3. **The DOC brand guidelines PDF** (9 pages, fully outlined): the logo and colourway reference.
4. **Reference screenshots of social pieces**: composition only. They are recompressed, so never derive a colour from them.

Two traps:
- A file named `logo-doc.svg` circulating with the brand sources is the **Dental Ownership Academy** wordmark, not Collective. Use the lockup in the Paper files (the site's `doc-logo.svg`, viewBox `0 0 132 48`, 26 paths).
- The site's Webflow CSS carries leftover template defaults (`--base-color-brand--blue #2D62FF`, `--base-color-brand--pink #DD23BB`, a `system--error / success / warning` set). They are **not** DOC colours.

If a token in a Paper file and the site disagree, flag it rather than picking one.

## Where the work goes

Never in the master file. Either:
- **a file the user names**, or
- **a new copy of the master**: `create_file` with `cloneFileId` = the master's id and a name like `<Campaign> · DOC Ads`, then delete the artboards that are not used in that copy.

If a copy cannot be made, ask the user to duplicate the file in Paper (right-click the file, Duplicate) and open it.

## Workflow

0. **Check the font first.** Call `get_font_family_info` with `Satoshi`. Satoshi is not on Google Fonts, so Paper only has it when it is installed on this Mac; when it is missing Paper silently renders every DOC text node in the system sans, and every screenshot, measurement and fit is wrong while the file itself still says Satoshi. An empty result means it is missing, even when the file lists Satoshi among its fonts.

   **If it is missing, install it before designing:**
   1. Tell the user Satoshi is needed, and ask before installing.
   2. Run `"${CLAUDE_PLUGIN_ROOT}/tools/fonts/install-satoshi.sh"`. It downloads the official package from Fontshare, copies the OTF weights into `~/Library/Fonts` and clears macOS's quarantine flag (a downloaded font that keeps the flag may not load).
   3. If the script cannot install it, it prints the manual steps: pass them on (open `fontshare.com/fonts/satoshi`, *Download family*, unzip, select every `.otf` in `Fonts/OTF`, double-click, *Install*).
   4. Ask the user to quit Paper completely (Cmd+Q) and open it again, then check with `get_font_family_info` once more. Only start designing when it answers.

   **Never commit the font files to this repository or send them to anyone.** Satoshi's licence (ITF Free Font License) allows installing it on the team's own machines, but not redistributing it through a repository, a public server or to outside agencies; each person gets it from Fontshare.
1. **Read the brief** and pick the starting layout (the production skill's catalog), or 2 or 3 of them as options when none was named.
2. **Make or open the working copy.** Ask once for missing facts; continue with visible placeholders when they are not available yet.
3. **Fill and adapt.** Copy first, then everything the piece needs: re-break the headline so the weight change lands on a line end, re-size type to the new copy, keep the lockup ladder.
4. **Review.** Screenshot every artboard and run `references/review-checklist.md`. Fix what fails.
5. **Deliver.** Call `finish_working_on_nodes` and report: what the piece started from, the copy used, anything changed beyond the copy, and what is still pending.

## References: read on demand

| File | Read it when |
|---|---|
| `references/tokens.md` | Checking a colour, ground, weight, tracking, spacing or radius token |
| `references/identity.md` | The lockup, colourways, grounds and themes, track coding, type and the two-weight headline |
| `references/voice.md` | Writing or shortening copy, choosing a CTA |
| `references/review-checklist.md` | Step 4, every time |
| `../brand/references/paper-quirks.md` | Before your first Paper write in a session, and whenever a Paper tool result looks wrong. It is about Paper, not about Archy, and applies here unchanged |

## Troubleshooting

| Symptom | Cause | What to tell the user |
|---|---|---|
| No Paper tools available | Paper Desktop closed, no file open, or a cloud session | Open Paper Desktop with a file, and use a **local** session in the Claude app |
| The wrong file is open | Paper works on whichever file is active | Open the right one with `open_file`; if that fails, ask the user to switch to it |
| Screenshots come back empty | Paper only renders the page on screen, or the file's renderer is stuck | Review with `get_node_info` / `get_computed_styles`; the user can open that page, or close and reopen the file, for a visual check |
| An export does not appear where expected | Paper always exports to `~/Downloads` | Look in Downloads |
