---
name: amazon-scripts-repo
description: "~/Workspace/git/amazon-scripts (renamed from work-scripts 2026-08-11) — 2022-era personal tooling repo, now backed up to mac-studio:git/amazon-scripts.git; working tree still dirty with an uncommitted 24-file reorg"
metadata: 
  node_type: memory
  type: project
  originSessionId: 27e89d38-2159-4b95-9416-70151c40cbd0
  modified: 2026-08-11T23:42:45.404Z
---

`~/Workspace/git/amazon-scripts` was `work-scripts` until 2026-08-11, when the user renamed it and asked for a mac-studio remote (closing task #85 — its history had existed only on this disk). Now: `origin = mac-studio:git/amazon-scripts.git` (bare repo created that day), branch `master` pushed and tracking. Gitleaks scanned the full 4-commit history clean before the first push.

Contents: 2022-era tooling — `tools/` (29), a modular zsh plugin system (`sh-plugins/`, `sh-plugins-common/`, `sh-plugins-extensions/`), `python-scripts/`, `jq-scripts/`, `monitoring-portal/`, `greasemonkey/`, `archive/`, `bin/rmb-curl`. Last commit "Cleaning things up" (2022-04-22).

The long-uncommitted reorg (26 entries — all of `sh-plugins-common/` and `sh-plugins-extensions/` deleted, a **pure 374-line deletion**, not a move) was committed on user request as `bd5fae4` and pushed 2026-08-11; the tree is now clean. The deleted content remains recoverable at `b14df24`. See [[pr-flow-for-all-repos]] — this personal repo has no PR flow; direct push to the private mac-studio remote is the norm.
