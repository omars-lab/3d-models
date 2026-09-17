// `bambu filament` — read-only view of the filament the printer has loaded (AMS + external spool).
//   list (default) : the loaded trays, one line each — material, colour, brand, remaining
//
// This is the discovery seam the print-model skill (docs/print-model-design.md §5.5) builds on: pick
// the filament before deciding nozzle/settings. It reaches the printer WITHOUT moving it — the same
// `pushing.pushall` status request `status show` uses (backends/mqtt.ts), reading `print.ams.ams[]`
// and `print.vt_tray` out of the cached report frame.
//
// DE-RISK (task #32): no surveyed tool names the X2D, and the H2-family AMS report schema had
// MQTT-validation churn (docs/research/print-model-research.md Topic 2, [X2D-UNCONFIRMED — H2-proxy]).
// So this parses the AMS block DEFENSIVELY — it never assumes a tray shape it has not seen — and, when
// the frame carries no AMS/tray data at all, says exactly that (with a --json escape hatch) rather
// than rendering a confident-but-empty table.
//
// CONFIRMED on the live X2D (20P6AJ641401412, 2026-09-17): the frame carries `print.ams.ams[]` with
// `tray[]` exactly as documented (empty trays report only `{id,state}`), and the external spool is
// `print.vir_slot` as an ARRAY (id "254" sentinel + a loaded virtual slot), NOT the H2-family
// `print.vt_tray` object (absent here). Parsing the array defensively is what surfaced the loaded
// external slot — see isRecord() below, where the array-vs-object trap actually bit.

import { Command } from "commander";
import { MqttBackend, type PrinterStatus } from "../backends/mqtt.js";
import { collectSlots, colorHex, type Slot } from "../frame.js";

function requireConfigured(b: { configured(): boolean }): void {
  if (!b.configured()) {
    console.error("Not configured. Set PRINTER_HOST / BAMBU_SERIAL / BAMBU_TOKEN (or .mcp.json).");
    console.error("Run `bambu setup doctor` to see what's missing.");
    process.exit(1);
  }
}

function renderTray(slot: Slot): string {
  const t = slot.tray;
  const type = (t.tray_type ?? "").trim();
  if (!type) return `${slot.where}: (empty)`;

  const parts: string[] = [type];
  const brand = (t.tray_sub_brands ?? "").trim();
  if (brand && brand !== type) parts.push(brand);
  const hex = colorHex(t.tray_color);
  if (hex) parts.push(hex);
  if (t.tray_info_idx) parts.push(`idx ${t.tray_info_idx}`);
  if (t.remain !== undefined) parts.push(t.remain < 0 ? "remain unknown (no RFID)" : `${t.remain}% left`);

  return `${slot.where}: ${parts.join(" · ")}`;
}

function renderFilament(s: PrinterStatus): string {
  const age = s._age_seconds;
  if (age === null || age === undefined) {
    return "No report received yet (the printer sent nothing on device/<serial>/report within the wait window).";
  }
  const slots = collectSlots(s);
  if (slots.length === 0) {
    return (
      "No AMS or external-spool data in the report frame.\n" +
      "  This X2D may not expose `ams`/`vt_tray` as the H2-family docs describe, or nothing is loaded.\n" +
      "  Re-run with --json to inspect the raw frame."
    );
  }
  const loaded = slots.filter((sl) => (sl.tray.tray_type ?? "").trim()).length;
  const body = slots.map(renderTray).join("\n");
  return `${body}\n\n(${loaded} of ${slots.length} slot(s) loaded; report age ${age}s; --json for the full frame)`;
}

export function registerFilament(program: Command): void {
  program
    .command("filament")
    .description("read-only view of loaded filament (AMS trays + external spool)")
    .option("--json", "print the raw ams/vt_tray frame instead of a summary")
    .action(async (opts: { json?: boolean }) => {
      const mqtt = new MqttBackend();
      requireConfigured(mqtt);
      try {
        await mqtt.connect();
        const s = await mqtt.requestStatus();
        if (opts.json) {
          const r = s as Record<string, unknown>;
          console.log(JSON.stringify({ ams: r.ams, vt_tray: r.vt_tray, vir_slot: r.vir_slot }, null, 2));
        } else {
          console.log(renderFilament(s));
        }
      } catch (err) {
        console.error(`filament failed: ${(err as Error).message}`);
        process.exitCode = 1;
      } finally {
        await mqtt.close();
      }
    });
}
