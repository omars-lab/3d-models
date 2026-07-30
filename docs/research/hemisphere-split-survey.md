# Hemisphere-split STL export — prior-art survey

Research backing [`../hemisphere-split-design.md`](../hemisphere-split-design.md) (task #11).
Two read-only investigations, preserved as delivered:

- **§0** — code grounding of the bikar tree (what exists, what is absent), every claim carrying
  `path:line`.
- **§1–§8** — external prior-art survey: slicer-native cut vs exporter-native split, registration
  clearances, bonding, split-plane placement literature, printing a dome cut-face-down, validating
  manifold-with-boundary meshes, a numbers table, and what could not be settled.

Measurements taken directly against the shipped engine (not from either agent) are recorded in the
design doc §2 and §9, not here.

---

# §0 — Code grounding (bikar tree, read-only)

# Grounding report — hemisphere-split STL export for orbs

Repo: `/Users/omareid/Workspace/git/bikar` (branch `fix-polygon-mpt-vertex`, files read as they are on disk). Sibling docs repo: `/Users/omareid/Workspace/git/3d-models`.

---

## 1. The 3D kernel — `packages/core/src/kernel3d/`

### Mesh data structure

`OrbMesh` is the single mesh type for everything 3D — orbs, pieces, tiles, clips, assemblies. **Indexed triangles**, not a soup.

- `packages/core/src/kernel3d/solidify-lattice.ts:31-35` — `export interface OrbMesh { vertices: readonly Vec3[]; triangles: readonly (readonly [number,number,number])[]; stats: OrbMeshStats }`
- `packages/core/src/kernel3d/solidify-lattice.ts:15-24` — `export interface OrbMeshStats { euler; genus; volumeMm3; watertight }`
- `packages/core/src/kernel3d/solidify-lattice.ts:115-148` — `meshStats(vertices, triangles)`: builds a directed-edge map keyed `"u,v"`; `watertight = bad === 0 && volume > 0` where `bad` counts any directed edge whose count ≠ 1 or whose reversed twin count ≠ 1 (`:130-135, :146`). `euler = V − E + F` with `E = directed.size / 2` (`:136-137`). Volume = signed tets to origin (`:139-141`).
- `packages/core/src/math/vec3.ts` — `Vec3` (`{x,y,z}`), with `add3/scale3/dot3/cross3/normalize3/sub3/distance3/lengthOf3`.

### The lattice pipeline (inset → lift → band emit → weld). Note: **no triangulation step** in the orb path.

`packages/core/src/kernel3d/solidify-lattice.ts`:
- `insetPolygon(poly, t)` `:59` — offsets a CCW simple polygon inward by `t`; returns `null` on degeneracy (`:85`).
- `insetIsDegenerate` `:94` (private) — edge-direction flip / non-finite / area-not-shrinking gate.
- `buildRings(voids, insetT)` `:165` (private) — insets every void **once in shared pattern space** so points on shared face boundaries lift to bitwise-near-identical 3D positions and weld (`:156-163`). Throws naming the void when the inset collapses (`:169-175`).
- `solidifyLattice(base, voids, params)` `:193` — the whole pipeline. Computes `meanCircumradiusMm` over base faces (`:198-207`), `unitMm = meanCircumradiusMm / PATTERN_CIRCUMRADIUS` (`:208`), builds rings at `strutWidth/2/unitMm` (`:209`), creates `new VertexPool(1e-3)` (`:213`), then **per face** builds `lift = makeFaceLift(faceVerts)` (`:219`) and a `liftPair` closure (`:220-237`) that interns an outer vertex at `mid + dir·halfDepth` and an inner at `mid − dir·halfDepth`. Thickness is applied **radially in both `spherical` and `faceted` modes** — the comment at `:224-227` says a per-face-normal offset would separate the same seam point by ≈0.9 mm on an icosahedron at depth 2.4, far beyond weld tolerance, so the shell could never close. Returns `{vertices, triangles, stats: meshStats(...)}` (`:243-244`).
- `emitVoidBand(ring, liftPair, triangles)` `:253` (private) — three quad strips per void: top band CCW-from-outside, bottom band reversed, hole wall facing into the void (`:264-272`). Each quad → 2 triangles (`:258-260`).
- `meshStats` `:115` (exported, above).

Radial extrude + stitch is *implicit*: neighbouring voids share centerline edges within and across faces, so bands tile the shell and close watertight by welding, not by an explicit stitch pass (`:180-189`).

### The welder

`packages/core/src/kernel3d/weld.ts:22` — `export class VertexPool` (quantized 3D interner, cubic grid of cell size `tolerance`, `intern` searches the 27 neighbouring cells; `:36-59`). `positions` getter `:29`. Documented as the 3D sibling of `kernel/point-index.ts` (`:10`).

### Base polyhedra

`packages/core/src/kernel3d/polyhedra.ts`: `Polyhedron` `:12`, `centroid3` `:18`, `newellNormal` `:30`, `tetrahedron` `:62`, `octahedron` `:75`, `cube` `:98`, `icosahedron` `:122`, `dodecahedron` `:172`, `subdivideGeodesic(poly, frequency)` `:210`.

### Face lifting

`packages/core/src/kernel3d/face-frame.ts`: `PATTERN_CIRCUMRADIUS = 100` `:12`, `patternCorner(n,k)` `:19`, `type FaceLift = (p: Point) => Vec3` `:28`, `barycentricPatternWeights` `:36`, `makeFaceLift(faceVertices)` `:93`, `faceCircumradiusMm(faceVertices, sphereRadius)` `:107`.

### Woven family (Family 1)

`packages/core/src/kernel3d/weave.ts`: `PatternGraph2D` `:18`, `WeaveParams` `:24`, `WeaveResult {mesh, strandCount, crossingCount}` `:38`, `patternGraphFromPlanar(graph)` `:53`, `weaveLattice(base, graph2d, params)` `:483` — lift+weld, detect 4-valent crossings, trace closed strands, solve global over/under parity, sweep each strand into a closed rectangular tube. Output is "a union of disjoint watertight tori" (`:476-478`).

### Piece solidifier (this *is* the triangulate path — earcut)

`packages/core/src/kernel3d/solidify-piece.ts`: `HOLE_SEGMENTS = 64` `:28`, `REVOLVE_SEGMENTS = 96` `:30`, `WELD_TOLERANCE = 1e-3` `:33`, `PieceHoleSpec` `:36`, `PieceSolid` `:49`, `circlePoints` `:55`, `normalizeRing` `:71`, `pointInPolygon` `:95`, `minDistToRing` `:108`, `pushQuad` `:122`, `emitCap` `:225`, `solidifyExtrudedPiece(outline, holes, depth)` `:320`, `solidifyRevolvedPiece(profile)` `:447`, `solidifyRodPiece(d, height)` `:501`, `solidifyTubePiece(innerD, outerD, height)` `:531`.
Triangulation library: `packages/core/src/kernel3d/earcut-vendored.ts` (vendored mapbox/earcut, default export `earcut` `:67`). It is used only by the piece/clip path (`corner-clip.ts:292,382`), never by `solidify-lattice.ts` or `weave.ts`.

### Slabs / connectors / other

- `solidify-slabs.ts`: `SectionCell` `:42`, `Slab` `:51`, `solidifySlabStack` `:237`.
- `clipseat.ts`: `CLIPSEAT_*` dims `:25-33`, `CornerName` `:36`, `cornerPoint` `:53`, `ClipseatKeyhole` `:137`, `buildClipseatTileSlabs` `:221`.
- `corner-clip.ts`: `CLIP_*` constants `:34-48`, `resolveCornerClipDims` `:174`, `buildCornerClipSlabs` `:350`.
- `keyhole.ts`: `KEYHOLE_*` `:20-28`, `KEYHOLE_SCREWS` `:55`, `keyholeRing` `:89`, `keyholeFootprint` `:126`, `keyholeMinDepthMm` `:137`, `buildKeyholeTileSlabs` `:152`.
- `frame.ts`: `Frame` `:42`, `RigidXform` `:55`, `PortFrame` `:69`, `rotate3` `:93`, `identityXform` `:112`, `applyXform` `:122`, `composeXform` `:137`, `invertXform` `:149`, `frameFromPort` `:163`, `transformFrame` `:170`, `matedFrame` `:187`, `xformFromTo` `:201`, **`applyXformToMesh(mesh, x)` `:218`**, **`concatMeshes(meshes)` `:232`**. Closure tolerances `CLOSURE_POS_TOL_MM = 1e-6` `:27`, `CLOSURE_ANG_TOL_RAD = 1e-6` `:35`.
- `calibration.ts`: `CAL_BET_IDS` `:33`, `Provenance` `:69`, `Calibrated<T>` `:82`, `provisional(bet, value, basis)` `:97`.
- `index.ts` (barrel) `packages/core/src/kernel3d/index.ts:1-106` — re-exports all of the above.

### Plane clip / half-space / boolean — the closest existing thing

**There is no mesh-level plane clip, half-space, or boolean anywhere in `kernel3d/`.** Grep for `halfspace|half-space|planeClip|clipPlane|boolean` over `kernel3d/` returns only `boolean` as a TS type and the two connector files named "clip" (`corner-clip.ts`, `clipseat.ts`), which are *bayonet clip hardware*, not geometric clipping.

The nearest existing machinery is `packages/core/src/kernel3d/slice.ts`, which already does triangle-vs-z-plane intersection but returns **2D loops, never a mesh**:
- `crossingPoint(a, b, z)` `:128` — linear interpolation of an edge against plane `z`.
- `triangleCut(tri, verts, z)` `:139` — returns the two crossing points, or `null` when the triangle does not straddle. Tie rule: "a vertex exactly at z counts as not-below, consistently for every triangle sharing it — that is what keeps the loops closed" (`:133-137`).
- `chainLoops(segments)` `:170` — chains segments into closed loops by quantized endpoint key (`key` `:158`, `CHAIN_TOLERANCE_MM`). Dead-ending chains "are dropped and counted by the caller's mesh gate" (`:167-169`).
- `nestLoops` `:221`, `nearestEnclosing` `:252`, `orient` `:267`.
- `sliceAt(mesh, z)` `:273` — cross-section at one absolute height, returns `SliceRegion[]`.
- `sliceMesh(mesh, layerHeightMm = 0.2)` `:297`; `MAX_LAYERS = 20000` `:43`, `DEFAULT_LAYER_HEIGHT_MM = 0.2` `:46`.
- Types: `SliceRegion` `:52`, `SliceLayer` `:60`, `Bounds2D` `:69`, `SliceResult` `:77`; helpers `signedArea` `:85`, `ringBounds` `:96`, `pointInRing` `:115`.

Core has **zero runtime dependencies** (`packages/core/package.json:21-23` lists only a devDependency). `print-gate.ts:29-33` states outright that this repo has no 2D boolean/offset dependency and that "the composition work that was supposed to bring one deliberately rejected it (see the W2 decision doc §A)".

---

## 2. STL / mesh emission

`packages/core/src/render/mesh-emitter.ts` — one export, one body:

```ts
export function emitBinarySTL(mesh: OrbMesh, header = 'bikar orb'): Uint8Array   // :17
```

- Binary STL only. Layout: 80-byte header, uint32 tri count, per triangle normal + 3 verts + uint16 zero (`:13-15`, `:18-40`).
- Per-triangle normals **recomputed** from vertex winding (`:33`), never trusted from upstream.
- Header truncated to 80 bytes, masked to 7-bit ASCII (`:24-26`); comment `:21-23` warns the header must not start with `"solid"`.
- **One mesh, one buffer, per call.** It cannot emit multiple bodies or multiple files. Multi-file output is done by the *caller* looping `emitBinarySTL` (see §5).

No ASCII-STL, 3MF, OBJ, or STEP emitter exists. `packages/core/src/render/` contains only: `animation-compiler.ts`, `gt-emitter.ts`, `index.ts`, `mesh-emitter.ts`, `orb-view-renderer.ts`, `source-tags.ts`, `svg-renderer.ts`, `svg-utils.ts`.

---

## 3. The mesh gate and the print gate

### Gate A — `meshGate` (`--check` / `--check mesh`)

`packages/core/src/kernel3d/mesh-gate.ts`:
- `DEFAULT_MIN_FEATURE_MM_CAL: Calibrated<number>` `:13` — bet `CAL-FEA-01`, value **1.2 mm**, basis text `:16-19` explicitly notes coupon MC-2's "sub-floor rungs are expected to FAIL this very gate by design".
- `DEFAULT_MIN_FEATURE_MM = 1.2` `:22`.
- `MeshGateOptions { minFeatureMm? }` `:25`.
- `MeshGateReport { watertight, euler, degenerateTriangles, declaredMinFeatureMm, minFeatureMm, passed, failures }` `:36-44`.
- `DEGENERATE_AREA_MM2 = 1e-6` `:52`; `countDegenerateTriangles` `:58` — repeated index or cross-product area < threshold.
- `meshGate(mesh, declaredMinFeatureMm, options?)` `:82`.

Exactly three assertions, in this order:
1. **Watertight** — `mesh-gate.ts:90-92`, sourced from `mesh.stats.watertight` (computed in `solidify-lattice.ts:146`). Failure message verbatim:
   `` `mesh is not watertight (euler=${mesh.stats.euler})` `` (`mesh-gate.ts:91`).
2. **Degenerate triangles** — `:93-95`, message `` `${n} degenerate triangle(s) (repeated vertex or ~zero area)` ``.
3. **Declared min feature ≥ floor** — `:96-101`, message `` `declared minimum feature ${x}mm is below the printable floor ${y}mm — widen 'struts width/depth' or relax the floor` ``.

**Euler is reported but deliberately not gated** — `:76-80`: "its expected value is family-specific (2 − 2g for a pierced shell, 0 for woven tubes) and the evaluator already enforces it per family."

### Gate B — `printGate` (`--check print`)

`packages/core/src/kernel3d/print-gate.ts`:
- Codes `PrintFindingCode = 'F1'|'F2'|'F3'|'F7'` `:73`; severity `:70`; `PrintFinding` `:76`.
- `MIN_BED_CONTACT_MM2_CAL` `:47` = **25 mm²** (bet `CAL-BED-01`, explicitly "no primary source at all", `:44-53`); `MIN_BED_CONTACT_RATIO_CAL` `:59` = **0.01**.
- `PrintGateOptions { layerHeightMm?, minBedContactMm2?, minBedContactRatio?, expectedBodies? }` `:109-115`.
- `PrintGateReport` `:118-134`.
- `countComponents(mesh)` `:147` — union-find over shared welded vertex indices. Known limit documented `:141-145`: two bodies meeting at a single welded vertex read as one component; F5 (V2) is the named backstop.
- `regionsOverlap` `:284`, `boundRegion` `:292`, `BoundedRegion` `:184`, `interiorProbes` `:255` (with `INTERIOR_NUDGE_MM = 1e-6` `:233`), `buildSupportLinks` `:307`, `markGrounded` `:319`, `findIslands` `:347`, `traceMerge` `:371`.
- `checkBodyCount` `:396`, `checkBedContact` `:429`, `islandFindings` `:470`, `printGate(mesh, options?)` `:508`.
- **Print orientation is not controllable**: `:502-507` — "Slices in the mesh's own orientation with the bed at its lowest z; print-orientation control is V3 work (design §4), so a part meant to print face-down must be modeled that way for now."
- F4 (overhang), F5 (neck), F6 (bridges) are **not implemented** — `:24-33`.

### The exemption question — this is the key finding

**There is no mechanism anywhere for exempting a mesh from a check.** No `@no-check` pragma, no `exempt` DSL keyword, no per-declaration gate override, no `--skip-check`, no `minFeatureMm` override reachable from the CLI. `meshGate`'s `options.minFeatureMm` (`mesh-gate.ts:27`) is the only override and **the CLI never passes it** (`packages/cli/src/index.ts:459` and `:207` both call `meshGate(mesh, declaredMin)` with no options).

The **W2 "sub-floor mesh-gate exemption" is expressed only in prose and in what the recommended command line omits.** The recipe is literally "don't pass `--check` on that part":
- `patterns/Coupons/Clip-Coupon.bkr:8-20` — "`--check` on the CLIP part reports FAIL — expected… (drop `--check` on the clip — its blade is intentionally sub-floor)".
- `patterns/Walls/Clip-Wall.bkr:12-23` — "only the separately-rendered clip is exempt… `--piece StarClip -o StarClip.stl` (its blade is intentionally sub-floor, so no `--check`)".
- `patterns/Coupons/Machine-Card.bkr:34` — "flag exists and none is being added (the W-series sub-floor rule…)". That line is an explicit statement that **no exemption flag is being added**.
- `docs/decisions/2026-07-29-w2-wall-connectors-mounts.md:150-165` §D "The clip is exempt from the FDM mesh floor; the tile is not (the policy call)" — "Two honest options: loosen the floor, or exempt the part. **Exempt the part, in the open.**" Rejected alternatives named at `:167-169`: lowering the global floor, and auto-detecting "connector-like" parts.
- `docs/decisions/2026-07-29-print-gate-v1-slice-structure.md:221-222` — the clip "which carries a *documented* sub-floor exemption (`wall-connectors` §D) — never reached the print gate at all."
- `docs/roadmap.md:20` — "The clip's ~0.6 mm bayonet jaw is a documented sub-floor mesh-gate exemption; the tile is not exempt (2.4 mm PASS)."
- The one *partial* in-code carve-out: the tile's clipseat rebate is deliberately excluded from `minFeatureMm` inside `kernel3d/clipseat.ts` because it is "a step, not a strut" (decision `:157-160`).

### The one existing "declared expectation" mechanism — `ExpectedBodies`

This is the closest precedent for a split-export exemption, and it is a **derived** value, not an authored one.

`print-gate.ts:100-106`:
```ts
export type ExpectedBodies =
  | { readonly kind: 'single' }
  | { readonly kind: 'assembly'; readonly count: number }
  | { readonly kind: 'woven' };
```
Rationale `:84-99`: F1 cannot be "exactly one body" unconditionally, because an assembly of N is N bodies by definition and a woven orb is interlocked-but-unfused ribbons. "a gate that cries wolf gets switched off." The comparison is **bidirectional** — `checkBodyCount` `:396-421` errors both when a part has fragmented (`count > want`) and when parts have fused (`count < want`).

It is derived in the CLI, never authored: `packages/cli/src/index.ts:256-263` `expectedBodies(result)` reads `result.assembly3d.parts.length` or `result.orb3d.family === 'weave'`. **There is no DSL statement that sets it**, and there is no analogous "expected open boundaries" concept anywhere — watertightness is unconditional and binary.

---

## 4. The C2 piece / port / rod / connect / assembly layer

### AST

`packages/core/src/dsl/ast.ts`:
- `PieceConstructorNode` `:174-179` — `extrude | revolve | tube | rod`. `rod` is "(C2) the solid cylinder `revolve` cannot make… a direct pin mesh for printed dowels, `d` a diameter" (`:170-172`).
- `PieceHoleBand { d, from, to }` `:181`; `PieceHoleNode { name, at, bands }` `:196-202`. Doc `:184-195`: "a hole is a named *stack of z-bands*, each subtracting a circle from the 2D section over its z range, so drilling stays 2D-per-slab. Every hole also auto-mints a port on its axis (`<Piece>.<name>`, the OnShape implicit-connector insight)."
- `PortContractNode` `:213-218`:
  ```
  pin {d, fit} | pin_socket {d} | ring {d, depth} | rim {d, depth} | axis
  ```
- `PiecePortNode { name, at, z, dir: '+z'|'-z', spinDeg, contract }` `:229-237`.
- `PieceDeclarationNode { kind, name, body, holes, ports }` `:248-254`.
- `TileDeclarationNode` `:277-289` (`holes`, `ports`, `mounts`, `clipseat`).
- `AssemblyConnectNode { from:{piece,port}, to:{piece,port}, spinDeg }` `:368-372`.
- `AssemblyDeclarationNode { kind, name, places: readonly string[], connects, exportParts }` `:382-388`.
- `OrbDeclarationNode { kind, name, base:{solid, subdivide?}, radius, inscribe, projection, struts:{width,depth}, pierce, weave? }` `:140-156`. **An orb has no `ports` field and no `holes` field.**

### What a port actually generates geometrically: **nothing**

A `port` is a *frame + contract only*. It emits zero triangles. Evidence:
- `mintDeclaredPorts` `packages/core/src/dsl/evaluator.ts:1219-1240` produces `{name, kind, frame:{origin, zDir, spinDeg}, contract}` — no mesh.
- The geometry that *does* exist comes from other statements: `hole` (subtracted z-band circles, `solidifyExtrudedPiece` `solidify-piece.ts:320`) and `rod` (the actual pin solid, `solidifyRodPiece` `solidify-piece.ts:501`). In `patterns/Assemblies/Pinned-Tiles.bkr` the pin is a separate `piece PinA / rod d $pin_d height 2 * $depth` (`:18-19`) with two ports declared on it (`:20-23`).
- Port anchoring rules: `resolveDeclaredPortAnchor` `evaluator.ts:1241-1265` — name-collision with an auto-minted hole port is an error (`:1249-1252`); `at point` on an axisymmetric (rod/tube) piece is an error (`:1254-1258`); point outside the outline is an error (`:1261-1264`). `resolveDeclaredPortZ` `:1267-1276` — default `+z → depth`, `-z → 0`; z outside `0..depth` errors.
- Hole-minted port convention: `evaluator.ts:1188-1191` — "pins enter from the top face — authors needing bottom entry declare an explicit port."

### Fit profiles and their numbers

`packages/core/src/kernel3d/fit-profile.ts`:
- `PortFit = 'press'|'snug'|'sliding'|'free'` `:20`.
- `FIT_GAP_MM_CAL` `:27-40` — bet `CAL-FIT-01`, diametral gap (socket ⌀ − pin ⌀): **press −0.1, snug +0.05, sliding +0.15, free +0.35** (`:31-34`). Basis: "Literature-shaped FDM clearance ladder, spaced on an even 0.10 mm step for legibility rather than fitted to any machine; no pin and socket have been printed and mated. Coupon MC-1 … settles it." `FIT_GAP_MM` `:41`.
- `FIT_TOL_MM_CAL` `:53-61` = **0.05 mm** symmetric window half-width; `FIT_TOL_MM` `:62`.
- `PrinterProfile` `:81`, `PROFILE_WARP_MM_CAL` `:105`, `PRINTER_PROFILES_CAL` `:120`, `PRINTER_PROFILES` `:134`, `knownProfileNames()` `:137`, `PERIMETER_WIDTH_MM = 0.4` `:148`, `PrinterProfileFacts` `:158`, `printerProfileFacts` `:166`, `requiredSocketD(pinD, fit)` `:175`, `fitGapDeviationMm` `:185`, `fitWindowOk` `:190`, `fitClassesForGap` `:201`.
- Profile compensation values (from `docs/language-reference.md:825-827`): `none` 0, `pla_calibrated` +0.20, `petg_calibrated` +0.25 mm added to printed hole ⌀ only; fit windows validate the *authored* ⌀.

### Can a port carry registration pins between two halves of ONE printed object? **No, not as the layer is built today.**

Hard constraints, each read directly:
1. **`connect` requires two named declarations, resolved by name against a registry.** `resolvePlacedPieces` `evaluator.ts:2414-2430` looks up every `place` in `pieceRegistry` and errors `assembly ${name}: piece '${p}' is not declared (or is declared after the assembly)`.
2. **Only `piece`, `tile`, and `clip` enter that registry — never `orb`.** `evaluator.ts:717-733`: `pieceDeclaration` → `pieceRegistry.set` `:719`; `tileDeclaration` → `:725`; `clipDeclaration` → `:730`. `case 'orbDeclaration'` at `:716` returns `evaluateOrbDecl(...)` **without registering anything**. So an orb literally cannot be `place`d in an assembly.
3. **One instance per piece.** `docs/language-reference.md:840` — "one instance per piece (`place … as …` instancing is C3)". So you could not `place TopHalf` twice, nor place one declaration as two halves.
4. **Every placed piece must be reachable from the root through connects.** `evaluator.ts:2467-2472` — error `piece '${unreached}' is placed but never connected`.
5. **One connection per port** — `evaluator.ts:2334` "Claim both of a connect's ports — the second claim of any port is an error".
6. **The combined assembly STL is concatenated, never welded.** `evaluator.ts:2483` `concatMeshes(parts.map(part => applyXformToMesh(part.mesh, part.xform)))`, with the rationale at `:2439-2442`: "parts concatenated, never welded, because welding would fuse coincident pin/socket faces into non-manifold edges".
7. **A port carries no clearance geometry.** The fit ladder is validated on *declared numbers* only (`evaluator.ts:2214-2270`); the physical gap must be authored as differing hole ⌀s (see `Pinned-Tiles.bkr:37` press bore `$pin_d - 0.10` vs `:46` sliding bore `$pin_d + 0.15`).

Conclusion for the design doc: registration between two halves of one split orb cannot reuse `port`/`connect` as-is. The *fit ladder numbers* (`FIT_GAP_MM`) and the *rod/socket geometry generators* (`solidifyRodPiece`, `solidifyExtrudedPiece`'s hole bands) are reusable; the assembly graph is not.

---

## 5. The CLI surface — `packages/cli/src/index.ts` (592 lines)

Hand-rolled arg parsing over `process.argv.slice(2)` (`:88-89`) — **no commander/yargs**. Helpers: `getFlag(name)` `:133` (errors if the next token is missing or starts with `--`), `orDie` `:150`, `collectParamOverrides` `:167`, `compileOptions` `:191`.

### Exact `render` flags (from `usage()` `:91-122`, verbatim strings)

| Flag | Values | Line |
|---|---|---|
| `-o <path>` | file, or **directory** for `views`/`parts` | `:93`, `:317`, `:353`, `:478` |
| `--stdout` | | `:93` |
| `--format` | `svg` \| `stl` \| `views` \| `parts` (default `svg`) | `:94`, `:403-407` |
| `--check` | bare = `mesh`; `--check mesh`; `--check print` | `:96-102`, `:229-237` |
| `--layer-height <mm>` | default 0.2 | `:101-102`, `:266` |
| `--piece <Name>` | render a named piece/tile/clip | `:103-105`, `:429` |
| `--width <px>` | default 900 (views + truth) | `:107`, `:358` |
| `--fit-profile` | `none` \| `pla_calibrated` \| `petg_calibrated` | `:111-112`, `:193` |
| `--param <name>=<value>` | repeatable | `:113-115`, `:167-183` |
| `--emit-truth <path.gt.json>`, `--image <name.png>`, `--height <px>`, `--sha256 <hex>` | | `:116-117` |

Other commands: `bikar parse <input>` `:118`, `bikar validate <input>` `:119`.

### How `--format stl` and `-o` interact (`:419-489`)

1. `compileToGeometry(source, compileOptions())` `:424`.
2. Optional `--piece` selection via `selectPiece` `:73-86` (dies listing declared pieces when absent).
3. `if (!result.orbMesh)` → error `--format stl requires an orb or piece declaration in the source (this file only produces 2D geometry — render it as SVG instead)` `:431-437`.
4. Wall/assembly stderr reports `:440-449` (suppressed when `--piece` given).
5. Gates `:450-476`. `declaredMin = result.orb3d ? Math.min(strutWidthMm, strutDepthMm) : result.piece3d!.minFeatureMm` `:456-458`. Both gates run before exiting (`:467-474`), and **nothing is written when either fails** — `if (failed) process.exit(1)` `:475`. The comment at `:468-472` says explicitly: "a part with a known sub-floor feature fails the mesh gate every time… Nothing is written until both have spoken, so a failing part never leaves an STL behind for someone to pick up by mistake."
6. `const stl = emitBinarySTL(result.orbMesh)` `:477`. `-o` is looked up via a raw `args.indexOf('-o')` (`:478`) — **not** `getFlag`. With `-o <path>`, `writeFileSync` + a stdout line reporting triangles / KiB / cm³ (`:480-485`). **Without `-o`, the raw STL bytes go to `process.stdout.write(stl)` `:487`** — which is why every gate line is on stderr.

So today `--format stl` is strictly **one mesh → one file (or stdout)**.

### The one existing multi-file path — `--format parts` (directly relevant precedent)

`renderAssemblyParts(source)` `:303-333`:
- Requires `result.assembly3d`, else error `--format parts requires an assembly declaration in the source (pieces and tiles are single prints — render them with --format stl)` `:307-311`.
- Requires opt-in in the DSL: `if (!assembly.exportParts)` → `Error: 'export parts' not declared in assembly '${name}'` `:313-316`. Rationale `:299-301`: "The assembly must opt in with 'export parts': the declaration is the printable-unit contract, not a CLI convenience."
- **`-o` must be a directory**: `Error: --format parts writes multiple files — pass -o <directory>` `:317-321`. `mkdirSync(outDir, {recursive:true})` `:322`.
- **Gate-all-before-write-any**: `if (args.includes('--check')) gateAssemblyParts(assembly)` `:323`, and `gateAssemblyParts` `:204-220` accumulates failures across all parts then `process.exit(1)` — "Exits before any STL is written when a part fails, matching the single-STL path's no-output-on-failure contract" (`:201-203`).
- **File-naming convention** `:326`:
  ```ts
  const path = join(outDir, `${assembly.name}-${part.piece}.stl`);
  ```
  i.e. `<Assembly>-<Piece>.stl`. Per-part stdout line at `:328-331`.
- Each part is emitted from its **piece-local** mesh, not its world pose (`:295-299`: "a printable part plates on its authored bottom face, not in its assembled pose").

The second multi-file path is `--format views` (`renderOrbViews` `:343-394`), naming `<orbName>.<viewId>.svg` and `<orbName>.<viewId>.gt.json` (`:385-386`), also requiring `-o <directory>` (`:353-357`).

---

## 6. Orb geometry facts

All 11 shipped orbs live in `patterns/Orbs/`. **All are `orb` declarations with a mid-surface sphere radius; there are no non-spherical orbs.** `projection` is either `spherical` (radially projected onto the sphere) or `faceted` (flat faces at scale R) — both apply thickness radially (`solidify-lattice.ts:224-235`).

Uniform defaults across every shipped orb:
- `param radius = 60 range 40..110 step 5`
- `param strut_width = 3 range 1.5..6 step 0.5 advanced`
- `param strut_depth = 2.4 range 1.2..4 step 0.2 advanced`

| Pattern | `base` | radius line | strut_width / strut_depth lines |
|---|---|---|---|
| `Dodeca-Orb.bkr` | dodecahedron `:26` | `:11` | `:12`, `:13` |
| `Hankin-Orb.bkr` | dodecahedron `:34` | `:17` | `:19`, `:20` |
| `Rosette-Orb.bkr` | dodecahedron `:46` | `:13` | `:16`, `:17` |
| `Rosette-Cube-Orb.bkr` | cube `:46` | `:13` | `:16`, `:17` |
| `Rosette-Weave-Orb.bkr` | dodecahedron `:46` | `:16` | `:20`, `:21` |
| `Star-Orb.bkr` | icosahedron `:31` | `:10` | `:11`, `:12` |
| `Star-Cube-Orb.bkr` | cube `:32` | `:12` | `:13`, `:14` |
| `Star-Octa-Orb.bkr` | octahedron `:33` | `:12` | `:13`, `:14` |
| `Star-Tetra-Orb.bkr` | tetrahedron `:33` | `:12` | `:13`, `:14` |
| `Weave-Orb.bkr` | icosahedron `:33` | `:17` | `:19`, `:20` |
| `Weave-Dodeca-Orb.bkr` | dodecahedron `:29` | `:13` | `:15`, `:16` |

So the default orb is **⌀120 mm** (R=60), 3 mm struts, 2.4 mm radial shell. Max R=110 → ⌀220 mm.

Note the mesh gate's declared feature for an orb is `min(strutWidthMm, strutDepthMm)` (`cli/src/index.ts:457`) = 2.4 mm at defaults, comfortably above the 1.2 mm floor.

### Poles / canonical axes

Yes — computed in `packages/core/src/kernel3d/orb-views.ts:39-48`, `symmetryViewAxes(base)`. It returns exactly three axes, deterministic (representatives are element 0 of each list, `:35-36`):
- `vertex-N`: `normalize3(base.vertices[0])`, fold = number of faces containing vertex 0 (`:40`, `:45`).
- `face-N`: `normalize3(centroid3(face0 verts))`, fold = `face0.length` (`:42`, `:46`).
- `edge-2`: `normalize3(midpoint(v[face0[0]], v[face0[1]]))`, fold 2 (`:43`, `:47`).

Types: `OrbViewKind` `:14`, `OrbViewAxis {id, kind, fold, axis}` `:23-28`. Consumed by `--format views` (`cli/src/index.ts:364`). Related: `DEFAULT_FRONT_CAP_MIN_DOT = 0.3` `:88`, `projectOrbView` `:151`, `OrbViewPolygon.minDot` documented as "1 at the pole, 0 on the rim" (`:57-58`).

Orb provenance carried to consumers: `OrbProvenance {name, base: Polyhedron, radiusMm, projection, strutWidthMm, strutDepthMm, family: 'lattice'|'weave'}` `packages/core/src/dsl/evaluator.ts:379-387`. Base construction: `buildOrbBase(decl)` `evaluator.ts:760`.

---

## 7. Existing docs on splitting / printing in pieces

### The decisive prior statement — hemisphere split is already named and deferred

`3d-models/docs/orb-lab-design.md:32-34`:
> Non-goals (v1): per-face pattern mixing (engine doesn't support it — see §2), girih-field orbs, community sharing/galleries, in-browser qiyas validation (Python; stays in CI), **hemisphere-split FDM export (task #11, separate decision)**.

`3d-models/docs/orb-lab-design.md:337-347` (§6.5 "Print target — localStorage, not URL (decided 2026-07-26)"):
> - Ceiling math: whole sphere must fit → `2R ≤ min(X, Y, Z) − 10 mm` margin. (The FDM **hemisphere-split variant, task #11**, would relax the Z term for tall-bed machines.)
> - The machine choice **implies the process**, driving guidance with zero extra knobs: FDM targets surface the weave "powder process required" notice and the **split-export dependency**; SLS/MJF service targets print everything as-is.

Machine table cited there: Bambu X1C/P1S (256³), A1 (256³), A1 mini (180³), Prusa MK4/Core One, Ender 3, plus SLS/MJF service presets and Custom (`:339-341`).

These are the two constraints the new doc must not contradict: (a) hemisphere split is `task #11` and owns its own decision doc; (b) the whole-sphere ceiling formula stays, with split relaxing only the **Z** term.

### Print orientation and supports — already decided as out of scope

- `packages/core/src/kernel3d/print-gate.ts:502-507` — orientation control is **V3**; today the mesh is sliced in its authored orientation, bed at lowest z.
- `3d-models/docs/print-validation-design.md:14`, `:64` — F4 overhang is a *warn*, not implemented (V2).
- `docs/roadmap.md:21` (bikar) — "the three Family-1 weave orbs fail F2 on genuinely unsupported islands (verified by hand: 34.9 mm² starting at z=60.1 with zero overlap below), **which is a print-recipe question for the prototype, not a gate bug**." Directly relevant: today's answer to un-printable orbs is "print recipe / supports", not "split the geometry".
- `3d-models/docs/print-validation-grounding-audit.md:39-46, 88` — overhang thresholds surveyed: PrusaSlicer auto = half extrusion width (≈48° at 0.2/0.45), Cura 50° from vertical, Bambu 30° from horizontal; "a fixed 45° over-warns relative to every mainstream default."

### Related decided ground

- `3d-models/docs/w2-connector-design.md:386` — "the coupons split into one file per part" (the `--format parts` / `--piece` idiom).
- `3d-models/docs/calibration-design.md:35, 264-292, 380` — coupon **MC-4 overhang fan** (`revolve`, 20/30/40/45/50/60° from vertical, bet `CAL-OVH-01`), rendered with `--format stl --check --piece MC4OverhangFan`. Orientation rule table `:506`: "MC-4 fan | upright, base on the bed | the flare is the overhang; any other orientation is a different test."
- `3d-models/docs/research/code-cad-composition-survey.md:125` — "**Print-in-place vs assembled**: consensus clearances — PIP joints 0.3 mm start (0.2–0.6 range); FDM snap/pin fits 0.2–0.3 mm snug, 0.4–0.5 mm free-sliding" — the survey that fed `FIT_GAP_MM`.
- `3d-models/docs/research/tile-wall-grounding-audit.md:132` — magnet pockets settled at **+0.1–0.2 mm clearance + glue note + entry chamfer**, with `fit press` (−0.1) available as explicit intent; the −0.1 interference school was explicitly rejected as an auto default. Relevant if the new doc proposes magnets as the registration feature.

**No document anywhere in either repo discusses splitting an orb into hemispheres beyond the two `orb-lab-design.md` deferral lines above.** Grep for `hemispher` across `packages/**/*.ts` returns only the *view-projection* meaning (front-hemisphere orthographic render): `orb-views.ts:18,85`, `render/gt-emitter.ts:222`, `render/orb-view-renderer.ts:64`, `lab/src/protocol.ts:22`, `docs/language-reference.md:532`, `docs/dsl-metadata-contract.md:145`. None of these is a geometric split.

---

## Confirmed absences

Each verified by reading the file or by an exhaustive grep, not inferred:

1. **No plane-clip, half-space, or CSG/boolean operation on meshes.** Nothing in `packages/core/src/kernel3d/` splits, unions, differences, or intersects an `OrbMesh`. `print-gate.ts:29-33` states the repo deliberately has no 2D boolean/offset dependency; `packages/core/package.json` has zero runtime dependencies.
2. **No mesh-splitting utility of any kind.** `slice.ts` cuts triangles against a z-plane (`triangleCut:139`) but produces only 2D `SliceRegion[]` — it never re-emits triangles or caps a cross-section.
3. **No cap/lid triangulator for an arbitrary cut cross-section.** `earcut-vendored.ts` exists and is used by `solidify-piece.ts`/`corner-clip.ts` for planar piece caps, but there is no code path from a slice loop set to a capped mesh.
4. **No `--split` flag, no `--surface` flag, no `--orient`/`--rotate` flag.** Grep of `packages/**/*.ts` for `--split`/`'split'`/`hemisphere` returns nothing in the CLI. The complete `render` flag set is listed in §5.
5. **No DSL keyword for splitting.** `OrbDeclarationNode` (`ast.ts:140-156`) admits exactly `base`, `radius`, `inscribe`, `project`, `struts`, `pierce`, `weave` — confirmed independently by `3d-models/docs/orb-lab-design.md:44-46` ("admits exactly seven statements").
6. **No mechanism to exempt a mesh from any check.** No pragma, attribute, DSL statement, or CLI flag. `patterns/Coupons/Machine-Card.bkr:34` explicitly says no such flag exists and none is being added. The W2 exemption is enforced socially: the pattern header tells you to *omit* `--check` for that `--piece`.
7. **No way to declare an expected number of open boundaries.** Watertightness (`mesh-gate.ts:90-92`) is unconditional and has no override. `MeshGateOptions` (`:25-28`) exposes only `minFeatureMm`, and the CLI never passes it (`cli/src/index.ts:207`, `:459`).
8. **`ExpectedBodies` is not authorable.** It exists (`print-gate.ts:100-106`) but is derived in the CLI from `assembly3d`/`orb3d.family` (`cli/src/index.ts:256-263`); no DSL statement sets it.
9. **An `orb` cannot participate in `assembly`/`connect`.** `evaluator.ts:716` returns the orb result without registering it in `pieceRegistry` (contrast `:719`, `:725`, `:730` for piece/tile/clip), and `resolvePlacedPieces:2420-2426` errors on any unregistered name.
10. **A `port` generates no geometry.** `mintDeclaredPorts` (`evaluator.ts:1219-1240`) produces a frame + contract only. Pins come from a separate `rod` piece; sockets from `hole` bands.
11. **`emitBinarySTL` cannot emit more than one body or file per call** (`mesh-emitter.ts:17-42`). Multi-file output exists only as a caller-side loop in `renderAssemblyParts` (`cli/src/index.ts:324-332`) and `renderOrbViews` (`:364-393`).
12. **No print-orientation control.** `printGate` slices in the mesh's authored orientation (`print-gate.ts:502-507`, "V3 work").
13. **No overhang, neck, or bridge check.** F4/F5/F6 are declared V2 and unimplemented (`print-gate.ts:24-33`; `PrintFindingCode` is `'F1'|'F2'|'F3'|'F7'` at `:73`).
14. **No prior doc, decision, or issue describes hemisphere splitting.** Only the two deferral lines at `3d-models/docs/orb-lab-design.md:34` and `:344` (plus the dependency mention at `:346`). No `docs/decisions/*` entry, no roadmap item, no design doc.
---

# Survey: hemisphere-split STL export for openwork lattice spheres

**Scope.** Prior art for exporting a pierced spherical Islamic-geometric lattice (Ø ~120 mm, strut ~3 mm wide, shell ~2.4 mm deep, single watertight binary STL) as two re-joinable hemispheres for FDM printing on Bambu A1 / P1S / X1C class machines.

**Method note.** Sources were fetched and read wherever possible (slicer source code, official docs, PDFs of papers and manufacturer data sheets). Anything seen only as a search-result snippet is tagged `(unverified snippet)`. Where sources disagree, both positions are reported. Numbers that are my own arithmetic on the orb's stated geometry are tagged **[derived]** and are not claims by any source.

---

## 1. Slicer-native cut vs exporter-native split

### 1.1 What the slicers actually ship today

**PrusaSlicer — Cut tool.** Prusa's Knowledge Base article documents two cut *modes*, **Planar** and **Dovetail**, and three *connector types*:

- **Plug** — "adds a plug to the side of the cut and subtracts the space for it from the other side"
- **Dowel** — "subtracts the pin from both sides and generates an extra object to print as the connector"
- **Snap** — "Adds a snap-fit connector on one side and subtracts the space to fit it on the other side"

Connector **style, shape, depth, size and rotation** are user-adjustable; a **Tolerance** parameter exists "for better fit of the pins or dovetails"; dovetail mode exposes tail dimensions. Crucially for this design, the user chooses whether the result is two *objects* or one object in two *parts*, and each resulting piece can "keep the current orientation, place the part where the cut was made down on the print surface, or flip the part upside down."
Source: https://help.prusa3d.com/article/cut-tool_1779

I read the implementation to get exact defaults, because the help page does not state them. From `src/slic3r/GUI/Gizmos/GLGizmoCut.hpp` and `.cpp` on PrusaSlicer master:

- modes: `{ "Planar", "Dovetail" }` (a "Grid" mode is present but commented out)
- connector types: `{ Plug, Dowel, Snap }`
- connector **styles**: `{ Prism, Frustum }`; connector **shapes**: `{ Triangle, Square, Hexagon, Circle }`
- defaults: `m_connector_depth_ratio = 3.0`, `m_connector_size = 2.5`, `m_connector_angle = 0`, **`m_connector_depth_ratio_tolerance = 0.1`**, **`m_connector_size_tolerance = 0.0`**
- snap geometry: `m_snap_bulge_proportion = 0.15`, `m_snap_space_proportion = 0.3`, 8 snap regions
- placement options are keyed `"none"` / `"on_cut"` / `"flip"` → "Keep orientation" / **"Place on cut"** / "Flip upside down"
- the tolerance slider is clamped: `max_tolerance_v = min(max_tolerance, 0.5 * mean_size)`
- there are explicit guards `is_outside_of_cut_contour()` and `is_conflict_for_connector()` that reject connectors placed off the cut cross-section or overlapping each other

Sources (read directly):
https://raw.githubusercontent.com/prusa3d/PrusaSlicer/master/src/slic3r/GUI/Gizmos/GLGizmoCut.hpp
https://raw.githubusercontent.com/prusa3d/PrusaSlicer/master/src/slic3r/GUI/Gizmos/GLGizmoCut.cpp

**OrcaSlicer.** OrcaSlicer's own wiki page for the cutting tool is, as of this survey, a one-line stub: "This tool is used to cut 3D models into smaller parts for easier printing or assembly." — and nothing else.
https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer_WIKI/main/print_prepare/prepare_cutting_tool.md (fetched; content is that single sentence)
https://www.orcaslicer.com/wiki/print_prepare/prepare_cutting_tool

The *feature* is nevertheless fully present, inherited from PrusaSlicer. OrcaSlicer's `GLGizmoCut.hpp`/`.cpp` carry byte-identical defaults — `m_connector_depth_ratio{3.f}`, `m_connector_size{2.5f}`, `m_connector_depth_ratio_tolerance{0.1f}`, `m_connector_size_tolerance{0.f}`, `m_snap_bulge_proportion{0.15f}`, `m_snap_space_proportion{0.3f}` — plus `m_connector_types = { "Plug", "Dowel", "Snap" }`, `m_modes = { "Planar", "Dovetail" }`, and the same `Keep orientation / Place on cut / Flip upside down` triple.
https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/src/slic3r/GUI/Gizmos/GLGizmoCut.hpp
https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/src/slic3r/GUI/Gizmos/GLGizmoCut.cpp

**Bambu Studio.** The official wiki documents a planar cut tool plus a **Dovetail mode** with adjustable **Depth, Width, Flap angle and Groove angle**, and an **Adding Connectors** section: "At present, the connectors that can be added are Plug, Dowel and Snap." Cutting produces "multiple objects (default) or a multi-part object", either half can be discarded via Object A / Object B toggles, and post-cut orientation offers **"Keep orientation, Place on cut and Flip."** Bambu explicitly names support reduction as a motivation: "Cutting allows you to reposition parts for more efficient printing, often minimizing or eliminating the need for support structures."
https://wiki.bambulab.com/en/software/bambu-studio/cut-tool (fetched via curl; direct WebFetch returns HTTP 402)

**The one caveat Bambu documents, and it is load-bearing:**

> "After dovetail cutting, a pop-up window may appear to indicate that non-mainfold edges remain after cutting. Click to fix the model according to the prompt, and then slice it."

That is a first-party admission that the slicer's non-planar (dovetail) cut can leave a mesh that is *not* manifold and needs a repair pass. A DeepWiki analysis of the BambuStudio source describes `GLGizmoAdvancedCut` with Plug/Dowel/Snap/Dovetail+Groove connector enums and says the backend uses "CGAL Surface Mesh" infrastructure with `is_closed` checks — this is an AI-generated code wiki, not a Bambu document, so treat as secondary: https://deepwiki.com/bambulab/BambuStudio/7.2-advanced-cutting-tools

**Cura.** UltiMaker Cura has no equivalent interactive cut-with-connectors gizmo comparable to the above; its mesh tools are per-model modifiers/support blockers, not a parting-plane tool with registration features. I could not find an official UltiMaker doc page for a cut tool, and no Cura-native connector generation. (Absence of evidence — flagged in §8.)

**Meshmixer (Autodesk, discontinued but still widely used).** Official Autodesk help for **Plane Cut** documents Cut Type `Cut` / `Slice` / `Slice Groups`, and Fill Type `No Fill` / `Minimal Fill` (constrained Delaunay triangulation) / `Remeshed Fill` / `Fixed Fill`. The key statement about watertightness: **"when you cut a solid, you get a solid"** — filling is automatic by default; the result becomes a shell only if the cut intersects a pre-existing boundary loop. Meshmixer has *no* connector generation; it aligns and separates only.
https://help.autodesk.com/cloudhelp/2019/ENU/MSHMXR/files/GUID-C36CDABA-05F7-44B0-9529-C33D9E435220.htm

**Blender — Bisect** (for completeness, since it is the usual "do it in CAD" answer). Documented options are Plane Point / Plane Normal (numeric), **Fill** ("Create new faces along the cutting plane to cover up any holes left by Clear Inner/Outer"), Clear Inner/Outer, and Axis Threshold ("Any vertices closer to the cutting plane than this threshold will be reused"). Planar only, no connectors, no cut-face-down placement.
https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/bisect.html

### 1.2 The steelman: the exporter should not do this

Stated as strongly as the evidence supports:

1. **Every target printer's own slicer already ships this.** The Bambu A1/P1S/X1C user is in Bambu Studio or OrcaSlicer. Both offer planar *and* dovetail cutting, three connector types, four connector cross-sections, prism/frustum styles, a tolerance slider, and a one-click **"Place on cut"** that does exactly the "print the flat face down" step this design is trying to achieve. All of it is free, interactive, previewable, and undoable.
2. **The slicer cut is watertight-by-construction in the normal (planar) case.** Prusa's help doesn't promise it, but Meshmixer states it explicitly for the equivalent operation and Blender's Fill does the same; PrusaSlicer's gizmo is built on `libslic3r/TriangleMeshSlicer` and produces printable solids in ordinary use.
3. **The user, not the generator, knows their assembly plan.** Cut height, connector count, connector size, tolerance for *their* printer and filament, and whether they want dowels or snaps are all decisions a slicer surfaces interactively. An exporter that bakes a split into the STL removes those choices and produces a file that cannot be un-split.
4. **Splitting in the exporter doubles the artifact surface.** Two files instead of one, plus the obligation to keep them consistent, version them, and validate them — for a capability the downstream tool already has.
5. **The literature agrees the connector is the easy part.** Chopper (§4) explicitly says of glue-only assembly: "Supporting glue would be strictly easier, requiring no modifications to geometry."

### 1.3 The rebuttals, with specifics

1. **Every slicer cut is planar (or a planar cut with a dovetail relief).** PrusaSlicer's `m_modes` are literally `{Planar, Dovetail}`; Orca's are identical; Bambu's wiki opens with "Bambu Studio provides a **planar** cut tool." None of them can route a seam around the void cells of a lattice. If the design's thesis is "cut through the holes, not the struts," no slicer today can express that. This is the single strongest argument *for* exporter-side splitting.
2. **Connector defaults are larger than the available material.** Default connector size is 2.5 mm with depth ratio 3.0 in both PrusaSlicer and OrcaSlicer. The orb's struts are 3 mm wide × 2.4 mm deep. A 2.5 mm connector centred in a 3 mm strut leaves 0.25 mm of wall per side — below one 0.4 mm extrusion. **[derived]** Hydra Research's design rules put minimum printable hole diameter at >Ø2 mm and minimum structural wall at 0.9 mm (2× extrusion width); a 2.5 mm hole plus 0.9 mm walls needs a 4.3 mm strut. The slicer's connector feature is effectively unusable on this geometry at defaults, and the gizmo's own `is_outside_of_cut_contour` / `is_conflict_for_connector` guards will fight the user on a cross-section that is dozens of ~7 mm² disjoint islands.
3. **The default size tolerance is 0.0 mm.** Both PrusaSlicer and OrcaSlicer ship `m_connector_size_tolerance{0.f}` — a nominal-to-nominal fit with no designed clearance. This matches the recurring user reports that Bambu Studio dowels "are too big" / "are slightly too long and do not allow the two cut sections to connect" (Bambu community forum threads surfaced in search; *unverified snippet*).
4. **Bambu's own docs warn the non-planar cut can produce non-manifold edges** (quoted above). A generator that owns the split can assert validity; a slicer cut cannot be asserted about from the generator's side at all.

**Net:** the slicer argument defeats exporter-side splitting *for a planar equatorial cut with pins*. It does not touch a void-following seam, and it does not survive the connector-size arithmetic against a 3 mm strut.

---

## 2. Registration features and FDM fit clearances

### 2.1 What is used

| Feature | Where documented | Notes |
|---|---|---|
| Plug (male boss + matching socket) | PrusaSlicer / Orca / Bambu cut tools | prism or frustum; triangle / square / hexagon / circle cross-section |
| Dowel (separate printed pin, socket both sides) | same | generates a third object to print |
| Snap-fit | same | bulge proportion 0.15, space proportion 0.3 of nominal |
| Dovetail / tongue-and-groove | Bambu wiki (Depth, Width, Flap angle, Groove angle); PrusaSlicer Dovetail mode | "Make a groove in the surface of one part, on the other part, add a tongue that matches the size of the groove" — https://www.3dprintinguk.com/3d-printing-joints/ *(unverified snippet)* |
| Pentagonal prism male/female | Chopper (Luo et al. 2012) — chosen specifically because a non-circular prism "prevents parts from rotating" | see §4 |
| Cube pegs + oversized slots | pychop3d (open-source Chopper implementation) | defaults below |
| Wedged mortise–tenon | Shen, Zhang & Qin 2026, *Progress in Additive Manufacturing* | measured, see §3 |
| Magnets in pockets | community only; no primary engineering source found | see §8 |

### 2.2 Real clearance numbers, and the spread

Sources disagree by roughly **an order of magnitude** (0.0 mm to 1.0 mm designed gap). Reported as found:

- **PrusaSlicer / OrcaSlicer defaults:** size tolerance **0.0 mm**, depth-ratio tolerance **0.1**. Tolerance slider is capped at half the connector's mean size. *(source code, read directly)*
- **pychop3d** (Python implementation of Chopper): `connector_diameter = 5` (mm, side length of cube pegs), **`connector_tolerance = 1`** ("extra side length for the 'slots'"), `connector_spacing = 10`, and a derived `connector_wall_distance = 0.5 × connector_diameter`. A 1 mm slot oversize on a 5 mm peg is a 20 % clearance — far looser than any hand-design guidance below.
  https://github.com/gregstarr/pychop3d (README + `pychop3d/configuration.py`)
- **Prusa Knowledge Base:** "An Original Prusa will be accurate to at least 0.2 mm"; for movable parts, "An initial good measurement for movable parts is at least **0.3 mm**." https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135
- **Hydra Research (printer manufacturer design rules):** "~0.2 mm for loose fit, ~0.1 mm for tight fit"; minimum hole Ø > 2 mm; minimum structural wall 0.9 mm (2× extrusion line width); horizontal-hole offset ≈ 0.3 mm. https://www.hydraresearch3d.com/design-rules
- **Protolabs Network / Hubs, dimensional accuracy:** desktop FDM **± 0.5 % with a ± 0.5 mm floor**; industrial FDM ± 0.15 % with a ± 0.2 mm floor. Note this *floor exceeds* the Prusa and Hydra clearance recommendations — i.e. the machine's own accuracy envelope is as large as the gap you are designing. https://www.hubs.com/knowledge-base/dimensional-accuracy-3d-printed-parts/
- **Bambu community, glue-moat thread:** a 0.2 mm gap recommended, with the poster noting "0.1 mm difference in size could then be too little." https://forum.bambulab.com/t/glue-moat-for-joined-parts/75168
- **3D Print Map:** "a clearance of 0.2 mm per side for sliding fits" *(unverified snippet)*; Unit Convr: "0.2–0.5 mm clearance for small features on hobby FDM printers" *(unverified snippet)*.

**Reading of the spread.** For a *glued, non-moving* registration feature the useful band is **0.1–0.3 mm total diametral clearance**, with 0.2 mm the modal value across independent sources. pychop3d's 1 mm is an outlier appropriate to 5 mm pegs on large parts. The slicers' 0.0 mm default is a genuine defect for FDM and is the likely root of the "dowels don't fit" complaints.

### 2.3 Pin diameter vs wall thickness

- **Protolabs/Hubs:** "Large pins (greater than 5 mm diameter) are printed with a perimeter and infill" while "smaller diameter pins (less than 5 mm diameter) can be made up of only perimeter prints with no infill." So sub-5 mm pins are pure-perimeter objects — their strength is the perimeter shell, not infill. https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/
- **Hydra Research:** minimum printable hole Ø > 2 mm; minimum structural wall 0.9 mm.
- **pychop3d** encodes a rule directly: keep connectors at least **half a connector diameter** away from a wall (`connector_wall_distance = 0.5 × connector_diameter`).

**[derived]** Combining these against the orb: a socket in a 3 mm strut can be at most Ø ≈ 3 − 2×0.9 = **1.2 mm** if you respect Hydra's 0.9 mm wall — which is *below* the 2 mm minimum printable hole. Pin-in-hole registration inside a single 3 mm strut is not obviously feasible. This is a hard finding and should drive the design toward geometry that spans multiple struts (a lip/rabbet along the seam, or a keyed cell boundary) rather than a drilled pin.

### 2.4 How many pins per joint

No primary engineering source found. The consensus in maker-facing guides is **two pins minimum** (one pin leaves a rotational degree of freedom), with the counter-caution that two round pins in round holes bind on assembly unless one hole is slotted — the classic pin-and-diamond-pin / pin-and-slot arrangement from fixture design *(unverified snippet, several guides; the specific quote encountered was "If you were to use two round dowel holes in this situation there is a strong likelihood that when you went to assemble the parts the dowel pins would bind on the dowel holes in the opposite part during assembly")*. **Chopper's** answer to the same problem is different and better documented: use a **non-circular** connector — pentagonal prisms — so a *single* connector constrains rotation.

---

## 3. Bonding and seam geometry

### 3.1 How strong is a glued FDM seam, really

The best-controlled number I found is from an open-access 2026 study that printed identical specimens joined two ways — cyanoacrylate ("SUPER GLUE Instant Adhesive", mating faces lightly abraded and cleaned with IPA) vs. a printed wedged mortise–tenon joint:

| | Tensile strength | Flexural strength | Flexural modulus | Tensile toughness |
|---|---|---|---|---|
| Adhesive (CA) joint | **2.46 ± 1.00 MPa** | **5.157 ± 1.408 MPa** | 374.6 ± 80.4 MPa | 69.2 ± 32.3 J/cm³ |
| Wedged mortise–tenon | **5.16 ± 0.66 MPa** | **8.126 ± 0.370 MPa** | 222.2 ± 12.4 MPa | 4429 ± 556 J/cm³ |

The M–T joint was 57.5 % stronger in bending and vastly tougher; the glued joint was *stiffer* but failed abruptly — "In glued joints, failure is localized at the adhesive bond, where stress concentration leads to abrupt failure." Dimensional deviation of the printed joints was 0.026 mm by 3D scan.
Shen, Zhang, Qin, "Wedged mortise-tenon structure for fixed connections in additive manufacturing assemblies using fused filament fabrication," *Progress in Additive Manufacturing* 11:4025–4041 (2026). https://doi.org/10.1007/s40964-026-01565-3 (open access PDF read directly)

Put that next to the base material. Prusament PLA's own TDS gives **tensile yield 51 ± 3 MPa** for printed specimens (57 ± 1 MPa for the filament) and — the number that matters for a shell printed in layers — **interlayer adhesion 17 ± 3 MPa**.
https://prusament.com/wp-content/uploads/2022/10/PLA_Prusament_TDS_2021_10_EN.pdf (PDF read directly)

**[derived]** A CA-glued seam at ~2.5 MPa is therefore roughly **5 % of printed PLA's tensile strength and ~15 % of its weakest (interlayer) direction**. The seam is not "as strong as the part." It is an order of magnitude weaker, and it fails brittlely.

### 3.2 The contradicting position

Henkel's own data says the opposite for *injection-moulded* ABS: Loctite 401 Prism, 414 Super Bonder, 4307 Flashcure and 3105 Light Cure "created bonds that were **stronger than the ABS substrate**," and for those adhesives the effect of surface roughening could not even be measured because the substrate failed first either way. Loctite also reports surface roughening gave a statistically significant strength increase for Black Max 380 and Depend 330 by "dramatically increasing the number of mechanical interlocking sites."
*Loctite Design Guide for Bonding Plastics, Volume 6* (2011), ABS section. https://www.ellsworth.com/globalassets/literature-library/manufacturer/henkel-loctite/henkel-loctite-design-guide-plastic-bonding.pdf (PDF read directly)

Maker-facing sources echo the Loctite position for prints — "In many cases, the PLA itself broke rather than the adhesive bond" *(unverified snippet, MakerBuildit)*. **The disagreement is real and I am not resolving it**, but it is explainable: Loctite's substrate-failure result is on *solid moulded* ABS coupons with generous lap area, whereas the 2026 FFF study measured a *joint-limited* geometry. Loctite itself supplies the reconciliation: "The lower tensile strengths of plastics make it common to create bonded joints that are stronger than the plastic itself… Because of the large joint overlap, the substrate will fail before the bond." The variable is **bond area**, not adhesive chemistry.

Note also that the Loctite guide is from 2011 and covers ABS, ASA, PMMA, acetal, nylon etc. — **it contains no PLA or PETG section at all.** Direct manufacturer data on bonding PLA is a gap.

### 3.3 Does a glued seam need surface area? — yes, and Loctite is specific about *which* area

Loctite's "Adhesive Joint Design" chapter gives four design rules, read verbatim from the PDF:

- **Maximize shear / minimize peel and cleavage** — "these bonds do not resist stress very well. The stress is located at one end of the bond line. Whereas, in the case of shear, both ends of the bond resist the stress."
- **Maximize compression / minimize tensile** — "In most adhesive films, the compressive strength is greater than the tensile strength."
- **Joint width more important than overlap** — "As a general rule, increase the joint **width** rather than the overlap area ('wider is better')." And: "if the overlapping length is greatly increased, there is little, if any, change in the bond strength. The contribution of the ends is not increased."
- A **scarf joint** ("an angular butt joint. Cutting the joint at an angle increases the surface area") is listed as a way to get area out of what would otherwise be a butt joint.

Loctite also publishes a **bondline-gap → stress-concentration** table (constants: adhesive modulus 100,000 psi, overlap 0.5 in):

| Bondline gap (in) | Max stress ratio |
|---|---|
| 0.001 | 18.40 |
| 0.002 | 13.00 |
| 0.005 | 8.31 |
| 0.010 | 5.93 |
| 0.020 | 4.25 |
| 0.040 | 3.06 |

This is counter-intuitive and worth restating: **a thicker glue line lowers peak stress concentration at the joint ends.** A zero-clearance butt face pressed metal-tight is the *worst* case in this table. Loctite also flags cyanoacrylate's key limitation as "**limited gap cure**" — CA does not cure across a thick gap — so the two constraints (want some bondline, CA can't bridge much) pull against each other and favour epoxy or an acrylic if the seam gap is large.

**Implication for a lattice seam.** A planar equatorial cut through struts produces a set of tiny butt faces of 3 mm × 2.4 mm = **7.2 mm² each [derived]**. A butt joint is the geometry Loctite's rules point away from; the fix is either a *lip/rabbet* (converting butt → lap, and increasing the *width* dimension Loctite says matters most) or a *scarf* (angled cut).

### 3.4 Solvent welding, mechanical welding, 3D pen

- **Solvent welding (ABS/ASA, acetone or MEK)** is the standard way to get an effectively monolithic seam; community sources describe "invisible seams" *(3dx.info, unverified snippet)*. There is a specific measurement — Tuazon, Espino & Dizon, "Lap Shear Strength Assessment of Acetone Welded 3D-Printed ABS Polymer," *Materials Science Forum* (2023) — but I could not obtain the MPa values; only the citation is confirmed. https://www.semanticscholar.org/paper/Lap-Shear-Strength-Assessment-of-Acetone-Welded-ABS-Tuazon-Espino *(metadata only, values not verified)*. **Solvent welding is not available for PLA**, which is not attacked by acetone.
- **Friction / friction-stir / spin welding** is a documented route specifically framed as beating the bed-size limit: Kumar et al., "Investigations on friction stir spot welding to overcome bed size limits of material extrusion (MEX) 3D printers," *Rapid Prototyping Journal* (2023), https://doi.org/10.1108/rpj-01-2023-0030; and "Investigations on the effect of Spin Friction Welding parameters on joint strength and cylindricity of similar/dissimilar MEX 3D printed parts," *Journal of Advanced Joining Processes* (2024), https://doi.org/10.1016/j.jajp.2024.100208 *(abstract-level via Semantic Scholar; full texts not read)*. Neither is plausible on a 3 mm lattice strut.
- **Survey of the whole space:** Kumar & Singh, "An overview on joining/welding as post-processing technique to circumvent the build volume limitation of an FDM-3D printer," *Rapid Prototyping Journal* (2021), https://doi.org/10.1108/RPJ-10-2020-0265 — classifies adhesive bonding, mechanical interlocking, fastening, big-area AM, and welding (friction stir, spin, microwave, ultrasonic) with pros/cons per method. Abstract verified via Semantic Scholar API; full text not read.
- **Joint-design-aware adhesive study:** Kumar, Singh et al., "Adhesive bonding of similar/dissimilar three-dimensional printed parts (ABS/PLA) considering joint design, surface treatments, and adhesive types," *IMechE Part C* (2022), https://doi.org/10.1177/09544062221089849. Abstract (verified): tested **lap, scarf and stepped** joint designs × epoxy / cyanoacrylate / polyurethane × sanding / vapour / plasma treatment. Parameter significance ranked **material type > joint configuration > adhesive type > surface pre-treatment**, with the best combination being ABS+ABS, **stepped** configuration, plasma-treated, Loctite adhesive. That ranking is directly useful: *the joint geometry mattered more than which glue you use.*
- **3D-pen / filament welding** appears only in maker media, no measurements found *(unverified snippets)*.

### 3.5 Glue relief / squeeze-out — the specific thing asked about

This is real and has a documented design. The Bambu Lab community "Glue 'moat' for joined parts" thread describes a shallow recessed channel set back from the seam edge so excess adhesive flows inward instead of out onto the visible surface. Dimensions proposed: **1 mm in from the edge, 2 mm wide, 1 mm deep, with a fillet to prevent overhang issues**, plus a **0.2 mm** fit gap. The originator's result after testing: "I can put enough glue to ensure I have a really good seal and glue coverage without worrying about it leaking out the sides… I've done a few more tests and it works very well" with "not even one small leak."
https://forum.bambulab.com/t/glue-moat-for-joined-parts/75168

Community consensus is that over-gluing is the dominant assembly failure: "The most common mistake people make… is using too much glue. We have seen many prints ruined by excessive squeeze-out" *(3dfilamentinsider.com, unverified snippet)*.

**Note the scale problem [derived]:** a 2 mm wide × 1 mm deep moat set 1 mm from the edge requires ≥ 4 mm of face width. The orb's struts are 3 mm. A per-strut glue moat does not fit. A moat is only available if the seam runs along a *lip* that is wider than a strut.

---

## 4. Split-plane placement on a patterned lattice (+ automated part decomposition literature)

### 4.1 The academic core: Chopper

**Luo, Baran, Rusinkiewicz & Matusik, "Chopper: Partitioning Models into 3D-Printable Parts," ACM TOG 31(6), Article 129 (SIGGRAPH Asia 2012).** DOI 10.1145/2366145.2366148. Project page https://gfx.cs.princeton.edu/pubs/Luo_2012_CPM/index.php ; full text read from the MIT author's-final-manuscript copy mirrored in the pychop3d repo (handle http://hdl.handle.net/1721.1/90389).

Verbatim, the objectives Chopper optimises:

> • **Printability**: the parts must fit inside the working volume.
> • **Assemblability**: it must be possible to put parts together (without interference) into a finished model.
> • **Efficiency**: the partition should avoid small parts and, in general, minimize the number of required sub-volumes.
> • **Connector feasibility**: each interface must be large enough to admit connectors, protrusions, or other aids to assembly.
> • **Structural soundness**: parts should not have thin slivers, and seams should be away from areas of high mechanical stress.
> • **Aesthetics**: seams should be unobtrusive, detracting from appearance as little as possible, and should follow the natural symmetries of the model.

Connectors, verbatim:

> "Chopper can support a number of possible connector designs. We have considered connectors that snap together, require screws, or even glue. For our experiments, we simply use **pentagonal prisms**, with a male prism extruding from the surface of one part and fitting into a female prism on another part. **Supporting glue would be strictly easier, requiring no modifications to geometry.**"

and

> "Depending on their design, the connectors may provide sufficient structural strength to hold parts together, or may merely serve as **guides for assembly, with glue used to permanently attach parts**."

Two things matter enormously for this design doc:

1. **Chopper is planar-only.** It searches a **BSP tree** of planar cuts. The paper states the reason explicitly: "Finding a set of cuts leading to an assemblable partition is difficult (**since these cuts may have to be non-planar**) and impractical to do every time we evaluate a covering's quality." So the canonical paper in this area *considered* non-planar cuts and rejected them on tractability grounds, not on merit.
2. **"Aesthetics: seams should be unobtrusive… and should follow the natural symmetries of the model"** is a named, first-class objective in the literature. A seam that follows the lattice's cell boundaries is precisely "following the natural symmetries of the model." The design's core intuition has an academic name.

**pychop3d** — open-source Python reimplementation, defaults read directly: cube pegs `connector_diameter = 5`, `connector_tolerance = 1`, `connector_spacing = 10` (minimum distance between adjacent connectors), `plane_spacing = 20`, `beam_width = 5`, objective weights including a `connector` term, `connector_collision_penalty = 1e10`, simulated annealing for connector placement (100,000 iterations). https://github.com/gregstarr/pychop3d

### 4.2 Successors and neighbours

Retrieved from the Chopper citation graph (Semantic Scholar API) and verified at abstract level:

- **Hu, Li, Zhang, Cohen-Or, "Approximate Pyramidal Shape Decomposition," ACM TOG 33(6) (SIGGRAPH Asia 2014).** DOI 10.1145/2661229.2661244. PDF: https://www2.cs.sfu.ca/~haoz/pubs/hu_siga14_pym.pdf. Decomposes a shape into *pyramidal* parts — parts with "a flat base with the remaining boundary forming a height function over the base" — which are optimal for moulding, casting and **layered 3D printing** because each part prints support-free from its base. This is the closest published work to the design's actual goal (support-free parts), and it is a *stronger* criterion than "fits in the build volume." (The fetched summary asserts it "outperforms Chopper" with "significantly fewer decomposed components"; I read this via an automated summary of the PDF rather than the results table, so treat the comparative claim as indicative only.)
- **Chen, Zhang, Lin, Hu, Li, Huang, Benes, Cohen-Or, Chen, "Dapper: decompose-and-pack for 3D printing," ACM TOG 34(6) (SIGGRAPH Asia 2015).** DOI 10.1145/2816795.2818087. Adds *packing* into the build volume as a joint objective with decomposition. (Metadata verified via Semantic Scholar; abstract elided by publisher, full text not read.)
- **Alderighi, Malomo, Bickel, Cignoni, Pietroni, "Volume decomposition for two-piece rigid casting," ACM TOG 40(6) (2021).** DOI 10.1145/3478513.3480555. Abstract verified: decomposes a volume into parts "that can be represented by **two opposite height fields**," using a precomputed per-point accessibility signal over a set of extraction directions. This is the most directly transferable formalism for a *two-piece* split of an orb: "two opposite height fields" is the exact mathematical condition under which two halves both print without undercuts.
- **VASCO: Volume and Surface Co-Decomposition for Hybrid Manufacturing**, ACM TOG (2023), DOI 10.1145/3618324.
- **"Strength-enhanced volume decomposition for multi-directional additive manufacturing," *Additive Manufacturing* (2023)**, DOI 10.1016/j.addma.2023.103529.
- **"Volume decomposition for multi-axis support-free and gouging-free printing based on ellipsoidal slicing," *CAD* (2022)**, DOI 10.1016/j.cad.2021.103135.

### 4.3 Does anyone do a wandering, non-planar, cell-following cut?

**Searching for this is actively hostile**, and that is itself a finding worth recording:

- **"non-planar cut"** returns almost exclusively **non-planar *slicing*** (curved toolpaths, wave-shaped layers) — e.g. a fully automatic non-planar slicing algorithm in *Additive Manufacturing* (https://www.sciencedirect.com/science/article/pii/S2214860423001549), https://github.com/Monta3D/SelectiveNonPlanarSlicer, https://xyzdims.com/2022/03/26/3d-printing-slicing-with-non-planar-geometries/. Completely different problem. If the design doc uses the phrase "non-planar cut," readers will misparse it. Prefer **"seam-following split"**, **"cell-boundary split"**, or the paper's own vocabulary, **"non-planar cuts"** used explicitly in the Chopper sense.
- **"seam-aware decomposition"** and **"shape-aware part decomposition"** return **zero results** on both DuckDuckGo and a Semantic Scholar title/abstract search. These are not established terms of art. Do not cite them as if they were.
- The nearest established terms are **"partitioning models into 3D-printable parts" (Chopper)**, **"pyramidal shape decomposition"**, and **"volume decomposition"**.

**Practical prior art (weak, community-level):** openwork/voronoi lamp spheres are routinely split into halves and glued. One MakerWorld voronoi sphere lamp explicitly describes designing the split so that "the Voronoi sphere cover seam [runs] sideway along the lamp and not be as visible," with two halves glued together using pegs for alignment (https://makerworld.com/uk/models/1396345-led-desk-lamp-modern-voronoi-sphere — *unverified snippet; the page returns HTTP 403 to automated fetch*). Thingiverse voronoi lamps by Hultis (thing:3147169) and leander_ow (thing:6891972) describe splitting into multiple parts and gluing *(unverified snippets)*. **I found no example, commercial or hobby, of a split that provably routes around cells rather than through struts.** That is a genuine gap and probably a genuine novelty claim — but it is a claim resting on absence of evidence, which is weaker than the design doc will want. Flagged in §8.

### 4.4 Synthesis for the design decision

The literature supports the design's instinct on *aesthetics* (Chopper names seam unobtrusiveness and symmetry-following as an objective) and on *support-freedom* (Hu et al.; Alderighi et al.'s two-opposite-height-fields criterion). It weighs against it on *tractability* (Chopper explicitly avoided non-planar cuts as impractical) and on *bond area* (§3: a void-following seam severs fewer struts, therefore has *less* glue area, not more — the aesthetic win and the structural win point in opposite directions). **[derived]** A planar equatorial cut through struts gives many small butt faces; a cell-following seam gives *zero* butt faces and must instead rely on interlocking geometry along the seam. These are qualitatively different joints, not two versions of the same joint.

---

## 5. Printing a hemispherical lattice cut-face-down

### 5.1 Does it solve the overhang problem?

**Partly — and the failure mode moves rather than disappearing.**

The purely geometric argument is favourable: for a dome resting on its flat face, each successive layer is *smaller* than the one below, so no layer overhangs its predecessor at the macro scale. Every source that discusses domes recommends flat-side-down: "To 3D print a dome, you want to keep the flat side down on the bed, while the round side will be built on top," and for larger structures "you may need to slice them in half and then glue them together once they are printed" (https://www.3dprinterly.com/how-to-3d-print-a-dome-or-sphere-without-supports/). Bambu's cut-tool wiki names the same rationale.

But the *surface tilt angle* still degrades toward the pole, and that is what governs support. Bambu Lab's own overhang documentation is explicit about the convention and the threshold:

> "Generally, when the overhang tilt angle is smaller than 45°, it is recommended to add supports; when it is larger than 45°, no support is needed. Note: **The overhang angle mentioned here refers to the angle formed between the inclined surface of the model and the heatbed surface.** In contrast, the overhang threshold refers to the proportion of unsupported extrusion width within an extrusion line, which is not the same concept."
> https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang

**[derived]** On a hemisphere of R = 60 mm sitting cut-face-down, the surface-to-bed angle is 90° at the rim and 0° at the pole; it passes through 45° at 45° latitude, i.e. at height z = R·sin45° = **42.4 mm**. Everything above that — the top **17.6 mm** of the 60 mm dome, and **29.3 %** of the hemisphere's surface area (2πR²(1 − sin45°) / 2πR²) — sits below the 45° threshold. So *roughly the top third of each hemisphere is in the "add supports" regime by Bambu's own rule.*

Bambu's forum post on dome structures describes exactly this failure and its fixes:

> "the overhang angle in the inner middle section gets steeper" while "the overlapping area between the layers becomes smaller" → "stringing and line detachment," potentially forming holes on the top surface.

with three remedies: flatten the dome's inner top surface in CAD; use **support painting** at a 30° overhang threshold so supports go only where needed; and reduce layer height (uniformly or adaptively) to improve cooling in the overhang region.
https://forum.bambulab.com/t/3-ways-to-reduce-line-detachment-in-dome-structures/192368

A Reddit r/3Dprinting answer to "Can I print half a dome without supports?" states the mechanism as "near the top of the dome the slope exceeds max overhang angle before the gap is bridged. With nothing to support the semicircular 'balcony', it'll droop" *(unverified snippet)*.

### 5.2 The extra problem specific to an openwork lattice: bridging, not overhang

A solid dome's near-pole layers rest on the layer below. **An openwork lattice's near-pole struts run nearly horizontally across voids** — they are *bridges*, and bridge guidance is much stricter than overhang guidance:

- **Protolabs/Hubs:** "sagging or marks from support material are to some extent always present unless the bridge is **less than 5 mm**." https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/
- **Hydra Research:** horizontal bridges without support should stay under **10 mm**. https://www.hydraresearch3d.com/design-rules
- **Prusa Knowledge Base (bridging):** gives no hard number — "the best results are achieved only over short distances" because cooling is essential; recommends lowering bridge flow ratio for the first bridging layer, reducing bridge speed, increasing cooling, and adjusting bridging angle. User comments in the thread report struggling at 30 mm and failing at 150 mm. https://help.prusa3d.com/article/bridging_1802

**[derived]** If the lattice's cell openings near the pole are larger than ~5–10 mm across, the top cap will require support regardless of how the hemisphere is oriented. The design needs the actual near-pole cell span as a number; it is not in the brief.

### 5.3 The 45° rule and where sources disagree

Genuine spread, all fetched:

| Source | Position |
|---|---|
| Protolabs / Hubs | "an overhang can usually be printed up to **45°** without compromising quality. At 45°, the newly printed layer is supported by 50 % of the previous layer." |
| Prusa Knowledge Base | "A 3D printer can cleanly print overhanging structures with an angle between **45 and 60 degrees**" depending on nozzle and settings; MK4S / CORE One "can handle overhangs of up to **75°** without supports." |
| Bambu Lab wiki | support below **45°** surface-to-bed tilt |
| **UltiMaker Cura, `fdmprinter.def.json`** | `support_angle` **default = 50°** — "The minimum angle of overhangs for which support is added. At a value of 0° all overhangs are supported, 90° will not provide any support." (Also from the same file: `support_z_distance` 0.1 mm, `support_brim_enable` **true** by default, `line_width` 0.4, `wall_thickness` 0.8.) https://raw.githubusercontent.com/Ultimaker/Cura/main/resources/definitions/fdmprinter.def.json |
| Hydra Research | avoid unsupported overhangs exceeding **50° from vertical**, "though some modern printers handle up to 70°" |

Note the **convention clash**: Prusa/Bambu/Hubs measure from the bed/horizontal; Hydra Research measures **from vertical**; Cura's `support_angle` is measured such that 90° means no support. These are not the same 45. A design doc quoting "the 45° rule" must state the reference axis.

### 5.4 Bed adhesion of a thin, interrupted lattice rim

No source gives a minimum first-layer contact area in mm². What all of them say is: expand the footprint.

- **Prusa Knowledge Base, Skirt and Brim:** brim "increases the surface area of the first layer," is for "printing tall objects with a small base" or "multiple small objects at once," recommends "at least a **3 mm** brim to increase the adhesion," offers Outer brim only / Inner brim only / both, and a "Brim separation gap" for easier removal. https://help.prusa3d.com/article/skirt-and-brim_133969
- **Cura** enables `support_brim_enable` by default.
- **Protolabs/Hubs** independently recommends "include a **45° chamfer or radius on all edges touching the build plate**" — which for a hemisphere rim would mean a small flare at the equator.

**[derived]** The orb's hemisphere rim is not a ring — it is a *ring of disjoint islands*, one per severed strut, each ~3 mm × 2.4 mm ≈ 7.2 mm². For a 120 mm sphere the equatorial circumference is ~377 mm; if the pattern severs ~20 struts, total first-layer contact is ~144 mm², spread over 20 separate islands each smaller than a 4 mm square. That is a first-layer situation the brim guidance was written for, and **"Outer brim only" would not connect the islands** — inner+outer brim, or a printed sacrificial raft/tab ring, is the relevant lever. If instead the seam follows cell boundaries, the first layer is a *wandering non-planar rim* that does not lie in the bed plane at all, and the hemisphere cannot rest flat — which is a decisive practical objection to the cell-following cut and should be stated plainly in the design doc.

---

## 6. Validating an open (manifold-with-boundary) mesh

### 6.1 What the libraries actually assert

- **trimesh** — `is_watertight`: "Check if a mesh is watertight by making sure **every edge is included in two faces**." `is_winding_consistent`: "A mesh with consistent winding has each shared edge going in an opposite direction from the other in the pair." `is_volume`: "Check if a mesh has all the properties required to represent a valid volume, rather than just a surface. These properties include being **watertight, having consistent winding and outward facing normals**." `euler_number` is computed as `referenced_vertices − len(edges_unique) + len(faces)` and the docstring warns "In order to guarantee correctness, this should be called after `remove_unreferenced_vertices`."
  https://trimesh.org/trimesh.base.html and https://github.com/mikedh/trimesh/blob/main/trimesh/base.py
  Relevant to the split itself: `trimesh.intersections.slice_mesh_plane(mesh, plane_normal, plane_origin, cap=False, ...)` — "`cap : bool` — If True, cap the result with a triangulated polygon." So trimesh will *optionally* close the cut; with `cap=False` you get an honest manifold-with-boundary. https://github.com/mikedh/trimesh/blob/main/trimesh/intersections.py
- **libigl** — `igl::is_edge_manifold`: "Check if the mesh is edge-manifold (**every edge is incident on one face (boundary) or two oppositely oriented faces**)." This is the precise definition you want: it *admits* boundary edges. `igl::is_vertex_manifold`: "only checks whether the faces incident on each vertex form exactly one connected component." `igl::boundary_loop`: "Compute list of **ordered boundary loops** for a manifold mesh," returning `L[i] = ordered list of boundary vertices in loop i`. `igl::boundary_facets` extracts boundary edges. https://github.com/libigl/libigl/tree/main/include/igl
- **CGAL Polygon Mesh Processing** defines a polygon mesh as "a consistent and orientable surface mesh, that **can have one or more boundaries**," where each edge "is shared by two faces (**including the null face for boundary edges**)," and requires only that "a polygon mesh is considered to have the topology of a 2-manifold" — a *combinatorial* requirement that does not exclude self-intersection or degeneracy. https://doc.cgal.org/latest/Polygon_mesh_processing/index.html . CGAL also ships `stitch_borders` for rejoining split boundaries: https://github.com/CGAL/cgal/blob/master/Polygon_mesh_processing/include/CGAL/Polygon_mesh_processing/stitch_borders.h
- **MeshLab** — its "Compute Topological Measures" filter emits exactly the fields you'd want as assertions: `vertices_number`, `edges_number`, `faces_number`, `unreferenced_vertices`, **`boundary_edges`**, `connected_components_number`, `is_mesh_two_manifold`, `non_two_manifold_edges`, `non_two_manifold_vertices`, and — **only if the mesh is 2-manifold** — `number_holes` and **`genus`**; otherwise both are set to −1 with the log "Genus is undefined (non 2-manifold mesh)". https://github.com/cnr-isti-vclab/meshlab/blob/main/src/meshlabplugins/filter_measure/filter_measure.cpp
- **manifold (elalish)** — requires manifold input: "you'll get an error status if the imported mesh isn't manifold"; provides a `Merge` function for slightly non-manifold input; promises "guaranteed manifold output without caveats or edge cases." Its documentation does **not** state whether meshes with boundary are accepted, so do not assume they are. It also carries a warning directly relevant to STL export: "**when saving a manifold mesh to STL there is no guarantee that the re-imported mesh will still be manifold, as the topology is lost**." https://github.com/elalish/manifold and https://manifoldcad.org/docs/html/index.html

### 6.2 The correct standing assertion

Assemble the above into a precise statement. A half is valid iff:

1. It is **2-manifold with boundary**: every edge is incident on exactly one face (a border edge) or exactly two oppositely-oriented faces (libigl's `is_edge_manifold` definition). Equivalently: `non_two_manifold_edges == 0` and `non_two_manifold_vertices == 0` in MeshLab's terms.
2. Its **winding is consistent** and normals point outward (trimesh `is_winding_consistent`; part of `is_volume`).
3. Its **border edges form closed loops** — `igl::boundary_loop` returns *b* loops with no dangling edges. `boundary_edges > 0` (a half is not watertight, by construction; `trimesh.is_watertight` must be asserted **False**, and asserting it True is a bug).
4. **The two halves' boundary loops are identical as point sets and opposite in orientation**, so `stitch_borders` (or any weld) closes them without new geometry.

Then, and only then, re-closing yields the original watertight solid.

### 6.3 The invariant that actually catches errors

Euler characteristic is additive: **χ(A ∪ B) = χ(A) + χ(B) − χ(A ∩ B)** (Wikipedia, *Euler characteristic*, https://en.wikipedia.org/wiki/Euler_characteristic). The two halves intersect in *b* circles, and a circle has χ = 0. Therefore:

> **χ(upper half) + χ(lower half) = χ(original closed orb).**

This is a cheap, exact, geometry-independent regression test on the split, and it is stronger than checking each half in isolation. Also standard: a closed orientable surface of genus *g* has χ = 2 − 2*g*; a sphere has χ = 2, a disc has χ = 1; a genus-*g* surface with *b* boundary components has **χ = 2 − 2g − b** (this last form is standard but Wikipedia states it only implicitly — derived from "removing open discs from a closed surface creates boundary components").

### 6.4 A correction the design doc probably needs

**[derived, important]** The brief says the generator "asserts its STL is watertight." If any assertion also fixes χ = 2 or genus 0, **it is wrong for a pierced lattice orb.** A spherical shell has two boundary spheres (χ = 4). Each cell pierced through the shell removes a disc from each sphere and glues in a tube: the first piercing merges the two spheres into one connected genus-0 surface (χ = 2), and each subsequent piercing adds a handle. For *n* pierced cells the resulting closed surface has **χ = 4 − 2n**, i.e. **genus n − 1**. For an orb with, say, 60 pierced cells, χ = −116 and genus 59. The correct standing assertion for the whole orb is therefore: *closed (every edge in exactly two faces), consistent winding, positive volume, one connected component* — **not** any particular χ or genus. MeshLab's behaviour of reporting genus only after confirming 2-manifoldness is the right ordering to copy.

---

## 7. Numbers table

Every quantitative claim found, with source and spread. "V" = fetched and read; "S" = search-result snippet only.

| Quantity | Value | Source | V/S |
|---|---|---|---|
| PrusaSlicer/Orca connector size (default) | **2.5** (mm) | `GLGizmoCut.hpp`, both projects | V |
| PrusaSlicer/Orca connector depth ratio | **3.0** | same | V |
| PrusaSlicer/Orca connector **size tolerance** | **0.0 mm** | same | V |
| PrusaSlicer/Orca connector depth-ratio tolerance | **0.1** | same | V |
| PrusaSlicer/Orca snap bulge / space proportion | **0.15 / 0.30** | same | V |
| Tolerance slider max | min(max_tolerance, **0.5 × mean size**) | `GLGizmoCut.cpp` | V |
| pychop3d connector peg (cube side) | **5 mm** | pychop3d `configuration.py` | V |
| pychop3d slot oversize (`connector_tolerance`) | **1 mm** (20 % of peg) | same | V |
| pychop3d min connector spacing | **10 mm** | same | V |
| pychop3d connector-to-wall distance | **0.5 × connector diameter** | same | V |
| Prusa: printer accuracy | "at least **0.2 mm**" | help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135 | V |
| Prusa: clearance for movable parts | "at least **0.3 mm**" | same | V |
| Hydra Research: tight fit / loose fit | **0.1 mm / 0.2 mm** | hydraresearch3d.com/design-rules | V |
| Hydra Research: min wall | **0.9 mm** (2× extrusion width) | same | V |
| Hydra Research: min hole Ø | **> 2 mm** | same | V |
| Hydra Research: max unsupported bridge | **< 10 mm** | same | V |
| Hydra Research: overhang limit | **50° from vertical** (some printers 70°) | same | V |
| Hubs/Protolabs: max bridge before sag | **< 5 mm** | hubs.com/knowledge-base/how-design-parts-fdm-3d-printing | V |
| Hubs/Protolabs: overhang limit | **45°** ("supported by 50 % of the previous layer") | same | V |
| Hubs/Protolabs: pin infill threshold | **5 mm** Ø (below → perimeters only, no infill) | same | V |
| Hubs/Protolabs: base-edge treatment | **45° chamfer or radius** on all bed-contacting edges | same | V |
| FDM dimensional accuracy, desktop | **± 0.5 %, floor ± 0.5 mm** | hubs.com/knowledge-base/dimensional-accuracy-3d-printed-parts | V |
| FDM dimensional accuracy, industrial | **± 0.15 %, floor ± 0.2 mm** | same | V |
| Prusa: printable overhang range | **45–60°**; MK4S/CORE One to **75°** | help.prusa3d.com/.../164135 | V |
| Bambu: support threshold | surface-to-bed tilt **< 45° → add supports** | wiki.bambulab.com/.../overhang | V |
| Bambu: overhang temp/cooling fix (PLA) | nozzle → **~205 °C**, overhang fan **100 %**, −5 to −10 °C steps | same | V |
| Bambu: dome support-paint threshold suggested | **30°** | forum.bambulab.com/t/.../192368 | V |
| Cura `support_angle` default | **50°** | Cura `fdmprinter.def.json` | V |
| Cura `support_z_distance` default | **0.1 mm** | same | V |
| Cura `line_width` / `wall_thickness` defaults | **0.4 mm / 0.8 mm** | same | V |
| Prusa: minimum useful brim | **≥ 3 mm** | help.prusa3d.com/article/skirt-and-brim_133969 | V |
| Glue moat geometry | **1 mm inset, 2 mm wide, 1 mm deep, filleted**; **0.2 mm** fit gap | forum.bambulab.com/t/glue-moat-for-joined-parts/75168 | V |
| CA-glued FFF joint, tensile | **2.46 ± 1.00 MPa** | Shen et al. 2026, Table 4 | V |
| CA-glued FFF joint, flexural | **5.157 ± 1.408 MPa** | Shen et al. 2026, Table 5 | V |
| Wedged mortise–tenon joint, tensile | **5.16 ± 0.66 MPa** | same | V |
| Wedged mortise–tenon joint, flexural | **8.126 ± 0.370 MPa** (+57.5 % vs glue) | same | V |
| M–T vs glue tensile toughness | **4429 vs 69 J/cm³** (64×) | same | V |
| M–T printed dimensional deviation | **0.026 mm** (3D scan, C2M) | same | V |
| Prusament PLA, printed tensile yield | **51 ± 3 MPa** | Prusament PLA TDS (ISO 527-1) | V |
| Prusament PLA, filament tensile yield | **57 ± 1 MPa** | same | V |
| Prusament PLA, **interlayer adhesion** | **17 ± 3 MPa** | same | V |
| Loctite bondline gap → stress ratio | 0.001″ → **18.40**; 0.005″ → 8.31; 0.010″ → 5.93; 0.040″ → **3.06** | Loctite Design Guide for Bonding Plastics v6, p.81 | V |
| Loctite overlap length → stress ratio | 1.000″ → 22.50; 0.500″ → 13.00; 0.250″ → 7.17; 0.125″ → **3.78** | same | V |
| Loctite: CA on ABS | Loctite 401/414/4307/3105 gave bonds **stronger than the ABS substrate** | same, ABS section | V |
| Chopper connector geometry | **pentagonal prisms**, male/female | Luo et al. 2012 §3.2.2 | V |
| Sliding-fit clearance | **0.2 mm per side** | 3dprintmap.com | S |
| Hobby-FDM small-feature clearance | **0.2–0.5 mm** | unitconvr.com | S |
| **[derived]** Butt-face area per severed strut | **7.2 mm²** (3 mm × 2.4 mm) | own arithmetic | — |
| **[derived]** Hemisphere area below 45° tilt | **29.3 %** of surface; top **17.6 mm** of a 60 mm dome | own arithmetic | — |
| **[derived]** Equatorial circumference | **~377 mm** (πD, D = 120 mm) | own arithmetic | — |
| **[derived]** Max socket Ø in a 3 mm strut at 0.9 mm walls | **1.2 mm** — below the 2 mm min printable hole | own arithmetic | — |
| **[derived]** Orb Euler characteristic with *n* pierced cells | **χ = 4 − 2n**, genus **n − 1** | own derivation | — |

---

## 8. What the survey could NOT settle

Ordered by how much a physical test print would resolve them.

1. **Does the top ~30 % of a *lattice* hemisphere actually need support?** All the overhang guidance is written for solid surfaces. The 45°-tilt rule says yes; the "each layer is smaller than the last" argument says no; the real answer depends on the near-pole *cell span*, which is a bridging problem with a 5 mm (Hubs) to 10 mm (Hydra) to "no number, it depends on cooling" (Prusa) limit. **No source addresses openwork shells specifically.** → **Print one hemisphere, no supports, and photograph the top 20 mm.**
2. **Does an interrupted rim of ~20 islands of ~7 mm² each stick to the bed?** No source gives a minimum first-layer area, and brim guidance assumes a continuous outline. Whether "outer brim only," "inner and outer brim," or a sacrificial tie-ring is needed is untested. → **Test print: first layer only, both brim modes.**
3. **What is the actual butt-joint strength of CA on a 7.2 mm² PLA face?** The one good measurement (2.46 MPa tensile) is on a different, larger geometry. Loctite's data says CA can exceed the substrate on ABS with generous lap area, and Loctite's own stress tables say the *geometry* is the variable. Nobody has measured a CA butt joint on a 3 mm printed strut. → **Test coupon: two struts, butt-glued, pull to failure.**
4. **Whether a cell-following seam is even placeable on a bed.** A wandering seam does not lie in a plane, so the hemisphere cannot rest cut-face-down. Nothing in the literature addresses this; Chopper explicitly declined to pursue non-planar cuts. This may be a fatal objection to the design's headline idea, or may be resolvable with a small planar flat at the rim — no source helps.
5. **Whether anyone has ever shipped a void-following split.** I found voronoi-sphere lamps split into glued halves, and one that positions the seam for visual reasons, but nothing that demonstrably routes around cells rather than through struts. The novelty claim rests on **absence of evidence**, which is weak. A deeper search of Printables/Thingiverse/MakerWorld model pages (which block automated fetching — MakerWorld returned HTTP 403) would be needed to firm this up.
6. **Cura's cut/mesh-tool capability.** I found no official UltiMaker documentation of a plane-cut-with-connectors feature and no evidence one exists. I cannot assert its absence from the evidence gathered.
7. **PLA-specific adhesive manufacturer data.** The Loctite Design Guide (v6, 2011) has sections for ABS, ASA, PMMA, acetal, nylon and more — **and none for PLA or PETG**. Every PLA adhesive number in this survey is from academic papers or community testing, not from an adhesive manufacturer.
8. **Solvent-weld strength numbers for ABS prints.** The Tuazon/Espino/Dizon lap-shear paper exists and is correctly cited, but I could not obtain its MPa values. Moot for PLA anyway (acetone does not attack PLA).
9. **Magnet pocket tolerances.** Only community forum guidance found; no manufacturer or engineering source. Also probably irrelevant at 3 mm strut scale.
10. **How many severed struts an equatorial plane actually crosses** on this specific pattern. Every bond-area estimate in §3 and §5 assumes ~20; the real number comes from the generator, not from any source, and changes the conclusions proportionally.
11. **Whether PrusaSlicer/OrcaSlicer's planar cut is guaranteed to leave watertight halves.** Prusa's help page does not say. Meshmixer and Blender both document auto-fill for the equivalent operation. Bambu documents that its *dovetail* cut can leave non-manifold edges. The planar case is probably fine but is not *documented* as fine anywhere I could find.

---

### Source list

**Slicer / CAD primary**
1. https://help.prusa3d.com/article/cut-tool_1779
2. https://github.com/prusa3d/PrusaSlicer/blob/master/src/slic3r/GUI/Gizmos/GLGizmoCut.hpp
3. https://github.com/prusa3d/PrusaSlicer/blob/master/src/slic3r/GUI/Gizmos/GLGizmoCut.cpp
4. https://github.com/OrcaSlicer/OrcaSlicer/blob/main/src/slic3r/GUI/Gizmos/GLGizmoCut.hpp
5. https://www.orcaslicer.com/wiki/print_prepare/prepare_cutting_tool (stub) / https://github.com/OrcaSlicer/OrcaSlicer_WIKI/blob/main/print_prepare/prepare_cutting_tool.md
6. https://wiki.bambulab.com/en/software/bambu-studio/cut-tool
7. https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang
8. https://wiki.bambulab.com/en/software/bambu-studio/support
9. https://github.com/Ultimaker/Cura/blob/main/resources/definitions/fdmprinter.def.json
10. https://help.autodesk.com/cloudhelp/2019/ENU/MSHMXR/files/GUID-C36CDABA-05F7-44B0-9529-C33D9E435220.htm
11. https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/bisect.html
12. https://deepwiki.com/bambulab/BambuStudio/7.2-advanced-cutting-tools *(secondary, AI-generated)*

**Printing guidance**
13. https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135
14. https://help.prusa3d.com/article/bridging_1802
15. https://help.prusa3d.com/article/skirt-and-brim_133969
16. https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/
17. https://www.hubs.com/knowledge-base/dimensional-accuracy-3d-printed-parts/
18. https://www.hydraresearch3d.com/design-rules
19. https://forum.bambulab.com/t/3-ways-to-reduce-line-detachment-in-dome-structures/192368
20. https://forum.bambulab.com/t/glue-moat-for-joined-parts/75168
21. https://www.3dprinterly.com/how-to-3d-print-a-dome-or-sphere-without-supports/
22. https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-how-do-i-print-this-printing-help/sphere-lampshade-print-top-fails/ *(thread has no resolution)*

**Bonding / materials**
23. https://www.ellsworth.com/globalassets/literature-library/manufacturer/henkel-loctite/henkel-loctite-design-guide-plastic-bonding.pdf — *Loctite Design Guide for Bonding Plastics*, Vol. 6 (2011)
24. https://prusament.com/wp-content/uploads/2022/10/PLA_Prusament_TDS_2021_10_EN.pdf
25. https://doi.org/10.1007/s40964-026-01565-3 — Shen, Zhang & Qin, wedged mortise–tenon joints for FFF, *Prog. Addit. Manuf.* 11:4025–4041 (2026), open access
26. https://doi.org/10.1177/09544062221089849 — adhesive bonding of 3D-printed ABS/PLA, joint design × adhesive × surface treatment, *IMechE Part C* (2022) *(abstract only)*
27. https://doi.org/10.1108/RPJ-10-2020-0265 — overview of joining/welding to beat FDM build-volume limits, *RPJ* (2021) *(abstract only)*
28. https://doi.org/10.1108/rpj-01-2023-0030 — friction stir spot welding to overcome bed size limits *(abstract only)*
29. https://doi.org/10.1016/j.jajp.2024.100208 — spin friction welding of MEX parts *(abstract only)*
30. https://www.semanticscholar.org/paper/Lap-Shear-Strength-Assessment-of-Acetone-Welded-ABS-Tuazon-Espino *(citation only, values not obtained)*

**Decomposition literature**
31. https://gfx.cs.princeton.edu/pubs/Luo_2012_CPM/index.php — Chopper, ACM TOG 31(6) 2012, DOI 10.1145/2366145.2366148 (full text read via http://hdl.handle.net/1721.1/90389)
32. https://github.com/gregstarr/pychop3d — open-source Chopper implementation
33. https://www2.cs.sfu.ca/~haoz/pubs/hu_siga14_pym.pdf — Approximate Pyramidal Shape Decomposition, DOI 10.1145/2661229.2661244
34. https://doi.org/10.1145/2816795.2818087 — Dapper: decompose-and-pack for 3D printing, TOG 34(6) 2015
35. https://doi.org/10.1145/3478513.3480555 — Volume decomposition for two-piece rigid casting, TOG 40(6) 2021
36. https://doi.org/10.1145/3618324 — VASCO, TOG 2023
37. https://doi.org/10.1016/j.addma.2023.103529 — strength-enhanced volume decomposition
38. https://doi.org/10.1016/j.cad.2021.103135 — support-free volume decomposition via ellipsoidal slicing

**Mesh validity**
39. https://trimesh.org/trimesh.base.html and https://github.com/mikedh/trimesh (`base.py`, `intersections.py`)
40. https://github.com/libigl/libigl/tree/main/include/igl (`is_edge_manifold.h`, `is_vertex_manifold.h`, `boundary_loop.h`, `boundary_facets.h`)
41. https://doc.cgal.org/latest/Polygon_mesh_processing/index.html and https://github.com/CGAL/cgal/blob/master/Polygon_mesh_processing/include/CGAL/Polygon_mesh_processing/stitch_borders.h
42. https://github.com/elalish/manifold and https://manifoldcad.org/docs/html/index.html
43. https://github.com/cnr-isti-vclab/meshlab/blob/main/src/meshlabplugins/filter_measure/filter_measure.cpp
44. https://en.wikipedia.org/wiki/Euler_characteristic and https://en.wikipedia.org/wiki/Surface_(topology)