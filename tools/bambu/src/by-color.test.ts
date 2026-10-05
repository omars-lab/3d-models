import { describe, expect, it } from "vitest";
import { parse as parseYaml } from "yaml";
import { type Demand, type PlateColor, groupByColor, itemLabels, normalHex, pieceGroups, readPiecesBkr, writeRecipes } from "./by-color.js";

// The one-plate-per-color writer (infill-color-ux-design §4.5) on a made-up pieces file. The real gBV
// files go through it in `bambu order fixtures`; these pin each rule with the input that breaks it.

const BKR = [
  "# a made-up pieces file, gBV's shape",
  "Middle = #6B4E9B",
  "Kite = #e05a47 # the kites",
  "Star = #2f6db5",
  "fill faces where orbit == 0 color Middle",
  "fill faces where orbit == 1 color Kite",
  "fill faces where orbit == 3 color Star",
  "fill faces where orbit == 4 color Star",
  "loose faces where orbit == 0",
  "loose faces where orbit == 1",
  "loose faces where orbit == 3",
  "loose faces where orbit == 4",
].join("\n");

const BANDS = [
  { orbit: 0, members: 1 },
  { orbit: 1, members: 10 },
  { orbit: 2, members: 10 },
  { orbit: 3, members: 10, color: "Star" },
  { orbit: 4, members: 10 },
];

const color = (key: string, hex: string): PlateColor => ({ key, hex, line: "PLA Basic", code: key, name: key, note: null });
const WHITE = color("10100", "#ffffff");
const BLACK = color("10101", "#000000");
const A = "bikar:patterns/Constructions/A-minimal-pieces.bkr";
const B = "bikar:patterns/Constructions/B-minimal-coaster.bkr";
const demand = (construction: string, piece: string | null, c: PlateColor, rank: number, count = 1): Demand => ({
  construction,
  params: { size: 100 },
  piece,
  count,
  rank,
  color: c,
});

describe("readPiecesBkr — what a pieces file says about its colors", () => {
  it("reads the palette, the orbit fills and the loose orbits, keeping a #hex past a comment", () => {
    expect(readPiecesBkr(BKR)).toEqual({
      hexes: { Middle: "#6b4e9b", Kite: "#e05a47", Star: "#2f6db5" },
      fills: { 0: "Middle", 1: "Kite", 3: "Star", 4: "Star" },
      looseOrbits: [0, 1, 3, 4],
    });
  });

  it("refuses a rule that picks one piece by index, and one chosen by anything but its orbit", () => {
    expect(() => readPiecesBkr("loose faces where orbit == 1 and index == 2")).toThrow("line 1: `loose` picks by `index`");
    expect(() => readPiecesBkr("Kite = #e05a47\nfill faces where ring == 1 color Kite")).toThrow(
      "line 2: `fill` is chosen by something other than `orbit == <n>`",
    );
  });
});

describe("pieceGroups — one group per palette name", () => {
  it("joins two orbits of one name into one group, counting both orbits' pieces", () => {
    expect(pieceGroups(readPiecesBkr(BKR), BANDS)).toEqual([
      { piece: "Middle", orbits: [0], members: 1, hex: "#6b4e9b" },
      { piece: "Kite", orbits: [1], members: 10, hex: "#e05a47" },
      { piece: "Star", orbits: [3, 4], members: 20, hex: "#2f6db5" },
    ]);
  });

  it("refuses a loose orbit bands does not have, or names differently", () => {
    expect(() => pieceGroups(readPiecesBkr(BKR), BANDS.filter((b) => b.orbit !== 4))).toThrow("loose orbit 4: bands reports no such orbit");
    expect(() => pieceGroups(readPiecesBkr(BKR), BANDS.map((b) => (b.orbit === 1 ? { ...b, color: "Hex" } : b)))).toThrow(
      "loose orbit 1: the .bkr fills it as Kite, bands says Hex",
    );
    expect(() => pieceGroups(readPiecesBkr("loose faces where orbit == 2"), BANDS)).toThrow("no palette name fills it");
  });
});

describe("groupByColor — one plate per color", () => {
  it("puts two groups of one color on one plate, frame first, in orbit order", () => {
    const plates = groupByColor([
      demand(A, null, WHITE, -1),
      demand(A, "Star", BLACK, 3),
      demand(A, "Kite", BLACK, 1),
      demand(A, "Middle", WHITE, 0),
    ]);
    expect(plates.map((p) => [p.color.key, p.items.map((i) => i.piece ?? "frame")])).toEqual([
      ["10100", ["frame", "Middle"]],
      ["10101", ["Kite", "Star"]],
    ]);
  });

  it("adds the counts of two lines asking for the same thing, and keeps different params apart", () => {
    const plates = groupByColor([demand(A, "Kite", BLACK, 1, 2), demand(A, "Kite", BLACK, 1, 3), { ...demand(A, "Kite", BLACK, 1), params: { size: 90 } }]);
    expect(plates[0]!.items.map((i) => [i.params.size, i.count])).toEqual([
      [100, 5],
      [90, 1],
    ]);
  });
});

describe("itemLabels — every label on a plate reads differently", () => {
  it("names the construction only when two share the plate", () => {
    const one = groupByColor([demand(A, null, WHITE, -1), demand(A, "Kite", WHITE, 1)])[0]!;
    expect(itemLabels(one.items)).toEqual(["COASTER", "KITE"]);
    const two = groupByColor([demand(A, null, WHITE, -1), demand(B, null, WHITE, -1)])[0]!;
    expect(itemLabels(two.items)).toEqual(["A COASTER", "B COASTER"]);
  });

  it("numbers two items that would still read the same", () => {
    const plate = groupByColor([demand(A, "Kite", BLACK, 1), { ...demand(A, "Kite", BLACK, 1), params: { size: 90 } }])[0]!;
    expect(itemLabels(plate.items)).toEqual(["KITE", "KITE 2"]);
  });
});

describe("writeRecipes — the recipe compose.ts slices", () => {
  const plates = groupByColor([demand(A, null, WHITE, -1, 2), demand(A, "Kite", BLACK, 1, 2), demand(A, "Star", BLACK, 3, 2)]);
  const written = writeRecipes(plates, "fixture-t", ["about line"], (it) => (it.piece === "Kite" ? 10 : it.piece ? 20 : 1));

  it("names each plate by its color code and writes the profile for its line", () => {
    expect(written.map((w) => w.name)).toEqual(["fixture-t-10100", "fixture-t-10101"]);
    const recipe = parseYaml(written[1]!.text) as { bed: string; profile: Record<string, string>; items: Array<Record<string, unknown>> };
    expect(recipe.bed).toBe("x2d");
    expect(recipe.profile).toEqual({
      settings: "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D",
      filament: "Bambu PLA Basic @BBL X2D 0.4 nozzle",
      color: "#000000",
    });
    expect(recipe.items).toEqual([
      { bkr: A, piece: "Kite", params: { size: 100 }, count: 2, label: "KITE" },
      { bkr: A, piece: "Star", params: { size: 100 }, count: 2, label: "STAR" },
    ]);
    expect(written[1]!.text).toContain("KITE  Kite pieces of A (20)");
  });

  it("names a second line's plate in the same code apart", () => {
    const silk = { ...BLACK, key: "PLA Silk|10101", line: "PLA Silk" };
    const two = writeRecipes(groupByColor([demand(A, "Kite", BLACK, 1), demand(A, "Star", silk, 3)]), "p", [], () => null);
    expect(two.map((w) => w.name)).toEqual(["p-10101", "p-pla-silk-10101"]);
  });
});

describe("normalHex", () => {
  it("drops the catalog's alpha and lowercases; refuses what is not a hex", () => {
    expect(normalHex("#E5B03DFF")).toBe("#e5b03d");
    expect(normalHex("56B7E6")).toBe("#56b7e6");
    expect(normalHex("#fff")).toBeNull();
  });
});
