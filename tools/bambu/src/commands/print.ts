// `bambu print` — dispatch + print control over our first-party LAN transport (#50).
//   send <plate.3mf> [--record] : upload a sliced .3mf (FTPS 990) + start it (MQTT project_file)
//                                  — OWNER-GATED, confirm-before-send
//   pause | resume | stop        : control the running print via MQTT (stop confirms)
//   list                         : enumerate print records (delegates to print-list)
//
// Why first-party (extends D-055): the griches MCP that once backed this was never installable
// (@griches/bambu-mcp is unpublished, ships no build), so both halves of dispatch now ride code we
// own — FtpsBackend for the upload, MqttBackend.startProjectFile for the start. Dispatch is the one
// verb that moves real hardware and printing is on hold until a CAL bet justifies a plate (memory:
// owner-gated-and-on-hold), so `send` is fail-closed: it refuses unless the operator passes --yes or
// confirms at a TTY, and --dry-run prints the EXACT FTPS target + MQTT payload it WOULD send without
// connecting — the review surface for the three X2D-UNCONFIRMED fields before the first real send.

import { Command } from "commander";
import { existsSync, statSync } from "node:fs";
import { basename, extname, resolve } from "node:path";
import { FtpsBackend, remoteUploadName } from "../backends/ftps.js";
import {
  MqttBackend,
  buildProjectFileCommand,
  type PrinterStatus,
  type ProjectFileOptions,
} from "../backends/mqtt.js";
import { loadConfig, type PrinterConfig } from "../config.js";
import { confirm } from "../prompt.js";
import { scaffoldRecord, type ScaffoldObject } from "../records.js";
import { recordProfileFrom, type RecordProfile } from "../header.js";
import { buildActuals, actualsToRecord, actualsAreEmpty } from "../actuals.js";
import { runPrintList } from "./print-list.js";
import { ev } from "../log.js";
import { sidecarFreshness, classifyWarnings, loadManifest, sidecarPath } from "../backends/warnings.js";

/** Dispatch needs host+serial+token: FTPS uses host+token, the project_file topic needs the serial. */
function requireConfigured(cfg: PrinterConfig): void {
  if (!cfg.host || !cfg.serial || !cfg.token) {
    console.error("Not configured. Set PRINTER_HOST / BAMBU_SERIAL / BAMBU_TOKEN (or .mcp.json).");
    console.error("Run `bambu setup doctor` to see what's missing.");
    process.exit(1);
  }
}

interface SendOpts {
  record?: boolean;
  yes?: boolean;
  dryRun?: boolean;
  slug?: string;
  object?: string[]; // --object bikar:<path>[=entry], repeatable
  allowUnverified?: boolean;
  plate?: string; // --plate N (commander passes a string)
  bedType?: string; // [X2D-UNCONFIRMED] override the default "auto"
  amsMapping?: string; // [X2D-UNCONFIRMED] comma-ints ("0" / "-1,0") or "none"
  md5?: string; // [X2D-UNCONFIRMED] override the default ""
  bedLeveling?: boolean; // --no-bed-leveling → false
  flowCali?: boolean; // --no-flow-cali → false
  vibrationCali?: boolean; // --no-vibration-cali → false
}

/**
 * Pre-dispatch warnings gate (#52): never send a plate Studio would warn about. Reads the warnings
 * sidecar `bambu slice` writes beside the .3mf, verifies it describes THIS plate, classifies it
 * against the by-design manifest, and:
 *   - no sidecar        → BLOCK (fail-closed: a plate we cannot verify is not dispatched);
 *   - stale sidecar     → BLOCK (source_sha256 ≠ the .3mf on disk — it was sliced from other bytes);
 *   - unverifiable      → BLOCK (a legacy sidecar with no source_sha256 cannot be proven fresh);
 *   - any UNEXPECTED    → BLOCK (Studio would warn about this);
 *   - clean / expected  → allow.
 * Each BLOCK is overridable only by --allow-unverified (the high-bar, loudly-logged escape hatch).
 * Returns true iff dispatch may proceed.
 */
function warningsGateAllows(plateAbs: string, allowUnverified: boolean): boolean {
  const { sidecar, status } = sidecarFreshness(plateAbs);
  if (status !== "fresh") {
    const reason =
      status === "missing"
        ? "no slicer-warnings capture beside this plate"
        : status === "stale"
          ? "the capture beside this plate was sliced from different .3mf bytes (STALE)"
          : "the capture beside this plate predates freshness tracking and cannot be verified";
    if (allowUnverified) {
      console.error(`⚠ warnings gate: ${reason} — proceeding under --allow-unverified.`);
      return true;
    }
    console.error(`✗ warnings gate: ${reason}.`);
    console.error(`  expected a fresh ${basename(sidecarPath(plateAbs))} — re-slice with \`bambu slice plate\` so`);
    console.error("  dispatch can verify Studio raised nothing unexpected. Override with --allow-unverified only if you must.");
    return false;
  }
  const { expected, unexpected } = classifyWarnings(sidecar!.warnings, loadManifest());
  if (unexpected.length > 0) {
    console.error(`✗ warnings gate: ${unexpected.length} UNEXPECTED slicer warning(s) — refusing to dispatch:`);
    for (const w of unexpected) console.error(`    [${w.severity}] ${w.object ?? "(plate)"}: ${w.message}`);
    console.error("  Studio would warn about this. Fix the model/settings and re-slice, or whitelist it in");
    console.error("  .claude/gates/expected-slicer-warnings.json if it is genuinely by-design.");
    return false;
  }
  console.error(
    sidecar!.warnings.length === 0
      ? "✓ warnings gate: clean — no slicer warnings (capture verified fresh for this plate)."
      : `✓ warnings gate: ${expected.length} expected-by-design warning(s), 0 unexpected (fresh).`,
  );
  return true;
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

/** Parse the [X2D-UNCONFIRMED] --ams-mapping flag: comma-ints, "none" (empty-string form), or unset. */
function parseAmsMapping(spec: string | undefined): number[] | string | undefined {
  if (spec === undefined) return undefined; // let the builder default to [0]
  const t = spec.trim().toLowerCase();
  if (t === "none" || t === "") return ""; // the OpenBambuAPI empty-string form (some firmware wants this)
  const nums = spec.split(",").map((s) => Number(s.trim()));
  if (nums.some((n) => !Number.isInteger(n))) {
    throw new Error(`--ams-mapping must be comma-separated integers (e.g. "0" or "-1,0") or "none", got "${spec}"`);
  }
  return nums;
}

/** Assemble the ProjectFileOptions from the flags — throws (caught by the caller) on a bad flag. */
function buildProjectOptions(remoteName: string, opts: SendOpts): ProjectFileOptions {
  let plate: number | undefined;
  if (opts.plate !== undefined) {
    plate = Number(opts.plate);
    if (!Number.isInteger(plate) || plate < 1) {
      throw new Error(`--plate must be a positive integer (the plate index inside the .3mf), got "${opts.plate}"`);
    }
  }
  return {
    remoteName,
    plate,
    bedType: opts.bedType,
    amsMapping: parseAmsMapping(opts.amsMapping),
    md5: opts.md5,
    bedLeveling: opts.bedLeveling,
    flowCali: opts.flowCali,
    vibrationCali: opts.vibrationCali,
  };
}

/**
 * Pre-fill the record's profile header from the SAME builder `bambu header` uses (D-052: one code
 * path). The .3mf being dispatched IS the `--plate`, so machine/nozzle/layer/profile/slicer come off
 * it; the printer-side material/chamber come from a best-effort MQTT read. Every step is best-effort:
 * a missing printer or an unreadable frame degrades to the plain TODO scaffold, never a crash — and
 * never a fabricated field (the builder leaves unconfirmed/manual fields out of the record profile).
 */
async function buildRecordProfile(plateFile: string): Promise<RecordProfile | undefined> {
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
  return recordProfileFrom(frame, plateFile);
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

  // Pre-dispatch warnings gate (#52) — refuse anything Studio would warn about. Runs before the owner
  // gate so a blocked plate never even reaches the confirm. --dry-run reports the verdict but does not
  // block (nothing is sent on a dry run anyway).
  const gateOk = warningsGateAllows(abs, Boolean(opts.allowUnverified));
  if (!gateOk && !opts.dryRun) {
    process.exitCode = 2;
    return;
  }

  // Build (and validate) the dispatch options before any network — a bad --plate/--ams-mapping fails
  // fast, not after an upload.
  let projectOpts: ProjectFileOptions;
  try {
    projectOpts = buildProjectOptions(remoteUploadName(abs), opts);
  } catch (err) {
    console.error((err as Error).message);
    process.exitCode = 2;
    return;
  }

  const cfg = loadConfig();
  requireConfigured(cfg);

  // Owner gate, stated out loud before anything reaches the printer.
  console.error("⚠ Dispatch is owner-gated: this sends a plate to the physical X2D.");
  console.error(`  plate: ${basename(abs)} (${kb} KB) → ${cfg.host ?? "(host unset)"}`);
  console.error("  Printing is on hold until a CAL bet justifies a plate (see the setup skill).");

  const command = buildProjectFileCommand(projectOpts);

  if (opts.dryRun) {
    console.log("dry run — would dispatch WITHOUT sending (no upload, no publish performed):");
    console.log(`  1. FTPS implicit-TLS upload → ${cfg.host}:990 (user bblp) STOR /${projectOpts.remoteName}`);
    console.log(`  2. MQTT publish → device/${cfg.serial}/request:`);
    console.log(JSON.stringify(command, null, 2));
    console.log("  [X2D-UNCONFIRMED] bed_type / ams_mapping / md5 — diff this payload against a BambuStudio");
    console.log("  ground-truth capture before the first real send (docs/issues/first-party-dispatch.md).");
    if (opts.record) console.log("would also scaffold a draft record under .bambu/records/.");
    return;
  }

  if (!(await confirm("Send this plate to the printer now?", Boolean(opts.yes)))) {
    console.error("refused — not sending. Pass --yes (or confirm at a TTY) to dispatch.");
    process.exitCode = 2;
    return;
  }

  const ftps = new FtpsBackend(cfg);
  const mqtt = new MqttBackend(cfg);
  try {
    ev("dispatch_start", { plate: basename(abs), kb });
    // 1. Upload the .3mf to the FTP root over implicit FTPS.
    console.error(`uploading ${basename(abs)} over FTPS (implicit TLS, :990)…`);
    const remote = await ftps.uploadFile(abs);
    console.error(`uploaded → /${remote}. Starting the print…`);
    // 2. Start the print from the uploaded file over MQTT.
    await mqtt.connect();
    const sent = await mqtt.startProjectFile({ ...projectOpts, remoteName: remote });
    // Best-effort confirmation: give the printer a beat, then read back its state so the operator
    // sees it took. The publish already happened; a failed read never un-dispatches it.
    let state = "(unconfirmed)";
    try {
      const status = await mqtt.requestStatus();
      state = String(status.gcode_state ?? status.mc_print_stage ?? "(unconfirmed)");
    } catch {
      /* status read is a nicety, not the dispatch */
    }
    ev("dispatch_done", { plate: basename(abs), state });
    console.log(`dispatched ${basename(abs)} (${String(sent.print.url)}) — printer state: ${state}.`);
    console.log("Watch it with `bambu status monitor`.");
  } catch (err) {
    console.error(`dispatch failed: ${(err as Error).message}`);
    process.exitCode = 1;
  } finally {
    await mqtt.close();
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

interface CaptureOpts {
  slug?: string;
  plate?: string; // path to the .3mf that was printed (optional) — fills the slice-side profile fields
  object?: string[]; // --object bikar:<path>[=entry], repeatable — pins R1 provenance, as `send --record`
  json?: boolean;
}

/** A trimmed string from a frame key, or undefined. Local to slug/label derivation (no shape drift). */
function frameString(frame: PrinterStatus, key: string): string | undefined {
  const v = frame[key];
  if (v == null) return undefined;
  const s = String(v).trim();
  return s || undefined;
}

/**
 * `bambu print capture` — read the printer's MQTT device report and scaffold a DRAFT record carrying
 * an `actuals:` block (the #71 metadata gap: a print started from the Studio GUI is seen by nothing, so
 * `docs/prints/` stays empty and the record count under-reports what we actually printed). This is
 * READ-ONLY and print-safe — `requestStatus` sends a pushall and reads the cached frame; it moves no
 * axis and starts/stops nothing (mqtt.ts). No owner gate: nothing is dispatched. The operator fills
 * provenance/photos/readings and promotes the draft to docs/prints/, exactly as a `--record` draft.
 */
async function runCapture(opts: CaptureOpts): Promise<void> {
  const cfg = loadConfig();
  requireConfigured(cfg); // MQTT needs host + serial + token

  // Resolve the (optional) .3mf up front so a bad path fails before we touch the network.
  let plateAbs: string | undefined;
  if (opts.plate) {
    plateAbs = resolve(opts.plate);
    if (!existsSync(plateAbs)) {
      console.error(`no such file: ${opts.plate} (omit --plate to capture without slice-side profile fields)`);
      process.exitCode = 1;
      return;
    }
  }

  // Read the device report (read-only). A best-effort read: an unreachable printer is a hard failure
  // here (unlike --record, there is nothing else to write), so report it and stop.
  let frame: PrinterStatus = {};
  const mqtt = new MqttBackend(cfg);
  try {
    ev("capture_read_start", {});
    await mqtt.connect();
    frame = await mqtt.requestStatus();
  } catch (err) {
    console.error(`could not read the printer report: ${(err as Error).message}`);
    process.exitCode = 1;
    return;
  } finally {
    await mqtt.close();
  }

  const actuals = buildActuals(frame);
  if (opts.json) {
    console.log(JSON.stringify({ actuals, raw: frame }, null, 2));
    return;
  }
  if (actualsAreEmpty(actuals)) {
    console.error("⚠ the report carried no print-state fields (state/progress/layer/job) — is a print running or");
    console.error("  just finished? Scaffolding anyway; the verbatim frame lands in device-report.json to inspect.");
  }

  const job = frameString(frame, "subtask_name");
  const slug = (opts.slug ?? job ?? "captured-print").replace(/[^a-z0-9]+/gi, "-").toLowerCase();
  const plateName = job ?? "(captured print)";
  const profile = await recordProfileFrom(frame, plateAbs);

  try {
    const dir = await scaffoldRecord({
      slug,
      plateName,
      plateFile: plateAbs ?? job ?? "captured",
      objects: parseObjects(opts.object),
      profile,
      via: "bambu print capture",
      capture: {
        actuals: actualsToRecord(actuals),
        capturedAt: actuals.captured_at.value ?? new Date().toISOString(),
        rawFrame: frame,
      },
    });
    ev("capture_done", { dir, state: actuals.state.value ?? "" });
    console.log(`captured → ${dir}`);
    console.log(`  printer state: ${actuals.state.value ?? "(none)"}  progress: ${actuals.progress_pct.value ?? "?"}%  layer: ${actuals.layer.value ?? "?"}`);
    console.log("Fill the object provenance + TODOs, then `bambu validate record .bambu/records` before moving it to docs/prints/.");
  } catch (err) {
    console.error(`capture scaffold failed: ${(err as Error).message}`);
    process.exitCode = 1;
  }
}

/** Shared body for pause/resume/stop over MQTT. `stop` confirms first; pause/resume are reversible. */
async function runControl(verb: "pause" | "resume" | "stop", opts: { yes?: boolean }): Promise<void> {
  if (verb === "stop" && !(await confirm("Stop the running print?", Boolean(opts.yes)))) {
    console.error("refused — not stopping. Pass --yes (or confirm at a TTY).");
    process.exitCode = 2;
    return;
  }
  const cfg = loadConfig();
  requireConfigured(cfg);
  const mqtt = new MqttBackend(cfg);
  try {
    await mqtt.connect();
    ev(`${verb}_call`, {});
    await mqtt.sendPrintControl(verb);
    console.log(`${verb} sent.`);
  } catch (err) {
    console.error(`${verb} failed: ${(err as Error).message}`);
    process.exitCode = 1;
  } finally {
    await mqtt.close();
  }
}

export function registerPrint(program: Command): void {
  const print = program
    .command("print")
    .description(
      "catalog, capture, dispatch and control prints — `list`/`capture` are local & read-only; " +
        "`send`/`pause`/`stop` move real hardware and are owner-gated",
    );

  print
    .command("send <plate>")
    .description("upload a sliced .3mf (FTPS) + start it (MQTT) — OWNER-GATED, confirm-before-send")
    .option("--record", "scaffold a draft print record under .bambu/records/", false)
    .option("--slug <slug>", "slug for the record run name (default: derived from the plate)")
    .option(
      "-O, --object <spec>",
      "printed object as bikar:<path>[=ENTRY] (repeatable) — pins R1 provenance in the record",
      (v: string, acc: string[]) => [...acc, v],
      [] as string[],
    )
    .option("--plate <n>", "plate index inside the .3mf to print (default 1 → Metadata/plate_1.gcode)")
    .option("--bed-type <type>", "[X2D-UNCONFIRMED] plate profile: auto|cool_plate|eng_plate|hot_plate|textured_plate (default auto)")
    .option("--ams-mapping <spec>", '[X2D-UNCONFIRMED] filament→slot map: comma-ints e.g. "0" or "-1,0", or "none" (default "0")')
    .option("--md5 <hex>", "[X2D-UNCONFIRMED] .3mf checksum for firmware that validates it (default empty)")
    .option("--no-bed-leveling", "skip auto bed-leveling before this print")
    .option("--no-flow-cali", "skip flow calibration before this print")
    .option("--no-vibration-cali", "skip vibration calibration before this print")
    .option("-y, --yes", "skip the confirmation prompt (still logs the owner-gate notice)", false)
    .option(
      "--allow-unverified",
      "dispatch a plate with no warnings-capture sidecar (high-bar override of the fail-closed gate)",
      false,
    )
    .option("--dry-run", "print the exact FTPS target + MQTT payload without connecting or dispatching", false)
    .action(runSend);

  print
    .command("capture")
    .description("read the printer's MQTT device report → scaffold a DRAFT record (counts a GUI print) — read-only, no owner gate")
    .option("--slug <slug>", "slug for the record run name (default: the printer's subtask_name, else 'captured-print')")
    .option("--plate <file>", "the sliced .3mf that was printed — fills the slice-side profile fields (machine/nozzle/layer/profile)")
    .option(
      "-O, --object <spec>",
      "printed object as bikar:<path>[=ENTRY] (repeatable) — pins R1 provenance in the record",
      (v: string, acc: string[]) => [...acc, v],
      [] as string[],
    )
    .option("--json", "print the built actuals + raw frame as JSON instead of scaffolding a record", false)
    .addHelpText(
      "after",
      "\nExample (after a print you started from Bambu Studio):\n" +
        "  bambu print capture --plate build/plate.3mf -O bikar:patterns/Coupons/Machine-Card.bkr=MC-1\n" +
        "Then fill the draft's TODOs and `bambu validate record .bambu/records` before moving it to docs/prints/.",
    )
    .action((opts: CaptureOpts) => runCapture(opts));

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
