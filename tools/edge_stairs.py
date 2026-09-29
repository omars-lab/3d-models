"""How far a polygon coaster's printed edge strays from its true edge, side by side.

The bikar kernel builds a coaster's top on a 0.4 mm grid, so a side that crosses the grid at a
slant comes out as steps. This reads an STL's bottom face, compares its outer edge with the
regular polygon the coaster is cut to, and prints per side how far the edge strays and how tall
the zigzag is (a straight side shifted off the line strays, but has no zigzag). With --svg it
also draws the picture on the 2026-09-29 open-calls page: the whole coaster with stepped sides
in red, and a close-up of one stepped side.

Usage: python3 tools/edge_stairs.py <coaster.stl> --sides 6 --flat 90 [--svg out.svg]
The polygon is centred on the origin with one flat side facing +x, as bikar writes it.

The 2026-09-29 numbers (slanted sides stray 0.27 mm, zigzag 0.54 mm) came from the CS-1 coaster,
rendered from bikar with
  node packages/cli/dist/index.js render patterns/Constructions/GimTvN9hw4U-coaster.bkr \
    --format stl --check --param size=90 -o cs1-90.stl
"""
import argparse
import math
import struct
from collections import Counter

ap = argparse.ArgumentParser(description="How far a polygon coaster's printed edge strays from its true edge.")
ap.add_argument("stl")
ap.add_argument("--sides", type=int, required=True, help="the polygon's number of sides")
ap.add_argument("--flat", type=float, required=True, help="width across the flats, mm")
ap.add_argument("--svg", help="also write the picture here")
args = ap.parse_args()
stl, N, FLAT = args.stl, args.sides, args.flat
with open(stl, "rb") as f:
    f.read(80)
    (n,) = struct.unpack("<I", f.read(4))
    tris = [struct.unpack("<12fH", f.read(50))[3:12] for _ in range(n)]

key = lambda x, y: (round(x, 4), round(y, 4))
edges = Counter()
for t in tris:
    if all(abs(t[i]) < 1e-6 for i in (2, 5, 8)):
        ks = [key(t[0], t[1]), key(t[3], t[4]), key(t[6], t[7])]
        for a, b in ((0, 1), (1, 2), (2, 0)):
            edges[tuple(sorted((ks[a], ks[b])))] += 1
outline = [e for e, c in edges.items() if c == 1]
pts = {p for e in outline for p in e}

# The true edge: the regular polygon the coaster is cut to. The mesh's own corner points are
# grid-snapped, so they are not used.
Rc = FLAT / 2 / math.cos(math.pi / N)
corners = [(Rc * math.cos(math.pi / N * (1 + 2 * k)), Rc * math.sin(math.pi / N * (1 + 2 * k))) for k in range(N)]
corners.sort(key=lambda p: math.atan2(p[1], p[0]))
R = Rc
sides = [(corners[i], corners[(i + 1) % N]) for i in range(N)]


def dist(p, a, b, signed=False):
    (ax, ay), (bx, by) = a, b
    L = math.hypot(bx - ax, by - ay)
    d = ((bx - ax) * (ay - p[1]) - (ax - p[0]) * (by - ay)) / L
    return d if signed else abs(d)


def side_of(p):
    """The side whose angular span holds p."""
    ang = math.atan2(p[1], p[0])
    for i, (a, b) in enumerate(sides):
        a1, b1 = math.atan2(a[1], a[0]), math.atan2(b[1], b[0])
        span = (b1 - a1) % (2 * math.pi)
        if (ang - a1) % (2 * math.pi) <= span + 1e-9:
            return i
    return 0


# The outer edge: outline edges whose both ends lie within 1 mm of their side's true line.
outer = [e for e in outline if all(dist(p, *sides[side_of(p)]) < 1.0 for p in e)]
# Per side, away from the corners: how far the edge strays (worst) and how tall its zigzag is
# (rough = highest minus lowest point across the line). A straight side shifted off the line has
# a worst but no rough.
lo, hi, worst = [9.0] * N, [-9.0] * N, [0.0] * N
for e in outer:
    for p in e:
        i = side_of(p)
        a, b = sides[i]
        t = ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / math.hypot(b[0] - a[0], b[1] - a[1]) ** 2
        if not 0.05 < t < 0.95:
            continue
        d = dist(p, a, b, signed=True)
        lo[i], hi[i], worst[i] = min(lo[i], d), max(hi[i], d), max(worst[i], abs(d))
rough = [hi[i] - lo[i] for i in range(N)]
for i in range(N):
    kind = "stairs" if rough[i] > 0.05 else "straight"
    print(f"ev=side i={i} kind={kind} strays_mm={worst[i]:.3f} zigzag_mm={rough[i]:.3f}")
if not args.svg:
    raise SystemExit(0)
out = args.svg

# --- picture ---
LW, RW, H = 520, 780, 560
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{LW + RW}" height="{H + 145}" viewBox="0 0 {LW + RW} {H + 145}">',
         '<rect width="100%" height="100%" fill="#ffffff"/>',
         '<style>text{font-family:Helvetica,Arial,sans-serif}</style>']

# Left: whole coaster.
s = (LW - 190) / (2 * R)
cx0, cy0 = LW / 2, 40 + H / 2
P = lambda x, y: (cx0 + x * s, cy0 - y * s)
parts.append(f'<text x="24" y="30" font-size="22" font-weight="bold">The whole coaster ({FLAT:g} mm)</text>')
for i, (a, b) in enumerate(sides):
    stepped = rough[i] > 0.05
    col = "#c53030" if stepped else "#2f855a"
    (x1, y1), (x2, y2) = P(*a), P(*b)
    parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="7" stroke-linecap="round"/>')
    mx, my = P((a[0] + b[0]) / 2 * 1.3, (a[1] + b[1]) / 2 * 1.3)
    label = "stairs" if stepped else "straight"
    parts.append(f'<text x="{mx:.0f}" y="{my + 6:.0f}" font-size="17" text-anchor="middle" fill="{col}">{label}</text>')

# Zoom target: middle of the worst side.
wi = max(range(N), key=lambda i: rough[i])
A, B = sides[wi]
zx, zy = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
W, Hm = 4.0, 3.0
bx, by = P(zx - W / 2, zy + Hm / 2)
parts.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{W * s:.1f}" height="{Hm * s:.1f}" fill="none" stroke="#1a202c" stroke-width="2"/>')

# Right: close-up.
S = (RW - 60) / W
ox, oy = LW + 30, 60
x0, y0 = zx - W / 2, zy - Hm / 2
Q = lambda x, y: (ox + (x - x0) * S, oy + (Hm - (y - y0)) * S)
parts.append(f'<text x="{LW + 30}" y="30" font-size="22" font-weight="bold">The black box, {S / s:.0f} times closer (4 mm across)</text>')
parts.append(f'<clipPath id="c"><rect x="{ox}" y="{oy}" width="{W * S:.0f}" height="{Hm * S:.0f}"/></clipPath>')
parts.append(f'<rect x="{ox}" y="{oy}" width="{W * S:.0f}" height="{Hm * S:.0f}" fill="#f7fafc" stroke="#cbd5e0"/>')
g = [f'<g clip-path="url(#c)">']
gx = math.floor(x0 / 0.4) * 0.4
while gx < x0 + W + 0.4:
    a, _ = Q(gx, 0)
    g.append(f'<line x1="{a:.1f}" y1="{oy}" x2="{a:.1f}" y2="{oy + Hm * S:.0f}" stroke="#e2e8f0" stroke-width="1.5"/>')
    gx += 0.4
gy = math.floor(y0 / 0.4) * 0.4
while gy < y0 + Hm + 0.4:
    _, b = Q(0, gy)
    g.append(f'<line x1="{ox}" y1="{b:.1f}" x2="{ox + W * S:.0f}" y2="{b:.1f}" stroke="#e2e8f0" stroke-width="1.5"/>')
    gy += 0.4
(ax, ay), (bx2, by2) = Q(*A), Q(*B)
for a, b in outer:
    (x1, y1), (x2, y2) = Q(*a), Q(*b)
    g.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#c53030" stroke-width="6" stroke-linecap="square"/>')
g.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx2:.1f}" y2="{by2:.1f}" stroke="#2b6cb0" stroke-width="3" stroke-dasharray="12 8"/>')
g.append("</g>")
parts += g
# 1 mm scale bar.
sx, sy = ox + 20, oy + Hm * S - 24
parts.append(f'<line x1="{sx}" y1="{sy}" x2="{sx + S:.0f}" y2="{sy}" stroke="#1a202c" stroke-width="4"/>')
parts.append(f'<text x="{sx}" y="{sy - 10}" font-size="17">1 mm</text>')

ty = H + 75
parts.append(f'<text x="24" y="{ty}" font-size="18">The printed file is built on a grid of 0.4 mm squares (grey). Green sides run along the grid, so they come out straight.</text>')
parts.append(f'<text x="24" y="{ty + 28}" font-size="18">Red sides cross the grid at a slant, so the file follows the grid in steps (red) instead of the true edge (blue dashes).</text>')
parts.append(f'<text x="24" y="{ty + 56}" font-size="18">Each step is one square high. The edge strays up to {max(worst[i] for i in range(N) if rough[i] > 0.05):.2f} mm either side of the true line: under three sheets of paper.</text>')
parts.append("</svg>")
open(out, "w").write("\n".join(parts))
print("wrote", out)
