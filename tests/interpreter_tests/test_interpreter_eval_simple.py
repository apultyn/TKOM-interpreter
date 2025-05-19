import src.interpreter.interpreter_objects as io
import src.parser.parser_objects as po


def test_int_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(po.IntExpr(5)) == io.IntValue(5)


def test_string_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(po.StringExpr("Hi")) == io.StringValue("Hi")


def test_float_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(po.FloatExpr(5.0)) == io.FloatValue(5.0)


def test_bool_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(po.BoolExpr(True)) == io.BoolValue(True)


def test_or_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(
        po.OrExpr(
            po.BoolExpr(True),
            po.BoolExpr(False),
        )
    ) == io.BoolValue(True)

    assert interpreter.eval(
        po.OrExpr(
            po.BoolExpr(False),
            po.BoolExpr(True),
        )
    ) == io.BoolValue(True)

    assert interpreter.eval(
        po.OrExpr(
            po.BoolExpr(True),
            po.BoolExpr(True),
        )
    ) == io.BoolValue(True)

    assert interpreter.eval(
        po.OrExpr(
            po.BoolExpr(False),
            po.BoolExpr(False),
        )
    ) == io.BoolValue(False)


def test_and_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(
        po.AndExpr(
            po.BoolExpr(True),
            po.BoolExpr(False),
        )
    ) == io.BoolValue(False)

    assert interpreter.eval(
        po.AndExpr(
            po.BoolExpr(False),
            po.BoolExpr(True),
        )
    ) == io.BoolValue(False)

    assert interpreter.eval(
        po.AndExpr(
            po.BoolExpr(True),
            po.BoolExpr(True),
        )
    ) == io.BoolValue(True)

    assert interpreter.eval(
        po.AndExpr(
            po.BoolExpr(False),
            po.BoolExpr(False),
        )
    ) == io.BoolValue(False)


def test_eq_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(po.EqExpr(po.IntExpr(5), po.IntExpr(5))) == io.BoolValue(
        True
    )

    assert interpreter.eval(po.EqExpr(po.IntExpr(5), po.IntExpr(-5))) == io.BoolValue(
        False
    )


def test_neq_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(po.NeqExpr(po.IntExpr(5), po.IntExpr(5))) == io.BoolValue(
        False
    )

    assert interpreter.eval(po.NeqExpr(po.IntExpr(5), po.IntExpr(-5))) == io.BoolValue(
        True
    )


def test_gt_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(po.GtExpr(po.IntExpr(5), po.IntExpr(-5))) == io.BoolValue(
        True
    )

    assert interpreter.eval(po.GtExpr(po.IntExpr(-5), po.IntExpr(5))) == io.BoolValue(
        False
    )


def test_geq_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(po.GeqExpr(po.IntExpr(5), po.IntExpr(-5))) == io.BoolValue(
        True
    )

    assert interpreter.eval(po.GeqExpr(po.IntExpr(-5), po.IntExpr(5))) == io.BoolValue(
        False
    )

    assert interpreter.eval(po.GeqExpr(po.IntExpr(5), po.IntExpr(5))) == io.BoolValue(
        True
    )


def test_lt_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(po.LtExpr(po.IntExpr(5), po.IntExpr(-5))) == io.BoolValue(
        False
    )

    assert interpreter.eval(po.LtExpr(po.IntExpr(-5), po.IntExpr(5))) == io.BoolValue(
        True
    )


def test_leq_expr(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(po.LeqExpr(po.IntExpr(5), po.IntExpr(-5))) == io.BoolValue(
        False
    )

    assert interpreter.eval(po.LeqExpr(po.IntExpr(-5), po.IntExpr(5))) == io.BoolValue(
        True
    )

    assert interpreter.eval(po.LeqExpr(po.IntExpr(5), po.IntExpr(5))) == io.BoolValue(
        True
    )


def test_add_expr_int(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(po.AddExpr(po.IntExpr(5), po.IntExpr(5))) == io.IntValue(10)


def test_add_expr_float(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(
        po.AddExpr(po.FloatExpr(5.0), po.FloatExpr(5.0))
    ) == io.FloatValue(10.0)


def test_add_expr_string(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(
        po.AddExpr(po.StringExpr("Hello"), po.StringExpr("World"))
    ) == io.StringValue("HelloWorld")


def test_sub_expr_int(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(po.SubExpr(po.IntExpr(5), po.IntExpr(5))) == io.IntValue(0)


def test_sub_expr_float(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(
        po.SubExpr(po.FloatExpr(5.0), po.FloatExpr(5.0))
    ) == io.FloatValue(0.0)


def test_mul_expr_int(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(po.MulExpr(po.IntExpr(5), po.IntExpr(5))) == io.IntValue(25)


def test_mul_expr_float(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(
        po.MulExpr(po.FloatExpr(5.0), po.FloatExpr(5.0))
    ) == io.FloatValue(25.0)


def test_div_expr_int(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(po.DivExpr(po.IntExpr(5), po.IntExpr(2))) == io.IntValue(2)


def test_div_expr_float(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(
        po.DivExpr(po.FloatExpr(5.0), po.FloatExpr(2.0))
    ) == io.FloatValue(2.5)


def test_logic_neg_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(po.LogicNegExpr(po.BoolExpr(True))) == io.BoolValue(False)

    assert interpreter.eval(po.LogicNegExpr(po.BoolExpr(False))) == io.BoolValue(True)


def test_arith_neg_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(po.ArithNegExpr(po.IntExpr(5))) == io.IntValue(-5)

    assert interpreter.eval(po.ArithNegExpr(po.FloatExpr(5.0))) == io.FloatValue(-5.0)


def test_list_expr(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(
        po.ListExpr([po.IntExpr(1, pos=(1, 1))], pos=(1, 1))
    ) == io.ListValue([io.IntValue(1)])


def test_normal_assignment(make_interpreter):
    interpreter = make_interpreter()
    interpreter.eval(
        po.NormalAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.IntExpr(5),
            pos=(1, 1),
        )
    )

    assert interpreter.global_env.get("x") == io.IntValue(5)


def test_normal_assignment_with_expr(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        po.NormalAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.AddExpr(po.IntExpr(5), po.IntExpr(5)),
            pos=(1, 1),
        )
    )
    assert interpreter.global_env.get("x") == io.IntValue(10)


def test_normal_assignment_overwrite(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        po.NormalAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.IntExpr(5),
            pos=(1, 1),
        )
    )

    interpreter.eval(
        po.NormalAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.FloatExpr(10.0),
            pos=(1, 1),
        )
    )

    assert interpreter.global_env.get("x") == io.FloatValue(10.0)


def test_plus_assignment(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        po.NormalAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.IntExpr(5),
            pos=(1, 1),
        )
    )

    interpreter.eval(
        po.PlusAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.IntExpr(5),
            pos=(1, 1),
        )
    )

    assert interpreter.global_env.get("x") == io.IntValue(10)


def test_plus_assignment_with_expr(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        po.NormalAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.IntExpr(5),
            pos=(1, 1),
        )
    )

    interpreter.eval(
        po.PlusAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.AddExpr(po.IntExpr(5), po.IntExpr(5)),
            pos=(1, 1),
        )
    )

    assert interpreter.global_env.get("x") == io.IntValue(15)


def test_minus_assignment(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        po.NormalAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.IntExpr(5),
            pos=(1, 1),
        )
    )

    interpreter.eval(
        po.MinusAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.IntExpr(5),
            pos=(1, 1),
        )
    )

    assert interpreter.global_env.get("x") == io.IntValue(0)


def test_minus_assignment_with_expr(make_interpreter):
    interpreter = make_interpreter()

    interpreter.eval(
        po.NormalAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.IntExpr(5),
            pos=(1, 1),
        )
    )

    interpreter.eval(
        po.MinusAssignmentStmt(
            po.Identifier("x", pos=(1, 1)),
            po.SubExpr(po.IntExpr(5), po.IntExpr(5)),
            pos=(1, 1),
        )
    )
    assert interpreter.global_env.get("x") == io.IntValue(5)
