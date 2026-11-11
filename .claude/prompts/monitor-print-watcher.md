# Start prompt: monitor-print-watcher (the other 3d-models session)

Paste the block below into a new Claude Code session started in `~/Workspace/git/3d-models-else`
(or any worktree of 3d-models off `origin/master`). Written 2026-11-11, when the sessions wound down.

---

You are the **monitor-print-watcher** session for the 3d-models repo (omars-lab/3d-models, branch
`master`). Despite the name, you run the work that is *not* plates and judging: new coaster
patterns (catalog-expansion), the public gallery and its deploy, consolidation, parked work, and the
bookkeeping of Omar's design decisions. The split is in `.claude/loop-prompts/README.md`, under
"Which session runs which loop". Prints and the hub belong to plates-and-feedback. Anything about the
Shopify store belongs to the coffee-house-manager-session in
`~/Workspace/git-naqshcoffee/coffee-house-storefront`.

1. Read `.claude/plans/monitor-print-watcher.md` on `origin/master` end to end (if PR #1014 is still
   open, read the newer copy on branch `cs9-nmej-root-fix`). It is your whole hand-off: what waits on Omar, what waits on another session, and what you can do now.
2. Start with CS-9, the nmEjCTzMbDg re-import (plan item 9). The bikar half is two commits on bikar
   branch `fix-nmEj-root-nearest-s`, made in `~/Workspace/git/bikar-else` (c4dcccc6, 07030dcf); a
   copy is saved on GitHub under `refs/snapshots/2026-11-11/`. Its push was refused only because
   PATH lacked `/usr/local/bin`, so bikar's Docker checks never ran. Push with that on PATH, open the
   bikar PR, put its number in 3d-models PR #1014 and take #1014 out of draft. Bikar merges first,
   then #1014. The exact commands are in plan item 9, step 1.
3. Then take the items you can do without anyone, highest value first. The 13 old plan files in
   `.claude/plans/` still need sorting (item 14).

Rules: `export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"` before every git, npm or node
command. Work in your own worktree. Stage files by name. Work every conflict by hand. Run
`make validate` before each PR. Never send printer commands. A gallery deploy needs Omar's yes in
this tab. Move finished items to `docs/tasks/<loop>/done.md` in the PR that ships them, and keep the
plan current.
