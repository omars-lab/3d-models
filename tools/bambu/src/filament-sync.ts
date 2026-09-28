// filament-sync — reconcile a sliced plate's LOGICAL AMS slots against the printer's PHYSICAL trays
// by color match, so the operator knows which spool to load where before a coaster plate prints.
//
// The gap this closes is the §6 caveat of docs/design/coaster/coaster-color-design.md and the K1/logical≠physical
// note in tools/bambu/src/ams.ts: a sliced 3MF carries only a LOGICAL filament order (slot 1, 2, …
// each a palette color), never a binding to a physical AMS tray. BambuStudio resolves that binding
// interactively at print time by color. This module does the same match head-of-time and prints it,
// so `bambu filament sync --plate <3mf>` answers "load AMS slot N with which spool?" from live trays.
//
// PURE — no IO, no printer, no filesystem. The command layer (commands/filament.ts) reads the plate
// (threemf.ts) and the live trays (frame.ts collectSlots) and hands them here. That keeps the match
// unit-testable: the whole of the operator-facing decision is `reconcile()`, exercised in
// filament-sync.test.ts against hand-built color cases, including the deliberately hard ones
// (a near-tie, a material mismatch, a missing color).

import { colorHex, type Slot } from "./frame.js";

/** One logical filament slot as the slice declared it: 1-based, a color, and a material type. */
export interface LogicalSlot {
  slot: number; // 1-based, = position in the 3MF's filament_colour[] + 1
  hex: string; // "#RRGGBB" — the color the slice wants in this slot
  type: string; // "PLA", "PETG", … ; "" when the config left it blank
}

/** One physical tray the printer reports loaded, normalised out of a frame Slot. */
export interface PhysicalTray {
  where: string; // "AMS 0 · slot 1" / "External spool" — the label to tell the operator
  hex: string | null; // "#RRGGBB" or null when the tray is empty / has no RFID color
  type: string | null; // "PLA" or null when empty
  remain: number | null; // percent left; null when the tray does not report it, -1 = unknown (no RFID)
  index?: number | null; // the tray number a send puts in ams_mapping (frame.ts trayIndex); null = unknown
}

export type MatchStatus =
  | "matched" // a tray within the color tolerance, material agrees — load it, no question
  | "material-mismatch" // color is close enough but the material differs — operator must confirm
  | "low-remain" // matched, but the tray reports little filament left — warn, do not block
  | "ambiguous" // two loaded trays are ~equally close — the operator's call which to use
  | "missing"; // no loaded tray is within tolerance of this color — load a spool

export interface SlotBinding {
  logical: LogicalSlot;
  tray: PhysicalTray | null; // the chosen physical tray, or null when missing
  runnerUp: PhysicalTray | null; // the second-closest, when it made the match ambiguous
  status: MatchStatus;
  distance: number | null; // color distance to the chosen tray (0 = exact), null when missing
}

export interface SyncReport {
  bindings: SlotBinding[];
  ok: boolean; // every logical slot resolved to a clean "matched" — safe to print unattended
  needsOperator: boolean; // any slot needs a human: missing / ambiguous / material-mismatch
}

// --- tunables. These decide auto-match vs. ask; the report ALWAYS prints the measured distance, so a
// generous tolerance never hides a mistake — the operator sees the number and the colors either way
// (docs/design/printing/print-model-design.md §5.5: "one clear match is chosen and stated, not asked"). ---

/** Max color distance (0–441.7, the RGB-cube diagonal) still called a match. 60 ≈ a shade's worth of
 *  drift — comfortably separates distinct palette colors while tolerating RFID/screen variance. */
export const MATCH_TOLERANCE = 60;
/** When the runner-up tray is within this of the best, the choice is a near-tie → ask the operator. */
export const AMBIGUITY_MARGIN = 15;
/** `remain` at or below this (and not the -1 "unknown" sentinel) warns of a spool that may run out. */
export const LOW_REMAIN_PCT = 10;

/** Parse "#RGB" / "#RRGGBB" / "#RRGGBBAA" / "RRGGBBAA" to [r,g,b], or null when unparseable. */
export function rgb(hex: string | null | undefined): [number, number, number] | null {
  if (!hex) return null;
  let h = hex.trim().replace(/^#/, "");
  if (/^[0-9a-fA-F]{3}$/.test(h)) h = h.split("").map((c) => c + c).join(""); // #abc → #aabbcc
  if (h.length >= 6) h = h.slice(0, 6);
  if (!/^[0-9a-fA-F]{6}$/.test(h)) return null;
  return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
}

/** Euclidean distance in the RGB cube (0 = identical, ~441.7 = black↔white). Symmetric, deterministic.
 *  A weighted/CIELAB metric would track perception better but adds a table for a match the operator
 *  eyeballs anyway; plain RGB is enough to separate palette colors and keeps the function trivially
 *  testable. Returns Infinity when either color is unparseable so such a pair never wins a match. */
export function colorDistance(a: string | null | undefined, b: string | null | undefined): number {
  const x = rgb(a);
  const y = rgb(b);
  if (!x || !y) return Infinity;
  return Math.hypot(x[0] - y[0], x[1] - y[1], x[2] - y[2]);
}

/** Normalise the frame's loaded slots into the tray shape the matcher consumes. Empty trays (no
 *  tray_type) are dropped — they cannot satisfy any slot and only add noise to the report. */
export function physicalTraysFromSlots(slots: Slot[]): PhysicalTray[] {
  const out: PhysicalTray[] = [];
  for (const s of slots) {
    const type = (s.tray.tray_type ?? "").trim();
    if (!type) continue; // empty tray
    out.push({
      where: s.where,
      hex: colorHex(s.tray.tray_color),
      type,
      remain: s.tray.remain ?? null,
      index: s.index ?? null,
    });
  }
  return out;
}

/** Turn a sliced plate's filament_colour[]/filament_type[] into 1-based logical slots. Color is the
 *  spine — a slot with no color cannot be matched, so it is skipped (it is a config the slice never
 *  filled, not a real print slot). Types shorter than colors pad with "" (blank, not a guess). */
export function logicalSlotsFromPlate(colors: string[], types: string[]): LogicalSlot[] {
  const out: LogicalSlot[] = [];
  colors.forEach((raw, i) => {
    const hex = rgb(raw) ? `#${rgb(raw)!.map((n) => n.toString(16).padStart(2, "0")).join("")}`.toUpperCase() : null;
    if (!hex) return;
    out.push({ slot: i + 1, hex, type: (types[i] ?? "").trim() });
  });
  return out;
}

interface ReconcileOpts {
  tolerance?: number;
  ambiguityMargin?: number;
  lowRemainPct?: number;
}

/**
 * Match every logical slot to a physical tray by color, each tray used at most once.
 *
 * Greedy on the global best pair: of all (unbound slot, unused tray) pairs, bind the closest first,
 * then the next, and so on. Greedy-by-least-distance is optimal-enough here (≤ a handful of slots)
 * and, unlike per-slot independent picks, never hands the same tray to two slots. Ties break by slot
 * then tray index, so the result is deterministic. After binding, each slot is classified:
 *   - distance > tolerance (or no tray left)      → missing
 *   - a still-unused tray within ambiguityMargin  → ambiguous (near-tie the operator resolves)
 *   - bound tray's material ≠ the slot's material → material-mismatch
 *   - bound tray remain in (−1, lowRemainPct]     → low-remain (a warning, still bound)
 *   - otherwise                                    → matched
 */
export function reconcile(
  logical: LogicalSlot[],
  physical: PhysicalTray[],
  opts: ReconcileOpts = {},
): SyncReport {
  const tolerance = opts.tolerance ?? MATCH_TOLERANCE;
  const margin = opts.ambiguityMargin ?? AMBIGUITY_MARGIN;
  const lowRemain = opts.lowRemainPct ?? LOW_REMAIN_PCT;

  const usedTray = new Set<number>();
  const chosen = new Map<number, { trayIdx: number; distance: number }>(); // slotIdx → binding

  // Global-greedy assignment: repeatedly take the closest unbound (slot, tray) pair.
  const pairs: Array<{ si: number; ti: number; d: number }> = [];
  logical.forEach((l, si) =>
    physical.forEach((t, ti) => pairs.push({ si, ti, d: colorDistance(l.hex, t.hex) })),
  );
  pairs.sort((a, b) => a.d - b.d || a.si - b.si || a.ti - b.ti);
  for (const { si, ti, d } of pairs) {
    if (d === Infinity) break; // nothing parseable left to bind
    if (chosen.has(si) || usedTray.has(ti)) continue;
    if (d > tolerance) continue; // too far to be this slot's color
    chosen.set(si, { trayIdx: ti, distance: d });
    usedTray.add(ti);
  }

  const bindings: SlotBinding[] = logical.map((l, si) => {
    const c = chosen.get(si);
    if (!c) {
      return { logical: l, tray: null, runnerUp: null, status: "missing", distance: null };
    }
    const tray = physical[c.trayIdx];
    if (!tray) return { logical: l, tray: null, runnerUp: null, status: "missing", distance: null };
    // Runner-up: the closest tray NOT bound to this slot (may be bound elsewhere — it still shows the
    // operator the choice was tight). A near-tie is the operator's call, per §5.5.
    let runnerUp: PhysicalTray | null = null;
    let runnerDist = Infinity;
    physical.forEach((t, ti) => {
      if (ti === c.trayIdx) return;
      const d = colorDistance(l.hex, t.hex);
      if (d < runnerDist) {
        runnerDist = d;
        runnerUp = t;
      }
    });
    const tight = runnerDist <= tolerance && runnerDist - c.distance <= margin;

    let status: MatchStatus;
    if (tight) status = "ambiguous";
    else if (l.type && tray.type && l.type.toUpperCase() !== tray.type.toUpperCase()) status = "material-mismatch";
    else if (tray.remain !== null && tray.remain >= 0 && tray.remain <= lowRemain) status = "low-remain";
    else status = "matched";

    return { logical: l, tray, runnerUp: tight ? runnerUp : null, status, distance: c.distance };
  });

  const needsOperator = bindings.some(
    (b) => b.status === "missing" || b.status === "ambiguous" || b.status === "material-mismatch",
  );
  const ok = bindings.length > 0 && bindings.every((b) => b.status === "matched" || b.status === "low-remain");
  return { bindings, ok, needsOperator };
}

const MARK: Record<MatchStatus, string> = {
  matched: "ok  ",
  "low-remain": "warn",
  "material-mismatch": "ASK ",
  ambiguous: "ASK ",
  missing: "LOAD",
};

/** One line per logical slot: what to load where, with the measured color distance always shown. */
export function renderReport(r: SyncReport): string {
  if (r.bindings.length === 0) {
    return "The plate declares no colored filament slots (nothing to reconcile).";
  }
  const lines = r.bindings.map((b) => {
    const l = b.logical;
    const head = `slot ${l.slot} ${l.hex}${l.type ? ` ${l.type}` : ""}`;
    const mark = MARK[b.status];
    switch (b.status) {
      case "matched":
        return `[${mark}] ${head} → ${b.tray!.where} (${b.tray!.type} ${b.tray!.hex ?? "?"}, Δ${b.distance!.toFixed(0)})`;
      case "low-remain":
        return `[${mark}] ${head} → ${b.tray!.where} (${b.tray!.type} ${b.tray!.hex ?? "?"}, Δ${b.distance!.toFixed(0)}) — LOW: ${b.tray!.remain}% left`;
      case "material-mismatch":
        return `[${mark}] ${head} → ${b.tray!.where} color matches (Δ${b.distance!.toFixed(0)}) but is ${b.tray!.type}, not ${l.type} — confirm the swap`;
      case "ambiguous":
        return `[${mark}] ${head} → ${b.tray!.where} (Δ${b.distance!.toFixed(0)}) or ${b.runnerUp!.where} (${b.runnerUp!.type} ${b.runnerUp!.hex ?? "?"}) — near-tie, pick one`;
      case "missing":
        return `[${mark}] ${head} → no loaded tray within Δ${MATCH_TOLERANCE} — load this color`;
    }
  });
  const verdict = r.ok
    ? "All slots matched — safe to print."
    : r.needsOperator
      ? "Operator action needed before printing (see ASK/LOAD above)."
      : "Matched with warnings (see warn above).";
  return `${lines.join("\n")}\n\n${verdict}`;
}

/** True when any filament feeds from an AMS tray (0–253); 254/255 are the external spool, -1 unused. */
export function feedsFromAms(mapping: number[]): boolean {
  return mapping.some((i) => i >= 0 && i < 254);
}

/** What a send puts in `use_ams` / `ams_mapping`, or why it will not choose for the operator. */
export type AmsPlan =
  | { ok: true; amsMapping: number[]; useAms: boolean }
  | { ok: false; reason: string };

/**
 * Turn a reconciliation into a send's `ams_mapping`: one entry per filament the project declares
 * (position i = filament i+1), the bound tray's number for each filament the plate uses, -1 for the
 * rest. `use_ams` follows from it. Refuses — never guesses — when a used filament has no clean match
 * (missing, a near-tie, a material mismatch) or its tray has no known number: which spool feeds the
 * print is the operator's call, made with `--ams-mapping`, not a default. The old default fed the
 * empty external spool on every send (found by the minis-01 run, 2026-09-25).
 */
export function planAmsMapping(report: SyncReport, filamentCount: number, used: number[]): AmsPlan {
  if (used.length === 0) return { ok: false, reason: "the plate lists no used filament (is it sliced?)" };
  const bySlot = new Map(report.bindings.map((b) => [b.logical.slot, b]));
  const mapping: number[] = Array.from({ length: Math.max(filamentCount, ...used) }, () => -1);
  const problems: string[] = [];
  for (const id of used) {
    const b = bySlot.get(id);
    if (!b) problems.push(`filament ${id} has no color in the plate to match a tray by`);
    else if (b.status !== "matched" && b.status !== "low-remain") problems.push(`filament ${id} is ${b.status}`);
    else if (b.tray?.index === null || b.tray?.index === undefined)
      problems.push(`filament ${id} matched ${b.tray?.where}, which has no known tray number`);
    else mapping[id - 1] = b.tray.index;
  }
  if (problems.length > 0) return { ok: false, reason: problems.join("; ") };
  return { ok: true, amsMapping: mapping, useAms: feedsFromAms(mapping) };
}
