// `bambu slice sheet <sheet.yaml>` — a SAMPLER SHEET: one labeled card with 30 mm windows of real
// coasters standing on it, printed as ONE object (docs/design/coaster/sampler-sheets-design.md §5).
//
// `slice compose` cannot build it: `--arrange` moves loose pieces wherever they fit, which would scatter
// each sample away from the label engraved for it. `slice coaster` already builds one object out of
// several parts in one shared frame; a sheet is the same with a POSITION per part. So this verb:
//   1. renders the card (a bikar coupons piece with its engraved labels) and each sample (its coaster's
//      own file with `--window <side>@<x>,<y>`, bikar #293), every one with the mesh check on;
//   2. moves each sample so its window centre lands on its cell's `at:` and its base sits on the card's
//      top face — touching, not overlapping, so the parts fuse in the slice without a doubled volume;
//   3. refuses a sample that hangs off the card or crosses its neighbour (checkCells — the sheet's
//      validator, below);
//   4. assembles ONE object (card + samples as parts) through the coaster verb's 3MF assembler and
//      verifies it headless on a tag-stripped copy, exactly as `slice coaster` does.
//
// Every part prints in the plate's default filament (slot 1) today: sheets 1–3 are one color. Sheet 5's
// color samples (`--format parts` per window) are the next step, not this one.
//
// A sample's recipe goes through resolveManifestItems like any plate item, so its it-<sha12> carries the
// window and a sample reprinted from a sheet or a compose plate is the same recipe.

import { Command } from "commander";
import { createHash } from "node:crypto";
import { existsSync, mkdtempSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join, resolve } from "node:path";
import { parse as parseYaml } from "yaml";
import { runWithTimeout, ev } from "../log.js";
import { locateStudio, probeStudio } from "../backends/studio-cli.js";
import { locateBikarCli, bikarDir, bikarHead } from "../backends/bikar.js";
import {
  parseManifest,
  parseWindow,
  resolveBed,
  bedFitPrecheck,
  resolveManifestItems,
  itemRenderFlags,
  type Bed,
  type ManifestItemBkr,
  type PlateProfile,
  type ResolvedItem,
} from "./compose.js";
import { verifyGeometry } from "./coaster.js";
import { buildAmsSlotMap } from "../ams.js";
import { buildThreeMfMembers, writeThreeMf, type AssemblyCoaster } from "../threemf-assemble.js";
import { stlToIndexedMesh, footprint, type Bounds, type IndexedMesh } from "../mesh.js";
import { scaffoldRecord, type ScaffoldObject } from "../records.js";
import { platesDir, repoRoot } from "../paths.js";

// **Default:** slot 1 is Bambu PLA Basic / white, the same plate default `slice coaster` uses (D-075).
const DEFAULT_FILAMENT = { type: "PLA", id: "GFA00", hex: "#ffffff" };

// ── The sheet file ────────────────────────────────────────────────────────────────────────────────
// A card and its cells. A cell is a plate item that MUST be a window (a sample shrunk with `size` is
// the design's §5 FAIL case; a window is cut at the coaster's own scale) plus where it stands.
//
// A cell can instead name a window this repo VENDORS as an STL, for a sample bikar main can no longer
// draw: sheet 1's row A is the staircase edge #291 replaced, cut by a backport of #293's window that was
// never merged (src/Samplers/sheets-01-row-a/README.md has how it was made). Its sha256 is in the sheet
// file, so a changed file is refused rather than printed under the old label.

export interface VendoredSample {
  stl: string; // repo-relative path of the STL, cut at `window` in its coaster's own frame
  sha256: string; // the file's sha256 when the sheet was written
  window: string; // the window it was cut at — the placement anchor, as for a rendered sample
}
export type SheetCell = {
  name: string; // what the cell is, e.g. "B TRUE / CS-1" — the part name in the slicer
  at: [number, number]; // the cell centre in the card's frame (mm), the same numbers the card's labels use
} & ({ item: ManifestItemBkr; vendored?: undefined } | { vendored: VendoredSample; item?: undefined }); // bkr + piece + params + window, or a vendored STL

/** Check a vendored cell's own fields; the plate parser never sees it (it renders nothing). */
function parseVendored(c: Record<string, unknown>, where: string): VendoredSample {
  if (typeof c.stl !== "string" || !c.stl.trim() || c.stl.startsWith("/") || c.stl.split("/").includes("..")) {
    throw new Error(`${where}: \`stl:\` must be a path inside this repo, e.g. src/Samplers/<sheet>/<file>.stl`);
  }
  for (const k of ["bkr", "piece", "params", "iteration"]) {
    if (c[k] !== undefined) throw new Error(`${where}: a vendored \`stl:\` cell cannot also carry \`${k}:\` — it renders nothing`);
  }
  if (typeof c.sha256 !== "string" || !/^[0-9a-f]{64}$/.test(c.sha256)) {
    throw new Error(`${where}: a vendored \`stl:\` cell needs \`sha256:\` (64 lowercase hex) so a changed file is refused`);
  }
  const window = String(c.window);
  if (!parseWindow(window)) {
    throw new Error(`${where}: \`window:\` must be bikar's "<side>[@<x>,<y>]" (e.g. 30@9.7,1), got ${JSON.stringify(c.window)}`);
  }
  for (const k of Object.keys(c)) {
    if (!["stl", "sha256", "window"].includes(k)) throw new Error(`${where}: unknown field \`${k}:\` on a vendored cell`);
  }
  return { stl: c.stl.trim(), sha256: c.sha256, window };
}

/** The sha256 of a file's bytes. */
export function fileSha256(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}
export interface SheetManifest {
  bed?: string;
  profile?: PlateProfile;
  card: ManifestItemBkr;
  cells: SheetCell[];
}

/** Parse + validate a sheet file. The card and each cell are checked as ordinary plate items by
 *  `parseManifest` (one set of rules for bkr/piece/params/window), then the sheet's own fields. */
export function parseSheetManifest(text: string): SheetManifest {
  let doc: unknown;
  try {
    doc = parseYaml(text);
  } catch (err) {
    throw new Error(`sheet file is not valid YAML: ${(err as Error).message}`);
  }
  if (!doc || typeof doc !== "object") throw new Error("sheet file is empty or not a mapping");
  const m = doc as Record<string, unknown>;
  if (!m.card || typeof m.card !== "object") {
    throw new Error("sheet file has no `card:` — the labeled card the samples stand on");
  }
  if ((m.card as Record<string, unknown>).window !== undefined) {
    throw new Error("`card:` cannot carry a window — the card is printed whole");
  }
  const cells = m.cells;
  if (!Array.isArray(cells) || cells.length === 0) {
    throw new Error("sheet file has no `cells:` — a card with nothing standing on it");
  }
  const items: Record<string, unknown>[] = [m.card as Record<string, unknown>];
  const itemCell: number[] = [-1]; // items[k] is cells[itemCell[k]] (the card is -1): vendored cells are not items
  const sheetFields: Array<{ name: string; at: [number, number]; vendored?: VendoredSample }> = [];
  cells.forEach((raw, i) => {
    const where = `cells[${i}]`;
    if (!raw || typeof raw !== "object") throw new Error(`${where} is not a mapping`);
    const c = { ...(raw as Record<string, unknown>) };
    if (typeof c.name !== "string" || !c.name.trim()) {
      throw new Error(`${where}: \`name:\` must say what the cell is (e.g. "B TRUE / CS-1")`);
    }
    const at = c.at;
    if (!Array.isArray(at) || at.length !== 2 || !at.every((v) => typeof v === "number" && Number.isFinite(v))) {
      throw new Error(`${where} (${c.name}): \`at:\` must be [x, y], the cell centre on the card in mm`);
    }
    if (c.window === undefined) {
      throw new Error(
        `${where} (${c.name}): a sample needs \`window:\` — it is cut from its coaster at the coaster's own ` +
          `scale; a whole piece or a shrunk coaster is not a true-size sample (sampler-sheets design §5)`,
      );
    }
    if (c.count !== undefined) throw new Error(`${where} (${c.name}): a cell is one sample; \`count:\` does not apply`);
    const name = c.name.trim();
    delete c.name;
    delete c.at;
    if (c.stl !== undefined) {
      sheetFields.push({ name, at: [at[0] as number, at[1] as number], vendored: parseVendored(c, `${where} (${name})`) });
      return;
    }
    sheetFields.push({ name, at: [at[0] as number, at[1] as number] });
    itemCell.push(i);
    items.push(c);
  });
  // One validator for the item fields: the plate parser's (window spelling, params as numbers, bkr form).
  let parsed;
  try {
    parsed = parseManifest(JSON.stringify({ items }));
  } catch (err) {
    // parseManifest names items[k]; say it in the sheet's terms.
    throw new Error(sheetTerms((err as Error).message, itemCell));
  }
  const [card, ...cellItems] = parsed.items as ManifestItemBkr[];
  if (typeof m.bed !== "undefined" && typeof m.bed !== "string") throw new Error("`bed:` must be a bed name");
  let k = 0;
  return {
    bed: m.bed as string | undefined,
    profile: (m.profile as PlateProfile) ?? undefined,
    card: card!,
    cells: sheetFields.map((f): SheetCell =>
      f.vendored ? { name: f.name, at: f.at, vendored: f.vendored } : { name: f.name, at: f.at, item: cellItems[k++]! },
    ),
  };
}

/** Rename a plate-parser `items[k]` to the sheet's `card` or `cells[i]`. */
function sheetTerms(message: string, itemCell: number[]): string {
  return message.replace(/^items\[(\d+)\]/, (_, n: string) => {
    const cell = itemCell[Number(n)];
    return cell === undefined || cell < 0 ? "card" : `cells[${cell}]`;
  });
}

// ── Placement ─────────────────────────────────────────────────────────────────────────────────────

/** Move a mesh by (dx, dy, dz). Pure: returns a new mesh, the triangles shared. */
export function translateMesh(mesh: IndexedMesh, dx: number, dy: number, dz: number): IndexedMesh {
  const v = mesh.vertices.slice();
  for (let i = 0; i < v.length; i += 3) {
    v[i] = v[i]! + dx;
    v[i + 1] = v[i + 1]! + dy;
    v[i + 2] = v[i + 2]! + dz;
  }
  return { vertices: v, triangles: mesh.triangles };
}

/** The axis-aligned bounds of an indexed mesh. */
export function meshBounds(mesh: IndexedMesh): Bounds {
  const v = mesh.vertices;
  const min: [number, number, number] = [Infinity, Infinity, Infinity];
  const max: [number, number, number] = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < v.length; i += 3) {
    for (let a = 0; a < 3; a++) {
      const x = v[i + a]!;
      if (x < min[a]!) min[a] = x;
      if (x > max[a]!) max[a] = x;
    }
  }
  return { min, max };
}

/** Stand a window sample on its cell: its WINDOW CENTRE (in the coaster's own frame, where bikar leaves
 *  the cut) moves to `at`, and its lowest point to the card's top `cardTop`. The window centre, not the
 *  mesh's bounding box, is the anchor: a window whose art stops short of one edge has a smaller box,
 *  and centring the box would shift the sample off the spot its label names. */
export function placeSample(mesh: IndexedMesh, window: string, at: [number, number], cardTop: number): IndexedMesh {
  const w = parseWindow(window);
  if (!w) throw new Error(`not a window: ${JSON.stringify(window)}`);
  const zMin = meshBounds(mesh).min[2];
  return translateMesh(mesh, at[0] - w.x, at[1] - w.y, cardTop - zMin);
}

/**
 * **Validator:** every placed sample stands wholly on the card and clear of every other sample. The
 * check is per sample and per pair, on the placed meshes' own bounds — never one union box, since a
 * union can sit inside the card while one sample hangs off it.
 *
 * PASS: sheet 1's six samples (30 mm windows at x = -20, 14, 48 and y = -10, -44 on a 138 × 122 card)
 * lie inside the card with 4 mm between neighbours.
 *
 * FAIL: a sample at x = 60 on that card spans 45..75 and passes the card's right edge at 69; two
 * samples 20 mm apart overlap by 10 mm.
 */
export function checkCells(
  card: Bounds,
  samples: Array<{ name: string; bounds: Bounds }>,
): string[] {
  const out: string[] = [];
  const EPS = 1e-6;
  for (const s of samples) {
    const b = s.bounds;
    if (b.min[0] < card.min[0] - EPS || b.max[0] > card.max[0] + EPS || b.min[1] < card.min[1] - EPS || b.max[1] > card.max[1] + EPS) {
      out.push(
        `${s.name}: spans x ${fmt(b.min[0])}..${fmt(b.max[0])}, y ${fmt(b.min[1])}..${fmt(b.max[1])}, off the card ` +
          `(x ${fmt(card.min[0])}..${fmt(card.max[0])}, y ${fmt(card.min[1])}..${fmt(card.max[1])})`,
      );
    }
  }
  for (let i = 0; i < samples.length; i++) {
    for (let j = i + 1; j < samples.length; j++) {
      const a = samples[i]!.bounds;
      const b = samples[j]!.bounds;
      const ox = Math.min(a.max[0], b.max[0]) - Math.max(a.min[0], b.min[0]);
      const oy = Math.min(a.max[1], b.max[1]) - Math.max(a.min[1], b.min[1]);
      if (ox > EPS && oy > EPS) {
        out.push(`${samples[i]!.name} and ${samples[j]!.name} overlap by ${fmt(ox)} × ${fmt(oy)} mm`);
      }
    }
  }
  return out;
}

function fmt(n: number): string {
  return String(Math.round(n * 100) / 100);
}

/** The one plate object: the card first, then each sample, every part in slot 1 (one color today). */
export function assembleSheet(
  sheetName: string,
  card: IndexedMesh,
  samples: Array<{ name: string; mesh: IndexedMesh }>,
): AssemblyCoaster {
  return {
    name: sheetName,
    bodies: [
      { region: "card", name: "card", extruder: 1, mesh: card },
      ...samples.map((s, i) => ({ region: `cell-${i + 1}`, name: s.name, extruder: 1, mesh: s.mesh })),
    ],
  };
}

// ── The verb ──────────────────────────────────────────────────────────────────────────────────────

/** The card and its placed samples as one binary STL, the way the plate will stand — for `print_review.py`. */
export function sheetStl(meshes: IndexedMesh[]): Buffer {
  const count = meshes.reduce((n, m) => n + m.triangles.length / 3, 0);
  const buf = Buffer.alloc(84 + 50 * count);
  buf.writeUInt32LE(count, 80);
  let o = 84;
  for (const m of meshes) {
    const v = m.vertices;
    for (let t = 0; t < m.triangles.length; t += 3) {
      o += 12; // normal left zero: readers recompute it from the winding
      for (let k = 0; k < 3; k++) {
        const i = m.triangles[t + k]! * 3;
        buf.writeFloatLE(v[i]!, o);
        buf.writeFloatLE(v[i + 1]!, o + 4);
        buf.writeFloatLE(v[i + 2]!, o + 8);
        o += 12;
      }
      o += 2;
    }
  }
  return buf;
}

interface SheetOpts {
  out?: string;
  stl?: string;
  outputdir?: string;
  settings?: string;
  filament?: string;
  bed?: string;
  timeout: string;
  verifyGeometry: boolean;
  dryRun?: boolean;
  record?: boolean;
}

/** Render one resolved item to STL with the mesh check on; throw with bikar's own words on a FAIL. */
async function renderChecked(r: ResolvedItem, bikarCli: string, stl: string): Promise<void> {
  const args = [bikarCli, "render", resolve(bikarDir(), r.sourcePath), "--format", "stl", "--check", "-o", stl];
  args.push(...itemRenderFlags(r));
  const res = await runWithTimeout("node", args, { timeoutMs: 180_000, label: "bikar_render_sheet" });
  if (res.code !== 0 || res.timedOut || !existsSync(stl)) {
    const tail = (res.stderr || res.stdout || "").trim().split("\n").slice(-6).join("\n");
    throw new Error(`bikar render --check failed for ${r.sourcePath}${r.window ? ` window ${r.window}` : ""}:\n${tail}`);
  }
}

async function runSheet(sheetPath: string, opts: SheetOpts): Promise<void> {
  const abs = resolve(sheetPath);
  if (!existsSync(abs)) {
    console.error(`no such sheet file: ${sheetPath}`);
    process.exitCode = 1;
    return;
  }
  let sheet: SheetManifest;
  try {
    sheet = parseSheetManifest(readFileSync(abs, "utf8"));
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 2;
    return;
  }
  const settingsName = opts.settings ?? sheet.profile?.settings;
  const filamentName = opts.filament ?? sheet.profile?.filament;
  if (!settingsName || !filamentName) {
    console.error("a sheet needs one slice profile — set `profile.settings` + `profile.filament`, or pass -s and -f.");
    process.exitCode = 2;
    return;
  }
  let bed: Bed;
  try {
    bed = resolveBed(opts.bed ?? sheet.bed ?? "x2d");
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 2;
    return;
  }
  const bikarCli = locateBikarCli();
  if (!bikarCli) {
    console.error(`bikar CLI not built at ${bikarDir()}/packages/cli/dist/index.js — build bikar, or set BIKAR_DIR.`);
    process.exitCode = 1;
    return;
  }
  const bikarRef = await bikarHead();
  if (!bikarRef) {
    console.error(`could not read bikar HEAD at ${bikarDir()} — is it a git checkout?`);
    process.exitCode = 1;
    return;
  }

  // 1. Resolve the card and every rendered sample to geometry pins + iteration ids (the window is in the
  //    key); check every vendored sample's file against the sha256 the sheet was written with.
  const rendered = sheet.cells.flatMap((c, i) => (c.item ? [{ cell: i, item: c.item }] : []));
  const itemCell = [-1, ...rendered.map((r) => r.cell)];
  let resolved: ResolvedItem[];
  try {
    resolved = await resolveManifestItems([sheet.card, ...rendered.map((r) => r.item)], bikarRef, {
      settings: settingsName,
      filament: filamentName,
    });
  } catch (err) {
    console.error(sheetTerms((err as Error).message, itemCell));
    process.exitCode = 2;
    return;
  }
  const [cardItem, ...renderedItems] = resolved;
  const root = repoRoot(dirname(abs)); // the sheet file's own repo, wherever the verb runs from
  const vendoredProblems = sheet.cells.flatMap((c, i) => {
    if (!c.vendored) return [];
    const path = root ? join(root, c.vendored.stl) : c.vendored.stl;
    if (!existsSync(path)) return [`cells[${i}] (${c.name}): no such file ${c.vendored.stl}`];
    const sha = fileSha256(path);
    return sha === c.vendored.sha256
      ? []
      : [`cells[${i}] (${c.name}): ${c.vendored.stl} has sha256 ${sha}, not the ${c.vendored.sha256} the sheet was written with`];
  });
  if (vendoredProblems.length > 0) {
    for (const p of vendoredProblems) console.error(p);
    process.exitCode = 2;
    return;
  }
  // Per cell: where its STL is, its window, and its recipe for the record.
  const cellSource = (i: number): { stl: string; window: string; iteration?: string } => {
    const c = sheet.cells[i]!;
    if (c.vendored) return { stl: root ? join(root, c.vendored.stl) : c.vendored.stl, window: c.vendored.window };
    const r = renderedItems[rendered.findIndex((x) => x.cell === i)]!;
    return { stl: stlOf(r), window: r.window, iteration: r.iteration };
  };

  // 2. Render the card and each rendered sample with the mesh check on. A vendored sample passed the same
  //    check when it was made (its README); the assembled plate's headless slice covers it here.
  const scratch = mkdtempSync(join(tmpdir(), "bambu-sheet-"));
  const stlOf = (r: ResolvedItem): string => join(scratch, `${r.iteration}.stl`);
  try {
    const done = new Set<string>();
    for (const r of resolved) {
      if (done.has(r.iteration)) continue;
      await renderChecked(r, bikarCli, stlOf(r));
      done.add(r.iteration);
    }
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 1;
    return;
  }

  // 3. Place each sample on its cell, on the card's top face, and check the layout.
  const cardMesh = stlToIndexedMesh(stlOf(cardItem!));
  const cardBounds = meshBounds(cardMesh);
  const cardTop = cardBounds.max[2];
  const sources = sheet.cells.map((_, i) => cellSource(i));
  const samples = sheet.cells.map((c, i) => {
    const mesh = placeSample(stlToIndexedMesh(sources[i]!.stl), sources[i]!.window, c.at, cardTop);
    return { name: c.name, mesh, bounds: meshBounds(mesh) };
  });
  const problems = checkCells(cardBounds, samples);
  const [fx, fy] = footprint(cardBounds);
  const fit = bedFitPrecheck([{ entry: "card", x: fx, y: fy, count: 1 }], bed);

  const sheetName = basename(abs).replace(/\.ya?ml$/i, "");
  const outDir = opts.outputdir ? resolve(opts.outputdir) : platesDir();
  const outFile = opts.out ?? `${sheetName}.plate.3mf`;
  const outPath = join(outDir, outFile);

  console.log(`sheet ${sheetName}: card ${fmt(fx)} × ${fmt(fy)} mm, top at z ${fmt(cardTop)}, ${samples.length} sample(s), bed ${bed.label}`);
  for (const [i, s] of samples.entries()) {
    const b = s.bounds;
    const src = sources[i]!;
    console.log(
      `  ${s.name}: window ${src.window} → x ${fmt(b.min[0])}..${fmt(b.max[0])}, ` +
        `y ${fmt(b.min[1])}..${fmt(b.max[1])}, z ${fmt(b.min[2])}..${fmt(b.max[2])} ` +
        `(${src.iteration ?? `vendored ${sheet.cells[i]!.vendored!.stl}`})`,
    );
  }
  console.log(`layout check: ${problems.length === 0 ? "PASS — every sample on the card, none touching another" : "FAIL"}`);
  for (const p of problems) console.log(`  ✗ ${p}`);
  console.log(`bed-fit pre-check: ${fit.ok ? "PASS" : "FAIL"}`);
  for (const f of fit.failures) console.log(`  ✗ ${f}`);
  if (opts.stl) {
    // Written before the checks stop the run, so a FAIL can be looked at too.
    writeFileSync(resolve(opts.stl), sheetStl([cardMesh, ...samples.map((s) => s.mesh)]));
    console.log(`sheet as one STL → ${opts.stl} (look: python3 tools/print_review.py art <out.png> ${opts.stl})`);
  }
  if (problems.length > 0 || !fit.ok) {
    process.exitCode = 1;
    return;
  }
  if (opts.dryRun) {
    console.log(`would assemble → ${outPath} (one object: the card + ${samples.length} sample part(s), all slot 1)`);
    console.log(opts.verifyGeometry ? "would then verify geometry headless on a tag-stripped copy." : "geometry verify: skipped (--no-verify-geometry).");
    return;
  }

  // 4. Assemble the one object and write the 3MF (the coaster verb's assembler, slot 1 for every part).
  const coaster = assembleSheet(sheetName, cardMesh, samples);
  const map = buildAmsSlotMap(
    [{ coaster: sheetName, pinch: "", parts: coaster.bodies.map((b) => ({ region: b.region, stl: "", triangles: 0, paletteName: null, hex: null })) }],
    { defaultFilament: filamentName },
  );
  const probe = await probeStudio();
  const studioVersion = probe.version?.match(/(\d+\.\d+\.\d+\.\d+)/)?.[1] ?? "02.08.02.61";
  const members = buildThreeMfMembers([coaster], map, DEFAULT_FILAMENT, `BambuStudio-${studioVersion}`);
  mkdirSync(outDir, { recursive: true });
  ev("sheet_assemble", { sheet: sheetName, samples: samples.length });
  try {
    writeThreeMf(members, outPath, join(scratch, "asm"));
  } catch (err) {
    console.error(`assembly failed: ${(err as Error).message}`);
    process.exitCode = 1;
    return;
  }
  console.log(`assembled → ${outPath} (${Math.round(statSync(outPath).size / 1024)} KB, one object, ${coaster.bodies.length} parts)`);

  // 5. Verify geometry headless, as `slice coaster` does.
  if (opts.verifyGeometry) {
    const studioBin = locateStudio();
    if (!studioBin) {
      console.log("geometry verify: skipped — no headless BambuStudio found (install it or --no-verify-geometry).");
    } else if (!(await verifyGeometry(studioBin, members, [coaster], settingsName, filamentName, opts.timeout, scratch))) {
      console.error("geometry verify FAILED — the assembled sheet did not slice clean headless (tag-stripped).");
      process.exitCode = 1;
      return;
    }
  }

  // 6. A draft record (gitignored) with every part's recipe id; never dispatches.
  if (opts.record !== false) {
    const fromItem = (entry: string, r: ResolvedItem): ScaffoldObject => ({
      entry,
      source: r.sourceAtRef,
      piece: r.piece || undefined,
      params: r.params,
      window: r.window || undefined,
      iteration: r.iteration,
    });
    const objects: ScaffoldObject[] = [
      fromItem("card", cardItem!),
      ...sheet.cells.map((c, i): ScaffoldObject => {
        if (!c.vendored) return fromItem(c.name, renderedItems[rendered.findIndex((x) => x.cell === i)]!);
        // A vendored sample has no bikar source or recipe id: its source is the file, pinned by its hash.
        return { entry: c.name, source: `3d-models:${c.vendored.stl}`, sourceSha256: c.vendored.sha256, window: c.vendored.window };
      }),
    ];
    try {
      const dir = await scaffoldRecord({ slug: sheetName, plateName: outFile, plateFile: outPath, objects, via: "bambu slice sheet" });
      console.log(`draft record → ${dir}`);
    } catch (err) {
      console.error(`warning: could not scaffold record: ${(err as Error).message}`);
    }
  }
  console.log(`look before sending: \`bambu slice open ${outPath}\` shows each sample on its label.`);
}

/** Attach the `sheet` subcommand to the `slice` command group. */
export function registerSheet(slice: Command): void {
  slice
    .command("sheet <sheet.yaml>")
    .description("assemble a sampler sheet: a labeled card with coaster windows standing on their cells, one object")
    .option("-o, --out <file>", "output filename (default: <sheet>.plate.3mf)")
    .option("-d, --outputdir <dir>", "output directory (default: build/plates at the repo root)")
    .option("--stl <file>", "also write the card + placed samples as one STL to look at (works with --dry-run)")
    .option("-s, --settings <names|paths>", "machine + process, semicolon-joined — overrides the sheet's profile")
    .option("-f, --filament <name|path>", "the filament — overrides the sheet's profile")
    .option("--bed <name>", "bed footprint for the fit pre-check (x2d = 256×256 mm)")
    .option("--no-verify-geometry", "skip the headless tag-stripped geometry slice")
    .option("--no-record", "skip scaffolding the draft plate record")
    .option("-t, --timeout <seconds>", "geometry-verify slice timeout in seconds", "300")
    .option("--dry-run", "render + place + check + print the plan, but do not assemble or verify", false)
    .action(async (sheetPath: string, opts: SheetOpts) => {
      await runSheet(sheetPath, opts);
    });
}
