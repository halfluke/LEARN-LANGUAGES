"""External editor ($EDITOR) for solution.c buffer."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


def _which_available(name: str) -> bool:
    return shutil.which(name) is not None


def resolve_editor() -> str:
    ed = os.environ.get("EDITOR", "").strip()
    if ed:
        return ed
    for cand in ("vim", "nvim", "nano", "micro", "code", "subl"):
        if _which_available(cand):
            return cand
    raise RuntimeError(
        "No editor found. Set $EDITOR or install vim/nano/vscode (on PATH)."
    )


def launch_editor(initial_code: str) -> str:
    editor = resolve_editor()
    nanos = time.time_ns()
    tmp_dir = Path(tempfile.gettempdir()) / f"learn-c-editor-{nanos}"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    prog = tmp_dir / "solution.c"
    prog.write_text(initial_code, encoding="utf-8")
    r = subprocess.run(
        [editor, str(prog)],
        stdin=subprocess.DEVNULL,
    )
    if r.returncode != 0:
        raise RuntimeError("editor exited with a non-zero status")
    return prog.read_text(encoding="utf-8")
