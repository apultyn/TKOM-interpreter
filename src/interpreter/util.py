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
    ListValue,
)

from src.util.pyscript_exceptions import RuntimeException


DEFAULT_SORT = BuiltInFuncValue(lambda _, __: IntValue(1))


def check_args_length(args, expected_length: int, func_name: str):
    if len(args) != expected_length:
        word = "argument" if len(args) == 1 else "arguments"
        raise RuntimeException(
            f"Function '{func_name}' requires {expected_length} {word}, got {len(args)}"
        )


def get_typeof(args):
    check_args_length(args, 1, "typeOf")
    return args[0].type_of()


def get_no_arg_func(object: Value, func_name: str, args):
    check_args_length(args, 0, func_name)

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
    func = DEFAULT_SORT
    if len(args) == 1:
        func = args[0]
        if not isinstance(func, FuncValue):
            raise RuntimeException(
                f"Dict constructor requires 'Function' type argument, got '{func.type_of()}'"
            )
    return DictValue(order_func=func)


def add_new_to_dict(call_method, env: Env, dict_value: DictValue, args):
    check_args_length(args, 2, "addNew")

    item = ItemValue(args[0], args[1])
    add_to_dict(call_method, env, dict_value, item)


def add_item_to_dict(call_method, env: Env, dict_value: DictValue, args):
    check_args_length(args, 1, "add")

    item = args[0]
    if not isinstance(item, ItemValue):
        raise RuntimeException(
            f"Function 'add' requires 'Item' type argument, got {item.type_of()}"
        )
    add_to_dict(call_method, env, dict_value, args[0])


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


def list_get(list: ListValue, args):
    check_args_length(args, 1, "get")

    idx = args[0]
    if not isinstance(idx, IntValue):
        raise RuntimeException(
            f"Function 'get' requires 'Int' type argument, got {idx.type_of()}"
        )

    return list.get(idx)


def dict_get(dict: DictValue, args):
    check_args_length(args, 1, "get")
    key = args[0]

    return dict.get(key)


def list_set(list: ListValue, args):
    check_args_length(args, 2, "set")

    idx, val = args
    if not isinstance(idx, IntValue):
        raise RuntimeException(f"Index param should be an 'Int', got {idx.type_of()}")

    list.set(idx, val)


def list_add(list: ListValue, args):
    check_args_length(args, 1, "add")

    list.add(args[0])


def list_remove(list: ListValue, args):
    check_args_length(args, 1, "remove")

    idx = args[0]
    if not isinstance(idx, IntValue):
        raise RuntimeException(f"Index param should be an 'Int', got {idx.type_of()}")

    list.remove(idx)


def dict_remove(dict: DictValue, args):
    check_args_length(args, 1, "remove")

    dict.remove(args[0])


def dict_contains(dict: DictValue, args):
    check_args_length(args, 1, "contains")

    return dict.contains(args[0])


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
        "StringValue.length": Cell(
            AccessedFuncValue(
                lambda string_value, *args: get_no_arg_func(
                    string_value, "length", args
                )
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
            AccessedFuncValue(lambda list_value, *args: list_get(list_value, args)),
        ),
        "ListValue.add": Cell(
            AccessedFuncValue(lambda list_value, *args: list_add(list_value, args)),
        ),
        "ListValue.set": Cell(
            AccessedFuncValue(
                lambda list_value, *args: list_set(list_value, args),
            ),
        ),
        "ListValue.remove": Cell(
            AccessedFuncValue(lambda list_value, *args: list_remove(list_value, args)),
        ),
        "ListValue.copy": Cell(
            AccessedFuncValue(
                lambda list_value, *args: get_no_arg_func(list_value, "copy", args)
            )
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
            AccessedFuncValue(lambda dict_value, *args: dict_get(dict_value, args)),
        ),
        "DictValue.remove": Cell(
            AccessedFuncValue(lambda dict_value, *args: dict_remove(dict_value, args)),
        ),
        "DictValue.contains": Cell(
            AccessedFuncValue(
                lambda dict_value, *args: dict_contains(dict_value, args)
            ),
        ),
        "DictValue.copy": Cell(
            AccessedFuncValue(
                lambda dict_value, *args: get_no_arg_func(dict_value, "copy", args)
            )
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
