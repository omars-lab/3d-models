import { describe, expect, it } from "vitest";
import { parse as parseYaml } from "yaml";
import { COLOR_AT_SEND, type Demand, type PlateColor, groupByColor, itemLabels, normalHex, pieceGroups, readPiecesBkr, writeRecipes } from "./by-color.js";

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
      pieces: {},
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

// One piece at a time (piece colors phase 5): the Lab's line for a kite taken out of its ring, in its
// own name, ahead of the orbit lines. Face 13 is one of orbit 1's ten.
const ORBIT_1_FACES = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20];
const ONE_KITE = BKR.replace("Star = #2f6db5", "Star = #2f6db5\nKite_13 = #2f6db5").replace(
  "fill faces where orbit == 0",
  "fill faces where index == 13 color Kite_13\nfill faces where orbit == 0",
);
const BANDS_FACES = BANDS.map((b) => ({ ...b, faces: b.orbit === 1 ? ORBIT_1_FACES : [100 + b.orbit] }));

describe("pieceGroups — one piece taken out of its ring", () => {
  it("prints the piece under its own name and one fewer in its ring", () => {
    expect(readPiecesBkr(ONE_KITE).pieces).toEqual({ 13: "Kite_13" });
    const bands = BANDS_FACES.map((b) => (b.orbit === 1 ? { ...b, color: "Kite, Kite_13" } : b));
    expect(pieceGroups(readPiecesBkr(ONE_KITE), bands)).toEqual([
      { piece: "Middle", orbits: [0], members: 1, hex: "#6b4e9b" },
      { piece: "Kite", orbits: [1], members: 9, hex: "#e05a47" },
      { piece: "Kite_13", orbits: [1], members: 1, hex: "#2f6db5" },
      { piece: "Star", orbits: [3, 4], members: 20, hex: "#2f6db5" },
    ]);
  });

  it("joins a piece taken out under another group's name to that group", () => {
    const toStar = ONE_KITE.replace("color Kite_13", "color Star");
    const groups = pieceGroups(readPiecesBkr(toStar), BANDS_FACES);
    expect(groups.find((g) => g.piece === "Kite")?.members).toBe(9);
    expect(groups.find((g) => g.piece === "Star")).toEqual({ piece: "Star", orbits: [1, 3, 4], members: 21, hex: "#2f6db5" });
  });

  it("refuses a one-piece line after an orbit line, which never wins", () => {
    const late = BKR + "\nfill faces where index == 13 color Kite";
    expect(() => readPiecesBkr(late)).toThrow("line 13: a one-piece `fill` after the orbit line on line 5 never wins");
  });

  it("refuses when bands lists no faces, names the orbit differently, or the face is in no loose orbit", () => {
    expect(() => pieceGroups(readPiecesBkr(ONE_KITE), BANDS)).toThrow("orbit 0: bands lists no faces");
    expect(() => pieceGroups(readPiecesBkr(ONE_KITE), BANDS_FACES.map((b) => (b.orbit === 1 ? { ...b, color: "Kite" } : b)))).toThrow(
      "loose orbit 1: the .bkr fills it as Kite, Kite_13, bands says Kite",
    );
    const stray = ONE_KITE.replace("index == 13", "index == 99");
    expect(() => pieceGroups(readPiecesBkr(stray), BANDS_FACES)).toThrow("face 99: taken out by `index` but in no loose orbit");
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

  it("names each plate by its color code and writes the profile for its line, with no color in it", () => {
    expect(written.map((w) => w.name)).toEqual(["fixture-t-10100", "fixture-t-10101"]);
    const recipe = parseYaml(written[1]!.text) as { bed: string; profile: Record<string, string>; items: Array<Record<string, unknown>> };
    expect(recipe.bed).toBe("x2d");
    // The color is named at the send, never fixed in a recipe (call 18): the profile has no `color`.
    expect(recipe.profile).toEqual({
      settings: "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D",
      filament: "Bambu PLA Basic @BBL X2D 0.4 nozzle",
    });
    expect(written[1]!.text).not.toMatch(/^\s+color:/m);
    expect(written[1]!.text).toContain(`# ${COLOR_AT_SEND}`);
    expect(written[1]!.text.split("\n")[0]).toContain("#000000");
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
