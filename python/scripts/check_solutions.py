#!/usr/bin/env python3
"""Verify every exercise *solution* in chapters/*.json matches expected_output."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "chapters"
DEFAULT_CHECK_WORK = ROOT / ".check-python-work"

sys.path.insert(0, str(ROOT))

from learn_python_tui.executor import execute_code  # noqa: E402


def check_one(solution: str, expected: str, work: Path) -> tuple[bool, str]:
    exp = (expected or "").strip()
    work.mkdir(parents=True, exist_ok=True)
    res = execute_code(solution.strip(), work_dir=work)
    if res.timed_out:
        return False, "timed out"
    if res.exit_code != 0:
        err = res.stderr or res.stdout or ""
        return False, f"run rc={res.exit_code}\nstderr:\n{err[:4000]}"
    got = res.stdout.strip()
    if got == exp:
        return True, ""
    return False, f"stdout mismatch:\n  expected: {exp!r}\n  got:      {got!r}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--chapter", help="only check this chapter id")
    ap.add_argument("--list-failures-only", action="store_true")
    args = ap.parse_args()

    work_env = os.environ.get("LEARN_PYTHON_CHECK_WORK", "").strip()
    base_work = Path(work_env) if work_env else DEFAULT_CHECK_WORK
    base_work.mkdir(parents=True, exist_ok=True)

    failures: list[tuple[str, str, str]] = []
    skipped = 0
    checked = 0

    for path in sorted(CHAPTERS.glob("*.json")):
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
            work = (base_work / cid / eid).resolve()
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
