// Shared parsing of the printer's MQTT pushall report frame (`print`/`mc_print`).
//
// `status`, `filament` and `header` all read the SAME cached report, so the shape-tolerant helpers
// that dig fields out of it live here — one code path, never two that can drift (the repo's D-052
// tenet). The frame drifts field names and shapes by model (the X2D reports `vir_slot` as an ARRAY,
// verified 2026-09-17 on 20P6AJ641401412, where the H2 family uses a `vt_tray` OBJECT), so every
// helper is defensive and never assumes a shape it has not seen.

import type { PrinterStatus } from "./backends/mqtt.js";

export function isRecord(v: unknown): v is Record<string, unknown> {
  // Arrays are `typeof "object"` too — exclude them, or an array-valued key (e.g. the X2D's
  // `vir_slot`) is mistaken for one record.
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

/** First scalar found among candidate keys, else undefined. The frame drifts field names by model. */
export function pick(s: PrinterStatus, ...keys: string[]): unknown {
  for (const k of keys) if (s[k] !== undefined && s[k] !== null) return s[k];
  return undefined;
}

/** One filament slot as we surface it, from an AMS tray or the external spool. */
export interface Tray {
  id?: string;
  tray_type?: string; // "PLA", "PETG", … ; "" when the slot is empty
  tray_color?: string; // RRGGBBAA hex
  tray_sub_brands?: string; // e.g. "PLA Basic"
  tray_info_idx?: string; // Bambu filament-profile id, e.g. "GFA00"
  tray_uuid?: string; // Studio tray SN (Bambu-RFID only) — H2-proxy, not seen on the X2D 2026-09-17
  remain?: number; // percent remaining; -1 = no RFID / unknown
}

export interface Slot {
  where: string; // human label: "AMS 0 · slot 1" or "External spool"
  tray: Tray;
}

/**
 * Pull every filament slot out of a report frame, tolerant of the shapes the H2/X2D line drifts
 * across. Handles `print.ams` as either `{ ams: [ {tray:[…]} ] }` (documented) or a bare
 * `[ {tray:[…]} ]`, plus `print.vt_tray` (object) and the newer `print.vir_slot` (array).
 */
export function collectSlots(s: PrinterStatus): Slot[] {
  const slots: Slot[] = [];

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
export function colorHex(raw: string | undefined): string | null {
  if (!raw || /^0*$/.test(raw)) return null;
  const rgb = raw.slice(0, 6);
  return /^[0-9a-fA-F]{6}$/.test(rgb) ? `#${rgb.toUpperCase()}` : null;
}

/** The first slot that carries a non-empty `tray_type` — the loaded filament the header describes. */
export function loadedSlot(s: PrinterStatus): Slot | null {
  return collectSlots(s).find((sl) => (sl.tray.tray_type ?? "").trim()) ?? null;
}
