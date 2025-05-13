from src.util.token_type import TokenType

from src.parser.parser_objects import Identifier, SimpleExpr, IntExpr


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


def check_error(mocked_error_handler, exception, position, *, msg=None):
    mocked_error_handler.handle_error.assert_called_once()
    exc = mocked_error_handler.handle_error.call_args.args[0]
    assert isinstance(exc, exception)
    assert exc.pos == position
    if msg:
        assert exc.msg == msg


def ident(name, pos):
    return Identifier(name, pos=pos)


def integer(value, pos):
    return IntExpr(value, pos=pos)
