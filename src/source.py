class Source:
    def __init__(self, source):
        self._source = source
        self._char = None
        self._col = 0
        self._row = 1
        self._EOF_found = False
        self._new_line_found = False

    def get_next_char(self):
        char = self._source.read(1)
        self._col += 1

        if self._new_line_found:
            self._col = 1
            self._row += 1
            self._new_line_found = False

        if char == "\r":
            next_char = self._source.read(1)
            if next_char != "\n":
                self._source.seek(self._source.tell() - 1)
            char = "\n"

        if char == "\n":
            self._new_line_found = True

        elif not char:
            char = "EOF"
            if not self._EOF_found:
                self._EOF_found = True
            else:
                self._col -= 1

        self._char = char
        return char

    def get_char(self):
        return self._char

    def get_pos(self):
        return (self._row, self._col)
