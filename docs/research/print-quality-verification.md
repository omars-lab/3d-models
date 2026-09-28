---
date: 2026-09-26
produced-by: print-quality checker (Claude Opus 5.5)
feeds:
  - '[[print-quality-design]]'
checks: docs/research/print-quality-a.md, docs/research/print-quality-b.md
---

# Print quality: what the checker re-opened, and what it says

Two researchers (A, PR #344 and B, PR #345) wrote on the same question: why minis-04
showed "tiny holes", a peg border that is "too big" and pegs that are "too tight". This
file records what I re-opened myself and what each source actually says, so the
consolidated doc ([`../design/printing/print-quality-design.md`](../design/printing/print-quality-design.md)) rests on
checked text, not on either researcher's summary.

Nothing was printed or measured. The printer was not contacted. Everything below is
either a file on this machine, a page fetched on 2026-09-26, or my own arithmetic, and
each entry says which.

## 1. Local evidence

### 1.1 The slicer call

`resolvePresetList` in [`../../tools/bambu/src/commands/slice.ts`](../../tools/bambu/src/commands/slice.ts)
maps a preset name to the bundled leaf JSON and passes that path to `--load-settings`
unchanged. It does not read `inherits`. The compose command calls the same function.
The comment by `injectFilamentMapMode` confirms a second process file is refused with
"duplicate process config file", so a fix has to produce one merged file.

### 1.2 The sliced plates against the preset chain

I unzipped two sliced plates and compared `Metadata/project_settings.config` with the
chain flattened by hand (child keys win, arrays replaced whole):

- `.bambu/plates/minis-04.plate.3mf` (gitignored, the minis-04 slice);
- `build/plates/minis-03.plate.3mf`.

Chains, from the bundled Studio 02.08.02.61 profiles:

- process: `0.20mm Standard @BBL X2D` → `fdm_process_dual_0.20_nozzle_0.4` →
  `fdm_process_dual_common` → `fdm_process_common`;
- filament: `Bambu PLA Basic @BBL X2D 0.4 nozzle` → `Bambu PLA Basic @base` →
  `fdm_filament_pla` → `fdm_filament_common`.

The two plates gave the same result:

| Preset | Leaf keys match | Leaf keys differ | Parent keys match | Parent keys differ |
|---|---|---|---|---|
| process | 43 | 0 | 92 | 54 |
| filament | 25 | 4 | 55 | 50 |

`different_settings_to_system` is empty in both files, so Studio did not record these as
user edits. The parent keys that match are ones where the built-in value happens to
equal the chain's value.

The process keys that matter here (chain value → value in the slice):

| Key | Chain | Slice |
|---|---|---|
| wall_generator | classic | arachne |
| elefant_foot_compensation | 0.15 | 0 |
| top_shell_layers / top_shell_thickness | 5 / 1.0 | 4 / 0.6 |
| line_width / inner_wall_line_width | 0.42 / 0.45 | 0.4 / 0.4 |
| outer_wall_line_width | 0.42 | 0 (the default width) |
| initial_layer_line_width | 0.5 | 0.4 |
| top_surface_line_width | 0.42 | 0.4 |
| top_surface_pattern / bottom_surface_pattern | monotonicline / monotonic | zig-zag / zig-zag |
| monotonic_travel_into_wall | 45 | 0% |
| only_one_wall_top | 1 | absent |
| sparse infill | 15% grid | 20% cubic |
| enable_arc_fitting | 1 | 0 |
| resolution | 0.012 | 0.01 |
| skirt_loops / brim_width | 0 / 5 | 1 / 0 |

The filament keys that matter:

| Key | Chain | Slice |
|---|---|---|
| hot_plate_temp and textured plate temp | 55 | 45 |
| fan_min_speed | 100 | 20 |
| additional_cooling_fan_speed (aux fan) | 70 | 0 |
| fan_cooling_layer_time | 100 | 60 |
| slow_down_layer_time | 4 | 5 |
| overhang_fan_threshold | 50% | 95% |

Keys where chain and slice agree: filament flow ratio 0.98, seam_gap 15%, seam_position
aligned, filter_out_gap_fill 0, X-Y hole and contour compensation 0, wall_loops 2,
detect_thin_wall 0, infill_wall_overlap 15%, curr_bed_type Cool Plate, wall_sequence
inner then outer.

The G-code header in the minis-04 slice agrees: `wall_generator = arachne`,
`elefant_foot_compensation = 0`, `top_shell_layers = 4`, `top_surface_pattern = zig-zag`,
`initial_layer_line_width = 0.4`.

### 1.3 What the minis-04 G-code does, per piece

I split the G-code by the "start printing object, unique label id" markers and counted
features per layer.

- **No "Gap infill" anywhere on the plate.** Arachne varies line width instead. The
  pegs pieces' inner walls run from 0.37 to 0.67 mm wide.
- **The pegs pieces (ids 132 and 143, both `it-05d681da9948.stl`) have no sparse
  infill.** They are 13 layers, 0.2 to 2.6 mm. Top surface appears only at the 1.4 mm
  layer (the exposed top of the base) and at 2.6 mm.
- **The strap tops are mostly wall lines**, not top-surface infill.
- The minimal-frame pieces (ids 121, 154, 165) do have sparse infill, at 0.8 to 1.8 mm.
- The twist piece (id 176) is 20 layers.

So a hole cause that needs top-surface infill meeting a wall can only act on the
exposed base top and the frames, not on the straps. A cause that needs sparse infill
under a thin top can act on the minimal-frame pieces, not on the pegs pieces.

### 1.4 The dovetail as the kernel builds it

bikar `packages/core/src/kernel3d/coaster.ts`, function `slottedRing`, at bikar
origin/main 6356bb3:

```ts
const headMm = neckMm + depthMm;
// Tab (out) at L/4.
out.push(at(s1 - neckMm / 2, 0), at(s1 - headMm / 2, depthMm));
out.push(at(s1 + headMm / 2, depthMm), at(s1 + neckMm / 2, 0));
// Slot (in) at 3L/4 — the tab's image, widened by the clearance on every face.
out.push(at(s2 - neckMm / 2 - c, 0), at(s2 - headMm / 2 - c, -(depthMm + c)));
out.push(at(s2 + headMm / 2 + c, -(depthMm + c)), at(s2 + neckMm / 2 + c, 0));
```

Confirmed: the straight edges beside the joint have zero designed gap, and the tab
flank leans at atan(0.5) = 26.57° whatever the neck n and depth d.

**My own derivation, not from a source.** The slot is not a true outward offset of the
tab. Its corners are the tab's corners moved sideways by c, with the head also moved
down by c. So the slot flank runs d/2 across over d + c down, steeper than the tab
flank's d/2 over d. The gap between the two flanks therefore narrows from the neck to
the head:

- horizontal gap: c at the neck, c·(1 − d / (2(d + c))) ≈ 0.52c at the tab's head
  corner (for c small against d);
- perpendicular gap at the tab's head corner: about 0.46c.

At the minis-04 knobs (n = 3, d = 3, c = 0.10) the tightest point is **0.047 mm**. At
c = 0.15 it is 0.071 mm. Hand check at c = 0.10, placing the slot flank from (1.6, 0) to
(3.1, 3.1) and the tab head corner at (3, 3): the distance is 0.16 / 3.444 = 0.0465 mm.

A true per-face offset of the tab would put the slot neck half-width at
n/2 + 1.118c and the head half-width (at depth d + c) at h/2 + 1.618c. The kernel is
short by 0.118c at the neck and 0.618c at the head.

With e the per-face overgrowth of every printed outline, the play for pulling the
pieces apart comes to roughly `c(1 + 2c/d) − 6.6e`, about `1.07c − 6.6e` at d = 3.
Play reaches zero at e ≈ 0.016 mm for c = 0.10 and e ≈ 0.025 mm for c = 0.15. B wrote
`2c − 6.5e`: the overgrowth factor agrees, but B's clearance factor assumes the slot is
c wider along the whole flank, which the kernel does not build.

[`../coaster-interlock-design.md`](../coaster-interlock-design.md) says the slot is
"offset outward by the clearance `c` on every face" and that the probe only
"approximates that". The kernel builds the approximation, so the doc and the kernel
disagree about what `c` means at the head.

### 1.5 The plates, the print record and the clearance ladder

- [`../plates/minis-04.yaml`](../plates/minis-04.yaml): 80 mm pieces, base 1.4 mm,
  straps 1.2 mm proud (2.6 mm in all), pegs pair clearance 0.1, twist piece height 4.
  Its own risk notes say "7 layers; tabs may snap/flex; may be floppy".
- [`../prints/2026-09-26-minis-03/index.md`](../prints/2026-09-26-minis-03/index.md):
  "sent from Bambu Studio" (the desktop app); clearance 0.15 was "a bit loose (hand
  feel, not measured)". The minis-03 base was 4 mm, so its first layer was 1 of 20. B's
  "1/20" is right; A's "about 1 of 26" divides by total height, not the joint's height.
- [`../../.claude/skills/calibrate/bets.md`](../../.claude/skills/calibrate/bets.md),
  CAL-FIT-01: press −0.1, snug 0.05, sliding 0.15, free 0.35, basis "Literature-shaped
  FDM clearance ladder ... no pin and socket have been printed".
- [`../design/pieces/c2-assembly-design.md`](../design/pieces/c2-assembly-design.md) §5 calls these "**Intent gaps**
  (diametral)", and Appendix B.3 says it "transcribes Creative3DP's calibrated-printer
  press-fit ladder verbatim, including its instruction to keep fit gap and printer
  compensation separate".
- [`../coaster-interlock-design.md`](../coaster-interlock-design.md) sets the coaster
  clearance default to 0.15 from CAL-FIT-01's sliding step. Its transfer sentence does
  not mention the step from diametral to per-face, nor that the ladder assumes printer
  compensation is applied separately. So A's point that this port is missing a K10
  condition holds.

## 2. Web sources re-opened

The wiki pages, Creative3DP, Prusa, Hubs and Formlabs were fetched with a
browser user agent and stripped to text. The GitHub issues were read with `gh`. The
Bambu forum threads come back as a script shell to a plain fetch, so I read them
through their `/t/<id>.json` endpoint.

| Source | What it says (checked) | Bears on |
|---|---|---|
| [BambuStudio #6836](https://github.com/bambulab/BambuStudio/issues/6836) | Open, label bug. Collaborator lanewei120: "CLI has limited logic to process the jsons, we suppose the full json has been generated before when passed to CLI". Gives a Python flatten using a shallow merge (child wins, lists replaced whole). No plan to add inheritance to the CLI. A commenter shows the CLI also clamps machine limits. | B's preset-chain claim: **verified** |
| [BambuStudio #9768](https://github.com/bambulab/BambuStudio/issues/9768) | Open, filed on an H2C with Studio 2.5.0.66. "The temporary solution is to use monotonic lines and overlaps"; staff say mitigation is coming and that the travel-into-wall feature "is designed to improve pinholes"; a user says the overlap setting "doesn't apply to the standard top infill pattern Monotonic Line"; an X2D owner saw gaps "more often like those described in this issue", "better, but not perfect" after a factory reset. | A's cause 1 is real, but minis-04 printed zig-zag with travel-into-wall 0 (§1.2), not the setup A describes |
| [BambuStudio #8784](https://github.com/bambulab/BambuStudio/issues/8784) | Open, H2S, Studio 02.03.01.51, pinholes in the preview; workaround re-slices with 0 walls and back. | B's cause 7, as B says |
| [Wall generator](https://wiki.bambulab.com/en/software/bambu-studio/wall-generator) | Classic: "If the polygon is too small, the result of the shrinkage will be empty, so the wall path will not be generated", and "only one seam per layer". Arachne "will generate discontinuous wall paths" that "can affect the print surface quality"; "the increase of wedges may cause over-extrusion". | The page says surface quality, not holes; both researchers extend it |
| [Seam](https://wiki.bambulab.com/en/software/bambu-studio/Seam) | Nearest priority: "concave non-overhang vertex > convex ..."; seam gap default 15%; the seam is "unavoidable in FDM". | Both, as written |
| [Elephant foot](https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot) | "usually layer 1, and sometimes the first few layers"; on "assemblies, snaps, rails, and shaft holes, the flared base directly affects fit ... may fail completely"; "For general models ... the system default is fine"; worked example (0.09 + 0.11)/2 = 0.10; "can vary between different types of build plates". | Both |
| [X-Y hole and contour compensation](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation) | Hole compensation acts on "closed, hollow areas", "only applies to closed paths" and "does not change the outer size"; contour compensation moves the outer contour; values are "specific to each filament"; a hole's diameter changes by twice the value; checklist includes elephant foot, moist filament and "Seam, this feature can affect hole precision". **No PLA 0.05 figure on the page.** | A slot open to the edge is contour: both right. "PLA 0.05" stays snippet-only |
| [Troubleshooting](https://wiki.bambulab.com/en/knowledge-sharing/troubleshooting-printing-issues) | A "general article" for "most Bambu Lab 3D printers". Flow 0.98 is "considered normal for PLA filament with X1C", raise toward 1.00. "Lines not connected to walls" from a K-factor too high; K usually 0.02–0.04. Minimum layer time is "commonly a problem when printing very small objects". "PLA benefits the most from a higher Auxiliary part cooling fan speed ... mostly applies on small objects". | Flow cause; and the aux fan the fallback set to 0 |
| [Creative3DP press-fit](https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/) | Diametral ladder: press −0.1, snug +0.05, close running +0.15, free +0.35. "Keep them separate" (fit and compensation). Holes 0.1–0.3 undersize, shafts about 0.1 oversize. Boxes "+0.15mm per mating pair". 0.5 mm × 45° chamfer. Folk numbers elsewhere are "fit-plus-compensation, pre-mixed". | A's §2.2 cause 1, see §3 |
| [Prusa, modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) | "An initial good measurement for movable parts is at least 0.3 mm"; "Using a chamfer on the edges of two parts that slot together can save you a lot of effort". Does not say per side or total. | A, as written |
| [Hubs, interlocking joints](https://www.hubs.com/knowledge-base/how-design-interlocking-joints-fastening-3d-printed-parts/) | Table row for FDM: 0.5 mm. "Adding a small radius to part edges assists joint assembly". | A and B, as written |
| [Formlabs, interlocking joints](https://formlabs.com/blog/how-to-3d-print-interlocking-joints/) | FDM row 0.5 mm; the 0.2 / 0.4 mm advice is for its SLA and SLS printers. | B, as written; the 0.2 / 0.4 figures do not transfer to FDM |
| [Forum 5489](https://forum.bambulab.com/t/top-surface-has-tiny-holes-and-gaps/5489) | "does the slicer have a problem with very pointy corners. It actually leaves gaps"; reply: "Long, narrow pointy areas are the worst case ... Often you can already see these problematic areas in the slicer preview." | B's cause 1, as written |
| [Forum 68800](https://forum.bambulab.com/t/gap-between-infill-and-inner-wall/68800) | "I ended up using .012 which eliminated almost all gaps ... K-factor was previously set to 0.025." | A, as written |
| [Forum 256619](https://forum.bambulab.com/t/holes-when-printing-seam-patterns/256619) | "Ironing. Turn it on and the holes appear; turn it off and they're gone." | B; ironing was off on minis-04 |
| [Forum 87473](https://forum.bambulab.com/t/how-to-join-large-flat-parts-at-the-edge/87473) | Dovetails "quite tight (about 0.04mm gap) with rounded corners". | B, as written |
| [Forum 123711](https://forum.bambulab.com/t/how-do-you-use-tolerance-value-in-your-design-with-bl/123711) | "0.1 and 0.15 is more than enough", from a poster who also says he adds "the tolerance to both parts" (so per side or total is unclear); another goes "between 0.15 to 0.20" and says it "depends a great deal on the filament"; a linked test notes "With the 0.4mm Nozzle the Slicer does not consider the 0.05mm gap". | A listed this as a snippet; now fetched. The 0.05 remark is about print-in-place parts sliced together, so it does not carry directly to two separately sliced coasters |
| [Forum 15122](https://forum.bambulab.com/t/micro-gaps-in-outer-skin/15122) | The poster: "Never was able to fix it. In the areas it was bad, I had the printer print the outer lines last, which dramatically reduced the occurrence." | **B inverts this** ("not last") and drops "never was able to fix it". Minis-04 already prints the outer wall last |

Not re-opened: the flow-rate and pressure-advance calibration wiki pages, the first-layer
guide, the Bambu PLA page, the Bambu ironing page, and the forum thread on H2 top-layer
gaps. For these I rely on the researchers' fetched notes; none of them carries a
load-bearing number in the consolidated doc.

## 3. Findings against the two write-ups

1. **B's preset-chain claim is right, and wider than B lists.** Beyond B's six keys,
   the fallback also printed a zig-zag top, travel-into-wall 0, a minimum fan of 20
   instead of 100, the aux fan at 0 instead of 70, 20% cubic infill, no arc fitting and
   an added skirt.
2. **A's §0 describes the preset, not the slice.** Classic walls, a monotonic-line top,
   travel-into-wall 45 and elephant-foot compensation 0.15 are what the chain says, not
   what printed. A's hole cause 1 (as a cause for this print), cause 2 (a strip classic
   walls leave empty) and the reason A ranks elephant foot low all rest on that.
3. **A misplaces 0.10 per face on the Creative3DP ladder.** 0.10 per face is 0.20
   across, which sits between close running (0.15) and free (0.35), not between snug
   and close running. And "below every published starting point read here" is not
   true of Creative3DP's snug or close-running steps, nor of the Hydra 0.1 per side
   that c2-assembly cites. It is true only against the pre-mixed folk numbers (Prusa
   0.3, Hubs 0.5), which include compensation.
4. **B's play formula overstates the clearance.** See §1.4: the kernel's slot is
   narrower than a true offset, so the tightest gap at c = 0.10 is about 0.047 mm, not
   0.10.
5. **B's seam corners.** B puts seam bumps at "the slot mouth and neck corners". By my
   reading of the outline, the slot's mouth corners are convex (about 63° of
   material) and the concave corners are the two at the bottom of the slot and the
   two at the root of the tab. A says "the slot's inner corners", which fits. Either
   way both concave pairs bear on the fit.
6. **First-layer share.** B's 1/7 and 1/20 are right; A's "1 of 26" is not.
7. **Which slice printed is still open.** minis-03 was sent from the desktop app. Whether
   the app re-slices a project 3MF with its full presets at send time was not
   checked. My untested guess is that it keeps the settings embedded in the file,
   which would mean the fallback settings printed. Omar can read this in the app
   without touching the printer.
