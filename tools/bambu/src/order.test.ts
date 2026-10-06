import { describe, expect, it } from "vitest";
import type { PieceGroup } from "./by-color.js";
import { type CatalogColor, type Plan, type SliceFacts, checkPlan, lookupCode, lookupColor, parseOrder, planOrder } from "./order.js";
import type { TimedRun } from "./timed-prints.js";

// The planner and its check (order-driven-lab-design §9.1, §9.5) on a made-up construction, with no
// bikar and no slicer. The fixtures under test/fixtures/orders run the same code on the real gBV
// files (`bambu order fixtures`); these pin the rules one at a time, each with the plan that breaks it.

const FRAME = "bikar:patterns/Constructions/T-minimal-coaster.bkr";
const PIECES = "bikar:patterns/Constructions/T-minimal-pieces.bkr";
const GROUPS: PieceGroup[] = [
  { piece: "Middle", orbits: [0], members: 1, hex: "#6b4e9b" },
  { piece: "Kite", orbits: [1], members: 10, hex: "#e05a47" },
  { piece: "Star", orbits: [3], members: 10, hex: "#2f6db5" },
  { piece: "Outer", orbits: [4], members: 10, hex: "#3a9a5b" },
];
const groupsOf = (c: string) => {
  if (c !== PIECES) throw new Error(`no groups for ${c}`);
  return GROUPS;
};

const CATALOG: CatalogColor[] = [
  { code: "11100", line: "PLA Matte", name: "Ivory White", hexes: ["#FFFFFFFF"] },
  { code: "11603", line: "PLA Matte", name: "Sky Blue", hexes: ["#56B7E6FF"] },
  { code: "11602", line: "PLA Matte", name: "Dark Blue", hexes: ["#042F56FF"] },
  { code: "10101", line: "PLA Basic", name: "Black", hexes: ["#000000FF"] },
  { code: "13401", line: "PLA Silk", name: "Gold", hexes: ["#E5B03DFF"] },
  { code: "13901", line: "PLA Silk", name: "Gilded Rose", hexes: ["#FF9425FF", "#C16784FF"], kind: "multi" },
  { code: "13906", line: "PLA Silk", name: "South Beach", hexes: ["#F772A4FF", "#00918BFF"], kind: "gradient" },
];
const NOTES = new Map([["PLA Silk|13401", "not on the US store, 2026-10-04"]]);

const BASIC = "Bambu PLA Basic @BBL X2D 0.4 nozzle";
const SETTINGS = "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D";
const RUNS: TimedRun[] = [
  { plate: "a", started: "2026-10-04 00:32", watched: 48, sliced: 42, settings: SETTINGS, filament: BASIC },
  { plate: "b", started: "2026-10-04 18:37", watched: 97, sliced: 86, settings: SETTINGS, filament: BASIC },
  { plate: "c", started: "2026-10-04 12:53", watched: 62, sliced: 22, settings: SETTINGS, filament: `${BASIC};${BASIC}` },
];

function order(colors: Record<string, [string, string]>, frame: [string, string] = ["PLA Matte", "11100"], count = 2) {
  const pick = ([line, code]: [string, string]) => `{ line: ${line}, code: "${code}" }`;
  return parseOrder(
    [
      'id: "FIXTURE-T"',
      "lines:",
      `  - count: ${count}`,
      "    frame:",
      `      construction: ${FRAME}`,
      "      params: { size: 100 }",
      `      color: ${pick(frame)}`,
      "    pieces:",
      `      construction: ${PIECES}`,
      "      params: { size: 100, gap: 0 }",
      "      colors:",
      ...Object.entries(colors).map(([g, c]) => `        ${g}: ${pick(c)}`),
    ].join("\n"),
  );
}

const MATTE = { Middle: ["PLA Matte", "11603"], Kite: ["PLA Matte", "11603"], Star: ["PLA Matte", "11602"], Outer: ["PLA Matte", "11602"] } as Record<
  string,
  [string, string]
>;
const BLACK = { Middle: ["PLA Basic", "10101"], Kite: ["PLA Basic", "10101"], Star: ["PLA Basic", "10101"], Outer: ["PLA Basic", "10101"] } as Record<
  string,
  [string, string]
>;

function deps(slices: Record<string, SliceFacts> = {}) {
  return { color: (c: { line: string; code: string }) => lookupColor(CATALOG, NOTES, c), groupsOf, slices, runs: RUNS };
}

/** Plan once to learn the recipe hashes, then freeze a slice for each. */
function sliced(o: ReturnType<typeof order>, facts: (name: string) => Omit<SliceFacts, "recipe">) {
  const slices: Record<string, SliceFacts> = {};
  for (const p of planOrder(o, deps()).plan.plates) slices[p.recipe_hash] = { recipe: p.name, ...facts(p.name) };
  return { d: deps(slices), plan: planOrder(o, deps(slices)).plan };
}

const clone = (p: Plan): Plan => JSON.parse(JSON.stringify(p)) as Plan;

describe("parseOrder — the order file", () => {
  it("reads a line with no pieces: a frame alone is a valid line", () => {
    const o = parseOrder(`id: 7\nlines:\n  - count: 1\n    frame: { construction: ${FRAME}, color: { line: PLA Basic, code: 10101 } }\n`);
    expect(o.id).toBe("7");
    expect(o.lines[0]!.pieces).toBeNull();
    expect(o.lines[0]!.frame.color.code).toBe("10101");
  });

  it("names the field that is wrong", () => {
    expect(() => parseOrder("id: x\nlines: []\n")).toThrow("no `lines:`");
    expect(() => parseOrder(`id: x\nlines:\n  - count: 0\n    frame: { construction: ${FRAME}, color: { line: L, code: "1" } }\n`)).toThrow(
      "lines[0].count",
    );
    expect(() => parseOrder("id: x\nlines:\n  - count: 1\n")).toThrow("every line has a frame");
    expect(() => parseOrder(`id: x\nlines:\n  - count: 1\n    frame: { construction: a.stl, color: { line: L, code: "1" } }\n`)).toThrow(
      'must be "bikar:<path>.bkr"',
    );
    expect(() =>
      parseOrder(`id: x\nlines:\n  - count: 1\n    frame: { construction: ${FRAME}, params: { size: big }, color: { line: L, code: "1" } }\n`),
    ).toThrow("params.size: must be a number");
  });
});

describe("lookupColor — a color is a catalog spool", () => {
  it("carries the palette's store note", () => {
    const c = lookupColor(CATALOG, NOTES, { line: "PLA Silk", code: "13401" });
    expect(c).toMatchObject({ key: "PLA Silk|13401", hex: "#e5b03d", name: "Gold", note: "not on the US store, 2026-10-04" });
  });

  it("refuses a color the catalog does not have", () => {
    expect(() => lookupColor(CATALOG, NOTES, { line: "PLA Silk+", code: "13401" })).toThrow("not in the color catalog");
  });

  it("gives a two-color spool its first hex, the tray's, and says so", () => {
    const c = lookupColor(CATALOG, NOTES, { line: "PLA Silk", code: "13901" });
    expect(c.hex).toBe("#ff9425");
    expect(c.note).toContain("a 2-color spool (#ff9425, #c16784)");
  });

  it("says what a two-color spool does by the catalog's kind: side by side, or along the spool", () => {
    expect(lookupColor(CATALOG, NOTES, { line: "PLA Silk", code: "13901" }).note).toMatch(/side by side in the strand/);
    expect(lookupColor(CATALOG, NOTES, { line: "PLA Silk", code: "13906" }).note).toMatch(/shifts along the spool/);
  });

  it("finds a spool by its code alone, with its own line", () => {
    expect(lookupCode(CATALOG, NOTES, "11602")).toMatchObject({ line: "PLA Matte", name: "Dark Blue", hex: "#042f56" });
    expect(() => lookupCode(CATALOG, NOTES, "99999")).toThrow("no spool with this code");
    const twice = [...CATALOG, { code: "11602", line: "PLA Basic", name: "Clash", hexes: ["#111111FF"] }];
    expect(() => lookupCode(twice, NOTES, "11602")).toThrow("PLA Matte and PLA Basic both use this code");
  });
});

describe("planOrder — one plate per color", () => {
  it("puts two groups of one color on one plate, the frame on its own color's", () => {
    const { plan } = planOrder(order(MATTE), deps());
    expect(plan.plates.map((p) => [p.name, p.items.map((i) => `${i.count}×${i.piece ?? "frame"}`)])).toEqual([
      ["fixture-t-11100", ["2×frame"]],
      ["fixture-t-11603", ["2×Middle", "2×Kite"]],
      ["fixture-t-11602", ["2×Star", "2×Outer"]],
    ]);
  });

  it("refuses a group with no color and a color with no group", () => {
    const { Kite: _, ...noKite } = MATTE;
    expect(() => planOrder(order(noKite), deps())).toThrow("no color for Kite");
    expect(() => planOrder(order({ ...MATTE, Hex: ["PLA Matte", "11602"] }), deps())).toThrow("no group named Hex");
  });

  it("shows a Matte plate as floor, naming the Basic ratio it did not use", () => {
    const { plan } = sliced(order(MATTE), () => ({ beds: 1, minutes: 50, grams: 20 }));
    const p = plan.plates[0]!;
    expect(p.floor).toBe(true);
    expect(p.minutes).toBeNull();
    expect(p.nearest_unused).toMatchObject({ filament: BASIC, value: 1.13, prints: 2 });
    expect(plan.total).toMatchObject({ plates: 3, beds: 3, warm_ups: 3, sliced_minutes: 150, minutes: null, floor: true, grams: 60 });
  });

  it("corrects a Basic plate by the pooled one-filament ratio, not the two-filament print", () => {
    const { plan } = sliced(order(BLACK, ["PLA Basic", "10101"]), () => ({ beds: 1, minutes: 86, grams: 27 }));
    expect(plan.plates).toHaveLength(1);
    const p = plan.plates[0]!;
    expect(p.ratio).toEqual({ value: 1.13, prints: 2 }); // (48 + 97) / (42 + 86), phones-01's 62/22 left out
    expect(p.minutes).toBe(Math.round((86 * 145) / 128));
    expect(p.sendable).toBe(true);
  });

  it("marks a plate that spills onto a second bed as not sendable", () => {
    const { plan } = sliced(order(MATTE), (n) => ({ beds: n.endsWith("11100") ? 2 : 1, minutes: 50, grams: 20 }));
    const frames = plan.plates[0]!;
    expect(frames.sendable).toBe(false);
    expect(frames.why_not).toContain("spills onto 2 beds");
    expect(plan.total.warm_ups).toBe(4);
  });
});

describe("checkPlan — plate by plate, never by the total", () => {
  const o = order(MATTE);
  const { d, plan } = sliced(o, () => ({ beds: 1, minutes: 50, grams: 20 }));

  it("passes the planner's own plan", () => {
    expect(checkPlan(o, plan, d)).toEqual([]);
  });

  it("refuses one kite group moved to another color's plate, every total kept", () => {
    const wrong = clone(plan);
    const kite = wrong.plates[1]!.items.find((i) => i.piece === "Kite")!;
    kite.count = 1;
    wrong.plates[2]!.items.push({ ...kite, count: 1 });
    expect(wrong.total).toEqual(plan.total);
    expect(checkPlan(o, wrong, d).join("\n")).toContain("Kite: the order wants 20 PLA Matte|11603, the plan prints 10 PLA Matte|11602, 10 PLA Matte|11603");
  });

  it("refuses two plates in one color", () => {
    const wrong = clone(plan);
    const [first, ...rest] = wrong.plates[2]!.items;
    wrong.plates[2]!.items = [first!];
    wrong.plates.push({ ...wrong.plates[2]!, name: "extra", items: rest });
    wrong.total.plates = wrong.plates.length;
    expect(checkPlan(o, wrong, d).join("\n")).toContain("extra: a second plate in PLA Matte|11602");
  });

  it("refuses a bed count its slice does not have, though the total adds up", () => {
    const two = sliced(o, (n) => ({ beds: n.endsWith("11100") ? 2 : 1, minutes: 50, grams: 20 }));
    const wrong = clone(two.plan);
    wrong.plates[0]!.beds = 1;
    wrong.plates[0]!.sendable = true;
    const errors = checkPlan(o, wrong, two.d).join("\n");
    expect(errors).toContain("fixture-t-11100: 1 beds, its slice has 2");
    expect(errors).toContain("total: beds 4, its plates add to 3");
  });

  it("refuses a ratio the timed prints do not give, and corrected minutes on a floor plate", () => {
    const wrong = clone(plan);
    wrong.plates[0]!.ratio = { value: 1.13, prints: 2 };
    wrong.plates[0]!.minutes = 57;
    const errors = checkPlan(o, wrong, d).join("\n");
    expect(errors).toContain("a ratio, but no timed print used Bambu PLA Matte @BBL X2D 0.4 nozzle");
    expect(errors).toContain("corrected minutes on a floor plate");
  });

  it("refuses numbers for a recipe that was never sliced", () => {
    const wrong = clone(plan);
    wrong.plates[0]!.recipe_hash = "000000000000";
    const errors = checkPlan(o, wrong, d).join("\n");
    expect(errors).toContain("re-freeze the slices");
    expect(errors).toContain("but its order writes");
  });
});
