#!/usr/bin/env python3
"""Draw the cookbook's pictures from the exact snippets on its pages.

Every picture in docs/cookbook/ is drawn by the real engine from the fence it
sits under, so a picture can never show something the snippet does not do. A
recipe is a fenced ```bkr block with a marker comment on the line before it:

    <!-- recipe: star-steps; swap: every 2 | every 3 | every 4 -->
    ```bkr
    pattern star
      ...
      connect every 3
    ```
    ![](img/star-steps.png)

The marker names the picture (img/<name>.png) and may vary ONE thing, drawn
side by side with a label under each copy:

  swap: A | B | C       replace whichever item the fence is written with by
                        each item in turn (every occurrence of it)
  param: NAME = 1 | 2   pass each value as `--param NAME=<value>`
  mate: MM              a coaster with a join: draw two copies MM apart
  lifted                a loose coaster: always draw the frame with its pieces lifted
                        above their holes, even where bikar's preview would draw
                        them in place (an open frame's holes only show this way)

A snippet with a `coaster` line is drawn as a 3D coaster: bikar's own color
preview when it can split the coaster into color bodies, otherwise the same
OpenSCAD picture `make coasters` uses (carved, open and jointed coasters). A
coaster with a `loose` line is drawn as it prints: the frame, with each color's
pieces lifted above their pockets in that color; one with a `split` line is
drawn opened up, the lower half, then the pieces, then the upper half turned
face up over them. Any other snippet is drawn flat, with the construction circles and lines bikar
normally hides shown in faint gray, the way the Lab's `?b=1` does.

A snippet that fails to draw fails the run, naming the recipe and bikar's
message: a cookbook entry that no longer compiles is a broken page.

A whole coaster file can be drawn the same way with `--file`, for a plate page's
picture: its `pack` clauses are dropped first, since packing only moves where
the pieces print, so each piece is drawn over its own pocket.

Usage:  python3 tools/cookbook_render.py --all
        python3 tools/cookbook_render.py --recipe star-steps
        python3 tools/cookbook_render.py --list
        python3 tools/cookbook_render.py --file <coaster.bkr> --out <png> [--param k=v ...]
Deps:   bikar CLI (BIKAR_DIR, built), rsvg-convert, ImageMagick, OpenSCAD
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
from brick_previews import mate_offset, openscad, render as openscad_render  # noqa: E402

BOOK = os.path.join(ROOT, "docs", "cookbook")
IMG = os.path.join(BOOK, "img")
MARKER = re.compile(r"<!--\s*recipe:\s*(.+?)\s*-->\s*\n```bkr\n(.*?)\n```", re.S)
TILE = 360  # px per copy in the side-by-side strip

# The construction layer bikar hides; shown thin, gray and dashed so the eye
# still reads the pattern first.
FAINT = ('<style>g[data-layer="-1"]{display:inline!important}'
         'g[data-layer="-1"] *{stroke:#b8b8b8;stroke-width:0.6;stroke-dasharray:2 1.5}</style>')


def bikar_cli():
    bikar_dir = os.environ.get("BIKAR_DIR", os.path.expanduser("~/Workspace/git/bikar-main"))
    cli = os.path.join(bikar_dir, "packages", "cli", "dist", "index.js")
    if not os.path.exists(cli):
        sys.exit(f"bikar CLI not built at {cli} — set BIKAR_DIR to a built bikar checkout")
    return cli


def recipes():
    """{name: (page, marker options, snippet)} across every cookbook page."""
    found = {}
    for page in sorted(glob.glob(os.path.join(BOOK, "*.md"))):
        with open(page) as fh:
            text = fh.read()
        for m in MARKER.finditer(text):
            name, *opts = [p.strip() for p in m.group(1).split(";")]
            if name in found:
                sys.exit(f"recipe '{name}' is named twice ({found[name][0]} and {page})")
            options = {}
            for opt in opts:
                key, _, value = opt.partition(":")
                options[key.strip()] = value.strip()
            found[name] = (page, options, m.group(2) + "\n")
    return found


def variants(name, options, snippet):
    """[(label, source text, extra CLI args)] — one per copy in the picture."""
    if "swap" in options:
        items = [s.strip() for s in options["swap"].split("|")]
        written = [s for s in items if s in snippet]
        if not written:
            sys.exit(f"recipe '{name}': none of the swap items {items} is written in the snippet")
        return [(s, snippet.replace(written[0], s), []) for s in items]
    if "param" in options:
        key, _, values = options["param"].partition("=")
        key = key.strip()
        return [(f"{key} = {v.strip()}", snippet, ["--param", f"{key}={v.strip()}"])
                for v in values.split("|")]
    return [("", snippet, [])]


def run(cmd, name):
    done = subprocess.run(cmd, capture_output=True, text=True)
    if done.returncode != 0:
        msg = (done.stderr or done.stdout).strip().splitlines()
        raise RuntimeError(f"recipe '{name}' did not draw: {msg[0] if msg else 'no message'}")
    return done


def draw_flat(cli, src, extra, out, name, tmp):
    svg = os.path.join(tmp, "flat.svg")
    run(["node", cli, "render", src, "-o", svg, *extra], name)
    with open(svg) as fh:
        text = fh.read()
    text = text.replace('style="display:none"', "", 1) if 'data-layer="-1"' in text else text
    text = re.sub(r"(<svg[^>]*>)", r"\1" + FAINT, text, count=1)
    with open(svg, "w") as fh:
        fh.write(text)
    run(["rsvg-convert", "-w", str(TILE * 2), "-o", out, svg], name)


LOOSE_LIFT = 30  # mm the loose pieces float above the frame, so pocket and piece both show


STRAP_COLOR = "#a8a8a8"  # a split coaster's halves when it names no base color: one neutral gray for both


def loose_parts(cli, src, text, extra, name, tmp, frame_piece="Frame", none_ok=False):
    """A loose coaster drawn the way it is printed: the frame (`--piece Frame`) in
    its base (or straps) color, and each loose color's pieces lifted above their pockets in that
    color. The pieces are whichever palette colors bikar builds as a `--piece`; a
    color it says is not a piece is not loose. `none_ok` is for a coaster whose pieces print
    inside its halves, so there are none to lift."""
    palette = dict(re.findall(r"^\s+(\w+)\s*=\s*(#[0-9a-fA-F]{6})\s*$", text, re.M))
    base = re.search(r"^\s+color\s+(?:base|straps)\s+(\w+)", text, re.M)  # a slab, or an open frame's straps
    frame = os.path.join(tmp, "frame.stl")
    run(["node", cli, "render", src, "--piece", frame_piece, "--format", "stl", "-o", frame, *extra], name)
    parts = []
    for color, hexcode in palette.items():
        stl = os.path.join(tmp, f"piece-{color}.stl")
        done = subprocess.run(["node", cli, "render", src, "--piece", color, "--format", "stl",
                               "-o", stl, *extra], capture_output=True, text=True)
        if done.returncode == 0:
            parts.append((stl, (0, 0, LOOSE_LIFT), hexcode))
        elif "is not a piece" not in done.stderr:
            raise RuntimeError(f"recipe '{name}' did not draw: {done.stderr.strip().splitlines()[0]}")
    if not parts and not none_ok:
        raise RuntimeError(f"recipe '{name}' has a loose line but bikar built no pieces")
    return frame, palette.get(base.group(1)) if base else None, parts


def split_parts(cli, src, text, extra, name, tmp):
    """A split coaster drawn opened up: the lower half (`--piece Lower`), each
    loose color's pieces lifted over their pockets, and the upper half
    (`--piece Upper`, printed face down) turned back over and lifted above them,
    so both holds and the pieces between them show. A pocket hold (way c) prints each piece
    half inside its half, so there are no pieces to lift: the upper half floats one lift up."""
    pocket = bool(re.search(r"\bhold\s+pocket\b", text))
    lower, color, parts = loose_parts(cli, src, text, extra, name, tmp, frame_piece="Lower",
                                      none_ok=pocket)
    color = color or STRAP_COLOR
    upper = os.path.join(tmp, "upper.stl")
    run(["node", cli, "render", src, "--piece", "Upper", "--format", "stl", "-o", upper, *extra], name)
    parts.append((upper, (0, 0, (2 if parts else 1) * LOOSE_LIFT), color, True))
    return lower, color, parts


class NeedsMesh(Exception):
    """bikar will not split this coaster into color bodies (carved, open or jointed)."""


def draw_coaster(cli, src, extra, out, name, tmp, mate_mm, mesh):
    mate = ["--mate", f"{mate_mm},0"] if mate_mm else []
    text = open(src).read()
    split = re.search(r"^\s+split\s", text, re.M)
    if not mesh and not split:
        done = subprocess.run(["node", cli, "render", src, "--format", "preview", "-o", out, *extra, *mate],
                              capture_output=True, text=True)
        if done.returncode == 0:
            return
        if done.stderr.startswith("Error: coaster"):
            raise NeedsMesh()
        raise RuntimeError(f"recipe '{name}' did not draw: {done.stderr.strip().splitlines()[0]}")
    # the picture `make coasters` draws for these in the gallery: the mesh, in OpenSCAD
    binary = openscad()
    if not binary:
        raise RuntimeError(f"recipe '{name}' needs OpenSCAD for its picture")
    if split:
        frame, color, parts = split_parts(cli, src, text, extra, name, tmp)
        openscad_render(binary, frame, out, parts=parts, color=color)
    elif re.search(r"^\s+loose\s", text, re.M):
        frame, color, parts = loose_parts(cli, src, text, extra, name, tmp)
        openscad_render(binary, frame, out, parts=parts, color=color)
    else:
        stl = os.path.join(tmp, "coaster.stl")
        coaster = re.search(r"^coaster\s+(\w+)", text, re.M).group(1)
        run(["node", cli, "render", src, "--piece", coaster, "--format", "stl", "-o", stl, *extra], name)
        openscad_render(binary, stl, out, mate_offset(stl, float(mate_mm)) if mate_mm else None)
    # OpenSCAD's cream background to white, so every picture sits on white
    run(["magick", out, "-fuzz", "6%", "-fill", "white", "-opaque", "#FFFFE5", out], name)


def draw_copy(cli, name, options, i, text, extra, tmp, mesh):
    src = os.path.join(tmp, f"v{i}.bkr")
    with open(src, "w") as fh:
        fh.write(text)
    png = os.path.join(tmp, f"v{i}.png")
    if re.search(r"^coaster\s", text, re.M):
        draw_coaster(cli, src, extra, png, name, tmp, options.get("mate"), mesh)
    else:
        draw_flat(cli, src, extra, png, name, tmp)
    # white behind, trimmed, then padded to one square tile
    run(["magick", png, "-background", "white", "-flatten", "-trim", "+repage",
         "-resize", f"{TILE - 24}x{TILE - 24}", "-gravity", "center",
         "-extent", f"{TILE}x{TILE}", png], name)
    return png


def draw(cli, name, options, snippet):
    copies = variants(name, options, snippet)
    os.makedirs(IMG, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        # one picture style per strip: if bikar refuses to color-split any copy,
        # every copy is drawn as a mesh so the side-by-side compares like with like
        try:
            pngs = [(label, draw_copy(cli, name, options, i, text, extra, tmp, "lifted" in options))
                    for i, (label, text, extra) in enumerate(copies)]
        except NeedsMesh:
            pngs = [(label, draw_copy(cli, name, options, i, text, extra, tmp, True))
                    for i, (label, text, extra) in enumerate(copies)]
        out = os.path.join(IMG, f"{name}.png")
        if len(pngs) == 1:
            shutil.copy(pngs[0][1], out)
        else:
            cmd = ["magick", "montage"]
            for label, png in pngs:
                cmd += ["-label", label, png]
            cmd += ["-tile", f"{len(pngs)}x1", "-geometry", "+8+8", "-pointsize", "20",
                    "-background", "white", out]
            run(cmd, name)
    return os.path.relpath(out, ROOT), len(copies)


def draw_file(cli, path, out, params):
    """One coaster file drawn as the cookbook draws a coaster recipe, to `out`."""
    name = os.path.basename(path)
    text = re.sub(r"[ \t]+pack\s+zipper(?:\s+spacing\s+\S+)?", "", open(path).read())
    if not re.search(r"^coaster\s", text, re.M):
        sys.exit(f"{path} has no coaster block — `--file` draws coasters only")
    extra = [arg for p in params for arg in ("--param", p)]
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, name)
        with open(src, "w") as fh:
            fh.write(text)
        try:
            draw_coaster(cli, src, extra, out, name, tmp, None, False)
        except NeedsMesh:
            draw_coaster(cli, src, extra, out, name, tmp, None, True)
    run(["magick", out, "-background", "white", "-flatten", "-trim", "+repage",
         "-bordercolor", "white", "-border", "24", out], name)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--recipe", help="draw one recipe by name")
    group.add_argument("--all", action="store_true", help="draw every recipe")
    group.add_argument("--list", action="store_true", help="list recipes and their pages")
    group.add_argument("--file", help="draw one coaster .bkr file opened up (needs --out)")
    ap.add_argument("--out", help="the picture --file writes")
    ap.add_argument("--param", action="append", default=[], help="k=v for --file, repeatable")
    args = ap.parse_args()

    if args.file:
        if not args.out:
            sys.exit("--file needs --out <png>")
        draw_file(bikar_cli(), args.file, args.out, args.param)
        print(args.out)
        return

    book = recipes()
    if args.list:
        for name, (page, options, _) in book.items():
            print(f"{name}\t{os.path.relpath(page, ROOT)}\t{options or ''}")
        return
    if args.recipe and args.recipe not in book:
        sys.exit(f"no recipe '{args.recipe}' — `--list` shows them")
    cli = bikar_cli()
    names = [args.recipe] if args.recipe else list(book)
    failed = []
    for name in names:
        page, options, snippet = book[name]
        try:
            out, n = draw(cli, name, options, snippet)
            print(f"{out}" + (f" ({n} side by side)" if n > 1 else ""))
        except RuntimeError as e:
            failed.append(str(e))
            print(f"FAIL {e} [{os.path.relpath(page, ROOT)}]", file=sys.stderr)
    # a picture on disk that no recipe names is a leftover from a renamed recipe
    if args.all:
        for png in glob.glob(os.path.join(IMG, "*.png")):
            if os.path.splitext(os.path.basename(png))[0] not in book:
                failed.append(f"{os.path.relpath(png, ROOT)} has no recipe — delete it or restore its marker")
                print(f"FAIL {failed[-1]}", file=sys.stderr)
    if failed:
        sys.exit(f"{len(failed)} cookbook picture(s) failed")
    print(f"drew {len(names)} recipe picture(s) -> {os.path.relpath(IMG, ROOT)}")


if __name__ == "__main__":
    main()
