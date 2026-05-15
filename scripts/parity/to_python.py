"""Convert C#-style exercise snippets to idiomatic Python 3 (single script)."""

from __future__ import annotations

import re


def _strip_usings(code: str) -> str:
    lines = []
    for line in code.splitlines():
        if line.strip().startswith("using "):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def _remove_type_blocks(code: str) -> str:
    """Drop C# class/record/interface bodies; keep top-level script logic."""
    lines = code.splitlines()
    out: list[str] = []
    skip = 0
    for line in lines:
        st = line.strip()
        if skip > 0:
            skip += line.count("{") - line.count("}")
            if skip <= 0:
                skip = 0
            continue
        if re.match(r"^(class|record|interface|struct|unsafe)\b", st):
            skip = line.count("{") - line.count("}") or 1
            continue
        out.append(line)
    return "\n".join(out)


def _convert_static_method(line: str) -> str | None:
    m = re.match(
        r"static\s+(\w+\??)\s+(\w+)\s*\(([^)]*)\)\s*=>\s*(.+);?\s*$",
        line.strip(),
    )
    if m:
        ret, name, args, body = m.groups()
        py_args = re.sub(r"\bint\b|\bstring\b|\bbool\b|\bdouble\b", "", args)
        py_args = py_args.replace("?", "").strip()
        body = body.strip().rstrip(";")
        if body.startswith("{"):
            return None
        return f"def {name}({py_args}):\n    return {body}"
    m = re.match(r"static\s+void\s+(\w+)\s*\(([^)]*)\)\s*\{\s*\}\s*$", line.strip())
    if m:
        name, args = m.groups()
        py_args = re.sub(r"\bstring\b", "", args).strip()
        return f"def {name}({py_args}):\n    pass"
    return None


def _convert_line(line: str) -> str:
    s = line.rstrip()
    if not s.strip():
        return ""
    st = s.strip()
    static_def = _convert_static_method(st)
    if static_def:
        return static_def

    s = re.sub(r'\$"([^"]*)"', r'f"\1"', s)
    s = s.replace("Console.WriteLine", "print")
    s = re.sub(r"Console\.Write\((.*)\)\s*;?\s*$", r"print(\1, end='')", s)
    s = re.sub(r"\bvar\s+", "", s)
    s = s.replace("new[] {", "[").replace("};", "]")
    s = s.replace("null", "None")
    s = re.sub(r"\btrue\b", "True", s)
    s = re.sub(r"\bfalse\b", "False", s)
    s = s.replace("?.", ".")
    s = s.replace(" is null", " is None")
    s = s.replace(" is not null", " is not None")
    s = re.sub(r"for\s*\(\s*var\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<=\s*(\d+)\s*;\s*\1\+\+\s*\)", r"for \1 in range(\2, \3 + 1)", s)
    s = re.sub(r"for\s*\(\s*var\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<=\s*(\d+)\s*;\s*\1\+\+\s*\)", r"for \1 in range(\2, \3 + 1)", s)
    s = re.sub(
        r"foreach\s*\(\s*var\s+(\w+)\s+in\s+(\w+)\s*\)",
        r"for \1 in \2",
        s,
    )
    s = re.sub(r"(\w+)\+\+", r"\1 += 1", s)
    s = s.rstrip(";")
    if " ? " in s and ":" in s and "if " not in s:
        # ternary -> keep as python conditional expression
        s = re.sub(
            r"(\w+)\s*=\s*(.+)\s*\?\s*\"([^\"]*)\"\s*:\s*(.+);?",
            r'\1 = "\3" if \2 else \4',
            s,
        )
    return s


def csharp_to_python(code: str) -> str:
    code = _strip_usings(code)
    code = _remove_type_blocks(code)
    if not code.strip():
        return "# write your solution\n"
    out: list[str] = []
    for line in code.splitlines():
        conv = _convert_line(line)
        if conv:
            if "\n" in conv:
                out.extend(conv.splitlines())
            else:
                out.append(conv)
    body = "\n".join(out).strip()
    body = body.replace("b++", "b += 1")
    body = body.replace("print(f", "print(f")
    return body + ("\n" if body else "")
