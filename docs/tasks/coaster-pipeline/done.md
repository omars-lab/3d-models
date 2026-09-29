# Done — first print and calibration

Newest first: date, what shipped, PR. Backlog: [`backlog.md`](backlog.md).

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
- 2026-09-26 — Joins sample plate (KEY-1): one mated pair per join on CS-1 at 80 mm, split across [minis-05](../../plates/minis-05.yaml) (plain, butterfly key with a 0.05/0.10/0.15 key ladder, tab) and [minis-06](../../plates/minis-06.yaml) (dovetail, slim dovetail), every piece through the mesh gate and the review sheet; closes the joins item — the print waits on Omar in the coaster-pipeline backlog
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
