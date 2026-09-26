#!/usr/bin/env -S npx tsx
// `bambu` — contextualized CLI companion to the setup-bambu-x2d skill. The command tree is in
// ./program.ts; this file only runs it.

import { buildProgram } from "./program.js";

buildProgram()
  .parseAsync(process.argv)
  .catch((err) => {
    console.error(err instanceof Error ? err.message : String(err));
    process.exit(1);
  });
