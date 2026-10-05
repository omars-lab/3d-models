// Tests for the cost view of `plates by-color --costs` (piece colors phase 2, infill-color-ux-design
// §6 and §7). The design names two: a one-color plate's minutes are the ones `bambu validate sliced`
// prints for the same slice, and a plate that spills onto a second bed shows that bed, not a total.
//
// Two fixtures are real: test/fixtures/gbv-by-color/pink.slice_info.config is the pink plate of gBV
// as `plates by-color --costs --slice` sliced it on 2026-10-05 (Bambu Studio 02.08.02.61), and the
// minis-05 spill is the one beds.test.ts reads.

import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { SWAP, costRoutes, pricePerKg, type CostInputs, type Prices } from "./by-color-costs.js";
import type { PlateColor, PlateItem, WrittenRecipe } from "./by-color.js";
import { sliceFacts } from "./order-io.js";
import type { SliceFacts } from "./order.js";
import { layersOf, minutesOf, sliceNumbers } from "./slice-numbers.js";

const fixtures = join(dirname(fileURLToPath(import.meta.url)), "..", "test", "fixtures");
const pinkInfo = readFileSync(join(fixtures, "gbv-by-color", "pink.slice_info.config"), "utf8");
const spillInfo = readFileSync(join(fixtures, "minis-05", "spilled.slice_info.config"), "utf8");

const PRICES: Prices = {
  read: "2026-10-04",
  source: "docs/research/2026-10-04-coaster-pricing.md",
  lines: { "PLA Basic": { refill: 15.99, spool: 18.99, ten_refill: 11.19 }, "PLA Sparkle": { spool: 24.99 } },
};

const C = "bikar:patterns/Constructions/gBV-minimal-coaster.bkr";
const color = (hex: string, line = "PLA Basic"): PlateColor => ({ key: hex, hex, line, code: null, name: null, note: null });
const item = (piece: string | null, count = 1): PlateItem => ({ construction: C, params: { size: 100 }, piece, count, rank: 0 });
const recipe = (name: string, c: PlateColor, items: PlateItem[]): WrittenRecipe => ({ name, plate: { color: c, items }, text: "", hash: "" });
const slice = (over: Partial<SliceFacts>): SliceFacts => ({ recipe: "x", beds: 1, minutes: 30, grams: 10, layers: 22, bed_minutes: [30], ...over });

const BLACK = color("#000000");
const PINK = color("#F5547C");
const GREEN = color("#00AE42");

function inputs(over: Partial<CostInputs>): CostInputs {
  return {
    coasters: 1,
    perColor: [],
    wholeSet: null,
    pieceCount: (it) => (it.piece === "Kite" ? 6 : 1),
    prices: PRICES,
    tier: "refill",
    ratio: () => null,
    ...over,
  };
}

describe("layersOf", () => {
  it("counts the layers of a range that ends at 21 as 22", () => {
    expect(layersOf(`<layer_filament_list filament_list="0" layer_ranges="0 21" />`)).toBe(22);
    expect(layersOf(pinkInfo)).toBe(22);
  });

  it("is null when the slice lists no ranges", () => {
    expect(layersOf("<config></config>")).toBeNull();
  });
});

describe("one plate per color", () => {
  it("shows the minutes `validate sliced` reads off the same slice", () => {
    const facts = sliceFacts("gbv-by-color-f5547c", pinkInfo);
    const read = sliceNumbers(pinkInfo);
    expect(facts.minutes).toBe(minutesOf(read.predictionS!));
    expect(facts.minutes).toBe(16.5); // prediction 992 s
    expect(facts.grams).toBe(2.8);

    const costs = costRoutes(inputs({ perColor: [{ recipe: recipe("gbv-by-color-f5547c", PINK, [item("Kite", 2)]), slice: facts }] }));
    const plate = costs.routes[0]!.plates[0]!;
    expect(plate.minutes).toBe(facts.minutes);
    expect(plate.sliced_minutes).toBe(facts.minutes);
    expect(plate.source).toBe("slice");
    expect(plate.sendable).toBe(true);
    expect(plate.usd).toBe(0.04); // 2.8 g at $15.99 a kg
  });

  it("shows each bed of a plate that spills onto a second one, and does not let it go out", () => {
    const facts = sliceFacts("minis-05", spillInfo);
    expect(facts.beds).toBe(2);
    expect(facts.bed_minutes).toEqual([minutesOf(15665), minutesOf(3349)]);

    const costs = costRoutes(inputs({ perColor: [{ recipe: recipe("minis-05", BLACK, [item(null, 12)]), slice: facts }] }));
    const r = costs.routes[0]!;
    const plate = r.plates[0]!;
    expect(plate.bed_minutes).toEqual([261.1, 55.8]);
    expect(plate.sendable).toBe(false);
    expect(plate.notes.join(" ")).toMatch(/spills onto 2 beds: a send prints bed 1 only/);
    expect(r.total.sends).toBe(2);
  });

  it("shows no time, grams or dollars for a plate with no slice, and says why", () => {
    const costs = costRoutes(inputs({ perColor: [{ recipe: recipe("a", BLACK, [item(null)]), slice: null }] }));
    const plate = costs.routes[0]!.plates[0]!;
    expect([plate.minutes, plate.grams, plate.usd, plate.source]).toEqual([null, null, null, "none"]);
    expect(costs.routes[0]!.total.minutes).toBeNull();
    expect(costs.notes.join(" ")).toMatch(/pass --slice/);
  });
});

describe("the whole set, and the one swapping plate", () => {
  const perColor = [
    { recipe: recipe("g-000000", BLACK, [item(null)]), slice: slice({ minutes: 57, grams: 16 }) },
    { recipe: recipe("g-f5547c", PINK, [item("Kite", 2)]), slice: slice({ minutes: 16.5, grams: 3 }) },
    { recipe: recipe("g-00ae42", GREEN, [item("Hex")]), slice: slice({ minutes: 24, grams: 8 }) },
  ];
  const whole = { recipe: recipe("g-whole-set-000000", BLACK, [item(null), item("Kite", 2), item("Hex")]), slice: slice({ minutes: 86.7, grams: 27, layers: 22 }) };

  it("prints the whole set once per color and names what each print leaves over", () => {
    const r = costRoutes(inputs({ perColor, wholeSet: whole })).routes.find((x) => x.key === "whole-set")!;
    expect(r.plates).toHaveLength(3);
    expect(r.total.minutes).toBe(260.1);
    expect(r.plates[0]!.notes).toEqual(["keep the #000000 ones; 13 pieces left over"]); // 2 Kites × 6 + a Hex
    expect(r.plates[1]!.notes).toEqual(["keep the #F5547C ones; 1 frame and 1 piece left over"]);
    expect(r.left_over).toBe("2 frames and 26 pieces");
  });

  it("adds a swap a layer for each color past the first, at phones-01's minutes and grams", () => {
    const r = costRoutes(inputs({ perColor, wholeSet: whole })).routes.find((x) => x.key === "one-plate")!;
    const p = r.plates[0]!;
    expect(p.swaps).toBe(44); // 22 layers × 2
    expect(p.swap_minutes).toBe(Math.round(44 * SWAP.minutes * 10) / 10);
    expect(p.minutes).toBe(Math.round((86.7 + 44 * SWAP.minutes) * 10) / 10);
    expect(p.grams).toBe(Math.round((27 + 44 * SWAP.grams) * 100) / 100);
    expect([p.source, p.sendable, r.fits_rule]).toEqual(["estimate", false, false]);
    expect(p.notes.join(" ")).toMatch(/^about 44 swaps/);
    expect(p.notes.some((n) => n.startsWith("low:"))).toBe(true);
  });

  it("does not call two colors a low estimate", () => {
    const two = costRoutes(inputs({ perColor: perColor.slice(0, 2), wholeSet: whole })).routes.find((x) => x.key === "one-plate")!;
    expect(two.plates[0]!.swaps).toBe(22);
    expect(two.plates[0]!.notes.some((n) => n.startsWith("low:"))).toBe(false);
  });
});

describe("pricePerKg", () => {
  it("uses the tier asked for when it was read", () => {
    expect(pricePerKg(PRICES, "PLA Basic", "ten_refill")).toEqual({ usd_per_kg: 11.19, tier: "ten_refill", note: null });
  });

  it("falls back to the spool price and says so", () => {
    const p = pricePerKg(PRICES, "PLA Sparkle", "refill");
    expect(p?.usd_per_kg).toBe(24.99);
    expect(p?.tier).toBe("spool");
    expect(p?.note).toMatch(/no refill price read; used its spool price/);
  });

  it("gives no price for a line the file does not list, and the plate no dollars", () => {
    expect(pricePerKg(PRICES, "PLA Galaxy", "refill")).toBeNull();
    const costs = costRoutes(inputs({ perColor: [{ recipe: recipe("a", color("#123456", "PLA Galaxy"), [item(null)]), slice: slice({}) }] }));
    expect(costs.routes[0]!.plates[0]!.usd).toBeNull();
    expect(costs.routes[0]!.plates[0]!.grams).toBe(10);
    expect(costs.notes).toContain("PLA Galaxy: no price in the price file, so its plates show no dollars");
  });
});
