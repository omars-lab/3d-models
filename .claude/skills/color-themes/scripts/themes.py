#!/usr/bin/env python3
"""Color themes for a loose-piece coaster: draw them, check them, cost them, and write the gallery.

One construction's themes live in one folder, `docs/design/coaster/themes/<id>/`:

    themes.yaml    the groups, the print size, and each theme's name, mood and group -> color map
    base.svg       bikar's flat drawing of the coaster, each group's faces in a marker color (`base`)
    volumes.yaml   each group's plastic, from bikar's STL of it (`measure`)
    <theme>.svg    the theme's picture (`render`)
    reviews.yaml   the persona reviews (the review-theme skill writes these)

and the gallery is `docs/design/coaster/themes/<id>-themes.md` (`gallery`).

Only `base` and `measure` run bikar. Everything else reads the files above, so `check --all`
runs offline in `make validate` and fails when a picture or a gallery page is stale.

Usage:
    themes.py base     <id>                  bikar -> base.svg
    themes.py measure  <id>                  bikar STLs -> volumes.yaml
    themes.py render   <id> [--png DIR]      every theme's picture; --png also writes PNGs to look at
    themes.py check    <id> | --all          colors, neighbors, contrast, plates; stale files fail
    themes.py suggest  <id> --helper match-trays|alternate|one-color [--colors a,b,...]
    themes.py suggest  <id> --helper gradient --from <color> --to <color> [--reverse] [--lines L1,L2]
    themes.py gallery  <id>                  write the gallery page
    themes.py --self-test

A color is a palette.yaml id. Every buy color is checked against the Bambu catalog that
`catalog.py` builds, which also says each color's finish (silk, sparkle, translucent, ...) and
whether its spool carries more than one hex; the pictures draw both.
"""
from __future__ import annotations

import argparse
import hashlib
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog as bambu  # noqa: E402  (the catalog script beside this one)

SKILL = Path(__file__).resolve().parent.parent
ROOT = SKILL.parent.parent.parent
THEMES_DIR = ROOT / "docs" / "design" / "coaster" / "themes"
PALETTE = SKILL / "palette.yaml"
PERSONAS = ROOT / ".claude" / "skills" / "review-theme" / "personas.md"

FRAME = "frame"
BACKDROP = "#EFEAE3"  # a light table color behind every picture, so white and black both show

# Two neighbors closer than this (CIE76 delta E) get a "may blur together" warning. Picked by eye
# on these renders; nothing we have measured says what a person sees across a strap, so it is a
# starting number to tune on the first prints (infill-color-ux-design §4.3 says the same).
CLOSE_DELTA_E = 20.0
# Below this colorfulness (C* in L*a*b*) a color counts as a gray, black or white: what the
# gradient helper picks a frame from, and never a step between two colorful ends.
NEUTRAL_CHROMA = 12.0


# ---------------------------------------------------------------- data


def load_yaml(path: Path):
    with open(path) as f:
        return yaml.safe_load(f)


def palette(path: Path = PALETTE, cat: dict | None = None) -> dict:
    """Color id -> {hex, hexes, name, owned, finish, alpha, kind, ...}.

    `hex` is the one color the checks and the color math use: the spool's own hex, or for a
    spool with several, their average. `hexes` is every hex the spool carries (without alpha).
    A buy color's finish, alpha and kind come from the catalog by its product code. An owned
    tray is only a hex the printer reported, so it has no finish and is drawn flat.
    """
    data = load_yaml(path)
    by_code = (cat or bambu.load_catalog())["by_code"]
    out = {}
    for c in data["owned"]:
        h = c["hex"].upper()
        out[c["id"]] = {**c, "hex": h, "hexes": [h], "owned": True, "finish": None, "alpha": 1.0, "kind": "single"}
    for c in data["buy"]:
        if c["id"] in out:
            raise SystemExit(f"palette: color id {c['id']} listed twice")
        hexes = [h.upper() for h in (c["hexes"] if "hexes" in c else [c["hex"]])]
        e = by_code.get(str(c["code"]))
        out[c["id"]] = {**c, "hex": spool_mean(hexes), "hexes": hexes, "owned": False,
                        "finish": e["finish"] if e else None,
                        "alpha": bambu.alpha(e["hexes"][0]) if e else 1.0,
                        "kind": e["kind"] if e else "single"}
    return out


def buy_problems(c: dict, cat: dict) -> list[str]:
    """A buy color must be a catalog color in a coaster line, with the catalog's name and hexes."""
    e = cat["by_code"].get(str(c.get("code")))
    if e is None:
        return [f"code {c.get('code')} is not in the Bambu catalog"]
    out = []
    want = [bambu.opaque(h) for h in e["hexes"]]
    if c["hexes"] != want:
        out.append(f"{' '.join(c['hexes'])} differs from the catalog's {' '.join(want)} for {e['code']}")
    if c["name"] != e["name"]:
        out.append(f"name {c['name']!r} differs from the catalog's {e['name']!r}")
    if c.get("line") != e["line"]:
        out.append(f"line {c.get('line')!r} differs from the catalog's {e['line']!r}")
    if e["line"] not in cat["coaster_lines"]:
        out.append(f"{e['line']} is not a line a coaster prints in (catalog.yaml coaster_lines)")
    return out


def construction(cid: str, root: Path = THEMES_DIR) -> dict:
    folder = root / cid
    data = load_yaml(folder / "themes.yaml")
    data["_folder"] = folder
    return data


def group_ids(con: dict) -> list[str]:
    return [g["id"] for g in con["groups"]] + [FRAME]


def theme_hash(theme: dict) -> str:
    """A short hash of the coloring alone, so a review can say which coloring it saw."""
    pairs = sorted(theme["colors"].items())
    return hashlib.sha256(repr(pairs).encode()).hexdigest()[:10]


# ---------------------------------------------------------------- color math


def rgb(hexstr: str) -> tuple[float, float, float]:
    h = hexstr.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))


def to_hex(c) -> str:
    return "#" + "".join(f"{max(0, min(255, round(v * 255))):02X}" for v in c)


def lab(hexstr: str) -> tuple[float, float, float]:
    """sRGB -> CIE L*a*b* (D65)."""

    def lin(v):
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (lin(v) for v in rgb(hexstr))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a: str, b: str) -> float:
    return math.dist(lab(a), lab(b))


def mix(hexstr: str, other: str, t: float) -> str:
    a, b = rgb(hexstr), rgb(other)
    return to_hex(tuple(x + (y - x) * t for x, y in zip(a, b)))


def spool_mean(hexes: list[str]) -> str:
    """The average of a spool's hexes, for the checks; one hex is itself."""
    if len(hexes) == 1:
        return hexes[0][:7].upper()
    cs = [rgb(h) for h in hexes]
    return to_hex(tuple(sum(c[i] for c in cs) / len(cs) for i in range(3)))


def edge_shade(hexstr: str) -> str:
    """A thin outline that shows on any color: darker for light colors, lighter for dark ones."""
    return mix(hexstr, "#000000", 0.35) if lab(hexstr)[0] > 30 else mix(hexstr, "#FFFFFF", 0.3)


# ---------------------------------------------------------------- bikar


def bikar_dir() -> Path:
    return Path(os.environ.get("BIKAR_DIR", os.path.expanduser("~/Workspace/git/bikar-main")))


def bikar_path(ref: str) -> Path:
    if not ref.startswith("bikar:"):
        raise SystemExit(f"expected a bikar:… path, got {ref}")
    return bikar_dir() / ref[len("bikar:") :]


def run_bikar(args: list[str]) -> str:
    cli = bikar_dir() / "packages" / "cli" / "dist" / "index.js"
    if not cli.exists():
        raise SystemExit(f"bikar CLI not built at {cli}; set BIKAR_DIR to a built bikar checkout")
    node = shutil.which("node")
    nvm = Path.home() / ".nvm" / "versions" / "node" / "v22.22.3" / "bin" / "node"
    if nvm.exists():
        node = str(nvm)
    proc = subprocess.run([node, str(cli), *args], capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise SystemExit(f"bikar {' '.join(args[:2])} failed:\n{proc.stdout}{proc.stderr}")
    return proc.stdout


def bikar_commit() -> str:
    proc = subprocess.run(["git", "-C", str(bikar_dir()), "rev-parse", "--short=10", "HEAD"],
                          capture_output=True, text=True)
    return proc.stdout.strip() or "unknown"


def marker_hex(index: int) -> str:
    """The color each group's faces get in base.svg. Never a filament color, never #333333."""
    return f"#01{(index * 37) % 256:02X}{index + 16:02X}"


def with_marker_palette(src: str, con: dict) -> str:
    """The frame .bkr with a palette that paints each group's orbits in its marker color.

    The palette goes inside the pattern block, just before the `coaster` block, which is where
    the gBV pieces file keeps its own. A file that already has a palette is refused rather than
    guessed at.
    """
    if re.search(r"^\s+palette\s", src, re.M):
        raise SystemExit("the frame file already has a palette; point `frame:` at a file with none")
    m = re.search(r"^coaster\s", src, re.M)
    if not m:
        raise SystemExit("no `coaster` block in the frame file")
    lines = ["  palette themes"]
    for i, g in enumerate(con["groups"]):
        lines.append(f"    G{i} = {marker_hex(i)}")
    for i, g in enumerate(con["groups"]):
        for orbit in g["orbits"]:
            lines.append(f"    fill void where orbit == {orbit} color G{i}")
    return src[: m.start()] + "\n".join(lines) + "\n\n" + src[m.start() :]


def param_args(params: dict) -> list[str]:
    out = []
    for k, v in params.items():
        out += ["--param", f"{k}={v}"]
    return out


def cmd_base(cid: str) -> None:
    con = construction(cid)
    src = bikar_path(con["source"]["frame"]).read_text()
    with tempfile.TemporaryDirectory() as tmp:
        bkr = Path(tmp) / "frame-with-markers.bkr"
        bkr.write_text(with_marker_palette(src, con))
        out = Path(tmp) / "base.svg"
        run_bikar(["render", str(bkr), "-o", str(out), *param_args(con["params"])])
        svg = out.read_text()
    faces, straps = parse_base(svg)
    known = {marker_hex(i) for i in range(len(con["groups"]))}
    stray = {f["fill"] for f in faces} - known
    if stray:
        raise SystemExit(f"base: faces in colors no group claims: {sorted(stray)}")
    header = (f"<!-- generated by .claude/skills/color-themes/scripts/themes.py base {cid}, "
              f"bikar {bikar_commit()}; each group's faces are in its marker color -->\n")
    (con["_folder"] / "base.svg").write_text(header + svg)
    print(f"base.svg: {len(faces)} faces, {len(straps)} strap lines")


def stl_volume(path: Path) -> float:
    """Volume in mm³ of a binary STL (bikar writes binary), by the signed-tetrahedron sum."""
    data = path.read_bytes()
    (n,) = struct.unpack_from("<I", data, 80)
    vol = 0.0
    for i in range(n):
        off = 84 + i * 50 + 12
        ax, ay, az, bx, by, bz, cx, cy, cz = struct.unpack_from("<9f", data, off)
        vol += (ax * (by * cz - bz * cy) - ay * (bx * cz - bz * cx) + az * (bx * cy - by * cx)) / 6
    return abs(vol)


def cmd_measure(cid: str) -> None:
    con = construction(cid)
    vols = {}
    with tempfile.TemporaryDirectory() as tmp:
        frame_stl = Path(tmp) / "frame.stl"
        run_bikar(["render", str(bikar_path(con["source"]["frame"])), "--format", "stl",
                   "-o", str(frame_stl), *param_args(con["params"])])
        vols[FRAME] = stl_volume(frame_stl)
        for g in con["groups"]:
            stl = Path(tmp) / f"{g['id']}.stl"
            run_bikar(["render", str(bikar_path(con["source"]["pieces"])), "--format", "stl",
                       "--piece", g["piece"], "-o", str(stl), *param_args(con["piece_params"])])
            vols[g["id"]] = stl_volume(stl)
    lines = [
        f"# generated by .claude/skills/color-themes/scripts/themes.py measure {cid}",
        f"# bikar {bikar_commit()}: mm³ of each group's STL at this construction's print size.",
        "# The cost split in the gallery is by these shares (an estimate; see SKILL.md).",
    ]
    for k in group_ids(con):
        lines.append(f"{k}: {vols[k]:.1f}")
    (con["_folder"] / "volumes.yaml").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[3:]))


# ---------------------------------------------------------------- the picture


def parse_base(svg: str):
    faces = []
    for m in re.finditer(r'<polygon points="([^"]+)" fill="(#[0-9A-Fa-f]{6})"', svg):
        pts = [tuple(round(float(v), 3) for v in p.split(",")) for p in m.group(1).split()]
        faces.append({"points": pts, "fill": m.group(2).upper()})
    straps = []
    for m in re.finditer(r'<line x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)" '
                         r'stroke="#333333" stroke-width="([\d.]+)"', svg):
        straps.append(tuple(float(v) for v in m.groups()))
    return faces, straps


def view_box(svg: str) -> str:
    return re.search(r'viewBox="([^"]+)"', svg).group(1)


def face_groups(con: dict, faces: list[dict]) -> list[str]:
    by_marker = {marker_hex(i): g["id"] for i, g in enumerate(con["groups"])}
    return [by_marker[f["fill"]] for f in faces]


def needs_finish(c: dict) -> bool:
    """Whether a color draws as more than a flat fill: a finish, a see-through, or several hexes."""
    return (len(c["hexes"]) > 1 or c["alpha"] < 1
            or c["finish"] in bambu.SHEEN or c["finish"] in bambu.FLECKS)


def draw(con: dict, theme: dict, base_svg: str, pal: dict) -> str:
    """The theme's picture. A flat color is a plain fill; a finish adds to it (catalog.py draws
    the same finishes on the swatch sheets): silk and metal a white sheen across each piece,
    sparkle and galaxy flecks, translucent a see-through fill, and a spool with several hexes a
    gradient through them. A color with none of these draws exactly as it did before finishes.
    """
    faces, straps = parse_base(base_svg)
    groups = face_groups(con, faces)
    colors = {k: pal[v] for k, v in theme["colors"].items()}
    hexes = {k: c["hex"] for k, c in colors.items()}
    keys = {k: f"f-{theme['colors'][k]}" for k in colors}
    vb = view_box(base_svg)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="480" height="480">',
        f"  <title>{con['short']}: {theme['name']}</title>",
    ]
    defs, seen = [], set()
    for k, c in colors.items():
        if needs_finish(c) and keys[k] not in seen:
            seen.add(keys[k])
            defs += bambu.finish_defs(keys[k], c["finish"], [h + "FF" for h in c["hexes"]])
    if defs:
        out += ["  <defs>", *("    " + d for d in defs), "  </defs>"]
    out += [f'  <rect x="-1000" y="-1000" width="2000" height="2000" fill="{BACKDROP}" />',
            '  <g class="pieces">']
    overlays = []
    for f, g in zip(faces, groups):
        pts = " ".join(f"{x:.3f},{y:.3f}" for x, y in f["points"])
        c = hexes[g]
        fill = f'fill="{c}"'
        if needs_finish(colors[g]):
            fill = bambu.fill_attrs(keys[g], [h + bambu_alpha(colors[g]) for h in colors[g]["hexes"]])
            for ov in bambu.overlay_fills(keys[g], colors[g]["finish"]):
                overlays.append(f'    <polygon points="{pts}" fill="{ov}" />')
        out.append(f'    <polygon points="{pts}" {fill} stroke="{edge_shade(c)}" '
                   f'stroke-width="0.35" stroke-linejoin="round" data-group="{g}" />')
    out.append("  </g>")
    if overlays:
        out += ['  <g class="finish">', *overlays, "  </g>"]
    frame = hexes[FRAME]
    fc = colors[FRAME]
    see = f' stroke-opacity="{bambu.draw_opacity(fc["alpha"])}"' if fc["alpha"] < 1 else ""
    # Each layer: class, stroke color, the line width from the strap's width, extra attributes.
    layers = [("frame-edge", edge_shade(frame), lambda w: w + 0.7, ' stroke-linecap="round"'),
              ("frame", fc["hexes"][0][:7], lambda w: w, ' stroke-linecap="round"' + see)]
    n = len(fc["hexes"])
    for i, h in enumerate(fc["hexes"][1:], 1):  # a spool's other hexes as dashes along the strap
        layers.append((f"frame-spool-{i}", h[:7], lambda w: w,
                       f' stroke-linecap="butt" stroke-dasharray="4 {4 * (n - 1):g}" '
                       f'stroke-dashoffset="{-4 * i:g}"{see}'))
    if fc["finish"] in bambu.SHEEN:
        layers.append(("frame-sheen", mix(frame, "#FFFFFF", 0.6), lambda w: w * 0.3,
                       ' stroke-linecap="round" stroke-opacity="0.7"'))
    if fc["finish"] in bambu.FLECKS:
        fleck = "#FFFFFF" if lab(frame)[0] < 60 else "#5A5A5A"
        # Small dots at uneven spacing: even spacing reads as stitching, not glitter.
        layers.append(("frame-flecks", fleck, lambda w: w * 0.16,
                       ' stroke-linecap="round" stroke-opacity="0.75" '
                       'stroke-dasharray="0 2.9 0 1.3 0 4.1 0 2.2"'))
    for cls, color, width, attrs in layers:
        out.append(f'  <g class="{cls}" stroke="{color}"{attrs}>')
        for x1, y1, x2, y2, w in straps:
            out.append(f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-width="{width(w):.3f}" />')
        out.append("  </g>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def bambu_alpha(c: dict) -> str:
    """The alpha byte a palette color is drawn with: the catalog's, or opaque."""
    return f"{round(c['alpha'] * 255):02X}"


def cmd_render(cid: str, png_dir: str | None) -> None:
    con = construction(cid)
    pal = palette()
    base = (con["_folder"] / "base.svg").read_text()
    for t in con["themes"]:
        problems = theme_problems(con, t, pal)
        if problems:
            raise SystemExit(f"{t['id']}: " + "; ".join(problems))
        path = con["_folder"] / f"{t['id']}.svg"
        path.write_text(draw(con, t, base, pal))
        if png_dir:
            Path(png_dir).mkdir(parents=True, exist_ok=True)
            png = Path(png_dir) / f"{cid}-{t['id']}.png"
            subprocess.run(["rsvg-convert", "-w", "480", str(path), "-o", str(png)], check=True)
        print(path.relative_to(ROOT))


# ---------------------------------------------------------------- checks


def theme_problems(con: dict, theme: dict, pal: dict) -> list[str]:
    """Hard errors: a theme must color every group, frame included, with a palette color."""
    want = set(group_ids(con))
    have = set(theme.get("colors", {}))
    out = []
    if want - have:
        out.append(f"no color for {sorted(want - have)}")
    if have - want:
        out.append(f"colors for groups this construction does not have: {sorted(have - want)}")
    for k, v in theme.get("colors", {}).items():
        if v not in pal:
            out.append(f"{k}: '{v}' is not a color in palette.yaml (owned or buy)")
    for key in ("id", "name", "mood"):
        if not theme.get(key):
            out.append(f"no {key}")
    return out


def neighbors(con: dict, faces: list[dict]) -> set[frozenset]:
    """Pairs of groups whose faces share an edge (two or more corners). The frame touches all."""
    groups = face_groups(con, faces)
    pairs = set()
    for i in range(len(faces)):
        a = set(faces[i]["points"])
        for j in range(i + 1, len(faces)):
            if groups[i] != groups[j] and len(a & set(faces[j]["points"])) >= 2:
                pairs.add(frozenset((groups[i], groups[j])))
    for g in con["groups"]:
        pairs.add(frozenset((g["id"], FRAME)))
    return pairs


def join_words(words: list[str]) -> str:
    return words[0] if len(words) == 1 else ", ".join(words[:-1]) + " and " + words[-1]


def short_label(label: str) -> str:
    """'the kites (10)' -> 'kites', for lists where the brackets would nest."""
    return re.sub(r"\s*\(.*\)$", "", label).removeprefix("the ")


def warnings(con: dict, theme: dict, pal: dict, pairs: set[frozenset]) -> list[str]:
    """Pieces in the frame's color, which melt into it; then close colors, pair by pair.

    Two pieces in one color are not warned about: a strap runs between every two pieces, so they
    still read as separate pieces (the gold pieces of black-and-gold). A piece in the frame's own
    color has nothing between it and the strap, and that part of the pattern is lost.
    """
    out = []
    pieces = [g["id"] for g in con["groups"]]
    frame_hex = pal[theme["colors"][FRAME]]["hex"]
    melted = [g for g in pieces if pal[theme["colors"][g]]["hex"] == frame_hex]
    if melted:
        name = pal[theme["colors"][FRAME]]["name"]
        who = "every piece is" if len(melted) == len(pieces) else f"{join_words(melted)} {'is' if len(melted) == 1 else 'are'}"
        out.append(f"{who} the frame's color ({name}), so {'they melt' if len(melted) > 1 else 'it melts'} "
                   "into the straps and only the seams show the pattern there")
    for pair in sorted(pairs, key=sorted):
        a, b = sorted(pair)
        ca, cb = theme["colors"][a], theme["colors"][b]
        if pal[ca]["hex"] != pal[cb]["hex"]:
            d = delta_e(pal[ca]["hex"], pal[cb]["hex"])
            if d < CLOSE_DELTA_E:
                out.append(f"{a} and {b} are close ({pal[ca]['name']} / {pal[cb]['name']}, "
                           f"delta E {d:.0f}), and may blur together")
    for c in used_colors(con, theme):
        if len(pal[c]["hexes"]) > 1:
            out.append(f"{pal[c]['name']} is a {SPOOL_WORD[pal[c]['kind']]} spool "
                       f"({' to '.join(pal[c]['hexes'])}); where along the spool its color shifts cannot be "
                       "predicted for a given piece, so the pieces will not come out as drawn")
    return out


SPOOL_WORD = {"gradient": "gradient", "multi": "multi-color", "single": "one-color"}


def plates(con: dict, theme: dict, vols: dict | None) -> list[dict]:
    """One plate per color, the groups of that color on it, with its share of the one-bed slice."""
    by_color: dict[str, list[str]] = {}
    for g in group_ids(con):
        by_color.setdefault(theme["colors"][g], []).append(g)
    total = sum(vols.values()) if vols else None
    out = []
    for color, gs in by_color.items():
        p = {"color": color, "groups": gs}
        if vols:
            share = sum(vols[g] for g in gs) / total
            p["share"] = share
            p["minutes"] = share * con["slice"]["minutes"]
            p["grams"] = share * con["slice"]["grams"]
        out.append(p)
    return sorted(out, key=lambda p: -p.get("share", 0))


def check_one(cid: str, root: Path = THEMES_DIR, pal: dict | None = None, quiet=False, silent=False) -> int:
    con = construction(cid, root)
    pal = pal or palette()
    folder = con["_folder"]
    errors = []
    base_path = folder / "base.svg"
    if not base_path.exists():
        print(f"{cid}: no base.svg; run `themes.py base {cid}`")
        return 1
    base = base_path.read_text()
    faces, _ = parse_base(base)
    pairs = neighbors(con, faces)
    ids = [t["id"] for t in con["themes"]]
    if len(ids) != len(set(ids)):
        errors.append("two themes share an id")
    for t in con["themes"]:
        for p in theme_problems(con, t, pal):
            errors.append(f"{t['id']}: {p}")
    if errors:
        print("\n".join(f"{cid}: {e}" for e in errors))
        return 1
    for t in con["themes"]:
        pic = folder / f"{t['id']}.svg"
        if not pic.exists() or pic.read_text() != draw(con, t, base, pal):
            errors.append(f"{t['id']}.svg is stale or missing; run `themes.py render {cid}`")
    page = root / f"{cid}-themes.md"
    if not page.exists() or page.read_text() != gallery_text(con, pal, pairs):
        errors.append(f"{page.name} is stale or missing; run `themes.py gallery {cid}`")
    if not quiet:
        vols = load_vols(con)
        for t in con["themes"]:
            print(f"{t['id']}: {', '.join(color_word(pal, c) for c in used_colors(con, t))}")
            for w in warnings(con, t, pal, pairs):
                print(f"  warn: {w}")
            for p in plates(con, t, vols):
                cost = f", about {p['minutes']:.0f} min, {p['grams']:.1f} g" if "share" in p else ""
                print(f"  plate {pal[p['color']]['name']}: {', '.join(p['groups'])}{cost}")
    if not silent:
        for e in errors:
            print(f"{cid}: {e}")
    return 1 if errors else 0


def load_vols(con: dict) -> dict | None:
    path = con["_folder"] / "volumes.yaml"
    return load_yaml(path) if path.exists() else None


def used_colors(con: dict, theme: dict) -> list[str]:
    seen = []
    for g in group_ids(con):
        c = theme["colors"][g]
        if c not in seen:
            seen.append(c)
    return seen


def color_word(pal: dict, cid: str, owned: bool = True) -> str:
    """'Caramel (buy)', or with owned=False the name with its finish when it has one worth saying:
    'Gold (silk)'. Basic and matte are the plain lines, so they go unsaid."""
    c = pal[cid]
    if not owned:
        f = c.get("finish")
        return c["name"] + (f" ({f})" if f and f not in ("basic", "matte") else "")
    return f"{c['name']} ({'owned' if c['owned'] else 'buy'})"


def all_constructions(root: Path = THEMES_DIR) -> list[str]:
    return sorted(p.name for p in root.iterdir() if (p / "themes.yaml").exists()) if root.exists() else []


# ---------------------------------------------------------------- helpers that suggest


def suggest(con: dict, helper: str, colors: list[str], pal: dict) -> dict:
    gids = [g["id"] for g in con["groups"]]
    if helper == "one-color":
        c = colors[0]
        mapping = {g: c for g in gids} | {FRAME: c}
        name = f"All {pal[c]['name']}"
    elif helper == "alternate":
        # Rings out from the middle take the colors in turn; the frame takes the last color given
        # when there are three or more, else the first one not used by the outer ring.
        ring_colors = colors[:-1] if len(colors) >= 3 else colors
        mapping = {g: ring_colors[i % len(ring_colors)] for i, g in enumerate(gids)}
        mapping[FRAME] = colors[-1] if len(colors) >= 3 else colors[(len(gids)) % len(colors)]
        name = "Alternate " + " / ".join(pal[c]["name"] for c in colors)
    elif helper == "match-trays":
        owned = [k for k, v in pal.items() if v["owned"]]
        # The darkest tray takes the frame; the others go round the rings in turn.
        owned.sort(key=lambda k: lab(pal[k]["hex"])[0])
        mapping = {FRAME: owned[0]}
        rest = owned[1:]
        for i, g in enumerate(gids):
            mapping[g] = rest[i % len(rest)]
        name = "The loaded trays"
    else:
        raise SystemExit(f"unknown helper {helper}")
    return {"id": re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"), "name": name,
            "mood": "(write one line)", "made_by": f"suggest --helper {helper}", "colors": mapping}


def palette_id_for(e: dict) -> str:
    """The id a catalog color gets on the buy list: its name, with the line's finish in front
    for every line but Basic and Matte (Silk Blue is not Basic Blue)."""
    name = bambu.slug(e["name"])
    if e["line"] in ("PLA Basic", "PLA Matte"):
        return name
    return bambu.slug(e["line"].removeprefix("PLA ")) + "-" + name


def gradient_candidates(pal: dict, cat: dict, lines: list[str]) -> list[dict]:
    """Every one-color, opaque catalog color in these lines, under its palette id when the buy
    list has it, plus the owned trays. A tray whose hex a candidate shares replaces it."""
    by_code = {str(c["code"]): k for k, c in pal.items() if not c["owned"]}
    trays = {c["hex"]: k for k, c in pal.items() if c["owned"]}
    out = [{"id": k, "hex": c["hex"], "name": c["name"], "owned": True, "entry": None}
           for k, c in pal.items() if c["owned"]]
    for e in cat["colors"]:
        if e["line"] not in lines or e["kind"] != "single" or bambu.alpha(e["hexes"][0]) < 1:
            continue
        h = bambu.opaque(e["hexes"][0])
        if h in trays:
            continue
        cid = by_code.get(e["code"], palette_id_for(e))
        out.append({"id": cid, "hex": h, "name": e["name"], "owned": False, "entry": e,
                    "listed": e["code"] in by_code})
    return out


def chroma(hexstr: str) -> float:
    return math.hypot(*lab(hexstr)[1:])


def lch_lerp(a: str, b: str, t: float) -> tuple:
    """The point a fraction t of the way from a to b, stepping lightness, colorfulness and hue
    each on its own (the short way round the hue circle), returned as L*a*b*. A straight line in
    L*a*b* between two blues dips toward gray in the middle; this keeps the steps blue."""
    (la, aa, ba), (lb, ab, bb) = lab(a), lab(b)
    ca, cb = math.hypot(aa, ba), math.hypot(ab, bb)
    ha, hb = math.atan2(ba, aa), math.atan2(bb, ab)
    if ca < 1e-6:
        ha = hb
    if cb < 1e-6:
        hb = ha
    dh = (hb - ha + math.pi) % (2 * math.pi) - math.pi
    L, C, H = la + (lb - la) * t, ca + (cb - ca) * t, ha + dh * t
    return (L, C * math.cos(H), C * math.sin(H))


# What a ring costs for taking the same color as the ring inside it, in delta E: a repeat is
# allowed, but a different real color up to this much farther from the step wins over it.
REPEAT_COST = 12.0
# A gradient runs one way in lightness; a ring may be this much (L*) the wrong way and no more.
LIGHTNESS_SLACK = 3.0


def best_path(pool: list[dict], targets: list[tuple], ends: list[dict]) -> list[dict]:
    """The colors for the rings between the ends: each near its target step, and no ring the
    same as the one inside it unless nothing else is close. Every sequence is weighed (summed
    distance to the targets, plus REPEAT_COST per repeat), by dynamic programming over the
    rings, so a repeat lands where it costs least."""
    if not targets:
        return []
    labs = [lab(c["hex"]) for c in pool]
    way = 1 if lab(ends[1]["hex"])[0] >= lab(ends[0]["hex"])[0] else -1

    def rep(a: dict, b: dict) -> float:
        """The cost of ring b following ring a: a repeat costs REPEAT_COST, and a step back
        the wrong way in lightness (lighter in a light-to-dark run) is ruled out."""
        if (lab(b["hex"])[0] - lab(a["hex"])[0]) * way < -LIGHTNESS_SLACK:
            return math.inf
        return REPEAT_COST if a["hex"] == b["hex"] else 0.0

    cost = [math.dist(labs[j], targets[0]) + rep(ends[0], c) for j, c in enumerate(pool)]
    back = []
    for t in targets[1:]:
        row, prev = [], []
        for j, c in enumerate(pool):
            k = min(range(len(pool)), key=lambda k: cost[k] + rep(pool[k], c))
            row.append(cost[k] + rep(pool[k], c) + math.dist(labs[j], t))
            prev.append(k)
        cost, back = row, back + [prev]
    j = min(range(len(pool)), key=lambda j: cost[j] + rep(pool[j], ends[1]))
    path = [j]
    for prev in reversed(back):
        j = prev[j]
        path.append(j)
    return [pool[j] for j in reversed(path)]


def gradient(con: dict, frm: str, to: str, pal: dict, cat: dict, lines: list[str] | None = None,
             reverse: bool = False) -> tuple[dict, list[dict]]:
    """A theme that runs from one color in the middle to another on the outer ring.

    The rings take evenly spaced steps between the two colors (lightness, colorfulness and hue
    each stepped on its own), and each step takes a real color among the candidates (catalog
    colors in `lines`, by default the ends' own lines so the finish stays even, and the trays):
    near its step, running one way in lightness, and repeating the ring inside it only when no
    other color is close (best_path). Between two colorful ends no step is a gray. The frame
    takes the neutral (gray, black or white) farthest from the outer ring, so the edge never
    melts into the frame.
    `--reverse` swaps the ends. Returns the theme and the catalog colors it needs added to the
    buy list.
    """
    asked = f"--from {frm} --to {to}" + (" --reverse" if reverse else "") + \
        (f" --lines \"{','.join(lines)}\"" if lines else "")
    if reverse:
        frm, to = to, frm
    gids = [g["id"] for g in con["groups"]]
    ends = [resolve_color(x, pal, cat) for x in (frm, to)]
    if lines is None:
        lines = sorted({e["entry"]["line"] for e in ends if e["entry"]}) or ["PLA Basic", "PLA Matte"]
    cands = gradient_candidates(pal, cat, lines)
    for e in ends:
        if all(c["id"] != e["id"] for c in cands):
            cands.append(e)
    neutrals = [c for c in cands if chroma(c["hex"]) < NEUTRAL_CHROMA]
    # Between two colorful ends the steps stay colorful: a gray ring in a blue gradient reads
    # as a gap, not a step.
    colorful = all(chroma(e["hex"]) >= NEUTRAL_CHROMA for e in ends)
    pool = [c for c in cands if c not in neutrals] if colorful else cands
    n = len(gids)
    targets = [lch_lerp(ends[0]["hex"], ends[1]["hex"], i / (n - 1)) for i in range(n)]
    steps = [ends[0]] + best_path(pool, targets[1:-1], ends) + [ends[1]]
    outer = steps[-1]["hex"]
    frame = max(neutrals, key=lambda c: (round(delta_e(c["hex"], outer)), c["owned"]))
    mapping = {g: s["id"] for g, s in zip(gids, steps)} | {FRAME: frame["id"]}
    name = f"{ends[0]['name']} to {ends[1]['name']}"
    add, seen = [], set(pal)
    for c in steps + [frame]:
        if c["id"] not in seen:
            seen.add(c["id"])
            e = c["entry"]
            add.append({"id": c["id"], "hex": bambu.opaque(e["hexes"][0]), "name": e["name"],
                        "line": e["line"], "code": e["code"]})
    theme = {"id": bambu.slug(name), "name": name, "mood": "(write one line)",
             "made_by": f"suggest --helper gradient {asked}", "colors": mapping}
    return theme, add


def resolve_color(x: str, pal: dict, cat: dict) -> dict:
    """A palette id, or a catalog product code, as a gradient candidate."""
    if x in pal:
        c = pal[x]
        e = None if c["owned"] else cat["by_code"].get(str(c["code"]))
        return {"id": x, "hex": c["hex"], "name": c["name"], "owned": c["owned"], "entry": e}
    e = cat["by_code"].get(x)
    if e is None:
        raise SystemExit(f"{x} is neither a palette color id nor a catalog product code")
    if len(e["hexes"]) > 1:
        raise SystemExit(f"{x} ({e['name']}) is a spool with several hexes; a gradient end needs one color")
    return {"id": palette_id_for(e), "hex": bambu.opaque(e["hexes"][0]), "name": e["name"],
            "owned": False, "entry": e}


# ---------------------------------------------------------------- gallery


def reviews_for(con: dict) -> dict:
    path = con["_folder"] / "reviews.yaml"
    if not path.exists():
        return {}
    data = load_yaml(path) or {}
    return {r["theme"]: r for r in data.get("reviews", [])}


def persona_names() -> dict:
    names = {}
    if PERSONAS.exists():
        for line in PERSONAS.read_text().splitlines():
            m = re.match(r"\|\s*`([a-z0-9-]+)`\s*\|\s*([^|]+?)\s*\|", line)
            if m:
                names[m.group(1)] = m.group(2)
    return names


def overall(review: dict) -> float:
    scores = [s["score"] for s in review["scores"].values()]
    return sum(scores) / len(scores)


def gallery_text(con: dict, pal: dict, pairs: set[frozenset]) -> str:
    cid = con["_folder"].name
    vols = load_vols(con)
    revs = reviews_for(con)
    names = persona_names()

    def sort_key(t):
        r = revs.get(t["id"])
        fresh = r and r.get("coloring") == theme_hash(t)
        return (-(overall(r) if fresh else -1), t["name"])

    themes = sorted(con["themes"], key=sort_key)
    s = con["slice"]
    out = [
        "---",
        "status: built",
        "generated: true",
        f"construction: {con['construction']}",
        "produced-by: .claude/skills/color-themes/scripts/themes.py gallery " + cid,
        "---",
        "",
        f"# {con['short']}: color themes to mix and match",
        "",
        f"> Generated from [{cid}/themes.yaml]({cid}/themes.yaml) and [{cid}/reviews.yaml]({cid}/reviews.yaml)"
        f" by `themes.py gallery {cid}`. Edit the data, not this page.",
        "",
        con["about"].strip(),
        "",
        "**How to read a theme.**",
        "",
        "- **Colors.** *Owned* means it is on a tray today; *buy* means a Bambu filament we do not have. "
        "Every buy color is checked against Bambu Studio's own color list, the "
        "[catalog](bambu-color-catalog.md). A hex is the maker's label for the color, not a measurement.",
        "- **Finishes are drawn, roughly.** Silk and metal get a white sheen, sparkle flecks, and a "
        "translucent color is half see-through. Matte and basic are flat, and a tray on the printer "
        "is drawn flat because the printer reports only its hex. A spool with two or more hexes (a "
        "gradient or multi-color spool) is drawn as its hexes, but where along the spool its color "
        "shifts cannot be predicted for a given piece.",
        f"- **Plates.** Each color prints as its own one-color plate, and the frame rides on the plate "
        f"of its color. Minutes and grams split [{s['plate']}](../../plates/{s['plate']}.md)'s one-bed slice "
        f"({s['minutes']} min, {s['grams']} g, everything on one bed) by each group's share of the plastic. "
        "So they are estimates: minutes do not follow volume exactly, and each extra plate adds a "
        "start-up that has not been measured. A plate of only a few minutes' plastic will take "
        "longer than its share says, by that unmeasured start-up.",
        "- **Scores.** Simulated opinions from the review-theme skill's personas, out of 5, not "
        "customer research. They are one model's reading of the picture through each persona's eyes, "
        "useful for ranking ideas, not for deciding what sells.",
        "",
        "| Theme | Score | Plates | Buy |",
        "|---|---|---|---|",
    ]
    for t in themes:
        r = revs.get(t["id"])
        fresh = r and r.get("coloring") == theme_hash(t)
        score = f"{overall(r):.1f}" if fresh else "not reviewed"
        buys = [color_word(pal, c, owned=False) for c in used_colors(con, t) if not pal[c]["owned"]]
        anchor = re.sub(r"[^a-z0-9 -]", "", t["name"].lower()).replace(" ", "-")
        out.append(f"| [{t['name']}](#{anchor}) | {score} | {len(plates(con, t, vols))} | "
                   f"{', '.join(buys) or 'nothing'} |")
    out.append("")
    for t in themes:
        r = revs.get(t["id"])
        fresh = r and r.get("coloring") == theme_hash(t)
        out += [f"## {t['name']}", "", f"*{t['mood'].strip()}*", "",
                f"![{con['short']} in the {t['name']} theme]({cid}/{t['id']}.svg)", ""]
        out += ["| Group | Color | |", "|---|---|---|"]
        labels = {g["id"]: g["label"] for g in con["groups"]} | {FRAME: "the frame (the straps)"}
        for g in group_ids(con):
            c = pal[t["colors"][g]]
            hexes = " ".join(f"`{h}`" for h in c["hexes"])
            where = "owned" if c["owned"] else f"buy, {c['line']}"
            out.append(f"| {labels[g]} | {c['name']} {hexes} | {where} |")
        out.append("")
        ws = warnings(con, t, pal, pairs)
        if ws:
            out += ["**Heads-up:** " + "; ".join(ws) + ".", ""]
        ps = plates(con, t, vols)
        cost = ""
        if vols:
            mins = sum(p["minutes"] for p in ps)
            grams = sum(p["grams"] for p in ps)
            cost = f", about {mins:.0f} min and {grams:.0f} g in all"
            if len(ps) > 1:
                cost += f", plus {len(ps) - 1} start-up{'s' if len(ps) > 2 else ''} not measured"
        out.append(f"**Plates:** {len(ps)}{cost}.")
        out.append("")
        for p in ps:
            line = f"- {pal[p['color']]['name']}: {join_words([short_label(labels[g]) for g in p['groups']])}"
            if "share" in p:
                line += f" (about {p['minutes']:.0f} min, {p['grams']:.1f} g)"
            out.append(line)
        out.append("")
        if fresh:
            out += [f"**Scores:** {overall(r):.1f} of 5. {r['overall'].strip()}", "",
                    "| Persona | Score | Why |", "|---|---|---|"]
            for pid, sc in r["scores"].items():
                out.append(f"| {names.get(pid, pid)} | {sc['score']} | {sc['why'].strip()} |")
            out.append("")
        elif r:
            out += ["**Scores:** the review was for an earlier coloring of this theme; review it again.", ""]
        else:
            out += ["**Scores:** not reviewed yet.", ""]
    return "\n".join(out).rstrip() + "\n"


def cmd_gallery(cid: str) -> None:
    con = construction(cid)
    pal = palette()
    faces, _ = parse_base((con["_folder"] / "base.svg").read_text())
    page = THEMES_DIR / f"{cid}-themes.md"
    page.write_text(gallery_text(con, pal, neighbors(con, faces)))
    print(page.relative_to(ROOT))


# ---------------------------------------------------------------- self-test


FIXTURE_BASE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 10 10" width="10" height="10">
  <g class="coaster-faces">
    <polygon points="0,0 1,0 1,1 0,1" fill="{a}" />
    <polygon points="1,0 2,0 2,1 1,1" fill="{b}" />
    <polygon points="3,0 4,0 4,1 3,1" fill="{a}" />
  </g>
  <line x1="0" y1="0" x2="4" y2="0" stroke="#333333" stroke-width="1.0000" stroke-linecap="round" />
</svg>
"""


def self_test() -> int:
    fails = []

    def expect(cond, what):
        if not cond:
            fails.append(what)

    # 1. Every buy hex is Bambu's own, from the catalog; one wrong digit must fail.
    cat = bambu.load_catalog()
    pal = palette(cat=cat)
    expect(len(cat["colors"]) == 314, f"catalog: expected 314 colors, read {len(cat['colors'])}")
    for k, c in pal.items():
        if not c["owned"]:
            for p in buy_problems(c, cat):
                fails.append(f"buy {k}: {p}")
    bad = {**pal["caramel"], "hexes": ["#AE835C"]}
    expect(any("differs" in p for p in buy_problems(bad, cat)), "a one-digit-off buy hex was not caught")
    expect(buy_problems({**pal["caramel"], "name": "Caramell"}, cat), "a misspelled buy name was not caught")
    expect(buy_problems({**pal["caramel"], "code": "99999"}, cat), "a code not in the catalog was not caught")
    abs_entry = next(e for e in cat["colors"] if e["line"] == "ABS")
    expect(any("not a line a coaster" in p for p in buy_problems(
        {"code": abs_entry["code"], "name": abs_entry["name"], "line": "ABS",
         "hexes": [bambu.opaque(h) for h in abs_entry["hexes"]]}, cat)), "an ABS color was let onto the buy list")
    multi = [c for c in pal.values() if len(c["hexes"]) > 1]
    for c in multi:
        expect(c["hex"] == spool_mean(c["hexes"]), f"{c['id']}: a multi-hex color's check hex is not its mean")

    # 2. Color math: black/white is far, a color with itself is zero, close shades warn.
    expect(delta_e("#000000", "#FFFFFF") > 99, "delta E black/white should be about 100")
    expect(delta_e("#F5547C", "#F5547C") == 0, "delta E of a color with itself")
    expect(delta_e("#F5547C", "#F55A74") < CLOSE_DELTA_E, "Hot Pink vs Pink should count as close")

    # 3. Neighbors, warnings and plates on a three-face fixture: a|b touch, the third a is alone.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "fx").mkdir()
        con_data = {
            "construction": "fixture", "short": "Fixture", "about": "A fixture.",
            "source": {"frame": "bikar:none", "pieces": "bikar:none"},
            "params": {}, "piece_params": {},
            "slice": {"plate": "none", "minutes": 100, "grams": 10},
            "groups": [{"id": "a", "piece": "A", "orbits": [0], "label": "the a"},
                       {"id": "b", "piece": "B", "orbits": [1], "label": "the b"}],
            "themes": [
                {"id": "two", "name": "Two", "mood": "m", "colors": {"a": "pink", "b": "black", "frame": "green"}},
                {"id": "same", "name": "Same", "mood": "m", "colors": {"a": "pink", "b": "pink", "frame": "green"}},
            ],
        }
        (root / "fx" / "themes.yaml").write_text(yaml.safe_dump(con_data))
        (root / "fx" / "base.svg").write_text(FIXTURE_BASE.format(a=marker_hex(0), b=marker_hex(1)))
        (root / "fx" / "volumes.yaml").write_text("a: 30\nb: 10\nframe: 60\n")
        con = construction("fx", root)
        faces, straps = parse_base((root / "fx" / "base.svg").read_text())
        expect(len(faces) == 3 and len(straps) == 1, f"fixture parse: {len(faces)} faces, {len(straps)} lines")
        pairs = neighbors(con, faces)
        expect(frozenset(("a", "b")) in pairs, "a and b share an edge and were not neighbors")
        two, same = con["themes"]
        expect(not warnings(con, two, pal, pairs), "pink next to black should not warn")
        expect(not warnings(con, same, pal, pairs),
               "two pink pieces with a green strap between them should not warn")
        melt = {**same, "colors": {"a": "green", "b": "pink", "frame": "green"}}
        melt_w = warnings(con, melt, pal, pairs)
        expect(any(w.startswith("a is the frame's color") for w in melt_w),
               f"a piece in the frame's color did not warn (the by-design failure): {melt_w}")
        all_w = warnings(con, {**same, "colors": {"a": "green", "b": "green", "frame": "green"}}, pal, pairs)
        expect(any(w.startswith("every piece is") for w in all_w), f"one color for all did not warn: {all_w}")
        close_w = warnings(con, {**same, "colors": {"a": "latte-brown", "b": "desert-tan", "frame": "black"}},
                           pal, pairs)
        expect(any("are close" in w for w in close_w), f"Latte Brown next to Desert Tan did not warn: {close_w}")
        ps = plates(con, two, load_vols(con))
        expect(len(ps) == 3 and abs(sum(p["grams"] for p in ps) - 10) < 1e-9,
               "three colors should make three plates whose grams add to the slice's")
        expect(len(plates(con, same, load_vols(con))) == 2, "two colors should make two plates")
        expect(abs(ps[0]["minutes"] - 60) < 1e-9, "the frame is 60% of the plastic, so 60 of 100 minutes")
        # A color not in the palette, and a missing group, are refused.
        broken = {**two, "colors": {"a": "#FF0000", "b": "black"}}
        probs = theme_problems(con, broken, pal)
        expect(any("not a color" in p for p in probs), "a raw hex was accepted as a color")
        expect(any("no color for" in p for p in probs), "a missing frame color was accepted")
        # Stale files fail the check; fresh ones pass.
        expect(check_one("fx", root, pal, quiet=True, silent=True) == 1, "missing pictures and gallery should fail")
        base = (root / "fx" / "base.svg").read_text()
        for t in con["themes"]:
            (root / "fx" / f"{t['id']}.svg").write_text(draw(con, t, base, pal))
        (root / "fx-themes.md").write_text(gallery_text(con, pal, pairs))
        expect(check_one("fx", root, pal, quiet=True, silent=True) == 0, "fresh pictures and gallery should pass")
        (root / "fx" / "two.svg").write_text("stale")
        expect(check_one("fx", root, pal, quiet=True, silent=True) == 1, "a stale picture should fail")

    # 4. The marker palette lands before the coaster block, and a file with a palette is refused.
    src = "pattern P on S\n  rotate 6\n\ncoaster Coaster\n  outline pattern\n"
    con = {"groups": [{"id": "a", "orbits": [0, 2]}, {"id": "b", "orbits": [1]}]}
    out = with_marker_palette(src, con)
    expect(out.index("palette themes") < out.index("coaster Coaster"), "palette after the coaster block")
    expect(out.count("fill void where orbit") == 3, "one fill line per orbit")
    try:
        with_marker_palette(out, con)
        fails.append("a file with a palette was not refused")
    except SystemExit:
        pass

    # 5. The helpers color every group.
    gcon = {"groups": [{"id": g} for g in "abcde"]}
    for helper, colors in (("one-color", ["green"]), ("alternate", ["pink", "black"]),
                           ("alternate", ["pink", "green", "black"]), ("match-trays", [])):
        t = suggest(gcon, helper, colors, pal)
        expect(set(t["colors"]) == set("abcde") | {FRAME}, f"{helper} left a group uncolored")

    # 6. The gradient: its ends are the colors asked for, it gets darker step by step from a light
    #    middle, every step is a real catalog color, --reverse swaps it, and the frame stands
    #    apart from the outer ring.
    t, add = gradient(gcon, "ice-blue", "dark-blue", pal, cat)
    ring = [t["colors"][g] for g in "abcde"]
    full = pal | {c["id"]: {"hex": c["hex"]} for c in add}
    ls = [lab(full[c]["hex"])[0] for c in ring]
    expect(ring[0] == "ice-blue" and ring[-1] == "dark-blue", f"gradient ends: {ring}")
    expect(all(x >= y for x, y in zip(ls, ls[1:])), f"ice to dark blue should darken ring by ring: {ring}")
    expect(all(c["code"] in cat["by_code"] for c in add), "a gradient step is not a catalog color")
    expect(delta_e(full[t["colors"][FRAME]]["hex"], full["dark-blue"]["hex"]) > 50,
           f"the frame ({t['colors'][FRAME]}) melts into the dark outer ring")
    r, _ = gradient(gcon, "ice-blue", "dark-blue", pal, cat, reverse=True)
    expect([r["colors"][g] for g in "abcde"][::-1] == ring, "--reverse is not the same rings outside in")
    expect(delta_e(full[r["colors"][FRAME]]["hex"], full["ice-blue"]["hex"]) > 50,
           f"the reversed frame ({r['colors'][FRAME]}) melts into the light outer ring")

    # 7. Finishes: a flat color draws as before; silk adds a sheen, sparkle flecks, translucent
    #    a see-through fill, and a two-hex spool its own gradient and a heads-up.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "fx").mkdir()
        (root / "fx" / "themes.yaml").write_text(yaml.safe_dump({**con_data, "themes": []}))
        (root / "fx" / "base.svg").write_text(FIXTURE_BASE.format(a=marker_hex(0), b=marker_hex(1)))
        fcon = construction("fx", root)
        base = (root / "fx" / "base.svg").read_text()
        fpal = pal | {
            "silk-x": {**pal["caramel"], "id": "silk-x", "finish": "silk", "line": "PLA Silk"},
            "spark-x": {**pal["caramel"], "id": "spark-x", "finish": "sparkle"},
            "clear-x": {**pal["caramel"], "id": "clear-x", "finish": "translucent", "alpha": 128 / 255},
            "duo-x": {**pal["caramel"], "id": "duo-x", "hexes": ["#FF9425", "#C16784"], "kind": "multi",
                      "hex": spool_mean(["#FF9425", "#C16784"]), "finish": "silk"},
        }
        flat = draw(fcon, {"name": "F", "colors": {"a": "pink", "b": "black", "frame": "green"}}, base, fpal)
        expect("<defs>" not in flat and 'class="finish"' not in flat, "a flat theme grew finish markup")
        silk = draw(fcon, {"name": "S", "colors": {"a": "silk-x", "b": "spark-x", "frame": "silk-x"}}, base, fpal)
        expect("f-silk-x-sheen" in silk and "frame-sheen" in silk, "silk drew no sheen")
        expect("f-spark-x-flecks" in silk, "sparkle drew no flecks")
        clear = draw(fcon, {"name": "C", "colors": {"a": "clear-x", "b": "black", "frame": "green"}}, base, fpal)
        expect('fill-opacity="0.5"' in clear, "translucent drew opaque")
        duo_t = {"name": "D", "colors": {"a": "duo-x", "b": "black", "frame": "duo-x"}}
        duo = draw(fcon, duo_t, base, fpal)
        expect("f-duo-x-spool" in duo and "frame-spool-1" in duo, "a two-hex spool drew as one color")
        expect(any("cannot be predicted" in w for w in warnings(fcon, duo_t, fpal, set())),
               "a two-hex spool gave no heads-up")

    for f in fails:
        print(f"self-test FAIL: {f}")
    print("self-test: " + ("ok" if not fails else f"{len(fails)} failed"))
    return 1 if fails else 0


# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    for name in ("base", "measure", "gallery"):
        sub.add_parser(name).add_argument("id")
    r = sub.add_parser("render")
    r.add_argument("id")
    r.add_argument("--png", help="also write a PNG of each picture here, to look at")
    c = sub.add_parser("check")
    c.add_argument("id", nargs="?")
    c.add_argument("--all", action="store_true")
    c.add_argument("--quiet", action="store_true")
    s = sub.add_parser("suggest")
    s.add_argument("id")
    s.add_argument("--helper", required=True, choices=["match-trays", "alternate", "one-color", "gradient"])
    s.add_argument("--colors", default="", help="palette color ids, comma-separated")
    s.add_argument("--from", dest="frm", help="gradient: the middle's color (a palette id or a catalog code)")
    s.add_argument("--to", help="gradient: the outer ring's color")
    s.add_argument("--reverse", action="store_true", help="gradient: swap the ends")
    s.add_argument("--lines", help="gradient: catalog lines to pick from, comma-separated "
                                   "(default: the ends' own lines)")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if a.cmd == "base":
        cmd_base(a.id)
    elif a.cmd == "measure":
        cmd_measure(a.id)
    elif a.cmd == "render":
        cmd_render(a.id, a.png)
    elif a.cmd == "gallery":
        cmd_gallery(a.id)
    elif a.cmd == "check":
        ids = all_constructions() if a.all else [a.id]
        if not ids or ids == [None]:
            ap.error("check needs an id or --all")
        return max(check_one(i, quiet=a.quiet) for i in ids)
    elif a.cmd == "suggest":
        con = construction(a.id)
        pal = palette()
        colors = [x for x in a.colors.split(",") if x]
        for x in colors:
            if x not in pal:
                raise SystemExit(f"{x} is not a palette color id")
        if a.helper in ("one-color", "alternate") and not colors:
            ap.error(f"--helper {a.helper} needs --colors")
        add = []
        if a.helper == "gradient":
            if not (a.frm and a.to):
                ap.error("--helper gradient needs --from and --to")
            lines = [x.strip() for x in a.lines.split(",")] if a.lines else None
            t, add = gradient(con, a.frm, a.to, pal, bambu.load_catalog(), lines, a.reverse)
        else:
            t = suggest(con, a.helper, colors, pal)
        faces, _ = parse_base((con["_folder"] / "base.svg").read_text())
        print(yaml.safe_dump([t], sort_keys=False).rstrip())
        if add:
            print("# add to palette.yaml buy: first (from the catalog)")
            for c in add:
                print("#   - " + yaml.safe_dump(c, default_flow_style=True, sort_keys=False, width=300).strip())
        full = pal | {c["id"]: {**c, "hexes": [c["hex"]], "owned": False, "kind": "single",
                                "finish": bambu.finish_of(c["line"]), "alpha": 1.0} for c in add}
        for w in warnings(con, t, full, neighbors(con, faces)):
            print(f"# warn: {w}")
    else:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
