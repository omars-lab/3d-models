# 3d-models

Product end of a three-repo system. **bikar** (`~/Workspace/git/bikar`) is the DSL
+ geometry engine and the producer of record; **qiyas** (`~/Workspace/git/qiyas`)
validates renders. This repo holds OpenSCAD sources, design docs, the gallery and
the gh-pages deploy — it consumes bikar, it does not reimplement it.

## Mechanics

- **Node**: prefix every `git`/`npm`/`tsx`/`vitest` invocation with
  `export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"`. The system Node
  is too old and fails in ways that look like code bugs.
- **Hooks**: `core.hooksPath = .githooks` (`make setup-hooks` once per clone);
  each sees only staged files, and `make validate` runs all of them over the
  whole tree. `00-branch` refuses a commit on master (`BRANCH_OK=1` overrides).
  `20-use-cases` **blocks** a commit staging a file the map pins (`USE_CASES_OK=1`
  overrides): `validate.py --refresh` re-pins hashes and *reports* moved anchors.
- **Build**: `make orbs` (bikar CLI → STL + views), `make cookie-cutters`,
  `make deploy` (gh-pages worktree). `gh-pages` is a deliberately diverged
  branch — never merge it into `master`.
- **CI**: there is none — no workflows, so `make validate` (alias `make local.ci`,
  the siblings' spelling) is the only run there is and `make deploy` needs no
  runner. A billing block is not a red build (`gh run view <id> --json jobs` →
  `"steps": []` in 2–3 s: nothing measured) and must never stop a merge or a deploy
  — [`docs/local-ci-runbook.md`](docs/local-ci-runbook.md).
- **Skills**: `ground-design-doc` (audit a doc's sources), `calibrate`
  (UNGROUNDED-and-empirical → a `CAL-*` bet), `prototype`, `maintain-use-cases`.

---

## Design-doc rules

Seven adversarial grounding audits of seven design docs here produced ~104
findings. Four failure kinds recur, are preventable by knowing about them, and are
*not* caught by any gate. Definitions, counts and `file:line` anchors:
[`docs/grounding-defect-taxonomy.md`](docs/grounding-defect-taxonomy.md).

### K1 — Do not strip a qualifier (7/7 audits)

Carry the source's hedge into the claim. Also carry **our own survey's** hedge:
a survey that says a risk "may be fatal, or may be resolvable" must not become
a doc that says "ruled out."

> *Failure mode:* `hemisphere-split` §3.2 hardened its own survey's open
> question into a ruling. `c2-assembly` §3 turned "slicers drop imported
> objects **by default, unless the user opts into the multipart workflow**"
> into an unconditional "all drop them."

### K2 — Do not assert exhaustiveness over a space you did not search (7/7)

"No system does X", "every surveyed ecosystem does Y", "all six presets" —
each is a claim about a set. Either enumerate the set in the doc, or write
"none of the N systems surveyed here."

> *Failure mode:* `piece-composition` claimed "every surveyed ecosystem
> conflates" a distinction that BOSL2's `screws.scad` separates — a library
> *inside* the surveyed set. `hemisphere-split` §1.1 said "all six presets"
> when nine ship, and the ninth (Custom) breaks the conclusion.

### K7 — Read the doc against itself before shipping it (4/7)

A contradiction between two sections needs no source to find and no research to
fix. Check: does every worked example satisfy the doc's own formula? Can the
flagship example be built by the machinery the doc ships? Does the status line
agree with the appendix?

> *Failure mode:* `tile-wall` §4 called the engaged clip "unstressed" while
> requiring it to pull bowed tiles flush. `piece-composition` §4.1's headline
> `hole grub radial` is classified out of scope by the same doc's §8.
> `hemisphere-split`'s status line claimed an audit that did not exist while
> Appendix B said "pending."

### K10 — State the transfer conditions when porting a rule (6/7)

A constant, rule or convention established under one process, material or
domain does not automatically carry to another. Write the sentence that says
what must hold: *"this transfers because …"* — and if you cannot write it, the
rule does not transfer.

> *Failure mode:* `tile-wall` ported a rigid-run rule from sun-exposed,
> tightly-interlocked garage floors to indoor decor with open 1.2 mm gaps.
> `print-validation` used Cura's from-vertical `h·tanθ` without saying so;
> PrusaSlicer measures from horizontal and uses `h/tanθ`, and they agree only
> at the 45° default — "a silent porting hazard." `lego-lab` reused a 0.2 mm
> inter-part **moulding relief** as a pattern-registration tolerance.

### Related, and enforced rather than remembered

`.claude/gates/docs_gate.py` runs on staged markdown via
`.githooks/pre-commit.d/30-docs-gate`, and on the whole tree via
`make validate-docs`. Write the marker and the gate checks the rest.

- **K4 → D3.** State a default with the `**Default:**` marker, followed by the
  value and then either a citation link or a `CAL-*` bet id in the same
  paragraph. Nothing else counts. If no source can settle the number, that is
  exactly what `calibrate` is for; a bet id is a legitimate answer and a bare
  number is not.
- **K6 → D2.** State a validator as `**Validator:** …` and follow it, in the same
  section, with a `PASS:` line and a `FAIL:` line. Every K6 instance was found by an
  auditor hand-constructing the counterexample the doc never wrote: `c2-assembly`'s
  ±0.05 fit windows overlap at gap 0.10; `lego-lab`'s grid-fit formula scores a
  hexagonal lattice 1.0 while its own table says it cannot; `tile-wall`'s anchor
  validator "will essentially never fire." The gate cannot check that your `FAIL:`
  is the *hard* case, and one substitution keeps passing it: **an aggregate cannot
  discharge a claim about every part.** `lego-lab` §14 certified every triangle CCW
  and measured one signed volume — one reversed triangle in 3,764 leaves it positive.
- **K9 → D1.** Every relative link must resolve on disk; universal, no marker.
- **K1 → D4. A withdrawal is corpus-wide, not a local edit.** When an audit kills a
  number, grep every doc before calling it fixed and add the literal to `WITHDRAWN`
  in `docs_gate.py`. `±0.1–0.2 mm printer accuracy` died 2026-07-29, was rebuilt in
  two docs, and stood five more days in `tile-wall` under "the load-bearing facts".
  D4 catches literals only — §2's "10–20× beyond FDM tolerance" escaped it.
- **K9 → the pointer gate.** A backticked path is a claim too, and
  `.claude/gates/doc_pointers.py` (hook `35-doc-pointers`) holds it to this repo,
  to a sibling **at a git ref** — not whatever someone else has checked out — or
  to a reasoned entry in `doc-pointer-baseline.json`, a ratchet that shrinks freely
  and grows only deliberately. An unwritten file belongs in it; stale does not.
- **A knob a coupon prescribes is a claim too.** Every `--param`, `--piece` and
  `--brick-fit` in `.claude/skills/prototype/catalog.md` must name something the
  entry's `.bkr` declares — `catalog_models.py`, hook `36-catalog-models`. Built by
  W-F1's missing model file and LG-F1's `--param rib_mm`. Declaration keywords and
  `BrickFit` fields are **harvested from bikar**, not listed: a listed set omitted
  `clip` and made findings of two correct entries.
- **Ground a claim in a link the hook re-checks against the diff.** A line number is a
  claim; the anchor grounds it. Write `` `3d-models:Makefile:L283 "orbs:"` `` — repo,
  path, line, literal — in *any* markdown here; `validate.py` scans the whole tree, reads
  each at the pinned commit, and when an edit moves the target it names where it went, so
  the reminder *is* the repair. Only `` `repo:path:L137` `` is exempt. Unanchored, **23 of
  44** drifted; scanning only the map let an `L99999` pointer pass three gates at exit 0.
- **A count is a claim too, and a number a tool can print is not typed.**
  `<!--count:NAME-->` pins a number to the tool that prints it (`counts_gate.py`,
  hook `37-counts`). Tag-presence is checked (C3) only in the form that measured
  **9 hits, 9 real**, not the 60-char window's 117 at ~4%: **measure a rule before
  gating on it**, and read across the wrap — two stale numbers were words. **Nor is
  the list beside the number:** the quantity §8 exempted to avoid "owning it twice"
  was wrong at 2 of its 3 sites while all 24 marked ones were right, and 16 of those
  24 sit next to the ids they count — so C4 checks the list, since rewriting the
  digit alone turns a blocking failure into a silent K2. [D-020](docs/decisions-log.md)

### Research is checked in

`ground-design-doc` requires it: research lives in `docs/research/*.md` under a
provenance header (date, produced-by, which doc it feeds), preserved verbatim, not
only in a transcript. A doc pointing at a research file the repo does not have is
a **K9** — it shipped twice, which is why D1 exists.

---

## The graduation rule

When a defect is found and fixed, **always** write the test or the doc correction
that fails before the fix and passes after — that is the whole obligation in the
normal case. **Only** write a durable narrative record when the fix also produces
a *tenet*, a rule that changes how the next doc gets written; then it goes in this
file, or in the taxonomy, not in a register.

There is deliberately **no issue catalog** here and no automated link checker —
both rejected on measurement in
[`docs/issue-register-evaluation.md`](docs/issue-register-evaluation.md). Of 15
defects traced through git history 5 graduated into a guard, and all 7 fixes in
July 2026 shipped a test and needed no entry: registers nobody re-reads decay
into what Richard Cook calls "a defensible argument that management is
occurring." §5.1 measured ~11% false alarms against a true dead-link rate under
1% — *"a gate that cries wolf gets switched off, which is worse than having no
gate."* The checkable invariant is not *does this URL resolve* but *is every
load-bearing number attributed to a source the research file records as actually
fetched* — local, no network.

## Robustness over ease — especially when offering the choice

Ease is visible at the moment of choosing and robustness is not, so the trade is
systematically mis-priced unless written down. When you present options, the
cheapest is not the default, "do nothing" is not neutral, and each must say **what
it verifies** — one that verifies nothing should be named as such or not offered.

> *Failure mode, 2026-08-03:* both options offered for the machine card produced 23
> STLs and **neither checked one**, while `calibration-design.md` §7 already shipped
> a 23-row expectation table. What shipped diffs the mesh gate against that table
> ([D-014](docs/decisions-log.md)) — a verifier with a build target as its front
> door, not the §6 re-typing the backlog framed it as.

Corollary: **the by-design failure is the load-bearing case.** A gate that
asserts "everything passes" must be wrong about a deliberate failure or skip
it, and skipping is how a gate stops testing the thing it exists for.

Corollary: **robust and simple beat cheap and easy, even at more work.** The cheap
fix routes around the defect; the robust one deletes it. Two code paths that disagree
— or one name with two meanings — *are* the defect: remove it rather than hide it,
price the cascade, and pay it. A migration never buys a fork — [D-041](docs/decisions-log.md), [D-052](docs/decisions-log.md).

## Precedent

Before proposing a new skill or hook, read
[`docs/dsl-extension-skill-evaluation.md`](docs/dsl-extension-skill-evaluation.md)
and [`docs/issue-register-evaluation.md`](docs/issue-register-evaluation.md): both
evaluated a proposed skill against measured recurrence and both concluded *no
skill, a gate instead*. Anthropic's own guidance on this file applies to this
file — bloat makes it ignored, so keep it under 200 lines and prefer deleting a
rule or converting it to a hook over adding prose.
