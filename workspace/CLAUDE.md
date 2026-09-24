# Archy Workspace

This folder is where the Archy marketing team works with Claude and Paper. The rules, templates and skills come from the `archy` plugin; this file only covers setup.

## If the `archy` plugin is not installed yet

Walk the person through setup, one step at a time, in the language they write in. They are not technical: explain each step in plain words and do the work for them where you can.

1. **GitHub access.** The plugin lives in a private GitHub repository, so this Mac needs to be signed in to GitHub.
   - Check with `gh auth status`. If `gh` is missing, check `brew --version`; with Homebrew, run `brew install gh`. Without Homebrew, send them to https://cli.github.com to download the macOS installer, and wait until they confirm it is installed.
   - Open a terminal tab for them and run `gh auth login --hostname github.com --git-protocol https --web`, then `gh auth setup-git`. Tell them to copy the one-time code, press Enter, and approve in the browser with the GitHub account that has access to Archy's repository.
2. **Install the plugin.** Ask them to click **+** next to the prompt box, choose **Plugins → Add plugin**, find **archy** and install it. The Paper plugin installs with it.
3. **Check.** Ask them to open Paper Desktop with any file, then start a new session in this folder and say "What file is open in Paper?". If Claude answers with the file name, setup is done.

If a step fails, read the error, fix what you can, and otherwise tell them exactly what to send to Marketing & Design.

## Once it is installed

Nothing else is needed here. Ask for pieces in plain words; the plugin knows the brand and the templates.
