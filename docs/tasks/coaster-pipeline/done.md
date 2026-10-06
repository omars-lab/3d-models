# Done — first print and calibration

Newest first: date, what shipped, PR. Backlog: [`backlog.md`](backlog.md).

- 2026-10-06 — The gBV split coasters pass the mesh gate at every size from 80 to 125 mm: a half's caps mend the zero-area triangles laid over vertices in a line, which failed 100 mm on both files, 115 on the lip and 109 on the flange (bikar #322)
- 2026-10-06 — A whole-file `render --check` of a split coaster gates each half and each piece color on its own instead of failing the closed view on the linkage gate, and the coaster mesh-hash test no longer fails on a comment edit (bikar #321); `make coasters` no longer skips split coasters (3d-models #SELF)
- 2026-10-06 — Way c, the pocket: `hold pocket` on a split coaster prints each piece half in place in its half, in a closed pocket with a neck at the face and at the cut, and the `Split-Pocket-Coupon` tries it at one and two layers of air (bikar #320); its plate [pkt-1](../../design/plates/pkt-1.md) with two pairs per rung, sliced and pictured up to the owner gate (34 minutes, 11.6 g); the print waits on Omar in the backlog (3d-models #590)
- 2026-10-06 — SPL-1, the split coupon: a `floor` knob and a press-fit gap on split studs, and two coupons in bikar, a stud fit tile and a trapped-piece tile (bikar #319); its plate [spl-1](../../design/plates/spl-1.md) with twelve fit pairs and two trap pairs, sliced and pictured up to the owner gate (43 minutes, 18.3 g); the bed picture's new `--zoom` puts each label on its own tile; the print waits on Omar in the backlog (3d-models #587)
- 2026-10-06 — the split recipe shows studs and its Watch out no longer says a loose line is needed (3d-models #587)
- 2026-10-05 — The dovetail join for split piece halves (D-107, Omar: "for joints i want to try the dovetail"): a `dovetail rail` / `dovetail slot` line on a bikar piece that refuses a dovetail that would not lock, the SLD-1 coupon (a rail half and a slot half of a hexagon piece, bikar #309), and its plate [sld-1](../../design/plates/sld-1.md) at gaps 0.10, 0.15 and 0.20 mm, sliced and pictured up to the owner gate (12 minutes, 2.4 g); the print waits on Omar in the backlog (3d-models #577)
- 2026-10-05 — The first themes' plates (D-106): 14 plates, one per color, for Midnight blue, Night sky, Terracotta souk and Iznik tile, each sliced with its color's own line preset and pictured, on the [theme plates page](../../design/coaster/themes/gbv-theme-plates.md) with a buy list of 11 colors priced from the store catalog ($193.89 for one of each); the color-themes skill's `theme_plates.py` makes them and never rewrites a page that has a yes, a hold or a print; black and white plates now get a grey backdrop so their bed pictures are not blank; the prints wait on Omar in the backlog (3d-models #575)
- 2026-10-05 — The swatch card (D-105): a chip engraved with the spool's code, made from one bikar file for every color (`text $code`, bikar #307), and a plate per color on the printer, [swatch-10204](../../design/plates/swatch-10204.md), [swatch-13903](../../design/plates/swatch-13903.md), [swatch-10101](../../design/plates/swatch-10101.md) and [swatch-10501](../../design/plates/swatch-10501.md), each sliced with its own line's preset; a bought color gets its swatch with `swatch.py recipe <code>`; the prints wait on Omar in the backlog (3d-models #574)
- 2026-10-05 — The split coaster's two holds, at Omar's ask on call 6 (D-100): the lip (A) and the flange (C) as two Coaster Lab entries on gBV (bikar #305), each on its own plate, [split-01](../../design/plates/split-01.md) and [split-02](../../design/plates/split-02.md), sliced and pictured up to the owner gate; the prints wait on Omar in the backlog (3d-models #558)
- 2026-10-05 — Omar's sheets-04g fit verdict, kites too tight and the middle too loose, worked out piece by piece: the middle pieces had about 0.447 mm of play, from the rounded corner of the strap. bikar #303 cuts the piece along the strap's real edge (bet CAL-LSE-01), and a fit plate was laid out to check it (3d-models #547)

- 2026-10-04 — sheets-04g printed in green, with the coaster and all 41 pieces in one color: approved (3d-models #537), sent (3d-models #540) and finished in about 98 minutes against 86 sliced, with its rows in the print log (3d-models #542)
- 2026-10-04 — sheets-04g laid out: the gBV coaster and all 41 pieces in one color, and the sheets-04d, 04e and 04f plates taken off the queue (3d-models #530)
- 2026-10-04 — phones-02, pink only, each axis scaled on its own: 12 minutes and 3.46 g (3d-models #526, #527, #528, #529)
- 2026-10-04 — phones-01, the first two-color plate sliced and sent without Studio: 22 minutes sliced, 62 printed, the time going to the color swaps (3d-models #521, #522, #525)
- 2026-10-04 — The sheets-04d, 04e and 04f plates laid out (3d-models #520); #530 later took them off the queue
- 2026-10-04 — sheets-04c, the gBV minimal coaster on its own: 42 minutes and 10 g sliced (3d-models #514), approved (3d-models #515), sent (3d-models #516) and finished clean (3d-models #517)
- 2026-10-03 — sheets-04b re-sliced for the Textured PEI plate (3d-models #506), approved again (3d-models #510) and sent (3d-models #511)
- 2026-10-03 — sheets-04 printed, sent by Omar from Studio (3d-models #483); the pieces fell through their holes, and the print record moved to the plate's page (3d-models #484)
- 2026-10-02 — sheets-04, the gBV fit plate, with a bed map and labels (3d-models #473); it then printed the pieces in the real minimal coaster (3d-models #474), was re-sliced on the exact holes (3d-models #475) and approved (3d-models #479)

- 2026-09-27 — The dovetail slot is a true outward offset of the tab, so the fit plays the same all round the neck instead of pinching at the corners; the docs say so (bikar #262, 3d-models #351)
- 2026-09-27 — Slicing flattens each preset chain before it runs and checks the slice took the settings asked for, so a plate no longer slices on an inherited default without saying (3d-models #349)
- 2026-09-27 — minis-04 print record, with a verdict for each piece, and its lessons written into the sample and review-print skills (3d-models #348)
- 2026-09-27 — Print-quality design (pinholes, the wide peg border, pegs too tight): two independent researchers and a checker, consolidated into the one doc to act on (3d-models #346)
- 2026-09-27 — The butterfly key's default clearance is the dovetail's 0.15 per face, no longer half of it: since the true-offset slot the dovetail plays about 2.24c, so a halved key played 0.45× it and a full-c key plays 0.89×; the tab stays at 0.15 (bikar #264)
- 2026-09-26 — minis-04: 80 mm coasters at half height with a twist, on a height knob every flat coaster now has (bikar #252, 3d-models #329)
- 2026-09-26 — The `print-coaster-samples` skill lays out a minis plate with mating styles as pairs, and minis-03 was built with it for the openwork styles (3d-models #319)
- 2026-09-26 — `bambu print send` no longer always feeds from the empty external spool: it matches the plate's used filaments to the loaded trays and sends their numbers in `ams_mapping`, with `use_ams` set to match, and refuses (listing the trays) when the match is not clean, so the operator picks with `--ams-mapping` (3d-models #337)
- 2026-09-26 — Every tool that defaults to a bikar checkout now defaults to `~/Workspace/git/bikar-main` (the Makefile, the `bambu` tool, the prints and site-graph gates, `verify_machine_card.py`), not the bare repo whose leftover files were a 12 September build; and `slice compose` writes its `.3mf` to `build/plates/` at the repo root, not the working directory (3d-models #336)
- 2026-09-26 — The Coaster Lab shows each coaster style's print history: a Printed panel with every piece printed from the open file, read from the `prints-manifest.json` the site deploys, with its plate, verdict, knobs and notes, and a line when the file has changed since the print (bikar #260)
- 2026-09-26 — Joins sample plate (KEY-1): one mated pair per join on CS-1 at 80 mm, split across [minis-05](../../design/plates/minis-05.yaml) (plain, butterfly key with a 0.05/0.10/0.15 key ladder, tab) and [minis-06](../../design/plates/minis-06.yaml) (dovetail, slim dovetail), every piece through the mesh gate and the review sheet; closes the joins item — the print waits on Omar in the coaster-pipeline backlog
- 2026-09-26 — First print record in `docs/prints/`: minis-03, with photos and a verdict and
  notes for each piece at the size it printed. Every printed piece now needs its own verdict
  (prints gate R15). `slice compose` fills the printer settings from the `.3mf`. The
  review-print skill has a step for recording a print when it comes back.
- 2026-09-26 — minis-03 printed by Omar (5 pieces: CS-1, CS-2 and rDux minimal-frame, and a
  CS-1 minimal-pegs pair). It read well, but at 40 mm it was too small, and the mated pegs had a
  wide solid band at the join and a slightly loose fit. The lessons are in `sample-rules.md`
  and the review-print rubric.

## From the session task board, before the split

Finished work up to 2026-09-25 was kept on one list, `docs/tasks/done.md`, as ten snapshots
of the session task board; its sections were moved here by loop on 2026-09-25 (the file is in
git history). Numbers are the board's task ids, and **the board was renumbered more than
once**, so an id means something only under its snapshot: Snapshot 1's #14 and Snapshot 2's
#14 are different tasks. Each snapshot's own note below says which sequence it uses. Newest
first.

**▸ Snapshot 7 — 2026-09-17 (the first-print campaign — bambu CLI, the print-model
skill, and X2D bring-up prep).** The live board was renumbered again after Snapshot
6, so these ids are a **fresh sequence**: Snapshot 7's `#8` is the X2D live-hardware
bring-up, not Snapshot 6's naqsh construction statements or Snapshot 4/5's ledger
block. The board is the plan "First-print campaign — turning the X2D into settled
calibration data" (session plan binary-tickling-kay; decisions D-053/D-054 in the
[decisions log](../../working-model/decisions-log.md), D-055 amending D-054). The A-numbers
(`A1…A11`) are the plan's own Phase-A ids. Still open on the board at this prune:
**`#9`** — slice a real plate + the first owner-gated dispatch, which stays
CAL-bet-gated and owner-physical (filament is loaded; the remaining steps are Omar's
caliper/instruments, the Plate 1 slice-to-`.3mf`, and `bambu print send --record`).
The Phase-A slice profile + MC-4 pre-flight (A4/A5, tasks `#21`/`#22`) landed via PR
#185; their whole-card slice + auto_brim finding landed separately in #210.

### Phase A — X2D software prep (no printer, no touchscreen)
- #18 — `A1`: register `bambu-x2d` as a `PrintTarget` in bikar `machines.ts` (bikar)
- #19 — `A2`: decide the dual-nozzle representation — X2D rides single-nozzle-labelled FDM, `PrintTarget` not widened (D-053) (3d-models #222, relanded onto master; original #182 fell behind master and was superseded)
- #20 — `A3`: re-verify the machine card reproduces (`make coupons` + `make validate-coupons`, local — proves the Plate-1 substrate intact before asking for filament)
- #21 — `A4`: ready the slice path for the X2D profile — proven headless against a real X2D profile, the known-good preset trio recorded in the bench sheet (3d-models #185; the whole-card slice + auto_brim footgun recorded in #210)
- #22 — `A5`: eyeball the MC-4 overhang fan in the slicer before filament — pre-flight eyeballed supports-off (3d-models #185)
- #23 — `A6`: capture the X2D-profile-gap discovery in memory/skill — the machines.ts gap + a SKILL.md troubleshoot row for the missing machine target (memory bambu-x2d-bringup; 3d-models #184)
- #24 — `A7`: the pre-populated Plate 1 bench sheet Omar carries to the printer (3d-models #180)
- #25 — `A8`: encode the print→photograph→compare→verdict loop — the compare-verdict gate R5 + the prototype seams (3d-models #180)
- #28 — `A10`: grounded survey of Bambu control/slicing transport options, research checked in under a provenance header (3d-models #223, relanded; original #183 superseded)
- #29 — `A11`: the `tools/bambu` CLI design doc — the two-layer split, mermaid, a recorded decision (D-054) (3d-models #223, relanded)

**▸ Snapshot 1 — 2026-08-15 (the original prune).** Ids in the sections below are
the pre-renumber board.

### Calibration + text-emit arc
- #86 — Make calibration-design §7's expectation table executable (make coupons)
- #87 — Catch a use-case as_of pin orphaned by a squash merge
- #88 — Add the four uncatalogued §3.5 print-gated items <!--count:quote--> to the prototype catalog
- #89 — Close §6.3's documentation residue: the angle-convention line and the misattribution cluster
- #90 — Land D-016/D-017/D-018 — the three §6.2 design decisions the user settled
- #92 — Close §6.3's unsourced-number cluster (the last live cluster)
- #93 — Build D-016's per-pair border validator in bikar
- #94 — Build D-017's frame statement + its band-width default in bikar
- #95 — Close the use-case validator's one-commit blind spot
- #96 — Research + design doc: text emit on printed parts
- #97 — T0: register CAL-TXT-01/CAL-TXT-02 as Calibrated records in bikar
- #98 — T1: bake the glyph constant + B1–B3 checks, with DM Sans asserted to fail
- #99 — T2: solidifyText + the text statement + the label-gap validator in the mesh gate
- #100 — T3: label the 23 calibration coupons and reprint the machine card
- #101 — Evaluate a bet→coupon→catalog-entry gate before writing one
- #102 — Bake a slashed zero into the face (needs Source Code Pro 2.x)
- #103 — Wire checkLabelGap/Counter/Charset into the mesh gate once there is text to gate
- #104 — Per-placement color in the assembly DSL (grounded names + codes)
