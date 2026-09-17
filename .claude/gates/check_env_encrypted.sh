#!/usr/bin/env sh
# check_env_encrypted.sh — no plaintext secret may enter this repo's history.
#
# Ported from bikar `scripts/check-env-encrypted.sh` (bikar PR #198's env loader
# work), where it guards a tracked .env. It transfers because the premise is
# the same here: `.gitignore` deliberately does NOT ignore `.env` — dotenvx
# encrypts every value (`encrypted:BB…`, readable only with `.env.keys`, which
# IS ignored) so the file is commit-safe and a second machine bootstraps from
# one LastPass entry. What that design gives up is the one protection everyone
# relies on: a plaintext `.env` written by `dotenvx decrypt`, an editor
# "save as" or a half-finished rotation is one `git add` away from committing
# every credential in it, and the ignore file cannot tell the two apart. This
# reads shape, not content, and can.
#
# Usage:
#   check_env_encrypted.sh --staged        # what is about to be committed (hook)
#   check_env_encrypted.sh                 # what is tracked right now (make)
#   check_env_encrypted.sh --file <path>   # one file, before it is staged
#   check_env_encrypted.sh --self-test     # the by-design failures must fire
#
# Exit 0 clean / 1 a violation or an unreadable line / 2 misuse. Needs no
# secrets, no network, and not even dotenvx.

set -u

MODE="${1:-tracked}"

# .env.example is exempt: it is the key list a new machine reads before it has
# any keys, and its values are placeholders. gitleaks still scans it.
ENV_PATTERN='(^|/)\.env($|\.)'
EXEMPT='(^|/)\.env\.example$'

scan() {
  mode="$1"; files="$2"
  candidates=$(printf '%s\n' "$files" | grep -E "$ENV_PATTERN" | grep -vE "$EXEMPT" || true)

  work=$(mktemp) || return 2
  violations=0

  for f in $candidates; do
    # The private key. Never committed, under any name — this is the one file
    # whose leak makes every encrypted value in the repo readable.
    case "$f" in
      *.keys|*.keys.*)
        violations=$((violations + 1))
        echo "  BLOCK $f — this is the dotenvx PRIVATE KEY. It must never be committed." >&2
        continue
        ;;
    esac

    # In --staged mode read the staged blob, not the worktree file: they differ
    # exactly when someone edits after `git add`, which is the case worth catching.
    if [ "$mode" = "--staged" ]; then
      git show ":$f" >"$work" 2>/dev/null || {
        violations=$((violations + 1))
        echo "  BLOCK $f — cannot read the staged blob." >&2
        continue
      }
    else
      [ -f "$f" ] || continue
      cat "$f" >"$work"
    fi

    line_no=0
    # Redirected, not piped: a `while` on the right of a pipe runs in a subshell
    # and its count of what it found dies with it.
    while IFS= read -r line || [ -n "$line" ]; do
      line_no=$((line_no + 1))
      case "$line" in
        ''|'#/'*) continue ;;             # blank, or dotenvx's own `#/…` banner
        '#'*)
          # A commented-out KEY=value is where a plaintext secret hides in plain
          # sight: dotenvx leaves comments untouched when it encrypts. Only a
          # comment that un-comments to KEY=<plaintext> is blocked; prose
          # comments and commented ciphertext/empty values pass.
          ckey=$(printf '%s' "$line" | sed -n 's/^[[:space:]]*#[[:space:]]*\(export[[:space:]]\{1,\}\)\{0,1\}\([A-Za-z_][A-Za-z0-9_]*\)=.*$/\2/p')
          [ -z "$ckey" ] && continue
          case "$ckey" in DOTENV_PUBLIC_KEY*) continue ;; esac
          cval=$(printf '%s' "$line" | sed 's/^[[:space:]]*#[[:space:]]*//; s/^[^=]*=//; s/^["'\'']//; s/["'\'']$//')
          case "$cval" in
            encrypted:*|'') continue ;;
            *) violations=$((violations + 1))
               echo "  BLOCK $f:$line_no — commented-out \`$ckey\` carries a PLAINTEXT value. dotenvx does not encrypt comments; delete the line." >&2 ;;
          esac
          continue
          ;;
      esac

      key=$(printf '%s' "$line" | sed -n 's/^[[:space:]]*\(export[[:space:]]\{1,\}\)\{0,1\}\([A-Za-z_][A-Za-z0-9_]*\)=.*$/\2/p')

      # A line this reader cannot classify is an error, not a skip. A checker
      # that silently ignores what it does not understand waves through the
      # one file it existed to stop.
      if [ -z "$key" ]; then
        violations=$((violations + 1))
        echo "  BLOCK $f:$line_no — not a comment and not KEY=value; cannot verify it is encrypted." >&2
        continue
      fi

      case "$key" in
        DOTENV_PUBLIC_KEY*) continue ;;   # the public half; publishing it is the point
      esac

      value=$(printf '%s' "$line" | sed 's/^[^=]*=//; s/^["'\'']//; s/["'\'']$//')
      case "$value" in
        encrypted:*) ;;                   # good
        '') ;;                            # an empty value discloses nothing
        *) violations=$((violations + 1))
           echo "  BLOCK $f:$line_no — \`$key\` is PLAINTEXT. Run: dotenvx encrypt -f $f" >&2 ;;
      esac
    done <"$work"
  done

  rm -f "$work"
  [ "$violations" -eq 0 ]
}

# Every by-design failure must fire and every legitimate shape must pass. A
# gate that has only ever seen green is untested; the load-bearing case is the
# first one, a plaintext value under a filename that says otherwise.
self_test() {
  tmp=$(mktemp -d) || exit 2
  failures=0
  run_case() {
    label="$1"; name="$2"; body="$3"; must_fail="$4"
    d="$tmp/$(printf '%s' "$label" | tr -c 'A-Za-z0-9' '-')"; mkdir -p "$d"
    printf '%s' "$body" > "$d/$name"
    if scan --file "$d/$name" 2>/dev/null; then fired=0; else fired=1; fi
    if [ "$fired" -eq "$must_fail" ]; then ok='ok  '; else ok='FAIL'; failures=$((failures + 1)); fi
    echo "  $ok  $label: $([ "$fired" -eq 1 ] && echo fires || echo passes)"
  }
  run_case "a plaintext value in .env"                 .env      'TOKEN=abc123
'  1
  run_case "the private key under any name"           .env.keys 'DOTENV_PRIVATE_KEY=encrypted:looks-fine
'  1
  run_case "a commented-out plaintext value"          .env      '# TOKEN=abc123
'  1
  run_case "a line that is neither comment nor KEY=v" .env      'export
'  1
  run_case "a plaintext value in .env.production"     .env.production 'A=1
'  1
  run_case "an encrypted .env with the public key"    .env      '#/---[DOTENV_PUBLIC_KEY]---/
DOTENV_PUBLIC_KEY="02abc"
# .env
BAMBU_TOKEN="encrypted:BBx"
EMPTY=
'  0
  run_case "a prose comment and commented ciphertext" .env      '# printer config
# OLD=encrypted:BBy
'  0
  run_case ".env.example placeholders are exempt"     .env.example 'BAMBU_TOKEN=your-token-here
'  0
  rm -rf "$tmp"
  if [ "$failures" -gt 0 ]; then
    echo "check_env_encrypted --self-test: $failures case(s) behaved wrongly" >&2
    return 1
  fi
  echo "check_env_encrypted --self-test: all cases behaved as designed"
}

case "$MODE" in
  --self-test) self_test; exit $? ;;
  --staged) files=$(git diff --cached --name-only --diff-filter=ACM) ;;
  tracked)  files=$(git ls-files) ;;
  --file)   files="${2:-}"; [ -n "$files" ] || { echo "usage: $0 --file <path>" >&2; exit 2; } ;;
  *) echo "usage: $0 [--staged | --file <path> | --self-test]" >&2; exit 2 ;;
esac

if scan "$MODE" "$files"; then
  echo "check_env_encrypted: OK (every checked env value is encrypted)."
  exit 0
fi
echo "" >&2
echo "check_env_encrypted: refusing." >&2
echo "  This repo's .env is committed ENCRYPTED (dotenvx; .env.keys stays ignored)." >&2
echo "  A plaintext value here is published to GitHub the moment it is pushed, and" >&2
echo "  a pushed credential is compromised whether or not the commit is removed." >&2
echo "  Encrypt:  dotenvx encrypt -f .env      Verify: make validate-env" >&2
exit 1
