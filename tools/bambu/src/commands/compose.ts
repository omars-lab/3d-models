// `bambu slice compose <plate.yaml>` — many rendered pieces onto one X2D plate.
//
// A subverb of the `slice` command group (sibling to `slice plate`/`slice open`). It reads a manifest
// of items, renders each variant through bikar (once, cached), runs a bed-fit pre-check, then hands ALL
// the STLs to the Bambu Studio CLI in one `--arrange 1 --export-3mf` invocation — one composed plate.
// It is NOT a new CLI or top-level command; it reuses `slice.ts`'s preset resolver and flattener,
// the check that the slice carried the flattened presets, the argv builder and warnings sidecar, and the `records.ts` scaffolder. Full spec: docs/design/printing/plate-composer-design.md.
//
// The one genuinely new idea (D-072): a manifest item is not an identity — it is the GEOMETRY HALF of
// an iteration key, completed by the plate's one slice profile and resolved to `it-<sha12>` (src/
// iteration.ts). The composer writes that id into the plate record's objects[].iteration; the manifest
// mints no parallel id, so nothing forks (CLAUDE.md "a migration never buys a fork", D-052).

import { Command } from "commander";
import { existsSync, readFileSync, writeFileSync, mkdtempSync, mkdirSync, statSync, readdirSync, copyFileSync, realpathSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join, resolve } from "node:path";
import { parse as parseYaml } from "yaml";
import { runWithTimeout, ev } from "../log.js";
import { surveyBackends, preferenceFor } from "../backends/router.js";
import { locateStudio } from "../backends/studio-cli.js";
import { locateBikarCli, bikarDir, bikarHead, bikarBlobSha, bikarRefOnMain } from "../backends/bikar.js";
import {
  parseSlicerWarnings,
  classifyWarnings,
  loadManifest,
  studioVersionFrom,
  sidecarPath,
  hashFile,
  type WarningsSidecar,
} from "../backends/warnings.js";
import { prepareSlicePresets, enforceSliceCarriesPresets, buildStudioArgs, filamentCount } from "./slice.js";
import { resolveSlicePlateType, studioSavedPlateType } from "../plate-type.js";
import type { FlattenedPreset } from "../preset-chain.js";
import { iterationId, type IterationKey } from "../iteration.js";
import { stlBounds, footprint, scaledCenteredStl } from "../mesh.js";
import { scaffoldRecord, type ScaffoldObject } from "../records.js";
import { recordProfileFrom } from "../header.js";
import { platesDir, recordsDir, repoRoot } from "../paths.js";
import { recipeHashOf, recipeIterationOf } from "../send-gate.js";
import { writePlatePreview, readBeds, readPlacements, type Placement, type SlicedBed } from "../threemf.js";

// ── The manifest ─────────────────────────────────────────────────────────────────────────────────
// A small hand-authorable file. Two item spellings resolve to the SAME iteration id (§3):
//   - {bkr, piece, params, count} — the geometry half, completed by the plate profile.
//   - {iteration, count}          — an already-known it-<sha12> (reprint-by-id; see resolveItem).
// A third renders nothing: {stl, sha256, scale, count} — a mesh file inside this repo, pinned by its
// hash like a sampler sheet's vendored cell, so a model bikar did not make can share a plate. Its file
// may be gitignored (`.bambu/imports/`): a third-party model whose license does not allow sharing it
// stays out of this public repo, and the hash still refuses a different file under the same name.

export interface PlateProfile {
  settings?: string; // "<machine>;<process>" preset display names (-s)
  filament?: string; // filament preset display name(s) (-f), ';'-joined: one per filament slot
  // "#RRGGBB", or a list with one per filament slot: the color(s) the slice carries, so the send
  // matches each slot to its tray (default: each preset's own)
  color?: string | string[];
}
export interface ManifestItemBkr {
  bkr: string; // "bikar:<path>" source
  piece?: string; // a NAMED piece/tile/clip to render; omit to render the file's default last solid
  params?: Record<string, number>; // --param overrides (bikar --param takes numbers)
  window?: string; // `--window <side>[@x,y]`: a square sample cut at the coaster's own scale (bikar #293)
  count?: number; // copies on the plate (default 1)
  label?: string; // what the person at the printer calls it ("GAP 05"); names it in the bed map, never in the id
  filament?: number; // the 1-based filament slot it prints in; needed on every item when the plate has two or more
  id?: string; // the piece's one-character id, cut into its bed face after the plate's id_code and iteration (D-109)
  no_id?: string; // why it carries no id, and how it is kept apart instead (a piece too small, one printed face down)
}
export interface ManifestItemIteration {
  iteration: string; // an already-known it-<sha12>
  count?: number;
  label?: string;
  filament?: number;
  no_id?: string; // a reprint by id re-renders a frozen key, so it cannot take a new id: say why it has none
}
export interface ManifestItemStl {
  stl: string; // repo-relative path of a mesh file (may be gitignored, e.g. .bambu/imports/<name>.stl)
  sha256: string; // the file's sha256: a different file under the same path is refused
  scale?: number | [number, number, number]; // one scale, or one per axis [x, y, z] (default 1)
  count?: number;
  label?: string;
  filament?: number;
  no_id?: string; // a file bikar did not make cannot be cut: say why it has none
}
export type ManifestItem = ManifestItemBkr | ManifestItemIteration | ManifestItemStl;
export interface PlateManifest {
  bed?: string; // bed footprint name (default x2d)
  beds?: number; // the most beds the arrange may use (default 1); a spill past it is refused
  profile?: PlateProfile; // the ONE slice profile the plate is sliced under
  id_code?: string; // the plate's 1-3 character code, the first line of every piece's carved id (D-109)
  items: ManifestItem[];
}

function isIterationItem(it: ManifestItem): it is ManifestItemIteration {
  return typeof (it as ManifestItemIteration).iteration === "string";
}

function isStlItem(it: ManifestItem): it is ManifestItemStl {
  return typeof (it as ManifestItemStl).stl === "string";
}

/** Check a local-file item's own fields. Same path and hash rules as a sheet's vendored cell. */
function checkStlItem(it: Record<string, unknown>, where: string): void {
  const p = it.stl;
  if (typeof p !== "string" || !p.trim() || p.startsWith("/") || p.split("/").includes("..")) {
    throw new Error(`${where}: \`stl:\` must be a path inside this repo, e.g. .bambu/imports/<name>.stl`);
  }
  for (const k of ["bkr", "piece", "params", "window", "iteration"]) {
    if (it[k] !== undefined) throw new Error(`${where}: an \`stl:\` item cannot also carry \`${k}:\` — it renders nothing`);
  }
  if (typeof it.sha256 !== "string" || !/^[0-9a-f]{64}$/.test(it.sha256)) {
    throw new Error(`${where}: an \`stl:\` item needs \`sha256:\` (64 lowercase hex) so a changed file is refused`);
  }
  const s = it.scale;
  const ok = (k: unknown) => typeof k === "number" && Number.isFinite(k) && k > 0;
  if (s !== undefined && !ok(s) && !(Array.isArray(s) && s.length === 3 && s.every(ok))) {
    throw new Error(`${where}: \`scale:\` must be a number > 0, or [x, y, z] of them, got ${JSON.stringify(s)}`);
  }
}

/** An `stl:` item's scale as iteration params: none at 1, `scale` when every axis is the same (so a
 *  uniform scale keeps the id it had before scales per axis existed), else `scale_x/_y/_z`. */
export function stlScaleParams(scale: ManifestItemStl["scale"]): Record<string, number> {
  const [x, y, z] = typeof scale === "number" ? [scale, scale, scale] : (scale ?? [1, 1, 1]);
  if (x === y && y === z) return x === 1 ? {} : { scale: x };
  return { scale_x: x, scale_y: y, scale_z: z };
}

/** The scale a resolved `stl:` item's copy is made at, read back from its params. */
function stlScaleOf(params: Record<string, number>): number | [number, number, number] {
  if (params.scale_x === undefined) return params.scale ?? 1;
  return [params.scale_x, params.scale_y ?? 1, params.scale_z ?? 1];
}

/** A parsed `--window` value: the square's side and its centre in the coaster's own frame. */
export interface WindowSpec {
  side: number;
  x: number;
  y: number;
}

/** Parse bikar's `<side>[@<x>,<y>]` window spelling (the centre defaults to the coaster's origin), or
 *  return null when the text is not one. A YAML `window: 30` arrives as a number; the caller passes
 *  `String(v)`. */
export function parseWindow(text: string): WindowSpec | null {
  const m = /^(\d+(?:\.\d+)?)(?:@(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?))?$/.exec(text.trim());
  if (!m) return null;
  const side = Number(m[1]);
  if (!(side > 0)) return null;
  return { side, x: m[2] === undefined ? 0 : Number(m[2]), y: m[3] === undefined ? 0 : Number(m[3]) };
}

/** The bikar flags that pick WHAT an item renders — its piece, params, window and carved id — shared by
 *  every verb that renders a resolved item, so a window can never reach one verb's render and miss another's. */
export function itemRenderFlags(r: {
  piece: string;
  params: Record<string, number>;
  window: string;
  bottomId?: string;
}): string[] {
  const out: string[] = [];
  if (r.piece) out.push("--piece", r.piece);
  for (const [k, v] of Object.entries(r.params)) out.push("--param", `${k}=${v}`);
  if (r.window) out.push("--window", r.window);
  if (r.bottomId) out.push("--bottom-id", r.bottomId);
  return out;
}

// ── The carved id (D-109) ────────────────────────────────────────────────────────────────────────
// Every experimental piece carries its plate, the recipe's iteration and its own id, cut into the face
// that sits on the bed. bikar cuts it (`--bottom-id`, bikar #330) in two lines of at most three
// characters: the plate's code, then the iteration and the piece's id — `SP1/2 D` is plate SP1,
// iteration 2, piece D. The iteration is not written in the recipe: it is the one the manage-approvals
// store records for the recipe as it is (`recipeIterationOf`), so an edit can never print last
// iteration's number. bikar cuts 0-9, A-Z, `-` and space and refuses an id holding both 0 and O; the
// letter O is left out here altogether, so a code and a piece id never have to be read apart from a zero.

/** One character of an id code or piece id: a digit or a capital letter other than O. */
const ID_CHAR = "[0-9A-NP-Z]";
const ID_CODE = new RegExp(`^${ID_CHAR}{1,3}$`);
const PIECE_ID = new RegExp(`^${ID_CHAR}$`);

/** The text bikar cuts: `<code>/<iteration> <id>`. Throws when the iteration does not fit its one
 *  digit, since a line of four characters is past what bikar cuts at a size that prints. */
export function bottomIdText(code: string, iteration: number, id: string): string {
  if (!Number.isInteger(iteration) || iteration < 1 || iteration > 9) {
    throw new Error(
      `iteration ${iteration} does not fit the carved id's one digit (1 to 9): ` +
        "start a new plate with its own id_code for the next round of this experiment",
    );
  }
  return `${code}/${iteration} ${id}`;
}

/** The repo whose approvals store numbers an id_code recipe: the one the recipe file sits in, as the
 *  recipe beside its page. The store is read by plate name, so a recipe run from another checkout, or a
 *  copy kept elsewhere, would otherwise be cut with an iteration that is not its own — compose did that
 *  on 2026-10-08, cutting `SL1/2` into spl-1's iteration 3 from the shell's other checkout. */
export function idRecipeRoot(absManifest: string): string {
  const root = repoRoot(dirname(absManifest));
  const name = basename(absManifest).replace(/\.ya?ml$/i, "");
  const beside = root ? join(root, "docs", "design", "plates", `${name}.yaml`) : null;
  if (!root || !beside || !existsSync(beside) || realpathSync(beside) !== realpathSync(absManifest)) {
    throw new Error(
      `${absManifest} has an \`id_code:\`, so it must be a plate's recipe in docs/design/plates, beside its ` +
        "page: the iteration cut into each piece is that recipe's (D-109). Move it there, or drop `id_code:`",
    );
  }
  return root;
}

/** Check the recipe's `id_code:` and each item's `id:` / `no_id:`. A recipe with an id_code gives every
 *  item one or the other; a recipe without one may not give any item an `id:`. Ids are unique. */
function checkIds(m: Record<string, unknown>, items: Record<string, unknown>[]): void {
  const code = m.id_code;
  if (code !== undefined && (typeof code !== "string" || !ID_CODE.test(code))) {
    throw new Error(
      `\`id_code:\` must be 1 to 3 of 0-9 and A-Z without the letter O (cut into every piece), got ${JSON.stringify(code)}`,
    );
  }
  const ids = new Set<string>();
  items.forEach((it, i) => {
    const where = `items[${i}]`;
    if (it.no_id !== undefined && (typeof it.no_id !== "string" || !it.no_id.trim())) {
      throw new Error(`${where}: \`no_id:\` must say why the piece has no id and how it is kept apart instead`);
    }
    if (it.id !== undefined) {
      if (it.no_id !== undefined) throw new Error(`${where}: an item has \`id:\` or \`no_id:\`, not both`);
      if (typeof it.bkr !== "string") {
        throw new Error(
          `${where}: only a \`bkr:\` item can be cut — an \`iteration:\` item re-renders a frozen key and an ` +
            "`stl:` item renders nothing; give it `no_id:` instead",
        );
      }
      if (code === undefined) throw new Error(`${where}: \`id:\` needs the recipe's \`id_code:\`, the first line of the id`);
      const id = typeof it.id === "number" ? String(it.id) : it.id; // a YAML `id: 7` is a number
      if (typeof id !== "string" || !PIECE_ID.test(id)) {
        throw new Error(`${where}: \`id:\` must be one of 0-9 and A-Z without the letter O, got ${JSON.stringify(it.id)}`);
      }
      if (ids.has(id)) throw new Error(`${where}: \`id: ${id}\` is already another item's — two pieces with one id cannot be told apart`);
      ids.add(id);
      it.id = id;
    } else if (code !== undefined && it.no_id === undefined) {
      throw new Error(
        `${where}: the recipe has an id_code, so every item needs \`id:\` (its one character) or \`no_id:\` ` +
          "(why it has none and how it is kept apart instead)",
      );
    }
  });
}

/** Parse + validate a plate manifest. Throws a clear, actionable error (naming the offending item)
 *  rather than letting a malformed manifest reach the renderer or slicer. */
export function parseManifest(text: string): PlateManifest {
  let doc: unknown;
  try {
    doc = parseYaml(text);
  } catch (err) {
    throw new Error(`plate manifest is not valid YAML: ${(err as Error).message}`);
  }
  if (!doc || typeof doc !== "object") throw new Error("plate manifest is empty or not a mapping");
  const m = doc as Record<string, unknown>;
  const items = m.items;
  if (!Array.isArray(items) || items.length === 0) {
    throw new Error("plate manifest has no `items:` — a plate with nothing to compose");
  }
  const labels = new Set<string>();
  items.forEach((raw, i) => {
    if (!raw || typeof raw !== "object") throw new Error(`items[${i}] is not a mapping`);
    const it = raw as Record<string, unknown>;
    const where = `items[${i}]`;
    if (it.stl !== undefined) {
      checkStlItem(it, where);
    } else if (typeof it.iteration === "string") {
      if (it.bkr || it.piece) throw new Error(`${where}: an \`iteration:\` item cannot also carry bkr/piece`);
    } else {
      if (typeof it.bkr !== "string" || !it.bkr.startsWith("bikar:")) {
        throw new Error(`${where}: \`bkr:\` must be a "bikar:<path>" string (or use \`iteration:\` or \`stl:\`)`);
      }
      if (it.piece !== undefined && (typeof it.piece !== "string" || !it.piece)) {
        throw new Error(`${where}: \`piece:\` must be a non-empty string (a named piece/tile/clip); omit it to render the file's default solid`);
      }
      if (it.window !== undefined) {
        if ((typeof it.window !== "string" && typeof it.window !== "number") || !parseWindow(String(it.window))) {
          throw new Error(`${where}: \`window:\` must be bikar's "<side>[@<x>,<y>]" (e.g. 30@9.7,1), got ${JSON.stringify(it.window)}`);
        }
        it.window = String(it.window); // a YAML `window: 30` is a number; the key and the flag want text
      }
      if (it.params !== undefined) {
        if (typeof it.params !== "object" || it.params === null || Array.isArray(it.params)) {
          throw new Error(`${where}: \`params:\` must be a mapping of name → number`);
        }
        for (const [k, v] of Object.entries(it.params as Record<string, unknown>)) {
          if (typeof v !== "number" || !Number.isFinite(v)) {
            throw new Error(`${where}: param \`${k}\` must be a number (bikar --param takes numbers), got ${JSON.stringify(v)}`);
          }
        }
      }
    }
    if (it.count !== undefined) {
      if (typeof it.count !== "number" || !Number.isInteger(it.count) || it.count < 1) {
        throw new Error(`${where}: \`count:\` must be an integer >= 1, got ${JSON.stringify(it.count)}`);
      }
    }
    if (it.label !== undefined) {
      if (typeof it.label !== "string" || !it.label.trim()) {
        throw new Error(`${where}: \`label:\` must be a non-empty string (what the bag and the bed map call it)`);
      }
      if (labels.has(it.label)) {
        throw new Error(`${where}: \`label: ${it.label}\` is already used by another item — two sets with one name cannot be told apart`);
      }
      labels.add(it.label);
    }
  });
  checkIds(m, items as Record<string, unknown>[]);
  if (m.beds !== undefined && (typeof m.beds !== "number" || !Number.isInteger(m.beds) || m.beds < 1)) {
    throw new Error(`\`beds:\` must be an integer >= 1 (the most beds the plate may use), got ${JSON.stringify(m.beds)}`);
  }
  const color = (m.profile as PlateProfile | undefined)?.color;
  const isHex = (c: unknown) => typeof c === "string" && /^#[0-9A-Fa-f]{6}$/.test(c);
  if (color !== undefined && !(Array.isArray(color) ? color.length > 0 && color.every(isHex) : isHex(color))) {
    throw new Error(
      `\`profile.color:\` must be "#RRGGBB" (the loaded tray's color), or a list of them with one per filament, got ${JSON.stringify(color)}`,
    );
  }
  const filament = (m.profile as PlateProfile | undefined)?.filament;
  if (typeof filament === "string") checkItemFilaments(items as ManifestItem[], filamentCount(filament));
  return {
    bed: typeof m.bed === "string" ? m.bed : undefined,
    beds: typeof m.beds === "number" ? m.beds : undefined,
    profile: (m.profile as PlateProfile) ?? undefined,
    ...(typeof m.id_code === "string" ? { id_code: m.id_code } : {}),
    items: items as ManifestItem[],
  };
}

/** Each item's `filament:` slot against the plate's filament count. One filament: the field may be
 *  left out (slot 1). Two or more: every item names its slot, since a plate where an item silently
 *  takes slot 1 prints it in the wrong color. Throws naming the item. */
export function checkItemFilaments(items: ManifestItem[], count: number): void {
  items.forEach((it, i) => {
    const f = it.filament;
    if (f === undefined) {
      if (count > 1) {
        throw new Error(`items[${i}]: the plate has ${count} filaments, so every item needs \`filament:\` (its slot, 1 to ${count})`);
      }
      return;
    }
    if (typeof f !== "number" || !Number.isInteger(f) || f < 1 || f > Math.max(count, 1)) {
      throw new Error(`items[${i}]: \`filament:\` must be a slot from 1 to ${Math.max(count, 1)}, got ${JSON.stringify(f)}`);
    }
  });
}

/** The name an item's mesh is handed to the slicer under, which the arranged object keeps: the bed
 *  map joins objects back to items by it. Slot 1 keeps `<iteration>.stl`, so one-color plates are
 *  unchanged; another slot adds `-f<slot>`, since two colors of one piece share an iteration id. */
export function stagedName(r: { iteration: string; filament: number }): string {
  return r.filament > 1 ? `${r.iteration}-f${r.filament}.stl` : `${r.iteration}.stl`;
}

// ── The bed and the fit pre-check (§6) ──────────────────────────────────────────────────────────
// **Default:** the x2d bed footprint is 256 × 256 mm — the X2D single-nozzle build area (D-053; the
// K1 note in docs/design/printing/plate-composer-design.md §6 carries the dual-nozzle narrowing to 235.5 mm). The
// pre-check is a NECESSARY condition only: it never claims a plate tiles — that is --arrange's job.

export interface Bed {
  name: string;
  x: number; // mm
  y: number; // mm
  label: string;
}
export const BEDS: Record<string, Bed> = {
  x2d: { name: "x2d", x: 256, y: 256, label: "X2D single-nozzle build area 256×256 mm (D-053)" },
};
export function resolveBed(name: string): Bed {
  const bed = BEDS[name.toLowerCase()];
  if (!bed) throw new Error(`unknown --bed "${name}". Known beds: ${Object.keys(BEDS).join(", ")}`);
  return bed;
}

export interface PartFootprint {
  entry: string;
  x: number; // footprint width (mm)
  y: number; // footprint depth (mm)
  count: number;
}
export interface PrecheckResult {
  ok: boolean;
  failures: string[];
}
/** Bed-fit pre-check, in two parts (§6): (i) per-part — every single part's footprint bbox fits the
 *  bed rectangle; (ii) aggregate — summed footprint area × count ≤ bed area. Both are necessary, not
 *  sufficient: an aggregate area check CANNOT discharge the per-part claim (K6/D2), so the per-part
 *  check is the one that catches the hard case (one oversized part on an otherwise near-empty plate). */
export function bedFitPrecheck(parts: PartFootprint[], bed: Bed): PrecheckResult {
  const failures: string[] = [];
  // (i) per-part fit — the load-bearing check.
  for (const p of parts) {
    if (p.x > bed.x || p.y > bed.y) {
      failures.push(
        `${p.entry}: footprint ${p.x.toFixed(1)}×${p.y.toFixed(1)} mm does not fit the ${bed.name} bed ` +
          `(${bed.x}×${bed.y} mm) — no arrangement can place it.`,
      );
    }
  }
  // (ii) aggregate area — a coarse necessary condition; the slicer's --arrange is the tiling authority.
  const bedArea = bed.x * bed.y;
  const usedArea = parts.reduce((sum, p) => sum + p.x * p.y * p.count, 0);
  if (usedArea > bedArea) {
    failures.push(
      `total footprint area ${Math.round(usedArea)} mm² exceeds the ${bed.name} bed area ${bedArea} mm² ` +
        `— even a perfect packing cannot fit these ${parts.reduce((n, p) => n + p.count, 0)} parts.`,
    );
  }
  return { ok: failures.length === 0, failures };
}

// ── The verb ─────────────────────────────────────────────────────────────────────────────────────

/**
 * The items `--arrange` put past the allowed beds. Studio opens a second bed when the first is full
 * and `print send` runs one bed, so a spill is items that silently never print (minis-05: 12 objects
 * sliced as 11 + 1). PURE: beds from the slice, the STL basename each entry was handed in under
 * (`<iteration>.stl`), and the limit. [] when the plate fits.
 */
export function spilledItems(beds: SlicedBed[], entryByStl: Map<string, string[]>, maxBeds: number): string[] {
  return beds
    .filter((b) => b.index > maxBeds)
    .flatMap((b) => b.objects.map((o) => `${(entryByStl.get(o) ?? [o]).join(" / ")} (bed ${b.index})`));
}

/** One row of the bed map: which plate item an arranged object is, and where it sits. */
export interface BedMapRow {
  object: string; // the 3MF object id
  entry: string; // c1, c2, … ("" when the object matched no item)
  label: string; // the manifest `label:`, else the entry
  piece: string;
  params: Record<string, number>;
  iteration: string;
  filament: number; // the 1-based filament slot it prints in
  x: number; // centre, bed millimetres from the front-left corner
  y: number;
  turn_deg: number;
}

/**
 * Join the arranged objects back to the plate items, so sets that look alike (sheets-04: four rings of
 * the same hexagons at four gaps) can be told apart on the bed. PURE. An object carries its input
 * file's name (`stagedName`: `<iteration>.stl`, `-f<slot>` past slot 1); an item handed in `count` times, or two items with one recipe, give
 * several objects one name, and those take the items in manifest order — they are the same geometry,
 * so which copy is which does not change what prints. An object no item claims keeps entry "".
 */
export function bedMap(placements: Placement[], resolved: ResolvedItem[]): BedMapRow[] {
  const waiting = new Map<string, ResolvedItem[]>();
  for (const r of resolved) {
    const key = stagedName(r);
    const list = waiting.get(key) ?? [];
    for (let c = 0; c < r.count; c++) list.push(r);
    waiting.set(key, list);
  }
  const entryOrder = (e: string) => Number(e.replace(/^c/, "")) || Number.MAX_SAFE_INTEGER;
  return placements
    .map((p) => {
      const r = waiting.get(p.name)?.shift();
      const round = (v: number) => Math.round(v * 10) / 10;
      return {
        object: p.objectId,
        entry: r?.entry ?? "",
        label: r ? r.label || r.entry : p.name,
        piece: r?.piece ?? "",
        params: r?.params ?? {},
        iteration: r?.iteration ?? p.name.replace(/\.stl$/i, ""),
        filament: r?.filament ?? 1,
        x: round(p.x),
        y: round(p.y),
        turn_deg: round(p.turnDeg),
      };
    })
    .sort((a, b) => entryOrder(a.entry) - entryOrder(b.entry));
}

/** Where the bed map goes: next to the plate, as `<name>.bedmap.json`. */
export function bedMapPathFor(threemf: string): string {
  return threemf.replace(/\.3mf$/i, "") + ".bedmap.json";
}

interface ComposeOpts {
  out?: string;
  outputdir?: string;
  settings?: string;
  filament?: string;
  bed: string;
  arrange: boolean;
  timeout: string;
  dryRun?: boolean;
  strict?: boolean;
  record?: boolean;
  plateType?: string;
}

/** One resolved on-plate item: its geometry pins, the count, and (filled after render) its footprint
 *  and cached STL path. `source` carries the @ref for the iteration key; the record strips it. */
export interface ResolvedItem {
  entry: string; // stable per-item label on the plate (compose orders them c1, c2, …)
  sourcePath: string; // "<path>" (no bikar: prefix, no @ref)
  sourceAtRef: string; // "bikar:<path>@<ref>" for the iteration key
  piece: string;
  params: Record<string, number>;
  window: string; // the `--window` cut, "" for the whole piece
  bottomId: string; // the carved id bikar cuts into its bed face (`SP1/2 D`), "" for none (D-109)
  count: number;
  sourceSha256: string;
  iteration: string; // it-<sha12>
  label: string; // the manifest's `label:`, "" when it has none; not part of the iteration key
  filament: number; // the 1-based filament slot (1 when the item names none)
  file?: string; // an `stl:` item's absolute path: copied (scaled by its scale params) instead of rendered
}

/** Resolve a bikar-tracked blob's source_sha256 at a ref, or throw a clear error. */
async function blobSha(ref: string, path: string): Promise<string> {
  const sha = await bikarBlobSha(ref, path);
  if (!sha) {
    throw new Error(
      `could not read bikar blob for "${path}" at ${ref} — is it committed in bikar (${bikarDir()})? ` +
        `A composed plate pins provenance to a committed source.`,
    );
  }
  return sha;
}

/** Scan the record store (drafts + finished) for the newest record whose objects carry `id`, and
 *  return its geometry (source path + piece + params) so a `{iteration}` manifest item can re-render
 *  the same recipe. This is the reprint-by-id lookup docs/design/printing/plate-composer-design.md §3 defers to; it
 *  reads records only (no re-slice here). Returns null if no record names the id yet. */
export function findIterationGeometry(
  id: string,
  recordDirs: string[],
  readIndex: (dir: string) => string | null,
): { sourcePath: string; piece: string; params: Record<string, number>; window: string } | null {
  const hits: Array<{
    run: string;
    geom: { sourcePath: string; piece: string; params: Record<string, number>; window: string };
  }> = [];
  for (const dir of recordDirs) {
    const text = readIndex(dir);
    if (!text) continue;
    const fm = text.match(/^---\n([\s\S]*?)\n---/);
    if (!fm) continue;
    let data: unknown;
    try {
      data = parseYaml(fm[1] ?? "");
    } catch {
      continue;
    }
    const objs = (data as { objects?: unknown[] })?.objects;
    if (!Array.isArray(objs)) continue;
    for (const o of objs as Array<Record<string, unknown>>) {
      if (o.iteration === id && typeof o.source === "string") {
        const sourcePath = o.source.replace(/^bikar:/, "").split("@")[0] ?? "";
        hits.push({
          run: basename(dir),
          geom: {
            sourcePath,
            piece: String(o.piece ?? ""),
            params: (o.params as Record<string, number>) ?? {},
            window: typeof o.window === "string" ? o.window : "",
          },
        });
      }
    }
  }
  hits.sort((a, b) => (a.run < b.run ? 1 : -1)); // newest run name first (date-prefixed)
  return hits[0]?.geom ?? null;
}

/** An `stl:` item's pins: the file must be there and must hash to the recipe's sha256. Its iteration
 *  key names the file (`3d-models:<path>`, as a sheet's vendored cell is recorded) and its scale, so
 *  the same file at another size is another recipe. */
function resolveStlItem(
  item: ManifestItemStl,
  n: number,
  root: string,
  sliceProfile: { settings: string; filament: string },
): ResolvedItem {
  const where = `items[${n - 1}]`;
  const file = join(root, item.stl);
  if (!existsSync(file)) {
    throw new Error(
      `${where}: no such file ${item.stl} under ${root}. A gitignored import lives in one checkout only: ` +
        `copy it there (its sha256 is in the recipe), or compose from the checkout that has it.`,
    );
  }
  const sha = hashFile(file);
  if (sha !== item.sha256) {
    throw new Error(`${where}: ${item.stl} has sha256 ${sha}, not the ${item.sha256} the recipe was written with`);
  }
  const params = stlScaleParams(item.scale);
  const source = `3d-models:${item.stl}`;
  const key: IterationKey = {
    source,
    source_sha256: item.sha256,
    piece: "",
    params,
    slice_profile: itemSliceProfile(item, sliceProfile),
  };
  return {
    entry: `c${n}`,
    sourcePath: item.stl,
    sourceAtRef: source,
    piece: "",
    params,
    window: "",
    bottomId: "",
    count: item.count ?? 1,
    sourceSha256: item.sha256,
    iteration: iterationId(key),
    label: item.label ?? "",
    filament: item.filament ?? 1,
    file,
  };
}

/** The slice profile that completes one item's iteration key. An item with a `filament:` slot is
 *  printed in that slot's preset, so its key names that preset alone; an item without one keeps the
 *  plate's whole filament string, so every id minted before slots existed stays the same. */
export function itemSliceProfile(
  item: { filament?: number },
  sliceProfile: { settings: string; filament: string },
): { settings: string; filament: string } {
  if (item.filament === undefined) return sliceProfile;
  const slots = sliceProfile.filament
    .split(";")
    .map((t) => t.trim())
    .filter(Boolean);
  const preset = slots[item.filament - 1];
  if (!preset) {
    throw new Error(`filament slot ${item.filament} is past the plate's ${slots.length} filament(s)`);
  }
  return { settings: sliceProfile.settings, filament: preset };
}

/** Resolve every manifest item to its geometry pins + iteration id. D-072: an item is the GEOMETRY
 *  HALF of the key, completed by the plate's one slice profile — the manifest mints no parallel id, so
 *  nothing forks (CLAUDE.md "a migration never buys a fork"). Shared by `slice compose` (loose-STL
 *  plates) and `slice coaster` (multi-part color plates), so both derive the same it-<sha12> for the
 *  same recipe. Throws an item-indexed error; the caller maps it to an exit code. */
export async function resolveManifestItems(
  items: ManifestItem[],
  bikarRef: string,
  sliceProfile: { settings: string; filament: string },
  root: string = repoRoot() ?? process.cwd(),
  ids: { code: string; iteration: number } | null = null, // the plate's id_code and recipe iteration (D-109)
): Promise<ResolvedItem[]> {
  const resolved: ResolvedItem[] = [];
  let n = 0;
  for (const item of items) {
    n += 1;
    if (isStlItem(item)) {
      resolved.push(resolveStlItem(item, n, root, sliceProfile));
      continue;
    }
    let sourcePath: string;
    let piece: string;
    let params: Record<string, number>;
    let window: string;
    if (isIterationItem(item)) {
      const geom = findIterationGeometry(
        item.iteration,
        listRecordDirs(),
        (d) => (existsSync(join(d, "index.md")) ? readFileSync(join(d, "index.md"), "utf8") : null),
      );
      if (!geom) {
        throw new Error(
          `items[${n - 1}]: iteration ${item.iteration} is not in any record yet, so its recipe cannot ` +
            `be re-rendered. Author it as {bkr, piece, params} instead (reprint-by-id needs a record that carries the id).`,
        );
      }
      sourcePath = geom.sourcePath;
      piece = geom.piece;
      params = geom.params;
      window = geom.window;
    } else {
      sourcePath = item.bkr.replace(/^bikar:/, "");
      piece = item.piece ?? ""; // "" ⇒ the file's default last solid (bikar renders it without --piece)
      params = item.params ?? {};
      window = item.window ?? "";
    }
    const id = isIterationItem(item) ? undefined : item.id;
    if (id !== undefined && !ids) {
      throw new Error(
        `items[${n - 1}]: \`id: ${id}\` needs the plate's id_code and iteration, which only \`slice compose\` reads so far (D-109)`,
      );
    }
    const bottomId = id !== undefined && ids ? bottomIdText(ids.code, ids.iteration, id) : "";
    const sourceSha256 = await blobSha(bikarRef, sourcePath);
    const key: IterationKey = {
      source: `bikar:${sourcePath}@${bikarRef}`,
      source_sha256: sourceSha256,
      piece,
      params,
      ...(window ? { window } : {}), // absent unless cut: pre-window ids stay byte-identical
      ...(bottomId ? { bottom_id: bottomId } : {}), // absent unless carved: pre-id ids stay byte-identical
      slice_profile: itemSliceProfile(item, sliceProfile),
    };
    resolved.push({
      entry: `c${n}`,
      sourcePath,
      sourceAtRef: `bikar:${sourcePath}@${bikarRef}`,
      piece,
      params,
      window,
      bottomId,
      count: item.count ?? 1,
      sourceSha256,
      iteration: iterationId(key),
      label: item.label ?? "",
      filament: item.filament ?? 1,
    });
  }
  return resolved;
}

async function runCompose(manifestPath: string, opts: ComposeOpts, raw: string[]): Promise<void> {
  const absManifest = resolve(manifestPath);
  if (!existsSync(absManifest)) {
    console.error(`no such manifest: ${manifestPath}`);
    process.exitCode = 1;
    return;
  }

  // 1. Parse the manifest and resolve the plate profile (CLI -s/-f override the manifest `profile:`).
  let manifest: PlateManifest;
  try {
    manifest = parseManifest(readFileSync(absManifest, "utf8"));
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 2;
    return;
  }
  const settingsName = opts.settings ?? manifest.profile?.settings;
  const filamentName = opts.filament ?? manifest.profile?.filament;
  const bedName = opts.bed ?? manifest.bed ?? "x2d";
  const maxBeds = manifest.beds ?? 1;
  let bed: Bed;
  try {
    bed = resolveBed(bedName);
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 2;
    return;
  }
  if (!settingsName || !filamentName) {
    console.error(
      "a plate needs one slice profile — set `profile.settings` + `profile.filament` in the manifest, " +
        "or pass -s/--settings and -f/--filament. One plate is sliced under one profile (D-072 §3).",
    );
    process.exitCode = 2;
    return;
  }

  // 2. bikar must be available — the composer renders each item's geometry from source.
  const bikarCli = locateBikarCli();
  if (!bikarCli) {
    console.error(`bikar CLI not built at ${bikarDir()}/packages/cli/dist/index.js.`);
    console.error("Build bikar (npm run build there), or set BIKAR_DIR to your checkout.");
    process.exitCode = 1;
    return;
  }
  const bikarRef = await bikarHead();
  if (!bikarRef) {
    console.error(`could not read bikar HEAD at ${bikarDir()} — is it a git checkout?`);
    process.exitCode = 1;
    return;
  }
  // A branch commit is pinned into the plate, then replaced when the branch squash-merges; the
  // record written from this plate would fail the prints gate (R16). Say so now, not at the record.
  const onMain = await bikarRefOnMain(bikarRef);
  if (onMain === "no") {
    console.error(`⚠ bikar HEAD ${bikarRef.slice(0, 12)} is not on origin/main (${bikarDir()}).`);
    console.error("  A plate composed now pins a commit a squash merge will replace, and its print record");
    console.error("  will fail the prints gate (R16). Merge the bikar change, fast-forward, and compose again.");
  } else if (onMain === "unknown") {
    console.error(`⚠ could not tell whether bikar HEAD ${bikarRef.slice(0, 12)} is on origin/main.`);
  }

  // 3. Resolve each manifest item to its geometry pins + iteration id (shared with `slice coaster`).
  const sliceProfile = { settings: settingsName, filament: filamentName };
  const filaments = filamentCount(filamentName);
  let resolved: ResolvedItem[];
  try {
    checkItemFilaments(manifest.items, filaments); // again: -f may have changed the count
    // A plate with an id_code cuts `<code>/<iteration> <id>` into each piece (D-109). The iteration is
    // read from the approvals store, never written in the recipe, so an edit cannot keep an old number.
    let ids: { code: string; iteration: number } | null = null;
    if (manifest.id_code) {
      const name = basename(absManifest).replace(/\.ya?ml$/i, "");
      ids = { code: manifest.id_code, iteration: recipeIterationOf(name, idRecipeRoot(absManifest)) };
    }
    resolved = await resolveManifestItems(manifest.items, bikarRef, sliceProfile, undefined, ids);
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 2;
    return;
  }

  // 4. Render each DISTINCT {source, params, piece} once (cache), collect footprints. The cache key is
  //    the source blob sha + canonical params + piece — which coincides with the iteration key's
  //    geometry half, so cache and id never disagree (§7).
  const scratch = mkdtempSync(join(tmpdir(), "bambu-compose-"));
  const cache = new Map<string, string>(); // cacheKey → rendered STL path
  const footprints = new Map<string, [number, number]>(); // cacheKey → [x, y]
  const renderPlan: string[] = [];
  const cacheKeyOf = (r: ResolvedItem): string =>
    `${r.sourceSha256}:${r.piece}:${JSON.stringify(r.params)}:${r.window}:${r.bottomId}`;
  const pieceLabel = (r: ResolvedItem): string => (r.file ? `file ${basename(r.sourcePath)}` : r.piece ? r.piece : "default solid");
  for (const r of resolved) {
    const ck = cacheKeyOf(r);
    if (cache.has(ck)) {
      renderPlan.push(`  ${r.entry}: cache hit — ${pieceLabel(r)} @ ${JSON.stringify(r.params)} (${r.iteration})`);
      continue;
    }
    const stl = join(scratch, `${r.iteration}.stl`);
    if (r.file) {
      // A local mesh renders nothing: copy it, scaled, under its iteration name so the bed map finds it.
      renderPlan.push(`  ${r.entry}: copy ${pieceLabel(r)} @ ${JSON.stringify(r.params)} → ${r.iteration}`);
      try {
        writeFileSync(stl, scaledCenteredStl(readFileSync(r.file), stlScaleOf(r.params)));
        cache.set(ck, stl);
        footprints.set(ck, footprint(stlBounds(stl)));
      } catch (err) {
        console.error(`${r.entry} (${r.sourcePath}): ${(err as Error).message}`);
        process.exitCode = 1;
        return;
      }
      continue;
    }
    // `--piece` renders a NAMED piece/tile/clip; a plain orb has none, so omit the flag and bikar
    // renders the file's default last solid (its own model — the only way to render a clip is --piece).
    const args = [bikarCli, "render", resolve(bikarDir(), r.sourcePath), "--format", "stl", "-o", stl];
    args.push(...itemRenderFlags(r));
    const idNote = r.bottomId ? ` id "${r.bottomId}"` : "";
    renderPlan.push(`  ${r.entry}: render ${pieceLabel(r)}${idNote} @ ${JSON.stringify(r.params)} → ${r.iteration}`);
    const res = await runWithTimeout("node", args, { timeoutMs: 120_000, label: "bikar_render" });
    if (res.code !== 0 || res.timedOut || !existsSync(stl)) {
      console.error(`bikar render failed for ${r.entry} (${r.sourcePath}, piece ${pieceLabel(r)}${idNote}):`);
      console.error((res.stderr || res.stdout || "").trim().split("\n").slice(-6).join("\n"));
      if (r.bottomId) {
        console.error(
          `  If the id is what bikar refused, leave this piece without one: mark its item ` +
            `\`no_id: "<bikar's reason>"\` in the recipe (D-109).`,
        );
      }
      process.exitCode = 1;
      return;
    }
    cache.set(ck, stl);
    try {
      const [fx, fy] = footprint(stlBounds(stl));
      footprints.set(ck, [fx, fy]);
    } catch (err) {
      console.error((err as Error).message);
      process.exitCode = 1;
      return;
    }
  }

  // 5. Bed-fit pre-check BEFORE the slow slicer (§6).
  const parts: PartFootprint[] = resolved.map((r) => {
    const [x, y] = footprints.get(cacheKeyOf(r))!;
    return { entry: r.entry, x, y, count: r.count };
  });
  const check = bedFitPrecheck(parts, bed);

  // 6. Build the Studio argv: all STL paths as trailing inputs (count copies each), --arrange 1. Each
  //    mesh goes in under its staged name, which the bed map reads back; one render serves every slot.
  //    With two or more filaments, each input also names its slot (--load-filament-ids).
  const inputs: string[] = [];
  const filamentIds: number[] = [];
  for (const r of resolved) {
    const rendered = cache.get(cacheKeyOf(r))!;
    const stl = join(scratch, stagedName(r));
    if (stl !== rendered && !existsSync(stl)) copyFileSync(rendered, stl);
    for (let c = 0; c < r.count; c++) {
      inputs.push(stl);
      filamentIds.push(r.filament);
    }
  }
  const outDir = opts.outputdir ? resolve(opts.outputdir) : platesDir();
  mkdirSync(outDir, { recursive: true });
  const outFile = opts.out ?? `${basename(absManifest).replace(/\.ya?ml$/i, "")}.plate.3mf`;
  const outPath = join(outDir, outFile);

  const studioBin = locateStudio();
  let settingsResolved = settingsName;
  let filamentResolved = filamentName;
  let presets: FlattenedPreset[] = [];
  if (studioBin) {
    try {
      // Names → files → one flattened file per preset (the CLI does not follow `inherits`), and the
      // plate to slice for, which Studio would otherwise default to a Cool Plate (plate-type.ts).
      const plate = resolveSlicePlateType(opts.plateType, studioSavedPlateType());
      console.log(`plate type: ${plate.type.name} (${plate.from})`);
      const prepared = prepareSlicePresets(
        settingsName,
        filamentName,
        studioBin,
        mkdtempSync(join(tmpdir(), "bambu-presets-")),
        plate.type,
        manifest.profile?.color,
      );
      settingsResolved = prepared.settings ?? settingsName;
      filamentResolved = prepared.filament ?? filamentName;
      presets = prepared.presets;
    } catch (err) {
      console.error((err as Error).message);
      process.exitCode = 2;
      return;
    }
  }
  const studioArgs = buildStudioArgs(
    inputs,
    outDir,
    outFile,
    {
      settings: settingsResolved,
      filament: filamentResolved,
      arrange: opts.arrange,
      plate: "0",
      ...(filaments > 1 ? { filamentIds } : {}), // one filament: the argv stays as it always was
    },
    raw,
  );

  // 7. --dry-run: print the plan, the resolved iteration ids, the pre-check, and the Studio argv —
  //    render happened (local, no slicer), but nothing is sliced and no record is written.
  if (opts.dryRun) {
    console.log(`plate: ${resolved.length} item(s), bed ${bed.label}`);
    console.log("render plan:");
    for (const line of renderPlan) console.log(line);
    console.log("resolved iterations:");
    for (const r of resolved) {
      const slot = filaments > 1 ? ` filament ${r.filament}` : "";
      console.log(`  ${r.entry}: ${r.iteration} ×${r.count} (${pieceLabel(r)})${r.label ? ` "${r.label}"` : ""}${slot}`);
    }
    console.log(`bed-fit pre-check: ${check.ok ? "PASS (necessary only — --arrange decides tiling)" : "FAIL"}`);
    for (const f of check.failures) console.log(`  ✗ ${f}`);
    console.log(`beds allowed: ${maxBeds} (the slice decides; a spill past it is refused after slicing)`);
    if (!studioBin) console.log("(BambuStudio not found — preset names shown unresolved)");
    console.log("dry run — would execute:");
    console.log([studioBin ?? "<BambuStudio>", ...studioArgs].map((a) => (/\s/.test(a) ? `"${a}"` : a)).join(" "));
    return;
  }

  // A failed pre-check refuses the plate before the slicer runs — naming the offending part.
  if (!check.ok) {
    console.error("bed-fit pre-check FAILED — not slicing:");
    for (const f of check.failures) console.error(`  ✗ ${f}`);
    process.exitCode = 1;
    return;
  }

  if (!studioBin) {
    console.error("No headless BambuStudio binary found — cannot slice a composed plate.");
    console.error("Install it (`bambu setup studio`) or set SLICER_PATH; then re-run compose.");
    process.exitCode = 1;
    return;
  }

  // 8. Slice.
  const timeoutMs = Math.max(30, Number(opts.timeout) || 600) * 1000;
  ev("compose_start", { manifest: basename(absManifest), items: resolved.length, inputs: inputs.length });
  const res = await runWithTimeout(studioBin, studioArgs, { timeoutMs, label: "studio_compose" });
  if (res.timedOut) {
    console.error(`compose slice timed out after ${opts.timeout}s. Raise --timeout, or compose fewer parts.`);
    process.exitCode = 1;
    return;
  }
  if (res.code !== 0 || !existsSync(outPath)) {
    console.error(`compose slice failed (exit ${res.code ?? "null"}).`);
    const tail = (res.stderr || res.stdout).trim().split("\n").slice(-8).join("\n");
    if (tail) console.error(tail);
    process.exitCode = 1;
    return;
  }
  const kb = Math.round(statSync(outPath).size / 1024);
  if (!(await enforceSliceCarriesPresets(outPath, presets))) {
    process.exitCode = 1;
    return;
  }

  // A plate that spilled onto more beds than the manifest allows is refused: no sidecar, no record,
  // so `print send` has nothing fresh to gate on. The .3mf stays for a look at what overflowed.
  const beds = (await readBeds(outPath)) ?? [];
  const entryByStl = new Map<string, string[]>();
  for (const r of resolved) {
    const key = stagedName(r);
    const label = `${r.entry} ${basename(r.sourcePath)}${r.piece ? ` piece ${r.piece}` : ""}`;
    entryByStl.set(key, [...(entryByStl.get(key) ?? []), label]);
  }
  const spilled = spilledItems(beds, entryByStl, maxBeds);
  if (spilled.length > 0) {
    console.error(
      `the plate spilled onto ${beds.length} beds (allowed ${maxBeds}) — ${spilled.length} object(s) would not print:`,
    );
    for (const s of spilled) console.error(`  ✗ ${s}`);
    console.error(`take items off, or set \`beds: ${beds.length}\` in the manifest if the spill is meant. (${outPath})`);
    process.exitCode = 1;
    return;
  }

  // Warnings sidecar — same capture/classify/sidecar as `slice plate`, so `bambu print send` can gate
  // the composed plate without re-slicing.
  const combined = `${res.stdout}\n${res.stderr}`;
  const warnings = parseSlicerWarnings(combined);
  const { expected, unexpected } = classifyWarnings(warnings, loadManifest());
  const sidecar: WarningsSidecar = {
    tool: "bambu slice compose",
    sliced_at: new Date().toISOString(),
    studio_version: studioVersionFrom(combined),
    source_sha256: hashFile(outPath) ?? undefined,
    recipe: recipeHashOf(outPath, repoRoot() ?? process.cwd()) ?? undefined, // slice-fresh.ts
    warnings,
  };
  try {
    writeFileSync(sidecarPath(outPath), JSON.stringify(sidecar, null, 2) + "\n");
  } catch (err) {
    console.error(`warning: could not write warnings sidecar: ${(err as Error).message}`);
  }
  ev("compose_done", { out: basename(outPath), kb, warnings: warnings.length, unexpected: unexpected.length });
  console.log(`composed → ${outPath} (${kb} KB, ${inputs.length} objects from ${resolved.length} variant(s))`);
  const preview = await writePlatePreview(outPath);
  console.log(preview ? `plate picture → ${preview} (look before sending)` : "plate picture: none in the 3MF.");

  // The bed map: which item each arranged object is, so sets that look alike are bagged right.
  const placements = await readPlacements(outPath);
  if (placements) {
    const rows = bedMap(placements, resolved);
    const mapPath = bedMapPathFor(outPath);
    writeFileSync(mapPath, JSON.stringify({ plate: basename(outPath), bed: bed.name, objects: rows }, null, 2) + "\n");
    console.log(`bed map → ${mapPath} (x, y from the front-left corner, mm):`);
    for (const row of rows) {
      const params = Object.entries(row.params).map(([k, v]) => `${k}=${v}`).join(" ");
      const what = [row.piece || "(default solid)", params].filter(Boolean).join(" ");
      const slot = filaments > 1 ? ` filament ${row.filament}` : "";
      console.log(`  ${row.label.padEnd(10)} ${row.entry.padEnd(4)} ${what.padEnd(24)} at ${row.x}, ${row.y}${slot}`);
    }
    const unmatched = rows.filter((r) => !r.entry);
    if (unmatched.length > 0) console.error(`warning: ${unmatched.length} object(s) on the bed matched no plate item.`);
  } else {
    console.error("warning: no bed map — the 3MF has no build items or object names to read.");
  }

  // 9. Scaffold the plate record with resolved objects[].iteration provenance (§7). Stops at a draft
  //    under .bambu/records/ and the OWNER GATE — compose never dispatches (that is `print send`).
  if (opts.record !== false) {
    const slug = outFile.replace(/\.(plate\.)?3mf$/i, "").replace(/[^a-z0-9-]+/gi, "-").toLowerCase();
    const objects: ScaffoldObject[] = resolved.map((r) => ({
      entry: r.entry,
      source: r.sourceAtRef, // @ref stripped by the scaffolder; the ref is pinned in pins.bikar_ref
      piece: r.piece || undefined, // "" (default solid) is recorded as an absent key, not an empty string
      sourceSha256: r.file ? r.sourceSha256 : undefined, // a local file has no bikar blob: record its own hash
      params: r.params,
      window: r.window || undefined,
      count: r.count,
      iteration: r.iteration,
    }));
    try {
      // The slice-side profile (machine, nozzle, layer, presets) comes off the .3mf just written —
      // the same builder `print send --record` uses; compose never reads the printer, so the frame
      // is empty and the printer-side fields (spool, loaded material) stay TODO.
      const profile = await recordProfileFrom({}, outPath);
      const dir = await scaffoldRecord({
        slug,
        plateName: outFile,
        plateFile: outPath,
        objects,
        profile,
        via: "bambu slice compose",
      });
      console.log(`draft record → ${dir} (fill TODOs, add photos, then \`bambu validate record\`).`);
    } catch (err) {
      console.error(`warning: could not scaffold record: ${(err as Error).message}`);
    }
  }

  if (unexpected.length > 0) {
    console.error(`slicer warnings: ${unexpected.length} UNEXPECTED — dispatch will be blocked:`);
    for (const w of unexpected) console.error(`  ✗ [${w.severity}] ${w.object ?? "(plate)"}: ${w.message}`);
  } else if (expected.length > 0) {
    console.log(`slicer warnings: ${expected.length} expected (by design).`);
  } else if (warnings.length === 0) {
    console.log("slicer warnings: none — clean.");
  }
  if (unexpected.length > 0 || (opts.strict && warnings.length > 0)) process.exitCode = 1;
}

/** The record dirs to scan for reprint-by-id: gitignored drafts + finished records under the repo. */
function listRecordDirs(): string[] {
  const dirs: string[] = [];
  for (const base of [recordsDir(), join(process.cwd(), "docs", "prints")]) {
    if (!existsSync(base)) continue;
    try {
      for (const d of readdirSync(base)) {
        const full = join(base, d);
        if (existsSync(join(full, "index.md"))) dirs.push(full);
      }
    } catch {
      /* unreadable base — skip */
    }
  }
  return dirs;
}

/** Attach the `compose` subcommand to the existing `slice` command group. */
export function registerCompose(slice: Command): void {
  slice
    .command("compose <plate.yaml>")
    .description("compose many bikar-rendered pieces onto one X2D plate (a manifest → one sliced .3mf)")
    .option("-o, --out <file>", "output filename (default: <manifest>.plate.3mf)")
    .option("-d, --outputdir <dir>", "output directory (default: build/plates at the repo root, else the current dir)")
    .option(
      "-s, --settings <names|paths>",
      "machine + process, semicolon-joined — overrides the manifest profile (preset display names or JSON paths; each inherits chain is flattened before slicing)",
    )
    .option(
      "-f, --filament <names|paths>",
      "filament, semicolon-joined — overrides the manifest profile (preset display name or JSON path; its inherits chain is flattened before slicing)",
    )
    .option("--bed <name>", "bed footprint for the fit pre-check (x2d = 256×256 mm)", "x2d")
    .option(
      "--plate-type <type>",
      "the build plate to slice for: cool_plate | eng_plate | hot_plate | textured_plate | supertack_plate (default: the one Bambu Studio is set to)",
    )
    .option("--arrange", "auto-arrange the objects on the plate (libnest2d in the slicer)", true)
    .option("--no-arrange", "do not auto-arrange (objects keep authored positions)")
    .option("--no-record", "skip scaffolding the draft plate record")
    .option("-t, --timeout <seconds>", "slice timeout in seconds", "600")
    .option("--strict", "exit non-zero if the slicer prints any warning at all", false)
    .option("--dry-run", "render + pre-check + print the exact BambuStudio invocation, but do not slice", false)
    .action(async (manifest: string, opts: ComposeOpts, cmd: Command) => {
      const raw = cmd.args.slice(1); // anything after `--` is forwarded to the BambuStudio CLI
      await runCompose(manifest, opts, raw);
    });
}
