// What an order costs to make and what to ask for it (order-driven-lab-design §9.3 and §9.7,
// orders phase 3). Omar on call 13 of the 2026-10-05 page: "we should have different simulatons,
// how much it costs us to do 1 peice, 5 pieces, 10, 100, etc".
//
// Every input is a setting with a name. A setting left empty is never read as zero: each amount that
// needs it shows no number and names it, and the amounts that do not need it still show. Minutes with
// no timed print behind them are the sliced minutes, marked "floor", and so is everything built on
// them. Nothing here reads a file; the command passes in the plan and the settings.

import { type Prices, type Tier, TIERS, pricePerKg } from "./by-color-costs.js";
import type { Plan } from "./order.js";

/** The twelve settings of §9.3 (the selling fee is two numbers), and the scenario inputs of §9.7.
 *  A key left out, or set to null, is empty. */
export interface Settings {
  price_per_gram?: Record<string, number | null> | null; // US dollars a gram, by filament line
  printer_watts?: number | null;
  electricity_rate?: number | null; // US dollars a kWh
  printer_price?: number | null;
  payback_hours?: number | null; // the printer hours the printer price is spread over
  warm_up_minutes?: number | null; // per bed, the minutes a slice leaves out
  good_plate_share?: number | null; // 0.8 when four plates in five come out good
  hands_on_minutes?: number | null; // per coaster: clearing, pressing pieces in, packing
  labor_rate?: number | null; // US dollars an hour
  packaging?: number | null; // US dollars an order
  fee_percent?: number | null; // a share of the price: 0.11 is 11%
  fixed_fee?: number | null; // US dollars an order
  markup?: number | null; // added on top of break-even: 1 doubles it
  scenarios?: ScenarioInputs | null;
}

/** §9.7's inputs: not used by a quote, so not among the twelve. Each starts empty. */
export interface ScenarioInputs {
  monthly_fixed_costs?: number | null;
  market_each?: number | null; // a pick inside the market band, per coaster
  story_each?: number | null; // a pick above it, per coaster
  finish_each?: Record<string, number | null> | null; // a price per coaster, by filament line
  set_of_4?: number | null; // the price of the whole set
  set_of_6?: number | null;
  custom_design_minutes?: number | null; // the design time a custom theme takes, per order
  launch_discount?: number | null; // a share off the cost-plus price: 0.2 is 20% off
}

export const SETTING_KEYS = [
  "price_per_gram",
  "printer_watts",
  "electricity_rate",
  "printer_price",
  "payback_hours",
  "warm_up_minutes",
  "good_plate_share",
  "hands_on_minutes",
  "labor_rate",
  "packaging",
  "fee_percent",
  "fixed_fee",
  "markup",
  "scenarios",
] as const;

const SCENARIO_KEYS = [
  "monthly_fixed_costs",
  "market_each",
  "story_each",
  "finish_each",
  "set_of_4",
  "set_of_6",
  "custom_design_minutes",
  "launch_discount",
] as const;

/** The plain name of each setting, the one a page or a refusal shows. */
const NAME: Record<string, string> = {
  printer_watts: "printer watts",
  electricity_rate: "electricity rate",
  printer_price: "printer price",
  payback_hours: "payback hours",
  warm_up_minutes: "warm-up minutes",
  good_plate_share: "good-plate share",
  hands_on_minutes: "hands-on minutes",
  labor_rate: "labor rate",
  packaging: "packaging",
  fee_percent: "fee percent",
  fixed_fee: "fixed fee",
  markup: "markup",
  monthly_fixed_costs: "monthly fixed costs",
  market_each: "market price each",
  story_each: "story price each",
  set_of_4: "set of 4 price",
  set_of_6: "set of 6 price",
  custom_design_minutes: "custom design minutes",
  launch_discount: "launch discount",
};

/** A settings file as written: price per gram may say `store <tier>`, for the whole setting or one
 *  line, meaning the store's price at that tier from prices.yaml. `resolveStorePrices` turns it into
 *  numbers. */
export interface SettingsFile extends Omit<Settings, "price_per_gram"> {
  price_per_gram?: string | Record<string, number | string | null> | null;
}

function checkNumbers(where: string, m: Record<string, unknown>, skip: string[] = []): void {
  for (const [k, v] of Object.entries(m)) {
    if (skip.includes(k)) continue;
    if (v !== null && typeof v !== "number") throw new Error(`settings: ${where}${k} must be a number or empty, not ${JSON.stringify(v)}`);
  }
}

function isMapping(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

/** A settings file's keys and values, checked: a misspelled key would read as an empty setting and
 *  hide, and a value in quotes would not add up. */
export function checkSettings(raw: unknown): SettingsFile {
  if (raw === null || raw === undefined) return {};
  if (!isMapping(raw)) throw new Error("settings: expected a mapping of setting names");
  const s = raw;
  for (const k of Object.keys(s)) {
    if (!(SETTING_KEYS as readonly string[]).includes(k)) throw new Error(`settings: unknown setting "${k}" (known: ${SETTING_KEYS.join(", ")})`);
  }
  checkNumbers("", s, ["scenarios", "price_per_gram"]);
  const ppg = s.price_per_gram;
  if (typeof ppg === "string") storeTier(ppg);
  else if (isMapping(ppg)) {
    for (const [line, v] of Object.entries(ppg)) if (typeof v === "string") storeTier(v, line);
    checkNumbers("price_per_gram.", Object.fromEntries(Object.entries(ppg).filter(([, v]) => typeof v !== "string")));
  } else if (ppg !== null && ppg !== undefined) throw new Error("settings: price_per_gram must be a mapping of line to US dollars a gram, or `store <tier>`");
  const sc = s.scenarios;
  if (sc !== null && sc !== undefined) {
    if (!isMapping(sc)) throw new Error("settings: scenarios must be a mapping");
    for (const k of Object.keys(sc)) {
      if (!(SCENARIO_KEYS as readonly string[]).includes(k)) throw new Error(`settings: unknown scenario input "${k}" (known: ${SCENARIO_KEYS.join(", ")})`);
    }
    checkNumbers("scenarios.", sc, ["finish_each"]);
    const fe = sc.finish_each;
    if (fe !== null && fe !== undefined) {
      if (!isMapping(fe)) throw new Error("settings: scenarios.finish_each must be a mapping of line to a price each");
      checkNumbers("scenarios.finish_each.", fe);
    }
  }
  return s as SettingsFile;
}

/** The tier a `store <tier>` value names, or a refusal that lists the tiers. */
function storeTier(v: string, line?: string): Tier {
  const m = /^store (\S+)$/.exec(v.trim());
  if (!m || !(TIERS as string[]).includes(m[1]!)) {
    throw new Error(`settings: price_per_gram${line ? `.${line}` : ""} is "${v}"; a word value must be \`store <tier>\`, one of ${TIERS.join(", ")}`);
  }
  return m[1] as Tier;
}

/** Each `store <tier>` turned into the store's price a gram for the lines the order uses. A line the
 *  store file does not list stays empty, never the price of a line with a near name (PLA Silk is not
 *  PLA Silk+), and a note says which. */
export function resolveStorePrices(f: SettingsFile, prices: Prices | null, lines: string[]): { settings: Settings; notes: string[] } {
  const notes: string[] = [];
  const { price_per_gram: ppg, ...rest } = f;
  if (ppg === null || ppg === undefined) return { settings: rest, notes };
  const asked: Record<string, number | string | null> = typeof ppg === "string" ? Object.fromEntries(lines.map((l) => [l, ppg])) : ppg;
  const out: Record<string, number | null> = {};
  for (const [line, v] of Object.entries(asked)) {
    if (typeof v !== "string") {
      out[line] = v;
      continue;
    }
    const tier = storeTier(v, line);
    const used = prices ? pricePerKg(prices, line, tier) : null;
    if (!used) {
      out[line] = null;
      notes.push(`${line}: the store file lists no price for this line${prices ? ` (read ${prices.read})` : ""}, so its price per gram is empty`);
      continue;
    }
    out[line] = used.usd_per_kg / 1000;
    notes.push(`${line}: price per gram from the store, ${used.tier}, $${used.usd_per_kg} a kg${prices ? ` (read ${prices.read})` : ""}${used.note ? `; ${used.note}` : ""}`);
  }
  return { settings: { ...rest, price_per_gram: out }, notes };
}

// ── amounts that know what they are missing ─────────────────────────────────────────────────────────

/** An amount, or the empty settings that keep it from being worked out. `floor` means it rests on
 *  sliced minutes no timed print has corrected, so it is the least it can be. */
export interface Amount {
  value: number | null;
  floor: boolean;
  missing: string[];
}

function setting(name: string, v: number | null | undefined): Amount {
  return v === null || v === undefined ? { value: null, floor: false, missing: [name] } : { value: v, floor: false, missing: [] };
}

function known(value: number, floor = false): Amount {
  return { value, floor, missing: [] };
}

function combine(f: (...xs: number[]) => number, ...as: Amount[]): Amount {
  const missing = [...new Set(as.flatMap((a) => a.missing))];
  const floor = as.some((a) => a.floor);
  return { value: missing.length ? null : f(...as.map((a) => a.value!)), floor, missing };
}

function round(a: Amount, places = 2): Amount {
  const k = 10 ** places;
  return { ...a, value: a.value === null ? null : Math.round(a.value * k) / k };
}

// ── what the price is worked from ───────────────────────────────────────────────────────────────────

/** One plate's share of the order: what its color costs and how long it prints. */
export interface BasisPlate {
  plate: string;
  line: string;
  code: string | null;
  name: string | null;
  note: string | null;
  grams: number | null;
  minutes: number | null; // corrected where a ratio matched, else sliced (floor)
  floor: boolean;
  beds: number | null;
}

/** An order as the price sees it: its coasters and plates. `scaled` says how it was made when it is
 *  not the plan itself. */
export interface Basis {
  order: string;
  coasters: number;
  plates: BasisPlate[];
  scaled: string | null;
}

/** The plan as the price reads it. A coaster is a frame, so the coasters are the frames planned. */
export function basisOf(plan: Plan): Basis {
  const coasters = plan.plates.reduce((a, p) => a + p.items.filter((it) => it.piece === null).reduce((b, it) => b + it.count, 0), 0);
  if (coasters === 0) throw new Error(`${plan.order}: the plan has no frame, so no coaster to price`);
  return {
    order: plan.order,
    coasters,
    plates: plan.plates.map((p) => ({
      plate: p.name,
      line: p.color.line,
      code: p.color.code,
      name: p.color.name,
      note: p.color.note,
      grams: p.grams,
      minutes: p.minutes ?? p.sliced_minutes,
      floor: p.floor,
      beds: p.beds,
    })),
    scaled: null,
  };
}

/** The same order at another size, worked out from the plan rather than planned: grams and minutes in
 *  proportion, and each plate's beds counted at this plan's fill, one more set of beds for every
 *  plan's worth of coasters past it. A bed that packs fuller than the plan's would cost less. The
 *  planner cannot plan most of these sizes yet: it does not split a color over plates. */
export function scaleBasis(b: Basis, coasters: number): Basis {
  if (coasters === b.coasters) return b;
  const f = coasters / b.coasters;
  const times = (x: number | null) => (x === null ? null : x * f);
  return {
    order: b.order,
    coasters,
    plates: b.plates.map((p) => ({ ...p, grams: times(p.grams), minutes: times(p.minutes), beds: p.beds === null ? null : p.beds * Math.ceil(f) })),
    scaled: `scaled from ${b.order}'s ${b.coasters} coaster(s): grams and minutes in proportion, beds at its fill`,
  };
}

// ── the price (§9.3) ────────────────────────────────────────────────────────────────────────────────

export interface MaterialLine {
  plate: string;
  line: string;
  code: string | null;
  name: string | null;
  grams: number | null;
  price_per_gram: number | null;
  usd: Amount;
  note: string | null;
}

export interface Price {
  order: string;
  coasters: number;
  scaled: string | null;
  empty: string[]; // every empty setting the price needs, in the formula's order
  floor: boolean;
  print_minutes: Amount;
  warm_ups: Amount;
  printer_hours: Amount;
  materials: MaterialLine[];
  material: Amount;
  power: Amount;
  wear: Amount;
  made: Amount;
  labor: Amount;
  packaging: Amount;
  cost: Amount;
  break_even: Amount;
  suggested: Amount;
  each: { cost: Amount; break_even: Amount; suggested: Amount };
  spools: { count: number | null; usd: Amount; note: string };
}

function gramsOf(p: BasisPlate): Amount {
  return p.grams === null ? { value: null, floor: false, missing: [`the slice of ${p.plate}`] } : known(p.grams);
}

/** The setting is by line, so it is named by line: five Matte colors need one Matte price, not five.
 *  The material line beside it names the color. */
function perGramOf(s: Settings, p: BasisPlate): Amount {
  return setting(`price per gram of ${p.line}`, (s.price_per_gram ?? {})[p.line]);
}

/** §9.3 at full precision; `priceOf` rounds it for showing. `extra` is a cost the order carries on
 *  top of the formula's (a custom theme's design time). */
function work(b: Basis, s: Settings, extra: Amount = known(0)) {
  const printMinutes = b.plates.reduce<Amount>(
    (acc, p) => combine((a, m) => a + m, acc, p.minutes === null ? { value: null, floor: false, missing: [`the slice of ${p.plate}`] } : known(p.minutes, p.floor)),
    known(0),
  );
  const bedsMissing = b.plates.filter((p) => p.beds === null).map((p) => `the slice of ${p.plate}`);
  const warmUps: Amount = bedsMissing.length ? { value: null, floor: false, missing: bedsMissing } : known(b.plates.reduce((a, p) => a + p.beds!, 0));
  const hours = combine((m, w, wm) => m / 60 + (w * wm) / 60, printMinutes, warmUps, setting(NAME.warm_up_minutes!, s.warm_up_minutes));

  const materials = b.plates.map((p) => ({ p, usd: combine((g, c) => g * c, gramsOf(p), perGramOf(s, p)) }));
  const material = materials.reduce<Amount>((acc, m) => combine((a, x) => a + x, acc, m.usd), known(0));
  const power = combine((h, w, r) => ((h * w) / 1000) * r, hours, setting(NAME.printer_watts!, s.printer_watts), setting(NAME.electricity_rate!, s.electricity_rate));
  const wear = combine((h, price, payback) => (h * price) / payback, hours, setting(NAME.printer_price!, s.printer_price), setting(NAME.payback_hours!, s.payback_hours));
  const made = combine((m, p, w, share) => (m + p + w) / share, material, power, wear, setting(NAME.good_plate_share!, s.good_plate_share));
  const labor = combine((min, rate) => ((min * b.coasters) / 60) * rate, setting(NAME.hands_on_minutes!, s.hands_on_minutes), setting(NAME.labor_rate!, s.labor_rate));
  const packaging = setting(NAME.packaging!, s.packaging);
  const cost = combine((m, l, p, x) => m + l + p + x, made, labor, packaging, extra);
  const breakEven = combine((c, fixed, pct) => (c + fixed) / (1 - pct), cost, setting(NAME.fixed_fee!, s.fixed_fee), setting(NAME.fee_percent!, s.fee_percent));
  const suggested = combine((be, mk) => be * (1 + mk), breakEven, setting(NAME.markup!, s.markup));
  return { printMinutes, warmUps, hours, materials, material, power, wear, made, labor, packaging, cost, breakEven, suggested };
}

/** §9.3, worked on one basis and rounded to the cent (hours to four places, minutes to one). */
export function priceOf(b: Basis, s: Settings): Price {
  const w = work(b, s);
  const each = (a: Amount) => round(combine((x) => x / b.coasters, a));

  // Charged against spent (§9.3): the order is charged its grams; the spools are cash out, and the
  // rest of each stays on the shelf. Counted as if none were on hand; the shelf's buy list says what is.
  const byColor = new Map<string, BasisPlate[]>();
  for (const p of b.plates) byColor.set(p.code ?? p.line, [...(byColor.get(p.code ?? p.line) ?? []), p]);
  const colors = [...byColor.values()].map((ps) => ({ p: ps[0]!, grams: ps.reduce<Amount>((acc, p) => combine((a, g) => a + g, acc, gramsOf(p)), known(0)) }));
  const spoolGrams = colors.map((c) => combine((g) => Math.ceil(g / 1000) * 1000, c.grams));
  const count = spoolGrams.some((g) => g.value === null) ? null : spoolGrams.reduce((a, g) => a + g.value! / 1000, 0);
  const spoolUsd = colors.reduce<Amount>((acc, c, i) => combine((a, g, ppg) => a + g * ppg, acc, spoolGrams[i]!, perGramOf(s, c.p)), known(0));

  return {
    order: b.order,
    coasters: b.coasters,
    scaled: b.scaled,
    empty: [...new Set([w.hours, w.material, w.power, w.wear, w.made, w.labor, w.packaging, w.cost, w.breakEven, w.suggested].flatMap((a) => a.missing))],
    floor: w.printMinutes.floor,
    print_minutes: round(w.printMinutes, 1),
    warm_ups: w.warmUps,
    printer_hours: round(w.hours, 4),
    materials: w.materials.map(({ p, usd }) => ({
      plate: p.plate,
      line: p.line,
      code: p.code,
      name: p.name,
      grams: p.grams === null ? null : Math.round(p.grams * 100) / 100,
      price_per_gram: perGramOf(s, p).value,
      usd: round(usd),
      note: p.note,
    })),
    material: round(w.material),
    power: round(w.power),
    wear: round(w.wear),
    made: round(w.made),
    labor: round(w.labor),
    packaging: round(w.packaging),
    cost: round(w.cost),
    break_even: round(w.breakEven),
    suggested: round(w.suggested),
    each: { cost: each(w.cost), break_even: each(w.breakEven), suggested: each(w.suggested) },
    spools: { count, usd: round(spoolUsd), note: "one 1 kg spool per color per started kilogram, as if none were on hand; the rest of each stays on the shelf" },
  };
}

/** The price at each size asked for: the plan's own size from the plan, the others scaled. */
export function byQuantity(b: Basis, s: Settings, sizes: number[]): Price[] {
  return sizes.map((n) => priceOf(scaleBasis(b, n), s));
}

// ── the scenarios (§9.7) ────────────────────────────────────────────────────────────────────────────

export interface ScenarioRow {
  strategy: string;
  how: string;
  coasters: number;
  scaled: string | null;
  price_each: number | null;
  cost_each: number | null;
  margin_each: number | null;
  to_cover: number | "never" | null; // coasters a month that pay the fixed costs at this margin
  below_break_even: boolean | null;
  floor: boolean;
  missing: string[];
}

/** margin each = price each × (1 − fee percent) − fixed fee ÷ coasters − cost each;
 *  to cover = monthly fixed costs ÷ margin each, rounded up, or "never" at a margin of zero or less. */
function row(strategy: string, how: string, b: Basis, s: Settings, cost: Amount, priceEach: Amount, monthly: Amount): ScenarioRow {
  const costEach = combine((c) => c / b.coasters, cost);
  const margin = combine(
    (p, pct, fixed, c) => p * (1 - pct) - fixed / b.coasters - c,
    priceEach,
    setting(NAME.fee_percent!, s.fee_percent),
    setting(NAME.fixed_fee!, s.fixed_fee),
    costEach,
  );
  const m = round(margin).value;
  const cover = combine((f) => f, monthly, margin);
  return {
    strategy,
    how,
    coasters: b.coasters,
    scaled: b.scaled,
    price_each: round(priceEach).value,
    cost_each: round(costEach).value,
    margin_each: m,
    to_cover: cover.value === null ? null : m! <= 0 ? "never" : Math.ceil(monthly.value! / margin.value!),
    below_break_even: m === null ? null : m <= 0,
    floor: priceEach.floor || margin.floor,
    missing: [...new Set([...priceEach.missing, ...margin.missing, ...monthly.missing])],
  };
}

/** One row per way of setting the price, each on §9.3's cost, never a cost of its own. A set row
 *  works out its own size, so its warm-ups and packaging spread over its own coasters. */
export function scenarios(b: Basis, s: Settings): ScenarioRow[] {
  const sc = s.scenarios ?? {};
  const monthly = setting(NAME.monthly_fixed_costs!, sc.monthly_fixed_costs);
  const own = work(b, s);
  const perCoaster = (a: Amount, n = b.coasters) => combine((x) => x / n, a);
  const rows: ScenarioRow[] = [];

  rows.push(row("cost-plus", "break-even × (1 + markup), §9.3", b, s, own.cost, perCoaster(own.suggested), monthly));
  rows.push(row("market range", "a pick inside what similar coasters are listed at", b, s, own.cost, setting(NAME.market_each!, sc.market_each), monthly));
  rows.push(row("story, premium", "a pick above the market band, for the geometry and the loose-piece build", b, s, own.cost, setting(NAME.story_each!, sc.story_each), monthly));

  // A coaster with any piece in a dearer finish sells at that finish's price.
  const finish = sc.finish_each ?? {};
  const lines = [...new Set(b.plates.map((p) => p.line))];
  const finishPrice = lines.reduce<Amount>((acc, l) => combine((a, x) => Math.max(a, x), acc, setting(`finish price each for ${l}`, finish[l])), known(0));
  rows.push(row("by finish", `one price per line, the dearest of this order's: ${lines.join(", ")}`, b, s, own.cost, finishPrice, monthly));

  for (const [n, key] of [[4, "set_of_4"], [6, "set_of_6"]] as const) {
    const sb = scaleBasis(b, n);
    rows.push(row(`set of ${n}`, `${n} coasters sold as one, at their own cost`, sb, s, work(sb, s).cost, perCoaster(setting(NAME[key]!, sc[key]), n), monthly));
  }

  const design = combine((min, rate) => (min / 60) * rate, setting(NAME.custom_design_minutes!, sc.custom_design_minutes), setting(NAME.labor_rate!, s.labor_rate));
  const custom = work(b, s, design);
  rows.push(row("custom theme", "cost-plus with the design time added to the cost", b, s, custom.cost, perCoaster(custom.suggested), monthly));

  const launch = combine((x, d) => x * (1 - d), perCoaster(own.suggested), setting(NAME.launch_discount!, sc.launch_discount));
  rows.push(row("launch price", "the cost-plus price less a launch discount", b, s, own.cost, launch, monthly));
  return rows;
}

