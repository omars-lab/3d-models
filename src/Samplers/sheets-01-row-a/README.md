# Sheet 1, row A: today's staircase edge, cut to 30 mm windows

These three STLs are the control row of [sampler sheet 1](../../../docs/plates/sheets-01.md): the
coaster edge as it was before the true edges shipped, every wall made of 0.4 mm squares. bikar main
can no longer draw that edge, and the commit that still draws it has no window cut. So the windows
were cut once, from that commit with the window cut copied onto it, and are kept here. The window
cut was never merged there, and never will be. A second edge on bikar main would be two code paths
for one thing, and the old edge has no other use.

| File | Coaster | Window | sha256 |
|---|---|---|---|
| GimTvN9hw4U-minimal-coaster-window.stl | CS-1 | 30@9.7,1 | da3a40df55a57b00cfa08b46edc27df7438e107b94770a940cf40ebf2d0263d9 |
| 7apC5Q9QS-8-minimal-coaster-window.stl | CS-2 | 30@18.5,18.5 | c0ba87472a8cf358a95f4aa9a25c208cbf3a10aed0283560a01eef8c49d34e38 |
| gBV_JTt3Kxk-minimal-coaster-window.stl | gBV | 30@0,0 | c1b596e59f39a41adbd124718c0ba689652e79def54228103b0efa3a1015bccb |

The sheet file names each one with its hash, and `bambu slice sheet` refuses a file whose hash has
changed.

## How they were made

- **The edge** is bikar commit ef680dd3d21d95c05456fe07fb688cb3efc33fd1 (#290), the last one
  before the true edges (#291).
- **The window cut** is bikar #293 (db2e9fb8185d4c725a2aad832a834847ca4f4e0f), copied onto that
  commit by hand. The result is [window-backport.patch](window-backport.patch). One part of #293
  could not come across. On main the cut also clips the traced walls and drops any piece the cut
  leaves loose, and both of those read a field (the solid value at each grid point) that only exists
  after #291. Here the window is the same test as on main, "is this cell's centre inside the
  square", applied to the old edge's whole-cell keep-or-drop, so the window's edge is stepped like
  every other edge on it. Nothing came loose to drop: each file passes bikar's one-body check.
- **The render**, from a checkout of ef680dd with the patch applied (`git apply`), after
  `npm ci`, `npm run build:core` and `npm run build:cli`. One window per run:

  ```
  node packages/cli/dist/index.js render patterns/Constructions/<file>.bkr --format stl --check --piece Coaster --window <window> -o <out>.stl
  ```

  Rebuilt this way on 2026-10-01, all three came out byte for byte the same as the files here.
- **The checks** at render time:

  | Sample | Mesh check | Triangles | Euler |
  |---|---|---|---|
  | CS-1 | PASS, 1 body | 13,692 | −6 |
  | CS-2 | PASS, 1 body | 13,660 | −12 |
  | gBV | PASS, 1 body | 15,620 | −20 |

## The pinholes in CS-2

Row A's CS-2 has three more holes than row B's (Euler −12 against −6). Each is one 0.4 mm grid
cell left open, at (12.2, 25.0), (18.2, 12.2) and
(25.0, 12.2) in the coaster's frame. They come from the old edge, not from the window. The whole
CS-2 coaster rendered at ef680dd with no window has eight of them, and these three are the
ones inside the window, at the same coordinates. They are part of what row A shows: the old edge
can leave single-cell holes where the true edge leaves none.
