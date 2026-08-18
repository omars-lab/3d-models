# Local CI runbook — the run that does not need a hosted runner

**This repo has no `.github/workflows` directory.** That is not an oversight and
not a gap to be closed later: everything this repo gates is a hook, `make
validate` runs every one of them over the whole tree, and `make deploy` pushes
the gallery from a `gh-pages` worktree on this machine. There is nothing here
that a GitHub Actions billing block can stop.

The runbook exists anyway, for two reasons. The first is that the sibling repos
*do* have workflows, and a change here often lands beside one there — so the
question "can I merge while Actions is down?" arrives here even though the
answer for this repo is always yes. The second is the harder half: with no CI,
**the local run is the only run there is**, so anything it quietly skips is
never caught by anything.

## The run

| Command | What it is |
|---|---|
| `make validate` (alias `make local.ci`) | every pre-commit hook, whole tree |
| `make validate-strict` (alias `make local.ci-strict`) | as above, but a check that could not run is a failure |
| `make validate-parity` (alias `make local.ci-parity`) | prove the hook set and the wholesale set still match |

The `local.ci` spellings are aliases, not copies — one definition, four repos,
one front-door name. The `validate*` names stay because here these are hooks,
not workflows, and that distinction is real.

**What makes the run trustworthy is not the run, it is `validate-parity`.** Each
hook in `.githooks/pre-commit.d/` declares its whole-tree form in a
`# wholesale:` line, and `.claude/gates/hook_parity.py --check` fails on a hook
that declares none. `make validate` was a hand-listed chain until that gate
shipped, which is exactly how a chain drifts: somebody adds a hook, nobody adds
it to the list, and the wholesale run reports success the whole time it is
incomplete.

`--self-test` runs first, ahead of `--check`, in all three targets. The reason is
this repo's own corollary — *the by-design failure is the load-bearing case*: a
checker that only ever sees a correct repo reports OK forever, including on the
day it stops looking. `--check` here is the assertion that everything is fine,
so it cannot be the thing that proves the checker still detects a repo that is
not; only a fixture can hold the counterexample.

Measured 2026-08-18 on this branch:

```
hook-parity --self-test: all cases behaved as designed
hook-parity: OK — 8 pre-commit hooks, all declaring a wholesale form
             (1 of them needs a tool on PATH),
             plus 2 check(s) with no hook behind them.
```

The eight hooks are `05-hook-parity`, `10-gitleaks`, `20-use-cases`,
`30-docs-gate`, `35-doc-pointers`, `36-catalog-models`, `37-counts` and
`40-site-graph`. The one needing a tool on PATH is gitleaks — without it the run
says **NOT VERIFIED** and names it, rather than passing over it in silence. That
distinction is the whole contract of the summary line: a green summary means
green on what ran, and what did not run is printed above it.

## Deploying

`make deploy` builds the images and the lab pages, then copies `DEPLOY_PATHS`
into a `gh-pages` worktree and pushes. No runner is involved at any point, and
`gh-pages` is a deliberately diverged branch — never merge it into `master`.
`validate-site-graph` runs as a prerequisite, so a deploy cannot ship a gallery
whose link graph does not check out.

## When a sibling's Actions run will not start

A merge here does not depend on Actions, but a cross-repo change often waits on
bikar or qiyas. Tell a billing block from a real failure before you decide
anything:

```
gh run view <id> --json jobs
```

A **real failure** shows steps and retrievable logs — something ran and reached a
verdict. A **billing block** shows `"steps": []` and a two-to-three second wall
time: the job never allocated a runner, so nothing about the branch was measured
in either direction. Reading that as a red build is reading a verdict that was
never rendered. Measured 2026-08-18 on bikar#105 — three checks, all reported
"failure", all `steps: 0`, `17:33:50 → 17:33:52`.

The runner-free form in each repo:

| Repo | Gate run | Deploy / publish |
|---|---|---|
| 3d-models | `make validate` / `make local.ci` | `make deploy` (gh-pages worktree) |
| bikar | `make local.ci` (`ci-parity.yaml`) | `make web-deploy`, `make local.publish-core-direct`, `make local.publish-schema-direct` |
| qiyas | `make local.ci` (`ci-parity.yaml`) | `make push TAG=vX.Y.Z` — single-arch, where `publish.yml` builds `linux/amd64,linux/arm64` |
| sacred-patterns | `make local.ci` (`gate-parity.yaml`) | `make deploy` (gh-pages worktree) |

Each sibling carries its own runbook — bikar and qiyas at
`docs/local-ci-runbook.md`, sacred-patterns at `local-gate-runbook.md` beside
it — each under its own checkout, not this one. They
are named that way rather than linked because a relative link into a sibling
would resolve against whatever someone happens to have on disk, which is exactly
what `.claude/gates/doc_pointers.py` exists to stop this repo from asserting.

**Merge on a named local run, never on "CI was down".** Paste the verdict line
verbatim, name every check it reported NOT VERIFIED and why, and say when that
gets re-run. If the answer to the second is "none" and you did not read the
output, you have not run it.

**The trap the whole arrangement exists to name:** *a fallback weaker than the
thing it falls back from.* The fallback is used at exactly the moment nothing
else is watching, so the asymmetry stays invisible until it costs something.
bikar had it in all three of its publishing paths, measured 2026-08-18 — `make
web-deploy` published a bundle its own secret scanner had never seen, and then
verified nothing had landed. There is no undo downstream of a publish: a version
on GitHub Packages cannot be reused, and a key in a shipped bundle has been
served. This repo's `make deploy` is the same shape and holds to the same rule —
it runs `validate-site-graph` first rather than after.
