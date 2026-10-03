// Tests for counting the beds of a sliced plate and naming what spilled past the allowed number.
//
// The fixture is real: test/fixtures/minis-05/spilled.slice_info.config is the slice summary of
// docs/design/plates/minis-05.yaml as `bambu slice compose` sliced it on 2026-09-30 (Bambu Studio
// 02.08.02.61). Its 12 objects arranged as 11 on bed 1 and 1 on bed 2, and nothing said so.

import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { parseBeds } from "./threemf.js";
import { spilledItems } from "./commands/compose.js";

const spilled = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "..", "test", "fixtures", "minis-05", "spilled.slice_info.config"),
  "utf8",
);

const oneBed = `<config>
  <plate>
    <metadata key="index" value="1"/>
    <metadata key="prediction" value="600"/>
    <object identify_id="1" name="it-aaaaaaaaaaaa.stl" skipped="false" />
    <object identify_id="2" name="it-bbbbbbbbbbbb.stl" skipped="false" />
  </plate>
</config>`;

describe("parseBeds", () => {
  it("finds both beds of the real minis-05 spill, 11 + 1", () => {
    const beds = parseBeds(spilled);
    expect(beds.map((b) => b.index)).toEqual([1, 2]);
    expect(beds.map((b) => b.objects.length)).toEqual([11, 1]);
    expect(beds[1]?.objects).toEqual(["it-5259a22ce77e.stl"]);
    expect(beds.map((b) => b.predictionS)).toEqual([15665, 3349]);
  });

  it("reads a plate that fits as one bed", () => {
    const beds = parseBeds(oneBed);
    expect(beds).toHaveLength(1);
    expect(beds[0]?.objects).toHaveLength(2);
  });

  it("returns no beds for an unsliced summary", () => {
    expect(parseBeds("<config/>")).toEqual([]);
  });
});

describe("spilledItems — what would not print", () => {
  const entries = new Map([["it-5259a22ce77e.stl", ["c3 CS-1-minimal-coaster.bkr"]]]);

  it("names the object on bed 2 by its plate entry when one bed is allowed", () => {
    expect(spilledItems(parseBeds(spilled), entries, 1)).toEqual(["c3 CS-1-minimal-coaster.bkr (bed 2)"]);
  });

  it("is empty when the manifest allows the second bed", () => {
    expect(spilledItems(parseBeds(spilled), entries, 2)).toEqual([]);
  });

  it("is empty for a plate that fits", () => {
    expect(spilledItems(parseBeds(oneBed), entries, 1)).toEqual([]);
  });

  it("falls back to the object name when no entry matches", () => {
    expect(spilledItems(parseBeds(spilled), new Map(), 1)).toEqual(["it-5259a22ce77e.stl (bed 2)"]);
  });
});
