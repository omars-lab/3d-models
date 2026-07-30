# Evaluating an issue-register skill with reminder hooks

**Date:** 2026-07-30 · **Status:** COMPLETE — verdict reached, nothing built yet
**Repos measured:** bikar, qiyas, 3d-models (this document)

---

## 0. The request, and what happened to it

> *"as we encounter new issues do we keep track of these in an issue catalog and
> websearch existing trusted solutions and best practices before recommending an
> approach… this should be a claude skill with reminder hooks in issues
> terminology"*

Three halves. **Verdict: all three mechanisms already exist. Two of them have
already been measured failing in this project, and the measurement says the
missing piece is not a register at all.**

| Half of the request | Premise | Verdict |
|---|---|---|
| An issue catalog | "we don't have one" | **Falsified in bikar (five exist), confirmed in 3d-models** — but a sixth would not have prevented what actually recurred |
| Websearch before recommending | "it doesn't happen" | **Confirmed** — 13 of 15 issue docs cite zero sources. A reminder hook is the wrong fix; one is already installed and did not work |
| Reminder hooks | "we should add some" | **Falsified** — two hook mechanisms are wired and running. Neither is pointed at any register, deliberately |

The task was posed as a question — *do we do this?* — so the answer required
measuring before building, per the precedent set by
[`dsl-extension-skill-evaluation.md`](dsl-extension-skill-evaluation.md)
("no skill, a gate instead"). Everything below is a count, not an impression.

---

## 1. Half one — "an issue catalog". Falsified in bikar, and the falsification is instructive

### 1.1 Five registers already exist

| # | Register | Size | Last grown | Documented in CLAUDE.md? |
|---|---|---|---|---|
| 1 | `bikar/docs/issues/*.md` | 15 docs, 2 303 lines | 2026-07-29 | **No — zero mentions** |
| 2 | `bikar/docs/engine-issues.md` | 10 entries, 81 lines | 2026-07-29 | Yes ("Add entries IMMEDIATELY") |
| 3 | `bikar/docs/lessons.md` | 446 lines | **2026-06-11** | Yes |
| 4 | `bikar/CLAUDE.md` §Hard-Won Lessons | ~17 bullets | all 2D/web-UI era | is itself |
| 5 | `qiyas/CLAUDE.md` tenets w/ `Failure mode this prevents:` + `Stop rule` | inline | current | is itself |

Registers 1 and 2 overlap on **exactly 1 of 24 union entries** — the 2026-07-29
region-overlap bug, the only `engine-issues.md` entry carrying a
`**Detail:** docs/issues/…` pointer. Twenty-three issues live in exactly one
register, and no rule anywhere states which gets what. The inversion is the
tell: **`CLAUDE.md` documents the register with 3 content updates in 4 months
and never mentions the one with 15 documents.**

Register 5 is the most evolved form and the only one that is read by
construction — the failure is welded to the rule as its justification, inside a
file that loads every session. It is not a separate artifact at all.

### 1.2 The register decayed while the defect rate tripled

Over 426 commits (2026-03-08 → 2026-07-30), 48 commits are defect fixes.
**Twelve have an entry in any register — 25%.**

| Month | Commits | Defect fixes | Fix rate | Covered by a register |
|---|---|---|---|---|
| 2026-05 | 200 | 14 | 7.0% | 7 (50%) |
| 2026-06 | 35 | 8 | **22.9%** | 2 (25%) |
| 2026-07 | 65 | 13 | **20.0%** | 1 (8%) |

The obvious reading — "the register works, it just needs enforcement" — is
available here, and June + July are its best evidence: **21 defect fixes
produced 2 issue docs, and neither of those 2 documents any of the 21.** It was
not a quiet period; per commit, June and July are the buggiest months in the
repo's history.

That reading has one direct test, and it fails.

### 1.3 The decisive measurement: a register entry that existed, was good, and changed nothing

`docs/issues/2026-05-15-silent-emission-filters.md` inventories **six** places
where the engine silently drops data rather than failing. It is a good document.
Its stated decision was "Option A — fix sites incrementally as they trip again."
It is still marked OPEN.

Between that date and 2026-07-30 the same class — *a reader that fails open on
input it cannot parse* — shipped and was fixed **six more times**:

| # | Commit | What failed open |
|---|---|---|
| 1 | the issue doc itself (2026-05-15) | six inventoried silent-drop sites |
| 2 | `fafd510` (05-18) | silent Option E skip in the evaluator |
| 3 | `2180d10` (06-26) | `check-pack.js` regex matched zero lines — the publish gate audited zero files and reported green, broken since 2026-04-22 |
| 4 | `64920a9` (07-29) | `param-rewrite.ts` failed open in both directions — returned source unchanged, or deleted a second `param` |
| 5 | `1d1fcb5` (07-29) | `stripDataSelectors` emitted half-stripped selectors where nothing validates |
| 6 | `dc97409` (07-29) | `evalPolygon` bound check let `-1` through, pushing `undefined` into the vertex array |
| 7 | `5426fe8` (07-30) | **the doc-pointer gate written to enforce this very class** failed open in its own first draft; violations went 5 → 31 once closed |

**`git grep silent-emission-filters` returns zero hits outside the file itself.**
A durable, well-written record of exactly this failure class sat on disk for 76
days and was never once cited — including by the commit that reinvented the
failure inside the gate built to prevent it.

What actually stopped it was not a register entry. It was **Tenet 29** landing
in `CLAUDE.md` on 2026-07-29 (`4e4a2b3`), 75 days later, plus one deliberate
sweep that found instances 4–7 in a single day. A rule that loads every session,
and a search. Not an archive.

### 1.4 The counter-case, stated fairly

The strongest evidence *for* a register is `docs/issues/2026-05-15-magick-msvg-blanks-valid-svg.md`,
headed **"REFRAMED-THIRD-TIME"**: a symptom that was rediagnosed three times
(ImageMagick parser bug → arc-face leak → the `connect arc … .CLASS` source path
was never sound), with seven options authored and falsified in sequence across
~35 commits.

Here **four issue docs existed and were actively maintained** — and the register
did not shorten the search. One of them
(`2026-05-16-region-identity-class-not-reaching-svg-fill.md`) describes itself
as "a regression of #329's claimed N=4/N=8 fix" and is *still* OPEN. A
companion doc states outright: "Same family as bikar#290 … and bikar#333."

So the register's best-covered episode is also its clearest demonstration that
coverage is not the binding constraint.

A related gap: `2026-07-29-region-overlap-boundary-degeneracy.md` (point-in-polygon
undefined on a shared boundary) cites source files, a decision doc and a design
doc under `## Related` — and **zero prior issue docs**, though
`2026-05-16` had already named probe-point precision in the same predicate
family 74 days earlier. Retrieval failed even for an author writing in the register.

### 1.5 What did work, measurably

Of the 15 issue docs, **5 reached an executable guard** (4 regression tests,
1 CI conformance gate); 5 are doc-only with no guard; 5 are still open.

Meanwhile the guard habit strengthened exactly as the narrative habit collapsed.
**All seven July defect fixes shipped a test, and none produced a register
entry:**

```
dc97409  →  polygon-midpoint-vertex.test.ts            (94 lines)
c836778  →  source-tags-shared-predicate.test.ts      (152 lines)
1d1fcb5  →  animation-compiler-selector-strip.test.ts
c1d7195  →  evaluator-nesting-rank.test.ts            (141 lines)
2180d10  →  scripts/check-pack.test.mjs                (74 lines)
64920a9  →  param-rewrite.test.ts                     (+244 lines)
7694835  →  lexer.test.ts                             (152 lines)
```

Plus `check-doc-pointers.ts` with an append-blocked baseline, wired into `ci`
and pre-commit. The thing that is working grew; the thing being proposed shrank.

### 1.6 3d-models: the premise holds, but for a different artifact

3d-models has **no backward-looking register of any kind** —
`git ls-files | grep -iE "issue|bug|defect|errata|retro"` returns zero paths —
and, more consequentially, **no `CLAUDE.md` at all**. It has three
forward-looking registers, two of them machine-validated: calibration bets
(generated from `Calibrated<T>` records, `npm run registry:calibration:check`),
the prototype catalog, and the use-case map (`validate.py`, blocking pre-commit
hook).

So this repo has invested in forward-looking machinery with executable
validators, and has zero session-loaded rules. That asymmetry is real. §5 shows
it is not an issue-catalog-shaped hole.

---

## 2. Half two — "websearch trusted solutions before recommending". Confirmed, and already refuted as a hook

### 2.1 The premise holds

**Thirteen of fifteen bikar issue docs cite zero external URLs.** The two
exceptions are both about third-party tooling (ImageMagick MSVG, gt-emitter
templates). Research does not happen at fix time.

That is not automatically a defect — most of these are engine-internal geometry
bugs whose fix derives from the engine's own invariants. But at least one had a
named canonical prior art that a single search would have surfaced: the
region-overlap bug is the textbook "even-odd ray casting is undefined for points
on the boundary" pitfall, with a standard remedy family. It was rediscovered
from first principles.

### 2.2 The experiment has already been run in this project, and it failed

qiyas ships `.claude/hooks/web-source-curation-watch.sh` — fires on
`PostToolUse(WebSearch|WebFetch)`, emits *"consider adding the source to
`docs/citations.md`"*. It is wired in `.claude/settings.json` and has been live
since **2026-05-11**.

`docs/citations.md` (344 lines, 22 entries) has had **one commit touch it
since**, on 2026-06-10, from an unrelated decision-memory feature commit. Its
last substantive content edits are from 2026-05-07 and 2026-04-28 — both
predating the hook.

A reminder hook, correctly implemented, firing on exactly the right event, at
exactly the right moment, into a register that already existed, did not keep
that register alive. This is the request's proposed design, already built,
already measured.

*(Honest limit: I cannot count how many `WebSearch` calls fired in qiyas during
that window, so I cannot state a per-firing conversion rate — only that the
destination did not grow.)*

### 2.3 What already covers the good case

[`ground-design-doc`](../.claude/skills/ground-design-doc/SKILL.md) covers
research-before-recommending thoroughly: adversarial verify-and-refute agents,
research checked into `docs/research/*.md`, counter-evidence per bet, the
`(unverified snippet)` marking rule, and a handoff of empirical residue to
`calibrate` as CAL bets. It produced the 14 research files and 7 audits this
repo runs on.

Its scope is a **design doc**, on manual invocation. It does not fire when a
fix is chosen at the terminal. That is the real gap, and it is a gap in *when*,
not in *what* — which is why a second skill saying the same thing is the wrong
shape.

---

## 3. Half three — "reminder hooks". Both mechanisms exist and are deliberately unpointed

| Repo | Mechanism | Rules | Points at a register? |
|---|---|---|---|
| bikar | `Stop` → `check-living-artifacts.py` + `living-artifacts.yaml` (glob → reminder) | 6 | **No** |
| qiyas | `PostToolUse` → six `*-watch.sh` hooks | 6 | citations.md only (see §2.2) |
| 3d-models | `.githooks/pre-commit.d/` → `10-gitleaks`, `20-use-cases` | 2 | n/a — blocking gates |

Adding an issue reminder is a **YAML rule**, not a skill and not a new hook —
roughly four lines in `living-artifacts.yaml`.

Two things are worth carrying forward from how this project already writes hooks:

- **Every qiyas hook states its measured justification in its own header.**
  `critical-path-check.sh`: *"drift audit on 2026-05-17 measured 63% off-path
  pickups over 30 commits; this hook is the structural fix."* `ci-drift-watch.sh`:
  *"CI was silent for 16 days while master accumulated ~12 red tests."* Any hook
  proposed here inherits that bar.
- **`check-doc-pointers.ts` excludes `docs/issues/` by rule**, with the reason
  stated in the source: each file is *"a dated report of a bug as it stood on
  the day, `**Status:** OPEN` and all… A checker that forced those to resolve
  would erase the history."* The register is, by construction, outside the gate
  ecosystem — which is precisely why entries in it cannot be kept honest the way
  pointers, decisions and calibration bets are.

---

## 4. What the outside literature says, applied to its own question

Research: [`docs/research/issue-register-practice-survey.md`](research/issue-register-practice-survey.md).
Headline findings, each traceable to a primary source:

- **The success condition is being re-read, not being written.** Google SRE:
  *"An unreviewed postmortem might as well never have existed."* Allspaw's
  markers of progress are *unique readers growing over time* and *explicit
  references appearing in forward-looking documents* — which is exactly the
  measurement §1.3 ran (`git grep` → 0) and exactly what it failed.
- **The decay mechanism is a spiral, and it is named:** *"People don't read them
  because they're terrible… because people don't put a lot of effort into them…
  because they don't think anybody's going to get anything out of it."*
- **GAO-02-195 (NASA)** is the canonical audit of a lessons-learned database
  that existed and was not read: *"lessons are not routinely identified,
  collected, or shared."* Capture was never the bottleneck; retrieval and
  incentive were. §1.3 is a two-person-shaped instance of the same finding.
- **The executable-guard half is well-attested prior art.** Django requires a
  regression test that *fails before the fix*; Fowler: *"first write a test that
  exposes the bug, and only then… fix it."* Google's SRE Workbook requires
  action items with *"a verifiable end state."*
- **The classification half is not.** ODC claims *insight*, not behaviour
  change; **IEEE 1044-2009 has been Inactive-Reserved since 2020**. A taxonomy
  scheme its own standards body stopped maintaining is weak ground for mandating
  taxonomy here.
- **There is no established backward-looking counterpart to the ADR.** Across
  Nygard's original, adr.github.io, and the largest ADR variant catalogue, every
  variant is prospective. A "decision ledger + issue register" pairing would be
  a local invention, which removes "industry standard practice" from its
  support.
- **Anthropic's own guidance points the opposite way from accumulation.**
  *"Bloated CLAUDE.md files cause Claude to ignore your actual instructions"*;
  target **under 200 lines**; *"If Claude already does something correctly
  without the instruction, delete it or convert it to a hook"*; skill
  descriptions compete inside a 1 536-character always-loaded listing; an
  invoked skill's content is *"a recurring token cost"* every turn.
  [Lost in the Middle (arXiv:2307.03172)](https://arxiv.org/abs/2307.03172)
  supplies the mechanism.

**The strongest sourced argument against building it** comes from Richard Cook,
and it names this proposal precisely: the organisational demand for *"the
reduction of an incident to a manageable discrete list of things to be done"* is
identified not as the goal of incident review but as the pressure that degrades
it into *"pallid, vapid, mechanical exercises"* producing *"a defensible
argument that management is occurring."* So the register's own governing rule —
"graduate into a guard or close as a one-off" — is, in the resilience literature,
the signature of the failure mode rather than a defence against it.

Which leaves a clean dominance argument: **the guard requirement does all the
work, and it needs neither a register nor a skill.** A test that fails before
the fix protects behaviour with zero re-reading, at zero context cost. The
register adds ongoing context cost and a third competing skill, and buys only
the cross-entry theme-spotting that Cook observes organisations with far more
volume *"seldom"* actually perform.

---

## 5. The recurrence in 3d-models is real — and it is not bugs

The seven grounding audits in `docs/research/*-grounding-audit.md` are an
unintentional corpus of ~104 findings across 7 independent design efforts.
Classified into failure kinds, **five kinds appear in all seven audits**:

| Kind | Audits | Preventable by |
|---|---|---|
| **K3** Citation does not contain the claim | 7/7 | mechanical half: **gate** · semantic half: **measurement only** |
| **K1** Qualifier stripped between source (or our own survey) and the claim | 7/7 | **prompt** |
| **K4** Unsourced number presented as fact, then defaults keyed to it | 7/7 | **gate** |
| **K2** Exhaustiveness asserted over an unsearched space | 7/7 | **prompt** for the framing, **measurement** for the search |
| **K6** Validator specified against the wrong acceptance region | 7/7 | **gate** |
| K5 Measured the wrong object | 6/7 | mostly measurement |
| K8 Semantic meaning assumed for an incidental artifact | 4/7 | **measurement only** |
| K11 Misread a CLI output field | 2/7 | — do not build for this |
| K12 Invariant carried across an invalidating change | 1/7 | trivially gate-able; highest severity, lowest frequency |

Two of the request's implicit premises land in the bottom rows. The failure
modes that felt most vivid from inside a session — misreading `islands=0/20`,
carrying an Euler identity across a design change — are **1/7 and 2/7 events**.
The ones that recur every single time are citation and validator-specification
defects.

**A checklist would plausibly have caught K1, K10, K7 and the framing half of
K2** (~4 kinds, ~45 instances). It would have caught **none** of K8, and only
the framing of K5.

### 5.1 A link checker is measurably the wrong gate

`docs/` holds **737 distinct URLs, 1 685 occurrences, across 29 files**, checked
by nothing. bikar's `check-doc-pointers.ts` validates *code* pointers only and
explicitly scopes out URLs; it does not scan this repo.

I sampled 62 of the 737 (8.4%) and fetched each with a browser user-agent:

| Result | Count | Reading |
|---|---|---|
| 200 / 202 | 53 | fine |
| 403 bot-blocked | 4 | **live pages** — makerworld, solidworks, dynamobim, printables |
| 429 rate-limited | 2 | **live pages** — github, metmuseum |
| 000 connection failure | 1 | ambiguous |
| 404 | 2 | **both artifacts of my own extraction** — one is a markdown link truncated at `Surface_(topology`, the other is a literal `…` inside a passage already documenting that URL as dead |
| **Confirmed dead-link defects** | **0** | |

The audits *did* find genuine dead links (a 404, a 403, and one URL with no
Wayback snapshot ever, all quoted for load-bearing numbers). At ~3 in 737, an
8.4% sample expects to catch 0.25 of them — so this sample is consistent with a
true dead-link rate under 1%, against a measured **false-alarm rate of ~11%**.
Roughly ten false alarms per true one. bikar's own print-gate issue doc states
the consequence: *"A gate that cries wolf gets switched off, which is worse than
having no gate."*

The checkable invariant is not *does the URL resolve*. It is **is every
load-bearing number attributed to a source the research file records as actually
fetched** — a local check, no network, zero false positives by construction.
`ground-design-doc` already established the vocabulary (`(unverified snippet)`)
and never enforced it: 76 markers exist, but four surveys carrying 161, 194, 169
and 84 URLs have **zero**.

---

## 6. Verdict

**No new skill. No sixth register. No reminder hook.** Every mechanism the
request asks for already exists, and the two that have been measured in this
project both failed in the specific way the external literature predicts.

What the measurement *does* justify, ranked by strength of evidence:

| # | Change | Evidence | Cost |
|---|---|---|---|
| 1 | **A `CLAUDE.md` for 3d-models**, under 200 lines, carrying the four prompt-preventable audit kinds (K1, K2-framing, K7, K10) as rules with their failure mode attached — the qiyas tenet shape | 5 kinds at 7/7 across 7 efforts; §1.3 shows a session-loaded rule is what stopped F1 | one file |
| 2 | **The K6 rule as a gate**: every validator specified in a design doc ships one asserted-PASS and one asserted-FAIL example | 7/7; every K6 instance was found by an auditor hand-constructing a counterexample — the method is directly executable | small |
| 3 | **The K4 rule as a gate**: a number in a normative sentence carries a citation or a `CAL-*` bet id | 7/7; the machinery exists and is already gate-checked (10 bets, 5 with no record) | extend existing |
| 4 | **Route bikar's two registers**: `CLAUDE.md` documents the unused one and never mentions the used one; union 24, intersection 1 | §1.1, §5-hygiene; Nygard: *"Large documents are never kept up to date"* | small |
| 5 | **State the graduation rule and let it retire entries**: a defect writes a *test* always, and a narrative record only when it also produces a tenet | 5/15 graduated; 7/7 July fixes shipped a test with no entry | policy, not code |

Explicitly **not** justified by the measurement: a link checker (§5.1), an issue
catalog for 3d-models, a `WebSearch` reminder hook (§2.2), and any defect
taxonomy scheme (§4 — ODC/IEEE 1044).

The through-line matches [#42](dsl-extension-skill-evaluation.md)'s and sharpens
it. There, the finding was *"the documentation was wrong in ways nothing could
detect, so the fix is a detector, not more documentation."* Here it is one step
further: **the documentation was right, and nobody read it.** A sixth place to
write things down would have produced a seventh instance of the failure it
described.

---

## 7. Scope-outs and honest limits

- **The 7 audits are not fully independent.** All were authored in one repo over
  four days (2026-07-27 → 07-30) by the same author under the same skill.
  Shared-author correlation inflates the 7/7 recurrence figures. The *ranking*
  of kinds is more trustworthy than the counts.
- **The defect-fix classification is judgment-based.** 48 of 426 commits, by
  stated criteria, with every hash listed in the source measurement; May's 14 is
  soft by ±2. The ~20 falsification-doc commits of 2026-05-19 were **not**
  counted as fixes — the reading that argues *against* the conclusion here.
- **The URL sample is 8.4%** and caught none of the known-dead links. The 10:1
  false-alarm ratio in §5.1 is an estimate with that bound stated, not a
  measurement of the true positive rate.
- **qiyas's `WebSearch` firing count is unknown**, so §2.2 establishes that the
  destination did not grow, not a per-firing conversion rate.
- **Cross-repo issue docs in qiyas and sacred-patterns were not read.** Only
  bikar's registers were mined in depth.
- **Nothing here settles whether the five 7/7 kinds would recur under a
  different author**, and no proposal in §6 has been built or tested. Items 2
  and 3 are gate *specifications*; they inherit the K6 rule they propose and
  must ship with a PASS and a FAIL example before being believed.
