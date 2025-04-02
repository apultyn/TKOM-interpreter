class Lexer:
    def __init__(self, source):
        self._source = source
        self._char = None
        self._col = 1
        self._line = 1

    def get_next_char(self):
        self._char = self._source.read(1)

    def parse_endline(self):
        pass

    def skip_whitechars(self):
        pass
