from src.interpreter.interpreter_objects import (
    IntValue,
    StringValue,
    FloatValue,
    BoolValue,
    ListValue,
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
    NormalAssignmentStmt,
    PlusAssignmentStmt,
    MinusAssignmentStmt,
    Block,
    ElifStmt,
)


def test_if_stmt(make_interpreter):
    interpreter = make_interpreter()
    interpreter.global_env.define("x", StringValue("If"))
    interpreter.global_env.define("path", StringValue("None"))
    interpreter.eval(
        IfStmt(
            condition=EqExpr(Identifier("x"), StringExpr("If")),
            body=Block([NormalAssignmentStmt(Identifier("path"), StringExpr("if_body"))]),
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

    interpreter.global_env.set("x", StringValue("Elif1"))
    interpreter.eval(
        IfStmt(
            condition=EqExpr(Identifier("x"), StringExpr("If")),
            body=Block([NormalAssignmentStmt(Identifier("path"), StringExpr("if_body"))]),
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

    interpreter.global_env.set("x", StringValue("Elif2"))
    interpreter.eval(
        IfStmt(
            condition=EqExpr(Identifier("x"), StringExpr("If")),
            body=Block([NormalAssignmentStmt(Identifier("path"), StringExpr("if_body"))]),
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


    interpreter.global_env.set("x", StringValue("Else"))
    interpreter.eval(
        IfStmt(
            condition=EqExpr(Identifier("x"), StringExpr("If")),
            body=Block([NormalAssignmentStmt(Identifier("path"), StringExpr("if_body"))]),
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
    assert interpreter.eval(
        ListExpr([IntExpr(1, pos=(1, 1))], pos=(1, 1))
    ) == ListValue([IntValue(1)])


def test_normal_assignment(make_interpreter):
    interpreter = make_interpreter()
    interpreter.eval(
        NormalAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            IntExpr(5),
            pos=(1, 1),
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
            pos=(1, 1),
        )
    )

    interpreter.eval(
        PlusAssignmentStmt(
            Identifier("x", pos=(1, 1)),
            AddExpr(IntExpr(5), IntExpr(5)),
            pos=(1, 1),
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
