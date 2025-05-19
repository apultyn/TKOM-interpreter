from src.interpreter.interpreter_objects import ItemValue, IntValue, BuiltInFuncValue


def get_default_sort() -> BuiltInFuncValue:
    return BuiltInFuncValue([[ItemValue, ItemValue]], lambda *_: IntValue(1))
