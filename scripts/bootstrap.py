#!/usr/bin/env python3
"""Create root .venv and editable-install the hub + Python-based tracks.

Usage (from repository root):
  python3 scripts/bootstrap.py --learn    # runtime only (new learners)
  python3 scripts/bootstrap.py --dev      # runtime + pytest in each Python track

Why two modes?
  pip install -e .       — installs [project] dependencies (e.g. Textual). Enough to run TUIs.
  pip install -e ".[dev]" — also installs [project.optional-dependencies.dev] (e.g. pytest)
                            for running tests under each track; not required to learn.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV_DIR = ROOT / ".venv"
PYTHON_TRACKS = ("c", "csharp", "python", "java")


def _venv_python() -> Path:
    py = VENV_DIR / "bin" / "python"
    if not py.is_file():
        py = VENV_DIR / "Scripts" / "python.exe"
    return py


def _run(cmd: list[str], *, label: str) -> None:
    print(f"\n→ {label}")
    print("  ", " ".join(cmd))
    subprocess.run(cmd, cwd=str(ROOT), check=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--learn",
        action="store_true",
        help="editable install hub + tracks (runtime dependencies only)",
    )
    mode.add_argument(
        "--dev",
        action="store_true",
        help="editable install hub + tracks with [dev] extras (adds pytest for contributors)",
    )
    args = ap.parse_args()
    dev = args.dev

    if not (ROOT / "pyproject.toml").is_file():
        print("Run from LEARN-LANGUAGES repository root (missing pyproject.toml).", file=sys.stderr)
        return 1

    if not VENV_DIR.is_dir():
        _run([sys.executable, "-m", "venv", str(VENV_DIR)], label="create .venv")
    else:
        print("\n→ reusing existing .venv")

    py = _venv_python()
    if not py.is_file():
        print("Could not find python in .venv", file=sys.stderr)
        return 1

    _run([str(py), "-m", "pip", "install", "-U", "pip"], label="upgrade pip")

    suffix = "[dev]" if dev else ""
    _run([str(py), "-m", "pip", "install", "-e", str(ROOT)], label="install hub (learn_languages)")

    for track in PYTHON_TRACKS:
        spec = f"{ROOT / track}{suffix}"
        _run(
            [str(py), "-m", "pip", "install", "-e", spec],
            label=f"install {track}" + (" [dev]" if dev else ""),
        )

    print(
        """

Done.

  source .venv/bin/activate    # Windows: .venv\\Scripts\\activate
  learn-languages

Non-Python tracks still need their own toolchains (not installed by this script):
  Rust / asmx64 — cargo, rustc (see rust/README.md, asmx64/README.md)
  Go            — go on PATH (see go/README.md)
"""
    )
    if dev:
        print(
            "Dev mode: run tests per track, e.g.  cd python && python -m pytest tests/ -q\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
