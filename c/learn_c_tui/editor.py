"""External editor ($EDITOR) for solution.c buffer."""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


def _which_available(name: str) -> bool:
    return shutil.which(name) is not None


def resolve_editor_command() -> list[str]:
    """Return argv for the editor (respects EDITOR='vim -u NONE' or 'code --wait')."""
    ed = os.environ.get("EDITOR", "").strip()
    if ed:
        return shlex.split(ed)
    for cand in ("nano", "micro", "vim", "nvim", "code", "subl"):
        if _which_available(cand):
            return [cand]
    raise RuntimeError(
        "No editor found. Set $EDITOR (e.g. export EDITOR=nano) or install nano/vim on PATH."
    )


def launch_editor(initial_code: str, *, filename: str = "solution.c") -> str:
    cmd = resolve_editor_command()
    nanos = time.time_ns()
    tmp_dir = Path(tempfile.gettempdir()) / f"learn-c-editor-{nanos}"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    prog = tmp_dir / filename
    prog.write_text(initial_code, encoding="utf-8")
    # Inherit stdin/stdout/stderr so vim/nano get the real terminal (caller must suspend the TUI).
    r = subprocess.run(cmd + [str(prog)])
    if r.returncode != 0:
        raise RuntimeError("editor exited with a non-zero status")
    return prog.read_text(encoding="utf-8")
