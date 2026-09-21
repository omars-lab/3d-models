import { describe, expect, it } from "vitest";
import { buildActuals, actualsToRecord, actualsAreEmpty } from "./actuals.js";
import type { PrinterStatus } from "./backends/mqtt.js";

// A pushall frame mid-print, carrying the state/progress/layer/temperature keys `status show` reads
// live off the X2D (commands/status.ts) — the PASS-case shape. NO filament-consumed key: that is the
// X2D-unconfirmed field the raw frame is persisted for.
const RUNNING_FRAME: PrinterStatus = {
  gcode_state: "RUNNING",
  mc_percent: 42,
  layer_num: 51,
  total_layer_num: 120,
  mc_remaining_time: 33,
  subtask_name: "eggs-2x3",
  print_error: 0,
  nozzle_temper: 219.8,
  bed_temper: 60.1,
  chamber_temper: 28,
  _cached_at: "2026-09-21T10:15:00.000Z",
  _age_seconds: 1,
};

describe("buildActuals — PASS case (a running X2D print)", () => {
  const a = buildActuals(RUNNING_FRAME, new Date("2026-09-21T10:15:02Z"));

  it("fills state / progress / job from the frame", () => {
    expect(a.state).toMatchObject({ value: "RUNNING", state: "filled" });
    expect(a.progress_pct).toMatchObject({ value: "42", state: "filled" });
    expect(a.job).toMatchObject({ value: "eggs-2x3", state: "filled" });
  });

  it("joins layer_num / total_layer_num into one 'N / M' field", () => {
    expect(a.layer).toMatchObject({ value: "51 / 120", state: "filled" });
  });

  it("fills the three temperatures and the remaining-time prediction", () => {
    expect(a.nozzle_c.value).toBe("219.8");
    expect(a.bed_c.value).toBe("60.1");
    expect(a.chamber_c.value).toBe("28");
    expect(a.remaining_min).toMatchObject({ value: "33", state: "filled" });
  });

  it("prefers the frame's _cached_at for captured_at over the clock", () => {
    expect(a.captured_at).toMatchObject({ value: "2026-09-21T10:15:00.000Z", state: "filled" });
  });

  it("marks filament grams unconfirmed — never fabricated — when the frame carries no such key", () => {
    expect(a.filament_g.value).toBeNull();
    expect(a.filament_g.state).toBe("unconfirmed");
  });

  it("is not empty when print-state keys are present", () => {
    expect(actualsAreEmpty(a)).toBe(false);
  });
});

describe("buildActuals — FAIL-guard case (an empty / idle frame answers nothing)", () => {
  const a = buildActuals({ _age_seconds: 5 }, new Date("2026-09-21T10:15:02Z"));

  it("marks every unread field 'absent', never fabricating a value", () => {
    expect(a.state).toMatchObject({ value: null, state: "absent" });
    expect(a.progress_pct.value).toBeNull();
    expect(a.layer.value).toBeNull();
    expect(a.job.value).toBeNull();
  });

  it("falls back to the injected clock for captured_at when _cached_at is missing", () => {
    expect(a.captured_at).toMatchObject({ value: "2026-09-21T10:15:02.000Z", state: "filled" });
  });

  it("reports the capture as empty (nothing worth a record was read)", () => {
    expect(actualsAreEmpty(a)).toBe(true);
  });
});

describe("actualsToRecord — only genuinely-filled fields carry a value", () => {
  it("projects the filled fields and omits the unconfirmed/absent ones", () => {
    const rec = actualsToRecord(buildActuals(RUNNING_FRAME));
    expect(rec.state).toBe("RUNNING");
    expect(rec.layer).toBe("51 / 120");
    expect(rec.chamber_c).toBe("28");
    // unconfirmed → omitted from the record block (recoverable only from the raw frame)
    expect(rec.filament_g).toBeUndefined();
  });

  it("omits everything for an idle frame — an actuals block with no fabricated numbers", () => {
    const rec = actualsToRecord(buildActuals({}));
    expect(Object.values(rec).every((v) => v === undefined)).toBe(true);
  });
});
