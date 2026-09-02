# Memory Index

- [autoMemoryDirectory setting](auto-memory-directory-setting.md) — relative paths and checked-in project settings are silently ignored; use an absolute `~/` path in `settings.local.json`
- [3D Models deploy](3d-models-deploy.md) — gh-pages diverged branch, OpenSCAD render + image pipeline
- [Islamic orb project](islamic-orb-project.md) — cross-repo orb build (bikar DSL 3D + qiyas + gallery). The dated shipped-record log (what merged, PR + sha, tenets) is the **Shipped record** section of that file; open work lives in the task system, which mirrors `docs/plan.md` (the working plan of record: objectives, priority queue, shipped, audit findings, links) — never here. Durable text cites stable ids (rung, CAL-*, D-number, PR + sha), never task numbers
- [bikar studio access](bikar-studio-access.md) — only public entry is bikar.naqshcoffee.com, gated behind org GitHub sign-in; internal audience, internet-reachable (settles the public-surface keystone)
- [gh auto-merge footgun](gh-auto-merge-footgun.md) — `--auto` merges immediately on NaqshCoffee repos; poll to green instead
- [3d-models use-case hook](3d-models-use-case-hook.md) — pre-commit dispatcher blocks pointer-file commits without map update; USE_CASES_OK=1 override
- [PR flow for all repos](pr-flow-for-all-repos.md) — every change (docs included) goes branch→PR→merge, never direct-to-master; marketplace repo is the exception
- [Stacked-PR stranding](stacked-pr-stranding.md) — never base a PR on another open PR's branch here; merge lands in the parent, not master, and strands it if the parent goes stale

Moved out of this repo's memory when auto-memory became per-repo (2026-08-16): `amazon-scripts-repo` → amazon-scripts, `marketplace-repo-mirror-and-held-branch` → oeid-claude-plugin-marketplace, `check-for-existing-e2e-before-reporting-blocked` and `supabase-paused-project-timeout` → bikar. Named without links because the files are no longer here and a dead relative link is a D1 gate failure.
