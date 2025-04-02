from .token_type import TokenType


class Token:
    def __init__(self, type: TokenType, pos: tuple[int, int], val=None):
        self._type = type
        self._pos = pos
        self._val = val

    def __repr__(self):
        return f"Token({self._type}, {self._pos}, {self._val})"

    def get_type(self):
        return self._type

    def get_pos(self):
        return self._pos

    def get_val(self):
        return self._val
