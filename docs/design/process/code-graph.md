---
status: idea
---

# A code graph across our repos

**Status:** idea (a proposal), 2026-11-05. The trial is not built yet. Rests on one research pass,
[../../research/2026-11-05-graphify-code-graph.md](../../research/2026-11-05-graphify-code-graph.md),
which read graphify's source and docs but did not run it, and on one test build run on
2026-11-06 (§6).

**In one paragraph.** Our sessions keep re-searching the same few facts. Graphify, a tool that
builds a graph of a code base, would answer one of the six we have measured fully and one in part,
and would miss four (the test build in §6 settled the two that were open). The facts we re-search are mostly settings, constants, data keys and
ids, and graphify is built for "who calls this function". So this doc proposes a short trial on
bikar only, plus two cheaper fixes that would help more: point sessions at the FAQ before they
grep, and add a complexity lint to 3d-models' Python.

## 1. The problem, measured by the six facts

The FAQ tool counts a fact as re-searched when a session greps for it, or fails on it, just before
using it (see [the issue note](../../issues/faq-counted-use-not-rederivation.md)). Six facts cleared
the bar of three or more sessions. They are listed in [the FAQ proposal](../../faq-proposal.md).

| Fact | Sessions | What kind of thing | Graphify answers it? |
|---|---|---|---|
| SCHEMA_VERSION | 5 | a constant, with several of the same name in qiyas | partly: bikar's `GT_SCHEMA_VERSION` is an entry (test build, §6), but the contract one is in qiyas, outside the trial |
| BIKAR_DIR | 4 | a setting in a Makefile, read from the environment | no |
| patternSources | 4 | a key in a data JSON file | no |
| tagSegments | 4 | a TypeScript method | yes |
| FILL_ATTRIBUTES | 3 | a private static set on a class | no: the test build (§6) does not record static class fields |
| UCN (use-case ids) | 3 | ids in a diagram, table cells and string values | no |

Five of the six already have answers in [the FAQ](../../faq.md), written 2026-11-03. The FAQ
tool's own check marks all five as "not taking": the one session since then searched for each
again. One session is far too few to judge. It still says the answers are not reaching sessions
before they grep, which is a delivery problem a graph would not fix.

## 2. One graph across the five repos

The five repos are 3d-models, bikar, qiyas, youtube and sacred-patterns. Searching across them is
a must.

- **Joining works.** Each repo's graph is built on its own, then joined into one combined graph
  (graphify's `global add` or `merge-graphs`). One query then covers all five. Node names carry
  the repo as a prefix, so a name in two repos stays two things.
- **Cross-repo links are narrow.** Graphify links a method call to its type in another repo, for
  TypeScript and several other languages but not Python. It also links a type declared the same
  way in two repos, a pass built for .NET; whether it fits our JSON schemas is unknown.
- **Our two examples get no link.** 3d-models' gates read BIKAR_DIR from the environment, which is
  a string to graphify. qiyas' schema and bikar's byte-for-byte copy are two unrelated files to it.
- **The smallest addition (an idea).** A short script, run after each join, adds the links we
  care about to the combined graph file. Best source: the use-case map's anchored pointers
  (`repo:path:Lnn "literal"`), which already name "this use, that definition" across repos and are
  checked by our hooks. Turning those into edges reuses a checked list instead of starting a
  second one. Setting links (from a grep for each read) and copy links (from a byte compare)
  would cover what the map lacks.

## 3. Where the graph lives, and how it stays in sync

All three options can answer one query across repos, because that comes from joining (section 2).
They differ in how fresh the graph is and what they cost.

**Recommended: (c) nothing stored, built locally.** Each repo's graph goes in a folder listed in
that repo's local git exclude file, so no tracked file changes. The combined graph sits in the
home folder.

- *Pros:* graphify's own way, so the least to build. Nothing in git. No cost for code.
- *Cons:* graphify's hooks skip worktrees on purpose, and most of our sessions work in worktrees.
  So the graph refreshes on `git pull` in the main checkout, or by hand, not on each commit.
  Installing its hooks would also write into our checked-in `.githooks` folder.
- *What it leads to:* a trial with no repo changes. If the graph is worth sharing or keeping
  history for, move to (b) without rebuilding anything.

**(b) One central repo, a folder per source repo, one branch.** Build as in (c), then copy each
repo's graph file (it records the commit it was built from) and the combined graph into a central
repo and commit.

- *Pros:* history, and the same graph on every machine.
- *Cons:* a new repo, a copy-and-commit step, and large JSON files churning in git.
- *What it leads to:* someone owns that repo and its step. Only worth it once the graph has proven
  useful.

**(a) One central repo, a branch per source repo.** As (b), with each graph on its own branch.

- *Pros:* each branch's history is that one repo's graph.
- *Cons:* a query across repos needs every branch checked out and joined, which graphify does not
  support. The source commit is already inside each graph file, so the branches add nothing.
- *What it leads to:* our own tooling to stitch branches together. Not recommended.

## 4. How sessions would ask it, and how it fits with what we have

- **Asking.** A session runs `graphify explain <name>` or `graphify query "<question>"`, or uses the
  optional MCP tools. A name with several matches is refused with the list of candidates, which is
  useful for SCHEMA_VERSION-style questions.
- **No strict hook.** Graphify can deny a session's first Read or Grep until it has queried the
  graph. That changes every session before we know it helps, so the trial leaves it off.
- **Who holds what.**

| Holds | Answers |
|---|---|
| The graph | who calls this, what imports this, how do these two connect (code only) |
| The FAQ | where a fact lives *and which one matters*, with checked pointers |
| CLAUDE.md | rules every session must follow |
| Memory | traps and decisions from past sessions |
| grep | anything else, always current |

- **The cheaper fix this doc also proposes (an idea).** The FAQ answers exist but are not reached.
  A one-line note in each repo's CLAUDE.md, "before grepping for a name, check docs/faq.md", or a
  hook that matches a grep against FAQ names and prints the answer, would test delivery directly.
  It belongs in the FAQ tool's own work, not here, but it should run before or beside the graph
  trial so the two results are not confused.

## 5. A cleanup skill fed by complexity and cycles

- **What graphify gives.** Import cycles: files that import each other in a loop, up to five long,
  listed in its report file. **No measure of how branchy a function is** (cyclomatic complexity).
- **What we already have.** bikar fails its lint above complexity 10 and already fails CI on any
  import cycle (`madge --circular`). qiyas has the same limit of 10 through ruff, with a list of
  files allowed to exceed it for now. So graphify adds nothing new for those two.
- **The real gap.** 3d-models' Python (`tools/`, `.claude/gates/`) has no complexity check at all.
- **Gate, not skill.** This repo's [precedent](dsl-extension-skill-evaluation.md) is that a proposed
  skill gets measured, and twice the answer was "no skill, a gate instead". The direct fix is a
  ruff complexity check in `make validate`, with the same limit as the siblings.

**Default:** a limit of 10 for 3d-models Python, the same number bikar and qiyas use, so a function
moved between repos is held to one bar. The source is bikar's lint setting,
[.eslintrc.cjs](https://github.com/NaqshCoffee/bikar/blob/main/.eslintrc.cjs), a convention
carried over rather than a value measured for this repo. It transfers because the three repos share authors and session habits, not because 10 was ever
tuned for this repo's gates.

- **What a cleanup skill would do (an idea, only if the gate leaves real work).** Read the lint's
  list of functions over the limit, plus bikar's cycle report, sort them by how often sessions
  touch those files, and propose one split per function as a PR. If that later proves a repeated
  manual task, extending the built-in `simplify` skill is cheaper than a new one.

## 6. The smallest first trial, and how to measure it

**The trial.** bikar only, code only (no AI model, no cost), version pinned, no hooks installed,
no strict mode, two weeks. Steps are in the research file, section 7. One line in bikar's CLAUDE.md
tells sessions it exists.

**The test build, 2026-11-06.** One code-only build of bikar main at `21420bc3`, on an exported
copy in a scratch folder (bikar's checkout untouched), with graphify 0.9.102. It answered the open
question, and the answer is half yes:

- **Exported module constants are entries.** All 299 exported upper-case constants in the `.ts`
  files under `packages/` are in the graph (constants that are not exported, camelCase ones and
  `.tsx`/`.js` files were not checked). For `FIT_GAP_MM`, `graphify explain` lists the 9 files that import it; plain grep
  finds 11, and the 2 extra only name it inside a string.
- **Static class fields are not.** `FILL_ATTRIBUTES`, a `private static readonly` set on the
  parser, is absent. Typed instance fields are kept as a list on the class (75 fields on 26
  classes), not as entries, so "who reads this field" has no answer.
- **The build:** 884 code files, 10,940 entries, 28,723 links (not timed). One parse error in
  `packages/core/src/dsl/parser.ts` at line 1363; extraction recovered past it (245 of the file's
  307 entries come after that line), but entries near it may be missing.

So of the six facts the trial answers one fully (tagSegments) and one in part (bikar's own schema
constant, not qiyas's contract one). FILL_ATTRIBUTES stays a FAQ answer. Constants being entries
also means the measure below can count constant lookups as well as function lookups.

**What we measure.** The six facts are mostly not code-symbol questions, so they cannot by
themselves show whether the graph helped. Instead count, in the FAQ tool's next run over bikar
sessions, how many re-searches are of *code symbols* (functions, methods, classes) before and
after, and how many sessions ran a graphify query at all.

**Validator:** after two weeks, rerun the FAQ tool's candidate count over bikar sessions. The graph
helped if re-searches of code symbols fell and sessions ran graphify queries in their place.

PASS: tagSegments-style lookups (functions, methods) drop, and the sessions where they would have
happened show a graphify query instead.

FAIL: the six facts drop to zero but the next batch is again settings, constants and ids, and no
session ran a graphify query. That means the FAQ helped and the graph did not, and a fall in the
total would have hidden it. Also a fail: code-symbol re-searches stay level although sessions query
the graph, meaning the answers were not good enough to stop the grep.

Removing it after a fail: `graphify uninstall --purge` in bikar and delete the exclude line.

## 7. Open questions for Omar

1. **Trial or skip?** The trial is cheap but answers a smaller question than the one asked: one
   fact in six. Skip is reasonable if the FAQ's delivery fix comes first.
2. **Should the graph see our docs?** That turns on the AI pass, which costs tokens and sends docs
   to the model. The trial keeps it off.
3. **Cross-repo link script.** Worth building only if the trial passes. Should it read the use-case
   map, so the map becomes the one list of cross-repo links?
4. **Complexity gate in 3d-models.** Add ruff's complexity check at 10 to `make validate`? This is
   independent of graphify and could go first.
