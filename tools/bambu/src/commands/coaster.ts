// `bambu slice coaster <plate.yaml>` — a multi-filament COLOUR plate for the X2D AMS.
//
// A subverb of the `slice` command group, sibling to `slice compose`. Where `compose` renders each item
// as one solid (`--format stl`) and hands the loose STLs to BambuStudio's `--arrange 1 --export-3mf`,
// a COLOUR plate cannot: a coaster's base/straps/border must stay coincident to register as ONE coaster
// (K10, plate-composer-design.md §12), and the headless CLI has no flag to assign an object to an AMS
// slot — the assignment must be baked into the INPUT 3MF (#9666). So this verb:
//   1. renders each item with `bikar render --format parts` → one STL per region body + a sidecar
//      tagging each body with its palette name + hex (bikar #215);
//   2. maps palette name → logical AMS slot across the whole plate (src/ams.ts, D-075);
//   3. ASSEMBLES the multi-part 3MF directly (src/threemf-assemble.ts) — each coaster one object, its
//      region bodies parts carrying `<metadata key="extruder">`, root `Application=BambuStudio-<ver>`;
//   4. VERIFIES geometry headless on a TAG-STRIPPED copy (the versioned tag SIGSEGVs the headless
//      slicer — docs/issues/coaster-3mf-filament-shape-and-export-hang.md §1), and leaves the colour
//      check to a GUI load (`bambu slice open`), which the pivot doc §4 shows is the only honest signal.
//
// It reuses `compose.ts`'s manifest parse + item resolution (the D-072 iteration key: an item is the
// geometry half, so a coaster reprinted from either verb derives the SAME it-<sha12> and nothing forks),
// the bed-fit pre-check, and the record scaffolder. It NEVER dispatches — that is `print send`, owner-gated.

import { Command } from "commander";
import { existsSync, mkdtempSync, mkdirSync, readdirSync, readFileSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, join, resolve } from "node:path";
import { runWithTimeout, ev } from "../log.js";
import { locateStudio, probeStudio } from "../backends/studio-cli.js";
import { locateBikarCli, bikarDir, bikarHead } from "../backends/bikar.js";
import {
  parseManifest,
  resolveBed,
  bedFitPrecheck,
  resolveManifestItems,
  type Bed,
  type PartFootprint,
  type PlateManifest,
  type ResolvedItem,
} from "./compose.js";
import {
  buildAmsSlotMap,
  extruderForRegion,
  DEFAULT_AMS_SLOTS,
  type CoasterPartsSidecar,
  type AmsSlotMap,
  type FilamentDefaults,
} from "../ams.js";
import {
  buildThreeMfMembers,
  writeThreeMf,
  stripApplicationTag,
  type AssemblyCoaster,
} from "../threemf-assemble.js";
import { stlToIndexedMesh, stlBounds, footprint, type Bounds, type IndexedMesh } from "../mesh.js";
import { resolvePresetList } from "./slice.js";
import { scaffoldRecord, type ScaffoldObject } from "../records.js";

// **Default:** the plate's slot-1 filament — the material every colour slot reuses and the id that keeps
// each slot off the external spool (a non-empty product id, §6). PLA / GFA00 (Bambu PLA Basic) / white.
// Resolving the id + colour from the actual `profile.filament` preset JSON is a follow-up; a wrong id
// would only mis-label slot 1's product, not mis-assign a region (the region→slot map is exact). (D-075.)
const DEFAULT_FILAMENT: FilamentDefaults = { type: "PLA", id: "GFA00", hex: "#ffffff" };

interface CoasterOpts {
  out?: string;
  outputdir?: string;
  settings?: string;
  filament?: string;
  bed: string;
  pinch: string;
  maxSlots?: string;
  timeout: string;
  verifyGeometry: boolean;
  dryRun?: boolean;
  record?: boolean;
}

/** One rendered coaster: the resolved item, the sidecar bikar wrote, and where its region STLs live. */
interface RenderedCoaster {
  item: ResolvedItem;
  sidecar: CoasterPartsSidecar;
  dir: string; // the render output dir (STLs + sidecar), keyed to the iteration id
}

/** The union footprint of a coaster's region bodies (the bodies share a frame, so the plate packs a
 *  whole coaster, not loose bodies — the bbox is the union, not the sum). */
export function coasterFootprint(dir: string, sidecar: CoasterPartsSidecar): [number, number] {
  let u: Bounds | null = null;
  for (const p of sidecar.parts) {
    const b = stlBounds(join(dir, p.stl));
    u = u
      ? {
          min: [Math.min(u.min[0], b.min[0]), Math.min(u.min[1], b.min[1]), Math.min(u.min[2], b.min[2])],
          max: [Math.max(u.max[0], b.max[0]), Math.max(u.max[1], b.max[1]), Math.max(u.max[2], b.max[2])],
        }
      : b;
  }
  if (!u) throw new Error(`coaster "${sidecar.coaster}" has no region bodies to measure`);
  return footprint(u);
}

/** Render one resolved item with `bikar render --format parts`, returning its sidecar + output dir.
 *  Distinct recipes are rendered once and cached by iteration id (the geometry half of the key). */
async function renderParts(
  r: ResolvedItem,
  bikarCli: string,
  pinch: string,
  scratch: string,
): Promise<CoasterPartsSidecar> {
  const outDir = join(scratch, r.iteration);
  mkdirSync(outDir, { recursive: true });
  const args = [bikarCli, "render", resolve(bikarDir(), r.sourcePath), "--format", "parts", "--pinch", pinch, "-o", outDir];
  if (r.piece) args.push("--piece", r.piece);
  for (const [k, v] of Object.entries(r.params)) args.push("--param", `${k}=${v}`);
  const res = await runWithTimeout("node", args, { timeoutMs: 180_000, label: "bikar_render_parts" });
  if (res.code !== 0 || res.timedOut) {
    const tail = (res.stderr || res.stdout || "").trim().split("\n").slice(-6).join("\n");
    throw new Error(`bikar render --format parts failed for ${r.entry} (${r.sourcePath}):\n${tail}`);
  }
  // bikar writes `<CoasterName>.parts.json`; there is exactly one coaster per source, so take the sidecar.
  const sidecarName = findSidecar(outDir);
  if (!sidecarName) {
    throw new Error(
      `${r.entry}: bikar rendered no <Coaster>.parts.json in ${outDir} — is there a coaster declaration ` +
        `with color regions in ${r.sourcePath}? (\`--format parts\` needs one.)`,
    );
  }
  const sidecar = JSON.parse(readFileSync(join(outDir, sidecarName), "utf8")) as CoasterPartsSidecar;
  return sidecar;
}

/** The single `*.parts.json` sidecar in a render dir (bikar writes exactly one per coaster source). */
function findSidecar(dir: string): string | null {
  return readdirSync(dir).find((f) => f.endsWith(".parts.json")) ?? null;
}

/** One distinct rendered recipe, ready to be expanded into `count` plate objects. */
export interface CoasterAssemblyInput {
  entry: string; // the manifest entry label (e.g. "1"), the object-name prefix
  count: number; // how many copies of this recipe the plate carries
  displayName: string; // bikar's coaster name (sidecar.coaster)
  key: string; // the slot-map coaster key (the iteration id the map was built under)
  parts: CoasterPartsSidecar["parts"];
  meshFor: (stl: string) => IndexedMesh; // resolves a region STL filename to its indexed mesh
}

/** Expand each recipe × its count into AssemblyCoaster objects: one object per copy, each region body
 *  carrying the logical extruder for its palette (via the slot map). A `#k` suffix distinguishes copies
 *  only when count > 1. Pure — the only disk access is behind `meshFor` — so the name/extruder/count
 *  invariants are unit-testable without bikar or BambuStudio (step 7 of runCoaster is this function). */
export function assembleCoasters(inputs: CoasterAssemblyInput[], map: AmsSlotMap): AssemblyCoaster[] {
  const coasters: AssemblyCoaster[] = [];
  for (const inp of inputs) {
    for (let c = 0; c < inp.count; c++) {
      const label = inp.count > 1 ? `${inp.displayName} #${c + 1}` : inp.displayName;
      coasters.push({
        name: `${inp.entry}: ${label}`,
        bodies: inp.parts.map((p) => ({
          region: p.region,
          name: `${label} · ${p.region}${p.paletteName ? ` (${p.paletteName})` : ""}`,
          extruder: extruderForRegion(map, inp.key, p.region),
          mesh: inp.meshFor(p.stl),
        })),
      });
    }
  }
  return coasters;
}

async function runCoaster(manifestPath: string, opts: CoasterOpts): Promise<void> {
  const absManifest = resolve(manifestPath);
  if (!existsSync(absManifest)) {
    console.error(`no such manifest: ${manifestPath}`);
    process.exitCode = 1;
    return;
  }

  // 1. Manifest + profile + bed (CLI -s/-f override the manifest `profile:`; same rules as compose).
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
  let bed: Bed;
  try {
    bed = resolveBed(opts.bed ?? manifest.bed ?? "x2d");
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 2;
    return;
  }
  if (!settingsName || !filamentName) {
    console.error(
      "a colour plate needs one slice profile — set `profile.settings` + `profile.filament` in the " +
        "manifest, or pass -s/--settings and -f/--filament. Slot 1 is the plate's default filament.",
    );
    process.exitCode = 2;
    return;
  }
  const maxSlots = opts.maxSlots ? Math.max(1, Number(opts.maxSlots) || DEFAULT_AMS_SLOTS) : DEFAULT_AMS_SLOTS;

  // 2. bikar must be available — the composer renders each coaster's region bodies from source.
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

  // 3. Resolve items to geometry pins + iteration ids (shared with `slice compose`, so an it-<sha12>
  //    reprinted either way is the same recipe — no parallel id, nothing forks).
  const sliceProfile = { settings: settingsName, filament: filamentName };
  let resolved: ResolvedItem[];
  try {
    resolved = await resolveManifestItems(manifest.items, bikarRef, sliceProfile);
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 2;
    return;
  }

  // 4. Render each DISTINCT recipe once with `--format parts`; key by iteration id (the geometry half).
  const scratch = mkdtempSync(join(tmpdir(), "bambu-coaster-"));
  const rendered = new Map<string, RenderedCoaster>(); // iteration id → rendered coaster
  try {
    for (const r of resolved) {
      if (rendered.has(r.iteration)) continue;
      const sidecar = await renderParts(r, bikarCli, opts.pinch, scratch);
      rendered.set(r.iteration, { item: r, sidecar, dir: join(scratch, r.iteration) });
    }
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 1;
    return;
  }

  // 5. Palette name → logical AMS slot across the whole plate. The slot map is keyed by a UNIQUE per-item
  //    key (the iteration id) so two items whose bikar coaster share a display name never collide; palette
  //    slots are plate-global (first-seen order = item order, then part order), so DISTINCT recipes seed it.
  const sidecarsForMap: CoasterPartsSidecar[] = [];
  const keyOf = new Map<string, string>(); // resolved.entry → slot-map coaster key (iteration id)
  for (const r of resolved) {
    if (keyOf.has(r.iteration)) {
      keyOf.set(r.entry, r.iteration);
      continue;
    }
    const rc = rendered.get(r.iteration)!;
    sidecarsForMap.push({ ...rc.sidecar, coaster: r.iteration });
    keyOf.set(r.entry, r.iteration);
  }
  let map: AmsSlotMap;
  try {
    map = buildAmsSlotMap(sidecarsForMap, { defaultFilament: filamentName, maxSlots });
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 1;
    return;
  }

  // 6. Bed-fit pre-check on whole-coaster footprints (union bbox per coaster × count).
  const parts: PartFootprint[] = [];
  for (const r of resolved) {
    const rc = rendered.get(r.iteration)!;
    const [x, y] = coasterFootprint(rc.dir, rc.sidecar);
    parts.push({ entry: r.entry, x, y, count: r.count });
  }
  const check = bedFitPrecheck(parts, bed);

  // 7. Assemble the AssemblyCoaster[] — each item × count is one object; region bodies are its parts.
  const coasters: AssemblyCoaster[] = assembleCoasters(
    resolved.map((r) => {
      const rc = rendered.get(r.iteration)!;
      return {
        entry: r.entry,
        count: r.count,
        displayName: rc.sidecar.coaster,
        key: keyOf.get(r.entry)!,
        parts: rc.sidecar.parts,
        meshFor: (stl: string) => stlToIndexedMesh(join(rc.dir, stl)),
      };
    }),
    map,
  );

  // 8. The output paths + the Application version tag (the shipped artifact keeps the versioned tag).
  const outDir = opts.outputdir ? resolve(opts.outputdir) : process.cwd();
  const outFile = opts.out ?? `${basename(absManifest).replace(/\.ya?ml$/i, "")}.plate.3mf`;
  const outPath = join(outDir, outFile);
  const probe = await probeStudio();
  const studioVersion = probe.version?.match(/(\d+\.\d+\.\d+\.\d+)/)?.[1] ?? "02.08.02.61";
  const appVersion = `BambuStudio-${studioVersion}`;

  // Report the slot map — the operator loads the physical AMS to match (logical ≠ physical, K1).
  const slotTable = map.slots.map((s) => `  slot ${s.slot}: ${s.paletteName ?? "(plate default)"} ${s.hex ?? DEFAULT_FILAMENT.hex}`);

  if (opts.dryRun) {
    console.log(`colour plate: ${resolved.length} coaster variant(s), ${coasters.length} object(s), bed ${bed.label}`);
    console.log("AMS logical slots (palette name → slot; physical spool bound at print time by colour):");
    for (const line of slotTable) console.log(line);
    console.log(`bed-fit pre-check: ${check.ok ? "PASS (necessary only — --arrange decides tiling)" : "FAIL"}`);
    for (const f of check.failures) console.log(`  ✗ ${f}`);
    console.log(`would assemble → ${outPath} (Application=${appVersion}; ${coasters.length} objects)`);
    console.log(opts.verifyGeometry ? "would then verify geometry headless on a tag-stripped copy." : "geometry verify: skipped (--no-verify-geometry).");
    return;
  }

  if (!check.ok) {
    console.error("bed-fit pre-check FAILED — not assembling:");
    for (const f of check.failures) console.error(`  ✗ ${f}`);
    process.exitCode = 1;
    return;
  }

  // 9. Assemble the shipped (tagged) 3MF.
  let members;
  try {
    members = buildThreeMfMembers(coasters, map, DEFAULT_FILAMENT, appVersion);
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 1;
    return;
  }
  ev("coaster_assemble", { manifest: basename(absManifest), coasters: coasters.length, slots: map.slots.length });
  try {
    writeThreeMf(members, outPath, join(scratch, "asm"));
  } catch (err) {
    console.error(`assembly failed: ${(err as Error).message}`);
    process.exitCode = 1;
    return;
  }
  const kb = Math.round(statSync(outPath).size / 1024);
  console.log(`assembled → ${outPath} (${kb} KB, ${coasters.length} coaster object(s), ${map.slots.length} AMS slot(s))`);
  console.log("AMS logical slots (load the physical AMS to match — logical ≠ physical, K1):");
  for (const line of slotTable) console.log(line);

  // 10. Verify GEOMETRY headless on a TAG-STRIPPED copy (the versioned tag SIGSEGVs the headless CLI;
  //     colour is verified by a GUI load — `bambu slice open`). No `--export-3mf` (it hangs headless, §3).
  if (opts.verifyGeometry) {
    const studioBin = locateStudio();
    if (!studioBin) {
      console.log("geometry verify: skipped — no headless BambuStudio found (install it or --no-verify-geometry).");
    } else {
      const ok = await verifyGeometry(studioBin, members, coasters, settingsName, filamentName, opts, scratch);
      if (!ok) {
        console.error("geometry verify FAILED — the assembled plate did not slice clean headless (tag-stripped).");
        process.exitCode = 1;
        return;
      }
    }
  }

  // 11. Scaffold the plate record (draft, gitignored) — provenance by iteration id; never dispatches.
  if (opts.record !== false) {
    const slug = outFile.replace(/\.(plate\.)?3mf$/i, "").replace(/[^a-z0-9-]+/gi, "-").toLowerCase();
    const objects: ScaffoldObject[] = resolved.map((r) => ({
      entry: r.entry,
      source: r.sourceAtRef,
      piece: r.piece || undefined,
      params: r.params,
      count: r.count,
      iteration: r.iteration,
    }));
    try {
      const dir = await scaffoldRecord({ slug, plateName: outFile, plateFile: outPath, objects });
      console.log(`draft record → ${dir} (verify colours in the GUI: \`bambu slice open ${outFile}\`).`);
    } catch (err) {
      console.error(`warning: could not scaffold record: ${(err as Error).message}`);
    }
  }

  console.log(`colour check is a GUI step: \`bambu slice open ${outFile}\` — the headless slice cannot read per-region colour (see docs/issues/coaster-3mf-filament-shape-and-export-hang.md §4).`);
}

/** Slice a TAG-STRIPPED copy of the assembled members headless and assert exit 0 + the expected object
 *  count. The versioned Application tag is rewritten to bare `BambuStudio` (headless-safe); no
 *  `--export-3mf` (it hangs the headless build). Returns true on a clean geometry slice. */
async function verifyGeometry(
  studioBin: string,
  members: ReturnType<typeof buildThreeMfMembers>,
  coasters: AssemblyCoaster[],
  settingsName: string,
  filamentName: string,
  opts: CoasterOpts,
  scratch: string,
): Promise<boolean> {
  const strippedPath = join(scratch, "verify.3mf");
  writeThreeMf(stripApplicationTag(members), strippedPath, join(scratch, "verify-asm"));
  const outDir = join(scratch, "verify-out");
  mkdirSync(outDir, { recursive: true });
  // --load-settings takes preset FILE PATHS, not display names (the CLI does a filename lookup, not a
  // registry lookup — a bare "0.20mm Standard @BBL X2D" fails with "can not find setting file"). Resolve
  // the manifest's display names to their system-profile JSON paths, exactly as `slice compose` does.
  let loadSettings: string;
  try {
    const settingsPaths = resolvePresetList(settingsName, "settings", studioBin);
    const filamentPath = resolvePresetList(filamentName, "filament", studioBin);
    loadSettings = `${settingsPaths};${filamentPath}`;
  } catch (err) {
    console.error(`geometry verify: ${(err as Error).message}`);
    return false;
  }
  // The pivot doc's honest headless command: --load-settings <paths>, --slice 0, NO --export-3mf.
  const args = ["--debug", "2", "--load-settings", loadSettings, "--slice", "0", strippedPath, "--outputdir", outDir];
  const timeoutMs = Math.max(30, Number(opts.timeout) || 300) * 1000;
  ev("coaster_verify_start", { objects: coasters.length });
  const res = await runWithTimeout(studioBin, args, { timeoutMs, label: "studio_verify" });
  if (res.timedOut) {
    console.error(`geometry verify timed out after ${opts.timeout}s.`);
    return false;
  }
  if (res.code !== 0) {
    const tail = (res.stderr || res.stdout).trim().split("\n").slice(-8).join("\n");
    console.error(`geometry verify: slicer exited ${res.code ?? "null"} (tag-stripped copy).`);
    if (tail) console.error(tail);
    return false;
  }
  // result.json (written by --debug 2) records the objects the slicer actually loaded. Colour is NOT
  // checked here (§4: --load-settings overrides the embedded filament arrays); only geometry.
  const resultPath = join(outDir, "result.json");
  if (existsSync(resultPath)) {
    try {
      const result = JSON.parse(readFileSync(resultPath, "utf8")) as {
        sliced_plates?: Array<{ objects?: unknown[] }>;
      };
      const loaded = result.sliced_plates?.[0]?.objects?.length ?? 0;
      ev("coaster_verify_done", { loaded, expected: coasters.length });
      console.log(`geometry verify: PASS — sliced clean headless, ${loaded} object(s) loaded (tag-stripped copy; colour is a GUI check).`);
      return true;
    } catch {
      /* result.json unreadable — fall through to the exit-code-only verdict */
    }
  }
  console.log("geometry verify: PASS — sliced clean headless (tag-stripped copy; colour is a GUI check).");
  return true;
}

/** Attach the `coaster` subcommand to the `slice` command group. */
export function registerCoaster(slice: Command): void {
  slice
    .command("coaster <plate.yaml>")
    .description("assemble a multi-filament COLOUR plate (bikar --format parts → per-region AMS 3MF) for the X2D")
    .option("-o, --out <file>", "output filename (default: <manifest>.plate.3mf)")
    .option("-d, --outputdir <dir>", "output directory (default: current dir)")
    .option("-s, --settings <names|paths>", "machine + process, semicolon-joined — overrides the manifest profile")
    .option("-f, --filament <name|path>", "the plate's default (slot-1) filament — overrides the manifest profile")
    .option("--bed <name>", "bed footprint for the fit pre-check (x2d = 256×256 mm)", "x2d")
    .option("--pinch <strategy>", "how a coaster pinch is split: fillet|merge|error (bikar --format parts)", "fillet")
    .option("--max-slots <n>", "AMS capacity to cap the logical slot count at (default one unit, 4)")
    .option("--no-verify-geometry", "skip the headless tag-stripped geometry slice")
    .option("--no-record", "skip scaffolding the draft plate record")
    .option("-t, --timeout <seconds>", "geometry-verify slice timeout in seconds", "300")
    .option("--dry-run", "render + map + pre-check + print the plan, but do not assemble or verify", false)
    .action(async (manifest: string, opts: CoasterOpts) => {
      await runCoaster(manifest, opts);
    });
}
