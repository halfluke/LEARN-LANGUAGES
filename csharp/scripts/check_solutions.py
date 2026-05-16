#!/usr/bin/env python3
"""Verify every exercise *solution* in chapters/*.json builds with `dotnet` and matches expected_output.

Uses the same path as the learner TUI: one SDK project per worker, overwrite Program.cs,
``dotnet build`` (``--no-restore`` after first build), then ``dotnet run --no-build``.

Usage:
  python3 scripts/check_solutions.py
  python3 scripts/check_solutions.py --chapter variables
  python3 scripts/check_solutions.py --jobs 2
  python3 scripts/check_solutions.py --list-failures-only

Env:
  LEARN_CSHARP_CHECK_WORK  override project dir (default: <repo>/.check-csharp-work).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "chapters"
DEFAULT_CHECK_WORK = ROOT / ".check-csharp-work"
DEFAULT_JOBS = 2

sys.path.insert(0, str(ROOT))

from learn_cs_tui.executor import check_dotnet_available, execute_code  # noqa: E402


@dataclass(frozen=True)
class _Exercise:
    chapter_id: str
    exercise_id: str
    solution: str
    expected: str


def check_one(solution: str, expected: str, work: Path) -> tuple[bool, str]:
    exp = (expected or "").strip()
    res = execute_code(
        solution.strip(),
        work_dir=work,
        incremental=True,
        prefer_exec=False,
    )
    if res.timed_out:
        return False, "timed out"
    if res.exit_code != 0:
        detail = (res.stderr or res.stdout or "(no output)")[:4000]
        return False, f"dotnet rc={res.exit_code}\n{detail}"
    got = res.stdout.strip()
    if got == exp:
        return True, ""
    return False, f"stdout mismatch:\n  expected: {exp!r}\n  got:      {got!r}"


def _worker_batch(batch: list[_Exercise], work_base: Path, worker_id: int) -> list[tuple[str, str, bool, str]]:
    work = work_base if worker_id < 0 else work_base / f"worker-{worker_id}"
    return [
        (ex.chapter_id, ex.exercise_id, *check_one(ex.solution, ex.expected, work))
        for ex in batch
    ]


def _partition(items: list[_Exercise], jobs: int) -> list[list[_Exercise]]:
    buckets: list[list[_Exercise]] = [[] for _ in range(jobs)]
    for i, item in enumerate(items):
        buckets[i % jobs].append(item)
    return [b for b in buckets if b]


def _count_skipped(chapter_filter: str | None) -> int:
    skipped = 0
    for path in sorted(CHAPTERS.glob("*.json")):
        ch = json.loads(path.read_text(encoding="utf-8"))
        if chapter_filter and ch["id"] != chapter_filter:
            continue
        for ex in ch.get("exercises", []):
            if not (ex.get("solution") or "").strip():
                skipped += 1
    return skipped


def _collect_exercises(chapter_filter: str | None) -> list[_Exercise]:
    out: list[_Exercise] = []
    for path in sorted(CHAPTERS.glob("*.json")):
        ch = json.loads(path.read_text(encoding="utf-8"))
        cid = ch["id"]
        if chapter_filter and cid != chapter_filter:
            continue
        for ex in ch.get("exercises", []):
            sol = (ex.get("solution") or "").strip()
            if not sol:
                continue
            out.append(
                _Exercise(
                    chapter_id=cid,
                    exercise_id=ex["id"],
                    solution=sol,
                    expected=ex.get("expected_output") or "",
                )
            )
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--chapter", help="only check this chapter id (e.g. variables)")
    ap.add_argument(
        "--jobs",
        type=int,
        default=DEFAULT_JOBS,
        help=f"parallel workers (default {DEFAULT_JOBS}; use 1 for sequential)",
    )
    ap.add_argument(
        "--list-failures-only",
        action="store_true",
        help="print only failing chapter/exercise lines",
    )
    args = ap.parse_args()

    if args.jobs < 1:
        print("--jobs must be >= 1", file=sys.stderr)
        return 1

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

    exercises = _collect_exercises(args.chapter)
    skipped = _count_skipped(args.chapter)
    checked = len(exercises)
    failures: list[tuple[str, str, str]] = []
    t0 = time.monotonic()

    if args.jobs == 1:
        results = _worker_batch(exercises, work, -1)
    else:
        parts = _partition(exercises, args.jobs)
        results = []
        with ThreadPoolExecutor(max_workers=len(parts)) as pool:
            futs = {
                pool.submit(_worker_batch, part, work, wid): wid
                for wid, part in enumerate(parts)
            }
            for fut in as_completed(futs):
                results.extend(fut.result())

    elapsed = time.monotonic() - t0

    for cid, eid, ok, detail in results:
        if not ok:
            failures.append((cid, eid, detail))
            if not args.list_failures_only:
                print(f"FAIL {cid}::{eid}\n{detail}\n", file=sys.stderr)

    if args.list_failures_only:
        for cid, eid, _ in failures:
            print(f"{cid}::{eid}")

    summary = (
        f"checked={checked} skipped_empty_solution={skipped} failed={len(failures)} "
        f"jobs={args.jobs} seconds={elapsed:.1f}"
    )
    print(summary, file=sys.stderr if failures else sys.stdout)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
