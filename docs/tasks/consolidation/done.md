# Done — consolidation

Newest first: date, what was merged or cleaned up, PRs. Backlog: [`backlog.md`](backlog.md).

- 2026-09-25 — the link check now catches what a rename or delete breaks elsewhere, covers
  `.claude/` files, and `make validate` installs `tools/bambu`'s packages in a fresh worktree
  (3d-models #313).
- 2026-09-25 — the `manage-tasks` skill: moves a finished or open task to the right
  `docs/tasks/<loop>/` file, by the routing rules beside it (3d-models #311).
- 2026-09-25 — one backlog and done list per loop in `docs/tasks/<loop>/`; the old
  `docs/tasks/done.md` and `docs/backlog.md` split into them by loop (3d-models #309, #310).
- 2026-09-25 — full pass across all six repos: 3d-models is master + gh-pages, bikar main,
  youtube main; 0 open PRs, 0 stashes (3d-models #295–#298, #301; bikar #226, #244–#246).

## From the session task board, before the split

Finished work up to 2026-09-25 was kept on one list, `docs/tasks/done.md`, as ten snapshots
of the session task board; its sections were moved here by loop on 2026-09-25 (the file is in
git history). Numbers are the board's task ids, and **the board was renumbered more than
once**, so an id means something only under its snapshot: Snapshot 1's #14 and Snapshot 2's
#14 are different tasks. Each snapshot's own note below says which sequence it uses. Newest
first.

**▸ Snapshot 10 — 2026-09-25 (plates, colour regions, the construction migrations,
the consolidation).** **A fresh id sequence, not a continuation of Snapshot 9.** The
live board was rebuilt from the continuation plan's later phases, so this snapshot's
`#1` is the plate composer and its `#37` is the B′ coords producer, not Snapshot 9's
colour-regions id. Where a title below cites a second number (e.g. "#37 part 2",
"#17 — youtube verdict scripts"), that inner number is the *old* board's id the task
was carried over from. Decisions D-072…D-080 are in the [decisions log](../../decisions-log.md).
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
D-056…D-064 in the [decisions log](../../decisions-log.md); the record of what is
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
teach flat→sphere construction, the full plan beyond the T9 gate (spec:
`.claude/plans/sunny-booping-crescent.md`; new-session brief:
`.claude/plans/breakdown-pages-kickoff.md`).

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
status page — the work [`plan.md`](../../plan.md) §2 rows 2.1–2.13 and §3 record in
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
- #42 — Give the d3 stream a durable home in docs/backlog.md
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
- #3 — Closed by moving the print queue into docs/backlog.md §3.8
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
