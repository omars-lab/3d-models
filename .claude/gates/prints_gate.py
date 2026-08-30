#!/usr/bin/env python3
"""Prints gate for 3d-models: a print-run record is checkable, or it is not shipped.

`docs/prints/<YYYY-MM-DD>-<slug>/` holds one `index.md` whose YAML frontmatter
pins the geometry a plate printed, the process it printed under, what it measured,
and the photos that prove it. The design is `docs/prints-tab-design.md`; the rules
this gate enforces are its §7. Three of the four ship here (R3, two-way bet
propagation, is held to S4 — there is no settled bet to propagate yet):

  R1  **Identity.** Every `objects[].source_sha256` equals the sha256 of
      `objects[].source` read from bikar *at the commit the record pins*
      (`pins.bikar_ref`), not at whatever is checked out. A record that claims to
      have printed a file it cannot re-resolve is a record of nothing. When bikar
      is not checked out beside this repo the pin cannot be read, and the gate
      says so and counts it as unverified — it never passes the claim silently.

  R2  **Photos.** Every `photos[].file` exists under the record, hashes to its
      recorded `sha256`, and no unlisted binary sits in `photos/`; and no two
      records share a photo digest. The uniqueness half is the load-bearing one:
      the same JPEG standing in for two different plates is how a record library
      quietly starts lying, and it is invisible inside either record alone.

  R4  **The subject count is printed.** The gate prints how many records it
      checked. A gate that says "all pass" over zero records is byte-for-byte
      indistinguishable from a gate that is broken — `docs/issue-register-
      evaluation.md` §5.1. Printing the count is what makes an empty run honest
      instead of falsely green, and it is why this gate can ship *before* the
      first plate: at zero records it says `0 records checked`, out loud.

Plus the well-formedness the §4 Validator names: the directory is `index.md` +
`photos/`, the frontmatter parses and carries every required key, and `run`
equals the directory name.

Whole-tree, not --staged: R2's uniqueness is a fact across records and R1 reads a
sibling repo — neither is visible in the one file a staged-only scope would see.

  wholesale: make validate-prints
  override once: PRINTS_GATE_OK=1 git commit
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PRINTS = ROOT / "docs" / "prints"
BIKAR_DIR = Path(os.environ.get("BIKAR_DIR", ROOT.parent / "bikar"))

RUN_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*$")
SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")

REQUIRED_TOP = ("run", "plate", "status", "outcome", "profile", "pins", "objects")
PROFILE_FIELDS = (
    "machine", "material", "spool", "nozzle_mm", "nozzle_type",
    "layer_mm", "slicer_profile", "ambient_c", "instrument",
)
OBJECT_FIELDS = ("entry", "source", "source_sha256")

# Set by self_test() to a stub keyed on the fixture's pins, so R1 can be exercised
# without a bikar checkout. In production it stays None and the git reader runs.
_BLOB_RESOLVER = None


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha256_file(p: Path) -> str:
    return _sha256_bytes(p.read_bytes())


def resolve_blob_sha(ref: str, path: str) -> tuple[str, str | None]:
    """(status, sha) for a bikar blob at a commit. status: ok | missing | skip.

    `skip` means the claim could not be read (bikar not checked out) — never a
    pass, never a fail; it is counted and reported.
    """
    if _BLOB_RESOLVER is not None:
        return _BLOB_RESOLVER(ref, path)
    git_dir = BIKAR_DIR / ".git"
    if not git_dir.exists():
        return ("skip", None)
    proc = subprocess.run(
        ["git", "-C", str(BIKAR_DIR), "cat-file", "-p", f"{ref}:{path}"],
        capture_output=True,
    )
    if proc.returncode != 0:
        return ("missing", None)
    return ("ok", _sha256_bytes(proc.stdout))


def parse_frontmatter(text: str) -> tuple[dict | None, str | None]:
    if not text.startswith("---\n"):
        return None, "index.md has no YAML frontmatter (no leading '---' fence)"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "index.md frontmatter fence is never closed"
    block = text[4:end + 1]
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as e:
        return None, f"index.md frontmatter does not parse as YAML: {e}"
    if not isinstance(data, dict):
        return None, "index.md frontmatter does not parse to a mapping"
    return data, None


def _missing(container: dict, keys) -> list[str]:
    return [k for k in keys if k not in container]


def check_record(rec: Path, seen_digests: dict[str, str]) -> tuple[list[str], int, int]:
    """Findings for one record dir, plus (readings, photos) counted for R4."""
    name = rec.name
    out: list[str] = []
    index = rec / "index.md"
    if not index.exists():
        return [f"{name}: no index.md in the record directory"], 0, 0

    data, err = parse_frontmatter(index.read_text(encoding="utf-8"))
    if err:
        return [f"{name}: {err}"], 0, 0

    for k in _missing(data, REQUIRED_TOP):
        out.append(f"{name}: frontmatter is missing required key '{k}'")
    # Without the core keys the rest cannot be read; report what is present.
    if out:
        return out, 0, 0

    if not RUN_NAME.match(name):
        out.append(f"{name}: directory name is not <YYYY-MM-DD>-<slug>")
    if data.get("run") != name:
        out.append(f"{name}: run key '{data.get('run')}' does not match the directory name")

    profile = data.get("profile") or {}
    if not isinstance(profile, dict):
        out.append(f"{name}: profile is not a mapping")
    else:
        for f in _missing(profile, PROFILE_FIELDS):
            out.append(f"{name}: profile field '{f}' is missing")

    pins = data.get("pins") or {}
    bikar_ref = pins.get("bikar_ref") if isinstance(pins, dict) else None
    if not bikar_ref:
        out.append(f"{name}: pins.bikar_ref is missing — geometry cannot be re-resolved")

    # R1 — identity, per object, at the pinned commit.
    objects = data.get("objects") or []
    if not isinstance(objects, list) or not objects:
        out.append(f"{name}: objects[] is empty — a record with no printed object")
        objects = []
    for i, obj in enumerate(objects):
        if not isinstance(obj, dict):
            out.append(f"{name}: objects[{i}] is not a mapping")
            continue
        for f in _missing(obj, OBJECT_FIELDS):
            out.append(f"{name}: objects[{i}] is missing '{f}'")
        src = obj.get("source", "")
        decl = obj.get("source_sha256", "")
        entry = obj.get("entry", f"#{i}")
        if not isinstance(src, str) or not src.startswith("bikar:"):
            out.append(f"{name}: {entry} source '{src}' is not a bikar: path")
            continue
        if not (isinstance(decl, str) and SHA256_HEX.match(decl)):
            out.append(f"{name}: {entry} source_sha256 is not a 64-hex digest")
            continue
        if not bikar_ref:
            continue
        status, real = resolve_blob_sha(bikar_ref, src[len("bikar:"):])
        if status == "skip":
            out.append(f"__skip__{name}:{entry}")
        elif status == "missing":
            out.append(f"{name}: R1 {entry} source {src[len('bikar:'):]} "
                       f"is not tracked in bikar at {bikar_ref[:12]}")
        elif real != decl:
            out.append(f"{name}: R1 {entry} source_sha256 {decl[:12]} "
                       f"does not equal the blob read at {bikar_ref[:12]} ({real[:12]})")

    # R2 — photos: presence, digest, no strays, cross-record uniqueness.
    photos = data.get("photos") or []
    listed = set()
    photo_dir = rec / "photos"
    for i, ph in enumerate(photos if isinstance(photos, list) else []):
        if not isinstance(ph, dict) or "file" not in ph or "sha256" not in ph:
            out.append(f"{name}: photos[{i}] needs both 'file' and 'sha256'")
            continue
        rel = ph["file"]
        listed.add(rel)
        f = rec / rel
        if not f.exists():
            out.append(f"{name}: R2 photos[] names {rel} but no such file in the record")
            continue
        got = _sha256_file(f)
        if got != ph["sha256"]:
            out.append(f"{name}: R2 {rel} sha256 does not match the recorded digest")
            continue
        if got in seen_digests:
            out.append(f"{name}: R2 {rel} has the same sha256 as {seen_digests[got]} "
                       f"— one JPEG cannot back two plates")
        else:
            seen_digests[got] = f"{name}/{rel}"
    if photo_dir.is_dir():
        for f in sorted(photo_dir.iterdir()):
            if f.is_file() and f"photos/{f.name}" not in listed:
                out.append(f"{name}: R2 photos/{f.name} sits in photos/ "
                           f"but no photos[] entry names it")

    readings = data.get("readings") or []
    return out, (len(readings) if isinstance(readings, list) else 0), len(listed)


def record_dirs(prints: Path) -> list[Path]:
    if not prints.is_dir():
        return []
    return sorted(p for p in prints.iterdir() if p.is_dir() and (p / "index.md").exists())


def run(prints: Path) -> int:
    dirs = record_dirs(prints)
    seen: dict[str, str] = {}
    findings: list[str] = []
    readings = photos = skipped = 0
    for rec in dirs:
        f, r, p = check_record(rec, seen)
        skipped += sum(1 for x in f if x.startswith("__skip__"))
        findings += [x for x in f if not x.startswith("__skip__")]
        readings += r
        photos += p

    n = len(dirs)
    if findings:
        for f in findings:
            print(f, file=sys.stderr)
        print(f"\nprints-gate: {len(findings)} finding(s) across {n} record(s). "
              "See docs/prints-tab-design.md §7. Override once with "
              "PRINTS_GATE_OK=1 git commit", file=sys.stderr)
        return 1

    # R4: the count is the point. It is printed on success, empty or not.
    if n == 0:
        print("prints: 0 records checked — docs/prints/ is empty (nothing printed yet)")
    else:
        tail = f"; {skipped} source pin(s) not verified (bikar not checked out)" if skipped else ""
        print(f"prints: {n} record(s) checked, {readings} reading(s), {photos} photo(s){tail}")
    print("OK")
    return 0


# ---------------------------------------------------------------------------
# self-test: a clean fixture must come back clean, then one mutation per rule
# must fire. R1's bikar read is stubbed so the identity rule is exercised with
# no checkout — the same shape as counts_gate's fixed stub authorities.
# ---------------------------------------------------------------------------

_FIX_REF = "8dda702fc943d1876c56fe14b5b608ed53ea51e8"
_FIX_SRC_PATH = "patterns/Coupons/Machine-Card.bkr"
_FIX_BLOB = b"orb MachineCard\n// a canned coupon blob for the fixture\n"
_FIX_SHA = _sha256_bytes(_FIX_BLOB)
_FIX_PHOTO = b"\xff\xd8\xff\xe0not-a-real-jpeg-but-bytes-enough\xff\xd9"
_FIX_PHOTO_SHA = _sha256_bytes(_FIX_PHOTO)


def _fixture_record(prints: Path, run_name: str, sha: str, photo: bytes) -> Path:
    rec = prints / run_name
    (rec / "photos").mkdir(parents=True)
    (rec / "photos" / "plate-overview.jpg").write_bytes(photo)
    fm = {
        "run": run_name,
        "plate": "Plate 1 — Machine Card",
        "status": "measured",
        "outcome": "readings",
        "profile": {f: ("Bambu A1" if f == "machine" else 0.4 if f.endswith("_mm") else "x")
                    for f in PROFILE_FIELDS},
        "pins": {"bikar_ref": _FIX_REF, "self_ref": "~"},
        "objects": [{
            "entry": "MC-2",
            "source": f"bikar:{_FIX_SRC_PATH}",
            "source_sha256": sha,
            "piece": "keyhole",
        }],
        "readings": [{"entry": "MC-2", "quantity": "KEYHOLE_FRONT_FLOOR_MM",
                      "median_mm": 0.79, "settles": "~"}],
        "photos": [{"file": "photos/plate-overview.jpg",
                    "sha256": _sha256_bytes(photo),
                    "of": "the whole plate"}],
    }
    body = "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBench account.\n"
    (rec / "index.md").write_text(body, encoding="utf-8")
    return rec


def _build_fixture(tmp: Path) -> Path:
    prints = tmp / "docs" / "prints"
    _fixture_record(prints, "2026-09-14-plate1-machine-card", _FIX_SHA, _FIX_PHOTO)
    return prints


def _corrupt_frontmatter(prints: Path) -> None:
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text("---\nrun: [unclosed\n", encoding="utf-8")


def _mismatch_run(prints: Path) -> None:
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(idx.read_text().replace(
        "run: 2026-09-14-plate1-machine-card", "run: 2026-09-14-something-else", 1), encoding="utf-8")


def _drop_profile_field(prints: Path) -> None:
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(re.sub(r"\n *instrument:.*", "", idx.read_text(), count=1), encoding="utf-8")


def _break_source_sha(prints: Path) -> None:
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(idx.read_text().replace(_FIX_SHA, "f" * 64, 1), encoding="utf-8")


def _lose_a_photo(prints: Path) -> None:
    (prints / "2026-09-14-plate1-machine-card" / "photos" / "plate-overview.jpg").unlink()


def _repaint_a_photo(prints: Path) -> None:
    (prints / "2026-09-14-plate1-machine-card" / "photos" / "plate-overview.jpg").write_bytes(
        _FIX_PHOTO + b"edited")


def _add_stray_photo(prints: Path) -> None:
    (prints / "2026-09-14-plate1-machine-card" / "photos" / "extra.jpg").write_bytes(b"stray")


def _duplicate_photo_digest(prints: Path) -> None:
    # A second record reusing the first plate's exact photo bytes.
    _fixture_record(prints, "2026-09-20-plate2-machine-card", _FIX_SHA, _FIX_PHOTO)


CASES = [
    ("frontmatter that does not parse", _corrupt_frontmatter, "frontmatter"),
    ("run key that disagrees with the dir", _mismatch_run, "does not match the directory name"),
    ("a profile field left out", _drop_profile_field, "profile field 'instrument' is missing"),
    ("R1 a source_sha256 that is not the blob", _break_source_sha, "does not equal the blob"),
    ("R2 a photo named but not on disk", _lose_a_photo, "but no such file in the record"),
    ("R2 a photo edited after recording", _repaint_a_photo, "does not match the recorded digest"),
    ("R2 a stray binary in photos/", _add_stray_photo, "no photos[] entry names it"),
    ("R2 one JPEG backing two plates", _duplicate_photo_digest, "same sha256 as"),
]


def self_test() -> int:
    import shutil
    import tempfile

    global _BLOB_RESOLVER  # noqa: PLW0603 — stub the sibling repo for the fixture
    _BLOB_RESOLVER = lambda ref, path: (  # noqa: E731
        ("ok", _FIX_SHA) if path == _FIX_SRC_PATH else ("missing", None))
    failures = 0
    tmp = Path(tempfile.mkdtemp(prefix="prints-gate-"))
    try:
        for label, mutate, want in [("the fixture itself is clean", None, None)] + CASES:
            case = tmp / re.sub(r"[^a-z0-9]+", "-", label.lower())
            case.mkdir()
            prints = _build_fixture(case)
            if mutate:
                mutate(prints)
            seen: dict[str, str] = {}
            found: list[str] = []
            for rec in record_dirs(prints):
                f, _, _ = check_record(rec, seen)
                found += [x for x in f if not x.startswith("__skip__")]
            if want is None:
                ok, why = not found, f"clean fixture reported {found}"
            else:
                ok = any(want in f for f in found)
                why = f"wanted {want!r}, got {found or 'nothing'}"
            failures += 0 if ok else 1
            print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}" + ("" if ok else f" — {why}"))

        # R1 skip path: with no resolver and no bikar, a pin is unverified, not a fail.
        _BLOB_RESOLVER = None
        case = tmp / "r1-skip-when-bikar-absent"
        case.mkdir()
        prints = _build_fixture(case)
        seen = {}
        found = []
        skipped = 0
        for rec in record_dirs(prints):
            f, _, _ = check_record(rec, seen)
            skipped += sum(1 for x in f if x.startswith("__skip__"))
            found += [x for x in f if not x.startswith("__skip__")]
        global BIKAR_DIR  # noqa: PLW0603
        ok = (not found) and skipped == 1 if not (BIKAR_DIR / ".git").exists() else True
        print(f"self-test {'ok  ' if ok else 'FAIL'}: R1 unverified when bikar is absent"
              + ("" if ok else f" — got findings={found}, skipped={skipped}"))
        failures += 0 if ok else 1
    finally:
        _BLOB_RESOLVER = None
        shutil.rmtree(tmp, ignore_errors=True)
    print("self-test: " + ("PASS" if failures == 0 else f"FAIL ({failures})"))
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    rest = [a for a in argv if not a.startswith("--")]
    prints = Path(rest[0]) if rest else PRINTS
    return run(prints)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
