// Backend: the griches Bambu MCP as transport.
//
// We act as an MCP *client* — spawn the griches server over stdio and call its tools. This is the
// same server Claude talks to, so the CLI and Claude drive the printer through one code path
// (robustness-over-ease tenet: one path, not two that can disagree).
//
// The griches tool NAMES are matched by hint rather than hard-coded, so a server update or an X2D
// model quirk that renames/omits a tool degrades to a clear error instead of a crash — and because
// none of the community servers list `x2d` in their model enums yet (verified 2026-09-13), we never
// assume a specific tool set.

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { ev } from "../log.js";
import { loadConfig, type PrinterConfig } from "../config.js";

export interface McpTool {
  name: string;
  description?: string;
}

export class McpBackend {
  private client: Client | null = null;
  readonly config: PrinterConfig;

  constructor(config: PrinterConfig = loadConfig()) {
    this.config = config;
  }

  /** True when we have enough config to even attempt a connection. */
  configured(): boolean {
    return Boolean(this.config.host && this.config.serial && this.config.token);
  }

  /** Spawn + connect the griches server. Command overridable via BAMBU_MCP_CMD for a local checkout. */
  async connect(timeoutMs = 20_000): Promise<void> {
    if (this.client) return;
    const cmd = process.env.BAMBU_MCP_CMD ?? "npx";
    const args = process.env.BAMBU_MCP_ARGS
      ? process.env.BAMBU_MCP_ARGS.split(" ")
      : ["-y", "@griches/bambu-mcp"];
    ev("mcp_connect_start", { cmd, args: `"${args.join(" ")}"` });
    // Narrow the child's environment (D-055 hardening): pass only what npx/node need to launch
    // (PATH, HOME, plus proxy vars if set) and the four printer vars — NOT the whole process.env.
    // Under `dotenvx run` the parent env carries every decrypted secret; a transport server has no
    // business seeing anything but the printer config it connects with.
    const passthrough: Record<string, string> = {};
    for (const k of ["PATH", "HOME", "TMPDIR", "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "npm_config_cache"]) {
      const v = process.env[k];
      if (v) passthrough[k] = v;
    }
    const transport = new StdioClientTransport({
      command: cmd,
      args,
      env: {
        ...passthrough,
        PRINTER_HOST: this.config.host ?? "",
        BAMBU_SERIAL: this.config.serial ?? "",
        BAMBU_TOKEN: this.config.token ?? "",
        BAMBU_MODEL: this.config.model ?? "",
      },
    });
    const client = new Client({ name: "3d-models-bambu-cli", version: "0.1.0" }, { capabilities: {} });
    const timer = setTimeout(() => {
      ev("mcp_connect_timeout", { timeout_ms: timeoutMs });
      void transport.close();
    }, timeoutMs);
    try {
      await client.connect(transport);
      this.client = client;
      ev("mcp_connect_done", {});
    } finally {
      clearTimeout(timer);
    }
  }

  async listTools(): Promise<McpTool[]> {
    if (!this.client) throw new Error("MCP not connected");
    const res = await this.client.listTools();
    return res.tools.map((t) => ({ name: t.name, description: t.description }));
  }

  /** Find a tool whose name contains ALL the given hint substrings (case-insensitive). */
  async findTool(...hints: string[]): Promise<string | null> {
    const tools = await this.listTools();
    const lc = hints.map((h) => h.toLowerCase());
    const hit = tools.find((t) => lc.every((h) => t.name.toLowerCase().includes(h)));
    return hit?.name ?? null;
  }

  async call(name: string, args: Record<string, unknown> = {}): Promise<unknown> {
    if (!this.client) throw new Error("MCP not connected");
    ev("mcp_call", { tool: name });
    return this.client.callTool({ name, arguments: args });
  }

  async close(): Promise<void> {
    if (this.client) {
      await this.client.close();
      this.client = null;
    }
  }
}
