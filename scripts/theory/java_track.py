"""Java 17+ theory snippets keyed by chapter id."""

from __future__ import annotations

THEORIES: dict[str, str] = {
    "variables": """
### Declarations and immutability
Java variables hold either a primitive value or a reference to an object. Local variable type inference with `var` (Java 10+) lets the compiler infer the type from the initializer, which keeps code concise when the right-hand side already documents the intent.

Use `final` for locals, parameters, and fields that must not be rebound after initialization. `final` does not deep-freeze mutable objects: a `final List<String>` cannot be reassigned, but the list contents can still change unless you use an unmodifiable view or an immutable implementation.

### Primitives, wrappers, and naming
Primitive types (`int`, `long`, `double`, `boolean`, …) live on the stack when they are local variables and avoid boxing overhead. Wrapper classes (`Integer`, `Double`, …) participate in generics and can be null; prefer primitives in hot paths and APIs where absence is not modeled as null.

Conventional style uses `camelCase` for locals and methods, `PascalCase` for types, and `ALL_CAPS` for constants declared as `static final`.

### Example
```java
public final class Demo {
    public static void main(String[] args) {
        var count = args.length; // int
        final var name = count > 0 ? args[0] : "world";
        System.out.println("Hello, " + name);
    }
}
```
""",
    "ownership": """
### References and garbage collection
Java does not expose manual memory ownership like systems languages with linear types. Instead, many references can alias the same object on the heap, and the garbage collector reclaims unreachable objects automatically. Your core obligation is logical correctness: do not leak references you no longer need in long-lived caches, static fields, or collections unless that retention is intentional.

Think in terms of lifetimes and scopes: locals and parameters disappear when a stack frame ends; instance fields live as long as the enclosing object; static fields live for the class loader’s lifetime.

### Resource ownership with try-with-resources
For non-memory resources (files, sockets, database connections), use try-with-resources so that `close()` runs deterministically. Types must implement `AutoCloseable` or `Closeable`.

```java
try (var reader = Files.newBufferedReader(path)) {
    // use reader
} // close called automatically
```

### Defensive copies and trust boundaries
When you accept mutable objects from callers, decide whether your API should store aliases or copy data. At trust boundaries (parsing input, crossing threads), prefer immutable snapshots or unmodifiable views to prevent surprising cross-caller mutation.
""",
    "controlflow": """
### Conditionals and Boolean discipline
`if` / `else` chains remain the workhorse for irregular conditions. Avoid redundant negations and keep conditions readable; extract complicated predicates into well-named `boolean` methods.

Switch expressions (Java 14+) can return values and use `yield` in statement blocks, reducing duplicate `break` bugs. Pattern matching for `switch` on types and null handling improves expressiveness in Java 17+ for sealed hierarchies and polymorphic dispatch.

### Loops and collection traversal
Traditional `for`, enhanced `for`, and `while` loops are still appropriate when indices matter or you need explicit control flow. For many collection pipelines, `Stream` may read better, but loops often win for clarity and performance tuning.

### Example
```java
String describe(Object o) {
    return switch (o) {
        case Integer i -> "int " + i;
        case String s -> "string " + s;
        case null -> "null";
        default -> "something else";
    };
}
```
""",
    "functions": """
### Methods, static versus instance behavior
Java organizes behavior in classes. Instance methods receive a hidden `this` reference; `static` methods belong to the type and cannot access instance fields without an explicit instance.

Methods support overloading: the compiler picks the most specific applicable signature. Overriding replaces inherited behavior when a subclass provides a method with the same signature; annotate overrides with `@Override` to catch signature drift at compile time.

### Lambdas and method references
Functional interfaces (one abstract method) are the target type for lambda expressions and method references. Keep lambdas short; if they grow multi-step logic, use a named private method.

```java
List<String> names = List.of("ada", "bob");
List<String> upper = names.stream()
    .map(String::toUpperCase)
    .toList(); // Java 16+ unmodifiable list from stream
```
""",
    "arrays": """
### Fixed-length sequences
Arrays (`T[]` for references, `int[]` for primitives) have a fixed length set at construction. They are covariant for reference types (`String[]` is an `Object[]`), which interacts with heap pollution checks at runtime if you assign incompatible element types.

Multidimensional arrays are arrays of arrays; ragged arrays (rows of different lengths) are natural in Java.

### Utilities and interoperability
`java.util.Arrays` provides sorting, binary search, copying, and parallel prefix helpers. Prefer `List` APIs at boundaries when you need grow/shrink semantics; convert with `List.of(array)` for a fixed list view where appropriate, understanding the aliasing implications.

```java
int[] nums = {3, 1, 4};
Arrays.sort(nums);
int[] copy = Arrays.copyOf(nums, nums.length + 1);
copy[copy.length - 1] = 1;
```
""",
    "slices": """
### Views instead of true slices
Java has no first-class slice type like some other systems languages. Instead, you work with ranges via views and copies. `List.subList(from, to)` returns a view backed by the original list: structural changes in either place can invalidate the sublist, and some operations are still linear in underlying list type.

For arrays, `Arrays.copyOfRange` produces an independent array segment (a copy), which is safer when you want isolation at the cost of allocation.

### Text ranges
`String` and `StringBuilder` offer `substring` / `subSequence` style APIs; remember that older `String` implementations could share backing arrays, but modern JDKs still treat string content as immutable from the caller’s perspective—treat results as ordinary strings.

```java
List<Integer> xs = new ArrayList<>(List.of(10, 20, 30, 40));
List<Integer> window = xs.subList(1, 3); // [20, 30]
int[] segment = Arrays.copyOfRange(new int[]{1,2,3,4,5}, 1, 4);
```
""",
    "maps": """
### Choosing a map implementation
`HashMap` offers expected O(1) operations with hashing; keys must obey consistent `equals` / `hashCode`. `LinkedHashMap` preserves insertion or access order; `TreeMap` keeps sorted order by key using `Comparable` or a `Comparator`.

For constants known at compile time, `Map.of(k, v, …)` and `Map.ofEntries` create compact immutable maps.

### Modern map idioms
`computeIfAbsent`, `merge`, and `compute` replace many manual get/put sequences. Prefer these when updates depend on the prior value to keep logic atomic relative to the bucket.

```java
Map<String, Integer> counts = new HashMap<>();
for (String word : words) {
    counts.merge(word, 1, Integer::sum);
}
```
""",
    "strings": """
### Immutability and performance
`java.lang.String` is immutable: “modifying” methods return new strings. For repeated concatenation in loops, use `StringBuilder` to avoid quadratic copying.

Text blocks (Java 15+) cleanly embed multi-line JSON, SQL, or markdown while preserving indentation you control with the closing delimiter alignment.

### Text processing conveniences
Methods like `strip`, `isBlank`, `lines`, and `repeat` express common operations without ad hoc trimming. Use `String.formatted` / `formatted` instance method for readable formatting with placeholders.

```java
String sql = String.join(System.lineSeparator(),
    "SELECT id, name",
    "FROM users",
    "WHERE id = ?");
String msg = "Hello, %s!".formatted("Ada");
```
""",
    "structs": """
### Records as transparent data carriers
Records (Java 16+) model immutable data with auto-generated constructors, accessors, `equals`, `hashCode`, and `toString`. Use them for DTOs, return values, and local aggregates instead of verbose POJOs when the primary purpose is holding state.

Records are shallowly immutable: if a record component is a mutable list, callers can still mutate that list unless you defensively copy on construction or expose unmodifiable views.

### Classes when invariants matter
When you need extensive validation, lazy initialization, or subclassing, a regular `class` remains appropriate. Sealed classes and interfaces (Java 17) let you model closed hierarchies where only permitted subtypes extend a base type.

```java
public record Point(int x, int y) {
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("coordinates must be non-negative");
        }
    }
}
```
""",
    "interfaces": """
### Contracts, defaults, and evolution
Interfaces define required behavior. Default methods allow evolving APIs without breaking every implementation; use them for shared helper logic described in terms of other interface methods.

Private methods inside interfaces (Java 9+) factor default-method code without exposing helpers on implementing classes.

### Sealed and functional interfaces
Sealed interfaces limit permitted implementors, which pairs well with exhaustive `switch` patterns. Mark single-abstract-method interfaces with `@FunctionalInterface` to communicate intent and let the compiler enforce the constraint.

```java
sealed interface Shape permits Circle, Rectangle { double area(); }

record Circle(double radius) implements Shape {
    @Override public double area() { return Math.PI * radius * radius; }
}
```
""",
    "methods": """
### Resolution and polymorphism
The JVM selects instance methods using dynamic dispatch: the runtime type of the receiver determines which override runs. Static methods and fields bind to the compile-time type of the reference, not the object’s runtime class—avoid hiding instance methods with `static` methods of the same name; it confuses readers.

Overload resolution considers widening, boxing, and varargs in a fixed order; when in doubt, simplify call sites with explicit casts or introduce differently named methods.

### Modules of behavior
Break large methods into private helpers with names that state intent. Prefer passing parameters over mutable fields used as temporary scratch space.

```java
public final class Orders {
    public Money totalTax(Money subtotal, TaxRate rate) {
        return subtotal.multiply(rate.value());
    }
}
```
""",
    "packages": """
### Namespaces and visibility
Packages group related types and control access: `public` types are visible everywhere their module exports allow; package-private types are confined to their package. Mirror your module structure with directory layout (`com/example/app/Main.java` for `package com.example.app;`).

Wildcard imports (`import java.util.*;`) reduce import churn but can obscure names; many teams prefer explicit imports for readability in reviews.

### Modules (JPMS)
`module-info.java` declares module names, exports, and `requires` clauses. Even if you stay on the classpath during migration, understanding modules helps when adopting libraries that are modular JARs.

```java
package com.example.greet;

public final class Greeter {
    public String hello(String name) {
        return "Hello, " + name;
    }
}
```
""",
    "pointers": """
### References, not pointer arithmetic
Java exposes object references that track garbage-collected heap objects; you cannot perform pointer arithmetic or cast integers into references. `null` is a legal reference value meaning “no object,” and dereferencing it throws `NullPointerException`.

Value types in core libraries are either primitives, or object references; generics erase to raw references except for specialized runtime support—expect autoboxing costs when mixing primitives and generic APIs.

### Modeling absence with intent
Prefer `Optional<T>` for methods that might lack a result in purely functional workflows, but avoid using `Optional` for fields or JavaBeans-style setters. Validate parameters early and fail fast if invariants require non-null references.

```java
public String firstNonBlank(List<String> xs) {
    for (var s : xs) {
        if (s != null && !s.isBlank()) {
            return s;
        }
    }
    return null; // or throw, depending on API contract
}
```
""",
    "errors": """
### Exceptions as control flow signals
Java distinguishes checked exceptions (must be declared or caught) from runtime exceptions and errors. Overusing checked exceptions can push `throws` clauses through many layers; use them when callers can plausibly recover or must handle failure explicitly.

Unchecked exceptions (`IllegalArgumentException`, `IllegalStateException`) document programmer mistakes or unrecoverable situations; reserve them for truly exceptional conditions, not ordinary control flow.

### Resources and suppression
Try-with-resources composes cleanly with catch blocks; the primary exception wins, and any close-time failures add suppressed exceptions you can inspect later.

```java
try {
    risky();
} catch (IOException e) {
    throw new UncheckedIOException("operation failed", e);
}
```
""",
    "concurrency": """
### Threads, pools, and safe publication
Use `ExecutorService` or its factory helpers to bound concurrency instead of creating unbounded `new Thread(...)` storms. Share data across threads through immutable objects, `volatile` fields when appropriate for visibility, `java.util.concurrent` locks and atomics, or higher-level concurrent collections.

Document thread-safety promises: many standard collections are not safe for concurrent mutation without external synchronization.

### Structured tasks and async composition
`CompletableFuture` chains dependent async work with explicit executors when you need to keep bounded parallelism. For CPU-bound divide-and-conquer problems, `ForkJoinPool` can help, but measure before assuming speedups.

On **Java 21+**, `Executors.newVirtualThreadPerTaskExecutor()` and structured concurrency previews further simplify I/O-heavy fan-out; on **Java 17**, bounded thread pools remain the portable default.

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
try {
    var f1 = pool.submit(this::downloadA);
    var f2 = pool.submit(this::downloadB);
    combine(f1.get(), f2.get());
} finally {
    pool.shutdown();
}
```
""",
    "testing": """
### JUnit 5 style
Tests live beside or under a parallel test tree. Prefer `@ParameterizedTest` for tables of inputs, `@Nested` for grouping scenarios, and explicit assertions that print meaningful messages on failure.

Keep tests deterministic: control time with a `Clock` you inject, isolate randomness with fixed seeds, and avoid implicit reliance on global statics when unit testing.

### Example
```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MathStuffTest {
    @Test
    void abs_nonNegative() {
        assertEquals(5, Math.abs(-5));
        assertEquals(0, Math.abs(0));
    }
}
```
""",
    "json": """
### Mapping values to text
Use a mature library (commonly Jackson or Gson) instead of hand-built string concatenation. Configure naming strategy, unknown-property policy, and date/time formats explicitly so upgrades behave predictably.

Records mesh well with serialization: many mappers can construct them with canonical constructors, giving concise JSON DTOs without Lombok.

### Streaming and large payloads
For large inputs, prefer streaming parsers over loading entire documents into memory. Validate required fields and reject oversized payloads at your HTTP layer before parsing deeply.

```java
// Illustrative Jackson usage (dependency required)
// ObjectMapper mapper = new ObjectMapper();
// User u = mapper.readValue(json, User.class);
// String out = mapper.writeValueAsString(u);
```
""",
    "time": """
### `java.time` first
Avoid legacy `Date` / `Calendar` in new code. Model instants on the UTC timeline with `Instant`, civil dates with `LocalDate`, wall-clock times with `LocalTime`, and civil datetimes without offset using `LocalDateTime`.

When zoning matters, use `ZonedDateTime` or convert carefully with `ZoneId`. Duration (`Duration`) covers day-time quantities; `Period` models calendar-aware day/month/year differences.

### Formatting and parsing
`DateTimeFormatter` is immutable and thread-safe; define explicit patterns or built-in ISO formats. Parse lazily only after validating input length and charset.

```java
ZoneId zone = ZoneId.of("Europe/Berlin");
ZonedDateTime meeting = ZonedDateTime.of(
    LocalDate.of(2026, 5, 16),
    LocalTime.of(14, 30),
    zone
);
String text = meeting.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME);
```
""",
}
