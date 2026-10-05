// `bambu shelf` — the spools on hand, what the open orders hold, and what to buy
// (order-driven-lab-design §9.2, phase 2).
//   show [shelf.yaml] : each spool's grams left, each color's on hand, held and available, the buy
//                       list, and how each print in the logs was counted
//
// The shelf file names its spools and its orders' plans. Where it lives is call 1 (#196, open), so
// the default is a gitignored local file, `.bambu/shelf/shelf.yaml`: an order names no person in
// this public repo, and neither does the shelf that holds it.

import { Command } from "commander";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import type { Plan } from "../order.js";
import { loadCatalog, loadNotes } from "../order-io.js";
import { repoRoot } from "../paths.js";
import { type ShelfInputs, type ShelfReport, parseShelf, shelfReport } from "../shelf.js";
import { logRows } from "../timed-prints.js";

export const SHELF = ".bambu/shelf/shelf.yaml";
export const PRINT_LOGS = "docs/design/plates/print-logs";

function root(): string {
  const r = repoRoot();
  if (!r) throw new Error("could not find the repo root (.claude/gates); run from inside the 3d-models repo");
  return r;
}

/** A shelf file and everything it points at: its plans, the print logs, the catalog and notes.
 *  The logs folder is `--logs`, else the file's `logs:`, else `defaultLogs` (none when null). */
export function readShelf(file: string, opts: { logs?: string; defaultLogs: string | null }): ShelfInputs {
  const r = root();
  const at = dirname(resolve(file));
  const shelf = parseShelf(readFileSync(resolve(file), "utf8"));
  const orders = shelf.orders.map((o) => ({ status: o.status, plan: JSON.parse(readFileSync(resolve(at, o.plan), "utf8")) as Plan }));
  const logsDir = opts.logs ? resolve(opts.logs) : shelf.logs ? resolve(at, shelf.logs) : opts.defaultLogs;
  const logs =
    logsDir && existsSync(logsDir)
      ? readdirSync(logsDir)
          .filter((f) => f.endsWith(".md"))
          .sort()
          .map((f) => ({ plate: basename(f, ".md"), rows: logRows(readFileSync(join(logsDir, f), "utf8")) }))
      : [];
  return { shelf, orders, logs, catalog: loadCatalog(r), notes: loadNotes(r) };
}

const g = (n: number | null) => (n === null ? "unknown" : `${n} g`);

function printShelf(rep: ShelfReport): void {
  console.log("spools");
  for (const s of rep.spools) {
    const corr = s.corrections_grams ? ` ${s.corrections_grams > 0 ? "+" : "−"} ${Math.abs(s.corrections_grams)} corrected` : "";
    const tag = s.tag_percent === null ? "" : `  (tag says ${s.tag_percent}%)`;
    console.log(`  ${s.id.padEnd(12)} ${`${s.line} ${s.code} ${s.name}`.padEnd(30)} ${s.start_grams} g${corr} − ${s.used_grams} used = ${s.on_hand} g${tag}`);
  }
  console.log("\ncolors");
  for (const c of rep.colors) {
    console.log(`  ${`${c.line} ${c.code} ${c.name}`.padEnd(30)} on hand ${g(c.on_hand)}, held ${g(c.held)}, available ${g(c.available)}`);
    for (const h of c.held_by) console.log(`      held by ${h.order} ${h.plate}: ${g(h.grams)}`);
    if (c.held === null) console.log("      a plate has no grams yet (slice it), so what is held is unknown");
  }
  console.log("\nbuy");
  if (!rep.buy.length) console.log("  nothing: every color the open orders need is on hand");
  for (const b of rep.buy) console.log(`  ${b.line} ${b.code} ${b.name}: ${b.spools} spool(s), ${b.short_grams} g short${b.note ? `  (${b.note})` : ""}`);
  const list = (title: string, rows: string[]) => {
    if (!rows.length) return;
    console.log(`\n${title}`);
    for (const r of rows) console.log(`  ${r}`);
  };
  list("prints counted", rep.closed.map((c) => `${c.plate} sent ${c.sent}, ${c.event} ${c.ended}: ${c.grams} g off ${c.spool}`));
  list("sends not closed yet", rep.not_closed.map((u) => `${u.plate} ${u.time}: ${u.why}`));
  list("trays with no spool (not counted)", rep.unmatched.map((u) => `${u.plate} sent ${u.sent}, ${u.hex} from ${u.tray}, ${u.grams} g: ${u.why}`));
  list("prints not counted", rep.uncounted.map((u) => `${u.plate} ${u.time}: ${u.why}`));
}

export function registerShelf(program: Command): void {
  const shelf = program.command("shelf").description("spools on hand, what open orders hold, and what to buy (order-driven-lab-design §9.2)");
  shelf
    .command("show [shelf.yaml]")
    .description(`each spool's grams left, each color's on hand, held and available, and the buy list (default: ${SHELF})`)
    .option("--logs <dir>", `the print logs to close prints from (default: the shelf file's logs:, else ${PRINT_LOGS})`)
    .option("--json", "print the shelf as JSON", false)
    .action((file: string | undefined, opts: { logs?: string; json?: boolean }) => {
      try {
        const path = file ?? join(root(), SHELF);
        if (!existsSync(path)) throw new Error(`no shelf file at ${path}; write one (spools and orders, see order-driven-lab-design §9.2)`);
        const rep = shelfReport(readShelf(path, { logs: opts.logs, defaultLogs: join(root(), PRINT_LOGS) }));
        if (opts.json) console.log(JSON.stringify(rep, null, 2));
        else printShelf(rep);
      } catch (e) {
        console.error(String((e as Error).message));
        process.exitCode = 1;
      }
    });
}
