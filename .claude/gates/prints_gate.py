#!/usr/bin/env python3
"""Prints gate for 3d-models: a print-run record is checkable, or it is not shipped.

`docs/prints/<YYYY-MM-DD>-<slug>/` holds one `index.md` whose YAML frontmatter
pins the geometry a plate printed, the process it printed under, what it measured,
and the photos that prove it. The design is `docs/prints-tab-design.md`; the rules
this gate enforces are its §7. Four of the five ship here (R3, two-way bet
propagation to `bets.md`, is held to S4 — there is no settled bet to propagate yet;
R5, its per-record precondition, ships now):

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

  R5  **A measured bet states its expectation and verdict.** Any `readings[]`
      entry whose `settles` names a real `CAL-…` bet (not `~`) must carry a
      non-empty `expected` (the bench-sheet criterion it was tested against) and a
      `verdict` in VERDICT_VOCAB (how it landed vs that criterion). This is the
      per-record *compare* seam — it turns "did the print match what we expected?"
      into structured data the gate checks, not prose an operator may forget. It
      is the precondition for R3 and, unlike R3, has no empty-subject problem: it
      fires the moment one reading names a bet, so it ships now.

  R6  **Status is a lifecycle state.** `status` is one of the ten plate/record
      states (`draft planned sliced printing paused printed failed measured
      propagated abandoned`, print-model-design.md §3.1). Membership only — the
      consistency between a state and the fields it implies (a `measured` carries a
      reading, a `sliced` names a `.3mf`) is the freshness gate's (task #39).

  R7  **A named sheet resolves.** The optional `sheet` — the bench sheet this print
      realizes — is a repo path that must resolve to a file. Many prints map to one
      sheet (re-prints, repeated attempts), so there is deliberately no uniqueness
      constraint; only that the pointer is not dangling.

  R8  **Repeated-element count is a positive integer.** Each `objects[].count` (the
      copies of that object on the plate) defaults to 1 when omitted and, when
      present, must be a plain int >= 1 — `bool` excluded, since `count: true` is a
      mistake, not one copy.

  R9  **Feedback is a mapping.** The optional `feedback` block (the recovery loop's
      symptom/notes, task #37) must be a mapping when present. Its required-when
      rules are R11 below.

The freshness rules (R10–R14, the "freshness gate" of print-model-design.md §6.3,
task #39). R1–R9 check that a record is *well-formed*; these check that its `status`
is backed by the *evidence that state implies* (§3.1's Validator) — the state and its
fields agreeing so the lifecycle cannot lie. They live here, not in a second gate
file, because they read the same parsed frontmatter R1–R9 already hold: one parser,
one hook, one self-test (CLAUDE.md, "a migration never buys a fork"). Grouped by the
plate's physical progression:

  R10 **A sliced-or-later plate names its `.3mf`.** A record whose `status` is at or
      past `sliced` (`sliced printing paused printed failed measured propagated`) must
      carry a `plate_3mf` naming the plate it sliced / came off (§3.1). Presence +
      `.3mf` suffix only — like R7's sheet, the artifact may be large or gitignored,
      so the record must *name* it, not resolve it.

  R11 **A terminal-physical record carries a feedback block.** A `printed`, `failed`,
      `measured`, or `propagated` record carries a `feedback` block — present, even if
      empty (§6.3 PASS for `printed`; the recovery loop, task #37, for `failed`;
      `measured`/`propagated` pass through `printed`). R9 checks it is a mapping; R11
      checks it is there at all for these states.

  R12 **A `measured` record carries a reading.** `status: measured` with an empty
      `readings[]` is refused — it claims a measurement while carrying none (§6.3
      FAIL). Hard case (K6/D2): a `feedback` block does **not** discharge it —
      `measured` specifically requires a reading, so R12 checks readings, not feedback.

  R13 **A `propagated` record names a bet.** `status: propagated` must carry at least
      one `readings[].settles` naming a real `CAL-…` bet, not `~` (§3.1 FAIL). Hard
      case (K6/D2): the aggregate "the record has readings" cannot discharge it — one
      reading with a real `settles` is required.

  R14 **A shipped record is past planning.** The whole-tree gate only sees records
      under `docs/prints/` — i.e. shipped ones. A shipped record still at `draft`/
      `planned` is the drift §6.3 names: the plan artifact is composed-not-stored
      (§2), so a shipped pre-slice record must be reconciled past planning first.

  R15 **A printed piece carries its verdict.** In a `printed`, `failed`, `measured` or
      `propagated` record, every `objects[]` entry carries a `verdict` in
      PIECE_VERDICTS (`keep` — print it again as is; `adjust` — the idea is right, change
      its params; `drop` — do not print it again), and the optional `notes` is a list of
      non-empty strings. The plate-level `feedback` cannot answer "was *this* piece good
      at *these* params": minis-03 (2026-09-26) mixed a good minimal-frame and a loose
      pegs pair at one size, and one plate note could not tell them apart. Hard case
      (K6/D2): one verdict on the plate does not discharge the rule; every object needs
      its own.

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
CAL_ID = re.compile(r"^CAL-[A-Z]+-\d+$")

# R5 — how a reading landed against its written expectation. Grounded in
# calibration-design.md §2's bracket vocabulary: the pass is the answer landing
# *inside* the ladder, and every-rung-passes / every-rung-fails is a valid
# re-centre direction, not a failure.
VERDICT_VOCAB = frozenset({"brackets", "above-range", "below-range", "refutes", "no-reading"})

# R6 — the full plate/record lifecycle (print-model-design.md §3.1). It extends the
# five states this schema first shipped (sliced/printed/measured/propagated/abandoned)
# with the pre-slice states the print-model skill owns (draft/planned) and the
# in-flight states read from the device (printing/paused/failed). R6 checks
# *membership* only; the state->required-field consistency (a `measured` carries a
# reading, a `sliced` names a .3mf) is the freshness rules R10-R14 below (task #39, §6.3).
STATUS_VOCAB = frozenset({
    "draft", "planned", "sliced", "printing", "paused",
    "printed", "failed", "measured", "propagated", "abandoned",
})

# Freshness (R10-R14, print-model-design.md §6.3) — status groups keyed to the plate's
# physical progression. POST_SLICE: a plate at or past `sliced` was sliced, so it names
# a .3mf (R10). FEEDBACK: a terminal-physical record carries the operator's account
# (R11). PRE_SHIP: a shipped record (this gate only sees docs/prints/) still at these
# pre-slice states is drift (R14). `measured` (R12) and `propagated` (R13) are singled
# out below rather than grouped, since each names a distinct evidence field.
POST_SLICE_STATES = frozenset({
    "sliced", "printing", "paused", "printed", "failed", "measured", "propagated",
})
FEEDBACK_STATES = frozenset({"printed", "failed", "measured", "propagated"})
PRE_SHIP_STATES = frozenset({"draft", "planned"})
# R15 — what the owner decided about one printed piece at the params it printed at.
PIECE_VERDICTS = ("keep", "adjust", "drop")

REQUIRED_TOP = ("run", "plate", "status", "outcome", "profile", "pins", "objects")
PROFILE_FIELDS = (
    "machine", "material", "spool", "nozzle_mm", "nozzle_type",
    "layer_mm", "slicer_profile", "ambient_c", "instrument",
)
# The "how" `print list` projects: the process-identity subset that lets an operator
# restart a plate from a number, not a memory (prints-tab-design.md §4.1). A SUBSET of
# PROFILE_FIELDS, sliced from it — never a second list of field names to drift apart.
# Order is display order.
HOW_FIELDS = ("machine", "material", "nozzle_mm", "layer_mm", "slicer_profile")
assert set(HOW_FIELDS) <= set(PROFILE_FIELDS), "HOW_FIELDS must be a subset of PROFILE_FIELDS"
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
    # Drop the GIT_* variables a hook runs under: pre-commit exports GIT_DIR and
    # GIT_INDEX_FILE for *this* repo, and `git -C bikar` would obey them and look for
    # the bikar commit in 3d-models' object store — every R1 "missing" on commit and
    # "ok" by hand (the first shipped record, minis-03, 2026-09-26).
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    proc = subprocess.run(
        ["git", "-C", str(BIKAR_DIR), "cat-file", "-p", f"{ref}:{path}"],
        capture_output=True, env=env,
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


def check_record(
    rec: Path, seen_digests: dict[str, str], shipped: bool = True
) -> tuple[list[str], int, int]:
    """Findings for one record dir, plus (readings, photos) counted for R4.

    `shipped` says whether this record lives in the shipped tree (docs/prints/) vs.
    the gitignored staging area (.bambu/records/, what `bambu validate record` scans
    by default). Only R14 depends on it: a pre-slice status is drift once *shipped*,
    but is exactly what a fresh `--record` draft looks like in staging. Every other
    rule is location-independent, so `shipped` defaults True (whole-tree callers).
    """
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

    # R6 — status is a member of the lifecycle vocabulary (design §3.1). Only
    # membership here; the state->required-field consistency is R10-R14 below. Named
    # `rec_status`, distinct from the `status` the R1 blob-resolve loop reuses below —
    # they are two unrelated states and one name for both is exactly the bug D-052
    # warns of. `status` is in REQUIRED_TOP, so it is present by the time we get here.
    rec_status = data.get("status")
    if rec_status not in STATUS_VOCAB:
        out.append(f"{name}: R6 status '{rec_status}' is not one of {sorted(STATUS_VOCAB)}")

    # R7 — sheet<->print (many-to-one). A record may name the bench sheet it realizes;
    # many prints (re-prints, repeated attempts) map to one sheet, so there is no
    # uniqueness constraint — only that the named sheet resolves to a file in the repo.
    sheet = data.get("sheet")
    if sheet is not None:
        if not isinstance(sheet, str) or not sheet.strip():
            out.append(f"{name}: R7 sheet is present but is not a path string")
        elif not (ROOT / sheet).is_file():
            out.append(f"{name}: R7 sheet '{sheet}' does not resolve to a file in the repo")

    # R9 — feedback block: optional; when present it must be a mapping (the recovery
    # loop, task #37, reads symptom/notes out of it). Its *required-when* rules (a
    # `failed` record carries a feedback block) are the freshness gate's (task #39),
    # not this structural shape check.
    feedback = data.get("feedback")
    if feedback is not None and not isinstance(feedback, dict):
        out.append(f"{name}: R9 feedback is present but is not a mapping")

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
        # R8 — repeated-element multiplicity. `count` is optional (a lone piece omits
        # it, meaning 1); when present it is how many copies of this object the plate
        # carried, so it must be a plain int >= 1. bool is an int subclass in Python
        # and `count: true` is a mistake, not a count of 1 — exclude it explicitly.
        entry_id = obj.get("entry", f"#{i}")
        count = obj.get("count", 1)
        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            out.append(f"{name}: R8 objects {entry_id} count {count!r} is not an integer >= 1")
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

    # R5 — a reading that settles a real bet must state what it was tested against
    # (`expected`) and how it landed (`verdict`). A reading with `settles: ~` is
    # exempt: it moves no bet, so there is nothing to compare it against.
    readings = data.get("readings") or []
    for i, rd in enumerate(readings if isinstance(readings, list) else []):
        if not isinstance(rd, dict):
            continue
        settles = rd.get("settles")
        if not (isinstance(settles, str) and CAL_ID.match(settles)):
            continue
        entry = rd.get("entry", f"#{i}")
        exp = rd.get("expected")
        if not (isinstance(exp, str) and exp.strip()):
            out.append(f"{name}: R5 reading {entry} settles {settles} but has no 'expected' "
                       "— the bench-sheet criterion it was tested against")
        vd = rd.get("verdict")
        if not (isinstance(vd, str) and vd in VERDICT_VOCAB):
            out.append(f"{name}: R5 reading {entry} settles {settles} but 'verdict' "
                       f"is not one of {sorted(VERDICT_VOCAB)}")

    # R10-R14 — freshness: the `status` must be backed by the evidence that state
    # implies (§3.1 Validator, §6.3). R6 above checked membership; these check
    # state->field consistency. Skipped when `status` is not a member — the R6 finding
    # already fired and the state groups below would silently miss it otherwise.
    if rec_status in STATUS_VOCAB:
        readings_list = readings if isinstance(readings, list) else []

        # R10 — a plate at or past `sliced` names the `.3mf` it sliced / came off
        # (§3.1). Presence + `.3mf` suffix only; like R7's sheet the artifact may be
        # large or gitignored, so the record must name it, not resolve it on disk.
        if rec_status in POST_SLICE_STATES:
            plate_3mf = data.get("plate_3mf")
            if not (isinstance(plate_3mf, str) and plate_3mf.strip().endswith(".3mf")):
                out.append(f"{name}: R10 status '{rec_status}' is at or past 'sliced' but "
                           "'plate_3mf' does not name a .3mf (the plate it sliced/came off)")

        # R11 — a terminal-physical record carries a feedback block, present even if
        # empty (§6.3 PASS for `printed`; the recovery loop, task #37, for `failed`).
        # R9 checked it is a mapping when present; R11 requires it be present at all.
        if rec_status in FEEDBACK_STATES and feedback is None:
            out.append(f"{name}: R11 status '{rec_status}' requires a 'feedback' block "
                       "(present, even if empty — §6.3), and none is set")

        # R15 — every printed piece carries its own verdict; notes, when present, are a
        # list of non-empty strings. Per object, not per plate (K6/D2).
        if rec_status in FEEDBACK_STATES:
            for i, obj in enumerate(objects):
                if not isinstance(obj, dict):
                    continue
                entry_id = obj.get("entry", f"#{i}")
                verdict = obj.get("verdict")
                if verdict not in PIECE_VERDICTS:
                    out.append(f"{name}: R15 objects {entry_id} verdict {verdict!r} is not one of "
                               f"{', '.join(PIECE_VERDICTS)} — say what this piece taught")
                notes = obj.get("notes", [])
                if not (isinstance(notes, list)
                        and all(isinstance(n, str) and n.strip() for n in notes)):
                    out.append(f"{name}: R15 objects {entry_id} notes is not a list of "
                               "non-empty strings")

        # R12 — a `measured` record carries at least one reading (§6.3 FAIL). Hard case
        # (K6/D2): a `feedback` block does NOT discharge it, so this checks readings.
        if rec_status == "measured" and not readings_list:
            out.append(f"{name}: R12 status 'measured' but readings[] is empty "
                       "— it claims a measurement while carrying none")

        # R13 — a `propagated` record names a bet (§3.1 FAIL). Hard case (K6/D2): the
        # aggregate "has readings" cannot discharge it — one reading must name a real
        # CAL bet, not `~`.
        if rec_status == "propagated":
            has_bet = any(
                isinstance(rd, dict) and isinstance(rd.get("settles"), str)
                and CAL_ID.match(rd["settles"])
                for rd in readings_list
            )
            if not has_bet:
                out.append(f"{name}: R13 status 'propagated' but no readings[].settles "
                           "names a bet — it claims to have moved a constant while "
                           "pointing at nothing")

        # R14 — a shipped record (docs/prints/) must be reconciled past planning before
        # it ships (§6.3, §3.2): the plan artifact is composed-not-stored, so a shipped
        # `draft`/`planned` record is drift. Scoped to the shipped tree: the very same
        # status is legitimate in the staging area (.bambu/records/), where a fresh
        # `--record` draft is always pre-slice — firing R14 there would refuse the draft
        # the scaffold's own closing line tells the operator to gate.
        if shipped and rec_status in PRE_SHIP_STATES:
            out.append(f"{name}: R14 status '{rec_status}' is pre-slice but the record is "
                       "shipped under docs/prints/ — reconcile it past planning first")

    return out, (len(readings) if isinstance(readings, list) else 0), len(listed)


def is_shipped_tree(prints: Path) -> bool:
    """True when `prints` is the shipped tree (docs/prints/), False for a staging area
    (.bambu/records/). R14's only input — the shipped-vs-staging distinction is the
    path, not the record: docs/prints/ is where a record has shipped."""
    p = prints.resolve()
    return p.name == "prints" and p.parent.name == "docs"


def record_dirs(prints: Path) -> list[Path]:
    if not prints.is_dir():
        return []
    return sorted(p for p in prints.iterdir() if p.is_dir() and (p / "index.md").exists())


def list_records(prints: Path) -> list[dict]:
    """Read-only projection of every record under `prints`, for `bambu print list`.

    One parser, not two: the CLI must never re-implement frontmatter reading, so it
    shells here instead. This is a *list*, not the gate — a record that does not
    parse is surfaced with an `error` and never silently dropped, because for the
    operator "a record is broken" is different news from "there is no record"
    (the opposite call from `build/prints_manifest.py`, which hides an unparseable
    record from the public page). Newest first is the caller's job; this returns
    directory order.
    """
    out: list[dict] = []
    for rec in record_dirs(prints):
        data, err = parse_frontmatter((rec / "index.md").read_text(encoding="utf-8"))
        if data is None:
            out.append({"run": rec.name, "error": err})
            continue
        readings = data.get("readings") or []
        readings = readings if isinstance(readings, list) else []
        settles = sorted({
            rd["settles"] for rd in readings
            if isinstance(rd, dict) and isinstance(rd.get("settles"), str)
            and CAL_ID.match(rd["settles"])
        })
        objects = data.get("objects") or []
        # The "how": the process-identity subset, so `print list --how` answers not
        # just what came off the plate but the numbers to reprint it. Absent fields
        # project as null rather than being dropped — an incomplete profile is honest
        # news, and the record gate (not this list) is what enforces completeness.
        profile = data.get("profile") or {}
        profile = profile if isinstance(profile, dict) else {}
        how = {k: profile.get(k) for k in HOW_FIELDS}
        out.append({
            "run": data.get("run", rec.name),
            "date": rec.name[:10] if RUN_NAME.match(rec.name) else None,
            "plate": data.get("plate"),
            "status": data.get("status"),
            "outcome": data.get("outcome"),
            "objects": len(objects) if isinstance(objects, list) else 0,
            "readings": len(readings),
            "settles": settles,
            "how": how,
        })
    return out


def run(prints: Path) -> int:
    dirs = record_dirs(prints)
    shipped = is_shipped_tree(prints)
    seen: dict[str, str] = {}
    findings: list[str] = []
    readings = photos = skipped = 0
    for rec in dirs:
        f, r, p = check_record(rec, seen, shipped=shipped)
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
        where = "docs/prints/" if shipped else f"{prints}/"
        print(f"prints: 0 records checked — {where} is empty (nothing printed yet)")
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
        # R10 — a measured plate is post-slice, so it names the .3mf it came off.
        "plate_3mf": f"{run_name}.3mf",
        # R11 — a measured record carries a feedback block, present even if empty.
        "feedback": {},
        "profile": {f: ("Bambu A1" if f == "machine" else 0.4 if f.endswith("_mm") else "x")
                    for f in PROFILE_FIELDS},
        "pins": {"bikar_ref": _FIX_REF, "self_ref": "~"},
        "objects": [{
            "entry": "MC-2",
            "source": f"bikar:{_FIX_SRC_PATH}",
            "source_sha256": sha,
            "piece": "keyhole",
            "count": 2,  # R8 — two copies of this coupon on the plate
            "verdict": "keep",  # R15 — a measured record says what each piece taught
            "notes": ["keyhole floor intact"],
        }],
        "readings": [{"entry": "MC-2", "quantity": "KEYHOLE_FRONT_FLOOR_MM",
                      "median_mm": 0.79, "settles": "CAL-FEA-01",
                      "expected": "≥0.8 mm survives as one clean floor",
                      "verdict": "brackets"}],
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


def _drop_expected(prints: Path) -> None:
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(re.sub(r"\n *expected:.*", "", idx.read_text(), count=1), encoding="utf-8")


def _bad_verdict(prints: Path) -> None:
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(idx.read_text().replace("verdict: brackets", "verdict: looks-good", 1),
                   encoding="utf-8")


def _bad_status(prints: Path) -> None:
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(idx.read_text().replace("status: measured", "status: half-done", 1),
                   encoding="utf-8")


def _dangling_sheet(prints: Path) -> None:
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(idx.read_text().replace(
        "outcome: readings", "outcome: readings\nsheet: docs/prints/no-such-sheet.md", 1),
        encoding="utf-8")


def _bad_count(prints: Path) -> None:
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(idx.read_text().replace("count: 2", "count: 0", 1), encoding="utf-8")


def _bad_feedback(prints: Path) -> None:
    # R9: the fixture's empty-but-present feedback mapping turned into a scalar.
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(idx.read_text().replace("feedback: {}", "feedback: just a string", 1),
                   encoding="utf-8")


def _drop_plate_3mf(prints: Path) -> None:
    # R10: a measured (post-slice) record no longer names its .3mf.
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(re.sub(r"\n *plate_3mf:.*", "", idx.read_text(), count=1), encoding="utf-8")


def _drop_feedback(prints: Path) -> None:
    # R11: a measured (terminal-physical) record with no feedback block at all.
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(re.sub(r"\n *feedback: \{\}", "", idx.read_text(), count=1), encoding="utf-8")


def _drop_piece_verdict(prints: Path) -> None:
    # R15: a measured record whose one piece carries no verdict.
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(re.sub(r"\n *verdict: keep", "", idx.read_text(), count=1), encoding="utf-8")


def _bad_piece_notes(prints: Path) -> None:
    # R15: notes written as one string, not a list.
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(re.sub(r"notes:\n *- keyhole floor intact", "notes: keyhole floor intact",
                          idx.read_text(), count=1), encoding="utf-8")


def _measured_no_readings(prints: Path) -> None:
    # R12: status stays `measured` but readings[] is emptied — the §6.3 FAIL case.
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    text = re.sub(r"\nreadings:.*?(?=\nphotos:)", "\nreadings: []", idx.read_text(),
                  count=1, flags=re.DOTALL)
    idx.write_text(text, encoding="utf-8")


def _propagated_no_bet(prints: Path) -> None:
    # R13 hard case (K6/D2): status `propagated` while the one reading present names
    # no bet (settles ~) — readings exist but the aggregate cannot discharge the claim.
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    text = idx.read_text().replace("status: measured", "status: propagated", 1)
    text = text.replace("settles: CAL-FEA-01", "settles: ~", 1)
    idx.write_text(text, encoding="utf-8")


def _shipped_planned(prints: Path) -> None:
    # R14: a record shipped under docs/prints/ but still at a pre-slice state.
    idx = prints / "2026-09-14-plate1-machine-card" / "index.md"
    idx.write_text(idx.read_text().replace("status: measured", "status: planned", 1),
                   encoding="utf-8")


CASES = [
    ("frontmatter that does not parse", _corrupt_frontmatter, "frontmatter"),
    ("run key that disagrees with the dir", _mismatch_run, "does not match the directory name"),
    ("a profile field left out", _drop_profile_field, "profile field 'instrument' is missing"),
    ("R1 a source_sha256 that is not the blob", _break_source_sha, "does not equal the blob"),
    ("R2 a photo named but not on disk", _lose_a_photo, "but no such file in the record"),
    ("R2 a photo edited after recording", _repaint_a_photo, "does not match the recorded digest"),
    ("R2 a stray binary in photos/", _add_stray_photo, "no photos[] entry names it"),
    ("R2 one JPEG backing two plates", _duplicate_photo_digest, "same sha256 as"),
    ("R5 a settled reading with no expected", _drop_expected, "has no 'expected'"),
    ("R5 a settled reading with a bad verdict", _bad_verdict, "'verdict' is not one of"),
    ("R6 a status outside the lifecycle vocab", _bad_status, "R6 status 'half-done' is not one of"),
    ("R7 a sheet that does not resolve", _dangling_sheet, "R7 sheet 'docs/prints/no-such-sheet.md'"),
    ("R8 a count that is not >= 1", _bad_count, "R8 objects MC-2 count 0 is not an integer >= 1"),
    ("R9 a feedback that is not a mapping", _bad_feedback, "R9 feedback is present but is not a mapping"),
    ("R10 a sliced-or-later plate with no .3mf", _drop_plate_3mf,
     "R10 status 'measured' is at or past 'sliced'"),
    ("R11 a terminal record with no feedback block", _drop_feedback,
     "R11 status 'measured' requires a 'feedback' block"),
    ("R12 a measured record with empty readings", _measured_no_readings,
     "R12 status 'measured' but readings[] is empty"),
    ("R13 a propagated record naming no bet", _propagated_no_bet,
     "R13 status 'propagated' but no readings[].settles"),
    ("R14 a shipped record still at planned", _shipped_planned,
     "R14 status 'planned' is pre-slice"),
    ("R15 a printed piece with no verdict", _drop_piece_verdict,
     "R15 objects MC-2 verdict None is not one of"),
    ("R15 notes that are not a list", _bad_piece_notes,
     "R15 objects MC-2 notes is not a list"),
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

        # R14 is a shipped-tree rule. A fresh `--record` draft is always pre-slice and
        # lives in the staging area (.bambu/records/, what `bambu validate record` scans
        # by default) — R14 must NOT fire there, or the gate would refuse the very draft
        # the scaffold's own closing line tells the operator to check. The same record
        # under docs/prints/ (shipped) still fires R14 (the `_shipped_planned` case above).
        _BLOB_RESOLVER = lambda ref, path: (  # noqa: E731
            ("ok", _FIX_SHA) if path == _FIX_SRC_PATH else ("missing", None))
        case = tmp / "r14-staging-draft-is-not-drift"
        staging = case / ".bambu" / "records"
        _fixture_record(staging, "2026-09-14-plate1-machine-card", _FIX_SHA, _FIX_PHOTO)
        idx = staging / "2026-09-14-plate1-machine-card" / "index.md"
        idx.write_text(idx.read_text().replace("status: measured", "status: draft", 1),
                       encoding="utf-8")
        seen = {}
        found = []
        shipped = is_shipped_tree(staging)
        for rec in record_dirs(staging):
            f, _, _ = check_record(rec, seen, shipped=shipped)
            found += [x for x in f if not x.startswith("__skip__")]
        ok = shipped is False and not any("R14" in f for f in found)
        print(f"self-test {'ok  ' if ok else 'FAIL'}: R14 does not fire on a draft in staging"
              + ("" if ok else f" — shipped={shipped}, found={found or 'nothing'}"))
        failures += 0 if ok else 1
        _BLOB_RESOLVER = None

        # A pre-commit hook exports GIT_DIR for *this* repo; `git -C bikar` must not
        # inherit it, or every R1 pin reads as "missing" (minis-03, 2026-09-26).
        fake_bikar = tmp / "fake-bikar"
        fake_bikar.mkdir()
        clean = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        git = lambda *a: subprocess.run(  # noqa: E731
            ["git", "-C", str(fake_bikar), *a], capture_output=True, text=True, env=clean,
            check=True).stdout.strip()
        git("init", "-q")
        (fake_bikar / "a.bkr").write_text("x\n", encoding="utf-8")
        git("add", "a.bkr")
        git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "t")
        head = git("rev-parse", "HEAD")
        other = tmp / "other-repo"
        other.mkdir()
        subprocess.run(["git", "-C", str(other), "init", "-q"], env=clean, check=True)
        saved_dir, saved_env = BIKAR_DIR, os.environ.get("GIT_DIR")
        BIKAR_DIR = fake_bikar
        os.environ["GIT_DIR"] = str(other / ".git")
        try:
            status, _ = resolve_blob_sha(head, "a.bkr")
        finally:
            BIKAR_DIR = saved_dir
            if saved_env is None:
                os.environ.pop("GIT_DIR", None)
            else:
                os.environ["GIT_DIR"] = saved_env
        ok = status == "ok"
        print(f"self-test {'ok  ' if ok else 'FAIL'}: R1 ignores a hook's GIT_DIR"
              + ("" if ok else f" — got {status}"))
        failures += 0 if ok else 1

        # list_records: the CLI's read-only projection. A clean fixture lists one
        # record with the fields `bambu print list` prints, and a broken record is
        # surfaced with an error, not dropped (the by-design case for a *list*).
        case = tmp / "list-records"
        case.mkdir()
        prints = _build_fixture(case)
        listed = list_records(prints)
        one = listed[0] if listed else {}
        how = one.get("how") or {}
        ok = (len(listed) == 1 and one.get("plate") == "Plate 1 — Machine Card"
              and one.get("objects") == 1 and one.get("readings") == 1
              and one.get("settles") == ["CAL-FEA-01"] and one.get("date") == "2026-09-14"
              # the "how": every HOW_FIELDS key present, none dropped, sourced from profile
              and set(how) == set(HOW_FIELDS)
              and how.get("machine") == "Bambu A1" and how.get("nozzle_mm") == 0.4)
        print(f"self-test {'ok  ' if ok else 'FAIL'}: list_records projects a clean record + its how"
              + ("" if ok else f" — got {listed}"))
        failures += 0 if ok else 1
        _corrupt_frontmatter(prints)
        listed = list_records(prints)
        ok = len(listed) == 1 and "error" in listed[0]
        print(f"self-test {'ok  ' if ok else 'FAIL'}: list_records surfaces a broken record, not drops it"
              + ("" if ok else f" — got {listed}"))
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
    if "--list" in argv:
        import json
        print(json.dumps({"records": list_records(prints)}, ensure_ascii=False))
        return 0
    return run(prints)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
