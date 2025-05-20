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


def test_all(make_parser, make_interpreter, mocked_error_handler):
    parser = make_parser(
        """my_list = [1, 2, 3, 4, 5];

func = function(arg) {
    for elem in arg {
        elem += 1;
    }
};

func(my_list);
print(my_list);

""",
        err=mocked_error_handler,
    )
    interpreter = make_interpreter(err=mocked_error_handler)
    program = parser.parse_program()

    interpreter.eval(program)
