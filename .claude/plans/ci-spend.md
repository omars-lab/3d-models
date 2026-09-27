# Cutting GitHub Actions down to what only GitHub can do

*Plan, 2026-09-27. Reviewed the same day against the workflow files and partly carried out:
qiyas now has the pre-push hook (#1's laptop half). What was checked, what changed, and what is
left for the owner are in [the last section](#review-and-progress-2026-09-27).*

## What should the session that picks this up do?

This plan lives here so a **dedicated session** can work it without holding up the hifth demo
work it was measured from. Start with the qiyas changes (#1 and #2 below): they are almost all of
the money. Then do bikar's deploys (#3), then hifth's move to local hooks (#5 and #6), which saves
no money but is what the owner asked for ("maximize checks we do via pre-commit hooks";
"assume they will be run all the time, we are only dev").

- Work each repo in its own branch and PR, in that repo.
- Measure qiyas's fast test half on the laptop **before** moving it into pre-push.
- Ask the owner before installing WebKit, before dropping qiyas's slow tests from the routine
  run, and before changing any billing setting.
- The numbers below were measured on 2026-09-27. Re-check them if much time has passed.

The owner's rule for this plan: **we are the only developers, and the local hooks always run.**
So a check the laptop runs before a commit or a push does not also run on GitHub as a backup.
GitHub keeps only what the laptop cannot do.

## Why do the builds stop working a few hours into each month?

The organisation that holds bikar and qiyas is on GitHub's Team plan. That plan includes
**3,000 Linux minutes a month**, and the spending limit above that is set to $0. Once the 3,000
minutes are gone, every job fails at once with the billing message, until the 1st of the next
month.

Measured from GitHub's billing records:

| month | minutes used | bikar | qiyas | everything else |
| --- | --- | --- | --- | --- |
| August | 3,000 (limit hit) | 1,535 | 1,422 | 43 |
| September | 3,006 (limit hit) | 2,450 | 495 | 55 |

September went like this: **1,381 minutes on the 1st and 1,085 on the 2nd.** The allowance was
effectively gone in about 36 hours. Every bikar run since 18 September has failed without
starting: 300 runs in a row. That is the red wall we have been seeing.

## Does hifth's CI cost anything?

**No.** hifth is a public repository under a personal account, and GitHub does not charge for
standard Linux runners on public repositories. GitHub's own timing record for a recent hifth run
shows 0 billable minutes. hifth does not draw on the organisation's allowance at all.

So thinning hifth's CI **saves no money**. The owner still wants it done, and there are good
reasons: faster feedback, one place where the checks live, and no week-long red streak that
nobody reads (main was merged red for about ten PRs this week because the result was only on
GitHub). The money is in qiyas and bikar, so their section comes first.

## Where do the minutes go today?

GitHub charges each job by rounding its length **up to the next whole minute**, so a 10-second
job costs a full minute.

### qiyas: the single biggest cost per change

| workflow · job | runs per merged change | minutes per run | runner | notes |
| --- | --- | --- | --- | --- |
| CI · lint-test | 2 (PR + main) | 64–73 | Linux | the test step alone is 62 min; lint, types and imports take 16 s |
| CI · docker-build | 2 | 3 | Linux | |
| CI · review-portal-build | 2 | 1–2 | Linux | |
| Secret scan | 2 | 1 | Linux | |
| **total per merged change** | | **≈ 150** | | measured, 4 sample runs |

About 20 merged changes a month is enough to use the whole organisation's allowance on qiyas
alone. The test step runs the whole suite, including tests the suite itself marks `slow` and
`integration`. Nothing filters them out.

Three qiyas workflows run on every PR and every push to main: `ci.yml` (the first three rows),
`secret-scan.yml` and `decision-coherence.yml` (only when decision docs change). Two more,
`publish.yml` (on a version tag) and `measure-floors-linux.yml` (by hand), do not run per change.

### bikar: already mostly fixed, one piece left

Before 21 September, a merged bikar change cost about **34 minutes**. That was 16 on the PR and
16 again on main, across CI (6), E2E (5), Orb validation (3), Secret scan, Calibration and
Decision coherence (1 each), plus a 2-minute deploy. All measured from successful runs on 17
September.

On 21 September (bikar #241) those six checking workflows were switched to **run only when
started by hand**, and bikar's pre-push hook now runs the full suite (`make local.ci-strict`)
instead. What still runs on every push to main:

| workflow | runs in the last 8 days | minutes per run | estimated per month |
| --- | --- | --- | --- |
| Deploy to Cloudflare Pages | 47 | 2 | ≈ 350 *(estimate)* |
| Sync patterns to Supabase | 17 | 1 | ≈ 65 *(estimate)* |

These are what the two would cost once minutes are available again. Right now they cost nothing,
because every bikar run since 18 September has failed before starting (300 of the 300 most recent
runs, checked at review). The deploy also has a laptop path: `make web-deploy` runs the same
bundle secret scan before publishing and the same three checks after (bikar's Makefile, read
at bikar main `e061ca4`), but it needs the Cloudflare token on the laptop.

### hifth: free, but here is its shape

| job | runs per merged change | minutes (rounded up) | runner |
| --- | --- | --- | --- |
| secrets scan | 2 | 1 | Linux |
| build + 32 checks | 2 | 2–3 | Linux |
| browser tests (iPhone, Android, desktop, golden images) | 2 | 5–7 | Linux, in the Playwright container |
| Lighthouse | 2 | 2 | Linux |
| deploy to Pages | 1 (main only) | 1 | Linux |
| **total** | | **≈ 24 per merged change, plus a full rerun for every `update-branch`** | measured, 6 sample runs |

## What would the laptop add to a commit or a push, if hifth's checks moved there?

Measured on this laptop today, all green:

| check | time here | fits |
| --- | --- | --- |
| lint | 4 s | before each commit |
| type check | 3 s | before each commit |
| unit tests (316) | 11 s | before each commit |
| 30 of the 32 checks | ≈ 6 s together (0.2–0.5 s each) | before each commit |
| check that the vendored corpus stays weighable | 5.4 s | before a commit that touches assets |
| check that pages are the pinned print | 3.9 s | before a commit that touches assets |
| data rebuild matches what is committed | 2 s | before a push |
| production build | 5 s | before a push |
| app size check (now also refuses pitch code) | < 1 s | before a push |
| desktop browser tests (95) | 26 s | before a push |
| Android browser tests (146) | 46 s | before a push |
| golden images, Mac set (14) | 9 s | before a push |
| iPhone browser tests | **cannot run yet**: Safari's engine (WebKit) is not installed here | before a push, once installed |
| Lighthouse | not measured; about 1.5 min on GitHub *(estimate)* | by hand, see below |

**A commit would wait about 25 seconds, and a push about 1.5 minutes** (about 2 minutes with
the iPhone tests). Today the pre-commit hook already runs the secrets scan and six of the
checks.

## What truly cannot run on the laptop?

- **The deploy itself.** GitHub Pages has to be published from GitHub.
- **A build from a clean checkout.** The laptop holds the private pitch data (The Study Quran's
  commentary, in a folder git ignores). The public build already deletes that folder from its
  output, and the size check now refuses any public build that carries pitch code. But the only
  build that *proves* the published site never had the private folder is the one made from a
  fresh clone. The deploy job already builds from a fresh clone, so that proof costs nothing
  extra: keep the build and the held-text checks inside the deploy job.
- **Nothing else.** The iPhone tests look like an exception, but they are not. WebKit installs
  on a Mac with one command (`pnpm exec playwright install webkit`, a one-time download of about
  100 MB). **That needs the owner's yes before it runs.** Once it is installed, the iPhone
  project runs in pre-push like the others. This matters: the iPhone project is the one that
  caught this week's jump bug, which the Android project missed.

## Which changes save the most, for the least effort and risk?

Ranked by organisation minutes saved per month. The hifth rows save $0 but carry the owner's
local-hooks rule.

| # | change | saves (per month) | effort |
| --- | --- | --- | --- |
| 1 | qiyas: stop running its three per-change workflows (CI, Secret scan, Decision coherence) on every PR and push; run them in the pre-push hook, the way bikar does | **≈ 1,400–3,000 min** *(estimate: August's 1,422 was a quiet month)* | small, but not only a trigger edit: qiyas's check that `make local.ci` matches CI found the workflows by their `pull_request` trigger, so dropping the trigger would have made it fail on every entry (bikar #241 hit the same). **Done at review** in the qiyas hook PR; the trigger edit itself is left for the owner |
| 2 | qiyas: when CI does run, skip the tests marked `slow` and `integration` | most of the 62 min per run *(not measured on GitHub)* | tiny: one pytest flag, `-m 'not slow and not integration' -n auto`, now `make local.test-fast` in the qiyas hook PR |
| 3 | bikar: deploy once per batch, not on every push to main | ≈ 250–300 min *(estimate)* | small |
| 4 | Never `gh pr update-branch`; bring main in locally before pushing | doubles as the fix for #1 in any repo still running PR checks | habit, no code |
| 5 | hifth: move every check into the local hooks; GitHub keeps only deploy | $0 (free repo); faster feedback, no hidden red | medium: hook and `make` wiring |
| 6 | hifth: Lighthouse off every push | $0 | tiny |

### 1 · qiyas: move CI into the pre-push hook

- **Pros:** removes about 150 minutes per merged change, which is most of the organisation's
  spend. qiyas already runs lint, format, strict types and import rules in pre-commit, and it
  has `make local.ci` / `local.ci-strict` plus a check that they cover every CI step. bikar
  has made the same switch already, so this is proven.
- **Cons:** the qiyas tests take 62 minutes on GitHub's two-core machine. A push that waits an
  hour is not workable, so this only works together with #2 (split fast and slow). Measured at
  review on this laptop (18 cores): `make local.test-unit`, everything but the four
  `integration` files, ran 2,415 tests green in **5 min 10 s**. Leaving out the three `slow` tests as well
  (`-m 'not slow and not integration' -n auto`, now `make local.test-fast`) ran 2,412 green in
  **3 min 04 s**, and 149 s inside the hook on the first real push. Most of what is left is a
  handful of unmarked corpus tests at 76–120 s each, so #2's con (a slow test nobody marked
  stays slow) is real, but a 3-minute push wait is workable.
- **Implications:** the slow and integration tests stop running on every change. They run by
  hand (`make` target, or the workflow started by hand) before a release, or once a night on the
  laptop. A regression that only the slow tests catch is found at that point, not on the PR.
  The Docker image build moves to the publish workflow, which already runs on a version tag.

### 2 · qiyas: skip the slow tests on routine runs

- **Pros:** one flag; the markers already exist (four whole files are `integration`, three
  single tests are `slow`). `make local.test-fast` (qiyas hook PR) applies
  `-m 'not slow and not integration'` with `-n auto` (all cores); `make local.test-unit`, which
  drops only `integration`, is left as it is because the coverage gate reads it.
- **Cons:** it depends on the markers being accurate. A slow test nobody marked stays slow.
- **Implications:** the full suite needs a named home (a `make` target and a manual workflow),
  or it quietly stops being run at all.

### 3 · bikar: fewer deploys

- **Pros:** 47 deploys in 8 days, at 2 minutes each. Deploying from a hand-started run, or once
  a day, keeps the site current and cuts most of that.
- **Cons:** a merged change is not live until the next deploy.
- **Implications:** when a change needs to be seen live, someone has to start the deploy. The
  pattern sync (1 minute, and only when pattern files change) can stay as it is. A third way,
  not in the first draft: deploy from the laptop with `make web-deploy`, which runs the same
  scan and checks as the workflow. That costs no minutes at all, but it needs the Cloudflare
  token and account id on the laptop, which is the owner's call.

### 4 · Stop `update-branch`

- **Pros:** each `gh pr update-branch` makes a merge commit on GitHub and reruns every PR check.
  In hifth this week it happened on almost every PR.
- **Cons:** without it, a branch can be green on its own but break once combined with a newer
  main.
- **Implications:** replace it with `git fetch && git rebase origin/main` (or merge) **locally**,
  then push. The pre-push hook then checks the combined code, which is the check
  `update-branch` was buying, but done on the laptop.

### 5 · hifth: every check local, GitHub keeps only the deploy

- **Pros:** results show up in the session before the push, not on a web page nobody opens.
  One list of checks instead of two. Main cannot go red silently for ten merges again, because
  a red check stops the push.
- **Cons:** a push waits about 1.5–2 minutes. PRs no longer show green ticks on GitHub, so a
  reviewer has to trust the hook.
- **Implications:**
  - WebKit has to be installed locally (the owner's call, above), or the iPhone project stops
    being run at all.
  - The golden images: GitHub checks the Linux set, and the laptop checks the Mac set. With
    GitHub out of it, the Linux set has no user. Either retire it (and relax the check that
    insists both sets come from one image), or keep `make golden-linux` (Docker) in pre-push,
    which is slower and not measured.
  - The check that "every check is wired into `make ci` and the workflow" has to be pointed at
    the hook targets instead.

### 6 · hifth: Lighthouse off every push

- **Pros:** it is a score (performance, accessibility and so on, each at least 90), not a
  catcher of specific bugs. It rarely moves in one change, and it takes about 1.5 minutes.
- **Cons:** a slow drift in accessibility or performance goes unseen until someone runs it.
- **Implications:** run `make lighthouse` by hand before showing the demo or a release, and put
  that step in the release checklist.

### Already in place, or not worth doing

- **Cancel older runs on the same branch:** hifth, bikar and qiyas already have this.
- **Docs-only changes skip checks:** qiyas's CI and bikar's deploy already skip markdown and
  `docs/`. qiyas's secret scan deliberately does not (a key pasted into a README is still
  leaked). hifth would not need this once #5 lands.
- **Caching installs:** already on (pnpm in hifth, npm in bikar, uv in qiyas), and install
  steps take 2–3 s.
  Nothing to gain.
- **Moving off macOS runners:** every job in all three repos already runs on Linux.
- **Shorter time limits:** they only change what a hung job costs, not a normal run. The
  first draft said qiyas's 120-minute limit could drop to 20 once #2 lands; with CI hand-started
  and running the whole suite, 120 stays.

## What would hifth's setup look like?

### Two `make` targets that the hooks and every other caller share

A sketch. Two names in it do not exist yet and would be written with it: `gates:fast` (hifth's
`gates` script minus `gate:assets` and `gate:pages`) and `etl-check` (hifth's Makefile has
`etl`, which rebuilds the data, but no target that only compares it with what is committed).

```make
# Before each commit: ~25 s. Fast checks, and the slow asset checks only when assets are staged.
.PHONY: pre-commit
pre-commit: core
	$(PNPM) lint
	$(PNPM) typecheck
	$(PNPM) test
	$(PNPM) gates:fast          # every gate except the two asset-weighing ones
	@git diff --cached --name-only | grep -q '^apps/web/public/assets/' \
	  && $(PNPM) gate:assets && $(PNPM) gate:pages || true

# Before each push: ~1.5-2 min. Rebuild, then the browser.
.PHONY: pre-push
pre-push: core
	$(MAKE) etl-check           # the data rebuild matches what is committed
	$(WEB) build
	$(PNPM) gate:budget         # size + no pitch code in the public bundle
	$(WEB) exec playwright test --project=desktop --project=android --project=iphone --project=golden
```

```sh
# .githooks/pre-commit  (keeps the existing gitleaks + staged-file checks above this line)
make -s pre-commit || exit 1

# .githooks/pre-push
make -s pre-push
```

The existing `make ci` becomes `pre-commit` plus `pre-push`, so there is one list. The check
that "every gate is invoked" (gate:gates) is pointed at these two targets.

The secrets scan must **fail** when gitleaks is missing, not skip with a note. That note
promised that "the CI secrets-scan job still gates every push", and that stops being true.

### What stays on GitHub

```yaml
name: Deploy
on:
  push:
    branches: [main]
    paths-ignore: ['docs/plans/**', '**.md', '.claude/**']
  workflow_dispatch:
concurrency: { group: deploy, cancel-in-progress: true }
jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions: { contents: read, pages: write, id-token: write }
    environment: { name: github-pages, url: '${{ steps.deploy.outputs.page_url }}' }
    steps:
      - uses: actions/checkout@v7          # a fresh clone: no private folder exists here
      - uses: pnpm/action-setup@v6
        with: { version: 9.15.0 }
      - uses: actions/setup-node@v7
        with: { node-version-file: .nvmrc, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - run: pnpm build                    # core + web, stages docs/
      - run: pnpm gate:budget              # size, and refuses pitch code
      - run: pnpm gate:notext && pnpm gate:scripture
      - run: test -s apps/web/dist/index.html && test -s apps/web/dist/docs/index.html
      - uses: actions/upload-pages-artifact@v5
        with: { path: apps/web/dist }
      - id: deploy
        uses: actions/deploy-pages@v5
```

The Cloudflare target and the "Publishable?" check stay as hand-started workflows, as they are
today.

### qiyas, the one that saves money

```yaml
# ci.yml, secret-scan.yml, decision-coherence.yml: hand-started only, as bikar #241 did.
# (The first draft kept `push: [main]` here, which contradicted #1's "stop running CI on
# every PR and push" and the owner's rule that GitHub is not a backup for the hooks.)
on:
  workflow_dispatch:
```

The whole suite stays in `ci.yml` for a hand-started run before a release, and in
`make local.ci` on the laptop. Its 120-minute limit can stay: it only ever runs by hand now.

The laptop half is done (qiyas PR, linked in the last section): `.githooks/pre-push` runs
`make local.prepush`, which is `make local.ci`'s list with one change, the Test step's
`prepush:` command (`make local.test-fast`, measured at 3 min 04 s). The qiyas check that the
local list matches CI now reads which workflows are gates from a list in `ci-parity.yaml`
(`pr_blocking_workflows`) instead of from their `pull_request` trigger, so the trigger edit
above no longer breaks it.

## What should change in how sessions work?

- **Push once per piece of work, not once per commit.** Commit as often as useful, but push when
  the branch is ready. In a repo that still runs PR checks, each push is a full run.
- **Never `gh pr update-branch`.** Rebase or merge main locally, let the pre-push hook check the
  combined code, then push.
- **Read the hook's result before calling a PR green.** With GitHub out of the loop, the hook's
  output in the session *is* the result. "Green" means the pre-push hook passed, not that
  nothing complained.
- **Never `--no-verify`.** This is already the rule, and it becomes load-bearing: the hook is now
  the only check.
- **Keep the hooks and the `make` targets one thing.** A hook contains nothing but `make
  <target>`. A new check is added to the `make` target, never to the hook file or a workflow
  directly. qiyas's parity check (`make local.check-ci-parity`) is the model for enforcing it.

## What can only the owner do?

- **Raise the spending limit or keep it at $0.** Changing the $0 limit on the organisation, or
  adding a payment method, is a billing setting only the owner can change. Even $5 buys about
  830 extra Linux minutes. That is not needed if #1 and #2 land, but it is a buffer.
- **Say yes to installing WebKit** on this laptop, so the iPhone tests can move into pre-push.
- **Decide whether qiyas's slow and integration tests may leave the routine run** (#2), and
  where the full suite runs instead.
- **Decide whether hifth PRs should show GitHub ticks at all.** With #5, they will not.
- **Switch the three qiyas workflows to hand-started** (#1). A session's attempt to make this
  edit was refused by the session's safety check, which treats turning off a repo's checks and
  secret scan on GitHub as the owner's call. Everything around it is in place, so it is the
  three-line `on:` change shown above, nothing else.
- **Choose how bikar deploys** (#3): once a day, by hand, or from the laptop (which needs the
  Cloudflare token there).

## How was this measured?

- **Monthly and daily minutes:** GitHub's billing usage summary for the organisation, for
  August and September, split by repo.
- **Minutes per job:** the start and end times of jobs in sample successful runs, rounded up
  per job the way GitHub bills. That is 6 hifth runs, 3 per workflow in bikar, and 4 qiyas CI
  runs.
- **Run counts:** the run lists for each repo. The bikar search stops at 1,000 results, so its
  August count is partial. Its minutes come from billing, not from the count.
- **Laptop times:** each check run once on this laptop on 2026-09-27, all passing.
- **Laptop times, qiyas (added at review):** `make local.test-unit` (2,415 passed, 5 min 10 s)
  and the `not slow and not integration` run (2,412 passed, 3 min 04 s), each once on this
  laptop (18 cores) on 2026-09-27, all passing; plus the hook's own run on its first push
  (all 18 steps verified, pytest 149 s).

## Review and progress, 2026-09-27

A second session read every workflow the plan names, in qiyas, bikar and hifth (their `main`
at review time), and checked the numbers it could reach again: September's 3,006 minutes (the
billing summary), qiyas's 62-minute test step (run 35225937198), bikar's run of failures since
18 September, the 32 hifth gates, and the $5 ≈ 830 minutes sum ($0.006 a minute). They held.
3d-models has no workflows, so nothing here changes it.

### What the review found, and what was fixed in this file

1. **#1 said "stop running CI on every PR and push", but the qiyas sketch kept `push: [main]`.**
   The two disagreed. Fixed: the sketch is hand-started only, as #1 and the owner's rule say.
2. **#1 was not only a trigger edit.** qiyas's parity check found its gates by the
   `pull_request` trigger, so removing the trigger would have failed it on every entry. bikar
   #241 had to fix the same thing. Now fixed in qiyas (below), and the effort cell says so.
3. **#1 named only CI.** qiyas has three per-change workflows (CI, Secret scan, Decision
   coherence). Now named.
4. **The fast half was unmeasured.** Now measured: 3 min 04 s without the `slow` and
   `integration` tests (5 min 10 s without only `integration`).
5. **bikar's deploy can run on the laptop.** `make web-deploy` runs the same scan and checks as
   the workflow. The "what cannot run on the laptop" section is about hifth's GitHub Pages
   deploy, not bikar's. Added as a third choice under #3.
6. **bikar's deploys cost nothing right now**, because every run since 18 September fails before
   starting. The ≈350 minutes a month is what they will cost once minutes return. Said so.
7. **The hifth sketch uses two names that do not exist yet** (`gates:fast`, `etl-check`). Marked
   as new.
8. **Small wording:** bikar caches npm, not pnpm; qiyas's secret scan deliberately does not
   skip docs; the 120-minute limit stays, because CI keeps the whole suite.
9. **Branch protection does not stand in the way.** qiyas and hifth `main` have no protection,
   and bikar's required checks list is empty, so hand-started workflows block no merge.

### What was done

- **qiyas PR [NaqshCoffee/qiyas#34](https://github.com/NaqshCoffee/qiyas/pull/34):** `.githooks/pre-push` runs `make local.prepush`, the same
  list as `make local.ci` with pytest's fast half (`make local.test-fast`); `ci-parity.yaml` names its gate workflows in
  `pr_blocking_workflows` (the bikar #241 change, with its self-tests); the Test entry gains a
  `prepush:` command that the checker insists carries a reason. The three workflows still run
  on GitHub until the owner flips them, so for now the hook is extra, not a replacement.

### What is left, and whose it is

| item | status | who |
| --- | --- | --- |
| #1 flip qiyas's three workflows to hand-started | ready: a three-line `on:` edit per file | owner (refused as a session edit) |
| #2 slow tests off the routine run | done on the laptop side: the hook runs the fast half | owner decides once #1 flips, because then the full suite only runs by hand |
| #3 bikar deploy cadence | three ways written up | owner |
| #4 no `gh pr update-branch` | a habit | every session |
| #5 hifth checks into hooks | not started: needs WebKit (owner), a call on the Linux golden set, and the deploy rewrite; saves $0 | dedicated hifth session, after the owner's calls |
| #6 hifth Lighthouse off every push | not started: it gates the Pages deploy (`needs:`), so it moves with #5's deploy rewrite | with #5 |
