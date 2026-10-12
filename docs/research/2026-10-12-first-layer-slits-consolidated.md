---
date: 2026-10-12
produced-by: Claude Opus 5.5, the checker agent consolidating passes A and B. Both passes were read in full. Every load-bearing claim was checked by re-opening its source (Bambu Studio's code at tag v02.08.02.61, four Bambu wiki pages, one GitHub issue, six forum threads). Nothing was printed or sliced for this file.
feeds:
  - the first slice plate for the bottom slits (not yet written)
  - docs/issues/bed-face-preset-failed-in-print.md
---

# First-layer slits on the X2D: the two research passes, checked and merged

The question: which X2D first-layer settings might close the slits on the bottom face of the
coasters (0.4 mm nozzle, PLA)? It also asks which settings can be set for one piece and which
only for the whole plate, and which test plate should come first. With the stock diagonal
pattern, the slits are lines that stop short of the strap walls. With rings, they are dashes where
rings meet. The history so far is in
[the bed-face issue](../issues/bed-face-preset-failed-in-print.md). Rings are dropped. The gold
textured plate gave fewer slits, but its grain rules it out for coasters. The 30% overlap closed
the strap edges once, but only together with rings.

The two passes this file checks are open pull requests, and their files are not on master yet:

- Pass A: [PR #713](https://github.com/omars-lab/3d-models/pull/713), files
  2026-10-12-first-layer-slits-a.md and 2026-10-12-first-layer-slits-a-recommendation.md.
- Pass B: [PR #712](https://github.com/omars-lab/3d-models/pull/712), files
  2026-10-12-first-layer-slits-b.md and 2026-10-12-first-layer-slits-b-recommendation.md.

This file is the one to act on. The two pass files stay as the record it was built from.

## 1. What I re-opened, and what it said

Each row is a claim that changes what gets printed. "Confirmed" means I opened the source and it
says this. "Contradicted" means I opened it and it says something else. "Flagged" means I could
not open it, or it rests on a search snippet.

| Claim | Who made it | Source I re-opened | Verdict |
|---|---|---|---|
| "Monotonic line travel extend" only works with the `monotonicline` pattern, so it does nothing on the stock `monotonic` bottom | A and B | Code: [Fill.cpp L241](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Fill/Fill.cpp#L241) reads it only when the pattern is monotonic line. Wiki: [strength settings](https://wiki.bambulab.com/en/software/bambu-studio/parameter/strength-advance-settings): "only works if your Top surface pattern or Bottom surface pattern is set to Monotonic Line" | Confirmed |
| The X2D profile already sets it to 45% | A and B | Profile `fdm_process_dual_common.json` at the tag: `"monotonic_travel_into_wall": "45.0"` | Confirmed |
| Its unit is a percent of the line width | B (code) | Code tooltip: "(percent to line width)", range 0 to 200. The wiki says "% of the inner wall thickness" | Confirmed from the code. The wiki words it differently, which is minor |
| The travel extend pushes the end of the line toward the wall | B | [ExtrusionEntity.hpp L671-710](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/ExtrusionEntity.hpp#L671-L710): the extra stretch is a path built with `no_extrusion = true`. The nozzle travels on toward the wall and back, but lays no plastic. Diatom-Bambu calls it a "non-extrude travel" on [issue 9768](https://github.com/bambulab/BambuStudio/issues/9768) | Contradicted as worded. The nozzle moves toward the wall, but the line of plastic does not get longer |
| The infill/wall overlap does nothing on the `monotonicline` pattern, so do not use the two together | A (from ingoingo on issue 9768) | [FillRectilinear.cpp L3239-3290](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Fill/FillRectilinear.cpp#L3239-L3290): the monotonic-line fill uses `no_overlap_expolygons`, the area *before* the overlap is added ([PerimeterGenerator.cpp L1400](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PerimeterGenerator.cpp#L1400)) | Confirmed by my reading of the code. B's piece C, which stacks them, would test nothing more than the pattern alone |
| Gap fill skips the voids beside the travel-extend hops, because the hops count as covered | B (from esolution00-cyber on issue 9768, 2026-09-29) | [ExtrusionEntity.cpp L60-68](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/ExtrusionEntity.cpp#L60-L68): `polygons_covered_by_spacing` does not check whether a path extrudes. FillRectilinear.cpp then fills only the area not covered | Confirmed by my reading of the code at the tag. Not tested in a slice or a print |
| First-layer flow (`initial_layer_flow_ratio`) and print flow (`print_flow_ratio`) are per-piece settings in the code | A and B | [PrintConfig.hpp L1165 and L1169](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.hpp#L1165) put both in the per-piece group. [GCode.cpp L7192](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L7192) multiplies by both. [GCode.cpp L6470](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/GCode.cpp#L6470) loads each piece's values before writing it | Confirmed in the code. Both are hidden unless the slicer is in Develop mode. No slice here has shown it yet |
| A per-piece first-layer flow can be lost: someone set 1.05 on a piece, and it went back to 1.00 when the project was synced to a different printer | Neither pass | [Forum 256312](https://forum.bambulab.com/t/first-top-layer-gaps-on-h2-series-confirmed-bug-still-unresolved/256312), post #32 (Chi_print, 2026-08-11) | New, and confirmed. A risk for the per-piece check below |
| Line width, first-layer height, first-layer speeds, nozzle temperature, filament flow, pressure advance and the Z offset are whole-plate only | A and B | PrintConfig.hpp L1474-1479 (the whole-plate group). `z_offset` is commented out (L1540). Our own slice found the same for the first-layer line width ([bed-face per piece, §1](2026-10-10-bed-face-per-piece-and-bedface-1.md#1-which-of-the-three-settings-bambu-takes-per-piece)) | Confirmed |
| X2D profile first-layer speeds: 50 mm/s, and 105 mm/s for infill | A and B | `0.20mm Standard @BBL X2D.json` at the tag | Confirmed |
| Bambu's wiki says to slow the first layer to 30 mm/s (outer wall) and 60 mm/s (infill) | A | [First-layer test print page](https://wiki.bambulab.com/en/knowledge-sharing/identify-and-fix-first-layer-issues-with-a-test-print), section 5 | Confirmed. The page gives it as advice for adhesion, not for gaps |
| Bambu support told an H2 user 20 mm/s first layer and 30 mm/s first-layer infill, plus 1.05 first-layer flow, and it was "still noticeably poorer" | B | Forum 256312 | Confirmed |
| Raising first-layer flow does not close these gaps | B (three threads) | Forum 256312: 1.05 and 1.10 "no better" (H2). [Forum 35462](https://forum.bambulab.com/t/optimize-a-almost-perfect-first-layer/35462): gaps stay up to 1.25 (X1C, Orca Slicer). [Forum 248800](https://forum.bambulab.com/t/first-layer-is-not-squished-enough-visible-gaps-h2s/248800): only at "obvious over-extrusion" (H2S) | Confirmed for those three printers. None is an X2D |
| X2D users found a lower first layer helped: −0.014 mm and −0.02 mm | A and B | [Forum 251550](https://forum.bambulab.com/t/x2d-pla-print-flow-rate-isnt-isnt-fine-or-some-other-issue/251550): "I lower it by 0,014" and "-.02 helped some". [Thread 253016, post 97](https://forum.bambulab.com/t/x2d-print-quality-issues/253016/97): the printer menu has a manual first-layer offset of ±0.05 mm. Set to −0.02 with fresh bed calibration, it gave a "perfect first layer" | Confirmed. The post 97 writer doubts the −0.02 did it and suspects the fresh calibration |
| Thread 257448 mentions the manual first-layer offset | B | [Forum 257448](https://forum.bambulab.com/t/underextrusion-on-the-top-layer-bambu-lab-x2d-warranty/257448) only links to post 97 above | Second-hand. The claim stands on post 97 |
| −0.02 mm is not enough on a textured plate; −0.04 mm is the least, −0.05 mm better | B | Issue 9768, abarylak, 2026-09-23 (H2C, textured plate) | Confirmed. Not an X2D, and not a smooth plate |
| None of the sources shows the bug on an X2D | B | Forum 256312, post #64: "very similar behavior on my X2D". Post 97 is also an X2D | Contradicted |
| Issue 9768's last activity was October 10 | B | GitHub reports the issue updated 2026-09-29 | Contradicted. Minor |
| Pressure advance (K) set too high leaves lines not joined to the walls | A (marked as its own inference) | [Wiki troubleshooting page](https://wiki.bambulab.com/en/knowledge-sharing/troubleshooting-printing-issues), "Lines not connected to walls": cause "K-factor set too high", normal K 0.02 to 0.04 | Confirmed that the section exists. But its body says the lines "don't connect with each other", and the cause it names is a typo ten times too high (0.25 for 0.025). Tying it to an auto K that runs a little high is a stretch, as A said |
| Automatic Flow Dynamics on this printer family can set K higher, with about 10% jitter; lag can leave "gaps or thin lines" | A and B | [Flow Dynamics wiki page](https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa), the "H2D/H2S/P2S/X2D Printer" section | Confirmed. The quotes name the H2D; the section heading includes the X2D. Modes are Automatic, Open and Off, and a manual K only counts when it is Off |
| 0.98 flow is normal; 1.00 should close gaps | A fetched it; B had it from a page that now returns "not found" | Wiki troubleshooting page, "Even gaps in the top layer" | Confirmed. It is about top layers on the X1C |
| Flow set too low leaves gaps between lines | A | [Flow rate wiki page](https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate) | Confirmed. General advice, not first-layer specific |
| A wider first line makes the gaps larger, and 0.3 mm makes them smaller but not zero | B | Forum 35462 (X1C) | Confirmed. Moot for a per-piece plate, since line width is whole-plate and the 2026-10-10 slice found the first-line width is not taken per piece |
| Taking the travel extend to 200% smeared and did not close the gaps | A | Issue 9768, krwc | Confirmed |
| Changing temperature did not help | A | Forum 248800 (H2S): "Tried different bed and hotend temperatures" in a list of things that did not fix it. What fixed it for that user was hot-bed leveling plus automatic calibration before each print | Confirmed |

Not re-opened here, because nothing below rests on them: Simplify3D's "gaps between infill and
outline" page and Ellis' first-layer squish guide (both passes fetched both), and Bambu's
CalibUtils.cpp (A). These rest on search snippets only and are flagged, not used for any step below:
the two Prusa forum threads, goodprints3d, siddament, the MakerWorld model, the BIQU plate page, the
PLA data sheet on additive-x, Flashforge's melting-point post, and the X2D press pages (All3DP,
3D Printing Industry, 3DJake). The wiki's "top layer inconsistencies" page that B cited now returns
"not found".

## 2. Where the passes agree, disagree, or stand alone

### They agree

- Travel extend is set to 45% in the profile and does nothing on the stock `monotonic` bottom.
- First-layer flow and print flow are per-piece settings in the code, but no slice has shown it yet.
- The overlap and the bottom pattern are the only two settings proven per piece in our own slices.
- Line width, first-layer height, speeds, temperature, filament flow, pressure advance and Z apply
  to the whole plate.
- X2D users report that lowering the first layer by 0.014 mm to 0.02 mm helped.
- Temperature is the weakest lead.
- Elephant-foot compensation shrinks the bottom edge and puts the fits at risk, so leave it alone.
- The slicer's plan cannot rank prints. Our own bedface-1 and bedface-2 showed this.

### They disagree

| Point | Pass A | Pass B | Which side the sources support |
|---|---|---|---|
| First whole-plate print | Pressure advance first: Flow Dynamics Off, with a hand-set K | A lower first layer (−0.02 mm) first, then Flow Dynamics On | **B.** Lowering Z has two X2D users, post 97, and our own gold-plate result (fewer slits with 0.02 mm lower). The K case rests on a wiki section about a typo and users' guesses |
| Overlap stacked on `monotonicline` | Do not stack | Piece C stacks them | **A.** The code fills the monotonic-line area without the overlap, so the stack tests only the pattern |
| Travel extend at 100% | Not proposed; cites 200% smearing | Proposed as a piece | **Open.** 100% is inside the 0-200 range. No print has tried it. The hops add no plastic, so expect little |
| Flow Dynamics mode | Off, with a hand-set K | On (automatic) | **Open.** The wiki says the automatic K can run high and jitters by about 10%. Neither side has a print. It goes late in the order |

### Only pass A found

- The wiki's "Lines not connected to walls" section, which names a K that is too high (see the
  hedge in §1).
- The wiki's advice to slow the first layer to 30 and 60 mm/s (given there for adhesion).
- Bambu's own calibration code varies `print_flow_ratio` per piece. I did not re-open this; it fits
  the per-piece group the code puts it in.
- The two nozzles may differ, so a result on one nozzle may not carry to the other.

### Only pass B found

- The wiki strength page's own words on travel extend.
- The theory that gap fill skips voids beside the hops. I confirmed it in the code at the tag; it
  is untested.
- The roughly 10% jitter in automatic Flow Dynamics.
- Forum 35462 (X1C): gaps survive 1.25 flow, and wider lines make them worse.
- abarylak's −0.04 to −0.05 mm on a textured plate (H2C).
- Piece F (rings plus more flow). This is moot now that rings are dropped.
- The table of the start code's Z trims. It matches
  [the plates research](2026-10-07-third-party-plates-b.md).

### Found only by this check

- The overlap is ignored on `monotonicline` (from the code, §1).
- The travel extend adds no plastic (from the code, §1). This is why B's "pushed toward the wall"
  overstates it.
- A per-piece first-layer flow was reset to 1.00 when a project was synced to another printer (forum 256312, post #32).
- An X2D user in forum 256312 (post #64) reports the same gaps, so this is not only an H2 problem.

## 3. The plan, ranked

The rules come from [experiments.md](../../.claude/skills/print-model/experiments.md).
Each piece is a pie slice holding one repeat of the coaster: straps, a star hole and the rim. Every
setting gets two pieces, because slits come and go from spot to spot. Every piece carries its carved
id. A stock pair sits on the same bed. Compare the same spot on each piece with
`python3 tools/print_review.py compare`, stock first.

Two settings are proven per piece by our own slices: `bottom_surface_pattern` and
`infill_wall_overlap` ([bed-face per piece, §1](2026-10-10-bed-face-per-piece-and-bedface-1.md#1-which-of-the-three-settings-bambu-takes-per-piece)).
The compose tool ([compose.ts](../../tools/bambu/src/commands/compose.ts)) accepts only those two,
and refuses any other key until a slice shows Studio honors it.

### Plate 1: per-piece settings, one bed, on the glacier plate

All pieces are sliced on the stock X2D 0.20 mm Standard profile, sliced as the glacier plate, in one
color. Listed best bet first. If the bed runs short of room, cut from the bottom.

1. **Stock, two pieces.** The control.
2. **Overlap 30% on the stock `monotonic` pattern.** Proven per piece. This is the top bet. The
   strap edges closed on `R` in bedface-2, but `R` also had rings, so the overlap has never been
   printed on its own. It may also move a loose piece's fit, so fits get checked again before it
   goes near one.
   *This carries over to the whole coaster because the overlap acts at each spot where a fill line
   meets a wall, and the slice holds the same straps, star hole and rim at the same line width and
   speed as the full coaster.*
3. **Overlap 55% on the stock `monotonic` pattern.** Proven per piece. ingoingo saw the holes
   "almost disappear" at 55% (H2C, top surface, issue 9768). More overlap risks a ridge where the
   infill crowds the wall, and the same fit check applies.
   *This carries over to the whole coaster for the same reason as the 30% pieces: it acts where each
   line meets a wall, and the slice has every kind of wall the coaster has.*
4. **First-layer flow 1.05, then 1.10 (two pairs).** **Not proven per piece**, and compose refuses
   the key today. The code says it is a per-piece setting. Before printing, add the key to compose
   only after a check on the file compose actually sends (the second slice, with the prime tower
   off):
   - the piece's own settings in the sliced 3mf show 1.05 (or 1.10), and the stock piece shows none;
   - in the G-code, the first-layer extrusion amounts for that piece are about 5% (or 10%) above the
     stock piece's for the same line length.

   If either check fails, the piece comes off the plate, and first-layer flow needs a plate of its
   own. Expect little: three threads on other printers saw no fix from more flow (§1). And syncing a
   project to another printer once reset this exact per-piece value to 1.00 (forum 256312, post
   #32), so the check must read the file that is sent, not the project on screen. If the PLA
   profile's own flow is below 1.00 (the post 97 X2D user ran 0.98), these pieces also cover the
   wiki's "use 1.00" advice, so it does not get a bed of its own.
   *This carries over to the whole coaster because the flow change applies to every first-layer
   line of the piece alike, and the slice's lines are the same width, speed and length range as the
   full coaster's.*
5. **The `monotonicline` pattern, with the profile's 45% travel extend.** The pattern key is proven
   per piece, but only with `concentric`. Compose already allows `monotonicline`, but no slice or
   print has tried it. Expect little. The travel extend adds no plastic. My reading of the code at
   the tag is that gap fill then skips the void beside each hop, which could leave the strap-end
   slits as they are or make them worse (untested). Do not add the overlap to these pieces: the code
   ignores it on this pattern.
   *This carries over to the whole coaster because the pattern and the hop happen at each line end
   that meets a wall, and the slice has the same strap ends as the coaster.*

Left off plate 1 on purpose: travel extend at 100%. The key is not proven per piece, and krwc saw
200% smear. It earns a place only if piece 5 comes out better than stock.

### Then the whole-plate prints, in order

Each of these changes the whole bed, so it gets a bed of its own, still in pieces (rule 4). A stock
control cannot sit beside them at the stock setting. The control is plate 1's stock pair: the same
slice, the same spot, compared photo to photo. If plate 1 finds a winner, every piece on these beds
uses that winner, and two pieces stay at plain stock to show what the whole-plate change adds.

1. **A lower first layer on the glacier plate: −0.02 mm first, then −0.04 mm if slits remain.**
   This has the strongest support. Our gold-plate print had fewer slits at 0.02 mm lower. Two X2D
   users report −0.014 mm and −0.02 mm helping. The hedges: the post 97 writer doubts the −0.02 was
   the cause. abarylak found −0.02 not enough on a textured plate (H2C). And the gold plate changed
   the surface as well as the height. There are two ways to do it:
   - Slice the glacier plate as Textured PEI. The start code then lowers it 0.02 mm. This is
     written in the sliced file, but today the send refuses it ([the issue](../issues/sliced-for-wrong-plate.md)),
     so it needs a tool change with its own check. It cannot reach −0.04.
   - Use the printer menu's manual first-layer offset (±0.05 mm). This is Omar's to set at the
     printer. Nothing in the plate recipe or the sliced file shows it, so the plate page must
     record the offset used, or later prints cannot be compared.

   Bambu chose the higher start for smooth plates on purpose. More squash may widen the bottom
   edge, so fits for loose pieces get checked again.
   *This carries over to the whole coaster because the nozzle height is the same at every point on
   the bed, so every first-layer line of the coaster gets the same squash as the pieces.*
2. **A slower first layer: 30 mm/s outer wall, 60 mm/s infill** (profile: 50 and 105). The wiki
   gives this for adhesion, not gaps. Simplify3D suggests slowing down for gaps between infill and
   outline. But Bambu support's 20 and 30 mm/s, with more flow, left an H2 user "still noticeably
   poorer".
   *This carries over to the whole coaster because first-layer speed is set for the whole plate,
   and the pieces' lines are as long as the coaster's, so they reach the same speed.*
3. **Pressure advance: Flow Dynamics Off with a hand-set K, against Automatic.** The passes split
   on this, and neither has a print behind it. The wiki's support is a typo case and an automatic K
   that may run high. Run it only if steps 1 and 2 leave slits.
   *This carries over to the whole coaster because K shapes the start and end of every line on the
   bed, and the pieces' lines start and stop at the same walls.*
4. **First-layer nozzle at 225 °C.** The weakest lead. One H2S user tried temperatures with no fix,
   and both passes rank it last. Run it only if everything above leaves slits.
   *This carries over to the whole coaster because the nozzle temperature is the same for every
   line on the bed.*

## 4. What this file assumes, not decides

- One pie slice of the coaster stands for the whole coaster's bottom. Rule 1 of experiments.md
  says so, and every sentence above leans on it.
- The second compose slice (prime tower off) is the file that gets sent. That is how
  [the 2026-10-10 slices](2026-10-10-bed-face-per-piece-and-bedface-1.md#1-which-of-the-three-settings-bambu-takes-per-piece)
  read it.
- Folding the filament flow 1.00 advice into the first-layer flow pieces assumes the PLA profile's
  flow is below 1.00. Read the profile before building plate 1.
- My readings of the code (no overlap on `monotonicline`, hops counted as covered) are from
  v02.08.02.61. The installed Studio may be a different version.
