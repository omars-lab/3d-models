# The grounding-defect taxonomy (K1–K12)

**Status:** derived 2026-07-30 from the seven adversarial grounding audits in
`docs/research/*-grounding-audit.md`. This file is the definition of record for
the `K*` kind ids used in `docs/issue-register-evaluation.md`.

---

## 0. Why this file exists — the defect it fixes

`docs/issue-register-evaluation.md` §5 publishes a taxonomy table with nine
rows: K1–K6, K8, K11, K12. Its prose then reasons about **K7 and K10**
("A checklist would plausibly have caught K1, K10, K7 and the framing half of
K2"), and §6 item 1 proposes carrying "the four prompt-preventable audit kinds
(K1, K2-framing, K7, K10)" into a `CLAUDE.md`.

K7, K9 and K10 are defined nowhere. `grep -rn "K7\|K9\|K10" docs/ .claude/`
returns only the two lines that *use* them.

That is a **K9** by this file's own definition — a reference that resolves to
nothing — sitting inside the document that classifies K9. It is also the
smaller half of a **K2**: a taxonomy asserted as complete while a third of its
range was never published. Two of the five changes §6 asks for are scoped by
kinds the reader could not look up.

The fix is not to invent three definitions that sound right. It is to re-derive
the whole taxonomy from the corpus, publish it with the instances it rests on,
and repoint §5/§6 here. That is what follows.

---

## 1. Corpus and method

| Audit | Lines | Design doc audited |
|---|---|---|
| `c2-assembly-grounding-audit.md` | 131 | C2 assembly |
| `hemisphere-split-grounding-audit.md` | 284 | hemisphere split |
| `lego-lab-grounding-audit.md` | 345 | Lego Lab |
| `piece-composition-grounding-audit.md` | 126 | piece composition |
| `print-validation-grounding-audit.md` | 118 | print validation |
| `tile-wall-grounding-audit.md` | 151 | tile walls |
| `w2-connector-grounding-audit.md` | 154 | W2 connector |

Seven audits, ~104 findings, 1 309 lines. Each was produced by an adversarial
agent under `.claude/skills/ground-design-doc` against a design doc written in
the same repo by the same author, and each is preserved verbatim under a
provenance header.

**Counting rule.** The `Audits` column below is *the number of audits in which
at least one instance can be pointed at*, not a count of instances. It is a
presence measure, deliberately: instance counts depend on how finely a finding
is split, presence does not. Every kind's row is backed by the cited
`file:line` anchors in §2, so the count is checkable.

**Provenance of the counts.** K7, K9 and K10 were counted in this pass. K1–K6,
K8, K11 and K12 carry the counts from the original classification pass recorded
in `issue-register-evaluation.md` §5; that pass was judgment-based and its
limits are disclosed in that document's §7. The two passes share an author and
therefore share that correlation.

---

## 2. The taxonomy

| Kind | Definition | Audits | Preventable by |
|---|---|---|---|
| **K1** | A qualifier present in the source (or in our own survey) is dropped between it and the claim | 7/7 | **prompt** |
| **K2** | Exhaustiveness asserted over a space that was never searched | 7/7 | **prompt** for the framing, **measurement** for the search |
| **K3** | The citation does not contain the claim it is attached to | 7/7 | mechanical half **gate**, semantic half **measurement only** |
| **K4** | A number is presented as fact with no source, and defaults are then keyed to it | 7/7 | **gate** |
| **K5** | The measurement was taken on the wrong object | 6/7 | mostly **measurement** |
| **K6** | A validator is specified against the wrong acceptance region | 7/7 | **gate** |
| **K7** | **Internal contradiction: two parts of the same document cannot both be true** | 4/7 | **prompt** (self-consistency read) |
| **K8** | Semantic meaning assumed for an incidental artifact | 4/7 | **measurement only** |
| **K9** | **Misdirected pointer: a reference resolves to nothing, or to something other than what is claimed of it** | 4/7 | **gate** (mechanical), **prompt** (attribution) |
| **K10** | **A rule is ported across a process, material or domain regime without stating the transfer conditions** | 6/7 | **prompt** |
| **K11** | A CLI/tool output field is misread | 2/7 | — do not build for this |
| **K12** | An invariant is carried across a change that invalidates it | 1/7 | trivially gate-able; highest severity, lowest frequency |

Bolded rows are the three defined here for the first time.

### K7 — Internal contradiction

Two parts of the document cannot both be true. No external source is required
to find it; the document refutes itself. Distinct from K3 (which needs the
source read) and from K6 (which is about a validator's region, not about
consistency).

- `tile-wall-grounding-audit.md:48` — §4 claims the engaged clip is
  "unstressed" *and* that capture depth ≥ 2× warp pulls bowed tiles flush.
  Flattening a bowed tile stores energy. The audit's own note:
  *"Internal contradiction found (no external source needed)"*.
- `tile-wall-grounding-audit.md:80` — the doc's own formula "slot = shank +
  0.5 mm" gives ≈4.7 mm for a #8, while its worked example says "4 × 8 mm".
- `piece-composition-grounding-audit.md:76` — §4.1's flagship example
  `hole grub radial 3.2` is a hole through a curved wall, which §8 itself
  classifies as forcing op (1), out of scope until C4. *"The doc's flagship
  BulbCollar therefore cannot be built with the machinery the doc ships."*
- `hemisphere-split-grounding-audit.md:230` (F12) — the status line asserts an
  audit was done; Appendix B says it is "pending".
- `lego-lab-grounding-audit.md:207` — §5.2 says the outline "is the pattern's,
  not a rectangle"; §7.2 partitions only the rectangular case.
- `lego-lab-grounding-audit.md:112` — a source cited approvingly designs in
  0.1 mm of clearance, "a direct contradiction of §3.2's zero-clearance
  premise, which the doc does not reconcile."

**Severity note.** K7 is the cheapest kind to find and among the most
expensive to leave: `hemisphere-split` F12 shipped a status line claiming an
audit that did not exist, and `piece-composition` shipped a headline example
its own machinery could not build.

### K9 — Misdirected pointer

A reference resolves to nothing, or resolves to something that is not what the
document claims of it. Three sub-forms, all present:

*Resolves to nothing.*
- `hemisphere-split-grounding-audit.md:232` — the status line links
  `research/hemisphere-split-grounding-audit.md`; the file did not exist.
- `lego-lab-grounding-audit.md:187` — a Brick Architect URL with *"zero Wayback
  snapshots, ever… The URL very likely never existed."*

*Resolves to the wrong line.*
- `hemisphere-split-grounding-audit.md:236` (F13) —
  `language-reference.md:838` should be `:840`; `evaluator.ts:2483` should be
  `:2485`. Both errors also present in the upstream survey.

*Resolves, but the attribution is wrong.*
- `piece-composition-grounding-audit.md:88-89` — two quotes cited to an HN item
  are verbatim from `juraph.com`; a "5–30×" figure cited to Manifold #387 is
  from OpenSCAD PR #4533, and a "3m36s → 3.4s" figure *"matches no fetched
  source and appears garbled."*
- `w2-connector-grounding-audit.md:106` — *"equations credited to McMaster &
  Lee of AlliedSignal Inc., not BASF; survey/doc call them 'the BASF Q-factor
  equations'."*
- `w2-connector-grounding-audit.md:12` — a real ½ layer-strain factor cited to
  Unionfab; it belongs to Core77/Fictiv.

**Why K9 is not K3.** In K3 the claim is unsupported. In the attribution
sub-form of K9 the claim is *true and sourced* — the pointer just names the
wrong source. K3 costs the claim; K9 costs the reader's ability to check it,
and silently inflates the apparent number of independent sources.

### K10 — Regime transfer without stated conditions

A rule, constant or convention established under one process, material or
domain is applied under another without stating what must hold for the transfer
to be valid. The rule is usually real; the transfer is the unstated step.

- `tile-wall-grounding-audit.md:20` — the ~10-module rigid-run rule ported from
  garage-tile buckling and EJ171. **"CONTESTED transfer"**: the source failures
  are *"sun-exposed, tightly interlocked, meter-scale floating floors"*; the
  target is indoor decor with open 1.2 mm gaps. `:63` — *"its physics
  justification indoors is circular."*
- `tile-wall-grounding-audit.md:59` — ANSI A108.02's 3× joint rule exists so
  *grout* can absorb facial variation; ungrouted printed gaps have no grout.
  The audit judges this transfer acceptable — which is the point: the transfer
  has to be *argued*, and here it was not.
- `print-validation-grounding-audit.md:17,47` — `h·tanθ` is Cura's
  from-vertical convention; PrusaSlicer measures from horizontal and uses
  `h/tanθ`. They coincide at 45°, so *"this will hide a convention bug until
  someone changes the default."* The audit calls it a **"silent porting
  hazard"**.
- `w2-connector-grounding-audit.md:37` — Covestro's snap-fit doctrine is
  injection-moulding doctrine and *"the liberal end"* of it; the Ticona and
  AlliedSignal lineages allow 50% of yield strain where Covestro allows 70%.
- `piece-composition-grounding-audit.md:72` — the fit ladder's small numbers
  are *"designed gaps after hole compensation on a calibrated printer"*;
  mainstream guidance quotes raw uncompensated clearances 2–10× looser. Plus a
  sign inversion: *"some sources' 'press fit 0.1 mm' means clearance, the
  ladder's means interference."*
- `lego-lab-grounding-audit.md:148` — a 0.2 mm **inter-part moulding relief**
  reused as a pattern-registration tolerance. *"Reusing it is a category
  error."* Same audit, `:290`: NIST's bore/boss split is metal LPBF —
  *"mechanism transfers, magnitudes do not"* — which is the correctly-stated
  version of the same move.
- `c2-assembly-grounding-audit.md:16,61` — BOSL2's library-wide spin convention
  is documented, but never composed for the anti-aligned case the doc needs;
  the doc's *"sign convention is undocumented"* generalises a gap in one page
  into a gap in the library.

**Why K10 is not K1.** K1 drops a qualifier the source stated. K10 omits a
condition the source never had to state, because the source was not writing for
our regime. It cannot be caught by re-reading the source more carefully; it is
caught by asking *what would have to be true for this to carry over.*

---

## 3. What the taxonomy buys

Mapping each kind to the mechanism that can actually catch it is what produced
the build list in `issue-register-evaluation.md` §6:

| Mechanism | Kinds it can catch | Change it justifies |
|---|---|---|
| Session-loaded rule (prompt) | K1, K2-framing, **K7**, **K10** | a `CLAUDE.md` carrying these four with their failure mode attached |
| Executable gate | K4, K6, K12, mechanical K3, mechanical **K9** | the K6 validator-example rule; the K4 citation-or-`CAL-*` rule |
| Adversarial measurement only | K5, K8, semantic K3 | keep running `ground-design-doc`; nothing cheaper substitutes |
| Nothing worth building | K11 | 2/7, low severity |

The three kinds defined here are not filler: **K7 and K10 are two of the four
kinds that carry the prompt-preventable case**, and K10 is 6/7 — tied with K5
as the third most frequent kind in the corpus. Leaving them undefined left the
single largest proposed change in §6 resting on ids that did not resolve.

### 3.1 What was built, and what it actually covers

The prompt half is `CLAUDE.md` at the repo root: K1, K2, K7 and K10 as four
rules, each with the corpus instance that produced it attached.

The gate half is `.claude/gates/docs_gate.py`, wired as
`.githooks/pre-commit.d/30-docs-gate` and `make validate-docs`. Three rules:

| Rule | Kind | What it checks |
|---|---|---|
| **D1** | K9 | every relative markdown link resolves on disk |
| **D2** | K6 | every `**Validator:**` declaration ships an asserted `PASS:` and `FAIL:` in its own section |
| **D3** | K4 | every `**Default:**` declaration carries a citation link or a `CAL-*` bet id in its paragraph |

Each rule ships an asserted-PASS and an asserted-FAIL fixture under
`.claude/gates/fixtures/`, verified by `docs_gate.py --self-test`. This gate
enforces the K6 rule, so it had to satisfy it; the PASS fixture caught a real
false positive in D3's first implementation, which only read the marker line
and therefore rejected provenance that had wrapped onto the next line.

**Measured coverage, 2026-07-30.** Against the 18 files in `docs/` plus
`CLAUDE.md`:

- **D1 checks 83 relative link targets and reports 0 findings** — zero false
  alarms on the corpus that rejected a URL link-checker at ~11% false alarms
  (`issue-register-evaluation.md` §5.1). D1 is the network-free half of that
  check, and it is the rule that would have caught `hemisphere-split`'s F12 and
  the dead pointer this repo shipped on 2026-07-29.
- **D2 and D3 currently match nothing: the corpus contains 0 `**Validator:**`
  and 0 `**Default:**` markers.** They are dormant. They constrain docs written
  from now on and do not retro-fit the seven audited docs, which state their
  validators and defaults in free prose.

That is the honest state, and it is a deliberate trade rather than an
oversight. A rule that infers "this sentence is normative and contains a
number" from prose is the noisy design §5.1 rejected. A marker the author opts
into is checkable with no false positives, and the failure mode is a doc that
declines the discipline rather than a gate that cries wolf. **The cost is
real:** D2 and D3 cannot catch an author who simply never writes a marker.
Whether that happens is the measurement that should decide their future — if
the next two design docs carry no markers, these two rules should be deleted,
not extended.

---

## 4. Honest limits

- **Shared author.** All seven design docs, all seven audits, and both
  classification passes come from the same author working in the same repo.
  Kind frequencies here are a fact about this corpus, not about design docs.
- **Presence, not instances.** The `Audits` column counts audits containing at
  least one instance. A kind at 4/7 may have one instance in each of four
  audits or twenty in one; the column does not distinguish, and no instance
  census was taken.
- **Two passes, one method.** K7/K9/K10 were counted in this pass against the
  full corpus; the other nine rows are carried. Both passes are judgment-based
  classifications of prose findings, with no inter-rater check.
- **The boundaries are judgment calls.** K3/K9 and K1/K10 are argued above
  precisely because they abut. A different classifier would move some findings
  across those lines; the counts would shift by ones, not by kinds.
- **This file has not been tested.** Like the §6 proposals it scopes, nothing
  here has been run against a new design doc. The first real test is whether a
  `CLAUDE.md` carrying K1/K2/K7/K10 changes what the next audit finds.
