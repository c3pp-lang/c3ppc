#!/bin/bash
# C3++ Bootstrapping Demo
set -e

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "╔══════════════════════════════════════════════════╗"
echo "║         C3++ Bootstrapping Demo v4.0             ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

echo "Step 1: Build bootstrap compiler (C3++ → C → gcc)"
gcc -Wall -O2 -o "$ROOT/c3ppc/bootstrap/c3ppc-bootstrap" "$ROOT/c3ppc/bootstrap/c3ppc_bootstrap.c"
echo "  ✓ c3ppc-bootstrap built"
echo ""

echo "Step 2: Bootstrap compiles hello.c3pp → C → executable"
"$ROOT/c3ppc/bootstrap/c3ppc-bootstrap" "$ROOT/c3ppc/examples/hello.c3pp" -o "$ROOT/c3ppc/bootstrap/hello.c"
gcc -o "$ROOT/c3ppc/bootstrap/hello" "$ROOT/c3ppc/bootstrap/hello.c"
echo "  ✓ hello built"
echo ""

echo "Step 3: Run hello"
"$ROOT/c3ppc/bootstrap/hello"
echo ""

echo "Step 4: Python compiler compiles fibonacci → x86-64 ASM → executable"
"$ROOT/venv/bin/python3" "$ROOT/c3ppc/compiler.py" "$ROOT/c3ppc/examples/fibonacci.c3pp" -o "$ROOT/c3ppc/bootstrap/fibonacci.s"
gcc -o "$ROOT/c3ppc/bootstrap/fibonacci" "$ROOT/c3ppc/bootstrap/fibonacci.s"
echo "  ✓ fibonacci built (ASM backend)"
echo ""

echo "Step 5: Run fibonacci"
"$ROOT/c3ppc/bootstrap/fibonacci" | head -5
echo "  ..."
echo ""

echo "══════════════════════════════════════════════════"
echo "Pipeline complete ✓"
echo ""
echo "  c3ppc (Python) → x86-64 ASM → executable"
echo "  c3ppc-bootstrap (C3++ → C)  → gcc → executable"
echo "══════════════════════════════════════════════════"
