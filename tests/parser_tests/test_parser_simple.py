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
    assert statement == po.CallExpr(po.Identifier("b"), [{None}])


def test_if_statement(make_parser):
    src = """
if (a < 4) {
    do_something();
} elif (a > 4) {
    do_something_else();
} else {
    do_something_differently();
}
"""
    statement = make_parser(src).parse_program().statements[0]

    assert statement == po.IfStmt(
        condition=po.BinaryExpr(
            po.Identifier("a"),
            pu.BinaryOperation.LT,
            po.SimpleTypeExpr(pu.SimpleLiteralType.INT, 4),
        ),
        body=po.Block([po.CallExpr(po.Identifier("do_something"), [{None}])]),
        elif_statements=[
            po.ElifStmt(
                condition=po.BinaryExpr(
                    po.Identifier("a"),
                    pu.BinaryOperation.GT,
                    po.SimpleTypeExpr(pu.SimpleLiteralType.INT, 4),
                ),
                body=po.Block(
                    [po.CallExpr(po.Identifier("do_something_else"), [{None}])]
                ),
            )
        ],
        else_body=po.Block(
            [po.CallExpr(po.Identifier("do_something_differently"), [{None}])]
        ),
    )


def test_while_loop(make_parser):
    src = """
a = 0;
while (a < 10) {
    do_something_ten_times();
    a += 1;
}

"""
    statement = make_parser(src).parse_program().statements[1]
    assert statement == po.WhileStmt(
        condition=po.BinaryExpr(
            po.Identifier("a"),
            pu.BinaryOperation.LT,
            po.SimpleTypeExpr(pu.SimpleLiteralType.INT, 10),
        ),
        body=po.Block(
            [
                po.CallExpr(po.Identifier("do_something_ten_times"), [{None}]),
                po.AssignmentStmt(
                    po.Identifier("a"),
                    pu.AssignmentType.PLUS,
                    po.SimpleTypeExpr(pu.SimpleLiteralType.INT, 1),
                ),
            ]
        ),
    )


def test_for_loop(make_parser):
    src = """
for element in my_dict {
    print(element.key()); // "first" "second"
}
"""
    statement = make_parser(src).parse_program().statements[0]
    assert statement == po.ForStmt(
        var=po.Identifier("element"),
        source=po.Identifier("my_dict"),
        body=po.Block(
            [
                po.CallExpr(
                    callee=po.Identifier("print"),
                    args=[
                        po.CallExpr(
                            callee=po.AccessExpr(
                                source=po.Identifier("element"),
                                target=po.Identifier("key"),
                            ),
                            args=[{None}],
                        )
                    ],
                ),
            ]
        ),
    )
