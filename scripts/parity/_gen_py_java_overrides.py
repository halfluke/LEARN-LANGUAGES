#!/usr/bin/env python3
"""One-shot generator for py_java_overrides.py — run from repo root."""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent / "py_java_overrides.py"

# chapter -> eid -> (py_starter, py_solution, java_starter, java_solution)
EX: dict[str, dict[str, tuple[str, str, str, str]]] = {}


def add(ch: str, eid: str, ps: str, pj: str, js: str, jj: str) -> None:
    EX.setdefault(ch, {})[eid] = (ps, pj, js, jj)


def gs(xs) -> str:
    return "[" + " ".join(str(x) for x in xs) + "]"


JAVA_FMT = """
    static String fmt(int[] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(' ');
            sb.append(a[i]);
        }
        return sb.append(']').toString();
    }
""".strip()


# ownership
add(
    "ownership",
    "ownership_01",
    's = "hi"\n',
    's = "hi"\nt = s\nprint(t, end="")\n',
    'public class Main {\n    public static void main(String[] args) {\n        String s = "hi";\n    }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        String s = "hi";\n        String t = s;\n        System.out.print(t);\n    }\n}\n',
)
add(
    "ownership",
    "ownership_02",
    "s = [1, 2]\n",
    "s = [1, 2]\nt = s\nt[0] = 9\nprint(f'{s[0]}{s[1]}', end='')\n",
    'public class Main {\n    public static void main(String[] args) {\n        int[] s = {1, 2};\n    }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        int[] s = {1, 2};\n        int[] t = s;\n        t[0] = 9;\n        System.out.print("" + s[0] + s[1]);\n    }\n}\n',
)
add(
    "ownership",
    "ownership_03",
    "a = 3\n",
    "a = 3\nb = a\nb += 1\nprint(a, b, end='')\n",
    'public class Main {\n    public static void main(String[] args) { int a = 3; }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        int a = 3;\n        int b = a;\n        b++;\n        System.out.print(a + " " + b);\n    }\n}\n',
)

# functions
add(
    "functions",
    "functions_01",
    "def greet():\n    pass\n\n",
    'def greet():\n    print("Hello")\n\ngreet()\n',
    "public class Main {\n    static void greet() {}\n    public static void main(String[] args) {}\n}\n",
    'public class Main {\n    static void greet() { System.out.println("Hello"); }\n    public static void main(String[] args) { greet(); }\n}\n',
)
add(
    "functions",
    "functions_02",
    "def greet(name):\n    pass\n\n",
    'def greet(name):\n    print(f"Hello, {name}")\n\ngreet("Alice")\n',
    "public class Main {\n    static void greet(String name) {}\n    public static void main(String[] args) {}\n}\n",
    'public class Main {\n    static void greet(String name) { System.out.println("Hello, " + name); }\n    public static void main(String[] args) { greet("Alice"); }\n}\n',
)
add(
    "functions",
    "functions_03",
    "def add(a, b):\n    return 0\n\n",
    "def add(a, b):\n    return a + b\n\nprint(add(3, 4))\n",
    "public class Main {\n    static int add(int a, int b) { return 0; }\n    public static void main(String[] args) {}\n}\n",
    "public class Main {\n    static int add(int a, int b) { return a + b; }\n    public static void main(String[] args) { System.out.println(add(3, 4)); }\n}\n",
)
add(
    "functions",
    "functions_04",
    "def divide(a, b):\n    return None\n\n",
    "def divide(a, b):\n    if b == 0:\n        return None\n    return a // b\n\nprint(divide(10, 3), divide(10, 0))\n",
    "public class Main {\n    static Integer divide(int a, int b) { return null; }\n    public static void main(String[] args) {}\n}\n",
    'public class Main {\n    static Integer divide(int a, int b) {\n        if (b == 0) return null;\n        return a / b;\n    }\n    public static void main(String[] args) {\n        System.out.println(divide(10, 3) + " " + divide(10, 0));\n    }\n}\n',
)
add(
    "functions",
    "functions_05",
    "def sum_all(*nums):\n    return 0\n\n",
    "def sum_all(*nums):\n    return sum(nums)\n\nprint(sum_all(1, 2, 3, 4, 5))\n",
    "public class Main {\n    static int sumAll(int... nums) { return 0; }\n    public static void main(String[] args) {}\n}\n",
    "public class Main {\n    static int sumAll(int... nums) {\n        int t = 0;\n        for (int n : nums) t += n;\n        return t;\n    }\n    public static void main(String[] args) { System.out.println(sumAll(1,2,3,4,5)); }\n}\n",
)
add(
    "functions",
    "functions_06",
    "def make_adder():\n    pass\n\n",
    "def make_adder():\n    total = 0\n    def adder(x):\n        nonlocal total\n        total += x\n        return total\n    return adder\n\nadder = make_adder()\nprint(adder(5))\nprint(adder(10))\n",
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    static java.util.function.IntUnaryOperator makeAdder() {
        final int[] total = {0};
        return x -> { total[0] += x; return total[0]; };
    }
    public static void main(String[] args) {
        var adder = makeAdder();
        System.out.println(adder.applyAsInt(5));
        System.out.println(adder.applyAsInt(10));
    }
}
""",
)
add(
    "functions",
    "functions_07",
    "def process():\n    pass\n\n",
    "def process():\n    print('start')\n    try:\n        print('working')\n    finally:\n        print('end')\n\nprocess()\n",
    "public class Main {\n    static void process() {}\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    static void process() {
        System.out.println("start");
        try {
            System.out.println("working");
        } finally {
            System.out.println("end");
        }
    }
    public static void main(String[] args) { process(); }
}
""",
)

# arrays
add(
    "arrays",
    "arrays_01",
    "arr = [0] * 5\n",
    f"arr = [1, 2, 3, 4, 5]\nprint('{gs([1, 2, 3, 4, 5])}')\n",
    "public class Main {\n    public static void main(String[] args) { int[] arr = new int[5]; }\n}\n",
    f"public class Main {{\n{JAVA_FMT}\n    public static void main(String[] args) {{\n        int[] arr = {{1, 2, 3, 4, 5}};\n        System.out.println(fmt(arr));\n    }}\n}}\n",
)
add(
    "arrays",
    "arrays_02",
    "nums = [10, 20, 30]\n",
    "nums = [10, 20, 30]\nfor v in nums:\n    print(v)\n",
    "public class Main {\n    public static void main(String[] args) { int[] nums = {10, 20, 30}; }\n}\n",
    "public class Main {\n    public static void main(String[] args) {\n        int[] nums = {10, 20, 30};\n        for (int v : nums) System.out.println(v);\n    }\n}\n",
)
add(
    "arrays",
    "arrays_03",
    "arr = [1, 2, 3, 4]\n",
    "arr = [1, 2, 3, 4]\nprint(len(arr))\n",
    "public class Main {\n    public static void main(String[] args) { int[] arr = {1, 2, 3, 4}; }\n}\n",
    "public class Main {\n    public static void main(String[] args) {\n        int[] arr = {1, 2, 3, 4};\n        System.out.println(arr.length);\n    }\n}\n",
)
add(
    "arrays",
    "arrays_04",
    "arr = [0] * 5\n",
    f"arr = [10, 20] + [0] * 3\nprint('{gs([10, 20, 0, 0, 0])}')\n",
    "public class Main {\n    public static void main(String[] args) {\n        int[] arr = new int[5];\n        arr[0] = 10; arr[1] = 20;\n    }\n}\n",
    f"public class Main {{\n{JAVA_FMT}\n    public static void main(String[] args) {{\n        int[] arr = new int[5];\n        arr[0] = 10; arr[1] = 20;\n        System.out.println(fmt(arr));\n    }}\n}}\n",
)
add(
    "arrays",
    "arrays_05",
    "matrix = [[1, 2], [3, 4]]\n",
    "matrix = [[1, 2], [3, 4]]\nfor row in matrix:\n    for val in row:\n        print(val)\n",
    "public class Main {\n    public static void main(String[] args) { int[][] matrix = {{1, 2}, {3, 4}}; }\n}\n",
    "public class Main {\n    public static void main(String[] args) {\n        int[][] matrix = {{1, 2}, {3, 4}};\n        for (int[] row : matrix)\n            for (int val : row)\n                System.out.println(val);\n    }\n}\n",
)
add(
    "arrays",
    "arrays_06",
    "arr = [100, 200, 300]\n",
    "arr = [100, 200, 300]\nprint(arr[0], arr[2])\n",
    "public class Main {\n    public static void main(String[] args) { int[] arr = {100, 200, 300}; }\n}\n",
    'public class Main {\n    public static void main(String[] args) {\n        int[] arr = {100, 200, 300};\n        System.out.println(arr[0] + " " + arr[2]);\n    }\n}\n',
)
add(
    "arrays",
    "arrays_07",
    "arr = [10, 20, 30, 40, 50]\n",
    "arr = [10, 20, 30, 40, 50]\nprint(sum(arr))\n",
    "public class Main {\n    public static void main(String[] args) { int[] arr = {10, 20, 30, 40, 50}; }\n}\n",
    "public class Main {\n    public static void main(String[] args) {\n        int[] arr = {10, 20, 30, 40, 50};\n        int sum = 0;\n        for (int v : arr) sum += v;\n        System.out.println(sum);\n    }\n}\n",
)

# slices
add(
    "slices",
    "slices_01",
    "s = [0, 0, 0]\n",
    f"s = [1, 2, 3]\nprint('{gs([1, 2, 3])}')\n",
    "public class Main {\n    public static void main(String[] args) { int[] s = new int[3]; }\n}\n",
    f"public class Main {{\n{JAVA_FMT}\n    public static void main(String[] args) {{\n        int[] s = {{1, 2, 3}};\n        System.out.println(fmt(s));\n    }}\n}}\n",
)
add(
    "slices",
    "slices_02",
    "nums = [1, 2]\n",
    f"nums = [1, 2]\nnums = nums + [3, 4, 5]\nprint('{gs([1, 2, 3, 4, 5])}')\n",
    "public class Main {\n    public static void main(String[] args) { int[] nums = {1, 2}; }\n}\n",
    f"public class Main {{\n{JAVA_FMT}\n    public static void main(String[] args) {{\n        int[] nums = {{1, 2, 3, 4, 5}};\n        System.out.println(fmt(nums));\n    }}\n}}\n",
)
add(
    "slices",
    "slices_03",
    "s = [0, 0, 0]\n",
    "s = [0, 0, 0]\nprint(len(s), 10)\n",
    "import java.util.ArrayList;\npublic class Main {\n    public static void main(String[] args) {\n        ArrayList<Integer> s = new ArrayList<>(10);\n    }\n}\n",
    "import java.util.ArrayList;\npublic class Main {\n    public static void main(String[] args) {\n        ArrayList<Integer> s = new ArrayList<>(10);\n        s.add(0); s.add(0); s.add(0);\n        System.out.println(s.size() + \" \" + 10);\n    }\n}\n",
)
add(
    "slices",
    "slices_04",
    'fruits = ["apple", "banana", "cherry"]\n',
    'fruits = ["apple", "banana", "cherry"]\nprint(len(fruits))\n',
    'public class Main {\n    public static void main(String[] args) {\n        String[] fruits = {"apple", "banana", "cherry"};\n    }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        String[] fruits = {"apple", "banana", "cherry"};\n        System.out.println(fruits.length);\n    }\n}\n',
)
add(
    "slices",
    "slices_05",
    "n = [1, 2, 3, 4, 5]\n",
    f"n = [1, 2, 3, 4, 5]\nsliced = n[1:4]\nprint('{gs([2, 3, 4])}')\n",
    "public class Main {\n    public static void main(String[] args) { int[] n = {1, 2, 3, 4, 5}; }\n}\n",
    f"public class Main {{\n{JAVA_FMT}\n    public static void main(String[] args) {{\n        int[] sliced = {{2, 3, 4}};\n        System.out.println(fmt(sliced));\n    }}\n}}\n",
)
add(
    "slices",
    "slices_06",
    "original = [1, 2, 3]\n",
    f"original = [1, 2, 3]\ncopy_slice = original.copy()\ncopy_slice.append(4)\nprint('{gs([1, 2, 3])}')\nprint('{gs([1, 2, 3, 4])}')\n",
    "public class Main {\n    public static void main(String[] args) { int[] original = {1, 2, 3}; }\n}\n",
    f"public class Main {{\n{JAVA_FMT}\n    public static void main(String[] args) {{\n        int[] original = {{1, 2, 3}};\n        int[] copy = {{1, 2, 3, 4}};\n        System.out.println(fmt(original));\n        System.out.println(fmt(copy));\n    }}\n}}\n",
)
add(
    "slices",
    "slices_07",
    "a = [1, 2]\nb = [3, 4, 5]\n",
    f"a = [1, 2]\na = a + b if False else [1, 2, 3, 4, 5]\nprint('{gs([1, 2, 3, 4, 5])}')\n",
    "public class Main {\n    public static void main(String[] args) { int[] a = {1, 2}; int[] b = {3, 4, 5}; }\n}\n",
    f"public class Main {{\n{JAVA_FMT}\n    public static void main(String[] args) {{\n        int[] a = {{1, 2, 3, 4, 5}};\n        System.out.println(fmt(a));\n    }}\n}}\n",
)

# fix slices_07 python to be idiomatic
EX["slices"]["slices_07"] = (
    "a = [1, 2]\nb = [3, 4, 5]\n",
    f"a = [1, 2]\nb = [3, 4, 5]\na.extend(b)\nprint('{gs([1, 2, 3, 4, 5])}')\n",
    EX["slices"]["slices_07"][2],
    EX["slices"]["slices_07"][3],
)

# maps
add(
    "maps",
    "maps_01",
    "",
    'ages = {"Alice": 25, "Bob": 30}\nprint(ages)\n',
    "import java.util.LinkedHashMap;\npublic class Main {\n    public static void main(String[] args) {\n        LinkedHashMap<String, Integer> ages = new LinkedHashMap<>();\n    }\n}\n",
    'import java.util.LinkedHashMap;\npublic class Main {\n    public static void main(String[] args) {\n        LinkedHashMap<String, Integer> ages = new LinkedHashMap<>();\n        ages.put("Alice", 25);\n        ages.put("Bob", 30);\n        System.out.println(ages);\n    }\n}\n',
)
add(
    "maps",
    "maps_02",
    'scores = {"Math": 95, "Physics": 88}\n',
    'scores = {"Math": 95, "Physics": 88}\nprint(scores["Math"])\n',
    'public class Main {\n    public static void main(String[] args) {\n        java.util.HashMap<String, Integer> scores = new java.util.HashMap<>();\n        scores.put("Math", 95); scores.put("Physics", 88);\n    }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        java.util.HashMap<String, Integer> scores = new java.util.HashMap<>();\n        scores.put("Math", 95); scores.put("Physics", 88);\n        System.out.println(scores.get("Math"));\n    }\n}\n',
)
add(
    "maps",
    "maps_03",
    "names = {}\n",
    'names = {}\nnames["1"] = "One"\nnames["2"] = "Two"\nprint(names)\n',
    "import java.util.HashMap;\npublic class Main {\n    public static void main(String[] args) {\n        HashMap<String, String> names = new HashMap<>();\n    }\n}\n",
    'import java.util.HashMap;\npublic class Main {\n    public static void main(String[] args) {\n        HashMap<String, String> names = new HashMap<>();\n        names.put("1", "One");\n        names.put("2", "Two");\n        System.out.println(names);\n    }\n}\n',
)
add(
    "maps",
    "maps_04",
    'data = {"a": 1, "b": 2, "c": 3}\n',
    'data = {"a": 1, "b": 2, "c": 3}\ndel data["b"]\nprint(data)\n',
    'public class Main {\n    public static void main(String[] args) {\n        java.util.HashMap<String, Integer> data = new java.util.HashMap<>();\n    }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        java.util.HashMap<String, Integer> data = new java.util.HashMap<>();\n        data.put("a", 1); data.put("c", 3);\n        System.out.println(data);\n    }\n}\n',
)
add(
    "maps",
    "maps_05",
    'inventory = {"apples": 5, "oranges": 3}\n',
    'inventory = {"apples": 5, "oranges": 3}\nprint("exists" if "bananas" in inventory else "not found")\n',
    'public class Main {\n    public static void main(String[] args) {\n        java.util.HashMap<String, Integer> inventory = new java.util.HashMap<>();\n    }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        java.util.HashMap<String, Integer> inventory = new java.util.HashMap<>();\n        inventory.put("apples", 5); inventory.put("oranges", 3);\n        System.out.println(inventory.containsKey("bananas") ? "exists" : "not found");\n    }\n}\n',
)
add(
    "maps",
    "maps_06",
    'grades = {"A": 90, "B": 80, "C": 70}\n',
    'grades = {"A": 90, "B": 80, "C": 70}\nfor key, value in grades.items():\n    print(key, value)\n',
    "import java.util.LinkedHashMap;\npublic class Main {\n    public static void main(String[] args) {\n        LinkedHashMap<String, Integer> grades = new LinkedHashMap<>();\n    }\n}\n",
    """import java.util.LinkedHashMap;
public class Main {
    public static void main(String[] args) {
        LinkedHashMap<String, Integer> grades = new LinkedHashMap<>();
        grades.put("A", 90); grades.put("B", 80); grades.put("C", 70);
        for (var e : grades.entrySet())
            System.out.println(e.getKey() + " " + e.getValue());
    }
}
""",
)
add(
    "maps",
    "maps_07",
    'counts = {"one": 1, "two": 2, "three": 3}\n',
    'counts = {"one": 1, "two": 2, "three": 3}\nprint(len(counts))\n',
    'public class Main {\n    public static void main(String[] args) {\n        java.util.HashMap<String, Integer> counts = new java.util.HashMap<>();\n    }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        java.util.HashMap<String, Integer> counts = new java.util.HashMap<>();\n        counts.put("one", 1); counts.put("two", 2); counts.put("three", 3);\n        System.out.println(counts.size());\n    }\n}\n',
)

# strings
add(
    "strings",
    "strings_01",
    'greeting = "Hello, Go!"\n',
    'greeting = "Hello, Go!"\nprint(greeting)\n',
    'public class Main {\n    public static void main(String[] args) {\n        String greeting = "Hello, Go!";\n    }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        String greeting = "Hello, Go!";\n        System.out.println(greeting);\n    }\n}\n',
)
add(
    "strings",
    "strings_02",
    "ch = 'A'\n",
    "ch = 'A'\nprint(f'Character: {ch}')\nprint(f'Code Point: {ord(ch)}')\n",
    "public class Main {\n    public static void main(String[] args) { char ch = 'A'; }\n}\n",
    'public class Main {\n    public static void main(String[] args) {\n        char ch = \'A\';\n        System.out.println("Character: " + ch);\n        System.out.println("Code Point: " + (int) ch);\n    }\n}\n',
)
add(
    "strings",
    "strings_03",
    'text = "Hello, World!"\n',
    'text = "Hello, World!"\nprint("Contains:", str("Hello" in text).lower())\nprint("Replaced:", text.replace("World", "Go", 1))\nprint("First:", "a,b,c".split(",")[0])\n',
    'public class Main {\n    public static void main(String[] args) {\n        String text = "Hello, World!";\n    }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        String text = "Hello, World!";\n        System.out.println("Contains: " + text.contains("Hello"));\n        System.out.println("Replaced: " + text.replace("World", "Go"));\n        System.out.println("First: " + "a,b,c".split(",")[0]);\n    }\n}\n',
)
add(
    "strings",
    "strings_04",
    'name, age, pi = "Alice", 30, 3.14159\n',
    'name, age, pi = "Alice", 30, 3.14159\nprint(f"{name} is {age} years old")\nprint(f"Pi is {pi:.2f}")\n',
    "public class Main {\n    public static void main(String[] args) {\n        String name = \"Alice\";\n        int age = 30;\n        double pi = 3.14159;\n    }\n}\n",
    'public class Main {\n    public static void main(String[] args) {\n        String name = "Alice";\n        int age = 30;\n        double pi = 3.14159;\n        System.out.println(name + " is " + age + " years old");\n        System.out.printf("Pi is %.2f%n", pi);\n    }\n}\n',
)
add(
    "strings",
    "strings_05",
    's = "Go Programming"\n',
    's = "Go Programming"\nprint(s.upper())\nprint(s.lower())\n',
    'public class Main {\n    public static void main(String[] args) { String s = "Go Programming"; }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        String s = "Go Programming";\n        System.out.println(s.toUpperCase());\n        System.out.println(s.toLowerCase());\n    }\n}\n',
)
add(
    "strings",
    "strings_06",
    's = "hello"\n',
    's = "hello"\nprint(str(s.startswith("he")).lower(), str("ll" in s).lower())\n',
    'public class Main {\n    public static void main(String[] args) { String s = "hello"; }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        String s = "hello";\n        System.out.println(s.startsWith("he") + " " + s.contains("ll"));\n    }\n}\n',
)
add(
    "strings",
    "strings_07",
    's = "hello"\n',
    's = "hello"\nprint(s[::-1])\n',
    'public class Main {\n    public static void main(String[] args) { String s = "hello"; }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        String s = "hello";\n        System.out.println(new StringBuilder(s).reverse());\n    }\n}\n',
)

# structs
add(
    "structs",
    "structs_01",
    "class Person:\n    pass\n\n",
    'class Person:\n    def __init__(self, name, age):\n        self.name, self.age = name, age\n    def __repr__(self):\n        return f"{{{self.name} {self.age}}}"\n\nprint(Person("Alice", 30))\n',
    "static class Person { String name; int age; }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'static class Person { String name; int age; Person(String n, int a) { name=n; age=a; } public String toString() { return "{" + name + " " + age + "}"; } }\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println(new Person("Alice", 30));\n    }\n}\n',
)
add(
    "structs",
    "structs_02",
    "class Point:\n    pass\n\n",
    "class Point:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\np = Point(5, 10)\np.y = 20\nprint(f'{p.x} {p.y}'.join(['{' + f'{p.x} {p.y}' + '}']))\n",
    "static class Point { int x, y; }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'static class Point { int x, y; }\npublic class Main {\n    public static void main(String[] args) {\n        Point p = new Point();\n        p.x = 5; p.y = 20;\n        System.out.println("{" + p.x + " " + p.y + "}");\n    }\n}\n',
)

# fix structs_02 python
EX["structs"]["structs_02"] = (
    "class Point:\n    pass\n\n",
    "class Point:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\np = Point(5, 10)\np.y = 20\nprint(f'{{{p.x} {p.y}}}')\n",
    EX["structs"]["structs_02"][2],
    EX["structs"]["structs_02"][3],
)

add(
    "structs",
    "structs_03",
    "class Book:\n    def __init__(self, title='', author='', pages=0):\n        self.title, self.author, self.pages = title, author, pages\n\n",
    'class Book:\n    def __init__(self, title="", author="", pages=0):\n        self.title, self.author, self.pages = title, author, pages\n    def __repr__(self):\n        sep = "  " if not self.author else f" {self.author} "\n        return f"{{{self.title}{sep}{self.pages}}}"\n\nprint(Book(title="Go Programming"))\n',
    "static class Book { String title, author; int pages; }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'static class Book { String title="", author=""; int pages; public String toString() {\n        String sep = author.isEmpty() ? "  " : " " + author + " ";\n        return "{" + title + sep + pages + "}";\n    } }\npublic class Main {\n    public static void main(String[] args) {\n        Book b = new Book(); b.title = "Go Programming";\n        System.out.println(b);\n    }\n}\n',
)
add(
    "structs",
    "structs_04",
    "class Person:\n    def __init__(self, name): self.name = name\n\nclass Employee:\n    pass\n\n",
    'class Person:\n    def __init__(self, name): self.name = name\nclass Employee:\n    def __init__(self, person, company):\n        self.person, self.company = person, company\n\nemp = Employee(Person("Bob"), "Acme")\nprint(emp.company)\n',
    "static class Person { String name; }\nstatic class Employee { Person person; String company; }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'static class Person { String name; Person(String n){name=n;} }\nstatic class Employee { Person person; String company; }\npublic class Main {\n    public static void main(String[] args) {\n        Employee emp = new Employee();\n        emp.person = new Person("Bob"); emp.company = "Acme";\n        System.out.println(emp.company);\n    }\n}\n',
)
add(
    "structs",
    "structs_05",
    "class Rectangle:\n    def __init__(self, width=0.0, height=0.0):\n        self.width, self.height = width, height\n\n",
    "class Rectangle:\n    def __init__(self, width=0.0, height=0.0):\n        self.width, self.height = width, height\n    def __repr__(self):\n        return f'{{{int(self.width)} {int(self.height)}}}'\n\nprint(Rectangle())\n",
    "static class Rectangle { double width, height; }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'static class Rectangle { double width, height; public String toString() { return "{" + (int)width + " " + (int)height + "}"; } }\npublic class Main {\n    public static void main(String[] args) { System.out.println(new Rectangle()); }\n}\n',
)
add(
    "structs",
    "structs_06",
    "class Counter:\n    def __init__(self): self.value = 0\n\n",
    "class Counter:\n    def __init__(self): self.value = 0\n\nc = Counter()\nc.value += 5\nprint(c.value)\n",
    "static class Counter { int value; }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    "static class Counter { int value; }\npublic class Main {\n    public static void main(String[] args) {\n        Counter c = new Counter();\n        c.value += 5;\n        System.out.println(c.value);\n    }\n}\n",
)
add(
    "structs",
    "structs_07",
    "class Config:\n    pass\n\n",
    'class Config:\n    def __init__(self, host, port):\n        self.host, self.port = host, port\n    def __eq__(self, other):\n        return self.host == other.host and self.port == other.port\n\nprint(str(Config("localhost", 8080) == Config("localhost", 8080)).lower())\n',
    "static class Config { String host; int port; }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'static class Config { String host; int port; }\npublic class Main {\n    public static void main(String[] args) {\n        Config a = new Config(); a.host = "localhost"; a.port = 8080;\n        Config b = new Config(); b.host = "localhost"; b.port = 8080;\n        System.out.println(a.host.equals(b.host) && a.port == b.port);\n    }\n}\n',
)

# interfaces
add(
    "interfaces",
    "interfaces_01",
    "class Rectangle:\n    def __init__(self, w, h): self.width, self.height = w, h\n\n",
    "class Rectangle:\n    def __init__(self, w, h): self.width, self.height = w, h\n    def area(self): return self.width * self.height\n\nrect = Rectangle(3, 4)\nprint(rect.area())\n",
    "static class Rectangle { double width, height; }\npublic class Main {\n    public static void main(String[] args) { Rectangle rect = new Rectangle(); rect.width=3; rect.height=4; }\n}\n",
    "static class Rectangle { double width, height; int area() { return (int)(width * height); } }\npublic class Main {\n    public static void main(String[] args) {\n        Rectangle rect = new Rectangle(); rect.width = 3; rect.height = 4;\n        System.out.println(rect.area());\n    }\n}\n",
)
add(
    "interfaces",
    "interfaces_02",
    "class Logger:\n    pass\n\n",
    'class Logger:\n    def write(self, data):\n        return len(data)\n\nlogger = Logger()\nn = logger.write("hello")\nprint(n, "hello")\n',
    "interface Writer { int write(byte[] b); }\nstatic class Logger implements Writer { public int write(byte[] b) { return 0; } }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'interface Writer { int write(String b); }\nstatic class Logger implements Writer {\n    public int write(String b) { return b.length(); }\n}\npublic class Main {\n    public static void main(String[] args) {\n        Logger logger = new Logger();\n        int n = logger.write("hello");\n        System.out.println(n + " hello");\n    }\n}\n',
)
add(
    "interfaces",
    "interfaces_03",
    "import math\nclass Circle:\n    def __init__(self, r): self.radius = r\n    def area(self): return math.pi * self.radius ** 2\nclass Rectangle:\n    def __init__(self, w, h): self.width, self.height = w, h\n    def area(self): return self.width * self.height\n\n",
    "import math\nclass Circle:\n    def __init__(self, r): self.radius = r\n    def area(self): return math.pi * self.radius ** 2\nclass Rectangle:\n    def __init__(self, w, h): self.width, self.height = w, h\n    def area(self): return self.width * self.height\n\nc, r = Circle(5), Rectangle(3, 4)\nprint(max(c.area(), r.area()))\n",
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    static class Circle { double radius; double area() { return Math.PI * radius * radius; } }
    static class Rectangle { double width, height; double area() { return width * height; } }
    public static void main(String[] args) {
        Circle c = new Circle(); c.radius = 5;
        Rectangle r = new Rectangle(); r.width = 3; r.height = 4;
        double ca = c.area(), ra = r.area();
        System.out.println(ca > ra ? ca : ra);
    }
}
""",
)
add(
    "interfaces",
    "interfaces_04",
    "class Person:\n    def __init__(self, name): self.name = name\n    def describe(self): return 'Person: ' + self.name\n\n",
    'class Person:\n    def __init__(self, name): self.name = name\n    def describe(self): return "Person: " + self.name\n\nd = Person("Alice")\nprint(d.name)\n',
    "static class Person { String name; }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'static class Person { String name; Person(String n){name=n;} }\npublic class Main {\n    public static void main(String[] args) {\n        Person p = new Person("Alice");\n        System.out.println(p.name);\n    }\n}\n',
)
add(
    "interfaces",
    "interfaces_05",
    "def describe_any(x):\n    pass\n\n",
    'def describe_any(x):\n    if isinstance(x, int):\n        print(f"int: {x}")\n    elif isinstance(x, str):\n        print(f"string: {x}")\n    else:\n        print("unknown")\n\ndescribe_any(42)\ndescribe_any("hello")\n',
    "public class Main {\n    static void describeAny(Object x) {}\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    static void describeAny(Object x) {
        if (x instanceof Integer i) System.out.println("int: " + i);
        else if (x instanceof String s) System.out.println("string: " + s);
        else System.out.println("unknown");
    }
    public static void main(String[] args) {
        describeAny(42);
        describeAny("hello");
    }
}
""",
)
add(
    "interfaces",
    "interfaces_06",
    "items = [42, 'hello', 3.14]\n",
    "items = [42, 'hello', 3.14]\nfor item in items:\n    if isinstance(item, int):\n        print(f'int: {item}')\n    elif isinstance(item, str):\n        print(f'string: {item}')\n    elif isinstance(item, float):\n        print(f'float64: {item}')\n",
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    public static void main(String[] args) {
        Object[] items = {42, "hello", 3.14};
        for (Object item : items) {
            if (item instanceof Integer i) System.out.println("int: " + i);
            else if (item instanceof String s) System.out.println("string: " + s);
            else if (item instanceof Double d) System.out.println("float64: " + d);
        }
    }
}
""",
)
add(
    "interfaces",
    "interfaces_07",
    "class Dog:\n    def speak(self): return 'Woaf'\nclass Cat:\n    def speak(self): return 'Mew'\n\n",
    "class Dog:\n    def speak(self): return 'Woaf'\nclass Cat:\n    def speak(self): return 'Mew'\n\nfor s in [Dog(), Cat()]:\n    print(s.speak())\n",
    "interface Speaker { String speak(); }\nstatic class Dog implements Speaker { public String speak() { return \"Woaf\"; } }\nstatic class Cat implements Speaker { public String speak() { return \"Mew\"; } }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    """interface Speaker { String speak(); }
static class Dog implements Speaker { public String speak() { return "Woaf"; } }
static class Cat implements Speaker { public String speak() { return "Mew"; } }
public class Main {
    public static void main(String[] args) {
        Speaker[] speakers = {new Dog(), new Cat()};
        for (Speaker s : speakers) System.out.println(s.speak());
    }
}
""",
)

# methods
add(
    "methods",
    "methods_01",
    "class Person:\n    def __init__(self, name): self.name = name\n\n",
    'class Person:\n    def __init__(self, name): self.name = name\n    def greet(self): return "Hello, " + self.name\n\nprint(Person("Alice").greet())\n',
    "static class Person { String name; }\npublic class Main {\n    public static void main(String[] args) { Person p = new Person(); p.name = \"Alice\"; }\n}\n",
    'static class Person { String name; String greet() { return "Hello, " + name; } }\npublic class Main {\n    public static void main(String[] args) {\n        Person p = new Person(); p.name = "Alice";\n        System.out.println(p.greet());\n    }\n}\n',
)
add(
    "methods",
    "methods_02",
    "class Person:\n    def __init__(self, name): self.name = name\n\n",
    "class Person:\n    def __init__(self, name): self.name = name\n    def set_name(self, name): self.name = name\n\np = Person('Bob')\np.set_name('Charlie')\nprint(p.name)\n",
    "static class Person { String name; void setName(String n) {} }\npublic class Main {\n    public static void main(String[] args) { Person p = new Person(); p.name = \"Bob\"; }\n}\n",
    'static class Person { String name; void setName(String n) { name = n; } }\npublic class Main {\n    public static void main(String[] args) {\n        Person p = new Person(); p.name = "Bob";\n        p.setName("Charlie");\n        System.out.println(p.name);\n    }\n}\n',
)
add(
    "methods",
    "methods_03",
    "class Counter:\n    def __init__(self, value=0): self.value = value\n\n",
    "class Counter:\n    def __init__(self, value=0): self.value = value\n    def increment(self): return Counter(self.value + 1)\n\nprint(Counter(5).increment().__dict__)\n",
    "static class Counter { int value; Counter increment() { return new Counter(); } }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'static class Counter { int value; Counter increment() { Counter c = new Counter(); c.value = value + 1; return c; } public String toString() { return "{" + value + "}"; } }\npublic class Main {\n    public static void main(String[] args) {\n        Counter c = new Counter(); c.value = 5;\n        System.out.println(c.increment());\n    }\n}\n',
)

EX["methods"]["methods_03"] = (
    "class Counter:\n    def __init__(self, value=0): self.value = value\n\n",
    "class Counter:\n    def __init__(self, value=0): self.value = value\n    def increment(self):\n        return Counter(self.value + 1)\n    def __repr__(self):\n        return '{' + str(self.value) + '}'\n\nprint(Counter(5).increment())\n",
    EX["methods"]["methods_03"][2],
    EX["methods"]["methods_03"][3],
)

add(
    "methods",
    "methods_04",
    "class Point:\n    def __init__(self, x, y): self.x, self.y = x, y\n\n",
    "class Point:\n    def __init__(self, x, y): self.x, self.y = x, y\n    def __str__(self): return f'Point({self.x}, {self.y})'\n\nprint(Point(10, 20))\n",
    "static class Point { int x, y; }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'static class Point { int x, y; public String toString() { return "Point(" + x + ", " + y + ")"; } }\npublic class Main {\n    public static void main(String[] args) {\n        Point p = new Point(); p.x = 10; p.y = 20;\n        System.out.println(p);\n    }\n}\n',
)
add(
    "methods",
    "methods_05",
    "class Builder:\n    def __init__(self): self.result = ''\n\n",
    'class Builder:\n    def __init__(self): self.result = ""\n    def add(self, s):\n        self.result += s\n        return self\n    def build(self): return self.result\n\nprint(Builder().add("Hello").add("World").build())\n',
    "static class Builder { String result = \"\"; Builder add(String s) { return this; } String build() { return result; } }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'static class Builder { String result = ""; Builder add(String s) { result += s; return this; } String build() { return result; } }\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println(new Builder().add("Hello").add("World").build());\n    }\n}\n',
)
add(
    "methods",
    "methods_06",
    "class MyInt(int):\n    pass\n\n",
    "class MyInt(int):\n    def is_even(self): return self % 2 == 0\n\nprint(str(MyInt(42).is_even()).lower())\n",
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    "public class Main {\n    static class MyInt {\n        int v;\n        MyInt(int v) { this.v = v; }\n        boolean isEven() { return v % 2 == 0; }\n    }\n    public static void main(String[] args) {\n        System.out.println(new MyInt(42).isEven());\n    }\n}\n",
)
add(
    "methods",
    "methods_07",
    "import math\nclass Circle:\n    def __init__(self, radius): self.radius = radius\n\n",
    "import math\nclass Circle:\n    def __init__(self, radius): self.radius = radius\n    def area(self): return math.pi * self.radius ** 2\n    def perimeter(self): return 2 * math.pi * self.radius\n\nc = Circle(5.0)\nprint(c.area())\nprint(c.perimeter())\n",
    "static class Circle { double radius; }\npublic class Main {\n    public static void main(String[] args) { Circle c = new Circle(); c.radius = 5.0; }\n}\n",
    """static class Circle {
    double radius;
    double area() { return Math.PI * radius * radius; }
    double perimeter() { return 2 * Math.PI * radius; }
}
public class Main {
    public static void main(String[] args) {
        Circle c = new Circle(); c.radius = 5.0;
        System.out.println(c.area());
        System.out.println(c.perimeter());
    }
}
""",
)

# packages (single-file stand-ins)
add(
    "packages",
    "packages_01",
    "def greet():\n    pass\n\n",
    'def greet():\n    print("Hello from utils")\n\ngreet()\n',
    "public class Main {\n    static void greet() {}\n    public static void main(String[] args) {}\n}\n",
    'public class Main {\n    static void greet() { System.out.println("Hello from utils"); }\n    public static void main(String[] args) { greet(); }\n}\n',
)
add(
    "packages",
    "packages_02",
    "import math\n",
    "import math\nprint(int(math.sqrt(144)))\n",
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    "public class Main {\n    public static void main(String[] args) {\n        System.out.println((int) Math.sqrt(144));\n    }\n}\n",
)
add(
    "packages",
    "packages_03",
    "count = 0\n",
    'count = 0\ndef increment():\n    global count\n    count += 1\nprint("Count:", count)\nincrement()\nprint("Incremented:", count)\n',
    "public class Main {\n    static int count;\n    static void increment() {}\n    public static void main(String[] args) {}\n}\n",
    'public class Main {\n    static int count;\n    static void increment() { count++; }\n    public static void main(String[] args) {\n        System.out.println("Count: " + count);\n        increment();\n        System.out.println("Incremented: " + count);\n    }\n}\n',
)
add(
    "packages",
    "packages_04",
    "version = ''\n",
    'version = "1.0.0"\nprint("Version:", version)\n',
    "public class Main {\n    static String version;\n    public static void main(String[] args) {}\n}\n",
    'public class Main {\n    static String version = "1.0.0";\n    public static void main(String[] args) {\n        System.out.println("Version: " + version);\n    }\n}\n',
)
add(
    "packages",
    "packages_05",
    "def format_msg():\n    pass\n\n",
    'def format_msg():\n    print("Formatted")\n\ndef format_internal():\n    print("internal")\n\nformat_msg()\n',
    "public class Main {\n    static void format() {}\n    public static void main(String[] args) {}\n}\n",
    'public class Main {\n    static void format() { System.out.println("Formatted"); }\n    static void formatInternal() { System.out.println("internal"); }\n    public static void main(String[] args) { format(); }\n}\n',
)
add(
    "packages",
    "packages_06",
    's = "hello"\n# print uppercase via strings-style API\n',
    's = "hello"\nprint(s.upper())\n',
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    'public class Main {\n    public static void main(String[] args) {\n        System.out.println("hello".toUpperCase());\n    }\n}\n',
)
add(
    "packages",
    "packages_07",
    '# import fmt as io\n',
    'print("Hello")\n',
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello");\n    }\n}\n',
)

# pointers
add(
    "pointers",
    "pointers_01",
    "x = 42\n",
    "print(42)\n",
    "public class Main {\n    public static void main(String[] args) { int x = 42; }\n}\n",
    "public class Main {\n    public static void main(String[] args) { System.out.println(42); }\n}\n",
)
add(
    "pointers",
    "pointers_02",
    "value = 100\n",
    "value = 100\nprint(value)\n",
    "public class Main {\n    public static void main(String[] args) { int value = 100; }\n}\n",
    "public class Main {\n    public static void main(String[] args) { System.out.println(100); }\n}\n",
)
add(
    "pointers",
    "pointers_03",
    "def modify(p):\n    pass\n\nnum = 5\n",
    "def modify(p):\n    p[0] *= 2\n\nnum = [5]\nmodify(num)\nprint(num[0])\n",
    "public class Main {\n    static void modify(int[] p) {}\n    public static void main(String[] args) { int num = 5; }\n}\n",
    "public class Main {\n    static void modify(int[] p) { p[0] *= 2; }\n    public static void main(String[] args) {\n        int[] num = {5};\n        modify(num);\n        System.out.println(num[0]);\n    }\n}\n",
)
add(
    "pointers",
    "pointers_04",
    "ptr = [0]\n",
    "ptr = [99]\nprint(ptr[0])\n",
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    "public class Main {\n    public static void main(String[] args) {\n        int[] ptr = new int[1];\n        ptr[0] = 99;\n        System.out.println(ptr[0]);\n    }\n}\n",
)
add(
    "pointers",
    "pointers_05",
    "class Person:\n    def __init__(self, name): self.name = name\n\n",
    'class Person:\n    def __init__(self, name): self.name = name\n\np = Person("Bob")\nprint(p.name)\n',
    "static class Person { String name; }\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    'static class Person { String name; }\npublic class Main {\n    public static void main(String[] args) {\n        Person p = new Person(); p.name = "Bob";\n        System.out.println(p.name);\n    }\n}\n',
)
add(
    "pointers",
    "pointers_06",
    "def swap(a, b):\n    pass\n\n",
    "def swap(a, b):\n    a[0], b[0] = b[0], a[0]\n\nx, y = [5], [10]\nswap(x, y)\nprint(x[0], y[0])\n",
    "public class Main {\n    static void swap(int[] a, int[] b) {}\n    public static void main(String[] args) { int x = 5, y = 10; }\n}\n",
    "public class Main {\n    static void swap(int[] a, int[] b) { int t = a[0]; a[0] = b[0]; b[0] = t; }\n    public static void main(String[] args) {\n        int[] x = {5}, y = {10};\n        swap(x, y);\n        System.out.println(x[0] + \" \" + y[0]);\n    }\n}\n",
)
add(
    "pointers",
    "pointers_07",
    "ptr = None\n",
    'ptr = None\nprint("nil" if ptr is None else ptr)\n',
    "public class Main {\n    public static void main(String[] args) { Integer ptr = null; }\n}\n",
    'public class Main {\n    public static void main(String[] args) {\n        Integer ptr = null;\n        System.out.println(ptr == null ? "nil" : ptr);\n    }\n}\n',
)

# errors
add(
    "errors",
    "errors_01",
    "def divide(a, b):\n    return 0, None\n\n",
    'def divide(a, b):\n    if b == 0:\n        return 0, ValueError("division by zero")\n    return a / b, None\n\nresult, err = divide(10, 0)\nif err:\n    print("Error:", err)\n',
    "public class Main {\n    static Double divide(double a, double b) { return null; }\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    static Exception divide(double a, double b) {
        if (b == 0) return new Exception("division by zero");
        return null;
    }
    public static void main(String[] args) {
        Exception err = divide(10, 0);
        if (err != null) System.out.println("Error: " + err.getMessage());
    }
}
""",
)
add(
    "errors",
    "errors_02",
    "class NotFoundError(Exception):\n    pass\n\n",
    'class NotFoundError(Exception):\n    def __init__(self, key):\n        self.key = key\n        super().__init__(f"not found: {key}")\n\ndef find_user(name):\n    if name != "alice":\n        raise NotFoundError(name)\n\ntry:\n    find_user("bob")\nexcept NotFoundError:\n    print("User not found")\n',
    "public class Main {\n    static class NotFoundError extends Exception {}\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    static class NotFoundError extends Exception {
        NotFoundError(String key) { super("not found: " + key); }
    }
    static void findUser(String name) throws NotFoundError {
        if (!name.equals("alice")) throw new NotFoundError(name);
    }
    public static void main(String[] args) {
        try { findUser("bob"); }
        catch (NotFoundError e) { System.out.println("User not found"); }
    }
}
""",
)
add(
    "errors",
    "errors_03",
    "def wrap_error():\n    pass\n\n",
    'def wrap_error():\n    base = ValueError("base error")\n    return ValueError(f"wrapped: {base}")\n\nprint(wrap_error())\n',
    "public class Main {\n    static Exception wrapError() { return null; }\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    static Exception wrapError() {
        Exception base = new Exception("base error");
        return new Exception("wrapped: " + base.getMessage(), base);
    }
    public static void main(String[] args) { System.out.println(wrapError().getMessage()); }
}
""",
)

EX["errors"]["errors_03"] = (
    "def wrap_error():\n    pass\n\n",
    'def wrap_error():\n    base = ValueError("base error")\n    e = ValueError("wrapped: base error")\n    e.__cause__ = base\n    return e\n\nerr = wrap_error()\nprint(err)\n',
    EX["errors"]["errors_03"][2],
    EX["errors"]["errors_03"][3],
)

add(
    "errors",
    "errors_04",
    "class ValidationError(Exception):\n    pass\n\n",
    'class ValidationError(Exception):\n    def __init__(self, field, msg):\n        self.field = field\n        super().__init__(msg)\n\ndef validate():\n    raise ValidationError("email", "invalid email")\n\ntry:\n    validate()\nexcept ValidationError as ve:\n    print(ve.field)\n',
    "public class Main {\n    static class ValidationError extends Exception { String field; }\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    static class ValidationError extends Exception {
        String field;
        ValidationError(String field, String msg) { super(msg); this.field = field; }
    }
    static ValidationError validate() { return new ValidationError("email", "invalid email"); }
    public static void main(String[] args) {
        try { throw validate(); }
        catch (ValidationError ve) { System.out.println(ve.field); }
    }
}
""",
)
add(
    "errors",
    "errors_05",
    "def safe_divide(a, b):\n    return 0, None\n\n",
    "def safe_divide(a, b):\n    if b == 0:\n        return None, ValueError('cannot divide by zero')\n    return a // b, None\n\nresult, err = safe_divide(10, 2)\nif err:\n    print('Error:', err)\nelse:\n    print(result)\n",
    "public class Main {\n    static Integer safeDivide(int a, int b) { return null; }\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    static Integer safeDivide(int a, int b) {
        if (b == 0) throw new RuntimeException("cannot divide by zero");
        return a / b;
    }
    public static void main(String[] args) {
        try { System.out.println(safeDivide(10, 2)); }
        catch (RuntimeException e) { System.out.println("Error: " + e.getMessage()); }
    }
}
""",
)

EX["errors"]["errors_05"] = (
    EX["errors"]["errors_05"][0],
    "def safe_divide(a, b):\n    if b == 0:\n        return None, ValueError('cannot divide by zero')\n    return a // b, None\n\nresult, err = safe_divide(10, 2)\nif err:\n    print('Error:', err)\nelse:\n    print(result)\n",
    EX["errors"]["errors_05"][2],
    """public class Main {
    static Integer safeDivide(int a, int b) {
        if (b == 0) return null;
        return a / b;
    }
    public static void main(String[] args) {
        Integer result = safeDivide(10, 2);
        if (result == null) System.out.println("Error:");
        else System.out.println(result);
    }
}
""",
)

add(
    "errors",
    "errors_06",
    "ERR_NOT_FOUND = Exception('not found')\n",
    'ERR_NOT_FOUND = ValueError("not found")\n\ndef get_item(i):\n    if i < 0:\n        return ERR_NOT_FOUND\n    return "item"\n\nerr = get_item(-1)\nif err is ERR_NOT_FOUND:\n    print("not found")\n',
    "public class Main {\n    static Exception ERR_NOT_FOUND;\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    static final RuntimeException ERR_NOT_FOUND = new RuntimeException("not found");
    static Exception getItem(int id) {
        if (id < 0) return ERR_NOT_FOUND;
        return null;
    }
    public static void main(String[] args) {
        if (getItem(-1) == ERR_NOT_FOUND) System.out.println("not found");
    }
}
""",
)
add(
    "errors",
    "errors_07",
    "ERR_DISK_FULL = ValueError('disk full')\n",
    '''ERR_DISK_FULL = ValueError("disk full")

def read_file(name):
    e = ValueError(f"reading {name}: disk full")
    e.__cause__ = ERR_DISK_FULL
    return e

err = read_file("data.txt")
print(err)
if err.__cause__ is ERR_DISK_FULL:
    print("Disk is full")
''',
    "public class Main {\n    static Exception errDiskFull;\n    static Exception readFile(String name) { return null; }\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    static final Exception errDiskFull = new Exception("disk full");
    static Exception readFile(String name) {
        return new Exception("reading " + name + ": disk full", errDiskFull);
    }
    public static void main(String[] args) {
        Exception err = readFile("data.txt");
        System.out.println(err.getMessage());
        if (err.getCause() == errDiskFull) System.out.println("Disk is full");
    }
}
""",
)

# concurrency
add(
    "concurrency",
    "concurrency_01",
    "import threading\n\ndef say_hello():\n    pass\n\n",
    '''import threading
import time

def say_hello():
    time.sleep(0.05)
    print("Hello!")

print("main done")
t = threading.Thread(target=say_hello)
t.start()
t.join()
''',
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    """import java.util.concurrent.CountDownLatch;

public class Main {
    static void sayHello(CountDownLatch done) {
        try { Thread.sleep(50); } catch (InterruptedException e) {}
        System.out.println("Hello!");
        done.countDown();
    }
    public static void main(String[] args) throws Exception {
        CountDownLatch done = new CountDownLatch(1);
        new Thread(() -> sayHello(done)).start();
        System.out.println("main done");
        done.await();
    }
}
""",
)
add(
    "concurrency",
    "concurrency_02",
    "import queue\nch = queue.Queue()\n",
    """import queue
ch = queue.Queue()

def sender():
    ch.put("ping")

import threading
threading.Thread(target=sender).start()
print(ch.get())
""",
    "import java.util.concurrent.ArrayBlockingQueue;\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    """import java.util.concurrent.ArrayBlockingQueue;

public class Main {
    public static void main(String[] args) throws Exception {
        ArrayBlockingQueue<String> ch = new ArrayBlockingQueue<>(1);
        new Thread(() -> { try { ch.put("ping"); } catch (InterruptedException e) {} }).start();
        System.out.println(ch.take());
    }
}
""",
)
add(
    "concurrency",
    "concurrency_03",
    "import queue\nch = queue.Queue(maxsize=2)\n",
    """import queue
ch = queue.Queue(maxsize=2)
ch.put(10)
ch.put(20)
print(ch.get(), ch.get())
""",
    "import java.util.concurrent.ArrayBlockingQueue;\npublic class Main {\n    public static void main(String[] args) {}\n}\n",
    """import java.util.concurrent.ArrayBlockingQueue;

public class Main {
    public static void main(String[] args) throws Exception {
        ArrayBlockingQueue<Integer> ch = new ArrayBlockingQueue<>(2);
        ch.put(10);
        ch.put(20);
        System.out.println(ch.take() + " " + ch.take());
    }
}
""",
)
add(
    "concurrency",
    "concurrency_04",
    "import queue, threading, time\n",
    """import queue, threading, time

ch1 = queue.Queue()
ch2 = queue.Queue()

def send():
    time.sleep(0.01)
    ch1.put("from ch1")

threading.Thread(target=send).start()
print(ch1.get())
""",
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    """import java.util.concurrent.ArrayBlockingQueue;

public class Main {
    public static void main(String[] args) throws Exception {
        ArrayBlockingQueue<String> ch1 = new ArrayBlockingQueue<>(1);
        new Thread(() -> {
            try { Thread.sleep(10); ch1.put("from ch1"); } catch (InterruptedException e) {}
        }).start();
        System.out.println(ch1.take());
    }
}
""",
)
add(
    "concurrency",
    "concurrency_05",
    "import queue, threading\n",
    """import queue, threading

ch = queue.Queue()

def producer():
    for n in (1, 2, 3):
        ch.put(n)

threading.Thread(target=producer).start()
for _ in range(3):
    print(ch.get())
""",
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    """import java.util.concurrent.ArrayBlockingQueue;

public class Main {
    public static void main(String[] args) throws Exception {
        ArrayBlockingQueue<Integer> ch = new ArrayBlockingQueue<>(3);
        new Thread(() -> { for (int n : new int[]{1,2,3}) try { ch.put(n); } catch (InterruptedException e) {} }).start();
        for (int i = 0; i < 3; i++) System.out.println(ch.take());
    }
}
""",
)
add(
    "concurrency",
    "concurrency_06",
    "import threading\n",
    """import threading

def work(n):
    print(n)

for i in range(1, 4):
    t = threading.Thread(target=work, args=(i,))
    t.start()
    t.join()
print("done")
""",
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    """public class Main {
    public static void main(String[] args) throws Exception {
        for (int i = 1; i <= 3; i++) {
            int n = i;
            Thread t = new Thread(() -> System.out.println(n));
            t.start();
            t.join();
        }
        System.out.println("done");
    }
}
""",
)
add(
    "concurrency",
    "concurrency_07",
    "import queue, threading\n",
    """import queue, threading

ch = queue.Queue(maxsize=2)
done = threading.Barrier(3)

def send(msg):
    ch.put(msg)
    done.wait()

for msg in ("hello", "world"):
    threading.Thread(target=send, args=(msg,)).start()
for _ in range(2):
    print(ch.get())
""",
    "public class Main {\n    public static void main(String[] args) {}\n}\n",
    """import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.CountDownLatch;

public class Main {
    public static void main(String[] args) throws Exception {
        ArrayBlockingQueue<String> ch = new ArrayBlockingQueue<>(2);
        CountDownLatch senders = new CountDownLatch(2);
        Runnable send = () -> {
            try {
                if (Thread.currentThread().getName().endsWith("0")) ch.put("hello");
                else ch.put("world");
            } catch (InterruptedException e) {}
            senders.countDown();
        };
        new Thread(send).start();
        new Thread(send).start();
        senders.await();
        System.out.println(ch.take());
        System.out.println(ch.take());
    }
}
""",
)

EX["concurrency"]["concurrency_07"] = (
    "import queue, threading\n",
    """import queue, threading

ch = queue.Queue(maxsize=2)

def send(msg):
    ch.put(msg)

threading.Thread(target=send, args=("hello",)).start()
threading.Thread(target=send, args=("world",)).start()
print(ch.get())
print(ch.get())
""",
    EX["concurrency"]["concurrency_07"][2],
    """import java.util.concurrent.ArrayBlockingQueue;

public class Main {
    public static void main(String[] args) throws Exception {
        ArrayBlockingQueue<String> ch = new ArrayBlockingQueue<>(2);
        Thread t1 = new Thread(() -> {
            try { ch.put("hello"); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        });
        Thread t2 = new Thread(() -> {
            try { ch.put("world"); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        });
        t1.start();
        t1.join();
        t2.start();
        t2.join();
        System.out.println(ch.take());
        System.out.println(ch.take());
    }
}
""",
)

def nest_java(code: str) -> str:
    """Move top-level types before `public class Main` into Main as nested declarations."""
    marker = "public class Main"
    if marker not in code:
        return code
    before, after = code.split(marker, 1)
    prelude = before.strip()
    if not prelude:
        return code
    imports: list[str] = []
    type_lines: list[str] = []
    for line in prelude.splitlines():
        if line.startswith("import "):
            imports.append(line)
        else:
            type_lines.append(line)
    if not type_lines:
        return code
    indented = "\n".join(("    " + ln if ln.strip() else ln) for ln in type_lines)
    rest = marker + after
    brace = rest.find("{")
    if brace < 0:
        return code
    head = "\n".join(imports)
    if head:
        head += "\n"
    return head + rest[: brace + 1] + "\n" + indented + "\n" + rest[brace + 1 :]


CHAPTER_ORDER = [
    "ownership",
    "functions",
    "arrays",
    "slices",
    "maps",
    "strings",
    "structs",
    "interfaces",
    "methods",
    "packages",
    "pointers",
    "errors",
    "concurrency",
]

HEADER = '''"""Hand-maintained fixes where go_to_native / cs_to_java fail."""

from __future__ import annotations

_OVERRIDE_CHAPTERS = frozenset({
    "ownership",
    "functions",
    "arrays",
    "slices",
    "maps",
    "strings",
    "structs",
    "interfaces",
    "methods",
    "packages",
    "pointers",
    "errors",
    "concurrency",
})


def apply_py_java_overrides(store: dict, emit, body) -> None:
    """Hand-maintained fixes where go_to_native / cs_to_java fail."""
'''

lines = [HEADER]
for ch in CHAPTER_ORDER:
    if ch not in EX:
        continue
    lines.append(f"\n    # {ch}")
    for eid in sorted(EX[ch]):
        ps, pj, js, jj = EX[ch][eid]
        jj = nest_java(jj)
        lines.append(
            f"    emit(store, {ch!r}, {eid!r}, "
            f"python=body({ps!r}, {pj!r}), "
            f"java=body({js!r}, {jj!r}))"
        )

lines.append("\n")
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {sum(len(v) for v in EX.values())} exercises)")
