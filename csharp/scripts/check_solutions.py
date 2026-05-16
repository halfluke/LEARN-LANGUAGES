#!/usr/bin/env python3
"""Verify every exercise *solution* in chapters/*.json builds with `dotnet` and matches expected_output.

Reuses one SDK console project under LEARN_CSHARP_CHECK_WORK: each solution overwrites Program.cs,
then ``dotnet build`` + ``dotnet run --no-build`` (see learn_cs_tui.executor).

Usage:
  python3 scripts/check_solutions.py
  python3 scripts/check_solutions.py --chapter variables
  python3 scripts/check_solutions.py --list-failures-only

Env:
  LEARN_CSHARP_CHECK_WORK  override project dir (default: <repo>/.check-csharp-work).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "chapters"
DEFAULT_CHECK_WORK = ROOT / ".check-csharp-work"

sys.path.insert(0, str(ROOT))

from learn_cs_tui.executor import check_dotnet_available, execute_code_in_dir  # noqa: E402


def check_one(
    solution: str,
    expected: str,
    work: Path,
) -> tuple[bool, str]:
    exp = (expected or "").strip()
    res = execute_code_in_dir(solution.strip(), work)
    if res.timed_out:
        return False, "timed out"
    if res.exit_code != 0:
        detail = (res.stderr or res.stdout or "(no output)")[:4000]
        return False, f"dotnet rc={res.exit_code}\n{detail}"
    got = res.stdout.strip()
    if got == exp:
        return True, ""
    return False, f"stdout mismatch:\n  expected: {exp!r}\n  got:      {got!r}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--chapter", help="only check this chapter id (e.g. variables)")
    ap.add_argument(
        "--list-failures-only",
        action="store_true",
        help="print only failing chapter/exercise lines",
    )
    args = ap.parse_args()

    try:
        check_dotnet_available()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1

    work_env = os.environ.get("LEARN_CSHARP_CHECK_WORK", "").strip()
    work = Path(work_env) if work_env else DEFAULT_CHECK_WORK
    work = work.resolve()
    work.mkdir(parents=True, exist_ok=True)

    if not CHAPTERS.is_dir():
        print("missing chapters dir:", CHAPTERS, file=sys.stderr)
        return 1

    paths = sorted(CHAPTERS.glob("*.json"))
    failures: list[tuple[str, str, str]] = []
    skipped = 0
    checked = 0

    for path in paths:
        ch = json.loads(path.read_text(encoding="utf-8"))
        cid = ch["id"]
        if args.chapter and cid != args.chapter:
            continue
        for ex in ch.get("exercises", []):
            eid = ex["id"]
            sol = (ex.get("solution") or "").strip()
            if not sol:
                skipped += 1
                continue
            checked += 1
            ok, detail = check_one(sol, ex.get("expected_output") or "", work)
            if not ok:
                failures.append((cid, eid, detail))
                if not args.list_failures_only:
                    print(f"FAIL {cid}::{eid}\n{detail}\n", file=sys.stderr)

    if args.list_failures_only:
        for cid, eid, _ in failures:
            print(f"{cid}::{eid}")

    print(
        f"checked={checked} skipped_empty_solution={skipped} failed={len(failures)}",
        file=sys.stderr if failures else sys.stdout,
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
