---
status: draft
date: 2026-09-30
produced-by: Claude (Opus 5.5), from a read of this repo at origin/master 5d0a4f0 and of youtube at refs/heads/main 30a2709
---

# Design: reconstruction intake, from a finished youtube rung to an import here

> Status: draft 2026-09-30, for Omar to decide the three calls in
> [Open calls for Omar](#7-open-calls-for-omar). Asked by Omar on 2026-09-30: "do we have a
> session start hook that keeps an eye on reconstructions/<id>/rung.yaml in ../youtube to look
> for completed reconstructions and properly imports them? do we have a skill to do this import?"
>
> Short answer: a session start hook exists, but it never reads rung.yaml and it imports
> nothing. The import skill exists, and it works one id at a time by hand. What is missing is
> the step between them: turning "done in youtube" into a ledger row and a place in the queue.

Every youtube fact below was read at youtube's `main` branch (commit 30a2709, 2026-09-30),
never from its working tree. The youtube repo has a remote today: `origin` is
`studio:git/youtube.git`.

## 1. What we have today

**The session start hook.** This repo's settings run the ledger gate in session mode at every
session start (`3d-models:.claude/settings.json:L16-L21 "--session"`). It prints two lines:
"N constructions not yet migrated" and "N youtube reconstructions have no ledger row". It took
0.28 s on this machine today.

**The ledger gate** (`.claude/gates/constructions_ledger.py`) decides what a reconstruction is
and whether it is done:

- A reconstruction is any youtube folder with a `construction.ggb-commands` file
  (`3d-models:.claude/gates/constructions_ledger.py:L218 "def youtube_recon_ids"`). It lists
  them at the ledger's youtube pin and at youtube's tip branch, read as a ref
  (`3d-models:.claude/gates/constructions_ledger.py:L239 "TIP_REFS"`). The L3 rule fails when
  one has no ledger row (`3d-models:.claude/gates/constructions_ledger.py:L36 "A youtube reconstruction with no ledger row"`).
  It reads both refs this way because a stale pin once hid `bknVRSMcLj0` for ten days
  ([the write-up](../issues/constructions-ledger-missed-new-reconstruction.md)).
- "Done" comes from youtube's task list (docs/tasks/done.md at the pin), and only as a text
  search: any id that appears anywhere in that file counts
  (`3d-models:.claude/gates/constructions_ledger.py:L250-L256 "cid in text"`).
- It never reads rung.yaml. It only reports and blocks; it writes nothing.

**The import skill** ([import-construction](../../.claude/skills/import-construction/SKILL.md))
migrates one construction by hand: GeoGebra, then a naqsh `.bkr` in bikar, then the three
oracles O1/O2/O3, a coaster, a catalog `CS-n` entry and a ledger row, ending in one bikar PR
and one 3d-models PR. Its step 0 picks the id from the [ledger](ledger.md)
(`3d-models:.claude/skills/import-construction/SKILL.md:L56 "### 0. Pick the id"`), in a fixed
ladder that names seven ids and then trails off. All seven are migrated now, so the named part
of that ladder no longer picks anything.

**Who decides what comes next.** The [catalog-expansion loop](../../.claude/loop-prompts/catalog-expansion.md)
takes "a finished reconstruction with no ledger row" first
(`3d-models:.claude/loop-prompts/catalog-expansion.md:L39 "A finished reconstruction with no ledger row"`),
and the [prioritize-design skill](../../.claude/skills/prioritize-design/SKILL.md) ranks the
candidates, reading them from "ledger rows done in youtube with no coaster"
(`3d-models:.claude/skills/prioritize-design/SKILL.md:L33 "Collect the candidates"`).

**youtube's side.** Since 30a2709, youtube keeps one reconstructions/<id>/rung.yaml per rung,
with two halves. `work` is kept by hand or by the rung script: `status` (queued, claimed,
in-progress, blocked, done), `blocked_by`, and `accepted_partial`. `synced` is written by
youtube's `make rung-sync` and never by hand: title, creator, `construction_digest`, and
`score` (verdict, passed/scored/steps, mean, the digest the score was made from, commit,
`fresh`). youtube's own rung script refuses `done` "unless the last score is a fresh PASS", or
a PARTIAL whose failing steps were examined and accepted with a written reason.

**The gap.** The hook does not read rung.yaml. Done-ness is read from a task list by text
search, not from the rung's own state file. And nothing turns "done in youtube" into a ledger
row and a place in the import queue. Three things show it today:

- The hook's "no ledger row" line lists `yZN_wn0uvTY`, which is **blocked** in youtube
  (PARTIAL 9/13). It cannot tell a finished rung from a stuck one.
- The ledger pin (e00730cd, 2026-09-29) predates rung.yaml: it has no rung files at all. youtube
  main is 50 commits ahead of it.
- The ledger's prose says `Y6kS1MvnKoc` scored short at 17/18; its rung.yaml now records
  PASS 18/18. The text drifted; the state file did not.

**Counted today, at youtube main.** 33 rungs: 32 done, 1 blocked. Of the 32 done, 31 are a
fresh PASS and one (`88q-u2eWZqg`, 6/9) is an accepted PARTIAL. 12 of them have a vendored
coaster here and one (`M60LJNNslHU`) is "no piece by design". That leaves **19 done in youtube
with no coaster**: 10 have a ledger row and 9 have none. For all 33, the digest of
construction.ggb-commands recomputed at the ref matches both digests in its rung.yaml.

## 2. What "completed" should mean

A rung is **completed** when all four hold, read from reconstructions/<id>/rung.yaml at
youtube's tip ref:

| field | test | what it guards against |
|---|---|---|
| `work.status` | is `done` | a rung someone is still working on, or one that is blocked (`yZN_wn0uvTY`) |
| `synced.score.verdict` | is `PASS`, or is `PARTIAL` with `work.accepted_partial` set | an unexamined partial score passing as finished |
| `synced.score.fresh` | is true | a score made from an older draft of the construction |
| the digest | sha256 of construction.ggb-commands at the same ref, first 12 hex, equals `synced.construction_digest` and `synced.score.construction_digest` | a rung.yaml whose synced half lags the construction beside it |

The first three repeat youtube's own rule for `done`, on purpose: if youtube changes that rule,
we read the same fields. The fourth is ours. youtube's pre-commit rung check (run with `--staged`)
compares the synced half only for the rungs a commit stages, so a rung.yaml can in principle
lag its construction. Recomputing the digest costs one `git show` per rung.

"Not yet imported" means: completed, **and** no ledger row names a `.bkr`, **and** the row is
not "no piece by design". A row that is missing counts as not imported.

Read at a ref, never the working tree. youtube's working tree may be on any branch, mid-edit
by another session. The gate already reads refs this way (`TIP_REFS`: `refs/heads/main`, then
`master`, then `origin/HEAD`); the intake reuses those helpers, so there is one youtube reader,
not two.

## 3. Options for the watch

| | (a) Extend the gate's session line | (b) A small intake tool, one reader for hook and make | (c) Auto-import at session start |
|---|---|---|---|
| What it is | `constructions_ledger.py --session` reads rung.yaml and prints "done in youtube, not in the ledger: ids", with score and creator | tools/reconstruction_intake.py: a read-only list for the hook, and a write mode (run by hand or by the loop) that adds ledger row stubs and moves the pin | the hook runs the import skill for each completed rung |
| Pros | Smallest change; no new file | The list and the fix live together, so a row is never owed for long; `make` and the loop call the same code; the gate stays a checker | Nothing to remember |
| Cons | A checker that also plans work mixes two jobs; still leaves the row stubs to be typed by hand | One new file and a make target | An import is one bikar PR and one 3d-models PR, oracles, and minutes of work that ends at Omar's merge |
| Implications | Rows keep going unwritten until someone types them, as the 9 missing today show | Step 0 of the import skill and prioritize-design both read one list | Wrong here: a hook must finish in seconds, must not write to another repo, and must not open PRs in a shared checkout another session uses |

**Recommendation: (b).** It closes the gap at its cause (rows nobody writes) while the session
hook stays read-only and fast.

## 4. The import skill

`import-construction` already does the import. It stays the only import skill. What changes is
where it gets its next id:

- **Step 0** reads the intake tool's list (completed, not yet imported) instead of the fixed
  seven-id list. One candidate: take it. More than one: take the pick from the latest
  prioritize-design round. If no round covers them, run prioritize-design first.
- **prioritize-design**'s "Collect the candidates" reads the same list, so the 9 rungs with no
  ledger row are no longer invisible to it.
- **Step 7** loses two stale claims: the ledger hook is `44-constructions` (it says hook 38),
  and a missing row now fails L3 (it says the gate only reports one)
  (`3d-models:.claude/skills/import-construction/SKILL.md:L182 "hook 38"`).

Not to build: a second import skill, a "bulk import" mode, or a hook that starts an import. The
ordering is a taste call and belongs to prioritize-design; youtube's `make ladder` screens
videos to study and is not an import order.

## 5. The ledger pin

The ledger pins one youtube commit ([ledger.md](ledger.md), the "Youtube pin" line). Every
youtube cell is read there. A pin that falls behind hides new reconstructions; that is how
`bknVRSMcLj0` went unledgered in September. L3 now also reads the tip, but the youtube column
is still dated to the pin.

Proposal: **the intake tool's write mode moves the pin.** It sets the pin to youtube's tip,
adds a stub row for each rung the tip has and the ledger lacks, and fills each stub's youtube
cell from its rung.yaml `work.status`. That lands as one small 3d-models PR. Each import PR
also moves the pin to the tip it read, as L3 already forces whenever a row is added.

What the gate checks, once the pin is at 30a2709 or later:

- The youtube cell of every row matches its rung.yaml status at the pin (replacing the text
  search in done.md). A row that says done while its rung says blocked fails.
- The pin is an ancestor of youtube's tip ref, so the pin cannot sit on a side branch.
- L3 stays as it is: a rung at the tip with no row fails. The write mode is what makes that
  failure a one-command fix.

## 6. What would need building

Smallest first. Each ships with the test that fails before it and passes after.

1. **Stale sentences.** The gate's "youtube has no remote today"
   (`3d-models:.claude/gates/constructions_ledger.py:L237 "remote today"`), the ledger's "no
   remote" (`3d-models:docs/constructions/ledger.md:L14 "no remote"`), step 7's hook number and
   "reports", and the same two in the umbrella design
   (`3d-models:docs/constructions/geogebra-construction-import-design.md:L333 "without"`).
   A doc correction, no test.
2. **The rung reader and the completed test**, in tools/reconstruction_intake.py, reusing the
   gate's youtube helpers. Test: a self-test builds a scratch youtube repo with five rungs
   (fresh PASS, accepted PARTIAL, done with a FAIL verdict, done with a stale digest, blocked);
   only the first two come back.
3. **The list** (`--list`, `--session`) and a `make intake` target running the self-test then
   the list. Test: in the scratch repo, a rung with a migrated row and a "no piece by design"
   row are both absent.
4. **The hook** in `.claude/settings.json` calls the intake tool's session mode in place of the
   gate's. Test: the self-test asserts session mode prints nothing when nothing is owed and
   writes no file.
5. **Step 0 and prioritize-design** read the list (prose). Check: run step 0 once against
   youtube main and see it name one of today's 19.
6. **The write mode** (`--write`, in a worktree only): stub rows, pin to tip, the
   `constructions-total` count. Test: after `--write`, the gate passes L3 on the scratch
   ledger; a second `--write` changes nothing.
7. **The gate's youtube column** reads rung.yaml at the pin instead of done.md, plus the
   ancestor check. Test: a done.md that mentions an id only as "attempted" no longer makes it
   done (fails today, because of the text search), and a row saying done over a blocked rung
   fails.

## 7. Open calls for Omar

**Call 1. How to watch.** (Section 3 has the full table.)

- [ ] **(b) A small intake tool, read-only at session start, writes on request (recommended).**
  Pros: rows get written by one command; one reader of youtube. Cons: one new file. Implies:
  build items 1 to 7.
- [ ] **(a) Only extend the gate's session line.** Pros: least code. Cons: rows are still typed
  by hand. Implies: the reader (item 2) goes into the gate, item 6 is dropped, and the 9
  missing rows stay a chore.
- [ ] **(c) Auto-import at session start.** Pros: nothing to remember. Cons: slow, writes to
  bikar, opens PRs from a hook. Implies: a session start hook that runs for minutes and
  writes to two repos. Not recommended.

**Call 2. When the pin moves.**

- [ ] **At every intake write, and at every import PR (recommended).** Pros: the pin trails
  youtube by at most one intake run. Cons: more small PRs. Implies: the loop's "take stock" step
  runs the write mode.
- [ ] **Only at import PRs.** Pros: fewer PRs. Cons: between imports the pin lags and L3 keeps
  failing on new rungs. Implies: rows are owed for days at a time, as today.

**Call 3. Does an accepted PARTIAL count as completed?**

- [ ] **Yes, as youtube's own `done` rule says, marked "accepted partial" in the list
  (recommended).** Pros: one meaning of done across both repos. Cons: `88q-u2eWZqg` (6/9) joins
  the queue. Implies: the oracles here still judge the import on its own.
- [ ] **No, fresh PASS only.** Pros: a stricter queue. Cons: two meanings of done; `88q-u2eWZqg`
  never enters the queue unless someone overrides it. Implies: a second rule to keep in step
  with youtube's.

## 8. Validator

**Validator:** the intake tool's list, run against youtube `main`, names exactly the completed
rungs that have no coaster here: no row naming a `.bkr`, no "no piece by design" row, and no
`src/Coasters/<id>*-standard.stl` file of any style.

PASS: run today, it lists 19 ids. `NtnlGMTElBk`, which has a coaster, is absent.
`M60LJNNslHU`, done and PASS but "no piece by design", is absent. `yZN_wn0uvTY`, blocked, is
absent. `88q-u2eWZqg` is present, marked accepted partial.

FAIL: a scratch rung with status done but verdict FAIL appears in the list. The hard case is a
rung whose status says done and whose verdict says PASS but whose construction changed after
the score: its digest no longer matches, and it must be left out.
