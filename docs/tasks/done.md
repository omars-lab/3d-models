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
