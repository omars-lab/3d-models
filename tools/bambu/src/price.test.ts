import { describe, expect, it } from "vitest";
import type { Prices } from "./by-color-costs.js";
import { type Basis, type Settings, checkSettings, priceOf, resolveStorePrices, scaleBasis, scenarios, sweep } from "./price.js";

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
    expect(market.missing).toEqual(["market price each", "monthly fixed costs"]);
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
