# Memory Index

- [autoMemoryDirectory setting](auto-memory-directory-setting.md) — relative paths and checked-in project settings are silently ignored; use an absolute `~/` path in `settings.local.json`
- [3D Models deploy](3d-models-deploy.md) — gh-pages diverged branch, OpenSCAD render + image pipeline
- [Islamic orb project](islamic-orb-project.md) — hub for the cross-repo orb build (bikar DSL 3D + qiyas + gallery): repo roles, where open work and the archived ship log live (`docs/research/shipped-record.md`), and the index of topic memories below
- [Orb repo roles](orb-repo-roles.md) — who owns what across bikar/qiyas/3d-models/sacred-patterns; `make orbs` globs only `patterns/Orbs/`, presets are claimed in three places
- [bikar build and test traps](bikar-build-and-test-traps.md) — stale core dist, worktree node_modules, vitest/Playwright cwd, eslint complexity 10, `--silent` loglevel leak, CLI `-o`
- [bikar dev server and browser checks](bikar-dev-server-and-browser-checks.md) — Lab on :4613, `lsof` + `--host 127.0.0.1` before trusting localhost, a real-browser check is part of shipping a page
- [git and gh mechanics](git-and-gh-mechanics.md) — bad pathspec aborts the whole add, force-push denied, local `--delete-branch` fails while the remote merge succeeded, branch fresh off origin/main
- [Use-case map mechanics](use-case-map-mechanics.md) — `--refresh` re-pins hashes but never moves lines; fetch the sibling first; cite bikar by PR not relative link; new Makefile targets at the END
- [Docs gate quirks](docs-gate-quirks.md) — bare `PASS:`/`FAIL:`, C4 checks the list, research/ exempt, an absence rule is not a coverage rule
- [Deploy verification](deploy-verification.md) — verify at the bundle not the green run; studio targets Cloudflare `bikar-studio`; deploy on main currently fails on a token permission
- [Calibration baseline trailer](calibration-baseline-trailer.md) — `Calibration-Baseline-May-Grow:` must be one line in the tip commit's final paragraph
- [qiyas runtime and gates](qiyas-runtime-and-gates.md) — orb-validate needs the `:dev` image, CI is the score authority, FastAPI only (never Flask), which score fields mean what
- [Contract and schema mirror](contract-and-schema-mirror.md) — sacred-patterns canonical, qiyas exports, bikar vendors byte-identical, hook 41 compares copy to source at the map's pins
- [Orb kernel facts](orb-kernel-facts.md) — no boolean union, weave is the only crossing resolution, genus = tunnels−1, earcut reflex fillers, aggregates cannot discharge per-part claims
- [Woven orb clearance](woven-orb-clearance.md) — D-039/D-040: the amplitude rule was about centrelines, clearance gated at 0.4 mm (CAL-CLR-01), range endpoints are the least-tested values
- [Maclado family facts](maclado-family-facts.md) — Family 3 by decision id D-030…D-033/D-040/D-044, the divisor trick, and the open taste call
- [Breakdown page instrument](breakdown-page-instrument.md) — projector gaps are artifacts, `display/` shield killed by D-041, re-record order hashes last, wrap-morph is a radial lerp
- [Orb Lab conventions](orb-lab-conventions.md) — knobs are DSL params, touched-set overrides, print target never in share URLs, knobs live in packages/knobs, walls via custom script only
- [Composition and wall facts](composition-and-wall-facts.md) — clips never route through connect, clip exempt from the FDM floor, mural STL fails `--check` by design, `crop stretch` unshipped
- [Lego Lab and LDraw facts](lego-lab-and-ldraw-facts.md) — grounded LDConfig colour names, stud colour in the inline block, thumbnail gates split at the GPU, `visibleColours` is baked
- [Text-emit facts](text-emit-facts.md) — face baked from Source Code Pro 2.042 for the slashed zero, confusables BLOCK, extrude-only labels, `make coupons BIKAR_DIR=`
- [bikar secrets and Supabase](bikar-secrets-and-supabase.md) — dotenvx key in LastPass `dotenvx/bikar` keyed by origin remote, secrets set by pipe, 42P10 guard lives in coffee-house-sites
- [Studio folder store](studio-folder-store.md) — root is an absent key never `''`; `.folders.json` is a three-state dev-only overlay; a folder is a label
- [d3 integration decisions](d3-integration-decisions.md) — Q-HOME/Q-SHELL/Q-VOCAB/Q-DATA settled; the ring is the join key, two id namespaces, join lives in the overlay
- [Rosette explorer findings](rosette-explorer-findings.md) — run the real kernel, measure roster preconditions per entry, param bleed throws, plates are data, cap keeps the thickest wall
- [Branch state across repos](branch-state-across-repos.md) — remote branch inventory after the 2026-08-30 cleanup, one kept prior-art branch, one superseded branch that must never merge, guards + protection
- [Owner-gated and on hold](owner-gated-and-on-hold.md) — printing paused (no CAL bet settled), `schema-v*` tag/publish, contract acceptance, Cloudflare/GHCR settings are Omar's
- [Omar's working preferences](omar-working-preferences.md) — decides via options, faithful over safe, deliverables before polish, PR everything, delete merged branches, memory holds facts not to-dos
- [bikar studio access](bikar-studio-access.md) — only public entry is bikar.naqshcoffee.com, gated behind org GitHub sign-in; internal audience, internet-reachable (settles the public-surface keystone)
- [gh auto-merge footgun](gh-auto-merge-footgun.md) — `--auto` merges immediately on NaqshCoffee repos; poll to green instead
- [3d-models use-case hook](3d-models-use-case-hook.md) — pre-commit dispatcher blocks pointer-file commits without map update; USE_CASES_OK=1 override
- [PR flow for all repos](pr-flow-for-all-repos.md) — every change (docs included) goes branch→PR→merge, never direct-to-master; marketplace repo is the exception
- [Gate verdict is checkout-independent](gate-verdict-checkout-independent.md) — worktree sibling fallback + self pin at the published base (#132, #133); any gate touching paths outside the repo gets a worktree self-test
- [Stacked-PR stranding](stacked-pr-stranding.md) — never base a PR on another open PR's branch here; merge lands in the parent, not master, and strands it if the parent goes stale
- [Check main's CI, not just the PR's](check-main-ci-not-just-the-pr.md) — bikar `ci` was red on main for four runs and three PRs merged past it; read main's last run first, fix in its own PR off main, rebase, then poll to green

Moved out of this repo's memory when auto-memory became per-repo (2026-08-16): `amazon-scripts-repo` → amazon-scripts, `marketplace-repo-mirror-and-held-branch` → oeid-claude-plugin-marketplace, `check-for-existing-e2e-before-reporting-blocked` and `supabase-paused-project-timeout` → bikar. Named without links because the files are no longer here and a dead relative link is a D1 gate failure.
