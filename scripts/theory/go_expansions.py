"""Expanded chapter theory for selected Go chapters."""

from __future__ import annotations

THEORIES: dict[str, str] = {
    "ownership": """### Values, assignment, and what “copy” means

Go is garbage-collected: there is no manual `free` and no compile-time borrow checker like
Rust’s. Still, you must understand **what assignment copies**. Small scalars (`int`, `float64`,
`bool`, pointers themselves) copy by value in a straightforward way. Structs copy **fieldwise**
when assigned—if every field is copyable, the whole struct is copyable; if a field contains
a slice header, map reference, or pointer, you copy the header or address, not necessarily
the deep data they point at.

That distinction is why the language borrows “ownership” language informally: **aliasing**
is common and intentional. Two `[]byte` variables may share one backing array; two map
variables observe one underlying hash table unless you reassign after `make`. Passing a
value to a function copies the top-level bits; passing a pointer shares one object across
callers—exactly the choice between value and pointer receivers for methods.

### `string`: immutable bytes behind a small header

A `string` is a read-only view of bytes managed by the runtime. Rebinding `s := t` copies
the string header (pointer + length), not the bytes. Converting `[]byte` ↔ `string` may copy
when the compiler cannot prove exclusivity—treat conversions as potentially allocating when
reasoning about performance-sensitive paths.

### Slices and maps: headers you copy, storage you share

Slices are triples (pointer, length, capacity) over a backing array. Assigning `t := s` lets
both names observe the same elements; mutating `t[i]` visible through `s` is expected, not
a bug. Appending can copy if capacity is exceeded—if you need independence, `copy` into a
fresh slice or index distinct arrays.

Maps behave like reference types: copying a `map` variable duplicates the **descriptor** that
points at shared runtime storage, not the logical key/value store. A `nil` map differs from
an empty `make` map: reads panic on `nil`, while `make` returns an initialized structure you
can grow.

```go
s := []int{1, 2}
t := s
t[0] = 9 // s[0] is now 9: shared backing array

m := map[string]int{"a": 1}
n := m
n["a"] = 2 // m["a"] is 2: one map table behind both vars
```

### Practical takeaway for APIs

Prefer pointers when a value is large, you must mutate through layers, or you want `nil` to
signal absence (`*User` versus a zero-valued `User`). Prefer values for tiny, immutable
config structs where copies are cheap and clarify thread-local independence. The garbage
collector reclaims unreachable graphs, but **reachability** still follows references—holding
a slice that retains a huge backing array keeps all of it alive until nothing points at it.
""",
}
