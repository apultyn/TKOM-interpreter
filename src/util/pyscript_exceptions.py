from dataclasses import dataclass

from src.util.token_type import TokenType


@dataclass(kw_only=True)
class PyscriptException(Exception):
    error_type: str
    msg: str
    pos: tuple[int, int]

    def __str__(self):
        return f"{self.error_type} ERROR - line {self.pos[0]}, col {self.pos[1]} - {self.msg}"


class LengthException(PyscriptException):
    def __init__(self, msg: str, pos: tuple[int, int]):
        super().__init__(error_type="LENGTH", msg=msg, pos=pos)


class UnclosedException(PyscriptException):
    def __init__(self, msg: str, pos: tuple[int, int]):
        super().__init__(error_type="UNCLOSED", msg=msg, pos=pos)


class InvalidValueException(PyscriptException):
    def __init__(self, msg: str, pos: tuple[int, int]):
        super().__init__(error_type="INVALID VALUE", msg=msg, pos=pos)


class NewLineException(PyscriptException):
    def __init__(self, msg: str, pos: tuple[int, int]):
        super().__init__(error_type="NEWLINE", msg=msg, pos=pos)


class TokenException(PyscriptException):
    def __init__(self, msg: str, pos: tuple[int, int]):
        super().__init__(error_type="TOKEN", msg=msg, pos=pos)


class SyntaxException(PyscriptException):
    def __init__(self, msg: str, pos: tuple[int, int], token_got: TokenType = None):
        if token_got:
            msg = f"{msg}, got '{token_got}'"
        super().__init__(error_type="SYNTAX", msg=msg, pos=pos)


class RuntimeException(PyscriptException):
    def __init__(self, msg: str, pos: tuple[int, int]):
        super().__init__(error_type="RUNTIME", msg=msg, pos=pos)
