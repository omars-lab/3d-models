#!/usr/bin/env python3
"""Timelapse gate for 3d-models: the breakdown's invariants, checked on disk.

`make orbs` writes one directory per orb under `build/orb-breakdown/`: a
manifest and the frames it names. Four properties make those frames a story
rather than a pile of drawings, and none of them is visible by looking at any
single file:

  T1  **The manifest declares every key the page reads.** Every missing key is
      a page state, not a crash — an orb rendered by a dist built before
      `--turntable` shipped produced fourteen perfectly valid directories that
      all rendered "this orb has no camera sweep" (2026-08-18). A gate that
      only opened the JSON would have called that a clean run.
  T2  **One viewBox across stages, tilt and spin.** The page cross-fades
      between them; a frame from a differently-sized projection makes the
      picture jump size mid-story, and nothing about the file says so.
  T3  **The last stage frame is the shipped view, repainted and not redrawn.**
      The story ends on the drawing qiyas scores. If it does not, the page has
      been teaching the construction of something else. It is still a byte
      identity, but against a *derived* expectation: the shipped view with its
      background rect repainted onto the page's ground, and wearing the limb.
      The frames are static SVGs served as `<img src>`, so the white square
      inside every grey panel was fixable in the file or not at all — and the
      instrument set is not a file a page's taste gets to move. Every byte but
      those two named differences still has to match, and the rule checks that
      the shipped view really is white and really has no limb, so it cannot go
      quiet if `--format views` ever starts writing either itself.

      The limb joined the derivation on 2026-08-20 rather than the frame
      losing it. It had been dropped from `complete` alone so that this rule
      could name a single substitution — which meant the one picture a reader
      stops on was the one picture with nothing in it saying "this is a ball".
      A rule about bytes had quietly decided what a reader gets to see.
  T4  **The two junctions are byte identities.** transition[0] is the complete
      frame and transition[last] is the orbit point it enters at, so neither
      hand-off can jump. They hold because the endpoint frames are rendered
      from the cameras they sit on rather than given synthetic names — an
      invariant one careless rename breaks silently.

And two hygiene checks that exist because the failure they catch is *absence*,
which no amount of looking at what is present will find:

  T5  Every file the manifest names exists, and no `.svg` in the directory is
      unnamed by it. An orphan is the shape of a frame the generator stopped
      writing and nothing removed — see T3's Maclado-9-Overlap case below.
  T6  **Every frame wears the limb; only the unfinished ones wear the
      scaffold.** The two marks answer different questions and so they part
      company on the last frame. `data-orb-scaffold` is the bare solid drawn
      as an outline underneath, so the pattern is seen landing on something
      rather than building up against a blank page — it answers *how far
      along is this*, which is moot once nothing is left to place, so the
      `complete` frame drops it and a scaffold leaking onto the finished orb
      is still a failure. `data-orb-silhouette` is the sphere's edge, and it
      answers *is this a ball*: the frame that answers it best is the last
      one, so every frame carries it. No frame in
      `frames` carries `data-orb-style`: shading belongs to the spin, and on
      a stage frame a Lambert envelope makes an unplaced region and a dim
      placed one look alike — the one distinction a stage frame exists to
      draw. Fills come only from the constants either way.

      The presence half is not symmetry for its own sake. Until 2026-08-19
      the base solid was written once, as frame zero, and never again, so
      from the second frame on there was nothing under the pattern; the gate
      then said every frame was fine, because it only ever checked for marks
      that should be *absent*. An absence rule cannot catch a missing
      picture.

And one containment check, because a picture can contradict the claim it
makes:

  T7  **A cell stage stays inside the solid the scaffold draws.** The outline
      is a picture of "the pattern lands on these faces", and on 2026-08-19 it
      was a false one: the base solid was handed to the renderer as its bare
      corners, so each edge was drawn as a chord, and a straight line between
      two points on a sphere runs *inside* it — by 6.6% of the radius on a
      dodecahedron's edge. The pattern's own cells are dense enough to hug the
      surface, so they sat *outside* the outline meant to contain them and
      RosetteWeaveOrb's units visibly burst through it. T6 could not see it:
      the scaffold was present on every frame, which is all T6 ever asked.
      `strand` stages are exempt with a reason rather than a threshold — a
      woven band's amplitude lifts it off the sphere by up to 3.68 mm across
      the corpus, by design.

**The by-design failure this gate shipped with, and why it is recorded here.**
On the tree this gate was written against, T3 and T5 both failed on
Maclado-9-Overlap: its bands cross rather than tile, the projector refuses to
draw it as cells by design, and three cell views from the run *before* that
refusal were still sitting in `build/orb-views/Maclado9Overlap/` — scored by
qiyas, picked as the gallery hero. Regeneration could not fix them, because
regeneration no longer wrote them. The remediation is the `rm -rf` in the
`orbs` target; this docstring is here so that a future reader who finds the
gate passing knows it was not always so, and what made it pass.

Usage:
  timelapse_gate.py                  check every orb under build/orb-breakdown
  timelapse_gate.py --keys [DIR]     T1 only — what `make orbs` calls, so the
                                     required-key tuple has exactly one owner
  timelapse_gate.py --self-test      mutate a fixture and prove each rule fires

Override once: TIMELAPSE_GATE_OK=1 git commit
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BREAKDOWN = ROOT / "build" / "orb-breakdown"
VIEWS = ROOT / "build" / "orb-views"

# The keys the breakdown page reads. Owned here and nowhere else: the Makefile
# used to carry its own copy of this tuple, which is the "two sites, one
# updated" shape `counts_gate.py` was built for.
REQUIRED_KEYS = (
    "orb",
    "views",
    "frames",
    "turntable",
    "turntableRepresentation",
    "transition",
    "flat",
    "base",
    "weave",
    "source",
    "sourceSha256",
    "engine",
)

# The one attribute a breakdown frame is allowed to differ from the shipped
# instrument view by: `DISPLAY_GROUND` in bikar's `packages/cli/src/index.ts`.
# The frames are static SVGs the page serves as `<img src>`, so no stylesheet
# can reach inside them — a white square inside a grey panel had to be fixed in
# the file or not at all, and the instrument set qiyas scores is not a file a
# page's taste gets to move. So T3 stopped being a whole-file hash and became a
# byte identity against a *derived* expectation. Every other byte still has to
# match; the check that `WHITE_RECT` is actually present is what keeps the rule
# from going quiet if `--format views` ever starts writing the ground itself.
GROUND = "#dfe3e5"
WHITE_RECT = 'fill="#ffffff" pointer-events="none"'
GROUND_RECT = f'fill="{GROUND}" pointer-events="none"'

# The second named difference: the limb. A display frame draws the sphere's
# edge as a circle and clips its content to it; the instrument view draws
# neither, because qiyas classifies a `fill="none"` element as a foreign
# contour. The complete frame used to drop the circle to keep this rule short,
# which cost the sequence its depth cue on the one picture a reader stops on.
# Under the front-cap cull the clip is a no-op — nothing the front cap keeps
# reaches the limb — so the pair is decoration on a terminal frame, and naming
# it here is cheaper than teaching a flat rosette. Written as the literal bytes
# bikar emits: a silent format change has to fail this, not be absorbed by it.
SILHOUETTE_RE = re.compile(
    r'^ {2}<circle cx="0" cy="0" r="([\d.]+)" fill="none" stroke="#333333" '
    r'stroke-width="0\.4" data-orb-silhouette="true" />$',
    re.M,
)


def _wearing_limb(shipped: str, radius: str) -> str:
    """The instrument view with the limb added — the derivation T3 checks against."""
    # Anchored on the rect element, not on which ground it is painted: the
    # two substitutions are then order-independent, and this helper is usable
    # on an instrument view as well as on a repainted one.
    after_rect = shipped.index("\n", shipped.index("<rect ")) + 1
    before_close = shipped.rindex("</svg>")
    limb = (
        f'  <circle cx="0" cy="0" r="{radius}" fill="none" stroke="#333333" '
        'stroke-width="0.4" data-orb-silhouette="true" />\n'
        f'  <clipPath id="orb-limb"><circle cx="0" cy="0" r="{radius}" /></clipPath>\n'
        '  <g clip-path="url(#orb-limb)">\n'
    )
    return (
        shipped[:after_rect]
        + limb
        + shipped[after_rect:before_close]
        + "  </g>\n"
        + shipped[before_close:]
    )


# bikar's DEFAULT_ORB_VIEW_FILL and DEFAULT_ORB_HIGHLIGHT_FILL, plus the card.
# `#ffffff` left this set when the card stopped being white, and its leaving is
# a rule in itself: a stage frame that still paints white is an un-repainted
# frame, which is the defect, not an exemption from it.
STAGE_FILLS = {"#8a8a8a", "#c9782e", GROUND, "none"}
STAGE_KINDS = {"base", "element", "repeat", "strand", "complete"}
# The two marks a stage frame wears, and they no longer travel together.
# `data-orb-scaffold` answers *how far along is this* — moot once nothing is
# left to place, so the complete frame drops it, and a scaffold leaking onto
# the finished orb is still a real failure. `data-orb-silhouette` answers *is
# this a sphere*, which the last frame is the best of all of them at saying,
# so every frame wears it. Until 2026-08-20 the complete frame dropped both,
# and it dropped the circle only to keep T3's derivation to one substitution —
# a rule about bytes deciding what a reader gets to see.
SCAFFOLD_MARK = "data-orb-scaffold"
LIMB_MARK = "data-orb-silhouette"

FILL_RE = re.compile(r'fill="([^"]*)"')
VIEWBOX_RE = re.compile(r'viewBox="([^"]*)"')


# A cell stage must sit inside the solid the scaffold draws. Bands do not:
# a woven strand's amplitude lifts it clear of the sphere the scaffold
# traces, by up to 3.68 mm across the corpus, so `strand` is exempt and
# the exemption has a reason rather than a threshold.
CONTAINED_KINDS = {"element", "repeat"}
# Slack for the coordinate rounding in the SVG, not for geometry: frames are
# written at 4 decimal places, and a vertex the renderer put exactly on a
# scaffold edge can land either side of it. Measured overhang for every cell
# stage of all 14 orbs is 0.000 mm, so anything this rule reports is real.
CONTAINMENT_SLACK_MM = 0.01

PATH_RE = re.compile(r"<path\b([^>]*)>")
D_RE = re.compile(r'\sd="([^"]+)"')
COORD_RE = re.compile(r"-?\d+\.?\d*")


def _polygons(svg: str) -> tuple[list[list[tuple[float, float]]], list[list[tuple[float, float]]]]:
    """The scaffold outlines and the drawn shapes of one frame, as point rings."""
    scaffold: list[list[tuple[float, float]]] = []
    drawn: list[list[tuple[float, float]]] = []
    for attrs in PATH_RE.findall(svg):
        d = D_RE.search(attrs)
        if not d:
            continue
        nums = [float(v) for v in COORD_RE.findall(d.group(1))]
        ring = list(zip(nums[0::2], nums[1::2]))
        if "data-orb-scaffold" in attrs:
            scaffold.append(ring)
        else:
            fill = FILL_RE.search(attrs)
            if fill and fill.group(1).lower() not in ("none", "#ffffff"):
                drawn.append(ring)
    return scaffold, drawn


def _inside(pt: tuple[float, float], ring: list[tuple[float, float]]) -> bool:
    x, y = pt
    hit = False
    for i, (x1, y1) in enumerate(ring):
        x2, y2 = ring[(i + 1) % len(ring)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            hit = not hit
    return hit


def _distance_to(pt: tuple[float, float], rings: list[list[tuple[float, float]]]) -> float:
    """How far outside `rings` a point lies, in mm — 0.0 if it is on an edge."""
    best = math.inf
    px, py = pt
    for ring in rings:
        for i, (ax, ay) in enumerate(ring):
            bx, by = ring[(i + 1) % len(ring)]
            dx, dy = bx - ax, by - ay
            span = dx * dx + dy * dy
            t = 0.0 if span == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / span))
            best = min(best, math.hypot(px - (ax + t * dx), py - (ay + t * dy)))
    return best


def _read(path: Path) -> str:
    return path.read_text(encoding="utf8")


def _view_box(path: Path) -> str | None:
    m = VIEWBOX_RE.search(_read(path))
    return m.group(1) if m else None


def check_keys(manifest: dict, where: str) -> list[str]:
    """T1. The one check `make orbs` also runs, on the tuple defined above."""
    missing = [k for k in REQUIRED_KEYS if k not in manifest]
    if not missing:
        return []
    return [
        f"{where}: manifest.json has no {', '.join(missing)} — rebuild the "
        "bikar CLI (npm run build -w packages/cli) and re-run make orbs"
    ]


def instrument_path(orb: str, view: str, representation: str) -> Path:
    """Where the shipped view for this orb lives.

    Cells at the top level of the orb's view directory, ribbons one down —
    the same split `--format views` writes and `qiyas orb-validate` reads.
    """
    base = VIEWS / orb
    if representation == "ribbons":
        base = base / "ribbons"
    return base / f"{orb}.{view}.svg"


def check_orb(d: Path) -> list[str]:  # noqa: C901 — one rule per block, read top to bottom
    """Every rule against one orb directory. Returns findings, empty if clean."""
    orb = d.name
    mf = d / "manifest.json"
    if not mf.exists():
        return [f"{orb}: no manifest.json"]
    try:
        m = json.loads(_read(mf))
    except json.JSONDecodeError as exc:
        return [f"{orb}: manifest.json is not JSON — {exc}"]

    findings = check_keys(m, orb)
    if findings:
        return findings  # every later rule reads a key this one just declared missing

    frames = m["frames"]
    turntable = m["turntable"]
    transition = m["transition"]

    # --- T5: named files exist, and nothing on disk is unnamed --------------
    named = {m["source"]}
    if m["flat"]:
        named.add(m["flat"]["file"])
    for f in frames + turntable + ((transition or {}).get("frames") or []):
        named.add(f["file"])
    for name in sorted(named):
        if not (d / name).exists():
            findings.append(f"{orb}: manifest names {name}, which is not on disk")
    for svg in sorted(d.glob("*.svg")):
        if svg.name not in named:
            findings.append(
                f"{orb}: {svg.name} is on disk and named by nothing in the "
                "manifest — a frame the generator stopped writing is not "
                "removed by writing the others"
            )
    if findings:
        return findings  # the rules below open files, and some of them are gone

    # --- T2: one viewBox across stages, tilt and spin -----------------------
    boxes = {}
    for f in frames + turntable + ((transition or {}).get("frames") or []):
        boxes.setdefault(_view_box(d / f["file"]), []).append(f["file"])
    if len(boxes) > 1:
        shapes = "; ".join(f"{k} ({len(v)} frame(s), e.g. {v[0]})" for k, v in boxes.items())
        findings.append(f"{orb}: the picture changes size mid-story — {shapes}")

    # --- T6: the scaffold is on the stages and off the finished drawing -----
    for f in frames:
        if f["kind"] not in STAGE_KINDS:
            findings.append(f"{orb}: {f['file']} has unknown kind {f['kind']!r}")
            continue
        svg = _read(d / f["file"])
        if "data-orb-style" in svg:
            findings.append(
                f"{orb}: {f['file']} carries data-orb-style — shading belongs to "
                "the spin, and it makes an unplaced region and a dim placed one "
                "look alike"
            )
        if LIMB_MARK not in svg:
            findings.append(
                f"{orb}: {f['file']} is missing {LIMB_MARK} — nothing in the frame "
                "says the drawing is on a ball rather than on a plate, and that is "
                "the whole question the page exists to answer"
            )
        if f["kind"] == "complete":
            if SCAFFOLD_MARK in svg:
                findings.append(
                    f"{orb}: the complete frame {f['file']} carries {SCAFFOLD_MARK} — "
                    "nothing is left to place, so an outline showing how far along "
                    "the build is has nothing to show"
                )
        elif SCAFFOLD_MARK not in svg:
            findings.append(
                f"{orb}: stage frame {f['file']} is missing {SCAFFOLD_MARK} — the "
                "pattern is building up against a blank page with nothing under it"
            )
        stray = sorted(set(FILL_RE.findall(svg)) - STAGE_FILLS)
        if stray:
            findings.append(f"{orb}: stage frame {f['file']} fills with {', '.join(stray)}")

    # --- T7: a cell stage stays inside the solid it is being copied onto ----
    # The scaffold is a picture of a claim — "the pattern lands on these
    # faces" — and a claim a picture can contradict. It did: the solid was
    # drawn corner to corner, and a straight line between two points on a
    # sphere runs inside it, so the pattern overhung its own outline by
    # 5.8% of the radius on RosetteWeaveOrb. Nothing caught it, because
    # T6 only ever asked whether the scaffold was *there*.
    base = next((f for f in frames if f["kind"] == "base"), None)
    if base is not None:
        outline, _ = _polygons(_read(d / base["file"]))
        if not outline:
            findings.append(f"{orb}: the base frame {base['file']} draws no scaffold at all")
        else:
            for f in frames:
                if f["kind"] not in CONTAINED_KINDS:
                    continue
                _, drawn = _polygons(_read(d / f["file"]))
                worst = 0.0
                for ring in drawn:
                    for pt in ring:
                        if not any(_inside(pt, o) for o in outline):
                            worst = max(worst, _distance_to(pt, outline))
                if worst > CONTAINMENT_SLACK_MM:
                    findings.append(
                        f"{orb}: {f['file']} overhangs the base solid by {worst:.2f} mm — "
                        "the pattern is bursting through the outline that is supposed "
                        "to contain it, so the outline is not the surface the pattern "
                        "is on"
                    )

    # --- T3: the story ends on the shipped drawing --------------------------
    last = frames[-1]
    if last["kind"] != "complete":
        findings.append(
            f"{orb}: the sequence ends on {last['kind']!r}, not 'complete' — the "
            "last thing a viewer sees is a frame with a copy still highlighted"
        )
    else:
        shipped = instrument_path(orb, last["view"], last.get("representation") or "cells")
        if not shipped.exists():
            findings.append(
                f"{orb}: the complete frame claims to be {shipped.relative_to(ROOT)}, "
                "which does not exist — run make orbs"
            )
        else:
            white = shipped.read_text(encoding="utf8")
            actual = (d / last["file"]).read_text(encoding="utf8")
            radius = SILHOUETTE_RE.search(actual)
            if WHITE_RECT not in white:
                findings.append(
                    f"{orb}: {shipped.relative_to(ROOT)} does not paint {WHITE_RECT} — "
                    "the instrument view moved, so the substitutions this rule allows "
                    "can no longer be the only differences it is checking"
                )
            elif LIMB_MARK in white or "orb-limb" in white:
                findings.append(
                    f"{orb}: {shipped.relative_to(ROOT)} already draws the limb — the "
                    "instrument set is not supposed to, and a substitution that is "
                    "already there stops being one this rule can check"
                )
            elif radius is None:
                findings.append(
                    f"{orb}: the complete frame {last['file']} draws no limb circle in "
                    "the form this rule names, so there is nothing to derive from"
                )
            # The radius is read off the frame under test rather than recomputed
            # here: the claim is that the limb is the *only* addition, not that
            # this gate can predict where it sits.
            elif _wearing_limb(white.replace(WHITE_RECT, GROUND_RECT), radius[1]) != actual:
                findings.append(
                    f"{orb}: the complete frame is not {shipped.relative_to(ROOT)} "
                    f"repainted onto {GROUND} and wearing the limb — the page teaches "
                    "the construction of a drawing nobody ships"
                )

    # --- T4: both junctions are byte identities -----------------------------
    if transition and transition["frames"]:
        rows = transition["frames"]
        if last["kind"] == "complete":
            if (d / rows[0]["file"]).read_bytes() != (d / last["file"]).read_bytes():
                findings.append(
                    f"{orb}: the tilt does not start on the complete frame — "
                    f"{rows[0]['file']} != {last['file']}"
                )
        enters = transition["entersAtIndex"]
        if not 0 <= enters < len(turntable):
            findings.append(f"{orb}: entersAtIndex {enters} is outside a {len(turntable)}-frame orbit")
        elif (d / rows[-1]["file"]).read_bytes() != (d / turntable[enters]["file"]).read_bytes():
            findings.append(
                f"{orb}: the tilt does not land on the orbit — {rows[-1]['file']} "
                f"!= {turntable[enters]['file']} (entersAtIndex {enters})"
            )

    # --- T1 tail: the source round-trips ------------------------------------
    digest = hashlib.sha256((d / m["source"]).read_bytes()).hexdigest()
    if digest != m["sourceSha256"]:
        findings.append(
            f"{orb}: sourceSha256 is {m['sourceSha256'][:12]}… but {m['source']} "
            f"hashes to {digest[:12]}… — the page would offer a source that did "
            "not produce these frames"
        )
    return findings


def run(dirs: list[Path], keys_only: bool = False) -> int:
    findings: list[str] = []
    for d in dirs:
        if keys_only:
            mf = d / "manifest.json"
            if not mf.exists():
                findings.append(f"{d.name}: no manifest.json")
                continue
            findings += check_keys(json.loads(_read(mf)), d.name)
        else:
            findings += check_orb(d)
    for f in findings:
        print(f, file=sys.stderr)
    scope = "manifest key(s)" if keys_only else "orb breakdown(s)"
    print(f"timelapse: {len(dirs)} {scope} checked")
    if findings:
        print(
            f"\ntimelapse-gate: {len(findings)} finding(s). Override once with "
            "TIMELAPSE_GATE_OK=1 git commit",
            file=sys.stderr,
        )
        return 1
    print("OK")
    return 0


# --- self-test -------------------------------------------------------------
#
# Every rule is proved by the mutation it exists to catch, on a fixture built
# from scratch each time. The pristine fixture must come back clean first: a
# gate that fires on everything is not evidence that it fires on the right
# thing, and "everything passes" is exactly the claim a by-design failure has
# to be able to contradict.

# Laid out the way bikar lays it out — one element per line, two-space indent
# — because T3's limb derivation is anchored on line boundaries. A fixture in a
# shape the renderer never emits would prove the rule fires on the fixture.
_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-70 -70 140 140">\n'
    '  <rect x="-70" y="-70" width="140" height="140" {rect} />\n'
    "{body}"
    "</svg>"
)
# The radius the fixture's limb is drawn at. Two decimals because that is what
# the renderer writes, and `SILHOUETTE_RE` reads the digits back out.
_R = "60.00"
# Two grounds, because the whole point of T3's substitution is that they
# differ: the instrument view keeps the renderer's white default and every
# frame the page shows is repainted. A fixture painted one colour throughout
# would pass T3 by never exercising it.

def _shipped_svg(body: str) -> str:
    return _SVG.format(rect=WHITE_RECT, body=body)


def _frame_svg(body: str) -> str:
    return _SVG.format(rect=GROUND_RECT, body=body)


def _limbed(svg: str) -> str:
    """A display frame: the ground already painted, now wearing the limb."""
    return _wearing_limb(svg, _R)


_PATTERN = '  <path d="M0 0" fill="#8a8a8a" stroke="#333333" />\n'
# The finished drawing: no scaffold, no limb, nothing but the pattern. The
# instrument version is what ships; the frame version is what `complete` and
# `transition[0]` have to equal, and the two differ by the ground alone.
_SHIPPED = _shipped_svg(_PATTERN)
_DONE = _limbed(_frame_svg(_PATTERN))
# What every stage frame carries underneath: the bare solid as an outline, and
# the sphere's limb, so a viewer has something to watch the pattern land on.
# Real rings, not `M0 0`: T7 measures whether the pattern sits inside the
# solid, and a degenerate path cannot fail a containment test — the fixture
# would pass the rule by having no geometry rather than by satisfying it.
_FACE = "M-40,-40 L40,-40 L40,40 L-40,40 Z"
_UNIT = "M-20,-20 L20,-20 L20,20 L-20,20 Z"
_SCAFFOLD = f'  <path d="{_FACE}" fill="none" stroke="#c8c8c8" data-orb-scaffold="true" />\n'
_BARE = _limbed(_frame_svg(_SCAFFOLD))
_HELD = _limbed(
    _frame_svg(_SCAFFOLD + f'  <path d="{_UNIT}" fill="#c9782e" stroke="#333333" />\n')
)
_SPUN = _limbed(
    _frame_svg('  <path d="M0 0" fill="#6f6f6f" stroke="#333333" data-orb-style="shaded" />\n')
)


def _fixture(tmp: Path) -> Path:
    """A minimal breakdown that satisfies every rule, plus its shipped view."""
    src = "orb TestOrb\n"
    views = tmp / "build" / "orb-views" / "TestOrb"
    d = tmp / "build" / "orb-breakdown" / "TestOrb"
    views.mkdir(parents=True)
    d.mkdir(parents=True)
    (views / "TestOrb.vertex-3.svg").write_text(_SHIPPED, encoding="utf8")
    (d / "source.bkr").write_text(src, encoding="utf8")
    files = {
        "TestOrb.flat.svg": _frame_svg(""),
        "TestOrb.vertex-3.base.000.svg": _BARE,
        "TestOrb.vertex-3.element.001.svg": _HELD,
        "TestOrb.vertex-3.complete.000.svg": _DONE,
        "TestOrb.transition.000.svg": _DONE,           # == the complete frame
        "TestOrb.transition.001.svg": _SPUN,           # == turntable[1]
        "TestOrb.turntable.000.svg": _limbed(_frame_svg('  <path d="M9 9" fill="#6f6f6f" />\n')),
        "TestOrb.turntable.001.svg": _SPUN,
    }
    for name, text in files.items():
        (d / name).write_text(text, encoding="utf8")
    manifest = {
        "orb": "TestOrb",
        "views": ["vertex-3"],
        "frames": [
            {"file": "TestOrb.vertex-3.base.000.svg", "view": "vertex-3", "kind": "base", "index": 0},
            {"file": "TestOrb.vertex-3.element.001.svg", "view": "vertex-3", "kind": "element", "index": 1},
            {
                "file": "TestOrb.vertex-3.complete.000.svg",
                "view": "vertex-3",
                "kind": "complete",
                "index": 0,
                "representation": "cells",
            },
        ],
        "turntable": [
            {"file": "TestOrb.turntable.000.svg", "index": 0},
            {"file": "TestOrb.turntable.001.svg", "index": 1},
        ],
        "turntableRepresentation": "cells",
        "transition": {
            "frames": [
                {"file": "TestOrb.transition.000.svg", "index": 0},
                {"file": "TestOrb.transition.001.svg", "index": 1},
            ],
            "entersAtIndex": 1,
        },
        "flat": {"file": "TestOrb.flat.svg", "relation": "lifted"},
        "base": {"faces": 4, "vertices": 4, "sides": [3]},
        "weave": None,
        "source": "source.bkr",
        "sourceSha256": hashlib.sha256(src.encode("utf8")).hexdigest(),
        "engine": "0.0.0-test",
    }
    (d / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf8")
    return d


def _edit_manifest(d: Path, mutate) -> None:
    m = json.loads(_read(d / "manifest.json"))
    mutate(m)
    (d / "manifest.json").write_text(json.dumps(m, indent=2), encoding="utf8")


def _drop_key(d: Path) -> None:
    _edit_manifest(d, lambda m: m.pop("weave"))


def _resize_a_frame(d: Path) -> None:
    p = d / "TestOrb.turntable.000.svg"
    p.write_text(_read(p).replace('viewBox="-70 -70 140 140"', 'viewBox="-90 -90 180 180"'), encoding="utf8")


def _change_the_shipped_view(d: Path) -> None:
    p = d.parents[1] / "orb-views" / "TestOrb" / "TestOrb.vertex-3.svg"
    p.write_text(_read(p).replace('fill="#8a8a8a"', 'fill="#8b8b8b"'), encoding="utf8")


def _leave_the_ending_white(d: Path) -> None:
    # The substitution T3 allows, not made: a `complete` frame still on the
    # instrument's white ground, alone among grey siblings. It is the exact
    # frame the reader ends on, and the one the eye would catch last.
    p = d / "TestOrb.vertex-3.complete.000.svg"
    p.write_text(_read(p).replace(GROUND_RECT, WHITE_RECT), encoding="utf8")


def _repaint_the_shipped_view(d: Path) -> None:
    # The other direction: `--format views` starts writing the page's ground
    # too. Nothing about the *frames* is wrong, and a rule that only compared
    # the derived expectation would go quiet — qiyas's instrument would have
    # moved and T3 would still say OK.
    p = d.parents[1] / "orb-views" / "TestOrb" / "TestOrb.vertex-3.svg"
    p.write_text(_read(p).replace(WHITE_RECT, GROUND_RECT), encoding="utf8")


def _end_on_a_highlight(d: Path) -> None:
    def mutate(m):
        m["frames"][-1]["kind"] = "repeat"
    _edit_manifest(d, mutate)


def _shade_a_stage_frame(d: Path) -> None:
    p = d / "TestOrb.vertex-3.element.001.svg"
    p.write_text(_read(p).replace("<path", '<path data-orb-style="shaded"', 1), encoding="utf8")


def _tint_a_stage_frame(d: Path) -> None:
    p = d / "TestOrb.vertex-3.element.001.svg"
    p.write_text(_read(p).replace('fill="#c9782e"', 'fill="#c79a2e"'), encoding="utf8")


def _strip_the_scaffold(d: Path) -> None:
    p = d / "TestOrb.vertex-3.element.001.svg"
    p.write_text(_read(p).replace(' data-orb-scaffold="true"', ""), encoding="utf8")


def _scaffold_the_finished_drawing(d: Path) -> None:
    p = d / "TestOrb.vertex-3.complete.000.svg"
    p.write_text(_read(p).replace("<path", _SCAFFOLD + "<path", 1), encoding="utf8")


def _blind_the_ending(d: Path) -> None:
    # The defect this rule was rewritten for, put back. The finished orb is
    # the picture a reader stops on, and without the limb it is a flat
    # rosette: nothing in the frame says the drawing is on a ball. It used to
    # be the *correct* state, held that way so T3 could name one substitution.
    p = d / "TestOrb.vertex-3.complete.000.svg"
    p.write_text(SILHOUETTE_RE.sub("", _read(p), count=1), encoding="utf8")


def _resize_the_ending_limb(d: Path) -> None:
    # The limb present but wrong. A presence check would pass this; the point
    # of deriving the whole file is that the circle has to be the one the
    # renderer would have drawn, not merely a circle.
    p = d / "TestOrb.vertex-3.complete.000.svg"
    p.write_text(_read(p).replace(f'r="{_R}" fill="none"', 'r="59.00" fill="none"'), encoding="utf8")


def _limb_the_shipped_view(d: Path) -> None:
    # The other direction, and the one that makes the rule go quiet rather
    # than fail: `--format views` starts drawing the limb itself. The frames
    # would be fine and qiyas's instrument would have grown a contour it
    # classifies as foreign — exactly what the substitution exists to keep out.
    p = d.parents[1] / "orb-views" / "TestOrb" / "TestOrb.vertex-3.svg"
    p.write_text(_limbed(_read(p)), encoding="utf8")


def _burst_the_outline(d: Path) -> None:
    p = d / "TestOrb.vertex-3.element.001.svg"
    p.write_text(_read(p).replace(_UNIT, "M50,50 L58,50 L58,58 L50,58 Z"), encoding="utf8")


def _miss_the_orbit(d: Path) -> None:
    p = d / "TestOrb.transition.001.svg"
    p.write_text(_read(p).replace('d="M0 0"', 'd="M0 1"'), encoding="utf8")


def _enter_off_the_end(d: Path) -> None:
    def mutate(m):
        m["transition"]["entersAtIndex"] = 7
    _edit_manifest(d, mutate)


def _lose_a_named_file(d: Path) -> None:
    (d / "TestOrb.flat.svg").unlink()


def _leave_an_orphan(d: Path) -> None:
    (d / "TestOrb.vertex-3.element.099.svg").write_text(_HELD, encoding="utf8")


def _edit_the_source(d: Path) -> None:
    (d / "source.bkr").write_text("orb SomethingElse\n", encoding="utf8")


CASES = [
    ("T1 a missing manifest key", _drop_key, "has no weave"),
    ("T2 a frame from a different projection", _resize_a_frame, "changes size mid-story"),
    ("T3 the shipped view moved under the story", _change_the_shipped_view, "repainted onto"),
    ("T3 the ending is left on the instrument's white", _leave_the_ending_white, "repainted onto"),
    ("T3 the instrument view takes the page's ground", _repaint_the_shipped_view, "does not paint"),
    ("T3 the story ends on a highlighted copy", _end_on_a_highlight, "not 'complete'"),
    ("T6 a shaded stage frame", _shade_a_stage_frame, "carries data-orb-style"),
    ("T6 a stage frame in gallery gold", _tint_a_stage_frame, "fills with"),
    ("T6 a stage frame with nothing under it", _strip_the_scaffold, "is missing"),
    ("T6 a scaffold left on the finished drawing", _scaffold_the_finished_drawing, "carries data-orb-scaffold"),
    ("T6 the finished orb left without its limb", _blind_the_ending, "is missing data-orb-silhouette"),
    ("T3 the ending's limb is a circle but not the right one", _resize_the_ending_limb, "wearing the limb"),
    ("T3 the instrument view starts drawing the limb", _limb_the_shipped_view, "already draws the limb"),
    ("T7 a unit that bursts through the outline", _burst_the_outline, "overhangs the base solid"),
    ("T4 the tilt lands beside the orbit", _miss_the_orbit, "does not land on the orbit"),
    ("T4 entersAtIndex past the orbit", _enter_off_the_end, "outside a 2-frame orbit"),
    ("T5 a named file that is not there", _lose_a_named_file, "not on disk"),
    ("T5 a frame nothing names", _leave_an_orphan, "named by nothing"),
    ("the source no longer hashes to its pin", _edit_the_source, "sourceSha256"),
]


def self_test() -> int:
    import shutil
    import tempfile

    global VIEWS, ROOT  # noqa: PLW0603 — the fixture *is* a different tree
    real_views, real_root = VIEWS, ROOT
    failures = 0
    tmp = Path(tempfile.mkdtemp(prefix="timelapse-gate-"))
    try:
        for label, mutate, want in [("the fixture itself is clean", None, None)] + CASES:
            case = tmp / label.replace(" ", "_").replace("'", "")
            case.mkdir()
            d = _fixture(case)
            ROOT, VIEWS = case, case / "build" / "orb-views"
            if mutate:
                mutate(d)
            found = check_orb(d)
            if want is None:
                ok, why = not found, f"clean fixture reported {found}"
            else:
                ok = any(want in f for f in found)
                why = f"wanted {want!r}, got {found or 'nothing'}"
            failures += 0 if ok else 1
            print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}" + ("" if ok else f" — {why}"))
    finally:
        ROOT, VIEWS = real_root, real_views
        shutil.rmtree(tmp, ignore_errors=True)
    # The skip is a verdict too: an absent build/ exits 0 and says so, while a
    # present-but-empty one still fails — asserted here so a future edit cannot
    # quietly turn the skip back into the failure the hook and the make target
    # used to disagree about.
    with tempfile.TemporaryDirectory() as tmp:
        absent = main([str(Path(tmp) / "never-built")])
        ok = absent == 0
        failures += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: an absent build/ is a skip, exit 0 (got {absent})")
        empty = main([tmp])
        ok = empty == 1
        failures += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: a build/ with no manifest is a failure, exit 1 (got {empty})")
    print("self-test: " + ("PASS" if failures == 0 else f"FAIL ({failures})"))
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    keys_only = "--keys" in argv
    rest = [a for a in argv if not a.startswith("--")]
    root = Path(rest[0]) if rest else BREAKDOWN
    if not root.is_dir():
        # Nothing rendered yet is not a failure: a fresh clone or worktree has
        # no build/ at all. The hook used to make this call and the make target
        # did not, so `make validate` failed where `git commit` passed — the
        # gate owns the decision now and both paths share it. An existing
        # build/ with no manifest in it stays a failure below: that is a build
        # that ran and produced nothing, which is the thing to look at.
        print(f"timelapse: no {root} — nothing rendered yet, skipping", file=sys.stderr)
        return 0
    dirs = sorted(p for p in root.iterdir() if (p / "manifest.json").exists())
    if not dirs:
        print(f"timelapse-gate: no orb under {root} wrote a manifest.json", file=sys.stderr)
        return 1
    return run(dirs, keys_only=keys_only)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
