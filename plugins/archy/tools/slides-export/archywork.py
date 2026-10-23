"""Where this tool reads and writes, resolved once and shared by every script.

The tool lives inside the plugin folder, which is replaced on every update, so nothing may
ever be written next to the code. Everything a run produces or consumes (dump/, assets/,
trees/, styles/, the output .pptx) lives in a WORK directory instead:

    --work=DIR (or --work DIR)   highest priority, stripped from sys.argv on import
    $ARCHY_WORK                  the project directory, e.g. $BASE/<project>
    BASE                         when neither is set

BASE is $ARCHY_WORK_BASE, else ${CLAUDE_PLUGIN_DATA}/slides-export, else
./archy-work/slides-export. Shared dependencies (node_modules, .venv, the Hugeicons tarball)
are installed once in BASE.

Code and generic lookups (tokens.json, assets-base/) resolve against HERE.
"""
import os
import sys

TOOL = "slides-export"
HERE = os.path.dirname(os.path.abspath(__file__))


def _take_work_arg():
    argv = sys.argv
    for i in range(1, len(argv)):
        if argv[i].startswith("--work="):
            v = argv[i][7:]
            del argv[i]
            return v
        if argv[i] == "--work" and i + 1 < len(argv):
            v = argv[i + 1]
            del argv[i:i + 2]
            return v
    return None


if os.environ.get("ARCHY_WORK_BASE"):
    BASE = os.environ["ARCHY_WORK_BASE"]
elif os.environ.get("CLAUDE_PLUGIN_DATA"):
    BASE = os.path.join(os.environ["CLAUDE_PLUGIN_DATA"], TOOL)
else:
    BASE = os.path.join(os.getcwd(), "archy-work", TOOL)
BASE = os.path.abspath(BASE)
WORK = os.path.abspath(_take_work_arg() or os.environ.get("ARCHY_WORK") or BASE)


def work(*parts):
    """A path inside WORK."""
    return os.path.join(WORK, *parts)


def here(*parts):
    """A path inside the tool's own directory (read only)."""
    return os.path.join(HERE, *parts)


def input_path(p):
    """Absolute as given; relative tries the current directory first, then WORK."""
    if os.path.isabs(p):
        return p
    if os.path.exists(p):
        return os.path.abspath(p)
    return work(p)


def output_path(p):
    """Absolute as given; relative always lands in WORK, never beside the code."""
    return p if os.path.isabs(p) else work(p)
