import io
import pytest

from src.lexer import Lexer
from src.my_token import Token
from src.token_type import TokenType
from src.lexer_config import LexerConfig
from src.pyscript_exceptions import LexerException


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


def test_too_long_comments():
    config = LexerConfig(max_comment_length=5)
    source = io.StringIO("/*Shor*/ /*Exact*/ /*TooLon*/")
    lexer = Lexer(source, config)

    assert lexer.get_next_token().get_type() == TokenType.BLOCK_COMMENT
    assert lexer.get_next_token().get_type() == TokenType.BLOCK_COMMENT
    with pytest.raises(LexerException):
        lexer.get_next_token()
