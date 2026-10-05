import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import type { Slot } from "./frame.js";
import { parseFilamentGrams, sentArgs, sentFeeds, writeSentRow, type Feed } from "./sent-row.js";
import { sentTrays } from "./shelf.js";

// Two beds, the shape a real slice writes (sheets-04g's filament line, 2026-10-05), plus a second
// filament and a second bed so the bed and the id both have to be read.
const SLICE = `<config>
  <plate>
    <metadata key="index" value="1"/>
    <filament id="1" tray_info_idx="GFA00" type="PLA" color="#00AE42" used_m="8.96" used_g="27.15" group_id="0"/>
    <filament id="3" type="PLA" color="#000000" used_m="1.00" used_g="3" group_id="0"/>
  </plate>
  <plate>
    <metadata key="index" value="2"/>
    <filament id="1" type="PLA" color="#00AE42" used_m="2.00" used_g="6.1"/>
  </plate>
</config>`;

const slot = (unit: number, tray: number, color: string): Slot => ({
  where: `AMS ${unit} · slot ${tray}`,
  tray: { tray_type: "PLA", tray_color: color },
  index: unit * 4 + tray,
});
const SLOTS = [slot(0, 0, "000000FF"), slot(0, 3, "00AE42FF"), slot(0, 1, "00000000")];

describe("parseFilamentGrams", () => {
  it("reads each filament's grams on the bed asked for", () => {
    expect([...parseFilamentGrams(SLICE, 1)]).toEqual([[1, 27.15], [3, 3]]);
    expect([...parseFilamentGrams(SLICE, 2)]).toEqual([[1, 6.1]]);
  });
  it("is empty for a bed the slice does not have", () => {
    expect(parseFilamentGrams(SLICE, 3).size).toBe(0);
  });
});

describe("sentFeeds", () => {
  it("names each mapped filament's tray, the tray's color and the slice's grams", () => {
    const r = sentFeeds([3, -1, 0], SLOTS, parseFilamentGrams(SLICE));
    expect(r).toEqual({
      ok: true,
      feeds: [
        { hex: "#00AE42", tray: "AMS 0 · slot 3", grams: 27.15 },
        { hex: "#000000", tray: "AMS 0 · slot 0", grams: 3 },
      ],
    });
  });
  it("takes the tray's color, not the slice's: with --color the slice's was never printed", () => {
    const r = sentFeeds([0], SLOTS, new Map([[1, 27.15]]));
    expect(r.ok && r.feeds[0]!.hex).toBe("#000000");
  });
  it("refuses the whole row when one feed cannot be named, saying which", () => {
    const grams = parseFilamentGrams(SLICE);
    expect(sentFeeds([3, -1, 2], SLOTS, grams)).toEqual({ ok: false, reason: "filament 3 went to tray 2, which the status read does not list" });
    expect(sentFeeds([1], SLOTS, new Map([[1, 5]]))).toEqual({ ok: false, reason: "filament 1 went to AMS 0 · slot 1, which reports no color" });
    expect(sentFeeds([3], SLOTS, new Map([[1, 0]]))).toEqual({ ok: false, reason: "the slice has no grams for filament 1 (slice it again)" });
    expect(sentFeeds([-1, -1], SLOTS, grams)).toEqual({ ok: false, reason: "the send mapped no filament to a tray" });
  });
});

describe("the sent row, written and read back", () => {
  const feeds: Feed[] = [
    { hex: "#00AE42", tray: "AMS 0 · slot 3", grams: 27.15 },
    { hex: "#000000", tray: "AMS 0 · slot 0", grams: 3 },
  ];

  it("passes print_monitor.py one --sent per tray", () => {
    expect(sentArgs("sheets-04g", feeds)).toEqual([
      "sheets-04g", "--sent", "#00AE42", "AMS 0 · slot 3", "27.15", "--sent", "#000000", "AMS 0 · slot 0", "3",
    ]);
    let seen: string[] = [];
    const row = writeSentRow("sheets-04g", feeds, (args) => {
      seen = args;
      return "ev=row | 2026-10-05 18:35 | sent |  |  | fed … |\n";
    });
    expect(seen).toEqual(sentArgs("sheets-04g", feeds));
    expect(row).toBe("| 2026-10-05 18:35 | sent |  |  | fed … |");
  });

  it("says why when print_monitor.py refuses", () => {
    const refuse = () => {
      throw Object.assign(new Error("exit 2"), { stderr: "usage: …\nprint_monitor.py: error: no plate page at x.md\n" });
    };
    expect(() => writeSentRow("x", feeds, refuse)).toThrow("print_monitor.py: error: no plate page at x.md");
  });

  it("is the row the shelf reads: print_monitor's own sent_line, parsed by sentTrays", () => {
    const scripts = fileURLToPath(new URL("../../../.claude/skills/monitor-print/scripts", import.meta.url));
    const trays = JSON.stringify(feeds.map((f) => [f.hex, f.tray, f.grams]));
    const line = execFileSync("python3", ["-c",
      `import sys, json; sys.path.insert(0, ${JSON.stringify(scripts)}); import print_monitor as m; print(m.sent_line("2026-10-05 18:35", [tuple(t) for t in json.loads(sys.argv[1])]))`,
      trays], { encoding: "utf8" }).trim();
    const said = line.split("|")[5]!.trim();
    expect(sentTrays(said)).toEqual(feeds.map((f) => ({ ...f, hex: f.hex.toLowerCase() })));
  });
});
