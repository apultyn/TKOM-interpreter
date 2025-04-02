from source import Source


class Lexer:
    def __init__(self, source):
        self._source = Source(source)
        self._char = None
        self._col = 1
        self._line = 1
