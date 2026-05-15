"""Entry point: prerequisite check + Textual app."""

from __future__ import annotations

import sys

from learn_python_tui.app import LearnPythonApp
from learn_python_tui.executor import check_python_available


def main() -> None:
    try:
        check_python_available()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1) from e
    LearnPythonApp().run()


if __name__ == "__main__":
    main()
