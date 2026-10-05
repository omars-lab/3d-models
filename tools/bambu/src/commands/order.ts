// `bambu order` — an order file in, its plates out (order-driven-lab-design §9, phase 1).
//   plan <order.yaml>  : one recipe per color, each plate's beds, minutes and grams from its slice,
//                        the minutes corrected by past prints, and the order's total
//   timed              : the prints the correction rests on (watched against sliced minutes)
//   fixtures           : the regression suite (§9.6): each fixture order planned and checked against
//                        its expected plan, and its wrong plan refused for the reason it names
//
// An order file names no person and stays out of this repo (it is public). The planner never sends:
// a plate it writes is a recipe with no page and no approval.

import { Command } from "commander";
import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { parse as parseYaml } from "yaml";
import { slug } from "../by-color.js";
import { canonicalJson } from "../iteration.js";
import {
  type ColorPick,
  type Order,
  type Plan,
  type SliceFacts,
  checkPlan,
  lookupColor,
  parseOrder,
  planOrder,
} from "../order.js";
import { fetchGroups, loadCatalog, loadNotes, sliceRecipe, writeRecipeFiles } from "../order-io.js";
import { repoRoot } from "../paths.js";
import { type TimedRun, readTimedRuns } from "../timed-prints.js";

const FIXTURES = "tools/bambu/test/fixtures/orders";

function root(): string {
  const r = repoRoot();
  if (!r) throw new Error("could not find the repo root (.claude/gates); run from inside the 3d-models repo");
  return r;
}

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

/** Everything a plan and its check read besides the order itself. */
async function depsFor(order: Order, slices: Record<string, SliceFacts>, runs: TimedRun[], extraPlans: Plan[] = []) {
  const r = root();
  const catalog = loadCatalog(r);
  const notes = loadNotes(r);
  const pairs = [
    ...order.lines.flatMap((l) => (l.pieces ? [{ construction: l.pieces.construction, params: l.pieces.params }] : [])),
    ...extraPlans.flatMap((p) => p.plates.flatMap((pl) => pl.items.filter((it) => it.piece !== null))),
  ];
  const groupsOf = await fetchGroups(pairs);
  return { color: (c: ColorPick) => lookupColor(catalog, notes, c), groupsOf, slices, runs };
}

interface PlanOpts {
  outDir?: string;
  slice?: boolean;
  slices?: string;
  prints?: string;
  json?: boolean;
}

async function runPlan(orderFile: string, opts: PlanOpts): Promise<void> {
  const order = parseOrder(readFileSync(resolve(orderFile), "utf8"));
  const out = resolve(opts.outDir ?? join(root(), "build", "orders", slug(order.id)));
  const slices: Record<string, SliceFacts> = opts.slices ? readJson(resolve(opts.slices)) : {};
  const runs: TimedRun[] = opts.prints ? readJson(resolve(opts.prints)) : readTimedRuns(join(root(), "docs/design/plates")).runs;
  const deps = await depsFor(order, slices, runs);

  let { plan, recipes } = planOrder(order, deps);
  const paths = writeRecipeFiles(out, recipes);
  if (opts.slice) {
    for (const [i, r] of recipes.entries()) {
      if (slices[r.hash]) continue;
      if (!opts.json) console.error(`slicing ${r.name} …`);
      slices[r.hash] = await sliceRecipe(paths[i]!, r.name, out);
    }
    writeFileSync(join(out, "slices.json"), JSON.stringify(slices, null, 2) + "\n");
    ({ plan, recipes } = planOrder(order, deps));
  }
  writeFileSync(join(out, "plan.json"), JSON.stringify(plan, null, 2) + "\n");

  // The plan is checked the way a fixture's is: one that fails its own check is a bug, not a plan.
  const errors = checkPlan(order, plan, deps);
  if (opts.json) {
    console.log(JSON.stringify(plan, null, 2));
  } else {
    printPlan(plan, out);
  }
  if (errors.length) {
    console.error(`\nthe plan fails its own check (a bug in the planner):\n  ${errors.join("\n  ")}`);
    process.exitCode = 1;
  }
}

function printPlan(plan: Plan, out: string): void {
  console.log(`order ${plan.order}: ${plan.total.plates} plate(s), recipes in ${out}`);
  for (const p of plan.plates) {
    const c = p.color;
    const what = [c.line, c.name, c.code ? `(${c.code})` : null].filter(Boolean).join(" ");
    const numbers =
      p.source === "none"
        ? "not sliced (pass --slice, or --slices with a frozen file)"
        : `${p.beds} bed(s), ${p.sliced_minutes} min sliced → ` +
          (p.floor ? "floor (no timed print used this filament)" : `${p.minutes} min at ${p.ratio!.value}× over ${p.ratio!.prints} print(s)`) +
          `, ${p.grams} g`;
    console.log(`\n  ${p.name}  ${what}  ${c.hex}`);
    for (const it of p.items) console.log(`    ${String(it.count).padStart(3)} × ${it.piece ? `${it.piece} set` : "frame"}  ${it.construction.replace(/^bikar:.*\//, "")}`);
    console.log(`    ${numbers}`);
    if (p.nearest_unused) console.log(`    nearest ratio not used: ${p.nearest_unused.value}× (${p.nearest_unused.why})`);
    if (c.note) console.log(`    note: ${c.code} ${c.note}`);
    if (!p.sendable && p.why_not) console.log(`    not sendable: ${p.why_not}`);
  }
  const t = plan.total;
  console.log(
    `\n  total: ${t.plates} plate(s), ${t.beds ?? "?"} bed(s), ${t.sliced_minutes ?? "?"} min sliced, ` +
      `${t.floor ? "corrected minutes unknown (a plate is floor)" : `${t.minutes ?? "?"} min corrected`}, ${t.grams ?? "?"} g`,
  );
  for (const n of plan.notes) console.log(`  · ${n}`);
}

function runTimed(opts: { json?: boolean }): void {
  const { runs, skipped } = readTimedRuns(join(root(), "docs/design/plates"));
  if (opts.json) {
    console.log(JSON.stringify(runs, null, 2));
    return;
  }
  for (const r of runs) console.log(`${r.plate.padEnd(14)} ${r.started}  ${r.watched}/${r.sliced} min  ${r.filament}`);
  for (const s of skipped) console.log(`  skipped ${s}`);
}

// ── the regression suite ────────────────────────────────────────────────────────────────────────────

// The last phase whose command exists (design §9.6 "Which phase builds which part"). A fixture of a
// later phase waits; raising this when a phase lands runs its fixtures, so none stays waiting by
// being forgotten.
const SHIPPED_PHASE = 1;

interface FixtureMeta {
  phase: number;
  about: string;
  wrong_must_say?: string;
}

interface FixturesOpts {
  dir?: string;
  writeExpected?: boolean;
  slice?: boolean;
}

async function runFixtures(opts: FixturesOpts): Promise<void> {
  const dir = resolve(opts.dir ?? join(root(), FIXTURES));
  const runs: TimedRun[] = readJson(join(dir, "prints.json"));
  const slices: Record<string, SliceFacts> = existsSync(join(dir, "slices.json")) ? readJson(join(dir, "slices.json")) : {};
  const used = new Set<string>();
  let failed = 0;
  const fixtures = readdirSync(dir, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name).sort();
  for (const name of fixtures) {
    const fx = join(dir, name);
    const meta = parseYaml(readFileSync(join(fx, "fixture.yaml"), "utf8")) as FixtureMeta;
    if (meta.phase > SHIPPED_PHASE) {
      console.log(`· ${name}: waiting on phase ${meta.phase}`);
      continue;
    }
    const problems: string[] = [];
    try {
      const order = parseOrder(readFileSync(join(fx, "order.yaml"), "utf8"));
      const wrong: Plan | null = existsSync(join(fx, "wrong-plan.json")) ? readJson(join(fx, "wrong-plan.json")) : null;
      const deps = await depsFor(order, slices, runs, wrong ? [wrong] : []);
      let { plan, recipes } = planOrder(order, deps);
      if (opts.slice) {
        // A fixture's numbers are real slices, frozen so the suite runs without the slicer; --slice
        // makes the ones a changed fixture is missing, here rather than merged in by hand.
        const out = join(root(), "build", "orders", "fixtures", name);
        const paths = writeRecipeFiles(out, recipes);
        for (const [i, r] of recipes.entries()) {
          if (slices[r.hash]) continue;
          console.error(`slicing ${r.name} …`);
          slices[r.hash] = await sliceRecipe(paths[i]!, r.name, out);
        }
        ({ plan, recipes } = planOrder(order, deps));
      }
      for (const r of recipes) used.add(r.hash);
      if (opts.writeExpected) writeFileSync(join(fx, "expected-plan.json"), JSON.stringify(plan, null, 2) + "\n");
      if (!existsSync(join(fx, "expected-plan.json"))) problems.push("no expected-plan.json");
      else if (canonicalJson(plan) !== canonicalJson(readJson(join(fx, "expected-plan.json")))) {
        problems.push("the plan differs from expected-plan.json (run `bambu order plan` on it and diff)");
      }
      problems.push(...checkPlan(order, plan, deps).map((e) => `its own plan fails the check: ${e}`));
      if (!wrong || !meta.wrong_must_say) problems.push("no wrong-plan.json, or no wrong_must_say in fixture.yaml");
      else {
        const said = checkPlan(order, wrong, deps);
        if (!said.some((e) => e.includes(meta.wrong_must_say!))) {
          problems.push(`the wrong plan was not refused for "${meta.wrong_must_say}"; the check said: ${said.join("; ") || "nothing"}`);
        }
      }
    } catch (e) {
      problems.push(String((e as Error).message));
    }
    if (problems.length) {
      failed++;
      console.log(`✗ ${name}: ${meta.about}\n    ${problems.join("\n    ")}`);
    } else {
      console.log(`✓ ${name}: ${meta.about}`);
    }
  }
  if (opts.slice) {
    // Only the slices some fixture still plans are kept, so an edited fixture leaves no stale numbers.
    const kept = Object.fromEntries(Object.entries(slices).filter(([hash]) => used.has(hash)).sort(([a], [b]) => a.localeCompare(b)));
    writeFileSync(join(dir, "slices.json"), JSON.stringify(kept, null, 2) + "\n");
    console.log(`slices.json: ${Object.keys(kept).length} slice(s) kept`);
  }
  if (failed) process.exitCode = 1;
}

export function registerOrder(program: Command): void {
  const order = program.command("order").description("plan an order: plates by color, beds, minutes, grams (order-driven-lab-design §9)");

  order
    .command("plan <order.yaml>")
    .description("write one plate recipe per color for an order, with each plate's beds, minutes and grams and the order total")
    .option("-o, --out-dir <dir>", "where the recipes and plan.json go (default: build/orders/<order id>)")
    .option("--slice", "slice each recipe now (bambu slice compose) and write slices.json beside the plan", false)
    .option("--slices <file>", "read slices frozen earlier (a slices.json, keyed by recipe hash)")
    .option("--prints <file>", "read timed prints frozen earlier (`bambu order timed --json`) instead of the print logs")
    .option("--json", "print the plan as JSON", false)
    .action(async (file: string, opts: PlanOpts) => {
      try {
        await runPlan(file, opts);
      } catch (e) {
        console.error(String((e as Error).message));
        process.exitCode = 1;
      }
    });

  order
    .command("timed")
    .description("the prints watched from start to finish, against their sliced minutes: what a plan's correction rests on")
    .option("--json", "print the runs as JSON (the shape --prints reads)", false)
    .action((opts: { json?: boolean }) => runTimed(opts));

  order
    .command("fixtures")
    .description("run the order regression suite: every fixture planned, checked, and its wrong plan refused")
    .option("--dir <dir>", `the fixtures folder (default: ${FIXTURES})`)
    .option("--write-expected", "overwrite each expected-plan.json with today's plan (then check every one by hand)", false)
    .option("--slice", "slice each fixture recipe slices.json lacks, and rewrite slices.json with only the slices in use", false)
    .action(async (opts: FixturesOpts) => runFixtures(opts));
}
