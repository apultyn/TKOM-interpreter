import re

from src.interpreter.interpreter_objects import (
    Value,
    Env,
    BuiltInFuncValue,
    Cell,
    AccessedFuncValue,
    DictValue,
    FuncValue,
    IntValue,
    ItemValue,
    Collection,
)

from src.util.pyscript_exceptions import RuntimeException


def get_typeof(args):
    if len(args) != 1:
        raise RuntimeException(
            f"Function 'typeOf' requires 1 argument, got {len(args)}"
        )
    return args[0].type_of()


def get_no_arg_func(object: Value, func_name: str, args):
    if len(args) != 0:
        raise RuntimeException(
            f"Function 'toString' requires no arguments, got {len(args)}"
        )
    snake_case = re.sub(r"([a-z])([A-Z])", r"\1_\2", func_name).lower()
    func = getattr(object, snake_case, None)
    if func is None:
        raise RuntimeException(
            f"Object of type '{object.__class__.__qualname__} has no {snake_case} method"
        )

    return func()


def get_dict(args):
    if len(args) not in [0, 1]:
        raise RuntimeException(
            f"Function 'Dict' requires 0 or 1 argument, got {len(args)}"
        )
    if len(args) == 1:
        func = args[0]
        if not isinstance(func, FuncValue):
            raise RuntimeException(
                f"Dict constructor requires 'Function' type argument, got '{func.type_of()}'"
            )
        return DictValue(order_func=func)


def add_new_to_dict(call_method, env: Env, dict_value: DictValue, args):
    if len(args) != 2:
        raise RuntimeException(
            f"Function 'addNew' requires 2 arguments, got {len(args)}"
        )

    item = ItemValue(args[0], args[1])
    return add_to_dict(call_method, env, dict_value, item)


def add_item_to_dict(call_method, env: Env, dict_value: DictValue, args):
    if len(args) != 1:
        raise RuntimeException(f"Function 'add' requires no arguments, got {len(args)}")
    item = args[0]
    if not isinstance(item, ItemValue):
        raise RuntimeException(
            f"Function 'add' requires 'Item' type argument, got {item.type_of()}"
        )
    return add_to_dict(call_method, env, dict_value, args[0])


def add_to_dict(call_method, env: Env, dict_value: DictValue, new_item: ItemValue):
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
            return
    dict_value.elements.append(new_item)


def print_args(args):
    modified = []
    for arg in args:
        if isinstance(arg, Collection):
            arg = arg.str_long()
        else:
            arg = str(arg)
        modified.append(arg)
    print(*modified)


GLOBAL_ENV = Env(
    None,
    "main",
    {
        "print": Cell(
            BuiltInFuncValue(
                lambda *args: print_args(args),
            )
        ),
        "typeOf": Cell(BuiltInFuncValue(lambda *args: get_typeof(args))),
        "Dict": Cell(BuiltInFuncValue(lambda *args: get_dict(args))),
        "IntValue.toString": Cell(
            AccessedFuncValue(
                lambda int_value, *args: get_no_arg_func(int_value, "toString", args)
            )
        ),
        "IntValue.toFloat": Cell(
            AccessedFuncValue(
                lambda int_value, *args: get_no_arg_func(int_value, "toFloat", args)
            )
        ),
        "FloatValue.toString": Cell(
            AccessedFuncValue(
                lambda float_value, *args: get_no_arg_func(
                    float_value, "toString", args
                )
            )
        ),
        "FloatValue.toInt": Cell(
            AccessedFuncValue(
                lambda float_value, *args: get_no_arg_func(float_value, "toInt", args)
            )
        ),
        "StringValue.toInt": Cell(
            AccessedFuncValue(
                lambda string_value, *args: get_no_arg_func(string_value, "toInt", args)
            )
        ),
        "StringValue.toFloat": Cell(
            AccessedFuncValue(
                lambda str_value, *args: get_no_arg_func(str_value, "toFloat", args)
            )
        ),
        "ItemValue.toString": Cell(
            AccessedFuncValue(
                lambda item_value, *args: get_no_arg_func(item_value, "toString", args)
            )
        ),
        "ItemValue.key": Cell(
            AccessedFuncValue(
                lambda item_value, *args: get_no_arg_func(item_value, "getKey", args)
            ),
        ),
        "ItemValue.value": Cell(
            AccessedFuncValue(
                lambda item_value, *args: get_no_arg_func(item_value, "getValue", args)
            ),
        ),
        "ListValue.length": Cell(
            AccessedFuncValue(
                lambda list_value, *args: get_no_arg_func(list_value, "length", args)
            ),
        ),
        "ListValue.get": Cell(
            AccessedFuncValue(
                [[Value]], lambda list_value, index: list_value.get(index)
            ),
        ),
        "ListValue.set": Cell(
            AccessedFuncValue(
                lambda list_value, index, value: list_value.set(index, value),
            ),
        ),
        "ListValue.add": Cell(
            AccessedFuncValue(lambda list_value, value: list_value.add(value)),
        ),
        "ListValue.remove": Cell(
            AccessedFuncValue(lambda list_value, index: list_value.remove(index)),
        ),
        "ListValue.toString": Cell(
            AccessedFuncValue(
                lambda list_value, *args: get_no_arg_func(list_value, "toString", args)
            ),
        ),
        "DictValue.length": Cell(
            AccessedFuncValue(
                lambda dict_value, *args: get_no_arg_func(dict_value, "length", args)
            ),
        ),
        "DictValue.get": Cell(
            AccessedFuncValue(lambda dict_value, key: dict_value.get(key)),
        ),
        "DictValue.contains": Cell(
            AccessedFuncValue(lambda dict_value, key: dict_value.contains(key)),
        ),
        "DictValue.remove": Cell(
            AccessedFuncValue(lambda dict_value, key: dict_value.remove(key)),
        ),
        "DictValue.toString": Cell(
            AccessedFuncValue(
                lambda dict_value, *args: get_no_arg_func(dict_value, "toString", args)
            ),
        ),
        "DictValue.addNew": Cell(
            AccessedFuncValue(
                lambda call_method, env, dict_value, *args: add_new_to_dict(
                    call_method, env, dict_value, args
                ),
                True,
            )
        ),
        "DictValue.add": Cell(
            AccessedFuncValue(
                lambda method, env, dict_value, *args: add_item_to_dict(
                    method, env, dict_value, args
                ),
                True,
            )
        ),
    },
)


def get_operation_unsupported_type_msg(value: Value, operation: str):
    return f"Operation '{operation}' not supported for type '{value.type_of()}'"
