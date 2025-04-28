import pytest

from src.parser.parser_objects import (
    AssignmentStmt,
    Identifier,
    SimpleTypeExpr,
    CallExpr,
    IfStmt,
    BinaryExpr,
    Block,
    ElifStmt,
    WhileStmt,
    ForStmt,
    AccessExpr,
    FunctionExpr,
    ReturnStmt,
    LinqExpr,
)
from src.parser.parser_util import (
    AssignmentType,
    SimpleLiteralType,
    BinaryOperationType,
)


@pytest.mark.parametrize(
    "src, assignment_type",
    [
        ("a = 10;", AssignmentType.NORMAL),
        ("a += 10;", AssignmentType.PLUS),
        ("a -= 10;", AssignmentType.MINUS),
    ],
)
def test_assigmnents(make_parser, src, assignment_type):
    statement = make_parser(src).parse_program().statements[0]
    assert statement == AssignmentStmt(
        l_value=Identifier("a"),
        assign_type=assignment_type,
        r_value=SimpleTypeExpr(SimpleLiteralType.INT, 10),
    )


def test_call_statement(make_parser):
    src = "b();"
    statement = make_parser(src).parse_program().statements[0]
    assert statement == CallExpr(callee=Identifier("b"), args=[])


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

    assert statement == IfStmt(
        condition=BinaryExpr(
            l_value=Identifier("a"),
            operation=BinaryOperationType.LT,
            r_value=SimpleTypeExpr(SimpleLiteralType.INT, 4),
        ),
        body=Block([CallExpr(Identifier("do_something"), [])]),
        elif_statements=[
            ElifStmt(
                condition=BinaryExpr(
                    Identifier("a"),
                    BinaryOperationType.GT,
                    SimpleTypeExpr(SimpleLiteralType.INT, 4),
                ),
                body=Block([CallExpr(Identifier("do_something_else"), [])]),
            )
        ],
        else_body=Block([CallExpr(Identifier("do_something_differently"), [])]),
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
    assert statement == WhileStmt(
        condition=BinaryExpr(
            Identifier("a"),
            BinaryOperationType.LT,
            SimpleTypeExpr(SimpleLiteralType.INT, 10),
        ),
        body=Block(
            [
                CallExpr(Identifier("do_something_ten_times"), []),
                AssignmentStmt(
                    Identifier("a"),
                    AssignmentType.PLUS,
                    SimpleTypeExpr(SimpleLiteralType.INT, 1),
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
    assert statement == ForStmt(
        var=Identifier("element"),
        source=Identifier("my_dict"),
        body=Block(
            [
                CallExpr(
                    callee=Identifier("print"),
                    args=[
                        CallExpr(
                            callee=AccessExpr(
                                source=Identifier("element"),
                                target=Identifier("key"),
                            ),
                            args=[],
                        )
                    ],
                ),
            ]
        ),
    )


def test_func_definition(make_parser):
    src = """
my_func = function(arg1, arg2) {
    return arg1 + arg2;
};
"""
    statement = make_parser(src).parse_program().statements[0]
    assert statement == AssignmentStmt(
        l_value=Identifier("my_func"),
        assign_type=AssignmentType.NORMAL,
        r_value=FunctionExpr(
            params=[Identifier("arg1"), Identifier("arg2")],
            body=Block(
                [
                    ReturnStmt(
                        BinaryExpr(
                            Identifier("arg1"),
                            BinaryOperationType.ADD,
                            Identifier("arg2"),
                        )
                    )
                ]
            ),
        ),
    )


def test_linq_query(make_parser):
    src = """
small_cities = from city in my_dict
    select city.key(), city.value() / 1000
    where city.value() < 5000000
    order by city.key() descending;

"""
    statement = make_parser(src).parse_program().statements[0]
    assert statement == AssignmentStmt(
        l_value=Identifier("small_cities"),
        assign_type=AssignmentType.NORMAL,
        r_value=LinqExpr(
            var=Identifier("city"),
            source=Identifier("my_dict"),
            selects=[
                CallExpr(
                    callee=AccessExpr(
                        source=Identifier("city"), target=Identifier("key")
                    ),
                    args=[],
                ),
                BinaryExpr(
                    l_value=CallExpr(
                        callee=AccessExpr(
                            source=Identifier("city"), target=Identifier("value")
                        ),
                        args=[],
                    ),
                    operation=BinaryOperationType.DIV,
                    r_value=SimpleTypeExpr(SimpleLiteralType.INT, 1000),
                ),
            ],
            where=BinaryExpr(
                l_value=CallExpr(
                    callee=AccessExpr(
                        source=Identifier("city"), target=Identifier("value")
                    ),
                    args=[],
                ),
                operation=BinaryOperationType.LT,
                r_value=SimpleTypeExpr(SimpleLiteralType.INT, 5000000),
            ),
            order_by=CallExpr(
                callee=AccessExpr(source=Identifier("city"), target=Identifier("key")),
                args=[],
            ),
            descending=True,
        ),
    )
