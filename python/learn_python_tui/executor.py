"""Run learner Python 3 scripts (python3 solution.py)."""

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


COMPILE_TIMEOUT = 30
RUN_TIMEOUT = 15


def resolve_python() -> str:
    for name in ("python3", "python"):
        if shutil.which(name):
            return name
    raise RuntimeError(
        "No Python interpreter found. Expected `python3` or `python` on PATH."
    )


def check_python_available() -> None:
    py = resolve_python()
    try:
        p = subprocess.run(
            [py, "--version"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except OSError as e:
        raise RuntimeError(f"Could not run {py}: {e}") from e
    if p.returncode != 0:
        raise RuntimeError(f"`{py} --version` failed.\n" + (p.stderr or p.stdout or ""))


def execute_code(code: str, *, work_dir: Path | None = None) -> ExecutionResult:
    """Write solution.py and run with python3."""
    cleanup = work_dir is None
    if work_dir is None:
        project_dir = Path(tempfile.mkdtemp(prefix="learn-python-run-"))
    else:
        project_dir = work_dir
        project_dir.mkdir(parents=True, exist_ok=True)

    py = resolve_python()
    src = project_dir / "solution.py"
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")

    try:
        src.write_text(code, encoding="utf-8")
        try:
            run = subprocess.run(
                [py, str(src)],
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
