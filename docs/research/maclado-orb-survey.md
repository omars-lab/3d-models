<!--
  Research produced 2026-08-08 by Claude Opus 4.8 (sub-agent) under the
  3d-models design-doc rules, for the faithful-9-fold "maclado" orb.
  Sources: WebSearch + WebFetch (and local pdftotext on the PDFs WebFetch
  saved) against en.wikipedia.org, cs.uwaterloo.ca (Kaplan), grail.cs.
  washington.edu (Kaplan/Salesin 2004), isohedral.ca, history.siggraph.org,
  archive.bridgesmathart.org (Bonner 2012), dictionary.iucr.org (attempted,
  403 — fell back to Wikipedia), traditionalarchitecturejournal.com,
  redmaestros.com, avilared.com, lagacetadesalamanca.es, raise3d.com,
  faculty.etsu.edu, and general web search for the Gauss-Wantzel result.
  Feeds: docs/maclado-orb-design.md (not yet written) — the faithful 9-fold
  maclado placement family, NOT a symmetric star-ball substitute.
  NOTHING WAS INSTALLED AND NOTHING WAS RUN. No geometry engine was invoked,
  no mesh was generated, no print was made. Every claim here is from
  documentation or from a fetched source; standard-mathematics claims say so
  and cite the best reference reached. Full fetch record is the final §.
-->

# The faithful 9-fold "maclado" orb — why the symmetry must break, what "maclado" means, and what the prior art actually did

*Research date: 2026-08-08. Scope: the facts a design doc needs to specify, in
the bikar engine, a 3D-printable strapwork sphere tiled with 9-pointed star
rosettes ("wheels") joined by filler tiles, in the deliberately-non-symmetric
manner of Ángel María Martín López's "9-SPIKE 'MACLADO' RIBBON" sphere. The
chosen direction is the faithful 9-fold construction, so this survey serves
that and does not pretend a symmetric star-ball is the same object.*

---

## 0. Standing disclaimers, and the limits of this survey

Two limits apply to **every** sentence below and are not repeated at each claim.

1. **Nothing was run.** No engine, no slicer, no mesh check. Statements about
   what geometry or a print *does* are quoted from a source or labelled as an
   inference.
2. **This is a survey of the ~13 sources fetched here (see §7), not of the
   space of Islamic-pattern software, crystallography, or spherical tiling.**
   Where the text says "of the sources surveyed here", read it literally. No
   sentence here should be taken as "no system / no maker does X" (K2).

One source could not be reached: the IUCr *Online Dictionary of
Crystallography* "Twinning" entry returned HTTP 403 to the fetcher. The
twinning claims below are therefore grounded in the Wikipedia *Crystal
twinning* article instead, and §2 flags exactly which sentence that weakens.

---

## 1. Why 9-fold forces broken symmetry on a sphere

**The claim, with its conditions.** A spherical tiling cannot carry two or more
*equivalent* 9-fold rosette centres related by the tiling's own rotational
symmetry — except in the trivial single-axis "beach-ball" case. It *can* carry
many 9-fold rosettes if you give up the requirement that a global symmetry maps
one onto another. That giving-up is precisely the maclado move.

**The group theory behind it.** The finite subgroups of the rotation group
SO(3) — equivalently, the finite rotation symmetry groups of the sphere — are
classified into exactly five families: the cyclic groups Cₙ (rotations about a
single axis), the dihedral groups Dₙ (order 2n), and the three polyhedral
groups — tetrahedral **T** (order 12), octahedral **O** (order 24), and
icosahedral **I** (order 60)
([en.wikipedia.org/wiki/Point_groups_in_three_dimensions](https://en.wikipedia.org/wiki/Point_groups_in_three_dimensions)).
This is a standard theorem of group theory / crystallography; the Wikipedia
article states the five-family split and the three polyhedral orders (12, 24,
60) as fetched above, and it is corroborated by the point-group literature
surfaced in search (Wolfram MathWorld's *Tetrahedral Group*, the *List of
spherical symmetry groups*).

**The rotation-axis orders in the polyhedral groups are only 2, 3, 4, and 5** —
never 9 (same source). Tetrahedral has 3- and 2-fold axes; octahedral has 4-,
3-, 2-fold; icosahedral has 5-, 3-, 2-fold. So:

- A polyhedral group (T/O/I) is the only way to place *many* equivalent
  high-symmetry sites on a sphere, and its site orders are capped at 5. A
  9-fold rosette centre cannot sit on a symmetry axis of any polyhedral group,
  because no polyhedral group has a 9-fold axis (fetched, same page).
- The only finite sphere group with a 9-fold axis at all is C₉ or D₉ — a
  *single* distinguished axis. That is the "beach-ball": you may put one 9-fold
  rosette at each pole and repeat a band nine times around the equator, but you
  cannot get a second, third, … inequivalent 9-fold centre distributed over the
  sphere and still have a symmetry carry one to another. (This is the
  single-axis restriction of Cₙ/Dₙ, read directly off the classification;
  same source.)

**Consequence for the engine, stated without over-claiming.** *If* the design
requires ≥2 nine-fold rosette centres spread over the sphere (not a single
polar axis), *then* no global rotation symmetry can relate all of them — the
tiling must break global symmetry. This is a theorem about rotation groups; it
does not by itself say the object is impossible, only that it cannot be
*symmetric* in the SO(3) sense. That is exactly why the maker "gives up global
radial symmetry": it is forced, not stylistic. (K10 note: this transfers to our
case only because the target genuinely wants many 9-fold centres over the whole
sphere; a single-axis 9-fold pendant would *not* need to break symmetry, and
the doc must not port the "must break" conclusion to that easier object.)

The nearest indexed *symmetric* alternative — a "star-ball" — pays for its
symmetry by changing the star order. Kaplan's spherical star patterns (see §4)
use 10-point stars on a truncated icosahedron, whose rotation group is
icosahedral (site orders 5, 3, 2); a 12-fold or 10-fold rosette can be
symmetrized on such a solid where a 9-fold one cannot. Choosing symmetry means
abandoning 9; keeping 9 means abandoning symmetry. The two are not both
available (this survey found no source offering both, and the group theory in
this § says why).

---

## 2. "Maclado" = crystal twinning — a symmetry of the aggregate, not of the parts

**The term.** *Maclado* is the Spanish adjective from *macla* (a crystal twin;
French *macle*, English *macle*/*twin*). The Wikipedia *Crystal twinning*
article records the term directly: *"Twinning, a version of macle, is a form of
symmetrical intergrowth between two or more adjacent crystals"*
([en.wikipedia.org/wiki/Crystal_twinning](https://en.wikipedia.org/wiki/Crystal_twinning)).

**The crystallography, and the exact analogy the maker draws.** A twin is an
oriented *association* of two or more crystal domains of the same species,
related by a **twin law** — a symmetry operation of the *aggregate*. The load-
bearing point is that this operation is **not** a symmetry of the individual
domain: the fetched Wikipedia article states *"The twin operation is not one of
the normal symmetry operations of the untwinned crystal structure"* and *"A twin
law is not a symmetry operation of the full set of basis points"* (same URL).

The analogy to the orb: each 9-fold rosette ("wheel") is a *domain* with local
C₉ symmetry. The sphere is the *aggregate*. There is no global operation that is
a symmetry of the whole sphere the way C₉ is a symmetry of one wheel — just as a
twin's overall symmetry is not the single crystal's symmetry. The maker's
"maclado" names exactly this: local order (each wheel is a faithful 9-star)
composed into a whole whose symmetry is only that of the *joining*, i.e. the
strapwork ribbons and filler tiles that stitch domains together, not a rotation
that maps every wheel onto every other.

**Qualifier (K1), honestly.** The canonical crystallographic definition lives in
the IUCr *Online Dictionary of Crystallography* "Twinning" entry, which the
fetcher could not reach (403). The two quoted sentences above are from Wikipedia,
which is reliable for this standard definition but is not the primary
crystallographic authority; a doc that leans hard on the exact wording of the
twin law should re-fetch the IUCr entry through an authenticated route before
quoting it as canonical.

---

## 3. Ángel María Martín López — who he is, and what is NOT retrievable

**Identity (well sourced).** Ángel María Martín López is a Spanish master of
*carpintería de lo blanco* (Mudéjar "white carpentry" — the trade of *lacería*
interlace in wood), founder and director since 2014–2015 of the Centro de
Interpretación de Carpintería Mudéjar Abulense (CICMA) in Narros del Castillo,
Ávila; a retired Ávila firefighter by first career; and a 2024 Europa Nostra /
European Heritage Award laureate for the white-carpentry school
([avilared.com](https://avilared.com/art/76848/felicitaciones-para-angel-maria-martin-premio-europa-nostra-por-la-carpinteria-de-lo-blanco);
[lagacetadesalamanca.es](https://www.lagacetadesalamanca.es/provincia/angel-maria-martin-lopez-restaurador-de-artesonados-hay-joyas-en-salamanca-con-500-anos-que-hacen-su-funcion-como-el-primer-dia-YD6126144);
[redmaestros.com](https://redmaestros.com/maestros-cat/angel-maria-martin-lopez/)).

**His spherical strapwork work (partially retrievable).** The Red de Maestros
profile describes his research into *"integración armónica de los motivos de
lacería de lazo diez … en cubiertas ochavadas y cúpulas esféricas"* (harmonious
integration of *ten*-fold interlace motifs in octagonal roofs and spherical
domes) and says he is preparing a monographic course on *"el desarrollo futuro
de las cúpulas de lacería regulares en toda la superficie esférica"* (the future
development of *regular* interlace cupolas across the entire spherical surface)
([redmaestros.com](https://redmaestros.com/maestros-cat/angel-maria-martin-lopez/)).
A conference paper on strapwork wooden domes with spherical geometry lists a
co-author "Ángel María Martín" (Universidad Politécnica de Madrid), proposing
*"the development of domes based on polyhedral symmetry that respond to the
strict layout of the strapwork wheels"*
([traditionalarchitecturejournal.com](https://www.traditionalarchitecturejournal.com/index.php/home/article/view/519)).

**What is NOT retrievable, stated plainly (K1).** Three things could not be
sourced and must survive as open qualifiers into the design doc:

1. **His exact placement rule for the 9-SPIKE maclado sphere is not
   retrievable.** The specific object named in the brief — the "9-SPIKE
   'MACLADO' RIBBON" sphere — was not found on any web-indexed page in this
   survey. His most active channel is Facebook, which is not web-indexed and
   was not fetchable here; so his own description of the 9-fold construction,
   its wheel count, its filler-tile scheme, and its over/under parity rule
   **could not be obtained**. The engine design cannot claim to reproduce his
   method exactly — only to build a faithful 9-fold object in the same spirit.
2. **Whether the "Ángel María Martín" of the UPM dome paper is the same person**
   as Ángel María Martín López is *likely but not confirmed* by the sources
   fetched (the surname "López" is dropped in the journal byline; both concern
   Mudéjar strapwork on spheres). Treat as probable, not established.
3. **The indexed record points at ten-fold and "regular" cupolas**, whereas the
   target object is nine-fold and explicitly *non-regular*. The 9-fold maclado
   sphere is thus, on the evidence reachable here, either later/parallel work or
   a distinct piece; the doc should not assert continuity it cannot source.

---

## 4. Spherical Islamic star patterns — prior art and technique (what was done, and what was NOT 9)

**Kaplan & Salesin, "Islamic Star Patterns in Absolute Geometry" (2004).** This
is the load-bearing prior-art datum. The method builds a star pattern from an
underlying tiling and a small set of parameters, and — because it is stated in
*absolute* geometry — the *"same construction can then be applied seamlessly
across the Euclidean plane, the surface of a sphere"* and the hyperbolic plane
(fetched PDF text). Crucially, the star order they place on the sphere is **not**
nine: *"patterns in the second column of Figure 15 consist of 10-pointed stars
on the sphere, 12-pointed stars in the Euclidean plane, and 14-pointed stars in
the hyperbolic plane"*
([grail.cs.washington.edu/…/kaplan-2004-isp.pdf](https://grail.cs.washington.edu/wp-content/uploads/2015/08/kaplan-2004-isp.pdf)).
The star orders they discuss are 8-, 10-, 12-, 14-pointed; **no 9-pointed star
appears in the fetched text.** The reason they can symmetrize 10 on the sphere is
that their spherical tilings sit on polyhedral (icosahedral/octahedral) symmetry
— exactly the site orders (§1) that admit 5/4/3/2 but not 9.

**Kaplan, "Interwoven Islamic Geometric Patterns" (Bridges 2017), and the 2016
3D prints.** Kaplan writes: *"In 2016 I was given the opportunity to display a
selection of my 3D printed spherical Islamic star patterns"*, that each tile is
converted into a module *"on a tiling of the plane or a polyhedron (i.e., a
tiling of the sphere)"*, and shows *"A 3D printed spherical interwoven star
pattern based on a truncated icosahedron"* and a *"dodecahedral"* sculpture with
**12-pointed stars** (fetched PDF text;
[cs.uwaterloo.ca/…/kaplan_2017.pdf](https://cs.uwaterloo.ca/~csk/publications/Papers/kaplan_2017.pdf)).
So the closest indexed 3D-printed spherical Islamic star ball in this survey is
built on a **truncated icosahedron / dodecahedron with 10- or 12-point stars —
not 9** — confirming that the symmetric route buys itself out of the 9-fold
problem by changing the star order, and that our 9-fold object is a genuinely
different construction, not a re-skin of Kaplan's.

**Jay Bonner, the polygonal technique, and where 9-fold lives.** Bonner's
polygonal (Hankin-derived) technique classifies patterns as *systematic* (a
small fixed set of module polygons) versus *non-systematic* (module polygons
"unique to the given pattern"). His Bridges 2012 workshop paper *Creating Non-
Systematic Islamic Geometric Patterns With Complex Combinations of Star Forms*
places 9-pointed stars only in the non-systematic family, in historical
composites such as *"12-pointed stars at the grid vertices; 9-pointed stars at
the center of each repetitive unit"* and *"11-pointed stars at each vertex … and
9-pointed stars at the vertices"*
([archive.bridgesmathart.org/2012/bridges2012-593.pdf](https://archive.bridgesmathart.org/2012/bridges2012-593.pdf)).
This is the historical "9-and-12" (lazo) precedent: nine-fold rosettes have
classically been *reconciled by irregular filler regions*, never by a global
symmetric grid — the same fix, one dimension down, that the maclado sphere uses.

**Hankin contact-angle / polygons-in-contact (PIC).** The technique Kaplan
formalizes is Hankin's: from a tiling, place a contact point on each polygon
edge and grow two rays at a chosen **contact angle**; star motifs emerge where
rays meet. Kaplan's *"Islamic Star Patterns from Polygons in Contact"* (Graphics
Interface 2005) is the method paper
([cs.uwaterloo.ca/…/kaplan_2005.pdf](https://cs.uwaterloo.ca/~csk/publications/Papers/kaplan_2005.pdf));
the 2004 paper exposes the same two knobs as **θ** (contact angle) and **s**
(truncation), demonstrated on 10-pointed stars (fetched text, §4 above). These
two parameters are the natural knobs for the engine's rosette generator.

*Survey scope (K2):* this covers the prior art reachable in this session —
Kaplan/Salesin and Bonner. It is not a claim about every spherical-pattern
system; e.g. Hankin's own primary papers and Bonner's 595-page monograph were
not fetched here, only referenced through the fetched papers and search.

---

## 5. Constructive geometry facts the engine needs

**The regular nonagon is NOT compass-and-straightedge constructible.** By the
Gauss–Wantzel theorem, a regular n-gon is constructible iff n is a power of 2
times a product of *distinct* Fermat primes. 9 = 3² repeats the Fermat prime 3,
so the nonagon fails. This is standard mathematics with no single canonical URL;
the fetched lecture notes state the theorem and its constructibility criterion
([faculty.etsu.edu/…/Eves6-5-6.pdf](https://faculty.etsu.edu/gardnerr/3040/Notes-Eves6/Eves6-5-6.pdf)),
and web search corroborates the specific 9-gon consequence (9 = 3², repeated
Fermat prime; Wantzel 1837). **Engine consequence:** the nonagon and its
20°/40° angles must be produced *numerically* (trisection-free, e.g.
θ = 2πk/9 by direct trig), not by an exact ruler-compass construction. This is
not a defect — bikar computes coordinates — but it means there is no "exact
construction" to validate against; the check is angular closure to tolerance
(nine vertices returning to the start), not constructibility.

**Polygons-in-contact inscription.** A rosette is inscribed into a bounding
polygon by the PIC rule of §4: contact points on edges + contact angle θ. For a
9-star the bounding cell is a nonagon (or a nonagon-plus-filler region); the
ribbon rays are placed by θ, and where a wheel meets a neighbour across a shared
edge, the two contact points must coincide for the ribbon to run continuously
(this is the seam-continuity condition the maker prizes).

**What a "spacer / filler" tile is.** In strapwork, when the primary motifs
(here, 9-fold wheels) do not themselves tile the surface, the leftover regions
between them are closed by *filler* / *spacer* tiles carrying their own short
ribbon segments, chosen so the over-under band runs unbroken from wheel to
wheel. Bonner's non-systematic composites (§4) are exactly this: irregular
inter-star regions doing the reconciling. **Engine consequence:** the filler
tile is a first-class object, not an afterthought — the maker's whole point is
that fillers stay *whole* (undistorted) precisely because global symmetry was
sacrificed to keep them so.

**Ribbon / strapwork over-under parity on a closed surface.** A woven strapwork
band alternates over/under at each crossing; on a *closed* surface the parity
must be globally consistent (every closed ribbon must return to its starting
over/under state). This is a 2-colouring / orientation condition on the crossing
graph. No source fetched here states a theorem specific to spherical strapwork
parity, so this is flagged as an **engine-level invariant to verify**, not a
sourced fact: the doc should specify the parity check (e.g. that the crossing
graph is consistently 2-colourable) rather than assert closure holds a priori.

---

## 6. 3D-printing / manifold constraints for a thin strapwork sphere

Kept light — this repo's print-validation research already covers overhang and
tolerance; only the two constraints specific to a thin ribbon sphere are noted.

- **Minimum strut/ribbon width for FDM.** A common, sourced rule is that a wall
  should be at least ~2× the nozzle diameter; for a 0.4 mm nozzle the fetched
  guide gives a **minimum wall of ~1.2 mm** (suitable range 1.2–2.5 mm,
  recommended ~2.0 mm), and notes unsupported walls need more than supported
  ones
  ([raise3d.com/blog/3d-printing-wall-thickness](https://www.raise3d.com/blog/3d-printing-wall-thickness/)).
  A strapwork ribbon *is* an unsupported thin wall over most of its length, so
  the design's ribbon cross-section should sit at the upper end of that range,
  not the 0.8 mm supported-wall floor. (K10: this is a nozzle-relative rule; it
  transfers only for ~0.4 mm-class FDM nozzles — a 0.2 mm or 0.8 mm nozzle
  shifts the floor, and the doc must state the assumed nozzle.)
- **Watertight / manifold.** The mesh must be manifold (every edge shared by
  exactly two faces, no holes) to slice reliably (same source and the general
  FDM guidance surveyed). A ribbon sphere is topologically awkward — many thin
  handles and holes — so the engine must emit a *single closed manifold* where
  ribbons fuse at crossings, not a soup of overlapping bands; the boolean union
  of bands must be watertight, which is the first thing a mesh gate here should
  check.

---

## 7. Fetch record

Each bullet is a URL actually fetched in this session (WebFetch, plus local
`pdftotext` on the PDF bytes WebFetch saved), and what it established. This is
the load-bearing part: every numbered/set claim above is attributed to one of
these.

- [en.wikipedia.org/wiki/Point_groups_in_three_dimensions](https://en.wikipedia.org/wiki/Point_groups_in_three_dimensions)
  — finite SO(3) subgroups = cyclic Cₙ / dihedral Dₙ / T(12) / O(24) / I(60);
  polyhedral rotation axes only orders 2,3,4,5; no 9-fold in any polyhedral
  group. Grounds §1.
- [grail.cs.washington.edu/wp-content/uploads/2015/08/kaplan-2004-isp.pdf](https://grail.cs.washington.edu/wp-content/uploads/2015/08/kaplan-2004-isp.pdf)
  (Kaplan & Salesin, *Islamic Star Patterns in Absolute Geometry*) — one
  construction spans Euclidean/spherical/hyperbolic; verbatim "10-pointed stars
  on the sphere, 12-pointed … Euclidean … 14-pointed … hyperbolic"; knobs θ
  (contact angle) and s (truncation); star orders 8/10/12/14, **no 9**.
  Extracted via pdftotext. Grounds §§1,4,5.
- [cs.uwaterloo.ca/~csk/publications/Papers/kaplan_2017.pdf](https://cs.uwaterloo.ca/~csk/publications/Papers/kaplan_2017.pdf)
  (Kaplan, *Interwoven Islamic Geometric Patterns*, Bridges 2017) — "In 2016 …
  3D printed spherical Islamic star patterns"; module per tile of a polyhedron
  = tiling of the sphere; "based on a truncated icosahedron"; dodecahedral;
  12-pointed. Extracted via pdftotext. Grounds §4 (the closest indexed 3D-
  printed star ball is 10/12 on a polyhedral solid, not 9).
- [cs.uwaterloo.ca/~csk/publications/Papers/kaplan_2005.pdf](https://cs.uwaterloo.ca/~csk/publications/Papers/kaplan_2005.pdf)
  (Kaplan, *Islamic Star Patterns from Polygons in Contact*, GI 2005) — the PIC
  / Hankin contact-angle method paper. Grounds §4/§5 (PIC + contact angle).
- [archive.bridgesmathart.org/2012/bridges2012-593.pdf](https://archive.bridgesmathart.org/2012/bridges2012-593.pdf)
  (Jay Bonner, *Creating Non-Systematic Islamic Geometric Patterns With Complex
  Combinations of Star Forms*, Bridges 2012) — 9-pointed stars live in the
  non-systematic family with irregular filler regions; verbatim composites
  mixing 9- with 12-, 10-, 11-pointed stars. Extracted via pdftotext. Grounds
  §4 (9-and-12 precedent) and §5 (filler tiles).
- [en.wikipedia.org/wiki/Crystal_twinning](https://en.wikipedia.org/wiki/Crystal_twinning)
  — "Twinning, a version of macle …"; twin law "is not one of the normal
  symmetry operations of the untwinned crystal structure" / "not a symmetry
  operation of the full set of basis points". Grounds §2. (Fallback after the
  IUCr dictionary 403'd.)
- dictionary.iucr.org/Twinning — **attempted, HTTP 403, not retrieved.** Noted
  in §0 and §2 as the canonical source that must be re-fetched via an
  authenticated route before its exact wording is quoted.
- [redmaestros.com/maestros-cat/angel-maria-martin-lopez/](https://redmaestros.com/maestros-cat/angel-maria-martin-lopez/)
  — Martín López's lazo work on octagonal roofs and spherical domes; "lazo
  diez" (ten-fold); a course in preparation on *regular* interlace cupolas over
  the whole sphere. Grounds §3 (identity + the ten-fold/regular qualifier that
  distinguishes it from the nine-fold non-regular target).
- [avilared.com/art/76848/…](https://avilared.com/art/76848/felicitaciones-para-angel-maria-martin-premio-europa-nostra-por-la-carpinteria-de-lo-blanco)
  — Europa Nostra 2024 award; CICMA / white-carpentry school. Grounds §3
  identity.
- [lagacetadesalamanca.es/provincia/angel-maria-martin-lopez-…](https://www.lagacetadesalamanca.es/provincia/angel-maria-martin-lopez-restaurador-de-artesonados-hay-joyas-en-salamanca-con-500-anos-que-hacen-su-funcion-como-el-primer-dia-YD6126144)
  — Martín López as restorer of Mudéjar coffered ceilings. Grounds §3 identity.
- [traditionalarchitecturejournal.com/index.php/home/article/view/519](https://www.traditionalarchitecturejournal.com/index.php/home/article/view/519)
  — strapwork-dome paper co-authored by "Ángel María Martín" (UPM); "domes
  based on polyhedral symmetry that respond to the strict layout of the
  strapwork wheels". Grounds §3 (probable-same-person qualifier; note that the
  *symmetric* dome route uses polyhedral symmetry — consistent with §1).
- [history.siggraph.org/artwork/craig-s-kaplan-islamic-patterns/](https://history.siggraph.org/artwork/craig-s-kaplan-islamic-patterns/)
  — "Kaplan has shown how star patterns can be adapted to the hyperbolic plane
  and the sphere"; fabrication via multiple technologies. Supporting context
  for §4 (did not itself carry the star-order numbers — those came from the
  2004/2017 PDFs).
- [isohedral.ca/interwoven-islamic-geometric-patterns/](https://isohedral.ca/interwoven-islamic-geometric-patterns/)
  — Kaplan's blog on the interwoven sculptures; ~20 cm spherical sculpture,
  cube/dodecahedron polyhedral forms. Supporting context for §4.
- [raise3d.com/blog/3d-printing-wall-thickness/](https://www.raise3d.com/blog/3d-printing-wall-thickness/)
  — wall ≥ ~2× nozzle; 0.4 mm nozzle → ~1.2 mm minimum wall (range 1.2–2.5 mm,
  ~2.0 mm recommended); supported vs unsupported distinction. Grounds §6.
- [faculty.etsu.edu/gardnerr/3040/Notes-Eves6/Eves6-5-6.pdf](https://faculty.etsu.edu/gardnerr/3040/Notes-Eves6/Eves6-5-6.pdf)
  — Gauss–Wantzel constructibility criterion for regular polygons (product of a
  power of 2 and distinct Fermat primes). Grounds §5's nonagon claim; the
  9 = 3² consequence corroborated by general web search (Wantzel 1837).

*Web searches (not single-page fetches) additionally corroborated: the SO(3)
finite-subgroup classification (MathWorld, List of spherical symmetry groups);
the 9-gon = 3² non-constructibility; Bonner's systematic/non-systematic
distinction; and FDM manifold/watertight requirements. These are used only as
corroboration of claims already grounded in the fetched sources above.*
