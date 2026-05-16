#!/usr/bin/env python3
"""Verify every exercise *solution* in chapters/*.json matches expected_output."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHECK_WORK = ROOT / ".check-go-work"
TIMEOUT_SEC = 60
GO_MOD = "module learnsnippet\n\ngo 1.21\n"
PATH_HEADER = re.compile(r"(?i)^\s*//\s*(?:File:\s*|path:\s*)(\S+)\s*$")


def resolve_chapters_dir() -> Path:
    env = os.environ.get("LEARN_GO_CHAPTERS", "").strip()
    if env:
        return Path(env)
    for path in (ROOT / "chapters", Path.cwd() / "chapters"):
        if path.is_dir() and any(path.glob("*.json")):
            return path
    return ROOT / "chapters"


def _default_name(part: str, index: int) -> str:
    if "func Test" in part or "func Benchmark" in part:
        return "main_test.go"
    return "main.go" if index == 0 else f"file_{index + 1}.go"


def _split_path_header(part: str) -> tuple[str, str]:
    lines = part.splitlines()
    if lines and (m := PATH_HEADER.match(lines[0])):
        return m.group(1), "\n".join(lines[1:]).strip()
    return "", part.strip()


def parse_source_files(code: str, expected: str) -> dict[str, str]:
    code = code.strip()
    if not code:
        raise ValueError("empty source")

    if "\n---\n" in code:
        files: dict[str, str] = {}
        for i, part in enumerate(code.split("\n---\n")):
            part = part.strip()
            if not part:
                continue
            path, body = _split_path_header(part)
            if not path:
                path = _default_name(part, i)
            files[path] = body
        return files

    lines = code.splitlines()
    marker_files: dict[str, str] = {}
    current = ""
    body: list[str] = []
    for line in lines:
        if m := PATH_HEADER.match(line):
            if current:
                marker_files[current] = "\n".join(body).strip()
            current = m.group(1)
            body = []
        elif current:
            body.append(line)
    if current:
        marker_files[current] = "\n".join(body).strip()
    if len(marker_files) > 1:
        return marker_files

    if expected.strip() == "PASS":
        for i, line in enumerate(lines):
            if line.strip().lower() in ("// main_test.go", "// file: main_test.go"):
                main = "\n".join(lines[:i]).strip()
                test = "\n".join(lines[i + 1 :]).strip()
                if main and "func Test" in test:
                    if PATH_HEADER.match(main.splitlines()[0]):
                        _, main = _split_path_header(main)
                    return {"main.go": main, "main_test.go": test}

    path, body = _split_path_header(code)
    if path:
        return {path: body}
    return {"main.go": code}


def write_workspace(work: Path, solution: str, expected: str) -> str:
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    (work / "go.mod").write_text(GO_MOD, encoding="utf-8")
    for rel, body in parse_source_files(solution, expected).items():
        rel_path = Path(rel)
        if ".." in rel_path.parts:
            raise ValueError(f"invalid path {rel}")
        dest = work / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body.rstrip() + "\n", encoding="utf-8")
    return "test" if expected.strip() == "PASS" else "run"


def check_one(solution: str, expected: str, work: Path) -> tuple[bool, str]:
    exp = (expected or "").strip()
    mode = write_workspace(work, solution, exp)
    cmd = ["go", "test", "-count=1"] if mode == "test" else ["go", "run", "."]
    try:
        proc = subprocess.run(
            cmd,
            cwd=work,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SEC,
        )
    except subprocess.TimeoutExpired:
        return False, "timed out"
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        return False, f"{' '.join(cmd)} rc={proc.returncode}\n{err[:4000]}"
    if exp == "PASS":
        return True, ""
    got = (proc.stdout or "").strip()
    if got == exp:
        return True, ""
    return False, f"stdout mismatch:\n  expected: {exp!r}\n  got:      {got!r}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--chapter", help="only check this chapter id")
    ap.add_argument("--list-failures-only", action="store_true")
    args = ap.parse_args()

    chapters = resolve_chapters_dir()
    if not chapters.is_dir():
        print(f"no chapters directory: {chapters}", file=sys.stderr)
        return 1

    work_env = os.environ.get("LEARN_GO_CHECK_WORK", "").strip()
    base_work = Path(work_env) if work_env else DEFAULT_CHECK_WORK
    base_work.mkdir(parents=True, exist_ok=True)

    failures: list[tuple[str, str, str]] = []
    skipped = 0
    checked = 0

    for path in sorted(chapters.glob("*.json")):
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
