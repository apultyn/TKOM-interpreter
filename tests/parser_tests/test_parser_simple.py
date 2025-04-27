import pytest

import src.parser.parser_objects as po
import src.parser.parser_util as pu


@pytest.mark.parametrize(
    "src, assignment_type",
    [
        ("a = 10;", pu.AssignmentType.NORMAL),
        ("a += 10;", pu.AssignmentType.PLUS),
        ("a -= 10;", pu.AssignmentType.MINUS),
    ],
)
def test_assigmnents(make_parser, src, assignment_type):
    statement = make_parser(src).parse_program().statements[0]
    assert statement == po.AssignmentStmt(
        po.Identifier("a"),
        assignment_type,
        po.SimpleTypeExpr(pu.SimpleLiteralType.INT, 10),
    )


def test_call_statement(make_parser):
    src = "b();"
    statement = make_parser(src).parse_program().statements[0]
    assert statement == po.CallExpr(
        po.Identifier("b"), [{None}]
    )