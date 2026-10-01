import { describe, expect, it } from "vitest";
import { assembleSheet, checkCells, meshBounds, parseSheetManifest, placeSample, sheetStl } from "./sheet.js";
import { stlToIndexedMeshFromBuffer } from "../mesh.js";
import { parseWindow, itemRenderFlags } from "./compose.js";
import { iterationId, type IterationKey } from "../iteration.js";
import type { Bounds, IndexedMesh } from "../mesh.js";

// These pin what `slice sheet` does before it touches bikar or BambuStudio: the sheet file's rules (a
// cell must be a window), where a sample lands (its window centre on the cell, its base on the card),
// the layout validator (per sample and per pair), and that a window changes a recipe's id without
// changing any id minted before windows existed.

/** A unit box mesh spanning [x0,x1] × [y0,y1] × [z0,z1] (8 corners; the triangles do not matter here). */
function box(x0: number, x1: number, y0: number, y1: number, z0: number, z1: number): IndexedMesh {
  const vertices: number[] = [];
  for (const x of [x0, x1]) for (const y of [y0, y1]) for (const z of [z0, z1]) vertices.push(x, y, z);
  return { vertices, triangles: [0, 1, 2] };
}
const b = (x0: number, x1: number, y0: number, y1: number): Bounds => ({ min: [x0, y0, 0], max: [x1, y1, 1] });

const SHEET = `
profile:
  settings: "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D"
  filament: "Bambu PLA Basic @BBL X2D 0.4 nozzle"
card:
  bkr: bikar:patterns/Coupons/Sampler-Cards.bkr
  piece: Sheet1Card
cells:
  - name: B TRUE / CS-1
    at: [-20, -10]
    bkr: bikar:patterns/Constructions/GimTvN9hw4U-minimal-coaster.bkr
    piece: Coaster
    window: 30@9.7,1
  - name: C DOME / GBV
    at: [48, -44]
    bkr: bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr
    piece: Coaster
    params: { round: 1.5 }
    window: 30
`;

describe("parseSheetManifest", () => {
  it("reads the card and each cell, a bare-number window as text", () => {
    const s = parseSheetManifest(SHEET);
    expect(s.card.piece).toBe("Sheet1Card");
    expect(s.cells.map((c) => c.name)).toEqual(["B TRUE / CS-1", "C DOME / GBV"]);
    expect(s.cells[0]!.at).toEqual([-20, -10]);
    expect(s.cells[0]!.item.window).toBe("30@9.7,1");
    expect(s.cells[1]!.item.window).toBe("30");
    expect(s.cells[1]!.item.params).toEqual({ round: 1.5 });
  });

  it("refuses a cell with no window: a whole or shrunk coaster is not a true-size sample", () => {
    const bad = SHEET.replace("    window: 30@9.7,1\n", "");
    expect(() => parseSheetManifest(bad)).toThrow(/B TRUE \/ CS-1.*needs `window:`/);
  });

  it("names the cell, not items[n], when an item field is wrong", () => {
    const bad = SHEET.replace("window: 30@9.7,1", "window: 30@9.7");
    expect(() => parseSheetManifest(bad)).toThrow(/^cells\[0\]: `window:`/);
  });

  it("refuses a cell with no position, and a card with a window", () => {
    expect(() => parseSheetManifest(SHEET.replace("    at: [-20, -10]\n", ""))).toThrow(/`at:` must be \[x, y\]/);
    expect(() => parseSheetManifest(SHEET.replace("  piece: Sheet1Card\n", "  piece: Sheet1Card\n  window: 30\n"))).toThrow(
      /card.*cannot carry a window/,
    );
  });
});

describe("parseWindow and the render flags", () => {
  it("reads bikar's spelling, the centre defaulting to the origin", () => {
    expect(parseWindow("30@9.7,1")).toEqual({ side: 30, x: 9.7, y: 1 });
    expect(parseWindow("30@-12.5,8")).toEqual({ side: 30, x: -12.5, y: 8 });
    expect(parseWindow("30")).toEqual({ side: 30, x: 0, y: 0 });
    for (const bad of ["", "30@", "30@1", "0", "-30", "30@a,b"]) expect(parseWindow(bad)).toBeNull();
  });

  it("passes --window to bikar only when the item is cut", () => {
    expect(itemRenderFlags({ piece: "Coaster", params: { round: 1.5 }, window: "30@0,0" })).toEqual([
      "--piece", "Coaster", "--param", "round=1.5", "--window", "30@0,0",
    ]);
    expect(itemRenderFlags({ piece: "", params: {}, window: "" })).toEqual([]);
  });
});

describe("the iteration key with a window", () => {
  const base: IterationKey = {
    source: "bikar:patterns/Constructions/x.bkr@abc",
    source_sha256: "0".repeat(64),
    piece: "Coaster",
    params: {},
    slice_profile: { settings: "m;p", filament: "f" },
  };
  it("leaves every pre-window id unchanged and gives each window its own id", () => {
    // The id this key hashed to before windows existed (computed with master's iteration.ts at 222f71c):
    // a key with no window field must still hash to it, or every record's id would silently fork.
    expect(iterationId(base)).toBe("it-385b1deca240");
    const a = iterationId({ ...base, window: "30@9.7,1" });
    const c = iterationId({ ...base, window: "30@0,0" });
    expect(a).not.toBe(iterationId(base));
    expect(a).not.toBe(c);
  });
});

describe("placeSample", () => {
  it("puts the window centre on the cell and the base on the card's top", () => {
    // CS-1's window 30@9.7,1 comes out of bikar in the coaster's own frame: x -5.3..24.7, y -14..16, z 0..4.
    const placed = placeSample(box(-5.3, 24.7, -14, 16, 0, 4), "30@9.7,1", [-20, -10], 1.4);
    const pb = meshBounds(placed);
    expect(pb.min[0]).toBeCloseTo(-35);
    expect(pb.max[0]).toBeCloseTo(-5);
    expect(pb.min[1]).toBeCloseTo(-25);
    expect(pb.max[1]).toBeCloseTo(5);
    expect(pb.min[2]).toBeCloseTo(1.4); // touching the card top, not sunk into it
    expect(pb.max[2]).toBeCloseTo(5.4);
  });

  it("anchors on the window centre, not the mesh's box, when the art stops short of an edge", () => {
    // Art only in the right half of a 30@0,0 window: x 0..15. Centring the box would move it 7.5 mm left.
    const pb = meshBounds(placeSample(box(0, 15, -15, 15, 0, 4), "30@0,0", [14, -10], 1.4));
    expect(pb.min[0]).toBeCloseTo(14);
    expect(pb.max[0]).toBeCloseTo(29);
  });
});

describe("checkCells — every sample on the card, clear of every other", () => {
  const card = b(-69, 69, -61, 61);
  it("PASS: sheet 1's six cells on the 138 × 122 card, 4 mm apart", () => {
    const samples = [-20, 14, 48].flatMap((x) =>
      [-10, -44].map((y) => ({ name: `${x},${y}`, bounds: b(x - 15, x + 15, y - 15, y + 15) })),
    );
    expect(checkCells(card, samples)).toEqual([]);
  });

  it("FAIL: a sample past the card's edge, named, even when the samples' union box is not", () => {
    const out = checkCells(card, [
      { name: "left", bounds: b(-60, -30, -10, 20) },
      { name: "off", bounds: b(45, 75, -10, 20) },
    ]);
    expect(out).toHaveLength(1);
    expect(out[0]).toMatch(/^off: spans x 45\.\.75/);
  });

  it("FAIL: two samples 20 mm apart overlap by 10 mm; touching edges do not count", () => {
    const out = checkCells(card, [
      { name: "a", bounds: b(-30, 0, -15, 15) },
      { name: "b", bounds: b(-10, 20, -15, 15) },
      { name: "c", bounds: b(20, 50, -15, 15) },
    ]);
    expect(out).toEqual(["a and b overlap by 10 × 30 mm"]);
  });
});

describe("sheetStl", () => {
  it("writes every part's triangles into one STL that reads back with the same bounds", () => {
    const card = { vertices: [-69, -61, 0, 69, -61, 0, 0, 61, 1.4], triangles: [0, 1, 2] };
    const sample = placeSample(box(-15, 15, -15, 15, 0, 4), "30", [48, -44], 1.4);
    const back = stlToIndexedMeshFromBuffer(sheetStl([card, sample]));
    expect(back).not.toBeNull();
    expect(back!.triangles.length / 3).toBe(2);
    const pb = meshBounds(back!);
    expect(pb.min).toEqual([-69, -61, 0]);
    expect(pb.max[0]).toBeCloseTo(69);
    expect(pb.max[2]).toBeCloseTo(5.4);
  });
});

describe("assembleSheet", () => {
  it("is one object: the card first, then each sample, every part in slot 1", () => {
    const m = box(0, 1, 0, 1, 0, 1);
    const obj = assembleSheet("sheets-01", m, [
      { name: "B TRUE / CS-1", mesh: m },
      { name: "C DOME / GBV", mesh: m },
    ]);
    expect(obj.name).toBe("sheets-01");
    expect(obj.bodies.map((x) => x.name)).toEqual(["card", "B TRUE / CS-1", "C DOME / GBV"]);
    expect(new Set(obj.bodies.map((x) => x.region)).size).toBe(3);
    expect(obj.bodies.every((x) => x.extruder === 1)).toBe(true);
  });
});
