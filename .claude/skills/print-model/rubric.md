# print-model decision rubric (read at run time)

The skill's run-time checklist. Each decision is a small procedure: the **questions it answers**, the
**inputs it reads**, a grounded **heuristic**, and the **advisory shape** (always a one-line "what a
master would do + why", never a silent change). This file is a sibling of
[`SKILL.md`](SKILL.md) so it can sharpen without editing the skill body.

**Where the grounded numbers live.** Every load-bearing figure below — and its hedge (secondary /
X2D-unconfirmed / thin-source) — is attributed in the print-model design doc
(docs/print-model-design.md §5, merged in PR #191) and its research file. This checklist carries the
*shape* of each decision; it does not re-assert a bare default. Tasks #33/#34/#42/#43/#44 deepen the
rows below and add the formal cited defaults.

## The decisions at a glance

| Decision | Questions we answer | Inputs read | Heuristic (grounded — see design §5) | Advisory shape |
|---|---|---|---|---|
| **Filament** | Which loaded filament, and is it right for this part? | AMS `ams[].tray[]` + external spool (`vt_tray`/`vir_slot`); model use | match `tray_type` to the part's need; if several plausible, **ask** | AskUserQuestion when ambiguous; else "using PLA in slot 2 because …" |
| **Nozzle** | 0.2 / 0.4 / 0.6 / 0.8 mm? | model min feature; functional vs display; part size | 0.4 as the general balance; deviate only on a stated cause (§5.1) | "0.6 mm — functional, no fine detail, faster; 0.4 to keep studs crisp" |
| **Orientation** | Which face down; minimize supports? | mesh overhangs, contact area, contour | Tweaker-3 objective: minimize support volume (not strength) | "laid flat: least support; layer lines run across the pin — weak there" |
| **Supports** | Any? normal or tree? threshold angle? | overhang angles vs threshold | tree for point contacts; none if overhangs ≤ threshold | "no supports — max overhang 38° is under the limit" |
| **Infill** | Pattern and density? | functional vs display; wall count | **defer to profile default**; advise a change only on cause | "leaving profile 15% — bump to 30% only if this bears load" |
| **Brim / raft** | Brim, raft, or neither? | footprint size, warp-prone corners, material | thin source — attribute to the named community source, never bare | "a small footprint like this warps; a brim would help (community guidance)" |
| **Arrangement** | How many fit; when to rotate to fit? | bed size, part footprint, repeat count | libnest2d NFP; try 0/45/90/135° | "9 fit at 0°; rotating 45° fits 12 — want the denser pack?" |
| **Scale / fill-bed** | Unused bed → more copies / another piece / bigger? | leftover bed area vs footprint | proactive when leftover ≥ one more part | "room for 3 more — add copies, or scale 1.4× to fill the plate?" |

## Per-decision notes (deepened by later tasks)

Each note below is a stub the named task fleshes out; the design doc section is the grounded source.

- **Filament (§5.5) — the selection procedure (task #35).** The X2D frame carries `print.ams.ams[]`
  (each unit a `tray[]`) and the external spool as `print.vir_slot` (an array on this machine; the
  H2-family `vt_tray` object may appear instead on other firmware) — confirmed on hardware 2026-09-17
  (memory *bambu-x2d-bringup*). A loaded tray reports
  `tray_type`/`tray_sub_brands`/`tray_color`/`tray_info_idx`/`remain` (`-1` = no RFID, i.e. *unknown*,
  not empty). Run the step like this:
  1. **Read** the loaded slots — `bambu filament` for the summary, `bambu filament --json` for the raw
     `ams`/`vt_tray`/`vir_slot` frame. The verb already parses both shapes defensively and skips empty
     trays; a slot is *loaded* when its `tray_type` is non-blank.
  2. **Nothing loaded → stop and say so.** If no slot is loaded, tell the operator to load a spool;
     there is no filament decision to make and a filament-less plate settles nothing.
  3. **Match material to the part's need** — PLA for display/decor and most LEGO/orb work; a tougher
     material (PETG/ABS/…) only when the part is functional, load-bearing, or heat-exposed *and* the
     operator has said so. Colour is the operator's taste unless the model fixes it.
  4. **One clear match → state it, do not ask** (global bias-to-action): e.g. "using the PLA in AMS 0
     slot 0 — #F5547C, 100% left — display piece, PLA is right." A single loaded PLA against a decor
     part is not a question.
  5. **Several plausible → AskUserQuestion** (the one pivotal call): one question, one option per
     *loaded* slot (empty slots omitted), label `PLA · AMS 0 slot 0 · #F5547C`, description
     `<sub-brand> · NN% left` (or `remain unknown` when `-1`), the recommended option first with its
     reason. "Plausible" means two-or-more materials that both fit, or a colour trade the model does
     not settle — not merely more than one spool present.
  6. **Footgun — remaining too low.** When the chosen slot's `remain` is a real number and shows a low
     remaining percentage, flag it in the plan ("slot 0 shows 8% left — may not finish this part");
     when `remain` is `-1`, state the level is unknown rather than assume full. Never a silent proceed.
- **Nozzle (§5.1).** 0.4 mm is the general balance; 0.2 for features ≲ 0.4 mm or fine text; 0.6 for
  functional/large parts where detail is non-critical; 0.8 for draft/max-flow. Footgun: a wall thinner
  than the chosen nozzle's single-wall floor cannot print — flag before slicing. Grounded, hedged
  numbers and the dual-nozzle caveat are design §5.1 (task #43).
- **Orientation (§5.2).** Minimize support volume (Tweaker-3 objective); **report** the layer-line
  direction as a strength advisory but do not claim to have optimized for strength — no surveyed tool
  does (task #33).
- **Supports / infill / brim (§5.3).** Tree supports for point contacts; defer infill to the profile;
  attribute brim/raft to the named community source (thin source) — never assert bare (task #34).
- **Arrangement (§5.4).** libnest2d No-Fit-Polygon packing at 0/45/90/135°; the rotate-to-fit advisory
  fires only when a rotated pack fits strictly more copies. Verify slicer flags at run time before
  relying on them. Dual-nozzle bed zoning on the X2D is unverified — do not assume a uniformly usable
  bed (task #42).
- **Proactive advisories (§7).** Fill-bed, scale-up, and the footgun catches — each a one-line offer in
  the plan, never an auto-change (task #44).

## The calibration exception

For any plate carrying a `settles: CAL-…` reading, **skip this whole rubric**: coupon settings are
measurements fixed by the bench sheet, not preferences. Defer wholly to
[`prototype`](../prototype/SKILL.md) / [`calibrate`](../calibrate/SKILL.md).
