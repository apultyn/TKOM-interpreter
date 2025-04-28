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
    ItemExpr,
    ListExpr
)
from src.parser.parser_util import (
    AssignmentType,
    SimpleLiteralType,
    BinaryOperationType,
)


@pytest.mark.parametrize(
    "src, assignment_type, col",
    [
        ("a = 10;", AssignmentType.NORMAL, 5),
        ("a += 10;", AssignmentType.PLUS, 6),
        ("a -= 10;", AssignmentType.MINUS, 6),
    ],
)
def test_assigmnents(make_parser, src, assignment_type, col):
    statement = make_parser(src).parse_program().statements[0]
    assert statement == AssignmentStmt(
        l_value=Identifier("a", pos=(1, 1)),
        assign_type=assignment_type,
        r_value=SimpleTypeExpr(SimpleLiteralType.INT, 10, pos=(1, col)),
        pos=(1, 3),
    )


@pytest.mark.parametrize(
    "ident_name, type, value, value_text",
    [
        ("a", SimpleLiteralType.INT, 125, 125),
        ("b", SimpleLiteralType.FLOAT, 0.25, 0.25),
        ("c", SimpleLiteralType.STRING, "Hello there", '"Hello there"'),
        ("d", SimpleLiteralType.BOOL, False, "False"),
        ("e", SimpleLiteralType.BOOL, True, "True"),
    ],
)
def test_simple_type_expressions(make_parser, ident_name, type, value, value_text):
    src = f"{ident_name} = {value_text};"
    statement = make_parser(src).parse_program().statements[0]
    assert statement == AssignmentStmt(
        l_value=Identifier(ident_name, pos=(1, 1)),
        assign_type=AssignmentType.NORMAL,
        r_value=SimpleTypeExpr(type, value, pos=(1, 5)),
        pos=(1, 3),
    )


def test_ident_as_expression(make_parser):
    src = "a = b;"
    statement = make_parser(src).parse_program().statements[0]
    assert statement == AssignmentStmt(
        l_value=Identifier("a", pos=(1, 1)),
        assign_type=AssignmentType.NORMAL,
        r_value=Identifier("b", pos=(1, 5)),
        pos=(1, 3),
    )

def test_item_literal(make_parser):
    src = """
a = ("key": "value");
b = (1: 10.0);
"""
    statements = make_parser(src).parse_program().statements
    assert statements == [
        AssignmentStmt(
            l_value=Identifier("a", pos=(2, 1)),
            assign_type=AssignmentType.NORMAL,
            r_value=ItemExpr(
                key=SimpleTypeExpr(SimpleLiteralType.STRING, "key", pos=(2, 6)),
                value=SimpleTypeExpr(SimpleLiteralType.STRING, "value", pos=(2, 13)),
                pos=(2, 5)
            ),
            pos=(2, 3),
        ),
        AssignmentStmt(
            l_value=Identifier("b", pos=(3, 1)),
            assign_type=AssignmentType.NORMAL,
            r_value=ItemExpr(
                key=SimpleTypeExpr(SimpleLiteralType.INT, 1, pos=(3, 6)),
                value=SimpleTypeExpr(SimpleLiteralType.FLOAT, 10.0, pos=(3, 9)),
                pos=(3, 5)
            ),
            pos=(3, 3),
        ),
    ]

def test_list_literal(make_parser):
    src="""
a = [];
b = [
        1, "Hello", -10.5, ("key": 5),
        ["hello", "from", "sublist"],
        {
            ("name": "dict),
            ("value": 5)
        }
];"""
    # statements = make_parser(src).parse_program().statements
    # assert statements == [
    #     AssignmentStmt(
    #         l_value=Identifier("a", pos=(2, 1)),
    #         assign_type=AssignmentType.NORMAL,
    #         r_value=ListExpr(
    #             elements=[],
    #             pos=(2, 5)
    #         ),
    #         pos=(2, 3)
    #     ),
    #     AssignmentStmt(
    #         l_value=Identifier("b", pos=(3, 1)),
    #         assign_type=AssignmentType.NORMAL,
    #         r_value=ListExpr(
    #             elements=[
    #                 SimpleTypeExpr(SimpleLiteralType.INT, 1, pos=(1, 9)),

    #             ],
    #             pos=(3, 5)
    #         ),
    #         pos=(3, 3)
    #     )
    # ]


def test_call_statement(make_parser):
    src = "b();"
    statement = make_parser(src).parse_program().statements[0]
    assert statement == CallExpr(
        callee=Identifier("b", pos=(1, 1)), args=[], pos=(1, 2)
    )


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
            l_value=Identifier("a", pos=(2, 5)),
            operation=BinaryOperationType.LT,
            r_value=SimpleTypeExpr(SimpleLiteralType.INT, 4, pos=(2, 9)),
            pos=(2, 7),
        ),
        body=Block(
            [CallExpr(Identifier("do_something", pos=(3, 5)), [], pos=(3, 17))],
            pos=(2, 12),
        ),
        elif_statements=[
            ElifStmt(
                condition=BinaryExpr(
                    Identifier("a", pos=(4, 9)),
                    BinaryOperationType.GT,
                    SimpleTypeExpr(SimpleLiteralType.INT, 4, pos=(4, 13)),
                    pos=(4, 11),
                ),
                body=Block(
                    [
                        CallExpr(
                            Identifier("do_something_else", pos=(5, 5)), [], pos=(5, 22)
                        )
                    ],
                    pos=(4, 16),
                ),
                pos=(4, 3),
            )
        ],
        else_body=Block(
            [
                CallExpr(
                    Identifier("do_something_differently", pos=(7, 5)), [], pos=(7, 29)
                )
            ],
            pos=(6, 8),
        ),
        pos=(2, 1),
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
            Identifier("a", pos=(3, 8)),
            BinaryOperationType.LT,
            SimpleTypeExpr(SimpleLiteralType.INT, 10, pos=(3, 12)),
            pos=(3, 10),
        ),
        body=Block(
            [
                CallExpr(
                    Identifier("do_something_ten_times", pos=(4, 5)), [], pos=(4, 27)
                ),
                AssignmentStmt(
                    Identifier("a", pos=(5, 5)),
                    AssignmentType.PLUS,
                    SimpleTypeExpr(SimpleLiteralType.INT, 1, pos=(5, 10)),
                    pos=(5, 7),
                ),
            ],
            pos=(3, 16),
        ),
        pos=(3, 1),
    )


def test_for_loop(make_parser):
    src = """
for element in my_dict {
    print(element.key()); // "first" "second"
}
"""
    statement = make_parser(src).parse_program().statements[0]
    assert statement == ForStmt(
        var=Identifier("element", pos=(2, 5)),
        source=Identifier("my_dict", pos=(2, 16)),
        body=Block(
            [
                CallExpr(
                    callee=Identifier("print", pos=(3, 5)),
                    args=[
                        CallExpr(
                            callee=AccessExpr(
                                source=Identifier("element", pos=(3, 11)),
                                target=Identifier("key", pos=(3, 19)),
                                pos=(3, 18),
                            ),
                            args=[],
                            pos=(3, 22),
                        )
                    ],
                    pos=(3, 10),
                ),
            ],
            pos=(2, 24),
        ),
        pos=(2, 1),
    )


def test_func_definition(make_parser):
    src = """
my_func = function(arg1, arg2) {
    return arg1 + arg2;
};
"""
    statement = make_parser(src).parse_program().statements[0]
    assert statement == AssignmentStmt(
        l_value=Identifier("my_func", pos=(2, 1)),
        assign_type=AssignmentType.NORMAL,
        r_value=FunctionExpr(
            params=[Identifier("arg1", pos=(2, 20)), Identifier("arg2", pos=(2, 26))],
            body=Block(
                [
                    ReturnStmt(
                        BinaryExpr(
                            Identifier("arg1", pos=(3, 12)),
                            BinaryOperationType.ADD,
                            Identifier("arg2", pos=(3, 19)),
                            pos=(3, 17),
                        ),
                        pos=(3, 5),
                    )
                ],
                pos=(2, 32),
            ),
            pos=(2, 11),
        ),
        pos=(2, 9),
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
        l_value=Identifier("small_cities", pos=(2, 1)),
        assign_type=AssignmentType.NORMAL,
        r_value=LinqExpr(
            var=Identifier("city", pos=(2, 21)),
            source=Identifier("my_dict", pos=(2, 29)),
            selects=[
                CallExpr(
                    callee=AccessExpr(
                        source=Identifier("city", pos=(3, 12)),
                        target=Identifier("key", pos=(3, 17)),
                        pos=(3, 16),
                    ),
                    args=[],
                    pos=(3, 20),
                ),
                BinaryExpr(
                    l_value=CallExpr(
                        callee=AccessExpr(
                            source=Identifier("city", pos=(3, 24)),
                            target=Identifier("value", pos=(3, 29)),
                            pos=(3, 28),
                        ),
                        args=[],
                        pos=(3, 34),
                    ),
                    operation=BinaryOperationType.DIV,
                    r_value=SimpleTypeExpr(SimpleLiteralType.INT, 1000, pos=(3, 39)),
                    pos=(3, 37),
                ),
            ],
            where=BinaryExpr(
                l_value=CallExpr(
                    callee=AccessExpr(
                        source=Identifier("city", pos=(4, 11)),
                        target=Identifier("value", pos=(4, 16)),
                        pos=(4, 15),
                    ),
                    args=[],
                    pos=(4, 21),
                ),
                operation=BinaryOperationType.LT,
                r_value=SimpleTypeExpr(SimpleLiteralType.INT, 5000000, pos=(4, 26)),
                pos=(4, 24),
            ),
            order_by=CallExpr(
                callee=AccessExpr(
                    source=Identifier("city", pos=(5, 14)),
                    target=Identifier("key", pos=(5, 19)),
                    pos=(5, 18),
                ),
                args=[],
                pos=(5, 22),
            ),
            descending=True,
            pos=(2, 16),
        ),
        pos=(2, 14),
    )
