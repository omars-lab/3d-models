# Decisions log

**Started:** 2026-07-30 · **Scope:** 3d-models, and cross-repo decisions taken from here

Each entry records the options that were actually on the table, which one was
taken, why, and **what would reverse it**. The last field is the one that makes
this different from a diary: a decision with no stated reversal condition is an
opinion that has learned to sound permanent.

---

## 0. Why this file exists when the repo rejects registers

[`CLAUDE.md`](../CLAUDE.md) says there is *deliberately no issue catalog* here,
and [`issue-register-evaluation.md`](issue-register-evaluation.md) measured why:
a good issue document sat unread for 76 days while the class it described
shipped six more times. That argument is about **defects**, and it turns on a
specific fact — a defect has a test, and the test protects the behaviour at zero
re-reading cost. The register was redundant with something strictly better.

A decision has no test. "We left the commit alone rather than rewriting a pushed
branch" cannot be asserted in `vitest`. Nothing else in the repo holds it, so
the choice is between writing it down and losing it.

So the boundary this file must respect, or it becomes the thing the evaluation
rejected:

- **A defect goes in a test**, per the graduation rule. Not here.
- **A decision between real alternatives goes here** — with its options, so a
  future reader can see what was rejected and check whether the reason still
  holds.
- **A rule that changes how the next thing gets written goes in `CLAUDE.md`**,
  not here. If an entry below ever hardens into one, it moves.

If this file reaches a length where nobody reads it, it has failed the same way,
and the answer is to delete entries whose reversal conditions have lapsed — not
to add a section explaining that it is important.

---

## D-001 — Leave bikar commit `9b1b4a3` as-is

**Date:** 2026-07-30 · **Status:** Decided (owner) · **Repo:** bikar

### Context

bikar's working checkout is shared with a concurrent session. While checking
whether Prettier failures predated my edits, I ran `git stash` / `git stash pop`
in that checkout — which the standing constraint forbids. The pop restored
everything, but the other session committed before my next command, sweeping my
two documentation files into its commit:

```
9b1b4a3  Diagnose the growth trailer git cannot see, instead of blocking mutely
  .github/workflows/calibration.yml               ← theirs
  .github/workflows/decision-coherence.yml        ← theirs
  CLAUDE.md                                 67++  ← mine
  docs/engine-issues.md                     33++  ← mine
  packages/core/tests/kernel3d/…test.ts           ← theirs
  scripts/check-calibration.ts                    ← theirs
  scripts/check-decision-coherence.sh             ← theirs
```

Verified: every `CLAUDE.md` and `docs/engine-issues.md` line in that commit is
mine, none of the other session's work was overwritten or lost, and the commit
is **already pushed** to `origin/trailer-nearmiss-diagnostic`.

### Options

| | Option | Cost |
|---|---|---|
| A | Leave it | Commit message describes 5 of its 7 files |
| B | Revert my 2 files, re-land clean later | Two extra commits; content temporarily absent |
| C | Split the commit, force-push | Rewrites a pushed branch another session may have built on |

### Decision

**A — leave it.** The content is correct and reaches `main` when the branch
merges.

### Why

C rewrites history on a pushed branch belonging to work this session does not
own; the failure mode (another session's local branch diverging from a
force-push it did not expect) is worse than an imprecise commit message. B pays
two commits and a window of absence to fix cosmetics.

### What would reverse it

If the branch has not merged and the other session asks to split it before
merging, do B. Do **not** do C without confirmation that the session is idle and
nothing is built on the branch.

### The process defect underneath

The mixed commit is a symptom; running a mutating git command in a shared
checkout is the defect. `git stash` was never necessary — the question was
"did these files fail Prettier before my edits", which
`git show main:CLAUDE.md | npx prettier --check --stdin-filepath CLAUDE.md`
answers without touching the working tree.

**Rule, for any checkout owned by another session:** read via `git show`,
`git log`, `git diff` against a ref. Never `stash`, `checkout`, `reset`, or
`clean`. Edits to tracked files are recoverable; stash is not, because it moves
work that is not yours.

---

## D-002 — The docs gate's D2 and D3 stay dormant

**Date:** 2026-07-30 · **Status:** Decided (owner) · **Repo:** 3d-models

### Context

[`.claude/gates/docs_gate.py`](../.claude/gates/docs_gate.py) ships three rules.
D1 (relative links resolve) checks 83 real targets across 18 files. D2 and D3
are marker-scoped — they fire only on a doc that declares a validator or a
default using the marked form — and the current corpus contains **zero** of
either marker. Both rules match nothing today.

### Options

| | Option | Effect |
|---|---|---|
| A | Leave dormant; let the stated criterion run | Rules bind new docs only |
| B | Retrofit all 7 audited docs to marked form | Rules go live; surfaces known K4/K6 instances |
| C | Retrofit only "load-bearing" defaults | Middle path |

### Decision

**A — leave dormant.** The criterion already recorded in
[`grounding-defect-taxonomy.md`](grounding-defect-taxonomy.md) §3.1 stands: *if
the next two design docs carry no markers, D2 and D3 should be deleted, not
extended.*

### Why

B is grading my own homework — same author, on docs whose defects I already know
from the audits, which is precisely the confound the taxonomy's §4 warns about.
It would also pre-empt the deletion criterion by manufacturing the adoption the
criterion is supposed to measure. C requires drawing a "load-bearing" line with
no test behind it, which is the kind of judgment call the taxonomy names as a
defect source rather than a tool.

Leaving them dormant costs nothing and keeps the measurement honest: two design
docs from now, either authors reached for the markers or they did not.

### What would reverse it

Two consecutive new design docs carrying no markers → delete D2 and D3. Markers
appearing unprompted → the rules earned their place, and retrofitting the older
docs becomes worth revisiting.

---

## D-003 — Build Lego Lab Q3 + M7; defer M6 behind the coupons

**Date:** 2026-07-30 · **Status:** Decided (owner) · **Repos:** bikar, 3d-models

### Context

[`lego-lab-design.md`](lego-lab-design.md) §10 marks R0 complete and puts
**LG-F1/F2/R1 — physical clutch coupons — directly before M6**, with the note
that they *"block M6's dimensions."* Those coupons need a printer, which is
owner-held and on hold. M6 as specified therefore cannot proceed.

Two things in the same document are *not* blocked:

- **§11 Q3** — *"does `unionPatternFaces` always return a ring the anchor test
  can use? … a pattern with a genuine interior void would have that void
  cancelled away, so the anchor test could pass on material that is not there.
  Needs a check against a deliberately-holed pattern before M7."* A falsifiable
  question, answerable in code, which the doc itself makes a precondition of M7.
- **M7** — anchor solver, `grid-gate.ts`, `sweepGridFit`. Registration geometry.
  Clutch does not enter it, so no coupon number does either.

### Options

| | Option | Blocked on owner? |
|---|---|---|
| A | Q3 + M7 only | No |
| B | Q3 + M7 + M6 with constants as `CAL-*` bets | No, but ships unmeasured dimensions |
| C | Audit an unaudited design doc first | No |
| D | Measure qiyas gate debt first | No |

### Decision

**Superseded within the hour — see D-005.** The decision as first taken was
*A — Q3 first, then M7, M6 waits for LG-F1/F2/R1*. The reasoning below is kept
because D-005 overturns a specific claim in it, and the claim should be legible.

### Why

Q3 is the cheapest falsifiable thing available and the doc already declares it a
gate on M7, so doing it first is following the spec rather than reordering it.
M7 is genuinely dimension-free, so nothing built there is at risk from a coupon
result.

B was rejected on the strength of §11 Q1: the "just use a finer nozzle" fallback
has *one direct counterexample and no supporting evidence*, and the answer may be
*"neither nozzle, without a rib."* Shipping `brick` geometry whose dimensions no
one has measured means asking for review of numbers that carry no information yet.

A also produces something C cannot. §8.5 of the evaluation admits `CLAUDE.md` is
untested and that no design doc has yet been written under it. M7's design doc
will be the first — which makes it the test case for whether the four rules
change what an audit finds. C widens the baseline but cannot test the rules;
it stays available as follow-on work.

### What would reverse it

Coupons get printed → M6 unblocks and moves to the front. Q3 finds that
`unionPatternFaces` does cancel interior voids → §7.2's inset step has the same
exposure and both need fixing before any of M7 is trustworthy.

---

## D-004 — Decisions live in this file

**Date:** 2026-07-30 · **Status:** Decided (owner) · **Repo:** 3d-models

### Context

3d-models had no decisions convention. bikar has `docs/decisions/` with a
generated ledger and a coherence gate.

### Options

| | Option | Cost |
|---|---|---|
| A | One dated `docs/decisions-log.md` | One file, gate-checked |
| B | Append a §9 to `issue-register-evaluation.md` | Pushes that file past 500 lines |
| C | Mirror bikar's `docs/decisions/` + generated ledger | Four files and a generator for three decisions |

### Decision

**A — this file.**

### Why

B was rejected by the target document's own content: it quotes Nygard's *"large
documents are never kept up to date"* while already running past 460 lines, and
decisions taken *after* a measurement are not part of the measurement. C is real
scaffolding — a directory convention, a generator, a gate — proposed for three
entries, and the repo's standing precedent on new machinery
([`dsl-extension-skill-evaluation.md`](dsl-extension-skill-evaluation.md),
[`issue-register-evaluation.md`](issue-register-evaluation.md)) is that it has to
be earned by measured recurrence first. It stays available if this file outgrows
itself.

### What would reverse it

This file passing roughly 400 lines, or two people needing to append to it
concurrently → adopt C, which is what the per-file shape solves.

---

## Corrections

### C-001 — Task #13's premise measured the wrong object (K5)

**Date:** 2026-07-30

Task #13 read *"5 codespell failures; 93 `format:check` failures"* in
bikar/qiyas. Re-measured on 2026-07-30, bikar's actual CI gates are clean:

```
npm run format:check  →  All matched files use Prettier code style!
npm run spelling      →  clean (codespell packages)
```

The failures I had been quoting came from `npx prettier --check .`, which walks
the whole tree — markdown, vendored `supabase/functions/*` — while the repo's
own gate is a narrow glob over `packages/*/src`, `packages/*/tests`, `scripts`,
and `packages/web/functions`. The two measure different sets, and only one of
them is the gate. That is a **K5** by
[`grounding-defect-taxonomy.md`](grounding-defect-taxonomy.md): measured the
wrong object, then reasoned about the number as though it were the right one.

It reached a plan because a number that *looks* like a gate result was not
checked against the gate that produces it.

**Rule:** quote a repo's own script, not a tool invoked directly —
`npm run format:check`, not `npx prettier --check .`. When they disagree, the
script is the gate and the direct call is a different question.

qiyas's half is still unmeasured; task #13 should be re-scoped to that alone.

---

## D-005 — Build the Lego Lab UI now; the knobs are how the constants get tuned

**Date:** 2026-07-30 · **Status:** Decided (owner, superseding D-003) · **Repos:** bikar, 3d-models

### Context

D-003 deferred M6 because [`lego-lab-design.md`](lego-lab-design.md) §10 says
the clutch coupons *"block M6's dimensions"*, and the coupons need a printer.
The owner's direction: build the Lab UI, with the disputed values exposed as
adjustable parameters, *because* real prints are coming and the Lab is where
their feedback lands.

### Decision

**Build M6 + M7 + P0.** Every constant the coupons were supposed to settle —
`ribMm`, `engage`, `studDia`, `pinDia`, `tubeDia`, wall clearances — ships as a
Lab knob backed by a `CAL-*` bet, not as a baked default.

### Why this overturns D-003

D-003's objection was: *"shipping `brick` geometry whose dimensions no one has
measured means asking for review of numbers that carry no information yet."*

That is only true of a **baked constant**. A knob is not a claim about the right
value — it is the instrument for finding it. The design doc already says this in
its own §8: LG-F1 is *"a five-rung rib-thickness ladder (`ribMm` 0 / 0.05 / 0.10
/ 0.15 / 0.20) … crossed with `engage` 1.6 / 3.2 / 8.0."* That coupon **is** a
parameter sweep. Building it as a printed matrix and building it as a Lab sweep
strip are the same act; the Lab version can be re-run after each print instead
of requiring a new plate.

So the dependency inverts. Not *coupons → constants → M6 → Lab*, but
*Lab with knobs → prints → tuned constants*. The coupons stop being a gate and
become the Lab's first input.

**What does not change:** a knob is not a measurement. The Lab must show, per
value, whether it came from a coupon or is still a default — §9 already requires
this (*"the panel must say when the active profile came from a coupon and when
it is a default"*), and it is the line that keeps this decision from quietly
re-becoming the thing D-003 refused. A `CAL-*` id with no record behind it must
read as *unmeasured* in the UI, not as a number.

### What would reverse it

Prints show the geometry is structurally wrong rather than mis-dimensioned — §11
Q1's *"neither nozzle, without a rib"* outcome — in which case `studs full` and
`studs edge` ship disabled and the knobs for them come out. That is a scope
change the Lab surfaces rather than hides.

### Order of work

1. **Q3** — the `unionPatternFaces` interior-void test. Unchanged from D-003:
   §11 makes it a precondition of M7, it is cheap, and a failure invalidates
   both the anchor solver and §7.2's inset.
2. **M6** — `brick` declaration, `kernel3d/brick.ts`, ribs, validators V1–V10.
3. **M7** — anchor solver, grid gate, `sweepGridFit`.
4. **P0** — the Lab page, knobs, lattice overlay, both gate panels, sweep strip,
   STL download, `make lego-lab`, gallery section.

---

## D-006 — Multi-piece export for bricks is studs-as-ports

**Date:** 2026-07-31 · **Status:** Decided (owner) · **Repos:** bikar, 3d-models

### Context

[`lego-lab-design.md`](lego-lab-design.md) §10 lists **multi-piece export** in
P1. Scoping it surfaced a defect: a `brick` accepts a declared socket-role
`port`, an `assembly` will `connect` a rod into it, and the C2 fit ladder checks
the pin against the socket diameter and passes — but `buildBrick` never reads
`decl.ports`. Only `hole` cuts material, and `brick` has no `hole` statement. The
exported mesh is byte-identical with and without the port: `Panel-Left.stl` is
3764 triangles either way.

So P1 had nothing to decompose, and §1's non-goals ruled out the joint that
normally would. The three options were argued with compiled sections in the design note
`multi-piece-export` — bikar `packages/lab/src/design/notes/multi-piece-export.ts`,
read at `design.html?n=multi-piece-export` after `make lab` (the page is
`preview` status and is not published yet). It is the first note written under
the [`design-note`](../.claude/skills/design-note/SKILL.md) skill.

Shipped in bikar `617bee1` (PR #34, the note as `preview`) and `3b31fab`
(PR #35, the note closed to `decided` and the validator below).

### Decision

**Studs as ports.** `brick` auto-mints stud and tube ports on the stud lattice;
an `assembly` connects `Top.tubeN` to `Base.studM` and `export parts` writes one
STL per brick, each plated on its own bottom face.

### Why, against the two it beat

The deciding fact is on the drawing: **both shapes are already in the exported
mesh.** The note cuts the same `ClassicBrick` twice — once through the anchor row
(the tubes that receive) and once through a stud row (the studs received) — and
neither section contains a line the kernel does not already emit. The option
names geometry; it does not add any. That is the opposite of the defect above,
where the fit ladder described a socket nothing had cut.

*Refuse the phantom* is the smallest scope and stays correct, but the only
assembly a user could actually reach is `Pinned-Tiles.bkr`, a **C2 tile**
assembly. The Lego Lab would ship a feature its own catalogue never triggers,
which satisfies the P1 line in letter and not in fact.

*Real hole* contradicts §1's stated non-goal — *"Technic geometry (axle holes,
pin holes, ⌀4.8 bars)"* — and the section shows why that non-goal was not
arbitrary: the bore passes through the ceiling and the shell wall, between two
tubes the anchor solver placed. Widening §1 may be right one day, but arriving
there as a side effect of a P1 checkbox is how a non-goal dies unnoticed.

Studs-as-ports is the largest scope of the three — two port kinds, a stud-index
naming scheme that survives a footprint change, a pose solver for the assembled
preview, and a clutch-fit rung for printed-onto-printed. It is taken with that
cost stated, not discovered.

### Built — bikar `c60faf2` (PR #36), 2026-07-31

Three of the four stated costs were not costs: the pose solver and `export parts`
were already generic over the piece registry, so the work was the minting and the
contract. The naming scheme was real and resolved as a **lattice coordinate** —
`stud_c<col>r<row>`, `anti_c<col>r<row>` — because an ordinal renumbers when the
footprint grows and would silently re-point an assembly written against the
narrower brick. `patterns/Assemblies/Brick-Stack.bkr` is the worked example.

The printed-onto-printed rung reported back, and it is the finding: **on the
shipped defaults there is no clutch.** Total radial interference computes to
0.00 mm, because the fit profile's −0.2 mm diametral offsets are calibrated for
a printed part meeting a *moulded* one — one shrinking side — and brick-onto-brick
applies them twice. `brickFit { studDiaMm 0 }` applies them once and the joint
grips. This is the reversal condition the decision named, *almost*: the stud is
still a joint, but only once someone states which process the number came from.
`CAL-STK-01` is the bet on the real entry ceiling and `LG-S1` the coupon that
settles it. Recorded as a **K10** in the port module, the test, bikar's
`docs/language-reference.md`, and the pattern header.

### Unconditional, regardless of this choice

A `brick` must not mint a socket-role port that cuts no geometry. That is a
validator and a test, and it ships whichever option had won — under this one it
still fires, because a *hand-declared* socket-role port on a brick remains
uncut. Per the graduation rule the test fails before the fix and passes after.

### What would reverse it

The printed-onto-printed clutch turns out not to hold — a stud printed on a
Lego-compatible tube either seizes or falls out across the whole fit ladder, so
no rung of the sweep is green. Then a stud is a shape, not a joint, and the
multi-piece path falls back to *refuse the phantom* with the reasoning here
intact. This is a measurement, so it is a `CAL-*` bet and not an argument: the
reversal condition is a coupon result, not a re-reading of this entry.

---

## D-007 — §5.3's rhombic row gets a label, not a wider grammar

**Date:** 2026-07-31 · **Status:** Decided (owner) · **Repos:** 3d-models

### Context

§5.3's lattice matrix is now measured — five bases swept across 2–20 mm,
[`research/lego-lattice-matrix-sweep.md`](research/lego-lattice-matrix-sweep.md).
Measuring it surfaced a gap between the table and the language. `gridFit` scores
any translation basis handed to it, while `env.repeatVectors` is assigned in
exactly one place, `packages/core/src/dsl/evaluator.ts`, and admits exactly two
shapes: `[(dx,0), (0,dy)]` for `mode rectangular` and `[(dx,0), (dx/2,dy)]` for
`mode hex`. A 72° rhombus is neither. So one row of the table described a
lattice **the gate can score and no `.bkr` can produce**, and a reader had no
way to tell which rows those were.

That is a **K7** — a document disagreeing with the machinery it ships, findable
by reading one against the other and needing no new research.

The three options were argued with the geometry compiled beside them in the
`lattice-basis` design note (bikar `packages/lab/src/design/notes/lattice-basis.ts`,
read at `design.html?n=lattice-basis` after `make lab`), the second note written
under the [`design-note`](../.claude/skills/design-note/SKILL.md) skill.

### Decision

**Label the row.** §5.3's table gains an **Authorable** column stating, per row,
whether a script can reach that lattice, plus the paragraph naming the single
assignment site that decides it. The grammar is unchanged and no row is removed.

### Why, against the two it beat

The note's figures moved the argument, and not in the direction the question
implied. The framing was "one unbuildable row against two buildable ones", and
what the drawings showed is that **scale is the variable that matters and it is
not enough**: the same 3 : 2 rectangular lattice scores **0.41 at 8 mm and 1.00
at 16 mm**, while hexagonal — a basis the grammar *already* expresses — tops out
at **0.8037** anywhere in the swept interval. So a low score is not a symptom of
a missing grammar feature. Widening the grammar would not have raised a single
number in the table; it would only have let an author write down a lattice that
still cannot register.

*Widen the grammar* is the largest scope — tokens, lexer, parser, AST, the
single evaluator assignment, the tiling loop (which steps an axis-aligned basis
today), the EBNF spec and its differential corpus gate, the language reference,
and tests — and it buys authorability of a basis whose measured ceiling is 0.73.
It is not refused on principle; it is refused because nothing currently needs it.

*Cut the row* is small, and destructive in the one place it matters. The 72°
rhombus is the 5-/10-fold case, which is the case this project exists for. The
hexagonal row would still carry the "irrational ratio never registers" argument,
so the point survives — but the reader who came to the table asking about a
5-fold star would find their case silently absent, which is a worse failure than
finding it present and marked.

Labelling costs one table column and one paragraph, and it converts the K7 from
a contradiction into a stated fact. It is the option that leaves the other two
open.

### What would reverse it

A pattern someone actually wants to build needs a basis the grammar cannot
express — not a row in a sweep, but a `.bkr` a person sat down to write and
could not. Then *widen the grammar* becomes the right call and this entry is the
record of what it costs. The **Authorable** column is also the detector: if it
ever needs a fourth distinct value, the two-shape restriction has stopped
describing the language and the column has become the thing it was meant to
document.

The reversal condition explicitly **is not** a low score. That was the confusion
this decision cleared up.

---

## D-008 — W-F1 is a new clip-in-notch coupon; the bore ladder keeps its own job

**Date:** 2026-08-02 · **Status:** Decided (owner) · **Repos:** 3d-models, bikar

### Context

Three documents disagreed about what catalog entry **W-F1** is, which
[`backlog.md`](backlog.md) §7 item 1 had already flagged without resolving.
[`catalog.md`](../.claude/skills/prototype/catalog.md)'s W-F1 *prose* asked
clipseat questions — which clearance seats a clip firmly, does it differ by tile
material — while its **Model** line pointed at `Fit-Coupon.bkr`, which is a plate
of bores and pins. [`w2-connector-design.md`](w2-connector-design.md) §8 named a
third thing, `Fit-Step-Gauge.bkr`, a file that has never existed in any repo.

Reading the geometry rather than the docs settled which description was wrong.
These are two different joints:

- **bore-and-pin** — a peg travelling straight into a hole. One axis, full
  contact around the circumference, no rotation. `Fit-Coupon.bkr` and MC-1's
  `MC1FitLadder` measure this.
- **clip-in-notch** — a bayonet blade dropping down the 1.2 mm channel between
  four tile corners and *then* sweeping sideways under load. Two motions, and the
  second one loads faces the first never touched.

A blade can pass the drop and bind on the twist. So the transfer sentence CLAUDE.md's
**K10** demands — *"this number transfers because …"* — cannot be written between
them, and the rule does not transfer. The catalog was not describing a coupon that
existed; the clip joint had no fit coupon at all.

A second defect fell out of the same reading. `Fit-Coupon.bkr` was cutting its
ladder at `+0.10 / +0.20 / +0.30` while the shipped `FIT_GAP_MM`
(`kernel3d/fit-profile.ts`) is `press −0.10 / snug +0.05 / sliding +0.15 /
free +0.35`. It had drifted from the constant it calibrates and nothing noticed,
because only one of its rungs carried a `connect`.

### Decision

**Two files, one job each.**

1. **W-F1 becomes `patterns/Coupons/Clipseat-Fit-Coupon.bkr`** — new, on its own
   plate: one 40 mm clipseat dummy tile plus five `CornerClip`s whose declared
   `gap` walks the blade clearance `0.40 / 0.30 / 0.20 / 0.10 / 0.00`. Rungs are
   named for the clearance, not the knob, so the names stay true if `wall_gap`
   moves. It prints before W-C1 because W-C1 consumes its number.
2. **`Fit-Coupon.bkr` keeps its bore-and-pin role** and its ladder is re-cut to
   the shipped `FIT_GAP_MM`, with one `connect` per fit class so a future edit to
   the constant stops the file evaluating instead of drifting again.

### Why, against the alternatives

*Fold W-F1 into W-C1* was the cheapest and is the one the sequencing rules out.
W-C1 decides rebate-vs-proud, the Z stack and the detent feel; it is the coupon
that spends the clearance number. A plate that has to settle the clearance and
the joint at once cannot tell a bad clearance from a bad jaw, which is the
contamination MC-1 splits its own two plates to avoid.

*Re-point the prose at the bore ladder* — i.e. declare W-F1 to have always been
about bores — was the smallest diff and would have made the catalog self-consistent
and wrong. It also has no work left in it: MC-1's `MC1FitLadder` measures the same
ladder at six diameters instead of one, so W-F1 would have become a duplicate of a
better coupon while the clip joint stayed unmeasured.

*Change `FIT_GAP_MM` to match the coupon* was available for the second defect and
is backwards: the coupon exists to measure the constant, so moving the constant to
whatever a stale file happened to say would destroy the only thing the file is for.

The ladder is deliberately built to be able to **fail at both ends**, which is what
distinguishes it from a coupon that can only return "yes". `C00`'s blade exactly
fills the channel; if it drops through, the finding is not "0.00 works" but that
this machine undersizes blades or oversizes channels, and the reading measures
*that*. `C40` sits on the two-perimeter floor (`2 × PERIMETER_WIDTH_MM`); if it
drops freely and shears on the twist, the blade has stopped being a structural
member. Both bounds are asserted in `corner-clip.test.ts`.

The confound is stated rather than hidden: the declared gap moves the blade width
*and* `rPadOutMm = rJaw − gap/√2`, the pad's reach over the border band, together.
That is accepted because the deliverable is one number to declare, not a
decomposition — and a failed rung still distinguishes them by inspection (a blade
that will not enter is the blade; a clip that enters, twists, then rocks is the
reach).

### What would reverse it

Measure the two joints and find the numbers agree. If the blade clearance W-F1
returns lands inside MC-1's snug window, the joints are behaving as one joint on
this machine and the transfer sentence K10 asked for can finally be written — at
which point `Clipseat-Fit-Coupon.bkr` becomes a confirmation coupon rather than a
gate, and W-C1 stops being blocked on it.

The reversal condition **is not** the two files looking redundant on paper. They
looked redundant on paper for the whole period in which one of the two joints had
no coupon at all.

---

## D-009 — The LDraw read-back is a studio panel, not a CI gate

**Date:** 2026-08-02 · **Status:** Decided (owner) · **Repos:** bikar, 3d-models

### Context

Until 2026-08-02 the LDraw export was only ever validated **by its own author**.
`ldraw-emitter.test.ts` has thirty-odd cases and they are good cases, but every
one of them checks bikar's output against bikar's reading of the LDraw spec. A
misreading of the spec passes all of them. Nothing outside bikar had ever parsed
the file.

[`ldraw-cli-viewers.md`](research/ldraw-cli-viewers.md) surveyed twelve
candidates for fixing that and recommended two: LDView for a picture (§1.2), and
three.js `LDrawLoader` in Node for a machine-checkable parse (§1.4), which it
called *"the route to put in CI"*. Neither had been run. LDView still has not
been — it installs from a `.dmg`, not Homebrew.

The §1.4 route was run on 2026-08-02 and the export **opens**: both type-1 lines
resolved against the inline `0 FILE` block with no parts library on disk. §8
records the run and the three §1.4 claims it falsified.

### Decision

**Wire `LDrawLoader` into the Lego Lab in bikar studio, behind the LDraw export
button. Do not add the headless CI gate §1.4 proposed — yet.**

The reasoning is that in studio these are not two things. `LDrawLoader` is a
browser library, studio is a browser app, and the Lego Lab already exports
LDraw. Rendering the preview *through the loader* means the picture on screen is
a foreign implementation's reading of the exact bytes the download button hands
over. The preview cannot drift from the validator because it **is** the
validator: an export that stopped resolving would stop drawing.

A headless CI case would assert the same invariant with none of the visibility,
and would be a second place for the same assertion to live. If the panel turns
out to be something people click past rather than look at, that is the signal to
add the CI case — not before.

Two traps from §8.2 are load-bearing for the implementation and are recorded
here so the panel does not rediscover them:

- `addDefaultMaterials()` throws unless `setConditionalLineMaterial()` is called
  first (three ≥ 0.18x). §1.4's recipe omits this and does not run as written.
- `addDefaultMaterials()` registers **only colour codes 16 and 24**. Our
  placements carry code 7, so a panel that stops there renders magenta. It needs
  a real `LDConfig` subset, or it will look broken while being correct.

### What would reverse it

The panel shipping and then being ignored — nobody looking at it, exports going
out unlooked-at. Then the invariant needs somewhere that fails loudly without a
human, and §1.4's vitest case is the answer that was passed over here.

---

## D-010 — Do not certify BFC until the winding's *handedness* is established

**Date:** 2026-08-02 · **Status:** **Reversed the same day — see D-012** ·
**Repos:** bikar

> Superseded 2026-08-02. Its reversal condition fired within the hour: the
> handedness was measured off the emitted bytes and confirmed against a
> consumer that culls. The entry is kept because the condition it named is the
> reason the reversal was cheap, and because the refusal was correct on the
> evidence available when it was made.

### Context

The read-back returned 15,056 triangles for a file containing 3,764 type-3
lines. `LDrawLoader.js` explains it: `doubleSided = ! bfcCertified || ! bfcCull`,
then `totalFaces += doubleSided ? 2 : 1`. Our MPD carries no `0 BFC CERTIFY` —
an omission the emitter makes deliberately, asserted by the test *"omits
`0 !LICENSE` and `0 BFC` — both deliberate"* — so a conforming consumer builds
every triangle twice, in both winding orders.

The tempting move is to certify. The emitter has already done the hard part: its
tests assert the axis map is a proper rotation (*"determinant +1, so triangle
winding survives"*) and that a mirroring placement is **refused** rather than
inverted silently. Winding is known-consistent. Certifying would halve what every
consumer builds.

### Decision

**Leave `0 BFC` off until it is established that our winding is CCW in LDraw's
own convention — not merely self-consistent.**

Consistency and handedness are different claims and the emitter's tests only
support the first. `0 BFC CERTIFY CCW` on CW geometry is worse than no
certification at all: an uncertified file makes a consumer draw both sides, which
is always correct and merely wasteful, while a wrongly-certified file makes it
cull the faces it should keep, which is silently wrong. The current state costs
3,764 redundant triangles on a model that renders instantly.

This is the **K1** rule applied to our own test suite. "Determinant +1" is a
hedge-bearing statement about a rotation being orientation-preserving; reading it
as "therefore CCW in LDraw's frame" strips the qualifier and asserts something
the test never checked.

### What would reverse it

Establishing the handedness — from the axis map composed with LDraw's stated
face-winding convention, confirmed by a consumer that actually culls. Then
`0 BFC CERTIFY CCW` is free and should ship.

---

## D-011 — One authorized upload to LDraw.org, as a tiebreaker

**Date:** 2026-08-02 · **Status:** Decided (owner) · **Repos:** 3d-models

### Context

`https://library.ldraw.org/model-viewer` is candidate 12 of the twelve in
[`ldraw-cli-viewers.md`](research/ldraw-cli-viewers.md) §3. It is the only one
that explicitly documents our exact case as supported — *"All parts used in the
file submitted to the model viewer must be embedded in the MPD, be present in the
Official Library, or listed on the Parts Tracker"* — and the only one that
requires **sending our geometry to a third party**: *"The model submitted here is
uploaded to LDraw.org for processing."*

§6 item 12 set the condition in advance: *"It should not be used as the routine
check. It is, however, a legitimate one-off tiebreaker if every local route
fails, provided a human decides the upload is acceptable."*

The local route did **not** fail. But it also did not produce a picture, and no
official LDraw implementation has read the file — three.js is a third-party
reimplementation, and LDView is still an uninstalled `.dmg`.

### Decision

**Upload once, with the owner's explicit authorization, given 2026-08-02.**

The stated condition ("if every local route fails") is not met and this decision
does not pretend otherwise — it is an owner override of a bar this file set, made
knowingly, for the one thing the local route cannot supply: a rendering by an
implementation LDraw.org itself hosts.

Scope is one file, once. `Brick-Stack.mpd` is 213 KiB of generated brick
geometry with no proprietary content and nothing derived from anything but our
own DSL. The routine check stays local and stays §1.4's.

### What would reverse it

Nothing to reverse — it is a single act, not a standing practice. What would
**extend** it is exactly what §6 item 12 says: every local route failing. Making
this the routine check without that is the thing to refuse.

---

## D-012 — D-010 reversed the same day: certify CCW

**Date:** 2026-08-02 · **Status:** Decided (owner) · **Repos:** bikar, 3d-models
· **Supersedes:** D-010

### Context

D-010, decided this morning, declined to emit `0 BFC CERTIFY CCW` and wrote its
own reversal condition:

> Establishing the handedness — from the axis map composed with LDraw's stated
> face-winding convention, confirmed by a consumer that actually culls. Then
> `0 BFC CERTIFY CCW` is free and should ship.

Both halves were met within the hour, and neither needed anything installed.

**The stated convention** was already in the repo, read first-hand in
[`lego-ldraw-export.md`](research/lego-ldraw-export.md) §4 — S1 verbatim,
*"LDraw uses a right-handed co-ordinate system where -Y is 'up'."* A
right-handed reading is therefore the correct one, and the signed volume of the
emitted block's 3,764 type-3 lines in that reading is **+62,282 LDU³**: wound
counter-clockwise as seen from outside.

**A consumer that culls** turned out to be the one §8 already had running.
three.js honours `0 BFC`. Feeding it the same bytes three ways
([`ldraw-cli-viewers.md`](research/ldraw-cli-viewers.md) §9.2) separates the
right certification from the wrong one, which a face count cannot: `CERTIFY CCW`
builds 3,764 faces at **+62,282 LDU³**, `CERTIFY CW` builds 3,764 at
**−62,282 LDU³**. Outward versus inside-out, same count, opposite sign.

### Decision

**Emit `0 BFC CERTIFY CCW` in the inline block. Keep `0 !LICENSE` off.**

D-010 was right to refuse on the evidence it had, and the refusal cost about
four hours. What made it cheap to reverse is that D-010 named a condition
rather than a preference — "until the handedness is established" is a thing
that can be established, where "it feels premature" is not.

Note what actually moved. The *derivation* is unchanged and was never in
doubt: `lego-ldraw-export.md` §5.3 had it in April, the emitter's docstring
restates it, and D-010 restated it again. Three documents agreed on the
conclusion and all three declined to act on it, because each carried the same
hedge — *"I did not render the output in a BFC-checking viewer."* The hedge was
correct and it was also, for that whole period, one `npm i three` away from
being dischargeable. **A hedge that nobody prices is a hedge that never
expires.**

`0 !LICENSE` is untouched by this and stays off: it asserts a CC BY 4.0 grant
over the geometry that nobody in this project has made, which is a question
about permission and not about winding.

### What would reverse it

A BFC-checking consumer that culls our certified file's *outward* faces —
i.e. disagrees with three.js about what `CCW` means here. LDView is the one
that matters, since it is what a person is most likely to open the file in, and
it is still un-run. If it renders the certified file inside-out, the line comes
straight back out and §9.3's "for three.js, and only for three.js" is why this
entry does not claim more than it measured.

### The graduation

Per CLAUDE.md, the obligation is the test that fails before and passes after.
It is a bikar unit test asserting the emitted block's signed volume in LDraw
coordinates is positive **and** that the `0 BFC CERTIFY CCW` line is present —
the first is the precondition the certification rests on, so a future change
that silently flipped the winding would fail on the number rather than on the
line.

### As shipped — bikar PR #63, 2026-08-02

Two things the decision above did not say, decided while building it.

**Both blocks are certified, not only the inline part.** The decision said "in
the inline block", which is where the triangles are. But S7 makes certification
hierarchical — *"A file is only treated as being BFC-compliant if it and all of
its superfiles are compliant"* — with a stated exception for part files, on the
grounds that *"they are complex closed solids, so there is never a valid reason
to invert them."* Certifying only the part would have made the file readable
*by way of that exception*. Certifying the main block too means it never has to
be granted. The main block asserts nothing false: it holds only type-1 lines,
and `ldrawPlacementMatrix` already refuses a mirroring placement, so there is no
`0 BFC INVERTNEXT` being silently omitted.

**A wrong claim surfaced while measuring, and it was on our side.** The
read-back panel reported an uncertified `Classic-Brick` as 7,528 triangles and
said "both sides kept". Neither survived a direct probe of the buffer: three
*sizes* the position array for two windings per face and fills only what it
draws, so half the entries are `(0,0,0)` under a `FrontSide` material. The
panel was counting reserved slots as geometry, and "both sides kept" was S7's
*"may not cull"* hardened into a claim about what a consumer draws — a **K1**,
found four days after the doc that made it. Corrected in
[`ldraw-cli-viewers.md`](research/ldraw-cli-viewers.md) §9.4, with its own
validator, and fixed in the same PR: `triangles` counts area, `degenerate`
reports the slots, and the panel's `|volume| < 1` verdict — which could never
fire on a real brick — is gone.

This changes nothing about the certification. The three measured rows of §9.2
stand; it was the word in the fourth column, not the numbers, that was inferred
rather than measured.

---

## D-013 — Murals cut art at nominal grid lines, and a printed-part set is not an L78 mosaic

**Date:** 2026-08-02 · **Status:** Decided (owner) · **Repos:** 3d-models, bikar

### Context

Two questions had to be settled before the `mural` family could ship, and they
travel together because both are about what the family *is*.

**Where does the art get cut?** A mural's pattern is one planar graph split
into c×r pieces whose physical bodies are `8n − 0.2` mm on an 8.0 mm stud
pitch. Two candidate rules were on the table:

- **Nominal-line cut (taken).** Art is cut at pure multiples of 8.0 mm; the
  body then clips 0.1 mm per side at build time, so exactly 0.2 mm of art is
  interrupted per seam. The cut lines are injected into the pattern's own
  planar-graph extraction, so both sides of every seam carry bit-identical
  vertex coordinates by construction
  ([design §5](lego-pattern-set-design.md)).
- **Gap-registered cut (rejected).** Pre-shrink each piece's art to the
  `8n − 0.2` body so relief runs flush to the physical edge. Rejected because
  it double-counts the inset — `PART_RELIEF_MM` transfers as a *physical-gap
  prediction*, not a pattern-registration offset, which is the repo's named
  K10 defect ([design §3.2](lego-pattern-set-design.md)) — and because a
  per-piece offset mints per-piece coordinates, demoting seam continuity from
  an identity to a tolerance claim needing its own gate.

**Is this the mosaic lego-lab ruled out?**
[`lego-lab-design.md`](lego-lab-design.md) L78 lists "stock-part mosaic
generation and BrickLink/Rebrickable BOMs" as an LG non-goal, and `mosaic` was
accordingly rejected as the declaration's name (bikar decision
`2026-08-02-mural-panelization`). The ruling: L78 excludes composing pictures
out of *purchased* LEGO parts — palette quantization, part BOMs. A mural is
the other branch: **printed** pieces carrying continuous engraved relief that
no purchasable part has, mounted on a stock baseplate. The non-goal stands
untouched; the family does not enter it
([design §1](lego-pattern-set-design.md)).

### Decision

Art is cut at nominal 8.0 mm grid lines; no art offset is ever applied; the
0.2 mm at each seam is the design's stated price. Printed-part pattern sets
are in scope and `mural` is their name.

### What would reverse it

**LG-P1's physical measurement, and only that.** The nominal-cut rule's
geometry is proven in software — bikar's `mural-split` tests assert the seam
vertex identity to 1e-12 and the area ledger to 1e-9 — so no further argument
or render can move this entry. What can move it is the two-piece
seam-registration coupon on a real LEGO-brand baseplate (CAL-REG-01,
[bets.md](../.claude/skills/calibrate/bets.md)): if a relief line crossing the
seam visibly jogs by more than the 0.2 mm gap predicts — stud-bore slop and
plate pitch error compounding into misregistration the nominal cut cannot see
— then the cut rule needs an art-side correction term, and it would be a
*measured* one, not a re-derivation of the K10 offset rejected above. Held
pending a printer, like everything print-gated.

### The graduation

The tests already exist on the bikar side (seam identity, ledger closure,
V-M5 containment — `packages/core/tests/kernel3d/mural-split.test.ts`), which
is why this entry records the *decision* and not the defect: what cannot be
asserted in vitest is that the gap-registered alternative was considered and
why it lost. That is what this file is for.

---

## D-014 — `make coupons` ships as a gate with a build target for a front door

**Date:** 2026-08-03 · **Status:** Decided · **Repos:** 3d-models

### Context

[`backlog.md`](backlog.md) §4 item 2 and open question 11 left this undecided,
and question 11 was careful about *why*: the repo's twice-measured precedent is
to prefer a gate over new machinery
([`dsl-extension-skill-evaluation.md`](dsl-extension-skill-evaluation.md),
[`issue-register-evaluation.md`](issue-register-evaluation.md)), but neither of
those evaluations is about a build target, so the precedent does not transfer
cleanly. That is the K10 sentence the backlog wrote rather than assumed, and it
is what kept the question open.

Three options were on the table:

- **Nothing** — keep typing §6's lines. Rejected on evidence, not taste: §6
  carries two rules a hand-typed session drops without producing any error.
  `--piece` is mandatory (without it the CLI renders the file's last solid —
  "a valid render and a useless coupon"), and the four sub-floor MC-2 rungs
  must run *without* `--check` or they write nothing. Both failures look like
  success at the shell.
- **A thin target** that re-types §6 into the Makefile. Rejected: it creates a
  second copy of the command lines, so the doc and the build can disagree, and
  it still verifies nothing. `backlog.md` §4 called the target "a judgement
  call and not an obligation" and it was right — the *target* was never the
  valuable part.
- **A verifier with a target as its entry point (taken).**
  [`build/verify_machine_card.py`](../build/verify_machine_card.py) reads the
  rung list and the whole expectation table out of
  [`calibration-design.md`](calibration-design.md) §7, renders each rung, and
  diffs the mesh gate's actual output against the row. No number and no rung
  name is restated in the Makefile or the script.

### Decision

`make coupons` renders and verifies; `make validate-coupons` self-tests the
verifier. §7's table is the spec, and the only copy of it.

The load-bearing detail is what the verifier does with the four rungs §7 marks
**FAIL — by design**. MC2Wall04/06/08/10 sit under the 1.2 mm feature floor on
purpose — rejecting them is what MC-2's wall ladder measures. A verifier that
asserted "every rung PASSes" would have to be wrong about those four or skip
them, and skipping is how a gate quietly stops testing the thing it exists for.
So each of the four is rendered twice: once bare, to write the STL §6 asks for,
and once under `--check` to assert it *fails*, at the minFeature §7 names. This
is the one claim in §7 that §6's own command line cannot demonstrate, because
§6 deliberately never runs `--check` on them.

Two further self-consistency checks come free and are K7 by construction: §6's
shell block and §7's table must name the same rungs, and the 23 measured
volumes must sum to the 89.7 cm³ §7 states.

### What would reverse it

A false alarm. `.claude/gates/docs_gate.py`'s house rule is that a gate which
cries wolf gets switched off, which is worse than no gate — so if the verifier
starts failing for reasons that are not drift between the doc and the geometry,
it should be narrowed or removed rather than tolerated. One near-miss already
happened during authoring and is worth recording: the first piece-set
cross-check read `MC1FitGaugePress` out of a §6 *comment* whose entire purpose
was to say that rung is deliberately not rendered, and reported a correct doc as
broken. Comments are now stripped before the command lines are parsed.

Floating-point noise was the other candidate and is handled by construction:
each number is compared at the precision §7 chose to print it, so
`minFeature=4.999999965721486` matches a row that says `5.000` without a
tolerance constant anyone has to justify.

### The graduation

`make validate-coupons` — seven mutations applied to a scratch copy of the doc,
each asserting the verifier fires: a drifted triangle count, euler, and
minFeature; a by-design FAIL relabelled `PASS`; a passing rung relabelled `FAIL
— by design`; a rung rendered by §6 that §7 does not tabulate; and MC-6 losing
the F7 warning it exists to raise. The fourth and fifth are the pair that
matters, because they pin the by-design label from both sides — it can neither
be tidied away nor used to hide a real failure. All eight cases (seven plus the
unmutated control) behave as documented as of 2026-08-03.

---

## D-015 — the use-case map's own pin must be *reachable*, not merely resolvable

**Date:** 2026-08-03 · **Status:** Decided · **Repos:** 3d-models

### Context

D-014's PR was squash-merged, and the squash orphaned the commit the use-case
map pinned. Every check kept passing: `git cat-file -e` resolved the object,
`git rev-list --count pin..HEAD` returned a number, so even the staleness
warning stayed quiet — all because the pre-squash commit was still sitting in
*this* clone as a dangling object. A fresh clone of `master` cannot resolve it
at all, and all 116 pointer checks fail together at the first one.

The gate had a check for the wrong thing. "This hash resolves here" is not the
claim the frontmatter makes; the claim is "these pointers are valid at a commit
anyone can fetch," and only reachability distinguishes the two.

### Decision

`validate.py`'s full mode errors when this repo's `as_of` is not an ancestor of
HEAD, naming the squash merge as the usual cause and `--refresh` as the fix.

**Self-repo only, deliberately.** A sibling is pinned at its own published ref
(`refresh_target` prefers `origin/HEAD`) and has every reason *not* to be an
ancestor of whatever its checkout has on HEAD — bikar's branches are built in a
worktree that shares one object database, which is the case `staleness_warning`
already documents. Applying the ancestry rule to siblings would fire on the
normal state of every sibling checkout here, and a gate that cries wolf gets
switched off.

The alternative considered and rejected was pinning this repo to `origin/master`
rather than HEAD, which would make orphaning structurally impossible. It breaks
the ordinary case instead: a PR that adds a file *and* a pointer to it cannot
validate against a published tip where the file does not yet exist. That case
is already the reason `USE_CASES_OK=1` exists, and making it unrepresentable is
worse than detecting the rarer failure after the fact.

### The graduation

A real git fixture in `validate.py --self-test` builds a branch, squash-merges
it to `master`, deletes the branch, and asserts three things in the state that
shipped: the orphaned pin errors, the object *still resolves* under
`cat-file -e`, and `staleness_warning` *still returns None* on the count that
`rev-list` happily produces. The last two are the point — they pin the reason
the pre-existing checks could not see this, so a later simplification cannot
quietly reintroduce it. A sibling pin at the same orphaned commit is asserted
to stay silent.

---

## D-016 — `checker` gets a shared `border` spec *and* a per-pair validator

**Date:** 2026-08-03 · **Status:** Decided · **Repos:** bikar (grammar + validator), 3d-models (doc)

### Context

[`tile-wall-design.md`](tile-wall-design.md) §10 Q2, open since the doc was
written: `checker` alternates two tile types across a wall, and every A–B
adjacency is a joint. If the two types disagree about edge gap, clip type or
clip position, the wall does not assemble. Enforce that by construction, or
detect it per pair?

### Decision

Both, and in that order.

A `border` declaration is the path `checker` is documented on: two tile types
that reference one `border` cannot diverge, so the common failure is not a
defect that gets caught — it is a state that cannot be written down. That is the
robustness-over-ease call.

A tile may still decline the shared spec and declare its own border, and then
the **per-pair validator** runs: walk every adjacency in the laid-out wall and
compare the border fields. Keeping this path open is deliberate — a deliberately
asymmetric pairing (a trim tile, a border course) is real tiling practice, and
D-017's `frame` needs exactly that freedom. Making it unrepresentable would have
forced a grammar change the first time someone wanted one.

### What still has to be built

The validator needs a **PASS:** and a **FAIL:** line per D2, and the `FAIL:` must
be the hard case, not the easy one. The easy counterexample is two tiles with
different `edge` gaps; the hard one is two tiles that agree on gap and clip type
but place the clip at different offsets along the edge — geometrically distinct,
trivially missed by a field-by-field compare that stops at type. Write that one.

Per D2's standing warning: **an aggregate cannot discharge a claim about every
pair.** Reporting "41 of 42 pairs agree" is not a pass, and one summary
comparison over the wall's distinct tile *types* is not a check of its
adjacencies — a `checker` wall with three types has pairs no type-level compare
visits.

### Amendment, 2026-08-03 — as built (bikar `2585a40`, PR #71)

Two corrections, both to the paragraph above. Recording them because the second
one **inverts** the counterexample that paragraph prescribed.

**1. The position field is a corner subset, not an offset.** The option chosen
for the clip position was `clipseat on ne,sw` — a subset of the tile's four
corners. The paragraph above describes it as "different offsets along the edge",
which is the wording the option preview used and is not what shipped. That cost
was stated when the option was chosen and this is the amendment it earned.

**2. The `FAIL:` above is the legal PASS.** A corner subset is *tile-local*, so
which vertices two neighbours actually share depends on the edge:

| joint | shared vertices |
|---|---|
| E–W, A left of B | A.`ne` ↔ B.`nw` · A.`se` ↔ B.`sw` |
| N–S, A below B | A.`nw` ↔ B.`sw` · A.`ne` ↔ B.`se` |

So `on ne,sw` beside `on nw,se` — the "geometrically distinct" pair the
paragraph above names as the hard failure — **mates at every vertex**. It is a
legal wall, and a must-be-identical rule would reject it. It is now the
documented `PASS:`.

The hard `FAIL:` is the opposite case: **two byte-identical `on ne,sw`
declarations**, which fail at *every* vertex, because a shared vertex is a
different corner of each of the four tiles meeting there. This is the one that
had to be written, and the one D2 exists for — a field-by-field compare reports
"identical" and ships a wall that does not assemble. The validator therefore
compares **seat state at a vertex**, not the two records.

The four-tile parity that makes this true is pinned at the kernel rather than
asserted in prose: for a complementary checker, the vertex at block `(c,r)`
seats a clip iff `(c+r)` is even, so exactly half the interior vertices seat
one. `packages/core/tests/kernel3d/tile-border.test.ts` asserts the literal clip
cells and both counters; the walk itself is
`packages/core/src/kernel/wall-borders.ts`, and it reports `pairsChecked` and
`pairsSkippedCropped` separately so the skipped cut edges stay visible.

**Graduation.** Building this found a live defect in G3's coverage gate: it read
only the `TokenType`-indexed dispatch table, and `border`'s head is an ordinary
identifier, so the gate stayed green with no `border` row for a declaration the
parser accepted. Fixed in the same change with a contextual-head table the
surface also reads, plus the test that fails before and passes after. It is the
same shape as the corollary in [`../CLAUDE.md`](../CLAUDE.md): a gate that
asserts "everything passes" has to be wrong about a deliberate failure or skip
it — here it skipped, silently, the newest thing it covered.

---

## D-017 — `frame` is orthogonal to `crop`, not a crop mode

**Date:** 2026-08-03 · **Status:** Decided · **Repos:** bikar (grammar), 3d-models (doc)

### Context

[`tile-wall-design.md`](tile-wall-design.md) §10 Q3 asked whether a cropped edge
tile keeps its relief clipped mid-motif, or whether the border band thickens to
absorb the cut — the tiler's trim strip, in-language. The doc leaned "offer
both", and sketched the syntax as `crop clip | crop clip with frame`.

### Decision

Offer both finishes — and **do not attach the frame to the crop.** `frame` is
its own wall-level statement; `crop` keeps deciding only what happens to a tile
the grid cuts.

The sketched `crop clip with frame` couples two things that are not the same
question. A frame is a finish on the wall's perimeter; a crop is what a
non-integer grid does to a tile. A wall whose grid divides evenly has no cropped
tiles at all and can still want a frame — under the coupled syntax that wall
could not ask for one, because it has no `crop` clause to hang it off. The
coupling also silently makes the finish depend on grid arithmetic: change
`grid 4 4` to `grid 4 5` and the perimeter finish appears or vanishes as a side
effect.

Decoupled, the four combinations are all writable and all mean something:
no frame with a raw cut, a frame over a raw cut, a frame on an uncut wall, and —
the case worth naming — a frame whose band is thick enough to swallow the
partial motif, which is what "absorb the cut" originally meant.

### What still has to be built

The band width needs a D3 default declaration, and it does not have a source.
Either it cites one or it is a calibration bet — and a bet is the likely honest answer,
because "thick enough that a cut motif reads as intentional" is a judgement
about how the wall looks in raking light, which is measured by printing it. W1's
2×2 pilot already reports `uncovered 4.8 cm²` and is the coupon that would carry
it.

---

## D-018 — F3 (supports required) stays a warning everywhere

**Date:** 2026-08-03 · **Status:** Decided · **Repos:** bikar (gate), 3d-models (doc)

### Context

[`print-validation-design.md`](print-validation-design.md) §8 Q3 asked whether
F3 should be a hard *error* for the presets shipped in the gallery, and recorded
a leaning: "yes-for-gallery, warn-for-Lab-custom."

### Decision

**Always warn.** The leaning is overruled.

Needing supports is a normal printable outcome, not a defect — a large fraction
of good models need them, and the printer handles it. Erroring on the gallery
path would fail `make orbs` over a condition the slicer is designed for.

The split severity also had a cost the leaning did not price: it makes F3's
meaning depend on who called the gate. The gate would need a `--strict` flag or
an equivalent caller-supplied policy, the severity table would stop being
readable on its own, and every future finding would face the same question. One
table, one meaning per finding code, is the cheaper invariant to keep true.

This does **not** mean a support-needing preset ships unnoticed. The warning is
emitted on the gallery path exactly as it is in the Lab; what changes is that a
human decides, rather than the build failing. F2 (an island that never merges)
remains an error — that is the genuinely unprintable case, and the distinction
between the two is now the whole of the difference.

### What this closes and what it does not

§8 Q3 is closed. §8 Q1 (slice representation) and Q2 (island-tracking
granularity) are untouched and stay open — both are V1-spike decisions, not
policy.
