#!/usr/bin/env python3
"""One-shot generator for scripts/parity/_builders.py — run from repo root."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

OUT = Path(__file__).resolve().parent / "_builders.py"

ROOT = Path(__file__).resolve().parent.parent.parent
import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.parity.chapters._util import c_main, c_prog  # noqa: E402


def _legacy_c_prog(body: str, *headers: str) -> str:
    hs = headers or ("stdio.h",)
    inc = "\n".join(f"#include <{h}>" for h in hs)
    return f"{inc}\n\nint main(void) {{\n{body}\n    return 0;\n}}\n"


def emit(ch: str, eid: str, cs: dict, c: dict, store: dict) -> None:
    store.setdefault(ch, {})[eid] = {"csharp": cs, "c": c}


def main() -> None:
    b: dict = {}

    # ownership
    emit(
        "ownership",
        "ownership_01",
        {
            "starter_code": 'var s = "hi";\n// var t = s;\n// Console.Write(t);',
            "solution": 'var s = "hi";\nvar t = s;\nConsole.Write(t);',
            "hints": ["`string` assignment copies the reference; content is immutable."],
        },
        {
            "starter_code": c_prog('    const char *s = "hi";\n    // const char *t = s;\n    // printf("%s", t);'),
            "solution": c_prog('    const char *s = "hi";\n    const char *t = s;\n    printf("%s", t);'),
            "hints": ["Both pointers refer to the same string literal."],
        },
        b,
    )
    emit(
        "ownership",
        "ownership_02",
        {
            "starter_code": "var s = new[] { 1, 2 };\n// var t = s;\n// t[0] = 9;\n// Console.Write($\"{s[0]}{s[1]}\");",
            "solution": "var s = new[] { 1, 2 };\nvar t = s;\nt[0] = 9;\nConsole.Write($\"{s[0]}{s[1]}\");",
            "hints": ["Arrays are reference types."],
        },
        {
            "starter_code": c_prog("    int s[] = {1, 2};\n    int *t = s;\n    // t[0] = 9;\n    // printf(\"%d%d\", s[0], s[1]);"),
            "solution": c_prog("    int s[] = {1, 2};\n    int *t = s;\n    t[0] = 9;\n    printf(\"%d%d\", s[0], s[1]);"),
            "hints": ["`t` aliases the array."],
        },
        b,
    )
    emit(
        "ownership",
        "ownership_03",
        {
            "starter_code": "var a = 3;\n// var b = a;\n// b++;\n// Console.Write($\"{a} {b}\");",
            "solution": "var a = 3;\nvar b = a;\nb++;\nConsole.Write($\"{a} {b}\");",
            "hints": ["`int` copies by value."],
        },
        {
            "starter_code": c_prog("    int a = 3;\n    int b = a;\n    // b++;\n    // printf(\"%d %d\", a, b);"),
            "solution": c_prog("    int a = 3;\n    int b = a;\n    b++;\n    printf(\"%d %d\", a, b);"),
            "hints": ["Only `b` changes."],
        },
        b,
    )

    # controlflow
    cf = [
        (
            "controlflow_01",
            "var age = 20;\n// if (age >= 18) Console.WriteLine(\"Adult\"); else Console.WriteLine(\"Minor\");",
            "var age = 20;\nif (age >= 18) Console.WriteLine(\"Adult\");\nelse Console.WriteLine(\"Minor\");",
            c_prog("    int age = 20;\n    // if (age >= 18) puts(\"Adult\"); else puts(\"Minor\");", "stdio.h"),
            c_prog("    int age = 20;\n    if (age >= 18) puts(\"Adult\");\n    else puts(\"Minor\");", "stdio.h"),
        ),
        (
            "controlflow_02",
            "for (var i = 1; i <= 5; i++) { /* Console.WriteLine(i); */ }",
            "for (var i = 1; i <= 5; i++) Console.WriteLine(i);",
            c_prog("    // for (int i = 1; i <= 5; i++) printf(\"%d\\n\", i);"),
            c_prog("    for (int i = 1; i <= 5; i++) printf(\"%d\\n\", i);"),
        ),
        (
            "controlflow_03",
            "var day = 2;\n// switch (day) { ... }",
            "var day = 2;\nswitch (day)\n{\n    case 1: Console.WriteLine(\"Monday\"); break;\n    case 2: Console.WriteLine(\"Tuesday\"); break;\n    case 3: Console.WriteLine(\"Wednesday\"); break;\n    default: Console.WriteLine(\"Unknown\"); break;\n}",
            c_prog("    int day = 2;\n    // switch (day) ..."),
            c_prog(
                "    int day = 2;\n    switch (day) {\n    case 1: puts(\"Monday\"); break;\n    case 2: puts(\"Tuesday\"); break;\n    case 3: puts(\"Wednesday\"); break;\n    default: puts(\"Unknown\"); break;\n    }"
            ),
        ),
        (
            "controlflow_04",
            'var colors = new[] { "red", "green", "blue" };\n// foreach (var c in colors) Console.WriteLine(c);',
            'var colors = new[] { "red", "green", "blue" };\nforeach (var c in colors) Console.WriteLine(c);',
            c_prog('    const char *colors[] = {"red", "green", "blue"};\n    // for ...'),
            c_prog(
                '    const char *colors[] = {"red", "green", "blue"};\n    for (size_t i = 0; i < 3; i++) printf("%s\\n", colors[i]);',
                "stdio.h",
                "stddef.h",
            ),
        ),
        (
            "controlflow_05",
            "var score = 85;\n// chain if / else if for grade",
            "var score = 85;\nstring grade = score >= 90 ? \"A\" : score >= 80 ? \"B\" : score >= 70 ? \"C\" : score >= 60 ? \"D\" : \"F\";\nConsole.WriteLine(grade);",
            c_prog("    int score = 85;\n    // print grade"),
            c_prog(
                "    int score = 85;\n    if (score >= 90) puts(\"A\");\n    else if (score >= 80) puts(\"B\");\n    else if (score >= 70) puts(\"C\");\n    else if (score >= 60) puts(\"D\");\n    else puts(\"F\");"
            ),
        ),
        (
            "controlflow_07",
            "var i = 1;\n// while / for with break at 5",
            "for (var i = 1; ; i++)\n{\n    if (i >= 5) break;\n    Console.WriteLine(i);\n}",
            c_prog("    int i = 1;\n    for (;;) { /* break at 5 */ }"),
            c_prog(
                "    int i = 1;\n    for (;;) {\n        if (i >= 5) break;\n        printf(\"%d\\n\", i);\n        i++;\n    }"
            ),
        ),
        (
            "controlflow_06",
            "for (var i = 1; i <= 10; i++) { /* skip evens */ }",
            "for (var i = 1; i <= 10; i++)\n{\n    if (i % 2 == 0) continue;\n    Console.WriteLine(i);\n}",
            c_prog("    for (int i = 1; i <= 10; i++) { /* continue on even */ }"),
            c_prog(
                "    for (int i = 1; i <= 10; i++) {\n        if (i % 2 == 0) continue;\n        printf(\"%d\\n\", i);\n    }"
            ),
        ),
    ]
    for eid, cs_st, cs_sol, c_st, c_sol in cf:
        emit("controlflow", eid, {"starter_code": cs_st, "solution": cs_sol, "hints": []}, {"starter_code": c_st, "solution": c_sol, "hints": []}, b)

    # functions
    emit(
        "functions",
        "functions_01",
        {
            "starter_code": "static void Greet() { }\n\n// Greet();",
            "solution": "static void Greet() { Console.WriteLine(\"Hello\"); }\n\nGreet();",
            "hints": ["`static void Greet()` then call it."],
        },
        {
            "starter_code": "#include <stdio.h>\n\nstatic void greet(void) { }\n\nint main(void) {\n    // greet();\n    return 0;\n}\n",
            "solution": "#include <stdio.h>\n\nstatic void greet(void) { printf(\"Hello\\n\"); }\n\nint main(void) { greet(); return 0; }\n",
            "hints": ["Define `greet` before `main`."],
        },
        b,
    )
    emit(
        "functions",
        "functions_02",
        {
            "starter_code": 'static void Greet(string name) { }\n\n// Greet("Alice");',
            "solution": 'static void Greet(string name) { Console.WriteLine($"Hello, {name}"); }\n\nGreet("Alice");',
            "hints": [],
        },
        {
            "starter_code": '#include <stdio.h>\n\nstatic void greet(const char *name) { }\n\nint main(void) { return 0; }\n',
            "solution": '#include <stdio.h>\n\nstatic void greet(const char *name) { printf("Hello, %s\\n", name); }\n\nint main(void) { greet("Alice"); return 0; }\n',
            "hints": [],
        },
        b,
    )
    emit(
        "functions",
        "functions_03",
        {
            "starter_code": "static int Add(int a, int b) => 0;\n\n// Console.WriteLine(Add(3, 4));",
            "solution": "static int Add(int a, int b) => a + b;\n\nConsole.WriteLine(Add(3, 4));",
            "hints": [],
        },
        {
            "starter_code": c_main(
                '    // printf("%d\\n", add(3, 4));',
                "stdio.h",
                preamble="static int add(int a, int b) { return 0; }\n",
            ),
            "solution": c_main(
                '    printf("%d\\n", add(3, 4));',
                "stdio.h",
                preamble="static int add(int a, int b) { return a + b; }\n",
            ),
            "hints": [],
        },
        b,
    )
    emit(
        "functions",
        "functions_04",
        {
            "starter_code": "static int? Divide(int a, int b) => null;\n\n// print Divide(10,3) and nil for Divide(10,0)",
            "solution": dedent(
                """
                static int? Divide(int a, int b) => b == 0 ? null : a / b;

                var r = Divide(10, 3);
                var e = Divide(10, 0);
                Console.WriteLine($"{r} {(e is null ? "<nil>" : e.ToString())}");
                """
            ).strip(),
            "hints": ["Match Go's `fmt.Println(result, err)` with `<nil>` for null."],
        },
        {
            "starter_code": dedent(
                """
                #include <stdio.h>

                static int divide(int a, int b, int *ok) {
                    if (b == 0) { *ok = 0; return 0; }
                    *ok = 1; return a / b;
                }

                int main(void) {
                    return 0;
                }
                """
            ).strip(),
            "solution": dedent(
                """
                #include <stdio.h>

                static int divide(int a, int b, int *ok) {
                    if (b == 0) { *ok = 0; return 0; }
                    *ok = 1; return a / b;
                }

                int main(void) {
                    int ok;
                    int r = divide(10, 3, &ok);
                    printf("%d ", r);
                    divide(10, 0, &ok);
                    if (!ok) printf("<nil>");
                    return 0;
                }
                """
            ).strip(),
            "hints": [],
        },
        b,
    )
    emit(
        "functions",
        "functions_05",
        {
            "starter_code": "static int Sum(params int[] nums) => 0;\n\n// Console.WriteLine(Sum(1,2,3,4,5));",
            "solution": "using System.Linq;\n\nstatic int Sum(params int[] nums) => nums.Sum();\n\nConsole.WriteLine(Sum(1, 2, 3, 4, 5));",
            "hints": ["`params` accepts variable arguments."],
        },
        {
            "starter_code": c_main(
                "    // printf(\"%d\\n\", sum(nums, 5));",
                "stdio.h",
                preamble="static int sum(const int *nums, int n) { return 0; }\n",
            ),
            "solution": dedent(
                """
                #include <stdio.h>

                static int sum(const int *nums, int n) {
                    int t = 0;
                    for (int i = 0; i < n; i++) t += nums[i];
                    return t;
                }

                int main(void) {
                    int nums[] = {1, 2, 3, 4, 5};
                    printf("%d\\n", sum(nums, 5));
                    return 0;
                }
                """
            ).strip(),
            "hints": ["Pass pointer + length instead of variadic."],
        },
        b,
    )
    emit(
        "functions",
        "functions_07",
        {
            "starter_code": "static void Process() { /* start, working, defer end */ }\n\n// Process();",
            "solution": dedent(
                """
                static void Process()
                {
                    Console.WriteLine("start");
                    Console.WriteLine("working");
                }

                try { Process(); }
                finally { Console.WriteLine("end"); }
                """
            ).strip(),
            "hints": ["`try/finally` after `Process()` prints `end` when the try block completes."],
        },
        {
            "starter_code": c_main(
                "    // process();",
                "stdio.h",
                preamble="static void process(void) { /* start, working, end */ }\n",
            ),
            "solution": dedent(
                """
                #include <stdio.h>
                #include <stdlib.h>

                static void print_end(void) { printf("end\\n"); }

                static void process(void) {
                    printf("start\\n");
                    atexit(print_end);
                    printf("working\\n");
                }

                int main(void) { process(); return 0; }
                """
            ).strip(),
            "hints": ["`atexit` registers cleanup at process exit (differs from Go defer but models cleanup)."],
        },
        b,
    )
    emit(
        "functions",
        "functions_06",
        {
            "starter_code": "Func<int, int> makeAdder = () => 0;\n// Console.WriteLine(makeAdder()(5));",
            "solution": dedent(
                """
                int sum = 0;
                Func<int, int> makeAdder() => x => { sum += x; return sum; };
                var adder = makeAdder();
                Console.WriteLine(adder(5));
                Console.WriteLine(adder(10));
                """
            ).strip(),
            "hints": ["Capture `sum` in a closure."],
        },
        {
            "starter_code": c_prog("static int adder(int x) { return 0; }\n"),
            "solution": dedent(
                """
                #include <stdio.h>

                static int g_sum = 0;

                static int adder(int x) {
                    g_sum += x;
                    return g_sum;
                }

                int main(void) {
                    printf("%d\\n", adder(5));
                    printf("%d\\n", adder(10));
                    return 0;
                }
                """
            ).strip(),
            "hints": ["File-scope state models the closure capture."],
        },
        b,
    )

    lines = [
        '"""Auto-generated exercise bodies for C# and C (see generate_builders.py)."""',
        "from __future__ import annotations",
        "",
        "BODIES: dict[str, dict[str, dict[str, dict[str, str | list[str]]]]] = "
        + repr(b),
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} with chapters: {sorted(b)}")


if __name__ == "__main__":
    main()
