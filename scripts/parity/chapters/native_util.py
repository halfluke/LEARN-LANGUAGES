"""Helpers for native Python/Java exercise bodies."""

from __future__ import annotations


def body(starter: str, solution: str, hints: list[str] | None = None) -> dict[str, str | list[str]]:
    return {"starter_code": starter, "solution": solution, "hints": hints or []}


def emit(
    b: dict,
    ch: str,
    eid: str,
    *,
    python: dict | None = None,
    java: dict | None = None,
) -> None:
    entry: dict[str, dict] = {}
    if python is not None:
        entry["python"] = python
    if java is not None:
        entry["java"] = java
    b.setdefault(ch, {})[eid] = entry
