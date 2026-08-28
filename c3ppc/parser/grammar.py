"""
C3++ Grammar Definition
=======================
Grammar rules for the C3++ programming language.
"""

from pylgen.grammar.grammar import AttributedGrammar
from pylgen.parser.parser_builder import ParserBuilder
from pylgen.parser.parser_type import ParserType
from .grammar_symbols import (
    END_SYMBOL,
    Program, ModuleDecl, ImportDecl, Declaration, DeclarationList,
    Expression, AssignmentExpr, LogicalOrExpr, LogicalAndExpr,
    BitwiseOrExpr, BitwiseXorExpr, BitwiseAndExpr,
    EqualityExpr, RelationalExpr, ShiftExpr,
    AdditiveExpr, MultiplicativeExpr, UnaryExpr, PostfixExpr, PrimaryExpr,
    Statement, Block, StatementList,
    IfStatement, WhileStatement, ForStatement, ForeachStatement,
    SwitchStatement, ReturnStatement, BreakStatement,
    ContinueStatement, DeferStatement, ExpressionStatement,
    VarDecl, VarDeclList, FnDecl, FnParams, FnParam, TypeDecl,
    Type, BasicType, PointerType, ArrayType, SliceType, FunctionType,
    ClassDecl, ClassBody, ClassMember, ClassMemberList,
    ConstructorDecl, DestructorDecl, MethodDecl,
    StructDecl, StructBody, StructMember, StructMemberList,
    EnumDecl, EnumBody, EnumMember, EnumMemberList,
    InterfaceDecl, InterfaceBody, InterfaceMember, InterfaceMemberList,
    AccessModifier, Identifier, TypeAnnotation, ExprList, ArgumentList,
    CaseClause, CaseClauseList,
    # Terminal symbols
    fn, return_kw, if_kw, else_kw, while_kw, for_kw, foreach_kw,
    switch_kw, case_kw, default_kw, break_kw, continue_kw, defer_kw,
    int_kw, long_kw, short_kw, float_kw, double_kw, char_kw,
    bool_kw, void_kw, string_kw,
    class_kw, struct_kw, enum_kw, interface_kw,
    extends_kw, implements_kw, new_kw, this_kw, super_kw,
    public_kw, private_kw, protected_kw,
    static_kw, virtual_kw, override_kw, abstract_kw, const_kw, mutable_kw,
    import_kw, module_kw, as_kw, typedef_kw, alias_kw,
    integer, float_literal, string_literal, char_literal, bool_literal, identifier,
    plus, minus, star, slash, percent, caret, ampersand, pipe, tilde, bang, question,
    equal, not_equal, less, less_equal, greater, greater_equal,
    and_op, or_op,
    assign, plus_assign, minus_assign, star_assign, slash_assign,
    percent_assign, ampersand_assign, pipe_assign, caret_assign,
    plus_plus, minus_minus,
    arrow, double_colon, colon, dot,
    lparen, rparen, lbrace, rbrace, lbracket, rbracket, semicolon, comma
)
from .reductors import (
    program_reductor, module_reductor, import_reductor,
    binary_expr_reductor, unary_prefix_reductor, unary_postfix_reductor,
    assignment_reductor, call_reductor, member_access_reductor,
    index_reductor, new_reductor, this_reductor, super_reductor,
    identifier_reductor, literal_reductor, parenthesized_reductor,
    block_reductor, if_reductor, while_reductor, for_reductor,
    foreach_reductor, switch_reductor, case_reductor,
    return_reductor, break_reductor, continue_reductor,
    defer_reductor, expression_statement_reductor,
    var_decl_reductor, const_decl_reductor, fn_decl_reductor, fn_param_reductor,
    basic_type_reductor, pointer_type_reductor, array_type_reductor,
    slice_type_reductor, function_type_reductor,
    class_decl_reductor, class_body_reductor,
    constructor_reductor, destructor_reductor,
    struct_decl_reductor, struct_body_reductor,
    enum_decl_reductor, enum_member_reductor,
    interface_decl_reductor, interface_body_reductor,
    statement_list_reductor, single_statement_reductor,
    expression_list_reductor, single_expression_reductor,
    param_list_reductor, single_param_reductor,
    type_list_reductor, single_type_reductor,
    member_list_reductor, single_member_reductor,
    case_list_reductor, single_case_reductor,
    enum_member_list_reductor, single_enum_member_reductor
)


def create_c3pp_grammar() -> AttributedGrammar:
    """
    Create the C3++ grammar.
    
    Returns:
        Configured AttributedGrammar instance
    """
    # Create grammar with Program as start symbol
    G = AttributedGrammar(Program, END_SYMBOL)
    
    # =========================================================================
    # Program Structure
    # =========================================================================
    
    # Program: module? import* declaration*
    G[Program] += (ModuleDecl, DeclarationList), program_reductor
    G[Program] += (DeclarationList,), program_reductor
    G[Program] += (ImportDecl, DeclarationList), program_reductor
    
    # Module declaration: module name ;
    G[ModuleDecl] += (module_kw, identifier, semicolon), module_reductor
    
    # Import declaration: import path [as alias] ;
    G[ImportDecl] += (import_kw, identifier, semicolon), import_reductor
    G[ImportDecl] += (import_kw, identifier, as_kw, identifier, semicolon), import_reductor
    
    # Declaration list
    G[DeclarationList] += (DeclarationList, Declaration), member_list_reductor
    G[DeclarationList] += (Declaration,), single_member_reductor
    
    # Declaration can be various types
    G[Declaration] += (VarDecl,), single_statement_reductor
    G[Declaration] += (FnDecl,), single_statement_reductor
    G[Declaration] += (ClassDecl,), single_statement_reductor
    G[Declaration] += (StructDecl,), single_statement_reductor
    G[Declaration] += (EnumDecl,), single_statement_reductor
    G[Declaration] += (InterfaceDecl,), single_statement_reductor
    
    # =========================================================================
    # Types
    # =========================================================================
    
    # Basic types
    G[BasicType] += (int_kw,), basic_type_reductor
    G[BasicType] += (long_kw,), basic_type_reductor
    G[BasicType] += (short_kw,), basic_type_reductor
    G[BasicType] += (float_kw,), basic_type_reductor
    G[BasicType] += (double_kw,), basic_type_reductor
    G[BasicType] += (char_kw,), basic_type_reductor
    G[BasicType] += (bool_kw,), basic_type_reductor
    G[BasicType] += (void_kw,), basic_type_reductor
    G[BasicType] += (string_kw,), basic_type_reductor
    G[BasicType] += (identifier,), basic_type_reductor
    
    # Pointer type: type *
    G[PointerType] += (Type, star), pointer_type_reductor
    
    # Array type: type [ expr ]
    G[ArrayType] += (Type, lbracket, Expression, rbracket), array_type_reductor
    
    # Slice type: type []
    G[SliceType] += (Type, lbracket, rbracket), slice_type_reductor
    
    # Function type: fn type ( type_list )
    G[FunctionType] += (fn, Type, lparen, TypeList, rparen), function_type_reductor
    G[FunctionType] += (fn, Type, lparen, rparen), function_type_reductor
    
    # Type can be any of these
    G[Type] += (BasicType,), single_type_reductor
    G[Type] += (PointerType,), single_type_reductor
    G[Type] += (ArrayType,), single_type_reductor
    G[Type] += (SliceType,), single_type_reductor
    G[Type] += (FunctionType,), single_type_reductor
    
    # Type list for function parameters
    G[TypeList] += (TypeList, comma, Type), type_list_reductor
    G[TypeList] += (Type,), single_type_reductor
    
    # =========================================================================
    # Expressions
    # =========================================================================
    
    # Primary expressions
    G[PrimaryExpr] += (identifier,), identifier_reductor
    G[PrimaryExpr] += (integer,), literal_reductor
    G[PrimaryExpr] += (float_literal,), literal_reductor
    G[PrimaryExpr] += (string_literal,), literal_reductor
    G[PrimaryExpr] += (char_literal,), literal_reductor
    G[PrimaryExpr] += (bool_literal,), literal_reductor
    G[PrimaryExpr] += (this_kw,), this_reductor
    G[PrimaryExpr] += (super_kw,), super_reductor
    G[PrimaryExpr] += (lparen, Expression, rparen), parenthesized_reductor
    G[PrimaryExpr] += (new_kw, identifier, lparen, ArgumentList, rparen), new_reductor
    G[PrimaryExpr] += (new_kw, identifier, lparen, rparen), new_reductor
    
    # Postfix expressions
    G[PostfixExpr] += (PostfixExpr, lparen, ArgumentList, rparen), call_reductor
    G[PostfixExpr] += (PostfixExpr, lparen, rparen), call_reductor
    G[PostfixExpr] += (PostfixExpr, dot, identifier), member_access_reductor
    G[PostfixExpr] += (PostfixExpr, lbracket, Expression, rbracket), index_reductor
    G[PostfixExpr] += (PostfixExpr, plus_plus), unary_postfix_reductor
    G[PostfixExpr] += (PostfixExpr, minus_minus), unary_postfix_reductor
    G[PostfixExpr] += (PrimaryExpr,), single_expression_reductor
    
    # Unary expressions
    G[UnaryExpr] += (bang, UnaryExpr), unary_prefix_reductor
    G[UnaryExpr] += (tilde, UnaryExpr), unary_prefix_reductor
    G[UnaryExpr] += (minus, UnaryExpr), unary_prefix_reductor
    G[UnaryExpr] += (plus_plus, UnaryExpr), unary_prefix_reductor
    G[UnaryExpr] += (minus_minus, UnaryExpr), unary_prefix_reductor
    G[UnaryExpr] += (star, UnaryExpr), unary_prefix_reductor  # Dereference
    G[UnaryExpr] += (ampersand, UnaryExpr), unary_prefix_reductor  # Address-of
    G[UnaryExpr] += (PostfixExpr,), single_expression_reductor
    
    # Multiplicative expressions
    G[MultiplicativeExpr] += (MultiplicativeExpr, star, UnaryExpr), binary_expr_reductor
    G[MultiplicativeExpr] += (MultiplicativeExpr, slash, UnaryExpr), binary_expr_reductor
    G[MultiplicativeExpr] += (MultiplicativeExpr, percent, UnaryExpr), binary_expr_reductor
    G[MultiplicativeExpr] += (UnaryExpr,), single_expression_reductor
    
    # Additive expressions
    G[AdditiveExpr] += (AdditiveExpr, plus, MultiplicativeExpr), binary_expr_reductor
    G[AdditiveExpr] += (AdditiveExpr, minus, MultiplicativeExpr), binary_expr_reductor
    G[AdditiveExpr] += (MultiplicativeExpr,), single_expression_reductor
    
    # Shift expressions
    G[ShiftExpr] += (ShiftExpr, less, less, AdditiveExpr), binary_expr_reductor
    G[ShiftExpr] += (ShiftExpr, greater, greater, AdditiveExpr), binary_expr_reductor
    G[ShiftExpr] += (AdditiveExpr,), single_expression_reductor
    
    # Relational expressions
    G[RelationalExpr] += (RelationalExpr, less, ShiftExpr), binary_expr_reductor
    G[RelationalExpr] += (RelationalExpr, less_equal, ShiftExpr), binary_expr_reductor
    G[RelationalExpr] += (RelationalExpr, greater, ShiftExpr), binary_expr_reductor
    G[RelationalExpr] += (RelationalExpr, greater_equal, ShiftExpr), binary_expr_reductor
    G[RelationalExpr] += (ShiftExpr,), single_expression_reductor
    
    # Equality expressions
    G[EqualityExpr] += (EqualityExpr, equal, RelationalExpr), binary_expr_reductor
    G[EqualityExpr] += (EqualityExpr, not_equal, RelationalExpr), binary_expr_reductor
    G[EqualityExpr] += (RelationalExpr,), single_expression_reductor
    
    # Bitwise AND expressions
    G[BitwiseAndExpr] += (BitwiseAndExpr, ampersand, EqualityExpr), binary_expr_reductor
    G[BitwiseAndExpr] += (EqualityExpr,), single_expression_reductor
    
    # Bitwise XOR expressions
    G[BitwiseXorExpr] += (BitwiseXorExpr, caret, BitwiseAndExpr), binary_expr_reductor
    G[BitwiseXorExpr] += (BitwiseAndExpr,), single_expression_reductor
    
    # Bitwise OR expressions
    G[BitwiseOrExpr] += (BitwiseOrExpr, pipe, BitwiseXorExpr), binary_expr_reductor
    G[BitwiseOrExpr] += (BitwiseXorExpr,), single_expression_reductor
    
    # Logical AND expressions
    G[LogicalAndExpr] += (LogicalAndExpr, and_op, BitwiseOrExpr), binary_expr_reductor
    G[LogicalAndExpr] += (BitwiseOrExpr,), single_expression_reductor
    
    # Logical OR expressions
    G[LogicalOrExpr] += (LogicalOrExpr, or_op, LogicalAndExpr), binary_expr_reductor
    G[LogicalOrExpr] += (LogicalAndExpr,), single_expression_reductor
    
    # Assignment expressions
    G[AssignmentExpr] += (PostfixExpr, assign, AssignmentExpr), assignment_reductor
    G[AssignmentExpr] += (PostfixExpr, plus_assign, AssignmentExpr), assignment_reductor
    G[AssignmentExpr] += (PostfixExpr, minus_assign, AssignmentExpr), assignment_reductor
    G[AssignmentExpr] += (PostfixExpr, star_assign, AssignmentExpr), assignment_reductor
    G[AssignmentExpr] += (PostfixExpr, slash_assign, AssignmentExpr), assignment_reductor
    G[AssignmentExpr] += (PostfixExpr, percent_assign, AssignmentExpr), assignment_reductor
    G[AssignmentExpr] += (PostfixExpr, ampersand_assign, AssignmentExpr), assignment_reductor
    G[AssignmentExpr] += (PostfixExpr, pipe_assign, AssignmentExpr), assignment_reductor
    G[AssignmentExpr] += (PostfixExpr, caret_assign, AssignmentExpr), assignment_reductor
    G[AssignmentExpr] += (LogicalOrExpr,), single_expression_reductor
    
    # Top-level expression
    G[Expression] += (AssignmentExpr,), single_expression_reductor
    
    # Expression list
    G[ExprList] += (ExprList, comma, Expression), expression_list_reductor
    G[ExprList] += (Expression,), single_expression_reductor
    
    # Argument list (can be empty)
    G[ArgumentList] += (ExprList,), single_expression_reductor
    
    # =========================================================================
    # Statements
    # =========================================================================
    
    # Block: { statement* }
    G[Block] += (lbrace, StatementList, rbrace), block_reductor
    G[Block] += (lbrace, rbrace), block_reductor
    
    # Statement list
    G[StatementList] += (StatementList, Statement), statement_list_reductor
    G[StatementList] += (Statement,), single_statement_reductor
    
    # Statement types
    G[Statement] += (VarDecl,), single_statement_reductor
    G[Statement] += (IfStatement,), single_statement_reductor
    G[Statement] += (WhileStatement,), single_statement_reductor
    G[Statement] += (ForStatement,), single_statement_reductor
    G[Statement] += (ForeachStatement,), single_statement_reductor
    G[Statement] += (SwitchStatement,), single_statement_reductor
    G[Statement] += (ReturnStatement,), single_statement_reductor
    G[Statement] += (BreakStatement,), single_statement_reductor
    G[Statement] += (ContinueStatement,), single_statement_reductor
    G[Statement] += (DeferStatement,), single_statement_reductor
    G[Statement] += (ExpressionStatement,), single_statement_reductor
    G[Statement] += (Block,), single_statement_reductor
    
    # Variable declaration
    G[VarDecl] += (identifier, colon, Type, assign, Expression, semicolon), var_decl_reductor
    G[VarDecl] += (identifier, colon, Type, semicolon), var_decl_reductor
    G[VarDecl] += (identifier, assign, Expression, semicolon), var_decl_reductor
    G[VarDecl] += (const_kw, identifier, assign, Expression, semicolon), const_decl_reductor
    
    # If statement
    G[IfStatement] += (if_kw, lparen, Expression, rparen, Block), if_reductor
    G[IfStatement] += (if_kw, lparen, Expression, rparen, Block, else_kw, Block), if_reductor
    G[IfStatement] += (if_kw, lparen, Expression, rparen, Block, else_kw, IfStatement), if_reductor
    
    # While statement
    G[WhileStatement] += (while_kw, lparen, Expression, rparen, Block), while_reductor
    
    # For statement
    G[ForStatement] += (for_kw, lparen, Expression, semicolon, Expression, semicolon, Expression, rparen, Block), for_reductor
    G[ForStatement] += (for_kw, lparen, VarDecl, Expression, semicolon, Expression, rparen, Block), for_reductor
    
    # Foreach statement
    G[ForeachStatement] += (foreach_kw, lparen, identifier, colon, Type, in_kw, Expression, rparen, Block), foreach_reductor
    G[ForeachStatement] += (foreach_kw, lparen, identifier, in_kw, Expression, rparen, Block), foreach_reductor
    
    # Switch statement
    G[SwitchStatement] += (switch_kw, lparen, Expression, rparen, lbrace, CaseClauseList, rbrace), switch_reductor
    G[SwitchStatement] += (switch_kw, lparen, Expression, rparen, lbrace, CaseClauseList, default_kw, colon, StatementList, rbrace), switch_reductor
    
    # Case clause
    G[CaseClause] += (case_kw, Expression, colon, StatementList), case_reductor
    
    # Case clause list
    G[CaseClauseList] += (CaseClauseList, CaseClause), case_list_reductor
    G[CaseClauseList] += (CaseClause,), single_case_reductor
    
    # Return statement
    G[ReturnStatement] += (return_kw, semicolon), return_reductor
    G[ReturnStatement] += (return_kw, Expression, semicolon), return_reductor
    
    # Break statement
    G[BreakStatement] += (break_kw, semicolon), break_reductor
    
    # Continue statement
    G[ContinueStatement] += (continue_kw, semicolon), continue_reductor
    
    # Defer statement
    G[DeferStatement] += (defer_kw, Statement), defer_reductor
    
    # Expression statement
    G[ExpressionStatement] += (Expression, semicolon), expression_statement_reductor
    
    # =========================================================================
    # Function Declarations
    # =========================================================================
    
    # Function declaration
    G[FnDecl] += (fn, identifier, lparen, FnParams, rparen, arrow, Type, Block), fn_decl_reductor
    G[FnDecl] += (fn, identifier, lparen, FnParams, rparen, Block), fn_decl_reductor
    G[FnDecl] += (fn, identifier, lparen, rparen, arrow, Type, Block), fn_decl_reductor
    G[FnDecl] += (fn, identifier, lparen, rparen, Block), fn_decl_reductor
    
    # Function parameters
    G[FnParams] += (FnParams, comma, FnParam), param_list_reductor
    G[FnParams] += (FnParam,), single_param_reductor
    
    # Function parameter
    G[FnParam] += (identifier, colon, Type), fn_param_reductor
    G[FnParam] += (identifier, colon, Type, assign, Expression), fn_param_reductor
    
    # =========================================================================
    # Class Declarations
    # =========================================================================
    
    # Class declaration
    G[ClassDecl] += (class_kw, identifier, ClassBody), class_decl_reductor
    G[ClassDecl] += (class_kw, identifier, extends_kw, identifier, ClassBody), class_decl_reductor
    G[ClassDecl] += (class_kw, identifier, implements_kw, identifier, ClassBody), class_decl_reductor
    G[ClassDecl] += (class_kw, identifier, extends_kw, identifier, implements_kw, identifier, ClassBody), class_decl_reductor
    
    # Class body
    G[ClassBody] += (lbrace, ClassMemberList, rbrace), class_body_reductor
    G[ClassBody] += (lbrace, rbrace), class_body_reductor
    
    # Class member list
    G[ClassMemberList] += (ClassMemberList, ClassMember), member_list_reductor
    G[ClassMemberList] += (ClassMember,), single_member_reductor
    
    # Class member
    G[ClassMember] += (VarDecl,), single_statement_reductor
    G[ClassMember] += (FnDecl,), single_statement_reductor
    G[ClassMember] += (ConstructorDecl,), single_statement_reductor
    G[ClassMember] += (DestructorDecl,), single_statement_reductor
    
    # Constructor declaration
    G[ConstructorDecl] += (identifier, lparen, FnParams, rparen, Block), constructor_reductor
    G[ConstructorDecl] += (identifier, lparen, rparen, Block), constructor_reductor
    
    # Destructor declaration
    G[DestructorDecl] += (tilde, identifier, lparen, rparen, Block), destructor_reductor
    
    # =========================================================================
    # Struct Declarations
    # =========================================================================
    
    # Struct declaration
    G[StructDecl] += (struct_kw, identifier, StructBody), struct_decl_reductor
    
    # Struct body
    G[StructBody] += (lbrace, StructMemberList, rbrace), struct_body_reductor
    G[StructBody] += (lbrace, rbrace), struct_body_reductor
    
    # Struct member list
    G[StructMemberList] += (StructMemberList, VarDecl), member_list_reductor
    G[StructMemberList] += (VarDecl,), single_member_reductor
    
    # =========================================================================
    # Enum Declarations
    # =========================================================================
    
    # Enum declaration
    G[EnumDecl] += (enum_kw, identifier, lbrace, EnumMemberList, rbrace), enum_decl_reductor
    
    # Enum member list
    G[EnumMemberList] += (EnumMemberList, comma, EnumMember), enum_member_list_reductor
    G[EnumMemberList] += (EnumMember,), single_enum_member_reductor
    
    # Enum member
    G[EnumMember] += (identifier,), enum_member_reductor
    G[EnumMember] += (identifier, assign, integer), enum_member_reductor
    
    # =========================================================================
    # Interface Declarations
    # =========================================================================
    
    # Interface declaration
    G[InterfaceDecl] += (interface_kw, identifier, InterfaceBody), interface_decl_reductor
    G[InterfaceDecl] += (interface_kw, identifier, extends_kw, identifier, InterfaceBody), interface_decl_reductor
    
    # Interface body
    G[InterfaceBody] += (lbrace, InterfaceMemberList, rbrace), interface_body_reductor
    G[InterfaceBody] += (lbrace, rbrace), interface_body_reductor
    
    # Interface member list
    G[InterfaceMemberList] += (InterfaceMemberList, FnDecl), member_list_reductor
    G[InterfaceMemberList] += (FnDecl,), single_member_reductor
    
    return G


def build_c3pp_parser():
    """
    Build the C3++ parser from the grammar.
    
    Returns:
        Configured parser instance
    """
    grammar = create_c3pp_grammar()
    return ParserBuilder.build_parser_from_attributed(grammar, ParserType.LALR1)
