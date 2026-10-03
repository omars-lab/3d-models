---
name: guide-print
description: Walk the operator through executing one physical print end-to-end — prep the plate, record the profile header, dispatch (on Omar's approval on the plate page), attend the print, then measure and propagate. Use for "walk me through a print", "how do I print this", "what do I do to print", "I'm at the printer, now what", "ready this for the machine", "run the print". Not first-time hardware setup (setup-bambu-x2d) and not the CLI verb reference (bambu) — this is the human session runbook that stitches those together.
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
   so before spending plastic. **A send needs Omar's approval on the plate's page** (D-093): his
   tick, or his yes in chat written onto the page. One approval covers one send.
3. **No measurement is worth the machine.** A coupon that could **physically damage** the printer is
   never sliced-for-dispatch or sent, no matter what bet it would settle — the value of any reading is
   capped by the cost of the hardware. Draw the line where FDM does: **cosmetic / geometry failures are
   not damage and stay fair game** — floating regions, a dropped thin wall, a sagging bridge, an
   overhang that curls are *the data* a by-design coupon exists to produce, and several coupons are
   built to fail (K10). What crosses the line is a **hardware-risk** failure: a part that detaches and
   is dragged into a blob the nozzle plows through, a toolpath into the bed/gantry, anything that could
   crash the nozzle or scar the plate. Such a coupon is only acceptable with **active mitigation** —
   on-device failure/spaghetti detection **and** small part mass — and absent that mitigation, **drop
   or redesign the coupon; never risk the printer to close a bet.** The X2D runs its own failure
   detection, so that half is taken as given: never ask Omar to turn it on or watch for it, and never
   hold a plate on that yes ([D-092](../../../docs/working-model/decisions-log.md#d-092--failure-detection-is-the-printers-job-not-a-per-plate-yes)).
   Small part mass is still ours to check.
   (The firmware owns collision/thermal/runout; this tenet owns the geometry we *choose* to send.)

## The seven steps

### 1 — Slice with the settings that are *measurements, not preferences*

`bambu slice plate <model.stl> --settings "<machine>;<process>" --filament "<pla>"` (preset names
resolve to the bundle JSONs). **For an ordinary model the *choice* of settings is
[`print-model`](../print-model/SKILL.md)'s job** — nozzle, orientation, supports/infill/brim,
arrangement — and it hands you the sliced plate; come here to run it. **On a calibration plate the
settings are not a choice — they are fixed measurements** set by the bench sheet, and this is exactly
the exception `print-model` carves out. The known-good Plate-1 trio and the full slicer-settings
rationale live in [`docs/prints/plate-1-bench-sheet.md`](../../../docs/prints/plate-1-bench-sheet.md)
and [`docs/design/printing/calibration-design.md`](../../../docs/design/printing/calibration-design.md) §4. **On the machine card
these settings *are* the experiment** — getting one wrong erases a reading:

- **MC-4 fan → supports OFF.** A support column would hide the overhang the coupon exists to measure.
- **MC-6 towers → bare plate, no brim/raft.** Watch the `0.20mm Standard @BBL X2D` **`auto_brim`
  footgun**: this profile can add a brim silently, which turns the adhesion test into a non-test.
- **MC-2 sub-floor rungs → slice without `--check`.** They fail the mesh check by design; the failure
  is the data.
- **The slice captures BambuStudio's own slicing warnings and triages them** (`--debug 2`, #52),
  writing a `<plate>.warnings.json` sidecar the dispatch gate reads. The sidecar records a
  `source_sha256` of the exact `.3mf` bytes it was sliced from, so the gate can refuse a **stale**
  sidecar (one left beside a `.3mf` regenerated by a different pipeline), not only a missing one —
  re-slicing is the only way to refresh it (#62). **One warning is expected on
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
type/color/brand) automatically. Paste its output onto the bench sheet and **hand-complete only the
blanks it leaves** — ambient room temp, enclosure open/closed, caliper make + that you zeroed it, and
the date. Fields the machine didn't answer render `unconfirmed` rather than fabricated (firmware, for
one — read that from `bambu setup discover`'s SSDP line); it never invents a number.
It also cross-checks the loaded nozzle against the sliced-for nozzle and flags a mismatch loudly:
**do not dispatch through a `⚠ NOZZLE MISMATCH`.**

### 4 — Dispatch (Omar's approval on the plate page, one per send)

**Before you dispatch — the pre-send gate.** This is the checklist that answers *"are we ready to
print?"* — the symmetric bookend to the two gates at the top. Every line must be green, or stop and
say which one is red. It is a checklist, not a vibe: each item names *what verifies it*, and none is
skippable.

1. **Warnings sidecar present, fresh, and clean.** A `<plate>.warnings.json` exists beside the `.3mf`,
   its `source_sha256` matches the plate's current bytes (**fresh**, not left over from an earlier
   slice), and it carries only warnings expected **by design** (Plate 1: exactly the one `MC2Wall04`
   0.4 mm floating-regions line — the 0.6 / 0.8 / 1.0 mm rungs slice clean). *Verify:* `bambu print
   send --dry-run` reports the gate verdict; `bambu validate plate` prints the freshness in its
   `warnings` line. **Missing, stale, or unverifiable (legacy, no hash) → the gate is fail-closed and
   `print send` refuses** — re-slice at `--debug 2` (step 1, #55/#62) to produce or refresh it. Never
   wave a missing, stale, or dirty sidecar past with `--allow-unverified` — that is the one move this
   gate exists to stop.
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
4. **Filament loaded and correct.** The material the slice assumed (type + color) is actually loaded.
   Confirm the *type and color* at the AMS/external-spool readout, not from memory. On **quantity**,
   don't over-think a tight spool: the X2D has a runout sensor and **pauses mid-print, prompting you to
   load more, then resumes on the same layer** — so a spool that's tight against the sliced estimate is
   fine to *start* (the slice reports the grams; Plate 1 ≈ 70 g by filament length, the dispatch-relevant
   figure, not the 111 g solid-volume equivalent). The runout backstop means only a *clearly* insufficient
   spool is worth stopping for; stay reachable to feed it when it nudges.
5. **The bed is empty and the plate is in.** *Verify:* `bambu print send <plate.3mf> --dry-run`
   saves one camera frame under `.bambu/bed/` and prints its path (`bambu status camera -o
   <file.jpg>` takes one on its own). Open the JPEG and look: no pieces left from the last print,
   the build plate seated. Say what you saw. A frame that failed to save is a warning, not a pass —
   then the operator looks at the bed in person. Spotting objects once the print starts is the
   X2D's own job (D-092); this photo is for the person sending.
6. **Omar approved this send, and the printer is idle.** *Verify:* the `✓ approval:` and
   `✓ printer:` lines of `print send --dry-run`. The approval lives on the plate's page in
   `docs/design/plates/` (D-093): his tick, or his yes in chat written onto the page with the date and his
   words. One approval covers one send: once the plate has been sent or printed, a reprint needs a
   new one, so a plate whose print showed the setup was wrong never goes out again on the old yes.
   A production plate is the exception: it has a standing approval while its prints still show production and its recipe is the one it was promoted on (D-095).
   Watching the first layer is not on this list: the X2D does its own first-layer and failure
   detection (D-092).

Then, and only then:

`bambu print send <plate.3mf> --record`. It is fail-closed: with no live approval on the page, or a
printer that is busy or will not say, it refuses, and no flag skips either check. Then it asks at a
TTY; `--yes` skips only that question, and only on a live page approval. The
[`send-plate`](../send-plate/SKILL.md) skill runs this whole step in order. A send that goes through
spends the approval: the box is unticked, the stage becomes `sent`, and a dated `sent` row joins the
page's timeline, which is the log of every approved reprint. `--record` scaffolds a
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
> — but the GUI path does **not** fire `--record`, so scaffold the record by hand if you use it. On
> either path the send needs Omar's live approval on the page (D-093); the GUI path does not spend
> it, so untick the box and add the dated `sent` row by hand.

### 5 — Attend the print, and print the whole card in one session

The residual first-print risks are operator-side and **non-damaging** (poor first-layer adhesion, no
filament, a profile mismatch) — the firmware owns collision/thermal/runout, and on the X2D the
first layer and print failures too (D-092). So the control that matters is **confirm-before-send**
(step 4). One exception is a reading, not a watch: MC-6 on Plate 1 prints on bare plate *by
design*, so how its first layer sticks **is** the adhesion measurement. Print the card in **one material, one profile, one session** — "a card printed across
two sessions is two half-cards."

**Runout is a pause, not a failure.** If the spool runs out, the X2D's runout sensor pauses the job,
retracts, and prompts you to load more; it resumes on the same layer once you feed it. This is why a
tight-but-close spool (step 4) does not block a start — the "one session" rule is about *material and
profile continuity*, not an uninterrupted clock, and a runout pause + reload keeps the card one card.
Stay reachable for the nudge rather than pre-aborting over grams.

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
[`prototype`](../prototype/SKILL.md)'s job. Carry the **photo map** to the bench so you shoot the
right coupons: `make plate-photo-map` renders it from the sliced `.3mf` (a top-down map with the
shoot-these coupons ringed, plus a printable contact sheet) — it is embedded in the bench sheet.

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

- **No measurement is worth the machine.** A coupon that could physically damage the printer is never
  sent (gate 3). Cosmetic/geometry failures are the data and stay fair game; a hardware-risk failure
  (a detached part dragged into a blob, a crash into bed/gantry) needs active mitigation or the coupon
  is dropped/redesigned. Never risk the printer to close a bet. The X2D's own failure detection is
  that mitigation for small loose parts; it is never asked of Omar per plate (D-092).
- **A send needs Omar's live approval.** His tick on the plate's page, or his yes in chat written
  onto it (D-093). One approval, one send; `print send` refuses without it, and no flag skips it.
- **The pre-send gate is a checklist, not a vibe.** Before any dispatch, walk step 4's six lines —
  sidecar clean · ground-truth diff done (first send) · nozzle matches · filament right · bed empty
  · approval live and printer idle — and stop at the first red one. "Are we ready to print?" is answered by that list, never
  by feel.
- **The header is the deliverable.** Record it before measuring; numbers without it are anecdote.
- **Slicer settings on a calibration plate are measurements.** Supports/brim/`--check` choices are
  part of the experiment, not taste — verify them in the preview (step 2) before dispatch.
- **One material, one profile, one session** for a card that must be read as a set.
- **The first layer is the printer's to watch.** The X2D detects first-layer and print failures
  itself; never ask the owner to watch it, and never hold a print for it (D-092).
- **A refuting reading is a result.** Never delete a reading that contradicts the design.
- Full campaign sequencing and the per-coupon expectation tables:
  [`.claude/plans/binary-tickling-kay.md`](../../plans/binary-tickling-kay.md).
