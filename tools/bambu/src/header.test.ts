import { describe, expect, it } from "vitest";
import { buildHeader, renderHeader, headerToRecordProfile, describeNozzleType } from "./header.js";
import { parseNozzleSides, parseProjectSettings, type PlateMeta } from "./threemf.js";
import type { PrinterStatus } from "./backends/mqtt.js";

// A pushall frame carrying a loaded AMS tray, plus the chamber, and NO nozzle fields — the shape of a
// frame that did not carry them, which must leave the nozzle type a blank rather than guess one.
const LOADED_FRAME: PrinterStatus = {
  ams: {
    ams: [{ id: "0", tray: [{ id: "0", tray_type: "PLA", tray_color: "F5547CFF", tray_sub_brands: "PLA Basic", tray_info_idx: "GFA00", remain: 84 }] }],
  },
  chamber_temper: 28,
  _age_seconds: 1,
};

// The same frame with the nozzle fields as the X2D reported them live on 2026-10-09 (during spl-2):
// a top-level code and size, and one `device.nozzle.info[]` entry per nozzle (id 0 right, 1 left).
const X2D_REPORT_FRAME: PrinterStatus = {
  ...LOADED_FRAME,
  nozzle_type: "HS01",
  nozzle_diameter: "0.4",
  device: {
    nozzle: {
      info: [
        { id: 0, diameter: 0.4, type: "HS01", wear: 0, sn: "N/A" },
        { id: 1, diameter: 0.4, type: "HS01", wear: 0, sn: "N/A" },
      ],
    },
  },
};

// An X2D plate's project_settings.config (the fields the .3mf stamps), as JSON the reader parses.
// filament_map / physical_extruder_map / the line widths are as every X2D plate since sheets-04 has them.
const X2D_PLATE_JSON = JSON.stringify({
  printer_settings_id: ["Bambu Lab X2D 0.4 nozzle"],
  printer_model: ["Bambu Lab X2D"],
  nozzle_diameter: ["0.4", "0.4"],
  layer_height: ["0.2"],
  line_width: "0.42",
  outer_wall_line_width: "0.42",
  filament_map: ["1"],
  physical_extruder_map: ["1", "0"],
  print_settings_id: ["0.20mm Standard @BBL X2D"],
  filament_settings_id: ["Bambu PLA Basic @BBL X2D 0.4 nozzle"],
  version: ["01.09.05.51"],
  "X-BBL-Client-Version": ["02.08.02.61"],
});

// slice_info.config, cut down from spl-1's: plate 1 prints filament 1, its own map puts it on 1 (left).
const sliceInfo = (filamentMaps: string, filaments = [1]) => `<?xml version="1.0" encoding="UTF-8"?>
<config>
  <plate>
    <metadata key="index" value="1"/>
    <metadata key="filament_maps" value="${filamentMaps}"/>
    ${filaments.map((id) => `<filament id="${id}" type="PLA" color="#00AE42" used_g="18.72"/>`).join("\n    ")}
  </plate>
</config>`;

/** The X2D plate with its nozzle sides read from slice_info, as readPlateMeta builds it. */
function x2dPlate(): PlateMeta {
  const plate = parseProjectSettings(X2D_PLATE_JSON);
  plate.nozzleSides = parseNozzleSides(X2D_PLATE_JSON, sliceInfo("1"));
  return plate;
}

describe("parseProjectSettings", () => {
  it("pulls the slice-side fields out of the .3mf config, unwrapping BambuStudio's array values", () => {
    const meta = parseProjectSettings(X2D_PLATE_JSON);
    expect(meta.machine).toBe("Bambu Lab X2D 0.4 nozzle");
    expect(meta.printerModel).toBe("Bambu Lab X2D");
    expect(meta.nozzleDiameters).toEqual(["0.4", "0.4"]);
    expect(meta.layerHeight).toBe("0.2");
    expect(meta.printSettingsId).toBe("0.20mm Standard @BBL X2D");
    expect(meta.filamentSettingsId).toBe("Bambu PLA Basic @BBL X2D 0.4 nozzle");
    expect(meta.slicerVersion).toBe("01.09.05.51");
  });

  it("returns an empty meta (never throws, never invents) on an unparseable config", () => {
    const meta = parseProjectSettings("{ not json");
    expect(meta.machine).toBeNull();
    expect(meta.nozzleDiameters).toEqual([]);
  });
});

describe("buildHeader — PASS case (X2D report + X2D --plate)", () => {
  const plate = x2dPlate();
  const h = buildHeader(X2D_REPORT_FRAME, plate, new Date("2026-09-17T12:00:00Z"));

  it("fills material type / color / brand from the AMS tray", () => {
    expect(h.material_type).toMatchObject({ value: "PLA", state: "filled" });
    expect(h.material_color).toMatchObject({ value: "#F5547C", state: "filled" });
    expect(h.material_brand).toMatchObject({ value: "PLA Basic", state: "filled" });
  });

  it("fills machine / layer / profile / slicer from the .3mf", () => {
    expect(h.machine).toMatchObject({ value: "Bambu Lab X2D 0.4 nozzle", state: "filled" });
    expect(h.layer_height).toMatchObject({ value: "0.2 mm", state: "filled" });
    expect(h.profile.value).toContain("0.20mm Standard @BBL X2D");
    expect(h.profile.value).toContain("Bambu PLA Basic @BBL X2D 0.4 nozzle");
    expect(h.slicer_version).toMatchObject({ state: "filled" });
  });

  it("fills the authoritative nozzle diameter from the .3mf (not the frame)", () => {
    expect(h.nozzle_diameter).toMatchObject({ value: "0.4,0.4 mm", state: "filled", source: ".3mf nozzle_diameter" });
  });

  it("leaves the genuinely-manual fields as blanks, never machine-known", () => {
    for (const f of [h.ambient_room_c, h.enclosure, h.settings_changed, h.caliper]) {
      expect(f.state).toBe("manual");
      expect(f.value).toBeNull();
    }
  });

  it("prints chamber on its OWN line and never into ambient room temp", () => {
    expect(h.chamber_c).toMatchObject({ value: "28°C", state: "filled" });
    expect(h.ambient_room_c.state).toBe("manual"); // chamber must NOT leak into room
    const text = renderHeader(h);
    expect(text).toContain("chamber (printer proxy, NOT room temp): 28°C");
    expect(text).toContain("Ambient   room ~____°C   enclosure: open / closed");
  });

  it("renders the bench-sheet block with the filled values", () => {
    const text = renderHeader(h);
    expect(text).toContain("Bambu Lab X2D 0.4 nozzle");
    expect(text).toContain("type PLA");
    expect(text).toContain("COLOR #F5547C");
    expect(text).toContain("diameter 0.4,0.4 mm");
    expect(text).toContain("Date      2026-09-17");
  });

  it("maps only genuinely-filled fields into the record profile (print send --record reuse)", () => {
    const profile = headerToRecordProfile(h);
    expect(profile.machine).toBe("Bambu Lab X2D 0.4 nozzle");
    expect(profile.material).toContain("PLA");
    expect(profile.nozzle_mm).toBe("0.4,0.4 mm");
    expect(profile.layer_mm).toBe("0.2 mm");
    expect(profile.slicer_profile).toContain("0.20mm Standard @BBL X2D");
    // The report carries the nozzle code (X2D, 2026-10-09), so the record gets it, spelled out.
    expect(profile.nozzle_type).toBe("HS01 (standard flow, hardened steel)");
    expect(profile.nozzle_side).toBe("left");
  });

  it("fills the nozzle type from the report entry for the nozzle the slice used", () => {
    expect(h.nozzle_type).toMatchObject({ value: "HS01 (standard flow, hardened steel)", state: "filled" });
    expect(h.nozzle_type.source).toContain("device.nozzle.info id 1");
    expect(h.nozzle_side).toMatchObject({ value: "left", state: "filled" });
    expect(h.nozzle_diameter_frame).toMatchObject({ value: "0.4 mm", state: "filled" });
    expect(renderHeader(h)).toContain("which nozzle: left");
  });

  it("names the used nozzle's type, not the other one's, when the two differ", () => {
    const frame: PrinterStatus = {
      ...X2D_REPORT_FRAME,
      device: { nozzle: { info: [{ id: 0, type: "HH01" }, { id: 1, type: "HS00" }] } },
    };
    expect(buildHeader(frame, plate).nozzle_type.value).toBe("HS00 (standard flow, stainless steel)");
  });
});

describe("buildHeader — a frame without nozzle fields", () => {
  it("leaves the nozzle type a blank for the operator, never a guess", () => {
    const h = buildHeader(LOADED_FRAME, x2dPlate());
    expect(h.nozzle_type).toMatchObject({ value: null, state: "manual" });
    expect(headerToRecordProfile(h).nozzle_type).toBeUndefined();
  });

  it("falls back to the top-level code when the per-nozzle list is absent", () => {
    const frame: PrinterStatus = { ...LOADED_FRAME, nozzle_type: "HS01" };
    expect(buildHeader(frame, x2dPlate()).nozzle_type).toMatchObject({
      value: "HS01 (standard flow, hardened steel)",
      source: "report nozzle_type",
    });
  });
});

describe("describeNozzleType", () => {
  it("reads the code the way Bambu Studio does: flow letter, then material digits", () => {
    expect(describeNozzleType("HS01")).toBe("standard flow, hardened steel");
    expect(describeNozzleType("HH01")).toBe("high flow, hardened steel");
    expect(describeNozzleType("HS00")).toBe("standard flow, stainless steel");
    expect(describeNozzleType("HS05")).toBe("standard flow, tungsten carbide");
  });

  it("gives null for a code it cannot read, so the raw code stands alone", () => {
    expect(describeNozzleType("N/A")).toBeNull();
    expect(describeNozzleType("HZ01")).toBeNull();
    expect(describeNozzleType("HS99")).toBeNull();
  });
});

describe("parseNozzleSides", () => {
  it("puts filament 1 on the left when the plate map says 1 and the physical map agrees", () => {
    expect(parseNozzleSides(X2D_PLATE_JSON, sliceInfo("1"))).toEqual([
      expect.objectContaining({ filament: 1, side: "left", physicalId: 1 }),
    ]);
  });

  it("lets the plate's own map win over the project-wide one", () => {
    const sides = parseNozzleSides(X2D_PLATE_JSON, sliceInfo("1 2", [1, 2]));
    expect(sides.map((s) => s.side)).toEqual(["left", "right"]);
    expect(sides.map((s) => s.physicalId)).toEqual([1, 0]);
  });

  it("falls back to the project filament_map when the plate has no map", () => {
    const xml = sliceInfo("1").replace(/\s*<metadata key="filament_maps"[^>]*>/, "");
    expect(parseNozzleSides(X2D_PLATE_JSON, xml)[0]).toMatchObject({ side: "left" });
    expect(parseNozzleSides(X2D_PLATE_JSON, xml)[0]!.why).toContain("project filament_map");
  });

  it("gives NO side when the file disagrees with itself (minis-03/04: physical_extruder_map [\"0\"])", () => {
    // The by-design FAIL: filament_map 1 says left, but the one-entry physical map names nozzle 0
    // (right). Picking either would be a guess, so the side is blank and both readings are named.
    const minis = JSON.stringify({ ...JSON.parse(X2D_PLATE_JSON), physical_extruder_map: ["0"] });
    const [only] = parseNozzleSides(minis, sliceInfo("1"));
    expect(only).toMatchObject({ filament: 1, side: null, physicalId: null });
    expect(only!.why).toContain("says left");
    expect(only!.why).toContain('["0"]');
    const plate = parseProjectSettings(minis);
    plate.nozzleSides = parseNozzleSides(minis, sliceInfo("1"));
    const h = buildHeader(X2D_REPORT_FRAME, plate);
    expect(h.nozzle_side.state).toBe("unconfirmed");
    expect(headerToRecordProfile(h).nozzle_side).toBeUndefined();
    // No side → no way to say which nozzle's entry applies, so the top-level code is used instead.
    expect(h.nozzle_type.source).toBe("report nozzle_type");
  });

  it("gives no side for a map value that is neither 1 nor 2", () => {
    expect(parseNozzleSides(X2D_PLATE_JSON, sliceInfo("3"))[0]).toMatchObject({ side: null });
  });
});

describe("buildHeader — FAIL guard (frame has no nozzle, no --plate)", () => {
  // The design's by-design FAIL: a header that fabricates a nozzle diameter the machine did not answer.
  const h = buildHeader(LOADED_FRAME, null, new Date("2026-09-17T12:00:00Z"));

  it("marks nozzle diameter todo-plate — it does NOT fabricate one from the frame", () => {
    expect(h.nozzle_diameter.state).toBe("todo-plate");
    expect(h.nozzle_diameter.value).toBeNull();
  });

  it("marks which nozzle todo-plate — the side comes only from the .3mf", () => {
    expect(h.nozzle_side).toMatchObject({ value: null, state: "todo-plate" });
  });

  it("marks the frame nozzle cross-check unconfirmed when the frame did not carry it", () => {
    expect(h.nozzle_diameter_frame.state).toBe("unconfirmed");
    expect(h.nozzle_diameter_frame.value).toBeNull();
  });

  it("renders NO fabricated nozzle diameter — the nozzle line is a blank/TODO, not a number", () => {
    const text = renderHeader(h);
    const nozzleLine = text.split("\n").find((l) => l.startsWith("Nozzle"))!;
    expect(nozzleLine).not.toMatch(/\d+(\.\d+)?\s*mm/); // no mm figure invented
    expect(nozzleLine).toContain("TODO — pass --plate");
  });

  it("leaves the slice-side fields as TODO — pass --plate (no invented machine/profile)", () => {
    for (const f of [h.machine, h.layer_height, h.profile, h.slicer_version]) {
      expect(f.state).toBe("todo-plate");
      expect(f.value).toBeNull();
    }
  });

  it("marks firmware unconfirmed (MQTT get_version not sent) and points at the SSDP source", () => {
    expect(h.firmware.state).toBe("unconfirmed");
    expect(h.firmware.source).toContain("setup discover");
  });
});

describe("buildHeader — spool id / third-party material honesty", () => {
  it("marks spool id unconfirmed when the frame carried no tray_uuid", () => {
    const h = buildHeader(LOADED_FRAME, null);
    expect(h.spool_id.state).toBe("unconfirmed");
  });

  it("fills spool id only when the frame actually carried tray_uuid", () => {
    const frame: PrinterStatus = { ams: { ams: [{ id: "0", tray: [{ id: "0", tray_type: "PLA", tray_uuid: "ABC123" }] }] } };
    expect(buildHeader(frame, null).spool_id).toMatchObject({ value: "ABC123", state: "filled" });
  });

  it("marks brand manual for a third-party spool (no RFID sub-brand)", () => {
    const frame: PrinterStatus = { ams: { ams: [{ id: "0", tray: [{ id: "0", tray_type: "PETG", tray_color: "00FF00FF" }] }] } };
    expect(buildHeader(frame, null).material_brand.state).toBe("manual");
  });
});

describe("buildHeader — nozzle cross-check mismatch", () => {
  it("shouts when the loaded nozzle (frame) disagrees with the sliced-for nozzle (.3mf)", () => {
    const frame: PrinterStatus = { ...LOADED_FRAME, nozzle_diameter: "0.6" };
    const plate = parseProjectSettings(X2D_PLATE_JSON); // sliced for 0.4
    const h = buildHeader(frame, plate);
    expect(h.nozzle_mismatch).toBeTruthy();
    expect(renderHeader(h)).toContain("⚠ NOZZLE MISMATCH");
  });

  it("does not flag a mismatch when frame and .3mf agree", () => {
    const frame: PrinterStatus = { ...LOADED_FRAME, nozzle_diameter: ["0.4", "0.4"] };
    const h = buildHeader(frame, parseProjectSettings(X2D_PLATE_JSON));
    expect(h.nozzle_mismatch).toBeNull();
  });
});

describe("secret safety", () => {
  it("the header object + rendered text never carry a token (the builder never sees config)", () => {
    const FAKE_TOKEN = "deadbeef-not-a-real-token";
    // Even if a token-shaped value somehow appeared in the frame, the builder reads only known fields.
    const frame: PrinterStatus = { ...LOADED_FRAME, access_code: FAKE_TOKEN, token: FAKE_TOKEN };
    const h = buildHeader(frame, parseProjectSettings(X2D_PLATE_JSON));
    const json = JSON.stringify(h);
    expect(json).not.toContain(FAKE_TOKEN);
    expect(json).not.toContain("BAMBU_TOKEN");
    expect(renderHeader(h)).not.toContain(FAKE_TOKEN);
  });
});
