import io
import pytest

from src.lexer import Lexer
from src.my_token import Token
from src.token_type import TokenType
from src.lexer_config import LexerConfig
from src.pyscript_exceptions import (
    LengthException,
    UnclosedException,
    InvalidValueException,
)


def test_build_simple_and_operators():
    source = io.StringIO(".,:;*(){}[]!=!-=-/*He/*l*lo*///Hel/**/llo\r\n+=+ ===\t>=><=<")
    lexer = Lexer(source)

    assert lexer.get_next_token() == Token(TokenType.DOT_OPERATOR, (1, 1))
    assert lexer.get_next_token() == Token(TokenType.COMMA, (1, 2))
    assert lexer.get_next_token() == Token(TokenType.COLON, (1, 3))
    assert lexer.get_next_token() == Token(TokenType.SEMICOLON, (1, 4))
    assert lexer.get_next_token() == Token(TokenType.MUL_OPERATOR, (1, 5))
    assert lexer.get_next_token() == Token(TokenType.LEFT_BRACKET, (1, 6))
    assert lexer.get_next_token() == Token(TokenType.RIGHT_BRACKET, (1, 7))
    assert lexer.get_next_token() == Token(TokenType.LEFT_CURLY_BRACKET, (1, 8))
    assert lexer.get_next_token() == Token(TokenType.RIGHT_CURLY_BRACKET, (1, 9))
    assert lexer.get_next_token() == Token(TokenType.LEFT_SQUARE_BRACKET, (1, 10))
    assert lexer.get_next_token() == Token(TokenType.RIGHT_SQUARE_BRACKET, (1, 11))
    assert lexer.get_next_token() == Token(TokenType.NEQ_OPERATOR, (1, 12))
    assert lexer.get_next_token() == Token(TokenType.LOGIC_NEG_OPERATOR, (1, 14))
    assert lexer.get_next_token() == Token(TokenType.ASSIGN_MINUS_OPERATOR, (1, 15))
    assert lexer.get_next_token() == Token(TokenType.MINUS_OPERATOR, (1, 17))
    assert lexer.get_next_token() == Token(TokenType.BLOCK_COMMENT, (1, 18))
    assert lexer.get_next_token() == Token(TokenType.LINE_COMMENT, (1, 30))
    assert lexer.get_next_token() == Token(TokenType.ASSIGN_PLUS_OPERATOR, (2, 1))
    assert lexer.get_next_token() == Token(TokenType.ADD_OPERATOR, (2, 3))
    assert lexer.get_next_token() == Token(TokenType.EQ_OPERATOR, (2, 5))
    assert lexer.get_next_token() == Token(TokenType.ASSIGN_OPERATOR, (2, 7))
    assert lexer.get_next_token() == Token(TokenType.GEQ_OPERATOR, (2, 9))
    assert lexer.get_next_token() == Token(TokenType.GREATER_OPERATOR, (2, 11))
    assert lexer.get_next_token() == Token(TokenType.LEQ_OPERATOR, (2, 12))
    assert lexer.get_next_token() == Token(TokenType.LESS_OPERATOR, (2, 14))
    assert lexer.get_next_token() == Token(TokenType.EOF, (2, 15))
    assert lexer.get_next_token() == Token(TokenType.EOF, (2, 15))


def test_too_long_block_comments():
    config = LexerConfig(max_comment_length=5)
    source = io.StringIO("/*Shor*/ /*Exact*/ /*TooLon*/")
    lexer = Lexer(source, config)

    assert lexer.get_next_token().get_type() == TokenType.BLOCK_COMMENT
    assert lexer.get_next_token().get_type() == TokenType.BLOCK_COMMENT
    with pytest.raises(LengthException):
        lexer.get_next_token()


def test_too_long_line_comments():
    config = LexerConfig(max_comment_length=5)
    source = io.StringIO("//Shor\n//Exact\n//TooLon")
    lexer = Lexer(source, config)

    assert lexer.get_next_token().get_type() == TokenType.LINE_COMMENT
    assert lexer.get_next_token().get_type() == TokenType.LINE_COMMENT
    with pytest.raises(LengthException):
        lexer.get_next_token()


def test_block_comment_not_closed():
    source = io.StringIO("/*Comment not closed*")
    lexer = Lexer(source)

    with pytest.raises(UnclosedException):
        lexer.get_next_token()


def test_keywords():
    source = io.StringIO(
        "if else function return while for from in select where order by descending True False or and"
    )
    lexer = Lexer(source)

    assert lexer.get_next_token() == Token(TokenType.IF_KEYWORD, (1, 1))
    assert lexer.get_next_token() == Token(TokenType.ELSE_KEYWORD, (1, 4))
    assert lexer.get_next_token() == Token(TokenType.FUNCTION_KEYWORD, (1, 9))
    assert lexer.get_next_token() == Token(TokenType.RETURN_KEYWORD, (1, 18))
    assert lexer.get_next_token() == Token(TokenType.WHILE_KEYWORD, (1, 25))
    assert lexer.get_next_token() == Token(TokenType.FOR_KEYWORD, (1, 31))
    assert lexer.get_next_token() == Token(TokenType.FROM_KEYWORD, (1, 35))
    assert lexer.get_next_token() == Token(TokenType.IN_KEYWORD, (1, 40))
    assert lexer.get_next_token() == Token(TokenType.SELECT_KEYWORD, (1, 43))
    assert lexer.get_next_token() == Token(TokenType.WHERE_KEYWORD, (1, 50))
    assert lexer.get_next_token() == Token(TokenType.ORDER_KEYWORD, (1, 56))
    assert lexer.get_next_token() == Token(TokenType.BY_KEYWORD, (1, 62))
    assert lexer.get_next_token() == Token(TokenType.DESCENDING_KEYWORD, (1, 65))
    assert lexer.get_next_token() == Token(TokenType.TRUE_LITERAL, (1, 76))
    assert lexer.get_next_token() == Token(TokenType.FALSE_LITERAL, (1, 81))
    assert lexer.get_next_token() == Token(TokenType.OR_OPERATOR, (1, 87))
    assert lexer.get_next_token() == Token(TokenType.AND_OPERATOR, (1, 90))


def test_identifiers():
    source = io.StringIO("Hello there")
    lexer = Lexer(source)

    assert lexer.get_next_token() == Token(TokenType.IDENTIFIER, (1, 1), "Hello")
    assert lexer.get_next_token() == Token(TokenType.IDENTIFIER, (1, 7), "there")


def test_too_long_identifiers():
    config = LexerConfig(max_identifier_length=10)
    source = io.StringIO("good descending toolongidentifier")
    lexer = Lexer(source, config)
    assert lexer.get_next_token().get_type() == TokenType.IDENTIFIER
    assert lexer.get_next_token().get_type() == TokenType.DESCENDING_KEYWORD
    with pytest.raises(LengthException):
        lexer.get_next_token()


def test_string_literal():
    source = io.StringIO(r'"Hello there" "another string"')
    lexer = Lexer(source)

    assert lexer.get_next_token() == Token(
        TokenType.STRING_LITERAL, (1, 1), "Hello there"
    )
    assert lexer.get_next_token() == Token(
        TokenType.STRING_LITERAL, (1, 15), "another string"
    )


def test_string_not_closed():
    source = io.StringIO(r'"Hello there" "unclosed string')
    lexer = Lexer(source)

    assert lexer.get_next_token().get_type() == TokenType.STRING_LITERAL
    with pytest.raises(UnclosedException):
        lexer.get_next_token()


def test_too_long_strings():
    config = LexerConfig(max_string_literal_length=10)
    source = io.StringIO(r'"Goodstr" "Atlimitstr" "Too long string"')
    lexer = Lexer(source, config)

    assert lexer.get_next_token().get_type() == TokenType.STRING_LITERAL
    assert lexer.get_next_token().get_type() == TokenType.STRING_LITERAL
    with pytest.raises(LengthException):
        lexer.get_next_token()


def test_escaping_strings():
    source = io.StringIO(r'"Hello with \"escaping\" chars" "Another \"escaping\""')
    lexer = Lexer(source)

    assert lexer.get_next_token() == Token(
        TokenType.STRING_LITERAL, (1, 1), r'Hello with "escaping" chars'
    )
    assert lexer.get_next_token() == Token(
        TokenType.STRING_LITERAL, (1, 33), r'Another "escaping"'
    )


def test_int_literal():
    source = io.StringIO("12345 0 14000 25")
    lexer = Lexer(source)

    assert lexer.get_next_token() == Token(TokenType.INT_LITERAL, (1, 1), 12345)
    assert lexer.get_next_token() == Token(TokenType.INT_LITERAL, (1, 7), 0)
    assert lexer.get_next_token() == Token(TokenType.INT_LITERAL, (1, 9), 14000)
    assert lexer.get_next_token() == Token(TokenType.INT_LITERAL, (1, 15), 25)


def test_int_something_after_0():
    source = io.StringIO("12345 025 123")
    lexer = Lexer(source)

    assert lexer.get_next_token() == Token(TokenType.INT_LITERAL, (1, 1), 12345)
    with pytest.raises(InvalidValueException):
        lexer.get_next_token()


def test_too_long_int():
    source = io.StringIO("1234 12345 123456")
    config = LexerConfig(max_int_literal_length=5)
    lexer = Lexer(source, config)

    assert lexer.get_next_token().get_type() == TokenType.INT_LITERAL
    assert lexer.get_next_token().get_type() == TokenType.INT_LITERAL
    with pytest.raises(LengthException):
        lexer.get_next_token()
