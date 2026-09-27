// `bambu print verdict` — set one printed piece's verdict (and add notes) in a shipped print record.
//
// The record is hand-kept YAML front matter with comments and a fixed key order, so this edits the
// lines in place rather than re-dumping the YAML: the diff a verdict makes is the verdict line and
// the notes it adds, nothing else. The result is then parsed back and checked, so a line edit that
// landed in the wrong place fails here instead of in the prints gate.
//
// It is the one writer the hub page calls, and it works from the terminal too.

import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { parse } from "yaml";

/** R15 in .claude/gates/prints_gate.py: keep (print it again as is), adjust, drop. */
export const PIECE_VERDICTS = ["keep", "adjust", "drop"] as const;
export type PieceVerdict = (typeof PIECE_VERDICTS)[number];

export interface VerdictChange {
  run: string;
  entry: string;
  from: string | null;
  to: PieceVerdict;
  notesAdded: string[];
  changed: boolean;
}

export class VerdictError extends Error {}

/** `docs/prints/<run>/index.md` under the repo root. */
export function recordPath(root: string, run: string): string {
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(run)) throw new VerdictError(`not a run name: ${JSON.stringify(run)}`);
  return join(root, "docs", "prints", run, "index.md");
}

const ENTRY_LINE = /^  - entry: "?([^"\n]+?)"?\s*$/;

/** Apply one verdict to the record text; pure, so the tests need no files. */
export function applyVerdict(
  text: string,
  entry: string,
  verdict: string,
  notes: readonly string[] = [],
): { text: string; from: string | null; notesAdded: string[] } {
  if (!(PIECE_VERDICTS as readonly string[]).includes(verdict)) {
    throw new VerdictError(`verdict must be one of ${PIECE_VERDICTS.join(", ")}, not ${JSON.stringify(verdict)}`);
  }
  for (const n of notes) {
    if (!n.trim() || /[\r\n]/.test(n)) throw new VerdictError("a note is one non-empty line");
  }

  const lines = text.split("\n");
  const fmEnd = lines[0] === "---" ? lines.indexOf("---", 1) : -1;
  if (fmEnd < 0) throw new VerdictError("the record has no front matter");

  const entries: string[] = [];
  let start = -1;
  for (let i = 1; i < fmEnd; i++) {
    const m = ENTRY_LINE.exec(lines[i]!);
    if (!m) continue;
    entries.push(m[1]!);
    if (m[1] === entry) start = i;
  }
  if (start < 0) {
    throw new VerdictError(`no piece ${JSON.stringify(entry)} in this record; it has ${entries.join(", ") || "none"}`);
  }
  // The piece's block runs to the next list item or the next top-level key.
  let end = start + 1;
  while (end < fmEnd && lines[end]!.startsWith("    ")) end++;

  const block = lines.slice(start, end);
  let from: string | null = null;
  const vIdx = block.findIndex((l) => /^    verdict:/.test(l));
  if (vIdx >= 0) {
    from = block[vIdx]!.replace(/^    verdict:\s*/, "").replace(/^"(.*)"$/, "$1").trim() || null;
    block[vIdx] = `    verdict: ${verdict}`;
  }

  const nIdx = block.findIndex((l) => /^    notes:/.test(l));
  const existing = new Set<string>();
  let notesEnd = nIdx + 1;
  if (nIdx >= 0) {
    while (notesEnd < block.length && block[notesEnd]!.startsWith("      - ")) {
      existing.add(parse(block[notesEnd]!.slice("      - ".length)) as string);
      notesEnd++;
    }
  }
  const notesAdded = notes.filter((n, i) => !existing.has(n) && notes.indexOf(n) === i);
  const noteLines = notesAdded.map((n) => `      - ${JSON.stringify(n)}`);

  if (vIdx < 0) {
    // No verdict line yet: it goes just before the notes, as the scaffolder writes it.
    block.splice(nIdx >= 0 ? nIdx : block.length, 0, `    verdict: ${verdict}`);
    if (nIdx >= 0) notesEnd++;
  }
  const nAt = block.findIndex((l) => /^    notes:/.test(l));
  if (nAt >= 0) {
    if (noteLines.length) {
      block[nAt] = "    notes:"; // `notes: []` becomes a block list
      block.splice(notesEnd, 0, ...noteLines);
    }
  } else if (noteLines.length) {
    block.push("    notes:", ...noteLines);
  }

  const out = [...lines.slice(0, start), ...block, ...lines.slice(end)].join("\n");
  check(out, entry, verdict, notesAdded);
  return { text: out, from, notesAdded };
}

/** Parse the edited front matter back and confirm the piece now says what was asked. */
function check(text: string, entry: string, verdict: string, notesAdded: readonly string[]): void {
  const fm = text.split("\n---")[0]!.replace(/^---\n/, "");
  const doc = parse(fm) as { objects?: Array<{ entry?: string; verdict?: string; notes?: unknown }> };
  const obj = doc.objects?.find((o) => String(o.entry) === entry);
  const notes = Array.isArray(obj?.notes) ? (obj!.notes as unknown[]) : [];
  if (!obj || obj.verdict !== verdict || !notesAdded.every((n) => notes.includes(n))) {
    throw new VerdictError(`the edit did not land on piece ${entry}; the record was left unchanged`);
  }
}

/** Read, apply and write back one record. Writes nothing when nothing changes. */
export function setVerdict(
  root: string,
  run: string,
  entry: string,
  verdict: string,
  notes: readonly string[] = [],
): VerdictChange {
  const path = recordPath(root, run);
  if (!existsSync(path)) throw new VerdictError(`no print record ${run} (looked for ${path})`);
  const before = readFileSync(path, "utf8");
  const r = applyVerdict(before, entry, verdict, notes);
  const changed = r.text !== before;
  if (changed) writeFileSync(path, r.text);
  return { run, entry, from: r.from, to: verdict as PieceVerdict, notesAdded: r.notesAdded, changed };
}
