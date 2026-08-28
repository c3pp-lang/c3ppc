"""
C3++ AST Nodes
==============
Abstract Syntax Tree node definitions for the C3++ programming language.
"""

from typing import List, Optional, Any
from pylgen.common.types import AST, Symbol


class BaseAST(AST):
    """Base class for all C3++ AST nodes."""
    
    def __init__(self, symbol: Symbol, line: int, column: int):
        super().__init__(symbol, line, column)
    
    def children(self) -> List[AST]:
        return []


# ============================================================================
# Program Structure
# ============================================================================

class ProgramAST(BaseAST):
    """Root node for a C3++ program."""
    
    def __init__(self, module: Optional['ModuleDeclAST'], 
                 imports: List['ImportDeclAST'],
                 declarations: List[BaseAST],
                 line: int, column: int):
        super().__init__(Symbol('Program'), line, column)
        self._module = module
        self._imports = imports
        self._declarations = declarations
    
    @property
    def module(self) -> Optional['ModuleDeclAST']:
        return self._module
    
    @property
    def imports(self) -> List['ImportDeclAST']:
        return self._imports
    
    @property
    def declarations(self) -> List[BaseAST]:
        return self._declarations
    
    def children(self) -> List[AST]:
        result = []
        if self._module:
            result.append(self._module)
        result.extend(self._imports)
        result.extend(self._declarations)
        return result


class ModuleDeclAST(BaseAST):
    """Module declaration."""
    
    def __init__(self, name: str, line: int, column: int):
        super().__init__(Symbol('ModuleDecl'), line, column)
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    def children(self) -> List[AST]:
        return []


class ImportDeclAST(BaseAST):
    """Import declaration."""
    
    def __init__(self, module_path: str, alias: Optional[str], line: int, column: int):
        super().__init__(Symbol('ImportDecl'), line, column)
        self._module_path = module_path
        self._alias = alias
    
    @property
    def module_path(self) -> str:
        return self._module_path
    
    @property
    def alias(self) -> Optional[str]:
        return self._alias
    
    def children(self) -> List[AST]:
        return []


# ============================================================================
# Expressions
# ============================================================================

class BinaryExprAST(BaseAST):
    """Binary expression (e.g., a + b)."""
    
    def __init__(self, left: BaseAST, operator: str, right: BaseAST, line: int, column: int):
        super().__init__(Symbol('BinaryExpr'), line, column)
        self._left = left
        self._operator = operator
        self._right = right
    
    @property
    def left(self) -> BaseAST:
        return self._left
    
    @property
    def operator(self) -> str:
        return self._operator
    
    @property
    def right(self) -> BaseAST:
        return self._right
    
    def children(self) -> List[AST]:
        return [self._left, self._right]


class UnaryExprAST(BaseAST):
    """Unary expression (e.g., -x, !flag)."""
    
    def __init__(self, operator: str, operand: BaseAST, prefix: bool, line: int, column: int):
        super().__init__(Symbol('UnaryExpr'), line, column)
        self._operator = operator
        self._operand = operand
        self._prefix = prefix
    
    @property
    def operator(self) -> str:
        return self._operator
    
    @property
    def operand(self) -> BaseAST:
        return self._operand
    
    @property
    def is_prefix(self) -> bool:
        return self._prefix
    
    def children(self) -> List[AST]:
        return [self._operand]


class AssignmentExprAST(BaseAST):
    """Assignment expression."""
    
    def __init__(self, target: BaseAST, operator: str, value: BaseAST, line: int, column: int):
        super().__init__(Symbol('AssignmentExpr'), line, column)
        self._target = target
        self._operator = operator
        self._value = value
    
    @property
    def target(self) -> BaseAST:
        return self._target
    
    @property
    def operator(self) -> str:
        return self._operator
    
    @property
    def value(self) -> BaseAST:
        return self._value
    
    def children(self) -> List[AST]:
        return [self._target, self._value]


class CallExprAST(BaseAST):
    """Function/method call expression."""
    
    def __init__(self, callee: BaseAST, arguments: List[BaseAST], line: int, column: int):
        super().__init__(Symbol('CallExpr'), line, column)
        self._callee = callee
        self._arguments = arguments
    
    @property
    def callee(self) -> BaseAST:
        return self._callee
    
    @property
    def arguments(self) -> List[BaseAST]:
        return self._arguments
    
    def children(self) -> List[AST]:
        return [self._callee] + self._arguments


class MemberExprAST(BaseAST):
    """Member access expression (e.g., obj.field)."""
    
    def __init__(self, object: BaseAST, member: str, line: int, column: int):
        super().__init__(Symbol('MemberExpr'), line, column)
        self._object = object
        self._member = member
    
    @property
    def object(self) -> BaseAST:
        return self._object
    
    @property
    def member(self) -> str:
        return self._member
    
    def children(self) -> List[AST]:
        return [self._object]


class IndexExprAST(BaseAST):
    """Index expression (e.g., arr[i])."""
    
    def __init__(self, object: BaseAST, index: BaseAST, line: int, column: int):
        super().__init__(Symbol('IndexExpr'), line, column)
        self._object = object
        self._index = index
    
    @property
    def object(self) -> BaseAST:
        return self._object
    
    @property
    def index(self) -> BaseAST:
        return self._index
    
    def children(self) -> List[AST]:
        return [self._object, self._index]


class NewExprAST(BaseAST):
    """Object creation expression (e.g., new ClassName())."""
    
    def __init__(self, class_name: str, arguments: List[BaseAST], line: int, column: int):
        super().__init__(Symbol('NewExpr'), line, column)
        self._class_name = class_name
        self._arguments = arguments
    
    @property
    def class_name(self) -> str:
        return self._class_name
    
    @property
    def arguments(self) -> List[BaseAST]:
        return self._arguments
    
    def children(self) -> List[AST]:
        return self._arguments


class ThisExprAST(BaseAST):
    """This expression."""
    
    def __init__(self, line: int, column: int):
        super().__init__(Symbol('ThisExpr'), line, column)
    
    def children(self) -> List[AST]:
        return []


class SuperExprAST(BaseAST):
    """Super expression."""
    
    def __init__(self, line: int, column: int):
        super().__init__(Symbol('SuperExpr'), line, column)
    
    def children(self) -> List[AST]:
        return []


class IdentifierExprAST(BaseAST):
    """Identifier expression."""
    
    def __init__(self, name: str, line: int, column: int):
        super().__init__(Symbol('IdentifierExpr'), line, column)
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    def children(self) -> List[AST]:
        return []


class LiteralAST(BaseAST):
    """Literal value (integer, float, string, char, bool)."""
    
    def __init__(self, value: Any, literal_type: str, line: int, column: int):
        super().__init__(Symbol('Literal'), line, column)
        self._value = value
        self._literal_type = literal_type
    
    @property
    def value(self) -> Any:
        return self._value
    
    @property
    def literal_type(self) -> str:
        return self._literal_type
    
    def children(self) -> List[AST]:
        return []


# ============================================================================
# Statements
# ============================================================================

class BlockAST(BaseAST):
    """Block of statements."""
    
    def __init__(self, statements: List[BaseAST], line: int, column: int):
        super().__init__(Symbol('Block'), line, column)
        self._statements = statements
    
    @property
    def statements(self) -> List[BaseAST]:
        return self._statements
    
    def children(self) -> List[AST]:
        return self._statements


class IfStatementAST(BaseAST):
    """If statement."""
    
    def __init__(self, condition: BaseAST, then_block: BaseAST, 
                 else_block: Optional[BaseAST], line: int, column: int):
        super().__init__(Symbol('IfStatement'), line, column)
        self._condition = condition
        self._then_block = then_block
        self._else_block = else_block
    
    @property
    def condition(self) -> BaseAST:
        return self._condition
    
    @property
    def then_block(self) -> BaseAST:
        return self._then_block
    
    @property
    def else_block(self) -> Optional[BaseAST]:
        return self._else_block
    
    def children(self) -> List[AST]:
        result = [self._condition, self._then_block]
        if self._else_block:
            result.append(self._else_block)
        return result


class WhileStatementAST(BaseAST):
    """While loop statement."""
    
    def __init__(self, condition: BaseAST, body: BaseAST, line: int, column: int):
        super().__init__(Symbol('WhileStatement'), line, column)
        self._condition = condition
        self._body = body
    
    @property
    def condition(self) -> BaseAST:
        return self._condition
    
    @property
    def body(self) -> BaseAST:
        return self._body
    
    def children(self) -> List[AST]:
        return [self._condition, self._body]


class ForStatementAST(BaseAST):
    """For loop statement."""
    
    def __init__(self, init: Optional[BaseAST], condition: Optional[BaseAST],
                 update: Optional[BaseAST], body: BaseAST, line: int, column: int):
        super().__init__(Symbol('ForStatement'), line, column)
        self._init = init
        self._condition = condition
        self._update = update
        self._body = body
    
    @property
    def init(self) -> Optional[BaseAST]:
        return self._init
    
    @property
    def condition(self) -> Optional[BaseAST]:
        return self._condition
    
    @property
    def update(self) -> Optional[BaseAST]:
        return self._update
    
    @property
    def body(self) -> BaseAST:
        return self._body
    
    def children(self) -> List[AST]:
        result = []
        if self._init:
            result.append(self._init)
        if self._condition:
            result.append(self._condition)
        if self._update:
            result.append(self._update)
        result.append(self._body)
        return result


class ForeachStatementAST(BaseAST):
    """Foreach loop statement."""
    
    def __init__(self, variable: str, iterable: BaseAST, body: BaseAST, 
                 line: int, column: int):
        super().__init__(Symbol('ForeachStatement'), line, column)
        self._variable = variable
        self._iterable = iterable
        self._body = body
    
    @property
    def variable(self) -> str:
        return self._variable
    
    @property
    def iterable(self) -> BaseAST:
        return self._iterable
    
    @property
    def body(self) -> BaseAST:
        return self._body
    
    def children(self) -> List[AST]:
        return [self._iterable, self._body]


class SwitchStatementAST(BaseAST):
    """Switch statement."""
    
    def __init__(self, expression: BaseAST, cases: List['CaseClauseAST'],
                 default: Optional[BaseAST], line: int, column: int):
        super().__init__(Symbol('SwitchStatement'), line, column)
        self._expression = expression
        self._cases = cases
        self._default = default
    
    @property
    def expression(self) -> BaseAST:
        return self._expression
    
    @property
    def cases(self) -> List['CaseClauseAST']:
        return self._cases
    
    @property
    def default(self) -> Optional[BaseAST]:
        return self._default
    
    def children(self) -> List[AST]:
        result = [self._expression]
        result.extend(self._cases)
        if self._default:
            result.append(self._default)
        return result


class CaseClauseAST(BaseAST):
    """Case clause in switch statement."""
    
    def __init__(self, value: BaseAST, statements: List[BaseAST], line: int, column: int):
        super().__init__(Symbol('CaseClause'), line, column)
        self._value = value
        self._statements = statements
    
    @property
    def value(self) -> BaseAST:
        return self._value
    
    @property
    def statements(self) -> List[BaseAST]:
        return self._statements
    
    def children(self) -> List[AST]:
        return [self._value] + self._statements


class ReturnStatementAST(BaseAST):
    """Return statement."""
    
    def __init__(self, value: Optional[BaseAST], line: int, column: int):
        super().__init__(Symbol('ReturnStatement'), line, column)
        self._value = value
    
    @property
    def value(self) -> Optional[BaseAST]:
        return self._value
    
    def children(self) -> List[AST]:
        return [self._value] if self._value else []


class BreakStatementAST(BaseAST):
    """Break statement."""
    
    def __init__(self, line: int, column: int):
        super().__init__(Symbol('BreakStatement'), line, column)
    
    def children(self) -> List[AST]:
        return []


class ContinueStatementAST(BaseAST):
    """Continue statement."""
    
    def __init__(self, line: int, column: int):
        super().__init__(Symbol('ContinueStatement'), line, column)
    
    def children(self) -> List[AST]:
        return []


class DeferStatementAST(BaseAST):
    """Defer statement."""
    
    def __init__(self, statement: BaseAST, line: int, column: int):
        super().__init__(Symbol('DeferStatement'), line, column)
        self._statement = statement
    
    @property
    def statement(self) -> BaseAST:
        return self._statement
    
    def children(self) -> List[AST]:
        return [self._statement]


class ExpressionStatementAST(BaseAST):
    """Expression statement."""
    
    def __init__(self, expression: BaseAST, line: int, column: int):
        super().__init__(Symbol('ExpressionStatement'), line, column)
        self._expression = expression
    
    @property
    def expression(self) -> BaseAST:
        return self._expression
    
    def children(self) -> List[AST]:
        return [self._expression]


# ============================================================================
# Declarations
# ============================================================================

class VarDeclAST(BaseAST):
    """Variable declaration."""
    
    def __init__(self, name: str, type_annotation: Optional['TypeAST'], 
                 initializer: Optional[BaseAST], is_const: bool, line: int, column: int):
        super().__init__(Symbol('VarDecl'), line, column)
        self._name = name
        self._type_annotation = type_annotation
        self._initializer = initializer
        self._is_const = is_const
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def type_annotation(self) -> Optional['TypeAST']:
        return self._type_annotation
    
    @property
    def initializer(self) -> Optional[BaseAST]:
        return self._initializer
    
    @property
    def is_const(self) -> bool:
        return self._is_const
    
    def children(self) -> List[AST]:
        result = []
        if self._type_annotation:
            result.append(self._type_annotation)
        if self._initializer:
            result.append(self._initializer)
        return result


class FnDeclAST(BaseAST):
    """Function declaration."""
    
    def __init__(self, name: str, params: List['FnParamAST'], 
                 return_type: Optional['TypeAST'], body: Optional[BaseAST],
                 is_virtual: bool, is_override: bool, is_abstract: bool,
                 access_modifier: Optional[str], is_static: bool,
                 line: int, column: int):
        super().__init__(Symbol('FnDecl'), line, column)
        self._name = name
        self._params = params
        self._return_type = return_type
        self._body = body
        self._is_virtual = is_virtual
        self._is_override = is_override
        self._is_abstract = is_abstract
        self._access_modifier = access_modifier
        self._is_static = is_static
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def params(self) -> List['FnParamAST']:
        return self._params
    
    @property
    def return_type(self) -> Optional['TypeAST']:
        return self._return_type
    
    @property
    def body(self) -> Optional[BaseAST]:
        return self._body
    
    @property
    def is_virtual(self) -> bool:
        return self._is_virtual
    
    @property
    def is_override(self) -> bool:
        return self._is_override
    
    @property
    def is_abstract(self) -> bool:
        return self._is_abstract
    
    @property
    def access_modifier(self) -> Optional[str]:
        return self._access_modifier
    
    @property
    def is_static(self) -> bool:
        return self._is_static
    
    def children(self) -> List[AST]:
        result = list(self._params)
        if self._return_type:
            result.append(self._return_type)
        if self._body:
            result.append(self._body)
        return result


class FnParamAST(BaseAST):
    """Function parameter."""
    
    def __init__(self, name: str, type_annotation: 'TypeAST', 
                 default_value: Optional[BaseAST], line: int, column: int):
        super().__init__(Symbol('FnParam'), line, column)
        self._name = name
        self._type_annotation = type_annotation
        self._default_value = default_value
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def type_annotation(self) -> 'TypeAST':
        return self._type_annotation
    
    @property
    def default_value(self) -> Optional[BaseAST]:
        return self._default_value
    
    def children(self) -> List[AST]:
        result = [self._type_annotation]
        if self._default_value:
            result.append(self._default_value)
        return result


# ============================================================================
# Types
# ============================================================================

class TypeAST(BaseAST):
    """Base type AST node."""
    
    def __init__(self, symbol: Symbol, line: int, column: int):
        super().__init__(symbol, line, column)


class BasicTypeAST(TypeAST):
    """Basic type (int, float, bool, etc.)."""
    
    def __init__(self, name: str, line: int, column: int):
        super().__init__(Symbol('BasicType'), line, column)
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    def children(self) -> List[AST]:
        return []


class PointerTypeAST(TypeAST):
    """Pointer type (e.g., int*)."""
    
    def __init__(self, base_type: TypeAST, line: int, column: int):
        super().__init__(Symbol('PointerType'), line, column)
        self._base_type = base_type
    
    @property
    def base_type(self) -> TypeAST:
        return self._base_type
    
    def children(self) -> List[AST]:
        return [self._base_type]


class ArrayTypeAST(TypeAST):
    """Array type (e.g., int[10])."""
    
    def __init__(self, element_type: TypeAST, size: Optional[BaseAST], line: int, column: int):
        super().__init__(Symbol('ArrayType'), line, column)
        self._element_type = element_type
        self._size = size
    
    @property
    def element_type(self) -> TypeAST:
        return self._element_type
    
    @property
    def size(self) -> Optional[BaseAST]:
        return self._size
    
    def children(self) -> List[AST]:
        result = [self._element_type]
        if self._size:
            result.append(self._size)
        return result


class SliceTypeAST(TypeAST):
    """Slice type (e.g., int[])."""
    
    def __init__(self, element_type: TypeAST, line: int, column: int):
        super().__init__(Symbol('SliceType'), line, column)
        self._element_type = element_type
    
    @property
    def element_type(self) -> TypeAST:
        return self._element_type
    
    def children(self) -> List[AST]:
        return [self._element_type]


class FunctionTypeAST(TypeAST):
    """Function type (e.g., fn int(int, int))."""
    
    def __init__(self, params: List[TypeAST], return_type: TypeAST, line: int, column: int):
        super().__init__(Symbol('FunctionType'), line, column)
        self._params = params
        self._return_type = return_type
    
    @property
    def params(self) -> List[TypeAST]:
        return self._params
    
    @property
    def return_type(self) -> TypeAST:
        return self._return_type
    
    def children(self) -> List[AST]:
        return self._params + [self._return_type]


# ============================================================================
# Class Declarations
# ============================================================================

class ClassDeclAST(BaseAST):
    """Class declaration."""
    
    def __init__(self, name: str, base_class: Optional[str],
                 implements: List[str], body: 'ClassBodyAST',
                 access_modifier: Optional[str], line: int, column: int):
        super().__init__(Symbol('ClassDecl'), line, column)
        self._name = name
        self._base_class = base_class
        self._implements = implements
        self._body = body
        self._access_modifier = access_modifier
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def base_class(self) -> Optional[str]:
        return self._base_class
    
    @property
    def implements(self) -> List[str]:
        return self._implements
    
    @property
    def body(self) -> 'ClassBodyAST':
        return self._body
    
    @property
    def access_modifier(self) -> Optional[str]:
        return self._access_modifier
    
    def children(self) -> List[AST]:
        return [self._body]


class ClassBodyAST(BaseAST):
    """Class body containing members."""
    
    def __init__(self, members: List[BaseAST], line: int, column: int):
        super().__init__(Symbol('ClassBody'), line, column)
        self._members = members
    
    @property
    def members(self) -> List[BaseAST]:
        return self._members
    
    def children(self) -> List[AST]:
        return self._members


class ConstructorDeclAST(BaseAST):
    """Constructor declaration."""
    
    def __init__(self, params: List['FnParamAST'], body: BaseAST,
                 line: int, column: int):
        super().__init__(Symbol('ConstructorDecl'), line, column)
        self._params = params
        self._body = body
    
    @property
    def params(self) -> List['FnParamAST']:
        return self._params
    
    @property
    def body(self) -> BaseAST:
        return self._body
    
    def children(self) -> List[AST]:
        return list(self._params) + [self._body]


class DestructorDeclAST(BaseAST):
    """Destructor declaration."""
    
    def __init__(self, body: BaseAST, line: int, column: int):
        super().__init__(Symbol('DestructorDecl'), line, column)
        self._body = body
    
    @property
    def body(self) -> BaseAST:
        return self._body
    
    def children(self) -> List[AST]:
        return [self._body]


# ============================================================================
# Struct Declarations
# ============================================================================

class StructDeclAST(BaseAST):
    """Struct declaration."""
    
    def __init__(self, name: str, body: 'StructBodyAST',
                 access_modifier: Optional[str], line: int, column: int):
        super().__init__(Symbol('StructDecl'), line, column)
        self._name = name
        self._body = body
        self._access_modifier = access_modifier
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def body(self) -> 'StructBodyAST':
        return self._body
    
    @property
    def access_modifier(self) -> Optional[str]:
        return self._access_modifier
    
    def children(self) -> List[AST]:
        return [self._body]


class StructBodyAST(BaseAST):
    """Struct body containing members."""
    
    def __init__(self, members: List['VarDeclAST'], line: int, column: int):
        super().__init__(Symbol('StructBody'), line, column)
        self._members = members
    
    @property
    def members(self) -> List['VarDeclAST']:
        return self._members
    
    def children(self) -> List[AST]:
        return self._members


# ============================================================================
# Enum Declarations
# ============================================================================

class EnumDeclAST(BaseAST):
    """Enum declaration."""
    
    def __init__(self, name: str, members: List['EnumMemberAST'],
                 access_modifier: Optional[str], line: int, column: int):
        super().__init__(Symbol('EnumDecl'), line, column)
        self._name = name
        self._members = members
        self._access_modifier = access_modifier
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def members(self) -> List['EnumMemberAST']:
        return self._members
    
    @property
    def access_modifier(self) -> Optional[str]:
        return self._access_modifier
    
    def children(self) -> List[AST]:
        return self._members


class EnumMemberAST(BaseAST):
    """Enum member."""
    
    def __init__(self, name: str, value: Optional[BaseAST], line: int, column: int):
        super().__init__(Symbol('EnumMember'), line, column)
        self._name = name
        self._value = value
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def value(self) -> Optional[BaseAST]:
        return self._value
    
    def children(self) -> List[AST]:
        return [self._value] if self._value else []


# ============================================================================
# Interface Declarations
# ============================================================================

class InterfaceDeclAST(BaseAST):
    """Interface declaration."""
    
    def __init__(self, name: str, extends: List[str], 
                 body: 'InterfaceBodyAST', access_modifier: Optional[str],
                 line: int, column: int):
        super().__init__(Symbol('InterfaceDecl'), line, column)
        self._name = name
        self._extends = extends
        self._body = body
        self._access_modifier = access_modifier
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def extends(self) -> List[str]:
        return self._extends
    
    @property
    def body(self) -> 'InterfaceBodyAST':
        return self._body
    
    @property
    def access_modifier(self) -> Optional[str]:
        return self._access_modifier
    
    def children(self) -> List[AST]:
        return [self._body]


class InterfaceBodyAST(BaseAST):
    """Interface body containing method signatures."""
    
    def __init__(self, members: List[BaseAST], line: int, column: int):
        super().__init__(Symbol('InterfaceBody'), line, column)
        self._members = members
    
    @property
    def members(self) -> List[BaseAST]:
        return self._members
    
    def children(self) -> List[AST]:
        return self._members
