#!/usr/bin/env python3
"""grid_plate.py — place N copies of ONE mesh on an EVEN, equi-spaced grid, baked into a .3mf.

WHY THIS EXISTS (provenance, 2026-09-18):
  `bambu slice … --arrange` runs libnest2d, which packs *tight* (fills from a region to minimise
  bed use) — the right tool for a production plate, the wrong one for a *display* layout where the
  ask is "spread N copies evenly with breathing room and a margin around the edge". An even grid is
  deterministic placement, which a nester cannot express. This tool computes the grid from the
  shape's own footprint and the bed, then writes a .3mf whose <build> instances the single mesh at
  each grid position. Slice it with `bambu slice plate <grid>.3mf` and NO --arrange, so BambuStudio
  keeps the authored positions.

THE PRINCIPLE (default guidance for spacing multiple pieces — see best-practices.md "Our examples"):
  Divide the bed into N equal cells per axis and CENTRE one piece in each cell. With bed B, piece
  footprint f, and N cells on an axis:
      pitch        = B / N
      cell centres = pitch * (i + 0.5),  i = 0 … N-1
      gap (edge→edge between pieces) = pitch - f
      edge margin  (piece → bed wall) = (pitch - f) / 2  =  gap / 2
  So the inter-piece gaps are all equal AND the margin to the wall is half a gap — the layout reads
  as uniformly spaced, and it always leaves an edge margin. It uses the WHOLE bed for a given N, so
  it is the maximum even spread at that count. The grid dimension is DERIVED FROM SHAPE SIZE: the
  most cells that still fit a min gap is  N = floor(B / (f + min_gap)); pass --rows/--cols for a
  target count (e.g. 5x5), or --count to auto-pick a near-square grid.

  Requires pitch >= f (else pieces overlap): the tool refuses a grid that would collide.

Usage:
  grid_plate.py <model.stl> --out <plate.3mf> [--rows R --cols C | --count N]
                [--bed 256] [--min-gap 8] [--margin M]
  --bed      bed size in mm (square), default 256 (X2D build area, D-053)
  --min-gap  minimum edge-to-edge gap when auto-deriving the grid, mm (default 8)
  --margin   force a fixed edge margin instead of the even gap/2 (mm); the grid then spans
             (B - 2*margin) and centres within it — use when a specific wall clearance is required
  --rows/--cols  explicit grid (a target count, e.g. --rows 5 --cols 5 = 25)
  --count    total copies; the grid is the near-square RxC that holds them, derived from footprint

Only STL input (binary or ASCII) is supported; convert a .3mf/.step to STL first if needed.
"""
import argparse
import math
import struct
import sys
import xml.sax.saxutils as sx
import zipfile


def read_stl(path):
    """Return (triangles, (minx,miny,minz), (maxx,maxy,maxz)). triangles = list of 3 (x,y,z) tuples."""
    with open(path, "rb") as fh:
        data = fh.read()
    tris = []
    # Binary STL is exactly 84 + 50*n bytes. Detect by that identity (a binary file can still start
    # with "solid", so size — not the header word — is the reliable discriminator).
    if len(data) >= 84:
        n = struct.unpack_from("<I", data, 80)[0]
        if len(data) == 84 + 50 * n:
            off = 84
            for _ in range(n):
                # 12 floats: normal(3) + v1(3) + v2(3) + v3(3), then 2-byte attr
                vals = struct.unpack_from("<12f", data, off)
                tris.append((vals[3:6], vals[6:9], vals[9:12]))
                off += 50
            return _bounds(tris)
    # ASCII STL fallback.
    text = data.decode("utf-8", "replace")
    verts = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("vertex"):
            _, x, y, z = line.split()[:4]
            verts.append((float(x), float(y), float(z)))
            if len(verts) == 3:
                tris.append((verts[0], verts[1], verts[2]))
                verts = []
    if not tris:
        sys.exit(f"no triangles read from {path} — not a valid STL?")
    return _bounds(tris)


def _bounds(tris):
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    return tris, (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def near_square(n):
    """Rows x cols holding n, as square as possible (cols >= rows)."""
    r = int(math.isqrt(n))
    while r > 1 and n % r:
        r -= 1
    c = math.ceil(n / r)
    return r, c


def main():
    ap = argparse.ArgumentParser(description="Place N copies of one mesh on an even grid, into a .3mf.")
    ap.add_argument("model")
    ap.add_argument("--out", required=True)
    ap.add_argument("--rows", type=int)
    ap.add_argument("--cols", type=int)
    ap.add_argument("--count", type=int)
    ap.add_argument("--bed", type=float, default=256.0)
    ap.add_argument("--min-gap", type=float, default=8.0)
    ap.add_argument("--margin", type=float, default=None)
    ap.add_argument("--name", default=None, help="object name written into the .3mf (default: model basename)")
    args = ap.parse_args()

    import os
    obj_name = args.name or os.path.splitext(os.path.basename(args.model))[0]

    tris, lo, hi = read_stl(args.model)
    fx = hi[0] - lo[0]
    fy = hi[1] - lo[1]
    cx = (lo[0] + hi[0]) / 2.0
    cy = (lo[1] + hi[1]) / 2.0

    # Derive the grid. Explicit rows/cols win; else --count → near-square; else auto-fit from footprint.
    if args.rows and args.cols:
        rows, cols = args.rows, args.cols
    elif args.count:
        rows, cols = near_square(args.count)
    else:
        cols = max(1, int((args.bed) // (fx + args.min_gap)))
        rows = max(1, int((args.bed) // (fy + args.min_gap)))

    # Span the bed (or the bed minus a forced margin) and centre each piece in an equal cell.
    span = args.bed if args.margin is None else args.bed - 2 * args.margin
    base = 0.0 if args.margin is None else args.margin
    pitch_x = span / cols
    pitch_y = span / rows
    gap_x = pitch_x - fx
    gap_y = pitch_y - fy
    if gap_x < 0 or gap_y < 0:
        sys.exit(
            f"grid {rows}x{cols} overlaps: pitch {pitch_x:.1f}x{pitch_y:.1f} mm < footprint "
            f"{fx:.1f}x{fy:.1f} mm on the {args.bed:.0f} mm bed. Use fewer copies or a bigger bed."
        )

    n = rows * cols
    edge_x = base + (pitch_x - fx) / 2.0 if args.margin is None else args.margin
    edge_y = base + (pitch_y - fy) / 2.0 if args.margin is None else args.margin
    print(
        f"grid: {rows}x{cols} = {n} copies · footprint {fx:.1f}x{fy:.1f} mm · bed {args.bed:.0f} mm\n"
        f"  pitch {pitch_x:.1f}x{pitch_y:.1f} mm · gap {gap_x:.1f}x{gap_y:.1f} mm · "
        f"edge margin {edge_x:.1f}x{edge_y:.1f} mm"
    )

    # Build the single shared mesh once; instance it N times in <build> (mesh stored once, D-052).
    vbuf = []
    tbuf = []
    idx = {}
    for t in tris:
        ti = []
        for v in t:
            key = (round(v[0], 5), round(v[1], 5), round(v[2], 5))
            j = idx.get(key)
            if j is None:
                j = len(vbuf)
                idx[key] = j
                vbuf.append(v)
            ti.append(j)
        tbuf.append(ti)
    verts_xml = "".join(f'<vertex x="{v[0]:.5f}" y="{v[1]:.5f}" z="{v[2]:.5f}"/>' for v in vbuf)
    tris_xml = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in tbuf)

    items = []
    for r in range(rows):
        for c in range(cols):
            tcx = base + pitch_x * (c + 0.5)
            tcy = base + pitch_y * (r + 0.5)
            tx = tcx - cx
            ty = tcy - cy
            tz = -lo[2]  # drop each instance so its base sits on the plate (z=0)
            items.append(f'<item objectid="1" transform="1 0 0 0 1 0 0 0 1 {tx:.5f} {ty:.5f} {tz:.5f}"/>')

    model = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n'
        " <resources>\n"
        f'  <object id="1" type="model" name={sx.quoteattr(obj_name)}><mesh>'
        f"<vertices>{verts_xml}</vertices><triangles>{tris_xml}</triangles>"
        "</mesh></object>\n"
        " </resources>\n"
        " <build>\n  " + "\n  ".join(items) + "\n </build>\n"
        "</model>\n"
    )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
        "</Types>\n"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
        'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
        "</Relationships>\n"
    )

    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("3D/3dmodel.model", model)
    print(f"wrote {args.out} ({n} instances, {len(vbuf)} verts / {len(tbuf)} tris in one mesh)")


if __name__ == "__main__":
    main()
