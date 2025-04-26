import pytest
from unittest.mock import MagicMock

from src.util.error_handler import ErrorHandler
from .util import AbortExecution

@pytest.fixture
def mocked_error_handler():
    mock = MagicMock(spec=ErrorHandler)
    mock.handle_error.side_effect = AbortExecution()
    return mock