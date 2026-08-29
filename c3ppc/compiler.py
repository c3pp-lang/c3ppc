"""
C3++ Compiler (c3ppc)
====================
C3++ to x86-64 assembly compiler.

C3++ has no preprocessor -- modules are imported, constants use ALL_CAPS const.
Generates x86-64 assembly, assembled with: gcc -o out out.s
"""

import sys
import os
import re
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class CompilerOptions:
    input_file: Optional[str] = None
    output_file: Optional[str] = None
    verbose: bool = False
    check_only: bool = False
    emit_c: bool = False
    is_interface: bool = False  # .c3ppi interface file


def _count_braces(line_text: str) -> int:
    depth = 0; j = 0
    in_str = in_char = in_lc = in_bc = False
    while j < len(line_text):
        ch = line_text[j]
        if in_bc:
            if ch == '*' and j + 1 < len(line_text) and line_text[j+1] == '/':
                in_bc = False; j += 2; continue
            j += 1; continue
        if in_lc: j += 1; continue
        if in_str:
            if ch == '\\' and j + 1 < len(line_text): j += 2; continue
            if ch == '"': in_str = False
            j += 1; continue
        if in_char:
            if ch == '\\' and j + 1 < len(line_text): j += 2; continue
            if ch == "'": in_char = False
            j += 1; continue
        if ch == '"': in_str = True
        elif ch == "'": in_char = True
        elif ch == '/' and j + 1 < len(line_text) and line_text[j+1] == '/':
            in_lc = True; j += 2; continue
        elif ch == '/' and j + 1 < len(line_text) and line_text[j+1] == '*':
            in_bc = True; j += 2; continue
        elif ch == '{': depth += 1
        elif ch == '}': depth -= 1
        j += 1
    return depth


class C3ppCompiler:
    """C3++ compiler: C3++ -> x86-64 assembly."""

    IMPORT_TO_HEADER = {
        'stdio': 'stdio.h', 'stdlib': 'stdlib.h', 'string': 'string.h',
        'math': 'math.h', 'ctype': 'ctype.h', 'time': 'time.h',
        'stdint': 'stdint.h', 'assert': 'assert.h',
        'std::io': 'stdio.h', 'std::lib': 'stdlib.h', 'std::string': 'string.h',
        'std::math': 'math.h', 'std::ctype': 'ctype.h', 'std::time': 'time.h',
        'std::stdint': 'stdint.h', 'std::assert': 'assert.h',
    }

    def __init__(self, options: Optional[CompilerOptions] = None):
        self._options = options or CompilerOptions()
        self._lexer = None

    def compile(self, source_code: str) -> str:
        if self._options.emit_c or self._options.is_interface:
            return self._compile_to_c(source_code)
        tokens = self._tokenize(source_code)
        parsed = self._parse_source(source_code, tokens)
        from c3ppc.codegen.asmgen import AsmGenerator
        return AsmGenerator().generate(parsed, source_code)

    def _is_raw_c_c3ppi(self, source_code: str) -> bool:
        """Detect if .c3ppi file contains raw C (vendor) vs C3++ syntax (interface)."""
        # Raw C files have #include, #define, typedef struct
        # C3++ interface files have fn, class, import, module
        raw_c_markers = ['#include', '#define', 'typedef struct', 'typedef enum']
        c3_markers = ['\nfn ', '\nclass ', '\nimport ', '\nmodule ']
        raw_score = sum(source_code.count(m) for m in raw_c_markers)
        c3_score = sum(source_code.count(m) for m in c3_markers)
        return raw_score > c3_score

    def _output_c3ppi_raw(self, source_code: str) -> str:
        """Output .c3ppi content as raw C, scanning for type names."""
        # Scan for struct/enum/class names so the main transpiler
        # knows to add 'struct'/'enum' prefixes in variable declarations
        lines = source_code.split('\n')
        for line in lines:
            s = line.strip()
            if s.startswith('typedef struct '):
                # typedef struct Foo { ... } Foo;
                parts = s.split()
                if len(parts) >= 3:
                    name = parts[2].rstrip('{').rstrip(';').strip()
                    if name and name not in ('{',):
                        self._known_classes.add(name)
            elif s.startswith('struct '):
                parts = s.split()
                if len(parts) >= 2:
                    name = parts[1].rstrip('{').strip()
                    if name and name not in ('{',):
                        self._known_classes.add(name)
            elif s.startswith('typedef enum '):
                parts = s.split()
                if len(parts) >= 3:
                    name = parts[2].rstrip('{').rstrip(';').strip()
                    if name and name not in ('{',):
                        self._known_classes.add(name)
                        self._enum_names.add(name)
            elif s.startswith('enum '):
                parts = s.split()
                if len(parts) >= 2:
                    name = parts[1].rstrip('{').strip()
                    if name and name not in ('{',):
                        self._known_classes.add(name)
                        self._enum_names.add(name)
        # Output as-is (raw C)
        return source_code

    def _compile_to_c_declarations(self, source_code: str) -> str:
        """Generate C declarations only from C3++ source (for imports)."""
        lines = source_code.split('\n')
        out = []
        # Save parent state
        saved_classes = self._known_classes.copy()
        saved_fields = dict(self._class_fields)
        saved_member_types = dict(self._known_member_types)
        saved_enum_names = self._enum_names.copy()
        self._known_classes = set()
        self._class_fields = {}
        self._known_member_types = {}
        self._enum_names = set()

        # Pre-scan: collect names
        i = 0
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith('class '):
                name = s.split()[1].split('{')[0].split('extends')[0].split('implements')[0].strip()
                self._known_classes.add(name)
                b, e = self._collect_block(lines, i)
                i = e; continue
            if s.startswith('struct '):
                name = s.split()[1].split('{')[0].strip()
                self._known_classes.add(name)
                b, e = self._collect_block(lines, i)
                i = e; continue
            if s.startswith('enum '):
                name = s.split()[1].split('{')[0].strip()
                self._known_classes.add(name)
                self._enum_names.add(name)
                b, e = self._collect_block(lines, i)
                i = e; continue
            i += 1

        # Emit declarations
        i = 0
        while i < len(lines):
            s = lines[i].strip()
            if not s or s.startswith('//'):
                i += 1; continue
            if s.startswith('module '):
                i += 1; continue
            if s.startswith('import '):
                i += 1; continue
            if s.startswith('const '):
                out.append(self._transpile_line(s)); i += 1; continue
            if s.startswith('fault '):
                out.append(self._transpile_line(s)); i += 1; continue
            if s.startswith('class '):
                block, i = self._collect_block(lines, i)
                lines2 = block.split('\n')
                first = lines2[0].strip()
                parts = first.split()
                class_name = parts[1]
                parent = None
                if 'extends' in first:
                    idx = parts.index('extends')
                    if idx + 1 < len(parts):
                        parent = parts[idx + 1].rstrip('{').strip()
                # Emit struct with member variables only
                out.append(f"struct {class_name} {{")
                if parent:
                    out.append(f"    struct {parent} _parent;")
                for l in lines2[1:]:
                    ms = l.strip()
                    if ms.startswith('fn '):
                        continue  # Methods handled below
                    elif ms == '}' or not ms:
                        continue
                    else:
                        member = ms.rstrip(';').strip()
                        member = re.sub(r'\bstring\b', 'char*', member)
                        member = re.sub(r'\bbool\b', 'int', member)
                        out.append(f"    {member};")
                out.append("};")
                out.append("")
                # Forward-declare methods as standalone functions
                for l in lines2[1:]:
                    ms = l.strip()
                    if ms.startswith('fn '):
                        rest = ms[3:].strip()
                        rest = re.sub(r'\s*@\w+\([^)]*\)', '', rest)
                        rest = re.sub(r'\bstring\b', 'char*', rest)
                        rest = re.sub(r'\bbool\b', 'int', rest)
                        parts2 = rest.split(None, 1)
                        ret_type = parts2[0] if parts2 else 'void'
                        if ret_type in self._known_classes:
                            ret_type = 'struct ' + ret_type
                        rest2 = parts2[1] if len(parts2) > 1 else ''
                        paren = rest2.find('(')
                        if paren >= 0:
                            method_name = rest2[:paren].strip()
                            params = rest2[paren+1:].rstrip(');').rstrip(')').strip()
                            params = self._add_struct_to_params(params, class_name)
                            out.append(f"{ret_type} {class_name}_{method_name}({params});")
                out.append("")
                continue
            if s.startswith('struct '):
                block, i = self._collect_block(lines, i)
                out.extend(self._transpile_struct(block, skip_new=True))
                continue
            if s.startswith('enum '):
                block, i = self._collect_block(lines, i)
                out.extend(self._transpile_enum(block))
                continue
            if s.startswith('fn '):
                # Emit function signature only (no body)
                rest = s[3:].strip()
                rest = re.sub(r'\s*@\w+\([^)]*\)', '', rest)
                rest = re.sub(r'\bstring\b', 'char*', rest)
                rest = re.sub(r'\bbool\b', 'int', rest)
                # Strip trailing { or ; and re-add ; without body
                rest = rest.rstrip().rstrip('{').rstrip().rstrip(';')
                # Add struct/enum prefix to return type and params
                rest = self._prefix_return_type(rest)
                rest = self._add_struct_to_params(rest, '')
                out.append(f"{rest};")
                i += 1; continue
            i += 1

        # Merge imported types back into parent state
        self._known_classes |= saved_classes
        self._class_fields.update(saved_fields)
        self._known_member_types.update(saved_member_types)
        self._enum_names |= saved_enum_names

        return '\n'.join(out) + '\n'

    def _resolve_import(self, module_name: str) -> Optional[str]:
        """Resolve an import to a .c3ppi or .c3pp file path."""
        if not self._options.input_file:
            return None
        base_dir = os.path.dirname(os.path.abspath(self._options.input_file))
        # Convert :: to / for path resolution (vendor::raylib6 -> vendor/raylib6)
        path_name = module_name.replace('::', '/')
        # Try .c3ppi first (interface), then .c3pp (implementation)
        for ext in ['.c3ppi', '.c3pp']:
            candidate = os.path.join(base_dir, path_name + ext)
            if os.path.exists(candidate):
                return candidate
        # Also try current working directory
        cwd = os.getcwd()
        for ext in ['.c3ppi', '.c3pp']:
            candidate = os.path.join(cwd, path_name + ext)
            if os.path.exists(candidate):
                return candidate
        return None

    def _compile_to_c(self, source_code: str) -> str:
        """Generate C code from C3++ source (block-aware transpilation)."""
        lines = source_code.split('\n')
        out = []
        self._known_classes = set()
        self._class_fields = {}  # class_name -> set of field names
        self._known_member_types = {}  # (class_name, field_name) -> type_string
        self._enum_names = set()
        out.append("/* Generated by c3ppc - C3++ to C compiler */")
        out.append("")

        # Pre-scan: collect class names for forward declarations
        class_names = []
        struct_names = []
        enum_names = []
        i = 0
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith('class '):
                name = s.split()[1].split('{')[0].split('extends')[0].split('implements')[0].strip()
                class_names.append(name)
                self._known_classes.add(name)
                b, e = self._collect_block(lines, i)
                i = e; continue
            if s.startswith('struct '):
                name = s.split()[1].split('{')[0].strip()
                struct_names.append(name)
                self._known_classes.add(name)
                b, e = self._collect_block(lines, i)
                i = e; continue
            if s.startswith('enum '):
                name = s.split()[1].split('{')[0].strip()
                enum_names.append(name)
                self._known_classes.add(name)
                self._enum_names.add(name)
                b, e = self._collect_block(lines, i)
                i = e; continue
            i += 1

        # Forward declarations
        for name in class_names:
            out.append(f"struct {name};")
        for name in struct_names:
            out.append(f"struct {name};")
        for name in enum_names:
            out.append(f"enum {name};")
        if class_names or struct_names or enum_names:
            out.append("")

        # Always include string.h for memset
        out.append("#include <string.h>")
        out.append("")

        # Transpile blocks
        i = 0
        while i < len(lines):
            s = lines[i].strip()
            if not s or s.startswith('//'):
                i += 1; continue
            if s.startswith('module '):
                out.append(f"/* {s} */"); i += 1; continue
            if s.startswith('import '):
                module_name = s.split('import')[1].split(';')[0].split('@')[0].strip()
                # Try to resolve module from .c3ppi/.c3pp files
                resolved = self._resolve_import(module_name)
                if resolved:
                    with open(resolved, 'r') as f:
                        dep_source = f.read()
                    if resolved.endswith('.c3ppi'):
                        # Check if .c3ppi is raw C (vendor) or C3++ syntax (interface)
                        if self._is_raw_c_c3ppi(dep_source):
                            dep_result = self._output_c3ppi_raw(dep_source)
                        else:
                            dep_result = self._compile_to_c_declarations(dep_source)
                    else:
                        # Implementation file: full compilation
                        dep_result = self._compile_to_c(dep_source)
                    out.append(f"/* === {module_name} ({os.path.basename(resolved)}) === */")
                    out.append(dep_result)
                else:
                    # Standard library import -> C header
                    out.append(self._transpile_line(s))
                i += 1; continue
            if s.startswith('const '):
                out.append(self._transpile_line(s)); i += 1; continue
            if s.startswith('class '):
                block, i = self._collect_block(lines, i)
                out.extend(self._transpile_class(block))
                continue
            if s.startswith('struct '):
                block, i = self._collect_block(lines, i)
                out.extend(self._transpile_struct(block))
                continue
            if s.startswith('enum '):
                block, i = self._collect_block(lines, i)
                out.extend(self._transpile_enum(block))
                continue
            if s.startswith('fn '):
                block, i = self._collect_function(lines, i)
                out.extend(self._transpile_fn(block))
                continue
            if s.startswith('alias '):
                out.append(self._transpile_line(s)); i += 1; continue
            # Regular statement
            out.append(self._transpile_line(s)); i += 1

        return '\n'.join(out) + '\n'

    def _transpile_class(self, block: str) -> list:
        """Transpile a class block to C struct + methods."""
        lines = block.split('\n')
        first = lines[0].strip()
        out = []

        # Parse: class Name [extends Parent] [implements Iface] {
        parts = first.split()
        class_name = parts[1]
        parent = None
        if 'extends' in first:
            idx = parts.index('extends')
            if idx + 1 < len(parts):
                parent = parts[idx + 1].rstrip('{').strip()

        out.append(f"/* class {class_name}" + (f" extends {parent}" if parent else "") + " */")

        # Collect body lines
        body_start = first.index('{')
        body_lines = [first[body_start:]]
        for l in lines[1:]:
            body_lines.append(l)

        # Parse members
        members = []
        methods = []
        constructor = None
        j = 1
        while j < len(lines):
            ms = lines[j].strip()
            if ms.startswith('fn '):
                # Method
                method_block, j = self._collect_function(lines, j)
                methods.append(method_block)
                continue
            if j + 1 < len(lines) and lines[j+1].strip().startswith('{'):
                # Could be constructor: ClassName(params) {
                ctor_block, j = self._collect_function(lines, j)
                constructor = ctor_block
                continue
            if ms == '}' or not ms:
                j += 1; continue
            members.append(ms)
            j += 1

        # Generate struct
        out.append(f"struct {class_name} {{")
        if parent:
            out.append(f"    struct {parent} _parent;  /* embedded parent */")
        for m in members:
            out.append(f"    {self._transpile_member_type(m)};" if not m.endswith(';') else f"    {m}")
        out.append("};")
        out.append("")

        # Track parent fields for inherited member access
        parent_fields = set()
        if parent and parent in self._class_fields:
            parent_fields = set(self._class_fields[parent])
        own_field_names = [m.split()[-1].rstrip(';') for m in members if m.strip()]
        all_fields = parent_fields | set(own_field_names)
        # Store fields in declaration order (parent first, then own)
        self._class_fields[class_name] = list(parent_fields) + own_field_names if parent_fields else own_field_names
        # Store member types for auto-constructor generation
        for m in members:
            s = m.strip().rstrip(';')
            parts = s.split(None, 1)
            if len(parts) == 2:
                self._known_member_types[(class_name, parts[1])] = parts[0]

        # Generate methods as ClassName_methodName
        for m in methods:
            out.extend(self._transpile_method(class_name, m, parent, parent_fields))

        # Generate constructor as ClassName_new (auto-generate if none defined)
        if constructor:
            out.extend(self._transpile_constructor(class_name, parent, constructor))
        else:
            out.extend(self._transpile_auto_constructor(class_name, parent, members, parent_fields))

        return out

    def _transpile_struct(self, block: str, skip_new: bool = False) -> list:
        """Transpile a struct block to C."""
        lines = block.split('\n')
        first = lines[0].strip()
        out = []
        struct_name = first.split()[1].rstrip('{').strip()
        out.append(f"struct {struct_name} {{")
        for l in lines[1:]:
            s = l.strip()
            if s == '}' or not s:
                continue
            if s.endswith(';'):
                # Already has semicolon - still need to add struct prefix
                out.append(f"    {self._transpile_member_type(s)};")
            else:
                out.append(f"    {self._transpile_member_type(s)};")
        out.append("};")
        out.append("")
        # Generate _new function (skip for .c3ppi interface files)
        if not skip_new:
            out.extend(self._transpile_struct_new(struct_name, lines))
        return out

    def _transpile_enum(self, block: str) -> list:
        """Transpile an enum block to C."""
        lines = block.split('\n')
        first = lines[0].strip()
        out = []
        enum_name = first.split()[1].rstrip('{').strip()
        out.append(f"enum {enum_name} {{")
        members = []
        member_names = []
        for l in lines[1:]:
            s = l.strip().rstrip(',')
            if s == '}' or not s:
                continue
            members.append(s)
            # Extract just the name (before = if present)
            name = s.split('=')[0].strip()
            member_names.append(name)
        out.append(",\n".join(f"    {m}" for m in members))
        out.append("};")
        out.append("")
        # Generate _names array for C3++ enum introspection
        out.append(f"static const char* {enum_name}_names[] = {{")
        out.append(",\n".join(f'    "{n}"' for n in member_names))
        out.append("};")
        # Generate _COUNT define
        out.append(f"#define {enum_name}_COUNT {len(member_names)}")
        out.append("")
        return out

    def _add_struct_to_params(self, params: str, class_name: str) -> str:
        """Add 'struct'/'enum' keyword to known types in params/return type."""
        for cname in self._known_classes:
            prefix = 'enum' if cname in self._enum_names else 'struct'
            # Pointer type: "Animal* self" -> "struct Animal* self"
            params = re.sub(rf'\b{cname}(\s*\*)', rf'{prefix} {cname}\1', params)
            # Value type in param list: "Vec2 name" -> "struct Vec2 name"
            params = re.sub(rf'([,(]\s*){cname}(\s+\w)', rf'\g<1>{prefix} {cname}\2', params)
        return params

    def _prefix_return_type(self, sig: str) -> str:
        """Add struct/enum prefix to return type in a function signature."""
        for cname in self._known_classes:
            prefix = 'enum' if cname in self._enum_names else 'struct'
            sig = re.sub(rf'^(\s*){cname}(\s+\w+\()', rf'\g<1>{prefix} {cname}\2', sig)
        return sig

    def _transpile_member_type(self, s: str) -> str:
        """Transpile a member declaration."""
        s = s.rstrip(';').strip()
        # Convert C3++ types to C
        s = re.sub(r'\bstring\b', 'char*', s)
        s = re.sub(r'\bbool\b', 'int', s)
        # Add struct/enum prefix for known types (skip if already prefixed)
        if self._known_classes:
            parts = s.split(None, 1)
            if parts:
                type_word = parts[0].lstrip('*')  # strip leading pointer stars
                if type_word in self._known_classes:
                    prefix = 'enum' if type_word in self._enum_names else 'struct'
                    if not s.startswith(f'{prefix} '):
                        s = f'{prefix} {s}'
        return s

    def _transpile_method(self, class_name: str, block: str, parent: str = None, parent_fields: set = None) -> list:
        """Transpile a method to a standalone C function."""
        lines = block.split('\n')
        out = []
        first = lines[0].strip()
        rest = first[3:].strip()  # strip 'fn '
        rest = re.sub(r'\bstring\b', 'char*', rest)
        rest = re.sub(r'\bbool\b', 'int', rest)
        paren_idx = rest.find('(')
        if paren_idx >= 0:
            header = rest[:paren_idx].strip()
            params_and_brace = rest[paren_idx+1:]
            close_paren = params_and_brace.find(')')
            params = params_and_brace[:close_paren].strip() if close_paren >= 0 else params_and_brace.strip()
        else:
            header = rest.strip()
            params = 'void'
        parts = header.split(None, 1)
        ret_type = parts[0] if parts else 'void'
        method_name = parts[1] if len(parts) > 1 else ''
        params = self._add_struct_to_params(params, class_name)
        out.append(f"{ret_type} {class_name}_{method_name}({params})")
        # Body — rewrite self->field to self->_parent.field for inherited members
        out.append("{")
        # Collect body lines, skipping empty ones and the final closing brace
        body_lines = []
        for l in lines[1:]:
            s = l.strip()
            if not s:
                continue
            body_lines.append(l)
        # Remove only the final closing brace (the method's own), not all trailing braces
        if body_lines and body_lines[-1].strip() == '}':
            body_lines.pop()
        for l in body_lines:
            s = l.strip()
            t = self._transpile_line(s)
            if parent_fields:
                for field in parent_fields:
                    t = t.replace(f'self->{field}', f'self->_parent.{field}')
            # Don't double-indent braces — _transpile_line already indents
            stripped = l.strip()
            if stripped.startswith('{') or stripped.startswith('}'):
                out.append(t)
            else:
                out.append(f"    {t}")
        out.append("}")
        out.append("")
        return out

    def _transpile_constructor(self, class_name: str, parent: str, block: str) -> list:
        """Transpile a constructor to ClassName_new function."""
        lines = block.split('\n')
        first = lines[0].strip()
        out = []
        # ConstructorName(params) -> struct ClassName ClassName_new(params)
        paren_idx = first.find('(')
        if paren_idx >= 0:
            params_and_brace = first[paren_idx+1:]
            close_paren = params_and_brace.find(')')
            params = params_and_brace[:close_paren].strip() if close_paren >= 0 else params_and_brace.strip()
        else:
            params = 'void'
        params = re.sub(r'\bstring\b', 'char*', params)
        params = re.sub(r'\bbool\b', 'int', params)
        out.append(f"struct {class_name} {class_name}_new({params})")
        out.append("{")
        out.append(f"    struct {class_name} _result;")
        out.append(f"    memset(&_result, 0, sizeof(struct {class_name}));")
        for l in lines[1:]:
            s = l.strip()
            if s == '}' or not s:
                continue
            t = self._transpile_line(s)
            t = t.replace('self->', '_result.')
            out.append(f"    {t}")
        out.append(f"    return _result;")
        out.append("}")
        out.append("")
        return out

    def _transpile_struct_new(self, struct_name: str, lines: list) -> list:
        """Generate a _new function for a struct."""
        out = []
        fields = []
        for l in lines[1:]:
            s = l.strip().rstrip(';')
            if s == '}' or not s:
                continue
            parts = s.split(None, 1)
            if len(parts) == 2:
                fields.append((parts[0], parts[1]))
        if not fields:
            return out
        params = ', '.join(f"{self._transpile_member_type(t)} {n}" for t, n in fields)
        out.append(f"struct {struct_name} {struct_name}_new({params})")
        out.append("{")
        out.append(f"    struct {struct_name} _result;")
        out.append(f"    memset(&_result, 0, sizeof(struct {struct_name}));")
        for _, n in fields:
            out.append(f"    _result.{n} = {n};")
        out.append(f"    return _result;")
        out.append("}")
        out.append("")
        return out

    def _transpile_auto_constructor(self, class_name: str, parent: str, members: list, parent_fields: set) -> list:
        """Auto-generate a _new constructor for a class based on its fields."""
        out = []
        # Collect own fields with their types
        own_fields = []
        for m in members:
            s = m.strip().rstrip(';')
            parts = s.split(None, 1)
            if len(parts) == 2:
                own_fields.append((parts[0], parts[1]))
        # Get parent fields as (type, name) tuples from parent's own members
        parent_params = []
        if parent and parent in self._class_fields:
            # Use ordered field list from parent
            for pname in self._class_fields[parent]:
                ptype = self._known_member_types.get((parent, pname), 'int')
                parent_params.append((ptype, pname))
        all_params = parent_params + own_fields
        if not all_params:
            return out
        params = ', '.join(f"{self._transpile_member_type(t)} {n}" for t, n in all_params)
        out.append(f"struct {class_name} {class_name}_new({params})")
        out.append("{")
        out.append(f"    struct {class_name} _result;")
        out.append(f"    memset(&_result, 0, sizeof(struct {class_name}));")
        for t, n in all_params:
            if parent and parent_fields and n in parent_fields:
                out.append(f"    _result._parent.{n} = {n};")
            else:
                out.append(f"    _result.{n} = {n};")
        out.append(f"    return _result;")
        out.append("}")
        out.append("")
        return out

    def _transpile_fn(self, block: str) -> list:
        """Transpile a function block."""
        lines = block.split('\n')
        first = lines[0].strip()
        out = []
        # Strip @require/@ensure annotations from function signature
        first = re.sub(r'\s*@\w+\([^)]*\)', '', first)
        rest = first[3:].strip()  # strip 'fn '
        if rest.startswith('void main'):
            rest = 'int main' + rest[9:]
        rest = re.sub(r'\bstring\b', 'char*', rest)
        rest = re.sub(r'\bbool\b', 'int', rest)
        # Apply struct/enum prefix to return type and params
        if self._known_classes:
            for cname in self._known_classes:
                prefix = 'enum' if cname in self._enum_names else 'struct'
                # Return type: "Vec2 funcname" -> "struct Vec2 funcname"
                rest = re.sub(rf'^(\s*){cname}(\s+\w+\()', rf'\g<1>{prefix} {cname}\2', rest)
                # Pointer param: "Vec2* p" -> "struct Vec2* p"
                rest = re.sub(rf'({cname})(\s*\*)', rf'{prefix} \1\2', rest)
                # Value param: inside parens, "Vec2 name" -> "struct Vec2 name"
                rest = re.sub(rf'([,(]\s*){cname}(\s+\w)', rf'\g<1>{prefix} {cname}\2', rest)
        out.append(rest)
        for l in lines[1:]:
            s = l.strip()
            if not s:
                out.append("")
                continue
            t = self._transpile_line(s)
            stripped = l.strip()
            out.append(f"    {t}" if not stripped.startswith('{') and not stripped.startswith('}') else t)
        return out

    @staticmethod
    def _strip_ns_outside_strings(s: str) -> str:
        """Strip module::prefix only outside string literals."""
        result = []
        i = 0
        while i < len(s):
            if s[i] == '"':
                # Copy the entire string literal as-is
                result.append(s[i])
                i += 1
                while i < len(s) and s[i] != '"':
                    if s[i] == '\\':
                        result.append(s[i:i+2])
                        i += 2
                    else:
                        result.append(s[i])
                        i += 1
                if i < len(s):
                    result.append(s[i])
                    i += 1
            elif s[i] == "'":
                # Copy char literal as-is
                result.append(s[i])
                i += 1
                while i < len(s) and s[i] != "'":
                    if s[i] == '\\':
                        result.append(s[i:i+2])
                        i += 2
                    else:
                        result.append(s[i])
                        i += 1
                if i < len(s):
                    result.append(s[i])
                    i += 1
            else:
                # Check for module::identifier pattern
                if s[i].isalpha() or s[i] == '_':
                    # Read word
                    start = i
                    while i < len(s) and (s[i].isalnum() or s[i] == '_'):
                        i += 1
                    word = s[start:i]
                    # Check if followed by ::
                    if i + 1 < len(s) and s[i] == ':' and s[i+1] == ':':
                        # Skip the word and ::
                        i += 2
                    else:
                        result.append(word)
                else:
                    result.append(s[i])
                    i += 1
        return ''.join(result)

    def _transpile_line(self, s: str) -> str:
        """Transpile one C3++ line to C."""
        # import std::io -> #include <stdio.h>
        if s.startswith('import '):
            p = s[7:].rstrip(';').strip()
            mapping = {
                'std::io': 'stdio.h', 'std::lib': 'stdlib.h',
                'std::string': 'string.h', 'std::math': 'math.h',
                'stdio': 'stdio.h', 'stdlib': 'stdlib.h',
                'string': 'string.h', 'math': 'math.h',
            }
            header = mapping.get(p, f'{p}.h')
            return f'#include <{header}>'

        # module -> comment
        if s.startswith('module '):
            return f'/* {s} */'

        # const [TYPE] NAME = VALUE; -> #define NAME VALUE
        if s.startswith('const '):
            p = s[6:].rstrip(';').strip()
            eq = p.find('=')
            if eq >= 0:
                lhs = p[:eq].strip()
                val = p[eq+1:].strip()
                parts = lhs.split()
                if len(parts) >= 2:
                    # Skip primitive type keywords or known struct/enum types
                    known_types = self._known_classes | {'int', 'float', 'double', 'char', 'unsigned', 'long', 'short', 'bool', 'size_t'}
                    # Consume all leading type words (handles unsigned int, etc.)
                    idx = 0
                    while idx < len(parts) and parts[idx] in known_types:
                        idx += 1
                    if idx > 0 and idx < len(parts):
                        name = parts[idx]
                    elif idx == 0:
                        name = lhs
                    else:
                        name = parts[-1]
                else:
                    name = lhs
                return f'#define {name} {val}'
            return f'/* {s} */'

        # fault NAME = VALUE; -> #define NAME VALUE
        if s.startswith('fault '):
            p = s[6:].rstrip(';').strip()
            eq = p.find('=')
            if eq >= 0:
                name = p[:eq].strip()
                val = p[eq+1:].strip()
                return f'#define {name} ({val})'
            return f'/* {s} */'

        # fn TYPE NAME(...) @require(...) @ensure(...) { -> TYPE NAME(...) {
        if s.startswith('fn '):
            s = re.sub(r'\s*@\w+\([^)]*\)', '', s)
            rest = s[3:]  # strip 'fn '
            # fn void main() -> int main()
            if rest.startswith('void main'):
                rest = 'int main' + rest[9:]
            # Generic: strip fn, convert types
            result = ''
            i = 0
            while i < len(rest):
                if rest[i:].startswith('string[]'):
                    result += 'char**'; i += 8
                elif rest[i:].startswith('string'):
                    result += 'char*'; i += 6
                elif rest[i:].startswith('bool'):
                    result += 'int'; i += 4
                else:
                    result += rest[i]; i += 1
            return result

        # io::printn("text") -> printf("text\n")
        m = re.match(r'io::printn\s*\(\s*"([^"]*)"\s*\);', s)
        if m:
            return f'    printf("{m.group(1)}\\n");'

        # io::print("text") -> printf("text")
        m = re.match(r'io::print\s*\(\s*"([^"]*)"\s*\);', s)
        if m:
            return f'    printf("{m.group(1)}");'

        # io::printfn("fmt", args) -> printf("fmt\n", args)
        if s.startswith('io::printfn("'):
            # Find the closing quote of the format string
            rest_after_io = s[12:]  # after io::printfn(
            # Find the first unescaped quote
            i = 1  # skip opening quote
            while i < len(rest_after_io):
                if rest_after_io[i] == '\\':
                    i += 2; continue
                if rest_after_io[i] == '"': break
                i += 1
            fmt = rest_after_io[1:i]  # format string without quotes
            args_part = rest_after_io[i+1:].strip()
            # Strip only the trailing ");" not individual ) or ;
            if args_part.endswith(');'):
                args_part = args_part[:-2].strip()
            elif args_part.endswith(')'):
                args_part = args_part[:-1].strip()
            if args_part.startswith(','):
                args_part = args_part[1:].strip()
            if args_part:
                return f'    printf("{fmt}\\n", {args_part});'
            return f'    printf("{fmt}\\n");'

        # Strip @require/@ensure annotations
        s = re.sub(r'\s*@\w+\([^)]*\)', '', s)

        # Suppress gcc -Wunused-result warnings on bare fread() calls
        s = re.sub(r'fread\(([^)]+)\)',
                   r'{ size_t _r = fread(\1); (void)_r; }', s)

        # Strip module namespace prefix: raylib6::InitWindow() -> InitWindow()
        # Skip string literals to avoid breaking pattern-matching strings
        s = self._strip_ns_outside_strings(s)

        # Add 'struct' or 'enum' keyword for known types in variable declarations
        if self._known_classes:
            for cname in self._known_classes:
                if cname in self._enum_names:
                    prefix = 'enum'
                else:
                    prefix = 'struct'
                s = re.sub(rf'\b{cname}(\s+\w+\s*[=;])', rf'{prefix} {cname}\1', s)

        # Everything else: pass through with indent
        return f'    {s}'

    def _tokenize(self, source_code):
        from c3ppc.lexer.lexer import create_c3pp_lexer
        self._lexer = create_c3pp_lexer()
        return self._lexer.tokenize(source_code)

    def _parse_source(self, source_code, tokens):
        parsed = {'module': '', 'imports': [], 'functions': [], 'constants': [],
                  'globals': [], 'classes': [], 'enums': [], 'faults': [], 'typedefs': []}
        lines = source_code.split('\n')
        i = 0
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith('//') or not s: i += 1; continue
            if s.startswith('module '):
                parsed['module'] = s[7:].rstrip(';').strip(); i += 1; continue
            if s.startswith('import '):
                imp = s[7:].rstrip(';').strip()
                parsed['imports'].append(imp); i += 1; continue
            if s.startswith('fault '):
                parsed['faults'].append(s); i += 1; continue
            if s.startswith('enum '):
                b, e = self._collect_block(lines, i); parsed['enums'].append({'code': b}); i = e; continue
            if s.startswith('class ') or s.startswith('struct '):
                b, e = self._collect_block(lines, i); parsed['classes'].append({'code': b}); i = e; continue
            if s.startswith('const '):
                parsed['constants'].append(s); i += 1; continue
            if s.startswith('fn '):
                b, e = self._collect_function(lines, i); parsed['functions'].append({'code': b}); i = e; continue
            if s.startswith('alias '):
                parsed['typedefs'].append(s); i += 1; continue
            if re.match(r'^[\w*\[\]<>?]+\s+\w+(\s*\[.*?\])?\s*[=;(]', s):
                parsed['globals'].append(s); i += 1; continue
            i += 1
        return parsed

    def _collect_block(self, lines, start):
        r = []; d = 0; f = False
        for idx in range(start, len(lines)):
            r.append(lines[idx]); d += _count_braces(lines[idx])
            if d > 0: f = True
            if f and d <= 0: return '\n'.join(r), idx + 1
        return '\n'.join(r), len(lines)

    def _collect_function(self, lines, start):
        r = []; d = 0; f = False
        for idx in range(start, len(lines)):
            r.append(lines[idx]); d += _count_braces(lines[idx])
            if '{' in lines[idx] and '}' in lines[idx] and not f: f = True
            if d > 0: f = True
            if f and d <= 0: return '\n'.join(r), idx + 1
        return '\n'.join(r), len(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="c3ppc - C3++ to x86-64 assembly compiler",
        epilog="Generates x86-64 assembly (.s), assembled with: gcc -o out out.s",
    )
    parser.add_argument("input_file", help="Input C3++ source file (.c3pp or .c3ppi)")
    parser.add_argument("-o", "--output", help="Output file (.s or .c)")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--c", action="store_true",
                        help="Generate C code instead of x86-64 assembly")
    parser.add_argument("--interface", action="store_true",
                        help="Compile .c3ppi interface file (declarations only)")
    parser.add_argument("--version", action="version", version="c3ppc 5.0.0")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: '{args.input_file}' not found", file=sys.stderr); sys.exit(1)
    try:
        with open(args.input_file, 'r') as f: source_code = f.read()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); sys.exit(1)

    options = CompilerOptions(input_file=args.input_file, output_file=args.output,
                              verbose=args.verbose, emit_c=getattr(args, 'c', False),
                              is_interface=getattr(args, 'interface', False))
    compiler = C3ppCompiler(options)
    try:
        result = compiler.compile(source_code)
        if result:
            if args.output:
                with open(args.output, 'w') as f: f.write(result)
                if args.verbose: print(f"Written to {args.output}")
            else:
                print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose: import traceback; traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
