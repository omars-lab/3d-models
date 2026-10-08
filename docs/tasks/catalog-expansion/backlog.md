# Backlog — grow the print catalog

Loop: [`catalog-expansion.md`](../../../.claude/loop-prompts/catalog-expansion.md). Done
list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal, per pass: the [ledger](../../constructions/ledger.md)'s migrated count up by one, or
the queue of screened candidates grown, each with a written GO or NO-GO.

## Open, in ROI order

Parked since 2026-10-06: Omar moved the work back to split coasters and split pieces ("i want
to wrap up consturciotn and move back to split coasters and split inflills"). Finish what is
half done (n_ICgwOr6qs, item 3) before starting a new construction.

1. **`nmEjCTzMbDg` still FAILs O1 and O2, and waits on youtube.** Causes found on
   2026-09-27 ([the FAILs note](../../research/ledger-oracle-fails-2026-09-27.md)). The
   youtube source's `R = Intersect(t, m, 2)` picks the other root in bikar. The patch,
   `Intersect(t, m, S)`, is proposed there and has not been made. Once youtube takes it:
   - regenerate the bikar fixture and goldens;
   - re-vendor the coaster and look at it (it is near-solid now: **do not print it**);
   - re-run O1 and O2.

   What O1 still cannot compare (parabolas, hyperbolas) is youtube's to add. Arcs and their
   `*_host` circles are compared on youtube branch `coaster-n_I` (2026-10-06); once it merges,
   re-run O1 on this one and on `gBV_JTt3Kxk`, which has ten scaffold arcs; its last O1 skipped or
   counted as extra 47 objects. Also youtube's: `naqsh_score.py` treats `ggb_score.py`'s FAIL exit
   (2) as a crash. That patch is in the same note.
2. **Reconstruction intake: read rung.yaml at session start, queue done reconstructions for
   import.** Asked by Omar on 2026-09-30. The session start hook never reads youtube's rung.yaml
   and imports nothing; 19 rungs are done in youtube with no coaster here, 9 of them with no
   ledger row. The [intake design](../../constructions/reconstruction-intake-design.md) proposes
   a small read-only intake list for the hook and a write mode for row stubs and the pin, with
   three open calls for Omar.
3. **Screened queue, 2026-09-27.** Two independent screens and a checker's consolidation:
   [the consolidated screen](../../research/candidate-screen-2026-09-27.md) is the one to act
   on. 10 GO, all from creators other than Sarah Brewer. Coaster fit was judged from
   thumbnails and storyboard frames only, so each still needs its render looked at. In
   rebuild order:
   1. `0ke_GpoBa-s`, Samira Mian, 10-fold rosette: chaptered, and the scaffold items 3, 5–7 reuse.
      **Done 2026-09-28 in youtube: 11/11 steps, mean edge-SSIM 0.869.** It is drawn on paper
      and filmed at a slight angle, so the frames had to be straightened first (`rectify.tsv`).
      The 10-fold grid (Ptolemy's pentagon, the {10/2} and {10/3} stars, the petal lines) is in
      `reconstructions/0ke_GpoBa-s/`, ready for the coaster step.
      **Coaster step done 2026-10-06**: bikar #315 (the grid and its minimal coaster; the
      diameters and circle stay scaffold), ledger row filled, `CS-16`, gallery card, vendored
      STL. Its youtube source rewrite (the petal ring as one whole ten-fold turn, and the hero
      export) is on youtube branch `coaster-0ke`, waiting on Omar's merge into main.
   2. `88q-u2eWZqg`, Eman Zainab, 16-petal rosette: a new fold; check the crowded centre.
      **Attempted 2026-09-28 in youtube: 6/9 steps, mean edge-SSIM 0.745.** The geometry is
      right. The three busiest steps stop near 0.59 because her pencil compass marks were
      never erased and her compass slipped a little, and no render can draw either. The
      centre was not the problem. For the coaster: the whole rosette is **one closed line**
      (each petal joins the petal three places round, and 3 and 16 share no factor), so it
      suits a single continuous groove. Two octagons, the inner circle and the 16 petals are in
      `reconstructions/88q-u2eWZqg/`, ready for the coaster step.
      **Coaster step done 2026-10-06**: bikar #317 (the rosette and its minimal coaster,
      imported from youtube main as it is; the circles and octagon turns stay scaffold), ledger
      row filled, `CS-17`, gallery card, vendored STL. At 40 mm the straps nearly close the
      middle windows, so its mini wants about 60 mm.
   3. `n_ICgwOr6qs`, Samira Mian, 5-fold arc motif: rebuild the 1:20–8:06 construction only; needs the arc path.
      **Done 2026-09-28 in youtube: 9/9 steps, mean edge-SSIM 0.886.** Drawn on paper and
      filmed, like 1; the camera zooms out once at about 04:00, so only the petals after it are
      scored. For the coaster: every line is an arc of **one compass size** (the chord across
      two of ten divisions), five front petals and five smaller behind petals, with a small gap
      at the centre where the front arcs stop short. Pure arcs, no straight lines, so it needs
      the arc path the other patterns do not. The ten arc pairs are in
      `reconstructions/n_ICgwOr6qs/`, ready for the coaster step.
      **Coaster step half done 2026-10-06, then parked** (Omar: "i want to wrap up consturciotn
      and move back to split coasters and split inflills"). Done: the source rewrite (whole lines
      through the unit points, and the 180° ray as a segment to a derived far point, so no free
      point sits off the frame) is on youtube branch `coaster-n_I` (6e7fc45), still 9/9 at mean
      0.886, waiting on Omar's merge into main. The O1 check for arcs is on the same branch.
      The importer change that rotates a list of arcs is its own bikar PR
      (`import-conjugate-arcs`). With both, the import lowers in full (nothing refused), and both
      checks pass: O1 34 compared, 0 failed, and O2 edge 0.982 with recall and precision 1.0.
      Left: in bikar, the golden, fixture, minimal coaster, `--check` at 40/60/90 mm and the Lab
      entry, following the 88q PR (#317). Then in this repo, the ledger row, `CS-18`, the gallery
      card and the vendored STL.
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
      over-under interlace. The construction is in `reconstructions/NtnlGMTElBk/`.
      **Coaster step done 2026-09-30**: bikar #285 (the piece and its minimal coaster, plain
      straps, no weave), ledger row filled, `CS-15`, gallery card, vendored STL. Its youtube
      source rewrite (`ntnl-supported-vocabulary`, ec697a1) is on youtube main since 2026-09-30,
      re-scored 13/13, mean 0.934.
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
      tiles edge to edge. The construction is in `reconstructions/gBV_JTt3Kxk/`.
      **Coaster step done 2026-09-30**: bikar #287 (the piece and its minimal coaster, the
      rosette alone with the paint-over masks left off), ledger row filled, `CS-13`, gallery
      card, vendored STL. O2 FAILs on precision because of those masks (see the ledger's oracle
      notes). Its youtube source rewrite (`gbv-supported-vocabulary`, d0732db) is on youtube
      main since 2026-09-30, re-scored 11/11, mean 0.913.
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
      **Done 2026-09-29 in youtube: 9/9 steps, mean edge-SSIM 0.921** (a silent animation; the
      scaffold is rebuilt to 06:50, and the finished unit at 11:30). For the coaster: a
      **1 × √3 rectangle** with star centres at two opposite corners, each corner split into
      15° steps. Every line is a tangent to one of two circles about a star centre, radius
      sin 22.5° = 0.383 or cos 37.5° = 0.793 of the short side, touching at 7.5° + 15°·k.
      Turned 180° about the rectangle's centre, the lines give the other star; the sides are
      mirror lines, so a rectangular coaster tiles edge to edge by reflection. The construction
      is in `reconstructions/fhGHzop7ULw/`, ready for the coaster step.
   9. `jlTmt_279M4`, unravelling pattern, 7-point stars in a square (Bourgoin pl. 170): conditional; frames near-white.
      **Done 2026-09-29 in youtube: 17/17 steps, mean edge-SSIM 0.941** (a 2:47 animation; the
      near-white frames were faint grey lines, which score fine). For the coaster: a **square
      tile tilted 90/7° = 12.857°**, with four seven-point stars (radius 0.4725 R) whose centres
      sit on the tile's sides, round an octagon (radius 0.327 R) at the centre. All straight
      lines. Each side runs through a star centre along one of the star's mirrors, so the
      sides are mirror lines: a square coaster tiles edge to edge by reflection, and the half
      stars on the edges close into whole stars. The tile alone has no mirror of its own
      (it turns by quarter turns only). Tile half-width 0.975 R. The construction is in
      `reconstructions/jlTmt_279M4/`.
      **Coaster step done 2026-09-30**: bikar #286 (the piece and its minimal coaster on a
      square fit), ledger row filled, `CS-14`, gallery card, vendored STL. Its O1 PASS needs
      youtube's `o1-polyline-ray` change (9a92134), on youtube main since 2026-09-30.
   10. `A9fefFurD_s`, Lex Wilson, 10-point star from Broug's book: low priority.
      **Done 2026-09-29 in youtube: 17/17 steps, mean edge-SSIM 0.855** (a 3:52 slide deck;
      the dense slides hold at ~0.73 because the slides' own lines are hand-placed slightly off).
      For the coaster: a **single ten-point star medallion**, not a tile. One eight-sided shape
      (corners at the top and bottom points of the circle, (±0.449, ±0.382) R and (±0.172, 0) R)
      turned 36° four times; its ten outer points sit on the circle of radius R, so it fits a
      round coaster. All straight lines, built from one circle by compass and straightedge
      (the pentagon by the golden cut). The construction is in `reconstructions/A9fefFurD_s/`,
      ready for the coaster step.
   11. `1h7iWJaoN80`, Sarah Brewer, Folio 192 of the Anonymous Persian Compendium (Isfahan):
      added from youtube's `make ladder` once rows 1–10 were done.
      **Done 2026-09-29 in youtube: 27/27 steps, mean edge-SSIM 0.862** (a 24-minute narrated
      GeoGebra screencast; the finished panel scores 0.945). For the coaster: a **rectangle of
      1.620 × 1** (the short side is the unit) filled with tan and blue tiles laid out on a
      **regular heptagon** of circumradius 0.2846. The two heptagon centres sit on the long
      sides (one on the bottom, one on the top), so each edge cuts a heptagon. Every edge runs
      along one of the heptagon's seven side directions, all straight lines, from one angle
      (3π/14) by compass and straightedge. The panel turns 180° about its centre onto itself
      but has no mirror of its own. The video says the pattern extends by reflecting the
      rectangle in its sides, so a rectangular coaster tiles edge to edge by reflection. The
      heptagon on the bottom edge is drawn whole and pokes past the rectangle; clip it at the
      edge. The construction is in `reconstructions/1h7iWJaoN80/`, ready for the coaster step.
   12. `kpFgs2e8YGw`, Sarah Brewer, star rosettes on a 3-uniform tiling (12-gon, hexagon,
      square, triangle): added from youtube's `make ladder`.
      **Done 2026-09-29 in youtube: 30/30 steps, mean edge-SSIM 0.911** (a narrated GeoGebra
      screencast with one angle slider). For the coaster: a **six-fold patch** (wallpaper
      group p6m), a ring of 12-fold rosettes round a 6-fold rosette at the hexagon centre,
      with 4-fold rosettes and triangle petals between them. Every line passes through a
      point where two circles touch, at ±30° from the line joining their centres; the circles
      sit on the vertices of a unit-edge tiling (radius ½) and at each polygon's centre
      (radius = circumradius − ½). The 12-gon circumradius is 1.932 of the edge. All straight
      lines, one parameter; at 30° the hexagons come out regular. It fits a round coaster
      centred on the hexagon, clipped at the rosette ring. The construction is in
      `reconstructions/kpFgs2e8YGw/`, ready for the coaster step.
   13. `cKYbKQvmsbs`, Sarah Brewer, Sultan Barsbay 16 & 8 (Cairo): added from youtube's
      `make ladder`.
      **Done 2026-09-29 in youtube: 50/50 steps, mean edge-SSIM 0.837** (a 28-minute narrated
      GeoGebra screencast; the finished field scores 0.915 and 0.921). For the coaster: a
      **square tile of side 2** (wallpaper group p4m) with a 16-fold rosette at its centre
      and a quarter of an 8-fold rosette in each corner. With the centre at (1, 0) and an edge
      midpoint at (0, 0), every line is one line, from (0, 0.541) to (0.324, 0.676), reflected
      over mirrors 11.25° apart at the centre; the 16-point star sits on a circle about the
      centre. All straight lines, by compass and straightedge. The sides are mirror lines, so
      a square coaster tiles edge to edge by reflection, and the quarter rosettes in the
      corners close into whole 8-fold rosettes. The construction is in
      `reconstructions/cKYbKQvmsbs/`, ready for the coaster step.
   14. `1TclLO9JKAA`, Sarah Brewer, a parallel 9-fold star rosette ("Avoiding Open Paths"):
      added from youtube's `make ladder`.
      **Done 2026-09-29 in youtube: 16/16 steps, mean edge-SSIM 0.931** (a 2:39 narrated
      GeoGebra screencast; the finished rosette scores 0.945). For the coaster: a **nine-fold
      rosette** (group D9) of nine petals whose long sides are parallel, inside a nonagon of
      side 1 (circumradius 1.462). One petal is built and rotated eight times about the
      centre; its width is 0.658 of the side. All straight lines, by compass and straightedge.
      It fits a round coaster centred on the rosette, keeping the nonagon as its outline.
      Nine-fold does not tile, so this is a single-piece coaster, not a tiling one. The
      construction is in `reconstructions/1TclLO9JKAA/`, ready for the coaster step.
   15. `ZXKYNvqtFKs`, Sarah Brewer, rings of tangent circles: added from youtube's
      `make ladder`.
      **Done 2026-09-29 in youtube: 26/26 steps, mean edge-SSIM 0.920** (a 3:54 narrated
      GeoGebra screencast). For the coaster: **rings of circles** inside a regular n-gon of
      side 1, any n from 3 to 30 (she shows 11, 8 and 12). A chain of five circles runs from
      a vertex toward the centre, each touching the last, their radii shrinking by a fixed
      ratio (0.606 at n = 11: 0.5, 0.303, 0.183, 0.111, 0.067); each is copied n times about
      the centre, so the rings pack into one another (group Dn). Circles only, no straight
      lines but the polygon. The smallest ring is fine detail at coaster size: two or three
      rings may be the printable cut. The construction is in `reconstructions/ZXKYNvqtFKs/`,
      ready for the coaster step.
   16. `tcZQLpnxGpw`, Sarah Brewer, 12-fold pattern in a 6-4-3-4 tiling: added from youtube's
      `make ladder`.
      **Done 2026-09-29 in youtube: 57/57 steps, mean edge-SSIM 0.8945** (a 19:57 narrated
      GeoGebra screencast). For the coaster: a **12-fold rosette filling a regular 12-gon of
      side 1** over the 3.4.6.4 tiling: a 12-point rosette in the central hexagon, an 8-point
      star in each of the six squares, and a ring of kites at each 12-gon corner. One angle α
      sets every piece; the finished piece is at α = 19°. The 12-gon is a natural round-ish
      coaster outline. Filled shapes with outlines, dense at the rim: the kite ring at each
      12-gon corner is the finest detail. One kite ring (at H) is built from a measured
      assumption, true at α = 19° (see the youtube reconstruction notes). The
      construction is in `reconstructions/tcZQLpnxGpw/`, ready for the coaster step.
   17. `itZftnqJ3tI`, Sarah Brewer, star rosettes on a 4-uniform tiling, in a square: added
      from youtube's `make ladder`.
      **Done 2026-09-29 in youtube: 102/102 steps, mean edge-SSIM 0.9062** (a 44:44 narrated
      GeoGebra screencast). For the coaster: a **square tile of the p4m cell** (side 3 + √3,
      the red mirror lines): 12-point rosettes on its four corners, four 4-fold rosettes about
      its centre, octagons on its edge midpoints, all set by one angle α (the finished piece
      is at α = 30°). A square outline is the natural coaster; it tiles, so a set of coasters
      makes the larger pattern. Filled shapes with outlines, of even density; the finest
      detail is the kite ring inside each 12-rosette (see the youtube reconstruction notes).
      The construction is in `reconstructions/itZftnqJ3tI/`, ready for the coaster step.
   18. `Ln-s5FzLGms`, Sarah Brewer, 8-fold rosettes turned 45°, with squares: added from
      youtube's `make ladder`.
      **Done 2026-09-30 in youtube: 40/40 steps, mean edge-SSIM 0.8833** (a 44:16 narrated
      GeoGebra screencast). For the coaster: a **4×4 square** of the square grid (group p4m).
      8-point star rosettes, each ringed by eight petals, sit on every other grid point, with
      octagons on the points between them and a small square where two bird's-foot tiles
      cross, so the rosettes run on a lattice turned 45° to the square. One angle α sets
      every piece; the finished piece is at α = 22.5°, "the classic version". The square is
      centred on a rosette and is one quarter turned four times, so a square coaster falls
      out naturally, and it tiles. Filled shapes with outlines, of even density; the finest
      detail is the petal ring about each rosette (see the youtube reconstruction notes).
      The construction is in `reconstructions/Ln-s5FzLGms/`, ready for the coaster step.
   19. `awOusq0uVzc`, Sarah Brewer, the Ibn Tulun variable-angle pattern (from the minbar):
      added from youtube's `make ladder`, first held because its keyframes missed the build,
      then screened GO once frames were grabbed every 6 seconds.
      **Done 2026-09-30 in youtube: 60/60 steps, mean edge-SSIM 0.9197** (a 35:45 narrated
      GeoGebra screencast). For the coaster: a **2×2 square** of the square grid (group p4m),
      centred on an 8-point star. Half stars sit on the edges and quarter octagons in the
      corners, with hexagonal petals and octagons between them. One angle α bends the whole
      pattern; α = 22.5° gives the classic version and the video finishes at α = 30°, so one
      construction yields a family of coasters. The square is one quarter turned four times
      and then mirrored, so a square coaster falls out naturally, and it tiles. Filled shapes
      with outlines; the finest detail is the petal and octagon pair round each star (see the
      youtube reconstruction notes). The construction is in `reconstructions/awOusq0uVzc/`,
      ready for the coaster step.
   20. `xtox61vADMA`, Sarah Brewer, a discrete variable star rosette on two whole-number
      sliders: picked from youtube's ladder over `yZN_wn0uvTY` and screened GO once frames
      were grabbed every 6 seconds over the build (the video is 65 minutes long).
      **Done 2026-09-30 in youtube: 30/30 steps, mean edge-SSIM 0.9297** (a narrated
      GeoGebra screencast). For the coaster: **one round rosette**, a ring of n stars and n
      kites about a centre (group Dn), so a round coaster falls out naturally; it does not
      tile. Two sliders make it a family: n sets the number of points (5 to 30) and k the
      angle of the pattern line, so one construction yields many coasters. The video ends at
      n = 18, k = 15, gray darts and white stars in thick black outline; the finest detail is
      the dart tips, which get narrow as k grows, so check the thinnest dart against the
      printer before picking n and k. The construction is in `reconstructions/xtox61vADMA/`,
      ready for the coaster step.
   21. `ZFQt67eZ9Sg`, Sarah Brewer, the door pattern of the Hall of the Two Sisters in the
      Alhambra: 8-fold in a unit square, screened GO on 2026-09-17 once frames were grabbed
      every 5 seconds over the build. **Done 2026-09-30 in youtube: 58/58 steps, mean
      edge-SSIM 0.8814** (a narrated GeoGebra screencast). For the coaster: **a square tile**,
      an 8-pointed star at the centre with kites and a 14-sided star round it, and three tiles
      along each edge, so a square coaster falls out naturally and it tiles (the finished door
      is this square repeated). Group D4 for the square, with an 8-fold star inside. It is
      drawn as blue lines with light green fills; the finest detail is the narrow triangle
      between the star's arms and the edge tiles, so check it against the printer. The
      construction is in `reconstructions/ZFQt67eZ9Sg/`, ready for the coaster step.
   22. `XfY1r7QKYwA`, Sarah Brewer, the 7-fold star rosette built slowly (27 minutes), screened
      GO on 2026-09-30 once frames were grabbed every 5 seconds over the build. **Done
      2026-09-30 in youtube: 30/30 steps, mean edge-SSIM 0.9489** (a narrated GeoGebra
      screencast). For the coaster: the same kind of rosette as `tA8eSdVx_EQ`, seven kites and
      seven arrow hexagons round a centre, with the star tips on the heptagon's edges at any
      slider angle. Group D7 (each piece is mirrored in its spoke), so it wants a round or
      heptagonal coaster and it does not tile. The slider angle α sets the look; she
      finishes at α = 24.5, and the thinnest part is the kite's tip near the centre, so check
      it against the printer before picking α. The construction is in
      `reconstructions/XfY1r7QKYwA/`, ready for the coaster step.
   23. `yZN_wn0uvTY`, Geogebra_Road to School, the Itimad-ud-Daula ten-fold rosette built by
      hand in GeoGebra and then tiled (Indonesian), screened GO (costly) on 2026-09-28.
      **Attempted 2026-09-30 in youtube: 9/13 steps, mean edge-SSIM 0.7375** (a narrated
      GeoGebra screencast; the four short steps are faint 1-px guide lines and point labels,
      and the finished tiling passes at 0.861). For the coaster: this is the same pattern as
      item 6 (`gBV_JTt3Kxk`), but her points were dragged by eye, so the ten-fold symmetry is
      off by up to 2° and the reconstruction keeps her error on purpose. **Print from item 6,
      not this one.** What this one adds is the tiling: the rosette with a peach petal in each
      red loop, copied by two vectors, u = (−6.12, 8.1) and v = (−5.85, −7.79). The
      construction is in `reconstructions/yZN_wn0uvTY/`.

   Held: `LoCRh3SOhls` (a variant of 1) and GeoGebra `hzyhmg9p` (9+12 on the page, 8/9/5 in
   its preview; open the applet first, NC licence, goes through import-construction). No
   non-Brewer 9-fold video turned up in the searched space; item 14 is Brewer's.
4. **frame block (P5.3)** — only if a public GeoGebra file needs one; nothing does yet. Moved
   from the coaster-pipeline backlog on 2026-09-25, where it sat by mistake (board #7).
5. **Radial fill on CS-1** — a minimal coaster with chosen rings of pieces made solid
   ([D-081](../../working-model/decisions-log.md)). The `orbit` word and openwork fill are on
   bikar main (bikar #270, 2026-09-29), with `patterns/Constructions/GimTvN9hw4U-radial-coaster.bkr`.
   **Omar picked none of the four fills below** (review thread kpdekz on the
   [2026-09-29 open-calls page](../../working-model/feedback-requests/2026-09-29-open-calls.md),
   2026-09-29). He wants to pick the fill himself in the Coaster Lab, and the picker is now on
   bikar main (bikar #288, 2026-09-30): click a piece in the picture, every piece on its ring
   (the same distance from the centre) lights up, the ring's row in the Orbits panel (bikar #282)
   is marked, and a chip offers Fill ring or Clear ring, writing the same `fill void where orbit`
   line the tick writes. **Waiting on Omar's pick** in the Lab; the file keeps fill A as its
   default until they save one.

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
6. **Lines and loose pieces in two colors, on any coaster; plus fill height and "assemble your own
   coaster".** Omar, 2026-09-29, review thread 3kqnku, asked three things: the fill height at either
   end, loose inner pieces for a printed frame, and a guided page. On 2026-10-01 (thread nhtq79, on
   gBV) he sharpened the second ask. Print the lines with the spaces open, and print the spaces as
   pieces in another color that fit back in, as an option on any coaster. The design is
   [loose-pieces-design.md](../../design/coaster/loose-pieces-design.md) (draft, 2026-09-30).
   Call 1 there is decided (D-090): the backed frame first for the gap reading, then the openwork
   frame, both with the same pieces, on gBV. The true edges shipped 2026-10-01 (bikar #291), and
   the loose-piece output and the backed frame the same day (bikar #292): `loose where …`,
   `--piece Frame` and one `--piece <color>`, pocket walls on the exact outline. The gBV fit sheet
   (item 8, sheet 4) is built and waits on Omar; the piece height (sheet 5's tall piece) shipped
   2026-10-06 (bikar #313), and so did the openwork frame (bikar #314): `loose` on a minimal coaster gives its frame and pieces from one file. The Lab's Loose button shipped 2026-10-05 (bikar #308). The catalog style name for a loose coaster file stays Omar's (design §6 item 6). Calls 2, 3 and 4 there
   (guided page, raised fills, the sample's gaps) are still Omar's. Call 2 on the open-calls page stays open for the default fill
   height.
7. **Start the gBV_JTt3Kxk coaster.** Omar picked it on 2026-10-01
   ([D-089](../../working-model/decisions-log.md#d-089--gbv_jtt3kxk-is-the-next-coaster)) from the
   [top-three renders page](../../working-model/feedback-requests/2026-09-30-top-three-renders.md).
   Its minimal coaster is in bikar (#287). It already has its ledger row (CS-13), a vendored STL
   and a gallery card, which is live on gh-pages (checked 2026-10-01). Its samples plate is folded
   into the gBV fit plate of item 6: that plate's openwork frame is this coaster's lines print, so a
   separate plate would print the same thing twice. The first full run of the
   [`prioritize-design`](../../../.claude/skills/prioritize-design/SKILL.md) skill is still owed.
8. **Sampler sheets: decide the smooth-lines calls with samples in the hand.** Omar, 2026-10-01,
   thread iykpc9 on the smooth-lines design, asked for printed sheets of labeled shape subsets
   before making the §6 calls. The design is
   [sampler-sheets-design.md](../../design/coaster/sampler-sheets-design.md) (draft): true-size
   30 mm windows of CS-1, CS-2 and gBV standing on a card with engraved row and column codes, five
   sheets (edge and top, star points, soft weld, fit, fill height). Sheets 4 and 5 were added the
   same day for loose-pieces calls 4 and 3 (Omar, thread tfuhdk), with three pictures for call 2.
   Its three calls are Omar's. The true edge that sheets 1 and 4 waited on shipped 2026-10-01
   (bikar #291), and the window cut shipped the same day (bikar #293), tried on all three columns
   and on sheet 5's square slab. The labeled cards for sheets 1 and 5 (bikar #294) and the
   sheet plate (`bambu slice sheet`, one color) shipped the same day too, and sheet 1 is built in
   full ([`sheets-01.yaml`](../../design/plates/sheets-01.yaml), waiting on Omar's tick). Sheet 4 is built
   in full too: its file is bikar's `Loose-Fit-Coupon.bkr` (#296) and its plate
   [`sheets-04.yaml`](../../design/plates/sheets-04.yaml) slices to one bed, 62 minutes, 17 g, with a bed
   map naming each look-alike set. Since 2026-10-02 it prints the pieces in the real minimal
   coaster (Omar's ask) rather than the coupon's frame. The coaster's holes are now cut on the
   pieces' exact outline (bikar #297), so every set keeps its full gap. A seventh set, `PEAK 2`, tries
   the 2 mm peaked pieces beside the flat ones (D-091). Omar approved the sheet 2026-10-02, and
   the failure-detection question is settled as the X2D's own (D-092). Omar printed it the same
   day, and all the small pieces fell right through the floorless coaster's holes at every gap.
   The next try, [sheets-04b](../../design/plates/sheets-04b.md), is pieces only, 4 mm tall and flat, at
   0.05 down to a −0.10 press fit (bikar #300), and waits on Omar's tick.
   Sheet 2 is built in full ([sheets-02](../../design/plates/sheets-02.md): option 5 as
   `holes round`, bikar #325, fed by a `tip` knob on every minimal coaster and its card, bikar
   #328) and waits on Omar's tick. Sheet 3 is built in full too
   ([sheets-03](../../design/plates/sheets-03.md): option 8 as `holes weld`, fed by a `weld`
   knob on every minimal coaster, and its card, bikar #329) and waits on Omar's tick.
   What is left: sheet 5 the
   sheet plate's color parts per sample (its tall-piece row's height shipped, bikar #313) and its raised row raised fills
   (loose-pieces §6 item 1, a bikar branch is enough). Sheet 5 has a plate page
   at `planned` ([sheets-05](../../design/plates/sheets-05.md)), whose `needs:`
   is this list; the print itself is on the coaster-pipeline loop's owner-gated list.
9. **Room for ids and dots on more coasters.** bikar's `mark` and `mark dots` (bikar #323) put
   an id on every prototype, at Omar's ask on the 2026-10-06 calls page ("every proptoty should
   have an id"). Using them on the 2026-10-07 plates (3d-models #600) showed three limits, all in
   bikar's `coaster-mark.ts` and `coaster-loose.ts`. Dots at the middle is done, and turns at 18°
   steps were measured and gained nothing, so they were not added
   ([the write-up](../../issues/mark-turns-18-no-gain.md)). One is left:
   - **One digit.** split-01 takes ids 1 to 9. split-02 takes 1 to 9 except 4, at 2 mm, and only
     at its 112.5 mm size. A tenth prototype of either coaster has no id that fits. Two digits
     need a smaller cap, which the 0.4 mm hole floor refuses, or a wider spot to put them. Of
     the two-digit ids, split-01 has room for 11, 12, 14, 15, 17, 71 and 77, though its `id`
     range stops at 9; split-02 has room for none of 10 to 19.

## Handed to the video loop

GO candidates not yet reconstructed go to the youtube repo's ladder, not here. Name the id
in this list when you hand it on, and move it to item 2's shape when it comes back done.

Nothing is out with the loop right now (`n_ICgwOr6qs` came back 2026-09-28, item 2.3).
