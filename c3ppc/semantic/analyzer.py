"""
C3++ Semantic Analyzer
======================
Semantic analysis for the C3++ programming language.
Performs type checking, scope resolution, and other semantic validations.
"""

from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from c3ppc.ast_nodes.nodes import (
    ProgramAST, ModuleDeclAST, ImportDeclAST,
    BinaryExprAST, UnaryExprAST, AssignmentExprAST,
    CallExprAST, MemberExprAST, IndexExprAST,
    NewExprAST, ThisExprAST, SuperExprAST,
    IdentifierExprAST, LiteralAST,
    BlockAST, IfStatementAST, WhileStatementAST,
    ForStatementAST, ForeachStatementAST,
    SwitchStatementAST, CaseClauseAST,
    ReturnStatementAST, BreakStatementAST,
    ContinueStatementAST, DeferStatementAST,
    ExpressionStatementAST,
    VarDeclAST, FnDeclAST, FnParamAST,
    BasicTypeAST, PointerTypeAST, ArrayTypeAST,
    SliceTypeAST, FunctionTypeAST,
    ClassDeclAST, ClassBodyAST,
    ConstructorDeclAST, DestructorDeclAST,
    StructDeclAST, StructBodyAST,
    EnumDeclAST, EnumMemberAST,
    InterfaceDeclAST, InterfaceBodyAST,
    BaseAST
)


class SemanticError:
    """Represents a semantic error."""
    
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
    
    def __str__(self) -> str:
        return f"Semantic Error at line {self.line}, column {self.column}: {self.message}"


class SymbolKind(Enum):
    """Kind of symbol in the symbol table."""
    VARIABLE = auto()
    FUNCTION = auto()
    CLASS = auto()
    STRUCT = auto()
    ENUM = auto()
    INTERFACE = auto()
    PARAMETER = auto()
    METHOD = auto()


@dataclass
class SymbolInfo:
    """Information about a symbol."""
    name: str
    kind: SymbolKind
    type_name: Optional[str] = None
    line: int = 0
    column: int = 0
    is_const: bool = False
    is_static: bool = False
    is_virtual: bool = False
    access_modifier: Optional[str] = None
    parent_class: Optional[str] = None
    parameters: List['SymbolInfo'] = field(default_factory=list)
    return_type: Optional[str] = None


class Scope:
    """Represents a lexical scope."""
    
    def __init__(self, parent: Optional['Scope'] = None):
        self._symbols: Dict[str, SymbolInfo] = {}
        self._parent = parent
    
    def define(self, name: str, info: SymbolInfo) -> bool:
        """Define a new symbol in this scope. Returns False if already defined."""
        if name in self._symbols:
            return False
        self._symbols[name] = info
        return True
    
    def lookup(self, name: str) -> Optional[SymbolInfo]:
        """Look up a symbol, checking parent scopes."""
        if name in self._symbols:
            return self._symbols[name]
        if self._parent:
            return self._parent.lookup(name)
        return None
    
    def lookup_local(self, name: str) -> Optional[SymbolInfo]:
        """Look up a symbol only in this scope."""
        return self._symbols.get(name)
    
    def get_all_symbols(self) -> Dict[str, SymbolInfo]:
        """Get all symbols in this scope (not including parents)."""
        return self._symbols.copy()


class SymbolTable:
    """Manages scopes and symbols."""
    
    def __init__(self):
        self._global_scope = Scope()
        self._current_scope = self._global_scope
        self._class_stack: List[str] = []
    
    def push_scope(self) -> Scope:
        """Create and enter a new scope."""
        new_scope = Scope(self._current_scope)
        self._current_scope = new_scope
        return new_scope
    
    def pop_scope(self) -> Scope:
        """Exit the current scope and return to parent."""
        if self._current_scope._parent:
            self._current_scope = self._current_scope._parent
        return self._current_scope
    
    def define(self, name: str, info: SymbolInfo) -> bool:
        """Define a symbol in the current scope."""
        return self._current_scope.define(name, info)
    
    def lookup(self, name: str) -> Optional[SymbolInfo]:
        """Look up a symbol in the current and parent scopes."""
        return self._current_scope.lookup(name)
    
    def enter_class(self, class_name: str):
        """Enter a class context."""
        self._class_stack.append(class_name)
    
    def exit_class(self):
        """Exit a class context."""
        if self._class_stack:
            self._class_stack.pop()
    
    @property
    def current_class(self) -> Optional[str]:
        """Get the current class name, if any."""
        return self._class_stack[-1] if self._class_stack else None


class SemanticAnalyzer:
    """
    Semantic analyzer for C3++ programs.
    
    Performs:
    - Type checking
    - Scope resolution
    - Access control validation
    - Method resolution
    - Inheritance validation
    """
    
    def __init__(self):
        self._symbol_table = SymbolTable()
        self._errors: List[SemanticError] = []
        self._current_return_type: Optional[str] = None
        self._in_loop: bool = False
        self._in_switch: bool = False
    
    def analyze(self, program: ProgramAST) -> List[SemanticError]:
        """
        Analyze a program AST.
        
        Args:
            program: Root AST node of the program
            
        Returns:
            List of semantic errors found
        """
        self._errors = []
        self._visit_program(program)
        return self._errors
    
    def _error(self, message: str, line: int, column: int):
        """Record a semantic error."""
        self._errors.append(SemanticError(message, line, column))
    
    def _visit_program(self, node: ProgramAST):
        """Visit program node."""
        # Process module declaration
        if node.module:
            self._symbol_table.define(node.module.name, SymbolInfo(
                name=node.module.name,
                kind=SymbolKind.VARIABLE,
                line=node.module.line,
                column=node.module.column
            ))
        
        # Process imports
        for import_decl in node.imports:
            self._visit_import(import_decl)
        
        # Process declarations
        for decl in node.declarations:
            self._visit_declaration(decl)
    
    def _visit_import(self, node: ImportDeclAST):
        """Visit import declaration."""
        # TODO: Implement import resolution
        pass
    
    def _visit_declaration(self, node: BaseAST):
        """Visit declaration node."""
        if isinstance(node, VarDeclAST):
            self._visit_var_decl(node)
        elif isinstance(node, FnDeclAST):
            self._visit_fn_decl(node)
        elif isinstance(node, ClassDeclAST):
            self._visit_class_decl(node)
        elif isinstance(node, StructDeclAST):
            self._visit_struct_decl(node)
        elif isinstance(node, EnumDeclAST):
            self._visit_enum_decl(node)
        elif isinstance(node, InterfaceDeclAST):
            self._visit_interface_decl(node)
    
    def _visit_var_decl(self, node: VarDeclAST):
        """Visit variable declaration."""
        # Check if already defined in current scope
        existing = self._symbol_table.lookup_local(node.name)
        if existing:
            self._error(f"Variable '{node.name}' already defined", node.line, node.column)
            return
        
        # Determine type
        type_name = None
        if node.type_annotation:
            type_name = self._get_type_name(node.type_annotation)
        
        # Check initializer
        if node.initializer:
            init_type = self._visit_expression(node.initializer)
            if type_name and init_type and type_name != init_type:
                self._error(f"Type mismatch: expected {type_name}, got {init_type}",
                           node.line, node.column)
        
        # Add to symbol table
        info = SymbolInfo(
            name=node.name,
            kind=SymbolKind.VARIABLE,
            type_name=type_name,
            line=node.line,
            column=node.column,
            is_const=node.is_const
        )
        self._symbol_table.define(node.name, info)
    
    def _visit_fn_decl(self, node: FnDeclAST):
        """Visit function declaration."""
        # Check if already defined
        existing = self._symbol_table.lookup_local(node.name)
        if existing:
            self._error(f"Function '{node.name}' already defined", node.line, node.column)
            return
        
        # Determine return type
        return_type = None
        if node.return_type:
            return_type = self._get_type_name(node.return_type)
        
        # Add to symbol table
        info = SymbolInfo(
            name=node.name,
            kind=SymbolKind.FUNCTION,
            return_type=return_type,
            line=node.line,
            column=node.column,
            is_virtual=node.is_virtual,
            access_modifier=node.access_modifier,
            is_static=node.is_static,
            parent_class=self._symbol_table.current_class
        )
        self._symbol_table.define(node.name, info)
        
        # Visit body if present
        if node.body:
            self._symbol_table.push_scope()
            
            # Add parameters to scope
            for param in node.params:
                param_type = self._get_type_name(param.type_annotation)
                param_info = SymbolInfo(
                    name=param.name,
                    kind=SymbolKind.PARAMETER,
                    type_name=param_type,
                    line=param.line,
                    column=param.column
                )
                self._symbol_table.define(param.name, param_info)
            
            # Visit body
            old_return_type = self._current_return_type
            self._current_return_type = return_type
            self._visit_statement(node.body)
            self._current_return_type = old_return_type
            
            self._symbol_table.pop_scope()
    
    def _visit_class_decl(self, node: ClassDeclAST):
        """Visit class declaration."""
        # Check if already defined
        existing = self._symbol_table.lookup_local(node.name)
        if existing:
            self._error(f"Class '{node.name}' already defined", node.line, node.column)
            return
        
        # Add to symbol table
        info = SymbolInfo(
            name=node.name,
            kind=SymbolKind.CLASS,
            line=node.line,
            column=node.column,
            access_modifier=node.access_modifier
        )
        self._symbol_table.define(node.name, info)
        
        # Check base class exists
        if node.base_class:
            base = self._symbol_table.lookup(node.base_class)
            if not base or base.kind != SymbolKind.CLASS:
                self._error(f"Base class '{node.base_class}' not found",
                           node.line, node.column)
        
        # Check interfaces exist
        for iface in node.implements:
            iface_info = self._symbol_table.lookup(iface)
            if not iface_info or iface_info.kind != SymbolKind.INTERFACE:
                self._error(f"Interface '{iface}' not found",
                           node.line, node.column)
        
        # Visit body
        self._symbol_table.enter_class(node.name)
        self._symbol_table.push_scope()
        
        if node.body:
            for member in node.body.members:
                self._visit_declaration(member)
        
        self._symbol_table.pop_scope()
        self._symbol_table.exit_class()
    
    def _visit_struct_decl(self, node: StructDeclAST):
        """Visit struct declaration."""
        existing = self._symbol_table.lookup_local(node.name)
        if existing:
            self._error(f"Struct '{node.name}' already defined", node.line, node.column)
            return
        
        info = SymbolInfo(
            name=node.name,
            kind=SymbolKind.STRUCT,
            line=node.line,
            column=node.column,
            access_modifier=node.access_modifier
        )
        self._symbol_table.define(node.name, info)
        
        if node.body:
            self._symbol_table.push_scope()
            for member in node.body.members:
                self._visit_var_decl(member)
            self._symbol_table.pop_scope()
    
    def _visit_enum_decl(self, node: EnumDeclAST):
        """Visit enum declaration."""
        existing = self._symbol_table.lookup_local(node.name)
        if existing:
            self._error(f"Enum '{node.name}' already defined", node.line, node.column)
            return
        
        info = SymbolInfo(
            name=node.name,
            kind=SymbolKind.ENUM,
            line=node.line,
            column=node.column,
            access_modifier=node.access_modifier
        )
        self._symbol_table.define(node.name, info)
    
    def _visit_interface_decl(self, node: InterfaceDeclAST):
        """Visit interface declaration."""
        existing = self._symbol_table.lookup_local(node.name)
        if existing:
            self._error(f"Interface '{node.name}' already defined", node.line, node.column)
            return
        
        info = SymbolInfo(
            name=node.name,
            kind=SymbolKind.INTERFACE,
            line=node.line,
            column=node.column,
            access_modifier=node.access_modifier
        )
        self._symbol_table.define(node.name, info)
        
        # Check extended interfaces
        for iface in node.extends:
            iface_info = self._symbol_table.lookup(iface)
            if not iface_info or iface_info.kind != SymbolKind.INTERFACE:
                self._error(f"Interface '{iface}' not found",
                           node.line, node.column)
        
        # Visit body
        if node.body:
            for member in node.body.members:
                if isinstance(member, FnDeclAST):
                    # Interfaces only have method signatures (no body)
                    self._visit_fn_decl(member)
    
    def _visit_statement(self, node: BaseAST):
        """Visit statement node."""
        if isinstance(node, BlockAST):
            self._visit_block(node)
        elif isinstance(node, IfStatementAST):
            self._visit_if_statement(node)
        elif isinstance(node, WhileStatementAST):
            self._visit_while_statement(node)
        elif isinstance(node, ForStatementAST):
            self._visit_for_statement(node)
        elif isinstance(node, ForeachStatementAST):
            self._visit_foreach_statement(node)
        elif isinstance(node, SwitchStatementAST):
            self._visit_switch_statement(node)
        elif isinstance(node, ReturnStatementAST):
            self._visit_return_statement(node)
        elif isinstance(node, BreakStatementAST):
            if not self._in_loop and not self._in_switch:
                self._error("break statement not in loop or switch",
                           node.line, node.column)
        elif isinstance(node, ContinueStatementAST):
            if not self._in_loop:
                self._error("continue statement not in loop",
                           node.line, node.column)
        elif isinstance(node, DeferStatementAST):
            self._visit_statement(node.statement)
        elif isinstance(node, ExpressionStatementAST):
            self._visit_expression(node.expression)
        elif isinstance(node, VarDeclAST):
            self._visit_var_decl(node)
        elif isinstance(node, FnDeclAST):
            self._visit_fn_decl(node)
    
    def _visit_block(self, node: BlockAST):
        """Visit block statement."""
        self._symbol_table.push_scope()
        for stmt in node.statements:
            self._visit_statement(stmt)
        self._symbol_table.pop_scope()
    
    def _visit_if_statement(self, node: IfStatementAST):
        """Visit if statement."""
        cond_type = self._visit_expression(node.condition)
        if cond_type and cond_type != 'bool':
            self._error(f"Condition must be bool, got {cond_type}",
                       node.line, node.column)
        
        self._visit_statement(node.then_block)
        if node.else_block:
            self._visit_statement(node.else_block)
    
    def _visit_while_statement(self, node: WhileStatementAST):
        """Visit while statement."""
        cond_type = self._visit_expression(node.condition)
        if cond_type and cond_type != 'bool':
            self._error(f"Condition must be bool, got {cond_type}",
                       node.line, node.column)
        
        old_in_loop = self._in_loop
        self._in_loop = True
        self._visit_statement(node.body)
        self._in_loop = old_in_loop
    
    def _visit_for_statement(self, node: ForStatementAST):
        """Visit for statement."""
        self._symbol_table.push_scope()
        
        if node.init:
            self._visit_statement(node.init)
        
        if node.condition:
            cond_type = self._visit_expression(node.condition)
            if cond_type and cond_type != 'bool':
                self._error(f"Condition must be bool, got {cond_type}",
                           node.line, node.column)
        
        if node.update:
            self._visit_expression(node.update)
        
        old_in_loop = self._in_loop
        self._in_loop = True
        self._visit_statement(node.body)
        self._in_loop = old_in_loop
        
        self._symbol_table.pop_scope()
    
    def _visit_foreach_statement(self, node: ForeachStatementAST):
        """Visit foreach statement."""
        self._symbol_table.push_scope()
        
        # TODO: Determine element type from iterable
        iter_type = self._visit_expression(node.iterable)
        
        # Add loop variable to scope
        var_info = SymbolInfo(
            name=node.variable,
            kind=SymbolKind.VARIABLE,
            type_name=iter_type,  # Simplified
            line=node.line,
            column=node.column
        )
        self._symbol_table.define(node.variable, var_info)
        
        old_in_loop = self._in_loop
        self._in_loop = True
        self._visit_statement(node.body)
        self._in_loop = old_in_loop
        
        self._symbol_table.pop_scope()
    
    def _visit_switch_statement(self, node: SwitchStatementAST):
        """Visit switch statement."""
        expr_type = self._visit_expression(node.expression)
        
        old_in_switch = self._in_switch
        self._in_switch = True
        
        for case in node.cases:
            case_type = self._visit_expression(case.value)
            if expr_type and case_type and expr_type != case_type:
                self._error(f"Case type mismatch: expected {expr_type}, got {case_type}",
                           case.line, case.column)
            
            for stmt in case.statements:
                self._visit_statement(stmt)
        
        if node.default:
            for stmt in node.default:
                if isinstance(stmt, BaseAST):
                    self._visit_statement(stmt)
        
        self._in_switch = old_in_switch
    
    def _visit_return_statement(self, node: ReturnStatementAST):
        """Visit return statement."""
        if node.value:
            ret_type = self._visit_expression(node.value)
            if self._current_return_type and ret_type:
                if self._current_return_type != ret_type:
                    self._error(
                        f"Return type mismatch: expected {self._current_return_type}, got {ret_type}",
                        node.line, node.column
                    )
        elif self._current_return_type and self._current_return_type != 'void':
            self._error(
                f"Function must return {self._current_return_type}",
                node.line, node.column
            )
    
    def _visit_expression(self, node: BaseAST) -> Optional[str]:
        """
        Visit expression and return its type.
        
        Returns:
            Type name or None if unknown
        """
        if isinstance(node, LiteralAST):
            return node.literal_type
        elif isinstance(node, IdentifierExprAST):
            info = self._symbol_table.lookup(node.name)
            if not info:
                self._error(f"Undefined variable '{node.name}'", node.line, node.column)
                return None
            return info.type_name
        elif isinstance(node, BinaryExprAST):
            left_type = self._visit_expression(node.left)
            right_type = self._visit_expression(node.right)
            # Simplified type checking
            if left_type == right_type:
                return left_type
            return None
        elif isinstance(node, UnaryExprAST):
            return self._visit_expression(node.operand)
        elif isinstance(node, AssignmentExprAST):
            target_type = self._visit_expression(node.target)
            value_type = self._visit_expression(node.value)
            if target_type and value_type and target_type != value_type:
                self._error(f"Type mismatch in assignment", node.line, node.column)
            return target_type
        elif isinstance(node, CallExprAST):
            # Look up function
            if isinstance(node.callee, IdentifierExprAST):
                info = self._symbol_table.lookup(node.callee.name)
                if not info:
                    self._error(f"Undefined function '{node.callee.name}'", 
                               node.line, node.column)
                return info.return_type if info else None
            return None
        elif isinstance(node, MemberExprAST):
            # TODO: Implement member access type checking
            self._visit_expression(node.object)
            return None
        elif isinstance(node, IndexExprAST):
            self._visit_expression(node.object)
            self._visit_expression(node.index)
            return None
        elif isinstance(node, NewExprAST):
            info = self._symbol_table.lookup(node.class_name)
            if not info or info.kind != SymbolKind.CLASS:
                self._error(f"Undefined class '{node.class_name}'", node.line, node.column)
            return node.class_name
        elif isinstance(node, ThisExprAST):
            return self._symbol_table.current_class
        elif isinstance(node, SuperExprAST):
            # TODO: Get parent class type
            return None
        else:
            return None
    
    def _get_type_name(self, type_node: BaseAST) -> Optional[str]:
        """Get type name from type AST node."""
        if isinstance(type_node, BasicTypeAST):
            return type_node.name
        elif isinstance(type_node, PointerTypeAST):
            base = self._get_type_name(type_node.base_type)
            return f"{base}*" if base else None
        elif isinstance(type_node, ArrayTypeAST):
            base = self._get_type_name(type_node.element_type)
            return f"{base}[]" if base else None
        elif isinstance(type_node, SliceTypeAST):
            base = self._get_type_name(type_node.element_type)
            return f"{base}[]" if base else None
        return None


def analyze_program(program: ProgramAST) -> List[SemanticError]:
    """
    Analyze a C3++ program for semantic errors.
    
    Args:
        program: Root AST node of the program
        
    Returns:
        List of semantic errors found
    """
    analyzer = SemanticAnalyzer()
    return analyzer.analyze(program)
