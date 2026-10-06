// An order, turned into plates: the pieces counted, sorted by color, one recipe per color, each with
// its beds, minutes and grams, and the minutes corrected by how long past prints really took.
//
// The design is order-driven-lab-design §9.1 (the steps) and §9.5 (the check). An order file is plain
// YAML that names no person; the hub writes it into its private store, never into this repo. Lines
// have a count, a frame (the coaster, one per count) and optionally the loose pieces that drop into
// it, each group in a catalog color:
//
//   id: "FIXTURE"
//   lines:
//     - count: 4
//       frame:  { construction: bikar:…-minimal-coaster.bkr, params: {…}, color: { line: PLA Matte, code: "11100" } }
//       pieces: { construction: bikar:…-minimal-pieces.bkr, params: {…}, colors: { Kite: { line: PLA Matte, code: "11603" }, … } }
//
// Nothing here reads a file or runs a program; commands/order.ts passes in the catalog, the groups
// `bikar bands` reports, the frozen or fresh slices and the timed runs.

import { parse as parseYaml } from "yaml";
import {
  type ColorPlate,
  type Demand,
  type PieceGroup,
  type PlateColor,
  type WrittenRecipe,
  PLATE_SETTINGS,
  filamentPreset,
  groupByColor,
  normalHex,
  slug,
  writeRecipes,
} from "./by-color.js";
import { canonicalJson } from "./iteration.js";
import { type NearestRatio, type Ratio, type TimedRun, nearestUnused, ratioFor } from "./timed-prints.js";

export interface ColorPick {
  line: string;
  code: string;
}

export interface OrderLine {
  count: number;
  frame: { construction: string; params: Record<string, number>; color: ColorPick };
  pieces: { construction: string; params: Record<string, number>; colors: Record<string, ColorPick> } | null;
}

export interface Order {
  id: string;
  lines: OrderLine[];
}

function isObj(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

function construction(v: unknown, where: string): string {
  if (typeof v !== "string" || !v.startsWith("bikar:") || !v.endsWith(".bkr")) {
    throw new Error(`${where}.construction: must be "bikar:<path>.bkr", got ${JSON.stringify(v)}`);
  }
  return v;
}

function params(v: unknown, where: string): Record<string, number> {
  if (v === undefined) return {};
  if (!isObj(v)) throw new Error(`${where}.params: must be a mapping of name → number`);
  for (const [k, n] of Object.entries(v)) {
    if (typeof n !== "number" || !Number.isFinite(n)) throw new Error(`${where}.params.${k}: must be a number, got ${JSON.stringify(n)}`);
  }
  return v as Record<string, number>;
}

function pick(v: unknown, where: string): ColorPick {
  if (!isObj(v) || typeof v.line !== "string" || (typeof v.code !== "string" && typeof v.code !== "number")) {
    throw new Error(`${where}: must be { line: <filament line>, code: "<color code>" }, got ${JSON.stringify(v)}`);
  }
  return { line: v.line, code: String(v.code) };
}

/** Parse and check an order file. Throws naming the field that is wrong. */
export function parseOrder(text: string): Order {
  const doc = parseYaml(text) as unknown;
  if (!isObj(doc)) throw new Error("the order file is empty or not a mapping");
  if (typeof doc.id !== "string" && typeof doc.id !== "number") throw new Error("the order has no `id:`");
  if (!Array.isArray(doc.lines) || doc.lines.length === 0) throw new Error("the order has no `lines:`");
  const lines = doc.lines.map((raw, i): OrderLine => {
    const where = `lines[${i}]`;
    if (!isObj(raw)) throw new Error(`${where}: not a mapping`);
    if (typeof raw.count !== "number" || !Number.isInteger(raw.count) || raw.count < 1) {
      throw new Error(`${where}.count: must be a whole number of coasters, 1 or more`);
    }
    if (!isObj(raw.frame)) throw new Error(`${where}.frame: every line has a frame, the coaster itself`);
    const frame = {
      construction: construction(raw.frame.construction, `${where}.frame`),
      params: params(raw.frame.params, `${where}.frame`),
      color: pick(raw.frame.color, `${where}.frame.color`),
    };
    let pieces: OrderLine["pieces"] = null;
    if (raw.pieces !== undefined) {
      const p = raw.pieces;
      if (!isObj(p) || !isObj(p.colors) || Object.keys(p.colors).length === 0) {
        throw new Error(`${where}.pieces: needs \`colors:\`, a color for each group of pieces`);
      }
      const colors: Record<string, ColorPick> = {};
      for (const [name, c] of Object.entries(p.colors)) colors[name] = pick(c, `${where}.pieces.colors.${name}`);
      pieces = { construction: construction(p.construction, `${where}.pieces`), params: params(p.params, `${where}.pieces`), colors };
    }
    return { count: raw.count, frame, pieces };
  });
  return { id: String(doc.id), lines };
}

/** One color from the catalog (catalog.yaml's `colors:` entries). */
export interface CatalogColor {
  code: string;
  line: string;
  name: string;
  hexes: string[];
  /** single, gradient (the color shifts along the spool) or multi (the colors side by side in the
   *  strand), as catalog.yaml files it. */
  kind?: string;
}

/** What a spool of more than one color does to a print, by the catalog's kind for it. */
const SHIFT: Record<string, string> = {
  gradient: "the color shifts along the spool, so where it shifts cannot be predicted for a given piece",
  multi: "the colors run side by side in the strand, so a piece can show either, or both",
};

/** Look a pick up in the catalog, with the palette's store note when it has one. A two-color spool
 *  takes its first hex, the one the AMS reports as the tray's color (the Neon City tray reads
 *  `tray_color: 0047BBFF`, `cols: [0047BBFF, BB22A3FF]`, 2026-10-05), so the send finds its tray. */
export function lookupColor(catalog: CatalogColor[], notes: Map<string, string>, c: ColorPick): PlateColor {
  const hit = catalog.find((e) => e.line === c.line && e.code === c.code);
  if (!hit) throw new Error(`${c.line} ${c.code}: not in the color catalog (docs/design/coaster/themes/catalog/catalog.yaml)`);
  const hexes = hit.hexes.map((h) => normalHex(h));
  if (hexes.length === 0 || hexes.some((h) => !h)) throw new Error(`${c.line} ${c.code} (${hit.name}): no hex in the catalog, so no plate color`);
  const many =
    hexes.length > 1
      ? `a ${hexes.length}-color spool (${hexes.join(", ")}): the plate's color is the first, which the AMS reports for the tray; ${SHIFT[hit.kind ?? ""] ?? "how its colors fall on a given piece cannot be predicted"}`
      : null;
  const note = [notes.get(`${c.line}|${c.code}`), many].filter(Boolean).join("; ") || null;
  return { key: `${c.line}|${c.code}`, hex: hexes[0]!, line: c.line, code: c.code, name: hit.name, note };
}

/** A pick by code alone (codes are unique across the catalog's lines), as `plates by-color` takes it. */
export function lookupCode(catalog: CatalogColor[], notes: Map<string, string>, code: string): PlateColor {
  const hits = catalog.filter((e) => e.code === code);
  if (hits.length === 0) throw new Error(`${code}: no spool with this code in the color catalog (docs/design/coaster/themes/catalog/catalog.yaml)`);
  if (hits.length > 1) throw new Error(`${code}: ${hits.map((h) => h.line).join(" and ")} both use this code; name the line too`);
  return lookupColor(catalog, notes, { line: hits[0]!.line, code });
}

/** The groups of a pieces construction at its params: `bikar bands` on the .bkr. */
export type GroupsOf = (construction: string, params: Record<string, number>) => PieceGroup[];

/** Every line's frame and pieces as demands, in order-file order. Throws when a line's colors and its
 *  construction's groups differ: a group with no color would print in nothing, a color with no group
 *  is a typo. */
export function orderDemands(order: Order, color: (c: ColorPick) => PlateColor, groupsOf: GroupsOf): Demand[] {
  const out: Demand[] = [];
  order.lines.forEach((l, i) => {
    out.push({ construction: l.frame.construction, params: l.frame.params, piece: null, count: l.count, rank: -1, color: color(l.frame.color) });
    if (!l.pieces) return;
    const groups = groupsOf(l.pieces.construction, l.pieces.params);
    const names = groups.map((g) => g.piece);
    const missing = names.filter((n) => !(n in l.pieces!.colors));
    const extra = Object.keys(l.pieces.colors).filter((n) => !names.includes(n));
    if (missing.length || extra.length) {
      throw new Error(
        `lines[${i}].pieces.colors: ` +
          [missing.length ? `no color for ${missing.join(", ")}` : "", extra.length ? `no group named ${extra.join(", ")}` : ""]
            .filter(Boolean)
            .join("; ") +
          ` (its groups: ${names.join(", ")})`,
      );
    }
    for (const g of groups) {
      out.push({
        construction: l.pieces.construction,
        params: l.pieces.params,
        piece: g.piece,
        count: l.count,
        rank: Math.min(...g.orbits),
        color: color(l.pieces.colors[g.piece]!),
      });
    }
  });
  return out;
}

/** A slice's numbers, frozen or fresh, keyed in slices.json by the recipe hash. */
export interface SliceFacts {
  recipe: string; // the recipe's name, for a person reading the file
  beds: number;
  minutes: number;
  grams: number;
  /** Written since piece colors phase 2; older slices.json files lack them. */
  layers?: number | null; // on the tallest bed, from the slice's layer ranges
  bed_minutes?: number[]; // one per bed, so a spill shows its second bed apart
}

export interface PlanPlate {
  name: string;
  color: { line: string; code: string | null; hex: string; name: string | null; note: string | null };
  settings: string;
  filament: string;
  recipe_hash: string;
  items: Array<{ construction: string; params: Record<string, number>; piece: string | null; count: number }>;
  source: "frozen" | "none";
  beds: number | null;
  sliced_minutes: number | null;
  grams: number | null;
  ratio: { value: number; prints: number } | null;
  minutes: number | null; // corrected; null when there is no ratio (floor) or no slice
  floor: boolean;
  nearest_unused: { filament: string; value: number; prints: number; why: string } | null;
  sendable: boolean;
  why_not: string | null;
}

export interface Plan {
  order: string;
  plates: PlanPlate[];
  total: {
    plates: number;
    beds: number | null;
    warm_ups: number | null;
    sliced_minutes: number | null;
    minutes: number | null;
    floor: boolean;
    grams: number | null;
  };
  notes: string[];
}

export interface PlanInputs {
  slices: Record<string, SliceFacts>; // by recipe hash
  runs: TimedRun[];
}

/** The plan for written recipes: each plate's numbers from its slice (by recipe hash), its ratio. */
export function planOf(orderId: string, written: WrittenRecipe[], inputs: PlanInputs): Plan {
  const plates = written.map((w) => planPlate(w, inputs));
  const sum = (f: (p: PlanPlate) => number | null) =>
    plates.some((p) => f(p) === null) ? null : Math.round(plates.reduce((a, p) => a + f(p)!, 0) * 100) / 100;
  const beds = sum((p) => p.beds);
  const notes: string[] = [];
  if (plates.some((p) => p.source === "none")) notes.push("not sliced: a plate has no slice, so its beds, minutes and grams are unknown");
  if (beds !== null) notes.push(`${beds} warm-ups, not timed: whether a slice's minutes include its warm-up is not known`);
  if (plates.some((p) => p.floor)) notes.push("floor: a plate printed with a profile no timed print used shows its sliced minutes only");
  return {
    order: orderId,
    plates,
    total: {
      plates: plates.length,
      beds,
      warm_ups: beds,
      sliced_minutes: sum((p) => p.sliced_minutes),
      minutes: plates.some((p) => p.floor) ? null : sum((p) => p.minutes),
      floor: plates.some((p) => p.floor),
      grams: sum((p) => p.grams),
    },
    notes,
  };
}

function planPlate(w: WrittenRecipe, inputs: PlanInputs): PlanPlate {
  const c = w.plate.color;
  const filament = filamentPreset(c.line);
  const s = inputs.slices[w.hash] ?? null;
  const ratio: Ratio | null = ratioFor(inputs.runs, PLATE_SETTINGS, filament);
  const near: NearestRatio | null = ratio ? null : nearestUnused(inputs.runs, PLATE_SETTINGS, filament);
  const spilled = s !== null && s.beds > 1;
  return {
    name: w.name,
    color: { line: c.line, code: c.code, hex: c.hex, name: c.name, note: c.note },
    settings: PLATE_SETTINGS,
    filament,
    recipe_hash: w.hash,
    items: w.plate.items.map((it) => ({ construction: it.construction, params: it.params, piece: it.piece, count: it.count })),
    source: s ? "frozen" : "none",
    beds: s ? s.beds : null,
    sliced_minutes: s ? s.minutes : null,
    grams: s ? s.grams : null,
    ratio: ratio ? { value: ratio.value, prints: ratio.prints.length } : null,
    minutes: s && ratio ? Math.round((s.minutes * ratio.watched) / ratio.sliced) : null,
    floor: s !== null && ratio === null,
    nearest_unused: near ? { filament: near.filament, value: near.value, prints: near.prints.length, why: near.why } : null,
    sendable: s !== null && !spilled,
    why_not: !s ? "not sliced" : spilled ? `spills onto ${s.beds} beds: a send prints bed 1 only, so split it before sending` : null,
  };
}

/** Write the order's recipes: one per color, named `<order id>-<color code>`. */
export function orderRecipes(order: Order, demands: Demand[], groupsOf: GroupsOf): WrittenRecipe[] {
  const plates: ColorPlate[] = groupByColor(demands);
  const members = (construction: string, params: Record<string, number>, piece: string) =>
    groupsOf(construction, params).find((g) => g.piece === piece)?.members ?? null;
  return writeRecipes(
    plates,
    slug(order.id),
    [
      `Written by \`bambu order plan\` for order ${order.id}: every frame and piece of the order in this color,`,
      "one plate per color (piece colors call 1). Do not edit by hand: change the order and plan again.",
    ],
    (it) => (it.piece ? members(it.construction, it.params, it.piece) : 1),
  );
}

/** Plan an order end to end, from its parsed file. */
export function planOrder(
  order: Order,
  deps: { color: (c: ColorPick) => PlateColor; groupsOf: GroupsOf } & PlanInputs,
): { plan: Plan; recipes: WrittenRecipe[] } {
  const demands = orderDemands(order, deps.color, deps.groupsOf);
  const recipes = orderRecipes(order, demands, deps.groupsOf);
  return { plan: planOf(order.id, recipes, deps), recipes };
}

// ── the check (§9.5) ────────────────────────────────────────────────────────────────────────────────

function pieceKey(construction: string, params: Record<string, number>, piece: string | null): string {
  return `${construction} ${canonicalJson(params)} ${piece ?? "frame"}`;
}

/** Each piece an order or a plan holds, by construction, params and group, as the list of colors its
 *  pieces get (one entry per piece). Two plans with the same totals but one kite on the wrong plate
 *  differ here. */
function piecesByColor(
  entries: Array<{ construction: string; params: Record<string, number>; piece: string | null; count: number; color: string }>,
  groupsOf: GroupsOf,
): Map<string, string[]> {
  const out = new Map<string, string[]>();
  for (const e of entries) {
    const members = e.piece === null ? 1 : (groupsOf(e.construction, e.params).find((g) => g.piece === e.piece)?.members ?? 0);
    const key = pieceKey(e.construction, e.params, e.piece);
    const list = out.get(key) ?? [];
    for (let i = 0; i < e.count * members; i++) list.push(e.color);
    out.set(key, list);
  }
  for (const l of out.values()) l.sort();
  return out;
}

function tally(list: string[]): string {
  const n = new Map<string, number>();
  for (const c of list) n.set(c, (n.get(c) ?? 0) + 1);
  return [...n.entries()].map(([c, k]) => `${k} ${c}`).join(", ") || "none";
}

/** What is wrong with a plan for an order, plate by plate; empty when nothing is. The totals are not
 *  trusted to vouch for a plate: every piece, every plate's numbers and every ratio is checked. */
export function checkPlan(
  order: Order,
  plan: Plan,
  deps: { color: (c: ColorPick) => PlateColor; groupsOf: GroupsOf } & PlanInputs,
): string[] {
  const errors: string[] = [];
  const colorKey = (line: string, code: string | null, hex: string) => (code ? `${line}|${code}` : hex);

  // Every piece on a plate of its own color.
  const want = piecesByColor(
    orderDemands(order, deps.color, deps.groupsOf).map((d) => ({ ...d, color: d.color.key })),
    deps.groupsOf,
  );
  const got = piecesByColor(
    plan.plates.flatMap((p) => p.items.map((it) => ({ ...it, color: colorKey(p.color.line, p.color.code, p.color.hex) }))),
    deps.groupsOf,
  );
  for (const key of new Set([...want.keys(), ...got.keys()])) {
    const w = want.get(key) ?? [];
    const g = got.get(key) ?? [];
    if (JSON.stringify(w) !== JSON.stringify(g)) errors.push(`pieces ${key}: the order wants ${tally(w)}, the plan prints ${tally(g)}`);
  }

  // One plate per color, each with its own color's filament.
  const seen = new Map<string, string>();
  for (const p of plan.plates) {
    const key = colorKey(p.color.line, p.color.code, p.color.hex);
    if (seen.has(key)) errors.push(`${p.name}: a second plate in ${key} (also ${seen.get(key)}); one color is one plate`);
    seen.set(key, p.name);
    if (p.filament !== filamentPreset(p.color.line)) errors.push(`${p.name}: filament ${p.filament} is not ${p.color.line}'s preset`);
    if (p.settings !== PLATE_SETTINGS) errors.push(`${p.name}: settings ${p.settings} are not the plate settings`);
  }

  // Each plate's numbers are its slice's, and its ratio is the one the timed prints give.
  for (const p of plan.plates) {
    const s = deps.slices[p.recipe_hash];
    if (!s) {
      if (p.source !== "none" || p.beds !== null || p.sliced_minutes !== null || p.grams !== null) {
        errors.push(`${p.name}: numbers with no slice of recipe ${p.recipe_hash}; re-freeze the slices`);
      }
    } else {
      if (p.beds !== s.beds) errors.push(`${p.name}: ${p.beds} beds, its slice has ${s.beds}`);
      if (p.sliced_minutes !== s.minutes) errors.push(`${p.name}: ${p.sliced_minutes} sliced minutes, its slice has ${s.minutes}`);
      if (p.grams !== s.grams) errors.push(`${p.name}: ${p.grams} g, its slice has ${s.grams} g`);
      if (p.sendable !== (s.beds === 1)) errors.push(`${p.name}: sendable ${p.sendable} on ${s.beds} beds`);
    }
    const r = ratioFor(deps.runs, p.settings, p.filament);
    if (r === null && p.ratio !== null) errors.push(`${p.name}: a ratio, but no timed print used ${p.filament}`);
    if (r !== null && (p.ratio?.value !== r.value || p.ratio?.prints !== r.prints.length)) {
      errors.push(`${p.name}: ratio ${JSON.stringify(p.ratio)}, the timed prints give ${r.value} over ${r.prints.length}`);
    }
    if (s && p.floor !== (r === null)) errors.push(`${p.name}: floor ${p.floor}, but ${r ? "a ratio applies" : "no ratio applies"}`);
    if (p.floor && p.minutes !== null) errors.push(`${p.name}: corrected minutes on a floor plate`);
  }

  // The recipes the plan names are the ones its items make, and the order total is its plates' sum.
  const demands = orderDemands(order, deps.color, deps.groupsOf);
  const recipes = orderRecipes(order, demands, deps.groupsOf);
  const hashes = new Map(recipes.map((r) => [r.name, r.hash]));
  for (const p of plan.plates) {
    if (hashes.has(p.name) && hashes.get(p.name) !== p.recipe_hash) {
      errors.push(`${p.name}: recipe ${p.recipe_hash}, but its order writes ${hashes.get(p.name)}`);
    }
  }
  const sum = (f: (p: PlanPlate) => number | null) =>
    plan.plates.some((p) => f(p) === null) ? null : Math.round(plan.plates.reduce((a, p) => a + f(p)!, 0) * 100) / 100;
  const t = plan.total;
  if (t.plates !== plan.plates.length) errors.push(`total: ${t.plates} plates, the plan lists ${plan.plates.length}`);
  for (const [field, value] of [
    ["beds", sum((p) => p.beds)],
    ["warm_ups", sum((p) => p.beds)],
    ["sliced_minutes", sum((p) => p.sliced_minutes)],
    ["grams", sum((p) => p.grams)],
  ] as const) {
    if (t[field] !== value) errors.push(`total: ${field} ${t[field]}, its plates add to ${value}`);
  }
  return errors;
}
