import io
import pytest

from src.lexer import Lexer
from src.my_token import Token
from src.token_type import TokenType


def test_code_integer():
    source = io.StringIO(
        """
{
    10;
    -50 +29;
}
"""
    )
    lexer = Lexer(source)

    assert lexer.get_next_token().get_type() == TokenType.LEFT_CURLY_BRACKET
    assert lexer.get_next_token().get_type() == TokenType.INT_LITERAL
    assert lexer.get_next_token().get_type() == TokenType.SEMICOLON
    assert lexer.get_next_token().get_type() == TokenType.MINUS_OPERATOR
    assert lexer.get_next_token().get_type() == TokenType.INT_LITERAL
    assert lexer.get_next_token().get_type() == TokenType.PLUS_OPERATOR
    assert lexer.get_next_token().get_type() == TokenType.INT_LITERAL
    assert lexer.get_next_token().get_type() == TokenType.SEMICOLON
    assert lexer.get_next_token().get_type() == TokenType.RIGHT_CURLY_BRACKET
    assert lexer.get_next_token().get_type() == TokenType.EOF


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

    assert lexer.get_next_token().get_type() == TokenType.LEFT_CURLY_BRACKET
    assert lexer.get_next_token().get_type() == TokenType.FLOAT_LITERAL
    assert lexer.get_next_token().get_type() == TokenType.SEMICOLON
    assert lexer.get_next_token().get_type() == TokenType.MINUS_OPERATOR
    assert lexer.get_next_token().get_type() == TokenType.FLOAT_LITERAL
    assert lexer.get_next_token().get_type() == TokenType.MUL_OPERATOR
    assert lexer.get_next_token().get_type() == TokenType.FLOAT_LITERAL
    assert lexer.get_next_token().get_type() == TokenType.SEMICOLON
    assert lexer.get_next_token().get_type() == TokenType.RIGHT_CURLY_BRACKET
