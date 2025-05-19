from src.interpreter.interpreter_objects import (
    Value,
    Env,
    BuiltInFuncValue,
    Cell,
    UserFuncValue,
    DictValue,
)
from src.parser.parser_objects import ReturnStmt


def get_typeof(value: Value):
    try:
        return value.type_of()
    except AttributeError:
        raise AttributeError(
            f"Object {value.__class__.__qualname__} does not have type_of method"
        )


def get_dict(func_value: Value):
    return DictValue([], func_value)


GLOBAL_ENV = Env(
    "main",
    None,
    {
        "print": Cell(
            BuiltInFuncValue(
                [
                    [Value],
                    [Value, Value],
                    [Value, Value, Value],
                    [Value, Value, Value, Value],
                    [Value, Value, Value, Value, Value],
                    [Value, Value, Value, Value, Value, Value],
                    [Value, Value, Value, Value, Value, Value, Value],
                    [Value, Value, Value, Value, Value, Value, Value, Value],
                    [Value, Value, Value, Value, Value, Value, Value, Value, Value],
                    [
                        Value,
                        Value,
                        Value,
                        Value,
                        Value,
                        Value,
                        Value,
                        Value,
                        Value,
                        Value,
                    ],
                ],
                lambda *args: print(*args),
            )
        ),
        "typeOf": Cell(
            BuiltInFuncValue("typeof", [[Value]], lambda _, __, val: get_typeof(val))
        ),
        "Dict": Cell(
            BuiltInFuncValue("Dict", [[UserFuncValue]], lambda _, __, func: get_dict(func))
        ),
    },
)


def get_operation_unsupported_type_msg(value: Value, operation: str):
    return f"Operation '{operation}' not supported for type '{value.type_of()}'"
