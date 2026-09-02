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

### Built, 2026-08-03 — bikar `fc5adee` (PR #72)

Three forms, and the band is taken **out of** the declared boundary — the grid
lays out in the inset field, so `boundaryMm` stays what the author wrote and a
new `fieldMm` reports what the grid actually got:

| Form | Band |
|---|---|
| `frame` | the `CAL-FRM-01` default, **12 mm** |
| `frame band <mm>` | the width stated |
| `frame absorb` | solved: the narrowest band at or above the floor leaving the grid uncut on **both** axes |

**The bet is a coupon of its own, not W1's.** The paragraph above nominated W1's
2×2 pilot, and that was wrong for a reason worth keeping: W1 varies its art and
its tile count between prints, so it cannot hold the field fixed while only the
margin changes — which is the entire comparison the question needs. **W-P1**
(`bikar` `patterns/Coupons/Frame-Band-Coupon.bkr`) does: the 2×2 field is pinned
at 121.2 mm and the *boundary* grows through B06/B12/B20/B30. The ladder can fail
at both ends — B06 reading as deliberate means the shipped 12 gives up a tile's
worth of field for nothing; B30 still reading thin means the constant should
track module size rather than be a constant at all.

W3 renders the band as the ring between the boundary rect and the field rect and
ships **no printable frame geometry**, so W-P1 says so plainly and takes its
reading on four printed tiles laid on the field spacing over each rung's 1:1 SVG.
A coupon that claimed a printed band would be prescribing a part that does not
exist — the defect `catalog_models.py` exists to catch.

### The absorb arithmetic is not the one the sketch implied

"A band thick enough to swallow the partial motif" reads as a per-axis solve, and
a per-axis solve is wrong. **One band serves all four sides**, so both axes inset
by the same `2b` and their *difference never changes*: `absorb` is impossible
unless the boundary's sides already differ by a whole number of pitches. A solver
that fitted each axis separately would report success on an ordinary rectangle
and be wrong **invisibly** — the wall still renders, and the fragments are still
there. So it refuses, and names which of the two causes it hit (every exact band
under the floor, versus sides differing by a fraction of a pitch).

And the claim is *measured* rather than restated: the kernel solves the band, then
the evaluator counts the grid the layout kernel actually produced and throws if a
fragment survived. A solver that agrees with itself proves nothing. The hard FAIL
(486 × 400, sides differing by 1.06 pitches) is a test that must throw, per
[`../CLAUDE.md`](../CLAUDE.md)'s corollary — the by-design failure is the
load-bearing case.

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

---

## D-019 — a count in a doc is pinned to the tool that prints it

**Date:** 2026-08-03 · **Status:** Decided · **Repos:** 3d-models

### Context

`docs/backlog.md` §2 carries a count table: registered bets, `Calibrated<T>`
records, prototype-catalog entries, `.bkr` coupon files. On 2026-08-03 every
number in it was wrong. Bets read 14 against 17; records 16 against 17; catalog
entries 28 against 29; coupon files 5 against 8. The table had gone three merges
stale, and one of its rows — "4 without a record in bikar" — enumerated a set it
had not re-counted, which is a K2 in the file that documents K2.

The worse half is §8. That section exists to read the backlog against itself,
and its "Counts reconcile" bullet restated the same figures *independently*.
Fixing §2 alone would have left two counts in one document disagreeing, and the
bullet whose job was to catch that had itself been asserting the stale
arithmetic for three merges.

Every one of those numbers is already printed by something that runs:
`make validate-catalog` prints the entry count, and
`.claude/skills/calibrate/bets.md` — generated by bikar's
`registry:calibration`, with a do-not-edit header — carries the bet and record
counts in its first line. The registry file had gone stale too, for exactly the
same reason: nobody re-ran it.

### Decision

`.claude/gates/counts_gate.py` (hook `37-counts`, `make validate-counts`). A
number is tagged `<!--count:NAME-->` and the gate compares it to what its
authority prints. Two rules:

- **C1** — a tagged count equals its authority's value.
- **C2** — every known quantity is tagged somewhere, so deleting a marker is a
  finding rather than a silent loss of coverage.

The tag is an HTML comment, invisible when rendered, so pinning a number costs
the prose nothing.

**Marker-scoped, and the gap is printed.** The gate cannot know about a count
nobody tagged, and guessing at one by regex over prose would fire on sentences
it cannot parse — the same trade `docs_gate.py`'s D2/D3 make. What it does
instead is print the per-quantity site count on every run, so a figure asserted
in two places and tagged in one is visible in the output. That is the shape the
use-case validator already uses for anchored pointers.

**The authority is read, not recomputed.** The gate parses `bets.md`'s generated
header rather than re-deriving the counts from bikar's `CAL_BETS`. Two
independent derivations of one number is precisely how they come to disagree,
and this defect is what that looks like.

### Validator

**Validator:** the gate's self-test runs against fixed stub authorities, so it
cannot pass by tracking whatever the repo currently says, and it asserts that
each rule fires.

PASS: a document whose four tagged counts all match the stubs → 0 findings.

FAIL: `FIXTURE_ONE_OF_TWO_STALE` — a document whose §2-style table is **correct**
and whose §8-style bullet restates one of the same figures at its old value →
exactly 1 finding, on the second site. This is the by-design failure the gate
exists for, and it is the load-bearing one: a gate that checked only the first
occurrence of a quantity, or stopped at the first finding per quantity, would
report this document clean. Two further fixtures cover a deleted marker (C2) and
a tag naming a quantity no authority computes.

### What this closes and what it does not

It closes the class where a doc's tally and its authority drift apart unnoticed.
It does **not** check counts nobody tagged.

### Amendment, same day — the next ratchet, and what it caught

The two quantities this decision left hand-maintained were taken later the same
day, and the exercise justified itself immediately.

- **The record split.** "Machine-card bets settle 12 of the 17 records; design
  coupons settle 5" is a projection of the *same* generated `bets.md` — its bet
  table carries a Coupon column and a record list per row. The gate now parses
  the rows and classifies by `MC-` prefix, and **cross-checks the split against
  the header's total**: if the rows do not sum to the header's record count, the
  parse is wrong and the gate says so rather than reporting a split that does
  not add up. That check is what makes reading one file twice safe, where
  deriving from `CAL_BETS` separately would not be.
- **The coupon file list.** Not derivable as written — the doc's "8" is 6 files
  in `bikar/patterns/Coupons/` plus 2 coupon models that live among ordinary
  brick models in `patterns/Lego/`, and no listing separates those two from
  their neighbours. So the claim was **restructured rather than the gate bent to
  fit it**: the 6 is now the directory's own file count at `origin/main`
  (`coupon-dir-bkr`), and the 2 are enumerated. An enumerated set is not a count
  claim, and inventing a fuzzy authority to cover it would have produced a
  number the gate blessed without checking.

Reading bikar means reading it **at a published ref** — `origin/HEAD`,
`origin/main`, `origin/master`, never the working tree or `HEAD`. The sibling
checkout routinely sits on a detached HEAD belonging to another session (D-001),
and a gate whose verdict depends on someone else's checkout teaches you to
ignore it. When bikar is unreachable at all — a fresh clone, the `gh-pages`
worktree — the quantity is **skipped, and labelled `[skipped: bikar not
readable]` in the summary**, never folded into a clean run.

And the extension found the same defect again on its first pass, in exactly the
quantity that had been left untagged: §4 item 2 of `docs/backlog.md` read *"All
**four** coupon `.bkr` files exist in `bikar/patterns/Coupons/`"* while §2's row
six lines above said six. Two sites, one updated — the shape D-019 was written
for, sitting in the one place D-019 had declined to cover.

**Validator (amendment):** `FIXTURE_SKIPPED_AUTHORITY` — a document tagging
`coupon-dir-bkr` while that authority is absent from the resolved set.

PASS: 0 findings **and** `sites["coupon-dir-bkr"] == 1`. Both halves are
asserted: zero findings alone would also be satisfied by a gate that dropped the
marker on the floor, and the site count is what makes the unchecked claim
visible in the run's output.

FAIL: `same-doc-when-resolvable` — the *identical document* with the authority
present and disagreeing → 1 C1 finding. The pair is the point: the same bytes
pass when bikar is unreadable and fail when it is readable, which is what proves
the skip is a skip and not a hole.

### Second amendment, same day — C3, and the rule that had to be measured first

**The question, from the user:** *"do we need hooks to validate presence of
tags?"* C1 checks a tagged number against its authority and C2 checks that a
known quantity is tagged *somewhere*. Neither can see a number written in prose
with no tag — and **all three defects this gate has found were at untagged
sites**. So the answer was plainly "something must", and the real decision was
what shape it could take without becoming a prose parser.

That was settled by measurement, not by argument — the method
[`issue-register-evaluation.md`](issue-register-evaluation.md) used for the issue
register and the one that killed the link checker. Two candidate detectors, run
over all 62 documents of `docs/` and `.claude/`:

| Rule | Hits | Real | Precision |
|---|---|---|---|
| number within 60 chars of the quantity's vocabulary | 117 | ~5 | **~4%** |
| number *immediately* before a curated noun phrase | 9 | 9 | **100%** |

The loose rule's noise was not marginal and not tunable: section numbers next to
the word "records" (`§5.2 records`), "records" used as a **verb** ("the repo
records", "each entry records"), path fragments (`bikar:patterns/Coupons`), and
line-number lists. That is the detector CLAUDE.md already describes as one that
"cries wolf and gets switched off, which is worse than having no gate." It did
not ship. The tight rule did, as **C3**.

**Decision: C3 is a short list of exact phrases, and stays one.** Each phrase is
registered beside the quantity it names in `PHRASES`, and the cost of a new
phrase is measured across the corpus before it is added — not reasoned about.
Two narrowings in the first hour were each bought with a real false positive,
which is the standard: an open `\w+` filler slot plus a coupon id donating its
trailing digit turned `LG-P1 / LG-P2, whose\ncatalog entries` into a finding, so
the slot became the closed literal `of the` and a `(?<![\w-])` guard went in
front of the number. C3 consequently misses claims phrased a third way. That is
the trade, taken deliberately: **a narrow rule that is always right is the only
kind worth blocking a commit on.**

**What it found immediately**, all in `docs/backlog.md`, all having survived both
PRs that built this gate:

- the opening status paragraph quoting the registry as "12 registered bets · 16 records" — *under a claim that the registry agrees*; <!--count:quote-->
- §4's "Seven of the fourteen registered bets and twelve of the sixteen provisional records"; <!--count:quote-->
- §3.6's "Count: 28 catalog entries = 28 print-gated items", while §8's tagged copy already said 29 — two sites, one updated, a **third** time. <!--count:quote-->

Six wrong numbers, of which **two were spelled as words** ("fourteen", "sixteen") and
**one wrapped mid-phrase** across a line break. A digit-keyed rule scores zero on
the first pair; a line-at-a-time rule scores zero on the third.

**`<!--count:quote-->` opts a line out**, and exists for exactly one thing: prose
whose subject is a number that *was* wrong. This log narrating "the table said
four when it was six" must be allowed to say four. The marker suppresses the
**line**, not the claim — so a quotation must be written on one unwrapped line to
be excused, and a marker cannot silence the lines that follow it. It is a
quotation mark, not a silencer.

**And C3 opened a hole, which is why it is recorded here rather than only in a
test.** Tagging one of the three corrections put the number at the end of a line
and its tag at the start of the next. The tag parse was line-scoped: C1 never saw
the pair, C3 saw a tag and fell silent, and the site disappeared from the
per-quantity counts — the run printed `cal-bets-no-record=1 site(s)` for a file
asserting it twice. **A tag that quietly stops being read is worse than a missing
one, because a missing one is a C2 finding.** `marks_in` now reads across the
wrap exactly as C3 does. The per-quantity site count is the only reason this was
visible at all, which is the argument for printing it on every run.

**Validator (second amendment):** `FIXTURE_UNMARKED_WRAPPED` — the claim
"Seven of the fourteen registered\nbets and twelve of the sixteen provisional records", <!--count:quote-->
split mid-phrase by a line break, with no tag.

PASS: exactly 2 C3 findings — `cal-bets` and `cal-records`. A line-at-a-time
implementation returns 0 here and looks green, which is why this fixture and not
a single-line one is the by-design failure. `FIXTURE_MARKED_PROSE` is its
counterpart: the same two sentences, tagged, → 0 findings, proving C3 is
satisfiable by tagging rather than only by rephrasing. A rule you can only escape
is a rule that gets escaped.

FAIL: `FIXTURE_WRAPPED_MARKER` — a `99 <!--count:cal-records-->` split across the wrap, <!--count:quote-->
against an authority of 17 → 1 C1 finding **and** `sites["cal-records"] ==
1`. Before `marks_in` joined lines this fixture produced **zero** findings and a
site count of zero: silent, green, and wrong. `FIXTURE_QUOTED_PAST_ERROR` closes
the set — a line quoting "14 registered bets" under `<!--count:quote-->` → 0
findings, so the opt-out is proved to work rather than assumed to.

---

## D-020 — a number a tool can print is not typed, and the list beside it is checked too

**Date:** 2026-08-04 · **Status:** built · **Supersedes:** D-019's "deliberately
untagged" carve-out for the bet split

### Context

D-019 pinned counts to the tools that print them and its two amendments closed
the gaps that opening found. The question that started this one was whether the
repo could go further and *derive* numbers rather than verify typed ones — a
`--refresh`-style writer that rewrites every marked digit from its authority.

Two measurements decided it, in the order that mattered.

**Feasibility, first.** All 24 marked sites are `<digits> <!--count:NAME-->` and
so mechanically rewritable; two of them wrap, which a rewriter would have to
handle exactly as `marks_in` already does. Nothing there blocks a writer.

**Then the risk, which did.** **16 of the 24 marked sites sit in prose that
enumerates the very ids the number counts.** A writer that bumps the digit and
leaves the list alone converts a loud, commit-blocking disagreement into a
silent **K2** — exhaustiveness asserted over a set nobody re-searched. The
cheapest mechanism was the one that made the corpus worse, which is the
robustness-over-ease trade in its usual disguise: the digit is what you see, the
list is what you do not.

**And the audit found the defect it predicted, already live.** `docs/backlog.md`
§2's row *"Bets settled by design-specific coupons"* read 5. Derived from the
registry's own Coupon column: MC-1…MC-6 settle 7 bets, `CAL-STR-01` has none, so
design coupons settle 17 − 7 − 1 = 9. The 5 was the *record* count from the same
row's note — a number that means something else, borrowed because it was
adjacent. §8's list of the splits repeated it, summing to 13 against a tagged
17, while §8's own reconciliation bullet nine hundred lines away had 9 and was
right.

The reason it was wrong is the finding. §8 named the bet split as **deliberately
untagged**, reasoning that the registry already prints the record split and *"a
second derivation of the bet split from the same table is a number this repo
would then own twice."* That was the one quantity in the section nothing
checked, and it was wrong at two of its three sites — while every one of the 24
tagged sites was correct. **The exemption, not the tagging, was what rotted.**

### Decision

**The tenet: a number some tool can print is not typed.** Marked, derived once,
in one place. "We would own it twice" is not a reason to leave a number
unchecked — owning it twice is not the hazard, *deriving* it twice is, and one
derivation behind one marker is neither.

Three consequences, all built:

1. **The bet split is derived.** `authority_bets` now classifies each registry
   row by its Coupon cell into `cal-bets-mc`, `cal-bets-design` and
   `cal-bets-no-coupon`, from the same rows the record split already came from.
   The partition is checked to sum to the header's bet total and its no-record
   count to match the header's, because a projection that disagrees with the
   summary it came from is a broken parse, not a second opinion.
2. **C4: a list beside a marked count must not omit a member.** The three shape
   choices were each bought with a real would-be false positive:
   - **One-sided** — only a *missing* id is a finding. §8 legitimately names
     `CAL-STR-01` next to the design-bet list; set-equality fires on that
     correct sentence.
   - **Nearest marker wins**, scope ending at the next marker, the end of a
     table row, a blank line, or eight lines. §2's registered-bets row carries a
     17-marker, then a 6-marker, then six ids; attributing those to the first
     marker reads a correct row as eleven missing.
   - **Never demands a list.** A marker with no ids after it is not checked. C4
     completes an enumeration; it does not require one.
3. **No blind rewriter.** Not built, and the reason is recorded rather than left
   to be rediscovered: on 16 of 24 sites it would have produced exactly the
   document C4's by-design fixture is made of — a correct digit above a short
   list, green on every other rule.

**`<!--count:partial-->`** waives C4, and **not** C1, on the line it is written
on. §1 says "21 <!--count:cal-bets--> ids are registered (twelve at the original sweep, plus …)" and
then names the six additions; the twelve are covered by a number, not by name,
and rewriting that to list seventeen ids would make the sentence worse rather
than truer. The digit stays checked, because "this list is short on purpose"
says nothing about whether the count is right. Every waiver is counted and
printed in the run summary, at zero as well as above it — an escape hatch whose
size is only visible when it is in use is one that grows unnoticed.

### Validator

**Validator:** `FIXTURE_SHORT_ENUMERATION` — a three-bet miniature registry in
which **every count is correct** and the row for the two design bets names one
of them.

PASS: exactly 1 finding, `C4 count:cal-bets-design … omits CAL-STK-01`. C1, C2
and C3 all pass this document, which is the point: it is precisely what a
digit-rewriting fix-it would have produced from the real 2026-08-04 row, and
every rule that existed before C4 calls it clean.
`FIXTURE_FULL_ENUMERATION` is its counterpart — the same rows with the missing
id written in → 0 findings, so C4 is satisfiable by completing the list and not
only by deleting it.

FAIL: `FIXTURE_ENUMERATION_NEIGHBOURS` carries both shapes that would have made
C4 unshippable — a total-marker followed by a subset-marker followed by that
subset's ids, and an enumeration trailed by a neighbouring id that belongs to a
different quantity → **0 findings**. Under set-equality, or under
first-marker-wins, this correct document fails. `FIXTURE_PARTIAL_WAIVER` closes
the set: a waived line whose digit is *also* wrong → 1 C1 finding and 0 C4,
proving the waiver releases one rule and not the other. A waiver that suppressed
both would let a single marker retire a number from checking altogether, which
is the exemption this whole entry is about.

### What this closes and what it does not

Closed: the bet split is derived and checked at all six of its sites; §2's row
and §8's list are corrected; the enumeration next to a marked count is checked
for the five quantities whose members are `CAL-*` ids.

Not closed, and deliberately: C4 knows one kind of member. A count of catalog
entries or of `.bkr` files sits next to lists too, and those lists are not
checked, because the id vocabulary for them was not measured. Adding a quantity
to C4 costs a measurement, the same price C3's phrase list charges. The gate
prints its waiver count so the size of the gap is legible on every run.

---

## D-021 — text is emitted from outline-font contours, not from a single-stroke centreline

**Date:** 2026-08-04 · **Status:** Decided · **Repos:** 3d-models (docs), bikar (to build)

### Context

[`calibration-design.md`](calibration-design.md) §8 names the absence of text
emit as the machine card's biggest structural weakness: 23 coupons that cannot
say which rung they are. The first research pass
([`research/text-emit-survey.md`](research/text-emit-survey.md)) took a
single-stroke Hershey font as the input, measured that giving a centreline width
requires a polygon offset, measured that a naive offset breaks, and produced four
routes — every one of them a way to acquire an offset primitive this repo does
not have.

The assumption that the input is a centreline was never stated, and therefore
never checked. It was dislodged by a question — *is there a better way to print
letters; does anything support text natively?* — not by any gate.

### Decision

**Bake outline-font glyph contours into a build-time constant and extrude them.**
A TrueType/CFF glyph is already closed contours with counters as holes, so there
is no offset and therefore no union. The design is
[`text-emit-design.md`](text-emit-design.md); the measurement is
[`research/outline-font-emit.md`](research/outline-font-emit.md), over 8 faces
and 296 glyphs.

What the measurement settled, in the order it mattered:

1. **No union — per font, and checked.** Six of eight faces have zero crossing
   contours across the 37 glyphs a rung label needs. DM Sans has six such glyphs
   and draws `H` as three overlapping rectangles. "Outline fonts need no union"
   is a K2 claim and is false; "this font needs none, and the bake script checks"
   is true and is what ships.
2. **The payload is coordinates either way.** 13,710 baked bytes against a
   minified single-stroke face's 7,503 — under 2×, with no runtime font parser,
   which leaves bikar's 2026-05-07 zero-runtime-dependency position untouched.
3. **Route A is not "a union we have".** `unionShapes` in
   `packages/core/src/graph/polygon-union.ts` returns the outer perimeter only
   and throws on a disconnected result, so every glyph with a counter comes back
   filled in. This was read, not assumed, and it is why the route comparison
   moved rather than the doc's tone.
4. **`solidifyExtrudedPiece` cannot emit a glyph in any font.** Its holes are
   circles (`PieceHoleSpec` is `{name, x, y, bands}`). The reusable machinery is
   one level down — the earcut cap builder that already takes outer ring plus
   reversed hole rings.

### The tenet

**A local test cannot discharge a claim about every part, any more than an
aggregate can.** The survey's per-join bound named three failing glyphs; testing
the produced outline directly found thirty, in four break classes, three of them
non-local. The repo already had the aggregate half of this rule. The local half
is the same failure wearing a different hat: something cheap was measured and the
claim was written about something else.

Second, smaller, and recorded because it was nearly published as a fact: a
stem-width run reported DM Sans Bold `H` at a 0.01 mm stem — false, because the
distance transform was taken from the drawn segments rather than from the ink
mask, and those agree only when no contours overlap. Which is the exact condition
the *previous* check had just found DM Sans to violate. **A finding about the
input is also a finding about every tool that reads the input**, and nothing made
that connection until the number came out absurd.

### What this closes and what it does not

Closed: the route question, the payload question, and which face can legally
ship. `research/text-emit-survey.md` §4 and §5.3 carry marked corrections rather
than deletions, because how each went wrong is the reusable part.

Not closed: nothing has been printed and no slicer was run. Every number is
measured from font data, which is the geometry a slicer is handed and not what it
does with it. Whether the six DM Sans glyphs are repairable by a build-time union
is untested — the claim is that the condition is detectable, not that it is
repaired.

---

## D-022 — emboss vs engrave is registered as a bet, not decided

**Date:** 2026-08-04 · **Status:** Decided (to defer) · **Repos:** 3d-models (doc), bikar (bets, to register)

### Context

[`research/text-emit-survey.md`](research/text-emit-survey.md) §3.3 and §6 gather
three arguments about whether raised or recessed text prints more legibly at
small sizes, and they point two ways. Engraving is more forgiving of over-extrusion
and leaves a clean top surface; embossing survives a first layer that squashes and
does not fill with debris. No source settles it, and the numbers that would settle
it are all about a machine this project has not characterized — which is what the
machine card exists to fix.

### Decision

**Register it as a bet rather than adopt a default with a confident face.**
CAL-TXT-01 carries emboss-vs-engrave and CAL-TXT-02 the minimum legible cap
height; [`text-emit-design.md`](text-emit-design.md) §6 states engrave and
5.0 mm as *provisional* sides, with the reasoning that a recessed feature which
prints badly still leaves a readable part while a raised one leaves debris on the
surface that matters.

One coupon replaces both paragraphs with a measurement: the same label at a
descending ladder of cap heights, in both relief directions, printed once.

### The hole this left open — closed 2026-08-04 by D5

The docs gate's D3 rule accepted a `CAL-*` id as provenance for a default and did
**not** check that the id was registered, so §6's three defaults were gate-green
on two ids that resolved to nothing. Writing that admission into the doc is what
this repo's CLAUDE.md calls a defensible argument that management is occurring;
the gate is the fix.

T0 landed both halves. Both bets are now in bikar's `CAL_BETS` (coupon `MC-7`,
catalogued in the same change), and `docs_gate.py` grew **D5**: a CAL id that
*discharges* a `**Default:**` must appear in the generated registry, or the gate
fails.

D5 is scoped to the discharge form and not to every CAL id in the corpus, which
is a measured choice, not a cautious one. Across 225 CAL-id sites in `docs/`
there are 20 distinct ids, 17 registered. Gating every site fires 4 times on
`CAL-SEA-01` — an id [`hemisphere-split-design.md`](hemisphere-split-design.md)
Appendix B names precisely to record that it was **deliberately not minted**.
That is correct prose, and a rule that calls it a defect is a rule that gets
switched off. Restricted to the paragraph D3 actually reads, the same corpus
gives **5 hits, 5 real**, firing on exactly the two ids this decision was about.
Measure a rule before gating on it — the same tenet C3 was built from.

---

## D-023 — the printable `0` is the face's own slashed alternate, and the whole face is re-baked to get it

**Date:** 2026-08-05 · **Status:** Decided (user, via AskUserQuestion) · **Repos:** bikar-tile-border (bake + checks + face), 3d-models (docs)

### Context

Source Code Pro Bold was chosen as the shipping face in
[`text-emit-design.md`](text-emit-design.md) §6 on measurement — zero crossing
contours, a thin stem that clears the nozzle by ~1.9×. But its **default** `0` is
a *dotted* zero: shell, counter, and a dot inside the counter. At the 5 mm cap
CAL-TXT-02 bets on, the air between the dot and the counter wall measures
**0.289 mm** — well under one 0.4 mm bead, so the two fuse and the `0` prints as a
filled ring. The gap check (`bikar:packages/core/src/kernel3d/text-layout.ts`,
`labelMinGap`) caught it: every zero-bearing label on the machine card fails, and
the dotted zero would need a **6.95 mm** cap — 39% over the bet — to print at all.

### Options on the table

- **Ship the dotted zero at a bigger cap.** Rejected: 6.95 mm breaks CAL-TXT-02's
  5 mm and every label would have to grow with it. This verifies nothing about the
  glyph; it just hides it behind a scale the machine card cannot afford.
- **Mix a second face in for the `0` only.** Rejected: a rung label set in one face
  with one glyph borrowed from another is the kind of incoherence the reader pays
  for, and it forks the licence/version story per glyph.
- **Take the face's own `zero.a` slashed alternate** (Recommended, chosen).
  Source Code Pro's `zero` OpenType feature maps `zero → zero.a`. The slash joins
  the ring into one ink island, leaving two *sibling* lobes at depth 1 — the dot
  and its depth-2 nesting are gone. The catch: 1.017 (the file already on this
  machine, the one the survey measured) ships an **empty** `zero` feature, so the
  alternate is only reachable from **2.042**.

### Decision

Download Source Code Pro Bold **2.042** (SIL OFL, sha256 `b2095e0d…`, 206 804
bytes; user-approved download) and **re-bake the entire face** from it with
`0 → zero.a`, rather than splice one glyph. 2.042 shares 1.017's family, upem,
cap height and every advance width but differs in 37 of 39 outlines, so re-baking
the whole face keeps it internally consistent and forces every quoted number to be
re-measured against what actually ships (§6, and the research addendum dated today).

Two things ride on the same change, by design:

- **The counter check is not optional.** A slash makes the `0` one ink island, so
  `labelMinGap` returns `null` and would pass it **without measuring anything** —
  retiring the only check that caught the dotted zero in the very commit that
  adopts the fix. `checkLabelCounter` (largest inscribed circle in a counter) is
  what actually clears the slashed zero: two lobes 0.959 / 0.960 mm across against
  a 0.4 mm floor, 2.4× margin. Neither check subsumes the other, and
  `text-layout.test.ts` pins the row that proves it.
- **The dotted zero is kept as a committed fixture**
  (`packages/core/tests/kernel3d/fixtures/glyphs-dotted-zero.ts`), baked from the
  same 2.042 file. It was B2's
  only depth-2 witness and the only glyph that fails the gap floor; losing it
  silently is exactly the failure the repo's own rule names — a gate that asserts
  everything passes must be wrong about a deliberate failure or skip it.

The confusable-charset rule (`checkLabelCharset` / `checkLabelSetCharset`: no label,
and no plate, mixes `0` with `O`) ships in the same change — a slashed `0` is more
distinguishable from `O` than the dotted one was, but distinguishable is not a
licence to place both on one plate.

### What would reverse it

A printed CAL-TXT-02 coupon showing the slashed zero is itself confusable (with
`8`, or with `O` despite the slash) at the chosen cap, or failing to print for a
reason the counter check does not model. Either sends the choice back to a
different glyph or a different face — not back to the dotted default, which the
6.95 mm number rules out independently of how the slash prints.

## D-024 — a bet→coupon→catalog gate is evaluated and declined: no measured recurrence

**Date:** 2026-08-05 · **Status:** Declined (no gate) · **Repos:** none changed

### Context

A candidate gate — call it "D6" — would assert that every coupon id named in
bikar's `CAL_BETS`
([`calibration.ts`](../../bikar/packages/core/src/kernel3d/calibration.ts),
`settles: { by: 'coupon', coupon: '…' }`) has a matching `## <id>` heading in
[`catalog.md`](../.claude/skills/prototype/catalog.md). The trigger was a real
near-miss: on 2026-08-04 a bare `MC-7` bet was registered whose catalog entry did
not yet exist, and it was caught by hand, not by a gate.

### Decision

**Do not build the gate yet.** CLAUDE.md's Precedent rule — *measure a rule before
gating on it* — and the two evaluations it cites
([`dsl-extension-skill-evaluation.md`](dsl-extension-skill-evaluation.md),
[`issue-register-evaluation.md`](issue-register-evaluation.md)), which both
concluded *no skill, and only a gate where recurrence was measured*, set the bar:
a rule with no measured recurrence does not earn a gate.

The measurement clears the near-miss rather than confirming it. Coverage was
**13 of 13** on 2026-08-04 and **14 of 14** on 2026-08-05 — every coupon id in
`CAL_BETS` (`LG-B2 LG-F1 LG-P1 LG-P2 LG-S1 MC-1..MC-7 W-C1 W-P1`) has a catalog
heading, including the `MC-7` that prompted this. Zero historical violations. The
hand-catch worked; the register it protects is 14 rows a person can still read in
one screen.

### The tripwire

Re-evaluate when either holds: a **second** id ships in `CAL_BETS` without a
catalog heading (recurrence measured, not hypothesised), or the coupon-settled bet
count grows past the point where a person re-checking the whole list by eye is
reliable. If built then, the home is
[`catalog_models.py`](../.claude/gates/catalog_models.py) — which already parses
the catalog and already reads bikar — as one more claim class, **not** a new hook.

### What this is not

This is not a ruling that the mapping does not matter — it is a ruling that a
person is currently a better check for it than a gate would be, and that adding
the gate now would be the register-bloat the repo's own precedent warns against.

## D-025 — a confusable label blocks the build, at the same tier as the gap and counter checks

**Date:** 2026-08-05 · **Status:** Decided (user, via AskUserQuestion) · **Repos:** bikar-tile-border (CLI wiring + test), 3d-models (docs)

### Context

D-023 added two confusability checks to bikar's `text-layout.ts` —
`checkLabelCharset` (a single label mixing the slashed `0` and the capital `O`)
and `checkLabelSetCharset` (two labels on one part that fold to the same string
after mapping confusables) — each with a `PASS:`/`FAIL:` example. Both were
exported and unit-tested but **never called**: the mesh-gate label loop in
bikar's `packages/cli/src/index.ts` ran only `checkLabelGap` and
`checkLabelCounter`. So a `text` statement carrying `MC-2 PORT0`, or a plate
carrying both `O3` and `03`, compiled and wrote an STL. What the build should do
about such a label was left open — the same shape as
[`text-emit-design.md`](text-emit-design.md) §7 Q2's "what to do with a label
that fails §5," which observes that *automatically fixing* a label makes the
validator unfalsifiable by construction.

### Decision

**Block.** Confusability is the third §5 legibility check and fails under
`--check` at the **same tier** as gap and counter: the CLI prints
`label gate: …` with the offending pair and exits 1, and no STL is written. Not
a warning (a confusable plate would ship silently, which is the failure
labelling exists to prevent), and not a compile-time refuse (that would make
charset stricter than its two siblings for no reason). The block is enforced,
not remembered — it rides the same build target as the mesh gate, per D-014.

Three reasons the block earns its keep rather than crying wolf:

- **The pair set is deliberately tiny.** `CONFUSABLE_PAIRS` is just `['0','O']`;
  `1`/`l`/`I` are excluded because Source Code Pro draws them apart and no
  measurement here says that separation fails. A gate that fires on one
  well-measured pair has a false-positive surface near zero.
- **A confusable label defeats the point of labelling.** The whole reason T3
  engraved rung ids onto the coupons was so a person holding the part can name
  the rung. A label they cannot tell from another is worse than no label.
- **The fix is a rename, and the author is the one who should choose it.**
  Auto-substituting `O`→`0` would make the check unfalsifiable — the §7 Q2
  argument — so the gate names the collision and stops, leaving the rename to the
  person who knows which rung is which.

The two checks stay separate because neither catches the other's case: `O3` and
`03` each clear `checkLabelCharset` alone and confuse only side by side, so
`checkLabelSetCharset` runs once over the piece's whole label set. The gate test
(bikar `packages/cli/tests/label-gate.test.ts`, PR
[#78](https://github.com/NaqshCoffee/bikar/pull/78)) carries a by-design failing
witness for each — `MC-2 PORT0` and a plate with `O3`+`03` — beside the existing
`WWW`/`MC-2 R08` gap witnesses.

### The fix exposed the next defect: a ring cannot express a fold

Sharing `passRadialOffsetMm` was the correct fix and it did not finish the job.
With the corners correctly on the centreline, a crossing pass runs
`+A/2 → +A → +A/2`: it **folds**. The band was drawn as one closed six-point ring,
and a ring's inner rails cross under a fold. Measured over the 15 symmetry views of
the five woven orbs:

| construction | self-crossing shapes | worst, as a fraction of a mean band |
| --- | --- | --- |
| before D-043 | 0 / 3,743 | — |
| D-043, one ring per pass | **96 / 3,743** | 1.26× |
| D-043, one quad per spine segment | **19 / 5,264** | 0.29× |

The pre-fix zero is not a clean bill of health; flattening every corner onto one
shell is precisely what had been hiding the fold. So each pass is drawn as one quad
per spine segment. For the two-point sub-spines a trimmed crossing produces this is
byte-identically the old outline, which is why the `gt-emitter` contract is
untouched.

Two alternatives were built and measured before this one was kept:

| construction | residual self-crossings | why not |
| --- | --- | --- |
| per-point sides, no mitre | 23 | strictly worse than the mitre |
| frame read from `sweepStrand` itself (r̂ × t̂, edge frames averaged) | **17** — the best count | took the parity-vs-depth by-design failure from 3 cells **back to 0** |

The second is the strongest possible reading of the tenet this entry executes: it
makes the picture's rails *be* the swept solid's rails, and it deletes `sideVector`,
`mitredSides` and `RIBBON_MITER_LIMIT` outright. It also re-silenced, at the shipped
amplitude, the exact boundary the section above had just moved into the light. **A
gate that stops firing is not a cheaper fix, it is a worse one** — the corollary in
`CLAUDE.md` that the by-design failure is the load-bearing case, deciding against the
option that scored best on every other number. Recorded here so the next reader does
not re-derive it and reach the opposite conclusion from the bow-tie count alone.

### The cascade did not come back clean, which is why it ran first

Order, per the stability test's own docstring: regenerate views → qiyas sweep →
re-pin composites → **hashes last**.

| preset | before | after |
| --- | --- | --- |
| `maclado-9-overlap` ribbons | 1.000, drop 0, drift 0.0003 | **0.999, drop 7, drift 0.0078** |
| `maclado-9-weave` ribbons | 1.000, drop 0, drift 0.0003 | **0.999, drop 3, drift 0.0145** |
| `rosette-weave`, `weave-dodeca`, `weave-icosa` ribbons | 1.000, drop 0 | unmoved |
| all 14 presets, cells | unchanged | unchanged |

The three unmoved woven orbs are exactly the three with no residual self-crossings.
That correspondence is what ties these numbers to their cause rather than to the
split in general, and it is the reason the drops are recorded rather than absorbed.

**The picture is right; what is lost is the trace.** qiyas partners one simple
polygon per shape and a self-crossing outline has no simple partner. The renderer
emits no `fill-rule`, so SVG's default `nonzero` paints both lobes of a twisted
ruled quad — which is the projected image of that quad. That absence is now asserted
in the test suite, so writing `fill-rule` later becomes a visible decision instead of
a silent one.

Drift is recorded as a **named per-entry exception, not a raised ceiling**. 52 of the
54 views still measure 0.0001–0.0003, and a ceiling moved to cover two of them stops
saying anything about the other 52 — the same argument the drop table already makes
about a blanket `toBe(0)`. Both values stay inside qiyas's own acceptance radius
(`max_dist` = 0.02·√2 = 0.028284; 0.0145 is 0.51 of it), so this is headroom being
spent, not a threshold being crossed. A tripwire fires if an exception ever outlives
its cause.

### The stamp that names the bikar was not wired to the renders

Found while running this cascade. `DEPLOY_PATHS` ships `build/bikar-ref.txt` beside
`build/stls` and `build/images`, so a reader takes it as *the bikar that produced
these* — but `orbs` was the one bikar-consuming target that did not depend on
`bikar-stamp` (`bricks`, `coupons` and `pattern-sets` all did). `make orbs` against
the freshly merged bikar left the stamp on the **pre-merge sha** while every render
under it came from the merge. One added prerequisite; the same shape of defect as the
one this entry is about, two artifacts answering the same question and disagreeing.

### What this resolves and what it does not

It resolves the **confusability** arm of §7 Q2. It does **not** decide the
gap/tracking arm — whether a too-tight label (`MC-4 R12` needs +0.219 mm, `WWW`
+0.369 mm) is opened by tracking, a larger cap, the monospace face, or refusal.
That failure is a continuous measurand with a fix that changes the geometry, and
it stays open and failing-loudly-with-the-number until a coupon settles it.

---

## D-026 — a `place` takes a colour by grounded name **or** by bare LDraw code

**Date:** 2026-08-06 · **Status:** Decided (user, via AskUserQuestion) · **Repos:** bikar-tile-border (DSL + emitter + tests), 3d-models (docs)

### Context

An assembly's parts all emitted as one LDraw colour, so `Brick-Stack.mpd` — a
two-brick stack — read as a single grey blob in every viewer, defeating the whole
point of exporting the parts as distinct sub-files (task #104; the symptom that
started it was a user seeing "just black" in `library.ldraw.org/model-viewer`).
Colour rides the type-1 placement line (`1 <colour> …`), not the part definition,
so making it real meant giving `place` a way to say which colour. Two sub-questions:
what does the author write, and is the name→code mapping grounded? The mapping had
been left **UNGROUNDED — not fetched** in
[`research/lego-ldraw-export.md`](research/lego-ldraw-export.md) §8 item 5.

### Decision

**Both — `place <Piece> [color <name|code>]` accepts a grounded colour name or a
bare integer LDraw code**, chosen by the user over name-only and code-only via
AskUserQuestion. A name (`red`) is the lower-cased LDConfig colour name; a code
(`4`) is any integer in LDraw's 0–511 range. The clause reuses the DSL's existing
`color` keyword — no new token — and an uncoloured `place` keeps the emitter
default (7, `Light_Grey`), so an all-grey assembly emits **byte-identically** to
before the feature. It is `--format ldraw` only; STL/SVG ignore it.

Three reasons the both-forms answer earns its keep:

- **A name asserts a grounded fact; a code asserts nothing.** Names are validated
  against the fetched palette (§7.4, S15 — `LDConfig.ldr` header `UPDATE
  2026-05-29`, fetched 2026-08-06) and an unknown name is refused with the valid
  list. That is the K4/grounding discipline: a name means exactly what LDConfig
  says. A bare integer is the escape hatch for any of the other ~370 codes, and
  like the old draft's `4`/`7` it asserts nothing about appearance — which is
  honest, not a gap.
- **Resolution is deferred to eval, not the parser**, so a bad colour fails
  **every** output format, not only the one that consumes it — surfacing the error
  where the author is, per "surface, don't hide."
- **The grounding was a prerequisite, not a follow-up.** Shipping name support
  while §7.4 still said "not fetched" would have left the emitter's doc comment
  pointing at an ungrounded claim — a K9/pointer hazard. So the palette was fetched
  and §7.4 written in the same change (feature
  [NaqshCoffee/bikar#79](https://github.com/NaqshCoffee/bikar/pull/79)).

### What this resolves and what it does not

It resolves how per-part colour is authored and grounds the ten-name palette the
clause exposes. It does **not** transcribe LDraw's full ~380-entry palette — only
the ten names the clause names are grounded; any other colour is reached by its
integer code, which stays a deliberate no-appearance-claim escape hatch. It also
does not touch the STL/SVG paths, which have no colour channel to carry.

## D-027 — a brick's studs take their own colour, fixed in the geometry, not on the reference

**Date:** 2026-08-06 · **Status:** Decided (user, via AskUserQuestion) · **Repos:** bikar-tile-border (DSL + emitter + read-back palette + tests), 3d-models (docs)

### Context

D-026 gives a placement one colour, carried on the type-1 line. A two-tone brick —
blue body, yellow studs, which is what a LEGO brick actually looks like — cannot be
said that way: the type-1 line has exactly **one** inherit slot (colour 16), so
everything in the shared block renders the one placement colour. The user, looking
at `Brick-Stack.mpd` in a viewer and seeing solid-colour bricks, asked whether the
pins could be coloured separately (task #105). The question underneath: where does a
second colour live, when the reference line has room for only one?

### Decision

**`place <Piece> [color <name|code>] [studs <name|code>]`** — an optional second
clause colours the studs independently of the body (chosen "per-brick stud colour"
over a body-only palette via AskUserQuestion, for full two-tone control). `studs`
resolves through the same grounded palette and 0–511 range check as `color` (D-026)
and is independent of it; either clause may appear alone, `color` first when both
are present. `studs` is a **contextual** word in the parser, not a reserved keyword —
safe because no assembly statement begins with it.

The mechanism is forced by the single inherit slot, and it is the decision:

- **The stud colour is baked into the triangle text, not the type-1 line.** The body
  triangles stay colour 16 and inherit the placement colour; the stud triangles carry
  the explicit stud code. One watertight block, two colour regions — the *mixed-colour
  inline part*. This was **spiked before implementation** (the load-bearing risk was
  whether a real LDraw loader renders a mixed-16/explicit block correctly): the spike
  placed one such part twice and read back a blue body and a red body sharing one
  yellow-studded part, through three.js `LDrawLoader`.
- **"Stud" is the top-face plane, exact not heuristic (K10).** A triangle is a stud iff
  a vertex stands above the body height `H`; `stackBrickSlabs` puts studs in the one
  slab above `H` and nothing else there, so the body's top face at exactly `H` never
  trips it. The transfer condition is written in the emitter and the design doc §14.6:
  it holds only for meshes whose sole geometry above the top face is studs. The emitter
  **refuses** a stud colour on an empty stud set (a `studs none` brick, a non-brick)
  rather than colour nothing.
- **De-dup splits exactly on stud-colour difference.** The block key is the geometry
  text and the stud code now lives in it, so two bricks with different stud colours
  mint two blocks and two with the same one still share a block — a consequence that
  falls out of the existing key, not a special case.
- **Robustness over ease — the read-back panel learned the palette.** §14.4 preloaded
  only code 7, so a coloured stud would have rendered as the magenta the panel's trap
  exists to surface (the same latent gap D-026's coloured bodies had). The read-back
  now preloads the full ten-colour grounded set with LDConfig's own RGB (§7,
  `UPDATE 2026-05-29`), and a test asserts a yellow-studded brick reads back at zero
  unresolved colours with unchanged winding/edge coherence.

### What this resolves and what it does not

It resolves how the pins are coloured apart from the body and closes the panel's
magenta gap for the whole grounded palette. It does **not** add per-*region* colour
beyond body-vs-studs (relief faces, walls and bed all stay body colour), and it does
not widen the grounded palette past D-026's ten names — an arbitrary stud code is the
same no-appearance-claim escape hatch, now reported as magenta in the panel rather
than resolved, because the panel has no LDConfig to look it up in.

## D-028 — a `.mpd`→PNG CLI renders a *set* of angles, gated by hard counts and soft goldens

**Date:** 2026-08-07 · **Status:** Decided (user, via AskUserQuestion) · **Repos:** bikar (CLI + gate + witness + lab scene, PR [#82](https://github.com/NaqshCoffee/bikar/pull/82) → `1113052`), 3d-models (design doc §15, this entry, use-case map)

### Context

§14.3 emits an LDraw `.mpd` and §14.4 reads it back inside the studio, but nothing
in any of the three repos turned a model into a picture headlessly. The user asked
directly — *"do we have a CLI to go from mod to png?"* — and wanted it to produce
*different screenshots* of a model plus a validation path, all tracked as tasks
(#106–#109). The research behind the render experiment had already found the
constraint that shapes the answer: [`ldraw-cli-viewers.md`](research/ldraw-cli-viewers.md)
§10.5 showed a three-quarter render of `Brick-Stack` is pixel-for-pixel a single
six-plate block — **on a file with no edge lines a render is evidence of shape, not
of structure** — so a one-shot screenshotter would be a tool that can lie about how
many parts it shows.

### Decision

Three sub-decisions, each settled with the user via AskUserQuestion:

- **Render backend — Playwright + full Chromium** (`channel: 'chromium'`), not the
  default headless shell. Forced by §10.3, which measured the shell failing to create
  a WebGL context on this machine class while full Chromium reaches the GPU through
  ANGLE/Metal. The CLI drives the *same* Lab scene the studio panel shows
  (`bikar:packages/lab/src/ldraw-scene.ts` on `bikar:packages/lab/thumbnail.html`), so
  a thumbnail is the same brick §14.4 reads back, not a second renderer that could
  disagree.
- **Validation basis — counts *and* golden pixels, unequal by design.** Not one or the
  other. **Counts are the hard gate**: the camera-independent read-back is deep-compared
  whole against `<name>.expected.json` and fails on any drift (`countsMatch`,
  `bikar:scripts/thumbnail-gate.ts`). **Golden pixels are the soft gate**: a render is
  GPU-dependent, so the differing-pixel fraction is compared against a small `--tolerance`
  (default 0.02), not zero — and a size mismatch is a hard `null` fail, not a swallowable
  ratio. This is the direct enforcement of §10.5: the composition facts a picture cannot
  establish are exactly what the counts pin, exactly.
- **A skill now, a gate later.** The path has a GPU in it, so a per-commit render gate
  would be slow and backend-fragile. The near-term home is a `validate-render` skill
  that runs the CLI on demand; graduating it to a hook waits until the defect it would
  catch shows measured recurrence — the *no skill/gate before the recurrence is measured*
  discipline of [`issue-register-evaluation.md`](issue-register-evaluation.md) and
  [`dsl-extension-skill-evaluation.md`](dsl-extension-skill-evaluation.md).

The gate logic is split out of the CLI into `bikar:scripts/thumbnail-gate.ts` so a
`node --test` witness (`bikar:scripts/thumbnail-gate.test.mjs`) can freeze the one
property that matters about a gate — that it **fires** — with cases built so a lazy
aggregate (count fields, average the pixels, ignore image size) passes while the real
gate fails: a single drifted field, a CCW→CW winding flip, a changed part hash, a
one-side-only field, a half-flipped frame, a size mismatch.

### The transfer condition, stated so it cannot be assumed (K10)

**The committed golden PNGs are valid only for the backend that produced them** — this
machine's Chromium-on-darwin through ANGLE/Metal (§10.6: "the renders used this
machine's GPU … nothing here was run headless over SSH, in a container, or in CI"). A
different GPU, driver, or OS may shift enough pixels to exceed the tolerance with nothing
wrong; the response is `--update-goldens` on that backend, not a loosened tolerance. The
**counts carry no such condition** — the read-back is pure geometry with no GPU in the
path — which is why the hard gate is the count gate and only the soft gate is the picture:
only one of the two ports.

### What this resolves and what it does not

It gives the repos a `.mpd`→PNG path that renders several disambiguating angles and can
hold them to a committed expectation. It does **not** yet ship the `validate-render`
skill (#108) or any pre-commit render gate (deferred by the third sub-decision), and it
does not widen coverage past one exercised model — the goldens exist for `Brick-Stack`
alone, and §10.6's "one of twelve viewers" caveat still stands for everything else.

## D-029 — a third `--check` strength (the colour set) plus a GPU-free catalog gate, split at the GPU

**Date:** 2026-08-08 · **Status:** Decided (user, via AskUserQuestion) · **Repos:** bikar (colour gate + `visibleColours` in `bikar:scripts/thumbnail-gate.ts`, the multi-material read-back fix in `bikar:packages/lab/src/ldraw-readback.ts`, PR [#83](https://github.com/NaqshCoffee/bikar/pull/83) → `6dba045`; per-model notes + catalog well-formedness test + hook, PR [#84](https://github.com/NaqshCoffee/bikar/pull/84) → `e8b07d5`), 3d-models (design doc §16, this entry, `validate-render` skill, use-case map)

### Context

D-028's `--check` has two strengths — hard counts, soft golden pixels — and D-026/D-027
gave each placement and stud its own colour precisely so an assembly reads as distinct
parts, not one grey mass. But nothing gated the parts *staying* distinct. The counts are
pure geometry and do not move when the colours collapse; the goldens do not port across
backends (D-028's K10), so on any machine whose goldens were never baked the pixel gate is
silent too. A model can regress to an all-grey blob and pass both. The user asked whether we
needed "a verification catalog of the visual aspects/checklist we expect to see in png per
model … with all the appropriate hooks."

### Decision

Two sub-decisions, each settled with the user via AskUserQuestion.

- **Checklist = a colour-presence gate plus per-model notes.** A third `--check` strength
  classifies every foreground pixel to the nearest colour in **the model's own palette plus
  the background** (not exact pixels, not the whole LDConfig set), accumulates each colour's
  best coverage across the angle set, and compares the colours clearing a small area floor
  (`--colour-min-area`, default 0.01) against a committed `visibleColours`. Nearest-of-palette
  is what makes it **port across backends** where the goldens cannot — a shaded blue is still
  blue — so it catches the grey blob on a machine the goldens were never baked for. The
  expectation is deliberately the **visible** set, a subset of the resolved colours: a colour
  can be wholly occluded in every angle (Brick-Stack's lower-brick yellow studs under the top
  brick) with nothing wrong, so `visibleColours` is *baked* from a trusted backend by
  `--update-goldens`, never derived from the read-back — the same discipline as the golden
  PNGs. Landing it exposed and fixed a latent read-back bug: three's `LDrawLoader` gives a
  multi-colour brick a material **array**, and the old single-material read reported an empty
  palette for every multi-colour model. Beside each fixture, a `<name>.notes.md` names every
  resolved colour (occluded ones marked), explains the `visibleColours` subset, and says what
  each baked angle is for — the human half of the checklist.
- **Hook boundary = catalog well-formedness only.** The render keeps a GPU in the path, so it
  stays skill-invoked (D-028, §15.4) and the colour gate rides along in the on-demand `--check`.
  What graduates to a pre-commit hook is the **catalog** — the fixtures and the metadata beside
  them — which needs no pixels: `bikar:scripts/thumbnail-catalog.test.mjs` checks that every
  `.mpd` is paired with an `expected.json` and a `.notes.md` (none orphaned), that every resolved
  colour is named in that model's notes (so the palette cannot grow without the notes — the W-F1
  coherence, ported), and that the catalog is non-empty. CI runs it wholesale (`test:scripts`);
  `bikar:.husky/pre-commit` runs it on staged fixture changes, deletions included so a stranded
  `expected.json` is caught as the orphan it is.

### The line, stated so the next model inherits the right half (K10)

The split is the GPU. **Counts** (deterministic geometry) and the **colour set**
(nearest-of-palette, shading-robust) both port across backends and so mean the same thing
everywhere — both live in `--check`. **Golden pixels** do not port and stay soft and tolerant.
The **catalog** has no pixels at all and so is the only one that becomes a hook. Not "the render
is a skill, full stop," but "the part with a GPU in it is a skill; the part without one is a gate."

### What this resolves and what it does not

It closes the grey-blob gap that counts and un-baked goldens both miss, and it binds the per-model
notes to the palette so the human checklist cannot silently drift. It does **not** turn the render
itself into a gate (still deferred, and still awaiting the measured recurrence D-028 requires), and
it does not widen coverage past `Brick-Stack` — the catalog holds one model, and adding a second is
the point at which the gate stops being about one fixture and starts being about the set.

## D-030 — the greedy chain is a documented partial: its gap cannot hold a small filler vocabulary

**Date:** 2026-08-08 · **Status:** Decided (measured; the §8 gate prescribed the outcome) · **Repos:** bikar (gap decomposition + clustering + witness tests, PR [#91](https://github.com/NaqshCoffee/bikar/pull/91)), 3d-models (design doc §8/§9, this entry, use-case map)

### Context

M4b is the maclado design doc's asymmetric faithful field, and its §8 gate was written
before any placement rule existed: *"if no placement rule the survey permits yields whole
fillers with a closable ribbon, the honest outcome is a documented partial in the decisions
log, not a distorted-filler orb that fails its own §5.3 validator."* Step 1 shipped the
greedy tightest-turn chain (`placeSpiralChain`, PR #90) and narrowed §9.1's convergence risk
to one question: does the inter-winding gap — ≈68% of the sphere at the M4 angle — decompose
into a small congruence-class set of whole fillers?

### Decision

Measured, and the answer is **no** — for this placement rule. Step 2
(`bikar:packages/core/src/kernel3d/maclado-gap.ts`) cut the gap by a documented rule (§6:
spherical Delaunay of the wheel centres, bridges between mutually nearest rim vertices, one
tile per hull triangle), verified the cut hard (hull count 2·W−4 = 34 exactly; partition
residual ~1e-9 mm² of 30,772.81 mm²; every rim vertex covered), and clustered the tiles by
the §5.3 congruence the validator already trusts:

- **34 tiles → 33 congruence classes** at maker tolerance (1e-3 mm / 1e-4 rad).
- The §9.2 tolerance sweep is what makes the verdict a verdict and not a knob artifact:
  still 33 classes at 1 mm / 0.1 rad — **three decades looser** — and the count only
  collapses (to 6) at a tolerance so absurd it equals the ring-size bucket count, the
  no-information end of the knob.
- **The cause is the field, not the cut.** The 51 hull edges take **32 distinct centre
  distances** (43.78 mm — the join distance — up to 76.48 mm): the greedy walk produces a
  *continuum* of wheel separations, so no cutting rule, this one or any other, could extract
  a small vocabulary from it. The negative result attaches to `placeSpiralChain`, and any
  future placement rule that hopes to converge must be built to **quantize its separations**
  — that is the transfer condition (K10) a successor rule inherits.
- The aggregate discipline held: an area-compensated distortion (grow one tile 15%,
  bisect-shrink another) keeps Σ areas exact to sub-µm² while per-tile congruence fails —
  pinned as a by-design failure in `bikar:packages/core/tests/kernel3d/maclado-gap.test.ts`.

### What this resolves and what it does not

It closes §9.1 and §9.2 **for the greedy chain**: the rule is honest machinery — exact
joins, free θ, measured gap — but it is a *chain generator*, not a *maclado generator*, and
the partial is documented here rather than shipped as a distorted-filler orb. It does **not**
close M4b's question for every permissible rule: the survey space still contains placement
rules with quantized separations (discrete step words, lattice-guided walks), and whether one
is worth building is a scope decision for the user, recorded in §8's M4b bullet as the open
follow-on. The symmetric M4 field is untouched — it remains the shipped, fully validated orb.

## D-031 — run the quantized-separation spike; the lattice walk collapses the vocabulary to 4 classes

**Date:** 2026-08-08 (user decision) / 2026-08-11 (measured) · **Status:** Decided (Option A chosen by the user; spike built and measured) · **Repos:** bikar (lattice walk + generalized polygonal gap cut + witness tests, PR [#92](https://github.com/NaqshCoffee/bikar/pull/92)), 3d-models (design doc §8 M4c, this entry, use-case map)

### Context

D-030 left one open follow-on, explicitly the user's scope decision: whether a
quantized-separation placement rule is worth building at all. A decision memo laid out
three options — **A**, run a bounded spike that builds candidate quantized placement rules
and measures them with D-030's own rule-agnostic instruments before committing to any
solidify/mesh machinery; **B**, stop at the documented partial; **C** (named as not a real
option), build a full successor rule straight to an orb. The memo carried D-030's trap
forward as the load-bearing hazard: a finite *turn-angle* menu does not quantize
non-adjacent separations, because 3D rotations do not commute — the greedy chain itself is
the measured proof, since its steps already came from a finite alphabet and its separations
still formed a 32-value continuum. Only a finite placement *site* set quantizes trivially.
The user chose **A**.

### Decision

Spike run, and quantization delivers. The candidate rule reuses the M4 field's 20
dodecahedral vertex sites as the finite point set
(`bikar:packages/core/src/kernel3d/maclado-lattice.ts`): a lowest-index-first DFS walk
along the field's adjacency, every consecutive pair joined exactly by the §2 divisor trick
(no search, no near-misses), every pairwise separation drawn by construction from the
solid's 5-value distance table. Measured with the same instrument, radius, and default
tolerance that produced D-030's 33-class verdict:

- **18-wheel walk: 13 tiles → 4 congruence classes** on 2 distinct hull-edge separations.
- 13-wheel walk: 12 tiles → 6 classes on 4 separations.
- Full 20-site field: 12 tiles → 1 class on 1 separation (the symmetric limit, for scale).
- Greedy chain, unchanged control: 34 tiles → 33 classes on 32 separations.

The walks are asymmetric partial fields — no global group — so the collapse is
quantization's doing, not symmetry's. Getting the measurement at all required a real
instrument fix: every supporting plane of a dodecahedral vertex subset is a face plane of
the solid (up to 5 coplanar sites), so the M4b triangle-only hull cut mis-counts C(k,3)
triangles per polygonal face. The cut now groups coplanar supporting triples into one hull
*face* (deduplicated by member set, because plane-key rounding splits one face into several
under float dust) and takes one tile per face; for centres in general position every face
is a triangle, and the M4b tests pin that the chain's 34/33 verdict is byte-for-byte
unchanged. Cross-checks: Euler W − E + F = 2 on every measured hull; the full-field tiles
reproduce the 12 filler rings `buildMacladoField` constructs by an independent route; and
the by-design failure is load-bearing — a clustered 9-site walk *fails* the partition
residual (>1e3 mm², vs ~1e-10 for the valid walks), so the instrument rejects
configurations it cannot faithfully cut instead of measuring them wrong
(`bikar:packages/core/tests/kernel3d/maclado-lattice.test.ts`).

### What this resolves and what it does not

It closes D-030's open follow-on with evidence in the direction the K10 transfer condition
predicted: a rule that quantizes separations by construction gets a small filler vocabulary
without full symmetry. It does **not** ship an orb: the walk is a spike instrument — no
solidify, seam-graph, or weave machinery consumes lattice walks, and the 18-wheel walk's
4-class vocabulary still trades against the full field's 1-class one. Whether a partial
lattice orb is worth *shipping* is a new scope decision, now an informed one; until then
the shipped maclado remains the symmetric M4/M5 field.

## D-032 — the overlap branch measured: tangency touches, overlap weaves, both need phase

**Date:** 2026-08-11 (user decision and measurement, same day) · **Status:** Decided (spike built and measured; welding into a mesh deliberately not attempted) · **Repos:** bikar (overlap instrument + validator + witness tests, PR [#93](https://github.com/NaqshCoffee/bikar/pull/93)), 3d-models (design doc §8 M4d + the M2 narrowing note, this entry, use-case map)

### Context

On 2026-08-11 the maker, Ángel María Martín López, posted a new photo of the 9-spike
maclado ribbon sphere, and the user's verdict on our shipped orb was direct: *"our orb
looks nothing like this."* The diagnosis held up: design §5.2 specifies the maclado move as
wheels that **overlap at the rim** — "a shared rim arc is welded so a ribbon entering one
wheel continues into its neighbour" — but M2 implemented the *tangent narrowing* of that
spec: centre separation exactly 2θ, a single tip-to-tip contact point. §8 then marked M2
"overlapped and welded ✅ Done", and every later milestone (M3 fillers, M4 field, M4b
chain, M4c lattice) built inside the tangent branch without reopening the reading. That is
a K1-shaped narrowing of our own spec — the qualifier "overlapping rim **arcs**" quietly
became "touching rim **points**" — and it is why the shipped orb reads as separated stars
with large fillers while the reference reads as interpenetrating stars with no designed
fillers at all. The user chose (AskUserQuestion, 2026-08-11) a bounded overlap spike before
any orb commitment, M4c discipline: instrument first, measure, record.

### Decision

Spike run (`bikar:packages/core/src/kernel3d/maclado-overlap.ts`). The instrument finds
transversal great-arc crossings between two placed wheels' 18-segment rim outlines —
transversality angle and rim-vertex clearance per crossing — and `checkOverlapWeld` is
§5.2's validator in the overlap sense: PASS requires an even count (≥2) of transversal
crossings, none through a rim vertex, and weld nodes at least a strut width apart. The
by-design FAIL is M2's own canonical joined pose: `checkWheelJoin` accepts it (the contact
is real) while the overlap validator counts exactly **one** degenerate vertex contact —
odd parity, which two closed curves in general position cannot have. Contact is an
aggregate; a weave needs transversal crossings, and the tangent branch has none.

Measured at R=60 with 2 mm struts, pinned by 10 tests
(`bikar:packages/core/tests/kernel3d/maclado-overlap.test.ts`):

- **Three pair regimes.** Tangent (separation 2θ): one vertex contact, not a weave.
  Tip-aligned overlap: exactly **2 transversal crossings ≈38°** where the facing spikes'
  flank edges pass through each other — the X of the reference photos. Gear mesh (spin
  more than ~±8° off tip alignment at 85% separation): the spikes interleave into the
  neighbour's valley notches with **zero** contact, down to ~80% of the join separation.
  Overlap therefore *inherits* the tangent branch's phase discipline rather than escaping
  it — the spin window is narrow either way.
- **A field-scale window exists and is comfortable.** Growing the M4 field's caps by
  ratio ρ (site lattice unchanged, so every placement survives): ρ ≈ **1.15–1.25** puts
  all 30 adjacent pairs in the clean 2-crossing regime — 60 degree-4 weld nodes (exactly
  what §5.4's parity solver accepts), inter-pair node clearance >35 mm so no degree-6
  triple points arise, and second-neighbour rims never touch anywhere in the swept range.
  Below the window the two nodes of a tip-cross fuse (0.76 mm apart at ρ=1.05, under the
  2 mm strut width); by ρ=1.30 the regime changes (10 crossings per pair, clearances
  collapse to 0.39 mm). At ρ=1.25 the cap-area sum passes 100% of the sphere — the dense
  look of the reference — while the weave is still one X per dodecahedral edge.

### What this resolves and what it does not

It settles that the overlap branch is *geometrically cheap where it was feared expensive*:
no search (the M4 sites and spins carry over unchanged), no triple points, a wide ρ
window, and a validator that cleanly rejects both the tangent touch and the gear mesh. It
does **not** ship a woven orb: the crossings are mid-surface rim nodes, and welding them
into a printable ribbon needs either the Family-1 radial over/under sweep or a geometric
boolean — and §5.5's manifold gate is combinatorial, so it cannot see whether two
interpenetrating shells were actually welded (the woven family exploits exactly that).
Building the welded crossing mesh is the next milestone-sized decision, now an informed
one; its input numbers are the window above. The dense multi-ring look of the reference
(second-neighbour crossings, incidental faces) starts past ρ=1.30 and is measured only as
"regime change" here — going there is a separate, larger step this spike deliberately did
not take.

## D-033 — build the welded woven-overlap orb: the D-032 window holds, parity solves, 60 loops ship

**Date:** 2026-08-15 (user decision; built same day) · **Status:** Decided (built, merged in bikar) · **Repos:** bikar (kernel module + DSL statement + preset + tests, PR [#94](https://github.com/NaqshCoffee/bikar/pull/94)), 3d-models (design doc §8 M4e, this entry, gallery entry, use-case map)

### Context

D-032 ended on a deliberate stop: the overlap instrument had measured the field-scale
window (ρ ≈ 1.15–1.25 puts all 30 adjacent pairs in the clean 2-crossing weave, 60
degree-4 weld nodes, no triple points) but no welded mesh existed, and building one was
named "the next milestone-sized decision." The user took it — "build the welded
woven-overlap orb" — which supersedes the older parked question of whether to ship a
partial-lattice orb from D-031's spike. One risk was still open from §5.4: the parity
solver had only ever run on the *tangent* field's seam graph (46 loops over 390
crossings); whether the crossing network of the *grown* field admits a globally
consistent over/under alternation — no odd cycle through the dodecahedral 5-rings — was
unmeasured, and a negative answer would have killed the weave outright.

### Decision

Build it as a graph problem feeding the existing Family-1 sweep, not as a geometric
boolean. `buildWovenOverlapGraph` (`bikar:packages/core/src/kernel3d/maclado-woven.ts`)
re-judges the ratio with the D-032 instrument on entry — the refusals are the
instrument's own, surfaced verbatim, and each is a by-design FAIL in the suite — then
grows every wheel whole through its placement frame at the grown cap angle, splits each
rim walk at its measured crossings, and interns everything in one 1e-3 mm pool so the
two wheels sharing a crossing weld it into one degree-4 node. Two facts made this
construction complete rather than approximate:

- **The lift is the same lift.** The field's `placeWheelInFrame` at the grown unit and
  the instrument's `reliftWheel` are both the gnomonic lift, pinned identical on the rim
  to < 1e-9 mm — so the instrument's crossing points land exactly on the module's grown
  rims and can be interned, not re-derived.
- **Only rims interact.** The closest a neighbour's rim comes to a wheel's pole
  (2θₜ − θ′ ≈ 16.7°) exceeds the valleys' cap angle (≈ 11.9°) throughout the window, so
  interior lattice edges never need splitting.

Measured (R=60, ribbon 1.2/1.2, amplitude 0.8; identical at ρ 1.15/1.20/1.25):
**600 nodes, 1020 edges, degree histogram {2:180, 4:420}**, 60 crossing nodes. The
parity risk resolved **positively**: the solver 2-colors the crossing network with no
odd alternation cycle, and `weaveSphereGraph` sweeps **60 closed ribbon loops over 420
alternating crossings** (360 interior + 60 rim welds) into a watertight aggregate-euler-0
mesh — 4080 vertices, 8160 triangles, ~10.1 cm³ at ρ=1.2. The DSL seam is one contextual
statement, `overlap <ratio>` on `base wheelfield`, requiring `weave` and a ratio strictly
above 1, with the window judged by the kernel rather than the parser; the preset is
`bikar:patterns/Orbs/Maclado-9-Overlap.bkr` and the published-surface count moved
118 → 119 with its own provenance paragraph.

### What this resolves and what it does not

It closes the D-032 follow-on and discharges §5.4's open risk for the grown field — the
weave exists, is globally consistent, and ships through the same DSL, gates and gallery
path as the tangent-field orbs. It does **not** touch the dense multi-ring regime past
ρ=1.30 (second-neighbour crossings, incidental faces), which stays measured only as
"regime change," exactly as D-032 scoped it. And no woven-overlap print exists — the
amplitude-vs-ribbon-depth fusing rule in the preset header and §7's nozzle-class
condition are stated, unprinted bets, like every orb on the page. What would reverse the
graph-first construction: a measured case inside the window where the swept ribbons
physically intersect *between* crossings (the sweep is per-strand and the gate per-tube,
so inter-strand collision is asserted by the ≥ (ribbon_depth + 0.4)/2 amplitude rule,
not by a mesh check) — that would force the geometric-boolean branch this decision
declined.

---

## D-034 — the Lab's coverage gaps are sweeps, not lists: a claim about every preset must read every preset

**Date:** 2026-08-15 · **Status:** Decided (shipped) · **Repos:** bikar (guard + registry + two sweep tests + an e2e seek that verifies itself, PRs [#97](https://github.com/NaqshCoffee/bikar/pull/97), [#98](https://github.com/NaqshCoffee/bikar/pull/98), [#99](https://github.com/NaqshCoffee/bikar/pull/99)), 3d-models (design doc §8 Q6, this entry, gallery `lab:` links)

### Context

Scoping the qiyas half of wheelfield validation meant opening the three Maclado presets
in the Orb Lab, and two of them could not be opened at all. What that surfaced was not
one bug but a shape: every claim the Lab makes about "the presets" was written as a
list in code, and each list had gone stale the moment Family 3 shipped, with nothing
to say so.

- `patterns/Orbs/` held 14 `.bkr` files and the Lab's registry offered **11**. The
  three wheelfield presets were rendered by this repo's Makefile and shown on the
  gallery page while being unreachable in the Lab — the one surface where a reader can
  turn a knob.
- `raiseAmplitudeFloor` in `packages/knobs/src/constraints.ts` resolved the weave's
  depth from a parameter literally named `strut_depth`. `Maclado-9-Weave.bkr` and
  `Maclado-9-Overlap.bkr` name theirs `ribbon_depth`, so the guard silently did nothing
  on exactly the two presets whose own headers state the rule it enforces — *amplitude
  must stay ≥ (ribbon_depth + 0.4) / 2 or adjacent ribbons fuse silently, because the
  mesh gate is per-tube*. A second reader had gone blind the same way and independently:
  the Lab's knob panel prints a "ribbon gap" row, `2·amplitude − depth`, marked `✗ fused`
  under 0.4, and it too read `values.strut_depth` only. The honest readout was absent
  from the designs that needed it most.

### Decision

Both fixes are sweeps over what is on disk, not longer lists. `orb-presets.test.ts`
matches registry against directory on file **content** (the registry imports `?raw`, so
identical source is what proves the chip opens the rendered file) and fails in both
directions — an orb the Lab cannot open, and a registry entry pointing at nothing.
`orb-weave-guard.test.ts` finds woven presets by `/^\s*weave crossing /m` in the source
and tests each **at the corner** (depth at its max, amplitude at its min), asserting
first that the corner really violates the floor and then that the guard moved it;
testing at defaults would have passed against a guard that does nothing. Both were shown
failing before the fix — the guard test on exactly the two Maclado weaves, the sweep
test against the pre-fix registry.

The depth knob is a **listed** pair, `['strut_depth', 'ribbon_depth']`, not a `_depth`
suffix match, so an unrelated future knob cannot enrol itself into a printability rule
by its name; and the two readers now share one exported `weaveDepthValue`, so the next
name is one edit rather than two that can drift apart again. No shipped default moves:
both Maclado weaves sit exactly on the floor at their defaults (amplitude 0.8,
`ribbon_depth` 1.2 → floor 0.8), and the fix changes behaviour only above depth 1.2.

The three presets are registered with `qiyasComposite: null` and a third trust-badge
state, **"not yet qiyas-validated"** — deliberately distinct from the existing
custom-design badge, which says something different. A recorded number would be a lie
(wheelfield views only became scoreable with the ribbon view set, and the CI job that
would record one is Q5's work), and no badge at all would read as a chip with nothing to
declare. The trio is pinned by exact id in the sweep test, so recording the first score
requires editing the assertion that says none exists.

### What this resolves and what it does not

Every committed orb is now openable in the Lab, the gallery's three wheelfield cards
carry `lab:` links, and neither gap can silently reopen. It does **not** validate the
wheelfield renders: the composites stay null until Q5 wires the job, and the badge says
so rather than implying a pass. The amplitude rule remains an asserted print constraint
rather than a mesh check, exactly as [D-033](#d-033--build-the-welded-woven-overlap-orb-the-d-032-window-holds-parity-solves-60-loops-ship) scoped it — this makes the guard fire on the presets it
was written for, not stronger.

**Superseded 2026-08-19.** The rule the guard enforced is the centreline rule
[D-039](#d-039--the-woven-orbs-print-as-one-lump-and-the-rule-that-said-otherwise-was-about-centrelines) withdrew, so the guard, `weaveDepthValue` and the shared depth-knob list are
all gone in [D-042](#d-042--a-withdrawal-is-corpus-wide-and-three-of-the-four-copies-were-not-markdown). What survives is this decision's *tenet* — a claim about every
preset must read every preset — and the mechanism that carries it: the
directory-derived preset sweep, ported into bikar's `linkage-gate.test.ts`
before the guard file was deleted.

One thing here is a partial and is recorded as such. The `packages/e2e` loop-closure
test fails on roughly 40% of CI ubuntu runs and never on macOS, including under 8× and
20× CPU throttle, and it blocked these merges. Its seek read `document.getAnimations()[0]`
— whichever animation the document lists first — and turned a missing one into "it is at
zero" with `?? 0`, either of which lands the frame an arbitrary distance from the time it
names; it now reads a `path.cell` and **verifies the phase it achieved** against the one
it asked for, across three cells, failing with the drift in milliseconds. That is a
removed mechanism and a named failure, **not a demonstrated fix** — it cannot be, from a
machine that has never reproduced the flake. If it recurs, the next report will say
whether the seek missed, the frame moved under the shutter, or the seam is real.

---

## D-035 — the rosette composites were a validator defect, not a geometry one, and a bounding box cannot see a shared edge

**Date:** 2026-08-17 · **Status:** Decided (shipped) · **Repos:** qiyas (the exclusion + its four tests, PR [#18](https://github.com/NaqshCoffee/qiyas/pull/18); the release, PR [#19](https://github.com/NaqshCoffee/qiyas/pull/19), tag `v0.4.0`), bikar (pin bump + the two recorded composites + `RECORDED_DROP`, PR [#103](https://github.com/NaqshCoffee/bikar/pull/103)), 3d-models (§3 footnote ², the §10 P2.6 note, the P2 badge copy, this entry)

### Context

Two of the fourteen orbs had never scored 1.000. `Rosette-Orb` sat at 0.954 and
`Rosette-Cube-Orb` at 0.975 from the day they were first measured (2026-07-26), through
every sweep since. [D-034](#d-034--the-labs-coverage-gaps-are-sweeps-not-lists-a-claim-about-every-preset-must-read-every-preset)'s
follow-on work carried `drop` out of the qiyas report and into `RECORDED_DROP` in
`bikar:packages/lab/tests/orb-composites.test.ts`, which pinned the shortfall at 26 shapes
on the dodeca and 4 on the cube so it could not widen unnoticed. What that pin did **not**
say is which side the defect was on. Two readings fit the same numbers equally well: bikar
draws 26 petal faces that are not really there, or qiyas fails to find 26 that are.

The pin also made the question answerable, because it named exactly which shapes went
missing. They are all petal faces, and every one of them shares a full edge with the face
it was lost to.

### The measurement that decided it

`_shapes_overlap` in `qiyas:src/qiyas/stages/detectors/reconcile.py` bucketed two candidate
shapes as one detection of the same region when three gates agreed: centroid distance under
`dedup_thresh`, bounding-box IoU over 0.6, and areas within 30%. All three read bounding
boxes and scalars. **None of them can distinguish "one region found twice" from "two regions
either side of a shared edge"**, and a mirror-image pair of triangles is the worst case for
all three at once: same area, coincident centroids, and a bounding box that is not merely
similar but *identical* when the mirror line is an image axis.

Across the 83-image corpus, 120 pairs reached the bucketing decision. Computing the actual
shared interior area splits them cleanly in two, with nothing in the middle:

| Group | Pairs | Interior-overlap fraction |
|---|---|---|
| Genuine duplicates — the same region found twice | 86 | 0.9241 … 1.0000 |
| Edge-adjacent faces — two regions, one shared boundary | 34 | exactly 0.0000 |

That gap is the whole argument. A constant chosen inside a bimodal gap this wide is a
constant no plausible re-measurement moves.

### Options

**(a) Raise `_BBOX_IOU_THRESHOLD`.** The obvious cheap fix, and it is not merely
insufficient — it is impossible. The 34 wrongly-bucketed pairs run IoU **0.6284 up to
exactly 1.0000**. A threshold that excludes the worst of them excludes every genuine
duplicate too, because there is no value above 1.0.

**(b) Add a specialist exclusion that computes the real shared area.** A shapely
intersection over the two candidate polygons, `_MIN_INTERIOR_OVERLAP_FRAC = 0.05`, read off
the gap above rather than chosen. Adds a runtime dependency edge to shapely, which qiyas
already carries.

**(c) Accept 0.954 and 0.975 as the honest reading, and keep `RECORDED_DROP` holding them.**
The status quo. It verifies nothing new, and it leaves 30 real faces invisible to a
validator whose whole job is to see them — including, silently, on any future design that
puts two faces either side of an edge.

### Decision

**(b).** The exclusion is the eighth in a file that already has seven, so the shape was
established; what it adds is the first one that reads geometry rather than a summary of
geometry. The constant is 0.05 because the measured gap is 0.0000 to 0.9241 — eighteen times
the constant on one side and zero on the other.

Four tests ship with it, and **the by-design failure is first**: two mirrored triangles
across a shared edge, at IoU exactly 1.0000, must stay separate. Then its converse — the
same two triangles genuinely overlapping must still be merged, so the exclusion is not
simply switching bucketing off. Then two crossing-band cases at 4.08% and 6.19%, which pin
the constant from both sides: move it and one of the two flips.

**The release is `v0.4.0`, and deliberately not for `v0.3.0`'s reason.** v0.3.0 was a minor
because the report gained fields (`drop`, `max_drift`); nothing gained a field here, and a
v0.3.0 report and a v0.4.0 report have the same shape and the same `SCHEMA`. It is a minor
because **what the encoder finds changed**: wire compatibility is intact and result
compatibility is not, and a consumer holding recorded numbers has work to do before adopting
the image. Do not read a policy out of the two samples — minor here does not mean "SCHEMA
bumped", it means the consumer has work to do.

**The pin and the numbers move in one commit.** `orb-validate.yml`'s `QIYAS_IMAGE`, the two
`qiyasComposite` values in `packages/lab/src/scripts.ts`, and `RECORDED_DROP`'s two non-zero
rows are one bikar PR, because the pin is what produced the numbers and a commit that moved
either half alone would be a red run with a misleading cause. `RECORDED_DROP`'s fourteen keys
stay — a blanket `toBe(0)` passes vacuously over an empty sweep, so the keys pin coverage
while the values pin the defect.

### The corpus-wide half, and one thing deliberately not done

`CLAUDE.md`'s D4 says a withdrawal is corpus-wide, so 0.954 and 0.975 were grepped for
before this was called fixed. Six sites, and they do not all get the same treatment, because
**a superseded measurement is not a withdrawn number.** 0.954 was a correct measurement of
the validator as it stood; it is not in the class D4 was built for, which is numbers that
were never true. So the live claims are corrected — §3's archetype table, §4.3's badge copy
in the P2 doc — and the dated records that say what was measured on their date are left
saying it, with a pointer forward: §10's P2.6 bullet, `docs/research/qiyas-wheelfield-validation-survey.md`
(preserved verbatim under its provenance header, as research files are), and the two
`.claude/memory/islamic-orb-project.md` entries.

For the same reason **no `WITHDRAWN` row was added to `.claude/gates/docs_gate.py`.** Its
docstring is explicit that every row there is a number *found restated as fact after the
withdrawal*, and none has been. A row would also fire on the research file and force
exculpating words into a document the repo requires to stay verbatim — a gate making a doc
worse to keep itself quiet.

### What this resolves and what it does not

Twelve of fourteen orbs scored exactly 1.000 before this and thirteen do now. The
verification chain was walked link by link rather than inferred: qiyas #18 merged, #19
merged, tag pushed, `publish.yml` green, and the image confirmed live through the packages
API before bikar's pin was allowed to reference it; then bikar #103's `orb-validate` job
green in 2m8s — and *a 2m8s pass has the same shape as a skip*, so the log says `swept 14
orb(s)` and `86 tests` (the with-sweep count, not the 87-case skip count), and the uploaded
artifact reproduces the macOS numbers exactly on Ubuntu: `drop=0`, `drift=0.0002`, both
rosettes.

That artifact matters more than usual here, because **the local sweep could not run.** Docker
would not start on this machine, and the `QIYAS_DIR` fallback dies in cairocffi — macOS
strips `DYLD_FALLBACK_LIBRARY_PATH` across the `sh` hop the sweep shells out through, so
qiyas's rasterizer cannot `dlopen` cairo. The recorded numbers came from direct per-orb
`qiyas orb-validate` runs, and CI's container is the authority that confirmed them. This is
stated rather than smoothed over: had CI disagreed, the recorded numbers would have been
wrong and the reason would have been invisible.

**One orb this does not touch, and that is the point.** `Star-Octa-Orb` still scores 0.9921
and `Weave-Orb` 0.9967, both with `drop` 0 — a *surplus*, the encoder finding more regions
than the ground truth declares, which is the opposite defect and which `RECORDED_DROP`
structurally cannot catch. §3's footnote ¹ called Star-Octa a 4-fold-tangency encoder quirk
and that reading survives, now with a post-fix measurement behind it. A narrow fix that
leaves a differently-shaped neighbour untouched is evidence the diagnosis was specific.

**What would reverse this:** a measured pair of genuinely-duplicate detections whose interior
overlap falls below 0.05. The 86-pair floor of 0.9241 says the margin is eighteenfold today,
but that floor was measured on one corpus of orb and pattern views; a producer emitting
near-tangent shapes of very different size could land in the gap, and the answer then is to
re-measure the distribution and move the constant with the new histogram beside it — not to
widen it because a case failed.

## D-036 — the breakdown page failed the only test it had; the fix is five beats, and every sentence on it is a measured number

**Date:** 2026-08-19 · **Status:** Decided (shipped) · **Repos:** bikar (depth cues, the two missing endpoint frames, the highlight, the tilt-in, the ribbon turntable, the rewritten page, PR [#111](https://github.com/NaqshCoffee/bikar/pull/111)), 3d-models (the structural gallery restyle, the stale-artifact wipe in `orbs`, `timelapse_gate.py` and its hook, the §3.4/§4.1/§8/§9 amendments, this entry, PR [#86](https://github.com/omars-lab/3d-models/pull/86))

### Context

The per-orb breakdown page shipped on 2026-08-18 with build stages, a 36-frame
turntable and a live-viewer handoff. It was reported failing its one job the next
day: **a viewer still could not see how the construction turns into an orb.** The
audit that followed rendered the frames and read them rather than reading the code
that wrote them, and found the failure was not one bug.

* Every frame carried the same `#8a8a8a` fill. No shading, no silhouette, nothing
  ever disappearing around a limb — so a rotating projection read as a wobbling
  flat mandala, which is the one thing it must not read as.
* The flat→sphere map ran *before* frame 1. The first frame was already on the
  sphere, and no flat drawing shipped in any breakdown directory. A newcomer was
  asked to accept the hardest step in the story before being shown anything.
* Twenty copies of one pattern unit were indistinguishable, so the repeat stages
  read as strokes piling up rather than as copies being placed.
* The stage camera sat 58° up and every turntable frame 18° up, byte-verified as
  never meeting — and the page played the spin *first*, then jumped back.

### The decision, and the one constraint that shaped it

**Style every surface a human looks at; keep the gray instrument byte-stable.**
`renderOrbViewSVG` has two consumers with incompatible needs: qiyas's raster
detector wants a flat, unvarying instrument, and a person wants shading and a
silhouette. The resolution is that styling is opt-in — `style` absent produces
character-identical bytes, pinned by a snapshot test written *before* the renderer
moved. That test is the shield: it protects the recorded composites, the gallery
recolor and qiyas's ground truth on this change and on every future one, which a
one-off re-record would not.

**Generality is the acceptance criterion, not a nice-to-have.** Every mechanism is
driven by what the manifest declares and nothing is keyed on an orb's name. Family
comes from the frame-kind set — cell-only (9 orbs), cell+strand (4), strand-only
(1). The highlight is keyed by each stage's *own* domain: `patternFaceIndex` for an
element stage, `baseFaceIndex` for a repeat stage, `strandId` for a strand stage.
The base solid is named from a `(faces, sides)` lookup with an honest fallback, so
"an icosahedron — 20 triangular faces" is a claim about geometry rather than about
a string someone typed, and the weave census is counted off `orbWeave.passes` — the
same passes the ribbon renderer draws from — so "60 loops over 420 crossings"
cannot disagree with the picture beside it.

**Maclado-9-Overlap reaches parity in the same stroke.** It is the orb the page
most needed to explain and the only one with no camera sweep at all, because the
sweep projected cells and its bands cross rather than tile. `projectSweepScene`
now picks cells or ribbons from what the orb can produce, so it spins on its
ribbons. Its three stale top-level cell views — an artifact of a run *before* the
engine started refusing to draw it that way — are removed, which closes the
long-standing terminal-identity failure `orb-construction-timelapse-design.md`
§4.1 had already written down as its FAIL case.

### Two findings worth keeping, both from building it

**A readout that reads the same on every frame of a moving camera is not a
readout.** Every tilt-in row reported the *destination's* angles, so frame 0 —
taken from the stage camera, 58° up on an icosahedron — claimed to be 18° up like
the orbit it had not yet reached. Found by writing the test that asserts each row
reports its own axis, and proven by running that test against the old behaviour
first.

**Regeneration cannot fix a file regeneration no longer writes.** Which drawings
an orb produces is decided by what it declares, so the set can *shrink* between
two versions of the engine. Three cell views the projector refuses by design to
produce sat in `build/orb-views/Maclado9Overlap/` for weeks — scored by qiyas,
picked as the gallery hero — because `make orbs` only ever wrote files. The fix is
a `rm -rf` of each orb's output directories before they are rewritten: only
deletion can remove an artifact the generator has stopped producing.

### What this resolves and what it does not

Closes tasks #14 (the stale views), #17 (the §9 gate) and #35 (Maclado-9-Overlap
has no sweep). The gate ships having failed twice on purpose, which is the point
of it: 14 manifests short of five keys from a stale `dist/`, and the Overlap
mismatch §4.1 predicted.

**Deliberately not built:** a `t`-parameterized flat→sphere wrap morph. It is the
one beat still told by two endpoints and a caption rather than by animation, and
it needs new geometry with nothing to reuse — the honest position is that the page
shows where the drawing starts and where it lands, and says so, rather than
implying a continuous map it cannot draw. Also unbuilt: a ghosted back hemisphere
(qiyas's detector reads `fill="none"` elements as stroke outlines, so it would have
to stay out of the instrument), per-strand highlighting on strand stages, and any
change to qiyas or to the recorded composites.

**What would reverse this:** a measured reading of the page by someone new to it
that still cannot answer "how does the flat drawing become a ball?" — the same
test this rework was opened by, applied to its result.
## D-037 — D-036's reversal test fired on first reading: the pattern had nothing under it, and the spin's edge was a detector's constraint

**Date:** 2026-08-19 · **Status:** Decided (shipped) · **Repos:** bikar (the scaffold underlay, the display cull, painter ordering, three replacement tests, PR [#113](https://github.com/NaqshCoffee/bikar/pull/113)), 3d-models (T6 rewritten with both halves, two new self-test mutations, the §3.4/§4.1 amendments, this entry)

### Context

[D-036](#d-036--the-breakdown-page-failed-the-only-test-it-had-the-fix-is-five-beats-and-every-sentence-on-it-is-a-measured-number) shipped the five-beat breakdown page and wrote its own reversal
condition: *"a measured reading of the page by someone new to it that still cannot
answer 'how does the flat drawing become a ball?'"* That reading happened the next
day, on the live page, and returned two defects in one screenshot of frame 1/32.

- **The pattern had nothing under it.** The base solid was written once, as frame
  zero, and never again. From the second frame on, cells accumulated against a blank
  page — the construction replayed in mid-air rather than on the thing being built.
  §3.4 had specified the base frame and the implementation delivered exactly that:
  *a* frame, not *a floor*.
- **The spin had a ragged edge and a permanent white ring.** Display frames were
  culled by `DEFAULT_FRONT_CAP_MIN_DOT = 0.3`, whose own docstring says it "keeps
  qiyas's 2D assumptions valid" — a **detector** constraint governing a picture no
  detector reads. Two consequences follow from culling whole cells at that threshold,
  and both are arithmetic rather than opinion: content can never exceed
  `r·√(1−0.3²) = 0.954r`, so a white annulus sits permanently inside the silhouette;
  and cells straddling the threshold vanish outright, so the boundary changes shape
  every frame, which is what reads as flicker when the orb turns.

The second is a **K10** by this repo's taxonomy — a rule ported from one domain to
another with no sentence saying what must hold for it to transfer. The sentence
could not be written, so the rule did not transfer.

### Decision

**Every stage frame carries the base solid as a stroke-only scaffold plus the
sphere's limb; `complete` carries neither.** The construction now replays on a
shape that stays put, and the terminal identity §4.1 pins is untouched because the
frame it pins is the one frame that drops both marks.

**Stage frames stay unshaded, deliberately.** A Lambert envelope makes an unplaced
region and a dim placed one look alike, and that is the single distinction a stage
frame exists to draw. Shading belongs to the spin, whose job is the opposite one.

**Display frames use `cull: 'back-face'`, tested on the centroid, painter-ordered by
`meanDot`.** `front-cap` remains the default and nothing qiyas scores asks for the
new mode. The ordering is not decoration: under the front cap the visible hemisphere
projects one-to-one onto the disc, so document order *was* a valid depth order; the
centroid test keeps limb-straddling cells whose far halves fold back over their
neighbours, and that assumption dies with it.

The cull flips with the style at `t > 0` and not at `t = 0`, which is what preserves
`transition[0] == complete`.

### The gate had an absence rule where it needed a presence rule

T6 checked that stage frames carry *no* `data-orb-style` and *no*
`data-orb-silhouette`. Every frame passed for the entire period the base solid was
missing from all of them, because a rule about marks that should be absent cannot
see a missing picture. **An absence rule is not a coverage rule**, and the fix is
that T6 now has two halves that fail in opposite directions: the scaffold and the
limb must be *present* on every stage frame and *absent* from `complete`.

Measured, in that order: against the tree as it stood, the amended gate produced
**632 findings across all 14 orbs**, every one of them the new presence half and no
other rule firing — which is the by-design failure this repo requires a gate to be
able to produce. After `make orbs` at bikar `57ee49d`: **0**.

### Verification

- Gate `--self-test`: 13 mutations, each firing on its own rule, pristine fixture
  clean. Two are new — a stage frame with its scaffold stripped, and a scaffold left
  on the finished drawing.
- The qiyas shield, re-measured across the whole instrument set rather than argued:
  78 files (`build/orb-views/<orb>/<orb>.<view>.svg` and `.gt.json`, all 14 orbs)
  hashed before and after regeneration — **byte-for-byte identical**. `style` absent
  still means unchanged output. bikar's own orb sweep re-ran the qiyas composites
  against the branch and they held.
- The three byte invariants on Star-Orb after the change: `complete` equals the
  shipped view, `transition[0]` equals `complete`, `transition[last]` equals
  `turntable[entersAtIndex]`.
- Suppressing `scaffoldElements` in bikar fails exactly two of twenty timelapse
  tests and nothing else.

**What would reverse this:** the same test D-036 wrote, applied again — a reader new
to the page who still cannot say what the flat drawing becomes. The two defects this
entry fixes were both invisible to every automated check in three repos and were
found by one person looking at one frame, which is the argument for keeping that test
in the loop rather than replacing it with the gate.

---

## D-038 — the outline the pattern burst through was a chord polygon; the scaffold now rides the sphere the pattern is on

**Date:** 2026-08-19 · **Status:** Decided (shipped) · **Repos:** bikar (`arcPoints` + the `baseSolidCells` rewrite, the failing-first sag test, the repeat caption, the e2e assertion, PR [#114](https://github.com/NaqshCoffee/bikar/pull/114)), 3d-models (T7 and its self-test mutation, criterion 11, the §9 amendments, this entry)

### Context

[D-037](#d-037--d-036s-reversal-test-fired-on-first-reading-the-pattern-had-nothing-under-it-and-the-spins-edge-was-a-detectors-constraint) put the base solid under every stage frame. One day later the same
reader looked at `breakdown.html?orb=RosetteWeaveOrb` and asked two questions about
the picture that fix produced: *why is it the same outline every time*, and *why did
this one break out of it*. They have different answers, and only the second is a
defect.

**The same outline is correct, and measurable.** Eight of the fourteen orbs sit on a
dodecahedron seen down the same vertex-3 axis, so eight scaffolds are the same
drawing because eight orbs are built on the same solid; across all fourteen there are
**5 distinct scaffold hashes**. `Rosette-Weave-Orb.bkr:46` declares `base dodecahedron`
and its manifest agrees — `faces: 12, vertices: 20, sides: [5]`. Nothing to fix; the
page just never said which solid it was drawing.

**Breaking out of the outline was real, and it was the scaffold's fault, not the
pattern's.** `baseSolidCells` handed each base face over as its bare corners, so the
renderer drew it corner to corner — and a straight line between two points on a
sphere runs *inside* it. Measured as a fraction of the radius: **0.0658 on a
dodecahedron edge, 0.1493 on an icosahedron's**. The pattern's own cells are
subdivided finely enough that every vertex lands on the sphere, so they hug it, and
they therefore sit *outside* a chord outline drawn from the same solid. On
RosetteWeaveOrb the units overhung by **3.50 mm — 5.8% of the radius, over 12% of
the outline's perimeter**. The outline was not containing the pattern because it was
never the surface the pattern was on.

A third defect fell out of reading the frame: the repeat caption said *"Everything
grey behind it is a copy already placed."* That was true when the only grey was
placed copies. D-037 added a second grey with a different meaning, and on copy 1
nothing is placed at all — **a caption is a claim about the picture, and the picture
changed underneath it.**

### Decision

**Hand each base edge over already walked as a great-circle arc.** `arcPoints(a, b)`
slerps between the corners and the subdivision count is derived, not picked: a
segment spanning angle `s` puts its midpoint at `cos(s/2)` of the radius, so the step
holding a sag tolerance `tol` is `2·acos(1 − tol)` and the count follows from the
arc. `MAX_SCAFFOLD_SAG_RATIO = 0.002` is the tolerance; on RosetteWeaveOrb it takes
the scaffold from **6 vertices per face to 31**. Slerp and not a normalised lerp,
because only slerp spaces the points evenly in angle — which is what makes the bound
hold *per segment* rather than on average.

**The caption names the second grey and says a unit may straddle an edge.** Three of
RosetteWeaveOrb's six unit-1 petals genuinely cross into neighbouring faces; the
source says petals *"fuse across edge midpoints and around shoulder points"*. That is
the pattern working, so the page says so rather than hiding it.

**T7 — a cell stage stays inside the solid the scaffold draws** (criterion 11). The
scaffold is a picture of a claim and a picture can contradict it; **T6 could not see
this, because T6 only ever asks whether the scaffold is *there*.** `strand` stages are
exempt **with a reason rather than a threshold**: a woven band's amplitude lifts it
off the sphere by design, up to 3.681 mm across the corpus. The 0.01 mm slack is for
the SVG's 4-decimal rounding, not for geometry.

### Measured

| | before | after |
|---|---|---|
| RosetteWeaveOrb overhang | 3.50 mm (5.8% of r), 12% of perimeter | 0.00 mm, 0% |
| scaffold vertices per face | 6 | 31 |
| cell stages (element/repeat), all 14 orbs | — | worst 0.000 mm |
| strand stages, all 14 orbs | — | worst 3.681 mm (by design) |

### Verification

- **The failing-first test is the sag itself**, not a vertex count: it walks every
  drawn scaffold segment on the corpus orb and asserts the worst midpoint sag is
  under `MAX_SCAFFOLD_SAG_RATIO`. It fails on the chord polygon and passes on the arc.
- **T7's by-design failure, reconstructed rather than argued.** T7 was written after
  its defect was fixed, so nothing on disk could still fail it. The pre-fix tree was
  rebuilt from the post-fix one by decimating each scaffold ring back to its five
  corners — exactly what the old code emitted, since the arc walk only interleaves
  points *between* corners it still emits. Against that reconstruction the gate
  reports **5 findings on RosetteWeaveOrb** (two `element`, three `repeat`), each
  **3.69 mm**; against the shipped tree, none. `--self-test` carries the same failure
  as a fixture mutation, and the fixture gained real ring geometry to carry it — its
  paths were `d="M0 0"`, and **a degenerate path passes a containment test by having
  no geometry rather than by satisfying it.**
- **The qiyas shield held without argument:** the 78-file instrument set hashed
  before and after — `d4adab2ae356745abfee49e098bbe9a9` both times. `complete`,
  `transition` and `turntable` frames are byte-identical; only stage frames moved.
  The scaffold appears in no frame carrying a byte identity, so it *cannot* reach the
  instrument.
- bikar: 3686 passed, 3 expected fail, 87 skipped; e2e 87 passed; `make local.ci`
  exit 0, ci-parity all 26 verified. 3d-models `make validate` green, hook-parity
  all 11.

**What would reverse this:** a scaffold that is visibly polygonal at some zoom the
page allows — the tolerance is a fixed fraction of the radius, not of the rendered
size, so a viewer that scales far past the 120 mm viewBox would eventually show the
segments. The fix then is to make `MAX_SCAFFOLD_SAG_RATIO` a function of the
projected size, not to subdivide harder everywhere.

---

## D-039 — the rule that kept the orbs apart was about centrelines, and a ribbon has width: four of five shipped fused

**Date:** 2026-08-19 · **Status:** Decided (shipped) · **Repos:** bikar (`linkageGate`, the five re-cut sources, two re-pinned by-design tests, three re-recorded ribbon hashes, PR [#116](https://github.com/NaqshCoffee/bikar/pull/116)), 3d-models (`CAL-CLR-01`, coupon MC-8, the count reconciliation, this entry)

### Context

The reader looked at `breakdown.html?orb=RosetteWeaveOrb` and asked whether these
orbs would survive being printed — *"they feel like they would crumble / parts not
fully connected."* That is a question `meshGate` structurally cannot answer. It asks
whether the mesh is manifold and whether the struts clear the FDM feature floor; a
woven orb passes both while being **one lump of plastic**, because a mesh that
interpenetrates itself everywhere is still a mesh. So `linkageGate` was built to ask
the other question — are the bodies separate, and is anything holding them together?

Then the gate was run, and it inverted its own premise.

**All five woven sources carried the same prose rule**, unenforced by anything:
*keep amplitude at or above `(strut_depth + 0.4) / 2`*. It is a statement about where
two ribbon **centrelines** sit at a crossing, and a ribbon is not a centreline. The
other ribbon's surface is half a width off the node, and at that offset the
sinusoidal weave has already decayed toward the sphere — the denser the crossing
pattern, the less of the amplitude is left where the surfaces actually meet. The rule
has no term for that, so it cannot be right for two patterns at once.

**The proof is a controlled pair.** `Weave-Orb.bkr` and `Rosette-Weave-Orb.bkr` ship
identical struts — `width 3`, `depth 2.4` — so the rule prescribes the same floor,
1.4, for both, and both shipped at 1.6, above it. Measured: Weave-Orb fused **all 75**
ribbon pairs into a single body; Rosette-Weave-Orb held **0.049 mm**. Same rule, same
inputs, opposite outcomes. The rule was not slightly wrong about a constant; it was
missing a variable.

### Decision

**Amplitude is measured, not derived.** Each of the five sources is pinned at the
first step of its own declared ladder that clears `linkageGate`'s body-clearance
floor **as `--check` measures it**, and the comment block in each file says so and
tells the next reader to re-run rather than re-derive. The false rule and the
consequence sentences it supported (*"nothing can be pulled off the assembly"*, on
orbs that were one object) are deleted, not softened.

**Two ranges were widened, and that is the load-bearing half.** Two of the measured
values landed on the *ceiling* of their declared range with ~0.03 mm to spare —
`Weave-Orb` at 2.6 in `1.4..2.6`, `Maclado-9-Weave` at 1.6 in `0.8..1.6`. A default
nobody can turn up re-fuses on the next strut-width change with no legal escape, so
the ranges go to `1.4..3.0` and `0.8..2.0`. Pinning a value at a wall it cannot move
off is how a measured default quietly becomes an unmeasurable one.

**The floor itself is not measured, and says so.** `MIN_BODY_CLEARANCE_MM = 0.4` was
lifted from the same prose rule this entry just discredited. Promoting a number from
a comment to a gate makes the doubt *checkable*; it does not make the number
*measured*. It ships provisional against **`CAL-CLR-01`**, and coupon **MC-8** — six
wall pairs printed in place at 0.1…0.8 mm — is what ends it. Not MC-1: a press-fit
ladder measures two parts assembled, this measures two surfaces never separated, and
there is no transfer sentence to write between them (**K10**).

### Measured

| orb | amplitude | clearance before | clearance after |
|---|---|---|---|
| `Weave-Orb` | 1.6 → **2.6** | 0.000 mm, **75 fused pairs** | 0.438 mm |
| `Rosette-Weave-Orb` | 1.6 → **2.0** | 0.049 mm, 0 fused | 0.642 mm |
| `Weave-Dodeca-Orb` | 1.6 → **2.2** | 0.000 mm, **45 fused pairs** | 0.408 mm |
| `Maclado-9-Weave` | 0.8 → **1.6** | 0.000 mm, **155 fused pairs** | 0.427 mm |
| `Maclado-9-Overlap` | 0.8 → **1.4** | 0.000 mm, **90 fused pairs** | 0.482 mm |

Four of five were outright interpenetrating; the fifth was at an eighth of the floor.
**Every woven orb the gallery has ever shipped would have printed as one object.**

### Verification

- **`make orbs` is the front door.** The target already runs `--check` on every
  source, so the gate would have turned the build red rather than filed a report.
  After the re-cut: exit 0, 14 orbs, `fusedPairs=0` on all five, every clearance above
  the floor.
- **Two by-design failures were silenced by this fix, and both were re-pinned rather
  than deleted.** This is the part worth remembering:
  - `linkage-gate.test.ts` demonstrates fusion on WeaveOrb by **reading the amplitude
    out of the file**. The finding changed the file, so the demonstration would have
    started passing — a by-design failure that silently stops failing has stopped
    testing the thing it exists for, and the source it read is exactly what the
    finding moved. The 1.6 is now a literal in the test, with the reason written above
    it.
  - The ribbon-view parity test's wrong-sort demonstration also went quiet. Its real
    scope was **measured, not guessed**: swept over both woven presets × 3 symmetry
    views × amplitude 0.8–2.0, the wrong sort is detectable in **exactly 1 of 42**
    configurations, and the new default is not one of them. Re-pinned at 1.2 — and the
    *silence* at the shipped amplitude is pinned too, so if a future change makes it
    detectable again the line fails and the comment gets rewritten instead of
    outliving its measurement.
- **The instrument re-record followed its own prescribed order** — regenerate views,
  re-run the sweep, re-pin composites, **update hashes last**. Three ribbon hashes
  moved (`vertex-3`, `face-5`, `edge-2` on Maclado-9-Overlap); **no cell hash moved**,
  because a cell view draws the pattern and not the weave, and amplitude is the one
  orb parameter only a ribbon view reads. The sweep put every composite exactly where
  it was pinned — all five `ribbons` at 1.000, `weave-icosa` cells 0.997, StarOcta
  0.992, drop 0, maxDrift 0.0003 — so `packages/lab/src/scripts.ts` needed no edit. A
  hash rewritten before that sweep would have asserted the same thing while measuring
  nothing.
- **The feared three-repo cascade was one repo, measured rather than assumed:**
  `build/` is gitignored here, so orb views are build artifacts and not checked-in
  state, and the sweep runs inside bikar.
- bikar `npm run ci`: 3708 passed, 3 expected fail, 87 skipped, 0 lint errors; e2e 88
  passed. qiyas sweep mean composite 1.000, PASS. 3d-models `make validate` green.

**What would reverse this:** MC-8 measuring the floor somewhere other than 0.4. Every
one of the five is pinned at the first ladder step clearing *this* number, so moving
it re-cuts all five — which is the argument for the number living in one place with a
bet id on it rather than in five comments. And MC-8's second question can break the
shape rather than the value: if a gap held open across layers behaves differently from
one held open along them, a single `MIN_BODY_CLEARANCE_MM` is the wrong object and the
gate needs two constants, not a new value for one.

---

## D-040 — the second overlap band builds two chains, not an orb; and the band's reported ceiling was the end of the sweep

**Date:** 2026-08-19 · **Status:** Decided (shipped) · **Repos:** bikar (`Maclado-9-Overlap.bkr` range and header, two new `linkageGate` tests, one re-pinned literal), 3d-models (research §5.1, this entry)

### Context

`Maclado-9-Overlap` declares `param overlap = 1.2`, a cap-growth ratio. A D-032
sweep found its feasible set is **not an interval**: two bands, `[1.08, 1.26]` and
`[1.38, 1.60]`, separated by a dead band where 30 of 30 adjacent pairs refuse to
weld. The two bands are different weave regimes — 750 ribbon polygons against
516, 270 `over` passes against 192 — so the second is not the first drawn larger.

That measurement carried its own caveat, and the caveat is why the question stayed
open for two weeks: *"Everything above is a compile-time result. No STL was
exported, no qiyas score was run, and nothing here says the second band is a
legitimate solid rather than one that happens to survive the welder."* The
instrument that could say — `linkageGate` — did not exist. D-039 built it. This
entry is that instrument turned on the question.

### Decision

**Band two is closed.** It compiles and it is not an orb, so nothing will be built
on it and the declared range stays inside band one. **Band one's declared range is
narrowed from `1.15..1.25` to `1.15..1.22`**, because its own ceiling was
unprintable.

### Measured

Re-run as `render --format stl --check`, amplitude held at the shipped 1.4.

Every ratio in band two, from bisected edge to bisected edge, fails identically:

| overlap | pieces | clearance | fused pairs | verdict |
|---|---|---|---|---|
| 1.38 | **2** | 0.000 mm | 60 | FAIL |
| 1.46 | **2** | 0.000 mm | 180 | FAIL |
| 1.60 | **2** | 0.000 mm | 180 | FAIL |
| 1.80 | **2** | 0.000 mm | 310 | FAIL |

`pieces=2` is the finding. The 60 ribbons close into two 30-ribbon chains with no
link between them: the print lifts apart into two halves. It also interpenetrates
everywhere. **Neither is curable by amplitude** — the knob that rescued all five
orbs in D-039. Swept at ratio 1.44 across amplitude 1.4, 2.0, 2.6, 3.2 and 4.0 —
nearly 3× the shipped value — `pieces` never leaves 2 and `fusedPairs` never falls
below 60.

**The band's ceiling was never measured.** `[1.38, 1.60]` was reported to the end
of a sweep that stepped 0.02 and stopped at 1.60. 1.68 and 1.80 both weld; the
real ceiling is ~1.84, after which three *different* mechanisms refuse in sequence
(weld-node spacing, crossing-to-crossing spacing, then strand parity). Bisected to
0.005, the edges are `(1.075, 1.08]`, `1.265 / 1.270`, and `1.365 / 1.370`.

**And the declared range's own ceiling was unprintable.** Inside band one, welding
is not the binding constraint — body clearance is, and it does not taper toward
the edge, it falls off a cliff:

| overlap | 1.20 | 1.21 | 1.22 | 1.23 | 1.24 | 1.25 |
|---|---|---|---|---|---|---|
| clearance | 0.482 | 0.490 | **0.498** | 0.348 | 0.001 | 0.000 |
| fused pairs | 0 | 0 | 0 | 0 | 0 | **60** |

At 1.25 — the stop the Lab's slider comes to rest against — 60 body pairs
interpenetrate. The shipped default 1.20 was never at risk; the value one step
past it was, and the range invited it.

### The tenet

**A declared range is a promise, and its endpoints are the least tested values in
it.** A `range lo..hi` becomes a slider, so every value in it is one a user is
invited to build, and the two a user reaches fastest are the stops. Both were
wrong here in the same file: `1.25` fuses, and the sibling `amplitude 0.8` fuses
too. Test the endpoints, not the default — the default is the one value someone
already looked at.

The test reads the endpoints out of the `.bkr` rather than pinning them, so it
keeps holding if the range moves again. Against the old range it fails
`overlap=1.25: expected 60 to be +0`; against the new one it passes.

### Verification

- `both endpoints of the declared overlap range build a printable orb` — fails
  before the narrowing, passes after (demonstrated, not asserted).
- `the second overlap band compiles, and is two loose chains rather than an orb` —
  a by-design failure pinning `pieces=2` at amplitude 1.4 **and** 4.0, so the
  demonstration cannot be quietly cured by the knob that cured D-039.
- The widened-source rewrite both tests depend on now asserts it substituted:
  a drifted literal used to turn the setup into a silent no-op, which fails
  loudly but for a misleading reason.
- bikar full suite: 3710 passed, 3 expected fail, 87 skipped.

**What would reverse this:** a welder that could link band two's two chains — the
piece count is a property of how that regime closes its loops, not of any
dimension, so it would take a different closure rule rather than a different
number. The clearance cliff would also move if `CAL-CLR-01` measures the floor
somewhere other than 0.4 mm, which re-cuts the 1.22 ceiling exactly as it re-cuts
the five amplitudes.

## D-041 — in a refactor, robust and simplifying outrank cheap: the `display/` shield was the wrong recommendation

**Date:** 2026-08-19 · **Status:** accepted · **Supersedes:** the option ranking
offered for tasks #53–#58 on 2026-08-19, not the audit findings behind them.

### Context

The [breakdown-page audit](research/orb-stage-decomposition-measurement.md)
confirmed that the 2D ribbon projection shatters: `orb-ribbons.ts:195` places every
pass on a **constant** shell at `radiusMm ± amplitudeMm`, while the 3D mesh at
`weave.ts:479` **interpolates** that offset to zero at the corners. A connected
solid cannot project to a disconnected figure, so every gap in the drawing is an
approximation artifact, growing as roughly `2·amplitude·ρ` — which is why
[D-039](#d-039)'s amplitude re-cut, correct for the print, widened every split by
75% in the picture.

Two remediations were offered. Fixing the projector changes the qiyas-scored
instrument set and therefore triggers the three-repo re-record cascade. Applying
the flattening only to the `display/` variants uses the subdirectory shield that
already exists and touches no pinned byte. The second was recommended, on the
ground that it "costs nothing".

That ranking priced only what was visible at the moment of choosing, which is the
exact failure `CLAUDE.md`'s *Robustness over ease* section exists to prevent. The
cheap option was recommended **because** it was cheap.

### Decision

**Delete the divergence rather than route around it.** Three rankings are
reversed:

1. **The projection (#54, #55, #56).** `orb-ribbons.ts` takes its offset from the
   same function the mesh uses, and the cascade is paid once. The `display/`
   shield would have made two disagreeing answers to *"where is a ribbon's
   surface"* permanent, and doubled every future ribbon change. It would also have
   left the qiyas-scored instrument certifying a picture we had already measured
   to be false — which is the argument that killed the link checker, turned around:
   **a gate that cries wolf gets switched off, and an instrument known to be wrong
   is worse than no instrument.** The cascade is not speculative; its shape was
   measured when task #52 ran it for D-039.
2. **The amplitude floors (#53).** Held because narrowing the five declared ranges
   would silence a by-design test whose point is that the value is *legal*. That
   coupling is itself the defect: the test reads the shipped orb's floor. Give the
   fuse-refusal test its own fixture source, then narrow all five ranges to what
   `linkageGate` measures as printable. One rule survives instead of two — a
   declared range is a promise measured at **both** endpoints ([D-040](#d-040)).
3. **`overlap` requires `weave` (#58).** Framed as a side effect of #54; it is its
   own simplification. Plain lines are the base case and weave is the option, and
   the parser coupling at `parser.ts:1444-1447` is the only line that says
   otherwise.
   **Reversed by measurement — see [D-044](#d-044--overlap-requires-weave-is-a-kernel-fact-and-the-measurement-is-what-ships).**
   The coupling is not a parser line. The solid branch has no overlap path at all,
   and the grown field fails the manifold gate at every ratio the shipped orb
   declares, so deleting the rule buys either a knob that changes nothing or a mesh
   that does not close. This item is left standing rather than edited: it is what
   the ranking believed, and the entry that disproves it is the record.

Unchanged: #57's two teaching defects are page-level and independent of all three.

### The tenet

> In a refactor, robust and simplifying outrank cheap. Two code paths that
> disagree *are* the defect: prefer the change that deletes the divergence to the
> one that routes around it, price the cascade, and pay it. A one-time migration
> never buys a permanent fork.

Recorded as a corollary in `CLAUDE.md` under *Robustness over ease*, beside the
by-design-failure corollary it rhymes with.

### Verification

A tenet is not gate-checkable, and no gate is proposed for it — the precedent in
[`issue-register-evaluation.md`](issue-register-evaluation.md) is that a rule
earns a gate by measured recurrence, and this has one instance. What is checkable
is each reversed ranking:

- **PASS (#54):** after the projector change, `git status` on `build/orb-views`
  shows ribbon geometry moved and *nothing else*, and the styleless byte-stability
  snapshot still holds for every non-ribbon view.
- **FAIL (#54):** any cell-family view byte-changes, or a `display/` variant
  diverges from its top-level counterpart in anything but style — either means the
  offset was forked again rather than shared.
- **PASS (#53):** the fuse-refusal test compiles its own fixture and fails before
  the ranges are narrowed, passes after; all five orbs' declared floors clear
  `linkageGate`.
- **FAIL (#53):** the test still reads a shipped `.bkr`, which reintroduces the
  coupling under a new name.

### What would reverse this

If the qiyas re-record proves unrepeatable — a ground-truth record that cannot be
regenerated from sources this repo has — then the shield becomes the honest option
and must ship **labelled as a known-wrong instrument**, not as a fix. Cost alone
does not reverse it; only impossibility does.

## D-042 — a withdrawal is corpus-wide, and three of the four copies were not markdown

**Date:** 2026-08-19 · **Status:** accepted · **Extends:**
[D-039](#d-039--the-woven-orbs-print-as-one-lump-and-the-rule-that-said-otherwise-was-about-centrelines) · **Supersedes:** the guard mechanism of
[D-034](#d-034--the-labs-coverage-gaps-are-sweeps-not-lists-a-claim-about-every-preset-must-read-every-preset), not its tenet.

### Context

[D-039](#d-039--the-woven-orbs-print-as-one-lump-and-the-rule-that-said-otherwise-was-about-centrelines) measured `amplitude >= (strut_depth + 0.4) / 2` and found it wrong —
it predicts the gap between two ribbon **centrelines**, but a ribbon has width, so
the other ribbon's surface sits half a width off the crossing node, where the
sinusoidal offset has already decayed. Four of the five woven orbs shipped fused
under it. D-039 withdrew it from the prose and re-cut the five defaults from
measurement.

It kept running. `CLAUDE.md`'s **D4** — *a withdrawal is corpus-wide, not a local
edit* — is enforced by `docs_gate.py`, which scans **markdown**. Three of the four
surviving copies were TypeScript, a `.bkr` header field, and a test file:

| # | site | what it did |
|---|---|---|
| 1 | five `.bkr` amplitude `range` floors | D-039 moved the **defaults** and left the **floors** behind |
| 2 | `bikar:packages/knobs/src/constraints.ts` `raiseAmplitudeFloor` | clamped the Lab slider by the rule |
| 3 | `bikar:packages/lab/src/main.ts` `weaveRows` | printed `2·amplitude − depth` as a ✓/✗ tick |
| 4 | `bikar:packages/lab/tests/orb-weave-guard.test.ts` | an entire file certifying site 2 |

Site 1 is not cosmetic. A declared range is a **promise**: the parser rejects an
override outside it (`parser.ts:1136`) and the Lab renders it as a slider, so every
stop in it is a value someone is invited to build. Swept step by step with
`linkageGate`, the amplitude at which each preset actually stops fusing turns out to
equal the value D-039 set as its default — so the floors were offering exactly the
band D-039 had just measured as unprintable.

Site 3 is the one a user meets. At Weave-Orb amplitude 2.0 with `strut_depth` 2.4
the Lab printed **`ribbon gap 1.6 mm ✓`** while `linkageGate` measures **60
interpenetrating pairs and zero clearance** — a green tick at the moment someone
decides to print. Its companion row, `N interlocked`, was a connected-component
count, which says how many shells the mesh has and nothing about interlocking:
strands are swept independently and never booleaned, so two ribbons passing straight
through each other are still two components.

The evidence that these were one rule, not four coincidences, was already checked in.
Site 2's own suite contained a test named *`agrees with the Lab ribbon-gap row it
shares a depth knob with`*, whose comment states that the clamp and the readout are
"one inequality written two ways".

### Decision

Delete the divergence rather than route around it, per
[D-041](#d-041--in-a-refactor-robust-and-simplifying-outrank-cheap-the-display-shield-was-the-wrong-recommendation). There is now **one** measurement of ribbon separation in the
system, `linkageGate`, and the Lab, the CLI and the tests all read it.

Ranges narrowed to the measured floor:

| preset | range before | range now | clearance at the new floor |
|---|---|---|---|
| Weave-Orb | `1.4..3.0 step 0.2` | `2.6..3.0` | 0.4384 mm |
| Weave-Dodeca-Orb | `1.4..2.6 step 0.2` | `2.2..2.6` | 0.4079 mm |
| Rosette-Weave-Orb | `1.4..2.6 step 0.2` | `2.0..2.6` | 0.6418 mm |
| Maclado-9-Weave | `0.8..2.0 step 0.1` | `1.6..2.0` | 0.4270 mm |
| Maclado-9-Overlap | `0.8..1.6 step 0.1` | `1.4..1.6` | 0.4824 mm |

**Validator:** every step of every woven preset's declared amplitude range compiles
to a mesh on which `linkageGate` reports zero interpenetrating pairs and no `L3`
finding, and the step **below** the declared floor does not.
PASS: `Rosette-Weave-Orb` at 2.0, 2.2, 2.4, 2.6 — all four stops, clearance
0.6418 mm at the floor, no `L3`.
FAIL: `Weave-Orb` at 2.4 — one step under its floor — where the gate reports an
`L3` clearance error, so the range cannot be narrowed to a merely cautious value
and still pass.

The endpoints alone would not discharge this: **an aggregate cannot discharge a
claim about every part**, and a range is exactly a claim about every part of itself.

Both by-design fuse demonstrations stay on **shipped geometry**, widening the range
in the fixture text through a helper that throws if the `range` line stops matching.
This reverses my own earlier plan to give them a hand-built fixture: the module
header states the property that *a gate demonstrated only on hand-built fixtures has
not been shown to fire on anything anyone will actually print*, and moving them
would have traded the load-bearing case for a convenient one.

Site 4's deletion is a net gain in coverage, not a loss. The file had already gone
structurally dead — it tested "the corner", depth at max and amplitude at min, and
after D-039's re-cut the corner no longer violated the floor on 4 of 5 presets, so
it failed with *"this corner does not reach the floor — pick another"*. Its one good
idea, deriving the preset list from disk by matching `/^\s*weave crossing /m` rather
than typing it, is [D-034](#d-034--the-labs-coverage-gaps-are-sweeps-not-lists-a-claim-about-every-preset-must-read-every-preset)'s tenet and was ported into the new sweep before the
file was removed.

### What this resolves and what it does not

It resolves the P1 defect: no woven preset now offers an amplitude that fuses, and
no surface in the system claims a clearance it did not measure. The Lab's weave rows
report bodies, how many the gate certifies as held, and the measured minimum
clearance — with `minBodyClearanceMm === null` printed as *"none within 1.2 mm"*
rather than as a zero, because it is a pass, not an absence.

It does **not** make 0.4 mm a measured floor. `MIN_BODY_CLEARANCE_MM` stays
provisional against `CAL-CLR-01`, settled by coupon MC-8; the 0.4 survives the
withdrawal of the formula around it because that term was always about what a nozzle
can leave open, never about the geometry the rest of the formula got wrong. Every
number in the table above moves if MC-8 lands somewhere else.

It also does not extend D4 to non-markdown. The gate still scans prose, and the
reason this defect was found at all is that a human went looking after D-039, not
that anything fired. What it leaves behind instead is the sweep test: the ranges are
now checked against the gate on every run, so this particular rule cannot come back
silently even though a gate for the general case does not exist.

**What would reverse this:** `CAL-CLR-01` measuring the clearance floor somewhere
other than 0.4 mm, which re-cuts all five ranges; or a change to the ribbon sweep
that alters where surfaces actually sit, in which case the sweep test fails and the
floors are re-measured rather than re-derived.

## D-043 — the picture derived the weave's offset a second time, and got the corners wrong

**Date:** 2026-08-19 · **Status:** accepted · **Executes:**
[D-041](#d-041--in-a-refactor-robust-and-simplifying-outrank-cheap-the-display-shield-was-the-wrong-recommendation)'s
ruling, and closes the P2 defect that ruling was about.

### Context

[D-041](#d-041--in-a-refactor-robust-and-simplifying-outrank-cheap-the-display-shield-was-the-wrong-recommendation)
withdrew the `display/` shield and named the cascade the price of fixing the
projector at source. This is that fix, and running it found the defect was larger
than the audit had described.

`projectRibbonPasses` put all three spine points of a pass on **one** shell,
`radiusMm ± amplitudeMm`, chosen by `pass.isOver`. `sweepStrand`, which builds the
mesh that is actually printed, uses a different rule: ±amplitude at a crossing,
**0 at a corner**, interpolated between. The two disagreed in two ways at once, not
one:

- a corner *inherits* `isOver` from the crossing it came from, so every corner was
  drawn a full amplitude off the shell it is on; and
- an edge whose two passes disagree on parity had its midpoint drawn **twice**, at
  two radii `2·amplitude` apart — so the drawn network came apart at exactly the
  points where the solid runs on unbroken.

Measured on Maclado-9-Overlap's hero view, the gap is **1.09 mm** — of the same
order as the strut itself, which is why the audit read it as a shattered figure
rather than as a seam.

### Decision

Delete the divergence rather than teach the projector to imitate the mesh —
[D-041](#d-041--in-a-refactor-robust-and-simplifying-outrank-cheap-the-display-shield-was-the-wrong-recommendation)'s
tenet applied to its own case. `passRadialOffsetMm` is exported from `weave.ts` and
called by both paths. The sweep no longer re-derives parity from the crossing map;
the passes are built *before* the sweep and the sweep reads them. The projector
calls the same function and averages over each edge's two passes, so the two bands
meeting at a midpoint arrive at one radius by construction. Every edge is `edgeOut`
of exactly one pass and `edgeIn` of exactly one other — the premise the average
rests on, asserted rather than assumed.

Two defects the same tree was carrying are fixed here, because they are the same
mistake seen from two other angles:

- **The silhouette was drawn on the centreline the weave rides around.** At
  `radiusMm` it sits outside the ribbons on a turntable frame and well inside the
  drawing's edge on a stage frame. Scenes now declare `limbRadiusMm` — `radiusMm`
  for cells, `radiusMm + amplitudeMm` for ribbons — so each representation answers
  for its own outline instead of the renderer guessing from culled polygons, which
  would make the outline breathe across a transition. The K10 in that comment
  calling the overshoot "a few tenths of a millimetre" was measured on cells and
  never re-derived for ribbons: it was **1.6 mm**.
- **Stage frames were built by filtering the finished scene**, in which every
  under-pass had already been cut for every crossing on the orb — so a loop arrived
  pre-chopped for a weave that is not in the frame. A gap is a fact about a *pair*
  of loops, so the drawn subset is now a projector input (`drawnStrandIds`) and not
  a filter.

### Validator

**Validator:** the drawn ribbon network must be continuous at every shared edge —
for each junction, the end cross-section of the pass leaving an edge and the start
cross-section of the pass entering it project to the same two points, and every
corner sits on the centreline shell (`passRadialOffsetMm === 0`).

PASS: `Maclado-9-Overlap` at the shipped amplitude — all 420 junctions agree to
under `1e-9`, and every non-crossing pass reports offset exactly 0.

FAIL: the pre-fix projector on the same orb — every corner is off its shell by the
full amplitude, and each parity-disagreeing edge reports its midpoint at two radii
`2·amplitude` apart; the largest measured separation is 1.09 mm.

### The by-design test moved with the geometry, and was re-measured

The parity-vs-depth tripwire — a test that fires when bands are painted by weave
parity instead of by depth — was **re-measured over 42 swept configurations, not
re-pinned**. The wrong sort used to be detectable only at amplitude 1.2 and below
(3 of 42), with the shipped 1.4 sitting on the silent side; it is now detectable
from 1.0 through 2.0 (6 of 42), the shipped default among them, by 0.717 mm. The
number moved because the geometry did, and the direction is the point: the tripwire
now covers the configuration that actually ships.

The overlap validator learned one thing in the same stroke: two runs of a single
under-pass are **one element**, not a pair to order. They share a `patternFaceIndex`
and a depth by construction, and once the spine is a fold their arms can cross in
projection seen edge-on. That started as a corner case — 4 pairs on
Maclado-9-Weave's `edge-2` view at amplitude 1.9 and up, nowhere else in the sweep
— and the fold-split below made it the ordinary one: every pass is now two elements,
so the exemption carries the whole weave. Re-measured across the 15 symmetry views
of the five woven orbs at their shipped parameters: **88 same-pass pairs**, 64 on
untrimmed crossings, 24 on corners, and 0 on a gapped under-pass, whose two runs are
cut apart and cannot reach each other.

### What this resolves and what it does not

It resolves the P2 defect and the two absorbed into it. It does **not** introduce a
flat→sphere morph, ghosted back hemisphere, or any other beat the breakdown page
still lacks; those remain where the timelapse plan left them.

It also does not make the projector and the sweep the same code — they still build
different things, a picture and a mesh. What they no longer do is answer the same
question twice. If a third consumer of weave parity appears, it calls
`passRadialOffsetMm` or it is the next instance of this defect.

**What would reverse this:** a weave whose corners genuinely do not sit on the
centreline shell — a variable-amplitude sweep, say — in which case
`passRadialOffsetMm` grows a parameter and both callers get it, rather than one of
them re-deriving it.


## D-044 — `overlap` requires `weave` is a kernel fact, and the measurement is what ships

**Date:** 2026-08-20 · **Status:** accepted · **Reverses:** item 3 of
[D-041](#d-041--in-a-refactor-robust-and-simplifying-outrank-cheap-the-display-shield-was-the-wrong-recommendation)'s
ranking. **Ships:** bikar #120. **Closes:** task #58.

### Context

[D-041](#d-041--in-a-refactor-robust-and-simplifying-outrank-cheap-the-display-shield-was-the-wrong-recommendation)
ranked three defects under the *robust and simplifying outrank cheap* tenet and put
`overlap`-requires-`weave` third, calling it "its own simplification": plain lines
are the base case, weave is the option, and one parser rule is the only thing
saying otherwise. The task written from that ranking set a PASS condition —

> a `.bkr` declaring `overlap` and no `weave` compiles and renders plain crossing
> lines; the existing woven orbs are byte-unchanged

— and a FAIL condition that only tested whether `overlap` was doing double duty on
the woven path. Neither asked what the *solid* path does with `overlap`.

### What the measurement found

`decl.overlap` has exactly two consumers, and neither is on the solid branch.
`solidWheelfieldMesh` reaches `solidifyMacladoField(field, params)` and never reads
it. So deleting the parser rule has two outcomes and both are worse than the error
it removes.

**Leave the solid path as it is.** The STL is byte-identical to the same file with
the `overlap` line deleted — the knob changes nothing — while the evaluator still
withholds `orbCells` under `overlap`, so the orb loses its 2D views as well. A
silently-ignored knob that breaks the pictures is not a simplification.

**Wire `overlap` through, the obvious completion.** Growing the cap half-angle is
the grown field as far as the solidifier is concerned; it recomputes `unitMm` from
`capHalfAngleDeg` and lifts through the same frames. Measured:

| field | watertight | euler | volume mm³ |
|---|---|---|---|
| tangent — what `Maclado-9.bkr` ships | **true** | −756 | 40241.1 |
| grown ×1.15 — bottom of the declared range | false | −36 | 41206.6 |
| grown ×1.20 — the default | false | −36 | 41522.1 |
| grown ×1.22 — top of the declared range | false | −36 | 41647.3 |

Growing the caps breaks every tip-to-tip join — the joined tips stop coinciding, so
the vertex pool stops welding them — and the 12 filler rings were computed for
tangent rims they no longer meet. What comes out is a shell with open seams, and
`solidWheelfieldMesh`'s manifold gate raises on it.

Nothing renders plain crossing lines because there is no renderer behind that
phrase. Crossing rims mean interpenetrating strut bands, bikar has no boolean
union, and weaving is the one construction it has that resolves a crossing without
one — by routing over and under. That is not a grammar coupling; it is the reason
the weave branch exists.

### The decision

No rule is deleted. What ships is the measurement, because the rule had already
been mis-read once from a reading of the source that was locally correct: `weave`
*is* optional in the grammar, `Maclado-9.bkr` *does* ship weave-less, and the rule
*is* six lines. Every one of those is true and the conclusion drawn from them was
still wrong, so the fix is the thing that makes the next reader stop — *the
by-design failure is the load-bearing case*, so it is measured rather than skipped.

- `bikar:packages/core/tests/kernel3d/maclado-overlap.test.ts` pins the tangent
  control against four grown ratios spanning the declared range. It fails if anyone
  makes the grown field solidifiable without revisiting the rule.
- The parser error and the `overlap` docstring in `bikar:packages/core/src/dsl/ast.ts`
  name the measured reason and point at that test, in place of the bare assertion
  that "the pierced shell has no overlap construction".
- The parser test's title now says *the solid shell has no overlap branch*, which
  is the checkable claim, and cites where the why is measured.

### What this does not resolve

It does not say plain crossing lines are unbuildable — only that they are not a
line deletion. Building them means giving the solid branch its own grown-field
construction: rim-arc filler rings for the crossed regions, and some resolution of
the interpenetrating bands at the 60 crossings. That is kernel work of the size the
weave branch was, and no orb currently asks for it.

It also does not touch the tenet it reverses an item of. *Robust and simplifying
outrank cheap* is what sent this to measurement in the first place; what the
measurement corrected was the belief that deleting the rule was the simplifying
move. The cheap option here was to delete six lines, and it was cheap precisely
because it did not look at the branch that would have to absorb the consequence.

**What would reverse this:** a solid construction for the grown field that closes —
at which point the rule narrows from "requires weave" to whatever the new branch
cannot do, and the test above becomes its acceptance criterion rather than its
guard.

---

## D-045 — the finished orb gets its limb back, and the identity names the substitution

**Date:** 2026-08-20 · **Repos:** bikar [#121](https://github.com/NaqshCoffee/bikar/pull/121) → `8dda702`, 3d-models
**Supersedes:** the second half of D-037's scaffold rule (this log, 2026-08-19)
**Status:** shipped, deployed

Two teaching defects on the breakdown page. They look unrelated and they are the
same defect: a correct local rule, still being applied where it had stopped
being about anything.

### 1. The one picture a reader stops on was the one with no depth cue

Every stage frame and every turntable frame draws the sphere's edge as a circle.
The `complete` frame did not — and a symmetry-view SVG of a finished orb with no
limb is a flat rosette. The reason it did not was §4.1: that frame is pinned
byte for byte against the shipped instrument view, and the instrument view
cannot carry the circle, because qiyas classifies a `fill="none"` element as a
foreign contour. So a rule about bytes had quietly decided what a reader gets to
see.

The identity was never "no differences" — it already named one, the display
ground. The limb is now the second named substitution. What makes that
affordable rather than a relaxation is a fact about the cull: **under the
front-cap cull the clip the silhouette installs is a no-op**, because nothing
the front cap keeps reaches the limb at all. On a terminal frame the pair is
decoration and strips cleanly, so the check stays a byte identity against a
derived expectation, with the radius read off the frame under test rather than
recomputed — the claim is that the limb is the *only* addition, not that the
checker can predict where it sits.

**Measured, and it is the by-design failure this change shipped with.** Against
the tree before regeneration the amended gate reports **32 findings across all
14 orbs** — every complete frame blind, two findings each for the orbs with one
and three for the two with two complete frames. `make orbs` against bikar
`8dda702` clears it: `timelapse: 14 orb breakdown(s) checked / OK`.

### 2. The slider's denominator was the other number

The strand lede read *"each step threads one more loop **of the 60** closed
loops on the orb"* beside a slider with 30 steps. Both numbers are real — 60 is
Maclado-9-Overlap's loop census, 30 is how many face the hero camera — but only
one is the slider's denominator and the sentence named the other, so a reader
dragging to the end saw a half-built orb and nothing said otherwise. The kernel
already states the rule where the stages are built: *a strand count here is a
picture count, not a solid count*, which is §3.5's mandatory hedge. The sentence
now states both counts, says which is which, and gives the hidden count as the
subtraction so a reader can check it against what they can see.

### What actually changed, and why it is a refactor and not a patch

The prose moved into `packages/lab/src/breakdown-copy.ts`, a pure module. It had to,
to be checkable at all: `breakdown-main.ts` touches `document` at import and
calls `main()` at the bottom, so nothing in it was reachable from a test. **The
one part of the page a newcomer actually reads was the one part nothing could
assert on** — which is how a sentence contradicting the widget beside it shipped
and stayed. Nine tests now cover the census hedges the old code had no way to
exercise: no `weave` key, every loop facing the camera, and a census smaller
than the stage count.

Failing before and passing after, in both repos:

| where | before | after |
| --- | --- | --- |
| `timelapse-story.test.ts` (2 re-pinned) | fail with `COMPLETE_STYLE.silhouette = false` | pass |
| `breakdown-copy.test.ts` (3 of 9) | fail with the old sentence restored | pass |
| `timelapse_gate.py` on the shipped tree | 32 findings / 14 orbs | OK |
| `timelapse_gate.py --self-test` | 20 cases, 3 of them new | PASS |

**What this does not resolve:** T3 still checks the terminal frame alone. A
substitution that appeared on a *stage* frame would be caught by T6's fill and
marker rules rather than by a derivation, which is a weaker check — deliberately,
because a stage frame has no shipped counterpart to derive from.

**What would reverse this:** qiyas learning to ignore a marked silhouette, at
which point the instrument view could carry the limb itself and both halves of
the substitution collapse into a plain byte identity again.

---

## D-046 — the prints tab absorbs one event, and its gate ships with the first plate, not before

**Date:** 2026-08-28 · **Repos:** 3d-models (design only; no build target yet)
**Status:** design accepted; S1 + S3 shipped (gate before the first plate — see the 2026-08-30 amendment); S2/S4 pending a physical print, S5–S7 buildable now
**Design:** [`prints-tab-design.md`](prints-tab-design.md) ·
**Research:** [`research/prints-tab-survey.md`](research/prints-tab-survey.md)

The repository records renders, bets, and a queue, but not the one event a printer
lives by: a plate came off a machine and taught something. A "prints tab" was asked
for — per-model, per-version records with photos, a backlog, and feedback. The risk
in building it is not the recording; it is that a second scheduler or a second bet
registry grows inside it. The design draws the boundary so the tab **absorbs exactly
one unowned thing** — the print-run record — while it **presents** the queue
([`backlog.md`](backlog.md) §3.8), **consumes** the bets and protocol, and
**deletes** the one empty register that pretends to track prints today (the catalog's
32 Iteration-log tables, 0 rows — the D-041 rule, paid while it costs zero rows).

### The four blockers, and how each was settled

Four questions blocked the build. Two were the author's to settle from precedent,
two were the user's to decide:

1. **Record format — YAML frontmatter** (author). The `20-use-cases` hook already
   reads frontmatter records; a print record is the same shape with a prose body a
   JSON blob cannot carry.
2. **First run — Plate 1, the machine card** (author). It defines the nine-field
   profile header every later record inherits, and is the plate the most bets depend
   on.
3. **Photo cap — 2048 px / 2 MB** (user). Large enough to read a plate defect at
   100%, small enough that a repository of prints does not bloat the pack. Photos are
   source, tracked on master beside their record — the repo's first tracked
   non-generated binaries.
4. **Audience — gallery visitors too** (user). This moves the `prints.html` lab page
   (S7) from "maybe" into committed scope.

### Why the gate does not ship in this PR

The natural instinct is to ship `prints_gate.py` now. The design refuses: a gate
whose subject set is empty reports green and is indistinguishable from a broken gate
— the measured lesson of [`issue-register-evaluation.md`](issue-register-evaluation.md)
§5.1. So the gate ships in S3 **with** the first real record (S2), and R4 makes it
print the number of records it checked, so "all pass over zero records" can never
read as coverage. What shipped in this PR is exactly what is buildable without a
printer: the record format, this decision, the survey, and the forward-reference
baseline entries for the still-unwritten gate and page.

**Amendment 2026-08-30 — the gate ships before the first plate, and R4 is why.**
The reasoning above conflated two things and drew the sequencing wrong. "A gate over
an empty subject set reports a false green" is true of a gate that *hides* its subject
count; it is exactly *false* of a gate that prints it. R4 is not a mitigation to add
later — it is the property that makes wiring the gate at zero records **honest**, and
so the gate is buildable and correct the moment R4 is in it, no plate required. The
tenet, sharper than "measure before you gate": *a zero-subject gate is dishonest
unless it prints its subject count out loud; once it does, it can and should ship
before its subject exists — the empty run is then a true "0 records checked", not a
false pass.* S3 (`prints_gate.py` with R1/R2/R4, hook `39-prints`, `make
validate-prints`, and the `docs/prints/**` grounding-gate exclusion) shipped on this
amendment's date, ahead of the first plate. Only **R3** (two-way bet propagation)
stays deferred — it has a real empty-subject problem R4 cannot fix, because there is
no settled bet to propagate *from* yet; it lands in S4 with the first flip (task #71).
The prompt for the correction: the reprioritisation that found most of S3–S7
buildable without the printer, against the earlier claim that it was all printer-gated.

**What this does not resolve:** no plate has been printed, so no record exists and no
bet has moved. The printer-gated rungs — S2 (print Plate 1, task #67) and S4 (R3,
task #71) — wait on the bench; the printer is user-held (Bambu A1/P1S/X1C class). The
record-independent rungs (S5 catalog cleanup #68, S6 page #69, S7 lab page #70) do not.

---

## D-047 — round-pattern orb placement is a new statement family, and v1 proves the mechanism before it builds the table

**Date:** 2026-08-31 · **Repos:** bikar (`packages/core` engine, witnesses, e2e), 3d-models (this log + [`round-orb-placement-design.md`](round-orb-placement-design.md))
**Status:** v1 shipped (Phase 0 + Phase 1 green in bikar); rule table + fillers are follow-on

Two owner decisions (AskUserQuestion, 2026-08-31) set the shape of the feature that
finally reads the `place rule` socket the maclado work left declared and never
consumed. This entry records both, and the one subtle engine result they surfaced.

### The two decisions

1. **Scope — prove the mechanism first.** The request
   (`bikar:docs/design/round-pattern-orb-placement.md`) named the general capability:
   place *any* round `.bkr` at the site set of *any* rule, with fillers between discs.
   The owner scoped v1 to the two lowest rungs instead — place ONE hand-authored round
   disc on a sphere (watertight, Phase 0), and weld TWO adjacent copies so they share a
   real welded vertex (Phase 1). The general rule table (all sites per axis class),
   reproducing the 20-wheel maclado field through this path, a second (icosahedral
   5-fold) rule, and fillers are an explicit follow-on. *Why:* the four hard parts were
   already general and shipped (the frame-based placer, the coincidence weld, the
   solidify tail, the studio's `orbMesh`-without-`orb3d` dispatch); the only missing
   piece was small — the `place rule` word had exactly one read in the whole repo, a
   round-trip test. Proving the mechanism on two rungs is cheap and de-risks the table;
   building the table first would be scope the owner didn't ask for (Tenet 28's inverse —
   don't build the robust system the owner deferred).

2. **Surface — a new `base sphere` / `place rule` spelling.** The rejected alternative
   was to route round placement through `base wheelfield` (the maclado family). The owner
   chose a fresh statement family: `base sphere` reads round-disc placement as its own
   thing, and the maclado `wheelfield` path — including its dead `placeRule` socket — is
   left byte-untouched. *Why:* `base wheelfield` builds the kernel's *own* circular wheel
   and refuses `inscribe`; a user placing *their* disc is a different operation, and
   conflating them would overload one statement with two constructions. The new
   `SphereOrbNode` is a separate AST node, and `decl.placeRule` is finally read in
   `evaluateSphereOrbDecl`.

### The subtle engine result — watertightness is per cap, not aggregate

Two welded discs share their fused contact's vertical rim-wall edge (`out0 → inn0`
appears in both caps' rim walls — a "doubled wall"), so the aggregate edge-twin check
reports `watertight === false`. But each cap individually closes. The gate for a
multi-site placement is therefore `capsWatertight` (every cap's triangle-slice
individually watertight), which equals aggregate `watertight` for a lone cap. The
welded pair's union is a deliberate non-manifold pinch — fillers between discs are the
follow-on, and v1 proves the *weld* (a shared vertex index), not a printable union.
The frozen witness is `bikar:packages/core/tests/kernel3d/place-cap.test.ts`
(`weldCount === 1`, `capsWatertight === true`, aggregate `watertight === false`); the
browser-side companion is `bikar:packages/e2e/tests/round-orb.spec.ts` reading
`2 sites · 1 weld` off the studio overlay.

### What this does not resolve

The CLI `--check mesh` gate keys on `orb3d || piece3d` and silently skips the sphere-orb
`orbMesh` path (`round-orb-placement-design.md` §6). The watertight guarantee is real —
the evaluator throws at compile time — but the dedicated CLI mesh gate does not yet cover
this path. Closing it (a one-line predicate widen plus the aggregate-vs-caps report
decision) and an `engine-issues.md` entry are the follow-on's first task. The rule table,
the maclado-field reproduction (the strongest correctness test, it has a fixture), the
5-fold rule, fillers, and unifying `MacladoWheel` into the general contact-ring model all
stay deferred to the follow-on, each a named milestone in the design doc.

*Resolved 2026-09-02, the first item only:* bikar `adb4e8c` widened the gate onto a typed
`sphere3d` provenance, and measuring that widen against this decision's by-design case — the
welded pair, aggregate `watertight` false while every cap closes — found it **failing** the
welded orb and, through `make orbs`, this repo's build. bikar `8a01836` makes `meshGate`
read `capsWatertight ?? watertight`, the evaluator's own expression, and print both flags.
Record: `round-orb-placement-design.md` §6.1. The rest of this list stands.

## D-048 — direct commits on the default branch are refused by hook in both repos; merging on red is branch protection's to stop, and that setting is the owner's

**Date:** 2026-09-02 · **Repos:** bikar (`.husky/pre-commit`, bikar #136), 3d-models (`.githooks/pre-commit.d/00-branch`, this log)
**Status:** hooks shipped in both repos; branch protection **applied 2026-09-02** on the owner's go-ahead and verified by GET — [D-049](#d-049--six-owner-decisions-of-2026-09-02-in-plain-words) §1; the command below is the one that ran

### What was measured

Neither default branch is protected: `gh api repos/NaqshCoffee/bikar/branches/main/protection`
and `gh api repos/omars-lab/3d-models/branches/master/protection` both answer
`404 Branch not protected` (2026-09-02). Every norm here says branch → PR →
squash-merge, and nothing enforced it. Two consequences were observed the same day
while shipping the prints page (D-046's S7):

1. bikar's `ci` workflow was red on `main` for four consecutive runs, 2026-08-31 →
   09-02. bikar #121 added an SVG-rasterizer dependency that `ubuntu-latest` does not
   ship; #125, #128 and #129 merged over the red; bikar #131 added the install step
   and its `ci-parity.yaml` entry. Then bikar #132 introduced an identifier codespell
   reads as a misspelling and `main` was red again within the hour (#133, then the
   rename in #135). A red gate that everyone merges past is a gate that has been
   switched off — bikar's own `ci.yml` header says so.
2. A `git commit` on either default branch lands, and the next `git push` publishes
   it. In bikar that is a commit no pull-request run ever measured; here it is a
   commit no hook-parity run on a second machine ever saw.

### The decision

Two failure paths, two mechanisms, and only one of them is ours to ship from a repo:

- **The direct-commit path is closed by hook, in both repos, now.** 3d-models
  `.githooks/pre-commit.d/00-branch` and the first block of bikar `.husky/pre-commit`
  refuse a commit whose branch is `master` or `main` — both names in both repos, so
  the rule reads the same in each. Detached HEAD is allowed (no branch to protect;
  `git worktree add --detach` is how both repos' hook tests build their fixtures)
  and so is `gh-pages` (a deliberately diverged branch `make deploy` commits to; it
  is not the default). The override is `BRANCH_OK=1`, the `*_OK=1` convention every
  other gate here uses, so choosing to skip it leaves a name in the shell history.

  **Validator:** `make validate-branch-guard` here (`.githooks/tests/refuse-main-commit.sh`,
  the hook's declared wholesale form) and `npm run test:hooks` in bikar, both driving
  *git* through the wired hook rather than running the file by hand.
  - PASS: a commit on `feat/topic`, on `gh-pages`, on a detached HEAD, and on
    `master` with `BRANCH_OK=1` all land.
  - FAIL: a commit on `master` or `main` is refused **with the guard's own message**.
    A refusal for any other reason (a scratch repo with no `scripts/`, say) is
    counted as the guard *not* having run — the vacuous pass the test exists to catch.

- **The merge-on-red path is not closable from inside a repo.** A hook runs on the
  committer's machine; a squash-merge happens on GitHub. Only branch protection with
  required status checks stops a merge on red, and applying it is an account-level
  change with a rule pulling the other way: a billing block is not a red build and
  must never stop a merge or a deploy (CLAUDE.md, `docs/local-ci-runbook.md`). Required
  checks that fail-closed during a billing outage would block every merge for as long
  as the outage lasts.

  So the setting is recorded here as the recommendation, and applied by the owner,
  not by a session:

  - **bikar `main`**: require a pull request; require the `ci`, `e2e` and `gitleaks`
    checks; **do not enforce for admins**, so the owner can still merge past a
    billing block while a red check on an ordinary day stops everyone else.
  - **3d-models `master`**: require a pull request only. There is no CI to require.

  ```sh
  gh api -X PUT repos/NaqshCoffee/bikar/branches/main/protection --input - <<'JSON'
  {"required_status_checks":{"strict":false,"contexts":["ci","e2e","gitleaks"]},
   "enforce_admins":false,
   "required_pull_request_reviews":{"required_approving_review_count":0},
   "restrictions":null}
  JSON
  gh api -X PUT repos/omars-lab/3d-models/branches/master/protection --input - <<'JSON'
  {"required_status_checks":null,"enforce_admins":false,
   "required_pull_request_reviews":{"required_approving_review_count":0},
   "restrictions":null}
  JSON
  ```

  Until that ran (it did, 2026-09-02 — D-049 §1), the hook was the whole gate on direct
  commits and *nothing* gated a merge on red. The standing practice stays: to read `main`'s last run before diagnosing
  a PR's red check (memory `check-main-ci-not-just-the-pr`) and to poll `gh pr checks`
  to all-pass before `gh pr merge`, never `--auto`.

### What this does not decide

Whether `strict: true` (branch must be up to date before merging) is worth the rebase
churn with several sessions merging in a day — left off here; it is the setting that
would have caught #132's codespell failure before merge, at the price of a re-run per
merge. Revisit if `main` goes red a third time from a merge that was green on its own
base.

## D-049 — six owner decisions of 2026-09-02, in plain words

**Date:** 2026-09-02 · **Repos:** both · **Status:** all six decided; §1 is applied and verified and §3 is shipped (sacred-patterns #44 `a89f45a`); §2 and §4–§6 are queued as `docs/plan.md` §2 rows 2.10–2.14 with the shape chosen here

### Why this entry exists

Six items were waiting on the owner, not on code: the branch-protection setting D-048
left to the owner, and five task-board items the 2026-09-01 audit had marked as needing
a decision (the fourth orb, the decision hub, the status page, the parked Rosette-N
explorations, the wrap morph). Each was put to the owner as one question with its
options spelled out plainly and the recommended one listed first. The answers are
below, one section per question: the question, the options as offered, the answer,
and what changes because of it. Task numbers appear only to say where a question came
from; the durable name of each item is its plan row and this entry.

### 1. Branch protection — "apply it now on both repos, or leave it as a recommendation?"

*Options offered:* apply on both repos now (recommended) · apply on bikar only, where
there is CI to require · leave D-048's recommendation unapplied.
*Answer:* **apply on both now.**

Applied 2026-09-02 with the two commands in D-048, unchanged, and read back:

| Repo, branch | Required checks | Up-to-date required | Enforced for admins | Approving reviews |
|---|---|---|---|---|
| bikar `main` | `ci`, `e2e`, `gitleaks` | no | no | none required |
| 3d-models `master` | none (there is no CI) | — | no | none required |

In plain terms: a change to bikar's main now needs a pull request whose three checks are
green; a change to master here needs a pull request. The owner, as admin, can still
merge past a billing block, which is the case CLAUDE.md says must never stop a merge.
Every norm in this repo already said branch → PR → merge; what changed is that GitHub
now refuses the other path, and the hooks from D-048 refuse the commit before it gets
that far. The first PRs merged under the setting were bikar #138 and #139 and 3d-models
#135, all polled to green first.

**Validator:** `gh api repos/<owner>/<repo>/branches/<default>/protection` for each repo,
read as data, not as a screenshot.
- PASS: bikar answers with exactly the three contexts above and 3d-models answers with
  no required checks; both answer `enforce_admins.enabled: false`.
- FAIL: either answers `404 Branch not protected` (the state D-048 measured), or bikar's
  contexts list lacks one of the three — a merge on red is then possible again and this
  entry's status line is wrong.

### 2. The wrap morph — "build it straight away, or design it first?"

*Options offered:* write a grounded design doc first, then build (recommended) · build
directly from the plan's three-line sketch · drop it, the endpoints and the tilt-in are
enough.
*Answer:* **design doc first, then build.**

The morph is the beat the breakdown page exists for — the flat drawing visibly
wrapping onto the sphere — and it was deliberately left out of v1 of
[`orb-construction-timelapse-design.md`](orb-construction-timelapse-design.md) because
nothing in bikar's core interpolates geometry; the flat and sphere endpoints were shipped
instead. So the doc has to establish, before code, three things a build would otherwise
guess at: how each vertex travels from the face-lift plane to the sphere as a function of
one parameter; that the morph frames keep the same viewBox and stay unstyled, so the
timelapse gate's junction identities still hold at both ends; and what the woven family,
which has no face lift, shows in that slot. Research goes in `docs/research/` under the
provenance header, per the design-doc rules. Then one bikar PR and one 3d-models PR,
never stacked.

### 3. The decision hub — "how does this repo's decision log join bikar's?"

*Options offered:* index only, generated by bikar's ledger script from this file's
headings, with links and no copying (recommended) · copy each decision into bikar's
`docs/decisions/` tree · leave the two logs unjoined.
*Answer:* **index only, generated.**

Each decision keeps one home. bikar's ledger script reads the `## D-0xx —` headings of
this file and emits an index of links; nothing is transcribed, so nothing can drift
between two copies. This is the same answer D-004 gave when it refused to mirror
bikar's generator, now with the join added. It also settles what the cross-repo ledger
check should block on, which was the open question in front of it: a D-number cited
across repos that does not exist as a heading in this file, or as a file in bikar's
tree, is a broken reference and blocks — the same rule the pointer gate already applies
to paths.

**Shipped 2026-09-02** (sacred-patterns #44 `a89f45a`). One correction the build made to the sentence above: the cross-repo hub is **sacred-patterns'** cross-repo ledger generator, not bikar's within-repo one — the per-repo `LEDGER.md` scripts are each repo's own, but the roll-up that joins all four already lived in sacred-patterns, so that is where the 3d-models index and the citation gate landed. bikar's pre-commit invokes it as a non-blocking NOTE; the block itself fires in sacred-patterns' own pre-commit and in its `make local.ci`. What shipped: a links-only *3d-models decisions — index* section generated from this file's headings at its origin ref, and a corpus-wide citation check that refuses (write) or blocks (`--check`) on a `D-0xx` cited in any of the four repos that resolves to neither a heading here nor a file in bikar's decisions tree. 20 test assertions, two of them regression witnesses this build earned: the citation scan excludes the suite's own fixtures, and the suite unsets the git-hook env vars so its scaffolds stay hermetic when run from a hook.

### 4. The studio status page — "what should it show?"

*Options offered:* pins and versions only, read from files (recommended) · pins plus a
shipped/preview state per surface · a full dashboard with build health.
*Answer:* **pins and versions.**

The page shows three facts and types none of them: the bikar commit the gallery was
built from (`build/bikar-ref.txt`), the `as_of` pins the use-cases map was last checked
against, and the last deploy. It is rendered the way the studio index already is —
from data the repos hold, with a test that holds it to the filesystem — so it cannot
say something the files do not. Anything beyond that is a later decision, and the
"shipped/preview per surface" option is the first candidate if the three facts turn
out not to be what a visitor asks.

### 5. The fourth orb — "build one on the M4c walk, or call the family done at three?"

*Options offered:* build a fourth orb on the M4c quantized lattice walk (D-031 proved
the walk gives few tile classes but shipped no orb) · done at three presets · defer
until after a print.
*Answer, in the owner's words:* **build a fourth orb, and use the build to find gaps and
inconsistencies and make the approach more robust in the process — and: "do we also
need an orb creation skill?"**

The skill question has a precedent in this repo, and the precedent decides it. Two
earlier proposals for a skill — one to extend the DSL, one for an issue register — were
each evaluated against measured recurrence and both ended the same way: *no skill, a
gate instead*, because the thing that was missing was a detector, not more instructions
([`dsl-extension-skill-evaluation.md`](dsl-extension-skill-evaluation.md) §3,
[`issue-register-evaluation.md`](issue-register-evaluation.md) §6). Three orbs have been
built without an orb skill, so no recurrence has been measured yet. The fourth build is
the measurement, and this is the rule it runs under:

Every time the build stops for something an earlier orb build also needed, the stop is
written into the build's design doc with one of two labels: **detector** — a test, gate
or generated file could have caught or produced it — or **instruction** — only a person
who had built an orb before could have known it. Detector items become gates or tests in
the same PR that hits them. An orb skill is written only if the instruction list is
non-empty when the orb ships, and it is then a checklist that points at those entries
and nothing else.

**Validator:** the fourth orb's design doc carries the stop list with every entry
labelled.
- PASS: the orb ships with each stop labelled and each detector item pointing at the
  gate or test it became; the skill exists if and only if the instruction list has
  entries.
- FAIL: a skill proposed before the list exists, or with an empty instruction list, or
  a detector item that became a paragraph in the skill instead of a check — that is the
  precedent's "a fourth thing to go stale", and the skill evaluation's verdict applies
  unchanged.

### 6. The parked Rosette-N explorations — "what happens to the three stashes?"

*Options offered:* record the three value-triples as a sweep table on a pushed branch,
then drop the stashes (recommended) · keep the stashes where they are · promote one
triple to the pattern's defaults now.
*Answer:* **record as a sweep table, then drop.**

Read on 2026-09-02 from the bikar checkout, without applying anything. The committed
pattern has points 10 (range 5–16), crossover 18 (10–50) and petal reach 0.53 (0.2–0.8).
The task text said the working tree held points 7; the diff says 5, and the diff is what
is recorded:

| Where it sits | points | crossover | petal reach | Note |
|---|---|---|---|---|
| committed `patterns/Rosettes/Rosette-N.bkr` | 10 | 18 | 0.53 | the defaults |
| stash@{0} "v3", 2026-08-31 | 5 | 18 | 0.53 | one knob: fewest petals the range allows |
| stash@{1} "v2", 2026-08-31 | 10 | 38 | 0.54 | crossover far past default; reach barely moved |
| working tree, uncommitted | 5 | 37 | 0.44 | both at once, reach pulled in |

The note column reads the values; the session that parked them wrote no intent down, so
none is claimed here. Both stashes also carry the same one-line edit to
`patterns/.folders.json` filing Rosette-N under Rosettes. What happens: the table goes
beside the pattern in bikar on a branch merged by PR; the folder edit goes with it if
the file still lacks the entry; the two stashes are dropped and the working-tree edit
reverted **only after** that PR is on origin, because a stash is local to one clone and
is lost with it. Which triple, if any, becomes the pattern's defaults stays the owner's
call — the table exists so that call can be made from a record instead of from memory.

### What this does not decide

The morph's geometry (the design doc's job); where the status page lives in the studio
(the page's own catalogue entry decides); and whether a fourth orb changes the
family's default preset. None of the six needed a source outside the two repos, which
is why this entry cites decisions and files rather than research.

## D-050 — the three d3 surfaces converge on one face-list vocabulary; the reversal condition is a measured re-divergence cost, not a taste change

**Date:** 2026-09-02 · **Repos:** bikar + sacred-patterns (recorded here) · **Status:** shipped — A↔B rename bikar #151 `1083046`; grow-C sacred-patterns #45 `76e3c17`; design [`vocabulary-convergence-design.md`](vocabulary-convergence-design.md)

### Why this entry exists

Q-VOCAB asked whether sacred-patterns' geometry/draw vocabulary should be shared with
the two d3 explorers or left a separate gallery. The owner chose, in their words, **"full
convergence, refactor C"** — the deepest of the three options: not only rename the A/B
collisions but grow sacred-patterns the face-list + data-join structure so its vocabulary
attaches to real code, not just matching labels. This entry records that decision, the one
correction the build made to the design, and the condition under which it would be undone.

### The decision, as offered and answered

*Options offered:* do nothing, keep C a separate dialect (rejected — forks the vocabulary
the d3 stream exists to unify) · thin A↔B rename only (adopted as step one, not the whole
job) · **full convergence, refactor C (chosen)**. *Answer:* **full convergence.** It is the
robust-over-cheap call (`3d-models/CLAUDE.md`): the deeper refactor deletes the divergence
rather than routing around it, and it is the only option under which all three surfaces read
one vocabulary — `index` (face identity), `polygon` (boundary), `ring` (concentric styling
index only), `faceKey` (the shared join key `String(index)`), `joinFaces` (A's path-creating
join).

### What shipped, and the K7 the build caught

The design's §2 and §6 (validator #2) said B should "route through `joinFaces()`" and carry
no private `.data().join()`. The build proved that wrong and the doc was corrected in the same
PR that records this: the orb-instrument page **keeps its own `.data().join()` by design** — it
binds `FaceStatus` onto the pre-rendered `<path data-face-index>` nodes and asserts enter and
exit are both empty, which the path-*creating* `joinFaces()` cannot do. What actually converges
the two joins is the shared **`faceKey`** (`viz-d3.ts`: "shared by every face join — the
path-creating `joinFaces` here and the status-binding join on the orb-instrument stage"). So the
canonical vocabulary gained `faceKey` as a fifth term, and the join convergence is *the key, not
the call*. sacred-patterns' side is a pure structural addition (`faceConstructs()` mapper +
`joinFaces()` `<path class="face">` renderer replacing imperative `<polyline>`), held
pixel-identical by a frozen coordinate golden — the `ring` field stays undefined there by the
§9 K10 transfer condition (its faces come only from polygons/stars, never circles).

### Reversal condition

This was decided by tests, not by a printer — no `CAL-*` bet. It reverses only if a **fourth
surface** arrives whose faces cannot be expressed as `{index, polygon, centroid, ring?}` without
adding producer-less bag fields (Tenet 15) — a curved, streaming, or non-face geometry — **or**
if maintaining the pixel-identical golden across the face-list seam starts costing more than the
one-vocabulary benefit returns. Either is a measured cost, re-litigated against this entry; a
mere preference for different names is not a reversal condition and does not reopen it.

**Validator:** the shared vocabulary is one definition with callers, not parallel copies.
- PASS: `faceKey` has a single definition in `bikar:packages/web/src/viz-d3.ts` and is imported
  by both the rosette explorer and the orb-instrument page; `faceIndex` and any boundary-holding
  `ring` field appear nowhere in bikar web sources; sacred-patterns' `sacred-patterns/test/regression/check.js`
  passes with the same boundary count and sorted coordinate set as the pre-refactor baseline.
- FAIL: either surface hard-codes its own key expression so two surfaces could key the same face
  differently; or `SvgFace` still carries a `ring` holding a point array while `FaceConstruct.ring`
  is a number (the two-meanings collision, merely split across files); or a sacred-patterns face's
  coordinate string differs from the frozen golden — the refactor changed a pixel, which is a
  regression, not a convergence.
