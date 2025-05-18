from src.interpreter.interpreter_objects import (
    Value,
    Env,
    BuiltInFunc,
    Cell,
    FuncValue,
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


class ReturnSignal(Exception):
    def __init__(self, statement: ReturnStmt, return_value: Value | None = None):
        self.return_statement = statement
        self.return_value = return_value
        super().__init__(f"Return signal with {self.return_value}")


GLOBAL_ENV = Env(
    None,
    {
        "print": Cell(
            BuiltInFunc(
                "print",
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
                print,
            )
        ),
        "typeOf": Cell(BuiltInFunc("typeof", [[Value]], get_typeof)),
        "Dict": Cell(BuiltInFunc("Dict", [[FuncValue]], get_dict)),
    },
)


def get_operation_unsupported_type_msg(value: Value, operation: str):
    return f"Operation '{operation}' not supported for type '{value.type_of()}'"
