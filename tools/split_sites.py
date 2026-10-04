#!/usr/bin/env python3
"""Where can a stud-and-socket pair go when a model is cut flat at height z?

Slices a binary STL at z, finds every point of the cut face that has room for a
socket of a given diameter plus a wall around it, picks sites greedily (roomiest
first, a minimum spacing apart) and draws the cut face with the sites on it.

    python3 tools/split_sites.py MODEL.stl --z 2.2 --svg out.svg
    python3 tools/split_sites.py MODEL.stl --z 2.2 --sweep 1.5,2,2.5,3,4.8

A site needs clearance >= (stud + gap) / 2 + wall, the clearance being the
distance from the point to the nearest edge of the cut face. Pure stdlib, so it
runs anywhere the repo's other tools do (see tools/edge_stairs.py). Feeds
docs/design/pieces/split-with-studs-design.md.
"""
from __future__ import annotations

import argparse
import math
import struct
import sys
from collections import defaultdict

Seg = tuple[float, float, float, float]


def read_stl(path: str):
    with open(path, "rb") as f:
        data = f.read()
    if data[:5] == b"solid" and b"facet" in data[:400]:
        sys.exit("ASCII STL not supported; render with --format stl (binary)")
    (n,) = struct.unpack_from("<I", data, 80)
    off = 84
    for _ in range(n):
        v = struct.unpack_from("<12fH", data, off)
        off += 50
        yield (v[3:6], v[6:9], v[9:12])


def slice_at(path: str, z: float) -> list[Seg]:
    segs: list[Seg] = []
    for tri in read_stl(path):
        pts = []
        for i in range(3):
            a, b = tri[i], tri[(i + 1) % 3]
            if (a[2] - z) * (b[2] - z) < 0:
                t = (z - a[2]) / (b[2] - a[2])
                pts.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
        if len(pts) == 2:
            segs.append((pts[0][0], pts[0][1], pts[1][0], pts[1][1]))
    return segs


def inside_points(segs: list[Seg], step: float):
    """Scanline fill: even-odd crossings of each row against the slice segments."""
    ys = [s[1] for s in segs] + [s[3] for s in segs]
    xs = [s[0] for s in segs] + [s[2] for s in segs]
    y0, y1, x0 = min(ys), max(ys), min(xs)
    rows: dict[int, list[Seg]] = defaultdict(list)
    for s in segs:
        lo, hi = sorted((s[1], s[3]))
        for r in range(int((lo - y0) / step), int((hi - y0) / step) + 2):
            rows[r].append(s)
    out = []
    r = 0
    while y0 + (r + 0.5) * step < y1:
        y = y0 + (r + 0.5) * step
        cross = sorted(
            s[0] + (y - s[1]) * (s[2] - s[0]) / (s[3] - s[1])
            for s in rows[r]
            if (s[1] - y) * (s[3] - y) < 0
        )
        for a, b in zip(cross[0::2], cross[1::2]):
            k = math.ceil((a - x0) / step - 0.5)
            while x0 + (k + 0.5) * step < b:
                out.append((x0 + (k + 0.5) * step, y))
                k += 1
        r += 1
    return out


def clearances(segs: list[Seg], pts, cap: float, cell: float = 2.0):
    grid: dict[tuple[int, int], list[Seg]] = defaultdict(list)
    for s in segs:
        for i in range(int(min(s[0], s[2]) // cell), int(max(s[0], s[2]) // cell) + 1):
            for j in range(int(min(s[1], s[3]) // cell), int(max(s[1], s[3]) // cell) + 1):
                grid[(i, j)].append(s)
    reach = int(math.ceil(cap / cell))
    out = []
    for x, y in pts:
        ci, cj = int(x // cell), int(y // cell)
        best = cap * cap
        for i in range(ci - reach, ci + reach + 1):
            for j in range(cj - reach, cj + reach + 1):
                for ax, ay, bx, by in grid.get((i, j), ()):
                    dx, dy = bx - ax, by - ay
                    L = dx * dx + dy * dy
                    t = 0.0 if L == 0 else max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L))
                    ex, ey = ax + t * dx - x, ay + t * dy - y
                    d = ex * ex + ey * ey
                    if d < best:
                        best = d
        out.append((x, y, math.sqrt(best)))
    return out


def pick(cl, need: float, spacing: float):
    cand = sorted((c for c in cl if c[2] >= need), key=lambda c: -c[2])
    chosen: list[tuple[float, float, float]] = []
    for c in cand:
        if all((c[0] - p[0]) ** 2 + (c[1] - p[1]) ** 2 >= spacing * spacing for p in chosen):
            chosen.append(c)
    return chosen


def draw(segs, cl, sites, need, stud, path, title):
    xs = [s[0] for s in segs] + [s[2] for s in segs]
    ys = [s[1] for s in segs] + [s[3] for s in segs]
    x0, x1, y0, y1 = min(xs) - 2, max(xs) + 2, min(ys) - 2, max(ys) + 2
    sc = 8.0
    W, H = (x1 - x0) * sc, (y1 - y0) * sc + 40

    def X(x):
        return (x - x0) * sc

    def Y(y):
        return (y1 - y) * sc + 40

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
         f'viewBox="0 0 {W:.0f} {H:.0f}"><rect width="100%" height="100%" fill="#fff"/>',
         f'<text x="10" y="26" font-family="sans-serif" font-size="20">{title}</text>']
    # the cut face, shaded by room: grey where a socket cannot go, green where it can
    step = 0.0
    if len(cl) > 1:
        step = min(abs(cl[i + 1][0] - cl[i][0]) for i in range(min(50, len(cl) - 1)) if cl[i + 1][0] != cl[i][0])
    for x, y, d in cl:
        col = "#7fc97f" if d >= need else "#d9d9d9"
        o.append(f'<rect x="{X(x - step / 2):.1f}" y="{Y(y + step / 2):.1f}" width="{step * sc + 0.3:.1f}" '
                 f'height="{step * sc + 0.3:.1f}" fill="{col}"/>')
    for ax, ay, bx, by in segs:
        o.append(f'<line x1="{X(ax):.1f}" y1="{Y(ay):.1f}" x2="{X(bx):.1f}" y2="{Y(by):.1f}" '
                 f'stroke="#333" stroke-width="1"/>')
    for x, y, _ in sites:
        o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{stud / 2 * sc:.1f}" fill="#d7301f" '
                 f'stroke="#000" stroke-width="1"/>')
    o.append("</svg>")
    with open(path, "w") as f:
        f.write("\n".join(o))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("stl")
    ap.add_argument("--z", type=float, required=True, help="cut height, mm")
    ap.add_argument("--stud", type=float, default=2.0, help="stud diameter, mm")
    ap.add_argument("--gap", type=float, default=0.0, help="diametral socket gap, mm")
    ap.add_argument("--wall", type=float, default=0.9, help="wall left around the socket, mm")
    ap.add_argument("--spacing", type=float, default=10.0, help="minimum centre spacing, mm")
    ap.add_argument("--step", type=float, default=0.2, help="sample grid, mm")
    ap.add_argument("--sweep", help="comma list of stud diameters to count sites for")
    ap.add_argument("--svg", help="write the cut face with the chosen sites")
    a = ap.parse_args(argv)

    segs = slice_at(a.stl, a.z)
    if not segs:
        sys.exit(f"nothing at z={a.z}")
    pts = inside_points(segs, a.step)
    studs = [float(s) for s in a.sweep.split(",")] if a.sweep else [a.stud]
    cap = max((s + a.gap) / 2 + a.wall for s in studs) + 1.0
    cl = clearances(segs, pts, cap)
    area = len(pts) * a.step * a.step
    widest = max(c[2] for c in cl)
    print(f"z={a.z} segments={len(segs)} cut_area_mm2={area:.0f} max_clearance_mm={widest:.2f} "
          f"max_socket_dia_mm={2 * (widest - a.wall) - a.gap:.2f}")
    for s in studs:
        need = (s + a.gap) / 2 + a.wall
        sites = pick(cl, need, a.spacing)
        room = sum(1 for c in cl if c[2] >= need) * a.step * a.step
        print(f"stud={s} need_clearance={need:.2f} room_mm2={room:.1f} sites={len(sites)}")
    if a.svg:
        need = (a.stud + a.gap) / 2 + a.wall
        sites = pick(cl, need, a.spacing)
        draw(segs, cl, sites, need, a.stud, a.svg,
             f"cut at z={a.z} mm: stud {a.stud} mm, gap {a.gap} mm, wall {a.wall} mm, "
             f"{len(sites)} sites (red); "
             f"green = room for a socket")
    return 0


if __name__ == "__main__":
    sys.exit(main())
