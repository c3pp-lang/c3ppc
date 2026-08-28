"""
C3++ Token Types
================
Token type definitions for the C3++ programming language (full C3 spec).
"""

from pylgen.common.enums import TokenType


class C3ppTokenType(TokenType):
    """Token types for C3++ language."""
    
    # Literals
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    STRING = 'STRING'
    CHAR = 'CHAR'
    BOOL = 'BOOL'
    HEX = 'HEX'
    OCTAL = 'OCTAL'
    BINARY = 'BINARY'
    RAW_STRING = 'RAW_STRING'       # `...` raw strings
    
    # Identifiers and Keywords
    IDENTIFIER = 'IDENTIFIER'
    KEYWORD = 'KEYWORD'
    
    # Operators
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    STAR = 'STAR'
    SLASH = 'SLASH'
    PERCENT = 'PERCENT'
    CARET = 'CARET'
    AMPERSAND = 'AMPERSAND'
    PIPE = 'PIPE'
    TILDE = 'TILDE'
    BANG = 'BANG'
    QUESTION = 'QUESTION'
    
    # Comparison
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'
    
    # Logical
    AND = 'AND'
    OR = 'OR'
    
    # Assignment
    ASSIGN = 'ASSIGN'
    PLUS_ASSIGN = 'PLUS_ASSIGN'
    MINUS_ASSIGN = 'MINUS_ASSIGN'
    STAR_ASSIGN = 'STAR_ASSIGN'
    SLASH_ASSIGN = 'SLASH_ASSIGN'
    PERCENT_ASSIGN = 'PERCENT_ASSIGN'
    AMPERSAND_ASSIGN = 'AMPERSAND_ASSIGN'
    PIPE_ASSIGN = 'PIPE_ASSIGN'
    CARET_ASSIGN = 'CARET_ASSIGN'
    
    # Increment/Decrement
    PLUS_PLUS = 'PLUS_PLUS'
    MINUS_MINUS = 'MINUS_MINUS'
    
    # Arrow operators
    ARROW = 'ARROW'
    DOUBLE_COLON = 'DOUBLE_COLON'
    COLON = 'COLON'
    DOT = 'DOT'
    ELLIPSIS = 'ELLIPSIS'           # ...
    
    # Optional/Fault operators
    NULL_COALESCE = 'NULL_COALESCE' # ??
    RETHROW = 'RETHROW'             # !
    
    # Range
    RANGE = 'RANGE'                 # ..
    
    # Delimiters
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'
    SEMICOLON = 'SEMICOLON'
    COMMA = 'COMMA'
    AT = 'AT'                       # @ for contracts
    
    # Special
    EOF = 'EOF'
    NEWLINE = 'NEWLINE'
    WHITESPACE = 'WHITESPACE'
    COMMENT = 'COMMENT'
    LINE_COMMENT = 'LINE_COMMENT'
    BLOCK_COMMENT = 'BLOCK_COMMENT'


# ── C3++ Keywords (complete list) ──────────────────────────────────

# OO keywords
C3PP_KEYWORDS_OO = {
    'class', 'struct', 'enum', 'interface', 'union',
    'extends', 'implements', 'new', 'this', 'super',
    'public', 'private', 'protected',
    'static', 'virtual', 'override', 'abstract', 'const',
    'fault',                      # fault constants
}

# Control flow
C3PP_KEYWORDS_CONTROL = {
    'fn', 'return', 'if', 'else', 'while', 'for', 'foreach', 'in',
    'switch', 'case', 'default', 'break', 'continue', 'defer',
    'goto', 'do',
}

# Types
C3PP_KEYWORDS_TYPES = {
    'int', 'long', 'short', 'float', 'double', 'char', 'bool', 'void', 'string',
    'true', 'false', 'null',
    'ichar', 'ushrt', 'uint', 'ulong', 'int128', 'uint128',
    'iptr', 'uptr', 'sz', 'usz',
    'any', 'typeid',
}

# Other
C3PP_KEYWORDS_OTHER = {
    'import', 'module', 'as', 'alias', 'distinct',
    'assert', 'ynamic', 'typeof', 'sizeof', 'alignof',
    'generic', 'macro', 'define',
}

# All keywords combined
C3PP_KEYWORDS = (
    C3PP_KEYWORDS_OO | C3PP_KEYWORDS_CONTROL |
    C3PP_KEYWORDS_TYPES | C3PP_KEYWORDS_OTHER
)


def get_keyword_pattern() -> str:
    """Get combined keyword pattern for lexer."""
    return '|'.join(sorted(C3PP_KEYWORDS, key=len, reverse=True))
