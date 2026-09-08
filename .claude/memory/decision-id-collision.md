---
name: decision-id-collision
description: "two concurrent sessions grabbed the same next D-0xx id (both D-051, 2026-09-02); the open PR yields — first-merged owns the id, renumber the loser everywhere it is referenced"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 332d42c3-dfe9-490a-9db7-883074290c91
  modified: 2026-09-02T17:05:03.099Z
---

The `docs/decisions-log.md` id sequence (D-0xx) has no allocator, so two sessions
working at once each read the same "next free" number and both write it. On
2026-09-02 my `data-orb-base-face` decision and another session's open-shell
lattice orb both claimed **D-051**; the lattice PR (#155) merged first and its
D-051 is on master, so mine was renumbered **D-052** (#157) — the tenet + decision
landed as [D-052](../../docs/decisions-log.md).

**Why:** the collision surfaces as a *merge conflict in decisions-log.md* at the
shared insertion point, not as a clean error, and GitHub reported #153 as
`MERGEABLE/CLEAN` right up until the other PR merged — mergeability is a snapshot,
recheck it at merge time, not when the PR opened.

**How to apply:**
- **First-merged owns the id.** The PR still open yields and renumbers; never
  renumber what is already on master.
- **Renumber corpus-wide, like a K1 withdrawal.** `git grep -n "D-0NN"` before
  calling it fixed — the id appears in the heading, in CLAUDE.md tenet links, in
  UC-map anchors (`decisions-log.md:LNNNN "## D-0NN"`), in the design/issue docs
  that cite it, and in any already-merged doc that referenced it before the
  collision was known (here #154's issue doc line 4 had to be corrected in the
  same rebase).
- **Rebase, don't fight the conflict.** Take master's version of the id block and
  of any file the other session also re-pinned (they had run the UC-map refresh,
  moving line numbers), then re-apply only your semantic edit on top.
- The **squash-merge subject** keeps your local commit message, so it may still
  read the old id — cosmetic, and not worth a master history rewrite (force-push
  is classifier-blocked anyway). The *heading* and *references* are what matter.

Pair with [[stacked-pr-stranding]] and [[git-and-gh-mechanics]]; the force-push /
`gh pr merge` classifier blocks are in [[pr-flow-for-all-repos]].
