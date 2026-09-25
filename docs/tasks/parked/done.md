# Done — work no loop owns

Newest first: date, what shipped, PR. Open work: [`backlog.md`](backlog.md).

## From the session task board, before the split

Finished work up to 2026-09-25 was kept on one list, `docs/tasks/done.md`, as ten snapshots
of the session task board; its sections were moved here by loop on 2026-09-25 (the file is in
git history). Numbers are the board's task ids, and **the board was renumbered more than
once**, so an id means something only under its snapshot: Snapshot 1's #14 and Snapshot 2's
#14 are different tasks. Each snapshot's own note below says which sequence it uses. Newest
first.

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

### D-052 base-face-honesty cascade (four repos: sacred-patterns → bikar → qiyas → 3d-models)
- #82 — Cascade step 2, bikar producer half: gt-emitter conditional `orb_base_face` (face-kind only) + GT_SCHEMA_VERSION 1.29 (bikar squash 09390b8, all 5 CI checks green, composites unmoved)
- #83 — Cascade step 3, qiyas validator half: mirror to v1.6 + parse-level inertness witness (no validate_dsl_contract.py change, no gt re-record — schema ≥1.24 satisfied by 1.29)
- #84 — (b) Migration/change-history pointer added to the canonical contract (sacred-patterns #52, ed7206a)
- #85 — (c) The mirror↔canonical invariant gate: contract_mirror.py + hook 42-contract-mirror + make validate-contract-mirror (3d-models #171, ef9b627)

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

### Orb breakdown + flat→sphere wrap morph
- #76 — Flat→sphere wrap morph for the breakdown page (deferred from the teach-construction plan)
- #77 — Wrap morph, bikar PR: kernel blend t + writeMorph + page caption (docs/orb-wrap-morph-design.md §6)
- #78 — Wrap morph, 3d-models PR: timelapse gate junction + count rules, make orbs, doc statuses
- #79 — Make `make orbs` robust to non-views orbs (round-pattern STL-only)
- #80 — bikar: give round-pattern orbs a breakdown (--format timelapse/views for base sphere + place)
- #72 — Widen bikar `--check mesh` to the orbMesh path (sphere orbs were silently un-gated)

### d3 / studio / decision hub
- #10 — Give the studio a status page fed from the repos, not typed
- #73 — d3 Phase 2: build the qiyas status overlay from the measured {id,x,y,status} join
- #9 — Decide how 3d-models' D-0xx log joins the decision hub

### Orbs + sweeps
- #4 — Build the fourth orb on the M4c quantized lattice walk, as the skill-vs-gate measurement
- #75 — Move the three Rosette-N param explorations out of stashes into a pushed sweep record

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

### d3 stream — the studio instruments (Phases 1–3)
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

### Rosette explorer — the open ledger (2.2)
- #52 — 6.6.1 widen the roster past Rosette-N/Star-N (girih, hex-field, rational-repeat)
- #53 — 6.6.2 ground the rosette explorer design doc (audit, apply, appendices)
- #54 — 6.6.3 plates as data: PLATES → data/plates.json, gated at load
- #55 — 6.6.4 interior-tube cap dial (clutch/material trade, kernel floor un-overridable)

### Decision hub, the fourth orb, and the studio status page
- #59 — 2.3 split islamic-orb-project.md (152 KB) into one-fact topic memories; archive the log
- #60 — 2.12 decision hub: cross-repo D-0xx index + citation gate
- #67 — 2.10 fourth orb on the M4c/D-031 lattice walk (built as process measurement)
- #68 — 2.10.a design doc for the lattice-walk orb, grounded
- #69 — 2.10.b bikar kernel build: the 18-wheel lattice-walk open shell
- #70 — 2.10.c 3d-models integration + the skill decision (eight detectors, zero instructions → no skill) + record
- #71 — 2.13 studio status page (three files-only provenance facts, standalone in 3d-models)

**▸ Snapshot 2 — 2026-08-30 (the renumbered board).** Fresh id namespace — see the
namespace warning in the header. Still open on the live board at this prune:
user-decision tasks #4 / #9 / #36; printer-independent tasks #8 / #10 / #26 / #49;
and prints-tab rungs #66–#71 — of which only #67 (print Plate 1 at the bench) and
#71 (R3, waits on the first settled bet) truly need a printer, the rest being
buildable now.

### Per-orb breakdown + timelapse arc (S2)
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

### Woven-orb amplitude re-cut — D-039 through D-045 (S2)
- #50 — Re-cut the five woven orbs' amplitude so they print unfused
- #51 — Re-pin the two by-design tests the amplitude re-cut silenced
- #52 — Re-record the ribbon instrument: three-repo qiyas cascade
- #53 — P1 · Every woven orb's declared amplitude floor fuses — narrow the ranges behind a fixture test
- #54 — P2 · The 2D weave shatters — share the mesh's offset function, cascade APPROVED
- #55 — Absorbed by #54 · The silhouette circle is not the orb's edge
- #56 — Absorbed by #54 · Stage frames draw each loop pre-diced for crossings not in the picture
- #57 — P4 · Two teaching defects on the breakdown page
- #58 — P3 · Closed by measurement inverting its premise — overlap-requires-weave is a kernel fact (D-044)

**▸ Snapshot 1 — 2026-08-15 (the original prune).** Ids in the sections below are
the pre-renumber board.

### Orb engine + gallery (M0–M5, Orb Lab)
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

### Composition DSL (C1/C2, W1/W2) + validation gates
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

### DSL formalization + tooling
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

### Lego Lab (M6/M7, P0–P3, LDraw)
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

### Maclado Family 3 (M1–M4d)
- #113 — Deep research: 9-spike "maclado" ribbon sphere
- #114 — Engine feasibility: 9-fold overlapping-wheel sphere in bikar
- #115 — Author grounded design doc: 9-spike maclado orb
- #116 — Implement the 9-spike maclado orb in bikar (M1–M5)
- #117 — M4c: quantized-separation placement spike (Option A, user-decided; D-031)
- #118 — M4d: overlap spike — rim crossings + weave feasibility (user-decided; D-032)

## Before the loops: non-printer residue kept in the print backlog

These two sections were §6.3 and §6.4 of `docs/backlog.md` until 2026-09-25, when that
file was split into the loop backlogs (it is in git history). Both are closed or shipped.
Their §3 and §8 references mean the sections of the
[print-gated register](../coaster-pipeline/backlog.md), which kept its numbering.

### The research files' own residue — mostly not printer work

All 17 files in [`research/`](../../research) were swept for their enumerated residue.
Only three use a literal "what could not be grounded" heading; the seven
grounding audits enumerate theirs under **"Misgrounded or missing citations"**,
the two field surveys under **"Errata"**, and
[`hemisphere-split-grounding-audit.md`](../../research/hemisphere-split-grounding-audit.md)
does the printer/no-printer split itself under "UNGROUNDED residue — ARGUED vs
EMPIRICAL". Those are the lists this section reports on; it is not a claim about
every sentence in those files.

The shape of the result is the useful part: **the large majority of the residue
is citation repair, a fetch, a spec reading or a design decision.** Only about a
dozen items across all 17 files need a printer, and nearly all of them are
already owned by a coupon in §3. The rest is work that can be done today — and a
re-check on 2026-08-03 found some of it had *already* been done before this
section was written, which is the subject of §8's fifth check.

Three clusters are worth naming because they change documents rather than
constants. **All three are now closed** — two were already closed when this
section was written, and the third closed on 2026-08-03; see each entry.

- **The unsourced-number cluster — closed 2026-08-03, and it produced a gate.**
  `±0.1–0.2 mm printer accuracy` was a load-bearing premise in three docs with
  **no vendor source**: the lego audit grepped the Bambu X1C and A1 spec PDFs for
  `accur|precis|toler|repeat|deviat` and got **zero matches in both**, and the
  Prusa MK4S page claims "Perfect Dimensional Accuracy" with no number.

  What this entry got wrong is *why* it was still open. The audit that killed the
  number ran on **2026-07-29** and the fix was applied the same week to
  [`lego-lab-design.md`](../../lego-lab-design.md) §3.5 (rebuilt from measured
  repeatability, σ ≈ 0.02 mm) and to
  [`print-validation-design.md`](../../print-validation-design.md) Appendix A. It was
  never applied to [`tile-wall-design.md`](../../tile-wall-design.md), which is a
  different *lineage* — a different survey, a different audit — that happens to
  share the number. So this was not research debt awaiting a fetch; it was a
  correction that stopped at a document boundary and sat for five days inside a
  section headed "the load-bearing facts". Both tile-wall sites now carry the
  rebuilt argument, and
  [`research/tile-craft-field-survey.md`](../../research/tile-craft-field-survey.md)
  carries errata item 9 (its body stays verbatim, per the survey convention).

  **The check that would have caught it** is `docs_gate.py`'s new **D4**: a
  hand-entered list of withdrawn literals that may not be restated as fact
  outside `docs/research/`. Its limit is recorded rather than papered over — run
  against the pre-fix file it reports **one** finding, not two, because
  tile-wall §2 wrote the number as a *multiple* ("10–20× beyond FDM tolerance")
  and left no literal to match. See
  [`grounding-defect-taxonomy.md`](../../grounding-defect-taxonomy.md) §"Why D4
  exists".

  The four adjacent items were checked in the same pass and none is live: the
  "0.02 mm clutch band" is corrected in `lego-lab-design.md` §3.5, the
  "7–10% PETG design band" is withdrawn as apparently synthesized in
  [`w2-connector-design.md`](../../w2-connector-design.md) B.1 with the ~2% endpoint
  re-derived three ways, the "PETG ~30% stronger interlayer bonding" claim never
  reached a design doc and carries errata item 3 in the survey, and the
  "0.2–0.5 mm FDM bow" is labelled a placeholder in both docs that use it — it
  is the one item in this cluster a print settles, and it is owned by the W2 clip
  coupon in §3.
- **The misattribution cluster — closed, verified 2026-08-03.** Several quotes
  were credited to the wrong page. All four are now corrected in the design docs:
  the build123d quotes cite
  [juraph](https://juraph.com/kiwi/playing_with_build123d/) with HN 41548945 kept
  as secondary discussion, the "5–30×" figure cites
  [openscad PR #4533](https://github.com/openscad/openscad/pull/4533) with
  discussion #387 named as the independent 11× report, the Q-factor equations are
  credited to McMaster & Lee of **AlliedSignal**, and the 1–3 mm bow is re-homed
  to WhyItFailed. The garbled "3m36s → 3.4s" benchmark is deleted rather than
  re-cited. Anchors:
  [`piece-composition-design.md`](../../piece-composition-design.md) Appendix A and
  [`w2-connector-design.md`](../../w2-connector-design.md) §3 and Appendix A.
  One of them
  ([`research/piece-composition-grounding-audit.md`](../../research/piece-composition-grounding-audit.md))
  is the **K2 instance the taxonomy cites**: BOSL2's `screws.scad` was inside
  the surveyed set and separates the distinction the doc claimed everyone
  conflates. That correction landed too.
  The *survey* files still read as first delivered, and should — research is
  checked in verbatim, so a survey carries an **Errata** section recording what
  the audit found rather than a rewritten body. Reading a survey line and a doc
  line side by side will therefore keep showing the old attribution next to the
  new one; that is the convention working, not residue.
- **The angle-convention line — closed; it was never open.** `print-validation`'s
  audit asked for one sentence saying whether θ is measured from vertical or
  horizontal, and the taxonomy calls this out under K10 as "a silent porting
  hazard" because the two conventions agree at exactly the 45° default. The
  sentence shipped in the *same commit as the audit* (`7fdb7e1`, 2026-07-27) and
  is in [`print-validation-design.md`](../../print-validation-design.md) under the
  support-map step: θ from vertical, `d = h·tan θ`, with PrusaSlicer's `h/tan θ`
  from horizontal named beside it. This entry was wrong for six days.

One item there needs flagging as a *tooling* lesson rather than a finding:
[`research/derivation-visualization-survey.md`](../../research/derivation-visualization-survey.md)
records that a WebFetch against a GitHub **search** URL returned "Your search did
not match any code" for a feature that exists in four source files — a confirmed
false negative. Anyone re-running the ungrounded items above should not trust
that path.


### The d3 stream — the only live non-printer work, and it lived elsewhere

Added 2026-09-01. Until this entry §6 listed nothing from the d3 workstream even
though it is the only non-printer work actually in flight — it lived in the
session-scoped task list and in two design docs. This subsection is a **pointer,
not a copy**: the owning sections are
[`d3-integration-design.md`](../../d3-integration-design.md) §4 (phases) and
[`rosette-pin-explorer-design.md`](../../rosette-pin-explorer-design.md) §6 (tracks),
and a number that changes there is not re-typed here.

| Item | State | Owner |
|---|---|---|
| Phase 1 — the rosette explorer on the real kernel (`/rosette-explorer` in bikar-studio) | shipped 2026-08-31 (bikar #123, #125, #127) | d3 doc §4; explorer doc §6 Track 1 |
| Track 2 — dials generated from each pattern's own compiled schema | shipped 2026-08-31 | explorer doc §6 Track 2 |
| Phase 2 — the full orb-view instrument: orb `.bkr` → orb-view SVG → qiyas encode (ref + degraded recon) → `/diff` → status overlay on the bikar-rendered SVG | shipped 2026-09-01 (bikar #129, #132; qiyas #26 D-API-5) as `/orb-instrument` | d3 doc §4 Phase 2 and §5 Q-DATA |
| Explorer coupons — physical pin and clutch checks | printer-gated, §3.2 | explorer doc §6 |
| The Lego open ledger — the residue of the whole Lego stream sorted by what gates it: four unblocked items (widen the roster, ground the explorer doc, plates as data, the tube cap), two download-gated viewers, one decision (§11 Q6's proxy), and the printer-held coupons that §3.2 already owns | added 2026-09-01; the four unblocked items are tracked in the task system | explorer doc §6.6 |
| The cross-repo governance stream — the tasks that had no plan anchor until the 2026-09-01 orb-tooling audit: how this repo's decisions log joins a decision hub (a user decision; [D-004](../../decisions-log.md) chose the local format and rejected mirroring bikar's generator), whether the cross-repo ledger check should block and bring this repo into the loop (gated on that decision), and a studio status page rendered from the repos the way bikar's studio index is rendered from its catalogue, never typed | added 2026-09-01; all on the task board, the hub decision gates the other two; no number re-typed here | bikar's cross-repo-dependencies doc and decision ledger; [D-004](../../decisions-log.md) |

Only the explorer-coupons row needs a printer, which is exactly why the stream was invisible
to a file organised around what a printer unblocks.

The governance row, still open, moved on 2026-09-25 to
[the parked backlog](backlog.md), "Cross-repo governance". The rest of
this table is shipped and stays as the record.
