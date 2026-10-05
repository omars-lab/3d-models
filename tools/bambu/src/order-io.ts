// The reading and running behind `bambu order plan` and `bambu plates by-color`: the color catalog,
// the palette's store notes, a pieces .bkr's groups (its text and `bikar bands`), and slicing a
// written recipe for its beds, minutes and grams. order.ts and by-color.ts stay pure; this file is
// what they are handed.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { isAbsolute, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { parse as parseYaml } from "yaml";
import { bikarDir, locateBikarCli } from "./backends/bikar.js";
import { type BandsOrbit, type PieceGroup, type WrittenRecipe, pieceGroups, readPiecesBkr } from "./by-color.js";
import { canonicalJson } from "./iteration.js";
import { runWithTimeout } from "./log.js";
import type { CatalogColor, GroupsOf, SliceFacts } from "./order.js";
import { minutesOf, sliceNumbers } from "./slice-numbers.js";
import { readMember } from "./threemf.js";

export const CATALOG = "docs/design/coaster/themes/catalog/catalog.yaml";
export const PALETTE = ".claude/skills/color-themes/palette.yaml";

/** Every color in the catalog (generated from Bambu Studio's own list). */
export function loadCatalog(root: string): CatalogColor[] {
  const doc = parseYaml(readFileSync(join(root, CATALOG), "utf8")) as { colors?: unknown };
  if (!Array.isArray(doc?.colors)) throw new Error(`${CATALOG}: no \`colors:\` list`);
  return doc.colors.map((c: Record<string, unknown>) => ({
    code: String(c.code),
    line: String(c.line),
    name: String(c.name),
    hexes: Array.isArray(c.hexes) ? c.hexes.map(String) : [],
  }));
}

/** The palette's store notes, by `<line>|<code>` ("not on the US store, 2026-10-04"). */
export function loadNotes(root: string): Map<string, string> {
  const doc = parseYaml(readFileSync(join(root, PALETTE), "utf8")) as Record<string, unknown>;
  const notes = new Map<string, string>();
  for (const list of Object.values(doc ?? {})) {
    if (!Array.isArray(list)) continue;
    for (const e of list as Array<Record<string, unknown>>) {
      if (e && typeof e.note === "string" && e.line && e.code) notes.set(`${String(e.line)}|${String(e.code)}`, e.note);
    }
  }
  return notes;
}

/** A construction as a recipe names it, `bikar:<path in the bikar checkout>`, from either that form,
 *  a path relative to the checkout, or an absolute path inside it. */
export function asBikarSource(arg: string): string {
  if (arg.startsWith("bikar:")) return arg;
  const rel = isAbsolute(arg) ? relative(bikarDir(), arg) : arg;
  if (rel.startsWith("..")) throw new Error(`${arg}: not inside the bikar checkout (${bikarDir()}); set BIKAR_DIR`);
  return `bikar:${rel}`;
}

function sourcePath(construction: string): string {
  return join(bikarDir(), construction.replace(/^bikar:/, ""));
}

const groupCache = new Map<string, PieceGroup[]>();
const keyOf = (construction: string, params: Record<string, number>) => `${construction} ${canonicalJson(params)}`;

/** Run `bikar bands` on each pieces construction not yet read, and read its .bkr: afterwards the
 *  returned lookup answers for those, and throws for any other (a bug: every pair is fetched first). */
export async function fetchGroups(pairs: Array<{ construction: string; params: Record<string, number> }>): Promise<GroupsOf> {
  for (const { construction, params } of pairs) {
    const key = keyOf(construction, params);
    if (groupCache.has(key)) continue;
    const file = sourcePath(construction);
    if (!existsSync(file)) throw new Error(`${construction}: no such file in the bikar checkout (${bikarDir()})`);
    const cli = locateBikarCli();
    if (!cli) throw new Error(`bikar CLI not built at ${bikarDir()}/packages/cli/dist/index.js; build it or set BIKAR_DIR`);
    const args = [cli, "bands", file, "--json", ...Object.entries(params).flatMap(([k, v]) => ["--param", `${k}=${v}`])];
    const res = await runWithTimeout("node", args, { timeoutMs: 120_000, label: "bikar_bands" });
    if (res.code !== 0 || res.timedOut) {
      throw new Error(`bikar bands ${construction} failed (exit ${res.code ?? "timeout"}): ${res.stderr.trim().split("\n").pop() ?? ""}`);
    }
    const orbits = (JSON.parse(res.stdout) as { orbits?: { orbits?: BandsOrbit[] } }).orbits?.orbits ?? [];
    groupCache.set(key, pieceGroups(readPiecesBkr(readFileSync(file, "utf8")), orbits));
  }
  return (construction, params) => {
    const g = groupCache.get(keyOf(construction, params));
    if (!g) throw new Error(`${construction} ${canonicalJson(params)}: groups not fetched`);
    return g;
  };
}

/** Write each recipe as `<dir>/<name>.yaml`. */
export function writeRecipeFiles(dir: string, recipes: WrittenRecipe[]): string[] {
  mkdirSync(dir, { recursive: true });
  return recipes.map((r) => {
    const path = join(dir, `${r.name}.yaml`);
    writeFileSync(path, r.text);
    return path;
  });
}

const BAMBU = fileURLToPath(new URL("../bin/bambu", import.meta.url));

/** Slice one written recipe with `bambu slice compose` and read its numbers. A spill onto a second
 *  bed makes compose exit 1 but keeps the .3mf, and that is still a slice: its beds say so. */
export async function sliceRecipe(recipePath: string, name: string, dir: string): Promise<SliceFacts> {
  const res = await runWithTimeout(BAMBU, ["slice", "compose", recipePath, "-d", dir, "--no-record"], {
    timeoutMs: 900_000,
    label: "slice_compose",
  });
  const threemf = join(dir, `${name}.plate.3mf`);
  const info = existsSync(threemf) ? await readMember(threemf, "Metadata/slice_info.config") : null;
  if (!info) {
    throw new Error(`${name}: the slice made no plate (exit ${res.code ?? "timeout"}): ${res.stderr.trim().split("\n").slice(-3).join(" | ")}`);
  }
  return sliceFacts(name, info);
}

/** A slice's facts from its slice_info, read by `sliceNumbers` as `bambu validate sliced` reads them,
 *  so the minutes a plan or the cost view shows are the ones that command prints. */
export function sliceFacts(name: string, info: string): SliceFacts {
  const n = sliceNumbers(info);
  if (n.predictionS === null) throw new Error(`${name}: the slice carries no time`);
  return {
    recipe: name,
    beds: Math.max(1, n.beds.length),
    minutes: minutesOf(n.predictionS),
    grams: n.grams,
    layers: n.layers,
    bed_minutes: n.beds.map((b) => (b.predictionS === null ? 0 : minutesOf(b.predictionS))),
  };
}
