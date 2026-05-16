"""Expanded chapter theory text for the C# / .NET track."""

from __future__ import annotations

THEORIES: dict[str, str] = {
    "variables": """### Types, locals, and inference

C# is a statically typed language on the CLR (Common Language Runtime): every expression has a type known at compile time unless you deliberately use dynamic features. Local variables can be declared with an explicit type (`int count = 0`) or with `var` when the right-hand side makes the type obvious (`var name = "Ada";`). `var` is still strongly typed—the compiler infers the exact type; it is not a weak or “anything goes” declaration.

Value types (such as `int`, `bool`, `double`, `decimal`, `char`) usually live on the stack when they are locals, while instances of reference types (`string`, `List<int>`, custom classes) are heap allocated and referenced through references. The `decimal` type exists for currency-like exact decimal arithmetic; floats use binary IEEE representations and can surprise you with rounding.

Constants are resolved at compile time: `const int Max = 42;` must be a literal or constexpr-friendly expression. For values computed at startup or configuration, prefer `static readonly` fields or `init`-only properties.

### Culture-stable text

Console exercises often compare stdout exactly. Use `CultureInfo.InvariantCulture` when formatting numbers or dates that must match a canonical string. Interpolated strings (`$"{n}"`) use the current culture by default; call `ToString(IFormatProvider)` or pass a format string when stability matters.

```csharp
using System;
using System.Globalization;

var pi = 3.14159;
Console.WriteLine(pi.ToString("F3", CultureInfo.InvariantCulture));
```
""",
    "ownership": """### Value vs reference semantics

C# does not use Rust-style ownership moves on ordinary class instances. Instead, assignment of a reference type copies the *reference* (a small pointer-like value), so two variables can alias the same object on the heap. Value types copy their entire payload unless you pass them with `ref`, `in`, or `out`.

structs are value types; **mutating methods** on a struct often require the instance to be a variable, not a temporary, because mutating a copy would hide bugs. **readonly struct** and `readonly` members communicate immutability intent and help the compiler optimize.

### Garbage collection and lifetime

You rarely `free` memory by hand. The garbage collector reclaims unreachable objects. That means “ownership” in a C# course is really **resource discipline**: avoid keeping large graphs reachable longer than needed, dispose `IDisposable` where appropriate, and understand that `using` statements translate to deterministic cleanup for unmanaged handles.

### Boxing and copies

Putting a value type into a location typed as `object` or an interface it implements causes **boxing**, which allocates on the heap. Modern APIs prefer generics (`List<int>`) to avoid repeated boxing. Where you need both performance and abstraction, `Span<T>` and generic constraints help.

```csharp
using System;
using System.Collections.Generic;

var numbers = new List<int> { 1, 2, 3 }; // no boxing for int elements

object boxed = 42; // int boxed as object

Span<int> stackInts = stackalloc int[3];
stackInts[0] = 7;
```
""",
    "controlflow": """### Conditionals and patterns

Branching uses `if`, `else if`, and `switch`. Modern C# favors **pattern matching**: you can switch on types, combine property tests with `when`, and use **switch expressions** that return values concisely.

The **nullable reference types** feature (nullable context) lets the compiler warn when you may dereference `null`. Combine it with null checks, null-coalescing (`??`), null-conditional (`?.`), and the `??=` assignment operator for clearer control flow around missing values.

### Loops and iterators

`for`, `while`, and `do/while` behave much like C-family languages. `foreach` works on anything that exposes a public `GetEnumerator` or satisfies the async enumerable pattern. `break` and `continue` work in loops; `goto` exists but is reserved for rare IL-level patterns or generated code.

LINQ methods (`Where`, `Select`, etc.) do not mutate collections—they describe queries executed when enumerated. That distinction matters for side effects and performance.

```csharp
using System;
using System.Linq;

var xs = new[] { 1, 2, 3, 4 };

var sumEven = xs.Where(n => n % 2 == 0).Sum();

var label = DateTime.Now.Hour switch
{
    < 12 => "morning",
    < 18 => "afternoon",
    _ => "evening"
};

Console.WriteLine($"{sumEven} {label}");
```
""",
    "functions": """### Methods, local functions, and delegates

Methods live on types; you choose `static` for operations that do not need instance state. Parameters default to **pass-by-value**: for reference types the value is the reference; for value types the whole struct is copied. Use `ref`, `in`, and `out` for by-reference semantics—`out` is an alias for output parameters that must be assigned before the method returns.

**Local functions** inside members keep helpers lexically scoped and can capture locals without exposing them on the type.

### Lambda expressions and Func/Action

Anonymous functions (`() => expr` or `delegate` blocks) convert to **delegate** types such as `Func<T>` and `Action`. LINQ depends heavily on delegates; expression trees (`Expression<Func<...>>`) represent code as data for providers like EF Core, but plain delegates execute immediately.

### Async signatures

Async methods often return `Task` or `Task<T>`. The `async` keyword enables `await` inside the method body; the compiler rewrites the method into a state machine. Prefer “async all the way”—avoid blocking with `.Result` or `.Wait()` on thread-pool backed work in libraries.

```csharp
using System;
using System.Threading.Tasks;

static int Add(in int a, in int b) => a + b;

Func<int, int, int> addFunc = (x, y) => x + y;

async Task<int> DelayedIncrement(int x)
{
    await Task.Delay(10);
    return x + 1;
}
```
""",
    "arrays": """### Array types in CLR

Arrays are reference types with a fixed length after allocation. One-dimensional arrays use `T[]` syntax; rectangular (`[,]`) and jagged (`[][]`) arrays model different layout and indexing trade-offs. Bounds checks happen on each access unless the JIT can prove them redundant.

`Array` static helpers (`Sort`, `BinarySearch`, `Fill`, `Copy`) operate on various shapes. For performance-critical low-allocation code, `stackalloc` produces a span-backed buffer on the stack (size must be known and reasonable).

### Initialization

Array initializers infer length (`new[] { 1, 2, 3 }`) and can target implicitly typed locals with `var xs = new[] { 1, 2 };`. When you expose arrays from APIs, consider whether callers might mutate internal state—a `ReadOnlyCollection<T>` wrapper or returning `IReadOnlyList<T>` clarifies intent.

```csharp
using System;

var nums = new int[] { 5, 2, 8 };

Array.Sort(nums);

Span<int> view = nums;

Console.WriteLine(nums[nums.Length - 1]);
```
""",
    "slices": """### Span, Memory, and ranges

C# models **windows into contiguous memory** with `Span<T>` and `ReadOnlySpan<T>` for synchronous stack-friendly code, and `Memory<T>` / `ReadOnlyMemory<T>` for async pipelines. These types unify arrays, stack buffers, and slices of unmanaged memory without copying.

The **range syntax** (`start..end`, `^n` from end) pairs with `Span<T>` and arrays to project sub-windows. For UTF-16 text, `ReadOnlySpan<char>` is the efficient surface many modern APIs accept.

### LINQ vs allocation

`Enumerable.Skip`/`Take` on arrays allocates iterators. When you already have contiguous storage, slicing with spans avoids intermediate sequence objects and reduces pressure on the GC.

```csharp
using System;

var text = "abcdef";

ReadOnlySpan<char> span = text.AsSpan();

ReadOnlySpan<char> mid = span[1..4];

Console.WriteLine(mid.ToString());

int[] a = { 10, 20, 30, 40, 50 };

Span<int> s = a.AsSpan(1, 3);
```
""",
    "maps": """### Dictionary and friends

`Dictionary<TKey, TValue>` is the hash-table workhorse: average O(1) lookups, keyed equality uses `IEqualityComparer<TKey>` when supplied. For concurrent scenarios, `ConcurrentDictionary<TKey, TValue>` provides thread-safe updates without external locking for many common operations.

`ImmutableDictionary` in `System.Collections.Immutable` is excellent for **stable snapshots** you share across threads: updates return new collections while sharing structure internally.

### Patterns with dictionaries

Try patterns (`dict.TryGetValue`) avoid double lookups. `GetValueOrDefault` simplifies optional keys. When keys are case-insensitive strings, pass `StringComparer.OrdinalIgnoreCase` into alternate constructors.

Many frameworks deserialize JSON objects into `Dictionary<string, JsonElement>` or strongly typed models via `System.Text.Json`—pick clarity and validation requirements accordingly.

```csharp
using System;
using System.Collections.Generic;

var scores = new Dictionary<string, int>
{
    ["ada"] = 100,
    ["linus"] = 98
};

if (scores.TryGetValue("ada", out var v))
    Console.WriteLine(v);
```
""",
    "strings": """### Strings as UTF-16

`string` is an immutable sequence of UTF-16 code units. Indexing yields `char` (16 bits), which is not always a full Unicode scalar value—extended grapheme clusters may span multiple `char` values. For user-perceived characters, consider `StringInfo` or `System.Text.Rune` in modern codebases.

Concatenating strings in loops allocates repeatedly; `StringBuilder` batches edits. Interpolated strings compile to efficient formatting when combined with `StringBuilder.Append` or `DefaultInterpolatedStringHandler` optimizations on modern runtimes.

### Memory and search

`ReadOnlySpan<char>` avoids allocating substrings when parsing slices of a larger string. `string.AsSpan()` bridges to span-based APIs. `MemoryExtensions` introduces span-aware `Contains`, `IndexOf`, and similar helpers.

Culture matters: `ToUpperInvariant`/`ToLowerInvariant` is preferred for protocol identifiers; linguistically correct casing uses culture-aware overloads.

```csharp
using System;
using System.Globalization;
using System.Text;

var sb = new StringBuilder();

sb.Append("Hello, ").Append("world");

Console.WriteLine(sb.ToString());

Console.WriteLine(42.ToString(CultureInfo.InvariantCulture));
```
""",
    "structs": """### Struct vs class

classes are reference types; structs are value types with **copy semantics** on assignment and when passed without `ref`. structs are ideal for small, cohesive bundles like coordinates or UUIDs when you want dense, embedded storage—think of structs as shaping memory layout and copying cost.

**Readonly struct** signals immutability and enables compiler optimizations; **ref struct** types (like `Span<T>`) cannot escape to the heap, preserving stack-only safety.

### Records (value semantics)

**record struct** gives concise syntax for value-like data carriers with value-based equality (`record struct Point(int X, int Y);`). **record class** provides similar ergonomics for reference types with synthesized equality and `with` expressions for non-destructive mutation. Pick structs when copying cost is acceptable and you want value equality without heap churn.

```csharp
readonly record struct Point(double X, double Y);

record Person(string Name, int Age);

var p1 = new Point(1, 2);

var p2 = p1 with { Y = 3 };
```
""",
    "interfaces": """### Contracts and polymorphism

Interfaces define capabilities without a single inheritance tree; a type may implement many interfaces. Explicit interface implementation hides members unless the reference is typed as that interface—useful when names collide or you want a cleaner public surface.

Default interface members (C# 8+) let you evolve contracts with optional implementations, but think carefully about versioning across assemblies.

### IDisposable and async

`IDisposable` (and `IAsyncDisposable`) represent resources beyond memory: file handles, network connections, database contexts. `using` and `await using` compile to try/finally with `Dispose`/`DisposeAsync` calls.

### Generic constraints

`where T : ISomething` constrains type parameters; combined with **covariance/contravariance** on interfaces (`IEnumerable<out T>`, `IComparer<in T>`), you can express flexible APIs while keeping static typing.

```csharp
using System;
using System.Threading.Tasks;

interface ILogger
{
    void Log(string message) => Console.WriteLine(message);
}

interface IAsyncWorker
{
    Task<int> ComputeAsync();
}
```
""",
    "methods": """### Instance vs static

Instance methods receive a hidden first parameter (`this`). `static` methods belong to the type itself. Extension methods are static methods in a static class whose first parameter uses `this`—they allow instance-call syntax and are heavily used by LINQ.

Partial methods and partial classes split generated and hand-written code—common in UI tooling and source generators.

### Operators and overloading

You can overload many operators for your types when it improves clarity (`+` on a `Vector2`). Implicit and explicit conversion operators customize bridging between types—avoid surprising conversions that hide expensive work.

### Overloading and parameters

C# resolves overloads by argument types, optional parameters, and `params` arrays. Named arguments disambiguate when many overloads exist; optional parameters must come at the end.

```csharp
using System;

static class StringExtensions
{
    public static bool IsNullOrEmpty(this string? s) =>
        string.IsNullOrEmpty(s);
}

record Box(int Value);

class Vector2(double x, double y)
{
    public double X { get; } = x;
    public double Y { get; } = y;

    public static Vector2 operator +(Vector2 a, Vector2 b) =>
        new(a.X + b.X, a.Y + b.Y);
}
```
""",
    "packages": """### Namespaces and assemblies

C# source organizes into **namespaces** (logical hierarchy) and **assemblies** (.dll outputs—the unit of deployment). The `global::` prefix escapes out of local aliases when names collide across libraries.

`using` imports namespaces; `using static` imports static members; **file-scoped namespaces** (`namespace Foo;`) reduce indentation in large files.

### NuGet and the SDK

The .NET SDK uses **MSBuild** and **PackageReference** items to pull NuGet packages at restore time. Transitive dependencies resolve automatically; `Directory.Build.props` centralizes versions in multi-project solutions.

Internals visible to friends (`InternalsVisibleTo`) lets test assemblies access `internal` API without widening public surface.

```csharp
using System;
using System.IO;

namespace Demo.App;

class Program
{
    static void Main()
    {
        Console.WriteLine(Path.Combine("data", "log.txt"));
    }
}
```
""",
    "pointers": """### References first

Most C# code expresses indirection with managed references (`ref`, `out`, `in`) instead of raw pointers. These participate in the type system and are tracked by the GC when pointing to managed objects.

### Unsafe code

`unsafe` contexts allow pointer arithmetic (`T*`), `stackalloc` in wider scenarios, and interop with native libraries. You must enable unsafe code in the project file for those blocks. Keep unsafe regions small and well-encapsulated—usually behind interop layers.

### Fixed and pinning

Taking the address of a managed object’s data may require `fixed` to **pin** the object so the GC cannot move it while native code runs. P/Invoke declarations (`LibraryImport` / `DllImport`) marshal blittable types efficiently; strings and arrays may require marshalling attributes.

```csharp
using System;

class Scalars
{
    public static void Bump(ref int x) => x++;

    public static unsafe void PrintAddress(int* p) =>
        Console.WriteLine((nuint)p);
}
```
""",
    "errors": """### Exceptions on the CLR

C# favors **exceptions** for exceptional failure: stack-unwinding runs `finally` blocks and `using` disposals. **Do not** use exceptions for ordinary control flow in hot loops—it is slower and obscures intent.

Derive from `Exception` for domain errors when you need rich context; built-in types like `ArgumentOutOfRangeException` communicate misuse clearly.

### Modern patterns

`OperationCanceledException` integrates with `CancellationToken` for cooperative cancellation—do not swallow it in generic catch blocks.

Some codebases layer a **Result**-style pattern for expected failures while still using exceptions for truly unexpected states. The `try`/`catch`/`finally` structure composes with `using` and `await using` for deterministic cleanup.

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

async Task<int> FetchAsync(CancellationToken ct)
{
    await Task.Delay(100, ct);
    return 7;
}

try
{
    await FetchAsync(CancellationToken.None);
}
catch (OperationCanceledException)
{
    // cooperative cancellation path
}
```
""",
    "concurrency": """### Threads, tasks, and the thread pool

`Task` represents potentially asynchronous work. `async`/`await` composes asynchronous operations without blocking a thread for I/O waits. CPU-bound work can be offloaded with `Task.Run` (sparingly—profile first).

### Synchronization

`lock` provides mutual exclusion around a reference object; **never** lock on `string` literals or `Type` objects shared across assemblies. `Monitor`, `Mutex`, `SemaphoreSlim`, and concurrent collections help with more complex coordination.

### async pitfalls

Avoid `async void` except for event handlers—it crashes the process on unobserved exceptions. `ConfigureAwait` matters for library code consumed from UI threads when you must resume on a captured context.

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

async Task<int> DoubleAsync(int x)
{
    await Task.Yield();
    return x * 2;
}

class Counter
{
    private int _n;
    private readonly object _gate = new();

    public void Inc()
    {
        lock (_gate) { _n++; }
    }
}
```
""",
    "testing": """### xUnit-style building blocks

.NET testing commonly uses **xUnit**, **NUnit**, or **MSTest**. `[Fact]` marks a single test; `[Theory]` pairs `[InlineData]` or member data with parameters. Assertions come from `Assert.*` helpers or fluent libraries like FluentAssertions.

### Isolation and fakes

Prefer testing through small, injectable dependencies (constructor injection) so you can substitute fakes in tests. `Microsoft.Extensions.DependencyInjection` is the typical container in ASP.NET Core apps.

### Coverage and determinism

Use deterministic clocks or seeds when testing time or randomness. Separate pure logic from IO so tests stay fast and reliable.

```csharp
using Xunit;

namespace Tests;

public class MathTests
{
    [Fact]
    public void Adds()
    {
        Assert.Equal(4, 2 + 2);
    }

    [Theory]
    [InlineData(1, 2, 3)]
    [InlineData(-1, 1, 0)]
    public void AddsMany(int a, int b, int sum) =>
        Assert.Equal(sum, a + b);
}
```
""",
    "json": """### System.Text.Json

`System.Text.Json` is the built-in serializer for high throughput and low allocation. `JsonSerializer.Serialize` / `Deserialize` map between JSON and CLR types via source-generated serializers (`JsonSerializerContext`) or reflection-based serializers.

**Naming policies** let you switch between `camelCase` JSON and PascalCase CLR properties. **Converters** handle tricky types like `DateTimeOffset` or discriminated unions expressed as tagged objects.

### DOM vs strongly typed

`JsonDocument` and `JsonNode` allow ad hoc navigation when schema is fluid; binding to records or classes catches shape errors early. For large files, **streaming** APIs avoid loading the entire payload into memory.

```csharp
using System;
using System.Text.Json;

record User(string Name, int Age);

var json = JsonSerializer.Serialize(new User("Ada", 36));

var u = JsonSerializer.Deserialize<User>(json);

Console.WriteLine(u);
```
""",
    "time": """### DateTime vs DateTimeOffset

`DateTime` mixes **unspecified**, UTC, and local kinds; bugs appear when you subtract values with different kinds or assume `Now` is universal. Prefer **`DateTimeOffset`** for instants that must round-trip with an explicit offset, and be deliberate about **UTC** at storage boundaries.

### TimeSpan and arithmetic

`TimeSpan` measures elapsed time between ticks; it does not encode calendar concepts. Calendars use `DateOnly` / `TimeOnly` (.NET 6+) for human schedules without tying them to a time zone ambiguously.

Time zone conversions should go through **`TimeZoneInfo`** rather than fixed offsets for historical DST rules. For monotonic measurements (timeouts, profiling), `Stopwatch` uses a high-resolution clock unrelated to wall time.

```csharp
using System;

var utc = DateTime.UtcNow;

var dto = DateTimeOffset.UtcNow;

var span = TimeSpan.FromMinutes(90);

Console.WriteLine($"{utc:o} | {dto:o} | {span}");
```
""",
}
