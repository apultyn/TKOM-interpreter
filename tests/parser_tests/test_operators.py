import pytest

from src.parser.parser_objects import (
    Identifier,
    BinaryExpr,
    NegationExpr,
    CallExpr,
    AccessExpr,
)
from src.parser.parser_util import BinaryOperationType, NegationType

from tests.util import ident, integer


@pytest.mark.parametrize(
    "operator_text, operator_type_object",
    [
        ("*", BinaryOperationType.MUL),
        ("/", BinaryOperationType.DIV),
        ("+", BinaryOperationType.ADD),
        ("-", BinaryOperationType.SUB),
        (">", BinaryOperationType.GT),
        (">=", BinaryOperationType.GEQ),
        ("<", BinaryOperationType.LT),
        ("<=", BinaryOperationType.LEQ),
        ("==", BinaryOperationType.EQ),
        ("!=", BinaryOperationType.NEQ),
        ("and", BinaryOperationType.AND),
        ("or", BinaryOperationType.OR),
    ],
)
def test_binary_operators(make_parser, operator_text, operator_type_object):
    src = f"a = b {operator_text} c;"
    expression = make_parser(src).parse_program().statements[0].r_value
    assert expression == BinaryExpr(
        l_value=Identifier("b", pos=(1, 5)),
        operation=operator_type_object,
        r_value=Identifier("c", pos=(1, 8 + len(operator_text))),
        pos=(1, 7),
    )


def test_and_over_or(make_parser):
    src = "a = 1 or 5 and 10;"
    expression = make_parser(src).parse_program().statements[0].r_value
    assert expression == BinaryExpr(
        l_value=integer(1, (1, 5)),
        operation=BinaryOperationType.OR,
        r_value=BinaryExpr(
            l_value=integer(5, (1, 10)),
            operation=BinaryOperationType.AND,
            r_value=integer(10, (1, 16)),
            pos=(1, 12),
        ),
        pos=(1, 7),
    )


def test_comp_over_and(make_parser):
    src = "a = 5 and 2 != 3;"
    expr = make_parser(src).parse_program().statements[0].r_value

    assert expr == BinaryExpr(
        l_value=integer(5, (1, 5)),
        operation=BinaryOperationType.AND,
        r_value=BinaryExpr(
            l_value=integer(2, (1, 11)),
            operation=BinaryOperationType.NEQ,
            r_value=integer(3, (1, 16)),
            pos=(1, 13),
        ),
        pos=(1, 7),
    )


def test_comparison_equal(make_parser):
    src = "a = 1 <= 2 < 3 >= 4 > 5 != 6 == 7;"
    expr = make_parser(src).parse_program().statements[0].r_value
    assert expr == BinaryExpr(
        l_value=BinaryExpr(
            l_value=BinaryExpr(
                l_value=BinaryExpr(
                    l_value=BinaryExpr(
                        l_value=BinaryExpr(
                            l_value=integer(1, (1, 5)),
                            operation=BinaryOperationType.LEQ,
                            r_value=integer(2, (1, 10)),
                            pos=(1, 7),
                        ),
                        operation=BinaryOperationType.LT,
                        r_value=integer(3, (1, 14)),
                        pos=(1, 12),
                    ),
                    operation=BinaryOperationType.GEQ,
                    r_value=integer(4, (1, 19)),
                    pos=(1, 16),
                ),
                operation=BinaryOperationType.GT,
                r_value=integer(5, (1, 23)),
                pos=(1, 21),
            ),
            operation=BinaryOperationType.NEQ,
            r_value=integer(6, (1, 28)),
            pos=(1, 25),
        ),
        operation=BinaryOperationType.EQ,
        r_value=integer(7, (1, 33)),
        pos=(1, 30),
    )


def test_addv_over_comp(make_parser):
    src = "a = 5 > 2 + 2;"
    expr = make_parser(src).parse_program().statements[0].r_value

    assert expr == BinaryExpr(
        l_value=integer(5, (1, 5)),
        operation=BinaryOperationType.GT,
        r_value=BinaryExpr(
            l_value=integer(2, (1, 9)),
            operation=BinaryOperationType.ADD,
            r_value=integer(2, (1, 13)),
            pos=(1, 11),
        ),
        pos=(1, 7),
    )


def test_mul_over_addv(make_parser):
    src = "a = 5 + 2 / 2;"
    expr = make_parser(src).parse_program().statements[0].r_value

    assert expr == BinaryExpr(
        l_value=integer(5, (1, 5)),
        operation=BinaryOperationType.ADD,
        r_value=BinaryExpr(
            l_value=integer(2, (1, 9)),
            operation=BinaryOperationType.DIV,
            r_value=integer(2, (1, 13)),
            pos=(1, 11),
        ),
        pos=(1, 7),
    )


def test_unary_over_mul(make_parser):
    src = "a = 10 * -5;"
    expr = make_parser(src).parse_program().statements[0].r_value

    assert expr == BinaryExpr(
        l_value=integer(10, (1, 5)),
        operation=BinaryOperationType.MUL,
        r_value=NegationExpr(
            neg_type=NegationType.ARITH, value=integer(5, (1, 11)), pos=(1, 10)
        ),
        pos=(1, 8),
    )


def test_postfix_over_unary(make_parser):
    src = """
a = -calc();
b = !obj.field;
"""
    statements = make_parser(src).parse_program().statements
    expr1 = statements[0].r_value
    expr2 = statements[1].r_value

    assert expr1 == NegationExpr(
        neg_type=NegationType.ARITH,
        value=CallExpr(callee=ident("calc", (2, 6)), args=[], pos=(2, 10)),
        pos=(2, 5),
    )

    assert expr2 == NegationExpr(
        neg_type=NegationType.LOGIC,
        value=AccessExpr(
            source=ident("obj", (3, 6)), target=ident("field", (3, 10)), pos=(3, 9)
        ),
        pos=(3, 5),
    )


def test_unary_sequence(make_parser):
    src = "a = -!-!a;"
    expr = make_parser(src).parse_program().statements[0].r_value

    assert expr == NegationExpr(
        neg_type=NegationType.ARITH,
        value=NegationExpr(
            neg_type=NegationType.LOGIC,
            value=NegationExpr(
                neg_type=NegationType.ARITH,
                value=NegationExpr(
                    neg_type=NegationType.LOGIC, value=ident("a", (1, 9)), pos=(1, 8)
                ),
                pos=(1, 7),
            ),
            pos=(1, 6),
        ),
        pos=(1, 5),
    )
