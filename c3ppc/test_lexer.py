"""
Simple test for C3++ lexer
"""

import sys
sys.path.insert(0, '.')

from c3ppc.lexer.lexer import C3ppLexer, create_c3pp_lexer
from c3ppc.lexer.tokens import C3ppTokenType
from pylgen.common.types import Symbol


def test_lexer():
    """Test the C3++ lexer."""
    print("Testing C3++ Lexer...")
    print("=" * 50)
    
    # Create lexer
    lexer = create_c3pp_lexer()
    
    # Simple symbol mapping function
    def symbol_func(token_type: C3ppTokenType, text: str) -> Symbol:
        return Symbol(text, True)
    
    # Create lexer instance
    pylgen_lexer = lexer.create_lexer(symbol_func)
    
    # Test source code
    source = """
    module test;
    
    class Animal {
        string name;
        
        Animal(string name) {
            this.name = name;
        }
        
        virtual string speak() {
            return "...";
        }
    }
    
    fn int main() {
        Animal a = new Animal("Dog");
        printf("%s\\n", a.speak());
        return 0;
    }
    """
    
    print("Source code:")
    print(source)
    print()
    
    # Tokenize
    tokens = lexer.tokenize(source)
    
    print(f"Generated {len(tokens)} tokens:")
    print("-" * 50)
    
    for i, token in enumerate(tokens[:50]):  # Print first 50 tokens
        print(f"{i:3d}: {token.type:20s} | {repr(token.text):30s} | Line {token.line}, Col {token.column}")
    
    if len(tokens) > 50:
        print(f"... and {len(tokens) - 50} more tokens")
    
    print()
    print("Lexer test completed successfully!")
    return True


def test_token_types():
    """Test specific token types."""
    print("\nTesting Token Types...")
    print("=" * 50)
    
    # Test various token patterns
    test_cases = [
        ("class", C3ppTokenType.CLASS),
        ("fn", C3ppTokenType.FN),
        ("return", C3ppTokenType.RETURN),
        ("if", C3ppTokenType.IF),
        ("else", C3ppTokenType.ELSE),
        ("while", C3ppTokenType.WHILE),
        ("for", C3ppTokenType.FOR),
        ("foreach", C3ppTokenType.FOREACH),
        ("switch", C3ppTokenType.SWITCH),
        ("case", C3ppTokenType.CASE),
        ("default", C3ppTokenType.DEFAULT),
        ("break", C3ppTokenType.BREAK),
        ("continue", C3ppTokenType.CONTINUE),
        ("defer", C3ppTokenType.DEFER),
        ("int", C3ppTokenType.INT),
        ("long", C3ppTokenType.LONG),
        ("float", C3ppTokenType.FLOAT_TYPE),
        ("double", C3ppTokenType.DOUBLE),
        ("char", C3ppTokenType.CHAR_TYPE),
        ("bool", C3ppTokenType.BOOL_TYPE),
        ("void", C3ppTokenType.VOID),
        ("string", C3ppTokenType.STRING_TYPE),
        ("struct", C3ppTokenType.STRUCT),
        ("enum", C3ppTokenType.ENUM),
        ("interface", C3ppTokenType.INTERFACE),
        ("extends", C3ppTokenType.EXTENDS),
        ("implements", C3ppTokenType.IMPLEMENTS),
        ("new", C3ppTokenType.NEW),
        ("this", C3ppTokenType.THIS),
        ("super", C3ppTokenType.SUPER),
        ("public", C3ppTokenType.PUBLIC),
        ("private", C3ppTokenType.PRIVATE),
        ("protected", C3ppTokenType.PROTECTED),
        ("static", C3ppTokenType.STATIC),
        ("virtual", C3ppTokenType.VIRTUAL),
        ("override", C3ppTokenType.OVERRIDE),
        ("abstract", C3ppTokenType.ABSTRACT),
        ("const", C3ppTokenType.CONST),
        ("import", C3ppTokenType.IMPORT),
        ("module", C3ppTokenType.MODULE),
        ("as", C3ppTokenType.AS),
        ("true", C3ppTokenType.BOOL),
        ("false", C3ppTokenType.BOOL),
        ("42", C3ppTokenType.INTEGER),
        ("3.14", C3ppTokenType.FLOAT),
        ('"hello"', C3ppTokenType.STRING),
        ("'c'", C3ppTokenType.CHAR),
        ("identifier", C3ppTokenType.IDENTIFIER),
        ("+", C3ppTokenType.PLUS),
        ("-", C3ppTokenType.MINUS),
        ("*", C3ppTokenType.STAR),
        ("/", C3ppTokenType.SLASH),
        ("%", C3ppTokenType.PERCENT),
        ("^", C3ppTokenType.CARET),
        ("&", C3ppTokenType.AMPERSAND),
        ("|", C3ppTokenType.PIPE),
        ("~", C3ppTokenType.TILDE),
        ("!", C3ppTokenType.BANG),
        ("?", C3ppTokenType.QUESTION),
        ("==", C3ppTokenType.EQUAL),
        ("!=", C3ppTokenType.NOT_EQUAL),
        ("<", C3ppTokenType.LESS),
        ("<=", C3ppTokenType.LESS_EQUAL),
        (">", C3ppTokenType.GREATER),
        (">=", C3ppTokenType.GREATER_EQUAL),
        ("&&", C3ppTokenType.AND),
        ("||", C3ppTokenType.OR),
        ("=", C3ppTokenType.ASSIGN),
        ("+=", C3ppTokenType.PLUS_ASSIGN),
        ("-=", C3ppTokenType.MINUS_ASSIGN),
        ("*=", C3ppTokenType.STAR_ASSIGN),
        ("/=", C3ppTokenType.SLASH_ASSIGN),
        ("%=", C3ppTokenType.PERCENT_ASSIGN),
        ("++", C3ppTokenType.PLUS_PLUS),
        ("--", C3ppTokenType.MINUS_MINUS),
        ("->", C3ppTokenType.ARROW),
        ("::", C3ppTokenType.DOUBLE_COLON),
        (":", C3ppTokenType.COLON),
        (".", C3ppTokenType.DOT),
        ("(", C3ppTokenType.LPAREN),
        (")", C3ppTokenType.RPAREN),
        ("{", C3ppTokenType.LBRACE),
        ("}", C3ppTokenType.RBRACE),
        ("[", C3ppTokenType.LBRACKET),
        ("]", C3ppTokenType.RBRACKET),
        (";", C3ppTokenType.SEMICOLON),
        (",", C3ppTokenType.COMMA),
    ]
    
    print(f"Testing {len(test_cases)} token patterns...")
    
    passed = 0
    failed = 0
    
    for text, expected_type in test_cases:
        # Create lexer for this single token
        lexer = create_c3pp_lexer()
        
        def symbol_func(token_type: C3ppTokenType, txt: str) -> Symbol:
            return Symbol(txt, True)
        
        pylgen_lexer = lexer.create_lexer(symbol_func)
        tokens = lexer.tokenize(text)
        
        if tokens and tokens[0].type == expected_type:
            passed += 1
        else:
            failed += 1
            actual = tokens[0].type if tokens else "NO TOKEN"
            print(f"  FAIL: {repr(text):20s} expected {expected_type:20s} got {actual}")
    
    print(f"\nResults: {passed} passed, {failed} failed out of {len(test_cases)}")
    return failed == 0


if __name__ == "__main__":
    try:
        success1 = test_lexer()
        success2 = test_token_types()
        
        print("\n" + "=" * 50)
        if success1 and success2:
            print("All tests passed!")
            sys.exit(0)
        else:
            print("Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
