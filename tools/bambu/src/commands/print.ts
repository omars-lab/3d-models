// `bambu print` — dispatch + print control via the griches MCP.
//   send <plate.3mf> [--record] : upload a sliced .3mf and start it (OWNER-GATED, confirm-before-send)
//   pause | resume | stop        : control the running print (stop confirms)
//
// Dispatch is the one verb that moves real hardware, and printing is on hold until a CAL bet
// justifies a plate (memory: owner-gated-and-on-hold). So `send` is fail-closed: it refuses unless
// the operator passes --yes or confirms at a TTY, and --dry-run shows exactly what it WOULD do
// without connecting. Tool names are matched by hint (griches may rename them / the X2D may differ),
// so a missing tool degrades to a clear error, never a crash.

import { Command } from "commander";
import { existsSync, statSync, readFileSync } from "node:fs";
import { basename, extname, resolve } from "node:path";
import { McpBackend } from "../backends/mcp.js";
import { MqttBackend, type PrinterStatus } from "../backends/mqtt.js";
import { confirm } from "../prompt.js";
import { scaffoldRecord, type ScaffoldObject } from "../records.js";
import { readPlateMeta } from "../threemf.js";
import { buildHeader, headerToRecordProfile, type RecordProfile } from "../header.js";
import { runPrintList } from "./print-list.js";
import { ev } from "../log.js";

function requireConfigured(mcp: McpBackend): void {
  if (!mcp.configured()) {
    console.error("Not configured. Set PRINTER_HOST / BAMBU_SERIAL / BAMBU_TOKEN (or .mcp.json).");
    console.error("Run `bambu setup doctor` to see what's missing.");
    process.exit(1);
  }
}

function renderResult(result: unknown): string {
  const r = result as { content?: Array<{ type?: string; text?: string }> };
  if (r?.content?.length) {
    return r.content.map((c) => (c.type === "text" && c.text ? c.text : JSON.stringify(c))).join("\n");
  }
  return JSON.stringify(result, null, 2);
}

interface SendOpts {
  record?: boolean;
  yes?: boolean;
  dryRun?: boolean;
  slug?: string;
  object?: string[]; // --object bikar:<path>[=entry], repeatable
}

/** Parse a repeated --object "bikar:path" or "bikar:path=ENTRY" into scaffold objects. */
function parseObjects(specs: string[] | undefined): ScaffoldObject[] {
  if (!specs || specs.length === 0) {
    // No provenance given — one placeholder object so the scaffold is well-formed and the gate can
    // point at exactly what's missing.
    return [{ entry: "obj-1", source: `bikar:TODO` }];
  }
  return specs.map((spec, i) => {
    const [src = "TODO", entry] = spec.split("=");
    return { entry: entry ?? `obj-${i + 1}`, source: src.startsWith("bikar:") ? src : `bikar:${src}` };
  });
}

/**
 * Pre-fill the record's profile header from the SAME builder `bambu header` uses (D-052: one code
 * path). The .3mf being dispatched IS the `--plate`, so machine/nozzle/layer/profile/slicer come off
 * it; the printer-side material/chamber come from a best-effort MQTT read. Every step is best-effort:
 * a missing printer or an unreadable frame degrades to the plain TODO scaffold, never a crash — and
 * never a fabricated field (the builder leaves unconfirmed/manual fields out of the record profile).
 */
async function buildRecordProfile(plateFile: string): Promise<RecordProfile | undefined> {
  try {
    const plateMeta = await readPlateMeta(plateFile);
    let frame: PrinterStatus = {};
    const mqtt = new MqttBackend();
    if (mqtt.configured()) {
      try {
        await mqtt.connect();
        frame = await mqtt.requestStatus();
      } catch {
        /* printer unreachable — fill only the slice-side fields from the .3mf */
      } finally {
        await mqtt.close();
      }
    }
    return headerToRecordProfile(buildHeader(frame, plateMeta));
  } catch {
    return undefined; // fall back to the TODO scaffold
  }
}

async function runSend(plate: string, opts: SendOpts): Promise<void> {
  const abs = resolve(plate);
  if (!existsSync(abs)) {
    console.error(`no such file: ${plate}`);
    process.exitCode = 1;
    return;
  }
  if (extname(abs).toLowerCase() !== ".3mf") {
    console.error(`dispatch expects a sliced .3mf, got '${extname(abs)}'. Slice first: bambu slice plate <model>`);
    process.exitCode = 2;
    return;
  }

  const kb = Math.round(statSync(abs).size / 1024);
  const mcp = new McpBackend();
  requireConfigured(mcp);

  // Owner gate, stated out loud before anything reaches the printer.
  console.error("⚠ Dispatch is owner-gated: this sends a plate to the physical X2D.");
  console.error(`  plate: ${basename(abs)} (${kb} KB) → ${mcp.config.host ?? "(host unset)"}`);
  console.error("  Printing is on hold until a CAL bet justifies a plate (see the setup skill).");

  if (opts.dryRun) {
    console.log("dry run — would upload the .3mf and start a print via the MCP (no send performed).");
    if (opts.record) console.log("would also scaffold a draft record under .bambu/records/.");
    return;
  }

  if (!(await confirm("Send this plate to the printer now?", Boolean(opts.yes)))) {
    console.error("refused — not sending. Pass --yes (or confirm at a TTY) to dispatch.");
    process.exitCode = 2;
    return;
  }

  try {
    await mcp.connect();
    // Upload the file, then start the print. Both tool names are hint-matched.
    const uploadTool = (await mcp.findTool("upload")) ?? (await mcp.findTool("send", "file"));
    const printTool =
      (await mcp.findTool("print", "start")) ?? (await mcp.findTool("start", "print")) ?? (await mcp.findTool("print"));
    if (!printTool) {
      const tools = (await mcp.listTools()).map((t) => t.name).join(", ");
      throw new Error(`no print/dispatch tool found. Available: ${tools}`);
    }
    ev("dispatch_start", { plate: basename(abs), kb });
    if (uploadTool) {
      const data = readFileSync(abs).toString("base64");
      console.log(renderResult(await mcp.call(uploadTool, { name: basename(abs), data })));
    }
    console.log(renderResult(await mcp.call(printTool, { file: basename(abs), name: basename(abs) })));
    ev("dispatch_done", { plate: basename(abs) });
    console.log(`dispatched ${basename(abs)}.`);
  } catch (err) {
    console.error(`dispatch failed: ${(err as Error).message}`);
    process.exitCode = 1;
  } finally {
    await mcp.close();
  }

  if (opts.record) {
    try {
      const slug = opts.slug ?? basename(abs, ".3mf").replace(/[^a-z0-9]+/gi, "-").toLowerCase();
      const profile = await buildRecordProfile(abs);
      const dir = await scaffoldRecord({
        slug,
        plateName: basename(abs, ".3mf"),
        plateFile: abs,
        objects: parseObjects(opts.object),
        profile,
      });
      console.log(`scaffolded draft record → ${dir}`);
      console.log("Fill the TODOs + photos, then `bambu validate record .bambu/records` before moving it to docs/prints/.");
    } catch (err) {
      console.error(`record scaffold failed: ${(err as Error).message}`);
      process.exitCode = 1;
    }
  }
}

/** Shared body for pause/resume/stop. `stop` confirms first; pause/resume are reversible. */
async function runControl(verb: "pause" | "resume" | "stop", opts: { yes?: boolean }): Promise<void> {
  if (verb === "stop" && !(await confirm("Stop the running print?", Boolean(opts.yes)))) {
    console.error("refused — not stopping. Pass --yes (or confirm at a TTY).");
    process.exitCode = 2;
    return;
  }
  const mcp = new McpBackend();
  requireConfigured(mcp);
  try {
    await mcp.connect();
    const tool = (await mcp.findTool(verb)) ?? (await mcp.findTool("print", verb));
    if (!tool) {
      const tools = (await mcp.listTools()).map((t) => t.name).join(", ");
      throw new Error(`no '${verb}' tool found. Available: ${tools}`);
    }
    ev(`${verb}_call`, {});
    console.log(renderResult(await mcp.call(tool)));
  } catch (err) {
    console.error(`${verb} failed: ${(err as Error).message}`);
    process.exitCode = 1;
  } finally {
    await mcp.close();
  }
}

export function registerPrint(program: Command): void {
  const print = program.command("print").description("dispatch + print control via the MCP (owner-gated)");

  print
    .command("send <plate>")
    .description("upload a sliced .3mf and start it — OWNER-GATED, confirm-before-send")
    .option("--record", "scaffold a draft print record under .bambu/records/", false)
    .option("--slug <slug>", "slug for the record run name (default: derived from the plate)")
    .option(
      "-O, --object <spec>",
      "printed object as bikar:<path>[=ENTRY] (repeatable) — pins R1 provenance in the record",
      (v: string, acc: string[]) => [...acc, v],
      [] as string[],
    )
    .option("-y, --yes", "skip the confirmation prompt (still logs the owner-gate notice)", false)
    .option("--dry-run", "show what would be sent without connecting or dispatching", false)
    .action(runSend);

  print
    .command("list")
    .description("list every print record — what came off the plate and (--how) how it was printed")
    .option("--shipped", "only the shipped docs/prints/ records", false)
    .option("--drafts", "only the gitignored .bambu/records/ drafts", false)
    .option("--how", "show the process identity (machine/material/nozzle/layer/profile) instead of outcome", false)
    .option("--settles <cal>", "only records settling a bet whose CAL id contains this (e.g. CAL-FIT)")
    .option("--material <m>", "only records printed in a material containing this (e.g. PLA)")
    .option("--machine <m>", "only records printed on a machine containing this (e.g. X2D)")
    .option("--status <s>", "only records at this exact lifecycle status (e.g. measured)")
    .option("--json", "emit the records as JSON instead of a table", false)
    .action(
      (opts: {
        shipped?: boolean;
        drafts?: boolean;
        how?: boolean;
        settles?: string;
        material?: string;
        machine?: string;
        status?: string;
        json?: boolean;
      }) => runPrintList(opts),
    );

  print
    .command("pause")
    .description("pause the running print")
    .action(() => runControl("pause", {}));
  print
    .command("resume")
    .description("resume the running print")
    .action(() => runControl("resume", {}));
  print
    .command("stop")
    .description("stop the running print (confirms first)")
    .option("-y, --yes", "skip the confirmation prompt", false)
    .action((opts: { yes?: boolean }) => runControl("stop", opts));
}
