// The shelf (order-driven-lab-design §9.2, phase 2): what each spool still holds, what the open
// orders hold of each color, what is left, and what to buy.
//
// - **On hand** is a spool's starting grams, plus the owner's corrections, minus the grams of every
//   print that used it. A tray tag's percent left is shown beside it, never used in the sum: the
//   owner weighs the spool and writes a correction when the two disagree.
// - **Held** is the sum of the open orders' planned grams per color. A plate that printed to the end
//   stops holding; a failed one keeps holding, since it gets printed again.
// - **Available** is on hand minus held, and the **buy list** is every color below zero, rounded up
//   to whole spools, with the palette's store note when there is one.
//
// A print is closed from its plate's print log: the send's `sent` row names the trays it fed and the
// slice's grams for each, and the next `finished`, `failed` or `stopped` row closes it. A failed
// print used filament too, so it counts its full slice grams. A stopped one is counted the same way,
// which can overcount a print stopped early; the owner corrects the spool. A terminal row with no
// `sent` row before it (every log written before the send wrote one) is listed, not guessed at.
//
// Nothing here reads a file: the command (`bambu shelf`) gathers the inputs.

import { parse as parseYaml } from "yaml";
import { normalHex } from "./by-color.js";
import type { CatalogColor, Plan } from "./order.js";
import type { LogRow } from "./timed-prints.js";

export interface Correction {
  date: string;
  grams: number; // added to the spool: negative when it weighed lighter than the book
  why: string;
}

export interface Spool {
  id: string;
  line: string;
  code: string;
  start_grams: number;
  tray?: string; // where it sits now ("AMS 1 slot 4"), which breaks a tie between two spools of one hex
  tag_percent?: number;
  corrections: Correction[];
}

export interface ShelfOrder {
  plan: string; // a plan.json (`bambu order plan` writes one per order), relative to the shelf file
  status: "open" | "closed";
}

export interface Shelf {
  spool_grams: number; // a new spool's grams, for the buy list
  spool_grams_by_line: Record<string, number>;
  logs: string | null; // the print logs folder, relative to the shelf file
  spools: Spool[];
  orders: ShelfOrder[];
}

const num = (v: unknown, what: string): number => {
  if (typeof v !== "number" || !Number.isFinite(v)) throw new Error(`${what} must be a number, not ${JSON.stringify(v)}`);
  return v;
};

/** A shelf file: its spools, its orders, and where the print logs are. */
export function parseShelf(text: string): Shelf {
  const doc = (parseYaml(text) ?? {}) as Record<string, unknown>;
  const spools = (Array.isArray(doc.spools) ? doc.spools : []) as Array<Record<string, unknown>>;
  const orders = (Array.isArray(doc.orders) ? doc.orders : []) as Array<Record<string, unknown>>;
  const ids = new Set<string>();
  return {
    spool_grams: doc.spool_grams === undefined ? 1000 : num(doc.spool_grams, "spool_grams"),
    spool_grams_by_line: Object.fromEntries(
      Object.entries((doc.spool_grams_by_line ?? {}) as Record<string, unknown>).map(([l, g]) => [l, num(g, `spool_grams_by_line.${l}`)]),
    ),
    logs: typeof doc.logs === "string" ? doc.logs : null,
    spools: spools.map((s, i) => {
      const id = String(s.id ?? "");
      if (!id) throw new Error(`spool ${i + 1} has no id`);
      if (ids.has(id)) throw new Error(`two spools are called ${id}`);
      ids.add(id);
      if (!s.line || !s.code) throw new Error(`spool ${id} needs a line and a code`);
      return {
        id,
        line: String(s.line),
        code: String(s.code),
        start_grams: num(s.start_grams, `spool ${id} start_grams`),
        ...(s.tray ? { tray: String(s.tray) } : {}),
        ...(s.tag_percent !== undefined ? { tag_percent: num(s.tag_percent, `spool ${id} tag_percent`) } : {}),
        corrections: ((Array.isArray(s.corrections) ? s.corrections : []) as Array<Record<string, unknown>>).map((c) => ({
          date: String(c.date ?? ""),
          grams: num(c.grams, `spool ${id} correction grams`),
          why: String(c.why ?? ""),
        })),
      };
    }),
    orders: orders.map((o, i) => {
      if (typeof o.plan !== "string") throw new Error(`order ${i + 1} names no plan (a plan.json from \`bambu order plan\`)`);
      if (o.status !== "open" && o.status !== "closed") throw new Error(`order ${o.plan}: status is open or closed, not ${JSON.stringify(o.status)}`);
      return { plan: o.plan, status: o.status };
    }),
  };
}

export interface SentTray {
  hex: string;
  tray: string;
  grams: number;
}

/** The trays a `sent` row names: "fed #00ae42 from AMS 1 slot 4, 27.28 g by the slice; …". */
export function sentTrays(said: string): SentTray[] {
  const out: SentTray[] = [];
  for (const m of said.matchAll(/(#[0-9a-fA-F]{6}) from (.+?), (\d+(?:\.\d+)?) g/g)) {
    out.push({ hex: m[1]!.toLowerCase(), tray: m[2]!.trim(), grams: Number(m[3]) });
  }
  return out;
}

const CLOSING = new Set(["finished", "failed", "stopped"]);

export interface Close {
  plate: string;
  sent: string;
  ended: string;
  event: string;
  trays: SentTray[];
}

export interface Unclosed {
  plate: string;
  time: string;
  why: string;
}

/** Every print the logs close, and the sends and ends that do not pair up. */
export function closes(logs: Array<{ plate: string; rows: LogRow[] }>): { closed: Close[]; not_closed: Unclosed[]; uncounted: Unclosed[] } {
  const closed: Close[] = [];
  const not_closed: Unclosed[] = [];
  const uncounted: Unclosed[] = [];
  for (const { plate, rows } of logs) {
    let pending: LogRow | null = null;
    for (const r of rows) {
      if (r.event === "sent") {
        if (pending) not_closed.push({ plate, time: pending.time, why: `sent again at ${r.time} before this send closed` });
        pending = r;
      } else if (CLOSING.has(r.event)) {
        if (!pending) {
          uncounted.push({ plate, time: r.time, why: `${r.event} with no sent row before it, so no tray or grams` });
          continue;
        }
        closed.push({ plate, sent: pending.time, ended: r.time, event: r.event, trays: sentTrays(pending.said) });
        pending = null;
      }
      // `lost` leaves the send open: the print may still be going.
    }
    if (pending) not_closed.push({ plate, time: pending.time, why: "no finished, failed or stopped row yet" });
  }
  return { closed, not_closed, uncounted };
}

export interface SpoolLine {
  id: string;
  line: string;
  code: string;
  name: string;
  start_grams: number;
  corrections_grams: number;
  used_grams: number;
  on_hand: number;
  tag_percent: number | null;
}

export interface ColorLine {
  line: string;
  code: string;
  name: string;
  on_hand: number;
  held: number | null; // null: an open plate has no grams yet, so the color's hold is unknown
  available: number | null;
  held_by: Array<{ order: string; plate: string; grams: number | null }>;
  note: string | null;
}

export interface BuyLine {
  line: string;
  code: string;
  name: string;
  short_grams: number;
  spools: number;
  note: string | null;
}

export interface ShelfReport {
  spools: SpoolLine[];
  colors: ColorLine[];
  buy: BuyLine[];
  closed: Array<{ plate: string; sent: string; ended: string; event: string; spool: string; grams: number }>;
  not_closed: Unclosed[];
  unmatched: Array<{ plate: string; sent: string; hex: string; tray: string; grams: number; why: string }>;
  uncounted: Unclosed[];
}

export interface ShelfInputs {
  shelf: Shelf;
  orders: Array<{ status: "open" | "closed"; plan: Plan }>;
  logs: Array<{ plate: string; rows: LogRow[] }>;
  catalog: CatalogColor[];
  notes: Map<string, string>;
}

const r2 = (n: number) => Math.round(n * 100) / 100;
const keyOf = (line: string, code: string) => `${line}|${code}`;

/** The shelf, added up. */
export function shelfReport(inp: ShelfInputs): ShelfReport {
  const { shelf, catalog, notes } = inp;
  const colorOf = new Map(catalog.map((c) => [keyOf(c.line, c.code), c]));
  const spools = shelf.spools.map((s) => {
    const c = colorOf.get(keyOf(s.line, s.code));
    if (!c) throw new Error(`spool ${s.id}: ${s.line} ${s.code} is not in the catalog`);
    return { s, c, hexes: new Set(c.hexes.map((h) => normalHex(h)).filter((h): h is string => h !== null)), used: 0 };
  });

  // Each closed print's grams onto the spool it fed from: the spools whose color is the tray's hex;
  // two colors with that hex are told apart by the spool's `tray:`, else it is not guessed.
  const { closed, not_closed, uncounted } = closes(inp.logs);
  const report: ShelfReport = { spools: [], colors: [], buy: [], closed: [], not_closed, unmatched: [], uncounted };
  for (const c of closed) {
    if (!c.trays.length) {
      report.not_closed.push({ plate: c.plate, time: c.sent, why: "the sent row names no tray" });
      continue;
    }
    for (const t of c.trays) {
      const miss = (why: string) => report.unmatched.push({ plate: c.plate, sent: c.sent, hex: t.hex, tray: t.tray, grams: t.grams, why });
      let cands = spools.filter((sp) => sp.hexes.has(t.hex));
      if (!cands.length) {
        miss(`no spool on the shelf is ${t.hex}`);
        continue;
      }
      const colors = new Set(cands.map((sp) => keyOf(sp.s.line, sp.s.code)));
      if (colors.size > 1) {
        const inTray = cands.filter((sp) => sp.s.tray === t.tray);
        if (new Set(inTray.map((sp) => keyOf(sp.s.line, sp.s.code))).size !== 1) {
          miss(`${t.hex} is ${[...colors].map((k) => k.replace("|", " ")).join(" and ")}; set tray: "${t.tray}" on the spool it was`);
          continue;
        }
        cands = inTray;
      }
      const sp = cands.find((x) => x.s.tray === t.tray) ?? cands[0]!;
      sp.used += t.grams;
      report.closed.push({ plate: c.plate, sent: c.sent, ended: c.ended, event: c.event, spool: sp.s.id, grams: t.grams });
    }
  }

  for (const sp of spools) {
    const corr = sp.s.corrections.reduce((a, c) => a + c.grams, 0);
    report.spools.push({
      id: sp.s.id,
      line: sp.s.line,
      code: sp.s.code,
      name: sp.c.name,
      start_grams: sp.s.start_grams,
      corrections_grams: r2(corr),
      used_grams: r2(sp.used),
      on_hand: r2(sp.s.start_grams + corr - sp.used),
      tag_percent: sp.s.tag_percent ?? null,
    });
  }

  // What the open orders hold, less every plate that printed to the end.
  const printed = new Set(closed.filter((c) => c.event === "finished").map((c) => c.plate));
  const colors = new Map<string, ColorLine>();
  const colorLine = (line: string, code: string, name: string): ColorLine => {
    const k = keyOf(line, code);
    let cl = colors.get(k);
    if (!cl) {
      cl = { line, code, name, on_hand: 0, held: 0, available: null, held_by: [], note: notes.get(k) ?? null };
      colors.set(k, cl);
    }
    return cl;
  };
  for (const s of report.spools) {
    const cl = colorLine(s.line, s.code, s.name);
    cl.on_hand = r2(cl.on_hand + s.on_hand);
  }
  for (const o of inp.orders) {
    if (o.status !== "open") continue;
    for (const p of o.plan.plates) {
      if (printed.has(p.name)) continue;
      if (!p.color.line || !p.color.code) throw new Error(`order ${o.plan.order}: plate ${p.name} has no catalog line and code`);
      const cl = colorLine(p.color.line, p.color.code, p.color.name ?? p.color.code);
      cl.held_by.push({ order: o.plan.order, plate: p.name, grams: p.grams });
      cl.held = cl.held === null || p.grams === null ? null : r2(cl.held + p.grams);
    }
  }
  for (const cl of colors.values()) {
    cl.available = cl.held === null ? null : r2(cl.on_hand - cl.held);
    if (cl.available !== null && cl.available < 0) {
      const size = shelf.spool_grams_by_line[cl.line] ?? shelf.spool_grams;
      const short = -cl.available;
      report.buy.push({ line: cl.line, code: cl.code, name: cl.name, short_grams: short, spools: Math.ceil(short / size - 1e-9), note: cl.note });
    }
  }
  const byKey = (a: { line: string; code: string }, b: { line: string; code: string }) =>
    a.line.localeCompare(b.line) || a.code.localeCompare(b.code);
  report.colors = [...colors.values()].sort(byKey);
  report.buy.sort(byKey);
  return report;
}

const label = (x: { line: string; code: string }) => `${x.line} ${x.code}`;

/** Where `got` and `expected` differ, one line per spool, color or buy line, named the way a person
 *  reads the shelf ("PLA Basic 10100: on hand 972.72, expected 1000"). */
export function shelfDiff(expected: ShelfReport, got: ShelfReport): string[] {
  const out: string[] = [];
  const g = (n: number | null) => (n === null ? "unknown" : String(n));
  const exS = new Map(expected.spools.map((s) => [s.id, s]));
  for (const s of got.spools) {
    const e = exS.get(s.id);
    if (!e) out.push(`spool ${s.id}: on the shelf, not expected`);
    else if (e.on_hand !== s.on_hand || e.used_grams !== s.used_grams) {
      out.push(`spool ${s.id} (${label(s)}): on hand ${s.on_hand} (used ${s.used_grams}), expected ${e.on_hand} (used ${e.used_grams})`);
    }
    exS.delete(s.id);
  }
  for (const id of exS.keys()) out.push(`spool ${id}: expected, not on the shelf`);

  const exC = new Map(expected.colors.map((c) => [keyOf(c.line, c.code), c]));
  for (const c of got.colors) {
    const e = exC.get(keyOf(c.line, c.code));
    exC.delete(keyOf(c.line, c.code));
    if (!e) {
      out.push(`${label(c)}: on the shelf, not expected`);
      continue;
    }
    if (e.on_hand !== c.on_hand) out.push(`${label(c)}: on hand ${c.on_hand}, expected ${e.on_hand}`);
    if (e.held !== c.held) out.push(`${label(c)}: held ${g(c.held)}, expected ${g(e.held)}`);
    if (e.available !== c.available) out.push(`${label(c)}: available ${g(c.available)}, expected ${g(e.available)}`);
  }
  for (const e of exC.values()) out.push(`${label(e)}: expected, not on the shelf`);

  const exB = new Map(expected.buy.map((b) => [keyOf(b.line, b.code), b]));
  for (const b of got.buy) {
    const e = exB.get(keyOf(b.line, b.code));
    exB.delete(keyOf(b.line, b.code));
    const what = `buy ${b.spools} spool(s), ${b.short_grams} g short${b.note ? ` (${b.note})` : ""}`;
    if (!e) out.push(`${label(b)}: ${what}, expected no buy`);
    else if (e.spools !== b.spools || e.short_grams !== b.short_grams || e.note !== b.note) {
      out.push(`${label(b)}: ${what}, expected ${e.spools} spool(s), ${e.short_grams} g short${e.note ? ` (${e.note})` : ""}`);
    }
  }
  for (const e of exB.values()) out.push(`${label(e)}: expected to buy ${e.spools} spool(s), nothing is short`);

  const lists = ["closed", "not_closed", "unmatched", "uncounted"] as const;
  for (const k of lists) {
    if (JSON.stringify(expected[k]) !== JSON.stringify(got[k])) out.push(`${k}: ${JSON.stringify(got[k])}, expected ${JSON.stringify(expected[k])}`);
  }
  return out;
}
