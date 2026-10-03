import { describe, expect, it } from "vitest";
import { cardRefusal, cardSummary, fmtKb, readStorage, renderStorage, rmRefusal } from "./storage.js";

// The storage fields as the X2D sent them on 2026-10-03, with no card in: the frame the sheets-04b
// send read just before its upload failed with 553.
const NO_CARD = {
  gcode_state: "FINISH",
  sdcard: false,
  ipcam: { tl_external_free_kb: 0, tl_external_total_kb: 0, tl_internal_free_kb: 884486, tl_internal_total_kb: 962560 },
  device: { cam: { tl_external_free_kb: 0, tl_external_total_kb: 0, tl_internal_free_kb: 884486, tl_internal_total_kb: 962560 } },
};

const card = (freeKb: number, totalKb = 31_000_000) => ({
  gcode_state: "IDLE",
  sdcard: true,
  ipcam: { tl_external_free_kb: freeKb, tl_external_total_kb: totalKb },
});

describe("readStorage", () => {
  it("reads the card and both spaces off the X2D's frame", () => {
    expect(readStorage(NO_CARD)).toEqual({
      card: false, cardFreeKb: 0, cardTotalKb: 0, internalFreeKb: 884486, internalTotalKb: 962560,
    });
  });
  it("falls back to device.cam, and says not reported when the frame is silent", () => {
    expect(readStorage({ device: { cam: { tl_internal_free_kb: "10" } } }).internalFreeKb).toBe(10);
    expect(readStorage({})).toEqual({ card: null, cardFreeKb: null, cardTotalKb: null, internalFreeKb: null, internalTotalKb: null });
  });
});

describe("cardRefusal", () => {
  it("refuses the sheets-04b frame: no card in", () => {
    expect(cardRefusal(NO_CARD, 900)).toContain("no storage card");
  });
  it("refuses a card with less room than the plate", () => {
    expect(cardRefusal(card(500), 900)).toBe("the storage card has 500 KB free and the plate is 900 KB");
  });
  it("lets a card with room through", () => {
    expect(cardRefusal(card(20_000_000), 900)).toBeNull();
  });
  it("does not refuse a frame that never mentions the card; the upload's own error still stops it", () => {
    expect(cardRefusal({ gcode_state: "IDLE" }, 900)).toBeNull();
  });
  it("does not read a card that reports no total as full", () => {
    expect(cardRefusal(card(0, 0), 900)).toBeNull();
  });
});

describe("rendering", () => {
  it("says no card, and that the built-in storage is out of the upload's reach", () => {
    const out = renderStorage(readStorage(NO_CARD));
    expect(out).toContain("storage card:     none in the printer");
    expect(out).toContain("864 MB free of 940 MB (the upload cannot reach it)");
  });
  it("sizes in KB, MB and GB", () => {
    expect(fmtKb(512)).toBe("512 KB");
    expect(fmtKb(2048)).toBe("2 MB");
    expect(fmtKb(31_000_000)).toBe("29.6 GB");
    expect(cardSummary(readStorage(card(20_000_000)))).toBe("in, 19.1 GB free of 29.6 GB");
  });
});

describe("rmRefusal", () => {
  const idle = { gcode_state: "FINISH", subtask_name: "sheets-04b.plate" };
  it("allows a plate at the card's top", () => {
    expect(rmRefusal("sheets-04b.plate.3mf", idle)).toBeNull();
    expect(rmRefusal("MINIS-01.3MF", null)).toBeNull();
  });
  it("refuses anything in a folder: those are the printer's", () => {
    expect(rmRefusal("timelapse/video.mp4", idle)).toContain("in a folder");
    expect(rmRefusal("cache/old.3mf", idle)).toContain("in a folder");
    expect(rmRefusal("/sheets-04b.plate.3mf", idle)).toContain("in a folder");
    expect(rmRefusal("..\\x.3mf", idle)).toContain("in a folder");
  });
  it("refuses a file that is not a plate", () => {
    expect(rmRefusal("timelapse", idle)).toContain("not a plate file");
    expect(rmRefusal("notes.gcode", idle)).toContain("not a plate file");
  });
  it("refuses the file the printer is printing from, and only while it prints", () => {
    const running = { gcode_state: "RUNNING", subtask_name: "sheets-04b.plate" };
    expect(rmRefusal("sheets-04b.plate.3mf", running)).toBe("the printer is printing from sheets-04b.plate.3mf (RUNNING)");
    expect(rmRefusal("minis-01.plate.3mf", running)).toBeNull();
  });
});
