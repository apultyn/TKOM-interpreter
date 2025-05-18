import pytest

import src.interpreter.interpreter_objects as io
import src.parser.parser_objects as po

from src.util.pyscript_exceptions import RuntimeException
from tests.util import AbortExecution, check_error


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
