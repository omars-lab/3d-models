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

function requireConfigured(b: { configured(): boolean }): void {
  if (!b.configured()) {
    console.error("Not configured. Set PRINTER_HOST / BAMBU_SERIAL / BAMBU_TOKEN (or .mcp.json).");
    console.error("Run `bambu setup doctor` to see what's missing.");
    process.exit(1);
  }
}

/** One filament slot as we surface it, from an AMS tray or the external spool. */
interface Tray {
  id?: string;
  tray_type?: string; // "PLA", "PETG", … ; "" when the slot is empty
  tray_color?: string; // RRGGBBAA hex
  tray_sub_brands?: string; // e.g. "PLA Basic"
  tray_info_idx?: string; // Bambu filament-profile id, e.g. "GFA00"
  remain?: number; // percent remaining; -1 = no RFID / unknown
}

interface Slot {
  where: string; // human label: "AMS 0 · slot 1" or "External spool"
  tray: Tray;
}

function isRecord(v: unknown): v is Record<string, unknown> {
  // Arrays are `typeof "object"` too — exclude them, or an array-valued key (the X2D reports
  // `vir_slot` as an array, verified 2026-09-17 on 20P6AJ641401412) is mistaken for one tray.
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

/**
 * Pull every filament slot out of a report frame, tolerant of the shapes the H2/X2D line is reported
 * to drift across. Handles `print.ams` as either `{ ams: [ {tray:[…]} ] }` (documented) or a bare
 * `[ {tray:[…]} ]`, plus `print.vt_tray` and the newer `print.vir_slot` external-spool key.
 */
function collectSlots(s: PrinterStatus): Slot[] {
  const slots: Slot[] = [];

  // Physical AMS units. `s.ams` is documented as an object carrying an `ams` array; accept a bare
  // array too rather than assume the wrapper is always present.
  const amsRaw = (s as Record<string, unknown>).ams;
  const units = Array.isArray(amsRaw)
    ? amsRaw
    : isRecord(amsRaw) && Array.isArray(amsRaw.ams)
      ? amsRaw.ams
      : [];
  units.forEach((unit, ui) => {
    if (!isRecord(unit)) return;
    const unitId = typeof unit.id === "string" ? unit.id : String(ui);
    const trays = Array.isArray(unit.tray) ? unit.tray : [];
    trays.forEach((tray, ti) => {
      if (!isRecord(tray)) return;
      const trayId = typeof tray.id === "string" ? tray.id : String(ti);
      slots.push({ where: `AMS ${unitId} · slot ${trayId}`, tray: tray as Tray });
    });
  });

  // External spool: the H2-family `vt_tray` object (sentinel id "254") and/or the X2D's `vir_slot`,
  // which arrives as an ARRAY of slots. Tag each with its slot id so two array entries are legible.
  const label = (base: string, t: unknown): string =>
    isRecord(t) && typeof t.id === "string" ? `${base} ${t.id}` : base;
  for (const [key, base] of [
    ["vt_tray", "External spool"],
    ["vir_slot", "External spool (vir_slot)"],
  ] as const) {
    const ext = (s as Record<string, unknown>)[key];
    if (isRecord(ext)) slots.push({ where: label(base, ext), tray: ext as Tray });
    else if (Array.isArray(ext))
      ext.forEach((t) => isRecord(t) && slots.push({ where: label(base, t), tray: t as Tray }));
  }

  return slots;
}

/** "#RRGGBB" from an "RRGGBBAA" hex, or null when it is missing / the empty sentinel. */
function colorHex(raw: string | undefined): string | null {
  if (!raw || /^0*$/.test(raw)) return null;
  const rgb = raw.slice(0, 6);
  return /^[0-9a-fA-F]{6}$/.test(rgb) ? `#${rgb.toUpperCase()}` : null;
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
