// Shared reader for the sliced `.3mf` (a zip). `validate sliced` and `header` both read the same
// members off the plate, so the `unzip` shell-outs live in one place — no bundled zip lib, one code
// path (the repo's D-052 tenet). The IO (`readMember`/`listMembers`) is separated from the pure
// parse (`parseProjectSettings`) so the header BUILDER can be unit-tested against fixture metadata
// with no zip, no printer, and no filesystem.

import { copyFileSync, existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { runWithTimeout } from "./log.js";

/** unzip -p one member of a .3mf to a string. Small members only (config/json). */
export async function readMember(threemf: string, member: string): Promise<string | null> {
  const res = await runWithTimeout("unzip", ["-p", threemf, member], {
    timeoutMs: 30_000,
    label: "unzip_member",
  });
  if (res.code !== 0 || !res.stdout) return null;
  return res.stdout;
}

/** List archive members (unzip -Z1). */
export async function listMembers(threemf: string): Promise<string[]> {
  const res = await runWithTimeout("unzip", ["-Z1", threemf], { timeoutMs: 30_000, label: "unzip_list" });
  if (res.code !== 0) return [];
  return res.stdout.split("\n").map((s) => s.trim()).filter(Boolean);
}

/** Where the plate picture for a sliced `.3mf` goes: next to it, as `<name>.preview.png`. */
export function previewPathFor(threemf: string): string {
  return threemf.replace(/\.3mf$/i, "") + ".preview.png";
}

/**
 * Copy the picture Bambu Studio draws of a sliced plate (`Metadata/plate_<n>.png`) out of the `.3mf`
 * to `previewPathFor(threemf)`, so the plate can be looked at before sending without unzipping it.
 * `unzip -p` would pass the PNG through a utf8 string, so this extracts to a temp dir and copies.
 * Returns the picture's path, or null when the plate has no picture (an unsliced export).
 */
export async function writePlatePreview(threemf: string, plate = 1): Promise<string | null> {
  const tmp = mkdtempSync(join(tmpdir(), "bambu-preview-"));
  try {
    const res = await runWithTimeout("unzip", ["-o", "-j", threemf, `Metadata/plate_${plate}.png`, "-d", tmp], {
      timeoutMs: 30_000,
      label: "unzip_preview",
    });
    const png = join(tmp, `plate_${plate}.png`);
    if (res.code !== 0 || res.timedOut || !existsSync(png)) return null;
    const out = previewPathFor(threemf);
    copyFileSync(png, out);
    return out;
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

/** The slice-side header fields the `.3mf` stamps — every value comes from a key the file carried. */
export interface PlateMeta {
  machine: string | null; // printer_settings_id (the preset name), e.g. "Bambu Lab X2D 0.4 nozzle"
  printerModel: string | null; // printer_model, e.g. "Bambu Lab X2D"
  nozzleDiameters: string[]; // nozzle_diameter, e.g. ["0.4","0.4"] — authoritative source for nozzle
  layerHeight: string | null; // layer_height, e.g. "0.2"
  printSettingsId: string | null; // print_settings_id — the process profile name
  filamentSettingsId: string | null; // filament_settings_id — the filament profile name
  slicerVersion: string | null; // Application / X-BBL-Client-Version, e.g. "BambuStudio-02.08.02.61"
  filamentColors: string[]; // filament_colour[] in slice/logical order — one per logical AMS slot
  filamentTypes: string[]; // filament_type[] in the same order; "" for a slot the config left blank
}

function firstString(v: unknown): string | null {
  if (typeof v === "string" && v.trim()) return v.trim();
  if (Array.isArray(v)) {
    for (const e of v) {
      const s = firstString(e);
      if (s) return s;
    }
  }
  return null;
}

/**
 * Parse `Metadata/project_settings.config` (JSON) into the header fields. PURE — no IO. Tolerant of
 * the array-valued keys BambuStudio uses (`printer_settings_id`, `nozzle_diameter`, … all ship as
 * one-element arrays). Every field is null/[] when the key is absent, so the builder can tell
 * "filled from the file" from "the file did not carry it" and never fabricate.
 */
export function parseProjectSettings(json: string): PlateMeta {
  let s: Record<string, unknown> = {};
  try {
    s = JSON.parse(json) as Record<string, unknown>;
  } catch {
    // Unparseable config → an empty meta; the caller reports "the file did not carry it".
    return {
      machine: null,
      printerModel: null,
      nozzleDiameters: [],
      layerHeight: null,
      printSettingsId: null,
      filamentSettingsId: null,
      slicerVersion: null,
      filamentColors: [],
      filamentTypes: [],
    };
  }
  const nozzle = s.nozzle_diameter;
  return {
    machine: firstString(s.printer_settings_id),
    printerModel: firstString(s.printer_model),
    nozzleDiameters: Array.isArray(nozzle) ? nozzle.map(String) : nozzle != null ? [String(nozzle)] : [],
    layerHeight: firstString(s.layer_height),
    printSettingsId: firstString(s.print_settings_id),
    filamentSettingsId: firstString(s.filament_settings_id),
    slicerVersion: firstString(s.version) ?? firstString(s.Application) ?? firstString(s["X-BBL-Client-Version"]),
    filamentColors: Array.isArray(s.filament_colour) ? s.filament_colour.map(String) : [],
    filamentTypes: Array.isArray(s.filament_type) ? s.filament_type.map(String) : [],
  };
}

/** Read + parse the plate's project_settings.config. null when the file has no such member. */
export async function readPlateMeta(threemf: string): Promise<PlateMeta | null> {
  const raw = await readMember(threemf, "Metadata/project_settings.config");
  if (!raw) return null;
  return parseProjectSettings(raw);
}

/**
 * The 1-based filament ids plate `plate` actually prints with, from `Metadata/slice_info.config`
 * (`<plate><metadata key="index" value="N"/> … <filament id="1" …/>`). project_settings lists every
 * filament in the project, used or not; a send must map only the used ones, or an unused slot would
 * demand a tray the print never touches. PURE. [] when the plate is absent or lists none.
 */
export function parseUsedFilaments(xml: string, plate = 1): number[] {
  for (const block of xml.match(/<plate>[\s\S]*?<\/plate>/g) ?? []) {
    const index = block.match(/<metadata\s+key="index"\s+value="(\d+)"/);
    if (!index || Number(index[1]) !== plate) continue;
    const ids = [...block.matchAll(/<filament\s+id="(\d+)"/g)].map((m) => Number(m[1]));
    return [...new Set(ids)].sort((a, b) => a - b);
  }
  return [];
}

/** Read the used filament ids of one plate. null when the .3mf has no slice_info (not sliced). */
export async function readUsedFilaments(threemf: string, plate = 1): Promise<number[] | null> {
  const raw = await readMember(threemf, "Metadata/slice_info.config");
  if (!raw) return null;
  return parseUsedFilaments(raw, plate);
}

/** One bed of a sliced `.3mf`: Bambu Studio's `--arrange` opens a second bed (plate) when the first
 *  is full, and each gets its own `<plate>` in slice_info.config and its own `plate_<n>.gcode`. */
export interface SlicedBed {
  index: number; // 1-based plate index
  objects: string[]; // object names on this bed (the input STL basenames, e.g. "it-<sha12>.stl")
  predictionS: number | null; // the slicer's time estimate for this bed alone
}

/**
 * Every bed in `Metadata/slice_info.config`, in index order. PURE. A plate that spilled onto a
 * second bed prints only bed 1 on a send (the default `--plate 1`), so the bed count is the thing to
 * check — minis-05 sliced 12 objects as 11 + 1 and nothing said so. [] when no `<plate>` is listed.
 */
export function parseBeds(xml: string): SlicedBed[] {
  const beds: SlicedBed[] = [];
  for (const block of xml.match(/<plate>[\s\S]*?<\/plate>/g) ?? []) {
    const index = block.match(/<metadata\s+key="index"\s+value="(\d+)"/);
    if (!index) continue;
    const pred = block.match(/<metadata\s+key="prediction"\s+value="(\d+(?:\.\d+)?)"/);
    beds.push({
      index: Number(index[1]),
      objects: [...block.matchAll(/<object\b[^>]*\bname="([^"]*)"/g)].map((m) => m[1] ?? ""),
      predictionS: pred ? Number(pred[1]) : null,
    });
  }
  return beds.sort((a, b) => a.index - b.index);
}

/** Read the beds of a sliced `.3mf`. null when the .3mf has no slice_info (not sliced). */
export async function readBeds(threemf: string): Promise<SlicedBed[] | null> {
  const raw = await readMember(threemf, "Metadata/slice_info.config");
  if (!raw) return null;
  return parseBeds(raw);
}

/** Where `--arrange` put one object: its 3MF object id, its name (the input STL basename) and the
 *  centre and turn of its build transform, in bed millimetres. */
export interface Placement {
  objectId: string;
  name: string;
  x: number;
  y: number;
  turnDeg: number; // rotation about z, counter-clockwise, 0 when arrange left it as rendered
}

/**
 * Every placed object of a sliced `.3mf`, in build order. PURE. The position is the `<item>`
 * transform in `3D/3dmodel.model` (12 numbers, row-vector form, the last three the move); the name
 * is the object's `name` in `Metadata/model_settings.config`, which Studio sets to the input file's
 * basename. An item whose object has no name keeps "" (the caller says it cannot be matched).
 */
export function parsePlacements(modelXml: string, settingsXml: string): Placement[] {
  const names = new Map<string, string>();
  for (const block of settingsXml.match(/<object\s+id="[^"]*">[\s\S]*?<\/object>/g) ?? []) {
    const id = block.match(/<object\s+id="([^"]*)"/)?.[1];
    const name = block.match(/<metadata\s+key="name"\s+value="([^"]*)"/)?.[1];
    if (id !== undefined && name !== undefined) names.set(id, name);
  }
  const build = modelXml.match(/<build\b[\s\S]*?<\/build>/)?.[0] ?? "";
  const out: Placement[] = [];
  for (const m of build.matchAll(/<item\b[^>]*>/g)) {
    const tag = m[0];
    const objectId = tag.match(/\bobjectid="([^"]*)"/)?.[1];
    if (objectId === undefined) continue;
    const t = (tag.match(/\btransform="([^"]*)"/)?.[1] ?? "1 0 0 0 1 0 0 0 1 0 0 0").trim().split(/\s+/).map(Number);
    const turn = (Math.atan2(t[1] ?? 0, t[0] ?? 1) * 180) / Math.PI;
    out.push({
      objectId,
      name: names.get(objectId) ?? "",
      x: t[9] ?? 0,
      y: t[10] ?? 0,
      turnDeg: Math.abs(turn) < 1e-6 ? 0 : turn,
    });
  }
  return out;
}

/** Read where each object sits on a sliced or arranged `.3mf`. null when either member is missing. */
export async function readPlacements(threemf: string): Promise<Placement[] | null> {
  const model = await readMember(threemf, "3D/3dmodel.model");
  const settings = await readMember(threemf, "Metadata/model_settings.config");
  if (!model || !settings) return null;
  return parsePlacements(model, settings);
}
