import{C as e,S as t,_ as n,b as r,c as i,d as a,f as o,g as ee,h as te,i as ne,l as re,m as ie,n as s,o as c,p as l,r as ae,t as oe,u as se,v as ce,x as le,y as ue}from"./style-BFHcl7lz.js";import"./modulepreload-polyfill-EeOZK34R.js";import{a as de}from"./dist-C49kJYEf.js";import{i as fe,n as pe,r as me}from"./worker-host-DV2pcHZL.js";var he=``+new URL(`eight-fold-rosette-border-DUgt4Ipi.png`,import.meta.url).href,ge=``+new URL(`eight-fold-rosette-interlock-B4ob1Q3n.png`,import.meta.url).href,_e=``+new URL(`eight-fold-rosette-minimal-frame-zQY1eLPp.png`,import.meta.url).href,ve=``+new URL(`eight-fold-rosette-minimal-pegs-vu9luDfH.png`,import.meta.url).href,ye=``+new URL(`eight-fold-rosette-minimal-CBAJQCEy.png`,import.meta.url).href,be=``+new URL(`eight-fold-rosette-twist-D7Kn5b1M.png`,import.meta.url).href,xe=``+new URL(`eight-fold-rosette-KiB8H68R.png`,import.meta.url).href,Se=``+new URL(`lEfWSogWscs-BwSjxbcG.png`,import.meta.url).href,Ce=``+new URL(`n3IidKfXE1I-Cnh2XpDn.png`,import.meta.url).href,we=``+new URL(`nmEjCTzMbDg-weqxEiAh.png`,import.meta.url).href,Te=``+new URL(`rDuxHF3xMOc-DOIdouvw.png`,import.meta.url).href,Ee=``+new URL(`sDO9fpu76v8-CQv66w82.png`,import.meta.url).href,De=``+new URL(`six-fold-rosette-border-DMkpEXyM.png`,import.meta.url).href,Oe=``+new URL(`six-fold-rosette-interlock-BwfZEuiU.png`,import.meta.url).href,ke=``+new URL(`six-fold-rosette-minimal-frame-Cr7ozvJF.png`,import.meta.url).href,Ae=``+new URL(`six-fold-rosette-minimal-pegs-QUkhXGba.png`,import.meta.url).href,je=``+new URL(`six-fold-rosette-minimal-C_t2AgJg.png`,import.meta.url).href,Me=``+new URL(`six-fold-rosette-twist-BYtouvxi.png`,import.meta.url).href,Ne=``+new URL(`six-fold-rosette-DroUiSxX.png`,import.meta.url).href,Pe=``+new URL(`tA8eSdVx_EQ-CjFPN8nV.png`,import.meta.url).href,Fe=Object.assign({"./coaster-thumbs/eight-fold-rosette-border.png":he,"./coaster-thumbs/eight-fold-rosette-interlock.png":ge,"./coaster-thumbs/eight-fold-rosette-minimal-frame.png":_e,"./coaster-thumbs/eight-fold-rosette-minimal-pegs.png":ve,"./coaster-thumbs/eight-fold-rosette-minimal.png":ye,"./coaster-thumbs/eight-fold-rosette-twist.png":be,"./coaster-thumbs/eight-fold-rosette.png":xe,"./coaster-thumbs/lEfWSogWscs.png":Se,"./coaster-thumbs/n3IidKfXE1I.png":Ce,"./coaster-thumbs/nmEjCTzMbDg.png":we,"./coaster-thumbs/rDuxHF3xMOc.png":Te,"./coaster-thumbs/sDO9fpu76v8.png":Ee,"./coaster-thumbs/six-fold-rosette-border.png":De,"./coaster-thumbs/six-fold-rosette-interlock.png":Oe,"./coaster-thumbs/six-fold-rosette-minimal-frame.png":ke,"./coaster-thumbs/six-fold-rosette-minimal-pegs.png":Ae,"./coaster-thumbs/six-fold-rosette-minimal.png":je,"./coaster-thumbs/six-fold-rosette-twist.png":Me,"./coaster-thumbs/six-fold-rosette.png":Ne,"./coaster-thumbs/tA8eSdVx_EQ.png":Pe});function Ie(e){return Fe[`./coaster-thumbs/${e}.png`]}var Le=`Other patterns`;function Re(e){let t=new Map;for(let n of e){let[e,r]=n.title.split(` · `),i=t.get(e)??[];i.push({script:n,label:r??`plain`}),t.set(e,i)}let n=[],r=[];for(let[e,i]of t)i.length>1?n.push({heading:e,tiles:i}):r.push({script:i[0].script,label:i[0].script.title});return r.length>0&&n.push({heading:Le,tiles:r}),n}var u=[{id:`six-fold-rosette`,title:`Six-Fold Rosette`,blurb:`a hexagonal coaster carrying a six-fold star rosette in relief`,source:`# naqsh construction — GimTvN9hw4U
# title: Simple 20-step Six-Fold Star Rosette
# url: https://www.youtube.com/watch?v=GimTvN9hw4U
# steps: 26 statements, 25 tagged steps
# source: reconstructions/GimTvN9hw4U/construction.ggb-commands sha256:6838767cbb24116b0e5986e62e05a0726b246b8ce0028dc1714fc7194525022e
# renamed: rosette -> rosette_ (reserved word)

param size = 90 range 40..120   # mm, finished coaster span across flats — the print knob
param margin = 2 range 1..10   # mm, blank slab between the art and the edge
param unit = ($size - 2 * $margin) / 4.5001   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin

blueprint GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=00:43  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=00:59  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:15  C = Rotate(A, -120°, B)
  point C = rotate A by -120 around B
  # t=01:15  D = Rotate(B, -120°, C)
  point D = rotate B by -120 around C
  # t=01:15  E = Rotate(C, -120°, D)
  point E = rotate C by -120 around D
  # t=01:15  F = Rotate(D, -120°, E)
  point F = rotate D by -120 around E
  # ────────────────────────────────────────────────────────
  # t=01:31  poly1 = Polygon(A, B, C, D, E, F)
  polygon poly1 [ A B C D E F ]
  # ────────────────────────────────────────────────────────
  # t=01:39  l = PerpendicularBisector(A, B)
  bisector l from A to B
  # ────────────────────────────────────────────────────────
  # t=01:44  m = PerpendicularBisector(A, C)
  bisector m from A to C
  # ────────────────────────────────────────────────────────
  # t=01:51  G = Intersect(l, m)
  point G = intersect l m
  # ────────────────────────────────────────────────────────
  # t=01:54  f = Line(A, B)
  line f from A to B
  # ────────────────────────────────────────────────────────
  # t=01:57  H = Intersect(l, f)
  point H = intersect l f
  # ────────────────────────────────────────────────────────
  # t=02:00  c = Circle(B, H)
  circle c center(B) through H
  # ────────────────────────────────────────────────────────
  # t=02:08  I = Midpoint(A, C)
  point I = midpoint A C
  # ────────────────────────────────────────────────────────
  # t=02:36  n = Line(I, l)
  line n through I parallel l
  # ────────────────────────────────────────────────────────
  # t=02:53  p = Line(B, F)
  line p from B to F
  # ────────────────────────────────────────────────────────
  # t=03:07  J = Intersect(n, p)
  point J = intersect n p
  # ────────────────────────────────────────────────────────
  # t=03:14  np = Reflect(n, m)
  line np = reflect n across m
  # ────────────────────────────────────────────────────────
  # t=03:27  K = Intersect(l, np)
  point K = intersect l np
  # ────────────────────────────────────────────────────────
  # t=03:37  Ip = Reflect(I, l)
  point Ip = reflect I across l
  # ────────────────────────────────────────────────────────
  # t=03:41  Jp = Reflect(J, l)
  point Jp = reflect J across l
  # ────────────────────────────────────────────────────────
  # t=03:50  pet = Polygon(H, J, I, K, Ip, Jp)
  polygon pet [ H J I K Ip Jp ]
  # ────────────────────────────────────────────────────────
  # de = Line(D, E)
  line de from D to E
  # ────────────────────────────────────────────────────────
  # t=05:34  reflRosette = Reflect(rosette, de)
  point G_reflRosette = reflect G across de
  # t=05:34  reflRosette = Reflect(rosette, de)
  polygon pet_reflRosette = reflect pet across de

pattern GimTvN9hw4U on GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # t=05:18  rosette = Sequence(Rotate(pet, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    edges from pet
  # ────────────────────────────────────────────────────────
  # t=06:04  tess = Sequence(Rotate(reflRosette, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    rotate 6 around G_reflRosette
      edges from pet_reflRosette
  palette pal
    Slab = #333333
    Gold = #d4af37

coaster Coaster
  outline polygon 6 $size rotate 30
  inscribe GimTvN9hw4U
  base 4
  relief straps emboss 1.2
  strap width 2
  color base Slab
  color straps Gold
`},{id:`eight-fold-rosette`,title:`Eight-Fold Rosette`,blurb:`a square coaster carrying an eight-fold rosette in relief`,source:`# naqsh construction — 7apC5Q9QS-8
# title: Geogebra for Beginners 8-Fold Rosette Walkthrough
# url: https://www.youtube.com/watch?v=7apC5Q9QS-8
# steps: 144 statements, 144 tagged steps
# source: reconstructions/7apC5Q9QS-8/construction.ggb-commands sha256:aa7562d6e790f05ccd1a2e79b2cda43ec935fdc5561eb109896abbcb3265a8be

param size = 90 range 40..120   # mm, finished coaster side — the print knob
param margin = 2 range 1..10   # mm, blank slab between the art and the edge
param unit = ($size - 2 * $margin) / 4   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin
param pause1 = 1

blueprint c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=01:32  A = (0, 0)
  point A = unit.mpt
  # t=01:32  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:45  c = Circle(A, B)
  circle c center(A) through B
  # ────────────────────────────────────────────────────────
  # t=03:03  f = Line(A, B)
  line f from A to B
  # t=03:03  g = PerpendicularLine(A, f)
  line g through A perpendicular f
  # ────────────────────────────────────────────────────────
  # t=03:44  h = Rotate(f, 22.5°, A)
  line h = rotate f by 22.5 around A
  # t=03:44  i = Rotate(f, 45°, A)
  line i = rotate f by 45 around A
  # t=03:44  j = Rotate(f, 67.5°, A)
  line j = rotate f by 67.5 around A
  # t=03:44  k = Rotate(f, 112.5°, A)
  line k = rotate f by 112.5 around A
  # t=03:44  l = Rotate(f, 135°, A)
  line l = rotate f by 135 around A
  # t=03:44  m = Rotate(f, 157.5°, A)
  line m = rotate f by 157.5 around A
  # ────────────────────────────────────────────────────────
  # t=05:46  sqR = PerpendicularLine(B, f)
  line sqR through B perpendicular f
  # t=05:46  sqT = Rotate(sqR, 90°, A)
  line sqT = rotate sqR by 90 around A
  # t=05:46  sqL = Rotate(sqR, 180°, A)
  line sqL = rotate sqR by 180 around A
  # t=05:46  sqB = Rotate(sqR, 270°, A)
  line sqB = rotate sqR by 270 around A
  # t=05:46  P1 = Intersect(sqR, sqT)
  point P1 = intersect sqR sqT
  # t=05:46  P2 = Intersect(sqT, sqL)
  point P2 = intersect sqT sqL
  # t=05:46  P3 = Intersect(sqL, sqB)
  point P3 = intersect sqL sqB
  # t=05:46  P4 = Intersect(sqB, sqR)
  point P4 = intersect sqB sqR
  # t=05:46  sq = Polygon(P1, P2, P3, P4)
  polygon sq [ P1 P2 P3 P4 ]
  # ────────────────────────────────────────────────────────
  # t=06:50  D = (0, 1)
  point D = unit.cpt1
  # t=06:50  C = Intersect(k, sqT)
  point C = intersect k sqT
  # ────────────────────────────────────────────────────────
  # t=07:47  d = Circle(C, D)
  circle d center(C) through D
  # ────────────────────────────────────────────────────────
  # t=07:50  E = Intersect(d, k, 1)
  point E = intersect d k pick 1
  # ────────────────────────────────────────────────────────
  # t=08:24  p = Line(E, g)
  line p through E parallel g
  # ────────────────────────────────────────────────────────
  # t=09:20  p1 = Reflect(p, k)
  line p1 = reflect p across k
  # ────────────────────────────────────────────────────────
  # t=09:30  p2 = Reflect(p1, g)
  line p2 = reflect p1 across g
  # ────────────────────────────────────────────────────────
  # t=09:40  p3 = Reflect(p2, j)
  line p3 = reflect p2 across j
  # ────────────────────────────────────────────────────────
  # t=10:30  q = AngleBisector(D, C, E)
  line q = bisect angle D C E
  # ────────────────────────────────────────────────────────
  # t=10:50  p4 = Reflect(p, q)
  line p4 = reflect p across q
  # ────────────────────────────────────────────────────────
  # t=11:20  r = Reflect(p4, g)
  line r = reflect p4 across g
  # ────────────────────────────────────────────────────────
  # t=11:42  G = Intersect(p, p4)
  point G = intersect p p4
  # ────────────────────────────────────────────────────────
  # t=11:50  F = Intersect(p3, r)
  point F = intersect p3 r
  # ────────────────────────────────────────────────────────
  # t=11:56  H = Intersect(p1, p2)
  point H = intersect p1 p2
  # ────────────────────────────────────────────────────────
  # t=11:58  I = Intersect(p3, p2)
  point I = intersect p3 p2
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  polygon pet1 [ D G E H I F ]
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  polygon pet2 = reflect pet1 across j
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  polygon pet3 = reflect pet1 across i
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  polygon pet4 = reflect pet1 across h
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  polygon pet5 = reflect pet1 across f
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  polygon pet6 = reflect pet1 across m
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  polygon pet7 = reflect pet1 across l
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  polygon pet8 = reflect pet1 across k
  # ────────────────────────────────────────────────────────
  # t=13:15  L1 = Reflect(p4, l)
  line L1 = reflect p4 across l
  # ────────────────────────────────────────────────────────
  # t=13:20  O1 = Intersect(L1, sqT)
  point O1 = intersect L1 sqT
  # t=13:20  O2 = Intersect(L1, p4)
  point O2 = intersect L1 p4
  # t=13:20  O3 = Intersect(p4, sqL)
  point O3 = intersect p4 sqL
  # ────────────────────────────────────────────────────────
  # t=13:29  oct1 = Polygon(P2, O1, O2, O3)
  polygon oct1 [ P2 O1 O2 O3 ]
  # ────────────────────────────────────────────────────────
  # t=13:40  H2 = Rotate(H, 45°, A)
  point H2 = rotate H by 45 around A
  # t=13:40  H3 = Rotate(H, 90°, A)
  point H3 = rotate H by 90 around A
  # t=13:40  H4 = Rotate(H, 135°, A)
  point H4 = rotate H by 135 around A
  # t=13:40  H5 = Rotate(H, 180°, A)
  point H5 = rotate H by 180 around A
  # t=13:40  H6 = Rotate(H, 225°, A)
  point H6 = rotate H by 225 around A
  # t=13:40  H7 = Rotate(H, 270°, A)
  point H7 = rotate H by 270 around A
  # t=13:40  H8 = Rotate(H, 315°, A)
  point H8 = rotate H by 315 around A
  # ────────────────────────────────────────────────────────
  # t=13:52  pL1 = Reflect(p1, f)
  line pL1 = reflect p1 across f
  # ────────────────────────────────────────────────────────
  # t=13:56  pL2 = Reflect(p2, f)
  line pL2 = reflect p2 across f
  # ────────────────────────────────────────────────────────
  # t=14:00  pH1 = Reflect(p, i)
  line pH1 = reflect p across i
  # ────────────────────────────────────────────────────────
  # t=14:02  pH2 = Reflect(p3, i)
  line pH2 = reflect p3 across i
  # ────────────────────────────────────────────────────────
  # t=14:09  T22 = Intersect(h, p1)
  point T22 = intersect h p1
  # t=14:09  T67 = Intersect(j, p1)
  point T67 = intersect j p1
  # t=14:09  T112 = Intersect(k, p2)
  point T112 = intersect k p2
  # t=14:09  T157 = Intersect(m, p2)
  point T157 = intersect m p2
  # ────────────────────────────────────────────────────────
  # t=14:14  T202 = Intersect(h, pL2)
  point T202 = intersect h pL2
  # t=14:14  T247 = Intersect(j, pL2)
  point T247 = intersect j pL2
  # t=14:14  T292 = Intersect(k, pL1)
  point T292 = intersect k pL1
  # t=14:14  T337 = Intersect(m, pL1)
  point T337 = intersect m pL1
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  polygon star [ H T112 H2 T157 H3 T202 H4 T247 H5 T292 H6 T337 H7 T22 H8 T67 ]
  # ────────────────────────────────────────────────────────
  # t=14:43  oct2 = Reflect(oct1, g)
  polygon oct2 = reflect oct1 across g
  # ────────────────────────────────────────────────────────
  # t=15:10  oct3 = Reflect(oct1, f)
  polygon oct3 = reflect oct1 across f
  # ────────────────────────────────────────────────────────
  # t=15:15  oct4 = Reflect(oct2, f)
  polygon oct4 = reflect oct2 across f
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  polygon petN1 = reflect pet1 across sqT
  # t=19:05  petN2 = Reflect(pet2, sqT)
  polygon petN2 = reflect pet2 across sqT
  # t=19:05  petN8 = Reflect(pet8, sqT)
  polygon petN8 = reflect pet8 across sqT
  # t=19:05  petN3 = Reflect(pet3, sqT)
  polygon petN3 = reflect pet3 across sqT
  # t=19:05  petN7 = Reflect(pet7, sqT)
  polygon petN7 = reflect pet7 across sqT
  # t=19:05  starN = Reflect(star, sqT)
  polygon starN = reflect star across sqT
  # t=19:05  octN1 = Reflect(oct1, sqT)
  polygon octN1 = reflect oct1 across sqT
  # t=19:05  octN2 = Reflect(oct2, sqT)
  polygon octN2 = reflect oct2 across sqT
  # t=19:05  Bl = Rotate(B, 180°, A)
  point Bl = rotate B by 180 around A
  # t=19:05  Fa = Rotate(G, 270°, A)
  point Fa = rotate G by 270 around A
  # t=19:05  Fb = Rotate(F, 90°, A)
  point Fb = rotate F by 90 around A
  # t=19:05  I3 = Rotate(I, 90°, A)
  point I3 = rotate I by 90 around A
  # t=19:05  I8 = Rotate(I, 315°, A)
  point I8 = rotate I by 315 around A
  # t=19:05  petT3 = Polygon(B, Fa, I8, H7)
  polygon petT3 [ B Fa I8 H7 ]
  # t=19:05  petT7 = Polygon(Bl, Fb, I3, H3)
  polygon petT7 [ Bl Fb I3 H3 ]
  # t=19:05  starT = Polygon(H7, T22, H8, T67, H, T112, H2, T157, H3)
  polygon starT [ H7 T22 H8 T67 H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  polygon starNh = reflect starT across sqT
  # t=19:24  petN3h = Reflect(petT3, sqT)
  polygon petN3h = reflect petT3 across sqT
  # t=19:24  petN7h = Reflect(petT7, sqT)
  polygon petN7h = reflect petT7 across sqT
  # ────────────────────────────────────────────────────────
  # t=20:06  petL1 = Polygon(D, G, E, H)
  polygon petL1 [ D G E H ]
  # t=20:06  starQ2 = Polygon(A, H, T112, H2, T157, H3)
  polygon starQ2 [ A H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  polygon petW1 = reflect petN1 across l
  # t=20:54  petW2 = Reflect(petN2, l)
  polygon petW2 = reflect petN2 across l
  # t=20:54  petW8 = Reflect(petN8, l)
  polygon petW8 = reflect petN8 across l
  # t=20:54  petW3h = Reflect(petN3h, l)
  polygon petW3h = reflect petN3h across l
  # t=20:54  petW7h = Reflect(petN7h, l)
  polygon petW7h = reflect petN7h across l
  # t=20:54  starWh = Reflect(starNh, l)
  polygon starWh = reflect starNh across l
  # t=20:54  octW1 = Reflect(octN1, l)
  polygon octW1 = reflect octN1 across l
  # t=20:54  octW2 = Reflect(octN2, l)
  polygon octW2 = reflect octN2 across l
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  polygon petE1 = reflect petN1 across i
  # t=21:04  petE2 = Reflect(petN2, i)
  polygon petE2 = reflect petN2 across i
  # t=21:04  petE8 = Reflect(petN8, i)
  polygon petE8 = reflect petN8 across i
  # t=21:04  petE3h = Reflect(petN3h, i)
  polygon petE3h = reflect petN3h across i
  # t=21:04  petE7h = Reflect(petN7h, i)
  polygon petE7h = reflect petN7h across i
  # t=21:04  starEh = Reflect(starNh, i)
  polygon starEh = reflect starNh across i
  # t=21:04  octE1 = Reflect(octN1, i)
  polygon octE1 = reflect octN1 across i
  # t=21:04  octE2 = Reflect(octN2, i)
  polygon octE2 = reflect octN2 across i
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  polygon petS1 = reflect petN1 across f
  # t=21:35  petS2 = Reflect(petN2, f)
  polygon petS2 = reflect petN2 across f
  # t=21:35  petS8 = Reflect(petN8, f)
  polygon petS8 = reflect petN8 across f
  # t=21:35  petS3h = Reflect(petN3h, f)
  polygon petS3h = reflect petN3h across f
  # t=21:35  petS7h = Reflect(petN7h, f)
  polygon petS7h = reflect petN7h across f
  # t=21:35  starSh = Reflect(starNh, f)
  polygon starSh = reflect starNh across f
  # t=21:35  octS1 = Reflect(octN1, f)
  polygon octS1 = reflect octN1 across f
  # t=21:35  octS2 = Reflect(octN2, f)
  polygon octS2 = reflect octN2 across f
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  polygon petNW1 = rotate pet8 by 180 around P2
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  polygon petNW7h = rotate petT7 by 180 around P2
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  polygon petNW1h = rotate petL1 by 180 around P2
  # t=21:57  octNW = Rotate(oct1, 180°, P2)
  polygon octNW = rotate oct1 by 180 around P2
  # t=21:57  starNWh = Reflect(starNh, sqL)
  polygon starNWh = reflect starNh across sqL
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  polygon starNWq = rotate starQ2 by 180 around P2
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  polygon petNE1 = reflect petNW1 across g
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  polygon petNE7h = reflect petNW7h across g
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  polygon petNE1h = reflect petNW1h across g
  # t=22:44  octNE = Reflect(octNW, g)
  polygon octNE = reflect octNW across g
  # t=22:44  starNEq = Reflect(starNWq, g)
  polygon starNEq = reflect starNWq across g
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  polygon petSW1 = reflect petNW1 across f
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  polygon petSW7h = reflect petNW7h across f
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  polygon petSW1h = reflect petNW1h across f
  # t=22:58  octSW = Reflect(octNW, f)
  polygon octSW = reflect octNW across f
  # t=22:58  starSWq = Reflect(starNWq, f)
  polygon starSWq = reflect starNWq across f
  # t=22:58  petSE1 = Reflect(petNE1, f)
  polygon petSE1 = reflect petNE1 across f
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  polygon petSE7h = reflect petNE7h across f
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  polygon petSE1h = reflect petNE1h across f
  # t=22:58  octSE = Reflect(octNE, f)
  polygon octSE = reflect octNE across f
  # t=22:58  starSEq = Reflect(starNEq, f)
  polygon starSEq = reflect starNEq across f
  # ────────────────────────────────────────────────────────
  # t=23:10  Q0 = Reflect(O1, g)
  point Q0 = reflect O1 across g
  # t=23:10  Q1 = Reflect(O2, g)
  point Q1 = reflect O2 across g
  # t=23:10  octA = Polygon(O2, O1, 8)
  polygon octA = regular 8 from O2 to O1
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  polygon octB = regular 8 from Q0 to Q1
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  polygon octC = reflect octA across f
  # t=23:19  octD = Reflect(octB, f)
  polygon octD = reflect octB across f

pattern c_7apC5Q9QS_8 on c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  edges from pet1
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  edges from pet2
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  edges from pet3
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  edges from pet4
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  edges from pet5
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  edges from pet6
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  edges from pet7
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  edges from pet8
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  edges from star
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  edges from petN1
  # t=19:05  petN2 = Reflect(pet2, sqT)
  edges from petN2
  # t=19:05  petN8 = Reflect(pet8, sqT)
  edges from petN8
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  edges from starNh
  # t=19:24  petN3h = Reflect(petT3, sqT)
  edges from petN3h
  # t=19:24  petN7h = Reflect(petT7, sqT)
  edges from petN7h
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  edges from petW1
  # t=20:54  petW2 = Reflect(petN2, l)
  edges from petW2
  # t=20:54  petW8 = Reflect(petN8, l)
  edges from petW8
  # t=20:54  petW3h = Reflect(petN3h, l)
  edges from petW3h
  # t=20:54  petW7h = Reflect(petN7h, l)
  edges from petW7h
  # t=20:54  starWh = Reflect(starNh, l)
  edges from starWh
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  edges from petE1
  # t=21:04  petE2 = Reflect(petN2, i)
  edges from petE2
  # t=21:04  petE8 = Reflect(petN8, i)
  edges from petE8
  # t=21:04  petE3h = Reflect(petN3h, i)
  edges from petE3h
  # t=21:04  petE7h = Reflect(petN7h, i)
  edges from petE7h
  # t=21:04  starEh = Reflect(starNh, i)
  edges from starEh
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  edges from petS1
  # t=21:35  petS2 = Reflect(petN2, f)
  edges from petS2
  # t=21:35  petS8 = Reflect(petN8, f)
  edges from petS8
  # t=21:35  petS3h = Reflect(petN3h, f)
  edges from petS3h
  # t=21:35  petS7h = Reflect(petN7h, f)
  edges from petS7h
  # t=21:35  starSh = Reflect(starNh, f)
  edges from starSh
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  edges from petNW1
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  edges from petNW7h
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  edges from petNW1h
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  edges from starNWq
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  edges from petNE1
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  edges from petNE7h
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  edges from petNE1h
  # t=22:44  starNEq = Reflect(starNWq, g)
  edges from starNEq
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  edges from petSW1
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  edges from petSW7h
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  edges from petSW1h
  # t=22:58  starSWq = Reflect(starNWq, f)
  edges from starSWq
  # t=22:58  petSE1 = Reflect(petNE1, f)
  edges from petSE1
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  edges from petSE7h
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  edges from petSE1h
  # t=22:58  starSEq = Reflect(starNEq, f)
  edges from starSEq
  # ────────────────────────────────────────────────────────
  # t=23:10  octA = Polygon(O2, O1, 8)
  edges from octA
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  edges from octB
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  edges from octC
  # t=23:19  octD = Reflect(octB, f)
  edges from octD
  palette pal
    Slab = #333333
    Gold = #d4af37

coaster Coaster
  outline square $size
  inscribe c_7apC5Q9QS_8
  base 4
  relief straps emboss 1.2
  strap width 2
  color base Slab
  color straps Gold
`},{id:`six-fold-rosette-interlock`,title:`Six-Fold Rosette · interlock`,blurb:`the hexagonal six-fold coaster with dovetail tabs and slots so a set tiles edge to edge`,source:`# naqsh construction — GimTvN9hw4U
# title: Simple 20-step Six-Fold Star Rosette
# url: https://www.youtube.com/watch?v=GimTvN9hw4U
# steps: 26 statements, 25 tagged steps
# source: reconstructions/GimTvN9hw4U/construction.ggb-commands sha256:6838767cbb24116b0e5986e62e05a0726b246b8ce0028dc1714fc7194525022e
# renamed: rosette -> rosette_ (reserved word)

param size = 90 range 40..120   # mm, finished coaster span across flats — the print knob
param neck = 3 range 2..5   # mm, dovetail neck at the edge line
param depth = 3 range 2..5   # mm, how far the tab protrudes / the slot cuts in
param clearance = 0.15 range 0.05..0.35   # mm, CAL-FIT-01 ladder: snug .. free
param margin = 2 + $depth + $clearance   # mm, the plain 2 mm border plus what the slot eats
param unit = ($size - 2 * $margin) / 4.5001   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin

blueprint GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=00:43  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=00:59  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:15  C = Rotate(A, -120°, B)
  point C = rotate A by -120 around B
  # t=01:15  D = Rotate(B, -120°, C)
  point D = rotate B by -120 around C
  # t=01:15  E = Rotate(C, -120°, D)
  point E = rotate C by -120 around D
  # t=01:15  F = Rotate(D, -120°, E)
  point F = rotate D by -120 around E
  # ────────────────────────────────────────────────────────
  # t=01:31  poly1 = Polygon(A, B, C, D, E, F)
  polygon poly1 [ A B C D E F ]
  # ────────────────────────────────────────────────────────
  # t=01:39  l = PerpendicularBisector(A, B)
  bisector l from A to B
  # ────────────────────────────────────────────────────────
  # t=01:44  m = PerpendicularBisector(A, C)
  bisector m from A to C
  # ────────────────────────────────────────────────────────
  # t=01:51  G = Intersect(l, m)
  point G = intersect l m
  # ────────────────────────────────────────────────────────
  # t=01:54  f = Line(A, B)
  line f from A to B
  # ────────────────────────────────────────────────────────
  # t=01:57  H = Intersect(l, f)
  point H = intersect l f
  # ────────────────────────────────────────────────────────
  # t=02:00  c = Circle(B, H)
  circle c center(B) through H
  # ────────────────────────────────────────────────────────
  # t=02:08  I = Midpoint(A, C)
  point I = midpoint A C
  # ────────────────────────────────────────────────────────
  # t=02:36  n = Line(I, l)
  line n through I parallel l
  # ────────────────────────────────────────────────────────
  # t=02:53  p = Line(B, F)
  line p from B to F
  # ────────────────────────────────────────────────────────
  # t=03:07  J = Intersect(n, p)
  point J = intersect n p
  # ────────────────────────────────────────────────────────
  # t=03:14  np = Reflect(n, m)
  line np = reflect n across m
  # ────────────────────────────────────────────────────────
  # t=03:27  K = Intersect(l, np)
  point K = intersect l np
  # ────────────────────────────────────────────────────────
  # t=03:37  Ip = Reflect(I, l)
  point Ip = reflect I across l
  # ────────────────────────────────────────────────────────
  # t=03:41  Jp = Reflect(J, l)
  point Jp = reflect J across l
  # ────────────────────────────────────────────────────────
  # t=03:50  pet = Polygon(H, J, I, K, Ip, Jp)
  polygon pet [ H J I K Ip Jp ]
  # ────────────────────────────────────────────────────────
  # de = Line(D, E)
  line de from D to E
  # ────────────────────────────────────────────────────────
  # t=05:34  reflRosette = Reflect(rosette, de)
  point G_reflRosette = reflect G across de
  # t=05:34  reflRosette = Reflect(rosette, de)
  polygon pet_reflRosette = reflect pet across de

pattern GimTvN9hw4U on GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # t=05:18  rosette = Sequence(Rotate(pet, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    edges from pet
  # ────────────────────────────────────────────────────────
  # t=06:04  tess = Sequence(Rotate(reflRosette, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    rotate 6 around G_reflRosette
      edges from pet_reflRosette

coaster Coaster
  outline polygon 6 $size rotate 30
  inscribe GimTvN9hw4U
  base 4
  relief straps emboss 1.2
  strap width 2
  interlock dovetail $neck $depth clearance $clearance
`},{id:`eight-fold-rosette-interlock`,title:`Eight-Fold Rosette · interlock`,blurb:`the square eight-fold coaster with dovetail tabs and slots so a set tiles edge to edge`,source:`# naqsh construction — 7apC5Q9QS-8
# title: Geogebra for Beginners 8-Fold Rosette Walkthrough
# url: https://www.youtube.com/watch?v=7apC5Q9QS-8
# steps: 144 statements, 144 tagged steps
# source: reconstructions/7apC5Q9QS-8/construction.ggb-commands sha256:aa7562d6e790f05ccd1a2e79b2cda43ec935fdc5561eb109896abbcb3265a8be

param size = 90 range 40..120   # mm, finished coaster side — the print knob
param neck = 3 range 2..5   # mm, dovetail neck at the edge line
param depth = 3 range 2..5   # mm, how far the tab protrudes / the slot cuts in
param clearance = 0.15 range 0.05..0.35   # mm, CAL-FIT-01 ladder: snug .. free
param margin = 2 + $depth + $clearance   # mm, the plain 2 mm border plus what the slot eats
param unit = ($size - 2 * $margin) / 4   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin
param pause1 = 1

blueprint c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=01:32  A = (0, 0)
  point A = unit.mpt
  # t=01:32  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:45  c = Circle(A, B)
  circle c center(A) through B
  # ────────────────────────────────────────────────────────
  # t=03:03  f = Line(A, B)
  line f from A to B
  # t=03:03  g = PerpendicularLine(A, f)
  line g through A perpendicular f
  # ────────────────────────────────────────────────────────
  # t=03:44  h = Rotate(f, 22.5°, A)
  line h = rotate f by 22.5 around A
  # t=03:44  i = Rotate(f, 45°, A)
  line i = rotate f by 45 around A
  # t=03:44  j = Rotate(f, 67.5°, A)
  line j = rotate f by 67.5 around A
  # t=03:44  k = Rotate(f, 112.5°, A)
  line k = rotate f by 112.5 around A
  # t=03:44  l = Rotate(f, 135°, A)
  line l = rotate f by 135 around A
  # t=03:44  m = Rotate(f, 157.5°, A)
  line m = rotate f by 157.5 around A
  # ────────────────────────────────────────────────────────
  # t=05:46  sqR = PerpendicularLine(B, f)
  line sqR through B perpendicular f
  # t=05:46  sqT = Rotate(sqR, 90°, A)
  line sqT = rotate sqR by 90 around A
  # t=05:46  sqL = Rotate(sqR, 180°, A)
  line sqL = rotate sqR by 180 around A
  # t=05:46  sqB = Rotate(sqR, 270°, A)
  line sqB = rotate sqR by 270 around A
  # t=05:46  P1 = Intersect(sqR, sqT)
  point P1 = intersect sqR sqT
  # t=05:46  P2 = Intersect(sqT, sqL)
  point P2 = intersect sqT sqL
  # t=05:46  P3 = Intersect(sqL, sqB)
  point P3 = intersect sqL sqB
  # t=05:46  P4 = Intersect(sqB, sqR)
  point P4 = intersect sqB sqR
  # t=05:46  sq = Polygon(P1, P2, P3, P4)
  polygon sq [ P1 P2 P3 P4 ]
  # ────────────────────────────────────────────────────────
  # t=06:50  D = (0, 1)
  point D = unit.cpt1
  # t=06:50  C = Intersect(k, sqT)
  point C = intersect k sqT
  # ────────────────────────────────────────────────────────
  # t=07:47  d = Circle(C, D)
  circle d center(C) through D
  # ────────────────────────────────────────────────────────
  # t=07:50  E = Intersect(d, k, 1)
  point E = intersect d k pick 1
  # ────────────────────────────────────────────────────────
  # t=08:24  p = Line(E, g)
  line p through E parallel g
  # ────────────────────────────────────────────────────────
  # t=09:20  p1 = Reflect(p, k)
  line p1 = reflect p across k
  # ────────────────────────────────────────────────────────
  # t=09:30  p2 = Reflect(p1, g)
  line p2 = reflect p1 across g
  # ────────────────────────────────────────────────────────
  # t=09:40  p3 = Reflect(p2, j)
  line p3 = reflect p2 across j
  # ────────────────────────────────────────────────────────
  # t=10:30  q = AngleBisector(D, C, E)
  line q = bisect angle D C E
  # ────────────────────────────────────────────────────────
  # t=10:50  p4 = Reflect(p, q)
  line p4 = reflect p across q
  # ────────────────────────────────────────────────────────
  # t=11:20  r = Reflect(p4, g)
  line r = reflect p4 across g
  # ────────────────────────────────────────────────────────
  # t=11:42  G = Intersect(p, p4)
  point G = intersect p p4
  # ────────────────────────────────────────────────────────
  # t=11:50  F = Intersect(p3, r)
  point F = intersect p3 r
  # ────────────────────────────────────────────────────────
  # t=11:56  H = Intersect(p1, p2)
  point H = intersect p1 p2
  # ────────────────────────────────────────────────────────
  # t=11:58  I = Intersect(p3, p2)
  point I = intersect p3 p2
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  polygon pet1 [ D G E H I F ]
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  polygon pet2 = reflect pet1 across j
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  polygon pet3 = reflect pet1 across i
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  polygon pet4 = reflect pet1 across h
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  polygon pet5 = reflect pet1 across f
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  polygon pet6 = reflect pet1 across m
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  polygon pet7 = reflect pet1 across l
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  polygon pet8 = reflect pet1 across k
  # ────────────────────────────────────────────────────────
  # t=13:15  L1 = Reflect(p4, l)
  line L1 = reflect p4 across l
  # ────────────────────────────────────────────────────────
  # t=13:20  O1 = Intersect(L1, sqT)
  point O1 = intersect L1 sqT
  # t=13:20  O2 = Intersect(L1, p4)
  point O2 = intersect L1 p4
  # t=13:20  O3 = Intersect(p4, sqL)
  point O3 = intersect p4 sqL
  # ────────────────────────────────────────────────────────
  # t=13:29  oct1 = Polygon(P2, O1, O2, O3)
  polygon oct1 [ P2 O1 O2 O3 ]
  # ────────────────────────────────────────────────────────
  # t=13:40  H2 = Rotate(H, 45°, A)
  point H2 = rotate H by 45 around A
  # t=13:40  H3 = Rotate(H, 90°, A)
  point H3 = rotate H by 90 around A
  # t=13:40  H4 = Rotate(H, 135°, A)
  point H4 = rotate H by 135 around A
  # t=13:40  H5 = Rotate(H, 180°, A)
  point H5 = rotate H by 180 around A
  # t=13:40  H6 = Rotate(H, 225°, A)
  point H6 = rotate H by 225 around A
  # t=13:40  H7 = Rotate(H, 270°, A)
  point H7 = rotate H by 270 around A
  # t=13:40  H8 = Rotate(H, 315°, A)
  point H8 = rotate H by 315 around A
  # ────────────────────────────────────────────────────────
  # t=13:52  pL1 = Reflect(p1, f)
  line pL1 = reflect p1 across f
  # ────────────────────────────────────────────────────────
  # t=13:56  pL2 = Reflect(p2, f)
  line pL2 = reflect p2 across f
  # ────────────────────────────────────────────────────────
  # t=14:00  pH1 = Reflect(p, i)
  line pH1 = reflect p across i
  # ────────────────────────────────────────────────────────
  # t=14:02  pH2 = Reflect(p3, i)
  line pH2 = reflect p3 across i
  # ────────────────────────────────────────────────────────
  # t=14:09  T22 = Intersect(h, p1)
  point T22 = intersect h p1
  # t=14:09  T67 = Intersect(j, p1)
  point T67 = intersect j p1
  # t=14:09  T112 = Intersect(k, p2)
  point T112 = intersect k p2
  # t=14:09  T157 = Intersect(m, p2)
  point T157 = intersect m p2
  # ────────────────────────────────────────────────────────
  # t=14:14  T202 = Intersect(h, pL2)
  point T202 = intersect h pL2
  # t=14:14  T247 = Intersect(j, pL2)
  point T247 = intersect j pL2
  # t=14:14  T292 = Intersect(k, pL1)
  point T292 = intersect k pL1
  # t=14:14  T337 = Intersect(m, pL1)
  point T337 = intersect m pL1
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  polygon star [ H T112 H2 T157 H3 T202 H4 T247 H5 T292 H6 T337 H7 T22 H8 T67 ]
  # ────────────────────────────────────────────────────────
  # t=14:43  oct2 = Reflect(oct1, g)
  polygon oct2 = reflect oct1 across g
  # ────────────────────────────────────────────────────────
  # t=15:10  oct3 = Reflect(oct1, f)
  polygon oct3 = reflect oct1 across f
  # ────────────────────────────────────────────────────────
  # t=15:15  oct4 = Reflect(oct2, f)
  polygon oct4 = reflect oct2 across f
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  polygon petN1 = reflect pet1 across sqT
  # t=19:05  petN2 = Reflect(pet2, sqT)
  polygon petN2 = reflect pet2 across sqT
  # t=19:05  petN8 = Reflect(pet8, sqT)
  polygon petN8 = reflect pet8 across sqT
  # t=19:05  petN3 = Reflect(pet3, sqT)
  polygon petN3 = reflect pet3 across sqT
  # t=19:05  petN7 = Reflect(pet7, sqT)
  polygon petN7 = reflect pet7 across sqT
  # t=19:05  starN = Reflect(star, sqT)
  polygon starN = reflect star across sqT
  # t=19:05  octN1 = Reflect(oct1, sqT)
  polygon octN1 = reflect oct1 across sqT
  # t=19:05  octN2 = Reflect(oct2, sqT)
  polygon octN2 = reflect oct2 across sqT
  # t=19:05  Bl = Rotate(B, 180°, A)
  point Bl = rotate B by 180 around A
  # t=19:05  Fa = Rotate(G, 270°, A)
  point Fa = rotate G by 270 around A
  # t=19:05  Fb = Rotate(F, 90°, A)
  point Fb = rotate F by 90 around A
  # t=19:05  I3 = Rotate(I, 90°, A)
  point I3 = rotate I by 90 around A
  # t=19:05  I8 = Rotate(I, 315°, A)
  point I8 = rotate I by 315 around A
  # t=19:05  petT3 = Polygon(B, Fa, I8, H7)
  polygon petT3 [ B Fa I8 H7 ]
  # t=19:05  petT7 = Polygon(Bl, Fb, I3, H3)
  polygon petT7 [ Bl Fb I3 H3 ]
  # t=19:05  starT = Polygon(H7, T22, H8, T67, H, T112, H2, T157, H3)
  polygon starT [ H7 T22 H8 T67 H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  polygon starNh = reflect starT across sqT
  # t=19:24  petN3h = Reflect(petT3, sqT)
  polygon petN3h = reflect petT3 across sqT
  # t=19:24  petN7h = Reflect(petT7, sqT)
  polygon petN7h = reflect petT7 across sqT
  # ────────────────────────────────────────────────────────
  # t=20:06  petL1 = Polygon(D, G, E, H)
  polygon petL1 [ D G E H ]
  # t=20:06  starQ2 = Polygon(A, H, T112, H2, T157, H3)
  polygon starQ2 [ A H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  polygon petW1 = reflect petN1 across l
  # t=20:54  petW2 = Reflect(petN2, l)
  polygon petW2 = reflect petN2 across l
  # t=20:54  petW8 = Reflect(petN8, l)
  polygon petW8 = reflect petN8 across l
  # t=20:54  petW3h = Reflect(petN3h, l)
  polygon petW3h = reflect petN3h across l
  # t=20:54  petW7h = Reflect(petN7h, l)
  polygon petW7h = reflect petN7h across l
  # t=20:54  starWh = Reflect(starNh, l)
  polygon starWh = reflect starNh across l
  # t=20:54  octW1 = Reflect(octN1, l)
  polygon octW1 = reflect octN1 across l
  # t=20:54  octW2 = Reflect(octN2, l)
  polygon octW2 = reflect octN2 across l
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  polygon petE1 = reflect petN1 across i
  # t=21:04  petE2 = Reflect(petN2, i)
  polygon petE2 = reflect petN2 across i
  # t=21:04  petE8 = Reflect(petN8, i)
  polygon petE8 = reflect petN8 across i
  # t=21:04  petE3h = Reflect(petN3h, i)
  polygon petE3h = reflect petN3h across i
  # t=21:04  petE7h = Reflect(petN7h, i)
  polygon petE7h = reflect petN7h across i
  # t=21:04  starEh = Reflect(starNh, i)
  polygon starEh = reflect starNh across i
  # t=21:04  octE1 = Reflect(octN1, i)
  polygon octE1 = reflect octN1 across i
  # t=21:04  octE2 = Reflect(octN2, i)
  polygon octE2 = reflect octN2 across i
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  polygon petS1 = reflect petN1 across f
  # t=21:35  petS2 = Reflect(petN2, f)
  polygon petS2 = reflect petN2 across f
  # t=21:35  petS8 = Reflect(petN8, f)
  polygon petS8 = reflect petN8 across f
  # t=21:35  petS3h = Reflect(petN3h, f)
  polygon petS3h = reflect petN3h across f
  # t=21:35  petS7h = Reflect(petN7h, f)
  polygon petS7h = reflect petN7h across f
  # t=21:35  starSh = Reflect(starNh, f)
  polygon starSh = reflect starNh across f
  # t=21:35  octS1 = Reflect(octN1, f)
  polygon octS1 = reflect octN1 across f
  # t=21:35  octS2 = Reflect(octN2, f)
  polygon octS2 = reflect octN2 across f
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  polygon petNW1 = rotate pet8 by 180 around P2
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  polygon petNW7h = rotate petT7 by 180 around P2
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  polygon petNW1h = rotate petL1 by 180 around P2
  # t=21:57  octNW = Rotate(oct1, 180°, P2)
  polygon octNW = rotate oct1 by 180 around P2
  # t=21:57  starNWh = Reflect(starNh, sqL)
  polygon starNWh = reflect starNh across sqL
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  polygon starNWq = rotate starQ2 by 180 around P2
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  polygon petNE1 = reflect petNW1 across g
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  polygon petNE7h = reflect petNW7h across g
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  polygon petNE1h = reflect petNW1h across g
  # t=22:44  octNE = Reflect(octNW, g)
  polygon octNE = reflect octNW across g
  # t=22:44  starNEq = Reflect(starNWq, g)
  polygon starNEq = reflect starNWq across g
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  polygon petSW1 = reflect petNW1 across f
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  polygon petSW7h = reflect petNW7h across f
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  polygon petSW1h = reflect petNW1h across f
  # t=22:58  octSW = Reflect(octNW, f)
  polygon octSW = reflect octNW across f
  # t=22:58  starSWq = Reflect(starNWq, f)
  polygon starSWq = reflect starNWq across f
  # t=22:58  petSE1 = Reflect(petNE1, f)
  polygon petSE1 = reflect petNE1 across f
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  polygon petSE7h = reflect petNE7h across f
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  polygon petSE1h = reflect petNE1h across f
  # t=22:58  octSE = Reflect(octNE, f)
  polygon octSE = reflect octNE across f
  # t=22:58  starSEq = Reflect(starNEq, f)
  polygon starSEq = reflect starNEq across f
  # ────────────────────────────────────────────────────────
  # t=23:10  Q0 = Reflect(O1, g)
  point Q0 = reflect O1 across g
  # t=23:10  Q1 = Reflect(O2, g)
  point Q1 = reflect O2 across g
  # t=23:10  octA = Polygon(O2, O1, 8)
  polygon octA = regular 8 from O2 to O1
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  polygon octB = regular 8 from Q0 to Q1
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  polygon octC = reflect octA across f
  # t=23:19  octD = Reflect(octB, f)
  polygon octD = reflect octB across f

pattern c_7apC5Q9QS_8 on c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  edges from pet1
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  edges from pet2
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  edges from pet3
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  edges from pet4
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  edges from pet5
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  edges from pet6
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  edges from pet7
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  edges from pet8
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  edges from star
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  edges from petN1
  # t=19:05  petN2 = Reflect(pet2, sqT)
  edges from petN2
  # t=19:05  petN8 = Reflect(pet8, sqT)
  edges from petN8
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  edges from starNh
  # t=19:24  petN3h = Reflect(petT3, sqT)
  edges from petN3h
  # t=19:24  petN7h = Reflect(petT7, sqT)
  edges from petN7h
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  edges from petW1
  # t=20:54  petW2 = Reflect(petN2, l)
  edges from petW2
  # t=20:54  petW8 = Reflect(petN8, l)
  edges from petW8
  # t=20:54  petW3h = Reflect(petN3h, l)
  edges from petW3h
  # t=20:54  petW7h = Reflect(petN7h, l)
  edges from petW7h
  # t=20:54  starWh = Reflect(starNh, l)
  edges from starWh
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  edges from petE1
  # t=21:04  petE2 = Reflect(petN2, i)
  edges from petE2
  # t=21:04  petE8 = Reflect(petN8, i)
  edges from petE8
  # t=21:04  petE3h = Reflect(petN3h, i)
  edges from petE3h
  # t=21:04  petE7h = Reflect(petN7h, i)
  edges from petE7h
  # t=21:04  starEh = Reflect(starNh, i)
  edges from starEh
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  edges from petS1
  # t=21:35  petS2 = Reflect(petN2, f)
  edges from petS2
  # t=21:35  petS8 = Reflect(petN8, f)
  edges from petS8
  # t=21:35  petS3h = Reflect(petN3h, f)
  edges from petS3h
  # t=21:35  petS7h = Reflect(petN7h, f)
  edges from petS7h
  # t=21:35  starSh = Reflect(starNh, f)
  edges from starSh
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  edges from petNW1
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  edges from petNW7h
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  edges from petNW1h
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  edges from starNWq
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  edges from petNE1
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  edges from petNE7h
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  edges from petNE1h
  # t=22:44  starNEq = Reflect(starNWq, g)
  edges from starNEq
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  edges from petSW1
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  edges from petSW7h
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  edges from petSW1h
  # t=22:58  starSWq = Reflect(starNWq, f)
  edges from starSWq
  # t=22:58  petSE1 = Reflect(petNE1, f)
  edges from petSE1
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  edges from petSE7h
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  edges from petSE1h
  # t=22:58  starSEq = Reflect(starNEq, f)
  edges from starSEq
  # ────────────────────────────────────────────────────────
  # t=23:10  octA = Polygon(O2, O1, 8)
  edges from octA
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  edges from octB
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  edges from octC
  # t=23:19  octD = Reflect(octB, f)
  edges from octD

coaster Coaster
  outline square $size
  inscribe c_7apC5Q9QS_8
  base 4
  relief straps emboss 1.2
  strap width 2
  interlock dovetail $neck $depth clearance $clearance
`},{id:`six-fold-rosette-minimal`,title:`Six-Fold Rosette · minimal`,blurb:`the six-fold rosette as a freestanding strap network — no slab, the pattern itself extruded with a rounded top edge`,source:`# naqsh construction — GimTvN9hw4U
# title: Simple 20-step Six-Fold Star Rosette
# url: https://www.youtube.com/watch?v=GimTvN9hw4U
# steps: 26 statements, 25 tagged steps
# source: reconstructions/GimTvN9hw4U/construction.ggb-commands sha256:6838767cbb24116b0e5986e62e05a0726b246b8ce0028dc1714fc7194525022e
# renamed: rosette -> rosette_ (reserved word)

param size = 90 range 40..120   # mm, finished coaster span across the strap network — the print knob
param strap = 3 range 1.6..5   # mm, strap width — the freestanding wall, floored at CAL-CST-07 (1.6 mm)
param round = 1 range 0..1.5   # mm, top-edge quarter-round run — CV10 needs 2*round <= strap
param unit = ($size - $strap) / 4.5001   # mm per GeoGebra unit — the art spans K units; the strap adds strap/2 each side

blueprint GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=00:43  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=00:59  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:15  C = Rotate(A, -120°, B)
  point C = rotate A by -120 around B
  # t=01:15  D = Rotate(B, -120°, C)
  point D = rotate B by -120 around C
  # t=01:15  E = Rotate(C, -120°, D)
  point E = rotate C by -120 around D
  # t=01:15  F = Rotate(D, -120°, E)
  point F = rotate D by -120 around E
  # ────────────────────────────────────────────────────────
  # t=01:31  poly1 = Polygon(A, B, C, D, E, F)
  polygon poly1 [ A B C D E F ]
  # ────────────────────────────────────────────────────────
  # t=01:39  l = PerpendicularBisector(A, B)
  bisector l from A to B
  # ────────────────────────────────────────────────────────
  # t=01:44  m = PerpendicularBisector(A, C)
  bisector m from A to C
  # ────────────────────────────────────────────────────────
  # t=01:51  G = Intersect(l, m)
  point G = intersect l m
  # ────────────────────────────────────────────────────────
  # t=01:54  f = Line(A, B)
  line f from A to B
  # ────────────────────────────────────────────────────────
  # t=01:57  H = Intersect(l, f)
  point H = intersect l f
  # ────────────────────────────────────────────────────────
  # t=02:00  c = Circle(B, H)
  circle c center(B) through H
  # ────────────────────────────────────────────────────────
  # t=02:08  I = Midpoint(A, C)
  point I = midpoint A C
  # ────────────────────────────────────────────────────────
  # t=02:36  n = Line(I, l)
  line n through I parallel l
  # ────────────────────────────────────────────────────────
  # t=02:53  p = Line(B, F)
  line p from B to F
  # ────────────────────────────────────────────────────────
  # t=03:07  J = Intersect(n, p)
  point J = intersect n p
  # ────────────────────────────────────────────────────────
  # t=03:14  np = Reflect(n, m)
  line np = reflect n across m
  # ────────────────────────────────────────────────────────
  # t=03:27  K = Intersect(l, np)
  point K = intersect l np
  # ────────────────────────────────────────────────────────
  # t=03:37  Ip = Reflect(I, l)
  point Ip = reflect I across l
  # ────────────────────────────────────────────────────────
  # t=03:41  Jp = Reflect(J, l)
  point Jp = reflect J across l
  # ────────────────────────────────────────────────────────
  # t=03:50  pet = Polygon(H, J, I, K, Ip, Jp)
  polygon pet [ H J I K Ip Jp ]
  # ────────────────────────────────────────────────────────
  # de = Line(D, E)
  line de from D to E
  # ────────────────────────────────────────────────────────
  # t=05:34  reflRosette = Reflect(rosette, de)
  point G_reflRosette = reflect G across de
  # t=05:34  reflRosette = Reflect(rosette, de)
  polygon pet_reflRosette = reflect pet across de

pattern GimTvN9hw4U on GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # t=05:18  rosette = Sequence(Rotate(pet, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    edges from pet
  # ────────────────────────────────────────────────────────
  # t=06:04  tess = Sequence(Rotate(reflRosette, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    rotate 6 around G_reflRosette
      edges from pet_reflRosette

coaster Coaster
  outline pattern
  inscribe GimTvN9hw4U
  base 4
  strap width $strap
  edge fillet $round top
`},{id:`eight-fold-rosette-minimal`,title:`Eight-Fold Rosette · minimal`,blurb:`the eight-fold rosette as a freestanding strap network — no slab, the pattern itself extruded with a rounded top edge`,source:`# naqsh construction — 7apC5Q9QS-8
# title: Geogebra for Beginners 8-Fold Rosette Walkthrough
# url: https://www.youtube.com/watch?v=7apC5Q9QS-8
# steps: 144 statements, 144 tagged steps
# source: reconstructions/7apC5Q9QS-8/construction.ggb-commands sha256:aa7562d6e790f05ccd1a2e79b2cda43ec935fdc5561eb109896abbcb3265a8be

param size = 90 range 40..120   # mm, finished coaster span across the strap network — the print knob
param strap = 3 range 1.6..5   # mm, strap width — the freestanding wall, floored at CAL-CST-07 (1.6 mm)
param round = 1 range 0..1.5   # mm, top-edge quarter-round run — CV10 needs 2*round <= strap
param unit = ($size - $strap) / 4   # mm per GeoGebra unit — the art spans K units; the strap adds strap/2 each side
param pause1 = 1

blueprint c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=01:32  A = (0, 0)
  point A = unit.mpt
  # t=01:32  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:45  c = Circle(A, B)
  circle c center(A) through B
  # ────────────────────────────────────────────────────────
  # t=03:03  f = Line(A, B)
  line f from A to B
  # t=03:03  g = PerpendicularLine(A, f)
  line g through A perpendicular f
  # ────────────────────────────────────────────────────────
  # t=03:44  h = Rotate(f, 22.5°, A)
  line h = rotate f by 22.5 around A
  # t=03:44  i = Rotate(f, 45°, A)
  line i = rotate f by 45 around A
  # t=03:44  j = Rotate(f, 67.5°, A)
  line j = rotate f by 67.5 around A
  # t=03:44  k = Rotate(f, 112.5°, A)
  line k = rotate f by 112.5 around A
  # t=03:44  l = Rotate(f, 135°, A)
  line l = rotate f by 135 around A
  # t=03:44  m = Rotate(f, 157.5°, A)
  line m = rotate f by 157.5 around A
  # ────────────────────────────────────────────────────────
  # t=05:46  sqR = PerpendicularLine(B, f)
  line sqR through B perpendicular f
  # t=05:46  sqT = Rotate(sqR, 90°, A)
  line sqT = rotate sqR by 90 around A
  # t=05:46  sqL = Rotate(sqR, 180°, A)
  line sqL = rotate sqR by 180 around A
  # t=05:46  sqB = Rotate(sqR, 270°, A)
  line sqB = rotate sqR by 270 around A
  # t=05:46  P1 = Intersect(sqR, sqT)
  point P1 = intersect sqR sqT
  # t=05:46  P2 = Intersect(sqT, sqL)
  point P2 = intersect sqT sqL
  # t=05:46  P3 = Intersect(sqL, sqB)
  point P3 = intersect sqL sqB
  # t=05:46  P4 = Intersect(sqB, sqR)
  point P4 = intersect sqB sqR
  # t=05:46  sq = Polygon(P1, P2, P3, P4)
  polygon sq [ P1 P2 P3 P4 ]
  # ────────────────────────────────────────────────────────
  # t=06:50  D = (0, 1)
  point D = unit.cpt1
  # t=06:50  C = Intersect(k, sqT)
  point C = intersect k sqT
  # ────────────────────────────────────────────────────────
  # t=07:47  d = Circle(C, D)
  circle d center(C) through D
  # ────────────────────────────────────────────────────────
  # t=07:50  E = Intersect(d, k, 1)
  point E = intersect d k pick 1
  # ────────────────────────────────────────────────────────
  # t=08:24  p = Line(E, g)
  line p through E parallel g
  # ────────────────────────────────────────────────────────
  # t=09:20  p1 = Reflect(p, k)
  line p1 = reflect p across k
  # ────────────────────────────────────────────────────────
  # t=09:30  p2 = Reflect(p1, g)
  line p2 = reflect p1 across g
  # ────────────────────────────────────────────────────────
  # t=09:40  p3 = Reflect(p2, j)
  line p3 = reflect p2 across j
  # ────────────────────────────────────────────────────────
  # t=10:30  q = AngleBisector(D, C, E)
  line q = bisect angle D C E
  # ────────────────────────────────────────────────────────
  # t=10:50  p4 = Reflect(p, q)
  line p4 = reflect p across q
  # ────────────────────────────────────────────────────────
  # t=11:20  r = Reflect(p4, g)
  line r = reflect p4 across g
  # ────────────────────────────────────────────────────────
  # t=11:42  G = Intersect(p, p4)
  point G = intersect p p4
  # ────────────────────────────────────────────────────────
  # t=11:50  F = Intersect(p3, r)
  point F = intersect p3 r
  # ────────────────────────────────────────────────────────
  # t=11:56  H = Intersect(p1, p2)
  point H = intersect p1 p2
  # ────────────────────────────────────────────────────────
  # t=11:58  I = Intersect(p3, p2)
  point I = intersect p3 p2
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  polygon pet1 [ D G E H I F ]
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  polygon pet2 = reflect pet1 across j
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  polygon pet3 = reflect pet1 across i
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  polygon pet4 = reflect pet1 across h
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  polygon pet5 = reflect pet1 across f
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  polygon pet6 = reflect pet1 across m
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  polygon pet7 = reflect pet1 across l
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  polygon pet8 = reflect pet1 across k
  # ────────────────────────────────────────────────────────
  # t=13:15  L1 = Reflect(p4, l)
  line L1 = reflect p4 across l
  # ────────────────────────────────────────────────────────
  # t=13:20  O1 = Intersect(L1, sqT)
  point O1 = intersect L1 sqT
  # t=13:20  O2 = Intersect(L1, p4)
  point O2 = intersect L1 p4
  # t=13:20  O3 = Intersect(p4, sqL)
  point O3 = intersect p4 sqL
  # ────────────────────────────────────────────────────────
  # t=13:29  oct1 = Polygon(P2, O1, O2, O3)
  polygon oct1 [ P2 O1 O2 O3 ]
  # ────────────────────────────────────────────────────────
  # t=13:40  H2 = Rotate(H, 45°, A)
  point H2 = rotate H by 45 around A
  # t=13:40  H3 = Rotate(H, 90°, A)
  point H3 = rotate H by 90 around A
  # t=13:40  H4 = Rotate(H, 135°, A)
  point H4 = rotate H by 135 around A
  # t=13:40  H5 = Rotate(H, 180°, A)
  point H5 = rotate H by 180 around A
  # t=13:40  H6 = Rotate(H, 225°, A)
  point H6 = rotate H by 225 around A
  # t=13:40  H7 = Rotate(H, 270°, A)
  point H7 = rotate H by 270 around A
  # t=13:40  H8 = Rotate(H, 315°, A)
  point H8 = rotate H by 315 around A
  # ────────────────────────────────────────────────────────
  # t=13:52  pL1 = Reflect(p1, f)
  line pL1 = reflect p1 across f
  # ────────────────────────────────────────────────────────
  # t=13:56  pL2 = Reflect(p2, f)
  line pL2 = reflect p2 across f
  # ────────────────────────────────────────────────────────
  # t=14:00  pH1 = Reflect(p, i)
  line pH1 = reflect p across i
  # ────────────────────────────────────────────────────────
  # t=14:02  pH2 = Reflect(p3, i)
  line pH2 = reflect p3 across i
  # ────────────────────────────────────────────────────────
  # t=14:09  T22 = Intersect(h, p1)
  point T22 = intersect h p1
  # t=14:09  T67 = Intersect(j, p1)
  point T67 = intersect j p1
  # t=14:09  T112 = Intersect(k, p2)
  point T112 = intersect k p2
  # t=14:09  T157 = Intersect(m, p2)
  point T157 = intersect m p2
  # ────────────────────────────────────────────────────────
  # t=14:14  T202 = Intersect(h, pL2)
  point T202 = intersect h pL2
  # t=14:14  T247 = Intersect(j, pL2)
  point T247 = intersect j pL2
  # t=14:14  T292 = Intersect(k, pL1)
  point T292 = intersect k pL1
  # t=14:14  T337 = Intersect(m, pL1)
  point T337 = intersect m pL1
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  polygon star [ H T112 H2 T157 H3 T202 H4 T247 H5 T292 H6 T337 H7 T22 H8 T67 ]
  # ────────────────────────────────────────────────────────
  # t=14:43  oct2 = Reflect(oct1, g)
  polygon oct2 = reflect oct1 across g
  # ────────────────────────────────────────────────────────
  # t=15:10  oct3 = Reflect(oct1, f)
  polygon oct3 = reflect oct1 across f
  # ────────────────────────────────────────────────────────
  # t=15:15  oct4 = Reflect(oct2, f)
  polygon oct4 = reflect oct2 across f
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  polygon petN1 = reflect pet1 across sqT
  # t=19:05  petN2 = Reflect(pet2, sqT)
  polygon petN2 = reflect pet2 across sqT
  # t=19:05  petN8 = Reflect(pet8, sqT)
  polygon petN8 = reflect pet8 across sqT
  # t=19:05  petN3 = Reflect(pet3, sqT)
  polygon petN3 = reflect pet3 across sqT
  # t=19:05  petN7 = Reflect(pet7, sqT)
  polygon petN7 = reflect pet7 across sqT
  # t=19:05  starN = Reflect(star, sqT)
  polygon starN = reflect star across sqT
  # t=19:05  octN1 = Reflect(oct1, sqT)
  polygon octN1 = reflect oct1 across sqT
  # t=19:05  octN2 = Reflect(oct2, sqT)
  polygon octN2 = reflect oct2 across sqT
  # t=19:05  Bl = Rotate(B, 180°, A)
  point Bl = rotate B by 180 around A
  # t=19:05  Fa = Rotate(G, 270°, A)
  point Fa = rotate G by 270 around A
  # t=19:05  Fb = Rotate(F, 90°, A)
  point Fb = rotate F by 90 around A
  # t=19:05  I3 = Rotate(I, 90°, A)
  point I3 = rotate I by 90 around A
  # t=19:05  I8 = Rotate(I, 315°, A)
  point I8 = rotate I by 315 around A
  # t=19:05  petT3 = Polygon(B, Fa, I8, H7)
  polygon petT3 [ B Fa I8 H7 ]
  # t=19:05  petT7 = Polygon(Bl, Fb, I3, H3)
  polygon petT7 [ Bl Fb I3 H3 ]
  # t=19:05  starT = Polygon(H7, T22, H8, T67, H, T112, H2, T157, H3)
  polygon starT [ H7 T22 H8 T67 H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  polygon starNh = reflect starT across sqT
  # t=19:24  petN3h = Reflect(petT3, sqT)
  polygon petN3h = reflect petT3 across sqT
  # t=19:24  petN7h = Reflect(petT7, sqT)
  polygon petN7h = reflect petT7 across sqT
  # ────────────────────────────────────────────────────────
  # t=20:06  petL1 = Polygon(D, G, E, H)
  polygon petL1 [ D G E H ]
  # t=20:06  starQ2 = Polygon(A, H, T112, H2, T157, H3)
  polygon starQ2 [ A H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  polygon petW1 = reflect petN1 across l
  # t=20:54  petW2 = Reflect(petN2, l)
  polygon petW2 = reflect petN2 across l
  # t=20:54  petW8 = Reflect(petN8, l)
  polygon petW8 = reflect petN8 across l
  # t=20:54  petW3h = Reflect(petN3h, l)
  polygon petW3h = reflect petN3h across l
  # t=20:54  petW7h = Reflect(petN7h, l)
  polygon petW7h = reflect petN7h across l
  # t=20:54  starWh = Reflect(starNh, l)
  polygon starWh = reflect starNh across l
  # t=20:54  octW1 = Reflect(octN1, l)
  polygon octW1 = reflect octN1 across l
  # t=20:54  octW2 = Reflect(octN2, l)
  polygon octW2 = reflect octN2 across l
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  polygon petE1 = reflect petN1 across i
  # t=21:04  petE2 = Reflect(petN2, i)
  polygon petE2 = reflect petN2 across i
  # t=21:04  petE8 = Reflect(petN8, i)
  polygon petE8 = reflect petN8 across i
  # t=21:04  petE3h = Reflect(petN3h, i)
  polygon petE3h = reflect petN3h across i
  # t=21:04  petE7h = Reflect(petN7h, i)
  polygon petE7h = reflect petN7h across i
  # t=21:04  starEh = Reflect(starNh, i)
  polygon starEh = reflect starNh across i
  # t=21:04  octE1 = Reflect(octN1, i)
  polygon octE1 = reflect octN1 across i
  # t=21:04  octE2 = Reflect(octN2, i)
  polygon octE2 = reflect octN2 across i
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  polygon petS1 = reflect petN1 across f
  # t=21:35  petS2 = Reflect(petN2, f)
  polygon petS2 = reflect petN2 across f
  # t=21:35  petS8 = Reflect(petN8, f)
  polygon petS8 = reflect petN8 across f
  # t=21:35  petS3h = Reflect(petN3h, f)
  polygon petS3h = reflect petN3h across f
  # t=21:35  petS7h = Reflect(petN7h, f)
  polygon petS7h = reflect petN7h across f
  # t=21:35  starSh = Reflect(starNh, f)
  polygon starSh = reflect starNh across f
  # t=21:35  octS1 = Reflect(octN1, f)
  polygon octS1 = reflect octN1 across f
  # t=21:35  octS2 = Reflect(octN2, f)
  polygon octS2 = reflect octN2 across f
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  polygon petNW1 = rotate pet8 by 180 around P2
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  polygon petNW7h = rotate petT7 by 180 around P2
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  polygon petNW1h = rotate petL1 by 180 around P2
  # t=21:57  octNW = Rotate(oct1, 180°, P2)
  polygon octNW = rotate oct1 by 180 around P2
  # t=21:57  starNWh = Reflect(starNh, sqL)
  polygon starNWh = reflect starNh across sqL
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  polygon starNWq = rotate starQ2 by 180 around P2
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  polygon petNE1 = reflect petNW1 across g
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  polygon petNE7h = reflect petNW7h across g
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  polygon petNE1h = reflect petNW1h across g
  # t=22:44  octNE = Reflect(octNW, g)
  polygon octNE = reflect octNW across g
  # t=22:44  starNEq = Reflect(starNWq, g)
  polygon starNEq = reflect starNWq across g
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  polygon petSW1 = reflect petNW1 across f
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  polygon petSW7h = reflect petNW7h across f
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  polygon petSW1h = reflect petNW1h across f
  # t=22:58  octSW = Reflect(octNW, f)
  polygon octSW = reflect octNW across f
  # t=22:58  starSWq = Reflect(starNWq, f)
  polygon starSWq = reflect starNWq across f
  # t=22:58  petSE1 = Reflect(petNE1, f)
  polygon petSE1 = reflect petNE1 across f
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  polygon petSE7h = reflect petNE7h across f
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  polygon petSE1h = reflect petNE1h across f
  # t=22:58  octSE = Reflect(octNE, f)
  polygon octSE = reflect octNE across f
  # t=22:58  starSEq = Reflect(starNEq, f)
  polygon starSEq = reflect starNEq across f
  # ────────────────────────────────────────────────────────
  # t=23:10  Q0 = Reflect(O1, g)
  point Q0 = reflect O1 across g
  # t=23:10  Q1 = Reflect(O2, g)
  point Q1 = reflect O2 across g
  # t=23:10  octA = Polygon(O2, O1, 8)
  polygon octA = regular 8 from O2 to O1
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  polygon octB = regular 8 from Q0 to Q1
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  polygon octC = reflect octA across f
  # t=23:19  octD = Reflect(octB, f)
  polygon octD = reflect octB across f

pattern c_7apC5Q9QS_8 on c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  edges from pet1
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  edges from pet2
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  edges from pet3
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  edges from pet4
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  edges from pet5
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  edges from pet6
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  edges from pet7
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  edges from pet8
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  edges from star
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  edges from petN1
  # t=19:05  petN2 = Reflect(pet2, sqT)
  edges from petN2
  # t=19:05  petN8 = Reflect(pet8, sqT)
  edges from petN8
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  edges from starNh
  # t=19:24  petN3h = Reflect(petT3, sqT)
  edges from petN3h
  # t=19:24  petN7h = Reflect(petT7, sqT)
  edges from petN7h
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  edges from petW1
  # t=20:54  petW2 = Reflect(petN2, l)
  edges from petW2
  # t=20:54  petW8 = Reflect(petN8, l)
  edges from petW8
  # t=20:54  petW3h = Reflect(petN3h, l)
  edges from petW3h
  # t=20:54  petW7h = Reflect(petN7h, l)
  edges from petW7h
  # t=20:54  starWh = Reflect(starNh, l)
  edges from starWh
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  edges from petE1
  # t=21:04  petE2 = Reflect(petN2, i)
  edges from petE2
  # t=21:04  petE8 = Reflect(petN8, i)
  edges from petE8
  # t=21:04  petE3h = Reflect(petN3h, i)
  edges from petE3h
  # t=21:04  petE7h = Reflect(petN7h, i)
  edges from petE7h
  # t=21:04  starEh = Reflect(starNh, i)
  edges from starEh
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  edges from petS1
  # t=21:35  petS2 = Reflect(petN2, f)
  edges from petS2
  # t=21:35  petS8 = Reflect(petN8, f)
  edges from petS8
  # t=21:35  petS3h = Reflect(petN3h, f)
  edges from petS3h
  # t=21:35  petS7h = Reflect(petN7h, f)
  edges from petS7h
  # t=21:35  starSh = Reflect(starNh, f)
  edges from starSh
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  edges from petNW1
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  edges from petNW7h
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  edges from petNW1h
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  edges from starNWq
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  edges from petNE1
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  edges from petNE7h
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  edges from petNE1h
  # t=22:44  starNEq = Reflect(starNWq, g)
  edges from starNEq
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  edges from petSW1
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  edges from petSW7h
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  edges from petSW1h
  # t=22:58  starSWq = Reflect(starNWq, f)
  edges from starSWq
  # t=22:58  petSE1 = Reflect(petNE1, f)
  edges from petSE1
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  edges from petSE7h
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  edges from petSE1h
  # t=22:58  starSEq = Reflect(starNEq, f)
  edges from starSEq
  # ────────────────────────────────────────────────────────
  # t=23:10  octA = Polygon(O2, O1, 8)
  edges from octA
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  edges from octB
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  edges from octC
  # t=23:19  octD = Reflect(octB, f)
  edges from octD

coaster Coaster
  outline pattern
  inscribe c_7apC5Q9QS_8
  base 4
  strap width $strap
  edge fillet $round top
`},{id:`six-fold-rosette-minimal-frame`,title:`Six-Fold Rosette · minimal-frame`,blurb:`the hexagonal six-fold coaster as openwork — a solid frame round the edge with the straps standing inside it and holes cut through the empty spaces`,source:`# naqsh construction — GimTvN9hw4U
# title: Simple 20-step Six-Fold Star Rosette
# url: https://www.youtube.com/watch?v=GimTvN9hw4U
# steps: 26 statements, 25 tagged steps
# source: reconstructions/GimTvN9hw4U/construction.ggb-commands sha256:6838767cbb24116b0e5986e62e05a0726b246b8ce0028dc1714fc7194525022e
# renamed: rosette -> rosette_ (reserved word)
# style: minimal-frame — the straps stand free inside a solid frame, the empty spaces cut through (openwork, docs/design/coaster-openwork.md)

param size = 90 range 40..120   # mm, finished coaster span across flats — the print knob
param strap = 2 range 1.6..5   # mm, strap width — a freestanding wall once the slab is cut away, floored at CAL-CST-07 (1.6 mm)
param frame = 3 range 2..10   # mm, the solid frame inside the edge — also a freestanding wall
param margin = $frame - 1   # mm, the art sits 1 mm into the frame so every outer strap end joins it
param unit = ($size - 2 * $margin) / 4.5001   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin

blueprint GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=00:43  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=00:59  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:15  C = Rotate(A, -120°, B)
  point C = rotate A by -120 around B
  # t=01:15  D = Rotate(B, -120°, C)
  point D = rotate B by -120 around C
  # t=01:15  E = Rotate(C, -120°, D)
  point E = rotate C by -120 around D
  # t=01:15  F = Rotate(D, -120°, E)
  point F = rotate D by -120 around E
  # ────────────────────────────────────────────────────────
  # t=01:31  poly1 = Polygon(A, B, C, D, E, F)
  polygon poly1 [ A B C D E F ]
  # ────────────────────────────────────────────────────────
  # t=01:39  l = PerpendicularBisector(A, B)
  bisector l from A to B
  # ────────────────────────────────────────────────────────
  # t=01:44  m = PerpendicularBisector(A, C)
  bisector m from A to C
  # ────────────────────────────────────────────────────────
  # t=01:51  G = Intersect(l, m)
  point G = intersect l m
  # ────────────────────────────────────────────────────────
  # t=01:54  f = Line(A, B)
  line f from A to B
  # ────────────────────────────────────────────────────────
  # t=01:57  H = Intersect(l, f)
  point H = intersect l f
  # ────────────────────────────────────────────────────────
  # t=02:00  c = Circle(B, H)
  circle c center(B) through H
  # ────────────────────────────────────────────────────────
  # t=02:08  I = Midpoint(A, C)
  point I = midpoint A C
  # ────────────────────────────────────────────────────────
  # t=02:36  n = Line(I, l)
  line n through I parallel l
  # ────────────────────────────────────────────────────────
  # t=02:53  p = Line(B, F)
  line p from B to F
  # ────────────────────────────────────────────────────────
  # t=03:07  J = Intersect(n, p)
  point J = intersect n p
  # ────────────────────────────────────────────────────────
  # t=03:14  np = Reflect(n, m)
  line np = reflect n across m
  # ────────────────────────────────────────────────────────
  # t=03:27  K = Intersect(l, np)
  point K = intersect l np
  # ────────────────────────────────────────────────────────
  # t=03:37  Ip = Reflect(I, l)
  point Ip = reflect I across l
  # ────────────────────────────────────────────────────────
  # t=03:41  Jp = Reflect(J, l)
  point Jp = reflect J across l
  # ────────────────────────────────────────────────────────
  # t=03:50  pet = Polygon(H, J, I, K, Ip, Jp)
  polygon pet [ H J I K Ip Jp ]
  # ────────────────────────────────────────────────────────
  # de = Line(D, E)
  line de from D to E
  # ────────────────────────────────────────────────────────
  # t=05:34  reflRosette = Reflect(rosette, de)
  point G_reflRosette = reflect G across de
  # t=05:34  reflRosette = Reflect(rosette, de)
  polygon pet_reflRosette = reflect pet across de

pattern GimTvN9hw4U on GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # t=05:18  rosette = Sequence(Rotate(pet, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    edges from pet
  # ────────────────────────────────────────────────────────
  # t=06:04  tess = Sequence(Rotate(reflRosette, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    rotate 6 around G_reflRosette
      edges from pet_reflRosette

coaster Coaster
  outline polygon 6 $size rotate 30
  inscribe GimTvN9hw4U
  base 4
  relief straps emboss 1.2
  strap width $strap
  openwork frame $frame
`},{id:`eight-fold-rosette-minimal-frame`,title:`Eight-Fold Rosette · minimal-frame`,blurb:`the square eight-fold coaster as openwork — a solid frame round the edge with the straps standing inside it and holes cut through the empty spaces`,source:`# naqsh construction — 7apC5Q9QS-8
# title: Geogebra for Beginners 8-Fold Rosette Walkthrough
# url: https://www.youtube.com/watch?v=7apC5Q9QS-8
# steps: 144 statements, 144 tagged steps
# source: reconstructions/7apC5Q9QS-8/construction.ggb-commands sha256:aa7562d6e790f05ccd1a2e79b2cda43ec935fdc5561eb109896abbcb3265a8be
# style: minimal-frame — the straps stand free inside a solid frame, the empty spaces cut through (openwork, docs/design/coaster-openwork.md)

param size = 90 range 40..120   # mm, finished coaster side — the print knob
param strap = 2 range 1.6..5   # mm, strap width — a freestanding wall once the slab is cut away, floored at CAL-CST-07 (1.6 mm)
param frame = 3 range 2..10   # mm, the solid frame inside the edge — also a freestanding wall
param margin = $frame - 1   # mm, the art sits 1 mm into the frame so every outer strap end joins it
param unit = ($size - 2 * $margin) / 4   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin
param pause1 = 1

blueprint c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=01:32  A = (0, 0)
  point A = unit.mpt
  # t=01:32  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:45  c = Circle(A, B)
  circle c center(A) through B
  # ────────────────────────────────────────────────────────
  # t=03:03  f = Line(A, B)
  line f from A to B
  # t=03:03  g = PerpendicularLine(A, f)
  line g through A perpendicular f
  # ────────────────────────────────────────────────────────
  # t=03:44  h = Rotate(f, 22.5°, A)
  line h = rotate f by 22.5 around A
  # t=03:44  i = Rotate(f, 45°, A)
  line i = rotate f by 45 around A
  # t=03:44  j = Rotate(f, 67.5°, A)
  line j = rotate f by 67.5 around A
  # t=03:44  k = Rotate(f, 112.5°, A)
  line k = rotate f by 112.5 around A
  # t=03:44  l = Rotate(f, 135°, A)
  line l = rotate f by 135 around A
  # t=03:44  m = Rotate(f, 157.5°, A)
  line m = rotate f by 157.5 around A
  # ────────────────────────────────────────────────────────
  # t=05:46  sqR = PerpendicularLine(B, f)
  line sqR through B perpendicular f
  # t=05:46  sqT = Rotate(sqR, 90°, A)
  line sqT = rotate sqR by 90 around A
  # t=05:46  sqL = Rotate(sqR, 180°, A)
  line sqL = rotate sqR by 180 around A
  # t=05:46  sqB = Rotate(sqR, 270°, A)
  line sqB = rotate sqR by 270 around A
  # t=05:46  P1 = Intersect(sqR, sqT)
  point P1 = intersect sqR sqT
  # t=05:46  P2 = Intersect(sqT, sqL)
  point P2 = intersect sqT sqL
  # t=05:46  P3 = Intersect(sqL, sqB)
  point P3 = intersect sqL sqB
  # t=05:46  P4 = Intersect(sqB, sqR)
  point P4 = intersect sqB sqR
  # t=05:46  sq = Polygon(P1, P2, P3, P4)
  polygon sq [ P1 P2 P3 P4 ]
  # ────────────────────────────────────────────────────────
  # t=06:50  D = (0, 1)
  point D = unit.cpt1
  # t=06:50  C = Intersect(k, sqT)
  point C = intersect k sqT
  # ────────────────────────────────────────────────────────
  # t=07:47  d = Circle(C, D)
  circle d center(C) through D
  # ────────────────────────────────────────────────────────
  # t=07:50  E = Intersect(d, k, 1)
  point E = intersect d k pick 1
  # ────────────────────────────────────────────────────────
  # t=08:24  p = Line(E, g)
  line p through E parallel g
  # ────────────────────────────────────────────────────────
  # t=09:20  p1 = Reflect(p, k)
  line p1 = reflect p across k
  # ────────────────────────────────────────────────────────
  # t=09:30  p2 = Reflect(p1, g)
  line p2 = reflect p1 across g
  # ────────────────────────────────────────────────────────
  # t=09:40  p3 = Reflect(p2, j)
  line p3 = reflect p2 across j
  # ────────────────────────────────────────────────────────
  # t=10:30  q = AngleBisector(D, C, E)
  line q = bisect angle D C E
  # ────────────────────────────────────────────────────────
  # t=10:50  p4 = Reflect(p, q)
  line p4 = reflect p across q
  # ────────────────────────────────────────────────────────
  # t=11:20  r = Reflect(p4, g)
  line r = reflect p4 across g
  # ────────────────────────────────────────────────────────
  # t=11:42  G = Intersect(p, p4)
  point G = intersect p p4
  # ────────────────────────────────────────────────────────
  # t=11:50  F = Intersect(p3, r)
  point F = intersect p3 r
  # ────────────────────────────────────────────────────────
  # t=11:56  H = Intersect(p1, p2)
  point H = intersect p1 p2
  # ────────────────────────────────────────────────────────
  # t=11:58  I = Intersect(p3, p2)
  point I = intersect p3 p2
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  polygon pet1 [ D G E H I F ]
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  polygon pet2 = reflect pet1 across j
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  polygon pet3 = reflect pet1 across i
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  polygon pet4 = reflect pet1 across h
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  polygon pet5 = reflect pet1 across f
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  polygon pet6 = reflect pet1 across m
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  polygon pet7 = reflect pet1 across l
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  polygon pet8 = reflect pet1 across k
  # ────────────────────────────────────────────────────────
  # t=13:15  L1 = Reflect(p4, l)
  line L1 = reflect p4 across l
  # ────────────────────────────────────────────────────────
  # t=13:20  O1 = Intersect(L1, sqT)
  point O1 = intersect L1 sqT
  # t=13:20  O2 = Intersect(L1, p4)
  point O2 = intersect L1 p4
  # t=13:20  O3 = Intersect(p4, sqL)
  point O3 = intersect p4 sqL
  # ────────────────────────────────────────────────────────
  # t=13:29  oct1 = Polygon(P2, O1, O2, O3)
  polygon oct1 [ P2 O1 O2 O3 ]
  # ────────────────────────────────────────────────────────
  # t=13:40  H2 = Rotate(H, 45°, A)
  point H2 = rotate H by 45 around A
  # t=13:40  H3 = Rotate(H, 90°, A)
  point H3 = rotate H by 90 around A
  # t=13:40  H4 = Rotate(H, 135°, A)
  point H4 = rotate H by 135 around A
  # t=13:40  H5 = Rotate(H, 180°, A)
  point H5 = rotate H by 180 around A
  # t=13:40  H6 = Rotate(H, 225°, A)
  point H6 = rotate H by 225 around A
  # t=13:40  H7 = Rotate(H, 270°, A)
  point H7 = rotate H by 270 around A
  # t=13:40  H8 = Rotate(H, 315°, A)
  point H8 = rotate H by 315 around A
  # ────────────────────────────────────────────────────────
  # t=13:52  pL1 = Reflect(p1, f)
  line pL1 = reflect p1 across f
  # ────────────────────────────────────────────────────────
  # t=13:56  pL2 = Reflect(p2, f)
  line pL2 = reflect p2 across f
  # ────────────────────────────────────────────────────────
  # t=14:00  pH1 = Reflect(p, i)
  line pH1 = reflect p across i
  # ────────────────────────────────────────────────────────
  # t=14:02  pH2 = Reflect(p3, i)
  line pH2 = reflect p3 across i
  # ────────────────────────────────────────────────────────
  # t=14:09  T22 = Intersect(h, p1)
  point T22 = intersect h p1
  # t=14:09  T67 = Intersect(j, p1)
  point T67 = intersect j p1
  # t=14:09  T112 = Intersect(k, p2)
  point T112 = intersect k p2
  # t=14:09  T157 = Intersect(m, p2)
  point T157 = intersect m p2
  # ────────────────────────────────────────────────────────
  # t=14:14  T202 = Intersect(h, pL2)
  point T202 = intersect h pL2
  # t=14:14  T247 = Intersect(j, pL2)
  point T247 = intersect j pL2
  # t=14:14  T292 = Intersect(k, pL1)
  point T292 = intersect k pL1
  # t=14:14  T337 = Intersect(m, pL1)
  point T337 = intersect m pL1
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  polygon star [ H T112 H2 T157 H3 T202 H4 T247 H5 T292 H6 T337 H7 T22 H8 T67 ]
  # ────────────────────────────────────────────────────────
  # t=14:43  oct2 = Reflect(oct1, g)
  polygon oct2 = reflect oct1 across g
  # ────────────────────────────────────────────────────────
  # t=15:10  oct3 = Reflect(oct1, f)
  polygon oct3 = reflect oct1 across f
  # ────────────────────────────────────────────────────────
  # t=15:15  oct4 = Reflect(oct2, f)
  polygon oct4 = reflect oct2 across f
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  polygon petN1 = reflect pet1 across sqT
  # t=19:05  petN2 = Reflect(pet2, sqT)
  polygon petN2 = reflect pet2 across sqT
  # t=19:05  petN8 = Reflect(pet8, sqT)
  polygon petN8 = reflect pet8 across sqT
  # t=19:05  petN3 = Reflect(pet3, sqT)
  polygon petN3 = reflect pet3 across sqT
  # t=19:05  petN7 = Reflect(pet7, sqT)
  polygon petN7 = reflect pet7 across sqT
  # t=19:05  starN = Reflect(star, sqT)
  polygon starN = reflect star across sqT
  # t=19:05  octN1 = Reflect(oct1, sqT)
  polygon octN1 = reflect oct1 across sqT
  # t=19:05  octN2 = Reflect(oct2, sqT)
  polygon octN2 = reflect oct2 across sqT
  # t=19:05  Bl = Rotate(B, 180°, A)
  point Bl = rotate B by 180 around A
  # t=19:05  Fa = Rotate(G, 270°, A)
  point Fa = rotate G by 270 around A
  # t=19:05  Fb = Rotate(F, 90°, A)
  point Fb = rotate F by 90 around A
  # t=19:05  I3 = Rotate(I, 90°, A)
  point I3 = rotate I by 90 around A
  # t=19:05  I8 = Rotate(I, 315°, A)
  point I8 = rotate I by 315 around A
  # t=19:05  petT3 = Polygon(B, Fa, I8, H7)
  polygon petT3 [ B Fa I8 H7 ]
  # t=19:05  petT7 = Polygon(Bl, Fb, I3, H3)
  polygon petT7 [ Bl Fb I3 H3 ]
  # t=19:05  starT = Polygon(H7, T22, H8, T67, H, T112, H2, T157, H3)
  polygon starT [ H7 T22 H8 T67 H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  polygon starNh = reflect starT across sqT
  # t=19:24  petN3h = Reflect(petT3, sqT)
  polygon petN3h = reflect petT3 across sqT
  # t=19:24  petN7h = Reflect(petT7, sqT)
  polygon petN7h = reflect petT7 across sqT
  # ────────────────────────────────────────────────────────
  # t=20:06  petL1 = Polygon(D, G, E, H)
  polygon petL1 [ D G E H ]
  # t=20:06  starQ2 = Polygon(A, H, T112, H2, T157, H3)
  polygon starQ2 [ A H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  polygon petW1 = reflect petN1 across l
  # t=20:54  petW2 = Reflect(petN2, l)
  polygon petW2 = reflect petN2 across l
  # t=20:54  petW8 = Reflect(petN8, l)
  polygon petW8 = reflect petN8 across l
  # t=20:54  petW3h = Reflect(petN3h, l)
  polygon petW3h = reflect petN3h across l
  # t=20:54  petW7h = Reflect(petN7h, l)
  polygon petW7h = reflect petN7h across l
  # t=20:54  starWh = Reflect(starNh, l)
  polygon starWh = reflect starNh across l
  # t=20:54  octW1 = Reflect(octN1, l)
  polygon octW1 = reflect octN1 across l
  # t=20:54  octW2 = Reflect(octN2, l)
  polygon octW2 = reflect octN2 across l
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  polygon petE1 = reflect petN1 across i
  # t=21:04  petE2 = Reflect(petN2, i)
  polygon petE2 = reflect petN2 across i
  # t=21:04  petE8 = Reflect(petN8, i)
  polygon petE8 = reflect petN8 across i
  # t=21:04  petE3h = Reflect(petN3h, i)
  polygon petE3h = reflect petN3h across i
  # t=21:04  petE7h = Reflect(petN7h, i)
  polygon petE7h = reflect petN7h across i
  # t=21:04  starEh = Reflect(starNh, i)
  polygon starEh = reflect starNh across i
  # t=21:04  octE1 = Reflect(octN1, i)
  polygon octE1 = reflect octN1 across i
  # t=21:04  octE2 = Reflect(octN2, i)
  polygon octE2 = reflect octN2 across i
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  polygon petS1 = reflect petN1 across f
  # t=21:35  petS2 = Reflect(petN2, f)
  polygon petS2 = reflect petN2 across f
  # t=21:35  petS8 = Reflect(petN8, f)
  polygon petS8 = reflect petN8 across f
  # t=21:35  petS3h = Reflect(petN3h, f)
  polygon petS3h = reflect petN3h across f
  # t=21:35  petS7h = Reflect(petN7h, f)
  polygon petS7h = reflect petN7h across f
  # t=21:35  starSh = Reflect(starNh, f)
  polygon starSh = reflect starNh across f
  # t=21:35  octS1 = Reflect(octN1, f)
  polygon octS1 = reflect octN1 across f
  # t=21:35  octS2 = Reflect(octN2, f)
  polygon octS2 = reflect octN2 across f
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  polygon petNW1 = rotate pet8 by 180 around P2
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  polygon petNW7h = rotate petT7 by 180 around P2
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  polygon petNW1h = rotate petL1 by 180 around P2
  # t=21:57  octNW = Rotate(oct1, 180°, P2)
  polygon octNW = rotate oct1 by 180 around P2
  # t=21:57  starNWh = Reflect(starNh, sqL)
  polygon starNWh = reflect starNh across sqL
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  polygon starNWq = rotate starQ2 by 180 around P2
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  polygon petNE1 = reflect petNW1 across g
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  polygon petNE7h = reflect petNW7h across g
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  polygon petNE1h = reflect petNW1h across g
  # t=22:44  octNE = Reflect(octNW, g)
  polygon octNE = reflect octNW across g
  # t=22:44  starNEq = Reflect(starNWq, g)
  polygon starNEq = reflect starNWq across g
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  polygon petSW1 = reflect petNW1 across f
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  polygon petSW7h = reflect petNW7h across f
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  polygon petSW1h = reflect petNW1h across f
  # t=22:58  octSW = Reflect(octNW, f)
  polygon octSW = reflect octNW across f
  # t=22:58  starSWq = Reflect(starNWq, f)
  polygon starSWq = reflect starNWq across f
  # t=22:58  petSE1 = Reflect(petNE1, f)
  polygon petSE1 = reflect petNE1 across f
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  polygon petSE7h = reflect petNE7h across f
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  polygon petSE1h = reflect petNE1h across f
  # t=22:58  octSE = Reflect(octNE, f)
  polygon octSE = reflect octNE across f
  # t=22:58  starSEq = Reflect(starNEq, f)
  polygon starSEq = reflect starNEq across f
  # ────────────────────────────────────────────────────────
  # t=23:10  Q0 = Reflect(O1, g)
  point Q0 = reflect O1 across g
  # t=23:10  Q1 = Reflect(O2, g)
  point Q1 = reflect O2 across g
  # t=23:10  octA = Polygon(O2, O1, 8)
  polygon octA = regular 8 from O2 to O1
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  polygon octB = regular 8 from Q0 to Q1
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  polygon octC = reflect octA across f
  # t=23:19  octD = Reflect(octB, f)
  polygon octD = reflect octB across f

pattern c_7apC5Q9QS_8 on c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  edges from pet1
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  edges from pet2
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  edges from pet3
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  edges from pet4
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  edges from pet5
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  edges from pet6
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  edges from pet7
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  edges from pet8
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  edges from star
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  edges from petN1
  # t=19:05  petN2 = Reflect(pet2, sqT)
  edges from petN2
  # t=19:05  petN8 = Reflect(pet8, sqT)
  edges from petN8
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  edges from starNh
  # t=19:24  petN3h = Reflect(petT3, sqT)
  edges from petN3h
  # t=19:24  petN7h = Reflect(petT7, sqT)
  edges from petN7h
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  edges from petW1
  # t=20:54  petW2 = Reflect(petN2, l)
  edges from petW2
  # t=20:54  petW8 = Reflect(petN8, l)
  edges from petW8
  # t=20:54  petW3h = Reflect(petN3h, l)
  edges from petW3h
  # t=20:54  petW7h = Reflect(petN7h, l)
  edges from petW7h
  # t=20:54  starWh = Reflect(starNh, l)
  edges from starWh
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  edges from petE1
  # t=21:04  petE2 = Reflect(petN2, i)
  edges from petE2
  # t=21:04  petE8 = Reflect(petN8, i)
  edges from petE8
  # t=21:04  petE3h = Reflect(petN3h, i)
  edges from petE3h
  # t=21:04  petE7h = Reflect(petN7h, i)
  edges from petE7h
  # t=21:04  starEh = Reflect(starNh, i)
  edges from starEh
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  edges from petS1
  # t=21:35  petS2 = Reflect(petN2, f)
  edges from petS2
  # t=21:35  petS8 = Reflect(petN8, f)
  edges from petS8
  # t=21:35  petS3h = Reflect(petN3h, f)
  edges from petS3h
  # t=21:35  petS7h = Reflect(petN7h, f)
  edges from petS7h
  # t=21:35  starSh = Reflect(starNh, f)
  edges from starSh
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  edges from petNW1
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  edges from petNW7h
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  edges from petNW1h
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  edges from starNWq
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  edges from petNE1
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  edges from petNE7h
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  edges from petNE1h
  # t=22:44  starNEq = Reflect(starNWq, g)
  edges from starNEq
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  edges from petSW1
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  edges from petSW7h
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  edges from petSW1h
  # t=22:58  starSWq = Reflect(starNWq, f)
  edges from starSWq
  # t=22:58  petSE1 = Reflect(petNE1, f)
  edges from petSE1
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  edges from petSE7h
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  edges from petSE1h
  # t=22:58  starSEq = Reflect(starNEq, f)
  edges from starSEq
  # ────────────────────────────────────────────────────────
  # t=23:10  octA = Polygon(O2, O1, 8)
  edges from octA
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  edges from octB
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  edges from octC
  # t=23:19  octD = Reflect(octB, f)
  edges from octD

coaster Coaster
  outline square $size
  inscribe c_7apC5Q9QS_8
  base 4
  relief straps emboss 1.2
  strap width $strap
  openwork frame $frame
`},{id:`six-fold-rosette-minimal-pegs`,title:`Six-Fold Rosette · minimal-pegs`,blurb:`the hexagonal six-fold coaster as openwork — minimal-frame with dovetail tabs and slots in the frame, so an openwork set tiles edge to edge`,source:`# naqsh construction — GimTvN9hw4U
# title: Simple 20-step Six-Fold Star Rosette
# url: https://www.youtube.com/watch?v=GimTvN9hw4U
# steps: 26 statements, 25 tagged steps
# source: reconstructions/GimTvN9hw4U/construction.ggb-commands sha256:6838767cbb24116b0e5986e62e05a0726b246b8ce0028dc1714fc7194525022e
# renamed: rosette -> rosette_ (reserved word)
# style: minimal-pegs — the minimal-frame coaster with a dovetail on every edge (openwork + interlock, docs/design/coaster-openwork.md)

param size = 90 range 40..120   # mm, finished coaster span across flats — the print knob
param neck = 3 range 2..5   # mm, dovetail neck at the edge line
param depth = 3 range 2..5   # mm, how far the tab protrudes / the slot cuts in
param clearance = 0.15 range 0.05..0.35   # mm, CAL-FIT-01 ladder: snug .. free
param strap = 2 range 1.6..5   # mm, strap width — a freestanding wall once the slab is cut away, floored at CAL-CST-07 (1.6 mm)
param frame = $depth + $clearance + 2.5   # mm, the solid frame: what the slot eats plus a 2.5 mm wall (the kernel needs 1.6 mm; the extra keeps the art clear of the slot, CV8)
param margin = $frame - 1   # mm, the art sits 1 mm into the frame so every outer strap end joins it
param unit = ($size - 2 * $margin) / 4.5001   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin

blueprint GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=00:43  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=00:59  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:15  C = Rotate(A, -120°, B)
  point C = rotate A by -120 around B
  # t=01:15  D = Rotate(B, -120°, C)
  point D = rotate B by -120 around C
  # t=01:15  E = Rotate(C, -120°, D)
  point E = rotate C by -120 around D
  # t=01:15  F = Rotate(D, -120°, E)
  point F = rotate D by -120 around E
  # ────────────────────────────────────────────────────────
  # t=01:31  poly1 = Polygon(A, B, C, D, E, F)
  polygon poly1 [ A B C D E F ]
  # ────────────────────────────────────────────────────────
  # t=01:39  l = PerpendicularBisector(A, B)
  bisector l from A to B
  # ────────────────────────────────────────────────────────
  # t=01:44  m = PerpendicularBisector(A, C)
  bisector m from A to C
  # ────────────────────────────────────────────────────────
  # t=01:51  G = Intersect(l, m)
  point G = intersect l m
  # ────────────────────────────────────────────────────────
  # t=01:54  f = Line(A, B)
  line f from A to B
  # ────────────────────────────────────────────────────────
  # t=01:57  H = Intersect(l, f)
  point H = intersect l f
  # ────────────────────────────────────────────────────────
  # t=02:00  c = Circle(B, H)
  circle c center(B) through H
  # ────────────────────────────────────────────────────────
  # t=02:08  I = Midpoint(A, C)
  point I = midpoint A C
  # ────────────────────────────────────────────────────────
  # t=02:36  n = Line(I, l)
  line n through I parallel l
  # ────────────────────────────────────────────────────────
  # t=02:53  p = Line(B, F)
  line p from B to F
  # ────────────────────────────────────────────────────────
  # t=03:07  J = Intersect(n, p)
  point J = intersect n p
  # ────────────────────────────────────────────────────────
  # t=03:14  np = Reflect(n, m)
  line np = reflect n across m
  # ────────────────────────────────────────────────────────
  # t=03:27  K = Intersect(l, np)
  point K = intersect l np
  # ────────────────────────────────────────────────────────
  # t=03:37  Ip = Reflect(I, l)
  point Ip = reflect I across l
  # ────────────────────────────────────────────────────────
  # t=03:41  Jp = Reflect(J, l)
  point Jp = reflect J across l
  # ────────────────────────────────────────────────────────
  # t=03:50  pet = Polygon(H, J, I, K, Ip, Jp)
  polygon pet [ H J I K Ip Jp ]
  # ────────────────────────────────────────────────────────
  # de = Line(D, E)
  line de from D to E
  # ────────────────────────────────────────────────────────
  # t=05:34  reflRosette = Reflect(rosette, de)
  point G_reflRosette = reflect G across de
  # t=05:34  reflRosette = Reflect(rosette, de)
  polygon pet_reflRosette = reflect pet across de

pattern GimTvN9hw4U on GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # t=05:18  rosette = Sequence(Rotate(pet, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    edges from pet
  # ────────────────────────────────────────────────────────
  # t=06:04  tess = Sequence(Rotate(reflRosette, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    rotate 6 around G_reflRosette
      edges from pet_reflRosette

coaster Coaster
  outline polygon 6 $size rotate 30
  inscribe GimTvN9hw4U
  base 4
  relief straps emboss 1.2
  strap width $strap
  interlock dovetail $neck $depth clearance $clearance
  openwork frame $frame
`},{id:`eight-fold-rosette-minimal-pegs`,title:`Eight-Fold Rosette · minimal-pegs`,blurb:`the square eight-fold coaster as openwork — minimal-frame with dovetail tabs and slots in the frame, so an openwork set tiles edge to edge`,source:`# naqsh construction — 7apC5Q9QS-8
# title: Geogebra for Beginners 8-Fold Rosette Walkthrough
# url: https://www.youtube.com/watch?v=7apC5Q9QS-8
# steps: 144 statements, 144 tagged steps
# source: reconstructions/7apC5Q9QS-8/construction.ggb-commands sha256:aa7562d6e790f05ccd1a2e79b2cda43ec935fdc5561eb109896abbcb3265a8be
# style: minimal-pegs — the minimal-frame coaster with a dovetail on every edge (openwork + interlock, docs/design/coaster-openwork.md)

param size = 90 range 40..120   # mm, finished coaster side — the print knob
param neck = 3 range 2..5   # mm, dovetail neck at the edge line
param depth = 3 range 2..5   # mm, how far the tab protrudes / the slot cuts in
param clearance = 0.15 range 0.05..0.35   # mm, CAL-FIT-01 ladder: snug .. free
param strap = 2 range 1.6..5   # mm, strap width — a freestanding wall once the slab is cut away, floored at CAL-CST-07 (1.6 mm)
param frame = $depth + $clearance + 2.5   # mm, the solid frame: what the slot eats plus a 2.5 mm wall (the kernel needs 1.6 mm; the extra keeps the art clear of the slot, CV8)
param margin = $frame - 1   # mm, the art sits 1 mm into the frame so every outer strap end joins it
param unit = ($size - 2 * $margin) / 4   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin
param pause1 = 1

blueprint c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=01:32  A = (0, 0)
  point A = unit.mpt
  # t=01:32  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:45  c = Circle(A, B)
  circle c center(A) through B
  # ────────────────────────────────────────────────────────
  # t=03:03  f = Line(A, B)
  line f from A to B
  # t=03:03  g = PerpendicularLine(A, f)
  line g through A perpendicular f
  # ────────────────────────────────────────────────────────
  # t=03:44  h = Rotate(f, 22.5°, A)
  line h = rotate f by 22.5 around A
  # t=03:44  i = Rotate(f, 45°, A)
  line i = rotate f by 45 around A
  # t=03:44  j = Rotate(f, 67.5°, A)
  line j = rotate f by 67.5 around A
  # t=03:44  k = Rotate(f, 112.5°, A)
  line k = rotate f by 112.5 around A
  # t=03:44  l = Rotate(f, 135°, A)
  line l = rotate f by 135 around A
  # t=03:44  m = Rotate(f, 157.5°, A)
  line m = rotate f by 157.5 around A
  # ────────────────────────────────────────────────────────
  # t=05:46  sqR = PerpendicularLine(B, f)
  line sqR through B perpendicular f
  # t=05:46  sqT = Rotate(sqR, 90°, A)
  line sqT = rotate sqR by 90 around A
  # t=05:46  sqL = Rotate(sqR, 180°, A)
  line sqL = rotate sqR by 180 around A
  # t=05:46  sqB = Rotate(sqR, 270°, A)
  line sqB = rotate sqR by 270 around A
  # t=05:46  P1 = Intersect(sqR, sqT)
  point P1 = intersect sqR sqT
  # t=05:46  P2 = Intersect(sqT, sqL)
  point P2 = intersect sqT sqL
  # t=05:46  P3 = Intersect(sqL, sqB)
  point P3 = intersect sqL sqB
  # t=05:46  P4 = Intersect(sqB, sqR)
  point P4 = intersect sqB sqR
  # t=05:46  sq = Polygon(P1, P2, P3, P4)
  polygon sq [ P1 P2 P3 P4 ]
  # ────────────────────────────────────────────────────────
  # t=06:50  D = (0, 1)
  point D = unit.cpt1
  # t=06:50  C = Intersect(k, sqT)
  point C = intersect k sqT
  # ────────────────────────────────────────────────────────
  # t=07:47  d = Circle(C, D)
  circle d center(C) through D
  # ────────────────────────────────────────────────────────
  # t=07:50  E = Intersect(d, k, 1)
  point E = intersect d k pick 1
  # ────────────────────────────────────────────────────────
  # t=08:24  p = Line(E, g)
  line p through E parallel g
  # ────────────────────────────────────────────────────────
  # t=09:20  p1 = Reflect(p, k)
  line p1 = reflect p across k
  # ────────────────────────────────────────────────────────
  # t=09:30  p2 = Reflect(p1, g)
  line p2 = reflect p1 across g
  # ────────────────────────────────────────────────────────
  # t=09:40  p3 = Reflect(p2, j)
  line p3 = reflect p2 across j
  # ────────────────────────────────────────────────────────
  # t=10:30  q = AngleBisector(D, C, E)
  line q = bisect angle D C E
  # ────────────────────────────────────────────────────────
  # t=10:50  p4 = Reflect(p, q)
  line p4 = reflect p across q
  # ────────────────────────────────────────────────────────
  # t=11:20  r = Reflect(p4, g)
  line r = reflect p4 across g
  # ────────────────────────────────────────────────────────
  # t=11:42  G = Intersect(p, p4)
  point G = intersect p p4
  # ────────────────────────────────────────────────────────
  # t=11:50  F = Intersect(p3, r)
  point F = intersect p3 r
  # ────────────────────────────────────────────────────────
  # t=11:56  H = Intersect(p1, p2)
  point H = intersect p1 p2
  # ────────────────────────────────────────────────────────
  # t=11:58  I = Intersect(p3, p2)
  point I = intersect p3 p2
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  polygon pet1 [ D G E H I F ]
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  polygon pet2 = reflect pet1 across j
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  polygon pet3 = reflect pet1 across i
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  polygon pet4 = reflect pet1 across h
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  polygon pet5 = reflect pet1 across f
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  polygon pet6 = reflect pet1 across m
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  polygon pet7 = reflect pet1 across l
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  polygon pet8 = reflect pet1 across k
  # ────────────────────────────────────────────────────────
  # t=13:15  L1 = Reflect(p4, l)
  line L1 = reflect p4 across l
  # ────────────────────────────────────────────────────────
  # t=13:20  O1 = Intersect(L1, sqT)
  point O1 = intersect L1 sqT
  # t=13:20  O2 = Intersect(L1, p4)
  point O2 = intersect L1 p4
  # t=13:20  O3 = Intersect(p4, sqL)
  point O3 = intersect p4 sqL
  # ────────────────────────────────────────────────────────
  # t=13:29  oct1 = Polygon(P2, O1, O2, O3)
  polygon oct1 [ P2 O1 O2 O3 ]
  # ────────────────────────────────────────────────────────
  # t=13:40  H2 = Rotate(H, 45°, A)
  point H2 = rotate H by 45 around A
  # t=13:40  H3 = Rotate(H, 90°, A)
  point H3 = rotate H by 90 around A
  # t=13:40  H4 = Rotate(H, 135°, A)
  point H4 = rotate H by 135 around A
  # t=13:40  H5 = Rotate(H, 180°, A)
  point H5 = rotate H by 180 around A
  # t=13:40  H6 = Rotate(H, 225°, A)
  point H6 = rotate H by 225 around A
  # t=13:40  H7 = Rotate(H, 270°, A)
  point H7 = rotate H by 270 around A
  # t=13:40  H8 = Rotate(H, 315°, A)
  point H8 = rotate H by 315 around A
  # ────────────────────────────────────────────────────────
  # t=13:52  pL1 = Reflect(p1, f)
  line pL1 = reflect p1 across f
  # ────────────────────────────────────────────────────────
  # t=13:56  pL2 = Reflect(p2, f)
  line pL2 = reflect p2 across f
  # ────────────────────────────────────────────────────────
  # t=14:00  pH1 = Reflect(p, i)
  line pH1 = reflect p across i
  # ────────────────────────────────────────────────────────
  # t=14:02  pH2 = Reflect(p3, i)
  line pH2 = reflect p3 across i
  # ────────────────────────────────────────────────────────
  # t=14:09  T22 = Intersect(h, p1)
  point T22 = intersect h p1
  # t=14:09  T67 = Intersect(j, p1)
  point T67 = intersect j p1
  # t=14:09  T112 = Intersect(k, p2)
  point T112 = intersect k p2
  # t=14:09  T157 = Intersect(m, p2)
  point T157 = intersect m p2
  # ────────────────────────────────────────────────────────
  # t=14:14  T202 = Intersect(h, pL2)
  point T202 = intersect h pL2
  # t=14:14  T247 = Intersect(j, pL2)
  point T247 = intersect j pL2
  # t=14:14  T292 = Intersect(k, pL1)
  point T292 = intersect k pL1
  # t=14:14  T337 = Intersect(m, pL1)
  point T337 = intersect m pL1
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  polygon star [ H T112 H2 T157 H3 T202 H4 T247 H5 T292 H6 T337 H7 T22 H8 T67 ]
  # ────────────────────────────────────────────────────────
  # t=14:43  oct2 = Reflect(oct1, g)
  polygon oct2 = reflect oct1 across g
  # ────────────────────────────────────────────────────────
  # t=15:10  oct3 = Reflect(oct1, f)
  polygon oct3 = reflect oct1 across f
  # ────────────────────────────────────────────────────────
  # t=15:15  oct4 = Reflect(oct2, f)
  polygon oct4 = reflect oct2 across f
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  polygon petN1 = reflect pet1 across sqT
  # t=19:05  petN2 = Reflect(pet2, sqT)
  polygon petN2 = reflect pet2 across sqT
  # t=19:05  petN8 = Reflect(pet8, sqT)
  polygon petN8 = reflect pet8 across sqT
  # t=19:05  petN3 = Reflect(pet3, sqT)
  polygon petN3 = reflect pet3 across sqT
  # t=19:05  petN7 = Reflect(pet7, sqT)
  polygon petN7 = reflect pet7 across sqT
  # t=19:05  starN = Reflect(star, sqT)
  polygon starN = reflect star across sqT
  # t=19:05  octN1 = Reflect(oct1, sqT)
  polygon octN1 = reflect oct1 across sqT
  # t=19:05  octN2 = Reflect(oct2, sqT)
  polygon octN2 = reflect oct2 across sqT
  # t=19:05  Bl = Rotate(B, 180°, A)
  point Bl = rotate B by 180 around A
  # t=19:05  Fa = Rotate(G, 270°, A)
  point Fa = rotate G by 270 around A
  # t=19:05  Fb = Rotate(F, 90°, A)
  point Fb = rotate F by 90 around A
  # t=19:05  I3 = Rotate(I, 90°, A)
  point I3 = rotate I by 90 around A
  # t=19:05  I8 = Rotate(I, 315°, A)
  point I8 = rotate I by 315 around A
  # t=19:05  petT3 = Polygon(B, Fa, I8, H7)
  polygon petT3 [ B Fa I8 H7 ]
  # t=19:05  petT7 = Polygon(Bl, Fb, I3, H3)
  polygon petT7 [ Bl Fb I3 H3 ]
  # t=19:05  starT = Polygon(H7, T22, H8, T67, H, T112, H2, T157, H3)
  polygon starT [ H7 T22 H8 T67 H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  polygon starNh = reflect starT across sqT
  # t=19:24  petN3h = Reflect(petT3, sqT)
  polygon petN3h = reflect petT3 across sqT
  # t=19:24  petN7h = Reflect(petT7, sqT)
  polygon petN7h = reflect petT7 across sqT
  # ────────────────────────────────────────────────────────
  # t=20:06  petL1 = Polygon(D, G, E, H)
  polygon petL1 [ D G E H ]
  # t=20:06  starQ2 = Polygon(A, H, T112, H2, T157, H3)
  polygon starQ2 [ A H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  polygon petW1 = reflect petN1 across l
  # t=20:54  petW2 = Reflect(petN2, l)
  polygon petW2 = reflect petN2 across l
  # t=20:54  petW8 = Reflect(petN8, l)
  polygon petW8 = reflect petN8 across l
  # t=20:54  petW3h = Reflect(petN3h, l)
  polygon petW3h = reflect petN3h across l
  # t=20:54  petW7h = Reflect(petN7h, l)
  polygon petW7h = reflect petN7h across l
  # t=20:54  starWh = Reflect(starNh, l)
  polygon starWh = reflect starNh across l
  # t=20:54  octW1 = Reflect(octN1, l)
  polygon octW1 = reflect octN1 across l
  # t=20:54  octW2 = Reflect(octN2, l)
  polygon octW2 = reflect octN2 across l
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  polygon petE1 = reflect petN1 across i
  # t=21:04  petE2 = Reflect(petN2, i)
  polygon petE2 = reflect petN2 across i
  # t=21:04  petE8 = Reflect(petN8, i)
  polygon petE8 = reflect petN8 across i
  # t=21:04  petE3h = Reflect(petN3h, i)
  polygon petE3h = reflect petN3h across i
  # t=21:04  petE7h = Reflect(petN7h, i)
  polygon petE7h = reflect petN7h across i
  # t=21:04  starEh = Reflect(starNh, i)
  polygon starEh = reflect starNh across i
  # t=21:04  octE1 = Reflect(octN1, i)
  polygon octE1 = reflect octN1 across i
  # t=21:04  octE2 = Reflect(octN2, i)
  polygon octE2 = reflect octN2 across i
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  polygon petS1 = reflect petN1 across f
  # t=21:35  petS2 = Reflect(petN2, f)
  polygon petS2 = reflect petN2 across f
  # t=21:35  petS8 = Reflect(petN8, f)
  polygon petS8 = reflect petN8 across f
  # t=21:35  petS3h = Reflect(petN3h, f)
  polygon petS3h = reflect petN3h across f
  # t=21:35  petS7h = Reflect(petN7h, f)
  polygon petS7h = reflect petN7h across f
  # t=21:35  starSh = Reflect(starNh, f)
  polygon starSh = reflect starNh across f
  # t=21:35  octS1 = Reflect(octN1, f)
  polygon octS1 = reflect octN1 across f
  # t=21:35  octS2 = Reflect(octN2, f)
  polygon octS2 = reflect octN2 across f
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  polygon petNW1 = rotate pet8 by 180 around P2
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  polygon petNW7h = rotate petT7 by 180 around P2
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  polygon petNW1h = rotate petL1 by 180 around P2
  # t=21:57  octNW = Rotate(oct1, 180°, P2)
  polygon octNW = rotate oct1 by 180 around P2
  # t=21:57  starNWh = Reflect(starNh, sqL)
  polygon starNWh = reflect starNh across sqL
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  polygon starNWq = rotate starQ2 by 180 around P2
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  polygon petNE1 = reflect petNW1 across g
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  polygon petNE7h = reflect petNW7h across g
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  polygon petNE1h = reflect petNW1h across g
  # t=22:44  octNE = Reflect(octNW, g)
  polygon octNE = reflect octNW across g
  # t=22:44  starNEq = Reflect(starNWq, g)
  polygon starNEq = reflect starNWq across g
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  polygon petSW1 = reflect petNW1 across f
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  polygon petSW7h = reflect petNW7h across f
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  polygon petSW1h = reflect petNW1h across f
  # t=22:58  octSW = Reflect(octNW, f)
  polygon octSW = reflect octNW across f
  # t=22:58  starSWq = Reflect(starNWq, f)
  polygon starSWq = reflect starNWq across f
  # t=22:58  petSE1 = Reflect(petNE1, f)
  polygon petSE1 = reflect petNE1 across f
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  polygon petSE7h = reflect petNE7h across f
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  polygon petSE1h = reflect petNE1h across f
  # t=22:58  octSE = Reflect(octNE, f)
  polygon octSE = reflect octNE across f
  # t=22:58  starSEq = Reflect(starNEq, f)
  polygon starSEq = reflect starNEq across f
  # ────────────────────────────────────────────────────────
  # t=23:10  Q0 = Reflect(O1, g)
  point Q0 = reflect O1 across g
  # t=23:10  Q1 = Reflect(O2, g)
  point Q1 = reflect O2 across g
  # t=23:10  octA = Polygon(O2, O1, 8)
  polygon octA = regular 8 from O2 to O1
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  polygon octB = regular 8 from Q0 to Q1
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  polygon octC = reflect octA across f
  # t=23:19  octD = Reflect(octB, f)
  polygon octD = reflect octB across f

pattern c_7apC5Q9QS_8 on c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  edges from pet1
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  edges from pet2
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  edges from pet3
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  edges from pet4
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  edges from pet5
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  edges from pet6
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  edges from pet7
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  edges from pet8
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  edges from star
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  edges from petN1
  # t=19:05  petN2 = Reflect(pet2, sqT)
  edges from petN2
  # t=19:05  petN8 = Reflect(pet8, sqT)
  edges from petN8
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  edges from starNh
  # t=19:24  petN3h = Reflect(petT3, sqT)
  edges from petN3h
  # t=19:24  petN7h = Reflect(petT7, sqT)
  edges from petN7h
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  edges from petW1
  # t=20:54  petW2 = Reflect(petN2, l)
  edges from petW2
  # t=20:54  petW8 = Reflect(petN8, l)
  edges from petW8
  # t=20:54  petW3h = Reflect(petN3h, l)
  edges from petW3h
  # t=20:54  petW7h = Reflect(petN7h, l)
  edges from petW7h
  # t=20:54  starWh = Reflect(starNh, l)
  edges from starWh
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  edges from petE1
  # t=21:04  petE2 = Reflect(petN2, i)
  edges from petE2
  # t=21:04  petE8 = Reflect(petN8, i)
  edges from petE8
  # t=21:04  petE3h = Reflect(petN3h, i)
  edges from petE3h
  # t=21:04  petE7h = Reflect(petN7h, i)
  edges from petE7h
  # t=21:04  starEh = Reflect(starNh, i)
  edges from starEh
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  edges from petS1
  # t=21:35  petS2 = Reflect(petN2, f)
  edges from petS2
  # t=21:35  petS8 = Reflect(petN8, f)
  edges from petS8
  # t=21:35  petS3h = Reflect(petN3h, f)
  edges from petS3h
  # t=21:35  petS7h = Reflect(petN7h, f)
  edges from petS7h
  # t=21:35  starSh = Reflect(starNh, f)
  edges from starSh
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  edges from petNW1
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  edges from petNW7h
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  edges from petNW1h
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  edges from starNWq
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  edges from petNE1
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  edges from petNE7h
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  edges from petNE1h
  # t=22:44  starNEq = Reflect(starNWq, g)
  edges from starNEq
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  edges from petSW1
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  edges from petSW7h
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  edges from petSW1h
  # t=22:58  starSWq = Reflect(starNWq, f)
  edges from starSWq
  # t=22:58  petSE1 = Reflect(petNE1, f)
  edges from petSE1
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  edges from petSE7h
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  edges from petSE1h
  # t=22:58  starSEq = Reflect(starNEq, f)
  edges from starSEq
  # ────────────────────────────────────────────────────────
  # t=23:10  octA = Polygon(O2, O1, 8)
  edges from octA
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  edges from octB
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  edges from octC
  # t=23:19  octD = Reflect(octB, f)
  edges from octD

coaster Coaster
  outline square $size
  inscribe c_7apC5Q9QS_8
  base 4
  relief straps emboss 1.2
  strap width $strap
  interlock dovetail $neck $depth clearance $clearance
  openwork frame $frame
`},{id:`six-fold-rosette-border`,title:`Six-Fold Rosette · border`,blurb:`the hexagonal six-fold coaster wrapped in a chevron band around the edge, in relief beside the art`,source:`# naqsh construction — GimTvN9hw4U
# title: Simple 20-step Six-Fold Star Rosette
# url: https://www.youtube.com/watch?v=GimTvN9hw4U
# steps: 26 statements, 25 tagged steps
# source: reconstructions/GimTvN9hw4U/construction.ggb-commands sha256:6838767cbb24116b0e5986e62e05a0726b246b8ce0028dc1714fc7194525022e
# renamed: rosette -> rosette_ (reserved word)

param size = 90 range 40..120   # mm, finished coaster span across flats — the print knob
param border = 8 range 3..15   # mm, chevron band width, measured inward from the edge
param margin = 2 range 1..10   # mm, blank slab between the art and the edge
param unit = ($size - 2 * ($border + $margin)) / 4.5001   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin

blueprint GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=00:43  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=00:59  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:15  C = Rotate(A, -120°, B)
  point C = rotate A by -120 around B
  # t=01:15  D = Rotate(B, -120°, C)
  point D = rotate B by -120 around C
  # t=01:15  E = Rotate(C, -120°, D)
  point E = rotate C by -120 around D
  # t=01:15  F = Rotate(D, -120°, E)
  point F = rotate D by -120 around E
  # ────────────────────────────────────────────────────────
  # t=01:31  poly1 = Polygon(A, B, C, D, E, F)
  polygon poly1 [ A B C D E F ]
  # ────────────────────────────────────────────────────────
  # t=01:39  l = PerpendicularBisector(A, B)
  bisector l from A to B
  # ────────────────────────────────────────────────────────
  # t=01:44  m = PerpendicularBisector(A, C)
  bisector m from A to C
  # ────────────────────────────────────────────────────────
  # t=01:51  G = Intersect(l, m)
  point G = intersect l m
  # ────────────────────────────────────────────────────────
  # t=01:54  f = Line(A, B)
  line f from A to B
  # ────────────────────────────────────────────────────────
  # t=01:57  H = Intersect(l, f)
  point H = intersect l f
  # ────────────────────────────────────────────────────────
  # t=02:00  c = Circle(B, H)
  circle c center(B) through H
  # ────────────────────────────────────────────────────────
  # t=02:08  I = Midpoint(A, C)
  point I = midpoint A C
  # ────────────────────────────────────────────────────────
  # t=02:36  n = Line(I, l)
  line n through I parallel l
  # ────────────────────────────────────────────────────────
  # t=02:53  p = Line(B, F)
  line p from B to F
  # ────────────────────────────────────────────────────────
  # t=03:07  J = Intersect(n, p)
  point J = intersect n p
  # ────────────────────────────────────────────────────────
  # t=03:14  np = Reflect(n, m)
  line np = reflect n across m
  # ────────────────────────────────────────────────────────
  # t=03:27  K = Intersect(l, np)
  point K = intersect l np
  # ────────────────────────────────────────────────────────
  # t=03:37  Ip = Reflect(I, l)
  point Ip = reflect I across l
  # ────────────────────────────────────────────────────────
  # t=03:41  Jp = Reflect(J, l)
  point Jp = reflect J across l
  # ────────────────────────────────────────────────────────
  # t=03:50  pet = Polygon(H, J, I, K, Ip, Jp)
  polygon pet [ H J I K Ip Jp ]
  # ────────────────────────────────────────────────────────
  # de = Line(D, E)
  line de from D to E
  # ────────────────────────────────────────────────────────
  # t=05:34  reflRosette = Reflect(rosette, de)
  point G_reflRosette = reflect G across de
  # t=05:34  reflRosette = Reflect(rosette, de)
  polygon pet_reflRosette = reflect pet across de

pattern GimTvN9hw4U on GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # t=05:18  rosette = Sequence(Rotate(pet, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    edges from pet
  # ────────────────────────────────────────────────────────
  # t=06:04  tess = Sequence(Rotate(reflRosette, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    rotate 6 around G_reflRosette
      edges from pet_reflRosette
  palette pal
    Slab = #333333
    Gold = #d4af37
    Copper = #b87333

blueprint GimTvN9hw4U_border_scaffold
  circle bl center(-3, 0) radius 1
  circle br center(3, 0) radius 1
  circle ap center(0, 6) radius 1

pattern GimTvN9hw4U_border on GimTvN9hw4U_border_scaffold
  connect bl.mpt -> ap.mpt
  connect ap.mpt -> br.mpt

coaster Coaster
  outline polygon 6 $size rotate 30
  inscribe GimTvN9hw4U
  border GimTvN9hw4U_border width $border
  base 4
  relief straps emboss 1.2
  strap width 2
  color base Slab
  color straps Gold
  color border Copper
`},{id:`eight-fold-rosette-border`,title:`Eight-Fold Rosette · border`,blurb:`the square eight-fold coaster wrapped in a chevron band around the edge, in relief beside the art`,source:`# naqsh construction — 7apC5Q9QS-8
# title: Geogebra for Beginners 8-Fold Rosette Walkthrough
# url: https://www.youtube.com/watch?v=7apC5Q9QS-8
# steps: 144 statements, 144 tagged steps
# source: reconstructions/7apC5Q9QS-8/construction.ggb-commands sha256:aa7562d6e790f05ccd1a2e79b2cda43ec935fdc5561eb109896abbcb3265a8be

param size = 90 range 40..120   # mm, finished coaster side — the print knob
param border = 8 range 3..15   # mm, chevron band width, measured inward from the edge
param margin = 2 range 1..10   # mm, blank slab between the art and the edge
param unit = ($size - 2 * ($border + $margin)) / 4   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin
param pause1 = 1

blueprint c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=01:32  A = (0, 0)
  point A = unit.mpt
  # t=01:32  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:45  c = Circle(A, B)
  circle c center(A) through B
  # ────────────────────────────────────────────────────────
  # t=03:03  f = Line(A, B)
  line f from A to B
  # t=03:03  g = PerpendicularLine(A, f)
  line g through A perpendicular f
  # ────────────────────────────────────────────────────────
  # t=03:44  h = Rotate(f, 22.5°, A)
  line h = rotate f by 22.5 around A
  # t=03:44  i = Rotate(f, 45°, A)
  line i = rotate f by 45 around A
  # t=03:44  j = Rotate(f, 67.5°, A)
  line j = rotate f by 67.5 around A
  # t=03:44  k = Rotate(f, 112.5°, A)
  line k = rotate f by 112.5 around A
  # t=03:44  l = Rotate(f, 135°, A)
  line l = rotate f by 135 around A
  # t=03:44  m = Rotate(f, 157.5°, A)
  line m = rotate f by 157.5 around A
  # ────────────────────────────────────────────────────────
  # t=05:46  sqR = PerpendicularLine(B, f)
  line sqR through B perpendicular f
  # t=05:46  sqT = Rotate(sqR, 90°, A)
  line sqT = rotate sqR by 90 around A
  # t=05:46  sqL = Rotate(sqR, 180°, A)
  line sqL = rotate sqR by 180 around A
  # t=05:46  sqB = Rotate(sqR, 270°, A)
  line sqB = rotate sqR by 270 around A
  # t=05:46  P1 = Intersect(sqR, sqT)
  point P1 = intersect sqR sqT
  # t=05:46  P2 = Intersect(sqT, sqL)
  point P2 = intersect sqT sqL
  # t=05:46  P3 = Intersect(sqL, sqB)
  point P3 = intersect sqL sqB
  # t=05:46  P4 = Intersect(sqB, sqR)
  point P4 = intersect sqB sqR
  # t=05:46  sq = Polygon(P1, P2, P3, P4)
  polygon sq [ P1 P2 P3 P4 ]
  # ────────────────────────────────────────────────────────
  # t=06:50  D = (0, 1)
  point D = unit.cpt1
  # t=06:50  C = Intersect(k, sqT)
  point C = intersect k sqT
  # ────────────────────────────────────────────────────────
  # t=07:47  d = Circle(C, D)
  circle d center(C) through D
  # ────────────────────────────────────────────────────────
  # t=07:50  E = Intersect(d, k, 1)
  point E = intersect d k pick 1
  # ────────────────────────────────────────────────────────
  # t=08:24  p = Line(E, g)
  line p through E parallel g
  # ────────────────────────────────────────────────────────
  # t=09:20  p1 = Reflect(p, k)
  line p1 = reflect p across k
  # ────────────────────────────────────────────────────────
  # t=09:30  p2 = Reflect(p1, g)
  line p2 = reflect p1 across g
  # ────────────────────────────────────────────────────────
  # t=09:40  p3 = Reflect(p2, j)
  line p3 = reflect p2 across j
  # ────────────────────────────────────────────────────────
  # t=10:30  q = AngleBisector(D, C, E)
  line q = bisect angle D C E
  # ────────────────────────────────────────────────────────
  # t=10:50  p4 = Reflect(p, q)
  line p4 = reflect p across q
  # ────────────────────────────────────────────────────────
  # t=11:20  r = Reflect(p4, g)
  line r = reflect p4 across g
  # ────────────────────────────────────────────────────────
  # t=11:42  G = Intersect(p, p4)
  point G = intersect p p4
  # ────────────────────────────────────────────────────────
  # t=11:50  F = Intersect(p3, r)
  point F = intersect p3 r
  # ────────────────────────────────────────────────────────
  # t=11:56  H = Intersect(p1, p2)
  point H = intersect p1 p2
  # ────────────────────────────────────────────────────────
  # t=11:58  I = Intersect(p3, p2)
  point I = intersect p3 p2
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  polygon pet1 [ D G E H I F ]
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  polygon pet2 = reflect pet1 across j
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  polygon pet3 = reflect pet1 across i
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  polygon pet4 = reflect pet1 across h
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  polygon pet5 = reflect pet1 across f
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  polygon pet6 = reflect pet1 across m
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  polygon pet7 = reflect pet1 across l
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  polygon pet8 = reflect pet1 across k
  # ────────────────────────────────────────────────────────
  # t=13:15  L1 = Reflect(p4, l)
  line L1 = reflect p4 across l
  # ────────────────────────────────────────────────────────
  # t=13:20  O1 = Intersect(L1, sqT)
  point O1 = intersect L1 sqT
  # t=13:20  O2 = Intersect(L1, p4)
  point O2 = intersect L1 p4
  # t=13:20  O3 = Intersect(p4, sqL)
  point O3 = intersect p4 sqL
  # ────────────────────────────────────────────────────────
  # t=13:29  oct1 = Polygon(P2, O1, O2, O3)
  polygon oct1 [ P2 O1 O2 O3 ]
  # ────────────────────────────────────────────────────────
  # t=13:40  H2 = Rotate(H, 45°, A)
  point H2 = rotate H by 45 around A
  # t=13:40  H3 = Rotate(H, 90°, A)
  point H3 = rotate H by 90 around A
  # t=13:40  H4 = Rotate(H, 135°, A)
  point H4 = rotate H by 135 around A
  # t=13:40  H5 = Rotate(H, 180°, A)
  point H5 = rotate H by 180 around A
  # t=13:40  H6 = Rotate(H, 225°, A)
  point H6 = rotate H by 225 around A
  # t=13:40  H7 = Rotate(H, 270°, A)
  point H7 = rotate H by 270 around A
  # t=13:40  H8 = Rotate(H, 315°, A)
  point H8 = rotate H by 315 around A
  # ────────────────────────────────────────────────────────
  # t=13:52  pL1 = Reflect(p1, f)
  line pL1 = reflect p1 across f
  # ────────────────────────────────────────────────────────
  # t=13:56  pL2 = Reflect(p2, f)
  line pL2 = reflect p2 across f
  # ────────────────────────────────────────────────────────
  # t=14:00  pH1 = Reflect(p, i)
  line pH1 = reflect p across i
  # ────────────────────────────────────────────────────────
  # t=14:02  pH2 = Reflect(p3, i)
  line pH2 = reflect p3 across i
  # ────────────────────────────────────────────────────────
  # t=14:09  T22 = Intersect(h, p1)
  point T22 = intersect h p1
  # t=14:09  T67 = Intersect(j, p1)
  point T67 = intersect j p1
  # t=14:09  T112 = Intersect(k, p2)
  point T112 = intersect k p2
  # t=14:09  T157 = Intersect(m, p2)
  point T157 = intersect m p2
  # ────────────────────────────────────────────────────────
  # t=14:14  T202 = Intersect(h, pL2)
  point T202 = intersect h pL2
  # t=14:14  T247 = Intersect(j, pL2)
  point T247 = intersect j pL2
  # t=14:14  T292 = Intersect(k, pL1)
  point T292 = intersect k pL1
  # t=14:14  T337 = Intersect(m, pL1)
  point T337 = intersect m pL1
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  polygon star [ H T112 H2 T157 H3 T202 H4 T247 H5 T292 H6 T337 H7 T22 H8 T67 ]
  # ────────────────────────────────────────────────────────
  # t=14:43  oct2 = Reflect(oct1, g)
  polygon oct2 = reflect oct1 across g
  # ────────────────────────────────────────────────────────
  # t=15:10  oct3 = Reflect(oct1, f)
  polygon oct3 = reflect oct1 across f
  # ────────────────────────────────────────────────────────
  # t=15:15  oct4 = Reflect(oct2, f)
  polygon oct4 = reflect oct2 across f
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  polygon petN1 = reflect pet1 across sqT
  # t=19:05  petN2 = Reflect(pet2, sqT)
  polygon petN2 = reflect pet2 across sqT
  # t=19:05  petN8 = Reflect(pet8, sqT)
  polygon petN8 = reflect pet8 across sqT
  # t=19:05  petN3 = Reflect(pet3, sqT)
  polygon petN3 = reflect pet3 across sqT
  # t=19:05  petN7 = Reflect(pet7, sqT)
  polygon petN7 = reflect pet7 across sqT
  # t=19:05  starN = Reflect(star, sqT)
  polygon starN = reflect star across sqT
  # t=19:05  octN1 = Reflect(oct1, sqT)
  polygon octN1 = reflect oct1 across sqT
  # t=19:05  octN2 = Reflect(oct2, sqT)
  polygon octN2 = reflect oct2 across sqT
  # t=19:05  Bl = Rotate(B, 180°, A)
  point Bl = rotate B by 180 around A
  # t=19:05  Fa = Rotate(G, 270°, A)
  point Fa = rotate G by 270 around A
  # t=19:05  Fb = Rotate(F, 90°, A)
  point Fb = rotate F by 90 around A
  # t=19:05  I3 = Rotate(I, 90°, A)
  point I3 = rotate I by 90 around A
  # t=19:05  I8 = Rotate(I, 315°, A)
  point I8 = rotate I by 315 around A
  # t=19:05  petT3 = Polygon(B, Fa, I8, H7)
  polygon petT3 [ B Fa I8 H7 ]
  # t=19:05  petT7 = Polygon(Bl, Fb, I3, H3)
  polygon petT7 [ Bl Fb I3 H3 ]
  # t=19:05  starT = Polygon(H7, T22, H8, T67, H, T112, H2, T157, H3)
  polygon starT [ H7 T22 H8 T67 H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  polygon starNh = reflect starT across sqT
  # t=19:24  petN3h = Reflect(petT3, sqT)
  polygon petN3h = reflect petT3 across sqT
  # t=19:24  petN7h = Reflect(petT7, sqT)
  polygon petN7h = reflect petT7 across sqT
  # ────────────────────────────────────────────────────────
  # t=20:06  petL1 = Polygon(D, G, E, H)
  polygon petL1 [ D G E H ]
  # t=20:06  starQ2 = Polygon(A, H, T112, H2, T157, H3)
  polygon starQ2 [ A H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  polygon petW1 = reflect petN1 across l
  # t=20:54  petW2 = Reflect(petN2, l)
  polygon petW2 = reflect petN2 across l
  # t=20:54  petW8 = Reflect(petN8, l)
  polygon petW8 = reflect petN8 across l
  # t=20:54  petW3h = Reflect(petN3h, l)
  polygon petW3h = reflect petN3h across l
  # t=20:54  petW7h = Reflect(petN7h, l)
  polygon petW7h = reflect petN7h across l
  # t=20:54  starWh = Reflect(starNh, l)
  polygon starWh = reflect starNh across l
  # t=20:54  octW1 = Reflect(octN1, l)
  polygon octW1 = reflect octN1 across l
  # t=20:54  octW2 = Reflect(octN2, l)
  polygon octW2 = reflect octN2 across l
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  polygon petE1 = reflect petN1 across i
  # t=21:04  petE2 = Reflect(petN2, i)
  polygon petE2 = reflect petN2 across i
  # t=21:04  petE8 = Reflect(petN8, i)
  polygon petE8 = reflect petN8 across i
  # t=21:04  petE3h = Reflect(petN3h, i)
  polygon petE3h = reflect petN3h across i
  # t=21:04  petE7h = Reflect(petN7h, i)
  polygon petE7h = reflect petN7h across i
  # t=21:04  starEh = Reflect(starNh, i)
  polygon starEh = reflect starNh across i
  # t=21:04  octE1 = Reflect(octN1, i)
  polygon octE1 = reflect octN1 across i
  # t=21:04  octE2 = Reflect(octN2, i)
  polygon octE2 = reflect octN2 across i
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  polygon petS1 = reflect petN1 across f
  # t=21:35  petS2 = Reflect(petN2, f)
  polygon petS2 = reflect petN2 across f
  # t=21:35  petS8 = Reflect(petN8, f)
  polygon petS8 = reflect petN8 across f
  # t=21:35  petS3h = Reflect(petN3h, f)
  polygon petS3h = reflect petN3h across f
  # t=21:35  petS7h = Reflect(petN7h, f)
  polygon petS7h = reflect petN7h across f
  # t=21:35  starSh = Reflect(starNh, f)
  polygon starSh = reflect starNh across f
  # t=21:35  octS1 = Reflect(octN1, f)
  polygon octS1 = reflect octN1 across f
  # t=21:35  octS2 = Reflect(octN2, f)
  polygon octS2 = reflect octN2 across f
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  polygon petNW1 = rotate pet8 by 180 around P2
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  polygon petNW7h = rotate petT7 by 180 around P2
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  polygon petNW1h = rotate petL1 by 180 around P2
  # t=21:57  octNW = Rotate(oct1, 180°, P2)
  polygon octNW = rotate oct1 by 180 around P2
  # t=21:57  starNWh = Reflect(starNh, sqL)
  polygon starNWh = reflect starNh across sqL
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  polygon starNWq = rotate starQ2 by 180 around P2
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  polygon petNE1 = reflect petNW1 across g
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  polygon petNE7h = reflect petNW7h across g
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  polygon petNE1h = reflect petNW1h across g
  # t=22:44  octNE = Reflect(octNW, g)
  polygon octNE = reflect octNW across g
  # t=22:44  starNEq = Reflect(starNWq, g)
  polygon starNEq = reflect starNWq across g
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  polygon petSW1 = reflect petNW1 across f
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  polygon petSW7h = reflect petNW7h across f
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  polygon petSW1h = reflect petNW1h across f
  # t=22:58  octSW = Reflect(octNW, f)
  polygon octSW = reflect octNW across f
  # t=22:58  starSWq = Reflect(starNWq, f)
  polygon starSWq = reflect starNWq across f
  # t=22:58  petSE1 = Reflect(petNE1, f)
  polygon petSE1 = reflect petNE1 across f
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  polygon petSE7h = reflect petNE7h across f
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  polygon petSE1h = reflect petNE1h across f
  # t=22:58  octSE = Reflect(octNE, f)
  polygon octSE = reflect octNE across f
  # t=22:58  starSEq = Reflect(starNEq, f)
  polygon starSEq = reflect starNEq across f
  # ────────────────────────────────────────────────────────
  # t=23:10  Q0 = Reflect(O1, g)
  point Q0 = reflect O1 across g
  # t=23:10  Q1 = Reflect(O2, g)
  point Q1 = reflect O2 across g
  # t=23:10  octA = Polygon(O2, O1, 8)
  polygon octA = regular 8 from O2 to O1
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  polygon octB = regular 8 from Q0 to Q1
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  polygon octC = reflect octA across f
  # t=23:19  octD = Reflect(octB, f)
  polygon octD = reflect octB across f

pattern c_7apC5Q9QS_8 on c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  edges from pet1
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  edges from pet2
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  edges from pet3
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  edges from pet4
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  edges from pet5
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  edges from pet6
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  edges from pet7
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  edges from pet8
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  edges from star
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  edges from petN1
  # t=19:05  petN2 = Reflect(pet2, sqT)
  edges from petN2
  # t=19:05  petN8 = Reflect(pet8, sqT)
  edges from petN8
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  edges from starNh
  # t=19:24  petN3h = Reflect(petT3, sqT)
  edges from petN3h
  # t=19:24  petN7h = Reflect(petT7, sqT)
  edges from petN7h
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  edges from petW1
  # t=20:54  petW2 = Reflect(petN2, l)
  edges from petW2
  # t=20:54  petW8 = Reflect(petN8, l)
  edges from petW8
  # t=20:54  petW3h = Reflect(petN3h, l)
  edges from petW3h
  # t=20:54  petW7h = Reflect(petN7h, l)
  edges from petW7h
  # t=20:54  starWh = Reflect(starNh, l)
  edges from starWh
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  edges from petE1
  # t=21:04  petE2 = Reflect(petN2, i)
  edges from petE2
  # t=21:04  petE8 = Reflect(petN8, i)
  edges from petE8
  # t=21:04  petE3h = Reflect(petN3h, i)
  edges from petE3h
  # t=21:04  petE7h = Reflect(petN7h, i)
  edges from petE7h
  # t=21:04  starEh = Reflect(starNh, i)
  edges from starEh
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  edges from petS1
  # t=21:35  petS2 = Reflect(petN2, f)
  edges from petS2
  # t=21:35  petS8 = Reflect(petN8, f)
  edges from petS8
  # t=21:35  petS3h = Reflect(petN3h, f)
  edges from petS3h
  # t=21:35  petS7h = Reflect(petN7h, f)
  edges from petS7h
  # t=21:35  starSh = Reflect(starNh, f)
  edges from starSh
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  edges from petNW1
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  edges from petNW7h
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  edges from petNW1h
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  edges from starNWq
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  edges from petNE1
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  edges from petNE7h
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  edges from petNE1h
  # t=22:44  starNEq = Reflect(starNWq, g)
  edges from starNEq
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  edges from petSW1
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  edges from petSW7h
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  edges from petSW1h
  # t=22:58  starSWq = Reflect(starNWq, f)
  edges from starSWq
  # t=22:58  petSE1 = Reflect(petNE1, f)
  edges from petSE1
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  edges from petSE7h
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  edges from petSE1h
  # t=22:58  starSEq = Reflect(starNEq, f)
  edges from starSEq
  # ────────────────────────────────────────────────────────
  # t=23:10  octA = Polygon(O2, O1, 8)
  edges from octA
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  edges from octB
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  edges from octC
  # t=23:19  octD = Reflect(octB, f)
  edges from octD
  palette pal
    Slab = #333333
    Gold = #d4af37
    Copper = #b87333

blueprint c_7apC5Q9QS_8_border_scaffold
  circle bl center(-3, 0) radius 1
  circle br center(3, 0) radius 1
  circle ap center(0, 6) radius 1

pattern c_7apC5Q9QS_8_border on c_7apC5Q9QS_8_border_scaffold
  connect bl.mpt -> ap.mpt
  connect ap.mpt -> br.mpt

coaster Coaster
  outline square $size
  inscribe c_7apC5Q9QS_8
  border c_7apC5Q9QS_8_border width $border
  base 4
  relief straps emboss 1.2
  strap width 2
  color base Slab
  color straps Gold
  color border Copper
`},{id:`eight-fold-rosette-twist`,title:`Eight-Fold Rosette · twist`,blurb:`the eight-fold rosette extruded into a helical tower — every course rotated a little more than the one below, so the strap network winds as it rises`,source:`# naqsh construction — 7apC5Q9QS-8
# title: Geogebra for Beginners 8-Fold Rosette Walkthrough
# url: https://www.youtube.com/watch?v=7apC5Q9QS-8
# steps: 144 statements, 144 tagged steps
# source: reconstructions/7apC5Q9QS-8/construction.ggb-commands sha256:aa7562d6e790f05ccd1a2e79b2cda43ec935fdc5561eb109896abbcb3265a8be

param size = 90 range 40..120   # mm, finished coaster span across the strap network — the print knob
param strap = 3 range 1.6..5   # mm, strap width — the freestanding wall, floored at CAL-CST-07 (1.6 mm)
param height = 10 range 4..16   # mm, tower height the helix rises over — taller lowers the wall lean per CV12/CAL-CST-08
param twist = 5 range 0..30   # deg, total helix rotation over the full height (0 = a straight tower); CV12 caps the wall lean
param unit = ($size - $strap) / 4   # mm per GeoGebra unit — the art spans K units; the strap adds strap/2 each side

blueprint c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=01:32  A = (0, 0)
  point A = unit.mpt
  # t=01:32  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:45  c = Circle(A, B)
  circle c center(A) through B
  # ────────────────────────────────────────────────────────
  # t=03:03  f = Line(A, B)
  line f from A to B
  # t=03:03  g = PerpendicularLine(A, f)
  line g through A perpendicular f
  # ────────────────────────────────────────────────────────
  # t=03:44  h = Rotate(f, 22.5°, A)
  line h = rotate f by 22.5 around A
  # t=03:44  i = Rotate(f, 45°, A)
  line i = rotate f by 45 around A
  # t=03:44  j = Rotate(f, 67.5°, A)
  line j = rotate f by 67.5 around A
  # t=03:44  k = Rotate(f, 112.5°, A)
  line k = rotate f by 112.5 around A
  # t=03:44  l = Rotate(f, 135°, A)
  line l = rotate f by 135 around A
  # t=03:44  m = Rotate(f, 157.5°, A)
  line m = rotate f by 157.5 around A
  # ────────────────────────────────────────────────────────
  # t=05:46  sqR = PerpendicularLine(B, f)
  line sqR through B perpendicular f
  # t=05:46  sqT = Rotate(sqR, 90°, A)
  line sqT = rotate sqR by 90 around A
  # t=05:46  sqL = Rotate(sqR, 180°, A)
  line sqL = rotate sqR by 180 around A
  # t=05:46  sqB = Rotate(sqR, 270°, A)
  line sqB = rotate sqR by 270 around A
  # t=05:46  P1 = Intersect(sqR, sqT)
  point P1 = intersect sqR sqT
  # t=05:46  P2 = Intersect(sqT, sqL)
  point P2 = intersect sqT sqL
  # t=05:46  P3 = Intersect(sqL, sqB)
  point P3 = intersect sqL sqB
  # t=05:46  P4 = Intersect(sqB, sqR)
  point P4 = intersect sqB sqR
  # t=05:46  sq = Polygon(P1, P2, P3, P4)
  polygon sq [ P1 P2 P3 P4 ]
  # ────────────────────────────────────────────────────────
  # t=06:50  D = (0, 1)
  point D = unit.cpt1
  # t=06:50  C = Intersect(k, sqT)
  point C = intersect k sqT
  # ────────────────────────────────────────────────────────
  # t=07:47  d = Circle(C, D)
  circle d center(C) through D
  # ────────────────────────────────────────────────────────
  # t=07:50  E = Intersect(d, k, 1)
  point E = intersect d k pick 1
  # ────────────────────────────────────────────────────────
  # t=08:24  p = Line(E, g)
  line p through E parallel g
  # ────────────────────────────────────────────────────────
  # t=09:20  p1 = Reflect(p, k)
  line p1 = reflect p across k
  # ────────────────────────────────────────────────────────
  # t=09:30  p2 = Reflect(p1, g)
  line p2 = reflect p1 across g
  # ────────────────────────────────────────────────────────
  # t=09:40  p3 = Reflect(p2, j)
  line p3 = reflect p2 across j
  # ────────────────────────────────────────────────────────
  # t=10:30  q = AngleBisector(D, C, E)
  line q = bisect angle D C E
  # ────────────────────────────────────────────────────────
  # t=10:50  p4 = Reflect(p, q)
  line p4 = reflect p across q
  # ────────────────────────────────────────────────────────
  # t=11:20  r = Reflect(p4, g)
  line r = reflect p4 across g
  # ────────────────────────────────────────────────────────
  # t=11:42  G = Intersect(p, p4)
  point G = intersect p p4
  # ────────────────────────────────────────────────────────
  # t=11:50  F = Intersect(p3, r)
  point F = intersect p3 r
  # ────────────────────────────────────────────────────────
  # t=11:56  H = Intersect(p1, p2)
  point H = intersect p1 p2
  # ────────────────────────────────────────────────────────
  # t=11:58  I = Intersect(p3, p2)
  point I = intersect p3 p2
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  polygon pet1 [ D G E H I F ]
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  polygon pet2 = reflect pet1 across j
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  polygon pet3 = reflect pet1 across i
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  polygon pet4 = reflect pet1 across h
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  polygon pet5 = reflect pet1 across f
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  polygon pet6 = reflect pet1 across m
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  polygon pet7 = reflect pet1 across l
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  polygon pet8 = reflect pet1 across k
  # ────────────────────────────────────────────────────────
  # t=13:15  L1 = Reflect(p4, l)
  line L1 = reflect p4 across l
  # ────────────────────────────────────────────────────────
  # t=13:20  O1 = Intersect(L1, sqT)
  point O1 = intersect L1 sqT
  # t=13:20  O2 = Intersect(L1, p4)
  point O2 = intersect L1 p4
  # t=13:20  O3 = Intersect(p4, sqL)
  point O3 = intersect p4 sqL
  # ────────────────────────────────────────────────────────
  # t=13:29  oct1 = Polygon(P2, O1, O2, O3)
  polygon oct1 [ P2 O1 O2 O3 ]
  # ────────────────────────────────────────────────────────
  # t=13:40  H2 = Rotate(H, 45°, A)
  point H2 = rotate H by 45 around A
  # t=13:40  H3 = Rotate(H, 90°, A)
  point H3 = rotate H by 90 around A
  # t=13:40  H4 = Rotate(H, 135°, A)
  point H4 = rotate H by 135 around A
  # t=13:40  H5 = Rotate(H, 180°, A)
  point H5 = rotate H by 180 around A
  # t=13:40  H6 = Rotate(H, 225°, A)
  point H6 = rotate H by 225 around A
  # t=13:40  H7 = Rotate(H, 270°, A)
  point H7 = rotate H by 270 around A
  # t=13:40  H8 = Rotate(H, 315°, A)
  point H8 = rotate H by 315 around A
  # ────────────────────────────────────────────────────────
  # t=13:52  pL1 = Reflect(p1, f)
  line pL1 = reflect p1 across f
  # ────────────────────────────────────────────────────────
  # t=13:56  pL2 = Reflect(p2, f)
  line pL2 = reflect p2 across f
  # ────────────────────────────────────────────────────────
  # t=14:00  pH1 = Reflect(p, i)
  line pH1 = reflect p across i
  # ────────────────────────────────────────────────────────
  # t=14:02  pH2 = Reflect(p3, i)
  line pH2 = reflect p3 across i
  # ────────────────────────────────────────────────────────
  # t=14:09  T22 = Intersect(h, p1)
  point T22 = intersect h p1
  # t=14:09  T67 = Intersect(j, p1)
  point T67 = intersect j p1
  # t=14:09  T112 = Intersect(k, p2)
  point T112 = intersect k p2
  # t=14:09  T157 = Intersect(m, p2)
  point T157 = intersect m p2
  # ────────────────────────────────────────────────────────
  # t=14:14  T202 = Intersect(h, pL2)
  point T202 = intersect h pL2
  # t=14:14  T247 = Intersect(j, pL2)
  point T247 = intersect j pL2
  # t=14:14  T292 = Intersect(k, pL1)
  point T292 = intersect k pL1
  # t=14:14  T337 = Intersect(m, pL1)
  point T337 = intersect m pL1
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  polygon star [ H T112 H2 T157 H3 T202 H4 T247 H5 T292 H6 T337 H7 T22 H8 T67 ]
  # ────────────────────────────────────────────────────────
  # t=14:43  oct2 = Reflect(oct1, g)
  polygon oct2 = reflect oct1 across g
  # ────────────────────────────────────────────────────────
  # t=15:10  oct3 = Reflect(oct1, f)
  polygon oct3 = reflect oct1 across f
  # ────────────────────────────────────────────────────────
  # t=15:15  oct4 = Reflect(oct2, f)
  polygon oct4 = reflect oct2 across f
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  polygon petN1 = reflect pet1 across sqT
  # t=19:05  petN2 = Reflect(pet2, sqT)
  polygon petN2 = reflect pet2 across sqT
  # t=19:05  petN8 = Reflect(pet8, sqT)
  polygon petN8 = reflect pet8 across sqT
  # t=19:05  petN3 = Reflect(pet3, sqT)
  polygon petN3 = reflect pet3 across sqT
  # t=19:05  petN7 = Reflect(pet7, sqT)
  polygon petN7 = reflect pet7 across sqT
  # t=19:05  starN = Reflect(star, sqT)
  polygon starN = reflect star across sqT
  # t=19:05  octN1 = Reflect(oct1, sqT)
  polygon octN1 = reflect oct1 across sqT
  # t=19:05  octN2 = Reflect(oct2, sqT)
  polygon octN2 = reflect oct2 across sqT
  # t=19:05  Bl = Rotate(B, 180°, A)
  point Bl = rotate B by 180 around A
  # t=19:05  Fa = Rotate(G, 270°, A)
  point Fa = rotate G by 270 around A
  # t=19:05  Fb = Rotate(F, 90°, A)
  point Fb = rotate F by 90 around A
  # t=19:05  I3 = Rotate(I, 90°, A)
  point I3 = rotate I by 90 around A
  # t=19:05  I8 = Rotate(I, 315°, A)
  point I8 = rotate I by 315 around A
  # t=19:05  petT3 = Polygon(B, Fa, I8, H7)
  polygon petT3 [ B Fa I8 H7 ]
  # t=19:05  petT7 = Polygon(Bl, Fb, I3, H3)
  polygon petT7 [ Bl Fb I3 H3 ]
  # t=19:05  starT = Polygon(H7, T22, H8, T67, H, T112, H2, T157, H3)
  polygon starT [ H7 T22 H8 T67 H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  polygon starNh = reflect starT across sqT
  # t=19:24  petN3h = Reflect(petT3, sqT)
  polygon petN3h = reflect petT3 across sqT
  # t=19:24  petN7h = Reflect(petT7, sqT)
  polygon petN7h = reflect petT7 across sqT
  # ────────────────────────────────────────────────────────
  # t=20:06  petL1 = Polygon(D, G, E, H)
  polygon petL1 [ D G E H ]
  # t=20:06  starQ2 = Polygon(A, H, T112, H2, T157, H3)
  polygon starQ2 [ A H T112 H2 T157 H3 ]
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  polygon petW1 = reflect petN1 across l
  # t=20:54  petW2 = Reflect(petN2, l)
  polygon petW2 = reflect petN2 across l
  # t=20:54  petW8 = Reflect(petN8, l)
  polygon petW8 = reflect petN8 across l
  # t=20:54  petW3h = Reflect(petN3h, l)
  polygon petW3h = reflect petN3h across l
  # t=20:54  petW7h = Reflect(petN7h, l)
  polygon petW7h = reflect petN7h across l
  # t=20:54  starWh = Reflect(starNh, l)
  polygon starWh = reflect starNh across l
  # t=20:54  octW1 = Reflect(octN1, l)
  polygon octW1 = reflect octN1 across l
  # t=20:54  octW2 = Reflect(octN2, l)
  polygon octW2 = reflect octN2 across l
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  polygon petE1 = reflect petN1 across i
  # t=21:04  petE2 = Reflect(petN2, i)
  polygon petE2 = reflect petN2 across i
  # t=21:04  petE8 = Reflect(petN8, i)
  polygon petE8 = reflect petN8 across i
  # t=21:04  petE3h = Reflect(petN3h, i)
  polygon petE3h = reflect petN3h across i
  # t=21:04  petE7h = Reflect(petN7h, i)
  polygon petE7h = reflect petN7h across i
  # t=21:04  starEh = Reflect(starNh, i)
  polygon starEh = reflect starNh across i
  # t=21:04  octE1 = Reflect(octN1, i)
  polygon octE1 = reflect octN1 across i
  # t=21:04  octE2 = Reflect(octN2, i)
  polygon octE2 = reflect octN2 across i
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  polygon petS1 = reflect petN1 across f
  # t=21:35  petS2 = Reflect(petN2, f)
  polygon petS2 = reflect petN2 across f
  # t=21:35  petS8 = Reflect(petN8, f)
  polygon petS8 = reflect petN8 across f
  # t=21:35  petS3h = Reflect(petN3h, f)
  polygon petS3h = reflect petN3h across f
  # t=21:35  petS7h = Reflect(petN7h, f)
  polygon petS7h = reflect petN7h across f
  # t=21:35  starSh = Reflect(starNh, f)
  polygon starSh = reflect starNh across f
  # t=21:35  octS1 = Reflect(octN1, f)
  polygon octS1 = reflect octN1 across f
  # t=21:35  octS2 = Reflect(octN2, f)
  polygon octS2 = reflect octN2 across f
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  polygon petNW1 = rotate pet8 by 180 around P2
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  polygon petNW7h = rotate petT7 by 180 around P2
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  polygon petNW1h = rotate petL1 by 180 around P2
  # t=21:57  octNW = Rotate(oct1, 180°, P2)
  polygon octNW = rotate oct1 by 180 around P2
  # t=21:57  starNWh = Reflect(starNh, sqL)
  polygon starNWh = reflect starNh across sqL
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  polygon starNWq = rotate starQ2 by 180 around P2
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  polygon petNE1 = reflect petNW1 across g
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  polygon petNE7h = reflect petNW7h across g
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  polygon petNE1h = reflect petNW1h across g
  # t=22:44  octNE = Reflect(octNW, g)
  polygon octNE = reflect octNW across g
  # t=22:44  starNEq = Reflect(starNWq, g)
  polygon starNEq = reflect starNWq across g
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  polygon petSW1 = reflect petNW1 across f
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  polygon petSW7h = reflect petNW7h across f
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  polygon petSW1h = reflect petNW1h across f
  # t=22:58  octSW = Reflect(octNW, f)
  polygon octSW = reflect octNW across f
  # t=22:58  starSWq = Reflect(starNWq, f)
  polygon starSWq = reflect starNWq across f
  # t=22:58  petSE1 = Reflect(petNE1, f)
  polygon petSE1 = reflect petNE1 across f
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  polygon petSE7h = reflect petNE7h across f
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  polygon petSE1h = reflect petNE1h across f
  # t=22:58  octSE = Reflect(octNE, f)
  polygon octSE = reflect octNE across f
  # t=22:58  starSEq = Reflect(starNEq, f)
  polygon starSEq = reflect starNEq across f
  # ────────────────────────────────────────────────────────
  # t=23:10  Q0 = Reflect(O1, g)
  point Q0 = reflect O1 across g
  # t=23:10  Q1 = Reflect(O2, g)
  point Q1 = reflect O2 across g
  # t=23:10  octA = Polygon(O2, O1, 8)
  polygon octA = regular 8 from O2 to O1
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  polygon octB = regular 8 from Q0 to Q1
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  polygon octC = reflect octA across f
  # t=23:19  octD = Reflect(octB, f)
  polygon octD = reflect octB across f

pattern c_7apC5Q9QS_8 on c_7apC5Q9QS_8_scaffold
  # ────────────────────────────────────────────────────────
  # t=12:09  pet1 = Polygon(D, G, E, H, I, F)
  edges from pet1
  # ────────────────────────────────────────────────────────
  # t=12:24  pet2 = Reflect(pet1, j)
  edges from pet2
  # ────────────────────────────────────────────────────────
  # t=12:29  pet3 = Reflect(pet1, i)
  edges from pet3
  # ────────────────────────────────────────────────────────
  # t=12:32  pet4 = Reflect(pet1, h)
  edges from pet4
  # ────────────────────────────────────────────────────────
  # t=12:35  pet5 = Reflect(pet1, f)
  edges from pet5
  # ────────────────────────────────────────────────────────
  # t=12:41  pet6 = Reflect(pet1, m)
  edges from pet6
  # ────────────────────────────────────────────────────────
  # t=13:05  pet7 = Reflect(pet1, l)
  edges from pet7
  # ────────────────────────────────────────────────────────
  # t=13:10  pet8 = Reflect(pet1, k)
  edges from pet8
  # ────────────────────────────────────────────────────────
  # t=14:34  star = Polygon(H, T112, H2, T157, H3, T202, H4, T247, H5, T292, H6, T337, H7, T22, H8, T67)
  edges from star
  # ────────────────────────────────────────────────────────
  # t=19:05  petN1 = Reflect(pet1, sqT)
  edges from petN1
  # t=19:05  petN2 = Reflect(pet2, sqT)
  edges from petN2
  # t=19:05  petN8 = Reflect(pet8, sqT)
  edges from petN8
  # ────────────────────────────────────────────────────────
  # t=19:24  starNh = Reflect(starT, sqT)
  edges from starNh
  # t=19:24  petN3h = Reflect(petT3, sqT)
  edges from petN3h
  # t=19:24  petN7h = Reflect(petT7, sqT)
  edges from petN7h
  # ────────────────────────────────────────────────────────
  # t=20:54  petW1 = Reflect(petN1, l)
  edges from petW1
  # t=20:54  petW2 = Reflect(petN2, l)
  edges from petW2
  # t=20:54  petW8 = Reflect(petN8, l)
  edges from petW8
  # t=20:54  petW3h = Reflect(petN3h, l)
  edges from petW3h
  # t=20:54  petW7h = Reflect(petN7h, l)
  edges from petW7h
  # t=20:54  starWh = Reflect(starNh, l)
  edges from starWh
  # ────────────────────────────────────────────────────────
  # t=21:04  petE1 = Reflect(petN1, i)
  edges from petE1
  # t=21:04  petE2 = Reflect(petN2, i)
  edges from petE2
  # t=21:04  petE8 = Reflect(petN8, i)
  edges from petE8
  # t=21:04  petE3h = Reflect(petN3h, i)
  edges from petE3h
  # t=21:04  petE7h = Reflect(petN7h, i)
  edges from petE7h
  # t=21:04  starEh = Reflect(starNh, i)
  edges from starEh
  # ────────────────────────────────────────────────────────
  # t=21:35  petS1 = Reflect(petN1, f)
  edges from petS1
  # t=21:35  petS2 = Reflect(petN2, f)
  edges from petS2
  # t=21:35  petS8 = Reflect(petN8, f)
  edges from petS8
  # t=21:35  petS3h = Reflect(petN3h, f)
  edges from petS3h
  # t=21:35  petS7h = Reflect(petN7h, f)
  edges from petS7h
  # t=21:35  starSh = Reflect(starNh, f)
  edges from starSh
  # ────────────────────────────────────────────────────────
  # t=21:57  petNW1 = Rotate(pet8, 180°, P2)
  edges from petNW1
  # t=21:57  petNW7h = Rotate(petT7, 180°, P2)
  edges from petNW7h
  # t=21:57  petNW1h = Rotate(petL1, 180°, P2)
  edges from petNW1h
  # ────────────────────────────────────────────────────────
  # t=22:20  starNWq = Rotate(starQ2, 180°, P2)
  edges from starNWq
  # ────────────────────────────────────────────────────────
  # t=22:44  petNE1 = Reflect(petNW1, g)
  edges from petNE1
  # t=22:44  petNE7h = Reflect(petNW7h, g)
  edges from petNE7h
  # t=22:44  petNE1h = Reflect(petNW1h, g)
  edges from petNE1h
  # t=22:44  starNEq = Reflect(starNWq, g)
  edges from starNEq
  # ────────────────────────────────────────────────────────
  # t=22:58  petSW1 = Reflect(petNW1, f)
  edges from petSW1
  # t=22:58  petSW7h = Reflect(petNW7h, f)
  edges from petSW7h
  # t=22:58  petSW1h = Reflect(petNW1h, f)
  edges from petSW1h
  # t=22:58  starSWq = Reflect(starNWq, f)
  edges from starSWq
  # t=22:58  petSE1 = Reflect(petNE1, f)
  edges from petSE1
  # t=22:58  petSE7h = Reflect(petNE7h, f)
  edges from petSE7h
  # t=22:58  petSE1h = Reflect(petNE1h, f)
  edges from petSE1h
  # t=22:58  starSEq = Reflect(starNEq, f)
  edges from starSEq
  # ────────────────────────────────────────────────────────
  # t=23:10  octA = Polygon(O2, O1, 8)
  edges from octA
  # t=23:10  octB = Polygon(Q0, Q1, 8)
  edges from octB
  # ────────────────────────────────────────────────────────
  # t=23:19  octC = Reflect(octA, f)
  edges from octC
  # t=23:19  octD = Reflect(octB, f)
  edges from octD

coaster Coaster
  outline pattern
  inscribe c_7apC5Q9QS_8
  base $height
  strap width $strap
  twist $twist
`},{id:`six-fold-rosette-twist`,title:`Six-Fold Rosette · twist`,blurb:`the six-fold star rosette extruded into a helical tower — the strap network winds as it rises, holes open between the straps`,source:`# naqsh construction — GimTvN9hw4U
# title: Simple 20-step Six-Fold Star Rosette
# url: https://www.youtube.com/watch?v=GimTvN9hw4U
# steps: 26 statements, 25 tagged steps
# source: reconstructions/GimTvN9hw4U/construction.ggb-commands sha256:6838767cbb24116b0e5986e62e05a0726b246b8ce0028dc1714fc7194525022e
# renamed: rosette -> rosette_ (reserved word)

param size = 90 range 40..120   # mm, finished coaster span across the strap network — the print knob
param strap = 3 range 1.6..5   # mm, strap width — the freestanding wall, floored at CAL-CST-07 (1.6 mm)
param height = 10 range 4..16   # mm, tower height the helix rises over — taller lowers the wall lean per CV12/CAL-CST-08
param twist = 5 range 0..30   # deg, total helix rotation over the full height (0 = a straight tower); CV12 caps the wall lean
param unit = ($size - $strap) / 4.5001   # mm per GeoGebra unit — the art spans K units; the strap adds strap/2 each side

blueprint GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=00:43  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=00:59  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:15  C = Rotate(A, -120°, B)
  point C = rotate A by -120 around B
  # t=01:15  D = Rotate(B, -120°, C)
  point D = rotate B by -120 around C
  # t=01:15  E = Rotate(C, -120°, D)
  point E = rotate C by -120 around D
  # t=01:15  F = Rotate(D, -120°, E)
  point F = rotate D by -120 around E
  # ────────────────────────────────────────────────────────
  # t=01:31  poly1 = Polygon(A, B, C, D, E, F)
  polygon poly1 [ A B C D E F ]
  # ────────────────────────────────────────────────────────
  # t=01:39  l = PerpendicularBisector(A, B)
  bisector l from A to B
  # ────────────────────────────────────────────────────────
  # t=01:44  m = PerpendicularBisector(A, C)
  bisector m from A to C
  # ────────────────────────────────────────────────────────
  # t=01:51  G = Intersect(l, m)
  point G = intersect l m
  # ────────────────────────────────────────────────────────
  # t=01:54  f = Line(A, B)
  line f from A to B
  # ────────────────────────────────────────────────────────
  # t=01:57  H = Intersect(l, f)
  point H = intersect l f
  # ────────────────────────────────────────────────────────
  # t=02:00  c = Circle(B, H)
  circle c center(B) through H
  # ────────────────────────────────────────────────────────
  # t=02:08  I = Midpoint(A, C)
  point I = midpoint A C
  # ────────────────────────────────────────────────────────
  # t=02:36  n = Line(I, l)
  line n through I parallel l
  # ────────────────────────────────────────────────────────
  # t=02:53  p = Line(B, F)
  line p from B to F
  # ────────────────────────────────────────────────────────
  # t=03:07  J = Intersect(n, p)
  point J = intersect n p
  # ────────────────────────────────────────────────────────
  # t=03:14  np = Reflect(n, m)
  line np = reflect n across m
  # ────────────────────────────────────────────────────────
  # t=03:27  K = Intersect(l, np)
  point K = intersect l np
  # ────────────────────────────────────────────────────────
  # t=03:37  Ip = Reflect(I, l)
  point Ip = reflect I across l
  # ────────────────────────────────────────────────────────
  # t=03:41  Jp = Reflect(J, l)
  point Jp = reflect J across l
  # ────────────────────────────────────────────────────────
  # t=03:50  pet = Polygon(H, J, I, K, Ip, Jp)
  polygon pet [ H J I K Ip Jp ]
  # ────────────────────────────────────────────────────────
  # de = Line(D, E)
  line de from D to E
  # ────────────────────────────────────────────────────────
  # t=05:34  reflRosette = Reflect(rosette, de)
  point G_reflRosette = reflect G across de
  # t=05:34  reflRosette = Reflect(rosette, de)
  polygon pet_reflRosette = reflect pet across de

pattern GimTvN9hw4U on GimTvN9hw4U_scaffold
  # ────────────────────────────────────────────────────────
  # t=05:18  rosette = Sequence(Rotate(pet, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    edges from pet
  # ────────────────────────────────────────────────────────
  # t=06:04  tess = Sequence(Rotate(reflRosette, pi*i/3, G), i, 0, 5)
  rotate 6 around G
    rotate 6 around G_reflRosette
      edges from pet_reflRosette

coaster Coaster
  outline pattern
  inscribe GimTvN9hw4U
  base $height
  strap width $strap
  twist $twist
`},{id:`rDuxHF3xMOc`,title:`Eight-Fold Star Rosette`,blurb:`a coaster carrying the eight-fold star rosette reconstructed from the "with sequences" GeoGebra walkthrough`,source:`# naqsh construction — rDuxHF3xMOc
# title: 8-fold star rosette with sequences in GeoGebra
# url: https://www.youtube.com/watch?v=rDuxHF3xMOc
# steps: 47 statements, 47 tagged steps
# source: reconstructions/rDuxHF3xMOc/construction.ggb-commands sha256:f964d2ea6dd813ecd624bf12a7c67db55d4c3e2045b07d041ce38d40ab9f9132
# renamed: L' -> L_p (apostrophe is not an identifier character)
# renamed: K' -> K_p (apostrophe is not an identifier character)
# renamed: M' -> M_p (apostrophe is not an identifier character)
# renamed: m2' -> m2_p (apostrophe is not an identifier character)
# renamed: l1' -> l1_p (apostrophe is not an identifier character)

param size = 90 range 40..120   # mm, finished coaster side — the print knob
param margin = 2 range 1..10   # mm, blank slab between the art and the edge
param unit = ($size - 2 * $margin) / 4.8285   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin

blueprint rDuxHF3xMOc_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=01:09  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=01:12  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=01:49  C = Rotate(A, -135°, B)
  point C = rotate A by -135 around B
  # t=01:49  D = Rotate(B, -135°, C)
  point D = rotate B by -135 around C
  # t=01:49  E = Rotate(C, -135°, D)
  point E = rotate C by -135 around D
  # t=01:49  F = Rotate(D, -135°, E)
  point F = rotate D by -135 around E
  # t=01:49  G = Rotate(E, -135°, F)
  point G = rotate E by -135 around F
  # t=01:49  H = Rotate(F, -135°, G)
  point H = rotate F by -135 around G
  # ────────────────────────────────────────────────────────
  # t=01:53  poly1 = Polygon(A, B, C, D, E, F, G, H)
  polygon poly1 [ A B C D E F G H ]
  # ────────────────────────────────────────────────────────
  # t=02:11  bot = Line(A, B)
  line bot from A to B
  # ────────────────────────────────────────────────────────
  # t=02:13  rgt = Line(C, D)
  line rgt from C to D
  # ────────────────────────────────────────────────────────
  # t=02:15  top = Line(E, F)
  line top from E to F
  # ────────────────────────────────────────────────────────
  # t=02:17  lft = Line(G, H)
  line lft from G to H
  # ────────────────────────────────────────────────────────
  # t=02:29  s   = PerpendicularBisector(A, B)
  bisector s from A to B
  # ────────────────────────────────────────────────────────
  # t=02:33  rad = PerpendicularBisector(A, C)
  bisector rad from A to C
  # ────────────────────────────────────────────────────────
  # t=02:47  O   = Intersect(s, rad)
  point O = intersect s rad
  # ────────────────────────────────────────────────────────
  # t=03:05  I   = Intersect(s, bot)
  point I = intersect s bot
  # ────────────────────────────────────────────────────────
  # t=03:18  gBC = Segment(B, C)
  segment gBC from B to C
  # ────────────────────────────────────────────────────────
  # t=03:22  c   = Circle(B, I)
  circle c center(B) through I
  # ────────────────────────────────────────────────────────
  # t=03:26  J   = Rotate(I, -135°, B)
  point J = rotate I by -135 around B
  # ────────────────────────────────────────────────────────
  # t=03:48  K   = Intersect(c, rad, 2)
  point K = intersect c rad pick 2
  # ────────────────────────────────────────────────────────
  # t=04:11  pl  = Line(K, s)
  line pl through K parallel s
  # ────────────────────────────────────────────────────────
  # t=04:38  bis = AngleBisector(A, B, O)
  line bis = bisect angle A B O
  # ────────────────────────────────────────────────────────
  # t=04:57  L   = Intersect(pl, bis)
  point L = intersect pl bis
  # ────────────────────────────────────────────────────────
  # t=05:08  plr = Reflect(pl, rad)
  line plr = reflect pl across rad
  # ────────────────────────────────────────────────────────
  # t=05:14  M   = Intersect(plr, s)
  point M = intersect plr s
  # ────────────────────────────────────────────────────────
  # t=05:20  L'  = Reflect(L, s)
  point L_p = reflect L across s
  # ────────────────────────────────────────────────────────
  # t=05:23  K'  = Reflect(K, s)
  point K_p = reflect K across s
  # ────────────────────────────────────────────────────────
  # t=05:31  poly2 = Polygon(I, L, K, M, K', L')
  polygon poly2 [ I L K M K_p L_p ]
  # ────────────────────────────────────────────────────────
  # t=05:58  plrs = Reflect(plr, s)
  line plrs = reflect plr across s
  # ────────────────────────────────────────────────────────
  # t=06:06  N    = Intersect(plrs, rad)
  point N = intersect plrs rad
  # ────────────────────────────────────────────────────────
  # t=06:14  M'   = Reflect(M, rad)
  point M_p = reflect M across rad
  # ────────────────────────────────────────────────────────
  # t=06:21  q1   = Polygon(K, M, N, M')
  polygon q1 [ K M N M_p ]
  # ────────────────────────────────────────────────────────
  # t=06:40  lIJ  = Line(I, J)
  line lIJ from I to J
  # ────────────────────────────────────────────────────────
  # t=06:57  P    = Intersect(lIJ, plr)
  point P = intersect lIJ plr
  # ────────────────────────────────────────────────────────
  # t=07:09  lIJr = Reflect(lIJ, gBC)
  line lIJr = reflect lIJ across gBC
  # ────────────────────────────────────────────────────────
  # t=07:20  Q    = Intersect(lIJr, bot)
  point Q = intersect lIJr bot
  # ────────────────────────────────────────────────────────
  # t=07:29  poly3 = Polygon(I, L, K, P, J, Q)
  polygon poly3 [ I L K P J Q ]
  # ────────────────────────────────────────────────────────
  # t=07:41  S    = Intersect(bot, rgt)
  point S = intersect bot rgt
  # ────────────────────────────────────────────────────────
  # t=07:43  R    = Intersect(lIJ, rgt)
  point R = intersect lIJ rgt
  # ────────────────────────────────────────────────────────
  # t=07:51  q2   = Polygon(S, R, J, Q)
  polygon q2 [ S R J Q ]
  # ────────────────────────────────────────────────────────
  # t=13:58  m2' = Reflect(m2, s)
  point O_m2_p = reflect O across s
  # t=13:58  m2' = Reflect(m2, s)
  polygon poly3_m2_p = reflect poly3 across s
  # ────────────────────────────────────────────────────────
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  point O_l1 = reflect O across lft
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  polygon q1_l1 = reflect q1 across lft
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  polygon poly2_l1 = reflect poly2 across lft
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  point O_l12 = reflect O across lft
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  polygon poly3_l1 = reflect poly3 across lft
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  point O_l13 = reflect O across lft
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  polygon q2_l1 = reflect q2 across lft
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  point O_m2_p_l1 = reflect O_m2_p across lft
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  polygon poly3_m2_p_l1 = reflect poly3_m2_p across lft
  # ────────────────────────────────────────────────────────
  # t=17:04  l1' = Reflect(l1, top)
  point O_l1_l1_p = reflect O_l1 across top
  # t=17:04  l1' = Reflect(l1, top)
  polygon q1_l1_l1_p = reflect q1_l1 across top
  # t=17:04  l1' = Reflect(l1, top)
  polygon poly2_l1_l1_p = reflect poly2_l1 across top
  # t=17:04  l1' = Reflect(l1, top)
  point O_l12_l1_p = reflect O_l12 across top
  # t=17:04  l1' = Reflect(l1, top)
  polygon poly3_l1_l1_p = reflect poly3_l1 across top
  # t=17:04  l1' = Reflect(l1, top)
  point O_l13_l1_p = reflect O_l13 across top
  # t=17:04  l1' = Reflect(l1, top)
  polygon q2_l1_l1_p = reflect q2_l1 across top
  # t=17:04  l1' = Reflect(l1, top)
  point O_m2_p_l1_l1_p = reflect O_m2_p_l1 across top
  # t=17:04  l1' = Reflect(l1, top)
  polygon poly3_m2_p_l1_l1_p = reflect poly3_m2_p_l1 across top
  # ────────────────────────────────────────────────────────
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  point O_coaster_fill = reflect O across top
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  polygon q1_coaster_fill = reflect q1 across top
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  polygon poly2_coaster_fill = reflect poly2 across top
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  point O_coaster_fill2 = reflect O across top
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  polygon poly3_coaster_fill = reflect poly3 across top
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  point O_coaster_fill3 = reflect O across top
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  polygon q2_coaster_fill = reflect q2 across top
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  point O_m2_p_coaster_fill = reflect O_m2_p across top
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  polygon poly3_m2_p_coaster_fill = reflect poly3_m2_p across top

pattern rDuxHF3xMOc on rDuxHF3xMOc_scaffold
  # ────────────────────────────────────────────────────────
  # t=11:34  m1 = Sequence(Rotate({q1, poly2}, i * 45°, O), i, 0, 7)
  rotate 8 around O
    edges from q1
    edges from poly2
  # ────────────────────────────────────────────────────────
  # t=13:32  m2 = Sequence(Rotate({poly3}, i * 90°, O), i, 0, 3)
  rotate 4 around O
    edges from poly3
  # ────────────────────────────────────────────────────────
  # t=13:58  m2' = Reflect(m2, s)
  rotate 4 around O_m2_p
    edges from poly3_m2_p
  # ────────────────────────────────────────────────────────
  # t=14:40  m3 = Sequence(Rotate({q2}, i * 90°, O), i, 0, 3)
  rotate 4 around O
    edges from q2
  # ────────────────────────────────────────────────────────
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  rotate 8 around O_l1
    edges from q1_l1
    edges from poly2_l1
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  rotate 4 around O_l12
    edges from poly3_l1
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  rotate 4 around O_l13
    edges from q2_l1
  # t=16:43  l1  = Reflect({m1, m2, m3, m2'}, lft)
  rotate 4 around O_m2_p_l1
    edges from poly3_m2_p_l1
  # ────────────────────────────────────────────────────────
  # t=17:04  l1' = Reflect(l1, top)
  rotate 8 around O_l1_l1_p
    edges from q1_l1_l1_p
    edges from poly2_l1_l1_p
  # t=17:04  l1' = Reflect(l1, top)
  rotate 4 around O_l12_l1_p
    edges from poly3_l1_l1_p
  # t=17:04  l1' = Reflect(l1, top)
  rotate 4 around O_l13_l1_p
    edges from q2_l1_l1_p
  # t=17:04  l1' = Reflect(l1, top)
  rotate 4 around O_m2_p_l1_l1_p
    edges from poly3_m2_p_l1_l1_p
  # ────────────────────────────────────────────────────────
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  rotate 8 around O_coaster_fill
    edges from q1_coaster_fill
    edges from poly2_coaster_fill
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  rotate 4 around O_coaster_fill2
    edges from poly3_coaster_fill
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  rotate 4 around O_coaster_fill3
    edges from q2_coaster_fill
  # coaster_fill = Reflect({m1, m2, m3, m2'}, top)   # coaster only — not in the video
  rotate 4 around O_m2_p_coaster_fill
    edges from poly3_m2_p_coaster_fill
  palette pal
    Slab = #333333
    Gold = #d4af37

coaster Coaster
  outline square $size
  inscribe rDuxHF3xMOc
  base 4
  relief straps emboss 1.2
  strap width 2
  color base Slab
  color straps Gold
`},{id:`sDO9fpu76v8`,title:`Royal Alcazar Tessellation`,blurb:`a coaster carrying the six-fold reflection tessellation from the Royal Alcazar of Seville`,source:`# naqsh construction — sDO9fpu76v8
# title: Royal Alcazar 6-fold reflection tessellation
# url: https://www.youtube.com/watch?v=sDO9fpu76v8
# steps: 87 statements, 77 tagged steps
# source: reconstructions/sDO9fpu76v8/construction.ggb-commands sha256:ffb1ca403e4af5c6dac560c88b1037d897b0365b34f65aaa064681426c2ff78e

param size = 90 range 40..120   # mm, finished coaster span across flats — the print knob
param margin = 2 range 1..10   # mm, blank slab between the art and the edge
param unit = ($size - 2 * $margin) / 6.5397   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin
param G = 0.33333333333

blueprint sDO9fpu76v8_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=00:57  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=01:05  B = (0, 1)
  point B = unit.cpt1
  # ────────────────────────────────────────────────────────
  # t=01:26  poly1 = Polygon(A, B, 6)
  polygon poly1 = regular 6 from A to B
  # ────────────────────────────────────────────────────────
  # t=02:33  cG = Circle(A, G)
  circle cG center(A) radius $G * $unit
  # ────────────────────────────────────────────────────────
  # t=02:50  segAB = Segment(A, B)
  segment segAB from A to B
  # ────────────────────────────────────────────────────────
  # t=02:53  H = Intersect(cG, segAB)
  point H = intersect cG segAB
  # ────────────────────────────────────────────────────────
  # t=03:06  cB = Circle(B, G)
  circle cB center(B) radius $G * $unit
  # ────────────────────────────────────────────────────────
  # t=03:10  J = Intersect(cB, segAB)
  point J = intersect cB segAB
  # ────────────────────────────────────────────────────────
  # t=03:15  I = Midpoint(A, B)
  point I = midpoint A B
  # ────────────────────────────────────────────────────────
  # t=03:23  cI = Circle(I, G)
  circle cI center(I) radius $G * $unit
  # ────────────────────────────────────────────────────────
  # t=03:55  O = Centroid(poly1)
  point O = centroid poly1
  # ────────────────────────────────────────────────────────
  # t=03:50  lAD = Line(A, O)
  line lAD from A to O
  # ────────────────────────────────────────────────────────
  # t=03:52  lBE = Line(B, O)
  line lBE from B to O
  # ────────────────────────────────────────────────────────
  # t=04:00  axisN = Line(O, I)
  line axisN from O to I
  # ────────────────────────────────────────────────────────
  # t=04:06  p = PerpendicularLine(J, segAB)
  line p through J perpendicular segAB
  # ────────────────────────────────────────────────────────
  # t=04:11  q = PerpendicularLine(H, segAB)
  line q through H perpendicular segAB
  # ────────────────────────────────────────────────────────
  # t=04:22  {Llo, L} = Intersect(cI, axisN)
  intersect LloL_ cI axisN
  # t=04:22  {Llo, L} = Intersect(cI, axisN)
  point Llo = LloL_.cpt0
  # t=04:22  {Llo, L} = Intersect(cI, axisN)
  point L = LloL_.cpt1
  # ────────────────────────────────────────────────────────
  # t=04:49  nR = Reflect(axisN, lAD)
  line nR = reflect axisN across lAD
  # ────────────────────────────────────────────────────────
  # t=04:51  pR = Reflect(p, lAD)
  line pR = reflect p across lAD
  # ────────────────────────────────────────────────────────
  # t=04:53  qR = Reflect(q, lAD)
  line qR = reflect q across lAD
  # ────────────────────────────────────────────────────────
  # t=05:04  r = PerpendicularLine(O, axisN)
  line r through O perpendicular axisN
  # ────────────────────────────────────────────────────────
  # t=05:09  nRR = Reflect(nR, r)
  line nRR = reflect nR across r
  # ────────────────────────────────────────────────────────
  # t=05:11  pRR = Reflect(pR, r)
  line pRR = reflect pR across r
  # ────────────────────────────────────────────────────────
  # t=05:13  qRR = Reflect(qR, r)
  line qRR = reflect qR across r
  # ────────────────────────────────────────────────────────
  # t=05:53  s = PerpendicularLine(L, axisN)
  line s through L perpendicular axisN
  # ────────────────────────────────────────────────────────
  # t=06:05  sR = Reflect(s, lAD)
  line sR = reflect s across lAD
  # ────────────────────────────────────────────────────────
  # t=06:07  sRR = Reflect(sR, r)
  line sRR = reflect sR across r
  # ────────────────────────────────────────────────────────
  # t=06:24  t = PerpendicularBisector(L, I)
  bisector t from L to I
  # ────────────────────────────────────────────────────────
  # t=06:30  tR = Reflect(t, lAD)
  line tR = reflect t across lAD
  # ────────────────────────────────────────────────────────
  # t=06:32  tRR = Reflect(tR, r)
  line tRR = reflect tR across r
  # ────────────────────────────────────────────────────────
  # t=07:08  K = Intersect(nR, tR)
  point K = intersect nR tR
  # ────────────────────────────────────────────────────────
  # t=07:26  {aPerp, a} = AngleBisector(r, nR)
  line aPerp = bisect angle r nR
  # t=07:26  {aPerp, a} = AngleBisector(r, nR)
  line a = bisect angle r nR other
  # ────────────────────────────────────────────────────────
  # t=07:50  pRR1 = Reflect(pR, a)
  line pRR1 = reflect pR across a
  # ────────────────────────────────────────────────────────
  # t=07:53  qRR1 = Reflect(qR, a)
  line qRR1 = reflect qR across a
  # ────────────────────────────────────────────────────────
  # t=08:12  f1 = Reflect(pRR1, nRR)
  line f1 = reflect pRR1 across nRR
  # ────────────────────────────────────────────────────────
  # t=08:14  b = Reflect(qRR1, nRR)
  line b = reflect qRR1 across nRR
  # ────────────────────────────────────────────────────────
  # t=08:20  g1 = Reflect(f1, axisN)
  line g1 = reflect f1 across axisN
  # ────────────────────────────────────────────────────────
  # t=08:23  bp = Reflect(b, axisN)
  line bp = reflect b across axisN
  # ────────────────────────────────────────────────────────
  # t=08:44  M = Intersect(lAD, t)
  point M = intersect lAD t
  # ────────────────────────────────────────────────────────
  # t=08:58  h1 = PerpendicularLine(M, r)
  line h1 through M perpendicular r
  # ────────────────────────────────────────────────────────
  # t=09:17  N0 = Intersect(qR, g1)
  point N0 = intersect qR g1
  # ────────────────────────────────────────────────────────
  # t=09:19  P0 = Intersect(lAD, qR)
  point P0 = intersect lAD qR
  # ────────────────────────────────────────────────────────
  # t=09:21  Q0 = Intersect(q, pRR1)
  point Q0 = intersect q pRR1
  # ────────────────────────────────────────────────────────
  # t=09:24  R0 = Intersect(nR, g1)
  point R0 = intersect nR g1
  # ────────────────────────────────────────────────────────
  # t=09:32  kite = Polygon(N0, P0, Q0, R0)
  polygon kite [ N0 P0 Q0 R0 ]
  # ────────────────────────────────────────────────────────
  # t=09:38  S0 = Reflect(H, lAD)
  point S0 = reflect H across lAD
  # ────────────────────────────────────────────────────────
  # t=09:40  T0 = Intersect(g1, h1)
  point T0 = intersect g1 h1
  # ────────────────────────────────────────────────────────
  # t=09:43  tri = Polygon(S0, N0, T0)
  polygon tri [ S0 N0 T0 ]
  # ────────────────────────────────────────────────────────
  # lAF = Line(A, S0)
  line lAF from A to S0
  # ────────────────────────────────────────────────────────
  # t=10:08  iK = Line(K, S0)
  line iK from K to S0
  # ────────────────────────────────────────────────────────
  # t=10:48  {jK2, jK} = AngleBisector(iK, nR)
  line jK2 = bisect angle iK nR
  # t=10:48  {jK2, jK} = AngleBisector(iK, nR)
  line jK = bisect angle iK nR other
  # ────────────────────────────────────────────────────────
  # t=11:12  V0 = Intersect(jK, lAF)
  point V0 = intersect jK lAF
  # ────────────────────────────────────────────────────────
  # t=11:22  kV = PerpendicularLine(V0, iK)
  line kV through V0 perpendicular iK
  # ────────────────────────────────────────────────────────
  # t=11:35  W0 = Intersect(nR, kV)
  point W0 = intersect nR kV
  # ────────────────────────────────────────────────────────
  # t=11:37  Z0 = Intersect(qR, kV)
  point Z0 = intersect qR kV
  # ────────────────────────────────────────────────────────
  # t=11:55  V1 = Reflect(V0, nR)
  point V1 = reflect V0 across nR
  # ────────────────────────────────────────────────────────
  # S1 = Reflect(S0, nR)
  point S1 = reflect S0 across nR
  # Z1 = Reflect(Z0, nR)
  point Z1 = reflect Z0 across nR
  # ────────────────────────────────────────────────────────
  # t=12:00  lK = PerpendicularLine(K, iK)
  line lK through K perpendicular iK
  # ────────────────────────────────────────────────────────
  # t=12:30  W2 = Reflect(W0, lK)
  point W2 = reflect W0 across lK
  # ────────────────────────────────────────────────────────
  # V2 = Reflect(V0, lK)
  point V2 = reflect V0 across lK
  # S2 = Reflect(S0, lK)
  point S2 = reflect S0 across lK
  # ────────────────────────────────────────────────────────
  # t=12:47  W3 = Reflect(W0, iK)
  point W3 = reflect W0 across iK
  # ────────────────────────────────────────────────────────
  # V3 = Reflect(V1, iK)
  point V3 = reflect V1 across iK
  # S3 = Reflect(S1, iK)
  point S3 = reflect S1 across iK
  # Z3 = Reflect(Z1, iK)
  point Z3 = reflect Z1 across iK
  # W4 = Reflect(W2, iK)
  point W4 = reflect W2 across iK
  # V4 = Reflect(V2, iK)
  point V4 = reflect V2 across iK
  # ────────────────────────────────────────────────────────
  # t=12:54  star8 = Polygon(V3, W3, Z0, S0, V0, W0, V1, S1, Z1, W2, V2, S2, V4, W4, Z3, S3)
  polygon star8 [ V3 W3 Z0 S0 V0 W0 V1 S1 Z1 W2 V2 S2 V4 W4 Z3 S3 ]
  # ────────────────────────────────────────────────────────
  # t=13:28  B1 = Intersect(bp, segAB)
  point B1 = intersect bp segAB
  # ────────────────────────────────────────────────────────
  # t=13:32  C1 = Reflect(B1, t)
  point C1 = reflect B1 across t
  # ────────────────────────────────────────────────────────
  # t=13:45  D1 = Intersect(t, bp)
  point D1 = intersect t bp
  # ────────────────────────────────────────────────────────
  # t=13:47  E1 = Reflect(D1, lAD)
  point E1 = reflect D1 across lAD
  # ────────────────────────────────────────────────────────
  # t=14:03  Ap = Reflect(A, t)
  point Ap = reflect A across t
  # ────────────────────────────────────────────────────────
  # t=14:15  F1 = Reflect(B1, h1)
  point F1 = reflect B1 across h1
  # ────────────────────────────────────────────────────────
  # t=14:16  G1 = Reflect(D1, h1)
  point G1 = reflect D1 across h1
  # ────────────────────────────────────────────────────────
  # t=14:17  H1 = Reflect(C1, h1)
  point H1 = reflect C1 across h1
  # ────────────────────────────────────────────────────────
  # t=14:21  App = Reflect(Ap, h1)
  point App = reflect Ap across h1
  # ────────────────────────────────────────────────────────
  # t=14:27  Tp = Reflect(T0, t)
  point Tp = reflect T0 across t
  # ────────────────────────────────────────────────────────
  # t=14:35  star6 = Polygon(Tp, Ap, C1, D1, B1, A, T0, E1, F1, G1, H1, App)
  polygon star6 [ Tp Ap C1 D1 B1 A T0 E1 F1 G1 H1 App ]
  # ────────────────────────────────────────────────────────
  # t=16:10  m2b = Reflect(m2, nRR)
  point O_m2b = reflect O across nRR
  # t=16:10  m2b = Reflect(m2, nRR)
  polygon tri_m2b = reflect tri across nRR
  # ────────────────────────────────────────────────────────
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  point O_lay1 = reflect O across tR
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  polygon kite_lay1 = reflect kite across tR
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  point O_lay12 = reflect O across tR
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  polygon tri_lay1 = reflect tri across tR
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  point O_m2b_lay1 = reflect O_m2b across tR
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  polygon tri_m2b_lay1 = reflect tri_m2b across tR
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  point O_lay13 = reflect O across tR
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  polygon star8_lay1 = reflect star8 across tR
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  polygon star6_lay1 = reflect star6 across tR

pattern sDO9fpu76v8 on sDO9fpu76v8_scaffold
  # ────────────────────────────────────────────────────────
  # t=15:46  m1 = Sequence(Rotate(kite, pi*i/6, O), i, 0, 11)
  rotate 12 around O
    edges from kite
  # ────────────────────────────────────────────────────────
  # t=15:51  m2 = Sequence(Rotate(tri, pi*i/3, O), i, 0, 5)
  rotate 6 around O
    edges from tri
  # ────────────────────────────────────────────────────────
  # t=16:10  m2b = Reflect(m2, nRR)
  rotate 6 around O_m2b
    edges from tri_m2b
  # ────────────────────────────────────────────────────────
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  rotate 12 around O_lay1
    edges from kite_lay1
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  rotate 6 around O_lay12
    edges from tri_lay1
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  rotate 6 around O_m2b_lay1
    edges from tri_m2b_lay1
  # t=17:58  lay1 = Reflect({m1, m2, m2b, m3}, tR)
  rotate 6 around O_lay13
    edges from star8_lay1
    edges from star6_lay1
  # ────────────────────────────────────────────────────────
  # t=18:41  lay2 = Sequence(Rotate(lay1, 5*pi*i/3, O), i, 0, 5)
  rotate 6 around O
    rotate 12 around O_lay1
      edges from kite_lay1
    rotate 6 around O_lay12
      edges from tri_lay1
    rotate 6 around O_m2b_lay1
      edges from tri_m2b_lay1
    rotate 6 around O_lay13
      edges from star8_lay1
      edges from star6_lay1
  palette pal
    Slab = #333333
    Gold = #d4af37

coaster Coaster
  outline polygon 6 $size rotate 0
  inscribe sDO9fpu76v8
  base 4
  relief straps emboss 1.2
  strap width 2
  color base Slab
  color straps Gold
`},{id:`n3IidKfXE1I`,title:`Variable-Angled 12-6-4 Rosette`,blurb:`a coaster carrying the variable-angled 12-6-4 star rosette construction`,source:`# naqsh construction — n3IidKfXE1I
# title: Variable-angled 12-6-4 Star Rosette Pattern
# url: https://youtu.be/n3IidKfXE1I
# steps: 65 statements, 61 tagged steps
# source: reconstructions/n3IidKfXE1I/construction.ggb-commands sha256:b93288707e9ffa7dcd88563208545e1b642ef2026261c2c9a1c2ad831d4d62e0
# renamed: O' -> O_p (apostrophe is not an identifier character)

param size = 90 range 40..120   # mm, finished coaster side — the print knob
param margin = 2 range 1..10   # mm, blank slab between the art and the edge
param unit = ($size - 2 * $margin) / 5.2321   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin

blueprint n3IidKfXE1I_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=03:02  A = (0, 0)
  point A = unit.mpt
  # t=03:02  B = (1, 0)
  point B = unit.cpt0
  # t=03:02  poly1 = Polygon(A, B, 12)
  polygon poly1 = regular 12 from A to B
  # ────────────────────────────────────────────────────────
  # Lv = Rotate(B, 150°, A)
  point Lv = rotate B by 150 around A
  # Cv = Rotate(A, -150°, B)
  point Cv = rotate A by -150 around B
  # Pv = Rotate(B, 270°, A)
  point Pv = rotate B by 270 around A
  # ────────────────────────────────────────────────────────
  # t=03:25  poly2 = Polygon(A, Lv, 6)
  polygon poly2 = regular 6 from A to Lv
  # t=03:25  poly3 = Polygon(Cv, B, 6)
  polygon poly3 = regular 6 from Cv to B
  # ────────────────────────────────────────────────────────
  # t=04:48  k_1 = PerpendicularBisector(A, B)
  bisector k_1 from A to B
  # ────────────────────────────────────────────────────────
  # t=04:53  l_1 = PerpendicularBisector(Pv, A)
  bisector l_1 from Pv to A
  # ────────────────────────────────────────────────────────
  # t=05:13  m_1 = PerpendicularBisector(A, Lv)
  bisector m_1 from A to Lv
  # ────────────────────────────────────────────────────────
  # t=05:37  O = Intersect(k_1, m_1)
  point O = intersect k_1 m_1
  # ────────────────────────────────────────────────────────
  # t=05:39  V = Intersect(k_1, l_1)
  point V = intersect k_1 l_1
  # t=05:39  W = Intersect(m_1, l_1)
  point W = intersect m_1 l_1
  # ────────────────────────────────────────────────────────
  # t=06:27  Z = Midpoint(A, B)
  point Z = midpoint A B
  # t=06:27  A_1 = Midpoint(A, Lv)
  point A_1 = midpoint A Lv
  # t=06:27  B_1 = Midpoint(A, Pv)
  point B_1 = midpoint A Pv
  # ────────────────────────────────────────────────────────
  # t=06:36  c_1 = Circle(A, Z)
  circle c_1 center(A) through Z
  # ────────────────────────────────────────────────────────
  # t=06:51  n_1 = Segment(O, A)
  segment n_1 from O to A
  # t=06:51  p_1 = Segment(W, A)
  segment p_1 from W to A
  # ────────────────────────────────────────────────────────
  # t=07:00  P = Intersect(c_1, n_1)
  point P = intersect c_1 n_1
  # ────────────────────────────────────────────────────────
  # t=07:01  D_1 = Intersect(c_1, p_1)
  point D_1 = intersect c_1 p_1
  # ────────────────────────────────────────────────────────
  # t=07:08  d_1 = Circle(O, P)
  circle d_1 center(O) through P
  # t=07:08  e_1 = Circle(W, D_1)
  circle e_1 center(W) through D_1
  # ────────────────────────────────────────────────────────
  # t=10:16  O' = Rotate(O, 23.5°, P)
  point O_p = rotate O by 23.5 around P
  # ────────────────────────────────────────────────────────
  # t=11:03  q_1 = Line(P, O')
  line q_1 from P to O_p
  # ────────────────────────────────────────────────────────
  # t=12:14  r_1 = AngleBisector(P, A, Z)
  line r_1 = bisect angle P A Z
  # ────────────────────────────────────────────────────────
  # t=13:03  C_1 = Intersect(m_1, q_1)
  point C_1 = intersect m_1 q_1
  # ────────────────────────────────────────────────────────
  # t=13:51  s_1 = Reflect(r_1, n_1)
  line s_1 = reflect r_1 across n_1
  # ────────────────────────────────────────────────────────
  # t=13:58  t_1 = Reflect(q_1, n_1)
  line t_1 = reflect q_1 across n_1
  # ────────────────────────────────────────────────────────
  # t=14:55  b_1 = Reflect(q_1, r_1)
  line b_1 = reflect q_1 across r_1
  # ────────────────────────────────────────────────────────
  # t=15:10  a_1 = Reflect(t_1, s_1)
  line a_1 = reflect t_1 across s_1
  # ────────────────────────────────────────────────────────
  # t=15:44  f_2 = Reflect(q_1, m_1)
  line f_2 = reflect q_1 across m_1
  # ────────────────────────────────────────────────────────
  # t=15:50  F_1 = Intersect(f_2, n_1)
  point F_1 = intersect f_2 n_1
  # ────────────────────────────────────────────────────────
  # t=15:55  G_1 = Intersect(t_1, k_1)
  point G_1 = intersect t_1 k_1
  # ────────────────────────────────────────────────────────
  # t=16:33  q1 = Polygon(P, C_1, F_1, G_1)
  polygon q1 [ P C_1 F_1 G_1 ]
  # ────────────────────────────────────────────────────────
  # X = Intersect(t_1, s_1)
  point X = intersect t_1 s_1
  # ────────────────────────────────────────────────────────
  # t=16:49  H_1 = Reflect(P, m_1)
  point H_1 = reflect P across m_1
  # ────────────────────────────────────────────────────────
  # t=16:52  I_1 = Reflect(X, m_1)
  point I_1 = reflect X across m_1
  # ────────────────────────────────────────────────────────
  # t=16:58  poly4 = Polygon(C_1, H_1, I_1, A_1, X, P)
  polygon poly4 [ C_1 H_1 I_1 A_1 X P ]
  # ────────────────────────────────────────────────────────
  # t=18:56  n_2 = Reflect(a_1, m_1)
  line n_2 = reflect a_1 across m_1
  # ────────────────────────────────────────────────────────
  # t=19:05  q_2 = AngleBisector(W, A, Lv)
  line q_2 = bisect angle W A Lv
  # ────────────────────────────────────────────────────────
  # t=19:12  J_1 = Intersect(n_2, q_2)
  point J_1 = intersect n_2 q_2
  # ────────────────────────────────────────────────────────
  # t=19:24  r_2 = Reflect(n_2, q_2)
  line r_2 = reflect n_2 across q_2
  # ────────────────────────────────────────────────────────
  # t=19:35  s_2 = Reflect(r_2, p_1)
  line s_2 = reflect r_2 across p_1
  # ────────────────────────────────────────────────────────
  # t=19:41  K_1 = Intersect(s_2, m_1)
  point K_1 = intersect s_2 m_1
  # ────────────────────────────────────────────────────────
  # t=19:50  L_1 = Reflect(J_1, m_1)
  point L_1 = reflect J_1 across m_1
  # t=19:50  M_1 = Reflect(D_1, m_1)
  point M_1 = reflect D_1 across m_1
  # ────────────────────────────────────────────────────────
  # t=19:55  poly5 = Polygon(J_1, A_1, L_1, M_1, K_1, D_1)
  polygon poly5 [ J_1 A_1 L_1 M_1 K_1 D_1 ]
  # ────────────────────────────────────────────────────────
  # t=21:10  Ev = Rotate(A, 90°, B)
  point Ev = rotate A by 90 around B
  # t=21:10  f_3 = Segment(A, Ev)
  segment f_3 from A to Ev
  # ────────────────────────────────────────────────────────
  # t=21:44  g_3 = Reflect(b_1, q_2)
  line g_3 = reflect b_1 across q_2
  # ────────────────────────────────────────────────────────
  # t=21:58  h_3 = AngleBisector(B, A, Ev)
  line h_3 = bisect angle B A Ev
  # ────────────────────────────────────────────────────────
  # t=22:08  R_1 = Intersect(g_3, h_3)
  point R_1 = intersect g_3 h_3
  # ────────────────────────────────────────────────────────
  # t=22:20  i_3 = Reflect(g_3, h_3)
  line i_3 = reflect g_3 across h_3
  # ────────────────────────────────────────────────────────
  # t=22:32  N_1 = Intersect(c_1, f_3)
  point N_1 = intersect c_1 f_3
  # t=22:32  c_3 = Circle(V, N_1)
  circle c_3 center(V) through N_1
  # ────────────────────────────────────────────────────────
  # t=23:03  j_3 = Reflect(i_3, f_3)
  line j_3 = reflect i_3 across f_3
  # t=23:03  Q_1 = Intersect(j_3, k_1)
  point Q_1 = intersect j_3 k_1
  # t=23:03  S_1 = Reflect(R_1, k_1)
  point S_1 = reflect R_1 across k_1
  # t=23:03  T_2 = Reflect(N_1, k_1)
  point T_2 = reflect N_1 across k_1
  # ────────────────────────────────────────────────────────
  # t=23:48  poly6 = Polygon(Z, R_1, N_1, Q_1, T_2, S_1)
  polygon poly6 [ Z R_1 N_1 Q_1 T_2 S_1 ]

pattern n3IidKfXE1I on n3IidKfXE1I_scaffold
  # ────────────────────────────────────────────────────────
  # t=03:02  poly1 = Polygon(A, B, 12)
  edges from poly1
  # ────────────────────────────────────────────────────────
  # t=03:25  poly2 = Polygon(A, Lv, 6)
  edges from poly2
  # t=03:25  poly3 = Polygon(Cv, B, 6)
  edges from poly3
  # ────────────────────────────────────────────────────────
  # t=16:33  q1 = Polygon(P, C_1, F_1, G_1)
  edges from q1
  # ────────────────────────────────────────────────────────
  # t=16:58  poly4 = Polygon(C_1, H_1, I_1, A_1, X, P)
  edges from poly4
  # ────────────────────────────────────────────────────────
  # t=18:22  m1 = Sequence(Rotate({q1, poly4}, pi*i/6, O), i, 0, 11)
  rotate 12 around O
    edges from q1
    edges from poly4
  # ────────────────────────────────────────────────────────
  # t=19:55  poly5 = Polygon(J_1, A_1, L_1, M_1, K_1, D_1)
  edges from poly5
  # ────────────────────────────────────────────────────────
  # t=20:34  m2 = Sequence(Rotate({poly5}, pi*i/3, W), i, 0, 5)
  rotate 6 around W
    edges from poly5
  # ────────────────────────────────────────────────────────
  # t=23:48  poly6 = Polygon(Z, R_1, N_1, Q_1, T_2, S_1)
  edges from poly6
  # ────────────────────────────────────────────────────────
  # t=24:22  m3 = Sequence(Rotate({poly6}, pi*i/2, V), i, 0, 3)
  rotate 4 around V
    edges from poly6
  palette pal
    Slab = #333333
    Gold = #d4af37

coaster Coaster
  outline square $size
  inscribe n3IidKfXE1I
  base 4
  relief straps emboss 1.2
  strap width 2
  color base Slab
  color straps Gold
`},{id:`lEfWSogWscs`,title:`Itimad ad-Daula Pattern`,blurb:`a coaster carrying the pattern from the tomb of Itimad ad-Daula in Agra, India`,source:`# naqsh construction — lEfWSogWscs
# title: Pattern from the tomb of Itimad ad-Daula in Agra, India
# url: https://www.youtube.com/watch?v=lEfWSogWscs
# steps: 49 statements, 49 tagged steps
# source: reconstructions/lEfWSogWscs/construction.ggb-commands sha256:abc8a7a2a19204979013350afba0321050f6231e917eeab7d7c0274abb7f0004

param size = 90 range 40..120   # mm, finished coaster span across flats — the print knob
param margin = 2 range 1..10   # mm, blank slab between the art and the edge
param unit = ($size - 2 * $margin) / 2.4143   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin

blueprint lEfWSogWscs_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=00:18  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=00:25  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=00:55  C = Rotate(A, -135°, B)
  point C = rotate A by -135 around B
  # t=00:55  D = Rotate(B, -135°, C)
  point D = rotate B by -135 around C
  # t=00:55  E = Rotate(C, -135°, D)
  point E = rotate C by -135 around D
  # t=00:55  F = Rotate(D, -135°, E)
  point F = rotate D by -135 around E
  # t=00:55  G = Rotate(E, -135°, F)
  point G = rotate E by -135 around F
  # t=00:55  H = Rotate(F, -135°, G)
  point H = rotate F by -135 around G
  # ────────────────────────────────────────────────────────
  # t=01:09  poly1 = Polygon(A, B, C, D, E, F, G, H)
  polygon poly1 [ A B C D E F G H ]
  # ────────────────────────────────────────────────────────
  # t=01:23  l = PerpendicularBisector(A, B)
  bisector l from A to B
  # ────────────────────────────────────────────────────────
  # t=01:28  m = PerpendicularBisector(B, C)
  bisector m from B to C
  # ────────────────────────────────────────────────────────
  # t=01:36  cen = Intersect(l, m)
  point cen = intersect l m
  # ────────────────────────────────────────────────────────
  # t=01:44  J = Midpoint(A, B)
  point J = midpoint A B
  # t=01:44  K = Midpoint(B, C)
  point K = midpoint B C
  # ────────────────────────────────────────────────────────
  # t=01:51  c = Circle(B, J)
  circle c center(B) through J
  # ────────────────────────────────────────────────────────
  # t=03:41  d = Circle(cen, 0.5)
  circle d center(cen) radius 0.5 * $unit
  # ────────────────────────────────────────────────────────
  # t=02:06  vB = Line(B, l)
  line vB through B parallel l
  # ────────────────────────────────────────────────────────
  # t=02:14  {Lo, L} = Intersect(c, vB)
  intersect LoL_ c vB
  # t=02:14  {Lo, L} = Intersect(c, vB)
  point Lo = LoL_.cpt0
  # t=02:14  {Lo, L} = Intersect(c, vB)
  point L = LoL_.cpt1
  # ────────────────────────────────────────────────────────
  # t=02:20  rJL = Line(J, L)
  line rJL from J to L
  # ────────────────────────────────────────────────────────
  # t=02:31  fI = Line(cen, rJL)
  line fI through cen parallel rJL
  # ────────────────────────────────────────────────────────
  # t=02:37  M = Midpoint(H, A)
  point M = midpoint H A
  # ────────────────────────────────────────────────────────
  # t=02:55  lMK = Line(M, K)
  line lMK from M to K
  # ────────────────────────────────────────────────────────
  # t=03:03  aI = Line(cen, lMK)
  line aI through cen parallel lMK
  # ────────────────────────────────────────────────────────
  # t=03:47  C1 = Intersect(aI, vB)
  point C1 = intersect aI vB
  # ────────────────────────────────────────────────────────
  # t=04:11  V  = Rotate(C1, 45°, cen)
  point V = rotate C1 by 45 around cen
  # ────────────────────────────────────────────────────────
  # t=04:14  W  = Rotate(C1, 90°, cen)
  point W = rotate C1 by 90 around cen
  # ────────────────────────────────────────────────────────
  # t=04:16  Z  = Rotate(C1, 135°, cen)
  point Z = rotate C1 by 135 around cen
  # t=04:16  A1 = Rotate(C1, 180°, cen)
  point A1 = rotate C1 by 180 around cen
  # ────────────────────────────────────────────────────────
  # t=04:09  T  = Rotate(C1, 225°, cen)
  point T = rotate C1 by 225 around cen
  # ────────────────────────────────────────────────────────
  # t=04:19  B1 = Rotate(C1, 270°, cen)
  point B1 = rotate C1 by 270 around cen
  # ────────────────────────────────────────────────────────
  # t=04:13  U  = Rotate(C1, 315°, cen)
  point U = rotate C1 by 315 around cen
  # ────────────────────────────────────────────────────────
  # t=04:26  b  = Line(T, U)
  line b from T to U
  # ────────────────────────────────────────────────────────
  # t=04:30  lA1B1 = Line(A1, B1)
  line lA1B1 from A1 to B1
  # ────────────────────────────────────────────────────────
  # t=05:16  iB = Line(cen, B)
  line iB from cen to B
  # ────────────────────────────────────────────────────────
  # t=05:27  D1 = Intersect(iB, b)
  point D1 = intersect iB b
  # ────────────────────────────────────────────────────────
  # t=05:01  h1 = Line(D1, l)
  line h1 through D1 parallel l
  # ────────────────────────────────────────────────────────
  # t=05:32  E1 = Intersect(h1, lA1B1)
  point E1 = intersect h1 lA1B1
  # ────────────────────────────────────────────────────────
  # t=05:36  S  = Intersect(h1, lMK)
  point S = intersect h1 lMK
  # ────────────────────────────────────────────────────────
  # t=05:40  F1 = Intersect(h1, rJL)
  point F1 = intersect h1 rJL
  # ────────────────────────────────────────────────────────
  # t=05:43  G1 = Reflect(E1, l)
  point G1 = reflect E1 across l
  # t=05:43  Sp = Reflect(S, l)
  point Sp = reflect S across l
  # t=05:43  H1 = Reflect(F1, l)
  point H1 = reflect F1 across l
  # ────────────────────────────────────────────────────────
  # t=05:48  g1 = Line(U, l)
  line g1 through U parallel l
  # ────────────────────────────────────────────────────────
  # t=05:50  dL = Line(D1, L)
  line dL from D1 to L
  # ────────────────────────────────────────────────────────
  # t=05:52  I1 = Intersect(g1, dL)
  point I1 = intersect g1 dL
  # ────────────────────────────────────────────────────────
  # t=05:55  J1 = Intersect(g1, lMK)
  point J1 = intersect g1 lMK
  # ────────────────────────────────────────────────────────
  # t=06:12  poly2 = Polygon(Sp, S, F1, J, H1)
  polygon poly2 [ Sp S F1 J H1 ]
  # ────────────────────────────────────────────────────────
  # t=06:42  poly3 = Polygon(B1, D1, U, I1, L, J1, S, E1)
  polygon poly3 [ B1 D1 U I1 L J1 S E1 ]

pattern lEfWSogWscs on lEfWSogWscs_scaffold
  # ────────────────────────────────────────────────────────
  # t=01:09  poly1 = Polygon(A, B, C, D, E, F, G, H)
  edges from poly1
  # ────────────────────────────────────────────────────────
  # t=07:37  motif = Sequence(Rotate({poly2, poly3}, pi*i/4, cen), i, 0, 7)
  rotate 8 around cen
    edges from poly2
    edges from poly3
  palette pal
    Slab = #333333
    Gold = #d4af37

coaster Coaster
  outline polygon 8 $size rotate 0
  inscribe lEfWSogWscs
  base 4
  relief straps emboss 1.2
  strap width 2
  color base Slab
  color straps Gold
`},{id:`tA8eSdVx_EQ`,title:`Seven-Fold Star Rosette`,blurb:`a coaster carrying the seven-fold star rosette from the five-minute construction`,source:`# naqsh construction — tA8eSdVx_EQ
# title: 5-minute 7-fold star rosette
# url: https://www.youtube.com/watch?v=tA8eSdVx_EQ
# steps: 30 statements, 30 tagged steps
# source: reconstructions/tA8eSdVx_EQ/construction.ggb-commands sha256:5f3f48e99524d7db1e775ff64c33ce915eb9ea8d3a74034ba1b751828a2bda80

param size = 90 range 40..120   # mm, finished coaster span across flats — the print knob
param margin = 2 range 1..10   # mm, blank slab between the art and the edge
param unit = ($size - 2 * $margin) / 2.7886   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin

blueprint tA8eSdVx_EQ_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=00:12  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=00:14  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=00:28  C = Rotate(A, -128.571429°, B)
  point C = rotate A by -128.571429 around B
  # t=00:28  poly1 = Polygon(A, B, 7)
  polygon poly1 = regular 7 from A to B
  # ────────────────────────────────────────────────────────
  # t=00:47  m = PerpendicularBisector(A, B)
  bisector m from A to B
  # ────────────────────────────────────────────────────────
  # t=00:49  n = PerpendicularBisector(B, C)
  bisector n from B to C
  # ────────────────────────────────────────────────────────
  # t=00:55  H = Intersect(m, n)
  point H = intersect m n
  # ────────────────────────────────────────────────────────
  # t=00:58  I = Midpoint(A, B)
  point I = midpoint A B
  # ────────────────────────────────────────────────────────
  # t=01:00  J = Midpoint(B, C)
  point J = midpoint B C
  # ────────────────────────────────────────────────────────
  # t=01:05  c = Circle(B, I)
  circle c center(B) through I
  # ────────────────────────────────────────────────────────
  # t=01:09  p = Line(B, H)
  line p from B to H
  # ────────────────────────────────────────────────────────
  # t=01:12  K = Intersect(c, p, 2)
  point K = intersect c p pick 2
  # ────────────────────────────────────────────────────────
  # t=01:16  d = Circle(H, I)
  circle d center(H) through I
  # ────────────────────────────────────────────────────────
  # t=01:37  Bp = Rotate(B, 24°, K)
  point Bp = rotate B by 24 around K
  # ────────────────────────────────────────────────────────
  # t=01:45  lb = Line(K, Bp)
  line lb from K to Bp
  # ────────────────────────────────────────────────────────
  # t=02:18  rb = AngleBisector(A, B, H)
  line rb = bisect angle A B H
  # ────────────────────────────────────────────────────────
  # t=02:31  L = Intersect(lb, m)
  point L = intersect lb m
  # ────────────────────────────────────────────────────────
  # t=02:37  lp = Reflect(lb, p)
  line lp = reflect lb across p
  # ────────────────────────────────────────────────────────
  # t=02:40  lpp = Reflect(lp, n)
  line lpp = reflect lp across n
  # ────────────────────────────────────────────────────────
  # t=02:43  O = Intersect(lpp, p)
  point O = intersect lpp p
  # ────────────────────────────────────────────────────────
  # t=02:45  M = Intersect(lp, lpp)
  point M = intersect lp lpp
  # ────────────────────────────────────────────────────────
  # t=02:49  lpr = Reflect(lp, rb)
  line lpr = reflect lp across rb
  # ────────────────────────────────────────────────────────
  # t=02:51  N = Intersect(lp, rb)
  point N = intersect lp rb
  # ────────────────────────────────────────────────────────
  # t=02:58  q1 = Polygon(K, L, O, M)
  polygon q1 [ K L O M ]
  # ────────────────────────────────────────────────────────
  # t=03:03  ls = Reflect(lpr, m)
  line ls = reflect lpr across m
  # ────────────────────────────────────────────────────────
  # t=03:13  P = Intersect(ls, p)
  point P = intersect ls p
  # ────────────────────────────────────────────────────────
  # t=03:16  Np = Reflect(N, p)
  point Np = reflect N across p
  # ────────────────────────────────────────────────────────
  # t=03:23  poly2 = Polygon(P, I, N, K, Np, J)
  polygon poly2 [ P I N K Np J ]

pattern tA8eSdVx_EQ on tA8eSdVx_EQ_scaffold
  # ────────────────────────────────────────────────────────
  # t=03:58  l1 = Sequence(Rotate(q1, 2*pi*i/7, H), i, 0, 6)
  rotate 7 around H
    edges from q1
  # ────────────────────────────────────────────────────────
  # t=04:40  l2 = Sequence(Rotate(poly2, 2*pi*i/7, H), i, 0, 6)
  rotate 7 around H
    edges from poly2
  palette pal
    Slab = #333333
    Gold = #d4af37

coaster Coaster
  outline polygon 7 $size rotate 0
  inscribe tA8eSdVx_EQ
  base 4
  relief straps emboss 1.2
  strap width 2
  color base Slab
  color straps Gold
`},{id:`nmEjCTzMbDg`,title:`N-Fold Flower`,blurb:`a coaster carrying the eighteen-fold flower — outward arc petals and radial spokes — from the GeoGebra Classic 5 construction`,source:`# naqsh construction — nmEjCTzMbDg
# title: n-fold flower in GeoGebra Classic 5
# url: https://www.youtube.com/watch?v=nmEjCTzMbDg
# steps: 38 statements, 38 tagged steps
# source: reconstructions/nmEjCTzMbDg/construction.ggb-commands sha256:b3524c5717ebb5c0a6285389991b251d03c624d747aba2fa7e6733150a49e486
# renamed: c' -> c_p (apostrophe is not an identifier character)
# renamed: I' -> I_p (apostrophe is not an identifier character)
# renamed: M' -> M_p (apostrophe is not an identifier character)
# renamed: P' -> P_p (apostrophe is not an identifier character)
# renamed: ring -> ring_ (reserved word)

param size = 90 range 40..120   # mm, finished coaster diameter — the print knob
param margin = 2 range 1..10   # mm, blank slab between the art and the edge
param unit = ($size - 2 * $margin) / 11.7376   # mm per GeoGebra unit — derived from size and margin so the art clears the edge by margin

blueprint nmEjCTzMbDg_scaffold
  # ────────────────────────────────────────────────────────
  # root frame — A = centre, B/D = unit-circle divisions (D-061)
  circle unit center(0, 0) radius $unit
  divide unit into 4
  # ────────────────────────────────────────────────────────
  # t=00:39  A = (0, 0)
  point A = unit.mpt
  # ────────────────────────────────────────────────────────
  # t=00:43  B = (1, 0)
  point B = unit.cpt0
  # ────────────────────────────────────────────────────────
  # t=00:57  C = Rotate(A, -160°, B)
  point C = rotate A by -160 around B
  # t=00:57  poly1 = Polygon(A, B, 18)
  polygon poly1 = regular 18 from A to B
  # ────────────────────────────────────────────────────────
  # t=01:18  m = PerpendicularBisector(A, B)
  bisector m from A to B
  # ────────────────────────────────────────────────────────
  # t=01:23  p = PerpendicularBisector(A, C)
  bisector p from A to C
  # ────────────────────────────────────────────────────────
  # t=01:28  H = Intersect(m, p)
  point H = intersect m p
  # ────────────────────────────────────────────────────────
  # t=01:32  I = Midpoint(A, B)
  point I = midpoint A B
  # ────────────────────────────────────────────────────────
  # t=01:34  c = Circle(B, I)
  circle c center(B) through I
  # ────────────────────────────────────────────────────────
  # t=01:40  J = Rotate(I, -80°, B)
  point J = rotate I by -80 around B
  # t=01:40  K = Reflect(J, B)
  point K = rotate J by 180 around B
  # ────────────────────────────────────────────────────────
  # t=01:53  d = Parabola(J, m)
  parabola d focus J directrix m
  # ────────────────────────────────────────────────────────
  # t=02:12  L = Intersect(d, p, 2)
  point L = intersect d p pick 2
  # ────────────────────────────────────────────────────────
  # t=02:19  e = Circle(L, J)
  circle e center(L) through J
  # ────────────────────────────────────────────────────────
  # t=02:27  M = ClosestPoint(m, L)
  point M = closest m to L
  # ────────────────────────────────────────────────────────
  # t=02:32  N = Reflect(J, L)
  point N = rotate J by 180 around L
  # ────────────────────────────────────────────────────────
  # t=02:34  q = Parabola(N, m)
  parabola q focus N directrix m
  # ────────────────────────────────────────────────────────
  # t=02:41  O = Intersect(q, p, 2)
  point O = intersect q p pick 2
  # ────────────────────────────────────────────────────────
  # t=02:44  r = Circle(O, N)
  circle r center(O) through N
  # ────────────────────────────────────────────────────────
  # t=02:47  P = ClosestPoint(m, O)
  point P = closest m to O
  # ────────────────────────────────────────────────────────
  # t=03:18  s = Circle(H, K)
  circle s center(H) through K
  # ────────────────────────────────────────────────────────
  # t=03:42  c' = Reflect(c, s)
  circle c_p = invert c in s
  # ────────────────────────────────────────────────────────
  # t=03:56  Q = Center(c')
  point Q = center c_p
  # ────────────────────────────────────────────────────────
  # t=04:11  t = Hyperbola(H, Q, K)
  hyperbola t foci H Q through K
  # ────────────────────────────────────────────────────────
  # t=04:35  S = Rotate(K, -10°, H)
  point S = rotate K by -10 around H
  # t=04:35  R = Intersect(t, m, 2)
  point R = intersect t m pick 2
  # ────────────────────────────────────────────────────────
  # t=04:38  c_1 = Circle(R, S)
  circle c_1 center(R) through S
  # ────────────────────────────────────────────────────────
  # t=04:49  d_1 = Reflect(c_1, s)
  circle d_1 = invert c_1 in s
  # t=04:49  D = Center(d_1)
  point D = center d_1
  # ────────────────────────────────────────────────────────
  # t=05:12  I' = Reflect(I, p)
  point I_p = reflect I across p
  # ────────────────────────────────────────────────────────
  # t=05:14  M' = Reflect(M, p)
  point M_p = reflect M across p
  # ────────────────────────────────────────────────────────
  # t=05:21  P' = Reflect(P, p)
  point P_p = reflect P across p
  # ────────────────────────────────────────────────────────
  # t=05:32  e_1 = CircularArc(O, P, P')
  circle e_1_host center(O) through P
  # ────────────────────────────────────────────────────────
  # t=05:35  f_1 = CircularArc(L, M, M')
  circle f_1_host center(L) through M
  # ────────────────────────────────────────────────────────
  # t=05:38  g_1 = CircularArc(B, I, I')
  circle g_1_host center(B) through I
  # ────────────────────────────────────────────────────────
  # t=06:10  T = Reflect(S, D)
  point T = rotate S by 180 around D
  # ────────────────────────────────────────────────────────
  # t=06:12  a = Segment(H, T)
  segment a from H to T
  # ────────────────────────────────────────────────────────
  # t=07:45  ring = Sequence(Rotate({e_1, f_1, g_1, d_1, a}, 2*pi*i/18, H), i, 0, 17)
  divide d_1 into 2

pattern nmEjCTzMbDg on nmEjCTzMbDg_scaffold
  # t=07:45  ring = Sequence(Rotate({e_1, f_1, g_1, d_1, a}, 2*pi*i/18, H), i, 0, 17)
  rotate 18 around H
    connect arc P -> P_p on e_1_host major
    connect arc M -> M_p on f_1_host major
    connect arc I -> I_p on g_1_host major
    connect arc d_1.cpt0 -> d_1.cpt1 on d_1
    connect arc d_1.cpt1 -> d_1.cpt0 on d_1 major
    connect H -> T
  palette pal
    Slab = #333333
    Gold = #d4af37

coaster Coaster
  outline round $size
  inscribe nmEjCTzMbDg
  base 4
  relief straps emboss 1.2
  strap width 2
  color base Slab
  color straps Gold
`}],ze=`six-fold-rosette`;function d(e){return u.find(t=>t.id===e)}var f=[`base`,`straps`,`border`],Be=/^coaster\b/;function Ve(e){let t=e.findIndex(e=>Be.test(e));if(t<0)return null;let n=t+1;for(;n<e.length&&/^\s/.test(e[n]);)n++;return{header:t,end:n}}function He(e,t,n,r){let i=RegExp(`^\\s*color\\s+${t}\\s+\\S`);for(let t=n;t<r;t++)if(i.test(e[t]))return t;return-1}function Ue(e,t){for(let n=t.header+1;n<t.end;n++){let t=/^(\s*)color\s/.exec(e[n]);if(t)return t[1]}return`  `}function We(e,t,n){let r=f.indexOf(n),i=t.end;for(let n=t.header+1;n<t.end;n++){let t=/^\s*color\s+(\S+)\s/.exec(e[n]);if(!t)continue;let a=f.indexOf(t[1]);a>=0&&a<r&&(i=n+1)}return i}function Ge(e,t,n){let r=e.split(`
`),i=Ve(r);if(!i)return e;let a=He(r,t,i.header+1,i.end);if(n===null)return a<0?e:(r.splice(a,1),r.join(`
`));let o=`${Ue(r,i)}color ${t} ${n}`;return a>=0?r[a]=o:r.splice(We(r,i,t),0,o),r.join(`
`)}var Ke=/^coaster\b/,p=/^\s*relief\s+(\S+)\b/,m=/\s+rods\s*$/;function qe(e){let t=e.findIndex(e=>Ke.test(e));if(t<0)return null;let n=t+1;for(;n<e.length&&/^\s/.test(e[n]);)n++;return{header:t,end:n}}function Je(e,t){for(let n=t.header+1;n<t.end;n++)if(p.test(e[n]))return n;return-1}function Ye(e){let t=e.split(`
`),n=qe(t);if(!n)return null;let r=Je(t,n);if(r<0)return null;let i=p.exec(t[r])[1];return i===`faces`?null:{target:i,shape:m.test(t[r])?`rod`:`band`}}function Xe(e,t){let n=e.split(`
`),r=qe(n);if(!r)return e;let i=Je(n,r);if(i<0||p.exec(n[i])[1]===`faces`)return e;let a=m.test(n[i]);return t===`rod`?a||(n[i]=`${n[i].replace(/\s*$/,``)} rods`):a&&(n[i]=n[i].replace(m,``)),n.join(`
`)}function h(e){let t=document.querySelector(e);if(!t)throw Error(`Coaster Lab markup is missing ${e}`);return t}var g=h(`#coaster-chips`),Ze=h(`#size-chips`),_=h(`#knob-panel`),Qe=h(`#colours-section`),$e=h(`#color-knobs`),et=h(`#relief-section`),tt=h(`#relief-shape-control`),v=h(`#machine-select`),nt=h(`#custom-dims`),y=h(`#dim-x`),b=h(`#dim-y`),x=h(`#dim-z`),rt=h(`#target-note`),S=h(`#stl-button`),C=h(`#copy-link`),it=h(`#bake-button`),at=h(`#bkr-download`),ot=h(`#drawer-hide`),st=h(`#open-studio`),w=h(`#findings-panel`),T=h(`#gate-panel`),E=h(`#error-panel`),ct=h(`#spinner`),lt=h(`#spinner-label`),D=h(`#stop-button`),O=h(`#toast`),ut=h(`#orb-canvas`),dt=[{label:`Mini · 40 mm`,value:40},{label:`Standard · 90 mm`,value:90}],ft=new fe(ut),k=Number(new URLSearchParams(window.location.search).get(`budgetMs`))||0,A=new pe({spawn:()=>new Worker(new URL(``+new URL(`worker-CknSOX5n.js`,import.meta.url).href,``+import.meta.url),{type:`module`}),onMessage:e=>Yt(e),...k>0?{budgetMs:()=>k}:{}}),j=ze,M=`preset`,N=[],P=``,F={},I=new Set,L=ce(),R=0,pt=0,mt=0,z=[],B=!1,ht=0,V=0,H=0,gt=0,_t=0;function U(e){O.textContent=e,O.hidden=!1,window.clearTimeout(gt),gt=window.setTimeout(()=>{O.hidden=!0},3600)}function W(){return M===`custom`?Y.getSource():(d(j)??u[0]).source}function G(){let e={};for(let t of I)F[t]!==void 0&&(e[t]=F[t]);return e}function K(){let e=W();R+=1,mt=R,lt.textContent=me(e)===6e4?`computing — this design is large, may take up to a minute…`:`computing…`,A.evaluate({type:`evaluate`,seq:R,source:e,params:G()}),window.clearTimeout(V),V=window.setTimeout(()=>{ct.hidden=!1},300),window.clearTimeout(H),D.hidden=!0,H=window.setTimeout(()=>{D.hidden=!1},2300)}function vt(){window.clearTimeout(V),window.clearTimeout(H),ct.hidden=!0,D.hidden=!0}var q=null;function J(e){if(M===`custom`){let t=Y.getSource();q=s(`custom`,N,F,e,n(t)),a(window.localStorage,c,{source:t,overrides:G()})}else q=s(j,N,F,e);Z()}function yt(){le(_,N,F,{radiusCeilingMm:r(L),onChange:xt})}function bt(){window.clearTimeout(ht),ht=window.setTimeout(()=>{K(),J(`replace`)},200)}function xt(t,n){z=z.filter(e=>e.name!==t),F[t]=n,I.add(t),B=!1;let r=ie(F,N);for(let e of r)I.add(e.name);r.length>0&&e(_,F),$(),bt()}function St(){let t=N.map(e=>[e.name,e.min,e.max,e.step,e.advanced].join(`|`)).join(`;`);if(t!==P){P=t,yt();return}e(_,F)}var Ct={base:`Base`,straps:`Straps`,border:`Border`};function wt(e,t){Y.setSource(Ge(Y.getSource(),e,t)),B=!1,X()}function Tt(e,t){let n=document.createElement(`div`);n.className=`color-row`;let r=document.createElement(`span`);r.className=`color-swatch`,r.style.background=e.hex??`transparent`;let i=document.createElement(`span`);i.className=`color-region`,i.textContent=Ct[e.region];let a=document.createElement(`select`);a.setAttribute(`aria-label`,`${Ct[e.region]} colour`);let o=document.createElement(`option`);o.value=``,o.textContent=`default (one colour)`,o.selected=e.paletteName===null,a.append(o);for(let n of t){let t=document.createElement(`option`);t.value=n.name,t.textContent=n.name,t.selected=e.paletteName===n.name,a.append(t)}return a.addEventListener(`change`,()=>wt(e.region,a.value||null)),n.append(r,i,a),n}function Et(e){$e.textContent=``;let t=e.splittable&&e.palette.length>0;if(Qe.hidden=!t,t)for(let t of e.colors)$e.append(Tt(t,e.palette))}var Dt=[{shape:`band`,label:`Band`},{shape:`rod`,label:`Rods`}];function Ot(e){Y.setSource(Xe(Y.getSource(),e)),B=!1,X()}function kt(){tt.textContent=``;let e=Ye(W());if(et.hidden=e===null,e!==null)for(let{shape:t,label:n}of Dt){let r=document.createElement(`button`);r.className=e.shape===t?`chip active`:`chip`,r.textContent=n,r.title=t===`rod`?`Each strap becomes a half-round rod; junctions round off`:`Each strap is a flat-topped band (the default)`,r.addEventListener(`click`,()=>Ot(t)),tt.append(r)}}function At(){window.clearTimeout(_t),_t=window.setTimeout(()=>{B=!1,X()},500)}var Y=new ae({drawer:h(`#code-drawer`),textarea:h(`#code-editor`),gutter:h(`#editor-gutter`),highlight:h(`#code-hl`),toggle:h(`#code-toggle`),resizeHandle:h(`#drawer-resize`),onInput:At});function X(){let e=se(Y.getSource(),u),t=M===`custom`;if(e){let n=t||j!==e;M=`preset`,j=e,i(window.localStorage,c),n&&Q(),J(`replace`)}else M=`custom`,t||Q(),J(t?`replace`:`push`);K()}function jt(){let e=G();if(Object.keys(e).length===0){U(`All knob values already match the code defaults`);return}let t=o(Y.getSource(),e);if(!t.ok){Wt(`Could not write the knob values into the code`,t.reason);return}let n=t.result;if(n.replacedExpressions.length>0){let e=n.replacedExpressions.join(`, `);if(!window.confirm(`Writing values will replace derived defaults (${e}) with plain numbers. Continue?`))return}I.clear(),Y.setSource(n.source),B=!1,X(),U(`Knob values written into the code`)}function Mt(){let e=o(Y.getSource(),G());if(!e.ok){Wt(`Could not build the .bkr download`,e.reason);return}let t=new Blob([e.result.source],{type:`text/plain`}),n=URL.createObjectURL(t),r=document.createElement(`a`);r.href=n,r.download=`${M===`custom`?`custom-coaster`:j}.bkr`,r.click(),URL.revokeObjectURL(n)}function Z(){if(st.href=`${ne}#code/${n(W())}`,M===`custom`&&q&&!q.codeIncluded){C.disabled=!0,C.title=`Too large to share as a link (${q.hrefLength} chars) — Download .bkr instead. Tip: trimming comments usually gets a script back under the line.`;return}C.disabled=!1,C.title=M===`custom`?`Anyone with this link gets your exact coaster — the code rides in the URL, the print target does not`:``}function Nt(e,t){let n=document.createElement(`dl`);for(let[e,r]of t){let t=document.createElement(`dt`);t.textContent=e;let i=document.createElement(`dd`);i.textContent=r,n.append(t,i)}e.append(n)}function Pt(e,t,n){for(let r of t){let t=document.createElement(`p`);t.className=n,t.textContent=r,e.append(t)}}function Ft(e){return e===void 0||!Number.isFinite(e)?`n/a`:Number.isInteger(e)?String(e):e.toFixed(2)}function It(e,t){let n=document.createElement(`div`);n.className=`cv-row`;let r=document.createElement(`div`),i=document.createElement(`span`);i.className=t.pass?`cv-verdict`:`cv-verdict fail`,i.textContent=t.pass?`PASS`:`FAIL`;let a=document.createElement(`span`);a.textContent=` ${t.code} — measured ${Ft(t.measured)}, limit ${Ft(t.limit)}`,r.append(i,a);let o=document.createElement(`p`);o.className=`cv-msg`,o.textContent=t.message,n.append(r,o),e.append(n)}function Lt(e){w.textContent=``,w.dataset.cv=String(e.findings.length);let t=e.findings.every(e=>e.pass),n=document.createElement(`div`);n.className=t?`gate-badge pass`:`gate-badge fail`,n.textContent=t?`PASS — all ${e.findings.length} structural checks`:`FAIL — a structural check did not hold`,w.append(n),Nt(w,[[`print floor`,`${e.featureFloorMm.toFixed(2)} mm — the coaster's own strap/neck floor (CAL-CST-01)`]]);for(let t of e.findings)It(w,t)}function Rt(e){if(!/is not a valid part/.test(e))return null;let t=[];for(let n of e.matchAll(/\b(CV\d[ab]?):\s*(.+)/g))t.push({code:n[1],pass:!1,message:n[2].trim()});return t.length>0?t:null}function zt(e){w.textContent=``,w.dataset.cv=`0`;let t=document.createElement(`div`);t.className=`gate-badge fail`,t.textContent=`FAIL — ${e.length} structural check${e.length===1?``:`s`} did not hold`,w.append(t);for(let t of e)It(w,t)}function Bt(e,t){let{gate:n,mesh:r}=e;T.textContent=``,T.dataset.tris=String(r.triangles.length);let i=document.createElement(`div`);i.className=n.passed?`gate-badge pass`:`gate-badge fail`,i.textContent=n.passed?`PASS — printable`:`FAIL`,T.append(i),Nt(T,[[`watertight`,n.watertight?`yes`:`NO`],[`triangles`,String(r.triangles.length)],[`volume`,`${(r.stats.volumeMm3/1e3).toFixed(1)} cm³`],[`judged against`,`${t.featureFloorMm.toFixed(2)} mm, the coaster floor (CAL-CST-01) — not the shipped ${de.toFixed(2)} mm FDM floor`]]),Pt(T,n.failures,`gate-failure`)}function Vt(e){for(let t of e)t.dropped?(I.delete(t.name),delete F[t.name]):F[t.name]=t.to}function Ht(){let e=ie(F,N);if(e.length===0)return B=!1,[];for(let t of e)I.add(t.name);return B||(B=!0,K(),J(`replace`)),e}function Ut(e){E.textContent=e,E.hidden=!1,S.disabled=!0;let t=Rt(e);t&&zt(t)}function Wt(e,t){E.textContent=`${e} — ${t}`,E.hidden=!1}function Gt(){for(let e of N)I.has(e.name)||(F[e.name]=e.value)}function Kt(e){if(e.family!==`coaster`||!e.coaster){Ut(M===`custom`?"This script does not declare a `coaster`, so the Coaster Lab has nothing to check. Add a `coaster` block, or open it in the Orb or Lego Lab.":"This script does not declare a `coaster` — the Coaster Lab previews coasters.");return}let t=e.coaster;N=e.specs,Vt(e.adjustments),Gt();let n=[...e.adjustments,...Ht()];if(n.length>0){z=n;let e=ee(n);e&&U(e)}E.hidden=!0,ft.setMesh(e.coasterTint??e.mesh),Et(t),kt(),Lt(t),Bt(e,t),S.disabled=!e.gate.passed,St(),ue(_,z),$(),J(`replace`)}function qt(){let e=(M===`custom`?`custom-coaster`:j)||`coaster`;for(let t of N){let n=F[t.name];n===void 0||n===t.defaultValue||(e+=`-${t.name}${String(Math.round(n*1e6)/1e6)}`)}return`${e}.stl`}function Jt(e){let t=new Blob([e],{type:`model/stl`}),n=URL.createObjectURL(t),r=document.createElement(`a`);r.href=n,r.download=qt(),r.click(),URL.revokeObjectURL(n)}function Yt(e){if(e.type===`stl`){Jt(e.data);return}if(!(e.type===`ldraw`||e.type===`views`||e.type===`sweep`)&&(e.seq===mt&&vt(),!(e.seq<=pt))){if(pt=e.seq,e.type===`error`){Ut(e.message);return}Kt(e)}}function Xt(e){if(M===`preset`&&e===j)return;let t=d(e)??u[0];M===`custom`&&!window.confirm(`Discard your custom coaster and load ${t.title}? Your code is still at the previous link (Back button) until you edit again.`)||(M=`preset`,j=t.id,I.clear(),F={},N=[],P=``,z=[],B=!1,Y.setSource(t.source),Q(),s(j,[],{},`push`),K())}function Zt({script:e,label:t}){let n=document.createElement(`button`),r=M===`preset`&&e.id===j;n.className=r?`coaster-tile active`:`coaster-tile`,n.title=`${e.title} — ${e.blurb}`,n.setAttribute(`aria-pressed`,String(r));let i=Ie(e.id);if(i){let e=document.createElement(`img`);e.src=i,e.alt=``,e.loading=`lazy`,n.append(e)}let a=document.createElement(`span`);return a.textContent=t,n.append(a),n.addEventListener(`click`,()=>Xt(e.id)),n}function Q(){g.textContent=``;for(let e of Re(u)){let t=document.createElement(`div`);t.className=`coaster-group`;let n=document.createElement(`h3`);n.textContent=e.heading;let r=document.createElement(`div`);r.className=`coaster-tiles`;for(let t of e.tiles)r.append(Zt(t));t.append(n,r),g.append(t)}if(M===`custom`){let e=document.createElement(`button`);e.className=`chip active`,e.textContent=`Custom coaster`,e.title=`Your edited script — not one of the committed presets`,g.append(e)}Z()}function Qt(t){xt(`size`,t),e(_,F)}function $(){Ze.textContent=``;let e=N.some(e=>e.name===`size`);for(let t of dt){let n=document.createElement(`button`);n.className=e&&F.size===t.value?`chip active`:`chip`,n.textContent=t.label,n.disabled=!e,n.title=e?`Set size to ${t.value} mm`:"This script declares no `size` param",n.addEventListener(`click`,()=>Qt(t.value)),Ze.append(n)}}function $t(){rt.textContent=`Build volume ${L.xMm}×${L.yMm}×${L.zMm} mm. A coaster is flat and small — this matters for how many fit on a plate, not whether one does.`}function en(){let e=(e,t)=>{let n=Number(e.value);return Number.isFinite(n)&&n>=50?n:t};return{xMm:e(y,256),yMm:e(b,256),zMm:e(x,256)}}function tn(e){let n=l.find(t=>t.id===e)??l[0];nt.hidden=n.id!==`custom`,L=n.id===`custom`?{...n,...en()}:n,t(L),$t()}function nn(){for(let e of l){let t=document.createElement(`option`);t.value=e.id,t.textContent=e.label,v.append(t)}v.value=L.id,nt.hidden=L.id!==`custom`,y.value=String(L.xMm),b.value=String(L.yMm),x.value=String(L.zMm),$t(),v.addEventListener(`change`,()=>tn(v.value));for(let e of[y,b,x])e.addEventListener(`change`,()=>tn(`custom`))}function rn(e){let t=0;for(let[n,r]of Object.entries(e)){let e=Number(r);if(!Number.isFinite(e)){t+=1;continue}F[n]=e,I.add(n)}t>0&&U(`Ignored ${t} non-numeric link value${t===1?``:`s`}`)}function an(e){if(e!==null){let t=te(e);if(t===null){U(`This share link is damaged — it may have been truncated by a chat app. Ask the sender for the .bkr file instead.`);return}M=`custom`,Y.setSource(t),Y.open();return}let t=re(window.localStorage,c);if(t){M=`custom`,Y.setSource(t.source),Y.open();for(let[e,n]of Object.entries(t.overrides))F[e]=n,I.add(e)}}function on(e){if(e.scriptId===`custom`){an(e.code);return}e.scriptId&&(d(e.scriptId)?j=e.scriptId:U(`Unknown coaster "${e.scriptId}" — showing the default`),e.code&&U(`This link names a preset — ignoring its embedded code`))}function sn(){let e=oe();on(e),rn(e.rawParams),M===`preset`&&Y.setSource((d(j)??u[0]).source),Q(),$(),nn(),S.addEventListener(`click`,()=>{R+=1,A.request({type:`stl`,seq:R})}),D.addEventListener(`click`,()=>A.stop()),it.addEventListener(`click`,jt),at.addEventListener(`click`,Mt),ot.addEventListener(`click`,()=>Y.close()),Z(),C.addEventListener(`click`,()=>{navigator.clipboard.writeText(window.location.href).then(()=>U(`Link copied — knobs travel, the print target does not`),()=>U(`Could not copy — use the address bar`))}),window.addEventListener(`popstate`,()=>window.location.reload()),K()}sn();