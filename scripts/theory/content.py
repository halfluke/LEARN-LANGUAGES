"""Aggregated chapter theory payloads for apply_chapter_theory.py."""

from __future__ import annotations

from .asmx64 import THEORIES as ASMX64
from .c import THEORIES as C
from .csharp import THEORIES as CSHARP
from .go_expansions import THEORIES as GO_EXPANSIONS
from .java_track import THEORIES as JAVA
from .python_track import THEORIES as PYTHON
from .rust_expansions import THEORIES as RUST_EXPANSIONS

THEORY_BY_TRACK: dict[str, dict[str, str]] = {
    "c": C,
    "csharp": CSHARP,
    "python": PYTHON,
    "java": JAVA,
    "asmx64": ASMX64,
    "rust": RUST_EXPANSIONS,
    "go": GO_EXPANSIONS,
}
