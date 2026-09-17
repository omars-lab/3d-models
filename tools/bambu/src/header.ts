// The profile-header BUILDER — the join of the printer frame and the sliced `.3mf` that fills the
// Plate-1 bench sheet's "Profile header" block (docs/bambu-header-autopull-design.md).
//
// This is PURE: it takes an already-read report frame and already-parsed `.3mf` metadata, and returns
// a structured header. No MQTT, no unzip, no clock-of-record beyond an injectable `now` — so it is
// unit-testable against fixtures, and it is the ONE builder both `bambu header` (stdout/--json) and
// `print send --record` (the record's profile block) consume (D-052: one code path, not a fork).
//
// The load-bearing rule (the design's Validator): a field is filled ONLY from a source that actually
// carried it. Machine-side fields the X2D has not been observed to answer (get_version firmware over
// MQTT, the frame's nozzle_diameter/nozzle_type, the AMS tray_uuid) are H2-proxy plausible but
// UNCONFIRMED — they print `unconfirmed` (with the real source to fall back on), NEVER a fabricated
// value. Genuinely-manual fields (ambient room temp, enclosure, caliper, settings-changed) print as
// the exact paper blanks. Fabricating a blank the machine did not answer is the by-design FAIL.

import type { PrinterStatus } from "./backends/mqtt.js";
import type { PlateMeta } from "./threemf.js";
import { colorHex, loadedSlot, pick, type Tray } from "./frame.js";

/** How a field got its value — drives both rendering and the honesty guarantee. */
export type FieldState =
  | "filled" // machine-read from a source that actually carried it
  | "todo-plate" // slice-side; needs `--plate <file.3mf>` to source it
  | "unconfirmed" // H2-proxy plausible but not observed on this X2D — never fabricate
  | "manual"; // the printer cannot know it; the operator fills the blank

export interface Field {
  value: string | null; // the machine-known value, or null when not filled
  state: FieldState;
  source: string; // where the value came from, or where to get it (SSDP, .3mf, operator)
}

export interface Header {
  machine: Field; // slice-side: printer_settings_id / printer_model
  firmware: Field; // H2-proxy unconfirmed over MQTT — SSDP (`bambu setup discover`) is the source
  material_type: Field; // AMS tray_type
  material_color: Field; // AMS tray_color → #RRGGBB
  material_brand: Field; // AMS tray_sub_brands (Bambu RFID) — else manual
  spool_id: Field; // AMS tray_uuid — H2-proxy unconfirmed / Bambu-RFID only
  nozzle_diameter: Field; // AUTHORITATIVE from .3mf; todo-plate without it — never from the frame alone
  nozzle_diameter_frame: Field; // frame nozzle_diameter — cross-check ONLY, H2-proxy unconfirmed
  nozzle_type: Field; // frame nozzle_type — H2-proxy unconfirmed → else manual
  layer_height: Field; // slice-side: layer_height
  profile: Field; // slice-side: print_settings_id + filament_settings_id
  slicer_version: Field; // slice-side: Application / X-BBL-Client-Version
  chamber_c: Field; // frame chamber_temper — a LABELLED proxy, never auto-filled into ambient room
  date: Field; // clock (UTC)
  ambient_room_c: Field; // manual (chamber is NOT room temp)
  enclosure: Field; // manual (no reliable door-state field)
  settings_changed: Field; // manual (operator intent, not a raw setting diff)
  caliper: Field; // manual (operator's instrument)
  /** Loud warning when the loaded nozzle (frame) disagrees with the sliced-for nozzle (.3mf). */
  nozzle_mismatch: string | null;
}

const filled = (value: string, source: string): Field => ({ value, state: "filled", source });
const todoPlate = (source: string): Field => ({ value: null, state: "todo-plate", source });
const unconfirmed = (source: string): Field => ({ value: null, state: "unconfirmed", source });
const manual = (source: string): Field => ({ value: null, state: "manual", source });

/** A single frame nozzle_diameter reading normalised to a comma-joined string, or null. */
function frameNozzle(frame: PrinterStatus): string | null {
  const raw = pick(frame, "nozzle_diameter", "nozzle_dia");
  if (raw == null) return null;
  if (Array.isArray(raw)) return raw.length ? raw.map(String).join(",") : null;
  const s = String(raw).trim();
  return s ? s : null;
}

function materialBrand(t: Tray): Field {
  const brand = (t.tray_sub_brands ?? "").trim();
  // A Bambu RFID spool carries its sub-brand in the frame; a third-party spool does not, so it is the
  // operator's to name — never inferred.
  if (brand) return filled(brand, "AMS tray_sub_brands (Bambu RFID)");
  return manual("operator (third-party spool has no RFID brand)");
}

/** Build the profile header from a report frame and (optionally) parsed `.3mf` metadata. */
export function buildHeader(frame: PrinterStatus, plate: PlateMeta | null, now: Date = new Date()): Header {
  const slot = loadedSlot(frame);
  const tray = slot?.tray ?? {};

  // ---- material (printer-side, from the AMS) ----
  const type = (tray.tray_type ?? "").trim();
  const material_type = type
    ? filled(type, "AMS tray_type")
    : manual("operator (no loaded tray in the frame)");
  const hex = colorHex(tray.tray_color);
  const material_color = hex
    ? filled(hex, "AMS tray_color")
    : manual("operator (no colour in the frame)");
  const material_brand = type ? materialBrand(tray) : manual("operator (no loaded tray)");

  // Spool id: tray_uuid is H2-proxy — not observed on the X2D AMS as of 2026-09-17. Fill it ONLY if
  // the frame actually carried it; otherwise mark unconfirmed rather than invent a spool SN.
  const uuid = (tray.tray_uuid ?? "").trim();
  const spool_id = uuid
    ? filled(uuid, "AMS tray_uuid")
    : unconfirmed("AMS tray_uuid (not observed on X2D; manual for third-party spools)");

  // ---- nozzle ----
  // The .3mf is the AUTHORITATIVE nozzle source. Without --plate we do NOT print a diameter — the
  // frame's nozzle_diameter is unconfirmed on this machine, so filling from it would be the FAIL case.
  const slicedNozzle = plate && plate.nozzleDiameters.length ? plate.nozzleDiameters.join(",") : null;
  const nozzle_diameter = slicedNozzle
    ? filled(`${slicedNozzle} mm`, ".3mf nozzle_diameter")
    : todoPlate(".3mf nozzle_diameter — pass --plate");
  const fNozzle = frameNozzle(frame);
  const nozzle_diameter_frame = fNozzle
    ? { value: `${fNozzle} mm`, state: "unconfirmed" as const, source: "frame nozzle_diameter (cross-check only, H2-proxy)" }
    : unconfirmed("frame nozzle_diameter (not observed on X2D; .3mf is authoritative)");
  const fType = pick(frame, "nozzle_type");
  const nozzle_type =
    fType != null && String(fType).trim()
      ? { value: String(fType).trim(), state: "unconfirmed" as const, source: "frame nozzle_type (H2-proxy)" }
      : manual("operator (nozzle_type not observed on X2D frame)");

  // Cross-check: loaded nozzle (frame) vs sliced-for nozzle (.3mf). A mismatch is a real bench error.
  let nozzle_mismatch: string | null = null;
  if (slicedNozzle && fNozzle) {
    const norm = (v: string) => v.split(",").map((x) => Number(x)).filter((n) => !Number.isNaN(n));
    const a = norm(slicedNozzle);
    const b = norm(fNozzle);
    const disjoint = a.every((x) => !b.includes(x)) || b.every((x) => !a.includes(x));
    if (disjoint) {
      nozzle_mismatch = `loaded nozzle (frame ${fNozzle}) ≠ sliced-for nozzle (.3mf ${slicedNozzle}) — the plate was sliced for a nozzle the machine is not wearing`;
    }
  }

  // ---- slice-side fields (need --plate) ----
  const machine = plate?.machine
    ? filled(plate.machine, ".3mf printer_settings_id")
    : plate?.printerModel
      ? filled(plate.printerModel, ".3mf printer_model")
      : todoPlate(".3mf printer_settings_id — pass --plate");
  const layer_height = plate?.layerHeight
    ? filled(`${plate.layerHeight} mm`, ".3mf layer_height")
    : todoPlate(".3mf layer_height — pass --plate");
  const profileName =
    plate && (plate.printSettingsId || plate.filamentSettingsId)
      ? [plate.printSettingsId, plate.filamentSettingsId].filter(Boolean).join(" + ")
      : null;
  const profile = profileName
    ? filled(profileName, ".3mf print_settings_id + filament_settings_id")
    : todoPlate(".3mf print_settings_id + filament_settings_id — pass --plate");
  const slicer_version = plate?.slicerVersion
    ? filled(plate.slicerVersion, ".3mf Application / X-BBL-Client-Version")
    : todoPlate(".3mf Application — pass --plate");

  // ---- firmware: MQTT get_version is H2-proxy unconfirmed; SSDP `setup discover` is the real source ----
  const firmware = unconfirmed("MQTT get_version not sent; confirm via `bambu setup discover` (SSDP)");

  // ---- chamber: a labelled proxy, printed on its OWN line — never auto-filled into ambient room ----
  const chamberRaw = pick(frame, "chamber_temper");
  const chamber_c =
    chamberRaw != null
      ? filled(`${chamberRaw}°C`, "frame chamber_temper (chamber, NOT room)")
      : unconfirmed("frame chamber_temper (which chamber field the X2D reports is unconfirmed)");

  const date = filled(now.toISOString().slice(0, 10), "clock (UTC)");

  return {
    machine,
    firmware,
    material_type,
    material_color,
    material_brand,
    spool_id,
    nozzle_diameter,
    nozzle_diameter_frame,
    nozzle_type,
    layer_height,
    profile,
    slicer_version,
    chamber_c,
    date,
    ambient_room_c: manual("operator (chamber_temper is chamber, not room)"),
    enclosure: manual("operator (no reliable door-state field)"),
    settings_changed: manual("operator (intent, not a raw setting diff)"),
    caliper: manual("operator's instrument"),
    nozzle_mismatch,
  };
}

/** How a field shows in the bench-sheet text: the value, or a labelled state marker. */
function show(f: Field, blank: string): string {
  if (f.state === "filled" && f.value != null) return f.value;
  if (f.state === "todo-plate") return "TODO — pass --plate";
  if (f.state === "unconfirmed") return `unconfirmed (${f.source})`;
  return blank; // manual → the exact paper blank
}

/**
 * Render the header as the bench sheet's "Profile header" block, so the printed output IS the header
 * (docs/prints/plate-1-bench-sheet.md) — not a second format to reconcile. Manual lines keep the
 * paper's exact blanks; chamber gets its own labelled line; a nozzle mismatch shouts at the top.
 */
export function renderHeader(h: Header): string {
  const lines: string[] = [];
  if (h.nozzle_mismatch) {
    lines.push(`⚠ NOZZLE MISMATCH: ${h.nozzle_mismatch}`);
    lines.push("");
  }
  lines.push(`Machine   ${show(h.machine, "______________________")}  firmware ${show(h.firmware, "____________")}`);
  lines.push(
    `Material  brand ${show(h.material_brand, "______________")}  type ${show(h.material_type, "______")}  COLOUR ${show(h.material_color, "______________")}  (colour changes flow — record it)`,
  );
  lines.push(`Spool     ${show(h.spool_id, "______________________")}  (so a re-measure can rule the spool in or out)`);
  lines.push(
    `Nozzle    diameter ${show(h.nozzle_diameter, "______")}  type ${show(h.nozzle_type, "______")}  (brass / hardened / CHT — they do not flow alike)`,
  );
  if (h.nozzle_diameter_frame.value) {
    lines.push(`          frame nozzle (cross-check, ${h.nozzle_diameter_frame.state}): ${h.nozzle_diameter_frame.value}`);
  }
  lines.push(`Layer height ${show(h.layer_height, "______")}`);
  lines.push(`Profile   ${show(h.profile, "________________________________")}  (slicer profile name VERBATIM)`);
  lines.push(`          slicer version: ${show(h.slicer_version, "____________")}`);
  lines.push(`          settings changed from it: ______________________________________`);
  lines.push(`Ambient   room ~____°C   enclosure: open / closed`);
  lines.push(`          chamber (printer proxy, NOT room temp): ${show(h.chamber_c, "____")}`);
  lines.push(`Date      ${show(h.date, "____________")}`);
  lines.push(`Caliper   make ____________  resolution ______  zeroed at session start? y / n`);
  return lines.join("\n");
}

/** The record's profile block (records.ts) — the SAME builder pre-filling `print send --record`. */
export interface RecordProfile {
  machine?: string;
  material?: string;
  spool?: string;
  nozzle_mm?: string;
  nozzle_type?: string;
  layer_mm?: string;
  slicer_profile?: string;
}

/** Map a built header onto the record's profile keys — only genuinely-filled fields carry over. */
export function headerToRecordProfile(h: Header): RecordProfile {
  const val = (f: Field): string | undefined => (f.state === "filled" && f.value ? f.value : undefined);
  const material = (() => {
    const parts = [val(h.material_type), val(h.material_color), val(h.material_brand)].filter(Boolean);
    return parts.length ? parts.join(" ") : undefined;
  })();
  return {
    machine: val(h.machine),
    material,
    spool: val(h.spool_id),
    nozzle_mm: val(h.nozzle_diameter),
    nozzle_type: val(h.nozzle_type),
    layer_mm: val(h.layer_height),
    slicer_profile: val(h.profile),
  };
}
