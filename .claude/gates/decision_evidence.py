#!/usr/bin/env python3
"""Every decision drawn from a print is linked both ways, and the print it came from
says what it was printed on.

A print record (`docs/prints/<run>/index.md`) names the decisions its pieces settled
in `feedback.decisions`. The decisions log (`docs/working-model/decisions-log.md`)
holds one `## D-xxx — title` section each. Three rules hold the two together:

  R1  every D-id a record names exists in the log, and that D section links the
      record (`../prints/<run>/`) or the record's plate page
      (`../design/plates/<plate>.md`, found through the plate page's `runs:` list);
  R2  every D section that links a record is named in that record's
      `feedback.decisions` -- a decision that cites a print as its evidence is one
      the print derived;
  R3  a record that names any decision has its setup filled in, not `~`:
      profile.machine, material, nozzle_mm, layer_mm and slicer_profile. A decision
      drawn from a print holds only for the setup it was printed on, so the setup is
      part of the evidence.

Usage:
  decision_evidence.py              check the repo, exit 1 on any failure
  decision_evidence.py --self-test  check the rules against fixtures, including
                                    one failure per rule that must be caught
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "gates"))

from prints_gate import parse_frontmatter, record_dirs  # noqa: E402

DECISION_HEAD = re.compile(r"^## (D-\d{3}) — (.+?)\s*$", re.M)
RECORD_LINK = re.compile(r"(?:\.\./|docs/)prints/(\d{4}-\d{2}-\d{2}-[a-z0-9-]+)/")
SETUP = ("machine", "material", "nozzle_mm", "layer_mm", "slicer_profile")


def decision_sections(log_text: str) -> dict[str, tuple[str, str]]:
    """D-id -> (title, body up to the next `## ` heading)."""
    heads = list(DECISION_HEAD.finditer(log_text))
    out: dict[str, tuple[str, str]] = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(log_text)
        body = log_text[m.end():end]
        nxt = re.search(r"^## ", body, re.M)
        out[m.group(1)] = (m.group(2), body[:nxt.start()] if nxt else body)
    return out


def load_records(prints: Path) -> dict[str, dict]:
    """run -> frontmatter, for every record that parses."""
    out: dict[str, dict] = {}
    for d in record_dirs(prints):
        fm, _ = parse_frontmatter((d / "index.md").read_text(encoding="utf-8"))
        if isinstance(fm, dict):
            out[d.name] = fm
    return out


def plate_of_run(plates: Path) -> dict[str, str]:
    """run -> plate page stem, from each plate page's `runs:` list."""
    out: dict[str, str] = {}
    for page in sorted(plates.glob("*.md")):
        fm, _ = parse_frontmatter(page.read_text(encoding="utf-8"))
        if isinstance(fm, dict):
            for run in fm.get("runs") or []:
                out.setdefault(str(run), page.stem)
    return out


def named_decisions(fm: dict) -> list[str]:
    fb = fm.get("feedback") if isinstance(fm.get("feedback"), dict) else {}
    return [str(d).strip() for d in (fb.get("decisions") or [])]


def links_record(body: str, run: str, plate: str | None) -> bool:
    if f"../prints/{run}/" in body or f"docs/prints/{run}/" in body:
        return True
    return bool(plate) and f"../design/plates/{plate}.md" in body


def check_r1(records, sections, plates) -> list[str]:
    errs = []
    for run, fm in records.items():
        for did in named_decisions(fm):
            if did not in sections:
                errs.append(f"R1 {run}: names {did}, which the decisions log does not have")
            elif not links_record(sections[did][1], run, plates.get(run)):
                errs.append(f"R1 {run}: names {did}, but {did} links neither "
                            f"../prints/{run}/ nor its plate page")
    return errs


def check_r2(records, sections) -> list[str]:
    errs = []
    for did, (_, body) in sections.items():
        for run in sorted(set(RECORD_LINK.findall(body))):
            if run in records and did not in named_decisions(records[run]):
                errs.append(f"R2 {did}: links the {run} record, but that record's "
                            f"feedback.decisions does not name {did}")
    return errs


def check_r3(records) -> list[str]:
    errs = []
    for run, fm in records.items():
        if not named_decisions(fm):
            continue
        prof = fm.get("profile") if isinstance(fm.get("profile"), dict) else {}
        empty = [k for k in SETUP if prof.get(k) in (None, "")]
        if empty:
            errs.append(f"R3 {run}: names decisions but its setup is blank: "
                        f"profile.{', profile.'.join(empty)}")
    return errs


def check(root: Path) -> list[str]:
    records = load_records(root / "docs" / "prints")
    log = root / "docs" / "working-model" / "decisions-log.md"
    sections = decision_sections(log.read_text(encoding="utf-8")) if log.exists() else {}
    plates = plate_of_run(root / "docs" / "design" / "plates")
    return check_r1(records, sections, plates) + check_r2(records, sections) + check_r3(records)


# ---- self-test ---------------------------------------------------------------

GOOD_PROFILE = ("profile:\n  machine: X2D\n  material: PLA\n  nozzle_mm: 0.4\n"
                "  layer_mm: 0.2\n  slicer_profile: 0.20mm Standard\n")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _fixture(tmp: Path) -> Path:
    """Two records, two decisions, all three rules holding."""
    _write(tmp / "docs/prints/2026-01-01-aa-1/index.md",
           "---\nrun: 2026-01-01-aa-1\n" + GOOD_PROFILE + "feedback:\n  decisions: [D-001]\n---\n")
    _write(tmp / "docs/prints/2026-01-02-bb-1/index.md",
           "---\nrun: 2026-01-02-bb-1\n" + GOOD_PROFILE + "feedback:\n  decisions: ['D-002']\n---\n")
    _write(tmp / "docs/design/plates/bb-1.md", "---\nruns: [2026-01-02-bb-1]\n---\n")
    _write(tmp / "docs/working-model/decisions-log.md",
           "# Log\n\n## D-001 — One\n\nFrom [aa-1](../prints/2026-01-01-aa-1/index.md).\n\n"
           "## D-002 — Two\n\nFrom the [bb-1 plate](../design/plates/bb-1.md).\n")
    return tmp


def _edit(root: Path, rel: str, old: str, new: str) -> None:
    p = root / rel
    p.write_text(p.read_text(encoding="utf-8").replace(old, new, 1), encoding="utf-8")


CASES = [
    ("R1: a named decision the log lacks", "R1",
     ("docs/prints/2026-01-01-aa-1/index.md", "[D-001]", "[D-001, D-009]")),
    ("R1: the decision links neither record nor plate page", "R1",
     ("docs/working-model/decisions-log.md", "../design/plates/bb-1.md", "elsewhere.md")),
    ("R2: a decision cites a record that does not name it (the by-design failure)", "R2",
     ("docs/prints/2026-01-01-aa-1/index.md", "[D-001]", "[]")),
    ("R3: a record naming a decision has a blank setup field", "R3",
     ("docs/prints/2026-01-01-aa-1/index.md", "layer_mm: 0.2", "layer_mm: ~")),
]


def self_test() -> int:
    bad = 0
    with tempfile.TemporaryDirectory() as t:
        errs = check(_fixture(Path(t)))
        print(f"{'ok ' if not errs else 'BAD'} clean fixture passes {errs or ''}")
        bad += bool(errs)
    for label, rule, (rel, old, new) in CASES:
        with tempfile.TemporaryDirectory() as t:
            root = _fixture(Path(t))
            _edit(root, rel, old, new)
            caught = any(e.startswith(rule) for e in check(root))
            print(f"{'ok ' if caught else 'BAD'} {label}")
            bad += not caught
    print("self-test passed" if not bad else f"self-test FAILED ({bad})")
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    errs = check(ROOT)
    for e in errs:
        print(e)
    print(f"decision evidence: {len(errs)} problem(s)" if errs else "decision evidence: ok")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
