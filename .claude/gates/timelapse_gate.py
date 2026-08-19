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
  T3  **The last stage frame is the shipped view, byte for byte.** The story
      ends on the drawing qiyas scores. If it does not, the page has been
      teaching the construction of something else.
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
  T6  **Stage frames wear the scaffold; the complete frame wears nothing.**
      Every stage frame carries `data-orb-scaffold` and `data-orb-silhouette`
      — the bare solid drawn as an outline underneath, so the pattern is seen
      landing on something rather than building up against a blank page. The
      `complete` frame carries neither, because it is the drawing qiyas
      scores and T3 pins it byte for byte; a scaffold leaking onto it breaks
      that identity with a change that looks purely cosmetic. No frame in
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

# bikar's DEFAULT_ORB_VIEW_FILL and DEFAULT_ORB_HIGHLIGHT_FILL, plus the card.
STAGE_FILLS = {"#8a8a8a", "#c9782e", "#ffffff", "none"}
STAGE_KINDS = {"base", "element", "repeat", "strand", "complete"}
# What a stage frame wears and the complete frame does not: bikar writes both
# from `STAGE_STYLE` plus the scaffold underlay, and drops both for `complete`.
SCAFFOLD_MARKERS = ("data-orb-scaffold", "data-orb-silhouette")

FILL_RE = re.compile(r'fill="([^"]*)"')
VIEWBOX_RE = re.compile(r'viewBox="([^"]*)"')


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
        if f["kind"] == "complete":
            for marker in SCAFFOLD_MARKERS:
                if marker in svg:
                    findings.append(
                        f"{orb}: the complete frame {f['file']} carries {marker} — "
                        "it has to be byte-identical to the shipped view, which "
                        "carries neither"
                    )
        else:
            for marker in SCAFFOLD_MARKERS:
                if marker not in svg:
                    findings.append(
                        f"{orb}: stage frame {f['file']} is missing {marker} — the "
                        "pattern is building up against a blank page with nothing "
                        "under it"
                    )
        stray = sorted(set(FILL_RE.findall(svg)) - STAGE_FILLS)
        if stray:
            findings.append(f"{orb}: stage frame {f['file']} fills with {', '.join(stray)}")

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
        elif shipped.read_bytes() != (d / last["file"]).read_bytes():
            findings.append(
                f"{orb}: the complete frame is not {shipped.relative_to(ROOT)} byte "
                "for byte — the page teaches the construction of a drawing nobody ships"
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

_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-70 -70 140 140">'
    '<rect x="-70" y="-70" width="140" height="140" fill="#ffffff" />'
    '{body}</svg>'
)
# The finished drawing: no scaffold, no limb, nothing but the pattern. This is
# what ships as the instrument view and what `complete` and `transition[0]`
# have to equal byte for byte.
_DONE = _SVG.format(body='<path d="M0 0" fill="#8a8a8a" stroke="#333333" />')
# What every stage frame carries underneath: the bare solid as an outline, and
# the sphere's limb, so a viewer has something to watch the pattern land on.
_SCAFFOLD = (
    '<path d="M0 0" fill="none" stroke="#c8c8c8" data-orb-scaffold="true" />'
    '<circle r="60" fill="none" stroke="#333333" data-orb-silhouette="true" />'
)
_BARE = _SVG.format(body=_SCAFFOLD)
_HELD = _SVG.format(body=_SCAFFOLD + '<path d="M0 0" fill="#c9782e" stroke="#333333" />')
_SPUN = _SVG.format(
    body='<circle r="60" fill="none" stroke="#333333" data-orb-silhouette="true" />'
    '<path d="M0 0" fill="#6f6f6f" stroke="#333333" data-orb-style="shaded" />'
)


def _fixture(tmp: Path) -> Path:
    """A minimal breakdown that satisfies every rule, plus its shipped view."""
    src = "orb TestOrb\n"
    views = tmp / "build" / "orb-views" / "TestOrb"
    d = tmp / "build" / "orb-breakdown" / "TestOrb"
    views.mkdir(parents=True)
    d.mkdir(parents=True)
    (views / "TestOrb.vertex-3.svg").write_text(_DONE, encoding="utf8")
    (d / "source.bkr").write_text(src, encoding="utf8")
    files = {
        "TestOrb.flat.svg": _SVG.format(body=""),
        "TestOrb.vertex-3.base.000.svg": _BARE,
        "TestOrb.vertex-3.element.001.svg": _HELD,
        "TestOrb.vertex-3.complete.000.svg": _DONE,
        "TestOrb.transition.000.svg": _DONE,           # == the complete frame
        "TestOrb.transition.001.svg": _SPUN,           # == turntable[1]
        "TestOrb.turntable.000.svg": _SVG.format(body='<path d="M9 9" fill="#6f6f6f" />'),
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


def _miss_the_orbit(d: Path) -> None:
    p = d / "TestOrb.transition.001.svg"
    p.write_text(_read(p).replace('r="60"', 'r="59"'), encoding="utf8")


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
    ("T3 the shipped view moved under the story", _change_the_shipped_view, "byte for byte"),
    ("T3 the story ends on a highlighted copy", _end_on_a_highlight, "not 'complete'"),
    ("T6 a shaded stage frame", _shade_a_stage_frame, "carries data-orb-style"),
    ("T6 a stage frame in gallery gold", _tint_a_stage_frame, "fills with"),
    ("T6 a stage frame with nothing under it", _strip_the_scaffold, "is missing"),
    ("T6 a scaffold left on the finished drawing", _scaffold_the_finished_drawing, "carries data-orb-scaffold"),
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
    print("self-test: " + ("PASS" if failures == 0 else f"FAIL ({failures})"))
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    keys_only = "--keys" in argv
    rest = [a for a in argv if not a.startswith("--")]
    root = Path(rest[0]) if rest else BREAKDOWN
    if not root.is_dir():
        print(f"timelapse-gate: no {root} — run make orbs", file=sys.stderr)
        return 1
    dirs = sorted(p for p in root.iterdir() if (p / "manifest.json").exists())
    if not dirs:
        print(f"timelapse-gate: no orb under {root} wrote a manifest.json", file=sys.stderr)
        return 1
    return run(dirs, keys_only=keys_only)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
