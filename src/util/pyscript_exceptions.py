import inspect
from dataclasses import dataclass

from src.util.token_type import TokenType
from src.interpreter.interpreter_objects import Env
from src.parser.parser_objects import ParserObject


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
    def __init__(self, pos: tuple[int, int], obj_expected: str, obj_got: str = None):
        msg = f"{obj_expected} expected"
        if obj_got:
            msg += f", got '{obj_got}'"
        super().__init__(error_type="SYNTAX", msg=msg.capitalize(), pos=pos)


class WrongTokenException(SyntaxException):
    def __init__(
        self,
        pos,
        token_expected: TokenType | list[TokenType],
        token_got: TokenType = None,
    ):
        if isinstance(token_expected, list):
            obj = " or ".join(token_expected)
        else:
            obj = str(token_expected)
        super().__init__(pos, obj, str(token_got) if token_got else None)


class WrongParserObjectException(SyntaxException):
    def __init__(
        self,
        pos,
        par_obj_expected: ParserObject | list[ParserObject],
        par_obj_got: ParserObject = None,
    ):

        def get_obj_name(obj):
            if inspect.isclass(obj):
                return getattr(obj, "class_display_name", obj.__name__)
            return str(obj)

        if isinstance(par_obj_expected, list):
            obj_str = " or ".join([get_obj_name(o) for o in par_obj_expected])
        else:
            obj_str = get_obj_name(par_obj_expected)

        got_str = get_obj_name(par_obj_got) if par_obj_got else None

        super().__init__(pos, obj_str, got_str)


class RuntimeException(PyscriptException):
    def __init__(self, msg: str, env: Env = None, pos: tuple[int, int] = None):
        self.env = env
        super().__init__(error_type="RUNTIME", msg=msg, pos=pos)

    def __str__(self):
        return super().__str__()

    def context(self):
        return str(self.env)
