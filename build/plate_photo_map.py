#!/usr/bin/env python3
"""Render a sliced Bambu `.3mf` as a top-down photo map: every coupon drawn at its
real plate footprint, labelled, with a chosen subset ringed as "photograph this".

The geometry is read, never eyeballed: object names from `Metadata/model_settings.config`,
plate placements + rotations from `3D/3dmodel.model` (`<build>`), and per-object mesh
bounds from the referenced `3D/Objects/object_N.model`. Full placement composes the
build-item transform with the component transform, so a label sits where the part sits.

*What* to ring is data, not code — it lives in a JSON sidecar (see
`docs/prints/plate-1-photo-map.json`) so the same tool serves any plate and the
photograph set stays reviewable next to the bench sheet it belongs to.

With `--contact-sheet <out.png>` it also emits a printable contact sheet: the
annotated map (the only tile carrying the "shoot this" rings) beside the preview
angles BambuStudio bakes into the `.3mf` itself — the isometric print thumbnail,
the lit top view, and the object-id pick map. Those baked thumbnails are the only
angles the slicer stores; a true turntable (front/side/back) is not in the file.

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
PAPER = (250, 249, 247)
INK = (20, 20, 20)
MUTE = (90, 90, 90)


def die(msg: str) -> None:
    print(f"plate_photo_map: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_xf(s):
    """3mf transform: 9 rotation (row-major 3x3) + 3 translation -> (2x2 XY rot, tx, ty)."""
    v = [float(x) for x in s.split()]
    return ((v[0], v[1], v[3], v[4]), v[9], v[10])


def compose(A, B):
    """A∘B : apply B, then A. Each is ((r00,r01,r10,r11), tx, ty)."""
    (a00, a01, a10, a11), ax, ay = A
    (b00, b01, b10, b11), bx, by = B
    r = (a00 * b00 + a01 * b10, a00 * b01 + a01 * b11,
         a10 * b00 + a11 * b10, a10 * b01 + a11 * b11)
    return (r, a00 * bx + a01 * by + ax, a10 * bx + a11 * by + ay)


def font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def render_photo_map(z, cfg_spec):
    """Read the plate geometry and return the annotated top-down map as a PIL Image."""
    groups = {k: tuple(v) for k, v in cfg_spec.get("groups", {}).items()}
    tiers = {int(k): v for k, v in cfg_spec.get("tiers", {}).items()}
    highlights = cfg_spec.get("highlights", {})

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

    # build item BID -> item transform
    items = {m.group(1): parse_xf(m.group(2))
             for m in re.finditer(r'<item objectid="(\d+)"[^>]*transform="([^"]*)"', model)}

    # BID -> (mesh file path, component transform). Each build object wraps one
    # component that points at the real mesh in 3D/Objects/object_N.model.
    comp = {}
    for m in re.finditer(
            r'<object id="(\d+)"[^>]*type="model">\s*<components>\s*'
            r'<component p:path="([^"]+)"\s+objectid="\d+"[^>]*transform="([^"]*)"',
            model, re.DOTALL):
        comp[m.group(1)] = (m.group(2).lstrip("/"), parse_xf(m.group(3)))

    _bb = {}

    def mesh_bbox(path):
        if path in _bb:
            return _bb[path]
        try:
            data = z.read(path).decode("utf8", "replace")
        except KeyError:
            _bb[path] = None
            return None
        xs, ys = [], []
        for vm in re.finditer(r'<vertex x="([^"]*)" y="([^"]*)"', data):
            xs.append(float(vm.group(1)))
            ys.append(float(vm.group(2)))
        _bb[path] = (min(xs), min(ys), max(xs), max(ys)) if xs else None
        return _bb[path]

    # Build plate-space footprints: each object -> (name, group, [corners], (cx,cy))
    objs = []
    allpts = []
    for bid, item_xf in items.items():
        name = names.get(bid)
        if not name:
            continue
        path, cxf = comp.get(bid, (None, None))
        (r00, r01, r10, r11), fx, fy = compose(item_xf, cxf) if cxf else item_xf
        bb = mesh_bbox(path) if path else None

        def place(lx, ly, r00=r00, r01=r01, r10=r10, r11=r11, fx=fx, fy=fy):
            return (r00 * lx + r01 * ly + fx, r10 * lx + r11 * ly + fy)

        if bb:
            x0, y0, x1, y1 = bb
            corners = [place(x0, y0), place(x1, y0), place(x1, y1), place(x0, y1)]
        else:
            corners = [place(-2, -2), place(2, -2), place(2, 2), place(-2, 2)]
        objs.append((name, name[:3], corners, (fx, fy)))
        allpts.extend(corners)

    if not objs:
        die("no placed objects found in the plate")

    # A highlight that names no object on the plate is a stale sidecar — fail loudly.
    present = {name for name, *_ in objs}
    missing = [n for n in highlights if n not in present]
    if missing:
        die("highlights name objects not on the plate (stale sidecar?): " + ", ".join(sorted(missing)))

    # --- canvas: plate bounds -> pixels, Y flipped (plate up == image down)
    minx = min(p[0] for p in allpts)
    maxx = max(p[0] for p in allpts)
    miny = min(p[1] for p in allpts)
    maxy = max(p[1] for p in allpts)
    PAD_MM, W = 14, 1600
    scale = (W - 2) / ((maxx - minx) + 2 * PAD_MM)
    H = int(((maxy - miny) + 2 * PAD_MM) * scale) + 2

    def to_px(x, y):
        px = (x - minx + PAD_MM) * scale
        py = H - (y - miny + PAD_MM) * scale   # flip Y
        return (px, py)

    img = Image.new("RGB", (W, H + 150), PAPER)  # extra strip for legend
    d = ImageDraw.Draw(img)
    F_LBL, F_SM, F_TTL = font(19), font(15), font(30)

    for name, grp, corners, (cx, cy) in objs:
        poly = [to_px(*c) for c in corners]
        fill = groups.get(grp, (150, 150, 150))
        d.polygon(poly, fill=fill, outline=(40, 40, 40))
        hit = highlights.get(name)
        if hit:
            tier = tiers.get(int(hit["tier"]), {})
            ring = tuple(tier.get("color", (220, 40, 40)))
            width = int(tier.get("width", 6))
            d.line(poly + [poly[0]], fill=ring, width=width, joint="curve")
        # label — strip the MC prefix and abbreviate the long piece nouns
        lx, ly = to_px(cx, cy)
        short = (name.replace("MC", "").replace("Tower", "T")
                     .replace("Wall", "W").replace("Pin", "P"))
        tb = d.textbbox((0, 0), short, font=F_SM)
        d.text((lx - (tb[2] - tb[0]) / 2, ly - (tb[3] - tb[1]) / 2), short,
               fill=(255, 255, 255), font=F_SM)

    # title + legend
    d.text((16, 10), cfg_spec.get("title", "Plate — what to photograph"), fill=INK, font=F_TTL)
    ly = H + 20
    for tier_key in sorted(tiers):
        t = tiers[tier_key]
        col = tuple(t.get("color", (220, 40, 40)))
        d.ellipse([18, ly, 42, ly + 24], outline=col, width=5)
        d.text((52, ly + 2), t.get("legend", ""), fill=INK, font=F_LBL)
        ly += 40
    if cfg_spec.get("footnote"):
        d.text((18, ly + 4), cfg_spec["footnote"], fill=MUTE, font=F_SM)

    return img, len(objs), sum(1 for o in objs if o[0] in highlights)


def build_contact_sheet(z, photo_map, cfg_spec):
    """Compose a printable contact sheet: the baked slicer thumbnails in a strip
    above the annotated photo map. Skips any baked view the .3mf does not carry."""
    W, MARGIN, GAP = 1600, 40, 24
    F_TTL, F_CAP, F_SM = font(30), font(18), font(15)

    tiles = []
    for path, cap in BAKED_TILES:
        try:
            raw = z.read(path)
        except KeyError:
            continue
        tiles.append((Image.open(io.BytesIO(raw)).convert("RGBA"), cap))

    # header
    header_h = 58
    # thumbnail strip (equal squares across the width), captioned
    if tiles:
        n = len(tiles)
        cell = (W - 2 * MARGIN - (n - 1) * GAP) // n
        strip_h = cell + 34  # square + one caption line
    else:
        cell = strip_h = 0

    # the annotated map, scaled to the content width
    content_w = W - 2 * MARGIN
    map_scaled = photo_map.resize(
        (content_w, round(photo_map.height * content_w / photo_map.width)),
        Image.LANCZOS)

    H = header_h + (strip_h + GAP if tiles else 0) + map_scaled.height + MARGIN
    sheet = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(sheet)

    title = cfg_spec.get("title", "Plate").split(" · ")[0] + " · print contact sheet"
    d.text((MARGIN, 14), title, fill=INK, font=F_TTL)

    y = header_h
    if tiles:
        for i, (im, cap) in enumerate(tiles):
            x = MARGIN + i * (cell + GAP)
            thumb = im.resize((cell, cell), Image.LANCZOS)
            bg = Image.new("RGB", (cell, cell), (255, 255, 255))
            bg.paste(thumb, (0, 0), thumb)  # flatten transparency onto white
            sheet.paste(bg, (x, y))
            d.rectangle([x, y, x + cell - 1, y + cell - 1], outline=(180, 180, 180))
            d.text((x + 2, y + cell + 8), cap, fill=MUTE, font=F_SM)
        y += strip_h + GAP

    sheet.paste(map_scaled, (MARGIN, y))
    return sheet


def main() -> None:
    ap = argparse.ArgumentParser(description="Render a sliced .3mf as a coupon photo map.")
    ap.add_argument("plate", help="sliced Bambu .3mf")
    ap.add_argument("highlights", help="JSON sidecar: what to ring (see docstring)")
    ap.add_argument("out", help="output PNG for the annotated top-down map")
    ap.add_argument("--contact-sheet", metavar="PNG",
                    help="also write a printable contact sheet tiling the baked slicer thumbnails")
    args = ap.parse_args()

    try:
        cfg_spec = json.loads(open(args.highlights, encoding="utf8").read())
    except (OSError, ValueError) as e:
        die(f"cannot read highlights sidecar {args.highlights}: {e}")

    try:
        z = zipfile.ZipFile(args.plate)
    except (OSError, zipfile.BadZipFile) as e:
        die(f"cannot open plate {args.plate}: {e}")

    photo_map, n_obj, n_hl = render_photo_map(z, cfg_spec)
    photo_map.save(args.out)
    print(f"wrote {args.out}  ({n_obj} objects, {n_hl} highlighted)")

    if args.contact_sheet:
        sheet = build_contact_sheet(z, photo_map, cfg_spec)
        sheet.save(args.contact_sheet)
        print(f"wrote {args.contact_sheet}  (contact sheet {sheet.width}x{sheet.height})")


if __name__ == "__main__":
    main()
