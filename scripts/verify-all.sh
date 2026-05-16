#!/usr/bin/env bash
# Run the maintainer verification matrix from the repository root.
#
# Usage (from anywhere):
#   ./scripts/verify-all.sh
#   ./scripts/verify-all.sh --skip-check-solutions   # fast: no bundled-solution grading
#   PYTHON=/path/to/python ./scripts/verify-all.sh
#
# Prerequisites:
#   ./scripts/setup-dev.sh   — root .venv + pytest for Python tracks
#   Toolchains on PATH for tracks you grade: cc/gcc, dotnet, javac, cargo, go, nasm, ld, gcc (asm)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SKIP_CHECK_SOLUTIONS=0
SERIAL_CHECK_SOLUTIONS=0

usage() {
  sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage 0 ;;
    --skip-check-solutions) SKIP_CHECK_SOLUTIONS=1; shift ;;
    --serial-check-solutions) SERIAL_CHECK_SOLUTIONS=1; shift ;;
    *) echo "Unknown option: $1" >&2; usage 1 ;;
  esac
done

if [[ -n "${PYTHON:-}" ]]; then
  PY="$PYTHON"
else
  if [[ -x "$ROOT/.venv/bin/python" ]]; then
    PY="$ROOT/.venv/bin/python"
  elif [[ -x "$ROOT/.venv/Scripts/python.exe" ]]; then
    PY="$ROOT/.venv/Scripts/python.exe"
  else
    PY="$(command -v python3 || true)"
  fi
fi

if [[ -z "${PY:-}" || ! -x "$PY" ]]; then
  echo "No Python interpreter found. Run ./scripts/setup-dev.sh or set PYTHON=." >&2
  exit 1
fi

# Absolute path for parallel subshells; use abspath (not realpath) so a venv entrypoint
# stays under .venv/ and keeps its site-packages.
PY="$("$PY" -c 'import os, sys; print(os.path.abspath(sys.executable))')"

step() { printf '\n==> %s\n' "$*"; }
fail() { printf 'FAIL: %s\n' "$*" >&2; FAILED=1; }

FAILED=0
TMPDIR="${TMPDIR:-/tmp}"
WORK="$TMPDIR/learn-languages-verify-$$"
mkdir -p "$WORK"
trap 'rm -rf "$WORK"' EXIT

step "Python $("$PY" --version 2>&1) at $PY"

step "compileall (hub + Python TUIs)"
"$PY" -m compileall -q \
  "$ROOT/learn_languages" \
  "$ROOT/c/learn_c_tui" \
  "$ROOT/csharp/learn_cs_tui" \
  "$ROOT/python/learn_python_tui" \
  "$ROOT/java/learn_java_tui"

step "hub import smoke"
"$PY" -c "from learn_languages.tracks import TRACKS; from learn_languages.app import LearnLanguagesMenu; print('hub OK:', len(TRACKS), 'tracks')"

if ! "$PY" -m pytest --version >/dev/null 2>&1; then
  echo "pytest not installed — run ./scripts/setup-dev.sh" >&2
  exit 1
fi

for track in c csharp python java; do
  step "pytest ($track)"
  (cd "$ROOT/$track" && "$PY" -m pytest tests/ -q)
done

if command -v go >/dev/null 2>&1; then
  step "go test"
  (cd "$ROOT/go" && go test ./...)
else
  fail "go not on PATH — skipped go test"
fi

if command -v cargo >/dev/null 2>&1; then
  step "cargo test (rust)"
  (cd "$ROOT/rust" && cargo test -q)
  step "cargo test (asmx64)"
  (cd "$ROOT/asmx64" && cargo test -q)
  step "cargo build (rust)"
  (cd "$ROOT/rust" && cargo build -q)
  step "cargo build --release (asmx64)"
  (cd "$ROOT/asmx64" && cargo build --release -q)
else
  fail "cargo not on PATH — skipped rust/asmx64 tests and builds"
fi

if command -v go >/dev/null 2>&1; then
  step "go build"
  (cd "$ROOT/go" && go build -o "$WORK/go-tui-smoke" .)
fi

step "chapter JSON parse (all tracks)"
"$PY" - "$ROOT" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
tracks = ("rust", "go", "c", "csharp", "python", "java", "asmx64")
errors: list[str] = []
count = 0
for track in tracks:
    chdir = root / track / "chapters"
    if not chdir.is_dir():
        errors.append(f"{track}: missing chapters/")
        continue
    for path in sorted(chdir.glob("*.json")):
        count += 1
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{track}/{path.name}: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{track}/{path.name}: root is not an object")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"JSON OK: {count} files")
PY

run_check_solutions() {
  local track="$1"
  local log="$WORK/check-$track.log"
  local exitf="$WORK/check-$track.exit"
  local ec=0
  set +e
  (cd "$ROOT/$track" && "$PY" scripts/check_solutions.py >"$log" 2>&1)
  ec=$?
  set -e
  echo "$ec" >"$exitf"
}

if [[ "$SKIP_CHECK_SOLUTIONS" -eq 0 ]]; then
  CHECK_TRACKS=(rust c csharp python java asmx64)
  step "check_solutions (${#CHECK_TRACKS[@]} tracks, PYTHON=$PY)"
  if [[ "$SERIAL_CHECK_SOLUTIONS" -eq 1 ]]; then
    for track in "${CHECK_TRACKS[@]}"; do
      run_check_solutions "$track"
    done
  else
    pids=()
    for track in "${CHECK_TRACKS[@]}"; do
      run_check_solutions "$track" &
      pids+=("$!")
    done
    for pid in "${pids[@]}"; do
      wait "$pid" || true
    done
  fi
  for track in "${CHECK_TRACKS[@]}"; do
    ec="$(cat "$WORK/check-$track.exit")"
    echo "--- $track (exit $ec) ---"
    tail -n 3 "$WORK/check-$track.log" || true
    if [[ "$ec" != "0" ]]; then
      fail "check_solutions $track — see $WORK/check-$track.log"
    fi
  done
else
  step "check_solutions (skipped)"
fi

if [[ "$FAILED" -ne 0 ]]; then
  echo >&2
  echo "verify-all: one or more steps failed." >&2
  exit 1
fi

step "verify-all: all steps passed"
