import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { type TimedRun, logRows, nearestUnused, ratioFor, readTimedRuns, watchedRuns } from "./timed-prints.js";

// The ratio that corrects a plan's sliced minutes (order-driven-lab-design §9.1 step 4): only runs the
// monitor watched from layer 0 to the end count, and only runs with exactly the plate's profile.

const log = (rows: string[]) => ["| When | Event | Layer | Done | Note |", "|---|---|---|---|---|", ...rows].join("\n");

describe("watchedRuns — a run counts only when watched from its start to its end", () => {
  it("times a run from its layer-0 watching row to its finished row", () => {
    const rows = logRows(log(["| 2026-10-04 18:37 | watching | 0/120 | 0% | |", "| 2026-10-04 19:10 | printing | 40/120 | 25% | |", "| 2026-10-04 20:14 | finished | 120/120 | 100% | |"]));
    expect(watchedRuns(rows)).toEqual([{ started: "2026-10-04 18:37", watched: 97 }]);
  });

  it("does not count a watch that began mid-print", () => {
    const rows = logRows(log(["| 2026-10-03 21:00 | watching | 46/120 | 38% | |", "| 2026-10-03 22:00 | finished | 120/120 | 100% | |"]));
    expect(watchedRuns(rows)).toEqual([]);
  });

  it("does not count a run a pause broke, and counts the next clean one", () => {
    const rows = logRows(
      log([
        "| 2026-10-03 10:00 | watching | 0/80 | 0% | |",
        "| 2026-10-03 10:05 | paused | 0/80 | 0% | 0500-8051 |",
        "| 2026-10-03 10:30 | resumed | 0/80 | 0% | |",
        "| 2026-10-03 11:00 | finished | 80/80 | 100% | |",
        "| 2026-10-03 12:00 | watching | 0/80 | 0% | |",
        "| 2026-10-03 12:48 | finished | 80/80 | 100% | |",
      ]),
    );
    expect(watchedRuns(rows)).toEqual([{ started: "2026-10-03 12:00", watched: 48 }]);
  });
});

const BASIC = "Bambu PLA Basic @BBL X2D 0.4 nozzle";
const MATTE = "Bambu PLA Matte @BBL X2D 0.4 nozzle";
const SETTINGS = "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D";
const run = (plate: string, watched: number, sliced: number, filament = BASIC): TimedRun => ({
  plate,
  started: "2026-10-04 00:00",
  watched,
  sliced,
  settings: SETTINGS,
  filament,
});
// The four timed runs as they stood on 2026-10-04 (test/fixtures/orders/prints.json).
const RUNS = [run("phones-01", 62, 22, `${BASIC};${BASIC}`), run("phones-02", 13, 12), run("sheets-04c", 48, 42), run("sheets-04g", 97, 86)];

describe("ratioFor — pooled over the runs with exactly this profile", () => {
  it("pools the one-filament Basic runs to 1.13 and leaves the two-filament print out", () => {
    const r = ratioFor(RUNS, SETTINGS, BASIC)!;
    expect(r).toMatchObject({ value: 1.13, watched: 158, sliced: 140 });
    expect(r.prints).toHaveLength(3);
    expect(ratioFor(RUNS, SETTINGS, `${BASIC};${BASIC}`)!.value).toBe(2.82);
  });

  it("gives none for a filament no timed print used", () => {
    expect(ratioFor(RUNS, SETTINGS, MATTE)).toBeNull();
  });
});

describe("nearestUnused — the ratio a floor plate did not use, and why", () => {
  it("names the filament resting on the most prints", () => {
    const n = nearestUnused(RUNS, SETTINGS, MATTE)!;
    expect(n).toMatchObject({ filament: BASIC, value: 1.13 });
    expect(n.prints).toHaveLength(3);
    expect(n.why).toBe(`printed with ${BASIC}, not ${MATTE}: another filament prints at its own speeds`);
  });

  it("gives none when no print shares the settings", () => {
    expect(nearestUnused(RUNS, "another printer", MATTE)).toBeNull();
  });
});

describe("readTimedRuns — the plates folder as the monitor and the pages leave it", () => {
  it("joins each log's runs with its page's minutes and its recipe's profile, and says why a log is skipped", () => {
    const dir = mkdtempSync(join(tmpdir(), "timed-prints-"));
    mkdirSync(join(dir, "print-logs"));
    writeFileSync(join(dir, "print-logs", "good.md"), log(["| 2026-10-04 00:32 | watching | 0/90 | 0% | |", "| 2026-10-04 01:20 | finished | 90/90 | 100% | |"]));
    writeFileSync(join(dir, "good.md"), "---\nminutes: 42\n---\n# good\n");
    writeFileSync(join(dir, "good.yaml"), `bed: x2d\nprofile:\n  settings: "${SETTINGS}"\n  filament: "${BASIC}"\nitems: []\n`);
    writeFileSync(join(dir, "print-logs", "late.md"), log(["| 2026-10-04 00:32 | watching | 40/90 | 44% | |", "| 2026-10-04 01:20 | finished | 90/90 | 100% | |"]));
    writeFileSync(join(dir, "print-logs", "bare.md"), log(["| 2026-10-04 00:32 | watching | 0/90 | 0% | |", "| 2026-10-04 01:20 | finished | 90/90 | 100% | |"]));
    expect(readTimedRuns(dir)).toEqual({
      runs: [{ plate: "good", started: "2026-10-04 00:32", watched: 48, sliced: 42, settings: SETTINGS, filament: BASIC }],
      skipped: ["bare: its page has no minutes", "late: no run watched from layer 0 to finished"],
    });
  });
});
