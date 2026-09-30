#!/usr/bin/env python3
"""Draw the pictures for smooth-lines-design-a.md.

Inputs are a bikar render of the CS-2 minimal coaster (size 90), made with the
bikar CLI (`render <bkr> --format svg|stl|preview --param size=90`):

    make_figures.py --svg cs2.svg --stl cs2.stl --previews r0.png,r1.png,r15.png \
        --out <dir> [--crop CX,CY,HALF] [--only fig02]

Everything drawn here is our own geometry: the strap centrelines come from the
SVG, the "today" staircase comes from the STL's bottom face, and each option is
computed from the centrelines with shapely / numpy / scikit-image.
"""
from __future__ import annotations

import argparse
import math
import re
import struct
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import shapely  # noqa: E402
from matplotlib.patches import PathPatch, Rectangle  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
from PIL import Image  # noqa: E402
from shapely.geometry import LineString, MultiPolygon, Point, Polygon, box  # noqa: E402
from shapely.ops import linemerge, unary_union  # noqa: E402
from skimage import measure  # noqa: E402

STRAP = 3.0
R = STRAP / 2
PITCH = 0.4
FILL = "#d9b25a"
EDGE = "#6b4f12"
EXACT = "#1f4e79"
BG = "#fbf8f1"

# ---------------------------------------------------------------- inputs


def load_segments(svg: Path) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """Strap centrelines, y flipped from SVG (y down) to model space (y up)."""
    pat = re.compile(r'x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"')
    segs = []
    for m in pat.finditer(svg.read_text()):
        x1, y1, x2, y2 = map(float, m.groups())
        segs.append(((x1, -y1), (x2, -y2)))
    return segs


def load_bottom(stl: Path, window: Polygon) -> Polygon | MultiPolygon:
    """Union of the STL's bottom-face triangles that touch `window`."""
    data = stl.read_bytes()
    n = struct.unpack("<I", data[80:84])[0]
    rec = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
    tri = np.frombuffer(data, dtype=rec, count=n, offset=84)["v"].astype(float)
    zmin = tri[:, :, 2].min()
    bottom = tri[np.all(np.abs(tri[:, :, 2] - zmin) < 1e-6, axis=1)]
    minx, miny, maxx, maxy = window.bounds
    cx = bottom[:, :, 0].mean(axis=1)
    cy = bottom[:, :, 1].mean(axis=1)
    keep = bottom[(cx > minx - 1) & (cx < maxx + 1) & (cy > miny - 1) & (cy < maxy + 1)]
    polys = [Polygon(t[:, :2]) for t in keep]
    return unary_union([p.buffer(1e-7) for p in polys if p.area > 0]).buffer(-1e-7)


# ---------------------------------------------------------------- geometry


def exact_shape(segs, r=R, quad=32, cap="round", join="round"):
    return unary_union([LineString(s).buffer(r, quad_segs=quad, cap_style=cap, join_style=join) for s in segs])


def seg_dist(px, py, a, b):
    """Distance from points to segment ab, and the projection parameter t."""
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = np.clip(((px - ax) * dx + (py - ay) * dy) / L2, 0, 1)
    qx, qy = ax + t * dx - px, ay + t * dy - py
    return np.hypot(qx, qy), t


def straight_segments(segs):
    """Merge collinear pieces so a straight strap split at a node is one stroke."""
    merged = linemerge([LineString(s) for s in segs])
    geoms = merged.geoms if hasattr(merged, "geoms") else [merged]
    out = []
    for g in geoms:
        pts = list(g.simplify(1e-6).coords)
        out += [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    return out


def grid_cells(shape, x0, y0, pitch, window):
    """Cells whose centre is inside `shape` (today's rule), as one polygon."""
    minx, miny, maxx, maxy = window.bounds
    i0, i1 = math.floor((minx - x0) / pitch) - 1, math.ceil((maxx - x0) / pitch) + 1
    j0, j1 = math.floor((miny - y0) / pitch) - 1, math.ceil((maxy - y0) / pitch) + 1
    ii, jj = np.meshgrid(np.arange(i0, i1), np.arange(j0, j1), indexing="ij")
    cx = x0 + (ii + 0.5) * pitch
    cy = y0 + (jj + 0.5) * pitch
    inside = shapely.contains_xy(shape, cx, cy)
    cells = [box(x0 + i * pitch, y0 + j * pitch, x0 + (i + 1) * pitch, y0 + (j + 1) * pitch)
             for i, j in zip(ii[inside], jj[inside])]
    return unary_union(cells)


def on_frame(seg, extent=45.0):
    """True for the straight outer border strokes, which keep a constant width."""
    (x1, y1), (x2, y2) = seg
    return (abs(x1 - x2) < 1e-6 and abs(abs(x1) - extent) < 0.05) or \
        (abs(y1 - y2) < 1e-6 and abs(abs(y1) - extent) < 0.05)


def field_signed(segs, xs, ys, radius_fn=None, blend=0.0, extent=45.0):
    """Signed inset field on a grid: >0 inside the strap.

    radius_fn(t) gives the half-width along a stroke (t in 0..1; the outer
    border keeps R); blend>0 joins the two nearest strokes with a quadratic
    smooth minimum (sorted, so the result does not depend on stroke order and
    keeps the pattern's symmetry).
    """
    X, Y = np.meshgrid(xs, ys)
    best = np.full(X.shape, np.inf)
    second = np.full(X.shape, np.inf)
    for a, b in segs:
        d, t = seg_dist(X, Y, a, b)
        f = d - (radius_fn(t) if radius_fn and not on_frame((a, b), extent) else R)
        lower = f < best
        second = np.where(lower, best, np.minimum(second, f))
        best = np.where(lower, f, best)
    if blend > 0:
        h = np.maximum(blend - np.abs(best - second), 0) / blend
        best = best - h * h * blend / 4
    return X, Y, -best


def contour_polys(X, Y, F, level=0.0):
    xs, ys = X[0], Y[:, 0]
    polys = []
    for c in measure.find_contours(F, level):
        px = np.interp(c[:, 1], np.arange(len(xs)), xs)
        py = np.interp(c[:, 0], np.arange(len(ys)), ys)
        if len(px) >= 3:
            polys.append(np.column_stack([px, py]))
    return polys


def stray(boundary_pts, exact, window, margin=0.6):
    """Largest and mean distance from a candidate edge to the exact edge."""
    inner = window.buffer(-margin)
    pts = [p for p in boundary_pts if inner.contains(Point(p))]
    if not pts:
        return 0.0, 0.0
    d = np.array([exact.boundary.distance(Point(p)) for p in pts])
    return float(d.max()), float(d.mean())


def densify(coords, step=0.05):
    out = []
    for (x1, y1), (x2, y2) in zip(coords[:-1], coords[1:]):
        n = max(1, int(math.hypot(x2 - x1, y2 - y1) / step))
        for k in range(n):
            out.append((x1 + (x2 - x1) * k / n, y1 + (y2 - y1) * k / n))
    return out


def rings(geom):
    polys = geom.geoms if hasattr(geom, "geoms") else [geom]
    for p in polys:
        if p.is_empty or not hasattr(p, "exterior"):
            continue
        yield list(p.exterior.coords)
        for h in p.interiors:
            yield list(h.coords)


def geom_edge_points(geom, step=0.05):
    pts = []
    for ring in rings(geom):
        pts += densify(ring, step)
    return pts


# ---------------------------------------------------------------- drawing


def draw_geom(ax, geom, fc=FILL, ec=EDGE, lw=0.8, alpha=1.0):
    polys = geom.geoms if hasattr(geom, "geoms") else [geom]
    for p in polys:
        if p.is_empty or not hasattr(p, "exterior"):
            continue
        verts, codes = [], []
        for ring in [p.exterior, *p.interiors]:
            c = list(ring.coords)
            verts += c
            codes += [MPath.MOVETO] + [MPath.LINETO] * (len(c) - 2) + [MPath.CLOSEPOLY]
        ax.add_patch(PathPatch(MPath(verts, codes), fc=fc, ec=ec, lw=lw, alpha=alpha))


def draw_exact(ax, exact, lw=0.9):
    for ring in rings(exact):
        a = np.array(ring)
        ax.plot(a[:, 0], a[:, 1], ls=(0, (3, 2)), color=EXACT, lw=lw)


def frame(ax, window, title=None, sub=None):
    minx, miny, maxx, maxy = window.bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor(BG)
    if title:
        ax.set_title(title, fontsize=12, fontweight="bold", pad=6)
    if sub:
        ax.text(0.5, -0.03, sub, transform=ax.transAxes, ha="center", va="top", fontsize=9.5, color="#333")


def scale_bar(ax, window, mm=1.0):
    minx, miny, maxx, maxy = window.bounds
    x = minx + 0.06 * (maxx - minx)
    y = miny + 0.06 * (maxy - miny)
    ax.plot([x, x + mm], [y, y], color="black", lw=3, solid_capstyle="butt")
    ax.text(x + mm / 2, y + 0.03 * (maxy - miny), f"{mm:g} mm", ha="center", fontsize=8.5)


def save(fig, out: Path, name: str):
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.png", dpi=150, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out / (name + '.png')}")


def sym_scores(shape):
    """Overlap (intersection over union) with 90-degree turn and with a mirror."""
    from shapely import affinity

    rot = affinity.rotate(shape, 90, origin=(0, 0))
    mir = affinity.scale(shape, xfact=-1, yfact=1, origin=(0, 0))
    iou = lambda a, b: a.intersection(b).area / a.union(b).area  # noqa: E731
    return iou(shape, rot), iou(shape, mir)


# ---------------------------------------------------------------- figures


def fig00(ctx):
    segs, exact, window = ctx["segs"], ctx["exact"], ctx["window"]
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.6))
    ax = axes[0]
    draw_geom(ax, exact, lw=0.3)
    ax.add_patch(Rectangle(window.bounds[:2], window.bounds[2] - window.bounds[0],
                           window.bounds[3] - window.bounds[1], fill=False, ec="#c0392b", lw=2.2))
    frame(ax, box(-49, -49, 49, 49), "The whole coaster (CS-2, 90 mm)",
          "red box = the small crop every option below is drawn in")
    img = Image.open(ctx["previews"][1])
    ax = axes[1]
    ax.imshow(img.crop(ctx["render_crop"]))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Today's render, strap walls up close", fontsize=12, fontweight="bold", pad=6)
    ax.text(0.5, -0.03, "the vertical ribs on every wall are the 0.4 mm steps", transform=ax.transAxes,
            ha="center", va="top", fontsize=9.5, color="#333")
    save(fig, ctx["out"], "fig00-where-and-what")


def fig01(ctx):
    exact, window, today = ctx["exact"], ctx["window"], ctx["today"]
    mx, mean = stray(geom_edge_points(today), exact, window)
    fig, ax = plt.subplots(figsize=(8.5, 8.5))
    draw_geom(ax, today)
    draw_exact(ax, exact, lw=1.3)
    scale_bar(ax, window)
    frame(ax, window, "Today: the edge is a 0.4 mm staircase",
          f"filled = the printed outline (read from the STL); dashed = the outline the pattern asks for\n"
          f"largest gap between them {mx:.2f} mm, typical {mean:.2f} mm")
    save(fig, ctx["out"], "fig01-today-staircase")
    ctx["today_stray"] = (mx, mean)


def fig02(ctx):
    segs, exact, window, today = ctx["segs"], ctx["exact"], ctx["window"], ctx["today"]
    x0, y0 = ctx["grid_origin"]
    fine2 = grid_cells(exact, x0, y0, 0.2, window)
    fine1 = grid_cells(exact, x0, y0, 0.1, window)
    minx, miny, maxx, maxy = window.buffer(1).bounds
    xs = np.arange(x0 + math.floor((minx - x0) / PITCH) * PITCH, maxx, PITCH)
    ys = np.arange(y0 + math.floor((miny - y0) / PITCH) * PITCH, maxy, PITCH)
    X, Y, F = field_signed(ctx["segs_near"], xs, ys)
    ms = contour_polys(X, Y, F)
    ms_geom = unary_union([Polygon(c).buffer(0) for c in ms if len(c) > 3])
    ms_pts = [tuple(p) for c in ms for p in densify([tuple(q) for q in c])]
    panels = [
        ("Today: 0.4 mm grid", today, geom_edge_points(today)),
        ("Finer grid, 0.2 mm", fine2, geom_edge_points(fine2)),
        ("Finer grid, 0.1 mm", fine1, geom_edge_points(fine1)),
        ("Marching squares, 0.4 mm", None, ms_pts),
        ("Exact offset", exact, geom_edge_points(exact)),
    ]
    fig, grid = plt.subplots(2, 3, figsize=(16, 11.4))
    axes = grid.ravel()
    for ax, (title, geom, pts) in zip(axes, panels):
        if geom is None:
            # draw marching squares as filled contours with polyline edges
            ax.contourf(X, Y, F, levels=[0, 99], colors=[FILL])
            for c in ms:
                ax.plot(c[:, 0], c[:, 1], color=EDGE, lw=0.8)
        else:
            draw_geom(ax, geom)
        draw_exact(ax, exact)
        mx, mean = stray(pts, exact, window)
        frame(ax, window, title, f"largest gap {mx:.2f} mm, typical {mean:.3f} mm")
    scale_bar(axes[0], window)
    # zoom on the sharpest hole point, where every method does worst
    ax = axes[5]
    tip = ctx["tip"]
    zw = box(tip[0] - 1.2, tip[1] - 1.2, tip[0] + 1.2, tip[1] + 1.2)
    draw_geom(ax, today.intersection(zw.buffer(0.5)), fc="none", ec=EDGE, lw=1.6)
    for c in ms:
        ax.plot(c[:, 0], c[:, 1], color="#c0392b", lw=1.8)
    draw_exact(ax, exact, lw=1.6)
    ax.plot([], [], color=EDGE, lw=1.6, label="today (0.4 mm steps)")
    ax.plot([], [], color="#c0392b", lw=1.8, label="marching squares")
    ax.plot([], [], color=EXACT, ls=(0, (3, 2)), lw=1.6, label="exact offset")
    ax.legend(loc="lower right", fontsize=9, frameon=True)
    frame(ax, zw, "Close-up: one sharp point of a star hole",
          "grid methods clip a point narrower than one step")
    scale_bar(ax, zw, 0.4)
    save(fig, ctx["out"], "fig02-edge-options")
    ctx["ms_geom"] = ms_geom


def mitre_shape(segs, r=R):
    """Traditional band: mitred bends, flat ends, crossings filled."""
    merged = linemerge([LineString(s) for s in segs])
    geoms = list(merged.geoms) if hasattr(merged, "geoms") else [merged]
    parts = [g.buffer(r, cap_style="flat", join_style="mitre", mitre_limit=5) for g in geoms]
    # fill each node where 3+ strokes meet with the hull of their flat ends
    ends: dict[tuple[float, float], list] = {}
    for a, b in segs:
        for p, q in ((a, b), (b, a)):
            key = (round(p[0], 3), round(p[1], 3))
            ends.setdefault(key, []).append(q)
    for key, others in ends.items():
        if len(others) >= 3:
            pts = []
            for q in others:
                dx, dy = q[0] - key[0], q[1] - key[1]
                L = math.hypot(dx, dy)
                nx, ny = -dy / L * r, dx / L * r
                pts += [(key[0] + nx, key[1] + ny), (key[0] - nx, key[1] - ny)]
            parts.append(shapely.MultiPoint(pts).convex_hull)
    return unary_union(parts)


def fig03(ctx):
    segs, exact, window = ctx["segs"], ctx["exact"], ctx["window"]
    near = ctx["segs_near"]
    base = exact_shape(near)
    fil075 = base.buffer(0.75, quad_segs=32).buffer(-0.75, quad_segs=32)
    fil15 = base.buffer(1.5, quad_segs=32).buffer(-1.5, quad_segs=32)
    mitre = mitre_shape(near)
    mitre_r = mitre.buffer(-0.3, quad_segs=16).buffer(0.3, quad_segs=16)
    panels = [
        ("Today: strap bends round,\nhole points sharp", base),
        ("Hole points rounded\n0.75 mm", fil075),
        ("Hole points rounded\n1.5 mm", fil15),
        ("Mitred band: strap bends\nsharp too (0.3 mm round)", mitre_r),
    ]
    fig, grid = plt.subplots(2, 2, figsize=(12, 12.6))
    axes = grid.ravel()
    for ax, (title, g) in zip(axes, panels):
        draw_geom(ax, g.intersection(window.buffer(2)))
        draw_exact(ax, exact, lw=0.7)
        frame(ax, window, title)
    axes[0].text(0.5, -0.03, "dashed = today's outline, for comparison", transform=axes[0].transAxes,
                 ha="center", va="top", fontsize=9.5)
    scale_bar(axes[0], window)
    save(fig, ctx["out"], "fig03-corner-options")


def fig04(ctx):
    theta = math.radians(90)  # angle between the two straights
    d = 1.0  # tangent length from the corner, same for both blends (1 mm fillet)
    u1 = np.array([-1.0, 0.0])
    u2 = np.array([math.cos(math.pi - theta), math.sin(math.pi - theta)])
    corner = np.array([0.0, 0.0])
    p0, p4 = corner + u1 * d, corner + u2 * d
    # circular fillet with the same tangent points
    half = theta / 2
    rad = d * math.tan(half)
    bis = (u1 + u2) / np.linalg.norm(u1 + u2)
    centre = corner + bis * (d / math.cos(half))
    a0 = math.atan2(*(p0 - centre)[::-1])
    a1 = math.atan2(*(p4 - centre)[::-1])
    if a1 - a0 > math.pi:
        a1 -= 2 * math.pi
    if a0 - a1 > math.pi:
        a1 += 2 * math.pi
    ang = np.linspace(a0, a1, 200)
    arc = centre + rad * np.column_stack([np.cos(ang), np.sin(ang)])
    # quartic Bezier: three control points on each straight -> zero curvature at the ends
    P = np.array([p0, corner + u1 * d / 2, corner, corner + u2 * d / 2, p4])
    t = np.linspace(0, 1, 400)[:, None]
    coef = [1, 4, 6, 4, 1]
    bez = sum(coef[k] * (1 - t) ** (4 - k) * t ** k * P[k] for k in range(5))

    def curvature(pts):
        dx, dy = np.gradient(pts[:, 0]), np.gradient(pts[:, 1])
        ddx, ddy = np.gradient(dx), np.gradient(dy)
        k = np.abs(dx * ddy - dy * ddx) / (dx * dx + dy * dy) ** 1.5
        s = np.concatenate([[0], np.cumsum(np.hypot(np.diff(pts[:, 0]), np.diff(pts[:, 1])))])
        return s, k

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw={"width_ratios": [1, 1.25]})
    ax = axes[0]
    lead = 1.2
    for u, p in ((u1, p0), (u2, p4)):
        q = p + u * lead
        ax.plot([p[0], q[0]], [p[1], q[1]], color="#444", lw=2)
    ax.plot(arc[:, 0], arc[:, 1], color="#c0392b", lw=2.2, label=f"circular fillet, radius {rad:.2f} mm")
    ax.plot(bez[:, 0], bez[:, 1], color=EXACT, lw=2.2, label="curvature-continuous blend")
    ax.plot([p0[0], corner[0], p4[0]], [p0[1], corner[1], p4[1]], ls=":", color="#999")
    nozzle = plt.Circle((-1.8, 1.9), 0.2, fc="#ddd", ec="#555")
    ax.add_patch(nozzle)
    ax.text(-1.8, 1.55, "0.4 mm nozzle, to scale", ha="center", va="top", fontsize=9)
    ax.set_xlim(-2.4, 0.9)
    ax.set_ylim(-0.9, 2.4)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor(BG)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), fontsize=9.5, frameon=False)
    ax.set_title("Same corner, two blends", fontsize=12, fontweight="bold")
    ax = axes[1]
    s, k = curvature(arc)
    s = np.concatenate([[-lead, 0], s, [s[-1], s[-1] + lead]])
    k = np.concatenate([[0, 0], k, [0, 0]])
    ax.plot(s, k, color="#c0392b", lw=2.2, label="circular fillet: bend jumps on and off")
    s2, k2 = curvature(bez)
    s2 = np.concatenate([[-lead], s2, [s2[-1] + lead]])
    k2 = np.concatenate([[0], k2, [0]])
    ax.plot(s2, k2, color=EXACT, lw=2.2, label="curvature-continuous: bend ramps up and down")
    ax.set_xlabel("distance along the edge (mm)")
    ax.set_ylabel("how sharply it bends (1 / radius, per mm)")
    ax.legend(fontsize=9, frameon=False, loc="upper right")
    ax.set_title("How sharply each one bends along the edge", fontsize=12, fontweight="bold")
    ax.set_facecolor(BG)
    save(fig, ctx["out"], "fig04-fillet-vs-curvature-continuous")


def varwidth_shape(segs, width_fn):
    return unary_union([LineString(s).buffer(width_fn(s) / 2, quad_segs=16) for s in segs])


def fig05(ctx):
    segs, window = ctx["segs"], ctx["window"]
    wmin, wmax = 1.8, 3.4

    def angle(s):
        (x1, y1), (x2, y2) = s
        return math.atan2(y2 - y1, x2 - x1)

    def fixed_nib(s):
        return wmin + (wmax - wmin) * abs(math.sin(angle(s) - math.radians(30)))

    def radial_nib(s):
        (x1, y1), (x2, y2) = s
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        radial = math.atan2(my, mx) if math.hypot(mx, my) > 1e-6 else 0.0
        return wmin + (wmax - wmin) * abs(math.sin(angle(s) - radial))

    straight = straight_segments(segs)
    X, Y, F = ctx["taper_field"]
    fixed = varwidth_shape(straight, fixed_nib)
    radial = varwidth_shape(straight, radial_nib)
    full = box(-49, -49, 49, 49)
    fig, axes = plt.subplots(1, 3, figsize=(19, 6.8))
    ax = axes[0]
    ax.contourf(X, Y, F, levels=[0, 99], colors=[FILL])
    ax.contour(X, Y, F, levels=[0], colors=[EDGE], linewidths=0.8)
    draw_exact(ax, ctx["exact"], lw=0.7)
    frame(ax, window, "Taper: 3 mm at the joins,\n2.2 mm mid-span",
          "dashed = today's constant 3 mm strap")
    scale_bar(ax, window)
    for ax, g, title in ((axes[1], fixed, "Pen held at one angle"), (axes[2], radial, "Pen turned with the pattern")):
        draw_geom(ax, g, lw=0.2)
        t90, mir = sym_scores(g)
        frame(ax, full, title, f"matches itself turned 90 degrees: {t90 * 100:.0f}%   mirrored: {mir * 100:.0f}%")
    save(fig, ctx["out"], "fig05-width-options")


def fig06(ctx):
    window, exact = ctx["window"], ctx["exact"]
    fig = plt.figure(figsize=(22, 6.6))
    gs = fig.add_gridspec(2, 6, width_ratios=[1, 1, 0.06, 1.5, 1.5, 1.5], hspace=0.35, wspace=0.12)
    # ---- trait sheet (abstract shapes, not letters)
    v = LineString([(-1.5, 1.2), (0, -0.6), (1.5, 1.2)])
    xs = np.linspace(-1.8, 1.8, 200)
    w = 0.55 - 0.18 * np.sin(np.pi * (xs + 1.8) / 3.6) ** 2
    waisted = unary_union([Polygon(np.column_stack([np.r_[xs, xs[::-1]], np.r_[w, -w[::-1]]])),
                           Point(-1.8, 0).buffer(0.55), Point(1.8, 0).buffer(0.55)])
    balls = unary_union([LineString([(-1.4, 0), (1.4, 0)]).buffer(0.35, cap_style="flat"),
                         Point(-1.4, 0).buffer(0.62), Point(1.4, 0).buffer(0.62)])
    traits = [
        (gs[0, 0], v.buffer(0.45, join_style="mitre"), "sharp notch (today)"),
        (gs[0, 1], v.buffer(0.45).buffer(0.5).buffer(-0.5), "round-bottomed notch"),
        (gs[1, 0], waisted, "swell at joins, waist mid-span"),
        (gs[1, 1], balls, "ball ends"),
    ]
    for spec, g, title in traits:
        ax = fig.add_subplot(spec)
        draw_geom(ax, g)
        ax.set_title(title, fontsize=10)
        _trait_frame(ax)
    fig.text(0.16, 0.97, "The traits, drawn as plain shapes", ha="center", fontsize=12, fontweight="bold")
    # ---- today vs two strengths of the SKIMS-influenced strap
    ax = fig.add_subplot(gs[:, 3])
    draw_geom(ax, exact.intersection(window.buffer(2)))
    frame(ax, window, "Today", "constant 3 mm")
    scale_bar(ax, window)
    for spec, (label, sub, (X, Y, F)) in zip((gs[:, 4], gs[:, 5]), ctx["skims_crop"]):
        ax = fig.add_subplot(spec)
        ax.contourf(X, Y, F, levels=[0, 99], colors=[FILL])
        ax.contour(X, Y, F, levels=[0], colors=[EDGE], linewidths=0.8)
        draw_exact(ax, exact, lw=0.7)
        frame(ax, window, label, sub + "; dashed = today")
    save(fig, ctx["out"], "fig06-skims-influenced")


def _trait_frame(ax):
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-1.3, 1.9)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor(BG)


def fig06b(ctx):
    """The SKIMS-influenced strap on the whole coaster, to check symmetry by eye."""
    fig, axes = plt.subplots(1, 3, figsize=(19, 6.9))
    full = box(-49, -49, 49, 49)
    draw_geom(axes[0], ctx["exact"], lw=0.25)
    frame(axes[0], full, "Today")
    ctx["skims_sym"] = []
    for ax, (label, sub, (X, Y, F)) in zip(axes[1:], ctx["skims_full"]):
        ax.contourf(X, Y, F, levels=[0, 99], colors=[FILL])
        ax.contour(X, Y, F, levels=[0], colors=[EDGE], linewidths=0.25)
        t90, mir = mask_sym(F)
        ctx["skims_sym"].append((label, t90, mir))
        frame(ax, full, label, f"{sub}\nmatches itself turned 90 degrees: {t90 * 100:.1f}%   mirrored: {mir * 100:.1f}%")
    save(fig, ctx["out"], "fig06b-skims-whole-coaster")


def mask_sym(F):
    """Overlap of the solid with its 90-degree turn and its mirror (grid must be symmetric about 0)."""
    m = F > 0
    iou = lambda a, b: (a & b).sum() / (a | b).sum()  # noqa: E731
    return float(iou(m, np.rot90(m))), float(iou(m, m[:, ::-1]))


def fig07(ctx):
    layer = 0.2
    h = 4.0
    fig, axes = plt.subplots(1, 3, figsize=(16, 3.3))
    for ax, rnd, title in zip(axes, (0.0, 1.0, 1.5), ("Square top (round 0)", "Quarter-round (round 1, today)",
                                                         "Full pillow (round 1.5)")):
        xs = np.linspace(-R, R, 400)
        inset = R - np.abs(xs)
        drop = np.where(inset < rnd, rnd - np.sqrt(np.maximum(rnd * rnd - (rnd - inset) ** 2, 0)), 0) if rnd else 0 * xs
        top = h - drop
        ax.fill_between(xs, 0, top, color="#eee", ec="#aaa", lw=0.6)
        ax.plot(xs, top, color=EXACT, ls=(0, (3, 2)), lw=1.3)
        # printed layers: each layer is as wide as the shape at its mid-height
        for z0 in np.arange(0, h, layer):
            zm = z0 + layer / 2
            inside = xs[top >= zm]
            if len(inside):
                ax.add_patch(Rectangle((inside[0], z0), inside[-1] - inside[0], layer, fc=FILL, ec=EDGE, lw=0.35))
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(2.2, 4.25)
        ax.set_aspect("equal")
        ax.set_facecolor(BG)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("across the strap (mm)")
    axes[0].set_ylabel("height (mm)")
    fig.text(0.5, -0.06, "top 2 mm of a 3 mm strap, 0.2 mm layers; dashed = the shape asked for, blocks = what "
             "the layers print", ha="center", fontsize=10)
    save(fig, ctx["out"], "fig07a-top-profiles")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.4))
    for ax, png, title in zip(axes, ctx["previews"], ("round 0", "round 1 (today)", "round 1.5")):
        ax.imshow(Image.open(png).crop(ctx["render_crop"]))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=12, fontweight="bold")
    fig.text(0.5, 0.04, "real bikar renders of the same coaster, same camera, same crop", ha="center", fontsize=10)
    save(fig, ctx["out"], "fig07b-top-profiles-rendered")


SLICER_TOLS = (0.2, 0.3)  # contour-simplify tolerances tried in place of the 0.012 mm Bambu default


def slicer_simplified(ctx):
    """Today's staircase after a Douglas-Peucker simplify at each tolerance, and its stray from exact."""
    out = []
    for tol in SLICER_TOLS:
        g = ctx["today"].simplify(tol, preserve_topology=True)
        out.append((tol, g, stray(geom_edge_points(g), ctx["exact"], ctx["window"])))
    return out


def fig08(ctx):
    rad = R
    simp = slicer_simplified(ctx)
    for tol, _, (mx, mean) in simp:
        print(f"slicer simplify {tol}: largest {mx:.3f} typical {mean:.3f}")
    fig, axes = plt.subplots(1, 3, figsize=(21, 6.4), gridspec_kw={"width_ratios": [1.25, 1, 1], "wspace": 0.35})
    ax = axes[2]
    tol, g, (mx, mean) = simp[-1]
    draw_geom(ax, g)
    draw_exact(ax, ctx["exact"], lw=1.1)
    scale_bar(ax, ctx["window"])
    frame(ax, ctx["window"], f"Slicer told to simplify at {tol} mm",
          f"today's steps simplified to within {tol} mm, dashed = exact\nlargest gap {mx:.2f} mm, typical {mean:.3f} mm")
    ax = axes[0]
    for k, n in enumerate((2, 4, 8, 16)):
        ox = k * 3.6
        th = np.linspace(0, math.pi / 2, n + 1)
        ax.plot(ox + rad * np.cos(np.linspace(0, math.pi / 2, 100)), rad * np.sin(np.linspace(0, math.pi / 2, 100)),
                color=EXACT, ls=(0, (3, 2)), lw=1)
        ax.plot(ox + rad * np.cos(th), rad * np.sin(th), color=EDGE, lw=1.8, marker="o", ms=3)
        err = rad * (1 - math.cos(math.pi / 4 / n))
        ax.text(ox + 0.75, -0.45, f"{n} flats per\nquarter turn\ngap {err:.3f} mm", ha="center", va="top", fontsize=9)
    ax.set_aspect("equal")
    ax.set_xlim(-0.4, 14.6)
    ax.set_ylim(-1.7, 1.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor(BG)
    ax.set_title("Round strap end (1.5 mm radius) as flat facets", fontsize=12, fontweight="bold")
    ax = axes[1]
    mx, mean = ctx["today_stray"]
    labels = ["today's steps\n(largest)", "today's steps\n(typical)", "exact outline,\n16 flats per\nquarter turn",
              "slicer detail limit\n(Bambu default)"]
    vals = [mx, mean, rad * (1 - math.cos(math.pi / 4 / 16)), 0.012]
    ax.barh(labels, vals, color=[EDGE, EDGE, EXACT, "#888"])
    for i, v in enumerate(vals):
        ax.text(v + 0.004, i, f"{v:.3f} mm", va="center", fontsize=9)
    ax.axvline(0.2, color="#c0392b", ls=":", lw=1)
    ax.text(0.2, 3.45, " half a nozzle width", color="#c0392b", fontsize=8.5, va="center")
    ax.set_xlim(0, max(vals) * 1.45)
    ax.invert_yaxis()
    ax.set_xlabel("how far the edge wanders from the true outline (mm)")
    ax.set_title("Where the roughness actually comes from", fontsize=12, fontweight="bold")
    ax.set_facecolor(BG)
    save(fig, ctx["out"], "fig08-mesh-and-slicer")


# ---------------------------------------------------------------- main


def grid_origin_from_stl(stl: Path):
    """Recover the grid's x0/y0 (mod pitch) from the bottom-face vertices."""
    data = stl.read_bytes()
    n = struct.unpack("<I", data[80:84])[0]
    rec = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
    v = np.frombuffer(data, dtype=rec, count=n, offset=84)["v"].reshape(-1, 3).astype(float)
    v = v[np.abs(v[:, 2] - v[:, 2].min()) < 1e-6]

    def mode(vals):
        r = np.round(np.mod(vals, PITCH), 3) % PITCH
        u, c = np.unique(r, return_counts=True)
        return float(u[np.argmax(c)])

    return mode(v[:, 0]), mode(v[:, 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg", type=Path, required=True)
    ap.add_argument("--stl", type=Path, required=True)
    ap.add_argument("--previews", required=True, help="round 0, 1, 1.5 preview PNGs, comma separated")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--crop", default="-8.3,-19.5,6", help="centre x, centre y, half-width (mm)")
    ap.add_argument("--render-crop", default="330,300,630,560", help="pixel box in the preview PNGs")
    ap.add_argument("--only", default="", help="comma separated figure names")
    a = ap.parse_args()
    cx, cy, half = map(float, a.crop.split(","))
    window = box(cx - half, cy - half, cx + half, cy + half)
    segs = load_segments(a.svg)
    near_win = window.buffer(STRAP * 2)
    segs_near = [s for s in segs if LineString(s).intersects(near_win)]
    exact = exact_shape(segs)
    ctx = {
        "segs": segs,
        "segs_near": segs_near,
        "exact": exact,
        "window": window,
        "out": a.out,
        "previews": a.previews.split(","),
        "render_crop": tuple(map(int, a.render_crop.split(","))),
    }
    ctx["grid_origin"] = grid_origin_from_stl(a.stl)
    ctx["today"] = load_bottom(a.stl, window.buffer(1))
    sim = grid_cells(exact, *ctx["grid_origin"], PITCH, window)
    w = window.buffer(-0.5)
    diff = ctx["today"].intersection(w).symmetric_difference(sim.intersection(w)).area
    print(f"grid origin {ctx['grid_origin']}; simulated vs STL 0.4 grid differ by {diff:.4f} mm^2 in the crop")
    only = set(filter(None, a.only.split(",")))
    want = lambda name: not only or name in only  # noqa: E731
    minx, miny, maxx, maxy = window.buffer(1).bounds
    fine = 0.03
    xs, ys = np.arange(minx, maxx, fine), np.arange(miny, maxy, fine)
    straight_near = straight_segments(segs_near)

    extent = max(abs(c) for s in segs for p in s for c in p)

    def taper(t):
        return R - 0.4 * np.sin(np.pi * t) ** 2

    # two strengths of the SKIMS-influenced strap: (label, caption, waist depth, blend width)
    skims = [("SKIMS-influenced, light", "joins melt 0.6 mm, 2.7 mm waist", 0.15, 0.6),
             ("SKIMS-influenced, strong", "joins melt 1.2 mm, 2.4 mm waist", 0.3, 1.2)]

    def waist_fn(depth):
        return lambda t: R - depth * np.sin(np.pi * t) ** 2

    if want("fig05"):
        ctx["taper_field"] = field_signed(straight_near, xs, ys, taper, extent=extent)
    if want("fig06"):
        ctx["skims_crop"] = [(lab, sub, field_signed(straight_near, xs, ys, waist_fn(d), blend=k, extent=extent))
                             for lab, sub, d, k in skims]
    if want("fig06b"):
        g = np.linspace(-49, 49, 817)  # symmetric about 0, so turns and mirrors land on grid points
        straight_all = straight_segments(segs)
        ctx["skims_full"] = [(lab, sub, field_signed(straight_all, g, g, waist_fn(d), blend=k, extent=extent))
                             for lab, sub, d, k in skims]
        X, Y, F = field_signed(straight_all, g, g, extent=extent)
        print("today (same grid) symmetry turn90=%.4f mirror=%.4f" % mask_sym(F))
    # the sharpest hole point in the crop: where today's steps stray furthest
    pts = geom_edge_points(ctx["today"])
    inner = window.buffer(-0.6)
    worst = max((p for p in pts if inner.contains(Point(p))), key=lambda p: exact.boundary.distance(Point(p)))
    near = exact.boundary.interpolate(exact.boundary.project(Point(worst)))
    ctx["tip"] = (near.x, near.y)
    for name, fn in (("fig00", fig00), ("fig01", fig01), ("fig02", fig02), ("fig03", fig03), ("fig04", fig04),
                     ("fig05", fig05), ("fig06", fig06), ("fig06b", fig06b), ("fig07", fig07), ("fig08", fig08)):
        if name == "fig08" and "today_stray" not in ctx:
            ctx["today_stray"] = stray(geom_edge_points(ctx["today"]), exact, window)
        if want(name):
            fn(ctx)
    for lab, t90, mir in ctx.get("skims_sym", []):
        print(f"{lab}: symmetry turn90={t90:.4f} mirror={mir:.4f}")
    print(f"today stray {ctx.get('today_stray')}; frame extent {extent}")


if __name__ == "__main__":
    main()
