---
name: bikar-build-and-test-traps
description: bikar monorepo traps that look like code bugs — stale core dist, worktree node_modules, vitest/Playwright cwd, eslint complexity cap, the --silent loglevel leak, CLI flags
metadata:
  type: feedback
---

- `packages/core/dist/` is gitignored; a stale build makes `npm run typecheck` in `cli`/`lab` fail with phantom missing-export or implicit-any errors. `npm run build` (core, knobs, qiyas-schema) first. A fresh worktree needs `npm ci` + `npm run build` before tsc/vitest resolve `@naqshcoffee/*`.
- A scratch worktree that symlinks the primary's `node_modules` resolves `@naqshcoffee/*` to the *primary's* packages. Build a real `node_modules` of per-entry symlinks with `@naqshcoffee/*` pointing into the worktree.
- vitest include patterns are repo-root-relative: run from bikar root. Playwright specs run from `packages/e2e`.
- Editing `constraints.ts` needs `bikar-knobs` rebuilt before the Lab sees it.
- eslint complexity cap is 10 with no disable allowed — extract helpers; `--fix` inserts an EMPTY JSDoc block that then fails `no-blank-blocks`, so write the comment.
- `npm run <x> --silent` exports `npm_config_loglevel=silent` to child npm and empties a gate's refusal message; pass `--loglevel=error` explicitly (bikar #146 `3daedd7`).
- CLI: output flag is `-o` (`--out` dumps binary STL to stdout); `--help` is unsupported.
- The starter-pattern bundle reads `patterns/**/*.bkr` verbatim via `import.meta.glob('?raw')`, so editing a `.bkr` needs no regeneration.
- Stale `__pycache__` in a Python gate can mask an edit; clear it when a change "does nothing".

**Why:** each of these cost a session a wrong diagnosis; none is visible from the error text.

**How to apply:** before debugging a type error in a sibling package, rebuild; before trusting a test run, check cwd and node_modules provenance. Related: [[bikar-dev-server-and-browser-checks]], [[git-and-gh-mechanics]].
