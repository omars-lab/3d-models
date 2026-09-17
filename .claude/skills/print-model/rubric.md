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
- **Orientation (§5.2) — the reasoning procedure (task #33).** Which face goes down, chosen to
  minimize support while staying printable. The objective is Tweaker-3's — least support *volume*
  subject to printability (design §5.2, research Topic 3) — **not** part strength. Run it like this:
  1. **Enumerate candidate bases** — the natural "down" for the part's function plus each large flat
     face that could sit on the bed. A part with an obvious flat bottom usually has one strong
     candidate; a rounded/organic part has several.
  2. **Score each candidate by support burden** — which surfaces become overhangs past the support
     threshold (the slicer profile's default angle; the X2D's own overhang limit `CAL-OVH-01` is not
     yet measured, so treat the profile value as advisory, not a gate) and how much bed contact the
     base gives. Prefer the orientation with the least support that still has adequate bed contact —
     a tiny-contact tip-down that "needs no support" but will not adhere is not printable.
  3. **Pick the scriptable path honestly.** Tweaker-3's headless CLI is the intended auto-orient
     (design §5.2), but do not assume it is installed — **verify it is on PATH at run time**; if it
     is not, fall back to the slicer's built-in auto-orient (BambuStudio/OrcaSlicer) or reason from
     the candidate faces by hand. Never report that a tool oriented the part when none ran.
  4. **K1 — report strength, do not claim to optimize it.** No surveyed tool optimizes layer-line
     strength / anisotropy (design §5.2). So **report** the layer-line direction as an advisory
     ("layer lines run across the pin — that is the weak axis") but never claim the orientation was
     chosen for strength. When function makes a weak axis unacceptable, surface the trade so the
     operator decides between less support and a stronger part.
  5. **Advisory shape:** "laid flat on the base face: least support; note the layer lines run across
     the pin — weaker there" — one line, what a master would do and why, never a silent re-orient.
- **Supports / infill / brim (§5.3) — the settings procedure (task #34).** Three sub-decisions, each
  an advisory line, never a silent change. Grounded in design §5.3 / research Topic 5.
  - **Supports.** Needed only where an overhang exceeds the support threshold (the slicer profile's
    default angle; the X2D's own limit `CAL-OVH-01` is unmeasured, so the profile value is advisory).
    Read the orientation (§5.2) chosen first — a good base often removes the need entirely. When
    support *is* needed, prefer **tree** for point contacts (branches from a small base, less
    material/time than a grid; interface layers cap it under the model). The advisory **names the max
    overhang** so the operator can see the why: "no supports — max overhang 38° is under the limit",
    or "tree supports under the two arms only".
  - **Infill.** **Defer to the slicer profile's default density and pattern**; advise a change only on
    a stated cause — load-bearing part → denser; display-only → lighter. Do **not** assert a bare
    default number (the profile owns it). The eight fill patterns are named from the source, not
    invented: Concentric, Rectilinear, Monotonic, Monotonic Line, Aligned Rectilinear, Hilbert Curve,
    Archimedean Chords, Octagram Spiral (research Topic 5). Advisory: "leaving the profile's 15% —
    bump to 30% only if this bears load".
  - **Brim / raft — THIN SOURCE, attribute never assert.** No authoritative Bambu page settles
    brim-vs-raft; the research found community guidance only (design §5.3, research Topic 5). So
    **attribute** any brim/raft advice to that community source and never state it bare: brim =
    adhesion for a small footprint or warp-prone corners; raft = a full base only for a very warpy
    material or an uneven bed (rarely). Advisory: "a small footprint like this can lift at the
    corners; a brim would help (community guidance — no vendor spec)". If a real plate ever settles
    this on *our* machine, it graduates into [`best-practices.md`](best-practices.md) with our own
    datum (§8 self-healing).
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
