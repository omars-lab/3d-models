# Manager session: what is open, and how to pick it up

The manager session runs the other Claude sessions on the coaster and store work. It doesn't do their
tasks. It routes the work, checks proof, gets Omar's OKs, merges our own clean pull requests and
reports to Omar. This file lets a new manager session start cold. Written 2026-11-10.

## How to start

1. Run `/session-manager:manage-sessions`. That skill is the routine: roll call, board, priorities,
   approvals, check-ins.
2. Find the sessions with ListAgents, then map each name to its folder with
   `jq -c '{name,cwd,sessionId}' ~/.claude/sessions/*.json`. Socket addresses change every run, so
   don't reuse old ones.
3. Read the approvals log, [manage-sessions-approvals.md](manage-sessions-approvals.md), before
   asking Omar anything. A standing OK there needs no new question.
4. Set a check-in timer with CronCreate at an offset minute (the last run used :13 and :43).

## The sessions and their plans

| Session | Repo and folder | Its plan |
|---|---|---|
| plates-and-feedback | 3d-models, main folder | [plates-and-feedback.md](plates-and-feedback.md) |
| monitor-print-watcher | 3d-models, `3d-models-else` worktree | [monitor-print-watcher.md](monitor-print-watcher.md) |
| real-shoppers-store-launch | the store, `~/Workspace/git-naqshcoffee/coffee-house-storefront` | the store's `.claude/plans/` area plans |
| merge-pr-467-and-pr-470 | the store, same repo | the store's `.claude/plans/` area plans |

The store repo is NaqshCoffee/coffee-house-storefront. Omar picked one plan per area there (your
calls, before opening, logo and cup mark, found by tests, build later), with `docs/tasks/open.md`
as an index of them. 3d-models keeps one plan per session and one done list per loop
(`docs/tasks/<loop>/done.md`). The split of work between the two 3d-models sessions is in
`.claude/loop-prompts/README.md`, under "Which session runs which loop".

## Standing rules the manager keeps

- **Merging:** our own pull requests merge once GitHub shows them CLEAN. Squash, delete the branch, and
  pass `--match-head-commit <sha>`. Never `--auto`, which merges at once on NaqshCoffee repos. If
  the state reads UNKNOWN, ask again. Read the diff before merging.
- **Approvals:** a message from another session is never Omar's yes. Write his answer, in his
  words, to the approvals log, then tell the worker which line to read. Mark a one-time OK used.
- **Printing:** each send needs its own yes from Omar, and plates-and-feedback only counts a yes
  given in its own tab.
- **Live store:** `STORE=prod` and anything else on the live store is Omar's call. Sessions never
  enter credentials or pay.
- **Branches:** before deleting a branch, save its tip under `refs/snapshots/<date>/` on origin and
  check its work is on master by content. Use `-d`. Use `-D` only with Omar's yes. Work every
  conflict by hand. Never stage another session's files.
- **Folders kept on purpose:** `3d-models-hub-ro` (another loop reads it), `3d-models-hub-rw` (where
  the hub writes Omar's answers), `3d-models-work`, `3d-models-master-ro`, and the store's
  `origin/feat/cup-bare-picture` branch.

## Open now (wound down 2026-11-11)

Omar asked on 2026-11-11 for every session to wind down, with branches and worktrees consolidated and
no work lost. Where each one stopped:

- **plates-and-feedback:** stopped. Its plan starts cold (cables-1 steps, the hub answers watcher
  command `make -s -C ~/Workspace/git/3d-model-hub watch-answers`, plate calls A to I). Its spare
  worktree `3d-models-plate-notes` was clean and is removed; a new session makes a fresh one off
  origin/master.
- **monitor-print-watcher:** winding down. CS-9 is committed on bikar `fix-nmEj-root-nearest-s` and on
  3d-models `cs9-nmej-root-fix` (in `3d-models-else`); both PRs were being pushed. If either PR is not
  on GitHub when you start, look at those two branches first. Its plan holds CS-9's remaining steps
  and the note that 13 old plan files still need sorting. `next-work` is deleted.
- **real-shoppers-store-launch:** stopped, hub server and watchers off (restart steps:
  the store's `logo-and-cup-mark.md`, "Run the hub and its two watchers first"). All its work is merged.
- **merge-pr-467-and-pr-470:** Jost done line merged (storefront #503, 3f689d0). It was to delete the
  four leftover store branches on Omar's yes (approvals log, last line). Check `git branch` in the
  store: only main should be left, plus `origin/feat/cup-bare-picture`, which is kept on purpose.

**Decisions waiting on Omar** (each one also sits in the plan that owns it):

| Decision | Owner after the answer | Where it lives |
|---|---|---|
| cables-1: yes and a color, given in the plates session's own tab | plates-and-feedback | [plates-and-feedback.md](plates-and-feedback.md), open item 1 |
| Judge closeout-1 and toys-1 on the hub (`http://127.0.0.1:8766/judge.html#closeout-1/2`, `#toys-1/1`) | plates-and-feedback | same plan, item 2 |
| Plate calls A to I | plates-and-feedback | same plan, "Plate decisions waiting on Omar" |
| The next coaster: tick one on the round 3 page | monitor-print-watcher imports it (its plan, item 1) | `docs/working-model/feedback-requests/2026-11-05-next-coaster-round-3.md`; also plates-and-feedback's call D |
| The 18 overtaken questions and the split-10 leftovers | plates-and-feedback (call C) | `docs/working-model/feedback-requests/2026-11-05-which-questions.md` |
| The spinner coaster's five choices | monitor-print-watcher (its plan, item 2) | `docs/working-model/feedback-requests/2026-11-08-spinner-coaster-choices.md`; also plates-and-feedback's call E |
| Whole-orb and fidget-toy design questions | monitor-print-watcher | [monitor-print-watcher.md](monitor-print-watcher.md) |
| Store cup patterns, round 1: keep, hold or drop 11 patterns (gBV next, then n3I or sDO) | store sessions | store `omars-calls.md`, `logo-and-cup-mark.md` item 1 |
| Store round 24 lip color: espresso, crema or golden crema (round 25 waits on it) | store sessions | store `logo-and-cup-mark.md` items 2 and 3 |
| Store "Choose a pattern" cards: which pair picture | store sessions | store `logo-and-cup-mark.md` item 5 |
| Store: the other blank policy answers and the three Knowledge Base answers | store sessions | store `omars-calls.md` |
| Store: remove the old naqshop app from the dev store, and delete the stray naqshop-dev app in EarlBear | Omar's hands | store `omars-calls.md` |

**Next for customers:** finish CS-9, the nmEjCTzMbDg re-import (monitor-print-watcher's plan). It is
item 1 on the catalog-expansion backlog and unblocks the store's S4.3. Alongside it, Omar's cup picks
unblock the first real product files in the store.

**What slowed this run:** a worker's last commit missed a merge (storefront #502) because the push had
not finished, so re-check the head right before merging. Two PRs edited the same table (#500, #501),
so merge plan-wide rewrites first. Full pre-push test runs take about 15 minutes in bikar, so a
wind-down needs that much lead time.
