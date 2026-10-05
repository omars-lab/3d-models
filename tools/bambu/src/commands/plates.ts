// `bambu plates by-color` — one plate recipe per color for a loose coaster (piece colors phase 1,
// infill-color-ux-design §4.5). Each group of pieces prints in its palette color unless `--color`
// says otherwise; groups of one color share a plate, and the frame rides on the plate of its color,
// or gets its own. The recipes are the same writer `bambu order plan` uses, for one coaster.
//
// `--costs` (piece colors phase 2, §6) adds what each way of printing that coloring costs: one plate
// per color, the whole set once per color, and one plate swapping colors. It writes the whole-set
// recipe too, slices what `--slice` asks for, and writes costs.json and costs.html beside the recipes.

import { Command } from "commander";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { parse as parseYaml } from "yaml";
import {
  type Demand,
  type PlateColor,
  type PlateItem,
  type WrittenRecipe,
  PLATE_SETTINGS,
  constructionStem,
  groupByColor,
  normalHex,
  slug,
  writeRecipes,
} from "../by-color.js";
import { type Costs, type Prices, type Tier, TIERS, costRoutes } from "../by-color-costs.js";
import { costsPage } from "../by-color-page.js";
import { bikarDir } from "../backends/bikar.js";
import type { SliceFacts } from "../order.js";
import { asBikarSource, fetchGroups, sliceRecipe, writeRecipeFiles } from "../order-io.js";
import { repoRoot } from "../paths.js";
import { copyMember } from "../threemf.js";
import { type TimedRun, ratioFor, readTimedRuns } from "../timed-prints.js";

interface ByColorOpts {
  param: string[];
  color: string[];
  frame?: string;
  frameParam: string[];
  frameColor?: string;
  count: string;
  outDir?: string;
  name?: string;
  json?: boolean;
  costs?: boolean;
  slice?: boolean;
  slices?: string;
  prints?: string;
  prices?: string;
  priceTier: string;
}

const PRICES = "docs/design/coaster/themes/catalog/prices.yaml";

const collect = (v: string, acc: string[]) => [...acc, v];

function parseParams(list: string[], flag: string): Record<string, number> {
  const out: Record<string, number> = {};
  for (const kv of list) {
    const m = /^([A-Za-z_]\w*)=(-?\d+(?:\.\d+)?)$/.exec(kv);
    if (!m) throw new Error(`${flag} ${kv}: expected name=number`);
    out[m[1]!] = Number(m[2]);
  }
  return out;
}

function hexColor(hex: string): PlateColor {
  return { key: hex, hex, line: "PLA Basic", code: null, name: null, note: null };
}

async function runByColor(piecesArg: string, opts: ByColorOpts): Promise<void> {
  const pieces = asBikarSource(piecesArg);
  const params = parseParams(opts.param, "--param");
  const count = Number(opts.count);
  if (!Number.isInteger(count) || count < 1) throw new Error(`--count ${opts.count}: a whole number, 1 or more`);
  const groups = (await fetchGroups([{ construction: pieces, params }]))(pieces, params);

  const overrides = new Map<string, string>();
  for (const c of opts.color) {
    const m = /^([A-Za-z_]\w*)=(#?[0-9A-Fa-f]{6})$/.exec(c);
    const hex = m ? normalHex(m[2]!) : null;
    if (!m || !hex) throw new Error(`--color ${c}: expected Name=#rrggbb`);
    if (!groups.some((g) => g.piece === m[1])) throw new Error(`--color ${c}: no group named ${m[1]} (its groups: ${groups.map((g) => g.piece).join(", ")})`);
    overrides.set(m[1]!, hex);
  }

  const demands: Demand[] = [];
  if (opts.frame) {
    const hex = opts.frameColor ? normalHex(opts.frameColor) : null;
    if (!hex) throw new Error("--frame needs --frame-color #rrggbb: the coaster has no palette color of its own");
    demands.push({ construction: asBikarSource(opts.frame), params: parseParams(opts.frameParam, "--frame-param"), piece: null, count, rank: -1, color: hexColor(hex) });
  }
  for (const g of groups) {
    const hex = overrides.get(g.piece) ?? g.hex;
    if (!hex) throw new Error(`${g.piece}: the .bkr palette gives it no color; pass --color ${g.piece}=#rrggbb`);
    demands.push({ construction: pieces, params, piece: g.piece, count, rank: Math.min(...g.orbits), color: hexColor(hex) });
  }

  const name = opts.name ?? slug(`${constructionStem(pieces)}-by-color`);
  const recipes = writeRecipes(
    groupByColor(demands),
    name,
    [
      `Written by \`bambu plates by-color\` from ${pieces.replace(/^bikar:/, "")}: every group of one color on one plate,`,
      "so each plate prints from one spool (piece colors phase 1). Slice it with `bambu slice compose`.",
    ],
    (it) => (it.piece ? (groups.find((g) => g.piece === it.piece)?.members ?? null) : 1),
  );
  const out = resolve(opts.outDir ?? join(repoRoot() ?? process.cwd(), "build", "plates", "by-color", name));
  const paths = writeRecipeFiles(out, recipes);
  const pieceCount = (it: PlateItem) => (it.piece ? (groups.find((g) => g.piece === it.piece)?.members ?? 1) : 1);

  if (opts.costs) {
    await runCosts(name, out, recipes, paths, demands, pieceCount, count, opts);
    return;
  }
  if (opts.json) {
    console.log(
      JSON.stringify(
        recipes.map((r, i) => ({ name: r.name, path: paths[i], recipe_hash: r.hash, color: r.plate.color.hex, items: r.plate.items.map(({ rank: _, ...it }) => it) })),
        null,
        2,
      ),
    );
    return;
  }
  console.log(`${recipes.length} plate(s) from ${pieces.replace(/^bikar:/, "")} (bikar at ${bikarDir()}), in ${out}`);
  for (const r of recipes) {
    const what = r.plate.items.map((it) => (it.piece ? `${it.piece} ×${it.count * pieceCount(it)}` : `frame ×${it.count}`));
    console.log(`  ${r.plate.color.hex}  ${r.name}.yaml  ${what.join(", ")}`);
  }
}

/** The cost view: the whole-set recipe beside the per-color ones, their slices, the three routes. */
async function runCosts(
  name: string,
  out: string,
  recipes: WrittenRecipe[],
  paths: string[],
  demands: Demand[],
  pieceCount: (it: PlateItem) => number,
  coasters: number,
  opts: ByColorOpts,
): Promise<void> {
  const tier = opts.priceTier as Tier;
  if (!TIERS.includes(tier)) throw new Error(`--price-tier ${opts.priceTier}: one of ${TIERS.join(", ")}`);
  const root = repoRoot();
  const pricesPath = resolve(opts.prices ?? join(root ?? process.cwd(), PRICES));
  if (!existsSync(pricesPath)) throw new Error(`no price file at ${pricesPath} (pass --prices)`);
  const prices = parseYaml(readFileSync(pricesPath, "utf8")) as Prices;
  const runs: TimedRun[] = opts.prints
    ? (JSON.parse(readFileSync(resolve(opts.prints), "utf8")) as TimedRun[])
    : root
      ? readTimedRuns(join(root, "docs/design/plates")).runs
      : [];

  // Every item on one plate, in the first plate's color: the slicer's time does not depend on it.
  const first = recipes[0]!.plate.color;
  const [whole] = writeRecipes(
    groupByColor(demands.map((d) => ({ ...d, color: first }))),
    `${name}-whole-set`,
    [
      "Written by `bambu plates by-color --costs`: the whole set on one plate, so the cost view can price",
      "printing it once per color, or once in every color with AMS swaps. Not a plate to send as is.",
    ],
    pieceCount,
  );
  const [wholePath] = writeRecipeFiles(out, [whole!]);
  const all = [...recipes, whole!];
  const allPaths = [...paths, wholePath!];

  const slicesPath = join(out, "slices.json");
  const slices: Record<string, SliceFacts> = opts.slices
    ? JSON.parse(readFileSync(resolve(opts.slices), "utf8"))
    : existsSync(slicesPath)
      ? JSON.parse(readFileSync(slicesPath, "utf8"))
      : {};
  if (opts.slice) {
    for (const [i, r] of all.entries()) {
      if (slices[r.hash]) continue;
      if (!opts.json) console.error(`slicing ${r.name} …`);
      slices[r.hash] = await sliceRecipe(allPaths[i]!, r.name, out);
    }
    writeFileSync(slicesPath, JSON.stringify(slices, null, 2) + "\n");
  }

  const costs = costRoutes({
    coasters,
    perColor: recipes.map((r) => ({ recipe: r, slice: slices[r.hash] ?? null })),
    wholeSet: { recipe: whole!, slice: slices[whole!.hash] ?? null },
    pieceCount,
    prices,
    tier,
    ratio: (filament) => {
      const r = ratioFor(runs, PLATE_SETTINGS, filament);
      return r ? { value: r.value, prints: r.prints.length } : null;
    },
  });
  writeFileSync(join(out, "costs.json"), JSON.stringify(costs, null, 2) + "\n");

  // Each slice's top view, one per bed, inline in the page.
  const pictures: Record<string, string[]> = {};
  for (const r of all) {
    const threemf = join(out, `${r.name}.plate.3mf`);
    const beds = slices[r.hash]?.beds ?? 0;
    if (!existsSync(threemf) || beds === 0) continue;
    pictures[r.name] = [];
    for (let b = 1; b <= beds; b++) {
      const png = await copyMember(threemf, `Metadata/top_${b}.png`, join(out, `${r.name}.top-${b}.png`));
      if (png) pictures[r.name]!.push(`data:image/png;base64,${readFileSync(png).toString("base64")}`);
    }
  }
  const html = join(out, "costs.html");
  writeFileSync(html, costsPage(costs, pictures, `${constructionStem(recipes[0]!.plate.items[0]!.construction)}: what each way of printing costs`));

  if (opts.json) console.log(JSON.stringify(costs, null, 2));
  else printCosts(costs, out, html);
}

function printCosts(costs: Costs, out: string, html: string): void {
  const min = (n: number | null) => (n === null ? "?" : `${n} min`);
  const usd = (n: number | null) => (n === null ? "$?" : `$${n.toFixed(2)}`);
  console.log(`${costs.coasters} coaster(s), ${costs.colors.length} color(s); recipes, costs.json and the page in ${out}`);
  for (const r of costs.routes) {
    console.log(`\n  ${r.title} — ${r.status}`);
    for (const p of r.plates) {
      const beds = p.bed_minutes && p.bed_minutes.length > 1 ? ` (${p.bed_minutes.map((m, i) => `bed ${i + 1} ${m} min`).join(", ")})` : "";
      const swaps = p.swaps ? ` incl. ${p.swaps} swaps` : "";
      console.log(
        `    ${p.colors.map((c) => c.hex).join("+")}  ${p.name}  ${min(p.minutes)}${swaps}${beds}, ${p.grams ?? "?"} g, ${usd(p.usd)}  [${p.source}]`,
      );
      for (const n of p.notes) console.log(`      · ${n}`);
    }
    const t = r.total;
    console.log(
      `    total: ${t.sends ?? "?"} send(s), ${min(t.minutes)}, ${t.grams ?? "?"} g, ${usd(t.usd)}; ` +
        `per coaster ${min(r.per_coaster.minutes)}, ${usd(r.per_coaster.usd)}; left over: ${r.left_over}`,
    );
  }
  for (const n of costs.notes) console.log(`  · ${n}`);
  console.log(`\n  page: ${html}`);
}

export function registerPlates(program: Command): void {
  const plates = program.command("plates").description("write plate recipes from a construction (piece colors, infill-color-ux-design §4.5)");
  plates
    .command("by-color <pieces.bkr>")
    .description("one plate recipe per color for a loose coaster's pieces (and its frame), each group in its palette color or --color's")
    .option("--param <name=value>", "a param of the pieces construction (repeatable)", collect, [])
    .option("--color <Name=#rrggbb>", "print this group in this color instead of its palette's (repeatable)", collect, [])
    .option("--frame <coaster.bkr>", "the coaster the pieces drop into, printed too")
    .option("--frame-param <name=value>", "a param of the frame construction (repeatable)", collect, [])
    .option("--frame-color <#rrggbb>", "the frame's color (required with --frame)")
    .option("--count <n>", "how many coasters' worth", "1")
    .option("-o, --out-dir <dir>", "where the recipes go (default: build/plates/by-color/<name>)")
    .option("--name <name>", "the recipes' name prefix (default: <construction>-by-color)")
    .option("--json", "print the plates as JSON", false)
    .option("--costs", "price each way of printing it (per color, whole set per color, one plate swapping) into costs.json and costs.html", false)
    .option("--slice", "with --costs: slice every recipe that has no slice yet (minutes and grams from the slicer)", false)
    .option("--slices <file>", "with --costs: a frozen slices.json to read instead of the one in the out dir")
    .option("--prints <file>", "with --costs: timed prints (JSON) instead of the plate print logs")
    .option("--prices <file>", `with --costs: the price file (default: ${PRICES})`)
    .option("--price-tier <tier>", `with --costs: ${TIERS.join(", ")}`, "refill")
    .action(async (file: string, opts: ByColorOpts) => {
      try {
        await runByColor(file, opts);
      } catch (e) {
        console.error(String((e as Error).message));
        process.exitCode = 1;
      }
    });
}
