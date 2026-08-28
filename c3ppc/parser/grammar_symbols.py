"""
C3++ Grammar Symbols
====================
Grammar symbols for the C3++ programming language parser.
"""

from pylgen.common.types import Symbol

# End of input symbol
END_SYMBOL = '$'

# Program structure
Program = Symbol('Program')
ModuleDecl = Symbol('ModuleDecl')
ImportDecl = Symbol('ImportDecl')
Declaration = Symbol('Declaration')
DeclarationList = Symbol('DeclarationList')

# Expressions
Expression = Symbol('Expression')
AssignmentExpr = Symbol('AssignmentExpr')
LogicalOrExpr = Symbol('LogicalOrExpr')
LogicalAndExpr = Symbol('LogicalAndExpr')
BitwiseOrExpr = Symbol('BitwiseOrExpr')
BitwiseXorExpr = Symbol('BitwiseXorExpr')
BitwiseAndExpr = Symbol('BitwiseAndExpr')
EqualityExpr = Symbol('EqualityExpr')
RelationalExpr = Symbol('RelationalExpr')
ShiftExpr = Symbol('ShiftExpr')
AdditiveExpr = Symbol('AdditiveExpr')
MultiplicativeExpr = Symbol('MultiplicativeExpr')
UnaryExpr = Symbol('UnaryExpr')
PostfixExpr = Symbol('PostfixExpr')
PrimaryExpr = Symbol('PrimaryExpr')

# Statements
Statement = Symbol('Statement')
Block = Symbol('Block')
StatementList = Symbol('StatementList')
IfStatement = Symbol('IfStatement')
WhileStatement = Symbol('WhileStatement')
ForStatement = Symbol('ForStatement')
ForeachStatement = Symbol('ForeachStatement')
SwitchStatement = Symbol('SwitchStatement')
ReturnStatement = Symbol('ReturnStatement')
BreakStatement = Symbol('BreakStatement')
ContinueStatement = Symbol('ContinueStatement')
DeferStatement = Symbol('DeferStatement')
ExpressionStatement = Symbol('ExpressionStatement')

# Declarations
VarDecl = Symbol('VarDecl')
VarDeclList = Symbol('VarDeclList')
FnDecl = Symbol('FnDecl')
FnParams = Symbol('FnParams')
FnParam = Symbol('FnParam')
TypeDecl = Symbol('TypeDecl')

# Types
Type = Symbol('Type')
BasicType = Symbol('BasicType')
PointerType = Symbol('PointerType')
ArrayType = Symbol('ArrayType')
SliceType = Symbol('SliceType')
FunctionType = Symbol('FunctionType')

# Class declarations
ClassDecl = Symbol('ClassDecl')
ClassBody = Symbol('ClassBody')
ClassMember = Symbol('ClassMember')
ClassMemberList = Symbol('ClassMemberList')
ConstructorDecl = Symbol('ConstructorDecl')
DestructorDecl = Symbol('DestructorDecl')
MethodDecl = Symbol('MethodDecl')

# Struct declarations
StructDecl = Symbol('StructDecl')
StructBody = Symbol('StructBody')
StructMember = Symbol('StructMember')
StructMemberList = Symbol('StructMemberList')

# Enum declarations
EnumDecl = Symbol('EnumDecl')
EnumBody = Symbol('EnumBody')
EnumMember = Symbol('EnumMember')
EnumMemberList = Symbol('EnumMemberList')

# Interface declarations
InterfaceDecl = Symbol('InterfaceDecl')
InterfaceBody = Symbol('InterfaceBody')
InterfaceMember = Symbol('InterfaceMember')
InterfaceMemberList = Symbol('InterfaceMemberList')

# Access modifiers
AccessModifier = Symbol('AccessModifier')

# Misc
Identifier = Symbol('Identifier')
TypeAnnotation = Symbol('TypeAnnotation')
ExprList = Symbol('ExprList')
ArgumentList = Symbol('ArgumentList')
CaseClause = Symbol('CaseClause')
CaseClauseList = Symbol('CaseClauseList')

# Terminal symbols (from lexer)
# Keywords
fn = Symbol('fn', True)
return_kw = Symbol('return', True)
if_kw = Symbol('if', True)
else_kw = Symbol('else', True)
while_kw = Symbol('while', True)
for_kw = Symbol('for', True)
foreach_kw = Symbol('foreach', True)
switch_kw = Symbol('switch', True)
case_kw = Symbol('case', True)
default_kw = Symbol('default', True)
break_kw = Symbol('break', True)
continue_kw = Symbol('continue', True)
defer_kw = Symbol('defer', True)

# Type keywords
int_kw = Symbol('int', True)
long_kw = Symbol('long', True)
short_kw = Symbol('short', True)
float_kw = Symbol('float', True)
double_kw = Symbol('double', True)
char_kw = Symbol('char', True)
bool_kw = Symbol('bool', True)
void_kw = Symbol('void', True)
string_kw = Symbol('string', True)

# OO keywords
class_kw = Symbol('class', True)
struct_kw = Symbol('struct', True)
enum_kw = Symbol('enum', True)
interface_kw = Symbol('interface', True)
extends_kw = Symbol('extends', True)
implements_kw = Symbol('implements', True)
new_kw = Symbol('new', True)
this_kw = Symbol('this', True)
super_kw = Symbol('super', True)

# Access modifiers
public_kw = Symbol('public', True)
private_kw = Symbol('private', True)
protected_kw = Symbol('protected', True)

# Other modifiers
static_kw = Symbol('static', True)
virtual_kw = Symbol('virtual', True)
override_kw = Symbol('override', True)
abstract_kw = Symbol('abstract', True)
const_kw = Symbol('const', True)
mutable_kw = Symbol('mutable', True)

# Other keywords
import_kw = Symbol('import', True)
module_kw = Symbol('module', True)
as_kw = Symbol('as', True)
typedef_kw = Symbol('typedef', True)
alias_kw = Symbol('alias', True)
in_kw = Symbol('in', True)

# Literals
integer = Symbol('integer', True)
float_literal = Symbol('float_literal', True)
string_literal = Symbol('string_literal', True)
char_literal = Symbol('char_literal', True)
bool_literal = Symbol('bool_literal', True)
identifier = Symbol('identifier', True)

# Operators
plus = Symbol('+', True)
minus = Symbol('-', True)
star = Symbol('*', True)
slash = Symbol('/', True)
percent = Symbol('%', True)
caret = Symbol('^', True)
ampersand = Symbol('&', True)
pipe = Symbol('|', True)
tilde = Symbol('~', True)
bang = Symbol('!', True)
question = Symbol('?', True)

# Comparison
equal = Symbol('==', True)
not_equal = Symbol('!=', True)
less = Symbol('<', True)
less_equal = Symbol('<=', True)
greater = Symbol('>', True)
greater_equal = Symbol('>=', True)

# Logical
and_op = Symbol('&&', True)
or_op = Symbol('||', True)

# Assignment
assign = Symbol('=', True)
plus_assign = Symbol('+=', True)
minus_assign = Symbol('-=', True)
star_assign = Symbol('*=', True)
slash_assign = Symbol('/=', True)
percent_assign = Symbol('%=', True)
ampersand_assign = Symbol('&=', True)
pipe_assign = Symbol('|=', True)
caret_assign = Symbol('^=', True)

# Increment/Decrement
plus_plus = Symbol('++', True)
minus_minus = Symbol('--', True)

# Arrow and special
arrow = Symbol('->', True)
double_colon = Symbol('::', True)
colon = Symbol(':', True)
dot = Symbol('.', True)

# Delimiters
lparen = Symbol('(', True)
rparen = Symbol(')', True)
lbrace = Symbol('{', True)
rbrace = Symbol('}', True)
lbracket = Symbol('[', True)
rbracket = Symbol(']', True)
semicolon = Symbol(';', True)
comma = Symbol(',', True)
