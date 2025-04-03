class LexerException(Exception):
    def __init__(self, error_type, message, position):
        self._error_type = error_type
        self._message = message
        self._position = position

    def __str__(self):
        return f"{self._error_type} ERROR - line {self._position[0]}, col {self._position[1]} - {self._message}"


class LengthException(LexerException):
    def __init__(self, *args):
        super().__init__("LENGTH", *args)


class UnclosedException(LexerException):
    def __init__(self, *args):
        super().__init__("UNCLOSED", *args)
