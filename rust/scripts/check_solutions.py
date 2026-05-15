#!/usr/bin/env python3
"""Verify every exercise *solution* in chapters/*.json compiles and matches expected_output.

Mirrors src/executor.rs routing:
  - #[test] in source -> cargo test -q (PASS == exit 0)
  - serde_json::, serde::, chrono::, chrono_tz:: -> cargo run -q
  - else -> rustc then run binary

Uses one persistent Cargo workspace + shared CARGO_TARGET_DIR so the first compile
pulls deps once; later exercises reuse the artifact cache.

Usage:
  python3 scripts/check_solutions.py
  python3 scripts/check_solutions.py --chapter json
  python3 scripts/check_solutions.py --list-failures-only

Env:
  LEARN_RUST_CHECK_TARGET  override target dir (default: <repo>/.check-solutions-target)
  LEARN_RUST_CHECK_CRATE   override workspace dir (default: <repo>/.check-solutions-crate)
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

CARGO_TOML = """[package]
name = "snippet"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
chrono = { version = "0.4", default-features = false, features = ["clock", "std"] }
chrono-tz = "0.10"
"""

PLACEHOLDER_MAIN = "fn main() {}\n"


def needs_cargo_test(code: str) -> bool:
    return "#[test]" in code


def needs_cargo(code: str) -> bool:
    return (
        "serde_json::" in code
        or "serde::" in code
        or "chrono::" in code
        or "chrono_tz::" in code
    )


def classify(code: str) -> str:
    if needs_cargo_test(code):
        return "cargo_test"
    if needs_cargo(code):
        return "cargo_run"
    return "rustc"


def ensure_cargo_workspace(crate_dir: Path) -> None:
    src = crate_dir / "src"
    src.mkdir(parents=True, exist_ok=True)
    (crate_dir / "Cargo.toml").write_text(CARGO_TOML, encoding="utf-8")
    main_rs = src / "main.rs"
    if not main_rs.exists():
        main_rs.write_text(PLACEHOLDER_MAIN, encoding="utf-8")


def run_cargo(
    crate_dir: Path,
    target_dir: Path,
    args: list[str],
    timeout: int,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["CARGO_TARGET_DIR"] = str(target_dir)
    return subprocess.run(
        ["cargo", *args],
        cwd=crate_dir,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def run_rustc_code(code: str, timeout_compile: int = 90, timeout_run: int = 15) -> tuple[int, str, str]:
    tmp = Path(tempfile.mkdtemp(prefix="lr-rustc-"))
    try:
        one = tmp / "main.rs"
        one.write_text(code, encoding="utf-8")
        out_bin = tmp / "run"
        c = subprocess.run(
            ["rustc", str(one), "-o", str(out_bin)],
            capture_output=True,
            text=True,
            timeout=timeout_compile,
        )
        if c.returncode != 0:
            return c.returncode, "", c.stderr
        r = subprocess.run(
            [str(out_bin)],
            capture_output=True,
            text=True,
            timeout=timeout_run,
        )
        return r.returncode, r.stdout, r.stderr
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def check_one(
    crate_dir: Path,
    target_dir: Path,
    solution: str,
    expected: str,
) -> tuple[bool, str]:
    mode = classify(solution)
    exp = expected.strip()

    if mode == "cargo_test":
        (crate_dir / "src" / "main.rs").write_text(solution, encoding="utf-8")
        p = run_cargo(crate_dir, target_dir, ["test", "-q"], timeout=180)
        if p.returncode != 0:
            return False, f"cargo test rc={p.returncode}\nstderr:\n{p.stderr[:4000]}"
        if exp == "PASS":
            return True, ""
        if p.stdout.strip() == exp:
            return True, ""
        return (
            False,
            f"expected stdout {exp!r} for non-PASS cargo test; got {p.stdout.strip()!r}",
        )

    if mode == "cargo_run":
        (crate_dir / "src" / "main.rs").write_text(solution, encoding="utf-8")
        p = run_cargo(crate_dir, target_dir, ["run", "-q"], timeout=180)
        if p.returncode != 0:
            return False, f"cargo run rc={p.returncode}\nstderr:\n{p.stderr[:4000]}"
        got = p.stdout.strip()
        if got == exp:
            return True, ""
        return False, f"stdout mismatch:\n  expected: {exp!r}\n  got:      {got!r}"

    # rustc
    rc, stdout, stderr = run_rustc_code(solution)
    if rc != 0:
        return False, f"rustc/run rc={rc}\nstderr:\n{stderr[:4000]}"
    got = stdout.strip()
    if got == exp:
        return True, ""
    return False, f"stdout mismatch:\n  expected: {exp!r}\n  got:      {got!r}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--chapter",
        help="only check this chapter id (e.g. json, time)",
    )
    ap.add_argument(
        "--list-failures-only",
        action="store_true",
        help="print only failing chapter/exercise lines",
    )
    args = ap.parse_args()

    target_dir = Path(
        os.environ.get("LEARN_RUST_CHECK_TARGET", ROOT / ".check-solutions-target")
    )
    crate_dir = Path(
        os.environ.get("LEARN_RUST_CHECK_CRATE", ROOT / ".check-solutions-crate")
    )
    target_dir.mkdir(parents=True, exist_ok=True)
    crate_dir.mkdir(parents=True, exist_ok=True)
    ensure_cargo_workspace(crate_dir)

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
            ok, detail = check_one(
                crate_dir,
                target_dir,
                sol,
                ex.get("expected_output") or "",
            )
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
