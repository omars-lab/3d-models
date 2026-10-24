#!/usr/bin/env python3
"""Where pins can go on a split coaster, ring by ring round its centre, as a picture to mark up.

A rosette repeats round its middle, so a pin that fits at one point of a ring fits at
the same point of every repeat. This finds every point on the cut face with room for a
pin, groups them into rings by their distance from the centre, gives each ring a letter,
and draws the face with each ring's pins in its own color and a label: letter, radius,
how many pins, and the turn of the first one. Omar marks the picture ("keep A and D, add
C"), and the kept rings become the coaster's `rings` list.

    python3 .claude/skills/place-pins/scripts/ring_map.py LOWER.stl --z 2.05 --stud 1.2 --gap 0.25 --out map.png
    python3 .claude/skills/place-pins/scripts/ring_map.py LOWER.stl --z 0.5 ...   # the plain strap, as with pin bosses

`--z` is the height the face is cut at. Just under the halves' cut (2.05 for a 4.4 mm
coaster) is the face as it is today, the hidden groove for the pieces' rims taken off it.
Low in the lower half (0.5) is the plain strap: the room a pin has once the groove is
filled round it (bikar's pin bosses).
"""
from __future__ import annotations

import argparse
import math
import pathlib
import subprocess
import sys

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "split_sites.py").exists())
sys.path.insert(0, str(ROOT / "tools"))
from split_sites import clearances, inside_points, pick, slice_at  # noqa: E402

COLORS = ["#d7301f", "#2171b5", "#238b45", "#6a51a3", "#d94801", "#c51b7d", "#01665e", "#8c510a"]


def rings_of(sites, cx: float, cy: float, tol: float):
    """Group sites into rings: sorted by radius, a new ring wherever the radius jumps by more than `tol`."""
    polar = sorted((math.hypot(x - cx, y - cy), math.degrees(math.atan2(y - cy, x - cx)) % 360, x, y)
                   for x, y, _ in sites)
    rings: list[list[tuple[float, float, float, float]]] = []
    for p in polar:
        if rings and p[0] - rings[-1][-1][0] <= tol:
            rings[-1].append(p)
        else:
            rings.append([p])
    out = []
    for i, ring in enumerate(rings):
        n = len(ring)
        r = sum(p[0] for p in ring) / n
        first = min(p[1] % (360 / n) for p in ring) if n else 0.0
        out.append({"letter": chr(ord("A") + i), "r": r, "n": n, "turn": first, "pts": ring})
    return out


def svg(segs, rings, cx, cy, title: str) -> str:
    xs = [s[0] for s in segs] + [s[2] for s in segs]
    ys = [s[1] for s in segs] + [s[3] for s in segs]
    half = max(max(xs) - cx, cx - min(xs), max(ys) - cy, cy - min(ys)) + 2
    sc = 9.0
    side = 2 * half * sc
    legend = 26 * (len(rings) + 2)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{side:.0f}" height="{side + legend:.0f}">',
         '<rect width="100%" height="100%" fill="#000"/>']

    def X(x):
        return (x - cx + half) * sc

    def Y(y):
        return (cy - y + half) * sc

    for ax, ay, bx, by in segs:
        o.append(f'<line x1="{X(ax):.1f}" y1="{Y(ay):.1f}" x2="{X(bx):.1f}" y2="{Y(by):.1f}" '
                 'stroke="#9a9a9a" stroke-width="1.5"/>')
    for i, ring in enumerate(rings):
        col = COLORS[i % len(COLORS)]
        o.append(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{ring["r"] * sc:.1f}" fill="none" '
                 f'stroke="{col}" stroke-width="1" stroke-dasharray="6 6" opacity="0.7"/>')
        for _, _, x, y in ring["pts"]:
            o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="7" fill="{col}" stroke="#fff" stroke-width="1.5"/>')
        x, y = ring["pts"][0][2], ring["pts"][0][3]
        o.append(f'<text x="{X(x) + 9:.1f}" y="{Y(y) - 9:.1f}" font-family="sans-serif" font-size="22" '
                 f'font-weight="bold" fill="#fff" stroke="#000" stroke-width="3" paint-order="stroke">{ring["letter"]}</text>')
    y0 = side + 30
    o.append(f'<text x="12" y="{y0}" font-family="sans-serif" font-size="20" fill="#fff">{title}</text>')
    for i, ring in enumerate(rings):
        col = COLORS[i % len(COLORS)]
        o.append(f'<text x="12" y="{y0 + 26 * (i + 1)}" font-family="sans-serif" font-size="20" fill="{col}">'
                 f'{ring["letter"]}: {ring["r"]:.1f} mm out, {ring["n"]} pins, first at {ring["turn"]:.0f}°</text>')
    o.append("</svg>")
    return "\n".join(o)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("stl")
    ap.add_argument("--z", type=float, required=True, help="height the face is cut at, mm")
    ap.add_argument("--stud", type=float, default=1.2, help="pin diameter, mm")
    ap.add_argument("--gap", type=float, default=0.25, help="how much wider the hole is than the pin, mm")
    ap.add_argument("--wall", type=float, default=0.9, help="plastic left round the hole, mm (bikar's socket wall)")
    ap.add_argument("--spacing", type=float, default=4.0, help="least distance between two pins, mm")
    ap.add_argument("--tol", type=float, default=0.75, help="pins this close in radius share a ring, mm")
    ap.add_argument("--step", type=float, default=0.2, help="sample grid, mm")
    ap.add_argument("--out", required=True, help="the picture, .png (an .svg is written beside it)")
    a = ap.parse_args(argv)

    segs = slice_at(a.stl, a.z)
    if not segs:
        sys.exit(f"nothing at z={a.z}")
    need = (a.stud + a.gap) / 2 + a.wall
    cl = clearances(segs, inside_points(segs, a.step), need + 1.0)
    xs = [s[0] for s in segs] + [s[2] for s in segs]
    ys = [s[1] for s in segs] + [s[3] for s in segs]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    rings = rings_of(pick(cl, need, a.spacing), cx, cy, a.tol)
    title = f"cut at {a.z} mm: {a.stud} mm pins, {len(rings)} rings"
    out = pathlib.Path(a.out)
    out.with_suffix(".svg").write_text(svg(segs, rings, cx, cy, title))
    subprocess.run(["rsvg-convert", "-o", str(out), str(out.with_suffix(".svg"))], check=True)
    print(f"z={a.z} stud={a.stud} need_room_mm={need:.3f} rings={len(rings)}")
    for ring in rings:
        print(f"ring={ring['letter']} radius_mm={ring['r']:.2f} pins={ring['n']} first_turn_deg={ring['turn']:.1f}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
