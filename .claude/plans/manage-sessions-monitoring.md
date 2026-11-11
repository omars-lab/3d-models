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

## Open now (2026-11-10)

**Tidy-up Omar asked for on Nov 11 (approvals log, last two lines):**

- 3d-models done lists and both 3d-models plans are merged (#1003, #1004). Memory notes are merged
  (#1005-#1007).
- Old 3d-models branches: done. All eight squash-merged branches were checked by content, saved
  under `refs/snapshots/2026-11-10/` and deleted with `-D` on Omar's yes. Local branches left:
  master, gh-pages, next-work (monitor-print-watcher's, in `3d-models-else`) and manager-plan
  (this file's, in `3d-models-manager`). `3d-models-plate-notes` is plates-and-feedback's second
  folder, now on master.
- Store: the area plans are merged (storefront #500, d731138, 2026-11-11). All 63 old open items
  were accounted for: 53 carried over, 7 finished went to done.md, and the rest were narrowed or
  became headings. merge-pr-467-and-pr-470 now cleans up branches in the store and hub repos
  (3d-model-hub, 3d-model-hub-work) the same way, keeps `origin/feat/cup-bare-picture`, and
  removes its worktree. It was also asked whether a commit landed after c913cd4, which was the
  merged head.

**Waiting on Omar** (each in plain words in the session plan that owns it):

- cables-1: a yes in the plates-and-feedback tab, and a color.
- Judge closeout-1 and toys-1 on the hub (the :8766 links in plates-and-feedback's plan).
- The next coaster: a tick on the round 3 page
  (`docs/working-model/feedback-requests/2026-11-05-next-coaster-round-3.md`). Sixteen finished
  youtube videos wait on that pick.
- The spinner coaster's five choices, the whole-orb and fidget-toy design questions, and whether
  to stop the graphify code-map trial early (monitor-print-watcher's plan).
- Store: cup picks (gBV first, then n3I or sDO, then the round 24 lip color), the Jost font
  download (answered yes on Nov 10; the rebuild is the store session's), the other blank policy
  answers, the three Knowledge Base answers, removing the old naqshop app from the dev store, and
  deleting the stray naqshop-dev app in the EarlBear organization. The FAQ care line is OKed for
  the next live release he approves.
- Plate calls A to I: listed in [plates-and-feedback.md](plates-and-feedback.md).

**Next for customers:** CS-9, the nmEjCTzMbDg re-import (monitor-print-watcher; a bikar PR, then
a 3d-models PR). It is item 1 on the catalog-expansion backlog and unblocks the store's S4.3.
Alongside it: Omar's cup picks. They unblock the first real product files, and with them
the store's one-buy-button-per-pattern item ("Before opening"). That item can't start before then,
because every product file today is a test fixture. real-shoppers-store-launch owns both.
