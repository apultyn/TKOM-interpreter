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


def check_args_length(args, expected_length: int, func_name: str, env: Env):
    if len(args) != expected_length:
        word = "argument" if len(args) == 1 else "arguments"
        raise RuntimeException(
            f"Function '{func_name}' requires {expected_length} {word}, got {len(args)}",
            env,
        )


def get_typeof(env: Env, args):
    env.context = "'typeOf' builtin function"
    check_args_length(args, 1, "typeOf", env)
    return args[0].type_of()


def get_no_arg_func(object: Value, env: Env, func_name: str, args):
    env.context = f"'{func_name}' builtin function"
    check_args_length(args, 0, func_name, env)

    snake_case = re.sub(r"([a-z])([A-Z])", r"\1_\2", func_name).lower()
    func = getattr(object, snake_case, None)
    if func is None:
        raise RuntimeException(
            f"Object of type '{object.__class__.__qualname__} has no {snake_case} method",
            env,
        )

    return func()


def get_dict(env: Env, args):
    env.context = "'Dict' builtin function"
    if len(args) not in [0, 1]:
        raise RuntimeException(
            f"Function 'Dict' requires 0 or 1 argument, got {len(args)}", env
        )
    func = DEFAULT_SORT
    if len(args) == 1:
        func = args[0]
        if not isinstance(func, FuncValue):
            raise RuntimeException(
                f"Dict constructor requires 'Function' type argument, got '{func.type_of()}'",
                env,
            )
    return DictValue(order_func=func)


def add_new_to_dict(call_method, env: Env, dict_value: DictValue, args):
    env.context = "'add' builtin function"
    check_args_length(args, 2, "addNew", env)

    item = ItemValue(args[0], args[1])
    add_to_dict(call_method, env, dict_value, item)


def add_item_to_dict(call_method, env: Env, dict_value: DictValue, args):
    env.context = "'addNew' builtin function"
    check_args_length(args, 1, "add", env)

    item = args[0]
    if not isinstance(item, ItemValue):
        raise RuntimeException(
            f"Function 'add' requires 'Item' type argument, got '{item.type_of()}'", env
        )
    add_to_dict(call_method, env, dict_value, args[0])


def add_to_dict(call_method, env: Env, dict_value: DictValue, new_item: ItemValue):
    try:
        dict_value.check_add(new_item)
    except KeyError as exc:
        raise RuntimeException(exc.args[0], env)

    for i, existing_item in enumerate(dict_value.elements):
        soring_val = call_method(dict_value.order_func, [new_item, existing_item], env)

        if not isinstance(soring_val, IntValue):
            raise RuntimeException(
                f"Sorting function should return 'Int', got '{soring_val.type_of()}'",
                env,
            )

        if soring_val < IntValue(0):
            dict_value.elements.insert(i, new_item)
            return
    dict_value.elements.append(new_item)


def list_get(list: ListValue, env: Env, args):
    env.context = "'List.get' builtin function"
    check_args_length(args, 1, "get", env)

    idx = args[0]
    if not isinstance(idx, IntValue):
        raise RuntimeException(
            f"Function 'get' requires 'Int' type argument, got '{idx.type_of()}'", env
        )

    return list.get(idx)


def dict_get(dict: DictValue, env: Env, args):
    env.context = "'Dict.get' builtin function"
    check_args_length(args, 1, "get", env)
    key = args[0]

    return dict.get(key)


def list_set(list: ListValue, env: Env, args):
    env.context = "'List.set' builtin function"
    check_args_length(args, 2, "set", env)

    idx, val = args
    if not isinstance(idx, IntValue):
        raise RuntimeException(
            f"Index param should be an 'Int', got '{idx.type_of()}'", env
        )

    list.set(idx, val)


def list_add(list: ListValue, env: Env, args):
    env.context = "'List.add' builtin function"
    check_args_length(args, 1, "add", env)

    list.add(args[0])


def list_remove(list: ListValue, env: Env, args):
    env.context = "'List.remove' builtin function"
    check_args_length(args, 1, "remove", env)

    idx = args[0]
    if not isinstance(idx, IntValue):
        raise RuntimeException(
            f"Index param should be an 'Int', got '{idx.type_of()}'", env
        )

    list.remove(idx)


def dict_remove(dict: DictValue, env: Env, args):
    env.context = "'Dict.remove' builtin function"
    check_args_length(args, 1, "remove", env)

    dict.remove(args[0])


def dict_contains(dict: DictValue, env: Env, args):
    env.context = "'Dict.contains' builtin function"
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
    "Main",
    None,
    {
        "print": Cell(
            BuiltInFuncValue(
                lambda _, *args: print_args(args),
            )
        ),
        "typeOf": Cell(BuiltInFuncValue(lambda env, *args: get_typeof(env, args))),
        "Dict": Cell(BuiltInFuncValue(lambda env, *args: get_dict(env, args))),
        "IntValue.toString": Cell(
            AccessedFuncValue(
                lambda int_value, env, *args: get_no_arg_func(
                    int_value, env, "toString", args
                )
            )
        ),
        "IntValue.toFloat": Cell(
            AccessedFuncValue(
                lambda int_value, env, *args: get_no_arg_func(
                    int_value, env, "toFloat", args
                )
            )
        ),
        "FloatValue.toString": Cell(
            AccessedFuncValue(
                lambda float_value, env, *args: get_no_arg_func(
                    float_value, env, "toString", args
                )
            )
        ),
        "FloatValue.toInt": Cell(
            AccessedFuncValue(
                lambda float_value, env, *args: get_no_arg_func(
                    float_value, env, "toInt", args
                )
            )
        ),
        "StringValue.length": Cell(
            AccessedFuncValue(
                lambda string_value, env, *args: get_no_arg_func(
                    string_value, env, "length", args
                )
            )
        ),
        "StringValue.toInt": Cell(
            AccessedFuncValue(
                lambda string_value, env, *args: get_no_arg_func(
                    string_value, env, "toInt", args
                )
            )
        ),
        "StringValue.toFloat": Cell(
            AccessedFuncValue(
                lambda str_value, env, *args: get_no_arg_func(
                    str_value, env, "toFloat", args
                )
            )
        ),
        "ItemValue.toString": Cell(
            AccessedFuncValue(
                lambda item_value, env, *args: get_no_arg_func(
                    item_value, env, "toString", args
                )
            )
        ),
        "ItemValue.key": Cell(
            AccessedFuncValue(
                lambda item_value, env, *args: get_no_arg_func(
                    item_value, env, "getKey", args
                )
            ),
        ),
        "ItemValue.value": Cell(
            AccessedFuncValue(
                lambda item_value, env, *args: get_no_arg_func(
                    item_value, env, "getValue", args
                )
            ),
        ),
        "ListValue.length": Cell(
            AccessedFuncValue(
                lambda list_value, env, *args: get_no_arg_func(
                    list_value, env, "length", args
                )
            ),
        ),
        "ListValue.get": Cell(
            AccessedFuncValue(
                lambda list_value, env, *args: list_get(list_value, env, args)
            ),
        ),
        "ListValue.add": Cell(
            AccessedFuncValue(
                lambda list_value, env, *args: list_add(list_value, env, args)
            ),
        ),
        "ListValue.set": Cell(
            AccessedFuncValue(
                lambda list_value, env, *args: list_set(list_value, env, args),
            ),
        ),
        "ListValue.remove": Cell(
            AccessedFuncValue(
                lambda list_value, env, *args: list_remove(list_value, env, args)
            ),
        ),
        "ListValue.copy": Cell(
            AccessedFuncValue(
                lambda list_value, env, *args: get_no_arg_func(
                    list_value, env, "copy", args
                )
            )
        ),
        "ListValue.toString": Cell(
            AccessedFuncValue(
                lambda list_value, env, *args: get_no_arg_func(
                    list_value, env, "toString", args
                )
            ),
        ),
        "DictValue.length": Cell(
            AccessedFuncValue(
                lambda dict_value, env, *args: get_no_arg_func(
                    dict_value, env, "length", args
                )
            ),
        ),
        "DictValue.get": Cell(
            AccessedFuncValue(
                lambda dict_value, env, *args: dict_get(dict_value, env, args)
            ),
        ),
        "DictValue.remove": Cell(
            AccessedFuncValue(
                lambda dict_value, env, *args: dict_remove(dict_value, env, args)
            ),
        ),
        "DictValue.contains": Cell(
            AccessedFuncValue(
                lambda dict_value, env, *args: dict_contains(dict_value, env, args)
            ),
        ),
        "DictValue.copy": Cell(
            AccessedFuncValue(
                lambda dict_value, env, *args: get_no_arg_func(
                    dict_value, env, "copy", args
                )
            )
        ),
        "DictValue.toString": Cell(
            AccessedFuncValue(
                lambda dict_value, env, *args: get_no_arg_func(
                    dict_value, env, "toString", args
                )
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
