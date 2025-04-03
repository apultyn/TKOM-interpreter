import io
import pytest

from src.lexer import Lexer
from src.token_type import TokenType


def test_code_integer():
    source = io.StringIO(
        """
{
    10;
    -50 +-29;
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.MINUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.PLUS_OPERATOR,
        TokenType.MINUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_code_float():
    source = io.StringIO(
        """
{
    1.0;
    -15.38*2.0;
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.FLOAT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.MINUS_OPERATOR,
        TokenType.FLOAT_LITERAL,
        TokenType.MUL_OPERATOR,
        TokenType.FLOAT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_string_code():
    source = io.StringIO(
        """
{
    "Hello World!";
    "Typing with quotes: \\"\\" and backslash: \\ there";
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.SEMICOLON,
        TokenType.STRING_LITERAL,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_bool_code():
    source = io.StringIO(
        """
{
    True;
    False;
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.TRUE_LITERAL,
        TokenType.SEMICOLON,
        TokenType.FALSE_LITERAL,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_list_code():
    source = io.StringIO(
        """
{
    [];
    [1, "Hello", -10.5, ("key": 5),
        ["hello", "from", "sublist"],
        {("name": "dict"), ("value": 5)})
    ];
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.SEMICOLON,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.MINUS_OPERATOR,
        TokenType.FLOAT_LITERAL,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_dict_code():
    source = io.StringIO(
        """
{
    {};
    {
        ("first_key": 5),
        ("another_key": "value"),
        ("one_more": [1, 5, "hello"]),
        ("last_one": {("key": "value")})
    };
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.SEMICOLON,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_variable_code():
    source = io.StringIO(
        """
{
    a = "Hello there";
    my_list = [1, "Hello", {
        (False: True),
        (-52.48: [1, 2, "Hello"])
    }];
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.STRING_LITERAL,
        TokenType.SEMICOLON,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_BRACKET,
        TokenType.FALSE_LITERAL,
        TokenType.COLON,
        TokenType.TRUE_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.MINUS_OPERATOR,
        TokenType.FLOAT_LITERAL,
        TokenType.COLON,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF
    ]
