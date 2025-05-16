from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Self, Callable
from copy import deepcopy

import src.parser.parser_objects as po
from src.util.pyscript_exceptions import RuntimeException


@dataclass
class Cell:
    value: "Value"


class Env:
    def __init__(
        self, parent: "Env | None" = None, symbols: dict[str, Cell] | None = None
    ):
        self.parent = parent
        self.symbols = symbols if symbols is not None else {}

    def lookup_cell(self, identifier: po.Identifier) -> Cell:
        name = identifier.value
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup_cell(name)
        raise RuntimeException(msg=f"'{name}' is not defined in this scope", pos=identifier.pos)

    def get(self, identifier: po.Identifier) -> "Value":
        return self.lookup_cell(identifier).value

    def set(self, identifier: po.Identifier, val: "Value"):
        self.lookup_cell(identifier).value = val

    def define(self, identifier: po.Identifier, val: "Value"):
        self.symbols[identifier.value] = Cell(val)


class Value(ABC):
    def truthy(self) -> bool:
        return True

    @abstractmethod
    def type_of(self) -> "StringValue":
        pass

    @staticmethod
    def typecheck(lhs: "Value", rhs: "Value", operation: str):
        if lhs.__class__ is not rhs.__class__:
            raise TypeError(
                f"Type missmatch in '{operation}' operation - got {lhs.__class__.__qualname__} and {rhs.__class__.__qualname__}"
            )


@runtime_checkable
class Additive(Protocol):
    @abstractmethod
    def __add__(self: Self, other: Self) -> Self:
        pass


@runtime_checkable
class Subtractive(Protocol):
    @abstractmethod
    def __sub__(self: Self, other: Self) -> Self:
        pass


@runtime_checkable
class Multiplicative(Protocol):
    @abstractmethod
    def __mul__(self: Self, other: Self) -> Self:
        pass


@dataclass
class BuiltInFunc(Value):
    name: str
    params_variants: list[list[type[Value]]]
    body: Callable[..., Value | None]

    def type_of(self) -> "StringValue":
        return StringValue("FuncValue")

    def __call__(self, call_pos: tuple[int, int], call_args: list[Value]):
        selected_variant = None
        for param_variant in self.params_variants:
            if len(call_args) != len(param_variant):
                continue

            for call_arg, param in zip(call_args, param_variant):
                if not isinstance(call_arg, param):
                    break
            selected_variant = param_variant
        if selected_variant is None:
            raise RuntimeException(
                msg=f"No '{self.name}' function override with {[call_arg.__class__.__qualname__ for call_arg in call_args]} types found",
                pos=call_pos,
            )
        return self.body(*call_args)


@dataclass(order=True)
class IntValue(Value, Additive, Subtractive, Multiplicative):
    value: int
    members: dict[str, Cell] = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        self.members = {
            "toString": Cell(BuiltInFunc("toString", [[]], self.to_string)),
            "toFloat": Cell(BuiltInFunc("toFloat", [[]], self.to_float)),
        }

    def truthy(self) -> bool:
        return self.value != 0

    def to_string(self) -> "StringValue":
        return StringValue(str(self.value))

    def to_float(self) -> "FloatValue":
        return FloatValue(float(self.value))

    def type_of(self) -> "StringValue":
        return StringValue("Int")

    def __add__(self, other: "IntValue") -> "IntValue":
        return IntValue(self.value + other.value)

    def __sub__(self, other: "IntValue") -> "IntValue":
        return IntValue(self.value - other.value)

    def __mul__(self, other: "IntValue") -> "IntValue":
        return IntValue(self.value * other.value)

    def __floordiv__(self, other: "IntValue") -> "IntValue":
        if other.value == 0:
            raise ZeroDivisionError
        return IntValue(self.value // other.value)

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass(order=True)
class FloatValue(Value, Additive, Subtractive, Multiplicative):
    value: float
    members: dict[str, Cell] = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        self.members = {
            "toString": Cell(BuiltInFunc("toString", [[]], self.to_string)),
            "toInt": Cell(BuiltInFunc("toInt", [[]], self.to_int)),
        }

    def truthy(self):
        return self.value != 0.0

    def to_string(self) -> "StringValue":
        return StringValue(str(self.value))

    def to_int(self) -> "IntValue":
        return IntValue(int(self.value))

    def type_of(self) -> "StringValue":
        return StringValue("Float")

    def __add__(self, other: "FloatValue") -> "FloatValue":
        return FloatValue(self.value + other.value)

    def __sub__(self, other: "FloatValue") -> "FloatValue":
        return FloatValue(self.value - other.value)

    def __mul__(self, other: "FloatValue") -> "FloatValue":
        return FloatValue(self.value * other.value)

    def __truediv__(self, other: "FloatValue") -> "FloatValue":
        if other.value == 0.0:
            raise ZeroDivisionError
        return FloatValue(self.value / other.value)

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass(order=True)
class StringValue(Value, Additive):
    value: str
    members: dict[str, Cell] = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        self.members = {
            "toInt": Cell(BuiltInFunc("toInt", [[]], self.to_int)),
            "toFloat": Cell(BuiltInFunc("toFloat", [[]], self.to_float)),
        }

    def truthy(self):
        return self.value != ""

    def length(self):
        return IntValue(len(self.value))

    def to_float(self, node: po.ParserObject) -> "FloatValue":
        try:
            return FloatValue(float(self.value))
        except ValueError:
            msg = f"Cannot cast '{self.value}' to Float"
            raise RuntimeException(msg, pos=node.pos)

    def to_int(self, node: po.ParserObject) -> "IntValue":
        try:
            return IntValue(int(self.value))
        except ValueError:
            msg = f"Cannot cast '{self.value}' to Int"
            raise RuntimeException(msg, pos=node.pos)

    def type_of(self) -> "StringValue":
        return StringValue("String")

    def __add__(self, other: "StringValue"):
        return StringValue(self.value + other.value)

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass
class BoolValue(Value):
    value: bool

    def truthy(self):
        return self.value

    def type_of(self) -> "StringValue":
        return StringValue("Bool")

    def __str__(self) -> str:
        return f"{self.value}"


_SIMPLE_TYPES = (IntValue, FloatValue, StringValue, BoolValue)


def is_simple(val: "Value") -> bool:
    return isinstance(val, _SIMPLE_TYPES)


@dataclass
class ItemValue(Value):
    key: Value
    value: Value
    members: dict[str, Cell] = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        self.members = {
            "key": Cell(BuiltInFunc("key", [[]], self.get_key)),
            "value": Cell(BuiltInFunc("value", [[]], self.get_value)),
        }

    def get_key(self) -> Value:
        return self.key

    def get_value(self) -> Value:
        return self.value

    def type_of(self):
        return StringValue("Item")

    def __str__(self) -> str:
        return f"({self.key}: {self.value})"


@dataclass(order=False)
class Collection(Value):
    elements: list[Value] = field(default_factory=list)

    def truthy(self):
        return len(self.elements) > 0

    def length(self) -> IntValue:
        return IntValue(len(self.elements))


@dataclass
class ListValue(Collection, Additive):
    members: dict[str, Cell] = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        self.members = {
            "length": Cell(BuiltInFunc("length", [[]], self.length)),
            "get": Cell(BuiltInFunc("get", [[ItemValue]], self.get)),
            "add": Cell(BuiltInFunc("add", [[Value]], self.add)),
            "set": Cell(BuiltInFunc("set", [[IntValue, Value]], self.set)),
            "remove": Cell(BuiltInFunc("remove", [[IntValue]], self.remove)),
        }

    def __add__(self, other: "ListValue"):
        return ListValue(self.elements + other.elements)

    def type_of(self) -> "StringValue":
        return StringValue("List")

    def get(self, index: IntValue) -> Value:
        if index.value < 0 or index.value >= self.length().value:
            raise IndexError(f"Index {index.value} out of range")
        return self.elements[index.value]

    def add(self, value: Value):
        self.elements.append(value)

    def set(self, index: IntValue, value: Value):
        if index.value < 0 or index.value >= self.length().value:
            raise IndexError(f"Index {index.value} out of range")
        self.elements[index.value] = value

    def remove(self, index: IntValue):
        if index.value < 0 or index.value >= self.length().value:
            raise IndexError(f"Index {index.value} out of range")
        self.elements.pop(index.value)

    def __str__(self) -> str:
        return f"List({self.length().value})"

    def str_long(self) -> str:
        elements = ", ".join([str(item) for item in self.elements])
        return "[" + elements + "]"


@dataclass
class DictValue(Collection, Additive):
    order_func: "FuncValue" = None
    members: dict[str, Cell] = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        self.members = {
            "addNew": Cell(BuiltInFunc("addNew", [[Value, Value]], self.add_new)),
            "add": Cell(BuiltInFunc("add", [[ItemValue]], self.add)),
            "remove": Cell(BuiltInFunc("remove", [[Value]], self.remove)),
            "contains": Cell(BuiltInFunc("contains", [[Value]], self.contains)),
            "get": Cell(BuiltInFunc("get", [[Value]], self.get)),
        }

    def add_new(self, key: Value, value: Value):
        if self.contains(key).value:
            raise KeyError(f"Key {key} already exists in the dictionary")
        if not is_simple(key):
            raise KeyError(f"{key.__class__.__qualname__} can't be an item key")

        for i, item in enumerate(self.elements):
            if self.order_func(key, item.get_key()) < IntValue(0):
                self.elements.insert(i, ItemValue(key, value))
                return
        self.elements.append(ItemValue(key, value))

    def add(self, item: ItemValue):
        self.add_new(item.get_key(), item.get_value())

    def remove(self, key: Value):
        for i, item in enumerate(self.elements):
            if item.get_key() == key:
                self.elements.pop(i)
                return
        raise KeyError(f"Key {key} not found in the dictionary")

    def contains(self, key: Value) -> BoolValue:
        for item in self.elements:
            if item.get_key() == key:
                return BoolValue(True)
        return BoolValue(False)

    def get(self, key: Value) -> Value:
        for item in self.elements:
            if item.get_key() == key:
                return item
        raise KeyError(f"Key {key} not found in the dictionary")

    def type_of(self) -> "StringValue":
        return StringValue("Dict")

    def __add__(self, other: "DictValue"):
        for item in other.elements:
            self.add(item)
        return self

    def __str__(self) -> str:
        return f"Dict({self.length().value})"

    def str_long(self) -> str:
        elements = ", ".join([str(item) for item in self.elements])
        return "{" + elements + "}"


@dataclass
class FuncValue(Value):
    params: list[str]
    body: po.Block
    closure: Env

    def type_of(self) -> StringValue:
        return StringValue("FuncValue")


    def get_call_env(
        self, args: list["Value"], call_pos: tuple[int, int]
    ) -> "Value | None":
        if len(args) != len(self.params):
            raise RuntimeException(
                msg=f"Function takes {len(self.params)} arguments, {len(args)} given",
                pos=call_pos,
            )

        local_env = Env(self.closure)

        for name, arg in zip(self.params, args):
            local_env.define(name, deepcopy(arg) if is_simple(arg) else arg)

        return local_env
