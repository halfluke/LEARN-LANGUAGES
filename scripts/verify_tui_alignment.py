#!/usr/bin/env python3
"""Verify bundled solutions pass through each track's *learner* executor + validator.

Uses the same execute_code + Validator.validate paths as the Textual TUIs.
Rust, Go, and asmx64 also have `*_alignment_test` in their crates (run via verify-all).

Usage (repo root):
  python3 scripts/verify_tui_alignment.py
  python3 scripts/verify_tui_alignment.py --track csharp
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEXTUAL_TRACKS: dict[str, tuple[str, str, str, str]] = {
    "python": (
        "python",
        "learn_python_tui.executor.execute_code",
        "learn_python_tui.validator.Validator",
    ),
    "java": (
        "java",
        "learn_java_tui.executor.execute_code",
        "learn_java_tui.validator.Validator",
    ),
    "c": (
        "c",
        "learn_c_tui.executor.execute_code",
        "learn_c_tui.validator.Validator",
    ),
    "csharp": (
        "csharp",
        "learn_cs_tui.executor.execute_code",
        "learn_cs_tui.validator.Validator",
    ),
}


def _import_attr(dotted: str):
    mod_name, _, attr = dotted.rpartition(".")
    mod = importlib.import_module(mod_name)
    return getattr(mod, attr)


def _exercise_from_json(ex: dict) -> types.SimpleNamespace:
    return types.SimpleNamespace(
        expected_output=ex.get("expected_output") or "",
        hints=ex.get("hints") or [],
        solution=(ex.get("solution") or "").strip(),
    )


def check_textual_track(track_key: str, chapter_filter: str | None) -> list[str]:
    track_dir, exec_path, val_path = TEXTUAL_TRACKS[track_key]
    if str(ROOT / track_dir) not in sys.path:
        sys.path.insert(0, str(ROOT / track_dir))
    execute_code = _import_attr(exec_path)
    Validator = _import_attr(val_path)
    validator = Validator()

    chapters_dir = ROOT / track_dir / "chapters"
    failures: list[str] = []
    work_root = ROOT / track_dir / ".verify-tui-alignment-work"
    if work_root.exists():
        import shutil

        shutil.rmtree(work_root)
    work_root.mkdir(parents=True, exist_ok=True)
    # Reuse one build tree per track (like a learner session), not per exercise.
    session_work = work_root / "_session"

    for path in sorted(chapters_dir.glob("*.json")):
        ch = json.loads(path.read_text(encoding="utf-8"))
        cid = ch["id"]
        if chapter_filter and cid != chapter_filter:
            continue
        for ex in ch.get("exercises", []):
            eid = ex["id"]
            sol = (ex.get("solution") or "").strip()
            if not sol:
                continue
            if track_key == "csharp":
                res = execute_code(
                    sol,
                    work_dir=session_work,
                    incremental=True,
                    prefer_exec=False,
                )
            elif track_key in ("java", "c"):
                res = execute_code(sol, work_dir=session_work)
            else:
                res = execute_code(sol, work_dir=session_work)
            result = validator.validate(res, _exercise_from_json(ex), 0)
            if not result.passed:
                failures.append(f"{track_key}::{cid}::{eid}: {result.message[:800]}")

    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--track", choices=[*TEXTUAL_TRACKS, "all"], default="all")
    ap.add_argument("--chapter", help="chapter id filter")
    args = ap.parse_args()

    failed: list[str] = []
    tracks = list(TEXTUAL_TRACKS) if args.track == "all" else [args.track]
    for key in tracks:
        print(f"verify_tui_alignment: {key}", file=sys.stderr)
        failed.extend(check_textual_track(key, args.chapter))

    if failed:
        print("\n".join(failed), file=sys.stderr)
        print(f"FAILED {len(failed)} exercise(s)", file=sys.stderr)
        return 1

    print("verify_tui_alignment: OK", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
