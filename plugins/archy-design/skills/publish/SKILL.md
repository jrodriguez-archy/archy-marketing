---
name: publish
description: Publish new learnings, brand rules, templates or skills to the team's archy-marketing repository and release new plugin versions. Use when a designer says "add this to the plugin", "publish this", "this is for the team", "update the rules", or has just prepared a template.
---

# Publish to the Archy plugins

The marketing team only receives what lands in the repository `jrodriguez-archy/archy-marketing`. Templates in the `Master - …` Paper files are live as soon as they are saved; their catalog entries, the brand rules and the skills are not.

## 1. Find the repository

Look for a local clone (commonly `~/Documents/Claude/archy-marketing`; `git -C <dir> remote get-url origin` must point to `jrodriguez-archy/archy-marketing`). If there is none, ask where to put it and `git clone https://github.com/jrodriguez-archy/archy-marketing.git` there. Then `git pull --ff-only`. Publishing needs write access to the repository with the designer's own GitHub account; if a push is refused, say so and stop.

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
| How designers work (preparing templates, exploring, exports) | `plugins/archy-design/skills/…` |
| A new kind of piece for marketing | a new skill in `plugins/archy/skills/` |

Read the target file first. Update the existing rule if there is one; never add a second copy.

## 3. Write it for the team

- **English**, neutral, imperative.
- **Nothing personal**: no names of who taught it or who asked, no chat-language preferences, no paths on anyone's machine.
- **No em dashes** (—): use a colon, comma, parentheses or a period.
- **Defaults with a fallback, not locks.** The system always delivers; only the brand non-negotiables, tokens, English on the canvas, untouched masters and "never invent facts" are absolute. Write "do X; when that does not fit, Y", never "stop if".
- One sentence of reason when it helps apply the rule.

## 4. Confirm

Show the designer a short summary of each change (file, one line) and the version bump for each plugin touched, in the language they write in. Wait for their OK.

## 5. Version and changelog

Each plugin has its own version, in its `.claude-plugin/plugin.json` **and** in its entry in `.claude-plugin/marketplace.json` (both must match):
- **patch**: a rule clarified or fixed, copy tweaks;
- **minor**: a new template, skill or tool;
- **major**: the slot convention changes.

Add a `## <plugin> X.Y.Z (YYYY-MM-DD)` section at the top of `CHANGELOG.md`, one line per change.

## 6. Check

```bash
cd <repo>
grep -rn "—" plugins CHANGELOG.md          # must be empty
grep -rn "/Users/" plugins                  # must be empty
CLAUDE_BIN=$(command -v claude || ls -d "$HOME/Library/Application Support/Claude/claude-code/"*/claude.app/Contents/MacOS/claude | tail -1)
"$CLAUDE_BIN" plugin validate .
for p in plugins/*/; do "$CLAUDE_BIN" plugin validate "$p"; done
```

Also search the changed files for the names of people. Fix anything before continuing.

## 7. Release

```bash
git add -A
git commit -m "<summary>"      # end with the Co-Authored-By line
git push
(cd plugins/<plugin> && "$CLAUDE_BIN" plugin tag --push)   # once per plugin whose version changed
```

The tag (`<plugin>--v<version>`) is what triggers everyone's auto-update. If `plugin tag` fails, `git tag "<plugin>--vX.Y.Z" && git push origin "<plugin>--vX.Y.Z"` does the same.

## 8. Report

The versions released, what changed, and that the team gets it on their next session (auto-update) or from **+ → Plugins → Manage plugins → Update**.
