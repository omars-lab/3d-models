"""Render a stencil's .scad into the card's STL and the plate page's two pictures.

The .scad follows the make-stencil skill's contract: a `part` variable with "sheet" (the card that
prints) and "paper" (the finished drawing on the page, with the card's outline where it sits).
This writes the STL, `on-paper.png` and `pieces.png`, and prints the STL's sha256 for the recipe.
The third picture, `bed.png`, is the slicer's: copy `build/plates/<plate>.plate.preview.png` after
`bambu slice compose`.

    python3 .claude/skills/make-stencil/scripts/render_stencil.py src/Stencils/LebanonCedar.scad \
        --stl src/Stencils/lebanon-cedar-sheet-letter.stl --media docs/design/plates/cedar-stencil-1-media
"""

import argparse
import hashlib
import subprocess
from pathlib import Path

OPENSCAD = "/Applications/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD"
PICTURE = ["--camera=0,0,0,0,0,0,520", "--viewall", "--autocenter", "--projection=o",
           "--imgsize=1600,1400", "--colorscheme=Tomorrow"]


def openscad(scad: Path, out: Path, part: str, defines: list[str], extra: list[str]) -> None:
    args = [OPENSCAD, "-D", f'part="{part}"', *[x for d in defines for x in ("-D", d)], *extra,
            "-o", str(out), str(scad)]
    run = subprocess.run(args, capture_output=True, text=True, timeout=600)
    if run.returncode != 0 or not out.is_file():
        raise SystemExit(f"OpenSCAD failed on part={part}:\n{run.stderr[-2000:]}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scad", type=Path)
    ap.add_argument("--stl", required=True, type=Path, help="where the card's STL goes")
    ap.add_argument("--media", type=Path, help="the plate's -media folder for the two pictures")
    ap.add_argument("-D", dest="defines", action="append", default=[],
                    help='an OpenSCAD override, e.g. -D \'paper="a4"\' (repeat for more)')
    a = ap.parse_args()

    a.stl.parent.mkdir(parents=True, exist_ok=True)
    openscad(a.scad, a.stl, "sheet", a.defines, [])
    sha = hashlib.sha256(a.stl.read_bytes()).hexdigest()
    print(f"stl={a.stl} sha256={sha}")
    if a.media:
        a.media.mkdir(parents=True, exist_ok=True)
        for part, name in (("paper", "on-paper.png"), ("sheet", "pieces.png")):
            openscad(a.scad, a.media / name, part, a.defines, PICTURE)
            print(f"picture={a.media / name}")


if __name__ == "__main__":
    main()
