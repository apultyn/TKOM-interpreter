from src.interpreter.interpreter_objects import ItemValue, IntValue


def default_sort(item1: ItemValue, item2: ItemValue) -> int:
    return IntValue(1)
