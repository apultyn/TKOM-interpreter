from dataclasses import dataclass

@dataclass
class PyscriptException(Exception):
    error_type: str
    message: str
    position: tuple[int, int]

    def __str__(self):
        return f"{self.error_type} ERROR - line {self.position[0]}, col {self.position[1]} - {self.message}"


class LengthException(PyscriptException):
    def __init__(self, *args):
        super().__init__("LENGTH", *args)


class UnclosedException(PyscriptException):
    def __init__(self, *args):
        super().__init__("UNCLOSED", *args)


class InvalidValueException(PyscriptException):
    def __init__(self, *args):
        super().__init__("INVALID VALUE", *args)


class NewLineException(PyscriptException):
    def __init__(self, *args):
        super().__init__("NEWLINE", *args)


class TokenException(PyscriptException):
    def __init__(self, *args):
        super().__init__("TOKEN", *args)


class SyntaxException(PyscriptException):
    def __init__(self, *args):
        super().__init__("SYNTAX", *args)
