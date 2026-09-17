import { describe, expect, it } from "vitest";
import { buildProjectFileCommand, buildPrintControlCommand, type ProjectFileOptions } from "./mqtt.js";
import { remoteUploadName } from "./ftps.js";

// These three builders are the whole grounded surface of first-party dispatch (#50): the exact MQTT
// `print.project_file` payload the firmware sees, the pause/resume/stop control payload, and the
// remote name an upload lands under. They must be pure and deterministic so `--dry-run` can print
// exactly what a real send would publish without a printer. The values asserted here are the grounded
// defaults from pybambu / bambulabs_api / OpenBambuAPI; the three X2D-UNCONFIRMED fields
// (bed_type / ams_mapping / md5) are asserted at their documented defaults and as overrides.

describe("remoteUploadName", () => {
  it("is the bare basename (the printer only accepts root uploads)", () => {
    expect(remoteUploadName("/abs/path/to/plate_1.3mf")).toBe("plate_1.3mf");
    expect(remoteUploadName("plate_1.3mf")).toBe("plate_1.3mf");
    expect(remoteUploadName("./build/A4-machine-card.3mf")).toBe("A4-machine-card.3mf");
  });
});

describe("buildProjectFileCommand — grounded defaults", () => {
  const cmd = buildProjectFileCommand({ remoteName: "plate_1.3mf" });
  const p = cmd.print;

  it("wraps the payload as { print: {...} }", () => {
    expect(Object.keys(cmd)).toEqual(["print"]);
  });

  it("names the local-file project_file command", () => {
    expect(p.command).toBe("project_file");
  });

  it("runs plate 1's gcode by default and references the FTP-root file with three slashes", () => {
    // Metadata/plate_<n>.gcode inside the .3mf; ftp:///<name> = empty host + /<name> at the FTP root.
    expect(p.param).toBe("Metadata/plate_1.gcode");
    expect(p.url).toBe("ftp:///plate_1.3mf");
  });

  it("defaults the job name to the file without its .3mf extension", () => {
    expect(p.subtask_name).toBe("plate_1");
  });

  it("sets all four *_id fields to the string '0' (always 0 for a local print)", () => {
    expect(p.project_id).toBe("0");
    expect(p.profile_id).toBe("0");
    expect(p.task_id).toBe("0");
    expect(p.subtask_id).toBe("0");
    expect(p.sequence_id).toBe("0");
  });

  it("carries the grounded calibration/AMS defaults for a single-filament LAN print", () => {
    expect(p.use_ams).toBe(false);
    expect(p.bed_leveling).toBe(true);
    expect(p.flow_cali).toBe(true);
    expect(p.vibration_cali).toBe(true);
    expect(p.layer_inspect).toBe(false);
    expect(p.timelapse).toBe(false);
  });

  it("defaults the three X2D-UNCONFIRMED fields to their documented values", () => {
    expect(p.bed_type).toBe("auto");
    expect(p.ams_mapping).toEqual([0]);
    expect(p.md5).toBe("");
  });
});

describe("buildProjectFileCommand — overrides", () => {
  it("selects a different plate for both param and default subtask name is unaffected by plate", () => {
    const p = buildProjectFileCommand({ remoteName: "card.3mf", plate: 3 }).print;
    expect(p.param).toBe("Metadata/plate_3.gcode");
    expect(p.url).toBe("ftp:///card.3mf");
    expect(p.subtask_name).toBe("card");
  });

  it("passes the X2D-UNCONFIRMED fields straight through when set", () => {
    const p = buildProjectFileCommand({
      remoteName: "card.3mf",
      bedType: "textured_plate",
      amsMapping: [-1, 0],
      md5: "d41d8cd98f00b204e9800998ecf8427e",
    }).print;
    expect(p.bed_type).toBe("textured_plate");
    expect(p.ams_mapping).toEqual([-1, 0]);
    expect(p.md5).toBe("d41d8cd98f00b204e9800998ecf8427e");
  });

  it("accepts the empty-string ams_mapping form some firmware wants", () => {
    const p = buildProjectFileCommand({ remoteName: "card.3mf", amsMapping: "" }).print;
    expect(p.ams_mapping).toBe("");
  });

  it("lets calibration steps be turned off individually", () => {
    const p = buildProjectFileCommand({
      remoteName: "card.3mf",
      bedLeveling: false,
      flowCali: false,
      vibrationCali: false,
    }).print;
    expect(p.bed_leveling).toBe(false);
    expect(p.flow_cali).toBe(false);
    expect(p.vibration_cali).toBe(false);
  });

  it("honours an explicit subtask name and sequence id", () => {
    const p = buildProjectFileCommand({
      remoteName: "card.3mf",
      subtaskName: "Plate 1 — machine card",
      sequenceId: "42",
    }).print;
    expect(p.subtask_name).toBe("Plate 1 — machine card");
    expect(p.sequence_id).toBe("42");
  });

  // false is a real value the builder must not clobber with its default (?? guards against exactly
  // this — a plain || would have flipped these back to true/on).
  it("preserves an explicitly-false flag rather than defaulting it back on", () => {
    const opts: ProjectFileOptions = { remoteName: "card.3mf", timelapse: false, useAms: false };
    const p = buildProjectFileCommand(opts).print;
    expect(p.timelapse).toBe(false);
    expect(p.use_ams).toBe(false);
  });
});

describe("buildPrintControlCommand", () => {
  it.each(["pause", "resume", "stop"] as const)("builds the %s control payload", (command) => {
    expect(buildPrintControlCommand(command)).toEqual({ print: { sequence_id: "0", command } });
  });

  it("echoes a caller-supplied sequence id", () => {
    expect(buildPrintControlCommand("stop", "7")).toEqual({ print: { sequence_id: "7", command: "stop" } });
  });
});
