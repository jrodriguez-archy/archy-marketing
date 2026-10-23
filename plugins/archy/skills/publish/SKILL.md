---
name: publish
description: Publish new learnings, brand rules, templates or skills to the team's archy-marketing repository and release a new version of the archy plugin. Use when a designer says "add this to the plugin", "publish this", "this is for the team", "update the rules", or has just prepared a template.
---

# Publish to the Archy plugin

The other designers only receive what lands in the repository `jrodriguez-archy/archy-marketing`. Templates in the `Master - …` Paper files are live as soon as they are saved; their catalog entries, the brand rules and the skills are not.

## 1. Find the repository

Look for a local clone (any folder whose `git -C <dir> remote get-url origin` points to `jrodriguez-archy/archy-marketing`; the person's own notes may say where it is). If there is none, ask where to put it and `git clone https://github.com/jrodriguez-archy/archy-marketing.git` there. Then `git pull --ff-only`. Publishing needs write access to the repository with the designer's own GitHub account; if a push is refused, say so and stop.

## 2. Decide where it goes

| What was learned | Where |
|---|---|
| Colour, token, font, icon | `plugins/archy/skills/brand/references/tokens.md` |
| Layout, Rulers, the mascot, logos, scale | `.../brand/references/composition.md` |
| Copy, tone, formats (dates, cities) | `.../brand/references/voice.md` |
| Something to check before delivering | `.../brand/references/review-checklist.md` |
| How Paper's tools behave | `.../brand/references/paper-quirks.md` |
| A template prepared | `.../brand/references/templates.md` (row in *At a glance* + its section) |
| Slides | `plugins/archy/skills/deck/references/…` |
| DOC or Offsite identity | `plugins/archy/skills/doc-brand/…`, `…/offsite-brand/…` |
| How designers work (preparing templates, exploring, exports, video) | the matching skill in `plugins/archy/skills/…` |
| A new kind of piece or workflow | a new skill in `plugins/archy/skills/` (and a line in the `start` skill's menu) |

Read the target file first. Update the existing rule if there is one; never add a second copy.

## 3. Write it for the team

- **English**, neutral, imperative.
- **Nothing personal**: no names of who taught it or who asked, no chat-language preferences, no paths on anyone's machine.
- **No em dashes** (—): use a colon, comma, parentheses or a period.
- **Defaults with a fallback, not locks.** The system always delivers; only the brand non-negotiables, tokens, English on the canvas, untouched masters and "never invent facts" are absolute. Write "do X; when that does not fit, Y", never "stop if".
- One sentence of reason when it helps apply the rule.

## 4. Confirm

Show the designer a short summary of each change (file, one line) and the version bump, in the language they write in. Wait for their OK.

## 5. Version and changelog

The plugin's version lives in `plugins/archy/.claude-plugin/plugin.json` **and** in its entry in `.claude-plugin/marketplace.json` (both must match):
- **patch**: a rule clarified or fixed, copy tweaks;
- **minor**: a new template, skill or tool;
- **major**: the slot convention changes.

Add a `## archy X.Y.Z (YYYY-MM-DD)` section at the top of `CHANGELOG.md`, one line per change.

## 6. Check

```bash
cd <repo>
grep -rn "—" plugins CHANGELOG.md | grep -v "skills/publish/SKILL.md"   # must be empty
grep -rn "/Users/" plugins | grep -v "skills/publish/SKILL.md"           # must be empty
CLAUDE_BIN=$(command -v claude || ls -d "$HOME/Library/Application Support/Claude/claude-code/"*/*/claude.app/Contents/MacOS/claude | tail -1)
"$CLAUDE_BIN" plugin validate .
"$CLAUDE_BIN" plugin validate plugins/archy
```

Also search the changed files for the names of people. Fix anything before continuing.

## 7. Release

```bash
git status                     # changes from other sessions stay out: mention them, do not commit them
git add <the files changed for this publish>
git commit -m "<summary>"      # end with the Co-Authored-By line
git push
(cd plugins/archy && "$CLAUDE_BIN" plugin tag --push)
```

The tag (`archy--v<version>`) marks the release. If `plugin tag` fails, `git tag "archy--vX.Y.Z" && git push origin "archy--vX.Y.Z"` does the same.

## 8. Report

The version released, what changed, and that the other designers get it on their next session (auto-update) or from **+ → Plugins → Manage plugins → Update**.
