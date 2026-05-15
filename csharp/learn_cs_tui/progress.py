"""Progress store (~/.learn-csharp-tui/progress.json)."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class ProgressEntry:
    chapter_id: str
    exercise_id: str
    completed: bool
    attempts: int
    hints_used: int
    last_attempt: int


class ProgressStore:
    def __init__(self, file_path: Path | None = None) -> None:
        home = Path.home()
        store_dir = home / ".learn-csharp-tui"
        self._path = file_path or (store_dir / "progress.json")
        self._entries: list[ProgressEntry] = []

    def load(self) -> None:
        if not self._path.is_file():
            self._entries = []
            return
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        self._entries = [ProgressEntry(**row) for row in raw]

    def save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = [asdict(e) for e in self._entries]
        self._path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def save_progress(
        self,
        chapter_id: str,
        exercise_id: str,
        *,
        completed: bool,
        attempts: int,
        hints_used: int,
    ) -> None:
        now = int(time.time())
        for e in self._entries:
            if e.chapter_id == chapter_id and e.exercise_id == exercise_id:
                e.completed = completed or e.completed
                if attempts > 0:
                    e.attempts = attempts
                if hints_used > 0:
                    e.hints_used = hints_used
                e.last_attempt = now
                return
        self._entries.append(
            ProgressEntry(
                chapter_id=chapter_id,
                exercise_id=exercise_id,
                completed=completed,
                attempts=attempts,
                hints_used=hints_used,
                last_attempt=now,
            )
        )

    def completed_for_chapter(self, chapter_id: str) -> set[str]:
        return {e.exercise_id for e in self._entries if e.chapter_id == chapter_id and e.completed}

    def entries(self) -> list[ProgressEntry]:
        return list(self._entries)
