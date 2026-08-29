# Prints tab — design doc (pre-implementation)

Status: **DRAFT, PARTIALLY BUILDABLE.** The record format, the four blocking
decisions, and this doc are buildable now and land in this PR. The gate
(`.claude/gates/prints_gate.py`), the rendered tab (`docs/prints.md`), and the
first real record all wait on a physical print — they ship when there is a subject
to measure, not before (the "measure before you gate" rule,
[`docs/issue-register-evaluation.md`](issue-register-evaluation.md) §5.1).

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
status:   printed                          # sliced|printed|measured|propagated|abandoned
outcome:  readings                         # readings|no-reading|partial
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
objects:                                   # one per printed object on the plate
  - entry:        MC-2
    source:       bikar:patterns/Coupons/Machine-Card.bkr
    source_sha256: fdc100884e34c0aeffc517a5335d3df2ce79d718c9ee8a31a7f4330643d0a0e4
    piece:        keyhole
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
photos:                                    # source binaries, tracked on master
  - file:   photos/plate-overview.jpg
    sha256: <digest>
    of:     "the whole plate, raking light"
    why:    "shows the keyhole floor intact"
```

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

## 7. The gate (ships in S3, with the first real record)

**Validator:** `.claude/gates/prints_gate.py`, wired to hook
`.githooks/pre-commit.d/39-prints` and `make validate-prints`, passes iff every
record directory under `docs/prints/` satisfies R1–R4 below and the count of real
records it checked is printed to stdout (never a silent green over an empty set).

PASS: a tree with one record whose pin resolves, whose photo digests match and are
unique across records, whose settled bet is marked settled in `bets.md`, and the
gate prints `prints_gate: 1 record checked`.

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

The gate ships **with** the first real record (S2 → S3), not before, for exactly the
R4 reason: an empty subject set reports green and teaches nothing.

## 8. Where it lives

Records live at `docs/prints/<run>/`. A rendered reader, `docs/prints.md`, is built
into the site as a tab (S6). Because the audience includes gallery visitors, not just
the operator ([D-046](decisions-log.md)), a lab page `prints.html` is vendored into
the site (S7); the site has no shared nav bar, so its `site-graph.json` pins shift
when a nav entry is inserted — that is the S7 hazard, handled in that rung.

## 9. Sequencing

The rungs are ordered so nothing gates an empty set and nothing renders a record
that does not exist:

| rung | ships | needs a printer? | task |
|---|---|---|---|
| S1 | record format + this doc + one filled example (fenced) | no | #65 |
| S2 | print Plate 1, fill the first real record | **yes** | #67 |
| S3 | `prints_gate.py` R1/R2/R4 + hook `39-prints` + `docs/prints/**` gate exclusion | yes (needs S2's record) | #66 |
| S4 | gate R3 two-way propagation | yes (after first bet flips) | #71 |
| S5 | delete the empty Iteration log from the catalog | no (but ordered after S3) | #68 |
| S6 | rendered `docs/prints.md` tab | yes (renders real records) | #69 |
| S7 | vendor `prints.html` lab page | yes | #70 |

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
| Know what I've proven | "What have I actually printed?" | the records list (empty today) |
| Know what's next | "What should I print next, and why?" | the queue (§6), transcluded from backlog |
| Improve a design | "Where do I capture what a print taught?" | the run record body + readings (§4) |
| Trust a number | "Which bet did this plate settle?" | `readings[].settles` → `bets.md` (§7 R3) |
| See it | "What did the plate look like?" | `photos[]` (§5) |

Rows the UX deliberately does **not** answer (cost, print time, filament grams) are
named as out of scope here rather than hidden — the tab records what a plate taught,
not what it cost.

## 12. Read against itself (K7)

- The worked example in §4.1 (`MC-2` / `CAL-FEA-01`) satisfies §4.1's own schema and
  its pins resolve against the ref in §3.
- §6 forbids a stored rank; no other section stores one.
- §7's FAIL case is the *hard* case (a mismatched geometry pin), not a trivially
  malformed file — an aggregate "all photos present" cannot discharge R1.
- The deletion in §2 and the sequencing in §9 agree: S5 deletes the Iteration log,
  ordered after S3 so the replacement register exists first.
