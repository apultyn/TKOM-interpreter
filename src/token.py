from token_type import TokenType


class Token:
    def __init__(self, type: TokenType, position: tuple[int, int], val=None):
        self._type = type
        self._position = position
        self._val = val

    def __repr__(self):
        return f"Token({self._type}, {self._position}, {self._val})"
