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
- **Arrangement (§5.4) — packing repeats and rotate-to-fit (task #42).** How many copies fit on one
  plate, and when rotating a part lets more fit. Grounded in design §5.4 / research Topic 4. Run it
  like this:
  1. **Take the count and the footprint as given.** The repeat count (how many of each distinct
     piece) comes from the model read (SKILL §How-one-run-flows step 1). The footprint is the part's
     2-D outline **in the base-down orientation already chosen by §5.2** — arrangement *follows*
     orientation, it never re-picks which face is down.
  2. **Know what rotate-to-fit is — and is not.** "Rotate to fit" is a **Z-rotation**: the part spins
     about the vertical axis *on the bed*, changing only its packing footprint. It does **not** change
     which face is down, so it cannot undo §5.2's support/strength decision or §5.3's supports. Keep
     the two separate in the plan: orientation is a face, arrangement is an in-plane angle.
  3. **Pack with the real nester at the four angles.** libnest2d No-Fit-Polygon packing — the same
     lib BambuStudio/Orca/PrusaSlicer share — trying at most **0 / 45 / 90 / 135°** (research Topic 4).
     Honour the profile's **`spacing`** (minimum gap); in a **by-object** print sequence the arrange
     polygon is expanded by `max(spacing, extruder_radius)` so the toolhead clears already-printed
     parts, so by-object packs looser than all-at-once — say which sequence the count assumes. Never
     pack to the bare bed edge.
  4. **Pick the scriptable path honestly.** The intended auto-arrange is the OrcaSlicer headless CLI
     (`--arrange --orient --rotate --scale --slice --export-3mf`), but the research flags the per-flag
     prose as needing a `--help` re-check — so **verify the exact flags at run time** before relying on
     them. Fall back to the slicer GUI (`A` arranges all and adds plates as needed; `Shift-A` the
     selected plate only) or a hand grid estimate (`floor(bedX/(footprintX+spacing)) ×
     floor(bedY/(footprintY+spacing))`). Never report that a tool packed the plate when none ran.
  5. **Rotate-to-fit advisory — fires only on a strict win.** Offer the rotation **only** when a
     rotated pack fits *strictly more* copies than 0°; a tie is not a reason to rotate. State both
     counts and the trade so the operator chooses: "9 fit as-is; rotating 45° fits 12 — denser pack,
     slightly more toolhead travel. Want the denser one?" Never silently rotate.
  6. **K2 — dual-nozzle bed zoning is unverified.** A forum report notes auto-arrange not using the
     H2D's L/R-nozzle-only bed areas (research Topic 4, `[X2D-UNCONFIRMED]`). Until confirmed on this
     X2D, do **not** assume the whole bed is uniformly usable: treat the full bed footprint as an
     **upper bound** on capacity and flag the uncertainty in the plan rather than promising a count
     the zoning might forbid.
  7. **Calibration exception.** A coupon plate's layout is *authored*, not packed — the machine card
     is one fixed plate (calibration-design §7), so arrangement does **not** repack a plate that
     carries a `settles: CAL-…` reading. See §The calibration exception; steps 3–6 short-circuit.
- **Proactive advisories (§7).** Fill-bed, scale-up, and the footgun catches — each a one-line offer in
  the plan, never an auto-change (task #44).

## Compose → slice → hand off — the plan artifact (task #36)

The last three steps of a run (SKILL §How-one-run-flows 6–8): turn the decisions above into one
reviewable **plan artifact**, slice it, and stop at the owner gate. The plan is **composed, not stored
twice** (design §2) — it is *presented* to the operator, not written into `docs/prints/` as a second
copy of the record. The record schema ([`prints-tab-design.md`](../../../docs/prints-tab-design.md)
§4.1) owns a print's stored identity; a print that is only *planned* has no record yet. On the record
axis (design §3.1) the plate sits at `planned` after step 6 and `sliced` after step 7 — parked at the
owner gate, never past it.

1. **Compose the plan** — one artifact, every decision with its one-line "what a master would do + why",
   in the order the operator would act on them. The shape (keep it this stable so two runs read alike):
   - **Model** — what it is, bounds, min feature, and the repeat count (how many of each distinct piece).
   - **Filament** — the chosen slot and why (or the AskUserQuestion outcome), carrying the low-remaining
     footgun if it fired (§Filament).
   - **Nozzle → orientation → supports/infill/brim → arrangement** — one line each, the advisory shape
     from the rows above; orientation carries the layer-line/weak-axis note (K1), never a strength claim.
   - **Advisories** — fill-bed / scale-up offers and any footgun catches, each a line the operator
     decides on (§7, task #44).
   - **Slice result** (filled by step 2) — the exact profile name, the `.3mf` path, the preview.
   This artifact is the deliverable even if slicing cannot run (design §9): a plan + reasoning handed to
   the operator has value on its own.
2. **Slice** — `bambu slice plate <model>` → a sliced `.3mf`. A `.bkr` is **not** a slicer input: render
   it to STL first (the 3d-models build, e.g. `make orbs`) and slice the STL — the verb rejects a `.bkr`
   rather than silently doing nothing. Name the **profile explicitly** in the plan (e.g. the X2D 0.4 mm
   preset); it is part of the print's identity, not a preference, and the same spelling the record's
   `profile.slicer_profile` will later carry. If no headless BambuStudio binary is found the verb exits
   non-zero and cannot produce a `.3mf` — say so and hand off the plan alone; do not fake a slice.
3. **Pull the preview** — the plate preview is the Metadata/plate_1.png member inside the sliced
   `.3mf` (a zip). Extract it with `unzip -p` (the sliced file, that archive member, redirected to a
   `.png`); it is the same asset the record's `photos[]` and the prints page use — extract it, do not
   re-render one.
4. **Footgun re-check on the sliced result** (§7) — thin wall vs the nozzle's single-wall floor, needless
   supports, fragile layer direction, wrong filament. An issue found is a one-line advisory; on the
   operator's say-so, revise the plan and re-slice (back to step 1). Never auto-change a setting.
5. **Hand off at the owner gate** — present the plan + the `.3mf` path + the preview PNG, then **STOP**.
   The skill never uploads, never starts a print, never passes `--yes`. Dispatch is Omar's
   `bambu print send` (design §9). Say plainly that the plate is parked at the gate awaiting his call.

## Recovery loop — when a print fails or disappoints (task #37)

A second entry point, not part of the forward run: the operator says "why did this warp / string /
fail?" (SKILL description). The loop is **diagnose → revise → re-slice → back to the owner gate**
(design §6.2), and it **reads against a named catalog — it does not invent a defect taxonomy.** The
catalog is Simplify3D's Print Quality Guide plus Bambu's own print-quality wiki (design §6.1, research
Topic 6); attribute a cause to it, carry its hedge (K1), and never assert a bare fix number the source
does not give.

The defects the skill models are **enumerated, not "all defects" (K2)** — seven, from design §6.1. For
each, map the symptom to the catalog's documented cause, then emit the revision as a **one-line advisory
pointing at the forward decision that owns the fix** (never a silent change):

| Symptom (operator / photo) | Catalog defect | Documented cause (attribute, don't assert) | Advisory revision → owning decision |
|---|---|---|---|
| corners lift off the bed | warping / poor bed adhesion | material shrinks as it cools; small or sharp-cornered footprint | a brim helps (community guidance, §Brim/raft); check first-layer adhesion — never bare numbers |
| fine hairs / blobs between parts | stringing / oozing | filament oozes on travel moves; retraction/temp off | more retraction or a lower nozzle temp, *attributed to the catalog* |
| layers offset partway up | layer shift | mechanical skip or too-fast motion | lower speed/accel; the mechanical half is the operator's, not a slice change |
| gaps / thin or blobby walls | under- / over-extrusion | flow miscalibrated | this is a **calibration** matter — defer to [`calibrate`](../calibrate/SKILL.md)/the bench sheet, not a taste advisory |
| first layer bulges out at the base | elephant's foot | first-layer squish + bed heat | first-layer compensation / lower bed temp, attributed |
| rough scars where supports touched | support scarring | supports too dense, or touching a show face | tree supports + more interface gap, or **reorient to remove them** (§Orientation) |
| underside of an overhang curls/droops | overhang droop | overhang past the printable angle; cooling | better cooling or supports, or reorient (§Orientation). The X2D's own angle `CAL-OVH-01` is unmeasured — advisory, not a gate |

**The loop, step by step (design §6.2):**
1. **Symptom in** — from the operator directly, or read from the record's `feedback` block
   (`prints-tab-design.md` §4.1, shipped task #38): `feedback.symptom` is the finding, `feedback.cause`
   the diagnosis, `feedback.next` the remedy tried. A photo attaches to the record's `photos[]`.
2. **Map to the catalog** — pick the defect + its documented cause from the table; if the symptom does
   not match a modeled defect, say so (K2) rather than force-fit one.
3. **Propose the revision** — one-line advisory pointing at the owning forward decision above.
4. **On the operator's say-so**, revise the plan → re-slice (the §Compose → slice → hand off procedure)
   → back to the owner gate. The record moves `failed → planned` on the record axis (design §3.1).
5. **If the finding is physical and new** — not already in the catalog, observed on *our* machine — it
   graduates into [`best-practices.md`](best-practices.md) as a fails-before / passes-after example (the
   self-healing seam, design §8, task #46). A catalog defect we merely re-hit does not graduate; a new
   datum does.

The freshness gate (design §6.3, task #39) is what keeps the `feedback`/`status` consistency honest —
a `failed` record must carry a feedback block; this loop is only the reasoning that fills it.

## The calibration exception

For any plate carrying a `settles: CAL-…` reading, **skip this whole rubric**: coupon settings are
measurements fixed by the bench sheet, not preferences. Defer wholly to
[`prototype`](../prototype/SKILL.md) / [`calibrate`](../calibrate/SKILL.md).
