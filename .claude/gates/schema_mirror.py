#!/usr/bin/env python3
"""Schema-mirror gate: bikar's vendored qiyas contract must equal qiyas's, at the pins.

WHAT IT HOLDS. qiyas is the producer of record for the render contract: its
Pydantic models are exported to `src/qiyas/contract/schemas/*.json`, and bikar
vendors those files **byte-identical** into `packages/qiyas-schema/schemas/`
before generating the TypeScript the web pages type against. Nothing in either
repo compares the two — qiyas cannot see bikar, and bikar's codegen is happy to
regenerate from whatever it was last handed. So the mirror can lag silently.

It did. qiyas SCHEMA 1.27 added `drop`, `surplus` and `max_drift` to `Scores`;
bikar's `Scores` still had four fields, and the orb instrument page derived the
three from the diff buckets rather than reading them (docs/plan.md row 2.9,
found building 2.1.d). The fix was one re-vendor (bikar #145); this gate is the
half that makes the drift visible the next time, from the one repo that reads
both producers.

WHERE IT READS. The use-case map (`.claude/skills/maintain-use-cases/use-cases.md`)
already pins a `bikar` and a `qiyas` commit in its `as_of` frontmatter. Both
schema directories are read **at those pins**, via `git show` in the sibling
checkout — never the working tree, which is whatever another session has
checked out (docs/decisions-log.md D-001; same rule as `doc_pointers.py`). So
the verdict is about the pinned pair, offline, and moves only when
`validate.py --refresh` re-pins. A stale mirror then shows up as: re-pin bikar,
the gate fires, the repair is bikar's `release-the-schema-mirror` runbook.

WHAT A FINDING SAYS. A stem qiyas ships that bikar does not vendor, or vice
versa; a stem whose bytes differ — named down to the `$defs` entry and the
property / `required` names that differ, since "diff.json differs" is not a
repair instruction and "Scores lacks drop, max_drift, surplus" is. Bytes equal
after JSON parsing but not before is still a finding: the runbook demands the
vendored copy be byte-identical, so a reformatted copy is a copy that was not
produced by the runbook.

SKIPS. A sibling that is not checked out at all is a warning and a skip, in the
same words the other sibling-reading gates use ("not checked out locally") so
`.githooks/tests/hook-env-git-dir.sh` can hold this gate to the same rule as
the rest. A sibling that is checked out but does not have the pinned commit is
**not** a skip: the pin is the map's, it exists on origin, and `git fetch` is
the repair. That is reported and fails.

    schema_mirror.py               compare, exit 1 on any finding
    schema_mirror.py --self-test   fixed fixtures, then a tempdir layout with a
                                   primary clone, a linked worktree and both
                                   siblings, asserting the same verdict from each
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from doc_pointers import _git_env, _sibling_root  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

#: Where each repo keeps the contract, relative to its root.
QIYAS_SCHEMAS = "src/qiyas/contract/schemas"
BIKAR_SCHEMAS = "packages/qiyas-schema/schemas"

#: The map whose `as_of` block pins both siblings.
USE_CASES_REL = ".claude/skills/maintain-use-cases/use-cases.md"

PIN_LINE = re.compile(r"^\s+(bikar|qiyas):\s*([0-9a-f]{40})\s*$")

REPAIR = (
    "repair: in bikar, follow .claude/skills/release-the-schema-mirror/SKILL.md "
    "(re-vendor byte-identical from qiyas, regenerate src/*.ts, bump the package), "
    "merge, then `python3 .claude/skills/maintain-use-cases/validate.py --refresh` here"
)


# --------------------------------------------------------------------------- pins


def read_pins(root: Path) -> dict[str, str]:
    """The `bikar` and `qiyas` commits from the use-case map's `as_of` block."""
    text = (root / USE_CASES_REL).read_text(encoding="utf-8")
    head = text.split("\n---", 2)[0] if text.startswith("---") else ""
    pins: dict[str, str] = {}
    for line in head.splitlines():
        m = PIN_LINE.match(line)
        if m:
            pins[m.group(1)] = m.group(2)
    return pins


# ------------------------------------------------------------------- sibling reads


def _git(repo: Path, *args: str) -> str | None:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            check=True,
            env=_git_env(),
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def schemas_at(repo: Path, pin: str, rel_dir: str) -> dict[str, bytes] | None:
    """`{stem: bytes}` for every `*.json` under `rel_dir` at `pin`; None if `pin` is unusable."""
    listing = _git(repo, "ls-tree", "-r", "--name-only", pin, "--", rel_dir)
    if listing is None:
        return None
    out: dict[str, bytes] = {}
    for path in listing.splitlines():
        if not path.endswith(".json"):
            continue
        blob = subprocess.run(
            ["git", "-C", str(repo), "show", f"{pin}:{path}"],
            capture_output=True,
            check=True,
            env=_git_env(),
        ).stdout
        out[Path(path).stem] = blob
    return out


# ---------------------------------------------------------------------- compare


def _defs(doc: dict) -> dict:
    return doc.get("$defs") or doc.get("definitions") or {}


def _shape_diff(name: str, ours: dict, theirs: dict) -> list[str]:
    """Property and `required` names present in `theirs` (qiyas) and absent in `ours` (bikar), and the reverse."""
    out: list[str] = []
    for key in ("properties", "required"):
        a = set(ours.get(key) or [])
        b = set(theirs.get(key) or [])
        if b - a:
            out.append(f"{name}.{key} lacks in bikar: {', '.join(sorted(b - a))}")
        if a - b:
            out.append(f"{name}.{key} extra in bikar: {', '.join(sorted(a - b))}")
    return out


def describe_difference(stem: str, bikar: bytes, qiyas: bytes) -> str:
    """One finding line for a stem whose bytes differ, naming what differs."""
    try:
        b, q = json.loads(bikar), json.loads(qiyas)
    except ValueError:
        return f"{stem}.json: bytes differ and at least one side is not JSON"
    if b == q:
        return f"{stem}.json: JSON-equal but not byte-identical — re-vendor, do not reformat"
    details = _shape_diff(stem, b, q)
    bd, qd = _defs(b), _defs(q)
    for name in sorted(set(bd) | set(qd)):
        if name not in bd:
            details.append(f"$defs.{name} missing in bikar")
        elif name not in qd:
            details.append(f"$defs.{name} missing in qiyas")
        else:
            details.extend(_shape_diff(name, bd[name], qd[name]))
    if not details:
        details.append("differs below the property level (a type, a default, a description)")
    return f"{stem}.json differs: " + "; ".join(details)


def compare(bikar: dict[str, bytes], qiyas: dict[str, bytes]) -> list[str]:
    """Findings between bikar's vendored copy and qiyas's export. Empty means mirrored."""
    findings: list[str] = []
    for stem in sorted(set(bikar) | set(qiyas)):
        if stem not in bikar:
            findings.append(f"{stem}.json: qiyas ships it, bikar does not vendor it")
        elif stem not in qiyas:
            findings.append(f"{stem}.json: bikar vendors it, qiyas no longer ships it")
        elif bikar[stem] != qiyas[stem]:
            findings.append(describe_difference(stem, bikar[stem], qiyas[stem]))
    return findings


# -------------------------------------------------------------------------- run


def run(root: Path) -> tuple[list[str], list[str]]:
    """(findings, warnings) for the repo at `root`, reading siblings at the map's pins."""
    pins = read_pins(root)
    warnings: list[str] = []
    missing_pin = [r for r in ("bikar", "qiyas") if r not in pins]
    if missing_pin:
        return [f"{USE_CASES_REL}: no as_of pin for {', '.join(missing_pin)}"], warnings
    trees: dict[str, dict[str, bytes]] = {}
    for name, rel_dir in (("bikar", BIKAR_SCHEMAS), ("qiyas", QIYAS_SCHEMAS)):
        repo = _sibling_root(name, root)
        if repo is None:
            warnings.append(f"repo '{name}' not checked out locally — skipped the schema-mirror check")
            return [], warnings
        tree = schemas_at(repo, pins[name], rel_dir)
        if tree is None:
            return [f"{name} pin {pins[name][:12]} is not in {repo} — `git -C {repo} fetch origin`"], warnings
        if not tree:
            return [f"{name}@{pins[name][:12]} has no *.json under {rel_dir}"], warnings
        trees[name] = tree
    return compare(trees["bikar"], trees["qiyas"]), warnings


def report(findings: list[str], warnings: list[str], pins: dict[str, str] | None) -> int:
    for w in warnings:
        print(f"schema-mirror: warning — {w}")
    if warnings and not findings:
        return 0
    label = ""
    if pins:
        label = f" (bikar@{pins['bikar'][:12]} vs qiyas@{pins['qiyas'][:12]})"
    if not findings:
        print(f"schema-mirror: bikar's vendored qiyas contract matches qiyas{label}")
        return 0
    print(f"schema-mirror: {len(findings)} finding(s){label}")
    for f in findings:
        print(f"  - {f}")
    print(f"  {REPAIR}")
    return 1


# --------------------------------------------------------------------- self-test


def _doc(scores_props: list[str], required: list[str]) -> bytes:
    doc = {
        "$defs": {
            "Scores": {
                "properties": {p: {"type": "number"} for p in scores_props},
                "required": required,
                "type": "object",
            }
        },
        "properties": {"scores": {"$ref": "#/$defs/Scores"}},
        "required": ["scores"],
        "title": "DiffResponse",
        "type": "object",
    }
    return (json.dumps(doc, indent=2) + "\n").encode()


FOUR = ["structural", "geometric", "symmetry", "composite"]
SEVEN = FOUR + ["drop", "surplus", "max_drift"]
QIYAS_FIXTURE = {"diff": _doc(SEVEN, FOUR + ["drop", "surplus"]), "encoding": b'{"a": 1}\n'}

#: name → (bikar tree, wanted finding count, substring every wanted finding carries)
FIXTURE_CASES: list[tuple[str, dict[str, bytes], int, str]] = [
    ("clean", dict(QIYAS_FIXTURE), 0, ""),
    # The defect that built the gate: bikar's Scores at four fields while qiyas
    # ships seven. The finding must name the def and the three fields, because
    # that is what the reader re-vendors to fix.
    (
        "scores-lag",
        {"diff": _doc(FOUR, FOUR), "encoding": QIYAS_FIXTURE["encoding"]},
        1,
        "Scores.properties lacks in bikar: drop, max_drift, surplus",
    ),
    ("stem-not-vendored", {"diff": QIYAS_FIXTURE["diff"]}, 1, "bikar does not vendor it"),
    (
        "reformatted-copy",
        {"diff": json.dumps(json.loads(QIYAS_FIXTURE["diff"])).encode(), "encoding": QIYAS_FIXTURE["encoding"]},
        1,
        "JSON-equal but not byte-identical",
    ),
]


def _fixture_cases() -> bool:
    ok = True
    for label, bikar, want, needle in FIXTURE_CASES:
        got = compare(bikar, QIYAS_FIXTURE)
        hit = len(got) == want and all(needle in f for f in got)
        ok &= hit
        detail = got[0] if got else "no findings"
        print(f"self-test {'ok  ' if hit else 'FAIL'}: {label} → {detail}")
    return ok


def _init_repo(path: Path, files: dict[str, bytes]) -> str:
    """A git repo at `path` with `files` committed; returns the commit sha."""
    path.mkdir(parents=True)
    for rel, data in files.items():
        (path / rel).parent.mkdir(parents=True, exist_ok=True)
        (path / rel).write_bytes(data)
    env = {**_git_env(), "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}
    cmds = [
        ["init", "-q"],
        ["add", "-A"],
        ["-c", "user.email=t@e.invalid", "-c", "user.name=t", "commit", "-q", "--no-verify", "-m", "fixture"],
    ]
    for c in cmds:
        subprocess.run(["git", "-C", str(path), *c], check=True, env=env, capture_output=True)
    return subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"], check=True, env=env, capture_output=True, text=True
    ).stdout.strip()


def _layout_case(tmp: Path) -> bool:
    """A primary clone, a linked worktree one level down, both siblings beside the primary.

    The worktree must reach the same verdict as the primary — the checkout-independence
    rule every sibling-reading gate here is held to. The siblings deliberately carry a
    lagging bikar so the verdict being agreed on is a *failing* one: two "nothing to
    check" runs would agree too.
    """
    qiyas_sha = _init_repo(tmp / "qiyas", {f"{QIYAS_SCHEMAS}/{k}.json": v for k, v in QIYAS_FIXTURE.items()})
    lagging = FIXTURE_CASES[1][1]
    bikar_sha = _init_repo(tmp / "bikar", {f"{BIKAR_SCHEMAS}/{k}.json": v for k, v in lagging.items()})
    map_text = (
        f"---\nname: use-cases\nas_of:\n  3d-models: {'0' * 40}\n  bikar: {bikar_sha}\n  qiyas: {qiyas_sha}\n---\n"
    )
    primary = tmp / "3d-models"
    _init_repo(primary, {USE_CASES_REL: map_text.encode()})
    wt = tmp / "3d-models.worktrees" / "gate"
    subprocess.run(
        ["git", "-C", str(primary), "worktree", "add", "-q", "--detach", str(wt)],
        check=True,
        env=_git_env(),
        capture_output=True,
    )
    saved = os.environ.pop("BIKAR_DIR", None)
    try:
        verdicts = {name: run(root) for name, root in (("primary", primary), ("worktree", wt))}
    finally:
        if saved is not None:
            os.environ["BIKAR_DIR"] = saved
    ok = True
    for name, (findings, warnings) in verdicts.items():
        hit = len(findings) == 1 and "Scores.properties lacks in bikar" in findings[0] and not warnings
        ok &= hit
        print(f"self-test {'ok  ' if hit else 'FAIL'}: layout/{name} → {findings or warnings or 'nothing'}")
    if verdicts["primary"] != verdicts["worktree"]:
        print("self-test FAIL: primary and worktree disagree")
        ok = False
    return ok


def self_test() -> int:
    ok = _fixture_cases()
    with tempfile.TemporaryDirectory() as d:
        ok &= _layout_case(Path(d))
    pins = read_pins(ROOT)
    pins_ok = {"bikar", "qiyas"} <= set(pins)
    ok &= pins_ok
    print(f"self-test {'ok  ' if pins_ok else 'FAIL'}: the use-case map pins bikar and qiyas — {sorted(pins)}")
    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="bikar's vendored qiyas contract vs qiyas's export, at the map's pins")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    findings, warnings = run(ROOT)
    pins = read_pins(ROOT)
    return report(findings, warnings, pins if {"bikar", "qiyas"} <= set(pins) else None)


if __name__ == "__main__":
    sys.exit(main())
