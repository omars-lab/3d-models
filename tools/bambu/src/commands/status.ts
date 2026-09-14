// `bambu status` — read-only view of the printer via the griches MCP.
//   show    : one-shot status (temps, progress, AMS)
//   monitor : poll status on an interval
//   camera  : capture a chamber snapshot (needs ffmpeg on X1/H2-class)
//
// This is the Phase-1 proof of transport: it reaches the printer WITHOUT sending anything, so we
// can trust the pipe before any dispatch verb exists.

import { Command } from "commander";
import { McpBackend } from "../backends/mcp.js";

function requireConfigured(mcp: McpBackend): void {
  if (!mcp.configured()) {
    console.error("Not configured. Set PRINTER_HOST / BAMBU_SERIAL / BAMBU_TOKEN (or .mcp.json).");
    console.error("Run `bambu setup doctor` to see what's missing.");
    process.exit(1);
  }
}

/** Pull readable text out of an MCP tool result's content array. */
function renderResult(result: unknown): string {
  const r = result as { content?: Array<{ type?: string; text?: string }> };
  if (r?.content?.length) {
    return r.content
      .map((c) => (c.type === "text" && c.text ? c.text : JSON.stringify(c)))
      .join("\n");
  }
  return JSON.stringify(result, null, 2);
}

async function fetchStatus(mcp: McpBackend): Promise<string> {
  await mcp.connect();
  const tool = (await mcp.findTool("status")) ?? (await mcp.findTool("get", "state"));
  if (!tool) {
    const tools = (await mcp.listTools()).map((t) => t.name).join(", ");
    throw new Error(`no status-like tool found. Available: ${tools}`);
  }
  return renderResult(await mcp.call(tool));
}

export function registerStatus(program: Command): void {
  const status = program.command("status").description("read-only printer status (proves transport)");

  status
    .command("show")
    .description("one-shot printer status via the griches MCP")
    .action(async () => {
      const mcp = new McpBackend();
      requireConfigured(mcp);
      try {
        console.log(await fetchStatus(mcp));
      } catch (err) {
        console.error(`status failed: ${(err as Error).message}`);
        process.exitCode = 1;
      } finally {
        await mcp.close();
      }
    });

  status
    .command("monitor")
    .description("poll status on an interval (Ctrl+C to stop)")
    .option("-i, --interval <seconds>", "seconds between polls", "10")
    .action(async (opts: { interval: string }) => {
      const mcp = new McpBackend();
      requireConfigured(mcp);
      const intervalMs = Math.max(2, Number(opts.interval) || 10) * 1000;
      let stop = false;
      process.on("SIGINT", () => {
        stop = true;
      });
      try {
        while (!stop) {
          console.log(`\n--- ${new Date().toISOString()} ---`);
          console.log(await fetchStatus(mcp));
          await new Promise((r) => setTimeout(r, intervalMs));
        }
      } catch (err) {
        console.error(`monitor failed: ${(err as Error).message}`);
        process.exitCode = 1;
      } finally {
        await mcp.close();
      }
    });

  status
    .command("camera")
    .description("capture a chamber snapshot (needs ffmpeg)")
    .option("-o, --out <path>", "output JPEG path", "chamber.jpg")
    .action(async (opts: { out: string }) => {
      const mcp = new McpBackend();
      requireConfigured(mcp);
      try {
        await mcp.connect();
        const tool = (await mcp.findTool("camera")) ?? (await mcp.findTool("snapshot"));
        if (!tool) throw new Error("no camera tool exposed by the MCP");
        const res = await mcp.call(tool, { path: opts.out });
        console.log(renderResult(res));
      } catch (err) {
        console.error(`camera failed: ${(err as Error).message}`);
        process.exitCode = 1;
      } finally {
        await mcp.close();
      }
    });
}
