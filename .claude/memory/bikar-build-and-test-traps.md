---
name: bikar-build-and-test-traps
description: "bikar monorepo traps that look like code bugs — stale core dist, worktree node_modules, vitest/Playwright cwd, eslint complexity cap, the --silent loglevel leak, CLI flags"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-04T03:25:45.723Z
---

- `packages/core/dist/` is gitignored; a stale build makes `npm run typecheck` in `cli`/`lab` fail with phantom missing-export or implicit-any errors. `npm run build` (core, knobs, qiyas-schema) first. A fresh worktree needs `npm ci` + `npm run build` before tsc/vitest resolve `@naqshcoffee/*`.
- bikar's bare `make build` is the **Docker** image build (fails on the package token), not the TypeScript build. The TS build is `make local.build`; the full check is `make local.build local.ci`. Wrong target cost one wasted run on 2026-09-28.
- A scratch worktree that symlinks the primary's `node_modules` resolves `@naqshcoffee/*` to the *primary's* packages. Build a real `node_modules` of per-entry symlinks with `@naqshcoffee/*` pointing into the worktree.
- vitest include patterns are repo-root-relative: run from bikar root. Playwright specs run from `packages/e2e`.
- Editing `constraints.ts` needs `bikar-knobs` rebuilt before the Lab sees it.
- eslint complexity cap is 10 with no disable allowed — extract helpers; `--fix` inserts an EMPTY JSDoc block that then fails `no-blank-blocks`, so write the comment.
- `npm run <x> --silent` exports `npm_config_loglevel=silent` to child npm and empties a gate's refusal message; pass `--loglevel=error` explicitly (bikar #146 `3daedd7`).
- CLI: output flag is `-o` (`--out` dumps binary STL to stdout); `--help` is unsupported.
- The starter-pattern bundle reads `patterns/**/*.bkr` verbatim via `import.meta.glob('?raw')`, so editing a `.bkr` needs no regeneration.
- Stale `__pycache__` in a Python gate can mask an edit; clear it when a change "does nothing".
- Two whole-corpus core tests (`bbox-curve-bulge` "no pattern draws outside its own viewBox", `gt-emitter-face-provenance` "every face of every pattern") sit near vitest's 30 s default: they timed out and failed a pre-push `make local.ci-strict` while 3d-models' pre-push gitleaks scan and `make validate` ran on the same machine, then passed (59 s suite) on a quiet retry (2026-09-23). Don't run two repos' push gates concurrently; a "Test timed out in 30000ms" on those two is load, not code — retry before debugging. **Fixed 2026-09-25 (bikar #247):** both now carry a 120 s budget, since the corpus (151 files) had grown enough that even a lone full-suite run tripped 30 s. If they time out again, raise the budget in the test, not by retrying. **Superseded 2026-10-03 (bikar #302):** they are now split into one test per pattern, so no single test walks the whole corpus; a timeout now names the one slow pattern — debug that file. The pre-push `--strict` run also needs Docker up (`open -a Docker`, wait for `docker info`), or five orb-sweep steps are NOT VERIFIED and the push is refused.

**Why:** each of these cost a session a wrong diagnosis; none is visible from the error text.

**How to apply:** before debugging a type error in a sibling package, rebuild; before trusting a test run, check cwd and node_modules provenance. Related: [[bikar-dev-server-and-browser-checks]], [[git-and-gh-mechanics]].

## From the memory index (moved 2026-10-09)

stale core dist, worktree node_modules, vitest/Playwright cwd, eslint complexity 10, `--silent` loglevel leak, CLI `-o`; the whole-corpus tests are split per pattern since bikar #302 (a timeout names the slow pattern), and never run two repos' push gates at once

## The push gate needs docker on PATH (2026-10-25)

bikar's pre-push runs `make local.ci-strict`, which probes `docker info` and fails the push with five "NOT VERIFIED (docker unavailable)" orb-sweep steps when it cannot. `docker` is `/usr/local/bin/docker`, so a pinned PATH without `/usr/local/bin` fails the push even with Docker Desktop running. Start Docker (`open -a Docker`) and keep `/usr/local/bin` in the PATH.

## The main bikar checkout is too old to slice split-07/09 (2026-10-27)

`~/Workspace/git/bikar` sat at 7d5990a and is another session's: never fast-forward it. It rejects the split flange coaster's `stud` params ("Unknown param override 'stud'"). Slice split-07 or split-09 with `BIKAR_DIR` pointing at a bikar clone at 112d257 or newer, including any re-slice at send time.
