# Plan: First-print campaign — turning the X2D into settled calibration data

> Supersedes this file's prior contents (the `setup-bambu-x2d` skill + `tools/bambu` CLI + blog
> build plan, fully executed: merged as #177 / #179 / blog #227, and recoverable from git history).
> That plan built the *capability*; this plan spends it.

## Context

A physical **Bambu X2D** now exists on the LAN (`192.168.1.186`, serial `20P6AJ641401412`,
firmware `01.02.00.00`). For the entire life of this project **nothing has ever been printed** —
`docs/tasks/coaster-pipeline/backlog.md` opens with *"PLANNING DOCUMENT, NOTHING MEASURED"* and the bet registry agrees:
**21 registered CAL bets · 21 `Calibrated` records — 21 provisional, 0 measured**. Every physical
number in every design doc is either quoted from someone else's literature or an explicitly-labelled
unmeasured default.

The printer is therefore **not a build blocker — it is a truth blocker** (`docs/tasks/coaster-pipeline/backlog.md` §1). All
geometry is authored and mesh-verified; the machine card renders, the Lego engine phases are
complete, the orbs render. What is missing is a single honest measurement of *this* machine. This
plan sequences the work that owning a printer unblocks, in the order the backlog proves is the only
honest one, and makes the physical / owner-gated steps explicit rather than assuming them.

**Printing stays owner-gated.** No CAL bet is settled, dispatch verbs default to confirm-before-send,
and the first filament committed is Omar's call (memory *owner-gated-and-on-hold*). This plan gets
everything to the edge of that gate and names exactly what only Omar can do.

## What already exists (grounded 2026-09-16, not assumed)

- **The `bambu` CLI is complete** — all five groups implemented, no stubs: `setup {discover,doctor,mcp,studio}`,
  `status {show,monitor,camera}`, `slice plate`, `print {send,pause,resume,stop}`, `validate {mesh,plate,record}`.
- **The `setup-bambu-x2d` skill + `rubric.md`** exist in `.claude/skills/setup-bambu-x2d/`.
- **`make coupons` / `make validate-coupons` + `build/verify_machine_card.py`** exist; the 23 machine-card
  rungs were rendered to `build/stls/coupons/machine-card/` on 2026-08-03 and match `calibration-design.md`
  §7's table (euler / watertight / minFeature / triangles / volume, summing to 89.7 cm³). `build/` is gitignored.
- **Discovery is done** — the X2D was found via passive SSDP (`bambu setup discover`, print-safe).

## The one meaningful gap this campaign surfaces (a growth discovery)

The machine card measures the **(printer, material, nozzle, profile)** tuple, and *every* number below is
scoped to it (`protocol.md`). But bikar's machine menu — `bikar:packages/knobs/src/machines.ts` `MACHINES`
— ships **10 `PrintTarget` entries and none is the X2D**: only `bambu-x1c`, `bambu-p1s`, `bambu-a1`,
`bambu-a1-mini` on the Bambu side, all single-nozzle. The `PrintTarget` schema is
`{ id, label, xMm, yMm, zMm, process: 'fdm'|'powder' }` — **no nozzle-diameter field and no
dual-nozzle / tool-count concept at all.** So:

- A reading cannot honestly be recorded against "the X2D" until an X2D `PrintTarget` exists.
- The X2D's dual nozzle cannot be represented as more than a label without a **bikar schema change** —
  which is a decision to make deliberately (decisions-log entry), not a silent widening.

## Two gates stand in front of Plate 1

1. **Live-hardware bring-up (#8) — owner physical action.** The printer is reachable but still
   **cloud-bound**. It needs **LAN Mode + Developer Mode toggled ON at the touchscreen** (surfaces the
   access code). Nothing in software flips it. Then the CLI path closes it: read access code → `bambu setup mcp`
   (writes gitignored `.mcp.json`; token via env, never committed) → `bambu setup doctor` → `bambu status show`
   (first read-only proof of transport — live temps/AMS). Memory: *bambu-x2d-bringup*.
2. **The X2D profile gap (above)** — must be closed before any reading lands, but is **software I can do now**.

## Phase A — software prep I can do now (no printer, no touchscreen)

Each its own branch → PR (PR-flow for all repos; stage by name; no `git add -A`).

1. **Register the X2D as a `PrintTarget` in bikar** (`packages/knobs/src/machines.ts`): add one `MACHINES`
   entry — `id: 'bambu-x2d'`, label, `process: 'fdm'`, build volume `xMm/yMm/zMm` **read off the machine /
   Bambu Studio, not invented** (confirm from the device during bring-up; leave a clearly-marked TODO if
   unknown at author time rather than guessing a number — the repo forbids invented numbers). Own PR in bikar.
2. **Decide the dual-nozzle representation** — open a `docs/decisions-log.md` entry (grab the next free
   D-0xx carefully, memory *decision-id-collision*): either (a) X2D rides as a single-nozzle-labelled FDM
   target for now (numbers still valid per-tuple; dual-nozzle is a slicer concern, not a knob concern), or
   (b) widen the `PrintTarget` schema. Recommend (a) — a migration never buys a fork; widen only when a
   knob actually needs to branch on nozzle count. Record the reasoning either way.
3. **Re-verify the machine card reproduces** — `make coupons` (regenerates the 23 rungs) then
   `make validate-coupons` (mutates a scratch doc 7 ways, confirms the verifier fires). Proves the Plate-1
   substrate is intact before we ask Omar for filament.
4. **Ready the slice path for the X2D profile** — `bambu slice plate <machine-card model>` against a real
   Bambu Studio X2D dual-nozzle profile (stable 2.7.x, fall back to 2.8.x beta per the old plan's decision).
   Record the chosen profile name; it is part of the header, not a preference.
5. **Eyeball the MC-4 overhang fan in the slicer** before filament — `calibration-design.md` §8 flags
   *"no raster render was eyeballed"* as MC-4's known weakness, and MC-4 is the piece whose failure mode is
   a silently-wrong dimension. Load the sliced plate; look at the fan.
6. **Capture the X2D-profile-gap discovery in memory / skill** (standing growth preference) — update
   *bambu-x2d-bringup* (or a new memory) with the machines.ts gap + the dual-nozzle schema decision, and
   add a Troubleshooting line to `setup-bambu-x2d` SKILL.md if the profile choice was non-obvious.
7. **Produce the Plate 1 bench sheet** — the physical artifact Omar carries to the printer. `protocol.md`
   ships a *blank* sheet; the value-add is a **pre-populated one**: for each MC rung, the nominal, the
   ladder steps, the instrument, and the PASS/borderline/FAIL scale already filled in (drawn from the tables
   in the next section), plus the profile-header block to fill at the bench and the "a failed rung is a
   result" reminder. Ships as `docs/prints/plate-1-bench-sheet.md` (or printable). Non-gated; I can write it now.
8. **Encode the print → photograph → compare → verdict loop (extend + gate, NOT a new skill).** Today the
   loop's two seams are un-owned: no step scripts *taking* the physical photos, and nothing compares a reading
   to its written expectation (the record schema has no `expected`/`verdict` field; `prints_gate.py` only
   *counts* readings). The repo precedent is explicit — `docs/dsl-extension-skill-evaluation.md` and
   `docs/issue-register-evaluation.md` both concluded *"no new skill, a gate instead"* — so:
   - **Extend `prototype/SKILL.md`** (already "the other half of the `calibrate` handoff") to script the two
     seams: (a) a per-coupon **photograph checklist** (what to shoot — the fit pairs, the fan underside, the
     four warp corners, the tower bases/elephant's foot), and (b) a **compare step** that reads each reading
     against the bench-sheet expectation and records a verdict, using §2's three-outcome vocabulary
     (`brackets` / `every-rung-passes` / `every-rung-fails`) plus the hand scales (`press/snug/sliding/free`,
     `clean/sagging/drooping/failed`).
   - **Add `expected` + `verdict` fields** to the record schema (`docs/prints-tab-design.md` `readings[]` /
     `objects[]`) so the comparison is structured data, not prose, and **add a `prints_gate.py` check**: any
     reading carrying `settles: CAL-…` must carry an `expected` and a `verdict`. This turns the compare seam
     into an enforced invariant — the repo's "a gate over a skill" idiom — and finally motivates shipping the
     designed-but-unshipped **gate R3** (two-way propagation to `bets.md`). Wire it into `make validate-prints`.
   - This is the durable answer to *"do we print, photograph, run physical tests, and check they match — as a
     skill?"*: after this, `prototype` walks the whole loop and the gate refuses a record that measures a bet
     without stating what was expected and whether it matched.

## Phase B — owner-gated physical steps (Omar; I hand these off explicitly)

- **B1. Toggle LAN Mode + Developer Mode** on the X2D touchscreen; read the access code. (Unblocks #8.)
- **B2. Buy / locate the instruments** the protocol assumes (`docs/tasks/coaster-pipeline/backlog.md` §4 not-done #4): a caliper
  (make + resolution recorded, zeroed at session start), a flat reference (granite plate or float glass) and
  feeler gauges for MC-5, plus **at least one real LEGO plate and one real LEGO 2×4 brick** for the LG series.
  Bags + a marker — rung identity does not survive onto the part; a mis-bagged rung "is worse than a missing one."
- **B3. Record the profile header** *before any measuring* — the card's series note says the header **is** the
  deliverable and "the numbers are meaningless without it."
- **B4. First dispatch** — `bambu print send --record` for Plate 1. Owner's call; confirm-before-send.

## Phase C — the print campaign (each plate settles, then propagates)

Order is fixed by *downstream work unblocked per plate* (`docs/tasks/coaster-pipeline/backlog.md` §2), not document age.

- **Plate 1 — machine card, all six coupons, one session** (`MC-1`…`MC-6`; 89.7 cm³ / ≈111 g PLA).
  *Why nothing else can go first:* settles **10 of 21 bets / 15 of 21 records** by measuring the machine
  tuple once. Printing any design coupon first measures the printer *inside* a clip/brick/orb.
  Slicer settings are **measurements not preferences** (§4 table): MC-4 fan supports **OFF**; MC-6 towers
  bare plate, **no brim/raft**; MC-2 sub-floor rungs rendered **without `--check`** (they FAIL by design);
  MC-3 bore mouths on the bed. One material, one profile, one session ("a card printed across two sessions
  is two half-cards"). **Releases:** `FIT_GAP_MM`/`FIT_TOL_MM`/`CLIP_CLEARANCE_MM`, `holeCompMm`, the two
  `*_calibrated` profiles, `DEFAULT_MIN_FEATURE_MM`, `BRIDGE_SPAN_MAX_MM`, the F5 overhang threshold,
  `warpMm` (today literally absent), both F7 bed-contact triggers — and with them the mesh gate's PASS/FAIL
  for *every part in the repo*.
- **Plate 2 — LEGO clutch ladder** (`LG-F1`/`LG-F2`/`LG-R1`, all `--piece` of `Lego-Clutch-Coupon.bkr`).
  First public data of its kind — no source reports caliper measurements on a printed LEGO-compatible stud.
  Bench conditions: mate every rung against a **real LEGO part Omar owns**; print without `--check`; record
  **spool + dryness** (fit reportedly moves with moisture). Decides two shipped surfaces (`studs full/edge`
  enablement; 1×N footprint support).
- **Plate 3 — W-series joint: `W-F1` then `W-C1`** (two plates in sequence; MC-1's bore number does *not*
  transfer to a twisting blade — D-008). Clips in PETG, dummy tiles in the wall's tile material. `W-P1`
  (frame band) rides whichever plate has bed room first, including Plate 1 — no dependency.
- **Plate 4 — P2 Star-Orb at defaults** (`Star-Orb.bkr`, 5,040 tris, 45.7 cm³). Settles **no** bet; it is
  the flagship deliverable — gallery hero + "what does an orb cost" photo. P1 strut trio rides along if bed allows.
- **Plate 5+ —** P3 hemisphere split, P4 Rosette-Orb, LG-D1 durability, LG-B1/S1, P5 weave family
  (expected to disappoint on FDM — pairs with an SLS/MJF service order; **no CAL bet may close from a powder
  process**, K10), MC-8 before P5, P6/P7. Each gated on the plate above.

## Phase D — propagate after each reading (the step that gets skipped)

For every measurement, all five must happen or the bet stays open (`docs/tasks/coaster-pipeline/backlog.md` §5): (1) the constant's value
**and** its `Calibrated<T>` status flip together to `measured` naming machine/material/nozzle/profile/date/coupon;
(2) the entry comes **out** of bikar's `.calibration-baseline.json` (baseline may only shrink);
(3) `bets.md` regenerated via `npm run registry:calibration`, never hand-edited; (4) the design doc's Appendix B
`[CAL-…]` entry closes with the measured value; (5) the catalog Status flips, questions answered **by number**,
iteration row dated, commit hashes cited in both repos. A reading that **refutes** the design is a success and
must not be deleted. `bambu print send --record` writes the `docs/prints/<date>-<slug>/` record that
`make validate-prints` gates.

## Phase E — dogfood the `guide-print` skill to a clean Plate-1 print (the current focus)

**Why this phase exists.** Phase A shipped the *capability*; running it for real on Plate 1 (2026-09-17,
the `guide-print` skill end-to-end) surfaced execution-side gaps the software prep never exercised. The
frame is now **dogfooding**: each gap found by actually using the skill becomes a tracked fix that folds
back into the skill, until a Plate-1 print is **simple, issue-free, minimal-clicks-in-Studio — or auto-sent
when there are no warnings.** Findings so far (all reproduced against the real machine card `.3mf`):

1. **The CLI slice hides a warning the Studio GUI shows.** Slicing MC2Wall04 headless produced no advisory,
   but opening the same plate in Studio surfaced a *floating-regions / enable-support* warning.
   `tools/bambu/src/backends/studio-cli.ts:35` captures BambuStudio's output **only** for the version string
   and discards the per-object warning stream. **A pre-dispatch gate must never let us send something Studio
   would have warned about** — the repo's "gate over skill" idiom.
2. **Dual-nozzle filament-grouping mode is unmodelled.** The X2D gcode reads `nozzle_diameter = 0.4,0.4`
   (dual nozzle, even the "0.4 nozzle" profile — D-053), and Studio surfaces a *Filament Grouping* selector
   (Filament-Saving / Convenience-Sync / Quality / Custom) our slice path ignores. For a single material it
   is a no-op and the Filament-Saving default is correct — but the skill should *reason* it, not ignore it.
3. **Opening the plate in Studio is a raw `open -a`, not a CLI verb.** The runbook shells out; it should be
   a first-party `bambu` verb (read-only, local, before the owner gate).

**The tasks (each its own branch → PR → merge; the print blocks on all of them):**

- **#51 — `bambu` open-in-Studio verb.** Replace the raw `open -a` with a real verb that opens a sliced
  `.3mf` in Bambu Studio. Read-only/local, sits before the owner gate.
- **#52 — the pre-dispatch warnings gate ("the proper hook").** `bambu slice` captures BambuStudio's
  per-object warnings (fix `studio-cli.ts:35` to keep the stream); a **classifier** splits *expected /
  by-design* (the sub-floor rungs MC2Wall04/06/08/10 below `DEFAULT_MIN_FEATURE_MM = 1.2` — their
  floating-regions advisory is the data, not a defect: **do not** add support or re-orient) from
  *unexpected*; a **gate** (in `.claude/gates` + a githook + enforced inside `print send`) refuses dispatch
  on any unexpected warning. Wire into `make validate-prints`. This is what enables auto-send-when-clean.
- **#53 — reason the filament-grouping mode.** `print-model` + `bambu slice` determine the X2D dual-nozzle
  grouping mode (find whether BambuStudio's headless CLI can set it; the skill records single-material →
  Filament-Saving default, and asks when material count > 1).
- **#50 — auto-send when the gate is clean.** Port `print send` to first-party FTPS 990 + MQTT
  `print.project_file` (retiring the un-ported griches `McpBackend` for dispatch, the way #188 did for
  status reads); **auto-send once the #52 gate is clean**, owner-gated confirm remains, `--record` keeps
  writing `docs/prints/<date>-<slug>/`. This is the auto-send ceiling, not a zero-Studio requirement.
- **#54 — fold every finding into `guide-print` SKILL.md.** Warnings triage (expected vs unexpected),
  grouping-mode reasoning, the open verb, and the one-click / auto-send flow — so the skill *is* the clean
  runbook, not a thing the operator patches by memory.
- **#9 — run it.** Dogfood `guide-print` end-to-end → a simple, issue-free Plate-1 print. Owner-gated;
  **STOP at the physical send** — the skill/agent never passes `--yes` on Omar's behalf.

**Task graph (blocking):** `#51 + #52 + #53 → #54 → #9`; `#52 → #50`; `#9` is also blocked by `#50`.
So the print (**#9**) cannot run until the findings are fixed (#51/#52/#53), the skill is updated (#54),
and — for auto-send — dispatch is ported (#50). This encodes the standing instruction: *address these
issues → update the skill → then run it at the end to print.*

**Acceptance criterion.** Plate 1 prints with a **simple, issue-free, minimal-clicks-in-Studio** flow —
**or auto-sends with no warnings** once #52's gate is clean. A print attempt on anything carrying an
*unexpected* Studio warning is refused by the gate before it reaches the printer.

## Written expectations & what you can physically test

**The honest shape of the expectation (read first).** The repo does **not** predict outcome numbers,
on purpose: `calibration-design.md` §2 — *"Every rung range is a **bracket around an unknown, not a
prediction**… the point is that the answer be inside the range, not near the middle."* So the written
expectation is a **judgement scale + acceptance criterion**, not a target value. Two consequences carried
onto the bench sheet: **every rung passing, or every rung failing, is a valid result** ("it told you which
way to move — not a coupon that didn't work"), and **a reading that refutes the design is a success**
(several coupons are "built to fail at both ends": W-F1 Q1, W-P1 Q1, and LG-F1 Q2 / LG-S1 Q2 each treat a
design-refuting reading as the finding). Also: **a reading without a profile header is anecdote, not
calibration** — record machine/material/**colour**/spool/nozzle/layer/profile-name/ambient/date/caliper-zeroed
before measuring, and print the whole card in **one material, one profile, one session**.

**Technique (protocol.md):** cool ≥30 min before the caliper touches it; three readings per feature, report
the **median** (a spread >0.05 mm is itself a result); bores = **two orthogonal diameters** at mid-height
(FDM bores aren't round); walls measured **away from seams**; hand judgements recorded **with who judged**.

### Plate 1 — what a good print looks like, per coupon (this is what you physically test)

| Coupon | Rungs (the ladder) | Test with | PASS / borderline / FAIL — as written | Settles |
|---|---|---|---|---|
| **MC-1 fit** | press −0.10 · line 0 · snug +0.05 · sliding +0.15 · free +0.35 mm | **fingers** (+ caliper the pair) | *press* needs a tool/bench pressure to seat · *snug* seats with firm thumb, won't fall out inverted · *sliding* moves under its own weight with resistance · *free* drops under its own weight. Each named class should behave like its name | `CAL-FIT-01` |
| **MC-1 bores** | ⌀3 / 4 / 5 / 6 / 8 / 10 mm | caliper (2 orthogonal ⌀) | measure bore **and** pin separately; only the *difference* is `holeCompMm` (currently 0.20/0.25). The drift from commanded ⌀ is the number sought | `CAL-HOL-01` |
| **MC-2 walls** | 0.4 / 0.6 / 0.8 / 1.0 / 1.2 / 1.6 / 2.0 mm | caliper + sliced preview | thinnest wall that prints as **one solid continuous perimeter**; a rung fails when it's Arachne'd into a single bead or dropped silently. First 4 rungs are sub-floor by design | `CAL-FEA-01` (moves the 1.2 mm floor) |
| **MC-3 bridge** | spans 4 / 6 / 8 / 10 / 12 / 16 / 20 / 25 mm | **eyes** | **clean / sagging / drooping / failed** — record the first rung that *sags*, not the first that fails; usable limit is the last clean one. (Top rungs are survey-argued, not blind) | `CAL-BRG-01` (≤10 mm rule) |
| **MC-4 fan** | 20 / 30 / 40 / 45 / 50 / 60° from vertical | **eyes + photo**, supports OFF | first angle showing **curl or droop** on the underside; photograph the fan. (Record from-vertical vs from-horizontal — they coincide at 45°) | `CAL-OVH-01` |
| **MC-5 warp** | 120×80×1.6 plate, four corners | **feeler gauge** on glass/granite | gap at **all four** corners (not the worst) — the *pattern* separates warp from bed-levelling. Corner A = by the ⌀3 fiducial, then B/C/D clockwise | `CAL-WRP-01` (`warpMm`, today absent) |
| **MC-6 towers** | ⌀3 / 5 / 8 / 12 × 40 mm, bare plate no brim | **eyes** (+ caliper foot) | which survived, which detached — and **never-stuck (adhesion)** vs **stuck-then-snapped mid-print (stiffness)** are different results; note height if seen. Measure elephant's foot at each base | `CAL-BED-01` |

*What a `--check` PASS does NOT tell you (say so, don't over-claim):* the mesh gate is silent on MC-3's 2 mm
bridged ceiling and MC-4's 2 mm fan wall (both are about mesh soundness only), and `MIN_BED_CONTACT_RATIO`
is untestable on a straight rod (reads 100% every rung) — it rides `CAL-BED-01` by inference.

### Plate 2 — the LEGO tests (highest novelty; each mates against a real LEGO part you own)

- **LG-F1** (rib ladder `ribMm` 0 / 0.05 / 0.10 / 0.15 / 0.20 × `engage` 1.6 / 3.2 / 8.0): which rib clutches
  a **real LEGO stud** firmly without forcing; **does rung 0 (no rib) clutch at all** — if a loose bore holds,
  the whole rib architecture is over-engineering. Pick up by the printed piece; repeated seat/unseat. Settles
  `CAL-RIB-01`, *"the largest unverified bet in the document,"* and gates the whole M6 phase.
- **LG-F2** (stud ⌀ ladder 4.65 / 4.73 / 4.80 / 4.88 / 4.95): **caliper every rung's realised stud ⌀ before
  testing fit** — the grounding audit found **no public source reporting caliper measurements on a printed
  LEGO-compatible stud; this table would be the first.** Mate to a real 2×4 brick from above.
- **LG-D1** (later): 100 seat/unseat cycles against one real plate — **zero public sources report a durability
  cycle count**; it "decides whether these are toys or display pieces."

### Priority order — what to physically test, most leverage first

1. **MC-1 fit ladder — by fingers, zero instruments, highest leverage.** Settles `CAL-FIT-01` on hand-feel
   the moment the plate is off the bed. Do this first.
2. **MC-3 bridge, MC-4 fan, MC-6 towers — by eye / camera, no instruments.** Bridge sag, overhang curl, tower
   survival are all visual reads; capture photos for the record.
3. **MC-1 bores + MC-2 walls — caliper.** Needs the caliper (median of three, orthogonal bores). Settles
   `CAL-HOL-01` and moves the repo-wide `DEFAULT_MIN_FEATURE_MM` floor — the single most consequential number.
4. **MC-5 warp — feeler gauge on a flat reference.** Needs the glass/granite + feelers (the instrument B2 buys).
5. **Plate 2 LG-F1 / LG-F2 — mate to real LEGO + caliper studs.** Highest *novelty* (first-of-kind data), but
   gated behind Plate 1 landing and behind owning real LEGO parts. Not before the card.

## Critical files

- `bikar:packages/knobs/src/machines.ts` — add the `bambu-x2d` `PrintTarget` (Phase A1).
- `docs/decisions-log.md` — dual-nozzle representation decision (Phase A2).
- `docs/tasks/coaster-pipeline/backlog.md` — the campaign master; update Plate statuses as prints land.
- `.claude/skills/prototype/catalog.md` — where each coupon's result is logged (Phase D5).
- `.claude/skills/prototype/SKILL.md` — extend to script the photograph + compare-verdict seams (Phase A8).
- `docs/prints-tab-design.md` (`readings[]`/`objects[]` schema) + `.claude/gates/prints_gate.py` — add `expected`/`verdict` fields + the compare check; ship gate R3 (Phase A8).
- `docs/calibration-design.md` §7 (23-row table) / §6 (render commands) / §4 (slicer settings) / §2 (bracket philosophy) — the card spec.
- `.claude/skills/calibrate/protocol.md` — the profile header, technique rules, judgement scales, blank bench sheet (source for the pre-populated one).
- `docs/prints/plate-1-bench-sheet.md` (new, Phase A7) — the pre-populated Plate 1 bench sheet Omar carries to the printer.
- `.claude/skills/guide-print/SKILL.md` — the operator runbook dogfooded in Phase E; #54 folds in the findings (warnings triage, grouping mode, open verb, one-click / auto-send flow).
- `tools/bambu/src/backends/studio-cli.ts` (line 35) — captures BambuStudio output only for the version string, discarding the per-object warning stream; Phase E #52 fixes this to feed the warnings gate.
- `tools/bambu/src/commands/{slice,print}.ts` + a new `.claude/gates` warnings gate + githook — Phase E #52/#50/#53: surface + classify warnings, refuse dispatch on an unexpected one, auto-send when clean.
- `.mcp.json` (gitignored) — written by `bambu setup mcp` at bring-up; `.mcp.json.example` committed.
- Memory *bambu-x2d-bringup*, *owner-gated-and-on-hold* — update as gates clear.

## Verification

1. **Phase A provable without printing:** `make coupons` regenerates 23 rungs; `make validate-coupons` green;
   the new `bambu-x2d` target loads in bikar (unit/type check); `bambu slice plate` produces a sliced `.3mf`
   for the machine card headless; `make validate` (local.ci) stays green.
2. **Bring-up (#8) provable read-only:** after B1, `bambu setup doctor` all-green and `bambu status show`
   returns live temps/AMS — transport proven **before** any filament.
3. **Each print:** `bambu validate record <dir>` + `make validate-prints` pass before the commit; the five-step
   propagate lands; `bets.md` shows one fewer provisional record. **After A8:** a record that measures a bet
   (`settles: CAL-…`) is *refused* unless it carries an `expected` and a `verdict` — the compare seam is now
   enforced, not narrated; `prototype` walks photograph → measure → compare end-to-end; gate R3 is green.
4. **Honesty checks stay green:** `docs_gate` (any new `**Default:**` carries a citation or CAL id),
   anchored pointers at a git ref, `counts_gate` (the 21→N bet/record counts are tool-printed, not typed).
5. **Phase E provable before the print:** re-slicing the machine card surfaces MC2Wall04's floating-regions
   advisory through `bambu slice` (no longer swallowed at `studio-cli.ts:35`); the classifier marks it
   *expected*; the warnings gate PASSES the plate (no *unexpected* warning) and would FAIL a deliberately-
   mis-oriented fixture; `bambu <open verb>` opens the sliced `.3mf`; `guide-print` walks slice → warnings
   triage → (auto-send-when-clean | one-click Studio) with no manual `open -a`.

## Sequencing & tracking

**Phase A is complete** (software prep, all merged — see `docs/tasks/coaster-pipeline/done.md` and `docs/tasks/print-infrastructure/done.md`, Snapshot 7, and the live board
tasks #18–#49). The campaign is now in **Phase E — dogfooding `guide-print` to a clean Plate-1 print**,
which is the current focus. Order:

Phase A (done) → hand B1–B3 to Omar → #8 bring-up (**done**, read-only transport proven) → **Phase E**:
fix the dogfooding findings (#51 open-in-Studio verb, #52 warnings gate, #53 grouping mode) → update the
skill (#54) → port dispatch for auto-send (#50) → **run the skill to print Plate 1 (#9)**, owner-gated,
stopping at the physical send → propagate (Phase D) → Plates 2–5+.

**The print (#9) is deliberately blocked** on Phase E's fix→skill→run chain: `#51 + #52 + #53 → #54 → #9`,
`#52 → #50`, `#9` also blocked by `#50`. This is the standing instruction encoded as a task graph —
*address these issues, update the skill, then run it at the end to print* — so no one attempts a print
before Studio's warnings are captured, classified and gated. The bench sheet (Phase A7) makes Plate 1
physically readable the moment it comes off the bed; Phase E makes getting it *onto* the bed simple,
issue-free, and gate-protected — minimal clicks in Studio, or auto-sent when there are no warnings.
