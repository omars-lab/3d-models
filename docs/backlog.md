# Print backlog — what a printer unblocks, and in what order

Status: **PLANNING DOCUMENT, NOTHING MEASURED.** No print has ever been made on
this project. Every physical number in every design doc here is either read out
of someone else's literature or is an explicitly-labelled unmeasured default,
and the generated bet registry agrees:
[`.claude/skills/calibrate/bets.md`](../.claude/skills/calibrate/bets.md) reads
**12 registered bets · 16 `Calibrated` records — 16 provisional, 0 measured**.

Scope: this file sequences the work that is blocked on *owning a printer*, and
separates it from the work that has queued up behind it but is not printer-gated
at all. It invents no numbers. Where the repo states a mass, a volume or a time,
it is quoted with its source; where it does not, the cell says **not stated**,
and where the repo's own figure is labelled an estimate, that label travels with
it.

Three related documents already exist and this one does not replace them:
[`.claude/skills/prototype/catalog.md`](../.claude/skills/prototype/catalog.md)
is the per-coupon detail and the place results get logged;
[`calibration-design.md`](calibration-design.md) is the machine card's coupon
design doc; [`.claude/skills/calibrate/protocol.md`](../.claude/skills/calibrate/protocol.md)
is the measurement ceremony. This file is the *order*, the *cost*, and the
*ledger of what is still missing*.

---

## 1. Where the project actually stands

**What has been searched, so the claims below can be read for what they are.**
`CAL-*` ids were grepped across all three repos of the system: `3d-models`
(`docs/` and `.claude/`), `bikar` (read-only, via the `bikar-lego-lab` worktree),
and `qiyas`. Fourteen ids are registered in `CAL_BETS` (twelve at the original
sweep, plus the two mural bets `CAL-REG-01`/`CAL-CLB-01` registered 2026-08-02);
one more, `CAL-SEA-01`, appears twice in `3d-models` only, in both cases as a bet that
[`hemisphere-split-design.md`](hemisphere-split-design.md) §Appendix B and its
grounding audit deliberately **declined to mint**. `qiyas` contains no `CAL-*`
id at all. That is the whole set as it exists on disk today; it is not a claim
about bets that could be minted.

| | Count | Note |
|---|---|---|
| Registered `CAL-*` bets | 14 | 12 with a coupon, 4 without a record in bikar (`CAL-OVH-01`, `CAL-STR-01`, and the two mural bets `CAL-REG-01`, `CAL-CLB-01`) |
| `Calibrated<T>` records | 16 | all provisional, all listed in bikar's `.calibration-baseline.json` |
| Bets settled by the machine card (MC-1…MC-6) | 7 | 12 of the 16 records |
| Bets settled by design-specific coupons | 4 | `CAL-RIB-01` (LG-F1), `CAL-STK-01` (LG-S1), `CAL-DET-01` + `CAL-CLP-01` (W-C1) — 4 records |
| Bets with no coupon anywhere | 1 | `CAL-STR-01`, Z-layer strength ratio — registry says it "needs a load rig, which does not exist" |
| Entries in the prototype catalog | 28 | 24 coupons (P1–P7, MC-1…MC-6, W-F1, W-C1, LG-F1/F2/S1/R1/D1/B1/B2/P1/P2) + the 4 deliverables C1, C2, W1, W2 catalogued 2026-08-03 (§3.5) |
| `.bkr` coupon files that exist today | 5 | `Machine-Card`, `Fit-Coupon`, `Clipseat-Fit-Coupon`, `Clip-Coupon`, `Lego-Clutch-Coupon` |

**What is already built, so no one re-does it.** The machine card is authored and
every rung renders: [`calibration-design.md`](calibration-design.md) §7 carries a
23-piece verification table with euler, watertightness, triangle count and volume
per piece, and its own status line says **"AUTHORED, UNPRINTED … no calibration
bet is settled."** The Lego engine phases M6/M7/P0/P1/P2/P3 are all marked
complete in [`lego-lab-design.md`](lego-lab-design.md) §10, and that table records
the reason the LG coupons stopped gating M6: a knob can ship unmeasured where a
baked constant cannot ([`decisions-log.md`](decisions-log.md) D-005, superseding
D-003). So the printer is no longer a *build* blocker anywhere in the system —
it is a **truth** blocker.

**Which printer.** The repo does not record a purchased machine. What it records
is a menu: bikar's `packages/knobs/src/machines.ts` ships ten `PrintTarget`
entries, of which four are Bambu Lab (X1 Carbon, P1S, A1, A1 mini), two Prusa,
one Creality, two powder services and one `Custom…`. Treat "a Bambu A1 / P1S /
X1C class machine" as the *expectation* it is, not as a fact this repo asserts —
and note that under
[`.claude/skills/calibrate/protocol.md`](../.claude/skills/calibrate/protocol.md)
it does not matter for planning, because every number below is a property of the
*(machine, material, colour, spool, nozzle, layer, profile)* tuple and has to be
re-earned on any other one.

---

## 2. The headline sequence

Ordered by **downstream work unblocked per plate**, not by document age. Each
plate names what it settles and what it releases.

### Plate 1 — the machine card, all six coupons, one session

`MC-1` bore & fit · `MC-2` wall ladder · `MC-3` bridge plate · `MC-4` overhang fan
· `MC-5` warp plate · `MC-6` bed-contact towers.

**Why first, and why nothing else can honestly go first.** The card measures the
*(printer, material, nozzle, profile)* tuple once. Seven of the fourteen registered
bets and twelve of the sixteen provisional records are on this one card. Four
separate design coupons — W-F1, W-C1, LG-F1 and P1 — each independently planned
to measure some of warp, wall floor and bore fit before the card existed;
[`calibration-design.md`](calibration-design.md) §1 is the argument for
collapsing them, and both W-F1 Q2 and LG-F1 Q5 have already been **re-pointed**
at MC-5 and MC-2 respectively in the catalog. Printing a design coupon before the
card means measuring the printer inside a clip, a brick and an orb, and then not
being able to tell a design result from a machine result.

`calibration-design.md` §9 asks for the whole card in **one material, one
profile, one session** where the bed allows it — "a card printed across two
sessions has two profile headers and is two half-cards." Whether all 23 pieces
fit one plate depends on the machine, which is why the doc states the constraint
rather than asserting the plate.

**Cost, as the repo states it:** total solid volume across all 23 pieces
**89.7 cm³**, "roughly 111 g of PLA at 100% infill, less in practice"
([`calibration-design.md`](calibration-design.md) §7). `MC3BridgePlate` alone is
27.5 cm³ and `MC5WarpPlate` 15.3 cm³. Print time: **not stated**.

**Three things this plate will not do.** `MC-2`'s four sub-floor rungs FAIL
`--check` by design and must be rendered without it (§3.1). `MC-3`'s and `MC-4`'s
`--check` PASS says nothing about the 2 mm bridged ceiling or the 2.00 mm fan
wall — both are outside the min-feature computation (§8). And
`MIN_BED_CONTACT_RATIO` is **not directly measured** by MC-6 at all: a rod's
first layer is its widest, so the ratio reads 100% on every rung and the constant
"rides the same bet and gets settled by inference from the absolute figure"
(§8). None of these is a defect to fix before printing; all three are recorded
so a reading is not over-claimed afterwards.

**What releases.** `FIT_GAP_MM` / `FIT_TOL_MM` / `CLIP_CLEARANCE_MM`,
`holeCompMm` and the two `*_calibrated` printer profiles, `DEFAULT_MIN_FEATURE_MM`
/ `KEYHOLE_FRONT_FLOOR_MM` / `PERIMETER_WIDTH_MM`, `BRIDGE_SPAN_MAX_MM`, the F5
overhang threshold, `warpMm` (today literally absent), and both F7 bed-contact
triggers. Downstream: `c2-assembly` B.3 and B.6, `piece-composition` B.2,
`print-validation` B.2 and B.4, `w2-connector` B.3 and B.5, `lego-lab` B.5, and
`hemisphere-split`'s whole constants table. Also W-F1's blade-clearance conversion
and, per the catalog, "P1 Q1 … is MC-2's question asked in strut form."

### Plate 2 — the LEGO clutch ladder: LG-F1, LG-F2 and LG-R1

All three are `--piece` renders of the **same file**,
`bikar/patterns/Coupons/Lego-Clutch-Coupon.bkr`
(`CouponAnchorPlate`, `CouponStudPlate`, `CouponPinStrip`), and all three are
three-plate 2×4-class bodies. **They can share a plate** to the extent the bed
allows — the constraint is rung count, not compatibility: LG-F1 alone is a
five-rung `ribMm` ladder crossed with three `engage` values, and LG-F2 and LG-R1
are five rungs each. The repo states no volume or mass for any of them.

**Why second.** The catalog's own framing is unusually strong here: "**No usable
clutch dimension can be derived on paper**", because LEGO's clutch is authored
from a tangency condition but realised as an elastic interference, no source
publishes a metrologically-obtained anti-stud tube diameter, and — per the
grounding audit — **no public source anywhere reports caliper measurements on a
printed LEGO-compatible stud, or a clutch durability cycle count**. LG-F2 and
LG-D1 "would be the first public data of their kind"
([`lego-lab-design.md`](lego-lab-design.md) §8). `CAL-RIB-01` is named in that
doc's Appendix B.8 as **"the largest unverified bet in the document."**

**What it decides that is not a number.** LG-F2 Q1 decides whether `studs full`
and `studs edge` ship at all, or ship disabled with a documented nozzle
requirement while `studs none` carries the feature ([`lego-lab-design.md`](lego-lab-design.md)
§11 Q1). LG-R1 Q3 decides whether 1×N footprints are supported or refused with a
pointer (§11 Q2). Two shipped-surface decisions from one plate.

**Carry these three conditions onto the bench sheet.** (a) Every rung mates
against a **real LEGO part the user owns** — the catalog is explicit that
compatibility with our own output proves nothing. (b) Print without `--check`;
the tube wall at 0.857 mm and the 0.1 mm rib are sub-floor by design. (c) Record
**spool and dryness**, not just machine and material — the catalog cites Bambu's
own documentation that "dry filament results in a looser fit", which if true here
means a LEGO profile is valid for a spool rather than for a printer.

**One published counterexample worth reading before slicing.** LG-F2's print
target asks for one ladder at 0.4 mm and, if available, one at 0.2–0.3 mm,
because Brickset printed the same brick both ways and reported the **0.4 mm**
part clutching *better*. "Just use a finer nozzle" is not an established escape
hatch, and §11 Q1 says the answer may be "neither nozzle, without a rib."

### Plate 3 — the W-series connector joint: W-F1 then W-C1

W-F1 is the blade-clearance fit coupon; W-C1 is the CornerClip joint that
consumes its number. The catalog blocks W-C1 on W-F1, so these are **two plates
in sequence, not one shared plate**. Whether MC-1 might supply W-F1's number
outright was §7 item 1's open question; it was resolved on 2026-08-02 as **no**
([`decisions-log.md`](decisions-log.md) D-008) — MC-1 measures a bore-and-pin
joint, and a blade that drops down a channel and then twists under load can pass
the drop and still bind on the twist. Two plates it is.

**Why third rather than second.** W-C1 settles two bets (`CAL-DET-01`,
`CAL-CLP-01`) against LG-F1's one, but it settles them for a feature whose
deliverable — `patterns/Walls/Clip-Wall.bkr`, "the first full wall once the joint
is proven" — is a *later* build, whereas the LEGO surface is already shipped and
running on unmeasured knobs. W-C1's headline is a **grammar default**: rebate
versus proud, judged in raking light on a real four-corner joint
([`w2-connector-design.md`](w2-connector-design.md) §10 Q1, and the same question
as [`tile-wall-design.md`](tile-wall-design.md) §10 Q1 — one print closes both).

**Conditions.** Clips in PETG; dummy tiles in the wall's tile material, to match
shrinkage. `--check` on the **clip** part reports FAIL by design — its bayonet
blade is ~0.6 mm — and whether that thin flexing blade survives repeated
seat/unseat is W-C1 Q3, i.e. the mesh-gate exemption is itself under test.
W-C1 Q2 (warp) has already been re-pointed: it **checks the clip's capture floor
against MC-5's number** rather than deriving one
([`w2-connector-design.md`](w2-connector-design.md) §9 and §11 Q3, corrected in
commit `14e1625`).

### Plate 4 — the first full orb: P2 Star-Orb at defaults

`bikar/patterns/Orbs/Star-Orb.bkr` at declared defaults (R=60, struts 3×2.4) —
`build/stls/StarOrb.stl`, **5,040 tris, 45.7 cm³** (catalog P2). This is the
first plate on the list that settles **no `CAL-*` bet**, and it is here anyway
because it is the flagship deliverable: it feeds the harness print-prototype
task, the gallery's "what does an orb cost" note, and photography of a real
object. Its Q5 (point bed contact on a sphere) is inherited from MC-6's threshold
rather than measured here — the bets registry says MC-6 "supersed[es] the
prototype catalog P2 Q5 measurement".

P1, the three-rung strut coupon, is **not** ahead of it any more: the catalog
says P2 is "blocked on P1's answer to Q1 only if P1 fails at 3 mm", and P1's Q1
is MC-2's question in strut form. If Plate 1's MC-2 puts the wall floor at or
below 1.2 mm, P1 becomes an optional confirmation rather than a gate. The three
P1 STLs are already rendered on disk at
`build/stls/coupons/P1-StrutCoupon-W{1.5,2,3}.stl` (2026-07-27) at
**15.8 / 20.3 / 28.2 cm³, ≈80 g PLA for the trio**, so it is cheap to add
alongside if the bed has room.

### Plate 5 and beyond

In catalog order, each gated on the plate above it: **P3** hemisphere split (cut
in the slicer on the `vertex` axis, not the equator — needs P2's support-scar
baseline to compare against); **P4** Rosette-Orb fine-feature fidelity;
**LG-D1** clutch durability (needs a *passing* LG-F1 rung); **LG-B1** the first
patterned brick (needs LG-F1's clutch number); **LG-S1** the printed-onto-printed
stack; **P5** the weave family, which the catalog expects to *fail or disappoint
on FDM* and pairs with an SLS/MJF service order; **P6** size extremes; **LG-B2**
the off-grid rosette brick, whose `.bkr` **does not exist and must be authored
first**; **LG-P1** the mural seam-registration pair (needs LG-F1's rung; its
minimal `Seam-Coupon.bkr` is authored — bikar `73514f1`); **LG-P2** the clone-plate clutch
differential (needs LG-F1's rung and clone plates bought); **P7** material and
finish.

**K10 — where the FDM findings stop.** P5 deliberately crosses a process
boundary: it prints the same ribbon gap on FDM and orders it from an SLS/MJF
service. Nothing measured on Plates 1–4 transfers across that boundary. A powder
process has no bed adhesion in the FDM sense (MC-6), no first-layer elephant's
foot, no unsupported bridge (MC-3) and no overhang angle (MC-4) — the part is
supported by unfused powder throughout — and its shrinkage and clearance
behaviour is a different physics from differential-cooling warp (MC-5). So the
service result in P5 Q3 must be recorded as its own profile header under
[`protocol.md`](../.claude/skills/calibrate/protocol.md), and **no `CAL-*` bet
may be closed from it**: every one of those bets is scoped to a filament machine.
The same applies to P7's resin candidate.

---

## 3. The print-gated register

Every item this audit found that cannot be settled without a printer. "Exists"
means a `.bkr` (or a documented CLI line over an existing `.bkr`) is on disk
today. Volumes and masses are quoted only where the repo states them.

### 3.1 Machine card — the shared substrate

| id | measures | demanded by | unblocks | `.bkr` | cost as stated |
|---|---|---|---|---|---|
| MC-1 | bore ⌀ drift 3–10 mm, and which gap seats as press/snug/sliding/free | [`calibration-design.md`](calibration-design.md) §5.1 | `CAL-FIT-01`, `CAL-HOL-01`; `c2-assembly` B.3+B.6, `piece-composition` B.2; W-F1's conversion | exists — `Machine-Card.bkr`, 9 pieces | 11.8 + 7.5 cm³ plates + 6 pins ≤1.2 cm³ each |
| MC-2 | thinnest wall that prints as a handleable feature, **and the direction of the error** | §5.2 | `CAL-FEA-01` (3 records); `lego-lab` B.5 and the §7.4 floor override; P1 Q1; LG-F1 Q5 | exists — 7 tube rungs | 0.2–1.3 cm³ per rung |
| MC-3 | first bridge span that **sags** (not fails), ⌀4–25 mm | §5.3 | `CAL-BRG-01`; `w2-connector` B.3, `print-validation` B.4, `lego-lab` §11 Q4 / V12 | exists — 1 plate | 27.5 cm³ |
| MC-4 | first overhang angle showing curl or droop, 20–60° from vertical | §5.4 | `CAL-OVH-01`; `print-validation` B.2 and the F5 tier split | exists — 1 revolve | 11.9 cm³ |
| MC-5 | first-plate corner warp, four corners on a flat reference | §5.5 | `CAL-WRP-01`; `w2-connector` B.5 and §11 Q3; W-F1 Q2 and W-C1's capture floor | exists — 1 plate | 15.3 cm³ |
| MC-6 | smallest footprint that holds a 40 mm column; elephant's foot | §5.6 | `CAL-BED-01`; `print-validation` F7; P2 Q5; `hemisphere-split` A0's headline | exists — 4 towers | 0.3–4.5 cm³ each |

Whole card: **89.7 cm³ / ≈111 g PLA at 100% infill**, repo-stated. Time: not stated.

### 3.2 LEGO ladder

| id | measures | demanded by | unblocks | `.bkr` | cost |
|---|---|---|---|---|---|
| LG-F1 | which `ribMm` (0/0.05/0.10/0.15/0.20) clutches a real LEGO stud; whether rung 0 clutches at all; whether `engage 1.6` sags as §3.6 predicts | [`lego-lab-design.md`](lego-lab-design.md) §8, B.8 | `CAL-RIB-01`; the `engage` default; LG-D1, LG-B1, LG-B2 all gate on it | exists — `Lego-Clutch-Coupon.bkr --piece CouponAnchorPlate` | not stated |
| LG-F2 | realised-vs-authored stud ⌀ at five rungs; **whether `studs full`/`studs edge` ship at all** | §8, §11 Q1 | the `studDia` profile entry; the Lab's nozzle requirement | exists — `--piece CouponStudPlate` | not stated |
| LG-R1 | whether a printed ⌀3.2 solid pin clutches, and whether FDM anisotropy shears it | §8, §11 Q2, §5.2 | the `pinDia` entry; the anchor solver's 1×N branch; whether 1×N ships or errors | exists — `--piece CouponPinStrip` | not stated |
| LG-S1 | max total radial interference two **printed** parts swallow before the joint will not push together | §10 P1, [`decisions-log.md`](decisions-log.md) D-006 | `CAL-STK-01`; `STUD_ENTRY_MAX_MM`; whether the fit profile grows a printed-pair entry; the warning text bikar emits on every `Brick-Stack` render | exists — `Brick-Stack.bkr --format parts` | not stated |
| LG-D1 | does clutch survive 100 seat/unseat cycles, and where does it fail | §8 | the material recommendation; §11 Q6's compliance-proxy question; B.8's "durable or one-shot" | reuses LG-F1's winning rung | not stated |
| LG-B1 | do relief and clutch coexist; is an 8-fold star legible at 4×4 (31.8 mm) | §8 | `relief depth` and `engage` defaults; the P1 compatibility matrix's first ✅ row | exists — `patterns/Lego/Star-Brick.bkr` | not stated |
| LG-B2 | does rotation lock hold on an incommensurable outline; **how much clutch is lost giving up the tangent side wall** | §8, §5.3, B.2 | B.2's rotation-lock criterion; V8's WARN-not-ERROR call; the 5-fold matrix row | **authored** (bikar `bf6c602`) — `patterns/Lego/Rosette-Brick.bkr`, a ten-fold rosette (five-fold girih family) riding the `footprint outline` mode that shipped in the same commit; six tubes at the default radius, corner-swept by the Lab | not stated |
| LG-P1 | lateral jog of a relief line crossing a mural seam on a real baseplate; whether the 0.2 mm gap reads as a groove | [`lego-pattern-set-design.md`](lego-pattern-set-design.md) §3 | `CAL-REG-01`; D-013's reversal condition; the gallery's "seam 0.2 mm" chip | **authored** (bikar `73514f1`) — `patterns/Lego/Seam-Coupon.bkr` (a 2×1-piece mural, two bars crossing the seam; one bar would delete the 2×2 pieces' only anchor — see the catalog entry); Star-Mural exists but is not minimal | not stated |
| LG-P2 | whether LG-F1's winning rib also clutches a clone plate; clone pitch error accumulated over 8 studs | `lego-pattern-set-design.md` §5, [`lego-baseplate-seam-survey.md`](research/lego-baseplate-seam-survey.md) | `CAL-CLB-01`; the K2 hedge "LEGO-brand verified, clone unmeasured" | reuses LG-F1's winning rung; needs plates bought, not modelled | not stated |

### 3.3 W-series connector

| id | measures | demanded by | unblocks | `.bkr` | cost |
|---|---|---|---|---|---|
| W-F1 | the blade clearance that seats a clip firmly without forcing; whether it differs by tile material | [`w2-connector-design.md`](w2-connector-design.md) §8 | the clip-joint half of `CAL-FIT-01`; the `--fit-profile` W-C1 and `Clip-Wall.bkr` inherit | exists — `Clipseat-Fit-Coupon.bkr`, 6 pieces (written 2026-08-02, D-008) | not stated |
| W-C1 | rebate vs proud in raking light; detent past-centre feel; PETG jaw survival; front-face lippage | §8, §10 Q1; [`tile-wall-design.md`](tile-wall-design.md) §10 Q1 | `CAL-DET-01`, `CAL-CLP-01`; the `clipseat` grammar default; the mesh-gate sub-floor exemption for bayonet clips | exists — `Clip-Coupon.bkr`, 3 pieces | not stated |

### 3.4 Orb ladder

| id | measures | demanded by | unblocks | `.bkr` | cost |
|---|---|---|---|---|---|
| P1 | smallest `strut_width` that prints clean; whether the floor needs to be orientation-aware; star-tip acute voids; tree-support scarring | catalog P1 | `strut_width`/`strut_depth` mins in every `patterns/Orbs/*.bkr`; the mesh-gate FDM floor. **Q1 is MC-2's question in strut form** | exists — CLI param override, STLs already on disk | 15.8 / 20.3 / 28.2 cm³; **≈80 g PLA for the trio** |
| P2 | whole-sphere printability; print time and mass at defaults; dimensional accuracy; handling strength; bed contact | catalog P2; [`orb-lab-design.md`](orb-lab-design.md) §5 | the harness print-prototype task; gallery print notes | exists — `Star-Orb.bkr` at defaults | 45.7 cm³, 5,040 tris |
| P3 | whether flat-down halves beat the whole print by enough to justify engine work; seam visibility; hand alignment; `vertex` vs `face` cut plane | [`hemisphere-split-design.md`](hemisphere-split-design.md) §9.2 | the split-export go/no-go — the doc **recommends not building** and hands P3 the verdict | slicer-side cut of `StarOrb.stl`; no engine work | not stated |
| P4 | do petal-zigzag sliver voids resolve or fuse; does `inner` at its 16 mm floor print | catalog P4 | `inner`/`shoulder` ranges; the Lab's default-preset choice | exists — `Rosette-Orb.bkr` | 47.0 cm³ |
| P5 | does FDM at a 0.8 mm ribbon gap print free-moving ribbons, fuse them, or fill them; the SLS/MJF result at the same gap | catalog P5 | the Lab's tier-3 weave/FDM notice; `amplitude` defaults; the ✓/fused threshold | exists — `Rosette-Weave-Orb.bkr` | 27.9 cm³ |
| P6 | R=40 graceful shrink; R=110 warp/adhesion/time; whether strut width should scale with radius | catalog P6 | the `radius` range; the Lab ceiling-margin rule (`2R ≤ min(XYZ) − 10`) | exists — `radius` baked via the Lab | not stated |
| P7 | which material/finish matches the gallery's gold renders in person | catalog P7 | gallery photography; per-material notes in the Lab machine table | whichever orb P2–P4 crowns | not stated |

### 3.5 The four deliverables — catalogued 2026-08-03

These four are demanded by a design doc and, until 2026-08-03, had **no entry**
in [`catalog.md`](../.claude/skills/prototype/catalog.md). They now do: entries
**C1**, **C2**, **W1** and **W2**, in a `# Deliverables` section at the end of
that file, placed last because nothing else in the catalog depends on them.
Every figure in them is from a render of the shipped model at bikar `d9b3c84`,
not an estimate. §4 item 6 is closed.

| item | catalog | measures | demanded by | `.bkr` |
|---|---|---|---|---|
| W1 2×2 tile pilot | **W1** | a real ≈100 mm relief tile's mass and print time — the doc's own figures are **"estimates until the W1 2×2 pilot measures a real tile"** | [`tile-wall-design.md`](tile-wall-design.md) §7.1 | exists — `patterns/Walls/Nail-Wall.bkr`, `patterns/Pieces/Nail-Tile.bkr` |
| C1 Nail-Tile deliverable | **C1** | whether the girih tile with a countersunk nail bore prints and hangs as designed | [`piece-composition-design.md`](piece-composition-design.md) | exists — `patterns/Pieces/Nail-Tile.bkr` |
| C2 Pinned-Tiles deliverable | **C2** | whether authored ⌀2.90 press / ⌀3.15 sliding sockets against ⌀3.00 printed pins behave as the fit windows claim | [`c2-assembly-design.md`](c2-assembly-design.md) §8 | exists — `patterns/Assemblies/Pinned-Tiles.bkr` |
| Clip-Wall first full wall | **W2** | whether the proven joint scales to a four-tile wall — hanging on **four** screws, one keyhole per tile, not the one §8 used to claim | [`w2-connector-design.md`](w2-connector-design.md) §8 | exists — `patterns/Walls/Clip-Wall.bkr` |

The tile-wall estimates, quoted with their hedge: a ≈100 mm relief tile at
"~40–60 g, ~2–4 h at 0.2 mm on a modern small printer", giving ~36 tiles /
~5 days / ~2 kg for a 0.6 × 0.6 m focal panel and ~200 tiles / ~4 weeks / ~10 kg
for a 1.2 × 1.8 m accent wall. §7.1 labels the whole table "*estimates*", and
[`tile-wall-design.md`](tile-wall-design.md) §7.1 makes computing them for real
a W3 deliverable of `layout report`.

### 3.6 Blocked on more than a printer

| item | why a printer is not enough |
|---|---|
| `CAL-STR-01` — Z-layer strength ratio | The registry's own coupon field reads **"none — measuring it needs a load rig, which does not exist; registered so the gap is visible."** Consumers: [`c2-assembly-design.md`](c2-assembly-design.md) B.5. |
| Adhesive seam strength per mm² on an FFF lap face (P3 Q2) | [`hemisphere-split-design.md`](hemisphere-split-design.md) Appendix B declines to mint `CAL-SEA-01` for a feature the same doc recommends not building. A print gives the halves; the *number* needs a tensile setup this repo does not have. Recorded, deliberately, as an open question rather than a bet. |
| PLA clip creep — "creeps loose within months" | [`research/tile-wall-grounding-audit.md`](research/tile-wall-grounding-audit.md) records this as an extrapolation with "no cited source giv[ing] a loosening timeline at wall-tile stress levels." Settling it ourselves needs a printed clip **held under load for months**, i.e. calendar time and a fixture, not a print. |
| P5's SLS/MJF rung | needs a **service order**, not a printer — and per §2's K10 note, no FDM constant transfers to it. |

**Count: 28 catalog entries = 28 print-gated items**,
plus 4 items that are blocked on apparatus, calendar time or a vendor beyond the
printer.

### 3.7 Print-gated residue in the research files that no coupon claims

A separate sweep of all 17 files in [`research/`](research) for their
"could not be grounded" / "Errata" / "Misgrounded or missing citations" sections
found that the overwhelming majority of the residue needs a *download, a fetch or
a decision* — not a printer. Three items in the printer-needing minority are
already owned above (the lattice-top support question by MC-4/P3, the
interrupted-rim adhesion question by MC-6, the bow band by MC-5/W-C1). One is
not owned anywhere:

| item | what the research says | owner |
|---|---|---|
| Magnet pocket interference | [`research/tile-wall-grounding-audit.md`](research/tile-wall-grounding-audit.md) flags the "−0.1 mm standard recipe" as resting on an unverified Printables page, and notes that magnet guides **recommend the opposite** — a +0.15–0.4 mm clearance plus glue. [`research/hemisphere-split-survey.md`](research/hemisphere-split-survey.md) §8 rates it "probably irrelevant at 3 mm strut scale," which is a hedge, not a dismissal. | none — no coupon, no `CAL-*` id, no catalog entry |

If magnets stay in any design, this needs either a citation or a pocket ladder on
a plate. It is listed here rather than in §3.5 because no design doc currently
*demands* it — which is exactly why it would otherwise be lost.

---

## 4. Before the first print

Checked against the repo, not against memory. Done / not done is stated per item.

**Already done — do not redo.**

1. The machine card is authored and every rung's geometry is verified —
   23 pieces, euler, watertightness and volume in
   [`calibration-design.md`](calibration-design.md) §7, plus independent
   silhouette and Pappus checks on MC-4 and z-level checks on MC-3.
2. All four coupon `.bkr` files exist in `bikar/patterns/Coupons/`.
3. The measurement ceremony exists in full:
   [`protocol.md`](../.claude/skills/calibrate/protocol.md) carries the profile
   header, the technique rules (three readings, median, two orthogonal bore
   diameters, light jaw pressure, 30 minutes of cooling), the per-coupon
   judgement scales and a blank bench data sheet.
4. The propagation gate exists and is CI-blocking: bikar's
   `scripts/check-calibration.ts` requires every provisional record to be listed
   in `.calibration-baseline.json`, requires each bet to name a coupon, and
   blocks the file from growing without `CALIBRATION_BASELINE_MAY_GROW=1`.
5. The build envelope check exists: the Lab's machine dropdown and
   `radiusCeilingMm` already clamp the radius knob to `min(XYZ) − 10`.
6. The bikar CLI is built in the working checkout, so every render command in
   [`calibration-design.md`](calibration-design.md) §6 runs today.

**Not done — do these first.**

1. ~~**Render the machine card to disk.**~~ — **done 2026-08-03**. All 23 rungs
   are in `build/stls/coupons/machine-card/`, rendered per §6 (the
   `--check`-less lines for `MC2Wall04/06/08/10`, `--check print` for the MC-6
   towers), from bikar `60383b5`. Every rung matches
   [`calibration-design.md`](calibration-design.md) §7's table — euler,
   watertight, degenerate, minFeature, verdict, triangles, volume — and the 23
   volumes sum to the 89.7 cm³ §7 states. `build/` is not tracked on master, so
   the STLs are a local artifact; `make coupons` reproduces them.
2. ~~**Decide whether a `make coupons` target is worth it.**~~ — **done
   2026-08-03**, [`Makefile`](../Makefile) `coupons` + `validate-coupons`. The
   deciding argument was not convenience: §6's command lines carry two
   non-obvious rules — `--piece` on every line, and *no* `--check` on the four
   sub-floor MC-2 rungs — that a hand-typed session can drop without any error
   appearing. The target does not restate them; it runs
   [`build/verify_machine_card.py`](../build/verify_machine_card.py), which
   reads the rung list and the expected results out of §7 and diffs the actual
   mesh gate against them, so the doc and the geometry cannot drift apart
   quietly. It also runs `--check` on the four by-design failures specifically
   to assert that they *fail*, which is the one thing §6's own command line
   cannot show. `make validate-coupons` mutates a scratch copy of the doc seven
   ways and confirms the verifier fires on each.
3. ~~**Reconcile W-F1's `.bkr` with its catalog entry**~~ — **done 2026-08-02**,
   see §7 item 1 and [`decisions-log.md`](decisions-log.md) D-008. The coupon it
   needed did not exist and was written; nothing here waits on a printer.
4. **Buy or locate the instruments the protocol assumes**: a caliper (make and
   resolution recorded, zeroed at session start), a flat reference — granite
   plate or float glass — and feeler gauges for MC-5, and at least one **real
   LEGO plate and one real LEGO 2×4 brick** for the LG series. Bags and a marker:
   §3.2 of the coupon doc is explicit that rung identity does not survive onto
   the part, so "bag each rung as it comes off the plate" is a stated operational
   requirement, and a mis-assigned rung "is worse than a missing one because it
   produces a confident wrong number."
5. **Record the profile header before anything is measured.** The card's series
   note says the header *is* the deliverable and "the numbers are meaningless
   without it."
6. ~~**Add the four uncatalogued items in §3.5 to
   [`catalog.md`](../.claude/skills/prototype/catalog.md)**~~ — **done 2026-08-03**.
   All four are in, as entries **C1**, **C2**, **W1** and **W2** under a
   `# Deliverables` heading at the end of that file. Each was grounded by
   rendering the shipped model rather than by reading the design doc: that is
   how the W2 entry found the **"hanging on one screw"** claim that
   [`w2-connector-design.md`](w2-connector-design.md) §2 and §8 both carried and
   the compiler had been contradicting all along — a wall mints one keyhole per
   *tile*, so the deliverable hangs on four. Corrected in that doc, in
   [`tile-wall-design.md`](tile-wall-design.md) §9 and in §3.5 above, and the
   design question it was silently deciding is now W2 §11 Q6.
7. **Look at the fan in a slicer before committing filament** —
   [`calibration-design.md`](calibration-design.md) §8 lists "no raster render
   was eyeballed" as a known weakness, and MC-4 is the piece whose failure mode
   would be a silently wrong dimension.

**Slicer settings the docs pin, per coupon.** These are measurements, not
preferences, and getting them wrong makes the coupon answer a different question.

| coupon | pinned setting | why |
|---|---|---|
| MC-1 plates | flat, bores vertical | bores print as vertical holes, which is how designs use them |
| MC-1 pins | upright on the ⌀ face | a pin printed lying down is elliptical |
| MC-2 tubes | upright | the wall is a vertical perimeter loop |
| MC-3 plate | flat, **bore mouths on the bed** | flipped, there is nothing to bridge |
| MC-4 fan | upright, base on bed, **supports off** | "an overhang number measured with supports is not an overhang number" |
| MC-5 plate | flat; record brim/raft **and part-fan settings verbatim** | those are precisely what the conflicting sources disagree about |
| MC-6 towers | upright, **bare plate, no brim, no raft** | the brim is the mitigation F7 exists to recommend, so printing with one measures the brim |
| LG series | record spool **and dryness**; mate against real LEGO | fit reportedly moves with moisture |
| W-C1 | clips in PETG, tiles in the wall's tile material | to match shrinkage across the joint |

---

## 5. After each print — the propagate step

`calibrate` describes harvest → cluster → design → measure → **propagate**, and
its own rules say the bet stays open until every one of five things has
happened. The step that gets skipped is the last one, "because the catalog
already *looks* updated"
([`.claude/skills/prototype/catalog.md`](../.claude/skills/prototype/catalog.md)
workflow, "Close the CAL bet").

For any reading, the full landing sequence is:

1. the constant's value **and** its `Calibrated<T>` `provenance.status` flip
   together, from `provisional` to a `measured` record naming machine, material,
   nozzle, profile, date and coupon;
2. the entry comes **out** of bikar's `.calibration-baseline.json` — the baseline
   may only shrink, and "a closed bet that stays baselined is the gate lying";
3. `bets.md` is **regenerated** (`npm run registry:calibration`), never
   hand-edited — the file's own header says an edit "reads as a fact while it is
   only a stale opinion";
4. the design doc's Appendix B entry carrying that `[CAL-…]` tag closes with the
   measured value — the tag is a two-way link;
5. the catalog entry's Status flips, its questions are answered **by number**,
   an iteration row is dated, and commit hashes are cited in both repos.

### Which measurement lands on which constant, and what then changes behaviour

| reading | lands on | the gate or test that then behaves differently |
|---|---|---|
| MC-1 bore drift, per ⌀ | `PRINTER_PROFILES.holeCompMm` (`kernel3d/fit-profile.ts`) | `--fit-profile pla_calibrated` / `petg_calibrated` stop being names that "claim a calibration that has not happened"; `check-calibration.ts` loses a baseline row |
| MC-1 hand-judged fit classes | `FIT_GAP_MM`, and `FIT_TOL_MM` re-derived | the assembly fit-window check in `c2`; note the card's own `MC1Fit` assembly **stops evaluating** if the ladder is edited without re-cutting — that is the drift guard, and it fires either way |
| MC-2 thinnest handleable wall | `DEFAULT_MIN_FEATURE_MM` (`mesh-gate.ts`), `KEYHOLE_FRONT_FLOOR_MM`, `PERIMETER_WIDTH_MM` | the mesh gate's PASS/FAIL for **every** part in the repo; `lego-lab` §7.4's 0.70 mm brick invariant is re-argued against a real number; P1's strut floor |
| MC-3 first sagging span | `BRIDGE_SPAN_MAX_MM` (`grid-gate.ts`) | V12's warn threshold on every brick; `print-validation` F6 |
| MC-4 first curling angle | the overhang threshold in `print-gate.ts` | F5's error/warn tier split — and the reading must record **from-vertical vs from-horizontal**, since the two coincide at 45°, "which is exactly how convention bugs hide" |
| MC-5 four corner gaps | `PrinterProfile.warpMm` — today literally absent | consumers stop falling back to `capture = max(1.0, 2 × warp)`; W-C1's capture floor gets a real basis; `tile-wall` §8's "placeholder until W2" row |
| MC-6 which towers detached | `MIN_BED_CONTACT_MM2`, and `MIN_BED_CONTACT_RATIO` **by inference only** | F7 could move off warn-only; `hemisphere-split` A0's headline claim rests on this floor |
| LG-F1 winning `ribMm` | `RIB_MM_CAL` (`kernel3d/lego.ts`) | the Lego Lab fit panel's per-value provenance stops reading *unmeasured* for that row; `engage` default |
| LG-F2 realised stud ⌀ | the `studDia` LEGO profile entry | whether `studs full` / `studs edge` are enabled at all |
| LG-R1 pin result | the `pinDia` entry; the solver's 1×N branch | whether 1×N footprints compile or error with a pointer |
| LG-S1 entry ceiling | `STUD_ENTRY_MAX_MM` (`kernel3d/lego.ts`) | the port-contract error on `Brick-Stack`; the warning text in `brick-ports.ts` and the K10 paragraph in bikar's `docs/language-reference.md`, both of which currently name this coupon as the thing that has not happened |
| W-C1 detent depth | `CLIP_DETENT_MM_CAL` (`corner-clip.ts`) | the shipped detent geometry ([`w2-connector-design.md`](w2-connector-design.md) §12) |
| W-C1 seated Z bias | `CLIP_Z_BIAS_MM_CAL` | the anti-rattle preload and sub-flush setback |
| W-C1 rebate vs proud | not a constant — a **grammar default** | the `clipseat` default in `patterns/Walls/*.bkr`; closes `tile-wall` §10 Q1 too |

A reading that **refutes** the design is a success outcome of `calibrate` and
must not be deleted: "bury it and the next person re-runs the print." A ladder
that brackets wrong — every rung passing, or every rung failing — is also a
result, and [`calibration-design.md`](calibration-design.md) §2 says so before
the fact precisely so it is not logged as "the coupon didn't work."

---

## 6. Queued behind the same work, but **not** printer-gated

These have accumulated alongside the print backlog and need something other than
a printer. Filing them here rather than above is the point of this document.

### 6.1 The LDraw afternoon — needs a `.dmg`, not a printer

`--format ldraw` shipped with Lego Lab P3 (bikar `a10f4f6`, PR #53), and
[`lego-lab-design.md`](lego-lab-design.md) §10 records the one thing §14.3 asked
for that is **not** done: *"no LDraw viewer has opened the output."*
[`research/ldraw-cli-viewers.md`](research/ldraw-cli-viewers.md) costs the run.
Five items are outstanding, and one of them is the reason to do this soon:

1. **The fifth item** — LeoCAD's `lcModel::LoadLDraw` appears to drop line types
   2–5 into `mFileLines`, read back only by `SaveLDraw`. Our MPD is two type-1
   lines and 3,764 type-3 triangles, and the name resolves, so the **predicted**
   outcome is an empty model and no error at all. §14.3.1 flags this itself:
   *"K1 — this is a source reading, not an observation"*, and what has not been
   ruled out is some other path reconstituting those lines. This is the
   export-succeeds-and-yields-the-wrong-thing class the whole section exists to
   avoid, so it is worth settling before anyone relies on the format.
2. LeoCAD's behaviour on an unresolvable reference, and whether it resolves names
   against same-file `0 FILE` blocks.
3. BrickLink Studio on an inline-defined part, on import and round-trip —
   **untouched**, and §14.3.1 says nothing in the viewer survey predicts it,
   because Studio maps LDraw parts onto its own catalogue.
4. Whether `0 BFC CERTIFY CCW` is safe to emit — derivable, but "has never been
   rendered in a BFC-checking viewer", so it stays out "until someone looks."
5. LDView's parts-tracker behaviour after a failed lookup — §14.3.1 records this
   as having **largely dissolved** for a well-formed file, surviving only for a
   malformed one.

**How it is actually run, with the doc's hedge intact.** Nothing LDraw is
installed on this machine, and the research found no Homebrew formula or cask for
LDView, LeoCAD or Studio — so this is a manual download first. LDView is the
candidate to reach for, with `-VerifyLDrawDir=0` so it runs with no parts library
(our MPD references nothing outside itself). But the macOS off-screen path is
claimed **on the strength of `MacOSX/LDView/main.m` and nothing else**, rests on
CGL pbuffers (a deprecated Apple API), and LDView's own help hedges it —
*"if your video card allows this to run without displaying a window."* Untested.
The survey is also explicitly bounded: **twelve named tools, not the space of
LDraw software** (§14.3.1's own K2 note).

### 6.2 Other non-printer work found in the same sweep

| item | what it needs | source |
|---|---|---|
| `--format ldraw` opened in three viewers | downloads (§6.1) | [`lego-lab-design.md`](lego-lab-design.md) §14.3.1 |
| §11 Q6's compliance proxy — whether rib-deflection or an FEA-lite bending estimate is worth adding to the grid gate | a decision, then code; **calibrating** it needs LG-F1 and LG-D1 | [`lego-lab-design.md`](lego-lab-design.md) §11 Q6, explicitly left open |
| `layout report` production metrics (W3): plates at the declared bed size, spool count, calendar estimate | code — though the per-tile input is the W1 pilot in §3.5 | [`tile-wall-design.md`](tile-wall-design.md) §7.1 |
| `tile-wall` §10 Q2 — `checker` border parity | **decided 2026-08-03, D-016: both** — shared `border` spec as the documented path, per-pair validator for tiles that decline it. Unbuilt: the validator, and its `FAIL:` must be the offset case, not two mismatched gaps | [`tile-wall-design.md`](tile-wall-design.md) §10, [`decisions-log.md`](decisions-log.md) D-016 |
| `tile-wall` §10 Q3 — cropped-edge finish | **decided 2026-08-03, D-017: both finishes, but `frame` is orthogonal to `crop`** — not the `crop clip with frame` sketch. Unbuilt: the band width, which needs a D3 default declaration and is likely a calibration bet on W1 | [`tile-wall-design.md`](tile-wall-design.md) §10, [`decisions-log.md`](decisions-log.md) D-017 |
| `print-validation` §8 Q3 — F3 severity | **decided 2026-08-03, D-018: always warn**, overruling the doc's own leaning. Nothing to build — §4's table already read `warn`; the decision makes the doc agree with itself | [`print-validation-design.md`](print-validation-design.md) §8, [`decisions-log.md`](decisions-log.md) D-018 |
| `lego-lab` §11 Q8's grammar gap — the rhombic lattice row `gridFit` can score but no `.bkr` can produce | **resolved as a label**, [`decisions-log.md`](decisions-log.md) D-007; widening the grammar to a general two-vector basis remains an unbuilt option | [`lego-lab-design.md`](lego-lab-design.md) §11 Q8 |
| The `polygon`/`C.mpt` evaluator asymmetry MC-4 had to work around | a bikar issue; "not worked around here beyond this idiom" | [`calibration-design.md`](calibration-design.md) §4 |
| No polygon-offset primitive — MC-4's wall thickness co-varies with the angle under test | a bikar feature; "if a future version of bikar gains a polygon offset, this is the coupon to re-cut first" | [`calibration-design.md`](calibration-design.md) §5.4, §8 |
| No text emit — rung identity cannot be printed onto a part | a bikar feature; §8 calls it "the card's biggest structural weakness and the one a text-emit capability would fix outright" | [`calibration-design.md`](calibration-design.md) §3.2 |

The last three are worth reading together: all three are engine capabilities
whose absence shaped the coupons, and none of them blocks a print. They are the
list to consult if the first card comes back hard to read.

### 6.3 The research files' own residue — mostly not printer work

All 17 files in [`research/`](research) were swept for their enumerated residue.
Only three use a literal "what could not be grounded" heading; the seven
grounding audits enumerate theirs under **"Misgrounded or missing citations"**,
the two field surveys under **"Errata"**, and
[`hemisphere-split-grounding-audit.md`](research/hemisphere-split-grounding-audit.md)
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
  [`lego-lab-design.md`](lego-lab-design.md) §3.5 (rebuilt from measured
  repeatability, σ ≈ 0.02 mm) and to
  [`print-validation-design.md`](print-validation-design.md) Appendix A. It was
  never applied to [`tile-wall-design.md`](tile-wall-design.md), which is a
  different *lineage* — a different survey, a different audit — that happens to
  share the number. So this was not research debt awaiting a fetch; it was a
  correction that stopped at a document boundary and sat for five days inside a
  section headed "the load-bearing facts". Both tile-wall sites now carry the
  rebuilt argument, and
  [`research/tile-craft-field-survey.md`](research/tile-craft-field-survey.md)
  carries errata item 9 (its body stays verbatim, per the survey convention).

  **The check that would have caught it** is `docs_gate.py`'s new **D4**: a
  hand-entered list of withdrawn literals that may not be restated as fact
  outside `docs/research/`. Its limit is recorded rather than papered over — run
  against the pre-fix file it reports **one** finding, not two, because
  tile-wall §2 wrote the number as a *multiple* ("10–20× beyond FDM tolerance")
  and left no literal to match. See
  [`grounding-defect-taxonomy.md`](grounding-defect-taxonomy.md) §"Why D4
  exists".

  The four adjacent items were checked in the same pass and none is live: the
  "0.02 mm clutch band" is corrected in `lego-lab-design.md` §3.5, the
  "7–10% PETG design band" is withdrawn as apparently synthesized in
  [`w2-connector-design.md`](w2-connector-design.md) B.1 with the ~2% endpoint
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
  [`piece-composition-design.md`](piece-composition-design.md) Appendix A and
  [`w2-connector-design.md`](w2-connector-design.md) §3 and Appendix A.
  One of them
  ([`research/piece-composition-grounding-audit.md`](research/piece-composition-grounding-audit.md))
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
  is in [`print-validation-design.md`](print-validation-design.md) under the
  support-map step: θ from vertical, `d = h·tan θ`, with PrusaSlicer's `h/tan θ`
  from horizontal named beside it. This entry was wrong for six days.

One item there needs flagging as a *tooling* lesson rather than a finding:
[`research/derivation-visualization-survey.md`](research/derivation-visualization-survey.md)
records that a WebFetch against a GitHub **search** URL returned "Your search did
not match any code" for a feature that exists in four source files — a confirmed
false negative. Anyone re-running the ungrounded items above should not trust
that path.

---

## 7. What could not be determined, per item

Stated so the next reader does not mistake an unanswered question for a settled
one.

1. ~~**What W-F1 actually is.**~~ **Resolved 2026-08-02 —
   [`decisions-log.md`](decisions-log.md) D-008.** Three descriptions disagreed:
   [`catalog.md`](../.claude/skills/prototype/catalog.md) asked clipseat
   questions over a `Fit-Coupon.bkr` model line, that file being a five-bore ⌀
   ladder with no clipseat, no tile and no `gap` param;
   [`c2-assembly-design.md`](c2-assembly-design.md) §8 described the same file
   correctly as C2's step gauge; and
   [`w2-connector-design.md`](w2-connector-design.md) §8 named a **third**
   filename, `Fit-Step-Gauge.bkr`, which had never existed.
   Reading the geometry settled it: the catalog's prose was describing a coupon
   nobody had written. A bore-and-pin number does not transfer to a bayonet blade
   that drops then twists, so W-F1 is now
   `patterns/Coupons/Clipseat-Fit-Coupon.bkr` — a new five-rung blade-clearance
   ladder on its own plate. It is **not** subsumed by MC-1, and Plate 3 stays two
   prints in sequence.
2. ~~**Whether `Fit-Coupon.bkr`'s ladder is still the shipped ladder.**~~
   **Resolved 2026-08-02 — same entry.** It was not: it stepped
   −0.10 / 0 / +0.10 / +0.20 / +0.30 against a shipped `FIT_GAP_MM` of
   −0.10 / +0.05 / +0.15 / +0.35. **Re-cut, not retired** — it keeps the
   bore-and-pin role that MC-1 extends rather than replaces — and it now carries
   one `connect` per fit class, so the next edit to the constant stops the file
   evaluating instead of drifting silently. The root cause was that four of its
   five rungs were unasserted; `Machine-Card.bkr` had the same hole (one connect,
   four rungs) and was closed with it.
3. **Which machine is arriving.** The repo records a ten-entry menu, not a
   purchase. Every plate above is machine-independent in geometry but not in
   result, and the A1 mini's 180 mm envelope versus the 256 mm class changes how
   many coupons share a plate — and MC-3 at 160 mm long is the piece that would
   feel it first.
4. **Print time for anything.** No document in this repo states a print-time
   estimate for any coupon. The only time figures found anywhere are
   [`tile-wall-design.md`](tile-wall-design.md) §7.1's, and that section labels
   its whole table as estimates pending the W1 pilot.
5. **Mass or volume for the LG and W series.** The catalog states volumes for the
   P-series and [`calibration-design.md`](calibration-design.md) §7 states them
   for all 23 MC pieces. Neither states one for any LG or W coupon, and I did not
   compute any — a render would give a number, but it would be mine and not the
   repo's.
6. **Whether the whole machine card fits one plate.** §9 asks for one session
   "where the bed allows it" and does not resolve the conditional, because it was
   authored without knowing the machine.
7. **How many LG-F1 rungs are actually wanted.** §8 specifies a five-rung `ribMm`
   ladder crossed with three `engage` values, which reads as fifteen parts, but
   neither the catalog nor the design doc says whether all fifteen print or
   whether `engage` is sampled. I did not resolve it.
8. **Whether the W-series "on hold" is lifted by a printer arriving.**
   [`w2-connector-design.md`](w2-connector-design.md) §8 says only "printing is
   currently on hold, so both entries land as `planned`", and
   [`decisions-log.md`](decisions-log.md) D-003 gives the cause as a printer that
   is "owner-held and on hold". The stated cause is the absent machine, but the
   doc does not say the hold is *only* that, so I have not asserted it lifts
   automatically.
9. **Whether `hemisphere-split-design.md`'s bet table is current.** It states
   that `CAL_BET_IDS` "registers ten ids" and lists ten. The generated registry
   now reads fourteen — `CAL-CLP-01`, `CAL-STK-01` and the mural pair
   `CAL-REG-01`/`CAL-CLB-01` were added later. The doc is
   stale on a count rather than wrong on a conclusion, but I could not tell
   whether anything downstream in that doc depends on the ten.
10. **What LG-B2's `.bkr` should look like.** The catalog says the model does not
    exist and that "authoring it is the first step of this coupon, not a lookup",
    and points at `patterns/Rosettes/*.bkr` as the nearest source of the outline —
    but those are 2D patterns with no `brick` declaration. The authoring work is
    named, not specified — and, checked on 2026-08-02 at bikar `73514f1`, it is
    **blocked on a missing DSL surface**: the pattern-outline body is specified
    in [`lego-lab-design.md`](lego-lab-design.md) §5.2/§7.2 and the kernel
    honours `BrickSpec.bodyOutline` (tests exercise it), but no `BrickStmt` in
    the grammar reaches it — `evaluateBrickDecl` builds every DSL brick
    rectangular, and none of the seven shipped presets is pattern-outline.
    Authoring `Rosette-Brick.bkr` therefore means first extending the brick
    declaration (a reserved-word / corpus-sweep / decision-doc change in bikar),
    not writing a file against today's grammar. An auto rule that silently
    flipped existing `inscribe` bricks to pattern-outline would rebuild
    Star-Brick's body; the surface has to be explicit.
    **Resolved 2026-08-02**: the explicit surface shipped as `footprint outline`
    (bikar `bf6c602`, decision doc
    `bikar:docs/decisions/2026-08-02-pattern-outline-footprint.md`, designed in
    [`pattern-outline-brick-design.md`](pattern-outline-brick-design.md)), and
    `Rosette-Brick.bkr` was authored against it in the same commit.
11. ~~**Whether a `make coupons` target is wanted.**~~ **Resolved 2026-08-03**:
    yes, and the precedent question resolved itself. The repo's preference for
    a gate over new machinery
    ([`dsl-extension-skill-evaluation.md`](dsl-extension-skill-evaluation.md),
    [`issue-register-evaluation.md`](issue-register-evaluation.md)) does not
    transfer to a build target, as noted here — but what shipped is a gate that
    happens to have a target as its entry point, so the preference is satisfied
    rather than bypassed. See §4 item 2 and
    [`decisions-log.md`](decisions-log.md) D-014.

---

## 8. Reading this file against itself

Five checks, run before shipping it, in the spirit of
[`grounding-defect-taxonomy.md`](grounding-defect-taxonomy.md) K7.

- **The headline sequence and the register agree.** §2 puts the machine card
  first; §3.1 shows no MC coupon blocked on anything. §2 puts the LG ladder
  second; §3.2 shows LG-F1/F2/R1 blocked on nothing, with LG-D1, LG-B1, LG-B2,
  LG-P1 and LG-P2 correctly shown as gated on LG-F1. §2 puts W-F1 before W-C1; §3.3 shows the
  same order, and §7 item 1 — which used to record that the ordering itself was
  uncertain — now records it as settled two-plates-in-sequence (D-008).
- **P2 is not claimed to settle a bet.** §2 Plate 4 says so explicitly and §3.4's
  P2 row lists no `CAL-*` id — consistent with the registry, which gives P2 Q5's
  measurement to MC-6.
- **Counts reconcile.** 14 bets = 7 on the card + 6 on design coupons
  (`CAL-RIB-01`, `CAL-STK-01`, `CAL-DET-01`, `CAL-CLP-01`, and the mural pair
  `CAL-REG-01` on LG-P1, `CAL-CLB-01` on LG-P2) + 1 with no coupon
  (`CAL-STR-01`). 16 records = 12 on the card + 4 on design coupons — the mural
  bets have coupons but no bikar record yet, which is why the record count did
  not move with the bet count. 28
  print-gated items = 28 catalog entries — 24 coupons plus the four deliverables
  catalogued on 2026-08-03, which is why this line no longer reads
  "24 + 4 uncatalogued". The magnet-pocket item
  in §3.7 is deliberately **outside** that 28: no design doc demands it, so
  counting it would inflate the register with work nobody has asked for. §3.7
  says so in place rather than leaving the arithmetic to look wrong.
- **Every residue item names what would close it.** Added 2026-08-03, because
  this check did not exist and §6.3 failed it. Two of that section's three
  clusters were **already fixed when it was written** on 2026-08-02 — the
  piece-composition misattributions and the angle-convention line in `7fdb7e1`
  (2026-07-27, the same commit as the audit that asked for them), the w2 ones in
  `981d7bc` (2026-07-28) — and the section still listed them as
  outstanding, one of them as "it costs one line and it is not written yet."
  Nothing was wrong with the research; the summary of it had simply aged, and a
  summary of another document's open items is a **claim about that document's
  current state**, decaying the moment the item is fixed. So each residue entry
  now carries the anchor that would settle it — a doc, a section, the phrase to
  look for — which turns re-checking the list into a grep instead of a reread.
  The entries that stay open (§6.1's five LDraw items, §6.2's remaining table
  rows) each say what they are waiting on for the same reason. This sentence
  named the unsourced-number cluster until 2026-08-03, when that cluster closed
  — the decay is not hypothetical and it is not slow.
- **No hedge was hardened.** Where a source says "may", "expected to",
  "predicted", "estimates" or "not ruled out", this file carries the word.
  The three places that matter most: P5 is *expected to* fail or disappoint on
  FDM, not known to; LeoCAD's empty-model outcome is *predicted from a source
  reading*, not observed; and every MC rung range is a **bracket around an
  unknown, not a prediction**.
