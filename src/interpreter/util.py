from src.interpreter.interpreter_objects import Value, Env, BuiltInFunc
from src.parser.parser_objects import ReturnStmt


def get_typeof(value: Value):
    try:
        return value.type_of()
    except AttributeError:
        raise AttributeError(
            f"Object {value.__class__.__qualname__} does not have type_of method"
        )


class ReturnSignal(Exception):
    def __init__(self, statement: ReturnStmt, return_value: Value | None = None):
        self.return_statement = statement
        self.return_value = return_value
        super().__init__(f"Return signal with {self.return_value}")


GLOBAL_ENV = Env(
    None,
    {
        "print": BuiltInFunc(
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
                [Value, Value, Value, Value, Value, Value, Value, Value, Value, Value],
            ],
            print,
        ),
        "typeOf": BuiltInFunc("typeof", [[Value]], get_typeof),
    },
)
