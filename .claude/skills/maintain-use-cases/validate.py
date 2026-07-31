#!/usr/bin/env python3
"""Validate the use-case map in use-cases.md.

Modes:
  validate.py             full validation of the working copy
  validate.py --staged    pre-commit mode (called by .githooks/pre-commit.d/20-use-cases)
  validate.py --refresh   rewrite frontmatter as_of hashes to each repo's HEAD, then validate
  validate.py --self-test run the page-catalog reader's own fixtures

Checks (full mode):
  - frontmatter parses and every as_of hash resolves in its repo
  - every pointer `repo:path:Lstart[-Lend]` names a file that exists at the
    pinned as_of commit and has at least Lend lines
  - the mermaid diagram and the pointer table declare the same UC ids
  - every `uc:` id declared by a frontmatter `page_catalogs` source is a use
    case this map carries (see check_catalogs below)
  - warns when a repo's as_of lags its local HEAD (missing cross-repo
    checkouts are warn-and-skip, never a failure)

Pre-commit mode adds the freshness contract:
  - use-cases.md staged  -> staged content must fully validate AND its
    3d-models as_of must equal HEAD (the commit being built upon)
  - use-cases.md not staged but a staged file is referenced by a 3d-models
    pointer -> BLOCK (override once with USE_CASES_OK=1 git commit ...)
  - staged files touch experience surfaces (index.html, Makefile, docs/,
    src/) -> non-blocking reminder
  - 3d-models as_of more than STALE_LIMIT commits behind HEAD -> reminder
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

import yaml

DOC_RELPATH = ".claude/skills/maintain-use-cases/use-cases.md"
SELF_REPO = "3d-models"
STALE_LIMIT = 20
SURFACE_PATTERNS = (
    re.compile(r"^index\.html$"),
    re.compile(r"^Makefile$"),
    re.compile(r"^docs/.*\.md$"),
    re.compile(r"^src/"),
)
# POINTER_RE and UC_RE are intentionally regexes: they match *tokens embedded in
# prose* (a code-span pointer inside a table cell, a UC id inside a diagram
# label), which is regex's proper job. They are not standing in for a parser —
# the document's structure (frontmatter, code fences) is read structurally
# below. Do not "fix" these into a parser.
POINTER_RE = re.compile(r"`(?P<repo>[\w.-]+):(?P<path>[^`\s:]+):L(?P<start>\d+)(?:-L(?P<end>\d+))?`")
UC_RE = re.compile(r"\bUC\d+\b")
# A `uc:` field in a page catalog — `{ uc: 'UC5', actor: 'lab-visitor', ... }`.
# Same justification as POINTER_RE: a token embedded in a source file this repo
# does not own and cannot import. Comment lines are dropped before matching, so
# a UC id quoted in prose above the data does not become a claim.
CATALOG_UC_RE = re.compile(r"\buc:\s*['\"](UC\d+)['\"]")
CATALOG_SPEC_RE = re.compile(r"^(?P<repo>[\w.-]+):(?P<path>\S+)$")


def run_git(repo_dir: str, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", repo_dir, *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def try_git(repo_dir: str, *args: str) -> str | None:
    try:
        return run_git(repo_dir, *args)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def split_frontmatter(text: str) -> tuple[str, str]:
    """Split a `---` fenced frontmatter block from the body.

    Structural, and fails closed: an absent opening fence or an unterminated
    block is an error, never an empty frontmatter that silently validates.
    """
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        raise ValueError(f"{DOC_RELPATH}: missing frontmatter block")
    for i in range(1, len(lines)):
        if lines[i] == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1 :])
    raise ValueError(f"{DOC_RELPATH}: frontmatter block is never closed by '---'")


def fence_marker(line: str) -> tuple[int, str] | None:
    """(backtick-run length, info string) if `line` is a code fence, else None."""
    s = line.strip()
    if not s.startswith("```"):
        return None
    ticks = len(s) - len(s.lstrip("`"))
    return ticks, s[ticks:].strip()


def fenced_blocks(body: str) -> list[tuple[str, str]]:
    """Walk the body's code fences, returning (info string, block text) pairs.

    Tracks fence open/close as structure rather than pattern-matching the body,
    so a ``` inside a block cannot be mistaken for a block of its own, and an
    unclosed fence is reported instead of quietly swallowing the rest of the doc.
    """
    blocks: list[tuple[str, str]] = []
    open_ticks: int | None = None
    info = ""
    buf: list[str] = []
    for line in body.split("\n"):
        marker = fence_marker(line)
        if open_ticks is None:
            if marker and "`" not in marker[1]:
                open_ticks, info, buf = marker[0], marker[1], []
            continue
        if marker and marker[1] == "" and marker[0] >= open_ticks:
            blocks.append((info, "\n".join(buf)))
            open_ticks = None
            continue
        buf.append(line)
    if open_ticks is not None:
        raise ValueError(f"{DOC_RELPATH}: unclosed '```{info}' code fence in the body")
    return blocks


def string_map(meta: dict, key: str, what: str) -> dict[str, str]:
    """Read `key` from the frontmatter as a mapping of name -> string.

    Every failure mode is an error: absent key, wrong type, or a value YAML
    resolved to something other than a string (an all-digit hash becomes an int,
    a bare date becomes a date). A value this reader cannot interpret is never
    skipped — that is what made a malformed pin look like a missing one.
    """
    if key not in meta:
        raise ValueError(f"{DOC_RELPATH}: frontmatter has no '{key}' mapping")
    section = meta[key]
    if not isinstance(section, dict):
        raise ValueError(f"{DOC_RELPATH}: frontmatter '{key}' is not a mapping (got {type(section).__name__})")
    out: dict[str, str] = {}
    for name, value in section.items():
        if not isinstance(name, str):
            raise ValueError(f"{DOC_RELPATH}: frontmatter '{key}' has a non-string key {name!r}")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{DOC_RELPATH}: frontmatter {key}.{name} is not a {what} "
                f"({value!r}) — quote it if YAML read it as a number or date"
            )
        out[name] = value.strip()
    return out


def string_specs(meta: dict, key: str) -> list[tuple[str, str]]:
    """Read an optional `key` as a list of `repo:path` strings.

    Absent is fine — a map with no page catalog to check is a legitimate state,
    and was the only state before `studio.html` existed. Present-but-malformed
    is not: a list that holds a dict, or an entry that is not `repo:path`, is an
    error rather than an entry that quietly drops out of the check.
    """
    if key not in meta:
        return []
    section = meta[key]
    if not isinstance(section, list):
        raise ValueError(f"{DOC_RELPATH}: frontmatter '{key}' is not a list (got {type(section).__name__})")
    out: list[tuple[str, str]] = []
    for entry in section:
        if not isinstance(entry, str):
            raise ValueError(f"{DOC_RELPATH}: frontmatter '{key}' entry {entry!r} is not a string")
        m = CATALOG_SPEC_RE.match(entry.strip())
        if not m:
            raise ValueError(f"{DOC_RELPATH}: frontmatter '{key}' entry {entry!r} is not 'repo:path'")
        out.append((m.group("repo"), m.group("path")))
    return out


def catalog_ucs(blob: str) -> set[str]:
    """The UC ids a page catalog claims, read off its `uc:` fields.

    Comment lines are dropped first. The catalog's own header explains the
    contract in prose and names example ids while doing it; counting those as
    claims would demand map entries for illustrations.
    """
    ids: set[str] = set()
    for line in blob.split("\n"):
        s = line.lstrip()
        if s.startswith(("*", "//", "/*")):
            continue
        ids.update(CATALOG_UC_RE.findall(line))
    return ids


class Doc:
    def __init__(self, text: str):
        frontmatter, body = split_frontmatter(text)
        try:
            meta = yaml.safe_load(frontmatter)
        except yaml.YAMLError as exc:
            detail = " ".join(str(exc).split())
            raise ValueError(f"{DOC_RELPATH}: frontmatter is not valid YAML: {detail}") from exc
        if not isinstance(meta, dict):
            raise ValueError(
                f"{DOC_RELPATH}: frontmatter is not a YAML mapping (got {type(meta).__name__})"
            )
        self.as_of: dict[str, str] = string_map(meta, "as_of", "commit hash")
        self.repos: dict[str, str] = string_map(meta, "repos", "repo path")
        self.catalogs: list[tuple[str, str]] = string_specs(meta, "page_catalogs")
        if SELF_REPO not in self.as_of:
            raise ValueError(f"{DOC_RELPATH}: frontmatter as_of is missing '{SELF_REPO}'")
        diagrams = [text for info, text in fenced_blocks(body) if info == "mermaid"]
        if not diagrams:
            raise ValueError(f"{DOC_RELPATH}: no mermaid diagram found")
        self.diagram_ucs = set(UC_RE.findall(diagrams[0]))
        self.table_ucs: set[str] = set()
        self.pointers: list[tuple[str, str, int, int]] = []
        for line in body.splitlines():
            if not line.startswith("| UC"):
                continue
            uc = UC_RE.match(line[2:])
            if uc:
                self.table_ucs.add(uc.group(0))
            for p in POINTER_RE.finditer(line):
                start = int(p.group("start"))
                end = int(p.group("end") or start)
                self.pointers.append((p.group("repo"), p.group("path"), start, end))

    def repo_dir(self, repo: str, root: str) -> str | None:
        if repo == SELF_REPO:
            return root
        rel = self.repos.get(repo)
        if rel is None:
            return None
        d = os.path.normpath(os.path.join(root, rel))
        return d if os.path.isdir(os.path.join(d, ".git")) else None


def unknown_catalog_ucs(claimed: set[str], carried: set[str]) -> list[str]:
    """Ids a catalog claims that the map does not carry, in id order."""
    return sorted(claimed - carried, key=lambda u: int(u[2:]))


def check_catalogs(doc: Doc, root: str) -> tuple[list[str], list[str]]:
    """Hold each declared page catalog to the ids this map actually carries.

    A page catalog (bikar's `packages/lab/src/catalog.ts`) is what the studio
    index renders itself from, and it names a use case per actor per page. This
    map is the register of what the system does for whom, so the catalog may
    *point into* it and may not invent entries in it: a page that advertises
    UC16 before UC16 exists here is a page making a promise nothing delivers.

    Read at the pinned `as_of`, like every other cross-repo read in this file,
    and warn-and-skip on an absent checkout or an absent file for the same
    reason — a pin that predates the catalog is a stale pin, not a defect in
    the catalog, and failing on it would make `--refresh` the only way to
    commit anything.
    """
    errors: list[str] = []
    warnings: list[str] = []
    for repo, path in doc.catalogs:
        pin = doc.as_of.get(repo)
        if pin is None:
            errors.append(f"page_catalogs names repo '{repo}' but frontmatter as_of has no hash for it")
            continue
        rdir = doc.repo_dir(repo, root)
        if rdir is None:
            warnings.append(f"repo '{repo}' not checked out locally — skipped its page-catalog check")
            continue
        blob = try_git(rdir, "cat-file", "-p", f"{pin}:{path}")
        if blob is None:
            warnings.append(
                f"page catalog {repo}:{path} does not exist at as_of {pin[:12]} — "
                "skipped; re-pin once that checkout carries it"
            )
            continue
        claimed = catalog_ucs(blob)
        if not claimed:
            # Fail closed. A catalog that parses to nothing is indistinguishable
            # from a catalog this reader no longer understands, and the second
            # would otherwise pass silently forever.
            errors.append(
                f"page catalog {repo}:{path} declares no `uc:` ids at as_of {pin[:12]} — "
                "the reader found nothing to check (did the catalog's shape change?)"
            )
            continue
        for uc in unknown_catalog_ucs(claimed, doc.table_ucs):
            errors.append(
                f"page catalog {repo}:{path} claims {uc}, which this map does not carry — "
                f"add {uc} to the diagram and the table, or stop claiming it on the page"
            )
    return errors, warnings


def staleness_warning(repo: str, behind: int | None, ahead: int | None) -> str | None:
    """Say whether a pin that differs from its checkout's HEAD is actually stale.

    `behind` counts `pin..HEAD` and `ahead` counts `HEAD..pin`. They are not
    opposites: a pin can be both (a divergence) or neither-but-unequal is
    impossible once both resolve.

    The case that forced this to be a function rather than an inline `!=` is a
    **sibling checkout that is not the one doing the work**. bikar's pointers
    are read out of `../bikar`, but its branches are built in a worktree, and
    worktrees share one object database — so `origin/main` can be pinned here
    and read here while `../bikar`'s own HEAD sits on an older commit that
    belongs to another session. That pin is ahead, not behind, and there is
    nothing to re-pin. Warning "0 commit(s) behind" on it was both false and
    unactionable, which is the shape of a warning that gets ignored.
    """
    if behind is None:
        return f"'{repo}' as_of does not share history with its local HEAD — check the pin"
    if behind == 0:
        return None
    if repo == SELF_REPO and behind <= STALE_LIMIT:
        # The self pin is always >= 1 behind once the map-commit lands
        # (as_of records that commit's parent) — only nag past the limit.
        return None
    tail = f", {ahead} ahead" if ahead else ""
    return f"'{repo}' as_of is {behind} commit(s) behind its local HEAD{tail}"


def validate_full(doc: Doc, root: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if doc.diagram_ucs != doc.table_ucs:
        only_d = ", ".join(sorted(doc.diagram_ucs - doc.table_ucs)) or "-"
        only_t = ", ".join(sorted(doc.table_ucs - doc.diagram_ucs)) or "-"
        errors.append(f"diagram/table mismatch: diagram-only [{only_d}], table-only [{only_t}]")
    pointer_repos = {p[0] for p in doc.pointers}
    for repo in sorted(pointer_repos - set(doc.as_of)):
        errors.append(f"pointers reference repo '{repo}' but frontmatter as_of has no hash for it")
    for repo, pin in doc.as_of.items():
        rdir = doc.repo_dir(repo, root)
        if rdir is None:
            warnings.append(f"repo '{repo}' not checked out locally — skipped its pointer checks")
            continue
        if try_git(rdir, "cat-file", "-e", f"{pin}^{{commit}}") is None:
            errors.append(f"as_of hash for '{repo}' ({pin[:12]}) does not resolve in {rdir}")
            continue
        head = try_git(rdir, "rev-parse", "HEAD")
        if head and head != pin:
            behind = try_git(rdir, "rev-list", "--count", f"{pin}..{head}")
            ahead = try_git(rdir, "rev-list", "--count", f"{head}..{pin}")
            warning = staleness_warning(
                repo,
                int(behind) if behind is not None else None,
                int(ahead) if ahead is not None else None,
            )
            if warning:
                warnings.append(warning)
        for prepo, path, start, end in doc.pointers:
            if prepo != repo:
                continue
            blob = try_git(rdir, "cat-file", "-p", f"{pin}:{path}")
            if blob is None:
                errors.append(f"{prepo}:{path} does not exist at as_of {pin[:12]}")
                continue
            nlines = blob.count("\n") + 1
            if end > nlines:
                errors.append(f"{prepo}:{path}:L{start}-L{end} exceeds file length {nlines} at as_of {pin[:12]}")
    cat_errors, cat_warnings = check_catalogs(doc, root)
    return errors + cat_errors, warnings + cat_warnings


def report(errors: list[str], warnings: list[str], context: str) -> int:
    for w in warnings:
        print(f"use-cases [{context}] warning: {w}", file=sys.stderr)
    for e in errors:
        print(f"use-cases [{context}] ERROR: {e}", file=sys.stderr)
    return 1 if errors else 0


def mode_full(root: str) -> int:
    with open(os.path.join(root, DOC_RELPATH), encoding="utf-8") as f:
        doc = Doc(f.read())
    rc = report(*validate_full(doc, root), context="full")
    if rc == 0:
        print(f"use-cases: {len(doc.table_ucs)} use cases, {len(doc.pointers)} pointers — all valid at pinned commits")
    return rc


def mode_refresh(root: str) -> int:
    path = os.path.join(root, DOC_RELPATH)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    doc = Doc(text)
    for repo, pin in doc.as_of.items():
        rdir = doc.repo_dir(repo, root)
        head = try_git(rdir, "rev-parse", "HEAD") if rdir else None
        if head is None:
            print(f"use-cases refresh: '{repo}' not available — pin kept at {pin[:12]}", file=sys.stderr)
        elif head != pin:
            # Fail closed: `pin` came back through yaml.safe_load, so it has lost
            # whatever quoting the file used. A raw replace that finds nothing
            # would silently leave the pin stale and still report success — the
            # same skip-what-you-can't-read shape this reader was fixed to end.
            updated = text.replace(f"{repo}: {pin}", f"{repo}: {head}")
            if updated == text:
                raise ValueError(
                    f"{DOC_RELPATH}: could not rewrite the '{repo}' pin in place — "
                    f"as_of.{repo} parsed as {pin!r} but no line reads '{repo}: {pin}' "
                    f"(is it quoted, or on a folded line?). Update it by hand."
                )
            text = updated
            print(f"use-cases refresh: {repo} {pin[:12]} -> {head[:12]}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return mode_full(root)


def mode_staged(root: str) -> int:
    staged = [f for f in run_git(root, "diff", "--cached", "--name-only").splitlines() if f]
    head = try_git(root, "rev-parse", "HEAD")
    if DOC_RELPATH in staged:
        doc = Doc(run_git(root, "show", f":{DOC_RELPATH}"))
        errors, warnings = validate_full(doc, root)
        if head and doc.as_of.get(SELF_REPO) != head:
            errors.append(
                f"staged {SELF_REPO} as_of {doc.as_of.get(SELF_REPO, '?')[:12]} != HEAD {head[:12]} — "
                f"run .claude/skills/maintain-use-cases/validate.py --refresh and restage"
            )
        return report(errors, warnings, context="pre-commit")
    try:
        doc = Doc(run_git(root, "show", f"HEAD:{DOC_RELPATH}"))
    except subprocess.CalledProcessError:
        return 0  # map not committed yet — nothing to guard
    referenced = {path for repo, path, _, _ in doc.pointers if repo == SELF_REPO}
    hits = sorted(referenced & set(staged))
    if hits:
        if os.environ.get("USE_CASES_OK") == "1":
            print(f"use-cases: override accepted for pointer-referenced files: {', '.join(hits)}", file=sys.stderr)
        else:
            print(
                "use-cases BLOCK: staged files are referenced by the use-case map "
                f"({', '.join(hits)}) but {DOC_RELPATH} is not staged.\n"
                "  Update the map + run validate.py --refresh, stage it, and retry —\n"
                "  or override once with: USE_CASES_OK=1 git commit ...",
                file=sys.stderr,
            )
            return 1
    elif any(p.match(f) for f in staged for p in SURFACE_PATTERNS):
        print(
            "use-cases reminder: this commit touches experience surfaces — if it adds or "
            f"changes a user-facing capability, update {DOC_RELPATH} (skill: maintain-use-cases).",
            file=sys.stderr,
        )
    pin = doc.as_of.get(SELF_REPO)
    if head and pin:
        behind = try_git(root, "rev-list", "--count", f"{pin}..{head}")
        if behind is None or int(behind) > STALE_LIMIT:
            print(
                f"use-cases reminder: the map's as_of is {behind or 'unknown-count'} commits behind HEAD — "
                "consider validate.py --refresh in a follow-up commit.",
            file=sys.stderr,
            )
    return 0


SELF_TEST_CATALOG = """/**
 * A page catalog header, which explains the contract in prose and names an
 * example while doing it: uc: 'UC99' is an illustration, not a claim.
 */
export const PAGES = [
  { id: 'studio', file: 'studio.html', useCases: [] },
  { id: 'lab', file: 'lab.html', useCases: [
    { uc: 'UC5', actor: 'lab-visitor', does: '...' },
    { uc: "UC4", actor: 'print-operator', does: '...' },
  ] },
];
"""


def self_test() -> int:
    """The page-catalog reader's fixtures — the check that fires on a real file.

    `check_catalogs` needs two checkouts and a pinned commit to run, so the part
    worth pinning is the part that decides: what the reader extracts, and what
    it calls unknown. Both are pure functions and both are exercised here.
    """
    ok = True

    def expect(name: str, got: object, want: object) -> None:
        nonlocal ok
        if got == want:
            print(f"self-test ok: {name}")
        else:
            ok = False
            print(f"self-test FAIL: {name} — got {got!r}, want {want!r}")

    expect(
        "reads uc ids in either quote style",
        catalog_ucs(SELF_TEST_CATALOG),
        {"UC5", "UC4"},
    )
    expect(
        "does not read a UC id out of a comment",
        "UC99" in catalog_ucs(SELF_TEST_CATALOG),
        False,
    )
    expect(
        "a catalog with no useCases yields nothing to check",
        catalog_ucs("export const PAGES = [];\n"),
        set(),
    )
    expect(
        "reports an id the map does not carry",
        unknown_catalog_ucs({"UC5", "UC16"}, {"UC4", "UC5"}),
        ["UC16"],
    )
    expect(
        "reports nothing when every claim is carried",
        unknown_catalog_ucs({"UC5", "UC4"}, {"UC4", "UC5", "UC16"}),
        [],
    )
    expect(
        "orders unknown ids numerically, not lexically",
        unknown_catalog_ucs({"UC16", "UC9"}, set()),
        ["UC9", "UC16"],
    )
    expect(
        "a pin ahead of a sibling checkout's HEAD is not stale",
        staleness_warning("bikar", 0, 2),
        None,
    )
    expect(
        "a pin genuinely behind its checkout still warns, and says how far ahead",
        staleness_warning("bikar", 3, 1),
        "'bikar' as_of is 3 commit(s) behind its local HEAD, 1 ahead",
    )
    expect(
        "the self pin's own map-commit offset stays quiet",
        staleness_warning(SELF_REPO, 1, 0),
        None,
    )
    expect(
        "the self pin past the limit does not",
        staleness_warning(SELF_REPO, STALE_LIMIT + 1, 0),
        f"'{SELF_REPO}' as_of is {STALE_LIMIT + 1} commit(s) behind its local HEAD",
    )
    expect(
        "an unrelated pin is reported as unrelated, not as a count",
        staleness_warning("bikar", None, None),
        "'bikar' as_of does not share history with its local HEAD — check the pin",
    )
    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    root = run_git(os.path.dirname(os.path.abspath(__file__)), "rev-parse", "--show-toplevel")
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    context = {"--staged": "pre-commit", "--refresh": "refresh"}.get(mode, "full")
    try:
        if mode == "--self-test":
            return self_test()
        if mode == "--staged":
            return mode_staged(root)
        if mode == "--refresh":
            return mode_refresh(root)
        return mode_full(root)
    except ValueError as exc:
        # An unreadable document is a failure, not a skip — report it in the
        # same voice as every other error and exit non-zero.
        return report([str(exc)], [], context=context)


if __name__ == "__main__":
    sys.exit(main())
