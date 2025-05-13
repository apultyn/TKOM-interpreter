from typing import Optional, Type

from src.util.token_type import TokenType
from src.util.my_token import Token
from src.parser.parser_objects import (
    OrExpr,
    AndExpr,
    EqExpr,
    NeqExpr,
    GtExpr,
    GeqExpr,
    LtExpr,
    LeqExpr,
    AddExpr,
    SubExpr,
    MulExpr,
    DivExpr,
    BinaryExpr,
    LogicNegExpr,
    ArithNegExpr,
    NegationExpr,
    SimpleExpr,
    IntExpr,
    FloatExpr,
    BoolExpr,
    StringExpr,
    Identifier,
)


def match_binary_operation(token_type: TokenType) -> Optional[Type[BinaryExpr]]:
    mapping = {
        TokenType.OR_OPERATOR: OrExpr,
        TokenType.AND_OPERATOR: AndExpr,
        TokenType.EQ_OPERATOR: EqExpr,
        TokenType.NEQ_OPERATOR: NeqExpr,
        TokenType.GT_OPERATOR: GtExpr,
        TokenType.GEQ_OPERATOR: GeqExpr,
        TokenType.LT_OPERATOR: LtExpr,
        TokenType.LEQ_OPERATOR: LeqExpr,
        TokenType.PLUS_OPERATOR: AddExpr,
        TokenType.MINUS_OPERATOR: SubExpr,
        TokenType.MUL_OPERATOR: MulExpr,
        TokenType.DIV_OPERATOR: DivExpr,
    }
    return mapping.get(token_type, None)


def match_negation_type(token_type: TokenType) -> Optional[Type[NegationExpr]]:
    mapping = {
        TokenType.MINUS_OPERATOR: ArithNegExpr,
        TokenType.LOGIC_NEG_OPERATOR: LogicNegExpr,
    }
    return mapping.get(token_type, None)


def match_simple_expr(token: Token) -> Optional[SimpleExpr]:
    mapping = {
        TokenType.INT_LITERAL: IntExpr(token.value, pos=token.pos),
        TokenType.FLOAT_LITERAL: FloatExpr(token.value, pos=token.pos),
        TokenType.STRING_LITERAL: StringExpr(token.value, pos=token.pos),
        TokenType.TRUE_LITERAL: BoolExpr(True, pos=token.pos),
        TokenType.FALSE_LITERAL: BoolExpr(False, pos=token.pos),
        TokenType.IDENTIFIER: Identifier(token.value, pos=token.pos),
    }
    return mapping.get(token.type, None)
