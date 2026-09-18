#!/usr/bin/env python3
"""Render a sliced Bambu `.3mf` as an annotated coupon photo map: every coupon
drawn at its real placed silhouette, labelled, with a chosen subset ringed as
"photograph this".

The geometry is read, never eyeballed: object names from
`Metadata/model_settings.config`, plate placements + rotations from
`3D/3dmodel.model` (`<build>`), and per-object mesh bounds (all three axes) from
the referenced `3D/Objects/object_N.model`. Full placement composes the
build-item transform with the component transform in 3D, so a silhouette sits
where the part sits and stands as tall as the part stands.

Each object is reduced to its mesh-local bounding box (8 corners), placed into
plate space, and projected onto whichever orthographic plane a view asks for.
The silhouette is the convex hull of the projected corners — a schematic box
outline, **not** a photoreal render (bores, the fan cone, fillets do not show);
it locates each coupon and shows its height/footprint on that face, which is
what a bench operator needs to tell one coupon from another and find an
underside. The standalone map (`out`) is the top-down view — the one you carry.

*What* to ring is data, not code — it lives in a JSON sidecar (see
`docs/prints/plate-1-photo-map.json`) so the same tool serves any plate and the
photograph set stays reviewable next to the bench sheet it belongs to.

With `--contact-sheet <out.png>` it also emits a printable contact sheet: the
six annotated orthographic faces (top/bottom, front/back, left/right) in a grid
beside the preview angles BambuStudio bakes into the `.3mf` itself — the
isometric print thumbnail, the lit top view, and the object-id pick map. Those
baked thumbnails are the only *rendered* angles the slicer stores; the six
annotated faces are projected here from the geometry, box-silhouette only.

Usage: plate_photo_map.py <plate.3mf> <highlights.json> <out.png> [--contact-sheet <sheet.png>]

The sidecar shape:
  {
    "title":    "<banner text>",
    "footnote": "<small print under the legend>",
    "groups":   { "MC1": [r,g,b], ... },        # fill by name prefix (first 3 chars)
    "tiers":    { "1": {"color":[r,g,b], "width":9, "legend":"..."}, "2": {...} },
    "highlights": { "<object name>": {"tier": 1, "why": "..."}, ... }
  }
`why` is the rationale of record for each pick (read by a reviewer); the tool rings
by `tier`. A highlight naming an object the plate does not contain is an error, not
a silent skip — a stale sidecar should fail loudly.
"""
import argparse
import io
import json
import re
import sys
import zipfile

from PIL import Image, ImageDraw, ImageFont

# The baked previews to tile on the contact sheet, in order, with captions. Each
# is an angle BambuStudio renders into the sliced .3mf; a missing one is skipped.
BAKED_TILES = [
    ("Metadata/plate_1.png", "Slicer print thumbnail (isometric)"),
    ("Metadata/top_1.png", "Slicer top view"),
    ("Metadata/pick_1.png", "Object-id pick map"),
]

# The six orthographic faces, each a projection of a placed (X,Y,Z) point to
# (u,v) in maths coords (u right, v up). Front/back and left/right are mirror
# pairs so each reads as if you walked around the plate to that side; bottom is
# the top flipped left-right, as if you tipped the plate toward you. Grid order
# pairs each face with its opposite.
PROJECTIONS = {
    "top":    (lambda X, Y, Z: (X, Y),  "TOP  (as sliced / as it prints)"),
    "bottom": (lambda X, Y, Z: (-X, Y), "BOTTOM  (undersides: fan, bridges, tower feet)"),
    "front":  (lambda X, Y, Z: (X, Z),  "FRONT  (+Y toward you)"),
    "back":   (lambda X, Y, Z: (-X, Z), "BACK  (-Y toward you)"),
    "left":   (lambda X, Y, Z: (-Y, Z), "LEFT  (-X toward you)"),
    "right":  (lambda X, Y, Z: (Y, Z),  "RIGHT  (+X toward you)"),
}
GRID_ORDER = [["top", "bottom"], ["front", "back"], ["left", "right"]]

PAPER = (250, 249, 247)
INK = (20, 20, 20)
MUTE = (90, 90, 90)


def die(msg: str) -> None:
    print(f"plate_photo_map: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_xf3(s):
    """3mf transform: 9 rotation (row-major 3x3) + 3 translation -> (R 9-tuple, tx, ty, tz)."""
    v = [float(x) for x in s.split()]
    return ((v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8]), v[9], v[10], v[11])


def compose3(A, B):
    """A∘B : apply B, then A (column-vector convention, R rows contiguous)."""
    (a0, a1, a2, a3, a4, a5, a6, a7, a8), ax, ay, az = A
    (b0, b1, b2, b3, b4, b5, b6, b7, b8), bx, by, bz = B
    r = (a0 * b0 + a1 * b3 + a2 * b6, a0 * b1 + a1 * b4 + a2 * b7, a0 * b2 + a1 * b5 + a2 * b8,
         a3 * b0 + a4 * b3 + a5 * b6, a3 * b1 + a4 * b4 + a5 * b7, a3 * b2 + a4 * b5 + a5 * b8,
         a6 * b0 + a7 * b3 + a8 * b6, a6 * b1 + a7 * b4 + a8 * b7, a6 * b2 + a7 * b5 + a8 * b8)
    return (r,
            a0 * bx + a1 * by + a2 * bz + ax,
            a3 * bx + a4 * by + a5 * bz + ay,
            a6 * bx + a7 * by + a8 * bz + az)


def place3(xf, x, y, z):
    """Apply a composed (R, t) transform to a point -> plate-space (X, Y, Z)."""
    (r0, r1, r2, r3, r4, r5, r6, r7, r8), tx, ty, tz = xf
    return (r0 * x + r1 * y + r2 * z + tx,
            r3 * x + r4 * y + r5 * z + ty,
            r6 * x + r7 * y + r8 * z + tz)


def convex_hull(pts):
    """Andrew's monotone chain; returns hull CCW. Handles <=2 points."""
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def read_objects(z):
    """Read plate geometry -> list of {name, group, corners:[(X,Y,Z)]*8}."""
    # objectid -> name  (config lists id then its name metadata; pair them in order)
    cfg = z.read("Metadata/model_settings.config").decode("utf8", "replace")
    names = {}
    cur = None
    for m in re.finditer(r'object id="(\d+)"|<metadata key="name" value="([^"]*)"', cfg):
        if m.group(1):
            cur = m.group(1)
        elif cur and cur not in names:
            names[cur] = re.sub(r"\.stl$", "", m.group(2))

    model = z.read("3D/3dmodel.model").decode("utf8", "replace")
    items = {m.group(1): parse_xf3(m.group(2))
             for m in re.finditer(r'<item objectid="(\d+)"[^>]*transform="([^"]*)"', model)}
    comp = {}
    for m in re.finditer(
            r'<object id="(\d+)"[^>]*type="model">\s*<components>\s*'
            r'<component p:path="([^"]+)"\s+objectid="\d+"[^>]*transform="([^"]*)"',
            model, re.DOTALL):
        comp[m.group(1)] = (m.group(2).lstrip("/"), parse_xf3(m.group(3)))

    _bb = {}

    def mesh_bbox3(path):
        if path in _bb:
            return _bb[path]
        try:
            data = z.read(path).decode("utf8", "replace")
        except KeyError:
            _bb[path] = None
            return None
        xs, ys, zs = [], [], []
        for vm in re.finditer(r'<vertex x="([^"]*)" y="([^"]*)" z="([^"]*)"', data):
            xs.append(float(vm.group(1)))
            ys.append(float(vm.group(2)))
            zs.append(float(vm.group(3)))
        _bb[path] = (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)) if xs else None
        return _bb[path]

    objs = []
    for bid, item_xf in items.items():
        name = names.get(bid)
        if not name:
            continue
        path, cxf = comp.get(bid, (None, None))
        xf = compose3(item_xf, cxf) if cxf else item_xf
        bb = mesh_bbox3(path) if path else None
        if bb:
            x0, y0, z0, x1, y1, z1 = bb
        else:  # unreadable mesh: a small placeholder cube so the object still shows
            x0 = y0 = z0 = -2.0
            x1 = y1 = z1 = 2.0
        corners = [place3(xf, x, y, zc)
                   for x in (x0, x1) for y in (y0, y1) for zc in (z0, z1)]
        objs.append({"name": name, "group": name[:3], "corners": corners})

    if not objs:
        die("no placed objects found in the plate")
    return objs


def validate_highlights(objs, highlights):
    """A highlight naming no object on the plate is a stale sidecar — fail loudly."""
    present = {o["name"] for o in objs}
    missing = [n for n in highlights if n not in present]
    if missing:
        die("highlights name objects not on the plate (stale sidecar?): "
            + ", ".join(sorted(missing)))


def _short(name):
    return (name.replace("MC", "").replace("Tower", "T")
                .replace("Wall", "W").replace("Pin", "P"))


def project(objs, view):
    """Project every object's corners onto `view` -> list of (name, group, hull, (cu,cv))."""
    fn = PROJECTIONS[view][0]
    out = []
    for o in objs:
        pts = [fn(*c) for c in o["corners"]]
        hull = convex_hull(pts)
        cu = sum(p[0] for p in hull) / len(hull)
        cv = sum(p[1] for p in hull) / len(hull)
        out.append((o["name"], o["group"], hull, (cu, cv)))
    return out


def view_extent(objs, view):
    """(umin, umax, vmin, vmax) of a whole plate in one projection."""
    fn = PROJECTIONS[view][0]
    us, vs = [], []
    for o in objs:
        for c in o["corners"]:
            u, v = fn(*c)
            us.append(u)
            vs.append(v)
    return min(us), max(us), min(vs), max(vs)


def draw_panel(objs, view, scale, cfg_spec, cell_w, cell_h, pad, label_font,
               caption=True, label_mode="all"):
    """Draw one orthographic face into a (cell_w x cell_h) image and return it.

    `label_mode` "all" labels every coupon (top/bottom, where ids are legible);
    "highlighted" labels only the ringed coupons (elevations, where every coupon
    stacks on one baseline and a full label set is an unreadable smear)."""
    groups = {k: tuple(v) for k, v in cfg_spec.get("groups", {}).items()}
    tiers = {int(k): v for k, v in cfg_spec.get("tiers", {}).items()}
    highlights = cfg_spec.get("highlights", {})

    umin, umax, vmin, vmax = view_extent(objs, view)
    cap_h = 30 if caption else 0
    content_h = cell_h - cap_h
    # centre the projected content in the cell
    off_u = (cell_w - (umax - umin) * scale) / 2
    off_v = (content_h - (vmax - vmin) * scale) / 2

    def to_px(u, v):
        return (off_u + (u - umin) * scale,
                content_h - off_v - (v - vmin) * scale)   # flip v (up == image up)

    img = Image.new("RGB", (cell_w, cell_h), PAPER)
    d = ImageDraw.Draw(img)
    if caption:
        d.text((4, content_h + 6), PROJECTIONS[view][1], fill=MUTE, font=font(15))
        d.line([(0, content_h), (cell_w, content_h)], fill=(225, 225, 225), width=1)

    for name, grp, hull, (cu, cv) in project(objs, view):
        poly = [to_px(*p) for p in hull]
        fill = groups.get(grp, (150, 150, 150))
        if len(poly) >= 3:
            d.polygon(poly, fill=fill, outline=(40, 40, 40))
        else:  # degenerate (edge-on): draw a thin line so it is not invisible
            d.line(poly, fill=fill, width=3)
        hit = highlights.get(name)
        if hit and len(poly) >= 2:
            tier = tiers.get(int(hit["tier"]), {})
            d.line(poly + [poly[0]], fill=tuple(tier.get("color", (220, 40, 40))),
                   width=int(tier.get("width", 6)), joint="curve")
        if label_mode == "highlighted" and not hit:
            continue
        short = _short(name)
        tb = d.textbbox((0, 0), short, font=label_font)
        lx, lv = to_px(cu, cv)
        d.text((lx - (tb[2] - tb[0]) / 2, lv - (tb[3] - tb[1]) / 2), short,
               fill=(255, 255, 255), font=label_font)
    return img


def draw_legend(d, x, y, cfg_spec, w_font, s_font):
    """Draw the tier legend + footnote at (x, y); return the y below it."""
    tiers = {int(k): v for k, v in cfg_spec.get("tiers", {}).items()}
    for tier_key in sorted(tiers):
        t = tiers[tier_key]
        col = tuple(t.get("color", (220, 40, 40)))
        d.ellipse([x, y, x + 24, y + 24], outline=col, width=5)
        d.text((x + 34, y + 2), t.get("legend", ""), fill=INK, font=w_font)
        y += 40
    if cfg_spec.get("footnote"):
        d.text((x, y + 4), cfg_spec["footnote"], fill=MUTE, font=s_font)
        y += 26
    return y


def render_top_map(z, cfg_spec):
    """The standalone deliverable: the top-down face + title + legend."""
    objs = read_objects(z)
    validate_highlights(objs, cfg_spec.get("highlights", {}))

    PAD_MM, W = 14, 1600
    umin, umax, vmin, vmax = view_extent(objs, "top")
    scale = (W - 2) / ((umax - umin) + 2 * PAD_MM)
    content_h = int(((vmax - vmin) + 2 * PAD_MM) * scale) + 2

    panel = draw_panel(objs, "top", scale, cfg_spec, W, content_h, PAD_MM * scale,
                       font(15), caption=False)
    img = Image.new("RGB", (W, content_h + 40 + 150), PAPER)
    img.paste(panel, (0, 40))
    d = ImageDraw.Draw(img)
    d.text((16, 6), cfg_spec.get("title", "Plate — what to photograph"), fill=INK, font=font(30))
    draw_legend(d, 18, content_h + 60, cfg_spec, font(19), font(15))

    n_hl = sum(1 for o in objs if o["name"] in cfg_spec.get("highlights", {}))
    return img, len(objs), n_hl


def build_contact_sheet(z, cfg_spec):
    """Printable sheet: baked slicer thumbnails, then the six annotated faces."""
    W, MARGIN, GAP = 1600, 40, 24
    objs = read_objects(z)
    validate_highlights(objs, cfg_spec.get("highlights", {}))

    # --- baked thumbnail strip (raw slicer renders), captioned
    tiles = []
    for path, cap in BAKED_TILES:
        try:
            raw = z.read(path)
        except KeyError:
            continue
        tiles.append((Image.open(io.BytesIO(raw)).convert("RGBA"), cap))

    # --- six orthographic faces: one shared scale so faces compare fairly, but
    # each row sized to its own content height (an elevation of flat coupons is a
    # short band — it must not inherit the tall top/bottom cell and waste the page).
    cell_w = (W - 2 * MARGIN - GAP) // 2
    PAD, CAP_H = 16, 30
    max_w = max((view_extent(objs, v)[1] - view_extent(objs, v)[0]) for v in PROJECTIONS)
    scale = (cell_w - 2 * PAD) / max_w
    row_h = []
    for row in GRID_ORDER:
        rmax_h = max((view_extent(objs, v)[3] - view_extent(objs, v)[2]) for v in row)
        row_h.append(int(rmax_h * scale) + 2 * PAD + CAP_H)

    header_h = 58
    if tiles:
        n = len(tiles)
        tcell = (W - 2 * MARGIN - (n - 1) * GAP) // n
        strip_h = tcell + 34
    else:
        tcell = strip_h = 0

    grid_h = sum(row_h) + (len(GRID_ORDER) - 1) * GAP
    legend_h = 130
    H = header_h + (strip_h + GAP if tiles else 0) + 40 + grid_h + legend_h + MARGIN

    sheet = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(sheet)
    title = cfg_spec.get("title", "Plate").split(" · ")[0] + " · print contact sheet"
    d.text((MARGIN, 14), title, fill=INK, font=font(30))

    y = header_h
    if tiles:
        for i, (im, cap) in enumerate(tiles):
            x = MARGIN + i * (tcell + GAP)
            thumb = im.resize((tcell, tcell), Image.LANCZOS)
            bg = Image.new("RGB", (tcell, tcell), (255, 255, 255))
            bg.paste(thumb, (0, 0), thumb)
            sheet.paste(bg, (x, y))
            d.rectangle([x, y, x + tcell - 1, y + tcell - 1], outline=(180, 180, 180))
            d.text((x + 2, y + tcell + 8), cap, fill=MUTE, font=font(15))
        y += strip_h + GAP

    d.text((MARGIN, y + 6), "Six annotated faces — projected from the geometry (box silhouettes)",
           fill=INK, font=font(20))
    y += 40

    label_font = font(13)
    for ri, row in enumerate(GRID_ORDER):
        cell_h = row_h[ri]
        # top/bottom carry the id labels; elevations label only the ringed coupons
        mode = "all" if row[0] in ("top", "bottom") else "highlighted"
        for col, view in enumerate(row):
            x = MARGIN + col * (cell_w + GAP)
            panel = draw_panel(objs, view, scale, cfg_spec, cell_w, cell_h, PAD,
                               label_font, caption=True, label_mode=mode)
            sheet.paste(panel, (x, y))
            d.rectangle([x, y, x + cell_w - 1, y + cell_h - 1], outline=(210, 210, 210))
        y += cell_h + GAP

    draw_legend(d, MARGIN, y + 6, cfg_spec, font(19), font(15))
    return sheet


def main() -> None:
    ap = argparse.ArgumentParser(description="Render a sliced .3mf as a coupon photo map.")
    ap.add_argument("plate", help="sliced Bambu .3mf")
    ap.add_argument("highlights", help="JSON sidecar: what to ring (see docstring)")
    ap.add_argument("out", help="output PNG for the annotated top-down map")
    ap.add_argument("--contact-sheet", metavar="PNG",
                    help="also write a printable contact sheet: baked thumbnails + six annotated faces")
    args = ap.parse_args()

    try:
        cfg_spec = json.loads(open(args.highlights, encoding="utf8").read())
    except (OSError, ValueError) as e:
        die(f"cannot read highlights sidecar {args.highlights}: {e}")

    try:
        z = zipfile.ZipFile(args.plate)
    except (OSError, zipfile.BadZipFile) as e:
        die(f"cannot open plate {args.plate}: {e}")

    photo_map, n_obj, n_hl = render_top_map(z, cfg_spec)
    photo_map.save(args.out)
    print(f"wrote {args.out}  ({n_obj} objects, {n_hl} highlighted)")

    if args.contact_sheet:
        sheet = build_contact_sheet(z, cfg_spec)
        sheet.save(args.contact_sheet)
        print(f"wrote {args.contact_sheet}  (contact sheet {sheet.width}x{sheet.height})")


if __name__ == "__main__":
    main()
