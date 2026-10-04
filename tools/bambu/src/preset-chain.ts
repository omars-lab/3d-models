// Flatten a Bambu Studio preset's `inherits` chain into one self-contained JSON.
//
// Why: the Studio command line reads a preset file as-is and does NOT follow `inherits` to the
// parent files (a Bambu maintainer on BambuStudio #6836: "CLI has limited logic to process the
// jsons, we suppose the full json has been generated before when passed to CLI"). Passing only the
// top preset left about 54 process and 50 filament settings at Studio's built-in values on the
// minis-03 and minis-04 slices (docs/research/print-quality-verification.md §1.2). So before
// slicing we walk the chain ourselves and hand the CLI one flattened file per preset.
//
// The merge is the maintainer's own from #6836: child over parent, a shallow key-by-key merge, and
// a list value replaced whole (never merged element by element). `inherits` is dropped from the
// result. A parent that cannot be found is a hard error naming it — never a silent fallback, since
// a silent fallback is exactly the bug this module exists to remove.
//
// PURE core (`flattenPreset` takes a lookup function), so the tests run on a fixture chain with no
// Studio install. `studioPresetLookup` is the real lookup over the app's bundled profiles.

import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";

export type PresetConfig = Record<string, unknown>;

/** Finds the file that defines preset `name` (of Studio `type` "process" | "filament" | "machine"). */
export type PresetLookup = (name: string, type: string) => string | null;

export interface FlattenedPreset {
  /** The leaf file the chain started from. */
  leaf: string;
  /** The leaf's `type` ("process", "filament", "machine"). */
  type: string;
  /** Preset names from the leaf down to the root, e.g. ["0.20mm Standard @BBL X2D", …, "fdm_process_common"]. */
  chain: string[];
  /** The merged settings, `inherits` removed. */
  config: PresetConfig;
  /** The file it was written to, once written: a preset listed twice (one filament in two slots) gets
   *  two files, so coloring one slot cannot rewrite the other. */
  out?: string;
}

function readPreset(path: string): PresetConfig {
  let parsed: unknown;
  try {
    parsed = JSON.parse(readFileSync(path, "utf8"));
  } catch (err) {
    throw new Error(`preset file ${path} is not readable JSON: ${(err as Error).message}`);
  }
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error(`preset file ${path} is not a JSON object`);
  }
  return parsed as PresetConfig;
}

/** Names listed in a preset's `include` key (a string or a list of strings). */
function includesOf(cfg: PresetConfig): string[] {
  const inc = cfg.include;
  if (typeof inc === "string" && inc.trim()) return [inc.trim()];
  if (Array.isArray(inc)) return inc.filter((e): e is string => typeof e === "string" && e.trim() !== "");
  return [];
}

/** Keys that name or describe a preset file; an include template never lends these to the preset. */
const INCLUDE_SKIP = new Set(["name", "inherits", "include", "from", "setting_id", "filament_id", "instantiation", "type", "description"]);

/** The `inherits` chain of one preset, leaf first, each level's raw JSON. Throws on a gap or a loop. */
function walkChain(
  leaf: PresetConfig,
  leafName: string,
  type: string,
  lookup: PresetLookup,
  from: string,
): { names: string[]; levels: PresetConfig[] } {
  const names = [leafName];
  const levels = [leaf];
  let current = leaf;
  while (typeof current.inherits === "string" && current.inherits.trim() !== "") {
    const parentName = current.inherits.trim();
    if (names.includes(parentName)) {
      throw new Error(`preset chain loops: ${[...names, parentName].join(" → ")}`);
    }
    const parentPath = lookup(parentName, type);
    if (!parentPath) {
      throw new Error(
        `missing parent preset "${parentName}" (inherited by "${names[names.length - 1]}", chain from ` +
          `${from}). Refusing to slice: without it every setting it carries would fall back to ` +
          `Studio's built-in value.`,
      );
    }
    current = readPreset(parentPath);
    names.push(parentName);
    levels.push(current);
  }
  return { names, levels };
}

/**
 * Walk `leafPath`'s `inherits` chain to the root and merge child over parent. Each level is laid on
 * in Studio's own order (PresetBundle.cpp, `load_vendor_configs_from_json`): the parent's merged
 * settings, then each `include` template the level names (itself flattened, since a template may
 * inherit too), then the level's own keys. Throws when a parent or an include is missing, naming
 * it and the preset that asked for it, or when the chain loops.
 */
export function flattenPreset(leafPath: string, lookup: PresetLookup, depth = 0): FlattenedPreset {
  if (depth > 8) throw new Error(`preset includes nest too deep at ${leafPath}`);
  const leaf = readPreset(leafPath);
  const type = typeof leaf.type === "string" ? leaf.type : "";
  const leafName = typeof leaf.name === "string" ? leaf.name : basename(leafPath, ".json");
  const { names, levels } = walkChain(leaf, leafName, type, lookup, leafPath);
  // Root first, then each child on top: child keys win, a list is replaced whole.
  const config: PresetConfig = {};
  for (const [i, level] of [...levels.entries()].reverse()) {
    for (const inc of includesOf(level)) {
      const incPath = lookup(inc, type);
      if (!incPath) {
        throw new Error(
          `missing include "${inc}" (named by "${names[i] ?? leafName}", chain from ${leafPath}). Refusing to ` +
            `slice: the settings it carries would fall back to Studio's built-in values.`,
        );
      }
      const incCfg = flattenPreset(incPath, lookup, depth + 1).config;
      for (const [k, v] of Object.entries(incCfg)) if (!INCLUDE_SKIP.has(k)) config[k] = v;
    }
    for (const [k, v] of Object.entries(level)) config[k] = v;
  }
  delete config.inherits;
  delete config.include;
  return { leaf: leafPath, type, chain: names, config };
}

/** Write the flattened preset to the file it was written to before, else `outDir/<leaf basename>`,
 *  and return that path. */
export function writeFlattened(flat: FlattenedPreset, outDir: string): string {
  const out = flat.out ?? join(outDir, basename(flat.leaf));
  writeFileSync(out, JSON.stringify(flat.config, null, 2) + "\n");
  flat.out = out;
  return out;
}

/**
 * Flatten every preset in a ';'-joined list of JSON paths and write each to `outDir`. Returns the
 * new ';'-joined list (the paths to hand `--load-settings` / `--load-filaments`) and the flattened
 * presets, which `compareSliceToPresets` checks the slice against afterwards. A preset with no
 * `inherits` and no `include` is still rewritten, so the files the CLI reads are always ours.
 */
export function flattenPresetList(
  list: string,
  lookup: PresetLookup,
  outDir: string,
): { list: string; presets: FlattenedPreset[] } {
  const presets: FlattenedPreset[] = [];
  const used = new Set<string>();
  const paths = list
    .split(";")
    .map((t) => t.trim())
    .filter(Boolean)
    .map((p) => {
      const flat = flattenPreset(p, lookup);
      // The second slot of one filament: "<name> #2.json", so each slot keeps its own color.
      const name = basename(p, ".json");
      let file = `${name}.json`;
      for (let n = 2; used.has(file); n++) file = `${name} #${n}.json`;
      used.add(file);
      flat.out = join(outDir, file);
      presets.push(flat);
      return writeFlattened(flat, outDir);
    });
  return { list: paths.join(";"), presets };
}

interface VendorIndexEntry {
  name?: string;
  sub_path?: string;
}

/**
 * The real lookup: Studio's bundled profiles root (`<app>/Contents/Resources/profiles`). Each vendor
 * has an index `<root>/<Vendor>.json` listing every preset by name with its `sub_path`, which is how
 * Studio itself finds a parent. BBL is searched first (the X2D is a Bambu Lab machine), then the
 * other vendors. Within a vendor the index list matching the child's `type` is tried first.
 */
export function studioPresetLookup(profilesRoot: string): PresetLookup {
  const vendors = readdirSync(profilesRoot, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);
  const ordered = ["BBL", ...vendors.filter((v) => v !== "BBL")].filter((v) => vendors.includes(v));
  const indexes = new Map<string, Record<string, VendorIndexEntry[]>>();
  const indexFor = (vendor: string): Record<string, VendorIndexEntry[]> => {
    let idx = indexes.get(vendor);
    if (!idx) {
      const file = join(profilesRoot, `${vendor}.json`);
      idx = existsSync(file) ? (JSON.parse(readFileSync(file, "utf8")) as Record<string, VendorIndexEntry[]>) : {};
      indexes.set(vendor, idx);
    }
    return idx;
  };
  return (name, type) => {
    const lists = [`${type}_list`, "process_list", "filament_list", "machine_list"];
    for (const vendor of ordered) {
      const idx = indexFor(vendor);
      for (const list of lists) {
        const entries = idx[list];
        if (!Array.isArray(entries)) continue;
        const hit = entries.find((e) => e.name === name && typeof e.sub_path === "string");
        if (hit) {
          const p = join(profilesRoot, vendor, hit.sub_path!);
          if (existsSync(p)) return p;
        }
      }
      if (type) {
        const direct = join(profilesRoot, vendor, type, `${name}.json`);
        if (existsSync(direct)) return direct;
      }
    }
    return null;
  };
}

// ── The check: did the slice carry the chain? ────────────────────────────────────────────────────

/**
 * Keys a preset file carries that describe the preset itself rather than set a slicing value, so
 * the slice's project settings legitimately hold something else (the project's own name, a
 * per-filament list of ids, and so on). Every other key the flattened chain sets is compared.
 */
export const PRESET_META_KEYS = new Set([
  "name",
  "inherits",
  "from",
  "setting_id",
  "filament_id",
  "instantiation",
  "description",
  "type",
  "version",
  "is_custom_defined",
  "compatible_printers",
  "compatible_printers_condition",
  "compatible_prints",
  "compatible_prints_condition",
  "renamed_from",
  // A preset file leaves these empty; the slice fills them with the preset's own name.
  "print_settings_id",
  "printer_settings_id",
  "filament_settings_id",
]);

export interface SettingMismatch {
  preset: string; // the leaf preset's name
  key: string;
  expected: unknown;
  actual: unknown; // undefined when the slice does not carry the key at all
}

/**
 * Filament keys whose preset value is a list but which Studio 02.08.02.61 stores as ONE value per
 * filament in the project, taking the list's first element. Measured on the minis-04 re-slice from
 * flattened presets, 2026-09-26: each held exactly the chain's first element. Kept as a named list,
 * not a general "a list may collapse to its head" rule, so a new collapse on a new Studio build
 * fails loudly and gets looked at.
 */
export const COLLAPSED_TO_FIRST = new Set([
  "filament_dev_ams_drying_ams_limitations",
  "filament_dev_ams_drying_temperature",
  "filament_dev_ams_drying_time",
]);

/** One scalar as Studio would print it back: trimmed, "AxB" points as "A,B", numbers by value. */
function scalar(v: unknown): string {
  const s = String(v).trim().replace(/^(-?[\d.]+)x(-?[\d.]+)$/, "$1,$2");
  // A number and the same number with a trailing % are one value: Studio writes a percent option
  // back with its sign ("100" → "100%", "45.0" → "45%") and drops a trailing ".0".
  const m = s.match(/^(-?\d+(?:\.\d+)?)%?$/);
  return m ? String(Number(m[1])) : s;
}

const isNil = (v: unknown): boolean =>
  v === "nil" || (Array.isArray(v) && v.length > 0 && v.every((e) => String(e) === "nil"));

/** Does the slice's value carry the preset's? Lists compare element by element; a scalar the slice
 *  expands to a list must hold in every element. */
function carries(key: string, expected: unknown, actual: unknown): boolean {
  const exp = Array.isArray(expected) ? expected.map(scalar) : [scalar(expected)];
  const act = Array.isArray(actual) ? actual.map(scalar) : [scalar(actual)];
  if (exp.length === act.length) return exp.every((e, i) => e === act[i]);
  if (exp.length === 1) return act.every((a) => a === exp[0]);
  if (act.length === 1 && COLLAPSED_TO_FIRST.has(key)) return act[0] === exp[0];
  return false;
}

/** The one-filament view of a per-filament project list: slot `slot` of `width` equal parts. */
function filamentSlot(actual: unknown, slot: number, width: number): unknown {
  if (!Array.isArray(actual)) return actual;
  if (width <= 1 || actual.length % width !== 0) return actual;
  const per = actual.length / width;
  return actual.slice(slot * per, slot * per + per);
}

export interface SliceComparison {
  /** Keys whose value in the slice is not the chain's. Any one is a failure. */
  mismatches: SettingMismatch[];
  /** Keys the chain sets that the slice does not carry at all: names this Studio build does not
   *  know (renamed or retired options, e.g. `wall_infill_order`, now `wall_sequence`). A built-in
   *  fallback always writes the key, so absence is not a fallback; it is reported, not failed. */
  notInSlice: string[];
}

/**
 * Compare every key each flattened preset sets against the slice's
 * `Metadata/project_settings.config`, skipping the preset-describing keys in `PRESET_META_KEYS` and
 * the "nil" placeholders (a filament's "use the process value"). Process and machine presets
 * compare key for key. A filament preset is one slot of the project's per-filament lists: with n
 * filament presets loaded in order, filament i's value is part i of the project list.
 */
export function compareSliceToPresets(projectSettings: PresetConfig, presets: FlattenedPreset[]): SliceComparison {
  const mismatches: SettingMismatch[] = [];
  const notInSlice: string[] = [];
  const filaments = presets.filter((p) => p.type === "filament");
  for (const p of presets) {
    const name = typeof p.config.name === "string" ? p.config.name : (p.chain[0] ?? "");
    const slot = p.type === "filament" ? filaments.indexOf(p) : -1;
    for (const [key, expected] of Object.entries(p.config)) {
      if (PRESET_META_KEYS.has(key) || isNil(expected)) continue;
      if (!(key in projectSettings)) {
        if (!notInSlice.includes(key)) notInSlice.push(key);
        continue;
      }
      let actual = projectSettings[key];
      if (slot >= 0) actual = filamentSlot(actual, slot, filaments.length);
      if (!carries(key, expected, actual)) mismatches.push({ preset: name, key, expected, actual });
    }
  }
  return { mismatches, notInSlice };
}

/** One human line per mismatch, naming the key. */
export function formatMismatch(m: SettingMismatch): string {
  const show = (v: unknown) => (v === undefined ? "(absent)" : Array.isArray(v) && v.length === 1 ? String(v[0]) : JSON.stringify(v));
  return `${m.preset}: ${m.key} is ${show(m.actual)} in the slice, preset chain sets ${show(m.expected)}`;
}
