"""Compile and run learner Java (javac + java Main)."""

from __future__ import annotations

import os
import re
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


def resolve_javac() -> str:
    if shutil.which("javac"):
        return "javac"
    raise RuntimeError(
        "`javac` is not installed or not in PATH.\n\n"
        "Install a JDK (e.g. OpenJDK 17) and ensure `javac` and `java` work."
    )


def check_java_available() -> None:
    for cmd in ("javac", "java"):
        if not shutil.which(cmd):
            raise RuntimeError(f"`{cmd}` not found on PATH. Install a JDK.")
    try:
        p = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except OSError as e:
        raise RuntimeError(f"Could not run java: {e}") from e
    if p.returncode != 0 and not (p.stderr or p.stdout):
        raise RuntimeError("`java -version` failed.")


def _main_class_name(code: str) -> str:
    m = re.search(r"public\s+class\s+(\w+)", code)
    return m.group(1) if m else "Main"


def execute_code(code: str, *, work_dir: Path | None = None) -> ExecutionResult:
    """Write Main.java (or detected public class), javac, java."""
    cleanup = work_dir is None
    if work_dir is None:
        project_dir = Path(tempfile.mkdtemp(prefix="learn-java-run-"))
    else:
        project_dir = work_dir
        project_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    javac = resolve_javac()
    class_name = _main_class_name(code)
    src = project_dir / f"{class_name}.java"

    try:
        for old in project_dir.glob("*.class"):
            old.unlink(missing_ok=True)
        src.write_text(code, encoding="utf-8")

        comp = subprocess.run(
            [javac, str(src)],
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
                ["java", class_name],
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
