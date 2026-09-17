// Backend: first-party Bambu LAN transport over MQTT (read path today; dispatch later).
//
// Why this exists (D-055, amends D-054): the survey (D-054) chose the griches MCP as the control
// transport, but that path was never exercised end-to-end — `@griches/bambu-mcp` is not on npm
// (`npx -y @griches/bambu-mcp` 404s) and the GitHub repo ships no build, so it cannot run as wired.
// The Bambu LAN status read is small and stable — subscribe one report topic, publish one pushall,
// read the cached JSON — so we own it directly rather than spawn an unpinned third-party server with
// the LAN token. We depend only on the same `mqtt` client library griches used (pinned exact). The
// griches source stays a *reference* for command shapes (`pushing.pushall`, `print.project_file`),
// not a runtime dependency. Dispatch (FTPS upload + `print.project_file`) is a later, owner-gated PR.
//
// Bambu LAN facts this encodes (grounded against griches src/mqtt-client.ts, verified 2026-09-16):
//   - mqtts://<host>:8883, username `bblp`, password = the 8-char LAN access code (BAMBU_TOKEN).
//   - The device cert is self-signed → `rejectUnauthorized: false` (standard for Bambu LAN; the
//     trust boundary is the LAN, not the cert). No cert pinning is possible against stock firmware.
//   - Status arrives asynchronously on `device/<serial>/report`; we cache `print`/`mc_print` and
//     nudge a full push with `device/<serial>/request` `{ pushing: { command: "pushall" } }`.
//   - Bambu firmware permits only ONE MQTT client at a time — BambuStudio/OrcaSlicer/Home Assistant
//     must be closed first, or the broker resets the connection.

import mqtt from "mqtt";
import { ev } from "../log.js";
import { loadConfig, type PrinterConfig } from "../config.js";

const MQTT_PORT = 8883;
const MQTT_USER = "bblp";

/** The subset of the printer's report we surface — kept open (record) because the report is large. */
export type PrinterStatus = Record<string, unknown> & {
  _cached_at?: string | null;
  _age_seconds?: number | null;
};

export class MqttBackend {
  private client: mqtt.MqttClient | null = null;
  private lastStatus: Record<string, unknown> = {};
  private lastStatusTime = 0;
  readonly config: PrinterConfig;

  constructor(config: PrinterConfig = loadConfig()) {
    this.config = config;
  }

  /** True when we have enough config to even attempt a connection. */
  configured(): boolean {
    return Boolean(this.config.host && this.config.serial && this.config.token);
  }

  private get deviceId(): string {
    return this.config.serial ?? "";
  }

  private get reportTopic(): string {
    return `device/${this.deviceId}/report`;
  }

  private get requestTopic(): string {
    return `device/${this.deviceId}/request`;
  }

  /**
   * Connect + subscribe to the report topic. Rejects with an actionable message on the two failures
   * we expect: a wrong token/host (connection refused/reset) and the single-client rule (ECONNRESET
   * while BambuStudio et al. hold the slot).
   */
  async connect(timeoutMs = 15_000): Promise<void> {
    if (this.client) return;
    if (!this.configured()) {
      throw new Error("printer config missing (need PRINTER_HOST / BAMBU_SERIAL / BAMBU_TOKEN)");
    }
    ev("mqtt_connect_start", { host: this.config.host ?? "", port: MQTT_PORT });

    await new Promise<void>((resolve, reject) => {
      let settled = false;
      const finish = (fn: () => void) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        fn();
      };

      const timer = setTimeout(() => {
        finish(() => {
          this.hardEnd();
          ev("mqtt_connect_timeout", { timeout_ms: timeoutMs });
          reject(new Error(`connection to ${this.config.host}:${MQTT_PORT} timed out after ${timeoutMs / 1000}s`));
        });
      }, timeoutMs);

      const client = mqtt.connect({
        host: this.config.host,
        port: MQTT_PORT,
        protocol: "mqtts",
        username: MQTT_USER,
        password: this.config.token,
        rejectUnauthorized: false, // self-signed device cert; trust boundary is the LAN
        reconnectPeriod: 0, // one shot — a CLI command is not a long-lived subscriber
        connectTimeout: Math.min(timeoutMs, 10_000),
      });
      this.client = client;

      client.on("connect", () => {
        client.subscribe(this.reportTopic, (err) => {
          if (err) {
            finish(() => {
              this.hardEnd();
              reject(new Error(`subscribe to ${this.reportTopic} failed: ${err.message}`));
            });
            return;
          }
          finish(() => {
            ev("mqtt_connect_done", { topic: this.reportTopic });
            resolve();
          });
        });
      });

      client.on("message", (_topic, payload) => {
        try {
          const data = JSON.parse(payload.toString()) as Record<string, unknown>;
          const status = (data.print ?? data.mc_print) as Record<string, unknown> | undefined;
          if (status) {
            this.lastStatus = { ...this.lastStatus, ...status };
            this.lastStatusTime = Date.now();
          }
        } catch {
          /* non-JSON or partial frame — ignore, the next report supersedes it */
        }
      });

      client.on("error", (err) => {
        finish(() => {
          this.hardEnd();
          reject(this.enhance(err));
        });
      });

      client.on("close", () => {
        finish(() => {
          this.hardEnd();
          reject(this.enhance(new Error("connection closed before the MQTT handshake completed")));
        });
      });
    });
  }

  /** Turn the two opaque LAN failures into the actions that fix them. */
  private enhance(err: Error): Error {
    const msg = err.message || "";
    if (/ECONNRESET|connack timeout|closed before/i.test(msg)) {
      return new Error(
        `${msg}. Two usual causes: (1) Bambu allows only ONE MQTT client — close BambuStudio / ` +
          `OrcaSlicer / Home Assistant and retry; (2) a wrong access code or serial. ` +
          `Re-check with \`bambu setup doctor\`.`,
      );
    }
    return err;
  }

  private hardEnd(): void {
    try {
      this.client?.end(true);
    } catch {
      /* best-effort */
    }
    this.client = null;
  }

  /**
   * Ask the printer to push its full state, then return the cached report. `pushall` is fire-and-
   * forget (the printer answers asynchronously on the report topic), so we wait a beat for the frame
   * to arrive. This sends a status *request* only — it moves no axis and starts no print.
   */
  async requestStatus(settleMs = 2500): Promise<PrinterStatus> {
    if (!this.client) throw new Error("MQTT not connected");
    const message = JSON.stringify({ pushing: { sequence_id: "0", command: "pushall" } });
    ev("mqtt_pushall", { topic: this.requestTopic });
    await new Promise<void>((resolve, reject) => {
      this.client!.publish(this.requestTopic, message, (err) => (err ? reject(err) : resolve()));
    });
    await new Promise((r) => setTimeout(r, settleMs));
    return this.getCachedStatus();
  }

  getCachedStatus(): PrinterStatus {
    return {
      ...this.lastStatus,
      _cached_at: this.lastStatusTime ? new Date(this.lastStatusTime).toISOString() : null,
      _age_seconds: this.lastStatusTime ? Math.round((Date.now() - this.lastStatusTime) / 1000) : null,
    };
  }

  async close(): Promise<void> {
    if (this.client) {
      await new Promise<void>((resolve) => this.client!.end(false, {}, () => resolve()));
      this.client = null;
    }
  }
}
