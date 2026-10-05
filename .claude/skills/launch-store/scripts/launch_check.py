#!/usr/bin/env python3
"""launch_check.py — the store's pre-launch checklist, checked and counted.

The checklist (`.claude/skills/launch-store/checklist.md`) is kept by hand, and a hand-kept
tick list drifts: the storefront design's own tick list said calls 2, 3 and 5 to 10 were open a
day after Omar decided all of them. This catches that, and the form:

- every item names who does it (`*Who:* <owner>.`, from a known list) and where it is tracked
  (`*Tracked:* [where](link)`, a link that resolves, heading included);
- a line that starts "Call N:" is ticked exactly when the call its link points at has a
  `**Decided` line under its heading, and that heading is call N;
- every D-id the list names is in the decisions log.

It cannot check that a ticked work item is really done; that is what the PR or date on the line
is for.

    python3 .claude/skills/launch-store/scripts/launch_check.py            # check + counts
    python3 .claude/skills/launch-store/scripts/launch_check.py --ticks <doc.md>
    python3 .claude/skills/launch-store/scripts/launch_check.py --self-test

`--ticks` runs only the call rule, on any doc with a tick list of calls (the storefront design's
§16.5 is the first).
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

SKILL = Path(__file__).resolve().parent.parent
ROOT = SKILL.parent.parent.parent
CHECKLIST = SKILL / "checklist.md"
DECISIONS = ROOT / "docs" / "working-model" / "decisions-log.md"

sys.path.insert(0, str(ROOT / ".claude" / "gates"))
from docs_gate import BLOCK_ID, FENCE, HEADING_TEXT, github_slug  # noqa: E402

OWNERS = ("Omar", "3d-models", "bikar", "coffee-house-storefront", "hub")

ITEM = re.compile(r"^- \[( |x)\] (.*)$")
WHO = re.compile(r"\*Who:\*\s*([^.*]+?)\.")
TRACKED = re.compile(r"\*Tracked:\*\s*\[[^\]]*\]\(([^)\s]+)\)")
CALL = re.compile(r"^(?:\[)?Call (\d+)\b")
LINK = re.compile(r"\]\(([^)\s]+)\)")
D_ID = re.compile(r"\bD-(\d{3})\b")
HEADING_LEVEL = re.compile(r"^(#{1,6})\s")


def items(path: Path) -> list[tuple[int, bool, str]]:
    """(line number, ticked, text) for each tick-box line outside code fences."""
    out, fence = [], False
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            fence = not fence
            continue
        m = None if fence else ITEM.match(line)
        if m:
            out.append((n, m.group(1) == "x", m.group(2)))
    return out


def split_link(doc: Path, link: str) -> tuple[Path, str]:
    target, _, frag = link.partition("#")
    return ((doc.parent / target).resolve() if target else doc.resolve()), unquote(frag)


def section(target: Path, frag: str) -> tuple[str, list[str]] | None:
    """The heading a `#fragment` names and the lines under it, up to the next heading of the
    same or a higher level. A `^id` on a body line belongs to the heading above it."""
    lines = target.read_text(encoding="utf-8").splitlines()
    heads: list[tuple[int, int, str]] = []
    seen: Counter[str] = Counter()
    hit = None
    fence = False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            fence = not fence
            continue
        if fence:
            continue
        m = HEADING_TEXT.match(line)
        if m:
            text = m.group(1)
            level = len(HEADING_LEVEL.match(line).group(1))
            heads.append((i, level, text))
            slug = github_slug(text)
            names = {slug if not seen[slug] else f"{slug}-{seen[slug]}", text.strip().casefold()}
            seen[slug] += 1
            if frag in names or frag.casefold() in names:
                hit = len(heads) - 1
        b = BLOCK_ID.search(line)
        if b and frag == "^" + b.group(1) and heads:
            hit = len(heads) - 1
    if hit is None:
        return None
    start, level, text = heads[hit]
    end = next((h[0] for h in heads[hit + 1:] if h[1] <= level), len(lines))
    return BLOCK_ID.sub("", text).strip(), lines[start + 1:end]


def is_decided(body: list[str]) -> bool:
    return any(line.startswith("**Decided") for line in body)


def check_call(doc: Path, n: int, ticked: bool, text: str) -> str | None:
    """One call line against its call's own heading."""
    call = CALL.match(text)
    links = LINK.findall(text)
    framed = [x for x in links if "#" in x]
    if not framed:
        return f"call {call.group(1)} has no link to its call's heading, so its tick cannot be checked"
    target, frag = split_link(doc, framed[0])
    if not target.exists():
        return f"call {call.group(1)}: {framed[0]} does not exist"
    found = section(target, frag)
    if found is None:
        return f"call {call.group(1)}: no heading for #{frag} in {target.name}"
    heading, body = found
    if not re.match(rf"^(?:Call )?{call.group(1)}\b", heading):
        return f"call {call.group(1)} links to a different call's heading: \"{heading}\""
    decided = is_decided(body)
    if ticked and not decided:
        return f"call {call.group(1)} is ticked, but \"{heading}\" has no Decided line"
    if decided and not ticked:
        return f"call {call.group(1)} is open, but \"{heading}\" says Decided"
    return None


def check_ticks(doc: Path) -> list[str]:
    errs = []
    for n, ticked, text in items(doc):
        if CALL.match(text):
            err = check_call(doc, n, ticked, text)
            if err:
                errs.append(f"{doc.name}:{n}: {err}")
    return errs


def decision_ids(log: Path) -> set[str]:
    return set(re.findall(r"^## D-(\d{3})\b", log.read_text(encoding="utf-8"), re.M))


def check_checklist(path: Path, log: Path) -> tuple[list[str], dict]:
    errs = check_ticks(path)
    known = decision_ids(log)
    owners: Counter[str] = Counter()
    done = 0
    rows = items(path)
    for n, ticked, text in rows:
        where = f"{path.name}:{n}"
        who = WHO.search(text)
        if not who:
            errs.append(f"{where}: no *Who:* owner")
        elif who.group(1).strip() not in OWNERS:
            errs.append(f"{where}: owner \"{who.group(1).strip()}\" is not one of {', '.join(OWNERS)}")
        tracked = TRACKED.search(text)
        if not tracked:
            errs.append(f"{where}: no *Tracked:* link")
        else:
            target, frag = split_link(path, tracked.group(1))
            if not target.exists():
                errs.append(f"{where}: tracked at {tracked.group(1)}, which does not exist")
            elif frag and section(target, frag) is None:
                errs.append(f"{where}: no heading for #{frag} in {target.name}")
        for d in D_ID.findall(text):
            if d not in known:
                errs.append(f"{where}: D-{d} is not in the decisions log")
        if ticked:
            done += 1
        elif who:
            owners[who.group(1).strip()] += 1
    return errs, {"items": len(rows), "done": done, "open": len(rows) - done, "owners": owners}


def report(stats: dict) -> str:
    by = ", ".join(f"{o} {c}" for o, c in stats["owners"].most_common())
    return f"{stats['items']} items: {stats['done']} done, {stats['open']} open ({by or 'none'})"


# ---------------------------------------------------------------- self-test

CALLS_PAGE = """# Open calls

## Store

### 12. Where the orders live

Options.

### 13. How the price is set ^ab12cd

**Decided 2026-10-05:** cost-plus → D-001

### 14. Something else

Text ^ef34gh

**Decided 2026-10-05:** yes

#### 14a. A sub-heading under 14

### 15. Open, but a later call is decided

## Next

**Decided 2026-10-05:** belongs to no call
"""

LOG = "# Decisions\n\n## D-001 — one\n\n## D-002 — two\n"

GOOD = """# List

- [ ] Call 12: where. *Who:* Omar. *Tracked:* [calls](calls.md#12-where-the-orders-live).
- [x] Call 13: price (D-001). *Who:* Omar. *Tracked:* [calls](calls.md#^ab12cd).
- [x] Call 14: else. *Who:* Omar. *Tracked:* [calls](calls.md#^ef34gh).
- [ ] Call 15: open. *Who:* Omar. *Tracked:* [calls](calls.md#15-open-but-a-later-call-is-decided).
- [ ] A thing to build (D-002). *Who:* bikar. *Tracked:* [calls](calls.md).
- [x] A thing built. *Who:* 3d-models. *Tracked:* [calls](calls.md#store).

```
- [ ] Call 99: inside a fence, not an item.
```
"""

BAD = {
    "a call ticked with no Decided line": (
        "- [x] Call 12: where. *Who:* Omar. *Tracked:* [c](calls.md#12-where-the-orders-live).",
        "ticked, but"),
    "a decided call left open (the §16.5 drift)": (
        "- [ ] Call 13: price. *Who:* Omar. *Tracked:* [c](calls.md#^ab12cd).",
        "is open, but"),
    "a call linked to another call's heading": (
        "- [ ] Call 16: x. *Who:* Omar. *Tracked:* [c](calls.md#12-where-the-orders-live).",
        "different call's heading"),
    "a call with no heading link": (
        "- [ ] Call 12: where. *Who:* Omar. *Tracked:* [c](calls.md).",
        "no link to its call's heading"),
    "a heading that does not exist": (
        "- [ ] Call 12: where. *Who:* Omar. *Tracked:* [c](calls.md#12-gone).",
        "no heading for"),
    "no owner": ("- [ ] A thing. *Tracked:* [c](calls.md).", "no *Who:*"),
    "an unknown owner": ("- [ ] A thing. *Who:* Bob. *Tracked:* [c](calls.md).", "is not one of"),
    "no tracking link": ("- [ ] A thing. *Who:* Omar.", "no *Tracked:*"),
    "a tracking link to a missing file": (
        "- [ ] A thing. *Who:* Omar. *Tracked:* [c](gone.md).", "does not exist"),
    "a D-id the log lacks": ("- [ ] A thing (D-404). *Who:* Omar. *Tracked:* [c](calls.md).",
                             "D-404 is not in"),
}


def self_test() -> int:
    fails = []
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "calls.md").write_text(CALLS_PAGE)
        log = d / "log.md"
        log.write_text(LOG)
        good = d / "good.md"
        good.write_text(GOOD)
        errs, stats = check_checklist(good, log)
        if errs:
            fails.append(f"the good list failed: {errs}")
        if (stats["items"], stats["done"], stats["owners"]) != (6, 3, Counter(Omar=2, bikar=1)):
            fails.append(f"counts wrong: {stats}")
        sub = section(d / "calls.md", "14-something-else")
        if sub is None or not is_decided(sub[1]):
            fails.append("a sub-heading cut call 14's section short or lost its Decided line")
        if section(d / "calls.md", "15-open-but-a-later-call-is-decided") and is_decided(
                section(d / "calls.md", "15-open-but-a-later-call-is-decided")[1]):
            fails.append("call 15 read a Decided line from past its section")
        for name, (line, want) in BAD.items():
            bad = d / "bad.md"
            bad.write_text(f"# List\n\n{line}\n")
            errs, _ = check_checklist(bad, log)
            if not any(want in e for e in errs):
                fails.append(f"{name}: expected \"{want}\", got {errs}")
    for f in fails:
        print(f"FAIL {f}")
    print(f"launch_check self-test: {len(BAD) + 4 - len(fails)} of {len(BAD) + 4} cases pass")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--ticks", type=Path, help="check only the call ticks of this doc")
    ap.add_argument("--checklist", type=Path, default=CHECKLIST)
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.ticks:
        errs = check_ticks(args.ticks)
        for e in errs:
            print(e)
        print(f"{args.ticks.name}: {'ticks match their calls' if not errs else f'{len(errs)} wrong'}")
        return 1 if errs else 0
    errs, stats = check_checklist(args.checklist, DECISIONS)
    for e in errs:
        print(e)
    print(report(stats))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
