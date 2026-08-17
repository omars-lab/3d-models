---
name: stacked-pr-stranding
description: "Don't stack a PR on another open PR's branch in these repos — merge lands it in the parent branch, not master, and strands it if the parent goes stale"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 792c03e6-3f91-4133-a2ea-35c8bfde5227
  modified: 2026-08-06T20:18:34.771Z
---

When work depends on an unmerged PR, do **not** open the child PR with `--base
<parent-branch>`. On these repos (squash-merge, no CI), merging the child then
lands it **into the parent's branch, not master**. If the parent later goes
stale and is closed, the child's content is stranded off master even though the
PR shows MERGED.

**Why:** happened 2026-08-06. #37 (a real GIT_DIR hook-hole fix) was stacked on
#36's branch. #37 merged — into #36's branch. Concurrent sessions then landed
#38/#39, which superseded #36's doc content, so #36 was closed. #37's unique fix
had never reached master and had to be rescued: cherry-pick onto fresh master,
re-anchor the drifted use-case pointers, re-open as #55, close #36.

**How to apply:** base every PR on `master`. If it truly can't stand alone until
another lands, keep the branch local and unpushed until the dependency merges,
then rebase onto fresh master and open against master. See [[pr-flow-for-all-repos]].
The GIT_DIR hole itself is why isolated worktree work was silently under-checked
— linked-worktree hooks get `GIT_DIR` set, which made the use-case validator
skip all sibling pointers and exit 0; fixed in #55.
