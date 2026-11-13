---
date: 2026-11-12
repo: 3d-models
session: monitor-print-watcher
branch: one-app-2a-notes, PR #1033 (paired with bikar #375 and #376)
folded: no
---

## Snags
- bikar `packages/lab/src/topbar.ts`: the Design and Print menus were separate `<details>` boxes, so both could be open at once and one list drew over the other. Omar caught it from a screenshot; no test or browser check had opened two menus. Giving the boxes one shared `name` fixed it with no script. A bar with more than one menu needs a check that opens one, then the other.
- bikar `make local.ci` failed on `check:jsdoc` after every test passed: a JSDoc summary ended in a closing quote. Running `npm run check:jsdoc` before the full suite would have saved a 20-minute rerun.
- `enable-page-comments --detect` guessed port 8000 for bikar, because the Studio's `dev` target hides its port. The always-on app (`vite preview` on 7136) also rules out the plugin's Vite mode, which is dev only. The right call, `--target http://127.0.0.1:7136 --port 7137`, came from the hubs port plan, not from detect.
- This session's worktree `3d-models-design` was removed by a tidy-up after #1033 merged, mid-session. A session that will keep working should start its next branch in the worktree before the merge tidy-up runs, or expect to add it back.

## Worth copying
- Serving the built Studio with `vite preview` on the always-on port, just for `enable.mjs --check`, proved the comment loop before the app's own PR (#374) had merged.
