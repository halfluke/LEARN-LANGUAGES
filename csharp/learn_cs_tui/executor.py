"""Run learner C# in a temporary SDK-style console project (dotnet run)."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool


# First run may restore NuGet packages; keep generous bounds like LEARN-RUST cargo path.
BUILD_RUN_TIMEOUT = 180


def check_dotnet_available() -> None:
    try:
        p = subprocess.run(
            ["dotnet", "--version"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except FileNotFoundError as e:
        raise RuntimeError(
            "`dotnet` is not installed or not in PATH.\n\n"
            "Install the .NET SDK (e.g. https://dotnet.microsoft.com/download ) "
            "and ensure `dotnet --version` works."
        ) from e
    if p.returncode != 0:
        raise RuntimeError("`dotnet --version` failed.\n" + (p.stderr or p.stdout or ""))


def _write_program_cs(project_dir: Path, code: str) -> None:
    (project_dir / "Program.cs").write_text(code, encoding="utf-8")


def execute_code(code: str, *, work_dir: Path | None = None) -> ExecutionResult:
    """Create (or reuse) a console project, overwrite Program.cs, `dotnet run`."""
    cleanup = work_dir is None
    if work_dir is None:
        project_dir = Path(tempfile.mkdtemp(prefix="learn-csharp-run-"))
    else:
        project_dir = work_dir
        project_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.setdefault("DOTNET_NOLOGO", "1")
    env.setdefault("TERM", env.get("TERM", "dumb"))

    try:
        csproj = next(project_dir.glob("*.csproj"), None)
        if csproj is None:
            init = subprocess.run(
                ["dotnet", "new", "console", "--force", "--name", "Snippet", "-o", str(project_dir)],
                capture_output=True,
                text=True,
                timeout=BUILD_RUN_TIMEOUT,
                env=env,
            )
            if init.returncode != 0:
                return ExecutionResult(
                    stdout="",
                    stderr=init.stderr or init.stdout or "dotnet new failed",
                    exit_code=init.returncode,
                    timed_out=False,
                )

        _write_program_cs(project_dir, code)

        start = time.monotonic()
        try:
            run = subprocess.run(
                ["dotnet", "run", "--project", str(project_dir), "--verbosity", "quiet"],
                capture_output=True,
                text=True,
                timeout=BUILD_RUN_TIMEOUT,
                cwd=str(project_dir),
                env=env,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(stdout="", stderr="", exit_code=-1, timed_out=True)

        elapsed = time.monotonic() - start
        _ = elapsed  # reserved for logging
        return ExecutionResult(
            stdout=run.stdout or "",
            stderr=run.stderr or "",
            exit_code=run.returncode,
            timed_out=False,
        )
    finally:
        if cleanup:
            shutil.rmtree(project_dir, ignore_errors=True)


def execute_code_in_dir(code: str, project_dir: Path) -> ExecutionResult:
    """For check_solutions: reuse one project directory."""
    return execute_code(code, work_dir=project_dir)
