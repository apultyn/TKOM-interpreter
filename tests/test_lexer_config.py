import pytest

from src.lexer_config import LexerConfig


def test_default():
    config = LexerConfig()
    assert config.max_comment_length == 10000
    assert config.max_identifier_length == 1000
    assert config.max_string_literal_length == 10000


def test_some_custom():
    config = LexerConfig(max_string_literal_length=5)
    assert config.max_comment_length == 10000
    assert config.max_identifier_length == 1000
    assert config.max_string_literal_length == 5


def test_too_short_identifier():
    with pytest.raises(ValueError):
        LexerConfig(max_identifier_length=9)


def test_too_short_identifier():
    with pytest.raises(ValueError):
        LexerConfig(max_identifier_length=9)
