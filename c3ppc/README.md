# C3++ Compiler (c3ppc)

A C3++ to x86-64 assembly compiler with bootstrapping support.

## Quick Start

```bash
# Compile C3++ to x86-64 assembly
python3 c3ppc/compiler.py examples/hello.c3pp -o hello.s

# Assemble and link
gcc -o hello hello.s

# Run
./hello
```

## C3++ Language

C3++ is an object-oriented extension of C3 with no preprocessors.

### Hello World
```c3pp
import std::io;

fn void main()
{
    io::printn("Hello, World!");
}
```

### Features
- **No preprocessors** — use `import`, `const`, `module`
- **C3 syntax** — `fn`, `io::printn()`, `io::printfn()`
- **Classes** — `class Dog extends Animal { ... }`
- **Enums** — `enum Color { RED, GREEN, BLUE }`
- **Faults** — `fault ERR_NULL = -1;`
- **Contracts** — `@require(x > 0)` `@ensure(result > 0)`
- **Full type system** — `string`, `bool`, `int`, `uint`, `sz`, `usz`, `iptr`, `uptr`

### Interface Files (.c3ppi)

C3++ supports interface files (`.c3ppi`) similar to C3's `.c3i` files. These contain declarations only (no implementations) and are used for:

- Library headers
- Dynamic library interfaces
- API documentation
- Forward declarations

```c3ppi
// mathlib.c3ppi — Interface file for math library
module mathlib;

import std::io;

// Constants
const PI = 3.14159265358979;

// Enums
enum MathOperation {
    ADD,
    SUBTRACT,
    MULTIPLY,
    DIVIDE
}

// Structs
struct Vec2 {
    double x;
    double y;
}

// Classes (method signatures only, no bodies)
class Calculator {
    char* name;
    int precision;

    fn void set_precision(Calculator* self, int p);
    fn double calculate(Calculator* self, MathOperation op, double a, double b);
}

// Free functions (signatures only)
fn double math_abs(double x);
fn double sqrt(double x);
fn Vec2 vec2_add(Vec2 a, Vec2 b);
```

Compile interface files like regular source:
```bash
python3 c3ppc/compiler.py --interface examples/mathlib.c3ppi -o mathlib.c
python3 c3ppc/compiler.py --c examples/mathlib.c3ppi -o mathlib.c
```

### Examples

| File | Description |
|------|-------------|
| `examples/hello.c3pp` | Hello World |
| `examples/fibonacci.c3pp` | Fibonacci numbers |
| `examples/classes.c3pp` | Classes, inheritance, methods |
| `examples/enums.c3pp` | Enums with name tables |
| `examples/faults.c3pp` | Faults and optional patterns |
| `examples/contracts.c3pp` | Contract programming |
| `examples/full.c3pp` | Comprehensive example |
| `examples/mathlib.c3ppi` | Math library interface |
| `examples/hello.c3ppi` | Simple interface example |

## Architecture

```
C3++ source (.c3pp)    Interface files (.c3ppi)
        │                       │
        ▼                       ▼
   c3ppc (Python) ──────────────┘
        │
        ▼
x86-64 assembly (.s)     ← AT&T GAS syntax
        │
        ▼
   gcc -o out out.s
        │
        ▼
   Native executable
```

## Bootstrap Compiler

The bootstrap compiler (`c3ppc-bootstrap`) is written in C3++ and transpiles C3++ to C:

```bash
# Build bootstrap
gcc -O2 -o c3ppc-bootstrap c3ppc/bootstrap/c3ppc_bootstrap.c

# Compile C3++ via bootstrap
./c3ppc-bootstrap examples/hello.c3pp -o hello.c
gcc -o hello hello.c
./hello

# Compile interface file
./c3ppc-bootstrap examples/mathlib.c3ppi -o mathlib.c
gcc -o mathlib mathlib.c
```

## Building

```bash
# Build bootstrap compiler
gcc -Wall -O2 -o c3ppc-bootstrap c3ppc/bootstrap/c3ppc_bootstrap.c

# Run full demo
bash c3ppc/bootstrap/demo.sh
```

## License

MIT License — see [LICENSE.md](LICENSE.md)
