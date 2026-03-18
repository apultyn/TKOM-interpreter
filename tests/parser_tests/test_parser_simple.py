import pytest

from src.parser.parser_objects import (
    NormalAssignmentStmt,
    MinusAssignmentStmt,
    PlusAssignmentStmt,
    Identifier,
    CallExpr,
    IfStmt,
    Block,
    ElifStmt,
    WhileStmt,
    ForStmt,
    AccessExpr,
    FunctionExpr,
    ReturnStmt,
    LinqExpr,
    ItemExpr,
    ListExpr,
    DictExpr,
    LtExpr,
    GtExpr,
    AddExpr,
    DivExpr,
    IntExpr,
    FloatExpr,
    StringExpr,
    BoolExpr,
)


@pytest.mark.parametrize(
    "src, AssignmentClass, col",
    [
        ("a = 10;", NormalAssignmentStmt, 5),
        ("a += 10;", PlusAssignmentStmt, 6),
        ("a -= 10;", MinusAssignmentStmt, 6),
    ],
)
def test_assigmnents(make_parser, src, AssignmentClass, col):
    statement = make_parser(src).parse_program().statements[0]
    assert statement == AssignmentClass(
        l_value=Identifier("a", pos=(1, 1)),
        r_value=IntExpr(10, pos=(1, col)),
        pos=(1, 3),
    )


@pytest.mark.parametrize(
    "ident_name, ExprClass, value, value_text",
    [
        ("a", IntExpr, 125, 125),
        ("b", FloatExpr, 0.25, 0.25),
        ("c", StringExpr, "Hello there", '"Hello there"'),
        ("d", BoolExpr, False, "False"),
        ("e", BoolExpr, True, "True"),
    ],
)
def test_simple_type_expressions(make_parser, ident_name, ExprClass, value, value_text):
    src = f"{ident_name} = {value_text};"
    statement = make_parser(src).parse_program().statements[0]
    assert statement == NormalAssignmentStmt(
        l_value=Identifier(ident_name, pos=(1, 1)),
        r_value=ExprClass(value, pos=(1, 5)),
        pos=(1, 3),
    )


def test_ident_as_expression(make_parser):
    src = "a = b;"
    statement = make_parser(src).parse_program().statements[0]
    assert statement == NormalAssignmentStmt(
        l_value=Identifier("a", pos=(1, 1)),
        r_value=Identifier("b", pos=(1, 5)),
        pos=(1, 3),
    )


def test_call_as_statement(make_parser):
    src = """
b();
a.b.c(5);
"""
    statements = make_parser(src).parse_program().statements
    assert statements == [
        CallExpr(callee=Identifier("b", pos=(2, 1)), args=[], pos=(2, 2)),
        CallExpr(
            callee=AccessExpr(
                source=AccessExpr(
                    source=Identifier("a", pos=(3, 1)),
                    target=Identifier("b", pos=(3, 3)),
                    pos=(3, 2),
                ),
                target=Identifier("c", pos=(3, 5)),
                pos=(3, 4),
            ),
            args=[IntExpr(5, pos=(3, 7))],
            pos=(3, 6),
        ),
    ]


def test_item_literal(make_parser):
    src = """
a = ("key": "value");
b = (1: 10.0);
"""
    statements = make_parser(src).parse_program().statements
    assert statements == [
        NormalAssignmentStmt(
            l_value=Identifier("a", pos=(2, 1)),
            r_value=ItemExpr(
                key=StringExpr("key", pos=(2, 6)),
                value=StringExpr("value", pos=(2, 13)),
                pos=(2, 5),
            ),
            pos=(2, 3),
        ),
        NormalAssignmentStmt(
            l_value=Identifier("b", pos=(3, 1)),
            r_value=ItemExpr(
                key=IntExpr(1, pos=(3, 6)),
                value=FloatExpr(10.0, pos=(3, 9)),
                pos=(3, 5),
            ),
            pos=(3, 3),
        ),
    ]


def test_list_literal(make_parser):
    src = """
a = [];
b = [
        1, "Hello", 10.5, ("key": 5),
        ["hello", "from", "sublist"],
        {
            ("name": "dict"),
            ("value": 5)
        }
];"""
    statements = make_parser(src).parse_program().statements
    assert statements == [
        NormalAssignmentStmt(
            l_value=Identifier("a", pos=(2, 1)),
            r_value=ListExpr(elements=[], pos=(2, 5)),
            pos=(2, 3),
        ),
        NormalAssignmentStmt(
            l_value=Identifier("b", pos=(3, 1)),
            r_value=ListExpr(
                elements=[
                    IntExpr(1, pos=(4, 9)),
                    StringExpr("Hello", pos=(4, 12)),
                    FloatExpr(10.5, pos=(4, 21)),
                    ItemExpr(
                        key=StringExpr("key", pos=(4, 28)),
                        value=IntExpr(5, pos=(4, 35)),
                        pos=(4, 27),
                    ),
                    ListExpr(
                        elements=[
                            StringExpr("hello", pos=(5, 10)),
                            StringExpr("from", pos=(5, 19)),
                            StringExpr("sublist", pos=(5, 27)),
                        ],
                        pos=(5, 9),
                    ),
                    DictExpr(
                        items=[
                            ItemExpr(
                                key=StringExpr("name", pos=(7, 14)),
                                value=StringExpr("dict", pos=(7, 22)),
                                pos=(7, 13),
                            ),
                            ItemExpr(
                                key=StringExpr("value", pos=(8, 14)),
                                value=IntExpr(5, pos=(8, 23)),
                                pos=(8, 13),
                            ),
                        ],
                        pos=(6, 9),
                    ),
                ],
                pos=(3, 5),
            ),
            pos=(3, 3),
        ),
    ]


def test_dict_literal(make_parser):
    src = """
a = {};
b = {
    ("first_key": 5),
    ("another_key": "value"),
    ("one_more": [1, 5, "hello"]),
    ("last_one": {("key": "value")})
};
"""
    statements = make_parser(src).parse_program().statements
    assert statements == [
        NormalAssignmentStmt(
            l_value=Identifier("a", pos=(2, 1)),
            r_value=DictExpr(items=[], pos=(2, 5)),
            pos=(2, 3),
        ),
        NormalAssignmentStmt(
            l_value=Identifier("b", pos=(3, 1)),
            r_value=DictExpr(
                items=[
                    ItemExpr(
                        key=StringExpr("first_key", pos=(4, 6)),
                        value=IntExpr(5, pos=(4, 19)),
                        pos=(4, 5),
                    ),
                    ItemExpr(
                        key=StringExpr("another_key", pos=(5, 6)),
                        value=StringExpr("value", pos=(5, 21)),
                        pos=(5, 5),
                    ),
                    ItemExpr(
                        key=StringExpr("one_more", pos=(6, 6)),
                        value=ListExpr(
                            elements=[
                                IntExpr(1, pos=(6, 19)),
                                IntExpr(5, pos=(6, 22)),
                                StringExpr("hello", pos=(6, 25)),
                            ],
                            pos=(6, 18),
                        ),
                        pos=(6, 5),
                    ),
                    ItemExpr(
                        key=StringExpr("last_one", pos=(7, 6)),
                        value=DictExpr(
                            items=[
                                ItemExpr(
                                    key=StringExpr("key", pos=(7, 20)),
                                    value=StringExpr("value", pos=(7, 27)),
                                    pos=(7, 19),
                                )
                            ],
                            pos=(7, 18),
                        ),
                        pos=(7, 5),
                    ),
                ],
                pos=(3, 5),
            ),
            pos=(3, 3),
        ),
    ]


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
        condition=LtExpr(
            l_value=Identifier("a", pos=(2, 5)),
            r_value=IntExpr(4, pos=(2, 9)),
            pos=(2, 7),
        ),
        body=Block(
            [CallExpr(Identifier("do_something", pos=(3, 5)), [], pos=(3, 17))],
            pos=(2, 12),
        ),
        elif_statements=[
            ElifStmt(
                condition=GtExpr(
                    Identifier("a", pos=(4, 9)),
                    IntExpr(4, pos=(4, 13)),
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
        condition=LtExpr(
            Identifier("a", pos=(3, 8)),
            IntExpr(10, pos=(3, 12)),
            pos=(3, 10),
        ),
        body=Block(
            [
                CallExpr(
                    Identifier("do_something_ten_times", pos=(4, 5)), [], pos=(4, 27)
                ),
                PlusAssignmentStmt(
                    Identifier("a", pos=(5, 5)),
                    IntExpr(1, pos=(5, 10)),
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
    assert statement == NormalAssignmentStmt(
        l_value=Identifier("my_func", pos=(2, 1)),
        r_value=FunctionExpr(
            params=[Identifier("arg1", pos=(2, 20)), Identifier("arg2", pos=(2, 26))],
            body=Block(
                [
                    ReturnStmt(
                        AddExpr(
                            Identifier("arg1", pos=(3, 12)),
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
    assert statement == NormalAssignmentStmt(
        l_value=Identifier("small_cities", pos=(2, 1)),
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
                DivExpr(
                    l_value=CallExpr(
                        callee=AccessExpr(
                            source=Identifier("city", pos=(3, 24)),
                            target=Identifier("value", pos=(3, 29)),
                            pos=(3, 28),
                        ),
                        args=[],
                        pos=(3, 34),
                    ),
                    r_value=IntExpr(1000, pos=(3, 39)),
                    pos=(3, 37),
                ),
            ],
            where=LtExpr(
                l_value=CallExpr(
                    callee=AccessExpr(
                        source=Identifier("city", pos=(4, 11)),
                        target=Identifier("value", pos=(4, 16)),
                        pos=(4, 15),
                    ),
                    args=[],
                    pos=(4, 21),
                ),
                r_value=IntExpr(5000000, pos=(4, 26)),
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
