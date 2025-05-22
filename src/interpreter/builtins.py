from functools import wraps

from src.interpreter.interpreter_objects import (
    Value,
    Env,
    BuiltInFuncValue,
    Cell,
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
                word = "argument" if len(args) == 1 else "arguments"
                raise RuntimeException(
                    f"Function '{public_name}' requires {arity} {word}, got {len(args)}",
                    env,
                )
            return fn(env, *args)

        wrapper.__builtin_public_name__ = public_name
        return BuiltInFuncValue(wrapper)

    return decorator


def method(
    *,
    of: type[Value],
    name: str | None = None,
    arity: int = 0,
    needs_inter: bool = False,
):
    def decorator(fn):
        public_name = name or fn.__name__

        @wraps(fn)
        def wrapper(owner, env, *args):
            if not isinstance(owner, of):
                raise RuntimeException(
                    f"Type '{owner.type_of()}' has no '{public_name}' function",
                    env.parent,
                )

            env.context = f"'{owner.type_of()}.{public_name}' builtin function"

            if len(args) != arity:
                word = "argument" if len(args) == 1 else "arguments"
                raise RuntimeException(
                    f"Function '{public_name}' requires {arity} {word}, got {len(args)}",
                    env,
                )
            return fn(owner, env, *args)

        wrapper.__builtin_key__ = f"{of.__name__}.{public_name}"
        return AccessedFuncValue(wrapper, needs_inter)

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


@method(of=IntValue)
def toString(owner, env):
    return owner.to_string()


@method(of=IntValue)
def toFloat(owner, env):
    return owner.to_float()


@method(of=FloatValue)
def toString(owner, env):
    return owner.to_string()


@method(of=FloatValue)
def toInt(owner, env):
    return owner.to_int()


@method(of=StringValue)
def length(owner, env):
    return owner.length()


@method(of=StringValue)
def toInt(owner, env):
    try:
        return owner.to_int()
    except ValueError as exc:
        raise RuntimeException(exc.args[0], env)


@method(of=StringValue)
def toFloat(owner, env):
    try:
        return owner.to_float()
    except ValueError as exc:
        raise RuntimeException(exc.args[0], env)


@method(of=ItemValue)
def key(owner, env):
    return owner.get_key()


@method(of=ItemValue)
def value(owner, env):
    return owner.get_value()


@method(of=ItemValue)
def toString(owner, env):
    return owner.to_string()


@method(of=ListValue)
def length(owner, env):
    return owner.length()


@method(of=ListValue, arity=1)
def get(owner, env, idx):
    if not isinstance(idx, IntValue):
        raise RuntimeException(
            f"Function 'List.get' requires 'Int' type argument, got '{idx.type_of()}'",
            env,
        )
    try:
        return owner.get(idx)
    except IndexError as exc:
        raise RuntimeException(
            exc.args[0],
            env
        )

@method(of=ListValue, arity=1)
def add(owner, env, value):
    if not isinstance(value, )