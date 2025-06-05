import pytest

import src.parser.parser_objects as po
import src.interpreter.interpreter_objects as io

from src.util.pyscript_exceptions import RuntimeException
from tests.util import AbortExecution, check_error


def test_program_return(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(po.Program([po.ReturnStmt(po.IntExpr(5), pos=(3, 1))]))

    check_error(
        mocked_error_handler,
        RuntimeException,
        (3, 1),
        msg="Return statement not allowed outside function",
    )


def test_program_return_nested(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.Program(
                [
                    po.IfStmt(
                        condition=po.IntExpr(5),
                        body=po.Block([po.ReturnStmt(po.IntExpr(5), pos=(3, 1))]),
                    )
                ]
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (3, 1),
        msg="Return statement not allowed outside function",
    )


def test_if_stmt_empty_condition(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.IfStmt(
                po.CallExpr(po.Identifier("func"), args=[], pos=(5, 3)),
                po.Block([]),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (5, 3),
        msg="Condition was evaluated to None, value expected",
    )


def test_elif_stmt_empty_condition(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.IfStmt(
                po.ListExpr([]),
                po.Block([]),
                elif_statements=[
                    po.ElifStmt(
                        po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                        po.Block([]),
                        pos=(1, 5),
                    )
                ],
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Condition was evaluated to None, value expected",
    )


def test_while_stmt_empty_condition(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.WhileStmt(
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                po.Block([]),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Condition was evaluated to None, value expected",
    )


def test_for_stmt_not_collention(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.ForStmt(
                po.Identifier("var"),
                po.IntExpr(5, pos=(2, 5)),
                po.Block([]),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 5),
        msg="Source should be a collection, got 'Int'",
    )


def test_for_stmt_empty_source(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.ForStmt(
                po.Identifier("var"),
                po.CallExpr(po.Identifier("func"), args=[], pos=(5, 3)),
                po.Block([]),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (5, 3),
        msg="Source was evaluated to None, value expected",
    )


def test_normal_assignment_empty_r_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.NormalAssignmentStmt(
                po.Identifier("var"),
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="r_value was evaluated to None, value expected",
    )


def test_plus_assignment_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    interpreter.global_env.define(
        "x",
        io.IntValue(5),
    )

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.PlusAssignmentStmt(
                po.Identifier("x", pos=(1, 1)),
                po.StringExpr("5"),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '+=' operation - got 'Int' and 'String'",
    )


def test_plus_assignment_unsupported_type(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    interpreter.global_env.define(
        "x",
        io.ItemValue(io.IntValue(1), io.IntValue(1)),
    )

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.PlusAssignmentStmt(
                po.Identifier("x", pos=(1, 1)),
                po.ItemExpr(po.IntExpr(1), po.IntExpr(1)),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Operation '+=' not supported for type 'Item'",
    )


def test_plus_assignment_undefined_variable(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.PlusAssignmentStmt(
                po.Identifier("x", pos=(1, 1)),
                po.IntExpr(5),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="'x' is not defined in this scope",
    )


def test_plus_assignment_empty_r_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(
        env=[("x", io.IntValue(1)), ("func", io.BuiltInFuncValue(lambda _: None))]
    )

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.PlusAssignmentStmt(
                po.Identifier("x"),
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="r_value was evaluated to None, value expected",
    )


def test_minus_assignment_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    interpreter.global_env.define(
        "x",
        io.IntValue(5),
    )

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.MinusAssignmentStmt(
                po.Identifier("x", pos=(1, 1)),
                po.StringExpr("5"),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '-=' operation - got 'Int' and 'String'",
    )


def test_minus_assignment_unsupported_type(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    interpreter.global_env.define(
        "x",
        io.ItemValue(io.IntValue(1), io.IntValue(1)),
    )

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.MinusAssignmentStmt(
                po.Identifier("x", pos=(1, 1)),
                po.ItemExpr(po.IntExpr(1), po.IntExpr(1)),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Operation '-=' not supported for type 'Item'",
    )


def test_minus_assignment_undefined_variable(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.MinusAssignmentStmt(
                po.Identifier("x", pos=(1, 1)),
                po.IntExpr(5),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="'x' is not defined in this scope",
    )


def test_minus_assignment_empty_r_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(
        env=[("x", io.IntValue(1)), ("func", io.BuiltInFuncValue(lambda _: None))]
    )

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.MinusAssignmentStmt(
                po.Identifier("x"),
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="r_value was evaluated to None, value expected",
    )


def test_or_expr_empty_l_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.OrExpr(
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                po.IntExpr(1),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="l_value was evaluated to None, value expected",
    )


def test_or_expr_empty_r_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.OrExpr(
                po.BoolExpr(False),
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="r_value was evaluated to None, value expected",
    )


def test_and_expr_empty_l_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.AndExpr(
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                po.IntExpr(1),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="l_value was evaluated to None, value expected",
    )


def test_and_expr_empty_r_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.AndExpr(
                po.BoolExpr(True),
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="r_value was evaluated to None, value expected",
    )


@pytest.mark.parametrize(
    "expression",
    [
        po.EqExpr,
        po.NeqExpr,
        po.GtExpr,
        po.GeqExpr,
        po.LtExpr,
        po.LeqExpr,
        po.AddExpr,
        po.SubExpr,
        po.MulExpr,
        po.DivExpr,
    ],
)
def test_expr_empty_r_value(expression, make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            expression(
                po.BoolExpr(True),
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="r_value was evaluated to None, value expected",
    )


@pytest.mark.parametrize(
    "expression",
    [
        po.EqExpr,
        po.NeqExpr,
        po.GtExpr,
        po.GeqExpr,
        po.LtExpr,
        po.LeqExpr,
        po.AddExpr,
        po.SubExpr,
        po.MulExpr,
        po.DivExpr,
    ],
)
def test_expr_empty_l_value(expression, make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            expression(
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                po.IntExpr(1),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="l_value was evaluated to None, value expected",
    )


def test_eq_expr_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(po.EqExpr(po.IntExpr(5), po.StringExpr("5"), pos=(1, 1)))

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '==' operation - got 'Int' and 'String'",
    )


def test_neq_expr_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(po.NeqExpr(po.IntExpr(5), po.StringExpr("5"), pos=(1, 1)))

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '!=' operation - got 'Int' and 'String'",
    )


def test_gt_expr_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(po.GtExpr(po.IntExpr(5), po.StringExpr("5"), pos=(1, 1)))

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '>' operation - got 'Int' and 'String'",
    )


def test_gt_expr_unsupported_type(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.GtExpr(
                po.ListExpr([]),
                po.ListExpr([po.IntExpr(1), po.IntExpr(2), po.IntExpr(3)]),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Operation '>' not supported for type 'List'",
    )


def test_geq_expr_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(po.GeqExpr(po.IntExpr(5), po.StringExpr("5"), pos=(1, 1)))

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '>=' operation - got 'Int' and 'String'",
    )


def test_geq_expr_unsupported_type(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.GeqExpr(
                po.ListExpr([]),
                po.ListExpr([po.IntExpr(1), po.IntExpr(2), po.IntExpr(3)]),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Operation '>=' not supported for type 'List'",
    )


def test_lt_expr_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(po.LtExpr(po.IntExpr(5), po.StringExpr("5"), pos=(1, 1)))

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '<' operation - got 'Int' and 'String'",
    )


def test_lt_expr_unsupported_type(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.LtExpr(
                po.ListExpr([]),
                po.ListExpr([po.IntExpr(1), po.IntExpr(2), po.IntExpr(3)]),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Operation '<' not supported for type 'List'",
    )


def test_leq_expr_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(po.LeqExpr(po.IntExpr(5), po.StringExpr("5"), pos=(1, 1)))

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '<=' operation - got 'Int' and 'String'",
    )


def test_leq_expr_unsupported_type(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.LeqExpr(
                po.ListExpr([]),
                po.ListExpr([po.IntExpr(1), po.IntExpr(2), po.IntExpr(3)]),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Operation '<=' not supported for type 'List'",
    )


def test_add_expr_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.AddExpr(
                po.IntExpr(5),
                po.StringExpr("5"),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '+' operation - got 'Int' and 'String'",
    )


def test_add_expr_unsupported_type(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.AddExpr(
                po.ItemExpr(po.IntExpr(1), po.IntExpr(1)),
                po.ItemExpr(po.IntExpr(1), po.IntExpr(1)),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Operation '+' not supported for type 'Item'",
    )


def test_sub_expr_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.SubExpr(
                po.IntExpr(5),
                po.StringExpr("5"),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '-' operation - got 'Int' and 'String'",
    )


def test_sub_expr_unsupported_type(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.SubExpr(
                po.ItemExpr(po.IntExpr(1), po.IntExpr(1)),
                po.ItemExpr(po.IntExpr(1), po.IntExpr(1)),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Operation '-' not supported for type 'Item'",
    )


def test_mul_expr_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.MulExpr(
                po.IntExpr(5),
                po.StringExpr("5"),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '*' operation - got 'Int' and 'String'",
    )


def test_mul_expr_unsupported_type(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.MulExpr(
                po.ItemExpr(po.IntExpr(1), po.IntExpr(1)),
                po.ItemExpr(po.IntExpr(1), po.IntExpr(1)),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Operation '*' not supported for type 'Item'",
    )


def test_div_expr_type_missmatch(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.DivExpr(
                po.IntExpr(5),
                po.StringExpr("5"),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Type missmatch in '/' operation - got 'Int' and 'String'",
    )


def test_div_expr_unsupported_type(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.DivExpr(
                po.StringExpr("hi"),
                po.StringExpr("there"),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Operation '/' not supported for type 'String'",
    )


def test_div_expr_zero_division_int(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.DivExpr(
                po.IntExpr(5),
                po.SubExpr(po.IntExpr(5), po.IntExpr(5)),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Division by zero is not allowed",
    )


def test_div_expr_zero_division_float(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.DivExpr(
                po.FloatExpr(5.0),
                po.FloatExpr(0.0),
                pos=(1, 1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (1, 1),
        msg="Division by zero is not allowed",
    )


def test_logic_neg_not_bool(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(po.LogicNegExpr(po.FunctionExpr([], None), pos=(4, 7)))

    check_error(
        mocked_error_handler,
        RuntimeException,
        (4, 7),
        msg="Operation '!' not supported for type 'Function'",
    )


def test_logic_neg_none_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.LogicNegExpr(
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Value to negate was evaluated to None, value expected",
    )


def test_arith_neg_not_bool(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(po.ArithNegExpr(po.DictExpr([]), pos=(4, 7)))

    check_error(
        mocked_error_handler,
        RuntimeException,
        (4, 7),
        msg="Operation '-' not supported for type 'Dict'",
    )


def test_arith_neg_none_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.ArithNegExpr(
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Value to negate was evaluated to None, value expected",
    )


def test_access_expr_not_existing(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("x", io.IntValue(10))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.AccessExpr(
                po.Identifier("x"), po.Identifier("notExistingMember"), pos=(10, 2)
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (10, 2),
        msg="Object of type 'Int' has no 'notExistingMember' member",
    )


def test_access_expr_none_source(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.AccessExpr(
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                po.Identifier("Hi"),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Access owner was evaluated to None, value expected",
    )


def test_call_function_not_func(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.call_function(io.IntValue(5), [], call_pos=(5, 2))

    check_error(
        mocked_error_handler,
        RuntimeException,
        (5, 2),
        msg="Object 'Int' is not a function",
    )


def test_call_expr_none_func(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.CallExpr(
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                [],
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Function was evaluated to None, value expected",
    )


def test_dict_expr_duplicated_keys(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.DictExpr(
                [
                    po.ItemExpr(po.IntExpr(1), po.StringExpr("val")),
                    po.ItemExpr(po.IntExpr(1, pos=(3, 18)), po.StringExpr("another")),
                ]
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (3, 18),
        msg="Item with key '1' already exists in dictionary",
    )


def test_func_expr_duplicated_params(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.FunctionExpr(
                [
                    po.Identifier("arg1"),
                    po.Identifier("arg2"),
                    po.Identifier("arg1", pos=(6, 8)),
                ],
                None,
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (6, 8),
        msg="Param 'arg1' already defined",
    )


def test_list_expr_none_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.ListExpr(
                [
                    po.IntExpr(1),
                    po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                ]
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="List element was evaluated to None, value expected",
    )


def test_item_expr_none_key(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.ItemExpr(
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                po.IntExpr(1),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Item key was evaluated to None, value expected",
    )


def test_item_expr_none_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.ItemExpr(
                po.IntExpr(1),
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Item value was evaluated to None, value expected",
    )


def test_dict_expr_none_item(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.DictExpr(
                [
                    po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                ]
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Item was evaluated to None, value expected",
    )


def test_linq_expr_none_source(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.LinqExpr(
                po.Identifier("hello"),
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                [],
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Source was evaluated to None, value expected",
    )


def test_linq_expr_none_condition(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.LinqExpr(
                po.Identifier("hello"),
                po.ListExpr([po.IntExpr(1)]),
                [],
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Condition was evaluated to None, value expected",
    )


def test_linq_expr_none_select(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.LinqExpr(
                po.Identifier("hello"),
                po.ListExpr([po.IntExpr(1)]),
                [
                    po.IntExpr(1),
                    po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                ],
                po.BoolExpr(True),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Selected value was evaluated to None, value expected",
    )


def test_linq_expr_none_order_by(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.LinqExpr(
                po.Identifier("hello"),
                po.ListExpr([po.IntExpr(1)]),
                [po.IntExpr(1)],
                po.BoolExpr(True),
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Order key was evaluated to None, value expected",
    )


def test_linq_expr_not_collection(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.LinqExpr(
                po.Identifier("x"),
                po.IntExpr(5, pos=(12, 21)),
                [],
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (12, 21),
        msg="Source should be a collection, got 'Int'",
    )


def test_linq_expr_where_not_bool(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.LinqExpr(
                var=po.Identifier("x"),
                source=po.ListExpr([po.IntExpr(5)]),
                selects=[],
                where=po.ListExpr([], pos=(2, 2)),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 2),
        msg="'where' condition should be a Bool, got 'List'",
    )


def test_linq_expr_where_comparing_error(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter()

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.LinqExpr(
                var=po.Identifier("x"),
                source=po.ListExpr([po.ListExpr([])]),
                selects=po.Identifier("x"),
                where=po.LtExpr(po.ListExpr([]), po.ListExpr([]), pos=(4, 8)),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (4, 8),
        msg="Operation '<' not supported for type 'List'",
    )


def test_brackets_expr_none_value(make_interpreter, mocked_error_handler):
    interpreter = make_interpreter(env=[("func", io.BuiltInFuncValue(lambda _: None))])

    with pytest.raises(AbortExecution):
        interpreter.eval(
            po.BracketsExpr(
                po.CallExpr(po.Identifier("func"), args=[], pos=(2, 3)),
                pos=(1, 5),
            )
        )

    check_error(
        mocked_error_handler,
        RuntimeException,
        (2, 3),
        msg="Value in brackets was evaluated to None, value expected",
    )
