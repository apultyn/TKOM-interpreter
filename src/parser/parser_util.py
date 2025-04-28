from enum import Enum, auto
from src.util.token_type import TokenType
from dataclasses import dataclass


@dataclass(kw_only=True)
class ParserObject:
    pos: tuple[int, int]

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


class BinaryOperationType(Enum):
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
        TokenType.OR_OPERATOR: BinaryOperationType.OR,
        TokenType.AND_OPERATOR: BinaryOperationType.AND,
        TokenType.EQ_OPERATOR: BinaryOperationType.EQ,
        TokenType.NEQ_OPERATOR: BinaryOperationType.NEQ,
        TokenType.GT_OPERATOR: BinaryOperationType.GT,
        TokenType.GEQ_OPERATOR: BinaryOperationType.GEQ,
        TokenType.LT_OPERATOR: BinaryOperationType.LT,
        TokenType.LEQ_OPERATOR: BinaryOperationType.LEQ,
        TokenType.PLUS_OPERATOR: BinaryOperationType.ADD,
        TokenType.MINUS_OPERATOR: BinaryOperationType.SUB,
        TokenType.MUL_OPERATOR: BinaryOperationType.MUL,
        TokenType.DIV_OPERATOR: BinaryOperationType.DIV,
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
