from dataclasses import dataclass

from src.util.token_type import TokenType
from src.interpreter.interpreter_objects import Env


@dataclass(kw_only=True)
class PyscriptException(Exception):
    error_type: str
    msg: str
    pos: tuple[int, int]

    def __str__(self):
        return f"{self.error_type} ERROR - line {self.pos[0]}, col {self.pos[1]} - {self.msg}"


class LengthException(PyscriptException):
    def __init__(self, kind: str, max_length: int, pos: tuple[int, int]):
        self.kind = kind
        self.max_length = max_length
        super().__init__(
            error_type="LENGTH",
            msg=f"Maximum {kind} length ({max_length}) exceeded",
            pos=pos,
        )


class UnclosedException(PyscriptException):
    def __init__(self, construct: str, pos: tuple[int, int]):
        self.construct = construct
        super().__init__(
            error_type="UNCLOSED",
            msg=f"{construct} not closed",
            pos=pos,
        )


class InvalidValueException(PyscriptException):
    def __init__(self, msg: str, pos: tuple[int, int]):
        super().__init__(error_type="INVALID VALUE", msg=msg, pos=pos)


class NewLineException(PyscriptException):
    def __init__(self, found_type: str, expected_type: str, pos: tuple[int, int]):
        self.found_type = found_type
        self.expected_type = expected_type
        super().__init__(
            error_type="NEWLINE",
            msg=f"Mixed newline types: expected {expected_type}, found {found_type}",
            pos=pos,
        )


class TokenException(PyscriptException):
    def __init__(self, char: str, pos: tuple[int, int]):
        self.char = char
        super().__init__(error_type="TOKEN", msg=f"Unknown token '{char}'", pos=pos)


class SyntaxException(PyscriptException):
    def __init__(
        self,
        msg: str,
        pos: tuple[int, int],
        token_expected: TokenType = None,
        token_got: TokenType = None,
    ):
        self.token_expected = token_expected
        self.token_got = token_got
        if token_got:
            msg = f"{msg}, got '{token_got}'"
        super().__init__(error_type="SYNTAX", msg=msg, pos=pos)


class RuntimeException(PyscriptException):
    def __init__(self, msg: str, env: Env = None, pos: tuple[int, int] = None):
        self.env = env
        super().__init__(error_type="RUNTIME", msg=msg, pos=pos)

    def __str__(self):
        return super().__str__()

    def context(self):
        return str(self.env)
