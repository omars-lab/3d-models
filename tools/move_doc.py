#!/usr/bin/env python3
"""move_doc — move notes in docs/ and every reference to them, in one run.

    python3 tools/move_doc.py OLD NEW [OLD NEW ...] [--dry-run]
    python3 tools/move_doc.py --plan FILE [--dry-run]
    python3 tools/move_doc.py --self-test

Paths are repo-relative (`docs/example-design.md docs/design/example/example-design.md`).
A plan file holds one move per line, `old new`; `#` starts a comment. A note's
review-md comments (`.<name>.comments.md`) and its picture folder (`<name>/`
beside it) move with it without being named.

What it rewrites, in every tracked text file:
  - markdown link targets that point at a moved file, and a moved note's own
    relative links for its new depth (`#heading` parts are kept as written);
  - wikilinks that name a path (`[[bases/x.base]]`); a bare `[[name]]` finds
    the note wherever it is, so it is left alone;
  - repo paths `docs/<old>` — backticked pointers, the use-case map's
    `3d-models:docs/<old>:L1` anchors, keys in doc-pointer-baseline.json, and
    comments or strings in the Makefile, tools, hooks and tools/bambu/src;
  - a backticked path a doc writes relative to itself (`example-design/x.png`),
    and a link label that repeats its own target ([`../x.md`](../x.md)).

What it leaves as written:
  - another repo's path written `<repo>:docs/x.md` (`qiyas:docs/x.md` is
    qiyas's file even when this repo has one of the same name).

What it leaves as written, and lists:
  - research/ prose. A research file is kept verbatim, so only its link targets
    move (a target is an address, not researched content);
  - the docs gate's fixtures (.claude/gates/fixtures/) are not on this list:
    their prose is test input, but the pointer gate reads them (it skips
    research/), so a link or backticked path to a real note moves with it;
  - review-md comment files. They are conversation, and review-md owns them;
  - a path it cannot tie to this repo (`3d-models-constructions/docs/x.md`);
  - files git does not track (another session's work);
  - references in the sibling repos, grepped read-only at their origin refs.
    A sibling that checks `3d-models/docs/...` pointers (bikar) needs its own
    PR right behind the move.

It also flags a bare `[[name]]` that stops being unique, and a view in
docs/bases/ that still keys on a note sitting at the docs root.

It refuses to touch a file with uncommitted changes, stages what it moved and
rewrote by name, and never commits. `--self-test` moves a real note in a copy
of this repo and requires the docs gate and the pointer gate to stay green —
and to go red when one reference the mover fixed is put back.
"""
from __future__ import annotations

import argparse
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parents[1]

FIXTURES = ".claude/gates/fixtures/"
RESEARCH = "docs/research/"
USE_CASES = ".claude/skills/maintain-use-cases/use-cases.md"
BASELINE = ".claude/gates/doc-pointer-baseline.json"
BASES = "docs/bases/"
SELF = "tools/move_doc.py"  # its test strings are data, never rewritten

# Siblings grepped read-only for references a move would break: (name, refs to
# try in order). Read at the ref, never the checked-out tree, so the answer does
# not depend on what another session has checked out over there.
SIBLINGS = (
    ("bikar", ("origin/main", "main")),
    ("qiyas", ("origin/main", "main")),
    ("sacred-patterns", ("origin/master", "master")),
    ("3d-model-hub", ("origin/main", "main")),
    ("youtube", ("origin/main", "main")),
)

# Link and code-span shapes, the same ones the docs gate reads.
FENCE = re.compile(r"^\s*(```|~~~)")
LINK = re.compile(r"(\[[^\]]*\]\()([^)\s]+)((?:\s+\"[^\"]*\")?\))")
WIKILINK = re.compile(r"(!?\[\[)([^\[\]|#^]*)([^\[\]]*\]\])")
BACKTICKED = re.compile(r"`([A-Za-z0-9_.@/-]+)`")
PATHISH = re.compile(r"[A-Za-z0-9_.@-]*(?:/[A-Za-z0-9_.@-]+)+/?")
# `qiyas:` just before a path: the path is that repo's, not this one's.
OTHER_REPO = re.compile(r"(?<![\w.-])(?!3d-models:)[\w-]+:\Z")
SKIP_SCHEMES = ("http://", "https://", "mailto:", "ftp://", "data:", "obsidian://")

# Relative-path arithmetic runs against a deep made-up root, so a link that
# climbs out of the repo (`../../bikar/x.md`) keeps pointing at the same place.
VROOT = "/v/v/v/v/v/v/v/v/repo"


# --- the move set -------------------------------------------------------------


@dataclass
class Move:
    old: str
    new: str
    is_dir: bool
    why: str  # "asked", "comments", "pictures"


def norm(p: str) -> str:
    p = p.strip().replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return posixpath.normpath(p)


def git(root: Path, *args: str, check: bool = True) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                          text=True, check=check, env=env).stdout


def read_plan(text: str) -> list[tuple[str, str]]:
    pairs = []
    for n, line in enumerate(text.splitlines(), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2:
            raise SystemExit(f"plan line {n}: want `old new`, got {line!r}")
        pairs.append((parts[0], parts[1]))
    return pairs


def expand(root: Path, pairs: list[tuple[str, str]]) -> tuple[list[Move], list[str]]:
    """The asked moves plus each note's comments file and picture folder."""
    moves: list[Move] = []
    errors: list[str] = []
    for old, new in pairs:
        old, new = norm(old), norm(new)
        src = root / old
        if not src.exists():
            errors.append(f"{old}: no such file or folder")
            continue
        if not old.startswith("docs/") or not new.startswith("docs/"):
            errors.append(f"{old} -> {new}: both paths must be under docs/")
            continue
        if (root / new).exists():
            errors.append(f"{new}: already exists")
            continue
        moves.append(Move(old, new, src.is_dir(), "asked"))
        if src.is_file() and old.endswith(".md"):
            od, on = posixpath.split(old)
            nd, nn = posixpath.split(new)
            ostem, nstem = on[:-3], nn[:-3]
            side = posixpath.join(od, f".{ostem}.comments.md")
            if (root / side).is_file():
                moves.append(Move(side, posixpath.join(nd, f".{nstem}.comments.md"), False, "comments"))
            pics = posixpath.join(od, ostem)
            if (root / pics).is_dir():
                moves.append(Move(pics, posixpath.join(nd, nstem), True, "pictures"))
    seen_old: dict[str, Move] = {}
    seen_new: set[str] = set()
    out = []
    for m in moves:
        if m.old in seen_old:
            if seen_old[m.old].new != m.new:
                errors.append(f"{m.old}: moved twice, to {seen_old[m.old].new} and {m.new}")
            continue
        if m.new in seen_new:
            errors.append(f"{m.new}: two moves land here")
            continue
        seen_old[m.old] = m
        seen_new.add(m.new)
        out.append(m)
    return out, errors


class Mapper:
    """Old path -> new path, for files and for everything under a moved folder."""

    def __init__(self, root: Path, moves: list[Move]):
        self.root = root
        self.moves = sorted(moves, key=lambda m: -len(m.old))

    def map(self, rel: str) -> str | None:
        for m in self.moves:
            if rel == m.old:
                return m.new
            if m.is_dir and rel.startswith(m.old + "/"):
                return m.new + rel[len(m.old):]
        return None

    def unmap(self, rel: str) -> str | None:
        for m in sorted(self.moves, key=lambda m: -len(m.new)):
            if rel == m.new:
                return m.old
            if m.is_dir and rel.startswith(m.new + "/"):
                return m.old + rel[len(m.new):]
        return None

    def exists_before(self, rel: str) -> bool:
        return not rel.startswith("..") and (self.root / rel).exists()

    def exists_after(self, rel: str) -> bool:
        """Does `rel` exist once the moves are done? Answered without moving."""
        if rel.startswith(".."):
            return False
        back = self.unmap(rel)
        if back is not None:
            return (self.root / back).exists()
        if self.map(rel) is not None:
            return False
        p = self.root / rel
        if p.exists():
            return True
        # A folder that only comes into being because something moves into it.
        return any(m.new.startswith(rel.rstrip("/") + "/") for m in self.moves)


# --- rewriting one file ---------------------------------------------------------


@dataclass
class Change:
    kind: str      # "link-in", "link-out", "wikilink", "path", "relative"
    line: int
    before: str
    after: str


@dataclass
class Leftover:
    file: str
    line: int
    token: str
    why: str


def rel_between(target: str, from_dir: str) -> str:
    """`target` (repo-relative, may climb out) written relative to `from_dir`."""
    return posixpath.relpath(posixpath.join(VROOT, target), posixpath.join(VROOT, from_dir))


def resolve_from(from_dir: str, bare: str) -> str:
    """A relative target read from `from_dir`, as a repo-relative path (may start `..`)."""
    full = posixpath.normpath(posixpath.join(VROOT, from_dir, bare))
    return posixpath.relpath(full, VROOT)


def code_spans(line: str, open_at_start: bool = False) -> tuple[list[tuple[int, int]], bool]:
    """The code spans on one line, and whether one is still open at its end.
    CommonMark lets a span wrap onto the next line of the same paragraph, so a
    line can start inside one (`open_at_start`); pairing backticks line by line
    would then pair them wrongly and hide a link after them. docs/ forbids the
    wrap (docs gate D6), but skills and plans outside it still have ~150."""
    spans, i = [], 0
    if open_at_start:
        j = line.find("`")
        if j < 0:
            return [(0, len(line))], True
        spans.append((0, j + 1))
        i = j + 1
    while True:
        j = line.find("`", i)
        if j < 0:
            return spans, False
        k = line.find("`", j + 1)
        if k < 0:
            spans.append((j, len(line)))
            return spans, True
        spans.append((j, k + 1))
        i = k + 1


def inside(spans: list[tuple[int, int]], i: int) -> bool:
    return any(a <= i < b for a, b in spans)


def is_comment_file(rel: str) -> bool:
    name = posixpath.basename(rel)
    return name.startswith(".") and name.endswith(".comments.md")


def rooted_pattern(mapper: Mapper) -> re.Pattern[str] | None:
    """`docs/<old>` wherever it is written as a path from the repo root: alone,
    or after `3d-models/` or `3d-models:`. Not after another path segment —
    `3d-models-constructions/docs/x.md` names a different checkout — and not
    after another repo's `name:` (`qiyas:docs/local-ci-runbook.md` is qiyas's)."""
    alts = []
    for m in mapper.moves:
        # A file path may end a sentence (`docs/a.md.`) but not run on (`docs/a.md.bak`).
        tail = r"(?![\w.-])" if m.is_dir else r"(?![\w-]|\.[\w-])"
        alts.append(re.escape(m.old) + tail)
    if not alts:
        return None
    return re.compile(r"(?:(?<=3d-models/)|(?<=3d-models:)|(?<![\w./:-]))(" + "|".join(alts) + ")")


def rewrite_text(rel: str, text: str, mapper: Mapper, rooted: re.Pattern | None) -> tuple[str, list[Change]]:
    """Every rewrite this file gets. `rel` is its path before the move."""
    new_rel = mapper.map(rel) or rel
    moved = new_rel != rel
    old_dir, new_dir = posixpath.dirname(rel), posixpath.dirname(new_rel)
    is_md = rel.endswith(".md")
    research = rel.startswith(RESEARCH)  # link targets move, prose is kept
    in_vault = rel.startswith("docs/")
    changes: list[Change] = []

    def fix_link(n: int, target: str) -> str:
        if target.startswith(SKIP_SCHEMES) or target.startswith(("#", "/", "<")) or "://" in target:
            return target
        bare, hashmark, frag = target.partition("#")
        if not bare:
            return target
        decoded = unquote(bare)
        was = resolve_from(old_dir, decoded)
        now = mapper.map(was) or was
        if not moved and now == was:
            return target
        new_bare = rel_between(now, new_dir)
        if decoded.endswith("/") and not new_bare.endswith("/"):
            new_bare += "/"
        if decoded.startswith("./") and not new_bare.startswith("."):
            new_bare = "./" + new_bare
        if decoded != bare:
            new_bare = quote(new_bare, safe="/.-_~")
        if new_bare == bare:
            return target
        out = new_bare + hashmark + frag
        changes.append(Change("link-out" if moved else "link-in", n, target, out))
        return out

    def fix_link_match(n: int, m: re.Match) -> str:
        """A link, and its label too when the label is the address itself
        ([`../x.md`](../x.md)) — then it is part of the address, not prose."""
        head, target, tail = m.group(1), m.group(2), m.group(3)
        new = fix_link(n, target)
        if new != target and head in (f"[{target}](", f"[`{target}`]("):
            head = head.replace(target, new, 1)
        return head + new + tail

    def fix_wikilink(n: int, target: str) -> str:
        t = target.strip()
        if "/" not in t or not in_vault:
            return target
        vault_rel = "docs/" + t
        cands = [vault_rel, vault_rel + ".md"]
        for c in cands:
            if mapper.exists_before(c):
                now = mapper.map(c)
                if now is None:
                    return target
                out = now[len("docs/"):]
                if c.endswith(".md") and not t.endswith(".md"):
                    out = out[:-3]
                changes.append(Change("wikilink", n, target, out))
                return out
        return target

    def fix_relative(n: int, tok: str) -> str:
        """A backticked path the doc writes relative to itself."""
        if tok.startswith(("docs/", "3d-models")) or "/" not in tok:
            return tok
        if mapper.exists_before(norm(tok)):
            return tok  # a path from the repo root, which the pointer gate tries first
        was = resolve_from(old_dir, tok)
        if not mapper.exists_before(was):
            return tok
        now = mapper.map(was) or was
        if not moved and now == was:
            return tok
        out = rel_between(now, new_dir)
        if tok.endswith("/") and not out.endswith("/"):
            out += "/"
        if out == tok:
            return tok
        changes.append(Change("relative", n, tok, out))
        return out

    lines = text.split("\n")
    in_fence = False
    span_open = False  # a code span wrapped onto this line from the one above
    for i, line in enumerate(lines):
        n = i + 1
        if is_md:
            if FENCE.match(line):
                in_fence = not in_fence
            if in_fence or FENCE.match(line) or not line.strip():
                span_open = False  # a paragraph ends, and an unclosed backtick with it
            else:
                opened = span_open
                spans, span_open = code_spans(line, opened)
                line = LINK.sub(lambda m: m.group(0) if inside(spans, m.start())
                                else fix_link_match(n, m), line)
                spans, _ = code_spans(line, opened)
                line = WIKILINK.sub(lambda m: m.group(0) if inside(spans, m.start())
                                    else m.group(1) + fix_wikilink(n, m.group(2)) + m.group(3), line)
                if not research:
                    line = BACKTICKED.sub(lambda m: "`" + fix_relative(n, m.group(1)) + "`", line)
        if rooted is not None and not research:
            def sub_rooted(m: re.Match) -> str:
                out = mapper.map(m.group(1))
                changes.append(Change("path", n, m.group(1), out))
                return out
            line = rooted.sub(sub_rooted, line)
        lines[i] = line
    return "\n".join(lines), changes


def leftovers(rel: str, text: str, mapper: Mapper, why: str) -> list[Leftover]:
    """Path-shaped tokens that still name a moved file's old place, once the
    rewrite is done: each would be a dead reference after the move."""
    new_rel = mapper.map(rel) or rel
    new_dir = posixpath.dirname(new_rel)
    names = {posixpath.basename(m.old) for m in mapper.moves}
    out = []
    for n, line in enumerate(text.split("\n"), 1):
        tokens = [m.group(0) for m in PATHISH.finditer(line)
                  if not OTHER_REPO.search(line, 0, m.start())]
        tokens += [m.group(2) for m in LINK.finditer(line)]
        for tok in tokens:
            bare = unquote(tok.split("#", 1)[0]).rstrip("/")
            if not bare or posixpath.basename(bare) not in names and \
                    not any(seg in names for seg in bare.split("/")):
                continue
            rooted = norm(bare)
            if mapper.exists_after(rooted) or mapper.exists_after(resolve_from(new_dir, bare)):
                continue
            framed = "/" + rooted + "/"
            names_old = any("/" + m.old + "/" in framed for m in mapper.moves)
            if not names_old and mapper.map(resolve_from(posixpath.dirname(rel), bare)) is None:
                continue  # names something else that happens to share a word
            out.append(Leftover(rel, n, tok, why))
    return out


# --- the run --------------------------------------------------------------------


@dataclass
class Report:
    moves: list[Move]
    changes: dict[str, list[Change]] = field(default_factory=dict)
    left: list[Leftover] = field(default_factory=list)
    name_only: int = 0
    collisions: list[str] = field(default_factory=list)
    base_warnings: list[str] = field(default_factory=list)
    siblings: list[str] = field(default_factory=list)
    sibling_refs: list[str] = field(default_factory=list)
    dirty: list[str] = field(default_factory=list)


def area(rel: str) -> str:
    if rel.startswith(RESEARCH):
        return "research"
    if rel.startswith(FIXTURES):
        return "gate fixtures"
    if rel == USE_CASES:
        return "use-case map"
    if rel == BASELINE:
        return "pointer baseline"
    if rel.startswith("docs/"):
        return "docs"
    if rel.startswith(".claude/") or rel == "CLAUDE.md":
        return ".claude"
    return "code"


def tracked(root: Path) -> list[str]:
    return [p for p in git(root, "ls-files").splitlines() if p]


def untracked(root: Path) -> list[str]:
    return [p for p in git(root, "ls-files", "-o", "--exclude-standard").splitlines() if p]


def candidates(root: Path, mapper: Mapper, files: list[str]) -> list[str]:
    """Tracked text files that could mention a moved path, plus the moved notes."""
    words = sorted({posixpath.basename(m.old).removesuffix(".md").lstrip(".").removesuffix(".comments")
                    for m in mapper.moves})
    args = ["grep", "-I", "-l", "-F"]
    for w in words:
        args += ["-e", w]
    hits = set(git(root, *args, check=False).splitlines())
    hits |= {f for f in files if mapper.map(f) is not None and f.endswith(".md")}
    known = set(files)
    return sorted(f for f in hits if f in known and f != SELF)


def names_ours(body: str, needle: str, sibling_has_own: bool) -> bool:
    """Whether a sibling's line names this repo's `needle` (a `docs/...` path).
    Tied to 3d-models (`3d-models/docs/x.md`, `3d-models:docs/x.md`, 3d-models
    `docs/x.md`) it does; after another repo's name (`qiyas:docs/x.md`) it does
    not; bare, it does only when the sibling has no file of that name itself."""
    for m in re.finditer(re.escape(needle) + r"(?![\w-]|\.[\w-])", body):
        before = body[:m.start()]
        if re.search(r"3d-models[/:]?\s*`?\Z", before):
            return True
        if re.search(r"[\w-]+[:/]\Z", before):
            continue
        if not sibling_has_own:
            return True
    return False


def sibling_refs(root: Path, moves: list[Move]) -> tuple[list[str], list[str]]:
    """Read-only grep of each sibling repo at its origin ref."""
    parent = Path(git(root, "rev-parse", "--path-format=absolute", "--git-common-dir").strip()).parent.parent
    searched, hits = [], []
    needles = [m.old for m in moves if m.why == "asked"]
    for name, refs in SIBLINGS:
        repo = parent / name
        if not repo.exists():
            searched.append(f"{name}: not checked out beside this repo — not searched")
            continue
        ref = next((r for r in refs if git(repo, "rev-parse", "--verify", "-q", r, check=False).strip()), None)
        if ref is None:
            searched.append(f"{name}: none of {', '.join(refs)} exists — not searched")
            continue
        sha = git(repo, "rev-parse", "--short", ref).strip()
        searched.append(f"{name} at {ref} ({sha})")
        args = ["grep", "-n", "-I", "-F"]
        for nd in needles:
            args += ["-e", nd]
        out = git(repo, *args, ref, "--", check=False)
        for line in out.splitlines():
            _, path, lineno, body = (line.split(":", 3) + ["", "", ""])[:4]
            # A sibling may have a docs/<same name> of its own, or name a third
            # repo's (`qiyas:docs/x.md`); only a mention of ours is listed.
            if not any(names_ours(body, nd, subprocess.run(
                    ["git", "-C", str(repo), "cat-file", "-e", f"{ref}:{nd}"],
                    capture_output=True).returncode == 0) for nd in needles if nd in body):
                continue
            hits.append(f"{name}:{path}:{lineno}: {body.strip()[:160]}")
    return searched, hits


def plan_run(root: Path, moves: list[Move], with_siblings: bool = True) -> tuple[Report, dict[str, str]]:
    mapper = Mapper(root, moves)
    rooted = rooted_pattern(mapper)
    files = tracked(root)
    report = Report(moves)
    new_texts: dict[str, str] = {}

    for rel in candidates(root, mapper, files):
        text = (root / rel).read_text(encoding="utf-8", errors="surrogateescape")
        if is_comment_file(rel):
            report.left += leftovers(rel, text, mapper, "review-md comments, not edited")
            continue
        new, changes = rewrite_text(rel, text, mapper, rooted)
        if changes:
            report.changes[rel] = changes
            new_texts[rel] = new
        why = "research prose, kept as written" if rel.startswith(RESEARCH) else "not tied to this repo"
        report.left += leftovers(rel, new, mapper, why)
        names = {posixpath.basename(m.old) for m in moves if not m.is_dir}
        report.name_only += sum(len(re.findall(r"(?<![\w/.(-])" + re.escape(nm) + r"(?![\w-])", new))
                                for nm in names)

    for rel in untracked(root):
        p = root / rel
        if not p.is_file() or p.stat().st_size > 2_000_000:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        report.left += leftovers(rel, text, mapper, "untracked — another session's file, not edited")

    # A bare [[name]] finds a note by its file name; that holds only while the
    # name is unique in the vault.
    vault = [f for f in files if f.startswith("docs/")]
    after = Counter(posixpath.basename(mapper.map(f) or f).lower() for f in vault)
    for m in moves:
        if not m.is_dir and m.new.endswith(".md") and after[posixpath.basename(m.new).lower()] > 1:
            twins = [f for f in vault if posixpath.basename(mapper.map(f) or f).lower()
                     == posixpath.basename(m.new).lower()]
            report.collisions.append(f"{posixpath.basename(m.new)}: {len(twins)} notes share this name "
                                     f"({', '.join(twins)}) — a bare [[wikilink]] to it is ambiguous")

    for rel in files:
        if rel.startswith(BASES) and rel.endswith(".base"):
            text = (root / rel).read_text(encoding="utf-8")
            if 'file.path.contains("/")' in text:
                report.base_warnings.append(f"{rel}: keys on a note sitting at the docs root "
                                            '(file.path.contains("/")) — moved notes drop out of it')
            for m in moves:
                if m.old[len("docs/"):] in text:
                    report.base_warnings.append(f"{rel}: names {m.old[len('docs/'):]} by path")

    touched = set(new_texts) | {m.old for m in moves}
    status = git(root, "status", "--porcelain", "--", *sorted(touched)) if touched else ""
    report.dirty = [line[3:] for line in status.splitlines() if line.strip()]

    if with_siblings:
        report.siblings, report.sibling_refs = sibling_refs(root, moves)
    return report, new_texts


def apply(root: Path, moves: list[Move], new_texts: dict[str, str]) -> list[str]:
    mapper = Mapper(root, moves)
    staged: list[str] = []
    for m in moves:
        (root / m.new).parent.mkdir(parents=True, exist_ok=True)
        git(root, "mv", m.old, m.new)
    for rel, text in new_texts.items():
        dest = mapper.map(rel) or rel
        (root / dest).write_text(text, encoding="utf-8", errors="surrogateescape")
        staged.append(dest)
    if staged:
        git(root, "add", "--", *staged)
    return staged


def summary(report: Report, dry: bool) -> str:
    out = []
    kinds = Counter(m.why for m in report.moves)
    out.append(("would move" if dry else "moved") +
               f": {kinds['asked']} note(s), {kinds['comments']} comment file(s), "
               f"{kinds['pictures']} picture folder(s)")
    for m in report.moves:
        out.append(f"  {m.old} -> {m.new}" + ("" if m.why == "asked" else f"   ({m.why})"))
    by = defaultdict(Counter)
    files_by = defaultdict(set)
    for rel, changes in report.changes.items():
        for c in changes:
            by[c.kind][area(rel)] += 1
            files_by[area(rel)].add(rel)
    labels = {"link-in": "inbound links", "link-out": "moved notes' own links",
              "wikilink": "path wikilinks", "path": "repo paths (docs/<old>)",
              "relative": "doc-relative backticked paths"}
    total = sum(len(c) for c in report.changes.values())
    out.append(("would rewrite" if dry else "rewrote") +
               f": {total} reference(s) in {len(report.changes)} file(s)")
    for kind in ("link-in", "link-out", "wikilink", "path", "relative"):
        if by[kind]:
            parts = ", ".join(f"{a} {n}" for a, n in sorted(by[kind].items()))
            out.append(f"  {labels[kind]}: {sum(by[kind].values())}  ({parts})")
    out.append("  files per area: " + ", ".join(f"{a} {len(s)}" for a, s in sorted(files_by.items())))
    if report.name_only:
        out.append(f"left alone: {report.name_only} mention(s) by file name only — a name still finds the note")
    groups = defaultdict(list)
    for lo in report.left:
        groups[lo.why].append(lo)
    for why, items in sorted(groups.items()):
        out.append(f"found, not rewritten — {why}: {len(items)}")
        for lo in items:
            out.append(f"  {lo.file}:{lo.line}: {lo.token}")
    for c in report.collisions:
        out.append(f"name clash: {c}")
    for w in report.base_warnings:
        out.append(f"view: {w}")
    if report.siblings:
        out.append("sibling repos (read-only, at their origin refs): " + "; ".join(report.siblings))
        out.append(f"  references there: {len(report.sibling_refs)}")
        for s in report.sibling_refs:
            out.append(f"  {s}")
    if USE_CASES in report.changes:
        out.append("next: python3 .claude/skills/maintain-use-cases/validate.py --refresh "
                   "(the use-case map changed), then make validate")
    elif not dry:
        out.append("next: make validate")
    return "\n".join(out)


# --- self-test ------------------------------------------------------------------


def _check(ok: bool, what: str, failures: list[str]) -> None:
    print(f"self-test {'ok  ' if ok else 'FAIL'}: {what}")
    if not ok:
        failures.append(what)


def unit_cases(failures: list[str]) -> None:
    """The path arithmetic, on strings, against a scratch tree."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel in ("docs/a-design.md", "docs/plan.md", "docs/research/r.md",
                    "docs/a-design/pic.png", "docs/.a-design.comments.md", "src/x.bkr"):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text("x\n")
        moves, errs = expand(root, [("docs/a-design.md", "docs/design/c/a-design.md")])
        _check(not errs and [m.why for m in moves] == ["asked", "comments", "pictures"],
               "a note brings its comments file and picture folder", failures)
        mp = Mapper(root, moves)
        rx = rooted_pattern(mp)
        cases = [
            ("docs/plan.md", "[a](a-design.md#x-y)", "[a](design/c/a-design.md#x-y)", "inbound link, #part kept"),
            ("docs/plan.md", "![p](a-design/pic.png)", "![p](design/c/a-design/pic.png)", "a picture in the moved folder"),
            ("docs/plan.md", "`[a](a-design.md)`", "`[a](a-design.md)`", "a link inside code is a mention"),
            ("docs/a-design.md", "[p](plan.md)", "[p](../../plan.md)", "a moved note's own link"),
            ("docs/a-design.md", "[s](../src/x.bkr)", "[s](../../../src/x.bkr)", "a moved note's link out of docs/"),
            ("docs/a-design.md", "[b](../../bikar/y.md)", "[b](../../../../bikar/y.md)", "a link that leaves the repo"),
            ("docs/a-design.md", "[p](a-design/pic.png)", "[p](a-design/pic.png)", "note and folder move together"),
            ("docs/a-design.md", "see [the top](#top)", "see [the top](#top)", "a same-page #part"),
            ("docs/research/r.md", "[a](../a-design.md)", "[a](../design/c/a-design.md)", "research: the link target moves"),
            ("docs/research/r.md", "from `docs/a-design.md` §3", "from `docs/a-design.md` §3", "research: prose is kept"),
            (".claude/gates/fixtures/pass/f.md", "[t](../../../../docs/a-design.md#k9)",
             "[t](../../../../docs/design/c/a-design.md#k9)", "a gate fixture: the link target moves"),
            (".claude/gates/fixtures/pass/f.md", "shipped as `docs/a-design.md`", "shipped as `docs/design/c/a-design.md`",
             "a gate fixture: the pointer gate reads it, so a pointer to a real note moves"),
            (".claude/x.md", "`docs/a-design.md`", "`docs/design/c/a-design.md`", "a backticked pointer"),
            (".claude/x.md", "`3d-models:docs/a-design.md:L1 \"# A\"`",
             "`3d-models:docs/design/c/a-design.md:L1 \"# A\"`", "a use-case map anchor"),
            ("tools/t.py", "# docs/a-design.md §2", "# docs/design/c/a-design.md §2", "a code comment"),
            ("tools/t.py", "docs/a-design/pic.png", "docs/design/c/a-design/pic.png", "a path into the moved folder"),
            (".claude/x.md", "`wt-x/docs/a-design.md`", "`wt-x/docs/a-design.md`", "another checkout's path"),
            ("docs/plan.md", "`qiyas:docs/a-design.md` and bikar:docs/a-design.md",
             "`qiyas:docs/a-design.md` and bikar:docs/a-design.md", "another repo's path, `repo:` prefixed"),
            (".claude/x.md", "`docs/a-design.md.bak` docs/a-design-b.md", "`docs/a-design.md.bak` docs/a-design-b.md",
             "a longer name that starts the same"),
            ("docs/plan.md", "`a-design/pic.png`", "`design/c/a-design/pic.png`", "a doc-relative backticked path"),
            ("docs/plan.md", "![[a-design/pic.png]] [[a-design]]", "![[design/c/a-design/pic.png]] [[a-design]]",
             "a path wikilink moves, a bare one stays"),
            (".claude/s/x.md", "run `validate\nrecord` then [a](../../docs/a-design.md) and `y`",
             "run `validate\nrecord` then [a](../../docs/design/c/a-design.md) and `y`",
             "a code span wrapped from the line above does not hide the link after it"),
            (".claude/s/x.md", "an open ` tick\n\n[a](../../docs/a-design.md) `x`",
             "an open ` tick\n\n[a](../../docs/design/c/a-design.md) `x`",
             "a blank line closes a paragraph's unpaired backtick"),
            (".claude/s/x.md", "run `validate\n[a](../../docs/a-design.md)` here",
             "run `validate\n[a](../../docs/a-design.md)` here", "a link inside a wrapped span is a mention"),
        ]
        for rel, before, want, why in cases:
            got, _ = rewrite_text(rel, before, mp, rx)
            _check(got == want, f"{why}: {before!r} -> {got!r}" + ("" if got == want else f" (want {want!r})"),
                   failures)
        nd = "docs/a-design.md"
        for body, own, want, why in [
            ("see 3d-models `docs/a-design.md`", True, True, "a sibling line tying the path to 3d-models"),
            ("Design: 3d-models/docs/a-design.md §3", True, True, "a sibling's `3d-models/docs/...`"),
            ("[`docs/a-design.md`](docs/a-design.md), as 3d-models does", True, False,
             "a sibling's own file of the same name, 3d-models named elsewhere on the line"),
            ("`bikar:docs/a-design.md` and `qiyas:docs/a-design.md`", False, False, "a third repo's path"),
            ("per `docs/a-design.md`", False, True, "a bare path the sibling has no file for"),
        ]:
            _check(names_ours(body, nd, own) == want, f"sibling grep: {why}", failures)
        left = leftovers("docs/research/r.md", "from `docs/a-design.md` §3", mp, "research")
        _check(len(left) == 1, "research prose that still names the old place is listed", failures)
        left = leftovers("docs/plan.md", "[a](design/c/a-design.md)", mp, "x")
        _check(not left, "a rewritten link is not listed as left over", failures)
        left = leftovers("docs/plan.md", "`qiyas:docs/a-design.md`", mp, "x")
        _check(not left, "another repo's `qiyas:docs/...` path is not listed as left over", failures)


def copy_repo(src: Path, dst: Path) -> None:
    """Tracked files into a fresh git repo: text and small files copied, large
    ones stubbed (the gates only ask whether they exist)."""
    for rel in tracked(src):
        s, d = src / rel, dst / rel
        if not s.is_file():
            continue
        d.parent.mkdir(parents=True, exist_ok=True)
        if s.stat().st_size < 1_000_000:
            shutil.copy2(s, d)
        else:
            d.write_bytes(b"")
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    for cmd in (["git", "init", "-q", "-b", "master"], ["git", "add", "."],
                ["git", "commit", "-q", "-m", "copy"]):
        subprocess.run(cmd, cwd=dst, check=True, env=env, capture_output=True)


def gate_findings(root: Path) -> tuple[set[str], set[str]]:
    """(docs gate findings, pointer gate violations) for the tree at `root`.

    bikar is an empty folder here. With no bikar at all the pointer gate skips
    an unprefixed path it cannot find (it may be bikar shorthand), which would
    hide a missed `docs/` pointer; an empty bikar makes every such path a miss,
    before the move and after, so only the difference counts."""
    fake = root.parent / "bikar-empty"
    fake.mkdir(exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["BIKAR_DIR"] = str(fake)
    d = subprocess.run([sys.executable, str(root / ".claude/gates/docs_gate.py")], cwd=root,
                       capture_output=True, text=True, env=env)
    docs = {ln for ln in d.stderr.splitlines() if ": D" in ln}
    p = subprocess.run([sys.executable, str(root / ".claude/gates/doc_pointers.py")], cwd=root,
                       capture_output=True, text=True, env=env)
    ptr = {ln.strip() for ln in p.stderr.splitlines() if "resolves to no file" in ln or "GREW" in ln
           or "delete its entry" in ln}
    return docs, ptr


FINDING_AT = re.compile(r"^([^:\s]+):\d+: ")


def as_after(findings: set[str], mapper: Mapper | None = None) -> set[str]:
    """A finding without its line number, its file named where it will be —
    so a finding that was there before the move matches itself after it."""
    out = set()
    for f in findings:
        m = FINDING_AT.match(f)
        if m:
            where = (mapper.map(m.group(1)) if mapper else None) or m.group(1)
            f = where + ": " + f[m.end():]
        out.add(f)
    return out


# The sample note: inbound links from docs and research, its own links, a
# backticked pointer, a baseline entry and a bare feeds: wikilink. Found by
# name, so the self-test still runs after the note itself has moved.
SAMPLE_NAME = "lego-lab-design.md"


def integration(failures: list[str]) -> None:
    """Move a real note in a copy of this repo and ask the real gates."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "repo"
        root.mkdir()
        copy_repo(ROOT, root)
        before_docs, before_ptr = gate_findings(root)
        print(f"self-test: the copy before the move — docs gate {len(before_docs)} finding(s), "
              f"pointer gate {len(before_ptr)} (bikar empty, so its paths all miss)")
        for f in sorted(before_docs):
            print(f"  before: {f}")
        where = next(f for f in tracked(root) if f.startswith("docs/") and posixpath.basename(f) == SAMPLE_NAME)
        dest = f"docs/self-test/deeper/{SAMPLE_NAME}"
        moves, errs = expand(root, [(where, dest)])
        report, texts = plan_run(root, moves, with_siblings=False)
        kinds = {(c.kind, area(rel)) for rel, cs in report.changes.items() for c in cs}
        need = {("link-in", "docs"): "an inbound link", ("link-in", "research"): "a research link",
                ("link-out", "docs"): "the note's own links", ("path", ".claude"): "a backticked pointer",
                ("path", "pointer baseline"): "a baseline key"}
        for k, what in need.items():
            _check(k in kinds, f"the sample move exercises {what}", failures)
        research_feeds = any(f"[[{SAMPLE_NAME[:-3]}]]" in (root / f).read_text(encoding="utf-8")
                             for f in tracked(root) if f.startswith(RESEARCH) and f.endswith(".md"))
        _check(research_feeds, "the sample has a bare feeds: wikilink to follow", failures)
        apply(root, moves, texts)
        mapper = Mapper(root, moves)
        before_docs, before_ptr = as_after(before_docs, mapper), as_after(before_ptr, mapper)
        after_docs, after_ptr = (as_after(x) for x in gate_findings(root))
        _check(after_docs <= before_docs, f"docs gate: no new finding after the move "
               f"({sorted(after_docs - before_docs)[:3]})", failures)
        _check(after_ptr <= before_ptr, f"pointer gate: no new violation after the move "
               f"({sorted(after_ptr - before_ptr)[:3]})", failures)

        # The failure case: put back one link and one pointer the mover fixed.
        link = next((rel, c) for rel, cs in report.changes.items() for c in cs
                    if c.kind == "link-in" and area(rel) == "docs")
        p = root / link[0]
        p.write_text(p.read_text(encoding="utf-8").replace("](" + link[1].after, "](" + link[1].before, 1),
                     encoding="utf-8")
        scanned = (".claude/skills/", ".claude/gates/")  # what the pointer gate reads
        ptr = next((rel, c) for rel, cs in report.changes.items() for c in cs
                   if c.kind == "path" and rel.startswith(scanned) and rel.endswith(".md")
                   and "`" + c.after in (root / rel).read_text(encoding="utf-8"))
        q = root / ptr[0]
        q.write_text(q.read_text(encoding="utf-8").replace("`" + ptr[1].after, "`" + ptr[1].before, 1),
                     encoding="utf-8")
        missed_docs, missed_ptr = (as_after(x) for x in gate_findings(root))
        _check(bool(missed_docs - before_docs), f"docs gate fires on a link the mover missed "
               f"({link[0]}:{link[1].line})", failures)
        _check(bool(missed_ptr - before_ptr), f"pointer gate fires on a pointer the mover missed "
               f"({ptr[0]}:{ptr[1].line})", failures)

        # A name that stops being unique is flagged; the same move without the
        # twin is not.
        again = expand(root, [(dest, f"docs/self-test/{SAMPLE_NAME}")])[0]
        alone, _ = plan_run(root, again, with_siblings=False)
        (root / f"docs/research/{SAMPLE_NAME}").write_text("x\n")
        git(root, "add", f"docs/research/{SAMPLE_NAME}")
        twin, _ = plan_run(root, again, with_siblings=False)
        _check(not alone.collisions and bool(twin.collisions),
               "a bare [[name]] that stops being unique is flagged", failures)


def self_test() -> int:
    failures: list[str] = []
    unit_cases(failures)
    integration(failures)
    print("self-test: " + ("PASS" if not failures else f"FAIL ({len(failures)})"))
    return 0 if not failures else 1


# --- main -----------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="OLD NEW [OLD NEW ...], repo-relative")
    ap.add_argument("--plan", type=Path, help="a file of `old new` lines")
    ap.add_argument("--dry-run", action="store_true", help="report, change nothing")
    ap.add_argument("--no-siblings", action="store_true", help="skip the sibling-repo grep")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if len(args.paths) % 2:
        ap.error("paths come in pairs: OLD NEW")
    pairs = list(zip(args.paths[::2], args.paths[1::2]))
    if args.plan:
        pairs += read_plan(args.plan.read_text(encoding="utf-8"))
    if not pairs:
        ap.error("nothing to move")
    moves, errors = expand(ROOT, pairs)
    if errors:
        print("refused:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 2
    report, texts = plan_run(ROOT, moves, with_siblings=not args.no_siblings)
    print(summary(report, args.dry_run))
    if report.dirty:
        print(("would refuse" if args.dry_run else "refused") +
              ": these have uncommitted changes, and the mover stages what it touches — "
              "commit or set them aside first:\n  " + "\n  ".join(report.dirty), file=sys.stderr)
        if not args.dry_run:
            return 2
    if not args.dry_run:
        apply(ROOT, moves, texts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
