"""Load LEARN-GO chapter exercise metadata."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GO_CHAPTERS = ROOT / "go" / "chapters"


@lru_cache(maxsize=32)
def go_chapter(chapter_id: str) -> dict:
    for path in sorted(GO_CHAPTERS.glob("*.json")):
        ch = json.loads(path.read_text(encoding="utf-8"))
        if ch.get("id") == chapter_id:
            return ch
    raise KeyError(f"no go chapter with id {chapter_id!r}")


def go_exercises(chapter_id: str) -> list[dict]:
    return list(go_chapter(chapter_id).get("exercises", []))
