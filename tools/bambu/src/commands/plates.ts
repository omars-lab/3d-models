// `bambu plates by-color` — one plate recipe per color for a loose coaster (piece colors phase 1,
// infill-color-ux-design §4.5). Each group of pieces prints in its palette color unless `--color`
// says otherwise; groups of one color share a plate, and the frame rides on the plate of its color,
// or gets its own. The recipes are the same writer `bambu order plan` uses, for one coaster.

import { Command } from "commander";
import { join, resolve } from "node:path";
import { type Demand, type PlateColor, constructionStem, groupByColor, normalHex, slug, writeRecipes } from "../by-color.js";
import { bikarDir } from "../backends/bikar.js";
import { asBikarSource, fetchGroups, writeRecipeFiles } from "../order-io.js";
import { repoRoot } from "../paths.js";

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
}

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
    const what = r.plate.items.map((it) => (it.piece ? `${it.piece} ×${it.count * (groups.find((g) => g.piece === it.piece)?.members ?? 1)}` : `frame ×${it.count}`));
    console.log(`  ${r.plate.color.hex}  ${r.name}.yaml  ${what.join(", ")}`);
  }
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
    .action(async (file: string, opts: ByColorOpts) => {
      try {
        await runByColor(file, opts);
      } catch (e) {
        console.error(String((e as Error).message));
        process.exitCode = 1;
      }
    });
}
