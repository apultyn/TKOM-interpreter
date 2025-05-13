import pytest

from src.parser.parser_objects import (
    Identifier,
    CallExpr,
    AccessExpr,
    BracketsExpr,
    MulExpr,
    DivExpr,
    AddExpr,
    SubExpr,
    GtExpr,
    GeqExpr,
    LtExpr,
    LeqExpr,
    EqExpr,
    NeqExpr,
    AndExpr,
    OrExpr,
    IntExpr,
    ArithNegExpr,
    LogicNegExpr,
)


@pytest.mark.parametrize(
    "operator_text, OperatorClass",
    [
        ("*", MulExpr),
        ("/", DivExpr),
        ("+", AddExpr),
        ("-", SubExpr),
        (">", GtExpr),
        (">=", GeqExpr),
        ("<", LtExpr),
        ("<=", LeqExpr),
        ("==", EqExpr),
        ("!=", NeqExpr),
        ("and", AndExpr),
        ("or", OrExpr),
    ],
)
def test_binary_operators(make_parser, operator_text, OperatorClass):
    src = f"a = b {operator_text} c;"
    expression = make_parser(src).parse_program().statements[0].r_value
    assert expression == OperatorClass(
        l_value=Identifier("b", pos=(1, 5)),
        r_value=Identifier("c", pos=(1, 8 + len(operator_text))),
        pos=(1, 7),
    )


def test_and_over_or(make_parser):
    src = "a = 1 or 5 and 10;"
    expression = make_parser(src).parse_program().statements[0].r_value
    assert expression == OrExpr(
        l_value=IntExpr(1, pos=(1, 5)),
        r_value=AndExpr(
            l_value=IntExpr(5, pos=(1, 10)),
            r_value=IntExpr(10, pos=(1, 16)),
            pos=(1, 12),
        ),
        pos=(1, 7),
    )


def test_comp_over_and(make_parser):
    src = "a = 5 and 2 != 3;"
    expr = make_parser(src).parse_program().statements[0].r_value

    assert expr == AndExpr(
        l_value=IntExpr(5, pos=(1, 5)),
        r_value=NeqExpr(
            l_value=IntExpr(2, pos=(1, 11)),
            r_value=IntExpr(3, pos=(1, 16)),
            pos=(1, 13),
        ),
        pos=(1, 7),
    )


def test_comparison_equal(make_parser):
    src = "a = 1 <= 2 < 3 >= 4 > 5 != 6 == 7;"
    expr = make_parser(src).parse_program().statements[0].r_value
    assert expr == EqExpr(
        l_value=NeqExpr(
            l_value=GtExpr(
                l_value=GeqExpr(
                    l_value=LtExpr(
                        l_value=LeqExpr(
                            l_value=IntExpr(1, pos=(1, 5)),
                            r_value=IntExpr(2, pos=(1, 10)),
                            pos=(1, 7),
                        ),
                        r_value=IntExpr(3, pos=(1, 14)),
                        pos=(1, 12),
                    ),
                    r_value=IntExpr(4, pos=(1, 19)),
                    pos=(1, 16),
                ),
                r_value=IntExpr(5, pos=(1, 23)),
                pos=(1, 21),
            ),
            r_value=IntExpr(6, pos=(1, 28)),
            pos=(1, 25),
        ),
        r_value=IntExpr(7, pos=(1, 33)),
        pos=(1, 30),
    )


def test_addv_over_comp(make_parser):
    src = "a = 5 > 2 + 2;"
    expr = make_parser(src).parse_program().statements[0].r_value

    assert expr == GtExpr(
        l_value=IntExpr(5, pos=(1, 5)),
        r_value=AddExpr(
            l_value=IntExpr(2, pos=(1, 9)),
            r_value=IntExpr(2, pos=(1, 13)),
            pos=(1, 11),
        ),
        pos=(1, 7),
    )


def test_mul_over_addv(make_parser):
    src = "a = 5 + 2 / 2;"
    expr = make_parser(src).parse_program().statements[0].r_value

    assert expr == AddExpr(
        l_value=IntExpr(5, pos=(1, 5)),
        r_value=DivExpr(
            l_value=IntExpr(2, pos=(1, 9)),
            r_value=IntExpr(2, pos=(1, 13)),
            pos=(1, 11),
        ),
        pos=(1, 7),
    )


def test_unary_over_mul(make_parser):
    src = "a = 10 * -5;"
    expr = make_parser(src).parse_program().statements[0].r_value

    assert expr == MulExpr(
        l_value=IntExpr(10, pos=(1, 5)),
        r_value=ArithNegExpr(value=IntExpr(5, pos=(1, 11)), pos=(1, 10)),
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

    assert expr1 == ArithNegExpr(
        value=CallExpr(callee=Identifier("calc", (2, 6)), args=[], pos=(2, 10)),
        pos=(2, 5),
    )

    assert expr2 == LogicNegExpr(
        value=AccessExpr(
            source=Identifier("obj", pos=(3, 6)),
            target=Identifier("field", pos=(3, 10)),
            pos=(3, 9),
        ),
        pos=(3, 5),
    )


def test_parenthesis_over_postifx(make_parser):
    src = "a = (2 + 2)(arg1);"
    expr = make_parser(src).parse_program().statements[0].r_value

    assert expr == CallExpr(
        callee=BracketsExpr(
            value=AddExpr(
                l_value=IntExpr(2, pos=(1, 6)),
                r_value=IntExpr(2, pos=(1, 10)),
                pos=(1, 8),
            ),
            pos=(1, 5),
        ),
        args=[Identifier("arg1", (1, 13))],
        pos=(1, 12),
    )


def test_unary_sequence(make_parser):
    src = "a = -!-!a;"
    expr = make_parser(src).parse_program().statements[0].r_value

    assert expr == ArithNegExpr(
        value=LogicNegExpr(
            value=ArithNegExpr(
                value=LogicNegExpr(value=Identifier("a", pos=(1, 9)), pos=(1, 8)),
                pos=(1, 7),
            ),
            pos=(1, 6),
        ),
        pos=(1, 5),
    )
