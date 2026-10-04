// STL bounding box — the footprint the bed pre-check measures.
//
// The plate composer needs each rendered part's XY footprint to run the bed-fit pre-check BEFORE the
// slow slicer runs (docs/design/printing/plate-composer-design.md §6). bikar emits an STL; rather than depend on an
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

/** A binary STL of `buf` scaled by `s`, moved so its footprint is centered on the origin and it rests
 *  on z = 0. The bed map reads each object's place from the plate's transform, which is where the
 *  mesh's origin lands, so a mesh modeled off-center would be mapped by its offset, not where it
 *  prints (an iPhone model at x 64–102 mapped 83 mm off, sheets-04d). `s` is one number, or one per
 *  axis [x, y, z]. A uniform scale and a move do not turn a face, so its normals stay as they are; a
 *  scale per axis tilts the faces, so each normal is worked out again from its triangle (phones-02's
 *  small phones, 2× thicker than they are wide). An ASCII input comes out binary, since the slicer
 *  reads either. */
export function scaledCenteredStl(buf: Buffer, s: number | readonly [number, number, number]): Buffer {
  const k3 = typeof s === "number" ? [s, s, s] : [...s];
  if (k3.length !== 3 || !k3.every((k) => k > 0 && Number.isFinite(k))) {
    throw new Error(`scale must be a number > 0, or three of them, got ${JSON.stringify(s)}`);
  }
  const uniform = k3[0] === k3[1] && k3[1] === k3[2];
  const b = stlBoundsFromBuffer(buf);
  if (!b) throw new Error("not a valid STL, or it has no vertices");
  const c = [(b.min[0] + b.max[0]) / 2, (b.min[1] + b.max[1]) / 2, b.min[2]];
  let out: Buffer;
  if (!looksAscii(buf)) {
    if (buf.length < 84 || buf.length < 84 + buf.readUInt32LE(80) * 50) throw new Error("not a valid binary STL");
    out = Buffer.from(buf);
    const tris = out.readUInt32LE(80);
    for (let t = 0; t < tris; t++) {
      const base = 84 + t * 50 + 12; // skip the 12-byte normal
      for (let k = 0; k < 9; k++) out.writeFloatLE((out.readFloatLE(base + k * 4) - c[k % 3]!) * k3[k % 3]!, base + k * 4);
    }
  } else {
    const re = /vertex\s+(-?[\d.eE+]+)\s+(-?[\d.eE+]+)\s+(-?[\d.eE+]+)/g;
    const v: number[] = [];
    let m: RegExpExecArray | null;
    while ((m = re.exec(buf.toString("latin1"))) !== null) {
      for (let k = 0; k < 3; k++) v.push((Number(m[k + 1]) - c[k]!) * k3[k]!);
    }
    const tris = Math.floor(v.length / 9);
    out = Buffer.alloc(84 + tris * 50);
    out.writeUInt32LE(tris, 80);
    for (let t = 0; t < tris; t++) {
      for (let k = 0; k < 9; k++) out.writeFloatLE(v[t * 9 + k]!, 84 + t * 50 + 12 + k * 4);
    }
  }
  if (!uniform) writeFaceNormals(out);
  return out;
}

/** Set every triangle's normal in a binary STL to the unit normal of its own corners (right-hand
 *  rule, so it points the way the corners wind). A degenerate triangle gets 0 0 0. */
function writeFaceNormals(out: Buffer): void {
  const tris = out.readUInt32LE(80);
  for (let t = 0; t < tris; t++) {
    const o = 84 + t * 50;
    const p = Array.from({ length: 9 }, (_, k) => out.readFloatLE(o + 12 + k * 4));
    const [ux, uy, uz] = [p[3]! - p[0]!, p[4]! - p[1]!, p[5]! - p[2]!];
    const [vx, vy, vz] = [p[6]! - p[0]!, p[7]! - p[1]!, p[8]! - p[2]!];
    const n = [uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx];
    const len = Math.hypot(n[0]!, n[1]!, n[2]!);
    for (let k = 0; k < 3; k++) out.writeFloatLE(len > 0 ? n[k]! / len : 0, o + k * 4);
  }
}

/** Read an STL file and return its bounding box, or throw a clear error if it cannot be parsed. */
export function stlBounds(path: string): Bounds {
  const buf = readFileSync(path);
  const b = stlBoundsFromBuffer(buf);
  if (!b) throw new Error(`could not read STL bounds from ${path} — not a valid STL, or it has no vertices`);
  return b;
}

// ── STL → indexed mesh (for the 3MF assembler, part 4b-ii) ─────────────────────────────────────────
// A 3MF `<mesh>` is INDEXED: a `<vertices>` list of unique points and a `<triangles>` list of index
// triples. STL is the opposite — every triangle carries its own three vertices, with coincident points
// repeated verbatim. So embedding a bikar STL in a 3MF means de-duplicating: coincident vertices must
// collapse to one index or the mesh reads as a cloud of disconnected facets and the slicer flags it
// non-manifold. We key the dedup on the vertices' exact value (bikar emits coincident corners as
// identical floats, so no rounding is needed — and rounding would risk welding genuinely distinct
// points), reusing the same buffer reader the bounds path already trusts.

/** An indexed triangle mesh: `vertices` is a flat [x,y,z, x,y,z, …] list of unique points; `triangles`
 *  is a flat [v1,v2,v3, …] list of 0-based indices into it. Flat arrays keep a 200k-triangle body cheap
 *  to build and to serialise. */
export interface IndexedMesh {
  vertices: number[];
  triangles: number[];
}

/** Dedup accumulator: a coincident vertex collapses to the first index that carried its exact x/y/z. */
class MeshBuilder {
  vertices: number[] = [];
  triangles: number[] = [];
  private index = new Map<string, number>();
  private vertex(x: number, y: number, z: number): number {
    // Value key: bikar writes a shared corner as identical floats, so string equality of the canonical
    // number matches without a tolerance (see the module note above).
    const key = `${x},${y},${z}`;
    const hit = this.index.get(key);
    if (hit !== undefined) return hit;
    const id = this.vertices.length / 3;
    this.vertices.push(x, y, z);
    this.index.set(key, id);
    return id;
  }
  triangle(ax: number, ay: number, az: number, bx: number, by: number, bz: number, cx: number, cy: number, cz: number): void {
    // Drop a degenerate facet (two corners coincide): it carries no surface, and a 0-area triangle is a
    // slicer warning, not geometry. A body of all-degenerates leaves triangles empty — caught by caller.
    const a = this.vertex(ax, ay, az);
    const b = this.vertex(bx, by, bz);
    const c = this.vertex(cx, cy, cz);
    if (a === b || b === c || a === c) return;
    this.triangles.push(a, b, c);
  }
  result(): IndexedMesh {
    return { vertices: this.vertices, triangles: this.triangles };
  }
}

function indexedFromBinary(buf: Buffer): IndexedMesh | null {
  if (buf.length < 84) return null;
  const tris = buf.readUInt32LE(80);
  if (buf.length < 84 + tris * 50) return null;
  const mb = new MeshBuilder();
  for (let t = 0; t < tris; t++) {
    const base = 84 + t * 50 + 12; // skip the 12-byte normal
    const o0 = base, o1 = base + 12, o2 = base + 24;
    mb.triangle(
      buf.readFloatLE(o0), buf.readFloatLE(o0 + 4), buf.readFloatLE(o0 + 8),
      buf.readFloatLE(o1), buf.readFloatLE(o1 + 4), buf.readFloatLE(o1 + 8),
      buf.readFloatLE(o2), buf.readFloatLE(o2 + 4), buf.readFloatLE(o2 + 8),
    );
  }
  return mb.result();
}

function indexedFromAscii(text: string): IndexedMesh | null {
  const mb = new MeshBuilder();
  const re = /vertex\s+(-?[\d.eE+]+)\s+(-?[\d.eE+]+)\s+(-?[\d.eE+]+)/g;
  const c: number[] = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(text)) !== null) {
    c.push(Number(m[1]), Number(m[2]), Number(m[3]));
    if (c.length === 9) {
      mb.triangle(c[0]!, c[1]!, c[2]!, c[3]!, c[4]!, c[5]!, c[6]!, c[7]!, c[8]!);
      c.length = 0;
    }
  }
  return mb.result();
}

/** Parse an in-memory STL buffer to an indexed mesh, or null if it has no readable triangles. */
export function stlToIndexedMeshFromBuffer(buf: Buffer): IndexedMesh | null {
  const mesh = looksAscii(buf) ? indexedFromAscii(buf.toString("latin1")) : indexedFromBinary(buf);
  if (!mesh || mesh.triangles.length === 0) return null;
  return mesh;
}

/** Read an STL file and return its indexed mesh, or throw a clear error if it cannot be parsed. */
export function stlToIndexedMesh(path: string): IndexedMesh {
  const mesh = stlToIndexedMeshFromBuffer(readFileSync(path));
  if (!mesh) throw new Error(`could not read STL mesh from ${path} — not a valid STL, or it has no triangles`);
  return mesh;
}
