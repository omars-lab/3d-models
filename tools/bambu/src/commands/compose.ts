// `bambu slice compose <plate.yaml>` — many rendered pieces onto one X2D plate.
//
// A subverb of the `slice` command group (sibling to `slice plate`/`slice open`). It reads a manifest
// of items, renders each variant through bikar (once, cached), runs a bed-fit pre-check, then hands ALL
// the STLs to the Bambu Studio CLI in one `--arrange 1 --export-3mf` invocation — one composed plate.
// It is NOT a new CLI or top-level command; it reuses `slice.ts`'s preset resolver, argv builder and
// warnings sidecar, and the `records.ts` scaffolder. Full spec: docs/plate-composer-design.md.
//
// The one genuinely new idea (D-072): a manifest item is not an identity — it is the GEOMETRY HALF of
// an iteration key, completed by the plate's one slice profile and resolved to `it-<sha12>` (src/
// iteration.ts). The composer writes that id into the plate record's objects[].iteration; the manifest
// mints no parallel id, so nothing forks (CLAUDE.md "a migration never buys a fork", D-052).

import { Command } from "commander";
import { existsSync, readFileSync, writeFileSync, mkdtempSync, statSync, readdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, join, resolve } from "node:path";
import { parse as parseYaml } from "yaml";
import { runWithTimeout, ev } from "../log.js";
import { surveyBackends, preferenceFor } from "../backends/router.js";
import { locateStudio } from "../backends/studio-cli.js";
import { locateBikarCli, bikarDir, bikarHead, bikarBlobSha } from "../backends/bikar.js";
import {
  parseSlicerWarnings,
  classifyWarnings,
  loadManifest,
  studioVersionFrom,
  sidecarPath,
  hashFile,
  type WarningsSidecar,
} from "../backends/warnings.js";
import { resolvePresetList, buildStudioArgs } from "./slice.js";
import { iterationId, type IterationKey } from "../iteration.js";
import { stlBounds, footprint } from "../mesh.js";
import { scaffoldRecord, type ScaffoldObject } from "../records.js";
import { recordProfileFrom } from "../header.js";
import { recordsDir } from "../paths.js";

// ── The manifest ─────────────────────────────────────────────────────────────────────────────────
// A small hand-authorable file. Two item spellings resolve to the SAME iteration id (§3):
//   - {bkr, piece, params, count} — the geometry half, completed by the plate profile.
//   - {iteration, count}          — an already-known it-<sha12> (reprint-by-id; see resolveItem).

export interface PlateProfile {
  settings?: string; // "<machine>;<process>" preset display names (-s)
  filament?: string; // filament preset display name(s) (-f)
}
export interface ManifestItemBkr {
  bkr: string; // "bikar:<path>" source
  piece?: string; // a NAMED piece/tile/clip to render; omit to render the file's default last solid
  params?: Record<string, number>; // --param overrides (bikar --param takes numbers)
  count?: number; // copies on the plate (default 1)
}
export interface ManifestItemIteration {
  iteration: string; // an already-known it-<sha12>
  count?: number;
}
export type ManifestItem = ManifestItemBkr | ManifestItemIteration;
export interface PlateManifest {
  bed?: string; // bed footprint name (default x2d)
  profile?: PlateProfile; // the ONE slice profile the plate is sliced under
  items: ManifestItem[];
}

function isIterationItem(it: ManifestItem): it is ManifestItemIteration {
  return typeof (it as ManifestItemIteration).iteration === "string";
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
  items.forEach((raw, i) => {
    if (!raw || typeof raw !== "object") throw new Error(`items[${i}] is not a mapping`);
    const it = raw as Record<string, unknown>;
    const where = `items[${i}]`;
    if (typeof it.iteration === "string") {
      if (it.bkr || it.piece) throw new Error(`${where}: an \`iteration:\` item cannot also carry bkr/piece`);
    } else {
      if (typeof it.bkr !== "string" || !it.bkr.startsWith("bikar:")) {
        throw new Error(`${where}: \`bkr:\` must be a "bikar:<path>" string (or use \`iteration:\`)`);
      }
      if (it.piece !== undefined && (typeof it.piece !== "string" || !it.piece)) {
        throw new Error(`${where}: \`piece:\` must be a non-empty string (a named piece/tile/clip); omit it to render the file's default solid`);
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
  });
  return {
    bed: typeof m.bed === "string" ? m.bed : undefined,
    profile: (m.profile as PlateProfile) ?? undefined,
    items: items as ManifestItem[],
  };
}

// ── The bed and the fit pre-check (§6) ──────────────────────────────────────────────────────────
// **Default:** the x2d bed footprint is 256 × 256 mm — the X2D single-nozzle build area (D-053; the
// K1 note in docs/plate-composer-design.md §6 carries the dual-nozzle narrowing to 235.5 mm). The
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
}

/** One resolved on-plate item: its geometry pins, the count, and (filled after render) its footprint
 *  and cached STL path. `source` carries the @ref for the iteration key; the record strips it. */
export interface ResolvedItem {
  entry: string; // stable per-item label on the plate (compose orders them c1, c2, …)
  sourcePath: string; // "<path>" (no bikar: prefix, no @ref)
  sourceAtRef: string; // "bikar:<path>@<ref>" for the iteration key
  piece: string;
  params: Record<string, number>;
  count: number;
  sourceSha256: string;
  iteration: string; // it-<sha12>
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
 *  the same recipe. This is the reprint-by-id lookup docs/plate-composer-design.md §3 defers to; it
 *  reads records only (no re-slice here). Returns null if no record names the id yet. */
export function findIterationGeometry(
  id: string,
  recordDirs: string[],
  readIndex: (dir: string) => string | null,
): { sourcePath: string; piece: string; params: Record<string, number> } | null {
  const hits: Array<{ run: string; geom: { sourcePath: string; piece: string; params: Record<string, number> } }> = [];
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
          geom: { sourcePath, piece: String(o.piece ?? ""), params: (o.params as Record<string, number>) ?? {} },
        });
      }
    }
  }
  hits.sort((a, b) => (a.run < b.run ? 1 : -1)); // newest run name first (date-prefixed)
  return hits[0]?.geom ?? null;
}

/** Resolve every manifest item to its geometry pins + iteration id. D-072: an item is the GEOMETRY
 *  HALF of the key, completed by the plate's one slice profile — the manifest mints no parallel id, so
 *  nothing forks (CLAUDE.md "a migration never buys a fork"). Shared by `slice compose` (loose-STL
 *  plates) and `slice coaster` (multi-part colour plates), so both derive the same it-<sha12> for the
 *  same recipe. Throws an item-indexed error; the caller maps it to an exit code. */
export async function resolveManifestItems(
  items: ManifestItem[],
  bikarRef: string,
  sliceProfile: { settings: string; filament: string },
): Promise<ResolvedItem[]> {
  const resolved: ResolvedItem[] = [];
  let n = 0;
  for (const item of items) {
    n += 1;
    let sourcePath: string;
    let piece: string;
    let params: Record<string, number>;
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
    } else {
      sourcePath = item.bkr.replace(/^bikar:/, "");
      piece = item.piece ?? ""; // "" ⇒ the file's default last solid (bikar renders it without --piece)
      params = item.params ?? {};
    }
    const sourceSha256 = await blobSha(bikarRef, sourcePath);
    const key: IterationKey = {
      source: `bikar:${sourcePath}@${bikarRef}`,
      source_sha256: sourceSha256,
      piece,
      params,
      slice_profile: sliceProfile,
    };
    resolved.push({
      entry: `c${n}`,
      sourcePath,
      sourceAtRef: `bikar:${sourcePath}@${bikarRef}`,
      piece,
      params,
      count: item.count ?? 1,
      sourceSha256,
      iteration: iterationId(key),
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

  // 3. Resolve each manifest item to its geometry pins + iteration id (shared with `slice coaster`).
  const sliceProfile = { settings: settingsName, filament: filamentName };
  let resolved: ResolvedItem[];
  try {
    resolved = await resolveManifestItems(manifest.items, bikarRef, sliceProfile);
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
    `${r.sourceSha256}:${r.piece}:${JSON.stringify(r.params)}`;
  const pieceLabel = (r: ResolvedItem): string => (r.piece ? r.piece : "default solid");
  for (const r of resolved) {
    const ck = cacheKeyOf(r);
    if (cache.has(ck)) {
      renderPlan.push(`  ${r.entry}: cache hit — ${pieceLabel(r)} @ ${JSON.stringify(r.params)} (${r.iteration})`);
      continue;
    }
    const stl = join(scratch, `${r.iteration}.stl`);
    // `--piece` renders a NAMED piece/tile/clip; a plain orb has none, so omit the flag and bikar
    // renders the file's default last solid (its own model — the only way to render a clip is --piece).
    const args = [bikarCli, "render", resolve(bikarDir(), r.sourcePath), "--format", "stl", "-o", stl];
    if (r.piece) args.push("--piece", r.piece);
    for (const [k, v] of Object.entries(r.params)) args.push("--param", `${k}=${v}`);
    renderPlan.push(`  ${r.entry}: render ${pieceLabel(r)} @ ${JSON.stringify(r.params)} → ${r.iteration}`);
    const res = await runWithTimeout("node", args, { timeoutMs: 120_000, label: "bikar_render" });
    if (res.code !== 0 || res.timedOut || !existsSync(stl)) {
      console.error(`bikar render failed for ${r.entry} (${r.sourcePath}, piece ${pieceLabel(r)}):`);
      console.error((res.stderr || res.stdout || "").trim().split("\n").slice(-6).join("\n"));
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

  // 6. Build the Studio argv: all STL paths as trailing inputs (count copies each), --arrange 1.
  const inputs: string[] = [];
  for (const r of resolved) {
    const stl = cache.get(cacheKeyOf(r))!;
    for (let c = 0; c < r.count; c++) inputs.push(stl);
  }
  const outDir = opts.outputdir ? resolve(opts.outputdir) : process.cwd();
  const outFile = opts.out ?? `${basename(absManifest).replace(/\.ya?ml$/i, "")}.plate.3mf`;
  const outPath = join(outDir, outFile);

  const studioBin = locateStudio();
  let settingsResolved = settingsName;
  let filamentResolved = filamentName;
  if (studioBin) {
    try {
      settingsResolved = resolvePresetList(settingsName, "settings", studioBin);
      filamentResolved = resolvePresetList(filamentName, "filament", studioBin);
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
    { settings: settingsResolved, filament: filamentResolved, arrange: opts.arrange, plate: "0" },
    raw,
  );

  // 7. --dry-run: print the plan, the resolved iteration ids, the pre-check, and the Studio argv —
  //    render happened (local, no slicer), but nothing is sliced and no record is written.
  if (opts.dryRun) {
    console.log(`plate: ${resolved.length} item(s), bed ${bed.label}`);
    console.log("render plan:");
    for (const line of renderPlan) console.log(line);
    console.log("resolved iterations:");
    for (const r of resolved) console.log(`  ${r.entry}: ${r.iteration} ×${r.count} (${pieceLabel(r)})`);
    console.log(`bed-fit pre-check: ${check.ok ? "PASS (necessary only — --arrange decides tiling)" : "FAIL"}`);
    for (const f of check.failures) console.log(`  ✗ ${f}`);
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
    warnings,
  };
  try {
    writeFileSync(sidecarPath(outPath), JSON.stringify(sidecar, null, 2) + "\n");
  } catch (err) {
    console.error(`warning: could not write warnings sidecar: ${(err as Error).message}`);
  }
  ev("compose_done", { out: basename(outPath), kb, warnings: warnings.length, unexpected: unexpected.length });
  console.log(`composed → ${outPath} (${kb} KB, ${inputs.length} objects from ${resolved.length} variant(s))`);

  // 9. Scaffold the plate record with resolved objects[].iteration provenance (§7). Stops at a draft
  //    under .bambu/records/ and the OWNER GATE — compose never dispatches (that is `print send`).
  if (opts.record !== false) {
    const slug = outFile.replace(/\.(plate\.)?3mf$/i, "").replace(/[^a-z0-9-]+/gi, "-").toLowerCase();
    const objects: ScaffoldObject[] = resolved.map((r) => ({
      entry: r.entry,
      source: r.sourceAtRef, // @ref stripped by the scaffolder; the ref is pinned in pins.bikar_ref
      piece: r.piece || undefined, // "" (default solid) is recorded as an absent key, not an empty string

      params: r.params,
      count: r.count,
      iteration: r.iteration,
    }));
    try {
      // The slice-side profile (machine, nozzle, layer, presets) comes off the .3mf just written —
      // the same builder `print send --record` uses; compose never reads the printer, so the frame
      // is empty and the printer-side fields (spool, loaded material) stay TODO.
      const profile = await recordProfileFrom({}, outPath);
      const dir = await scaffoldRecord({ slug, plateName: outFile, plateFile: outPath, objects, profile });
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
    .option("-d, --outputdir <dir>", "output directory (default: current dir)")
    .option(
      "-s, --settings <names|paths>",
      "machine + process, semicolon-joined — overrides the manifest profile (preset display names or JSON paths)",
    )
    .option(
      "-f, --filament <names|paths>",
      "filament, semicolon-joined — overrides the manifest profile (preset display name or JSON path)",
    )
    .option("--bed <name>", "bed footprint for the fit pre-check (x2d = 256×256 mm)", "x2d")
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
