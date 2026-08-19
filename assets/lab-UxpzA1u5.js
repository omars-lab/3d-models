import{C as e,S as t,_ as n,b as r,c as i,d as a,f as o,g as s,i as ee,l as te,m as ne,n as c,o as l,p as u,r as re,s as ie,t as ae,u as oe,x as se,y as ce}from"./style-ClcwKhJ5.js";import"./modulepreload-polyfill-CXK8biUa.js";import{i as le,n as ue,r as de}from"./worker-host-V6a3BZe7.js";var d=[{id:`rosette-dodeca`,title:`Rosette · Dodecahedron`,blurb:`10-petal rosettes on 12 pentagonal faces`,source:`# Rosette-Orb — dodecahedral 10-petal rosette sphere.
# Each of the 12 pentagonal faces carries a classical rosette: 10 kite
# petals reaching all 5 corners and all 5 edge midpoints (both shared
# with the neighboring faces, so the lattice closes watertight), joined
# shoulder-to-shoulder on a ring so their inner edges zigzag into a
# 10-pointed star core. 21 voids per face: 10 petals + 10 boundary
# cells + the pierced star core.
# Render with: bikar render Rosette-Orb.bkr --format stl -o out.stl
# Sweep a knob: bikar render Rosette-Orb.bkr --format stl --param inner=50 -o out.stl

# Ranges are the measured gate-PASS envelopes (2026-07 sweep at radius 60);
# keep inner below shoulder - 8 or the petals invert into bowties.
param radius = 60 range 40..110 step 5
param inner = 38 range 16..58 step 2
param shoulder = 60 range 48..76 step 2
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint pent_rosette
  # Face pentagon: circumradius 100, corners at 90 + k*72 deg CCW — the
  # canonical orb pattern frame.
  circle C0 center(0,0) radius 100
  divide C0 into 5 offset 90
  polygon pent [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3 C0.cpt4]
  # Midpoint-direction circle: rays at 54 + k*72 aim at edge midpoints.
  circle Cm center(0,0) radius 100
  divide Cm into 5 offset 54
  # Exact edge midpoint = edge chord x center ray (point R0_E4.cpt0).
  line E4 from C0.cpt4 to C0.cpt0
  line R0 from C0.mpt to Cm.cpt0
  # Inner ring (star core) and shoulder ring, 10 points each.
  circle C1 center(0,0) radius $inner
  divide C1 into 10 offset 18
  circle C2 center(0,0) radius $shoulder
  divide C2 into 10 offset 36

pattern pent_rosette on pent_rosette
  edges from pent
  rotate 5 around C0.mpt
    # Corner petal + midpoint petal; adjacent petals share shoulders.
    connect cycle [C0.cpt0 C2.cpt1 C1.cpt2 C2.cpt2]
    connect cycle [R0_E4.cpt0 C2.cpt0 C1.cpt1 C2.cpt1]
  voids detect

orb RosetteOrb
  base dodecahedron
  radius $radius
  inscribe pent_rosette
  project spherical
  struts width $strut_width depth $strut_depth
`,qiyasComposite:{cells:1,ribbons:null}},{id:`rosette-cube`,title:`Rosette · Cube`,blurb:`8-petal rosettes on 6 square faces`,source:`# Rosette-Cube-Orb — cubic 8-petal rosette sphere.
# The same rosette construction as Rosette-Orb on the cube's 6 square
# faces: 8 kite petals per face reaching all 4 corners and all 4 edge
# midpoints (both shared with the neighboring faces), joined
# shoulder-to-shoulder so their inner edges zigzag into an 8-pointed
# star core. 17 voids per face: 8 petals + 8 boundary cells + the
# pierced star core.
# Render with: bikar render Rosette-Cube-Orb.bkr --format stl -o out.stl

# Ring ranges carry over from the dodecahedral rosette sweep (same
# pattern-unit frame); keep inner below shoulder - 8 or the petals
# invert into bowties. The mesh gate backstops the square-face extremes.
param radius = 60 range 40..110 step 5
param inner = 38 range 16..58 step 2
param shoulder = 60 range 48..76 step 2
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint sq_rosette
  # Face square: circumradius 100, corners at 90 + k*90 deg CCW — the
  # canonical orb pattern frame.
  circle C0 center(0,0) radius 100
  divide C0 into 4 offset 90
  polygon sq [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3]
  # Midpoint-direction circle: rays at 45 + k*90 aim at edge midpoints.
  circle Cm center(0,0) radius 100
  divide Cm into 4 offset 45
  # Exact edge midpoint = edge chord x center ray (point R0_E3.cpt0).
  line E3 from C0.cpt3 to C0.cpt0
  line R0 from C0.mpt to Cm.cpt0
  # Inner ring (star core) and shoulder ring, 8 points each.
  circle C1 center(0,0) radius $inner
  divide C1 into 8 offset 0
  circle C2 center(0,0) radius $shoulder
  divide C2 into 8 offset 22.5

pattern sq_rosette on sq_rosette
  edges from sq
  rotate 4 around C0.mpt
    # Corner petal + midpoint petal; adjacent petals share shoulders.
    connect cycle [C0.cpt0 C2.cpt1 C1.cpt2 C2.cpt2]
    connect cycle [R0_E3.cpt0 C2.cpt0 C1.cpt1 C2.cpt1]
  voids detect

orb RosetteCubeOrb
  base cube
  radius $radius
  inscribe sq_rosette
  project spherical
  struts width $strut_width depth $strut_depth
`,qiyasComposite:{cells:1,ribbons:null}},{id:`rosette-weave`,title:`Rosette Weave · Dodecahedron`,blurb:`petals threaded into 10 interlaced chainmail ribbons`,source:`# Rosette-Weave-Orb — dodecahedral woven flower sphere (Family 1).
# Each pentagonal face carries only 5 midpoint kite petals chained
# through shoulders placed under the corners (no face-boundary edges and
# no corner petals — those would make odd-degree nodes, which cannot
# weave). Petals fuse across edge midpoints and around shoulder points,
# and strand tracing threads them into 10 closed ribbons that interlace
# alternately into a linked chainmail flower-ball: all 45 ribbon pairs
# have linking number 1, so nothing can be pulled off the assembly.
# Render with: bikar render Rosette-Weave-Orb.bkr --format stl -o out.stl

# Ring ranges stay inside the rosette sweet range — the weave adds parity
# and clearance constraints on top of the lattice's, so the envelope is
# narrower than the pierced rosettes'.
#
# Amplitude is measured, not derived. The old rule here — keep it at or
# above (strut_depth + 0.4) / 2 — is a statement about ribbon *centrelines*
# and ignores that a ribbon has width: the other ribbon's surface sits half
# a width off the crossing node, where the sinusoidal offset has already
# decayed, and the denser the crossing pattern the faster it decays. Under
# that rule 4 of the 5 woven orbs shipped interpenetrating. The value below
# is the first step that clears linkageGate's {CAL-CLR-01} 0.4mm body
# clearance floor, measured at 0.642mm; \`--check\` re-measures it, so change a
# strut dimension and re-run rather than re-deriving from a formula.
param radius = 60 range 40..110 step 5
param inner = 38 range 24..50 step 2
param shoulder = 60 range 48..70 step 2
param amplitude = 2.0 range 1.4..2.6 step 0.2
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint pent_flower
  # Canonical circumradius-100 pentagon frame (corners at 90 + k*72 CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 5 offset 90
  polygon pent [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3 C0.cpt4]
  # Midpoint-direction circle: rays at 54 + k*72 aim at edge midpoints.
  circle Cm center(0,0) radius 100
  divide Cm into 5 offset 54
  # Exact edge midpoint = edge chord x center ray (point R0_E4.cpt0).
  line E4 from C0.cpt4 to C0.cpt0
  line R0 from C0.mpt to Cm.cpt0
  # Inner ring under the midpoints; shoulder ring under the corners.
  circle C1 center(0,0) radius $inner
  divide C1 into 5 offset 54
  circle C2 center(0,0) radius $shoulder
  divide C2 into 5 offset 90

pattern pent_flower on pent_flower
  rotate 5 around C0.mpt
    connect cycle [R0_E4.cpt0 C2.cpt4 C1.cpt0 C2.cpt0]
  voids detect

orb RosetteWeaveOrb
  base dodecahedron
  radius $radius
  inscribe pent_flower
  project spherical
  struts width $strut_width depth $strut_depth
  weave crossing alternating amplitude $amplitude
`,qiyasComposite:{cells:1,ribbons:1}},{id:`hankin-dodeca`,title:`Hankin · Dodecahedron`,blurb:`polygons-in-contact stars — dial the contact angle`,source:`# Hankin-Orb — dodecahedral polygons-in-contact star sphere (Kaplan 2005,
# Bonner's Hankin method). Each pentagonal face launches two rays from
# every edge midpoint at the contact angle theta to the edge; adjacent
# rays intersect to form a five-pointed central star with kite cells at
# the corners. The contact points are the edge midpoints — shared with
# the neighboring face — so the lattice closes watertight across every
# edge for any theta in the calibrated range.
# Render with: bikar render Hankin-Orb.bkr --format stl -o out.stl
# Sweep the star: bikar render Hankin-Orb.bkr --format stl --param theta=36 -o out.stl

# theta detents worth trying: 36 (the pentagon's natural k*180/5 angle),
# 54 (ideal angle 90 - 180/5 — the classical balanced star, default),
# 72 (fat/obtuse family). Range 18..80 is the measured gate-PASS envelope
# across the full radius and strut-width ranges; outside it the corner
# kites collapse below the strut inset limit and the engine reports the
# degeneracy.
param radius = 60 range 40..110 step 5
param theta = 54 range 18..80 step 1
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint pent_hankin
  # Canonical circumradius-100 pentagon frame (corners at 90 + k*72 CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 5 offset 90
  polygon pent [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3 C0.cpt4]

pattern pent_pic on pent_hankin
  edges from pent
  hankin angle $theta on C0
  voids detect

orb HankinOrb
  base dodecahedron
  radius $radius
  inscribe pent_pic
  project spherical
  struts width $strut_width depth $strut_depth
  pierce voids
`,qiyasComposite:{cells:1,ribbons:null}},{id:`star-icosa`,title:`Star · Icosahedron`,blurb:`hexagrams on 20 triangular faces`,source:`# Star-Orb — icosahedral pierced-lattice sphere (the M0 spike, in DSL).
# Each of the 20 triangular faces carries a {6/2} hexagram whose
# alternating tips land exactly on the triangle's edge midpoints, so the
# lattice connects across every face boundary and the shell closes
# watertight. Render with: bikar render Star-Orb.bkr --format stl -o out.stl

# The hexagram circle stays at the fixed inradius 50 — its tips must land
# exactly on the edge midpoints or the cross-face weld fails — so the
# pattern itself has no knobs; only the print dimensions do.
param radius = 60 range 40..110 step 5
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint tri_face
  # Face triangle: circumradius 100, corners at 90/210/330 deg — the
  # canonical orb pattern frame (corners at 90 + k*120, CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 3 offset 90
  polygon tri [C0.cpt0 C0.cpt1 C0.cpt2]
  # Inradius circle: its 6 points are the 3 edge midpoints (at 30/150/270)
  # plus 3 points under the corners — the hexagram's tips.
  circle C1 center(0,0) radius 50
  divide C1 into 6 offset 30

pattern tri_star on tri_face
  edges from tri
  connect every 2 on C1
  voids detect

orb StarOrb
  base icosahedron
  radius $radius
  inscribe tri_star
  project spherical
  struts width $strut_width depth $strut_depth
`,qiyasComposite:{cells:1,ribbons:null}},{id:`star-dodeca`,title:`Star · Dodecahedron`,blurb:`corner-to-corner pentagrams on 12 pentagonal faces`,source:`# Dodeca-Orb — dodecahedral pierced-lattice sphere with a 5-fold star.
# Each of the 12 pentagonal faces (pattern circumradius 100, corners at
# 90 + k*72 deg CCW) carries a corner-to-corner pentagram {5/2}: every
# strut ends on a face corner or runs along a face edge, both shared with
# the neighboring faces, so the lattice closes watertight (11 voids per
# face: 5 star tips + 5 edge regions + the central pentagon).
# Render with: bikar render Dodeca-Orb.bkr --format stl -o out.stl

# The pentagram runs corner-to-corner on the fixed face frame, so the
# pattern itself has no knobs; only the print dimensions do.
param radius = 60 range 40..110 step 5
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint pent_face
  circle C0 center(0,0) radius 100
  divide C0 into 5 offset 90
  polygon pent [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3 C0.cpt4]

pattern pent_star on pent_face
  edges from pent
  connect every 2 on C0
  voids detect

orb DodecaOrb
  base dodecahedron
  radius $radius
  inscribe pent_star
  project spherical
  struts width $strut_width depth $strut_depth
`,qiyasComposite:{cells:1,ribbons:null}},{id:`star-cube`,title:`Star · Cube`,blurb:`{8/3} octagrams on 6 square faces`,source:`# Star-Cube-Orb — cubic pierced-lattice sphere with an {8/3} octagram.
# Each of the 6 square faces carries an eight-pointed star whose tips sit
# on the face's inradius circle: 4 land exactly on the edge midpoints
# (shared with the neighboring faces) and 4 under the corners, so the
# lattice closes watertight across every edge.
# Render with: bikar render Star-Cube-Orb.bkr --format stl -o out.stl

# The octagram circle stays at the fixed inradius 100*cos(45) — its
# midpoint tips must land exactly on the edge midpoints or the cross-face
# weld fails — so the pattern itself has no knobs; only the print
# dimensions do.
param radius = 60 range 40..110 step 5
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint sq_star_face
  # Canonical circumradius-100 square frame (corners at 90 + k*90 CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 4 offset 90
  polygon sq [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3]
  # Inradius circle: its 8 points are the 4 edge midpoints (at 45 + k*90)
  # plus 4 points under the corners — the octagram's tips.
  circle C1 center(0,0) radius 70.7106781187
  divide C1 into 8 offset 45

pattern sq_octagram on sq_star_face
  edges from sq
  connect every 3 on C1
  voids detect

orb StarCubeOrb
  base cube
  radius $radius
  inscribe sq_octagram
  project spherical
  struts width $strut_width depth $strut_depth
  pierce voids
`,qiyasComposite:{cells:1,ribbons:null}},{id:`star-octa`,title:`Star · Octahedron`,blurb:`bold hexagrams on 8 large triangular faces`,source:`# Star-Octa-Orb — octahedral pierced-lattice sphere with a {6/2} hexagram.
# The same canonical triangle-face hexagram as Star-Orb, on the
# octahedron's 8 faces: alternating tips land exactly on the triangle's
# edge midpoints, so the lattice connects across every face boundary and
# the shell closes watertight. Fewer, larger faces than the icosahedral
# Star-Orb give a bolder, more open star field.
# Render with: bikar render Star-Octa-Orb.bkr --format stl -o out.stl

# The hexagram circle stays at the fixed inradius 50 — its tips must land
# exactly on the edge midpoints or the cross-face weld fails — so the
# pattern itself has no knobs; only the print dimensions do.
param radius = 60 range 40..110 step 5
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint tri_face
  # Face triangle: circumradius 100, corners at 90/210/330 deg — the
  # canonical orb pattern frame (corners at 90 + k*120, CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 3 offset 90
  polygon tri [C0.cpt0 C0.cpt1 C0.cpt2]
  # Inradius circle: its 6 points are the 3 edge midpoints (at 30/150/270)
  # plus 3 points under the corners — the hexagram's tips.
  circle C1 center(0,0) radius 50
  divide C1 into 6 offset 30

pattern tri_star on tri_face
  edges from tri
  connect every 2 on C1
  voids detect

orb StarOctaOrb
  base octahedron
  radius $radius
  inscribe tri_star
  project spherical
  struts width $strut_width depth $strut_depth
  pierce voids
`,qiyasComposite:{cells:.992,ribbons:null}},{id:`star-tetra`,title:`Star · Tetrahedron`,blurb:`four quarter-sphere hexagrams — the minimal base`,source:`# Star-Tetra-Orb — tetrahedral pierced-lattice sphere with a {6/2} hexagram.
# The same canonical triangle-face hexagram as Star-Orb, on the
# tetrahedron's 4 faces: alternating tips land exactly on the triangle's
# edge midpoints, so the lattice connects across every face boundary and
# the shell closes watertight. The minimal base — 4 giant faces whose
# spherical projection stretches each star across a full quarter-sphere.
# Render with: bikar render Star-Tetra-Orb.bkr --format stl -o out.stl

# The hexagram circle stays at the fixed inradius 50 — its tips must land
# exactly on the edge midpoints or the cross-face weld fails — so the
# pattern itself has no knobs; only the print dimensions do.
param radius = 60 range 40..110 step 5
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint tri_face
  # Face triangle: circumradius 100, corners at 90/210/330 deg — the
  # canonical orb pattern frame (corners at 90 + k*120, CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 3 offset 90
  polygon tri [C0.cpt0 C0.cpt1 C0.cpt2]
  # Inradius circle: its 6 points are the 3 edge midpoints (at 30/150/270)
  # plus 3 points under the corners — the hexagram's tips.
  circle C1 center(0,0) radius 50
  divide C1 into 6 offset 30

pattern tri_star on tri_face
  edges from tri
  connect every 2 on C1
  voids detect

orb StarTetraOrb
  base tetrahedron
  radius $radius
  inscribe tri_star
  project spherical
  struts width $strut_width depth $strut_depth
  pierce voids
`,qiyasComposite:{cells:1,ribbons:null}},{id:`weave-icosa`,title:`Weave · Icosahedron`,blurb:`26 interlaced great-circle and triangle ribbons`,source:`# Weave-Orb — icosahedral woven-strapwork sphere (Family 1).
# Each face carries only the {6/2} hexagram (no face-boundary edges — those
# would make degree-6 nodes, which cannot weave). The hexagram's medial
# triangle connects the face's edge midpoints, so its edges run straight
# through into adjacent faces and close into 6 great-circle ribbons (the
# icosidodecahedron's equators); the other triangle stays interior, giving
# 20 small triangular ribbons. All 26 ribbons interlace alternately into
# a genuinely linked chainmail ball: every one of the 75 ribbon pairs has
# linking number 1, so nothing can be pulled off the assembly.
# Render with: bikar render Weave-Orb.bkr --format stl -o out.stl

# The hexagram circle stays at the fixed inradius 50 (tips must land on
# edge midpoints for cross-face closure).
#
# Amplitude is measured, not derived. The old rule here — keep it at or
# above (strut_depth + 0.4) / 2 — is a statement about ribbon *centrelines*
# and ignores that a ribbon has width: the other ribbon's surface sits half
# a width off the crossing node, where the sinusoidal offset has already
# decayed, and the denser the crossing pattern the faster it decays. Under
# that rule 4 of the 5 woven orbs shipped interpenetrating. The value below
# is the first step that clears linkageGate's {CAL-CLR-01} 0.4mm body
# clearance floor, measured at 0.438mm; \`--check\` re-measures it, so change a
# strut dimension and re-run rather than re-deriving from a formula.
param radius = 60 range 40..110 step 5
param amplitude = 2.6 range 1.4..3.0 step 0.2
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint tri_weave_face
  # Inradius circle of the canonical circumradius-100 triangle frame: its
  # 6 points are the 3 edge midpoints (at 30/150/270) plus 3 inner points
  # under the corners — the hexagram's vertices.
  circle C1 center(0,0) radius 50
  divide C1 into 6 offset 30

pattern tri_hexagram on tri_weave_face
  connect every 2 on C1

orb WeaveOrb
  base icosahedron
  radius $radius
  inscribe tri_hexagram
  project spherical
  struts width $strut_width depth $strut_depth
  weave crossing alternating amplitude $amplitude
`,qiyasComposite:{cells:.997,ribbons:1}},{id:`weave-dodeca`,title:`Weave · Dodecahedron`,blurb:`pentagram chords woven into chainmail ribbons`,source:`# Weave-Dodeca-Orb — dodecahedral woven pentagram sphere (Family 1).
# Each pentagonal face carries only a {5/2} pentagram connecting the 5
# edge midpoints (no face-boundary edges — those would make odd-degree
# nodes, which cannot weave). Midpoints are degree 2 in-face and weld to
# degree 4 across the edge, so strand tracing runs each chord straight
# through into the neighboring face, closing the lattice into ribbons
# that interlace alternately — a linked chainmail star-ball.
# Render with: bikar render Weave-Dodeca-Orb.bkr --format stl -o out.stl

# Amplitude is measured, not derived. The old rule here — keep it at or
# above (strut_depth + 0.4) / 2 — is a statement about ribbon *centrelines*
# and ignores that a ribbon has width: the other ribbon's surface sits half
# a width off the crossing node, where the sinusoidal offset has already
# decayed, and the denser the crossing pattern the faster it decays. Under
# that rule 4 of the 5 woven orbs shipped interpenetrating. The value below
# is the first step that clears linkageGate's {CAL-CLR-01} 0.4mm body
# clearance floor, measured at 0.408mm; \`--check\` re-measures it, so change a
# strut dimension and re-run rather than re-deriving from a formula.
param radius = 60 range 40..110 step 5
param amplitude = 2.2 range 1.4..2.6 step 0.2
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint pent_weave_face
  # Midpoint circle of the canonical circumradius-100 pentagon frame
  # (corners at 90 + k*72): inradius 100*cos(36), midpoints at 126 + k*72.
  circle C1 center(0,0) radius 80.9016994375
  divide C1 into 5 offset 126

pattern pent_pentagram on pent_weave_face
  connect every 2 on C1
  voids detect

orb WeaveDodecaOrb
  base dodecahedron
  radius $radius
  inscribe pent_pentagram
  project spherical
  struts width $strut_width depth $strut_depth
  weave crossing alternating amplitude $amplitude
  pierce voids
`,qiyasComposite:{cells:1,ribbons:1}},{id:`maclado-9`,title:`Maclado · Wheelfield`,blurb:`20 nine-spike wheels on the 3-fold axes, tip-to-tip`,source:`# Maclado-9 — the 9-spike "maclado" wheel field (Family 3).
# Ángel María Martín López's nine-fold wheel, placed by the divisor trick:
# a 9-point wheel is C3-invariant (3 | 9), so its centre may sit on a
# 3-fold icosahedral axis — the 20 dodecahedron vertices — and 120 = 3·40
# aligns one tip at all three neighbours at once, making the 30
# dodecahedral edges exact tip-to-tip joins with 12 congruent 30-gon
# fillers. See 3d-models docs/maclado-orb-design.md (§2, corrected).
# Render with: bikar render Maclado-9.bkr --format stl -o out.stl

# strut_width 3 degenerates at radius 60 — the derived cap half-angle
# (≈20.905°) gives unitMm ≈ 0.229, and width 3 insets the wheel's inner
# triangles past their inradius. The kernel throws rather than emit
# slivers, so the default and range here stay below that edge.
param radius = 60 range 40..110 step 5
param strut_width = 2 range 1.5..2.5 step 0.25 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

orb Maclado9
  base wheelfield
  radius $radius
  wheel points 9 contact 0.5
  place rule dodecahedral
  struts width $strut_width depth $strut_depth
`,qiyasComposite:{cells:1,ribbons:null}},{id:`maclado-9-weave`,title:`Maclado Weave · Wheelfield`,blurb:`the same field as 46 linked ribbon loops`,source:`# Maclado-9-Weave — the 9-spike maclado field as woven ribbons (Family 1
# treatment of the Family 3 field). The welded seam graph has 390
# degree-4 crossings and 120 degree-2 free tips; every strand closes with
# an even crossing count, so strict alternation is globally consistent —
# 46 linked ribbon loops. See 3d-models docs/maclado-orb-design.md §5.4.
# Render with: bikar render Maclado-9-Weave.bkr --format stl -o out.stl

# Ribbon 1.2/1.2 is the tested combination from the M4 field suite.
#
# Amplitude is measured, not derived. The old rule here — keep it at or
# above (ribbon_depth + 0.4) / 2 — is a statement about ribbon *centrelines*
# and ignores that a ribbon has width: the other ribbon's surface sits half
# a width off the crossing node, where the sinusoidal offset has already
# decayed, and the denser the crossing pattern the faster it decays. Under
# that rule 4 of the 5 woven orbs shipped interpenetrating. The value below
# is the first step that clears linkageGate's {CAL-CLR-01} 0.4mm body
# clearance floor, measured at 0.427mm; \`--check\` re-measures it, so change a
# strut dimension and re-run rather than re-deriving from a formula.
param radius = 60 range 40..110 step 5
param amplitude = 1.6 range 0.8..2.0 step 0.1
param ribbon_width = 1.2 range 0.8..2 step 0.1 advanced
param ribbon_depth = 1.2 range 0.8..2 step 0.1 advanced

orb Maclado9Weave
  base wheelfield
  radius $radius
  wheel points 9
  place rule dodecahedral
  struts width $ribbon_width depth $ribbon_depth
  weave crossing alternating amplitude $amplitude
`,qiyasComposite:{cells:1,ribbons:1}},{id:`maclado-9-overlap`,title:`Maclado Overlap · Wheelfield`,blurb:`wheels grown past tangency — rims cross and weave, 60 loops`,source:`# Maclado-9-Overlap — the welded woven-overlap orb (M4e, the D-032
# follow-on): the 9-spike field grown past tangency so adjacent rims
# CROSS, with ribbons woven over/under through the crossings — the
# maker's-reference interpenetrating regime, not the tangent join. The
# strand network has 420 degree-4 crossings (360 interior lattice + the
# 60 rim-crossing weld nodes) and 180 free tips; it decomposes into 60
# linked ribbon loops with globally consistent alternation. The kernel
# judges the overlap ratio against the D-032 instrument and refuses one
# whose crossings cannot weld (tangent touch at 1.0, fused weld nodes
# below ~1.15 or past ~1.25 at this ribbon width). See 3d-models
# docs/maclado-orb-design.md §5.2 and decision D-032.
# Render with: bikar render Maclado-9-Overlap.bkr --format stl -o out.stl

# Ribbon 1.2/1.2 is the tested combination from the M4e suite.
#
# Amplitude is measured, not derived. The old rule here — keep it at or
# above (ribbon_depth + 0.4) / 2 — is a statement about ribbon *centrelines*
# and ignores that a ribbon has width: the other ribbon's surface sits half
# a width off the crossing node, where the sinusoidal offset has already
# decayed, and the denser the crossing pattern the faster it decays. Under
# that rule 4 of the 5 woven orbs shipped interpenetrating. The value below
# is the first step that clears linkageGate's {CAL-CLR-01} 0.4mm body
# clearance floor, measured at 0.482mm; \`--check\` re-measures it, so change a
# strut dimension and re-run rather than re-deriving from a formula.
param radius = 60 range 40..110 step 5
param overlap = 1.2 range 1.15..1.25 step 0.01
param amplitude = 1.4 range 0.8..1.6 step 0.1
param ribbon_width = 1.2 range 0.8..2 step 0.1 advanced
param ribbon_depth = 1.2 range 0.8..2 step 0.1 advanced

orb Maclado9Overlap
  base wheelfield
  radius $radius
  wheel points 9
  place rule dodecahedral
  struts width $ribbon_width depth $ribbon_depth
  weave crossing alternating amplitude $amplitude
  overlap $overlap
`,qiyasComposite:{cells:null,ribbons:1}}],fe=`rosette-dodeca`;function f(e){return d.find(t=>t.id===e)}function p(e){let t=document.querySelector(e);if(!t)throw Error(`Orb Lab markup is missing ${e}`);return t}var m=p(`#knob-panel`),h=p(`#archetype-chips`),g=p(`#machine-select`),_=p(`#custom-dims`),v=p(`#dim-x`),y=p(`#dim-y`),b=p(`#dim-z`),pe=p(`#target-note`),me=p(`#process-note`),x=p(`#stl-button`),S=p(`#copy-link`),C=p(`#gate-panel`),w=p(`#error-panel`),he=p(`#spinner`),ge=p(`#spinner-label`),T=p(`#stop-button`),E=p(`#toast`),D=p(`#view-tabs`),_e=p(`#axis-view`),ve=p(`#orb-canvas`),ye=p(`#bake-button`),be=p(`#bkr-download`),xe=p(`#open-studio`),Se=p(`#drawer-hide`),Ce=new le(ve),O=Number(new URLSearchParams(window.location.search).get(`budgetMs`))||0,k=new ue({spawn:()=>new Worker(new URL(``+new URL(`worker-DTNAxfBf.js`,import.meta.url).href,``+import.meta.url),{type:`module`}),onMessage:e=>it(e),...O>0?{budgetMs:()=>O}:{}}),A=`preset`,j=fe,M=[],N=``,P={},F=new Set,I=n(),L=null,R=null,z=`3d`,we=``,B=null,V=0,H=0,Te=0,Ee=0,U=!1,De=0,Oe=0,W=0,G=0,ke=0;function K(e){E.textContent=e,E.hidden=!1,window.clearTimeout(ke),ke=window.setTimeout(()=>{E.hidden=!0},3600)}function Ae(){return A===`custom`?Z.getSource():(f(j)??d[0]).source}function q(){let e={};for(let t of F)P[t]!==void 0&&(e[t]=P[t]);return e}function J(){let e=Ae();V+=1,Te=V,ge.textContent=de(e)===6e4?`computing — this design is large, may take up to a minute…`:`computing…`,k.evaluate({type:`evaluate`,seq:V,source:e,params:q()}),window.clearTimeout(W),W=window.setTimeout(()=>{he.hidden=!1},300),window.clearTimeout(G),T.hidden=!0,G=window.setTimeout(()=>{T.hidden=!1},2300)}function je(){window.clearTimeout(W),window.clearTimeout(G),he.hidden=!0,T.hidden=!0}var Y=null;function X(e){if(A===`custom`){let t=Z.getSource();Y=c(`custom`,M,P,e,s(t)),oe(window.localStorage,l,{source:t,overrides:q()})}else Y=c(j,M,P,e);Re()}function Me(){r(m,M,P,{radiusCeilingMm:ce(I),onChange:Ne})}function Ne(e,n){P[e]=n,F.add(e),U=!1;let r=u(P,M);for(let e of r)F.add(e.name);r.length>0&&t(m,P),window.clearTimeout(De),De=window.setTimeout(()=>{J(),X(`replace`)},200)}function Pe(){window.clearTimeout(Oe),Oe=window.setTimeout(()=>{U=!1,Fe()},500)}var Z=new re({drawer:p(`#code-drawer`),textarea:p(`#code-editor`),gutter:p(`#editor-gutter`),toggle:p(`#code-toggle`),resizeHandle:p(`#drawer-resize`),onInput:Pe});function Fe(){let e=te(Z.getSource(),d);if(e){let t=A===`custom`||j!==e;A=`preset`,j=e,ie(window.localStorage,l),t&&Q(),X(`replace`)}else{let e=A===`preset`;A=`custom`,e&&Q(),X(e?`push`:`replace`)}J()}function Ie(){let e=q();if(Object.keys(e).length===0){K(`All knob values already match the code defaults`);return}let t=a(Z.getSource(),e);if(!t.ok){We(`Could not write the knob values into the code`,t.reason);return}let n=t.result;if(n.replacedExpressions.length>0){let e=n.replacedExpressions.join(`, `);if(!window.confirm(`Writing values will replace derived defaults (${e}) with plain numbers. Continue?`))return}F.clear(),Z.setSource(n.source),U=!1,Fe(),K(`Knob values written into the code`)}function Le(){let e=a(Z.getSource(),q());if(!e.ok){We(`Could not build the .bkr download`,e.reason);return}let t=new Blob([e.result.source],{type:`text/plain`}),n=URL.createObjectURL(t),r=document.createElement(`a`);r.href=n,r.download=`${A===`custom`?`custom-orb`:j}.bkr`,r.click(),URL.revokeObjectURL(n)}function Re(){if(xe.href=`${ee}#code/${s(Ae())}`,A===`custom`&&Y&&!Y.codeIncluded){S.disabled=!0,S.title=`Too large to share as a link (${Y.hrefLength} chars) — Download .bkr instead. Tip: trimming comments usually gets a script back under the line.`;return}S.disabled=!1,S.title=A===`custom`?`Anyone with this link gets your exact orb — the code rides in the URL`:``}function ze(t){if(t.family!==`weave`)return[];let n=[];t.strandCount!==null&&n.push([`ribbons`,`${t.strandCount} interlocked`]);let r=P.amplitude,i=e(P);if(r!==void 0&&i!==void 0){let e=2*r-i;n.push([`ribbon gap`,`${e.toFixed(1)} mm ${e>=.4?`✓`:`✗ fused`}`])}return n}function Be(e){let t=e.wall;if(!t)return[];let n=[[`wall`,`${t.name} · ${t.boundaryMm.width}×${t.boundaryMm.height} mm`],[`tiles`,`${t.fullCount} full`+(t.fragmentCount>0?`, ${t.fragmentCount} fragment`:``)+(t.droppedCount>0?`, ${t.droppedCount} dropped`:``)],[`module`,`${t.tile} · ${t.moduleSideMm} mm, pitch ${t.pitchMm} mm`]];return t.clips&&n.push([`clips`,`${t.clips.count} × CornerClip (${t.clips.material})`]),t.screwCount>0&&n.push([`screws`,`${t.screwCount} × keyhole`]),n}function Ve(){let e=document.createElement(`div`);if(e.className=`trust-badge`,A===`custom`)return e.classList.add(`custom`),e.textContent=`custom design — not qiyas-validated`,e.title=`The mesh gate above is the entire claim. To score a custom design offline: bikar render <file.bkr> --format views, then qiyas orb-validate on the output.`,e;let t=f(j)??d[0];if(t.qiyasComposite===null)return e.classList.add(`unvalidated`),e.textContent=`not yet qiyas-validated`,e.title=`A committed preset, but no qiyas score has been recorded for it — the mesh gate above is the entire claim.`,e;let n=[[`cells`,t.qiyasComposite.cells],[`ribbons`,t.qiyasComposite.ribbons]].flatMap(([e,t])=>typeof t==`number`?[[e,t]]:[]),r=Math.min(...n.map(([,e])=>e)).toFixed(3),i=n.map(([e,t])=>`${e} ${t.toFixed(3)}`).join(`, `);return[...F].every(e=>{let t=M.find(t=>t.name===e);return t===void 0||P[e]===t.defaultValue})?(e.classList.add(`validated`),e.textContent=`qiyas-validated ✓ ${r}`,e.title=`CI score of this committed script at declared defaults — ${i} (composite gate ≥ 0.95). The composite scores position and area against bikar's ground truth; it does not check shape types.`):(e.classList.add(`range`),e.textContent=`calibrated range`,e.title=`Knobs moved within the gate-swept envelope — the qiyas score (${i}) was measured at declared defaults.`),e}function He(e){let{gate:t,mesh:n}=e;C.textContent=``,C.dataset.tris=String(n.triangles.length);let r=e.family===`wall`,i=document.createElement(`div`);i.className=t.passed?`gate-badge pass`:`gate-badge fail`,i.textContent=t.passed?r?`PASS — module printable`:`PASS — printable`:`FAIL`,C.append(i,Ve());let a=[...Be(e),[`watertight`,t.watertight?`yes`:`NO`],[`triangles`,String(n.triangles.length)],[`volume`,`${(n.stats.volumeMm3/1e3).toFixed(1)} cm³`],[`min feature`,`${t.minFeatureMm.toFixed(2)} mm (declared ${t.declaredMinFeatureMm.toFixed(2)} mm)`],...ze(e)],o=document.createElement(`dl`);for(let[e,t]of a){let n=document.createElement(`dt`);n.textContent=e;let r=document.createElement(`dd`);r.textContent=t,o.append(n,r)}C.append(o);for(let e of t.failures){let t=document.createElement(`p`);t.className=`gate-failure`,t.textContent=e,C.append(t)}}function Ue(e){w.textContent=e,w.hidden=!1,x.disabled=!0}function We(e,t){w.textContent=`${e} — ${t}`,w.hidden=!1}function Ge(){V+=1,Ee=V,k.request({type:`views`,seq:V})}function Ke(){let e=B?.find(e=>e.id===z);e&&(_e.innerHTML=e.svg)}function qe(){if(B){Ke();return}Ge()}function Je(e){z=e;for(let t of D.querySelectorAll(`button`)){let n=t.dataset.view===e;t.classList.toggle(`active`,n),t.setAttribute(`aria-selected`,n?`true`:`false`)}let t=e===`3d`;ve.hidden=!t,_e.hidden=t,t||qe()}function Ye(e){D.textContent=``;let t=[{id:`3d`,label:`3D`,title:`Interactive preview — drag to rotate`},...e.map(e=>({id:e.id,label:e.id,title:`${e.fold}-fold symmetry axis — the view qiyas validates`}))];for(let e of t){let t=document.createElement(`button`);t.className=`view-tab`,t.dataset.view=e.id,t.setAttribute(`role`,`tab`),t.textContent=e.label,t.title=e.title,t.addEventListener(`click`,()=>Je(e.id)),D.append(t)}}function Xe(){let e=L===`weave`&&I.process===`fdm`;me.hidden=!e,e&&(me.textContent=`Interlocked ribbons print pre-assembled only on powder systems — pick an SLS/MJF service for this design, or print it as a keepsake that needs support surgery.`)}function Ze(e){L=e.family,B=null;let t=e.viewAxes.map(e=>e.id).join(`,`);t!==we&&(we=t,Ye(e.viewAxes)),Je(z===`3d`||e.viewAxes.some(e=>e.id===z)?z:`3d`),Xe()}function Qe(e){for(let t of e)t.dropped?(F.delete(t.name),delete P[t.name]):P[t.name]=t.to}function $e(){let e=u(P,M);if(e.length===0)return U=!1,0;for(let t of e)F.add(t.name);return U||(U=!0,J(),X(`replace`)),e.length}function et(){let e=M.map(e=>[e.name,e.min,e.max,e.step,e.advanced].join(`|`)).join(`;`);if(e!==N){N=e,Me();return}t(m,P)}function tt(e){M=e.specs,Qe(e.adjustments);for(let e of M)F.has(e.name)||(P[e.name]=e.value);let t=$e(),n=e.adjustments.length+t;n>0&&K(`Adjusted ${n} parameter${n===1?``:`s`} to printable values`),w.hidden=!0,R=e.wall?.tile??null,Ce.setMesh(e.mesh,e.wall?.instances),He(e),Ze(e),x.disabled=!e.gate.passed,et(),X(`replace`)}function nt(){let e=R?`${R}-module`:A===`custom`?`custom-orb`:j;for(let t of M){let n=P[t.name];n===void 0||n===t.defaultValue||(e+=`-${t.name}${String(Math.round(n*1e6)/1e6)}`)}return`${e}.stl`}function rt(e){let t=new Blob([e],{type:`model/stl`}),n=URL.createObjectURL(t),r=document.createElement(`a`);r.href=n,r.download=nt(),r.click(),URL.revokeObjectURL(n)}function it(e){if(e.type===`stl`){rt(e.data);return}if(e.type===`views`){e.seq===Ee&&(B=e.views,z!==`3d`&&Ke());return}if(!(e.type===`sweep`||e.type===`ldraw`)&&(e.seq===Te&&je(),!(e.seq<=H))){if(H=e.seq,e.type===`error`){Ue(e.message);return}tt(e)}}function at(e){if(A===`preset`&&e===j)return;let t=f(e)??d[0];A===`custom`&&!window.confirm(`Discard your custom orb and load ${t.title}? Your code is still at the previous link (Back button) until you edit again.`)||(A=`preset`,j=t.id,F.clear(),P={},M=[],N=``,U=!1,Z.setSource(t.source),Q(),c(j,[],{},`push`),J())}function Q(){h.textContent=``;for(let e of d){let t=document.createElement(`button`);t.className=A===`preset`&&e.id===j?`chip active`:`chip`,t.textContent=e.title,t.title=e.blurb,t.addEventListener(`click`,()=>at(e.id)),h.append(t)}if(A===`custom`){let e=document.createElement(`button`);e.className=`chip active`,e.textContent=`Custom orb`,e.title=`Your edited script — not one of the committed presets`,h.append(e)}Re()}function ot(){pe.textContent=`Largest printable radius: ${ce(I)} mm (${I.xMm}×${I.yMm}×${I.zMm} mm build volume, 10 mm margin)`}function st(){let e=(e,t)=>{let n=Number(e.value);return Number.isFinite(n)&&n>=50?n:t};return{xMm:e(v,256),yMm:e(y,256),zMm:e(b,256)}}function $(e){let t=o.find(t=>t.id===e)??o[0];_.hidden=t.id!==`custom`,I=t.id===`custom`?{...t,...st()}:t,se(I),ot(),Xe(),Me()}function ct(){for(let e of o){let t=document.createElement(`option`);t.value=e.id,t.textContent=e.label,g.append(t)}g.value=I.id,_.hidden=I.id!==`custom`,v.value=String(I.xMm),y.value=String(I.yMm),b.value=String(I.zMm),ot(),g.addEventListener(`change`,()=>$(g.value));for(let e of[v,y,b])e.addEventListener(`change`,()=>$(`custom`))}function lt(e){let t=0;for(let[n,r]of Object.entries(e)){let e=Number(r);if(!Number.isFinite(e)){t+=1;continue}P[n]=e,F.add(n)}t>0&&K(`Ignored ${t} non-numeric link value${t===1?``:`s`}`)}function ut(e){if(e!==null){let t=ne(e);if(t===null){K(`This share link is damaged — it may have been truncated by a chat app. Ask the sender for the .bkr file instead.`);return}A=`custom`,Z.setSource(t),Z.open();return}let t=i(window.localStorage,l);if(t){A=`custom`,Z.setSource(t.source),Z.open();for(let[e,n]of Object.entries(t.overrides))P[e]=n,F.add(e)}}function dt(e){if(e.scriptId===`custom`){ut(e.code);return}e.scriptId&&(f(e.scriptId)?j=e.scriptId:K(`Unknown design "${e.scriptId}" — showing the default`),e.code&&K(`This link names a preset — ignoring its embedded code`))}function ft(){let e=ae();dt(e),lt(e.rawParams),A===`preset`&&Z.setSource((f(j)??d[0]).source),Q(),ct(),x.addEventListener(`click`,()=>{V+=1,k.request({type:`stl`,seq:V})}),T.addEventListener(`click`,()=>k.stop()),S.addEventListener(`click`,()=>{navigator.clipboard.writeText(window.location.href).then(()=>K(`Link copied`),()=>K(`Could not copy — use the address bar`))}),ye.addEventListener(`click`,Ie),be.addEventListener(`click`,Le),Se.addEventListener(`click`,()=>Z.close()),window.addEventListener(`popstate`,()=>window.location.reload()),J()}ft();