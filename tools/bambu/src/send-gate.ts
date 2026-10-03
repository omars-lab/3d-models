// The two checks `print send` makes before anything reaches the printer, kept apart so they can be
// tested without a printer:
//
//   - Approval (D-093). Omar's yes to a send is the Approve box on the plate's page in docs/plates/,
//     ticked by him in Obsidian, or ticked for him when he says yes in chat (the session then writes
//     the tick, the date and his words onto the page). A plate with no page has no box to tick, so it
//     cannot be approved and does not go out.
//
//     One approval is good for one send. The page's `## Timeline` table is the log: every `approved`,
//     `sent` and `printed` row is dated, so an approval counts only when it comes after the last time
//     the plate went out. A plate whose last print showed the setup was wrong cannot be sent again on
//     the yes that sent it the first time. A successful send spends the approval: `spendApproval`
//     unticks the box, sets the stage to `sent` and adds a dated `sent` row, so the table holds every
//     approved reprint against the plate.
//
//     A ticked box with no `approved` row yet counts only on a page that has never gone out. After a
//     send, a tick has to be read back into a dated `approved` row first: a box ticked before a send
//     made outside this CLI (Bambu Studio does not untick it) looks exactly like a fresh one.
//   - Idle. A send while another print runs would queue over it or fail on the printer; the state
//     comes off the same status read the filament match already makes. A state we cannot read is a
//     refusal, not a pass.

import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";
import { parse } from "yaml";
import type { PrinterStatus } from "./backends/mqtt.js";

/** `build/plates/sheets-04b.plate.3mf` → `sheets-04b`: the name its page in docs/plates/ carries. */
export function plateNameOf(plateFile: string): string {
  return basename(plateFile).replace(/\.3mf$/i, "").replace(/\.plate$/i, "");
}

export function platePagePath(name: string, root: string): string {
  return join(root, "docs", "plates", `${name}.md`);
}

export interface Approval {
  page: string; // where the page is, or would be
  exists: boolean;
  approved: boolean;
  how: string; // what said yes, or why not
  sends: number; // how many times the timeline says it went out
}

// The same readings as the plates gate (`.claude/gates/plates_gate.py`: TICKED_APPROVE, ROW, timeline).
const TICKED_APPROVE = /^\s*-\s*\[[xX]\]\s*\*{0,2}Approve/m;
const TICKED_APPROVE_ALL = /^(\s*-\s*)\[[xX]\](\s*\*{0,2}Approve)/gm;
const ROW = /^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([a-z]+)\b/;
const TIMELINE = /^## Timeline\b.*$([\s\S]*?)(?=^## |(?![\s\S]))/m;
const FRONTMATTER = /^---\n([\s\S]*?)\n---/;

interface Row {
  date: string;
  event: string;
}

function timeline(body: string): Row[] {
  const section = TIMELINE.exec(body)?.[1];
  if (section === undefined) return [];
  const rows: Row[] = [];
  for (const line of section.split("\n")) {
    const r = ROW.exec(line.trim());
    if (r?.[1] && r[2]) rows.push({ date: r[1], event: r[2] });
  }
  return rows;
}

/** The last row naming one of these events, and where it sits (-1 and undefined when none does). */
function lastOf(rows: Row[], events: string[]): { at: number; row: Row | undefined } {
  const at = rows.findLastIndex((r) => events.includes(r.event));
  return { at, row: rows[at] };
}

/** Is this plate approved for its next send? An approval after the last send, or a first-time tick. */
export function plateApproval(name: string, root: string): Approval {
  const page = platePagePath(name, root);
  if (!existsSync(page)) {
    return { page, exists: false, approved: false, how: "no plate page, so nothing to approve", sends: 0 };
  }
  const text = readFileSync(page, "utf8");
  const fm = FRONTMATTER.exec(text);
  let data: Record<string, unknown> = {};
  try {
    data = (fm?.[1] ? parse(fm[1]) : {}) ?? {};
  } catch {
    return { page, exists: true, approved: false, how: "the page's frontmatter does not parse", sends: 0 };
  }
  const body = fm ? text.slice(fm[0].length) : text;
  const rows = timeline(body);
  const sends = rows.filter((r) => r.event === "sent").length;
  const out = lastOf(rows, ["sent", "printed"]);
  const yes = lastOf(rows, ["approved"]);
  const ticked = TICKED_APPROVE.test(body);
  const nth = sends === 0 ? "its first send" : `send ${sends + 1}`;

  if (yes.row && yes.at > out.at) {
    return { page, exists: true, approved: true, how: `approved on ${yes.row.date}, for ${nth}`, sends };
  }
  if (!out.row && (ticked || data.approved === true)) {
    const how = ticked ? "the Approve box is ticked" : `approved on ${String(data.approved_on ?? "(no date)")}`;
    return { page, exists: true, approved: true, how: `${how}, for ${nth}`, sends };
  }
  if (out.row && yes.row) {
    const tail = ticked ? "; the box is ticked, but a tick after a send needs a dated approved row first" : "";
    return {
      page, exists: true, approved: false, sends,
      how: `the approval of ${yes.row.date} was spent when it was ${out.row.event} on ${out.row.date}${tail}`,
    };
  }
  if (out.row) {
    return { page, exists: true, approved: false, how: `it went out on ${out.row.date} and has no approval since`, sends };
  }
  return { page, exists: true, approved: false, how: "the Approve box is not ticked", sends };
}

/**
 * Spend the approval on a successful send: untick every Approve box, set the stage to `sent`, and add a
 * dated `sent` row to the timeline. Returns the row it wrote. The page is rewritten in place; the
 * caller ships it like any doc change.
 */
export function spendApproval(page: string, date: string, approval: Approval): string {
  const text = readFileSync(page, "utf8");
  const fm = FRONTMATTER.exec(text);
  if (!fm) throw new Error(`${page} has no frontmatter`);
  const head = fm[0].replace(/^stage:.*$/m, "stage: sent");
  let body = text.slice(fm[0].length).replace(TICKED_APPROVE_ALL, "$1[ ]$2");
  const row = `| ${date} | sent — by \`bambu print send\`; spends the approval (${approval.how}) | this page |`;
  const m = TIMELINE.exec(body);
  const section = m?.[1];
  if (!m || section === undefined) {
    body = `${body.replace(/\n*$/, "\n")}\n## Timeline\n\n| Date | What happened | Where it is written |\n|---|---|---|\n${row}\n`;
  } else {
    const lines = section.split("\n");
    let lastRow = -1;
    lines.forEach((l, i) => {
      if (l.trim().startsWith("|")) lastRow = i;
    });
    if (lastRow === -1) lines.splice(lines.length, 0, row);
    else lines.splice(lastRow + 1, 0, row);
    const start = m.index + m[0].length - section.length;
    body = body.slice(0, start) + lines.join("\n") + body.slice(start + section.length);
  }
  writeFileSync(page, head + body);
  return row;
}

// What the X2D reports as gcode_state when nothing is printing. Anything else (RUNNING, PAUSE,
// PREPARE, SLICING, …) means the machine is busy.
const IDLE_STATES = new Set(["IDLE", "FINISH", "FAILED"]);

/** Why the printer cannot take a plate now, or null when it is idle. */
export function printerBusy(frame: PrinterStatus): string | null {
  const raw = frame.gcode_state;
  if (raw === undefined || raw === null || String(raw).trim() === "") {
    return "the printer did not report its state";
  }
  const state = String(raw).trim().toUpperCase();
  if (IDLE_STATES.has(state)) return null;
  const job = frame.subtask_name ? ` (${String(frame.subtask_name)})` : "";
  return `the printer is ${state}${job}`;
}
