from functools import wraps

from src.interpreter.interpreter_objects import (
    Value,
    BuiltInFuncValue,
    AccessedFuncValue,
    DictValue,
    FuncValue,
    IntValue,
    FloatValue,
    StringValue,
    ItemValue,
    Collection,
    ListValue,
)
from src.util.pyscript_exceptions import RuntimeException


def builtin(name: str, *, arity: int | None = None):
    def decorator(fn):
        public_name = name or fn.__name__

        @wraps(fn)
        def wrapper(env, *args):
            env.context = f"'{public_name}' builtin function"
            if arity is not None and len(args) != arity:
                word = "argument" if arity == 1 else "arguments"
                raise RuntimeException(
                    f"Function '{public_name}' requires {arity} {word}, got {len(args)}",
                    env,
                )
            return fn(env, *args)

        wrapper.__builtin_key__ = public_name
        value_obj = BuiltInFuncValue(wrapper)
        value_obj.__builtin_key__ = wrapper.__builtin_key__
        return value_obj

    return decorator


def method(
    *,
    of: type[Value],
    name: str | None = None,
    arity: int = 0,
    types: list[type[Value]] = [],
    needs_inter: bool = False,
):
    def decorator(fn):
        public_name = name or fn.__name__

        @wraps(fn)
        def wrapper(owner, env, *args):
            if len(types) != arity:
                raise NotImplementedError("Wrong builtin func definition")

            if not isinstance(owner, of):
                raise RuntimeException(
                    f"Type '{owner.type_of()}' has no '{public_name}' function",
                    env.parent,
                )

            env.context = f"'{owner.type_of()}.{public_name}' builtin function"

            if needs_inter:
                call_func = args[0]
                args = args[1:]

            if len(args) != arity:
                word = "argument" if arity == 1 else "arguments"
                raise RuntimeException(
                    f"Function '{public_name}' requires {arity} {word}, got {len(args)}",
                    env,
                )

            for i, (arg, type) in enumerate(zip(args, types)):
                if not isinstance(arg, type):
                    raise RuntimeException(
                        f"Param {i+1} of function'{owner.type_of()}.{public_name}' should be '{type.TYPE_NAME}', got '{arg.type_of()}'"
                    )
            if needs_inter:
                return fn(call_func, owner, env, *args)
            else:
                return fn(owner, env, *args)

        wrapper.__builtin_key__ = f"{of.TYPE_NAME}.{public_name}"
        value_obj = AccessedFuncValue(wrapper, needs_inter)
        value_obj.__builtin_key__ = wrapper.__builtin_key__
        return value_obj

    return decorator


@builtin("print")
def _print(env, *args):
    def stringify(x):
        return x.str_long() if isinstance(x, Collection) else str(x)

    print(*(stringify(a) for a in args))


@builtin("typeOf", arity=1)
def _typeof(env, value):
    return value.type_of()


@builtin("Dict", arity=1)
def _Dict(env, func):
    if not isinstance(func, FuncValue):
        raise RuntimeException(
            f"Dict constructor requires 'Function' type argument, got '{func.type_of()}'",
            env,
        )
    return DictValue(order_func=func)


@method(of=IntValue, name="toString")
def int_to_string(owner, env):
    return owner.to_string()


@method(of=IntValue, name="toFloat")
def int_to_float(owner, env):
    return owner.to_float()


@method(of=FloatValue, name="toString")
def float_to_string(owner, env):
    return owner.to_string()


@method(of=FloatValue, name="toInt")
def float_to_int(owner, env):
    return owner.to_int()


@method(of=StringValue, name="length")
def string_length(owner, env):
    return owner.length()


@method(of=StringValue, name="toInt")
def string_to_int(owner, env):
    try:
        return owner.to_int()
    except ValueError as exc:
        raise RuntimeException(exc.args[0], env)


@method(of=StringValue, name="toFloat")
def string_to_float(owner, env):
    try:
        return owner.to_float()
    except ValueError as exc:
        raise RuntimeException(exc.args[0], env)


@method(of=ItemValue, name="key")
def item_key(owner, env):
    return owner.get_key()


@method(of=ItemValue, name="value")
def item_value(owner, env):
    return owner.get_value()


@method(of=ItemValue, name="toString")
def item_to_string(owner, env):
    return owner.to_string()


@method(of=ListValue, name="length")
def list_length(owner, env):
    return owner.length()


@method(of=ListValue, name="get", arity=1, types=[IntValue])
def list_get(owner, env, idx):
    try:
        return owner.get(idx)
    except IndexError as exc:
        raise RuntimeException(exc.args[0], env)


@method(of=ListValue, name="add", arity=1, types=[Value])
def list_add(owner, env, value):
    owner.add(value)


@method(of=ListValue, name="set", arity=2, types=[IntValue, Value])
def list_set(owner, env, idx, value):
    try:
        owner.set(idx, value)
    except IndexError as exc:
        raise RuntimeException(exc.args[0], env)


@method(of=ListValue, name="remove", arity=1, types=[IntValue])
def list_remove(owner, env, idx):
    try:
        owner.remove(idx)
    except IndexError as exc:
        raise RuntimeException(exc.args[0], env)


@method(of=ListValue, name="copy")
def list_copy(owner, env):
    return owner.copy()


@method(of=ListValue, name="toString")
def list_to_string(owner, env):
    return owner.to_string()


@method(of=DictValue, name="get", arity=1, types=[Value])
def dict_get(owner, env, key):
    try:
        return owner.get(key)
    except KeyError as exc:
        raise RuntimeException(exc.args[0], env)


@method(of=DictValue, name="remove", arity=1, types=[Value])
def dict_remove(owner, env, key):
    try:
        owner.remove(key)
    except KeyError as exc:
        raise RuntimeException(exc.args[0], env)


@method(of=DictValue, name="contains", arity=1, types=[Value])
def dict_contains(owner, env, key):
    return owner.contains(key)


@method(of=DictValue, name="copy")
def dict_copy(owner, env):
    return owner.copy()


@method(of=DictValue, name="toString")
def dict_to_string(owner, env):
    return owner.to_string()


def add_item_to_dict(call_func, env, dict: DictValue, new_item: ItemValue):
    try:
        dict.check_add(new_item)
    except KeyError as exc:
        raise RuntimeException(exc.args[0], env)

    for i, existing_item in enumerate(dict.elements):
        soring_val = call_func(dict.order_func, [new_item, existing_item], env)

        if not isinstance(soring_val, IntValue):
            raise RuntimeException(
                f"Sorting function should return 'Int', got '{soring_val.type_of()}'",
                env,
            )

        if soring_val < IntValue(0):
            dict.elements.insert(i, new_item)
            return
    dict.elements.append(new_item)


@method(of=DictValue, name="add", arity=1, types=[ItemValue], needs_inter=True)
def dict_add(func, owner, env, item):
    add_item_to_dict(func, env, owner, item)


@method(of=DictValue, name="addNew", arity=2, types=[Value, Value], needs_inter=True)
def dict_add_new(func, owner, env, key, value):
    add_item_to_dict(func, env, owner, ItemValue(key, value))
