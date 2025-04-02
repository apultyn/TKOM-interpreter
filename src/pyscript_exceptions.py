class LexerException(Exception):
    def __init__(self, message, position):
        self._message = message
        self._position = position

    def __str__(self):
        return f"LEXER ERROR - line {self._position[0]}, col {self._position[1]} - {self._message}"
