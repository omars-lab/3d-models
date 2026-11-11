# Open work of the monitor-print-watcher session, 2026-11-11

Written so a new session can pick this up cold. Omar asked on 2026-11-11 for every session's open
work to go into one plan file like this one, with finished work moved to the done lists.

## Goal

Grow what customers can buy and see: new coaster designs, themes and toys from our patterns, a
current public gallery, and the bookkeeping that keeps Omar's decisions findable. Highest value
next: **build the pattern Omar ticks on the round 3 page** (below), since it is the next new coaster.

## Which work this is

The session that is not plates-and-feedback. By the routing rule in
[`.claude/loop-prompts/README.md`](../loop-prompts/README.md) ("Which session runs which loop") it
owns consolidation, catalog-expansion, parked, the parts of print-infrastructure that are not
plates or judging (the plate-packing skill, the gallery and its deploy), D- id and FAQ bookkeeping.
Anything a shopper or the store touches belongs to the storefront repo; its list is
`~/Workspace/git-naqshcoffee/coffee-house-storefront/docs/tasks/open.md`.

The backlogs stay where they are; this file points at them:
[catalog-expansion](../../docs/tasks/catalog-expansion/backlog.md),
[parked](../../docs/tasks/parked/backlog.md),
[print-infrastructure](../../docs/tasks/print-infrastructure/backlog.md),
[consolidation](../../docs/tasks/consolidation/backlog.md).

## How to work here

- Every command needs the newer Node first:
  `export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"`.
- Work in your own worktree off `origin/master`, never in the shared checkout
  `~/Workspace/git/3d-models` (fast-forward it only). Stage files by name, run
  `git branch --show-current` before each commit, `make validate` before each PR.
- PRs go to `omars-lab/3d-models`. The manager session merges them (`gh pr merge` is refused here).
- Every print send needs Omar's own yes. Never send printer commands from this session; plates
  belong to plates-and-feedback.
- A gallery deploy, or any other public change, needs Omar's yes in this session's chat.

## Where things stand, and what each item waits on

### Waiting on Omar

1. **Round 3: which pattern becomes the next coaster.** Seven patterns ranked on
   [the round 3 page](../../docs/working-model/feedback-requests/2026-11-05-next-coaster-round-3.md)
   (#881). Nothing ticked yet in master's copy. When he ticks one: read the page back the
   request-feedback way (a decisions-log entry, a `**Decided <date>:**` line), add a round-log
   line to `.claude/skills/prioritize-design/scoring.md`, add the import as a catalog-expansion
   backlog item, then run the `import-construction` skill on it. Get the D- id from
   `python3 tools/next_id.py next D`. The same call is entry D in [plates-and-feedback's list of plate decisions](plates-and-feedback.md#plate-decisions-waiting-on-omar-from-every-session).
2. **Spinner coaster: five choices.** The design is
   [spinner-coaster-design.md](../../docs/design/pieces/spinner-coaster-design.md) (#957); the
   choices page with a picture per option is
   [2026-11-08-spinner-coaster-choices.md](../../docs/working-model/feedback-requests/2026-11-08-spinner-coaster-choices.md)
   (#960): what spins, how thick, which bearing, how the pause gets into the file, pause or split
   halves. Backlog: the spinner paragraph at the top of the catalog-expansion backlog. No plate and
   no print until he answers; then the first test piece (a small pocket coupon with no steel in it)
   goes to plates-and-feedback. The design side stays here; the plate side is entry E in
   [plates-and-feedback's list of plate decisions](plates-and-feedback.md#plate-decisions-waiting-on-omar-from-every-session).
3. **Cup-band pictures in the pattern catalog**, catalog-expansion item 8. Waits on Omar's cup
   pick for the store (store-launch call 1-08). Then one bikar PR adds the 13 cup-band coasters to
   the Lab's coaster list with a thumbnail each, then a catalog sync here. Don't add a second
   picture path to the catalog script.
4. **FAQ: keep or drop the last candidate** (the use-case ids). Parked backlog, "The FAQ".
   Regenerate the proposal first with `python3 tools/session_reflect.py update-faq`. Never write an
   FAQ answer yourself.
5. **Orbs printed whole, with supports only outside.** Design
   [whole-orb-outside-supports-design.md](../../docs/design/orb/whole-orb-outside-supports-design.md)
   (#950); its §8 holds five questions for Omar (how far PLA bridges, whether the top half sags,
   the bed-contact floor, strut width, woven orbs). Not on any backlog yet. Its first step, a
   slice with no print then one top-cap test piece, would be a plate, so it goes to
   plates-and-feedback once Omar answers. Survey script: `uv run tools/orb_support_survey.py --self-test`.
   The questions that decide what gets printed are entry G in [plates-and-feedback's list of plate decisions](plates-and-feedback.md#plate-decisions-waiting-on-omar-from-every-session); the design side stays here.
6. **Fidget toys from our patterns.** Design
   [fidget-toys-from-patterns.md](../../docs/design/pieces/fidget-toys-from-patterns.md) (#948);
   its §9 holds five questions (how the toys-1 star came out, size, sliding or turning, which
   pattern, mixing). Not on any backlog yet. The toys-1 and fidget-star-1 prints are recorded in
   the coaster-pipeline lists; fidget-star-1 is kept (#987). bikar would need ring outlines and a
   ring-toy declaration before any build. The questions that decide what gets printed are entry F
   in [plates-and-feedback's list of plate decisions](plates-and-feedback.md#plate-decisions-waiting-on-omar-from-every-session); the design side stays here.

### Waiting on another session or a date

7. **Code map trial (graphify on bikar, D-129).** Parked backlog, "Code graph trial". Runs to
   2026-11-20. The side-by-side test came back 2026-11-10 and does not pass (#993). Still owed on
   2026-11-20: rerun the FAQ tool over bikar sessions and judge it against the design's PASS and
   FAIL lines ([code-graph.md](../../docs/design/process/code-graph.md) §6). Omar said on
   2026-11-11 to let it run to that planned end (approvals log, #1009), so no early stop.
8. **A post about the code map**, written with the social session (claude-techniques, in
   social-presence-hub). Numbers and design only; don't copy employer content from that repo.
9. **`nmEjCTzMbDg` (CS-9): R fixed 2026-11-11**, catalog-expansion item 1. youtube had already
   made the fix (d72fc2a, 2026-09-29); bikar's copy was stale and is re-imported on bikar branch
   `fix-nmEj-root-nearest-s` (commits c4dcccc6 and 07030dcf; its PR is named in the done line
   once open). The 3d-models half is written and in the same PR as this plan (branch
   `cs9-nmej-root-fix`): the re-vendored `src/Coasters/nmEjCTzMbDg-coaster.bkr` and its
   `-standard.stl` (rendered with the bikar branch's CLI, mesh check passed, 162,492 triangles),
   ledger row 145 (`FAIL 34/3 | PASS 1.0/1.0`) and its note, backlog item 1, and the correction
   section at the end of `docs/research/ledger-oracle-runs-2026-11-10.md`. Left, in order:
   1. Wait for the manager to merge the bikar PR. If bikar's push gate failed, the reason is in
      the bikar PR or the done line; fix that first (watch for "NOT VERIFIED (docker
      unavailable)": the push PATH needs `/usr/local/bin`).
   2. After the bikar merge, run `python3 .claude/skills/pattern-catalog/scripts/catalog.py sync`
      so `docs/catalog/media/nmEjCTzMbDg/nmEjCTzMbDg-plain.png` takes bikar main's new Lab
      thumbnail; commit it in its own PR.
   3. A print review (`review-print` skill) of the new coaster before anyone prints it: the
      spokes crowd at the centre. Do not print it until then.
   4. To redo any comparison: O1 is `make -C ~/Workspace/git/youtube naqsh-coords
      ID=nmEjCTzMbDg NAQSH=<bkr> OUT=<scratch>/o1 BIKAR_DIR=<bikar worktree>`, O2 is
      `make -C ~/Workspace/git/youtube naqsh-score ID=nmEjCTzMbDg NAQSH=<bkr>`. In a fresh bikar
      worktree, build every package (`npm ci`, then root `npm run build`), not only core and the
      CLI: without `bikar-knobs` and `qiyas-schema` the Lab thumbnail script never finishes
      (now in the `bikar-build-and-test-traps` memory note).

### Can be done without anyone

14. **The 13 old plan files in this folder still need sorting** (manager's ask, 2026-11-11):
    authorized-2026-11-03, binary-tickling-kay, breakdown-pages-kickoff, cheerful-mixing-tiger,
    ci-spend, coaster-border-continuation, glowing-popping-pinwheel, iterative-dazzling-finch,
    lego-tooling, nmej-conic-arc-support, sleepy-yawning-bubble, sprightly-jingling-milner and
    sunny-booping-crescent. For each: finished means a done line and delete it; still open means
    fold it into this plan or plates-and-feedback's (ask that session about plate ones); dead means
    say why and delete it. One PR. Before deleting, `git grep` the file name and fix the links.


10. **Gallery freshness.** `make validate-gallery` said on 2026-11-10: 2 unpublished changes, both
    print records on the prints page (ball-1, dragon-egg-1, fidget-star-1), inside the 7-day
    window. Past 7 days it warns; then ask Omar in chat for a deploy, and follow the last deploy
    line in the [consolidation done list](../../docs/tasks/consolidation/done.md) (restore the
    build folder from gh-pages, `make coasters`, `make deploy`, check the live site).
11. **Shrinking the complexity list**, parked backlog, one function a PR; 52 over 10 on 2026-11-11 by the commit hook (the backlog line's "68 left" is older). The `self_test`
    functions are skipped on purpose. Read `.claude/gates/complexity-baseline.json` before picking.
    Low value for customers; do it only between higher items.
12. **16 youtube reconstructions not yet imported here** (the SessionStart line lists them).
    Catalog-expansion has been parked since 2026-10-06 by Omar's call; import only what he asks for,
    which today means the round 3 pick.
13. **Plate-packing skill**, print-infrastructure item 1. Waits until a second plate needs packing.

## Things to know

- **Store names live in the storefront**: before naming a theme or pattern a shopper will read,
  check the storefront repo's `docs/naming/names.yaml`. The all-green gBV theme is "Emerald green"
  by Omar's 2026-10-11 pick (#999).
- **Branches and worktrees**: don't delete or switch any until the plan PRs merge; then the
  manager runs one cleanup per repo with the `consolidate-branches` skill.
