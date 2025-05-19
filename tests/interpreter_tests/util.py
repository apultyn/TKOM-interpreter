from src.interpreter.interpreter_objects import ItemValue, IntValue, BuiltInFunc


def default_sort() -> BuiltInFunc:
    return BuiltInFunc("default_sort", [[ItemValue, ItemValue]], lambda *_: IntValue(1))
