import io

from src.source import Source
from src.lexer import Lexer
from src.token_type import TokenType


def test_build():
    source = io.StringIO("* == <= ! >")
    lexer = Lexer(source)

    assert lexer.get_next_token().get_type() == TokenType.MUL_OPERATOR
    assert lexer.get_next_token().get_type() == TokenType.EQ_OPERATOR
    assert lexer.get_next_token().get_type() == TokenType.LEQ_OPERATOR
    assert lexer.get_next_token().get_type() == TokenType.LOGIC_NEG_OPERATOR
    assert lexer.get_next_token().get_type() == TokenType.GREATER_OPERATOR
