from dataclasses import dataclass
from typing import Optional, Any

from .token_type import TokenType


@dataclass
class Token:
    type: TokenType
    pos: tuple[int, int]
    value: Optional[Any] = None

    def __repr__(self):
        return f"Token({self.type}, {self.pos}, {self.value})"

    def __eq__(self, other):
        return (
            self.type == other.type
            and self.pos == other.pos
            and self.value == other.value
        )
