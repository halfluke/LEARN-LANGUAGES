"""Run learner C# in a temporary SDK-style console project (dotnet build + exec)."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import threading
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool


# First run may restore NuGet packages; keep generous bounds like LEARN-RUST cargo path.
BUILD_TIMEOUT = 180
RUN_TIMEOUT = 60

_BUILT_ONCE: set[str] = set()
_BUILT_ONCE_LOCK = threading.Lock()


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


def _dotnet_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("DOTNET_NOLOGO", "1")
    env.setdefault("DOTNET_SKIP_FIRST_TIME_EXPERIENCE", "1")
    env.setdefault("DOTNET_CLI_TELEMETRY_OPTOUT", "1")
    env.setdefault("TERM", env.get("TERM", "dumb"))
    return env


def _write_program_cs(project_dir: Path, code: str) -> None:
    (project_dir / "Program.cs").write_text(code, encoding="utf-8")


def _ensure_allow_unsafe(csproj: Path) -> None:
    text = csproj.read_text(encoding="utf-8")
    if "AllowUnsafeBlocks" not in text:
        text = text.replace(
            "</PropertyGroup>",
            "    <AllowUnsafeBlocks>true</AllowUnsafeBlocks>\n  </PropertyGroup>",
            1,
        )
        csproj.write_text(text, encoding="utf-8")


def ensure_console_project(project_dir: Path) -> Path:
    """Create a console SDK project in *project_dir* if missing; return the .csproj path."""
    project_dir.mkdir(parents=True, exist_ok=True)
    csproj = next(project_dir.glob("*.csproj"), None)
    if csproj is None:
        init = subprocess.run(
            ["dotnet", "new", "console", "--force", "--name", "Snippet", "-o", str(project_dir)],
            capture_output=True,
            text=True,
            timeout=BUILD_TIMEOUT,
            env=_dotnet_env(),
        )
        if init.returncode != 0:
            raise RuntimeError(init.stderr or init.stdout or "dotnet new failed")
        csproj = next(project_dir.glob("*.csproj"), None)
    if csproj is None:
        raise RuntimeError(f"no .csproj under {project_dir}")
    _ensure_allow_unsafe(csproj)
    return csproj


def _main_dll(project_dir: Path, csproj: Path) -> Path:
    pattern = f"bin/Debug/net*/{csproj.stem}.dll"
    matches = sorted(project_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(
            f"built assembly not found ({pattern}); run dotnet build first"
        )
    return matches[-1]


def _run_subprocess(
    cmd: list[str],
    *,
    cwd: Path,
    timeout: int,
) -> ExecutionResult:
    try:
        run = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(cwd),
            env=_dotnet_env(),
        )
    except subprocess.TimeoutExpired:
        return ExecutionResult(stdout="", stderr="", exit_code=-1, timed_out=True)
    return ExecutionResult(
        stdout=run.stdout or "",
        stderr=run.stderr or "",
        exit_code=run.returncode,
        timed_out=False,
    )


def build_project(project_dir: Path, *, csproj: Path | None = None) -> ExecutionResult:
    """Compile the project after Program.cs was updated."""
    proj = project_dir.resolve()
    csproj = (csproj or ensure_console_project(proj)).resolve()
    key = str(proj)
    with _BUILT_ONCE_LOCK:
        no_restore = key in _BUILT_ONCE
    cmd = ["dotnet", "build", str(csproj), "--verbosity", "quiet"]
    if no_restore:
        cmd.append("--no-restore")
    res = _run_subprocess(cmd, cwd=proj, timeout=BUILD_TIMEOUT)
    if res.exit_code == 0 and not res.timed_out:
        with _BUILT_ONCE_LOCK:
            _BUILT_ONCE.add(key)
    return res


def run_built_project(project_dir: Path, *, csproj: Path | None = None) -> ExecutionResult:
    """Run a built console app via ``dotnet exec`` on the output DLL."""
    proj = project_dir.resolve()
    csproj = (csproj or next(proj.glob("*.csproj"))).resolve()
    try:
        dll = _main_dll(proj, csproj)
    except FileNotFoundError as e:
        return ExecutionResult(stdout="", stderr=str(e), exit_code=1, timed_out=False)
    return _run_subprocess(
        ["dotnet", "exec", str(dll.resolve())],
        cwd=proj,
        timeout=RUN_TIMEOUT,
    )


def execute_code(
    code: str,
    *,
    work_dir: Path | None = None,
    incremental: bool = False,
) -> ExecutionResult:
    """Run *code* in a console project.

    When *incremental* is true and *work_dir* is set, reuse the project: write Program.cs,
    ``dotnet build`` (``--no-restore`` after the first successful build), then ``dotnet exec``.
    """
    cleanup = work_dir is None
    if work_dir is None:
        project_dir = Path(tempfile.mkdtemp(prefix="learn-csharp-run-"))
    else:
        project_dir = work_dir
        project_dir.mkdir(parents=True, exist_ok=True)

    try:
        proj = project_dir.resolve()
        try:
            csproj = ensure_console_project(proj)
        except RuntimeError as e:
            return ExecutionResult(stdout="", stderr=str(e), exit_code=1, timed_out=False)
        _write_program_cs(proj, code)

        if incremental and work_dir is not None:
            built = build_project(proj, csproj=csproj)
            if built.timed_out:
                return built
            if built.exit_code != 0:
                return built
            return run_built_project(proj, csproj=csproj)

        return _run_subprocess(
            [
                "dotnet",
                "run",
                "--project",
                str(csproj.resolve()),
                "--verbosity",
                "quiet",
            ],
            cwd=proj,
            timeout=BUILD_TIMEOUT,
        )
    finally:
        if cleanup:
            shutil.rmtree(project_dir, ignore_errors=True)


def execute_code_in_dir(code: str, project_dir: Path) -> ExecutionResult:
    """For check_solutions: reuse one project directory with incremental build+exec."""
    return execute_code(code, work_dir=project_dir, incremental=True)
