import { afterEach, describe, expect, it, vi } from "vitest";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { Command } from "commander";
import { collectSlots } from "./frame.js";
import { physicalTraysFromSlots, type PhysicalTray } from "./filament-sync.js";
import { designColorsFromByColor, mapColors, renderColorMap, traysFromFilamentJson, type MapRow } from "./filament-map.js";
import { MqttBackend, type PrinterStatus } from "./backends/mqtt.js";
import { buildProgram } from "./program.js";

// `bambu filament map` (print-time-color-map-design §3, §4, §10): each design color of a
// `plates by-color --json` run goes through the send's own `reconcile` against every loaded tray at
// once, so one tray never serves two design colors. The trays come in through the real frame parser
// (collectSlots → physicalTraysFromSlots), in the X2D shape seen 2026-09-17: `ams.ams[].tray[]`,
// empty trays as `{id, state}`, and the external spool as a `vir_slot` array with id "254".

const PINK = "#F5547C"; // the pink phones-01 and phones-02 print in
const BLACK = "#000000";
const GOLD = "#C8A24A"; // §10's gold
const TAN = "#C9A44C"; // §10's tan: 3 from the gold

type T = { id: string; color?: string; type?: string; remain?: number };
function trays(list: T[]): PhysicalTray[] {
  const frame = {
    ams: {
      ams: [
        {
          id: "0",
          tray: list.map((t) =>
            t.color ? { id: t.id, tray_type: t.type ?? "PLA", tray_color: `${t.color.slice(1)}FF`, remain: t.remain ?? 80 } : { id: t.id, state: 0 },
          ),
        },
      ],
    },
    vir_slot: [{ id: "254", tray_type: "", tray_color: "00000000" }],
  } as unknown as PrinterStatus;
  return physicalTraysFromSlots(collectSlots(frame));
}

// Rows in the shape `plates by-color --json` prints (commands/plates.ts runByColor).
const C = "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr";
function byColor(list: Array<[hex: string, ...pieces: Array<string | null>]>): unknown {
  return list.map(([hex, ...pieces]) => {
    const name = `gbv-by-color-${hex.slice(1).toLowerCase()}`;
    return {
      name,
      path: `build/plates/by-color/gbv-by-color/${name}.yaml`,
      recipe_hash: "0".repeat(12),
      color: hex,
      items: pieces.map((piece) => ({ construction: C, params: { size: 112.5 }, piece, count: 1 })),
    };
  });
}

const row = (rows: MapRow[], hex: string): MapRow => {
  const r = rows.find((x) => x.design_hex === hex);
  if (!r) throw new Error(`no row for ${hex}`);
  return r;
};

describe("designColorsFromByColor", () => {
  it("reads name, path, color and the groups from each by-color row", () => {
    const colors = designColorsFromByColor(byColor([[PINK, "Kite", "Star"], [BLACK, null]]));
    expect(colors).toEqual([
      { name: "gbv-by-color-f5547c", path: "build/plates/by-color/gbv-by-color/gbv-by-color-f5547c.yaml", hex: PINK, groups: ["Kite", "Star"] },
      { name: "gbv-by-color-000000", path: "build/plates/by-color/gbv-by-color/gbv-by-color-000000.yaml", hex: BLACK, groups: ["frame"] },
    ]);
  });

  it("refuses a file that is not by-color's array, or a row with no hex, naming the row", () => {
    expect(() => designColorsFromByColor({ rows: [] })).toThrow(/JSON array/);
    expect(() => designColorsFromByColor([])).toThrow(/no plates/);
    expect(() => designColorsFromByColor([{ name: "a", color: "pink" }])).toThrow(/row 1 \(a\).*#RRGGBB/);
    expect(() => designColorsFromByColor([{ color: PINK }])).toThrow(/row 1: no "name"/);
  });
});

describe("mapColors: §10 PASS, a three-color gBV design", () => {
  const colors = designColorsFromByColor(byColor([[PINK, "Kite"], [BLACK, "Star"], [GOLD, null]]));

  it("pink and black loaded, gold not: pink and black each get their own tray, gold is missing", () => {
    const m = mapColors(colors, trays([{ id: "0", color: "#FFFFFF" }, { id: "1", color: PINK }, { id: "2" }, { id: "3", color: BLACK }]));
    const pink = row(m.rows, PINK);
    const black = row(m.rows, BLACK);
    const gold = row(m.rows, GOLD);
    expect([pink.status, pink.tray?.index, pink.tray?.hex, pink.distance]).toEqual(["matched", 1, PINK, 0]);
    expect([black.status, black.tray?.index, black.tray?.hex, black.distance]).toEqual(["matched", 3, BLACK, 0]);
    expect([gold.status, gold.tray, gold.distance]).toEqual(["missing", null, null]);
    // The nearest tray is still named, and that it already went to pink: "use the nearest" would
    // print two groups in one color, so the question has to say so.
    expect(gold.nearest).toMatchObject({ index: 1, hex: PINK, taken_by: "gbv-by-color-f5547c" });
    expect(gold.nearest!.distance).toBeCloseTo(103, 5);
    expect(m.ok).toBe(false);
    expect(m.needs_operator).toBe(true);
  });

  it("after gold is loaded, every color has its own tray: three rows, three different tray hexes", () => {
    const m = mapColors(colors, trays([{ id: "0", color: "#FFFFFF" }, { id: "1", color: PINK }, { id: "2", color: GOLD }, { id: "3", color: BLACK }]));
    expect(m.rows.map((r) => [r.design_hex, r.status, r.tray?.index])).toEqual([
      [PINK, "matched", 1],
      [BLACK, "matched", 3],
      [GOLD, "matched", 2],
    ]);
    for (const r of m.rows) expect(r.tray!.hex).toBe(r.design_hex); // each plate's --color is its own tray's hex
    expect(m.ok).toBe(true);
  });
});

describe("mapColors: §10 FAIL, gold and tan with one gold tray", () => {
  const colors = designColorsFromByColor(byColor([[GOLD, "Kite"], [TAN, "Star"]]));
  const loaded = trays([{ id: "0", color: GOLD }, { id: "1", color: BLACK }, { id: "2", color: "#FFFFFF" }]);

  it("a per-color nearest pick would give both the gold tray: the failure this guards against is real", () => {
    // Each color mapped on its own, as a second matcher that skipped reconcile would do.
    const alone = [GOLD, TAN].map((hex) => mapColors(colors.filter((c) => c.hex === hex), loaded).rows[0]!);
    expect(alone.map((r) => [r.status, r.tray?.index])).toEqual([
      ["matched", 0],
      ["matched", 0],
    ]);
  });

  it("mapped together, gold keeps the gold tray and tan does not also get it", () => {
    const m = mapColors(colors, loaded);
    const gold = row(m.rows, GOLD);
    const tan = row(m.rows, TAN);
    expect([gold.status, gold.tray?.index]).toEqual(["matched", 0]);
    expect([tan.status, tan.tray]).toEqual(["missing", null]);
    expect(tan.nearest).toMatchObject({ index: 0, hex: GOLD, taken_by: "gbv-by-color-c8a24a" });
    expect(tan.nearest!.distance).toBe(3);
    // Per color, not a count: no tray hex is held by two rows.
    const held = m.rows.flatMap((r) => (r.tray ? [r.tray.hex] : []));
    expect(new Set(held).size).toBe(held.length);
    expect(renderColorMap(m)).toContain("already given to gbv-by-color-c8a24a");
  });

  it("with a second gold-ish tray loaded, tan takes that one and is asked about, since the gold tray is as close", () => {
    const m = mapColors(colors, trays([{ id: "0", color: GOLD }, { id: "1", color: "#E0B050" }]));
    const tan = row(m.rows, TAN);
    expect(row(m.rows, GOLD).tray?.index).toBe(0);
    expect([tan.status, tan.tray?.index, tan.runner_up?.index]).toEqual(["ambiguous", 1, 0]);
    expect(tan.distance).toBeCloseTo(26.25, 2);
  });
});

describe("mapColors: what each row says about the tray", () => {
  const colors = designColorsFromByColor(byColor([[PINK, "Kite"]]));

  it("marks a spool with no tag (remain -1), whose color was set by hand", () => {
    const m = mapColors(colors, trays([{ id: "0", color: PINK, remain: -1 }]));
    expect(m.rows[0]!.tray).toMatchObject({ remain: -1, tagged: false });
    expect(m.rows[0]!.status).toBe("matched"); // -1 is "unknown", not low
    expect(renderColorMap(m)).toContain("no tag");
  });

  it("gives low-remain for a tagged spool at 10% or less, still mapped", () => {
    const m = mapColors(colors, trays([{ id: "0", color: PINK, remain: 5 }]));
    expect(m.rows[0]).toMatchObject({ status: "low-remain", tray: { index: 0, tagged: true, remain: 5 } });
    expect(m.ok).toBe(true);
    expect(m.needs_operator).toBe(false);
  });

  it("lists every loaded tray it mapped against, and none when nothing is loaded", () => {
    expect(mapColors(colors, trays([{ id: "0", color: PINK }, { id: "1" }])).trays.map((t) => t.index)).toEqual([0]);
    const empty = mapColors(colors, trays([{ id: "0" }]));
    expect(empty.rows[0]).toMatchObject({ status: "missing", nearest: null });
    expect(renderColorMap(empty)).toContain("no tray is loaded");
  });
});

describe("bambu filament map, the command", () => {
  afterEach(() => {
    process.exitCode = undefined;
    vi.restoreAllMocks();
  });

  it("sees a --json written after `map`, and refuses a bad --colors file before reaching the printer", async () => {
    const dir = mkdtempSync(join(tmpdir(), "filament-map-"));
    const bad = join(dir, "colors.json");
    writeFileSync(bad, JSON.stringify([{ name: "x", color: "pink" }]));
    const errors: string[] = [];
    vi.spyOn(console, "error").mockImplementation((...a: unknown[]) => void errors.push(a.join(" ")));
    const program = buildProgram();
    await program.parseAsync(["filament", "map", "--colors", bad, "--json"], { from: "user" });
    const map = program.commands.find((c) => c.name() === "filament")!.commands.find((c: Command) => c.name() === "map")!;
    // Commander gives a --json after `map` to the parent `filament`; the action reads both.
    expect(map.optsWithGlobals()).toMatchObject({ colors: bad, json: true });
    expect(process.exitCode).toBe(2);
    expect(errors.join("\n")).toMatch(/#RRGGBB/);
  });
});

describe("bambu filament map --trays, a saved tray list in place of the printer", () => {
  // The shape `bambu filament --json` prints: {ams, vt_tray, vir_slot}. Made-up trays.
  const saved = {
    ams: {
      ams: [
        {
          id: "0",
          tray: [
            { id: "0", tray_type: "PLA", tray_color: "F5547CFF", remain: 80 },
            { id: "1", state: 0 },
            { id: "2", tray_type: "PLA", tray_color: "000000FF", remain: -1 },
          ],
        },
      ],
    },
    vir_slot: [{ id: "254", tray_type: "", tray_color: "00000000" }],
  };

  afterEach(() => {
    process.exitCode = undefined;
    vi.restoreAllMocks();
  });

  it("reads the trays through the same frame parser as a live read", () => {
    expect(traysFromFilamentJson(saved).map((x) => [x.index, x.hex, x.remain])).toEqual([
      [0, PINK, 80],
      [2, BLACK, -1],
    ]);
  });

  it("refuses a file that is not `bambu filament --json`, rather than map against no trays", () => {
    expect(() => traysFromFilamentJson([])).toThrow(/JSON object/);
    expect(() => traysFromFilamentJson({ rows: [] })).toThrow(/no ams, vt_tray or vir_slot/);
  });

  it("maps from the file, says where the trays came from, and never reaches the printer", async () => {
    const dir = mkdtempSync(join(tmpdir(), "filament-map-trays-"));
    const colorsFile = join(dir, "by-color.json");
    const traysFile = join(dir, "trays.json");
    writeFileSync(colorsFile, JSON.stringify(byColor([[PINK, "Kite"], [GOLD, null]])));
    writeFileSync(traysFile, JSON.stringify(saved));
    const connect = vi.spyOn(MqttBackend.prototype, "connect").mockRejectedValue(new Error("reached the printer"));
    const configured = vi.spyOn(MqttBackend.prototype, "configured");
    const out: string[] = [];
    vi.spyOn(console, "log").mockImplementation((...a: unknown[]) => void out.push(a.join(" ")));
    await buildProgram().parseAsync(["filament", "map", "--colors", colorsFile, "--trays", traysFile, "--json"], { from: "user" });
    expect(connect).not.toHaveBeenCalled();
    expect(configured).not.toHaveBeenCalled();
    expect(process.exitCode).toBeUndefined();
    const map = JSON.parse(out.join("\n"));
    expect(map.trays_from).toBe(traysFile);
    expect(typeof map.read_at).toBe("string");
    expect(map.rows.map((r: MapRow) => [r.design_hex, r.status, r.tray?.index ?? null])).toEqual([
      [PINK, "matched", 0],
      [GOLD, "missing", null],
    ]);
  });

  it("a bad --trays file fails with exit 2, naming the file", async () => {
    const dir = mkdtempSync(join(tmpdir(), "filament-map-trays-"));
    const colorsFile = join(dir, "by-color.json");
    const traysFile = join(dir, "trays.json");
    writeFileSync(colorsFile, JSON.stringify(byColor([[PINK, "Kite"]])));
    writeFileSync(traysFile, JSON.stringify({ nothing: true }));
    const errors: string[] = [];
    vi.spyOn(console, "error").mockImplementation((...a: unknown[]) => void errors.push(a.join(" ")));
    vi.spyOn(console, "log").mockImplementation(() => undefined);
    await buildProgram().parseAsync(["filament", "map", "--colors", colorsFile, "--trays", traysFile], { from: "user" });
    expect(process.exitCode).toBe(2);
    expect(errors.join("\n")).toContain(`--trays ${traysFile}`);
  });
});
