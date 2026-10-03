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
 * A calibration step's mode in a start command, as Studio sends it to an X2D: 0 off, 1 on, 2 auto
 * (the printer decides). The start G-code reads these through `M1002 judge_flag`, so the job, not a
 * boolean, decides whether the step runs (docs/research/2026-10-03-studio-start-payload.md, row 3).
 */
export type CaliMode = 0 | 1 | 2;

/**
 * Options for the `print.project_file` command that starts a print from an ALREADY-UPLOADED file
 * (#50). The defaults are what Bambu Studio sends an X2D, from the one wire capture we have
 * (bambuddy #1192, X2D firmware 01.01, two Studio sends) and Studio's own send code; the checked
 * research is docs/research/2026-10-03-studio-start-payload.md. `md5` is still disputed between
 * captures, and the external spool's `ams_mapping2` entry has not been seen on an X2D.
 */
export interface ProjectFileOptions {
  /** Bare remote filename at the FTP root, from FtpsBackend.uploadFile (e.g. "plate_1.3mf"). */
  remoteName: string;
  /** Which plate's gcode inside the .3mf to run. Default 1 → param "Metadata/plate_1.gcode". */
  plate?: number;
  /** Job display name. Default: remoteName without its .3mf extension. */
  subtaskName?: string;
  /**
   * The plate type the slice was made for, as Studio's token ("textured_plate", …), read off the
   * .3mf (plate-type.ts). Required: Studio never sends "auto", and the X2D pauses with 0500-8051 when
   * this does not match the plate on the bed (sheets-04b, 2026-10-03).
   */
  bedType: string;
  /**
   * Filament→tray map, one entry per project filament: `unit*4 + tray` for an AMS tray, 254/255 for
   * the external spool, -1 unused (frame.ts trayIndex). Default [0]. `ams_mapping2` is built from it.
   */
  amsMapping?: number[] | string;
  /** [X2D-UNCONFIRMED] file checksum. Default "". Studio sends a real MD5 or "from_sd_card"; the X2D took "". */
  md5?: string;
  useAms?: boolean; // default false (single filament / external spool)
  bedLeveling?: CaliMode; // auto_bed_leveling, default 2 (auto)
  flowCali?: CaliMode; // extrude_cali_flag, default 2 (auto)
  nozzleOffsetCali?: CaliMode; // nozzle_offset_cali, default 2 (auto)
  vibrationCali?: boolean; // default false: Studio hard-codes it off (SelectMachine.cpp L3371-3383)
  layerInspect?: boolean; // default true, as Studio sends it
  timelapse?: boolean; // default false
  sequenceId?: string; // echo-back id; default startSequenceId() — in the 20000s, never reused
}

/**
 * A `sequence_id` for a start command: in the 20000s, as Studio's X2D sends are (20001, 20002), and
 * different from one run of the CLI to the next, since the printer refuses an id reused across
 * restarts (err_code 84033544, open-bamboo print ABI L164). The seconds clock gives a new id per
 * second and comes round again only after 10,000 s.
 */
export function startSequenceId(nowMs: number = Date.now()): string {
  return String(20000 + (Math.floor(nowMs / 1000) % 10000));
}

/** The external spool's tray numbers (frame.ts trayIndex): 254, and 255 for a second spool. */
const isExternal = (i: number): boolean => i === 254 || i === 255;

/**
 * Studio's `ams_mapping2` from our flat map: `{ams_id, slot_id}` per filament, `{255, 255}` for an
 * unused one (the P2S capture: `[3,-1,-1]` → `[{0,3},{255,255},{255,255}]`; the X2D capture:
 * `[1,0]` → `[{0,1},{0,0}]`). [X2D-UNCONFIRMED] the external spool: bambuddy's notes say ams_id 254
 * is the X2D's left nozzle spool and 255 the right one, so its own number with slot 0; no capture of
 * an X2D external-spool send has been seen.
 */
export function amsMapping2(mapping: number[]): { ams_id: number; slot_id: number }[] {
  return mapping.map((i) => {
    if (isExternal(i)) return { ams_id: i, slot_id: 0 };
    if (i < 0) return { ams_id: 255, slot_id: 255 };
    return { ams_id: Math.floor(i / 4), slot_id: i % 4 };
  });
}

/**
 * The flat `ams_mapping` as sent: the external spool becomes -1 there and lives only in
 * `ams_mapping2`, because a 254/255 in the flat list makes the printer raise 0700_8012 (bambuddy's
 * notes, carried by the research, single-source).
 */
function flatMappingForSend(mapping: number[]): number[] {
  return mapping.map((i) => (isExternal(i) ? -1 : i));
}

/** A `print.*` request payload as the firmware expects it: `{ print: { ... } }`. */
export type PrintRequest = { print: Record<string, unknown> };

/**
 * Build the `print.project_file` payload for a LAN-mode, local-file print (pure; unit-tested). The
 * command references the file uploaded to the FTP root as `ftp:///<name>` (three slashes: empty host
 * + /<name>), and runs the plate's gcode inside the .3mf via `param`. All four *_id fields are the
 * string "0" — the RE spec annotates each "Always 0 for local prints". The field set is the X2D
 * capture's (bambuddy #1192) less `nozzle_mapping`, which that capture does not carry; the url stays
 * `ftp:///`, which the X2D took, where Studio's eMMC send says `brtc://emmc/`.
 */
export function buildProjectFileCommand(opts: ProjectFileOptions): PrintRequest {
  const plate = opts.plate ?? 1;
  const name = opts.remoteName;
  const mapping = opts.amsMapping ?? [0];
  const bedLeveling = opts.bedLeveling ?? 2;
  const flowCali = opts.flowCali ?? 2;
  return {
    print: {
      sequence_id: opts.sequenceId ?? startSequenceId(),
      command: "project_file",
      param: `Metadata/plate_${plate}.gcode`,
      url: `ftp:///${name}`,
      file: name,
      subtask_name: opts.subtaskName ?? name.replace(/\.3mf$/i, ""),
      project_id: "0",
      profile_id: "0",
      task_id: "0",
      subtask_id: "0",
      md5: opts.md5 ?? "",
      bed_type: opts.bedType,
      // The mode rides in the numbers; the old booleans are true only when a step is forced on, as
      // Studio's X2D sends show (false beside the 2s).
      auto_bed_leveling: bedLeveling,
      extrude_cali_flag: flowCali,
      nozzle_offset_cali: opts.nozzleOffsetCali ?? 2,
      extrude_cali_manual_mode: 0,
      bed_leveling: bedLeveling === 1,
      flow_cali: flowCali === 1,
      vibration_cali: opts.vibrationCali ?? false,
      layer_inspect: opts.layerInspect ?? true,
      timelapse: opts.timelapse ?? false,
      cfg: "0",
      use_ams: opts.useAms ?? false,
      ams_mapping: Array.isArray(mapping) ? flatMappingForSend(mapping) : mapping,
      ams_mapping2: Array.isArray(mapping) ? amsMapping2(mapping) : [],
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
