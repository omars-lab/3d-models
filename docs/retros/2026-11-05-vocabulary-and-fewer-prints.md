---
date: 2026-11-05
repo: 3d-models
session: b317004f
branch: vocabulary-page, PR #898 (hub #25); fewer-prints-tenet, PR #900
folded: no
---

## Snags
- `.claude/skills/maintain-vocabulary/SKILL.md` "Looking at it": once merged, the live hub on
  4717 keeps running the old server code, so its new `/api/vocabulary` route 404s until someone
  restarts it, and the agent is refused the restart. The page needs a sanctioned restart path (a
  hub Makefile target, or a line saying Omar restarts it) rather than "shows it once merged".
- Hub main checkout: `git pull --ff-only` fails there because pull is set to rebase and the other
  session's page-comment thread files are uncommitted. `git fetch` then
  `git merge --ff-only origin/main` works and leaves them alone.

## Worth copying
- Keeping CLAUDE.md at 199 lines by rewriting the paragraph a new rule grew from, instead of
  adding a line beside it.
