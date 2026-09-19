import { describe, expect, it } from "vitest";
import { footprint, stlBoundsFromBuffer, stlToIndexedMeshFromBuffer } from "./mesh.js";

// The bed pre-check reads each part's footprint from the STL bikar emits. These pin the two encodings
// (bikar writes binary; a hand-authored ASCII fixture proves the parser without a bikar checkout) and
// the footprint projection, since a wrong bbox would let an oversized part pass the §6 pre-check.

function asciiTriangle(v: Array<[number, number, number]>): string {
  return [
    "solid test",
    " facet normal 0 0 1",
    "  outer loop",
    ...v.map(([x, y, z]) => `   vertex ${x} ${y} ${z}`),
    "  endloop",
    " endfacet",
    "endsolid test",
  ].join("\n");
}

/** Build a minimal binary STL with one triangle at the given vertices. */
function binaryTriangle(v: Array<[number, number, number]>): Buffer {
  const buf = Buffer.alloc(84 + 50);
  buf.writeUInt32LE(1, 80); // one triangle
  let o = 84 + 12; // skip 80-byte header, 4-byte count, 12-byte normal
  for (const [x, y, z] of v) {
    buf.writeFloatLE(x, o);
    buf.writeFloatLE(y, o + 4);
    buf.writeFloatLE(z, o + 8);
    o += 12;
  }
  return buf;
}

describe("stlBoundsFromBuffer — ASCII", () => {
  it("reads min/max across vertices", () => {
    const b = stlBoundsFromBuffer(
      Buffer.from(asciiTriangle([[0, 0, 0], [10, 4, 2], [-3, 8, 5]]), "latin1"),
    );
    expect(b).not.toBeNull();
    expect(b!.min).toEqual([-3, 0, 0]);
    expect(b!.max).toEqual([10, 8, 5]);
  });
});

describe("stlBoundsFromBuffer — binary", () => {
  it("reads min/max from little-endian floats", () => {
    const b = stlBoundsFromBuffer(binaryTriangle([[1, 2, 0], [5, 2, 3], [1, 9, 0]]));
    expect(b).not.toBeNull();
    expect(b!.min).toEqual([1, 2, 0]);
    expect(b!.max).toEqual([5, 9, 3]);
  });

  it("returns null for a buffer with no readable geometry", () => {
    expect(stlBoundsFromBuffer(Buffer.from("not an stl"))).toBeNull();
  });
});

describe("footprint — XY projection", () => {
  it("is [width along X, depth along Y]", () => {
    expect(footprint({ min: [-3, 0, 1], max: [10, 8, 5] })).toEqual([13, 8]);
  });
});

// ── STL → indexed mesh (3MF assembler input, part 4b-ii) ────────────────────────────────────────────
// A 3MF <mesh> is indexed, so coincident STL vertices must collapse to one index or the slicer reads a
// cloud of disconnected facets (non-manifold). These pin the dedup and the degenerate-facet drop across
// both encodings, since a wrong index or an un-welded seam is exactly what BambuStudio flags on import.

/** Build a binary STL from a list of triangles (each three [x,y,z] corners). */
function binaryMesh(tris: Array<Array<[number, number, number]>>): Buffer {
  const buf = Buffer.alloc(84 + 50 * tris.length);
  buf.writeUInt32LE(tris.length, 80);
  tris.forEach((v, t) => {
    let o = 84 + t * 50 + 12; // skip this facet's 12-byte normal
    for (const [x, y, z] of v) {
      buf.writeFloatLE(x, o);
      buf.writeFloatLE(y, o + 4);
      buf.writeFloatLE(z, o + 8);
      o += 12;
    }
  });
  return buf;
}

/** Build an ASCII STL from a list of triangles. */
function asciiMesh(tris: Array<Array<[number, number, number]>>): string {
  return [
    "solid test",
    ...tris.flatMap((v) => [
      " facet normal 0 0 1",
      "  outer loop",
      ...v.map(([x, y, z]) => `   vertex ${x} ${y} ${z}`),
      "  endloop",
      " endfacet",
    ]),
    "endsolid test",
  ].join("\n");
}

// Two triangles of a unit square sharing the diagonal edge (0,0,0)–(1,1,0): six STL vertices, four unique.
const SQUARE: Array<Array<[number, number, number]>> = [
  [[0, 0, 0], [1, 0, 0], [1, 1, 0]],
  [[0, 0, 0], [1, 1, 0], [0, 1, 0]],
];

describe("stlToIndexedMeshFromBuffer — dedup + degenerate drop", () => {
  it("collapses coincident vertices to unique indices (binary)", () => {
    const m = stlToIndexedMeshFromBuffer(binaryMesh(SQUARE));
    expect(m).not.toBeNull();
    expect(m!.vertices.length).toBe(4 * 3); // four unique corners, not six
    expect(m!.triangles.length).toBe(2 * 3);
    // The shared corners (0,0,0) and (1,1,0) must resolve to the same index in both triangles.
    expect(m!.triangles[0]).toBe(m!.triangles[3]); // first vertex of each triangle is (0,0,0)
    expect(m!.triangles[2]).toBe(m!.triangles[4]); // (1,1,0): 3rd of tri A, 2nd of tri B
  });

  it("collapses coincident vertices to unique indices (ASCII)", () => {
    const m = stlToIndexedMeshFromBuffer(Buffer.from(asciiMesh(SQUARE), "latin1"));
    expect(m).not.toBeNull();
    expect(m!.vertices.length).toBe(4 * 3);
    expect(m!.triangles.length).toBe(2 * 3);
  });

  it("drops a degenerate facet (two coincident corners) rather than emit a zero-area triangle", () => {
    const withDegenerate = binaryMesh([
      ...SQUARE,
      [[2, 2, 0], [2, 2, 0], [3, 3, 0]], // two corners identical → no surface
    ]);
    const m = stlToIndexedMeshFromBuffer(withDegenerate);
    expect(m).not.toBeNull();
    expect(m!.triangles.length).toBe(2 * 3); // the degenerate triangle is not indexed
  });

  it("returns null for a buffer with no readable triangles", () => {
    expect(stlToIndexedMeshFromBuffer(Buffer.from("not an stl"))).toBeNull();
  });
});
