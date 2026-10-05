---
status: idea
started: 2026-10-05
asked_by: Omar
---

# Finish techniques: split the pieces too, and every other way to a better-looking print

**Status: brainstorm.** Nothing here is decided or built. Started on 2026-10-05 when Omar asked,
after the split coaster plates: "can we think of techniques of splitting the infill to and
reassemble in a qualitative fashion so their outward facing sides are first layer on glacier
plate... we should have all these techniques ina brainstorm high quality printing
enhancement/techniques".

**In short.** The split coaster ([split-01](../plates/split-01.md), [split-02](../plates/split-02.md))
already prints both of its outer faces on the bed. Its pieces do not: a whole piece prints one face
down, so one face is a first layer and the other is the last layer, two different finishes on the
same coaster. Cut each piece in two as well, print both halves face down, and every face you can
see is a first layer. Section 1 has five ways to do it. My pick is to start with the lip and a cut
piece (way **a**): it is the smallest change to split-01, it needs no glue, and it lets each face of
the coaster be its own color. Section 3 is the wider list of finish techniques, each marked with
whether we have tried it.

## 1. Split the pieces too

![Four cut-through side views. 1: today, one whole piece, its lower face a first layer and its upper face a top surface. 2: the lip with the piece cut in two, both faces first layers. 3: the flange with the piece cut in two, the band hanging past the face block. 4: the flange printed in place, each coaster half printed with its piece halves already inside, then closed.](finish-techniques-media/split-pieces.png)

The picture is drawn from [split-pieces.html](finish-techniques-media/split-pieces.html), rendered
headless, and is not to scale.

**Why it matters.** The bed gives a face its finish: the plate's texture or smoothness, pressed in.
The last layer gets the nozzle's lines instead, and on the minis it is where the pinholes showed
([print quality §2](print-quality-design.md#2-tiny-holes)). On a split coaster the straps on both
faces are first layers, so a piece whose upper face is a top surface is the one part that looks
different. Cut the piece at the same height as the coaster and that difference goes away.

### 1.1 Five ways

| Way | How it holds | Pros | Cons | What it commits us to |
|---|---|---|---|---|
| **a. Lip + cut piece** (picture 2) | Each piece half drops into its own coaster half. When the halves close, the two lips trap both halves, as they trap a whole piece today. | The smallest change to split-01: the piece is cut at the coaster's cut, nothing else moves. Plain blocks, so no overhang. No glue. Each face can be its own color, which gives a coaster that is two coasters, one on each side. | Twice as many parts to place, and a kite half is small (1.6 mm thick). The stars still have no lip (bikar refuses one that closes up their arms), so they stay open holes, as on split-01. The piece face still sits 0.6 mm in from the coaster face, under the lip. | One new bikar knob on `hold lip` to cut the pieces. The plates get twice the piece count, so packing and time change. |
| **b. Flange + cut piece** (picture 3) | Each half is a face block plus half the band. The halves close on the bands in the undercut, as with split-02. | Pieces sit flush with the coaster face, and the stars are held too. No glue. | Printed face down, the band hangs 0.8 mm past its face block: a short overhang with nothing under it. It is hidden inside the coaster, but a drooped band may not close cleanly. | The same knob on `hold flange`. Whether the overhang closes is a coupon question. |
| **c. Flange, printed in place** (picture 4) | Each coaster half prints with its piece halves already inside it, the band caught under the face. Turn one half over onto the other and the coaster is done. | No pieces to place at all, and they cannot be lost. Every face is a first layer. Fastest to put together. | The band must not touch the coaster where it is printed, so it needs a layer of air under it, and the band's underside droops into that air. Whether one 0.2 mm layer keeps them apart is unknown. One color per coaster half, unless the plate swaps filament, which costs time and waste (phones-01 took about 62 minutes against 22 sliced, [phones-02](../plates/phones-02.md)). | A print-in-place mode in bikar: the piece halves placed in their holes with a set gap, not packed beside the coaster. The color of each piece is then fixed by the plate, not by hand. |
| **d. Pegged halves** | The two halves of each piece are joined by a small peg and socket, with no help from the coaster. | Works in a one-piece coaster too (sheets-04g's loose frame), not only a split one. | A peg needs room. The split design's studs are 2 mm across ([split §4.1](../pieces/split-with-studs-design.md#41-the-stud-and-socket)), and a kite's half is narrow near its tips. A press fit is the kind of fit that went wrong on sheets-04g (kites too tight, middle too loose). | A peg fit to calibrate, one per piece shape, as today's press fit needed. |
| **e. Glued halves** | Two halves glued face to face into one solid piece. | Any frame, any piece, nothing to design. | Glue on every piece, a seam on the side of every piece, and pieces fixed for good. Whether to glue at all is still the split design's call 3. | It hangs on call 3. |

**My pick: a first, then c.** **a** changes one thing on a plate we already have, so a print of it
answers one question: does a cut piece look and hold like a whole one? **c** is the bigger win
(nothing to place), but it adds a print-in-place mode and an air gap nobody has measured, so it
comes after **a** has shown that cut pieces are worth it.

### 1.2 True of every way

- **Turn the upper half over; never mirror it.** Turning the half over keeps its outline as it is,
  but a mirrored copy of a lopsided piece will not fit its hole. The tool that draws the plates
  already turns parts over (`build/brick_previews.py`).
- **Each half is half as thick.** At gBV's 3.2 mm piece, a half is 1.6 mm, eight 0.2 mm layers. A
  thin small half is easy to lose and may lift off the bed at its tips.
- **The edge flare moves to both faces.** The first layer spreads a little past its outline
  (elephant's foot). Today one face of each piece has it; cut in two, both do. The X2D preset
  corrects by 0.15 mm, and Bambu says that value changes from plate to plate
  ([split §1](../pieces/split-with-studs-design.md#1-what-glossy-means-here-plate-by-plate)).
- **More first layers, more time.** First layers print slowly, and a cut piece has two. The slicer
  will say how much; nothing here has measured it.
- **The seam is out of sight.** The cut between two piece halves is at the coaster's own cut,
  inside, so neither face shows it.

### 1.3 How it would be tried

A coupon, not a coaster: three pieces of each shape (kite, hex, middle), whole and cut, in one
split-01 coaster's halves. It answers three things: do the cut halves sit level under the lip, does
the coaster still close, and do the cut faces look like the straps around them. Nothing is built
for it yet; it needs the bikar knob in **a** first.

## 2. The glacier plate

Omar named a glacier plate. It is not in our notes yet: the plate table in
[split §1](../pieces/split-with-studs-design.md#1-what-glossy-means-here-plate-by-plate) lists
Bambu's Textured PEI, Smooth PEI, Cool Plate SuperTack, Engineering and Dual-Texture plates, and no
glacier. Before a slice for it:

- **Which plate it is**: a Bambu one under another name, or another maker's. The name says nothing
  about the finish it presses into a face, and only a print shows that.
- **Which plate type the slicer should use for it.** The slice sets the bed temperature, and on the
  X2D a first-layer offset, by plate type, and the send refuses a slice made for a different plate
  ([sliced for the wrong plate](../../issues/sliced-for-wrong-plate.md)). Our slice takes
  `cool_plate`, `eng_plate`, `hot_plate`, `textured_plate` or `supertack_plate`.
- **The edge flare, measured again on it**, since Bambu says the correction changes with the plate.

## 3. Other techniques, a brainstorm list

Each line gives what it should improve and where it stands here. "Not checked here" means we have
not read it in the slicer version we run or printed it.

### 3.1 The faces (the first layer)

- **Every visible face on the bed.** Done for the split coaster's straps (both halves face down).
  Section 1 does it for the pieces.
- **Pick the plate for the face.** Textured PEI gives a grain. Smooth PEI is matte. SuperTack and
  the Engineering plate come closest to gloss
  ([split §1](../pieces/split-with-studs-design.md#1-what-glossy-means-here-plate-by-plate)).
  Gloss has to be judged on a print, not looked up.
- **A cooler bed for less edge flare.** Bambu says SuperTack's lower bed temperature "helps
  effectively reduce ... 'elephant foot'". The print-quality plan lists a 45 °C bed and a thinner
  first line as one fix for holes on the underside
  ([print quality §2](print-quality-design.md#2-tiny-holes)). Not tried.
- **A small chamfer on the face edge.** Cutting the bottom edge back a little in the model hides the
  flare instead of correcting it. A common trick. Not tried, and it changes the look of every edge.
- **Clean the plate before a face print.** Grease shows on a first layer. A habit, not a setting.

### 3.2 The top surface (when a face has to be one)

- **Ironing.** A second, very light pass that smooths the top. Off here: a Bambu forum thread traced
  pinholes to ironing ([print quality §2](print-quality-design.md#2-tiny-holes)). Worth one
  coupon on a part with no fine holes.
- **The top line pattern.** Bambu Studio offers several, monotonic and concentric among them. The
  preset fix found a zig-zag top had been in use by mistake ([print quality §1](print-quality-design.md#1-the-short-answer)).
  Not checked here which one reads best on a coaster.
- **More top layers.** A thicker top skin closes pinholes. It costs a little time.
- **Thinner layers near the top.** Variable layer height smooths a curved top, such as a `peak`
  piece. Not tried.

### 3.3 The walls and edges

- **Get the preset right first.** minis-01 to minis-06 printed on fallback settings, because our
  slicer passed only the last preset file in the chain; fixed since
  ([print quality §1](print-quality-design.md#1-the-short-answer)). Every other line on this list
  assumes that fix.
- **Where the seam goes.** Each wall loop starts and ends somewhere, and that spot shows. It can be
  put at the back, lined up, or blended along a slope (a scarf seam). Not checked here.
- **The wall generator.** The print-quality plan puts the holes in 2 mm straps and sharp star
  points down to the slicer's own gaps under Arachne walls
  ([print quality §2](print-quality-design.md#2-tiny-holes)). Wider straps or the classic
  walls are the two levers there.
- **True edges.** The kernel now draws coaster edges as true curves, not short straight steps
  ([smooth lines](../coaster/smooth-lines-design.md)).
- **A textured side (fuzzy skin).** A deliberately rough outer wall hides layer lines on the sides.
  A look call, not a fix. Not tried.

### 3.4 The fit (a good finish is also pieces that sit right)

- **One fit, not one per shape.** The lip holds the piece, so the gap only has to let it drop in
  ([split §11.1](../pieces/split-with-studs-design.md#111-why-this-is-easier-than-a-press-fit)).
  On sheets-04g the kites wanted a different gap from the middle.
- **Edge flare and fit.** The flare widens a part where it touches the bed, so a part that mates
  there fits tighter. The plan found it uncorrected on the minis
  ([print quality §3](print-quality-design.md#3-pegs-too-tight)).

### 3.5 Color

- **One color per plate.** Each filament swap cost about 1.6 minutes and some filament on
  phones-01. The one-color phones-02 printed in about 13 to 14 minutes against its 12 sliced
  ([phones-02](../plates/phones-02.md)).
- **A different color on each face.** This becomes possible once the pieces are cut (way **a**):
  the lower halves in one color and the upper halves in another, each color on its own plate.
- **The filament's own finish.** Silk, matte, sparkle and translucent each change the look more than
  most settings do. The color-themes skill already draws them.

### 3.6 After the print

- **Light sanding of a top surface**, for a face that could not go on the bed. It costs hand time
  on every coaster.
- **A clear coat.** Seals the surface and can add gloss. Whether it suits a coaster that meets hot
  mugs and wet glasses is not checked here.

## 4. What to try first

By what each tells us per unit of work:

1. **Find out which plate the glacier plate is**, and its slicer plate type. It costs nothing and
   decides every slice after it.
2. **Way a as a coupon** (§1.3): one bikar knob, three pieces per shape, on one split-01.
3. **A top-pattern and ironing coupon** on a solid piece. It costs nothing in design and covers
   every face that has to be a top surface.
4. **Way c**, once **a** shows that cut pieces are worth it.

## 5. Open for Omar

- **Which plate is the glacier plate?** (§2)
- **Start with way a?** Or go straight to c, or only keep this as a list for now.
