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

/**
 * Options for the `print.project_file` command that starts a print from an ALREADY-UPLOADED file
 * (#50). The three fields the RE corpus disagrees on for a dual-nozzle X2D — `bedType`, `amsMapping`,
 * `md5` — are exposed so they can be settled against a ground-truth capture without a code change
 * (see docs/issues/first-party-dispatch.md; treat as a CAL-shaped bet). The rest carry grounded
 * defaults that two independent working clients (pybambu, bambulabs_api) send.
 */
export interface ProjectFileOptions {
  /** Bare remote filename at the FTP root, from FtpsBackend.uploadFile (e.g. "plate_1.3mf"). */
  remoteName: string;
  /** Which plate's gcode inside the .3mf to run. Default 1 → param "Metadata/plate_1.gcode". */
  plate?: number;
  /** Job display name. Default: remoteName without its .3mf extension. */
  subtaskName?: string;
  /** [X2D-UNCONFIRMED] plate profile. Default "auto" (firmware detects). */
  bedType?: string;
  /** [X2D-UNCONFIRMED] filament→slot map. Default [0]; dual-nozzle firmware may need a nozzle field. */
  amsMapping?: number[] | string;
  /** [X2D-UNCONFIRMED] file checksum. Default "" (accepted on P1/A1; X1-class historically validated it). */
  md5?: string;
  useAms?: boolean; // default false (single filament / external spool)
  bedLeveling?: boolean; // default true
  flowCali?: boolean; // default true
  vibrationCali?: boolean; // default true
  layerInspect?: boolean; // default false
  timelapse?: boolean; // default false
  sequenceId?: string; // echo-back id; default "0"
}

/** A `print.*` request payload as the firmware expects it: `{ print: { ... } }`. */
export type PrintRequest = { print: Record<string, unknown> };

/**
 * Build the `print.project_file` payload for a LAN-mode, local-file print (pure; unit-tested). The
 * command references the file uploaded to the FTP root as `ftp:///<name>` (three slashes: empty host
 * + /<name>), and runs the plate's gcode inside the .3mf via `param`. All four *_id fields are the
 * string "0" — the RE spec annotates each "Always 0 for local prints".
 */
export function buildProjectFileCommand(opts: ProjectFileOptions): PrintRequest {
  const plate = opts.plate ?? 1;
  const name = opts.remoteName;
  return {
    print: {
      sequence_id: opts.sequenceId ?? "0",
      command: "project_file",
      param: `Metadata/plate_${plate}.gcode`,
      url: `ftp:///${name}`,
      subtask_name: opts.subtaskName ?? name.replace(/\.3mf$/i, ""),
      project_id: "0",
      profile_id: "0",
      task_id: "0",
      subtask_id: "0",
      md5: opts.md5 ?? "",
      bed_type: opts.bedType ?? "auto",
      bed_leveling: opts.bedLeveling ?? true,
      flow_cali: opts.flowCali ?? true,
      vibration_cali: opts.vibrationCali ?? true,
      layer_inspect: opts.layerInspect ?? false,
      timelapse: opts.timelapse ?? false,
      use_ams: opts.useAms ?? false,
      ams_mapping: opts.amsMapping ?? [0],
    },
  };
}

/** Build a `print.{pause,resume,stop}` control payload (pure; unit-tested). */
export function buildPrintControlCommand(command: "pause" | "resume" | "stop", sequenceId = "0"): PrintRequest {
  return { print: { sequence_id: sequenceId, command } };
}

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

  /** Publish a request payload on device/<serial>/request. Fire-and-forget; the printer acks on report. */
  private async publishRequest(payload: PrintRequest): Promise<void> {
    if (!this.client) throw new Error("MQTT not connected");
    await new Promise<void>((resolve, reject) => {
      this.client!.publish(this.requestTopic, JSON.stringify(payload), (err) => (err ? reject(err) : resolve()));
    });
  }

  /**
   * Start a print from a file ALREADY UPLOADED to the FTP root (#50). OWNER-GATED — the caller owns
   * the confirm; this method only publishes once told to. Returns the command it sent so the caller
   * can log/record the exact payload.
   */
  async startProjectFile(opts: ProjectFileOptions): Promise<PrintRequest> {
    const cmd = buildProjectFileCommand(opts);
    ev("mqtt_project_file", { url: String(cmd.print.url), param: String(cmd.print.param) });
    await this.publishRequest(cmd);
    return cmd;
  }

  /** Send a `print.{pause,resume,stop}` control command. */
  async sendPrintControl(command: "pause" | "resume" | "stop"): Promise<void> {
    ev("mqtt_print_control", { command });
    await this.publishRequest(buildPrintControlCommand(command));
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
