#!/usr/bin/env python3
"""Style bikar orb views into gallery preview PNGs.

`make orbs` renders each orb along every symmetry axis of its base
solid and writes two drawings per axis: the instrument at the top level
of build/orb-views/<Orb>/ (flat #8a8a8a faces on a white card — what
qiyas encodes and scores) and its shaded twin under display/. This
script picks each orb's hero view, recolors it to the catalog gold,
drops the background card so the orb floats on the page like every
other plate, and rasterizes it into build/images/<Orb>.png, where
`make web-images` autocrops it alongside the OpenSCAD renders.

Two things it must not do, and both used to be possible:

* **Read the instrument when a display twin exists.** The instrument is
  byte-pinned for qiyas; the gallery is the surface a person looks at,
  and a flat gray blob recolored gold is still a flat blob. Preference
  order is display/ → ribbons/display/ → the instrument → ribbons/, so
  an orb that has no cell views at all (the woven-overlap wheelfield
  draws only bands) still gets a hero instead of being skipped.
* **Recolor by literal string replacement.** `fill="#8a8a8a"` → gold
  was exact on a one-fill drawing and silently wrong the moment shading
  arrived: it matched none of the shaded grays and left them gray. The
  mapping below is structural — any gray fill is carried into gold at
  its own luminance ratio, so the modeling survives the recolor.

Usage:  python3 build/orb_previews.py
Deps:   rsvg-convert   (brew install librsvg)
"""
import glob
import os
import re
import subprocess
import sys

VIEWS_DIR = "build/orb-views"
OUT_DIR = "build/images"
SIZE = 1024
FILL = "#c79a2e"    # --gold in index.html — echoes the OpenSCAD render gold
STROKE = "#7a5d17"
BASE_GRAY = "#8a8a8a"  # bikar DEFAULT_ORB_VIEW_FILL — unshaded is ratio 1.0


# Where a hero may come from, best first. display/ is the shaded twin
# of the instrument beside it; ribbons/ is the whole view set for an orb
# whose bands cross rather than tile, which has no cell views at all.
SOURCES = ("display", "ribbons/display", "", "ribbons")


def hero(svgs):
    # Highest symmetry fold reads most iconic (vertex-5 on icosahedral
    # orbs, face-5 on dodecahedral); tie-break vertex > face > edge.
    def key(path):
        m = re.search(r"\.([a-z]+)-(\d+)\.svg$", os.path.basename(path))
        kind, fold = (m.group(1), int(m.group(2))) if m else ("", 0)
        rank = {"vertex": 0, "face": 1, "edge": 2}.get(kind, 3)
        return (-fold, rank)
    return sorted(svgs, key=key)[0]


def views(orb_dir):
    """The best available view set for one orb, and where it came from."""
    for sub in SOURCES:
        d = os.path.join(orb_dir, sub) if sub else orb_dir
        found = [p for p in sorted(glob.glob(os.path.join(d, "*.svg")))
                 if ".preview." not in p]
        if found:
            return found, (sub or "instrument")
    return [], None


def _gold(ratio):
    """The catalog gold at `ratio` of full luminance, as #rrggbb."""
    r, g, b = (int(FILL[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(
        max(0, min(255, round(c * ratio))) for c in (r, g, b)
    )


def recolor_fill(match):
    """Carry one gray fill into gold, keeping its luminance ratio.

    The shaded views model depth by darkening the base gray — a face
    turned away from the camera comes out #5e5e5e where a face square
    on to it stays #8a8a8a. Mapping only the base gray (what this did
    before shading existed) would recolor the brightest faces and leave
    every shaded one gray, so the ratio is what travels, not the value.

    Anything that is not a gray is left exactly as it is: the highlight
    tint on a stage frame is a deliberate color and pushing it toward
    gold would erase the one thing it exists to say.
    """
    r, g, b = (match.group(1)[i:i + 2] for i in (0, 2, 4))
    if not (r == g == b):
        return match.group(0)
    value = int(r, 16)
    if value == 255:            # the white card, dropped just above
        return match.group(0)
    return f'fill="{_gold(value / int(BASE_GRAY[1:3], 16))}"'


def restyle(text):
    text = re.sub(r'<rect [^>]*fill="#ffffff"[^>]*/>\s*', "", text, count=1)
    text = re.sub(r'fill="#([0-9a-fA-F]{6})"', recolor_fill, text)
    text = text.replace('stroke="#333333"', f'stroke="{STROKE}"')
    return text


def main():
    orb_dirs = sorted(glob.glob(f"{VIEWS_DIR}/*/"))
    if not orb_dirs:
        sys.exit(f"no views under {VIEWS_DIR} — run `make orbs` first")
    for d in orb_dirs:
        svgs, source = views(d)
        if not svgs:
            print(f"{os.path.basename(d.rstrip('/'))}: no views — skipped")
            continue
        pick = hero(svgs)
        orb = os.path.basename(pick).split(".")[0]
        with open(pick) as f:
            styled = restyle(f.read())
        tmp = os.path.join(d, f"{orb}.preview.svg")
        with open(tmp, "w") as f:
            f.write(styled)
        out = f"{OUT_DIR}/{orb}.png"
        subprocess.run(
            ["rsvg-convert", "-w", str(SIZE), "-h", str(SIZE), "-o", out, tmp],
            check=True,
        )
        os.remove(tmp)
        print(f"{orb}: {source}/{os.path.basename(pick)} -> {out}")


SHADED = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-70 -70 140 140">'
    '<rect x="-70" y="-70" width="140" height="140" fill="#ffffff" />'
    '<circle cx="0" cy="0" r="60" fill="none" stroke="#333333" '
    'data-orb-silhouette="true" />'
    '<path d="M0 0" fill="#8a8a8a" stroke="#333333" data-orb-style="shaded" />'
    '<path d="M1 1" fill="#5e5e5e" stroke="#333333" data-orb-style="shaded" />'
    '<path d="M2 2" fill="#c9782e" stroke="#333333" />'
    "</svg>"
)


def self_test():
    """Prove the recolor on the case that used to escape it.

    The old `restyle` replaced the single literal `fill="#8a8a8a"`. That
    was exact while every face carried the base gray and silently wrong
    the day shading arrived: a shaded face is #5e5e5e, no literal
    matched it, and it rasterised gray into a gold gallery. The check is
    therefore not "some fill became gold" — the base gray would pass
    that on its own — but "no gray survives", which is the shape the
    defect had.
    """
    out = restyle(SHADED)
    grays = [m for m in re.findall(r'fill="#([0-9a-fA-F]{6})"', out)
             if m[0:2] == m[2:4] == m[4:6]]
    checks = [
        ("no gray fill survives the recolor", grays == [], f"left {grays}"),
        ("the darker face stays darker",
         out.count(_gold(0x5e / 0x8a)) == 1
         and _gold(0x5e / 0x8a) != _gold(1.0),
         "shading flattened"),
        ("an unshaded view still lands on the exact catalog gold",
         f'fill="{FILL}"' in out, "base gray moved off #c79a2e"),
        ("the highlight tint is left alone",
         'fill="#c9782e"' in out, "a deliberate color was pushed to gold"),
        ("the silhouette stroke is recolored with the rest",
         f'stroke="{STROKE}"' in out and 'stroke="#333333"' not in out,
         "a black outline would ring the gold"),
        ("the white card is dropped", "<rect" not in out, "card kept"),
    ]
    failures = 0
    for label, ok, why in checks:
        failures += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}"
              + ("" if ok else f" — {why}"))
    print("self-test: " + ("PASS" if failures == 0 else f"FAIL ({failures})"))
    return 1 if failures else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    main()
