#!/usr/bin/env python3
"""Design-doc gate for 3d-models.

Three rules, each derived from a failure kind measured across the seven
grounding audits in docs/research/. See docs/grounding-defect-taxonomy.md for
the definitions and the instances each rule is built from.

  D1 (K9)  Every relative markdown link resolves on disk.
  D2 (K6)  Every `**Validator:**` declaration ships an asserted PASS and an
           asserted FAIL example in its own section.
  D3 (K4)  Every `**Default:**` declaration carries a citation link or a
           CAL-* bet id.
  D4 (K1)  A number an audit has withdrawn may not be restated as fact. The
           bullet or paragraph that names it must also say so.
  D5 (K9)  A CAL-* bet id that *discharges* a `**Default:**` must be registered
           in .claude/skills/calibrate/bets.md.

D1 is universal: it applies to every markdown file checked, needs no network,
and has no false positives by construction — the target either exists on disk
or it does not.

D2 and D3 are **marker-scoped**: they check that the discipline, once entered,
is completed. A doc that declares no validators and no defaults passes them
silently. That is a real limit and it is stated in the taxonomy doc: this gate
catches an incomplete discipline, not an absent one. It is the same trade
bikar's check-doc-pointers.ts makes, and it is deliberate — a gate that fires
on prose it cannot parse gets switched off, which is worse than no gate.

D4 is **literal-scoped**: it knows one list of exact numbers, each entered by
hand when an audit withdrew it, and it fires nowhere else. It exists because a
withdrawal is a corpus-wide event and was twice treated as a local edit:
"±0.1–0.2 mm printer accuracy" was withdrawn on 2026-07-29, corrected in
lego-lab-design.md and print-validation-design.md, and left standing in
tile-wall-design.md as a load-bearing premise until 2026-08-03. Research files
under docs/research/ are exempt: the convention there is a verbatim body plus an
Errata section, so the withdrawn number is *supposed* to still be in the text —
the errata note is what carries the correction.

D5 is **discharge-scoped**, which is narrower than "every CAL id in the corpus"
and deliberately so. D3 accepts a `**Default:**` that names a bet id *instead*
of a citation, and it never asked whether the bet exists — so on 2026-08-03
`docs/text-emit-design.md` shipped three gate-green defaults resting on
`CAL-TXT-01` and `CAL-TXT-02`, neither of which was registered anywhere. The
doc said so itself, in a blockquote, which is exactly the "defensible argument
that management is occurring" this repo's CLAUDE.md warns about.

The rule was measured before it was written, per the C3 tenet. Across the 225
CAL-id sites in docs/, 20 distinct ids: 17 registered, 3 not. Gating on *every*
site would have fired 4 times on `CAL-SEA-01` — an id `hemisphere-split-design.md`
Appendix B and `backlog.md` name precisely to record that it was **deliberately
not minted**, correct prose that a naive rule would call a defect. Restricted to
the discharge form, the same corpus gives **5 hits, 5 real**: every CAL id
sitting inside a `**Default:**` paragraph is load-bearing, and exactly the two
unregistered ones fire. A CAL id anywhere else — prose, a table, a bullet, an
open question — is a mention and is not checked.

It fails **loud, not open**: an unreadable registry, or one that parses to
implausibly few ids, is reported as a finding on the first default it would
have vouched for. A gate that silently stops checking is worse than one that
never did (`catalog_models.py`).

D4's reach is a floor, and the defect that built it proves the ceiling. That
defect had two sites in one file. D4 catches Appendix A's "FDM ±0.1–0.2 mm"
and does **not** catch §2's "LEGO-class interference (±0.02 mm sensitivity) is
10–20× beyond FDM tolerance", which restates the same withdrawn figure as a
multiple and so contains no literal to match. Run against the pre-fix file the
gate reports one finding, not two. D4 makes the cheapest form of the mistake
un-shippable; it does not certify that a withdrawn number is gone.

Usage:
  docs_gate.py [FILE ...]     check the given files (default: all docs/**/*.md)
  docs_gate.py --staged       check staged markdown files only
  docs_gate.py --self-test    run the PASS/FAIL fixtures and verify the gate
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"

# The generated projection of bikar's CAL_BETS array — the only list of bet ids
# that exists on this side. Generated, never hand-edited, so reading it is
# reading the records themselves rather than a second copy of them.
REGISTRY_REL = ".claude/skills/calibrate/bets.md"
REGISTRY = ROOT / REGISTRY_REL

# Below this, the registry did not parse — a renamed heading, a reformatted
# table, a truncated write. 17 ids were registered when D5 was written, so any
# read returning fewer than five means the reader, not the registry, is wrong.
REGISTRY_MIN_IDS = 5

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^#{1,6}\s")
VALIDATOR = re.compile(r"\*\*Validator:\*\*")
DEFAULT = re.compile(r"\*\*Default:\*\*")
CAL_ID = re.compile(r"\bCAL-[A-Z]{3}-\d{2}\b")
HTTP_LINK = re.compile(r"\]\(https?://")
ASSERT_PASS = re.compile(r"^\s*[-*]?\s*PASS:", re.IGNORECASE)
ASSERT_FAIL = re.compile(r"^\s*[-*]?\s*FAIL:", re.IGNORECASE)

SKIP_SCHEMES = ("http://", "https://", "mailto:", "ftp://", "data:")

BLOCK_START = re.compile(r"^\s*(?:[-*+]\s|\d+\.\s|#{1,6}\s|>)|^\s*$")

# Numbers an adversarial grounding audit withdrew, and what a doc must say if
# it names one anyway. Add a row when an audit withdraws a number; never add a
# row speculatively — every row here is a number that was found restated as
# fact in a doc after the withdrawal.
WITHDRAWN: list[tuple[re.Pattern, str, str]] = [
    (
        re.compile(r"±\s*0\.1\s*[–-]\s*0\.2\s*mm"),
        "±0.1–0.2 mm FDM accuracy",
        "no printer vendor publishes an accuracy figure at all (Bambu X1C and A1 "
        "spec sheets: zero matches; Prusa MK4S: no number). The rebuilt argument "
        "is docs/lego-lab-design.md §3.5",
    ),
    (
        re.compile(r"\b6 of 37\b|\b4 self-intersections\b"),
        "DM Sans's first crossing measurement (6 of 37 glyphs; 4 self-intersections)",
        "a second, independent implementation (bikar:scripts/bake-glyphs.py) "
        "re-derived it on 2026-08-04 as 5 of 37 and 2 self-intersections, stable "
        "across four chord tolerances and two rounding depths: `Y` is a single "
        "9-point straight-line contour and cannot cross, and the self-crossing in "
        "`B` went uncounted. The corrected numbers are "
        "docs/research/outline-font-emit.md §2a",
    ),
]

# A block escapes D4 by saying, in the block itself, that the number is not
# being asserted. Anything vaguer than these words is not a withdrawal.
EXCULPATE = re.compile(r"withdrawn|uncited|corrected|correction", re.IGNORECASE)


def strip_code(lines: list[str]) -> list[str]:
    """Blank out fenced blocks and inline code spans.

    A marker or a link written as code is a *mention*, not a use — this file's
    own fixtures, CLAUDE.md and the taxonomy doc all have to write
    `**Validator:**` and `**Default:**` inline to document the discipline, and
    none of those is a declaration. Line numbers are preserved.
    """
    out, in_fence = [], False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else INLINE_CODE.sub("", line))
    return out


def check_d1_links(path: Path, lines: list[str]) -> list[str]:
    findings = []
    for n, line in enumerate(lines, 1):
        for target in LINK.findall(line):
            if target.startswith(SKIP_SCHEMES) or target.startswith("#"):
                continue
            bare = target.split("#", 1)[0]
            if not bare:
                continue
            resolved = (path.parent / bare).resolve()
            if not resolved.exists():
                findings.append(
                    f"{path.relative_to(ROOT)}:{n}: D1 (K9) link target does not "
                    f"exist: {bare}"
                )
    return findings


def sections(lines: list[str], marker: re.Pattern) -> list[tuple[int, list[str]]]:
    """Slice the file at each marker hit; a section ends at the next heading
    or the next marker hit, whichever comes first."""
    starts = [i for i, line in enumerate(lines) if marker.search(line)]
    out = []
    for i in starts:
        end = len(lines)
        for j in range(i + 1, len(lines)):
            if HEADING.match(lines[j]) or marker.search(lines[j]):
                end = j
                break
        out.append((i + 1, lines[i:end]))
    return out


def check_d2_validators(path: Path, lines: list[str], raw: list[str]) -> list[str]:
    findings = []
    for lineno, body in sections(lines, VALIDATOR):
        missing = []
        if not any(ASSERT_PASS.match(b) for b in body):
            missing.append("PASS:")
        if not any(ASSERT_FAIL.match(b) for b in body):
            missing.append("FAIL:")
        if missing:
            name = raw[lineno - 1].strip()[:80]
            findings.append(
                f"{path.relative_to(ROOT)}:{lineno}: D2 (K6) validator ships no "
                f"{' and no '.join(missing)} example — {name}"
            )
    return findings


def check_d3_defaults(path: Path, lines: list[str], raw: list[str]) -> list[str]:
    findings = []
    for lineno, body in sections(lines, DEFAULT):
        # Provenance may wrap onto continuation lines, so read the whole
        # paragraph — but stop at the blank line, so an unrelated link further
        # down the section cannot vouch for this default.
        para = [body[0]]
        for line in body[1:]:
            if not line.strip():
                break
            para.append(line)
        blob = "\n".join(para)
        if HTTP_LINK.search(blob) or CAL_ID.search(blob):
            continue
        findings.append(
            f"{path.relative_to(ROOT)}:{lineno}: D3 (K4) default carries neither "
            f"a citation link nor a CAL-* bet id — {raw[lineno - 1].strip()[:80]}"
        )
    return findings


def registered_bets() -> tuple[set[str], str | None]:
    """The bet ids `bets.md` registers, and why the read failed if it did.

    Returns `(ids, None)` on a good read and `(set(), reason)` on a bad one.
    The caller turns a reason into a finding rather than into silence: a
    registry this gate could not read must not be reported as a registry in
    which every id was found.
    """
    if not REGISTRY.exists():
        return set(), f"{REGISTRY_REL} does not exist"
    ids = set(CAL_ID.findall(REGISTRY.read_text(errors="replace")))
    if len(ids) < REGISTRY_MIN_IDS:
        return set(), (
            f"{REGISTRY_REL} parsed to only {len(ids)} bet id(s), "
            f"below the {REGISTRY_MIN_IDS} this reader expects — regenerate it with "
            "`cd ../bikar && npm run registry:calibration`"
        )
    return ids, None


def check_d5_registered_bets(path: Path, lines: list[str], raw: list[str]) -> list[str]:
    """A bet id that discharges a default must name a bet that exists.

    Scoped to the paragraph D3 reads, for the reason in the module docstring:
    a CAL id in ordinary prose can legitimately name a bet that was considered
    and declined, and firing on those is how a gate earns being switched off.
    """
    findings = []
    ids, reason = registered_bets()
    for lineno, body in sections(lines, DEFAULT):
        para = [body[0]]
        for line in body[1:]:
            if not line.strip():
                break
            para.append(line)
        cited = CAL_ID.findall("\n".join(para))
        if not cited:
            continue
        if reason is not None:
            findings.append(
                f"{path.relative_to(ROOT)}:{lineno}: D5 (K9) cannot verify "
                f"{', '.join(sorted(set(cited)))} — {reason}"
            )
            break
        for bet in sorted(set(cited)):
            if bet in ids:
                continue
            findings.append(
                f"{path.relative_to(ROOT)}:{lineno}: D5 (K9) default rests on "
                f"{bet}, which is not registered in {REGISTRY_REL} — "
                f"add it to CAL_BETS in bikar and regenerate, or cite a source instead"
            )
    return findings


def block_at(lines: list[str], i: int) -> str:
    """The bullet, list item or paragraph containing line i.

    Bullets in these docs run several lines with no blank line between them,
    so a blank-line paragraph would span a whole list and let one bullet's
    disclaimer vouch for every other bullet's number. The block therefore also
    ends at the next list marker or heading.
    """
    start = i
    while start > 0 and not BLOCK_START.match(lines[start]):
        start -= 1
    end = i + 1
    while end < len(lines) and not BLOCK_START.match(lines[end]):
        end += 1
    return "\n".join(lines[start:end])


def check_d4_withdrawn(path: Path, lines: list[str]) -> list[str]:
    if "research" in path.parts:
        return []
    findings = []
    for pattern, label, why in WITHDRAWN:
        for n, line in enumerate(lines):
            if not pattern.search(line):
                continue
            if EXCULPATE.search(block_at(lines, n)):
                continue
            findings.append(
                f"{path.relative_to(ROOT)}:{n + 1}: D4 (K1) restates a withdrawn "
                f"number as fact: {label} — {why}"
            )
    return findings


def is_print_record(path: Path) -> bool:
    """A print-run record under docs/prints/ carries a bench operator's account
    of what a plate measured — a plate can measure a number a later audit
    withdraws, and the operator's account is the *source*, not a claim to
    ground. So the grounding rules (D2 validators, D3 defaults, D4 withdrawn
    literals, D5 bets) do not apply there; D1 (every link resolves) still does.
    Mirrors how bikar's check-doc-pointers.ts excludes docs/issues/. Keyed on
    the posix path so a tempdir fixture under .../docs/prints/ is caught too.
    Design: docs/prints-tab-design.md §4.2."""
    return "/docs/prints/" in path.as_posix()


def check_file(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8").splitlines()
    lines = strip_code(raw)
    if is_print_record(path):
        return check_d1_links(path, lines)
    return (
        check_d1_links(path, lines)
        + check_d2_validators(path, lines, raw)
        + check_d3_defaults(path, lines, raw)
        + check_d4_withdrawn(path, lines)
        + check_d5_registered_bets(path, lines, raw)
    )


def staged_markdown() -> list[Path]:
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    return [ROOT / p for p in out if p.endswith(".md") and (ROOT / p).exists()]


def self_test() -> int:
    """Every rule ships an asserted-PASS and an asserted-FAIL fixture.

    This gate enforces the K6 rule, so it must satisfy it: a rule that has
    never been shown to fire is a rule nobody has tested.
    """
    expected = {
        "fail/d1-dead-link.md": ["D1 (K9)"],
        "fail/d2-validator-no-examples.md": ["D2 (K6)"],
        "fail/d3-uncited-default.md": ["D3 (K4)"],
        "fail/d4-withdrawn-number.md": ["D4 (K1)"],
        "fail/d4-withdrawn-dm-sans.md": ["D4 (K1)"],
        "fail/d5-unregistered-bet.md": ["D5 (K9)"],
    }
    ok = True
    for name in sorted((FIXTURES / "pass").glob("*.md")):
        findings = check_file(name)
        if findings:
            ok = False
            print(f"self-test FAIL: {name.name} should be clean, got:")
            for f in findings:
                print(f"    {f}")
        else:
            print(f"self-test ok: pass/{name.name} → 0 findings")
    for rel, codes in expected.items():
        path = FIXTURES / rel
        findings = check_file(path)
        blob = " ".join(findings)
        for code in codes:
            if code not in blob:
                ok = False
                print(f"self-test FAIL: {rel} should report {code}, got: {findings}")
                break
        else:
            if len(findings) != 1:
                ok = False
                print(f"self-test FAIL: {rel} should report exactly 1 finding, "
                      f"got {len(findings)}: {findings}")
            else:
                print(f"self-test ok: {rel} → {findings[0].split(': ', 1)[1]}")
    # docs/prints/** exclusion: the D4 fixture (its one link is external, so D1
    # is clean either way) must report its finding under a normal path and
    # nothing under a docs/prints/ path — only D1 runs there. Design §4.2.
    import shutil
    import tempfile
    d4 = (FIXTURES / "fail" / "d4-withdrawn-number.md").read_text(encoding="utf-8")
    # Under ROOT so check_file's relative_to(ROOT) resolves; removed in finally.
    tmp = Path(tempfile.mkdtemp(prefix=".docs-gate-prints-", dir=ROOT))
    try:
        normal = tmp / "docs" / "guide" / "note.md"
        record = tmp / "docs" / "prints" / "2026-09-14-x" / "index.md"
        for p in (normal, record):
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(d4, encoding="utf-8")
        if not check_file(normal):
            ok = False
            print("self-test FAIL: D4 content under a normal path should fire, got nothing")
        else:
            print("self-test ok: docs/guide/note.md → D4 fires (not excluded)")
        if check_file(record):
            ok = False
            print(f"self-test FAIL: docs/prints/ record should skip D2–D5, got: {check_file(record)}")
        else:
            print("self-test ok: docs/prints/.../index.md → grounding rules skipped, D1 only")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    if args.staged:
        targets = staged_markdown()
    elif args.files:
        targets = [p if p.is_absolute() else (ROOT / p) for p in args.files]
    else:
        targets = sorted((ROOT / "docs").rglob("*.md")) + [ROOT / "CLAUDE.md"]

    targets = [p for p in targets if FIXTURES not in p.parents]

    findings = []
    for path in targets:
        findings.extend(check_file(path))

    for f in findings:
        print(f, file=sys.stderr)
    if findings:
        print(
            f"\ndocs-gate: {len(findings)} finding(s) in {len(targets)} file(s). "
            "See docs/grounding-defect-taxonomy.md. Override once with "
            "DOCS_GATE_OK=1 git commit",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
