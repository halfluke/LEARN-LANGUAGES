"""Entry point: prerequisite check + Textual app."""

from __future__ import annotations

import sys

from learn_java_tui.app import LearnJavaApp
from learn_java_tui.executor import check_java_available


def main() -> None:
    try:
        check_java_available()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1) from e
    LearnJavaApp().run()


if __name__ == "__main__":
    main()
