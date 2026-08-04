#!/usr/bin/env python3
"""Count gate for 3d-models: a count in a doc is a claim too.

A number like "29 catalog entries" or "17 registered bets" is a claim about a
set, and every one of them is already computed by something that runs: the
catalog gate prints the entry count, and bikar's `registry:calibration`
generates `.claude/skills/calibrate/bets.md` with the bet and record counts in
its header. Nothing re-ran the hand tally in the doc, so it decayed while
reading as verified.

That is not hypothetical. On 2026-08-03 `docs/backlog.md` §2's count table was
stale by three merges — bets 14 (17), records 16 (17), catalog entries 28 (29),
`.bkr` coupons 5 (8) — and §8's "Counts reconcile" bullet, whose entire job is
to catch that, restated the same wrong figures independently. Fixing §2 and not
§8 would have left two counts disagreeing. **Two sites, one updated, is the
load-bearing failure here**, not an absent number, so it is the case the
self-test asserts.

Rules:

  C1  A marked count equals what its authority prints.
  C2  Every known quantity is marked somewhere, so a quantity cannot quietly
      stop being checked by having its marker deleted.
  C3  A number written directly in front of a phrase that *names* a known
      quantity carries that quantity's marker. C1 and C2 are both blind to an
      unmarked claim, and every defect this gate has caught was found at a site
      nobody had marked yet.

Authorities, and where each is read from:

  catalog-entries      `catalog_models.py`'s summary line
  cal-bets             the generated `bets.md` header
  cal-records          "
  cal-bets-no-record   "
  cal-mc-records       the generated `bets.md` *rows*, classified by the `MC-`
  cal-design-records   prefix on each row's coupon cell — and cross-checked
                       against the header total, because a projection that does
                       not add up to the summary it came from is a broken parse,
                       not a second opinion
  coupon-dir-bkr       the file count of bikar's `patterns/Coupons/`, read at a
                       published ref. Skippable: when bikar is unreachable the
                       quantity is labelled `[skipped]` in the summary rather
                       than folded into a clean run

Marker syntax, written immediately after the number:

    | Entries in the prototype catalog | 29 <!--count:catalog-entries--> | ... |

The comment is invisible in rendered markdown, so marking a number costs the
prose nothing.

C1 and C2 are marker-scoped, and that was the whole gate until 2026-08-03, when
the question "does anything check that a claim is marked *at all*?" was answered
by measurement rather than by opinion — the method `docs/issue-register-\
evaluation.md` and the rejected link checker both used. Over the 62 documents of
`docs/` and `.claude/`:

  * a number within 60 characters of the quantity's vocabulary → **117 hits,
    ~5 real (~4% precision)**. Section numbers beside "records", "records" as a
    verb, path fragments, line-number lists. That rule is the one that "cries
    wolf and gets switched off, which is worse than having no gate" — it must
    not ship, and it did not.
  * a number *immediately* in front of a curated noun phrase → **9 hits, 9 real
    (100%)**, of which **6 were wrong at the time of writing** and had survived
    both of this gate's own merges. That is C3.

So C3 is not a prose parser and must never grow into one. It is a short list of
exact phrases, each registered next to the quantity it names, and the price of
each phrase is measured before it is added. Two consequences of the measurement
are load-bearing:

  * **Match across the line wrap.** `backlog.md` §4 read "Seven of the fourteen
    registered\\nbets" — stale by three, and invisible to every line-at-a-time
    rule. The wrapped case is the self-test's by-design failure for exactly that
    reason.
  * **Match number *words*.** Two of the six stale claims were spelled
    "fourteen" and "sixteen". A digit-only rule scores zero on them.

`<!--count:quote-->` opts a line out. It exists for one legitimate use: prose
that deliberately restates a number that *was* wrong — `docs/decisions-log.md`
narrating "this said four when it was six" must be allowed to say four. It is
not a silencer for a claim you have not checked.

The gate also prints the per-quantity site count on every run, so a quantity
asserted in two places and marked in one stays visible in the output. That is
the same opt-in-with-the-gap-shown shape the use-case validator uses for
anchored pointers.

Usage:
  counts_gate.py [FILE ...]     check the given files (default: docs/**/*.md)
  counts_gate.py --self-test    run the fixtures and verify the gate fires
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from doc_pointers import _sibling_root, _tracked_at_ref  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
GATES = Path(__file__).resolve().parent
BETS = ROOT / ".claude" / "skills" / "calibrate" / "bets.md"

# `29 <!--count:catalog-entries-->` — the number, then the tag naming its
# authority. Whitespace between them is optional so a table cell can be tight,
# and may be a newline: see `marks_in` for why that matters.
MARK = re.compile(r"(\d[\d,]*)\s*<!--\s*count:\s*([a-z0-9-]+)\s*-->")

# The generated registry's header line, which is the authority for three of the
# four quantities. Generated by bikar's scripts/gen-calibration-registry.ts —
# reading it rather than recomputing from CAL_BETS is deliberate: two
# independent derivations of one number is how they come to disagree.
BETS_HEADER = re.compile(
    r"\*\*(\d+) registered bets · (\d+) `Calibrated` records — "
    r"\d+ provisional, \d+ measured · (\d+) bets with no record in bikar\.\*\*"
)

#: One row of the generated **Bets** table:
#: `| \`CAL-FIT-01\` | quantity | \`MC-1\` | provisional | \`A_CAL\`, \`B_CAL\` |`
#: Group 1 is the coupon cell, group 2 the comma-separated record list. The
#: coupon cell is not always an id — `CAL-STR-01` carries a sentence explaining
#: why it has no coupon — so it is matched as free text and classified by
#: prefix, not required to be an id.
BETS_ROW = re.compile(
    r"^\| `CAL-[A-Z]+-\d+` \| [^|]* \| ([^|]*) \| [^|]* \| ([^|]*) \|\s*$",
    re.MULTILINE,
)

#: Number words, because two of the six claims C3 first caught were spelled out
#: ("fourteen registered bets", "sixteen provisional records"). Twenty is the
#: ceiling on purpose: past that, prose in this repo uses digits, and every word
#: added to this alternation is another way for the phrase patterns to misfire.
NUMBER_WORD = (
    "one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
    "fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty"
)
NUMBER = rf"(?:\d[\d,]*|{NUMBER_WORD})"

#: The C3 vocabulary: phrases that make the number in front of them a claim
#: about a known quantity. Curated, not derived — see the module docstring for
#: the measurement that set the shape. Add a phrase only after checking what it
#: costs across the corpus; a phrase that fires on prose it cannot parse takes
#: the whole gate down with it.
PHRASES: dict[str, list[str]] = {
    "cal-bets": [r"registered bets", r"`CAL-\*` bets", r"ids are registered"],
    "cal-records": [r"`?Calibrated(?:<T>)?`? records", r"provisional records"],
    "catalog-entries": [r"catalog entries", r"print-gated items"],
    "coupon-dir-bkr": [r"coupon `\.bkr` files"],
}

#: `NUMBER`, an optional marker, an optional "of the", then the phrase.
#:
#: Both narrowings here were bought with a false positive, not guessed at. The
#: filler slot was one free `\\w+`, and `LG-P1 / LG-P2, whose\\ncatalog entries`
#: in a research file duly read as "2 … catalog entries" — a coupon id donating
#: its digit and "whose" filling the slot. Nothing in the corpus's real claims
#: uses the open slot, so it costs a finding and buys nothing: it is now the
#: closed literal `of the`, and `(?<![\\w-])` stops an identifier's trailing
#: digit from being read as a count. C3 misses "17 of the registered bets"
#: phrased some third way; that is the intended trade, because a narrow rule
#: that is always right is the only kind worth blocking a commit on.
C3 = {
    name: [
        re.compile(
            rf"(?<![\w-])({NUMBER})\s*(<!--\s*count:\s*[a-z0-9-]+\s*-->)?"
            rf"\s*(?:of the\s+)?{p}",
            re.I,
        )
        for p in patterns
    ]
    for name, patterns in PHRASES.items()
}

#: Opts a line out of **C1 and C3 both**. For prose that quotes a number which
#: was *known to be* wrong, which the decision log does by design.
#:
#: C1 as well as C3, because the first thing written under this marker was
#: `docs/decisions-log.md` reciting a self-test fixture verbatim —
#: `99 <!--count:cal-records-->` — and a gate that reads a quoted fixture as an
#: assertion makes its own validator section unwritable. The marker means "this
#: line is *about* a number", and that is one fact, not two.
QUOTE = re.compile(r"<!--\s*count:quote\s*-->")

CATALOG_SUMMARY = re.compile(r"^catalog models: (\d+) entries;", re.MULTILINE)

#: Where the coupon models live in bikar. A directory listing is a real
#: authority — no curation, nothing to keep in sync by hand.
COUPON_DIR = "patterns/Coupons/"

#: Quantities whose authority lives in a sibling repo, and so may legitimately
#: be unreachable — a fresh clone, or the `gh-pages` worktree. Everything else
#: is sourced from this repo and its absence is a failure, not a skip.
SKIPPABLE = frozenset({"coupon-dir-bkr"})

#: Only the *published* refs. Reading bikar's working tree, or its `HEAD`, makes
#: this count a function of whichever branch the other session has checked out —
#: and that checkout is routinely on a detached HEAD (`docs/decisions-log.md`
#: D-001). This is the same reasoning `doc_pointers._tracked_at_ref` is built
#: on, and the same trap it was written after walking into.
BIKAR_REFS = ("origin/HEAD", "origin/main", "origin/master")


def authority_catalog_entries() -> int:
    """However many entries `make validate-catalog` reports."""
    proc = subprocess.run(
        [sys.executable, str(GATES / "catalog_models.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    blob = proc.stdout + proc.stderr
    m = CATALOG_SUMMARY.search(blob)
    if not m:
        raise RuntimeError(
            "catalog_models.py printed no 'catalog models: N entries' summary; "
            f"cannot source catalog-entries from it. Output was:\n{blob}"
        )
    return int(m.group(1))


def authority_bets() -> dict[str, int]:
    """Every quantity the generated registry knows: its header, and its rows.

    The header gives the totals. The rows give the split by coupon series —
    which records a machine-card bet settles, and which a design-specific
    coupon does. Both are read out of the one generated file, and the row sum
    is checked against the header total: if a projection of the registry
    disagrees with the registry's own summary, the parse is wrong and saying so
    is the only honest outcome.
    """
    if not BETS.exists():
        raise RuntimeError(
            f"{BETS.relative_to(ROOT)} is missing — regenerate it with "
            "`cd ../bikar && npm run registry:calibration`"
        )
    text = BETS.read_text(encoding="utf-8")
    m = BETS_HEADER.search(text)
    if not m:
        raise RuntimeError(
            f"{BETS.relative_to(ROOT)} has no parseable header line. It is "
            "generated; if its format changed, this gate's BETS_HEADER pattern "
            "must change with it rather than the file being hand-edited."
        )
    bets, records, no_record = int(m.group(1)), int(m.group(2)), int(m.group(3))

    rows = BETS_ROW.findall(text)
    mc = design = 0
    for coupon, record_cell in rows:
        n = len(
            [r for r in record_cell.split(",") if r.strip() and r.strip() != "—"]
        )
        if coupon.strip().strip("`").startswith("MC-"):
            mc += n
        else:
            design += n

    if len(rows) != bets or mc + design != records:
        raise RuntimeError(
            f"{BETS.relative_to(ROOT)}: the row parse disagrees with the "
            f"header — {len(rows)} row(s) summing to {mc + design} record(s), "
            f"against a header of {bets} bets and {records} records. The table "
            "format changed; BETS_ROW must change with it. A split that does "
            "not add up to the total is worse than no split."
        )

    return {
        "cal-bets": bets,
        "cal-records": records,
        "cal-bets-no-record": no_record,
        "cal-mc-records": mc,
        "cal-design-records": design,
    }


def authority_coupon_dir() -> int | None:
    """How many `.bkr` files live in bikar's `patterns/Coupons/`.

    None when bikar is not reachable — a fresh clone, or the `gh-pages`
    worktree. That is a genuine skip and not a pass: `check` reports it in the
    summary and declines to fire C2 for the quantity, so a marker that stops
    being checked is still visible in the output.
    """
    repo = _sibling_root("bikar", ROOT)
    if repo is None:
        return None
    for ref in BIKAR_REFS:
        tree = _tracked_at_ref(repo, ref)
        if tree is None:
            continue
        return len(
            [p for p in tree if p.startswith(COUPON_DIR) and p.endswith(".bkr")]
        )
    return None


def resolve_authorities() -> dict[str, tuple[int, str]]:
    """Every quantity this gate knows, its current value, and who printed it.

    The set is hard-coded and small on purpose. A gate that discovers its own
    quantities cannot tell a number that vanished from a number that was never
    there, and C2 depends on exactly that distinction.

    A quantity whose authority is unreachable is simply absent from the result;
    `SKIPPABLE` names the ones that may legitimately be, so `check` can tell an
    unreachable authority from a marker nobody defined.
    """
    bets = authority_bets()
    header = "`.claude/skills/calibrate/bets.md` header"
    rows = "`.claude/skills/calibrate/bets.md`'s bet table"
    out: dict[str, tuple[int, str]] = {
        "catalog-entries": (
            authority_catalog_entries(),
            "`make validate-catalog`",
        ),
        "cal-bets": (bets["cal-bets"], header),
        "cal-records": (bets["cal-records"], header),
        "cal-bets-no-record": (bets["cal-bets-no-record"], header),
        "cal-mc-records": (bets["cal-mc-records"], rows),
        "cal-design-records": (bets["cal-design-records"], rows),
    }
    coupons = authority_coupon_dir()
    if coupons is not None:
        out["coupon-dir-bkr"] = (
            coupons,
            f"`bikar/{COUPON_DIR}` at {'/'.join(BIKAR_REFS)}",
        )
    return out


def marks_in(path: Path) -> list[tuple[int, str, int, str]]:
    """(lineno, quantity, claimed value, the line) for every marker in a file.

    Joined across the line wrap, for the same reason C3 is — and for one more,
    found the moment C3 shipped: a number at the end of a line with its marker
    at the start of the next was invisible to a line-scoped parse, so C1 checked
    nothing while C3 saw the marker and stayed quiet. A marker that silently
    stops being read is worse than an absent one, because the absent one is a C2
    finding. Reported against the line the *number* is on.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for i, line in enumerate(lines):
        if QUOTE.search(line):
            continue
        joined = line + " " + (lines[i + 1] if i + 1 < len(lines) else "")
        for m in MARK.finditer(joined):
            if m.start() >= len(line):
                continue
            out.append(
                (i + 1, m.group(2), int(m.group(1).replace(",", "")), line.strip())
            )
    return out


def unmarked_claims(path: Path) -> list[tuple[int, str, str]]:
    """(lineno, quantity, the matched text) for every C3 hit lacking a marker.

    Each line is joined to the one after it before matching, and a hit is
    reported only when it *starts* on the line being scanned. That is what makes
    a wrapped claim visible: "Seven of the fourteen registered\\nbets" is one
    claim, and reading lines in isolation is precisely how it stayed stale for
    three merges.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for i, line in enumerate(lines):
        if QUOTE.search(line):
            continue
        joined = line + " " + (lines[i + 1] if i + 1 < len(lines) else "")
        for name, patterns in C3.items():
            for pat in patterns:
                for m in pat.finditer(joined):
                    if m.start() >= len(line) or m.group(2):
                        continue
                    out.append((i + 1, name, m.group(0)))
    return out


def check(
    targets: list[Path], authorities: dict[str, tuple[int, str]]
) -> tuple[list[str], dict[str, int]]:
    findings: list[str] = []
    sites: dict[str, int] = {name: 0 for name in authorities}
    #: Markers whose authority did not resolve this run. Counted and reported,
    #: never failed on — but never silently passed either.
    skipped = sorted(SKIPPABLE - set(authorities))
    for name in skipped:
        sites[name] = 0

    for path in targets:
        for lineno, name, claimed, line in marks_in(path):
            rel = path.relative_to(ROOT)
            if name in skipped:
                sites[name] += 1
                continue
            if name not in authorities:
                findings.append(
                    f"{rel}:{lineno}: C1 unknown quantity 'count:{name}' — this "
                    f"gate knows {', '.join(sorted(authorities))}. Add an "
                    f"authority for it or drop the marker; a marker with no "
                    f"authority checks nothing while looking like it does."
                )
                continue
            sites[name] += 1
            expected, who = authorities[name]
            if claimed != expected:
                findings.append(
                    f"{rel}:{lineno}: C1 count:{name} says {claimed}, "
                    f"{who} says {expected} — {line[:90]}"
                )

        for lineno, name, text in unmarked_claims(path):
            rel = path.relative_to(ROOT)
            findings.append(
                f"{rel}:{lineno}: C3 «{text.strip()[:70]}» names a quantity this "
                f"gate knows (count:{name}) but carries no marker, so nothing "
                f"checks it. Write the number as a digit followed by "
                f"`<!--count:{name}-->`. If the line is deliberately quoting a "
                f"number that was wrong, mark it `<!--count:quote-->`."
            )

    for name, count in sorted(sites.items()):
        if count == 0 and name not in skipped:
            expected, who = authorities[name]
            findings.append(
                f"C2 quantity 'count:{name}' is marked nowhere, so nothing "
                f"checks it. {who} currently says {expected}. Either mark the "
                f"place that asserts it, or remove it from this gate — a "
                f"quantity that silently stops being checked is how the tally "
                f"went stale in the first place."
            )
    return findings, sites


FIXTURE_OK = """\
| Entries in the prototype catalog | 29 <!--count:catalog-entries--> | fine |
| Registered bets | 17 <!--count:cal-bets--> | fine |
| Records | 17 <!--count:cal-records--> | fine |
| No record in bikar | 6 <!--count:cal-bets-no-record--> | fine |
"""

# The load-bearing fixture. §2's table is *correct*; the §8 bullet that restates
# the same figure was not updated with it. A gate that only checked the first
# occurrence, or that stopped at the first finding per quantity, would pass this
# — and this is the exact shape of the 2026-08-03 defect.
FIXTURE_ONE_OF_TWO_STALE = """\
| Entries in the prototype catalog | 29 <!--count:catalog-entries--> | correct |
| Registered bets | 17 <!--count:cal-bets--> | correct |
| Records | 17 <!--count:cal-records--> | correct |
| No record in bikar | 6 <!--count:cal-bets-no-record--> | correct |

Reading this file against itself: 28 <!--count:catalog-entries--> print-gated
items = 28 catalog entries. This bullet was not updated with the table above.
"""

FIXTURE_MARKER_DELETED = """\
| Registered bets | 17 <!--count:cal-bets--> | fine |
| Records | 17 <!--count:cal-records--> | fine |
| No record in bikar | 6 <!--count:cal-bets-no-record--> | fine |
"""

FIXTURE_UNKNOWN_QUANTITY = """\
| Entries in the prototype catalog | 29 <!--count:catalog-entries--> | fine |
| Registered bets | 17 <!--count:cal-bets--> | fine |
| Records | 17 <!--count:cal-records--> | fine |
| No record in bikar | 6 <!--count:cal-bets-no-record--> | fine |
| Coupon models | 8 <!--count:coupon-models--> | nothing prints this |
"""

# A quantity sourced from bikar, marked here, with bikar unreachable — a fresh
# clone or the `gh-pages` worktree. It must not fail (there is nothing to
# compare against) and must not read as an unknown quantity (it is defined,
# just unresolvable). It must still be *counted*, so the run says out loud that
# one site went unchecked rather than folding it into a clean summary.
FIXTURE_SKIPPED_AUTHORITY = """\
| Entries in the prototype catalog | 29 <!--count:catalog-entries--> | fine |
| Registered bets | 17 <!--count:cal-bets--> | fine |
| Records | 17 <!--count:cal-records--> | fine |
| No record in bikar | 6 <!--count:cal-bets-no-record--> | fine |
| Files in `patterns/Coupons/` | 6 <!--count:coupon-dir-bkr--> | bikar is absent |
"""

# C3's load-bearing fixture. The claim wraps mid-phrase — "fourteen registered"
# ends one line and "bets" begins the next — which is how the real one survived
# three merges and both of this gate's own PRs. A line-at-a-time implementation
# passes this fixture, so it is the case that proves C3 reads across the wrap.
# The second claim is spelled as a word, which a digit-only rule scores zero on.
FIXTURE_UNMARKED_WRAPPED = """\
| Entries in the prototype catalog | 29 <!--count:catalog-entries--> | fine |
| Registered bets | 17 <!--count:cal-bets--> | fine |
| Records | 17 <!--count:cal-records--> | fine |
| No record in bikar | 6 <!--count:cal-bets-no-record--> | fine |

The card measures the tuple once. Seven of the fourteen registered
bets and twelve of the sixteen provisional records are on this one card.
"""

# The same two sentences, unwrapped and marked. Proves C3 is satisfiable by
# marking rather than only by rephrasing — a rule you can only escape is a rule
# that gets escaped.
FIXTURE_MARKED_PROSE = """\
| Entries in the prototype catalog | 29 <!--count:catalog-entries--> | fine |
| No record in bikar | 6 <!--count:cal-bets-no-record--> | fine |

Seven of the 17 <!--count:cal-bets--> registered bets and twelve of the
17 <!--count:cal-records--> provisional records are on this one card.
"""

# The decision log's legitimate use: narrating a number that *was* wrong. Without
# the opt-out this is a false positive, and a gate that cannot be told "yes, I
# know, that is the point" gets switched off.
FIXTURE_QUOTED_PAST_ERROR = """\
| Entries in the prototype catalog | 29 <!--count:catalog-entries--> | fine |
| Registered bets | 17 <!--count:cal-bets--> | fine |
| Records | 17 <!--count:cal-records--> | fine |
| No record in bikar | 6 <!--count:cal-bets-no-record--> | fine |

D-019: the table said 14 registered bets for three merges. <!--count:quote-->
The fixture reads `99 <!--count:cal-records-->`, which is not a claim. <!--count:quote-->
"""

# A marker split from its number by the line wrap, and *wrong*. Before
# `marks_in` read across the wrap this fixture produced zero findings: C1 never
# saw the pair, and C3 saw a marker and fell silent. Written the day C3 shipped,
# because that is the day the hole opened.
FIXTURE_WRAPPED_MARKER = """\
| Entries in the prototype catalog | 29 <!--count:catalog-entries--> | fine |
| No record in bikar | 6 <!--count:cal-bets-no-record--> | fine |

The registry reads 17 <!--count:cal-bets--> registered bets and 99
<!--count:cal-records--> `Calibrated` records.
"""

FAKE = {
    "catalog-entries": (29, "a stub"),
    "cal-bets": (17, "a stub"),
    "cal-records": (17, "a stub"),
    "cal-bets-no-record": (6, "a stub"),
}

#: The same skippable quantity, this time resolved and disagreeing. Paired with
#: the skip case so the pair proves the skip is a *skip* and not a hole: the
#: identical document fails when the authority is readable.
FAKE_WITH_COUPONS = {**FAKE, "coupon-dir-bkr": (7, "a stub")}


def self_test() -> int:
    """Fixed authorities, so the self-test cannot pass by tracking the repo."""
    import tempfile

    cases: list[tuple[str, str, int, str, dict[str, int], dict]] = [
        ("clean", FIXTURE_OK, 0, "", {}, FAKE),
        # 2, not 1: the marked "28" is C1, and the *same sentence* restates it
        # unmarked as "= 28 catalog entries", which is C3. Both are real, and
        # the fixture having accidentally contained a C3 site before C3 existed
        # is itself the argument for C3.
        ("one-of-two-stale", FIXTURE_ONE_OF_TWO_STALE, 2, "says 28", {}, FAKE),
        ("marker-deleted", FIXTURE_MARKER_DELETED, 1, "C2 quantity", {}, FAKE),
        ("unknown-quantity", FIXTURE_UNKNOWN_QUANTITY, 1, "unknown quantity", {}, FAKE),
        (
            "skipped-authority",
            FIXTURE_SKIPPED_AUTHORITY,
            0,
            "",
            {"coupon-dir-bkr": 1},
            FAKE,
        ),
        (
            "same-doc-when-resolvable",
            FIXTURE_SKIPPED_AUTHORITY,
            1,
            "coupon-dir-bkr says 6",
            {"coupon-dir-bkr": 1},
            FAKE_WITH_COUPONS,
        ),
        ("unmarked-wrapped", FIXTURE_UNMARKED_WRAPPED, 2, "C3", {}, FAKE),
        ("marked-prose", FIXTURE_MARKED_PROSE, 0, "", {}, FAKE),
        ("quoted-past-error", FIXTURE_QUOTED_PAST_ERROR, 0, "", {}, FAKE),
        (
            "wrapped-marker",
            FIXTURE_WRAPPED_MARKER,
            1,
            "cal-records says 99",
            {"cal-records": 1},
            FAKE,
        ),
    ]

    ok = True
    with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
        for label, body, want, needle, want_sites, stubs in cases:
            path = Path(tmp) / f"{label}.md"
            path.write_text(body, encoding="utf-8")
            findings, sites = check([path], stubs)
            bad_sites = {k: sites.get(k) for k, v in want_sites.items() if sites.get(k) != v}
            if (
                len(findings) != want
                or (needle and needle not in " ".join(findings))
                or bad_sites
            ):
                ok = False
                print(
                    f"self-test FAIL: {label} wanted {want} finding(s) "
                    f"containing {needle!r} and sites {want_sites}, got "
                    f"{findings} / {bad_sites}"
                )
            else:
                detail = findings[0].split(": ", 1)[-1][:70] if findings else "clean"
                print(f"self-test ok  : {label} → {detail}")

    # The authorities must actually resolve against the live repo, or the gate
    # is green because it never read anything.
    try:
        live = resolve_authorities()
    except RuntimeError as exc:
        print(f"self-test FAIL: authorities did not resolve — {exc}")
        return 1
    print(
        "self-test ok  : authorities resolve — "
        + ", ".join(f"{k}={v[0]}" for k, v in sorted(live.items()))
    )

    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    if args.files:
        targets = [p if p.is_absolute() else (ROOT / p) for p in args.files]
    else:
        targets = sorted((ROOT / "docs").rglob("*.md"))
    targets = [p for p in targets if p.exists()]

    try:
        authorities = resolve_authorities()
    except RuntimeError as exc:
        print(f"counts-gate: {exc}", file=sys.stderr)
        return 1

    findings, sites = check(targets, authorities)

    for f in findings:
        print(f, file=sys.stderr)
    # A skipped quantity is labelled in the summary rather than left to look
    # like a checked one. The site count is still printed: "1 site(s), skipped"
    # says a claim went unverified this run, which is the whole point of
    # printing per-quantity counts at all.
    skipped = SKIPPABLE - set(authorities)
    summary = ", ".join(
        f"{k}={sites[k]} site(s)" + (" [skipped: bikar not readable]" if k in skipped else "")
        for k in sorted(sites)
    )
    print(f"counts: {len(targets)} document(s); {summary}")
    if findings:
        print(
            f"\ncounts-gate: {len(findings)} finding(s). Every number here is one "
            "some tool prints — take it from the tool. Override once with "
            "COUNTS_GATE_OK=1 git commit",
            file=sys.stderr,
        )
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
