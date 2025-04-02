class Token:
    def __init__(self, type, pos, val=None):
        self._type = type
        self._pos = pos
        self._val = val
