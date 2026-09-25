# Completed session tasks — frozen archive

**What this is:** periodic wholesale snapshots (Snapshot 1: 2026-08-15; Snapshot
2: 2026-08-30) of the completed entries in the
Claude Code session task list, archived so the task numbers cited elsewhere
(decisions log entries, memory notes, PR descriptions — e.g. "task #84") keep a
referent after the live list was pruned. **What this is not:** a register anyone
maintains. Nothing gets added here except by another wholesale prune, and the
authoritative record of *what happened* stays where it always was — the
[decisions log](../decisions-log.md), the design docs, and git history in this
repo and bikar. (See [issue-register-evaluation](../issue-register-evaluation.md)
for why this repo does not keep live registers; this file is an index of spent
identifiers, not an exception to that.)

Numbers below are the session task ids. Tasks #1–#5 were pruned before this
archive existed. Open tasks at snapshot time — #10 (print a physical orb
prototype, user-held) and #119 (M4e: build the welded woven-overlap orb) —
remain on the live list.

**Two id namespaces live in this file.** The live board was renumbered after
Snapshot 1, so Snapshot 2's ids are a fresh sequence: old #14 (Snapshot 1, Orb
Lab configurator) and new #14 (Snapshot 2, Maclado stale cell views) are
different tasks. Always read an id under its snapshot's date.

---

**▸ Snapshot 1 — 2026-08-15 (the original prune).** Ids in the sections below are
the pre-renumber board.

## Orb engine + gallery (M0–M5, Orb Lab)

- #6 — PR + merge unpushed orb commits in all three repos (user-authorized)
- #7 — [user] Deploy 3d-models gallery (make deploy)
- #8 — [user] Deploy bikar studio to Cloudflare Pages
- #9 — [user] Contract amendment + qiyas-schema publish (owner-gated)
- #11 — Design doc: FDM-friendly hemisphere-split STL export
- #12 — Design rosette-oriented orbs (new .bkr patterns)
- #13 — [optional] Clear pre-existing qiyas/bikar gate debt
- #14 — Design doc: Orb Lab configurator (knobs + URL state + custom orbs)
- #15 — Implement M5 DSL params + Orb Lab P0 per design doc
- #16 — Implement Orb Lab P1 (breadth): all-six preset scripts, weave readouts, axis-view tabs, calibration sweeps
- #17 — Implement Orb Lab P2 (custom orbs + studio Dials) per orb-lab-p2 design doc
- #19 — [user] Redeploy studio to Cloudflare Pages (prod predates P2.5)

## Composition DSL (C1/C2, W1/W2) + validation gates

- #20 — Design doc: print validation gate (layer connectivity, islands, overhangs)
- #21 — Design doc: piece composition DSL (piece/port/connect/assembly)
- #22 — Design doc: tile + wall layout DSL (connectors, crops, layout rules)
- #23 — Adversarial grounding audit of the three design docs
- #24 — Prepare P1 strut-coupon .bkr variants + STLs (turnkey coupon plate)
- #25 — Add production-planning subsection to tile-wall design doc
- #26 — Implement C1: piece/hole/port/connect/assembly core in bikar
- #27 — Implement W1: tile + wall grid, crop clip, SVG wall render, validators
- #28 — Create maintain-use-cases skill + hooks in 3d-models
- #29 — Deep research + design doc: C2 ports/connect/assembly
- #30 — Deep research + design doc: W2 connectors, coupons, mounts
- #31 — Implement C2 in bikar: port/rod/assembly + fit profiles + parts export
- #32 — Implement W2 (clip connectors + keyhole mounts) in bikar
- #33 — Add a Claude Stop hook that mesh-gates changed pattern .bkr files
- #34 — [user] Push the 9 W2 commits in bikar
- #35 — Design doc: visual derivation worksheet for part composition
- #36 — Implement the print-validation gate (--check print) in bikar

## DSL formalization + tooling

- #37 — Design pass: AST as a schema-validated JSON IR
- #38 — Design doc: click-to-source for bikar
- #39 — Add statement spans + comment retention to bikar parser/lexer
- #40 — Design doc: DSL grammar formalization (BNF/EBNF)
- #41 — Fix preprocessSource column corruption in bikar lexer
- #42 — Evaluate an extend-the-dsl skill with hook-validated code pointers
- #43 — Write the EBNF grammar spec + differential corpus gate for the bikar DSL
- #44 — Close bikar PR #1; salvage its ideas into a fresh PR
- #45 — Evaluate an issue-register skill + reminder hooks
- #46 — Build the justified §6 changes + document the grounding-defect taxonomy
- #47 — Route bikar's two issue registers (§6 item 4, deferred)
- #48 — Q3: check unionPatternFaces against a deliberately-holed pattern

## Lego Lab (M6/M7, P0–P3, LDraw)

- #49 — M6: brick declaration + kernel3d brick module + validators V1–V10
- #50 — M7: anchor solver + grid gate + sweepGridFit
- #51 — P0: Lego Lab page with adjustable params
- #52 — P1: sweep strip, compatibility matrix, multi-piece export
- #53 — Build a design-artifact skill: /artifact-design → studio page
- #54 — Diagnose the solidifier's position-dependent degenerate triangles (Lego Lab §11 Q7)
- #55 — Land §11 Q8 decision (label the row) — D-007, note closed, §5.3 column
- #56 — Deploy the 3d-models gallery (user-approved 2026-07-31)
- #57 — Lego Lab §11 Q4/Q5/Q6 — the three open questions buildable without a coupon
- #58 — Author the LG-series coupon pack (Lego-Clutch-Coupon.bkr + STLs)
- #59 — Compiled design note for V12/V13 (design.html)
- #60 — [user] Deploy the gallery with V12/V13 + Lego Lab P2 custom mode
- #61 — Lego Lab P2: custom mode (code drawer, code= links, Open in Studio, draft)
- #62 — Spec then build Lego Lab P3 (print notes, adjustment toasts, LDraw .ldr export)
- #63 — Build the LDraw MPD emitter in bikar per §14.3
- #64 — Record P3 in the design doc + add the LDraw use-case row
- #65 — Research a CLI-drivable LDraw viewer + write the research note
- #66 — Resolve what W-F1 actually is (three docs disagree)
- #67 — Port check-doc-pointers to 3d-models (backticked paths must resolve)
- #68 — Catalog↔model coherence gate (the W-F1 defect, mechanized)
- #69 — Read the emitted LDraw MPD back with an independent parser
- #70 — Correct the LDraw research note §1.4 against the first real run
- #71 — Record D-009/D-010/D-011 in the decisions log
- #72 — Build the LDraw read-back preview panel into Lego Lab studio
- #73 — Establish emitted LDraw winding handedness before deciding BFC
- #74 — [user-authorized] Upload Brick-Stack.mpd to library.ldraw.org once
- #75 — Ship 0 BFC CERTIFY CCW in bikar's LDraw emitter (D-012)
- #76 — Correct the read-back triangle count and the "both sides kept" claim
- #80 — Graduate the winding-coherence check into a bikar test
- #91 — Settle the LDraw render experiment (LDView removed by the OS; three.js route run instead)
- #105 — Per-brick stud (pin) colour in LDraw export
- #106 — Design: LDraw thumbnail CLI + validation skill
- #107 — Build the LDraw multi-angle thumbnail CLI
- #108 — Build the LDraw render-validation skill
- #109 — PR + merge + use-case map + record the thumbnail CLI/skill
- #110 — Add a colour-presence gate to the thumbnail --check (bikar)
- #111 — Per-model render-notes + GPU-free catalog well-formedness test/hook (bikar)
- #112 — Record the visual checklist: design doc §16 + D-029 + skill + map (3d-models)

## Calibration + text-emit arc

- #86 — Make calibration-design §7's expectation table executable (make coupons)
- #87 — Catch a use-case as_of pin orphaned by a squash merge
- #88 — Add the four uncatalogued §3.5 print-gated items <!--count:quote--> to the prototype catalog
- #89 — Close §6.3's documentation residue: the angle-convention line and the misattribution cluster
- #90 — Land D-016/D-017/D-018 — the three §6.2 design decisions the user settled
- #92 — Close §6.3's unsourced-number cluster (the last live cluster)
- #93 — Build D-016's per-pair border validator in bikar
- #94 — Build D-017's frame statement + its band-width default in bikar
- #95 — Close the use-case validator's one-commit blind spot
- #96 — Research + design doc: text emit on printed parts
- #97 — T0: register CAL-TXT-01/CAL-TXT-02 as Calibrated records in bikar
- #98 — T1: bake the glyph constant + B1–B3 checks, with DM Sans asserted to fail
- #99 — T2: solidifyText + the text statement + the label-gap validator in the mesh gate
- #100 — T3: label the 23 calibration coupons and reprint the machine card
- #101 — Evaluate a bet→coupon→catalog-entry gate before writing one
- #102 — Bake a slashed zero into the face (needs Source Code Pro 2.x)
- #103 — Wire checkLabelGap/Counter/Charset into the mesh gate once there is text to gate
- #104 — Per-placement color in the assembly DSL (grounded names + codes)

## Maclado Family 3 (M1–M4d)

- #113 — Deep research: 9-spike "maclado" ribbon sphere
- #114 — Engine feasibility: 9-fold overlapping-wheel sphere in bikar
- #115 — Author grounded design doc: 9-spike maclado orb
- #116 — Implement the 9-spike maclado orb in bikar (M1–M5)
- #117 — M4c: quantized-separation placement spike (Option A, user-decided; D-031)
- #118 — M4d: overlap spike — rim crossings + weave feasibility (user-decided; D-032)

## Repo operations + hygiene

- #18 — Track .claude/ in git with gitleaks pre-commit guard
- #77 — Clean up merged branches + PR the private-site gallery regen
- #78 — Work through sacred-patterns' 16 dependabot PRs
- #79 — Finish bikar worktree cleanup once the parallel session is idle
- #81 — Clean up hifth worktrees + merge without losing work
- #82 — Scan all repos for secrets before any push (gitleaks)
- #83 — Install the gitleaks pre-commit hook in repos that lack it
- #84 — Land the held local-guide plugin + reconcile mac-studio divergence (marketplace repo)
- #85 — Give amazon-scripts (ex work-scripts) a mac-studio remote and push its history

---

**▸ Snapshot 2 — 2026-08-30 (the renumbered board).** Fresh id namespace — see the
namespace warning in the header. Still open on the live board at this prune:
user-decision tasks #4 / #9 / #36; printer-independent tasks #8 / #10 / #26 / #49;
and prints-tab rungs #66–#71 — of which only #67 (print Plate 1 at the bench) and
#71 (R3, waits on the first settled bet) truly need a printer, the rest being
buildable now.

## Cross-repo, CI, and deploy hygiene (S2)

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

## Per-orb breakdown + timelapse arc (S2)

- #11 — Answer: is there a per-orb review UX, a page per orb?
- #12 — Build a per-orb breakdown page
- #13 — Design the per-orb construction report (staged build-up)
- #14 — Fix Maclado-9-Overlap's stale shipped cell views
- #15 — Investigate the second overlap band at [1.38, 1.60]
- #16 — Build the bikar stage-sequence generator + --format timelapse
- #17 — Ship the timelapse invariant gate
- #18 — Close the open questions in the timelapse design's §11
- #19 — Re-derive the rasterisation cost the research file marks NOT VERIFIED
- #20 — Fix the dangling §6.3 reference in derivation-worksheet-design.md
- #22 — Merge the two open timelapse PRs: bikar #107 and 3d-models #83
- #28 — bikar: --turntable <n> on --format timelapse
- #29 — bikar: OrbViewer public camera control
- #30 — bikar: build packages/lab/breakdown.html
- #31 — bikar: register breakdown in vite config + catalogue
- #32 — 3d-models: use-case map entry for the breakdown
- #33 — 3d-models: wire breakdown into build and deploy
- #34 — 3d-models: link the breakdown from gallery and Orb Lab
- #35 — Give Maclado-9-Overlap a camera sweep — the one orb that most needs it has none
- #37 — bikar: meanDot + baseSolidCells in kernel3d
- #38 — bikar: OrbViewStyle depth cues + per-unit highlight in the renderer
- #39 — bikar CLI: flat/base/complete frames, highlight, transition, ribbon turntable
- #40 — bikar: breakdown page tells the five beats, family-parameterised
- #41 — 3d-models: gallery restyle + Makefile keys + regeneration
- #42 — 3d-models: timelapse_gate.py with both by-design failures
- #43 — 3d-models: doc amendments + decision entry for the breakdown rework
- #46 — bikar: persistent base-solid scaffold under every stage frame
- #47 — bikar: fix the turntable limb — back-face cull for display frames
- #48 — 3d-models: regenerate, amend the timelapse gate, redeploy

## Woven-orb amplitude re-cut — D-039 through D-045 (S2)

- #50 — Re-cut the five woven orbs' amplitude so they print unfused
- #51 — Re-pin the two by-design tests the amplitude re-cut silenced
- #52 — Re-record the ribbon instrument: three-repo qiyas cascade
- #53 — P1 · Every woven orb's declared amplitude floor fuses — narrow the ranges behind a fixture test
- #54 — P2 · The 2D weave shatters — share the mesh's offset function, cascade APPROVED
- #55 — Absorbed by #54 · The silhouette circle is not the orb's edge
- #56 — Absorbed by #54 · Stage frames draw each loop pre-diced for crossings not in the picture
- #57 — P4 · Two teaching defects on the breakdown page
- #58 — P3 · Closed by measurement inverting its premise — overlap-requires-weave is a kernel fact (D-044)

## Decision handbacks + prints tab S1 (S2)

- #61 — Hand back #4 (M4c orb) as a visual decision artifact
- #62 — Hand back #36 (as_of pin under squash merges) as a visual decision artifact
- #63 — Hand back #9 (this repo's D-log joins the decision hub) as a visual decision artifact
- #64 — Prints tab: record the 4 resolved decisions + preserve the design in-repo
- #65 — Prints tab S1: write the run-record format + one filled Plate-1 example

---

**▸ Snapshot 3 — 2026-09-02 (the d3 / 2.x prune).** The live board was renumbered
again after Snapshot 2, so the ids below are a **fresh sequence** — Snapshot 3's
`#29` is the bikar-studio public-surface keystone, not Snapshot 2's OrbViewer
camera-control `#29`. Read every id under this date. These are the completed
entries of the board that carried the d3 stream (Phases 1–3), the rosette
explorer's open ledger, the memory decomposition, the fourth orb and the studio
status page — the work [`../plan.md`](../plan.md) §2 rows 2.1–2.13 and §3 record in
detail. Still open on the board at this prune: user-decision `#36`
(coffee-house-sites#1); parked `#35` (publish the contract+schema under semver — the
breakage-detection skill and version-bump hook); standing `#50` (keep `plan.md`
current); printer-held `#37` (first physical print — **closed by fold-in** into
[`../backlog.md`](../backlog.md) §3.8 in this same prune, not completed, exactly as
Snapshot 2 closed its `#3`); and the two live successors `#72` (this housekeeping
PR) and `#73` (the rosette-N seam-spacing-as-a-dial plan, the next session's focus).

## d3 stream — the studio instruments (Phases 1–3)

- #29 — DECISION: does bikar-studio stay a public surface? (keystone) — org-gated, internet-reachable
- #30 — qiyas: type the data-model endpoints so the schema reaches OpenAPI
- #31 — d3 Phase 1: rosette explorer as the reference d3 surface
- #32 — d3 Phase 2: the full orb-view instrument — orb .bkr → orb-view SVG → qiyas encode ref + degraded recon → diff → status overlay, joined by id
- #33 — d3 Phase 1 follow-on 1.3: pattern picker for other .bkr in the rosette explorer
- #34 — d3 Phase 1 follow-on Track 2: generic dial schema from a .bkr's parameters
- #44 — 2.1.a orb-view SVG from an orb .bkr inside packages/web
- #45 — 2.1.b getting a browser-rendered SVG into qiyas (POST /diff inline, D-API-5)
- #46 — 2.1.c the join across the two id namespaces
- #47 — 2.1.d the /orb-instrument page (rosette-explorer shape, status join in viz-d3)
- #48 — 2.1.e registration (route table, page marker, routing test, public surface) + fixture
- #49 — 2.1.f record the Phase 2 ship
- #51 — bikar qiyas-schema Scores lacked drop/surplus/max_drift — regenerate from the current qiyas OpenAPI
- #61 — 2.4 d3 Phase 3: unify vocabulary across explorers + sacred-patterns (Q-VOCAB)
- #62 — 2.4.a preserve the Q-VOCAB vocabulary survey as checked-in research
- #63 — 2.4.b design doc: vocabulary convergence
- #64 — 2.4.c execute A↔B convergence in bikar (renames + join refactor + tests)
- #65 — 2.4.d execute the sacred-patterns structural refactor
- #66 — 2.4.e record the Phase 3 ship

## Rosette explorer — the open ledger (2.2)

- #52 — 6.6.1 widen the roster past Rosette-N/Star-N (girih, hex-field, rational-repeat)
- #53 — 6.6.2 ground the rosette explorer design doc (audit, apply, appendices)
- #54 — 6.6.3 plates as data: PLATES → data/plates.json, gated at load
- #55 — 6.6.4 interior-tube cap dial (clutch/material trade, kernel floor un-overridable)

## Memory decomposition, use-case map, and house hygiene

- #38 — Prune task-state out of memory; leave only a backlog pointer
- #39 — Branch/worktree hygiene: delete verified-merged branches, remove stale worktrees (all three repos)
- #40 — MEMORY.md index line held the whole shipped-record log — move it into the memory file, leave a hook
- #41 — Stop citing dead session-scoped ids in durable text
- #42 — Give the d3 stream a durable home in docs/backlog.md
- #43 — qiyas local main diverged 2 ahead / 3 behind — sentinel-verify before any reset, then reconcile
- #56 — Use-case map: re-pin bikar pointers at the drifted main, repair 9 moved anchors (+2 in orb-pipeline-map.md)
- #57 — Use-case map: add rows for the rosette explorer and orb instrument
- #58 — bikar check-lock-sync: the dry-run inherited npm_config_loglevel=silent and the FAIL message went empty

## Decision hub, the fourth orb, and the studio status page

- #59 — 2.3 split islamic-orb-project.md (152 KB) into one-fact topic memories; archive the log
- #60 — 2.12 decision hub: cross-repo D-0xx index + citation gate
- #67 — 2.10 fourth orb on the M4c/D-031 lattice walk (built as process measurement)
- #68 — 2.10.a design doc for the lattice-walk orb, grounded
- #69 — 2.10.b bikar kernel build: the 18-wheel lattice-walk open shell
- #70 — 2.10.c 3d-models integration + the skill decision (eight detectors, zero instructions → no skill) + record
- #71 — 2.13 studio status page (three files-only provenance facts, standalone in 3d-models)

---

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

## Prints tab (S-series)

- #66 — Prints tab S3: ship prints_gate.py with R1/R2/R4 + hook 39-prints
- #68 — Prints tab S5: delete the empty Iteration log from every catalog entry
- #69 — Prints tab S6: build the rendered docs/prints.md tab
- #70 — Prints tab S7: vendor the prints.html lab page (audience: gallery visitors)

## Orb breakdown + flat→sphere wrap morph

- #76 — Flat→sphere wrap morph for the breakdown page (deferred from the teach-construction plan)
- #77 — Wrap morph, bikar PR: kernel blend t + writeMorph + page caption (docs/orb-wrap-morph-design.md §6)
- #78 — Wrap morph, 3d-models PR: timelapse gate junction + count rules, make orbs, doc statuses
- #79 — Make `make orbs` robust to non-views orbs (round-pattern STL-only)
- #80 — bikar: give round-pattern orbs a breakdown (--format timelapse/views for base sphere + place)
- #72 — Widen bikar `--check mesh` to the orbMesh path (sphere orbs were silently un-gated)

## d3 / studio / decision hub

- #10 — Give the studio a status page fed from the repos, not typed
- #73 — d3 Phase 2: build the qiyas status overlay from the measured {id,x,y,status} join
- #9 — Decide how 3d-models' D-0xx log joins the decision hub

## Orbs + sweeps

- #4 — Build the fourth orb on the M4c quantized lattice walk, as the skill-vs-gate measurement
- #75 — Move the three Rosette-N param explorations out of stashes into a pushed sweep record

## Hooks + security hygiene

- #74 — Refuse direct commits on main/master by hook, in both repos
- #36 — The as_of pin has no fixed point under squash merges — decide what the pin means
- #26 — Sweep the remaining interpolated-innerHTML sites in bikar's web package (DOM-node fixes + semgrep taint gate; bikar PR #162)

---

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

## Cross-repo contract + gates (carried open from Snapshot 4, closed here)

- #8 — Make the cross-repo ledger check block, and add 3d-models to the loop
- #49 — T9: tie the drawn outline to the solid the manifest declares (base-face honesty consumer half, D-052)

## Prints tab (S-series, bench/bet-gated, closed at the bench)

- #67 — Prints tab S2: print Plate 1 and fill the first run record at the bench
- #71 — Prints tab S4: add gate rule R3 (two-way propagation) after the first bet flips (was blocked by #67)

## D-052 base-face-honesty cascade (four repos: sacred-patterns → bikar → qiyas → 3d-models)

- #82 — Cascade step 2, bikar producer half: gt-emitter conditional `orb_base_face` (face-kind only) + GT_SCHEMA_VERSION 1.29 (bikar squash 09390b8, all 5 CI checks green, composites unmoved)
- #83 — Cascade step 3, qiyas validator half: mirror to v1.6 + parse-level inertness witness (no validate_dsl_contract.py change, no gt re-record — schema ≥1.24 satisfied by 1.29)
- #84 — (b) Migration/change-history pointer added to the canonical contract (sacred-patterns #52, ed7206a)
- #85 — (c) The mirror↔canonical invariant gate: contract_mirror.py + hook 42-contract-mirror + make validate-contract-mirror (3d-models #171, ef9b627)

---

**▸ Snapshot 6 — 2026-09-17 (the GeoGebra-constructions → naqsh → coaster prune).**
The live board was renumbered again after Snapshot 5, so these ids are a **fresh
sequence**: Snapshot 6's `#8` is the naqsh construction statements, not Snapshot
4/5's cross-repo ledger block, and its `#1` is the worktree setup, not Snapshot 2's
Q5 unstale. The board is the plan "GeoGebra constructions → naqsh (bikar) → STL
coasters, repeatably" (session plan file iterative-dazzling-finch; decisions
D-056…D-064 in the [decisions log](../decisions-log.md); the record of what is
migrated is the [constructions ledger](../constructions/ledger.md)). Task ids
`P<phase>.<n>` are the plan's own. Still open on the board at this prune: `#12`
(the later-phases umbrella: P3.1 skill, P3.3 catalog + `make coasters`, P4.x plate
composer, P5.x corpus), `#17` (youtube's O1/O2 verdict scripts sit on its local
`feat/ggb-coords` branch until Omar says main), `#21` (CI secrets sync,
owner-gated), `#24` (session-reflect implementation, waits on the `#23` design
review), `#27` (P2.7 disc coaster + the product-side coaster design doc, agent
running) and `#30` (P2.5 cookbook + P2.4 readability rules, agent running).

## Phase 0 — ground and decide (docs only)

- #1 — P0.5 worktrees: `3d-models-constructions` (also the `THREED_MODELS_DIR` every bikar commit's registry hook reads), `bikar-constructions`, youtube per its CLAUDE.md (commits on `main` only when asked)
- #2 — P0.1 research survey, preserved verbatim under a provenance header (3d-models #187, 18ba47c)
- #3 — P0.2 umbrella design doc — architecture, rubric + option tables, AST contract, ledger, skill; Default/Validator markers green (3d-models #187)
- #4 — P0.3 decisions D-A…D-I appended as D-056…D-064 (3d-models #187) — D-055 was taken by master mid-flight, so the whole block renumbered before merge (memory: decision-id-collision-recurred)
- #5 — P0.4 naqsh names the language, bikar keeps the engine: decision note, doc titles, bikar-dsl skill line, memory naqsh-is-bikar-dsl-synonym (bikar #191, 4c81a52)

## Phase 1 — languages made robust (grammar as source of truth)

- #6 — P1.1 youtube EBNF for `.ggb-commands` + G3-twin conformance test + G2-twin vocabulary fixture; no parser rewrite (youtube main ff58490)
- #7 — P1.3 youtube `--ast-json` + Pydantic schema with a regenerate-and-byte-compare test (youtube main ff58490); schema vendored byte-identical into bikar's qiyas-schema package (bikar #192, c244794)
- #8 — P1.4 naqsh construction statements: (a) named points — `point <id> = …`, bare-name PointRefs, `pick`, a *defined* intersect order (bikar #193, 489758c); (b)–(d) transforms, derived lines/circles, `regular` polygons, rotate inside mirror (bikar #197, 93b0216)
- #9 — P1.5 printer, re-scoped: the first agent looped 9.5 h / 1,348 tool calls / zero files written trying to invert the whole parser for a full-corpus round-trip (memory: subagent-loop-signal); shipped instead as a printer for the statement subset the importer emits, inside bikar #200; the full-corpus round-trip is a follow-on, not a claim
- #10 — P1.2b youtube coordinate oracle: Playwright + GeoGebra Apps API → `coords.json`, `--scad` → OpenSCAD `reference.stl` (youtube `feat/ggb-coords` 86147cb, 16a7202 — local, see `#17`)
- #13 — P1.6 kernel half: height-field coaster kernel, structural validators with hard FAIL fixtures, CAL-CST-01…05 registered, design doc coaster-height-field in bikar (bikar #194, 6c6a54d)
- #26 — P1.6 DSL half: the `coaster` declaration — grammar §10.3, parser, evaluator, `--piece` render, three Tier-0 witnesses, 37 tests (bikar #203, 6b89f6f). Carried finding: CV4 (bottom bevel > 45°) is unexpressible in the surface syntax because `edge` mints an equal rise, so it is exercised only at the validator level; the parser's fall-through keyword list had omitted `mural`
- #19 — P1.7 highlighting generated from one source: bikar tmLanguage + keywords JSON + lab editor overlay, checked in a real browser (bikar #196, 4456607); youtube Prism grammar + keyword mirror byte-identical (youtube `feat/ggb-highlight` aa6cbe8, ed04bbe — local)

## Phase 2 — transpiler, first constructions, oracles

- #11 — P2.1 `bikar import geogebra` (lowering, fail-loud coverage) + P2.2 first slice GimTvN9hw4U golden and fixture (bikar #200, 3c79b46); oracles on the golden: O1 PASS 23/0, O2 PASS (SSIM 0.983), O3 PASS coverage 1.000
- #25 — P2.3 fast coaster: `--piece`/`--depth` emit the slice-1 `piece Coaster` trailer, unit range corrected to 8..25 (bikar #201, 50169f1); mini at unit 9 = 40.5 × 46.8 × 4.0 mm, standard at unit 20 = 90.0 × 103.9 × 4.0 mm, mesh + linkage `--check` PASS on both
- #16 — P2.3b `qiyas mesh compare`, the O3 oracle (qiyas #32, bcd84fa) with the dropped-edge variant as the by-design FAIL; finding carried into the equivalence doc: bikar's extrude solidifies the silhouette, so O3 at the flat stage cannot see interior edges
- #18 — construction-equivalence design doc + measurements research file (3d-models #187) and CAL-EQV-01, the O2 coverage floor (bikar #195, dcbfb40)
- #28 — P2.6 second slice 7apC5Q9QS-8, 144/144 lowered (bikar #202, c1c9063). The O2 recall-0.01 FAIL was two defects: a stale square hero export (guard + issue note on youtube `feat/ggb-coords` 49e7e1a; memory o2-stale-hero-export) and the lowerer drawing exported-and-hidden labels (drawn = exported ∧ ¬hidden, unit test + golden); after both O1 PASS 144/0, O2 PASS 1.000/1.000

## Phase 3 — the ledger

- #20 — P3.2 constructions ledger + gate + hook `44-constructions` + SessionStart nudge, self-tested in a fresh worktree, `M60LJNNslHU` as the "no piece by design" row the gate must not skip (3d-models #206, a0dc2f7)
- #29 — first two migrated rows, verdicts copied from the validators not re-typed, design docs linked (3d-models #219, 73ec316)

## Cross-repo hygiene + skills

- #14 — housekeeping after bikar #191/#192: doc-pointer baseline entries for the merged branches dropped (with #206), sibling pins refreshed and a `youtube:` pin added so the schema-mirror hook compares bikar's vendored AST schema against its producer (with #187)
- #15 — merged the queued bikar PRs in order — #196, #197, #199, #200 — polling only the required checks, merge at `MERGEABLE CLEAN`, never `--auto`
- #22 — troubleshoot-ci skill: a red check to a fix in its own PR, causes kept as a sidecar read at run time (bikar #199, 197fd7b)
- #23 — session-reflect skill design + research census (17 main + 176 subagent transcripts) proposing a census-generated FAQ with a falling-recurrence success metric (3d-models #218, open — awaiting Omar's review; finding: subagent transcripts are separate files, memory subagent-transcripts-are-separate-files)

---

**▸ Snapshot 7 — 2026-09-17 (the first-print campaign — bambu CLI, the print-model
skill, and X2D bring-up prep).** The live board was renumbered again after Snapshot
6, so these ids are a **fresh sequence**: Snapshot 7's `#8` is the X2D live-hardware
bring-up, not Snapshot 6's naqsh construction statements or Snapshot 4/5's ledger
block. The board is the plan "First-print campaign — turning the X2D into settled
calibration data" (session plan binary-tickling-kay; decisions D-053/D-054 in the
[decisions log](../decisions-log.md), D-055 amending D-054). The A-numbers
(`A1…A11`) are the plan's own Phase-A ids. Still open on the board at this prune:
**`#9`** — slice a real plate + the first owner-gated dispatch, which stays
CAL-bet-gated and owner-physical (filament is loaded; the remaining steps are Omar's
caliper/instruments, the Plate 1 slice-to-`.3mf`, and `bambu print send --record`).
The Phase-A slice profile + MC-4 pre-flight (A4/A5, tasks `#21`/`#22`) landed via PR
#185; their whole-card slice + auto_brim finding landed separately in #210.

## Bring-up + the bambu CLI foundation

- #8 — X2D live-hardware bring-up (LAN + Developer Mode + transport proof). The touchscreen toggle is owner-physical; transport was proven read-only end-to-end by the first-party MQTT backend (`status show` → live temps/state off the device), memory bambu-x2d-bringup
- #10 — merge the bambu phases 1–3 PR: the `setup-bambu-x2d` skill + `tools/bambu` CLI (3d-models #177)
- #11 — merge the blog PR documenting the printer bring-up (omars-lab.github.io #225)
- #12 — refresh the use-case map's stale as_of base + repair 18 drifted bikar anchors (3d-models #178)
- #13 — encrypt the blog `.env` with dotenvx + a commit-time secret hook (blog repo)
- #14 — `bambu setup discover`: passive, print-safe LAN printer discovery, zero-touch (3d-models #179)
- #15 — carry the dotenvx v1→v2 fixes back to bikar (bikar)
- #16 — a stale `build/orb-breakdown` dist tripped the 38-timelapse gate (74 findings); rebuilt so the gate reads current
- #17 — pin/migrate dotenvx v1→v2 in bikar + the blog env-sync (an unpinned `npx` was resolving 2.28) (bikar, blog)
- #26 — `A9`: `bambu print list` — enumerate print history from the records (3d-models #181)
- #27 — the day-to-day bambu-CLI usage skill, the front door over the verbs (3d-models #181)
- #30 — first-party MQTT `status` backend that retires the spawned MCP for reads (D-055, amends D-054) (3d-models #188)

## Phase A — X2D software prep (no printer, no touchscreen)

- #18 — `A1`: register `bambu-x2d` as a `PrintTarget` in bikar `machines.ts` (bikar)
- #19 — `A2`: decide the dual-nozzle representation — X2D rides single-nozzle-labelled FDM, `PrintTarget` not widened (D-053) (3d-models #222, relanded onto master; original #182 fell behind master and was superseded)
- #20 — `A3`: re-verify the machine card reproduces (`make coupons` + `make validate-coupons`, local — proves the Plate-1 substrate intact before asking for filament)
- #21 — `A4`: ready the slice path for the X2D profile — proven headless against a real X2D profile, the known-good preset trio recorded in the bench sheet (3d-models #185; the whole-card slice + auto_brim footgun recorded in #210)
- #22 — `A5`: eyeball the MC-4 overhang fan in the slicer before filament — pre-flight eyeballed supports-off (3d-models #185)
- #23 — `A6`: capture the X2D-profile-gap discovery in memory/skill — the machines.ts gap + a SKILL.md troubleshoot row for the missing machine target (memory bambu-x2d-bringup; 3d-models #184)
- #24 — `A7`: the pre-populated Plate 1 bench sheet Omar carries to the printer (3d-models #180)
- #25 — `A8`: encode the print→photograph→compare→verdict loop — the compare-verdict gate R5 + the prototype seams (3d-models #180)
- #28 — `A10`: grounded survey of Bambu control/slicing transport options, research checked in under a provenance header (3d-models #223, relanded; original #183 superseded)
- #29 — `A11`: the `tools/bambu` CLI design doc — the two-layer split, mermaid, a recorded decision (D-054) (3d-models #223, relanded)

## The print-model skill (the sage-operator driver)

- #31 — scaffold the print-model skill dir + SKILL.md front door (3d-models #193)
- #32 — filament discovery: the `bambu filament` verb reads AMS trays + external spool, read-only (3d-models #192)
- #33 — best-orientation reasoning for a piece (3d-models #196)
- #34 — settings reasoning: infill / supports / brim / raft (3d-models #197)
- #35 — the AskUserQuestion filament-selection step (3d-models #195)
- #36 — the per-print plan artifact + slice/preview + the owner-gate handoff (3d-models #199)
- #37 — print-issue feedback + the recovery loop (3d-models #200)
- #42 — plate arrangement: pack repeated pieces on a grid, rotate-to-fit (3d-models #203)
- #43 — nozzle-diameter recommendation (0.2 / 0.4 / 0.6 / 0.8) (3d-models #204)
- #44 — the proactive-advisory sweep: fill unused bed, scale-up, catch footguns (3d-models #205)
- #45 — the best-practices reference, grounded in full + our real examples (3d-models #208)
- #46 — the self-healing loop: physical-iteration findings graduate into best-practices examples (3d-models #209)
- #49 — the task-tracked lifecycle + the questions-intro + the sage input-critique principle (3d-models #220)

## Print metadata + the prints gate

- #38 — the print-metadata schema: lifecycle status, feedback, sheet↔print + repeated-element mapping (rules R6–R9) (3d-models #198)
- #39 — the freshness rules R10–R14: a record's status must match its evidence (3d-models #201)
- #40 — the print-history query: what we printed AND how — `print list --how` + filters (3d-models #202)

## Design docs

- #41 — `docs/print-model-design.md`: lifecycle, mermaid diagrams, decisions + the run-time rubric (3d-models #191)
- #47 — the plate-builder frontend-experience design doc (the served operator front end; now the seed of the private 3d-model-hub repo, Option D)
- #48 — reconcile the print-metadata design with Omar's PMR answers + the estimation-slice primitive (3d-models #217)

---

**▸ Snapshot 8 — 2026-09-17 (first-party dispatch + the dogfooding gates).** A
**continuation of Snapshot 7's board, not a renumber** — `#50`–`#57` sit on the same
fresh sequence Snapshot 7 opened (`#8` = X2D bring-up), so Snapshot 8's `#50` is the
first-party dispatch port, not Snapshot 1's Lego M7 anchor solver or Snapshot 2's
woven re-cut `#50`. These closed the transport gap and the pre-dispatch honesty gates
that stood between the sliced Plate 1 and a send. Still open on the board at this
prune: **`#9`** — dogfood guide-print to a physical Plate 1 print, now blocked only by
`#9b` (the warnings sidecar, owned by the concurrent slice-preflight session) and the
owner-gated physical send; its dispatch dependency (`#50`) is delivered and proven by
`--dry-run`. `#9a` (the checked-in ground-truth diff surface) shipped with the
guide-print pre-send-gate work in this same prune.

## First-party dispatch + the pre-dispatch gates

- #50 — port `bambu print send` to first-party dispatch: FTPS :990 implicit-TLS upload + MQTT `print.project_file`, retiring the uninstallable griches MCP from the dispatch path; 18 builder unit tests, `--dry-run` review surface, pivot doc first-party-dispatch.md, the three X2D-UNCONFIRMED CAL fields (bed_type/ams_mapping/md5) exposed as flags (3d-models #243)
- #51 — `bambu slice open <plate.3mf>`: a first-class read-only verb that opens a sliced plate in Bambu Studio for visual approval and dispatches nothing, replacing the raw `open -a` (3d-models, guide-print step 2)
- #52 — the pre-dispatch warnings gate: capture Studio's own slicing warnings, classify against expected-by-design, and fail-closed on an unexpected one (or a missing `<plate>.warnings.json` sidecar) so `print send` never dispatches what Studio would warn about
- #53 — reason the X2D dual-nozzle filament-grouping mode in print-model + `bambu slice --filament-map-mode` — a no-op on a single-material plate (Studio's Filament-Saving default is already correct), a real choice only on a multi-filament plate
- #54 — fold the dogfooding findings into guide-print: warnings triage, grouping mode, open-in-Studio, the GUI one-click alternative
- #55 — slice at `--debug 2` so Studio's slicing warnings surface headlessly into the sidecar the gate reads
- #56 — correct the sub-floor-rung assumption: only `MC2Wall04` (0.4 mm) floats by design; the 0.6 / 0.8 / 1.0 mm rungs slice clean and must not expect the warning (measured 2026-09-17)
- #57 — guard against re-slicing an already-sliced `.3mf` (its embedded custom presets aren't in the bundle, so a re-slice silently loses them)
- #9a — the checked-in ground-truth diff surface: the exact Plate-1 `project_file` payload to diff against a BambuStudio GUI capture, appended to first-party-dispatch.md; the guide-print step-4 pre-send gate + the "are we ready to print?" checklist shipped alongside

---

**▸ Snapshot 9 — 2026-09-17 (the coaster forms — shape v2, interlock, Coaster Lab,
minimal).** A **continuation of Snapshot 6's constructions board, not of Snapshot
7/8's first-print board**: `#27` and `#30` are the two "agent running" ids Snapshot 6
left open, and `#31`–`#38` were minted on that same sequence afterwards — so this
snapshot's `#33` is coaster shape v2, not an id on the first-print board (Snapshot 7's
`#13` is the blog `.env`). The board is still the plan "GeoGebra constructions →
naqsh (bikar) → STL coasters" (session plan iterative-dazzling-finch), now carried
by its self-contained continuation
[coaster-border-continuation](../../.claude/plans/coaster-border-continuation.md);
decisions D-065…D-071 in the [decisions log](../decisions-log.md). Still open on
the board at this prune: `#12` (the later-phases umbrella: P4.x plate composer,
P5.x corpus), `#17` (youtube's O1/O2 verdict scripts on its local `feat/ggb-coords`
until Omar says main), `#21` (CI secrets sync, owner-gated), `#24` (session-reflect
implementation, waits on the `#23` design review), **`#36`** (the coaster border,
D-071: design shipped in 3d-models #257, bikar implementation checkpointed at
f5d1781 on `feat/coaster-border`, validators/importer/docs remaining per the
continuation plan §2) and `#37` (colour regions → per-body export → filament map).

## Phase 2/3 remainder — the first coasters into the catalog

- #27 — P2.7 disc coaster from the GimTvN9hw4U golden: mini `size=40` / standard `size=90`, `--check` both; the importer emits the coaster block itself, `--coaster` beside `--piece` (bikar #207, 05d12ff); the product-side coaster design doc + D-065 (3d-models #227, 6bb053b)
- #30 — P2.5 GeoGebra → naqsh cookbook, held to the importer by a conformance test + the G3 fence glob (bikar #204, 035b0df); P2.4 readability rules + `validate --style constructions` (bikar #206, 1d42690)
- #31 — P3.3 catalog + gallery + `make coasters` for the two migrated coasters, CS-1/CS-2 (3d-models #244, 41a4939)
- #32 — P3.1 `import-construction` skill: GeoGebra construction → naqsh → coaster, rubric read at run time (3d-models #230, 6c06590)

## Coaster forms (D-066…D-070)

- #33 — shape v2: outline fitted to the art (hex / square / octagon), `rotate` and `margin` knobs, CV7 enclosure, the "clipped" claim retracted — design + D-066…D-068 (3d-models #239, 50de1ba); bikar implementation (bikar #208, 48b28b9); CS-1/CS-2 re-vendored from bikar main at shape v2 (3d-models #247, e47ce9a)
- #34 — interlock: self-mating half-edge dovetail on every straight edge, D-069 — design (3d-models #245, 97e6952); bikar grammar `interlock`, slotted ring + exact wall, CV8/CV9, `--interlock` importer flag, CAL-CST-06 (bikar #209, 89b63fd); CS-3 + mated-pair gallery previews, D-069 → built (3d-models #250, 1ab40f2)
- #35 — Coaster Lab in bikar's lab on the Orb Lab pattern, D-067: live structural-check panel, the knobs ARE the param block, roster pinned to `patterns/Constructions/*-coaster.bkr` by a presets test that sweeps mini and standard (bikar #210, 3b7b6f8); vendored into the gallery (3d-models #253, 2f600c3); pointer baseline shrunk once its paths resolved on bikar main (3d-models #254, b33606e)
- #38 — minimal coasters: `outline pattern`, the strap network itself extruded with a rounded top edge and no slab; CAL-CST-07 free-standing floor, CV10 round-over check — design D-070 (3d-models #251, 8688876); bikar (bikar #211, 5152cfd); CS-4 + gallery pair, D-070 → built (3d-models #255, fa86bab)

---

**▸ Snapshot 10 — 2026-09-25 (plates, colour regions, the construction migrations,
the consolidation).** **A fresh id sequence, not a continuation of Snapshot 9.** The
live board was rebuilt from the continuation plan's later phases, so this snapshot's
`#1` is the plate composer and its `#37` is the B′ coords producer, not Snapshot 9's
colour-regions id. Where a title below cites a second number (e.g. "#37 part 2",
"#17 — youtube verdict scripts"), that inner number is the *old* board's id the task
was carried over from. Decisions D-072…D-080 are in the [decisions log](../decisions-log.md).
Still open on the board at this prune: `#4` (P4.3 print record for minis-01, waits on
a physical print), `#6` (P5.2 standard-size plate, after the CAL-CST-* bets are
measured), `#7` (P5.3 frame block, only if a public GeoGebra fixture needs it), `#9`
(push bikar CI secrets, owner-gated) and `#10` (session-reflect skill, after Omar
reviews the 3d-models #218 design).

## Plates and the bambu CLI (P4.x)

- #1 — P4.1 `bambu slice compose`, the plate composer with a shared `it-<sha12>` helper — design D-072 (3d-models #264, 83703d4); implementation (3d-models #265, bd83fe6)
- #3 — P4.2 minis-01, the first coaster compose plate (3d-models #280, c450fd4)
- #11 — bambu CLI help gate: a generated flag reference held in sync by hook 45 (3d-models #273, fc8ecd8)
- #19 — `bambu ams` read verb + filament-sync: reconcile a plate's logical AMS slots to the live trays by colour (3d-models #285, 7c022fa)

## Coaster colour regions → per-body export → AMS filament map (old #37)

- #2 — the umbrella: a coaster's colour regions become separate bodies that land on separate AMS slots, plus a Coaster Lab knob — design D-073 (3d-models #264, 83703d4); closed by #12–#18 below
- #12 — part 2: `color <region> <PaletteName>` grammar + evaluator (bikar #213, a325d73)
- #13 — §6 research: the headless BambuStudio 3MF → AMS filament-assignment contract (3d-models #267, 871762a)
- #14 — part 3: `--format parts` region body split, pinch detection and `--pinch` strategies, D-074 (bikar #214, 726d567); the `.parts.json` sidecar (bikar #215, 1649389)
- #15 — part 4: palette name → AMS logical slot map for coaster plates, D-075 (3d-models #271, 58612a3)
- #16 — part 5: Coaster Lab per-region colour knob + full per-region 3D tint (bikar #216, 6746237); D-076 recorded (3d-models #272, 1a79fef)
- #17 — K7 reconcile of the design doc's §4 error phases against bikar's parse-time checks (3d-models #267, 871762a)
- #18 — part 4b-ii: multi-part coaster → AMS 3MF assembler + the headless-crash pivot (3d-models #274, d96ea8c); `slice coaster` verb end to end, bikar `--format parts` → `--load-filaments` (3d-models #275, ce86591)

## Coaster kernel features

- #20–#24 — twist / helix extrude, T1–T5: lofted-ring solid, the `twist <deg>` statement and its conflict refusal, evaluator + render wiring, CV12 + CAL-CST-08, Lab preset + tests (bikar #217, 42ce6dd); CAL-CST-08 mirrored into the calibrate bets file (3d-models #279, 2c1dbb0; count fix #281, 5ed8031)
- #25 — radial-band colouring: the ring a polygon sits in is a print region, D-078 — design (3d-models #277, 6d67693); `bands` verb (bikar #219, 103caa8); ring colour onto the height field (bikar #220, f68a536); `--format parts` split by ring colour (bikar #221, 2e45cd5)
- #26 — emit-golden fix: `emitBkr` round-trips palette + color blocks (bikar #218, 60b5ff4)
- #28, #30 — rods relief: investigated as a Coaster Lab option, then built as path A, half-round height-field straps (bikar #226, 5a588e5)

## Construction migrations (P5.1)

- #5 — P5.1 umbrella, the five remaining constructions; ledger at 8 migrated / 1 by design / 0 remaining; closed by #29 and #32–#39
- #29 — lEfWSogWscs (Tomb of Itimad ad-Daula): bikar golden (bikar #225, 28f3989); CS-7 standard STL + catalog entry (3d-models #284, 4d7f072)
- #32 — rDuxHF3xMOc, 8-fold star rosette with Sequences: list-literal transforms lowered (bikar #227, 2da2e68); CS-8 (3d-models #287, eadf605)
- #33 — sDO9fpu76v8, Royal Alcazar pattern (bikar #228, cc35d6d); CS-11 (3d-models #294, 350d134)
- #34, #38 — nmEjCTzMbDg, n-fold flower, the first open line-art migration, via the B′ self-bootstrapped coords (bikar #243, 87ea3b4); CS-9 (3d-models #291, 34ad03b)
- #35 — n3IidKfXE1I, variable-angled 12-6-4 star rosette (bikar #229, 0191780); CS-10 (3d-models #294, 350d134)
- #36 — the self-improvement loop: each migration fills the gap the last one hit — point reflection (bikar #230), circle inversion (bikar #231), conic loci (bikar #232), arc straps (bikar #233), CircularArc/Circle/Segment lowering (bikar #234); written up as a tenet (3d-models #286, fe0b764)
- #37 — B′: `--emit-coords` / evaluatedCoords, bikar self-bootstraps `cached_coords` (bikar #236, 07f1bf3); decision D-080 (3d-models #290, 265a4e3)
- #39 — the printer emits `connect points`, nmEj's last engine gap (bikar #238, f201377)

## Skills, repo hygiene and the consolidation

- #27 — design-craft skills: `review-design` + `write-design` for newcomer-readable design docs (3d-models #278, d2a63a4)
- #31 — regenerate the calibrate bets file: **closed with no change.** The "28/26 → 32/28 drift" came from reading the lagging local `master` ref instead of `origin/master`; nothing needed regenerating
- #8 — youtube's O1/O2 verdict scripts (old #17) onto youtube main: four local branches hand-merged with a both-sides no-loss proof (youtube c22a60c, e34a7aa, 8d1eaeb; env-check fix 6d359b1; youtube has no remote)
- #40 — track the dotenvx-encrypted `.env`, gated by gitleaks + hook 11-env-encrypted (3d-models #299, efb708e)
- #41 — consolidate branches and worktrees: 3d-models is master + gh-pages, bikar is main, youtube is main (3d-models #295–#298; bikar #244, #245, #226)
