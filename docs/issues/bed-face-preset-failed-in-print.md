---
date: 2026-10-11
---

# The bed-face preset: clean in the slicer's plan, no cleaner in print

**2026-10-11.** [bedface-1](../design/plates/bedface-1.md) printed
[sheets-04g-fit2](../design/plates/sheets-04g-fit2.md)'s pieces again on the house bed-face preset,
[`tools/bambu/presets/bed-face-0.20.json`](../../tools/bambu/presets/bed-face-0.20.json): rings on
the first layer instead of diagonal lines, the fill pushed 30% into the wall, and a 0.42 mm first
line instead of 0.5. The [bed-face design](../design/printing/bed-face-slicing-design.md) proposed it
to close the slits Omar asked about on 2026-10-10 ("why do i get gaps like this in the plate
touching side"). The record is [2026-10-11-bedface-1](../prints/2026-10-11-bedface-1/index.md).

## What was tried

The design sliced five pieces with and without the preset and drew each first layer from the
G-code. In that plan the gBV coaster's bare share fell from 0.88% to 0.21%, and on bedface-1's own
slice from 1.10% (fit2, stock) to 0.26%. The design's check (§6) passed it. The design also said,
in §6 and §7, that the plan is not the print: covered in the plan is not proof of covered in the
print, and the narrower first line squashes less. So one plate went to the printer before any other
plate took the preset.

## What the print showed

- **The coaster's bottom was no cleaner.** Omar, beside fit2's stock coaster: "About the same", then
  "F as a coaster has more slits", and with a photo, "F has a lot of slits ..". The photo shows the
  strap edges closed, as the plan said, and short dark dashes and small triangles down the middle of
  the straps and where straps meet: where the rings from the two sides come together. The design
  drew those spots (§3.3, "a thin row of specks down the middle of some straps") and counted them as
  small. In print they are what you see.
- **The kites' core filled.** "f's kites don't have dents". The 0.42 mm line did the one thing only
  it could do.
- **Every fit came out tighter**, by about one 0.025 mm rung: the middle piece's winner moved from
  0.025 (fit2's `4GH 1C`) to 0.05 (`FC1 1E`), and the 0.05 kites went from tough to "too tight".
  The design expected the fit to stay put (§4). Coasters already move about one rung from print to
  print ([fit2's record](../prints/2026-10-10-sheets-04g-fit2/index.md)), so this one plate cannot
  say how much of the shift is the preset.

## Why the approach changes

The approach was "slice, draw the plan, score the bare bed, print the setting that scores best".
The print shows the score ranked the wrong way on the thing Omar sees: the plan scored the house
coaster three quarters less bare, and it came out the same or worse. So the plan's bare share is
not a stand-in for the bottom in the hand, at least for rings, and a setting is no longer picked on
it alone. Three suspects, none separated by this plate:

1. **Where rings meet.** The plan's drawing at the planned line width shows the meeting line as a
   speck or nothing. A likely reading, not measured: in print the bead is narrower or flatter than
   the drawing, and the meeting line opens up.
2. **Less squash from the narrower line.** 0.42 mm is squashed less than 0.5, so a gap the plan
   leaves is not pressed closed (design §7).
3. **The glacier plate.** Sliced as Smooth PEI, it gets no extra 0.02 mm push on the first layer
   that the Textured PEI plate gets (design §3.4).

## What replaced it

Nothing yet. Every plate stays on the X2D 0.20 mm Standard preset, which the design's §5.3 already
made the default until a print said otherwise; now a print has said so. The preset file stays in
the repo as the record of what was tried. The next step is Omar's call, from these:

| Option | What it verifies | Pros | Cons | Implications |
|---|---|---|---|---|
| **A split plate at the stock line width: half stock, half rings and overlap** (recommended) | Whether rings close their meeting lines when squashed like stock (0.5 line), against stock on the same bed | Bambu takes the rings and the overlap per piece (design §5.2), so one plate separates suspect 2 from suspect 1; the fit moves only by the overlap, not the line | Cannot fix the kites' core (that needs the 0.42 line, plate-wide); one more print | If the ring half is cleaner, rings come back without the 0.42 line and the kites get their own fix; if not, rings are dropped for good |
| **bedface-1 again on the gold Textured PEI plate** | Whether the extra 0.02 mm squash closes the meeting lines (suspect 3) | Same recipe, so it reads straight against this plate | Mixes the plate into every fit we judged on the glacier; tests one suspect | A yes would tie the preset to the gold plate |
| **Fix the plan first: score the meeting lines as bare**, then print what it ranks best | Nothing in print until the next plate; it makes the drawing agree with this photo | No print; every later setting is ranked on a check that has been held against a print | Fitting the check to one photo is a bet on one print | The simulator's "best" column is re-run; its §9 table may change |
| **Stop: stay on stock** | Nothing | No more prints on this; fits stay as judged | The slits Omar asked about stay; the kites keep their dent | The bed-face design closes as not fixed |

**2026-10-11: A was picked** ("go A"). The plate is [bedface-2](../design/plates/bedface-2.md): two
gBV coasters on one bed at the stock 0.5 mm first line, `S` on stock and `R` with rings and the 30%
overlap on that coaster alone, through a new `object_settings:` block in the plate recipe. In the
slicer's plan `R` is 0.41% bare against `S`'s 0.93%; the print decides. Every plate stays on stock
until it does.

## 2026-10-12: bedface-2, rings move the slits, they do not close them

bedface-2 printed (twice, from one slice), and Omar judged one pair by hand: `R` against `S`,
"About the same", then "both have slits, byt in different places". His photos show where. On the
stock coaster `S` the slits run along the strap edges, where the diagonal fill turns short of the
wall. On the ring coaster `R` the edges are closed, and the specks and small triangles sit down the
strap middles and where straps meet, the same places bedface-1's `F` had them. The record is
[2026-10-12-bedface-2](../prints/2026-10-12-bedface-2/index.md).

**What it settles.** Both coasters were squashed alike, at the stock 0.5 mm first line, so the
narrower line (suspect 2) did not make bedface-1's dashes: where the rings meet (suspect 1) did. As
the plate page set out before the print, that drops rings for good, and every plate stays on the
X2D 0.20 mm Standard. And the slicer's plan ranked the ring bottom cleaner for the second plate
running (0.41% bare against 0.93%) while the print found them about even, so the plan's bare share
is not a way to rank first-layer settings.

**What it does not settle.** The slits on the stock coaster are still there, so the question Omar
asked on 2026-10-10 is still open. The glacier plate's missing 0.02 mm push (suspect 3) was the
same for both coasters and is still untested. And `R` changed two things, the rings and the 30%
overlap: its strap edges came out closed, and this plate cannot say which of the two closed them.
Rows 2 and 3 of the page (`R` beside `F`, and `FC1 1E`'s fit in each) are not judged yet.

**What is left, Omar's to pick:**

| Option | What it verifies | Pros | Cons | Implications |
|---|---|---|---|---|
| **Stock lines with the 30% overlap only, beside stock** | Whether the overlap alone closes the slits along the strap edges, which is where stock leaves them | The edges were closed on `R`, and stock's diagonal lines have no meeting line down the middle to open; the overlap is set per piece, so the same two-coaster plate works | The edges may have closed because of the rings, not the overlap; the overlap may move a loose piece's fit (row 3 is not judged) | A yes puts the overlap on the coasters and sends fits to be checked again before it goes on a plate with loose pieces; a no leaves the overlap out too |
| **Stock on the gold Textured PEI plate, beside stock on the glacier** | Whether the extra 0.02 mm push the gold plate gets closes the stock slits (suspect 3) | Changes nothing in the slice but the plate type; tests the one suspect never tested | Two plates means two prints; mixes the plate into fits judged on the glacier | A yes ties a clean bottom to the gold plate for coasters |
| **Stop: stay on stock** | Nothing | No more prints on this; every fit stays as judged | The slits Omar asked about stay | The bed-face design closes as not fixed |
