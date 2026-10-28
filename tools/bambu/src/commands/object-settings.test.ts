import { describe, expect, it } from "vitest";
import {
  injectObjectSettings,
  objectSettingsMissing,
  parseManifest,
  primeTowerDroppedByStudio,
  readObjectSettings,
} from "./compose.js";
import { iterationId, type IterationKey } from "../iteration.js";

// The shape Studio writes into an arranged plate's Metadata/model_settings.config (cut down from the
// bedface-2 trial, 2026-10-11): object-level lines first, then the part's own.
const object = (id: number, name: string, extra = "") =>
  `  <object id="${id}">\n` +
  `    <metadata key="name" value="${name}"/>\n` +
  extra +
  `    <metadata key="extruder" value="1"/>\n` +
  `    <metadata face_count="120"/>\n` +
  `    <part id="${id - 1}" subtype="normal_part">\n` +
  `      <metadata key="name" value="${name}"/>\n` +
  `      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 2.2 0 0 0 1"/>\n` +
  `    </part>\n` +
  `  </object>\n`;
const config = (...objects: string[]) =>
  `<?xml version="1.0" encoding="UTF-8"?>\n<config>\n${objects.join("")}  <plate>\n  </plate>\n</config>\n`;

const RINGS = { bottom_surface_pattern: "concentric", infill_wall_overlap: "30%" };

const recipe = (settings: string) => `
profile: { settings: "m;p", filament: "f" }
items:
  - bkr: "bikar:patterns/coaster.bkr"
${settings}`;

describe("object_settings: — parsed against the allowed list", () => {
  it("takes the rings and the overlap on a bkr item", () => {
    const m = parseManifest(recipe('    object_settings: { bottom_surface_pattern: concentric, infill_wall_overlap: "30%" }'));
    expect((m.items[0] as { object_settings?: unknown }).object_settings).toEqual(RINGS);
  });

  it("refuses the first-layer line width, saying why", () => {
    expect(() => parseManifest(recipe("    object_settings: { initial_layer_line_width: 0.42 }"))).toThrow(
      /initial_layer_line_width` cannot be set per piece: .*research\/2026-10-10-bed-face-per-piece/,
    );
  });

  it("refuses a setting not on the list, and a value Studio does not take", () => {
    expect(() => parseManifest(recipe("    object_settings: { top_surface_pattern: concentric }"))).toThrow(
      /not one Studio was seen to honor per piece/,
    );
    expect(() => parseManifest(recipe("    object_settings: { bottom_surface_pattern: concentirc }"))).toThrow(
      /takes monotonic, monotonicline, concentric/,
    );
    expect(() => parseManifest(recipe("    object_settings: { infill_wall_overlap: 30 }"))).toThrow(/a percent/);
    expect(() => parseManifest(recipe("    object_settings: {}"))).toThrow(/is empty/);
  });

  it("takes a first-layer flow as text, and refuses a bare number, one out of range, or a trailing zero", () => {
    const m = parseManifest(recipe('    object_settings: { initial_layer_flow_ratio: "1.05" }'));
    expect((m.items[0] as { object_settings?: unknown }).object_settings).toEqual({ initial_layer_flow_ratio: "1.05" });
    expect(() => parseManifest(recipe('    object_settings: { initial_layer_flow_ratio: "1.1" }'))).not.toThrow();
    expect(() => parseManifest(recipe("    object_settings: { initial_layer_flow_ratio: 1.05 }"))).toThrow(/as text/);
    expect(() => parseManifest(recipe('    object_settings: { initial_layer_flow_ratio: "1.5" }'))).toThrow(/0.8 to 1.2/);
    // Studio writes 1.10 back as 1.1, so the read-back would fail a slice that holds it.
    expect(() => parseManifest(recipe('    object_settings: { initial_layer_flow_ratio: "1.10" }'))).toThrow(/no trailing zero/);
  });

  it("takes supports under one piece as \"1\", and refuses \"0\" or a bare number", () => {
    const m = parseManifest(recipe('    object_settings: { enable_support: "1" }'));
    expect((m.items[0] as { object_settings?: unknown }).object_settings).toEqual({ enable_support: "1" });
    // Off is the preset's own value, so it is written by leaving the key out, not as "0".
    expect(() => parseManifest(recipe('    object_settings: { enable_support: "0" }'))).toThrow(/leave it out/);
    expect(() => parseManifest(recipe("    object_settings: { enable_support: 1 }"))).toThrow();
  });

  it("takes a base under one piece: grid supports, a raft, or a brim, and refuses values Studio would drop", () => {
    const grid = parseManifest(recipe('    object_settings: { enable_support: "1", support_type: "normal(auto)" }'));
    expect((grid.items[0] as { object_settings?: unknown }).object_settings).toEqual({
      enable_support: "1",
      support_type: "normal(auto)",
    });
    const brim = parseManifest(recipe('    object_settings: { brim_type: "outer_only", brim_width: "5" }'));
    expect((brim.items[0] as { object_settings?: unknown }).object_settings).toEqual({ brim_type: "outer_only", brim_width: "5" });
    expect(() => parseManifest(recipe('    object_settings: { raft_layers: "2" }'))).not.toThrow();
    expect(() => parseManifest(recipe('    object_settings: { raft_layers: "0" }'))).toThrow(/leave it out/);
    expect(() => parseManifest(recipe('    object_settings: { support_type: "normal" }'))).toThrow(/normal\(auto\)/);
    expect(() => parseManifest(recipe('    object_settings: { brim_width: "5.5" }'))).toThrow(/whole mm/);
    expect(() => parseManifest(recipe('    object_settings: { brim_type: "auto_brim" }'))).toThrow();
  });

  it("refuses it on an item that is not rendered from bikar", () => {
    const text = `
profile: { settings: "m;p", filament: "f" }
items:
  - iteration: it-0123456789ab
    object_settings: { bottom_surface_pattern: concentric }`;
    expect(() => parseManifest(text)).toThrow(/only a `bkr:` item takes `object_settings:`/);
  });
});

describe("the iteration id — settings are part of the recipe", () => {
  const key: IterationKey = {
    source: "bikar:patterns/coaster.bkr@abc",
    source_sha256: "0".repeat(64),
    piece: "",
    params: { size: 112.5 },
    slice_profile: { settings: "m;p", filament: "f" },
  };
  it("the same mesh with rings gets another id; with none, the id is the key's as before", () => {
    const none: Record<string, string> | undefined = [][0];
    const spreadNone = { ...key, ...(none ? { object_settings: none } : {}) };
    expect(iterationId(spreadNone)).toBe(iterationId(key));
    expect(iterationId({ ...key, object_settings: RINGS })).not.toBe(iterationId(key));
  });
});

describe("injectObjectSettings + readObjectSettings — written in, read back", () => {
  const xml = config(object(2, "it-aaaaaaaaaaaa.stl"), object(4, "it-bbbbbbbbbbbb.stl"), object(6, "it-aaaaaaaaaaaa.stl"));

  it("writes the settings into every copy of the named piece and nowhere else", () => {
    const out = injectObjectSettings(xml, new Map([["it-aaaaaaaaaaaa.stl", RINGS]]));
    const read = readObjectSettings(out);
    expect(read.map((o) => o.name)).toEqual(["it-aaaaaaaaaaaa.stl", "it-bbbbbbbbbbbb.stl", "it-aaaaaaaaaaaa.stl"]);
    expect(read[0]!.settings).toEqual({ ...RINGS, extruder: "1" });
    expect(read[1]!.settings).toEqual({ extruder: "1" });
    expect(read[2]!.settings).toEqual({ ...RINGS, extruder: "1" });
    expect(out.match(/<metadata key="matrix"/g)).toHaveLength(3); // the parts are untouched
  });

  it("throws when the arranged plate has no object of that name", () => {
    expect(() => injectObjectSettings(xml, new Map([["it-cccccccccccc.stl", RINGS]]))).toThrow(/no object named it-cccccccccccc/);
  });

  it("throws rather than overwrite a setting the object already holds", () => {
    const held = config(object(2, "it-aaaaaaaaaaaa.stl", '    <metadata key="infill_wall_overlap" value="15%"/>\n'));
    expect(() => injectObjectSettings(held, new Map([["it-aaaaaaaaaaaa.stl", RINGS]]))).toThrow(/already sets infill_wall_overlap/);
  });
});

describe("objectSettingsMissing — the read-back that fails a slice", () => {
  const want = [{ name: "it-aaaaaaaaaaaa.stl", count: 2, settings: RINGS }];

  it("passes when every copy carries every setting", () => {
    const sliced = readObjectSettings(injectObjectSettings(
      config(object(2, "it-aaaaaaaaaaaa.stl"), object(4, "it-aaaaaaaaaaaa.stl")),
      new Map([["it-aaaaaaaaaaaa.stl", RINGS]]),
    ));
    expect(objectSettingsMissing(sliced, want)).toEqual([]);
  });

  it("fails when Studio dropped a setting from one copy", () => {
    const sliced = readObjectSettings(config(
      object(2, "it-aaaaaaaaaaaa.stl", '    <metadata key="bottom_surface_pattern" value="concentric"/>\n    <metadata key="infill_wall_overlap" value="30%"/>\n'),
      object(4, "it-aaaaaaaaaaaa.stl", '    <metadata key="bottom_surface_pattern" value="concentric"/>\n'),
    ));
    expect(objectSettingsMissing(sliced, want)).toEqual([
      "it-aaaaaaaaaaaa.stl: infill_wall_overlap is (absent) in the slice, the recipe sets 30%",
    ]);
  });

  it("fails when a piece with no settings carries one, so the stock piece is stock", () => {
    const sliced = readObjectSettings(injectObjectSettings(
      config(object(2, "it-aaaaaaaaaaaa.stl"), object(4, "it-aaaaaaaaaaaa.stl"),
        object(6, "it-bbbbbbbbbbbb.stl", '    <metadata key="bottom_surface_pattern" value="concentric"/>\n')),
      new Map([["it-aaaaaaaaaaaa.stl", RINGS]]),
    ));
    expect(objectSettingsMissing(sliced, want)).toEqual([
      "it-bbbbbbbbbbbb.stl: bottom_surface_pattern is concentric in the slice, the recipe sets none for it",
    ]);
  });

  it("fails when a copy is missing from the slice", () => {
    const sliced = readObjectSettings(injectObjectSettings(config(object(2, "it-aaaaaaaaaaaa.stl")), new Map([["it-aaaaaaaaaaaa.stl", RINGS]])));
    expect(objectSettingsMissing(sliced, want)).toEqual(["it-aaaaaaaaaaaa.stl: 1 object(s) in the slice, 2 expected"]);
  });
});

describe("primeTowerDroppedByStudio — the one mismatch a two-pass slice may carry", () => {
  const LOG = "[warning] disable_wipe_tower_after_mapping: disable prime tower for only one filament!";
  const tower = { preset: "p", key: "enable_prime_tower", expected: "1", actual: "0" };

  it("allows the prime tower off on a one-filament plate when Studio says it turned it off", () => {
    expect(primeTowerDroppedByStudio(tower, 1, LOG)).toBe(true);
  });

  it("allows nothing else: another key, two filaments, no log line, or the other way round", () => {
    expect(primeTowerDroppedByStudio({ ...tower, key: "bottom_surface_pattern", expected: "monotonic", actual: "concentric" }, 1, LOG)).toBe(false);
    expect(primeTowerDroppedByStudio(tower, 2, LOG)).toBe(false);
    expect(primeTowerDroppedByStudio(tower, 1, "")).toBe(false);
    expect(primeTowerDroppedByStudio({ ...tower, expected: "0", actual: "1" }, 1, LOG)).toBe(false);
  });
});
