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

## Architecture

```
C3++ source (.c3pp)
        │
        ▼
   c3ppc (Python)
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
