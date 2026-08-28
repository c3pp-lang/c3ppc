# C3++ Bootstrap Compiler Makefile
ROOT = ../..
PYTHON = python3
export PYTHONPATH = $(ROOT)

.PHONY: all clean test chain

all: c3ppc-bootstrap

# Step 1: Python compiler builds bootstrap from C3++ source (generates C)
c3ppc-bootstrap.c: $(ROOT)/c3ppc/bootstrap/compiler.c3pp $(ROOT)/c3ppc/compiler.py
	$(PYTHON) $(ROOT)/c3ppc/compiler.py --c $(ROOT)/c3ppc/bootstrap/compiler.c3pp -o c3ppc-bootstrap.c

c3ppc-bootstrap: c3ppc-bootstrap.c
	gcc -Wall -O2 -o c3ppc-bootstrap c3ppc-bootstrap.c

# Test: compile hello.c3pp through bootstrap
test: c3ppc-bootstrap
	./c3ppc-bootstrap $(ROOT)/c3ppc/examples/hello.c3pp -o hello.c
	gcc -o hello hello.c
	./hello

# Full bootstrapping chain
chain: c3ppc-bootstrap
	@echo "=== Step 1: Python builds bootstrap ==="
	@echo "=== Step 2: Bootstrap compiles hello ==="
	./c3ppc-bootstrap $(ROOT)/c3ppc/examples/hello.c3pp -o hello.c
	gcc -o hello hello.c
	./hello
	@echo "=== Step 3: Bootstrap self-compiles ==="
	./c3ppc-bootstrap $(ROOT)/c3ppc/bootstrap/compiler.c3pp -o c3ppc-second.c
	gcc -Wall -O2 -o c3ppc-second c3ppc-second.c
	@echo "=== Step 4: Self-compiled compiles hello ==="
	./c3ppc-second $(ROOT)/c3ppc/examples/hello.c3pp -o hello2.c
	gcc -o hello2 hello2.c
	./hello2
	@echo "=== Chain complete ✓ ==="

# Demo (comprehensive)
demo:
	bash $(ROOT)/c3ppc/bootstrap/demo.sh

clean:
	rm -f c3ppc-bootstrap c3ppc-bootstrap.c c3ppc-second c3ppc-second.c
	rm -f hello hello.c hello2 hello2.c fibonacci fibonacci.s
