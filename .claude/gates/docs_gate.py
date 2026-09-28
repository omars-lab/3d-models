#!/usr/bin/env python3
"""Design-doc gate for 3d-models.

Five grounding rules (D1–D5), each derived from a failure kind measured across the seven
grounding audits in docs/research/. See docs/grounding-defect-taxonomy.md for
the definitions and the instances each rule is built from. D6 and D7 are render
rules: they catch markdown that does not render as written — D6 in Obsidian's
editor, D7 on GitHub and in Obsidian alike.

  D1 (K9)  Every relative markdown link resolves on disk, and its `#part`, on
           a link to a markdown file, names a heading or `^block-id` there.
           An `obsidian://` link is checked the same way, through the vault
           mapping in obsidian-vaults.json.
  D2 (K6)  Every `**Validator:**` declaration ships an asserted PASS and an
           asserted FAIL example in its own section.
  D3 (K4)  Every `**Default:**` declaration carries a citation link or a
           CAL-* bet id.
  D4 (K1)  A number an audit has withdrawn may not be restated as fact. The
           bullet or paragraph that names it must also say so.
  D5 (K9)  A CAL-* bet id that *discharges* a `**Default:**` must be registered
           in .claude/skills/calibrate/bets.md.
  D6 (render)  An inline code span opens and closes on one line. Obsidian's
           editor pairs backticks per line, so one wrapped span shows the rest
           of the file as raw text. Not run under .claude/ (not in the vault).
           `--fix-code-spans FILE ...` rewraps without changing what renders.
  D7 (render)  Every table row has as many cells as its header. A pipe splits
           a cell even inside backticks, so a literal one is written \\|.

D1 is universal: it applies to every markdown file checked, needs no network,
and has no false positives by construction for the file part — the target
either exists on disk or it does not. The `#part` depends on a slug rule, so it
accepts both readers of these files: GitHub's slug and Obsidian's heading text.

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
  docs_gate.py [FILE ...]     check the given files (default: every markdown file
                              under docs/ and .claude/, plus CLAUDE.md; .claude/
                              files get the link check D1 only)
  docs_gate.py --staged       check staged markdown files; when the commit renames
                              or deletes a file, also run D1 on every other file,
                              since their links into it are what break
  docs_gate.py --self-test    run the PASS/FAIL fixtures and verify the gate
"""

from __future__ import annotations

import argparse
import os
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


def _primary_root(root: Path) -> Path | None:
    """The primary checkout's root when `root` is a linked git worktree, else None.

    A worktree at `X.worktrees/<branch>` sits one directory deeper than the primary
    clone, so a `../../bikar/...` link that resolves beside the primary lands in
    `X.worktrees/bikar` from here. The gate's verdict must not depend on which
    checkout runs it, so a link that escapes this root is re-tried from the primary.
    GIT_DIR/GIT_WORK_TREE are scrubbed: under a hook they point at the primary and
    would make every checkout answer as the primary.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    try:
        common = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--path-format=absolute", "--git-common-dir"],
            capture_output=True, text=True, check=True, env=env,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    primary = Path(common).resolve().parent
    return None if primary == root.resolve() else primary


def link_resolves(doc: Path, bare: str, root: Path = ROOT) -> bool:
    """True when a relative link target exists — beside this checkout, or, for a
    target that escapes the checkout, beside the primary clone it is a worktree of."""
    if (doc.parent / bare).resolve().exists():
        return True
    root = root.resolve()
    resolved = (doc.parent / bare).resolve()
    if resolved.is_relative_to(root):
        return False
    primary = _primary_root(root)
    if primary is None:
        return False
    try:
        rel = doc.resolve().parent.relative_to(root)
    except ValueError:
        return False
    return (primary / rel / bare).resolve().exists()


HEADING_TEXT = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")
BLOCK_ID = re.compile(r"\s\^([A-Za-z0-9-]+)\s*$")
MD_LINK_TEXT = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def github_slug(heading: str) -> str:
    """GitHub's anchor for a heading: the rendered text, lowercased, with every
    character that is not a letter, digit, space, `-` or `_` dropped, and spaces
    turned into `-`. So `D-050 — the three` becomes `d-050--the-three`: the dash
    goes and both spaces stay."""
    text = MD_LINK_TEXT.sub(r"\1", heading).strip().lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


_ANCHORS: dict[Path, set[str]] = {}


def anchors(target: Path) -> set[str]:
    """Every `#part` a link into `target` may use: each heading's GitHub slug
    (with GitHub's `-1`, `-2` for repeats), the heading text itself (Obsidian's
    form, case-folded), and `^id` for each block id review-md writes."""
    key = target.resolve()
    if key in _ANCHORS:
        return _ANCHORS[key]
    out: set[str] = set()
    seen: dict[str, int] = {}
    in_fence = False
    for line in target.read_text(encoding="utf-8").splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_TEXT.match(line)
        if m:
            slug = github_slug(m.group(1))
            n = seen.get(slug, 0)
            seen[slug] = n + 1
            out.add(slug if n == 0 else f"{slug}-{n}")
            out.add(m.group(1).strip().casefold())
        b = BLOCK_ID.search(line)
        if b:
            out.add("^" + b.group(1))
    _ANCHORS[key] = out
    return out


def fragment_resolves(target: Path, fragment: str) -> bool:
    from urllib.parse import unquote
    frag = unquote(fragment)
    have = anchors(target)
    return frag in have or frag.casefold() in have


VAULTS_FILE = Path(__file__).resolve().parent / "obsidian-vaults.json"
OBSIDIAN_AUTOLINK = re.compile(r"<(obsidian://[^>\s]+)>")


def load_vaults(path: Path = VAULTS_FILE) -> list[dict]:
    import json
    return json.loads(path.read_text(encoding="utf-8"))["vaults"]


def _vault_file(root: Path, vault: dict, rel: str) -> Path | None:
    """The file `rel` names inside a vault, in this checkout. Obsidian lets a
    link leave off `.md`, so both spellings are tried."""
    base = root / vault["repo_dir"]
    for cand in (rel, rel + ".md"):
        p = (base / cand).resolve()
        if p.is_relative_to(base.resolve()) and p.is_file():
            return p
    return None


def check_obsidian(url: str, root: Path = ROOT, vaults: list[dict] | None = None) -> str | None:
    """Why an `obsidian://` link opens nothing, or None when it lands.

    The link names a vault by name or id (`vault=`) or by folder (`path=`);
    `obsidian-vaults.json` maps each of ours to a folder in this repo, and the
    file, `#heading` and review-md `thread` are checked there. A vault not in
    that table is a finding: nothing here can say the link works."""
    from urllib.parse import parse_qs, urlsplit
    vaults = load_vaults() if vaults is None else vaults
    parts = urlsplit(url)
    action = parts.netloc
    q = {k: v[0] for k, v in parse_qs(parts.query).items()}
    if "path" in q:
        target, _, frag = q["path"].partition("#")
        for v in vaults:
            vroot = os.path.expanduser(v["path"]).rstrip("/")
            if target == vroot or target.startswith(vroot + "/"):
                vault, rel = v, target[len(vroot) + 1:]
                break
        else:
            return f"path {target} is in no vault listed in obsidian-vaults.json"
    else:
        name = q.get("vault")
        if name is None:
            return "names no vault (vault= or path=)"
        vault = next((v for v in vaults if name in (v["name"], v["id"])), None)
        if vault is None:
            return f"vault {name} is not listed in obsidian-vaults.json"
        if "file" not in q:
            return None
        rel, _, frag = q["file"].partition("#")
    frag = frag or parts.fragment
    if not rel:
        return None
    file = _vault_file(root, vault, rel)
    if file is None:
        return f"no file {rel} in vault {vault['name']} ({vault['repo_dir']}/)"
    if frag and not fragment_resolves(file, frag):
        return f"no heading or block id #{frag} in {vault['repo_dir']}/{rel}"
    thread = q.get("thread") if action.startswith("review-md-") else None
    if thread:
        comments = file.with_name(f".{file.stem}.comments.md")
        known = "^" + thread in anchors(file) or (
            comments.is_file() and thread in comments.read_text(encoding="utf-8"))
        if not known:
            return f"no review-md thread {thread} on {vault['repo_dir']}/{rel}"
    return None


def check_d1_links(path: Path, lines: list[str]) -> list[str]:
    """A link's file must exist, and a `#part` on a link to a markdown file must
    name a heading or block id in it. Measured before gating, 2026-09-27: 15 of
    54 heading links in docs/ were dead (a renamed heading, a renumbered
    decision, a one-hyphen slug for a heading with a dash) while every file
    they named existed — the file check had been dropping the `#part`.

    An `obsidian://` link is held to the same standard through the vault
    mapping (`check_obsidian`); before, D1 read one as a relative path and
    failed every such link, right or wrong."""
    findings = []
    shown = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    for n, line in enumerate(lines, 1):
        for target in LINK.findall(line) + OBSIDIAN_AUTOLINK.findall(line):
            if target.startswith("obsidian://"):
                why = check_obsidian(target)
                if why:
                    findings.append(f"{shown}:{n}: D1 (K9) obsidian link {why}")
                continue
            if target.startswith(SKIP_SCHEMES):
                continue
            bare, _, fragment = target.partition("#")
            if bare and not link_resolves(path, bare):
                findings.append(
                    f"{shown}:{n}: D1 (K9) link target does not "
                    f"exist: {bare}"
                )
                continue
            file = (path.parent / bare).resolve() if bare else path
            if fragment and file.suffix == ".md" and file.is_file() \
                    and not fragment_resolves(file, fragment):
                findings.append(
                    f"{shown}:{n}: D1 (K9) no heading or block id "
                    f"#{fragment} in {bare or 'this file'}"
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


TABLE_SEPARATOR = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")


def check_d6_code_spans(path: Path, raw: list[str]) -> list[str]:
    """D6 (render): an inline code span opens and closes on one line.

    CommonMark lets a span run across a line break, and GitHub and Obsidian's
    reading view render one fine. Obsidian's editor (Live Preview, where the
    docs are read and reviewed) pairs backticks line by line, so every backtick
    after the break pairs with the wrong partner, and an odd count left at the
    end of a paragraph leaves the rest of the file unrendered: headings, bold
    and tables show as raw text. Built from construction-equivalence.md §4,
    whose wrapped `bikar render … --check` span left §5 and §6's tables as raw
    pipes (review thread 7rlhya, 2026-09-28).

    Scoped to files outside .claude/, which is not in the Obsidian vault. One
    finding per span, on the line it opens: the line that closes it is skipped
    up to the closing run, then read on."""
    findings, in_fence, carry = [], False, None
    for n, line in enumerate(raw, 1):
        if FENCE.match(line):
            in_fence, carry = not in_fence, None
            continue
        if not line.strip():
            carry = None
        if in_fence or line.startswith("    ") and not line.lstrip().startswith(("-", "*", "|")):
            continue
        if carry:
            close = re.compile(rf"(?<!`){carry}(?!`)").search(line)
            if not close:
                continue
            line, carry = line[close.end():], None
        p = unclosed_backtick(line)
        if p is not None:
            carry = re.match(r"`+", line[p:]).group()
            findings.append(
                f"{path.relative_to(ROOT)}:{n}: D6 (render) a code span runs onto the "
                "next line, so Obsidian's editor shows the rest of the file as raw "
                "text — keep each span on one line (docs_gate.py --fix-code-spans FILE)"
            )
    return findings


def unclosed_backtick(line: str) -> int | None:
    """Index of the first backtick run on the line with no closing run of the
    same length after it, or None when every span on the line closes."""
    i = 0
    while (m := re.compile(r"`+").search(line, i)):
        run = m.group()
        close = re.compile(rf"(?<!`){run}(?!`)").search(line, m.end())
        if not close:
            return m.start()
        i = close.end()
    return None


def fix_code_spans(raw: list[str]) -> list[str]:
    """Rewrap so no code span crosses a line break, without changing what any
    renderer shows: the whole word holding the unclosed backtick moves down to
    the start of the next line (a soft break renders as a space, so the text is
    the same), or the next line is joined up when the word starts its line.
    Lines D6 cannot fix safely — the next line is blank, a new block, or would
    start like one — are left for a hand fix and still reported."""
    out, in_fence, i = list(raw), False, 0
    while i < len(out):
        line = out[i]
        if FENCE.match(line):
            in_fence = not in_fence
            i += 1
            continue
        code = line.startswith("    ") and not line.lstrip().startswith(("-", "*", "|"))
        p = None if in_fence or code or line.lstrip().startswith("|") else unclosed_backtick(line)
        nxt = out[i + 1] if i + 1 < len(out) else ""
        if p is None:
            i += 1
            continue
        if not nxt.strip() or FENCE.match(nxt) or HEADING.match(nxt.lstrip()) \
                or re.match(r"^\s*(?:[-*+]\s|\d+\.\s|>|\|)", nxt):
            # Left for a hand fix. The next line's first backtick closes this
            # span, so reading it as an opener would move the wrong word.
            i += 2
            continue
        while p > 0 and not line[p - 1].isspace():
            p -= 1
        head, word = line[:p].rstrip(), line[p:]
        body = nxt.lstrip()
        if not head.strip() or re.fullmatch(r"\s*(?:[-*+]|\d+\.)", head) \
                or re.match(r"(?:[-*+]\s|\d+\.\s|#|>)", word):
            out[i] = line.rstrip() + " " + body
            del out[i + 1]
        else:
            out[i] = head
            out[i + 1] = nxt[: len(nxt) - len(body)] + word.rstrip() + " " + body
            i += 1
    return out


def table_cells(line: str) -> int:
    """Cells in a table row, split the way GitHub and Obsidian split them: on
    every unescaped pipe, inside a code span too, with the optional leading
    and trailing pipe not counted."""
    s = line.strip()
    s = s[1:] if s.startswith("|") else s
    s = s[:-1] if s.endswith("|") and not s.endswith("\\|") else s
    return len(re.split(r"(?<!\\)\|", s))


def check_d7_tables(path: Path, raw: list[str]) -> list[str]:
    """D7 (render): every row of a table has as many cells as its header, and
    the separator row under the header matches it. A row with an extra
    unescaped pipe (a `|` inside backticks is one) silently loses the cells
    past the header's count; a separator that does not match the header means
    the block is not a table at all. Asked for in review thread 7rlhya."""
    findings, in_fence, i = [], False, 0
    while i < len(raw):
        line = raw[i]
        if FENCE.match(line):
            in_fence = not in_fence
        elif (not in_fence and "|" in line and i + 1 < len(raw)
              and TABLE_SEPARATOR.match(raw[i + 1]) and "-" in raw[i + 1]):
            want = table_cells(line)
            got = table_cells(raw[i + 1])
            if got != want:
                findings.append(
                    f"{path.relative_to(ROOT)}:{i + 2}: D7 (render) table separator has "
                    f"{got} cells, header has {want} — the block does not render as a table"
                )
            j = i + 2
            while j < len(raw) and raw[j].strip() and "|" in raw[j]:
                got = table_cells(raw[j])
                if got != want:
                    findings.append(
                        f"{path.relative_to(ROOT)}:{j + 1}: D7 (render) table row has "
                        f"{got} cells, header has {want} — "
                        + ("escape a literal pipe as \\|, even inside backticks" if got > want
                           else "a cell is missing, so the columns shift")
                    )
                j += 1
            i = j
            continue
        i += 1
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


def is_claude_config(path: Path) -> bool:
    """A skill, loop prompt, plan or memory file under .claude/ is not a design
    doc: it quotes the markers to teach them and states no defaults of its own.
    So only D1 applies there — its links must still resolve, because a loop
    follows them. The gate's own fixtures live under .claude/ too and keep
    every rule, since they exist to show each rule firing.

    Judged on the path *inside the repo* when the file is under ROOT: a
    worktree checked out at `<repo>/.claude/worktrees/<name>/` has `/.claude/`
    in every absolute path, and matching that silently skipped D2–D5 for the
    whole tree (docs/issues/docs-gate-worktree-under-claude.md)."""
    if FIXTURES in path.parents:
        return False
    resolved = path.resolve()
    if resolved.is_relative_to(ROOT):
        return resolved.relative_to(ROOT).parts[:1] == (".claude",)
    return "/.claude/" in path.as_posix()


def check_file(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8").splitlines()
    lines = strip_code(raw)
    render = check_d7_tables(path, raw)
    if is_claude_config(path):
        return check_d1_links(path, lines) + render
    render = check_d6_code_spans(path, raw) + render
    if is_print_record(path):
        return check_d1_links(path, lines) + render
    return (
        check_d1_links(path, lines)
        + render
        + check_d2_validators(path, lines, raw)
        + check_d3_defaults(path, lines, raw)
        + check_d4_withdrawn(path, lines)
        + check_d5_registered_bets(path, lines, raw)
    )


def _git_lines(root: Path, *args: str) -> list[str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=True, env=env,
    ).stdout.splitlines()


def is_comment_file(p: str) -> bool:
    """A review-md comment file, `.<note>.comments.md` next to its note. Comments
    are conversation, not claims: a reviewer's "see [the old draft](x.md)" may
    name a file that is gone. Measured 2026-09-27 with a probe comment: D1 fired
    on its link, so every rule skips these files."""
    name = Path(p).name
    return name.startswith(".") and name.endswith(".comments.md")


def staged_markdown(root: Path = ROOT) -> list[Path]:
    out = _git_lines(root, "diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return [root / p for p in out
            if p.endswith(".md") and not is_comment_file(p) and (root / p).exists()]


def stages_a_removal(root: Path = ROOT) -> bool:
    """True when the commit renames or deletes a file. Links *to* that file sit
    in other docs the commit does not stage, so checking only the staged files
    passes a rename that breaks them — measured 2026-09-25: renaming
    docs/tasks/parked/done.md committed clean with five inbound links dead."""
    if _git_lines(root, "diff", "--cached", "--name-only", "--diff-filter=DR"):
        return True
    return stages_a_heading_change(root)


def stages_a_heading_change(root: Path = ROOT) -> bool:
    """True when the commit removes or rewrites a heading line in a markdown
    file. A heading is a link target like a file, and the links into it sit in
    files the commit does not stage."""
    diff = _git_lines(root, "diff", "--cached", "-U0", "--", "*.md")
    return any(HEADING.match(line[1:]) for line in diff
               if line.startswith("-") and not line.startswith("---"))


def tree_markdown(root: Path = ROOT) -> list[Path]:
    """Every markdown file whose links are checked: docs/, CLAUDE.md and .claude/,
    tracked or new, but not gitignored, and not review-md comment files."""
    out = _git_lines(root, "ls-files", "-co", "--exclude-standard", "--",
                     "docs", ".claude", "CLAUDE.md")
    return sorted(root / p for p in out
                  if p.endswith(".md") and not is_comment_file(p) and (root / p).exists())


def staged_findings(root: Path = ROOT) -> tuple[list[str], int]:
    """Every rule on the staged files; D1 on the rest of the tree as well when
    the commit renames or deletes something."""
    staged = [p for p in staged_markdown(root) if FIXTURES not in p.parents]
    findings = [f for p in staged for f in check_file(p)]
    checked = len(staged)
    if stages_a_removal(root):
        done = set(staged)
        for p in tree_markdown(root):
            if p in done or FIXTURES in p.parents:
                continue
            findings += check_d1_links(p, strip_code(p.read_text(encoding="utf-8").splitlines()))
            checked += 1
    return findings, checked


def self_test() -> int:
    """Every rule ships an asserted-PASS and an asserted-FAIL fixture.

    This gate enforces the K6 rule, so it must satisfy it: a rule that has
    never been shown to fire is a rule nobody has tested.
    """
    expected = {
        "fail/d1-dead-link.md": ["D1 (K9)"],
        "fail/d1-dead-heading.md": ["D1 (K9) no heading"],
        "fail/d1-dead-obsidian.md": ["D1 (K9) obsidian link no heading"],
        "fail/d2-validator-no-examples.md": ["D2 (K6)"],
        "fail/d3-uncited-default.md": ["D3 (K4)"],
        "fail/d4-withdrawn-number.md": ["D4 (K1)"],
        "fail/d4-withdrawn-dm-sans.md": ["D4 (K1)"],
        "fail/d5-unregistered-bet.md": ["D5 (K9)"],
        "fail/d6-wrapped-code-span.md": ["D6 (render)"],
        "fail/d7-table-pipe.md": ["D7 (render)"],
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

    # obsidian:// links, through a throwaway vault: every form Obsidian and
    # review-md write must land, and each way one can miss must say why.
    vbase = Path(tempfile.mkdtemp(prefix="docs-gate-vault-"))
    try:
        (vbase / "docs" / "n").mkdir(parents=True)
        (vbase / "docs" / "n" / "note.md").write_text("# Note\n\n## minimal\n\nA passage. ^t1\n")
        (vbase / "docs" / "n" / ".note.comments.md").write_text("thread t2\n")
        home = str(vbase / "vault")
        vs = [{"name": "docs", "id": "abc123", "path": home, "repo_dir": "docs"}]
        cases = [
            (f"obsidian://open?path={home}%2Fn%2Fnote.md%23minimal", None),
            ("obsidian://open?vault=docs&file=n%2Fnote", None),
            ("obsidian://open?vault=abc123&file=n%2Fnote.md%23Minimal", None),
            ("obsidian://review-md-open?vault=docs&file=n%2Fnote.md&thread=t1", None),
            ("obsidian://review-md-reply?vault=docs&file=n%2Fnote.md&thread=t2", None),
            ("obsidian://review-md-export?vault=docs", None),
            ("obsidian://open?vault=other&file=n%2Fnote.md", "not listed"),
            ("obsidian://open?path=%2Felsewhere%2Fnote.md", "in no vault"),
            ("obsidian://open?vault=docs&file=n%2Fgone.md", "no file"),
            ("obsidian://open?vault=docs&file=n%2Fnote.md%23frame", "no heading"),
            ("obsidian://review-md-open?vault=docs&file=n%2Fnote.md&thread=t9", "no review-md thread"),
        ]
        missed = 0
        for url, want in cases:
            got = check_obsidian(url, root=vbase, vaults=vs)
            if (want is None and got is not None) or (want is not None and (got is None or want not in got)):
                missed += 1
                print(f"self-test FAIL: {url} expected {want or 'to land'}, got {got}")
        if missed:
            ok = False
        else:
            print(f"self-test ok: obsidian links — {len(cases)} forms land or miss as designed")
    finally:
        shutil.rmtree(vbase, ignore_errors=True)
        _ANCHORS.clear()

    # D1 must give the same verdict from a linked worktree as from the primary
    # clone: a `../../sib/f.md` link written for the primary layout escapes a
    # worktree at `repo.worktrees/w` and must be re-tried beside the primary.
    import subprocess as _sp
    base = Path(tempfile.mkdtemp(prefix="docs-gate-wt-"))
    try:
        genv = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        genv.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
                    GIT_COMMITTER_EMAIL="t@t")
        repo = base / "repo"
        repo.mkdir()
        _sp.run(["git", "init", "-q", str(repo)], check=True, env=genv)
        (repo / "docs").mkdir()
        (repo / "docs" / "a.md").write_text("[x](../../sib/f.md) [y](../../sib/missing.md)\n")
        _sp.run(["git", "-C", str(repo), "add", "."], check=True, env=genv)
        _sp.run(["git", "-C", str(repo), "commit", "-qm", "init"], check=True, env=genv)
        (base / "sib").mkdir()
        (base / "sib" / "f.md").write_text("sib\n")
        wt = base / "repo.worktrees" / "w"
        _sp.run(["git", "-C", str(repo), "worktree", "add", "-q", str(wt)], check=True, env=genv)
        doc = wt / "docs" / "a.md"
        got = (link_resolves(doc, "../../sib/f.md", root=wt),
               link_resolves(doc, "../../sib/missing.md", root=wt),
               link_resolves(repo / "docs" / "a.md", "../../sib/f.md", root=repo))
        if got != (True, False, True):
            ok = False
            print(f"self-test FAIL: worktree D1 fallback expected (True, False, True), got {got}")
        else:
            print("self-test ok: a sibling link resolves from a worktree via the primary; a dead one stays dead")
    finally:
        shutil.rmtree(base, ignore_errors=True)

    # Links break where the renamed file is linked *from*, not where it moved,
    # and .claude/ files are linked from loops that follow them. Both are
    # exercised in a throwaway repo: a doc under .claude/ keeps D1 but not the
    # design-doc rules, the whole-tree list reaches it, and a staged rename
    # fails the commit through a link in a file the commit does not touch.
    base = Path(tempfile.mkdtemp(prefix="docs-gate-rename-"))
    try:
        repo = base / "repo"
        (repo / "docs").mkdir(parents=True)
        (repo / ".claude" / "skills").mkdir(parents=True)
        _sp.run(["git", "init", "-q", str(repo)], check=True, env=genv)
        (repo / "docs" / "target.md").write_text("target\n")
        (repo / "docs" / "linker.md").write_text("[t](target.md)\n")
        # A review-md comment file linking the same target: the rename below
        # breaks its link too, and it must not be reported.
        comments = repo / "docs" / ".linker.comments.md"
        comments.write_text("[t](target.md) [gone](none.md)\n")
        skill = repo / ".claude" / "skills" / "note.md"
        skill.write_text(d4 + "\n[t](../../docs/target.md) [gone](../../docs/none.md)\n")
        _sp.run(["git", "-C", str(repo), "add", "."], check=True, env=genv)
        _sp.run(["git", "-C", str(repo), "commit", "-qm", "init"], check=True, env=genv)

        codes = [f.split(": ")[1].split(" ")[0] for f in check_file(skill)]
        if codes != ["D1"]:
            ok = False
            print(f"self-test FAIL: a .claude/ doc should get D1 only (one dead link), got {codes}")
        else:
            print("self-test ok: a .claude/ doc gets D1 only — its dead link fires, its D4 text does not")
        if skill not in tree_markdown(repo):
            ok = False
            print("self-test FAIL: the whole-tree list should include .claude/ markdown")
        else:
            print("self-test ok: the whole-tree list reaches .claude/")
        if comments in tree_markdown(repo):
            ok = False
            print("self-test FAIL: the whole-tree list should skip review-md comment files")
        else:
            print("self-test ok: the whole-tree list skips review-md comment files")

        skill.write_text("[t](../../docs/target.md)\n")
        _sp.run(["git", "-C", str(repo), "commit", "-qam", "fix"], check=True, env=genv)

        # A heading is a link target too: renaming it in a staged file must
        # fail on the unstaged file that links to it.
        (repo / "docs" / "target.md").write_text("# Title\n")
        (repo / "docs" / "linker.md").write_text("[t](target.md#title)\n")
        _sp.run(["git", "-C", str(repo), "commit", "-qam", "heading"], check=True, env=genv)
        (repo / "docs" / "target.md").write_text("# Renamed\n")
        _sp.run(["git", "-C", str(repo), "add", "docs/target.md"], check=True, env=genv)
        _ANCHORS.clear()
        found, _ = staged_findings(repo)
        if [Path(f.split(":")[0]).name for f in found] != ["linker.md"]:
            ok = False
            print(f"self-test FAIL: a staged heading rename should fail on the unstaged linker, got {found}")
        else:
            print("self-test ok: a staged heading rename fails on a link in a file the commit does not touch")
        _sp.run(["git", "-C", str(repo), "reset", "-q", "--hard"], check=True, env=genv)
        (repo / "docs" / "linker.md").write_text("[t](target.md)\n")
        _sp.run(["git", "-C", str(repo), "commit", "-qam", "unlink"], check=True, env=genv)
        _ANCHORS.clear()
        _sp.run(["git", "-C", str(repo), "mv", "docs/target.md", "docs/moved.md"], check=True, env=genv)
        found, _ = staged_findings(repo)
        hit = sorted({Path(f.split(":")[0]).name for f in found})
        if hit != ["linker.md", "note.md"]:
            ok = False
            print(f"self-test FAIL: a staged rename should fail on both unstaged linkers, got {found}")
        else:
            print("self-test ok: a staged rename fails on links in files the commit does not touch")
    finally:
        shutil.rmtree(base, ignore_errors=True)

    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--fix-code-spans", action="store_true",
                    help="rewrap the given files so no code span crosses a line (D6), then check them")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    if args.fix_code_spans:
        for p in args.files:
            raw = p.read_text(encoding="utf-8").splitlines()
            fixed = fix_code_spans(raw)
            if fixed != raw:
                p.write_text("\n".join(fixed) + "\n", encoding="utf-8")
                print(f"rewrapped {p}")

    if args.staged:
        findings, checked = staged_findings()
    else:
        if args.files:
            targets = [p if p.is_absolute() else (ROOT / p) for p in args.files]
        else:
            targets = tree_markdown()
        targets = [p for p in targets if FIXTURES not in p.parents]
        findings = [f for p in targets for f in check_file(p)]
        checked = len(targets)

    for f in findings:
        print(f, file=sys.stderr)
    if findings:
        print(
            f"\ndocs-gate: {len(findings)} finding(s) in {checked} file(s). "
            "See docs/grounding-defect-taxonomy.md. Override once with "
            "DOCS_GATE_OK=1 git commit",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
