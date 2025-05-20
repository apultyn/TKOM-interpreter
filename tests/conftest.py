import pytest
import io
from unittest.mock import MagicMock
from copy import deepcopy

from src.util.error_handler import ErrorHandler
from src.util.configs import LexerConfig
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter, GLOBAL_ENV
from src.interpreter.interpreter_objects import Value
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


@pytest.fixture
def make_env():
    def _factory():
        return deepcopy(GLOBAL_ENV)

    return _factory


@pytest.fixture
def make_interpreter(mocked_error_handler, make_env) -> Interpreter:
    def _factory(*, env: list[tuple[str, Value]] = [], err=mocked_error_handler):
        interpreter = Interpreter(error_handler=err, env=make_env())

        for name, value in env:
            interpreter.global_env.define(name, value)
        return interpreter

    return _factory
