import { describe, expect, it } from "vitest";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { assembleCoasters, coasterFootprint, type CoasterAssemblyInput } from "./coaster.js";
import { buildAmsSlotMap, type CoasterPartsSidecar } from "../ams.js";
import type { IndexedMesh } from "../mesh.js";

// These pin the two pure steps `slice coaster` does before it touches bikar or BambuStudio: expanding a
// rendered recipe into per-copy plate objects with the right extruder per region (step 7), and measuring
// a coaster's whole footprint as the UNION of its region bodies (K10: the bodies share a frame, so the
// bed packs a coaster, not loose bodies). A wrong extruder mis-assigns a colour; a summed footprint would
// reject a coaster that fits.

const stubMesh: IndexedMesh = { vertices: [0, 0, 0, 1, 0, 0, 1, 1, 0], triangles: [0, 1, 2] };

/** A 3-region coaster sidecar (base=Slab, straps=Gold, border=Copper), matching the shipped presets. */
function borderSidecar(name: string): CoasterPartsSidecar {
  return {
    coaster: name,
    pinch: "fillet",
    parts: [
      { region: "base", stl: `${name}-base.stl`, triangles: 1, paletteName: "Slab", hex: "#333333" },
      { region: "straps", stl: `${name}-straps.stl`, triangles: 1, paletteName: "Gold", hex: "#d4af37" },
      { region: "border", stl: `${name}-border.stl`, triangles: 1, paletteName: "Copper", hex: "#b87333" },
    ],
  };
}

/** The slot map keyed by iteration id (as runCoaster builds it), plus an input builder for that key. */
function inputFor(key: string, entry: string, count: number, sc: CoasterPartsSidecar): CoasterAssemblyInput {
  return {
    entry,
    count,
    displayName: sc.coaster,
    key,
    parts: sc.parts,
    meshFor: () => stubMesh,
  };
}

describe("assembleCoasters — recipe × count → plate objects", () => {
  it("maps each region body to the extruder its palette holds in the slot map", () => {
    const sc = borderSidecar("Star");
    const map = buildAmsSlotMap([{ ...sc, coaster: "it-abc" }], { defaultFilament: "PLA Basic" });
    const obj = assembleCoasters([inputFor("it-abc", "1", 1, sc)], map)[0]!;
    // Slot 1 is the plate default; the three distinct palettes take slots 2,3,4 in first-seen order.
    const byRegion = Object.fromEntries(obj.bodies.map((b) => [b.region, b.extruder]));
    expect(byRegion.base).toBe(map.assignments.get("it-abc")!.get("base"));
    expect(byRegion.straps).toBe(map.assignments.get("it-abc")!.get("straps"));
    expect(byRegion.border).toBe(map.assignments.get("it-abc")!.get("border"));
    // The three palettes are distinct, so the three extruders are distinct (none is slot 1's default).
    expect(new Set(obj.bodies.map((b) => b.extruder)).size).toBe(3);
  });

  it("expands count into that many objects and suffixes the label only when count > 1", () => {
    const sc = borderSidecar("Star");
    const map = buildAmsSlotMap([{ ...sc, coaster: "it-abc" }], { defaultFilament: "PLA Basic" });
    const objs = assembleCoasters([inputFor("it-abc", "3", 2, sc)], map);
    expect(objs).toHaveLength(2);
    expect(objs[0]!.name).toBe("3: Star #1");
    expect(objs[1]!.name).toBe("3: Star #2");
    // Each copy carries all three region bodies.
    expect(objs[0]!.bodies.map((b) => b.region)).toEqual(["base", "straps", "border"]);
  });

  it("omits the #k suffix for a single copy", () => {
    const sc = borderSidecar("Star");
    const map = buildAmsSlotMap([{ ...sc, coaster: "it-abc" }], { defaultFilament: "PLA Basic" });
    const obj = assembleCoasters([inputFor("it-abc", "1", 1, sc)], map)[0]!;
    expect(obj.name).toBe("1: Star");
    expect(obj.bodies[1]!.name).toBe("Star · straps (Gold)");
  });

  it("keeps palette slots plate-global across two recipes sharing a palette", () => {
    // Two distinct coasters both use Gold: it must resolve to the SAME slot in both (first-seen wins).
    const a = borderSidecar("Star");
    const b: CoasterPartsSidecar = {
      coaster: "Moon",
      pinch: "fillet",
      parts: [
        { region: "base", stl: "Moon-base.stl", triangles: 1, paletteName: "Slab", hex: "#333333" },
        { region: "straps", stl: "Moon-straps.stl", triangles: 1, paletteName: "Gold", hex: "#d4af37" },
      ],
    };
    const map = buildAmsSlotMap(
      [{ ...a, coaster: "it-a" }, { ...b, coaster: "it-b" }],
      { defaultFilament: "PLA Basic" },
    );
    const objs = assembleCoasters(
      [inputFor("it-a", "1", 1, a), inputFor("it-b", "2", 1, b)],
      map,
    );
    const goldA = objs[0]!.bodies.find((x) => x.region === "straps")!.extruder;
    const goldB = objs[1]!.bodies.find((x) => x.region === "straps")!.extruder;
    expect(goldA).toBe(goldB);
  });

  it("labels an untagged region without a palette parenthetical", () => {
    const sc: CoasterPartsSidecar = {
      coaster: "Plain",
      pinch: "fillet",
      parts: [{ region: "base", stl: "Plain-base.stl", triangles: 1, paletteName: null, hex: null }],
    };
    const map = buildAmsSlotMap([{ ...sc, coaster: "it-p" }], { defaultFilament: "PLA Basic" });
    const obj = assembleCoasters([inputFor("it-p", "1", 1, sc)], map)[0]!;
    expect(obj.bodies[0]!.name).toBe("Plain · base");
    expect(obj.bodies[0]!.extruder).toBe(1); // untagged ⇒ the plate default (slot 1)
  });
});

/** Write a minimal binary STL (one triangle) whose bbox is exactly [min]→[max] via two opposite corners. */
function writeStl(path: string, min: [number, number, number], max: [number, number, number]): void {
  const buf = Buffer.alloc(84 + 50);
  buf.writeUInt32LE(1, 80);
  const verts: Array<[number, number, number]> = [min, max, min];
  let o = 84 + 12;
  for (const [x, y, z] of verts) {
    buf.writeFloatLE(x, o);
    buf.writeFloatLE(y, o + 4);
    buf.writeFloatLE(z, o + 8);
    o += 12;
  }
  writeFileSync(path, buf);
}

describe("coasterFootprint — union bbox of the region bodies", () => {
  it("is the union across all region STLs, not their sum", () => {
    const dir = mkdtempSync(join(tmpdir(), "coaster-fp-"));
    try {
      // Two bodies, overlapping in a shared frame: base spans 0..40 in X, border 5..45. Union = 0..45.
      writeStl(join(dir, "Star-base.stl"), [0, 0, 0], [40, 30, 3]);
      writeStl(join(dir, "Star-border.stl"), [5, -2, 0], [45, 32, 3]);
      const sc: CoasterPartsSidecar = {
        coaster: "Star",
        pinch: "fillet",
        parts: [
          { region: "base", stl: "Star-base.stl", triangles: 1, paletteName: "Slab", hex: "#333333" },
          { region: "border", stl: "Star-border.stl", triangles: 1, paletteName: "Copper", hex: "#b87333" },
        ],
      };
      // Union X: 0..45 = 45; union Y: -2..32 = 34. A sum would wrongly give 85 × 62.
      expect(coasterFootprint(dir, sc)).toEqual([45, 34]);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
