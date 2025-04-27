from src.util.token_type import TokenType


def get_token_list(lexer):
    tokens = []
    token = lexer.get_next_token()

    while token.type != TokenType.EOF:
        tokens.append(token)
        token = lexer.get_next_token()

    tokens.append(token)
    return tokens


class AbortExecution(Exception):
    pass


def check_error_position(mocked_error_handler, exception, position):
    mocked_error_handler.handle_error.assert_called_once()
    exc = mocked_error_handler.handle_error.call_args.args[0]
    assert isinstance(exc, exception)
    assert exc.position == position
