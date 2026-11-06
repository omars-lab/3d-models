#!/usr/bin/env python3
"""The print evidence log: decisions, issues, assumptions and risks, each linked to the print
it came from.

`docs/prints/evidence-log.md` is written by this script and never by hand. Every line comes
from a record already kept:

  Decisions    the D- ids each print record names in `feedback.decisions`, with the record,
               its plate page and the date. `.claude/gates/decision_evidence.py` holds the
               two-way link, so this list and the decisions log cannot disagree.
  Issues       the `docs/issues/*.md` write-ups that print records link.
  Assumptions  the calibration bets (`CAL-*`) that print records name, with their state from
               `.claude/skills/calibrate/bets.md`. Chosen over each plate's "what we expect"
               column because a bet has a kept state (open, provisional, earned), and an
               expectation has none until the plate is judged.
  Risks        plates printed and finished but not judged yet (`after_print.py waiting`), with
               the questions still open on each. Grams are left out: they come from the local
               slice under `build/`, which is not checked in, so the page would differ by machine.

  check:      python3 .claude/skills/review-print/scripts/evidence_log.py
  rewrite:    python3 .claude/skills/review-print/scripts/evidence_log.py --write
  self-test:  python3 .claude/skills/review-print/scripts/evidence_log.py --self-test
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / ".claude" / "gates"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import after_print as ap  # noqa: E402
from decision_evidence import (decision_sections, load_records, named_decisions,  # noqa: E402
                               plate_of_run)
from docs_gate import github_slug  # noqa: E402

PAGE = Path("docs/prints/evidence-log.md")
ISSUE_LINK = re.compile(r"issues/([a-z0-9-]+)\.md")
BET = re.compile(r"\bCAL-[A-Z]{3}-\d{2}\b")
BETS = Path(".claude/skills/calibrate/bets.md")

HEAD = """---
title: Print evidence log
---

# Print evidence log

What the prints have taught us, each line linked to the print that shows it. This page is
written by `.claude/skills/review-print/scripts/evidence_log.py` from the print records, the
decisions log, the issue write-ups, the calibration bets and the plate pages. Do not edit it by
hand: change the record, then run the script with `--write`.
"""


def _record_text(root: Path, run: str) -> str:
    return (root / "docs" / "prints" / run / "index.md").read_text(encoding="utf-8")


def _plate_link(root: Path, plates: dict[str, str], run: str) -> str:
    stem = plates.get(run)
    if stem and (root / "docs" / "design" / "plates" / f"{stem}.md").exists():
        return f"[{stem}](../design/plates/{stem}.md)"
    return "no plate page"


def decisions(root: Path, records: dict[str, dict]) -> list[str]:
    log = root / "docs" / "working-model" / "decisions-log.md"
    sections = decision_sections(log.read_text(encoding="utf-8"))
    plates = plate_of_run(root / "docs" / "design" / "plates")
    rows = []
    for run, fm in sorted(records.items()):
        for did in named_decisions(fm):
            title = sections.get(did, ("not in the decisions log", ""))[0]
            link = (f"[{did}](../working-model/decisions-log.md#{github_slug(f'{did} — {title}')})"
                    if did in sections else did)
            rows.append(f"| {link} | {title} | [{run}]({run}/index.md) | "
                        f"{_plate_link(root, plates, run)} | {run[:10]} |")
    out = ["## Decisions", "",
           "Each decision a print led to, from the record's `feedback.decisions`. The full "
           "reasoning is in the [decisions log](../working-model/decisions-log.md).", ""]
    if not rows:
        return out + ["No print record names a decision yet.", ""]
    return out + ["| Decision | What it says | Print record | Plate page | Printed |",
                  "|---|---|---|---|---|", *rows, ""]


def _issue_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def issues(root: Path, records: dict[str, dict]) -> list[str]:
    by_issue: dict[str, list[str]] = {}
    for run in sorted(records):
        for slug in sorted(set(ISSUE_LINK.findall(_record_text(root, run)))):
            by_issue.setdefault(slug, []).append(run)
    out = ["## Issues", "", "Write-ups in `docs/issues/` that a print record links: a print "
           "that went wrong and changed how we work.", ""]
    rows = []
    for slug, runs in sorted(by_issue.items()):
        path = root / "docs" / "issues" / f"{slug}.md"
        name = f"[{_issue_title(path)}](../issues/{slug}.md)" if path.exists() else f"{slug} (missing)"
        rows.append(f"| {name} | {', '.join(f'[{r}]({r}/index.md)' for r in runs)} |")
    if not rows:
        return out + ["No print record links an issue write-up yet.", ""]
    return out + ["| Issue | Print records that link it |", "|---|---|", *rows, ""]


def bet_states(root: Path) -> dict[str, tuple[str, str]]:
    """bet id -> (what it is about, its state), from the Bets table in bets.md."""
    out: dict[str, tuple[str, str]] = {}
    for line in (root / BETS).read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in ap.PIPE.split(line.strip().strip("|"))]
        if len(cells) >= 4 and BET.fullmatch(cells[0].strip("`")):
            out.setdefault(cells[0].strip("`"), (cells[1], cells[3]))
    return out


def assumptions(root: Path, records: dict[str, dict]) -> list[str]:
    by_bet: dict[str, list[str]] = {}
    for run in sorted(records):
        for bet in sorted(set(BET.findall(_record_text(root, run)))):
            by_bet.setdefault(bet, []).append(run)
    states = bet_states(root)
    out = ["## Assumptions", "", "Calibration bets a print record names: a number we print by "
           "before a print has settled it. The state comes from `" + str(BETS) + "`.", ""]
    rows = []
    for bet, runs in sorted(by_bet.items()):
        what, state = states.get(bet, ("not in the bets table", "unknown"))
        rows.append(f"| {bet} | {what} | {state} | {', '.join(f'[{r}]({r}/index.md)' for r in runs)} |")
    if not rows:
        return out + ["No print record names a calibration bet yet.", ""]
    return out + ["| Bet | What it is about | State | Print records |", "|---|---|---|---|", *rows, ""]


def _open_rows(plate: str, plates: Path) -> list[str]:
    rows, _ = ap.rows_of(plate, plates)
    _, _, _, body = ap.read_page(plate, plates)
    done = ap.latest(ap.judged(body))
    return [f"  - Row {r['row']}: {' '.join(r['look_for'].split()) or ' '.join(r['question'].split())}"
            for r in rows if done.get(r["row"], {}).get("answer", ap.NOT_JUDGED) == ap.NOT_JUDGED]


def risks(root: Path) -> list[str]:
    plates = root / "docs" / "design" / "plates"
    out = ["## Risks", "", "Plates printed and finished but not judged yet. Until they are, what "
           "they test is still a guess, and the longer they wait the more a later plate may "
           "replace them.", ""]
    waiting = ap.waiting(plates, root / "docs" / "prints")
    if not waiting:
        return out + ["Every finished plate has been judged.", ""]
    for w in waiting:
        out.append(f"- [{w['title'] or w['plate']}](../design/plates/{w['plate']}.md): "
                   f"{w['answered']} of {w['rows']} questions answered. Still open:")
        out += _open_rows(w["plate"], plates)
    return out + [""]


def render(root: Path) -> str:
    records = load_records(root / "docs" / "prints")
    parts = [HEAD.rstrip("\n"), ""]
    for section in (decisions(root, records), issues(root, records),
                    assumptions(root, records), risks(root)):
        parts += section
    return "\n".join(parts).rstrip("\n") + "\n"


def check(root: Path, page: Path) -> list[str]:
    if not page.exists():
        return [f"{PAGE} is missing; run evidence_log.py --write"]
    if page.read_text(encoding="utf-8") != render(root):
        return [f"{PAGE} is behind the records; run evidence_log.py --write"]
    return []


def self_test() -> int:
    """The rendered page passes; the same page one line stale is caught (the by-design failure)."""
    bad = 0
    with tempfile.TemporaryDirectory() as t:
        page = Path(t) / "evidence-log.md"
        page.write_text(render(ROOT), encoding="utf-8")
        ok = not check(ROOT, page)
        print(f"{'ok ' if ok else 'BAD'} a freshly written page passes")
        bad += not ok
        page.write_text(page.read_text(encoding="utf-8").replace("| [D-", "| [D-9", 1), encoding="utf-8")
        caught = bool(check(ROOT, page))
        print(f"{'ok ' if caught else 'BAD'} a hand-edited decision row is caught")
        bad += not caught
        page.unlink()
        caught = bool(check(ROOT, page))
        print(f"{'ok ' if caught else 'BAD'} a missing page is caught")
        bad += not caught
    for name, fn in (("decisions", decisions), ("issues", issues), ("assumptions", assumptions)):
        has = any(line.startswith("| [") or line.startswith("| CAL-")
                  for line in fn(ROOT, load_records(ROOT / "docs" / "prints")))
        print(f"{'ok ' if has else 'BAD'} the {name} section has rows on the real tree")
        bad += not has
    print("self-test passed" if not bad else f"self-test FAILED ({bad})")
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    page = ROOT / PAGE
    if "--write" in argv:
        page.write_text(render(ROOT), encoding="utf-8")
        print(f"wrote {PAGE}")
        return 0
    findings = check(ROOT, page)
    for f in findings:
        print(f"evidence-log: {f}", file=sys.stderr)
    if findings:
        return 1
    print("evidence log: current")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
