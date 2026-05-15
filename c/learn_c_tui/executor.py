"""Compile and run a single C11 translation unit (cc or gcc)."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool


COMPILE_TIMEOUT = 60
RUN_TIMEOUT = 15


def resolve_c_compiler() -> str:
    """Prefer POSIX `cc`, then `gcc` (plan: v1 is POSIX toolchains; MSVC out of scope)."""
    for name in ("cc", "gcc"):
        if shutil.which(name):
            return name
    raise RuntimeError(
        "No C compiler found. Expected `cc` or `gcc` on PATH.\n\n"
        "Linux: sudo apt install build-essential\n"
        "macOS: install Xcode Command Line Tools\n"
        "Windows: use WSL2 or MSYS2 with gcc — native MSVC is not supported in v1."
    )


def check_cc_available() -> None:
    """Fail fast before the TUI: probe compiler."""
    cc = resolve_c_compiler()
    try:
        p = subprocess.run(
            [cc, "--version"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except OSError as e:
        raise RuntimeError(f"Could not run {cc}: {e}") from e
    if p.returncode != 0:
        raise RuntimeError(f"`{cc} --version` failed.\n" + (p.stderr or p.stdout or ""))


def needs_link_m(code: str) -> bool:
    """Append -lm when libm is likely needed (link order: source before -lm)."""
    low = code.lower()
    if "#include <math.h>" in low or "#include <tgmath.h>" in low:
        return True
    for needle in (" sin(", " cos(", " tan(", " pow(", " sqrt(", " exp(", " log("):
        if needle in low:
            return True
    return False


def execute_code(code: str, *, work_dir: Path | None = None) -> ExecutionResult:
    """Write solution.c, compile with -std=c11, run binary. If work_dir is None, use a fresh temp dir and delete it."""
    cleanup = work_dir is None
    if work_dir is None:
        project_dir = Path(tempfile.mkdtemp(prefix="learn-c-run-"))
    else:
        project_dir = work_dir
        project_dir.mkdir(parents=True, exist_ok=True)

    cc = resolve_c_compiler()
    src = project_dir / "solution.c"
    out_bin = project_dir / "learn_c_run"

    env = os.environ.copy()

    try:
        src.write_text(code, encoding="utf-8")
        if out_bin.is_file():
            out_bin.unlink()

        compile_cmd = [
            cc,
            "-std=c11",
            "-D_DEFAULT_SOURCE",
            "-Wall",
            "-Wextra",
            "-o",
            str(out_bin),
            str(src),
        ]
        if needs_link_m(code):
            compile_cmd.append("-lm")

        comp = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            timeout=COMPILE_TIMEOUT,
            cwd=str(project_dir),
            env=env,
        )
        if comp.returncode != 0:
            return ExecutionResult(
                stdout="",
                stderr=comp.stderr or comp.stdout or "compile failed",
                exit_code=comp.returncode,
                timed_out=False,
            )

        try:
            run = subprocess.run(
                [str(out_bin)],
                capture_output=True,
                text=True,
                timeout=RUN_TIMEOUT,
                cwd=str(project_dir),
                env=env,
                stdin=subprocess.DEVNULL,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(stdout="", stderr="", exit_code=-1, timed_out=True)

        return ExecutionResult(
            stdout=run.stdout or "",
            stderr=run.stderr or "",
            exit_code=run.returncode,
            timed_out=False,
        )
    finally:
        if cleanup:
            shutil.rmtree(project_dir, ignore_errors=True)
