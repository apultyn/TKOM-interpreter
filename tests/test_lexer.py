import io

from src.lexer import Lexer


def test_get_next_char():
    source = io.StringIO("Hello World")
    lexer = Lexer(source)

    lexer.get_next_char()
    assert lexer._char == "H"
