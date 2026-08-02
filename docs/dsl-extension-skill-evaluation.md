# Evaluating an `extend-the-dsl` skill with hook-validated code pointers

**Date:** 2026-07-30 · **Status:** COMPLETE — verdict reached and implemented
**Repos touched:** bikar (all code), 3d-models (this document)

---

## 0. The request, and what happened to it

> *"track task to see if we need a skill to extend the dsl/spec/etc that captures
> the setup with code pointers that are validated via hooks etc"*

Two halves. **Verdict: the first half is already built and a third skill would
make it worse; the second half was genuinely missing and is now a gate.**

The task was posed as a question — *do we need this?* — so the honest answer
required measuring before building. Both halves were measured. One premise
failed and one held.

---

## 1. Half one — "a skill to extend the DSL". **Falsified. Not built.**

There are already two, with a routing tree between them:

| Skill | Covers |
|---|---|
| `.claude/skills/dsl-design/SKILL.md` | The *shape* — naming, relative construction, statement-vs-attribute, the pitfalls |
| `.claude/skills/engine-extension/SKILL.md` | The *mechanics* — the token→AST→parser→evaluator→environment→UI→tests walk, plus the DCEL internals |

Neither is a stub. `engine-extension` opens with a five-way routing preamble
whose stop rule is *"before building a new primitive, confirm it doesn't already
exist"*, and `dsl-design` opens by pointing at `engine-extension` for the
geometry-algorithm case. A third `extend-the-dsl` skill would sit exactly on top
of that seam and its only distinguishing content would be a table of contents for
the other two. Skills compete for a reader's attention; a third one that says
what two already say makes the correct one **harder** to find, not easier.

**So the work moved to where those two were actually wrong.** Which turned out to
be a real place.

### 1.1 The gap, proven rather than asserted

`engine-extension`'s step list is headed *"Follow these steps in order. Every step
is required."* Seven steps: Token → AST Node → Parser → Evaluator → Environment →
Web UI → Tests.

That list was written before this week's grammar work. To find out whether it was
still true, a `chamfer` statement was injected in an **isolated git worktree**
following the seven steps exactly, then the suite was run:

```
FAIL  keywords-snapshot.test.ts
  new reserved word(s) — every .bkr using one as a name now fails:
  expected [ 'chamfer chamfer' ] to deeply equal []

FAIL  grammar-conformance.test.ts
  statement form(s) with no row in docs/grammar.md §12:
  expected [ 'chamfer' ] to deeply equal []
```

**Three failures, from a checklist that claims completeness.** An author who
follows the skill precisely and stops where it stops hands over a red suite. That
is not a documentation nicety; it is the skill actively lying about being done.

Two further staleness findings from the same read:

- Step 3 said *"add to `parseStatement()` switch."* It has not been a switch since
  the spans work — it is a `Partial<Record<TokenType, () => ASTNode | null>>`
  handler table, and that is not a cosmetic difference: the table is precisely
  what lets `grammarSurface()` export the author-visible keyword list to the gates
  in the new step 8. Following the stale instruction produces code that works and
  a gate that can no longer see it.
- Step 3 also said *"add to `BODY_STARTERS`"*, singular. There are **three**,
  declared locally in `parseRepeat`, `parseRotate` and `parseMirror`, and they are
  **not identical** — `repeat`'s omits `mirror`, `bisector`, `tangent`, `offset`
  and `fillet`. "Add it to BODY_STARTERS" is not an executable instruction.

### 1.2 What was changed

`engine-extension` gains steps **8 (Grammar)** and **9 (Keyword snapshot)**, each
leading with the failure it prevents rather than the procedure it prescribes, and
the preamble now states the measured result: *stopping at step 7 leaves the suite
red, and here are the three failures.* Steps 3's two stale claims are corrected.
`dsl-design` gains a pointer to `docs/grammar.md` as the syntax specification,
with the precedence rule (`grammar.md` wins over `language-reference.md`) stated,
so the *shape* question is settled against the real list of existing forms.

Step 9 carries the part a checklist usually omits — the blast radius. Adding a
keyword silently revokes every existing `.bkr` file's right to use that word as a
circle id, point name, param name or pattern name. The snapshot's job is to make
that a decision someone typed. The step says so, and says to sweep the corpus
before updating the fixture, and says the honest resolution: *if the word is in
use, rename the keyword — a keyword is cheaper to change than someone else's
pattern.*

---

## 2. Half two — "code pointers validated via hooks". **Confirmed. Built.**

### 2.1 The premise held, and it was worse than the request implied

The nearest existing mechanism, `check-living-artifacts.py`, turned out on reading
to be an advisory **reminder** — it nudges you to update a living doc when related
code changes. It does not check that anything the doc *says* is true. So nothing
validated code pointers, and the request's premise was correct.

A crude first sweep of every backticked path in every doc found rot immediately.
Three refinement passes separated genuine rot from scanner naivety:

| Pass | Flagged | What changed |
|---|---|---|
| crude regex over all docs | 137 / 400 | — |
| require a file extension + a `/` | 37 / 361 | placeholders, prose, absolute paths dropped |
| **fail closed** (see §2.2) | 31 | the open predicate removed |
| scope rules (records excluded) | 23 | `docs/decisions/**`, `docs/issues/**` are records, not living prose |
| after fixing what had a right answer | **12** | baselined |

The three worst were exactly the kind that matter:

- **`.claude/skills/engine-extension/SKILL.md`** — the skill whose entire job is
  telling the next author where the files live — pointed at
  `packages/core/src/renderer/` for a directory named `render`. Two rows of its
  key-file table were dead.
- **`CLAUDE.md`** cited `.github/workflows/ci.yml` inside a bullet about *qiyas's*
  CI. The file exists in qiyas; the pointer, read from bikar, resolves to bikar's.
  A pointer that resolves to the wrong repo is worse than one that resolves to
  nothing.
- **`docs/dev-mental-model.md`** pointed at `packages/core/src/kernel/face-extraction.ts`
  for `packages/core/src/graph/face-extractor.ts` — wrong directory *and* wrong
  filename, in the document whose purpose is orienting a newcomer.

### 2.2 The gate failed open on its first draft, and that is the finding

After the doc-relative-path fix, the checker reported the `engine-extension`
`renderer/` line as **`ok`**. The directory does not exist. The cause was the
sibling-repo fallback, written as an open predicate:

```ts
return sibling !== path && !existsSync(siblingRoot) && /^[a-z0-9-]+$/.test(sibling);
```

`packages` matches `^[a-z0-9-]+$`, and `../packages` does not exist, so the
predicate returned `true` — *"this is a sibling repo I can't see, so I can't call
it wrong."* Every unresolvable path whose first segment looked like a repo name
was being waved through.

This is Tenet 29's exact failure mode, committed inside the gate written to
enforce it. The fix is a **closed** set:

```ts
const SIBLING_REPOS = new Set(['bikar', 'qiyas', '3d-models', 'sacred-patterns',
                               'coffee-house-design-kit']);
if (!SIBLING_REPOS.has(sibling)) return false;
```

Violations went **5 → 31**. The 26 that appeared were all real, and had been real
the whole time. Recorded here because the number is the argument: a gate that
fails open does not report a smaller problem, it reports a *different* problem,
and the difference was 5× here.

Where a sibling repo *is* named and *is not* checked out, the checker returns
`true` — but that is "unknowable", not "unverified": a distinct case, reachable
only through the closed set, and it degrades to a warning rather than a silent
pass. Everything else is `false`.

### 2.3 What shipped

`bikar/scripts/check-doc-pointers.ts` — scans `CLAUDE.md`, `.claude/skills/**/*.md`
and `docs/**/*.md`; extracts every backticked path bearing a file extension and a
`/`; resolves it against the workspace roots, then the document's own directory,
then the closed sibling set; fails closed otherwise. Current state: **353 claims
across 88 documents, 339 resolve, 12 grandfathered.**

`bikar/.doc-pointer-baseline.json` — the **shrink-only, append-blocked** baseline,
following `.calibration-baseline.json`'s precedent exactly. Growth requires
`DOC_POINTER_BASELINE_MAY_GROW=1`, so a new dead pointer is a decision someone
typed rather than a diff nobody noticed. The gate also ratchets *down*: a
baselined entry that starts resolving, or that is no longer written anywhere,
is itself a violation telling you to delete it.

Wired into `npm run ci` and into `.husky/pre-commit`, scoped to staged docs,
skills, the baseline and the checker itself.

**The 12 grandfathered entries are not laziness — none can be fixed by editing a
path**, and the baseline's `_comment` says which group each is in:

1. **Mirrored canonical docs** (`decision-schema.md`, `dsl-metadata-contract.md`)
   — authored in sacred-patterns and mirrored verbatim; editing bikar's copy forks
   the mirror. Fix upstream and re-mirror. *(This was learned the hard way: the
   file was edited, then reverted with `git checkout --` on reading its own
   header — "when a mirror disagrees with this file, this file wins.")*
2. **Deleted artifacts** still cited as examples by living prose — the file is
   genuinely gone and the surrounding sentence needs rewriting by someone who
   knows what it should say now, which is editorial work, not a path fix.
3. **Sister-repo tools** whose path omits the repo prefix and whose repo may not
   be checked out.

### 2.4 The second bug: the verdict depended on build state

The gate was green in the working checkout and, run for the first time in a fresh
worktree, immediately failed on **4 pointers into `dist/`** —
`packages/core/dist/index.js` and friends, in `.claude/skills/dev-workflow/SKILL.md`, `CLAUDE.md`
and `docs/lessons.md`. Those files exist in a checkout that has been built all
week and in no other.

A gate whose answer changes with whether you last ran `npm run build` is worse
than no gate, because it teaches you to ignore it — and it would have failed CI on
a clean runner the first time it ran there, on a violation with nothing to fix.
Excluded by rule (`GENERATED`, matching a `dist`/`build`/`coverage` segment at any
depth), not baselined, for the same reason `docs/decisions/**` is by rule: a
baseline entry means "known broken, fix later", and these were never broken.

Both checkouts now report identically — **353 claims, 339 resolve, 12
grandfathered** — which is the property that was actually wanted.

This is also why the worktree was used rather than committing from the working
tree: the isolated run is what surfaced it.

### 2.5 Verified adversarially, in both directions

Neither direction was assumed:

```
A. inject `packages/core/src/nope/does-not-exist.ts` into docs/roadmap.md
   → 1 violation, names the file and prints the JSON to paste.  EXIT=1

B. replace a live baseline entry with a path no doc writes
   → 2 violations: the now-unbaselined real pointer, AND
     "`scripts/never-written.sh` is no longer written in docs/roadmap.md
      — delete its entry."                                       EXIT=1
```

---

## 3. Verdict

| Half of the request | Verdict | Outcome |
|---|---|---|
| A skill to extend the DSL | **Premise falsified** | No new skill. Two existing skills corrected — 2 new mandatory steps, 2 stale claims fixed, 1 routing pointer added. |
| Code pointers validated via hooks | **Premise confirmed** | `check-doc-pointers.ts` + shrink-only baseline, in `ci` and pre-commit. 11 dead pointers fixed, 12 grandfathered with reasons. |

The through-line is that both halves resolved the same way: **the documentation
was wrong in ways nothing could detect, so the fix is a detector, not more
documentation.** Adding a third skill would have added a fourth thing to go stale.
Adding a gate makes the existing three keep themselves honest — and it earned its
keep before it was even committed, by catching a lie in the very skill that tells
authors where the code is.

### Scope-outs

- **Pointers inside `docs/decisions/**` and `docs/issues/**` are not checked.**
  These are dated *records*. A decision doc that cites `/tmp/probe-3.mjs` is
  correctly reporting what was run that day; making it resolve would mean
  falsifying the record. Excluded by rule, not by baseline.
- **Non-backticked paths are not checked.** A path in plain prose is not a claim
  in the way a code-formatted one is, and the false-positive rate on prose was
  what made the crude first pass useless.
- **Heading and URL targets are not checked** — headings already are, by
  `grammar-conformance.test.ts`, for the `> Grammar:` links specifically. Neither
  was generalized here.
- **The sibling repos are not cloned to check.** If one is absent its pointers are
  unknowable and pass; the closed set bounds which names get that treatment.
