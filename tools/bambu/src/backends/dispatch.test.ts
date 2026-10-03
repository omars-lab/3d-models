import { describe, expect, it } from "vitest";
import {
  amsMapping2,
  buildProjectFileCommand,
  buildPrintControlCommand,
  startSequenceId,
  type ProjectFileOptions,
} from "./mqtt.js";
import { remoteUploadName } from "./ftps.js";

// These three builders are the whole grounded surface of first-party dispatch (#50): the exact MQTT
// `print.project_file` payload the firmware sees, the pause/resume/stop control payload, and the
// remote name an upload lands under. They must be pure and deterministic so `--dry-run` can print
// exactly what a real send would publish without a printer. The defaults asserted here are what Bambu
// Studio sends an X2D: the wire capture in bambuddy #1192 (firmware 01.01) and Studio's send code,
// checked in docs/research/2026-10-03-studio-start-payload.md. md5 stays X2D-UNCONFIRMED.

describe("remoteUploadName", () => {
  it("is the bare basename (the printer only accepts root uploads)", () => {
    expect(remoteUploadName("/abs/path/to/plate_1.3mf")).toBe("plate_1.3mf");
    expect(remoteUploadName("plate_1.3mf")).toBe("plate_1.3mf");
    expect(remoteUploadName("./build/A4-machine-card.3mf")).toBe("A4-machine-card.3mf");
  });
});

describe("buildProjectFileCommand — grounded defaults", () => {
  const cmd = buildProjectFileCommand({ remoteName: "plate_1.3mf", bedType: "textured_plate" });
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
  });

  it("names the file, as Studio's X2D sends do", () => {
    expect(p.file).toBe("plate_1.3mf");
  });

  it("uses a sequence id in the 20000s", () => {
    const id = Number(p.sequence_id);
    expect(id).toBeGreaterThanOrEqual(20000);
    expect(id).toBeLessThan(30000);
  });

  // use_ams:false is only the builder's default. `print send` never relies on it: it always sets
  // use_ams and ams_mapping from the loaded trays or --ams-mapping (ams-mapping.test.ts).
  it("sends the calibration modes as Studio's X2D send does: numbers, 2 = auto", () => {
    expect(p.auto_bed_leveling).toBe(2);
    expect(p.extrude_cali_flag).toBe(2);
    expect(p.nozzle_offset_cali).toBe(2);
    expect(p.extrude_cali_manual_mode).toBe(0);
  });

  it("sends the booleans as Studio does: false beside the modes, vibration off, layer check on", () => {
    expect(p.use_ams).toBe(false);
    expect(p.bed_leveling).toBe(false);
    expect(p.flow_cali).toBe(false);
    expect(p.vibration_cali).toBe(false);
    expect(p.layer_inspect).toBe(true);
    expect(p.timelapse).toBe(false);
    expect(p.cfg).toBe("0");
  });

  // Every field of the X2D capture but `url` (eMMC there, FTPS here) is in our payload, and nothing
  // the capture lacks is added — `nozzle_mapping` stays out until an X2D capture shows it.
  it("carries exactly the X2D capture's field set", () => {
    const capture = [
      "ams_mapping", "ams_mapping2", "auto_bed_leveling", "bed_leveling", "bed_type", "cfg", "command",
      "extrude_cali_flag", "extrude_cali_manual_mode", "file", "flow_cali", "layer_inspect", "md5",
      "nozzle_offset_cali", "param", "profile_id", "project_id", "sequence_id", "subtask_id",
      "subtask_name", "task_id", "timelapse", "url", "use_ams", "vibration_cali",
    ];
    expect(Object.keys(p).sort()).toEqual(capture);
  });

  // Studio never sends "auto": the plate type is the slice's own, so the builder has no default
  // and carries it as given (sheets-04b paused on "auto" with 0500-8051, 2026-10-03).
  it("carries the slice's plate type as given", () => {
    expect(p.bed_type).toBe("textured_plate");
  });

  it("defaults the mapping to tray 0 and md5 to empty", () => {
    expect(p.ams_mapping).toEqual([0]);
    expect(p.ams_mapping2).toEqual([{ ams_id: 0, slot_id: 0 }]);
    expect(p.md5).toBe("");
  });
});

describe("buildProjectFileCommand — overrides", () => {
  it("selects a different plate for both param and default subtask name is unaffected by plate", () => {
    const p = buildProjectFileCommand({ remoteName: "card.3mf", bedType: "cool_plate", plate: 3 }).print;
    expect(p.param).toBe("Metadata/plate_3.gcode");
    expect(p.url).toBe("ftp:///card.3mf");
    expect(p.subtask_name).toBe("card");
  });

  it("passes the mapping and md5 through when set", () => {
    const p = buildProjectFileCommand({
      remoteName: "card.3mf",
      bedType: "textured_plate",
      amsMapping: [-1, 0],
      md5: "d41d8cd98f00b204e9800998ecf8427e",
    }).print;
    expect(p.bed_type).toBe("textured_plate");
    expect(p.ams_mapping).toEqual([-1, 0]);
    expect(p.ams_mapping2).toEqual([{ ams_id: 255, slot_id: 255 }, { ams_id: 0, slot_id: 0 }]);
    expect(p.md5).toBe("d41d8cd98f00b204e9800998ecf8427e");
  });

  // The X2D capture: ams_mapping [1, 0] beside ams_mapping2 [{0,1},{0,0}] (bambuddy #1192).
  it("matches the X2D capture's two mappings", () => {
    const p = buildProjectFileCommand({ remoteName: "card.3mf", bedType: "textured_plate", amsMapping: [1, 0] }).print;
    expect(p.ams_mapping).toEqual([1, 0]);
    expect(p.ams_mapping2).toEqual([{ ams_id: 0, slot_id: 1 }, { ams_id: 0, slot_id: 0 }]);
  });

  // A 254/255 in the flat list makes the printer raise 0700_8012 (bambuddy's notes): the external
  // spool is -1 there and named only in ams_mapping2.
  it("moves the external spool out of the flat mapping", () => {
    const p = buildProjectFileCommand({ remoteName: "card.3mf", bedType: "textured_plate", amsMapping: [254, 5] }).print;
    expect(p.ams_mapping).toEqual([-1, 5]);
    expect(p.ams_mapping2).toEqual([{ ams_id: 254, slot_id: 0 }, { ams_id: 1, slot_id: 1 }]);
  });

  it("accepts the empty-string ams_mapping form some firmware wants", () => {
    const p = buildProjectFileCommand({ remoteName: "card.3mf", bedType: "cool_plate", amsMapping: "" }).print;
    expect(p.ams_mapping).toBe("");
    expect(p.ams_mapping2).toEqual([]);
  });

  it("lets calibration steps be turned off individually", () => {
    const p = buildProjectFileCommand({
      remoteName: "card.3mf",
      bedType: "cool_plate",
      bedLeveling: 0,
      flowCali: 0,
      nozzleOffsetCali: 0,
    }).print;
    expect(p.auto_bed_leveling).toBe(0);
    expect(p.extrude_cali_flag).toBe(0);
    expect(p.nozzle_offset_cali).toBe(0);
    expect(p.bed_leveling).toBe(false);
    expect(p.flow_cali).toBe(false);
  });

  it("sets the old booleans only when a step is forced on", () => {
    const p = buildProjectFileCommand({
      remoteName: "card.3mf",
      bedType: "cool_plate",
      bedLeveling: 1,
      flowCali: 1,
      vibrationCali: true,
    }).print;
    expect(p.bed_leveling).toBe(true);
    expect(p.flow_cali).toBe(true);
    expect(p.vibration_cali).toBe(true);
  });

  it("honours an explicit subtask name and sequence id", () => {
    const p = buildProjectFileCommand({
      remoteName: "card.3mf",
      bedType: "cool_plate",
      subtaskName: "Plate 1 — machine card",
      sequenceId: "42",
    }).print;
    expect(p.subtask_name).toBe("Plate 1 — machine card");
    expect(p.sequence_id).toBe("42");
  });

  // false is a real value the builder must not clobber with its default (?? guards against exactly
  // this — a plain || would have flipped these back to true/on).
  it("preserves an explicitly-false flag rather than defaulting it back on", () => {
    const opts: ProjectFileOptions = { remoteName: "card.3mf", bedType: "cool_plate", timelapse: false, useAms: false };
    const p = buildProjectFileCommand(opts).print;
    expect(p.timelapse).toBe(false);
    expect(p.use_ams).toBe(false);
  });
});

describe("amsMapping2", () => {
  // The P2S capture (open-bamboo print ABI): [3,-1,-1] → [{0,3},{255,255},{255,255}].
  it("matches the P2S capture, unused filaments as 255/255", () => {
    expect(amsMapping2([3, -1, -1])).toEqual([
      { ams_id: 0, slot_id: 3 },
      { ams_id: 255, slot_id: 255 },
      { ams_id: 255, slot_id: 255 },
    ]);
  });

  it("splits a tray number into its unit and slot", () => {
    expect(amsMapping2([7, 8])).toEqual([{ ams_id: 1, slot_id: 3 }, { ams_id: 2, slot_id: 0 }]);
  });
});

describe("startSequenceId", () => {
  it("stays in the 20000s and moves with the clock", () => {
    expect(startSequenceId(0)).toBe("20000");
    expect(startSequenceId(1_000)).toBe("20001");
    expect(startSequenceId(9_999_000)).toBe("29999");
    expect(startSequenceId(10_000_000)).toBe("20000");
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
