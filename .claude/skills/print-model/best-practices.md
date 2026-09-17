# print-model best practices (read at run time)

Grounded rules the print-model design doc establishes, **plus our own real examples** as we practice
them. This file is **self-healing**: a defect found on a real plate graduates into an example that
fails-before / passes-after the next plan — the repo's graduation rule
([`CLAUDE.md`](../../../CLAUDE.md), "The graduation rule") applied to printing. Grounded rules and their
hedges are attributed in the print-model design doc (docs/print-model-design.md, PR #191) and its
research file; this file adds *our* data on top.

> **How to read this file.** Every rule below carries a **confidence tag** so a plan can weight it
> honestly — a master states how sure they are, not just what they'd do:
> - **[grounded]** — cited to a source the research file records as actually fetched.
> - **[attributed]** — from a named community/secondary source, carried *with its hedge* (K1); we have
>   not measured it on this machine, so it is advice, not a datum.
> - **[wants-CAL]** — unmeasured on *our* X2D; a real plate would settle it. The bet id, where one is
>   registered, is named so a reading can close it.
> - **[measured]** — our own datum from a plate that came off *this* machine. There are none yet; task
>   #46 wires the graduation that fills this tag, and every [attributed]/[wants-CAL] rule is a candidate
>   to be *replaced* by a [measured] one the first time a plate settles it.
>
> Numbers and their `**Default:**` markers live in the design doc (docs/print-model-design.md §5.x),
> which owns them; this file states the *rule* and its confidence and points there — it never restates a
> default (DRY, one owner per number).

## Our examples (real, from this project)

- **Known-good X2D Plate-1 slice trio.** machine `Bambu Lab X2D 0.4 nozzle` · process
  `0.20mm Standard @BBL X2D` · filament `Bambu PLA Basic @BBL X2D 0.4 nozzle`. Slices clean end-to-end
  to an X2D-headed `.3mf` (`printer_model = Bambu Lab X2D`, `nozzle_diameter = 0.4,0.4`). Source: memory
  *bambu-x2d-bringup* and the Plate-1 bench sheet.
- **MC-4 overhang fan → supports OFF.** The calibration fan coupon is sliced deliberately with supports
  off (its whole point is to read unsupported overhang) — a calibration case where the setting is a
  *measurement*, not a choice. Pre-flight eyeballed OK (full 360° funnel, base on bed, flare up).
- **The whole 23-rung machine card slices onto one plate in one command.** No composite STL and no CLI
  change: pass one rung as the `slice plate <model>` positional and the other 22 after `--`, with
  `--arrange` — the verb forwards the trailing STLs to BambuStudio as model files and libnest2d packs
  them (`bambu slice plate MC1BoreSweep.stl --arrange -s "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL
  X2D" -f "Bambu PLA Basic @BBL X2D 0.4 nozzle" -- <22 more .stl>`). Sliced 2026-09-17 to a valid
  23-object X2D `.3mf` (89.7 cm³, one material/profile/session — the card's hard requirement).
- **Card slice → brim OFF is not a no-op; the default profile fights you.** The shipped
  `0.20mm Standard @BBL X2D` process carries `brim_type = auto_brim`, which **silently brims the MC-6
  towers** (found on the 2026-09-17 slice: a `; FEATURE: Brim` block inside MC6Tower05's footprint) —
  brim on an adhesion coupon invalidates `CAL-BED-01`, and on the MC-5 plate would mask warp
  (`CAL-WRP-01`). The bench-sheet pre-flight already *requires* "bare plate, no brim/raft"; this is the
  mechanism that makes it non-trivial. Fix: force `brim_type = no_brim` plate-wide. Headless, an
  *inheriting stub* (`"inherits": "0.20mm Standard @BBL X2D"`) is rejected `process not compatible with
  printer` (the parent's `compatible_printers` is dropped); **materialize the full process JSON with only
  `brim_type` flipped** and pass it as the process token. Re-sliced: brim 0, supports 0, raft 0. (A loose
  skirt remains — neither brim nor raft, not attached to a coupon, so it does not touch the reads.)
- **LEGO sources slice clean at 0.4 mm.** `ClassicBrick.stl`, `RosetteBrick.stl`, and `StarBrick.stl`
  all slice by preset name to a valid X2D plate at 0.4 mm — no profile-specific surprise before Plate 2.
- **Loaded filament, read live (2026-09-17).** `bambu filament` read AMS 0 slot 0 =
  PLA Basic · #F5547C · GFA00 · 100%, plus a loaded external `vir_slot`. Confirms the discovery seam the
  filament decision depends on.

## Grounded rules, by decision

The rules the design doc grounds, organized in the order a run works the decisions (§4). Each names the
design section that owns its numbers and carries the source's own hedge.

### Nozzle (design §5.1, research Topic 8)

- **[grounded] Start from the default, then justify every deviation.** The default nozzle is the design
  §5.1 `**Default:**` marker (advisory — the source that sets it was bot-blocked, so §5.1 flags it as
  such); a plan states it and only moves off it for a *stated* cause.
- **[grounded] Min-feature drives it down.** A fine feature or fine text below the default's comfortable
  floor calls for the smaller nozzle; a large/functional part with no fine feature can go up for speed.
- **[attributed] The larger-nozzle speed win (~30–40% faster than the default) is attributed, not
  measured.** It rides in as a community figure; it **[wants-CAL]** a real timing bet before a plan
  treats it as fact.
- **[grounded] Sanity bounds.** Layer height sits at roughly a quarter-to-three-quarters of the nozzle
  diameter, and the single-wall floor is about one nozzle diameter — use these to catch an impossible
  combination before slicing (see the footgun below).
- **[wants-CAL] One nozzle diameter per plate on the X2D's dual head is a K2 upper bound**, not a
  confirmed capability — `[X2D-UNCONFIRMED — H2-proxy]` in the research. Never promise mixed-nozzle on
  one plate as if it were tested.

### Orientation (design §5.2)

- **[grounded] Orientation minimizes support burden, not strength.** Score candidate bases by the
  support they require; pick the cheapest sound base. This is what the surveyed tools (Tweaker-3 and
  peers) actually optimize.
- **[grounded] Layer-line strength is *reported*, never *claimed-optimized* (K1).** If a load axis runs
  across the layer lines, say so as a weakness advisory — no surveyed tool orients for strength, so a
  plan must not imply it did.
- **[grounded] Reorienting to delete supports beats adding them.** If a cheaper base removes the support
  a part would otherwise need, that is the offer — surfaced by the §7 footgun sweep.

### Supports / infill / brim (design §5.3)

- **[grounded] Supports are tree-type and threshold-gated.** Advise supports only past the overhang
  threshold the design grounds; below it, none.
- **[grounded] Defer infill to the profile.** Density and pattern default to the slicer profile; advise a
  change only on a *stated* cause — load-bearing → denser, pure display → lighter. A bare infill number
  is a D3 violation and a preference masquerading as a fact.
- **[attributed] Brim/raft is thin-sourced — attribute, never assert.** Any brim/raft advice carries its
  named community source (§5.3 marks the sources as thin/secondary). It **[wants-CAL]**; when a real
  plate settles adhesion, the community rule is replaced by our datum here.

### Arrangement (design §5.4, research Topic 4)

- **[grounded] Count and footprint are inputs, not guesses.** Pack the given repeats; rotate-to-fit is an
  in-plane **Z-rotation**, never a re-orientation (that would undo the §5.2 decision).
- **[grounded] Nesting honours spacing.** The libnest2d NFP pack tries 0/45/90/135° and honours the
  `spacing` minimum gap; a by-object sequence expands each arrange polygon by `max(spacing,
  extruder_radius)`.
- **[grounded] A rotate advisory fires only on a strict win.** Offer a rotation only when it strictly
  increases the count or strictly frees bed; never churn the layout for a tie.
- **[wants-CAL] Dual-nozzle bed-zoning is an unconfirmed upper bound** (`[X2D-UNCONFIRMED]`), same K2
  caveat as the nozzle note.

### Filament (design §5.5)

- **[grounded] Match the loaded filament, state the match, ask only when several are plausible.** Bias to
  action: one clear match is chosen and *stated*; `AskUserQuestion` is reserved for the genuinely
  ambiguous case (design §5.5, and the global "stop and ask" rule).
- **[grounded] Wrong-filament-for-the-use is a footgun, not a silent accept.** PLA on a functional or
  heat-exposed part is surfaced as a §7 advisory pointing at this decision.
- **[grounded] Low remaining is a footgun.** A tray too low to finish the plate is flagged before slicing,
  not discovered mid-print.

### Freshness (design §6.3)

- **[grounded] A record is fresh or it is anecdote.** A reading without its profile header, or a stale
  record, is not calibration; the freshness hook/gate (task #39) keeps records current so a reprint reads
  from a number, not a memory.

## Proactive-advisory rules (design §7)

The §7 sweep is an *offer* layer, never an auto-change — these are the rules it applies (the run-time
procedure is [`rubric.md`](rubric.md) §Proactive advisories):

- **[grounded] Fill unused bed** only when the leftover area is ≥ one more part footprint; reuse the
  §5.4 pack, and stay silent on a near-full plate.
- **[grounded] Scale-up is for no-fixed-dimension parts only.** Never offer to scale a dimensioned or
  functional part (a LEGO stud, an orb at spec, a coupon, any mating part) — scaling breaks it — and it
  is always a question, never an assumption.
- **[grounded] The footgun catches are collected from the decisions that own them** (thin wall §5.1,
  removable supports §5.2, fragile layer-line §5.2, wrong filament §5.5), not re-derived in the sweep.
- **[grounded] Say nothing when nothing fires.** No invented advice.

## The one footgun that is a hard stop, not an offer

- **[grounded] A wall thinner than the chosen nozzle's single-wall floor cannot print.** Catch it before
  slicing rather than let the slicer silently drop the wall or Arachne it to a single bead. The fix is a
  *smaller nozzle*, not a silent drop — surfaced as the §7 thin-wall footgun, and grounded against the
  MC-2 wall ladder once `CAL-FEA-01` settles the floor on our machine.

## The calibration exception

Calibration coupons (`settles: CAL-…`) never take advice from this file: their settings are measurements
fixed by the bench sheet. See [`prototype`](../prototype/SKILL.md) / [`calibrate`](../calibrate/SKILL.md).

## How a finding graduates here (self-healing, design §8)

The full run-time procedure — what graduates, the tag-flip-over-new-rule preference, the fails-before /
passes-after shape, and the "no register" discipline — is [`rubric.md`](rubric.md) §Self-healing. In
short:

1. A plate comes off **our** machine and a defect (or a confirmed-good setting) is observed and recorded
   against the print record's `feedback` block + `photos[]` (design §6). The record is the evidence.
2. It graduates here only if it is **physical, new** (not a re-hit catalog defect), and a **practice**
   finding — a `settles: CAL-…` coupon reading is *not* a practice finding; it closes a bet through the
   [`prototype`](../prototype/SKILL.md) / [`calibrate`](../calibrate/SKILL.md) propagate loop, never
   this file (the boundary in the rubric).
3. Carrying its plate's process identity (the `how`: machine / material / nozzle / layer / profile — a
   finding without a profile header is anecdote, not a datum), it either **flips an existing rule's
   confidence tag to `[measured]`** with our number and the plate (preferred — one owner per fact,
   D-052) or becomes a new `[measured]` example under "Our examples".
4. It is stated so the *next plan honors it* — a plan made before would have repeated the defect, one
   made after does not: the repo's fails-before / passes-after obligation, applied to printing. No
   register is opened; this example *is* the durable record.
