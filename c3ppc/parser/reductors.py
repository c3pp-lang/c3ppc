"""
C3++ Parser Reductors
=====================
Reductor functions for building AST nodes during parsing.
"""

from typing import List, Optional
from pylgen.common.types import AST, ASTListView, Token
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


# ============================================================================
# Helper Functions
# ============================================================================

def get_token_text(asts: ASTListView, index: int) -> str:
    """Get text from a token at the given index."""
    token = asts[index]
    if isinstance(token, Token):
        return token.text
    return str(token)


def get_token_line(asts: ASTListView, index: int) -> int:
    """Get line number from a token at the given index."""
    token = asts[index]
    if isinstance(token, Token):
        return token.line
    return 0


def get_token_column(asts: ASTListView, index: int) -> int:
    """Get column number from a token at the given index."""
    token = asts[index]
    if isinstance(token, Token):
        return token.column
    return 0


def get_access_modifier(asts: ASTListView, index: int) -> Optional[str]:
    """Extract access modifier from token."""
    text = get_token_text(asts, index)
    if text in ('public', 'private', 'protected'):
        return text
    return None


# ============================================================================
# Program Structure Reductors
# ============================================================================

def program_reductor(asts: ASTListView) -> AST:
    """Reduce program: module? import* declaration*"""
    # Simplified - just return the first child for now
    return asts[0]


def module_reductor(asts: ASTListView) -> AST:
    """Reduce module declaration."""
    name = get_token_text(asts, 1)
    return ModuleDeclAST(name, get_token_line(asts, 0), get_token_column(asts, 0))


def import_reductor(asts: ASTListView) -> AST:
    """Reduce import declaration."""
    module_path = get_token_text(asts, 1)
    alias = None
    if len(asts) > 3:
        alias = get_token_text(asts, 3)
    return ImportDeclAST(module_path, alias, get_token_line(asts, 0), get_token_column(asts, 0))


# ============================================================================
# Expression Reductors
# ============================================================================

def binary_expr_reductor(asts: ASTListView) -> AST:
    """Reduce binary expression: expr op expr"""
    left = asts[0]
    operator = get_token_text(asts, 1)
    right = asts[2]
    return BinaryExprAST(left, operator, right, 
                        get_token_line(asts, 1), get_token_column(asts, 1))


def unary_prefix_reductor(asts: ASTListView) -> AST:
    """Reduce unary prefix expression: op expr"""
    operator = get_token_text(asts, 0)
    operand = asts[1]
    return UnaryExprAST(operator, operand, True,
                       get_token_line(asts, 0), get_token_column(asts, 0))


def unary_postfix_reductor(asts: ASTListView) -> AST:
    """Reduce unary postfix expression: expr op"""
    operand = asts[0]
    operator = get_token_text(asts, 1)
    return UnaryExprAST(operator, operand, False,
                       get_token_line(asts, 1), get_token_column(asts, 1))


def assignment_reductor(asts: ASTListView) -> AST:
    """Reduce assignment expression: target = value"""
    target = asts[0]
    operator = get_token_text(asts, 1)
    value = asts[2]
    return AssignmentExprAST(target, operator, value,
                            get_token_line(asts, 1), get_token_column(asts, 1))


def call_reductor(asts: ASTListView) -> AST:
    """Reduce function call: callee(args)"""
    callee = asts[0]
    # Extract arguments from the argument list
    args = []
    if len(asts) > 2:
        arg_list = asts[2]
        if isinstance(arg_list, list):
            args = arg_list
        else:
            args = [arg_list]
    return CallExprAST(callee, args,
                      get_token_line(asts, 0), get_token_column(asts, 0))


def member_access_reductor(asts: ASTListView) -> AST:
    """Reduce member access: obj.member"""
    obj = asts[0]
    member = get_token_text(asts, 2)
    return MemberExprAST(obj, member,
                        get_token_line(asts, 2), get_token_column(asts, 2))


def index_reductor(asts: ASTListView) -> AST:
    """Reduce index expression: arr[index]"""
    arr = asts[0]
    index = asts[2]
    return IndexExprAST(arr, index,
                       get_token_line(asts, 2), get_token_column(asts, 2))


def new_reductor(asts: ASTListView) -> AST:
    """Reduce new expression: new ClassName(args)"""
    class_name = get_token_text(asts, 1)
    args = []
    if len(asts) > 3:
        arg_list = asts[3]
        if isinstance(arg_list, list):
            args = arg_list
        else:
            args = [arg_list]
    return NewExprAST(class_name, args,
                     get_token_line(asts, 0), get_token_column(asts, 0))


def this_reductor(asts: ASTListView) -> AST:
    """Reduce this expression."""
    return ThisExprAST(get_token_line(asts, 0), get_token_column(asts, 0))


def super_reductor(asts: ASTListView) -> AST:
    """Reduce super expression."""
    return SuperExprAST(get_token_line(asts, 0), get_token_column(asts, 0))


def identifier_reductor(asts: ASTListView) -> AST:
    """Reduce identifier expression."""
    name = get_token_text(asts, 0)
    return IdentifierExprAST(name,
                            get_token_line(asts, 0), get_token_column(asts, 0))


def literal_reductor(asts: ASTListView) -> AST:
    """Reduce literal expression."""
    text = get_token_text(asts, 0)
    line = get_token_line(asts, 0)
    column = get_token_column(asts, 0)
    
    # Determine literal type
    if text.isdigit() or (text.startswith('-') and text[1:].isdigit()):
        return LiteralAST(int(text), 'integer', line, column)
    elif '.' in text:
        return LiteralAST(float(text), 'float', line, column)
    elif text.startswith('"') or text.startswith('`'):
        return LiteralAST(text[1:-1], 'string', line, column)
    elif text.startswith("'"):
        return LiteralAST(text[1], 'char', line, column)
    elif text in ('true', 'false'):
        return LiteralAST(text == 'true', 'bool', line, column)
    else:
        return IdentifierExprAST(text, line, column)


def parenthesized_reductor(asts: ASTListView) -> AST:
    """Reduce parenthesized expression: (expr)"""
    return asts[1]


# ============================================================================
# Statement Reductors
# ============================================================================

def block_reductor(asts: ASTListView) -> AST:
    """Reduce block: { statements }"""
    statements = []
    if len(asts) > 2:
        stmt_list = asts[1]
        if isinstance(stmt_list, list):
            statements = stmt_list
        else:
            statements = [stmt_list]
    return BlockAST(statements,
                   get_token_line(asts, 0), get_token_column(asts, 0))


def if_reductor(asts: ASTListView) -> AST:
    """Reduce if statement: if (condition) block else? block?"""
    condition = asts[2]
    then_block = asts[4]
    else_block = None
    if len(asts) > 6:
        else_block = asts[6]
    return IfStatementAST(condition, then_block, else_block,
                         get_token_line(asts, 0), get_token_column(asts, 0))


def while_reductor(asts: ASTListView) -> AST:
    """Reduce while statement: while (condition) block"""
    condition = asts[2]
    body = asts[4]
    return WhileStatementAST(condition, body,
                            get_token_line(asts, 0), get_token_column(asts, 0))


def for_reductor(asts: ASTListView) -> AST:
    """Reduce for statement: for (init; condition; update) block"""
    init = asts[2]
    condition = asts[4]
    update = asts[6]
    body = asts[8]
    return ForStatementAST(init, condition, update, body,
                          get_token_line(asts, 0), get_token_column(asts, 0))


def foreach_reductor(asts: ASTListView) -> AST:
    """Reduce foreach statement: foreach (var in iterable) block"""
    variable = get_token_text(asts, 2)
    iterable = asts[4]
    body = asts[6]
    return ForeachStatementAST(variable, iterable, body,
                              get_token_line(asts, 0), get_token_column(asts, 0))


def switch_reductor(asts: ASTListView) -> AST:
    """Reduce switch statement: switch (expr) { cases }"""
    expression = asts[2]
    cases = []
    default = None
    # Parse cases from the case list
    if len(asts) > 4:
        case_list = asts[4]
        if isinstance(case_list, list):
            for case in case_list:
                if isinstance(case, CaseClauseAST):
                    cases.append(case)
                else:
                    default = case
    return SwitchStatementAST(expression, cases, default,
                             get_token_line(asts, 0), get_token_column(asts, 0))


def case_reductor(asts: ASTListView) -> AST:
    """Reduce case clause: case expr: statements"""
    value = asts[1]
    statements = []
    if len(asts) > 3:
        stmt_list = asts[3]
        if isinstance(stmt_list, list):
            statements = stmt_list
        else:
            statements = [stmt_list]
    return CaseClauseAST(value, statements,
                        get_token_line(asts, 0), get_token_column(asts, 0))


def return_reductor(asts: ASTListView) -> AST:
    """Reduce return statement: return expr?"""
    value = None
    if len(asts) > 1:
        value = asts[1]
    return ReturnStatementAST(value,
                             get_token_line(asts, 0), get_token_column(asts, 0))


def break_reductor(asts: ASTListView) -> AST:
    """Reduce break statement."""
    return BreakStatementAST(get_token_line(asts, 0), get_token_column(asts, 0))


def continue_reductor(asts: ASTListView) -> AST:
    """Reduce continue statement."""
    return ContinueStatementAST(get_token_line(asts, 0), get_token_column(asts, 0))


def defer_reductor(asts: ASTListView) -> AST:
    """Reduce defer statement: defer statement"""
    statement = asts[1]
    return DeferStatementAST(statement,
                            get_token_line(asts, 0), get_token_column(asts, 0))


def expression_statement_reductor(asts: ASTListView) -> AST:
    """Reduce expression statement: expr ;"""
    expression = asts[0]
    return ExpressionStatementAST(expression,
                                 get_token_line(asts, 0), get_token_column(asts, 0))


# ============================================================================
# Declaration Reductors
# ============================================================================

def var_decl_reductor(asts: ASTListView) -> AST:
    """Reduce variable declaration: name: type = expr?"""
    name = get_token_text(asts, 0)
    type_annotation = None
    initializer = None
    
    # Parse based on pattern
    if len(asts) >= 3:
        # Check if we have type annotation
        if get_token_text(asts, 1) == ':':
            type_annotation = asts[2]
            if len(asts) >= 5 and get_token_text(asts, 3) == '=':
                initializer = asts[4]
        elif get_token_text(asts, 1) == '=':
            initializer = asts[2]
    
    is_const = False
    return VarDeclAST(name, type_annotation, initializer, is_const,
                     get_token_line(asts, 0), get_token_column(asts, 0))


def const_decl_reductor(asts: ASTListView) -> AST:
    """Reduce const declaration: const name = expr"""
    name = get_token_text(asts, 1)
    initializer = asts[3]
    return VarDeclAST(name, None, initializer, True,
                     get_token_line(asts, 0), get_token_column(asts, 0))


def fn_decl_reductor(asts: ASTListView) -> AST:
    """Reduce function declaration: fn name(params) -> ret_type block?"""
    name = get_token_text(asts, 1)
    params = []
    return_type = None
    body = None
    is_virtual = False
    is_override = False
    is_abstract = False
    access_modifier = None
    is_static = False
    
    # Parse based on pattern
    idx = 2
    if get_token_text(asts, idx) == '(':
        # Parse params
        if len(asts) > 3 and asts[3] is not None:
            param_list = asts[3]
            if isinstance(param_list, list):
                params = param_list
        idx = 4  # Skip )
    
    # Check for return type
    if idx < len(asts) and get_token_text(asts, idx) == '->':
        return_type = asts[idx + 1]
        idx += 2
    
    # Check for body
    if idx < len(asts) and get_token_text(asts, idx) == '{':
        body = asts[idx]
    
    return FnDeclAST(name, params, return_type, body,
                    is_virtual, is_override, is_abstract,
                    access_modifier, is_static,
                    get_token_line(asts, 0), get_token_column(asts, 0))


def fn_param_reductor(asts: ASTListView) -> AST:
    """Reduce function parameter: name: type"""
    name = get_token_text(asts, 0)
    type_annotation = asts[2]
    default_value = None
    if len(asts) > 3 and get_token_text(asts, 3) == '=':
        default_value = asts[4]
    return FnParamAST(name, type_annotation, default_value,
                     get_token_line(asts, 0), get_token_column(asts, 0))


# ============================================================================
# Type Reductors
# ============================================================================

def basic_type_reductor(asts: ASTListView) -> AST:
    """Reduce basic type."""
    name = get_token_text(asts, 0)
    return BasicTypeAST(name,
                       get_token_line(asts, 0), get_token_column(asts, 0))


def pointer_type_reductor(asts: ASTListView) -> AST:
    """Reduce pointer type: base_type *"""
    base_type = asts[0]
    return PointerTypeAST(base_type,
                         get_token_line(asts, 0), get_token_column(asts, 0))


def array_type_reductor(asts: ASTListView) -> AST:
    """Reduce array type: type[size]"""
    element_type = asts[0]
    size = asts[2]
    return ArrayTypeAST(element_type, size,
                       get_token_line(asts, 0), get_token_column(asts, 0))


def slice_type_reductor(asts: ASTListView) -> AST:
    """Reduce slice type: type[]"""
    element_type = asts[0]
    return SliceTypeAST(element_type,
                       get_token_line(asts, 0), get_token_column(asts, 0))


def function_type_reductor(asts: ASTListView) -> AST:
    """Reduce function type: fn return_type(params)"""
    return_type = asts[1]
    params = []
    if len(asts) > 3:
        param_list = asts[3]
        if isinstance(param_list, list):
            params = param_list
    return FunctionTypeAST(params, return_type,
                          get_token_line(asts, 0), get_token_column(asts, 0))


# ============================================================================
# Class Declaration Reductors
# ============================================================================

def class_decl_reductor(asts: ASTListView) -> AST:
    """Reduce class declaration: class Name extends? Base implements? Ifaces body"""
    name = get_token_text(asts, 1)
    base_class = None
    implements = []
    body = None
    access_modifier = None
    
    idx = 2
    if idx < len(asts) and get_token_text(asts, idx) == 'extends':
        base_class = get_token_text(asts, idx + 1)
        idx += 2
    
    if idx < len(asts) and get_token_text(asts, idx) == 'implements':
        # Parse interface list
        idx += 1
        while idx < len(asts) and get_token_text(asts, idx) != '{':
            if get_token_text(asts, idx) != ',':
                implements.append(get_token_text(asts, idx))
            idx += 1
    
    if idx < len(asts) and get_token_text(asts, idx) == '{':
        body = asts[idx]
    
    return ClassDeclAST(name, base_class, implements, body,
                       access_modifier,
                       get_token_line(asts, 0), get_token_column(asts, 0))


def class_body_reductor(asts: ASTListView) -> AST:
    """Reduce class body: { members }"""
    members = []
    if len(asts) > 2:
        member_list = asts[1]
        if isinstance(member_list, list):
            members = member_list
        else:
            members = [member_list]
    return ClassBodyAST(members,
                       get_token_line(asts, 0), get_token_column(asts, 0))


def constructor_reductor(asts: ASTListView) -> AST:
    """Reduce constructor: ClassName(params) block"""
    params = []
    body = None
    
    idx = 1
    if idx < len(asts) and get_token_text(asts, idx) == '(':
        if len(asts) > 2 and asts[2] is not None:
            param_list = asts[2]
            if isinstance(param_list, list):
                params = param_list
        idx = 3  # Skip )
    
    if idx < len(asts) and get_token_text(asts, idx) == '{':
        body = asts[idx]
    
    return ConstructorDeclAST(params, body,
                            get_token_line(asts, 0), get_token_column(asts, 0))


def destructor_reductor(asts: ASTListView) -> AST:
    """Reduce destructor: ~ClassName() block"""
    body = None
    if len(asts) > 2 and get_token_text(asts, 2) == '{':
        body = asts[2]
    return DestructorDeclAST(body,
                           get_token_line(asts, 0), get_token_column(asts, 0))


# ============================================================================
# Struct Declaration Reductors
# ============================================================================

def struct_decl_reductor(asts: ASTListView) -> AST:
    """Reduce struct declaration: struct Name body"""
    name = get_token_text(asts, 1)
    body = asts[2] if len(asts) > 2 else None
    access_modifier = None
    return StructDeclAST(name, body, access_modifier,
                        get_token_line(asts, 0), get_token_column(asts, 0))


def struct_body_reductor(asts: ASTListView) -> AST:
    """Reduce struct body: { members }"""
    members = []
    if len(asts) > 2:
        member_list = asts[1]
        if isinstance(member_list, list):
            members = member_list
        else:
            members = [member_list]
    return StructBodyAST(members,
                        get_token_line(asts, 0), get_token_column(asts, 0))


# ============================================================================
# Enum Declaration Reductors
# ============================================================================

def enum_decl_reductor(asts: ASTListView) -> AST:
    """Reduce enum declaration: enum Name { members }"""
    name = get_token_text(asts, 1)
    members = []
    if len(asts) > 3:
        member_list = asts[3]
        if isinstance(member_list, list):
            members = member_list
        else:
            members = [member_list]
    access_modifier = None
    return EnumDeclAST(name, members, access_modifier,
                      get_token_line(asts, 0), get_token_column(asts, 0))


def enum_member_reductor(asts: ASTListView) -> AST:
    """Reduce enum member: NAME = value?"""
    name = get_token_text(asts, 0)
    value = None
    if len(asts) > 2 and get_token_text(asts, 1) == '=':
        value = asts[2]
    return EnumMemberAST(name, value,
                        get_token_line(asts, 0), get_token_column(asts, 0))


# ============================================================================
# Interface Declaration Reductors
# ============================================================================

def interface_decl_reductor(asts: ASTListView) -> AST:
    """Reduce interface declaration: interface Name extends? Ifaces body"""
    name = get_token_text(asts, 1)
    extends = []
    body = None
    access_modifier = None
    
    idx = 2
    if idx < len(asts) and get_token_text(asts, idx) == 'extends':
        # Parse interface list
        idx += 1
        while idx < len(asts) and get_token_text(asts, idx) != '{':
            if get_token_text(asts, idx) != ',':
                extends.append(get_token_text(asts, idx))
            idx += 1
    
    if idx < len(asts) and get_token_text(asts, idx) == '{':
        body = asts[idx]
    
    return InterfaceDeclAST(name, extends, body, access_modifier,
                           get_token_line(asts, 0), get_token_column(asts, 0))


def interface_body_reductor(asts: ASTListView) -> AST:
    """Reduce interface body: { members }"""
    members = []
    if len(asts) > 2:
        member_list = asts[1]
        if isinstance(member_list, list):
            members = member_list
        else:
            members = [member_list]
    return InterfaceBodyAST(members,
                           get_token_line(asts, 0), get_token_column(asts, 0))


# ============================================================================
# List Reductors
# ============================================================================

def statement_list_reductor(asts: ASTListView) -> AST:
    """Reduce statement list: statements statement"""
    if isinstance(asts[0], list):
        result = asts[0]
    else:
        result = [asts[0]]
    result.append(asts[1])
    return result


def single_statement_reductor(asts: ASTListView) -> AST:
    """Reduce single statement."""
    return asts[0]


def expression_list_reductor(asts: ASTListView) -> AST:
    """Reduce expression list: expr, expr"""
    if isinstance(asts[0], list):
        result = asts[0]
    else:
        result = [asts[0]]
    result.append(asts[2])
    return result


def single_expression_reductor(asts: ASTListView) -> AST:
    """Reduce single expression."""
    return asts[0]


def param_list_reductor(asts: ASTListView) -> AST:
    """Reduce parameter list: param, param"""
    if isinstance(asts[0], list):
        result = asts[0]
    else:
        result = [asts[0]]
    result.append(asts[2])
    return result


def single_param_reductor(asts: ASTListView) -> AST:
    """Reduce single parameter."""
    return asts[0]


def type_list_reductor(asts: ASTListView) -> AST:
    """Reduce type list: type, type"""
    if isinstance(asts[0], list):
        result = asts[0]
    else:
        result = [asts[0]]
    result.append(asts[2])
    return result


def single_type_reductor(asts: ASTListView) -> AST:
    """Reduce single type."""
    return asts[0]


def member_list_reductor(asts: ASTListView) -> AST:
    """Reduce member list: members member"""
    if isinstance(asts[0], list):
        result = asts[0]
    else:
        result = [asts[0]]
    result.append(asts[1])
    return result


def single_member_reductor(asts: ASTListView) -> AST:
    """Reduce single member."""
    return asts[0]


def case_list_reductor(asts: ASTListView) -> AST:
    """Reduce case list: cases case"""
    if isinstance(asts[0], list):
        result = asts[0]
    else:
        result = [asts[0]]
    result.append(asts[1])
    return result


def single_case_reductor(asts: ASTListView) -> AST:
    """Reduce single case."""
    return asts[0]


def enum_member_list_reductor(asts: ASTListView) -> AST:
    """Reduce enum member list: members , member"""
    if isinstance(asts[0], list):
        result = asts[0]
    else:
        result = [asts[0]]
    result.append(asts[2])
    return result


def single_enum_member_reductor(asts: ASTListView) -> AST:
    """Reduce single enum member."""
    return asts[0]
