# Cutting GitHub Actions down to what only GitHub can do

*Plan, 2026-09-27. Nothing below has been changed yet; this is the proposal.*

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
| 1 | qiyas: stop running CI on every PR and push; run it in the pre-push hook, the way bikar does | **≈ 1,400–3,000 min** *(estimate: August's 1,422 was a quiet month)* | small: qiyas already has `make local.ci` and a check that it matches CI |
| 2 | qiyas: when CI does run, skip the tests marked `slow` and `integration` | most of the 62 min per run *(not measured)* | tiny: one flag |
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
  hour is not workable, so this only works together with #2 (split fast and slow). The laptop
  is probably much faster, but that is not measured yet.
- **Implications:** the slow and integration tests stop running on every change. They run by
  hand (`make` target, or the workflow started by hand) before a release, or once a night on the
  laptop. A regression that only the slow tests catch is found at that point, not on the PR.
  The Docker image build moves to the publish workflow, which already runs on a version tag.

### 2 · qiyas: skip the slow tests on routine runs

- **Pros:** one flag (`-m "not slow and not integration"`); the markers already exist.
- **Cons:** it depends on the markers being accurate. A slow test nobody marked stays slow.
- **Implications:** the full suite needs a named home (a `make` target and a manual workflow),
  or it quietly stops being run at all.

### 3 · bikar: fewer deploys

- **Pros:** 47 deploys in 8 days, at 2 minutes each. Deploying from a hand-started run, or once
  a day, keeps the site current and cuts most of that.
- **Cons:** a merged change is not live until the next deploy.
- **Implications:** when a change needs to be seen live, someone has to start the deploy. The
  pattern sync (1 minute, and only when pattern files change) can stay as it is.

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
- **Docs-only changes skip checks:** qiyas and bikar already skip markdown and `docs/`. hifth
  would not need this once #5 lands.
- **Caching installs:** already on (pnpm cache and uv cache), and install steps take 2–3 s.
  Nothing to gain.
- **Moving off macOS runners:** every job in all three repos already runs on Linux.
- **Shorter time limits:** they only change what a hung job costs, not a normal run. The
  exception is qiyas's 120-minute limit, which can drop to 20 once #2 lands.

## What would hifth's setup look like?

### Two `make` targets that the hooks and every other caller share

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
# ci.yml: on every change, only the fast half, and only by hand or on main
on:
  workflow_dispatch:
  push:
    branches: [main]
    paths-ignore: ['**.md', 'docs/**', '.claude/**', 'CHANGELOG.md']
jobs:
  lint-test:
    timeout-minutes: 20
    steps:
      # ...unchanged setup...
      - run: uv run pytest -m "not slow and not integration"
```

Add a qiyas `.githooks/pre-push` that runs `make local.ci`, with the same fast-test filter, as
bikar does. A separate hand-started workflow (or `make local.ci-full`) runs the whole suite before
a release. **Measure the laptop time of the fast half before switching**, because it is not
measured yet.

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

## How was this measured?

- **Monthly and daily minutes:** GitHub's billing usage summary for the organisation, for
  August and September, split by repo.
- **Minutes per job:** the start and end times of jobs in sample successful runs, rounded up
  per job the way GitHub bills. That is 6 hifth runs, 3 per workflow in bikar, and 4 qiyas CI
  runs.
- **Run counts:** the run lists for each repo. The bikar search stops at 1,000 results, so its
  August count is partial. Its minutes come from billing, not from the count.
- **Laptop times:** each check run once on this laptop on 2026-09-27, all passing.
