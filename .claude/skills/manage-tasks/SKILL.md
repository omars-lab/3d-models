---
name: manage-tasks
description: Move tasks into the right file under docs/tasks/<loop>/. Use when Omar says to move completed or finished tasks to done, record what shipped, move open tasks (or the session task board) to the backlog, park something, or file a finding "in the right backlog"; also at the end of a loop pass when its item shipped or it found work it did not do. Picks the owning loop (coaster-pipeline, print-infrastructure, catalog-expansion, consolidation, or parked), writes done lines newest first with date and PR, deletes them from the backlog, and slots open work into the backlog in ROI order.
---

# Manage tasks — put each item in the right file

Every loop keeps two lists in `docs/tasks/<loop>/`: `backlog.md` (open, in ROI order) and
`done.md` (shipped, newest first). Work no loop owns lives in `docs/tasks/parked/`. The loop
table in [`.claude/loop-prompts/README.md`](../../loop-prompts/README.md) is the list of loops;
this skill only moves lines between those files. Which file an item belongs in is decided by
[`routing.md`](routing.md) — read it every run, it is kept apart so it can sharpen.

## 1. Gather the items

- **"Move completed tasks"**: finished items from the session task board (`TaskList`, status
  completed), plus anything the user names. For each, find the PR that shipped it
  (`gh pr list --state merged --search <words>`) and its merge date. No PR means it has not
  shipped — leave it open and say so.
- **"Move open tasks to the backlog"**: pending or in-progress board items, plus anything the
  user names or the pass found and did not do.

## 2. Route each one

Use [`routing.md`](routing.md) to pick one file per item. If an item already sits in some
backlog, the done line goes to *that* loop's done list, not wherever it would route fresh.
When two loops fit equally, pick one, and say which and why in the report — do not ask.

## 3. Write it

**A finished item** goes to `docs/tasks/<loop>/done.md`:

- one line, above the `## From the session task board, before the split` section and above
  older dated lines, so the newest is first:
  `- 2026-09-25 — <what shipped, in plain words> (3d-models #312)` — name the repo when the PR
  is not in 3d-models;
- then **delete** its entry from the backlog (the numbered item or bullet, with any
  sub-bullets), and renumber the list that remains. Never leave a struck-through or "done"
  line in a backlog.

**An open item** goes to `docs/tasks/<loop>/backlog.md`:

- under `## Open, in ROI order`, at the place its ROI puts it (the order rule at the top of
  that section, if the file has one), as a numbered item: a bold one-line title, then what
  it needs and where it came from ("found by the minis-01 run, 2026-09-25");
- work the loop may not take goes under `## Found elsewhere, maybe this loop's` instead;
- in parked, as its own `##` section with the same where-it-came-from line.
- Before adding, search every `docs/tasks/*/backlog.md` for the same work; if it is already
  there, add the new detail to that entry instead of a second copy.

## 4. What this skill never writes

- **Owner-gated work is Omar's to do, not ours to mark done**: a physical print, filament
  loading, `make setup-secrets`, a `schema-v*` tag, Cloudflare or GHCR settings. Put it in a
  backlog as waiting on Omar; never record it as done until he says it happened.
- **The FAQ review** (the untracked FAQ proposal in `docs/`) is Omar's. Do not write its answers into any list.
- The old snapshot sections in the done lists are history — do not edit them.
- The video-reconstruction loop's lists are in the youtube repo; route its items there and
  edit them in that repo.

## 5. Ship it

These are checked-in docs, so the change goes branch → PR → merge like any other: a worktree
off `origin/master`, stage the task files by name, `make validate`, open the PR. When the
item's own PR is still open, make the move in that PR instead of a separate one.

Report back as a short table: item → file → done or backlog, and anything left unrouted.
