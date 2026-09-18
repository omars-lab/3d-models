#!/usr/bin/env bash
# slice-copies.sh — slice N copies of ONE model onto a single X2D plate, packed by libnest2d.
#
# WHY THIS EXISTS (provenance, 2026-09-18):
#   A common ask — "print as many of this MakerWorld model as fit on one sheet" (find-model → here) —
#   needs N instances of a single-object model on one plate. There is NO `bambu slice --copies N` flag,
#   and `--arrange` alone does not *multiply* an object (it only packs the objects already present).
#   But the 23-rung machine-card example (print-model best-practices.md "Our examples") already showed
#   the mechanism: pass one model as the `slice plate <model>` positional, more model files after `--`,
#   and `--arrange` — the verb forwards the trailing files to BambuStudio and libnest2d packs them.
#   For N copies that is simply the SAME file repeated N times. This script is the runnable form.
#   (rubric.md §Arrangement step 4 "hand grid estimate / verify-flags" fallback; §Self-healing Reusable scripts.)
#
# THIS IS A FALLBACK. The proper home is a `bambu slice plate <model> --copies N` flag (owned by the
#   bambu CLI). When that flag lands, delete this script and call the flag.
#
# NOT the .3mf regex-repack path. An earlier approach hand-edited the .3mf <build> to replicate the
#   build item; it works but is a second, fragile code path (it segfaults BambuStudio if the
#   Metadata/*.config members are dropped, and must preserve the <build p:UUID=…> tag). --arrange over
#   repeated positionals reuses the capability the slicer already owns — one code path, no surgery.
#   (repo tenet: "a migration never buys a fork"; CLAUDE.md "Robustness over ease".)
#
# GOTCHA — a decorative/organic model may raise a by-design "floating regions" warning per copy. That is
#   the supportless-overhang advisory (e.g. the twisted dragon egg prints supportless by design). The
#   calibration-grade `bambu print send` gate is fail-closed and will BLOCK on it. For a fun print, send
#   it from the Bambu Studio GUI (`bambu slice open <plate>` → Print), which shows the note but does not
#   block; only whitelist it in .claude/gates/expected-slicer-warnings.json if it is genuinely by-design
#   AND you want the gated CLI path. Do NOT "fix" it with supports on a model built to print without them.
#
# Usage:
#   .claude/skills/print-model/scripts/slice-copies.sh <model.stl|.3mf> <N> [extra bambu-slice args…]
# Env overrides (defaults are the known-good X2D trio, memory: bambu-x2d-bringup):
#   MACHINE, PROCESS, FILAMENT, TIMEOUT, OUT (output filename), OUTDIR (output directory)
# Examples:
#   slice-copies.sh ~/Downloads/egg.stl 20
#   OUT=eggs.3mf OUTDIR=/tmp slice-copies.sh ~/Downloads/egg.stl 20
set -euo pipefail

export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"   # repo rule: system Node is too old

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
BAMBU="$REPO_ROOT/tools/bambu/bin/bambu"

MODEL="${1:?usage: slice-copies.sh <model> <N> [extra bambu-slice args…]}"
N="${2:?usage: slice-copies.sh <model> <N> [extra bambu-slice args…]}"
shift 2

if [[ ! -f "$MODEL" ]]; then
  echo "model not found: $MODEL" >&2
  exit 1
fi
if ! [[ "$N" =~ ^[1-9][0-9]*$ ]]; then
  echo "N must be a positive integer, got: $N" >&2
  exit 1
fi

MACHINE="${MACHINE:-Bambu Lab X2D 0.4 nozzle}"
PROCESS="${PROCESS:-0.20mm Standard @BBL X2D}"
FILAMENT="${FILAMENT:-Bambu PLA Basic @BBL X2D 0.4 nozzle}"
TIMEOUT="${TIMEOUT:-600}"
# The CLI resolves -o relative to the input model's directory, so pass -o as a BASENAME and steer the
# location with -d (OUTDIR). An absolute -o gets concatenated onto the input dir (a real footgun).
base="$(basename "${MODEL%.*}")"
OUT="${OUT:-${base}-${N}x.sliced.3mf}"
OUTDIR="${OUTDIR:-$(cd "$(dirname "$MODEL")" && pwd)}"

# N total instances = 1 positional + (N-1) trailing model files after `--`; --arrange (libnest2d) packs.
repeats=()
for ((i = 1; i < N; i++)); do repeats+=("$MODEL"); done

echo "packing $N copies of $(basename "$MODEL") → $OUTDIR/$OUT"
# `bambu slice` exits non-zero when it captures UNEXPECTED slicer warnings (a by-design floating-regions
# advisory on a decorative model), even though the plate IS written. Distinguish that from a real slice
# failure by whether the output plate exists: warnings-but-sliced is a note for a fun print, not an abort.
set +e
"$BAMBU" slice plate "$MODEL" \
  --arrange \
  -s "$MACHINE;$PROCESS" \
  -f "$FILAMENT" \
  -o "$OUT" \
  -d "$OUTDIR" \
  -t "$TIMEOUT" \
  "$@" \
  ${repeats[@]:+-- "${repeats[@]}"}
slice_rc=$?
set -e
if [[ ! -f "$OUTDIR/$OUT" ]]; then
  echo "slice failed (exit $slice_rc) — no plate written." >&2
  exit "$slice_rc"
fi
if [[ "$slice_rc" -ne 0 ]]; then
  echo "note: the slicer raised warnings (exit $slice_rc) — review them above." >&2
  echo "      a decorative model's 'floating regions' is usually by-design (supportless overhang);" >&2
  echo "      the CLI 'print send' gate will BLOCK on it — send via 'bambu slice open $OUT' → Print instead." >&2
fi

# Verify the REALIZED plate, not just the settings (D-014: a verifier as the front door). Prove N copies
# actually landed on the X2D at 0.4 mm. Not --bare-plate: a fun print may legitimately carry a skirt.
# `validate sliced` bakes in the same warnings check the slice ran, with no flag to tolerate a by-design
# advisory — so on a decorative model it FAILs on the very floating-regions we already explained. Rule:
# a CLEAN slice makes validate authoritative (propagate its exit); a WARNINGS slice runs validate only
# for the displayed facts (objects/printer/nozzle/realized brim-support-raft) — read them; do not abort.
echo "verifying the sliced plate …"
set +e
"$BAMBU" validate sliced "$OUTDIR/$OUT" --expect-objects "$N" --machine X2D --nozzle 0.4
val_rc=$?
set -e
if [[ "$slice_rc" -eq 0 && "$val_rc" -ne 0 ]]; then
  echo "verify FAILED on a clean slice — a real problem, not a by-design warning." >&2
  exit "$val_rc"
fi
