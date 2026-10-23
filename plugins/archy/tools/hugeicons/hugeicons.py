#!/usr/bin/env python3
"""Hugeicons Stroke Rounded, straight from the free npm package, as Paper-ready SVG.

    hugeicons.py fetch                              download the package once, write names.txt
    hugeicons.py names [substring ...]              list (or search) the real icon names
    hugeicons.py svg <Name> [<Name> ...] --stroke "var(--color-royal-blue-500)"
                     [--size 24] [--out icons.svg]  print SVG markup, one <svg> per icon

Names are the package's module names (`UserGroupIcon`); the `Icon` suffix may be left off.
Every name is validated against names.txt and a near miss is refused with suggestions,
because a plausible invented name is the easy mistake.

The markup is `viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round"
stroke-linejoin="round"` with `stroke` set to the colour given (a token on the canvas,
never `currentColor`: it does not resolve through a parent frame in Paper).

Work directory (where the tarball, names.txt and any --out file live), never the plugin
folder: --work DIR > $ARCHY_WORK > ${CLAUDE_PLUGIN_DATA}/hugeicons > ./archy-work/hugeicons.
Needs `npm` on the PATH for `fetch` (it asks npm for the tarball URL). No other dependencies.
"""
import argparse
import difflib
import os
import re
import subprocess
import sys
import tarfile
import urllib.request

PACKAGE = "@hugeicons/core-free-icons"
MODULE_RE = re.compile(r"^package/dist/esm/(\w+Icon)\.js$")
# The module's attribute keys are UNQUOTED JS, not JSON: `{ d: "M20.99...", ..., key: "0" }`.
# A regex looking for `"d":` matches nothing and silently yields empty paths. Every element
# ends with a `key` property, which makes a reliable terminator.
ELEMENT_RE = re.compile(r'\["(\w+)",\s*\{(.*?)\s*key:', re.S)
ATTR_RE = re.compile(r'(\w+):\s*(?:"([^"]*)"|([-\d.]+))')
# Set once on the <svg>, so dropped from each element.
SVG_LEVEL = {"stroke", "strokeWidth", "strokeLinecap", "strokeLinejoin", "key"}


def work_dir(arg):
    if arg:
        return os.path.abspath(arg)
    if os.environ.get("ARCHY_WORK"):
        return os.path.abspath(os.environ["ARCHY_WORK"])
    if os.environ.get("CLAUDE_PLUGIN_DATA"):
        return os.path.join(os.environ["CLAUDE_PLUGIN_DATA"], "hugeicons")
    return os.path.abspath(os.path.join("archy-work", "hugeicons"))


def kebab(name):
    return re.sub(r"([A-Z])", lambda m: "-" + m.group(1).lower(), name)


def fetch(work):
    os.makedirs(work, exist_ok=True)
    tgz = os.path.join(work, "hugeicons.tgz")
    if not os.path.exists(tgz) or os.path.getsize(tgz) == 0:
        try:
            url = subprocess.run(["npm", "view", PACKAGE, "dist.tarball"], check=True,
                                 capture_output=True, text=True).stdout.strip()
        except FileNotFoundError:
            raise SystemExit("npm not found: install Node.js (nodejs.org, or `brew install node`)")
        print("downloading %s" % url, file=sys.stderr)
        urllib.request.urlretrieve(url, tgz)
    with tarfile.open(tgz) as tar:
        names = sorted(m.group(1) for m in (MODULE_RE.match(n) for n in tar.getnames()) if m)
    if not names:
        raise SystemExit("no icon modules found in %s" % tgz)
    with open(os.path.join(work, "names.txt"), "w") as f:
        f.write("\n".join(names) + "\n")
    print("%d icons, names in %s" % (len(names), os.path.join(work, "names.txt")),
          file=sys.stderr)
    return tgz, names


def load(work):
    tgz = os.path.join(work, "hugeicons.tgz")
    txt = os.path.join(work, "names.txt")
    if not (os.path.exists(tgz) and os.path.exists(txt)):
        return fetch(work)
    return tgz, open(txt).read().split()


def resolve(name, names):
    known = set(names)
    for cand in (name, name + "Icon"):
        if cand in known:
            return cand
    close = difflib.get_close_matches(name if name.endswith("Icon") else name + "Icon",
                                      names, n=6, cutoff=0.6)
    raise SystemExit("%s is not a real icon name.%s" % (
        name, (" Close: " + ", ".join(close)) if close else ""))


def elements(tar, name):
    src = tar.extractfile("package/dist/esm/%s.js" % name).read().decode("utf-8")
    out = []
    for tag, body in ELEMENT_RE.findall(src):
        attrs = {k: (s if s is not None else n) for k, s, n in ATTR_RE.findall(body)}
        if tag == "path":
            # The silent failure is an empty `d`: a blank square that reads as a spacing
            # bug rather than a missing icon.
            d = re.search(r'd:\s*"([^"]*)"', body)
            if not d or not d.group(1).strip():
                raise SystemExit("%s: empty path data" % name)
        parts = []
        for k, v in attrs.items():
            if k in SVG_LEVEL:
                continue
            parts.append('%s="%s"' % (kebab(k), v))
        out.append((tag, attrs, " ".join(parts)))
    if not out:
        raise SystemExit("%s: no elements found" % name)
    return out


def svg(tar, name, stroke, size):
    body = []
    for tag, attrs, rendered in elements(tar, name):
        # A filled element (a dot) paints in the icon colour rather than currentColor.
        rendered = rendered.replace('fill="currentColor"', 'fill="%s"' % stroke)
        body.append("  <%s %s/>" % (tag, rendered))
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" '
            'viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round">\n{b}\n</svg>').format(
                s=size, c=stroke, b="\n".join(body))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--work", help="work directory (default: see above)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch")
    p = sub.add_parser("names")
    p.add_argument("query", nargs="*")
    p = sub.add_parser("svg")
    p.add_argument("icons", nargs="+")
    p.add_argument("--stroke", required=True,
                   help='colour, e.g. "var(--color-royal-blue-500)" or "#013DF5"')
    p.add_argument("--size", type=int, default=24)
    p.add_argument("--out", help="also write the markup to this file (relative = work dir)")
    a = ap.parse_args()
    work = work_dir(a.work)

    if a.cmd == "fetch":
        fetch(work)
        return
    tgz, names = load(work)
    if a.cmd == "names":
        qs = [q.lower() for q in a.query]
        for n in names:
            if all(q in n.lower() for q in qs):
                print(n)
        return

    if a.stroke.strip() == "currentColor":
        print("warning: currentColor does not resolve through a parent frame in Paper; "
              "pass a token", file=sys.stderr)
    with tarfile.open(tgz) as tar:
        markup = "\n".join(svg(tar, resolve(n, names), a.stroke, a.size) for n in a.icons)
    if 'd=""' in markup:
        raise SystemExit("empty d attribute in the output")
    print(markup)
    if a.out:
        out = a.out if os.path.isabs(a.out) else os.path.join(work, a.out)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            f.write(markup + "\n")
        print("wrote %s" % out, file=sys.stderr)


if __name__ == "__main__":
    main()
