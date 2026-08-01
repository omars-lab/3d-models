<!--
  Research produced 2026-08-01 by Claude (Opus 5) under the 3d-models
  design-doc rules, for the LDraw half of Lego Lab phase P3.
  Sources: WebFetch against ldraw.org/leocad.org/tcobbs.github.io/
  studiohelp.bricklink.com (fetch record in §0), plus first-hand reading of
  bikar at worktree `bikar-lego-lab`, branch `main`, commit 9cca1ae, and of
  `docs/research/lego-brick-system-survey.md` in this repo.
  Feeds: docs/lego-lab-design.md §10 P3 — the `.ldr` placement export only.
  Measurements produced by this file were run against bikar's built
  `packages/core/dist/index.js` at 9cca1ae; reproduction recipe in §5.4.
-->

# LDraw `.ldr` export for generated bricks — what the format permits, and what it costs

*Research date: 2026-08-01. Scope: the LDraw export line of `docs/lego-lab-design.md`
§10 P3 only. Per-family print notes and adjusted-parameter toasts are out of scope
and are not discussed.*

The P3 row and §13 both state the blocker in one sentence: *"a generated brick is not
an LDraw part and has no part number, so a type-1 line has nothing to reference."*
That sentence is correct, and it is the whole of §3 below. §§1–2 establish the format
facts it rests on, §4 answers the scale question, §5 records what bikar's data
structures actually hold, §6 recommends, §7 is a full worked example, and §8 lists
what could not be grounded.

---

## 0. Fetch record — what was actually retrieved, and what was not

Every load-bearing number and quotation below is attributed to one of these. **All
web access in this session was via WebFetch; WebSearch was unavailable (per-session
budget exhausted), so no exploratory search was performed** and the URL set below is
the set I could reach by following links from the spec index. That is a real limit on
the exhaustiveness of §3's viewer survey and §8 records it.

| # | Source | URL | Status |
|---|---|---|---|
| S1 | LDraw File Format Specification 1.0.2 | https://www.ldraw.org/article/218.html | fetched (4 passes) |
| S2 | LDraw.org Official Library Header Specification | https://www.ldraw.org/article/398.html | fetched |
| S3 | MPD and Image Embedding Language Extension | https://www.ldraw.org/article/47.html | fetched, incl. the full worked example |
| S4 | Official Model Repository (OMR) Specification | https://www.ldraw.org/article/593.html | fetched |
| S5 | OMR Rules and Procedures | https://www.ldraw.org/docs-main/official-model-repository-omr/rules-and-procedures-for-the-official-model-repository.html | fetched |
| S6 | LDraw Part Number Specification | https://www.ldraw.org/part-number-spec.html | fetched |
| S7 | BFC (back-face culling) Language Extension | https://www.ldraw.org/article/415.html | fetched |
| S8 | LDView Help | https://raw.githubusercontent.com/tcobbs/ldview/master/Help.html | fetched |
| S9 | LDView home page | https://tcobbs.github.io/ldview/ | fetched |
| S10 | LeoCAD — Parts Library docs | https://leocad.org/docs/library.html | fetched |
| S11 | LeoCAD — Meta Commands docs | https://leocad.org/docs/meta.html | fetched |
| S12 | BrickLink Studio — Import formats | https://studiohelp.bricklink.com/hc/en-us/articles/6502277722647-Import-formats | fetched |
| S13 | This repo's own LEGO survey | [`lego-brick-system-survey.md`](lego-brick-system-survey.md) | read on disk |
| S14 | This repo's lattice sweep | [`lego-lattice-matrix-sweep.md`](lego-lattice-matrix-sweep.md) | read on disk |

**Retrieval failures, disclosed:**

- `https://www.ldraw.org/article/218.html` fetched by `curl` returns
  *"Sorry, something has gone wrong. Please contact a site administrator.
  (CMSMS\Database\DatabaseConnectionException)"* — 124 bytes. The WebFetch path
  succeeded. Anyone re-checking these quotations should use a browser, not `curl`.
- `https://www.ldraw.org/documentation/ldraw-org-file-format-standards.html`,
  `https://www.leocad.org/docs/`, `https://www.leocad.org/docs.html`,
  `https://library.ldraw.org/official/parts/3001.dat`,
  `https://library.ldraw.org/official/p/stud.dat` — all **404**. Per-file LDraw web
  paths not resolving is the same failure S13 recorded on 2026-07-29
  (*"Per-file LDraw web paths (`ldraw.org/library/official/p/stud4.dat`) 404 — the
  library must be taken as the zip"*), so **every claim below about the content of a
  specific `.dat` file is quoted from S13's first-hand reading of the downloaded
  library, not re-verified by me.**
- S1's "File Type" section returned as a garbled fragment on the pass that asked for
  it verbatim (`"File -, Submodel -, Element +, Sub-part +, …"` — evidently a table
  the markdown conversion flattened). **I do not rely on it.** §2 uses S2 and S4,
  which state the type values in prose.
- BrickLink Studio's PartDesigner help category returned only navigation chrome, and
  the Studio import article says nothing about unknown parts. See §8.

---

## 1. The format facts

### 1.1 The type-1 (sub-file reference) line

S1, verbatim:

> Line type 1 is a sub-file reference. The generic format is:
>
> `1 <colour> x y z a b c d e f g h i <file>`
>
> Where:
>
> - `<colour>` is a number representing the colour of the part. See the Colours
>   section for allowable colour numbers.
> - `x y z` is the x y z coordinate of the part
> - `a b c d e f g h i` is a top left 3x3 matrix of a standard 4x4 homogeneous
>   transformation matrix. This represents the rotation and scaling of the part.

The matrix layout, also S1 verbatim:

```
/ a d g 0 \     / a b c x \
| b e h 0 |  or | d e f y |
| c f i 0 |     | g h i z |
\ x y z 1 /     \ 0 0 0 1 /
```

> The transformed point (u', v', w') can be calculated from point (u, v, w) as
> follows: u' = a\*u + b\*v + c\*w + x   v' = d\*u + e\*v + f\*w + y
> w' = g\*u + h\*v + i\*w + z

So the field order on the wire is **row-major** — `a b c` is the first row of the
matrix that multiplies the sub-file's coordinates. The 4×4 shown on the left is the
same matrix transposed; the arithmetic line is the one to implement against, and it
is unambiguous.

Two things the spec says about the matrix that matter here:

1. It **"represents the rotation and scaling of the part."** Scaling is explicitly
   permitted, not merely tolerated. §4 uses this.
2. I asked S1 specifically for text about the **determinant, mirroring, or winding of
   a type-1 matrix** and the fetch reported none present. So the format spec, as
   fetched, places **no constraint on the determinant** of a type-1 matrix. (This is
   a claim about S1 only. The BFC extension S7 governs winding; a negative-determinant
   reference inverts winding, and S7's `0 BFC INVERTNEXT` exists for that class of
   problem. Our export never needs a non-proper matrix — see §5.3 — so I did not
   pursue it further.)

Colour, S1 verbatim:

> Colour 16 is referred to as the "main colour" or "current colour". When a sub-file
> is referenced by another file all the colour 16 command lines are displayed using
> the colour of the line that referenced it.

> Colour 24 is referred to as the "complement colour" or "edge colour". Colour 24 is
> most commonly used for line types 2 (line) and 5 (optional line).

Note the hedge: **"most commonly used for"** — not *reserved for*. Carried as-is.

The consequence for our emitter: geometry inside a generated part should be written
in colour 16 so the part takes whatever colour the type-1 line that placed it names.
A type-1 line at the **top level of a model has no referencing line**, so colour 16
there has nothing to inherit from; the emitter must name a concrete code. S3's own
worked example uses codes `7` and `4` at top level. **I did not fetch `LDConfig.ldr`
and therefore make no claim about which colour name any numeric code renders as.**

### 1.2 The other line types

S1, verbatim: type 0 is `0 // <comment>` or `0 <comment>` — *"Line type 0 has two
uses. One use is a comment the other is as a META command."* Types 2/3/4/5:

```
2 <colour> x1 y1 z1 x2 y2 z2                                     line
3 <colour> x1 y1 z1 x2 y2 z2 x3 y3 z3                            filled triangle
4 <colour> x1 y1 z1 x2 y2 z2 x3 y3 z3 x4 y4 z4                   filled quadrilateral
5 <colour> x1 y1 z1 x2 y2 z2 x3 y3 z3 x4 y4 z4                   optional line
```

On quad winding, S1 verbatim: *"While no specific order (winding) is required, the
points of the quadrilateral must be declared in either a clockwise (CW) or
counter-clockwise (CCW) order."*

### 1.3 The LDU, in millimetres

S1 gives **two** conversions and hedges both:

> 1 LDU = 1/64 in
>
> 1 LDU = 0.4 mm
>
> These real world approximations are just that: approximations.

S1 also fixes the LEGO-relative sizes: **1 brick width/depth = 20 LDU, 1 brick height
= 24 LDU, 1 plate height = 8 LDU, 1 stud diameter = 12 LDU.**

**The two conversions are not the same number and the difference is not negligible.**
1/64 in = 0.396875 mm, so 20 LDU is 8.000 mm under one and 7.9375 mm under the other —
a 0.78 % difference, which over a 32-stud model is 2.0 mm. The design doc's §3.1 stud
pitch is 8.0 mm and bikar's `STUD_PITCH_MM` is `8.0` (`packages/core/src/kernel3d/lego.ts:34`).

**K10 — why 0.4 mm/LDU transfers into our emitter and 1/64 in does not.** The emitter
needs the conversion under which 20 LDU reproduces the pitch the geometry was authored
at. 20 × 0.4 = 8.000 exactly; 20 × (1/64 in) = 7.9375, which is not the pitch any
number in the design doc was derived under. It is also the conversion S13 read the
whole §3.1 dimension table under (*"1 LDU = 0.4 mm ≈ 1/64 in, with the official
specification's own caveat"*), so using it keeps the export dimensionally consistent
with the table the geometry came from. The 1/64-in figure does **not** transfer and
must not be offered as an option in the emitter.

The spec's own hedge survives that: 0.4 mm/LDU is the conversion this project should
use, and it remains an *approximation of a real-world size* by the spec's own words —
not a statement that any LEGO element measures exactly 20 LDU.

### 1.4 Axis conventions, and the map from a Z-up mesh

S1, verbatim: **"LDraw uses a right-handed co-ordinate system where -Y is 'up'."**

S13, from first-hand reading of the library zip: *"LDraw's Y axis points down, so a
brick's top face is y = 0 and its bottom is y = 24."* — i.e. in the part files S13
read, a brick's local origin sits on the **top plane of the brick body**, with the
studs occupying y = 0 → −4 and the body y = 0 → +24. S13 names `parts/3001.dat`,
`parts/3004.dat` and `p/stud.dat` among the files read. **This is a statement about
the files S13 read, not a spec statement**; I could not re-fetch the `.dat` files (§0),
and S1 as fetched says nothing about where a part's origin goes.

bikar's mesh frame is right-handed millimetres with **+z up** and the brick's bed at
z = 0 (`brick-ports.ts:72` — *"The bed face — z = 0, the brick's underside"* — and
:52, the top face at `provenance.heightMm`). `frame.ts:214` notes that a proper
rotation (det +1) preserves triangle winding and outward normals.

The map from bikar millimetres to LDraw LDU is therefore

```
C = [ 1  0  0 ]        (x, y, z)  ->  (x, -z, y)        det(C) = +1
    [ 0  0 -1 ]
    [ 0  1  0 ]
```

`det(C) = 1·(0·0 − (−1)·1) = +1`, so **the map is a proper rotation: it takes bikar's
right-handed frame to LDraw's right-handed frame without mirroring, and preserves
triangle winding.** The alternative `(x, y, z) → (x, −z, −y)` has det −1 and would
silently invert every face; it must not be used.

Folding in the LDU divisor and the origin convention of §1.4, a brick vertex at
bikar-local `(x, y, z)` mm on a brick of height `H` mm emits as

```
X = x / 0.4        Y = (H − z) / 0.4        Z = y / 0.4          (LDU)
```

which puts the bed at `Y = H/0.4`, the top face at `Y = 0` and a 1.6 mm stud crown at
`Y = −4` — matching S13's reading of `3001.dat`. §5.4's run confirms it numerically:
the first emitted triangle of a 2×4 is `3 16 -19.75 24 -39.75 …` (bed corner) and the
last is `3 16 15.6395 -4 28.8782 …` (stud crown, exactly −4).

**K10 — when the "origin on the top face" convention transfers.** It transfers *if
and only if* the export is meant to sit in the same file as library parts. Its whole
value is that a user who drops a `3001.dat` next to our brick gets it in the right
place. If the export were only ever going to contain our own bricks, any consistent
origin would do — but then the first stock part a user adds is 9.6 mm out, silently.
Since interoperation is the only reason to emit `.ldr` at all, the convention
transfers and the emitter should adopt it.

---

## 2. Header and meta lines

### 2.1 What the format spec itself requires

S1, verbatim: *"If the first line of a file is a line type 0 the remainder of the line
is considered the file title."* That is the only header requirement I found in S1.
S1 also states: *"All LDraw files carry the LDR (default), DAT or MPD extension."*

**S1, as fetched, imposes no other required header line on a model file.** Everything
in §2.2 and §2.3 comes from specifications that are scoped to *submission* to an
LDraw.org repository, and §2.4 says what that scoping means for us.

### 2.2 The parts header spec (S2) — scoped to the Official Library

S2 defines `0 !LDRAW_ORG <type>` with these values, verbatim as returned:

> Part | Subpart | Primitive | 8_Primitive | 48_Primitive | Shortcut are used in
> Official Library Parts

and, for unofficial parts, `Unofficial_Part | Unofficial_Subpart |
Unofficial_Primitive | Unofficial_8_Primitive | Unofficial_48_Primitive |
Unofficial_Shortcut`.

`0 Name:` — *"Filename is the file name of the part including the folder (e.g. s/, 48/)
if it is not directly in the parts or p folders."*

`0 Author:` — *"RealName is the author's real name. UserName is the author's LDraw
username. It is optional for those authors that had parts released prior to the
establishment of the Parts Tracker and have not contributed since."*

`0 BFC` — S2, verbatim: *"A `0 BFC CERTIFY CCW` command is required for Official
Library parts. For all other uses it is highly recommended … but not required."*

S2 also states: *"No other meta-commands are allowed in the part header other than
those specified in this document."*

The fetch reported S2's scope as **the Official Library**: *"the LDraw Official
Library header format suitable for the implementation of the Contributor Agreement"*,
and that it *"does not address general model files."*

### 2.3 The OMR spec (S4) — the model-file header

S4 is the document that specifies a *model* header. Required, per the fetch:

```
0 FILE <Filename>.ldr
0 <Individual filename>                     (the description / title line)
0 Name: <Filename>.ldr
0 Author: <Author Name> [Username]
0 !LDRAW_ORG Model      -OR-   0 !LDRAW_ORG Unofficial_Model
0 !LICENSE Licensed under CC BY 4.0 : see CAreadme.txt
```

Optional per S4: `0 !THEME`, `0 !KEYWORDS`, `0 !HISTORY`.

S5 confirms the licence line as a gate on acceptance: *"The OMR will only consider new
models that contain the `0 !LICENSE Licensed under CC BY 4.0 : see CAreadme.txt`
statement."*

**`Model` and `Unofficial_Model` are the two allowed `!LDRAW_ORG` values for a model
file, and they come from S4 — not from S1 and not from S2.**

### 2.4 Required vs conventional — the honest split

| Line | Required by | Required *for us*? |
|---|---|---|
| `0 <title>` on line 1 | S1 (defines what line 1 means, does not mandate it) | conventional; cheap and worth writing |
| `0 FILE <name>` | S3, to open an MPD block; S4, for OMR models | **required** for the MPD option (§3), otherwise not |
| `0 Name:` | S2 (library parts), S4 (OMR models) | conventional |
| `0 Author:` | S2, S4 | conventional |
| `0 !LDRAW_ORG` | S2 (parts), S4 (models) | conventional |
| `0 !LICENSE` | S4, and S5 as an acceptance gate | conventional — and see below |
| `0 BFC CERTIFY CCW` | S2 for Official Library parts only | optional; see §5.3 |

**K10 — these do not transfer as requirements, only as conventions.** Every "required"
in S2 and S4 is required *for acceptance into an LDraw.org repository*. A file we
generate for a user's own viewer is submitted nowhere, so nothing in S2 or S4 binds it.
What does transfer is the *reader's expectation*: a viewer that has parsed thousands of
library files is being handed a file shaped like the ones it has seen, which costs us
six lines. So: **write them, and do not claim the file is "spec-compliant" on the
strength of having written them** — the specs that define those lines do not have
jurisdiction over this file.

The `0 !LICENSE` line is the one exception to "write them all". Its S4 text asserts a
specific CC BY 4.0 grant referring to LDraw's `CAreadme.txt`; writing that on a file
generated from this project's geometry would be a licensing statement about *our*
geometry that nobody in this project has made. **Do not emit `0 !LICENSE` by copying
S4's string.** Emit whatever licence this repo actually grants, or emit none.

S7 (BFC) settles what happens when BFC is absent, verbatim: *"If a file has no 0 BFC
meta-statement before the first operational command-line, 0 BFC NOCERTIFY is assumed
and BFC processing will be disabled for the file."* So omitting BFC is safe — it costs
render performance and possibly some shading quality, not correctness.

---

## 3. The hard problem — a part that is not in the LDraw library

### 3.1 There is no user namespace to put it in

S6, the part-number spec, verbatim on naming:

> If the part number (Design ID) used by LEGO is known, then that number should be
> used.

> If LEGO part number is not known, "u" prefix is used (e.g. u1234.dat). … This number
> will be requested from the Parts Library Admin prior to submitting the part to the
> Parts Tracker.

> Third party parts will have a tNNNN.dat format where NNNN is a number assigned by the
> Library Administrator.

So the three namespaces S6 defines — `NNNN`, `uNNNN`, `tNNNN` — are **all
administrator-assigned**, and the fetch reports that S6 *"does not explicitly reserve
a namespace for user-created custom parts outside the official library context."*

There is therefore no legitimate part number for a generated brick, and there is no
reserved prefix that guarantees a generated name will never collide with a future
library part. The practical mitigation is to pick a name that is *structurally*
outside all three namespaces — one that begins with letters and contains a hyphen, e.g.
`bikar-ClassicBrick-2x4-3p-<hash>.dat` — so it can never be confused with `3001.dat`,
`u1234.dat` or `t0042.dat`. That is a mitigation, not a guarantee, and the reason it
matters is S3's scoping statement, quoted next.

### 3.2 What MPD permits, and its one sharp edge

S3, verbatim:

> MPD files or "Multi-Part Documents" are a way to combine several LDraw and encoded
> binary files into one consolidated source.

> Blocks starting with the 0 FILE statement are normal type 0..5 line LDraw code.

> The first block in the MPD is treated as the "main model" -- all other files in the
> MPD will only be rendered if they are referenced by the main model, directly or
> indirectly.

> The end of each block, or just the last block in the MPD, may be marked with a
> 0 NOFILE line.

`0 FILE <filename>` — *"Where: `<filename>` is the name of the following LDraw file."*
`0 NOFILE` — *"There are no options or parameters."*

And the sharp edge, S3 verbatim:

> So far, there are no clear scoping or namespace rules on MPD files.

which the fetch summarised as meaning a locally-defined block *could override library
versions unintentionally*. **This cuts both ways and both matter to us:** it is exactly
what lets an inline `0 FILE bikar-ClassicBrick-2x4.dat` block satisfy the type-1 line
that references it, and it is exactly why naming that block `3001.dat` would silently
replace the real 2×4 for every other part in the file.

S3's own worked example — reproduced in §7's structure — contains a block
(`sticker.ldr`) that carries `0 UNOFFICIAL PART`, `0 BFC CERTIFY CCW`, a type-1
reference to `box5.dat`, and a raw type-4 quad. **The official MPD spec's own example
therefore defines a part inline, with geometry, inside an MPD.** That is the strongest
grounding available for option B below.

Note S3's example uses the older `0 UNOFFICIAL PART` form rather than
`0 !LDRAW_ORG Unofficial_Part`. I did not find a statement reconciling the two forms
in any of S1–S7; §8 records it.

### 3.3 What each viewer does — and what I could not learn

**LDView** (S8, the shipped `Help.html`) is the one viewer whose resolution rule I
could quote. Search order, verbatim:

> the directory the model is located in, as well as the P, PARTS, and MODELS
> directories inside the LDraw directory (in that order). If it doesn't find the file
> in any of those directories, it will then search all the directories listed in the
> Extra Search Dirs.

and on a part it cannot find, verbatim:

> if LDView encounters a request for a part that it cannot find, it will attempt to
> download the part from the LDraw.org parts tracker

with S8 noting a warning is generated whenever an unofficially downloaded file is used.
S8 on MPD: LDView reads MPD files and offers a *"MPD Model Selection Dialog"* to select
sub-models, displaying a selected sub-model *"as if that model had been loaded directly
into LDView."*

**The model's own directory is searched first.** That is the fact that makes option C
(companion `.dat` beside the `.ldr`) work in LDView specifically.

**What I could not learn about LDView:** what it does *after* the parts-tracker
download fails for a name that does not exist there. S8 as fetched does not say.

**LeoCAD** (S10, S11). S10 verbatim: LeoCAD *"is completely compatible with LDraw's
parts library"*, *"can use either a zip file or a regular folder for its library"*, and
resolves an alternative library by, in priority order, the `-l` command-line option,
the `LEOCAD_LIB` environment variable, and the Preferences path. Unofficial parts: for
the default library, place `ldrawunf.zip` beside `library.bin` and restart; for a loose-
file custom library, *"place the files in the 'unofficial' folder."* S10 as fetched
**does not describe what LeoCAD does with a part it cannot locate**, and describes **no
search of the model's own directory**. S11 (LeoCAD's meta-command page) lists only
`0 !LEOCAD …` commands and does not mention `0 FILE`, `0 !LDRAW_ORG`, `0 Name:` or
`0 Author:`. LeoCAD's home page states it *"reads and writes LDR and MPD files"*, so
MPD is supported; **the inline-part-inside-MPD case is not documented on any LeoCAD page
I could reach.**

**BrickLink Studio** (S12). The import article lists `.io`, `.ldr`, `.mpd`, `.lxf`,
`.lxfml`, `.obj`/`.mtl`, `.stl`, image formats, BrickLink XML wanted lists and set
numbers. **It says nothing about parts it does not recognise**, and the PartDesigner
help category returned only navigation chrome. **Studio's behaviour on an unknown or
inline-defined part is UNGROUNDED here.** §8 gives the experiment.

**K2 — the bound on this survey.** Three viewers were checked and only one (LDView) has
documented resolution behaviour I could quote. I did not check LDCad, Bricksmith,
LPub3D, the browser-based LDraw model viewer at `library.ldraw.org/model-viewer`,
three.js `LDrawLoader`, or Blender's LDraw importers. Nothing below should be read as
"viewers do X" — only as *"of the three viewers checked here, one documents X and two
document nothing."*

### 3.4 The options, and what each costs

Costs marked **measured** were run at bikar 9cca1ae; see §5.4.

| # | Option | What the format permits | Cost | When it lies |
|---|---|---|---|---|
| **A** | Type-1 reference to the nearest stock part (`3001.dat` for a 2×4) | Fully permitted: it is an ordinary type-1 line with a library filename. No spec objection at all. | Tiny file — one line per brick, ~50 bytes. Renders in every viewer that has the library, with no extra files. | **Whenever the generated brick is not that part** — which is *most of the time*. See §3.5. Of the **7** brick scripts shipped in bikar's `patterns/Lego/`, **5** carry `relief depth` and/or `studs none`/`studs edge`, and no LDraw part exists with a pattern relief cut into it. Only `Classic-Brick` (2×4, `studs full`, no relief) and `Pin-Rail` (1×N, `studs full`, no relief) have a stock analogue at all — and even those differ dimensionally by §3.5's table. |
| **B** | MPD: `0 FILE <generated>.dat` block with the mesh as type-3 lines, referenced by type-1 from the main block | Permitted, and S3's own example does exactly this shape (`sticker.ldr` block with `0 UNOFFICIAL PART` + geometry). | **Measured: 217,206 bytes (212.1 KiB) of type-3 text for one plain 2×4** (3,764 triangles, 1,884 vertices, 4-decimal rounding, mean 57.7 bytes/line). Estimated at the same 57.7 B/line for the other shipped bricks: `Star-Brick` 1,300 tris ≈ 73 KiB, `Hex-Field-Tile` 12,148 tris ≈ 685 KiB, `Grid-Field-Tile` 12,844 tris ≈ 724 KiB. A 20-brick model of field tiles is therefore in the **10 MB** range. Also: the emitted "part" is a triangle soup with no LDraw primitives, so it is unreusable as a library contribution and will render slower than a real part. | It does not lie about geometry — this is the only option that is dimensionally honest. It *does* misrepresent itself if the block is named after a real part (S3: no scoping rules), and it claims a part identity the LDraw library has never issued (§3.1). |
| **C** | Placement-only: type-1 lines referencing a name the user must supply, plus a companion `<name>.dat` written beside the `.ldr` | Permitted — it is option A's line with a different filename. | Same tiny `.ldr`. But the model is **not self-contained**: it only renders where the companion file is found. Grounded for **LDView only**, whose documented search order puts *"the directory the model is located in"* first (S8). **Not documented for LeoCAD** (S10 describes a library zip/folder and an `unofficial` folder, no model-directory search) and **not documented for Studio**. In LDView, a missing companion additionally triggers a parts-tracker download attempt for a part number that does not exist (S8). | Does not lie; it *omits*. The failure is a model that renders correctly on the machine that generated it and not on the machine it was sent to — the worst failure mode of the three, because it is invisible to the author. |
| **D** | Emit nothing until the geometry question is settled — i.e. do not ship the export | — | Zero. | — |

### 3.5 Quantifying the lie in option A

Every number in this table is bikar's `patterns/Lego/Classic-Brick.bkr` (2×4, 3 plates,
`studs full`, `clutch auto`) against `3001.dat` as S13 read it. bikar values are from
`kernel3d/lego.ts` plus the shipped `DEFAULT_BRICK_FIT`, which the compile run confirms
is what a default `Classic-Brick` is built with (`studDiaMm -0.2, tubeDiaMm -0.2,
pinDiaMm -0.2, wallMm 0, ribMm 0.1, ribArcMm 0.8`, all provenance `default`).

| Feature | `3001.dat` as modelled (S13) | Generated brick | Δ |
|---|---|---|---|
| Footprint, 4-stud run | 80 LDU = 32.0 mm (nominal grid; S13: *"LDraw does not model this gap"*) | `8n − 0.2` = 31.8 mm — **measured** in the emitted lines as ±39.75 LDU, not ±40 | **0.1 mm per side** |
| Stud ⌀ | 12 LDU = 4.8 mm (`p/stud.dat`) | 4.8 − 0.2 = **4.6 mm** | 0.2 mm |
| Anti-stud tube ⌀ | 16 LDU = 6.4 mm (`p/stud4.dat`) | 6.514 − 0.2 = **6.314 mm** | 0.086 mm |
| Stud height | 4 LDU = 1.6 mm (`p/stud.dat`) | **1.6 mm** (`lego.ts:50` follows LDraw deliberately) | **0** |
| Brick height | 24 LDU = 9.6 mm | 9.6 mm | 0 |
| Clutch rib | no analogue — `stud4.dat` is a plain annulus | 0.1 mm radial lobes, 0.8 mm arc (`RIB_MM_CAL`, `RIB_ARC_MM`) | a **feature**, not a dimension |
| Pattern relief | none, on any stock part | up to 2.0 mm deep on 5 of the 7 shipped scripts | unrepresentable |

**Correction to a premise this research was given.** The brief said the doc uses a
1.7 mm stud height against LDraw's 1.6. It does not. §3.1's table gives **1.6**,
sourced to LDraw's `p/stud.dat`, and lists 1.7 as the *contested* value from Bartneck
and Brick Owl; `lego.ts:50` implements 1.6 with the comment *"We follow LDraw because
the rest of the geometry is authored against its primitives."* Stud height is one of
the few places where option A does **not** lie.

**When option A is honest, precisely.** When the brick is rectangular, `studs full`,
carries no relief, has a stock analogue at that footprint and height, and the
consumer's question is *"where does this sit on the grid"* rather than *"what shape is
it"*. Δ ≤ 0.2 mm on a diameter is below what any of the checked viewers renders
meaningfully at model scale. **When it lies:** any relief, any non-rectangular outline,
`studs none`/`studs edge`, any non-default fit, and any use of the file as a
dimensional record rather than a layout preview.

---

## 4. Scale — the non-8 mm pitch question

### 4.1 The premise needs correcting first

The brief asks what happens "if a generated brick is authored at a pitch that is not
8.0 mm (this project sweeps pitch — see §5.3)". **This project does not sweep the stud
pitch.** `STUD_PITCH_MM = 8.0` is a module constant in
`packages/core/src/kernel3d/lego.ts:34`, commented *"The one uncontested number in the
system"*, and it is not a knob: it is not in `BrickFit`, not in `FIT_FIELDS`, and not
reachable from `BrickFitOverride`. What §5.3 and S14 sweep is the **pattern's scale** —
the size of the decorative motif — *against a fixed 8 mm stud pitch*. S14's own method
note is explicit: *"Stud pitch: 8 mm (`STUD_PITCH_MM`)."*

So the question has two separate real answers.

### 4.2 Pattern scale: nothing to express

A pattern scale sweep changes the relief geometry cut into a brick whose lattice is
still 8 mm. In LDU that brick is still 20 LDU per stud and 24 LDU tall; only the
relief shape changes. **This costs the export nothing under option B** (the relief is
just more triangles) and it is **exactly what option A cannot represent at all** (§3.5's
last row).

### 4.3 If the pitch were ever made a knob

The format permits it, in two different senses, and neither is a good answer:

1. **Coordinates are floats, and the LDU is a unit, not a grid.** S1 defines the LDU as
   a length; nothing in S1 as fetched constrains a type-1 line's `x y z` to integers or
   to multiples of 20. A brick placed on a 7.5 mm pitch would emit at 18.75 LDU centres
   and every viewer would render it exactly where it was put. Nothing breaks; nothing is
   flagged; and the model is silently incompatible with every part in the library.
2. **The type-1 matrix scales.** S1: the 3×3 *"represents the rotation and scaling of
   the part."* So `1 16 0 0 0 0.9375 0 0 0 0.9375 0 0 0 0.9375 <part>.dat` places a
   part at 15/16 scale, legally. But a uniform scale shrinks the **studs and tubes too**,
   so the result mates with nothing — and a non-uniform scale that preserved the studs
   while changing the pitch is not expressible at all, because pitch is a property of
   *where the studs are inside the part*, not of the part's placement.

**I did not find any meta command in S1, S2, S3, S4 or S7 that declares a file's units
or a global scale factor.** I did not read every LDraw language extension — S1's link
list alone names a dozen more — so this is *"none of the five specifications read here
defines one"*, not *"LDraw has none"*.

**The honest answer, stated plainly:** the `.ldr` export is only meaningful at true
scale. There is no way to say "this model is on a 7.5 mm pitch" in a `.ldr` file such
that a reader would understand it; the format's whole premise is a single fixed unit.
If a pitch knob is ever added, **the emitter must refuse to export** rather than emit
a file that reads as a normal LDraw model and is not one. Since `STUD_PITCH_MM` is
presently a constant, that refusal is a guard against a future change, not a live case.

---

## 5. What bikar actually holds — verified, not assumed

The export can only emit what the data structures carry. Read at
`bikar-lego-lab`, branch `main`, commit `9cca1ae`.

### 5.1 The assembly

`AssemblyProvenance` (`packages/core/dist/index.d.ts:5947`) carries `name`, `root`,
`parts: readonly PlacedPart[]`, `closures`, `exportParts`, `warnings`.

`PlacedPart` (`:5915`) carries `piece: string`, `xform: RigidXform`, `mesh: OrbMesh`
(**piece-local** — the doc comment says *"`xform` carries piece-local into assembly
world, while `mesh` stays piece-local"*), `piece3d: PieceProvenance`, and an optional
`featureFloorMm`.

`RigidXform` (`:1804`) is `{ r0, r1, r2, t }` — three `Vec3` **rows** of a rotation
matrix plus a translation, confirmed by `frame.ts:122`:
`applyXform(x, p) = (dot3(x.r0,p)+x.t.x, dot3(x.r1,p)+x.t.y, dot3(x.r2,p)+x.t.z)`.
Translations are millimetres.

`AssemblyDeclarationNode` (`:4180`) has `places: readonly string[]` — **a place carries
no coordinates**. Every position in an assembly comes from solving the `connect`
statements, and the root part lands at identity. So there is nothing to read but
`PlacedPart.xform`, and that is sufficient.

**Everything a type-1 line needs is present**: a name (`piece`), a rotation and a
translation in millimetres (`xform`), and a height (`piece3d.brick3d.heightMm`, via
`BrickProvenance`) to apply the §1.4 origin convention. **Nothing more is needed for
option A or C.** For option B the mesh is also present, piece-local, which is the right
frame: option B's inline part block wants piece-local geometry and the type-1 line
carries the pose.

### 5.2 The type-1 line, derived

With `C` from §1.4 and `R` the rotation whose rows are `r0, r1, r2`, the matrix a
type-1 line needs is `M = C R Cᵀ` (C is orthogonal, so `C⁻¹ = Cᵀ`). Expanding:

```
             a  b  c        r00  −r02   r01
  M  =       d  e  f   =   −r20   r22  −r21
             g  h  i        r10  −r12   r11
```

and, because the emitted part's local origin sits `d = (0, H/0.4, 0)` LDU from the
bikar-local origin (§1.4), the translation is

```
  (x, y, z)_LDU = ( t.x/0.4 , −t.z/0.4 , t.y/0.4 )  −  M · (0, H/0.4, 0)
```

For an identity rotation this collapses to `M = I` and
`(x, y, z) = ( t.x/0.4 , −(t.z + H)/0.4 , t.y/0.4 )`, which is what §7 uses.

**Sanity check against a real solve.** `patterns/Assemblies/Brick-Stack.bkr` compiles
to two parts: `Base` at `r = I, t = (0, 0, 0)` and `Cap` at `r = I, t = (0, 0, 9.6)`,
with `heightMm = 9.6` on both (measured — §5.4). The formula gives `(0, −24, 0)` and
`(0, −48, 0)`. Those are 24 LDU apart, one brick height, with the lower brick's bottom
face at `Y = 0` — and 24-LDU stacking is exactly the shape of S3's own example, whose
`house.ldr` places bricks at `y = 0, −24, −48`.

### 5.3 BFC — the mesh already satisfies the precondition

`OrbMeshStats` (`:1693`) documents `volumeMm3` as *"Signed enclosed volume; positive
when winding is outward"* and `watertight` as *"True iff every directed edge appears
exactly once with exactly one twin."* For `Classic-Brick` the compile reports
`{"euler":2,"genus":0,"volumeMm3":3986.06,"watertight":true}` — **measured**. So the
mesh is closed, genus 0, and consistently wound outward.

Consistently-outward winding in a right-handed frame means each triangle reads
counter-clockwise viewed from outside; §1.4's map has `det +1` and therefore preserves
that. So `0 BFC CERTIFY CCW` is *derivable* for option B's inline block.

**Hedge, and it is load-bearing: I did not render the output in a BFC-checking viewer.**
The chain above is an argument from two documented mesh statistics and a determinant,
not an observation. S7 makes the safe fallback explicit — omit the BFC line and
*"0 BFC NOCERTIFY is assumed and BFC processing will be disabled for the file"* — which
costs shading quality, not correctness. **Emit no BFC line until someone has actually
looked at the render.**

### 5.4 Reproducing the measurements in this file

Against `bikar-lego-lab` at `9cca1ae`, with
`export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"`:

```
node packages/cli/dist/index.js render patterns/Assemblies/Brick-Stack.bkr \
     --format parts -o /tmp/bs
     # -> Stack-Base.stl and Stack-Cap.stl, 3764 triangles / 184 KiB each
```

The triangle counts, mesh stats, fit set, and the `PlacedPart.xform` values were read
by importing `packages/core/dist/index.js` and calling `compileToGeometry(source, {})`:
`result.assembly3d.parts[i].xform` for the poses, `result.orbMesh.triangles.length` and
`result.orbMesh.stats` for a single `brick`, `result.brick3d.fit` for the fit set. The
212.1 KiB figure is the byte length of the joined type-3 lines produced by applying
§1.4's map to `Classic-Brick`'s mesh with coordinates rounded to 4 decimals.

Triangle counts, all measured: `Classic-Brick` 3,764 · `Star-Brick` 1,300 ·
`Hex-Field-Tile` 12,148 · `Grid-Field-Tile` 12,844.

---

## 6. Recommendation

**Ship option B — an MPD with one inline `0 FILE …dat` block per distinct generated
brick — and ship it as `.ldr`'s honest sibling rather than as `.ldr`.** Do not ship
option A as the default. Do not ship option C at all.

The reasoning, in the order that decides it:

1. **Option A is a claim about identity that is false for 5 of the 7 shipped scripts,
   and the failure is silent.** A user who exports a `Star-Brick` field and gets
   `3001.dat` lines back has a file that renders as plain grey 2×4s. Nothing warns
   them. That is the same defect class as C2's dropped multipart objects: an export
   that succeeds and produces the wrong thing. The Lab already refuses to let an
   unmeasured fit value read as measured (D-005); letting a generated brick read as a
   LEGO part number is the same category of misrepresentation, one layer up.
2. **Option B is the only option that is dimensionally honest**, and honesty is the
   whole reason this project models a 0.857 mm tube wall and a 0.1 mm rib rather than
   copying LDraw's 6.4.
3. **Option C's failure mode is the worst available**: correct on the author's machine,
   broken on the recipient's, and grounded in exactly one of the three viewers checked.
4. **The cost of B is bytes, and bytes are the cheap axis here.** 212 KiB for a plain
   2×4 is large for a text file and small for a 3D asset — it is *larger* than the
   184 KiB binary STL of the same mesh, which is the useful comparison, since a user
   who wanted the mesh already has `--format stl`.

Two conditions on shipping it, both of which follow from §§1–3 rather than from taste:

- **Name the inline block outside every namespace S6 defines** — letters and hyphens,
  never `NNNN` / `uNNNN` / `tNNNN` — because S3 states there are *"no clear scoping or
  namespace rules on MPD files"* and a block named `3001.dat` would replace the real
  2×4 for the whole document.
- **State in the file, in a `0 //` comment, that the part is generated and is not an
  LDraw part.** This costs one line and it is the only place the fact can live.

**Deliberately not recommended, and why it is worth revisiting later:** an *option A/B
hybrid* that emits a stock reference when the brick provably matches a stock part
within a stated tolerance and inline geometry otherwise. It is the best answer in
principle. It needs a stock-part match table (footprint × height × stud mode → part
number) that this research did not build and that would have to be maintained against
library updates, and it needs a tolerance that only a rendered comparison can set. It
should be a follow-on, not a precondition — and if it is built, the tolerance is the
number to argue about, because §3.5 shows the deltas are all in the 0.086–0.2 mm band
where "close enough for a layout preview" and "wrong as a dimensional record" are the
same number.

**What this recommendation does not settle:** whether P3 should ship the export at all.
That is a scope call, not a research finding. What §§3–5 establish is that *if* it
ships, B is the shape it should take, and that the "one line per piece, no mesh work"
framing in the §10 P3 row and in S13 §6 is **only true for options A and C** — the two
options this research recommends against. **Option B is a mesh emit.** The P3 row's
cost estimate should be corrected before the phase is planned.

---

## 7. Worked example — two stacked 2×4 bricks, every field labelled

Real data: `patterns/Assemblies/Brick-Stack.bkr` compiled at bikar `9cca1ae`, whose two
parts solve to `Base` at `r = I, t = (0,0,0)` mm and `Cap` at `r = I, t = (0,0,9.6)` mm,
each 3,764 triangles, `heightMm = 9.6`.

### 7.1 Option B — the recommended MPD

```ldraw
0 FILE Stack.ldr
0 Brick-Stack — 2 x 4 x 2, generated by bikar
0 Name: Stack.ldr
0 Author: bikar (3d-models Lego Lab)
0 !LDRAW_ORG Unofficial_Model
0 // Generated from patterns/Assemblies/Brick-Stack.bkr. The parts below are
0 // NOT LDraw library parts and have no LDraw part number. Dimensions differ
0 // from the nearest stock elements; see docs/lego-lab-design.md 3.1 / 3.2.
1 4 0 -24 0 1 0 0 0 1 0 0 0 1 bikar-Base-2x4-3p.dat
1 7 0 -48 0 1 0 0 0 1 0 0 0 1 bikar-Cap-2x4-3p.dat
0 NOFILE

0 FILE bikar-Base-2x4-3p.dat
0 Brick 2 x 4 (generated, not a LEGO element)
0 Name: bikar-Base-2x4-3p.dat
0 Author: bikar (3d-models Lego Lab)
0 !LDRAW_ORG Unofficial_Part
0 // 3764 triangles. Stud pitch 20 LDU = 8.0 mm. Body 39.5 x 79.5 x 24 LDU
0 // (8n - 0.2 mm footprint), stud dia 11.5 LDU, tube outer dia 15.785 LDU,
0 // plus 0.1 mm clutch ribs that no stock part carries.
3 16 -19.75 24 -39.75 19.75 24 -39.75 19.75 16 -39.75
3 16 -19.75 24 -39.75 19.75 16 -39.75 -19.75 16 -39.75
3 16 19.75 24 -39.75 19.75 24 39.75 19.75 16 39.75
0 // ... 3760 further type-3 lines, 217206 bytes in total ...
3 16 15.6395 -4 28.8782 15.3123 -4 27.7996 15.5024 -4 28.3309
0 NOFILE

0 FILE bikar-Cap-2x4-3p.dat
0 Brick 2 x 4 (generated, not a LEGO element)
0 Name: bikar-Cap-2x4-3p.dat
0 Author: bikar (3d-models Lego Lab)
0 !LDRAW_ORG Unofficial_Part
3 16 -19.75 24 -39.75 19.75 24 -39.75 19.75 16 -39.75
0 // ... 3763 further type-3 lines ...
0 NOFILE
```

The four type-3 lines shown are the real first three and real last line of
`Classic-Brick`'s mesh under §1.4's map (§5.4). `Base` and `Cap` are the same geometry
here; a real emitter should de-duplicate identical bricks into one block and reference
it twice, which halves this file.

### 7.2 The placement line, field by field

Taking the `Cap` line:

```
1      4       0    -48   0     1 0 0   0 1 0   0 0 1     bikar-Cap-2x4-3p.dat
│      │       │     │    │     └───────┬─────────┘       └──────┬────────────┘
│      │       │     │    │             │                        │
│      │       │     │    │             │                        └─ <file>: the sub-file.
│      │       │     │    │             │                           Resolved against the MPD's
│      │       │     │    │             │                           own 0 FILE blocks first
│      │       │     │    │             │                           (S3: no scoping rules), then
│      │       │     │    │             │                           by the viewer's search path.
│      │       │     │    │             │
│      │       │     │    │             └─ a b c d e f g h i: row-major 3x3.
│      │       │     │    │                a=1 b=0 c=0 / d=0 e=1 f=0 / g=0 h=0 i=1.
│      │       │     │    │                Identity, because bikar's xform for Cap is
│      │       │     │    │                r0=(1,0,0) r1=(0,1,0) r2=(0,0,1) and
│      │       │     │    │                M = C R C^T = I  (5.2).
│      │       │     │    │
│      │       │     │    └─ z = t.y / 0.4 = 0 / 0.4 = 0 LDU
│      │       │     │
│      │       │     └─ y = -(t.z + H)/0.4 = -(9.6 + 9.6)/0.4 = -48 LDU.
│      │       │        Negative because -Y is up (S1). 24 LDU per brick.
│      │       │
│      │       └─ x = t.x / 0.4 = 0 LDU
│      │
│      └─ <colour>: a concrete code, because a top-level type-1 line has no
│         referencing line for colour 16 to inherit from (S1). Geometry inside
│         the referenced block is written in 16 so it takes this code.
│         (Which code renders as which colour is defined in LDConfig.ldr,
│         which I did not fetch — see 8.)
│
└─ line type 1: sub-file reference.
```

`Base`'s line is `1 4 0 -24 0 1 0 0 0 1 0 0 0 1 bikar-Base-2x4-3p.dat` by the same
arithmetic with `t.z = 0`. The lower brick's bottom face therefore sits at `Y = 0` and
the upper brick's top face at `Y = −48`.

### 7.3 Option A, for comparison — the same two lines, and the lie

```ldraw
1 4 0 -24 0 1 0 0 0 1 0 0 0 1 3001.dat
1 7 0 -48 0 1 0 0 0 1 0 0 0 1 3001.dat
```

**The placement arithmetic is identical** — that is a real and useful property, and it
comes from §1.4's origin convention matching the one S13 read off `3001.dat`. The whole
difference between options A and B is which filename the type-1 line names. What
changes is that this two-line file asserts these are LEGO 2×4 bricks, when they are
0.2 mm narrower per run, carry 4.6 mm studs against 4.8, carry 6.314 mm tubes against
6.4, and carry clutch ribs that no LEGO element has (§3.5).

---

## 8. What could not be grounded

Each item states what would settle it.

1. **UNGROUNDED — empirical. What LeoCAD does with a type-1 line naming a part it
   cannot find, and whether it resolves a name against `0 FILE` blocks in the same
   MPD.** S10 documents the library search (zip or folder, `unofficial` subfolder) and
   documents no model-directory search; S11 lists only `0 !LEOCAD` metas. *Experiment:*
   open §7.1's MPD in LeoCAD; then open a variant whose type-1 line names a nonexistent
   `.dat` with no matching block. Record: renders / renders with placeholder / warns /
   drops the part silently / refuses the file.

2. **UNGROUNDED — empirical. What BrickLink Studio does with an inline-defined part in
   an imported `.mpd`, and with an unresolvable reference.** S12 confirms `.ldr`/`.mpd`
   import and says nothing about unknown parts; the PartDesigner help category returned
   no article text. *Experiment:* the same two files, imported into Studio. Studio maps
   LDraw parts onto its own catalogue, so the failure mode may differ in kind from a
   viewer's — record whether the inline part survives import at all, and whether a
   round-trip export back to `.ldr` preserves it.

3. **UNGROUNDED — empirical. What LDView does after its parts-tracker download attempt
   fails.** S8 documents the attempt (*"it will attempt to download the part from the
   LDraw.org parts tracker"*) but not the outcome for a name the tracker has never had.
   *Experiment:* open a model referencing `bikar-nonexistent.dat` with no companion file
   and no network, and with network. Record the message and whether the rest of the
   model still renders.

4. **UNGROUNDED — no source found. Whether `0 UNOFFICIAL PART` (used in S3's own
   example) and `0 !LDRAW_ORG Unofficial_Part` (S2) are interchangeable, and which a
   viewer prefers.** None of S1–S7 reconciles them. §7.1 writes the S2 form on the
   reasoning that S2 is the current header specification and S3's example may predate
   it — **that is an inference, not a sourced claim.** *Settled by:* the LDraw
   Standards Board's revision history for S2, or by testing both forms in a viewer that
   reports part status.

5. **UNGROUNDED — not fetched. The numeric colour code → colour name mapping.** It
   lives in `LDConfig.ldr`; S13 records that the library ships `LDConfig.ldr`,
   `LDCfgalt.ldr` and `LDConfig_TLG.ldr`, but I did not read any of them. Codes `4` and
   `7` in §7 are used only because S3's official example uses them; **no claim is made
   about what colour they render as.**

6. **Not re-verified. Every `.dat` file dimension in §3.5.** All are quoted from S13's
   first-hand reading of the downloaded library zip on 2026-07-29. Per-file web paths
   404 (§0), so I could not independently check a single one. If the export's fidelity
   claims ever become load-bearing, the library should be re-downloaded and the four
   rows re-read.

7. **Bounded, not exhaustive: the viewer survey.** Three viewers were checked (LDView,
   LeoCAD, Studio) and only LDView's resolution behaviour is documented in a source I
   could quote. Not checked: LDCad, Bricksmith, LPub3D, `library.ldraw.org/model-viewer`,
   three.js `LDrawLoader`, Blender LDraw importers. **No statement in this file should
   be read as "LDraw viewers do X".**

8. **Bounded, not exhaustive: the specification survey.** Seven LDraw specification
   documents were read (S1–S7). S1's own link list names roughly a dozen further
   language extensions (TEXMAP, CATEGORY/KEYWORDS, and others) that were not read. §4.3's
   "no units or global-scale meta command" claim is bounded to S1–S7 and is stated that
   way there.

9. **Untested. The BFC derivation in §5.3.** The argument that outward winding plus a
   `det +1` axis map yields `0 BFC CERTIFY CCW` is sound on paper and has not been
   rendered. §5.3 recommends omitting the BFC line until it has been, on S7's grounds
   that absence is safe.

10. **Estimated, not measured: three of the four file-size figures.** Only
    `Classic-Brick`'s 217,206 bytes was measured directly. `Star-Brick`,
    `Hex-Field-Tile` and `Grid-Field-Tile` were measured for *triangle count* and their
    byte figures extrapolated at 57.7 bytes/line, which will be wrong wherever
    coordinate magnitudes or decimal places differ. They are order-of-magnitude figures
    and §3.4 labels them as estimates.
