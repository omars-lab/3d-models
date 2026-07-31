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
