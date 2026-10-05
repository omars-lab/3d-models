// The send's row in the plate's print log (order-driven design §9.2): which tray fed each filament,
// its color, and the slice's grams for it. The shelf (`bambu shelf show`) takes those grams off the
// spool when the next finished, failed or stopped row closes the print, so this row is the only
// place a print says which spool it used.
//
// It is built from what the send already decided, not read again: the `ams_mapping` the send
// published (matched by color, or passed by hand), the trays on the status read the send made, and
// the grams the slice wrote for each filament. The tray's own color goes in the row, not the slice's,
// because the spool on the shelf is the one in the tray (with `--color`, the slice's color was never
// the one printed). The tray's name is the one `bambu filament-sync` prints ("AMS 0 · slot 3"), so a
// spool's `tray:` on the shelf is written the way the CLI shows it.
//
// A feed that cannot be named in full refuses the whole row: a row naming two of three trays would
// take too little off the shelf and say nothing. With no row, the print shows on the shelf as not
// counted, and the operator writes the row by hand (`print_monitor.py <plate> --sent …`).

import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { colorHex, type Slot } from "./frame.js";

export interface Feed {
  hex: string; // the tray's color, "#00AE42"
  tray: string; // the tray's name, "AMS 0 · slot 3"
  grams: number; // the slice's grams for this filament
}

/** The slice's grams for each filament of one bed, by 1-based filament id, from slice_info.config
 *  (`<filament id="1" … used_g="27.15" …/>`). PURE. Empty when the bed is absent. */
export function parseFilamentGrams(xml: string, plate = 1): Map<number, number> {
  for (const block of xml.match(/<plate>[\s\S]*?<\/plate>/g) ?? []) {
    const index = block.match(/<metadata\s+key="index"\s+value="(\d+)"/);
    if (!index || Number(index[1]) !== plate) continue;
    const out = new Map<number, number>();
    for (const m of block.matchAll(/<filament\b[^>]*>/g)) {
      const id = /\bid="(\d+)"/.exec(m[0]);
      const g = /\bused_g="(\d+(?:\.\d+)?)"/.exec(m[0]);
      if (id && g) out.set(Number(id[1]), (out.get(Number(id[1])) ?? 0) + Number(g[1]));
    }
    return out;
  }
  return new Map();
}

export type Feeds = { ok: true; feeds: Feed[] } | { ok: false; reason: string };

/**
 * One feed per filament the send mapped to a tray: position i of `mapping` is filament i+1, -1 is
 * unused. PURE. Refuses, saying why, when a mapped tray is not on the status read, has no color, or
 * the slice has no grams for the filament (a slice older than sheets-04 wrote used_g="0.00").
 */
export function sentFeeds(mapping: number[], slots: Slot[], grams: Map<number, number>): Feeds {
  const feeds: Feed[] = [];
  const problems: string[] = [];
  mapping.forEach((trayNo, i) => {
    if (trayNo < 0) return;
    const id = i + 1;
    const slot = slots.find((s) => s.index === trayNo);
    const hex = slot ? colorHex(slot.tray.tray_color) : null;
    const g = grams.get(id);
    if (!slot) problems.push(`filament ${id} went to tray ${trayNo}, which the status read does not list`);
    else if (!hex) problems.push(`filament ${id} went to ${slot.where}, which reports no color`);
    else if (g === undefined || g <= 0) problems.push(`the slice has no grams for filament ${id} (slice it again)`);
    else feeds.push({ hex, tray: slot.where, grams: g });
  });
  if (problems.length > 0) return { ok: false, reason: problems.join("; ") };
  if (feeds.length === 0) return { ok: false, reason: "the send mapped no filament to a tray" };
  return { ok: true, feeds };
}

/** The monitor-print skill's `print_monitor.py --sent` arguments for these feeds. PURE. */
export function sentArgs(plate: string, feeds: Feed[]): string[] {
  return [plate, ...feeds.flatMap((f) => ["--sent", f.hex, f.tray, String(f.grams)])];
}

/** Runs `print_monitor.py` with these arguments and returns its stdout; throws on a refusal. */
export type MonitorTool = (args: string[]) => string;

const MONITOR = fileURLToPath(
  new URL("../../../.claude/skills/monitor-print/scripts/print_monitor.py", import.meta.url),
);

export const printMonitorTool: MonitorTool = (args) =>
  execFileSync("python3", [MONITOR, ...args], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });

/** Writes the send's row into the plate's print log and returns the row; throws saying why not. */
export function writeSentRow(plate: string, feeds: Feed[], tool: MonitorTool = printMonitorTool): string {
  let out: string;
  try {
    out = tool(sentArgs(plate, feeds));
  } catch (err) {
    const e = err as { stderr?: string; message?: string };
    throw new Error(String(e.stderr || e.message || err).trim().split("\n").pop() ?? "print_monitor.py refused");
  }
  const row = out.split("\n").find((l) => l.startsWith("ev=row "));
  return row ? row.slice("ev=row ".length) : out.trim();
}
