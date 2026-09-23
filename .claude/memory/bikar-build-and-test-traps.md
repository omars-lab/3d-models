---
name: bikar-build-and-test-traps
description: "bikar monorepo traps that look like code bugs — stale core dist, worktree node_modules, vitest/Playwright cwd, eslint complexity cap, the --silent loglevel leak, CLI flags"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-23T05:10:01.112Z
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
- Two whole-corpus core tests (`bbox-curve-bulge` "no pattern draws outside its own viewBox", `gt-emitter-face-provenance` "every face of every pattern") sit near vitest's 30 s default: they timed out and failed a pre-push `make local.ci-strict` while 3d-models' pre-push gitleaks scan and `make validate` ran on the same machine, then passed (59 s suite) on a quiet retry (2026-09-23). Don't run two repos' push gates concurrently; a "Test timed out in 30000ms" on those two is load, not code — retry before debugging.

**Why:** each of these cost a session a wrong diagnosis; none is visible from the error text.

**How to apply:** before debugging a type error in a sibling package, rebuild; before trusting a test run, check cwd and node_modules provenance. Related: [[bikar-dev-server-and-browser-checks]], [[git-and-gh-mechanics]].
