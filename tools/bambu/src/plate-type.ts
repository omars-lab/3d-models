// The build plate a slice is made for, and the one on the bed.
//
// Bambu Studio slices for one plate type, `curr_bed_type` in the process config, and it is not a
// label: it picks the bed temperature (`cool_plate_temp` or `textured_plate_temp`, …) and, in the X2D
// start G-code, a first-layer nozzle offset only a Textured PEI Plate gets. The X2D's camera reads the
// plate's marker before it prints (the printer-wide `buildplate_marker_detector` setting; the G-code's
// own `build_plate_detect_flag=1` line is commented out) and pauses with HMS 0500-8051 when the plate
// is not the one the job names. Studio's headless CLI defaults to Cool Plate
// (`curr_bed_type` = btPC, PrintConfig.cpp) and our slices never set it, so sheets-04b was sliced for
// a Cool Plate while a Textured PEI Plate sat on the bed (bed photo, 2026-10-03), then sent as
// "auto", a value Studio never sends. See docs/issues/first-party-dispatch.md.
//
// Every name below is Studio's own, read from its source (BambuStudio 02.08, 2026-10-03):
// `s_keys_map_BedType` in PrintConfig.cpp gives the config name, `bed_type_to_gcode_string` in
// PrintConfig.hpp the token the start command carries, and the `BedType` enum order the number
// BambuStudio.conf stores. The parse is PURE; the IO (`readSlicePlateType`, `studioSavedPlateType`)
// is kept apart so the tests need no zip and no Studio install.

import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { readMember } from "./threemf.js";

export interface PlateType {
  token: string; // what the start command's `bed_type` carries, e.g. "textured_plate"
  name: string; // Studio's `curr_bed_type` name, e.g. "Textured PEI Plate"
  index: number; // the BedType enum value BambuStudio.conf stores
}

export const PLATE_TYPES: readonly PlateType[] = [
  { token: "cool_plate", name: "Cool Plate", index: 1 },
  { token: "eng_plate", name: "Engineering Plate", index: 2 },
  { token: "hot_plate", name: "High Temp Plate", index: 3 },
  { token: "textured_plate", name: "Textured PEI Plate", index: 4 },
  { token: "supertack_plate", name: "Supertack Plate", index: 5 },
];

export function plateTypeFromToken(token: string): PlateType | null {
  return PLATE_TYPES.find((p) => p.token === token.trim().toLowerCase()) ?? null;
}

export function plateTypeFromName(name: string): PlateType | null {
  return PLATE_TYPES.find((p) => p.name === name.trim()) ?? null;
}

/** A plate type given on the command line, or throw naming the ones there are. */
export function parsePlateTypeFlag(token: string): PlateType {
  const hit = plateTypeFromToken(token);
  if (!hit) {
    throw new Error(`unknown plate type "${token}". Use one of: ${PLATE_TYPES.map((p) => p.token).join(", ")}.`);
  }
  return hit;
}

export interface SlicePlateType {
  type: PlateType | null; // null: the file names no plate type we know
  from: string; // where it was read, or why nothing was
}

/**
 * The plate type a sliced file was made for. Studio's own send prefers the per-plate value
 * (`plate_data.bed_type`, PrintJob.cpp), which is `Metadata/plate_<n>.json`, and falls back to the
 * project's `curr_bed_type` in `Metadata/project_settings.config`. PURE: pass the two members' text,
 * or null for a member the file does not have.
 */
export function parseSlicePlateType(plateJson: string | null, projectSettings: string | null, plate = 1): SlicePlateType {
  const member = `Metadata/plate_${plate}.json`;
  if (plateJson) {
    let raw: unknown;
    try {
      raw = (JSON.parse(plateJson) as Record<string, unknown>).bed_type;
    } catch {
      raw = undefined;
    }
    if (typeof raw === "string" && raw) {
      const type = plateTypeFromToken(raw);
      return type ? { type, from: member } : { type: null, from: `${member} names "${raw}", not a plate type Studio knows` };
    }
  }
  if (projectSettings) {
    let raw: unknown;
    try {
      raw = (JSON.parse(projectSettings) as Record<string, unknown>).curr_bed_type;
    } catch {
      raw = undefined;
    }
    if (typeof raw === "string" && raw) {
      const type = plateTypeFromName(raw);
      return type
        ? { type, from: "Metadata/project_settings.config" }
        : { type: null, from: `project_settings.config names "${raw}", not a plate type Studio knows` };
    }
  }
  return { type: null, from: `the file carries no plate type (no ${member} bed_type, no curr_bed_type)` };
}

export async function readSlicePlateType(threemf: string, plate = 1): Promise<SlicePlateType> {
  const [plateJson, settings] = await Promise.all([
    readMember(threemf, `Metadata/plate_${plate}.json`),
    readMember(threemf, "Metadata/project_settings.config"),
  ]);
  return parseSlicePlateType(plateJson, settings, plate);
}

/** Where Bambu Studio keeps its app settings on macOS. */
export function studioConfPath(): string {
  return join(homedir(), "Library", "Application Support", "BambuStudio", "BambuStudio.conf");
}

/**
 * The plate type Bambu Studio is set to, which is what a project made in Studio slices for. Reads
 * only `app.curr_bed_type` (an enum number; AppConfig keeps its plain keys in the "app" section) and
 * nothing else: the same file holds the printer's access code. PURE over the file's text.
 */
export function parseStudioSavedPlateType(confText: string): PlateType | null {
  let raw: unknown;
  try {
    const app = (JSON.parse(confText) as Record<string, unknown>).app as Record<string, unknown> | undefined;
    raw = app?.curr_bed_type;
  } catch {
    return null;
  }
  const n = Number(raw);
  return PLATE_TYPES.find((p) => p.index === n) ?? null;
}

export function studioSavedPlateType(confPath = studioConfPath()): PlateType | null {
  if (!existsSync(confPath)) return null;
  try {
    return parseStudioSavedPlateType(readFileSync(confPath, "utf8"));
  } catch {
    return null;
  }
}

/**
 * The plate type to slice for: the one asked for, else the one Bambu Studio is set to (so a slice
 * here matches a slice made in Studio), else throw. Never Studio's built-in Cool Plate default,
 * which is what put the wrong plate into sheets-04b.
 */
export function resolveSlicePlateType(flag: string | undefined, saved: PlateType | null): { type: PlateType; from: string } {
  if (flag) return { type: parsePlateTypeFlag(flag), from: "--plate-type" };
  if (saved) return { type: saved, from: "Bambu Studio's saved plate type" };
  throw new Error(
    "no plate type: Bambu Studio's settings name none. Pass --plate-type " +
      `(${PLATE_TYPES.map((p) => p.token).join(", ")}) for the plate on the bed.`,
  );
}

/**
 * The printer's own plate report, `print.device.plate.cur_id`, decoded only where we have seen an id
 * next to a plate we could name. No source decodes these ids (both research passes, 2026-10-03), so
 * this list grows one sighting at a time; an id not on it is shown, never guessed at.
 */
export const PRINTER_PLATE_IDS: Readonly<Record<string, { token: string; seen: string }>> = {
  P0101: {
    token: "textured_plate",
    seen: "2026-10-03: the X2D reported P0101 while the bed photo showed a Textured PEI Plate and Bambu Studio was set to one",
  },
};

/** The printer's `device.plate.cur_id` from a status frame, or null when it does not report one. */
export function printerPlateId(frame: Record<string, unknown> | null | undefined): string | null {
  const device = frame?.device as Record<string, unknown> | undefined;
  const plate = device?.plate as Record<string, unknown> | undefined;
  const id = plate?.cur_id;
  return typeof id === "string" && id.trim() ? id.trim() : null;
}

export interface PlateCheck {
  ok: boolean; // false: refuse the send
  line: string; // the dry run's ✓ / ⚠ / ✗ line, without the mark
  mark: "✓" | "⚠" | "✗";
}

/** Compare the slice's plate type with what the printer says is on the bed. PURE. */
export function checkPlate(slice: SlicePlateType, printerPlateId: string | null | undefined): PlateCheck {
  if (!slice.type) {
    return { ok: false, mark: "✗", line: `plate: ${slice.from}. Slice it again with --plate-type for the plate on the bed.` };
  }
  const want = `the slice is for a ${slice.type.name} (${slice.from})`;
  const id = printerPlateId?.trim() || "";
  if (!id) return { ok: true, mark: "⚠", line: `plate: ${want}; the printer did not say which plate it has. Check the bed photo.` };
  const known = PRINTER_PLATE_IDS[id];
  if (!known) {
    return { ok: true, mark: "⚠", line: `plate: ${want}; the printer reports plate ${id}, an id we have not matched to a plate yet. Check the bed photo.` };
  }
  const onBed = plateTypeFromToken(known.token);
  if (known.token !== slice.type.token) {
    return {
      ok: false,
      mark: "✗",
      line: `plate: ${want}, but the printer reports ${id}, a ${onBed?.name ?? known.token}. Slice it again for that plate, or change the plate.`,
    };
  }
  return { ok: true, mark: "✓", line: `plate: ${want}; the printer reports ${id}, a ${onBed?.name ?? known.token}.` };
}
