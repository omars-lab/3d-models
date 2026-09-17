import { describe, expect, it } from "vitest";
import { buildHeader, renderHeader, headerToRecordProfile } from "./header.js";
import { parseProjectSettings, type PlateMeta } from "./threemf.js";
import type { PrinterStatus } from "./backends/mqtt.js";

// A pushall frame carrying a loaded AMS tray (the PASS-case shape the design names), plus the chamber
// the X2D reports. NO nozzle_diameter / nozzle_type — those are the X2D-unconfirmed frame fields.
const LOADED_FRAME: PrinterStatus = {
  ams: {
    ams: [{ id: "0", tray: [{ id: "0", tray_type: "PLA", tray_color: "F5547CFF", tray_sub_brands: "PLA Basic", tray_info_idx: "GFA00", remain: 84 }] }],
  },
  chamber_temper: 28,
  _age_seconds: 1,
};

// An X2D plate's project_settings.config (the fields the .3mf stamps), as JSON the reader parses.
const X2D_PLATE_JSON = JSON.stringify({
  printer_settings_id: ["Bambu Lab X2D 0.4 nozzle"],
  printer_model: ["Bambu Lab X2D"],
  nozzle_diameter: ["0.4", "0.4"],
  layer_height: ["0.2"],
  print_settings_id: ["0.20mm Standard @BBL X2D"],
  filament_settings_id: ["Bambu PLA Basic @BBL X2D 0.4 nozzle"],
  version: ["01.09.05.51"],
  "X-BBL-Client-Version": ["02.08.02.61"],
});

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

describe("buildHeader — PASS case (frame tray + X2D --plate)", () => {
  const plate = parseProjectSettings(X2D_PLATE_JSON);
  const h = buildHeader(LOADED_FRAME, plate, new Date("2026-09-17T12:00:00Z"));

  it("fills material type / colour / brand from the AMS tray", () => {
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
    expect(text).toContain("COLOUR #F5547C");
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
    // nozzle_type was not observed on the frame → it must NOT be pre-filled in the record.
    expect(profile.nozzle_type).toBeUndefined();
  });
});

describe("buildHeader — FAIL guard (frame has no nozzle, no --plate)", () => {
  // The design's by-design FAIL: a header that fabricates a nozzle diameter the machine did not answer.
  const h = buildHeader(LOADED_FRAME, null, new Date("2026-09-17T12:00:00Z"));

  it("marks nozzle diameter todo-plate — it does NOT fabricate one from the frame", () => {
    expect(h.nozzle_diameter.state).toBe("todo-plate");
    expect(h.nozzle_diameter.value).toBeNull();
  });

  it("marks the frame nozzle cross-check unconfirmed (not observed on this X2D)", () => {
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
