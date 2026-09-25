// Where this tool reads and writes, resolved once and shared by every script.
//
// The tool itself lives inside the plugin folder, which is replaced on every update, so
// nothing may ever be written next to the code. Everything a run produces or consumes
// (dump/, assets/, trees/, styles/, the output .pptx, node_modules) lives in a WORK
// directory instead:
//
//   --work=DIR (or --work DIR)       highest priority, stripped from process.argv
//   $ARCHY_WORK                      the project directory, e.g. $BASE/<project>
//   $BASE                            when neither is set
//
// BASE is $ARCHY_WORK_BASE, else ${CLAUDE_PLUGIN_DATA}/slides-export, else
// ./archy-work/slides-export. Shared dependencies (node_modules, .venv, the Hugeicons
// tarball) are installed once in BASE and found from any project under it.
//
// Code and generic lookups (tokens.json, assets-base/) resolve against HERE, the
// script's own directory.

const fs = require("fs");
const path = require("path");
const { createRequire } = require("module");

const TOOL = "slides-export";
const HERE = __dirname;

function takeWorkArg() {
  const argv = process.argv;
  for (let i = 2; i < argv.length; i++) {
    if (argv[i].startsWith("--work=")) {
      const v = argv[i].slice(7);
      argv.splice(i, 1);
      return v;
    }
    if (argv[i] === "--work" && i + 1 < argv.length) {
      const v = argv[i + 1];
      argv.splice(i, 2);
      return v;
    }
  }
  return null;
}

const BASE = path.resolve(
  process.env.ARCHY_WORK_BASE ||
  (process.env.CLAUDE_PLUGIN_DATA
    ? path.join(process.env.CLAUDE_PLUGIN_DATA, TOOL)
    : path.join(process.cwd(), "archy-work", TOOL))
);
const WORK = path.resolve(takeWorkArg() || process.env.ARCHY_WORK || BASE);

// An input path: absolute as given; relative tries the current directory first (so a
// path typed at the shell means what it says), then WORK.
function input(p) {
  if (path.isAbsolute(p)) return p;
  const here = path.resolve(p);
  return fs.existsSync(here) ? here : path.join(WORK, p);
}

// An output path: absolute as given; relative always lands in WORK, never beside the code.
function output(p) {
  return path.isAbsolute(p) ? p : path.join(WORK, p);
}

// An asset a spec names as "assets/…": the project's own copy in WORK wins, and the
// generic set shipped with the tool (assets-base/) is the fallback, so the 55-layout
// template library builds in an empty work directory.
function asset(p) {
  if (path.isAbsolute(p)) return p;
  const own = path.join(WORK, p);
  if (fs.existsSync(own)) return own;
  const rel = p.replace(/^\.?\/?assets\//, "");
  const base = path.join(HERE, "assets-base", rel);
  return fs.existsSync(base) ? base : own;
}

// Resolve an npm dependency from the directories it is installed into, never from the
// plugin folder: WORK, then BASE, then WORK's parent (a project under a default BASE).
function requireDep(name) {
  const tried = [];
  for (const dir of [...new Set([WORK, BASE, path.dirname(WORK)])]) {
    const nm = path.join(dir, "node_modules");
    tried.push(nm);
    if (!fs.existsSync(path.join(nm, name))) continue;
    return createRequire(path.join(dir, "noop.js"))(name);
  }
  try {
    return require(name);             // NODE_PATH, or a global install
  } catch (e) {
    throw new Error(
      `cannot find "${name}". Install it once with:\n  npm install --prefix "${BASE}" ${name}\n` +
      `looked in:\n  ${tried.join("\n  ")}`);
  }
}

module.exports = { TOOL, HERE, BASE, WORK, input, output, asset, requireDep };
