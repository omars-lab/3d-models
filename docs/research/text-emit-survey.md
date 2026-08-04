<!--
  Research produced 2026-08-04 by Claude (Opus 5) under the 3d-models
  design-doc rules, for the text-emit capability that
  docs/calibration-design.md §8 names as the machine card's biggest
  structural weakness.
  Sources: WebSearch and WebFetch against en.wikipedia.org, solhsa.com,
  mandarin3d.com and github.com; one `curl` of
  raw.githubusercontent.com/techninja/hersheytextjs/master/hersheytext.json;
  and first-hand measurement of that file with the Python in §5.4, run on
  this machine on 2026-08-04. Full fetch record in §7.
  Feeds: docs/text-emit-design.md — specifically the font-source choice,
  the stroke-to-outline feasibility bound, and the emboss/engrave question.
  NOTHING WAS INSTALLED. No slicer was run and nothing was printed. Every
  claim about print outcomes in this file is from a vendor or shop guide,
  never from observation; §3 says so per number. The §5 numbers are the
  exception — those are measured, from the font data, not from a print.
-->

# Text emit: font sources, printable stroke widths, and what the geometry costs

## 0. What this file is, and what it is not

[`calibration-design.md`](../calibration-design.md) §3.2 records that "bikar has
no text emit. There is no `text`, no emboss, no engrave", and §8 calls the
resulting loss of rung identity "the card's biggest structural weakness and the
one a text-emit capability would fix outright." This file is the research behind
closing that gap. It answers four questions and refuses a fifth.

| # | Question | Answered by | Kind of answer |
|---|---|---|---|
| 1 | Where does glyph outline data come from, and at what licence? | §1, §2 | Documentary |
| 2 | How small can a printed glyph stroke be and stay legible? | §3 | **Shop guidance, contested** |
| 3 | Can a single-stroke glyph be turned into printable geometry without a general polygon-offset primitive? | §5 | **Measured — and the answer is no** |
| 4 | Is emboss or engrave the safer default? | §3.3, §6 | **Unresolved; the sources disagree** |
| 5 | What does bikar's geometry kernel already provide? | — | Deliberately not here; it is a code survey, not research, and it belongs in the design doc against `path:line` pointers |

The one number in this file that is *ours* — §5's stroke-width bound — is
measured from the font data by a script printed in full in §5.4, so it can be
re-run. Everything in §3 is somebody's shop guidance and is labelled as such.

> **Read this with its companion.** This file asks all four of its questions
> about a **single-stroke centreline** font, and never asks whether a centreline
> is the right input at all. It is not:
> [`outline-font-emit.md`](outline-font-emit.md) measures the outline-font route,
> where the glyph is already a set of closed contours and no offset — and
> therefore no union — is needed. Two sections here were refuted by that
> measurement and carry a marked correction: **§4**, whose conclusion did not
> follow from its premise, and **§5.3**, whose per-join bound names three failing
> glyphs where direct testing finds thirty. §1, §2, §3 and §5.1–§5.2 stand as
> written; §6's route list is superseded by the five-route comparison in
> [`../text-emit-design.md`](../text-emit-design.md) §2.

## 1. The Hershey fonts: provenance

The Hershey fonts are vector (single-stroke, "centreline") letterforms developed
c. 1967 by Dr. Allen Vincent Hershey at the U.S. Naval Weapons Laboratory. Font
data for 1,377 occidental characters was published by NIST in 1976; in their
original form the data is a series of coordinates meant to be connected by
straight lines. Some glyphs exist in four weights — Simplex, Duplex, Complex and
Triplex — differing in how many strokes compose each contour.
([Wikipedia](https://en.wikipedia.org/wiki/Hershey_fonts), fetched 2026-08-04.)

They are the standard choice for engraving, plotting and CNC marking precisely
because they are *centrelines*: a glyph is the path a pen or cutter follows, not
the boundary of an inked region. That property is what makes them attractive
here and also what creates §5's problem.

## 2. Licensing, and a qualifier that gets stripped downstream

This is a **K1 hazard in the wild**, and it is worth stating carefully because
the convenient source is the one that drops the hedge.

**Upstream.** The coordinates as published carry no copyright, but the
distribution that everyone actually uses — James Hurt's Usenet-era reformatting —
carries a USE RESTRICTION with two conditions: acknowledgements naming
Dr. A. V. Hershey (as working at the U.S. National Bureau of Standards) and
James Hurt of Cognition, Inc. must be distributed with the font data, and the
data may be converted into any format **except** the format distributed by the
U.S. NTIS, which holds a copyright on that format. The archived Ghostscript
documentation makes the same NTIS-format point.
([solhsa.com/hershey](https://solhsa.com/hershey/) and
[Wikipedia](https://en.wikipedia.org/wiki/Hershey_fonts), fetched 2026-08-04.
solhsa notes NTIS "reportedly does not enforce" restrictions on other formats —
a report, not a legal opinion, and reproduced here as one.)

**Downstream.** [`techninja/hersheytextjs`](https://github.com/techninja/hersheytextjs),
the JSON port this file measures, states its terms as "JSON data Public Domain,
All other code MIT Licensed" (fetched 2026-08-04) and says nothing about the
acknowledgement.

Those two statements are not the same statement. A repackager's "public domain"
does not discharge an upstream condition, and the cost of honouring it is two
sentences in a source comment. **Whatever route is taken, carry the
acknowledgement.** Note also that the restriction constrains *format*, not use:
converting the coordinates into a TypeScript constant is expressly the permitted
direction, and reproducing the NTIS distribution format is the prohibited one.

Alternative sources exist and were not evaluated in depth:
[`hersheytext` on npm](https://www.npmjs.com/package/hersheytext),
[`chazu/hershey-js`](https://github.com/chazu/hershey-js),
[`golanlevin/p5-single-line-font-resources`](https://github.com/golanlevin/p5-single-line-font-resources)
(an archive of monoline fonts, several not Hershey-derived and under their own
terms), and [`scruss/AVHershey-OTF`](https://github.com/scruss/AVHershey-OTF)
(OpenType wrappers of Hershey subsets). This is **five sources located, not the
space of single-stroke font data.**

## 3. How small a printed glyph can be — and the contradiction at the centre of it

### 3.1 The numbers

[Mandarin3D's text guide](https://mandarin3d.com/blog/text-and-engravings-best-practices-for-readable-3d-printed-text)
(fetched 2026-08-04) gives the most specific table found, assuming a 0.4 mm
nozzle at 0.1–0.2 mm layers:

| | line width min | line width rec. | depth/height min | depth/height rec. | char height min | char height rec. |
|---|---|---|---|---|---|---|
| **Engraved** | 0.5 mm | 0.8 mm | 0.3 mm | 0.5 mm | 3 mm | 5 mm |
| **Embossed** | 1.0 mm | 1.5 mm | 0.5 mm | 0.8 mm | 4 mm | 6 mm |

plus two nozzle-relative rules: multiply nozzle diameter by **2.5** for a minimum
feature width (1.0 mm at 0.4 mm), and by **6** for the smallest readable
character width (2.4 mm). It also splits by orientation — 16 pt bold minimum on
top/bottom surfaces, 10 pt bold on vertical walls.

**None of these is presented as a measurement.** They are a print shop's rules of
thumb, stated as such, and every one of them is about *somebody else's* printer.
Under [K10](../../CLAUDE.md) none of them transfers to this project's machine
without the sentence that says why — and no such sentence can be written, because
the machine is uncharacterized. That is the entire reason the machine card exists.

### 3.2 What that means for a default

The design doc must not adopt 0.8 mm or 1.0 mm as a gate-marked default. The honest form
is a `CAL-*` bet settled by a coupon: a legibility ladder that prints the same
label at a descending series of stroke widths and asks which is the last one that
can be read. That is the same shape as every other rung on the card, and the
ladder can ride the card itself.

### 3.3 The contradiction

Search-result summaries of the general shop advice say **embossed text usually
prints clearer than engraved**. The Mandarin3D page, read directly, says the
opposite: it recommends engraved as "more forgiving to print, survives real-world
use better" than embossed, which suffers contact and wear damage.

These are not reconcilable by reading harder — they are two shops' experience
pointing opposite ways, and one of them is a *durability* argument while the
other is a *fidelity* argument, which is probably the whole explanation. It does
mean the emboss/engrave choice cannot be settled from the literature. §6 records
a geometric argument that cuts the other way from Mandarin3D's, which makes three
positions and no winner.

## 4. What OpenSCAD's `text()` costs — and why this section was wrong

> **CORRECTED 2026-08-04, same day, before this file fed any design doc.**
> This section originally concluded that the outline-font route was "closed
> here". The conclusion does not follow from its own premise, and the
> measurement that replaces it is in
> [`outline-font-emit.md`](outline-font-emit.md). The original text is kept
> below the rule, because *how* it went wrong is the reusable part.

OpenSCAD's `text()` is built on three C++ libraries: **FreeType2** for outline
extraction, **HarfBuzz** for shaping, and **fontconfig** for matching a font
description to a font file on the system.
([openscad/openscad#512](https://github.com/openscad/openscad/issues/512) and
the linked discussion, fetched 2026-08-04.)

**What is still true.** The fontconfig half cannot exist in the browser. bikar's
Lab and studio are deployed as static bundles; there is no system font directory
to match against. Any font must be *embedded in the bundle*, not resolved at run
time. A `text` feature that behaved differently in the CLI and in the Lab would
be a worse gap than the one it closes.

**What was wrong, and how.** The paragraph below concluded from that constraint
that outline fonts are "the heavy option", and the rest of this file then spent
its entire measurement budget on the single-stroke route without ever asking
whether a centreline is the right *input*. Three separate errors:

1. **Two different things were conflated.** fontconfig does font *matching*;
   FreeType does outline *extraction*. Only the first is impossible in a browser,
   and it is the one you do not need — the font is pinned, not matched.
2. **The extraction cost was assumed, not measured.** The comparison should never
   have been "a parser plus a font file" against "coordinates". Flattening can
   run at **build time**, and then the runtime payload is coordinates in both
   cases: **13,710 bytes** of closed rings for 37 glyphs against futural's 7,503
   bytes for 95 — roughly double, for a route with no offset in it at all.
3. **The decisive property was never named.** A TTF/CFF glyph is a set of
   **closed** contours with counters as holes. §5's whole problem — a centreline
   has no width, so it needs an offset, so it needs a union — simply does not
   arise. That is not a cost comparison; it is a different problem.

This is a K10 failure in its own right: a constraint established for *font
matching in a static bundle* was carried to *outline extraction* without the
sentence saying why it transfers. It does not transfer.

---

*Original text, superseded:*

> Two consequences for bikar:
>
> 1. **The fontconfig half cannot exist in the browser.** …
> 2. **Outline fonts are the heavy option.** The TypeScript equivalent of the
>    FreeType half is a TTF/OTF parser plus a font file. A single-stroke font is
>    coordinates and nothing else — §5.1 measures it at **7,503 bytes** for a
>    complete 95-glyph face.
>
> bikar's own precedent points the same way: it vendors `earcut` into
> `kernel3d/earcut-vendored.ts` rather than taking a dependency.

The vendoring precedent survives the correction and now argues the other way:
`earcut` is vendored because it is small and does one job, and
`kernel3d/earcut-vendored.ts` is exactly what an extruded glyph outline is handed
to.

## 5. The measurement that decides the design

### 5.1 What a single-stroke face actually contains

Measured on 2026-08-04 from `hersheytext.json` (476,882 bytes, 20 faces), taking
the `futural` face — Hershey Simplex sans, the plain single-stroke roman:

| Quantity | Value |
|---|---|
| Glyphs | **95**, ASCII 33–127 |
| Minified JSON, this face alone | **7,503 bytes** |
| Coordinate extent | x 0…26, y −3…29 (cap height 21 units, y 1…22) |
| Advance widths | 4…15 units |
| Open polylines | **188** total, mean 1.98 per glyph, max 4 sub-strokes (`M`, `W`, `w`, `[`, `]`) |
| Segments | **940** total, mean 9.89 per glyph, longest polyline 34 points |
| Segment lengths | min 1.00, p10 1.41, median 2.83, max 36.72 units |
| A realistic label, `MC-2 R08` | **90 segments** |

A glyph is `{"d": "M4,1 L4,22 M4,1 L18,22 M18,1 L18,22", "o": 11}` — SVG-ish path
data in which `M` starts a new open sub-stroke, and `o` is the advance width.

### 5.2 The problem: a centreline has no width

Every one of those 188 polylines is **open and zero-width**. Turning one into
printable geometry means giving it a width, which is the stroke-to-outline
operation, which is a polygon offset. [`backlog.md`](../backlog.md) §6.2 records
that bikar has no polygon-offset primitive — the same absence that already forces
MC-4's wall thickness to co-vary with the angle under test
([`calibration-design.md`](../calibration-design.md) §5.4, §8).

So the question is whether the offset can be done *analytically* for this
restricted case. Offsetting an **open polyline** is genuinely easier than
offsetting a general polygon: walk one side forward, the other side back, and
insert a fan at each convex join. It needs no boolean — **unless the inner side
folds over itself.**

At a join whose turn angle is `t`, the inner offset edge runs backward by
`(w/2)·tan(t/2)`. It folds when that exceeds the shorter adjacent segment:

```
safe half-width  w/2  ≤  min over joins of  min(len_prev, len_next) / tan(t/2)
```

### 5.3 The result

Measured over the 37 glyphs a rung label needs (`0-9`, `A-Z`, `-`), at a 5 mm cap
height (1 unit = 0.238 mm):

| Glyph | Tightest join | Max stroke before the offset self-intersects |
|---|---|---|
| `5` | 141° turn, adjacent segments 9.06 and 1.41 u | **0.24 mm** |
| `3` | 127° turn, segments 10.00 and 3.00 u | 0.71 mm |
| `1` | 135° turn, segments 4.24 and 21.00 u | 0.84 mm |
| `2` | 27° turn | 2.02 mm |
| `S` | 45° turn | 2.30 mm |
| `6`, `8`, `9` | 45° turn | 2.57 mm |
| the other 29 | — | ≥ 2.85 mm, median unconstrained |

**The naive analytic offset does not survive contact with the alphabet.** It
fails on three glyphs — `5`, `3`, `1` — and `5` fails by more than 4×: it caps
the stroke at 0.24 mm against §3.1's 1.0 mm minimum printable feature. Scaling up
does not rescue it; at a 10 mm cap height `5` still caps at 0.47 mm, because the
bound scales linearly with the type size while the printability floor does not
scale at all.

> **CORRECTED 2026-08-04 — three is a floor, not a count.** The bound above is
> computed **per join**, from that join's own turn angle and its two adjacent
> segment lengths. It can therefore only ever see the failure mode where an
> offset edge folds back over its own join. Building the offset outline and
> testing *it* for self-intersection — rather than testing the local bound that
> predicts one class of self-intersection — finds **30 of the 37 glyphs** broken
> at a printable width, in four classes:
>
> | Class | Glyphs | What breaks |
> |---|---|---|
> | *fold* | 3 | the join folds — the only class this bound sees |
> | *seam* | 4 | two strokes of one glyph are drawn as separate polylines and their offsets overlap |
> | *approach* | 2 | two non-adjacent parts of one polyline pass within `w` of each other |
> | *multi* | 22 | the glyph is several polylines whose offset bodies simply intersect |
>
> The bound is *correct about the glyphs it names* and blind to the other three
> classes, all of which are non-local: no property of a single join can detect
> two strokes that only meet each other. The measurement, the classifier and the
> per-glyph breakdown are in
> [`outline-font-emit.md`](outline-font-emit.md).
>
> This is the same tenet as the first bullet below, one level up and pointed at
> the method rather than the sample: **an aggregate cannot discharge a claim
> about every part — and neither can a local test.** Both times the failure was
> the same shape: something cheap was measured, and the claim was written about
> something else.

Two things about this number matter more than the number:

- **The median is a lie here.** The median glyph's bound is *unconstrained* — no
  join tightens it at any width. A survey that reported the median, or that
  sampled a few letters, would have concluded the analytic offset ships. This is
  [CLAUDE.md](../../CLAUDE.md)'s "an aggregate cannot discharge a claim about
  every part", arriving unprompted in a second domain.
- **The failing glyphs are not exotic.** `5` and `3` and `1` are digits, and a
  rung label is mostly digits. `MC-5`, and every rung index past R09, contains one.

### 5.4 The script, so the numbers can be re-derived

```python
"""Max stroke width before a two-sided offset of a Hershey `futural` polyline
self-intersects at a join. Run 2026-08-04 against hersheytext.json fetched from
raw.githubusercontent.com/techninja/hersheytextjs/master/hersheytext.json."""
import json, re, math

chars = json.load(open('hersheytext.json'))['futural']['chars']

def polylines(s):
    out = []
    for sub in s.split('M'):
        sub = sub.strip()
        if not sub:
            continue
        pts = [(int(a), int(b)) for a, b in re.findall(r'(-?\d+),(-?\d+)', sub)]
        if len(pts) >= 2:
            out.append(pts)
    return out

CAP = 21.0                       # glyph units from baseline y=1 to cap y=22
for ch in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-":
    lim = float('inf')
    for pts in polylines(chars[ord(ch) - 33]['d']):
        for k in range(1, len(pts) - 1):
            p, q, r = pts[k - 1], pts[k], pts[k + 1]
            v1 = (q[0] - p[0], q[1] - p[1])
            v2 = (r[0] - q[0], r[1] - q[1])
            l1, l2 = math.hypot(*v1), math.hypot(*v2)
            if l1 == 0 or l2 == 0:
                continue
            cos = max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (l1 * l2)))
            t = math.acos(cos)                      # turn angle at the join
            if t < 1e-9:
                continue
            lim = min(lim, min(l1, l2) / math.tan(t / 2))   # max half-width here
    print(f"{ch!r}: max stroke {2 * lim * 5.0 / CAP:.2f} mm at a 5 mm cap height")
```

## 6. The three routes out, and what each one costs

§5 rules out "offset it analytically and ship." What is left:

**A. A real 2D union.** Emit each stroke segment as a rectangle and each join as
a disc, then union them. Every input is convex, which is the well-conditioned
case for a union, and the result is a genuine non-self-intersecting outline that
extrudes cleanly and works for both emboss and engrave. Cost: a union that
handles ~90 primitives per label robustly. Whether bikar's
`graph/polygon-union.ts` already does this in the general case is a code
question, not a research question, and is left to the design doc.

**B. Interpenetrating closed solids, unioned by the slicer.** Extrude each
segment as its own closed capsule and let them overlap. This needs no boolean at
all. **It is the riskiest of the three and the literature says so.** Cura's
"Union overlapping volumes" is documented as addressing problems *inside a single
mesh* — which is our case — while interaction *between* meshes is governed by a
different setting; PrusaSlicer's behaviour depends on whether the second body was
loaded as a sub-part or as a separate object, and
[PrusaSlicer#2501](https://github.com/prusa3d/PrusaSlicer/issues/2501) is titled
"overlapping objects do not get sliced correctly". Repair-tool guidance treats
self-intersecting meshes and overlapping shells as the class basic repair cannot
fix. (All fetched 2026-08-04 via search summary; **the PrusaSlicer issue was not
read in full and no slicer was run** — this is documentary, and route B's real
status is untested.) This is the export-succeeds-and-yields-the-wrong-thing class
that [`lego-lab-design.md`](../lego-lab-design.md) §14.3 exists to avoid.

**C. Don't use a font.** The requirement in
[`calibration-design.md`](../calibration-design.md) §3.2 is *rung identity*, not
arbitrary text: a rung must say which rung it is. A row of dots, a notch count,
or a small binary pip field says that with **convex primitives bikar already
has**, no offset, no union, and features an order of magnitude above the
printability floor. It is strictly more robust than either A or B and strictly
less legible than both — you count rather than read. It is worth noting that it
is *not* the failure §3.2 complains about: §3.2's problem is counting positions
*on a plate*, which is lost the moment a part is knocked off; counting pips *on
the part* survives everything.

**A geometric argument that contradicts §3.3.** In the no-boolean world, emboss
and engrave are not symmetric. Emboss adds material, so route B's interpenetrating
capsules are at least a *plausible* union. Engrave removes it, and subtracting
interpenetrating tool solids is not something an STL can express at all — it needs
a real boolean or a slicer modifier mesh. So on geometry grounds **emboss is the
cheap one**, which is the opposite of Mandarin3D's durability-based preference for
engraving. Three positions, no winner: this is a decision to take, not a fact to
look up.

## 7. Fetch record

| Source | URL | Fetched | Used for |
|---|---|---|---|
| Wikipedia, Hershey fonts | https://en.wikipedia.org/wiki/Hershey_fonts | 2026-08-04 | §1 provenance, §2 NTIS-format restriction |
| solhsa.com Hershey page | https://solhsa.com/hershey/ | 2026-08-04 | §2 USE RESTRICTION terms, glyph counts, format caveats |
| Mandarin3D text guide | https://mandarin3d.com/blog/text-and-engravings-best-practices-for-readable-3d-printed-text | 2026-08-04 | §3.1 table, §3.3 engrave-is-more-forgiving position |
| techninja/hersheytextjs | https://github.com/techninja/hersheytextjs | 2026-08-04 | §2 downstream licence claim, §5 data format |
| `hersheytext.json` | https://raw.githubusercontent.com/techninja/hersheytextjs/master/hersheytext.json | 2026-08-04 (`curl`) | §5 — all measurements |
| openscad/openscad#512 | https://github.com/openscad/openscad/issues/512 | 2026-08-04 | §4 FreeType/HarfBuzz/fontconfig stack |
| Search summary, slicer union behaviour | Cura community forum, PrusaSlicer forum + issue 2501, Polyvia3D repair guide | 2026-08-04 | §6 route B risk — **summaries only, not read in full** |
| hersheytext (npm), chazu/hershey-js, golanlevin/p5-single-line-font-resources, scruss/AVHershey-OTF | see §2 links | 2026-08-04 | §2 alternatives, located but not evaluated |

## 8. What could not be determined

- **Whether emboss or engrave is right for this project's parts.** §3.3 and §6
  give three arguments pointing two ways. A coupon settles it; the literature
  does not.
- **The legible minimum stroke width on the actual machine.** Uncharacterized by
  construction — this is what the machine card is for. Every number in §3.1 is
  another shop's.
- **Whether route B survives a real slicer.** Nothing was sliced. The evidence in
  §6 is documentary and partly from search summaries rather than full reads, and
  a single run of the real thing would outrank all of it.
- **Whether `futural` is the right face.** It was measured because it is the plain
  single-stroke roman. `futuram` (a heavier duplex) was not measured, and a
  duplex face changes §5's bound in an unknown direction — more strokes per glyph,
  but potentially gentler joins.
- **The generality of bikar's existing union.** Out of scope here on purpose; §0
  says why.
