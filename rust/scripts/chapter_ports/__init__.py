"""Rust chapter builders keyed by LEARN-GO chapter id (see forge_chapters.py)."""

from __future__ import annotations

from . import (
    arrays,
    concurrency,
    controlflow,
    errors,
    functions,
    interfaces,
    json_chapter,
    maps,
    methods,
    packages,
    pointers,
    slices,
    strings,
    structs,
    testing,
    time_chapter,
    variables,
)

BUILDERS = {
    "variables": variables.build,
    "arrays": arrays.build,
    "slices": slices.build,
    "controlflow": controlflow.build,
    "functions": functions.build,
    "maps": maps.build,
    "structs": structs.build,
    "pointers": pointers.build,
    "methods": methods.build,
    "interfaces": interfaces.build,
    "packages": packages.build,
    "strings": strings.build,
    "errors": errors.build,
    "concurrency": concurrency.build,
    "testing": testing.build,
    "json": json_chapter.build,
    "time": time_chapter.build,
}

__all__ = ["BUILDERS"]
