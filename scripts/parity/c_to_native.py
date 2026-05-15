"""Port C exercise snippets to Python 3 / Java 17."""

from __future__ import annotations

import re


def _c_main_body(c_code: str) -> tuple[str, str]:
  """Return (preamble static funcs, main body)."""
  lines = c_code.splitlines()
  preamble: list[str] = []
  body: list[str] = []
  in_main = False
  depth = 0
  for line in lines:
    st = line.strip()
    if st.startswith("#include") or st.startswith("#"):
      continue
    if re.match(r"int\s+main\s*\(", st):
      in_main = True
      depth = line.count("{") - line.count("}")
      continue
    if not in_main:
      if st and not st.startswith("//"):
        preamble.append(line)
      continue
    depth += line.count("{") - line.count("}")
    if depth <= 0 and "}" in line:
      break
    body.append(line)
  return "\n".join(preamble).strip(), "\n".join(body).strip()


def c_to_python(c_code: str) -> str:
  pre, body = _c_main_body(c_code)
  out: list[str] = []
  if pre:
    for line in pre.splitlines():
      m = re.match(r"static\s+\w+\s+(\w+)\s*\(([^)]*)\)", line.strip())
      if m:
        name, args = m.groups()
        args = re.sub(r"\bint\b|\bconst\b|\bchar\s*\*", "", args).replace("*", "").strip()
        out.append(f"def {name}({args}):")
        out.append("    pass")
  for line in body.splitlines():
    s = line.strip()
    if not s or s in ("return 0;", "return 0"):
      continue
    s = re.sub(r'printf\("%s",\s*(\w+)\)', r"print(\1, end='')", s)
    s = re.sub(r'printf\("%s\\n",\s*(\w+)\)', r"print(\1)", s)
    s = re.sub(r'printf\("%d\\n",\s*(.+)\)', r"print(\1)", s)
    s = re.sub(r'printf\("%d %d\\n",\s*(.+)\)', r"print(\1)", s)
    s = re.sub(r'printf\("%d %d",\s*(.+)\)', r"print(\1, end='')", s)
    s = re.sub(r'puts\("([^"]*)"\)', r'print("\1")', s)
    s = re.sub(r"int\s+(\w+)\[\]\s*=\s*\{([^}]+)\}", r"\1 = [\2]", s)
    s = re.sub(r"int\s+(\w+)\s*=\s*([^;]+);", r"\1 = \2", s)
    s = s.replace("NULL", "None").replace("nullptr", "None")
    out.append(s)
  text = "\n".join(out).strip()
  return text + "\n" if text else "# write your solution\n"


def c_to_java(c_code: str) -> str:
  pre, body = _c_main_body(c_code)
  statics: list[str] = []
  for line in pre.splitlines():
    st = line.strip()
    if st.startswith("static"):
      statics.append("    " + st.replace("const char *", "String ").replace("int ", "int "))
  main: list[str] = []
  for line in body.splitlines():
    s = line.strip()
    if not s or s == "return 0;":
      continue
    s = s.replace("printf", "System.out.printf").replace("puts", "System.out.println")
    s = re.sub(r"int\s+(\w+)\[\]\s*=\s*\{([^}]+)\}", r"int[] \1 = {\2}", s)
    main.append("        " + s)
  parts = ["public class Main {"]
  parts.extend(statics)
  parts.append("    public static void main(String[] args) {")
  parts.extend(main or ["        // TODO"])
  parts.append("    }")
  parts.append("}")
  return "\n".join(parts) + "\n"
