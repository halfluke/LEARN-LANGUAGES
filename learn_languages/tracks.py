"""Language track metadata and launch commands."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class Track:
    id: str
    title: str
    subtitle: str
    directory: str
    kind: Literal["cargo", "go", "python"]


TRACKS: tuple[Track, ...] = (
    Track("rust", "Rust", "cargo run", "rust", "cargo"),
    Track("go", "Go", "go run .", "go", "go"),
    Track("c", "C", "learn_c_tui", "c", "python"),
    Track("csharp", "C#", "learn_cs_tui", "csharp", "python"),
    Track("python", "Python", "learn_python_tui", "python", "python"),
    Track("java", "Java", "learn_java_tui", "java", "python"),
    Track("asmx64", "x86-64 asm", "cargo run (ELF64 / NASM)", "asmx64", "cargo"),
)

_PYTHON_MODULES = {
    "c": "learn_c_tui",
    "csharp": "learn_cs_tui",
    "python": "learn_python_tui",
    "java": "learn_java_tui",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _python_exe(track_dir: Path) -> Path:
    for rel in (".venv/bin/python", "venv/bin/python", ".venv/Scripts/python.exe"):
        candidate = track_dir / rel
        if candidate.is_file():
            return candidate
    return Path(sys.executable)


def launch_track(track: Track, *, root: Path | None = None) -> int:
    """Run a track TUI in the foreground; return its exit code (or 127 if missing)."""
    base = root or repo_root()
    track_dir = (base / track.directory).resolve()
    if not track_dir.is_dir():
        print(f"Missing track directory: {track_dir}", file=sys.stderr)
        return 1

    if track.kind == "cargo":
        cmd = ["cargo", "run", "--quiet"]
        if track.id == "asmx64":
            cmd = ["cargo", "run", "--release", "--quiet"]
        return subprocess.run(cmd, cwd=str(track_dir), env=os.environ.copy()).returncode

    if track.kind == "go":
        binary = track_dir / "learn-go-tui"
        if binary.is_file():
            return subprocess.run([str(binary)], cwd=str(track_dir), env=os.environ.copy()).returncode
        return subprocess.run(["go", "run", "."], cwd=str(track_dir), env=os.environ.copy()).returncode

    module = _PYTHON_MODULES[track.id]
    py = _python_exe(track_dir)
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(track_dir))
    return subprocess.run(
        [str(py), "-m", module],
        cwd=str(track_dir),
        env=env,
    ).returncode
