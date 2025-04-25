from enum import Enum, auto


class Node:
    def accept(self, visitor):
        return visitor.visit(self)


class AssignmentType(Enum):
    NORMAL = auto()
    PLUS = auto()
    MINUS = auto()


class BinaryOperation(Enum):
    OR = auto()
    AND = auto()
    EQ = auto()
    NEQ = auto()
    GT = auto()
    GEQ = auto()
    LT = auto()
    LEQ = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()


class SimpleLiteralType(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()


class NegationType(Enum):
    LOGIC = auto()
    ARITH = auto()
