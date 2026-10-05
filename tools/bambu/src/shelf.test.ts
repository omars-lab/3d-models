import { describe, expect, it } from "vitest";
import type { CatalogColor, Plan, PlanPlate } from "./order.js";
import { closes, parseShelf, sentTrays, shelfDiff, shelfReport } from "./shelf.js";
import { logRows } from "./timed-prints.js";

// The shelf (order-driven-lab-design §9.2) one rule at a time. The fixtures under
// test/fixtures/orders run the same code on real plans (`bambu order fixtures`); these pin the
// rules the fixtures do not reach: a tie between two spools, a plate with no grams, a send never
// closed.

const CATALOG: CatalogColor[] = [
  { code: "10100", line: "PLA Basic", name: "Jade White", hexes: ["#FFFFFFFF"] },
  { code: "10501", line: "PLA Basic", name: "Bambu Green", hexes: ["#00AE42FF"] },
  { code: "11100", line: "PLA Matte", name: "Ivory White", hexes: ["#FFFFFFFF"] },
  { code: "11602", line: "PLA Matte", name: "Dark Blue", hexes: ["#042F56FF"] },
];
const NOTES = new Map([["PLA Matte|11602", "a made-up store note"]]);

function plate(name: string, line: string, code: string, grams: number | null): PlanPlate {
  return {
    name,
    color: { line, code, hex: "#000000", name: null, note: null },
    settings: "",
    filament: "",
    recipe_hash: "",
    items: [],
    source: grams === null ? "none" : "frozen",
    beds: 1,
    sliced_minutes: 10,
    grams,
    ratio: null,
    minutes: null,
    floor: true,
    nearest_unused: null,
    sendable: true,
    why_not: null,
  };
}
const plan = (order: string, plates: PlanPlate[]): Plan => ({
  order,
  plates,
  total: { plates: plates.length, beds: null, warm_ups: null, sliced_minutes: null, minutes: null, floor: true, grams: null },
  notes: [],
});

const log = (rows: string[]) => logRows(["| Time (UTC) | Event | Layer | Done | What the printer said |", "|---|---|---|---|---|", ...rows].join("\n"));
const SENT = (hex: string, tray: string, g: number) => `| 2026-10-04 18:35 | sent | | | fed ${hex} from ${tray}, ${g} g by the slice |`;
const END = (event: string) => `| 2026-10-04 20:14 | ${event} | 22/22 | 100% | FINISH |`;

const shelf = (yaml: string) => parseShelf(yaml);
const SPOOLS = `
spools:
  - { id: green-1, line: PLA Basic, code: "10501", start_grams: 1000 }
  - { id: blue-1, line: PLA Matte, code: "11602", start_grams: 40 }
`;

describe("sent rows", () => {
  it("reads every tray a send names, with its grams", () => {
    expect(sentTrays("fed #00AE42 from AMS 1 slot 4, 27.28 g by the slice; #042f56 from AMS 1 slot 1, 3 g by the slice")).toEqual([
      { hex: "#00ae42", tray: "AMS 1 slot 4", grams: 27.28 },
      { hex: "#042f56", tray: "AMS 1 slot 1", grams: 3 },
    ]);
  });

  it("closes a send on finished, failed or stopped, waits through lost, and lists an end with no send", () => {
    const got = closes([
      { plate: "a", rows: log([SENT("#00ae42", "AMS 1 slot 4", 27), "| 2026-10-04 19:00 | lost | | | |", END("failed")]) },
      { plate: "b", rows: log([END("finished")]) },
      { plate: "c", rows: log([SENT("#00ae42", "AMS 1 slot 4", 5)]) },
    ]);
    expect(got.closed.map((c) => [c.plate, c.event])).toEqual([["a", "failed"]]);
    expect(got.uncounted.map((u) => u.plate)).toEqual(["b"]);
    expect(got.not_closed.map((u) => [u.plate, u.why])).toEqual([["c", "no finished, failed or stopped row yet"]]);
  });
});

describe("the shelf", () => {
  const base = { catalog: CATALOG, notes: NOTES };

  it("a print takes its slice grams off the spool, finished or failed", () => {
    for (const end of ["finished", "failed"]) {
      const r = shelfReport({ ...base, shelf: shelf(SPOOLS), orders: [], logs: [{ plate: "a", rows: log([SENT("#00ae42", "AMS 1 slot 4", 27), END(end)]) }] });
      expect(r.spools.find((s) => s.id === "green-1")!.on_hand).toBe(973);
    }
  });

  it("two open orders hold the sum, and a color 1 g short buys one spool with its note", () => {
    const r = shelfReport({
      ...base,
      shelf: shelf(SPOOLS),
      orders: [
        { status: "open", plan: plan("O-1", [plate("o-1-11602", "PLA Matte", "11602", 20)]) },
        { status: "open", plan: plan("O-2", [plate("o-2-11602", "PLA Matte", "11602", 21)]) },
        { status: "closed", plan: plan("O-3", [plate("o-3-11602", "PLA Matte", "11602", 500)]) },
      ],
      logs: [],
    });
    const blue = r.colors.find((c) => c.code === "11602")!;
    expect([blue.held, blue.available]).toEqual([41, -1]);
    expect(r.buy).toEqual([{ line: "PLA Matte", code: "11602", name: "Dark Blue", short_grams: 1, spools: 1, note: "a made-up store note" }]);
  });

  it("a plate that printed to the end stops holding; a failed one keeps holding", () => {
    const orders = [{ status: "open" as const, plan: plan("O-1", [plate("o-1-10501", "PLA Basic", "10501", 27)]) }];
    const held = (end: string) =>
      shelfReport({ ...base, shelf: shelf(SPOOLS), orders, logs: [{ plate: "o-1-10501", rows: log([SENT("#00ae42", "AMS 1 slot 4", 27), END(end)]) }] }).colors.find(
        (c) => c.code === "10501",
      )!.held;
    expect(held("finished")).toBe(0);
    expect(held("failed")).toBe(27);
  });

  it("a hex two colors share is not guessed, unless a spool's tray says which", () => {
    const two = `
spools:
  - { id: jade-1, line: PLA Basic, code: "10100", start_grams: 1000 }
  - { id: ivory-1, line: PLA Matte, code: "11100", start_grams: 1000 TRAY }
`;
    const logs = [{ plate: "a", rows: log([SENT("#ffffff", "AMS 1 slot 2", 10), END("finished")]) }];
    const r = shelfReport({ ...base, shelf: shelf(two.replace(" TRAY", "")), orders: [], logs });
    expect(r.unmatched.map((u) => u.why)).toEqual(['#ffffff is PLA Basic 10100 and PLA Matte 11100; set tray: "AMS 1 slot 2" on the spool it was']);
    expect(r.spools.every((s) => s.used_grams === 0)).toBe(true);
    const t = shelfReport({ ...base, shelf: shelf(two.replace(" TRAY", ', tray: "AMS 1 slot 2"')), orders: [], logs });
    expect(t.spools.find((s) => s.id === "ivory-1")!.on_hand).toBe(990);
  });

  it("a plate with no grams makes its color's hold unknown, never zero, and buys nothing", () => {
    const r = shelfReport({ ...base, shelf: shelf(SPOOLS), orders: [{ status: "open", plan: plan("O-1", [plate("p", "PLA Matte", "11602", null)]) }], logs: [] });
    const blue = r.colors.find((c) => c.code === "11602")!;
    expect([blue.held, blue.available]).toEqual([null, null]);
    expect(r.buy).toEqual([]);
  });

  it("a correction moves the spool, and the diff names what moved", () => {
    const yaml = SPOOLS.replace("start_grams: 40 }", "start_grams: 40, corrections: [{ date: 2026-10-05, grams: -4, why: weighed }] }");
    const got = shelfReport({ ...base, shelf: shelf(yaml), orders: [], logs: [] });
    const was = shelfReport({ ...base, shelf: shelf(SPOOLS), orders: [], logs: [] });
    expect(got.spools.find((s) => s.id === "blue-1")!.on_hand).toBe(36);
    expect(shelfDiff(was, got)).toContain("PLA Matte 11602: on hand 36, expected 40");
  });
});
