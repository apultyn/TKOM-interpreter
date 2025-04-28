import pytest

from src.parser.parser_objects import Identifier, BinaryExpr
from src.parser.parser_util import BinaryOperationType

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


def test_neq_over_and(make_parser):
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
