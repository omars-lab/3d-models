// The profile-header BUILDER — the join of the printer frame and the sliced `.3mf` that fills the
// Plate-1 bench sheet's "Profile header" block (docs/design/printing/bambu-header-autopull-design.md).
//
// This is PURE: it takes an already-read report frame and already-parsed `.3mf` metadata, and returns
// a structured header. No MQTT, no unzip, no clock-of-record beyond an injectable `now` — so it is
// unit-testable against fixtures, and it is the ONE builder both `bambu header` (stdout/--json) and
// `print send --record` (the record's profile block) consume (D-052: one code path, not a fork).
//
// The load-bearing rule (the design's Validator): a field is filled ONLY from a source that actually
// carried it. Machine-side fields the X2D has not been observed to answer (get_version firmware over
// MQTT, the AMS tray_uuid) are H2-proxy plausible but UNCONFIRMED — they print `unconfirmed` (with
// the real source to fall back on), NEVER a fabricated value. The nozzle fields moved out of that set
// on 2026-10-09: the X2D's report, read live during spl-2, carries a top-level `nozzle_type` ("HS01")
// and `nozzle_diameter` ("0.4") and one `device.nozzle.info[]` entry per nozzle, so they fill when the
// frame carries them. Genuinely-manual fields (ambient room temp, enclosure, caliper, settings-changed)
// print as the exact paper blanks. Fabricating a blank the machine did not answer is the by-design FAIL.

import type { PrinterStatus } from "./backends/mqtt.js";
import { readPlateMeta, type PlateMeta } from "./threemf.js";
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
  nozzle_diameter_frame: Field; // frame nozzle_diameter — a cross-check of the .3mf, never the record's size
  nozzle_type: Field; // the report's nozzle code, e.g. "HS01 (standard flow, hardened steel)" → else manual
  nozzle_side: Field; // .3mf: which nozzle (left / right) each filament was sliced onto
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

const FLOW: Record<string, string> = {
  S: "standard flow",
  A: "standard flow",
  X: "standard flow",
  H: "high flow",
  E: "high flow",
  U: "TPU high flow",
  B: "E3D high flow",
};
const MATERIAL: Record<string, string> = { "00": "stainless steel", "01": "hardened steel", "05": "tungsten carbide" };

/**
 * Spell out a nozzle code the printer reports, e.g. "HS01" → "standard flow, hardened steel". Read the
 * way Bambu Studio reads it (s_parse_nozzle_type in
 * https://github.com/bambulab/BambuStudio/blob/d1398b73d1151f78df7dea1ed9794d2b0a99deb4/src/slic3r/GUI/DeviceCore/DevNozzleSystem.cpp):
 * the second letter is the flow type and the next two digits the material. null for a code it cannot
 * read ("N/A", too short, an unknown letter or material), so the code is then recorded on its own.
 */
export function describeNozzleType(code: string): string | null {
  const c = code.trim();
  if (c.length < 4) return null;
  const flow = FLOW[c.charAt(1)];
  const material = MATERIAL[c.slice(2, 4)];
  return flow && material ? `${flow}, ${material}` : null;
}

interface ReportNozzle {
  id: number;
  type: string | null;
  diameter: string | null;
}

/** The report's per-nozzle list, `device.nozzle.info[]` (id 0 = right, 1 = left on the X2D). */
function reportNozzles(frame: PrinterStatus): ReportNozzle[] {
  const device = pick(frame, "device");
  const nozzle = device && typeof device === "object" ? (device as Record<string, unknown>).nozzle : undefined;
  const info = nozzle && typeof nozzle === "object" ? (nozzle as Record<string, unknown>).info : undefined;
  if (!Array.isArray(info)) return [];
  const out: ReportNozzle[] = [];
  for (const e of info) {
    if (!e || typeof e !== "object") continue;
    const r = e as Record<string, unknown>;
    const id = Number(r.id);
    if (!Number.isInteger(id)) continue;
    const type = r.type != null && String(r.type).trim() && String(r.type).trim() !== "N/A" ? String(r.type).trim() : null;
    const diameter = r.diameter != null && String(r.diameter).trim() ? String(r.diameter).trim() : null;
    out.push({ id, type, diameter });
  }
  return out;
}

/**
 * The nozzle type the print used: the `device.nozzle.info[]` entry for each nozzle the slice put a
 * filament on, else the report's top-level `nozzle_type`. The printer's code is kept verbatim, with
 * its plain reading beside it when describeNozzleType can give one.
 */
function nozzleTypeField(frame: PrinterStatus, plate: PlateMeta | null): Field {
  const label = (code: string) => {
    const words = describeNozzleType(code);
    return words ? `${code} (${words})` : code;
  };
  const used = [...new Set((plate?.nozzleSides ?? []).map((n) => n.physicalId).filter((n): n is number => n != null))];
  const nozzles = reportNozzles(frame);
  if (used.length) {
    const types = used.map((id) => nozzles.find((n) => n.id === id)?.type ?? null);
    if (types.every((t): t is string => t != null)) {
      const distinct = [...new Set(types)];
      if (distinct.length === 1) return filled(label(distinct[0]!), `report device.nozzle.info id ${used.join(",")}`);
      return filled(
        used.map((id, i) => `${id === 1 ? "left" : "right"} ${label(types[i]!)}`).join("; "),
        "report device.nozzle.info",
      );
    }
  }
  const top = pick(frame, "nozzle_type");
  if (top != null && String(top).trim() && String(top).trim() !== "N/A") {
    return filled(label(String(top).trim()), "report nozzle_type");
  }
  return manual("operator (the report carried no nozzle_type)");
}

/** Which nozzle the slice put each filament on; one word when they all agree. */
function nozzleSideField(plate: PlateMeta | null): Field {
  if (!plate) return todoPlate(".3mf filament_map — pass --plate");
  const sides = plate.nozzleSides;
  if (!sides.length) return unconfirmed(".3mf has no slice_info filament list");
  const blank = sides.find((s) => s.side == null);
  if (blank) return unconfirmed(`.3mf filament ${blank.filament}: ${blank.why}`);
  const distinct = [...new Set(sides.map((s) => s.side))];
  if (distinct.length === 1) return filled(distinct[0]!, ".3mf filament_map + physical_extruder_map");
  return filled(
    sides.map((s) => `filament ${s.filament} ${s.side}`).join(", "),
    ".3mf filament_map + physical_extruder_map",
  );
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
    : manual("operator (no color in the frame)");
  const material_brand = type ? materialBrand(tray) : manual("operator (no loaded tray)");

  // Spool id: tray_uuid is H2-proxy — not observed on the X2D AMS as of 2026-09-17. Fill it ONLY if
  // the frame actually carried it; otherwise mark unconfirmed rather than invent a spool SN.
  const uuid = (tray.tray_uuid ?? "").trim();
  const spool_id = uuid
    ? filled(uuid, "AMS tray_uuid")
    : unconfirmed("AMS tray_uuid (not observed on X2D; manual for third-party spools)");

  // ---- nozzle ----
  // The .3mf is the AUTHORITATIVE nozzle size: it is what the plate was sliced for. Without --plate we
  // do NOT print a size from the frame — the frame says what is fitted now, which is the cross-check.
  const slicedNozzle = plate && plate.nozzleDiameters.length ? plate.nozzleDiameters.join(",") : null;
  const nozzle_diameter = slicedNozzle
    ? filled(`${slicedNozzle} mm`, ".3mf nozzle_diameter")
    : todoPlate(".3mf nozzle_diameter — pass --plate");
  const fNozzle = frameNozzle(frame);
  const nozzle_diameter_frame = fNozzle
    ? filled(`${fNozzle} mm`, "report nozzle_diameter (cross-check of the .3mf)")
    : unconfirmed("report nozzle_diameter (absent from this frame; the .3mf is the size of record)");
  // The type: the report's code for the nozzle(s) the slice used (seen on the X2D 2026-10-09).
  const nozzle_type = nozzleTypeField(frame, plate);
  const nozzle_side = nozzleSideField(plate);

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
    nozzle_side,
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
    `Material  brand ${show(h.material_brand, "______________")}  type ${show(h.material_type, "______")}  COLOR ${show(h.material_color, "______________")}  (color changes flow — record it)`,
  );
  lines.push(`Spool     ${show(h.spool_id, "______________________")}  (so a re-measure can rule the spool in or out)`);
  lines.push(
    `Nozzle    diameter ${show(h.nozzle_diameter, "______")}  type ${show(h.nozzle_type, "______")}  (brass / hardened / CHT — they do not flow alike)`,
  );
  lines.push(`          which nozzle: ${show(h.nozzle_side, "left / right")}`);
  if (h.nozzle_diameter_frame.value) {
    lines.push(`          fitted now (report, cross-check): ${h.nozzle_diameter_frame.value}`);
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
  nozzle_side?: string;
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
    nozzle_side: val(h.nozzle_side),
    layer_mm: val(h.layer_height),
    slicer_profile: val(h.profile),
  };
}

/** The profile block from a frame we ALREADY read + (optionally) the sliced .3mf. Pure of MQTT — the
 *  caller owns the read — so `print capture` (which already holds a frame) and `print send --record`
 *  share one profile builder (D-052: one code path), and so does `slice compose`, which
 *  passes an empty frame: it never talks to the printer, so only the slice-side fields fill. Without a plate, material/spool still fill from
 *  the frame's AMS; the slice-side fields stay TODO. */
export async function recordProfileFrom(frame: PrinterStatus, plateFile?: string): Promise<RecordProfile | undefined> {
  try {
    const plateMeta = plateFile ? await readPlateMeta(plateFile) : null;
    return headerToRecordProfile(buildHeader(frame, plateMeta));
  } catch {
    return undefined; // fall back to the TODO scaffold
  }
}
