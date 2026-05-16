"""Expanded chapter theory for selected Rust chapters (thin originals).

Long-form ### sections and ```rust blocks, similar depth to the variables chapter.
"""

from __future__ import annotations

THEORIES: dict[str, str] = {
    "maps": """### Choosing a map

`HashMap<K, V>` is the default unordered map: average *O*(1) lookups assuming a good
hash for `K` and a decent hasher. When you need keys sorted, deterministic iteration,
or BTrees friendly to range queries, prefer `BTreeMap<K, V>`. Exercises that compare
`Debug` output or iterate keys in order almost always pick **`BTreeMap`** even when a
hash map would be faster in production.

Maps own their keys and values unless you store references (`&str` keys with a careful
borrow story, or `Rc<str>`/`Arc<str>` when sharing). For owned strings as keys, `String`
versus `&str` affects who allocates and how long keys live.

### Insert, entry API, and overwriting

`insert` replaces an existing value and returns the old one in an `Option`. The **`entry`**
API avoids double lookups when you want “insert if missing” or “update in place”: it is
idiomatic for frequency counting and memo tables.

```rust
use std::collections::BTreeMap;

let mut scores: BTreeMap<&str, i32> = BTreeMap::new();
scores.insert("Ada", 10);
*scores.entry("Ada").or_insert(0) += 5;
assert_eq!(scores["Ada"], 15);
```

### No nils: use `Option` from `get`

Indexing with `[` panics if the key is missing. **`get`** returns **`Option<&V>`**, which
forces you to handle absence. For parsed configuration or external input, prefer **`get`**
or **`get_mut`** plus explicit error paths rather than silently panicking.
""",
    "strings": """### `&str` versus `String`

`&str` is a borrowed view of UTF-8 bytes somewhere else—stack, heap, or static storage.
`String` is an owned, growable buffer on the heap that **always** holds well-formed UTF-8.
Converting `&str` → `String` allocates (`to_owned`, `to_string`); converting `String` →
`&str` is cheap (`as_str`, deref coercion).

Because `String` owns data, you can mutate the buffer (`push`, `push_str`, `clear`) while
holding no other owners. Shared references (`&str`) forbid mutation; use `&mut str` rarely
and only when you already have unique access to some UTF-8 buffer.

### Iteration, slicing, and grapheme caveats

Rust strings index by **byte offset**, not character index. Slicing at arbitrary `usize`
values can panic if you split a multibyte UTF-8 sequence. Iterating **`chars()`** yields
Unicode scalar values, not full grapheme clusters—fine for many exercises, not for every
human-language editing scenario.

```rust
let s = String::from("café");
assert_eq!(s.len(), 5); // 'é' is two bytes in UTF-8

let prefix: &str = &s[..3]; // "caf"
// let bad = &s[..4]; // may panic: cuts inside 'é'
```

### Building and formatting

Use `format!` for interpolation, `push_str` in hot loops when you know capacity upfront,
and `with_capacity` when you can predict output size—`String` can amortize growth, but
avoid repeated reallocations inside tight loops when profiling says it matters.
""",
    "structs": """### Named product types

`struct` bundles fields with names, giving you nominal typing: two structs with identical
layouts are still different types unless you relate them intentionally. Field order
determines memory layout together with **`repr`** attributes; the default Rust layout is
optimized and not stable for FFI unless you opt into **`#[repr(C)]`**.

Update syntax (`let q = Point { x: 1, ..p }`) copies unchanged fields from an existing
value and is ideal for large configurations with one tweak—the compiler still moves or
copies per field rules.

### Visibility and constructors

Associated functions `fn new(...) -> Self` are convention, not magic: `Self` refers to
the implementing type. Combine with **`pub`** on fields selectively to hide invariants—
a private field plus public accessors prevents callers from putting an enum into an
impossible state.

```rust
pub struct Counter(i32);

impl Counter {
    pub fn new() -> Self { Counter(0) }
    pub fn bump(&mut self) { self.0 += 1 }
    pub fn get(&self) -> i32 { self.0 }
}
```

### Derives and manual impls

`#[derive(Debug, Clone, Copy, PartialEq, Eq)]` covers most tutorial structs. Reach for
manual `PartialEq` when equality should ignore cache fields or round FP differently.
Remember: `Copy` is shallow bitwise duplication—only sensible for small, `Copy`-safe fields.
""",
    "interfaces": """### Traits: shared behavior, not inheritance

Traits describe **what you can do** with a type: methods, associated types, and optional
default bodies. They are closer to **Java interfaces** than to subclassing: you implement
them explicitly (`impl Trait for Type`) or blanketingly (`impl Trait for T where ...`).

Dynamic dispatch (`dyn Trait`) carries a vtable pointer (`dyn Trait` behind `&`/`Box`).
Static dispatch (`impl Trait` in argument position, generics) monomorphizes—faster, bigger
binary. Choose `dyn` when you genuinely need heterogeneous collections of behaviors.

```rust
trait Area {
    fn area(&self) -> f64;
}

struct Circle { r: f64 }
impl Area for Circle {
    fn area(&self) -> f64 { std::f64::consts::PI * self.r * self.r }
}

fn print_area(s: &dyn Area) {
    println!("{}", s.area());
}
```

### Coherence and orphan rules

You may not implement foreign traits for foreign types—Rust’s **orphan rule** keeps trait
resolution predictable. Newtypes (`struct Meters(f64);`) unlock useful impls locally while
preserving type safety.

### Common standard traits

`Clone`, `Copy`, `Debug`, `PartialEq`, `Eq`, `Hash`, `Default`, and `Iterator` appear daily.
Understanding which ones imply bounds on generic parameters (`T: Clone`) prevents sprawling
`where` clauses when composing structs.
""",
    "methods": """### `self`, `&self`, `&mut self`

Methods are functions in an `impl` block whose first parameter is `self`. Taking **`self`**
by value consumes the receiver—use for builders or finalizing transitions. **`&self`**
borrows immutably; **`&mut self`** allows in-place field mutation without moving the outer value.

Rust automatically borrows when you use dot syntax: `s.len()` becomes `(&s).len()` when
`len` expects `&self`. This ergonomics layer is why method chains look fluent even when
ownership is strict underneath.

### Inherent vs trait methods

Inherent methods live directly on the type. Trait methods arrive via scope: explicit
`Trait::method(&x)` disambiguates when name clashes occur. UFCS (universal function call
syntax) is your friend when the compiler’s pick surprises.

```rust
struct Rect { w: f64, h: f64 }

impl Rect {
    fn area(&self) -> f64 { self.w * self.h }
    fn scale(&mut self, k: f64) {
        self.w *= k;
        self.h *= k;
    }
}
```

### Builder patterns and privacy

Method-heavy APIs often pair `pub fn new` with private fields so only approved transitions
run—`mut` access cannot bypass module privacy. That combination is how small structs still
enforce large invariants.
""",
    "packages": """### Crates, editions, and modules

A **crate** is the unit the compiler builds: binary (`main`) or library (`lib`). **Editions**
(`2018`, `2021`, …) gate syntax and prelude tweaks without breaking old code. Within a
crate, **`mod`** declares modules; filesystem modules mirror directory trees when you use
`mod child;` with `src/child.rs` or `src/child/mod.rs`.

Visibility flows with `pub`, `pub(crate)`, `pub(super)`, and `pub(in path)`. Default is
private to the parent module—leak only what should form your API surface.

### Paths and `use`

Absolute paths start at the crate root (`crate::foo`) or extern crates (`::serde` historically,
now mostly subsumed by `use`). The **`use`** tree rebinds names for call sites; **`pub use`**
re-exports for ergonomic facades (`pub use inner::Thing` from a `prelude` module).

```rust
// src/lib.rs
mod parser;
pub use parser::parse;

mod parser {
    pub fn parse(input: &str) -> Vec<&str> {
        input.split_whitespace().collect()
    }
}
```

### `Cargo.toml` matters

Dependencies, features, and workspace membership live in **`Cargo.toml`**. Features let
you toggle optional integrations (`serde`, `async`) without forking the crate. Lockfiles
`Cargo.lock` pin versions for binaries; libraries leave resolution to dependents—know which
side of that line your project sits on.
""",
    "pointers": """### References are proven pointers

Safe Rust references (`&T`, `&mut T`) compile down to pointers, but the borrow checker
erases use-after-free and iterator invalidation at compile time. Raw pointers (`*const T`,
`*mut T`) reappear in FFI, intrusive structures, and performance-critical code where you
duplicate the compiler’s reasoning manually inside **`unsafe`** blocks.

The `*` operator dereferences references; with raw pointers you need `unsafe` unless you
are only passing them through to other unsafe operations.

### Boxes and the heap

`Box<T>` allocates `T` on the heap and frees it deterministically when the box drops—no
GC, no manual `free`. Thin `Box` is one word wide; fat pointers (`dyn Trait`, slices)
carry metadata alongside the address.

```rust
let mut p = Box::new(41);
*p += 1;
assert_eq!(*p, 42);
```

### Interior mutability patterns

Sometimes you need mutation through a shared `&` reference (`Rc<RefCell<T>>`, `Mutex<T>`,
`Atomic*`). These types move checks from compile time to runtime or atomics—reachable when
building graphs or caching but easy to misuse if you forget re-entrancy or deadlocks.

### References vs slices

A slice `&[T]` is a “pointer + length” pair mirroring `fat pointers`; strings mirror the
same with UTF-8 validity. Knowing this explains why slicing and borrowing interact the way
they do in APIs.
""",
    "concurrency": """### Threads and ownership transfers

`std::thread::spawn` takes a closure that must be `'static`—it cannot borrow stack locals
unless you `scope` joining threads. Ownership of data crosses thread boundaries with **`Send`**:
types that are not `Send` (like `Rc` guarded references) cannot move to another thread
safely.

Message passing with channels (`std::sync::mpsc`) moves ownership of values to receivers,
which sidesteps shared mutable state by construction. **`Arc<Mutex<T>>`** is the bread-and-
butter shared mutable pattern; prefer finer-grained locks when contention shows up in profiles.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..4 {
    let c = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        let mut n = c.lock().unwrap();
        *n += 1;
    }));
}

for h in handles { h.join().unwrap(); }
assert_eq!(*counter.lock().unwrap(), 4);
```

### Atomics and ordering

`Atomic*` in `std::sync::atomic` provides lock-free counters and flags when used carefully.
Memory orderings (`Relaxed`, `Acquire`, `Release`, `AcqRel`, `SeqCst`) dictate which writes
threads observe; **`SeqCst`** is the slowest but simplest mental model when learning.

### Async note

`async`/`await` schedules work on executors; it is cooperative concurrency layered atop OS
threads or runtimes. This course’s `std::thread` material is still foundational: executors
eventually park real threads and shuffle tasks much like channels shuffle messages.
""",
    "testing": """### Built-in test harness

`cargo test` compiles functions annotated with **`#[test]`** into a separate binary. Assertions
(`assert!`, `assert_eq!`, `debug_assert!`) panic on failure; the harness catches panics and
reports them as failing tests. **`#[should_panic]`** documents expected failures—use sparingly
and prefer checking error values when semantics allow.

Integration tests live in `tests/*.rs`, compiled as separate crates against your library,
exercising the **public** API. Unit tests inline in `src` files behind `mod tests` keep helpers
private and fast.

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adds() {
        assert_eq!(add(2, 2), 4);
    }
}
```

### Fixtures, determinism, and `#[ignore]`

Heavy tests can be marked **`#[ignore]`** for selective runs (`cargo test -- --ignored`).
Seed random number generators, freeze clocks with injected times, and avoid network reliance
unless you gate those tests behind features—CI should be reproducible.

### Property-based and snapshot testing

Crates like `proptest` or `quickcheck` generate inputs; `insta` captures structured snapshots.
They catch edge cases `assert_eq!` might never think of—but good shrinking and readable
failures matter more than raw case volume.
""",
}
