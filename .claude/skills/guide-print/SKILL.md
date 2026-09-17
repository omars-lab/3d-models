---
name: guide-print
description: Walk the operator through executing one physical print end-to-end — prep the plate, record the profile header, dispatch (owner-gated), attend the print, then measure and propagate. Use for "walk me through a print", "how do I print this", "what do I do to print", "I'm at the printer, now what", "ready this for the machine", "run the print". Not first-time hardware setup (setup-bambu-x2d) and not the CLI verb reference (bambu) — this is the human session runbook that stitches those together.
---

# Guide a print session, end to end

This is the **operator runbook**: the ordered, mostly-physical procedure for turning a chosen model
into a *measured* print without skipping the steps a tired operator forgets. It owns no mechanics of
its own — it routes through the [`bambu`](../bambu/SKILL.md) CLI (slice/dispatch/record), the
[`prototype`](../prototype/SKILL.md) skill (the photograph→compare→verdict loop), and
[`calibrate`](../calibrate/SKILL.md) (turning a reading into an earned number). First-time hardware
wiring is a different skill — [`setup-bambu-x2d`](../setup-bambu-x2d/SKILL.md).

**Where this sits next to [`print-model`](../print-model/SKILL.md):** they are two halves of one
arc. `print-model` is the *planning* front-half — "how should I print this model": it reasons nozzle,
orientation, supports/infill/brim and plate arrangement and hands back a reviewable plan + sliced
plate + preview, stopping **at** the owner gate. `guide-print` is the *execution* back-half — it
picks up at that gate and walks record-header → dispatch → attend → measure → propagate. So for an
arbitrary model, run `print-model` first to decide *how*, then this skill to *run and read* it.

The worked example throughout is **Plate 1** (the machine card), because it is the print that has to
go first — but the seven steps are the shape of *any* print session.

## Before you touch the slicer — the gates

Two things must be true, or stop and say so:

1. **Transport is proven read-only.** `bambu status show` returns live temps/state. If it doesn't,
   this is a setup problem — go to [`setup-bambu-x2d`](../setup-bambu-x2d/SKILL.md), not here.
2. **A reason to print exists.** A plate is a *prototype* only if it answers a question
   ([`prototype`](../prototype/SKILL.md) restates them first); a coupon is worth filament only if it
   settles a `CAL-*` bet ([`calibrate`](../calibrate/SKILL.md)). If neither, it's decoration — say
   so before spending plastic. **Dispatch stays owner-gated** until a bet justifies it: the operator
   sends, never the skill.

## The seven steps

### 1 — Slice with the settings that are *measurements, not preferences*

`bambu slice plate <model.stl> --settings "<machine>;<process>" --filament "<pla>"` (preset names
resolve to the bundle JSONs). **For an ordinary model the *choice* of settings is
[`print-model`](../print-model/SKILL.md)'s job** — nozzle, orientation, supports/infill/brim,
arrangement — and it hands you the sliced plate; come here to run it. **On a calibration plate the
settings are not a choice — they are fixed measurements** set by the bench sheet, and this is exactly
the exception `print-model` carves out. The known-good Plate-1 trio and the full slicer-settings
rationale live in [`docs/prints/plate-1-bench-sheet.md`](../../../docs/prints/plate-1-bench-sheet.md)
and [`docs/calibration-design.md`](../../../docs/calibration-design.md) §4. **On the machine card
these settings *are* the experiment** — getting one wrong erases a reading:

- **MC-4 fan → supports OFF.** A support column would hide the overhang the coupon exists to measure.
- **MC-6 towers → bare plate, no brim/raft.** Watch the `0.20mm Standard @BBL X2D` **`auto_brim`
  footgun**: this profile can add a brim silently, which turns the adhesion test into a non-test.
- **MC-2 sub-floor rungs → slice without `--check`.** They fail the mesh check by design; the failure
  is the data.
- **The slice captures BambuStudio's own slicing warnings and triages them** (`--debug 2`, #52),
  writing a `<plate>.warnings.json` sidecar the dispatch gate reads. **One warning is expected on
  Plate 1**: *"object MC2Wall04.stl has floating regions — re-orient or enable support"* — and only on
  the **0.4 mm** wall rung (measured 2026-09-17; the 0.6 / 0.8 / 1.0 mm rungs slice clean — do not
  expect it on them). It is by design (below the min-feature floor, `CAL-FEA-01`): **do not add support
  or re-orient — that defeats the measurement.** `bambu slice` prints it as `✓ expected (by design)`.
  An *unexpected* warning is different: it **blocks dispatch** (the gate is fail-closed) and must be
  fixed or, if genuinely by-design, whitelisted in `.claude/gates/expected-slicer-warnings.json` — never
  waved past. See [`docs/issues/slicer-warnings-cli-visibility-pivot.md`](../../../docs/issues/slicer-warnings-cli-visibility-pivot.md).
- **Filament grouping (X2D dual-nozzle) → leave it on Plate 1.** With one material the grouping mode is
  a no-op and Studio's **Filament-Saving** default is already correct — nothing to set, no click to make.
  Only a *multi-filament* plate reasons Filament-Saving vs Quality vs Custom
  ([`print-model` rubric](../print-model/rubric.md) §Filament grouping; `bambu slice --filament-map-mode`, #53).

### 2 — Eyeball the sliced plate before it leaves the screen

Pull the plate preview (`Metadata/plate_*.png` inside the `.3mf`) and *look*: no brim under MC-6, no
supports on MC-4, every coupon on the bed. `calibration-design.md` §8 flags MC-4 specifically —
*"no raster render was eyeballed"* is its known weakness, and MC-4's failure mode is a silently-wrong
dimension. Fix the slice now, not after 3 hours of print time.

To see the plate in the slicer itself, run **`bambu slice open <plate.3mf>`** — a read-only, local
approval step that opens the file in Bambu Studio and dispatches **nothing** (it reports honestly if
Studio isn't installed rather than failing cryptically). This is the first-class verb that replaced
the old raw `open -a "/Applications/BambuStudio.app"` (task #51) — use it, not the raw open.

### 3 — Record the profile header *before anything moves*

**A reading without a profile header is anecdote, not calibration.** Run
`bambu header --plate <plate.3mf>` — it joins the live printer frame with the sliced `.3mf` and fills
most of the header (machine, layer height, profile, slicer version, and the loaded material's
type/colour/brand) automatically. Paste its output onto the bench sheet and **hand-complete only the
blanks it leaves** — ambient room temp, enclosure open/closed, caliper make + that you zeroed it, and
the date. Fields the machine didn't answer render `unconfirmed` rather than fabricated (firmware, for
one — read that from `bambu setup discover`'s SSDP line); it never invents a number.
It also cross-checks the loaded nozzle against the sliced-for nozzle and flags a mismatch loudly:
**do not dispatch through a `⚠ NOZZLE MISMATCH`.**

### 4 — Dispatch (owner-gated — the operator's call, never the skill's)

**Before you dispatch — the pre-send gate.** This is the checklist that answers *"are we ready to
print?"* — the symmetric bookend to the two gates at the top. Every line must be green, or stop and
say which one is red. It is a checklist, not a vibe: each item names *what verifies it*, and none is
skippable.

1. **Warnings sidecar present and clean.** A `<plate>.warnings.json` exists beside the `.3mf` and
   carries only warnings expected **by design** (Plate 1: exactly the one `MC2Wall04` 0.4 mm
   floating-regions line — the 0.6 / 0.8 / 1.0 mm rungs slice clean). *Verify:* `bambu print send
   --dry-run` reports the gate verdict. **No sidecar → the gate is fail-closed and `print send`
   refuses** — re-slice at `--debug 2` (step 1, #55) to produce it. Never wave a missing or dirty
   sidecar past with `--allow-unverified` — that is the one move this gate exists to stop.
2. **First-real-send ground-truth diff done — first dispatch to *this machine* only.** Run `bambu
   print send <plate.3mf> --dry-run` and diff its `print.project_file` payload field-for-field
   against a **BambuStudio GUI MQTT capture** (send one plate from the GUI with a sniffer on
   `device/<serial>/request`). Correct any of the three X2D-UNCONFIRMED fields (`bed_type`,
   `ams_mapping`, `md5`) — or wire the flag — and close the bet with a one-line note. The exact
   Plate-1 payload to diff is checked in at
   [`docs/issues/first-party-dispatch.md`](../../../docs/issues/first-party-dispatch.md). Once closed
   for this machine it stays closed; later sends skip this line.
3. **Nozzle matches.** `bambu header --plate <plate.3mf>` shows **no** `⚠ NOZZLE MISMATCH` (step 3).
   A mismatch means the loaded nozzle isn't the one the plate was sliced for — stop.
4. **Filament loaded and correct.** The material the slice assumed (type + colour) is actually loaded,
   and there is enough of it for the plate's estimated grams (Plate 1 ≈ 111 g PLA). Confirm at the
   AMS/external-spool readout, not from memory.
5. **Owner is at the machine.** Dispatch is owner-gated: watching the first layer is a non-damaging
   risk only a present human catches (step 5), and the physical send — and any `--yes` — is the
   operator's, never the skill's.

Then, and only then:

`bambu print send <plate.3mf> --record`. It is fail-closed: it prints the owner-gate notice and
refuses unless the operator passes `--yes` or confirms at a TTY (`--dry-run` shows exactly what it
would send without connecting). **Never pass `--yes` on the owner's behalf.** `--record` scaffolds a
draft under the gitignored `.bambu/records/` — pre-filled with the same header builder as step 3, so
the record and the bench sheet agree.

> **Dispatch is first-party now (as of 2026-09-17, #50).** Both halves — FTPS upload (:990) + MQTT
> `print.project_file` — ride backends we own, alongside the status read (D-055). `print send` no
> longer routes through the uninstallable griches MCP. Run `bambu print send <plate.3mf> --record`
> and it uploads over FTPS then starts the print over MQTT; `--dry-run` prints the exact FTPS target
> and MQTT payload *without connecting* — always eyeball that first. **One caveat on the very first
> real send:** three payload fields are still a CAL-shaped bet for the dual-nozzle X2D (`bed_type`,
> `ams_mapping`, `md5`) — before trusting the first dispatch, diff the `--dry-run` payload against a
> BambuStudio ground-truth capture ([`docs/issues/first-party-dispatch.md`](../../../docs/issues/first-party-dispatch.md)).
> The **Bambu Studio GUI** remains a fine alternative — with the plate already open from step 2
> (`bambu slice open <plate.3mf>`) it is **one click**: confirm the plate, **Print** → send over LAN
> — but the GUI path does **not** fire `--record`, so scaffold the record by hand if you use it. The
> owner-gate rule is unchanged on either path: the physical send — and any `--yes` — is the
> operator's, never the skill's.

### 5 — Attend the print, and print the whole card in one session

The residual first-print risks are operator-side and **non-damaging** (poor first-layer adhesion, no
filament, a profile mismatch) — the firmware owns collision/thermal/runout. So the two controls that
matter are **watch the first layer** and **confirm-before-send** (step 4). On Plate 1 this is doubly
load-bearing: MC-6 prints on bare plate *by design*, so watching the first layer **is** the adhesion
measurement. Print the card in **one material, one profile, one session** — "a card printed across
two sessions is two half-cards."

### 6 — Measure, highest-leverage first

Cool ≥30 min before a caliper touches it; three readings per feature, report the **median** (a spread
>0.05 mm is itself a result); bores = two orthogonal diameters at mid-height; walls away from seams;
hand judgements recorded **with who judged**. Order (from the plan):

1. **MC-1 fit ladder — fingers, zero instruments, highest leverage.** Settles `CAL-FIT-01` the moment
   the plate is off the bed. Do this first.
2. **MC-3 bridge / MC-4 fan / MC-6 towers — eyes + photos**, supports off. Sag, curl, tower survival.
3. **MC-1 bores + MC-2 walls — caliper.** Moves the repo-wide min-feature floor — the single most
   consequential number.
4. **MC-5 warp — feeler gauge on glass/granite**, all four corners (the *pattern* separates warp from
   bed-levelling, so record all four, not the worst).

**Bag and label each rung as it comes off** — rung identity does not survive onto the plastic, and a
mis-bagged rung is worse than a missing one. The per-coupon PASS / borderline / FAIL scales are
pre-filled in the bench sheet; the photograph checklist and the compare-to-expectation step are
[`prototype`](../prototype/SKILL.md)'s job.

### 7 — Propagate (the step that gets skipped)

A refuting reading is a **success**, not a broken coupon — several coupons are built to fail at both
ends, and *every rung passing or every rung failing is a valid result* (it tells you which way to
move). For every measurement, the five-step propagate in
[`.claude/plans/binary-tickling-kay.md`](../../plans/binary-tickling-kay.md) (Phase D) must all
happen or the bet stays open: flip the constant *and* its `Calibrated<T>` status together (naming
machine/material/nozzle/profile/date/coupon); pull the entry out of bikar's calibration baseline;
regenerate `bets.md` via the registry (never hand-edit); close the design doc's `[CAL-…]` entry with
the measured value; flip the catalog Status and date the iteration row. `validate record <dir>` +
`make validate-prints` gate the record before commit.

## Rules

- **Dispatch is owner-gated.** The skill walks to the send and stops. The physical send — and any
  `--yes` — is the owner's, every time.
- **The pre-send gate is a checklist, not a vibe.** Before any dispatch, walk step 4's five lines —
  sidecar clean · ground-truth diff done (first send) · nozzle matches · filament right · owner
  present — and stop at the first red one. "Are we ready to print?" is answered by that list, never
  by feel.
- **The header is the deliverable.** Record it before measuring; numbers without it are anecdote.
- **Slicer settings on a calibration plate are measurements.** Supports/brim/`--check` choices are
  part of the experiment, not taste — verify them in the preview (step 2) before dispatch.
- **One material, one profile, one session** for a card that must be read as a set.
- **Attend the first layer.** It is the one non-damaging risk that a human catches and the firmware
  doesn't.
- **A refuting reading is a result.** Never delete a reading that contradicts the design.
- Full campaign sequencing and the per-coupon expectation tables:
  [`.claude/plans/binary-tickling-kay.md`](../../plans/binary-tickling-kay.md).
