// `bambu status` — read-only view of the printer over first-party MQTT (D-055).
//   show    : one-shot status (temps, progress, print state)
//   monitor : poll status on an interval
//   camera  : capture a chamber snapshot (needs ffmpeg on X1/H2-class)
//
// This is the Phase-1 proof of transport: it reaches the printer WITHOUT sending anything that moves
// the machine (a `pushing.pushall` status request only), so we can trust the pipe before any dispatch
// verb. The transport is our own MqttBackend, not a spawned MCP — see backends/mqtt.ts for why.

import { Command } from "commander";
import { MqttBackend, type PrinterStatus } from "../backends/mqtt.js";
import { McpBackend } from "../backends/mcp.js";

function requireConfigured(b: { configured(): boolean }): void {
  if (!b.configured()) {
    console.error("Not configured. Set PRINTER_HOST / BAMBU_SERIAL / BAMBU_TOKEN (or .mcp.json).");
    console.error("Run `bambu setup doctor` to see what's missing.");
    process.exit(1);
  }
}

/** First scalar found among candidate keys, else undefined. Bambu reports drift field names by model. */
function pick(s: PrinterStatus, ...keys: string[]): unknown {
  for (const k of keys) if (s[k] !== undefined && s[k] !== null) return s[k];
  return undefined;
}

function fmtTemp(cur: unknown, target: unknown): string | null {
  if (cur === undefined) return null;
  const t = target !== undefined && Number(target) > 0 ? ` → ${target}°C` : "";
  return `${cur}°C${t}`;
}

/** Human summary of the interesting fields; falls back to a note when the report is empty. */
function renderStatus(s: PrinterStatus): string {
  const age = s._age_seconds;
  if (age === null || age === undefined) {
    return "No report received yet (the printer sent nothing on device/<serial>/report within the wait window).";
  }
  const lines: string[] = [];
  const state = pick(s, "gcode_state");
  if (state !== undefined) lines.push(`state:     ${state}`);
  const nozzle = fmtTemp(pick(s, "nozzle_temper"), pick(s, "nozzle_target_temper"));
  if (nozzle) lines.push(`nozzle:    ${nozzle}`);
  const bed = fmtTemp(pick(s, "bed_temper"), pick(s, "bed_target_temper"));
  if (bed) lines.push(`bed:       ${bed}`);
  const chamber = pick(s, "chamber_temper");
  if (chamber !== undefined) lines.push(`chamber:   ${chamber}°C`);
  const pct = pick(s, "mc_percent");
  const layer = pick(s, "layer_num");
  const total = pick(s, "total_layer_num");
  if (pct !== undefined) {
    const layers = layer !== undefined && total !== undefined ? `  layer ${layer}/${total}` : "";
    lines.push(`progress:  ${pct}%${layers}`);
  }
  const remain = pick(s, "mc_remaining_time");
  if (remain !== undefined) lines.push(`remaining: ${remain} min`);
  const task = pick(s, "subtask_name");
  if (task) lines.push(`job:       ${task}`);
  const err = pick(s, "print_error");
  if (err !== undefined && Number(err) !== 0) lines.push(`ERROR:     print_error=${err}`);

  const header = lines.length
    ? lines.join("\n")
    : "(connected; report received but no known fields present — use --json)";
  return `${header}\n\n(report age ${age}s; --json for the full frame)`;
}

export function registerStatus(program: Command): void {
  const status = program.command("status").description("read-only printer status (proves transport)");

  status
    .command("show")
    .description("one-shot printer status over first-party MQTT")
    .option("--json", "print the raw report frame instead of a summary")
    .action(async (opts: { json?: boolean }) => {
      const mqtt = new MqttBackend();
      requireConfigured(mqtt);
      try {
        await mqtt.connect();
        const s = await mqtt.requestStatus();
        console.log(opts.json ? JSON.stringify(s, null, 2) : renderStatus(s));
      } catch (err) {
        console.error(`status failed: ${(err as Error).message}`);
        process.exitCode = 1;
      } finally {
        await mqtt.close();
      }
    });

  status
    .command("monitor")
    .description("poll status on an interval (Ctrl+C to stop)")
    .option("-i, --interval <seconds>", "seconds between polls", "10")
    .option("--json", "print the raw report frame instead of a summary")
    .action(async (opts: { interval: string; json?: boolean }) => {
      const mqtt = new MqttBackend();
      requireConfigured(mqtt);
      const intervalMs = Math.max(2, Number(opts.interval) || 10) * 1000;
      let stop = false;
      process.on("SIGINT", () => {
        stop = true;
      });
      try {
        await mqtt.connect();
        while (!stop) {
          console.log(`\n--- ${new Date().toISOString()} ---`);
          const s = await mqtt.requestStatus();
          console.log(opts.json ? JSON.stringify(s, null, 2) : renderStatus(s));
          if (!stop) await new Promise((r) => setTimeout(r, intervalMs));
        }
      } catch (err) {
        console.error(`monitor failed: ${(err as Error).message}`);
        process.exitCode = 1;
      } finally {
        await mqtt.close();
      }
    });

  // Camera stays on the MCP transport for now: a chamber snapshot is an RTSP/ffmpeg pull, a separate
  // capability from the MQTT status/control channel. It rides the first-party path in a later PR.
  status
    .command("camera")
    .description("capture a chamber snapshot (needs ffmpeg) — via the MCP transport")
    .option("-o, --out <path>", "output JPEG path", "chamber.jpg")
    .action(async (opts: { out: string }) => {
      const mcp = new McpBackend();
      requireConfigured(mcp);
      try {
        await mcp.connect();
        const tool = (await mcp.findTool("camera")) ?? (await mcp.findTool("snapshot"));
        if (!tool) throw new Error("no camera tool exposed by the MCP");
        const res = (await mcp.call(tool, { path: opts.out })) as {
          content?: Array<{ type?: string; text?: string }>;
        };
        console.log(
          res?.content?.length
            ? res.content.map((c) => (c.type === "text" && c.text ? c.text : JSON.stringify(c))).join("\n")
            : JSON.stringify(res, null, 2),
        );
      } catch (err) {
        console.error(`camera failed: ${(err as Error).message}`);
        process.exitCode = 1;
      } finally {
        await mcp.close();
      }
    });
}
