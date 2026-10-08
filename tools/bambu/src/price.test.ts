import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { parse as parseYaml } from "yaml";
import { describe, expect, it } from "vitest";
import type { Prices } from "./by-color-costs.js";
import type { Plan } from "./order.js";
import {
  type Basis,
  type ScenarioInputs,
  type ScenarioRow,
  type Settings,
  basisOf,
  checkSettings,
  priceBreaks,
  priceOf,
  resolveStorePrices,
  scaleBasis,
  scenarios,
  sweep,
} from "./price.js";

// The price (order-driven-lab-design §9.3, §9.7) one rule at a time. The fixtures under
// test/fixtures/orders run the same code on real plans (`bambu order fixtures`), and fixture 1's
// README works them by hand; these pin the rules a golden file can hide: an empty setting against a
// zero, a near line name, a corrected plate beside a floor one, a set row's own cost.

// FIXTURE: made-up settings, whole numbers and rates of 1.
const FULL: Settings = {
  price_per_gram: { "PLA Basic": 1 },
  printer_watts: 1000,
  electricity_rate: 1,
  printer_price: 100,
  payback_hours: 100,
  warm_up_minutes: 0,
  good_plate_share: 1,
  hands_on_minutes: 60,
  labor_rate: 1,
  packaging: 1,
  fee_percent: 0,
  fixed_fee: 0,
  markup: 1,
};

/** One coaster on one plate: 10 g, 60 minutes, corrected unless `floor`. */
function basis(floor = false, line = "PLA Basic"): Basis {
  return {
    order: "FIXTURE-T",
    coasters: 1,
    plates: [{ plate: "t", line, code: "10101", name: "Black", note: null, grams: 10, minutes: 60, floor, beds: 1 }],
    scaled: null,
  };
}

describe("an empty setting is never a zero", () => {
  it("prices packaging 0, and names packaging when it is empty", () => {
    // material 10, power 1, wear 1, labor 1: made 12; cost 12 + packaging
    expect(priceOf(basis(), { ...FULL, packaging: 0 }).cost.value).toBe(13);
    const empty = priceOf(basis(), { ...FULL, packaging: null });
    expect(empty.cost.value).toBeNull();
    expect(empty.break_even.value).toBeNull();
    expect(empty.suggested.value).toBeNull();
    expect(empty.empty).toEqual(["packaging"]);
  });

  it("still shows the lines that do not need the empty setting", () => {
    const p = priceOf(basis(), { ...FULL, packaging: null });
    expect(p.material.value).toBe(10);
    expect(p.made.value).toBe(12);
    expect(p.labor.value).toBe(1);
  });

  it("names every empty setting when none is filled", () => {
    const p = priceOf(basis(), {});
    expect(p.suggested.value).toBeNull();
    expect(p.empty).toContain("price per gram of PLA Basic");
    expect(p.empty).toContain("markup");
    expect(p.empty).toContain("warm-up minutes");
  });
});

describe("a price per gram is the line's own", () => {
  it("does not lend PLA Silk+'s price to PLA Silk", () => {
    const p = priceOf(basis(false, "PLA Silk"), { ...FULL, price_per_gram: { "PLA Silk+": 1 } });
    expect(p.material.value).toBeNull();
    expect(p.empty).toEqual(["price per gram of PLA Silk"]);
  });

  it("leaves a line the store file lacks empty, and says so", () => {
    const prices: Prices = { read: "2026-10-05", source: "test", lines: { "PLA Silk+": { refill: 15, spool: 18 } } };
    const { settings, notes } = resolveStorePrices({ price_per_gram: "store spool" }, prices, ["PLA Silk", "PLA Silk+"]);
    expect(settings.price_per_gram).toEqual({ "PLA Silk": null, "PLA Silk+": 0.018 });
    expect(notes.some((n) => n.startsWith("PLA Silk: the store file lists no price"))).toBe(true);
  });

  it("keeps a typed number beside a store tier for another line", () => {
    const prices: Prices = { read: "2026-10-05", source: "test", lines: { "PLA Basic": { refill: 16 } } };
    const { settings } = resolveStorePrices({ price_per_gram: { "PLA Basic": "store refill", "PLA Matte": 0.02 } }, prices, ["PLA Basic"]);
    expect(settings.price_per_gram).toEqual({ "PLA Basic": 0.016, "PLA Matte": 0.02 });
  });
});

describe("floor", () => {
  it("marks every amount built on sliced-only minutes, and not the grams-only ones", () => {
    const p = priceOf(basis(true), FULL);
    expect(p.floor).toBe(true);
    expect(p.power.floor).toBe(true);
    expect(p.suggested.floor).toBe(true);
    expect(p.material.floor).toBe(false);
    expect(priceOf(basis(false), FULL).suggested.floor).toBe(false);
  });
});

describe("the scenarios", () => {
  it("works the set of 6 on its own six coasters, not the plan's cost each", () => {
    // Two coasters on a plate that takes 1 hour; at 6 coasters each plate takes 3 beds.
    const b: Basis = { ...basis(), coasters: 2 };
    const s = { ...FULL, warm_up_minutes: 60, packaging: 6, scenarios: { set_of_6: 600 } };
    const rows = scenarios(b, s);
    const own = rows.find((r) => r.strategy === "cost-plus")!;
    const six = rows.find((r) => r.strategy === "set of 6")!;
    expect(six.coasters).toBe(6);
    expect(six.scaled).not.toBeNull();
    expect(six.cost_each).not.toBe(own.cost_each);
    // six: 30 g, 180 min + 3 beds × 60 = 6 h; made 30 + 6 + 6 = 42; labor 6; packaging 6: 54 ÷ 6
    expect(six.cost_each).toBe(9);
  });

  it("says never, and tags below break-even, at a margin of zero or less", () => {
    const rows = scenarios(basis(), { ...FULL, scenarios: { monthly_fixed_costs: 100, market_each: 14, story_each: 15 } });
    const at = rows.find((r) => r.strategy === "market range")!;
    expect(at.margin_each).toBe(0);
    expect(at.to_cover).toBe("never");
    expect(at.below_break_even).toBe(true);
    const above = rows.find((r) => r.strategy === "story, premium")!;
    expect(above.to_cover).toBe(100);
    expect(above.below_break_even).toBe(false);
  });

  it("names the empty input of a row and leaves the others standing", () => {
    const rows = scenarios(basis(), FULL);
    const market = rows.find((r) => r.strategy === "market range")!;
    expect(market.price_each).toBeNull();
    expect(market.missing).toEqual(["market price each", "monthly fixed costs", "coasters a month"]);
    expect(rows.find((r) => r.strategy === "cost-plus")!.price_each).toBe(28);
  });
});

describe("the price sweep", () => {
  it("gives the margin the scenario row gives at the same price", () => {
    const s = { ...FULL, fee_percent: 0.1, fixed_fee: 1, scenarios: { monthly_fixed_costs: 100 } };
    const own = scenarios(basis(), s).find((r) => r.strategy === "cost-plus")!;
    const [at] = sweep(basis(), s, [own.price_each!]);
    expect(at!.margin_each).toBe(own.margin_each);
    expect(at!.to_cover).toBe(own.to_cover);
  });

  it("tags a price below the cost, and none at or above it", () => {
    // cost 14 each, no fees: 10 loses 4, 14 makes nothing, 20 makes 6
    const rows = sweep(basis(), { ...FULL, scenarios: { monthly_fixed_costs: 60 } }, [10, 14, 20]);
    expect(rows.map((r) => r.margin_each)).toEqual([-4, 0, 6]);
    expect(rows.map((r) => r.below_break_even)).toEqual([true, true, false]);
    expect(rows.map((r) => r.to_cover)).toEqual(["never", "never", 10]);
  });

  it("names what the margin needs when a setting is empty, and still shows the price tried", () => {
    const [at] = sweep(basis(), { ...FULL, packaging: null }, [20]);
    expect(at!.price_each).toBe(20);
    expect(at!.margin_each).toBeNull();
    expect(at!.missing).toContain("packaging");
  });
});

// §9.7's what-if and price breaks, on fixture 1's plan and FIXTURE settings (X = 40 and the made-up
// breaks of the worked example). Each test is one PASS or FAIL line of §9.7's validator; the FAIL
// lines are the wrong ways of working it, each checked to give a number the right way does not.
const FX1 = join(dirname(fileURLToPath(import.meta.url)), "..", "test", "fixtures", "orders", "01-ice-to-navy");
const fx1 = basisOf(JSON.parse(readFileSync(join(FX1, "expected-plan.json"), "utf8")) as Plan);
const fx1Settings = checkSettings(parseYaml(readFileSync(join(FX1, "settings.fixture.yaml"), "utf8"))) as Settings;
const withInputs = (more: ScenarioInputs): Settings => ({ ...fx1Settings, scenarios: { ...fx1Settings.scenarios, ...more } });
const pick = (rows: ScenarioRow[], strategy: string) => rows.find((r) => r.strategy === strategy)!;
const costPlusAt = (x: number | null) => pick(scenarios(fx1, withInputs({ coasters_a_month: x })), "cost-plus");

describe("make and sell X a month", () => {
  it("PASS: the cost-plus row at X = 40 shows revenue $6,873.17, margin $2,749.27 and profit $1,749.27", () => {
    const row = costPlusAt(40);
    expect([row.price_each, row.margin_each, row.to_cover]).toEqual([171.83, 68.73, 15]);
    expect([row.revenue_month, row.margin_month, row.profit_month]).toEqual([6873.17, 2749.27, 1749.27]);
  });

  it("FAIL: profit worked per coaster and never multiplied by X ($68.73 − $1,000 = −$931.27)", () => {
    const row = costPlusAt(40);
    expect(row.profit_month).not.toBe(Math.round((row.margin_each! - 1000) * 100) / 100);
    expect(row.profit_month).not.toBe(-931.27);
    // and it moves with X, by the margin each per coaster
    expect(costPlusAt(41).profit_month!).toBeCloseTo(row.profit_month! + 68.73, 1);
  });

  it("PASS: profit is above zero at X = 15 and below it at X = 14, where to cover says 15", () => {
    expect(costPlusAt(15).to_cover).toBe(15);
    expect(costPlusAt(15).profit_month).toBe(30.98);
    expect(costPlusAt(14).profit_month).toBe(-37.76);
    // and it agrees with "to cover" on every row: profit ≥ 0 exactly when X ≥ to cover
    for (const x of [14, 15, 37, 40, 77, 110]) {
      for (const r of [...scenarios(fx1, withInputs({ coasters_a_month: x })), ...priceBreaks(fx1, withInputs({ coasters_a_month: x }))]) {
        if (r.to_cover === "never") expect(r.profit_month!).toBeLessThan(0);
        else expect(r.profit_month! >= 0).toBe(x >= r.to_cover!);
      }
    }
  });

  it("FAIL: margin each rounded before it is multiplied, $68.73 × 40 = $2,749.20 against $2,749.27", () => {
    const row = costPlusAt(40);
    expect(row.margin_month).toBe(2749.27);
    expect(row.margin_month).not.toBe(Math.round(row.margin_each! * 40 * 100) / 100);
  });

  it("FAIL: an empty X shown as $0 revenue and −$1,000 profit; every what-if cell is a dash instead", () => {
    const empty = withInputs({ coasters_a_month: null });
    for (const r of [...scenarios(fx1, empty), ...priceBreaks(fx1, empty)]) {
      expect([r.revenue_month, r.margin_month, r.profit_month]).toEqual([null, null, null]);
      expect(r.missing).toEqual(["coasters a month"]);
      // the columns that do not need X still show
      expect(r.price_each).not.toBeNull();
      expect(r.to_cover).not.toBeNull();
    }
  });

  it("X = 0 is a number tried, not an empty one: no revenue, and the fixed costs lost", () => {
    const row = costPlusAt(0);
    expect([row.revenue_month, row.margin_month, row.profit_month]).toEqual([0, 0, -1000]);
  });

  it("shows dashes in the a-month columns when any other input of the row is empty, whatever X is", () => {
    const row = pick(scenarios(fx1, withInputs({ market_each: null })), "market range");
    expect([row.price_each, row.revenue_month, row.margin_month, row.profit_month]).toEqual([null, null, null, null]);
    const noFixed = pick(scenarios(fx1, withInputs({ monthly_fixed_costs: null })), "cost-plus");
    expect(noFixed.revenue_month).toBe(6873.17);
    expect(noFixed.margin_month).toBe(2749.27);
    expect(noFixed.profit_month).toBeNull();
    expect(noFixed.to_cover).toBeNull();
  });
});

describe("the price breaks", () => {
  it("PASS: every row of §9.7's worked table at X = 40, to the cent", () => {
    const got = priceBreaks(fx1, fx1Settings).map((r) => [r.strategy, r.coasters, r.price_each, r.cost_each, r.margin_each, r.to_cover, r.revenue_month, r.margin_month, r.profit_month]);
    expect(got).toEqual([
      ["single", 1, 150, 72.98, 46.02, 22, 6000, 1840.73, 840.73],
      ["set of 4", 4, 120, 68.48, 27.27, 37, 4800, 1090.73, 90.73],
      ["set of 6", 6, 102, 68.32, 13.12, 77, 4080, 524.73, -475.27],
      ["gift order", 8, 108, 67.98, 18.29, 55, 4320, 731.73, -268.27],
      ["café order", 24, 96, 67.65, 9.11, 110, 3840, 364.4, -635.6],
      ["wholesale", 24, 60, 67.65, -19.69, "never", 2400, -787.6, -1787.6],
    ]);
  });

  it("PASS: the set-of-6 row prices at $102.00, one break on the set-of-4 price, and costs an order of 6", () => {
    const six = pick(priceBreaks(fx1, fx1Settings), "set of 6");
    expect(six.price_each).toBe(102);
    expect(six.coasters).toBe(6);
    expect(six.scaled).not.toBeNull();
    expect(six.cost_each).toBe(68.32);
    expect(six.cost_each).not.toBe(pick(priceBreaks(fx1, fx1Settings), "set of 4").cost_each);
  });

  it("FAIL: the set-of-4 break applied a second time on the way to the set of 6 ($81.60 each, −$3.20, never)", () => {
    const six = pick(priceBreaks(fx1, fx1Settings), "set of 6");
    expect(six.price_each).not.toBe(81.6);
    expect(six.margin_each).not.toBe(-3.2);
    expect(six.to_cover).not.toBe("never");
    // the set-of-6 price does not move when only the set-of-4 break's second use would move it
    expect(six.price_each).toBeCloseTo(150 * (1 - 0.2) * (1 - 0.15), 9);
  });

  it("FAIL: a break taken off the Sets and bundles row's typed price; that row stays the typed set price", () => {
    const typed = (more: ScenarioInputs) => scenarios(fx1, withInputs(more));
    const noBreaks = { set_of_4_break: null, set_of_6_break: null };
    expect(pick(typed({}), "set of 4").price_each).toBe(110);
    expect(pick(typed({}), "set of 6").price_each).toBe(90);
    expect(pick(typed(noBreaks), "set of 4")).toEqual(pick(typed({}), "set of 4"));
    expect(pick(typed(noBreaks), "set of 6")).toEqual(pick(typed({}), "set of 6"));
  });

  it("PASS: a row at or below zero margin shows never and the below-break-even tag", () => {
    const whole = pick(priceBreaks(fx1, fx1Settings), "wholesale");
    expect(whole.to_cover).toBe("never");
    expect(whole.below_break_even).toBe(true);
    for (const r of priceBreaks(fx1, fx1Settings).filter((r) => r.strategy !== "wholesale")) expect(r.below_break_even).toBe(false);
  });

  it("takes the wholesale fee percent in place of the fee percent, on the wholesale row only", () => {
    const dearer = priceBreaks(fx1, withInputs({ wholesale_fee_percent: 0.25 }));
    // 60 × 0.75 − 1/24 − 67.65 = −22.69
    expect(pick(dearer, "wholesale").margin_each).toBe(-22.69);
    expect(pick(dearer, "café order").margin_each).toBe(9.11);
    const none = pick(priceBreaks(fx1, withInputs({ wholesale_fee_percent: null })), "wholesale");
    expect(none.price_each).toBe(60);
    expect(none.margin_each).toBeNull();
    expect(none.missing).toEqual(["wholesale fee percent"]);
  });

  it("shows dashes, and names the input, when a break, the single price or an order size is empty", () => {
    const noSingle = priceBreaks(fx1, withInputs({ single_each: null }));
    for (const r of noSingle) {
      expect([r.price_each, r.margin_each, r.to_cover, r.revenue_month, r.profit_month]).toEqual([null, null, null, null, null]);
      expect(r.missing).toContain("single price each");
    }
    const noGift = pick(priceBreaks(fx1, withInputs({ gift_coasters: null })), "gift order");
    expect(noGift.coasters).toBeNull();
    expect(noGift.price_each).toBe(108);
    expect([noGift.cost_each, noGift.margin_each, noGift.revenue_month]).toEqual([null, null, 4320]);
    expect(noGift.missing).toEqual(["gift-order coasters"]);
    const noBreak = pick(priceBreaks(fx1, withInputs({ set_of_6_break: null })), "set of 6");
    expect(noBreak.price_each).toBeNull();
    expect(noBreak.missing).toEqual(["set-of-6 break"]);
  });
});

describe("scaling", () => {
  it("adds a set of beds for each plan's worth of coasters started", () => {
    expect(scaleBasis(basis(), 3).plates[0]!.beds).toBe(3);
    expect(scaleBasis({ ...basis(), coasters: 4 }, 5).plates[0]!.beds).toBe(2);
    expect(scaleBasis({ ...basis(), coasters: 4 }, 1).plates[0]!.beds).toBe(1);
  });
});

describe("checkSettings", () => {
  it("refuses a misspelled setting, which would otherwise read as empty", () => {
    expect(() => checkSettings({ packageing: 2 })).toThrow(/unknown setting "packageing"/);
    expect(() => checkSettings({ scenarios: { set_of_5: 2 } })).toThrow(/unknown scenario input "set_of_5"/);
  });

  it("refuses a value that would not add up", () => {
    expect(() => checkSettings({ markup: "1" })).toThrow(/markup must be a number/);
    expect(() => checkSettings({ price_per_gram: { "PLA Basic": "cheap" } })).toThrow(/store <tier>/);
    expect(() => checkSettings({ price_per_gram: "store bulk" })).toThrow(/one of refill, spool/);
  });

  it("takes an empty value as empty", () => {
    expect(checkSettings({ packaging: null, price_per_gram: "store refill" })).toEqual({ packaging: null, price_per_gram: "store refill" });
  });
});
