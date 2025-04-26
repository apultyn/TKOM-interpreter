from enum import Enum, auto
from src.util.token_type import TokenType


class Node:
    def accept(self, visitor):
        return visitor.visit(self)


class AssignmentType(Enum):
    NORMAL = auto()
    PLUS = auto()
    MINUS = auto()


def match_assignment_type(token_type: TokenType):
    mapping = {
        TokenType.ASSIGN_OPERATOR: AssignmentType.NORMAL,
        TokenType.ASSIGN_PLUS_OPERATOR: AssignmentType.PLUS,
        TokenType.ASSIGN_MINUS_OPERATOR: AssignmentType.MINUS,
    }

    return mapping.get(token_type, None)


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


def match_binary_operation(token_type: TokenType):
    mapping = {
        TokenType.OR_OPERATOR: BinaryOperation.OR,
        TokenType.AND_OPERATOR: BinaryOperation.AND,
        TokenType.EQ_OPERATOR: BinaryOperation.EQ,
        TokenType.NEQ_OPERATOR: BinaryOperation.NEQ,
        TokenType.GT_OPERATOR: BinaryOperation.GT,
        TokenType.GEQ_OPERATOR: BinaryOperation.GEQ,
        TokenType.LT_OPERATOR: BinaryOperation.LT,
        TokenType.LEQ_OPERATOR: BinaryOperation.LEQ,
        TokenType.PLUS_OPERATOR: BinaryOperation.ADD,
        TokenType.MINUS_OPERATOR: BinaryOperation.SUB,
        TokenType.MUL_OPERATOR: BinaryOperation.MUL,
        TokenType.DIV_OPERATOR: BinaryOperation.DIV,
    }
    return mapping.get(token_type, None)


class SimpleLiteralType(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()


class NegationType(Enum):
    LOGIC = auto()
    ARITH = auto()


def match_negation_type(token_type: TokenType):
    mapping = {
        TokenType.MINUS_OPERATOR: NegationType.ARITH,
        TokenType.LOGIC_NEG_OPERATOR: NegationType.LOGIC,
    }
    return mapping.get(token_type, None)
