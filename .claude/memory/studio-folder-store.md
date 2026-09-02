---
name: studio-folder-store
description: bikar studio folder semantics — root is an absent folder key never '', the dev overlay patterns/.folders.json is three-state, folders are labels not objects
metadata:
  type: project
---

- **Root is an ABSENT `folder` key, never `''`**: `'' ?? null` is `''`, so an empty string lands in the column as a folder named `""` that no header renders while the tree draws the file at root — row and display disagree silently. `setPatternFolder` in `packages/web/src/pattern-api.ts` folds `''` into root, and lives there rather than `main.ts` because `main.ts` needs a DOM and cannot be imported by vitest.
- Dev's folder store `patterns/.folders.json` is a **three-state overlay**: entry absent = ask the disk, `name → "Orbs"` = filed there, `name → null` = deliberately at root. Omitting a root pattern hands the question back to the disk, so the move undoes itself on reload. The reader throws on an unparseable file rather than returning `{}`. On main the file is `{}`: the filing is the directory, the overlay is dev-only.
- A folder is a label, not an object: dragging the last file out dissolves it; `knownFolders` keeps it droppable for the session.
- Folder-move UI: drag onto a folder header to file, onto the root zone under the tree to unfile (bikar #49 `c9cf3fb`).

**Why:** two representations of "root" and two of "unset" produced a reload that reverted user moves with nothing to say why.

**How to apply:** any new per-pattern attribute follows the same null-vs-absent discipline end to end ([[bikar-secrets-and-supabase]] for the server half).
