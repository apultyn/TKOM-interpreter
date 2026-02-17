from unittest.mock import MagicMock

from src.interpreter.interpreter_objects import (
    IntValue,
    StringValue,
    FloatValue,
    BoolValue,
    ListValue,
    AccessedFuncValue,
    ItemValue,
    DictValue,
    UserFuncValue,
    BuiltInFuncValue,
)
from src.parser.parser_objects import (
    IfStmt,
    Identifier,
    IntExpr,
    StringExpr,
    FloatExpr,
    BoolExpr,
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
    LogicNegExpr,
    ArithNegExpr,
    ListExpr,
    ItemExpr,
    DictExpr,
    NormalAssignmentStmt,
    PlusAssignmentStmt,
    MinusAssignmentStmt,
    Block,
    ElifStmt,
    WhileStmt,
    ForStmt,
    AccessExpr,
    CallExpr,
    FunctionExpr,
    ReturnStmt,
    LinqExpr,
    BracketsExpr,
)

from src.interpreter.util import DEFAULT_SORT


def test_if_stmt_if_body(make_interpreter):
    interpreter = make_interpreter(
        env=[("x", StringValue("If")), ("path", StringValue("None"))]
    )
    interpreter.eval(
        IfStmt(
            condition=EqExpr(Identifier("x"), StringExpr("If")),
            body=Block(
                [NormalAssignmentStmt(Identifier("path"), StringExpr("if_body"))]
            ),
            elif_statements=[
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif1")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif1"))]
                    ),
                ),
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif2")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif2"))]
                    ),
                ),
            ],
            else_body=Block(
                [NormalAssignmentStmt(Identifier("path"), StringExpr("else"))]
            ),
        )
    )
    assert interpreter.global_env.get("path") == StringValue("if_body")


def test_if_stmt_elif_1(make_interpreter):
    interpreter = make_interpreter(
        env=[("x", StringValue("Elif1")), ("path", StringValue("None"))]
    )
    interpreter.eval(
        IfStmt(
            condition=EqExpr(Identifier("x"), StringExpr("If")),
            body=Block(
                [NormalAssignmentStmt(Identifier("path"), StringExpr("if_body"))]
            ),
            elif_statements=[
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif1")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif1"))]
                    ),
                ),
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif2")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif2"))]
                    ),
                ),
            ],
            else_body=Block(
                [NormalAssignmentStmt(Identifier("path"), StringExpr("else"))]
            ),
        )
    )
    assert interpreter.global_env.get("path") == StringValue("elif1")


def test_if_stmt_elif2(make_interpreter):
    interpreter = make_interpreter(
        env=[("x", StringValue("Elif2")), ("path", StringValue("None"))]
    )
    interpreter.eval(
        IfStmt(
            condition=EqExpr(Identifier("x"), StringExpr("If")),
            body=Block(
                [NormalAssignmentStmt(Identifier("path"), StringExpr("if_body"))]
            ),
            elif_statements=[
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif1")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif1"))]
                    ),
                ),
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif2")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif2"))]
                    ),
                ),
            ],
            else_body=Block(
                [NormalAssignmentStmt(Identifier("path"), StringExpr("else"))]
            ),
        )
    )
    assert interpreter.global_env.get("path") == StringValue("elif2")


def test_if_stmt_else(make_interpreter):
    interpreter = make_interpreter(
        env=[("x", StringValue("Else")), ("path", StringValue("None"))]
    )
    interpreter.eval(
        IfStmt(
            condition=EqExpr(Identifier("x"), StringExpr("If")),
            body=Block(
                [NormalAssignmentStmt(Identifier("path"), StringExpr("if_body"))]
            ),
            elif_statements=[
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif1")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif1"))]
                    ),
                ),
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif2")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif2"))]
                    ),
                ),
            ],
            else_body=Block(
                [NormalAssignmentStmt(Identifier("path"), StringExpr("else"))]
            ),
        )
    )
    assert interpreter.global_env.get("path") == StringValue("else")


def test_if_execute_only_1_elif(make_interpreter):
    interpreter = make_interpreter(
        env=[("x", StringValue("Elif")), ("path", StringValue("None"))]
    )
    interpreter.eval(
        IfStmt(
            condition=EqExpr(Identifier("x"), StringExpr("If")),
            body=Block(
                [NormalAssignmentStmt(Identifier("path"), StringExpr("if_body"))]
            ),
            elif_statements=[
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif1"))]
                    ),
                ),
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif2"))]
                    ),
                ),
            ],
            else_body=Block(
                [NormalAssignmentStmt(Identifier("path"), StringExpr("else"))]
            ),
        )
    )

    assert interpreter.global_env.get("path") == StringValue("elif1")


def test_if_no_path(make_interpreter):
    interpreter = make_interpreter(
        env=[("x", StringValue("Else")), ("path", StringValue("None"))]
    )
    interpreter.eval(
        IfStmt(
            condition=EqExpr(Identifier("x"), StringExpr("If")),
            body=Block(
                [NormalAssignmentStmt(Identifier("path"), StringExpr("if_body"))]
            ),
            elif_statements=[
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif1")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif1"))]
                    ),
                ),
                ElifStmt(
                    condition=EqExpr(Identifier("x"), StringExpr("Elif1")),
                    body=Block(
                        [NormalAssignmentStmt(Identifier("path"), StringExpr("elif2"))]
                    ),
                ),
            ],
            else_body=None,
        )
    )

    assert interpreter.global_env.get("path") == StringValue("None")


def test_while_stmt(make_interpreter):
    interpreter = make_interpreter(env=[("x", IntValue(5)), ("i", IntValue(0))])

    interpreter.eval(
        WhileStmt(
            condition=GeqExpr(Identifier("x"), IntExpr(0)),
            body=Block(
                [
                    MinusAssignmentStmt(Identifier("x"), IntExpr(1)),
                    PlusAssignmentStmt(Identifier("i"), IntExpr(1)),
                ]
            ),
        )
    )

    assert interpreter.global_env.get("i") == IntValue(6)


def test_while_stmt_0(make_interpreter):
    interpreter = make_interpreter(env=[("x", IntValue(5)), ("i", IntValue(0))])

    interpreter.eval(
        WhileStmt(
            condition=LtExpr(Identifier("x"), IntExpr(0)),
            body=Block(
                [
                    MinusAssignmentStmt(Identifier("x"), IntExpr(1)),
                    PlusAssignmentStmt(Identifier("i"), IntExpr(1)),
                ]
            ),
        )
    )

    assert interpreter.global_env.get("i") == IntValue(0)


def test_for_stmt(make_interpreter):
    interpreter = make_interpreter(
        env=[
            ("list", ListValue([IntValue(1), IntValue(2), IntValue(3)])),
            ("new_list", ListValue([])),
            ("var", StringValue("Original")),
        ]
    )

    interpreter.eval(
        ForStmt(
            var=Identifier("var"),
            source=Identifier("list"),
            body=Block(
                [
                    CallExpr(
                        callee=AccessExpr(
                            source=Identifier("new_list"), target=Identifier("add")
                        ),
                        args=[AddExpr(Identifier("var"), IntExpr(1))],
                    )
                ]
            ),
        )
    )

    interpreter.global_env.get("list") == ListValue(
        [IntValue(1), IntValue(2), IntValue(3)]
    )
    interpreter.global_env.get("new_list") == ListValue(
        [IntValue(2), IntValue(3), IntValue(4)]
    )
    interpreter.global_env.get("var") == StringValue("Original")


def test_for_stmt_empty_col(make_interpreter):
    interpreter = make_interpreter(
        env=[
            ("list", ListValue([])),
            ("counter", IntValue(0)),
            ("var", StringValue("Original")),
        ]
    )

    interpreter.eval(
        ForStmt(
            var=Identifier("var"),
            source=Identifier("list"),
            body=Block([PlusAssignmentStmt(Identifier("counter"), IntValue(1))]),
        )
    )

    assert interpreter.global_env.get("counter") == IntValue(0)


def test_normal_assignment(make_interpreter):
    interpreter = make_interpreter()
    interpreter.eval(
        NormalAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            IntExpr(5),
        )
    )

    assert interpreter.global_env.get("x") == IntValue(5)


def test_normal_assignment_with_expr(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        NormalAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            AddExpr(IntExpr(5), IntExpr(5)),
            pos=(1, 1),
        )
    )
    assert interpreter.global_env.get("x") == IntValue(10)


def test_normal_assignment_overwrite(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        NormalAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            IntExpr(5),
            pos=(1, 1),
        )
    )

    interpreter.eval(
        NormalAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            FloatExpr(10.0),
            pos=(1, 1),
        )
    )

    assert interpreter.global_env.get("x") == FloatValue(10.0)


def test_plus_assignment(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        NormalAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            IntExpr(5),
            pos=(1, 1),
        )
    )

    interpreter.eval(
        PlusAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            IntExpr(5),
            pos=(1, 1),
        )
    )

    assert interpreter.global_env.get("x") == IntValue(10)


def test_plus_assignment_with_expr(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        NormalAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            IntExpr(5),
        )
    )

    interpreter.eval(
        PlusAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            AddExpr(IntExpr(5), IntExpr(5)),
        )
    )

    assert interpreter.global_env.get("x") == IntValue(15)


def test_minus_assignment(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        NormalAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            IntExpr(5),
            pos=(1, 1),
        )
    )

    interpreter.eval(
        MinusAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            IntExpr(5),
            pos=(1, 1),
        )
    )

    assert interpreter.global_env.get("x") == IntValue(0)


def test_minus_assignment_with_expr(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        NormalAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            IntExpr(5),
            pos=(1, 1),
        )
    )

    interpreter.eval(
        MinusAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            SubExpr(IntExpr(5), IntExpr(5)),
            pos=(1, 1),
        )
    )
    assert interpreter.global_env.get("x") == IntValue(5)


def test_int_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(IntExpr(5)) == IntValue(5)


def test_string_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(StringExpr("Hi")) == StringValue("Hi")


def test_float_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(FloatExpr(5.0)) == FloatValue(5.0)


def test_bool_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(BoolExpr(True)) == BoolValue(True)


def test_or_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(
        OrExpr(
            BoolExpr(True),
            BoolExpr(False),
        )
    ) == BoolValue(True)

    assert interpreter.eval(
        OrExpr(
            BoolExpr(False),
            BoolExpr(True),
        )
    ) == BoolValue(True)

    assert interpreter.eval(
        OrExpr(
            BoolExpr(True),
            BoolExpr(True),
        )
    ) == BoolValue(True)

    assert interpreter.eval(
        OrExpr(
            BoolExpr(False),
            BoolExpr(False),
        )
    ) == BoolValue(False)


def test_and_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(
        AndExpr(
            BoolExpr(True),
            BoolExpr(False),
        )
    ) == BoolValue(False)

    assert interpreter.eval(
        AndExpr(
            BoolExpr(False),
            BoolExpr(True),
        )
    ) == BoolValue(False)

    assert interpreter.eval(
        AndExpr(
            BoolExpr(True),
            BoolExpr(True),
        )
    ) == BoolValue(True)

    assert interpreter.eval(
        AndExpr(
            BoolExpr(False),
            BoolExpr(False),
        )
    ) == BoolValue(False)


def test_eq_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(EqExpr(IntExpr(5), IntExpr(5))) == BoolValue(True)
    assert interpreter.eval(EqExpr(IntExpr(5), IntExpr(-5))) == BoolValue(False)


def test_neq_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(NeqExpr(IntExpr(5), IntExpr(5))) == BoolValue(False)
    assert interpreter.eval(NeqExpr(IntExpr(5), IntExpr(-5))) == BoolValue(True)


def test_gt_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(GtExpr(IntExpr(5), IntExpr(-5))) == BoolValue(True)
    assert interpreter.eval(GtExpr(IntExpr(-5), IntExpr(5))) == BoolValue(False)


def test_geq_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(GeqExpr(IntExpr(5), IntExpr(-5))) == BoolValue(True)
    assert interpreter.eval(GeqExpr(IntExpr(-5), IntExpr(5))) == BoolValue(False)
    assert interpreter.eval(GeqExpr(IntExpr(5), IntExpr(5))) == BoolValue(True)


def test_lt_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(LtExpr(IntExpr(5), IntExpr(-5))) == BoolValue(False)
    assert interpreter.eval(LtExpr(IntExpr(-5), IntExpr(5))) == BoolValue(True)


def test_leq_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(LeqExpr(IntExpr(5), IntExpr(-5))) == BoolValue(False)
    assert interpreter.eval(LeqExpr(IntExpr(-5), IntExpr(5))) == BoolValue(True)
    assert interpreter.eval(LeqExpr(IntExpr(5), IntExpr(5))) == BoolValue(True)


def test_add_expr_int(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(AddExpr(IntExpr(5), IntExpr(5))) == IntValue(10)


def test_add_expr_float(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(AddExpr(FloatExpr(5.0), FloatExpr(5.0))) == FloatValue(10.0)


def test_add_expr_string(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(
        AddExpr(StringExpr("Hello"), StringExpr("World"))
    ) == StringValue("HelloWorld")


def test_sub_expr_int(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(SubExpr(IntExpr(5), IntExpr(5))) == IntValue(0)


def test_sub_expr_float(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(SubExpr(FloatExpr(5.0), FloatExpr(5.0))) == FloatValue(0.0)


def test_mul_expr_int(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(MulExpr(IntExpr(5), IntExpr(5))) == IntValue(25)


def test_mul_expr_float(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(MulExpr(FloatExpr(5.0), FloatExpr(5.0))) == FloatValue(25.0)


def test_div_expr_int(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(DivExpr(IntExpr(5), IntExpr(2))) == IntValue(2)


def test_div_expr_float(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(DivExpr(FloatExpr(5.0), FloatExpr(2.0))) == FloatValue(2.5)


def test_logic_neg_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(LogicNegExpr(BoolExpr(True))) == BoolValue(False)
    assert interpreter.eval(LogicNegExpr(BoolExpr(False))) == BoolValue(True)


def test_arith_neg_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(ArithNegExpr(IntExpr(5))) == IntValue(-5)
    assert interpreter.eval(ArithNegExpr(FloatExpr(5.0))) == FloatValue(-5.0)


def test_list_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(ListExpr([IntExpr(1)])) == ListValue([IntValue(1)])

    assert interpreter.eval(
        ListExpr(
            [
                AddExpr(IntExpr(5), IntExpr(5)),
                EqExpr(StringExpr("Hi"), StringExpr("there")),
            ]
        )
    ) == ListValue([IntValue(10), BoolValue(False)])


def test_item_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(ItemExpr(StringExpr("key"), IntExpr(10))) == ItemValue(
        StringValue("key"), IntValue(10)
    )

    assert interpreter.eval(
        ItemExpr(
            AddExpr(IntExpr(5), IntExpr(5)),
            EqExpr(StringExpr("Hi"), StringExpr("there")),
        )
    ) == ItemValue(IntValue(10), BoolValue(False))


def test_dict_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(
        DictExpr(
            [
                ItemExpr(IntExpr(10), IntExpr(-5)),
                ItemExpr(AddExpr(IntExpr(2), IntExpr(2)), StringExpr("Val")),
                ItemExpr(StringExpr("Key"), StringExpr("value")),
            ],
        )
    ) == DictValue(
        [
            ItemValue(IntValue(10), IntValue(-5)),
            ItemValue(IntValue(4), StringValue("Val")),
            ItemValue(StringValue("Key"), StringValue("value")),
        ],
        DEFAULT_SORT,
    )


def test_function_expr(make_interpreter):
    interpreter = make_interpreter()

    func_expr = FunctionExpr(
        [Identifier("arg1"), Identifier("arg2")],
        Block([ReturnStmt(AddExpr(Identifier("arg1"), Identifier("arg2")))]),
    )

    assert interpreter.eval(func_expr) == UserFuncValue(["arg1", "arg2"], func_expr)


def test_linq_expr(make_interpreter):
    interpreter = make_interpreter(
        env=[
            ("var", StringValue("Original")),
            ("source", ListValue([IntValue(-1), IntValue(-2), IntValue(3)])),
        ]
    )

    assert interpreter.eval(
        LinqExpr(
            var=Identifier("var"),
            source=Identifier("source"),
            selects=[
                MulExpr(Identifier("var"), Identifier("var")),
                MulExpr(
                    Identifier("var"),
                    MulExpr(Identifier("var"), Identifier("var")),
                ),
            ],
            where=LtExpr(MulExpr(Identifier("var"), Identifier("var")), IntExpr(9)),
            order_by=ArithNegExpr(Identifier("var")),
            descending=True,
        )
    ) == ListValue(
        [ListValue([IntValue(4), IntValue(-8)]), ListValue([IntValue(1), IntValue(-1)])]
    )


def test_brackets_expr(make_interpreter):
    assert make_interpreter().eval(
        MulExpr(IntExpr(3), BracketsExpr(AddExpr(IntExpr(5), IntExpr(-10))))
    ) == IntValue(-15)


def test_access_expr(make_interpreter):
    interpreter = make_interpreter(
        env=[
            (
                "Int.getFive",
                AccessedFuncValue(body=lambda: IntValue(5)),
            )
        ]
    )

    func = interpreter.eval(AccessExpr(source=IntExpr(0), target=Identifier("getFive")))
    assert isinstance(func, AccessedFuncValue)
    assert func.body() == IntValue(5)
    assert func.needs_inter == False
    assert func.owner == IntValue(0)

    another_func = interpreter.eval(
        AccessExpr(
            source=AddExpr(IntExpr(-5), IntExpr(5)), target=Identifier("getFive")
        )
    )

    assert isinstance(another_func, AccessedFuncValue)
    assert func.body() == IntValue(5)
    assert func.owner == IntValue(0)


def test_call_expr(make_interpreter, monkeypatch):
    dummy_func = UserFuncValue([[]], None)

    interpreter = make_interpreter(env=[("my_func", dummy_func)])
    node = CallExpr(
        Identifier("my_func"),
        [IntExpr(5), MulExpr(FloatExpr(8.5), FloatExpr(7.3))],
        pos=(1, 1),
    )

    expected_value = StringValue("Result")
    mock_call = MagicMock(return_value=expected_value)

    monkeypatch.setattr(interpreter, "call_function", mock_call)

    assert interpreter.eval(node) == StringValue("Result")

    mock_call.assert_called_once()
    function, arg_objects, env, call_pos = mock_call.call_args[0]

    assert function is dummy_func
    assert arg_objects == [IntValue(5), FloatValue(62.05)]
    assert env is interpreter.global_env
    assert call_pos == (1, 1)


def test_call_function_user(make_interpreter):
    interpreter = make_interpreter()

    func = UserFuncValue(
        ["arg1", "arg2"],
        FunctionExpr(
            [Identifier("arg1"), Identifier("arg2")],
            Block([ReturnStmt(AddExpr(Identifier("arg1"), Identifier("arg2")))]),
        ),
    )

    assert interpreter.call_function(
        func,
        [IntValue(1), IntValue(3)],
    ) == IntValue(4)


def test_call_function_built_in(make_interpreter):
    interpreter = make_interpreter()

    func = BuiltInFuncValue(lambda _, text: text + StringValue(" There"))

    assert interpreter.call_function(func, [StringValue("Hello")]) == StringValue(
        "Hello There"
    )


def test_call_function_access(make_interpreter):
    interpreter = make_interpreter()

    func = AccessedFuncValue(
        lambda owner, _, float: (float / FloatValue(2.5)) + owner,
        owner=FloatValue(1.75),
    )

    assert interpreter.call_function(func, [FloatValue(-6.25)]) == FloatValue(-0.75)


def test_normal_assignment_updates_parent_scope(make_interpreter):
    interpreter = make_interpreter(env=[("x", IntValue(1))])

    func = UserFuncValue(
        [],
        FunctionExpr(
            [],
            Block([NormalAssignmentStmt(Identifier("x"), IntExpr(99))]),
        ),
    )

    interpreter.call_function(func, [], interpreter.global_env)

    assert interpreter.global_env.get("x") == IntValue(99)


def test_normal_assignment_defines_new_var_in_current_scope(make_interpreter):
    interpreter = make_interpreter()

    func = UserFuncValue(
        [],
        FunctionExpr(
            [],
            Block([NormalAssignmentStmt(Identifier("y"), IntExpr(42))]),
        ),
    )

    interpreter.call_function(func, [], interpreter.global_env)

    # y was defined inside the function scope and should not leak to global
    try:
        interpreter.global_env.get("y")
        assert False, "y should not exist in global scope"
    except ValueError:
        pass


def test_linq_no_where(make_interpreter):
    interpreter = make_interpreter(
        env=[("source", ListValue([IntValue(3), IntValue(1), IntValue(2)]))]
    )

    assert interpreter.eval(
        LinqExpr(
            var=Identifier("x"),
            source=Identifier("source"),
            selects=[Identifier("x")],
        )
    ) == ListValue(
        [ListValue([IntValue(3)]), ListValue([IntValue(1)]), ListValue([IntValue(2)])]
    )


def test_linq_no_where_order_ascending(make_interpreter):
    interpreter = make_interpreter(
        env=[("source", ListValue([IntValue(3), IntValue(1), IntValue(2)]))]
    )

    assert interpreter.eval(
        LinqExpr(
            var=Identifier("x"),
            source=Identifier("source"),
            selects=[Identifier("x")],
            order_by=Identifier("x"),
            descending=False,
        )
    ) == ListValue(
        [ListValue([IntValue(1)]), ListValue([IntValue(2)]), ListValue([IntValue(3)])]
    )


def test_linq_no_where_order_descending(make_interpreter):
    interpreter = make_interpreter(
        env=[("source", ListValue([IntValue(3), IntValue(1), IntValue(2)]))]
    )

    assert interpreter.eval(
        LinqExpr(
            var=Identifier("x"),
            source=Identifier("source"),
            selects=[Identifier("x")],
            order_by=Identifier("x"),
            descending=True,
        )
    ) == ListValue(
        [ListValue([IntValue(3)]), ListValue([IntValue(2)]), ListValue([IntValue(1)])]
    )
