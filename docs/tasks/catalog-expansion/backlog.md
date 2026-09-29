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
   5. `NtnlGMTElBk`, Samira Mian, 10-fold interlaced star: clean digital frames, 82 s, no narration.
   6. `yZN_wn0uvTY`, Geogebra_Road to School, 10-fold rosette built in GeoGebra with the algebra list on screen.
   7. `_U6G8QSfWnk`, Samira Mian, 5/10-fold girih tiling: conditional; faint tracing steps, may need a one-cell crop.
   8. `fhGHzop7ULw`, Mohamad Aljanabi, 6-fold rectangle repeat unit: new creator, no new fold.
   9. `jlTmt_279M4`, unravelling pattern, 7-point stars in a square (Bourgoin pl. 170): conditional; frames near-white.
   10. `A9fefFurD_s`, Lex Wilson, 10-point star from Broug's book: low priority.

   Held: `LoCRh3SOhls` (a variant of 1) and GeoGebra `hzyhmg9p` (9+12 on the page, 8/9/5 in
   its preview; open the applet first, NC licence, goes through import-construction). No
   non-Brewer 9-fold video turned up in the searched space.
3. **frame block (P5.3)** — only if a public GeoGebra file needs one; nothing does yet. Moved
   from the coaster-pipeline backlog on 2026-09-25, where it sat by mistake (board #7).
4. **Radial fill on CS-1** — a minimal coaster with chosen rings of pieces made solid
   ([D-081](../../decisions-log.md)). Being built in bikar: the `orbit` word (pieces
   grouped about the pattern's true centre) and openwork fill. Then render 3 or 4 fill patterns;
   Omar picks one, and the CS-1 note gets a `radial` heading and picture. Asked by Omar on
   2026-09-27 (board #96).
   - **Color and Lab controls** (Omar, 2026-09-28): coloring the radial fills, colored
     gallery PNGs, and an Orbits panel in Coaster Lab. Act on
     [color-preview-design.md](../../design/coaster/color-preview-design.md), §10 lists the bikar PRs,
     smallest first. The radial coaster needs the openwork split and the top-fillet split (§4)
     before it can print in more than one color.

## Handed to the video loop

GO candidates not yet reconstructed go to the youtube repo's ladder, not here. Name the id
in this list when you hand it on, and move it to item 2's shape when it comes back done.

Nothing is out with the loop right now (`n_ICgwOr6qs` came back 2026-09-28, item 2.3).
