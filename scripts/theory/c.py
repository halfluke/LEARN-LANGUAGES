THEORIES: dict[str, str] = {
    "variables": """### Declarations and types

In C, every variable has a static type known at compile time. You declare a name, give it a type, and optionally initialize it. The language provides integer types of different widths (`char`, `short`, `int`, `long`, `long long`, each with signed and unsigned variants), floating types (`float`, `double`, `long double`), enumeration types, and derived types such as pointers, arrays, structures, and unions. Local variables typically live in automatic storage on the stack; file-scope and `static` locals have static storage duration and are zero-initialized if you omit an initializer.

Initialization rules reward clarity: scalars can be set with `= value`, while compound literals and designated initializers (C99) let you build structs and arrays readably. Understand integer promotions and the usual arithmetic conversions—mixing narrow types with `int` can surprise you when values widen silently in expressions. Use explicit casts when you intentionally narrow a value or reinterpret bits.

### Storage, scope, and linkage

Scope determines where an identifier is visible: block scope inside `{}`, file scope for globals, and prototype scope for parameters in declarations. Linkage (`static` at file scope, `extern`, or none) controls whether multiple translation units share one object or each gets a private copy. Automatic variables are created on block entry and destroyed on exit; `static` locals persist but remain private to their function.

### Practical habits

Prefer `const` for data that must not change after initialization. Use fixed-width types from `<stdint.h>` when you need exact sizes for protocols or binary formats. For string-like data held in buffers, track both capacity and length—C does not bundle them for you.

```c
#include <stdint.h>

int main(void) {
    const uint32_t magic = 0xdeadbeef;
    unsigned char buf[256] = {0};
    (void)buf;
    (void)magic;
    return 0;
}
```
""",
    "ownership": """### Responsibility without a checker

C has no ownership or borrow checker. You—the programmer—decide who allocates memory, who may access it, and who must free it. A pointer is merely an address; the compiler does not verify that it remains valid. That makes discipline essential: establish clear conventions for “caller allocates / callee fills” versus “callee allocates / caller frees,” and document lifetimes in function comments when the protocol is non-obvious.

Stack allocation is cheap and automatic: arrays and structs with automatic storage vanish when the block ends. Heap allocation via `malloc`, `calloc`, and `realloc` from `<stdlib.h>` survives until `free` is called; forgetting to free causes leaks, double-free is undefined behavior, and use-after-free is a classic security and stability bug.

### Patterns that scale

To mimic “single owner,” pair every successful `malloc` with exactly one `free` on all code paths—use early returns carefully and consider a single cleanup label at the bottom of functions for complex control flow. When multiple parts of a program need read-only access, share `const` pointers; when mutation must be coordinated, serialize access with mutexes or clear thread roles. Resource Acquisition Is Initialization (RAII) is not built in, but you can approximate it with careful struct lifetimes and init/destroy function pairs.

### Debugging ownership issues

Tools such as Valgrind, AddressSanitizer (ASan), and LeakSanitizer catch many heap mistakes at runtime. Defensive coding—initializing pointers to `NULL`, null-checking before dereference, and zeroing freed pointers in long-lived structures—reduces accidental reuse.

```c
#include <stdlib.h>

void example(void) {
    int *p = malloc(sizeof *p * 4);
    if (!p) return;
    p[0] = 1;
    free(p);
    p = NULL;
}
```
""",
    "controlflow": """### Selection and repetition

Control flow in C is intentionally small: `if` / `else`, `switch` (with `case` labels and `break` or fall-through), `while`, `do`/`while`, and `for`. The `for` loop bundles initialization, test, and step—ideal for iterating with an index. The comma operator is legal but easy to abuse; reserve it for idiomatic patterns like multiple assignments in a `for` header.

`switch` works on integer expressions; each `case` must be a compile-time constant. Forgetting `break` continues into the next case—sometimes intentional (grouping cases), often a bug. `default` handles unmatched values and is good defensive style. Be cautious comparing signed and unsigned values: usual conversions can invert comparisons.

### Jumping with purpose

`goto` is not evil in C: it can consolidate cleanup on shared exit paths in kernel-like code or parsers. `continue` skips to the next loop iteration; `break` exits the innermost `switch` or loop. `return` leaves the current function, optionally with a value. Setjmp/longjmp from `<setjmp.h>` implements non-local jumps—powerful and easy to misuse, so treat them as advanced.

### Example: structured iteration

```c
#include <stdio.h>

int main(void) {
    for (int i = 0; i < 3; ++i) {
        if (i == 1) continue;
        printf("%d\\n", i);
    }
    return 0;
}
```
""",
    "functions": """### Declarations, definitions, and linkage

Functions are the primary unit of reuse. A declaration (prototype) tells the compiler the name, return type, and parameter types so calls type-check before the definition is seen. The definition supplies the body. At file scope, `static` functions are private to the translation unit; non-`static` functions have external linkage and can be called from other object files if linked together.

The execution environment starts in `main`; hosted implementations accept `int main(void)` or `int main(int argc, char *argv[])`. Parameters are passed by value: structs are copied unless you pass pointers. For “output” parameters, callers pass addresses. Variadic functions (`printf` style) use `<stdarg.h>`; the callee must know types through a fixed argument or format string—there is no type-safe varargs in C.

### Inlining and optimization

`inline` (C99) is a hint; the definition often lives in a header if you need the compiler to inline across translation units (with `static inline` or `extern inline` patterns depending on your toolchain rules). `restrict` (C99) promises non-aliasing through particular pointers, enabling stronger optimizations—only use it when you can prove aliasing does not occur.

```c
#include <stdio.h>

static int add(int a, int b) { return a + b; }

int main(void) {
    printf("%d\\n", add(2, 3));
    return 0;
}
```
""",
    "arrays": """### Fixed buffers and rank

Array types have compile-time size (except VLAs in C99, which are optional in later standards for freestanding use) or runtime size on the stack as a VLA where supported. The name of an array in most expressions “decays” to a pointer to its first element; `sizeof` on the array object still yields total bytes. Multidimensional arrays are row-major: `int m[3][4]` stores four `int`s per row.

### Indexing and bounds

C does not check array bounds at runtime by default. Out-of-bounds access is undefined behavior—silent corruption, crashes, or exploitable vulnerabilities. Always tie indices to sizes stored in `size_t` and compare carefully with unsigned semantics. For dynamic sizes, either use VLAs where appropriate or allocate a 1D buffer and index manually with `row * width + col`.

### Passing arrays to functions

Function parameters written as `int a[]` or `int *a` are equivalent at the first dimension—both are pointer types. Specify the leading dimensions for multi-dimensional arrays so the compiler can compute addresses: `void f(int a[3][4]);`.

```c
#include <stdio.h>

int main(void) {
    int xs[4] = {1, 2, 3, 4};
    for (size_t i = 0; i < sizeof xs / sizeof xs[0]; ++i) {
        printf("%d ", xs[i]);
    }
    putchar('\\n');
    return 0;
}
```
""",
    "slices": """### Pointer-length pairs

C has no built-in slice type. The idiomatic stand-in is a pointer to the first element together with a length (often `size_t`) or a pointer one past the last valid element. This pattern appears in APIs that must view a substring of a buffer without copying, or when parsing protocols. The length prevents silent overruns when discipline is maintained—callers must not lie about extents.

### Functions over ranges

Standard library functions such as `memcpy`, `memmove`, `memcmp`, and `memset` take a byte count. String functions like `strncmp` stop at `n` characters or the first `\\0`. Prefer these when you have explicit sizes; unbounded `strcpy` is dangerous on untrusted input. When you expose a “slice” in your own API, document whether the range is `[start, count)` or `[first, last)`.

### Safer iteration

Loop with indices bounded by the recorded length, or maintain `const unsigned char *cur` and `const unsigned char *end`. This mirrors iterators in other languages but stays explicit in C.

```c
#include <stddef.h>
#include <stdio.h>

void print_ints(const int *base, size_t n) {
    for (size_t i = 0; i < n; ++i) {
        printf("%d ", base[i]);
    }
}
```
""",
    "maps": """### No built-in table

The C standard library does not provide associative containers. You implement key–value maps with data structures (hash tables with separate chaining or open addressing; balanced trees for ordered maps) or you embed a mature library such as khash, uthash, or similar when licensing fits your project. Keys are often strings (`char *` with `strcmp`) or integers; values can be `void *` with type discipline enforced by convention.

### Hashing and equality

For hash maps you need a hash function (djb2, FNV, xxHash for speed—not cryptographically secure), an equality predicate, and a policy for resizing when load factor grows. Collisions are inevitable—your chaining or probing strategy defines performance. For small fixed universes, a flat table with linear search often suffices without hashing.

### Practical API shape

Typical operations are `insert`, `lookup`, `remove`, and optionally `foreach`. Store `struct entry { const char *key; void *value; }` for string keys, or wrap opaque handles if you need stable pointers across reallocation of backing storage.

```c
#include <stddef.h>
#include <string.h>

/* Map-like lookup in a tiny static table of string keys */
typedef struct { const char *k; int v; } pair_t;

int lookup(const pair_t *tab, size_t n, const char *key) {
    for (size_t i = 0; i < n; ++i) {
        if (strcmp(tab[i].k, key) == 0) return tab[i].v;
    }
    return -1;
}
```
""",
    "strings": """### Null-terminated byte strings

C strings are sequences of `char` ending at the first `\\0` byte. The standard library in `<string.h>` provides `strlen`, `strcmp`, `strncmp`, `strchr`, `strstr`, and more. Because length is implicit, overrunning a buffer while copying is a chronic bug—always know destination capacity. Prefer `strncpy` only if you understand its padding semantics; `snprintf` into a buffer is often clearer for bounded string building.

### Wide and multibyte text

For international text, `<wchar.h>` and `<uchar.h>` add wide and UTF-8/UTF-16/UTF-32 utilities, but `char` strings remain the default. Treat external text as UTF-8 is common on modern POSIX systems; still validate and normalize when security matters. Do not confuse byte counts with character counts in Unicode.

### Copying and formatting

`memcpy` copies raw bytes; `memmove` handles overlapping regions safely. For formatted output use `printf` family with correct format specifiers (`%zu` for `size_t`, `PRIu32` macros from `<inttypes.h>` for fixed integers). Read input with `fgets` for line-oriented data rather than unbounded `scanf` into fixed stacks.

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char dst[32];
    const char *src = "hello";
    snprintf(dst, sizeof dst, "%s world", src);
    printf("%zu\\n", strlen(dst));
    return 0;
}
```
""",
    "structs": """### Aggregating data

`struct` groups named members with defined layout (order matters). Access members with `.` for values and `->` through pointers. Anonymous structs and unions (C11) can simplify nested layouts when supported. Padding between members is inserted for alignment—`sizeof` can exceed the sum of member sizes. Use `#pragma pack` or compiler attributes sparingly and only for binary protocols; misaligned access can be slow or invalid on some architectures.

### Typedef and opaque types

`typedef` creates aliases for struct types, improving readability (`typedef struct Node Node;`). Opaque pointers (`typedef struct Impl Impl;` with only forward declaration in headers) hide implementation details across modules—clients call functions you supply to construct and destroy values.

### Bit-fields and unions

Bit-fields pack small flags into integers with implementation-defined layout—fine for hardware registers when documented. Unions share storage; writing one member and reading another is type-punning with strict aliasing rules—use `memcpy` for safe reinterpretation of object representations when needed.

```c
#include <stdio.h>

typedef struct {
    double x;
    double y;
} point_t;

int main(void) {
    point_t p = {.x = 1.0, .y = 2.0};
    printf("%g %g\\n", p.x, p.y);
    return 0;
}
```
""",
    "interfaces": """### Contracts via function pointers

C does not have interfaces in the language sense, but you can model polymorphism with tables of function pointers—effectively manual vtables. A “class” becomes a struct of data plus pointers to operations (`open`, `read`, `close`, etc.). Different modules supply matching functions for their concrete types. This pattern appears in drivers, plugin systems, and embedded HALs.

### Context pointers

Pass an opaque `void *ctx` or a tagged union as the first argument to interface functions so implementations can recover their private state. Document lifetimes: who allocates `ctx`, whether it outlives individual calls, and threading constraints. Comparison with object-oriented languages: you trade compiler-enforced interfaces for explicit wiring and disciplined conventions.

### Simple vtable sketch

```c
typedef struct io io_t;
struct io {
    void *ctx;
    ssize_t (*read)(io_t *, void *buf, size_t n);
    void (*close)(io_t *);
};

static ssize_t dummy_read(io_t *self, void *buf, size_t n) {
    (void)self;
    (void)buf;
    return (ssize_t)n;
}
```
""",
    "pointers": """### Addresses and indirection

The unary `&` takes the address of an object; unary `*` dereferences a pointer. Pointer types must match the pointed-to object unless you intentionally use `void *` as a generic address and cast when reading (with care). Pointer arithmetic scales by the pointee size: `p + 1` advances one element, not one byte—use `char *` for byte-oriented walks.

### `const` and `restrict`

`const T *` prevents modification through that path; `T *const` fixes the pointer variable itself. `const`-correct APIs document who may mutate shared data. `restrict` promises exclusive access during a function call—misuse breaks optimizations and semantics.

### Null and undefined behavior

A null pointer (`NULL`) is not dereferenceable. Wild pointers and use-after-free look like data corruption. For interoperability with hardware, `volatile` and `uintptr_t` appear, but never casually—misuse masks optimizer assumptions.

```c
#include <stdio.h>

void bump(int *p) { if (p) (*p)++; }

int main(void) {
    int x = 0;
    bump(&x);
    printf("%d\\n", x);
    return 0;
}
```
""",
    "errors": """### Return codes and `errno`

C commonly signals failure through return values: `0` or positive for success counts, `-1` for generic failure, or `NULL` for pointer results. Many library functions also set the thread-local `errno` from `<errno.h>`—check return values first, then inspect `errno` only when documentation promises it. Never compare `errno` to specific values without including the right headers; use macros like `ENOMEM`, `EINVAL`.

### Stratify severity

Distinguish programmer errors (assert with `assert.h` in debug builds) from runtime conditions (disk full, network timeout). For recoverable errors, return enums or structured results; for unrecoverable invariant violations, abort or log fatally according to policy. Avoid encoding unrelated data in the sign bit unless your API is narrowly scoped.

### Clearing and threads

`errno` is typically per-thread in modern POSIX; still set it to `0` before calls when you must disambiguate rare ambiguity in some POSIX functions’ error reporting. Print human-readable messages with `perror` or `strerror`.

```c
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *f = fopen("nope.txt", "rb");
    if (!f) {
        perror("fopen");
        return EXIT_FAILURE;
    }
    fclose(f);
    return EXIT_SUCCESS;
}
```
""",
    "concurrency": """### Threads and synchronization

POSIX threads (`pthread.h`) provide `pthread_create`, `pthread_join`, mutexes (`pthread_mutex_t`), condition variables, and read-write locks. Share only immutable data freely; mutable shared memory requires synchronization. Mutex rules—“lock before touching shared state, unlock on all paths”—mirror discipline you would apply in any concurrent system, but C gives no compile-time race detection.

### Atomics and memory order

C11 `<stdatomic.h>` supplies atomic types and fences for lock-free algorithms when you can prove correctness—expert territory. Weaker-than-`memory_order_seq_cst` orderings enable performance but are easy to misuse; prefer mutexes until profiling proves otherwise.

### Pitfalls

Data races on non-atomic objects are undefined behavior. Destroying a mutex while held, double-locking non-recursive mutexes without design, or signaling condition variables without the right predicate checks are common bugs. Tools like ThreadSanitizer (TSan) help enormously.

```c
#include <pthread.h>
#include <stdio.h>

static void *worker(void *arg) {
    (void)arg;
    return NULL;
}

int main(void) {
    pthread_t t;
    pthread_create(&t, NULL, worker, NULL);
    pthread_join(t, NULL);
    puts("done");
    return 0;
}
```
""",
    "methods": """### Structs and functions as methods

C has no built-in method syntax. You model behavior with **functions** that take a pointer to the struct as the first parameter—often named `self`, `ctx`, or the type name abbreviated (`circle`, `buf`). Keep the struct definition in a header and declare function prototypes beside it so call sites read like `stack_push(&s, value)`.

### Naming and visibility

Prefix functions with the type name to avoid linker clashes: `String_append`, `Vec_clear`. Use `static` for helpers that should stay inside one `.c` file. Document which functions mutate the receiver versus those that only read fields.

### Pointer versus value receivers

Pass **`const T *`** when the function must not modify the object; pass **`T *`** when it may update fields or write through internal buffers. Passing large structs by value copies bytes—prefer pointers for anything bigger than a few machine words. For small plain structs (2D points, RGB tuples), by-value parameters can be clearer.

### Initialization and invariants

Provide a dedicated constructor-style function (`foo_init`, `foo_new`) that sets valid defaults and returns an error code if allocation fails. Pair it with `foo_destroy` or `foo_free` when the struct owns heap memory. Methods should preserve invariants documented in the header (non-null pointers, size bounds).

```c
typedef struct {
    int *data;
    size_t len;
    size_t cap;
} IntStack;

void stack_init(IntStack *s);
void stack_free(IntStack *s);
int stack_push(IntStack *s, int value);
int stack_pop(IntStack *s, int *out);
```
""",
    "testing": """### Assertions and harnesses

Lightweight testing starts with `assert` macro (`NDEBUG` disables it in release). For systematic checks, structure suites that run many small tests, report failures with file and line, and return nonzero exit status to CI. Popular minimal frameworks exist as single headers; alternatively, integrate CTest/autotools or Meson test targets to run binaries under sanitizers.

### Isolation and determinism

Pure functions over explicit inputs are easiest to test. For code touching `time`, files, or randomness, inject dependencies via function pointers or small wrapper modules so tests can swap deterministic fakes. Golden-file tests help for parsers; property-based fuzzing (libFuzzer, AFL) complements unit tests for parsers and decoders.

### Coverage and CI

Combine unit tests with AddressSanitizer/UndefinedBehaviorSanitizer in CI builds. Coverage tools (`gcov`, `llvm-cov`) highlight untested branches—aim for meaningful coverage, not percentages alone.

```c
#include <assert.h>

static int square(int x) { return x * x; }

int main(void) {
    assert(square(3) == 9);
    return 0;
}
```
""",
    "json": """### Parsing without a standard library type

JSON is text; C represents it as `char` buffers. You typically choose a third-party parser/serializer such as cJSON, Jansson, or json-c depending on license and API taste. These libraries build trees of objects and arrays, expose iterators, and handle Unicode escapes. Rolling a full parser is an exercise in lexing and state machines—not something to ship casually.

### DOM versus streaming

DOM-style APIs load the entire document into memory—simple for small configs. For large inputs, SAX-like streaming reduces RAM at the cost of more complex code. Always validate sizes before allocating proportional buffers; deep nesting can stack-overflow naive recursive descents—iterate or bound recursion.

### Typing and numbers

JSON numbers are IEEE doubles in most implementations; integers beyond 53 bits may lose precision unless your library offers arbitrary precision. Emitting stable, sorted keys aids reproducible outputs and diffs for tests.

```c
/* Conceptual: with a hypothetical API */
#include <stdio.h>

int main(void) {
    /* json_t *root = json_loads("{\"a\":1}", 0, &error); */
    puts("Integrate a real JSON library in projects.");
    return 0;
}
```
""",
    "time": """### Calendar and monotonic clocks

`<time.h>` provides `time` for calendar seconds since the epoch (often as `time_t`), `localtime`/`gmtime` to break into `struct tm`, and `mktime`/`strftime` for formatting—beware locale and reentrancy (`localtime_r` on POSIX). These are wall-clock times; they jump with daylight saving or NTP adjustments—do not use them alone for measuring intervals.

### Monotonic and high resolution

For benchmarking and timeouts, POSIX offers `clock_gettime(CLOCK_MONOTONIC, …)` when available; compare differences in nanoseconds. Windows has QueryPerformanceCounter—stick to your platform’s documented clock for durations. Convert carefully between `struct timespec` fields to avoid precision loss.

### Sleeping and timers

`sleep`, `nanosleep`, and `usleep` (deprecated/nonstandard) pause the thread—pick the portable option for your targets. Combine monotonic reads with condition variables to implement cancellable waits.

```c
#include <stdio.h>
#include <time.h>

int main(void) {
    time_t now = time(NULL);
    struct tm *tm_info = localtime(&now);
    char buf[64];
    if (tm_info) {
        strftime(buf, sizeof buf, "%Y-%m-%d %H:%M:%S", tm_info);
        puts(buf);
    }
    return 0;
}
```
""",
}
