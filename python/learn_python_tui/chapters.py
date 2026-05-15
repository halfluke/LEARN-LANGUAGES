"""Load chapter JSON (same schema as LEARN-RUST / TUTORIAL_PLATFORM)."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Exercise:
    id: str
    title: str
    description: str
    starter_code: str
    expected_output: str
    hints: list[str] = field(default_factory=list)
    solution: str = ""


@dataclass
class Chapter:
    id: str
    title: str
    description: str
    theory: str
    exercises: list[Exercise]
    exercise_count: int = 0


def default_chapters_dir() -> Path:
    env = os.environ.get("LEARN_PYTHON_CHAPTERS", "").strip()
    if env:
        return Path(env)
    root = Path(__file__).resolve().parent.parent
    dev = root / "chapters"
    if dev.is_dir() and any(dev.glob("*.json")):
        return dev
    cwd_ch = Path.cwd() / "chapters"
    if cwd_ch.is_dir() and any(cwd_ch.glob("*.json")):
        return cwd_ch
    return dev


def load_chapters(chapters_dir: Path | None = None) -> list[Chapter]:
    base = chapters_dir or default_chapters_dir()
    if not base.is_dir():
        raise FileNotFoundError(f"no chapters directory: {base}")
    paths = sorted(base.glob("*.json"))
    if not paths:
        raise ValueError(f"no chapter JSON files in {base}")
    out: list[Chapter] = []
    for path in paths:
        out.append(_load_one(path))
    return out


def _load_one(path: Path) -> Chapter:
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    cid = data.get("id") or ""
    if not cid:
        raise ValueError(f"{path}: missing id")
    title = data.get("title") or ""
    if not title:
        raise ValueError(f"{path}: missing title")
    desc = data.get("description") or ""
    if not desc:
        raise ValueError(f"{path}: missing description")
    raw_ex = data.get("exercises") or []
    if not raw_ex:
        raise ValueError(f"{path}: no exercises")
    exercises: list[Exercise] = []
    for i, ex in enumerate(raw_ex):
        eid = ex.get("id") or ""
        if not eid:
            raise ValueError(f"{path} exercise {i}: missing id")
        if not (ex.get("title") or "").strip():
            raise ValueError(f"{path} exercise {eid}: missing title")
        starter = ex.get("starter_code")
        if starter is None or not str(starter).strip():
            raise ValueError(f"{path} exercise {eid}: missing starter_code")
        eo = ex.get("expected_output")
        if eo is None:
            raise ValueError(f"{path} exercise {eid}: missing expected_output")
        exercises.append(
            Exercise(
                id=eid,
                title=ex.get("title", ""),
                description=ex.get("description", ""),
                starter_code=str(starter),
                expected_output=str(eo),
                hints=list(ex.get("hints") or []),
                solution=str(ex.get("solution") or ""),
            )
        )
    return Chapter(
        id=cid,
        title=title,
        description=desc,
        theory=data.get("theory") or "",
        exercises=exercises,
        exercise_count=int(data.get("exercise_count") or len(exercises)),
    )
