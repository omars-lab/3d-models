// STL bounding box — the footprint the bed pre-check measures.
//
// The plate composer needs each rendered part's XY footprint to run the bed-fit pre-check BEFORE the
// slow slicer runs (docs/plate-composer-design.md §6). bikar emits an STL; rather than depend on an
// undocumented bikar "bounds" flag, we read the mesh's own vertices — the authoritative geometry — and
// track min/max per axis. One reader handles both STL encodings (binary is what bikar writes; ASCII is
// supported so a hand-authored fixture works in tests without a bikar checkout).
//
// This is a NECESSARY-condition input only: the footprint bbox says whether a part *can* fit a bed
// rectangle, never whether a set of parts *tiles* — that is the slicer's --arrange authority (§6).

import { readFileSync } from "node:fs";

export interface Bounds {
  min: [number, number, number];
  max: [number, number, number];
}

/** XY footprint (mm) of a bounds box: [width along X, depth along Y]. */
export function footprint(b: Bounds): [number, number] {
  return [b.max[0] - b.min[0], b.max[1] - b.min[1]];
}

/** True if the buffer looks like ASCII STL (starts with "solid" and has no binary triangle count that
 *  matches its size). We treat a file as ASCII only if it begins with "solid" AND contains "facet",
 *  since a binary STL may also start with the bytes "solid" in its 80-byte header. */
function looksAscii(buf: Buffer): boolean {
  const head = buf.subarray(0, Math.min(buf.length, 512)).toString("latin1");
  if (!/^\s*solid/.test(head)) return false;
  // A binary STL's header is 80 bytes then a uint32 triangle count; its body is 50 bytes/triangle.
  // If the length matches that formula exactly, it is binary regardless of a "solid" header.
  if (buf.length >= 84) {
    const tris = buf.readUInt32LE(80);
    if (buf.length === 84 + tris * 50) return false;
  }
  return /facet/.test(head) || /vertex/.test(buf.subarray(0, Math.min(buf.length, 4096)).toString("latin1"));
}

// Six tracked scalars, not indexed min[a]/max[a]: under noUncheckedIndexedAccess a tuple index is
// `number | undefined`, so per-axis accumulators are kept as named locals the compiler can prove real.
class BoundsAcc {
  minX = Infinity;
  minY = Infinity;
  minZ = Infinity;
  maxX = -Infinity;
  maxY = -Infinity;
  maxZ = -Infinity;
  seen = false;
  add(x: number, y: number, z: number): void {
    if (!Number.isFinite(x) || !Number.isFinite(y) || !Number.isFinite(z)) return;
    if (x < this.minX) this.minX = x;
    if (y < this.minY) this.minY = y;
    if (z < this.minZ) this.minZ = z;
    if (x > this.maxX) this.maxX = x;
    if (y > this.maxY) this.maxY = y;
    if (z > this.maxZ) this.maxZ = z;
    this.seen = true;
  }
  result(): Bounds | null {
    return this.seen
      ? { min: [this.minX, this.minY, this.minZ], max: [this.maxX, this.maxY, this.maxZ] }
      : null;
  }
}

function boundsFromAscii(text: string): Bounds | null {
  const acc = new BoundsAcc();
  const re = /vertex\s+(-?[\d.eE+]+)\s+(-?[\d.eE+]+)\s+(-?[\d.eE+]+)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text)) !== null) {
    acc.add(Number(m[1]), Number(m[2]), Number(m[3]));
  }
  return acc.result();
}

function boundsFromBinary(buf: Buffer): Bounds | null {
  if (buf.length < 84) return null;
  const tris = buf.readUInt32LE(80);
  if (buf.length < 84 + tris * 50) return null;
  const acc = new BoundsAcc();
  for (let t = 0; t < tris; t++) {
    const base = 84 + t * 50 + 12; // skip the 12-byte normal; 3 vertices × 3 floats follow
    for (let vtx = 0; vtx < 3; vtx++) {
      const o = base + vtx * 12;
      acc.add(buf.readFloatLE(o), buf.readFloatLE(o + 4), buf.readFloatLE(o + 8));
    }
  }
  return acc.result();
}

/** Parse an in-memory STL buffer to its bounds, or null if it has no readable vertices. */
export function stlBoundsFromBuffer(buf: Buffer): Bounds | null {
  return looksAscii(buf) ? boundsFromAscii(buf.toString("latin1")) : boundsFromBinary(buf);
}

/** Read an STL file and return its bounding box, or throw a clear error if it cannot be parsed. */
export function stlBounds(path: string): Bounds {
  const buf = readFileSync(path);
  const b = stlBoundsFromBuffer(buf);
  if (!b) throw new Error(`could not read STL bounds from ${path} — not a valid STL, or it has no vertices`);
  return b;
}
