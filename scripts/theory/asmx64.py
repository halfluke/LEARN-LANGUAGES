"""Chapter theory copy for the Linux x86-64 / NASM Intel-syntax track.

Use ### headings and fenced ```nasm (or ```asm) blocks. Content targets ELF64
objects linked with ld (raw _start + syscalls) or gcc when calling libc.
"""

from __future__ import annotations

THEORIES: dict[str, str] = {
    "variables": """### Program shape on Linux x86-64

Every standalone program in this track is assembled to a **64-bit ELF relocatable**
(`nasm -f elf64`) and linked into an executable. When you use a global `_start` label
and talk to the kernel yourself, the **dynamic linker is optional** and `ld` is enough.
When you call **`extern`** symbols from the C library, you normally link with **`gcc`**
so startup files, libc, and ABI details are wired correctly.

Immediate values and register moves are your first “variables”: they are ephemeral,
but they are how you satisfy the Linux syscall calling convention. For **64-bit Linux**
syscalls, you place the syscall number in **`rax`**, arguments in **`rdi`**, **`rsi`**,
**`rdx`**, **`r10`**, **`r8`**, **`r9`**, then execute **`syscall`**.

### Exit and write syscalls

`sys_exit` (`rax = 60`) terminates the process; **`rdi`** carries the exit status.
`sys_write` (`rax = 1`) copies bytes from userspace to a file descriptor: **`rdi`**
is the fd (1 for stdout), **`rsi`** points at the first byte, **`rdx`** is the length.
Keep addresses of buffers in `.data` or `.bss` so they stay valid for the whole run.

```nasm
; Minimal exit(0)
global _start
section .text
_start:
    mov rax, 60         ; sys_exit
    xor rdi, rdi        ; status 0
    syscall

; Write "Hi" to stdout then exit — pattern used everywhere in this course
global _start
section .data
    msg: db 'H', 'i'
    len equ $ - msg
section .text
_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, len
    syscall
    mov rax, 60
    xor rdi, rdi
    syscall
```

### Assemble and link

Typical commands from the repo root mirror the exercise harness: assemble to `*.o`,
then `ld` for pure-syscall binaries or `gcc` when you import libc helpers. If you mix
hand-written `_start` with libc, pay attention to stack alignment and the AMD64 ABI
before calling C functions.
""",
    "controlflow": """### Flags and branches

After arithmetic and many logical operations, the CPU records outcomes in **rFLAGS**:
carry, zero, sign, and overflow matter most for branching. In Intel-syntax NASM,
comparisons are usually written as **`cmp`** (subtract) or **`test`** (bitwise AND
without storing a result), followed by a **conditional jump** such as **`je`**, **`jne`**,
**`jl`**, or **`jg`**. Unconditional flow uses **`jmp`**, and tiny loops often pair
**`dec`/`jnz`** or use **`loop`** when **`rcx`** is your counter.

Think of labels as human-readable addresses: the assembler computes distances for
relative jumps in simple cases, while large jumps still assemble cleanly in 64-bit mode.

### Structured layout with `.data`

Constants and small tables live in **`.data`**; uninitialized scratch space belongs in
**`.bss`**. Keeping read-only text separate from writable memory makes reasoning about
bugs easier and matches how real binaries separate **`.text`**, **`.rodata`**, and **`.data`**.

```nasm
global _start
section .data
    needle: db 7
section .text
_start:
    movzx eax, byte [rel needle]
    cmp eax, 7
    je .eq
    ; ... not equal path ...
.eq:
    ; ... equal path ...
```

### Syscalls still drive observable behavior

Control flow is only useful if it eventually reaches **`syscall`** (or calls routines
that do). When branching around I/O, double-check that every path sets **`rax`**, **`rdi`**,
**`rsi`**, and **`rdx`** consistently before a write, and ends with a well-defined exit.
""",
    "functions": """### The machine-level call contract

`call label` pushes the **return address** (the next instruction’s **RIP**) onto the
stack and jumps to **`label`**. **`ret`** pops that address back into **RIP**. If your
procedure uses the stack for locals, you must **`leave`/`mov rsp, rbp; pop rbp`** or
mirror whatever prologue you wrote so **`ret`** sees the correct return address on top
of the stack.

For interoperability with **C** on Linux AMD64, arguments arrive in **`rdi`**, **`rsi`**,
**`rdx`**, **`rcx`**, **`r8`**, **`r9`**, with additional stack spillover; **`rax`** carries
the integer return value, and **`rdx`** may carry the high half of a 128-bit result.
This track’s toy callees may use a simpler convention, but learning the ABI pays off
the moment you `extern printf`.

### Alignment before you reach libc

The AMD64 ABI expects **RSP mod 16 = 0** immediately before a **`call`** into functions
that may use SSE instructions—including much of **`libc`**. Pure-syscall programs are
more forgiving, but adopting the discipline early prevents mysterious crashes when you
promote a helper to call **`puts`**.

```nasm
section .text
say_hi:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, mlen
    syscall
    ret

global _start
section .data
    msg: db 'H', 'i'
    mlen equ $ - msg
section .text
_start:
    call say_hi
    mov rax, 60
    xor rdi, rdi
    syscall
```

### Preserving registers

General-purpose registers **`rbx`**, **`rbp`**, **`r12`–`r15`** are **callee-saved** in
the System V ABI: if you use them inside a procedure, restore them before **`ret`**.
**`rax`**, **`rcx`**, **`rdx`**, **`rsi`**, **`rdi`**, **`r8`–`r11`** are **caller-saved**;
assume callees trash them unless documented otherwise.
""",
    "arrays": """### Contiguous bytes, words, and quadwords

An **array** in assembly is mostly an address plus a stride. You define storage with
**`db`**, **`dw`**, **`dd`**, or **`dq`** and refer to elements with indexed addressing
modes such as **`byte [array + rcx]`** or **`qword [array + rcx*8]`**.

The **`equ`** pseudo-op is handy for sizes (`len equ $ - msg`) but remember **`$`**
evaluates at assembly time, so it captures the distance from the label’s base address
at the point where it appears in the source.

### Indexing and bounds

Hardware does not check array bounds: an out-of-range index silently reads or clobbers
adjacent memory. In learning exercises you compute indices carefully; in production you
prove them safe in a higher layer or insert explicit checks.

```nasm
section .data
    scores: db 10, 20, 30

section .text
; rcx = logical index 0..2
    movzx eax, byte [rel scores + rcx]
```

### Alignment and performance

Natural alignment (`dd` on 4-byte boundaries, `dq` on 8-byte boundaries) avoids split
access penalties on some cores. NASM lays out items sequentially; insert explicit **`align`**
directives when you care about cache-line or SIMD alignment even in userspace samples.
""",
    "slices": """### Pointer-length pairs by hand

Higher-level languages expose **slices** as pointer, length, and sometimes capacity.
In assembly you implement that trio yourself: one register holds the **base address**,
another holds the **element count** or **byte length**, and you advance the base when
you trim the front.

Negative lengths are meaningless; treat lengths as unsigned quantities and guard loops
so **`rcx`** does not wrap from zero with **`loop`** unless you intend the full **2⁶⁴**
iteration degenerate case—which you almost never do.

### Walking a range

A common idiom compares a running pointer to an end pointer computed as **`base + length`**
or decrements an explicit counter. Choose the pattern that keeps the fewest registers
live across **`syscall`** boundaries.

```nasm
; rsi points at first byte, rdx is byte length (already matches write syscall args)
    mov rax, 1
    mov rdi, 1
    syscall
```

### Re-slice without copying

Trimming prefix bytes only adjusts **RSI** and **RDX** for **`sys_write`**: the backing
storage stays put in **`.data`** or **`.bss`**. That mirrors how string views and byte
slices share storage in managed languages—only here there is no borrow checker to catch
use-after-trims gone wrong.
""",
    "strings": """### Bytes, not abstract text

In this track, strings are **byte sequences** with a known length. UTF-8 literals in
the assembler appear exactly as the bytes you wrote between quotes; NASM does not interpret
them as Unicode code points beyond encoding those bytes.

For truly dynamic text you either format into a scratch buffer or emit digits by repeated
division—classic **itoa**-style loops—or use libc helpers when you link with **gcc**.

### `write`-friendly layouts

Place literals in **`.data`** (`db 'H', 'e', 'l', 'l', 'o'`) and compute **`len equ $ - msg`**
so lengths stay consistent when you edit content. When printing single computed digits,
materialize ASCII by adding **`'0'`** into a byte buffer in **`.bss`**.

```nasm
section .data
    greeting: db 'Hello', 10
    glen equ $ - greeting

section .text
    mov rax, 1
    mov rdi, 1
    mov rsi, greeting
    mov rdx, glen
    syscall
```

### NUL terminators are optional

C strings end at **`0`**, but **syscalls** consume explicit lengths. Do not assume a
NUL unless you call routines that do; mixing models is a common off-by-one source.
""",
    "structs": """### Records as ordered layout

A **struct** is a block of fields at fixed offsets. NASM does not know about Rust or C
layouts automatically; you either equate offsets (`struc`/`istruc` support in NASM) or
document them and address fields as **`base + displacement`**.

Padding appears when types naturally align to machine boundaries—mirror what **`clang`**
would emit if you need to share a struct with C **`extern`** functions.

### Example record in `.data`

```nasm
struc Point
    .x: resd 1
    .y: resd 1
endstruc

section .data
    origin: istruc Point
        at Point.x, dd 2
        at Point.y, dd 3
    iend
```

### Loading members

Use appropriately sized moves: **`dword`** for 32-bit fields, **`qword`** for pointers.
Sign-extend or zero-extend when promoting narrower fields to **`rax`** for arithmetic,
matching how compilers prepare values before AMD64 operations.
""",
    "methods": """### Code plus explicit `this`

There are no methods in the language sense. You simulate them with **plain functions**
that take an extra argument—the address of the “receiver” struct—in **`rdi`** following
the AMD64 ABI, or whichever register your mini-convention uses consistently.

This mirrors what C++ lowers to before vtables enter the picture: **`adjust_field`** is
just a named block ending in **`ret`**, and the “object” is memory you pass by pointer.

```nasm
; void bump(ptr) — ptr in rdi, increments dword at offset 0
bump:
    inc dword [rdi]
    ret
```

### Shared helpers versus monolithic `_start`

Factoring **`write_line`**-style helpers keeps **`_start`** readable and matches how real
programs isolate syscalls behind tiny wrappers. Document which registers each helper
preserves so callers know what remains valid across **`call`**.
""",
    "pointers": """### Addresses with `lea` versus `mov`

**`lea reg, [base + index*scale + disp]`** computes an address without accessing memory.
**`mov reg, [addr]`** dereferences. Confusing the two is like mixing up **`&x`** and **`x`**:
both are legitimate, but only one loads the value.

Pointer-sized quantities are **64 bits** (`qword`). When you store an address of a label,
use **`dq label`** in **`.data`** and load it with **`mov rax, qword [rel ptr]`**.

### Stores and reloads

```nasm
section .bss
    slot: resb 1
section .data
    pslot: dq slot
section .text
    mov rax, qword [rel pslot]
    mov byte [rax], 'Z'
```

### Aliasing and TBAs

Two pointers that resolve to the same address alias the same memory. The CPU will happily
perform stores you did not logically expect if you computed two different paths to one
backing object—exactly why higher-level languages spend so much effort modeling aliasing.
""",
    "concurrency": """### Atomic read-modify-write

Modern CPUs expose **lock-prefixed** instructions that perform an atomic update on a
memory operand visible to other logical processors. For example, **`lock inc qword [mem]`**
reads the quadword, adds one, and writes back without a torn read in the middle—provided
every concurrent writer uses locking or compatible atomics.

This chapter is deliberately small: you see **`lock`** as a prefix on a handful of
instructions, not a full mutex implementation. Real systems combine atomics with **futex**
syscalls, queues, or RCU—but recognizing **`lock`** in disassembly is a prerequisite for
reading low-level performance patches.

### Single-threaded harness, atomic discipline

These exercises still run one thread; the **`lock`** prefix is instructional scaffolding
for how hardware serializes the operation. When you add threads later, every shared
location needs a consistent synchronization strategy—mixing plain loads with locked
updates elsewhere is still a data race in the C11 sense.

```nasm
section .data
    counter: dq 0

section .text
again:
    lock inc qword [rel counter]
    ; ... loop control ...
```

### Where to go next

User-space threads come from **`clone`**-family syscalls and pthreads; kernel schedules
them preemptively. Treat this chapter as connecting **instruction-set atomics** to the
broader concurrency story you will explore in higher-level languages back on top of the
same hardware primitives.
""",
}
