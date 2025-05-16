import pytest

from src.parser.parser_objects import CallExpr, AccessExpr, Identifier, IntExpr

from src.interpreter.interpreter_objects import StringValue


def test_int(make_interpreter):
    interpreter = make_interpreter()

    assert interpreter.eval(
        CallExpr(
            AccessExpr(
                IntExpr(5, pos=(1, 1)), Identifier("toString", pos=(1, 3)), pos=(1, 5)
            ),
            args=[],
            pos=(1, 2),
        ),
        interpreter.global_env,
    ) == StringValue("5")
