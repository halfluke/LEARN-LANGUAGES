"""Port C# top-level Program.cs exercise snippets to Python 3 / Java 17."""

from __future__ import annotations

import re


def _strip_usings(code: str) -> str:
    return "\n".join(
        ln for ln in code.splitlines() if not ln.strip().startswith("using ")
    ).strip()


def _split_statics(code: str) -> tuple[list[str], list[str]]:
    """Return static method lines and top-level statements."""
    lines = code.splitlines()
    statics: list[str] = []
    main: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        st = line.strip()
        if st.startswith("static "):
            block = [line]
            brace = line.count("{") - line.count("}")
            i += 1
            while i < len(lines) and brace > 0:
                block.append(lines[i])
                brace += lines[i].count("{") - lines[i].count("}")
                i += 1
            statics.append("\n".join(block))
            continue
        if st.startswith(("class ", "record ", "interface ", "struct ", "unsafe")):
            brace = line.count("{") - line.count("}")
            i += 1
            while i < len(lines) and brace > 0:
                brace += lines[i].count("{") - lines[i].count("}")
                i += 1
            continue
        if st:
            main.append(line)
        i += 1
    return statics, main


def _static_to_py(block: str) -> str:
    st = block.strip()
    m = re.match(r"static\s+void\s+(\w+)\s*\(([^)]*)\)\s*\{\s*(.*?)\s*\}\s*$", st, re.S)
    if m:
        name, args, body = m.groups()
        args = re.sub(r"\bstring\b|\bint\b|\bbool\b|\bdouble\b", "", args).replace("?", "").strip()
        body = _stmt_to_py(body.strip())
        return f"def {name}({args}):\n    {body}"
    m = re.match(r"static\s+(\w+\??)\s+(\w+)\s*\(([^)]*)\)\s*=>\s*(.+);", st)
    if m:
        _, name, args, body = m.groups()
        args = re.sub(r"\bstring\b|\bint\b|\bbool\b|\bdouble\b", "", args).replace("?", "").strip()
        return f"def {name}({args}):\n    return {_expr_to_py(body.strip())}"
    return f"# {st}"


def _expr_to_py(expr: str) -> str:
    e = expr
    e = re.sub(r"new\[\]\s*\{([^}]*)\}", r"[\1]", e)
    e = re.sub(r'\$"([^"]*)"', lambda m: 'f"' + m.group(1) + '"', e)
    e = e.replace("null", "None")
    e = re.sub(r"\btrue\b", "True", e)
    e = re.sub(r"\bfalse\b", "False", e)
    e = e.replace("?.", ".")
    e = e.replace(" is null", " is None")
    e = e.replace("Math.PI", "3.141592653589793")
    e = e.replace(".Sum()", "sum(nums)")
    e = e.replace('string.Join(" ", arr)', "' '.join(str(x) for x in arr)")
    e = re.sub(r"(\w+)\.Length\b", r"len(\1)", e)
    e = re.sub(r"(\w+)\+\+", r"\1 += 1", e)
    return e.rstrip(";")


def _stmt_to_py(stmt: str) -> str:
    s = stmt.strip().rstrip(";")
    if s.startswith("Console.WriteLine"):
        arg = s[s.index("(") + 1 : s.rindex(")")]
        return f"print({_expr_to_py(arg)})"
    if s.startswith("Console.Write"):
        arg = s[s.index("(") + 1 : s.rindex(")")]
        return f"print({_expr_to_py(arg)}, end='')"
    return _expr_to_py(s)


def _line_to_py(line: str) -> str:
    s = line.strip().rstrip(";")
    if not s or s.startswith("//"):
        return ""
    static = _static_to_py(s)
    if static.startswith("def "):
        return static
    m = re.match(r"var\s+(\w+)\s*=\s*(.+)", s)
    if m:
        return f"{m.group(1)} = {_expr_to_py(m.group(2))}"
    m = re.match(r"for\s*\(\s*var\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<=\s*(\d+)\s*;\s*\1\+\+\s*\)", s)
    if m:
        return f"for {m.group(1)} in range({m.group(2)}, {int(m.group(3)) + 1}):"
    m = re.match(r"foreach\s*\(\s*var\s+(\w+)\s+in\s+(\w+)\s*\)", s)
    if m:
        return f"for {m.group(1)} in {m.group(2)}:"
    m = re.match(r"foreach\s*\(\s*var\s+(\w+)\s+in\s+(\w+)\s*\)\s+(.+)", s)
    if m:
        return f"for {m.group(1)} in {m.group(2)}:\n    {_line_to_py(m.group(3))}"
    if s.startswith("if (") and ")" in s:
        cond, rest = s[3:].split(")", 1)
        rest = rest.strip()
        if rest:
            body = _line_to_py(rest) if not rest.startswith("Console") else _stmt_to_py(rest)
            return f"if {cond.strip()}:\n    {body}"
        return f"if {cond.strip()}:"
    if s.startswith("else "):
        rest = s[4:].strip()
        return f"else:\n    {_line_to_py(rest)}" if rest else "else:"
    if s.startswith("Console."):
        return _stmt_to_py(s)
    if s.startswith("try"):
        return s.replace("{", ":").replace("}", "")
    return _expr_to_py(s) if s else ""


def cs_to_python(code: str) -> str:
    code = _strip_usings(code)
    statics, main = _split_statics(code)
    out: list[str] = []
    for block in statics:
        conv = _static_to_py(block)
        if conv:
            out.append(conv)
    for line in main:
        conv = _line_to_py(line)
        if not conv:
            continue
        if "\n" in conv:
            out.extend(conv.splitlines())
        else:
            out.append(conv)
    body = "\n".join(out).strip()
    return body + "\n" if body else "# write your solution\n"


def _static_to_java(block: str) -> str:
    st = block.strip()
    m = re.match(r"static\s+void\s+(\w+)\s*\(([^)]*)\)\s*\{\s*(.*?)\s*\}\s*$", st, re.S)
    if m:
        name, args, body = m.groups()
        jbody = _stmt_to_java(body.strip())
        return f"    static void {name}({args}) {{ {jbody}; }}"
    m = re.match(r"static\s+(\w+\??)\s+(\w+)\s*\(([^)]*)\)\s*=>\s*(.+);", st)
    if m:
        ret, name, args, body = m.groups()
        jret = ret.replace("?", "").replace("int", "int").replace("string", "String")
        if "?" in ret:
            jret = "Integer" if "int" in ret else jret
        return f"    static {jret} {name}({args}) {{ return {body.rstrip(';')}; }}"
    return f"    // {st}"


def _stmt_to_java(stmt: str) -> str:
    s = stmt.strip().rstrip(";")
    if s.startswith("Console.WriteLine"):
        arg = s[s.index("(") + 1 : s.rindex(")")]
        return f"System.out.println({arg})"
    if s.startswith("Console.Write"):
        arg = s[s.index("(") + 1 : s.rindex(")")]
        return f"System.out.print({arg})"
    return s


def _line_to_java(line: str) -> str:
    s = line.strip().rstrip(";")
    if not s:
        return ""
    m = re.match(r"var\s+(\w+)\s*=\s*(.+)", s)
    if m:
        return f"{m.group(1)} = {_expr_to_py(m.group(2))}"
    m = re.match(r"for\s*\(\s*var\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<=\s*(\d+)\s*;\s*\1\+\+\s*\)", s)
    if m:
        return f"for (int {m.group(1)} = {m.group(2)}; {m.group(1)} <= {m.group(3)}; {m.group(1)}++)"
    m = re.match(r"foreach\s*\(\s*var\s+(\w+)\s+in\s+(\w+)\s*\)", s)
    if m:
        return f"for (int {m.group(1)} : {m.group(2)})"
    if s.startswith("if "):
        return s.replace("if (", "if (").replace(") ", ") ")
    if s.startswith("Console."):
        return _stmt_to_java(s)
    return s


def cs_to_java(code: str) -> str:
    code = _strip_usings(code)
    statics, main = _split_statics(code)
    parts = ["public class Main {"]
    for block in statics:
        parts.append(_static_to_java(block))
    parts.append("    public static void main(String[] args) {")
    for line in main:
        conv = _line_to_java(line)
        if conv:
            parts.append(f"        {conv};")
    parts.append("    }")
    parts.append("}")
    return "\n".join(parts) + "\n"
