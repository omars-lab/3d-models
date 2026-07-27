(function(){let e=document.createElement(`link`).relList;if(e&&e.supports&&e.supports(`modulepreload`))return;for(let e of document.querySelectorAll(`link[rel="modulepreload"]`))n(e);new MutationObserver(e=>{for(let t of e)if(t.type===`childList`)for(let e of t.addedNodes)e.tagName===`LINK`&&e.rel===`modulepreload`&&n(e)}).observe(document,{childList:!0,subtree:!0});function t(e){let t={};return e.integrity&&(t.integrity=e.integrity),e.referrerPolicy&&(t.referrerPolicy=e.referrerPolicy),e.crossOrigin===`use-credentials`?t.credentials=`include`:e.crossOrigin===`anonymous`?t.credentials=`omit`:t.credentials=`same-origin`,t}function n(e){if(e.ep)return;e.ep=!0;let n=t(e);fetch(e.href,n)}})();function e(e,t){return e.find(e=>e.name===t)}function t(t,n,r){if(!e(n,`inner`)||!e(n,`shoulder`)||t.inner===void 0||t.shoulder===void 0)return;let i=t.shoulder-8;t.inner<=i||(r.push({name:`inner`,from:t.inner,to:i,reason:`inner radius must stay 8 mm under the shoulder`}),t.inner=i)}function n(t,n,r){let i=e(n,`amplitude`);if(!i||!e(n,`strut_depth`)||t.amplitude===void 0||t.strut_depth===void 0)return;let a=(t.strut_depth+.4)/2,o=i.max===void 0?a:Math.min(a,i.max);t.amplitude>=o||(r.push({name:`amplitude`,from:t.amplitude,to:o,reason:`weave amplitude must clear the strut depth`}),t.amplitude=o)}function r(e,r){let i=[];return t(e,r,i),n(e,r,i),i}function i(e,t){let n={},r=[];for(let i of t){let t=e[i.name];if(t===void 0)continue;let a=Number(t);if(!Number.isFinite(a)){r.push({name:i.name,from:NaN,to:i.defaultValue,reason:`"${t}" is not a number — using the default`}),n[i.name]=i.defaultValue;continue}let o=a;i.min!==void 0&&(o=Math.max(i.min,o)),i.max!==void 0&&(o=Math.min(i.max,o)),o!==a&&r.push({name:i.name,from:a,to:o,reason:`clamped into the declared range`}),n[i.name]=o}return{values:n,adjustments:r}}function a(e){return e.name.replace(/_/g,` `)}function o(e){let t=e.min??Math.min(e.defaultValue/2,e.defaultValue-1),n=e.max??Math.max(e.defaultValue*2,e.defaultValue+1);return{min:t,max:n,step:e.step??Math.max(.1,Math.round((n-t)/100*10)/10)}}function s(e,t,n){let{min:r,max:i,step:s}=o(e),c=document.createElement(`div`);c.className=`knob-row`,c.dataset.knob=e.name;let l=document.createElement(`label`);l.textContent=a(e),l.htmlFor=`knob-${e.name}`;let u=document.createElement(`input`);u.type=`range`,u.id=`knob-${e.name}`,u.min=String(r),u.max=String(i),u.step=String(s),u.value=String(t);let d=document.createElement(`input`);d.type=`number`,d.setAttribute(`aria-label`,`${a(e)} value`),d.min=String(r),d.max=String(i),d.step=String(s),d.value=String(t);let f=document.createElement(`span`);if(f.className=`knob-chip`,f.hidden=!0,e.name===`radius`){let e=e=>{f.textContent=`exceeds your print target`,f.hidden=e<=n.radiusCeilingMm};e(t),c.dataset.radiusChip=`1`,u.addEventListener(`input`,()=>e(Number(u.value))),d.addEventListener(`input`,()=>e(Number(d.value)))}return u.addEventListener(`input`,()=>{d.value=u.value,n.onChange(e.name,Number(u.value))}),d.addEventListener(`change`,()=>{let t=Math.max(r,Math.min(i,Number(d.value)||e.defaultValue));d.value=String(t),u.value=String(t),n.onChange(e.name,t)}),c.append(l,u,d,f),c}function c(e,t,n,r){if(e.textContent=``,t.length===0){let t=document.createElement(`p`);t.className=`knob-empty`,t.textContent=`This script declares no knobs.`,e.append(t);return}let i=t.filter(e=>!e.advanced),a=t.filter(e=>e.advanced);for(let t of i)e.append(s(t,n[t.name]??t.value,r));if(a.length>0){let t=document.createElement(`details`);t.className=`knob-advanced`;let i=document.createElement(`summary`);i.textContent=`Advanced (${a.length})`,t.append(i);for(let e of a)t.append(s(e,n[e.name]??e.value,r));e.append(t)}}function l(e,t){for(let n of e.querySelectorAll(`.knob-row`)){let e=n.dataset.knob;if(!e||t[e]===void 0)continue;let r=n.querySelector(`input[type="range"]`),i=n.querySelector(`input[type="number"]`);r&&(r.value=String(t[e])),i&&(i.value=String(t[e]))}}var u=[{id:`bambu-x1c`,label:`Bambu Lab X1 Carbon (256³)`,xMm:256,yMm:256,zMm:256,process:`fdm`},{id:`bambu-p1s`,label:`Bambu Lab P1S (256³)`,xMm:256,yMm:256,zMm:256,process:`fdm`},{id:`bambu-a1`,label:`Bambu Lab A1 (256³)`,xMm:256,yMm:256,zMm:256,process:`fdm`},{id:`bambu-a1-mini`,label:`Bambu Lab A1 mini (180³)`,xMm:180,yMm:180,zMm:180,process:`fdm`},{id:`prusa-mk4s`,label:`Prusa MK4S (250×210×220)`,xMm:250,yMm:210,zMm:220,process:`fdm`},{id:`prusa-core-one`,label:`Prusa CORE One (250×220×270)`,xMm:250,yMm:220,zMm:270,process:`fdm`},{id:`ender-3`,label:`Creality Ender 3 (220×220×250)`,xMm:220,yMm:220,zMm:250,process:`fdm`},{id:`sls-service`,label:`SLS print service — nylon (300³)`,xMm:300,yMm:300,zMm:300,process:`powder`},{id:`mjf-service`,label:`MJF print service (380×284×380)`,xMm:380,yMm:284,zMm:380,process:`powder`},{id:`custom`,label:`Custom…`,xMm:256,yMm:256,zMm:256,process:`fdm`}];function d(e){return Math.floor((Math.min(e.xMm,e.yMm,e.zMm)-10)/2)}var f=`orbLab.printTarget`;function p(){try{let e=localStorage.getItem(f);if(e){let t=JSON.parse(e),n=u.find(e=>e.id===t.id);if(n&&n.id===`custom`)return{...n,xMm:typeof t.xMm==`number`?t.xMm:n.xMm,yMm:typeof t.yMm==`number`?t.yMm:n.yMm,zMm:typeof t.zMm==`number`?t.zMm:n.zMm};if(n)return n}}catch{}return u[0]}function m(e){try{localStorage.setItem(f,JSON.stringify(e))}catch{}}var h=[{id:`rosette-dodeca`,title:`Rosette · Dodecahedron`,blurb:`10-petal rosettes on 12 pentagonal faces`,source:`# Rosette-Orb — dodecahedral 10-petal rosette sphere.
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
`},{id:`rosette-cube`,title:`Rosette · Cube`,blurb:`8-petal rosettes on 6 square faces`,source:`# Rosette-Cube-Orb — cubic 8-petal rosette sphere.
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
`},{id:`rosette-weave`,title:`Rosette Weave · Dodecahedron`,blurb:`petals threaded into 10 interlaced chainmail ribbons`,source:`# Rosette-Weave-Orb — dodecahedral woven flower sphere (Family 1).
# Each pentagonal face carries only 5 midpoint kite petals chained
# through shoulders placed under the corners (no face-boundary edges and
# no corner petals — those would make odd-degree nodes, which cannot
# weave). Petals fuse across edge midpoints and around shoulder points,
# and strand tracing threads them into 10 closed ribbons that interlace
# alternately: amplitude 1.6 over a 2.4 ribbon depth leaves a 0.8mm
# clearance, so the print is a linked chainmail flower-ball.
# Render with: bikar render Rosette-Weave-Orb.bkr --format stl -o out.stl

# Ring ranges stay inside the rosette sweet range — the weave adds parity
# and clearance constraints on top of the lattice's, so the envelope is
# narrower than the pierced rosettes'. Keep amplitude at or above
# (strut_depth + 0.4) / 2: the mesh gate is per-tube and cannot see
# ribbon-ribbon interpenetration.
param radius = 60 range 40..110 step 5
param inner = 38 range 24..50 step 2
param shoulder = 60 range 48..70 step 2
param amplitude = 1.6 range 1.4..2.6 step 0.2
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
`},{id:`hankin-dodeca`,title:`Hankin · Dodecahedron`,blurb:`polygons-in-contact stars — dial the contact angle`,source:`# Hankin-Orb — dodecahedral polygons-in-contact star sphere (Kaplan 2005,
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
`},{id:`star-icosa`,title:`Star · Icosahedron`,blurb:`hexagrams on 20 triangular faces`,source:`# Star-Orb — icosahedral pierced-lattice sphere (the M0 spike, in DSL).
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
`},{id:`star-dodeca`,title:`Star · Dodecahedron`,blurb:`corner-to-corner pentagrams on 12 pentagonal faces`,source:`# Dodeca-Orb — dodecahedral pierced-lattice sphere with a 5-fold star.
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
`},{id:`star-cube`,title:`Star · Cube`,blurb:`{8/3} octagrams on 6 square faces`,source:`# Star-Cube-Orb — cubic pierced-lattice sphere with an {8/3} octagram.
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
`},{id:`star-octa`,title:`Star · Octahedron`,blurb:`bold hexagrams on 8 large triangular faces`,source:`# Star-Octa-Orb — octahedral pierced-lattice sphere with a {6/2} hexagram.
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
`},{id:`star-tetra`,title:`Star · Tetrahedron`,blurb:`four quarter-sphere hexagrams — the minimal base`,source:`# Star-Tetra-Orb — tetrahedral pierced-lattice sphere with a {6/2} hexagram.
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
`},{id:`weave-icosa`,title:`Weave · Icosahedron`,blurb:`26 interlaced great-circle and triangle ribbons`,source:`# Weave-Orb — icosahedral woven-strapwork sphere (Family 1).
# Each face carries only the {6/2} hexagram (no face-boundary edges — those
# would make degree-6 nodes, which cannot weave). The hexagram's medial
# triangle connects the face's edge midpoints, so its edges run straight
# through into adjacent faces and close into 6 great-circle ribbons (the
# icosidodecahedron's equators); the other triangle stays interior, giving
# 20 small triangular ribbons. All 26 ribbons interlace alternately:
# amplitude 1.6 over a 2.4 ribbon depth leaves a 0.8mm clearance, so the
# print is a genuinely linked chainmail ball, not a fused lattice.
# Render with: bikar render Weave-Orb.bkr --format stl -o out.stl

# The hexagram circle stays at the fixed inradius 50 (tips must land on
# edge midpoints for cross-face closure). Keep amplitude at or above
# (strut_depth + 0.4) / 2 — the mesh gate is per-tube and cannot see
# ribbon-ribbon interpenetration, so a too-small amplitude fuses the
# chainmail silently.
param radius = 60 range 40..110 step 5
param amplitude = 1.6 range 1.4..2.6 step 0.2
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
`},{id:`weave-dodeca`,title:`Weave · Dodecahedron`,blurb:`pentagram chords woven into chainmail ribbons`,source:`# Weave-Dodeca-Orb — dodecahedral woven pentagram sphere (Family 1).
# Each pentagonal face carries only a {5/2} pentagram connecting the 5
# edge midpoints (no face-boundary edges — those would make odd-degree
# nodes, which cannot weave). Midpoints are degree 2 in-face and weld to
# degree 4 across the edge, so strand tracing runs each chord straight
# through into the neighboring face, closing the lattice into ribbons
# that interlace alternately — a linked chainmail star-ball.
# Render with: bikar render Weave-Dodeca-Orb.bkr --format stl -o out.stl

# Keep amplitude at or above (strut_depth + 0.4) / 2 — the mesh gate is
# per-tube and cannot see ribbon-ribbon interpenetration, so a too-small
# amplitude fuses the chainmail silently.
param radius = 60 range 40..110 step 5
param amplitude = 1.6 range 1.4..2.6 step 0.2
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
`}],g=`rosette-dodeca`;function _(e){return h.find(t=>t.id===e)}function v(){let e=new URLSearchParams(window.location.search),t={},n=null;for(let[r,i]of e)if(r!==`v`){if(r===`f`){n=i;continue}t[r]=i}return{scriptId:n,rawParams:t}}function y(e){return String(Math.round(e*1e6)/1e6)}function b(e,t,n,r){let i=new URLSearchParams;i.set(`v`,`1`),i.set(`f`,e);for(let e of t){let t=n[e.name];t===void 0||t===e.defaultValue||i.set(e.name,y(t))}let a=`${window.location.pathname}?${i.toString()}`;r===`push`?history.pushState(null,``,a):history.replaceState(null,``,a)}var x=class{canvas;mesh=null;yaw=-.6;pitch=.35;zoom=1;frame=0;constructor(e){this.canvas=e,this.attachPointerHandlers(),this.attachWheelHandler(),window.addEventListener(`resize`,()=>{this.fitCanvas(),this.redraw()}),this.fitCanvas()}setMesh(e){this.mesh=e,this.redraw()}fitCanvas(){let e=window.devicePixelRatio||1,t=this.canvas.parentElement,n=Math.max(280,Math.min(720,(t?.clientWidth??640)-16,(t?.clientHeight??640)-16));this.canvas.width=Math.round(n*e),this.canvas.height=Math.round(n*e),this.canvas.style.width=`${n}px`,this.canvas.style.height=`${n}px`}redraw(){this.frame||=requestAnimationFrame(()=>{this.frame=0,this.draw()})}project(e){let t=Math.cos(this.yaw),n=Math.sin(this.yaw),r=Math.cos(this.pitch),i=Math.sin(this.pitch),a=e.vertices,o=a.length,s=new Float64Array(o),c=new Float64Array(o),l=new Float64Array(o),u=0;for(let e=0;e<o;e++){let o=a[e];u=Math.max(u,Math.hypot(o.x,o.y,o.z));let d=t*o.x+n*o.z,f=t*o.z-n*o.x;s[e]=d,c[e]=r*o.y-i*f,l[e]=i*o.y+r*f}return{xs:s,ys:c,zs:l,maxLen:u}}draw(){let e=this.mesh,t=this.canvas.getContext(`2d`);if(!e||!t)return;let n=this.canvas.width;t.clearRect(0,0,n,n);let{xs:r,ys:i,zs:a,maxLen:o}=this.project(e),s=n/2,c=(s-12)/(o||1)*this.zoom,l=e.triangles,u=new Float64Array(l.length);for(let e=0;e<l.length;e++){let[t,n,r]=l[e];u[e]=a[t]+a[n]+a[r]}let d=l.map((e,t)=>t);d.sort((e,t)=>u[e]-u[t]);let f=Math.hypot(.35,.55,.76),p=-.35/f,m=.55/f,h=.76/f;for(let e of d){let[n,o,u]=l[e],d=r[o]-r[n],f=i[o]-i[n],g=a[o]-a[n],_=r[u]-r[n],v=i[u]-i[n],y=a[u]-a[n],b=f*y-g*v,x=g*_-d*y,S=d*v-f*_,C=Math.hypot(b,x,S);if(C===0)continue;b/=C,x/=C,S/=C;let w=S>0,T=w?b*p+x*m+S*h:-(b*p+x*m+S*h),E=.4+.6*Math.max(0,T),D=w?`rgb(${Math.round(214*E)},${Math.round(178*E)},${Math.round(84*E)})`:`rgb(${Math.round(105*E)},${Math.round(82*E)},${Math.round(40*E)})`;t.beginPath(),t.moveTo(s+r[n]*c,s-i[n]*c),t.lineTo(s+r[o]*c,s-i[o]*c),t.lineTo(s+r[u]*c,s-i[u]*c),t.closePath(),t.fillStyle=D,t.strokeStyle=D,t.lineWidth=1,t.fill(),t.stroke()}}attachPointerHandlers(){let e=!1,t=0,n=0;this.canvas.addEventListener(`pointerdown`,r=>{e=!0,t=r.clientX,n=r.clientY,this.canvas.setPointerCapture(r.pointerId),this.canvas.classList.add(`dragging`)}),this.canvas.addEventListener(`pointermove`,r=>{e&&(this.yaw+=(r.clientX-t)*.01,this.pitch=Math.max(-1.5,Math.min(1.5,this.pitch+(r.clientY-n)*.01)),t=r.clientX,n=r.clientY,this.redraw())}),this.canvas.addEventListener(`pointerup`,t=>{e=!1,this.canvas.releasePointerCapture(t.pointerId),this.canvas.classList.remove(`dragging`)})}attachWheelHandler(){this.canvas.addEventListener(`wheel`,e=>{e.preventDefault(),this.zoom=Math.max(.4,Math.min(3,this.zoom*Math.exp(-e.deltaY*.0015))),this.redraw()},{passive:!1})}};function S(e){let t=document.querySelector(e);if(!t)throw Error(`Orb Lab markup is missing ${e}`);return t}var C=S(`#knob-panel`),w=S(`#archetype-chips`),T=S(`#machine-select`),E=S(`#custom-dims`),D=S(`#dim-x`),O=S(`#dim-y`),k=S(`#dim-z`),ee=S(`#target-note`),te=S(`#process-note`),A=S(`#stl-button`),ne=S(`#copy-link`),j=S(`#gate-panel`),M=S(`#error-panel`),re=S(`#spinner`),N=S(`#toast`),P=S(`#view-tabs`),F=S(`#axis-view`),I=S(`#orb-canvas`),ie=new x(I),L=new Worker(new URL(``+new URL(`worker-UrobqkPC.js`,import.meta.url).href,``+import.meta.url),{type:`module`}),R=g,z=[],B={},V=new Set,H=p(),U=null,W=`3d`,ae=``,G=null,K=0,oe=0,se=0,ce=0,q=null,J=!0,le=0,Y=0,ue=0;function X(e){N.textContent=e,N.hidden=!1,window.clearTimeout(ue),ue=window.setTimeout(()=>{N.hidden=!0},3600)}function Z(e){L.postMessage(e)}function de(){let e={};for(let t of V)B[t]!==void 0&&(e[t]=B[t]);return e}function Q(){let e=_(R)??h[0];K+=1,se=K,Z({type:`evaluate`,seq:K,source:e.source,params:de()}),window.clearTimeout(Y),Y=window.setTimeout(()=>{re.hidden=!1},300)}function fe(){window.clearTimeout(Y),re.hidden=!0}function pe(e){b(R,z,B,e)}function $(){c(C,z,B,{radiusCeilingMm:d(H),onChange:me})}function me(e,t){B[e]=t,V.add(e);let n=r(B,z);for(let e of n)V.add(e.name);n.length>0&&l(C,B),window.clearTimeout(le),le=window.setTimeout(()=>{Q(),pe(`replace`)},200)}function he(e){if(e.family!==`weave`)return[];let t=[];e.strandCount!==null&&t.push([`ribbons`,`${e.strandCount} interlocked`]);let n=B.amplitude,r=B.strut_depth;if(n!==void 0&&r!==void 0){let e=2*n-r;t.push([`ribbon gap`,`${e.toFixed(1)} mm ${e>=.4?`✓`:`✗ fused`}`])}return t}function ge(e){let{gate:t,mesh:n}=e;j.textContent=``;let r=document.createElement(`div`);r.className=t.passed?`gate-badge pass`:`gate-badge fail`,r.textContent=t.passed?`PASS — printable`:`FAIL`,j.append(r);let i=[[`watertight`,t.watertight?`yes`:`NO`],[`triangles`,String(n.triangles.length)],[`volume`,`${(n.stats.volumeMm3/1e3).toFixed(1)} cm³`],[`min feature`,`${t.minFeatureMm.toFixed(2)} mm (declared ${t.declaredMinFeatureMm.toFixed(2)} mm)`],...he(e)],a=document.createElement(`dl`);for(let[e,t]of i){let n=document.createElement(`dt`);n.textContent=e;let r=document.createElement(`dd`);r.textContent=t,a.append(n,r)}j.append(a);for(let e of t.failures){let t=document.createElement(`p`);t.className=`gate-failure`,t.textContent=e,j.append(t)}}function _e(e){M.textContent=e,M.hidden=!1,A.disabled=!0}function ve(){K+=1,ce=K,Z({type:`views`,seq:K})}function ye(){let e=G?.find(e=>e.id===W);e&&(F.innerHTML=e.svg)}function be(){if(G){ye();return}ve()}function xe(e){W=e;for(let t of P.querySelectorAll(`button`)){let n=t.dataset.view===e;t.classList.toggle(`active`,n),t.setAttribute(`aria-selected`,n?`true`:`false`)}let t=e===`3d`;I.hidden=!t,F.hidden=t,t||be()}function Se(e){P.textContent=``;let t=[{id:`3d`,label:`3D`,title:`Interactive preview — drag to rotate`},...e.map(e=>({id:e.id,label:e.id,title:`${e.fold}-fold symmetry axis — the view qiyas validates`}))];for(let e of t){let t=document.createElement(`button`);t.className=`view-tab`,t.dataset.view=e.id,t.setAttribute(`role`,`tab`),t.textContent=e.label,t.title=e.title,t.addEventListener(`click`,()=>xe(e.id)),P.append(t)}}function Ce(){let e=U===`weave`&&H.process===`fdm`;te.hidden=!e,e&&(te.textContent=`Interlocked ribbons print pre-assembled only on powder systems — pick an SLS/MJF service for this design, or print it as a keepsake that needs support surgery.`)}function we(e){U=e.family,G=null;let t=e.viewAxes.map(e=>e.id).join(`,`);t!==ae&&(ae=t,Se(e.viewAxes)),xe(W===`3d`||e.viewAxes.some(e=>e.id===W)?W:`3d`),Ce()}function Te(){let e=q??{};q=null,J=!1;let t=i(e,z);for(let[e,n]of Object.entries(t.values))B[e]=n,V.add(e);let n=r(B,z);for(let e of n)V.add(e.name);$();let a=t.adjustments.length+n.length;a>0&&X(`Adjusted ${a} parameter${a===1?``:`s`} to printable values`),pe(`replace`),V.size>0&&Q()}function Ee(e){z=e.specs;for(let e of z)V.has(e.name)||(B[e.name]=e.value);if(M.hidden=!0,ie.setMesh(e.mesh),ge(e),we(e),A.disabled=!e.gate.passed,q){Te();return}if(J){J=!1,$();return}l(C,B)}function De(){let e=R;for(let t of z){let n=B[t.name];n===void 0||n===t.defaultValue||(e+=`-${t.name}${String(Math.round(n*1e6)/1e6)}`)}return`${e}.stl`}function Oe(e){let t=new Blob([e],{type:`model/stl`}),n=URL.createObjectURL(t),r=document.createElement(`a`);r.href=n,r.download=De(),r.click(),URL.revokeObjectURL(n)}L.onmessage=e=>{let t=e.data;if(t.type===`stl`){Oe(t.data);return}if(t.type===`views`){t.seq===ce&&(G=t.views,W!==`3d`&&ye());return}if(t.seq===se&&fe(),!(t.seq<=oe)){if(oe=t.seq,t.type===`error`){_e(t.message);return}Ee(t)}};function ke(e){e!==R&&(R=e,V.clear(),B={},z=[],J=!0,Ae(),b(R,[],{},`push`),Q())}function Ae(){w.textContent=``;for(let e of h){let t=document.createElement(`button`);t.className=e.id===R?`chip active`:`chip`,t.textContent=e.title,t.title=e.blurb,t.addEventListener(`click`,()=>ke(e.id)),w.append(t)}}function je(){ee.textContent=`Largest printable radius: ${d(H)} mm (${H.xMm}×${H.yMm}×${H.zMm} mm build volume, 10 mm margin)`}function Me(){let e=(e,t)=>{let n=Number(e.value);return Number.isFinite(n)&&n>=50?n:t};return{xMm:e(D,256),yMm:e(O,256),zMm:e(k,256)}}function Ne(e){let t=u.find(t=>t.id===e)??u[0];E.hidden=t.id!==`custom`,H=t.id===`custom`?{...t,...Me()}:t,m(H),je(),Ce(),$()}function Pe(){for(let e of u){let t=document.createElement(`option`);t.value=e.id,t.textContent=e.label,T.append(t)}T.value=H.id,E.hidden=H.id!==`custom`,D.value=String(H.xMm),O.value=String(H.yMm),k.value=String(H.zMm),je(),T.addEventListener(`change`,()=>Ne(T.value));for(let e of[D,O,k])e.addEventListener(`change`,()=>Ne(`custom`))}function Fe(){let e=v();e.scriptId&&(_(e.scriptId)?R=e.scriptId:X(`Unknown design "${e.scriptId}" — showing the default`)),Object.keys(e.rawParams).length>0&&(q=e.rawParams),Ae(),Pe(),A.addEventListener(`click`,()=>{K+=1,Z({type:`stl`,seq:K})}),ne.addEventListener(`click`,()=>{navigator.clipboard.writeText(window.location.href).then(()=>X(`Link copied`),()=>X(`Could not copy — use the address bar`))}),window.addEventListener(`popstate`,()=>window.location.reload()),Q()}Fe();