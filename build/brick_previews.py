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

A mural set gets the same treatment from its *composed* panel STL — every
piece placed at its layout offset, written ungated by `make pattern-sets`
(the per-piece gate already ran in the `--format parts` pass). The set's
gallery claim is the reconstituted pattern, so that is what gets drawn.

Usage:  python3 build/brick_previews.py          # bricks (build/.brick-names)
        python3 build/brick_previews.py --sets   # mural sets (build/.set-names)
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
    # Each make target records which stems it just wrote, so this script
    # previews those and not the orbs or cookie cutters sharing build/stls/.
    sets = "--sets" in sys.argv[1:]
    names_file = "build/.set-names" if sets else NAMES_FILE
    target = "make pattern-sets" if sets else "make bricks"
    if not os.path.exists(names_file):
        sys.exit(f"{names_file} missing — run `{target}`, which writes it")
    with open(names_file) as fh:
        names = [line.strip() for line in fh if line.strip()]

    os.makedirs(OUT_DIR, exist_ok=True)
    for name in names:
        stl = f"{STL_DIR}/{name}.stl"
        if not os.path.exists(stl):
            sys.exit(f"{stl} missing — `{target}` did not write it")
        render(binary, stl, f"{OUT_DIR}/{name}.png")
        print(f"{name}.png")
    kind = "set" if sets else "brick"
    print(f"rendered {len(names)} {kind} preview(s) -> {OUT_DIR}")


if __name__ == "__main__":
    main()
