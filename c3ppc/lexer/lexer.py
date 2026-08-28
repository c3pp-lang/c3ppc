"""
C3++ Lexer
==========
Lexer implementation for the C3++ programming language.
Uses Python's re module for tokenization with pylgen-compatible output.
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Callable

from pylgen.common.types import Symbol
from .tokens import C3ppTokenType, C3PP_KEYWORDS


@dataclass
class Token:
    """Represents a single token."""
    type: C3ppTokenType
    text: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.text)}, L{self.line}:C{self.column})"


class C3ppLexer:
    """
    Lexer for the C3++ programming language.
    
    C3++ extends C3 with object-oriented features including:
    - Classes with inheritance
    - Virtual methods and abstract classes
    - Access modifiers (public, private, protected)
    - Constructors and destructors
    - Interfaces
    """
    
    # Token patterns: (priority, token_type, regex_pattern)
    # Higher priority number = matched first when same length
    TOKEN_PATTERNS = [
        # Comments (ignored - mapped to special type)
        (100, C3ppTokenType.LINE_COMMENT, r'//[^\n]*'),
        (100, C3ppTokenType.BLOCK_COMMENT, r'/\*[\s\S]*?\*/'),
        
        # Strings
        (90, C3ppTokenType.STRING, r'"[^"]*"'),
        (90, C3ppTokenType.CHAR, r"'[^']*'"),
        
        # Numbers (before identifiers)
        (80, C3ppTokenType.HEX, r'0[xX][0-9a-fA-F]+'),
        (80, C3ppTokenType.OCTAL, r'0[oO][0-7]+'),
        (80, C3ppTokenType.BINARY, r'0[bB][01]+'),
        (75, C3ppTokenType.FLOAT, r'[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?'),
        (70, C3ppTokenType.INTEGER, r'[0-9]+'),
        
        # Multi-character operators (before single-char)
        (60, C3ppTokenType.ARROW, r'->'),
        (60, C3ppTokenType.DOUBLE_COLON, r'::'),
        (60, C3ppTokenType.PLUS_PLUS, r'\+\+'),
        (60, C3ppTokenType.MINUS_MINUS, r'--'),
        (60, C3ppTokenType.PLUS_ASSIGN, r'\+='),
        (60, C3ppTokenType.MINUS_ASSIGN, r'-='),
        (60, C3ppTokenType.STAR_ASSIGN, r'\*='),
        (60, C3ppTokenType.SLASH_ASSIGN, r'/='),
        (60, C3ppTokenType.PERCENT_ASSIGN, r'%='),
        (60, C3ppTokenType.AMPERSAND_ASSIGN, r'&='),
        (60, C3ppTokenType.PIPE_ASSIGN, r'\|='),
        (60, C3ppTokenType.CARET_ASSIGN, r'\^='),
        (60, C3ppTokenType.EQUAL, r'=='),
        (60, C3ppTokenType.NOT_EQUAL, r'!='),
        (60, C3ppTokenType.LESS_EQUAL, r'<='),
        (60, C3ppTokenType.GREATER_EQUAL, r'>='),
        (60, C3ppTokenType.AND, r'&&'),
        (60, C3ppTokenType.OR, r'\|\|'),
        (60, C3ppTokenType.NULL_COALESCE, r'\?\?'),
        (60, C3ppTokenType.RANGE, r'\.\.'),
        (60, C3ppTokenType.ELLIPSIS, r'\.\.\.'),
        
        # Single character operators
        (50, C3ppTokenType.PLUS, r'\+'),
        (50, C3ppTokenType.MINUS, r'-'),
        (50, C3ppTokenType.STAR, r'\*'),
        (50, C3ppTokenType.SLASH, r'/'),
        (50, C3ppTokenType.PERCENT, r'%'),
        (50, C3ppTokenType.CARET, r'\^'),
        (50, C3ppTokenType.AMPERSAND, r'&'),
        (50, C3ppTokenType.PIPE, r'\|'),
        (50, C3ppTokenType.TILDE, r'~'),
        (50, C3ppTokenType.BANG, r'!'),
        (50, C3ppTokenType.QUESTION, r'\?'),
        (50, C3ppTokenType.AT, r'@'),
        (50, C3ppTokenType.LESS, r'<'),
        (50, C3ppTokenType.GREATER, r'>'),
        (50, C3ppTokenType.ASSIGN, r'='),
        
        # Delimiters
        (40, C3ppTokenType.COLON, r':'),
        (40, C3ppTokenType.DOT, r'\.'),
        (40, C3ppTokenType.LPAREN, r'\('),
        (40, C3ppTokenType.RPAREN, r'\)'),
        (40, C3ppTokenType.LBRACE, r'\{'),
        (40, C3ppTokenType.RBRACE, r'\}'),
        (40, C3ppTokenType.LBRACKET, r'\['),
        (40, C3ppTokenType.RBRACKET, r'\]'),
        (40, C3ppTokenType.SEMICOLON, r';'),
        (40, C3ppTokenType.COMMA, r','),
        
        # Identifiers (and keywords - handled in post-processing)
        (10, C3ppTokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ]
    
    def __init__(self):
        """Initialize the C3++ lexer."""
        self._compiled_patterns: List[tuple] = []
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Pre-compile all regex patterns."""
        self._compiled_patterns = []
        for priority, token_type, pattern in self.TOKEN_PATTERNS:
            compiled = re.compile(pattern)
            self._compiled_patterns.append((priority, token_type, compiled))
    
    def tokenize(self, source_code: str) -> List[Token]:
        """
        Tokenize source code into a list of tokens.
        
        Args:
            source_code: C3++ source code to tokenize
            
        Returns:
            List of Token objects
        """
        tokens = []
        line = 1
        column = 1
        pos = 0
        source_len = len(source_code)
        
        while pos < source_len:
            # Skip whitespace
            if source_code[pos] in ' \t\r':
                column += 1
                pos += 1
                continue
            
            # Handle newlines
            if source_code[pos] == '\n':
                line += 1
                column = 1
                pos += 1
                continue
            
            # Try to match a token
            best_match = None
            best_length = 0
            best_type = None
            
            for priority, token_type, pattern in self._compiled_patterns:
                match = pattern.match(source_code, pos)
                if match and match.end() - match.start() > best_length:
                    best_match = match
                    best_length = match.end() - match.start()
                    best_type = token_type
            
            if best_match and best_length > 0:
                text = best_match.group()
                token_type = best_type
                
                # Skip comments
                if token_type in (C3ppTokenType.LINE_COMMENT, C3ppTokenType.BLOCK_COMMENT):
                    # Count newlines in block comments
                    if token_type == C3ppTokenType.BLOCK_COMMENT:
                        newlines = text.count('\n')
                        if newlines > 0:
                            line += newlines
                            column = len(text) - text.rfind('\n')
                        else:
                            column += len(text)
                    else:
                        column += len(text)
                    pos = best_match.end()
                    continue
                
                # Check if identifier is actually a keyword
                if token_type == C3ppTokenType.IDENTIFIER and text in C3PP_KEYWORDS:
                    token_type = C3ppTokenType.KEYWORD
                
                tokens.append(Token(token_type, text, line, column))
                column += best_length
                pos = best_match.end()
            else:
                # Unknown character - skip it
                tokens.append(Token(C3ppTokenType.IDENTIFIER, source_code[pos], line, column))
                column += 1
                pos += 1
        
        # Add EOF token
        tokens.append(Token(C3ppTokenType.EOF, 'END', line, column))
        
        return tokens
    
    def get_symbol(self, token: Token) -> Symbol:
        """
        Convert a token to a pylgen Symbol.
        
        Args:
            token: The token to convert
            
        Returns:
            Pylgen Symbol object
        """
        return Symbol(token.text, True)


def create_c3pp_lexer() -> C3ppLexer:
    """
    Factory function to create a C3++ lexer.
    
    Returns:
        Configured C3ppLexer instance
    """
    return C3ppLexer()
