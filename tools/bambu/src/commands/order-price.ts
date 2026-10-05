// `bambu order price <plan.json>` — what an order costs to make and what to ask for it
// (order-driven-lab-design §9.3 and §9.7, orders phase 3). The sums are in ../price.ts; this file
// reads the settings, the store prices and the market band, and prints.
//
// The settings are Omar's and private (§9.4): labor rate, markup and his own costs never enter this
// public repo. They live in a gitignored file, `.bambu/pricing/settings.yaml` by default, which
// `--init-settings` writes with every setting empty.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { parse as parseYaml } from "yaml";
import type { Prices } from "../by-color-costs.js";
import type { Plan } from "../order.js";
import { repoRoot } from "../paths.js";
import {
  type Amount,
  type Basis,
  type Price,
  type ScenarioRow,
  type Settings,
  basisOf,
  byQuantity,
  checkSettings,
  priceOf,
  resolveStorePrices,
  scenarios,
} from "../price.js";

export const DEFAULT_SETTINGS = ".bambu/pricing/settings.yaml";
const PRICES = "docs/design/coaster/themes/catalog/prices.yaml";
const MARKET_BAND = "docs/design/coaster/themes/catalog/market-band.yaml";
/** Omar on call 13: "how much it costs us to do 1 peice, 5 pieces, 10, 100, etc". The plan's own
 *  size is added to these. */
export const DEFAULT_QUANTITIES = [1, 5, 10, 100];

/** Every setting empty, each with where its value comes from (design §9.3's table). */
export const SETTINGS_TEMPLATE = `# Pricing settings for \`bambu order price\` (order-driven-lab-design §9.3). PRIVATE: this file is
# gitignored and must never be committed; labor rate, markup and your own costs stay off the public repo.
# Every setting starts empty. A price shows only when every setting it needs is filled; an empty one is
# named, never read as zero. What the research found for each:
# docs/research/2026-10-04-coaster-pricing.md (references to confirm or replace, not settled values).

# US dollars a gram, by filament line, e.g. { "PLA Matte": 0.016 }. Or \`store refill\` (or spool,
# ten_refill, ten_spool) for the store's price from prices.yaml, for every line or for one line.
# Looked up; your real receipts replace it.
price_per_gram:
printer_watts:        # looked up; a plug meter on one plate settles it
electricity_rate:     # US dollars a kWh, from your own bill
printer_price:        # US dollars; what you actually paid
payback_hours:        # yours to choose: the printer hours the printer price is spread over
warm_up_minutes:      # per bed, measured by a timed print; 0 if the slice already includes it
good_plate_share:     # 0.8 when four plates in five come out good; measured from the print logs
hands_on_minutes:     # per coaster: clearing the plate, pressing pieces in, packing; measured
labor_rate:           # US dollars an hour, yours to choose
packaging:            # US dollars an order: box, insert, label
fee_percent:          # a share of the price, 0.11 for 11%; looked up for the channel
fixed_fee:            # US dollars an order the channel takes
markup:               # added on top of break-even: 1 doubles it; yours to choose

# The scenarios (§9.7): ways of setting the price, each worked on the cost above.
scenarios:
  monthly_fixed_costs:    # US dollars a month the shop pays whatever it sells
  market_each:            # a pick inside the market band, per coaster
  story_each:             # a pick above it, per coaster
  finish_each:            # a price per coaster by filament line, e.g. { "PLA Silk+": 9 }
  set_of_4:               # the price of a set of 4
  set_of_6:               # the price of a set of 6
  custom_design_minutes:  # the design time a custom theme takes, per order
  launch_discount:        # a share off the cost-plus price, 0.2 for 20% off
`;

interface BandRow {
  what: string;
  median?: number;
  low?: number;
  high?: number;
  listings: number;
  hedge: string;
}

export interface MarketBand {
  read: string;
  source: string;
  each: BandRow[];
}

export interface PriceReport {
  order: string;
  settings: string; // the file read, or why none was
  notes: string[];
  price: Price;
  by_quantity: Price[];
  scenarios: ScenarioRow[];
  market_band: MarketBand;
}

function root(): string {
  const r = repoRoot();
  if (!r) throw new Error("could not find the repo root (.claude/gates); run from inside the 3d-models repo");
  return r;
}

function readYaml<T>(path: string): T {
  return parseYaml(readFileSync(path, "utf8")) as T;
}

/** The settings a basis is priced on: the file checked, and `store <tier>` turned into the store's
 *  prices for the lines the order uses. */
export function settingsFor(file: string | null, b: Basis): { settings: Settings; notes: string[] } {
  const raw = file ? checkSettings(readYaml(file)) : {};
  const prices = readYaml<Prices>(join(root(), PRICES));
  return resolveStorePrices(raw, prices, [...new Set(b.plates.map((p) => p.line))]);
}

export function marketBand(): MarketBand {
  return readYaml<MarketBand>(join(root(), MARKET_BAND));
}

/** The plan's own size and the sizes asked for, smallest first. */
export function sizesFor(b: Basis, asked: number[]): number[] {
  return [...new Set([...asked, b.coasters])].sort((x, y) => x - y);
}

export function priceReport(plan: Plan, file: string | null, settingsNote: string, quantities: number[]): PriceReport {
  const b = basisOf(plan);
  const { settings, notes } = settingsFor(file, b);
  return {
    order: plan.order,
    settings: settingsNote,
    notes,
    price: priceOf(b, settings),
    by_quantity: byQuantity(b, settings, sizesFor(b, quantities)),
    scenarios: scenarios(b, settings),
    market_band: marketBand(),
  };
}

export interface PriceOpts {
  settings?: string;
  quantities?: string;
  json?: boolean;
  initSettings?: boolean;
}

export function runPrice(planFile: string, opts: PriceOpts): void {
  const file = resolve(opts.settings ?? join(root(), DEFAULT_SETTINGS));
  if (opts.initSettings) {
    if (existsSync(file)) throw new Error(`${file} already exists; it is left as it is`);
    mkdirSync(dirname(file), { recursive: true });
    writeFileSync(file, SETTINGS_TEMPLATE);
    console.error(`wrote ${file}, every setting empty`);
  }
  const quantities = opts.quantities ? opts.quantities.split(",").map((q) => parseQuantity(q)) : DEFAULT_QUANTITIES;
  const plan = JSON.parse(readFileSync(resolve(planFile), "utf8")) as Plan;
  const there = existsSync(file);
  const report = priceReport(plan, there ? file : null, there ? file : `no settings file at ${file}, so every setting is empty (--init-settings writes one)`, quantities);
  if (opts.json) console.log(JSON.stringify(report, null, 2));
  else printReport(report);
}

function parseQuantity(q: string): number {
  const n = Number(q.trim());
  if (!Number.isInteger(n) || n < 1) throw new Error(`--quantities: "${q}" is not a whole number of coasters`);
  return n;
}

// ── printing ────────────────────────────────────────────────────────────────────────────────────────

function money(v: number | null): string {
  return v === null ? "—" : `${v < 0 ? "-" : ""}$${Math.abs(v).toFixed(2)}`;
}

/** What an amount is missing, in words: two or fewer are named; past that, the ones the report's
 *  first lines already list are counted, so the full list is printed once, not on every line. */
function needs(missing: string[], listed: Set<string>): string {
  if (missing.length <= 2) return missing.join(", ");
  const own = missing.filter((m) => !listed.has(m));
  const n = missing.length - own.length;
  return [...own, ...(n ? [n === listed.size ? "the settings listed as empty" : `${n} of the settings listed as empty`] : [])].join(", ");
}

function printReport(r: PriceReport): void {
  const p = r.price;
  const listed = new Set(p.empty);
  const usd = (a: Amount): string => (a.value === null ? `— needs ${needs(a.missing, listed)}` : `${money(a.value)}${a.floor ? " (floor)" : ""}`);
  // In a table the lines above already say what an empty amount needs.
  const cell = (a: Amount): string => (a.value === null ? "—" : `${money(a.value)}${a.floor ? " (floor)" : ""}`);
  console.log(`order ${r.order}: ${p.coasters} coaster(s)`);
  console.log(`  settings: ${r.settings}`);
  for (const n of r.notes) console.log(`  · ${n}`);
  if (p.empty.length) console.log(`  empty, so no price: ${p.empty.join(", ")}`);
  if (p.floor) console.log(`  floor: no timed print corrects some plate's minutes, so the amounts are the least they can be`);

  const hours = p.printer_hours.value === null ? `— needs ${needs(p.printer_hours.missing, listed)}` : `${p.printer_hours.value} h`;
  console.log(`\n  printer hours  ${hours}  (${p.print_minutes.value ?? "?"} min printing, ${p.warm_ups.value ?? "?"} warm-up(s))`);
  for (const m of p.materials) {
    const what = [m.line, m.code, m.name].filter(Boolean).join(" ");
    console.log(`    ${m.plate}: ${m.grams ?? "?"} g of ${what}${m.price_per_gram === null ? "" : ` at $${m.price_per_gram} a gram`}, ${usd(m.usd)}`);
    if (m.note) console.log(`      note: ${m.note}`);
  }
  for (const [label, a] of [
    ["material", p.material],
    ["power", p.power],
    ["wear", p.wear],
    ["made", p.made],
    ["labor", p.labor],
    ["packaging", p.packaging],
    ["cost", p.cost],
    ["break-even", p.break_even],
    ["suggested", p.suggested],
  ] as const) {
    console.log(`  ${label.padEnd(14)} ${usd(a)}`);
  }
  console.log(`  each           cost ${cell(p.each.cost)}, break-even ${cell(p.each.break_even)}, suggested ${cell(p.each.suggested)}`);
  console.log(`  spools         ${p.spools.count ?? "?"} to buy; cash out ${usd(p.spools.usd)} (${p.spools.note})`);

  console.log(`\n  by quantity (cost, break-even, suggested, each)`);
  for (const q of r.by_quantity) {
    console.log(`    ${String(q.coasters).padStart(4)}  ${cell(q.each.cost).padEnd(16)} ${cell(q.each.break_even).padEnd(16)} ${cell(q.each.suggested).padEnd(16)}${q.scaled ? "scaled" : "the plan"}`);
  }
  const scaled = r.by_quantity.find((q) => q.scaled);
  if (scaled) console.log(`    scaled: ${scaled.scaled}`);

  console.log(`\n  scenarios (price, cost, margin each; coasters a month to cover the fixed costs)`);
  for (const s of r.scenarios) {
    const cover = s.to_cover === null ? "—" : String(s.to_cover);
    const tag = s.below_break_even ? "  below break-even" : "";
    console.log(`    ${s.strategy.padEnd(16)} ${String(s.coasters).padStart(3)}  ${money(s.price_each).padEnd(9)} ${money(s.cost_each).padEnd(9)} ${money(s.margin_each).padEnd(9)} ${cover.padStart(6)}${tag}${s.floor ? "  floor" : ""}`);
    if (s.missing.length) console.log(`      needs ${needs(s.missing, listed)}`);
  }

  const band = r.market_band;
  console.log(`\n  market band: asking prices, not sales, read ${band.read} (${band.source})`);
  for (const row of band.each) {
    const v = row.median !== undefined ? `$${row.median.toFixed(2)} median each` : `$${row.low!.toFixed(2)} to $${row.high!.toFixed(2)} each`;
    console.log(`    ${row.what}: ${v}, ${row.listings} listings; ${row.hedge}`);
  }
}
