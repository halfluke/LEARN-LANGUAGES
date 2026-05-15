#!/usr/bin/env python3
"""Verify every exercise *solution* in chapters/*.json assembles, links, and matches expected_output.

Mirrors src/executor.rs routing:
  - `nasm -f elf64` -> `solution.o`
  - if `extern` appears (case-insensitive) in source -> `gcc -no-pie -o solution solution.o`
  - else -> `ld -o solution solution.o`
  - run `./solution`; exit code must be 0; compare trimmed stdout to trimmed expected_output

By default each exercise uses a fresh temp directory (same isolation model as rustc-only
checks in LEARN-RUST). Optionally set LEARN_ASMX64_CHECK_WORK to a persistent directory
to reuse one folder for all runs (objects are tiny).

Usage:
  python3 scripts/check_solutions.py
  python3 scripts/check_solutions.py --chapter variables
  python3 scripts/check_solutions.py --list-failures-only

Env:
  LEARN_ASMX64_CHECK_WORK  if set, build under this directory instead of per-exercise temp dirs
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "chapters"

ASSEMBLE_TIMEOUT = 30
RUN_TIMEOUT = 10


def needs_gcc_link(code: str) -> bool:
    return "extern" in code.lower()


def run_asm_pipeline(
    code: str,
    work: Path | None,
) -> tuple[int, str, str, str]:
    """Returns (effective_rc, stdout, stderr, detail_prefix). effective_rc 0 means success."""
    if work is not None:
        tmp = work
        tmp.mkdir(parents=True, exist_ok=True)
        cleanup = False
    else:
        tmp = Path(tempfile.mkdtemp(prefix="lr-asm-check-"))
        cleanup = True

    asm = tmp / "solution.asm"
    obj = tmp / "solution.o"
    out_bin = tmp / "solution"

    try:
        asm.write_text(code, encoding="utf-8")
        if obj.exists():
            obj.unlink()
        if out_bin.exists():
            out_bin.unlink()

        nasm = subprocess.run(
            ["nasm", "-f", "elf64", "-o", str(obj), str(asm)],
            capture_output=True,
            text=True,
            timeout=ASSEMBLE_TIMEOUT,
        )
        if nasm.returncode != 0:
            return (
                nasm.returncode,
                "",
                nasm.stderr,
                f"nasm rc={nasm.returncode}\nstderr:\n{nasm.stderr[:4000]}",
            )

        if needs_gcc_link(code):
            link = subprocess.run(
                ["gcc", "-no-pie", "-o", str(out_bin), str(obj)],
                capture_output=True,
                text=True,
                timeout=ASSEMBLE_TIMEOUT,
            )
        else:
            link = subprocess.run(
                ["ld", "-o", str(out_bin), str(obj)],
                capture_output=True,
                text=True,
                timeout=ASSEMBLE_TIMEOUT,
            )

        if link.returncode != 0:
            return (
                link.returncode,
                "",
                link.stderr,
                f"link rc={link.returncode}\nstderr:\n{link.stderr[:4000]}",
            )

        run = subprocess.run(
            [str(out_bin)],
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT,
        )
        if run.returncode != 0:
            return (
                run.returncode,
                run.stdout,
                run.stderr,
                f"run rc={run.returncode}\nstderr:\n{run.stderr[:4000]}",
            )
        return 0, run.stdout, run.stderr, ""
    finally:
        if cleanup:
            shutil.rmtree(tmp, ignore_errors=True)


def check_one(solution: str, expected: str, work: Path | None) -> tuple[bool, str]:
    exp = (expected or "").strip()
    rc, stdout, stderr, err = run_asm_pipeline(solution.strip(), work)
    if rc != 0:
        return False, err or f"nonzero rc={rc}\nstderr:\n{stderr[:4000]}"
    got = stdout.strip()
    if got == exp:
        return True, ""
    return False, f"stdout mismatch:\n  expected: {exp!r}\n  got:      {got!r}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--chapter",
        help="only check this chapter id (e.g. variables)",
    )
    ap.add_argument(
        "--list-failures-only",
        action="store_true",
        help="print only failing chapter/exercise lines",
    )
    args = ap.parse_args()

    work_env = os.environ.get("LEARN_ASMX64_CHECK_WORK", "").strip()
    work: Path | None = Path(work_env) if work_env else None
    if work is not None:
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
