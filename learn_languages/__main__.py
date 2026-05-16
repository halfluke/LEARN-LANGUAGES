"""Entry point: LEARN-LANGUAGES hub menu."""

from __future__ import annotations

import sys

from learn_languages.app import LearnLanguagesMenu


def main() -> None:
    LearnLanguagesMenu().run()


if __name__ == "__main__":
    main()
