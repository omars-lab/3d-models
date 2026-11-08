#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "trimesh", "rtree"]
# ///
"""Measure a hollow round shell (an orb, a lattice ball) for printing with supports only from the bed.

    uv run tools/orb_support_survey.py <mesh.stl> [<mesh.stl> ...] [--gate-log <stem>=<log>] [--json]
    uv run tools/orb_support_survey.py --self-test

Written for docs/design/orb/whole-orb-outside-supports-design.md, which explains every number this
prints. Per mesh, in the mesh's own orientation (+z up, the bed under the lowest point):

- **frame**: the shell's centre (a least-squares sphere fit to the vertices) and its inner and outer
  radius (the 3rd and 97th percentile of vertex distance from that centre).
- **bed**: the area of the cross-section 0.1 mm above the lowest point, the middle of a 0.2 mm first
  layer.
- **rings**: the top half read at 35 latitudes, every 2.5 degrees from 2.5 to 87.5, each at five
  depths through the wall (5% in from each face), keeping the depth that holds the most material
  (on a faceted shell the outer depths can miss the flat faces). The ring is sampled every
  0.05 mm: the share of the ring that is material, the
  width of each strut crossing (arc length along the ring) and the width of each gap, as the
  straight line across it (the chord), which is the span a bridge would have to cross. A woven
  ribbon bows in and out of the wall, so at its crossings one depth can read a gap another depth
  fills: for woven orbs the gap figures lean high.
- **overhangs**: the faces in the top half that face down more steeply than the slicer's support
  threshold (Bambu Studio's `support_threshold_angle`, 30 degrees from level in the X2D 0.20 mm
  Standard profile; `--threshold-deg` to change it). Each is sorted by where a support grown
  straight down under it would go: *inside* (the column passes through the hollow, because the face
  sits nearer the vertical axis than the inner wall), split into those that land on the inside wall
  and those that drop through a gap in the bottom half to the bed; or *outside*, split into those
  that land on the model and those that reach the bed. A straight-down column is a simplification:
  tree supports lean, so this is where support *starts* to be needed, not the path a slicer draws.
- **F3 above the equator** (with `--gate-log`): how many of bikar's "material starts in mid-air"
  starts sit above the centre, read from a `bikar render --check print` log.

Read third-party meshes as data only. This tool writes nothing but its report.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys

import numpy as np
import trimesh

RING_LATITUDES_DEG = [2.5 * k for k in range(1, 36)]
SAMPLE_STEP_MM = 0.05
WALL_SAMPLES = 5
FIRST_LAYER_MID_MM = 0.1
DEFAULT_THRESHOLD_DEG = 30.0


def shell_frame(mesh: trimesh.Trimesh) -> dict:
    """Centre and inner/outer radius of a round shell."""
    v = mesh.vertices
    a = np.c_[2 * v, np.ones(len(v))]
    b = (v**2).sum(axis=1)
    sol, *_ = np.linalg.lstsq(a, b, rcond=None)
    centre = sol[:3]
    dist = np.linalg.norm(v - centre, axis=1)
    return {
        "centre": centre,
        "r_in": float(np.percentile(dist, 3)),
        "r_out": float(np.percentile(dist, 97)),
    }


def slice_segments(mesh: trimesh.Trimesh, z: float) -> np.ndarray:
    """The cross-section at height z as 2D segments, shape (m, 2, 2)."""
    segs = trimesh.intersections.mesh_plane(mesh, plane_normal=[0, 0, 1], plane_origin=[0, 0, z])
    return np.asarray(segs)[:, :, :2] if len(segs) else np.zeros((0, 2, 2))


def inside_2d(points: np.ndarray, segs: np.ndarray) -> np.ndarray:
    """Even-odd test of 2D points against closed slice loops (a ray toward +x)."""
    if len(segs) == 0:
        return np.zeros(len(points), dtype=bool)
    ax, ay = segs[:, 0, 0], segs[:, 0, 1]
    bx, by = segs[:, 1, 0], segs[:, 1, 1]
    out = np.zeros(len(points), dtype=bool)
    for start in range(0, len(points), 2000):
        px = points[start:start + 2000, 0:1]
        py = points[start:start + 2000, 1:2]
        straddle = (ay > py) != (by > py)
        with np.errstate(divide="ignore", invalid="ignore"):
            cross_x = ax + (py - ay) * (bx - ax) / (by - ay)
        hits = straddle & (px < cross_x)
        out[start:start + 2000] = hits.sum(axis=1) % 2 == 1
    return out


def runs(mask: np.ndarray) -> tuple[list[int], list[int]]:
    """Lengths of the material runs and the void runs around a closed ring."""
    if mask.all() or not mask.any():
        whole = [len(mask)]
        return (whole, []) if mask.all() else ([], whole)
    shift = int(np.argmax(mask != mask[0]))
    rolled = np.roll(mask, -shift)
    edges = np.flatnonzero(np.diff(rolled.astype(int))) + 1
    pieces = np.split(rolled, edges)
    material = [len(p) for p in pieces if p[0]]
    void = [len(p) for p in pieces if not p[0]]
    return material, void


def wall_depths(frame) -> np.ndarray:
    """Five distances from the centre, spread through the wall, 5% in from each face."""
    r_in, r_out = frame["r_in"], frame["r_out"]
    t = r_out - r_in
    return np.linspace(r_in + 0.05 * t, r_out - 0.05 * t, WALL_SAMPLES)


def ring_mask(mesh, frame, lat_deg, depth):
    """Material-or-not around the ring at one latitude and one depth in the wall, and its radius."""
    c = frame["centre"]
    phi = math.radians(lat_deg)
    rho = depth * math.cos(phi)
    n = max(int(2 * math.pi * rho / SAMPLE_STEP_MM), 64)
    theta = np.linspace(0, 2 * math.pi, n, endpoint=False)
    pts = np.c_[c[0] + rho * np.cos(theta), c[1] + rho * np.sin(theta)]
    return inside_2d(pts, slice_segments(mesh, c[2] + depth * math.sin(phi))), rho


def chord(steps: int, n: int, rho: float) -> float:
    """Straight-line width across a gap of `steps` samples out of `n` around a ring of radius rho."""
    angle = 2 * math.pi * steps / n
    return 2 * rho if angle >= math.pi else 2 * rho * math.sin(angle / 2)


def ring_profile(mesh, frame, lat_deg) -> dict:
    """Share covered, strut widths and gap widths round one latitude, at the best-covered depth.

    Five depths through the wall are read, and the one holding the most material is kept: on a
    faceted shell the vertex radii overshoot the flat faces (Dodeca-Orb's outer radius reads 61.2 mm
    where its faces sit at 59.5 mm), so the outer depths can miss the wall and read one ring-wide
    "gap". Keeping the best depth makes every gap here a lower bound on the span to bridge."""
    best = None
    for depth in wall_depths(frame):
        mask, rho = ring_mask(mesh, frame, lat_deg, depth)
        if best is None or mask.mean() > best[0].mean():
            best = (mask, rho)
    mask, rho = best
    n = len(mask)
    material, void = runs(mask)
    struts = [m * 2 * math.pi * rho / n for m in material] if void else []
    gaps = [chord(v, n, rho) for v in void]
    return {"lat": lat_deg, "coverage": float(mask.mean()), "struts_mm": struts, "gaps_mm": gaps}


def classify_overhangs(mesh, frame, threshold_deg) -> dict:
    """Area of the top half's steep down-facing faces, by where a straight-down support would go."""
    c = frame["centre"]
    normals, centres, areas = mesh.face_normals, mesh.triangles_center, mesh.area_faces
    steep = (normals[:, 2] < -math.cos(math.radians(threshold_deg))) & (centres[:, 2] > c[2] + 0.5)
    idx = np.flatnonzero(steep)
    origins = centres[idx] - [0, 0, 0.01]
    hit = mesh.ray.intersects_any(origins, np.tile([0.0, 0.0, -1.0], (len(idx), 1)))
    d_axis = np.linalg.norm(centres[idx, :2] - c[:2], axis=1)
    inside = d_axis < frame["r_in"]
    a = areas[idx]
    return {
        "threshold_deg": threshold_deg,
        "inside_lands_on_wall_mm2": float(a[inside & hit].sum()),
        "inside_drops_to_bed_mm2": float(a[inside & ~hit].sum()),
        "outside_lands_on_model_mm2": float(a[~inside & hit].sum()),
        "outside_reaches_bed_mm2": float(a[~inside & ~hit].sum()),
    }


def bed_contact(mesh) -> float:
    """First-layer contact area, by counting 0.05 mm grid points inside the cross-section."""
    segs = slice_segments(mesh, mesh.bounds[0][2] + FIRST_LAYER_MID_MM)
    if len(segs) == 0:
        return 0.0
    pts = segs.reshape(-1, 2)
    step = SAMPLE_STEP_MM
    xs = np.arange(pts[:, 0].min(), pts[:, 0].max() + step, step) + step / 2
    ys = np.arange(pts[:, 1].min(), pts[:, 1].max() + step, step) + step / 2
    grid = np.array(np.meshgrid(xs, ys)).reshape(2, -1).T
    return float(inside_2d(grid, segs).sum() * step * step)


def f3_above(log_path: str, centre_z: float) -> tuple[int, int]:
    """(F3 starts above the centre, all F3 starts) from a bikar --check print log."""
    pattern = re.compile(r"F3: material starts in mid-air at z=(-?[\d.]+)mm[^(]*(?:\(and (\d+) more)?")
    above = total = 0
    with open(log_path) as fh:
        for line in fh:
            m = pattern.search(line)
            if not m:
                continue
            count = 1 + int(m.group(2) or 0)
            total += count
            above += count if float(m.group(1)) > centre_z else 0
    return above, total


def summarise(rings: list[dict]) -> dict:
    struts = [s for r in rings for s in r["struts_mm"]]
    gaps = [g for r in rings for g in r["gaps_mm"]]
    cover = [r["coverage"] for r in rings]
    return {
        "coverage_min": min(cover),
        "coverage_max": max(cover),
        "strut_p10_mm": float(np.percentile(struts, 10)) if struts else None,
        "strut_median_mm": statistics.median(struts) if struts else None,
        "strut_p90_mm": float(np.percentile(struts, 90)) if struts else None,
        "gap_median_mm": statistics.median(gaps) if gaps else 0.0,
        "gap_max_mm": max(gaps) if gaps else 0.0,
        "gap_count": len(gaps),
    }


def survey(path: str, threshold_deg: float, gate_log: str | None) -> dict:
    mesh = trimesh.load_mesh(path)
    frame = shell_frame(mesh)
    rings = [ring_profile(mesh, frame, lat) for lat in RING_LATITUDES_DEG]
    out = {
        "mesh": path.rsplit("/", 1)[-1],
        "size_mm": [float(x) for x in mesh.extents],
        "r_in_mm": frame["r_in"],
        "r_out_mm": frame["r_out"],
        "bed_mm2": bed_contact(mesh),
        **summarise(rings),
        **classify_overhangs(mesh, frame, threshold_deg),
        "rings": rings,
    }
    if gate_log:
        out["f3_above"], out["f3_total"] = f3_above(gate_log, float(frame["centre"][2]))
    return out


def fmt_row(r: dict) -> str:
    f3 = f"{r['f3_above']}/{r['f3_total']}" if "f3_above" in r else "-"
    strut = (
        f"{r['strut_p10_mm']:.1f} / {r['strut_median_mm']:.1f} / {r['strut_p90_mm']:.1f}" if r["strut_p10_mm"] else "-"
    )
    return (
        f"| {r['mesh']} | {r['size_mm'][0]:.0f} | {r['r_in_mm']:.1f}-{r['r_out_mm']:.1f} | {r['bed_mm2']:.1f} "
        f"| {strut} | {100 * r['coverage_min']:.0f}-{100 * r['coverage_max']:.0f}% "
        f"| {r['gap_median_mm']:.1f} | {r['gap_max_mm']:.1f} | {f3} "
        f"| {r['inside_lands_on_wall_mm2']:.0f} | {r['inside_drops_to_bed_mm2']:.0f} "
        f"| {r['outside_lands_on_model_mm2']:.0f} | {r['outside_reaches_bed_mm2']:.0f} |"
    )


HEADER = (
    "| mesh | width mm | shell radius mm | bed mm² | strut crossing mm (10th / median / 90th pct) | ring covered "
    "| gap median mm | gap max mm | F3 above equator | inside, lands on wall mm² | inside, drops to bed mm² "
    "| outside, lands on model mm² | outside, reaches bed mm² |\n" + "|---" * 13 + "|"
)


def shell_fixture(r_in=18.0, r_out=20.0) -> trimesh.Trimesh:
    """A closed hollow sphere with no gaps: outer ball plus an inside-out inner ball."""
    outer = trimesh.creation.icosphere(subdivisions=4, radius=r_out)
    inner = trimesh.creation.icosphere(subdivisions=4, radius=r_in)
    inner.invert()
    return trimesh.util.concatenate([outer, inner])


def strut_fixture(count=8, width=2.0, rho=16.44, z=9.5) -> trimesh.Trimesh:
    """`count` closed boxes, `width` mm across, standing round a ring of radius rho at height z."""
    boxes = []
    for k in range(count):
        angle = 2 * math.pi * k / count
        box = trimesh.creation.box(extents=[3.0, width, 2.0])
        box.apply_translation([rho, 0, z])
        box.apply_transform(trimesh.transformations.rotation_matrix(angle, [0, 0, 1]))
        boxes.append(box)
    return trimesh.util.concatenate(boxes)


def self_test() -> int:
    mesh = shell_fixture()
    frame = shell_frame(mesh)
    assert abs(frame["r_in"] - 18.0) < 0.2 and abs(frame["r_out"] - 20.0) < 0.2, frame
    rings = [ring_profile(mesh, frame, lat) for lat in (10.0, 45.0, 80.0)]
    assert all(r["coverage"] > 0.99 and not r["gaps_mm"] for r in rings), rings
    over = classify_overhangs(mesh, frame, DEFAULT_THRESHOLD_DEG)
    # A gapless shell's inner ceiling is all "inside, lands on the wall": a cap of the inner
    # sphere steeper than 30 degrees, area 2*pi*r^2*(1-sin 60) = 273 mm² at r=18.
    assert abs(over["inside_lands_on_wall_mm2"] - 273) < 15, over
    assert over["inside_drops_to_bed_mm2"] < 1 and over["outside_lands_on_model_mm2"] < 1, over
    # By design: eight 2 mm struts round a ring leave eight gaps at the kept depth, each
    # 10.1 mm (innermost depth) to 11.3 mm (outermost) straight across.
    ring = ring_profile(strut_fixture(), {"centre": np.zeros(3), "r_in": 18.0, "r_out": 20.0}, 30.0)
    assert len(ring["gaps_mm"]) == 8, ring
    assert all(10.0 < g < 11.45 for g in ring["gaps_mm"]), ring
    assert all(abs(s - 2.0) < 0.2 for s in ring["struts_mm"]), ring
    print("orb_support_survey self-test: ok")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("meshes", nargs="*")
    ap.add_argument("--threshold-deg", type=float, default=DEFAULT_THRESHOLD_DEG)
    ap.add_argument("--gate-log", action="append", default=[], help="<mesh file name>=<bikar log>")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_intermixed_args(argv)
    if args.self_test:
        return self_test()
    logs = dict(item.split("=", 1) for item in args.gate_log)
    results = [survey(p, args.threshold_deg, logs.get(p.rsplit("/", 1)[-1])) for p in args.meshes]
    if args.json:
        print(json.dumps(results, indent=1))
        return 0
    print(HEADER)
    for r in results:
        print(fmt_row(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
