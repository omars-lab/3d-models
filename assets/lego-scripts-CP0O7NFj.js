import{C as e}from"./dist-DJl9eW3M.js";function t(t,n,r){return{w:e(t),h:e(n),ox:r.col*8,oy:r.row*8}}var n=[{id:`classic-brick`,title:`Classic 2×4`,blurb:`LDraw's 3001 printed — the reference brick, no art`,source:`# Classic-Brick — the reference part: a plain 2 × 4 with studs on top and
# anti-studs underneath, i.e. LDraw \`3001.dat\` printed instead of moulded.
#
# It carries no art on purpose. Every other preset here changes one thing
# about this piece, so this is the one to print first and the one to measure
# a clutch against: if a real brick will not stack onto this, no amount of
# pattern work downstream is going to fit either. That is also why it is the
# preset whose knobs are the *interface* dimensions rather than the art —
# \`plates\`, \`engage\`, and the footprint itself.
#
# \`studs full\` is what makes it stackable, and it is the mode V4 refuses to
# combine with relief: a stud sits 1.6 mm proud of exactly the surface art
# would be cut into. A patterned piece gives up stacking; this one gives up
# the pattern. There is no setting that gets both on one face.
#
# The 2 × 4 footprint is where §3.3's contact census is least forgiving: the
# tangent side wall supplies 50 % of the clamping contacts on this shape (67 %
# on a 2 × 2), so the three tube anchors are only half the grip and the shell
# wall is the other half. \`clutch auto\` emits the §7.6 rib set into both.
#
# Render:
#   bikar render patterns/Lego/Classic-Brick.bkr --format stl --check -o ClassicBrick.stl
#     (STL = the printable brick; stderr = the anchor gate and §6 warnings)
#
# Every dimension the clutch depends on is an unmeasured bet (CAL-RIB-01,
# coupon LG-F1). Print the coupon before trusting the fit.

param cols = 2 range 2..8 step 1
param rows = 4 range 2..8 step 1
param plates = 3 range 1..9 step 1
param engage = 3.2 range 1.6..4.0 step 0.2

brick ClassicBrick
  footprint $cols x $rows
  height $plates plates
  studs full
  anchors auto
  engage $engage
  clutch auto
  origin centered
`},{id:`star-brick`,title:`Star Brick`,blurb:`{8/3} octagram cut as relief into a 4×4 top face`,source:`# Star-Brick — the Lego Lab M6 deliverable: a LEGO-compatible brick whose
# top face carries an {8/3} octagram cut in as relief.
#
# The art is inscribed in a radius-12 circle, so its bounding box spans
# 24 mm. \`footprint auto\` rounds that up to the smallest whole footprint
# that contains it — 4 × 4 studs, i.e. 8·4 − 0.2 = 31.8 mm — which leaves
# ~3.9 mm of margin per side between the art and the shell wall. Nothing is
# scaled to make that fit: bikar draws pieces at real scale, so a bigger
# brick is a bigger \`footprint\` and smaller art is a smaller pattern.
#
# \`studs none\` is not a style choice. Studs and relief are mutually
# exclusive on the same face (validator V4) — a stud sits 1.6 mm proud of
# exactly the surface the art is cut into, so studs would bury it. The
# piece is still a full participant in the system: it has anti-studs
# underneath, and \`anchors auto\` gives it the 3 × 3 tube grid that locks it
# against rotation on whatever it is pressed onto.
#
# The default \`plates 3\` is one brick, 9.6 mm. That is what carries the
# settled 3.2 mm \`engage\`: a single plate is 3.2 mm tall, so a plate that
# engaged 3.2 mm would have no ceiling left at all. The remaining 6.4 mm of
# ceiling is what the 0.8 mm relief is cut into.
#
# The three knobs are ranged so that every combination reachable in the Lab
# is buildable, which is not automatic — \`ceiling = plates·3.2 − engage\` and
# V3 needs 1.2 mm of it left under the relief. At the thinnest corner of the
# space (2 plates, engage 4.0) the budget is 1.2 mm, so \`relief\`'s 2.0 mm
# ceiling gets clamped rather than refused, and the floor of \`plates\` is 2
# because §4's one-plate body has no relief budget at any legal \`engage\`.
# \`relief\` starts at 0.8 and not lower for a different reason entirely: a
# pocket shallower than the 0.7 mm floor brick geometry is allowed to carry
# is refused by the kernel, art or not.
#
# Render:
#   bikar render patterns/Lego/Star-Brick.bkr --format stl --check -o StarBrick.stl
#     (STL = the printable brick; stderr = the anchor/grid gates and the
#      §6 validator warnings)
#   bikar render patterns/Lego/Star-Brick.bkr --format svg -o StarBrick.svg
#     (the art alone — the pattern check before plastic)
#
# Every dimension the clutch depends on is an unmeasured bet (CAL-RIB-01,
# coupon LG-F1). Print the coupon before trusting the fit.

param plates = 3 range 2..9 step 1
param engage = 3.2 range 1.6..4.0 step 0.2
param relief = 0.8 range 0.8..2.0 step 0.1

blueprint star_face
  circle C1 center(0,0) radius 12
  divide C1 into 8 offset 0

pattern star_relief on star_face
  connect every 3 on C1
  voids detect

brick StarBrick
  inscribe star_relief
  footprint auto
  height $plates plates
  studs none
  anchors auto
  engage $engage
  clutch auto
  relief depth $relief
  origin centered
`},{id:`edge-stud-tile`,title:`Edge-Stud Tile`,blurb:`6×6 with a perimeter stud ring and a rosette in the middle`,source:`# Edge-Stud-Tile — the third interface: studs on the perimeter cells only,
# with the art cut into the interior they enclose.
#
# \`studs none\` gives up stacking to carry a pattern and \`studs full\` gives up
# the pattern to stack (V4 will not let one face do both). \`studs edge\` is the
# partial answer available on a footprint big enough to have an interior: the
# ring of perimeter studs still takes a piece on top around the border, and
# the interior stays flat for relief. It is not free — anything laid across
# the middle bridges the art rather than clutching to it — but on a 6 × 6 the
# ring is 20 studs and the interior is a 4 × 4 field, which is 32 mm, which
# is where a radius-12 rosette fits with room to spare.
#
# Like \`Star-Brick\`, the art here is a single centred motif, so the scored
# grid gate reports \`n/a\` rather than a number: a one-off rosette has no
# repeat vectors to measure against the 8 mm lattice, and §5.3 says
# \`undefined\` for unmeasurable instead of scoring it zero. \`Grid-Field-Tile\`
# is the preset that gives that gate something to chew on.
#
# Render:
#   bikar render patterns/Lego/Edge-Stud-Tile.bkr --format stl --check -o EdgeStudTile.stl
#   bikar render patterns/Lego/Edge-Stud-Tile.bkr --format svg -o EdgeStudTile.svg
#
# Every dimension the clutch depends on is an unmeasured bet (CAL-RIB-01,
# coupon LG-F1). Print the coupon before trusting the fit.

param plates = 3 range 2..9 step 1
param engage = 3.2 range 1.6..4.0 step 0.2
param relief = 0.8 range 0.8..2.0 step 0.1

blueprint rosette_face
  circle C1 center(0,0) radius 12
  divide C1 into 12 offset 0

pattern rosette_relief on rosette_face
  connect every 5 on C1
  voids detect

brick EdgeStudTile
  inscribe rosette_relief
  footprint 6 x 6
  height $plates plates
  studs edge
  anchors auto
  engage $engage
  clutch auto
  relief depth $relief
  origin centered
`},{id:`grid-field-tile`,title:`Grid Field Tile`,blurb:`a tiled diamond field — drag the pitch and watch the grid gate score it`,source:`# Grid-Field-Tile — the preset that makes the *scored* gate say a number.
#
# Every other preset here inscribes a one-off motif, and a one-off motif has
# no repeat vectors, so §5.3's grid fit honestly reports \`n/a\` rather than a
# score of zero. This one tiles a motif on a square lattice of pitch \`pitch\`,
# which gives the gate two vectors to measure and the Lab a knob that moves
# the score: at \`pitch 8.0\` the art repeats exactly on the stud lattice and
# the fit is 1.0; drag it to 8.5 and the pattern walks off the studs a little
# more with every repeat.
#
# That is the whole point of scoring rather than passing/failing. A piece
# whose art does not register on the 8 mm grid is still printable and still
# clutches — the anchor gate is the one that can fail — but it cannot be
# extended by adding another one beside it without the pattern breaking at
# the seam. V8 warns below 0.8 and names the nearest sweet spot.
#
# Two circles, one drawn and one not: \`M\` carries the diamond that becomes
# the relief pocket, \`G\` exists only so the tiler has a pair of points a
# whole \`pitch\` apart to step by. \`M\` is deliberately smaller than half the
# pitch, so neighbouring pockets stay separated instead of meeting at a
# corner — a vertex-touching pocket pair is a T-junction the cell partition
# has to resolve, and there is no reason to hand it one on purpose.
#
# Render:
#   bikar render patterns/Lego/Grid-Field-Tile.bkr --format stl --check -o GridFieldTile.stl
#   bikar render patterns/Lego/Grid-Field-Tile.bkr --format svg -o GridFieldTile.svg
#
# Every dimension the clutch depends on is an unmeasured bet (CAL-RIB-01,
# coupon LG-F1). Print the coupon before trusting the fit.

param pitch = 8.0 range 6.0..12.0 step 0.1
param plates = 3 range 2..9 step 1
param engage = 3.2 range 1.6..4.0 step 0.2
param relief = 0.8 range 0.8..2.0 step 0.1

blueprint diamond_cell
  circle G center(0,0) radius $pitch / 2
  divide G into 4 offset 0
  circle M center(0,0) radius $pitch * 0.35
  divide M into 4 offset 0

pattern diamond_motif on diamond_cell
  connect cycle [M.cpt0 M.cpt1 M.cpt2 M.cpt3]

pattern diamond_field
  tile diamond_motif
    repeat_x 3
    repeat_y 3
    offset_col G.cpt2 G.cpt0
    offset_row G.cpt3 G.cpt1
    mode rectangular
  voids detect

brick GridFieldTile
  inscribe diamond_field
  footprint 5 x 5
  height $plates plates
  studs none
  anchors auto
  engage $engage
  clutch auto
  relief depth $relief
  origin centered
`},{id:`pin-rail`,title:`Pin Rail 1×8`,blurb:`the 1×n footprint class, which takes pins instead of tubes`,source:`# Pin-Rail — a 1 × 8 strip, the footprint class that gets *pins* instead of
# tubes.
#
# §3.3's census is a rule about shape, not size: a footprint needs two studs
# in both axes to have an interior vertex a tube can sit on, so anything
# \`1 × n\` takes solid pins between the studs of the host row and a \`1 × 1\`
# takes nothing at all. \`anchors auto\` picks; this preset exists so the
# picker's other branch is one click away in the Lab and shows up in the
# lattice overlay as pins on the row line rather than tubes on the grid
# crossings.
#
# A rail is also the piece where rotation lock is thinnest. Seven pins in a
# straight line resist twisting only through their own spacing, and the
# clutch is doing that work alone — there is no second row to triangulate
# against. Print it before assuming a long thin piece behaves like a brick.
#
# \`studs full\` keeps it stackable and, at 1 × 8, useful as an edge or a
# spacer. \`rows\` stops at 2 rather than 1: a 1 × 1 gets no anchor at all, so
# it fails §5.3's hard gate outright and V7 warns that a single stud cannot
# lock rotation — the degenerate end of the same fact, and not something to
# put a slider stop on top of.
#
# Render:
#   bikar render patterns/Lego/Pin-Rail.bkr --format stl --check -o PinRail.stl
#
# Every dimension the clutch depends on is an unmeasured bet (CAL-RIB-01,
# coupon LG-F1). Print the coupon before trusting the fit.

param rows = 8 range 2..12 step 1
param plates = 3 range 1..9 step 1
param engage = 3.2 range 1.6..4.0 step 0.2

brick PinRail
  footprint 1 x $rows
  height $plates plates
  studs full
  anchors auto
  engage $engage
  clutch auto
  origin centered
`},{id:`hex-field-tile`,title:`Hex Field Tile`,blurb:`Grid Field Tile on a hexagonal lattice — scores 0.48 and no knob fixes it`,source:`# Hex-Field-Tile — the preset where the grid gate is *right* to score low.
#
# This is \`Grid-Field-Tile\` with one word changed. Same diamond motif, same
# cell size, same footprint class, same knobs — \`mode hex\` instead of
# \`mode rectangular\`. Everything the two presets disagree about is the
# lattice, which is exactly what the 3d-models design doc's §5.3 says decides
# the score, so putting them side by side is the experiment.
#
# The square one scores 1.00 at \`pitch 8.0\`. This one scores 0.48 there, and
# the §5.3 sweep found a hexagonal basis tops out at 0.80 anywhere in
# 2..20 mm and never once reaches 1.0. No knob on this page fixes that.
#
# The reason is readable straight off the geometry. The tiler's hexagonal mode
# steps by \`(offsetX, 0)\` and \`(offsetX/2, offsetY)\` — the second vector
# staggers odd rows by half a column. At \`pitch 8.0\` the first vector is
# exactly one stud pitch, so that axis snaps dead on; the second carries an
# x-component of 4 mm, which is *half* a pitch, which is the furthest from a
# stud a point can get. One axis perfect, one axis maximally wrong, and
# rotating the whole lattice cannot improve one without spoiling the other.
# The 0.48 is the compromise, and the gate is reporting it honestly.
#
# \`H\`'s radius sets \`offsetY\` to \`pitch * sqrt(3)/2\`, the true hexagonal row
# height, so this is a real hexagonal lattice and not a squashed stand-in.
#
# What the preset is *for*: a piece that scores low here is still a correct,
# printable, clutching piece — V8 is a warning, not an error, because refusing
# it would delete the hexagonal and 5-fold families from the Lab entirely.
# What a low score costs is seamless extension: butt two of these edge to edge
# and the art breaks at the join. That is a trade to make knowingly, and this
# is where you see the number before making it.
#
# Render:
#   bikar render patterns/Lego/Hex-Field-Tile.bkr --format stl --check -o HexFieldTile.stl
#   bikar render patterns/Lego/Hex-Field-Tile.bkr --format svg -o HexFieldTile.svg
#
# Every dimension the clutch depends on is an unmeasured bet (CAL-RIB-01,
# coupon LG-F1). Print the coupon before trusting the fit.

param pitch = 8.0 range 6.0..12.0 step 0.1
param plates = 3 range 2..9 step 1
param engage = 3.2 range 1.6..4.0 step 0.2
param relief = 0.8 range 0.8..2.0 step 0.1

blueprint hex_cell
  circle G center(0,0) radius $pitch / 2
  divide G into 4 offset 0
  circle H center(0,0) radius $pitch * 0.4330127
  divide H into 4 offset 0
  circle M center(0,0) radius $pitch * 0.3
  divide M into 4 offset 0

pattern hex_motif on hex_cell
  connect cycle [M.cpt0 M.cpt1 M.cpt2 M.cpt3]

pattern hex_field
  tile hex_motif
    repeat_x 3
    repeat_y 3
    offset_col G.cpt2 G.cpt0
    offset_row H.cpt3 H.cpt1
    mode hex
  voids detect

brick HexFieldTile
  inscribe hex_field
  footprint 6 x 6
  height $plates plates
  studs none
  anchors auto
  engage $engage
  clutch auto
  relief depth $relief
  origin centered
`},{id:`rational-repeat-tile`,title:`Rational Repeat Tile`,blurb:`a 3 : 2 lattice that scores 1.00 — registering does not mean being square`,source:`# Rational-Repeat-Tile — a lattice that is not square and still lands perfectly.
#
# It is easy to read \`Grid-Field-Tile\` (square, scores 1.0) beside
# \`Hex-Field-Tile\` (hexagonal, never scores 1.0) and conclude that registering
# on the stud grid means being square. It does not. What the 3d-models design
# doc's §5.3 measures is the *ratio* of the two basis vectors, and any
# **rational** ratio lands at the right scale — this one is 3/2.
#
# The row vector is one and a half column vectors tall (\`R\`'s diameter is
# \`1.5 * pitch\`), so the lattice steps 1 : 1.5. At \`pitch 16.0\` that is
# 16 mm × 24 mm — two studs by three — and the gate reports fit 1.0 with a
# repeat unit of **3 × 2 studs**. Not a square cell, and a perfect score.
#
# This matters beyond the arithmetic. The design doc's v1 claimed 5-/10-fold
# designs can never register, which is false: those patterns are periodic and
# many of them have a rectangular repeat unit — Cromwell describes a decagonal
# design whose rose centres are opposite corners of a rectangle that repeats.
# The thing that actually blocks a lattice is an *irrational* ratio, and the
# irrational in the 5-fold case is cot 36° = 1.3764, not the golden ratio it is
# usually blamed on. A 10-fold motif on a rational rectangular repeat is a
# perfectly registerable brick.
#
# Drag \`pitch\` and watch the score fall off and come back: the sweet spots are
# periodic, not unique. That is the other thing this preset is here to show —
# a sweep window that happens to straddle none of them draws a flat curve for
# a lattice that registers exactly.
#
# Render:
#   bikar render patterns/Lego/Rational-Repeat-Tile.bkr --format stl --check -o RationalRepeatTile.stl
#   bikar render patterns/Lego/Rational-Repeat-Tile.bkr --format svg -o RationalRepeatTile.svg
#
# Every dimension the clutch depends on is an unmeasured bet (CAL-RIB-01,
# coupon LG-F1). Print the coupon before trusting the fit.

param pitch = 16.0 range 8.0..20.0 step 0.5
param plates = 3 range 2..9 step 1
param engage = 3.2 range 1.6..4.0 step 0.2
param relief = 0.8 range 0.8..2.0 step 0.1

blueprint ratio_cell
  circle G center(0,0) radius $pitch / 2
  divide G into 4 offset 0
  circle R center(0,0) radius $pitch * 0.75
  divide R into 4 offset 0
  circle M center(0,0) radius $pitch * 0.28
  divide M into 10 offset 0

pattern rose_motif on ratio_cell
  connect every 3 on M

pattern rose_field
  tile rose_motif
    repeat_x 3
    repeat_y 2
    offset_col G.cpt2 G.cpt0
    offset_row R.cpt3 R.cpt1
    mode rectangular
  voids detect

brick RationalRepeatTile
  inscribe rose_field
  footprint 8 x 8
  height $plates plates
  studs none
  anchors auto
  engage $engage
  clutch auto
  relief depth $relief
  origin centered
`},{id:`rosette-brick`,title:`Rosette Brick`,blurb:`footprint outline: the piece's silhouette is the rosette, only its anchors obey the grid`,source:`# Rosette-Brick — LG-B2's coupon: a ten-fold rosette (the five-fold girih
# family) whose *silhouette* is the piece, sitting on a square lattice it
# does not obey. The load-bearing bet of the anchor-only approach: a printed
# piece's outline need not follow the grid so long as its interface does.
#
# \`footprint outline\` takes the body from the pattern's face union — here
# the fully tiled rosette disc, whose boundary is the 20-vertex scalloped
# ring through the kite tips (radius R) and the mid-ring shoulders
# (~0.727·R). Measured on the shipped rosette corpus 2026-08-02: one
# edge-connected component (V19 passes by construction) and a sharpest
# convex angle of 72° at the tips — three times the ≈23.1° miter-clamp
# floor, so the V18 wall check passes with no cusp-rounding.
#
# There is deliberately no \`relief depth\`. On this piece the silhouette IS
# the art; a relief would union every bounded face into one pocket — the
# whole disc — and sink the entire top face uniformly, which is a recess,
# not a pattern.
#
# Coverage arithmetic, at the default radius 20: the body's closest
# approach to centre is the shoulder ring at ~14.5 mm; the 5×5 centred
# grid's centre cell and its four edge-neighbours have far corners at
# ≤ 12.7 mm, so five lattice cells are fully covered (the anchor gate
# needs two) and the tube anchors land in them. At the range floor of 18
# the same five cells clear by ~0.4 mm — below that the edge cells' far
# corners poke past the shoulders and the gate rightly refuses.
#
# Render:
#   bikar render patterns/Lego/Rosette-Brick.bkr --format stl --check -o RosetteBrick.stl
#   bikar render patterns/Lego/Rosette-Brick.bkr --format svg -o RosetteBrick.svg
#
# What the print settles (both registered, both LG-B2): CAL-ANC-01 — the
# retention ratio of an anchor-only body against a rectangular control at
# the same profile; CAL-INW-01 — printed integrity of the 1.5 mm inset
# cavity wall following a concave lobed outline. Until then every clutch
# number here is provisional.
#
# Construction is Rosette-10.bkr's wedge-and-rotate (after Sarah Brewer's
# 10-fold tutorial), parameterized: skip-3 chords of a decagon intersect in
# the inner (R/φ) and middle (~0.727·R) rings, and three rotated cycles —
# outer kites, inter-petal triangles, inner spokes — tile the disc.

param radius = 20 range 18..40 step 2
param plates = 3 range 2..6 step 1

blueprint rosette10
  circle C0 center(0,0) radius $radius
  divide C0 into 10

  line L0 from C0.cpt0 to C0.cpt3
  line L1 from C0.cpt1 to C0.cpt4
  line L2 from C0.cpt2 to C0.cpt5
  line L3 from C0.cpt3 to C0.cpt6
  line L4 from C0.cpt4 to C0.cpt7
  line L5 from C0.cpt5 to C0.cpt8
  line L6 from C0.cpt6 to C0.cpt9
  line L7 from C0.cpt7 to C0.cpt0
  line L8 from C0.cpt8 to C0.cpt1
  line L9 from C0.cpt9 to C0.cpt2

pattern rosette10 on rosette10
  # Outer petal kites — circumference to inner ring via mid-ring shoulders
  rotate 10 around C0.mpt
    connect cycle [C0.cpt0 L8_L0.cpt0 L9_L8.cpt0 L9_L7.cpt0]

  # Inter-petal triangles — fill gaps between kites at mid-ring level
  rotate 10 around C0.mpt
    connect cycle [L8_L0.cpt0 L9_L8.cpt0 L9_L0.cpt0]

  # Inner star spokes — inner ring to center, forms 10-pointed star
  rotate 10 around C0.mpt
    connect cycle [L9_L8.cpt0 C0.mpt L9_L0.cpt0]

  voids detect

brick RosetteBrick
  inscribe rosette10
  footprint outline
  height $plates plates
  studs none
  anchors auto
  clutch auto
  origin centered
`}],r=`classic-brick`;function i(e){return n.find(t=>t.id===e)}export{t as i,r as n,i as r,n as t};