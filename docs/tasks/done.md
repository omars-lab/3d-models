# Completed session tasks — frozen archive

**What this is:** a one-time snapshot (2026-08-15) of the completed entries in the
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
