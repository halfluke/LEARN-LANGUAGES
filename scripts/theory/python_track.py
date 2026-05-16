"""Chapter theory copy for the Python learning track.

Strings are Markdown-ish: use ### headings and fenced ```python blocks.
"""

from __future__ import annotations

THEORIES: dict[str, str] = {
    "variables": """### Names and assignment

In Python, variables are **names** bound to objects. Assignment (`=`) attaches a
label to a value already sitting in memory rather than carving out a separately
managed memory slot by name alone. The same object can have multiple names, and rebinding
one name never magically changes another name unless you mutate a shared mutable
object through one of those names.

### What to internalize early

Use descriptive snake_case names. Use plain `=` for assignment; the walrus operator
(`:=`) belongs inside expressions (for example `if (n := len(items)) > 0:`). Constants-by-convention use
`SCREAMING_SNAKE_CASE` but remain mutable unless you freeze them (for example with
immutable types like `tuple` or `frozenset`).

```python
items = [1, 2, 3]
alias = items
alias.append(4)
assert items == [1, 2, 3, 4]  # same list object

x = y = []
x.append(1)
assert y == [1]
```
""",
    "ownership": """### Objects, references, and lifetime

Python manages memory with reference counting plus a cycle-breaking collector.
There is no manual free/dispose step and no compile-time ownership checker: an
object lives while something still references it. Thinking in terms of **who
references what** helps you predict aliasing bugs and when large graphs stay alive.

### Copies versus views

Assignment shares references. For independent containers, prefer explicit copying
strategies (`list(...)`, `dict.copy()`, `copy.copy` / `copy.deepcopy`) instead of
assuming independence. Immutable objects (`int`, `str`, `tuple` of immutables)
are safely shared and cheap to pass around.

```python
import copy

original = {"nums": [1, 2]}
shallow = original.copy()
shallow["nums"].append(3)
assert original["nums"] == [1, 2, 3]

deep = copy.deepcopy(original)
deep["nums"].append(99)
assert original["nums"] == [1, 2, 3]
```
""",
    "controlflow": """### Conditionals and loops

`if` / `elif` / `else` evaluate truthiness (`bool(x)`). Loops are `for name in
iterable` (preferred) and `while condition`. `break` exits the nearest loop;
`continue` jumps to the next iteration. The optional `else` clause on a loop runs
only if the loop finishes **without** `break`—handy for search patterns.

### Structural pattern matching

Python 3.10+ adds `match` / `case` for branching on shape and structure. It shines
with dataclasses, tuples, and nested structures. Prefer readability: reach for `if`
when the logic is a simple predicate.

```python
for n in range(2, 20):
    for x in range(2, n):
        if n % x == 0:
            break
    else:
        print(n, "is prime-ish candidate")

match {"kind": "point", "x": 3, "y": 4}:
    case {"kind": "point", "x": x, "y": y}:
        print(x + y)
```
""",
    "functions": """### Defining behavior

Functions are first-class objects created with `def`. Type annotations document
intent (`def greet(name: str) -> str:`) but are not enforced at runtime unless you
add a separate checker. Default arguments are evaluated **once** at function
definition time—never use mutable defaults (`def bad(items=[])`); use `None` and
allocate inside the body.

### Flexible signatures

`*args` collects positional extras into a tuple; `**kwargs` collects keyword extras
into a dict. Use `/` and `*` in the parameter list to control positional-only vs
keyword-only arguments when designing stable APIs.

```python
def append_suffix(base: str, *, suffix: str = "!") -> str:
    return base + suffix


def summarize(title: str, *scores: int, **meta: str) -> dict[str, object]:
    return {"title": title, "scores": scores, "meta": meta}
```
""",
    "arrays": """### Lists as growable sequences

The built-in `list` is the everyday “dynamic array”: indexed, ordered, and
heterogeneous if you want (though homogeneous lists are easier to reason about).
Amortized `append` makes building sequences in a loop natural. For numeric arrays
with fixed machine types, the standard library offers `array.array`; for heavy
numerics you typically reach for third-party libraries.

### Practical idioms

List comprehensions and generator expressions express transformations clearly.
Prefer them over `map`/`filter` when readability wins. Sorting is stable:
`sorted(iterable, key=...)` returns a new list; `.sort()` sorts in place.

```python
squares = [n * n for n in range(10) if n % 2 == 0]
coords = [(x, y) for x in range(3) for y in range(3)]

rows = [["z", "b"], ["y", "a"]]
rows.sort(key=lambda r: r[1])
assert rows == [["y", "a"], ["z", "b"]]
```
""",
    "slices": """### Slice objects

Slicing uses `[start:stop:step]` with half-open intervals: `stop` is exclusive.
Omitted bounds default to sequence ends; negative indices count from the right.
A slice returns a **new** shallow copy for lists; for strings and tuples you always
get new immutable sequences sharing elements.

### Advanced usage

`slice(start, stop, step)` objects can be reused. For multidimensional numeric work,
libraries layer richer slicing; for plain Python, compose nested indexing manually.

```python
nums = list(range(10))
assert nums[2:8:2] == [2, 4, 6]
assert nums[::-1] == list(reversed(nums))

title = "reference"
assert title[::2] == "rfec"
```
""",
    "maps": """### Dictionaries as the core mapping

`dict` stores key→value pairs with fast lookup. Keys must be hashable (immutable
and comparable predictably). Insertion order is preserved (Python 3.7+ language
guarantee). Use dict comprehensions and unpacking merges (`{**a, **b}` or `a | b`
on 3.9+) for concise joins.

### Patterns that scale

`collections.Counter`, `defaultdict`, and `ChainMap` extend mapping workflows.
Prefer `.get` or membership tests instead of catching `KeyError` when absence is
normal control flow—reserve exceptions for truly exceptional cases.

```python
counts = {c: "aeiou".count(c) for c in "sequoia"}
merged = {"x": 1} | {"y": 2}

from collections import defaultdict

dd = defaultdict(list)
dd["k"].append(1)
```
""",
    "strings": """### Text as immutable sequences

`str` holds Unicode code points; normalize encoding concerns at I/O boundaries
(decode bytes early, encode late). Strings are immutable: “changing” one builds a
new object. `str.join` is the idiomatic way to concatenate many fragments without
quadratic copies.

### Formatting

f-strings (`f"{value:!r}"`) are the default readability win. `str.format` and
`Template` remain useful for localization pipelines or user-supplied patterns where
you want different safety trade-offs.

```python
parts = ["hydro", "electric"]
label = "-".join(parts)

ratio = 0.125
assert f"{ratio:.1%}" == "12.5%"
```
""",
    "structs": """### Modeling records cleanly

Plain classes work, but **dataclasses** (`@dataclass`) generate `__init__`,
repr, comparisons, and more—perfect for simple aggregates. For lightweight,
immutable tuples with named fields, use `typing.NamedTuple`. When modeling dict
shapes with known keys, `typing.TypedDict` bridges structured dict literals and
static checking.

### Defaults and mutability

Dataclass field defaults follow the same rule as functions: never put mutable
defaults directly in the field list—use `field(default_factory=list)` instead.

```python
from dataclasses import dataclass, field


@dataclass(slots=True)
class Profile:
    handle: str
    tags: list[str] = field(default_factory=list)


p = Profile("neo")
p.tags.append("learners")
```
""",
    "interfaces": """### Protocols and duck typing

Python culture favors **duck typing**: if an object exposes the methods you need,
you can use it without requiring a shared base class. For static checks,
`typing.Protocol` describes structural interfaces—anything matching the required
methods is compatible without inheritance.

### Abstract Base Classes

`collections.abc` provides ABCs (`Iterable`, `Mapping`, `MutableSequence`) that
document intent and provide mixin helpers. Use ABCs when you want inheritance-based
contracts; use Protocols when you want structural composition.

```python
from typing import Protocol


class Drawable(Protocol):
    def draw(self) -> None: ...


def render(items: list[Drawable]) -> None:
    for item in items:
        item.draw()
```
""",
    "methods": """### Binding behavior to objects

Instance methods take `self` implicitly when accessed through an instance.
**Class methods** (`@classmethod`) receive the class object as `cls`; **static
methods** (`@staticmethod`) are ordinary functions namespaced on the class. Prefer
classmethods for alternate constructors.

### Calling conventions

You can also retrieve functions unbound from the class and pass instances
explicitly—useful in rare metaprogramming scenarios—but idiomatic code sticks to
normal dotted calls.

```python
class Bucket:
    def __init__(self, limit: int) -> None:
        self.limit = limit

    @classmethod
    def tiny(cls) -> "Bucket":
        return cls(3)


b = Bucket.tiny()
assert isinstance(b, Bucket)
```
""",
    "packages": """### Modules and import paths

Each `.py` file is typically a **module**; directories become **packages** when
they include `__package__` metadata—often via `__init__.py` (still recommended for
namespace clarity). Imports bind names to modules or symbols (`from pkg import util`
vs `import pkg.util`). Prefer absolute imports inside packages; relative imports
(`.sub`) work within package hierarchies.

### Public surfaces

Leading underscore (`_helper`) signals “internal by convention.” `__all__` in
`__init__.py` documents exports when `from pkg import *` matters—avoid star-imports
in application code.

```python
# example/layout.py — illustrative only
CONFIG = {"debug": True}


def load():
    return CONFIG.copy()
```
""",
    "pointers": """### References without pointer syntax

Python hides addresses behind references. Use `id(obj)` when you need identity,
and `is` (not `==`) to test whether two names refer to the **same** object.
Small integers and interned strings may be cached—do not rely on accidental
identity for equality logic.

### Mutability pitfalls

Mutable defaults and shared containers are the usual footguns. Immutable objects
(numbers, strings, tuples of immutables) hash safely and behave like values for
dict keys and set membership.

```python
a = []
b = a
assert a is b

x = 256
y = 256
assert x is y  # CPython may intern small ints — do not depend on this casually

t1 = (1, "ok")
t2 = (1, "ok")
assert t1 is not t2 and t1 == t2
```
""",
    "errors": """### Exceptions as control flow signals

Python uses exceptions for errors **and** for benign sentinel patterns (`StopIteration`,
`StopAsyncIteration`). Prefer specific exceptions (`ValueError`, `KeyError`,
`TypeError`) over bare `Exception`. `try` / `except` / `else` / `finally` structures
cleanup clearly: `else` runs when no exception occurs in `try`; `finally` always runs.

### Raising and chaining

`raise RuntimeError("bad") from original` preserves context. Custom exceptions are
ordinary classes—usually inherit from `Exception`, not `BaseException` (reserved for
system exits and keyboard interrupts).

```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("b must be non-zero")
    return a / b


try:
    divide(1, 0)
except ZeroDivisionError as err:
    recovered = f"handled: {err}"
```
""",
    "concurrency": """### Threads, asyncio, and processes

The standard library offers three major styles: `threading` for blocking I/O with
shared interpreter state (subject to the GIL for CPU-bound Python bytecode),
`asyncio` for cooperative multitasking with explicit `await` points, and
`multiprocessing` for parallel CPU work across processes. Pick the model that matches
your bottleneck: I/O wait vs CPU saturation vs isolation.

### Safety primitives

Use `queue.Queue` for cross-thread work queues; prefer immutable messages or clear
ownership transfers for shared data. For asyncio, avoid blocking calls inside tasks;
delegate blocking sections to executors.

```python
import asyncio


async def gather_squares(nums: list[int]) -> list[int]:
    async def sq(n: int) -> int:
        await asyncio.sleep(0)  # yield control cooperatively
        return n * n

    return list(await asyncio.gather(*(sq(n) for n in nums)))
```
""",
    "testing": """### Automated checks as executable specs

`unittest` ships in the standard library with classes and assertions; many teams
prefer **pytest** for plain functions and fixtures. Structure tests around behavior:
Arrange inputs, Act on the code under test, Assert expected outputs or exceptions.

### Fixtures and parametrization

Pytest fixtures inject dependencies cleanly; `@pytest.mark.parametrize` fights
copy-paste when scenarios differ only by data. Keep tests deterministic—mock time,
randomness, and network boundaries when needed.

```python
import pytest


def odds_only(nums: list[int]) -> list[int]:
    return [n for n in nums if n % 2]


@pytest.mark.parametrize(
    "nums,expected",
    [
        ([1, 2, 3], [1, 3]),
        ([], []),
    ],
)
def test_odds_only(nums: list[int], expected: list[int]) -> None:
    assert odds_only(nums) == expected
```
""",
    "json": """### Serialization with `json`

The `json` module converts JSON text to Python objects (`object_hook` optional) and
back (`default` for non-JSON-native types). JSON maps become dicts; arrays become
lists; strings stay `str`; numbers become `int` or `float`; booleans and `null`
map to `True`, `False`, and `None`.

### Practical cautions

Floating-point JSON numbers may surprise you; decimals are not native in JSON.
Pretty-print with `indent=` for human-readable dumps. Never parse untrusted JSON
with dangerous custom hooks—treat deserialization as input validation.

```python
import json

payload = {"count": 3, "tags": ["alpha", "omega"]}
text = json.dumps(payload, sort_keys=True)
roundtrip = json.loads(text)
assert roundtrip == payload
```
""",
    "time": """### Clocks and calendars

`datetime.datetime` models civil date/time; combine `timezone.utc` or `zoneinfo`
for aware timestamps—avoid “naive” datetimes when crossing DST or UTC boundaries.
For monotonic timers (measuring elapsed intervals), use `time.monotonic()`, not
wall-clock functions.

### Parsing and formatting

`strftime` / `strptime` patterns round-trip textual representations. ISO 8601 helpers
like `datetime.fromisoformat` simplify logs interchange.

```python
from datetime import datetime, timedelta, timezone


launch = datetime(1969, 7, 20, 20, 17, tzinfo=timezone.utc)
touchdown = launch + timedelta(hours=2, minutes=31)

assert touchdown.strftime("%Y-%m-%d") == "1969-07-21"
```
""",
}
