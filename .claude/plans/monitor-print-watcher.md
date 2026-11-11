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
   `python3 tools/next_id.py next D`.
2. **Spinner coaster: five choices.** The design is
   [spinner-coaster-design.md](../../docs/design/pieces/spinner-coaster-design.md) (#957); the
   choices page with a picture per option is
   [2026-11-08-spinner-coaster-choices.md](../../docs/working-model/feedback-requests/2026-11-08-spinner-coaster-choices.md)
   (#960): what spins, how thick, which bearing, how the pause gets into the file, pause or split
   halves. Backlog: the spinner paragraph at the top of the catalog-expansion backlog. No plate and
   no print until he answers; then the first test piece (a small pocket coupon with no steel in it)
   goes to plates-and-feedback.
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
6. **Cable spiral** (Omar, 2026-11-11: an open-topped disc to wrap a cable round, thin and
   stackable). Model `src/CableSpiral/cable-spiral.scad` and design
   [cable-spiral-design.md](../../docs/design/pieces/cable-spiral-design.md), in 3d-models #1023
   (draft; taking it out of draft was refused here, so that is Omar's or the manager's). The
   research is #1020, #1021 and the checker's #1022. The design doc passed the readability review
   13 of 13 on round 11. Waits on Omar: his cables measured with calipers (the model is set to
   4 mm), then the design fork in open question 1 (walls that cannot bend in the S-bend and the
   outer half turns) after test strips K and P print. The test-piece plate goes to
   plates-and-feedback; never sent from here.
7. **Fidget toys from our patterns.** Design
   [fidget-toys-from-patterns.md](../../docs/design/pieces/fidget-toys-from-patterns.md) (#948);
   its §9 holds five questions (how the toys-1 star came out, size, sliding or turning, which
   pattern, mixing). Not on any backlog yet. The toys-1 and fidget-star-1 prints are recorded in
   the coaster-pipeline lists; fidget-star-1 is kept (#987). bikar would need ring outlines and a
   ring-toy declaration before any build.

### Waiting on another session or a date

8. **Code map trial (graphify on bikar, D-129).** Parked backlog, "Code graph trial". Runs to
   2026-11-20. The side-by-side test came back 2026-11-10 and does not pass (#993). Still owed on
   2026-11-20: rerun the FAQ tool over bikar sessions and judge it against the design's PASS and
   FAIL lines ([code-graph.md](../../docs/design/process/code-graph.md) §6). Stopping early and
   removing graphify is Omar's call.
9. **A post about the code map**, written with the social session (claude-techniques, in
   social-presence-hub). Numbers and design only; don't copy employer content from that repo.
10. **`nmEjCTzMbDg` still fails two render checks**, catalog-expansion item 1. Waits on youtube
   taking the `Intersect(t, m, S)` patch. youtube is read-only from here.

### Can be done without anyone

11. **Gallery freshness.** `make validate-gallery` said on 2026-11-10: 2 unpublished changes, both
    print records on the prints page (ball-1, dragon-egg-1, fidget-star-1), inside the 7-day
    window. Past 7 days it warns; then ask Omar in chat for a deploy, and follow the last deploy
    line in the [consolidation done list](../../docs/tasks/consolidation/done.md) (restore the
    build folder from gh-pages, `make coasters`, `make deploy`, check the live site).
12. **Shrinking the complexity list**, parked backlog, one function a PR; 52 over 10 on 2026-11-11 by the commit hook (the backlog line's "68 left" is older). The `self_test`
    functions are skipped on purpose. Read `.claude/gates/complexity-baseline.json` before picking.
    Low value for customers; do it only between higher items.
13. **16 youtube reconstructions not yet imported here** (the SessionStart line lists them).
    Catalog-expansion has been parked since 2026-10-06 by Omar's call; import only what he asks for,
    which today means the round 3 pick.
14. **Plate-packing skill**, print-infrastructure item 1. Waits until a second plate needs packing.
15. **One application for designing and printing** (Omar, 2026-11-11). The approved plan moves the
    Print Hub's pages into bikar beside the editor and labs, with every answer given in the app.
    Step 0a (two broken links) is done in 3d-models #1017 and hub #37. Step 0b, the design doc,
    is written and scored 13 of 13 for readability: `docs/design/process/users-and-surfaces-design.md`,
    D-130, use case UC35, in 3d-models #1019 (worktree `~/Workspace/git/3d-models-design`), waiting
    on the manager to merge. Step 1 (one page list, one top bar, Coaster Lab and print history
    added) is next, in bikar, started 2026-11-11; its paired 3d-models change (`LAB_PAGES`, the map
    pointer) branches off master after #1019 merges, since both edit the use-case map. Slices 2 to 5 change pages the
    plates-and-feedback session uses daily, so that session hears through its plan file first.
    The launcher repo (`~/Workspace/git/hubs`) is not to be touched.

### Open pull requests from this session

- Print Hub #36: comment on each numbered piece in a plate's bed picture on the judge page.
  After it merges, run `make agent-install` in the hub repo so the page on port 8768 shows it.
- Print Hub #37: plate links point at `docs/design/plates/`.
- 3d-models #1017: the judge-page skill and its script use comment port 8768, not 8766.
- 3d-models #1019: the one-application design doc (step 0b above).
- 3d-models #1020, #1021, #1022: the cable spiral research (two passes and the checker).
- 3d-models #1023: the cable spiral model and design doc (item 6).
- The plan sort (this PR): the 13 old files in `.claude/plans/` are gone; one moved into the
  guide-print skill. Each is listed in a done list and kept in git history at 266f32ce.

## Things to know

- **Store names live in the storefront**: before naming a theme or pattern a shopper will read,
  check the storefront repo's `docs/naming/names.yaml`. The all-green gBV theme is "Emerald green"
  by Omar's 2026-10-11 pick (#999).
- **Branches and worktrees**: don't delete or switch any until the plan PRs merge; then the
  manager runs one cleanup per repo with the `consolidate-branches` skill.
