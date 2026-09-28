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
import sys
import tempfile
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent.parent
MIN_OPAQUE = 0.05  # fraction of the picture; a 90 mm coaster at 1024 px fills ~30 %


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


def touches_frame(alpha: bytes, w: int, h: int) -> bool:
    rows = any(alpha[x] == 255 or alpha[(h - 1) * w + x] == 255 for x in range(w))
    cols = any(alpha[y * w] == 255 or alpha[y * w + w - 1] == 255 for y in range(h))
    return rows or cols


def check_picture(path: Path, raw: bool) -> list[str]:
    """P1-P4 on one bikar-drawn picture. Returns findings (empty = pass)."""
    if not path.exists():
        return [f"{path}: missing"]
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    alpha = im.getchannel("A").tobytes()
    out = []
    if not corners_transparent(alpha, w, h):
        out.append(f"{path}: P1 a corner is not transparent — a background was drawn")
    holes, first = enclosed_non_opaque(alpha, w, h)
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
    for name in drawn:
        findings += check_picture(root / f"build/images/{name}.png", raw=True)
        web = root / f"build/images/web/{name}.png"
        if web.exists():
            findings += check_picture(web, raw=False)
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
        f"coaster-pictures: {len(drawn)} bikar picture(s) checked P1-P4 "
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
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args()
    return _self_test() if args.self_test else run(args.root)


if __name__ == "__main__":
    sys.exit(main())
