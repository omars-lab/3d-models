# 3d-models

Product end of a three-repo system. **bikar** (`~/Workspace/git/bikar`) is the
DSL + geometry engine and the producer of record. **qiyas**
(`~/Workspace/git/qiyas`) validates renders. This repo holds OpenSCAD sources,
design docs, the gallery, and the gh-pages deploy — it consumes bikar, it does
not reimplement it.

## Mechanics

- **Node**: prefix every `git`/`npm`/`tsx`/`vitest` invocation with
  `export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"`. The system Node
  is too old and fails in ways that look like code bugs.
- **Hooks**: `core.hooksPath = .githooks` (run `make setup-hooks` once per
  clone). `pre-commit.d/10-gitleaks` scans for secrets; `20-use-cases` **blocks**
  a commit that stages a file the use-case map pins. Fix with
  `python3 .claude/skills/maintain-use-cases/validate.py --refresh`; override
  with `USE_CASES_OK=1` only when you know why.
- **Build**: `make orbs` (bikar CLI → STL + views), `make cookie-cutters`,
  `make deploy` (gh-pages worktree). `gh-pages` is a deliberately diverged
  branch — never merge it into `master`.
- **Skills**: `ground-design-doc` (audit a doc's sources), `calibrate` (turn
  UNGROUNDED-and-empirical into a `CAL-*` bet), `prototype` (physical print
  pack), `maintain-use-cases`.

---

## Design-doc rules

Seven adversarial grounding audits of seven design docs written here produced
~104 findings. Four failure kinds recur, are preventable by knowing about them,
and are *not* caught by any gate. Definitions, per-kind instance counts, and
`file:line` anchors: [`docs/grounding-defect-taxonomy.md`](docs/grounding-defect-taxonomy.md).

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
- **K6 → D2.** State a validator as `**Validator:** …` and follow it, in the
  same section, with a `PASS:` line and a `FAIL:` line. Every K6 instance in
  the corpus was found by an auditor hand-constructing the counterexample the
  doc never wrote: `c2-assembly`'s ±0.05 fit windows overlap at gap 0.10;
  `lego-lab`'s grid-fit formula scores a hexagonal lattice 1.0 while the doc's
  own table says it cannot; `tile-wall`'s anchor validator "will essentially
  never fire."
- **K9 → D1.** Every relative link must resolve on disk. This one is universal
  and needs no marker.
- **K9 → the pointer gate.** A backticked path is a claim too, and
  `.claude/gates/doc_pointers.py` (hook `35-doc-pointers`, `make
  validate-pointers`) holds it to this repo, to a sibling **at a git ref** — not
  at whatever someone else has checked out — or to a reasoned entry in
  `.claude/gates/doc-pointer-baseline.json`. The baseline is a ratchet: it may
  shrink freely and only grows deliberately. Cite a third party's tree, name a
  file still to be authored, or propose a module, and you belong in it; be
  stale and you do not.
- **A knob a coupon prescribes is a claim too.** Every `--param`, `--piece` and
  `--brick-fit` in `.claude/skills/prototype/catalog.md` must name something the
  entry's `.bkr` declares — `.claude/gates/catalog_models.py`, hook
  `36-catalog-models`, `make validate-catalog`. Two instances built it: W-F1's
  model file that never existed under the name given, and LG-F1's `--param
  rib_mm`, "a knob that never existed". The DSL's declaration keywords and the
  `BrickFit` field set are **harvested from bikar**, not listed — a hand-written
  list omitted `clip` and turned two correct entries into findings on the first
  run.

### Research is checked in

`ground-design-doc` requires it: the research behind a doc lives in
`docs/research/*.md` under a provenance header (date, produced-by, which doc it
feeds), preserved verbatim — not only in a transcript. A doc that points at a
research file the repo does not have is a **K9**; that shipped in
`hemisphere-split-design.md` and again here on 2026-07-29, which is why D1
exists.

---

## The graduation rule

When a defect is found and fixed:

1. **Always** write the test or the doc correction that fails before the fix
   and passes after. This is the whole obligation in the normal case.
2. **Only** write a durable narrative record when the fix also produces a
   *tenet* — a rule that changes how the next doc gets written. Then it goes in
   this file, or in the taxonomy, not in a register.

There is deliberately **no issue catalog** in this repo. The measurement behind
that decision is in
[`docs/issue-register-evaluation.md`](docs/issue-register-evaluation.md): of 15
defects traced through git history, 5 graduated into a guard; all 7 fixes in
July 2026 shipped a test and none needed an entry. Registers that nobody
re-reads decay into what Richard Cook calls "a defensible argument that
management is occurring." A test protects behaviour at zero re-reading cost.

There is also no automated link checker: an 8.4% sample of the repo's 737 URLs
measured ~11% false alarms against a true dead-link rate under 1%, and *"a gate
that cries wolf gets switched off, which is worse than having no gate."*
The checkable invariant is not *does this URL resolve* but *is every
load-bearing number attributed to a source the research file records as
actually fetched* — a local check with no network.

## Precedent

Before proposing a new skill or hook, read
[`docs/dsl-extension-skill-evaluation.md`](docs/dsl-extension-skill-evaluation.md)
and [`docs/issue-register-evaluation.md`](docs/issue-register-evaluation.md).
Both evaluated a proposed skill against measured recurrence and both concluded
*no skill, a gate instead*. Anthropic's own guidance on this file applies to
this file: bloat makes it ignored — keep it under 200 lines, and prefer
deleting a rule or converting it to a hook over adding prose.
