#!/usr/bin/env python3
"""Style bikar orb validation views into gallery preview PNGs.

`make orbs` renders each orb's per-symmetry-axis views (SVG) into
build/orb-views/<Orb>/. Those are validation renders — flat gray faces
on a white card. This script picks each orb's hero view (the
highest-fold axis reads most iconic), recolors it to the catalog gold,
drops the background card so the orb floats on the page like every
other plate, and rasterizes it into build/images/<Orb>.png, where
`make web-images` autocrops it alongside the OpenSCAD renders.

Usage:  python3 build/orb_previews.py
Deps:   rsvg-convert   (brew install librsvg)
"""
import glob
import os
import re
import subprocess
import sys

VIEWS_DIR = "build/orb-views"
OUT_DIR = "build/images"
SIZE = 1024
FILL = "#c79a2e"    # --gold in index.html — echoes the OpenSCAD render gold
STROKE = "#7a5d17"


def hero(svgs):
    # Highest symmetry fold reads most iconic (vertex-5 on icosahedral
    # orbs, face-5 on dodecahedral); tie-break vertex > face > edge.
    def key(path):
        m = re.search(r"\.([a-z]+)-(\d+)\.svg$", os.path.basename(path))
        kind, fold = (m.group(1), int(m.group(2))) if m else ("", 0)
        rank = {"vertex": 0, "face": 1, "edge": 2}.get(kind, 3)
        return (-fold, rank)
    return sorted(svgs, key=key)[0]


def restyle(text):
    text = re.sub(r'<rect [^>]*fill="#ffffff"[^>]*/>\s*', "", text, count=1)
    text = text.replace('fill="#8a8a8a"', f'fill="{FILL}"')
    text = text.replace('stroke="#333333"', f'stroke="{STROKE}"')
    return text


def main():
    orb_dirs = sorted(glob.glob(f"{VIEWS_DIR}/*/"))
    if not orb_dirs:
        sys.exit(f"no views under {VIEWS_DIR} — run `make orbs` first")
    for d in orb_dirs:
        svgs = [p for p in glob.glob(os.path.join(d, "*.svg"))
                if ".preview." not in p]
        if not svgs:
            continue
        pick = hero(svgs)
        orb = os.path.basename(pick).split(".")[0]
        with open(pick) as f:
            styled = restyle(f.read())
        tmp = os.path.join(d, f"{orb}.preview.svg")
        with open(tmp, "w") as f:
            f.write(styled)
        out = f"{OUT_DIR}/{orb}.png"
        subprocess.run(
            ["rsvg-convert", "-w", str(SIZE), "-h", str(SIZE), "-o", out, tmp],
            check=True,
        )
        os.remove(tmp)
        print(f"{orb}: {os.path.basename(pick)} -> {out}")


if __name__ == "__main__":
    main()
