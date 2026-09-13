// Interactive confirmation for owner-gated, outward-facing actions (dispatch, stop).
//
// A dispatch reaches the physical printer, so it is never silent: the caller must pass --yes, or
// answer a prompt at an interactive TTY. With neither (a script/pipe and no --yes) we REFUSE rather
// than default to sending — fail-closed on the one action that moves real hardware.

import { createInterface } from "node:readline";

/** True only if the user explicitly confirms. Non-interactive + no --yes ⇒ false (fail-closed). */
export async function confirm(question: string, presetYes: boolean): Promise<boolean> {
  if (presetYes) return true;
  if (!process.stdin.isTTY) return false;
  const rl = createInterface({ input: process.stdin, output: process.stderr });
  try {
    const answer = await new Promise<string>((resolve) => rl.question(`${question} [y/N] `, resolve));
    return /^y(es)?$/i.test(answer.trim());
  } finally {
    rl.close();
  }
}
