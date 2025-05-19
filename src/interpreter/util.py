from src.interpreter.interpreter_objects import (
    Value,
    Env,
    BuiltInFuncValue,
    Cell,
    AccessedFuncValue,
    DictValue,
    UserFuncValue,
    IntValue,
    ItemValue,
)

from src.util.pyscript_exceptions import RuntimeException


def add_to_dict(
    call_method, env: Env, dict_value: DictValue, new_item: ItemValue
) -> Value:
    try:
        dict_value.check_add(new_item)
    except KeyError as exc:
        raise RuntimeException(exc.args[0])

    for i, existing_item in enumerate(dict_value.elements):
        soring_val = call_method(dict_value.order_func, [new_item, existing_item], env)

        if not isinstance(soring_val, IntValue):
            raise RuntimeException(
                f"Sorting function should return 'Int', got {soring_val.type_of()}"
            )

        if soring_val < IntValue(0):
            dict_value.elements.insert(i, new_item)
    dict_value.elements.append(new_item)


GLOBAL_ENV = Env(
    None,
    "main",
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
                print,
            )
        ),
        "typeOf": Cell(BuiltInFuncValue([[Value]], lambda val: val.type_of())),
        "Dict": Cell(
            BuiltInFuncValue([[UserFuncValue]], lambda func: DictValue(order_func=func))
        ),
        "IntValue.toString": Cell(
            AccessedFuncValue([[]], lambda int_value: int_value.to_string())
        ),
        "IntValue.toFloat": Cell(
            AccessedFuncValue([[]], lambda int_value: int_value.to_float())
        ),
        "FloatValue.toString": Cell(
            AccessedFuncValue([[]], lambda float_value: float_value.to_string())
        ),
        "FloatValue.toInt": Cell(
            AccessedFuncValue([[]], lambda float_value: float_value.to_int())
        ),
        "StringValue.toInt": Cell(
            AccessedFuncValue([[]], lambda str_value: str_value.to_int())
        ),
        "StringValue.toFloat": Cell(
            AccessedFuncValue([[]], lambda str_value: str_value.to_float())
        ),
        "ItemValue.toString": Cell(
            AccessedFuncValue([[]], lambda item_value: item_value.to_string())
        ),
        "ItemValue.key": Cell(
            AccessedFuncValue([[]], lambda item_value: item_value.get_key()),
        ),
        "ItemValue.value": Cell(
            AccessedFuncValue([[]], lambda item_value: item_value.get_value()),
        ),
        "ListValue.length": Cell(
            AccessedFuncValue([[]], lambda list_value: list_value.length()),
        ),
        "ListValue.get": Cell(
            AccessedFuncValue([Value], lambda list_value, index: list_value.get(index)),
        ),
        "ListValue.set": Cell(
            AccessedFuncValue(
                [[IntValue, Value]],
                lambda list_value, index, value: list_value.set(index, value),
            ),
        ),
        "ListValue.add": Cell(
            AccessedFuncValue(
                [[Value]], lambda list_value, value: list_value.add(value)
            ),
        ),
        "ListValue.remove": Cell(
            AccessedFuncValue(
                [[IntValue]], lambda list_value, index: list_value.remove(index)
            ),
        ),
        "ListValue.toString": Cell(
            AccessedFuncValue([[]], lambda list_value: list_value.to_string()),
        ),
        "DictValue.length": Cell(
            AccessedFuncValue([[]], lambda dict_value: dict_value.length()),
        ),
        "DictValue.get": Cell(
            AccessedFuncValue([Value], lambda dict_value, key: dict_value.get(key)),
        ),
        "DictValue.contains": Cell(
            AccessedFuncValue(
                [[Value]], lambda dict_value, key: dict_value.contains(key)
            ),
        ),
        "DictValue.remove": Cell(
            AccessedFuncValue(
                [[Value]], lambda dict_value, key: dict_value.remove(key)
            ),
        ),
        "DictValue.toString": Cell(
            AccessedFuncValue([[]], lambda dict_value: dict_value.to_string()),
        ),
        "DictValue.addNew": Cell(
            AccessedFuncValue(
                [[Value, Value]],
                lambda call_method, env, dict_value, key, value: add_to_dict(
                    call_method, env, dict_value, ItemValue(key, value)
                ),
                True,
            )
        ),
        "DictValue.add": Cell(
            AccessedFuncValue(
                [[ItemValue]],
                lambda method, env, dict_value, item_value: add_to_dict(
                    method, env, dict_value, item_value
                ),
                True,
            )
        ),
    },
)


def get_operation_unsupported_type_msg(value: Value, operation: str):
    return f"Operation '{operation}' not supported for type '{value.type_of()}'"
