# The FAQ tool counted sessions that used a fact, not ones that re-derived it

**Date:** 2026-09-25. **Affects:** `tools/session_reflect.py`,
[session-reflection-design.md](../session-reflection-design.md) §3, §4, §8,
the `session-reflect` skill.

## What was tried

The first build counted a session toward a fact when the assistant *typed* the
fact: it showed up in a command it ran, a thinking block, or a text block
("authored", as opposed to text that only came back in a tool result). Search
commands counted too, under the same rule: any `grep`, `rg` or `find`, seen in
three or more sessions, became a candidate question.

## What the first real run showed

`update-faq` over the 3d-models and bikar transcripts proposed **79 candidates**.
Almost none of them were questions:

- **The search candidates were routine outline scans**, not lookups:
  `grep ^##`, `grep export`, `grep def`, `grep function`, and `find .`. A grep
  for a heading marker or a keyword is how a session reads a file's shape. It
  is not a session hunting for a fact it should already know.
- **The fact candidates measured rule-following.** Every session is *supposed*
  to type the Node prefix `v22.22.3`. Counting that as re-derivation means that
  the better an answer works, the worse it scores.

To check the second point, a `census --context` run looked at the moment each
transcript file first used each fact. It asked what came in the 12 lines just
before that first use. Across both repos, very few first uses came right after
a failure:

| Fact | First uses | After a failure |
|---|---|---|
| D-id collision | 14 | 0 |
| THREED_MODELS_DIR | 23 | 0 |
| gitleaks | 53 | 5 |
| dotenvx | 25 | 2 |
| gh-pages | 33 | 2 |
| make validate is the only CI | 57 | 1 |
| npm install | 43 | 1 |
| use-cases hook | 32 | 3 |
| Node v22.22.3 | 97 | 1 (unrelated) |
| worktree add | 26 | 0 |

The Reads and searches before a first use were almost always about the task in
hand, not the fact. So sessions mostly *already know* these facts. The answers
in memory and CLAUDE.md are doing their job, and a count of "sessions that typed
it" cannot tell that apart from a problem.

## Why the approach changed

A measured FAQ is only worth keeping if it can say "this answer is not working."
Counting use can't do that, because use rises exactly when an answer works. The
count has to be of the thing the FAQ is meant to prevent: a session working
the fact out again.

## What replaced it

A session **re-derives** a fact when, at the first time that transcript file
authors it, one of two things happened just before (within 12 lines, or on the
same line):

- **failure:** a failed tool result names the fact. The use-cases hook's block
  message names USE_CASES_OK, so a session that learns the override from the
  block counts.
- **search:** it ran a `grep`/`rg` whose search term matches the fact.

Anything else is **knew it**, and does not count. A failure *after* the first
use does not count either: by then the session already had the fact.

Search candidates are narrowed the same way. Only `grep`/`rg` count, since
`find`'s first argument is a directory, not the thing sought. The search term
must name one specific thing: an identifier with an underscore (`BIKAR_DIR`),
camelCase (`patternSources`), or all caps and at least four characters long
(`UC23`).

Candidates, `show`, and the before/after verdicts all use re-derivation now.
"Used in N sessions" is still printed, but for context only.

## The rerun

Same transcripts, same bar (three sessions):

- **6 candidates, down from 79.** All six are greps for specific names:
  `SCHEMA_VERSION` (5 sessions), `BIKAR_DIR`, `patternSources`, `tagSegments`
  (4 each), `FILL_ATTRIBUTES` and `UCN` (3 each).
- **No fact probe reaches three sessions.** The most is "make validate is the
  only CI" at 2 (both by search, against 55 first uses where the session knew it).

`UCN` is not a literal term. The command shape folds digits, so greps for
different use-case ids (`grep -n "UC23" … catalog.ts`) land in one cluster. It
reads as "where does use case UC-nn live?", a family of lookups rather than one
fact. The reviewer decides whether that is one question.

## What the self-test now plants

The PASS fixture plants the fact learned from a hook's failure, learned by a
grep, learned inside a subagent, and one session that knew it and then hit a
failure afterwards (which must not count). It also plants a fact every session
types and none re-derives (which must not be proposed), and a `grep ^##` in
three sessions next to a `grep parseSeam` in the same three (only the second is
a candidate). Two mutants were run against it. One counts every first use as
re-derived; it fails 4 of the 12 checks. The other drops the subagent walk and
counts read-backs; it fails 7 of 12.
