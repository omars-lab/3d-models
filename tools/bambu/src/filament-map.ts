// filament-map — which loaded tray each color of a design prints from, planned before any send
// (docs/design/coaster/print-time-color-map-design.md §3, §4; build step 2).
//
// `bambu plates by-color --json` writes one recipe per design color. This module takes those rows
// and the printer's loaded trays and runs the send's own matcher, `reconcile`, with every design
// color as one slot of a single plate. So each tray is used at most once across all the colors, and
// the plan here uses the same rule and the same two numbers (MATCH_TOLERANCE, AMBIGUITY_MARGIN) as
// the send's check. There is no second matcher: two would be two code paths that could disagree.
//
// PURE: no printer, no files. The command (commands/filament.ts, `filament map`) reads the trays
// (from the printer, or with --trays from a saved `bambu filament --json`) and the by-color file and
// hands them here, so every row is testable without a printer.

import type { PrinterStatus } from "./backends/mqtt.js";
import { collectSlots } from "./frame.js";
import {
  MATCH_TOLERANCE,
  colorDistance,
  physicalTraysFromSlots,
  reconcile,
  rgb,
  type LogicalSlot,
  type MatchStatus,
  type PhysicalTray,
} from "./filament-sync.js";

/** One design color: one row of `bambu plates by-color --json`. */
export interface DesignColor {
  name: string; // the recipe's name, e.g. "gbv-by-color-c8a24a"
  path: string | null; // the recipe file, when the row gives it
  hex: string; // "#RRGGBB", the color the design asks for
  groups: string[]; // the piece groups this color prints ("frame" for the coaster frame)
}

/** A loaded tray as a row names it. */
export interface TrayRef {
  where: string; // "AMS 0 · slot 1" / "External spool (vir_slot) 254"
  index: number | null; // the number `print send --ams-mapping` takes; null when unknown
  hex: string | null; // "#RRGGBB" the tray reports
  type: string | null; // "PLA"
  remain: number | null; // percent left, -1 for a spool with no tag, null when not reported
  tagged: boolean | null; // false when remain is -1 (no tag, so the color was set by hand); null when unknown
}

/** One design color's place: a tray, or why not, and the nearest tray when there is no match. */
export interface MapRow {
  name: string;
  path: string | null;
  design_hex: string;
  groups: string[];
  status: MatchStatus;
  tray: TrayRef | null; // the tray reconcile gave this color, null when missing
  distance: number | null; // RGB distance to that tray, null when missing
  runner_up: (TrayRef & { distance: number }) | null; // the other close tray, when ambiguous
  nearest: (TrayRef & { distance: number; taken_by: string | null }) | null; // when missing: the closest loaded tray, and which design color has it, if any
}

export interface ColorMap {
  rows: MapRow[];
  trays: TrayRef[]; // every loaded tray the map was made against
  ok: boolean; // every color matched (or matched with a low spool)
  needs_operator: boolean; // some color is missing, ambiguous or a material mismatch
}

function asHex(raw: unknown): string | null {
  if (typeof raw !== "string") return null;
  const t = rgb(raw);
  return t ? `#${t.map((n) => n.toString(16).padStart(2, "0")).join("")}`.toUpperCase() : null;
}

/**
 * Read the rows `bambu plates by-color --json` prints: an array of `{ name, path, color, items }`.
 * Throws, naming the row, when the shape is not that: a map made from a half-read file would plan
 * the wrong plates.
 */
export function designColorsFromByColor(json: unknown): DesignColor[] {
  if (!Array.isArray(json)) throw new Error("expected the JSON array `bambu plates by-color --json` prints");
  if (json.length === 0) throw new Error("the by-color file lists no plates");
  return json.map((row, i) => {
    const where = `row ${i + 1}`;
    if (typeof row !== "object" || row === null) throw new Error(`${where}: not an object`);
    const r = row as Record<string, unknown>;
    if (typeof r.name !== "string" || !r.name) throw new Error(`${where}: no "name"`);
    const hex = asHex(r.color);
    if (!hex) throw new Error(`${where} (${r.name}): "color" is not a #RRGGBB hex: ${JSON.stringify(r.color)}`);
    const items = Array.isArray(r.items) ? r.items : [];
    const groups = items.map((it) => {
      const piece = typeof it === "object" && it !== null ? (it as Record<string, unknown>).piece : undefined;
      return typeof piece === "string" ? piece : "frame";
    });
    return { name: r.name, path: typeof r.path === "string" ? r.path : null, hex, groups: [...new Set(groups)] };
  });
}

/**
 * The loaded trays from a saved copy of what `bambu filament --json` prints (`{ams, vt_tray,
 * vir_slot}`), read by the same frame parser as a live read. This is `filament map --trays`: a map
 * made without the printer, for the send-plate skill's self-test and for planning against trays saved
 * earlier. Throws when the object carries none of the three keys, since a map against "no trays" read
 * from the wrong file would ask to load every color.
 */
export function traysFromFilamentJson(json: unknown): PhysicalTray[] {
  if (typeof json !== "object" || json === null || Array.isArray(json)) {
    throw new Error("expected the JSON object `bambu filament --json` prints ({ams, vt_tray, vir_slot})");
  }
  const r = json as Record<string, unknown>;
  if (r.ams === undefined && r.vt_tray === undefined && r.vir_slot === undefined) {
    throw new Error("no ams, vt_tray or vir_slot key: not what `bambu filament --json` prints");
  }
  return physicalTraysFromSlots(collectSlots(r as PrinterStatus));
}

function trayRef(t: PhysicalTray): TrayRef {
  const remain = t.remain ?? null;
  return {
    where: t.where,
    index: t.index ?? null,
    hex: t.hex,
    type: t.type,
    remain,
    tagged: remain === null ? null : remain >= 0,
  };
}

/**
 * Map every design color to a loaded tray in one `reconcile` call, so a tray goes to at most one
 * color. A design color carries no material (the by-color rows give only a hex), so the material
 * check is left to the send, which reads it from the slice: the slot's type is blank here.
 */
export function mapColors(colors: DesignColor[], trays: PhysicalTray[]): ColorMap {
  const logical: LogicalSlot[] = colors.map((c, i) => ({ slot: i + 1, hex: c.hex, type: "" }));
  const report = reconcile(logical, trays);
  const holder = new Map<PhysicalTray, string>();
  report.bindings.forEach((b, i) => {
    if (b.tray) holder.set(b.tray, colors[i]!.name);
  });

  const rows = report.bindings.map((b, i): MapRow => {
    const c = colors[i]!;
    let nearest: MapRow["nearest"] = null;
    if (!b.tray) {
      let best: PhysicalTray | null = null;
      let bestDist = Infinity;
      for (const t of trays) {
        const d = colorDistance(c.hex, t.hex);
        if (d < bestDist) {
          bestDist = d;
          best = t;
        }
      }
      if (best) nearest = { ...trayRef(best), distance: bestDist, taken_by: holder.get(best) ?? null };
    }
    const runner = b.runnerUp as PhysicalTray | null;
    return {
      name: c.name,
      path: c.path,
      design_hex: c.hex,
      groups: c.groups,
      status: b.status,
      tray: b.tray ? trayRef(b.tray) : null,
      distance: b.distance,
      runner_up: runner ? { ...trayRef(runner), distance: colorDistance(c.hex, runner.hex) } : null,
      nearest,
    };
  });
  return { rows, trays: trays.map(trayRef), ok: report.ok, needs_operator: report.needsOperator };
}

const d = (n: number) => `Δ${n.toFixed(0)}`;
const tag = (t: TrayRef) => (t.tagged === false ? ", no tag" : "");
const trayText = (t: TrayRef) => `${t.where} (${[t.type, t.hex ?? "no color"].filter(Boolean).join(" ")}${tag(t)})`;

/** One line per design color, for a person at the terminal; `--json` is the skill's shape. */
export function renderColorMap(m: ColorMap): string {
  const lines = m.rows.map((r) => {
    const head = `${r.design_hex} ${r.name}${r.groups.length ? ` [${r.groups.join(", ")}]` : ""}`;
    switch (r.status) {
      case "matched":
        return `[ok  ] ${head} → ${trayText(r.tray!)}, ${d(r.distance!)}`;
      case "low-remain":
        return `[warn] ${head} → ${trayText(r.tray!)}, ${d(r.distance!)}, only ${r.tray!.remain}% left`;
      case "material-mismatch":
        return `[ASK ] ${head} → ${trayText(r.tray!)}, ${d(r.distance!)}, but the material differs`;
      case "ambiguous":
        return `[ASK ] ${head} → ${trayText(r.tray!)}, ${d(r.distance!)}, or ${trayText(r.runner_up!)}, ${d(r.runner_up!.distance)}: too close to call`;
      case "missing": {
        const n = r.nearest;
        const near = n
          ? `; nearest ${trayText(n)}, ${d(n.distance)}${n.taken_by ? `, already given to ${n.taken_by}` : ""}`
          : "; no tray is loaded";
        return `[LOAD] ${head} → no free tray within Δ${MATCH_TOLERANCE}${near}`;
      }
    }
  });
  const verdict = m.ok
    ? "Every color has a tray."
    : m.needs_operator
      ? "Some colors need a question before their plates are sent (LOAD / ASK above)."
      : "Every color has a tray, with warnings (warn above).";
  return `${lines.join("\n")}\n\n${verdict} A plan only: the send reads the trays again.`;
}
