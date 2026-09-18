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
| **Filament grouping** (X2D dual-nozzle) | Which grouping mode — and does it even matter here? | filament *count* on the plate | 1 filament → no-op, Filament-Saving default is right; ≥2 → reason Saving vs Quality vs Custom | "single filament → grouping is a no-op, default Filament-Saving" / "2 colours: Quality — fewer cross-nozzle swaps" |
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
- **Filament grouping (X2D dual-nozzle) — the mode decision (task #53).** The X2D's two nozzles let
  Studio *group* filaments across them; the GUI's "Filament Grouping" selector is the process-config
  enum `filament_map_mode` (verified settable headlessly — [`x2d-filament-grouping-mode`](../../../docs/issues/x2d-filament-grouping-mode.md)).
  Decide it **by filament count**, and lead with the honest no-op:
  1. **One filament on the plate → it is a no-op. Say so and move on.** With a single filament the slice
     collapses to one group (`filament_maps=1`) whatever the mode, and Studio's default is already
     Filament-Saving. State it — "single filament → grouping has no effect; default Filament-Saving is
     correct" — rather than offering a knob that does nothing. **Every current-campaign plate is
     single-material, so this is the usual branch.**
  2. **Two or more filaments/colours → reason the mode, then recommend.** `saving` (Filament-Saving,
     `Auto For Flush` — minimise waste/flush; the default) vs `quality` (`Auto For Match` — fewer
     cross-nozzle changes, better surface, more flush) vs `manual`/Custom (a hand-assigned per-filament
     nozzle map). Default to `saving` and name the trade; recommend `quality` when the part's surface
     matters more than filament economy. Never silently pick.
  3. **It rides `bambu slice`, not a knob.** When a mode other than the default is wanted, pass
     `bambu slice plate … --filament-map-mode <saving|quality|manual>` — it merges the enum into the
     process preset (single filament → it prints the no-op note and changes nothing). `manual` needs an
     explicit `filament_map` array the CLI does not synthesise; the plan says so rather than faking one.
  4. **Calibration exception.** A coupon plate's profile is fixed by the bench sheet — do not add or
     change a grouping mode on a plate carrying a `settles: CAL-…` reading.
- **Nozzle (§5.1) — the recommendation procedure (task #43).** Which of 0.2 / 0.4 / 0.6 / 0.8 mm, on
  a stated cause, never a silent pick. The grounded, hedged numbers and their citations live in design
  §5.1 — this is how the skill *uses* them; it does not restate the `**Default:**` markers (§5.1 owns
  them). Run it like this:
  1. **Read the model's minimum feature first** — the driving input. Note the thinnest wall, the
     finest text/detail, and the overall size, from the model read (SKILL §How-one-run-flows step 1).
  2. **Default to 0.4 mm and state it** — the general-purpose balance (design §5.1, cited there;
     advisory, as the source page was bot-blocked at fetch). Global bias-to-action: a normal part on
     the standard nozzle is *stated*, not asked. Deviate only on a cause the model gives:
     - **0.2 mm** when the minimum feature is ≲ 0.4 mm or fine surface text matters — worth the time
       penalty. This is the crisp-detail case (LEGO studs, fine engraving).
     - **0.6 mm** when the part is functional/large and detail is non-critical. The "~30–40% faster
       than 0.4" figure is **attributed and non-official** (§5.1, wants a `CAL-*` bet) — offer it as a
       reported speed win, never as our measured number.
     - **0.8 mm** for draft prototyping and max-flow infill only.
  3. **Sanity-check the layer height and the single-wall floor** — layer ≈ 25–75% of nozzle diameter,
     minimum single-wall ≈ one nozzle diameter (design §5.1, advisory endpoints pending a page
     re-check, not a hard gate). These bound what the chosen nozzle can actually resolve.
  4. **Footgun — thin wall below the floor.** If the model's thinnest wall is under the chosen nozzle's
     single-wall floor (a 0.5 mm wall on a 0.8 nozzle cannot print), flag it **before slicing** — the
     slicer would silently drop or Arachne-thin it. The fix is usually a *smaller* nozzle, which loops
     back to step 1's min-feature read; surface the trade (finer wall vs. slower print), never auto-switch.
  5. **K2 — one diameter per plate, for now.** That all four diameters ship *per-nozzle* on the X2D
     specifically is `[X2D-UNCONFIRMED — H2-proxy]`, and mixing two diameters at once is an **open
     capability, not an assumed one** (design §5.1). So recommend a *single* nozzle for the whole plate
     until mixed-nozzle is confirmed on this machine; do not plan a two-diameter plate on spec.
  6. **Advisory shape:** "0.4 mm — general-purpose, no feature under 0.4; 0.6 would cut time ~30–40%
     (reported, not measured) if you can lose the fine detail" — one line, what a master would do and
     why, the operator decides.
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
     **For N copies of ONE model** (a fun-print "print 20 of this", when the count is not already in the
     model), there is no `--copies` flag: pack 1 positional + (N−1) of the same file after `--` with
     `--arrange`. The runnable form is [`scripts/slice-copies.sh`](scripts/slice-copies.sh) `<model> <N>` —
     see [`best-practices.md`](best-practices.md) "Our examples" for the gotchas (by-design floating-regions
     block the gated send → GUI; authored `.3mf` warns less than raw STL; the `-o` basename footgun).
  5. **Rotate-to-fit advisory — fires only on a strict win.** Offer the rotation **only** when a
     rotated pack fits *strictly more* copies than 0°; a tie is not a reason to rotate. State both
     counts and the trade so the operator chooses: "9 fit as-is; rotating 45° fits 12 — denser pack,
     slightly more toolhead travel. Want the denser one?" Never silently rotate.
  6. **K2 — dual-nozzle bed zoning is unverified** (distinct from filament *grouping*, which now **is**
     verified — see §Filament grouping). A forum report notes auto-arrange not using the H2D's
     L/R-nozzle-only bed areas (research Topic 4, `[X2D-UNCONFIRMED]`). Until confirmed on this X2D, do
     **not** assume the whole bed is uniformly usable: treat the full bed footprint as an **upper bound**
     on capacity and flag the uncertainty in the plan rather than promising a count the zoning might
     forbid.
  7. **Calibration exception.** A coupon plate's layout is *authored*, not packed — the machine card
     is one fixed plate (calibration-design §7), so arrangement does **not** repack a plate that
     carries a `settles: CAL-…` reading. See §The calibration exception; steps 3–6 short-circuit.
- **Proactive advisories (§7) — the "sage" sweep (task #44).** The pass that makes the skill a master
  rather than a slicer front-end: after the decisions above are made (nozzle → orientation →
  supports/infill/brim → arrangement) and *before* composing the plan, sweep for "is the operator
  getting in their own way?". Every item is **one line in the plan, an offer, never an auto-change** —
  a master would not do X because Y, and the operator decides. Grounded in design §7. Run it like this:
  1. **Fill unused bed.** Take the packed footprint from §5.4 and the bed size; if the leftover area is
     **≥ one more part footprint**, offer to use it: "room for N more copies, or another queued piece —
     want to fill the plate?" Reuse §5.4's pack (do not re-nest by hand). Only fire on a real ≥1-part
     gap — a nearly-full plate gets no nag.
  2. **Scale up — only a part with no fixed dimension.** A small part alone on a large bed → "this is
     4 cm on a 25 cm bed; scale 2× if you meant it bigger?" **Guard:** never offer scale-up on a
     **dimensioned or functional** part — a LEGO stud (4.8 mm matters), an orb at spec, a coupon, any
     part that mates with something — scaling those *breaks* them. Scale-up is for decorative,
     free-size pieces, and even then it is a question, never an assumption that bigger was meant.
  3. **Collect the footgun catches — do not re-derive them.** The four footguns are each *owned* by the
     decision that found them; this sweep gathers them into the plan, it does not recompute them:
     - **thin wall < single-wall floor** — §Nozzle step 4 (§5.1).
     - **supports where reorienting removes them** — §Orientation (§5.2): if a cheaper base exists, say so.
     - **fragile layer-line on a load axis** — §Orientation step 4 (§5.2), *reported* not claimed-optimized.
     - **loaded filament wrong for the stated use** — §Filament (§5.5): PLA on a functional/heat part.
  4. **Say nothing when there is nothing to say.** If the plate is full, the part is correctly sized,
     and no footgun fired, the sweep adds no lines — a master does not invent advice to look busy.
  5. **Calibration exception.** A coupon plate (`settles: CAL-…`) skips this whole sweep — its layout,
     size, and profile are fixed by the bench sheet (see §The calibration exception).

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
   - **Offer to open the sliced plate in Bambu Studio for visual approval** — `open -b
     com.bambulab.bambu-studio <plate>.3mf` (the bundle id, not `-a "Bambu Studio"`, which fails — the
     `.app` bundle name is `BambuStudio`). This loads the sliced project (plate layout + toolpath preview)
     in the real slicer so the operator can eyeball it at full fidelity — a richer review than the
     preview PNG, and the natural place to *approve* before dispatch. It **opens a file; it dispatches
     nothing** — read-only, on the operator's side of the gate. Offer it, don't force it (a headless run
     or an operator who trusts the PNG skips it). **Approving in Studio does not change where dispatch
     happens:** the recorded path stays `bambu print send --record` (which writes the
     `docs/prints/<date>-<slug>/` record). If the operator instead hits *Print* inside Studio, that works
     but bypasses our record loop — say so, so it is a chosen trade, not a silent gap.

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

## Self-healing — how a finding graduates (design §8, task #46)

This is the repo's graduation rule ([`CLAUDE.md`](../../../CLAUDE.md), "The graduation rule") applied to
printing: a defect found and fixed on a real plate must leave behind the thing that catches it next
time. Here that thing is a [`best-practices.md`](best-practices.md) example the *next plan is made to
honor* — the print-plan analogue of "the test that fails before the fix and passes after".

**What graduates — two tracks, and neither is a CAL coupon reading:**

*Track 1 — a physical plate finding* (all three must hold):
1. It came off **our** machine — a reading from a plate, not a figure from literature.
2. It is **physical and new** — not a catalog defect we merely re-hit (recovery-loop step 5). Re-hitting
   a known defect changes nothing; a new datum does.
3. It is a **practice** finding about a decision this skill owns (orientation, supports, brim, filament,
   arrangement, a printability limit) — **not** a `settles: CAL-…` coupon reading. Coupon readings
   propagate through the bet registry, not here (see the boundary below).

*Track 2 — an operational / slice-path / tooling finding* (all three must hold): a learning that surfaces
while **running the skill** — slicing, arranging, dispatching, reading the device — rather than off a
plate. It graduates when it is:
1. **Reproducible in our toolchain** — a behavior of our slicer profiles, the `bambu` CLI, or the
   device path that we observed and can trigger again, not a one-off guess.
2. **New** — not already an example or rule here.
3. About a **step this skill owns or drives**, and **not** a `settles: CAL-…` reading (those still go to
   the bet registry). *Worked example, 2026-09-17:* the shipped `0.20mm Standard @BBL X2D` profile's
   `brim_type = auto_brim` silently brims the MC-6 towers — a slice-path footgun caught before any plate,
   graduated to "Our examples" (PR #210). No plate was printed, so Track 1 would have rejected it; Track 2
   is exactly for this.

**How it graduates:**
1. **Carry the provenance.** The example records the plate's process identity — the `how`
   (machine / material / nozzle / layer / profile) and the record dir. *A finding without its profile
   header is anecdote, not a datum, and does not graduate* (the calibration provenance discipline).
2. **Prefer a tag-flip over a new rule.** If the finding confirms or refutes a rule already in
   best-practices, flip *that* rule's confidence tag to `[measured]` with our number and the plate —
   do not add a second, parallel rule. One owner per fact (D-052 no-fork). A genuinely new finding
   becomes a new `[measured]` example under "Our examples".
3. **Make it fails-before / passes-after.** State the example so a plan written *before* it would have
   repeated the defect and a plan written *after* honors it — that is what makes it a test, not a note.
4. **Do not open a register.** The example that changes the next plan *is* the durable record; a log
   nobody re-reads decays ([`CLAUDE.md`](../../../CLAUDE.md) "no issue catalog";
   [`docs/issue-register-evaluation.md`](../../../docs/issue-register-evaluation.md)). Only when the
   finding produces a **tenet** — a rule that changes how *every* future plan is made — is a durable
   line written, and it goes in best-practices' grounded-rules section as a `[measured]` rule, never a
   catalog.

**Reusable scripts & recipes — don't leave a repeatable fix as prose.** When a finding's fix is a
*command sequence you would run again* (the auto_brim fix is: materialize the full process JSON with
`brim_type` flipped, then slice the 23 rungs with `--arrange` and the trailing-`--` escape hatch), the
example must not be the only copy of it. In order of preference:
1. **Push the variation into the tool** ([`CLAUDE.md`](../../../CLAUDE.md) "Run one simple command"): a
   `bambu` CLI flag or a `make` target, so the call site stays one stable, allow-listable command
   (`bambu slice plate … --no-brim` beats a re-typed profile dance). The `bambu` CLI and the slice
   pre-flight are owned elsewhere ([`bambu` skill](../bambu/SKILL.md); coordinate with the branch that
   owns them before adding a flag — do not fork the verb).
2. **Else, a script beside this skill** — `scripts/<name>.sh` (or `.py`) in this dir, self-documenting,
   with the provenance in a header comment. This is the fallback when the fix is too skill-specific to
   belong in the shared CLI or the owning branch is mid-flight.
3. **Either way, name it where a run will find it** — reference the flag/target/script by name from the
   best-practices example that motivated it *and* from [`SKILL.md`](SKILL.md) (the "Best practices +
   self-healing" section), so the next run reaches for the tool, not the prose. A recipe nobody can
   find is a recipe that gets re-derived.

**The boundary — graduation is not calibration.** A reading against a `settles: CAL-…` coupon closes a
bet: value + `Calibrated<T>` status flip, baseline shrink, `bets.md` regenerate, design Appendix B close,
catalog Status flip — the five-step propagate owned by [`prototype`](../prototype/SKILL.md) /
[`calibrate`](../calibrate/SKILL.md), never this file. best-practices.md graduates *practice* rules; the
bet registry graduates *measured constants*. Keeping them apart is why the calibration exception (below)
short-circuits this skill entirely for a coupon plate.

## The calibration exception

For any plate carrying a `settles: CAL-…` reading, **skip this whole rubric**: coupon settings are
measurements fixed by the bench sheet, not preferences. Defer wholly to
[`prototype`](../prototype/SKILL.md) / [`calibrate`](../calibrate/SKILL.md).
