#!/usr/bin/env python3
"""Render bikar brick STLs into gallery preview PNGs.

Orbs get their previews from their per-symmetry-axis *validation* views
(build/orb_previews.py restyles those SVGs). A brick has no view set —
qiyas validates orb symmetry-axis renders and there is no brick
equivalent, so a brick's claim is made by its two grid gates and the
mesh gate, not by a render. That leaves the mesh itself as the only
honest thing to draw, so this script draws it: OpenSCAD `import()`s
each STL `make bricks` just wrote and rasterizes one three-quarter
view.

That gets the gallery chain for free. OpenSCAD's Cornfield preview is
gold on cream (#FFFFE5), which is exactly what build/process_images.py
already keys out to transparency and autocrops — so a brick PNG lands
in build/images/ and `make web-images` finishes it alongside every
OpenSCAD render and every orb.

Usage:  python3 build/brick_previews.py
Deps:   OpenSCAD  (the same binary the cookie-cutter targets use)
"""
import glob
import os
import subprocess
import sys
import tempfile

STL_DIR = "build/stls"
OUT_DIR = "build/images"
NAMES_FILE = "build/.brick-names"
SIZE = 1024

# Rotation only. `--viewall --autocenter` computes the distance, so the
# same three-quarter angle frames a 1x8 rail and a 6x6 tile alike without
# a per-model camera — and a per-model camera is a number nobody measured.
CAMERA = "0,0,0,60,0,25,0"


def openscad():
    """The OpenSCAD binary, resolved across install variants (mirrors the Makefile)."""
    for pat in (
        "/Applications/OpenSCAD-*.app/Contents/MacOS/OpenSCAD",
        "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD",
    ):
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    from shutil import which

    return which("openscad")


def render(binary, stl, out):
    with tempfile.NamedTemporaryFile("w", suffix=".scad", delete=False) as fh:
        fh.write(f'import("{os.path.abspath(stl)}");\n')
        scad = fh.name
    try:
        subprocess.run(
            [
                binary,
                "-o",
                out,
                f"--imgsize={SIZE},{SIZE}",
                f"--camera={CAMERA}",
                "--viewall",
                "--autocenter",
                "--colorscheme=Cornfield",
                scad,
            ],
            check=True,
            capture_output=True,
        )
    finally:
        os.unlink(scad)


def main():
    binary = openscad()
    if not binary:
        sys.exit("OpenSCAD not found — brick previews need the same binary as `make cookie-cutters`")
    # `make bricks` records which stems it just wrote, so this script previews
    # the bricks and not the orbs or cookie cutters sharing build/stls/.
    if not os.path.exists(NAMES_FILE):
        sys.exit(f"{NAMES_FILE} missing — run `make bricks`, which writes it")
    with open(NAMES_FILE) as fh:
        names = [line.strip() for line in fh if line.strip()]

    os.makedirs(OUT_DIR, exist_ok=True)
    for name in names:
        stl = f"{STL_DIR}/{name}.stl"
        if not os.path.exists(stl):
            sys.exit(f"{stl} missing — `make bricks` did not write it")
        render(binary, stl, f"{OUT_DIR}/{name}.png")
        print(f"{name}.png")
    print(f"rendered {len(names)} brick preview(s) -> {OUT_DIR}")


if __name__ == "__main__":
    main()
