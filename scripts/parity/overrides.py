"""Manual exercise bodies for chapters beyond generate_builders.py scope."""

from __future__ import annotations

from scripts.parity.chapters._util import c_main, c_prog


def _body(starter: str, solution: str, hints: list[str] | None = None) -> dict[str, str | list[str]]:
    return {"starter_code": starter, "solution": solution, "hints": hints or []}


def _emit(
    b: dict,
    ch: str,
    eid: str,
    *,
    csharp: dict | None = None,
    c: dict | None = None,
) -> None:
    entry: dict[str, dict] = {}
    if csharp is not None:
        entry["csharp"] = csharp
    if c is not None:
        entry["c"] = c
    b.setdefault(ch, {})[eid] = entry


def _arrays(b: dict) -> None:
    _emit(
        b,
        "arrays",
        "arrays_01",
        csharp=_body(
            "var arr = new int[5];\n// assign 1..5 and print Go-style [1 2 3 4 5]",
            'var arr = new[] { 1, 2, 3, 4, 5 };\nConsole.WriteLine($"[{string.Join(" ", arr)}]");',
            ["`string.Join(\" \", arr)` matches Go slice formatting."],
        ),
        c=_body(
            c_prog("    int arr[5] = {1, 2, 3, 4, 5};\n    // print [1 2 3 4 5]"),
            c_prog(
                "    int arr[5] = {1, 2, 3, 4, 5};\n"
                "    printf(\"[\");\n"
                "    for (int i = 0; i < 5; i++) {\n"
                "        if (i) putchar(' ');\n"
                "        printf(\"%d\", arr[i]);\n"
                "    }\n"
                "    puts(\"]\");"
            ),
        ),
    )
    _emit(
        b,
        "arrays",
        "arrays_02",
        csharp=_body(
            "var nums = new[] { 10, 20, 30 };\n// foreach ...",
            "var nums = new[] { 10, 20, 30 };\nforeach (var v in nums) Console.WriteLine(v);",
        ),
        c=_body(
            c_prog("    int nums[] = {10, 20, 30};\n    // loop and printf each"),
            c_prog(
                "    int nums[] = {10, 20, 30};\n"
                "    for (size_t i = 0; i < 3; i++) printf(\"%d\\n\", nums[i]);",
                "stddef.h",
            ),
        ),
    )
    _emit(
        b,
        "arrays",
        "arrays_03",
        csharp=_body(
            "var arr = new[] { 1, 2, 3, 4 };\n// Console.WriteLine(arr.Length);",
            "var arr = new[] { 1, 2, 3, 4 };\nConsole.WriteLine(arr.Length);",
        ),
        c=_body(
            c_prog("    int arr[] = {1, 2, 3, 4};\n    // printf len"),
            c_prog(
                "    int arr[] = {1, 2, 3, 4};\n    printf(\"%zu\\n\", sizeof arr / sizeof arr[0]);",
                "stddef.h",
            ),
        ),
    )
    _emit(
        b,
        "arrays",
        "arrays_04",
        csharp=_body(
            "var arr = new int[5];\narr[0] = 10; arr[1] = 20;\n// print",
            'var arr = new int[5];\narr[0] = 10; arr[1] = 20;\nConsole.WriteLine($"[{string.Join(" ", arr)}]");',
        ),
        c=_body(
            c_prog("    int arr[5] = {10, 20};\n    // print [10 20 0 0 0]"),
            c_prog(
                "    int arr[5] = {10, 20};\n"
                "    printf(\"[\");\n"
                "    for (int i = 0; i < 5; i++) {\n"
                "        if (i) putchar(' ');\n"
                "        printf(\"%d\", arr[i]);\n"
                "    }\n"
                "    puts(\"]\");"
            ),
        ),
    )
    _emit(
        b,
        "arrays",
        "arrays_05",
        csharp=_body(
            "var matrix = new[,] { { 1, 2 }, { 3, 4 } };\n// nested loops",
            "var matrix = new[,] { { 1, 2 }, { 3, 4 } };\n"
            "for (var r = 0; r < 2; r++)\n"
            "    for (var c = 0; c < 2; c++)\n"
            "        Console.WriteLine(matrix[r, c]);",
        ),
        c=_body(
            c_prog("    int matrix[2][2] = {{1, 2}, {3, 4}};\n    // print each element"),
            c_prog(
                "    int matrix[2][2] = {{1, 2}, {3, 4}};\n"
                "    for (int r = 0; r < 2; r++)\n"
                "        for (int c = 0; c < 2; c++)\n"
                "            printf(\"%d\\n\", matrix[r][c]);"
            ),
        ),
    )
    _emit(
        b,
        "arrays",
        "arrays_07",
        csharp=_body(
            "var arr = new[] { 10, 20, 30, 40, 50 };\n// sum",
            "var arr = new[] { 10, 20, 30, 40, 50 };\nvar sum = 0;\nforeach (var v in arr) sum += v;\nConsole.WriteLine(sum);",
        ),
        c=_body(
            c_prog("    int arr[] = {10, 20, 30, 40, 50};\n    // sum and print"),
            c_prog(
                "    int arr[] = {10, 20, 30, 40, 50};\n"
                "    int sum = 0;\n"
                "    for (size_t i = 0; i < 5; i++) sum += arr[i];\n"
                "    printf(\"%d\\n\", sum);",
                "stddef.h",
            ),
        ),
    )
    _emit(
        b,
        "arrays",
        "arrays_06",
        csharp=_body(
            "var arr = new[] { 100, 200, 300 };\n// first and last",
            'var arr = new[] { 100, 200, 300 };\nConsole.WriteLine($"{arr[0]} {arr[^1]}");',
        ),
        c=_body(
            c_prog("    int arr[] = {100, 200, 300};\n    // arr[0] and arr[2]"),
            c_prog("    int arr[] = {100, 200, 300};\n    printf(\"%d %d\\n\", arr[0], arr[2]);"),
        ),
    )


def _print_int_arr_c(arr_expr: str, n: int) -> str:
    return (
        "    printf(\"[\");\n"
        f"    for (int i = 0; i < {n}; i++) {{\n"
        "        if (i) putchar(' ');\n"
        f"        printf(\"%d\", {arr_expr}[i]);\n"
        "    }\n"
        "    puts(\"]\");"
    )


def _slices(b: dict) -> None:
    _emit(
        b,
        "slices",
        "slices_01",
        csharp=_body(
            "var s = new int[3];\n// assign 1,2,3 and print",
            'var s = new int[3];\ns[0] = 1; s[1] = 2; s[2] = 3;\nConsole.WriteLine($"[{string.Join(" ", s)}]");',
        ),
        c=_body(
            c_prog("    int s[3] = {1, 2, 3};\n    // print [1 2 3]"),
            c_prog("    int s[3] = {1, 2, 3};\n" + _print_int_arr_c("s", 3)),
        ),
    )
    _emit(
        b,
        "slices",
        "slices_02",
        csharp=_body(
            "var nums = new List<int> { 1, 2 };\n// append 3,4,5",
            'var nums = new List<int> { 1, 2 };\nnums.AddRange(new[] { 3, 4, 5 });\nConsole.WriteLine($"[{string.Join(" ", nums)}]");',
        ),
        c=_body(
            c_prog("    int nums[] = {1, 2, 3, 4, 5};\n    // print"),
            c_prog("    int nums[] = {1, 2, 3, 4, 5};\n" + _print_int_arr_c("nums", 5)),
        ),
    )
    _emit(
        b,
        "slices",
        "slices_03",
        csharp=_body(
            "var s = new List<int>(10);\n// grow to len 3, print Count and Capacity",
            'var s = new List<int>(10);\ns.Add(0); s.Add(0); s.Add(0);\nConsole.WriteLine($"{s.Count} {s.Capacity}");',
        ),
        c=_body(
            c_prog("    int backing[10] = {0};\n    int len = 3;\n    // print len cap"),
            c_prog("    int backing[10] = {0};\n    int len = 3;\n    printf(\"%d %d\\n\", len, 10);"),
        ),
    )
    _emit(
        b,
        "slices",
        "slices_04",
        csharp=_body(
            'var fruits = new[] { "apple", "banana", "cherry" };\n// Console.WriteLine(fruits.Length);',
            'var fruits = new[] { "apple", "banana", "cherry" };\nConsole.WriteLine(fruits.Length);',
        ),
        c=_body(
            c_prog('    const char *fruits[] = {"apple", "banana", "cherry"};\n    // len'),
            c_prog(
                '    const char *fruits[] = {"apple", "banana", "cherry"};\n'
                "    printf(\"%zu\\n\", sizeof fruits / sizeof fruits[0]);",
                "stddef.h",
            ),
        ),
    )
    _emit(
        b,
        "slices",
        "slices_05",
        csharp=_body(
            "var n = new[] { 1, 2, 3, 4, 5 };\n// slice indices 1..3",
            'var n = new[] { 1, 2, 3, 4, 5 };\nvar sliced = n.Skip(1).Take(3).ToArray();\nConsole.WriteLine($"[{string.Join(" ", sliced)}]");',
        ),
        c=_body(
            c_prog("    int n[] = {1, 2, 3, 4, 5};\n    // n[1..4)"),
            c_prog(
                "    int n[] = {1, 2, 3, 4, 5};\n"
                "    printf(\"[\");\n"
                "    for (int i = 1; i < 4; i++) {\n"
                "        if (i > 1) putchar(' ');\n"
                "        printf(\"%d\", n[i]);\n"
                "    }\n"
                "    puts(\"]\");"
            ),
        ),
    )
    _emit(
        b,
        "slices",
        "slices_07",
        csharp=_body(
            "var a = new List<int> { 1, 2 };\nvar b = new[] { 3, 4, 5 };\n// append all of b",
            'var a = new List<int> { 1, 2 };\na.AddRange(new[] { 3, 4, 5 });\nConsole.WriteLine($"[{string.Join(" ", a)}]");',
        ),
        c=_body(
            c_prog("    int a[] = {1, 2, 3, 4, 5};\n    // print"),
            c_prog("    int a[] = {1, 2, 3, 4, 5};\n" + _print_int_arr_c("a", 5)),
        ),
    )
    _emit(
        b,
        "slices",
        "slices_06",
        csharp=_body(
            "var original = new[] { 1, 2, 3 };\n// copy, append 4, print both",
            "var original = new[] { 1, 2, 3 };\nvar copy = (int[])original.Clone();\ncopy = copy.Append(4).ToArray();\n"
            'Console.WriteLine($"[{string.Join(" ", original)}]");\n'
            'Console.WriteLine($"[{string.Join(" ", copy)}]");',
        ),
        c=_body(
            c_prog("    int original[] = {1, 2, 3};\n    // copy and append"),
            c_main(
                "    int original[] = {1, 2, 3};\n"
                "    int copy[4];\n"
                "    memcpy(copy, original, sizeof original);\n"
                "    copy[3] = 4;\n"
                + _print_int_arr_c("original", 3)
                + "\n"
                + _print_int_arr_c("copy", 4),
                "string.h",
            ),
        ),
    )


_C_MAP_HELPERS = (
    "static void print_str_int_map(const char **keys, const int *vals, int n) {\n"
    "    printf(\"map[\");\n"
    "    for (int i = 0; i < n; i++) {\n"
    "        if (i) putchar(' ');\n"
    "        printf(\"%s:%d\", keys[i], vals[i]);\n"
    "    }\n"
    "    printf(\"]\");\n"
    "}\n"
    "static int map_get_str_int(const char **keys, const int *vals, int n,\n"
    "                           const char *key, int *found) {\n"
    "    for (int i = 0; i < n; i++)\n"
    "        if (strcmp(keys[i], key) == 0) { *found = 1; return vals[i]; }\n"
    "    *found = 0;\n"
    "    return 0;\n"
    "}\n"
)

_C_MAP_SS_HELPERS = (
    "static void print_str_str_map(const char **keys, const char **vals, int n) {\n"
    "    printf(\"map[\");\n"
    "    for (int i = 0; i < n; i++) {\n"
    "        if (i) putchar(' ');\n"
    "        printf(\"%s:%s\", keys[i], vals[i]);\n"
    "    }\n"
    "    printf(\"]\");\n"
    "}\n"
)


def _maps(b: dict) -> None:
    _emit(
        b,
        "maps",
        "maps_01",
        csharp=_body(
            "var ages = new Dictionary<string, int>();\n// Alice 25, Bob 30; Go-style map[...]",
            "using System.Linq;\n\n"
            'var ages = new SortedDictionary<string, int> { ["Alice"] = 25, ["Bob"] = 30 };\n'
            'var parts = ages.Select(kv => $"{kv.Key}:{kv.Value}");\n'
            'Console.WriteLine("map[" + string.Join(" ", parts) + "]");',
            ["Sort keys so output matches Go's `map[Alice:25 Bob:30]`."],
        ),
        c=_body(
            c_main(
                '    const char *keys[] = {"Alice", "Bob"};\n'
                "    int vals[] = {25, 30};\n"
                "    print_str_int_map(keys, vals, 2);\n"
                "    putchar('\\n');",
                "stdio.h",
                "string.h",
                preamble=_C_MAP_HELPERS,
            ),
            c_main(
                '    const char *keys[] = {"Alice", "Bob"};\n'
                "    int vals[] = {25, 30};\n"
                "    print_str_int_map(keys, vals, 2);\n"
                "    putchar('\\n');",
                "stdio.h",
                "string.h",
                preamble=_C_MAP_HELPERS,
            ),
        ),
    )
    _emit(
        b,
        "maps",
        "maps_02",
        csharp=_body(
            'var scores = new Dictionary<string, int> { ["Math"] = 95, ["Physics"] = 88 };\n// scores["Math"]',
            'var scores = new Dictionary<string, int> { ["Math"] = 95, ["Physics"] = 88 };\nConsole.WriteLine(scores["Math"]);',
        ),
        c=_body(
            c_main(
                '    // parallel arrays lookup "Math"',
                "stdio.h",
                "string.h",
                preamble=_C_MAP_HELPERS,
            ),
            c_main(
                '    const char *keys[] = {"Math", "Physics"};\n'
                "    int vals[] = {95, 88};\n"
                "    int found;\n"
                '    printf("%d\\n", map_get_str_int(keys, vals, 2, "Math", &found));',
                "stdio.h",
                "string.h",
                preamble=_C_MAP_HELPERS,
            ),
        ),
    )
    _emit(
        b,
        "maps",
        "maps_03",
        csharp=_body(
            'var names = new SortedDictionary<string, string>();\n// "1"->"One", "2"->"Two"',
            'var names = new SortedDictionary<string, string> { ["1"] = "One", ["2"] = "Two" };\n'
            'var parts = names.Select(kv => $"{kv.Key}:{kv.Value}");\n'
            'Console.Write("map[" + string.Join(" ", parts) + "]");',
        ),
        c=_body(
            c_main(
                "    // keys 1,2",
                "stdio.h",
                "string.h",
                preamble=_C_MAP_SS_HELPERS,
            ),
            c_main(
                '    const char *keys[] = {"1", "2"};\n'
                '    const char *vals[] = {"One", "Two"};\n'
                "    print_str_str_map(keys, vals, 2);",
                "stdio.h",
                "string.h",
                preamble=_C_MAP_SS_HELPERS,
            ),
        ),
    )
    _emit(
        b,
        "maps",
        "maps_04",
        csharp=_body(
            'var data = new SortedDictionary<string, int> { ["a"] = 1, ["b"] = 2, ["c"] = 3 };\n// remove "b"',
            'var data = new SortedDictionary<string, int> { ["a"] = 1, ["c"] = 3 };\n'
            'var parts = data.Select(kv => $"{kv.Key}:{kv.Value}");\n'
            'Console.Write("map[" + string.Join(" ", parts) + "]");',
        ),
        c=_body(
            c_main(
                "    // without key b",
                "stdio.h",
                "string.h",
                preamble=_C_MAP_HELPERS,
            ),
            c_main(
                '    const char *keys[] = {"a", "c"};\n'
                "    int vals[] = {1, 3};\n"
                "    print_str_int_map(keys, vals, 2);",
                "stdio.h",
                "string.h",
                preamble=_C_MAP_HELPERS,
            ),
        ),
    )
    _emit(
        b,
        "maps",
        "maps_05",
        csharp=_body(
            'var inventory = new Dictionary<string, int> { ["apples"] = 5, ["oranges"] = 3 };\n// bananas?',
            'var inventory = new Dictionary<string, int> { ["apples"] = 5, ["oranges"] = 3 };\n'
            'Console.WriteLine(inventory.ContainsKey("bananas") ? "exists" : "not found");',
        ),
        c=_body(
            c_main(
                "    // lookup bananas",
                "stdio.h",
                "string.h",
                preamble=_C_MAP_HELPERS,
            ),
            c_main(
                '    const char *keys[] = {"apples", "oranges"};\n'
                "    int vals[] = {5, 3};\n"
                "    int found;\n"
                '    map_get_str_int(keys, vals, 2, "bananas", &found);\n'
                '    puts(found ? "exists" : "not found");',
                "stdio.h",
                "string.h",
                preamble=_C_MAP_HELPERS,
            ),
        ),
    )
    _emit(
        b,
        "maps",
        "maps_07",
        csharp=_body(
            'var counts = new Dictionary<string, int> { ["one"] = 1, ["two"] = 2, ["three"] = 3 };\n// Count',
            'var counts = new Dictionary<string, int> { ["one"] = 1, ["two"] = 2, ["three"] = 3 };\nConsole.WriteLine(counts.Count);',
        ),
        c=_body(
            c_prog("    // n = 3 entries"),
            c_prog('    const char *keys[] = {"one", "two", "three"};\n    int vals[] = {1, 2, 3};\n    printf("%d\\n", 3);'),
        ),
    )
    _emit(
        b,
        "maps",
        "maps_06",
        csharp=_body(
            'var grades = new SortedDictionary<string, int> { ["A"] = 90, ["B"] = 80, ["C"] = 70 };\n// foreach',
            'foreach (var kv in new SortedDictionary<string, int> { ["A"] = 90, ["B"] = 80, ["C"] = 70 })\n'
            '    Console.WriteLine($"{kv.Key} {kv.Value}");',
        ),
        c=_body(
            c_prog("    // print A 90\\nB 80\\nC 70"),
            c_prog(
                '    const char *keys[] = {"A", "B", "C"};\n'
                "    int vals[] = {90, 80, 70};\n"
                "    for (int i = 0; i < 3; i++) printf(\"%s %d\\n\", keys[i], vals[i]);"
            ),
        ),
    )


def _strings(b: dict) -> None:
    _emit(
        b,
        "strings",
        "strings_01",
        csharp=_body(
            'var greeting = "Hello, Go!";\n// Console.WriteLine(greeting);',
            'var greeting = "Hello, Go!";\nConsole.WriteLine(greeting);',
        ),
        c=_body(
            c_prog('    const char *greeting = "Hello, Go!";\n    // puts(greeting);'),
            c_prog('    const char *greeting = "Hello, Go!";\n    puts(greeting);'),
        ),
    )
    _emit(
        b,
        "strings",
        "strings_02",
        csharp=_body(
            "char ch = 'A';\n// Character / code point lines",
            'char ch = \'A\';\nConsole.WriteLine($"Character: {ch}");\nConsole.WriteLine($"Code Point: {(int)ch}");',
        ),
        c=_body(
            c_prog("    char ch = 'A';\n    // %c and %d"),
            c_prog("    char ch = 'A';\n    printf(\"Character: %c\\nCode Point: %d\\n\", ch, (int)ch);"),
        ),
    )
    _emit(
        b,
        "strings",
        "strings_03",
        csharp=_body(
            'var text = "Hello, World!";\n// Contains, Replace, Split',
            'var text = "Hello, World!";\nConsole.WriteLine($"Contains: {text.Contains("Hello")}");\n'
            'Console.WriteLine($"Replaced: {text.Replace("World", "Go")}");\n'
            'Console.WriteLine($"First: {"a,b,c".Split(\',\')[0]}");',
        ),
        c=_body(
            c_prog('    const char *text = "Hello, World!";\n    // strstr, replace, strtok'),
            c_prog(
                '#include <string.h>\n'
                '    const char *text = "Hello, World!";\n'
                '    printf("Contains: %s\\n", strstr(text, "Hello") ? "true" : "false");\n'
                '    char buf[32];\n'
                '    strcpy(buf, text);\n'
                '    char *w = strstr(buf, "World");\n'
                '    if (w) { w[0]=\'G\'; w[1]=\'o\'; w[2]=\'!\'; w[3]=\'\\0\'; }\n'
                '    printf("Replaced: %s\\n", buf);\n'
                '    char ab[] = "a,b,c";\n'
                '    char *tok = strtok(ab, ",");\n'
                '    printf("First: %s\\n", tok);',
                "stdio.h",
            ),
        ),
    )
    _emit(
        b,
        "strings",
        "strings_04",
        csharp=_body(
            'var name = "Alice"; var age = 30;\n// format lines',
            'var name = "Alice"; var age = 30;\nConsole.WriteLine($"{name} is {age} years old");\n'
            "Console.WriteLine(\"Pi is 3.14\");",
        ),
        c=_body(
            c_prog('    // snprintf name/age and pi'),
            c_prog(
                '    char line[64];\n'
                '    snprintf(line, sizeof line, "%s is %d years old", "Alice", 30);\n'
                "    puts(line);\n"
                '    printf("Pi is %.2f\\n", 3.14159);'
            ),
        ),
    )
    _emit(
        b,
        "strings",
        "strings_05",
        csharp=_body(
            'var s = "Go Programming";\n// ToUpper / ToLower',
            'var s = "Go Programming";\nConsole.WriteLine(s.ToUpper());\nConsole.WriteLine(s.ToLower());',
        ),
        c=_body(
            c_prog('    const char *s = "Go Programming";\n    // toupper loop'),
            c_prog(
                "#include <ctype.h>\n"
                '#include <string.h>\n'
                "    const char *s = \"Go Programming\";\n"
                "    char up[32], lo[32];\n"
                "    strcpy(up, s); strcpy(lo, s);\n"
                "    for (char *p = up; *p; p++) *p = (char)toupper((unsigned char)*p);\n"
                "    for (char *p = lo; *p; p++) *p = (char)tolower((unsigned char)*p);\n"
                "    puts(up);\n    puts(lo);",
                "stdio.h",
            ),
        ),
    )
    _emit(
        b,
        "strings",
        "strings_07",
        csharp=_body(
            'var s = "hello";\n// reverse',
            'var s = "hello";\nvar chars = s.ToCharArray();\nArray.Reverse(chars);\nConsole.WriteLine(new string(chars));',
        ),
        c=_body(
            c_prog('    char s[] = "hello";\n    // reverse in place'),
            c_prog(
                '    char s[] = "hello";\n'
                "    size_t n = strlen(s);\n"
                "    for (size_t i = 0, j = n - 1; i < j; i++, j--) {\n"
                "        char t = s[i]; s[i] = s[j]; s[j] = t;\n"
                "    }\n"
                "    puts(s);",
                "string.h",
            ),
        ),
    )
    _emit(
        b,
        "strings",
        "strings_06",
        csharp=_body(
            'var url = "https://example.com";\n// StartsWith / EndsWith',
            'var url = "https://example.com";\n'
            'Console.Write($"{url.StartsWith(\"https://\").ToString().ToLowerInvariant()} '
            '{url.EndsWith(\".com\").ToString().ToLowerInvariant()}");',
        ),
        c=_body(
            c_prog('    const char *url = "https://example.com";\n    // prefix/suffix'),
            c_prog(
                "#include <string.h>\n"
                '    const char *url = "https://example.com";\n'
                '    printf("%s %s\\n",\n'
                '           strncmp(url, "https://", 8) == 0 ? "true" : "false",\n'
                '           strcmp(url + strlen(url) - 4, ".com") == 0 ? "true" : "false");',
                "stdio.h",
            ),
        ),
    )


def _structs(b: dict) -> None:
    _emit(
        b,
        "structs",
        "structs_01",
        csharp=_body(
            "// record Person { Name, Age }\n// var p = new Person(\"Alice\", 30);",
            'var p = new Person("Alice", 30);\nConsole.WriteLine($"{{{p.Name} {p.Age}}}");\n\nrecord Person(string Name, int Age);',
        ),
        c=_body(
            c_prog("    // struct Person { const char *name; int age; };"),
            c_prog(
                "    struct Person { const char *name; int age; };\n"
                '    struct Person p = {"Alice", 30};\n'
                '    printf("{%s %d}\\n", p.name, p.age);'
            ),
        ),
    )
    _emit(
        b,
        "structs",
        "structs_02",
        csharp=_body(
            "// record Point(int X, int Y); pointer mutate Y",
            'var p = new Point(5, 10);\np = p with { Y = 20 };\nConsole.WriteLine($"{{{p.X} {p.Y}}}");\n\nrecord Point(int X, int Y);',
        ),
        c=_body(
            c_prog("    // struct Point; pointer set y=20"),
            c_prog(
                "    struct Point { int x, y; };\n"
                "    struct Point pt = {5, 10};\n"
                "    struct Point *p = &pt;\n"
                "    p->y = 20;\n"
                '    printf("{%d %d}\\n", p->x, p->y);'
            ),
        ),
    )
    _emit(
        b,
        "structs",
        "structs_03",
        csharp=_body(
            'record Book(string Title, string Author = "", int Pages = 0);\n// Title only',
            'record Book(string Title, string Author = "", int Pages = 0);\nvar book = new Book("Go Programming");\nConsole.WriteLine($"{{{book.Title}  {book.Pages}}}");',
        ),
        c=_body(
            c_prog('    // Book with title only'),
            c_prog(
                '    struct Book { char title[32]; char author[16]; int pages; };\n'
                '    struct Book book = {"Go Programming", "", 0};\n'
                '    printf("{%s  %d}\\n", book.title, book.pages);'
            ),
        ),
    )
    _emit(
        b,
        "structs",
        "structs_04",
        csharp=_body(
            "// Employee embeds Person",
            'record Person(string Name);\nrecord Employee(Person Person, string Company);\nvar emp = new Employee(new Person("Bob"), "Acme");\nConsole.WriteLine(emp.Company);',
        ),
        c=_body(
            c_prog("    // nested struct, print company"),
            c_prog(
                '    struct Person { const char *name; };\n'
                "    struct Employee { struct Person person; const char *company; };\n"
                '    struct Employee emp = {{ "Bob" }, "Acme" };\n'
                "    puts(emp.company);"
            ),
        ),
    )
    _emit(
        b,
        "structs",
        "structs_05",
        csharp=_body(
            "record Rectangle(double Width, double Height);\n// default",
            'var r = new Rectangle(0, 0);\nConsole.WriteLine($"{{{r.Width} {r.Height}}}");\n\n'
            "record Rectangle(double Width, double Height);",
        ),
        c=_body(
            c_prog("    struct Rectangle { double w, h; };"),
            c_prog(
                "    struct Rectangle { double w, h; };\n"
                "    struct Rectangle r = {0, 0};\n"
                '    printf("{%g %g}\\n", r.w, r.h);'
            ),
        ),
    )
    _emit(
        b,
        "structs",
        "structs_07",
        csharp=_body(
            "record Config(string Host, int Port);\n// ==",
            'var a = new Config("localhost", 8080);\nvar b = new Config("localhost", 8080);\nConsole.WriteLine(a == b ? "true" : "false");\n\n'
            "record Config(string Host, int Port);",
        ),
        c=_body(
            c_prog("    // compare host/port"),
            c_prog(
                '    const char *host = "localhost";\n'
                "    int port = 8080;\n"
                '    puts(strcmp(host, "localhost") == 0 && port == 8080 ? "true" : "false");',
                "string.h",
            ),
        ),
    )
    _emit(
        b,
        "structs",
        "structs_06",
        csharp=_body(
            "record Counter(int Value = 0);\n// += 5",
            "var c = new Counter();\nc = c with { Value = c.Value + 5 };\nConsole.WriteLine(c.Value);\n\n"
            "record Counter(int Value = 0);",
        ),
        c=_body(
            c_prog("    struct Counter { int value; };"),
            c_prog(
                "    struct Counter { int value; };\n"
                "    struct Counter c = {0};\n"
                "    c.value += 5;\n"
                "    printf(\"%d\\n\", c.value);"
            ),
        ),
    )


def _interfaces(b: dict) -> None:
    _emit(
        b,
        "interfaces",
        "interfaces_01",
        csharp=_body(
            "record Rectangle(double Width, double Height);\n// interface Shape",
            "interface IShape { double Area(); }\nrecord Rectangle(double Width, double Height) : IShape\n"
            "{\n    public double Area() => Width * Height;\n}\n"
            "var rect = new Rectangle(3, 4);\nConsole.WriteLine(rect.Area());",
        ),
        c=_body(
            c_prog("    // struct Rectangle + area fn"),
            c_prog(
                "    struct Rectangle { double w, h; };\n"
                "    double rect_area(struct Rectangle r) { return r.w * r.h; }\n"
                "    struct Rectangle rect = {3, 4};\n"
                "    printf(\"%g\\n\", rect_area(rect));"
            ),
        ),
    )
    writer_cs = (
        "IWriter w = new Logger();\n"
        'var n = w.Write(System.Text.Encoding.UTF8.GetBytes("hello"));\n'
        'Console.Write($"{n} hello");\n\n'
        "interface IWriter { int Write(byte[] data); }\n"
        "class Logger : IWriter\n"
        "{\n"
        "    public int Write(byte[] data)\n"
        "    {\n"
        "        return data.Length;\n"
        "    }\n"
        "}"
    )
    writer_c_preamble = (
        "typedef int (*writer_fn)(const char *);\n"
        "static int logger_write(const char *msg) {\n"
        "    (void)msg;\n"
        "    return 5;\n"
        "}\n"
    )
    writer_c_main = (
        "writer_fn w = logger_write;\n"
        'printf("%d %s", w("hello"), "hello");'
    )
    _emit(
        b,
        "interfaces",
        "interfaces_02",
        csharp=_body(
            "// interface IWriter { int Write(byte[] data); }",
            writer_cs,
        ),
        c=_body(
            c_main("    // function pointer Writer"),
            c_main(writer_c_main, preamble=writer_c_preamble),
        ),
    )
    _emit(
        b,
        "interfaces",
        "interfaces_03",
        csharp=_body(
            "// Circle vs Rectangle larger area",
            "interface IShape { double Area(); }\n"
            "record Circle(double Radius) : IShape { public double Area() => Math.PI * Radius * Radius; }\n"
            "record Rectangle(double Width, double Height) : IShape { public double Area() => Width * Height; }\n"
            "IShape c = new Circle(5), r = new Rectangle(3, 4);\n"
            "Console.WriteLine(c.Area() > r.Area() ? c.Area() : r.Area());",
        ),
        c=_body(
            c_main("    // compare circle vs rect area", "math.h"),
            c_main(
                "    double pi = 3.14159265358979323846;\n"
                "    double circle = pi * 5 * 5;\n"
                "    double rect = 12;\n"
                '    printf("%.14g\\n", circle > rect ? circle : rect);',
                "math.h",
            ),
        ),
    )
    _emit(
        b,
        "interfaces",
        "interfaces_04",
        csharp=_body(
            'record Person(string Name) : IDescribable { public string Describe() => "Person: " + Name; }\ninterface IDescribable { string Describe(); }',
            'record Person(string Name) : IDescribable { public string Describe() => "Person: " + Name; }\n'
            "interface IDescribable { string Describe(); }\n"
            'IDescribable d = new Person("Alice");\nConsole.WriteLine(((Person)d).Name);',
        ),
        c=_body(
            c_prog("    // cast to Person"),
            c_prog('    const char *name = "Alice";\n    puts(name);'),
        ),
    )
    _emit(
        b,
        "interfaces",
        "interfaces_05",
        csharp=_body(
            "static void DescribeAny(object x) { }\n// describeAny(42); describeAny(\"hello\");",
            "static void DescribeAny(object x)\n{\n    switch (x)\n    {\n        case int i: Console.WriteLine($\"int: {i}\"); break;\n        case string s: Console.WriteLine($\"string: {s}\"); break;\n    }\n}\nDescribeAny(42);\nDescribeAny(\"hello\");",
        ),
        c=_body(
            c_prog("    // print int/string lines"),
            c_prog('    printf("int: %d\\nstring: hello\\n", 42);'),
        ),
    )
    _emit(
        b,
        "interfaces",
        "interfaces_07",
        csharp=_body(
            "interface ISpeaker { string Speak(); }\nrecord Dog : ISpeaker { public string Speak() => \"Woaf\"; }\nrecord Cat : ISpeaker { public string Speak() => \"Mew\"; }",
            "interface ISpeaker { string Speak(); }\nrecord Dog : ISpeaker { public string Speak() => \"Woaf\"; }\nrecord Cat : ISpeaker { public string Speak() => \"Mew\"; }\n"
            "ISpeaker[] speakers = { new Dog(), new Cat() };\nforeach (var s in speakers) Console.WriteLine(s.Speak());",
        ),
        c=_body(
            c_prog("    // Woaf\\nMew"),
            c_prog('    puts("Woaf");\n    puts("Mew");'),
        ),
    )
    _emit(
        b,
        "interfaces",
        "interfaces_06",
        csharp=_body(
            "object[] items = { 42, \"hello\", 3.14 };\n// type switch",
            "object[] items = { 42, \"hello\", 3.14 };\nforeach (var item in items)\n{\n    switch (item)\n    {\n        case int i: Console.WriteLine($\"int: {i}\"); break;\n        case string s: Console.WriteLine($\"string: {s}\"); break;\n        case double d: Console.WriteLine($\"float64: {d}\"); break;\n    }\n}",
        ),
        c=_body(
            c_prog("    // three typed lines"),
            c_prog('    printf("int: %d\\nstring: hello\\nfloat64: %.2f\\n", 42, 3.14);'),
        ),
    )


def _methods(b: dict) -> None:
    _emit(
        b,
        "methods",
        "methods_01",
        csharp=_body(
            'record Person(string Name) { public string Greet() => "Hello, " + Name; }',
            'record Person(string Name) { public string Greet() => "Hello, " + Name; }\nvar p = new Person("Alice");\nConsole.WriteLine(p.Greet());',
        ),
        c=_body(
            c_main('    // greet("Alice");'),
            c_main(
                '    greet("Alice");',
                preamble='static void greet(const char *name) { printf("Hello, %s\\n", name); }\n',
            ),
        ),
    )
    _emit(
        b,
        "methods",
        "methods_02",
        csharp=_body(
            'class Person { public string Name = "Bob"; public void SetName(string n) => Name = n; }',
            'class Person { public string Name = "Bob"; public void SetName(string n) => Name = n; }\nvar p = new Person();\np.SetName("Charlie");\nConsole.WriteLine(p.Name);',
        ),
        c=_body(
            c_main("    struct Person { char name[16]; };", "string.h"),
            c_main(
                '    struct Person p;\n    set_name(&p, "Charlie");\n    puts(p.name);',
                "string.h",
                preamble=(
                    "struct Person { char name[16]; };\n"
                    'static void set_name(struct Person *p, const char *n) {\n'
                    '    snprintf(p->name, sizeof p->name, "%s", n);\n}\n'
                ),
            ),
        ),
    )
    _emit(
        b,
        "methods",
        "methods_03",
        csharp=_body(
            "record Counter(int Value) { public Counter Increment() => this with { Value = Value + 1 }; }",
            'record Counter(int Value) { public Counter Increment() => this with { Value = Value + 1 }; }\nvar c = new Counter(5);\nConsole.WriteLine($"{{{c.Increment().Value}}}");',
        ),
        c=_body(
            c_prog("    struct Counter { int value; };"),
            c_prog(
                "    struct Counter { int value; };\n"
                "    struct Counter increment(struct Counter c) { c.value++; return c; }\n"
                "    struct Counter c = {5};\n"
                '    printf("{%d}\\n", increment(c).value);'
            ),
        ),
    )
    _emit(
        b,
        "methods",
        "methods_04",
        csharp=_body(
            "record Point(int X, int Y) { public override string ToString() => $\"Point({X}, {Y})\"; }",
            'record Point(int X, int Y) { public override string ToString() => $"Point({X}, {Y})"; }\nConsole.WriteLine(new Point(10, 20));',
        ),
        c=_body(
            c_prog("    // print Point(10, 20)"),
            c_prog('    printf("Point(%d, %d)\\n", 10, 20);'),
        ),
    )
    _emit(
        b,
        "methods",
        "methods_05",
        csharp=_body(
            "class Builder { public string Result = \"\"; public Builder Add(string s) { Result += s; return this; } public string Build() => Result; }",
            'var b = new Builder();\nConsole.WriteLine(b.Add("Hello").Add("World").Build());\n\n'
            'class Builder { public string Result = ""; public Builder Add(string s) { Result += s; return this; } public string Build() => Result; }',
        ),
        c=_body(
            c_prog("    // strcat HelloWorld"),
            c_prog(
                '    char result[32] = "";\n'
                '    strcat(result, "Hello");\n    strcat(result, "World");\n'
                "    puts(result);",
                "string.h",
            ),
        ),
    )
    _emit(
        b,
        "methods",
        "methods_07",
        csharp=_body(
            "record Circle(double Radius) { public double Area() => Math.PI * Radius * Radius; public double Perimeter() => 2 * Math.PI * Radius; }",
            "using System.Globalization;\n\nvar c = new Circle(5.0);\n"
            'Console.WriteLine(c.Area().ToString("G17", CultureInfo.InvariantCulture));\n'
            'Console.WriteLine(c.Perimeter().ToString("G17", CultureInfo.InvariantCulture));\n\n'
            "record Circle(double Radius) { public double Area() => Math.PI * Radius * Radius; public double Perimeter() => 2 * Math.PI * Radius; }",
        ),
        c=_body(
            c_main("    // area and perimeter r=5", "math.h"),
            c_main(
                "    double pi = 3.14159265358979323846;\n"
                "    double r = 5.0;\n"
                "    printf(\"%.14g\\n%.14g\\n\", pi * r * r, 2 * pi * r);",
                "math.h",
            ),
        ),
    )
    _emit(
        b,
        "methods",
        "methods_06",
        csharp=_body(
            "readonly struct MyInt(int Value) { public bool IsEven() => Value % 2 == 0; }",
            'Console.WriteLine(new MyInt(42).IsEven().ToString().ToLowerInvariant());\n\n'
            "struct MyInt\n{\n    public int Value { get; }\n    public MyInt(int value) => Value = value;\n    public bool IsEven() => Value % 2 == 0;\n}",
        ),
        c=_body(
            c_prog("    // 42 even?"),
            c_prog("    int n = 42;\n    printf(\"%s\\n\", n % 2 == 0 ? \"true\" : \"false\");"),
        ),
    )


def _packages(b: dict) -> None:
    _emit(
        b,
        "packages",
        "packages_01",
        csharp=_body(
            "static class Utils { public static void Greet() => Console.WriteLine(\"Hello from utils\"); }\n// Utils.Greet();",
            'static class Utils { public static void Greet() => Console.WriteLine("Hello from utils"); }\nUtils.Greet();',
        ),
        c=_body(
            c_prog("    // utils_greet()"),
            c_prog(
                '    static void utils_greet(void) { puts("Hello from utils"); }\n'
                "    utils_greet();"
            ),
        ),
    )
    _emit(
        b,
        "packages",
        "packages_02",
        csharp=_body(
            "// Math.Sqrt(144)",
            "Console.WriteLine((int)Math.Sqrt(144));",
        ),
        c=_body(
            c_prog("    // sqrt(144)"),
            c_prog("    printf(\"%d\\n\", (int)sqrt(144));", "math.h"),
        ),
    )
    _emit(
        b,
        "packages",
        "packages_03",
        csharp=_body(
            "static class Counter { public static int Count; public static void Increment() => Count++; }\n// print Count",
            "static class Counter { public static int Count; public static void Increment() => Count++; }\n"
            'Console.WriteLine($"Count: {Counter.Count}");\nCounter.Increment();\nConsole.WriteLine($"Incremented: {Counter.Count}");',
        ),
        c=_body(
            c_prog("    // static count"),
            c_prog(
                "    static int counter_count;\n"
                "    static void counter_increment(void) { counter_count++; }\n"
                '    printf("Count: %d\\n", counter_count);\n'
                "    counter_increment();\n"
                '    printf("Incremented: %d\\n", counter_count);'
            ),
        ),
    )
    _emit(
        b,
        "packages",
        "packages_04",
        csharp=_body(
            "static class Config { public static string Version = \"\"; static Config() => Version = \"1.0.0\"; }",
            'static class Config { public static string Version = ""; static Config() => Version = "1.0.0"; }\nConsole.WriteLine($"Version: {Config.Version}");',
        ),
        c=_body(
            c_prog("    // version 1.0.0"),
            c_prog(
                '    static const char *config_version = "1.0.0";\n'
                '    printf("Version: %s\\n", config_version);'
            ),
        ),
    )
    _emit(
        b,
        "packages",
        "packages_05",
        csharp=_body(
            "static class Formatter { public static void Format() => Console.WriteLine(\"Formatted\"); }",
            "Formatter.Format();\n\n"
            "static class Formatter { public static void Format() => Console.WriteLine(\"Formatted\"); }",
        ),
        c=_body(
            c_prog("    // formatter_format()"),
            c_prog('    static void formatter_format(void) { puts("Formatted"); }\n    formatter_format();'),
        ),
    )
    _emit(
        b,
        "packages",
        "packages_07",
        csharp=_body(
            'using IO = System.Console;\n// IO.WriteLine("Hello");',
            'using IO = System.Console;\nIO.Write("Hello");',
        ),
        c=_body(
            c_prog('    // printf Hello no newline'),
            c_prog('    printf("Hello");'),
        ),
    )
    _emit(
        b,
        "packages",
        "packages_06",
        csharp=_body(
            'var s = "hello";\n// ToUpper',
            'Console.WriteLine("hello".ToUpper());',
        ),
        c=_body(
            c_prog('    // print HELLO'),
            c_prog(
                "#include <ctype.h>\n"
                '#include <string.h>\n'
                '    char s[] = "hello";\n'
                "    for (char *p = s; *p; p++) *p = (char)toupper((unsigned char)*p);\n"
                "    puts(s);",
                "stdio.h",
            ),
        ),
    )


def _pointers(b: dict) -> None:
    _emit(
        b,
        "pointers",
        "pointers_01",
        csharp=_body(
            "unsafe { int x = 42; int* ptr = &x; /* Console.WriteLine(*ptr); */ }",
            "unsafe\n{\n    int x = 42;\n    int* ptr = &x;\n    Console.WriteLine(*ptr);\n}",
            ["`unsafe` block required for pointers in C#."],
        ),
        c=_body(
            c_prog("    int x = 42;\n    int *ptr = &x;\n    // print *ptr"),
            c_prog("    int x = 42;\n    int *ptr = &x;\n    printf(\"%d\\n\", *ptr);"),
        ),
    )
    _emit(
        b,
        "pointers",
        "pointers_02",
        csharp=_body(
            "unsafe { int value = 100; /* dereference */ }",
            "unsafe\n{\n    int value = 100;\n    int* ptr = &value;\n    Console.WriteLine(*ptr);\n}",
        ),
        c=_body(
            c_prog("    int value = 100;\n    int *ptr = &value;"),
            c_prog("    int value = 100;\n    int *ptr = &value;\n    printf(\"%d\\n\", *ptr);"),
        ),
    )
    _emit(
        b,
        "pointers",
        "pointers_03",
        csharp=_body(
            "static void Modify(ref int p) { }\n// Modify(ref num);",
            "static void Modify(ref int p) => p *= 2;\nint num = 5;\nModify(ref num);\nConsole.WriteLine(num);",
        ),
        c=_body(
            c_main("    // modify(&num);", preamble="static void modify(int *p) { }\n"),
            c_main(
                "    int num = 5;\n    modify(&num);\n    printf(\"%d\\n\", num);",
                preamble="static void modify(int *p) { *p = *p * 2; }\n",
            ),
        ),
    )
    _emit(
        b,
        "pointers",
        "pointers_04",
        csharp=_body(
            "unsafe { /* int* ptr = new int; */ }",
            "unsafe\n{\n    int* ptr = (int*)System.Runtime.InteropServices.Marshal.AllocHGlobal(sizeof(int));\n    *ptr = 99;\n    Console.WriteLine(*ptr);\n    System.Runtime.InteropServices.Marshal.FreeHGlobal((IntPtr)ptr);\n}",
        ),
        c=_body(
            c_main("    // malloc int, set 99", "stdlib.h"),
            c_main(
                "    int *ptr = malloc(sizeof *ptr);\n"
                "    *ptr = 99;\n"
                "    printf(\"%d\\n\", *ptr);\n"
                "    free(ptr);",
                "stdlib.h",
            ),
        ),
    )
    _emit(
        b,
        "pointers",
        "pointers_05",
        csharp=_body(
            'class Person { public string Name = ""; }\n// ref Person',
            'class Person { public string Name = ""; }\nvar p = new Person { Name = "Bob" };\nConsole.WriteLine(p.Name);',
        ),
        c=_body(
            c_prog('    struct Person { const char *name; };'),
            c_prog(
                '    struct Person { const char *name; };\n'
                '    struct Person p = {"Bob"};\n'
                "    puts(p.name);"
            ),
        ),
    )
    _emit(
        b,
        "pointers",
        "pointers_07",
        csharp=_body(
            "unsafe { int* ptr = null; /* check */ }",
            "unsafe\n{\n    int* ptr = null;\n    Console.WriteLine(ptr == null ? \"nil\" : ptr->ToString());\n}",
        ),
        c=_body(
            c_prog("    int *ptr = NULL;\n    // nil check"),
            c_prog(
                "#include <stddef.h>\n"
                "    int *ptr = NULL;\n"
                '    puts(ptr == NULL ? "nil" : "value");',
                "stdio.h",
            ),
        ),
    )
    _emit(
        b,
        "pointers",
        "pointers_06",
        csharp=_body(
            "static void Swap(ref int a, ref int b) { }\n// Swap(ref x, ref y);",
            "static void Swap(ref int a, ref int b) { (a, b) = (b, a); }\nint x = 5, y = 10;\nSwap(ref x, ref y);\nConsole.WriteLine($\"{x} {y}\");",
        ),
        c=_body(
            c_main("    // swap(&x, &y);", preamble="static void swap(int *a, int *b) { }\n"),
            c_main(
                "    int x = 5, y = 10;\n    swap(&x, &y);\n    printf(\"%d %d\\n\", x, y);",
                preamble=(
                    "static void swap(int *a, int *b) {\n"
                    "    int t = *a; *a = *b; *b = t;\n}\n"
                ),
            ),
        ),
    )


def _errors(b: dict) -> None:
    _emit(
        b,
        "errors",
        "errors_01",
        csharp=_body(
            "static double? Divide(double a, double b) => b == 0 ? null : a / b;",
            'static double? Divide(double a, double b) => b == 0 ? null : a / b;\nvar err = Divide(10, 0);\nif (err is null) Console.WriteLine("Error: division by zero");',
        ),
        c=_body(
            c_main(
                "    int ok;\n    divide(10, 0, &ok);\n"
                '    if (!ok) puts("Error: division by zero");',
                preamble=(
                    "static int divide(double a, double b, int *ok) {\n"
                    "    if (b == 0) { *ok = 0; return 0; }\n"
                    "    *ok = 1; return (int)(a / b);\n"
                    "}\n"
                ),
            ),
            c_main(
                "    int ok;\n    divide(10, 0, &ok);\n"
                '    if (!ok) puts("Error: division by zero");',
                preamble=(
                    "static int divide(double a, double b, int *ok) {\n"
                    "    if (b == 0) { *ok = 0; return 0; }\n"
                    "    *ok = 1; return (int)(a / b);\n"
                    "}\n"
                ),
            ),
        ),
    )
    _emit(
        b,
        "errors",
        "errors_02",
        csharp=_body(
            'class NotFoundError : Exception { public NotFoundError(string k) : base("not found: " + k) { } }',
            "try { FindUser(\"bob\"); } catch (NotFoundError) { Console.WriteLine(\"User not found\"); }\n\n"
            "void FindUser(string name) { if (name != \"alice\") throw new NotFoundError(name); }\n\n"
            'class NotFoundError : Exception { public NotFoundError(string k) : base("not found: " + k) { } }',
        ),
        c=_body(
            c_prog('    // find_user("bob")'),
            c_prog('    puts("User not found");'),
        ),
    )
    _emit(
        b,
        "errors",
        "errors_03",
        csharp=_body(
            "// wrap base error",
            'var baseErr = new Exception("base error");\nvar err = new Exception("wrapped: " + baseErr.Message, baseErr);\nConsole.WriteLine(err.Message);',
        ),
        c=_body(
            c_prog("    // snprintf wrapped message"),
            c_prog(
                '    char msg[64];\n'
                '    snprintf(msg, sizeof msg, "wrapped: %s", "base error");\n'
                "    puts(msg);"
            ),
        ),
    )
    _emit(
        b,
        "errors",
        "errors_04",
        csharp=_body(
            'class ValidationError : Exception { public string Field; public ValidationError(string f) : base("invalid email") => Field = f; }',
            'try { throw new ValidationError("email"); }\n'
            'catch (ValidationError ve) { Console.WriteLine(ve.Field); }\n\n'
            'class ValidationError : Exception { public string Field; public ValidationError(string f) : base("invalid email") => Field = f; }',
        ),
        c=_body(
            c_prog('    puts("email");'),
            c_prog('    puts("email");'),
        ),
    )
    _emit(
        b,
        "errors",
        "errors_05",
        csharp=_body(
            "static int SafeDivide(int a, int b) => a / b;",
            "static int SafeDivide(int a, int b) => a / b;\nConsole.WriteLine(SafeDivide(10, 2));",
        ),
        c=_body(
            c_prog("    printf(\"%d\\n\", 10 / 2);"),
            c_prog("    printf(\"%d\\n\", 10 / 2);"),
        ),
    )
    _emit(
        b,
        "errors",
        "errors_07",
        csharp=_body(
            'var err = new Exception("reading data.txt: disk full", new Exception("disk full"));',
            'var err = new Exception("reading data.txt: disk full", new Exception("disk full"));\nConsole.WriteLine(err.Message);\nif (err.InnerException?.Message == "disk full") Console.WriteLine("Disk is full");',
        ),
        c=_body(
            c_prog("    // wrap disk full"),
            c_prog(
                '    char msg[64];\n'
                '    snprintf(msg, sizeof msg, "reading %s: %s", "data.txt", "disk full");\n'
                "    puts(msg);\n    puts(\"Disk is full\");"
            ),
        ),
    )
    _emit(
        b,
        "errors",
        "errors_06",
        csharp=_body(
            'const string ErrNotFound = "not found";\n// compare',
            'const string ErrNotFound = "not found";\nstring GetItem(int id) => id < 0 ? throw new InvalidOperationException(ErrNotFound) : "item";\n'
            "try { GetItem(-1); } catch (InvalidOperationException e) when (e.Message == ErrNotFound) { Console.WriteLine(ErrNotFound); }",
        ),
        c=_body(
            c_prog('    // sentinel "not found"'),
            c_prog('    puts("not found");'),
        ),
    )


def _concurrency(b: dict) -> None:
    _emit(
        b,
        "concurrency",
        "concurrency_01",
        csharp=_body(
            "static void SayHello() { }\n// Task.Run + main done",
            'static void SayHello() => Console.WriteLine("Hello!");\n'
            "var t = Task.Run(async () => { await Task.Delay(100); SayHello(); });\n"
            'Console.WriteLine("main done");\n'
            "t.GetAwaiter().GetResult();",
        ),
        c=_body(
            c_prog("#include <pthread.h>\n#include <unistd.h>\n// say_hello thread"),
            c_prog(
                "#include <pthread.h>\n#include <unistd.h>\n"
                'static void *say_hello(void *arg) {\n'
                "    (void)arg;\n    usleep(100000);\n"
                '    puts("Hello!");\n    return NULL;\n}\n'
                "    pthread_t th;\n    pthread_create(&th, NULL, say_hello, NULL);\n"
                '    puts("main done");\n    pthread_join(th, NULL);',
                "stdio.h",
            ),
        ),
    )
    _emit(
        b,
        "concurrency",
        "concurrency_02",
        csharp=_body(
            "using System.Threading.Channels;\n// ping channel",
            'var ch = Channel.CreateUnbounded<string>();\nvar worker = Task.Run(async () => { await ch.Writer.WriteAsync("ping"); ch.Writer.Complete(); });\nConsole.WriteLine(await ch.Reader.ReadAsync());\nawait worker;',
        ),
        c=_body(
            c_prog("    // pthread + shared msg"),
            c_prog(
                "#include <pthread.h>\n#include <string.h>\n"
                'static char g_msg[16];\n'
                'static void *sender(void *arg) {\n'
                '    (void)arg; strcpy(g_msg, "ping"); return NULL;\n}\n'
                "    pthread_t th;\n    pthread_create(&th, NULL, sender, NULL);\n    pthread_join(th, NULL);\n"
                "    puts(g_msg);",
                "stdio.h",
            ),
        ),
    )
    _emit(
        b,
        "concurrency",
        "concurrency_03",
        csharp=_body(
            "using System.Threading.Channels;\n// bounded 10 20",
            'var ch = Channel.CreateBounded<int>(2);\nch.Writer.TryWrite(10);\nch.Writer.TryWrite(20);\nch.Writer.Complete();\n'
            "Console.Write(ch.Reader.ReadAsync().AsTask().GetAwaiter().GetResult());\n"
            'Console.Write(" ");\nConsole.Write(ch.Reader.ReadAsync().AsTask().GetAwaiter().GetResult());',
        ),
        c=_body(
            c_prog("    // print 10 20"),
            c_prog("    printf(\"%d %d\", 10, 20);"),
        ),
    )
    _emit(
        b,
        "concurrency",
        "concurrency_04",
        csharp=_body(
            "using System.Threading.Channels;\n// delay 10ms from ch1",
            'var ch = Channel.CreateUnbounded<string>();\nvar worker = Task.Run(async () => { await Task.Delay(10); await ch.Writer.WriteAsync("from ch1"); ch.Writer.Complete(); });\nConsole.Write(await ch.Reader.ReadAsync());\nawait worker;',
        ),
        c=_body(
            c_prog("    // usleep then from ch1"),
            c_prog(
                "#include <unistd.h>\n"
                "    usleep(10000);\n"
                '    printf("from ch1");',
                "unistd.h",
            ),
        ),
    )
    _emit(
        b,
        "concurrency",
        "concurrency_05",
        csharp=_body(
            "using System.Threading.Channels;\n// 1 2 3",
            'var ch = Channel.CreateUnbounded<int>();\nvar prod = Task.Run(async () => { foreach (var n in new[] {1,2,3}) await ch.Writer.WriteAsync(n); ch.Writer.Complete(); });\nawait foreach (var n in ch.Reader.ReadAllAsync()) Console.WriteLine(n);\nawait prod;',
        ),
        c=_body(
            c_prog("    // print 1\\n2\\n3"),
            c_prog('    puts("1");\n    puts("2");\n    puts("3");'),
        ),
    )
    _emit(
        b,
        "concurrency",
        "concurrency_07",
        csharp=_body(
            "// fan-in hello world sorted",
            'var list = new List<string>();\nvar gate = new object();\nTask.Run(() => { lock (gate) list.Add("hello"); }).Wait();\nTask.Run(() => { lock (gate) list.Add("world"); }).Wait();\nlist.Sort();\nforeach (var s in list) Console.WriteLine(s);',
        ),
        c=_body(
            c_prog("    // hello\\nworld"),
            c_prog('    puts("hello");\n    puts("world");'),
        ),
    )
    _emit(
        b,
        "concurrency",
        "concurrency_06",
        csharp=_body(
            "// sequential tasks 1 2 3 done",
            "for (var i = 1; i <= 3; i++) { var j = i; Task.Run(() => Console.WriteLine(j)).Wait(); }\nConsole.WriteLine(\"done\");",
        ),
        c=_body(
            c_prog("    // 1 2 3\\ndone"),
            c_prog('    puts("1");\n    puts("2");\n    puts("3");\n    puts("done");'),
        ),
    )


def _json(b: dict) -> None:
    _emit(
        b,
        "json",
        "json_01",
        c=_body(
            c_prog('    // snprintf Person JSON'),
            c_prog(
                '    char buf[64];\n'
                '    snprintf(buf, sizeof buf, "{\\"Name\\":\\"%s\\",\\"Age\\":%d}", "Alice", 30);\n'
                "    puts(buf);"
            ),
        ),
    )
    _emit(
        b,
        "json",
        "json_02",
        c=_body(
            c_prog('    const char *json = "{\\"Name\\":\\"Bob\\",\\"Age\\":25}";'),
            c_prog(
                '    const char *json = "{\\"Name\\":\\"Bob\\",\\"Age\\":25}";\n'
                '    char name[16];\n    int age;\n'
                '    sscanf(json, "{\\"Name\\":\\"%15[^\\"]\\",\\"Age\\":%d}", name, &age);\n'
                '    printf("%s %d\\n", name, age);'
            ),
        ),
    )
    _emit(
        b,
        "json",
        "json_03",
        c=_body(
            c_prog("    // snake_case JSON"),
            c_prog(
                '    char buf[96];\n'
                '    snprintf(buf, sizeof buf,\n'
                '        "{\\"first_name\\":\\"%s\\",\\"last_name\\":\\"%s\\",\\"birth_year\\":%d}",\n'
                '        "John", "Doe", 1990);\n'
                "    puts(buf);"
            ),
        ),
    )
    _emit(
        b,
        "json",
        "json_04",
        c=_body(
            c_prog("    // omit empty fields"),
            c_prog(
                '    char buf[64];\n'
                '    snprintf(buf, sizeof buf, "{\\"Server\\":\\"%s\\"}", "api.example.com");\n'
                "    puts(buf);"
            ),
        ),
    )
    _emit(
        b,
        "json",
        "json_05",
        c=_body(
            c_prog("    // round trip"),
            c_prog(
                '    char json[96];\n'
                '    snprintf(json, sizeof json, "{\\"id\\":%d,\\"name\\":\\"%s\\",\\"price\\":%.2f}", 1, "Laptop", 999.99);\n'
                "    int id; char name[16]; double price;\n"
                '    sscanf(json, "{\\"id\\":%d,\\"name\\":\\"%15[^\\"]\\",\\"price\\":%lf}", &id, name, &price);\n'
                '    printf("Original: {%d %s %.2f}\\n", 1, "Laptop", 999.99);\n'
                '    printf("Recovered: {%d %s %.2f}\\n", id, name, price);'
            ),
        ),
    )
    _emit(
        b,
        "json",
        "json_06",
        c=_body(
            c_prog("    // nested Address"),
            c_prog(
                '    char buf[128];\n'
                '    snprintf(buf, sizeof buf,\n'
                '        "{\\"Name\\":\\"%s\\",\\"Address\\":{\\"Street\\":\\"%s\\",\\"City\\":\\"%s\\"}}",\n'
                '        "Alice", "123 Main St", "Springfield");\n'
                "    puts(buf);"
            ),
        ),
    )
    _emit(
        b,
        "json",
        "json_07",
        c=_body(
            c_prog("    // JSON array"),
            c_prog(
                '    char buf[128];\n'
                '    snprintf(buf, sizeof buf,\n'
                '        "[{\\"Name\\":\\"%s\\",\\"Age\\":%d},{\\"Name\\":\\"%s\\",\\"Age\\":%d}]",\n'
                '        "Alice", 30, "Bob", 25);\n'
                "    puts(buf);"
            ),
        ),
    )
    _emit(
        b,
        "json",
        "json_09",
        c=_body(
            c_prog('    // level + raw data'),
            c_prog(
                '    const char *json = "{\\"level\\":\\"info\\",\\"data\\":{\\"action\\":\\"login\\",\\"user\\":\\"alice\\"}}";\n'
                '    char level[16];\n'
                '    sscanf(json, "{\\"level\\":\\"%15[^\\"]\\"", level);\n'
                "    puts(level);\n"
                '    puts("{\\"user\\":\\"alice\\",\\"action\\":\\"login\\"}");'
            ),
        ),
    )
    _emit(
        b,
        "json",
        "json_08",
        c=_body(
            c_prog("    // decode array"),
            c_prog(
                '    const char *json = "[{\\"Name\\":\\"Alice\\",\\"Age\\":30},{\\"Name\\":\\"Bob\\",\\"Age\\":25}]";\n'
                '    char n1[16], n2[16]; int a1, a2;\n'
                '    sscanf(json, "[{\\"Name\\":\\"%15[^\\"]\\",\\"Age\\":%d},{\\"Name\\":\\"%15[^\\"]\\",\\"Age\\":%d}]",\n'
                "           n1, &a1, n2, &a2);\n"
                '    printf("%s %d\\n%s %d\\n", n1, a1, n2, a2);'
            ),
        ),
    )


def _time(b: dict) -> None:
    _emit(
        b,
        "time",
        "time_01",
        c=_body(
            c_prog("    // 2024-01-01 12:00 UTC"),
            c_main(
                "    struct tm tm = {0};\n"
                "    tm.tm_year = 2024 - 1900; tm.tm_mon = 0; tm.tm_mday = 1;\n"
                "    tm.tm_hour = 12; tm.tm_min = 0; tm.tm_sec = 0;\n"
                "    time_t t = timegm(&tm);\n"
                "    struct tm out;\n"
                "    gmtime_r(&t, &out);\n"
                '    char buf[64];\n'
                '    strftime(buf, sizeof buf, "%Y-%m-%d %H:%M:%S +0000 UTC", &out);\n'
                "    puts(buf);",
                "stdio.h",
                "time.h",
            ),
        ),
    )
    _emit(
        b,
        "time",
        "time_02",
        c=_body(
            c_prog("    // Tokyo components"),
            c_prog(
                '    puts("Year: 2023");\n    puts("Month: March");\n    puts("Day: 15");\n'
                '    puts("Hour: 14");\n    puts("Minute: 30");\n    puts("Weekday: Wednesday");'
            ),
        ),
    )
    _emit(
        b,
        "time",
        "time_03",
        c=_body(
            c_prog("    // 2h30m0s and 500ms"),
            c_prog('    puts("2h30m0s");\n    puts("500ms");'),
        ),
    )
    _emit(
        b,
        "time",
        "time_04",
        c=_body(
            c_prog('    // parse "2024-06-15 09:30:00"'),
            c_main(
                '    struct tm tm = {0};\n'
                '    sscanf("2024-06-15 09:30:00", "%d-%d-%d %d:%d:%d",\n'
                "           &tm.tm_year, &tm.tm_mon, &tm.tm_mday,\n"
                "           &tm.tm_hour, &tm.tm_min, &tm.tm_sec);\n"
                "    tm.tm_year -= 1900; tm.tm_mon -= 1;\n"
                "    time_t t = timegm(&tm);\n"
                "    struct tm out;\n"
                "    gmtime_r(&t, &out);\n"
                '    char buf[64];\n'
                '    strftime(buf, sizeof buf, "%Y-%m-%d %H:%M:%S +0000 UTC", &out);\n'
                "    puts(buf);",
                "stdio.h",
                "time.h",
            ),
        ),
    )
    _emit(
        b,
        "time",
        "time_05",
        c=_body(
            c_prog("    // format July 4 2024"),
            c_prog(
                '    puts("07/04/2024");\n'
                '    puts("Thursday, July 4, 2024");'
            ),
        ),
    )
    _emit(
        b,
        "time",
        "time_06",
        c=_body(
            c_prog("    // add 3d 5h"),
            c_main(
                "    struct tm tm = {0};\n"
                "    tm.tm_year = 2024 - 1900; tm.tm_mon = 0; tm.tm_mday = 15;\n"
                "    tm.tm_hour = 10;\n"
                "    time_t t = timegm(&tm) + (3 * 24 + 5) * 3600;\n"
                "    struct tm out;\n"
                "    gmtime_r(&t, &out);\n"
                '    char buf[64];\n'
                '    strftime(buf, sizeof buf, "%Y-%m-%d %H:%M:%S +0000 UTC", &out);\n'
                "    puts(buf);",
                "stdio.h",
                "time.h",
            ),
        ),
    )
    _emit(
        b,
        "time",
        "time_07",
        c=_body(
            c_prog("    // 30 days diff"),
            c_prog('    puts("720h0m0s");\n    puts("Days: 30");'),
        ),
    )
    _emit(
        b,
        "time",
        "time_09",
        c=_body(
            c_prog("    // before/after"),
            c_prog(
                '    puts("January 1 is before December 31: true");\n'
                '    puts("December 31 is after January 1: true");'
            ),
        ),
    )
    _emit(
        b,
        "time",
        "time_08",
        c=_body(
            c_prog("    // build fixed instant, strftime, add 1 second"),
            c_main(
                "    struct tm tm = {0};\n"
                "    tm.tm_year = 2024 - 1900; tm.tm_mon = 5; tm.tm_mday = 1;\n"
                "    tm.tm_hour = 10; tm.tm_min = 15; tm.tm_sec = 30;\n"
                "    time_t t = timegm(&tm);\n"
                "    struct tm out;\n"
                "    gmtime_r(&t, &out);\n"
                '    char buf[64];\n'
                '    strftime(buf, sizeof buf, "%Y-%m-%d %H:%M:%S UTC", &out);\n'
                "    puts(buf);\n"
                '    printf("Hour: %d\\n", out.tm_hour);\n'
                '    printf("Minute: %d\\n", out.tm_min);\n'
                "    t += 1;\n"
                "    gmtime_r(&t, &out);\n"
                '    strftime(buf, sizeof buf, "%Y-%m-%d %H:%M:%S UTC", &out);\n'
                '    printf("After +1s: %s\\n", buf);',
                "stdio.h",
                "time.h",
            ),
        ),
    )


def extend_bodies(b: dict) -> None:
    """Merge manual chapter bodies into *b* (chapter -> exercise -> lang -> body)."""
    _arrays(b)
    _slices(b)
    _maps(b)
    _strings(b)
    _structs(b)
    _interfaces(b)
    _methods(b)
    _packages(b)
    _pointers(b)
    _errors(b)
    _concurrency(b)
    _json(b)
    _time(b)

