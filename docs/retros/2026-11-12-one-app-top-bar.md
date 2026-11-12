---
date: 2026-11-12
repo: 3d-models
session: monitor-print-watcher
branch: one-app-bar, PR #1025 (paired with bikar #372)
folded: no
---

## Snags
- bikar's pre-push suite: a page-wide `a[href="/posts"]` selector in `packages/e2e/tests/posts-page.spec.ts` broke once a shared top bar linked the same page. A test that finds a link on a page should name the element it means (`a.card[...]`), not just the address.
- bikar `packages/e2e/tests/studio-dials.spec.ts` "a dial drag writes the param line" failed once in the full pre-push run and passed 3 of 3 alone. It was not flaky: repeated 30 times it failed 4, because `packages/web/src/main.ts` swapped in the disk copy of the patterns over any early edit. Fixed in bikar #373, with a test that holds the disk copy back. A test that fails "only under load" is worth one repeated run before it is called flaky.
- `make deploy` copies only `DEPLOY_PATHS` and never deleted a page dropped from it, so removing `studio.html` from the list would have left it live. Caught by building the public Lab copy, not the Studio one; fixed with `RETIRED_PATHS` in #1027.
- `.claude/skills/maintain-use-cases/validate.py --refresh` after a sibling merge reported 12 moved anchors at once; `--repair` moved 9, and the 3 whose text was gone (a route moved from `vite.config.ts` into the page list) needed a hand edit.

## Worth copying
- Replacing a removed link on `index.html` with a one-line comment kept every line number the site graph anchors on, so no other edge moved.
- Holding the 3d-models half until the bikar half merged meant the gallery never stopped listing a page bikar still built.
