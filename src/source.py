class Source:
    def __init__(self, source):
        self._source = source
        self._char = 'EOF'
        self._col = 1
        self._row = 1

    def get_next_char(self):
        char = self._source.read(1)

        if char == '\r':
            next_char = self._source.read(1)
            if next_char != 'n':
                self._source.seek(self._source.tell() - 1)
            char = '\n'

        if char == '\n':
            self._col = 1
            self._row += 1

        elif not char:
            char = 'EOF'

        else:
            self._col += 1

        self._char = char
        return char
