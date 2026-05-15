"""Port Go exercise solutions to Python 3 / Java 17 (main-package exercises)."""

from __future__ import annotations

import re
import textwrap


def _extract_package_funcs(go: str) -> str:
    """Return all top-level func bodies (helpers + main) as pseudo-main block."""
    lines = go.splitlines()
    chunks: list[str] = []
    i = 0
    while i < len(lines):
        st = lines[i].strip()
        if st.startswith("func ") and not st.startswith("func main"):
            depth = lines[i].count("{") - lines[i].count("}")
            block = [lines[i]]
            i += 1
            while i < len(lines) and depth > 0:
                depth += lines[i].count("{") - lines[i].count("}")
                block.append(lines[i])
                i += 1
            chunks.append("\n".join(block))
            continue
        if st.startswith("func main"):
            depth = lines[i].count("{") - lines[i].count("}")
            block = [lines[i]]
            i += 1
            while i < len(lines) and depth > 0:
                depth += lines[i].count("{") - lines[i].count("}")
                block.append(lines[i])
                i += 1
            chunks.append("\n".join(block))
            continue
        i += 1
    return "\n\n".join(chunks)


def _go_func_to_py_def(block: str) -> list[str]:
    header = block.splitlines()[0].strip()
    m = re.match(r"func\s+(\w+)\s*\(([^)]*)\)\s*(.*)\{", header)
    if not m:
        return []
    name, args, ret = m.groups()
    args = args.strip()
    py_args = []
    if args:
        for part in args.split(","):
            part = part.strip()
            if not part:
                continue
            if " " in part:
                py_args.append(part.rsplit(" ", 1)[0].strip())
            else:
                py_args.append(part)
    sig = f"def {name}({', '.join(py_args)}):"
    body_lines = block.splitlines()[1:]
    inner = _extract_main_block("func main() {\n" + "\n".join(body_lines) + "\n}")
    go_lines = inner.splitlines()
    base_indent = min((_leading_tabs(l) for l in go_lines if l.strip()), default=0)
    body: list[str] = []
    for line in go_lines:
        if not line.strip():
            continue
        rel = max(0, _leading_tabs(line) - base_indent)
        conv = _convert_line(line)
        if conv is None:
            continue
        body.append("    " * (rel // 4 + 1) + conv)
    out = [sig]
    for ln in body:
        out.append("    " + ln if ln.strip() else ln)
    return out


def _extract_main_block(go: str) -> str:
    lines = go.splitlines()
    out: list[str] = []
    depth = 0
    started = False
    for line in lines:
        st = line.strip()
        if re.match(r"func\s+main\s*\(", st):
            started = True
            depth = st.count("{") - st.count("}")
            continue
        if not started:
            continue
        depth += line.count("{") - line.count("}")
        if depth < 0:
            break
        if depth == 0 and st == "}":
            break
        out.append(line)
    return "\n".join(out)


def _leading_tabs(s: str) -> int:
    return len(s) - len(s.lstrip("\t "))


def _convert_line(line: str) -> str | None:
    raw = line.strip()
    if not raw or raw in ("{", "}"):
        return None
    if raw.startswith("//"):
        return None
    if raw == "}":
        return None
    if raw.startswith("} else {"):
        return "else:"

    # headers
    m = re.match(r"for\s+(\w+)\s*:=\s*(\d+)\s*;\s*\1\s*<=\s*(\d+)\s*;\s*\1\+\+", raw)
    if m:
        v, lo, hi = m.groups()
        return f"for {v} in range({lo}, {int(hi) + 1}):"
    m = re.match(r"for\s+(\w+),\s*(\w+)\s*:=\s*range\s+(\w+)", raw)
    if m:
        return f"for {m.group(2)} in {m.group(3)}:"
    m = re.match(r"for\s+(\w+)\s*:=\s*range\s+(\w+)", raw)
    if m:
        return f"for {m.group(1)} in {m.group(2)}:"
    if raw == "for {":
        return "while True:"

    m = re.match(r"if\s+(.+)\s*\{", raw)
    if m:
        return f"if {_expr(m.group(1))}:"
    m = re.match(r"\}\s*else\s+if\s+(.+)\s*\{", raw)
    if m:
        return f"elif {_expr(m.group(1))}:"
    m = re.match(r"switch\s+(\w+)\s*\{", raw)
    if m:
        return f"_sw = {m.group(1)}"
    m = re.match(r"case\s+(\d+):", raw)
    if m:
        return f"elif _sw == {m.group(1)}:"
    if raw == "default:":
        return "else:"

    if raw == "break":
        return "break"
    if raw == "continue":
        return "continue"
    if raw.startswith("defer "):
        inner = raw[6:].strip()
        if inner.startswith("fmt."):
            return f"# defer: {_fmt(inner)}"
        return f"# defer: {inner}"

    raw = re.sub(r"^(\w+)\s*:=\s*", r"\1 = ", raw)
    if raw.startswith("fmt."):
        return _fmt(raw)
    if raw.endswith("++"):
        return raw[:-2].strip() + " += 1"
    return _expr(raw)


def _expr(e: str) -> str:
    e = e.strip()
    e = re.sub(r"\[\]string\{([^}]*)\}", r"[\1]", e)
    e = re.sub(r"\[\]int\{([^}]*)\}", r"[\1]", e)
    e = re.sub(r"map\[string\]int\{", "{", e)
    e = re.sub(r"map\[string\]string\{", "{", e)
    e = re.sub(r"dict\{", "{", e)
    e = re.sub(r"make\(map\[string\]string\)", "{}", e)
    e = re.sub(r"make\(map\[string\]int\)", "{}", e)
    e = re.sub(r"\[(\d+)\]int", r"list", e)
    e = e.replace("&&", " and ").replace("||", " or ")
    e = e.replace("nil", "None")
    e = re.sub(r"\btrue\b", "True", e)
    e = re.sub(r"\bfalse\b", "False", e)
    e = re.sub(r"float64\(([^)]+)\)", r"float(\1)", e)
    e = re.sub(r"make\(\[\]int,\s*(\d+)\)", r"[0] * \1", e)
    e = re.sub(r"make\(\[\]int,\s*(\d+),\s*(\d+)\)", r"([0] * \1)", e)
    e = re.sub(r"append\(([^,]+),\s*([^)]+)\)", r"\1 + [\2]", e)
    e = re.sub(r"append\(([^,]+),\s*([^)]+)\.\.\.\)", r"\1 + list(\2)", e)
    e = re.sub(r"delete\((\w+),\s*\"([^\"]+)\"\)", r'del \1["\2"]', e)
    e = re.sub(r"delete\((\w+),\s*(\w+)\)", r"del \1[\2]", e)
    e = re.sub(r"(\w+),\s*(\w+)\s*=\s*(\w+),\s*(\w+)", r"\1, \2 = \3, \4", e)
    return e


def _fmt(line: str) -> str:
    m = re.match(r'fmt\.Printf\("([^"]*)"(.*)\)', line)
    if m:
        fmt, rest = m.groups()
        args = [a.strip() for a in rest.strip().lstrip(",").split(",") if a.strip()]
        if fmt == "%s" and len(args) == 1:
            return f"print({args[0]}, end='')"
        if fmt == "%d%d" and len(args) == 2:
            return f"print({args[0]}{args[1]}, end='')".replace("print(", "print(f'").replace(", end='')", "}{" + args[1] + "}', end='')")
        if args:
            return f"print({', '.join(args)})"
    m = re.match(r"fmt\.Println\((.*)\)", line)
    if m:
        return f"print({m.group(1)})"
    m = re.match(r"fmt\.Print\((.*)\)", line)
    if m:
        return f"print({m.group(1)}, end='')"
    return line


def _rewrite_switch(lines: list[str]) -> list[str]:
    """Turn switch/case blocks into if/elif/else on _sw."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "_sw = day" or re.match(r"_sw = \w+", ln.strip()):
            var = ln.strip().split("=", 1)[1].strip()
            out.append(ln)
            i += 1
            first = True
            while i < len(lines):
                st = lines[i].strip()
                if st.startswith("elif _sw =="):
                    case = st.split("==", 1)[1].strip().rstrip(":")
                    prefix = "if" if first else "elif"
                    out.append(f"{'    ' * (len(lines[i]) - len(lines[i].lstrip()))}{prefix} {var} == {case}:")
                    first = False
                    i += 1
                elif st == "else:":
                    out.append(lines[i])
                    i += 1
                else:
                    out.append(lines[i])
                    i += 1
                    if st.startswith("print("):
                        # next should be elif/else or done
                        if i < len(lines) and not lines[i].strip().startswith(("elif", "else")):
                            if not lines[i].strip().startswith("elif _sw"):
                                pass
                if i < len(lines) and lines[i].strip().startswith("_sw ="):
                    break
            continue
        out.append(ln)
        i += 1
    return out


def go_to_python(go_solution: str) -> str:
    helpers: list[str] = []
    full = _extract_package_funcs(go_solution)
    main_part = ""
    for chunk in re.split(r"\n(?=func )", full.strip()):
        chunk = chunk.strip()
        if not chunk:
            continue
        if chunk.startswith("func main"):
            main_part = chunk
        elif chunk.startswith("func "):
            helpers.extend(_go_func_to_py_def(chunk))

    block = _extract_main_block(main_part or go_solution)
    if not block.strip() and not helpers:
        return "# write your solution\n"

    go_lines = block.splitlines()
    base_indent = min((_leading_tabs(l) for l in go_lines if l.strip()), default=0)

    py_lines: list[str] = []
    for line in go_lines:
        if not line.strip():
            continue
        rel = max(0, _leading_tabs(line) - base_indent)
        conv = _convert_line(line)
        if conv is None:
            continue
        py_lines.append("    " * (rel // 4) + conv)

    py_lines = _rewrite_switch(py_lines)
    text = "\n".join(helpers + py_lines).strip()
    return text + "\n" if text else "# write your solution\n"


def go_to_java(go_solution: str) -> str:
    """Java port: use hand-maintained overrides in generate_native_bodies patches where needed."""
    block = _extract_main_block(go_solution)
    lines: list[str] = []
    for line in block.splitlines():
        raw = line.strip()
        if not raw or raw in ("{", "}") or raw.startswith("//"):
            continue
        raw = re.sub(r"^(\w+)\s*:=\s*", r"\1 = ", raw)
        m = re.match(r"for\s+(\w+)\s*:=\s*(\d+)\s*;\s*\1\s*<=\s*(\d+)\s*;\s*\1\+\+", raw)
        if m:
            v, lo, hi = m.groups()
            lines.append(f"for (int {v} = {lo}; {v} <= {hi}; {v}++) {{")
            continue
        m = re.match(r"if\s+(.+)\s*\{", raw)
        if m:
            lines.append(f"if ({m.group(1)}) {{")
            continue
        if raw.startswith("} else {"):
            lines.append("} else {")
            continue
        if raw.startswith("fmt.Println"):
            lines.append("System.out.println" + raw[11:])
            continue
        if raw.startswith("fmt.Print"):
            lines.append("System.out.print" + raw[9:])
            continue
        if raw.startswith("fmt.Printf"):
            lines.append("System.out.printf" + raw[10:])
            continue
        if not raw.endswith(";") and not raw.endswith("{"):
            raw += ";"
        lines.append(raw)

    body = "\n        ".join(lines)
    return (
        "public class Main {\n"
        "    public static void main(String[] args) {\n"
        f"        {body}\n"
        "    }\n}\n"
    )
