# Archy - Design: the Archy plugin for designers

The **archy** plugin gives Claude the Archy brand system and the design team's workflows: brand rules for Archy, DOC and the Archy Offsite, the template catalogs, new explorations and templates, decks, product feature scenes, pixel textures, DOC course videos, and exports to Google Slides, Figma and print. Claude works directly in **Paper**.

The marketing team makes finished pieces from the templates with **Archy Studio**, not with this plugin.

---

## Install

You need **Paper Desktop** (signed in to the Archy team) and the **Claude desktop app** with the **Code** tab. In a local Claude Code session, run these one at a time:

```
/plugin marketplace add paper-design/agent-plugins
```

```
/plugin marketplace add jrodriguez-archy/archy-marketing
```

```
/plugin install archy@archy-marketing
```

The first line registers Paper's catalog (the plugin depends on its Paper plugin), the second registers the Archy catalog, and the third installs the plugin with Paper's included. Then open Paper Desktop with any file and ask Claude "What file is open in Paper?". If it answers with the file's name, you are ready.

**New here?** Ask Claude "It's my first time, what can I do?". The `start` skill checks your setup and shows what the plugin does.

**Working on DOC?** DOC uses Satoshi, which Paper does not include. The first time you ask for a DOC piece, Claude checks for it and, with your OK, installs it from Fontshare. Then quit Paper (Cmd+Q) and open it again.

The export tools also need Node and Python on your Mac; the skills say what is missing.

---

## What is inside

| Area | Skill | What it does |
|---|---|---|
| Brand | `brand` | Archy brand rules: colours, type, Rulers, the mascot, logos, voice, review checklist, template catalog |
| | `doc-brand` | DOC (Dental Ownership Collective): tokens, the lockup, themes, Satoshi, voice, review checklist |
| | `offsite-brand` | The Archy Offsite 2026 identity |
| Templates | `social-post` | Event social: Post, Stories, OG link preview, Square, event page cover |
| | `ad` | Archy ads: spotlights, one-pagers and their Posts, print ads |
| | `doc-ad` | DOC ads from the DOC - Ads master |
| | `chrome-store` | Chrome Web Store listing images for Archy extensions |
| Decks | `deck` | Slides from the Master - Decks library |
| | `slides-export` | Paper slides to an editable Google Slides / PowerPoint file |
| New work | `explore` | New pieces on brand, beyond the templates |
| | `prepare-template` | A finished design into a slot-ready template, documented in the catalog |
| | `feature-scenes` | Product UI "before / after" frames for marketing and video |
| Textures and icons | `pixel` | Pixel Gradients (PNG, video loops, live Webflow) and Pixel Effects on photos |
| | `hugeicons` | Hugeicons placed in Paper with the right style |
| DOC video | `doc-video` | DOC course video graphics from the Videos Foundations master |
| | `doc-video-edit` | A DOC course video edited end to end in Tesseract |
| Out of Paper | `figma-export` | A Paper artboard into Figma as editable layers |
| | `print-pdf` | A Paper PDF into a print-ready file |
| | `business-card` | Print-ready business cards, with a booking QR |
| Team | `publish` | Rules, templates or skills added to this repository, with a new release |
| | `start` | Welcome and setup check |

Skills run on their own when your request matches; you can also call one directly, for example `/archy:explore` or `/archy:pixel`.

How Claude works with the templates:

- **The masters stay untouched.** It works in a copy: a file you name, or a new one named after the campaign.
- **No template picked? You get 2 or 3 options**, then the other formats of the one you choose.
- **Missing facts never stop it**, and it never invents them: it leaves a visible placeholder and lists what is pending.
- **Exports and publishing are your call.** Paper saves exports to **Downloads**.

---

## Moving from Archy - Design / Archy - Marketing

Until version 0.20.0 this repository had two plugins: `archy` ("Archy - Marketing") and `archy-design` ("Archy - Design"). They are now one plugin, `archy`, shown as **Archy - Design**.

- **You do not need to do anything.** On your next sessions `archy` updates with every skill and `archy-design` is retired on its own. Work the design tools saved before (slide exports, venvs, the Figma import plugin) stays where it was and is linked into the new plugin automatically.
- The design skills are now called `/archy:...` (for example `/archy:pixel` instead of `/archy-design:pixel`).
- If the design skills are missing in the first session after the update, restart Claude, or run `claude plugin update archy@archy-marketing` in the Terminal.
- Run `claude plugin install archy@archy-marketing` once. Before, `archy` came in as a dependency of `archy-design`, so it may still be marked as installed automatically; installing it yourself keeps `claude plugin prune` from removing it.

---

## Updates

The plugin updates itself in the background when a new version is published; Claude may ask you to reload once it has. Templates live in Paper, so changes to them reach you as soon as they are saved.

To force an update: **+ → Plugins → Manage plugins**, then update **Archy - Design**.

### When the update button is greyed out

Sometimes Claude keeps an old copy of the plugin list and believes you are already up to date. Refresh it from the Terminal:

```bash
claude plugin marketplace update archy-marketing
claude plugin update archy@archy-marketing
```

Then quit Claude completely (Cmd+Q) and open it again.

---

## Troubleshooting

| What you see | What to do |
|---|---|
| Claude does not mention Paper or cannot see any file | Open **Paper Desktop** with a file. Paper only connects while the app is open with a file |
| Claude is working on the wrong file | Paper works on whichever file is in front. Switch to the right one, or tell Claude which file to use |
| No Paper tools at all, even with Paper open | You are in a **cloud** session. Start a **local** session instead |
| Claude stops responding to Paper, or tools fail | Quit and reopen Paper Desktop, then start a new Claude session |
| Screenshots come back blank | Close the file in Paper and open it again |
| The `archy` skills do not appear | Check **+ → Plugins**: is **Archy - Design** installed and enabled? If not, repeat the install |
| Installing fails because of the Paper dependency | Run `/plugin marketplace add paper-design/agent-plugins` first, then install again |
| A new version was published but you do not get it | See *When the update button is greyed out* |

---

## Maintaining the plugin

- **Templates** live in the `Master - …` Paper files; edits there reach everyone as soon as they are saved.
- **Rules, catalogs, skills and tools** live here, under `plugins/archy/`. The `publish` skill does the whole release: where each change goes, the version bump in `plugins/archy/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, the `CHANGELOG.md` entry, the checks, the commit, the push and the `archy--vX.Y.Z` tag.
- Versions: **patch** for a rule or copy fix, **minor** for a new template, skill or tool, **major** for a change to the slot convention.
- Publishing needs write access to this repository with your own GitHub account.

Changes are listed in [CHANGELOG.md](CHANGELOG.md).
