---
name: bikar-env-loader-pin-and-required-checks
description: "The global dotenvx on PATH is v1.71.3 (no `--format eval-export`); bikar reads .env only through the pinned npx 2.28.0 in scripts/lib/dotenvx.sh (PR #198). bikar main requires only ci, e2e, gitleaks; the rest are path-filtered."
metadata: 
  node_type: memory
  type: project
  originSessionId: 82a84811-d601-4caf-aeb6-288a0d47b1e9
  modified: 2026-09-17T15:24:59.032Z
---

Two facts established 2026-09-17 while answering "can we use our dotenvx secrets with a script to update CI secrets?":

- **dotenvx on PATH is the wrong build.** `~/.nvm/versions/node/v22.22.3/bin/dotenvx` is v1.71.3; its `get --format` knows only json/shell/colon/eval, so `--format eval-export` dumps JSON. bikar's `scripts/lib/load-env.sh` (the one reader behind `setup-secrets.sh`, `cf-verify.sh`, `cf-setup.sh`, `cf-token-probe.sh`, `cf-tunnel-verify.sh`) now sources `scripts/lib/dotenvx.sh` — the same `npx -y @dotenvx/dotenvx@2.28.0 … --no-native` pin `env-sync.sh` uses, plus `dotenvx_isolated` so an exported shell variable can never shadow the file value (bikar PR #198). Never call bare `dotenvx` in a bikar script; source the lib. `cf-tunnel-setup.sh` still takes a homebrew binary path for its owner-only calls.
- **Pushing secrets is `make setup-secrets`** (after `bash scripts/setup-secrets.sh --check`, which prints names and last-set timestamps only). It is shared CI state: Omar's go-ahead first. As of 2026-09-17 the GitHub `CF_ACCESS_CLIENT_ID/SECRET` were last set 2026-09-02 while the other four were set 2026-09-10 and the local `.env` dates from 2026-09-10 — the hypothesis for the failing deploy post-check (`check-deploy.sh` sees the Access login wall).
- **bikar branch protection requires only `ci`, `e2e`, `gitleaks`** (`gh api repos/NaqshCoffee/bikar/branches/main/protection/required_status_checks`). `coherence`, `orb-validate`, `calibration`, `sync-patterns` are path-filtered and may not run at all on a PR; a poll that waits for them times out. Merge on `gh pr view N --json mergeable,mergeStateStatus` → `MERGEABLE CLEAN`.

**Why:** the loader failed closed on a green `make env-check`, and a PR poll sat on four passing checks waiting for two that would never start — both look like a broken repo and are not.

**How to apply:** run the secrets check through `setup-secrets.sh --check`, not by hand; poll the three required checks only; see [[deploy-verification]], [[bikar-studio-access]], [[bikar-secrets-and-supabase]], [[gh-auto-merge-footgun]].
