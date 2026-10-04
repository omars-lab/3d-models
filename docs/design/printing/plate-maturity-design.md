---
status: draft
---

# Plate maturity: experiment, repeatable, production

**Status:** draft, 2026-10-03. The level on each page, the gate rule (P8) and the grade tool are
built; every plate today is an experiment, by its prints and on its page. Omar decided call 1 the
same day: production plates get a standing approval, and a change to a production recipe goes on
a new experiment plate ([D-095](../../working-model/decisions-log.md), §6). §8 lists the calls
still theirs.

Produced by: a worker session for the plate-maturity side quest, 2026-10-03. Feeds:
[print-review-design.md](print-review-design.md) (the plate pages this adds a field to) and
[D-094](../../working-model/decisions-log.md). No outside research: every number here is measured
on this repo's pages, records and slices, or is a first guess named as one.

## 1. What Omar asked for

On 2026-10-03 Omar asked whether plates need a maturity — "experimental vs not? … vs repeatable
… production ready … prototype" — and for "a hook to validate proper maturity and a grading skill
to grade maturity of plate from historic prints, space efficiency of plate, proven value of
prints". And the rule that sets the rest: **"prod plates should be optimized, experimental
plates arent".**

That last line is why maturity has to be a field and not a feeling. An experiment is laid out to
answer a question: a pair of pieces side by side so the difference is easy to read, a lot of
empty bed so a failure cannot spread. Packing it tight would spoil the reading. A plate that
prints something known, again, for use, should waste neither bed nor hours. The same plate page
cannot be judged by both standards unless it says which one it is under.

## 2. The levels

| Level | Means | Bed packed? |
|---|---|---|
| `experiment` | a question is still open about at least one piece | no, and not asked to be |
| `repeatable` | every piece on the plate has printed well, its latest K times, somewhere | not yet asked |
| `production` | repeatable, this plate printed clean as laid out, and its bed fill is measured | `bed_fill` at least the rubric's number, which is 0 (no bar) since D-098 |

Three levels, not four. "Prototype" and "experiment" differ by intent — trying a new idea versus
checking a known one — and the page already carries intent in `kind` (`new` or `taste`). A fourth
level would hold nothing the prints can tell apart, so the gate rejects the word.

**Every page starts at `experiment`.** It is the honest default: nothing has been shown yet.

## 3. What each level reads

The evidence is the print records in `docs/prints/`, read per piece. A **piece** is the same piece
on any plate: the same model file, the same `piece`, the same params (and, on a sampler sheet,
the same window). That is the point of reading across plates: minis-05 and minis-06 reuse pieces
minis-04 already printed, and what minis-04 showed about them counts for both.

- **Repeatable:** every distinct piece in the plate's current recipe has its **latest K
  verdicts all `keep`**, across every record on any plate. K is `keeps_for_repeatable` in the
  rubric (2 at first, 1 since 2026-10-04, D-098). The latest K, not any K: a piece kept twice and then judged `adjust` was
  judged wrong last. And every piece, not a total: three pieces kept twice each and one never
  printed is not repeatable, however many keeps there are in all.
- **Production:** repeatable, and
  - the page's `bed_fill` is at least `production_fill` in the rubric (0.45 at first, 0 since
    2026-10-04, D-098, §4);
  - the page is `kind: repeat` (§5);
  - this plate's own latest run kept every piece, and printed the same pieces in the same
    counts the recipe holds now. Pieces proven on other plates are not enough: packing a bed
    tighter is itself a change, and only this plate's run shows it printed packed.

The page writes the level as `maturity:` and the bed as `bed_fill:` (a share, 0 to 1), next to
`minutes` and `grams`, which also come from a slice.

### Moving up, moving down

Up is written, never assumed. A page above `experiment` carries a dated `promoted` row in its
timeline, and the last `promoted` or `demoted` row names the level the page says. The
[grade-plate skill](../../../.claude/skills/grade-plate/SKILL.md) writes both after the grade
says the evidence holds.

Down is forced by the evidence. Nothing has to remember to demote a plate: the gate fails the
moment a page claims more than its prints show, and the fix is to lower `maturity` and add a
`demoted` row saying why. The ways a plate falls:

- **A new verdict.** A record judges a piece `adjust` or `drop`; its latest K are no longer all
  keeps.
- **A recipe change.** A new piece, or the same piece with different params, has no keeps yet.
  The plate is an experiment again until it has.
- **A repack.** Changing the counts (more of a piece to fill the bed) means this plate's latest
  run no longer printed what the recipe holds, so production falls to repeatable until a packed
  run prints clean.
- **A stricter rubric.** Raising K or the fill turns plates back. That is intended: the rubric is
  read at run time, so the bar can move without code changing, and the gate says which pages it
  moved.

Under-claiming is allowed. A plate whose prints would carry `repeatable` but whose page says
`experiment` gets a notice, not a finding: Omar may want it kept an experiment, and an
experiment is never wrong about what has been shown.

## 4. "Optimized", measured

`bed_fill` is the share of the first bed the pieces cover, seen from above: each object's convex
outline (as `--arrange` placed it), summed, over the X2D's 256 × 256 mm bed. The outline counts
the space inside a ring as used, which is right for packing, since nothing else can go there.
`python3 tools/plate_grade.py --fill <plate.3mf>` measures it from a slice, and the grade does it
for every plate with a local slice.

Measured on the slices that exist, 2026-10-03:

| Plate | Objects on bed 1 | Fill |
|---|---|---|
| minis-01 | 4 | 0.092 |
| minis-02 | 7 | 0.169 |
| minis-03 | 5 | 0.121 |
| minis-04 | 6 | 0.552 |
| sheets-04 | 7 | 0.278 |
| sheets-04b | 6 | 0.208 |

None was packed, and none should have been: each was an experiment. minis-04 is high only
because its pieces are large.

The production number is 0.45, a first guess, not measured against a packed plate (none exists).
Worked by hand on the 256 mm bed: four 100 mm round coasters in a 2 × 2 cover about 0.48 and
pass; four 90 mm coasters cover about 0.39 and fail; five 90 mm coasters in rows of 2, 1, 2 with
2 mm between them fit in 251 mm and cover about 0.49, which passes. So at 0.45 a bed of 90 mm
coasters is production only when it holds the fifth coaster a square grid leaves room for, which
is the kind of packing "optimized" should mean. The number lives in the
[rubric](../../../.claude/skills/grade-plate/rubric.md) with a round log, and it was Omar's call 2.

**Since 2026-10-04 the bar is 0** ([D-098](../../working-model/decisions-log.md), call 2 below).
Omar wanted phones-02, four phones covering 2% of the bed, saved as production after one good
print, and chose to change the rule rather than pack the plate first. A production page still
carries a measured `bed_fill`, so an empty bed stays visible, but the fill no longer decides the
level. Packing is still worth doing for hours and filament; it is the plate-packing skill's job.

Fill is the measure because it is the one a slice settles and a page can carry. Hours per piece
would be closer to the cost, but it changes with the piece, so a single bar could not hold
across plates of coasters and plates of minis.

## 5. `kind` and maturity are different questions

`kind` says why the **next** print happens: a `new` question, a `taste` (a look at something
known), or a `repeat`. Maturity says what the **past** prints showed. They move apart all the
time: a plate of pieces all kept twice (repeatable) can be printed once more as a `taste` of a
new color; a brand-new plate (experiment) is `kind: new`.

They meet in one place. A production plate prints what is known, for use, so it is
`kind: repeat`, and the gate holds that. Folding the two into one field would lose the first
case: a repeatable plate printed for a reason other than use.

## 6. Approval: one per send, standing for production

The send check D-093 built (`plateApproval` in `tools/bambu/src/send-gate.ts`) refuses a send
unless the page's Approvals table has an open `approved` row, one a send has not spent yet
([D-096](../../working-model/decisions-log.md); before the table it read timeline rows, and a
ticked box counted on its own for a plate that had never gone out). That holds for experiments and
repeatable plates.

A production plate has a **standing** approval ([D-095](../../working-model/decisions-log.md)):
it goes out again with no new yes. Omar, 2026-10-03: "yes prod plates get standing approval".
It still goes through `plateApproval` and nowhere else, so there stays one place that says whether
a plate may go out. Two things end it, both checked at send time rather than trusted from the page:

- **The prints slip.** `plateApproval` asks `.claude/skills/manage-approvals/scripts/plate_approve.py <page> --status --json`, which
  reads the same `maturity_evidence` as the gate. A page that still says production after a run
  came back `adjust` has no standing approval, even before anyone lowers it.
- **The recipe changes.** Promotion pins `recipe_hash` on the page: the first 12 hex digits of
  the SHA-256 of the parsed recipe, so a comment does not count and a repack with the same pieces
  does. A recipe that no longer matches is a P8 finding and has no standing approval. Promotion
  also writes a `standing` row in the Approvals table (`plate_approve.py <page> --standing`),
  covering that same recipe, so the table shows when the standing approval began.

A plate without its standing approval falls back to one yes per send; so does a plate the grader
cannot grade. A standing send leaves the box alone and writes a `sent` row that says it went out
on the standing approval, so the timeline still holds every send.

**A production recipe does not change in place.** Omar: "recipe change should be in a new
experimental plate derived from a prod plate".
`python3 tools/plate_grade.py --derive <parent> <new> --answers "…"` copies the recipe to a new plate whose page is an unapproved experiment with
`derived_from: <parent>`, and refuses a parent that is not production (an experiment's recipe is
edited in place). The new plate is printed, judged and promoted on its own records; then the
parent is retired. The grade-plate skill has the steps.

The tests: the plates gate's self-test (a production page with no pin, a recipe edited in place,
a comment-only edit, a `derived_from` with no page; standing approval held, lost on an `adjust`,
lost on a recipe edit), the grader's (a derived plate passes the gate as written), and
`send-gate.test.ts` (a grader that stands, one that does not, one that cannot run, a fresh yes on
a plate that lost its standing, and the real grader's JSON on this repo).

## 7. The gate, and why a skill as well

The precedent here is firm: both evaluations of a proposed skill
([dsl-extension](../process/dsl-extension-skill-evaluation.md),
[issue register](../process/issue-register-evaluation.md)) concluded "a gate instead". This
design ships a gate as the check and a skill only for the writing the gate cannot do: reading
the grade, copying `bed_fill` from a slice, and adding the dated row. The skill writes; the gate
holds what it wrote. Both read the same function (`maturity_evidence` in the plates gate), so the
grade the skill shows and the check hook 39 runs cannot disagree.

**P8, maturity is earned.** In `.claude/gates/plates_gate.py`, run by hook 39 and
`make validate-prints`, after P1–P6 pass on a page:

- `maturity` is one of the three levels; `bed_fill`, when present, is in (0, 1].
- The level is no higher than the prints show (§3).
- A production page is `kind: repeat`.
- A level above experiment has a `promoted` row, and the last promoted or demoted row names it.

**Validator:** `python3 .claude/gates/plates_gate.py --self-test` builds a clean set of pages and
records, then claims each level with and without its evidence, once per way a claim can be
wrong, and requires P8 to fire (or not) each time. It also checks that raising K in the rubric
turns a repeatable page back, and that an under-claim is a notice, not a finding.

PASS: a page at `repeatable` whose two pieces each have their last two verdicts `keep`, with a
`promoted` row; and a `production` page whose own latest run kept every piece, with
`bed_fill: 0.6` against a rubric of 0.5 and `kind: repeat`.

FAIL: a page at `repeatable` with three keeps on the plate while one of its two pieces was never
kept (the other was kept all three times) — an aggregate cannot carry a claim about every piece. Also a `production` page whose pieces
were all kept on other plates while this plate's own latest run adjusted one, and a piece kept
twice and then judged `adjust`.

Measured on the 12 real pages, 2026-10-03: before the pages carried the field, P8 gave 12
findings, one per page (`maturity` missing). With `maturity: experiment` written on each, 0
findings and 0 notices. The grade agrees: every page is an experiment by its prints too. Only one
piece has a keep anywhere (sheets-04's gBV minimal coaster, kept once); the three records hold no
bet readings yet; and only minis-04's bed is above 0.45. So the rule is forward-looking today:
the first plate it can promote is one whose pieces print well twice.

### What it does not see

- **A model edited in bikar.** A `.bkr` changed upstream with the same file name and params is
  the same piece to the gate. A record's `source_sha256` could tell them apart later.
- **A layout change that keeps the counts, below production.** Moving pieces without adding any
  keeps the plate's own run valid. Packing changes counts in practice, which the gate does see.
  On a production plate the pinned `recipe_hash` sees any change (§6).
- **`bed_fill` itself.** It is copied from a slice, which is gitignored, so the gate checks that
  it is a share and above the bar, not that the slice says so. The grade prints both and flags a
  difference.
- **Sheet windows.** A sampler-sheet piece is keyed by its window as the recipe writes it; a
  record that wrote the window differently would read as another piece. No sheet record has a
  window yet.

## 8. Omar's calls

Decided by Omar: production plates are optimized and experiments are not (2026-10-03). Call 1
is decided; the rest is open.

**1. A standing approval for production plates?**

| | Keep one yes per send (my pick) | A production plate carries a standing yes |
|---|---|---|
| **Pros** | Nothing to change; every send is looked at; D-093 stays as built | Reprinting a proven plate is one command |
| **Cons** | A plate printed for use asks every time | A recipe edit or a bad run between sends would go out on the old yes unless the yes lapses on both; that is call 6 of the print-review design again (decided by D-097: a change resets the yes) |
| **What it leads to** | Revisit once a plate actually reaches production | A change to `plateApproval` that reads `maturity`, and a lapse rule the gate holds |

- [ ] One yes per send
- [x] A standing yes for production (say what should end it in the notes)

**Decided 2026-10-03:** a standing yes for production → D-095. It ends when the prints slip or the
recipe changes, and a recipe change goes on a derived experiment plate (§6). Every plate today
stays an experiment.

**2. The numbers: K = 2 keeps, fill 0.45.** Both are first guesses (§3, §4); no plate has
printed twice or been packed. Keeping them and moving one when a grade looks wrong (my pick)
costs nothing now. The rubric's round log is where a change goes.

- [ ] Keep them
- [x] Change them (say to what in the notes)

**Decided 2026-10-04, in chat:** change them, to one keep and no fill bar → D-098. After phones-02
printed, Omar said "print good, lets save it as prod ready" and picked "Change the production
rule" over reprinting it once or packing it first. The exact numbers (1 and 0) are my reading of
the option's "one clean print, or no fill bar"; phones-02 needed both to qualify.

**3. Call 6 of the print-review design (does an approval lapse when the recipe changes?) stays
open there, for experiments.** D-095 answers it for production: the recipe does not change in
place, and an edited one loses the standing approval. For an experiment the yes is one per send
already, so call 6 asks only whether an edit between the yes and the send voids it.
**Decided 2026-10-03:** it does → [D-097](../../working-model/decisions-log.md). An experiment's
recipe changes in place as a new iteration, and the change resets the open yes; production keeps
D-095 and derives a new plate.

Notes:
