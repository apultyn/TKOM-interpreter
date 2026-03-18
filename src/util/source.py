from .pyscript_exceptions import NewLineException


class Source:
    def __init__(self, source):
        self._source = source
        self._char = None
        self._pushback = None
        self._col = 0
        self._row = 1
        self._EOF_found = False
        self._new_line_found = False
        self._new_line_type = None

    def get_next_char(self):
        if self._pushback is not None:
            char = self._pushback
            self._pushback = None
        else:
            char = self._source.read(1)
        self._col += 1

        if not char:
            if not self._EOF_found:
                self._EOF_found = True
                self._char = "EOF"
            else:
                self._col -= 1
            return "EOF"

        if self._new_line_found:
            self._col = 1
            self._row += 1
            self._new_line_found = False

        if char == "\n":
            if self._new_line_type is None:
                self._new_line_type = "unix"
            elif self._new_line_type != "unix":
                raise NewLineException(
                    found_type="unix",
                    expected_type="windows",
                    pos=(self._row, self._col),
                )
            self._new_line_found = True
            self._char = "\n"
            return "\n"

        if char == "\r":
            next_char = self._source.read(1)
            if next_char == "\n":
                if self._new_line_type is None:
                    self._new_line_type = "windows"
                elif self._new_line_type != "windows":
                    raise NewLineException(
                        found_type="windows",
                        expected_type="unix",
                        pos=(self._row, self._col),
                    )
                self._new_line_found = True
                self._char = "\n"
                return "\n"
            else:
                if next_char:
                    self._pushback = next_char

        self._char = char
        return char

    def get_char(self):
        return self._char

    def get_pos(self):
        return (self._row, self._col)
