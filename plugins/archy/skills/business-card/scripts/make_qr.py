#!/usr/bin/env python3
"""Make a business-card QR as SVG path data and verify it decodes.

Usage: make_qr.py <url> [--version 7] [--error q] [--out qr.d]

Prints the path `d` for an SVG with viewBox "0 0 N N" (N = modules, 45 for
version 7), one horizontal run per rect, no quiet zone (the plate padding is the
quiet zone). Exits with an error if the rendered matrix does not decode back to
the exact URL. Needs: pip install segno numpy opencv-python-headless
"""
import argparse, sys
import numpy as np, segno, cv2

p = argparse.ArgumentParser()
p.add_argument("url")
p.add_argument("--version", type=int, default=7)
p.add_argument("--error", default="q")
p.add_argument("--out")
a = p.parse_args()

try:
    q = segno.make(a.url, version=a.version, error=a.error, boost_error=False)
except Exception as e:  # URL too long for the version: let segno pick
    print(f"version {a.version} too small ({e}); using the smallest that fits", file=sys.stderr)
    q = segno.make(a.url, error=a.error, boost_error=False)
m = np.array([[1 if v else 0 for v in row] for row in q.matrix])
n = m.shape[0]

img = np.pad((np.kron(1 - m, np.ones((10, 10))) * 255).astype(np.uint8), 40, constant_values=255)
decoded = cv2.QRCodeDetector().detectAndDecode(img)[0]
if decoded != a.url:
    sys.exit(f"QR does not decode back to the URL (got {decoded!r})")

parts = []
for r in range(n):
    c = 0
    while c < n:
        if m[r, c]:
            s = c
            while c < n and m[r, c]:
                c += 1
            parts.append(f"M{s} {r}h{c - s}v1h-{c - s}z")
        else:
            c += 1
d = "".join(parts)
print(f"version {q.version}, error {q.error}, {n} modules, decodes OK", file=sys.stderr)
if a.out:
    open(a.out, "w").write(d)
print(d)
