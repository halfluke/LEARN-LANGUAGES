"""Shared helpers for chapter body definitions."""

from __future__ import annotations


def c_prog(body: str, *headers: str) -> str:
    return c_main(body, *headers)


def c_main(body: str, *headers: str, preamble: str = "") -> str:
    hs = list(headers) if headers else []
    if "stdio.h" not in hs:
        hs.insert(0, "stdio.h")
    inc = "\n".join(f"#include <{h}>" for h in hs)
    pre = (preamble.rstrip() + "\n\n") if preamble else ""
    return f"{inc}\n\n{pre}int main(void) {{\n{body}\n    return 0;\n}}\n"


def cs_join_arr(nums: list[int]) -> str:
    return "[" + " ".join(str(n) for n in nums) + "]"
