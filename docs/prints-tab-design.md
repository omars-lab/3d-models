# Prints tab — design doc (pre-implementation)

Status: **DRAFT, PARTIALLY BUILT.** The record format, the four blocking decisions,
and this doc landed in S1. The gate (`.claude/gates/prints_gate.py`, R1/R2/R4)
shipped in S3 **before** the first plate — R4 prints its subject count, so an empty
run is a true `0 records checked`, not a false green, which is the whole content of
the "measure before you gate" rule ([`docs/issue-register-evaluation.md`](issue-register-evaluation.md)
§5.1) once you read it correctly. What still waits on a physical print is the first
real record (S2), gate R3 (S4), and — for real content to render — the tab in its
populated form (S6/S7). (Corrected 2026-08-30 from "the gate waits on a print"; see
[`decisions-log.md`](decisions-log.md) D-046's amendment.)

Research: [`research/prints-tab-survey.md`](research/prints-tab-survey.md) — local
measurements; every zero-state number below is grounded there.
Visual design review: published artifact "Zero Prints, One Register"
(https://claude.ai/code/artifact/6849e2d5-1558-4a48-a09a-cdbfb5b4c462) carries the
UX mockup and the jobs→UX map in rendered form; this doc is the durable engineering
record the gates read.

---

## 1. What the tab is, in one sentence

A **print** is the one event this repository does not yet record: a physical plate
came off a machine, taught something, and that lesson should attach to the exact
geometry-and-process that produced it. The prints tab **records that event**,
**presents** the queue and backlog that already own scheduling
([`backlog.md`](backlog.md) §3.8), **consumes** the bets and protocol that already
own calibration, and **deletes** the one empty register that pretends to track
prints today.

## 2. The boundary — what it absorbs, presents, consumes, deletes

The single design risk is a second scheduler or a second bet registry growing
inside the prints tab. The boundary is drawn so it absorbs exactly one unowned
thing:

- **Absorbs (new, unowned):** the *print-run record* — a checked-in per-run
  directory pinning geometry, process, outcome, readings, and photos.
- **Presents (owned elsewhere, transcluded not copied):** the queue and backlog
  order, from [`backlog.md`](backlog.md) §3.8. The tab shows the order; it does
  **not** store a rank integer (§6).
- **Consumes (owned elsewhere, read-only):** the calibration bets
  (`.claude/skills/calibrate/bets.md`), the print protocol
  (`.claude/skills/calibrate/protocol.md`), the machine-card expectations
  ([`calibration-design.md`](calibration-design.md)).
- **Deletes (a divergence, per D-041):** the empty **Iteration log** tables in the
  prototype catalog — 32 tables, 0 rows
  ([`research/prints-tab-survey.md`](research/prints-tab-survey.md) §1). One
  register for the print-lesson, not two. Paid now while it costs zero rows.

## 3. A "version" is a (geometry, process) pair

The tab tracks per-model, per-version records. A version is not a version string —
it is the pair of identities that together determine what a plate can teach:

- **Geometry identity:** the `.bkr` source path, the blob's `sha256`, the bikar
  commit the blob was read at, and the piece selected. Two prints of the same file
  at different commits are different versions; the pin makes that checkable
  ([`research/prints-tab-survey.md`](research/prints-tab-survey.md) §4).
- **Process identity:** the nine-field profile header the print protocol already
  defines (`.claude/skills/calibrate/protocol.md`) — machine, material, spool,
  nozzle diameter, nozzle type, layer height, slicer profile, ambient temperature,
  instrument. The same geometry at 0.2 mm and at 0.12 mm layers are different
  versions, because they can print differently and teach different numbers.

## 4. The record format

**Validator:** a run-record directory is well-formed iff it is a directory named
`docs/prints/<YYYY-MM-DD>-<slug>/` containing exactly one `index.md` whose
frontmatter carries every required key in §4.1, and a `photos/` subdirectory
holding exactly the files its `photos[]` list names (no more, no fewer), each
matching its recorded `sha256`.

PASS: `docs/prints/2026-09-14-plate1-machine-card/` with an `index.md` whose
`photos[]` names `photos/plate-overview.jpg` and one file of that name sits in
`photos/` with a `sha256` equal to the recorded digest.

FAIL: the same directory with a second file `photos/extra.jpg` present on disk that
no `photos[]` entry names — an untracked binary in a record directory is a broken
record, because the gate can no longer say what every photo in the record is of.

### 4.1 Frontmatter schema

The record is Markdown-with-frontmatter, not JSON — the precedent is
`.claude/skills/maintain-use-cases/use-cases.md`, and the prose body carries the
human account a JSON blob cannot. Required keys:

```yaml
run:      2026-09-14-plate1-machine-card   # equals the directory name
plate:    "Plate 1 — Machine Card"         # human title
status:   printed                          # the 10-state lifecycle (print-model-design §3.1): draft|planned|sliced|printing|paused|printed|failed|measured|propagated|abandoned (R6)
outcome:  readings                         # readings|no-reading|partial
sheet:    docs/prints/plate-1-bench-sheet.md  # optional — the bench sheet this print realizes; many prints → one sheet, so no uniqueness (R7)
plate_3mf: 2026-09-14-plate1-machine-card.3mf  # the sliced plate this print came off; REQUIRED once status is sliced-or-later (R10). Named, not resolved — the .3mf may be large/gitignored
profile:                                   # the nine-field process identity (protocol.md)
  machine:        "Bambu A1"
  material:       "PLA Basic"
  spool:          "Bambu PLA Basic black, lot ..."
  nozzle_mm:      0.4
  nozzle_type:    "hardened steel"
  layer_mm:       0.2
  slicer_profile: "0.20mm Standard @A1"
  ambient_c:      24
  instrument:     "Mitutoyo 500-196-30 caliper"
pins:                                      # geometry identity, re-resolvable (R1)
  bikar_ref:  8dda702fc943d1876c56fe14b5b608ed53ea51e8
  self_ref:   <commit this record was recorded at, for two-way propagation>
objects:                                   # one per DISTINCT printed object on the plate
  - entry:        MC-2
    source:       bikar:patterns/Coupons/Machine-Card.bkr
    source_sha256: fdc100884e34c0aeffc517a5335d3df2ce79d718c9ee8a31a7f4330643d0a0e4
    piece:        keyhole
    count:        1                        # copies of THIS object on the plate; optional (default 1); int ≥ 1 (R8)
    params:       {}
    check:        "keyhole front floor prints without bridging sag"
    outcome:      printed                  # printed|did-not-print|abandoned
readings:                                  # one per measured quantity
  - entry:        MC-2
    question:     "does the 0.8 mm keyhole floor survive the bridge?"
    quantity:     KEYHOLE_FRONT_FLOOR_MM
    values_mm:    [0.78, 0.80, 0.79]
    median_mm:    0.79
    spread_mm:    0.02
    judged_by:    caliper
    settles:      CAL-FEA-01              # the bet this reading moves, or ~
    expected:     "≥0.8 mm survives as one clean floor (calibration-design §7)"  # the bench-sheet criterion, required once settles is a real bet (R5)
    verdict:      brackets                # brackets|above-range|below-range|refutes|no-reading — how the reading landed vs expected (R5)
photos:                                    # source binaries, tracked on master
  - file:   photos/plate-overview.jpg
    sha256: <digest>
    of:     "the whole plate, raking light"
    why:    "shows the keyhole floor intact"
feedback:                                   # optional — the recovery loop's account (task #37); a mapping when present (R9)
  symptom:   "warp lift at corner C"        # what went wrong, if anything
  cause:     "small footprint, no brim"     # the operator's / skill's diagnosis
  next:      "add a brim, re-slice"         # the remedy tried next
```

**On `objects[].count` (R8).** `objects[]` lists *distinct* geometries; `count` records
how many copies of each the plate carried, so a plate of nine identical clips is one
object with `count: 9`, not nine entries. This is the repeated-element multiplicity the
plate-arrangement work (task #42) packs and the query (task #40) sums; omitting it means
one copy. The `count`-vs-entries split keeps identity (R1, one `source_sha256` per
geometry) orthogonal to multiplicity.

### 4.2 The body is ungated prose

Below the frontmatter, the record carries a free-text account: what the operator
saw, what went wrong, what to try next. It is deliberately not gated — the bench
account is the source, and the four grounding gates (D2/D3/D4) do **not** apply to
`docs/prints/**`; only D1 (links resolve) does. Withdrawn literals may legitimately
appear in a record (a plate can measure a number an audit later kills), which is why
the exclusion is by rule, not by luck. This exclusion is part of the gate PR (S3),
mirroring how bikar's `check-doc-pointers.ts` excludes `docs/issues/`.

## 5. Photos

A record photo is capped at **2048 px on the long edge and 2 MB per file**,
re-encoded before commit — a policy the user chose, recorded in
[D-046](decisions-log.md) (not a measured engineering default, so no `**Default:**`
marker: its provenance is the decision, not a source). Rationale: large enough to
read a plate defect at 100%, small enough
that a repository of prints does not bloat the pack. Photos are tracked on master
beside their record (not under `build/`, which `make orbs` wipes — 
[`research/prints-tab-survey.md`](research/prints-tab-survey.md) §3), and are the
repo's first tracked non-generated binaries.

## 6. Priority is presented, never stored

The tab shows print order, but stores no rank integer. Order is
[`backlog.md`](backlog.md) §3.8's argument, transcluded. Beside each item the tab
shows how many bets it would settle — **which is explicitly not the rank**: a plate
can rank fourth while settling zero bets, and the tab must say so rather than let the
bet count read as the order. Storing a rank would be a second scheduler, the exact
thing §2 forbids.

## 7. The gate (ships in S3, before the first plate — R4 is why)

**Validator:** `.claude/gates/prints_gate.py`, wired to hook
`.githooks/pre-commit.d/39-prints` and `make validate-prints`, passes iff every
record directory under `docs/prints/` satisfies R1, R2, R4, R5, R6, R7, R8 and R9
below (R3 ships in S4) and the count of records it checked is printed to stdout
(never a silent green over an empty set).

PASS: an empty tree — no `docs/prints/` records yet — and the gate prints
`prints: 0 records checked — docs/prints/ is empty` and exits 0. The printed count is
what makes this a true pass, not a false one, which is why the gate ships before the
first plate rather than after. (One populated record passes the same way, printing
`prints: 1 record(s) checked, …`.)

FAIL: a tree with one record whose `objects[].source_sha256` does not equal the blob
read at `pins.bikar_ref` — the geometry identity is broken, the record claims to have
printed a file it did not, and the gate must refuse it rather than pass.

- **R1 — identity.** Each `objects[].source_sha256` equals the `sha256` of
  `objects[].source` read at `pins.bikar_ref`. Re-resolvable, checked at the recorded
  commit — not at whatever is checked out.
- **R2 — photos.** Every `photos[].file` exists, matches its `sha256`, and no
  unlisted file sits in `photos/`; digests are unique across all records (the same
  JPEG cannot back two different plates).
- **R3 — propagation (two-way, ships in S4 after the first bet flips).** A reading
  that `settles` a bet must be reflected in `bets.md` **and** the reverse: a bet that
  `bets.md` marks `measured` must have a record that settled it. The reverse direction
  is load-bearing — it is what catches a settled bet with no evidence behind it.
- **R4 — subject count printed.** The gate prints the number of records it checked.
  A gate that says "all pass" over zero records is indistinguishable from a broken
  gate; printing the count is the guard (`docs/issue-register-evaluation.md` §5.1).
- **R5 — a measured bet states its expectation and verdict (ships in S3, testable now).**
  Any reading whose `settles` names a real `CAL-…` bet (not `~`) must carry a non-empty
  `expected` — the bench-sheet criterion the reading was tested against — and a `verdict`
  from `{brackets, above-range, below-range, refutes, no-reading}` saying how it landed
  (`brackets` = inside the ladder, the pass; `above/below-range` = every rung passed/failed,
  re-centre that way; `refutes` = the reading contradicts the design's premise, a finding;
  `no-reading` = the coupon yielded no measurement but the attempt is logged). This is the
  per-record *compare* seam — it makes "did the print match what we expected?" structured
  data the gate checks, not prose an operator may forget. It is the precondition for R3:
  a reading cannot be propagated to `bets.md` until it has stated what it measured against.
  Unlike R3, R5 has no empty-subject problem — it fires the moment one reading settles a
  bet, so it ships now with R1/R2/R4.
- **R6 — status is a lifecycle state.** `status` is one of the ten plate/record states
  `{draft, planned, sliced, printing, paused, printed, failed, measured, propagated,
  abandoned}` ([`print-model-design.md`](print-model-design.md) §3.1). This is a
  *membership* check only; the consistency between a state and the fields it implies
  (a `measured` carries a reading, a `sliced` names a `.3mf`) is the freshness rules
  R10–R14 below (task #39, §6.3), not R6.
- **R7 — a named sheet resolves.** The optional `sheet` — the bench sheet this print
  realizes — must be a repo-relative path that resolves to a file. Many prints map to
  one sheet (re-prints, repeated attempts of one plate), so there is deliberately **no**
  uniqueness constraint; the rule only forbids a dangling pointer.
- **R8 — repeated-element count.** Each `objects[].count` defaults to 1 when omitted
  and, when present, must be a plain integer ≥ 1 (`bool` excluded — `count: true` is a
  mistake, not one copy). It is the multiplicity §4.1 splits from identity.
- **R9 — feedback is a mapping.** The optional `feedback` block (task #37's recovery
  account) must be a mapping when present. Its *required-when* rules (a `failed` record
  carries feedback) are R11 below, not this structural check.

The **freshness rules (R10–R14)** — the "freshness gate" of
[`print-model-design.md`](print-model-design.md) §6.3 (task #39). R1–R9 check a record
is *well-formed*; these check its `status` is backed by the *evidence that state
implies* (§3.1's Validator), so the lifecycle cannot lie. They live in the same
`prints_gate.py` as R1–R9, not a second gate file — the checks read the same parsed
frontmatter, and one parser / one hook / one self-test is the repo's no-fork rule
([`CLAUDE.md`](../CLAUDE.md), [D-052](decisions-log.md)) applied here.

- **R10 — a sliced-or-later plate names its `.3mf`.** A record whose `status` is at or
  past `sliced` (`sliced printing paused printed failed measured propagated`) carries a
  `plate_3mf` naming the plate it sliced / came off (§3.1). Presence + `.3mf` suffix
  only — like R7's `sheet`, the artifact may be large or gitignored, so the record must
  *name* it, not resolve it on disk.
- **R11 — a terminal-physical record carries a feedback block.** A `printed`, `failed`,
  `measured`, or `propagated` record carries a `feedback` block, present even if empty
  (§6.3 PASS for `printed`; the recovery loop, task #37, for `failed`). R9 checks it is
  a mapping; R11 checks it is there at all for these states.
- **R12 — a `measured` record carries a reading.** `status: measured` with an empty
  `readings[]` is refused — it claims a measurement while carrying none (§6.3 FAIL).
  *Hard case (K6/D2):* a `feedback` block does **not** discharge it — `measured`
  specifically requires a reading, so R12 checks readings, not feedback.
- **R13 — a `propagated` record names a bet.** `status: propagated` carries at least one
  `readings[].settles` naming a real `CAL-…` bet, not `~` (§3.1 FAIL). *Hard case
  (K6/D2):* the aggregate "the record has readings" cannot discharge it — one reading
  with a real `settles` is required.
- **R14 — a shipped record is past planning.** The whole-tree gate only sees records
  under `docs/prints/` — shipped ones — so a shipped record still at `draft`/`planned`
  is the drift §6.3 names: the plan artifact is composed-not-stored (§2), so a shipped
  pre-slice record must be reconciled past planning first.

The gate ships **before** the first real record, and R4 is precisely what makes that
honest: an empty subject set reports a *true* `0 records checked` when the gate prints
its count, and a false green only when it hides it. R1, R2, R5, R6, R7, R8, R9 and the
freshness rules R10–R14 are wired at zero (each a per-record invariant with no
empty-subject problem — a record either satisfies its state's evidence or it does not).
Only **R3** waits for S4 — it has an empty-subject problem R4 cannot fix,
because there is no settled bet to propagate from until the first one flips. R5 does *not*
share that problem: it is a per-record invariant that fires on the first reading to name a
bet, so it ships in S3 as the compare seam R3 will later build on. (Corrected
2026-08-30 from an earlier "ships with the first record, not before" — see
[D-046](decisions-log.md)'s amendment.)

## 8. Where it lives

Records live at `docs/prints/<run>/`. A rendered reader, `docs/prints.md`, is built
into the site as a tab (S6). Because the audience includes gallery visitors, not just
the operator ([D-046](decisions-log.md)), a lab page `prints.html` is vendored into
the site (S7); the site has no shared nav bar, so its `site-graph.json` pins shift
when a nav entry is inserted — that is the S7 hazard, handled in that rung.

S7 shipped 2026-09-01 (bikar #130; the vendoring PR here). What the page reads is
`prints-manifest.json`, written by `build/prints_manifest.py` from every
`docs/prints/<run>/index.md` with the gate's own frontmatter parser, gitignored and
rebuilt by `make deploy` — nobody types a printed plate into existence, and an
absent `docs/prints/` writes an empty register the page shows as the true state.
The site ships the manifest, not the record directories: photos are source
binaries tracked on master, so each record and each photo carries the repository
URL it is served from. The queue is linked from the page, not copied into it.

## 9. Sequencing

The rungs are ordered so that what gates an empty set does so *honestly* — printing
its zero count (S3's R4) — and only R3, which cannot, waits for a record to exist:

| rung | ships | needs a printer? | task |
|---|---|---|---|
| S1 | record format + this doc + one filled example (fenced) | no | #65 |
| S2 | print Plate 1, fill the first real record | **yes** | #67 |
| S3 | `prints_gate.py` R1/R2/R4 + hook `39-prints` + `docs/prints/**` gate exclusion | no (R4 makes the zero-state honest) | #66 |
| S4 | gate R3 two-way propagation | **yes** (after first bet flips) | #71 |
| S5 | delete the empty Iteration log from the catalog | no (but ordered after S3) | #68 |
| S6 | rendered `docs/prints.md` tab | no (renders the empty state until a record lands) | #69 |
| S7 | vendor `prints.html` lab page + the manifest generator | no (zero-state lab page) | shipped 2026-09-01, bikar #130 |

Only S1 is in this PR. The printer-gated rungs stay pending; shipping an empty
`prints_gate.py` into `make validate` would be the anti-pattern this repo warns
against.

## 10. The four decisions, resolved

All four blockers were resolved 2026-08-28 ([D-046](decisions-log.md)):

1. **Record dependency format** — YAML frontmatter, matching the `20-use-cases`
   precedent (resolved by author).
2. **First run** — Plate 1 (the machine card): it defines the profile header and is
   the plate most bets depend on (resolved by author).
3. **Photo cap** — 2048 px / 2 MB (resolved by user).
4. **Audience** — gallery visitors too, which moves `prints.html` (S7) into committed
   scope (resolved by user).

## 11. Jobs → questions → UX (the acceptance test)

Every question an operator walks in with must map to a surface the tab answers, and
every surface must answer a question. The full rendered map is in the artifact; the
load-bearing rows:

| the job | the question | answered by |
|---|---|---|
| Know what I've proven | "What have I actually printed?" | the records list (empty today); `bambu print list` |
| Reprint from a number | "How did I print it — machine/material/nozzle/profile?" | `print list --how`, the process-identity subset of §4.1's profile |
| Know what's next | "What should I print next, and why?" | the queue (§6), transcluded from backlog |
| Improve a design | "Where do I capture what a print taught?" | the run record body + readings (§4) |
| Trust a number | "Which bet did this plate settle?" | `readings[].settles` → `bets.md` (§7 R3) |
| See it | "What did the plate look like?" | `photos[]` (§5) |
| Plan the run | "How long, and how much filament?" | the `estimates` block (pre-print) and, once it runs, the MQTT `actuals` — surfaced on the tab (D-046 amendment 2026-09-17, PMR-8) |

**Amendment 2026-09-17 (PMR-8, [D-046](decisions-log.md)).** Print *time* and *filament
grams* — estimate before the print, MQTT-measured actual after
([`print-metadata-and-reprint-design.md`](print-metadata-and-reprint-design.md) §3.3.1) —
**do** now surface on the tab: Omar asked for them, and showing a number the record
already stores adds no second scheduler or bet registry, which is the boundary D-046
actually defends (§2). What stays out of scope is a *monetary* cost figure (a spool price
× grams): the repo does not hold filament prices, and inventing one would fabricate a
number the way §3.3.1 refuses to. So the tab answers "how long / how much filament,"
not "how many dollars."

## 12. Read against itself (K7)

- The worked example in §4.1 (`MC-2` / `CAL-FEA-01`) satisfies §4.1's own schema and
  its pins resolve against the ref in §3.
- §6 forbids a stored rank; no other section stores one.
- §7's FAIL case is the *hard* case (a mismatched geometry pin), not a trivially
  malformed file — an aggregate "all photos present" cannot discharge R1.
- The deletion in §2 and the sequencing in §9 agree: S5 deletes the Iteration log,
  ordered after S3 so the replacement register exists first.
