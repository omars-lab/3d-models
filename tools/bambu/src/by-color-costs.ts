// What each way of printing a colored coaster costs, plate by plate (piece colors phase 2,
// infill-color-ux-design §6). Omar on call 1 of the 2026-10-05 page: "Can there be printing options
// where we visulzie each of the plates and their colors and the net cost and time and average time
// per coaster?"
//
// Three ways, the design's §6 routes:
//   per-color   one plate per color, the `plates by-color` recipes, each from its own slice
//   whole-set   the whole set on one plate, printed once per color (what sheets-04g does today)
//   one-plate   the whole set on one plate in every color at once, swapping on the AMS; dropped by
//               Omar on 2026-10-04, shown so the cost of dropping it stays in view
//
// Numbers come from a slice where one exists. The swaps in the third way have no slice to come
// from (the slicer counts none), so they are an estimate from one print, phones-01, and labeled so.
// Nothing here reads a file or runs a program; the command passes in the recipes and their slices.

import { type PlateItem, type WrittenRecipe, filamentPreset } from "./by-color.js";
import { canonicalJson } from "./iteration.js";
import type { SliceFacts } from "./order.js";

/** One color swap on the X2D, from phones-01 (2026-10-04, pink and black, one swap on each of its 22
 *  layers): it took about 62 minutes against the slicer's 22, which the phones-02 page puts at about
 *  1.6 minutes a swap (1.8 if all 40 extra minutes were swaps). About 1.5 g went to the swaps and the prime tower, by difference with
 *  phones-02 (pink only, 3.46 g against 4.85 g, the small phones slightly bigger), so about 0.07 g a
 *  swap. It transfers only to the same printer, filament and purge settings, and only as an average.
 *  phones-01's two colors sat on the X2D's two nozzles, so nothing was flushed; a third color shares
 *  a nozzle and adds a flush on each change, so for three colors or more this is a low estimate. */
export const SWAP = { minutes: 1.6, grams: 0.07, from: "phones-01, 2026-10-04" } as const;

export type Tier = "refill" | "spool" | "ten_refill" | "ten_spool";
export const TIERS: Tier[] = ["refill", "spool", "ten_refill", "ten_spool"];

export interface Prices {
  read: string;
  source: string;
  lines: Record<string, Partial<Record<Tier, number>>>;
  /** Each spool's own price, by its code. The store files some spools under a line of its own:
   *  Neon City (13903) is PLA Silk in the catalog and PLA Silk Multi-Color at the store, at its price. */
  colors?: Record<string, Partial<Record<Tier, number>> & { line?: string; name?: string; out_of_stock?: Tier[] }>;
}

export interface PriceUsed {
  usd_per_kg: number;
  tier: Tier;
  note: string | null; // set when the tier asked for was not read, or the store had it out of stock
}

/** A spool's price per kg at a tier: its own, by code, when the price file has it, else its line's.
 *  A tier not read falls back to the spool price, then the refill, and says so; no price at all is
 *  null, never a guess. */
export function pricePerKg(prices: Prices, line: string, tier: Tier, code: string | null = null): PriceUsed | null {
  const own = code ? prices.colors?.[code] : undefined;
  const p = own ?? prices.lines[line];
  if (!p) return null;
  const what = own ? `${line} ${code}` : line;
  for (const t of [tier, "spool", "refill"] as Tier[]) {
    const v = p[t];
    if (v === undefined) continue;
    const notes = [];
    if (t !== tier) notes.push(`${what} has no ${tier} price read; used its ${t} price`);
    if (own?.out_of_stock?.includes(t)) notes.push(`${what} was out of stock as a ${t} when the prices were read`);
    return { usd_per_kg: v, tier: t, note: notes.length ? notes.join("; ") : null };
  }
  return null;
}

export interface RouteColor {
  hex: string;
  line: string;
  code: string | null;
  name: string | null;
}

/** What a color is priced as: its line, and its code when it has one. */
function priceKey(c: RouteColor): string {
  return c.code ? `${c.line} ${c.code}` : c.line;
}

export interface RoutePlate {
  name: string; // the recipe it prints from
  colors: RouteColor[]; // one for a one-color plate; every color for the swapping plate
  what: string[]; // "Kite ×10", "frame ×1"
  source: "slice" | "estimate" | "none";
  beds: number | null;
  bed_minutes: number[] | null; // one per bed, so a spill shows each bed
  sliced_minutes: number | null; // the slicer's, warm-up included
  swaps: number;
  swap_minutes: number;
  minutes: number | null; // sliced + swaps
  watched_minutes: number | null; // sliced × the watched/sliced ratio of past prints, + swaps; null with no ratio
  grams: number | null;
  usd: number | null;
  sendable: boolean;
  notes: string[];
}

export interface Route {
  key: "per-color" | "whole-set" | "one-plate";
  title: string;
  status: string;
  fits_rule: boolean; // Omar's 2026-10-04 rule: one color per plate
  plates: RoutePlate[];
  total: {
    sends: number | null; // one per bed
    swaps: number;
    minutes: number | null;
    watched_minutes: number | null;
    grams: number | null;
    usd: number | null;
  };
  per_coaster: { minutes: number | null; watched_minutes: number | null; grams: number | null; usd: number | null };
  left_over: string;
  notes: string[];
}

export interface Costs {
  coasters: number;
  colors: RouteColor[];
  prices: { read: string; source: string; tier: Tier; used: Record<string, PriceUsed | null> };
  swap: typeof SWAP;
  routes: Route[];
  notes: string[];
}

export interface CostInputs {
  coasters: number;
  /** The `plates by-color` recipes, one per color, each with its slice if it has one. */
  perColor: Array<{ recipe: WrittenRecipe; slice: SliceFacts | null }>;
  /** Every item of every color on one recipe, with its slice; null when it was not written. */
  wholeSet: { recipe: WrittenRecipe; slice: SliceFacts | null } | null;
  pieceCount: (it: PlateItem) => number; // pieces one item renders (1 for a frame)
  prices: Prices;
  tier: Tier;
  /** The watched/sliced ratio for a filament preset, from past prints; null when none timed it. */
  ratio: (filament: string) => { value: number; prints: number } | null;
}

const r1 = (n: number) => Math.round(n * 10) / 10;
const r2 = (n: number) => Math.round(n * 100) / 100;

function sumOrNull(xs: Array<number | null>): number | null {
  return xs.some((x) => x === null) ? null : xs.reduce((a: number, x) => a + x!, 0);
}

function itemKey(it: PlateItem): string {
  return `${it.construction} ${canonicalJson(it.params)} ${it.piece ?? "frame"}`;
}

function describe(items: PlateItem[], pieceCount: CostInputs["pieceCount"]): string[] {
  return items.map((it) => (it.piece ? `${it.piece} ×${it.count * pieceCount(it)}` : `frame ×${it.count}`));
}

function colorOf(w: WrittenRecipe): RouteColor {
  const c = w.plate.color;
  return { hex: c.hex, line: c.line, code: c.code, name: c.name };
}

/** The three routes for one coloring, plate by plate. */
export function costRoutes(inputs: CostInputs): Costs {
  const colors = inputs.perColor.map(({ recipe }) => colorOf(recipe));
  const used: Record<string, PriceUsed | null> = {};
  for (const c of colors) used[priceKey(c)] ??= pricePerKg(inputs.prices, c.line, inputs.tier, c.code);
  const usdFor = (grams: number | null, c: RouteColor) => {
    const p = used[priceKey(c)] ?? pricePerKg(inputs.prices, c.line, inputs.tier, c.code);
    return grams === null || !p ? null : r2((grams / 1000) * p.usd_per_kg);
  };
  const watched = (sliced: number | null, line: string, swapMinutes: number) => {
    const ratio = inputs.ratio(filamentPreset(line));
    return sliced === null || !ratio ? null : r1(sliced * ratio.value + swapMinutes);
  };

  const perColor = inputs.perColor.map(({ recipe, slice }) => onePlate(recipe.name, [colorOf(recipe)], describe(recipe.plate.items, inputs.pieceCount), slice, usdFor, watched));
  const routes: Route[] = [
    route(
      "per-color",
      "One plate per color",
      "fits Omar's 2026-10-04 rule: one color per plate",
      true,
      perColor,
      inputs.coasters,
      "nothing",
      ["each plate's minutes are its own slice's, warm-up included, so the total counts every warm-up"],
    ),
  ];

  const whole = inputs.wholeSet;
  if (whole) {
    // Which color each item of the whole set belongs to, from the per-color recipes.
    const colorOfItem = new Map<string, RouteColor>();
    for (const { recipe } of inputs.perColor) for (const it of recipe.plate.items) colorOfItem.set(itemKey(it), colorOf(recipe));
    const what = describe(whole.recipe.plate.items, inputs.pieceCount);

    const prints = colors.map((c) => {
      const p = onePlate(whole.recipe.name, [c], what, whole.slice, usdFor, watched);
      const spare = whole.recipe.plate.items.filter((it) => colorOfItem.get(itemKey(it))?.hex !== c.hex);
      p.notes.push(`keep the ${c.hex} ones; ${countItems(spare, inputs.pieceCount) || "nothing"} left over`);
      return p;
    });
    const spare = colors.flatMap((c) => whole.recipe.plate.items.filter((it) => colorOfItem.get(itemKey(it))?.hex !== c.hex));
    routes.push(
      route(
        "whole-set",
        "Whole set, once per color",
        "what sheets-04g does today",
        true,
        prints,
        inputs.coasters,
        countItems(spare, inputs.pieceCount) || "nothing",
        ["the same plate printed once in each color; only that color's pieces are kept from each print"],
      ),
    );

    // One plate, every color: the whole set's slice plus the swaps the slicer does not count.
    const layers = whole.slice?.layers ?? null;
    const swaps = layers === null ? null : layers * (colors.length - 1);
    const swapMinutes = swaps === null ? 0 : r1(swaps * SWAP.minutes);
    const swapGrams = swaps === null ? 0 : r2(swaps * SWAP.grams);
    const s = whole.slice;
    const sliced = s ? s.minutes : null;
    const grams = s ? r2(s.grams + swapGrams) : null;
    // Dollars by color: the whole set's grams split as the per-color slices split them.
    const split = perColor.map((p) => p.grams);
    const splitTotal = sumOrNull(split);
    let usd: number | null = null;
    if (grams !== null && splitTotal) {
      usd = sumOrNull(perColor.map((p, i) => usdFor((grams * split[i]!) / splitTotal, p.colors[0]!)));
      if (usd !== null) usd = r2(usd);
    }
    const ratio = inputs.ratio(filamentPreset(colors[0]?.line ?? "PLA Basic"));
    const notes = [
      swaps === null
        ? "no layer count in the slice, so the swaps are not estimated"
        : `about ${swaps} swaps: ${layers} layers × ${colors.length - 1}, assuming every color prints on every layer`,
      `swaps at ${SWAP.minutes} min and ${SWAP.grams} g each, from one print (${SWAP.from}); an average, not this plate's`,
    ];
    if (colors.length > 2) notes.push("low: phones-01 had one color per nozzle; a third color shares a nozzle and flushes on every change, which phones-01 never timed");
    if (splitTotal) notes.push("dollars split by color as the one-plate-per-color slices split the grams");
    const onePlateRow: RoutePlate = {
      name: whole.recipe.name,
      colors,
      what,
      source: s ? "estimate" : "none",
      beds: s ? s.beds : null,
      bed_minutes: s?.bed_minutes ?? (s ? [s.minutes] : null),
      sliced_minutes: sliced,
      swaps: swaps ?? 0,
      swap_minutes: swapMinutes,
      minutes: sliced === null ? null : r1(sliced + swapMinutes),
      watched_minutes: sliced === null || !ratio ? null : r1(sliced * ratio.value + swapMinutes),
      grams,
      usd,
      sendable: false,
      notes,
    };
    routes.push(
      route("one-plate", `One plate, ${colors.length} colors`, "dropped by Omar on 2026-10-04: slower and more waste", false, [onePlateRow], inputs.coasters, "nothing", [
        "an estimate: the slicer counts no swaps, so its minutes are the slice's plus the swaps'",
      ]),
    );
  }

  const notes: string[] = [];
  if (inputs.perColor.some((p) => !p.slice)) notes.push("not sliced: a plate with no slice shows no minutes, grams or dollars (pass --slice)");
  for (const [line, p] of Object.entries(used)) {
    if (!p) notes.push(`${line}: no price in the price file, so its plates show no dollars`);
    else if (p.note) notes.push(p.note);
  }
  return {
    coasters: inputs.coasters,
    colors,
    prices: { read: inputs.prices.read, source: inputs.prices.source, tier: inputs.tier, used },
    swap: SWAP,
    routes,
    notes,
  };
}

function countItems(items: PlateItem[], pieceCount: CostInputs["pieceCount"]): string {
  const frames = items.filter((it) => !it.piece).reduce((a, it) => a + it.count, 0);
  const pieces = items.filter((it) => it.piece).reduce((a, it) => a + it.count * pieceCount(it), 0);
  const parts = [];
  if (frames) parts.push(`${frames} frame${frames === 1 ? "" : "s"}`);
  if (pieces) parts.push(`${pieces} piece${pieces === 1 ? "" : "s"}`);
  return parts.join(" and ");
}

function onePlate(
  name: string,
  colors: RouteColor[],
  what: string[],
  s: SliceFacts | null,
  usdFor: (g: number | null, c: RouteColor) => number | null,
  watched: (sliced: number | null, line: string, swapMinutes: number) => number | null,
): RoutePlate {
  const line = colors[0]!.line;
  const spilled = s !== null && s.beds > 1;
  return {
    name,
    colors,
    what,
    source: s ? "slice" : "none",
    beds: s ? s.beds : null,
    bed_minutes: s?.bed_minutes ?? (s ? [s.minutes] : null),
    sliced_minutes: s ? s.minutes : null,
    swaps: 0,
    swap_minutes: 0,
    minutes: s ? s.minutes : null,
    watched_minutes: watched(s ? s.minutes : null, line, 0),
    grams: s ? s.grams : null,
    usd: usdFor(s ? s.grams : null, colors[0]!),
    sendable: s !== null && !spilled,
    notes: spilled ? [`spills onto ${s.beds} beds: a send prints bed 1 only, so split it before sending`] : [],
  };
}

function route(
  key: Route["key"],
  title: string,
  status: string,
  fitsRule: boolean,
  plates: RoutePlate[],
  coasters: number,
  leftOver: string,
  notes: string[],
): Route {
  const total = {
    sends: sumOrNull(plates.map((p) => p.beds)),
    swaps: plates.reduce((a, p) => a + p.swaps, 0),
    minutes: nullable(sumOrNull(plates.map((p) => p.minutes)), r1),
    watched_minutes: nullable(sumOrNull(plates.map((p) => p.watched_minutes)), r1),
    grams: nullable(sumOrNull(plates.map((p) => p.grams)), r2),
    usd: nullable(sumOrNull(plates.map((p) => p.usd)), r2),
  };
  const each = (n: number | null, round: (x: number) => number) => (n === null ? null : round(n / coasters));
  return {
    key,
    title,
    status,
    fits_rule: fitsRule,
    plates,
    total,
    per_coaster: { minutes: each(total.minutes, r1), watched_minutes: each(total.watched_minutes, r1), grams: each(total.grams, r2), usd: each(total.usd, r2) },
    left_over: leftOver,
    notes,
  };
}

function nullable(n: number | null, f: (x: number) => number): number | null {
  return n === null ? null : f(n);
}
