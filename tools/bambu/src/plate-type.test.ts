import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import {
  PLATE_TYPES,
  checkPlate,
  parsePlateTypeFlag,
  parseSlicePlateType,
  parseStudioSavedPlateType,
  plateTypeFromName,
  plateTypeFromToken,
  printerPlateId,
  resolveSlicePlateType,
  studioSavedPlateType,
} from "./plate-type.js";
import { setPlateType } from "./commands/slice.js";
import type { FlattenedPreset } from "./preset-chain.js";

// The plate type is what sheets-04b got wrong (2026-10-03): sliced for Studio's CLI default, a Cool
// Plate, while a Textured PEI Plate sat on the bed, then started as "auto". These pin the names to
// Studio's own and the order every reader uses.

const textured = plateTypeFromToken("textured_plate")!;
const cool = plateTypeFromToken("cool_plate")!;

describe("the plate types", () => {
  it("are Studio's five, each with its token, config name and enum number", () => {
    expect(PLATE_TYPES.map((p) => [p.index, p.token, p.name])).toEqual([
      [1, "cool_plate", "Cool Plate"],
      [2, "eng_plate", "Engineering Plate"],
      [3, "hot_plate", "High Temp Plate"],
      [4, "textured_plate", "Textured PEI Plate"],
      [5, "supertack_plate", "Supertack Plate"],
    ]);
    for (const p of PLATE_TYPES) {
      expect(plateTypeFromToken(p.token)).toBe(p);
      expect(plateTypeFromName(p.name)).toBe(p);
    }
  });

  it("refuse a flag that is not one of them, auto included", () => {
    expect(parsePlateTypeFlag(" Textured_Plate ")).toBe(textured);
    expect(() => parsePlateTypeFlag("auto")).toThrow(/unknown plate type "auto".*cool_plate/);
  });
});

describe("parseSlicePlateType", () => {
  it("reads the plate's own bed_type first, as Studio's send does", () => {
    const got = parseSlicePlateType('{"bed_type":"textured_plate"}', '{"curr_bed_type":"Cool Plate"}', 1);
    expect(got).toEqual({ type: textured, from: "Metadata/plate_1.json" });
  });

  it("falls back to the project's curr_bed_type", () => {
    const got = parseSlicePlateType('{"nozzle_diameter":0.4}', '{"curr_bed_type":"Cool Plate"}', 2);
    expect(got).toEqual({ type: cool, from: "Metadata/project_settings.config" });
    expect(parseSlicePlateType(null, '{"curr_bed_type":"Cool Plate"}').type).toBe(cool);
  });

  it("names what it found when the type is unknown or missing", () => {
    expect(parseSlicePlateType('{"bed_type":"auto"}', null)).toEqual({
      type: null,
      from: 'Metadata/plate_1.json names "auto", not a plate type Studio knows',
    });
    expect(parseSlicePlateType(null, '{"curr_bed_type":"Glass"}').from).toMatch(/names "Glass"/);
    expect(parseSlicePlateType("not json", null).from).toMatch(/carries no plate type/);
  });
});

describe("Bambu Studio's saved plate type", () => {
  it("is the app section's curr_bed_type number, and nothing else is read", () => {
    // Omar's conf, 2026-10-03: app.curr_bed_type "4", and no top-level key. A curr_bed_type anywhere
    // else (top level, a preset's) must not be taken for it.
    expect(parseStudioSavedPlateType('{"app":{"curr_bed_type":"4"},"presets":{"curr_bed_type":"1"}}')).toBe(textured);
    expect(parseStudioSavedPlateType('{"curr_bed_type":"4","presets":{"curr_bed_type":"1"}}')).toBeNull();
    expect(parseStudioSavedPlateType('{"app":{"curr_bed_type":"0"}}')).toBeNull(); // btDefault names no plate
    expect(parseStudioSavedPlateType("{broken")).toBeNull();
  });

  it("is null when there is no conf", () => {
    const dir = mkdtempSync(join(tmpdir(), "plate-type-"));
    expect(studioSavedPlateType(join(dir, "BambuStudio.conf"))).toBeNull();
    writeFileSync(join(dir, "BambuStudio.conf"), '{"app":{"curr_bed_type":"1"}}');
    expect(studioSavedPlateType(join(dir, "BambuStudio.conf"))).toBe(cool);
  });
});

describe("resolveSlicePlateType", () => {
  it("takes the flag, then Studio's saved type, and never Studio's Cool Plate default", () => {
    expect(resolveSlicePlateType("cool_plate", textured)).toEqual({ type: cool, from: "--plate-type" });
    expect(resolveSlicePlateType(undefined, textured)).toEqual({ type: textured, from: "Bambu Studio's saved plate type" });
    expect(() => resolveSlicePlateType(undefined, null)).toThrow(/no plate type.*--plate-type/);
  });
});

describe("checkPlate", () => {
  const slice = { type: textured, from: "Metadata/plate_1.json" };

  it("refuses a slice that names no plate type", () => {
    const c = checkPlate({ type: null, from: "the file carries no plate type" }, "P0101");
    expect([c.ok, c.mark]).toEqual([false, "✗"]);
  });

  it("warns, and points at the photo, when the printer names no plate or one we have not matched", () => {
    expect(checkPlate(slice, null)).toMatchObject({ ok: true, mark: "⚠" });
    const c = checkPlate(slice, "P0999");
    expect([c.ok, c.mark]).toEqual([true, "⚠"]);
    expect(c.line).toMatch(/P0999.*bed photo/);
  });

  it("refuses a known plate that is not the one the slice is for — the sheets-04b case", () => {
    const c = checkPlate({ type: cool, from: "Metadata/plate_1.json" }, "P0101");
    expect([c.ok, c.mark]).toEqual([false, "✗"]);
    expect(c.line).toMatch(/Cool Plate.*P0101, a Textured PEI Plate/);
  });

  it("passes a match", () => {
    expect(checkPlate(slice, "P0101")).toMatchObject({ ok: true, mark: "✓" });
  });
});

describe("printerPlateId", () => {
  it("reads device.plate.cur_id and nothing that is not a string", () => {
    expect(printerPlateId({ device: { plate: { cur_id: " P0101 " } } })).toBe("P0101");
    expect(printerPlateId({ device: { plate: { cur_id: 5 } } })).toBeNull();
    expect(printerPlateId({ device: {} })).toBeNull();
    expect(printerPlateId(null)).toBeNull();
  });
});

describe("setPlateType", () => {
  const preset = (type: string): FlattenedPreset => ({ leaf: `/p/${type}.json`, type, chain: [type], config: { name: type } });

  it("writes the plate name into the process preset only, and onto its file", () => {
    const dir = mkdtempSync(join(tmpdir(), "plate-type-"));
    const presets = [preset("machine"), preset("process"), preset("filament")];
    setPlateType(presets, textured, dir);
    expect(presets[1]!.config.curr_bed_type).toBe("Textured PEI Plate");
    expect(presets[0]!.config.curr_bed_type).toBeUndefined();
    expect(JSON.parse(readFileSync(join(dir, "process.json"), "utf8")).curr_bed_type).toBe("Textured PEI Plate");
  });

  it("refuses settings with no process preset to hold it", () => {
    expect(() => setPlateType([preset("machine")], textured, mkdtempSync(join(tmpdir(), "plate-type-")))).toThrow(
      /needs a process preset/,
    );
  });
});
