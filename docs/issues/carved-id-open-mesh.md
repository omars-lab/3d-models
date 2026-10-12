---
date: 2026-10-12
---

# A carved id left holes in the bed face, and compose never checked

2026-10-12. Found while cutting one repeat of the gBV coaster into a test piece for the bottom slits.
The piece passed bikar's mesh check without an id and failed it with one.

## What happened

Every experiment piece carries an id cut into the face that sits on the bed (D-109, bikar #330).
To cut the id, bikar takes the bed face away and lays a new one with the id's letters as holes in it.
When the face's outline has a long straight run made of many points close together (0.4 mm
apart along a cut edge or a strap edge), the new face comes out with gaps along that run. It also
gets triangles with no area, at height zero.

- The whole gBV coaster at 112.5 mm with the id `S` (bedface-2's coaster): not closed, 22 flat
  triangles.
- The 50 mm window piece with an id: 15 open edges and 11 flat triangles, all on two straight runs,
  one along the window's cut edge and one along a strap edge.
- The same pieces without an id: closed, and they pass.

## Why nobody saw it

`bambu slice compose` rendered every piece with `bikar render` but without `--check`, bikar's mesh
check. `bambu slice sheet` always passed it, and so does the plates gate's own render, so the gap was
in compose alone. Every compose plate with a carved id since bikar #330 went to the slicer with these
gaps, and Studio's warnings came back empty: it slices the shape at each layer's height, above the
bed face, where the walls are whole.

All 44 compose recipes were dry-run with the check, against bikar before the fix. It refuses
six, every one a gBV coaster with an id: bedface-1, -2 and -3 (ids F, S, G) and sheets-04g-fit,
-fit2 and -fit3 (ids Z, Z, 3). Every other recipe passes, the minis, sheets, splits, studs, swatches
and themes among them, so no plate fails the check on purpose. (The two phone plates copy a
downloaded mesh that lives only in the main checkout, outside git, so they were run there; bikar
renders nothing for them.) Five of the six printed with the
gaps. That most likely did not change what printed, for the reason above. Nobody checked
it against a slice made from a closed mesh, though, so the bedface records do not lean on it either way.

## What changed

- **compose runs the mesh check.** compose and sheet now build their render command in one place,
  `renderStlArgs` in `tools/bambu/src/commands/compose.ts`, which always adds `--check`. A unit test
  in `compose-ids.test.ts` checks that the flag is there for a plain piece, a window and a carved id.
  A piece that fails is refused before anything reaches the slicer, with bikar's last lines and the
  hint on cutting less of the id.
- **bikar closes the face.** The bikar fix lays the bed face without the in-line points, then puts
  each one back by splitting the triangle that holds its stretch of edge, so the face stays closed
  and no triangle is flat. The test there fails on the window piece before the fix and passes after.

`bambu coaster` renders with `--format parts`, not an STL, and is not changed here.
