import { describe, expect, it } from "vitest";
import { footprint, stlBoundsFromBuffer } from "./mesh.js";

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
