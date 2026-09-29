# Backlog — grow the print catalog

Loop: [`catalog-expansion.md`](../../../.claude/loop-prompts/catalog-expansion.md). Done
list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal, per pass: the [ledger](../../constructions/ledger.md)'s migrated count up by one, or
the queue of screened candidates grown, each with a written GO or NO-GO.

## Open, in ROI order

1. **`nmEjCTzMbDg` still FAILs O1 and O2, and waits on youtube.** Causes found on
   2026-09-27 ([the FAILs note](../../research/ledger-oracle-fails-2026-09-27.md)). The
   youtube source's `R = Intersect(t, m, 2)` picks the other root in bikar. The patch,
   `Intersect(t, m, S)`, is proposed there and has not been made. Once youtube takes it:
   - regenerate the bikar fixture and goldens;
   - re-vendor the coaster and look at it (it is near-solid now: **do not print it**);
   - re-run O1 and O2.

   What O1 still cannot compare (parabolas, hyperbolas, arcs, the `*_host` circles) is
   youtube's to add. Also youtube's: `naqsh_score.py` treats `ggb_score.py`'s FAIL exit
   (2) as a crash. That patch is in the same note.
2. **Screened queue, 2026-09-27.** Two independent screens and a checker's consolidation:
   [the consolidated screen](../../research/candidate-screen-2026-09-27.md) is the one to act
   on. 10 GO, all from creators other than Sarah Brewer. Coaster fit was judged from
   thumbnails and storyboard frames only, so each still needs its render looked at. In
   rebuild order:
   1. `0ke_GpoBa-s`, Samira Mian, 10-fold rosette: chaptered, and the scaffold items 3, 5–7 reuse.
      **Done 2026-09-28 in youtube: 11/11 steps, mean edge-SSIM 0.869.** It is drawn on paper
      and filmed at a slight angle, so the frames had to be straightened first (`rectify.tsv`).
      The 10-fold grid (Ptolemy's pentagon, the {10/2} and {10/3} stars, the petal lines) is in
      `reconstructions/0ke_GpoBa-s/`, ready for the coaster step.
   2. `88q-u2eWZqg`, Eman Zainab, 16-petal rosette: a new fold; check the crowded centre.
      **Attempted 2026-09-28 in youtube: 6/9 steps, mean edge-SSIM 0.745.** The geometry is
      right. The three busiest steps stop near 0.59 because her pencil compass marks were
      never erased and her compass slipped a little, and no render can draw either. The
      centre was not the problem. For the coaster: the whole rosette is **one closed line**
      (each petal joins the petal three places round, and 3 and 16 share no factor), so it
      suits a single continuous groove. Two octagons, the inner circle and the 16 petals are in
      `reconstructions/88q-u2eWZqg/`, ready for the coaster step.
   3. `n_ICgwOr6qs`, Samira Mian, 5-fold arc motif: rebuild the 1:20–8:06 construction only; needs the arc path.
      **Done 2026-09-28 in youtube: 9/9 steps, mean edge-SSIM 0.886.** Drawn on paper and
      filmed, like 1; the camera zooms out once at about 04:00, so only the petals after it are
      scored. For the coaster: every line is an arc of **one compass size** (the chord across
      two of ten divisions), five front petals and five smaller behind petals, with a small gap
      at the centre where the front arcs stop short. Pure arcs, no straight lines, so it needs
      the arc path the other patterns do not. The ten arc pairs are in
      `reconstructions/n_ICgwOr6qs/`, ready for the coaster step.
   4. `Y6kS1MvnKoc`, Eric Broug, 10-fold star field (Mamluk Qur'an page): crop to the centre star.
      **Done 2026-09-28 in youtube: 17/18 slides, mean edge-SSIM 0.861.** Not paper: a deck of
      clean vector slides, so no camera correction. The whole page was rebuilt, not just the
      centre star. For the coaster: the red pattern is all straight lines, and every corner of it
      sits where two edges of the seven ten-point stars cross, so it can be cut from exact
      points. The page is a rectangle of ratio 1.376 (tan 54°), which is not a coaster shape.
      Crop to a circle round the centre star, or take the page as a tile. Mirror-symmetric both
      ways: a quarter drawn and reflected twice. The construction is in
      `reconstructions/Y6kS1MvnKoc/`, ready for the coaster step.
   5. `NtnlGMTElBk`, Samira Mian, 10-fold interlaced star: clean digital frames, 82 s, no narration.
      **Done 2026-09-28 in youtube: 13/13 steps, mean edge-SSIM 0.930.** For the coaster: the
      finished star is one closed white band, all straight lines, forty segments (a four-segment
      unit turned ten times). Every corner sits where a line of the {10/3} star crosses a line of
      the {10/4} star, so it can be cut from exact points. It already fits a circle (the unit
      circle), so no cropping is needed. The band crosses itself, so it could be cut as an
      over-under interlace. The construction is in `reconstructions/NtnlGMTElBk/`, ready for the
      coaster step.
   6. `yZN_wn0uvTY`, Geogebra_Road to School, 10-fold rosette built in GeoGebra with the algebra list on screen.
      **Swapped 2026-09-28 in youtube for its source, `gBV_JTt3Kxk`** (Samira Mian, "Itimad Ud
      Daula", a 2-minute silent animation of the same pattern). yZN drags the ten divisions by
      eye, so it is held behind gBV. **gBV done: 11/11 steps, mean edge-SSIM 0.906.** For the
      coaster: a ten-fold rosette of straight segments on two line families, pink {10/3} at
      0.588 R and black at 0.139 R, with every vertex a crossing of two named lines. It comes
      with its **repeat cell**, a 72° rhombus with apexes at the top and bottom points and side
      corners at (±tan 36°, 0) = (±0.7265, 0) R. The cell's sides are pink lines already in the
      pattern, so a tile edge never cuts a line at an arbitrary point. The lattice is
      (±0.7265, 1) R. It is either a round coaster (the rosette alone) or a rhombus coaster that
      tiles edge to edge. The construction is in `reconstructions/gBV_JTt3Kxk/`, ready for the
      coaster step.
   7. `_U6G8QSfWnk`, Samira Mian, 5/10-fold girih tiling: conditional; faint tracing steps, may need a one-cell crop.
      **Done 2026-09-29 in youtube: 6/6 steps, mean edge-SSIM 0.895** (pencil on paper, then
      tracing paper; 08:05–17:00 only). The worry did not hold: the pattern is lines, not
      near-solid, and no crop was needed, because the **fivefold rectangle is itself the cell**.
      For the coaster: a rectangle of 1.176 × 1.618 R (aspect tan 54°), with the centres of two
      ten-point stars at opposite corners. Star radii are exact: inner 0.618 R (1/φ), outer
      0.7265 R (tan 36°). The lines inside are a quarter of each star, turned 180° about the
      rectangle's centre; its sides are mirror lines of the tiling, so a rectangular coaster
      tiles edge to edge by reflection. The construction is in `reconstructions/_U6G8QSfWnk/`,
      ready for the coaster step.
   8. `fhGHzop7ULw`, Mohamad Aljanabi, 6-fold rectangle repeat unit: new creator, no new fold.
   9. `jlTmt_279M4`, unravelling pattern, 7-point stars in a square (Bourgoin pl. 170): conditional; frames near-white.
   10. `A9fefFurD_s`, Lex Wilson, 10-point star from Broug's book: low priority.

   Held: `LoCRh3SOhls` (a variant of 1) and GeoGebra `hzyhmg9p` (9+12 on the page, 8/9/5 in
   its preview; open the applet first, NC licence, goes through import-construction). No
   non-Brewer 9-fold video turned up in the searched space.
3. **frame block (P5.3)** — only if a public GeoGebra file needs one; nothing does yet. Moved
   from the coaster-pipeline backlog on 2026-09-25, where it sat by mistake (board #7).
4. **Radial fill on CS-1** — a minimal coaster with chosen rings of pieces made solid
   ([D-081](../../working-model/decisions-log.md)). The `orbit` word and openwork fill are on
   bikar main (bikar #270, 2026-09-29), with `patterns/Constructions/GimTvN9hw4U-radial-coaster.bkr`.
   **Waiting on Omar's pick** from the four fills below (orbits are numbered outwards; all four
   pass the mesh gate at 90 mm as one body). The pick becomes the file's live fill lines, and the
   CS-1 note gets a `radial` heading and picture.

   ![CS-1 radial fill choices](../../catalog/media/GimTvN9hw4U/GimTvN9hw4U-radial-choices.png)

   | Tile | Filled orbits | Open share |
   |---|---|---|
   | plain | none (the minimal coaster) | 0.38 |
   | A | 1, 3, 5, 7: a six-armed snowflake round an open centre star (the file's default) | 0.21 |
   | B | 0, 2, 4, 6: the centre and alternate rings, mostly solid | 0.17 |
   | C | 0, 1: a solid centre in an open lattice | 0.33 |
   | D | 6, 7: a solid rim round an open centre | 0.28 |

   Rebuilt with the four `fill void where orbit …` blocks the `.bkr` lists as alternatives,
   `bikar render … --format stl --check --param size=90`, then `python3 tools/print_review.py sheet`.
   Asked by Omar on 2026-09-27 (board #96).
   - **Color and Lab controls** (Omar, 2026-09-28) are built: all eight steps of
     [color-preview-design.md](../../design/coaster/color-preview-design.md) §10 (see
     [done.md](done.md)). The radial coaster now splits into a straps body and a Gold body, the top
     fillet kept. Printing it in more than one color still waits on a first-layer coupon, which is
     Omar's to print (write the bet with `calibrate` first).

## Handed to the video loop

GO candidates not yet reconstructed go to the youtube repo's ladder, not here. Name the id
in this list when you hand it on, and move it to item 2's shape when it comes back done.

Nothing is out with the loop right now (`n_ICgwOr6qs` came back 2026-09-28, item 2.3).
