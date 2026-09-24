# Changelog

All notable changes to the `archy` plugin. Versions follow semver:

- **Patch**: a copy fix or a rule clarified.
- **Minor**: a new template, skill or tool.
- **Major**: a change to the slot naming convention.

## 0.2.0 (2026-09-24)

- Master - Events: nine event templates, each with Post, Stories and OG: Booth Icon List, Booth Invite Photo, Booth Invite Offer, Booth Light Rulers, Booth Photo Band, Speaker Invite, Countdown Mascota, Countdown Offer, Countdown Masthead. Slots named, partner logo separated into its own slot, solid Rulers, pills and offer bars that grow with their text.
- Templates run on the flat Archy grounds; photos only for speaker portraits and untreated city photos. No background art.
- When no template is chosen, the agent builds 2 or 3 options (the Post of each) for the requester to pick.
- Missing facts: ask; if a fact does not exist, remove it together with its label; placeholders only for facts that are pending.
- Partner logos: requester's file, the official logo made one-colour when needed, or a placeholder; sized optically.
- Masters are never edited: work happens in the user's file or a clone of the master.
- Paper quirks: moving or duplicating vector elements into another SVG, recolouring SVG paths, fixed-width SVG pills.

## 0.1.0 (2026-09-24)

- First release.
- `brand`: Archy brand rules (tokens, composition, voice, review checklist, Paper quirks) and the template catalog. Flexible defaults: masters stay untouched, work happens in a copy, 2 or 3 template options when none is chosen, placeholders for missing facts and logos.
- `social-post`: event social pieces (Post, Stories, OG) from Master - Events. First template: `Booth Icon List`.
- `deck`: slides from the Master - Decks library, including redesigning an existing deck from its PPTX and PDF.
- `offsite-brand`: the Archy Offsite 2026 identity.
- `slides-export`, `figma-export`, `print-pdf`, `hugeicons`: tool skills (documentation; the tools themselves ship in a later version).
- Archy Workspace folder with the marketplaces pre-registered and auto-update on.
