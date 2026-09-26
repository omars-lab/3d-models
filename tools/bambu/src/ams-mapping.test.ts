import { describe, expect, it } from "vitest";
import { collectSlots, trayIndex } from "./frame.js";
import { parseUsedFilaments } from "./threemf.js";
import {
  feedsFromAms,
  logicalSlotsFromPlate,
  physicalTraysFromSlots,
  planAmsMapping,
  reconcile,
} from "./filament-sync.js";
import type { PrinterStatus } from "./backends/mqtt.js";

// `bambu print send` used to publish use_ams:false / ams_mapping:[0] on every send, which feeds the
// external spool — empty on our X2D, so a CLI send would have printed nothing (found by the minis-01
// run, 2026-09-25). A send now maps each used filament to the loaded tray it matches, or refuses.

// The X2D frame shape seen 2026-09-17: `ams.ams[].tray[]`, and the external spool as a `vir_slot`
// ARRAY carrying the id "254".
const frame = (trays: Array<{ id: string; type: string; color: string }>, ext?: { type: string; color: string }) =>
  ({
    ams: { ams: [{ id: "0", tray: trays.map((t) => ({ id: t.id, tray_type: t.type, tray_color: t.color, remain: 80 })) }] },
    vir_slot: [{ id: "254", tray_type: ext?.type ?? "", tray_color: ext?.color ?? "00000000" }],
  }) as unknown as PrinterStatus;

describe("trayIndex", () => {
  it("numbers an AMS tray unit*4 + tray, and the external spool by its own id", () => {
    expect(trayIndex("0", "0")).toBe(0);
    expect(trayIndex("0", "3")).toBe(3);
    expect(trayIndex("1", "2")).toBe(6);
    expect(trayIndex(null, "254")).toBe(254);
    expect(trayIndex(null, "255")).toBe(255);
  });

  it("gives null for anything it cannot number for sure — an AMS HT unit, a bad id, an odd spool id", () => {
    expect(trayIndex("128", "0")).toBeNull();
    expect(trayIndex("0", "4")).toBeNull();
    expect(trayIndex("0", "")).toBeNull();
    expect(trayIndex("x", "0")).toBeNull();
    expect(trayIndex(null, "0")).toBeNull();
  });

  it("is carried on every slot collectSlots reads", () => {
    const slots = collectSlots(frame([{ id: "2", type: "PLA", color: "FFFFFFFF" }]));
    expect(slots.map((s) => s.index)).toEqual([2, 254]);
  });
});

describe("parseUsedFilaments", () => {
  // Trimmed from build/plates/minis-01.plate.3mf (BambuStudio 02.08.02.61).
  const xml = `<config><plate>
    <metadata key="index" value="1"/>
    <object identify_id="105" name="it-a8a9f6bf7606.stl" skipped="false" />
    <filament id="3" type="PLA" color="#FFFFFF" used_m="1.0"/>
    <filament id="1" type="PLA" color="#00AE42" used_m="6.70"/>
  </plate><plate>
    <metadata key="index" value="2"/>
    <filament id="2" type="PETG" color="#000000" used_m="2.0"/>
  </plate></config>`;

  it("lists the used filament ids of the asked plate, sorted", () => {
    expect(parseUsedFilaments(xml)).toEqual([1, 3]);
    expect(parseUsedFilaments(xml, 2)).toEqual([2]);
  });

  it("is empty for a plate the file does not have", () => {
    expect(parseUsedFilaments(xml, 5)).toEqual([]);
  });
});

describe("planAmsMapping", () => {
  const plan = (colours: string[], used: number[], f: PrinterStatus) => {
    const logical = logicalSlotsFromPlate(colours, colours.map(() => "PLA")).filter((l) => used.includes(l.slot));
    return planAmsMapping(reconcile(logical, physicalTraysFromSlots(collectSlots(f))), colours.length, used);
  };

  it("maps a single-colour plate to the AMS tray that holds its colour, and feeds from the AMS", () => {
    const p = plan(["#FFFFFF"], [1], frame([{ id: "0", type: "PLA", color: "000000FF" }, { id: "2", type: "PLA", color: "FFFFFFFF" }]));
    expect(p).toEqual({ ok: true, amsMapping: [2], useAms: true });
  });

  it("puts -1 for a filament the plate declares but does not print with", () => {
    const p = plan(["#00AE42", "#FFFFFF"], [2], frame([{ id: "1", type: "PLA", color: "FFFFFFFF" }]));
    expect(p).toEqual({ ok: true, amsMapping: [-1, 1], useAms: true });
  });

  it("feeds from the external spool only when that is the matching tray", () => {
    const p = plan(["#FF0000"], [1], frame([], { type: "PLA", color: "FF0000FF" }));
    expect(p).toEqual({ ok: true, amsMapping: [254], useAms: false });
  });

  // The hard case, and the one our plates hit: slices carry Studio's default green, which is not
  // what is loaded. A send must refuse, not pick a spool — the operator names it with --ams-mapping.
  it("refuses when a used filament matches no loaded tray", () => {
    const p = plan(["#00AE42"], [1], frame([{ id: "0", type: "PLA", color: "FFFFFFFF" }]));
    expect(p.ok).toBe(false);
    if (!p.ok) expect(p.reason).toMatch(/filament 1 is missing/);
  });

  it("refuses a near-tie rather than choose between two trays", () => {
    const p = plan(["#FFFFFF"], [1], frame([{ id: "0", type: "PLA", color: "FFFFFFFF" }, { id: "1", type: "PLA", color: "FAFAFAFF" }]));
    expect(p.ok).toBe(false);
    if (!p.ok) expect(p.reason).toMatch(/ambiguous/);
  });

  it("refuses when the matching tray has no known number", () => {
    const f = { ams: { ams: [{ id: "128", tray: [{ id: "0", tray_type: "PLA", tray_color: "FFFFFFFF" }] }] } } as unknown as PrinterStatus;
    const p = plan(["#FFFFFF"], [1], f);
    expect(p.ok).toBe(false);
    if (!p.ok) expect(p.reason).toMatch(/no known tray number/);
  });

  it("refuses a plate that lists no used filament", () => {
    expect(plan(["#FFFFFF"], [], frame([])).ok).toBe(false);
  });
});

describe("feedsFromAms", () => {
  it("is true for an AMS tray and false for the external spool or unused entries", () => {
    expect(feedsFromAms([0])).toBe(true);
    expect(feedsFromAms([-1, 5])).toBe(true);
    expect(feedsFromAms([254])).toBe(false);
    expect(feedsFromAms([-1])).toBe(false);
  });
});
