from src.interpreter.interpreter_objects import ItemValue, IntValue, BuiltInFuncValue


def default_sort() -> BuiltInFuncValue:
    return BuiltInFuncValue("default_sort", [[ItemValue, ItemValue]], lambda *_: IntValue(1))
