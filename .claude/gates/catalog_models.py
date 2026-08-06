#!/usr/bin/env python3
"""Hold each prototype-catalog entry to the model file it prescribes.

A catalog entry is a set of instructions for standing at a printer. It names a
`.bkr` and then names knobs to turn — `--param engage=3.2`, `--piece
CouponAnchorPlate`, `--brick-fit ribMm=0.10`. Each of those names is a claim
about that file, and each is silently falsifiable: the model gains a param,
loses a piece, renames a field, and the entry still *reads* fine.

WHY THIS IS A GATE AND NOT A PARAGRAPH. Two instances, both in this catalog,
both costing real time before anyone noticed:

  * **W-F1** named a model file, `Fit-Step-Gauge.bkr`, that had never existed
    under that name, and described the wrong joint besides. Three documents
    disagreed about what the coupon was. Resolved in `docs/decisions-log.md`
    D-008 — after a full re-derivation, not a lookup.
  * **LG-F1** prescribed `--param rib_mm=…`. The catalog still says it: "a knob
    that never existed." Rib thickness is not a `param` at all — no `brick`
    statement reads one — it is a `brickFit` offset reached by `--brick-fit`.

Neither is caught by `docs_gate.py` (which checks links, validators and
defaults) nor by `doc_pointers.py` (which checks that paths resolve — it would
have caught W-F1's filename, and does now, but a *param* name is not a path).

DIVISION OF LABOUR WITH `doc_pointers.py`. That gate owns the question *does
this file exist*. This one owns *does this entry's vocabulary match that file*.
So an entry whose model is marked to-author — LG-B2's `Rosette-Brick.bkr` — is
reported here as `pending`, never as a violation: its existence claim is
already grandfathered over there with a reason, and duplicating the finding
would mean two gates to satisfy for one fix.

K10 — WHAT THIS GATE ASSUMES ABOUT BIKAR'S SOURCE, AND WHAT IT DOES NOT.
It reads three things out of a repo it does not own:

  * `param <name>` lines in a `.bkr` — the DSL's own declaration syntax.
  * which keywords open a declaration, from the `XDecl = "kw" …` productions in
    bikar's `docs/grammar.md`. **Not** a hand-written list: the first run of
    this gate carried one, it omitted `clip`, and it duly reported W-F1's
    `--piece FitClipC40` and W-C1's `--piece CouponClip` as undeclared when both
    are `clip` declarations. bikar's own G3 conformance test holds grammar.md to
    what the parser dispatches on, so harvesting is the read that stays true.
  * the field names of `interface BrickFit` in
    `packages/core/src/kernel3d/lego.ts`, by regex over a flat list of
    `readonly <name>: number;` lines.

The last two are the fragile ones, so they fail **loud, not open**: if the
interface or the productions cannot be read, or parse to implausibly few
entries, the affected flag goes unchecked and the summary says which and why. A
gate that silently stops checking is worse than one that never did.

What is deliberately NOT checked: values. Whether `engage=3.2` is inside the
`range 1.6..8.0` the model declares is bikar's business — its CLI validates
overrides against declared ranges, and re-implementing that here would be a
second, drifting copy of somebody else's rule.

Usage:
    python3 .claude/gates/catalog_models.py            # check; non-zero on a violation
    python3 .claude/gates/catalog_models.py --list     # every claim and its verdict
    python3 .claude/gates/catalog_models.py --self-test

Env:
    BIKAR_DIR                       where bikar is checked out (Makefile passes it)
    CATALOG_MODELS_OK=1             skip entirely (the hook honours it)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from doc_pointers import _git_env, _sibling_root, _tracked_at_ref  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CATALOG_REL = ".claude/skills/prototype/catalog.md"
BASELINE_REL = ".claude/gates/catalog-model-baseline.json"
LEGO_TS_REL = "packages/core/src/kernel3d/lego.ts"

#: `## W-F1 — Clipseat fit coupon (blade clearance ladder)` → `W-F1`.
ENTRY = re.compile(r"^## ([A-Z]+-?[A-Z]?\d+)\b")
#: The bullet that names the model. `(to author)` and other asides may follow.
MODEL_BULLET = re.compile(r"^- \*\*Model\*\*")
NEXT_BULLET = re.compile(r"^- \*\*")
#: A repo path, so a `/` is required. Without it the Model bullet's prose picks
#: up bare filenames the entry only *mentions* — P1 says "no baked `.bkr`
#: needed" and W-F1 names `Fit-Coupon.bkr` in the sentence disowning it. Both
#: would then read as unreadable models and push the entry to `pending`,
#: silently dropping the claims the gate exists to check.
BACKTICK_SPAN = re.compile(r"`([^`]*)`")
#: A repo path, so a `/` is required. Without it the Model bullet's prose picks
#: up bare filenames the entry only *mentions* — P1 says "no baked `.bkr`
#: needed" and W-F1 names `Fit-Coupon.bkr` in the sentence disowning it. Both
#: would then read as unreadable models and push the entry to `pending`,
#: silently dropping the claims the gate exists to check.
#:
#: Matched *inside* a span rather than against the whole span, because a model
#: path is as often embedded in a render command as quoted on its own — P1's
#: only mention is mid-`cd bikar && … render patterns/Orbs/Star-Orb.bkr …`.
BKR = re.compile(r"([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\.bkr)\b")

#: Every knob a catalog entry can prescribe, and what declares it in the model.
FLAG = re.compile(r"--(param|piece|brick-fit)\s+([A-Za-z_][A-Za-z0-9_]*)")
DECL_PARAM = re.compile(r"^\s*param\s+([A-Za-z_][A-Za-z0-9_]*)", re.M)
#: `ClipDecl = "clip" IDENT "for" …` in bikar's docs/grammar.md — the keyword
#: that opens each declaration, harvested rather than listed here. Hardcoding
#: the list is what made this gate's first run report `--piece FitClipC40` and
#: `--piece CouponClip` as undeclared: both are `clip` declarations, and `clip`
#: was not in the hand-written set. bikar's own G3 conformance test holds
#: grammar.md to what the parser dispatches on, so harvesting is the honest read.
GRAMMAR_MD_REL = "docs/grammar.md"
DECL_HEAD = re.compile(r'^[A-Za-z]+Decl\s*=\s*"([a-z]+)"', re.M)
#: `param` is the other category — a knob, not a thing `--piece` can render.
DECL_NOT_A_PIECE = frozenset({"param"})
#: A flat `readonly name: number;` line inside `interface BrickFit { … }`.
BRICKFIT_BLOCK = re.compile(r"export interface BrickFit \{(.*?)\n\}", re.S)
BRICKFIT_FIELD = re.compile(r"^\s*readonly\s+([A-Za-z_][A-Za-z0-9_]*)\s*:", re.M)
#: `provenance` is metadata about the other fields, not an offset a coupon turns.
BRICKFIT_NOT_A_KNOB = frozenset({"provenance"})


class Claim:
    """One knob a catalog entry prescribes, located well enough to report."""

    __slots__ = ("entry", "line", "flag", "name")

    def __init__(self, entry: str, line: int, flag: str, name: str) -> None:
        self.entry = entry
        self.line = line
        self.flag = flag
        self.name = name


class Entry:
    """One `## ID` section: the models it names and the knobs it turns."""

    __slots__ = ("id", "line", "models", "claims")

    def __init__(self, id_: str, line: int) -> None:
        self.id = id_
        self.line = line
        self.models: list[str] = []
        self.claims: list[Claim] = []


def parse_catalog(text: str) -> list[Entry]:
    """Split the catalog into entries, each with its model files and its knobs.

    Models come from the `**Model**` bullet ONLY, not from anywhere in the
    section. W-F1 is the reason: it names `Clipseat-Fit-Coupon.bkr` as its model
    and then spends a paragraph on `Fit-Coupon.bkr` explaining that it is *not*
    the same coupon. Scanning the whole section would let a param declared in
    the file the entry disowns satisfy a claim about the file it uses.
    """
    entries: list[Entry] = []
    lines = text.split("\n")
    cur: Entry | None = None
    bullet: list[str] = []
    in_model = False

    def flush() -> None:
        # The bullet's lines are joined before matching: a backtick span may run
        # across a markdown line wrap. P1's model path sits mid-span that way,
        # and matching line-by-line saw unbalanced backticks and no model at all
        # — the entry went `pending` and its claims went unchecked in silence.
        if cur is not None and bullet:
            for span in BACKTICK_SPAN.findall(" ".join(bullet)):
                cur.models.extend(p for p in BKR.findall(span) if "/" in p)
        bullet.clear()

    for i, line in enumerate(lines, 1):
        m = ENTRY.match(line)
        if m:
            flush()
            cur = Entry(m.group(1), i)
            entries.append(cur)
            in_model = False
            continue
        if cur is None:
            continue
        if MODEL_BULLET.match(line):
            in_model = True
        elif NEXT_BULLET.match(line):
            flush()
            in_model = False
        if in_model:
            bullet.append(line)
        for fm in FLAG.finditer(line):
            cur.claims.append(Claim(cur.id, i, fm.group(1), fm.group(2)))
    flush()
    return entries


def declaration_keywords(root: Path = ROOT) -> tuple[frozenset[str], str | None]:
    """The keywords that open a declaration in the DSL, harvested from bikar.

    Returns `(keywords, reason_unavailable)`. Same fail-loud contract as
    `brickfit_fields`: if grammar.md cannot be read or yields an implausibly
    small set, `--piece` goes unchecked *and the output says so*.
    """
    src = read_from_bikar(GRAMMAR_MD_REL, root)
    if src is None:
        return frozenset(), f"bikar's {GRAMMAR_MD_REL} could not be read"
    kws = frozenset(DECL_HEAD.findall(src)) - DECL_NOT_A_PIECE
    if len(kws) < 6:
        return frozenset(), (
            f"{GRAMMAR_MD_REL} yielded only {len(kws)} declaration keyword(s) — "
            "its `XDecl = \"kw\"` productions have changed shape"
        )
    return kws, None


def read_from_bikar(rel: str, root: Path = ROOT) -> str | None:
    """A file's text from the bikar checkout, or None when it is not there.

    Working tree first, then `origin/HEAD` — the same order and the same reason
    as `doc_pointers._exists_in_sibling`: a verdict must not depend on which
    branch a parallel session has checked out.
    """
    bikar = _sibling_root("bikar", root)
    if bikar is None:
        return None
    p = bikar / rel
    if p.is_file():
        return p.read_text(encoding="utf-8")
    import subprocess

    for ref in ("origin/HEAD", "origin/main", "origin/master", "HEAD"):
        tree = _tracked_at_ref(bikar, ref)
        if tree is None or rel not in tree:
            continue
        try:
            return subprocess.run(
                ["git", "-C", str(bikar), "show", f"{ref}:{rel}"],
                capture_output=True,
                text=True,
                check=True,
                env=_git_env(),
            ).stdout
        except subprocess.CalledProcessError:
            continue
    return None


def brickfit_fields(root: Path = ROOT) -> tuple[frozenset[str], str | None]:
    """The knobs `--brick-fit` can set, or an explanation of why we do not know.

    Returns `(fields, reason_unavailable)`. A non-None reason means
    `--brick-fit` claims go UNCHECKED and the caller must say so out loud; see
    the K10 note in the module docstring.
    """
    src = read_from_bikar(LEGO_TS_REL, root)
    if src is None:
        return frozenset(), f"bikar's {LEGO_TS_REL} could not be read"
    block = BRICKFIT_BLOCK.search(src)
    if not block:
        return frozenset(), f"no `export interface BrickFit` found in {LEGO_TS_REL}"
    fields = frozenset(BRICKFIT_FIELD.findall(block.group(1))) - BRICKFIT_NOT_A_KNOB
    if len(fields) < 4:
        return frozenset(), (
            f"`interface BrickFit` in {LEGO_TS_REL} parsed to only {len(fields)} field(s) — "
            "its shape has changed and this gate's regex no longer reads it"
        )
    return fields, None


def declared_in(
    models: list[str], decl_kws: frozenset[str], root: Path = ROOT
) -> tuple[set[str], set[str], list[str]]:
    """(params, pieces, models that could not be read) across an entry's models."""
    params: set[str] = set()
    pieces: set[str] = set()
    missing: list[str] = []
    decl = re.compile(
        r"^\s*(?:" + "|".join(sorted(decl_kws)) + r")\s+([A-Za-z_][A-Za-z0-9_]*)", re.M
    ) if decl_kws else None
    for model in models:
        rel = model[len("bikar/"):] if model.startswith("bikar/") else model
        src = read_from_bikar(rel, root)
        if src is None:
            missing.append(model)
            continue
        params.update(DECL_PARAM.findall(src))
        if decl is not None:
            pieces.update(decl.findall(src))
    return params, pieces, missing


# --- baseline -------------------------------------------------------------


def read_baseline(text: str, label: str) -> list[dict[str, str]]:
    """Parse the baseline, failing closed on every shape it does not match."""
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as e:
        raise SystemExit(f"{label}: not valid JSON — {e}")
    if not isinstance(parsed, dict) or not isinstance(parsed.get("undeclared"), list):
        raise SystemExit(f'{label}: expected an object with an "undeclared" array')
    for e in parsed["undeclared"]:
        if not isinstance(e, dict) or not all(isinstance(e.get(k), str) for k in ("entry", "flag", "name")):
            raise SystemExit(f'{label}: every entry needs string "entry", "flag" and "name" — got {e!r}')
    return parsed["undeclared"]


# --- run ------------------------------------------------------------------


def run(root: Path, list_all: bool) -> tuple[list[str], list[str]]:
    """Check the catalog. Returns (violations, summary lines)."""
    catalog = root / CATALOG_REL
    if not catalog.is_file():
        return [], [f"catalog models: no {CATALOG_REL} in this worktree — skipping"]
    entries = parse_catalog(catalog.read_text(encoding="utf-8"))
    fit_fields, fit_reason = brickfit_fields(root)
    decl_kws, decl_reason = declaration_keywords(root)

    baseline_path = root / BASELINE_REL
    baseline = (
        read_baseline(baseline_path.read_text(encoding="utf-8"), BASELINE_REL)
        if baseline_path.exists()
        else []
    )
    excused = {(e["entry"], e["flag"], e["name"]) for e in baseline}

    violations: list[str] = []
    checked = pending = grandfathered = unchecked = 0
    pending_entries: list[str] = []

    for entry in entries:
        if not entry.claims:
            continue
        params, pieces, missing = declared_in(entry.models, decl_kws, root)
        if not entry.models or missing:
            # The model is to-author or unreadable. `doc_pointers.py` owns that
            # claim; reporting it again here would mean two gates for one fix.
            pending += len(entry.claims)
            what = ", ".join(missing) if missing else "no model file named"
            pending_entries.append(f"{entry.id} ({what})")
            if list_all:
                for c in entry.claims:
                    print(f"pend {CATALOG_REL}:{c.line}  {c.entry} --{c.flag} {c.name}")
            continue

        for c in entry.claims:
            if (c.entry, c.flag, c.name) in excused:
                grandfathered += 1
                verdict, detail = "base", "grandfathered"
            elif c.flag == "param":
                ok = c.name in params
                checked += 1
                verdict, detail = ("ok  ", "declared") if ok else ("MISS", "no `param` declares it")
            elif c.flag == "piece":
                if decl_reason is not None:
                    unchecked += 1
                    verdict, detail = "skip", "declaration keywords unavailable"
                else:
                    ok = c.name in pieces
                    checked += 1
                    verdict, detail = ("ok  ", "declared") if ok else (
                        "MISS", "no declaration in the model gives it that name"
                    )
            else:  # brick-fit
                if fit_reason is not None:
                    unchecked += 1
                    verdict, detail = "skip", "BrickFit field set unavailable"
                else:
                    ok = c.name in fit_fields
                    checked += 1
                    verdict, detail = ("ok  ", "a BrickFit field") if ok else ("MISS", "not a BrickFit field")
            if list_all:
                print(f"{verdict} {CATALOG_REL}:{c.line}  {c.entry} --{c.flag} {c.name}   [{detail}]")
            if verdict == "MISS":
                where = ", ".join(entry.models) if c.flag != "brick-fit" else LEGO_TS_REL
                violations.append(
                    f"{CATALOG_REL}:{c.line}: {c.entry} prescribes `--{c.flag} {c.name}` — {detail}"
                    f" in {where}.\n"
                    f"    Fix the entry, fix the model, or — if the entry names it deliberately,"
                    f" as LG-F1 does —\n"
                    f"    record it in {BASELINE_REL} with:\n"
                    f'      {{ "entry": {json.dumps(c.entry)}, "flag": {json.dumps(c.flag)},'
                    f' "name": {json.dumps(c.name)}, "why": "…" }}'
                )

    summary = [
        f"catalog models: {len(entries)} entries; {checked} claim(s) checked, "
        f"{grandfathered} grandfathered, {pending} pending a to-author model"
    ]
    if pending_entries:
        summary.append("  pending: " + "; ".join(pending_entries))
    if fit_reason is not None:
        summary.append(f"  --brick-fit UNCHECKED: {fit_reason}")
    if decl_reason is not None:
        summary.append(f"  --piece UNCHECKED: {decl_reason}")
    if unchecked:
        summary.append(f"  {unchecked} claim(s) went unchecked for the reason(s) above")
    return violations, summary


def self_test() -> int:
    """Assert each verdict fires, on constructed inputs."""
    failures = 0

    doc = "\n".join([
        "## X-1 — an entry that uses its model",
        "- **Model**: `bikar/patterns/Coupons/Real.bkr` — the one it uses",
        "- **Print target**: `bikar/patterns/Coupons/Disowned.bkr` is NOT this coupon",
        "  ```",
        "  render --param good=1 --piece GoodPiece --brick-fit ribMm=0.1",
        "  ```",
        "## X-2 — an entry with no model bullet at all",
        "- **Status**: planned",
        "  `--param orphan=2`",
        "## X-3 — model path embedded in a wrapped render command",
        "- **Model**: no baked `.bkr` needed; render it via",
        "  `cd bikar && node cli.js render",
        "  patterns/Orbs/Star-Orb.bkr --param radius=40`",
        "- **Status**: planned",
    ])
    entries = parse_catalog(doc)
    cases: list[tuple[str, object, object, str]] = [
        ("three entries parsed", len(entries), 3, "`## ID` starts a section"),
        ("models come from the Model bullet only", entries[0].models,
         ["bikar/patterns/Coupons/Real.bkr"],
         "a .bkr the entry disowns must not satisfy its claims"),
        ("knobs are found anywhere in the section", len(entries[0].claims), 3,
         "render commands are not always in the Model bullet"),
        ("an entry with no model still yields its claims", len(entries[1].claims), 1,
         "it is reported pending, not dropped"),
        ("a path embedded in a wrapped command is found", entries[2].models,
         ["patterns/Orbs/Star-Orb.bkr"],
         "P1's only model mention is mid-command across a line wrap; a bare `.bkr` is not a path"),
    ]
    for label, got, want, why in cases:
        ok = got == want
        failures += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: {label} → {got!r} (want {want!r}; {why})")

    # The BrickFit reader must fail loud on a shape it cannot parse, not open.
    shape_cases = [
        ("export interface BrickFit {\n  readonly a: number;\n}\n", 0,
         "a two-field interface is a parse failure, not a two-knob answer"),
        ("interface Something Else {}\n", 0, "no BrickFit at all"),
    ]
    for src, want_n, why in shape_cases:
        block = BRICKFIT_BLOCK.search(src)
        fields = frozenset(BRICKFIT_FIELD.findall(block.group(1))) - BRICKFIT_NOT_A_KNOB if block else frozenset()
        loud = not block or len(fields) < 4
        ok = loud and len(fields) >= want_n
        failures += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: BrickFit reader is loud on {src.splitlines()[0]!r} ({why})")

    # And it must read the real one.
    fields, reason = brickfit_fields(ROOT)
    ok = reason is None and "ribMm" in fields
    failures += 0 if ok else 1
    print(
        f"self-test {'ok  ' if ok else 'FAIL'}: real BrickFit reads {sorted(fields)}"
        + (f" — unavailable: {reason}" if reason else "")
    )

    # The declaration-keyword harvest must include `clip`: a hand-written list
    # left it out, and two correct catalog entries were reported as defects.
    kws, kw_reason = declaration_keywords(ROOT)
    ok = kw_reason is None and {"clip", "tile", "brick", "piece"} <= kws and "param" not in kws
    failures += 0 if ok else 1
    print(
        f"self-test {'ok  ' if ok else 'FAIL'}: declaration keywords read {sorted(kws)}"
        + (f" — unavailable: {kw_reason}" if kw_reason else "")
    )

    # The same fail-loud floor, on a grammar that has changed shape.
    thin = frozenset(DECL_HEAD.findall('OrbDecl = "orb" IDENT ;\n')) - DECL_NOT_A_PIECE
    ok = len(thin) < 6
    failures += 0 if ok else 1
    print(
        f"self-test {'ok  ' if ok else 'FAIL'}: a grammar yielding {len(thin)} keyword(s) is a "
        "parse failure, not a one-keyword language"
    )

    print("self-test: " + ("PASS" if failures == 0 else f"FAIL ({failures})"))
    return 0 if failures == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="print every claim and its verdict")
    ap.add_argument("--self-test", action="store_true", help="verify the gate's own classifications")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    violations, summary = run(ROOT, args.list)
    for line in summary:
        print(line)
    if violations:
        print("")
        for v in violations:
            print(v)
        print(f"\ncatalog models: {len(violations)} violation(s). Override once: CATALOG_MODELS_OK=1 git commit")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
