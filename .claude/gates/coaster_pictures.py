#!/usr/bin/env python3
"""No-hole check for the coaster pictures `make coasters` draws.

docs/design/coaster/color-preview-design.md §7, last validator: a gallery PNG has no hole
inside the coaster. `make coasters` draws a coaster with `bikar render --format
preview` when bikar can split it, and falls back to the OpenSCAD picture
(build/brick_previews.py) when bikar refuses. bikar's picture has no
background, so no color key runs over it; this gate is what says so.

For every picture bikar drew (the names in build/.coaster-previewed), in
build/images/ and, once `make web-images` has run, in build/images/web/:

  P1  all four corners are fully transparent (no background was drawn);
  P2  no hole: every pixel that is not fully opaque is joined to the image
      edge through other not-fully-opaque pixels. A see-through pixel walled
      in by coaster is a hole — a pinhole between faces, or a color key that
      ate a lit face;
  P3  the coaster is there: at least MIN_OPAQUE of the picture is opaque, so
      an empty or all-transparent PNG cannot pass P1 and P2 by having nothing;
  P4  the coaster is not cut off: no opaque pixel on the outermost row or
      column (raw picture only — `process_images.py` autocrops the web copy
      to PAD px, so its edge is not the render frame);
  P5  the web copy is the raw picture cropped and nothing else: inside the
      box around the visible pixels, the two alpha channels are equal pixel
      for pixel. This is the check that catches a color key eating a cream
      body. P2 cannot: keyed straps reach the outer ring, so the see-through
      region is joined to the outside (measured 2026-09-28 on 7apC5Q9QS-8-fill
      with its straps repainted #fffde8 — the old key made 123k px
      see-through and P2 passed).

What it does NOT check, said here so a green run is read correctly:
  - A notch that opens to the silhouette's edge is joined to the outside, so
    P2 does not see it in the raw picture. Only an enclosed hole is caught
    there; P5 covers the web copy against the raw one, not the raw one itself.
  - P2 on an openwork coaster: one whose source cuts the pattern's spaces
    through (`outline pattern` — minimal, twist, radial — or `openwork frame`).
    Its openings are real, and no pixel rule tells one from a pinhole:
    measured 2026-09-29 (`--measure`) on the minimal and radial pictures, real
    openings seen past a wall show as regions of 1 and 2 px, the size of a
    pinhole. Until bikar drew openwork itself (bikar #274, #270) every openwork
    picture was an OpenSCAD fallback and skipped for the same reason; the
    skip is now keyed on the source, not on who drew the picture. P1, P3, P4
    and P5 still run on them. A crack between faces is the mesh gate's to
    catch (`watertight=true` on every `make coasters` render).
  - The OpenSCAD fallback pictures (the names in build/.coaster-names that
    bikar refused) get no hole check. Openwork coasters have real openings,
    and those pictures are keyed by `process_images.py`, so a transparent
    pixel inside them may be a real opening. Their web copies get P1 only;
    the raw OpenSCAD render has an opaque cream background by design.

An absent build/.coaster-names is a skip, exit 0 (nothing rendered yet, e.g.
a fresh clone). A names file with a missing picture is a failure.

Usage:  python3 .claude/gates/coaster_pictures.py [--root DIR]
        python3 .claude/gates/coaster_pictures.py --self-test
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent.parent
MIN_OPAQUE = 0.05  # fraction of the picture; a 90 mm coaster at 1024 px fills ~30 %
OPENWORK_CLAUSE = re.compile(r"^\s*(outline\s+pattern|openwork\s+frame)\b", re.M)


def corners_transparent(alpha: bytes, w: int, h: int) -> bool:
    return all(alpha[i] == 0 for i in (0, w - 1, (h - 1) * w, h * w - 1))


def enclosed_non_opaque(alpha: bytes, w: int, h: int) -> tuple[int, tuple[int, int] | None]:
    """Count not-fully-opaque pixels not joined (4-way) to the image edge."""
    seen = bytearray(w * h)
    q: deque[int] = deque()
    edge = [y * w + x for x in range(w) for y in (0, h - 1)] + [
        y * w + x for y in range(h) for x in (0, w - 1)
    ]
    for i in edge:
        if alpha[i] < 255 and not seen[i]:
            seen[i] = 1
            q.append(i)
    while q:
        i = q.popleft()
        x, y = i % w, i // w
        if x > 0 and not seen[i - 1] and alpha[i - 1] < 255:
            seen[i - 1] = 1
            q.append(i - 1)
        if x < w - 1 and not seen[i + 1] and alpha[i + 1] < 255:
            seen[i + 1] = 1
            q.append(i + 1)
        if y > 0 and not seen[i - w] and alpha[i - w] < 255:
            seen[i - w] = 1
            q.append(i - w)
        if y < h - 1 and not seen[i + w] and alpha[i + w] < 255:
            seen[i + w] = 1
            q.append(i + w)
    count, first = 0, None
    for i in range(w * h):
        if alpha[i] < 255 and not seen[i]:
            count += 1
            if first is None:
                first = (i % w, i // w)
    return count, first


def enclosed_regions(alpha: bytes, w: int, h: int) -> list[tuple[int, tuple[int, int]]]:
    """Each enclosed see-through region (4-way joined), as (pixel count, first pixel)."""
    count, _ = enclosed_non_opaque(alpha, w, h)
    if not count:
        return []
    edge_joined = bytearray(w * h)
    q: deque[int] = deque()
    for i in [y * w + x for x in range(w) for y in (0, h - 1)] + [y * w + x for y in range(h) for x in (0, w - 1)]:
        if alpha[i] < 255 and not edge_joined[i]:
            edge_joined[i] = 1
            q.append(i)
    while q:
        i = q.popleft()
        for j in _neighbours(i, w, h):
            if not edge_joined[j] and alpha[j] < 255:
                edge_joined[j] = 1
                q.append(j)
    regions = []
    for s in range(w * h):
        if alpha[s] < 255 and not edge_joined[s]:
            edge_joined[s] = 1
            q.append(s)
            n = 0
            while q:
                i = q.popleft()
                n += 1
                for j in _neighbours(i, w, h):
                    if not edge_joined[j] and alpha[j] < 255:
                        edge_joined[j] = 1
                        q.append(j)
            regions.append((n, (s % w, s // w)))
    return regions


def _neighbours(i: int, w: int, h: int):
    x, y = i % w, i // w
    if x > 0:
        yield i - 1
    if x < w - 1:
        yield i + 1
    if y > 0:
        yield i - w
    if y < h - 1:
        yield i + w


def touches_frame(alpha: bytes, w: int, h: int) -> bool:
    rows = any(alpha[x] == 255 or alpha[(h - 1) * w + x] == 255 for x in range(w))
    cols = any(alpha[y * w] == 255 or alpha[y * w + w - 1] == 255 for y in range(h))
    return rows or cols


def check_picture(path: Path, raw: bool, openwork: bool = False) -> list[str]:
    """P1-P4 on one bikar-drawn picture (P2 skipped for openwork). Returns findings (empty = pass)."""
    if not path.exists():
        return [f"{path}: missing"]
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    alpha = im.getchannel("A").tobytes()
    out = []
    if not corners_transparent(alpha, w, h):
        out.append(f"{path}: P1 a corner is not transparent — a background was drawn")
    holes, first = (0, None) if openwork else enclosed_non_opaque(alpha, w, h)
    if holes:
        out.append(f"{path}: P2 {holes} see-through px inside the coaster, first at {first}")
    opaque = sum(1 for a in alpha if a == 255)
    if opaque < MIN_OPAQUE * w * h:
        out.append(f"{path}: P3 only {opaque} opaque px of {w * h} — the coaster is missing")
    if raw and touches_frame(alpha, w, h):
        out.append(f"{path}: P4 opaque px on the picture's edge — the coaster is cut off")
    return out


def same_alpha_as_raw(raw: Path, web: Path) -> list[str]:
    """P5: the web copy is the raw picture cropped, not keyed.

    Both are cut to the bounding box of their visible pixels and their alpha
    compared pixel for pixel. A color key that ate a body changes the alpha
    inside that box even where the eaten region reaches the silhouette's edge,
    which is exactly where P2 is blind."""
    a = Image.open(raw).convert("RGBA").getchannel("A")
    b = Image.open(web).convert("RGBA").getchannel("A")
    box_a, box_b = a.getbbox(), b.getbbox()
    if box_a is None or box_b is None:
        return [f"{web}: P5 nothing visible to compare against {raw.name}"]
    ca, cb = a.crop(box_a), b.crop(box_b)
    if ca.size != cb.size:
        return [f"{web}: P5 visible area {cb.size} differs from the raw picture's {ca.size}"]
    diff = sum(1 for x, y in zip(ca.tobytes(), cb.tobytes()) if x != y)
    if diff:
        return [f"{web}: P5 {diff} px differ in transparency from the raw picture — it was keyed, not only cropped"]
    return []


def read_names(path: Path) -> list[str]:
    return [s.strip() for s in path.read_text().splitlines() if s.strip()]


def is_openwork(root: Path, name: str) -> bool:
    """The coaster has real openings: its source cuts the pattern's spaces
    through (`outline pattern` — minimal, twist, radial — or `openwork frame`).
    No source found means not openwork, so the strict P2 applies."""
    src = root / f"src/Coasters/{name}-coaster.bkr"
    if not src.exists():
        return False
    return bool(OPENWORK_CLAUSE.search(src.read_text()))


def measure(root: Path) -> int:
    """Print every enclosed see-through region per bikar picture, smallest
    first — the numbers MIN_OPENING was set from, re-measurable."""
    drawn_file = root / "build/.coaster-previewed"
    if not drawn_file.exists():
        print("coaster-pictures: no build/.coaster-previewed — run make coasters first", file=sys.stderr)
        return 1
    for name in read_names(drawn_file):
        path = root / f"build/images/{name}.png"
        if not path.exists():
            continue
        im = Image.open(path).convert("RGBA")
        regions = sorted(enclosed_regions(im.getchannel("A").tobytes(), *im.size))
        kind = "openwork" if is_openwork(root, name) else "solid"
        print(f"{name:32s} {kind:8s} regions={len(regions):3d} smallest={regions[:8]}")
    return 0


def run(root: Path) -> int:
    names_file = root / "build/.coaster-names"
    if not names_file.exists():
        print("coaster-pictures: no build/.coaster-names — nothing rendered yet, skipping", file=sys.stderr)
        return 0
    names = read_names(names_file)
    drawn_file = root / "build/.coaster-previewed"
    drawn = read_names(drawn_file) if drawn_file.exists() else []
    findings: list[str] = []
    web_checked = 0
    openwork = [n for n in drawn if is_openwork(root, n)]
    for name in drawn:
        ow = name in openwork
        findings += check_picture(root / f"build/images/{name}.png", raw=True, openwork=ow)
        web = root / f"build/images/web/{name}.png"
        if web.exists():
            findings += check_picture(web, raw=False, openwork=ow)
            raw = root / f"build/images/{name}.png"
            if raw.exists():
                findings += same_alpha_as_raw(raw, web)
            web_checked += 1
    fallback = [n for n in names if n not in drawn]
    fb_web = 0
    for name in fallback:
        web = root / f"build/images/web/{name}.png"
        if web.exists():
            fb_web += 1
            im = Image.open(web).convert("RGBA")
            if not corners_transparent(im.getchannel("A").tobytes(), *im.size):
                findings.append(f"{web}: P1 a corner is not transparent")
    for f in findings:
        print(f, file=sys.stderr)
    print(
        f"coaster-pictures: {len(drawn)} bikar picture(s) checked P1-P4, "
        f"{len(openwork)} of them openwork and so not P2 "
        f"({web_checked} web copies: P1-P3 and P5); {len(fallback)} OpenSCAD fallback(s) not hole-checked "
        f"({fb_web} web copies checked P1) — {'FAILED' if findings else 'ok'}"
    )
    return 1 if findings else 0


# --- self-test: every by-design failure must fire ---------------------------

def _coaster(size=200, hole=False, background=False, empty=False, cut=False, notch=False):
    bg = (255, 255, 229, 255) if background else (0, 0, 0, 0)
    im = Image.new("RGBA", (size, size), bg)
    d = ImageDraw.Draw(im)
    if not empty:
        box = (-20, 40, 160, 160) if cut else (40, 40, 160, 160)
        d.polygon([(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])],
                  fill=(51, 51, 51, 255))
        d.ellipse((80, 80, 120, 120), fill=(212, 175, 55, 255))
    if hole:
        im.putpixel((100, 60), (0, 0, 0, 0))
    if notch:
        d.rectangle((95, 40, 105, 70), fill=(0, 0, 0, 0))
    return im


def _self_test() -> int:
    cases = [
        ("a clean picture passes", {}, None),
        ("a one-pixel hole is P2", {"hole": True}, "P2"),
        ("a cream background is P1", {"background": True}, "P1"),
        ("an empty picture is P3", {"empty": True}, "P3"),
        ("a coaster cut off at the frame is P4", {"cut": True}, "P4"),
        # The documented blind spot: a notch open to the edge is not a hole.
        ("a notch open to the silhouette edge is NOT caught (documented)", {"notch": True}, None),
    ]
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        for label, kw, want in cases:
            p = Path(tmp) / "c.png"
            _coaster(**kw).save(p)
            got = check_picture(p, raw=True)
            ok = (not got) if want is None else any(f": {want} " in g for g in got)
            bad += not ok
            print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}" + ("" if ok else f" -> {got}"))

        # P5: a keyed band that reaches the silhouette edge — invisible to P2.
        raw, web = Path(tmp) / "raw.png", Path(tmp) / "web.png"
        _coaster().save(raw)
        keyed = _coaster()
        ImageDraw.Draw(keyed).rectangle((40, 95, 160, 105), fill=(0, 0, 0, 0))
        keyed.save(web)
        p2 = check_picture(web, raw=False)
        p5 = same_alpha_as_raw(raw, web)
        ok = not p2 and any(": P5 " in g for g in p5)
        bad += not ok
        print(f"self-test {'ok  ' if ok else 'FAIL'}: a keyed band open to the edge passes P2 but is P5"
              + ("" if ok else f" -> P2={p2} P5={p5}"))
        _coaster().crop((20, 20, 180, 180)).save(web)
        ok = not same_alpha_as_raw(raw, web)
        bad += not ok
        print(f"self-test {'ok  ' if ok else 'FAIL'}: a web copy that is only cropped passes P5")

        root = Path(tmp) / "repo"
        rc = run(root)
        ok = rc == 0
        bad += not ok
        print(f"self-test {'ok  ' if ok else 'FAIL'}: an absent build/ is a skip, exit 0 (got {rc})")

        (root / "build/images").mkdir(parents=True)
        (root / "build/.coaster-names").write_text("a\nb\n")
        (root / "build/.coaster-previewed").write_text("a\n")
        rc = run(root)
        ok = rc == 1
        bad += not ok
        print(f"self-test {'ok  ' if ok else 'FAIL'}: a drawn name with no picture fails, exit 1 (got {rc})")

        _coaster().save(root / "build/images/a.png")
        rc = run(root)
        ok = rc == 0
        bad += not ok
        print(f"self-test {'ok  ' if ok else 'FAIL'}: the fallback name b is not hole-checked, exit 0 (got {rc})")

        # Openwork: an enclosed opening passes when the source cuts openings
        # through, and the same picture still fails P2 on a solid source.
        _coaster(hole=True).save(root / "build/images/a.png")
        (root / "src/Coasters").mkdir(parents=True)
        src = root / "src/Coasters/a-coaster.bkr"
        src.write_text("coaster c\n  relief straps emboss 1.2\n")
        rc = run(root)
        ok = rc == 1
        bad += not ok
        print(f"self-test {'ok  ' if ok else 'FAIL'}: a hole in a solid coaster's picture is P2, exit 1 (got {rc})")
        src.write_text("coaster c\n  outline pattern\n")
        rc = run(root)
        ok = rc == 0
        bad += not ok
        print(f"self-test {'ok  ' if ok else 'FAIL'}: an opening in an openwork coaster's picture passes, exit 0 (got {rc})")
        src.write_text("coaster c\n  # outline pattern would make it openwork\n  relief straps emboss 1.2\n")
        ok = not is_openwork(root, "a")
        bad += not ok
        print(f"self-test {'ok  ' if ok else 'FAIL'}: a commented-out clause does not make a coaster openwork")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--measure", action="store_true",
                    help="print each picture's enclosed see-through regions, smallest first")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    return measure(args.root) if args.measure else run(args.root)


if __name__ == "__main__":
    sys.exit(main())
