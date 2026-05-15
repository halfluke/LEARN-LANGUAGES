"""Convert C#-style exercise snippets to Java 17 single-file Main."""

from __future__ import annotations

import re

from scripts.parity.to_python import _remove_type_blocks, _strip_usings


def _convert_static_line(line: str) -> str | None:
    st = line.strip()
    m = re.match(r"static\s+(\w+\??)\s+(\w+)\s*\(([^)]*)\)\s*=>\s*(.+);?\s*$", st)
    if m:
        ret, name, args, body = m.groups()
        jret = ret.replace("?", "").replace("int", "int").replace("string", "String")
        if "?" in ret:
            jret = "Integer" if "int" in ret else "Double" if "double" in ret else jret
        return f"    static {jret} {name}({args}) {{ return {body.rstrip(';')}; }}"
    m = re.match(r"static\s+void\s+(\w+)\s*\(([^)]*)\)\s*\{\s*\}\s*$", st)
    if m:
        return f"    static void {m.group(1)}({m.group(2)}) {{ }}"
    return None


def _convert_main_line(line: str) -> str:
    s = line.rstrip()
    st = s.strip()
    static = _convert_static_line(st)
    if static:
        return static
    s = re.sub(r'\$"([^"]*)"', r'"\1"', s)
    # restore interpolated holes
    s = re.sub(r"\{(\w+)\}", r'" + \1 + "', s)
    s = s.replace("Console.WriteLine", "System.out.println")
    s = re.sub(r"Console\.Write\((.*)\)", r"System.out.print(\1)", s)
    s = re.sub(r"\bvar\s+", "", s)
    s = s.replace("new[] {", "new int[] {")
    s = s.replace("null", "null")
    s = re.sub(r"foreach\s*\(\s*var\s+(\w+)\s+in\s+(\w+)\s*\)", r"for (String \1 : \2)", s)
    s = re.sub(
        r"for\s*\(\s*var\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<=\s*(\d+)\s*;\s*\1\+\+\s*\)",
        r"for (int \1 = \2; \1 <= \3; \1++)",
        s,
    )
    if not st.startswith("static") and st and not st.startswith("//"):
        s = "        " + s.strip()
    return s.rstrip(";")


def csharp_to_java(code: str, *, wrap: bool = True) -> str:
    code = _strip_usings(code)
    code = _remove_type_blocks(code)
    if not code.strip():
        return (
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        // write your solution\n"
            "    }\n"
            "}\n"
        )
    statics: list[str] = []
    main: list[str] = []
    for line in code.splitlines():
        st = line.strip()
        if not st:
            continue
        if st.startswith("static "):
            conv = _convert_static_line(st)
            if conv:
                statics.append(conv)
            continue
        conv = _convert_main_line(line)
        if conv.strip():
            main.append(conv if conv.startswith("        ") else "        " + conv.strip())

    parts = ["public class Main {"]
    if statics:
        parts.extend(statics)
    parts.append("    public static void main(String[] args) {")
    parts.extend(main or ["        // TODO"])
    parts.append("    }")
    parts.append("}")
    return "\n".join(parts) + "\n"
