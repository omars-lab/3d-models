---
name: pr-flow-for-all-repos
description: "All changes to every repo — including docs-only 3d-models commits — go through a PR, never direct-to-master"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 27e89d38-2159-4b95-9416-70151c40cbd0
  modified: 2026-08-06T15:44:07.432Z
---

Route **every** change through a branch → PR → merge, in all repos, **including docs-only commits to 3d-models**. Do not push directly to `master`/`main`.

**Why:** the standing directive is "merge everything back to main via prs" so work-tree changes are not lost and there is a review surface. On 2026-08-06 the #104 docs half was pushed straight to 3d-models master (`03facc4`) while the bikar half correctly went through PR #79; asked how to handle it, the user chose "Leave it, PR next time" — i.e. accept that one, but PR going forward, docs included.

**How to apply:** for any repo change, create a branch, open a PR, let CI/gates go green, then merge. Never `git push origin master` with local commits that never saw a PR. Docs-only is NOT an exemption. See [[islamic-orb-project]] for the #104 context and [[gh-auto-merge-footgun]] for the merge-timing trap (poll to green, don't `--auto` blindly).
