from src.interpreter import builtins as _builtins_mod
from inspect import getmembers

from src.interpreter.interpreter_objects import (
    Value,
    BuiltInFuncValue,
    IntValue,
    Cell,
    Env,
)

DEFAULT_SORT = BuiltInFuncValue(lambda _, __, ___: IntValue(1))


def get_operation_unsupported_type_msg(value: Value, operation: str):
    return f"Operation '{operation}' not supported for type '{value.type_of()}'"


def gather_builtins():
    symbols = {}
    print(_builtins_mod)
    for _, obj in getmembers(_builtins_mod):
        if hasattr(obj, "__builtin_key__"):
            symbols[obj.__builtin_key__] = Cell(obj)
    return symbols


global_env = Env("Main", None, gather_builtins())
