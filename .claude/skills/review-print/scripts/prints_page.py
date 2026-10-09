#!/usr/bin/env python3
"""The Prints page's records and lessons, written from the print records.

`docs/prints.md` lists every print under `docs/prints/<run>/`: the plate it was, what it
tested, what happened and why, what it changed, and its pictures. Below that, one line per
lesson across all the prints. Both blocks are written by this script and never by hand: the
hand-written list stopped at two records while six more shipped, so the page now cannot fall
behind the records any more than the plates queue can fall behind the plate pages.

Each record's `feedback` block gives the words: `lesson` (one line, for the roll-up),
`symptom`, `cause`, `next`, and `decisions` (the D- ids the print led to). The plate page is
the one whose `runs:` names the record. A record with no photo of the real print says so, and
links the plate page's rendered pictures instead.

  check:      python3 .claude/skills/review-print/scripts/prints_page.py
  rewrite:    python3 .claude/skills/review-print/scripts/prints_page.py --write
  self-test:  python3 .claude/skills/review-print/scripts/prints_page.py --self-test
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

import yaml


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / ".claude" / "gates" / "prints_gate.py").exists():
            return p
    raise SystemExit("prints-page: cannot find the repo root above " + str(here))


ROOT = _repo_root()
sys.path.insert(0, str(ROOT / ".claude" / "gates"))
from docs_gate import github_slug  # noqa: E402
from prints_gate import parse_frontmatter, record_dirs  # noqa: E402

R_START, R_END = "<!-- records:start -->", "<!-- records:end -->"
L_START, L_END = "<!-- lessons:start -->", "<!-- lessons:end -->"
WRITER = "python3 .claude/skills/review-print/scripts/prints_page.py --write"
DECISION_HEAD = re.compile(r"^## (D-\d{3}) — (.+?)\s*$")
VERDICTS = ("keep", "adjust", "drop", "not-judged")


def decision_titles(log: Path) -> dict[str, str]:
    if not log.exists():
        return {}
    out: dict[str, str] = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        m = DECISION_HEAD.match(line)
        if m:
            out.setdefault(m.group(1), m.group(2))
    return out


def plate_pages(plates: Path) -> dict[str, tuple[Path, list[str]]]:
    """run -> (plate page, its pictures), from each page's `runs:` list."""
    out: dict[str, tuple[Path, list[str]]] = {}
    for page in sorted(plates.glob("*.md")):
        fm, _ = parse_frontmatter(page.read_text(encoding="utf-8"))
        if not isinstance(fm, dict):
            continue
        pics = [p for p in (fm.get("pictures") or []) if isinstance(p, str)]
        for run in fm.get("runs") or []:
            out.setdefault(str(run), (page, pics))
    return out


def _one_line(text) -> str:
    return " ".join(str(text).split()) if text not in (None, "") else ""


def _sentence(text: str) -> str:
    text = text[:1].upper() + text[1:]
    return text if text.endswith((".", "?", "!")) else text + "."


def read_records(prints: Path) -> tuple[list[dict], list[str]]:
    recs, findings = [], []
    for d in record_dirs(prints):
        fm, err = parse_frontmatter((d / "index.md").read_text(encoding="utf-8"))
        if fm is None:
            findings.append(f"{d.name}: {err}")
            continue
        fm["_dir"] = d
        recs.append(fm)
    recs.sort(key=lambda r: r["_dir"].name, reverse=True)
    return recs, findings


def render(root: Path) -> tuple[str, str, list[str]]:
    """(records block, lessons block, findings) for the page at root/docs/prints.md."""
    docs = root / "docs"
    recs, findings = read_records(docs / "prints")
    pages = plate_pages(docs / "design" / "plates")
    titles = decision_titles(docs / "working-model" / "decisions-log.md")

    rec_lines = [R_START, "", f"Written by `{WRITER}` from the records; newest first.", ""]
    lesson_lines = [L_START, "", f"One line per print, written by `{WRITER}` from each record's "
                    "`feedback.lesson`.", ""]
    measured = 0
    for r in recs:
        run = r["_dir"].name
        link = f"prints/{run}/index.md"
        fb = r.get("feedback") if isinstance(r.get("feedback"), dict) else {}
        plate = _one_line(r.get("plate"))
        name, _, tested = plate.partition(" — ")
        if r.get("readings"):
            measured += 1
        rec_lines.append(f"### [{run}]({link})")
        rec_lines.append("")
        page = pages.get(run)
        if page:
            rel = page[0].relative_to(docs).as_posix()
            rec_lines.append(f"- **Plate:** [{name}]({rel}) — {tested or plate}")
        else:
            rec_lines.append(f"- **Plate:** {plate} (no plate page names this run)")
        objs = [o for o in (r.get("objects") or []) if isinstance(o, dict)]
        counts = {v: sum(1 for o in objs if o.get("verdict") == v) for v in VERDICTS}
        tally = ", ".join(f"{n} {v}" for v, n in counts.items() if n)
        rec_lines.append(f"- **Pieces:** {len(objs)} ({tally or 'none judged'})")
        for key, label in (("symptom", "What happened"), ("cause", "Why"), ("next", "What it changed")):
            text = _one_line(fb.get(key))
            if text:
                rec_lines.append(f"- **{label}:** {_sentence(text)}")
        ids = [str(i) for i in (fb.get("decisions") or [])]
        if ids:
            parts = []
            for i in ids:
                if i not in titles:
                    findings.append(f"{run}: feedback.decisions names {i}, which the decisions log does not have")
                    parts.append(i)
                    continue
                anchor = github_slug(f"{i} — {titles[i]}")
                parts.append(f"[{i}](working-model/decisions-log.md#{anchor}) ({titles[i]})")
            rec_lines.append(f"- **Decided from it:** {'; '.join(parts)}")
        photos = [p for p in (r.get("photos") or []) if isinstance(p, dict) and p.get("file")]
        shown = None  # the one picture drawn inline, so the page shows what printed at a glance
        if photos:
            shots = ", ".join(f"[{_one_line(p.get('of')) or p['file']}](prints/{run}/{p['file']})"
                              for p in photos)
            rec_lines.append(f"- **Photos of the print:** {shots}")
            shown = (f"photo: {_one_line(photos[0].get('of')) or run}", f"prints/{run}/{photos[0]['file']}")
        else:
            pics = page[1] if page else []
            base = page[0].parent.relative_to(docs).as_posix() if page else ""
            # A plate page can show the print's own photo (minis-03 does); a record without
            # photos only has renders, so name what each link is.
            renders = [p for p in pics if "/prints/" not in p]
            if renders:
                shots = ", ".join(f"[{Path(p).stem}]({base}/{p})" for p in renders)
                rec_lines.append(f"- **Photos of the print:** none. Rendered pictures from the plate page: {shots}")
                shown = (f"render, not a photo: {Path(renders[0]).stem}", f"{base}/{renders[0]}")
            else:
                rec_lines.append("- **Photos of the print:** none, and the plate page has no rendered pictures.")
        if shown:
            rec_lines += ["", f"![{shown[0]}]({shown[1]})"]
        rec_lines.append("")
        lesson = _one_line(fb.get("lesson"))
        if lesson:
            lesson_lines.append(f"- {_sentence(lesson)} ([{run}]({link}))")
        else:
            lesson_lines.append(f"- No lesson written yet. ([{run}]({link}))")
    if recs:
        rec_lines.append(f"{len(recs)} records; {measured} measured with a tool, so "
                         f"{'no bet has moved yet' if not measured else 'see each record for the bet it moved'}.")
    else:
        rec_lines.append("Nothing has printed yet.")
    rec_lines += ["", R_END]
    lesson_lines += ["", L_END]
    return "\n".join(rec_lines), "\n".join(lesson_lines), findings


def _block(text: str, start: str, end: str) -> str | None:
    a, b = text.find(start), text.find(end)
    return text[a:b + len(end)] if a != -1 and b != -1 else None


def _replace(text: str, start: str, end: str, block: str) -> str:
    a, b = text.find(start), text.find(end)
    return text[:a] + block + text[b + len(end):]


def check(root: Path) -> list[str]:
    page = root / "docs" / "prints.md"
    records, lessons, findings = render(root)
    text = page.read_text(encoding="utf-8")
    for start, end, want, what in ((R_START, R_END, records, "records"), (L_START, L_END, lessons, "lessons")):
        have = _block(text, start, end)
        if have is None:
            findings.append(f"prints.md has no {start} … {end} block")
        elif have != want:
            findings.append(f"prints.md: the {what} block is not what the records give — run `{WRITER}`")
    return findings


def write(root: Path) -> int:
    page = root / "docs" / "prints.md"
    records, lessons, findings = render(root)
    if findings:
        for f in findings:
            print(f"prints-page: {f}", file=sys.stderr)
        return 1
    text = page.read_text(encoding="utf-8")
    for start, end in ((R_START, R_END), (L_START, L_END)):
        if _block(text, start, end) is None:
            print(f"prints-page: {page} has no {start} … {end} block", file=sys.stderr)
            return 1
    text = _replace(text, R_START, R_END, records)
    text = _replace(text, L_START, L_END, lessons)
    page.write_text(text, encoding="utf-8")
    print(f"prints page written: {page}")
    return 0


# ---------------------------------------------------------------- self-test

def _fixture(tmp: Path, *, photo: bool, decision: str) -> Path:
    root = tmp / "repo"
    (root / "docs" / "prints" / "2026-01-02-pl-1").mkdir(parents=True)
    (root / "docs" / "design" / "plates" / "pl-1-media").mkdir(parents=True)
    (root / "docs" / "working-model").mkdir(parents=True)
    (root / "docs" / "working-model" / "decisions-log.md").write_text(
        "# Decisions\n\n## D-001 — The first call\n\nText.\n", encoding="utf-8")
    (root / "docs" / "design" / "plates" / "pl-1.md").write_text(
        "---\nplate: pl-1\nruns: [2026-01-02-pl-1]\npictures:\n  - pl-1-media/bed.png\n---\n\n# pl-1\n",
        encoding="utf-8")
    fm = {
        "run": "2026-01-02-pl-1", "plate": "pl-1 — a test plate", "status": "printed",
        "objects": [{"entry": "a", "verdict": "keep"}, {"entry": "b", "verdict": "drop"}],
        "readings": [],
        "photos": [{"file": "photos/top.jpg", "of": "the plate from above"}] if photo else [],
        "feedback": {"lesson": "Gap 0.2 fits", "symptom": "b was loose", "cause": "too much gap",
                     "next": "print b tighter", "decisions": [decision]},
    }
    (root / "docs" / "prints" / "2026-01-02-pl-1" / "index.md").write_text(
        "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n\nAccount.\n",
        encoding="utf-8")
    (root / "docs" / "prints.md").write_text(
        f"# Prints\n\n{R_START}\n{R_END}\n\n## Lessons\n\n{L_START}\n{L_END}\n", encoding="utf-8")
    return root


def self_test() -> int:
    fails = 0

    def report(ok: bool, what: str, detail: str = "") -> None:
        nonlocal fails
        print(f"  {'PASS' if ok else 'FAIL'}: {what}" + (f" — {detail}" if not ok and detail else ""))
        fails += 0 if ok else 1

    with tempfile.TemporaryDirectory() as t:
        root = _fixture(Path(t), photo=False, decision="D-001")
        report(any("records block is not" in f for f in check(root)),
               "a record the page does not list fails the check")
        report(write(root) == 0 and check(root) == [], "after --write the check passes")
        text = (root / "docs" / "prints.md").read_text(encoding="utf-8")
        report("[pl-1](design/plates/pl-1.md) — a test plate" in text, "the record links its plate page")
        report("**Photos of the print:** none. Rendered pictures from the plate page: "
               "[bed](design/plates/pl-1-media/bed.png)" in text,
               "a record with no photo says so and links the plate page's renders", text)
        report("![render, not a photo: bed](design/plates/pl-1-media/bed.png)" in text,
               "the render drawn inline is labeled as a render, not a photo", text)
        report("[D-001](working-model/decisions-log.md#d-001--the-first-call)" in text,
               "a decision links to its heading in the log", text)
        report("- Gap 0.2 fits. ([2026-01-02-pl-1](prints/2026-01-02-pl-1/index.md))" in text,
               "the lesson rolls up with a link to its record", text)
        report("2 (1 keep, 1 drop)" in text, "the verdicts are counted")
    with tempfile.TemporaryDirectory() as t:
        root = _fixture(Path(t), photo=True, decision="D-001")
        write(root)
        text = (root / "docs" / "prints.md").read_text(encoding="utf-8")
        report("[the plate from above](prints/2026-01-02-pl-1/photos/top.jpg)" in text,
               "a record's own photos are linked in place of renders", text)
    with tempfile.TemporaryDirectory() as t:
        root = _fixture(Path(t), photo=False, decision="D-999")
        report(write(root) == 1 and any("D-999" in f for f in check(root)),
               "a decision the log does not have is refused")
    print("prints-page self-test: " + ("OK" if not fails else f"{fails} failure(s)"))
    return 1 if fails else 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    if "--write" in argv:
        return write(ROOT)
    findings = check(ROOT)
    for f in findings:
        print(f"prints-page: {f}", file=sys.stderr)
    if findings:
        return 1
    print("prints page: records and lessons current")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
