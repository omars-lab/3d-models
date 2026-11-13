# Done — consolidation

Newest first: date, what was merged or cleaned up, PRs. Backlog: [`backlog.md`](backlog.md).

- 2026-11-13 — The Studio's side bar links to the Naqsh design hub (coffee-house-storefront, `http://127.0.0.1:9494/`): a "Naqsh designs" row under Check, opening in a new tab. This is the Studio's half of Omar's "linked, for now" call, recorded in the storefront's hub-unification design doc; the storefront's pattern pages now open the Studio editor at `/editor#<file name>` (bikar #381, design note in bikar's `docs/features/studio-sidebar.md`)
- 2026-11-13 — The always-on Studio app is merged: the Studio's built pages served on 7136 by a launch agent, with print requests passed on to the Print Hub on 4717. Its conflict with main's comment-server target was worked by hand, keeping both (bikar #374). What is left is Omar loading the launch agent once (`make app-agent-install`)
- 2026-11-13 — The Studio's side bar with a light and dark switch replaced the top bar: Make, Study and Print groups, a line, then the other apps; folds to icons; a drawer on a phone (bikar #380, design `docs/features/studio-sidebar.md` in bikar). Merged by Omar
- 2026-11-13 — The local link check no longer asks Omar every session about a site that is only not running. Until the always-on Studio runs, the Studio is down on this Mac every session, so a down site now gets one quiet line; only a broken page on a running site asks at session start or stops the session at the end (3d-models #1038)
- 2026-11-13 — A Studio print page that can't reach its data now offers its Print Hub page first, keeping the plate in the link, and the top bar's Print menu points at the Print Hub when the print data is not reachable. This covers the gap until the always-on app runs (bikar #379, design `docs/features/print-pages-fallback.md` in bikar)

- 2026-11-13 — A check that opens the local pages and counts broken links, after Omar found the Studio's print pages showing "can't be reached" by hand. It follows every link between the Studio (7136), the Print Hub (4717) and the judging pages (8768), opens the Studio and Print Hub pages in a hidden Chrome, and counts pages that fail, pages that show the "can't be reached" sentence, and links into a site that is down. It runs at session start and, after a session that changed page files, at session end. Skill `check-local-links`, design `docs/design/process/local-link-check-design.md`, `make local-links` (3d-models #1036)
- 2026-11-12 — One app, slice 3: five more Print Hub pages readable in the Studio, read-only: the plates list and one plate's page (bikar #377), the printer, printed plates and print words pages (bikar #378). Plan updated in 3d-models #1035
- 2026-11-12 — Page comments on the Studio's always-on app: `make comments` starts a comment server on 7137 in front of the app on 7136; threads saved in `.page-comments/threads/`, screenshots in iCloud (bikar #376). Retro note `docs/retros/2026-11-12-one-app-judge-page.md` (3d-models #1034)
- 2026-11-12 — One app, slice 2A: the Judge page and the "Waiting on you" list moved into the Studio beside the old judging page, which keeps working; the top bar's Design and Print menus no longer open over each other (bikar #375). The 3d-models half: the app on 7136, the forward to the Print Hub, and the launch agent for Omar to load (3d-models #1033). Omar's go for slices 2 to 5 recorded in the raid log, the plans and the design's Appendix B (3d-models #1032). The app itself, bikar #374, waits on Omar's merge
- 2026-11-12 — Two gaps in the plugins closed: the raid log gained its task and ask sections, and the clean-up-after-merge and whats-next steps cover them (guardrail-manager 1.16.1, task-management-manager 1.6.1; marketplace 15deb47, 20bc0dd); the raid count on the status line runs the installed `raid.py` instead of a copy kept by hand (task-management-manager 1.6.2; marketplace 30a5475)

- 2026-11-12 — Two follow-ups to the top bar. The gallery deploy now deletes pages that left its list, so the old `studio.html` comes off the live gallery at the next deploy (#1027). The Studio no longer throws away an edit made in the first moments after it opens, before the disk copy of the patterns arrives; this was the dial test's "flaky" failure (bikar #373). The public Lab copy was checked at 390 px: its bar links all six Lab pages.
- 2026-11-12 — One top bar on every designing and printing page (slice 1 of the one-app design, D-130). Every Lab and Studio page now carries the same bar along the top (Home, Design, Print, and on the Studio Learn and Check), built into the page so it shows with scripting off; one set of colors; the Coaster Lab and print history listed in the Studio; the Lab's own index page `studio.html` removed, since the bar does its job. The public gallery copy links only public pages, and a test fails if a private address gets onto it (bikar #372). Here: the gallery's page list, front page, `hub.yaml`, the site map and the use-case map moved off `studio.html`. The gallery shows the bar after the next deploy
- 2026-11-11 — The 13 old plan files in `.claude/plans/` sorted: all 13 were finished, none had work left that only the plan held, and every file is in git history at 266f32ce. Removed: the orb breakdown-page plans (sunny-booping-crescent and its brief breakdown-pages-kickoff, shipped as bikar #149, #158, #170, marked shipped in 3d-models #173) and their close-out glowing-popping-pinwheel; the 2026-10-28 cross-repo branch cleanup cheerful-mixing-tiger, carried out and then replaced by the 11-03 and 11-10 passes (3d-models #820, #821, #998); ci-spend, already recorded below (3d-models #356). The first-print campaign plan moved to `.claude/skills/guide-print/first-print-campaign.md`, because guide-print still reads its five-step propagate and coupon tables; its plates to print are in the coaster-pipeline backlog. The other removals are recorded in the catalog-expansion and parked done lists. Every link to a removed file now names the commit instead
- 2026-11-11 — The manager session's run from 2026-11-07 to 2026-11-11 closed out, and its four sessions wound down on Omar's word. Merged on the standing CLEAN-PR rule: 3d-models #927 to #1016 (plates, records, plans, the approvals log #1008, the plate decisions list #1010, the wound-down state #1013 and #1015, the start prompts #1016); storefront #467, #470 and #478 to #503 (the dev-store share button and test order #1001, lead time #494/#497, FAQ care #499, Jost #503); hub #32, #34 and #35, which saved 14 page-comment threads nobody had committed. Each session moved its finished items to its done lists and wrote a plan for its open work: `.claude/plans/plates-and-feedback.md` and `monitor-print-watcher.md` here, and five area plans in the store, which coffee-house-manager-session checked and now owns. Branches: squash-merged ones force-deleted on Omar's three logged yeses (approvals log, 2026-11-10 and 2026-11-11), each tip saved under `refs/snapshots/<date>/` first and its files checked on main; the clean `3d-models-plate-notes` worktree removed. CS-9's two bikar commits, which were only on this Mac in `bikar-else`, saved as `refs/snapshots/2026-11-11/fix-nmEj-root-nearest-s` on bikar's GitHub. Start prompts for each session are in `.claude/prompts/`.
- 2026-11-11 — The design for one app that holds the pattern-designing and printing pages written down, on Omar's three calls that day (bikar holds every page, every answer is a button in the app, Design and Print now with Learn and Check as links; the launcher left alone). `docs/design/process/users-and-surfaces-design.md` now opens on a rendered mockup of the top bar and the "Waiting on you" list at 1280 and 390 px, names who uses what, the journeys, the pages that move, the build order in six slices, and five open calls each with a suggested answer. Decision D-130, the Owner actor and use case UC35 in the use-case map, and the page survey checked in under `docs/research/`. Scored by six fresh readers against the design-craft rubric until 13 of 13 rules passed. Step 0a, the two broken links, shipped in 3d-models #1017 and Print Hub #37 (3d-models #1019)
- 2026-11-10 — Branches across the repos cleared again, under the manager session's limits for a day when three other sessions were working: nothing checked out, nothing with an open PR, nothing with a commit in the last 24 hours, nothing deleted in coffee-house-storefront, remote branches only when their PR merged. 68 deleted, each saved under `refs/snapshots/2026-11-10/` on its repo's GitHub first and re-proven dead just before its delete. In 3d-models that was 48 local branches, among them the three closeout-1-reprint branches once they passed 24 hours. In hifth it was 14 local branches, plus 6 on GitHub whose PRs merged (#540, #541, #542, #546, #549, #550). The manager checked that the 19 hifth snapshot refs are all inside hifth main's history already, so pushing them put nothing back that the 2026-10-08 rewrite removed. Listed, not deleted: the storefront's `decisions/0ke-allen-citation` (the manager's rule for that repo), youtube's `coaster-n_I` (youtube is read-only to this session), 3d-model-hub's `fix/judge-page-opens-plate-first` (under 24 hours). Left in place: the clean detached worktrees `bikar-storefront` and `hifth-walk`, and `split-rewrite-text` for its owner; the manager is listing them for Omar.
- 2026-11-08 — The public gallery deployed again, from master b893fce4, on Omar's "Yes, deploy now": gh-pages b7774718 ("Deploy gallery from master (b893fce4)"), 4 files changed and none removed. The live build folder was restored from gh-pages first, then `make coasters` and `make deploy` ran. The Pages build finished as built. On the live site the split-flange coaster source (`src/Coasters/gBV_JTt3Kxk-split-flange-coaster.bkr`, star pins) and the prints page (`docs/prints.md`, with the #894, #915 and #916 edits) are byte for byte master's, `prints-manifest.json` answers 200, and `bikar-ref.txt` names bikar main fe6b109e. The split-flange file did not change in this deploy: the 2026-11-04 deploy already carried bikar's star-pin version, and #931 brought master up to it.
- 2026-11-04 — The public gallery deployed from master 735a222b, on Omar's "deploy the gallery", so the Ten-Petal Blossom coaster from #872 shows live: gh-pages f223a626 ("Deploy gallery from master (735a222b)"), 57 files changed and none removed. The live STLs, pictures and breakdowns were first restored from gh-pages, then `make coasters` and `make deploy` ran with bikar main and the Pillow Python. The Pages build finished as built, and the blossom card, its picture and its 3.1 MB STL each answer 200 at blog.bytesofpurpose.com/3d-models. Two things to know: `make coasters` copies each coaster's source from bikar, and bikar already has the star-pin default in `gBV_JTt3Kxk-split-flange-coaster.bkr` that master has not picked up, so the live copy is bikar's (the STLs are built from it); and the deploy copies `src/` whole, so the gitignored `*-mini.stl` files went up too. (3d-models #877)
- 2026-11-03 — Every open PR merged and the branches behind them cleared, on Omar's "merge all prs and cleanup": 3d-models #872, #873, #875; bikar #368, #369, then the cup-band stack. Its bottom PR #362 would not merge after #368/#369 changed `patterns/index.json` and `public-surface.json`, so main was merged into the stack tip `feat/cup-bands-three` by hand (both sides kept, the pattern count reconciled to 199), the strict suite passed and was recorded, #366 was retargeted to main and squashed as 21420bc3, and #362 and #363 closed as superseded. The storefront's handoff PR #464 went last, as its body asked. Deleted after each was proven dead by content: bikar's `feat/cup-bands-{seven,star-lines,three}` and the three `feat/cup-band-{bkn,n3i,ta8}` branches (every one an ancestor of the merged stack tip; tips under `refs/snapshots/2026-11-03/`), their two worktrees, and the merged branches `blossom-n_I`, `tray-list-paste` (bikar), `authorized-2026-11-03`, `star-2-done-pr` (3d-models) and `docs/handoff-open-tasks` (storefront) with their worktrees. Nothing lost: every worktree was clean, every tip on origin and no stash before any remove. bikar main and the shared 3d-models and storefront checkouts fast-forwarded. The catalog sync then wrote the cup-band style into the ten pattern notes whose band files #366 put on bikar main, and the style page and index. (3d-models #876)
- 2026-11-03 — bikar's pre-push hook skips the local CI suite when a push is only tags on commits main already holds: narrow and fail-closed like the deletion skip beside it, so a tag off main, a tag with a branch or no stdin still runs the suite, and the wiring test proves all three. Omar's call on 2026-11-03 ("do all the things to do"), merged on his "merge all prs" (bikar #365)
- 2026-11-03 — The shared 3d-models checkout fast-forwarded to origin/master at 0331ebf8, after the day's PRs #859 to #873 had merged, so a session opened there starts from the merged work
- 2026-11-03 — The other repos inventoried (bikar, qiyas, sacred-patterns, 3d-model-hub, youtube, hifth, review-md, the nine store repos): one branch proven dead, bikar's local `feat/pins-ring-no-middle`, snapshotted on bikar's origin and deleted; nothing else to delete, no conflict to work. bikar's three `feat/cup-band-*` branches on GitHub are ancestors of PR #366's branch and go once it merges. The inventory now takes bare repo names and lists a repo once when the store glob also matches its worktree. State in the `branch-state-across-repos` memory. (3d-models #866)
- 2026-11-03 — The snapshot step refuses to put back a removed picture: before pushing, `branch_inventory.py snapshot` looks for a commit off the default whose twin (same subject, same author date, twin parents) sits on the default, the mark of a `git filter-repo` rewrite, and when the tip side holds files that twin lacks it writes the refs locally, names the files and pushes nothing. Tried read-only on hifth's 2026-10-08 snapshot: it names the two held-text pictures. A branch with no twin is untouched, and a cherry-pick is not a twin. A self-test case builds the rewrite. (3d-models #865)
- 2026-11-03 — `make validate` now says when the public gallery is behind master: a new check reads the gh-pages tip's "Deploy gallery from master" line, lists the master commits after it that touch a file the gallery ships, and warns (never fails) when the oldest is over a week old; the warning is named in the suite's end summary, not only mid-stream, so it is read where the verdict is read. Deploying stays a hand step. (`.claude/gates/gallery_stale.py`, `make validate-gallery`, 3d-models #864)
- 2026-11-03 — The public gallery deployed again, five weeks after the last time: the split-pocket coaster got the gallery card the render gate demanded (#859), every one of the 75 cards checked for a picture and an STL, gh-pages at ddc724ad, the live site checked. The three leftover copies removed: the duplicate `-pm` and `-master-ro` worktrees, and the dead subagent worktree (tip saved under `refs/snapshots/2026-11-03/`). Two items closed without work: hifth's GitHub purge (Omar decided no purge on 2026-10-30) and bikar's Supabase upload (its runs succeed again since 2026-10-29, the 2026-11-01 push seeded 6 patterns)
- 2026-11-03 — The 3d-models branches brought back to master with nothing to merge: the inventory found 16 dead branches (12 local, 4 on GitHub), 0 with unmerged work, 0 open PRs, 0 stashes; each tip saved under `refs/snapshots/2026-11-03/` on GitHub, re-proven dead, then deleted one per command. The lagging `-hub-rw` worktree moved to master. The plan for every pass written into the backlog, and the two sessions split by kind of work in the loop README: plates-and-feedback keeps prints, the hub's judging and comments, and print records; the other session takes the rest. The subagent worktree `agent-aa28c8…` (clean, merged, session closed) and `-pm`/`-master-ro` left for Omar
- 2026-11-02 — The merged hub worktree `3d-model-hub-owed` was found already removed, with nothing left to clean up; the gallery's deploy date checked (last deployed 2026-09-30) and put on the backlog as waiting on Omar
- 2026-10-29 — Every tool reads bikar from `~/Workspace/git/bikar`, and the `bikar-main` checkout is gone; bikar's failing pattern upload to Supabase diagnosed and put on this backlog for Omar (3d-models #824, #825)
- 2026-10-27 — Branches across the eight repos checked again, and none held work its main lacked, so nothing needed merging. Six dead 3d-models branches deleted, each saved under `refs/snapshots/2026-10-27/`. bikar's local main brought up to date. Three old hifth branches deleted, saved on this Mac only, because pushing them would put back the pictures hifth's history rewrite removed. The worktree limit raised to 9 on Omar's word, and the hifth trap written into the skill's rules
- 2026-10-24 — Branches and worktrees brought back to main again across the repos, with no work lost in either direction; the consolidate-branches skill sharpened from it (3d-models #768, #773)
- 2026-10-08 — Worktrees cut from 15 towards Omar's budget of 5, without losing work: in 3d-models nine subagent worktrees removed, 35 local and 5 remote dead branches deleted, every tip saved under `refs/snapshots/2026-10-08/`, one worktree's unsaved print-record draft and bambu files copied out before it went; bikar's `next-bikar` and `revendor-prep` deleted; three hifth research worktrees removed. Six 3d-models worktrees remain, one over budget: dropping `-pm` or `-master-ro` is Omar's call. The memory notes that lived only in the shared checkout landed (3d-models #622)

- 2026-10-06 — bikar's `bikar-next` and `coaster-n_I` branches deleted, each tip saved under `refs/snapshots/2026-10-06/` first; the importer change from them landed as bikar #318

- 2026-09-30: the gallery redeployed from master 42ef7de (gh-pages a9cfe0c). It carries the
  re-centred CS-6 and the three D-087 minimal coasters, Ntnl, gBV and jlTmt. The live CS-6
  picture was checked against the build by hash.

- 2026-09-30: #430, another session's ledger rows for the ten youtube reconstructions that had
  none, landed after Omar approved it. It had fallen behind master, so a fresh branch merged it
  and its two conflicts (the use-case pins and the catalog backlog's item numbers) were worked by
  hand, all 25 commits kept; the constructions check passes again without `CONSTRUCTIONS_OK=1`
  (3d-models #449). The gates now read `MERGE_HEAD` too, so a merge's inherited work is not
  treated as new (3d-models #447).

- 2026-10-04: the `consolidate-branches` skill turns the cleanup into one flow: inventory, prove
  what is merged by content (now also against each PR's merge commit, with British and American spellings of color folded),
  snapshot every tip under `refs/snapshots/<date>/` and push it, delete only what is proven dead,
  and land unmerged work through a fresh branch with every conflict worked by hand. The inventory
  script moved into the skill, and its keep lists and leave-alone worktrees moved into the
  skill's `rules.md`, read at run time.

- 2026-09-29: the branch inventory script (since 2026-10-04 in the `consolidate-branches` skill)
  lists, read-only, what a branch or worktree cleanup
  would lose across our repos: worktrees with uncommitted files, branches marked merged by
  ancestry or by content, stashes and open PRs. It ran the fifth cleanup; every branch it
  flagged as unique turned out to be landed, so unique means look, not keep (3d-models #415).

- 2026-09-28: the docs folders restructured. `tools/move_doc.py` moves a note and fixes every
  reference to it (3d-models #393). Guides went to `docs/guides/`, process notes to
  `docs/design/process/`, the construction notes beside the ledger, the printing notes to
  `docs/design/printing/`, the language, orb and pieces notes to `docs/design/`, and the coaster
  notes to `docs/design/coaster/` (3d-models #395, #396, #397, #398, #400). On 2026-09-29 the
  decisions log, plan and backlog moved into `docs/working-model/` (3d-models #413). bikar's
  pointers followed each move (bikar #279, #280, #281).

- 2026-09-28: the use-case map checks sibling-repo pointers again and fails when a sibling
  can't be read, instead of skipping it (3d-models #394). bikar's doc-pointer check reads a
  sibling at `origin/HEAD` and follows the folder moves (bikar #278).

- 2026-09-28: "color" everywhere, the American spelling Omar chose (D-083): text, file names
  and identifiers renamed in both repos, with a gate that fails on the British spelling coming
  back (3d-models #392, bikar #277).

- 2026-09-29: the gallery's old CS-10 picture is gone. Omar had read it as "a really weird
  coaster" (thread uqjg9s). `make coasters` then `make deploy` (gh-pages 202e464) redrew all 27
  coaster pictures from bikar e2b65c4. The CS-10 picture is now the symmetric 12-fold rosette.
  The build had stopped on the one coaster with no gallery card, CS-1 radial (bikar #270). That
  card is added, and "radial" is now in the style names. The deploy deleted only old Lab asset
  files that the new build replaces. Two more checks were broken and are fixed in the same PR.
  The coaster-pictures gate no longer applies its no-see-through-holes rule to openwork coasters,
  because their real openings look the same as a pinhole in the picture. The constructions
  ledger gains its cKYbKQvmsbs row (gallery-refresh PR).

- 2026-09-29: the stranded video-loop stack is on master. Omar accepted all eight records
  (D-084); they landed as one PR, #406–#410 were closed with a link to it, and the six
  `backlog-*` branches still on the remote were deleted after checking every line they added is
  on master (3d-models #421). The shared checkout was fast-forwarded to it.

- 2026-09-29: two items the fourth pass left are gone, checked 2026-09-29. hifth's remote
  now has only `main`, and youtube no longer has the `feat/any-source-video-fetch` branch.

- 2026-09-27: fourth pass, with 0 open PRs and 0 stashes in any repo. Every deleted branch
  was first proved dead, either by a content diff against its PR's merge commit or as an
  ancestor of it.
  - **3d-models:** 8 local branches deleted (7 `worktree-agent-*` and
    `docs/multicolor-constructions`) and 9 remote.
  - **bikar:** 5 local branches deleted and 6 remote (#252–#265); `bikar-main` was
    fast-forwarded to origin/main.
  - **qiyas:** `merge-nudge-hook` deleted from the remote.
  - **qiyas and 3d-model-hub:** main fast-forwarded in both.
  - **hifth:** 9 merged local branches deleted. Its remote branches are left for Omar
    (see the backlog).

- 2026-09-27 — Omar set the rule that the 3,000 included GitHub minutes a month have to be
  enough, and the spending limit stays at $0. To make that hold:
  - qiyas's CI, Secret scan and Decision coherence are hand-started, and the pre-push hook runs
    the fast test half (qiyas #34);
  - bikar deploys by hand, with `make web-deploy` or `gh workflow run deploy.yml` (bikar #267);
  - hifth's checks all run in its hooks, WebKit included, with the Linux golden set retired and
    Lighthouse run by hand (hifth #119);
  - the plan records these calls (3d-models #356; the ci-spend plan, retired 2026-11-11, is in git history at 266f32ce).
- 2026-09-25 — Omar logged in to LastPass and bikar's CI secrets were pushed with
  `make setup-secrets`: 4 Cloudflare Pages secrets and 6 GitHub Actions secrets, all overwriting
  existing ones; the 3 optional `QIYAS_*` secrets are not in `.env` and were skipped (no PR).
- 2026-09-25 — the link check now catches what a rename or delete breaks elsewhere, covers
  `.claude/` files, and `make validate` installs `tools/bambu`'s packages in a fresh worktree
  (3d-models #313).
- 2026-09-25 — the `manage-tasks` skill: moves a finished or open task to the right
  `docs/tasks/<loop>/` file, by the routing rules beside it (3d-models #311).
- 2026-09-25 — one backlog and done list per loop in `docs/tasks/<loop>/`; the old
  `docs/tasks/done.md` and `docs/working-model/backlog.md` split into them by loop (3d-models #309, #310).
- 2026-09-25 — full pass across all six repos: 3d-models is master + gh-pages, bikar main,
  youtube main; 0 open PRs, 0 stashes (3d-models #295–#298, #301; bikar #226, #244–#246).

## From the session task board, before the split

Finished work up to 2026-09-25 was kept on one list, `docs/tasks/done.md`, as ten snapshots
of the session task board; its sections were moved here by loop on 2026-09-25 (the file is in
git history). Numbers are the board's task ids, and **the board was renumbered more than
once**, so an id means something only under its snapshot: Snapshot 1's #14 and Snapshot 2's
#14 are different tasks. Each snapshot's own note below says which sequence it uses. Newest
first.

**▸ Snapshot 10 — 2026-09-25 (plates, color regions, the construction migrations,
the consolidation).** **A fresh id sequence, not a continuation of Snapshot 9.** The
live board was rebuilt from the continuation plan's later phases, so this snapshot's
`#1` is the plate composer and its `#37` is the B′ coords producer, not Snapshot 9's
color-regions id. Where a title below cites a second number (e.g. "#37 part 2",
"#17 — youtube verdict scripts"), that inner number is the *old* board's id the task
was carried over from. Decisions D-072…D-080 are in the [decisions log](../../working-model/decisions-log.md).
Still open on the board at this prune: `#4` (P4.3 print record for minis-01, waits on
a physical print), `#6` (P5.2 standard-size plate, after the CAL-CST-* bets are
measured), `#7` (P5.3 frame block, only if a public GeoGebra fixture needs it), `#9`
(push bikar CI secrets, owner-gated) and `#10` (session-reflect skill, after Omar
reviews the 3d-models #218 design).

### Skills, repo hygiene and the consolidation
- #27 — design-craft skills: `review-design` + `write-design` for newcomer-readable design docs (3d-models #278, d2a63a4)
- #31 — regenerate the calibrate bets file: **closed with no change.** The "28/26 → 32/28 drift" came from reading the lagging local `master` ref instead of `origin/master`; nothing needed regenerating
- #8 — youtube's O1/O2 verdict scripts (old #17) onto youtube main: four local branches hand-merged with a both-sides no-loss proof (youtube c22a60c, e34a7aa, 8d1eaeb; env-check fix 6d359b1; youtube has no remote)
- #40 — track the dotenvx-encrypted `.env`, gated by gitleaks + hook 11-env-encrypted (3d-models #299, efb708e)
- #41 — consolidate branches and worktrees: 3d-models is master + gh-pages, bikar is main, youtube is main (3d-models #295–#298; bikar #244, #245, #226)

**▸ Snapshot 6 — 2026-09-17 (the GeoGebra-constructions → naqsh → coaster prune).**
The live board was renumbered again after Snapshot 5, so these ids are a **fresh
sequence**: Snapshot 6's `#8` is the naqsh construction statements, not Snapshot
4/5's cross-repo ledger block, and its `#1` is the worktree setup, not Snapshot 2's
Q5 unstale. The board is the plan "GeoGebra constructions → naqsh (bikar) → STL
coasters, repeatably" (session plan file iterative-dazzling-finch; decisions
D-056…D-064 in the [decisions log](../../working-model/decisions-log.md); the record of what is
migrated is the [constructions ledger](../../constructions/ledger.md)). Task ids
`P<phase>.<n>` are the plan's own. Still open on the board at this prune: `#12`
(the later-phases umbrella: P3.1 skill, P3.3 catalog + `make coasters`, P4.x plate
composer, P5.x corpus), `#17` (youtube's O1/O2 verdict scripts sit on its local
`feat/ggb-coords` branch until Omar says main), `#21` (CI secrets sync,
owner-gated), `#24` (session-reflect implementation, waits on the `#23` design
review), `#27` (P2.7 disc coaster + the product-side coaster design doc, agent
running) and `#30` (P2.5 cookbook + P2.4 readability rules, agent running).

### Cross-repo hygiene + skills
- #14 — housekeeping after bikar #191/#192: doc-pointer baseline entries for the merged branches dropped (with #206), sibling pins refreshed and a `youtube:` pin added so the schema-mirror hook compares bikar's vendored AST schema against its producer (with #187)
- #15 — merged the queued bikar PRs in order — #196, #197, #199, #200 — polling only the required checks, merge at `MERGEABLE CLEAN`, never `--auto`
- #22 — troubleshoot-ci skill: a red check to a fix in its own PR, causes kept as a sidecar read at run time (bikar #199, 197fd7b)
- #23 — session-reflect skill design + research census (17 main + 176 subagent transcripts) proposing a census-generated FAQ with a falling-recurrence success metric (3d-models #218, open — awaiting Omar's review; finding: subagent transcripts are separate files, memory subagent-transcripts-are-separate-files)

**▸ Snapshot 5 — 2026-09-10 (the D-052 base-face-honesty cascade + contract-mirror
gate prune).** A **continuation of Snapshot 4's board, not a renumber** — the four
tasks Snapshot 4 listed as still-open all closed here (`#8` cross-repo ledger block,
`#49` the T9 outline↔solid gate, and the two bench/bet-gated Prints entries `#67` and
`#71`), and the D-052 cascade added `#81`–`#85` on the same sequence. So Snapshot 4's
and Snapshot 5's shared ids (`#8`, `#49`, `#67`, `#71`) are the *same* tasks, closed
here. Still open on the board at this prune: **`#81`** — make the orb breakdown pages
teach flat→sphere construction, the full plan beyond the T9 gate (spec: the plan
sunny-booping-crescent; new-session brief: breakdown-pages-kickoff; both shipped and were
retired 2026-11-11, in git history at 266f32ce).

### Cross-repo contract + gates (carried open from Snapshot 4, closed here)
- #8 — Make the cross-repo ledger check block, and add 3d-models to the loop
- #49 — T9: tie the drawn outline to the solid the manifest declares (base-face honesty consumer half, D-052)

**▸ Snapshot 4 — 2026-09-02 (the prints / wrap-morph / innerHTML prune).** Same
calendar day as Snapshot 3 but a **later, separate prune of a board that was
renumbered again** after it — so the ids below are yet another **fresh
sequence**: Snapshot 4's `#4` is the M4c lattice-walk fourth orb, not Snapshot
2's OrbViewer task or Snapshot 3's `#67`; Snapshot 4's `#72`/`#73` are the mesh-
gate widening and the d3 Phase-2 status overlay, not Snapshot 3's housekeeping
PR / rosette-N plan under the same numbers. Read every id under this date. These
are the completed entries of the board that carried the Prints tab (S-series),
the flat→sphere wrap morph and round-pattern breakdowns, the studio status page
and d3 Phase 2, and the master-commit and innerHTML-taint gates. Still open on
the board at this prune: `#8` (make the cross-repo ledger check block + add
3d-models to the loop); `#49` (T9 — tie the drawn outline to the manifest's
solid, owned by another concurrent session); bench-gated `#67` (Prints S2 —
print Plate 1 and fill the first run record at the bench); and bet-gated `#71`
(Prints S4 — add gate rule R3, two-way propagation, after the first bet flips,
blocked by `#67`).

### Hooks + security hygiene
- #74 — Refuse direct commits on main/master by hook, in both repos
- #36 — The as_of pin has no fixed point under squash merges — decide what the pin means
- #26 — Sweep the remaining interpolated-innerHTML sites in bikar's web package (DOM-node fixes + semgrep taint gate; bikar PR #162)

**▸ Snapshot 3 — 2026-09-02 (the d3 / 2.x prune).** The live board was renumbered
again after Snapshot 2, so the ids below are a **fresh sequence** — Snapshot 3's
`#29` is the bikar-studio public-surface keystone, not Snapshot 2's OrbViewer
camera-control `#29`. Read every id under this date. These are the completed
entries of the board that carried the d3 stream (Phases 1–3), the rosette
explorer's open ledger, the memory decomposition, the fourth orb and the studio
status page — the work [`plan.md`](../../working-model/plan.md) §2 rows 2.1–2.13 and §3 record in
detail. Still open on the board at this prune: user-decision `#36`
(coffee-house-sites#1); parked `#35` (publish the contract+schema under semver — the
breakage-detection skill and version-bump hook); standing `#50` (keep `plan.md`
current); printer-held `#37` (first physical print — **closed by fold-in** into
[the print-gated register](../coaster-pipeline/backlog.md) §3.8 in this same prune, not completed, exactly as
Snapshot 2 closed its `#3`); and the two live successors `#72` (this housekeeping
PR) and `#73` (the rosette-N seam-spacing-as-a-dial plan, the next session's focus).

### Memory decomposition, use-case map, and house hygiene
- #38 — Prune task-state out of memory; leave only a backlog pointer
- #39 — Branch/worktree hygiene: delete verified-merged branches, remove stale worktrees (all three repos)
- #40 — MEMORY.md index line held the whole shipped-record log — move it into the memory file, leave a hook
- #41 — Stop citing dead session-scoped ids in durable text
- #42 — Give the d3 stream a durable home in docs/working-model/backlog.md
- #43 — qiyas local main diverged 2 ahead / 3 behind — sentinel-verify before any reset, then reconcile
- #56 — Use-case map: re-pin bikar pointers at the drifted main, repair 9 moved anchors (+2 in orb-pipeline-map.md)
- #57 — Use-case map: add rows for the rosette explorer and orb instrument
- #58 — bikar check-lock-sync: the dry-run inherited npm_config_loglevel=silent and the FAIL message went empty

**▸ Snapshot 2 — 2026-08-30 (the renumbered board).** Fresh id namespace — see the
namespace warning in the header. Still open on the live board at this prune:
user-decision tasks #4 / #9 / #36; printer-independent tasks #8 / #10 / #26 / #49;
and prints-tab rungs #66–#71 — of which only #67 (print Plate 1 at the bench) and
#71 (R3, waits on the first settled bet) truly need a printer, the rest being
buildable now.

### Cross-repo, CI, and deploy hygiene (S2)
- #1 — Unstale the Q5 status in qiyas-wheelfield-validation-design.md
- #2 — Land the qiyas #20 O-7 cascade end to end
- #3 — Closed by moving the print queue into docs/working-model/backlog.md §3.8
- #6 — Retract the sh-wrapper overreach from PR #79 and PR #106
- #7 — Regenerate the cross-repo XREPO decision ledger
- #21 — Fix the semgrep XSS finding in bikar packages/web/src/sessions.ts
- #23 — Write the CLAUDE.md tenet: Actions billing must never block a merge or a deploy
- #24 — Close the gap between make local.ci and what GitHub Actions actually checks
- #25 — Build the deploy path that does not need a hosted runner
- #27 — Fix the three red local_only checks on sacred-patterns master
- #44 — Make the Lab e2e skip measure the Lab, not an env var
- #45 — Give ci-parity steps the env CI gives them, and make the GHCR login a step
- #59 — Rebase and land 3d-models #77 — orb pipeline map + line-number checks
- #60 — Rebase and land bikar #104 — revive two dead pre-commit guards, wire git to the tracked hook dir

**▸ Snapshot 1 — 2026-08-15 (the original prune).** Ids in the sections below are
the pre-renumber board.

### Repo operations + hygiene
- #18 — Track .claude/ in git with gitleaks pre-commit guard
- #77 — Clean up merged branches + PR the private-site gallery regen
- #78 — Work through sacred-patterns' 16 dependabot PRs
- #79 — Finish bikar worktree cleanup once the parallel session is idle
- #81 — Clean up hifth worktrees + merge without losing work
- #82 — Scan all repos for secrets before any push (gitleaks)
- #83 — Install the gitleaks pre-commit hook in repos that lack it
- #84 — Land the held local-guide plugin + reconcile mac-studio divergence (marketplace repo)
- #85 — Give amazon-scripts (ex work-scripts) a mac-studio remote and push its history
