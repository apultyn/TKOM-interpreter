import pytest
import io
from unittest.mock import MagicMock

from src.util.error_handler import ErrorHandler
from src.util.configs import LexerConfig
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from .util import AbortExecution


@pytest.fixture
def mocked_error_handler():
    mock = MagicMock(spec=ErrorHandler)
    mock.handle_error.side_effect = AbortExecution()
    return mock


@pytest.fixture
def make_lexer(mocked_error_handler):
    def _factory(
        text: str, *, config: LexerConfig | None = None, err=mocked_error_handler
    ):
        source = io.StringIO(text)
        return (
            Lexer(source=source, error_handler=mocked_error_handler, config=config)
            if config
            else Lexer(source=source, error_handler=err)
        )

    return _factory


@pytest.fixture
def make_parser(make_lexer, mocked_error_handler):
    def _factory(text: str, *, err=mocked_error_handler):
        lexer = make_lexer(text, err=err)
        return Parser(lexer=lexer, error_handler=err)

    return _factory
