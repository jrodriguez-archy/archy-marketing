# Archy Marketing with Claude and Paper

Make on-brand Archy pieces (event social, ads, slides, and more) by asking Claude in plain words. Claude works directly in **Paper**, starting from the approved templates and following the Archy brand rules. You review the result and adjust anything you like.

The same setup covers **DOC** (Dental Ownership Collective) and the **Archy Offsite** identity. Each keeps its own look.

---

## What you need

| | |
|---|---|
| **Paper Desktop** | The Paper app installed and signed in to the Archy team |
| **Claude desktop app** | With the **Code** tab |
| **The Archy Workspace folder** | The `workspace` folder from this repository (see step 1) |

---

## One-time setup (about 5 minutes)

### 1. Get the workspace folder

Either get it from Marketing & Design, or open [github.com/jrodriguez-archy/archy-marketing](https://github.com/jrodriguez-archy/archy-marketing), click **Code → Download ZIP**, unzip it, and keep the `workspace` folder. Put it somewhere easy, for example `Documents/Archy Workspace`.

### 2. Open it in Claude

In the Claude desktop app, open the **Code** tab and start a new **local** session in the `Archy Workspace` folder. When Claude asks whether you trust the folder, say **yes**. That connects Claude to the Archy plugin catalog.

### 3. Let Claude set you up

Type:

> Set me up for Archy.

Claude will walk you through installing the **archy** plugin from **+ → Plugins → Add plugin**. The Paper plugin installs with it.

### 4. Check it works

Open Paper Desktop with any file. Start a new session in the workspace folder and ask:

> What file is open in Paper?

If Claude answers with the file's name, you are ready.

---

## Making a piece

Open Paper Desktop, start a session in the workspace folder, and describe what you need. Some examples:

> We have booth #2215 at Yankee Dental Congress 2027, Boston, MA, Boston Convention & Exhibition Center, January 28 – 30. Make the social posts.

> I need three options for a speaker event in Denver on February 24, 6:00 pm, at Left Hand Brewing Company.

> Redesign the slides in the "Q3 Review" folder in the Archy deck system.

What to expect:

- **Claude never touches the master templates.** It works in a copy: a file you name, or a new file named after your campaign.
- **If you do not pick a template, you get 2 or 3 options** to choose from. It then builds the other formats of the one you choose.
- **Missing information does not stop it.** It leaves a clear placeholder (`[Booth #]`, a `PARTNER LOGO` box) and tells you what to fill in.
- **It adapts the templates to your content** (a long event name, a missing venue) and tells you everything it adjusted.
- **You can ask for something new.** Say it is an exploration and Claude will propose a piece inspired by the templates, still on brand.
- **At the end it lists** the artboards it made, the copy it used, what it adjusted and what is still pending.

Tips:

- Give the real facts: event name, city, venue, dates, booth, partner. Claude never invents them.
- If you have the partner's logo, say where the file is, or drop it into the logo space in Paper afterwards.
- To pick a template yourself, select it in Paper before asking, or name it.
- Exports are up to you. Ask "export these as PNG" and Paper saves them to your **Downloads** folder.

---

## Updates

The plugin updates itself in the background when a new version is published; Claude may ask you to reload once it has. Templates live in Paper, so changes to them reach you as soon as they are saved.

To force an update: **+ → Plugins → Manage plugins**, then update **Archy - Marketing** (and **Archy - Design** if you have it).

### When the update button is greyed out

Sometimes Claude keeps an old copy of the plugin list and believes you are already up to date, so auto-update does nothing and the **Update** button stays disabled, even after turning auto-update off and on. Refresh it from the Terminal:

```bash
claude plugin marketplace update archy-marketing
claude plugin update archy@archy-marketing
claude plugin update archy-design@archy-marketing   # only if you have Archy - Design
```

Then quit Claude completely (Cmd+Q) and open it again. **+ → Plugins → Manage plugins** should now show the latest version.

---

## Troubleshooting

| What you see | What to do |
|---|---|
| Claude does not mention Paper or cannot see any file | Open **Paper Desktop** with a file. Paper only connects while the app is open with a file |
| Claude is working on the wrong file | Paper works on whichever file is in front. Switch to the right one, or tell Claude which file to use |
| No Paper tools at all, even with Paper open | You are in a **cloud** session. Start a **local** session in the workspace folder instead |
| Claude stops responding to Paper, or tools fail | Quit and reopen Paper Desktop, then start a new Claude session |
| Screenshots come back blank | Close the file in Paper and open it again |
| The `archy` skills do not appear | Check **+ → Plugins**: is **Archy - Marketing** installed and enabled? If it is not listed, repeat step 3 of the setup |
| An export is not where you expected | Paper always saves exports to **Downloads** |
| A new version was published but you do not get it, and **Update** is greyed out | See *When the update button is greyed out* under **Updates** |

Still stuck? Send Marketing & Design what you asked and a screenshot of the reply.

---

## What is inside (for the curious)

Two plugins live in this repository.

**`archy`**, for everyone:

| Skill | What it does |
|---|---|
| `brand` | Archy brand rules: colours, type, Rulers, the mascot, logos, voice, review checklist, template catalog |
| `social-post` | Event social: Post, Stories and OG link previews |
| `deck` | Slides from the Master - Decks library |
| `offsite-brand` | The Archy Offsite 2026 identity |

**`archy-design`**, for designers (it installs `archy` with it):

| Skill | What it does |
|---|---|
| `prepare-template` | Turn a finished design into a slot-ready template for marketing, and document it |
| `explore` | Design new pieces on brand, beyond the templates |
| `publish` | Add rules, templates or skills to this repository and release a new version |
| `slides-export` | Turn Paper slides into an editable Google Slides / PowerPoint file |
| `figma-export` | Publish a Paper artboard into Figma as editable layers |
| `print-pdf` | Turn a Paper PDF into a print-ready file |
| `hugeicons` | Bring Hugeicons into a Paper file |
| `pixel` | Pixel textures: gradient backgrounds (PNG, video loops, live Webflow) and pixel effects on photos |

Skills run on their own when your request matches; you can also call one directly, for example `/archy:social-post` or `/archy-design:prepare-template`.

### For designers

Follow the setup above, then also install **archy-design** from **+ → Plugins → Add plugin**. To publish changes you need write access to this repository with your own GitHub account; ask Marketing & Design. The export tools also need Node and Python on your Mac (the skills tell you what is missing).

---|---|
| `brand` | Archy brand rules: colours, type, Rulers, the mascot, logos, voice, review checklist |
| `social-post` | Event social: Post, Stories and OG link previews |
| `deck` | Slides from the Master - Decks library |
| `slides-export` | Turn Paper slides into an editable Google Slides / PowerPoint file |
| `figma-export` | Publish a Paper artboard into Figma as editable layers |
| `print-pdf` | Turn a Paper PDF into a print-ready file |
| `hugeicons` | Bring Hugeicons into a Paper file |
| `offsite-brand` | The Archy Offsite 2026 identity |

Skills run on their own when your request matches; you can also call one directly, for example `/archy:social-post`.

---

## Maintaining the plugin

- **Templates** live in the `Master - …` Paper files; edits there reach everyone as soon as they are saved.
- **Rules, catalog and skills** live here, under `plugins/archy/skills/`. After a change: bump `version` in `plugins/archy/.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`, add a line to `CHANGELOG.md`, commit and push, then run `claude plugin tag --push` from `plugins/archy/`. The tag (`archy--vX.Y.Z`) is what triggers everyone's auto-update.
- Versions: **patch** for a rule or copy fix, **minor** for a new template, skill or tool, **major** for a change to the slot convention.
- Setup for a new teammate only needs the `workspace` folder: its `.claude/settings.json` registers both marketplaces (`archy-marketing` and `paper`) with auto-update on. Both are needed; without the Paper marketplace the plugin cannot resolve its Paper dependency.

Maintained by Marketing & Design. Changes are listed in [CHANGELOG.md](CHANGELOG.md).
